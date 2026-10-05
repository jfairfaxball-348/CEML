"""Stage: hardware characterization; offline build of the synthetic checkpoint
store harness from the CheckpointCodec, FilesystemAdapter and CheckpointStore
sources. The pinned GMP capability build is re-verified first. No network."""
from __future__ import annotations

import json
import sys

from gmp_setup import FLAGS, PIN, ROOT, Refusal, build, hashes, invoke, msvc_environment, now, require_authorization

CAL1 = ROOT / 'local/c1/cal1'
SOURCES = ('tools/c1/ckpt_case.c', 'src/ceml_sha3.c', 'src/ceml_codec.c', 'src/ceml_fs_win32.c', 'src/ceml_store.c')
HEADERS = ('src/ceml_sha3.h', 'src/ceml_codec.h', 'src/ceml_fs.h', 'src/ceml_store.h')
DRIVERS = ('tools/c1/ckpt_suite.py', 'tools/c1/ckpt_build.py', 'tools/c1/cal1_guard.c', 'tools/c1/gmp_setup.py',
           'tools/c1/engineering_codec.py', 'config/c1_gmp_pin.toml')


def lf(path):
    return (ROOT / path).read_bytes().replace(bytes([13, 10]), bytes([10]))


def main():
    require_authorization()
    evidence = build(True)
    env, bindir, toolchain = msvc_environment()
    folder = CAL1 / 'bin'
    if not (folder / 'gmp_public.lib').is_file() or not (folder / 'cal1_guard.exe').is_file():
        raise Refusal('Bounded harness build must exist first')
    if hashes((folder / 'libgmp-10.dll').read_bytes()) != evidence['dll']:
        raise Refusal('Harness dependency differs from the pinned candidate')
    names = []
    for path in SOURCES + HEADERS:
        name = path.rsplit('/', 1)[1]
        (folder / name).write_bytes(lf(path))
        if name.endswith('.c'):
            names.append(name)
    invoke([str(bindir / 'cl.exe'), *FLAGS, '-I.', *names, 'gmp_public.lib', '-Fe:ckpt_case.exe', '-link', '-Brepro'], env, folder)
    result = dict(stage='hardware characterization', observed_at=now(), offline=True, toolchain=toolchain, flags=FLAGS,
                  executables={name: hashes((folder / name).read_bytes()) for name in ('ckpt_case.exe', 'cal1_guard.exe')},
                  dependency=evidence['dll'], pin=hashes(PIN.read_bytes()),
                  committed_sources={path: hashes(lf(path)) for path in sorted(SOURCES + HEADERS + DRIVERS)})
    (CAL1 / 'ckpt_build.json').write_text(json.dumps(result, indent=1) + '\n', encoding='ascii')
    print(json.dumps({'status': 'ok', 'observed_at': result['observed_at'],
                      'ckpt_case': result['executables']['ckpt_case.exe']['sha3_256'][:16]}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'refused', 'reason': str(error) if isinstance(error, Refusal) else 'Build refused; raw diagnostic suppressed'}))
        sys.exit(1)
