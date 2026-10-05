"""Stage: implementation; pinned offline build of the production engine.

Builds ceml.exe (portable-release), ceml_checked.exe (assertion and
run-time-check mode) and the resource guard from committed sources only, after
re-verifying the committed GMP pin. No network access exists on this path; a
missing or changed pinned input refuses the build. The record written here is
the input of BUILD_MANIFEST.json; it is not itself the manifest.
"""
from __future__ import annotations

import json
import sys

from gmp_setup import FLAGS, LOCAL, PIN, ROOT, Refusal, build, hashes, invoke, msvc_environment, now, pe_info, require_authorization
from cal1_build import CHECKED, GUARD_LIBRARIES, public_import_library

ENGINE = ROOT / 'local/c1/engine'
SOURCES = ('src/ceml_main.c', 'src/ceml_calibrate.c', 'src/ceml_engine.c', 'src/ceml_oracle.c', 'src/ceml_start.c',
           'src/ceml_validate.c', 'src/ceml_codec.c', 'src/ceml_sha3.c', 'src/ceml_fs_win32.c', 'src/ceml_store.c')
HEADERS = ('src/ceml_calibrate.h', 'src/ceml_engine.h', 'src/ceml_oracle.h', 'src/ceml_start.h', 'src/ceml_validate.h',
           'src/ceml_codec.h', 'src/ceml_records.h', 'src/ceml_records.inc', 'src/ceml_sha3.h', 'src/ceml_fs.h', 'src/ceml_store.h')
GUARD = 'tools/c1/cal1_guard.c'
TOOLING = ('tools/c1/engine_build.py', 'tools/c1/cal1_build.py', 'tools/c1/cal1_suite.py', 'tools/c1/ckpt_suite.py',
           'tools/c1/gmp_setup.py', 'tools/c1/engineering_codec.py', 'config/c1_gmp_pin.toml', 'config/calibration_suite_v1.json')
ENGINE_LIBRARIES = ['gmp_public.lib', 'psapi.lib']


def lf(path):
    return (ROOT / path).read_bytes().replace(bytes([13, 10]), bytes([10]))


def source_set_digest(paths):
    """One identity for an ordered multi-file source set."""
    import hashlib
    digest256, digest3, total = hashlib.sha256(), hashlib.sha3_256(), 0
    for path in sorted(paths):
        data = lf(path)
        for d in (digest256, digest3):
            d.update(len(path).to_bytes(8, 'big') + path.encode('ascii') + len(data).to_bytes(8, 'big') + data)
        total += len(data)
    return {'sha256': digest256.hexdigest(), 'sha3_256': digest3.hexdigest(), 'bytes': str(total)}


def main():
    require_authorization()
    evidence = build(True)
    env, bindir, toolchain = msvc_environment()
    folder = ENGINE / 'bin'
    folder.mkdir(parents=True, exist_ok=True)
    for filename in ('gmp.h', 'libgmp-10.dll'):
        (folder / filename).write_bytes((LOCAL / 'offline' / filename).read_bytes())
    library = public_import_library(folder, env, bindir)
    names = []
    for path in SOURCES + HEADERS + (GUARD,):
        name = path.rsplit('/', 1)[1]
        (folder / name).write_bytes(lf(path))
        if name.endswith('.c') and path != GUARD:
            names.append(name)
    artifacts = {}
    for executable, flags in (('ceml.exe', FLAGS), ('ceml_checked.exe', CHECKED)):
        invoke([str(bindir / 'cl.exe'), *flags, '-I.', *names, *ENGINE_LIBRARIES, '-Fe:' + executable, '-link', '-Brepro'], env, folder)
        data = (folder / executable).read_bytes()
        if 'libgmp-10.dll' not in pe_info(data)['imports']:
            raise Refusal('Engine does not import the pinned GMP library')
        artifacts[executable] = dict(source=source_set_digest(SOURCES + HEADERS), source_path='src', flags=list(flags),
                                     libraries=ENGINE_LIBRARIES, executable=hashes(data), imports=pe_info(data)['imports'])
    invoke([str(bindir / 'cl.exe'), *FLAGS, '-I.', 'cal1_guard.c', *GUARD_LIBRARIES, '-Fe:cal1_guard.exe', '-link', '-Brepro'], env, folder)
    artifacts['cal1_guard.exe'] = dict(source=hashes(lf(GUARD)), source_path=GUARD, flags=list(FLAGS), libraries=GUARD_LIBRARIES,
                                       executable=hashes((folder / 'cal1_guard.exe').read_bytes()))
    committed = {path: hashes(lf(path)) for path in sorted(SOURCES + HEADERS + (GUARD,) + TOOLING)}
    result = dict(stage='implementation', observed_at=now(), offline=True, toolchain=toolchain, flags=list(FLAGS), artifacts=artifacts,
                  executables={'ceml.exe': artifacts['ceml.exe']['executable'], 'cal1_guard.exe': artifacts['cal1_guard.exe']['executable']},
                  dependency=evidence['dll'], dependency_header=evidence['header'], import_library=library,
                  pin=hashes(PIN.read_bytes()), pin_lf=hashes(lf('config/c1_gmp_pin.toml')),
                  driver=committed['tools/c1/cal1_suite.py'], committed_sources=committed)
    (ENGINE / 'build.json').write_text(json.dumps(result, indent=1) + '\n', encoding='ascii')
    print(json.dumps({'status': 'ok', 'observed_at': result['observed_at'],
                      'executables': {k: v['executable']['sha3_256'][:16] for k, v in artifacts.items()}}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'refused', 'reason': str(error) if isinstance(error, Refusal) else 'Build refused; raw diagnostic suppressed'}))
        sys.exit(1)
