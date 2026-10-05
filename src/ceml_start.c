/* ceml-start-v1 (docs/RANDOMNESS_AND_REPRODUCIBILITY.md): immutable adapter.
 * This file never obtains a seed. During C1 it is exercised only with the
 * public non-scientific test seed of the frozen vectors. */
#include "ceml_start.h"
#include "ceml_sha3.h"

#include <stdlib.h>
#include <string.h>

static void power_of_ten(mpz_t out, unsigned long long exponent) {
    mpz_t base;
    mpz_init_set_ui(base, 10);
    mpz_set_ui(out, 1);
    while (exponent) {
        if (exponent & 1) mpz_mul(out, out, base);
        exponent >>= 1;
        if (exponent) mpz_mul(base, base, base);
    }
    mpz_clear(base);
}

static int append_small(ceml_buffer *out, unsigned long long value) {
    mpz_t z;
    int ok;
    mpz_init(z);
    mpz_import(z, 1, 1, sizeof(value), 0, 0, &value);
    ok = ceml_uenc_append(out, z);
    mpz_clear(z);
    return ok;
}

int ceml_start_generate(const unsigned char seed[32], unsigned long long digits, unsigned long long rung_index, mpz_t n,
                        unsigned long long *accepted_retry) {
    static const char prefix[] = "CEML-SCIENTIFIC-START-V1";
    mpz_t a, m, x;
    size_t bits, bytes;
    unsigned char *random;
    unsigned long long retry;
    int ok = 0;
    if (digits < 1) return 0;
    mpz_inits(a, m, x, NULL);
    if (digits == 1) mpz_set_ui(a, 1); else { power_of_ten(a, digits - 1); mpz_add_ui(a, a, 1); }
    power_of_ten(m, digits); mpz_sub_ui(m, m, 1); mpz_sub(m, m, a); mpz_tdiv_q_2exp(m, m, 1); mpz_add_ui(m, m, 1);
    mpz_sub_ui(x, m, 1);
    bits = mpz_sgn(x) == 0 ? 0 : mpz_sizeinbase(x, 2);      /* bit_length(M_D - 1) */
    bytes = (bits + 7) >> 3;
    /* The pinned LLP64 GMP counts bits in 32 bits; larger rungs fail closed here. */
    random = bits > 0xfffffff0UL ? NULL : (unsigned char *)malloc(bytes ? bytes : 1);
    for (retry = 0; random; ++retry) {
        ceml_buffer message;
        ceml_keccak shake;
        ceml_buffer_init(&message);
        if (!ceml_buffer_append(&message, prefix, sizeof(prefix)) || !ceml_buffer_append(&message, seed, 32) ||
            !append_small(&message, digits) || !append_small(&message, rung_index) || !append_small(&message, retry)) {
            ceml_buffer_free(&message);
            break;
        }
        ceml_shake256_init(&shake);
        ceml_keccak_update(&shake, message.data, message.length);
        ceml_shake256_squeeze(&shake, random, bytes);
        ceml_buffer_free(&message);
        mpz_import(x, bytes, 1, 1, 1, 0, random);
        mpz_fdiv_r_2exp(x, x, (mp_bitcnt_t)bits);                       /* mask away the unused top bits */
        if (mpz_cmp(x, m) >= 0) continue;                    /* rejection depends only on generator output */
        mpz_mul_2exp(x, x, 1);
        mpz_add(n, a, x);
        *accepted_retry = retry;
        ok = 1;
        break;
    }
    free(random);
    mpz_clears(a, m, x, NULL);
    return ok;
}

int ceml_start_digest(const mpz_t n, char hex[CEML_HEX]) {
    ceml_buffer encoded;
    int ok;
    ceml_buffer_init(&encoded);
    ok = ceml_uenc_append(&encoded, n);
    if (ok) ceml_domain_digest("CEML-START-V1", encoded.data, encoded.length, hex);
    ceml_buffer_free(&encoded);
    return ok;
}

void ceml_seed_commitment(const unsigned char seed[32], char hex[CEML_HEX]) {
    ceml_domain_digest("CEML-SCIENTIFIC-SEED-COMMIT-V1", seed, 32, hex);
}
