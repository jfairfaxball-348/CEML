#include "ceml_engine.h"

#include <limits.h>
#include <stdlib.h>
#include <string.h>

const char *const CEML_ROUTE_ID[CEML_ROUTE_COUNT] = {
    "engine.direct_t", "engine.small_affine", "engine.hier_affine.explicit", "state.dense", "arith.gmp.public",
    "alloc.copy", "alloc.reuse", "parallel.single", "terminal.direct_t", "terminal.odd_only", "audit.divisibility",
    "audit.modular", "checkpoint.buffered", "checkpoint.streaming" };

const char *ceml_error_text(int code) {
    static const char *const TEXT[] = { "ok", "invalid-argument", "out-of-memory", "table-entry-mismatch",
        "divisibility-canary", "split-length", "modular-audit", "counter-invariant", "terminal-invariant",
        "route-forbidden", "required-route-not-activated", "fallback-occurred", "bound-exceeded" };
    return code >= 0 && code <= CEML_E_BOUND ? TEXT[code] : "unknown";
}

void ceml_config_profile(ceml_config *config) {
    memset(config, 0, sizeof(*config));
    config->macro = CEML_MACRO_HIER;
    config->width = 0;
    config->divisor = 2;
    config->cap = 16384;
    config->copy = 1;
    config->audit = CEML_AUDIT_DIVISIBILITY;
    config->terminal_odd_only = 0;
}

void ceml_state_init(ceml_state *s) {
    mpz_inits(s->n, s->shortcut_steps, s->odd_steps, s->standard_steps, NULL);
    mpz_set_ui(s->n, 1);
    s->terminal_reached = 1;
}

void ceml_state_clear(ceml_state *s) { mpz_clears(s->n, s->shortcut_steps, s->odd_steps, s->standard_steps, NULL); }

int ceml_state_set(ceml_state *s, const mpz_t n) {
    if (mpz_sgn(n) <= 0) return CEML_E_ARGUMENT;
    mpz_set(s->n, n);
    mpz_set_ui(s->shortcut_steps, 0); mpz_set_ui(s->odd_steps, 0); mpz_set_ui(s->standard_steps, 0);
    s->terminal_reached = mpz_cmp_ui(n, 1) == 0;
    return CEML_OK;
}

int ceml_state_check(const ceml_state *s) {
    mpz_t sum;
    int ok;
    if (mpz_sgn(s->n) <= 0) return CEML_E_TERMINAL;
    if ((mpz_cmp_ui(s->n, 1) == 0) != (s->terminal_reached != 0)) return CEML_E_TERMINAL;
    if (mpz_sgn(s->shortcut_steps) < 0 || mpz_sgn(s->odd_steps) < 0 || mpz_cmp(s->odd_steps, s->shortcut_steps) > 0)
        return CEML_E_COUNTER;
    mpz_init(sum);
    mpz_add(sum, s->shortcut_steps, s->odd_steps);
    ok = mpz_cmp(sum, s->standard_steps) == 0;
    mpz_clear(sum);
    return ok ? CEML_OK : CEML_E_COUNTER;
}

void ceml_block_init(ceml_block *block) { mpz_inits(block->a, block->b, NULL); block->k = block->i = 0; mpz_set_ui(block->a, 1); }

void ceml_block_clear(ceml_block *block) { mpz_clears(block->a, block->b, NULL); }

static int touch(ceml_engine *e, int route, unsigned long k, unsigned long i) {
    if (e->config.request[route] == CEML_REQUEST_FORBID) return CEML_E_ROUTE_FORBIDDEN;
    ++e->activated[route];
    if (e->trace)
        e->trace_digest_state[0] = (e->trace_digest_state[0] ^ ((unsigned long long)route << 48 ^ (unsigned long long)k << 24 ^ i))
                                   * 1099511628211ULL;
    return CEML_OK;
}

/* One-shot validation fault: fires when the countdown reaches zero. */
static int fault_now(ceml_engine *e, int kind) {
    if (e->fault != kind) return 0;
    if (e->fault_countdown) { --e->fault_countdown; return 0; }
    e->fault = CEML_FAULT_NONE;
    return 1;
}

/* For k <= 20: a = 3^i <= 3^20 < 2^32, b <= 3^20 - 2^20 < 2^32, and the iterated
 * residue stays below 2^20 (3/2)^20 + 1 < 2^33, so 64-bit arithmetic is exact. */
static int leaf_core(uint64_t residue, unsigned long k, int flip_first, uint32_t *a, uint32_t *b, unsigned long *odd) {
    uint64_t A = 1, B = 0;
    unsigned long j, i = 0;
    if (k > CEML_LEAF || (k < 64 && residue >> k)) return CEML_E_ARGUMENT;
    for (j = 0; j < k; ++j) {
        int parity = (int)(residue & 1);
        if (flip_first && j == 0) parity ^= 1;      /* validation-only parity fault */
        if (parity) { B = 3*B + ((uint64_t)1 << j); A *= 3; ++i; residue = (3*residue + 1) >> 1; }
        else residue >>= 1;
    }
    if (A > 0xffffffffULL || B > 0xffffffffULL) return CEML_E_BOUND;
    *a = (uint32_t)A; *b = (uint32_t)B; *odd = i;
    return CEML_OK;
}

int ceml_leaf(uint64_t residue, unsigned long k, uint32_t *a, uint32_t *b, unsigned long *odd) {
    return leaf_core(residue, k, 0, a, b, odd);
}

void ceml_block_compose(ceml_block *out, const ceml_block *first, const ceml_block *second) {
    mpz_t t, u;
    mpz_inits(t, u, NULL);
    mpz_mul(t, second->a, first->b);              /* a2 b1 */
    mpz_mul_2exp(u, second->b, first->k);         /* b2 2^k1 */
    mpz_add(t, t, u);
    mpz_mul(u, second->a, first->a);              /* a2 a1 */
    mpz_set(out->b, t); mpz_set(out->a, u);
    out->k = first->k + second->k; out->i = first->i + second->i;
    mpz_clears(t, u, NULL);
}

int ceml_block_from_parity(ceml_block *block, const mpz_t parity_word, unsigned long k) {
    unsigned long j;
    mpz_t power;
    mpz_init_set_ui(power, 1);
    mpz_set_ui(block->a, 1); mpz_set_ui(block->b, 0); block->i = 0; block->k = k;
    for (j = 0; j < k; ++j) {
        if (mpz_tstbit(parity_word, j)) {
            mpz_mul_ui(block->b, block->b, 3); mpz_add(block->b, block->b, power);
            mpz_mul_ui(block->a, block->a, 3); ++block->i;
        }
        mpz_mul_2exp(power, power, 1);
    }
    mpz_clear(power);
    return CEML_OK;
}

int ceml_block_build(ceml_engine *e, ceml_block *p, const mpz_t r, unsigned long k) {
    int rc = CEML_OK;
    if (k == 0 || mpz_sgn(r) < 0 || mpz_sizeinbase(r, 2) > k) return CEML_E_ARGUMENT;
    if (k <= CEML_LEAF) {
        uint32_t a, b;
        unsigned long odd;
        uint64_t residue = (uint64_t)mpz_get_ui(r) & (((uint64_t)1 << k) - 1);
        if (fault_now(e, CEML_FAULT_LOW_BITS)) residue ^= 1;
        rc = leaf_core(residue, k, fault_now(e, CEML_FAULT_PARITY), &a, &b, &odd);
        if (rc) return rc;
        mpz_set_ui(p->a, a); mpz_set_ui(p->b, b); p->k = k; p->i = odd;
    } else {
        unsigned long k1 = k >> 1, k2 = k - k1;
        ceml_block left, right;
        mpz_t low, mid;
        ceml_block_init(&left); ceml_block_init(&right);
        mpz_inits(low, mid, NULL);
        mpz_fdiv_r_2exp(low, r, k1);                       /* first residue: r mod 2^k1 */
        rc = ceml_block_build(e, &left, low, k1);
        if (!rc) {
            mpz_mul(mid, left.a, r); mpz_add(mid, mid, left.b);   /* exact splice before reduction */
            if (e->config.audit != CEML_AUDIT_STRUCTURAL) {
                rc = touch(e, CEML_ROUTE_AUDIT_DIVISIBILITY, k1, 0);
                if (!rc && !mpz_divisible_2exp_p(mid, k1)) rc = CEML_E_DIVISIBILITY;
            }
        }
        if (!rc) {
            mpz_tdiv_q_2exp(mid, mid, k1);
            mpz_fdiv_r_2exp(low, mid, k2);                 /* right input is the post-left residue */
            rc = ceml_block_build(e, &right, low, k2);
        }
        if (!rc && (left.k != k1 || right.k != k2 || k1 + k2 != k)) rc = CEML_E_SPLIT;
        if (!rc) {
            if (fault_now(e, CEML_FAULT_COMPOSITION_ORDER)) ceml_block_compose(p, &right, &left);
            else ceml_block_compose(p, &left, &right);     /* P2 after P1 */
        }
        mpz_clears(low, mid, NULL);
        ceml_block_clear(&left); ceml_block_clear(&right);
    }
    return rc;
}

static unsigned long power_mod(unsigned long exponent) {
    uint64_t result = 1, base = 2;
    while (exponent) {
        if (exponent & 1) result = result*base % CEML_AUDIT_PRIME;
        base = base*base % CEML_AUDIT_PRIME;
        exponent >>= 1;
    }
    return (unsigned long)result;
}

int ceml_block_apply(ceml_engine *e, mpz_t n, const mpz_t a, const mpz_t b, unsigned long k) {
    unsigned long before = 0, am = 0, bm = 0;
    mpz_t fresh;
    mpz_ptr product;
    int rc;
    if (e->config.audit == CEML_AUDIT_MODULAR) {
        before = mpz_fdiv_ui(n, CEML_AUDIT_PRIME); am = mpz_fdiv_ui(a, CEML_AUDIT_PRIME); bm = mpz_fdiv_ui(b, CEML_AUDIT_PRIME);
    }
    rc = touch(e, e->config.copy ? CEML_ROUTE_ALLOC_COPY : CEML_ROUTE_ALLOC_REUSE, k, 0);
    if (rc) return rc;
    /* alloc.copy uses fresh temporaries every time; alloc.reuse keeps one scratch value. */
    if (e->config.copy) { mpz_init(fresh); product = fresh; } else product = e->scratch;
    mpz_mul(product, a, n); mpz_add(product, product, b);
    if (fault_now(e, CEML_FAULT_PRODUCT)) mpz_combit(product, k + 1);
    if (e->config.audit != CEML_AUDIT_STRUCTURAL) {
        rc = touch(e, CEML_ROUTE_AUDIT_DIVISIBILITY, k, 0);
        if (!rc && !mpz_divisible_2exp_p(product, k)) rc = CEML_E_DIVISIBILITY;
    }
    if (!rc) {
        if (e->config.copy) {
            mpz_t next;
            mpz_init(next);
            mpz_tdiv_q_2exp(next, product, k);
            mpz_swap(n, next);
            mpz_clear(next);
        } else mpz_tdiv_q_2exp(n, product, k);
    }
    if (e->config.copy) mpz_clear(fresh);
    if (!rc && e->config.audit == CEML_AUDIT_MODULAR) {
        uint64_t left = ((uint64_t)am*before + bm) % CEML_AUDIT_PRIME;
        rc = touch(e, CEML_ROUTE_AUDIT_MODULAR, k, 0);
        if (!rc && left != (uint64_t)power_mod(k)*mpz_fdiv_ui(n, CEML_AUDIT_PRIME) % CEML_AUDIT_PRIME) rc = CEML_E_MODULAR;
    }
    if (!rc) rc = touch(e, CEML_ROUTE_GMP_PUBLIC, k, 0);
    if (!rc) rc = touch(e, CEML_ROUTE_STATE_DENSE, k, 0);
    return rc;
}

/* One exact shortcut step on the production side (not the definition oracle). */
static int elementary(ceml_engine *e, mpz_t n, unsigned long *odd) {
    int rc = touch(e, e->config.copy ? CEML_ROUTE_ALLOC_COPY : CEML_ROUTE_ALLOC_REUSE, 1, 0);
    if (rc) return rc;
    *odd = mpz_odd_p(n) ? 1UL : 0UL;
    if (e->config.copy) {
        mpz_t next;
        mpz_init(next);
        if (*odd) { mpz_mul_ui(next, n, 3); mpz_add_ui(next, next, 1); mpz_tdiv_q_2exp(next, next, 1); }
        else mpz_tdiv_q_2exp(next, n, 1);
        mpz_swap(n, next);
        mpz_clear(next);
    } else {
        if (*odd) { mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1); }
        mpz_tdiv_q_2exp(n, n, 1);
    }
    rc = touch(e, CEML_ROUTE_GMP_PUBLIC, 1, *odd);
    return rc ? rc : touch(e, CEML_ROUTE_STATE_DENSE, 1, *odd);
}

static int build_table(ceml_engine *e, unsigned long width) {
    unsigned long count = 1UL << width, r;
    e->table = (ceml_small *)malloc(sizeof(ceml_small)*count);
    if (!e->table) return CEML_E_MEMORY;
    for (r = 0; r < count; ++r) {
        uint64_t x = (uint64_t)count + r, direct = x;
        unsigned long j, odd;
        int rc = leaf_core(r, width, 0, &e->table[r].a, &e->table[r].b, &odd);
        if (rc) return rc;
        e->table[r].odd = (uint8_t)odd;
        for (j = 0; j < width; ++j) direct = (direct & 1) ? (3*direct + 1) >> 1 : direct >> 1;
        x = x*e->table[r].a + e->table[r].b;
        if ((x & (count - 1)) != 0 || (x >> width) != direct) return CEML_E_TABLE;
    }
    return CEML_OK;
}

int ceml_engine_init(ceml_engine *e, const ceml_config *config) {
    memset(e, 0, sizeof(*e));
    e->config = *config;
    mpz_init(e->scratch);
    if (config->macro == CEML_MACRO_SMALL) {
        if (config->width < 4 || config->width > CEML_MAX_TABLE_WIDTH || config->width % 4) return CEML_E_ARGUMENT;
        return build_table(e, config->width);
    }
    if (config->macro == CEML_MACRO_HIER) {
        if (config->divisor != 2 && config->divisor != 3 && config->divisor != 4 && config->divisor != 6 && config->divisor != 8)
            return CEML_E_ARGUMENT;
        if (config->cap != 1024 && config->cap != 4096 && config->cap != 16384) return CEML_E_ARGUMENT;
    } else if (config->macro != CEML_MACRO_DIRECT) return CEML_E_ARGUMENT;
    return CEML_OK;
}

void ceml_engine_clear(ceml_engine *e) { free(e->table); e->table = NULL; mpz_clear(e->scratch); }

void ceml_engine_reset_routes(ceml_engine *e) {
    memset(e->activated, 0, sizeof(e->activated));
    e->fallback_count = 0;
    memset(e->trace_digest_state, 0, sizeof(e->trace_digest_state));
}

int ceml_engine_check_routes(const ceml_engine *e) {
    int route;
    if (e->fallback_count) return CEML_E_FALLBACK;
    for (route = 0; route < CEML_ROUTE_COUNT; ++route)
        if (e->config.request[route] == CEML_REQUEST_REQUIRE && e->activated[route] == 0) return CEML_E_ROUTE_NOT_ACTIVATED;
    return CEML_OK;
}

unsigned long ceml_macro_length(const ceml_config *config, const mpz_t n) {
    size_t bits = mpz_sizeinbase(n, 2);
    size_t k = bits/config->divisor;
    if (k > config->cap) k = config->cap;
    if (k < 1) k = 1;
    if (k > bits - 1) k = bits - 1;          /* first-1 safety: k <= bit_length(n) - 1 */
    return (unsigned long)k;
}

/* Centralized accounting: kernels report (k, i); only this function updates counters. */
static int account(ceml_engine *e, ceml_state *s, unsigned long k, unsigned long i) {
    if (k == 0 || i > k) return CEML_E_COUNTER;
    if (fault_now(e, CEML_FAULT_COUNTER)) ++i;
    mpz_add_ui(s->shortcut_steps, s->shortcut_steps, k);
    mpz_add_ui(s->odd_steps, s->odd_steps, i);
    mpz_add_ui(s->standard_steps, s->standard_steps, k);
    mpz_add_ui(s->standard_steps, s->standard_steps, i);
    if (mpz_sgn(s->n) <= 0) return CEML_E_TERMINAL;
    s->terminal_reached = mpz_cmp_ui(s->n, 1) == 0;
    return CEML_OK;
}

int ceml_engine_advance(ceml_engine *e, ceml_state *s, unsigned long budget, unsigned long max_macros,
                        unsigned long *performed) {
    ceml_block block;
    mpz_t low, a, b;
    unsigned long done = 0, macros = 0;
    int rc = ceml_state_check(s);
    if (performed) *performed = 0;
    if (rc) return rc;
    ceml_block_init(&block);
    mpz_inits(low, a, b, NULL);
    while (!rc && !s->terminal_reached && (budget == 0 || done < budget) && (max_macros == 0 || macros < max_macros)) {
        size_t bits = mpz_sizeinbase(s->n, 2);
        unsigned long remaining = budget ? budget - done : ULONG_MAX, k = 1, i = 0;
        if (e->config.macro == CEML_MACRO_DIRECT) {
            rc = touch(e, CEML_ROUTE_DIRECT_T, 1, 0);
            if (!rc) rc = elementary(e, s->n, &i);
        } else if (e->config.macro == CEML_MACRO_SMALL) {
            unsigned long width = e->config.width;
            if (remaining < width || bits - 1 < width) {
                /* Declared, counted handoff: REQUIRE(engine.small_affine) fails closed on it. */
                ++e->fallback_count;
                rc = touch(e, CEML_ROUTE_TERMINAL_T, 1, 0);
                if (!rc) rc = elementary(e, s->n, &i);
            } else {
                const ceml_small *entry = &e->table[mpz_fdiv_ui(s->n, 1UL << width)];
                rc = touch(e, CEML_ROUTE_SMALL_AFFINE, width, entry->odd);
                if (!rc) {
                    mpz_set_ui(a, entry->a); mpz_set_ui(b, entry->b);
                    rc = ceml_block_apply(e, s->n, a, b, width);
                }
                k = width; i = entry->odd;
            }
        } else {
            k = ceml_macro_length(&e->config, s->n);
            if (k < 2) {
                /* Exact terminal handoff: one elementary T, or one exact odd-only run. */
                if (e->config.terminal_odd_only) {
                    rc = touch(e, CEML_ROUTE_TERMINAL_U, 1, 0);
                    if (!rc) {
                        unsigned long v;
                        if (mpz_odd_p(s->n)) { mpz_mul_ui(s->n, s->n, 3); mpz_add_ui(s->n, s->n, 1); i = 1; }
                        v = (unsigned long)mpz_scan1(s->n, 0);
                        k = v > remaining ? remaining : v;      /* an exact prefix of the run when budgeted */
                        mpz_tdiv_q_2exp(s->n, s->n, k);
                        rc = touch(e, CEML_ROUTE_GMP_PUBLIC, k, i);
                        if (!rc) rc = touch(e, CEML_ROUTE_STATE_DENSE, k, i);
                    }
                } else {
                    rc = touch(e, CEML_ROUTE_TERMINAL_T, 1, 0);
                    if (!rc) rc = elementary(e, s->n, &i);
                    k = 1;
                }
            } else {
                if (k > remaining) k = remaining;
                mpz_fdiv_r_2exp(low, s->n, k);                  /* exactly n mod 2^k */
                rc = ceml_block_build(e, &block, low, k);
                if (!rc && block.k != k) rc = CEML_E_SPLIT;
                if (!rc && fault_now(e, CEML_FAULT_COEFFICIENT_A)) mpz_add_ui(block.a, block.a, 2);
                if (!rc && fault_now(e, CEML_FAULT_COEFFICIENT_B)) mpz_combit(block.b, k + 2);
                if (!rc) rc = touch(e, CEML_ROUTE_HIER_EXPLICIT, k, block.i);
                if (!rc) rc = ceml_block_apply(e, s->n, block.a, block.b, k);
                i = block.i;
            }
        }
        if (!rc) rc = account(e, s, k, i);
        done += k; ++macros;
    }
    if (!rc) rc = touch(e, CEML_ROUTE_PARALLEL_SINGLE, 0, 0);
    if (!rc) rc = ceml_state_check(s);
    mpz_clears(low, a, b, NULL);
    ceml_block_clear(&block);
    if (performed) *performed = done;
    return rc;
}
