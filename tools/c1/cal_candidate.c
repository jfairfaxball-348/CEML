/* Stage: hardware characterization. Initial CEML-CAL-1 route subset only. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>

typedef struct { unsigned long a, b, odd; } Block;

static void construct(Block *p, unsigned long residue) {
    unsigned j;
    p->a = 1; p->b = 0; p->odd = 0;
    for (j = 0; j < 4; ++j) {
        if (residue & 1) {
            p->a *= 3; p->b = 3*p->b + (1UL << j); ++p->odd;
            residue = (3*residue+1) / 2;
        } else residue /= 2;
    }
}

static unsigned long elementary_t(mpz_t n) {
    unsigned long odd = mpz_odd_p(n) ? 1UL : 0UL;
    if (odd) { mpz_mul_ui(n, n, 3); mpz_add_ui(n, n, 1); }
    mpz_tdiv_q_2exp(n, n, 1);
    return odd;
}

int main(int argc, char **argv) {
    mpz_t n, reference, small, expected;
    Block table[16];
    unsigned long steps = 0, odd = 0, reference_steps = 0, reference_odd = 0;
    unsigned long activation = 0, tail = 0, index;
    LARGE_INTEGER frequency, begin, end;
    char output[2048], reference_output[2048];
    int affine, agreement;
    size_t length, i;
    if (argc != 4 || strcmp(argv[1], "--calibration-only") != 0) return 2;
    affine = strcmp(argv[2], "affine-small-public") == 0;
    if (!affine && strcmp(argv[2], "t-direct") != 0) return 2;
    length = strlen(argv[3]);
    if (length != 256 && length != 1024) return 2; /* prescribed 1024/4096-bit classes */
    for (i=0; i<length; ++i) if (!((argv[3][i]>='0' && argv[3][i]<='9') ||
        (argv[3][i]>='a' && argv[3][i]<='f'))) return 2;
    mpz_inits(n, reference, small, expected, NULL);
    if (mpz_set_str(n, argv[3], 16) || mpz_sizeinbase(n, 2) != length*4 || !mpz_odd_p(n)) return 2;
    mpz_set(reference, n);
    for (index=0; index<16; ++index) {
        unsigned j;
        construct(&table[index], index);
        mpz_set_ui(small, 16+index); mpz_set(expected, small);
        for (j=0; j<4; ++j) (void)elementary_t(expected);
        mpz_mul_ui(small, small, table[index].a);
        mpz_add_ui(small, small, table[index].b);
        if (!mpz_divisible_2exp_p(small, 4)) return 3;
        mpz_tdiv_q_2exp(small, small, 4);
        if (mpz_cmp(small, expected)) return 3;
    }
    if (!QueryPerformanceFrequency(&frequency) || !QueryPerformanceCounter(&begin)) return 4;
    while (steps < 256 && mpz_cmp_ui(n, 1) != 0) {
        if (affine && steps <= 252 && mpz_sizeinbase(n, 2) > 4) {
            const Block *block = &table[mpz_fdiv_ui(n, 16)];
            mpz_mul_ui(n, n, block->a); mpz_add_ui(n, n, block->b);
            if (!mpz_divisible_2exp_p(n, 4)) return 3;
            mpz_tdiv_q_2exp(n, n, 4);
            steps += 4; odd += block->odd; ++activation;
        } else {
            odd += elementary_t(n); ++steps;
            if (affine) ++tail; else ++activation;
        }
    }
    if (!QueryPerformanceCounter(&end)) return 4;
    /* Independent definition C path: no candidate elementary/affine helper. */
    while (reference_steps < 256 && mpz_cmp_ui(reference, 1) != 0) {
        if (mpz_even_p(reference)) {
            mpz_tdiv_q_2exp(reference, reference, 1);
        } else {
            mpz_mul_ui(reference, reference, 3); mpz_add_ui(reference, reference, 1);
            if (!mpz_even_p(reference)) return 3;
            mpz_tdiv_q_2exp(reference, reference, 1); ++reference_odd;
        }
        ++reference_steps;
    }
    agreement = mpz_cmp(n, reference) == 0 && steps == reference_steps && odd == reference_odd;
    mpz_get_str(output, 16, n); mpz_get_str(reference_output, 16, reference);
    printf("{\"kind\":\"candidate\",\"route\":\"%s\",\"n_hex\":\"%s\","
           "\"reference_hex\":\"%s\",\"shortcut_steps\":\"%lu\",\"odd_steps\":\"%lu\","
           "\"standard_steps\":\"%lu\",\"reference_shortcut_steps\":\"%lu\",\"reference_odd_steps\":\"%lu\","
           "\"activated_count\":\"%lu\",\"fallback_count\":\"0\",\"tail_count\":\"%lu\","
           "\"table_entries_checked\":\"16\",\"correctness_agreement\":%s,\"kernel_ticks\":\"%lld\","
           "\"qpc_frequency\":\"%lld\"}\n", argv[2], output, reference_output, steps, odd, steps+odd,
           reference_steps, reference_odd, activation, tail, agreement ? "true" : "false",
           (long long)(end.QuadPart-begin.QuadPart), (long long)frequency.QuadPart);
    mpz_clears(n, reference, small, expected, NULL);
    return agreement && activation > 0 && tail == 0 ? 0 : 3;
}
