/* CalibrationRunner child entry (docs/CODEX_HANDOFF.md section 2.12, 10, 15).
 *
 * `ceml --calibration-only ...` runs one bounded CEML-CAL-1 engineering case of
 * the production engine itself so that calibration evidence binds to this
 * exact executable. Hard bounds equal the I1 suite maxima. Operands and
 * synthetic identities arrive on standard input from the fixed C1 driver; the
 * entry has no scientific generator path and accepts only identities marked
 * synthetic. One process is one warm-up plus measured repetitions. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <psapi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ceml_calibrate.h"
#include "ceml_engine.h"
#include "ceml_fs.h"
#include "ceml_store.h"

#define MAX_BITS 131072UL
#define MAX_FIXED_STEPS 4096UL
#define MAX_MACRO 16384UL
#define MAX_TERMINAL_BITS 4097UL
#define MAX_STATE_BYTES 32768UL
#define REPEATS 6
#define MUL_ITERATIONS 256
#define LINE 70000

static size_t live_bytes, peak_live_bytes;
static char line[LINE];

static void *tracked_alloc(size_t size) {
    void *p = malloc(size);
    if (!p) ExitProcess(20);
    live_bytes += size;
    if (live_bytes > peak_live_bytes) peak_live_bytes = live_bytes;
    return p;
}
static void *tracked_realloc(void *p, size_t old_size, size_t size) {
    p = realloc(p, size);
    if (!p) ExitProcess(20);
    live_bytes = live_bytes - old_size + size;
    if (live_bytes > peak_live_bytes) peak_live_bytes = live_bytes;
    return p;
}
static void tracked_free(void *p, size_t size) { free(p); live_bytes -= size; }

static int read_line(size_t capacity) {
    size_t length;
    if (!fgets(line, (int)(capacity < LINE ? capacity : LINE), stdin)) return 0;
    length = strlen(line);
    while (length && (line[length-1] == '\n' || line[length-1] == '\r')) line[--length] = 0;
    return length > 0;
}

static int read_operand(mpz_t value, unsigned long max_bits) {
    size_t length, i;
    if (!read_line(LINE)) return 0;
    length = strlen(line);
    if (length > max_bits/4 + 1 || line[0] == '0') return 0;
    for (i = 0; i < length; ++i)
        if (!((line[i] >= '0' && line[i] <= '9') || (line[i] >= 'a' && line[i] <= 'f'))) return 0;
    return mpz_set_str(value, line, 16) == 0 && mpz_sgn(value) > 0 && mpz_sizeinbase(value, 2) <= max_bits;
}

static int parse_number(const char *text, unsigned long minimum, unsigned long maximum, unsigned long *value) {
    char *end;
    if (!text[0] || text[0] == '0' || strlen(text) > 6) return 0;
    *value = strtoul(text, &end, 10);
    return *end == 0 && *value >= minimum && *value <= maximum;
}

static void print_value(const char *name, const mpz_t value, int base, const char *tail) {
    char *text = mpz_get_str(NULL, base, value);
    void (*release)(void *, size_t);
    printf("\"%s\":\"%s\"%s", name, text, tail);
    mp_get_memory_functions(NULL, NULL, &release);
    release(text, strlen(text) + 1);
}

static unsigned long long process_cpu_100ns(void) {
    FILETIME created, exited, kernel, user_time;
    if (!GetProcessTimes(GetCurrentProcess(), &created, &exited, &kernel, &user_time)) ExitProcess(28);
    return (((unsigned long long)kernel.dwHighDateTime << 32) | kernel.dwLowDateTime) +
           (((unsigned long long)user_time.dwHighDateTime << 32) | user_time.dwLowDateTime);
}

static unsigned long long peak_working_set(void) {
    PROCESS_MEMORY_COUNTERS memory = {0};
    if (!GetProcessMemoryInfo(GetCurrentProcess(), &memory, sizeof(memory))) ExitProcess(28);
    return (unsigned long long)memory.PeakWorkingSetSize;
}

/* argv: route direct|small|hier W D CAP STEPS reuse|copy AUDIT fixed|terminal-t|terminal-u
 *       mul
 *       repr LOWBITS STEPS */
static int arithmetic_case(int argc, char **argv) {
    ceml_config config;
    ceml_engine engine;
    ceml_state state;
    mpz_t input, second, first, first_shortcut, first_odd, low;
    LARGE_INTEGER frequency, begin, end, table_begin, table_end;
    long long ticks[REPEATS];
    unsigned long long cpu[REPEATS], rss[REPEATS], live_peak[REPEATS];
    unsigned long fixed = 0, low_bits = 0, width = 0;
    int kernel, identical = 1, repeat, route, rc = CEML_OK, is_terminal = 0;
    unsigned char *exported = NULL;
    size_t exported_length = 0;
    ceml_config_profile(&config);
    config.copy = 0;
    mpz_inits(input, second, first, first_shortcut, first_odd, low, NULL);
    ceml_state_init(&state);
    if (strcmp(argv[0], "route") == 0 && argc == 9) {
        kernel = 0;
        if (strcmp(argv[1], "direct") == 0) config.macro = CEML_MACRO_DIRECT;
        else if (strcmp(argv[1], "small") == 0) config.macro = CEML_MACRO_SMALL;
        else if (strcmp(argv[1], "hier") == 0) config.macro = CEML_MACRO_HIER;
        else return 2;
        if (config.macro == CEML_MACRO_SMALL) { if (!parse_number(argv[2], 4, 16, &width) || width % 4) return 2; config.width = width; }
        else if (strcmp(argv[2], "1")) return 2;
        if (config.macro == CEML_MACRO_HIER) {
            if (!parse_number(argv[3], 2, 8, &config.divisor) || !parse_number(argv[4], 1024, MAX_MACRO, &config.cap)) return 2;
        } else if (strcmp(argv[3], "1") || strcmp(argv[4], "1")) return 2;
        config.copy = strcmp(argv[6], "copy") == 0;
        if (!config.copy && strcmp(argv[6], "reuse")) return 2;
        config.audit = strcmp(argv[7], "structural") == 0 ? CEML_AUDIT_STRUCTURAL : strcmp(argv[7], "divisibility") == 0 ?
                       CEML_AUDIT_DIVISIBILITY : strcmp(argv[7], "modular") == 0 ? CEML_AUDIT_MODULAR : -1;
        if (config.audit < 0) return 2;
        if (strcmp(argv[8], "fixed") == 0) {
            /* A hierarchical case is a sequence of macro constructions, each within the
             * I1 macro bound; other routes are fixed-step cases. */
            if (!parse_number(argv[5], 1, config.macro == CEML_MACRO_HIER ? MAX_MACRO : MAX_FIXED_STEPS, &fixed)) return 2;
            if (!read_operand(input, MAX_BITS)) return 2;
        } else {
            is_terminal = 1; config.terminal_odd_only = strcmp(argv[8], "terminal-u") == 0;
            if ((!config.terminal_odd_only && strcmp(argv[8], "terminal-t")) || config.macro != CEML_MACRO_HIER || strcmp(argv[5], "1")) return 2;
            if (!read_operand(input, MAX_TERMINAL_BITS)) return 2;
        }
    } else if (strcmp(argv[0], "mul") == 0 && argc == 1) {
        kernel = 1;
        if (!read_operand(input, MAX_BITS) || !read_operand(second, MAX_BITS)) return 2;
    } else if (strcmp(argv[0], "repr") == 0 && argc == 3) {
        kernel = 2; config.macro = CEML_MACRO_DIRECT;
        if (!parse_number(argv[1], 1, MAX_FIXED_STEPS, &low_bits) || !parse_number(argv[2], 1, MAX_FIXED_STEPS, &fixed)) return 2;
        if (!read_operand(input, MAX_BITS)) return 2;
        exported = (unsigned char *)malloc(MAX_BITS/8 + 8);
        if (!exported) return 20;
    } else return 2;
    if (!QueryPerformanceFrequency(&frequency) || !QueryPerformanceCounter(&table_begin)) return 4;
    if (ceml_engine_init(&engine, &config) != CEML_OK) return 22;       /* builds and checks any table */
    if (!QueryPerformanceCounter(&table_end)) return 4;
    for (repeat = 0; repeat < REPEATS && rc == CEML_OK; ++repeat) {
        unsigned long long cpu_before;
        if (kernel != 1) ceml_state_set(&state, input);
        peak_live_bytes = live_bytes;
        cpu_before = process_cpu_100ns();
        if (!QueryPerformanceCounter(&begin)) return 4;
        if (kernel == 0) rc = ceml_engine_advance(&engine, &state, fixed, 0, NULL);
        else if (kernel == 1) {
            int m;       /* one repetition is MUL_ITERATIONS identical exact products */
            for (m = 0; m < MUL_ITERATIONS; ++m) {
                mpz_mul(state.n, input, second);
                ++engine.activated[CEML_ROUTE_GMP_PUBLIC]; ++engine.activated[CEML_ROUTE_STATE_DENSE];
            }
            ++engine.activated[CEML_ROUTE_PARALLEL_SINGLE];
        } else {
            mpz_export(exported, &exported_length, 1, 1, 1, 0, state.n);   /* canonical big-endian magnitude */
            mpz_fdiv_r_2exp(low, state.n, low_bits);                       /* exactly n mod 2^k */
            rc = ceml_engine_advance(&engine, &state, fixed, 0, NULL);
        }
        if (!QueryPerformanceCounter(&end)) return 4;
        ticks[repeat] = end.QuadPart - begin.QuadPart;
        cpu[repeat] = (process_cpu_100ns() - cpu_before)*100;
        rss[repeat] = peak_working_set(); live_peak[repeat] = peak_live_bytes;
        if (repeat == 0) { mpz_set(first, state.n); mpz_set(first_shortcut, state.shortcut_steps); mpz_set(first_odd, state.odd_steps); }
        else if (mpz_cmp(first, state.n) || mpz_cmp(first_shortcut, state.shortcut_steps) || mpz_cmp(first_odd, state.odd_steps))
            identical = 0;
    }
    if (rc != CEML_OK) { printf("{\"kind\":\"engine-refusal\",\"reason\":\"%s\"}\n", ceml_error_text(rc)); return 3; }
    printf("{\"kind\":\"candidate\",");
    print_value("n_hex", state.n, 16, ",");
    print_value("shortcut_steps", state.shortcut_steps, 10, ",");
    print_value("odd_steps", state.odd_steps, 10, ",");
    print_value("standard_steps", state.standard_steps, 10, ",");
    if (kernel == 2) {
        static const char digits[] = "0123456789abcdef";
        size_t i;
        print_value("low_bits_hex", low, 16, ",");
        printf("\"export_hex\":\"");
        for (i = 0; i < exported_length; ++i) { putchar(digits[exported[i] >> 4]); putchar(digits[exported[i] & 15]); }
        printf("\",");
    }
    printf("\"terminal_reached\":%s,\"repeats_identical\":%s,\"fallback_count\":\"%llu\",\"activated\":{",
           kernel != 1 && mpz_cmp_ui(state.n, 1) == 0 ? "true" : "false", identical ? "true" : "false", engine.fallback_count);
    for (route = 0; route < CEML_ROUTE_COUNT; ++route)
        printf("%s\"%s\":\"%llu\"", route ? "," : "", CEML_ROUTE_ID[route], engine.activated[route]);
    printf("},\"qpc_frequency\":\"%lld\",\"table_ticks\":\"%lld\",\"table_entries_checked\":\"%lu\",\"repeats\":[",
           (long long)frequency.QuadPart, (long long)(table_end.QuadPart - table_begin.QuadPart),
           config.macro == CEML_MACRO_SMALL ? 1UL << width : 0UL);
    for (repeat = 0; repeat < REPEATS; ++repeat)
        printf("%s{\"ticks\":\"%lld\",\"cpu_ns\":\"%llu\",\"peak_working_set_bytes\":\"%llu\",\"peak_live_bytes\":\"%llu\"}",
               repeat ? "," : "", ticks[repeat], cpu[repeat], rss[repeat], live_peak[repeat]);
    printf("],\"checked_build\":%s,\"is_terminal\":%s,\"production_engine\":true}\n",
#ifdef CEML_CHECKED
           "true",
#else
           "false",
#endif
           is_terminal ? "true" : "false");
    return identical ? 0 : 3;
}

static int read_hex_field(char *out, size_t minimum) {
    if (!read_line(LINE) || !ceml_is_hex(line, minimum, 64)) return 0;
    strcpy_s(out, CEML_HEX, line);
    return 1;
}

int ceml_read_synthetic_identity(char *directory, size_t directory_size, ceml_identity *identity) {
    memset(identity, 0, sizeof(*identity));
    if (!read_line(directory_size)) return 0;
    strcpy_s(directory, directory_size, line);
    if (strstr(directory, "..") || directory[0] == '\\' || strchr(directory, ':')) return 0;      /* relative, contained */
    if (!read_line(sizeof(identity->run_id))) return 0;
    strcpy_s(identity->run_id, sizeof(identity->run_id), line);
    /* Only identities marked non-scientific are accepted outside the gated run command. */
    if (strncmp(identity->run_id, "c1-synthetic-", 13) != 0 && strncmp(identity->run_id, "v1-validation-", 14) != 0) return 0;
    return read_hex_field(identity->manifest_digest, 64) && read_hex_field(identity->original_start_digest, 64) &&
           read_hex_field(identity->protocol_commit, 40) && read_hex_field(identity->engine_commit, 40) &&
           read_hex_field(identity->build_digest, 64) && read_hex_field(identity->machine_profile_digest, 64) &&
           read_hex_field(identity->validation_evidence_digest, 64);
}

int ceml_read_synthetic_state(mpz_t n, mpz_t shortcut, mpz_t odd) {
    if (!read_line(LINE) || line[0] == '0' || mpz_set_str(n, line, 16) != 0 || mpz_sgn(n) <= 0 ||
        mpz_sizeinbase(n, 2) > 8UL*MAX_STATE_BYTES) return 0;
    if (!read_line(LINE) || !ceml_is_decimal(line) || mpz_set_str(shortcut, line, 10) != 0) return 0;
    return read_line(LINE) && ceml_is_decimal(line) && mpz_set_str(odd, line, 10) == 0 && mpz_cmp(odd, shortcut) <= 0;
}

void ceml_print_recovery(const ceml_recovery *recovery, int directory_flush_supported) {
    static const char *const STATUS[] = { "selected", "empty", "integrity-refusal", "ambiguity-refusal",
                                          "provenance-refusal", "io-refusal" };
    static const char *const POINTER[] = { "absent", "agrees", "ignored" };
    printf("{\"kind\":\"recover\",\"status\":\"%s\",\"valid_generations\":\"%u\",\"invalid_generations\":\"%u\","
           "\"temporary_entries\":\"%u\",\"foreign_entries\":\"%u\",\"pointer\":\"%s\",\"directory_flush_supported\":%s",
           STATUS[recovery->status], recovery->valid_generations, recovery->invalid_generations, recovery->temporary_entries,
           recovery->foreign_entries, POINTER[recovery->pointer], directory_flush_supported ? "true" : "false");
    if (recovery->status == CEML_STORE_OK) {
        printf(",\"metadata_digest\":\"%s\",\"body_digest\":\"%s\",\"previous_metadata_digest\":%s%s%s,\"terminal_reached\":%s,",
               recovery->metadata.metadata_digest, recovery->metadata.body_digest, recovery->metadata.has_previous ? "\"" : "",
               recovery->metadata.has_previous ? recovery->metadata.previous_metadata_digest : "null",
               recovery->metadata.has_previous ? "\"" : "", recovery->metadata.terminal_reached ? "true" : "false");
        print_value("n_hex", recovery->n, 16, ",");
        print_value("sequence", recovery->metadata.sequence, 10, ",");
        print_value("shortcut_steps", recovery->metadata.shortcut_steps, 10, ",");
        print_value("odd_steps", recovery->metadata.odd_steps, 10, ",");
        print_value("standard_steps", recovery->metadata.standard_steps, 10, "");
    }
    printf("}\n");
}

/* argv: promote buffered|streaming FAULT COUNT   |   recover none none 1 */
static int checkpoint_case(int argc, char **argv) {
    static char directory[512];
    ceml_identity identity;
    ceml_fs_capability capability;
    mpz_t n, shortcut, odd;
    unsigned long count, i;
    int streaming, promote;
    if (argc != 4) return 2;
    promote = strcmp(argv[0], "promote") == 0;
    streaming = strcmp(argv[1], "streaming") == 0;
    if (promote && !streaming && strcmp(argv[1], "buffered") != 0) return 2;
    if (strcmp(argv[2], "none") != 0) ceml_fs_set_fault(argv[2]);
    count = strtoul(argv[3], NULL, 10);
    if (count < 1 || count > 4) return 2;
    if (!ceml_read_synthetic_identity(directory, sizeof(directory), &identity) || strncmp(identity.run_id, "c1-synthetic-", 13)) return 2;
    ceml_fs_describe(directory, &capability);
    if (promote) {
        ceml_store_timing timing[4];
        mpz_inits(n, shortcut, odd, NULL);
        if (!ceml_read_synthetic_state(n, shortcut, odd)) return 2;
        for (i = 0; i < count; ++i)
            if (!ceml_store_promote(directory, &identity, n, shortcut, odd, streaming, &timing[i])) {
                printf("{\"kind\":\"promote\",\"ok\":false,\"completed\":\"%lu\"}\n", i);
                return 3;
            }
        printf("{\"kind\":\"promote\",\"ok\":true,\"strategy\":\"%s\",\"adapter\":\"%s\",\"directory_flush_supported\":%s,"
               "\"qpc_frequency\":\"%llu\",\"promotions\":[", CEML_ROUTE_ID[streaming ? CEML_ROUTE_CHECKPOINT_STREAMING : CEML_ROUTE_CHECKPOINT_BUFFERED],
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
        ceml_recovery recovery;
        if (strcmp(argv[0], "recover") != 0) return 2;
        ceml_recovery_init(&recovery);
        ceml_store_recover(directory, &identity, &recovery);
        ceml_print_recovery(&recovery, capability.directory_flush_supported);
        return recovery.status == CEML_STORE_OK || recovery.status == CEML_STORE_EMPTY ? 0 : 4;
    }
}

int ceml_calibration_entry(int argc, char **argv) {
    if (argc < 1) return 2;
    mp_set_memory_functions(tracked_alloc, tracked_realloc, tracked_free);
    if (strcmp(argv[0], "promote") == 0 || strcmp(argv[0], "recover") == 0) return checkpoint_case(argc, argv);
    return arithmetic_case(argc, argv);
}
