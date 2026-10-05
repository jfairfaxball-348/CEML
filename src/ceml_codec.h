/* CanonicalCodec: UENC/MAG integer framing, frozen CEML-SCI-1 digest domains,
 * and the exact CEML-CKPT-1 state.bin and metadata.json encodings.
 * These are immutable adapters to docs/CHECKPOINT_SPEC.md,
 * docs/SECURITY_AND_INTEGRITY.md and schemas/checkpoint_metadata.schema.json.
 * Integers cross this boundary only as canonical bytes, never as host limbs. */
#ifndef CEML_CODEC_H
#define CEML_CODEC_H

#include <stddef.h>
#include <gmp.h>

#define CEML_HEX 65            /* 64 lowercase hex characters and a terminator */
#define CEML_BODY_PREFIX 18    /* ASCII label and one NUL byte */

typedef struct { unsigned char *data; size_t length, capacity; } ceml_buffer;

typedef struct {
    char run_id[129];
    mpz_t sequence, body_bytes, shortcut_steps, odd_steps, standard_steps;
    int has_previous;
    char previous_metadata_digest[CEML_HEX];
    char manifest_digest[CEML_HEX], original_start_digest[CEML_HEX];
    char protocol_commit[CEML_HEX], engine_commit[CEML_HEX];
    char build_digest[CEML_HEX], machine_profile_digest[CEML_HEX], validation_evidence_digest[CEML_HEX];
    char body_digest[CEML_HEX], current_value_digest[CEML_HEX], metadata_digest[CEML_HEX];
    int terminal_reached;
} ceml_metadata;

void ceml_buffer_init(ceml_buffer *buffer);
void ceml_buffer_free(ceml_buffer *buffer);
int ceml_buffer_append(ceml_buffer *buffer, const void *data, size_t length);

/* SHA3-256(ASCII(label) || 00 || data), rendered as lowercase hex. */
void ceml_domain_digest(const char *label, const unsigned char *data, size_t length, char hex[CEML_HEX]);

int ceml_is_hex(const char *text, size_t minimum, size_t maximum);
int ceml_is_decimal(const char *text);

/* UENC(x) = U64BE(len(MAG(x))) || MAG(x) for x >= 0, MAG(0) = 00. The decoder
 * rejects non-minimal magnitudes, length mismatch and trailing bytes. */
int ceml_uenc_append(ceml_buffer *out, const mpz_t value);
int ceml_uenc_decode(const unsigned char *data, size_t length, mpz_t value);

/* state.bin = "CEML-CKPT-BODY-V1" || 00 || U64BE(len(MAG(n))) || MAG(n), n >= 1. */
int ceml_body_encode(const mpz_t n, ceml_buffer *body);
/* Rejects wrong label, zero, non-minimal magnitude, length mismatch and trailing bytes. */
int ceml_body_decode(const unsigned char *body, size_t length, mpz_t n);

void ceml_metadata_init(ceml_metadata *metadata);
void ceml_metadata_clear(ceml_metadata *metadata);
/* RFC 8785 JCS bytes of the metadata, with or without the self digest member. */
int ceml_metadata_emit(const ceml_metadata *metadata, int with_digest, ceml_buffer *out);
/* Fills body/current digests from the body and computes metadata_digest. */
int ceml_metadata_seal(ceml_metadata *metadata, const unsigned char *body, size_t body_length);
/* Computes metadata_digest once every other member is set. */
int ceml_metadata_finish(ceml_metadata *metadata);
/* Emits state.bin through sink in bounded chunks while computing the body and
 * current-value digests incrementally; sets body_bytes and both digests. */
typedef int (*ceml_sink)(const void *data, size_t length, void *context);
int ceml_body_stream(const mpz_t n, ceml_sink sink, void *context, ceml_metadata *metadata);
/* Strict canonical decode of metadata.json; verifies the self digest. */
int ceml_metadata_parse(const unsigned char *json, size_t length, ceml_metadata *metadata);
/* Full CEML-CKPT-1 pair validation; on success n receives the exact value. */
int ceml_checkpoint_validate(const ceml_metadata *metadata, const unsigned char *body, size_t body_length, mpz_t n);

#endif
