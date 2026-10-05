"""Stage: hardware characterization; bounded synthetic CEML-CKPT-1 filesystem tests.

Two fixed commands, no free parameters beyond a run ID:

  matrix       forced process interruption at every materially distinct write,
               flush, promotion, pointer and retirement boundary, followed by
               fresh-process recovery and fresh-process continuation, plus
               pointer-distrust, corruption, ambiguity and provenance cases;
  performance  CEML-CAL-1 family 09 timing of the buffered and streaming
               serialization strategies through the resource guard.

Every expected byte and digest is recomputed here by an independent Python
implementation of the frozen encodings. All states and identities are
synthetic and labelled non-scientific. Process interruption does not test
power loss; no power-cut test is performed or claimed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import msvcrt
import os
import re
import shutil
import subprocess
import sys

from engineering_codec import artifact_digest, blob, canonical_bytes, uenc
from gmp_setup import ROOT, Refusal, hashes
from privacy_gate import I1_BASELINE, inspect_text, parse_json

SEED = bytes(range(32))
DOMAIN = b'CEML-CALIBRATION-RANDOM-V1\0'
CAL1 = ROOT / 'local/c1/cal1'
WORK = ROOT / 'local/c1/ckpt-work'
BUNDLES = ROOT / 'local/c1/benchmark_bundles'
BUDGET = ROOT / 'local/c1/cal1-budget.json'
AGGREGATE_NS = 900 * 10**9
CASE_NS = 5 * 10**9
STRATEGIES = {'buffered': 'checkpoint.buffered', 'streaming': 'checkpoint.streaming'}
PRE_PUBLICATION = ('body-partial', 'body-complete', 'metadata-partial', 'metadata-complete-before-flush',
                   'after-flush-before-verify', 'after-verify-before-promote')
POST_PUBLICATION = ('after-promote-before-dirsync', 'pointer-temp-written', 'after-pointer-promote',
                    'published-before-retire', 'retire-renamed', 'retire-partial', 'complete-before-exit')
R4_PHASES = {'body-partial': 'before body completion',
             'body-complete': 'between body and metadata completion',
             'metadata-partial': 'between body and metadata completion',
             'metadata-complete-before-flush': 'before durable file flush',
             'after-flush-before-verify': 'after file flush but before promotion',
             'after-verify-before-promote': 'during or around promotion (immediately before the rename)',
             'after-promote-before-dirsync': 'after promotion but before the directory or pointer durability step',
             'pointer-temp-written': 'after promotion but before the directory or pointer durability step',
             'after-pointer-promote': 'after promotion but before the directory or pointer durability step',
             'published-before-retire': 'during cleanup or retirement of the older slot',
             'retire-renamed': 'during cleanup or retirement of the older slot',
             'retire-partial': 'during cleanup or retirement of the older slot',
             'complete-before-exit': 'during cleanup or retirement of the older slot'}


def digest(label, data):
    return hashlib.sha3_256(label.encode('ascii') + b'\0' + data).hexdigest()


def synthetic(field):
    return hashlib.sha3_256(('C1-SYNTHETIC-NONSCIENTIFIC-' + field).encode('ascii')).hexdigest()


def identity(run_id, commit):
    return dict(run_id='c1-synthetic-' + run_id, manifest_digest=synthetic('manifest'),
                original_start_digest=synthetic('start'), protocol_commit=I1_BASELINE, engine_commit=commit,
                build_digest=synthetic('build'), machine_profile_digest=synthetic('profile'),
                validation_evidence_digest=synthetic('validation'))


def generated(bits, index, stream, odd):
    message = DOMAIN + SEED + blob(b'checkpoint') + uenc(bits) + uenc(index) + uenc(stream)
    value = int.from_bytes(hashlib.shake_256(message).digest((bits + 7)//8), 'big')
    value &= (1 << bits) - 1
    value |= 1 << (bits - 1)
    return value | 1 if odd else value


def checkpoint_input(magnitude_bytes, index):
    """Synthetic state with an exact magnitude size. The 32 KiB class joins two
    generated operands so that no generated operand exceeds 131072 bits."""
    bits = 8*magnitude_bytes
    if bits <= 131072:
        operands = (generated(bits, index, 0, True),)
        roles = [dict(forced_odd=True, role='state', size_bits=str(bits), stream_index='0')]
        value = operands[0]
    else:
        operands = (generated(131072, index, 0, False), generated(131072, index, 1, True))
        roles = [dict(forced_odd=False, role='state-high-half', size_bits='131072', stream_index='0'),
                 dict(forced_odd=True, role='state-low-half', size_bits='131072', stream_index='1')]
        value = (operands[0] << 131072) | operands[1]
    name = f'cal1/09/checkpoint/{bits}/{index}'
    descriptor = dict(case_index=str(index), family='checkpoint', generator='shake256-ceml-calibration-random-v1',
                      input_id=name, operand_roles=roles, size_bits=str(bits), suite_version='CEML-CAL-1')
    preimage = b'CEML-I1-CALIBRATION-INPUT-V1\0' + blob(canonical_bytes(descriptor))
    for operand in operands:
        preimage += blob(uenc(operand))
    return value, descriptor, hashlib.sha3_256(preimage).hexdigest()


def body_bytes(n):
    return b'CEML-CKPT-BODY-V1\0' + uenc(n)


def metadata_object(ident, sequence, previous, n, shortcut, odd):
    body = body_bytes(n)
    meta = dict(schema_version='CEML-CHECKPOINT-METADATA-1', checkpoint_format_version='CEML-CKPT-1',
                run_id=ident['run_id'], sequence=str(sequence), previous_metadata_digest=previous,
                manifest_digest=ident['manifest_digest'], original_start_digest=ident['original_start_digest'],
                protocol_version='CEML-SCI-1', protocol_commit=ident['protocol_commit'],
                engine_commit=ident['engine_commit'], build_digest=ident['build_digest'],
                machine_profile_digest=ident['machine_profile_digest'],
                validation_evidence_digest=ident['validation_evidence_digest'], map_semantics_version='CEML-COLLATZ-1',
                body_bytes=str(len(body)), body_digest=digest('CEML-CHECKPOINT-BODY-DIGEST-V1', body),
                current_value_digest=digest('CEML-CHECKPOINT-CURRENT-V1', uenc(n)), shortcut_steps=str(shortcut),
                odd_steps=str(odd), standard_steps=str(shortcut + odd), terminal_reached=n == 1)
    meta['metadata_digest'] = digest('CEML-CHECKPOINT-METADATA-V1', canonical_bytes(meta))
    return meta


_SCHEMA = None


def schema_valid(meta):
    global _SCHEMA
    if _SCHEMA is None:
        from jsonschema import Draft202012Validator
        _SCHEMA = Draft202012Validator(parse_json(subprocess.check_output(
            ['git', '-C', str(ROOT), 'show', I1_BASELINE + ':schemas/checkpoint_metadata.schema.json']).decode('utf-8')))
    return _SCHEMA.is_valid(meta)


def frozen_vector():
    body = body_bytes(1)
    if body.hex() != '43454d4c2d434b50542d424f44592d563100000000000000000101' or digest(
            'CEML-CHECKPOINT-BODY-DIGEST-V1', body) != '181ce6b5c4488f56cac3a7439cf6c42048d03b195e3f0b21bf37f6c59f285a9f':
        raise Refusal('Frozen checkpoint body vector not reproduced')


def stdin_for(directory, ident, state=None):
    lines = [directory, ident['run_id'], ident['manifest_digest'], ident['original_start_digest'], ident['protocol_commit'],
             ident['engine_commit'], ident['build_digest'], ident['machine_profile_digest'], ident['validation_evidence_digest']]
    if state:
        lines += [format(state[0], 'x'), str(state[1]), str(state[2])]
    return ''.join(x + '\n' for x in lines).encode('ascii')


def launch(arguments, stdin, guarded=False):
    """One fresh process per call. Returns (exit code, parsed JSON lines)."""
    binaries = CAL1 / 'bin'
    command = [str(binaries / 'cal1_guard.exe'), 'ckpt_case.exe'] if guarded else [str(binaries / 'ckpt_case.exe'), '--calibration-only']
    process = subprocess.run(command + arguments, cwd=WORK, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=30)
    if process.stderr or len(process.stdout) > 400000:
        raise Refusal('Unexpected checkpoint tool output')
    return process.returncode, [json.loads(x) for x in process.stdout.splitlines() if x]


def promote(directory, ident, state, strategy='buffered', fault='none'):
    code, lines = launch(['promote', strategy, fault, '1'], stdin_for(directory, ident, state))
    return code, (lines[0] if lines else None)


def recover(directory, ident):
    code, lines = launch(['recover', 'none', 'none', '1'], stdin_for(directory, ident))
    return code, lines[0]


def inspect_store(directory, ident, states):
    """Independent byte-level validation of every published generation."""
    folder = WORK / directory
    published, temporary = {}, []
    for entry in sorted(os.listdir(folder)):
        if entry.endswith('.tmp'):
            temporary.append(entry)
        elif re.fullmatch(r'gen-(0|[1-9][0-9]*)', entry):
            sequence = int(entry[4:])
            n, shortcut, odd = states[sequence]
            previous = published[sequence - 1]['metadata_digest'] if sequence - 1 in published else None
            body = (folder / entry / 'state.bin').read_bytes()
            raw = (folder / entry / 'metadata.json').read_bytes()
            meta = parse_json(raw.decode('ascii'))
            expected = metadata_object(ident, sequence, meta['previous_metadata_digest'], n, shortcut, odd)
            exact = (body == body_bytes(n) and raw == canonical_bytes(expected) and schema_valid(meta)
                     and (previous is None or meta['previous_metadata_digest'] == previous)
                     and (sequence == 0) == (meta['previous_metadata_digest'] is None))
            published[sequence] = dict(exact=exact, metadata_digest=meta['metadata_digest'])
    return published, temporary


def state_for(sequence):
    value, _, _ = checkpoint_input(1024, sequence % 3)
    return value, 1000*(sequence + 1), 400*(sequence + 1)


def matrix_scenario(run_id, ident, strategy, phase, existing):
    directory = f'{run_id}\\m-{strategy}-{phase}-{existing}'
    (WORK / directory).mkdir(parents=True)
    states = {i: state_for(i) for i in range(existing + 3)}
    outcome = dict(strategy=STRATEGIES[strategy], phase=phase, r4_phase=R4_PHASES[phase],
                   existing_generations=str(existing), checks={})
    checks = outcome['checks']
    for sequence in range(existing):
        code, _ = promote(directory, ident, states[sequence], strategy)
        checks[f'setup-{sequence}'] = code == 0
    code, _ = promote(directory, ident, states[existing], strategy, phase)
    reached = code == 99
    outcome['interruption'] = 'forced-termination' if reached else 'boundary-not-reached'
    checks['writer-terminated-or-completed'] = code in (0, 99)
    published_expected = existing if (not reached or phase in POST_PUBLICATION) else existing - 1
    code, report = recover(directory, ident)
    outcome['recovery_after_interruption'] = {k: report[k] for k in ('status', 'valid_generations', 'invalid_generations',
                                                                      'temporary_entries', 'pointer')}
    if published_expected < 0:
        checks['fresh-recovery-reports-empty'] = report['status'] == 'empty' and code == 0
    else:
        n, shortcut, odd = states[published_expected]
        checks['fresh-recovery-selects-exact-state'] = (
            report['status'] == 'selected' and report['sequence'] == str(published_expected)
            and int(report['n_hex'], 16) == n and report['shortcut_steps'] == str(shortcut)
            and report['odd_steps'] == str(odd) and report['standard_steps'] == str(shortcut + odd))
    published, temporary = inspect_store(directory, ident, states)
    outcome['published_after_interruption'] = sorted(str(x) for x in published)
    outcome['temporary_after_interruption'] = str(len(temporary))
    checks['no-partial-or-inexact-generation-published'] = all(x['exact'] for x in published.values()) and report['invalid_generations'] == '0'
    if published_expected >= 0:
        checks['selected-digest-matches-independent-encoding'] = report.get('metadata_digest') == published[published_expected]['metadata_digest']
    if existing >= 1:
        checks['previous-validated-generation-retained'] = (existing - 1) in published and published[existing - 1]['exact']
    # Fresh-process continuation: the next promotion must succeed and chain correctly.
    following = published_expected + 1
    code, _ = promote(directory, ident, states[following], strategy)
    checks['fresh-process-continuation-succeeds'] = code == 0
    code, report = recover(directory, ident)
    n, shortcut, odd = states[following]
    published, temporary = inspect_store(directory, ident, states)
    checks['continuation-selected-exactly'] = (report['status'] == 'selected' and report['sequence'] == str(following)
                                              and int(report['n_hex'], 16) == n and report['pointer'] == 'agrees'
                                              and report['temporary_entries'] == '0' and not temporary
                                              and all(x['exact'] for x in published.values()))
    checks['two-generations-retained-after-continuation'] = (following == 0 and sorted(published) == [0]) or \
        sorted(published) == [following - 1, following]
    if following >= 1:
        checks['chain-links-to-previous'] = report.get('previous_metadata_digest') == published[following - 1]['metadata_digest']
    outcome['passed'] = all(checks.values())
    return outcome


def adversarial(run_id, ident):
    """Recovery must rely on slot contents: pointer distrust, corruption, ambiguity, provenance."""
    results = []
    states = {i: state_for(i) for i in range(4)}

    def fresh(name, generations=3):
        directory = f'{run_id}\\a-{name}'
        (WORK / directory).mkdir(parents=True)
        for sequence in range(generations):
            if promote(directory, ident, states[sequence])[0] != 0:
                raise Refusal('Adversarial setup failed')
        return directory

    def record(name, directory, expectation, passed, report):
        results.append(dict(case=name, expectation=expectation, passed=bool(passed),
                            recovery={k: report.get(k) for k in ('status', 'sequence', 'valid_generations',
                                                                 'invalid_generations', 'pointer')}))

    d = fresh('pointer-missing')
    os.remove(WORK / d / 'latest')
    code, r = recover(d, ident)
    record('pointer-missing', d, 'newest valid generation selected without a pointer',
           r['status'] == 'selected' and r['sequence'] == '2' and r['pointer'] == 'absent', r)
    d = fresh('pointer-garbage')
    (WORK / d / 'latest').write_bytes(b'gen-999 ' + b'0'*64 + b'\n')
    code, r = recover(d, ident)
    record('pointer-garbage', d, 'pointer ignored; newest valid generation selected',
           r['status'] == 'selected' and r['sequence'] == '2' and r['pointer'] == 'ignored', r)
    d = fresh('pointer-stale')
    older = parse_json((WORK / d / 'gen-1' / 'metadata.json').read_text('ascii'))['metadata_digest']
    (WORK / d / 'latest').write_bytes(('gen-1 ' + older + '\n').encode('ascii'))
    code, r = recover(d, ident)
    record('pointer-stale', d, 'pointer naming the older valid generation is ignored',
           r['status'] == 'selected' and r['sequence'] == '2' and r['pointer'] == 'ignored', r)
    for name, target, mutate in (
            ('newest-body-bit-flip', 'state.bin', lambda b: b[:40] + bytes([b[40] ^ 1]) + b[41:]),
            ('newest-body-truncated', 'state.bin', lambda b: b[:-1]),
            ('newest-body-trailing-byte', 'state.bin', lambda b: b + b'\0'),
            ('newest-metadata-counter-edit', 'metadata.json', lambda b: b.replace(b'"odd_steps":"1200"', b'"odd_steps":"1201"')),
            ('newest-metadata-noncanonical-space', 'metadata.json', lambda b: b.replace(b'{"', b'{ "', 1)),
            ('newest-metadata-missing', 'metadata.json', None)):
        d = fresh(name)
        path = WORK / d / 'gen-2' / target
        if mutate is None:
            os.remove(path)
        else:
            original = path.read_bytes()
            changed = mutate(original)
            if changed == original:
                raise Refusal('Adversarial mutation did not apply')
            path.write_bytes(changed)
        code, r = recover(d, ident)
        record(name, d, 'corrupt newest generation is refused, never accepted and never silently replaced',
               r['status'] == 'integrity-refusal' and code != 0, r)
    d = fresh('older-body-bit-flip')
    path = WORK / d / 'gen-1' / 'state.bin'
    original = path.read_bytes()
    path.write_bytes(original[:40] + bytes([original[40] ^ 1]) + original[41:])
    code, r = recover(d, ident)
    record('older-body-bit-flip', d, 'valid newest generation still selected; the corrupt older one is counted, not used',
           r['status'] == 'selected' and r['sequence'] == '2' and r['invalid_generations'] == '1', r)
    d = fresh('chain-break')
    other = f'{run_id}\\a-chain-break-donor'
    (WORK / other).mkdir(parents=True)
    promote(other, ident, states[3])                       # a different valid sequence-0 state
    promote(other, ident, states[0])                       # a valid sequence-1 generation with another history
    shutil.rmtree(WORK / d / 'gen-1')
    shutil.copytree(WORK / other / 'gen-1', WORK / d / 'gen-1')
    code, r = recover(d, ident)
    record('chain-break', d, 'previous-digest mismatch between two valid generations is refused as ambiguous',
           r['status'] == 'ambiguity-refusal' and code != 0, r)
    d = fresh('foreign-identity')
    stranger = dict(ident, manifest_digest=synthetic('another-manifest'))
    code, r = recover(d, stranger)
    record('foreign-identity', d, 'generation bound to another manifest identity is refused',
           r['status'] == 'provenance-refusal' and code != 0, r)
    d = f'{run_id}\\a-terminal-state'
    (WORK / d).mkdir(parents=True)
    promote(d, ident, (1, 70, 41))
    code, r = recover(d, ident)
    raw = parse_json((WORK / d / 'gen-0' / 'metadata.json').read_text('ascii'))
    record('terminal-state', d, 'current value 1 is stored with terminal_reached true and recovered exactly',
           r['status'] == 'selected' and r['n_hex'] == '1' and r['terminal_reached'] is True
           and raw == metadata_object(ident, 0, None, 1, 70, 41), r)
    return results


def write(folder, name, obj):
    data = canonical_bytes(obj)
    if inspect_text(data.decode('ascii'), name):
        raise Refusal('Evidence privacy check failed')
    (folder / name).write_bytes(data)


def prepare(run_id, suffix):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,40}', run_id):
        raise Refusal('Run ID must contain only lowercase letters, digits and hyphens')
    frozen_vector()
    build = json.loads((CAL1 / 'ckpt_build.json').read_text())
    for name, meta in build['committed_sources'].items():
        if hashes(subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)) != meta:
            raise Refusal('Checkpoint sources must be committed unchanged before the tests')
    for name in ('ckpt_case.exe', 'cal1_guard.exe'):
        if hashes((CAL1 / 'bin' / name).read_bytes()) != build['executables'][name]:
            raise Refusal('Checkpoint executable changed')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    folder = BUNDLES / f'{run_id}-09-checkpoint-{suffix}'
    if folder.exists() or (WORK / (run_id + '-' + suffix)).exists():
        raise Refusal('Existing checkpoint evidence retained; no overwrite or repeat')
    WORK.mkdir(parents=True, exist_ok=True)
    code = subprocess.run([str(CAL1 / 'bin' / 'cal1_guard.exe'), '--pressure-check'], cwd=WORK, stdout=subprocess.PIPE).returncode
    if code != 0:
        raise Refusal('Resource preflight refused')
    folder.mkdir(parents=True)
    write(folder, 'build.json', build)
    return build, commit, folder


def run_matrix(run_id):
    build, commit, folder = prepare(run_id, 'durability')
    work_id = run_id + '-durability'
    ident = identity(work_id, commit)
    scenarios = []
    for strategy in sorted(STRATEGIES):
        for phase in PRE_PUBLICATION + POST_PUBLICATION:
            for existing in (0, 1, 2):
                outcome = matrix_scenario(work_id, ident, strategy, phase, existing)
                scenarios.append(outcome)
                write(folder, f'matrix-{strategy}-{phase}-{existing}.json', outcome)
    hostile = adversarial(work_id, ident)
    write(folder, 'adversarial.json', dict(cases=hostile))
    _, capability = recover(f'{work_id}\\a-pointer-missing', ident)
    reached = [x for x in scenarios if x['interruption'] == 'forced-termination']
    summary = dict(
        purpose='non-scientific synthetic CEML-CKPT-1 interruption and recovery matrix',
        filesystem_target='repository checkpoint filesystem (same volume as the intended checkpoint directory)',
        source_commit=commit, scenarios=str(len(scenarios)), forced_terminations=str(len(reached)),
        boundary_not_reached=str(len(scenarios) - len(reached)),
        scenarios_passed=str(sum(x['passed'] for x in scenarios)),
        adversarial_cases=str(len(hostile)), adversarial_passed=str(sum(x['passed'] for x in hostile)),
        phases_forced={phase: str(sum(1 for x in reached if x['phase'] == phase)) for phase in PRE_PUBLICATION + POST_PUBLICATION},
        r4_phase_map=R4_PHASES, directory_flush_supported=capability['directory_flush_supported'],
        all_passed=all(x['passed'] for x in scenarios) and all(x['passed'] for x in hostile),
        limitation='Forced process termination only. No power-loss, device-cache or operating-system crash behaviour was tested.')
    write(folder, 'summary.json', summary)
    shutil.rmtree(WORK / work_id)          # reproducible synthetic files; digests and outcomes are retained
    print(json.dumps({k: summary[k] for k in ('scenarios', 'forced_terminations', 'scenarios_passed', 'adversarial_cases',
                                              'adversarial_passed', 'directory_flush_supported', 'all_passed')}))
    return 0 if summary['all_passed'] else 1


def run_performance(run_id):
    from cal1_suite import validator
    build, commit, folder = prepare(run_id, 'performance')
    work_id = run_id + '-performance'
    ident = identity(work_id, commit)
    context = dict(source_commit=commit, target_triple=build['toolchain']['target'], abi=build['toolchain']['abi'],
                   toolchains=[{'name': 'MSVC tools', 'version': build['toolchain']['msvc_tools_version']},
                               {'name': 'Windows SDK', 'version': build['toolchain']['windows_sdk_version']}],
                   flags=build['flags'] + ['-link', '-Brepro'],
                   dependencies=[{'name': 'GMP', 'version': '6.3.0-2', 'linkage': 'dynamic-public-C', 'features': ['mpz']}],
                   enabled_features=['bounded-engineering-only', 'synthetic-checkpoint-states', 'python-independent-codec'],
                   process_count='1', thread_count='1',
                   affinity='One allowed logical processor; lowest set bit of inherited process affinity')
    with os.fdopen(os.open(BUDGET, os.O_RDWR), 'r+b') as budget:
        msvcrt.locking(budget.fileno(), msvcrt.LK_NBLCK, 1)
        budget.seek(0)
        state = json.loads(budget.read(1024))
        charged = int(state['charged_ns'])
        for magnitude in (1024, 4096, 16384, 32768):
            for strategy in sorted(STRATEGIES):
                for index in range(3):
                    if charged + CASE_NS > AGGREGATE_NS:
                        raise Refusal('Aggregate resource ceiling exhausted')
                    n, descriptor, input_digest = checkpoint_input(magnitude, index)
                    counters = (1000*(index + 1), 400*(index + 1))
                    directory = f'{work_id}\\p-{magnitude}-{strategy}-{index}'
                    (WORK / directory).mkdir(parents=True)
                    code, lines = launch(['promote', strategy, 'none', '4'], stdin_for(directory, ident, (n, *counters)), guarded=True)
                    guards = [x for x in lines if x.get('kind') == 'guard']
                    results = [x for x in lines if x.get('kind') == 'promote']
                    if len(guards) != 1:
                        raise Refusal('Required guarded outcome unavailable')
                    guard, result = guards[0], results[0] if results else None
                    abort = guard['abort_code']
                    charged += min(CASE_NS, max(1, int(guard.get('process_wall_ticks', '0'))*10**9//int(guard.get('qpc_frequency', '1')))) \
                        if abort != 'C1_PREFLIGHT_REFUSAL' else 0
                    budget.seek(0)
                    budget.write(json.dumps(dict(state, charged_ns=str(charged))).encode())
                    budget.truncate()
                    budget.flush()
                    os.fsync(budget.fileno())
                    agreement = False
                    reference = digest('CEML-CHECKPOINT-METADATA-V1', b'unavailable')
                    actual = reference
                    if result and result.get('ok') and abort is None:
                        # Fresh-process recovery plus independent byte-exact validation of both retained generations.
                        _, report = recover(directory, ident)
                        states = {i: (n, *counters) for i in range(4)}
                        published, temporary = inspect_store(directory, ident, states)
                        expected_previous = published[2]['metadata_digest'] if 2 in published else None
                        reference = metadata_object(ident, 3, expected_previous, n, *counters)['metadata_digest']
                        actual = report.get('metadata_digest', actual)
                        agreement = (report['status'] == 'selected' and report['sequence'] == '3' and actual == reference
                                     and int(report['n_hex'], 16) == n and sorted(published) == [2, 3]
                                     and all(x['exact'] for x in published.values()) and not temporary
                                     and result['strategy'] == STRATEGIES[strategy])
                    if abort is None and not agreement:
                        abort = 'C1_CORRECTNESS_INVALID'
                    route = STRATEGIES[strategy]
                    activation = dict(requested_routes=[route], fallback_count='0',
                                      activated_counts={route: str(len(result['promotions'])) if result and result.get('ok') else '0'})
                    activation['route_evidence_digest'] = hashlib.sha3_256(canonical_bytes(activation)).hexdigest()
                    frequency = int(result['qpc_frequency']) if result and result.get('ok') else 1

                    def ns(ticks):
                        return str(int(ticks)*10**9//frequency)

                    for repeat in range(4):
                        sample = result['promotions'][repeat] if result and result.get('ok') else None
                        ok = abort is None
                        record = dict(
                            experiment='CEML', schema_version='CEML-CALIBRATION-RECORD-1', record_class='CALIBRATION_MEASUREMENT',
                            record_id=f'cal1.09.{8*magnitude}.{strategy}.{index}.a1.r{repeat}', suite_version='CEML-CAL-1',
                            case_id=chr(47).join((descriptor['input_id'], 'checkpoint-' + strategy)), input_id=descriptor['input_id'],
                            input_digest=input_digest, candidate_id='checkpoint-' + strategy,
                            build_id='c1-ckpt-' + build['executables']['ckpt_case.exe']['sha3_256'][:16],
                            executable_digest=build['executables']['ckpt_case.exe']['sha3_256'], build_context=context,
                            wall_clock_method='QueryPerformanceCounter around one complete promotion including recovery scan, write, flush, verification, publication, pointer and retirement; integer floor to nanoseconds',
                            cpu_time_method='Not separated per promotion; unavailable',
                            peak_rss_method='GetProcessMemoryInfo PeakWorkingSetSize of the whole child observed by the guard; bytes',
                            artifact_digests=sorted({v['sha3_256'] for v in build['executables'].values()}
                                                    | {v['sha3_256'] for v in build['committed_sources'].values()}),
                            repeat_index=str(repeat), warmup=repeat == 0, measured=repeat != 0, activation=activation,
                            wall_time_ns=ns(sample['total_ticks']) if sample else None, cpu_time_ns=None,
                            peak_rss_bytes=guard.get('peak_rss_bytes') if ok else None, live_bytes=None,
                            scratch_bytes=str(2*(int(sample['body_bytes']) + int(sample['metadata_bytes']))) if sample else '0',
                            swap_observation='PDH pages input/output over intervals of at least one second; excursions='
                                             + guard.get('pages_input_excursion_intervals', '0') + '; output required zero',
                            thermal_observation='Temperature unavailable; processor performance minimum percent='
                                                + str(guard.get('minimum_processor_performance_percent')),
                            frequency_observation='PDH processor performance minimum percent='
                                                  + str(guard.get('minimum_processor_performance_percent')),
                            checkpoint_metrics=dict(
                                serialized_bytes=str(int(sample['body_bytes']) + int(sample['metadata_bytes'])),
                                serialization_time_ns=ns(sample['serialization_ticks']), write_time_ns=ns(sample['write_ticks']),
                                durable_flush_time_ns=ns(sample['flush_ticks']), promotion_time_ns=ns(sample['promotion_ticks']),
                                directory_sync_time_ns=ns(sample['directory_ticks'])) if sample else None,
                            correctness_state_digest=actual, reference_state_digest=reference,
                            correctness_agreement=bool(agreement), valid=ok,
                            invalid_reason=None if ok else guard.get('reason') if guard.get('reason', 'none') != 'none' else abort,
                            abort_code=abort)
                        record['artifact_digest'] = artifact_digest(record)
                        if not validator().is_valid(record):
                            raise Refusal('Calibration schema check failed')
                        write(folder, f'{8*magnitude:06d}-checkpoint-{strategy}-{index}-a1-r{repeat}-record.json', record)
                    write(folder, f'{8*magnitude:06d}-checkpoint-{strategy}-{index}-a1-detail.json',
                          dict(descriptor=descriptor, guard=guard, candidate=result, attempt='1'))
                    print(json.dumps({'case': f'checkpoint/{magnitude}/{strategy}/{index}', 'abort_code': abort}), flush=True)
                    if abort is not None:
                        raise Refusal('Ordered family stopped at the retained invalid case')
    shutil.rmtree(WORK / work_id)
    print(json.dumps({'status': 'ok', 'family': 'checkpoint', 'children': 24}))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('matrix', 'performance'))
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    return run_matrix(args.run_id) if args.command == 'matrix' else run_performance(args.run_id)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps({'status': 'refused', 'reason': str(error) if isinstance(error, Refusal) else 'Checkpoint suite refused; raw diagnostic suppressed'}))
        sys.exit(1)
