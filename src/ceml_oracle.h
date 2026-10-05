#ifndef CEML_ORACLE_H
#define CEML_ORACLE_H

#include <gmp.h>

void ceml_oracle_c(mpz_t n);                 /* one standard-map step, n >= 1 */
unsigned long ceml_oracle_t(mpz_t n);        /* one shortcut step; returns 1 if the input was odd */
unsigned long ceml_oracle_u(mpz_t n);        /* odd n: n <- (3n+1) / 2^v, returns v */
/* Direct C stepping compared at T boundaries. budget counts shortcut steps; 0 runs to the first 1. */
void ceml_oracle_run_c(mpz_t n, mpz_t shortcut, mpz_t odd, mpz_t standard, unsigned long budget);
void ceml_oracle_run_t(mpz_t n, mpz_t shortcut, mpz_t odd, unsigned long budget);

#endif
