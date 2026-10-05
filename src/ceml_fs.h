/* FilesystemAdapter: the only path by which checkpoint bytes reach storage.
 * Each operation maps to one documented platform primitive so that C1 can
 * test the actual target filesystem. Paths are UTF-8, relative or absolute. */
#ifndef CEML_FS_H
#define CEML_FS_H

#include <stddef.h>
#include "ceml_codec.h"

typedef struct ceml_file ceml_file;

typedef struct {
    const char *adapter;                 /* stable adapter identifier */
    const char *write_primitive;
    const char *file_flush_primitive;
    const char *atomic_promote_primitive;
    const char *directory_durability_primitive;
    int directory_flush_supported;       /* observed at run time on the target */
} ceml_fs_capability;

ceml_file *ceml_fs_create_new(const char *path);              /* fails if the file exists */
int ceml_fs_write_exact(ceml_file *file, const void *data, size_t length);
int ceml_fs_flush(ceml_file *file);                           /* file data and metadata */
int ceml_fs_close(ceml_file *file);
int ceml_fs_read_all(const char *path, ceml_buffer *out, size_t maximum);   /* fresh handle, exact bytes */
int ceml_fs_make_directory(const char *path);
int ceml_fs_atomic_promote(const char *from, const char *to, int replace);  /* same-directory rename */
int ceml_fs_durable_directory(const char *path);              /* 1 done, 0 failed, -1 unsupported */
int ceml_fs_remove_file(const char *path);
int ceml_fs_remove_directory(const char *path);
int ceml_fs_exists(const char *path);
/* Calls visit(name, is_directory, context) for every entry; returns 0 on failure. */
int ceml_fs_enumerate(const char *directory, int (*visit)(const char *, int, void *), void *context);
void ceml_fs_describe(const char *directory, ceml_fs_capability *capability);

/* Fault-injection boundary: when the configured phase name is reached the
 * process is terminated at once, with no flush, unwind or cleanup. */
void ceml_fs_set_fault(const char *phase);
void ceml_fs_fault_boundary(const char *phase);

unsigned long long ceml_fs_ticks(void);
unsigned long long ceml_fs_ticks_per_second(void);

#endif
