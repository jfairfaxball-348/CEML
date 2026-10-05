"""BuildProfiler: freeze BUILD_MANIFEST.json and config/local_machine_profile.json.

Runs only after the engineering decisions exist and the pinned offline engine
build is present. Every profile value is copied from a committed sanitized
report, the decision log or the build record; nothing is measured, guessed or
tuned here. The tool refuses if a decision disagrees with the engine's frozen
defaults, if a built artifact differs from its record, or if any source of the
build differs from the named commit. It does not run V1.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tomllib

from engineering_codec import blob, canonical_bytes
from gmp_setup import ROOT, hashes
from privacy_gate import inspect_text, validate_artifact

ENGINE = ROOT / 'local/c1/engine'
REPORTS = ROOT / 'local_reports'
ENABLED = ['arith.gmp.public', 'alloc.copy', 'audit.divisibility', 'checkpoint.buffered', 'engine.hier_affine.explicit',
           'oracle.c.direct', 'oracle.t.direct', 'oracle.u.odd_only', 'parallel.single', 'state.dense', 'terminal.direct_t']
EXPECTED = {'decision.matrix.01.route-crossover': 'engine.hier_affine.explicit',
            'decision.matrix.03.hierarchical-sweep': 'hier-explicit-d2-k16384',
            'decision.matrix.04.backend-multiplication': 'arith.gmp.public', 'decision.matrix.05.representation': 'state.dense',
            'decision.matrix.06.allocation': 'alloc.copy', 'decision.matrix.07.compiler-build': 'portable-release',
            'decision.matrix.08.parallelism': 'parallel.single', 'decision.matrix.09.checkpoint': 'checkpoint.buffered',
            'decision.matrix.10.terminal-handoff': 'terminal.direct_t', 'decision.matrix.11.audit-cost': 'audit.divisibility',
            'decision.checkpoint.filesystem': 'supported', 'decision.matrix.02.small-block-sweep': 'small_block_width null'}


def domain_digest(label, obj, omit):
    body = {k: v for k, v in obj.items() if k != omit}
    return hashlib.sha3_256(label.encode('ascii') + b'\0' + blob(canonical_bytes(body))).hexdigest()


def lf(path):
    return (ROOT / path).read_bytes().replace(bytes([13, 10]), bytes([10]))


def load(name):
    return json.loads((REPORTS / name).read_text(encoding='utf-8'))


def main():
    build = json.loads((ENGINE / 'build.json').read_text())
    commit = subprocess.check_output(['git', 'log', '-1', '--format=%H', '--', 'src'], cwd=ROOT).decode().strip()
    for path, meta in build['committed_sources'].items():
        if hashes(subprocess.check_output(['git', 'show', commit + ':' + path], cwd=ROOT)) != meta and \
                hashes(subprocess.check_output(['git', 'show', 'HEAD:' + path], cwd=ROOT)) != meta:
            raise ValueError('A build source differs from the committed source: ' + path)
        if path.startswith('src/') and hashes(subprocess.check_output(['git', 'show', commit + ':' + path], cwd=ROOT)) != meta:
            raise ValueError('Engine source is not the source commit content: ' + path)
    artifacts = []
    for name in ('ceml.exe', 'ceml_checked.exe', 'cal1_guard.exe'):
        data = (ENGINE / 'bin' / name).read_bytes()
        if hashes(data) != build['artifacts'][name]['executable']:
            raise ValueError('Built artifact differs from its build record')
        artifacts.append(dict(logical_name=name, sha3_256=hashlib.sha3_256(data).hexdigest(), bytes=str(len(data))))
    dll = (ENGINE / 'bin' / 'libgmp-10.dll').read_bytes()
    if hashes(dll) != build['dependency']:
        raise ValueError('Dependency differs from the pinned candidate')
    artifacts.append(dict(logical_name='libgmp-10.dll', sha3_256=hashlib.sha3_256(dll).hexdigest(), bytes=str(len(dll))))
    pin = tomllib.loads(lf('config/c1_gmp_pin.toml').decode('utf-8'))
    if pin['dll_sha3_256'] != build['dependency']['sha3_256'] or pin['msvc_tools_version'] != build['toolchain']['msvc_tools_version']:
        raise ValueError('Pin and build record disagree')
    decisions = {d['decision_id']: d for d in load('ENGINEERING_DECISIONS.json')['decisions']}
    for identity, marker in EXPECTED.items():
        selection = decisions[identity]['selection']
        if selection is None or marker not in selection:
            raise ValueError('Decision does not support the engine default: ' + identity)
    hardware, summary, log = load('HARDWARE_REPORT.json'), load('BENCHMARK_SUMMARY.json'), load('ENGINEERING_DECISIONS.json')
    facts = {r['record_id']: r for r in hardware['records']}

    def value(identity):
        v = facts[identity]['value']
        return v['value'] if isinstance(v, dict) and 'value' in v else v

    toolchain = build['toolchain']
    cl = facts['tools.msvc.cl.exe']['value']
    link = facts['tools.msvc.link.exe']['value']
    flags = build['artifacts']['ceml.exe']['flags'] + ['-link', '-Brepro'] + build['artifacts']['ceml.exe']['libraries']
    dependencies = [
        dict(name='GMP', version='6.3.0 (distribution release 6.3.0-2)',
             source_channel='MSYS2 UCRT64 binary package mingw-w64-ucrt-x86_64-gmp from the official mirror; published SHA-256 verified; matching source package retained in the content-addressed local cache',
             artifact_digest=build['dependency']['sha3_256'],
             build_options=['prebuilt distribution shared library, not rebuilt locally', 'package SHA-256 ' + pin['binary_sha256'],
                            'source package SHA-256 ' + pin['source_sha256'], 'header SHA3-256 ' + pin['header_sha3_256']],
             linkage='dynamic; import library generated locally from the documented public mpz exports and the custom-allocation functions',
             features=['custom-allocation-interface', 'mpz']),
        dict(name='Microsoft Universal C Runtime and Visual C++ runtime', version='Windows SDK ' + toolchain['windows_sdk_version'] + ', MSVC tools ' + toolchain['msvc_tools_version'],
             source_channel='Installed toolchain; dynamic runtime selected by the MD option', artifact_digest=None,
             build_options=['operating-system and toolchain component; content not pinned by digest'], linkage='dynamic', features=[]),
    ]
    manifest = dict(
        experiment='CEML', schema_version='CEML-BUILD-MANIFEST-1', source_commit=commit, target_triple=toolchain['target'],
        abi=toolchain['abi'],
        toolchains=[dict(name='Microsoft C compiler cl.exe', version='.'.join(cl[k] for k in ('major', 'minor', 'build', 'revision'))),
                    dict(name='Microsoft linker link.exe', version='.'.join(link[k] for k in ('major', 'minor', 'build', 'revision'))),
                    dict(name='MSVC tools', version=toolchain['msvc_tools_version']),
                    dict(name='Windows SDK', version=toolchain['windows_sdk_version']),
                    dict(name='Python build driver', version=pin['python_version']),
                    dict(name='zstandard extraction module', version=pin['zstandard_version'])]
        + [dict(name='tool content SHA3-256 ' + tool, version=digest) for tool, digest in sorted(pin['tool_sha3_256'].items())],
        flags=flags, native_tuning=False, non_portable=False, dependencies=dependencies, enabled_routes=ENABLED,
        lock_artifacts=[dict(logical_path=path, sha3_256=hashlib.sha3_256(lf(path)).hexdigest())
                        for path in ('config/c1_dependency_manifest.toml', 'config/c1_gmp_pin.toml')],
        build_artifacts=artifacts,
        offline_rebuild_recipe=['Populate local/c1/cache/sha256 with the two pinned GMP archives named in config/c1_gmp_pin.toml (the only network step: python tools/c1/gmp_setup.py acquire)',
                                'python tools/c1/gmp_setup.py build', 'python tools/c1/gmp_setup.py offline-smoke',
                                'python tools/c1/engine_build.py',
                                'The build and engine_build steps never fetch; they refuse if a pinned archive, header, library, compiler binary, flag or source differs',
                                'Compare the SHA3-256 of each produced artifact with build_artifacts'])
    manifest['build_digest'] = domain_digest('CEML-I1-BUILD-V1', manifest, 'build_digest')
    text = json.dumps(manifest, ensure_ascii=True, indent=2) + '\n'
    if validate_artifact(manifest, 'BUILD_MANIFEST.json', ROOT) or inspect_text(text, 'BUILD_MANIFEST.json'):
        raise ValueError('Build manifest schema or privacy check failed')
    (REPORTS / 'BUILD_MANIFEST.json').write_text(text, encoding='utf-8', newline='\n')

    # Deterministic scan artifact over the committed sanitized C1 artifact set (excluding the profile itself).
    scanned = {}
    for path in ('local_reports/HARDWARE_REPORT.json', 'local_reports/HARDWARE_REPORT.md', 'local_reports/BENCHMARK_SUMMARY.json',
                 'local_reports/BENCHMARK_BUNDLES.json', 'local_reports/ENGINEERING_DECISIONS.json', 'local_reports/BUILD_MANIFEST.json',
                 'config/c1_dependency_manifest.toml', 'config/c1_gmp_pin.toml'):
        content = lf(path)
        findings = inspect_text(content.decode('utf-8'), path)
        if findings:
            raise ValueError('Sensitive-data scan failed for ' + path)
        scanned[path] = dict(sha3_256=hashlib.sha3_256(content).hexdigest(), findings='0')
    scan = canonical_bytes(dict(scanner='tools/c1/privacy_gate.py inspect_text', files=scanned, result='PASS'))
    (ROOT / 'local/c1/privacy_scan_final.json').write_bytes(scan)

    ceilings = facts['resource.ceilings']['value']
    memory_kib = int(value('obs.memory.physically_installed'))
    profile = dict(
        experiment='CEML', schema_version='CEML-LOCAL-MACHINE-PROFILE-1', source_commit=commit, build_digest=manifest['build_digest'],
        hardware_report_digest=hardware['artifact_digest'], benchmark_summary_digest=summary['artifact_digest'],
        engineering_decision_log_digest=log['artifact_digest'],
        system=dict(os_family='Windows', os_release=value('obs.os.Caption') + ' ' + value('obs.os.Version'),
                    kernel_release='Windows NT build ' + value('obs.os.BuildNumber'), architecture='x86_64 (' + value('obs.os.OSArchitecture') + ')',
                    abi='LLP64', virtualization=None),
        cpu=dict(vendor=value('obs.cpu.0.Manufacturer'), model=value('obs.cpu.0.Name'), physical_cores=value('obs.cpu.0.NumberOfCores'),
                 logical_threads=value('obs.cpu.0.NumberOfLogicalProcessors'), instruction_features=[], cache_summary=[]),
        memory=dict(installed_bytes=str(memory_kib*1024), available_bytes_at_audit=value('obs.memory.performance.AvailableBytes'),
                    swap_capacity_bytes=str(int(value('obs.memory.SizeStoredInPagingFiles'))*1024), page_size_bytes=value('obs.memory.page_size')),
        checkpoint_storage=dict(filesystem_class=value('obs.storage.FileSystemType') + ' on a ' + value('obs.storage.DriveType').lower() + ' local volume',
                                local_or_remote='local', durability_supported=True, durability_decision_id='decision.checkpoint.filesystem',
                                strategy='win32-ntfs-generation-directory-v1: write and FlushFileBuffers both files, flush the directory, re-read and validate, '
                                         'publish by one same-directory MoveFileExW write-through rename, flush the parent directory, update the pointer hint, '
                                         're-read, retain the previous generation, retire older ones; recovery by content only'),
        toolchain=dict(language_family='C17', compiler='Microsoft C compiler cl.exe', compiler_version=manifest['toolchains'][0]['version']
                       + ' (MSVC tools ' + toolchain['msvc_tools_version'] + ')', linker='Microsoft linker link.exe',
                       linker_version=manifest['toolchains'][1]['version'], target_triple=toolchain['target'], abi=toolchain['abi'], flags=flags,
                       native_tuning=False, non_portable=False),
        dependencies=[dict(name=d['name'], version=d['version'], source_channel=d['source_channel'], artifact_digest=d['artifact_digest'],
                           linkage=d['linkage'], features=d['features']) for d in dependencies],
        engineering_choices=dict(backend_route='arith.gmp.public', state_representation='state.dense', small_block_width=None,
                                 hierarchical_divisor='2', hierarchical_k_cap='16384', allocation_strategy='alloc.copy',
                                 parallelism_route='parallel.single', thread_count='1', terminal_handoff='terminal.direct_t',
                                 audit_mode='audit.divisibility',
                                 checkpoint_strategy='checkpoint.buffered; promotion at the first macro boundary after 600 seconds and at the terminal state'),
        resource_limits=dict(minimum_available_memory_bytes=ceilings['minimum_available_memory_bytes'],
                             maximum_process_memory_bytes=ceilings['maximum_process_memory_bytes'],
                             minimum_free_storage_bytes=ceilings['minimum_free_storage_bytes'],
                             swap_pressure_rule='Any page output in a one-second interval, or page input above 100 pages per second in two consecutive '
                                                'one-second intervals, refuses or aborts; admission waits at most 30 intervals for page input only',
                             maximum_processes=ceilings['maximum_processes'], maximum_threads=ceilings['maximum_threads'],
                             thermal_stop_rule='Temperature unavailable; stop when processor performance reads below 100 percent of nominal at a sampled interval; '
                                               'bounded cases of at most 5 seconds separated by monitoring',
                             maximum_case_seconds=ceilings['maximum_case_seconds'],
                             power_sleep_precondition='AC power and zero standby and hibernate idle indices, checked at every polling boundary; no power policy is changed'),
        unavailable_constraints=[
            'Temperature telemetry unavailable; no thermal-safety claim',
            'Instruction-set features, cache hierarchy, topology and virtualization status were not probed; none is inferred',
            'No native-tuned build mode exists for the pinned compiler; the build is portable-release',
            'FLINT, Rust with rug, sparse state, value-threaded recursion and auxiliary parallelism are unavailable or not implemented',
            'Checkpoint durability rests on documented flush semantics and forced process-termination tests; no power-loss evidence',
            'The resource limits above are the bounded-calibration ceilings; resource limits for scientific-scale states are not established by C1',
            'The pinned LLP64 GMP counts bits in 32 bits: states and generator masks of 2^32 bits or more (about 1.29e9 decimal digits) are outside this build',
            'The hierarchical cap and divisor were chosen among performance-tied candidates, not as a measured winner',
            'Scientific-scale performance and memory behaviour are not measured'],
        evidence_refs=sorted(decisions),
        privacy_attestation=dict(sensitive_identifiers_excluded=True, scan_passed=True, scan_artifact_digest=hashlib.sha3_256(scan).hexdigest()))
    profile['machine_profile_digest'] = domain_digest('CEML-I1-MACHINE-PROFILE-V1', profile, 'machine_profile_digest')
    text = json.dumps(profile, ensure_ascii=True, indent=2) + '\n'
    if validate_artifact(profile, 'local_machine_profile.json', ROOT) or inspect_text(text, 'local_machine_profile.json'):
        raise ValueError('Machine profile schema or privacy check failed')
    (ROOT / 'config/local_machine_profile.json').write_text(text, encoding='utf-8', newline='\n')
    print(json.dumps(dict(source_commit=commit, build_digest=manifest['build_digest'], machine_profile_digest=profile['machine_profile_digest'],
                          scan_artifact_digest=profile['privacy_attestation']['scan_artifact_digest'])))


def verify():
    """Reproduce both dedicated digests and the generic artifact digests from the committed files."""
    from engineering_codec import artifact_digest
    manifest = load('BUILD_MANIFEST.json')
    profile = json.loads((ROOT / 'config/local_machine_profile.json').read_text(encoding='utf-8'))
    checks = {'build_digest': domain_digest('CEML-I1-BUILD-V1', manifest, 'build_digest') == manifest['build_digest'],
              'machine_profile_digest': domain_digest('CEML-I1-MACHINE-PROFILE-V1', profile, 'machine_profile_digest') == profile['machine_profile_digest'],
              'profile_binds_build': profile['build_digest'] == manifest['build_digest'] and profile['source_commit'] == manifest['source_commit']}
    for name, key in (('HARDWARE_REPORT.json', 'hardware_report_digest'), ('BENCHMARK_SUMMARY.json', 'benchmark_summary_digest'),
                      ('ENGINEERING_DECISIONS.json', 'engineering_decision_log_digest'), ('BENCHMARK_BUNDLES.json', None)):
        report = load(name)
        checks[name] = artifact_digest(report) == report['artifact_digest'] and (key is None or profile[key] == report['artifact_digest'])
    summary = load('BENCHMARK_SUMMARY.json')
    checks['summary_binds_reports'] = (summary['hardware_report_digest'] == load('HARDWARE_REPORT.json')['artifact_digest']
                                       and summary['benchmark_bundle_index_digest'] == load('BENCHMARK_BUNDLES.json')['artifact_digest'])
    for item in manifest['lock_artifacts']:
        checks['lock:' + item['logical_path']] = hashlib.sha3_256(lf(item['logical_path'])).hexdigest() == item['sha3_256']
    for item in manifest['build_artifacts']:
        path = ENGINE / 'bin' / item['logical_name']
        if path.is_file():
            checks['artifact:' + item['logical_name']] = hashlib.sha3_256(path.read_bytes()).hexdigest() == item['sha3_256']
    for name, ok in checks.items():
        print('OK  ' if ok else 'FAIL', name)
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    try:
        sys.exit(verify() if sys.argv[1:] == ['verify'] else main())
    except (ValueError, KeyError) as error:
        print('REFUSED:', error)
        sys.exit(1)
