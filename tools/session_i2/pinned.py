"""CEML-SESSION-I2 Windows read leases. No persistent verification cache."""
import ctypes
from ctypes import wintypes
from pathlib import Path
import os
import stat


class IntegrityError(Exception):
    pass


class ReadLeases:
    """Deny writes/deletes to files and deletes/renames to their ancestor directories."""
    def __init__(self, root):
        if os.name != 'nt':
            raise IntegrityError('I2 read leases require Windows; no unsafe fallback')
        self.root = Path(root).absolute()
        self.handles = {}
        self.kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self.kernel.CreateFileW.argtypes = (wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                           ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE)
        self.kernel.CreateFileW.restype = wintypes.HANDLE
        self.kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
        self.kernel.CloseHandle.restype = wintypes.BOOL

    def _open(self, path, directory):
        path = Path(path).absolute()
        if '..' in path.parts:
            raise IntegrityError('Parent traversal lease refused')
        if path in self.handles:
            return
        if not path.is_relative_to(self.root):
            raise IntegrityError('Lease path outside workspace')
        info = path.lstat()
        if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise IntegrityError('Reparse-point lease refused')
        access = 0x80000000  # GENERIC_READ
        sharing = 3 if directory else 1  # directories allow writes, never deletion; files read only
        flags = (0x02000000 if directory else 0x80) | 0x00200000  # never follow final reparse point
        handle = self.kernel.CreateFileW(str(path), access, sharing, None, 3, flags, None)
        if handle == ctypes.c_void_p(-1).value:
            raise IntegrityError('Cannot establish exclusive read lease')
        self.handles[path] = handle
        # The handle now prevents replacement, closing the lstat/open race.
        info = path.lstat()
        if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise IntegrityError('Reparse-point lease refused')
        if stat.S_ISDIR(info.st_mode) != directory:
            raise IntegrityError('Lease object type mismatch')

    def pin(self, path):
        path = Path(path).absolute()
        if not path.is_relative_to(self.root):
            raise IntegrityError('Lease path outside workspace')
        # Walk literal ancestors, never resolve/follow a junction or symlink.
        current = self.root
        self._open(current, True)
        for part in path.relative_to(self.root).parts[:-1]:
            current = current / part
            self._open(current, True)
        self._open(path, False)
        if path.stat().st_size > 8*1024*1024:
            raise IntegrityError('Oversized lease input')
        return path.read_bytes()

    def close(self):
        for handle in reversed(list(self.handles.values())):
            self.kernel.CloseHandle(handle)
        self.handles.clear()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
