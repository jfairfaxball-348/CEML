/* CEML exact engine: canonical T-boundary state, centralized counters, affine
 * blocks, hierarchical batching, terminal safety and the route registry.
 * Implements docs/CODEX_HANDOFF.md sections 2.1, 2.3-2.9 and 3. The definition
 * oracle lives separately in ceml_oracle.c and shares no code with this file.
 * Only documented public GMP mpz functions are used; no fixed-width value can
 * hold a state, a counter or a coefficient of a block longer than CEML_LEAF. */
#ifndef CEML_ENGINE_H
#define CEML_ENGINE_H

#include <stdint.h>
#include <gmp.h>

#define CEML_LEAF 20UL              /* 3^20 and the leaf additive constant fit 32 bits */
#define CEML_MAX_TABLE_WIDTH 16UL
#define CEML_AUDIT_PRIME 4294967291UL

enum {                               /* stable route identifiers, I1 section 6 */
    CEML_ROUTE_DIRECT_T, CEML_ROUTE_SMALL_AFFINE, CEML_ROUTE_HIER_EXPLICIT, CEML_ROUTE_STATE_DENSE,
    CEML_ROUTE_GMP_PUBLIC, CEML_ROUTE_ALLOC_COPY, CEML_ROUTE_ALLOC_REUSE, CEML_ROUTE_PARALLEL_SINGLE,
    CEML_ROUTE_TERMINAL_T, CEML_ROUTE_TERMINAL_U, CEML_ROUTE_AUDIT_DIVISIBILITY, CEML_ROUTE_AUDIT_MODULAR,
    CEML_ROUTE_CHECKPOINT_BUFFERED, CEML_ROUTE_CHECKPOINT_STREAMING, CEML_ROUTE_COUNT
};
extern const char *const CEML_ROUTE_ID[CEML_ROUTE_COUNT];

enum { CEML_MACRO_DIRECT, CEML_MACRO_SMALL, CEML_MACRO_HIER };
enum { CEML_AUDIT_STRUCTURAL, CEML_AUDIT_DIVISIBILITY, CEML_AUDIT_MODULAR };
enum { CEML_REQUEST_AUTO, CEML_REQUEST_REQUIRE, CEML_REQUEST_FORBID };

enum {                               /* engine outcomes; every nonzero value fails closed */
    CEML_OK = 0, CEML_E_ARGUMENT, CEML_E_MEMORY, CEML_E_TABLE, CEML_E_DIVISIBILITY, CEML_E_SPLIT, CEML_E_MODULAR,
    CEML_E_COUNTER, CEML_E_TERMINAL, CEML_E_ROUTE_FORBIDDEN, CEML_E_ROUTE_NOT_ACTIVATED, CEML_E_FALLBACK, CEML_E_BOUND
};

enum {                               /* validation-only fault injection (V1 hook 9); CEML_FAULT_NONE in production */
    CEML_FAULT_NONE, CEML_FAULT_PARITY, CEML_FAULT_COEFFICIENT_A, CEML_FAULT_COEFFICIENT_B, CEML_FAULT_LOW_BITS,
    CEML_FAULT_PRODUCT, CEML_FAULT_COUNTER, CEML_FAULT_COMPOSITION_ORDER
};

typedef struct {                     /* exact scientific state at a shortcut-map boundary */
    mpz_t n, shortcut_steps, odd_steps, standard_steps;
    int terminal_reached;
} ceml_state;

typedef struct { mpz_t a, b; unsigned long k, i; } ceml_block;      /* 2^k T^k(n) = a n + b, a = 3^i */
typedef struct { uint32_t a, b; uint8_t odd; } ceml_small;

typedef struct {
    int macro;                       /* CEML_MACRO_* */
    unsigned long width;             /* table width for CEML_MACRO_SMALL */
    unsigned long divisor, cap;      /* k = max(1, min(cap, floor(bit_length(n) / divisor))) */
    int copy;                        /* alloc.copy when nonzero, alloc.reuse otherwise */
    int audit;                       /* CEML_AUDIT_* */
    int terminal_odd_only;           /* terminal.odd_only when nonzero, terminal.direct_t otherwise */
    int request[CEML_ROUTE_COUNT];   /* CEML_REQUEST_* per route */
} ceml_config;

typedef struct {
    ceml_config config;
    ceml_small *table;
    mpz_t scratch;                   /* persistent product buffer for alloc.reuse */
    unsigned long long activated[CEML_ROUTE_COUNT];
    unsigned long long fallback_count;
    unsigned long long trace_digest_state[4];   /* deterministic running trace of (route, k, i) */
    int trace;
    int fault;
    unsigned long fault_countdown;
} ceml_engine;

/* The frozen C1 profile defaults (local_reports/ENGINEERING_DECISIONS.json). */
void ceml_config_profile(ceml_config *config);

void ceml_state_init(ceml_state *state);
void ceml_state_clear(ceml_state *state);
int ceml_state_set(ceml_state *state, const mpz_t n);          /* counters zero; n >= 1 */
int ceml_state_check(const ceml_state *state);                 /* counter and terminal invariants */

void ceml_block_init(ceml_block *block);
void ceml_block_clear(ceml_block *block);
/* Base block built directly from elementary T on a residue below 2^k, k <= CEML_LEAF. */
int ceml_leaf(uint64_t residue, unsigned long k, uint32_t *a, uint32_t *b, unsigned long *odd);
/* Explicit-coefficient binary splitting for the residue r = n mod 2^k, any k >= 1. */
int ceml_block_build(ceml_engine *engine, ceml_block *block, const mpz_t residue, unsigned long k);
/* Reconstruct a block from its parity word (bit j = parity of step j); used by validation. */
int ceml_block_from_parity(ceml_block *block, const mpz_t parity_word, unsigned long k);
/* P2 after P1: a = a2 a1, b = a2 b1 + b2 2^k1. */
void ceml_block_compose(ceml_block *out, const ceml_block *first, const ceml_block *second);
/* n <- (a n + b) / 2^k with the configured audit and allocation modes. */
int ceml_block_apply(ceml_engine *engine, mpz_t n, const mpz_t a, const mpz_t b, unsigned long k);

int ceml_engine_init(ceml_engine *engine, const ceml_config *config);   /* builds and checks any table */
void ceml_engine_clear(ceml_engine *engine);
void ceml_engine_reset_routes(ceml_engine *engine);
/* Advance by exactly `budget` shortcut steps, or to the first occurrence of 1 when
 * budget is 0, never past it. max_macros bounds the number of scheduler iterations
 * (0 = unbounded) so a caller can checkpoint between macros. */
int ceml_engine_advance(ceml_engine *engine, ceml_state *state, unsigned long budget, unsigned long max_macros,
                        unsigned long *performed);
/* REQUIRE routes must have executed and no fallback may have occurred. */
int ceml_engine_check_routes(const ceml_engine *engine);
/* Terminal-safe macro length for a nonterminal state: at most bit_length(n) - 1. */
unsigned long ceml_macro_length(const ceml_config *config, const mpz_t n);
const char *ceml_error_text(int code);

#endif
