/* New, bounded CEML-FRONTIER-1 worker. No legacy production entry point. */
#include "frontier_worker.h"
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <io.h>
#include <stdlib.h>
#include <limits.h>

static int refusal(void) {
    fputs("REFUSED invalid or incomplete worker arguments\n", stderr);
    return 2;
}

static int scan_authority(const mpz_t end) {
    const char *mode, *path;
    char status[128u * 1024u + 2u];
    const char phase_key[] = "**Authoritative current phase:**";
    const char science_key[] = "**Scientific execution authorization:**";
    const char phase_description[] = "RUN1 \xe2\x80\x94 ";
    char *line;
    FILE *file;
    size_t length;
    unsigned int phase_fields = 0, science_fields = 0;
    int phase_valid = 0, science_valid = 0, read_failed;
    /* All L1 scans are expressly tiny test fixtures. High-bit identities are
     * separate fixed-step operations. A later driver must also enforce the
     * full frozen RUN1 evidence/snapshot/acknowledgment gate. */
    if (mpz_cmp_ui(end, 10000ul) <= 0) return 1;
    mode = getenv("CEML_FRONTIER_DRIVER_MODE");
    path = getenv("CEML_FRONTIER_STATUS_PATH");
    if (mode == NULL || strcmp(mode, "RUN1-AUTHORIZED") != 0 || path == NULL) return 0;
    file = fopen(path, "rb");
    if (file == NULL) return 0;
    length = fread(status, 1u, sizeof(status) - 1u, file);
    read_failed = ferror(file);
    if (fclose(file) != 0) read_failed = 1;
    if (read_failed || length > 128u * 1024u || memchr(status, '\0', length) != NULL) return 0;
    status[length] = '\0';
    line = status;
    while (*line != '\0') {
        char *next = strchr(line, '\n');
        size_t line_length;
        if (next != NULL) *next = '\0';
        line_length = strlen(line);
        if (line_length > 0u && line[line_length - 1u] == '\r') line[line_length - 1u] = '\0';
        if (strncmp(line, phase_key, sizeof(phase_key) - 1u) == 0) {
            const char *value = line + sizeof(phase_key) - 1u;
            if (phase_fields == UINT_MAX) return 0;
            ++phase_fields;
            if (*value != ' ') return 0;
            ++value;
            phase_valid = strcmp(value, "RUN1") == 0
                || (strncmp(value, phase_description, sizeof(phase_description) - 1u) == 0
                    && value[sizeof(phase_description) - 1u] != '\0');
        }
        if (strncmp(line, science_key, sizeof(science_key) - 1u) == 0) {
            const char *value = line + sizeof(science_key) - 1u;
            if (science_fields == UINT_MAX) return 0;
            ++science_fields;
            if (*value != ' ') return 0;
            ++value;
            science_valid = strcmp(value, "AUTHORISED") == 0;
        }
        if (next == NULL) break;
        line = next + 1;
    }
    return phase_fields == 1u && science_fields == 1u && phase_valid && science_valid;
}

int main(int argc, char **argv) {
    mpz_t start, end, width;
    const char *start_text = NULL, *end_text = NULL, *per_text = NULL, *total_text = NULL;
    unsigned long max_per = 0, max_total = 0;
    int i, result = 2;
    /* Windows CRT otherwise translates protocol LF into CRLF. */
    if (_setmode(_fileno(stdout), _O_BINARY) == -1) return refusal();
    if (_setmode(_fileno(stderr), _O_BINARY) == -1) return refusal();
    frontier_memory_init();
    mpz_inits(start, end, width, NULL);
    if (argc == 2 && strcmp(argv[1], "--table") == 0) {
        result = frontier_table();
        goto done;
    }
    if (argc == 4 && strcmp(argv[1], "--identity") == 0) {
        if (!frontier_decimal(start, argv[2], 1)
                || !frontier_budget(&max_per, argv[3], 128ul)) goto bad;
        result = frontier_identity(start, max_per);
        goto done;
    }
    if (argc != 9) goto bad;
    for (i = 1; i < argc; i += 2) {
        const char **destination = NULL;
        if (strcmp(argv[i], "--start") == 0) destination = &start_text;
        else if (strcmp(argv[i], "--end") == 0) destination = &end_text;
        else if (strcmp(argv[i], "--max-t-per-explicit") == 0) destination = &per_text;
        else if (strcmp(argv[i], "--max-total-t") == 0) destination = &total_text;
        else goto bad;
        if (*destination != NULL) goto bad;
        *destination = argv[i + 1];
    }
    if (start_text == NULL || end_text == NULL || per_text == NULL || total_text == NULL
            || !frontier_decimal(start, start_text, 1)
            || !frontier_decimal(end, end_text, 1)
            || !frontier_budget(&max_per, per_text, FRONTIER_MAX_T_PER_EXPLICIT)
            || !frontier_budget(&max_total, total_text, FRONTIER_MAX_TOTAL_T)
            || mpz_cmp_ui(start, 2ul) < 0 || mpz_cmp(end, start) <= 0) goto bad;
    mpz_sub(width, end, start);
    if (mpz_cmp_ui(width, FRONTIER_MAX_BATCH) > 0) goto bad;
    if (!scan_authority(end)) {
        fputs("REFUSED RUN1 authority absent; high values permit identity fixtures only\n", stderr);
        goto done;
    }
    result = frontier_scan(start, end, max_per, max_total);
    goto done;
bad:
    result = refusal();
done:
    mpz_clears(start, end, width, NULL);
    return result;
}
