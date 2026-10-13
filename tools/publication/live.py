"""Optional read-only observer. Publishes informational status, never runs science."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from github_transport import ROOT, REPO, PublicationError, api, authenticate, commit_files, run
from runner_status import detect, UnknownLiveness

CHAIN = ROOT / 'local/frontier/run1/RUN1-operational-0001'
STATE_DIR = ROOT / 'local/frontier/live-publisher'
BRANCH = 'live-status'
FILENAME = 'frontier_live_status.json'
BUILD = 'c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032'
BASE = '2392518188130438742016'


def iso(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def read_record(path, tag=None):
    if path.stat().st_size > 131072:
        raise ValueError('oversize record')
    raw = path.read_bytes()
    value = json.loads(raw)
    if not isinstance(value, dict) or canonical(value) != raw:
        raise ValueError('noncanonical record')
    if tag:
        bare = {key: item for key, item in value.items() if key != 'digest'}
        digest = hashlib.sha3_256(b'CEML-FRONTIER-2/' + tag.encode('ascii') + b'\0' + canonical(bare)).hexdigest()
        if value.get('digest') != digest:
            raise ValueError('record digest mismatch')
    if value.get('base_B') != BASE or value.get('base_kind') != 'operational' or value.get('native_build_digest') != BUILD:
        raise ValueError('record identity mismatch')
    schemas = {'CERTIFICATE': 'CEML-FRONTIER-2-CERTIFICATE', 'CHECKPOINT': 'CEML-FRONTIER-CKPT-2', None: 'CEML-FRONTIER-2-RUN'}
    if value.get('schema') != schemas[tag] or tag != 'CHECKPOINT' and value.get('run_id') != 'RUN1-operational-0001':
        raise ValueError('record schema or run mismatch')
    return value


def active_runner():
    """Read local process information; command lines never enter the public payload."""
    script = "$ErrorActionPreference='Stop'; @(Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | Where-Object { $_.CommandLine -match 'run_frontier[.]py' } | ForEach-Object { @{command=$_.CommandLine; started=$_.CreationDate.ToUniversalTime().ToString('o')} }) | ConvertTo-Json -Compress"
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', script],
                            capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError('Cannot read launcher process state')
    items = json.loads(result.stdout or '[]')
    if isinstance(items, dict):
        items = [items]
    runs = []
    for item in items:
        line = item['command']
        if '--plan' in line:
            continue
        # Only the accepted absolute path or the documented repository-relative path.
        parsed = parse_runner_command(line)
        if parsed:
            runs.append({**parsed, 'started_at': item['started'],
                         'started': datetime.fromisoformat(item['started']).timestamp()})
    if len(runs) > 1:
        raise ValueError('Multiple launchers observed')
    return runs[0] if runs else None


def parse_runner_command(line):
    if '--plan' in line:
        return None
    prefix = r'(?:C:[\\/]CEML[\\/])?tools[\\/]operator[\\/]run_frontier[.]py["\s]+'
    if re.search(prefix + r'start\b', line, re.IGNORECASE):
        return dict(requested=None, mode='continuous')
    match = re.search(prefix + r'(?:check-next\s+|--count\s+)?([1-9][0-9]*)\b', line, re.IGNORECASE)
    return dict(requested=int(match[1]), mode='finite') if match else None


def snapshot(chain, runner, now, previous_session=None):
    """Only an allowlist of aggregate fields leaves the computer."""
    recent, pending, completed = [], [], []
    dirs = list(chain.glob('batch-*'))
    if any(not re.fullmatch(r'batch-[0-9]{4,}', d.name) or d.name != f'batch-{int(d.name[6:]):04d}' for d in dirs):
        raise ValueError('Unexpected local batch layout')
    dirs.sort(key=lambda d: int(d.name[6:]))
    for directory in dirs:
        number = int(directory.name[6:])
        cert_path = directory / 'certificate.json'
        if cert_path.exists():
            cert = read_record(cert_path, 'CERTIFICATE')
            if cert.get('status') != 'conditional_complete' or cert.get('pending') is not None or cert.get('unresolved_count') != '0':
                raise ValueError('Unexpected certificate state')
            width = int(cert['batch_end']) - int(cert['batch_start'])
            if not 1 <= width <= 14400:
                raise ValueError('Unexpected certificate width')
            finish = cert_path.stat().st_mtime
            recent.append(dict(number=number, start=cert['batch_start'], end=cert['batch_end'],
                               width=width, status='committed', finished_at=iso(finish)))
            completed.append((width, finish))
        else:
            run_path = directory / 'run.json'
            if not run_path.exists():
                continue  # Atomic creation may be between files; try again next poll.
            run = read_record(run_path)
            width = int(run['batch_end']) - int(run['batch_start'])
            if run.get('run_id') != 'RUN1-operational-0001' or not 1 <= width <= 14400:
                raise ValueError('Unexpected run state')
            cursor = int(run['batch_start'])
            run_digest = hashlib.sha3_256(b'CEML-FRONTIER-2/RUN\0' + canonical(run)).hexdigest()
            checkpoints = []
            for slot in directory.glob('ckpt.*.json'):
                try:
                    checkpoint = read_record(slot, 'CHECKPOINT')
                    if checkpoint.get('run_digest') == run_digest and checkpoint.get('batch_start') == run['batch_start'] and checkpoint.get('batch_end') == run['batch_end']:
                        checkpoints.append(checkpoint)
                except (OSError, ValueError):
                    continue  # A checkpoint can be torn; never promote it.
            if checkpoints:
                cursor = int(max(checkpoints, key=lambda c: int(c['generation']))['next_n'])
            if not int(run['batch_start']) <= cursor <= int(run['batch_end']):
                raise ValueError('Checkpoint cursor outside batch')
            pending.append(dict(number=number, start=run['batch_start'], end=run['batch_end'],
                                width=width, processed=cursor-int(run['batch_start']), started_at=iso(run_path.stat().st_mtime)))
    if len(pending) > 1:
        raise ValueError('Multiple incomplete batches')
    current = pending[0] if pending else None
    session_source = runner or previous_session
    session = None
    if session_source:
        if 'initial_end' in session_source:
            anchor = int(session_source['initial_end'])
            done = sum(max(0, int(b['end']) - max(anchor, int(b['start']))) for b in recent)
            done += max(0, int(current['start']) + current['processed'] - max(anchor, int(current['start']))) if current else 0
        else:
            done = sum(width for width, finished in completed if finished >= session_source['started'])
            done += current['processed'] if current and datetime.fromisoformat(current['started_at'].replace('Z', '+00:00')).timestamp() >= session_source['started'] else 0
        requested = session_source['requested']
        if requested is not None and done > requested:
            raise ValueError('Observed session progress exceeds request')
        session = dict(requested=requested, completed=done, started_at=session_source['started_at'], mode=session_source.get('mode', 'finite'))
    unfinished = session and session['requested'] is not None and session['completed'] < session['requested']
    state = 'running' if runner else 'stopped' if current or unfinished or session_source and session_source.get('stale_active') else 'idle'
    message = ('Local observations; checkpoints are provisional. Verified tally changes only after separate publication.'
               if runner else 'No verification run active. Live observations do not change the published verified tally.')
    return dict(schema_version=1, state=state, updated_at=iso(now), message=message,
                current_batch=current, session=session, recent_batches=list(reversed(recent[-20:])))


def upload(payload):
    """Keep heartbeat commits away from main and all scientific evidence."""
    refs = api(f'repos/{REPO}/git/matching-refs/heads/{BRANCH}')
    exact = [r for r in refs if r['ref'] == 'refs/heads/' + BRANCH]
    parent = exact[0]['object']['sha'] if exact else None
    head = commit_files(parent, None, {FILENAME: json.dumps(payload, indent=2) + '\n'}, 'Live informational status')
    if parent:
        api(f'repos/{REPO}/git/refs/heads/{BRANCH}', 'PATCH', {'sha': head, 'force': False})
    else:
        api(f'repos/{REPO}/git/refs', 'POST', {'ref': 'refs/heads/' + BRANCH, 'sha': head})


@contextmanager
def publisher_lock():
    import msvcrt
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with (STATE_DIR / 'publisher.lock').open('a+b') as handle:
        handle.seek(0, 2)
        if not handle.tell():
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise PublicationError('Live publisher is already running') from error
        try:
            yield
        finally:
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)


def observe(previous):
    try:
        now = time.time()
        runner, recorded = detect(now)
        if recorded is None:
            runner = active_runner()  # compatibility only when no managed control/lock exists
        payload = snapshot(CHAIN, runner, now, recorded or previous)
        return payload, recorded or runner or previous
    except UnknownLiveness as error:
        # Retain aggregate details; uncertain visibility must not imply stopped.
        try:
            recorded = error.source or previous
            payload = snapshot(CHAIN, None, time.time(), recorded)
            payload.update(state='error', message='Run activity could not be confirmed. Last observed progress is informational; audited publication is unchanged.')
            return payload, recorded
        except (OSError, ValueError, KeyError):
            pass
        return dict(schema_version=1, state='error', updated_at=iso(time.time()),
                    message='Local status needs review. No work is promoted by the live publisher.',
                    current_batch=None, session=None, recent_batches=[]), previous
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
        return dict(schema_version=1, state='error', updated_at=iso(time.time()),
                    message='Local status needs review. No work is promoted by the live publisher.',
                    current_batch=None, session=None, recent_batches=[]), previous


def watch():
    # pythonw under Task Scheduler has no console. Keep diagnostics local.
    if sys.stdout is None or sys.stderr is None:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        log = (STATE_DIR / 'publisher.log').open('a', encoding='utf-8', buffering=1)
        sys.stdout = sys.stderr = log
    with publisher_lock():
        previous = None
        (STATE_DIR / 'stop').unlink(missing_ok=True)
        while True:
            payload, previous = observe(previous)
            stopping = (STATE_DIR / 'stop').exists()
            if stopping:
                payload.update(state='paused', message='Live publisher stopped. The verification runner is unaffected.')
            try:
                upload(payload)
                (STATE_DIR / 'last-success.json').write_text(json.dumps(payload) + '\n', encoding='ascii')
                print(f"Published live state: {payload['state']}", flush=True)
            except (PublicationError, OSError, ValueError, subprocess.TimeoutExpired):
                print('Live upload failed; retrying in 60 seconds. Verification is unaffected.', flush=True)
            if stopping:
                return
            for _ in range(60):
                if (STATE_DIR / 'stop').exists():
                    break
                time.sleep(1)


def control_task(action):
    run(['powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
         '-File', str(Path(__file__).with_name('watch_task.ps1')), '-Action', action,
         '-Python', sys.executable])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('start', 'stop', 'watch', 'once', 'preview'), nargs='?', default='start')
    args = parser.parse_args()
    try:
        if args.action == 'preview':
            payload, _ = observe(None)
            print(json.dumps(payload, indent=2)); return 0
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        if args.action == 'stop':
            control_task('Stop')
            (STATE_DIR / 'stop').write_text('stop\n', encoding='ascii')
            print('Stop requested; scientific execution is unaffected.'); return 0
        authenticate()
        if args.action == 'once':
            with publisher_lock():
                payload, _ = observe(None); upload(payload)
            print('Live status published.'); return 0
        if args.action == 'watch':
            watch(); return 0
        control_task('Start')
        print('Live publisher started as a hidden Windows task with logon and automatic recovery. Use stop to disable uploads.')
        return 0
    except (PublicationError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        print('LIVE_PUBLISHER_STOPPED: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
