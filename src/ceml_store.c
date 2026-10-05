#include "ceml_store.h"
#include "ceml_fs.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PATH_MAXIMUM 900
#define METADATA_MAXIMUM ((size_t)1 << 26)
#define BODY_MAXIMUM ((size_t)-1 >> 1)
#define POINTER_MAXIMUM 4096

typedef struct { char *name; int is_directory; } entry;
typedef struct { entry *items; size_t count, capacity; int ok; } listing;
typedef struct { mpz_t sequence; int valid, foreign_identity; char digest[CEML_HEX], previous[CEML_HEX]; int has_previous; } generation;

static int collect(const char *name, int is_directory, void *context) {
    listing *list = (listing *)context;
    if (list->count == list->capacity) {
        size_t capacity = list->capacity ? list->capacity*2 : 16;
        entry *grown = (entry *)realloc(list->items, capacity*sizeof(entry));
        if (!grown) return list->ok = 0;
        list->items = grown; list->capacity = capacity;
    }
    list->items[list->count].name = _strdup(name);
    if (!list->items[list->count].name) return list->ok = 0;
    list->items[list->count++].is_directory = is_directory;
    return 1;
}

static void free_listing(listing *list) {
    size_t i;
    for (i = 0; i < list->count; ++i) free(list->items[i].name);
    free(list->items);
}

static int join(char *out, const char *a, const char *b, const char *c) {
    return snprintf(out, PATH_MAXIMUM, "%s\\%s%s%s", a, b, c ? "\\" : "", c ? c : "") < PATH_MAXIMUM;
}

static int ends_with(const char *text, const char *suffix) {
    size_t a = strlen(text), b = strlen(suffix);
    return a >= b && strcmp(text + a - b, suffix) == 0;
}

static char *decimal(const mpz_t value) { return mpz_get_str(NULL, 10, value); }

static void release(char *text) {
    void (*free_function)(void *, size_t);
    mp_get_memory_functions(NULL, NULL, &free_function);
    free_function(text, strlen(text) + 1);
}

static int identity_matches(const ceml_metadata *m, const ceml_identity *id) {
    return strcmp(m->run_id, id->run_id) == 0 && strcmp(m->manifest_digest, id->manifest_digest) == 0 &&
           strcmp(m->original_start_digest, id->original_start_digest) == 0 &&
           strcmp(m->protocol_commit, id->protocol_commit) == 0 && strcmp(m->engine_commit, id->engine_commit) == 0 &&
           strcmp(m->build_digest, id->build_digest) == 0 &&
           strcmp(m->machine_profile_digest, id->machine_profile_digest) == 0 &&
           strcmp(m->validation_evidence_digest, id->validation_evidence_digest) == 0;
}

/* Independent validation of one published generation from its own bytes. */
static int load_generation(const char *directory, const char *name, ceml_metadata *metadata, mpz_t n) {
    char path[PATH_MAXIMUM];
    ceml_buffer json, body;
    mpz_t named;
    int ok;
    ceml_buffer_init(&json); ceml_buffer_init(&body);
    mpz_init(named);
    ok = join(path, directory, name, "metadata.json") && ceml_fs_read_all(path, &json, METADATA_MAXIMUM) &&
         join(path, directory, name, "state.bin") && ceml_fs_read_all(path, &body, BODY_MAXIMUM) &&
         ceml_metadata_parse(json.data, json.length, metadata) &&
         ceml_checkpoint_validate(metadata, body.data, body.length, n) &&
         mpz_set_str(named, name + 4, 10) == 0 && mpz_cmp(named, metadata->sequence) == 0;
    mpz_clear(named);
    ceml_buffer_free(&json); ceml_buffer_free(&body);
    return ok;
}

void ceml_recovery_init(ceml_recovery *recovery) {
    memset(recovery, 0, sizeof(*recovery));
    ceml_metadata_init(&recovery->metadata);
    mpz_init(recovery->n);
    recovery->status = CEML_STORE_IO;
}

void ceml_recovery_clear(ceml_recovery *recovery) {
    ceml_metadata_clear(&recovery->metadata);
    mpz_clear(recovery->n);
}

static int published_name(const entry *item) {
    return item->is_directory && strncmp(item->name, "gen-", 4) == 0 && ceml_is_decimal(item->name + 4);
}

int ceml_store_recover(const char *directory, const ceml_identity *expected, ceml_recovery *recovery) {
    listing list = { NULL, 0, 0, 1 };
    generation *generations = NULL;
    size_t i, count = 0, newest = (size_t)-1, newest_invalid = (size_t)-1;
    ceml_metadata scratch;
    mpz_t value, previous;
    int foreign = 0;
    recovery->status = CEML_STORE_IO;
    recovery->valid_generations = recovery->invalid_generations = recovery->temporary_entries = recovery->foreign_entries = 0;
    recovery->pointer = CEML_POINTER_ABSENT;
    if (!ceml_fs_enumerate(directory, collect, &list) || !list.ok) { free_listing(&list); return recovery->status; }
    generations = (generation *)calloc(list.count ? list.count : 1, sizeof(generation));
    if (!generations) { free_listing(&list); return recovery->status; }
    mpz_inits(value, previous, NULL);
    ceml_metadata_init(&scratch);
    for (i = 0; i < list.count; ++i) {
        generation *g;
        if (ends_with(list.items[i].name, ".tmp")) { ++recovery->temporary_entries; continue; }
        if (strcmp(list.items[i].name, "latest") == 0 && !list.items[i].is_directory) continue;
        if (!published_name(&list.items[i])) { ++recovery->foreign_entries; continue; }
        g = &generations[count++];
        mpz_init(g->sequence);
        mpz_set_str(g->sequence, list.items[i].name + 4, 10);
        g->valid = load_generation(directory, list.items[i].name, &scratch, value);
        if (g->valid) {
            strcpy_s(g->digest, CEML_HEX, scratch.metadata_digest);
            g->has_previous = scratch.has_previous;
            strcpy_s(g->previous, CEML_HEX, scratch.previous_metadata_digest);
            if (expected && !identity_matches(&scratch, expected)) { g->foreign_identity = 1; foreign = 1; }
            ++recovery->valid_generations;
            if (newest == (size_t)-1 || mpz_cmp(g->sequence, generations[newest].sequence) > 0) newest = count - 1;
        } else {
            ++recovery->invalid_generations;
            if (newest_invalid == (size_t)-1 || mpz_cmp(g->sequence, generations[newest_invalid].sequence) > 0)
                newest_invalid = count - 1;
        }
    }
    if (foreign) recovery->status = CEML_STORE_PROVENANCE;
    else if (newest == (size_t)-1) recovery->status = recovery->invalid_generations ? CEML_STORE_INTEGRITY : CEML_STORE_EMPTY;
    else if (newest_invalid != (size_t)-1 && mpz_cmp(generations[newest_invalid].sequence, generations[newest].sequence) > 0)
        recovery->status = CEML_STORE_INTEGRITY;
    else {
        recovery->status = CEML_STORE_OK;
        /* Where the immediately previous generation is available and valid, the chain must link. */
        mpz_sub_ui(previous, generations[newest].sequence, 1);
        for (i = 0; i < count; ++i)
            if (generations[i].valid && mpz_cmp(generations[i].sequence, previous) == 0 &&
                (!generations[newest].has_previous || strcmp(generations[newest].previous, generations[i].digest) != 0))
                recovery->status = CEML_STORE_AMBIGUOUS;
    }
    if (recovery->status == CEML_STORE_OK) {
        char name[PATH_MAXIMUM], path[PATH_MAXIMUM], expected_pointer[PATH_MAXIMUM];
        char *text = decimal(generations[newest].sequence);
        ceml_buffer pointer;
        snprintf(name, sizeof(name), "gen-%s", text);
        release(text);
        /* Reload the selected generation so the caller receives its exact state. */
        if (!load_generation(directory, name, &recovery->metadata, recovery->n)) recovery->status = CEML_STORE_INTEGRITY;
        ceml_buffer_init(&pointer);
        if (join(path, directory, "latest", NULL) && ceml_fs_exists(path)) {
            snprintf(expected_pointer, sizeof(expected_pointer), "%s %s\n", name, recovery->metadata.metadata_digest);
            recovery->pointer = ceml_fs_read_all(path, &pointer, POINTER_MAXIMUM) &&
                                pointer.length == strlen(expected_pointer) &&
                                memcmp(pointer.data, expected_pointer, pointer.length) == 0
                                ? CEML_POINTER_AGREES : CEML_POINTER_IGNORED;
        }
        ceml_buffer_free(&pointer);
    }
    for (i = 0; i < count; ++i) mpz_clear(generations[i].sequence);
    free(generations);
    ceml_metadata_clear(&scratch);
    mpz_clears(value, previous, NULL);
    free_listing(&list);
    return recovery->status;
}

static int remove_tree_one_level(const char *directory, const char *name, int is_directory) {
    char path[PATH_MAXIMUM], child[PATH_MAXIMUM];
    listing inner = { NULL, 0, 0, 1 };
    size_t i;
    int ok = join(path, directory, name, NULL);
    if (!ok) return 0;
    if (!is_directory) return ceml_fs_remove_file(path);
    if (!ceml_fs_enumerate(path, collect, &inner) || !inner.ok) { free_listing(&inner); return 0; }
    for (i = 0; ok && i < inner.count; ++i)
        ok = !inner.items[i].is_directory && join(child, path, inner.items[i].name, NULL) && ceml_fs_remove_file(child);
    free_listing(&inner);
    return ok && ceml_fs_remove_directory(path);
}

typedef struct { ceml_file *file; int calls; } stream_target;

/* The interruption boundary falls after the label and length frame, before the magnitude. */
static int file_sink(const void *data, size_t length, void *context) {
    stream_target *target = (stream_target *)context;
    if (!ceml_fs_write_exact(target->file, data, length)) return 0;
    if (++target->calls == 2) ceml_fs_fault_boundary("body-partial");
    return 1;
}

static int write_with_boundary(ceml_file *file, const unsigned char *data, size_t length, const char *phase) {
    size_t half = length >> 1;
    if (!ceml_fs_write_exact(file, data, half)) return 0;
    ceml_fs_fault_boundary(phase);
    return ceml_fs_write_exact(file, data + half, length - half);
}

int ceml_store_promote(const char *directory, const ceml_identity *identity, const mpz_t n, const mpz_t shortcut_steps,
                       const mpz_t odd_steps, int streaming, ceml_store_timing *timing) {
    char generation_name[PATH_MAXIMUM], temporary_name[PATH_MAXIMUM], temporary[PATH_MAXIMUM], published[PATH_MAXIMUM];
    char body_path[PATH_MAXIMUM], metadata_path[PATH_MAXIMUM], pointer_temporary[PATH_MAXIMUM], pointer_path[PATH_MAXIMUM];
    char pointer_text[PATH_MAXIMUM], *text;
    ceml_recovery recovery;
    ceml_metadata metadata, reread;
    ceml_buffer body, json, check_body, check_json;
    ceml_file *body_file = NULL, *metadata_file = NULL, *pointer_file;
    listing list = { NULL, 0, 0, 1 };
    mpz_t check_n, retire_below, sequence;
    unsigned long long start, mark;
    size_t i;
    int ok = 0, status, directory_result;
    memset(timing, 0, sizeof(*timing));
    start = ceml_fs_ticks();
    ceml_recovery_init(&recovery); ceml_metadata_init(&metadata); ceml_metadata_init(&reread);
    ceml_buffer_init(&body); ceml_buffer_init(&json); ceml_buffer_init(&check_body); ceml_buffer_init(&check_json);
    mpz_inits(check_n, retire_below, sequence, NULL);
    status = ceml_store_recover(directory, identity, &recovery);
    if (status != CEML_STORE_OK && status != CEML_STORE_EMPTY) goto done;

    /* Remove unpublished leftovers. They were never checkpoints. */
    if (!ceml_fs_enumerate(directory, collect, &list) || !list.ok) goto done;
    for (i = 0; i < list.count; ++i)
        if (ends_with(list.items[i].name, ".tmp") &&
            !remove_tree_one_level(directory, list.items[i].name, list.items[i].is_directory)) goto done;

    strcpy_s(metadata.run_id, sizeof(metadata.run_id), identity->run_id);
    strcpy_s(metadata.manifest_digest, CEML_HEX, identity->manifest_digest);
    strcpy_s(metadata.original_start_digest, CEML_HEX, identity->original_start_digest);
    strcpy_s(metadata.protocol_commit, CEML_HEX, identity->protocol_commit);
    strcpy_s(metadata.engine_commit, CEML_HEX, identity->engine_commit);
    strcpy_s(metadata.build_digest, CEML_HEX, identity->build_digest);
    strcpy_s(metadata.machine_profile_digest, CEML_HEX, identity->machine_profile_digest);
    strcpy_s(metadata.validation_evidence_digest, CEML_HEX, identity->validation_evidence_digest);
    if (status == CEML_STORE_OK) {
        mpz_add_ui(metadata.sequence, recovery.metadata.sequence, 1);
        metadata.has_previous = 1;
        strcpy_s(metadata.previous_metadata_digest, CEML_HEX, recovery.metadata.metadata_digest);
    }
    mpz_set(metadata.shortcut_steps, shortcut_steps); mpz_set(metadata.odd_steps, odd_steps);
    mpz_add(metadata.standard_steps, shortcut_steps, odd_steps);
    metadata.terminal_reached = mpz_cmp_ui(n, 1) == 0;
    mpz_set(sequence, metadata.sequence);
    text = decimal(sequence);
    snprintf(generation_name, sizeof(generation_name), "gen-%s", text);
    snprintf(temporary_name, sizeof(temporary_name), "gen-%s.tmp", text);
    release(text);
    if (!join(temporary, directory, temporary_name, NULL) || !join(published, directory, generation_name, NULL) ||
        !join(body_path, temporary, "state.bin", NULL) || !join(metadata_path, temporary, "metadata.json", NULL) ||
        !join(pointer_temporary, directory, "latest.tmp", NULL) || !join(pointer_path, directory, "latest", NULL)) goto done;
    if (ceml_fs_exists(published) || !ceml_fs_make_directory(temporary)) goto done;

    /* Serialize and write the candidate pair. */
    body_file = ceml_fs_create_new(body_path);
    if (!body_file) goto done;
    if (streaming) {
        stream_target target = { NULL, 0 };
        target.file = body_file;
        mark = ceml_fs_ticks();
        if (!ceml_body_stream(n, file_sink, &target, &metadata) || !ceml_metadata_finish(&metadata)) goto done;
        timing->write_ticks += ceml_fs_ticks() - mark;      /* serialization is interleaved with the write */
    } else {
        mark = ceml_fs_ticks();
        if (!ceml_body_encode(n, &body) || !ceml_metadata_seal(&metadata, body.data, body.length)) goto done;
        timing->serialization_ticks += ceml_fs_ticks() - mark;
        mark = ceml_fs_ticks();
        if (!write_with_boundary(body_file, body.data, body.length, "body-partial")) goto done;
        timing->write_ticks += ceml_fs_ticks() - mark;
    }
    ceml_fs_fault_boundary("body-complete");
    mark = ceml_fs_ticks();
    if (!ceml_metadata_emit(&metadata, 1, &json)) goto done;
    timing->serialization_ticks += ceml_fs_ticks() - mark;
    mark = ceml_fs_ticks();
    metadata_file = ceml_fs_create_new(metadata_path);
    if (!metadata_file || !write_with_boundary(metadata_file, json.data, json.length, "metadata-partial")) goto done;
    timing->write_ticks += ceml_fs_ticks() - mark;
    ceml_fs_fault_boundary("metadata-complete-before-flush");

    /* Durable flush of each file, then close. */
    mark = ceml_fs_ticks();
    if (!ceml_fs_flush(body_file) || !ceml_fs_flush(metadata_file)) goto done;
    ok = ceml_fs_close(body_file); body_file = NULL;
    ok = ceml_fs_close(metadata_file) && ok; metadata_file = NULL;
    if (!ok) goto done;
    ok = 0;
    timing->flush_ticks = ceml_fs_ticks() - mark;
    mark = ceml_fs_ticks();
    directory_result = ceml_fs_durable_directory(temporary);
    if (directory_result == 0) goto done;
    timing->directory_ticks += ceml_fs_ticks() - mark;
    ceml_fs_fault_boundary("after-flush-before-verify");

    /* Reopen, re-read and fully validate before publication. */
    mark = ceml_fs_ticks();
    if (!ceml_fs_read_all(body_path, &check_body, BODY_MAXIMUM) || !ceml_fs_read_all(metadata_path, &check_json, METADATA_MAXIMUM) ||
        check_json.length != json.length || memcmp(check_json.data, json.data, json.length) != 0 ||
        !ceml_metadata_parse(check_json.data, check_json.length, &reread) ||
        !ceml_checkpoint_validate(&reread, check_body.data, check_body.length, check_n) || mpz_cmp(check_n, n) != 0 ||
        mpz_cmp(reread.shortcut_steps, shortcut_steps) != 0 || mpz_cmp(reread.odd_steps, odd_steps) != 0 ||
        mpz_cmp(reread.sequence, sequence) != 0 || !identity_matches(&reread, identity) ||
        strcmp(reread.metadata_digest, metadata.metadata_digest) != 0) goto done;
    timing->verify_ticks = ceml_fs_ticks() - mark;
    timing->body_bytes = check_body.length; timing->metadata_bytes = check_json.length;
    ceml_fs_fault_boundary("after-verify-before-promote");

    /* Atomic publication, then directory and pointer durability. */
    mark = ceml_fs_ticks();
    if (!ceml_fs_atomic_promote(temporary, published, 0)) goto done;
    timing->promotion_ticks = ceml_fs_ticks() - mark;
    ceml_fs_fault_boundary("after-promote-before-dirsync");
    mark = ceml_fs_ticks();
    directory_result = ceml_fs_durable_directory(directory);
    if (directory_result == 0) goto done;
    timing->directory_ticks += ceml_fs_ticks() - mark;
    timing->directory_flush = directory_result;
    mark = ceml_fs_ticks();
    snprintf(pointer_text, sizeof(pointer_text), "%s %s\n", generation_name, metadata.metadata_digest);
    pointer_file = ceml_fs_create_new(pointer_temporary);
    if (!pointer_file) goto done;
    ok = ceml_fs_write_exact(pointer_file, pointer_text, strlen(pointer_text)) && ceml_fs_flush(pointer_file);
    ok = ceml_fs_close(pointer_file) && ok;
    if (!ok) goto done;
    ok = 0;
    ceml_fs_fault_boundary("pointer-temp-written");
    if (!ceml_fs_atomic_promote(pointer_temporary, pointer_path, 1)) goto done;
    timing->promotion_ticks += ceml_fs_ticks() - mark;
    ceml_fs_fault_boundary("after-pointer-promote");
    mark = ceml_fs_ticks();
    if (ceml_fs_durable_directory(directory) == 0) goto done;
    timing->directory_ticks += ceml_fs_ticks() - mark;

    /* Re-read the published generation from its final name. */
    mark = ceml_fs_ticks();
    if (!load_generation(directory, generation_name, &reread, check_n) || mpz_cmp(check_n, n) != 0 ||
        strcmp(reread.metadata_digest, metadata.metadata_digest) != 0) goto done;
    timing->verify_ticks += ceml_fs_ticks() - mark;
    ceml_fs_fault_boundary("published-before-retire");

    /* Only now retire generations older than the immediately previous one. */
    mark = ceml_fs_ticks();
    if (mpz_cmp_ui(sequence, 2) >= 0) {
        mpz_sub_ui(retire_below, sequence, 1);
        for (i = 0; i < list.count; ++i) {
            char retired_name[PATH_MAXIMUM], from[PATH_MAXIMUM], to[PATH_MAXIMUM], child[PATH_MAXIMUM];
            if (!published_name(&list.items[i])) continue;
            mpz_set_str(check_n, list.items[i].name + 4, 10);
            if (mpz_cmp(check_n, retire_below) >= 0) continue;
            snprintf(retired_name, sizeof(retired_name), "%s.retired.tmp", list.items[i].name);
            if (!join(from, directory, list.items[i].name, NULL) || !join(to, directory, retired_name, NULL) ||
                !ceml_fs_atomic_promote(from, to, 0)) goto done;
            ceml_fs_fault_boundary("retire-renamed");
            if (!join(child, to, "state.bin", NULL) || !ceml_fs_remove_file(child)) goto done;
            ceml_fs_fault_boundary("retire-partial");
            if (!join(child, to, "metadata.json", NULL) || !ceml_fs_remove_file(child) || !ceml_fs_remove_directory(to)) goto done;
            ++timing->retired;
        }
        if (ceml_fs_durable_directory(directory) == 0) goto done;
    }
    timing->retire_ticks = ceml_fs_ticks() - mark;
    ceml_fs_fault_boundary("complete-before-exit");
    ok = 1;
done:
    if (body_file) ceml_fs_close(body_file);
    if (metadata_file) ceml_fs_close(metadata_file);
    timing->total_ticks = ceml_fs_ticks() - start;
    free_listing(&list);
    mpz_clears(check_n, retire_below, sequence, NULL);
    ceml_buffer_free(&body); ceml_buffer_free(&json); ceml_buffer_free(&check_body); ceml_buffer_free(&check_json);
    ceml_metadata_clear(&metadata); ceml_metadata_clear(&reread);
    ceml_recovery_clear(&recovery);
    return ok;
}
