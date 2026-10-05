/* Fixed-schema scientific records owned by the CanonicalCodec: strict canonical
 * CEML-RUN-MANIFEST-1 decoding and CEML-RESULT-1 emission. Both are reachable
 * only behind the E1 gate; C1 exercises them with synthetic public vectors. */
#ifndef CEML_RECORDS_H
#define CEML_RECORDS_H

#include "ceml_codec.h"

typedef struct {
    char run_id[129], created_at[48];
    char build_digest[CEML_HEX], engine_commit[CEML_HEX], machine_profile_digest[CEML_HEX], manifest_digest[CEML_HEX];
    char protocol_commit[CEML_HEX], validation_evidence_digest[CEML_HEX];
    char seed_commitment[CEML_HEX], seed_hex[CEML_HEX], start_digest[CEML_HEX];
    char retry[24], start_bit_length[24], start_decimal_digits[24], decimal_digits[24], rung_index[24];
} ceml_manifest;

/* Strict canonical decode with self-digest verification. */
int ceml_manifest_parse(const unsigned char *json, size_t length, ceml_manifest *manifest);

typedef struct {
    const char *run_id, *manifest_digest, *protocol_commit, *engine_commit, *build_digest, *machine_profile_digest;
    const char *validation_evidence_digest, *seed_commitment, *start_digest, *decimal_digits, *rung_index;
    const char *status, *status_detail;          /* status_detail NULL for completed */
    const char *final_value;                     /* canonical decimal or NULL */
    const char *shortcut_steps, *odd_steps, *standard_steps;
    char final_checkpoint_digest[CEML_HEX];      /* empty string renders null */
    char result_digest[CEML_HEX];
} ceml_result;

/* Computes result_digest over the JCS bytes without that member, then emits. */
int ceml_result_emit(ceml_result *result, ceml_buffer *out);

#endif
