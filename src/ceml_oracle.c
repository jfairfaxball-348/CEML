/* DefinitionOracle (docs/CODEX_HANDOFF.md section 2.2 and 2.3).
 *
 * Deliberately elementary and separately written: it calls no affine block,
 * no table, no production low-bit helper, no scheduler and nothing else from
 * ceml_engine.c. The direct C path is the definition-level independence
 * anchor; T and U are the other elementary definitions. */
#include "ceml_oracle.h"

void ceml_oracle_c(mpz_t n) {
    if (mpz_even_p(n)) mpz_divexact_ui(n, n, 2);        /* C(n) = n/2 */
    else { mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1); }   /* C(n) = 3n+1 */
}

unsigned long ceml_oracle_t(mpz_t n) {
    if (mpz_even_p(n)) { mpz_divexact_ui(n, n, 2); return 0; }   /* T(n) = n/2 */
    mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1);
    mpz_divexact_ui(n, n, 2);                                    /* T(n) = (3n+1) / 2 */
    return 1;
}

unsigned long ceml_oracle_u(mpz_t n) {
    unsigned long v = 0;
    mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1);
    while (mpz_even_p(n)) { mpz_divexact_ui(n, n, 2); ++v; }     /* v = v2(3n+1), retained exactly */
    return v;
}

void ceml_oracle_run_c(mpz_t n, mpz_t shortcut, mpz_t odd, mpz_t standard, unsigned long budget) {
    unsigned long done = 0;
    mpz_set_ui(shortcut, 0); mpz_set_ui(odd, 0); mpz_set_ui(standard, 0);
    while (mpz_cmp_ui(n, 1) != 0 && (budget == 0 || done < budget)) {
        if (mpz_odd_p(n)) {
            ceml_oracle_c(n);                 /* 3n+1: not yet a T boundary */
            mpz_add_ui(standard, standard, 1);
            mpz_add_ui(odd, odd, 1);
        }
        ceml_oracle_c(n);                     /* the halving reaches the T boundary */
        mpz_add_ui(standard, standard, 1);
        mpz_add_ui(shortcut, shortcut, 1);
        ++done;
    }
}

void ceml_oracle_run_t(mpz_t n, mpz_t shortcut, mpz_t odd, unsigned long budget) {
    unsigned long done = 0;
    mpz_set_ui(shortcut, 0); mpz_set_ui(odd, 0);
    while (mpz_cmp_ui(n, 1) != 0 && (budget == 0 || done < budget)) {
        mpz_add_ui(odd, odd, ceml_oracle_t(n));
        mpz_add_ui(shortcut, shortcut, 1);
        ++done;
    }
}
