/* Windows FilesystemAdapter. Primitives:
 *   write    CreateFileW(CREATE_NEW, no sharing) + WriteFile, exact length;
 *   flush    FlushFileBuffers on the file handle;
 *   promote  MoveFileExW(MOVEFILE_WRITE_THROUGH [| MOVEFILE_REPLACE_EXISTING]),
 *            source and target in one directory on one volume;
 *   dirsync  FlushFileBuffers on a directory handle opened with
 *            FILE_FLAG_BACKUP_SEMANTICS; reported unsupported if refused.
 * No power-loss behaviour is asserted by this code. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdlib.h>
#include <string.h>

#include "ceml_fs.h"

struct ceml_file { HANDLE handle; };

static char fault_phase[64];

static wchar_t *widen(const char *path) {
    int length = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, NULL, 0);
    wchar_t *wide;
    if (length <= 0) return NULL;
    wide = (wchar_t *)malloc(sizeof(wchar_t) * (size_t)length);
    if (wide && MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, wide, length) != length) { free(wide); wide = NULL; }
    return wide;
}

ceml_file *ceml_fs_create_new(const char *path) {
    wchar_t *wide = widen(path);
    ceml_file *file;
    HANDLE handle;
    if (!wide) return NULL;
    handle = CreateFileW(wide, GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
    free(wide);
    if (handle == INVALID_HANDLE_VALUE) return NULL;
    file = (ceml_file *)malloc(sizeof(*file));
    if (!file) { CloseHandle(handle); return NULL; }
    file->handle = handle;
    return file;
}

int ceml_fs_write_exact(ceml_file *file, const void *data, size_t length) {
    const unsigned char *bytes = (const unsigned char *)data;
    while (length) {
        DWORD chunk = length > 0x40000000u ? 0x40000000u : (DWORD)length, written = 0;
        if (!WriteFile(file->handle, bytes, chunk, &written, NULL) || written == 0) return 0;
        bytes += written; length -= written;
    }
    return 1;
}

int ceml_fs_flush(ceml_file *file) { return FlushFileBuffers(file->handle) != 0; }

int ceml_fs_close(ceml_file *file) {
    int ok = CloseHandle(file->handle) != 0;
    free(file);
    return ok;
}

int ceml_fs_read_all(const char *path, ceml_buffer *out, size_t maximum) {
    wchar_t *wide = widen(path);
    HANDLE handle;
    LARGE_INTEGER size;
    int ok = 0;
    out->length = 0;
    if (!wide) return 0;
    handle = CreateFileW(wide, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    free(wide);
    if (handle == INVALID_HANDLE_VALUE) return 0;
    if (GetFileSizeEx(handle, &size) && size.QuadPart >= 0 && (unsigned long long)size.QuadPart <= maximum) {
        size_t remaining = (size_t)size.QuadPart;
        unsigned char chunk[65536];
        ok = 1;
        while (ok && remaining) {
            DWORD want = remaining > sizeof(chunk) ? (DWORD)sizeof(chunk) : (DWORD)remaining, got = 0;
            ok = ReadFile(handle, chunk, want, &got, NULL) && got == want && ceml_buffer_append(out, chunk, got);
            remaining -= got;
        }
        if (ok) { DWORD got = 0; unsigned char extra; ok = ReadFile(handle, &extra, 1, &got, NULL) && got == 0; }
    }
    CloseHandle(handle);
    return ok;
}

int ceml_fs_make_directory(const char *path) {
    wchar_t *wide = widen(path);
    int ok = wide && CreateDirectoryW(wide, NULL) != 0;
    free(wide);
    return ok;
}

int ceml_fs_atomic_promote(const char *from, const char *to, int replace) {
    wchar_t *source = widen(from), *target = widen(to);
    int ok = source && target &&
             MoveFileExW(source, target, MOVEFILE_WRITE_THROUGH | (replace ? MOVEFILE_REPLACE_EXISTING : 0)) != 0;
    free(source); free(target);
    return ok;
}

int ceml_fs_durable_directory(const char *path) {
    wchar_t *wide = widen(path);
    HANDLE handle;
    int result;
    if (!wide) return 0;
    handle = CreateFileW(wide, GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE, NULL,
                         OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, NULL);
    free(wide);
    if (handle == INVALID_HANDLE_VALUE) return -1;
    result = FlushFileBuffers(handle) ? 1 : -1;
    CloseHandle(handle);
    return result;
}

int ceml_fs_remove_file(const char *path) {
    wchar_t *wide = widen(path);
    int ok = wide && DeleteFileW(wide) != 0;
    free(wide);
    return ok;
}

int ceml_fs_remove_directory(const char *path) {
    wchar_t *wide = widen(path);
    int ok = wide && RemoveDirectoryW(wide) != 0;
    free(wide);
    return ok;
}

int ceml_fs_exists(const char *path) {
    wchar_t *wide = widen(path);
    DWORD attributes = wide ? GetFileAttributesW(wide) : INVALID_FILE_ATTRIBUTES;
    free(wide);
    return attributes != INVALID_FILE_ATTRIBUTES;
}

int ceml_fs_enumerate(const char *directory, int (*visit)(const char *, int, void *), void *context) {
    char pattern[1024], name[1024];
    wchar_t *wide;
    WIN32_FIND_DATAW entry;
    HANDLE find;
    int ok = 1;
    if (strlen(directory) + 3 > sizeof(pattern)) return 0;
    strcpy_s(pattern, sizeof(pattern), directory); strcat_s(pattern, sizeof(pattern), "\\*");
    wide = widen(pattern);
    if (!wide) return 0;
    find = FindFirstFileW(wide, &entry);
    free(wide);
    if (find == INVALID_HANDLE_VALUE) return 0;
    do {
        if (wcscmp(entry.cFileName, L".") == 0 || wcscmp(entry.cFileName, L"..") == 0) continue;
        if (WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, entry.cFileName, -1, name, sizeof(name), NULL, NULL) <= 0) { ok = 0; break; }
        ok = visit(name, (entry.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) != 0, context);
    } while (ok && FindNextFileW(find, &entry));
    if (ok && GetLastError() != ERROR_NO_MORE_FILES) ok = 0;
    FindClose(find);
    return ok;
}

void ceml_fs_describe(const char *directory, ceml_fs_capability *capability) {
    capability->adapter = "win32-ntfs-generation-directory-v1";
    capability->write_primitive = "CreateFileW CREATE_NEW exclusive + WriteFile exact length";
    capability->file_flush_primitive = "FlushFileBuffers on the file handle";
    capability->atomic_promote_primitive = "MoveFileExW MOVEFILE_WRITE_THROUGH same-directory rename";
    capability->directory_durability_primitive = "FlushFileBuffers on a FILE_FLAG_BACKUP_SEMANTICS directory handle";
    capability->directory_flush_supported = ceml_fs_durable_directory(directory) == 1;
}

void ceml_fs_set_fault(const char *phase) {
    fault_phase[0] = 0;
    if (phase && strlen(phase) < sizeof(fault_phase)) strcpy_s(fault_phase, sizeof(fault_phase), phase);
}

void ceml_fs_fault_boundary(const char *phase) {
    if (fault_phase[0] && strcmp(fault_phase, phase) == 0) TerminateProcess(GetCurrentProcess(), 99);
}

unsigned long long ceml_fs_ticks(void) {
    LARGE_INTEGER value;
    QueryPerformanceCounter(&value);
    return (unsigned long long)value.QuadPart;
}

unsigned long long ceml_fs_ticks_per_second(void) {
    LARGE_INTEGER value;
    QueryPerformanceFrequency(&value);
    return (unsigned long long)value.QuadPart;
}
