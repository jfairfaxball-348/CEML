/* Stage: hardware characterization. Bounded synthetic CEML-CKPT-1 store cases
 * on the intended checkpoint filesystem. Non-scientific: the state, counters
 * and identity digests arrive from the fixed C1 driver and are synthetic.
 * The process can be made to terminate itself abruptly at one named write,
 * flush, promotion or retirement boundary for the interruption matrix. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>

#include "ceml_fs.h"
#include "ceml_store.h"

#define LINE 70000
#define MAX_STATE_BYTES 32768

static int read_line(char *line, size_t capacity) {
    size_t length;
    if (!fgets(line, (int)capacity, stdin)) return 0;
    length = strlen(line);
    while (length && (line[length-1] == '\n' || line[length-1] == '\r')) line[--length] = 0;
    return length > 0;
}

static int read_hex_field(char *line, char *out, size_t minimum) {
    if (!read_line(line, LINE) || !ceml_is_hex(line, minimum, 64)) return 0;
    strcpy_s(out, CEML_HEX, line);
    return 1;
}

static void print_number(const char *name, const mpz_t value, const char *tail) {
    char *text = mpz_get_str(NULL, 10, value);
    void (*release)(void *, size_t);
    printf("\"%s\":\"%s\"%s", name, text, tail);
    mp_get_memory_functions(NULL, NULL, &release);
    release(text, strlen(text) + 1);
}

int main(int argc, char **argv) {
    static char line[LINE], directory[512];
    ceml_identity identity;
    ceml_fs_capability capability;
    mpz_t n, shortcut, odd;
    unsigned long count, i;
    int streaming, promote;
    if (argc != 6 || strcmp(argv[1], "--calibration-only") != 0) return 2;
    promote = strcmp(argv[2], "promote") == 0;
    if (!promote && strcmp(argv[2], "recover") != 0) return 2;
    streaming = strcmp(argv[3], "streaming") == 0;
    if (promote && !streaming && strcmp(argv[3], "buffered") != 0) return 2;
    if (strcmp(argv[4], "none") != 0) ceml_fs_set_fault(argv[4]);
    count = strtoul(argv[5], NULL, 10);
    if (count < 1 || count > 4) return 2;
    memset(&identity, 0, sizeof(identity));
    if (!read_line(line, sizeof(directory))) return 2;
    strcpy_s(directory, sizeof(directory), line);
    if (strstr(directory, "..") || directory[0] == '\\' || strchr(directory, ':')) return 2;   /* relative, contained */
    if (!read_line(line, sizeof(identity.run_id))) return 2;
    strcpy_s(identity.run_id, sizeof(identity.run_id), line);
    if (strncmp(identity.run_id, "c1-synthetic-", 13) != 0) return 2;   /* never a scientific run identity */
    if (!read_hex_field(line, identity.manifest_digest, 64) || !read_hex_field(line, identity.original_start_digest, 64) ||
        !read_hex_field(line, identity.protocol_commit, 40) || !read_hex_field(line, identity.engine_commit, 40) ||
        !read_hex_field(line, identity.build_digest, 64) || !read_hex_field(line, identity.machine_profile_digest, 64) ||
        !read_hex_field(line, identity.validation_evidence_digest, 64)) return 2;
    ceml_fs_describe(directory, &capability);
    if (promote) {
        ceml_store_timing timing[4];
        mpz_inits(n, shortcut, odd, NULL);
        if (!read_line(line, LINE) || line[0] == '0' || mpz_set_str(n, line, 16) != 0 || mpz_sgn(n) <= 0 ||
            mpz_sizeinbase(n, 2) > 8UL*MAX_STATE_BYTES) return 2;
        if (!read_line(line, LINE) || !ceml_is_decimal(line) || mpz_set_str(shortcut, line, 10) != 0) return 2;
        if (!read_line(line, LINE) || !ceml_is_decimal(line) || mpz_set_str(odd, line, 10) != 0) return 2;
        for (i = 0; i < count; ++i)
            if (!ceml_store_promote(directory, &identity, n, shortcut, odd, streaming, &timing[i])) {
                printf("{\"kind\":\"promote\",\"ok\":false,\"completed\":\"%lu\"}\n", i);
                return 3;
            }
        printf("{\"kind\":\"promote\",\"ok\":true,\"strategy\":\"%s\",\"adapter\":\"%s\",\"directory_flush_supported\":%s,"
               "\"qpc_frequency\":\"%llu\",\"promotions\":[", streaming ? "checkpoint.streaming" : "checkpoint.buffered",
               capability.adapter, capability.directory_flush_supported ? "true" : "false", ceml_fs_ticks_per_second());
        for (i = 0; i < count; ++i)
            printf("%s{\"serialization_ticks\":\"%llu\",\"write_ticks\":\"%llu\",\"flush_ticks\":\"%llu\","
                   "\"verify_ticks\":\"%llu\",\"promotion_ticks\":\"%llu\",\"directory_ticks\":\"%llu\","
                   "\"retire_ticks\":\"%llu\",\"total_ticks\":\"%llu\",\"body_bytes\":\"%llu\",\"metadata_bytes\":\"%llu\","
                   "\"directory_flush\":\"%s\",\"retired\":\"%u\"}", i ? "," : "", timing[i].serialization_ticks,
                   timing[i].write_ticks, timing[i].flush_ticks, timing[i].verify_ticks, timing[i].promotion_ticks,
                   timing[i].directory_ticks, timing[i].retire_ticks, timing[i].total_ticks, timing[i].body_bytes,
                   timing[i].metadata_bytes, timing[i].directory_flush == 1 ? "performed" : "unsupported", timing[i].retired);
        printf("]}\n");
        return 0;
    } else {
        static const char *const STATUS[] = { "selected", "empty", "integrity-refusal", "ambiguity-refusal",
                                              "provenance-refusal", "io-refusal" };
        static const char *const POINTER[] = { "absent", "agrees", "ignored" };
        ceml_recovery recovery;
        char *hex;
        void (*release)(void *, size_t);
        ceml_recovery_init(&recovery);
        ceml_store_recover(directory, &identity, &recovery);
        printf("{\"kind\":\"recover\",\"status\":\"%s\",\"valid_generations\":\"%u\",\"invalid_generations\":\"%u\","
               "\"temporary_entries\":\"%u\",\"foreign_entries\":\"%u\",\"pointer\":\"%s\",\"directory_flush_supported\":%s",
               STATUS[recovery.status], recovery.valid_generations, recovery.invalid_generations,
               recovery.temporary_entries, recovery.foreign_entries, POINTER[recovery.pointer],
               capability.directory_flush_supported ? "true" : "false");
        if (recovery.status == CEML_STORE_OK) {
            hex = mpz_get_str(NULL, 16, recovery.n);
            printf(",\"n_hex\":\"%s\",\"metadata_digest\":\"%s\",\"body_digest\":\"%s\",\"previous_metadata_digest\":%s%s%s,"
                   "\"terminal_reached\":%s,", hex, recovery.metadata.metadata_digest, recovery.metadata.body_digest,
                   recovery.metadata.has_previous ? "\"" : "", recovery.metadata.has_previous ?
                   recovery.metadata.previous_metadata_digest : "null", recovery.metadata.has_previous ? "\"" : "",
                   recovery.metadata.terminal_reached ? "true" : "false");
            mp_get_memory_functions(NULL, NULL, &release);
            release(hex, strlen(hex) + 1);
            print_number("sequence", recovery.metadata.sequence, ",");
            print_number("shortcut_steps", recovery.metadata.shortcut_steps, ",");
            print_number("odd_steps", recovery.metadata.odd_steps, ",");
            print_number("standard_steps", recovery.metadata.standard_steps, "");
        }
        printf("}\n");
        return recovery.status == CEML_STORE_OK || recovery.status == CEML_STORE_EMPTY ? 0 : 4;
    }
}
