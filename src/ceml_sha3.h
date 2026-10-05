/* FIPS 202 SHA3-256 and SHAKE256 (August 2015). Byte-oriented, portable C17.
 * Frozen-primitive adapter for CEML-SCI-1 digests and engineering digests. */
#ifndef CEML_SHA3_H
#define CEML_SHA3_H

#include <stddef.h>
#include <stdint.h>

typedef struct {
    uint64_t state[25];
    unsigned char buffer[136];
    size_t used;
    int squeezing;
} ceml_keccak;

void ceml_sha3_256_init(ceml_keccak *context);
void ceml_shake256_init(ceml_keccak *context);
void ceml_keccak_update(ceml_keccak *context, const void *data, size_t length);
void ceml_sha3_256_final(ceml_keccak *context, unsigned char digest[32]);
/* May be called repeatedly; the first call ends absorption. */
void ceml_shake256_squeeze(ceml_keccak *context, unsigned char *output, size_t length);
void ceml_hex(const unsigned char *bytes, size_t length, char *text);   /* writes 2*length+1 chars */

#endif
