#ifndef CEML_VALIDATE_H
#define CEML_VALIDATE_H

#define CEML_HOOK_COUNT 12

typedef struct { unsigned long long cases, failures; } ceml_hook_result;

extern const char *const CEML_HOOK_NAME[CEML_HOOK_COUNT];

/* Runs one CEML-V1-SUITE-1 class target. full = 0 is the bounded developer mode
 * used by self-test; full = 1 is the complete class, reachable only through the
 * status-gated validate command. Classes 8 and 9 need a scratch directory name. */
int ceml_hook_run(int index, int full, const char *scratch_directory, ceml_hook_result *result);

#endif
