"""Stage: hardware characterization; fixed bounded CEML-CAL-1 arithmetic matrix.

The matrix, sizes, candidates, work budgets and repeat counts are constants of
this file. No seed, start, size, budget or route is accepted from the caller.
Every case is one guarded child that performs one warm-up and five measured
repetitions. The exact reference is computed here with Python integers by
direct standard-map C stepping compared at T boundaries (or an exact Python
product), independently of the native candidate code and of GMP.

Order: family, size ascending, candidate ID ASCII, case index, repeat. The run
stops at the first invalid case and retains it. A stopped run may be resumed
only explicitly, with at most one further attempt per case and five resumed
attempts per run. These are engineering records, not V1 and not science.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import msvcrt
import os
import re
import subprocess
import sys

from engineering_codec import artifact_digest, blob, canonical_bytes, self_test_vector, uenc
from gmp_setup import ROOT, Refusal, hashes
from privacy_gate import I1_BASELINE, inspect_text, parse_json

SEED = bytes(range(32))
DOMAIN = b'CEML-CALIBRATION-RANDOM-V1\0'
CAL1 = ROOT / 'local/c1/cal1'
BUNDLES = ROOT / 'local/c1/benchmark_bundles'
BUDGET = ROOT / 'local/c1/cal1-budget.json'
PRIOR_CHARGED_NS = 80015800          # carried from the initial route-subset budget
AGGREGATE_NS = 900 * 10**9
CASE_NS = 5 * 10**9
MAX_RESUMES = 5
SIZES = (256, 1024, 4096, 16384, 65536, 131072)
FAMILIES = {'route-crossover': 1, 'small-block-sweep': 2, 'hierarchical-sweep': 3, 'backend-multiplication': 4,
            'representation': 5, 'allocation': 6, 'compiler-build': 7, 'terminal-handoff': 10, 'audit-cost': 11,
            'memory-scaling': 12}
HIER_DEFAULT = ('4', '4096')        # labelled harness default for families that do not sweep the scheduler
_VALIDATOR = None


def generated(family, bits, index, stream, odd):
    message = DOMAIN + SEED + blob(family.encode()) + uenc(bits) + uenc(index) + uenc(stream)
    value = int.from_bytes(hashlib.shake_256(message).digest((bits + 7)//8), 'big')
    value &= (1 << bits) - 1
    value |= 1 << (bits - 1)
    return value | 1 if odd else value


def describe(family, bits, index, roles, operands):
    identity = f'cal1/{FAMILIES[family]:02d}/{family}/{bits}/{index}'
    formula = 'formula' in roles[0]
    descriptor = dict(case_index=str(index), family=family,
                      generator='formula-v1' if formula else 'shake256-ceml-calibration-random-v1',
                      input_id=identity, operand_roles=roles, size_bits=str(bits), suite_version='CEML-CAL-1')
    preimage = b'CEML-I1-CALIBRATION-INPUT-V1\0' + blob(canonical_bytes(descriptor))
    for operand in operands:
        preimage += blob(uenc(operand))
    return descriptor, hashlib.sha3_256(preimage).hexdigest()


def state_input(family, bits, index):
    value = generated(family, bits, index, 0, True)
    roles = [dict(forced_odd=True, role='state', size_bits=str(bits), stream_index='0')]
    return (value,), describe(family, bits, index, roles, (value,))


def product_input(bits, index):
    """Indices 0-2, 3-5 and 6-8 use multiplier bit-length ratios 1, 2 and 4."""
    small = bits >> (index//3)
    left = generated('backend-multiplication', bits, index, 0, False)
    right = generated('backend-multiplication', small, index, 1, False)
    roles = [dict(forced_odd=False, role='multiplicand', size_bits=str(bits), stream_index='0'),
             dict(forced_odd=False, role='multiplier', size_bits=str(small), stream_index='1')]
    return (left, right), describe('backend-multiplication', bits, index, roles, (left, right))


def sparse_input(bits, index):
    """Indices 3-5 are formula-defined sparse states; 0-2 are generated dense."""
    if index < 3:
        return state_input('representation', bits, index)
    formulas = {3: ('(2^64-1)*2^(s-64)+(2^64-1)', ((1 << 64) - 1)*(1 << (bits - 64)) + (1 << 64) - 1),
                4: ('2^(s-1)+1', (1 << (bits - 1)) + 1),
                5: ('2^(s-1)+2^(s/2)+3', (1 << (bits - 1)) + (1 << (bits//2)) + 3)}
    text, value = formulas[index]
    return (value,), describe('representation', bits, index, [dict(formula=text + ' with s=' + str(bits), role='state')], (value,))


def terminal_input(exponent, index):
    text, value = (('2^m', 1 << exponent), ('2^m-1', (1 << exponent) - 1), ('2^m+1', (1 << exponent) + 1))[index]
    roles = [dict(formula=text + ' with m=' + str(exponent), role='state')]
    return (value,), describe('terminal-handoff', exponent, index, roles, (value,))


def reference_state(n, budget):
    """Definition oracle: standard map C only, compared at T boundaries."""
    shortcut = odd = standard = 0
    while n != 1 and (budget is None or shortcut < budget):
        if n & 1:
            n = 3*n + 1
            standard += 1
            odd += 1
        n >>= 1
        standard += 1
        shortcut += 1
    assert standard == shortcut + odd
    return n, shortcut, odd


def state_digest(n, shortcut, odd):
    return hashlib.sha3_256(b'CEML-I1-CALIBRATION-STATE-V1\0' + uenc(n) + uenc(shortcut) + uenc(odd)
                            + uenc(shortcut + odd)).hexdigest()


def route_args(route, width='1', divisor='1', cap='1', steps='2016', alloc='reuse', audit='divisibility', mode='fixed'):
    return ['route', route, width, divisor, cap, steps, alloc, audit, mode]


def matrix():
    """Yield (family, size, candidate, index, maker, executable, args, required routes, kind, budget)."""
    rows = []

    def add(family, sizes, candidates, indices, maker, kind='state'):
        for bits in sizes:
            for candidate in sorted(candidates):
                executable, args, required, budget = candidates[candidate]
                for index in indices:
                    rows.append((family, bits, candidate, index, maker, executable, args, required, kind, budget))

    case = 'cal1_case.exe'
    small = {f'affine-small-w{w:02d}': (case, route_args('small', width=str(w)), ['engine.small_affine'], 2016)
             for w in (4, 8, 12, 16)}
    crossover = dict(small)
    crossover['t-direct'] = (case, route_args('direct'), ['engine.direct_t'], 2016)
    for d in (2, 3, 4, 6, 8):
        crossover[f'hier-explicit-d{d}-k04096'] = (case, route_args('hier', divisor=str(d), cap='4096'),
                                                   ['engine.hier_affine.explicit'], 2016)
    add('route-crossover', SIZES[1:], crossover, range(3), lambda b, i: state_input('route-crossover', b, i))
    add('small-block-sweep', (4096, 16384, 65536), small, range(3), lambda b, i: state_input('small-block-sweep', b, i))
    sweep = {f'hier-explicit-d{d}-k{k:05d}': (case, route_args('hier', divisor=str(d), cap=str(k), steps='16384'),
                                              ['engine.hier_affine.explicit'], 16384)
             for d in (2, 3, 4, 6, 8) for k in (1024, 4096, 16384)}
    add('hierarchical-sweep', SIZES[3:], sweep, range(3), lambda b, i: state_input('hierarchical-sweep', b, i))
    add('backend-multiplication', SIZES, {'gmp-mpz-mul': (case, ['mul'], ['arith.gmp.public'], None)}, range(9),
        product_input, 'product')
    add('representation', SIZES[2:], {'dense-gmp': (case, ['repr', '1024', '2016'], ['state.dense'], 2016)}, range(6),
        sparse_input, 'representation')
    d, k = HIER_DEFAULT
    hier = dict(divisor=d, cap=k, steps='16384')
    allocation = {'direct-copy': (case, route_args('direct', alloc='copy'), ['engine.direct_t', 'alloc.copy'], 2016),
                  'direct-reuse': (case, route_args('direct'), ['engine.direct_t', 'alloc.reuse'], 2016),
                  'hier-copy': (case, route_args('hier', alloc='copy', **hier), ['engine.hier_affine.explicit', 'alloc.copy'], 16384),
                  'hier-reuse': (case, route_args('hier', **hier), ['engine.hier_affine.explicit', 'alloc.reuse'], 16384)}
    add('allocation', SIZES[3:], allocation, range(3), lambda b, i: state_input('allocation', b, i))
    builds = {'build-checked': ('cal1_case_checked.exe', route_args('hier', **hier), ['engine.hier_affine.explicit'], 16384),
              'build-portable-release': (case, route_args('hier', **hier), ['engine.hier_affine.explicit'], 16384)}
    add('compiler-build', SIZES[3:], builds, range(3), lambda b, i: state_input('compiler-build', b, i))
    terminal = {'terminal-direct-t': (case, route_args('hier', divisor='2', cap='1024', steps='1', mode='terminal-t'),
                                      ['engine.hier_affine.explicit', 'terminal.direct_t'], None),
                'terminal-odd-only': (case, route_args('hier', divisor='2', cap='1024', steps='1', mode='terminal-u'),
                                      ['engine.hier_affine.explicit', 'terminal.odd_only'], None)}
    add('terminal-handoff', (8, 64, 256, 1024, 4096), terminal, range(3), terminal_input)
    audit = {'audit-divisibility': (case, route_args('hier', **hier), ['engine.hier_affine.explicit', 'audit.divisibility'], 16384),
             'audit-divisibility-modular': (case, route_args('hier', audit='modular', **hier),
                                            ['engine.hier_affine.explicit', 'audit.divisibility', 'audit.modular'], 16384),
             'audit-structural': (case, route_args('hier', audit='structural', **hier), ['engine.hier_affine.explicit'], 16384)}
    add('audit-cost', SIZES[3:], audit, range(3), lambda b, i: state_input('audit-cost', b, i))
    memory = {'mem-direct-t': (case, route_args('direct', steps='512'), ['engine.direct_t'], 512),
              'mem-hier-d2-k16384': (case, route_args('hier', divisor='2', cap='16384', steps='512'), ['engine.hier_affine.explicit'], 512),
              'mem-small-w04': (case, route_args('small', width='4', steps='512'), ['engine.small_affine'], 512),
              'mem-small-w16': (case, route_args('small', width='16', steps='512'), ['engine.small_affine'], 512)}
    add('memory-scaling', SIZES, memory, range(3), lambda b, i: state_input('memory-scaling', b, i))
    return rows


def validator():
    global _VALIDATOR
    if _VALIDATOR is None:
        from jsonschema import Draft202012Validator
        schema = parse_json(subprocess.check_output(
            ['git', '-C', str(ROOT), 'show', I1_BASELINE + ':schemas/c1_evidence.schema.json']).decode('utf-8'))
        _VALIDATOR = Draft202012Validator(schema)
    return _VALIDATOR


def write(folder, name, obj):
    data = canonical_bytes(obj)
    if inspect_text(data.decode('ascii'), name):
        raise Refusal('Evidence privacy check failed')
    (folder / name).write_bytes(data)


def build_context(build, commit, executable, thread_note):
    flags = build['artifacts'][executable]['flags']
    return dict(source_commit=commit, target_triple=build['toolchain']['target'], abi=build['toolchain']['abi'],
                toolchains=[{'name': 'MSVC tools', 'version': build['toolchain']['msvc_tools_version']},
                            {'name': 'Windows SDK', 'version': build['toolchain']['windows_sdk_version']}],
                flags=flags + ['-link', '-Brepro'],
                dependencies=[{'name': 'GMP', 'version': '6.3.0-2', 'linkage': 'dynamic-public-C', 'features': ['mpz']}],
                enabled_features=['bounded-engineering-only', 'python-definition-C-reference', 'in-process-warmup-plus-five'],
                process_count='1', thread_count='1', affinity=thread_note)


def evaluate(row, operands, parsed):
    """Return (candidate digest, reference digest, agreement) from exact integers only."""
    family, bits, candidate, index, maker, executable, args, required, kind, budget = row
    if kind == 'product':
        expected = operands[0]*operands[1]
        actual = int(parsed['n_hex'], 16)
        return state_digest(actual, 0, 0), state_digest(expected, 0, 0), actual == expected
    n, shortcut, odd = reference_state(operands[0], budget)
    actual = (int(parsed['n_hex'], 16), int(parsed['shortcut_steps']), int(parsed['odd_steps']))
    agreement = actual == (n, shortcut, odd) and int(parsed['standard_steps']) == actual[1] + actual[2]
    agreement &= parsed['terminal_reached'] == (n == 1)
    if kind == 'representation':
        exported = bytes.fromhex(parsed['export_hex'])
        agreement &= blob(exported) == uenc(operands[0])
        agreement &= int(parsed['low_bits_hex'], 16) == operands[0] % (1 << 1024)
    return state_digest(*actual), state_digest(n, shortcut, odd), agreement


def one_case(row, folder, build, commit, attempt):
    family, bits, candidate, index, maker, executable, args, required, kind, budget = row
    operands, (descriptor, input_digest) = maker(bits, index)
    binaries = CAL1 / 'bin'
    for name in (executable, 'cal1_guard.exe'):
        if hashes((binaries / name).read_bytes()) != build['artifacts'][name]['executable']:
            raise Refusal('Calibration executable changed')
    if hashes((binaries / 'libgmp-10.dll').read_bytes()) != build['dependency']:
        raise Refusal('Calibration dependency changed')
    stdin = ''.join(format(x, 'x') + '\n' for x in operands).encode('ascii')
    process = subprocess.run([str(binaries / 'cal1_guard.exe'), executable, *args], cwd=binaries, input=stdin,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    if len(process.stdout) > 400000 or process.stderr:
        raise Refusal('Unexpected calibration output')
    lines = [json.loads(line) for line in process.stdout.splitlines() if line]
    guards = [x for x in lines if x.get('kind') == 'guard']
    states = [x for x in lines if x.get('kind') == 'candidate']
    if len(guards) != 1 or len(states) > 1:
        raise Refusal('Required guarded outcome unavailable')
    guard, parsed = guards[0], states[0] if states else None
    abort = guard['abort_code']
    digest = reference = '0'*64
    agreement = False
    counts = {route: '0' for route in required}
    fallback = '0'
    if parsed:
        digest, reference, agreement = evaluate(row, operands, parsed)
        agreement &= parsed['repeats_identical']
        counts = parsed['activated']
        fallback = parsed['fallback_count']
        if abort is None and not agreement:
            abort = 'C1_CORRECTNESS_INVALID'
        elif abort is None and (fallback != '0' or any(int(counts.get(route, '0')) <= 0 for route in required)):
            abort = 'C1_ROUTE_INVALID'
    elif abort is None:
        abort = 'C1_MEASUREMENT_INVALID'
    if abort is None and process.returncode:
        abort = 'C1_MEASUREMENT_INVALID'
    activation = dict(requested_routes=required, activated_counts=counts, fallback_count=fallback)
    activation['route_evidence_digest'] = hashlib.sha3_256(canonical_bytes(activation)).hexdigest()
    case_id = descriptor['input_id'] + '/' + candidate
    stem = f'{bits:06d}-{candidate}-{index}-a{attempt}'
    context = build_context(build, commit, executable, 'One allowed logical processor; lowest set bit of inherited process affinity')
    pressure = ('PDH pages input/output over intervals of at least one second; intervals=' + guard.get('pressure_intervals', '0')
                + '; input excursions above 100=' + guard.get('pages_input_excursion_intervals', '0')
                + '; maximum input rounded=' + guard.get('maximum_pages_input_rounded', '0') + '; output required zero')
    performance = guard.get('minimum_processor_performance_percent')
    frequency = ('PDH processor performance percent of nominal; minimum over case intervals=' + performance
                 if performance else 'Processor performance counter unavailable')
    records = []
    for repeat in range(6):
        sample = parsed['repeats'][repeat] if parsed else None
        ok = abort is None
        record = dict(
            experiment='CEML', schema_version='CEML-CALIBRATION-RECORD-1', record_class='CALIBRATION_MEASUREMENT',
            record_id=f'cal1.{FAMILIES[family]:02d}.{bits}.{candidate}.{index}.a{attempt}.r{repeat}',
            suite_version='CEML-CAL-1', case_id=case_id, input_id=descriptor['input_id'], input_digest=input_digest,
            candidate_id=candidate, build_id='c1-cal1-' + build['artifacts'][executable]['executable']['sha3_256'][:16],
            executable_digest=build['artifacts'][executable]['executable']['sha3_256'], build_context=context,
            wall_clock_method='QueryPerformanceCounter around the candidate kernel of one repetition; integer floor to nanoseconds',
            cpu_time_method='GetProcessTimes delta of the single-threaded child across one repetition; 100 ns units, coarse scheduler granularity',
            peak_rss_method='GetProcessMemoryInfo PeakWorkingSetSize of the child, cumulative through this repetition; bytes',
            artifact_digests=sorted({build['artifacts'][name][part]['sha3_256'] for name in (executable, 'cal1_guard.exe')
                                     for part in ('source', 'executable')} | {build['dependency']['sha3_256'], build['pin']['sha3_256'],
                                                                             build['driver']['sha3_256']}),
            repeat_index=str(repeat), warmup=repeat == 0, measured=repeat != 0, activation=activation,
            wall_time_ns=str(int(sample['ticks'])*10**9//int(parsed['qpc_frequency'])) if sample else None,
            cpu_time_ns=sample['cpu_ns'] if sample and ok else None,
            peak_rss_bytes=sample['peak_working_set_bytes'] if sample and ok else None,
            live_bytes=sample['peak_live_bytes'] if sample and ok else None, scratch_bytes='0',
            swap_observation=pressure, thermal_observation='Temperature unavailable; ' + frequency,
            frequency_observation=frequency, checkpoint_metrics=None,
            correctness_state_digest=digest, reference_state_digest=reference, correctness_agreement=bool(agreement),
            valid=ok, invalid_reason=None if ok else guard.get('reason') if guard.get('reason', 'none') != 'none' else abort,
            abort_code=abort)
        record['artifact_digest'] = artifact_digest(record)
        if not validator().is_valid(record):
            raise Refusal('Calibration schema check failed')
        write(folder, f'{stem}-r{repeat}-record.json', record)
        records.append(record)
    write(folder, f'{stem}-detail.json', dict(descriptor=descriptor, guard=guard, candidate=parsed, child_arguments=args,
                                              executable=executable, attempt=str(attempt)))
    charged = 0 if abort == 'C1_PREFLIGHT_REFUSAL' else int(guard.get('process_wall_ticks', '0'))*10**9//int(guard.get('qpc_frequency', '1'))
    if abort != 'C1_PREFLIGHT_REFUSAL' and not 0 < charged <= CASE_NS:
        charged = CASE_NS
    return abort, charged


def save_budget(handle, value, resumes):
    handle.seek(0)
    handle.write(json.dumps({'charged_ns': str(value), 'resumed_attempts': resumes}).encode())
    handle.truncate()
    handle.flush()
    os.fsync(handle.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--family', required=True, choices=sorted(FAMILIES, key=FAMILIES.get))
    parser.add_argument('--resume-after-refusal', action='store_true')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,40}', args.run_id):
        raise Refusal('Run ID must contain only lowercase letters, digits and hyphens')
    vector = self_test_vector()
    value, (descriptor, digest) = state_input('route-crossover', 256, 0)
    if digest != vector['input_digest'] or state_digest(value[0], 0, 0) != vector['initial_state_digest']:
        raise Refusal('Normative generator vector not reproduced')
    rows = [row for row in matrix() if row[0] == args.family]
    if args.list:
        print(json.dumps({'family': args.family, 'children': len(rows)}))
        return
    build = json.loads((CAL1 / 'build.json').read_text())
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    for name, meta in build['committed_sources'].items():
        if hashes(subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)) != meta:
            raise Refusal('Calibration sources must be committed unchanged before measurement')
    folder = BUNDLES / f'{args.run_id}-{FAMILIES[args.family]:02d}-{args.family}'
    with os.fdopen(os.open(BUDGET, os.O_RDWR | os.O_CREAT, 0o600), 'r+b') as budget:
        msvcrt.locking(budget.fileno(), msvcrt.LK_NBLCK, 1)
        budget.seek(0)
        prior = budget.read(1024)
        state = json.loads(prior) if prior else {'charged_ns': str(PRIOR_CHARGED_NS), 'resumed_attempts': {}}
        charged, resumes = int(state['charged_ns']), state['resumed_attempts']
        if not PRIOR_CHARGED_NS <= charged <= AGGREGATE_NS:
            raise Refusal('Aggregate budget state invalid')
        if folder.exists() and not args.resume_after_refusal:
            raise Refusal('Existing family evidence retained; resume must be explicit')
        folder.mkdir(parents=True, exist_ok=True)
        if not (folder / 'build.json').exists():
            write(folder, 'build.json', build)
        elif (folder / 'build.json').read_bytes() != canonical_bytes(build):
            raise Refusal('Build identity changed inside one family bundle')
        for row in rows:
            family, bits, candidate, index = row[:4]
            prefix = f'{bits:06d}-{candidate}-{index}-a'
            attempts = sorted(folder.glob(prefix + '*-detail.json'))
            if attempts:
                last = json.loads((folder / attempts[-1].name.replace('-detail', '-r1-record')).read_text())
                if last['valid']:
                    continue
                if len(attempts) >= 2:
                    raise Refusal('Case refused twice; family remains without a valid measurement')
                if resumes.get(args.run_id, 0) >= MAX_RESUMES:
                    raise Refusal('Resume allowance for this run exhausted')
                resumes[args.run_id] = resumes.get(args.run_id, 0) + 1
            if charged + CASE_NS > AGGREGATE_NS:
                raise Refusal('Aggregate resource ceiling exhausted')
            save_budget(budget, charged + CASE_NS, resumes)
            abort, elapsed = one_case(row, folder, build, commit, len(attempts) + 1)
            charged += elapsed
            save_budget(budget, charged, resumes)
            print(json.dumps({'case': f'{family}/{bits}/{candidate}/{index}', 'abort_code': abort}), flush=True)
            if abort is not None:
                raise Refusal('Ordered family stopped at the retained invalid case')
    print(json.dumps({'status': 'ok', 'family': args.family, 'children': len(rows)}), flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'refused', 'reason': str(error) if isinstance(error, Refusal) else 'Suite refused; raw diagnostic suppressed'}))
        sys.exit(1)
