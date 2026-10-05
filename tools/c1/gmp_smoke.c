/* Stage: hardware characterization. Fixed small public-API capability probe.
 * No trajectory, calibration timing, scientific input, or GMP internals. */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <gmp.h>

int main(void) {
    mpz_t a, b, product, roundtrip;
    char text[160];
    unsigned char bytes[80];
    size_t count = 0;
    int ok = 1;
    wchar_t application_name[32768], library_name[32768];
    DWORD application_length = GetModuleFileNameW(NULL, application_name, 32768);
    DWORD library_length = GetModuleFileNameW(GetModuleHandleW(L"libgmp-10.dll"), library_name, 32768);
    wchar_t *application_last = wcsrchr(application_name, L'\\');
    wchar_t *library_last = wcsrchr(library_name, L'\\');
    int local_library = 0;
    if (application_length > 0 && application_length < 32768 && library_length > 0 &&
        library_length < 32768 && application_last && library_last) {
        *application_last = 0;
        *library_last = 0;
        local_library = _wcsicmp(application_name, library_name) == 0;
    }
    ok &= local_library;
    mpz_inits(a, b, product, roundtrip, NULL);
    ok &= mpz_set_str(a, "123456789012345678901234567890", 10) == 0;
    ok &= mpz_set_str(b, "98765432109876543210987654321", 10) == 0;
    mpz_mul(product, a, b);
    mpz_get_str(text, 10, product); /* caller owns the output buffer */
    ok &= strcmp(text, "12193263113702179522618503273362292333223746380111126352690") == 0;
    mpz_export(bytes, &count, 1, 1, 1, 0, product);
    mpz_import(roundtrip, count, 1, 1, 1, 0, bytes);
    ok &= count > 0 && bytes[0] != 0 && mpz_cmp(product, roundtrip) == 0;
    ok &= strcmp(gmp_version, "6.3.0") == 0;
    ok &= __GNU_MP_VERSION == 6 && __GNU_MP_VERSION_MINOR == 3 && __GNU_MP_VERSION_PATCHLEVEL == 0;
    ok &= GMP_NAIL_BITS == 0 && GMP_LIMB_BITS == 64 && mp_bits_per_limb == 64;
    ok &= sizeof(void *) == 8 && sizeof(long) == 4 && sizeof(mp_limb_t) == 8;
    printf("{\"ok\":%s,\"runtime_version\":\"%s\",\"header_version\":\"6.3.0\","
           "\"pointer_bytes\":\"%u\",\"long_bytes\":\"%u\",\"limb_bytes\":\"%u\","
           "\"limb_bits\":\"%u\",\"nail_bits\":\"%u\",\"export_bytes\":\"%u\","
           "\"product_decimal\":\"%s\",\"roundtrip_equal\":%s,\"dll_beside_executable\":%s}\n",
           ok ? "true" : "false", gmp_version, (unsigned)sizeof(void *),
           (unsigned)sizeof(long), (unsigned)sizeof(mp_limb_t), (unsigned)GMP_LIMB_BITS,
           (unsigned)GMP_NAIL_BITS, (unsigned)count, text,
           mpz_cmp(product, roundtrip) == 0 ? "true" : "false", local_library ? "true" : "false");
    mpz_clears(a, b, product, roundtrip, NULL);
    return ok ? 0 : 1;
}
