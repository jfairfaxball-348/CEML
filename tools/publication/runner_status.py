"""Read-only operator liveness independent of elevated command-line visibility.

Restart Manager ONLY lists file users. No shutdown, restart or signalling API.
Private control tokens, PIDs and process creation times never enter the feed.
"""
import ctypes
from ctypes import wintypes as w
from datetime import datetime
import errno
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / 'local/frontier/operator-session.json'
LOCK = ROOT / 'local/frontier/operator.lock'


class UnknownLiveness(ValueError):
    def __init__(self, source=None):
        super().__init__('Cannot confirm operator liveness')
        self.source = source


def read_control(path, now):
    try:
        with path.open('rb') as handle:
            raw = handle.read(131073)
    except FileNotFoundError:
        return None
    if len(raw) > 131072:
        raise ValueError('Oversized operator control')
    value = json.loads(raw)
    if not isinstance(value, dict) or type(value.get('active')) is not bool or not re.fullmatch('[0-9a-f]{32}', str(value.get('token', ''))):
        raise ValueError('Invalid operator control')
    mode, requested = value.get('mode'), value.get('requested')
    if mode not in ('finite', 'continuous') or (mode == 'continuous' and requested is not None) or (mode == 'finite' and not re.fullmatch('[1-9][0-9]{0,19}', str(requested))):
        raise ValueError('Invalid operator session request')
    started = datetime.fromisoformat(value['started_at'])
    if started.tzinfo is None or started.timestamp() > now + 5:
        raise ValueError('Invalid operator session time')
    if 'initial_end' in value and not re.fullmatch('[1-9][0-9]{0,8191}', str(value['initial_end'])):
        raise ValueError('Invalid operator session anchor')
    return value


def lock_busy(path):
    """Nonblocking probe: never waits for, writes or releases the owner's lock."""
    import msvcrt
    try:
        handle = path.open('r+b')
    except FileNotFoundError:
        return False
    with handle:
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            if error.errno in (errno.EACCES, errno.EDEADLK):
                return True
            raise
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        return False


class Process(ctypes.Structure):
    _fields_ = [('pid', w.DWORD), ('started', w.FILETIME)]


class ProcessInfo(ctypes.Structure):
    _fields_ = [('process', Process), ('app', w.WCHAR * 256), ('service', w.WCHAR * 64),
                ('type', w.DWORD), ('status', w.ULONG), ('session', w.DWORD), ('restartable', w.BOOL)]


def ticks(value):
    return (value.dwHighDateTime << 32) | value.dwLowDateTime


def lock_users(path):
    if os.name != 'nt':
        raise UnknownLiveness()
    library = ctypes.WinDLL('rstrtmgr', use_last_error=True)
    library.RmStartSession.argtypes = (ctypes.POINTER(w.DWORD), w.DWORD, w.LPWSTR)
    library.RmRegisterResources.argtypes = (w.DWORD, w.UINT, ctypes.POINTER(w.LPCWSTR), w.UINT, ctypes.POINTER(Process), w.UINT, ctypes.POINTER(w.LPCWSTR))
    library.RmGetList.argtypes = (w.DWORD, ctypes.POINTER(w.UINT), ctypes.POINTER(w.UINT), ctypes.POINTER(ProcessInfo), ctypes.POINTER(w.DWORD))
    library.RmEndSession.argtypes = (w.DWORD,)
    for name in ('RmStartSession', 'RmRegisterResources', 'RmGetList', 'RmEndSession'):
        getattr(library, name).restype = w.DWORD
    session, key = w.DWORD(), ctypes.create_unicode_buffer(33)
    if library.RmStartSession(ctypes.byref(session), 0, key):
        raise UnknownLiveness()
    try:
        paths = (w.LPCWSTR * 1)(str(path.absolute()))
        if library.RmRegisterResources(session, 1, paths, 0, None, 0, None):
            raise UnknownLiveness()
        for capacity in (32, 128):
            count, needed, reason = w.UINT(capacity), w.UINT(), w.DWORD()
            items = (ProcessInfo * capacity)()
            result = library.RmGetList(session, ctypes.byref(needed), ctypes.byref(count), items, ctypes.byref(reason))
            if result == 0:
                return [{'pid': item.process.pid, 'ticks': ticks(item.process.started)}
                        for item in items[:count.value] if item.process.pid != os.getpid()]
            if result != 234 or needed.value > 128:
                raise UnknownLiveness()
        raise UnknownLiveness()
    finally:
        library.RmEndSession(session)


def same_lock_user(owner, path):
    """Re-list the exact PID/birth pair; no privileged process handle is needed."""
    return owner in lock_users(path) and lock_busy(path)


def identity(control):
    return tuple(control.get(key) for key in ('token', 'active', 'started_at', 'mode', 'requested', 'initial_end'))


def source(control):
    return dict(mode=control['mode'], requested=int(control['requested']) if control['requested'] is not None else None,
                started_at=control['started_at'], started=datetime.fromisoformat(control['started_at']).timestamp(),
                **({'initial_end': control['initial_end']} if 'initial_end' in control else {}),
                stale_active=control['active'])


def detect(now, control_path=CONTROL, lock_path=LOCK):
    """No source means no managed session; uncertainty must never become idle."""
    last_source = None
    try:
        for _ in range(2):
            control = read_control(control_path, now)
            if control is None:
                if lock_busy(lock_path):
                    raise UnknownLiveness()
                return None, None
            last_source = source(control)
            running = False
            if control['active'] and lock_busy(lock_path):
                owners = lock_users(lock_path)
                started = last_source['started']
                matches = [owner for owner in owners
                           if 0 <= started - (owner['ticks'] / 1e7 - 11644473600) <= 30]
                if len(matches) > 1 or not owners or any(started - (o['ticks'] / 1e7 - 11644473600) > 30 for o in owners):
                    raise UnknownLiveness(last_source)
                running = bool(matches) and same_lock_user(matches[0], lock_path)
            after = read_control(control_path, now)
            if after is not None and identity(control) == identity(after):
                return last_source if running else None, last_source
        raise UnknownLiveness(last_source)
    except (OSError, ValueError, KeyError) as error:
        raise UnknownLiveness(last_source) from error
