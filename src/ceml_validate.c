/* ValidationRunner: one callable target per CEML-V1-SUITE-1 class
 * (docs/CODEX_HANDOFF.md section 17, docs/VALIDATION_PLAN.md section 3).
 *
 * C1 exposes the hooks and uses a reduced bounded mode for `ceml self-test`.
 * That is developer evidence only. Executing the suite as V1, emitting
 * validation evidence and claiming V1-PASS are gated in ceml_main.c on the
 * programme status and are not performed in C1. The reference in every
 * differential check is the separately written definition oracle. */
#include "ceml_validate.h"
#include "ceml_engine.h"
#include "ceml_fs.h"
#include "ceml_oracle.h"
#include "ceml_sha3.h"
#include "ceml_start.h"
#include "ceml_store.h"

#include <stdio.h>
#include <string.h>

const char *const CEML_HOOK_NAME[CEML_HOOK_COUNT] = {
    "elementary_identities", "exhaustive_small_residues", "randomized_bounded_differential", "adversarial_patterns",
    "odd_split_lengths", "terminal_overshoot", "serialization_digest_roundtrip", "checkpoint_restart_equivalence",
    "fault_injection", "feature_route_activation", "formula_defined_fixtures", "checked_sanitized_builds" };

static void check(ceml_hook_result *r, int condition) { ++r->cases; if (!condition) ++r->failures; }

/* Public validation randomness: SHAKE256("CEML-VALIDATION-RANDOM-V1" || 00 || seed32 ||
 * UENC(bits) || UENC(case) || UENC(stream)), top bit forced so the value has exactly `bits` bits. */
static void validation_value(mpz_t out, unsigned long bits, unsigned long case_index, unsigned long stream) {
    static const char prefix[] = "CEML-VALIDATION-RANDOM-V1";
    unsigned char seed[32], bytes[1024];
    ceml_buffer message;
    ceml_keccak shake;
    mpz_t z;
    unsigned long field[3], i;
    size_t length = (bits + 7) >> 3;
    field[0] = bits; field[1] = case_index; field[2] = stream;
    for (i = 0; i < 32; ++i) seed[i] = (unsigned char)i;
    ceml_buffer_init(&message);
    mpz_init(z);
    ceml_buffer_append(&message, prefix, sizeof(prefix));
    ceml_buffer_append(&message, seed, 32);
    for (i = 0; i < 3; ++i) { mpz_set_ui(z, field[i]); ceml_uenc_append(&message, z); }
    ceml_shake256_init(&shake);
    ceml_keccak_update(&shake, message.data, message.length);
    ceml_shake256_squeeze(&shake, bytes, length);
    mpz_import(out, length, 1, 1, 1, 0, bytes);
    mpz_fdiv_r_2exp(out, out, bits);
    mpz_setbit(out, bits - 1);
    mpz_clear(z);
    ceml_buffer_free(&message);
}

/* Engine under `config` for `budget` steps (0 = to first 1) against direct C stepping. */
static int differential(const ceml_config *config, const mpz_t start, unsigned long budget, int fault, int *engine_error) {
    ceml_engine engine;
    ceml_state state;
    mpz_t n, shortcut, odd, standard;
    int rc, equal = 0;
    ceml_state_init(&state);
    mpz_inits(n, shortcut, odd, standard, NULL);
    rc = ceml_engine_init(&engine, config);
    if (!rc) {
        engine.fault = fault;
        rc = ceml_state_set(&state, start);
        if (!rc) rc = ceml_engine_advance(&engine, &state, budget, 0, NULL);
        if (!rc) rc = ceml_engine_check_routes(&engine);
    }
    mpz_set(n, start);
    ceml_oracle_run_c(n, shortcut, odd, standard, budget);
    if (!rc) equal = mpz_cmp(n, state.n) == 0 && mpz_cmp(shortcut, state.shortcut_steps) == 0 &&
                     mpz_cmp(odd, state.odd_steps) == 0 && mpz_cmp(standard, state.standard_steps) == 0;
    if (engine_error) *engine_error = rc;
    ceml_engine_clear(&engine);
    ceml_state_clear(&state);
    mpz_clears(n, shortcut, odd, standard, NULL);
    return equal;
}

static void hook_elementary(int full, ceml_hook_result *r) {
    unsigned long limit = full ? 200000UL : 3000UL, value;
    mpz_t n, c, t, u, shortcut, odd, standard, t_shortcut, t_odd;
    mpz_inits(n, c, t, u, shortcut, odd, standard, t_shortcut, t_odd, NULL);
    for (value = 1; value <= limit; ++value) {
        unsigned long was_odd, v = 0, j;
        mpz_set_ui(c, value); mpz_set_ui(t, value);
        ceml_oracle_c(c);
        if (value & 1) ceml_oracle_c(c);                     /* odd: two C applications reach the T boundary */
        was_odd = ceml_oracle_t(t);
        check(r, mpz_cmp(c, t) == 0 && was_odd == (value & 1));
        if (value & 1) {
            mpz_set_ui(u, value); v = ceml_oracle_u(u);
            mpz_set_ui(t, value);
            for (j = 0; j < v; ++j) ceml_oracle_t(t);        /* one U is v shortcut steps, one of them odd */
            check(r, v >= 1 && mpz_cmp(u, t) == 0 && mpz_odd_p(u));
        }
        if (value <= (full ? 20000UL : 500UL)) {
            mpz_set_ui(n, value); ceml_oracle_run_c(n, shortcut, odd, standard, 0);
            mpz_set_ui(t, value); ceml_oracle_run_t(t, t_shortcut, t_odd, 0);
            mpz_add(c, shortcut, odd);
            check(r, mpz_cmp(c, standard) == 0 && mpz_cmp(shortcut, t_shortcut) == 0 && mpz_cmp(odd, t_odd) == 0 &&
                     mpz_cmp_ui(n, 1) == 0 && mpz_cmp_ui(t, 1) == 0);
        }
    }
    mpz_clears(n, c, t, u, shortcut, odd, standard, t_shortcut, t_odd, NULL);
}

static void hook_exhaustive(int full, ceml_hook_result *r) {
    unsigned long width, top = full ? 16UL : 12UL, k, top_leaf = full ? CEML_LEAF : 12UL;
    mpz_t x, expected;
    mpz_inits(x, expected, NULL);
    for (width = 4; width <= top; width += 4) {             /* every entry of every forcible table width */
        ceml_config config;
        ceml_engine engine;
        unsigned long residue;
        ceml_config_profile(&config);
        config.macro = CEML_MACRO_SMALL; config.width = width;
        check(r, ceml_engine_init(&engine, &config) == CEML_OK);
        for (residue = 0; engine.table && residue < (1UL << width); ++residue) {
            unsigned long j, odd = 0;
            mpz_set_ui(x, (1UL << width) + residue); mpz_set(expected, x);
            for (j = 0; j < width; ++j) odd += ceml_oracle_t(expected);
            mpz_mul_ui(x, x, engine.table[residue].a); mpz_add_ui(x, x, engine.table[residue].b);
            check(r, mpz_divisible_2exp_p(x, width) != 0 && engine.table[residue].odd == odd);
            mpz_tdiv_q_2exp(x, x, width);
            check(r, mpz_cmp(x, expected) == 0);
        }
        ceml_engine_clear(&engine);
    }
    for (k = 1; k <= top_leaf; ++k) {                       /* every leaf block the hierarchical route can use */
        unsigned long residue, step = k > 16 ? 97UL : 1UL;
        for (residue = 0; residue < (1UL << k); residue += step) {
            uint32_t a, b;
            unsigned long odd, j, expected_odd = 0;
            check(r, ceml_leaf(residue, k, &a, &b, &odd) == CEML_OK);
            mpz_set_ui(x, residue); mpz_setbit(x, k + 3); mpz_set(expected, x);
            for (j = 0; j < k; ++j) expected_odd += ceml_oracle_t(expected);
            mpz_mul_ui(x, x, a); mpz_add_ui(x, x, b);
            check(r, mpz_divisible_2exp_p(x, k) != 0 && odd == expected_odd);
            mpz_tdiv_q_2exp(x, x, k);
            check(r, mpz_cmp(x, expected) == 0);
        }
    }
    mpz_clears(x, expected, NULL);
}

static void hook_randomized(int full, ceml_hook_result *r) {
    unsigned long cases = full ? 4000UL : 150UL, index;
    ceml_config config;
    mpz_t n, again;
    mpz_inits(n, again, NULL);
    ceml_config_profile(&config);
    for (index = 0; index < cases; ++index) {
        unsigned long bits = 2 + (index*37) % 4095, budget = 1 + (index*101) % 700;
        validation_value(n, bits, index, 0);
        validation_value(again, bits, index, 0);
        check(r, mpz_cmp(n, again) == 0);                    /* deterministic regeneration */
        check(r, differential(&config, n, budget, CEML_FAULT_NONE, NULL));
    }
    mpz_clears(n, again, NULL);
}

static void hook_adversarial(int full, ceml_hook_result *r) {
    static const unsigned long EXPONENT[] = { 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65, 127, 128, 129,
                                              191, 192, 193, 255, 256, 257, 1023, 1024, 1025, 4095, 4096, 4097 };
    ceml_config config;
    mpz_t n;
    size_t e;
    unsigned shape;
    mpz_init(n);
    ceml_config_profile(&config);
    for (e = 0; e < sizeof(EXPONENT) / sizeof(EXPONENT[0]); ++e) {
        unsigned long m = EXPONENT[e];
        for (shape = 0; shape < 8; ++shape) {
            mpz_set_ui(n, 0);
            mpz_setbit(n, m);
            if (shape == 0) mpz_sub_ui(n, n, 1);             /* 2^m - 1: all-one low words */
            else if (shape == 2) mpz_add_ui(n, n, 1);        /* 2^m + 1 */
            else if (shape == 3) mpz_setbit(n, m >> 1);      /* sparse: long zero runs */
            else if (shape == 4) { unsigned long j; for (j = 0; j < m; j += 2) mpz_setbit(n, j); }   /* alternating */
            else if (shape == 5) mpz_mul_2exp(n, n, 64);     /* long low-zero run */
            else if (shape == 6) { mpz_mul_2exp(n, n, 64); mpz_sub_ui(n, n, 1); }                    /* carry chain */
            else if (shape == 7) { mpz_setbit(n, m + 64); mpz_add_ui(n, n, 3); }                     /* sparse high limb */
            check(r, differential(&config, n, 1, CEML_FAULT_NONE, NULL));
            check(r, differential(&config, n, 65, CEML_FAULT_NONE, NULL));
            check(r, differential(&config, n, full || m <= 257 ? 0 : 700, CEML_FAULT_NONE, NULL));
        }
    }
    mpz_clear(n);
}

static void hook_odd_split(int full, ceml_hook_result *r) {
    static const unsigned long LENGTH[] = { 21, 23, 25, 27, 29, 31, 33, 41, 43, 63, 65, 127, 129, 255, 257, 1023, 1025, 4097 };
    ceml_config config;
    ceml_engine engine;
    mpz_t residue, n, expected, parity, mid, low;
    ceml_block built, word, p1, p2, p3, forward, reversed, left_first, right_first;
    size_t index, count = full ? sizeof(LENGTH) / sizeof(LENGTH[0]) : 14;
    ceml_config_profile(&config);
    ceml_engine_init(&engine, &config);
    mpz_inits(residue, n, expected, parity, mid, low, NULL);
    ceml_block_init(&built); ceml_block_init(&word); ceml_block_init(&p1); ceml_block_init(&p2); ceml_block_init(&p3);
    ceml_block_init(&forward); ceml_block_init(&reversed); ceml_block_init(&left_first); ceml_block_init(&right_first);
    for (index = 0; index < count; ++index) {
        unsigned long k = LENGTH[index], k1 = k >> 1, k2 = k - k1, j, odd = 0, third = k/3;
        validation_value(n, k + 96, (unsigned long)index, 1);
        mpz_fdiv_r_2exp(residue, n, k);
        check(r, k1 + k2 == k && k2 == k1 + 1);                                   /* floor and ceiling halves */
        check(r, ceml_block_build(&engine, &built, residue, k) == CEML_OK && built.k == k);
        mpz_set(expected, n); mpz_set_ui(parity, 0);
        for (j = 0; j < k; ++j) if (ceml_oracle_t(expected)) { mpz_setbit(parity, j); ++odd; }
        ceml_block_from_parity(&word, parity, k);                                 /* independent reconstruction */
        check(r, mpz_cmp(word.a, built.a) == 0 && mpz_cmp(word.b, built.b) == 0 && built.i == odd);
        mpz_mul(mid, built.a, n); mpz_add(mid, mid, built.b);
        check(r, mpz_divisible_2exp_p(mid, k) != 0);
        mpz_tdiv_q_2exp(mid, mid, k);
        check(r, mpz_cmp(mid, expected) == 0);                                    /* 2^k T^k(n) = 3^i n + B */
        /* Order sensitivity: P2 after P1 equals the direct block; the reverse does not when both halves have odd steps. */
        mpz_fdiv_r_2exp(low, residue, k1);
        ceml_block_build(&engine, &p1, low, k1);
        mpz_mul(mid, p1.a, residue); mpz_add(mid, mid, p1.b); mpz_tdiv_q_2exp(mid, mid, k1);
        mpz_fdiv_r_2exp(low, mid, k2);
        ceml_block_build(&engine, &p2, low, k2);
        ceml_block_compose(&forward, &p1, &p2);
        ceml_block_compose(&reversed, &p2, &p1);
        check(r, mpz_cmp(forward.a, built.a) == 0 && mpz_cmp(forward.b, built.b) == 0 && forward.k == k);
        if (p1.i && p2.i && p1.i != k1) check(r, mpz_cmp(reversed.b, built.b) != 0);
        /* Three-way split: (P3 after P2) after P1 equals P3 after (P2 after P1). */
        mpz_fdiv_r_2exp(low, residue, third);
        ceml_block_build(&engine, &p1, low, third);
        mpz_mul(mid, p1.a, residue); mpz_add(mid, mid, p1.b); mpz_tdiv_q_2exp(mid, mid, third);
        mpz_fdiv_r_2exp(low, mid, third);
        ceml_block_build(&engine, &p2, low, third);
        mpz_mul(mid, p2.a, mid); mpz_add(mid, mid, p2.b); mpz_tdiv_q_2exp(mid, mid, third);
        mpz_fdiv_r_2exp(low, mid, k - 2*third);
        ceml_block_build(&engine, &p3, low, k - 2*third);
        ceml_block_compose(&left_first, &p1, &p2); ceml_block_compose(&left_first, &left_first, &p3);
        ceml_block_compose(&right_first, &p2, &p3); ceml_block_compose(&right_first, &p1, &right_first);
        check(r, mpz_cmp(left_first.a, built.a) == 0 && mpz_cmp(left_first.b, built.b) == 0 &&
                 mpz_cmp(right_first.a, built.a) == 0 && mpz_cmp(right_first.b, built.b) == 0);
    }
    ceml_block_clear(&built); ceml_block_clear(&word); ceml_block_clear(&p1); ceml_block_clear(&p2); ceml_block_clear(&p3);
    ceml_block_clear(&forward); ceml_block_clear(&reversed); ceml_block_clear(&left_first); ceml_block_clear(&right_first);
    mpz_clears(residue, n, expected, parity, mid, low, NULL);
    ceml_engine_clear(&engine);
}

static void hook_terminal(int full, ceml_hook_result *r) {
    ceml_config config;
    ceml_engine engine;
    ceml_state state;
    mpz_t n;
    unsigned long m, value, limit = full ? 60000UL : 2500UL, performed;
    int odd_only;
    mpz_init(n);
    ceml_state_init(&state);
    for (odd_only = 0; odd_only < 2; ++odd_only) {
        ceml_config_profile(&config);
        config.terminal_odd_only = odd_only;
        ceml_engine_init(&engine, &config);
        mpz_set_ui(n, 1);                                     /* start 1: terminal, no transition is permitted */
        ceml_state_set(&state, n);
        check(r, ceml_engine_advance(&engine, &state, 0, 0, &performed) == CEML_OK && performed == 0 &&
                 state.terminal_reached && mpz_sgn(state.shortcut_steps) == 0);
        check(r, ceml_engine_advance(&engine, &state, 5, 0, &performed) == CEML_OK && performed == 0);
        for (m = 1; m <= (full ? 600UL : 130UL); ++m) {       /* 2^m reaches the first 1 in exactly m steps */
            mpz_set_ui(n, 0); mpz_setbit(n, m);
            ceml_state_set(&state, n);
            check(r, ceml_engine_advance(&engine, &state, 0, 0, NULL) == CEML_OK && state.terminal_reached &&
                     mpz_cmp_ui(state.shortcut_steps, m) == 0 && mpz_sgn(state.odd_steps) == 0);
            check(r, ceml_macro_length(&config, n) <= m);     /* macro never longer than bit_length - 1 */
            ceml_state_set(&state, n);                        /* an overlong request stops at the first 1 */
            check(r, ceml_engine_advance(&engine, &state, m + 7, 0, &performed) == CEML_OK && performed == m &&
                     state.terminal_reached);
        }
        ceml_engine_clear(&engine);
        for (value = 2; value <= limit; ++value) {
            mpz_set_ui(n, value);
            check(r, ceml_macro_length(&config, n) <= mpz_sizeinbase(n, 2) - 1);
            check(r, differential(&config, n, 0, CEML_FAULT_NONE, NULL));
        }
    }
    ceml_state_clear(&state);
    mpz_clear(n);
}

static int digest_is(const char *label, const void *data, size_t length, const char *expected) {
    char hex[CEML_HEX];
    ceml_domain_digest(label, (const unsigned char *)data, length, hex);
    return strcmp(hex, expected) == 0;
}

static void start_vector(ceml_hook_result *r, unsigned long long digits, unsigned long long index, const char *decimal,
                         unsigned long long retry, const char *digest) {
    unsigned char seed[32];
    char hex[CEML_HEX];
    unsigned long long accepted = 99;
    mpz_t n, expected;
    int i;
    for (i = 0; i < 32; ++i) seed[i] = (unsigned char)i;      /* public non-scientific test seed */
    mpz_init(n); mpz_init_set_str(expected, decimal, 10);
    check(r, ceml_start_generate(seed, digits, index, n, &accepted) && mpz_cmp(n, expected) == 0 && accepted == retry);
    check(r, ceml_start_digest(n, hex) && strcmp(hex, digest) == 0);
    mpz_clears(n, expected, NULL);
}

static void hook_serialization(int full, ceml_hook_result *r) {
    static const unsigned char body_one[] = { 0x43, 0x45, 0x4d, 0x4c, 0x2d, 0x43, 0x4b, 0x50, 0x54, 0x2d, 0x42, 0x4f, 0x44,
                                              0x59, 0x2d, 0x56, 0x31, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 };
    static const unsigned char non_minimal[] = { 0, 0, 0, 0, 0, 0, 0, 2, 0, 1 }, short_frame[] = { 0, 0, 0, 0, 0, 0, 0, 2, 1 },
                               trailing[] = { 0, 0, 0, 0, 0, 0, 0, 1, 1, 0 };
    unsigned char seed[32], digest[32], shake_out[32];
    char hex[CEML_HEX];
    ceml_keccak context;
    ceml_buffer buffer, json;
    ceml_metadata metadata, parsed;
    mpz_t n, decoded;
    unsigned long bits;
    int i;
    (void)full;
    ceml_buffer_init(&buffer); ceml_buffer_init(&json);
    mpz_inits(n, decoded, NULL);
    ceml_sha3_256_init(&context); ceml_sha3_256_final(&context, digest); ceml_hex(digest, 32, hex);
    check(r, strcmp(hex, "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a") == 0);
    ceml_shake256_init(&context); ceml_shake256_squeeze(&context, shake_out, 32); ceml_hex(shake_out, 32, hex);
    check(r, strcmp(hex, "46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762f") == 0);
    for (bits = 0; bits <= 200; ++bits) {                     /* UENC round trip, including 0 and limb boundaries */
        mpz_set_ui(n, 0);
        if (bits) { mpz_setbit(n, bits - 1); if (bits > 3) mpz_add_ui(n, n, 5); }
        buffer.length = 0;
        check(r, ceml_uenc_append(&buffer, n) && ceml_uenc_decode(buffer.data, buffer.length, decoded) && mpz_cmp(n, decoded) == 0);
    }
    check(r, !ceml_uenc_decode(non_minimal, sizeof(non_minimal), decoded));
    check(r, !ceml_uenc_decode(short_frame, sizeof(short_frame), decoded));
    check(r, !ceml_uenc_decode(trailing, sizeof(trailing), decoded));
    mpz_set_ui(n, 1);                                         /* frozen checkpoint body vector */
    check(r, ceml_body_encode(n, &buffer) && buffer.length == sizeof(body_one) && memcmp(buffer.data, body_one, sizeof(body_one)) == 0);
    check(r, digest_is("CEML-CHECKPOINT-BODY-DIGEST-V1", body_one, sizeof(body_one),
                       "181ce6b5c4488f56cac3a7439cf6c42048d03b195e3f0b21bf37f6c59f285a9f"));
    check(r, ceml_body_decode(body_one, sizeof(body_one), decoded) && mpz_cmp_ui(decoded, 1) == 0);
    check(r, !ceml_body_decode(body_one, sizeof(body_one) - 1, decoded));
    check(r, digest_is("CEML-RUN-MANIFEST-V1", "{\"a\":\"1\",\"z\":\"2\"}", 17,
                       "90cef02ce54b3454f57b23c6148914edba7ca5b93813e0847e9e0b77278382bc"));
    for (i = 0; i < 32; ++i) seed[i] = (unsigned char)i;
    ceml_seed_commitment(seed, hex);
    check(r, strcmp(hex, "824873c331f2b22382714991a57809abc6fc3e43600cd31556470006981b9009") == 0);
    start_vector(r, 1, 0, "5", 0, "d9487e99d4abe61f51c82dc14937252d479f4cfa816d44594675035d6bfee7f9");
    start_vector(r, 2, 0, "95", 0, "71fca1897e39b8df0616a3f87d31d6a04139bf86bf0099ab4316f71a7174255e");
    start_vector(r, 6, 3, "200305", 0, "979616fd70427e9a5a1c461bd57f7aabb746915008e2fef314520999a5d6fe31");
    start_vector(r, 20, 0, "13800309462001533421", 1, "c9a821d7a8b775fdc6d88f3655732d9e5e7eb369db8153a4e2fa502d62a51e67");
    start_vector(r, 1, 1, "3", 1, "7a947a3d5d546eb6ad33bc3d1b9580e49a69af455bf0d7f1b1839b3bcccf4692");
    /* Metadata: canonical emit, strict parse, byte-identical re-emit, and rejection of edits. */
    ceml_metadata_init(&metadata); ceml_metadata_init(&parsed);
    strcpy_s(metadata.run_id, sizeof(metadata.run_id), "self-test.codec-1");
    memset(hex, 'a', 64); hex[64] = 0;
    strcpy_s(metadata.manifest_digest, CEML_HEX, hex); strcpy_s(metadata.original_start_digest, CEML_HEX, hex);
    strcpy_s(metadata.build_digest, CEML_HEX, hex); strcpy_s(metadata.machine_profile_digest, CEML_HEX, hex);
    strcpy_s(metadata.validation_evidence_digest, CEML_HEX, hex);
    hex[40] = 0;
    strcpy_s(metadata.protocol_commit, CEML_HEX, hex); strcpy_s(metadata.engine_commit, CEML_HEX, hex);
    mpz_set_ui(n, 27); mpz_set_ui(metadata.shortcut_steps, 5); mpz_set_ui(metadata.odd_steps, 3); mpz_set_ui(metadata.standard_steps, 8);
    check(r, ceml_body_encode(n, &buffer) && ceml_metadata_seal(&metadata, buffer.data, buffer.length) &&
             ceml_metadata_emit(&metadata, 1, &json));
    check(r, ceml_metadata_parse(json.data, json.length, &parsed) && ceml_checkpoint_validate(&parsed, buffer.data, buffer.length, decoded) &&
             mpz_cmp_ui(decoded, 27) == 0);
    if (json.length > 40) {
        json.data[json.length - 3] ^= 1;                      /* edit inside the last digest */
        check(r, !ceml_metadata_parse(json.data, json.length, &parsed));
        json.data[json.length - 3] ^= 1;
        check(r, !ceml_metadata_parse(json.data, json.length - 1, &parsed));
    }
    ceml_metadata_clear(&metadata); ceml_metadata_clear(&parsed);
    mpz_clears(n, decoded, NULL);
    ceml_buffer_free(&buffer); ceml_buffer_free(&json);
}

static void fill_identity(ceml_identity *identity, const char *run_id) {
    char hex[CEML_HEX];
    memset(identity, 0, sizeof(*identity));
    strcpy_s(identity->run_id, sizeof(identity->run_id), run_id);
    ceml_domain_digest("CEML-I1-ENGINEERING-ARTIFACT-V1", (const unsigned char *)run_id, strlen(run_id), hex);
    strcpy_s(identity->manifest_digest, CEML_HEX, hex); strcpy_s(identity->original_start_digest, CEML_HEX, hex);
    strcpy_s(identity->build_digest, CEML_HEX, hex); strcpy_s(identity->machine_profile_digest, CEML_HEX, hex);
    strcpy_s(identity->validation_evidence_digest, CEML_HEX, hex);
    hex[40] = 0;
    strcpy_s(identity->protocol_commit, CEML_HEX, hex); strcpy_s(identity->engine_commit, CEML_HEX, hex);
}

static int clear_directory(const char *entry_name, int is_directory, void *context) {
    char path[600], child[700];
    static const char *const FILES[] = { "state.bin", "metadata.json" };
    int i;
    snprintf(path, sizeof(path), "%s\\%s", (const char *)context, entry_name);
    if (!is_directory) return ceml_fs_remove_file(path);
    for (i = 0; i < 2; ++i) { snprintf(child, sizeof(child), "%s\\%s", path, FILES[i]); ceml_fs_remove_file(child); }
    return ceml_fs_remove_directory(path);
}

/* In-process stop and resume at several exact boundaries. Fresh-process resume is
 * exercised through the `checkpoint` and `resume` commands by the V1 runner. */
static void hook_restart(int full, const char *directory, ceml_hook_result *r) {
    static const unsigned long BITS[] = { 70, 200, 1100, 4200 };
    ceml_config config;
    ceml_identity identity;
    size_t index;
    int streaming;
    (void)full;
    if (!directory) { check(r, 0); return; }
    ceml_config_profile(&config);
    fill_identity(&identity, "self-test.restart-1");
    for (index = 0; index < sizeof(BITS) / sizeof(BITS[0]); ++index) {
        for (streaming = 0; streaming < 2; ++streaming) {
            ceml_engine engine, resumed_engine;
            ceml_state whole, part;
            ceml_recovery recovery;
            ceml_store_timing timing;
            mpz_t start;
            unsigned stops = 0;
            int rc;
            mpz_init(start);
            validation_value(start, BITS[index], (unsigned long)index, 2);
            ceml_state_init(&whole); ceml_state_init(&part);
            ceml_engine_init(&engine, &config);
            ceml_state_set(&whole, start); ceml_state_set(&part, start);
            rc = ceml_engine_advance(&engine, &whole, 0, 0, NULL);          /* uninterrupted */
            check(r, rc == CEML_OK && ceml_fs_make_directory(directory));
            while (rc == CEML_OK && !part.terminal_reached && stops < 40) {
                rc = ceml_engine_advance(&engine, &part, 0, 1 + stops % 3, NULL);     /* stop at a macro boundary */
                if (rc != CEML_OK) break;
                check(r, ceml_store_promote(directory, &identity, part.n, part.shortcut_steps, part.odd_steps, streaming, &timing));
                ceml_recovery_init(&recovery);
                check(r, ceml_store_recover(directory, &identity, &recovery) == CEML_STORE_OK);
                /* Discard all engine state and rebuild derived caches from the checkpoint alone. */
                ceml_engine_init(&resumed_engine, &config);
                mpz_set(part.n, recovery.n);
                mpz_set(part.shortcut_steps, recovery.metadata.shortcut_steps);
                mpz_set(part.odd_steps, recovery.metadata.odd_steps);
                mpz_set(part.standard_steps, recovery.metadata.standard_steps);
                part.terminal_reached = recovery.metadata.terminal_reached;
                ceml_engine_clear(&engine);
                engine = resumed_engine;
                ceml_recovery_clear(&recovery);
                ++stops;
            }
            if (rc == CEML_OK && !part.terminal_reached) rc = ceml_engine_advance(&engine, &part, 0, 0, NULL);
            check(r, rc == CEML_OK && stops >= 1 && mpz_cmp(part.n, whole.n) == 0 &&
                     mpz_cmp(part.shortcut_steps, whole.shortcut_steps) == 0 && mpz_cmp(part.odd_steps, whole.odd_steps) == 0 &&
                     mpz_cmp(part.standard_steps, whole.standard_steps) == 0 && part.terminal_reached == whole.terminal_reached);
            ceml_fs_enumerate(directory, clear_directory, (void *)directory);
            check(r, ceml_fs_remove_directory(directory));
            ceml_engine_clear(&engine);
            ceml_state_clear(&whole); ceml_state_clear(&part);
            mpz_clear(start);
        }
    }
}

static void hook_faults(int full, const char *directory, ceml_hook_result *r) {
    static const int ENGINE_FAULT[] = { CEML_FAULT_PARITY, CEML_FAULT_COEFFICIENT_A, CEML_FAULT_COEFFICIENT_B, CEML_FAULT_LOW_BITS,
                                        CEML_FAULT_PRODUCT, CEML_FAULT_COUNTER, CEML_FAULT_COMPOSITION_ORDER };
    ceml_config config;
    ceml_buffer body, json;
    ceml_metadata metadata, parsed;
    ceml_identity identity, other;
    mpz_t n, decoded;
    size_t index;
    unsigned long sample;
    (void)full;
    mpz_inits(n, decoded, NULL);
    ceml_config_profile(&config);
    for (index = 0; index < sizeof(ENGINE_FAULT) / sizeof(ENGINE_FAULT[0]); ++index) {
        for (sample = 0; sample < 6; ++sample) {
            int error = 0, equal;
            validation_value(n, 900 + 211*sample, sample, 3);
            check(r, differential(&config, n, 400, CEML_FAULT_NONE, NULL));               /* the unfaulted run agrees */
            equal = differential(&config, n, 400, ENGINE_FAULT[index], &error);
            check(r, !equal);            /* detected: an engine check fired or the direct oracle disagreed */
        }
    }
    /* Serialized bytes, digests, counters and provenance. */
    ceml_buffer_init(&body); ceml_buffer_init(&json);
    ceml_metadata_init(&metadata); ceml_metadata_init(&parsed);
    fill_identity(&identity, "self-test.fault-1"); fill_identity(&other, "self-test.fault-2");
    strcpy_s(metadata.run_id, sizeof(metadata.run_id), identity.run_id);
    strcpy_s(metadata.manifest_digest, CEML_HEX, identity.manifest_digest);
    strcpy_s(metadata.original_start_digest, CEML_HEX, identity.original_start_digest);
    strcpy_s(metadata.protocol_commit, CEML_HEX, identity.protocol_commit);
    strcpy_s(metadata.engine_commit, CEML_HEX, identity.engine_commit);
    strcpy_s(metadata.build_digest, CEML_HEX, identity.build_digest);
    strcpy_s(metadata.machine_profile_digest, CEML_HEX, identity.machine_profile_digest);
    strcpy_s(metadata.validation_evidence_digest, CEML_HEX, identity.validation_evidence_digest);
    validation_value(n, 777, 0, 4);
    mpz_set_ui(metadata.shortcut_steps, 12); mpz_set_ui(metadata.odd_steps, 7); mpz_set_ui(metadata.standard_steps, 19);
    check(r, ceml_body_encode(n, &body) && ceml_metadata_seal(&metadata, body.data, body.length) && ceml_metadata_emit(&metadata, 1, &json) &&
             ceml_metadata_parse(json.data, json.length, &parsed) && ceml_checkpoint_validate(&parsed, body.data, body.length, decoded));
    if (body.length > 60 && json.length > 100) {
        unsigned char *counter;
        body.data[50] ^= 4;                                   /* serialized value byte */
        check(r, !ceml_checkpoint_validate(&parsed, body.data, body.length, decoded));
        body.data[50] ^= 4;
        parsed.body_digest[5] = parsed.body_digest[5] == '0' ? '1' : '0';       /* body digest */
        check(r, !ceml_checkpoint_validate(&parsed, body.data, body.length, decoded));
        ceml_metadata_parse(json.data, json.length, &parsed);
        mpz_add_ui(parsed.odd_steps, parsed.odd_steps, 1);    /* serialized counter */
        check(r, !ceml_checkpoint_validate(&parsed, body.data, body.length, decoded));
        counter = (unsigned char *)strstr((char *)json.data, "\"odd_steps\":\"7\"");
        if (counter) { counter[13] = '8'; check(r, !ceml_metadata_parse(json.data, json.length, &parsed)); counter[13] = '7'; }   /* metadata field */
        else check(r, 0);
    } else check(r, 0);
    if (directory && ceml_fs_make_directory(directory)) {     /* provenance field */
        ceml_store_timing timing;
        ceml_recovery recovery;
        check(r, ceml_store_promote(directory, &identity, n, metadata.shortcut_steps, metadata.odd_steps, 0, &timing));
        ceml_recovery_init(&recovery);
        check(r, ceml_store_recover(directory, &other, &recovery) == CEML_STORE_PROVENANCE);
        check(r, ceml_store_recover(directory, &identity, &recovery) == CEML_STORE_OK);
        ceml_recovery_clear(&recovery);
        ceml_fs_enumerate(directory, clear_directory, (void *)directory);
        check(r, ceml_fs_remove_directory(directory));
    } else check(r, 0);
    ceml_metadata_clear(&metadata); ceml_metadata_clear(&parsed);
    ceml_buffer_free(&body); ceml_buffer_free(&json);
    mpz_clears(n, decoded, NULL);
}

static void route_case(ceml_hook_result *r, const ceml_config *config, int required, unsigned long budget) {
    ceml_config forced = *config;
    mpz_t n;
    int error = 0;
    mpz_init(n);
    forced.request[required] = CEML_REQUEST_REQUIRE;
    validation_value(n, 3000, (unsigned long)required, 5);
    check(r, differential(&forced, n, budget, CEML_FAULT_NONE, &error) && error == CEML_OK);
    mpz_clear(n);
}

static void hook_routes(int full, ceml_hook_result *r) {
    ceml_config config, other;
    mpz_t n;
    int error = 0;
    (void)full;
    mpz_init(n);
    ceml_config_profile(&config);
    route_case(r, &config, CEML_ROUTE_HIER_EXPLICIT, 960);
    route_case(r, &config, CEML_ROUTE_ALLOC_COPY, 960);
    route_case(r, &config, CEML_ROUTE_AUDIT_DIVISIBILITY, 960);
    route_case(r, &config, CEML_ROUTE_GMP_PUBLIC, 960);
    route_case(r, &config, CEML_ROUTE_STATE_DENSE, 960);
    route_case(r, &config, CEML_ROUTE_PARALLEL_SINGLE, 960);
    route_case(r, &config, CEML_ROUTE_TERMINAL_T, 0);
    other = config; other.copy = 0; route_case(r, &other, CEML_ROUTE_ALLOC_REUSE, 960);
    other = config; other.audit = CEML_AUDIT_MODULAR; route_case(r, &other, CEML_ROUTE_AUDIT_MODULAR, 960);
    other = config; other.terminal_odd_only = 1; route_case(r, &other, CEML_ROUTE_TERMINAL_U, 0);
    other = config; other.macro = CEML_MACRO_DIRECT; route_case(r, &other, CEML_ROUTE_DIRECT_T, 960);
    other = config; other.macro = CEML_MACRO_SMALL; other.width = 8; route_case(r, &other, CEML_ROUTE_SMALL_AFFINE, 960);
    /* Fail closed: a required route that cannot run, a forbidden route that would run, a table remainder. */
    validation_value(n, 3000, 99, 5);
    other = config; other.request[CEML_ROUTE_SMALL_AFFINE] = CEML_REQUEST_REQUIRE;
    check(r, !differential(&other, n, 960, CEML_FAULT_NONE, &error) && error == CEML_E_ROUTE_NOT_ACTIVATED);
    other = config; other.request[CEML_ROUTE_HIER_EXPLICIT] = CEML_REQUEST_FORBID;
    check(r, !differential(&other, n, 960, CEML_FAULT_NONE, &error) && error == CEML_E_ROUTE_FORBIDDEN);
    other = config; other.macro = CEML_MACRO_SMALL; other.width = 8; other.request[CEML_ROUTE_SMALL_AFFINE] = CEML_REQUEST_REQUIRE;
    check(r, !differential(&other, n, 963, CEML_FAULT_NONE, &error) && error == CEML_E_FALLBACK);
    mpz_clear(n);
}

static void fixture(ceml_hook_result *r, const mpz_t start, unsigned long shortcut, unsigned long odd, unsigned long standard) {
    ceml_config config;
    ceml_engine engine;
    ceml_state state;
    mpz_t n, s, o, c;
    ceml_config_profile(&config);
    ceml_engine_init(&engine, &config);
    ceml_state_init(&state);
    mpz_inits(n, s, o, c, NULL);
    ceml_state_set(&state, start);
    check(r, ceml_engine_advance(&engine, &state, 0, 0, NULL) == CEML_OK && state.terminal_reached &&
             mpz_cmp_ui(state.shortcut_steps, shortcut) == 0 && mpz_cmp_ui(state.odd_steps, odd) == 0 &&
             mpz_cmp_ui(state.standard_steps, standard) == 0);
    mpz_set(n, start);
    ceml_oracle_run_c(n, s, o, c, 0);                         /* recomputed, never trusted as stored */
    check(r, mpz_cmp_ui(n, 1) == 0 && mpz_cmp_ui(s, shortcut) == 0 && mpz_cmp_ui(o, odd) == 0 && mpz_cmp_ui(c, standard) == 0);
    mpz_clears(n, s, o, c, NULL);
    ceml_state_clear(&state);
    ceml_engine_clear(&engine);
}

static void hook_fixtures(int full, ceml_hook_result *r) {
    mpz_t n;
    mpz_init_set_ui(n, 27);
    fixture(r, n, 70, 41, 111);
    mpz_set_ui(n, 0); mpz_setbit(n, 127); mpz_sub_ui(n, n, 1);
    fixture(r, n, 1067, 593, 1660);
    if (full) {                                               /* 2^44497-1: only in the gated full suite */
        mpz_set_ui(n, 0); mpz_setbit(n, 44497); mpz_sub_ui(n, n, 1);
        fixture(r, n, 383917, 214150, 598067);
    }
    mpz_clear(n);
}

/* Fixed-width paths that exist in this engine: the 64-bit leaf construction, the
 * table self-check and the 64-bit modular audit. Their stated bounds are checked
 * here against arbitrary precision; sanitizer runs belong to the checked build. */
static void hook_checked(int full, ceml_hook_result *r) {
    unsigned long k;
    mpz_t a, b, x;
    (void)full;
    mpz_inits(a, b, x, NULL);
    for (k = 1; k <= CEML_LEAF; ++k) {
        uint32_t la, lb;
        unsigned long odd;
        uint64_t all_ones = (((uint64_t)1 << k) - 1);
        check(r, ceml_leaf(all_ones, k, &la, &lb, &odd) == CEML_OK && odd == k);      /* extreme coefficients */
        mpz_ui_pow_ui(a, 3, k); mpz_set_ui(b, 0); mpz_setbit(b, k); mpz_sub(x, a, b);  /* 3^k and 3^k - 2^k */
        check(r, mpz_cmp_ui(a, la) == 0 && mpz_cmp_ui(x, lb) == 0);
    }
    {
        uint32_t la, lb;
        unsigned long odd;
        check(r, ceml_leaf(0, CEML_LEAF + 1, &la, &lb, &odd) != CEML_OK);              /* over-long leaf refused */
        check(r, ceml_leaf(4, 2, &la, &lb, &odd) != CEML_OK);                          /* residue outside 2^k refused */
    }
    check(r, sizeof(unsigned long) >= 4 && sizeof(uint64_t) == 8 && sizeof(mp_limb_t) == 8);
#ifdef CEML_CHECKED
    check(r, 1);                                              /* this is the assertion and run-time-check build */
#endif
    mpz_clears(a, b, x, NULL);
}

int ceml_hook_run(int index, int full, const char *scratch_directory, ceml_hook_result *result) {
    result->cases = result->failures = 0;
    switch (index) {
    case 0: hook_elementary(full, result); break;
    case 1: hook_exhaustive(full, result); break;
    case 2: hook_randomized(full, result); break;
    case 3: hook_adversarial(full, result); break;
    case 4: hook_odd_split(full, result); break;
    case 5: hook_terminal(full, result); break;
    case 6: hook_serialization(full, result); break;
    case 7: hook_restart(full, scratch_directory, result); break;
    case 8: hook_faults(full, scratch_directory, result); break;
    case 9: hook_routes(full, result); break;
    case 10: hook_fixtures(full, result); break;
    case 11: hook_checked(full, result); break;
    default: return 0;
    }
    return 1;
}
