/* ceml: command surface of docs/CODEX_HANDOFF.md section 15.
 *
 * Authorization boundaries. The executable reads PROGRAM_STATUS.md from the
 * current directory and fails closed:
 *   validate        refuses unless the authoritative current phase is V1;
 *   prepare, run    refuse unless the phase is E1 and scientific execution is
 *                   AUTHORIZED, and then only for a digest-valid manifest whose
 *                   start regenerates exactly;
 *   checkpoint, resume   outside `run` accept only identities marked
 *                   non-scientific (c1-synthetic-, v1-validation-).
 * hardware-report, calibrate, decide and build-profile are C1 orchestration
 * commands implemented by the tools/c1 scripts; `--calibration-only` is the
 * bounded child entry they launch. This program never obtains a seed. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ceml_calibrate.h"
#include "ceml_engine.h"
#include "ceml_fs.h"
#include "ceml_records.h"
#include "ceml_start.h"
#include "ceml_store.h"
#include "ceml_validate.h"

#define CHECKPOINT_INTERVAL_SECONDS 600ULL     /* decision.matrix.09.checkpoint cadence */
#define STATUS_FILE "PROGRAM_STATUS.md"

static int refuse(const char *command, const char *reason) {
    printf("{\"command\":\"%s\",\"status\":\"refused\",\"reason\":\"%s\"}\n", command, reason);
    return 3;
}

/* 0 = unreadable, otherwise bit 1: C1, bit 2: V1, bit 4: E1 with scientific execution authorized. */
static int programme_gate(void) {
    ceml_buffer text;
    int gate = 0;
    ceml_buffer_init(&text);
    if (ceml_fs_read_all(STATUS_FILE, &text, 1 << 20) && ceml_buffer_append(&text, "", 1)) {
        const char *s = (const char *)text.data;
        if (strlen(s) + 1 == text.length) {                       /* no embedded NUL */
            if (strstr(s, "**Authoritative current phase:** C1")) gate |= 1;
            if (strstr(s, "**Authoritative current phase:** V1")) gate |= 2;
            if (strstr(s, "**Authoritative current phase:** E1") &&
                strstr(s, "**Scientific execution authorization:** AUTHORIZED")) gate |= 4;
        }
    }
    ceml_buffer_free(&text);
    return gate;
}

static int run_hooks(const char *command, int full, const char *scratch) {
    ceml_hook_result result;
    unsigned long long failures = 0;
    int index;
    printf("{\"command\":\"%s\",\"mode\":\"%s\",\"classes\":{", command, full ? "full-suite" : "bounded-developer");
    for (index = 0; index < CEML_HOOK_COUNT; ++index) {
        ceml_hook_run(index, full, scratch, &result);
        failures += result.failures + (result.cases == 0);
        printf("%s\"%s\":{\"cases\":\"%llu\",\"failures\":\"%llu\"}", index ? "," : "", CEML_HOOK_NAME[index], result.cases,
               result.failures);
    }
    printf("},\"status\":\"%s\",\"note\":\"%s\"}\n", failures ? "FAIL" : "PASS",
           full ? "class results only; V1 evidence assembly and acceptance are a separate reviewed step"
                : "bounded developer invariants and frozen vectors; this is not V1 and not V1-PASS");
    return failures ? 1 : 0;
}

static int command_status(const char *directory) {
    ceml_recovery recovery;
    ceml_fs_capability capability;
    int gate = programme_gate();
    printf("{\"command\":\"status\",\"programme_status_readable\":%s,\"phase\":\"%s\",\"validate_enabled\":%s,"
           "\"scientific_run_enabled\":%s}\n", gate ? "true" : "false", gate & 4 ? "E1" : gate & 2 ? "V1" : gate & 1 ? "C1" : "unknown",
           gate & 2 ? "true" : "false", gate & 4 ? "true" : "false");
    if (directory) {                                             /* read-only artifact validity report */
        ceml_recovery_init(&recovery);
        ceml_fs_describe(directory, &capability);
        ceml_store_recover(directory, NULL, &recovery);
        ceml_print_recovery(&recovery, capability.directory_flush_supported);
        ceml_recovery_clear(&recovery);
    }
    return 0;
}

/* Non-scientific checkpoint write of a state supplied on standard input. */
static int command_checkpoint(const char *strategy) {
    char directory[512];
    ceml_identity identity;
    ceml_store_timing timing;
    mpz_t n, shortcut, odd;
    int streaming = strcmp(strategy, "streaming") == 0, ok;
    if (!streaming && strcmp(strategy, "buffered") != 0) return refuse("checkpoint", "unknown-strategy");
    mpz_inits(n, shortcut, odd, NULL);
    if (!ceml_read_synthetic_identity(directory, sizeof(directory), &identity) || !ceml_read_synthetic_state(n, shortcut, odd))
        return refuse("checkpoint", "only-nonscientific-identities-and-exact-states-are-accepted-outside-run");
    ok = ceml_store_promote(directory, &identity, n, shortcut, odd, streaming, &timing);
    printf("{\"command\":\"checkpoint\",\"status\":\"%s\"}\n", ok ? "promoted" : "refused");
    return ok ? 0 : 4;
}

/* Non-scientific fresh-process resume: recover, rebuild caches, advance, promote. */
static int command_resume(const char *steps_text) {
    char directory[512];
    ceml_identity identity;
    ceml_recovery recovery;
    ceml_config config;
    ceml_engine engine;
    ceml_state state;
    ceml_store_timing timing;
    ceml_fs_capability capability;
    unsigned long steps = strtoul(steps_text, NULL, 10);
    int rc;
    if (!ceml_read_synthetic_identity(directory, sizeof(directory), &identity))
        return refuse("resume", "only-nonscientific-identities-are-accepted-outside-run");
    ceml_recovery_init(&recovery);
    if (ceml_store_recover(directory, &identity, &recovery) != CEML_STORE_OK) return refuse("resume", "no-unique-valid-checkpoint");
    ceml_config_profile(&config);
    ceml_state_init(&state);
    mpz_set(state.n, recovery.n);
    mpz_set(state.shortcut_steps, recovery.metadata.shortcut_steps);
    mpz_set(state.odd_steps, recovery.metadata.odd_steps);
    mpz_set(state.standard_steps, recovery.metadata.standard_steps);
    state.terminal_reached = recovery.metadata.terminal_reached;
    rc = ceml_engine_init(&engine, &config);
    if (!rc) rc = ceml_engine_advance(&engine, &state, steps, 0, NULL);     /* steps 0: to the first 1 */
    if (rc) return refuse("resume", ceml_error_text(rc));
    if (!ceml_store_promote(directory, &identity, state.n, state.shortcut_steps, state.odd_steps, 0, &timing))
        return refuse("resume", "promotion-failed");
    ceml_recovery_clear(&recovery);
    ceml_recovery_init(&recovery);
    ceml_fs_describe(directory, &capability);
    ceml_store_recover(directory, &identity, &recovery);
    ceml_print_recovery(&recovery, capability.directory_flush_supported);
    return recovery.status == CEML_STORE_OK ? 0 : 4;
}

static int hex_to_bytes(const char *hex, unsigned char *out, size_t count) {
    size_t i;
    for (i = 0; i < count; ++i) {
        unsigned value = 0;
        int j;
        for (j = 0; j < 2; ++j) {
            char c = hex[2*i + j];
            value = value*16 + (unsigned)(c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10);
        }
        out[i] = (unsigned char)value;
    }
    return 1;
}

/* Verify a manifest and regenerate its start; never chooses or rerolls anything. */
static int verify_manifest(const char *path, ceml_manifest *manifest, mpz_t start, const char **reason) {
    ceml_buffer json;
    unsigned char seed[32];
    char digest[CEML_HEX], text[32];
    unsigned long long retry = 0, digits, index;
    int ok;
    ceml_buffer_init(&json);
    *reason = "manifest-unreadable-or-noncanonical-or-digest-mismatch";
    ok = ceml_fs_read_all(path, &json, 1 << 20) && ceml_manifest_parse(json.data, json.length, manifest);
    ceml_buffer_free(&json);
    if (!ok) return 0;
    digits = strtoull(manifest->decimal_digits, NULL, 10);
    index = strtoull(manifest->rung_index, NULL, 10);
    hex_to_bytes(manifest->seed_hex, seed, 32);
    ceml_seed_commitment(seed, digest);
    *reason = "seed-commitment-mismatch";
    if (strcmp(digest, manifest->seed_commitment) != 0) return 0;
    *reason = "start-regeneration-mismatch";
    if (!ceml_start_generate(seed, digits, index, start, &retry) || !ceml_start_digest(start, digest) ||
        strcmp(digest, manifest->start_digest) != 0) return 0;
    snprintf(text, sizeof(text), "%llu", retry);
    if (strcmp(text, manifest->retry) != 0) return 0;
    snprintf(text, sizeof(text), "%llu", (unsigned long long)mpz_sizeinbase(start, 2));
    if (strcmp(text, manifest->start_bit_length) != 0 || strcmp(manifest->start_decimal_digits, manifest->decimal_digits) != 0) return 0;
    /* Rung membership follows from the generator's finite domain; the digest binds the value. */
    return mpz_odd_p(start) != 0;
}

static int command_prepare(const char *path) {
    ceml_manifest manifest;
    const char *reason;
    mpz_t start;
    int ok;
    if (!(programme_gate() & 4)) return refuse("prepare", "E1-not-authorized-by-PROGRAM_STATUS");
    mpz_init(start);
    ok = verify_manifest(path, &manifest, start, &reason);
    mpz_clear(start);
    if (!ok) return refuse("prepare", reason);
    printf("{\"command\":\"prepare\",\"status\":\"verified\",\"manifest_digest\":\"%s\",\"start_digest\":\"%s\"}\n",
           manifest.manifest_digest, manifest.start_digest);
    return 0;
}

static char *decimal_of(const mpz_t value) { return mpz_get_str(NULL, 10, value); }

static int write_result(const char *directory, const ceml_manifest *manifest, const ceml_state *state, const char *status,
                        const char *detail, const char *checkpoint_digest) {
    ceml_result result;
    ceml_buffer json;
    ceml_file *file = NULL;
    char path[900], temporary[900];
    int ok;
    memset(&result, 0, sizeof(result));
    result.run_id = manifest->run_id; result.manifest_digest = manifest->manifest_digest;
    result.protocol_commit = manifest->protocol_commit; result.engine_commit = manifest->engine_commit;
    result.build_digest = manifest->build_digest; result.machine_profile_digest = manifest->machine_profile_digest;
    result.validation_evidence_digest = manifest->validation_evidence_digest; result.seed_commitment = manifest->seed_commitment;
    result.start_digest = manifest->start_digest; result.decimal_digits = manifest->decimal_digits;
    result.rung_index = manifest->rung_index; result.status = status; result.status_detail = detail;
    result.final_value = decimal_of(state->n); result.shortcut_steps = decimal_of(state->shortcut_steps);
    result.odd_steps = decimal_of(state->odd_steps); result.standard_steps = decimal_of(state->standard_steps);
    if (checkpoint_digest) strcpy_s(result.final_checkpoint_digest, CEML_HEX, checkpoint_digest);
    ceml_buffer_init(&json);
    snprintf(path, sizeof(path), "%s\\result.json", directory);
    snprintf(temporary, sizeof(temporary), "%s\\result.json.tmp", directory);
    ceml_fs_remove_file(temporary);
    ok = ceml_result_emit(&result, &json) && (file = ceml_fs_create_new(temporary)) != NULL;
    if (ok) {
        ok = ceml_fs_write_exact(file, json.data, json.length) && ceml_fs_flush(file);
        ok = ceml_fs_close(file) && ok;
        ok = ok && ceml_fs_atomic_promote(temporary, path, 1) && ceml_fs_durable_directory(directory) != 0;
    }
    if (ok) printf("{\"command\":\"run\",\"status\":\"%s\",\"result_digest\":\"%s\"}\n", status, result.result_digest);
    ceml_buffer_free(&json);
    return ok;
}

/* Scientific execution. Reachable only under an E1 programme status. */
static int command_run(const char *manifest_path, const char *directory) {
    ceml_manifest manifest;
    ceml_identity identity;
    ceml_recovery recovery;
    ceml_config config;
    ceml_engine engine;
    ceml_state state;
    ceml_store_timing timing;
    const char *reason;
    mpz_t start;
    unsigned long long last, frequency = ceml_fs_ticks_per_second();
    int rc, status;
    if (!(programme_gate() & 4)) return refuse("run", "E1-not-authorized-by-PROGRAM_STATUS");
    mpz_init(start);
    if (!verify_manifest(manifest_path, &manifest, start, &reason)) return refuse("run", reason);
    memset(&identity, 0, sizeof(identity));
    strcpy_s(identity.run_id, sizeof(identity.run_id), manifest.run_id);
    strcpy_s(identity.manifest_digest, CEML_HEX, manifest.manifest_digest);
    strcpy_s(identity.original_start_digest, CEML_HEX, manifest.start_digest);
    strcpy_s(identity.protocol_commit, CEML_HEX, manifest.protocol_commit);
    strcpy_s(identity.engine_commit, CEML_HEX, manifest.engine_commit);
    strcpy_s(identity.build_digest, CEML_HEX, manifest.build_digest);
    strcpy_s(identity.machine_profile_digest, CEML_HEX, manifest.machine_profile_digest);
    strcpy_s(identity.validation_evidence_digest, CEML_HEX, manifest.validation_evidence_digest);
    ceml_recovery_init(&recovery);
    ceml_state_init(&state);
    status = ceml_store_recover(directory, &identity, &recovery);
    if (status == CEML_STORE_EMPTY) ceml_state_set(&state, start);
    else if (status == CEML_STORE_OK) {
        mpz_set(state.n, recovery.n);
        mpz_set(state.shortcut_steps, recovery.metadata.shortcut_steps);
        mpz_set(state.odd_steps, recovery.metadata.odd_steps);
        mpz_set(state.standard_steps, recovery.metadata.standard_steps);
        state.terminal_reached = recovery.metadata.terminal_reached;
    } else return refuse("run", status == CEML_STORE_PROVENANCE ? "provenance_failure" : "integrity_failure");
    ceml_config_profile(&config);
    rc = ceml_engine_init(&engine, &config);
    if (!rc && status == CEML_STORE_EMPTY &&
        !ceml_store_promote(directory, &identity, state.n, state.shortcut_steps, state.odd_steps, 0, &timing))
        return refuse("run", "initial-checkpoint-failed");
    last = ceml_fs_ticks();
    while (!rc && !state.terminal_reached) {
        rc = ceml_engine_advance(&engine, &state, 0, 1, NULL);              /* one macro, then a safe boundary */
        if (!rc && !state.terminal_reached && (ceml_fs_ticks() - last) / frequency >= CHECKPOINT_INTERVAL_SECONDS) {
            if (!ceml_store_promote(directory, &identity, state.n, state.shortcut_steps, state.odd_steps, 0, &timing))
                return refuse("run", "resource_stop-checkpoint-promotion-failed");
            last = ceml_fs_ticks();
        }
    }
    if (rc) {       /* an invariant failure is never divergence; the last accepted checkpoint is preserved */
        ceml_store_recover(directory, &identity, &recovery);
        return write_result(directory, &manifest, &state, "validation_failure", ceml_error_text(rc), NULL) ? 5 : 6;
    }
    if (!ceml_store_promote(directory, &identity, state.n, state.shortcut_steps, state.odd_steps, 0, &timing) ||
        ceml_store_recover(directory, &identity, &recovery) != CEML_STORE_OK || !recovery.metadata.terminal_reached)
        return refuse("run", "terminal-checkpoint-failed");
    return write_result(directory, &manifest, &state, "completed", NULL, recovery.metadata.metadata_digest) ? 0 : 6;
}

/* Read-only verification of a checkpoint directory or a manifest file. */
static int command_verify(const char *kind, const char *path) {
    if (strcmp(kind, "checkpoint") == 0) {
        ceml_recovery recovery;
        ceml_fs_capability capability;
        ceml_recovery_init(&recovery);
        ceml_fs_describe(path, &capability);
        ceml_store_recover(path, NULL, &recovery);
        ceml_print_recovery(&recovery, capability.directory_flush_supported);
        return recovery.status == CEML_STORE_OK ? 0 : 4;
    }
    if (strcmp(kind, "manifest") == 0) {
        ceml_manifest manifest;
        ceml_buffer json;
        int ok;
        ceml_buffer_init(&json);
        ok = ceml_fs_read_all(path, &json, 1 << 20) && ceml_manifest_parse(json.data, json.length, &manifest);
        ceml_buffer_free(&json);
        printf("{\"command\":\"verify\",\"artifact\":\"manifest\",\"canonical_and_digest_valid\":%s}\n", ok ? "true" : "false");
        return ok ? 0 : 4;
    }
    return refuse("verify", "unknown-artifact-kind");
}

int main(int argc, char **argv) {
    const char *command = argc > 1 ? argv[1] : "";
    if (strcmp(command, "--calibration-only") == 0) return ceml_calibration_entry(argc - 2, argv + 2);
    if (strcmp(command, "self-test") == 0) return run_hooks("self-test", 0, argc > 2 ? argv[2] : "ceml-self-test.tmp");
    if (strcmp(command, "validate") == 0) {
        if (!(programme_gate() & 2)) return refuse("validate", "V1-not-authorized-by-PROGRAM_STATUS");
        return run_hooks("validate", 1, argc > 2 ? argv[2] : "ceml-validate.tmp");
    }
    if (strcmp(command, "status") == 0) return command_status(argc > 2 ? argv[2] : NULL);
    if (strcmp(command, "prepare") == 0 && argc == 3) return command_prepare(argv[2]);
    if (strcmp(command, "run") == 0 && argc == 4) return command_run(argv[2], argv[3]);
    if (strcmp(command, "checkpoint") == 0 && argc == 3) return command_checkpoint(argv[2]);
    if (strcmp(command, "resume") == 0 && argc == 3) return command_resume(argv[2]);
    if (strcmp(command, "verify") == 0 && argc == 4) return command_verify(argv[2], argv[3]);
    if (strcmp(command, "hardware-report") == 0 || strcmp(command, "calibrate") == 0 || strcmp(command, "decide") == 0 ||
        strcmp(command, "build-profile") == 0)
        return refuse(command, "C1-orchestration-command-provided-by-tools-c1-ceml.py");
    printf("{\"status\":\"refused\",\"reason\":\"unknown-command\",\"commands\":\"self-test status verify checkpoint resume "
           "validate prepare run\"}\n");
    return 2;
}
