/* CheckpointStore: two-valid-generation CEML-CKPT-1 storage.
 *
 * Layout inside one run directory:
 *   directory gen-<sequence> holding state.bin and metadata.json   published, immutable
 *   <name>.tmp                                               unpublished or retiring
 *   latest                                                   operational hint only
 * A generation is published by one same-directory rename of a fully written,
 * flushed, re-read and validated temporary directory. The immediately
 * previous generation is retained; older ones are retired only after the new
 * one has been published, made durable as far as the adapter allows and
 * re-read. Recovery never trusts the pointer and never repairs anything. */
#ifndef CEML_STORE_H
#define CEML_STORE_H

#include "ceml_codec.h"

typedef struct {
    char run_id[129];
    char manifest_digest[CEML_HEX], original_start_digest[CEML_HEX];
    char protocol_commit[CEML_HEX], engine_commit[CEML_HEX];
    char build_digest[CEML_HEX], machine_profile_digest[CEML_HEX], validation_evidence_digest[CEML_HEX];
} ceml_identity;

enum {
    CEML_STORE_OK = 0,            /* unique newest valid generation selected */
    CEML_STORE_EMPTY = 1,         /* no published generation exists */
    CEML_STORE_INTEGRITY = 2,     /* a published generation at or above the newest valid one is invalid */
    CEML_STORE_AMBIGUOUS = 3,     /* sequence or previous-digest chain is inconsistent */
    CEML_STORE_PROVENANCE = 4,    /* a published generation belongs to another identity */
    CEML_STORE_IO = 5             /* the directory could not be read */
};

enum { CEML_POINTER_ABSENT = 0, CEML_POINTER_AGREES = 1, CEML_POINTER_IGNORED = 2 };

typedef struct {
    int status;
    ceml_metadata metadata;       /* of the selected generation when status is OK */
    mpz_t n;                      /* exact selected value */
    unsigned valid_generations, invalid_generations, temporary_entries, foreign_entries;
    int pointer;
} ceml_recovery;

typedef struct {
    unsigned long long serialization_ticks, write_ticks, flush_ticks, verify_ticks, promotion_ticks, directory_ticks,
                       retire_ticks, total_ticks;
    unsigned long long body_bytes, metadata_bytes;
    int directory_flush;          /* 1 performed, -1 unsupported by the adapter on this target */
    unsigned retired;
} ceml_store_timing;

void ceml_recovery_init(ceml_recovery *recovery);
void ceml_recovery_clear(ceml_recovery *recovery);

/* expected may be NULL to skip the identity comparison (status inspection). */
int ceml_store_recover(const char *directory, const ceml_identity *expected, ceml_recovery *recovery);

/* Writes generation (newest + 1) for an exact T-boundary state. streaming
 * selects chunked writes with incremental digests instead of one buffered
 * body. Returns 1 only after the published generation has been re-read. */
int ceml_store_promote(const char *directory, const ceml_identity *identity, const mpz_t n, const mpz_t shortcut_steps,
                       const mpz_t odd_steps, int streaming, ceml_store_timing *timing);

#endif
