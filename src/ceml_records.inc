
/* ---- CEML-RUN-MANIFEST-1 and CEML-RESULT-1 (fixed member sets, JCS order) ---- */

static void object_member(scanner *s, const char *key, int first) {
    expect(s, first ? "\"" : ",\""); expect(s, key); expect(s, "\":");
}

static void decimal_text(scanner *s, const char *key, char *out, size_t capacity, int first, int positive) {
    text_member(s, key, out, capacity, first);
    if (s->ok && (!ceml_is_decimal(out) || (positive && out[0] == '0'))) s->ok = 0;
}

int ceml_manifest_parse(const unsigned char *json, size_t length, ceml_manifest *m) {
    static const char digest_key[] = ",\"manifest_digest\":\"";
    scanner s;
    const unsigned char *digest_at, *after;
    ceml_buffer preimage;
    char digest[CEML_HEX];
    size_t i;
    int ok;
    s.at = json; s.end = json + length; s.ok = 1;
    expect(&s, "{");
    object_member(&s, "authorization_gate", 1); expect(&s, "\"E1\"");
    text_member(&s, "build_digest", m->build_digest, CEML_HEX, 0);
    constant_member(&s, "checkpoint_format_version", "CEML-CKPT-1");
    text_member(&s, "created_at", m->created_at, sizeof(m->created_at), 0);
    text_member(&s, "engine_commit", m->engine_commit, CEML_HEX, 0);
    expect(&s, ",\"exact_arithmetic\":true");
    constant_member(&s, "experiment", "CEML");
    object_member(&s, "generator", 0); expect(&s, "{");
    object_member(&s, "primitive", 1); expect(&s, "\"SHAKE256-FIPS202-2015\"");
    decimal_text(&s, "retry", m->retry, sizeof(m->retry), 0, 0);
    text_member(&s, "seed_commitment", m->seed_commitment, CEML_HEX, 0);
    text_member(&s, "seed_hex", m->seed_hex, CEML_HEX, 0);
    decimal_text(&s, "start_bit_length", m->start_bit_length, sizeof(m->start_bit_length), 0, 1);
    decimal_text(&s, "start_decimal_digits", m->start_decimal_digits, sizeof(m->start_decimal_digits), 0, 1);
    text_member(&s, "start_digest", m->start_digest, CEML_HEX, 0);
    constant_member(&s, "version", "ceml-start-v1");
    expect(&s, "}");
    text_member(&s, "machine_profile_digest", m->machine_profile_digest, CEML_HEX, 0);
    digest_at = s.at;
    text_member(&s, "manifest_digest", m->manifest_digest, CEML_HEX, 0);
    after = s.at;
    constant_member(&s, "map_semantics_version", "CEML-COLLATZ-1");
    text_member(&s, "protocol_commit", m->protocol_commit, CEML_HEX, 0);
    constant_member(&s, "protocol_version", "CEML-SCI-1");
    text_member(&s, "run_id", m->run_id, sizeof(m->run_id), 0);
    object_member(&s, "rung", 0); expect(&s, "{");
    decimal_text(&s, "decimal_digits", m->decimal_digits, sizeof(m->decimal_digits), 1, 1);
    constant_member(&s, "definition_version", "decimal-digits-v1");
    decimal_text(&s, "rung_index", m->rung_index, sizeof(m->rung_index), 0, 0);
    expect(&s, "}");
    constant_member(&s, "schema_version", "CEML-RUN-MANIFEST-1");
    text_member(&s, "validation_evidence_digest", m->validation_evidence_digest, CEML_HEX, 0);
    expect(&s, "}");
    if (!s.ok || s.at != s.end) return 0;
    ok = run_id_valid(m->run_id) && ceml_is_hex(m->build_digest, 64, 64) && ceml_is_hex(m->engine_commit, 40, 64) &&
         ceml_is_hex(m->seed_commitment, 64, 64) && ceml_is_hex(m->seed_hex, 64, 64) && ceml_is_hex(m->start_digest, 64, 64) &&
         ceml_is_hex(m->machine_profile_digest, 64, 64) && ceml_is_hex(m->manifest_digest, 64, 64) &&
         ceml_is_hex(m->protocol_commit, 40, 64) && ceml_is_hex(m->validation_evidence_digest, 64, 64);
    for (i = 0; ok && m->created_at[i]; ++i) {
        char c = m->created_at[i];
        ok = (c >= '0' && c <= '9') || c == 'T' || c == 'Z' || c == ':' || c == '.' || c == '+' || c == '-';
    }
    if (!ok || (size_t)(after - digest_at) != sizeof(digest_key) - 1 + 64 + 1) return 0;
    /* Self digest: the canonical bytes with exactly the manifest_digest member omitted. */
    ceml_buffer_init(&preimage);
    ok = ceml_buffer_append(&preimage, json, (size_t)(digest_at - json)) &&
         ceml_buffer_append(&preimage, after, (size_t)(s.end - after));
    if (ok) {
        ceml_domain_digest("CEML-RUN-MANIFEST-V1", preimage.data, preimage.length, digest);
        ok = strcmp(digest, m->manifest_digest) == 0;
    }
    ceml_buffer_free(&preimage);
    return ok;
}

static int result_body(const ceml_result *r, int with_digest, ceml_buffer *out) {
    out->length = 0;
    if (!append_text(out, "{") || !member_text(out, "build_digest", r->build_digest, 1) ||
        !member_text(out, "engine_commit", r->engine_commit, 0) || !member_text(out, "experiment", "CEML", 0)) return 0;
    if (r->final_checkpoint_digest[0]) { if (!member_text(out, "final_checkpoint_digest", r->final_checkpoint_digest, 0)) return 0; }
    else if (!append_text(out, ",\"final_checkpoint_digest\":null")) return 0;
    if (r->final_value) { if (!member_text(out, "final_value", r->final_value, 0)) return 0; }
    else if (!append_text(out, ",\"final_value\":null")) return 0;
    if (!member_text(out, "generator_version", "ceml-start-v1", 0) ||
        !member_text(out, "machine_profile_digest", r->machine_profile_digest, 0) ||
        !member_text(out, "manifest_digest", r->manifest_digest, 0) ||
        !member_text(out, "map_semantics_version", "CEML-COLLATZ-1", 0) || !member_text(out, "odd_steps", r->odd_steps, 0) ||
        !member_text(out, "protocol_commit", r->protocol_commit, 0) || !member_text(out, "protocol_version", "CEML-SCI-1", 0)) return 0;
    if (with_digest && !member_text(out, "result_digest", r->result_digest, 0)) return 0;
    if (!member_text(out, "run_id", r->run_id, 0) || !append_text(out, ",\"rung\":{") ||
        !member_text(out, "decimal_digits", r->decimal_digits, 1) || !member_text(out, "definition_version", "decimal-digits-v1", 0) ||
        !member_text(out, "rung_index", r->rung_index, 0) || !append_text(out, "}") ||
        !member_text(out, "schema_version", "CEML-RESULT-1", 0) || !member_text(out, "seed_commitment", r->seed_commitment, 0) ||
        !member_text(out, "shortcut_steps", r->shortcut_steps, 0) || !member_text(out, "standard_steps", r->standard_steps, 0) ||
        !member_text(out, "start_digest", r->start_digest, 0) || !member_text(out, "status", r->status, 0)) return 0;
    if (r->status_detail) { if (!member_text(out, "status_detail", r->status_detail, 0)) return 0; }
    else if (!append_text(out, ",\"status_detail\":null")) return 0;
    return member_text(out, "validation_evidence_digest", r->validation_evidence_digest, 0) && append_text(out, "}");
}

int ceml_result_emit(ceml_result *r, ceml_buffer *out) {
    size_t i;
    if (!ceml_is_decimal(r->shortcut_steps) || !ceml_is_decimal(r->odd_steps) || !ceml_is_decimal(r->standard_steps) ||
        (r->final_value && !ceml_is_decimal(r->final_value))) return 0;
    for (i = 0; r->status_detail && r->status_detail[i]; ++i)      /* detail text restricted to escape-free ASCII */
        if (r->status_detail[i] < 0x20 || r->status_detail[i] > 0x7e || r->status_detail[i] == '"' || r->status_detail[i] == '\\') return 0;
    if (!result_body(r, 0, out)) return 0;
    ceml_domain_digest("CEML-RESULT-V1", out->data, out->length, r->result_digest);
    return result_body(r, 1, out);
}
