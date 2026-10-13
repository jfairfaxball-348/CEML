"""Owner-invoked continuation using V2 or explicitly accepted SESSION-I1.

This operator convenience layer is outside the frozen verifier identity.
It never modifies frozen verifier code or writes batch records itself.
"""

import argparse
from contextlib import contextmanager, ExitStack
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time
import uuid


ROOT = Path(__file__).resolve().parents[2]
RUN_ID = 'RUN1-operational-0001'
CHAIN = Path('local/frontier/run1') / RUN_ID
MANIFESTS = Path('local/frontier/run1') / (RUN_ID + '-manifests')
DRIVER = 'tools/frontier/ceml_frontier.py'
BUILD = 'c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032'
WORKER = '8d3a72aa077fed414ad36e8008900f95a2a0630933e5dea5e66363fd34c19b6b'
TABLE = 'd368ec417e3170729f67737c414b02ced2d2f6cab349f9cd534404985058391c'
SNAPSHOT = '538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729'
BASE = '2392518188130438742016'
GENESIS = 'a416bf0f89ebdb16911baf830b6c375d280829bd58587dd7787e36f5d3c53caf'
PILOT3 = 'ab213f7ba9016bc54afe67873747e605dd88813480a695e8fb54b9b0821f46e6'
ACK = SNAPSHOT + ':operational:' + BASE
ACCEPTED_SOURCE = 'e74efd95c813e38f24aeff8f155825f87d3881a9'
TIP = Path('local/frontier/operator_tip.json')
CONTROL = Path('local/frontier/operator-session.json')
DEFAULT_WIDTH = 9999
ISOLATE_CHILD_SIGNALS = False
SESSION_CLIENT = None


class StopRun(Exception):
    pass


def require(condition, message):
    if not condition:
        raise StopRun(message)


def command(arguments, status):
    """No shell interpolation; a nonzero exit or unexpected status stops the run."""
    isolation = {}
    if ISOLATE_CHILD_SIGNALS:
        isolation = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8', **isolation)
    require(result.returncode == 0,
            result.stdout.strip() or result.stderr.strip() or 'Command failed')
    try:
        value = json.loads(result.stdout)
    except ValueError as error:
        raise StopRun('Command did not return one JSON result') from error
    require(isinstance(value, dict) and value.get('status') == status,
            'Stopped: ' + json.dumps(value, sort_keys=True))
    return value


def driver(*arguments, status):
    if SESSION_CLIENT is not None and arguments[0] in ('ledger', 'verify-batch', 'prepare-manifest', 'pilot', 'replay', 'inspect'):
        value = SESSION_CLIENT.call(arguments)
        require(value.get('status') == status, 'Stopped: ' + json.dumps(value, sort_keys=True))
        return value
    return command([DRIVER, *map(str, arguments)], status)


@contextmanager
def verification_session():
    """Opt-in only. No acceptance means the unchanged frozen CLI execution path."""
    global SESSION_CLIENT
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/session_i1'))
    from identity import accepted
    if not accepted():
        yield
        return
    from client import Client
    print('SESSION-I1: auditing the full chain once and protecting verified files.', flush=True)
    with Client(ROOT / CHAIN) as client:
        SESSION_CLIENT = client
        try:
            yield
        finally:
            SESSION_CLIENT = None


def accept_incremental():
    """An owner action only; never starts a scientific batch."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/session_i1'))
    from identity import ACCEPTANCE, PROFILE, digest
    with operator_lock():
        build = command(['tools/frontier/f1_build.py', '--verify'], 'PASS')
        require(build.get('digest') == BUILD, 'Accepted V2 build identity mismatch')
        status = subprocess.run(['git', 'status', '--porcelain=v1'], cwd=ROOT, capture_output=True, text=True)
        require(status.returncode == 0 and not status.stdout.strip(), 'Working tree must be clean before acceptance')
        identity = digest()
        print('Accept execution profile ' + PROFILE + ' at digest ' + identity + '.', flush=True)
        print('Read docs/SESSION_I1_VALIDATION.md first. This changes session execution; V2 records and publication audits remain unchanged.', flush=True)
        require(input('Type ACCEPT-SESSION-I1 to accept, or anything else to cancel: ').strip() == 'ACCEPT-SESSION-I1', 'Acceptance canceled')
        value = dict(profile=PROFILE, profile_digest=identity, v2_build_digest=BUILD, acknowledgement='ACCEPT-SESSION-I1')
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(dir=ACCEPTANCE.parent, delete=False) as handle:
            name = handle.name
            handle.write(json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii'))
            handle.flush(); os.fsync(handle.fileno())
        os.replace(name, ACCEPTANCE)
        return dict(status='PROFILE_ACCEPTED_NOT_EXECUTED', **value)


def batch_plan(start, count, existing, width):
    require(count >= 1, 'Count must be positive')
    require(1 <= width <= 14400, 'Batch width must be from 1 to 14400')
    require(1 <= existing <= 256, 'Invalid existing batch count')
    require(count <= (256 - existing) * width, 'Requested continuation exceeds the 256-batch limit')
    batches = []
    remaining = count
    while remaining:
        span = min(width, remaining)
        number = existing + len(batches) + 1
        require(number <= 256, 'Requested continuation exceeds the 256-batch limit')
        batches.append(dict(number=number, start=start, end=start + span, width=span))
        start += span
        remaining -= span
    return batches


def published_anchor():
    """Read data fields from the locally frozen, tracked aggregate record; never a URL."""
    text = (ROOT / 'docs/RUN1_PROGRESS.md').read_text(encoding='utf-8')
    patterns = {
        'batches': r'^Batches: ([1-9][0-9]*)\b',
        'end': r'^Verified conditional on that assumption: every integer in \[[0-9]+,([1-9][0-9]*)\) converges$',
        'latest_certificate_digest': r'^Latest certificate digest: ([0-9a-f]{64})$',
        'genesis_digest': r'^Genesis digest: ([0-9a-f]{64})$',
    }
    anchor = {}
    for key, pattern in patterns.items():
        values = re.findall(pattern, text, re.MULTILINE)
        require(len(values) == 1, 'Published continuation anchor missing or ambiguous')
        anchor[key] = values[0]
    return anchor


def check_anchor(anchor, ledger):
    require(isinstance(anchor, dict) and set(anchor) == {'batches', 'end', 'latest_certificate_digest', 'genesis_digest'}
            and all(isinstance(v, str) for v in anchor.values()), 'Continuation anchor shape mismatch')
    require(re.fullmatch('[1-9][0-9]{0,2}', anchor['batches']) is not None and
            re.fullmatch('[1-9][0-9]{0,8191}', anchor['end']) is not None and
            re.fullmatch('[0-9a-f]{64}', anchor['latest_certificate_digest']) is not None,
            'Continuation anchor encoding mismatch')
    number = int(anchor['batches'])
    require(1 <= number <= int(ledger['batches']) <= 256 and
            int(anchor['end']) <= int(ledger['end']) and anchor['genesis_digest'] == GENESIS,
            'Chain rolled back or differs from retained continuation anchor')
    result = driver('verify-batch', '--certificate', CHAIN / f'batch-{number:04d}' / 'certificate.json',
                    status='conditional_complete')
    require(result.get('digest') == anchor['latest_certificate_digest'] and
            result.get('batch_end') == anchor['end'], 'Retained continuation anchor differs from chain')


def remember_tip(ledger):
    """Atomic local receipt outside batch directories; mathematical authority stays in certificates."""
    value = {key: ledger[key] for key in ('batches', 'end', 'latest_certificate_digest', 'genesis_digest')}
    destination = ROOT / TIP
    payload = json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii')
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='operator-tip-', suffix='.tmp',
                                     delete=False) as handle:
        temporary = handle.name
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, destination)


def preflight(args):
    require(sys.version_info[:3] == (3, 12, 10), 'Use the accepted Python 3.12.10')
    require(args.acknowledge in (None, ACK), 'Acknowledgement differs from the accepted operational base')
    require(args.expected_latest is None or re.fullmatch('[0-9a-f]{64}', args.expected_latest) is not None,
            'Expected certificate must be a lowercase 64-hex digest')
    status = subprocess.run(['git', 'status', '--porcelain=v1'], cwd=ROOT,
                            capture_output=True, text=True)
    require(status.returncode == 0 and not status.stdout.strip(), 'Working tree must be clean')
    ancestry = subprocess.run(['git', 'merge-base', '--is-ancestor', ACCEPTED_SOURCE, 'HEAD'],
                              cwd=ROOT, capture_output=True)
    require(ancestry.returncode == 0, 'Checkout does not descend from the accepted source')
    build = command(['tools/frontier/f1_build.py', '--verify'], 'PASS')
    require(build.get('digest') == BUILD and build.get('executable_sha3_256') == WORKER
            and build.get('table_digest') == TABLE, 'Accepted build identity mismatch')
    require(driver('rules', status='rules_pass').get('table_digest') == TABLE,
            'Accepted rule table mismatch')
    snapshot = driver('snapshot', '--file', 'config/frontier_snapshot_v2.json',
                      status='research_only_unaccepted')
    require(snapshot.get('digest') == SNAPSHOT and snapshot['operational']['B'] == BASE,
            'Accepted snapshot mismatch')
    ledger = driver('ledger', '--dir', CHAIN, status='conditional_chain')
    require(ledger.get('start') == BASE and ledger.get('genesis_digest') == GENESIS,
            'Chain root differs from the published external record')
    require(args.expected_latest is None or ledger.get('latest_certificate_digest') == args.expected_latest,
            'Chain differs from expected certificate; stop and compare the external record')
    check_anchor(published_anchor(), ledger)
    receipt = ROOT / TIP
    if receipt.exists():
        require(receipt.stat().st_size <= 131072, 'Local continuation receipt oversized')
        check_anchor(json.loads(receipt.read_text(encoding='ascii')), ledger)
    # The audited genesis already contains the owner's accepted acknowledgement.
    # Continuation reuses it; this does not accept a new base, snapshot or trust tier.
    args.acknowledge = ACK
    existing = int(ledger['batches'])
    expected_dirs = {f'batch-{i:04d}' for i in range(1, existing + 1)}
    actual_dirs = {p.name for p in (ROOT / CHAIN).iterdir() if p.is_dir()}
    require(actual_dirs == expected_dirs, 'Uncommitted or unexpected batch directory; inspect it first')
    prior = CHAIN / f'batch-{existing:04d}' / 'certificate.json'
    verified = driver('verify-batch', '--certificate', prior, status='conditional_complete')
    require(verified.get('digest') == ledger['latest_certificate_digest'] and verified.get('batch_end') == ledger['end'],
            'Latest numbered batch differs from the ledger')
    count = (256 - existing) * DEFAULT_WIDTH if getattr(args, 'mode', 'finite') == 'continuous' else args.count
    plan = batch_plan(int(ledger['end']), count, existing, args.batch_width) if count else []
    for batch in plan:
        name = f"batch-{batch['number']:04d}"
        require(not (ROOT / CHAIN / name).exists() and
                not (ROOT / MANIFESTS / (name + '.json')).exists(),
                'Output or manifest already exists; do not overwrite or automatically retry')
    return ledger, plan


@contextmanager
def control_lock():
    """Short control transaction; never wait for the scientific operator lock."""
    import msvcrt
    with (ROOT / 'local/frontier/operator-control.lock').open('a+b') as handle:
        handle.seek(0, 2)
        if not handle.tell():
            handle.write(b'0'); handle.flush()
        for attempt in range(50):
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                if attempt == 49:
                    raise StopRun('Control state is busy; retry the stop command')
                time.sleep(0.02)
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def save_control(value):
    destination = ROOT / CONTROL
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='operator-session-', suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(json.dumps(value, sort_keys=True, separators=(',', ':')).encode('ascii'))
            handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def read_control():
    path = ROOT / CONTROL
    require(path.stat().st_size <= 131072, 'Operator control state oversized')
    value = json.loads(path.read_text(encoding='ascii'))
    require(isinstance(value, dict) and isinstance(value.get('token'), str) and
            isinstance(value.get('active'), bool) and isinstance(value.get('stop_requested'), bool),
            'Operator control state invalid')
    return value


def operator_running():
    import msvcrt
    path = ROOT / 'local/frontier/operator.lock'
    if not path.exists():
        return False
    with path.open('r+b') as handle:
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            return True
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    return False


def request_stop():
    with control_lock():
        if not operator_running():
            return dict(status='NO_ACTIVE_RUN')
        require((ROOT / CONTROL).exists(), 'Active launcher has no clean-stop control; inspect its version')
        value = read_control()
        if not value['active']:
            return dict(status='NO_ACTIVE_RUN')
        value['stop_requested'] = True
        save_control(value)
        return dict(status='STOP_REQUESTED', message='The current batch will finish and verify before exit. Wait for CLEAN_STOPPED and the run terminal prompt before publishing.')


def update_session(args, **fields):
    token = getattr(args, 'session_token', None)
    if token is None:
        return
    with control_lock():
        value = read_control()
        require(value['token'] == token, 'Operator control session changed')
        value.update(fields)
        save_control(value)


def stop_requested(args):
    if getattr(args, 'stop_local', False):
        return True
    token = getattr(args, 'session_token', None)
    if token is None:
        return False
    with control_lock():
        value = read_control()
        require(value['token'] == token, 'Operator control session changed')
        return value['stop_requested']


def admit_batch(args, number):
    """A stop before admission creates no records; a stop after it finishes this batch."""
    if getattr(args, 'stop_local', False):
        return False
    if getattr(args, 'session_token', None) is None:
        return True
    with control_lock():
        value = read_control()
        require(value['token'] == args.session_token, 'Operator control session changed')
        if value['stop_requested']:
            return False
        value.update(phase='batch', batch=number)
        save_control(value)
        return True


@contextmanager
def managed_run(args):
    global ISOLATE_CHILD_SIGNALS
    with ExitStack() as stack:
        # Same ordering as stop: control first, then a nonblocking operator-lock attempt.
        with control_lock():
            stack.enter_context(operator_lock())
            args.session_token = uuid.uuid4().hex
            args.stop_local = False
            args.session_outcome = 'STOPPED'
            save_control(dict(token=args.session_token, active=True, stop_requested=False,
                              mode=args.mode, requested=str(args.count) if args.count is not None else None,
                              started_at=datetime.now(timezone.utc).isoformat(), phase='preflight', batch=None))
        previous_handler = signal.getsignal(signal.SIGINT)
        previous_isolation = ISOLATE_CHILD_SIGNALS
        # Avoid filesystem/lock operations inside the signal handler.
        signal.signal(signal.SIGINT, lambda *_: setattr(args, 'stop_local', True))
        ISOLATE_CHILD_SIGNALS = True
        try:
            yield
        finally:
            ISOLATE_CHILD_SIGNALS = previous_isolation
            signal.signal(signal.SIGINT, previous_handler)
            update_session(args, active=False, phase='finished', outcome=args.session_outcome)


@contextmanager
def operator_lock():
    """Serialise wrapper invocations. The verifier retains its own batch guards."""
    import msvcrt
    path = ROOT / 'local/frontier/operator.lock'
    with path.open('a+b') as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise StopRun('Another operator launcher is running') from error
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def execute(args, ledger, plan):
    original_start = ledger['end']
    previous_digest = ledger['latest_certificate_digest']
    existing = int(ledger['batches'])
    prior = CHAIN / f'batch-{existing:04d}' / 'certificate.json'
    continuous = getattr(args, 'mode', 'finite') == 'continuous'
    instruction = 'check consecutive batches of 9999 until clean stop or the accepted 256-batch limit' if continuous else f'check the next {args.count}'
    outcome = 'CHAIN_LIMIT_REACHED' if continuous else 'CONDITIONAL_RUN_COMPLETE'
    update_session(args, initial_end=original_start, end=ledger['end'], completed='0', phase='between_batches')
    for batch in plan:
        if stop_requested(args):
            outcome = 'CLEAN_STOPPED'
            break
        number = batch['number']
        name = f'batch-{number:04d}'
        directory = CHAIN / name
        manifest = MANIFESTS / (name + '.json')
        # Check the prior trusted in-memory anchor before each new authority record.
        ledger = driver('ledger', '--dir', CHAIN, status='conditional_chain')
        require(ledger.get('latest_certificate_digest') == previous_digest and
                ledger.get('end') == str(batch['start']) and ledger.get('batches') == str(number - 1)
                and ledger.get('genesis_digest') == GENESIS and ledger.get('start') == BASE,
                'Chain changed during this invocation; stop')
        require(not (ROOT / directory).exists() and not (ROOT / manifest).exists(),
                'Output appeared during this invocation; stop')
        if not admit_batch(args, number):
            outcome = 'CLEAN_STOPPED'
            break
        authority = 'RUN1-owner-cli-' + datetime.now(timezone.utc).strftime('%Y-%m-%d') + f'-{number:04d}'
        print(f"Batch {number}: [{batch['start']},{batch['end']}) ({batch['width']} integers)", flush=True)
        driver('prepare-authority', '--authority-id', authority, '--base-kind', 'operational',
               '--batch-start', batch['start'], '--batch-end', batch['end'],
               '--acknowledge', args.acknowledge, '--owner-instruction', instruction,
               status='AUTHORITY_RECORDED_NOT_EXECUTED')
        prepared = driver('prepare-manifest', '--out', manifest, '--authority-id', authority,
                          '--acknowledge', args.acknowledge, '--max-t-per-explicit', '100000',
                          '--max-total-t', '2000000', '--after-certificate', prior,
                          '--width', batch['width'], status='MANIFEST_WRITTEN_NOT_EXECUTED')
        require(prepared.get('batch_start') == str(batch['start']) and
                prepared.get('batch_end') == str(batch['end']) and
                prepared.get('predecessor_digest') == previous_digest, 'Prepared interval/anchor mismatch')
        committed = driver('pilot', '--manifest', manifest, '--out', directory, status='COMMITTED')
        certificate = directory / 'certificate.json'
        verified = driver('verify-batch', '--certificate', certificate, status='conditional_complete')
        replay = driver('replay', '--batch-dir', directory, status='REFERENCE_REPLAY_MATCH')
        ledger = driver('ledger', '--dir', CHAIN, status='conditional_chain')
        digest = committed.get('digest')
        require(isinstance(digest, str) and re.fullmatch('[0-9a-f]{64}', digest) is not None and
                verified.get('digest') == replay.get('digest') == ledger.get('latest_certificate_digest') == digest
                and ledger.get('end') == verified.get('batch_end') == committed.get('batch_end') == str(batch['end'])
                and verified.get('batch_start') == replay.get('batch_start') == str(batch['start'])
                and replay.get('batch_end') == str(batch['end']) and ledger.get('batches') == str(number)
                and ledger.get('genesis_digest') == GENESIS and ledger.get('start') == BASE,
                'Post-batch verification disagrees; do not extend')
        inspection = driver('inspect', '--batch-dir', directory, status='INSPECTION_ONLY')
        recovery = inspection.get('recovery', {})
        require(recovery.get('status') == 'RECOVERABLE' and recovery.get('pending') is None
                and not recovery.get('warnings') and inspection.get('temporaries') == '0',
                'Inspection found an integrity warning; record it and stop before extension')
        previous_digest = digest
        prior = certificate
        remember_tip(ledger)
        update_session(args, end=ledger['end'], completed=str(int(ledger['end'])-int(original_start)), phase='between_batches', batch=None)
        print(json.dumps(dict(status='VERIFIED_BATCH', **{key: ledger[key] for key in
              ('batches', 'end', 'genesis_digest', 'latest_certificate_digest')}), sort_keys=True), flush=True)
    if stop_requested(args):
        outcome = 'CLEAN_STOPPED'
    args.session_outcome = outcome
    summary = dict(status=outcome, run_id=RUN_ID,
                   added_start=original_start, added_end=ledger['end'], added_count=str(int(ledger['end'])-int(original_start)),
                   snapshot_digest=SNAPSHOT, native_build_digest=BUILD,
                   **{key: ledger[key] for key in ('batches', 'genesis_digest', 'latest_certificate_digest')})
    if not getattr(args, 'defer_summary', False):
        print_summary(summary)
    return summary


def print_summary(summary):
    print(json.dumps(summary, sort_keys=True), flush=True)
    print('Continuation receipt saved. Retain the final digests with the aggregate progress record.')
    print('Conditional on the accepted author-reported base; no independent reproduction or world-frontier claim.')


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', nargs='?', help='start, stop, accept-incremental, or a legacy finite quantity')
    parser.add_argument('quantity', nargs='?', type=int)
    parser.add_argument('--count', type=int, help='Additional integers (legacy option)')
    parser.add_argument('--acknowledge', help='Optional exact acknowledgement; otherwise reuse accepted chain acknowledgement')
    parser.add_argument('--expected-latest', help='Optional explicit digest pin; otherwise audit and discover the current tip')
    parser.add_argument('--batch-width', type=int, default=DEFAULT_WIDTH, help='9999 by default; continuous start requires 9999')
    parser.add_argument('--plan', action='store_true', help='Read-only preflight and plan; execute no batch')
    args = parser.parse_args(argv)
    args.mode = 'finite'
    if args.operation == 'accept-incremental':
        if args.quantity is not None or args.count is not None or args.plan or args.batch_width != DEFAULT_WIDTH:
            parser.error('accept-incremental has no quantity or plan')
        args.mode = 'accept'
        return args
    if args.operation in ('start', 'stop'):
        if args.quantity is not None or args.count is not None or args.batch_width != DEFAULT_WIDTH:
            parser.error('use start or stop with no quantity; continuous batches are exactly 9999')
        if args.operation == 'stop' and args.plan:
            parser.error('stop has no plan option')
        args.mode = 'continuous' if args.operation == 'start' else 'stop'
        return args
    if args.operation == 'check-next':
        if args.quantity is None or args.count is not None:
            parser.error('use check-next X with one positive integer quantity')
        args.count = args.quantity
    elif args.operation is not None:
        if re.fullmatch('[0-9]+', args.operation) is None or args.quantity is not None or args.count is not None:
            parser.error('use one positive integer quantity')
        try:
            args.count = int(args.operation)
        except ValueError:
            parser.error('quantity is too large')
    elif args.count is None or args.quantity is not None:
        parser.error('supply the number of additional integers as the last argument')
    if args.count < 1:
        parser.error('X must be positive')
    return args


def main():
    args = parse_arguments()
    try:
        if args.mode == 'accept':
            print(json.dumps(accept_incremental(), sort_keys=True))
            return 0
        if args.mode == 'stop':
            print(json.dumps(request_stop(), sort_keys=True))
            return 0
        if args.plan:
            ledger, plan = preflight(args)
            print(json.dumps(dict(status='PLAN_ONLY', run_id=RUN_ID, mode=args.mode, added_count=str(args.count) if args.count is not None else None,
                                  start=ledger['end'], end=str(plan[-1]['end']) if plan else ledger['end'],
                                  batches=[{key: str(value) for key, value in batch.items()} for batch in plan]),
                             sort_keys=True))
        else:
            args.defer_summary = True
            with managed_run(args), verification_session():
                ledger, plan = preflight(args)
                remember_tip(ledger)
                summary = execute(args, ledger, plan)
            # The operator lock is released before reporting publication readiness.
            print_summary(summary)
        return 0
    except (StopRun, OSError, ValueError, KeyError) as error:
        print(json.dumps(dict(status='STOPPED', reason=str(error)), sort_keys=True), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('Interrupted. Inspect and verify existing records; no automatic resume or retry.', file=sys.stderr)
        return 130


if __name__ == '__main__':
    sys.exit(main())
