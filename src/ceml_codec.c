#include "ceml_codec.h"
#include "ceml_sha3.h"

#include <stdlib.h>
#include <string.h>

static const char BODY_LABEL[] = "CEML-CKPT-BODY-V1";

void ceml_buffer_init(ceml_buffer *buffer) { buffer->data = NULL; buffer->length = buffer->capacity = 0; }

void ceml_buffer_free(ceml_buffer *buffer) { free(buffer->data); ceml_buffer_init(buffer); }

int ceml_buffer_append(ceml_buffer *buffer, const void *data, size_t length) {
    if (length > (size_t)-1 - buffer->length) return 0;
    if (buffer->length + length > buffer->capacity) {
        size_t capacity = buffer->capacity ? buffer->capacity : 256;
        unsigned char *grown;
        while (capacity < buffer->length + length) {
            if (capacity > (size_t)-1/2) { capacity = buffer->length + length; break; }
            capacity *= 2;
        }
        grown = (unsigned char *)realloc(buffer->data, capacity);
        if (!grown) return 0;
        buffer->data = grown; buffer->capacity = capacity;
    }
    if (length) memcpy(buffer->data + buffer->length, data, length);
    buffer->length += length;
    return 1;
}

static int append_text(ceml_buffer *buffer, const char *text) { return ceml_buffer_append(buffer, text, strlen(text)); }

void ceml_domain_digest(const char *label, const unsigned char *data, size_t length, char hex[CEML_HEX]) {
    ceml_keccak context;
    unsigned char digest[32];
    ceml_sha3_256_init(&context);
    ceml_keccak_update(&context, label, strlen(label) + 1);   /* label and its NUL */
    ceml_keccak_update(&context, data, length);
    ceml_sha3_256_final(&context, digest);
    ceml_hex(digest, 32, hex);
}

int ceml_is_hex(const char *text, size_t minimum, size_t maximum) {
    size_t i, length = strlen(text);
    if (length < minimum || length > maximum) return 0;
    for (i = 0; i < length; ++i)
        if (!((text[i] >= '0' && text[i] <= '9') || (text[i] >= 'a' && text[i] <= 'f'))) return 0;
    return 1;
}

int ceml_is_decimal(const char *text) {
    size_t i;
    if (!text[0] || (text[0] == '0' && text[1])) return 0;
    for (i = 0; text[i]; ++i) if (text[i] < '0' || text[i] > '9') return 0;
    return 1;
}

static unsigned char *reserve(ceml_buffer *buffer, size_t extra) {
    size_t offset = buffer->length;
    if (extra > (size_t)-1 - offset) return NULL;
    if (offset + extra > buffer->capacity) {
        unsigned char *grown = (unsigned char *)realloc(buffer->data, offset + extra);
        if (!grown) return NULL;
        buffer->data = grown; buffer->capacity = offset + extra;
    }
    buffer->length = offset + extra;
    return buffer->data + offset;
}

int ceml_body_encode(const mpz_t n, ceml_buffer *body) {
    size_t bytes, written = 0, i;
    unsigned char frame[8], *magnitude;
    if (mpz_sgn(n) <= 0) return 0;
    bytes = (mpz_sizeinbase(n, 2) + 7) >> 3;
    for (i = 0; i < 8; ++i) frame[i] = (unsigned char)((unsigned long long)bytes >> (8*(7 - i)));
    body->length = 0;
    if (!ceml_buffer_append(body, BODY_LABEL, CEML_BODY_PREFIX) || !ceml_buffer_append(body, frame, 8)) return 0;
    magnitude = reserve(body, bytes);
    if (!magnitude) return 0;
    /* The documented exporter writes the minimal big-endian magnitude. */
    mpz_export(magnitude, &written, 1, 1, 1, 0, n);
    return written == bytes && magnitude[0] != 0;
}

int ceml_body_decode(const unsigned char *body, size_t length, mpz_t n) {
    unsigned long long declared = 0;
    size_t i;
    if (length < CEML_BODY_PREFIX + 9 || memcmp(body, BODY_LABEL, CEML_BODY_PREFIX) != 0) return 0;
    for (i = 0; i < 8; ++i) declared = (declared << 8) | body[CEML_BODY_PREFIX + i];
    if (declared != (unsigned long long)(length - CEML_BODY_PREFIX - 8)) return 0;   /* no trailing bytes */
    if (body[CEML_BODY_PREFIX + 8] == 0) return 0;      /* zero or non-minimal magnitude */
    mpz_import(n, (size_t)declared, 1, 1, 1, 0, body + CEML_BODY_PREFIX + 8);
    return mpz_sgn(n) > 0;
}

void ceml_metadata_init(ceml_metadata *m) {
    memset(m, 0, sizeof(*m));
    mpz_inits(m->sequence, m->body_bytes, m->shortcut_steps, m->odd_steps, m->standard_steps, NULL);
}

void ceml_metadata_clear(ceml_metadata *m) {
    mpz_clears(m->sequence, m->body_bytes, m->shortcut_steps, m->odd_steps, m->standard_steps, NULL);
}

static int run_id_valid(const char *text) {
    size_t i, length = strlen(text);
    if (length < 1 || length > 128) return 0;
    for (i = 0; i < length; ++i) {
        char c = text[i];
        int alnum = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
        if (!(alnum || (i > 0 && (c == '.' || c == '_' || c == '-')))) return 0;
    }
    return 1;
}

static int member_text(ceml_buffer *out, const char *key, const char *value, int first) {
    return append_text(out, first ? "\"" : ",\"") && append_text(out, key) && append_text(out, "\":\"") &&
           append_text(out, value) && append_text(out, "\"");
}

static int member_number(ceml_buffer *out, const char *key, const mpz_t value) {
    char *text;
    int ok;
    if (mpz_sgn(value) < 0) return 0;
    text = mpz_get_str(NULL, 10, value);
    if (!text) return 0;
    ok = member_text(out, key, text, 0);
    {
        void (*release)(void *, size_t);
        mp_get_memory_functions(NULL, NULL, &release);
        release(text, strlen(text) + 1);
    }
    return ok;
}

static int fields_valid(const ceml_metadata *m, int with_digest) {
    return run_id_valid(m->run_id) && ceml_is_hex(m->manifest_digest, 64, 64) &&
           ceml_is_hex(m->original_start_digest, 64, 64) && ceml_is_hex(m->protocol_commit, 40, 64) &&
           ceml_is_hex(m->engine_commit, 40, 64) && ceml_is_hex(m->build_digest, 64, 64) &&
           ceml_is_hex(m->machine_profile_digest, 64, 64) && ceml_is_hex(m->validation_evidence_digest, 64, 64) &&
           ceml_is_hex(m->body_digest, 64, 64) && ceml_is_hex(m->current_value_digest, 64, 64) &&
           (!m->has_previous || ceml_is_hex(m->previous_metadata_digest, 64, 64)) &&
           (!with_digest || ceml_is_hex(m->metadata_digest, 64, 64)) && mpz_sgn(m->body_bytes) > 0 &&
           mpz_sgn(m->sequence) >= 0 && mpz_sgn(m->shortcut_steps) >= 0 && mpz_sgn(m->odd_steps) >= 0 &&
           mpz_sgn(m->standard_steps) >= 0;
}

/* Member names are ASCII, so JCS code-unit order is plain byte order. Every
 * value is restricted to characters that need no JSON escaping. */
int ceml_metadata_emit(const ceml_metadata *m, int with_digest, ceml_buffer *out) {
    out->length = 0;
    if (!fields_valid(m, with_digest)) return 0;
    if (!append_text(out, "{\"body_bytes\":\"")) return 0;
    {
        char *text = mpz_get_str(NULL, 10, m->body_bytes);
        void (*release)(void *, size_t);
        int ok;
        if (!text) return 0;
        ok = append_text(out, text) && append_text(out, "\"");
        mp_get_memory_functions(NULL, NULL, &release);
        release(text, strlen(text) + 1);
        if (!ok) return 0;
    }
    if (!member_text(out, "body_digest", m->body_digest, 0) || !member_text(out, "build_digest", m->build_digest, 0) ||
        !member_text(out, "checkpoint_format_version", "CEML-CKPT-1", 0) ||
        !member_text(out, "current_value_digest", m->current_value_digest, 0) ||
        !member_text(out, "engine_commit", m->engine_commit, 0) ||
        !member_text(out, "machine_profile_digest", m->machine_profile_digest, 0) ||
        !member_text(out, "manifest_digest", m->manifest_digest, 0) ||
        !member_text(out, "map_semantics_version", "CEML-COLLATZ-1", 0)) return 0;
    if (with_digest && !member_text(out, "metadata_digest", m->metadata_digest, 0)) return 0;
    if (!member_number(out, "odd_steps", m->odd_steps) ||
        !member_text(out, "original_start_digest", m->original_start_digest, 0)) return 0;
    if (m->has_previous) { if (!member_text(out, "previous_metadata_digest", m->previous_metadata_digest, 0)) return 0; }
    else if (!append_text(out, ",\"previous_metadata_digest\":null")) return 0;
    if (!member_text(out, "protocol_commit", m->protocol_commit, 0) ||
        !member_text(out, "protocol_version", "CEML-SCI-1", 0) || !member_text(out, "run_id", m->run_id, 0) ||
        !member_text(out, "schema_version", "CEML-CHECKPOINT-METADATA-1", 0) ||
        !member_number(out, "sequence", m->sequence) || !member_number(out, "shortcut_steps", m->shortcut_steps) ||
        !member_number(out, "standard_steps", m->standard_steps)) return 0;
    if (!append_text(out, m->terminal_reached ? ",\"terminal_reached\":true" : ",\"terminal_reached\":false")) return 0;
    return member_text(out, "validation_evidence_digest", m->validation_evidence_digest, 0) && append_text(out, "}");
}

static void body_digests(const unsigned char *body, size_t length, char body_digest[CEML_HEX], char current[CEML_HEX]) {
    ceml_domain_digest("CEML-CHECKPOINT-BODY-DIGEST-V1", body, length, body_digest);
    ceml_domain_digest("CEML-CHECKPOINT-CURRENT-V1", body + CEML_BODY_PREFIX, length - CEML_BODY_PREFIX, current);
}

int ceml_metadata_seal(ceml_metadata *m, const unsigned char *body, size_t body_length) {
    if (body_length < CEML_BODY_PREFIX + 9) return 0;
    body_digests(body, body_length, m->body_digest, m->current_value_digest);
    mpz_import(m->body_bytes, 1, 1, sizeof(body_length), 0, 0, &body_length);
    return ceml_metadata_finish(m);
}

int ceml_metadata_finish(ceml_metadata *m) {
    ceml_buffer canonical;
    int ok;
    ceml_buffer_init(&canonical);
    ok = ceml_metadata_emit(m, 0, &canonical);
    if (ok) ceml_domain_digest("CEML-CHECKPOINT-METADATA-V1", canonical.data, canonical.length, m->metadata_digest);
    ceml_buffer_free(&canonical);
    return ok;
}

int ceml_body_stream(const mpz_t n, ceml_sink sink, void *context, ceml_metadata *m) {
    static const char body_label[] = "CEML-CHECKPOINT-BODY-DIGEST-V1", current_label[] = "CEML-CHECKPOINT-CURRENT-V1";
    ceml_keccak body, current;
    unsigned char frame[8], digest[32], *magnitude;
    size_t bytes, written = 0, offset, i, total;
    int ok;
    if (mpz_sgn(n) <= 0) return 0;
    bytes = (mpz_sizeinbase(n, 2) + 7) >> 3;
    magnitude = (unsigned char *)malloc(bytes);
    if (!magnitude) return 0;
    mpz_export(magnitude, &written, 1, 1, 1, 0, n);
    for (i = 0; i < 8; ++i) frame[i] = (unsigned char)((unsigned long long)bytes >> (8*(7 - i)));
    ceml_sha3_256_init(&body); ceml_keccak_update(&body, body_label, sizeof(body_label));
    ceml_sha3_256_init(&current); ceml_keccak_update(&current, current_label, sizeof(current_label));
    ceml_keccak_update(&body, BODY_LABEL, CEML_BODY_PREFIX);
    ceml_keccak_update(&body, frame, 8); ceml_keccak_update(&current, frame, 8);
    ok = written == bytes && magnitude[0] != 0 && sink(BODY_LABEL, CEML_BODY_PREFIX, context) && sink(frame, 8, context);
    for (offset = 0; ok && offset < bytes; ) {
        size_t chunk = bytes - offset > 65536 ? 65536 : bytes - offset;
        ceml_keccak_update(&body, magnitude + offset, chunk); ceml_keccak_update(&current, magnitude + offset, chunk);
        ok = sink(magnitude + offset, chunk, context);
        offset += chunk;
    }
    free(magnitude);
    if (!ok) return 0;
    ceml_sha3_256_final(&body, digest); ceml_hex(digest, 32, m->body_digest);
    ceml_sha3_256_final(&current, digest); ceml_hex(digest, 32, m->current_value_digest);
    total = CEML_BODY_PREFIX + 8 + bytes;
    mpz_import(m->body_bytes, 1, 1, sizeof(total), 0, 0, &total);
    return 1;
}

typedef struct { const unsigned char *at, *end; int ok; } scanner;

static void expect(scanner *s, const char *text) {
    size_t length = strlen(text);
    if (!s->ok || (size_t)(s->end - s->at) < length || memcmp(s->at, text, length) != 0) { s->ok = 0; return; }
    s->at += length;
}

static void quoted(scanner *s, char *out, size_t capacity) {
    size_t length = 0;
    expect(s, "\"");
    while (s->ok && s->at < s->end && *s->at != '"') {
        unsigned char c = *s->at++;
        if (c < 0x20 || c > 0x7e || c == '\\' || length + 1 >= capacity) { s->ok = 0; return; }
        out[length++] = (char)c;
    }
    out[length] = 0;
    expect(s, "\"");
}

static void text_member(scanner *s, const char *key, char *out, size_t capacity, int first) {
    expect(s, first ? "\"" : ",\""); expect(s, key); expect(s, "\":");
    quoted(s, out, capacity);
}

static void constant_member(scanner *s, const char *key, const char *value) {
    char found[64];
    text_member(s, key, found, sizeof(found), 0);
    if (s->ok && strcmp(found, value) != 0) s->ok = 0;
}

static void number_member(scanner *s, const char *key, mpz_t value, int first) {
    /* Bounded: a decimal counter in a checkpoint cannot exceed its own file. */
    size_t capacity = (size_t)(s->end - s->at) + 1;
    char *text = (char *)malloc(capacity);
    if (!text) { s->ok = 0; return; }
    text_member(s, key, text, capacity, first);
    if (s->ok && (!ceml_is_decimal(text) || mpz_set_str(value, text, 10) != 0)) s->ok = 0;
    free(text);
}

int ceml_metadata_parse(const unsigned char *json, size_t length, ceml_metadata *m) {
    scanner s;
    ceml_buffer canonical;
    char digest[CEML_HEX];
    int ok;
    s.at = json; s.end = json + length; s.ok = 1;
    expect(&s, "{");
    number_member(&s, "body_bytes", m->body_bytes, 1);
    text_member(&s, "body_digest", m->body_digest, CEML_HEX, 0);
    text_member(&s, "build_digest", m->build_digest, CEML_HEX, 0);
    constant_member(&s, "checkpoint_format_version", "CEML-CKPT-1");
    text_member(&s, "current_value_digest", m->current_value_digest, CEML_HEX, 0);
    text_member(&s, "engine_commit", m->engine_commit, CEML_HEX, 0);
    text_member(&s, "machine_profile_digest", m->machine_profile_digest, CEML_HEX, 0);
    text_member(&s, "manifest_digest", m->manifest_digest, CEML_HEX, 0);
    constant_member(&s, "map_semantics_version", "CEML-COLLATZ-1");
    text_member(&s, "metadata_digest", m->metadata_digest, CEML_HEX, 0);
    number_member(&s, "odd_steps", m->odd_steps, 0);
    text_member(&s, "original_start_digest", m->original_start_digest, CEML_HEX, 0);
    expect(&s, ",\"previous_metadata_digest\":");
    if (s.ok && s.at < s.end && *s.at == 'n') { expect(&s, "null"); m->has_previous = 0; m->previous_metadata_digest[0] = 0; }
    else { quoted(&s, m->previous_metadata_digest, CEML_HEX); m->has_previous = 1; }
    text_member(&s, "protocol_commit", m->protocol_commit, CEML_HEX, 0);
    constant_member(&s, "protocol_version", "CEML-SCI-1");
    text_member(&s, "run_id", m->run_id, sizeof(m->run_id), 0);
    constant_member(&s, "schema_version", "CEML-CHECKPOINT-METADATA-1");
    number_member(&s, "sequence", m->sequence, 0);
    number_member(&s, "shortcut_steps", m->shortcut_steps, 0);
    number_member(&s, "standard_steps", m->standard_steps, 0);
    expect(&s, ",\"terminal_reached\":");
    if (s.ok && s.at < s.end && *s.at == 't') { expect(&s, "true"); m->terminal_reached = 1; }
    else { expect(&s, "false"); m->terminal_reached = 0; }
    text_member(&s, "validation_evidence_digest", m->validation_evidence_digest, CEML_HEX, 0);
    expect(&s, "}");
    if (!s.ok || s.at != s.end) return 0;
    /* Byte-for-byte canonical round trip, then the self digest. */
    ceml_buffer_init(&canonical);
    ok = ceml_metadata_emit(m, 1, &canonical) && canonical.length == length && memcmp(canonical.data, json, length) == 0;
    if (ok) {
        ok = ceml_metadata_emit(m, 0, &canonical);
        if (ok) {
            ceml_domain_digest("CEML-CHECKPOINT-METADATA-V1", canonical.data, canonical.length, digest);
            ok = strcmp(digest, m->metadata_digest) == 0;
        }
    }
    ceml_buffer_free(&canonical);
    return ok;
}

int ceml_checkpoint_validate(const ceml_metadata *m, const unsigned char *body, size_t body_length, mpz_t n) {
    char body_digest[CEML_HEX], current[CEML_HEX];
    mpz_t sum;
    int ok;
    if (!fields_valid(m, 1) || !ceml_body_decode(body, body_length, n)) return 0;
    mpz_init(sum);
    mpz_import(sum, 1, 1, sizeof(body_length), 0, 0, &body_length);
    ok = mpz_cmp(sum, m->body_bytes) == 0;
    body_digests(body, body_length, body_digest, current);
    ok = ok && strcmp(body_digest, m->body_digest) == 0 && strcmp(current, m->current_value_digest) == 0;
    mpz_add(sum, m->shortcut_steps, m->odd_steps);
    ok = ok && mpz_cmp(sum, m->standard_steps) == 0 && mpz_cmp(m->odd_steps, m->shortcut_steps) <= 0;
    ok = ok && ((mpz_cmp_ui(n, 1) == 0) == (m->terminal_reached != 0));
    ok = ok && ((mpz_sgn(m->sequence) == 0) == (m->has_previous == 0));
    mpz_clear(sum);
    return ok;
}

int ceml_uenc_append(ceml_buffer *out, const mpz_t value) {
    size_t bytes, written = 0, i;
    unsigned char frame[8], *magnitude;
    if (mpz_sgn(value) < 0) return 0;
    bytes = mpz_sgn(value) == 0 ? 1 : (mpz_sizeinbase(value, 2) + 7) >> 3;
    for (i = 0; i < 8; ++i) frame[i] = (unsigned char)((unsigned long long)bytes >> (8*(7 - i)));
    if (!ceml_buffer_append(out, frame, 8)) return 0;
    magnitude = reserve(out, bytes);
    if (!magnitude) return 0;
    if (mpz_sgn(value) == 0) { magnitude[0] = 0; return 1; }      /* MAG(0) = 00 */
    mpz_export(magnitude, &written, 1, 1, 1, 0, value);
    return written == bytes;
}

int ceml_uenc_decode(const unsigned char *data, size_t length, mpz_t value) {
    unsigned long long declared = 0;
    size_t i;
    if (length < 9) return 0;
    for (i = 0; i < 8; ++i) declared = (declared << 8) | data[i];
    if (declared != (unsigned long long)(length - 8)) return 0;      /* length mismatch or trailing bytes */
    if (declared > 1 && data[8] == 0) return 0;                      /* non-minimal magnitude */
    mpz_import(value, (size_t)declared, 1, 1, 1, 0, data + 8);
    return 1;
}

#include "ceml_records.h"
#include "ceml_records.inc"
