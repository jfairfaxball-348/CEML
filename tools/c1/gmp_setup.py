"""Stage: hardware characterization; explicit acquisition and offline C17 probe.

No global installation, scientific arithmetic or production stack selection.
Only acquire uses the network. Raw tool diagnostics and locators stay in memory.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import io
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import subprocess
import sys
import tarfile
import tomllib
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / 'local/c1/gmp-setup'
CACHE = ROOT / 'local/c1/cache/sha256'
PIN = ROOT / 'config/c1_gmp_pin.toml'
BINARY_NAME = 'mingw-w64-ucrt-x86_64-gmp-6.3.0-2-any.pkg.tar.zst'
BINARY_SHA256 = 'e82a75968a556484a50084578238a84eb60fb93e34986fd6695c537975bd39ea'
SOURCE_NAME = 'mingw-w64-gmp-6.3.0-2.src.tar.zst'
BINARY_URL = 'https://mirror.msys2.org/mingw/ucrt64/' + BINARY_NAME
SOURCE_URL = 'https://mirror.msys2.org/mingw/sources/' + SOURCE_NAME
DOWNLOAD_LIMIT = 32 * 1024 * 1024
EXTRACT_LIMIT = 128 * 1024 * 1024
FLAGS = ['-nologo', '-std:c17', '-W4', '-WX', '-O2', '-MD', '-D_CRT_SECURE_NO_WARNINGS', '-Brepro', '-external:I.', '-external:W0']


class Refusal(Exception):
    """Fixed safe message only; never include external tool output."""


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def hashes(data):
    return {'sha256': hashlib.sha256(data).hexdigest(),
            'sha3_256': hashlib.sha3_256(data).hexdigest(), 'bytes': str(len(data))}


def save(name, value):
    LOCAL.mkdir(parents=True, exist_ok=True)
    (LOCAL / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def require_authorization():
    status = (ROOT / 'PROGRAM_STATUS.md').read_text(encoding='utf-8')
    if '**Authoritative current phase:** C1' not in status or '**Scientific execution authorization:** DENIED' not in status:
        raise Refusal('C1 authorization is not established')
    if not (ROOT / 'docs/C1_DEPENDENCY_SETUP.md').exists():
        raise Refusal('Dependency setup scope must be recorded first')


def storage_preflight():
    if shutil.disk_usage(ROOT).free < 16 * 1024**3:
        raise Refusal('Setup storage reserve unavailable')
    if os.name != 'nt':
        raise Refusal('This candidate requires Windows')
    import ctypes
    class Memory(ctypes.Structure):
        _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in
                    ('total_physical', 'available_physical', 'total_page', 'available_page', 'total_virtual', 'available_virtual', 'extended')]
    m = Memory()
    m.length = ctypes.sizeof(m)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)) or m.available_physical < 4 * 1024**3:
        raise Refusal('Setup memory reserve unavailable')


def fetch(url, expected=None):
    data = bytearray()
    with urllib.request.urlopen(url, timeout=30) as response:
        while True:
            part = response.read(65536)
            if not part:
                break
            data.extend(part)
            if len(data) > DOWNLOAD_LIMIT:
                raise Refusal('Archive exceeds download bound')
    data = bytes(data)
    meta = hashes(data)
    if expected and meta['sha256'] != expected:
        raise Refusal('Archive does not match published pin')
    folder = CACHE / meta['sha256']
    folder.mkdir(parents=True, exist_ok=True)
    name = url.rsplit('/', 1)[-1]
    (folder / name).write_bytes(data)
    return dict(name=name, url=url, **meta)


def unpack_zstd(data):
    import zstandard
    reader = zstandard.ZstdDecompressor().stream_reader(io.BytesIO(data))
    with reader:
        result = reader.read(EXTRACT_LIMIT + 1)
        if len(result) > EXTRACT_LIMIT:
            raise Refusal('Decompressed archive exceeds bound')
        return result


def inspect_tar(data):
    """Read bounded regular members; never extract links or metadata paths."""
    selected = {}
    total = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:') as archive:
        for entry in archive:
            path = PurePosixPath(entry.name)
            if (path.is_absolute() or '..' in path.parts or '\\' in entry.name
                    or ':' in entry.name or any(ord(c) < 32 for c in entry.name)):
                raise Refusal('Unsafe archive member')
            if entry.isdir():
                continue
            if not entry.isfile() or entry.name in selected or entry.size < 0:
                raise Refusal('Unsupported archive member')
            total += entry.size
            if total > EXTRACT_LIMIT:
                raise Refusal('Extracted archive exceeds bound')
            handle = archive.extractfile(entry)
            if handle is None:
                raise Refusal('Archive member unavailable')
            selected[entry.name] = handle.read(entry.size + 1)
            if len(selected[entry.name]) != entry.size:
                raise Refusal('Archive member length mismatch')
    return selected


def acquire():
    storage_preflight()
    binary = fetch(BINARY_URL, BINARY_SHA256)
    source = fetch(SOURCE_URL)
    for item in (binary, source):
        inspect_tar(unpack_zstd((CACHE / item['sha256'] / item['name']).read_bytes()))
    result = dict(stage='hardware characterization', observed_at=now(),
                  binary=binary, source=source, source_authentication='Official HTTPS channel; no independent signature verification claimed')
    save('acquisition.json', result)
    return result


def load_package():
    path = CACHE / BINARY_SHA256 / BINARY_NAME
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != BINARY_SHA256:
        raise Refusal('Cached binary pin mismatch')
    return inspect_tar(unpack_zstd(data))


def pe_info(data):
    """Minimal bounds-checked PE32+ import/export inspection, not GMP internals."""
    def read(fmt, offset):
        size = struct.calcsize(fmt)
        if offset < 0 or offset + size > len(data):
            raise Refusal('Malformed PE extent')
        return struct.unpack_from(fmt, data, offset)
    if data[:2] != b'MZ':
        raise Refusal('PE header absent')
    pe, = read('<I', 60)
    if data[pe:pe+4] != b'PE\0\0':
        raise Refusal('PE signature absent')
    machine, nsections = read('<HH', pe+4)
    optional_size, = read('<H', pe+20)
    optional = pe+24
    magic, = read('<H', optional)
    if machine != 0x8664 or magic != 0x20b or nsections > 96 or optional_size < 128:
        raise Refusal('Unexpected PE target')
    sections = []
    for i in range(nsections):
        off = optional + optional_size + 40*i
        virtual_size, address, raw_size, raw = read('<IIII', off+8)
        flags, = read('<I', off+36)
        sections.append((address, max(virtual_size, raw_size), raw, raw_size, flags))
    def locate(rva):
        for address, extent, raw, raw_size, flags in sections:
            if address <= rva < address + extent and rva-address < raw_size:
                return raw+rva-address, flags
        raise Refusal('Unmapped PE data')
    def string(rva):
        off, _ = locate(rva)
        end = data.find(b'\0', off, min(len(data), off+512))
        if end < 0:
            raise Refusal('Unterminated PE name')
        value = data[off:end].decode('ascii')
        if not re.fullmatch(r'[A-Za-z0-9_.?-]+', value):
            raise Refusal('Unexpected PE name')
        return value
    export_rva, export_size, import_rva, _ = read('<IIII', optional+112)
    imports = []
    if import_rva:
        offset, _ = locate(import_rva)
        for i in range(256):
            desc = read('<IIIII', offset+20*i)
            if not any(desc):
                break
            imports.append(string(desc[3]))
        else:
            raise Refusal('Too many PE imports')
    exports = {}
    if export_rva:
        offset, _ = locate(export_rva)
        nfunc, nnames, funcs, names, ordinals = read('<IIIII', offset+20)
        if nnames > 10000 or nfunc > 10000:
            raise Refusal('Too many PE exports')
        foff, _ = locate(funcs)
        noff, _ = locate(names)
        ooff, _ = locate(ordinals)
        for i in range(nnames):
            nrva, = read('<I', noff+4*i)
            ordinal, = read('<H', ooff+2*i)
            if ordinal >= nfunc:
                raise Refusal('Bad PE export ordinal')
            frva, = read('<I', foff+4*ordinal)
            if export_rva <= frva < export_rva + export_size:
                raise Refusal('Forwarded PE export unsupported')
            matching = [s for s in sections if s[0] <= frva < s[0] + s[1]]
            if len(matching) != 1:
                raise Refusal('Unmapped PE export')
            flags = matching[0][4]  # BSS exports have no initialized raw bytes.
            exports[string(nrva)] = 'function' if flags & 0x20000000 else 'data'
    return dict(machine='x86_64', format='PE32+', imports=sorted(imports), exports=exports)


def invoke(args, env=None, cwd=None, timeout=60):
    # Capture external diagnostics only in memory. Never emit raw errors or paths.
    p = subprocess.run(args, env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    if p.returncode:
        # Local debugger may examine p.stdout in memory. Persistent output stays minimized.
        raise Refusal('Tool command failed; raw diagnostic suppressed')
    if len(p.stdout) > 1024*1024:
        raise Refusal('Tool output exceeds bound')
    return p.stdout


def msvc_environment():
    locator = Path(os.environ.get('ProgramFiles(x86)', '')) / 'Microsoft Visual Studio/Installer/vswhere.exe'
    base = invoke([str(locator), '-latest', '-products', '*', '-requires',
                   'Microsoft.VisualStudio.Component.VC.Tools.x86.x64', '-property', 'installationPath']).decode('utf-8-sig').strip()
    root = Path(base)
    script = root / 'VC/Auxiliary/Build/vcvars64.bat'
    if not root.is_absolute() or not script.is_file() or any(c in str(script) for c in ('"', '\n', '\r', '%', '!', '&', '|', '<', '>', '^')):
        raise Refusal('Unsupported compiler locator')
    command = 'call "' + str(script) + '" >nul && set'
    switch = chr(47)
    command_processor = os.environ.get('COMSPEC', 'cmd.exe')
    if any(c in command_processor for c in ('"', '\n', '\r', '%', '!', '&', '|', '<', '>', '^')):
        raise Refusal('Unsupported command processor locator')
    # cmd has its own quoting grammar; list2cmdline would backslash-escape its quotes.
    command_line = '"' + command_processor + '" ' + ' '.join(switch+x for x in ('d', 's', 'c')) + ' "' + command + '"'
    initial_env = dict(os.environ)
    for key in ('CL', '_CL_', 'LINK', '_LINK_', 'INCLUDE', 'LIB', 'LIBPATH'):
        initial_env.pop(key, None)
    output = invoke(command_line, env=initial_env)
    env = initial_env.copy()
    for line in output.decode('mbcs').splitlines():
        if '=' in line and not line.startswith('='):
            key, value = line.split('=', 1)
            env[key.upper()] = value
    compiler_version = (root / 'VC/Auxiliary/Build/Microsoft.VCToolsVersion.default.txt').read_text().strip()
    sdk_version = env.get('WINDOWSSDKVERSION', '').strip('\\/')
    if not re.fullmatch(r'\d+(?:\.\d+){2,3}', compiler_version) or not re.fullmatch(r'\d+(?:\.\d+){2,3}', sdk_version):
        raise Refusal('Toolchain version unavailable')
    bindir = root / 'VC/Tools/MSVC' / compiler_version / 'bin/Hostx64/x64'
    tool_hashes = {name: hashes((bindir / name).read_bytes()) for name in ('cl.exe', 'link.exe', 'lib.exe', 'c1.dll', 'c2.dll')}
    return env, bindir, dict(msvc_tools_version=compiler_version, windows_sdk_version=sdk_version,
                            target='x86_64-pc-windows-msvc', abi='LLP64', linkage='dynamic-GMP-and-UCRT',
                            tool_bytes=tool_hashes)


def build(enforce_pin):
    storage_preflight()
    package = load_package()
    header = package['ucrt64/include/gmp.h']
    dll = package['ucrt64/bin/libgmp-10.dll']
    info = pe_info(dll)
    # The import library exposes only the public mpz namespace and public data.
    exports = {k: v for k, v in info['exports'].items()
               if k.startswith('__gmpz_') or k in ('__gmp_version', '__gmp_bits_per_limb')}
    if exports.get('__gmp_version') != 'data' or exports.get('__gmpz_mul') != 'function':
        raise Refusal('Expected public GMP exports unavailable')
    env, bindir, toolchain = msvc_environment()
    source = (ROOT / 'tools/c1/gmp_smoke.c').read_bytes()
    pin = None
    if enforce_pin:
        pin = tomllib.loads(PIN.read_text(encoding='utf-8'))
        if (pin['binary_sha256'] != BINARY_SHA256 or pin['dll_sha3_256'] != hashes(dll)['sha3_256']
                or pin['header_sha3_256'] != hashes(header)['sha3_256']
                or pin['msvc_tools_version'] != toolchain['msvc_tools_version']
                or pin['windows_sdk_version'] != toolchain['windows_sdk_version']):
            raise Refusal('Offline build pin mismatch')
        if pin['smoke_source_sha3_256'] != hashes(source)['sha3_256'] or pin['compiler_flags'] != FLAGS:
            raise Refusal('Offline source or flag mismatch')
        if pin['python_version'] != '.'.join(str(x) for x in sys.version_info[:3]) or pin['zstandard_version'] != importlib.metadata.version('zstandard'):
            raise Refusal('Offline extraction tool version mismatch')
        source_archive = CACHE / pin['source_sha256'] / SOURCE_NAME
        if hashes(source_archive.read_bytes())['sha256'] != pin['source_sha256']:
            raise Refusal('Retained source archive pin mismatch')
        for name, meta in toolchain['tool_bytes'].items():
            if pin['tool_sha3_256'][name] != meta['sha3_256']:
                raise Refusal('Offline compiler content mismatch')
    folder = LOCAL / ('offline' if enforce_pin else 'probe')
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'gmp.h').write_bytes(header)
    (folder / 'libgmp-10.dll').write_bytes(dll)
    definition = 'LIBRARY libgmp-10.dll\nEXPORTS\n' + ''.join(
        name + (' DATA' if kind == 'data' else '') + '\n' for name, kind in sorted(exports.items()))
    (folder / 'gmp.def').write_text(definition, encoding='ascii')
    invoke([str(bindir/'lib.exe'), '-nologo', '-machine:x64', '-def:gmp.def', '-out:gmp.lib'], env, folder)
    # Source is copied to a fixed relative build name; debug paths are not emitted.
    (folder/'gmp_smoke.c').write_bytes(source)
    invoke([str(bindir/'cl.exe'), *FLAGS, '-I.', 'gmp_smoke.c', 'gmp.lib', '-Fe:gmp_smoke.exe',
            '-Fo:gmp_smoke.obj', '-link', '-Brepro'], env, folder)
    executable = (folder/'gmp_smoke.exe').read_bytes()
    exeinfo = pe_info(executable)
    if 'libgmp-10.dll' not in exeinfo['imports']:
        raise Refusal('Executable does not import intended GMP DLL')
    result = dict(stage='hardware characterization', observed_at=now(), offline=enforce_pin,
                  package_sha256=BINARY_SHA256, header=hashes(header), dll=hashes(dll),
                  definition=hashes(definition.encode('ascii')), import_library=hashes((folder/'gmp.lib').read_bytes()),
                  source=hashes(source), executable=hashes(executable), compiler_flags=FLAGS,
                  linker_flags=['-Brepro'], toolchain=toolchain, dll_imports=info['imports'],
                  executable_imports=exeinfo['imports'], public_export_count=str(len(exports)))
    if enforce_pin and result['executable']['sha3_256'] != pin['smoke_executable_sha3_256']:
        raise Refusal('Offline executable differs from pinned capability build')
    save('offline_build.json' if enforce_pin else 'probe_build.json', result)
    return result


def smoke(offline=False):
    storage_preflight()
    folder = LOCAL / ('offline' if offline else 'probe')
    record = json.loads((LOCAL / ('offline_build.json' if offline else 'probe_build.json')).read_text())
    for name, key in (('libgmp-10.dll', 'dll'), ('gmp_smoke.exe', 'executable')):
        if hashes((folder/name).read_bytes()) != record[key]:
            raise Refusal('Smoke binary bytes changed after build')
    raw = invoke([str(folder/'gmp_smoke.exe')], cwd=folder, timeout=5)
    result = json.loads(raw)
    expected = 123456789012345678901234567890 * 98765432109876543210987654321
    if (not result.get('ok') or result['product_decimal'] != str(expected)
            or result['runtime_version'] != '6.3.0' or not result['roundtrip_equal'] or not result['dll_beside_executable']):
        raise Refusal('Small capability correctness disagreement')
    evidence = dict(stage='hardware characterization', observed_at=now(), offline=offline,
                    executable_sha3_256=record['executable']['sha3_256'], result=result,
                    reference='Independent Python integer product of two fixed decimal operands; no transition')
    save('offline_smoke.json' if offline else 'probe_smoke.json', evidence)
    return evidence


def calibration_build():
    # Pin verification and offline capability rebuild precede this new harness.
    evidence = build(True)
    env, bindir, toolchain = msvc_environment()
    folder = LOCAL / 'calibration'
    folder.mkdir(parents=True, exist_ok=True)
    for filename in ('gmp.h', 'gmp.lib', 'libgmp-10.dll'):
        (folder / filename).write_bytes((LOCAL / 'offline' / filename).read_bytes())
    artifacts = {}
    for base, libraries in (('cal_candidate', ['gmp.lib']),
                            ('cal_guard', ['pdh.lib', 'powrprof.lib', 'psapi.lib', 'uuid.lib'])):
        source = (ROOT/'tools/c1'/(base+'.c')).read_bytes()
        (folder/(base+'.c')).write_bytes(source)
        invoke([str(bindir/'cl.exe'), *FLAGS, '-I.', base+'.c', *libraries,
                '-Fe:'+base+'.exe', '-Fo:'+base+'.obj', '-link', '-Brepro'], env, folder)
        artifacts[base] = dict(source=hashes(source), executable=hashes((folder/(base+'.exe')).read_bytes()))
    result = dict(stage='hardware characterization', observed_at=now(), offline=True,
                  compiler_flags=FLAGS, toolchain=toolchain, artifacts=artifacts,
                  dependency=evidence['dll'], pin=hashes(PIN.read_bytes()))
    save('calibration_build.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('acquire', 'probe-build', 'build', 'smoke', 'offline-smoke', 'calibration-build'))
    args = parser.parse_args()
    require_authorization()
    if args.command == 'acquire':
        result = acquire()
    elif args.command == 'calibration-build':
        result = calibration_build()
    elif args.command in ('build', 'probe-build'):
        result = build(args.command == 'build')
    else:
        result = smoke(args.command == 'offline-smoke')
    print(json.dumps({'status': 'ok', 'command': args.command, 'observed_at': result['observed_at']}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        message = str(error) if isinstance(error, Refusal) else 'Setup refused; raw diagnostic suppressed'
        print(json.dumps({'status': 'refused', 'reason': message}))
        sys.exit(1)
