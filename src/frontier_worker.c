/* GMP-only exact ascending first-descent worker. The Python driver supplies
 * source/status/run authorization and checks every frame independently. */
#include "frontier_worker.h"
#include "ceml_oracle.h"
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEMORY_LIMIT ((size_t)16u * 1024u * 1024u)
/* Pinned x64 malloc is 16-byte aligned. A 16-byte header preserves that
 * alignment; MSVC C does not expose the C11 max_align_t typedef. */
typedef union { size_t bytes; double alignment[2]; } allocation_header;
_Static_assert(sizeof(allocation_header) == 16u, "Pinned allocator header alignment");
_Static_assert(sizeof(unsigned long) == 4u, "Pinned LLP64 counter width");
_Static_assert(ULONG_MAX >= FRONTIER_MAX_TOTAL_T, "Finite budget fits counter");
static size_t memory_used = 0;
static mpz_t decimal_ceiling;

static void resource_exit(void) {
    fputs("UNRESOLVED memory resource refusal\n", stderr);
    fflush(stderr);
    _Exit(3);
}

static void *bounded_allocate(size_t bytes) {
    allocation_header *block;
    if (bytes > MEMORY_LIMIT || memory_used > MEMORY_LIMIT - bytes
            || bytes > SIZE_MAX - sizeof(*block)) resource_exit();
    block = (allocation_header *)malloc(sizeof(*block) + bytes);
    if (block == NULL) resource_exit();
    block->bytes = bytes;
    memory_used += bytes;
    return block + 1;
}

static void bounded_free(void *pointer, size_t old_bytes) {
    allocation_header *block;
    (void)old_bytes;
    if (pointer == NULL) return;
    block = (allocation_header *)pointer - 1;
    if (block->bytes > memory_used) resource_exit();
    memory_used -= block->bytes;
    free(block);
}

static void *bounded_reallocate(void *pointer, size_t old_bytes, size_t bytes) {
    allocation_header *block, *updated;
    size_t retained;
    (void)old_bytes;
    if (pointer == NULL) return bounded_allocate(bytes);
    block = (allocation_header *)pointer - 1;
    if (block->bytes > memory_used) resource_exit();
    retained = memory_used - block->bytes;
    if (bytes > MEMORY_LIMIT || retained > MEMORY_LIMIT - bytes
            || bytes > SIZE_MAX - sizeof(*block)) resource_exit();
    updated = (allocation_header *)realloc(block, sizeof(*block) + bytes);
    if (updated == NULL) resource_exit();
    updated->bytes = bytes;
    memory_used = retained + bytes;
    return updated + 1;
}

void frontier_memory_init(void) {
    mp_set_memory_functions(bounded_allocate, bounded_reallocate, bounded_free);
    mpz_init(decimal_ceiling);
    mpz_ui_pow_ui(decimal_ceiling, 10ul, FRONTIER_MAX_DECIMAL);
    mpz_sub_ui(decimal_ceiling, decimal_ceiling, 1ul);
}

int frontier_decimal(mpz_t value, const char *text, int positive) {
    size_t length = 0;
    if (text == NULL) return 0;
    while (text[length] != '\0') {
        if (length >= FRONTIER_MAX_DECIMAL || text[length] < '0' || text[length] > '9') return 0;
        ++length;
    }
    if (length == 0 || (length > 1 && text[0] == '0')
            || (positive && length == 1 && text[0] == '0')) return 0;
    if (mpz_set_str(value, text, 10) != 0 || mpz_sgn(value) < 0
            || mpz_sizeinbase(value, 2) > FRONTIER_MAX_BITS) return 0;
    return !positive || mpz_sgn(value) > 0;
}

int frontier_budget(unsigned long *value, const char *text, unsigned long ceiling) {
    mpz_t candidate, roundtrip;
    int valid = 0;
    mpz_inits(candidate, roundtrip, NULL);
    if (frontier_decimal(candidate, text, 1) && mpz_cmp_ui(candidate, ceiling) <= 0) {
        *value = mpz_get_ui(candidate);
        mpz_set_ui(roundtrip, *value);
        valid = mpz_cmp(candidate, roundtrip) == 0;
    }
    mpz_clears(candidate, roundtrip, NULL);
    return valid;
}

static int operand_ok(const mpz_t value) {
    return mpz_sgn(value) > 0 && mpz_sizeinbase(value, 2) <= FRONTIER_MAX_BITS
        && mpz_cmp(value, decimal_ceiling) <= 0;
}

static int t_step(mpz_t value, unsigned long *odd) {
    mpz_t next;
    int valid;
    if (!operand_ok(value)) return 0;
    mpz_init_set(next, value);
    if (mpz_odd_p(value)) {
        /* Guard 3*n+1 BEFORE allocating/computing the intermediate. */
        if (mpz_sizeinbase(value, 2) > FRONTIER_MAX_BITS - 2u) { mpz_clear(next); return 0; }
        mpz_mul_ui(next, next, 3ul);
        mpz_add_ui(next, next, 1ul);
        if (!mpz_divisible_ui_p(next, 2ul)) { mpz_clear(next); return 0; }
        mpz_divexact_ui(next, next, 2ul);
        *odd = 1ul;
    } else {
        mpz_divexact_ui(next, next, 2ul);
        *odd = 0ul;
    }
    valid = operand_ok(next);
    if (valid) mpz_set(value, next);
    mpz_clear(next);
    return valid;
}

static int decimal_out(char *output, size_t capacity, const mpz_t value) {
    size_t estimated, actual;
    if (!operand_ok(value)) return 0;
    estimated = mpz_sizeinbase(value, 10);
    /* GMP's decimal size can overestimate by one digit. */
    if (estimated > FRONTIER_MAX_DECIMAL + 1u || estimated > SIZE_MAX - 1u
            || estimated + 1u > capacity) return 0;
    if (mpz_get_str(output, 10, value) != output) return 0;
    actual = strlen(output);
    return actual > 0 && actual <= FRONTIER_MAX_DECIMAL && actual + 1u <= capacity;
}

static int emit(const mpz_t n, const char *rule, unsigned long steps,
                unsigned long odd, const mpz_t witness) {
    char number[FRONTIER_MAX_DECIMAL + 2u], result[FRONTIER_MAX_DECIMAL + 2u];
    char frame[FRONTIER_MAX_FRAME + 1u];
    int length;
    if (!decimal_out(number, sizeof(number), n)
            || !decimal_out(result, sizeof(result), witness)) return 0;
    length = snprintf(frame, sizeof(frame), "%s|%s|%lu|%lu|%s\n", number, rule, steps, odd, result);
    if (length <= 0 || (size_t)length >= sizeof(frame)) return 0;
    return fwrite(frame, 1u, (size_t)length, stdout) == (size_t)length && fflush(stdout) == 0;
}

static const char *classify(const mpz_t n) {
    if (mpz_even_p(n)) return "E2";
    if (mpz_cmp_ui(n, 5ul) >= 0 && mpz_fdiv_ui(n, 4ul) == 1ul) return "Q4";
    if (mpz_fdiv_ui(n, 3ul) == 2ul) return "P3";
    if (mpz_cmp_ui(n, 4ul) >= 0 && mpz_fdiv_ui(n, 9ul) == 4ul) return "M9";
    if (mpz_cmp_ui(n, 3ul) >= 0 && mpz_fdiv_ui(n, 16ul) == 3ul) return "S2K4-03";
    return "EXPLICIT";
}

int frontier_scan(const mpz_t start, const mpz_t end, unsigned long max_per, unsigned long max_total) {
    mpz_t n, witness;
    unsigned long total = 0;
    int status = 3;
    unsigned long pending_steps = 0, pending_odds = 0;
    const char *reason = "operand_limit";
    mpz_inits(n, witness, NULL);
    mpz_set(n, start);
    while (mpz_cmp(n, end) < 0) {
        const char *rule = classify(n);
        unsigned long steps = 0, odds = 0;
        pending_steps = 0;
        pending_odds = 0;
        mpz_set(witness, n);
        if (strcmp(rule, "E2") == 0) mpz_divexact_ui(witness, witness, 2ul);
        else if (strcmp(rule, "Q4") == 0) {
            mpz_sub_ui(witness, witness, 1ul);
            if (!mpz_divisible_ui_p(witness, 4ul)) goto unresolved;
            mpz_divexact_ui(witness, witness, 4ul);
            mpz_mul_ui(witness, witness, 3ul);
            mpz_add_ui(witness, witness, 1ul);
        } else if (strcmp(rule, "P3") == 0) {
            mpz_mul_ui(witness, witness, 2ul);
            mpz_sub_ui(witness, witness, 1ul);
            if (!mpz_divisible_ui_p(witness, 3ul)) goto unresolved;
            mpz_divexact_ui(witness, witness, 3ul);
        } else if (strcmp(rule, "M9") == 0) {
            mpz_mul_ui(witness, witness, 8ul);
            mpz_sub_ui(witness, witness, 5ul);
            if (!mpz_divisible_ui_p(witness, 9ul)) goto unresolved;
            mpz_divexact_ui(witness, witness, 9ul);
        } else if (strcmp(rule, "S2K4-03") == 0) {
            /* (9*n+5)/16, evaluated as 9*((n-3)/16)+2. */
            mpz_sub_ui(witness, witness, 3ul);
            if (!mpz_divisible_ui_p(witness, 16ul)) goto unresolved;
            mpz_divexact_ui(witness, witness, 16ul);
            mpz_mul_ui(witness, witness, 9ul);
            mpz_add_ui(witness, witness, 2ul);
        } else {
            do {
                unsigned long parity = 0;
                if (total >= max_total) {
                    reason = "total_budget";
                    goto unresolved;
                }
                if (steps >= max_per) {
                    reason = "step_budget";
                    goto unresolved;
                }
                /* Range proved by budgets before each fixed-width mutation. */
                if (steps == ULONG_MAX || total == ULONG_MAX || odds == ULONG_MAX
                        || !t_step(witness, &parity)) goto unresolved;
                ++steps;
                ++total;
                odds += parity;
                pending_steps = steps;
                pending_odds = odds;
            } while (mpz_cmp(witness, n) >= 0);
        }
        if (!operand_ok(witness) || mpz_cmp(witness, n) >= 0) goto unresolved;
        if (!emit(n, rule, steps, odds, witness)) {
            reason = "output_error";
            goto unresolved;
        }
        mpz_add_ui(n, n, 1ul);
    }
    if (fflush(stdout) != 0) { reason = "output_error"; goto unresolved; }
    fputs("COMPLETE\n", stderr);
    status = 0;
    goto done;
unresolved:
    /* n has not advanced; no partial result was sent as a successful event. */
    {
        char number[FRONTIER_MAX_DECIMAL + 2u], last[FRONTIER_MAX_DECIMAL + 2u];
        if (decimal_out(number, sizeof(number), n) && decimal_out(last, sizeof(last), witness))
            fprintf(stderr, "UNRESOLVED|%s|%s|%lu|%lu|%s\n", number, reason, pending_steps, pending_odds, last);
        else fputs("UNRESOLVED operand_limit\n", stderr);
    }
done:
    mpz_clears(n, witness, NULL);
    return status;
}

int frontier_identity(const mpz_t start, unsigned long steps) {
    mpz_t direct, shortcut;
    unsigned long i, odd = 0;
    char initial[FRONTIER_MAX_DECIMAL + 2u], final[FRONTIER_MAX_DECIMAL + 2u];
    int status = 3;
    mpz_inits(direct, shortcut, NULL);
    mpz_set(direct, start);
    mpz_set(shortcut, start);
    for (i = 0; i < steps; ++i) {
        unsigned long parity;
        if (!t_step(shortcut, &parity)) goto done;
        if (mpz_odd_p(direct)) ceml_oracle_c(direct);
        ceml_oracle_c(direct);
        if (mpz_cmp(direct, shortcut) != 0 || odd == ULONG_MAX) goto done;
        odd += parity;
    }
    if (!decimal_out(initial, sizeof(initial), start)
            || !decimal_out(final, sizeof(final), shortcut)
            || printf("%s|IDENTITY|%lu|%lu|%s|%lu\n", initial, steps, odd, final, steps + odd) < 0
            || fflush(stdout) != 0) goto done;
    fputs("COMPLETE IDENTITY TEST ONLY\n", stderr);
    status = 0;
done:
    if (status != 0) fputs("UNRESOLVED bounded identity resource refusal\n", stderr);
    mpz_clears(direct, shortcut, NULL);
    return status;
}

int frontier_table(void) {
    unsigned long residue;
    /* Tiny constants are table derivation only, never endpoints or T values
     * of a worker trajectory. Cross-check two independent constructions. */
    for (residue = 0; residue < 16ul; ++residue) {
        unsigned long value = residue, a = 1ul, b = 0ul, j;
        char parity[5];
        for (j = 0; j < 4ul; ++j) {
            unsigned long is_odd = value % 2ul;
            parity[j] = is_odd ? '1' : '0';
            if (is_odd) { value = (3ul * value + 1ul) / 2ul; a *= 3ul; b = 3ul*b + (1ul << j); }
            else value /= 2ul;
        }
        parity[4] = '\0';
        if ((a*residue + b) % 16ul != 0ul || (a*residue + b)/16ul != value
                || (residue == 3ul && (strcmp(parity, "1100") != 0 || a != 9ul || b != 5ul || value != 2ul))) {
            fputs("REFUSED parity table disagreement\n", stderr);
            return 2;
        }
        if (printf("%lu|%s|%lu|%lu|%lu\n", residue, parity, a, b, value) < 0) return 3;
    }
    if (fflush(stdout) != 0) return 3;
    fputs("COMPLETE TABLE TEST ONLY\n", stderr);
    return 0;
}
