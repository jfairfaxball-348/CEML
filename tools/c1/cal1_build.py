"""Stage: hardware characterization; offline build of the bounded CEML-CAL-1 harness.

Verifies the committed GMP pin by rebuilding the pinned capability probe, then
compiles the native case and guard programs with exact recorded flags. No
network access exists on this path. This is not a production build manifest.
"""
from __future__ import annotations

import json
import sys

from gmp_setup import FLAGS, LOCAL, PIN, ROOT, Refusal, build, hashes, invoke, msvc_environment, now, pe_info, require_authorization

CAL1 = ROOT / 'local/c1/cal1'
CHECKED = ['-nologo', '-std:c17', '-W4', '-WX', '-Od', '-RTC1', '-MD', '-D_CRT_SECURE_NO_WARNINGS', '-DCEML_CHECKED',
           '-Brepro', '-external:I.', '-external:W0']
GUARD_LIBRARIES = ['pdh.lib', 'powrprof.lib', 'psapi.lib', 'uuid.lib']
PROGRAMS = (('cal1_case.exe', 'tools/c1/cal1_case.c', FLAGS, ['gmp_public.lib', 'psapi.lib']),
            ('cal1_case_checked.exe', 'tools/c1/cal1_case.c', CHECKED, ['gmp_public.lib', 'psapi.lib']),
            ('cal1_guard.exe', 'tools/c1/cal1_guard.c', FLAGS, GUARD_LIBRARIES))
EXTRA_SOURCES = ('tools/c1/cal1_suite.py', 'tools/c1/cal1_build.py', 'tools/c1/gmp_setup.py',
                 'tools/c1/engineering_codec.py', 'config/c1_gmp_pin.toml', 'config/calibration_suite_v1.json')


def public_import_library(folder, env, bindir):
    """Import library for the documented public mpz namespace, the two public
    data symbols and the documented custom-allocation functions only."""
    exports = pe_info((folder / 'libgmp-10.dll').read_bytes())['exports']
    allowed = {name: kind for name, kind in exports.items() if name.startswith('__gmpz_') or name in (
        '__gmp_version', '__gmp_bits_per_limb', '__gmp_set_memory_functions', '__gmp_get_memory_functions')}
    if allowed.get('__gmp_set_memory_functions') != 'function' or allowed.get('__gmpz_mul') != 'function':
        raise Refusal('Expected public GMP exports unavailable')
    definition = 'LIBRARY libgmp-10.dll\nEXPORTS\n' + ''.join(
        name + (' DATA' if kind == 'data' else '') + '\n' for name, kind in sorted(allowed.items()))
    (folder / 'gmp_public.def').write_text(definition, encoding='ascii')
    invoke([str(bindir / 'lib.exe'), '-nologo', '-machine:x64', '-def:gmp_public.def', '-out:gmp_public.lib'], env, folder)
    return dict(definition=hashes(definition.encode('ascii')), library=hashes((folder / 'gmp_public.lib').read_bytes()),
                public_export_count=str(len(allowed)))


def compile_programs(folder, programs, env, bindir):
    artifacts = {}
    for name, source_path, flags, libraries in programs:
        source = (ROOT / source_path).read_bytes()
        stem = name[:-4]
        (folder / (stem + '.c')).write_bytes(source)
        invoke([str(bindir / 'cl.exe'), *flags, '-I.', stem + '.c', *libraries, '-Fe:' + name, '-Fo:' + stem + '.obj',
                '-link', '-Brepro'], env, folder)
        artifacts[name] = dict(source=hashes(source), source_path=source_path, flags=list(flags), libraries=list(libraries),
                               executable=hashes((folder / name).read_bytes()))
    return artifacts


def main():
    require_authorization()
    evidence = build(True)
    env, bindir, toolchain = msvc_environment()
    folder = CAL1 / 'bin'
    folder.mkdir(parents=True, exist_ok=True)
    for filename in ('gmp.h', 'libgmp-10.dll'):
        (folder / filename).write_bytes((LOCAL / 'offline' / filename).read_bytes())
    library = public_import_library(folder, env, bindir)
    artifacts = compile_programs(folder, PROGRAMS, env, bindir)
    # Repository blobs use LF; a checkout may present CRLF. Record the LF form
    # so the driver can compare against the committed blob exactly.
    committed = {path: hashes((ROOT / path).read_bytes().replace(bytes([13, 10]), bytes([10]))) for path in
                 sorted({p[1] for p in PROGRAMS} | set(EXTRA_SOURCES))}
    result = dict(stage='hardware characterization', observed_at=now(), offline=True, toolchain=toolchain,
                  artifacts=artifacts, dependency=evidence['dll'], import_library=library,
                  pin=hashes(PIN.read_bytes()), driver=committed['tools/c1/cal1_suite.py'], committed_sources=committed)
    (CAL1 / 'build.json').write_text(json.dumps(result, indent=1) + '\n', encoding='ascii')
    print(json.dumps({'status': 'ok', 'observed_at': result['observed_at'],
                      'executables': {k: v['executable']['sha3_256'][:16] for k, v in artifacts.items()}}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'refused', 'reason': str(error) if isinstance(error, Refusal) else 'Build refused; raw diagnostic suppressed'}))
        sys.exit(1)
