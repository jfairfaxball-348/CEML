#ifndef CEML_CALIBRATE_H
#define CEML_CALIBRATE_H

#include <stddef.h>
#include "ceml_store.h"

/* argv after `--calibration-only`. Bounded CEML-CAL-1 engineering cases only. */
int ceml_calibration_entry(int argc, char **argv);

/* Shared readers for non-scientific (synthetic or validation) identities and states on standard input. */
int ceml_read_synthetic_identity(char *directory, size_t directory_size, ceml_identity *identity);
int ceml_read_synthetic_state(mpz_t n, mpz_t shortcut, mpz_t odd);
void ceml_print_recovery(const ceml_recovery *recovery, int directory_flush_supported);

#endif
