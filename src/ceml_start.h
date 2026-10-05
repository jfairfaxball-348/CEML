#ifndef CEML_START_H
#define CEML_START_H

#include "ceml_codec.h"

/* Deterministic rejection-sampled start for decimal-digit rung `digits` at zero-based
 * ladder position `rung_index`. The caller supplies the 32 raw seed bytes. */
int ceml_start_generate(const unsigned char seed[32], unsigned long long digits, unsigned long long rung_index, mpz_t n,
                        unsigned long long *accepted_retry);
int ceml_start_digest(const mpz_t n, char hex[CEML_HEX]);
void ceml_seed_commitment(const unsigned char seed[32], char hex[CEML_HEX]);

#endif
