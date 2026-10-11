#ifndef CEML_FRONTIER_WORKER_H
#define CEML_FRONTIER_WORKER_H

#include <gmp.h>
#include <stddef.h>

#define FRONTIER_MAX_DECIMAL 8192u
#define FRONTIER_MAX_BITS 32768u
#define FRONTIER_MAX_FRAME 32768u
#define FRONTIER_MAX_BATCH 14400ul
#define FRONTIER_MAX_T_PER_EXPLICIT 100000ul
#define FRONTIER_MAX_TOTAL_T 2000000ul

/* Installing the bounded allocator must precede every GMP operation. */
void frontier_memory_init(void);
int frontier_decimal(mpz_t value, const char *text, int positive);
int frontier_budget(unsigned long *value, const char *text, unsigned long ceiling);
int frontier_scan(const mpz_t start, const mpz_t end,
                  unsigned long max_per, unsigned long max_total);
int frontier_identity(const mpz_t start, unsigned long steps);
int frontier_table(void);

#endif
