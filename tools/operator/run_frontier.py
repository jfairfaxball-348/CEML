"""Owner-invoked continuation using the unchanged CEML-FRONTIER-2 CLI.

This operator convenience layer is outside the frozen verifier identity.
It never imports or modifies verifier code or writes batch records itself.
"""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys


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


class StopRun(Exception):
    pass


def require(condition, message):
    if not condition:
        raise StopRun(message)


def command(arguments, status):
    """No shell interpolation; a nonzero exit or unexpected status stops the run."""
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8')
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
    return command([DRIVER, *map(str, arguments)], status)


def batch_plan(start, count, existing, width):
    require(1 <= count <= 100000, 'Count must be from 1 to 100000')
    require(1 <= width <= 14400, 'Batch width must be from 1 to 14400')
    require(1 <= existing <= 256, 'Invalid existing batch count')
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


def preflight(args):
    require(sys.version_info[:3] == (3, 12, 10), 'Use the accepted Python 3.12.10')
    require(args.acknowledge == ACK, 'Acknowledgement differs from the accepted operational base')
    require(re.fullmatch('[0-9a-f]{64}', args.expected_latest) is not None,
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
    require(ledger.get('latest_certificate_digest') == args.expected_latest,
            'Chain differs from expected certificate; stop and compare the external record')
    existing = int(ledger['batches'])
    expected_dirs = {f'batch-{i:04d}' for i in range(1, existing + 1)}
    actual_dirs = {p.name for p in (ROOT / CHAIN).iterdir() if p.is_dir()}
    require(actual_dirs == expected_dirs, 'Uncommitted or unexpected batch directory; inspect it first')
    prior = CHAIN / f'batch-{existing:04d}' / 'certificate.json'
    verified = driver('verify-batch', '--certificate', prior, status='conditional_complete')
    require(verified.get('digest') == args.expected_latest and verified.get('batch_end') == ledger['end'],
            'Latest numbered batch differs from the ledger')
    plan = batch_plan(int(ledger['end']), args.count, existing, args.batch_width)
    for batch in plan:
        name = f"batch-{batch['number']:04d}"
        require(not (ROOT / CHAIN / name).exists() and
                not (ROOT / MANIFESTS / (name + '.json')).exists(),
                'Output or manifest already exists; do not overwrite or automatically retry')
    return ledger, plan


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
    instruction = (f'Owner CLI invocation: continue {RUN_ID} for {args.count} integers '
                   f'from {original_start} on the accepted operational base, in sequential verified batches.')
    for batch in plan:
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
        print(json.dumps(dict(status='VERIFIED_BATCH', **{key: ledger[key] for key in
              ('batches', 'end', 'genesis_digest', 'latest_certificate_digest')}), sort_keys=True), flush=True)
    print(json.dumps(dict(status='CONDITIONAL_RUN_COMPLETE', run_id=RUN_ID,
                         added_start=original_start, added_end=ledger['end'], added_count=str(args.count),
                         snapshot_digest=SNAPSHOT, native_build_digest=BUILD,
                         **{key: ledger[key] for key in ('batches', 'genesis_digest', 'latest_certificate_digest')}),
                     sort_keys=True), flush=True)
    print('Save these final digests outside this machine and back up the chain/dependencies to a separate device.')
    print('Conditional on the accepted author-reported base; no independent reproduction or world-frontier claim.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--count', type=int, required=True, help='Additional integers, at most 100000')
    parser.add_argument('--acknowledge', required=True, help='Exact operational acknowledgement typed by the owner')
    parser.add_argument('--expected-latest', default=PILOT3, help='Externally retained latest digest; defaults to pilot 3')
    parser.add_argument('--batch-width', type=int, default=14400, help='At most 14400 per batch')
    parser.add_argument('--plan', action='store_true', help='Read-only preflight and plan; execute no batch')
    args = parser.parse_args()
    try:
        if args.plan:
            ledger, plan = preflight(args)
            print(json.dumps(dict(status='PLAN_ONLY', run_id=RUN_ID, added_count=str(args.count),
                                  start=ledger['end'], end=str(plan[-1]['end']), batches=plan), sort_keys=True))
        else:
            with operator_lock():
                ledger, plan = preflight(args)
                execute(args, ledger, plan)
        return 0
    except (StopRun, OSError, ValueError, KeyError) as error:
        print(json.dumps(dict(status='STOPPED', reason=str(error)), sort_keys=True), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print('Interrupted. Inspect and verify existing records; no automatic resume or retry.', file=sys.stderr)
        return 130


if __name__ == '__main__':
    sys.exit(main())
