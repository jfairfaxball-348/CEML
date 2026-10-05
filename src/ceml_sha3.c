/* FIPS 202 Keccak-f[1600] sponge with rate 136 bytes (capacity 512 bits).
 * SHA3-256 uses domain suffix 0x06; SHAKE256 uses 0x1f. No table of secrets,
 * no host-endianness dependence: lanes are loaded and stored little-endian. */
#include "ceml_sha3.h"

#include <string.h>

#define RATE 136

static const uint64_t ROUND_CONSTANT[24] = {
    0x0000000000000001ULL, 0x0000000000008082ULL, 0x800000000000808aULL, 0x8000000080008000ULL,
    0x000000000000808bULL, 0x0000000080000001ULL, 0x8000000080008081ULL, 0x8000000000008009ULL,
    0x000000000000008aULL, 0x0000000000000088ULL, 0x0000000080008009ULL, 0x000000008000000aULL,
    0x000000008000808bULL, 0x800000000000008bULL, 0x8000000000008089ULL, 0x8000000000008003ULL,
    0x8000000000008002ULL, 0x8000000000000080ULL, 0x000000000000800aULL, 0x800000008000000aULL,
    0x8000000080008081ULL, 0x8000000000008080ULL, 0x0000000080000001ULL, 0x8000000080008008ULL };
static const int ROTATION[24] = { 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 2, 14, 27, 41, 56, 8, 25, 43, 62, 18, 39, 61, 20, 44 };
static const int LANE[24] = { 10, 7, 11, 17, 18, 3, 5, 16, 8, 21, 24, 4, 15, 23, 19, 13, 12, 2, 20, 14, 22, 9, 6, 1 };

static uint64_t rotate(uint64_t value, int count) { return (value << count) | (value >> (64 - count)); }

static void permute(uint64_t a[25]) {
    int round, i, j;
    for (round = 0; round < 24; ++round) {
        uint64_t c[5], t;
        for (i = 0; i < 5; ++i) c[i] = a[i] ^ a[i + 5] ^ a[i + 10] ^ a[i + 15] ^ a[i + 20];
        for (i = 0; i < 5; ++i) {
            t = c[(i + 4) % 5] ^ rotate(c[(i + 1) % 5], 1);
            for (j = 0; j < 25; j += 5) a[j + i] ^= t;
        }
        t = a[1];
        for (i = 0; i < 24; ++i) { uint64_t keep = a[LANE[i]]; a[LANE[i]] = rotate(t, ROTATION[i]); t = keep; }
        for (j = 0; j < 25; j += 5) {
            for (i = 0; i < 5; ++i) c[i] = a[j + i];
            for (i = 0; i < 5; ++i) a[j + i] = c[i] ^ (~c[(i + 1) % 5] & c[(i + 2) % 5]);
        }
        a[0] ^= ROUND_CONSTANT[round];
    }
}

static void absorb_block(ceml_keccak *context, const unsigned char *block) {
    int i, b;
    for (i = 0; i < RATE/8; ++i) {
        uint64_t lane = 0;
        for (b = 7; b >= 0; --b) lane = (lane << 8) | block[8*i + b];
        context->state[i] ^= lane;
    }
    permute(context->state);
}

static void start(ceml_keccak *context, int squeezing) {
    memset(context, 0, sizeof(*context));
    context->squeezing = squeezing;
}

void ceml_sha3_256_init(ceml_keccak *context) { start(context, 0); }
void ceml_shake256_init(ceml_keccak *context) { start(context, 0); }

void ceml_keccak_update(ceml_keccak *context, const void *data, size_t length) {
    const unsigned char *bytes = (const unsigned char *)data;
    while (length) {
        size_t take = RATE - context->used;
        if (take > length) take = length;
        memcpy(context->buffer + context->used, bytes, take);
        context->used += take; bytes += take; length -= take;
        if (context->used == RATE) { absorb_block(context, context->buffer); context->used = 0; }
    }
}

static void finish(ceml_keccak *context, unsigned char suffix) {
    memset(context->buffer + context->used, 0, RATE - context->used);
    context->buffer[context->used] ^= suffix;
    context->buffer[RATE - 1] ^= 0x80;
    absorb_block(context, context->buffer);
    context->used = 0;
    context->squeezing = 1;
}

static void extract(ceml_keccak *context, unsigned char *output, size_t length) {
    while (length) {
        size_t i, take;
        if (context->used == RATE) { permute(context->state); context->used = 0; }
        take = RATE - context->used;
        if (take > length) take = length;
        for (i = 0; i < take; ++i) {
            size_t position = context->used + i;
            output[i] = (unsigned char)(context->state[position/8] >> (8*(position % 8)));
        }
        context->used += take; output += take; length -= take;
    }
}

void ceml_sha3_256_final(ceml_keccak *context, unsigned char digest[32]) {
    finish(context, 0x06);
    extract(context, digest, 32);
}

void ceml_shake256_squeeze(ceml_keccak *context, unsigned char *output, size_t length) {
    if (!context->squeezing) finish(context, 0x1f);
    extract(context, output, length);
}

void ceml_hex(const unsigned char *bytes, size_t length, char *text) {
    static const char digits[] = "0123456789abcdef";
    size_t i;
    for (i = 0; i < length; ++i) { text[2*i] = digits[bytes[i] >> 4]; text[2*i + 1] = digits[bytes[i] & 15]; }
    text[2*length] = 0;
}
