"""Stage: hardware characterization; fixed initial CEML-CAL-1 route subset.

No arbitrary starts, seeds, sizes, budgets, routes or repeats are accepted.
Stop at the first refusal; retain it and every completed repeat.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sys
import re

from engineering_codec import artifact_digest, blob, canonical_bytes, self_test_vector, uenc
from gmp_setup import LOCAL, ROOT, Refusal, hashes
from privacy_gate import inspect_text, validate_artifact

BUNDLE = ROOT / 'local/c1/benchmark_bundles/c1-20261005-route-subset'
BUDGET = ROOT / 'local/c1/initial-route-budget.json'
SEED = bytes(range(32))
ROUTES = {'affine-small-public': 'engine.small_affine', 't-direct': 'engine.direct_t'}


def engineering_input(bits, index):
    if bits not in (1024, 4096) or index not in (0, 1, 2):
        raise Refusal('Input outside initial prescribed route subset')
    family = 'route-crossover'
    identity = f'cal1/01/{family}/{bits}/{index}'
    msg = b'CEML-CALIBRATION-RANDOM-V1\0' + SEED + blob(family.encode()) + uenc(bits) + uenc(index) + uenc(0)
    value = int.from_bytes(hashlib.shake_256(msg).digest((bits+7)//8), 'big')
    value &= (1 << bits)-1
    value |= (1 << (bits-1)) | 1
    descriptor = dict(case_index=str(index), family=family, generator='shake256-ceml-calibration-random-v1',
                      input_id=identity, operand_roles=[dict(forced_odd=True, role='state', size_bits=str(bits), stream_index='0')],
                      size_bits=str(bits), suite_version='CEML-CAL-1')
    digest = hashlib.sha3_256(b'CEML-I1-CALIBRATION-INPUT-V1\0'+blob(canonical_bytes(descriptor))+blob(uenc(value))).hexdigest()
    return value, descriptor, digest


def state_digest(n, t, odd):
    return hashlib.sha3_256(b'CEML-I1-CALIBRATION-STATE-V1\0'+uenc(n)+uenc(t)+uenc(odd)+uenc(t+odd)).hexdigest()


def raw_write(name, obj):
    data = canonical_bytes(obj)
    if inspect_text(data.decode('ascii'), name):
        raise Refusal('Evidence privacy check failed')
    (BUNDLE / name).write_bytes(data)


def build_context(build, source_commit):
    return dict(source_commit=source_commit, target_triple=build['toolchain']['target'], abi=build['toolchain']['abi'],
                toolchains=[{'name': 'MSVC tools', 'version': build['toolchain']['msvc_tools_version']},
                            {'name': 'Windows SDK', 'version': build['toolchain']['windows_sdk_version']}],
                flags=build['compiler_flags']+['-link', '-Brepro'],
                dependencies=[{'name': 'GMP', 'version': '6.3.0-2', 'linkage': 'dynamic-public-C', 'features': ['mpz']}],
                enabled_features=['bounded-engineering-only', '256-shortcut-steps', 'width-4', 'definition-C-reference', 'divisibility-check'],
                process_count='1', thread_count='1', affinity='One allowed logical processor; lowest set bit of inherited process affinity')


def save_budget(handle, nanoseconds):
    handle.seek(0)
    handle.write(json.dumps({'charged_ns': str(nanoseconds)}).encode())
    handle.truncate()
    handle.flush()
    os.fsync(handle.fileno())


def one_case(build, context, bits, candidate, index, repeat):
    n, descriptor, input_digest = engineering_input(bits, index)
    case_id = descriptor['input_id'] + '/' + candidate
    folder = LOCAL / 'calibration'
    for base in ('cal_candidate', 'cal_guard'):
        if hashes((folder / (base+'.exe')).read_bytes()) != build['artifacts'][base]['executable']:
            raise Refusal('Calibration executable changed')
    if hashes((folder / 'libgmp-10.dll').read_bytes()) != build['dependency']:
        raise Refusal('Calibration dependency changed')
    p = subprocess.run([str(folder / 'cal_guard.exe'), candidate, format(n, 'x')], cwd=folder,
                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=12)
    if len(p.stdout) > 32768 or p.stderr:
        raise Refusal('Unexpected calibration output')
    lines = [json.loads(line) for line in p.stdout.splitlines() if line]
    guards = [x for x in lines if x.get('kind') == 'guard']
    states = [x for x in lines if x.get('kind') == 'candidate']
    if len(guards) != 1 or len(states) > 1:
        raise Refusal('Required guarded outcome unavailable')
    guard = guards[0]
    candidate_state = states[0] if states else None
    abort = guard['abort_code']
    agreement = False
    route_count = '0'
    fallback = '0'
    digest = reference = state_digest(n, 0, 0)
    kernel_ns = None
    if candidate_state:
        digest = state_digest(int(candidate_state['n_hex'], 16), int(candidate_state['shortcut_steps']), int(candidate_state['odd_steps']))
        reference = state_digest(int(candidate_state['reference_hex'], 16), int(candidate_state['reference_shortcut_steps']), int(candidate_state['reference_odd_steps']))
        agreement = digest == reference and candidate_state['correctness_agreement']
        agreement &= int(candidate_state['standard_steps']) == int(candidate_state['shortcut_steps'])+int(candidate_state['odd_steps'])
        route_count = candidate_state['activated_count']
        fallback = candidate_state['fallback_count']
        kernel_ns = str(int(candidate_state['kernel_ticks'])*1000000000//int(candidate_state['qpc_frequency']))
        if not agreement:
            abort = abort or 'C1_CORRECTNESS_INVALID'
        elif int(route_count) <= 0 or fallback != '0' or candidate_state['tail_count'] != '0':
            abort = abort or 'C1_ROUTE_INVALID'
    elif abort is None:
        abort = 'C1_MEASUREMENT_INVALID'
    if p.returncode and abort is None:
        abort = 'C1_MEASUREMENT_INVALID'
    route = dict(requested_routes=[ROUTES[candidate]], activated_counts={ROUTES[candidate]: route_count}, fallback_count=fallback)
    route['route_evidence_digest'] = hashlib.sha3_256(canonical_bytes(route)).hexdigest()
    record = dict(experiment='CEML', schema_version='CEML-CALIBRATION-RECORD-1', record_class='CALIBRATION_MEASUREMENT',
                  record_id=f'calibration.route.{bits}.{candidate}.{index}.{repeat}', suite_version='CEML-CAL-1',
                  case_id=case_id, input_id=descriptor['input_id'], input_digest=input_digest, candidate_id=candidate,
                  build_id='c1-native-route-subset-'+build['artifacts']['cal_candidate']['executable']['sha3_256'][:16],
                  executable_digest=build['artifacts']['cal_candidate']['executable']['sha3_256'], build_context=context,
                  wall_clock_method='QueryPerformanceCounter around candidate transitions only; integer floor conversion to nanoseconds',
                  cpu_time_method='GetProcessTimes: whole child including initialization and definition oracle; 100 ns units',
                  peak_rss_method='GetProcessMemoryInfo PeakWorkingSetSize over whole child; bytes',
                  artifact_digests=[build['artifacts'][x][kind]['sha3_256'] for x in ('cal_candidate','cal_guard') for kind in ('source','executable')]+[build['dependency']['sha3_256'],build['pin']['sha3_256']],
                  repeat_index=str(repeat), warmup=repeat == 0, measured=repeat != 0, activation=route,
                  wall_time_ns=kernel_ns, cpu_time_ns=guard.get('cpu_time_ns') if abort is None else None,
                  peak_rss_bytes=guard.get('peak_rss_bytes') if abort is None else None, scratch_bytes='0',
                  correctness_state_digest=digest, reference_state_digest=reference, correctness_agreement=bool(agreement),
                  valid=abort is None, invalid_reason=None if abort is None else guard.get('reason', abort), abort_code=abort,
                  thermal_observation='Unavailable; five-second child limit and sixty-second aggregate ceiling',
                  swap_observation='PDH pages input/output proxy; includes mapped-file traffic; two admission samples and mid-case checks')
    record['artifact_digest'] = artifact_digest(record)
    if validate_artifact(record, 'repeat.json', ROOT):
        raise Refusal('Calibration schema check failed')
    stem = f'{bits}-{candidate}-{index}-{repeat}'
    raw_write(stem+'-record.json', record)
    raw_write(stem+'-detail.json', dict(descriptor=descriptor, guard=guard, candidate=candidate_state))
    charged = 0 if abort == 'C1_PREFLIGHT_REFUSAL' else int(guard.get('process_wall_ticks', '0'))*1000000000//int(guard.get('qpc_frequency', '1'))
    if abort != 'C1_PREFLIGHT_REFUSAL' and not 0 < charged <= 5000000000:
        charged = 5000000000
    return record, charged


def main():
    global BUNDLE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle-id', default='c1-20261005-route-subset')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', args.bundle_id):
        raise Refusal('Bundle ID must contain only lowercase letters, digits and hyphens')
    BUNDLE = ROOT / 'local/c1/benchmark_bundles' / args.bundle_id
    self_test_vector()
    if BUNDLE.exists():
        raise Refusal('Existing subset evidence retained; no automatic overwrite or repeat')
    build = json.loads((LOCAL / 'calibration_build.json').read_text())
    source_commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT).decode().strip()
    for base in ('cal_candidate', 'cal_guard'):
        committed_source = subprocess.check_output(['git','show','HEAD:tools/c1/'+base+'.c'], cwd=ROOT)
        if hashes(committed_source) != build['artifacts'][base]['source']:
            raise Refusal('Native calibration source must be committed before measurement')
    context = build_context(build, source_commit)
    BUDGET.parent.mkdir(parents=True, exist_ok=True)
    with os.fdopen(os.open(BUDGET, os.O_RDWR | os.O_CREAT, 0o600), 'r+b') as budget:
        budget.seek(0)
        msvcrt.locking(budget.fileno(), msvcrt.LK_NBLCK, 1)
        budget.seek(0)
        prior = budget.read(1024)
        charged = int(json.loads(prior)['charged_ns']) if prior else 0
        if not 0 <= charged <= 60000000000:
            raise Refusal('Aggregate budget state invalid')
        BUNDLE.mkdir(parents=True)
        raw_write('build.json', build)
        for bits in (1024, 4096):
            for candidate in sorted(ROUTES):
                for index in (0, 1, 2):
                    for repeat in range(6):
                        if charged+5000000000 > 60000000000:
                            raise Refusal('Aggregate resource ceiling exhausted')
                        save_budget(budget, charged+5000000000)
                        record, elapsed = one_case(build, context, bits, candidate, index, repeat)
                        charged += elapsed
                        save_budget(budget, charged)
                        print(json.dumps({'record_id':record['record_id'], 'valid':record['valid'], 'abort_code':record['abort_code']}), flush=True)
                        if not record['valid']:
                            raise Refusal('Ordered subset stopped at the retained invalid record')
        print('Completed initial route subset. This does not establish a production winner or C1 PASS.', flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status':'refused','reason':str(error) if isinstance(error, Refusal) else 'Subset refused; raw diagnostic suppressed'}))
        sys.exit(1)
