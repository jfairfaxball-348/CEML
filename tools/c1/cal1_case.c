/* Stage: hardware characterization. Bounded CEML-CAL-1 candidate kernels only.
 *
 * One process runs one warm-up and five measured repetitions of one fixed case
 * and prints one JSON line. Operands arrive as lowercase hex lines on standard
 * input from the fixed driver; this program has no generator, no scientific
 * input path and hard work bounds equal to the I1 suite maxima. Correctness is
 * decided by the driver against an independent definition-level reference in
 * a different language; nothing here is a reference oracle, V1 evidence or a
 * production engine. Only documented public GMP mpz functions are used. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <psapi.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>

#define MAX_BITS 131072UL
#define MAX_FIXED_STEPS 4096UL
#define MAX_MACRO 16384UL
#define MAX_TERMINAL_BITS 4097UL
#define TERMINAL_STEP_CAP 200000UL
#define LEAF 20UL
#define REPEATS 6
#define MUL_ITERATIONS 256
#define LINE (MAX_BITS/4 + 8)
#define AUDIT_PRIME 4294967291UL

enum { R_DIRECT, R_SMALL, R_HIER };
enum { AUDIT_STRUCTURAL, AUDIT_DIVISIBILITY, AUDIT_MODULAR };
enum { C_DIRECT, C_SMALL, C_HIER, C_DENSE, C_GMP, C_COPY, C_REUSE, C_SINGLE, C_TERM_T, C_TERM_U,
       C_DIVISIBILITY, C_MODULAR, C_COUNT };
static const char *const ROUTE_ID[C_COUNT] = {
    "engine.direct_t", "engine.small_affine", "engine.hier_affine.explicit", "state.dense",
    "arith.gmp.public", "alloc.copy", "alloc.reuse", "parallel.single", "terminal.direct_t",
    "terminal.odd_only", "audit.divisibility", "audit.modular" };

typedef struct { uint32_t a, b; uint8_t odd; } Small;
typedef struct { mpz_t a, b; unsigned long k, i; } Block;

static size_t live_bytes, peak_live_bytes;
static unsigned long long activated[C_COUNT];
static unsigned long long fallback_count;
static int audit_mode = AUDIT_DIVISIBILITY, copy_mode, terminal_odd_only;
static Small *table;
static unsigned long table_width;

static void fail(int code) { fflush(stdout); ExitProcess((UINT)code); }

static void *tracked_alloc(size_t size) {
    void *p = malloc(size);
    if (!p) fail(20);
    live_bytes += size;
    if (live_bytes > peak_live_bytes) peak_live_bytes = live_bytes;
    return p;
}
static void *tracked_realloc(void *p, size_t old_size, size_t size) {
    p = realloc(p, size);
    if (!p) fail(20);
    live_bytes = live_bytes - old_size + size;
    if (live_bytes > peak_live_bytes) peak_live_bytes = live_bytes;
    return p;
}
static void tracked_free(void *p, size_t size) { free(p); live_bytes -= size; }

/* Base block built directly from elementary T on a bounded residue.
 * For k <= 20: A = 3^i <= 3^20 and B <= 3^20 - 2^20 both fit 32 bits, and the
 * iterated residue stays below 2^20 * (3/2)^20 + 1 < 2^33. */
static void leaf(uint64_t residue, unsigned long k, uint32_t *a, uint32_t *b, unsigned long *odd) {
    uint64_t A = 1, B = 0;
    unsigned long j, i = 0;
    if (k > LEAF) fail(21);
    for (j = 0; j < k; ++j) {
        if (residue & 1) { B = 3*B + ((uint64_t)1 << j); A *= 3; ++i; residue = (3*residue + 1) >> 1; }
        else residue >>= 1;
    }
    if (A > 0xffffffffULL || B > 0xffffffffULL) fail(21);
    *a = (uint32_t)A; *b = (uint32_t)B; *odd = i;
}

static void build_table(unsigned long width) {
    unsigned long count = 1UL << width, r, odd;
    table = (Small *)malloc(sizeof(Small) * count);
    if (!table) fail(20);
    for (r = 0; r < count; ++r) {
        uint64_t x = (uint64_t)count + r, direct = x;
        unsigned long j;
        leaf(r, width, &table[r].a, &table[r].b, &odd);
        table[r].odd = (uint8_t)odd;
        /* Every entry is checked against separately written elementary T. */
        for (j = 0; j < width; ++j) direct = (direct & 1) ? (3*direct + 1) >> 1 : direct >> 1;
        x = x*table[r].a + table[r].b;
        if ((x & (count - 1)) != 0 || (x >> width) != direct) fail(22);
    }
    table_width = width;
}

/* Explicit-coefficient binary splitting: k1 = floor(k/2), the right block is
 * selected by the exact post-left residue, and composition is P2 after P1. */
static void build(Block *p, const mpz_t r, unsigned long k) {
    if (k <= LEAF) {
        uint32_t a, b;
        unsigned long odd;
        leaf((uint64_t)mpz_get_ui(r) & (((uint64_t)1 << k) - 1), k, &a, &b, &odd);
        mpz_set_ui(p->a, a); mpz_set_ui(p->b, b); p->k = k; p->i = odd;
    } else {
        unsigned long k1 = k/2, k2 = k - k1;
        Block right;
        mpz_t low, mid;
        mpz_inits(low, mid, right.a, right.b, NULL);
        mpz_fdiv_r_2exp(low, r, k1);
        build(p, low, k1);
        mpz_mul(mid, p->a, r); mpz_add(mid, mid, p->b);
        if (audit_mode != AUDIT_STRUCTURAL) {
            if (!mpz_divisible_2exp_p(mid, k1)) fail(23);
            ++activated[C_DIVISIBILITY];
        }
        mpz_tdiv_q_2exp(mid, mid, k1);
        mpz_fdiv_r_2exp(low, mid, k2);
        build(&right, low, k2);
        if (k1 + k2 != k || p->k != k1 || right.k != k2) fail(24);
        mpz_mul(mid, right.a, p->b);            /* A2*B1 */
        mpz_mul_2exp(low, right.b, k1);         /* B2*2^k1 */
        mpz_add(p->b, mid, low);
        mpz_mul(p->a, right.a, p->a);           /* A2*A1 */
        p->k = k; p->i += right.i;
        mpz_clears(low, mid, right.a, right.b, NULL);
    }
}

/* n <- (A*n + B) / 2^k with the selected audit and allocation modes. */
static void apply(mpz_t n, mpz_t scratch, const mpz_t a, const mpz_t b, unsigned long k) {
    unsigned long before = 0, am = 0, bm = 0;
    if (audit_mode == AUDIT_MODULAR) {
        before = mpz_fdiv_ui(n, AUDIT_PRIME); am = mpz_fdiv_ui(a, AUDIT_PRIME); bm = mpz_fdiv_ui(b, AUDIT_PRIME);
    }
    if (copy_mode) {
        mpz_t product, next;
        mpz_init(product); mpz_mul(product, a, n); mpz_add(product, product, b);
        if (audit_mode != AUDIT_STRUCTURAL) {
            if (!mpz_divisible_2exp_p(product, k)) fail(23);
            ++activated[C_DIVISIBILITY];
        }
        mpz_init(next); mpz_tdiv_q_2exp(next, product, k);
        mpz_swap(n, next); mpz_clear(next); mpz_clear(product);
        ++activated[C_COPY];
    } else {
        mpz_mul(scratch, a, n); mpz_add(scratch, scratch, b);
        if (audit_mode != AUDIT_STRUCTURAL) {
            if (!mpz_divisible_2exp_p(scratch, k)) fail(23);
            ++activated[C_DIVISIBILITY];
        }
        mpz_tdiv_q_2exp(n, scratch, k);
        ++activated[C_REUSE];
    }
    if (audit_mode == AUDIT_MODULAR) {
        uint64_t left = ((uint64_t)am*before + bm) % AUDIT_PRIME, power = 1, base = 2;
        unsigned long e = k;
        while (e) { if (e & 1) power = power*base % AUDIT_PRIME; base = base*base % AUDIT_PRIME; e >>= 1; }
        if (left != power*mpz_fdiv_ui(n, AUDIT_PRIME) % AUDIT_PRIME) fail(25);
        ++activated[C_MODULAR];
    }
    ++activated[C_GMP]; ++activated[C_DENSE];
}

static unsigned long elementary(mpz_t n) {
    unsigned long odd = mpz_odd_p(n) ? 1UL : 0UL;
    if (copy_mode) {
        mpz_t next;
        mpz_init(next);
        if (odd) { mpz_mul_ui(next, n, 3); mpz_add_ui(next, next, 1); mpz_tdiv_q_2exp(next, next, 1); }
        else mpz_tdiv_q_2exp(next, n, 1);
        mpz_swap(n, next); mpz_clear(next);
        ++activated[C_COPY];
    } else {
        if (odd) { mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1); }
        mpz_tdiv_q_2exp(n, n, 1);
        ++activated[C_REUSE];
    }
    ++activated[C_GMP]; ++activated[C_DENSE];
    return odd;
}

/* Centralized exact accounting: kernels report (k, i); only this updates. */
static void account(mpz_t shortcut, mpz_t odd, mpz_t standard, unsigned long k, unsigned long i) {
    if (i > k) fail(26);
    mpz_add_ui(shortcut, shortcut, k); mpz_add_ui(odd, odd, i);
    mpz_add_ui(standard, standard, k); mpz_add_ui(standard, standard, i);
}

/* fixed == 0 means run to the first occurrence of 1 (terminal-handoff family). */
static void run(mpz_t n, mpz_t shortcut, mpz_t odd, mpz_t standard, int route, unsigned long width,
                unsigned long divisor, unsigned long cap, unsigned long fixed) {
    mpz_t scratch, low, small_a, small_b;
    Block block;
    unsigned long done = 0;
    mpz_inits(scratch, low, small_a, small_b, block.a, block.b, NULL);
    while (mpz_cmp_ui(n, 1) != 0 && (fixed == 0 || done < fixed)) {
        size_t bits = mpz_sizeinbase(n, 2);
        unsigned long remaining = fixed ? fixed - done : TERMINAL_STEP_CAP - done, k, i;
        if (remaining == 0) fail(27);
        if (route == R_DIRECT) {
            i = elementary(n); k = 1; ++activated[C_DIRECT];
        } else if (route == R_SMALL) {
            if (remaining < width || bits - 1 < width) { ++fallback_count; i = elementary(n); k = 1; }
            else {
                const Small *entry = &table[mpz_fdiv_ui(n, 1UL << width)];
                if (!copy_mode && audit_mode != AUDIT_MODULAR) {
                    /* Single-word coefficients: public mpz_*_ui forms, in place. */
                    mpz_mul_ui(n, n, entry->a); mpz_add_ui(n, n, entry->b);
                    if (audit_mode != AUDIT_STRUCTURAL) {
                        if (!mpz_divisible_2exp_p(n, width)) fail(23);
                        ++activated[C_DIVISIBILITY];
                    }
                    mpz_tdiv_q_2exp(n, n, width);
                    ++activated[C_REUSE]; ++activated[C_GMP]; ++activated[C_DENSE];
                } else {
                    mpz_set_ui(small_a, entry->a); mpz_set_ui(small_b, entry->b);
                    apply(n, scratch, small_a, small_b, width);
                }
                k = width; i = entry->odd; ++activated[C_SMALL];
            }
        } else {
            k = (unsigned long)(bits/divisor);
            if (k > cap) k = cap;
            if (k < 1) k = 1;
            if (k > bits - 1) k = (unsigned long)(bits - 1);   /* first-1 safety: k <= bit_length(n)-1 */
            if (k > remaining) k = remaining;
            if (k > MAX_MACRO) fail(27);
            if (fixed == 0 && k < 2) {                         /* exact terminal handoff */
                if (terminal_odd_only) {
                    if (mpz_odd_p(n)) { mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1); i = 1; } else i = 0;
                    k = (unsigned long)mpz_scan1(n, 0);
                    mpz_tdiv_q_2exp(n, n, k);
                    ++activated[C_TERM_U]; ++activated[C_GMP]; ++activated[C_DENSE];
                } else { i = elementary(n); k = 1; ++activated[C_TERM_T]; }
            } else {
                mpz_fdiv_r_2exp(low, n, k);
                build(&block, low, k);
                if (block.k != k) fail(24);
                apply(n, scratch, block.a, block.b, k);
                i = block.i; ++activated[C_HIER];
            }
        }
        account(shortcut, odd, standard, k, i);
        done += k;
        if (mpz_sgn(n) <= 0) fail(26);
    }
    ++activated[C_SINGLE];
    mpz_clears(scratch, low, small_a, small_b, block.a, block.b, NULL);
}

static int read_operand(mpz_t value, char *line, unsigned long max_bits) {
    size_t length, i;
    if (!fgets(line, (int)LINE, stdin)) return 0;
    length = strlen(line);
    while (length && (line[length-1] == '\n' || line[length-1] == '\r')) line[--length] = 0;
    if (!length || length > max_bits/4 + 1 || line[0] == '0') return 0;
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

static void print_hex(const char *name, const mpz_t value) {
    char *text = mpz_get_str(NULL, 16, value);
    printf("\"%s\":\"%s\",", name, text);
    tracked_free(text, strlen(text) + 1);
}

static void print_decimal(const char *name, const mpz_t value) {
    char *text = mpz_get_str(NULL, 10, value);
    printf("\"%s\":\"%s\",", name, text);
    tracked_free(text, strlen(text) + 1);
}

static unsigned long long process_cpu_100ns(void) {
    FILETIME created, exited, kernel, user_time;
    if (!GetProcessTimes(GetCurrentProcess(), &created, &exited, &kernel, &user_time)) fail(28);
    return (((unsigned long long)kernel.dwHighDateTime << 32) | kernel.dwLowDateTime) +
           (((unsigned long long)user_time.dwHighDateTime << 32) | user_time.dwLowDateTime);
}

static unsigned long long peak_working_set(void) {
    PROCESS_MEMORY_COUNTERS memory = {0};
    if (!GetProcessMemoryInfo(GetCurrentProcess(), &memory, sizeof(memory))) fail(28);
    return (unsigned long long)memory.PeakWorkingSetSize;
}

int main(int argc, char **argv) {
    mpz_t input, second, n, first, shortcut, odd, standard, first_shortcut, first_odd, extra, first_extra;
    LARGE_INTEGER frequency, begin, end, table_begin, table_end;
    long long ticks[REPEATS];
    unsigned long long cpu[REPEATS], rss[REPEATS], live_peak[REPEATS];
    unsigned long width = 0, divisor = 0, cap = 0, fixed = 0, low_bits = 0;
    int route = -1, kernel, identical = 1, repeat, c, is_terminal = 0;
    char *line, *exported = NULL;
    size_t exported_length = 0;
    /* argv: --calibration-only route direct|small|hier W D CAP STEPS reuse|copy AUDIT fixed|terminal-t|terminal-u
     *       --calibration-only mul
     *       --calibration-only repr LOWBITS STEPS */
    if (argc < 3 || strcmp(argv[1], "--calibration-only") != 0) return 2;
    mp_set_memory_functions(tracked_alloc, tracked_realloc, tracked_free);
    mpz_inits(input, second, n, first, shortcut, odd, standard, first_shortcut, first_odd, extra, first_extra, NULL);
    line = (char *)malloc(LINE);
    if (!line) return 20;
    if (strcmp(argv[2], "route") == 0 && argc == 11) {
        kernel = 0;
        route = strcmp(argv[3], "direct") == 0 ? R_DIRECT : strcmp(argv[3], "small") == 0 ? R_SMALL :
                strcmp(argv[3], "hier") == 0 ? R_HIER : -1;
        if (route < 0) return 2;
        if (route == R_SMALL) { if (!parse_number(argv[4], 4, 16, &width) || width % 4) return 2; }
        else if (strcmp(argv[4], "1")) return 2;
        if (route == R_HIER) {
            if (!parse_number(argv[5], 2, 8, &divisor) || divisor == 5 || divisor == 7) return 2;
            if (!parse_number(argv[6], 1024, MAX_MACRO, &cap) || (cap != 1024 && cap != 4096 && cap != 16384)) return 2;
        } else if (strcmp(argv[5], "1") || strcmp(argv[6], "1")) return 2;
        copy_mode = strcmp(argv[8], "copy") == 0;
        if (!copy_mode && strcmp(argv[8], "reuse")) return 2;
        audit_mode = strcmp(argv[9], "structural") == 0 ? AUDIT_STRUCTURAL : strcmp(argv[9], "divisibility") == 0 ?
                     AUDIT_DIVISIBILITY : strcmp(argv[9], "modular") == 0 ? AUDIT_MODULAR : -1;
        if (audit_mode < 0) return 2;
        if (strcmp(argv[10], "fixed") == 0) {
            /* A hierarchical case is a sequence of macro constructions, each at most
             * the I1 macro bound; other routes are fixed-step cases. */
            if (!parse_number(argv[7], 1, route == R_HIER ? MAX_MACRO : MAX_FIXED_STEPS, &fixed)) return 2;
            if (!read_operand(input, line, MAX_BITS)) return 2;
        } else {
            is_terminal = 1; terminal_odd_only = strcmp(argv[10], "terminal-u") == 0;
            if ((!terminal_odd_only && strcmp(argv[10], "terminal-t")) || route != R_HIER || strcmp(argv[7], "1")) return 2;
            if (!read_operand(input, line, MAX_TERMINAL_BITS)) return 2;
        }
    } else if (strcmp(argv[2], "mul") == 0 && argc == 3) {
        kernel = 1;
        if (!read_operand(input, line, MAX_BITS) || !read_operand(second, line, MAX_BITS)) return 2;
    } else if (strcmp(argv[2], "repr") == 0 && argc == 5) {
        kernel = 2; route = R_DIRECT;
        if (!parse_number(argv[3], 1, MAX_FIXED_STEPS, &low_bits) || !parse_number(argv[4], 1, MAX_FIXED_STEPS, &fixed)) return 2;
        if (!read_operand(input, line, MAX_BITS)) return 2;
        exported = (char *)malloc(MAX_BITS/8 + 8);
        if (!exported) return 20;
    } else return 2;
    if (!QueryPerformanceFrequency(&frequency) || !QueryPerformanceCounter(&table_begin)) return 4;
    if (route == R_SMALL) build_table(width);
    if (!QueryPerformanceCounter(&table_end)) return 4;
    for (repeat = 0; repeat < REPEATS; ++repeat) {
        unsigned long long cpu_before;
        size_t live_before = live_bytes;
        mpz_set(n, input); mpz_set_ui(shortcut, 0); mpz_set_ui(odd, 0); mpz_set_ui(standard, 0);
        peak_live_bytes = live_bytes; (void)live_before;
        cpu_before = process_cpu_100ns();
        if (!QueryPerformanceCounter(&begin)) return 4;
        if (kernel == 0) run(n, shortcut, odd, standard, route, width, divisor, cap, fixed);
        else if (kernel == 1) {
            int m;   /* one repetition is MUL_ITERATIONS identical exact products */
            for (m = 0; m < MUL_ITERATIONS; ++m) { mpz_mul(n, input, second); ++activated[C_GMP]; ++activated[C_DENSE]; }
            ++activated[C_SINGLE];
        }
        else {
            mpz_export(exported, &exported_length, 1, 1, 1, 0, n);   /* canonical big-endian magnitude */
            mpz_fdiv_r_2exp(extra, n, low_bits);                     /* exactly n mod 2^k */
            run(n, shortcut, odd, standard, R_DIRECT, 0, 0, 0, fixed);
        }
        if (!QueryPerformanceCounter(&end)) return 4;
        ticks[repeat] = end.QuadPart - begin.QuadPart;
        cpu[repeat] = (process_cpu_100ns() - cpu_before)*100;
        rss[repeat] = peak_working_set(); live_peak[repeat] = peak_live_bytes;
        /* The accounting identity is asserted for every repetition. */
        mpz_add(first_extra, shortcut, odd);
        if (mpz_cmp(first_extra, standard) != 0) return 26;
        if (repeat == 0) { mpz_set(first, n); mpz_set(first_shortcut, shortcut); mpz_set(first_odd, odd); }
        else if (mpz_cmp(first, n) || mpz_cmp(first_shortcut, shortcut) || mpz_cmp(first_odd, odd)) identical = 0;
    }
    printf("{\"kind\":\"candidate\",");
    print_hex("n_hex", n);
    print_decimal("shortcut_steps", shortcut); print_decimal("odd_steps", odd); print_decimal("standard_steps", standard);
    if (kernel == 2) {
        size_t i;
        static const char digits[] = "0123456789abcdef";
        print_hex("low_bits_hex", extra);
        printf("\"export_hex\":\"");
        for (i = 0; i < exported_length; ++i) { putchar(digits[(unsigned char)exported[i] >> 4]); putchar(digits[exported[i] & 15]); }
        printf("\",");
    }
    printf("\"terminal_reached\":%s,\"repeats_identical\":%s,\"fallback_count\":\"%llu\",\"activated\":{",
           mpz_cmp_ui(n, 1) == 0 && kernel != 1 ? "true" : "false", identical ? "true" : "false", fallback_count);
    for (c = 0; c < C_COUNT; ++c) printf("%s\"%s\":\"%llu\"", c ? "," : "", ROUTE_ID[c], activated[c]);
    printf("},\"qpc_frequency\":\"%lld\",\"table_ticks\":\"%lld\",\"table_entries_checked\":\"%lu\",\"repeats\":[",
           (long long)frequency.QuadPart, (long long)(table_end.QuadPart - table_begin.QuadPart),
           route == R_SMALL ? 1UL << width : 0UL);
    for (repeat = 0; repeat < REPEATS; ++repeat)
        printf("%s{\"ticks\":\"%lld\",\"cpu_ns\":\"%llu\",\"peak_working_set_bytes\":\"%llu\",\"peak_live_bytes\":\"%llu\"}",
               repeat ? "," : "", ticks[repeat], cpu[repeat], rss[repeat], live_peak[repeat]);
    printf("],\"checked_build\":%s,\"is_terminal\":%s}\n",
#ifdef CEML_CHECKED
           "true",
#else
           "false",
#endif
           is_terminal ? "true" : "false");
    return identical ? 0 : 3;
}
