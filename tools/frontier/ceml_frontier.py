"""CEML-FRONTIER-2 offline driver. L1 fixtures are engineering evidence only."""
from __future__ import annotations

import argparse
import ctypes
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

import reference
from f1_build import Refusal as BuildRefusal

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / 'local/frontier'
PROTOCOL = 'CEML-FRONTIER-2'
DOMAIN = b'CEML-FRONTIER-2/'
SCHEMA_IDS = {'snapshot': 'CEML-FRONTIER-2-SNAPSHOT', 'run': 'CEML-FRONTIER-2-RUN',
              'checkpoint': 'CEML-FRONTIER-CKPT-2', 'certificate': 'CEML-FRONTIER-2-CERTIFICATE'}
# The frozen version-1 snapshot is provenance only; no version-1 record is runnable here.
V1_SNAPSHOT_FILE = 'config/frontier_snapshot_v1.json'
V1_SNAPSHOT_SCHEMA = 'CEML-FRONTIER-1-SNAPSHOT'
V1_SNAPSHOT_DIGEST = 'a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66'
SLOTS = 3
DAMAGED = object()
FAULT_POINTS = ('before_create', 'before_write', 'during_write', 'before_flush', 'after_flush',
                'before_rename', 'after_rename', 'after_directory_flush')
RULESET = 'E2-Q4-P3-M9-S2K4-03-v1'
MAX_RECORD = 128 * 1024
MAX_EVENT_BYTES = 16 * 1024 * 1024
MAX_CHAIN = 256
NATIVE_L1_CAP = 10000
NATIVE_WALL_SECONDS = 30
IDENTITY = ('run_id', 'snapshot_digest', 'base_kind', 'base_B', 'ruleset_id',
            'table_digest', 'native_build_digest')
BINDING = IDENTITY + ('batch_start', 'batch_end', 'predecessor_digest')
TOTALS = ('counts', 'transcript_digest', 'explicit_t_steps', 'explicit_odd_steps',
          'explicit_standard_steps', 'explicit_attempts')
AUTHORITY_KEYS = ('authority_id', 'snapshot_digest', 'base_kind', 'base_B', 'accepted_assumption_ack',
                  'batch_start', 'batch_end', 'owner_instruction')
FIXTURES = {'L1-fixture-a': (2, 146), 'L1-fixture-b': (143, 287),
            'L1-fixture-c': (17, 113), 'L1-fixture-successor': (146, 290),
            'L1-fixture-wide': (2, 9602)}
# Intervals a fixture manifest may carry, by run ID. 'L1-fixture-successor' only names the
# second batch of the L1-fixture-a chain; it is never itself a run ID.
FIXTURE_INTERVALS = {'L1-fixture-a': {(2, 146), (146, 290)}, 'L1-fixture-b': {(143, 287)},
                     'L1-fixture-c': {(17, 113)}, 'L1-fixture-wide': {(2, 9602)}}
sys.set_int_max_str_digits(10000)


class Refusal(Exception):
    pass


class NativeFailure(Refusal):
    def __init__(self, reason, exit_code, stderr, summary):
        super().__init__(reason)
        self.record = dict(schema='CEML-FRONTIER-2-NATIVE-ANOMALY', reason=reason,
                           exit_code=str(exit_code), stderr_hex=bytes(stderr).hex(),
                           next_n=summary['next_n'], transcript_digest=summary['transcript_digest'])


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def H(tag, payload):
    return hashlib.sha3_256(DOMAIN + tag.encode('ascii') + b'\0' + payload).hexdigest()


def canonical(value):
    def walk(v, depth=0):
        require(depth <= 12, 'object nesting limit')
        if isinstance(v, dict):
            for k, item in v.items():
                require(isinstance(k, str) and k.isascii(), 'ASCII keys required')
                walk(item, depth + 1)
        elif isinstance(v, list):
            for item in v:
                walk(item, depth + 1)
        else:
            require(v is None or isinstance(v, str) and v.isascii(), 'ASCII strings/null required')
    walk(value)
    data = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      allow_nan=False).encode('ascii')
    require(len(data) <= MAX_RECORD, 'record length limit')
    return data


def local_path(value):
    raw = str(value)
    require(not raw.startswith(('\\\\', '//')) and '://' not in raw and '\0' not in raw,
            'local file required')
    require('..' not in raw.replace('\\', '/').split('/'), 'path traversal refused')
    p = Path(value)
    require(not any(part.is_symlink() or getattr(part, 'is_junction', lambda: False)()
                    for part in (p, *p.parents)), 'symlink/junction refused')
    resolved = p.resolve()
    require(not str(resolved).startswith(('\\\\', '//')) and '://' not in str(resolved),
            'resolved network path refused')
    return resolved


def parse_bytes(data):
    require(len(data) <= MAX_RECORD and data.isascii(), 'record size/encoding')
    # Check lexical depth before the JSON parser can allocate deeply nested structures.
    depth, quoted, escaped = 0, False, False
    for char in data:
        if quoted:
            if escaped:
                escaped = False
            elif char == 92:
                escaped = True
            elif char == 34:
                quoted = False
        elif char == 34:
            quoted = True
        elif char in (91, 123):
            depth += 1
            require(depth <= 12, 'object nesting limit')
        elif char in (93, 125):
            depth -= 1
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    try:
        obj = json.loads(data, object_pairs_hook=pairs,
                         parse_constant=lambda _: (_ for _ in ()).throw(Refusal('invalid JSON constant')))
    except (ValueError, RecursionError) as error:
        raise Refusal('invalid JSON') from error
    require(canonical(obj) == data, 'noncanonical JSON bytes')
    return obj


def validate_shape(obj, kind, version=2):
    spec = json.loads((ROOT / f'schemas/frontier_{kind}_v{version}.schema.json').read_text('ascii'))
    def check(value, shape):
        if 'anyOf' in shape:
            for option in shape['anyOf']:
                try:
                    check(value, option)
                    return
                except Refusal:
                    pass
            raise Refusal('schema union mismatch')
        if 'const' in shape:
            require(value == shape['const'], 'schema constant mismatch')
        if 'enum' in shape:
            require(value in shape['enum'], 'schema enum mismatch')
        typ = shape.get('type')
        if typ == 'object':
            require(isinstance(value, dict), 'object required')
            require(set(shape.get('required', ())) <= set(value), 'missing field')
            require(not shape.get('additionalProperties') and set(value) <= set(shape['properties']),
                    'unknown field')
            for key, item in value.items():
                check(item, shape['properties'][key])
        elif typ == 'string':
            require(isinstance(value, str) and value.isascii(), 'ASCII string required')
            require(shape.get('minLength', 0) <= len(value) <= shape.get('maxLength', MAX_RECORD),
                    'string length limit')
            if 'pattern' in shape:
                require(re.fullmatch(shape['pattern'], value) is not None, 'string pattern mismatch')
        elif typ == 'null':
            require(value is None, 'null required')
    canonical(obj)
    check(obj, spec)


def seal(obj, tag):
    result = dict(obj)
    result.pop('digest', None)
    result['digest'] = H(tag, canonical(result))
    return result


def read_bounded(path):
    with local_path(path).open('rb') as stream:
        return stream.read(MAX_RECORD + 1)


def load_record(path, kind):
    obj = parse_bytes(read_bounded(path))
    validate_shape(obj, kind)
    if kind in ('checkpoint', 'certificate'):
        require(obj == seal(obj, kind.upper()), 'record digest mismatch')
    return obj


def v1_snapshot(path=None):
    """Frozen version-1 research snapshot: exact bytes, shape and version-1 digest."""
    raw = read_bounded(ROOT / V1_SNAPSHOT_FILE if path is None else path)
    obj = parse_bytes(raw)
    validate_shape(obj, 'snapshot', 1)
    digest = hashlib.sha3_256(b'CEML-FRONTIER-1/SNAPSHOT\0' + raw).hexdigest()
    require(digest == V1_SNAPSHOT_DIGEST, 'frozen version-1 snapshot bytes changed')
    return obj, digest, hashlib.sha3_256(raw).hexdigest()


def validate_snapshot(obj):
    validate_shape(obj, 'snapshot')
    p, o = obj['published'], obj['operational']
    frozen, frozen_digest, frozen_plain = v1_snapshot()
    require(obj['provenance']['source_digest'] == frozen_digest and
            obj['provenance']['source_sha3_256'] == frozen_plain and
            all(obj[key] == frozen[key] for key in ('observed_at_utc', 'published', 'operational')),
            'snapshot provenance does not match the frozen version-1 snapshot')
    try:
        observed = datetime.strptime(obj['observed_at_utc'], '%Y-%m-%dT%H:%M:%SZ')
        generated = datetime.strptime(o['site_generated_utc'], '%Y-%m-%dT%H:%M:%SZ')
        published = datetime.strptime(p['publication_date'], '%Y-%m-%d')
    except ValueError as error:
        raise Refusal('invalid calendar timestamp') from error
    require(published <= observed and generated <= observed, 'source times after observation')
    for source in (p, o):
        require(re.fullmatch(r'https://[A-Za-z0-9][A-Za-z0-9._~:/?&=%+#-]*', source['source_url']),
                'invalid source URL metadata')
    require(int(p['B']) == 2**71, 'published source-fact mismatch')
    size, unit = int(o['work_unit_size']), int(o['first_incomplete_unit'])
    require(size == 2**40 and unit > 0, 'work-unit source-fact mismatch')
    require(int(o['B']) == unit * size and int(o['first_incomplete_end']) == (unit + 1) * size,
            'work-unit endpoint mismatch')
    require(int(p['B']) <= int(o['headline_B']) <= int(o['B']), 'baseline order mismatch')
    require(int(o['headline_B']) % 2**60 == 0, 'headline arithmetic mismatch')
    require(int(o['first_unassigned_unit']) >= unit, 'assignment/completion mismatch')
    return H('SNAPSHOT', canonical(obj))


def snapshot():
    obj = load_record(ROOT / 'config/frontier_snapshot_v2.json', 'snapshot')
    validate_snapshot(obj)
    return obj


def genesis(run):
    return H('GENESIS', '|'.join(run[k] for k in IDENTITY).encode('ascii'))


def validate_manifest(run, snap, test=False):
    validate_shape(run, 'run')
    require(run['snapshot_digest'] == validate_snapshot(snap), 'snapshot identity mismatch')
    require(run['table_digest'] == reference.table_digest(), 'table identity mismatch')
    start, end, base = map(int, (run['batch_start'], run['batch_end'], run['base_B']))
    require(2 <= base <= start < end and end - start <= 14400, 'invalid interval/base')
    require(1 <= int(run['max_t_per_explicit']) <= 100000 and
            1 <= int(run['max_total_t']) <= 2000000, 'finite budget bounds')
    require(run['accepted_assumption_ack'] == ':'.join((run['snapshot_digest'], run['base_kind'], run['base_B'])),
            'external assumption acknowledgement mismatch')
    if test:
        require(run['run1_authority_id'] == 'L1-NONSCIENTIFIC' and
                (start, end) in FIXTURE_INTERVALS.get(run['run_id'], ()), 'not a predesignated L1 fixture')
        expected_base = 2 if run['run_id'] == 'L1-fixture-a' else start
        require(base == expected_base and run['base_kind'] == 'published', 'fixture identity mismatch')
    else:
        require(run['base_B'] == snap[run['base_kind']]['B'], 'selected external B mismatch')
        require(run['run1_authority_id'] != 'L1-NONSCIENTIFIC', 'engineering fixture is not science')
        require(start != base or end - start == 144, 'first RUN1 pilot is exactly 144 starts')
    if start == base:
        require(run['predecessor_digest'] == genesis(run), 'genesis mismatch')
    return run


def status_path():
    return ROOT / 'PROGRAM_STATUS.md'


def status_text():
    return status_path().read_text('utf-8')


def run1_status():
    status = status_text()
    require(phase_is(status, 'RUN1') and
            status_field(status, 'Scientific execution authorization') == 'AUTHORISED', 'RUN1 not owner-authorised')


def science_readable(test):
    """Read-only commands recompute starts: a fixture, or full RUN1 status, never the phase alone."""
    if test:
        return True
    try:
        run1_status()
    except Refusal:
        return False
    return True


def run1_gate(run):
    """Return the exact authority-evidence bytes that cover this one batch."""
    run1_status()
    raw = read_bounded(LOCAL / 'run1_authorization.json')
    evidence = parse_bytes(raw)
    require(isinstance(evidence, dict) and set(evidence) == set(AUTHORITY_KEYS) and
            all(isinstance(value, str) for value in evidence.values()), 'RUN1 authority evidence shape')
    require(evidence['owner_instruction'].strip() and evidence['authority_id'] == run['run1_authority_id'],
            'fresh RUN1 owner authority missing')
    for key in AUTHORITY_KEYS[1:-1]:
        require(evidence[key] == run[key], 'RUN1 authority does not cover this batch')
    if run['batch_start'] == run['base_B']:
        require(int(run['batch_end'])-int(run['batch_start']) == 144, 'first RUN1 pilot is exactly 144 starts')
    return raw


def l1_gate():
    status = status_text()
    require(phase_is(status, 'L1') and
            status_field(status, 'Scientific execution authorization').split()[0] == 'DENIED', 'L1 fixture phase not established')
    evidence = parse_bytes(read_bounded(LOCAL/'l1_authorization.json'))
    require(isinstance(evidence, dict) and
            set(evidence) == {'scope', 'owner_instruction', 'entry_main', 'p2_merge', 'authorized_on'} and
            evidence['scope'] == 'L1-IMPLEMENTATION-ACCEPTANCE-ONLY' and evidence['owner_instruction'] and
            evidence['entry_main'] == evidence['p2_merge'] == 'abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016',
            'fresh L1 invocation evidence missing')


def status_field(status, label):
    values = re.findall(r'^\*\*' + re.escape(label) + r':\*\* ([^\r\n]+)$', status, re.MULTILINE)
    require(len(values) == 1, 'missing/duplicate authoritative status field')
    return values[0].strip()


def phase_is(status, phase):
    value = status_field(status, 'Authoritative current phase')
    return value == phase or value.startswith(phase + ' — ')


def fixture_run(name, max_t=100000, max_total=2000000, build_digest=None):
    require(name in FIXTURES, 'fixture name')
    if build_digest is None:
        from f1_build import build_digest as digest
        build_digest = digest()
    start, end = FIXTURES[name]
    snap_digest = validate_snapshot(snapshot())
    base = 2 if name == 'L1-fixture-successor' else start
    run = dict(schema=SCHEMA_IDS['run'], run_id='L1-fixture-a' if name == 'L1-fixture-successor' else name,
               run1_authority_id='L1-NONSCIENTIFIC',
               snapshot_digest=snap_digest, base_kind='published', base_B=str(base),
               accepted_assumption_ack=f'{snap_digest}:published:{base}', batch_start=str(start),
               batch_end=str(end), predecessor_digest='0'*64, ruleset_id=RULESET,
               table_digest=reference.table_digest(), native_build_digest=build_digest,
               map_id='T-shortened-v1', max_t_per_explicit=str(max_t), max_total_t=str(max_total))
    run['predecessor_digest'] = genesis(run)
    return run


def summary_reference(start, end, max_t, max_total):
    raw = reference.replay(start, end, max_t, max_total)
    return {k: ({name: str(v) for name, v in raw[k].items()} if k == 'counts' else
                raw[k] if k in ('pending', 'transcript_digest') else str(raw[k]))
            for k in ('next_n', 'pending') + TOTALS}


def validate_summary(summary, start, end, max_t, max_total):
    cursor = int(summary['next_n'])
    require(start <= cursor <= end, 'cursor out of bounds')
    prefix = summary_reference(start, cursor, max_t, max_total)
    # The replay must itself reach the claimed cursor: a cursor beyond the first
    # unresolved start would otherwise be compared with a shorter prefix's counters.
    require(prefix['next_n'] == summary['next_n'] and prefix['pending'] is None,
            'claimed prefix is not completely resolved by independent replay')
    require(sum(map(int, summary['counts'].values())) == cursor - start, 'prefix coverage sum mismatch')
    for key in TOTALS[:-1]:
        require(summary[key] == prefix[key], 'prefix replay mismatch: ' + key)
    pending = summary['pending']
    attempt = 0
    if pending is not None:
        require(cursor < end and pending['n'] == str(cursor), 'pending cursor mismatch')
        require(pending['reason'] in ('step_budget', 'total_budget', 'resource_refusal', 'native_failure', 'oracle_mismatch'),
                'unknown pending reason')
        steps, value = int(pending['attempted_steps']), cursor
        require(0 <= steps <= max_t and int(prefix['explicit_t_steps']) + steps <= max_total, 'pending budget mismatch')
        attempt = int(reference.classify(cursor) == 'EXPLICIT')
        require(attempt or steps == 0, 'rule failure has explicit steps')
        for _ in range(steps):
            value = reference.T(value)
            require(value >= cursor, 'pending includes completed descent')
        require(pending['last_value'] == str(value), 'pending exact state mismatch')
        if pending['reason'] == 'step_budget':
            require(attempt and steps == max_t, 'step budget not exhausted')
        if pending['reason'] == 'total_budget':
            require(attempt and int(prefix['explicit_t_steps']) + steps == max_total, 'total budget not exhausted')
    require(summary['explicit_attempts'] == str(int(prefix['explicit_attempts']) + attempt), 'attempt count mismatch')
    require(cursor != end or pending is None, 'complete cursor has pending work')


def checked_events(frames, start, end, max_t, max_total, complete=True):
    digest = hashlib.sha3_256(DOMAIN + b'EVENTS\0')
    counts = {k: '0' for k in reference.expected_counts(start, start)}
    # expected_counts includes all coverage categories in the reference contract.
    t_steps, odd_steps, cursor = 0, 0, start
    mapping = {'E2':'e2_count', 'Q4':'q4_count', 'P3':'p3_count', 'M9':'m9_count',
               'S2K4-03':'s2_count', 'EXPLICIT':'explicit_count'}
    for frame in frames:
        require(cursor < end and len(frame) <= 32768 and frame.endswith(b'\n') and frame.isascii(),
                'extra/truncated/oversized event')
        try:
            expected = reference.event(cursor, max_t)
        except reference.Unresolved as error:
            raise Refusal('successful event for unresolved start') from error
        require(frame == expected, 'event ordering/rule/witness mismatch')
        fields = frame.decode('ascii').rstrip('\n').split('|')
        rule, steps, odd = fields[1], int(fields[2]), int(fields[3])
        require(t_steps + steps <= max_total, 'total budget exceeded')
        counts[mapping[rule]] = str(int(counts[mapping[rule]]) + 1)
        t_steps += steps
        odd_steps += odd
        digest.update(frame)
        cursor += 1
    require(not complete or cursor == end, 'missing native event')
    return dict(next_n=str(cursor), pending=None, counts=counts, transcript_digest=digest.hexdigest(),
                explicit_t_steps=str(t_steps), explicit_odd_steps=str(odd_steps),
                explicit_standard_steps=str(t_steps + odd_steps), explicit_attempts=counts['explicit_count'])


def consume_native(start, end, max_t, max_total, exe=None):
    require(2 <= start < end and end-start <= 14400, 'native interval guard')
    require(1 <= max_t <= 100000 and 1 <= max_total <= 2000000, 'native budget guard')
    if exe is None:
        from f1_build import verify_build
        verify_build()
        exe = LOCAL / 'build/ceml_frontier.exe'
    command = [str(local_path(exe)), '--start', str(start), '--end', str(end),
               '--max-t-per-explicit', str(max_t), '--max-total-t', str(max_total)]
    env = dict(os.environ)
    env.pop('CEML_FRONTIER_DRIVER_MODE', None)
    env.pop('CEML_FRONTIER_STATUS_PATH', None)
    # Same boundary as the worker's own gate: any scan ending above the L1 cap needs RUN1.
    if end > NATIVE_L1_CAP:
        run1_status()
        env['CEML_FRONTIER_DRIVER_MODE'] = 'RUN1-AUTHORIZED'
        env['CEML_FRONTIER_STATUS_PATH'] = str(status_path())
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=Path(exe).parent, env=env)
    # Bounded pipe polling in this process, with no helper threads or per-n files.
    deadline, stderr, buffer = time.monotonic()+NATIVE_WALL_SECONDS, bytearray(), bytearray()
    frames, event_bytes = [], 0
    try:
        if os.name == 'nt':
            import msvcrt
            peek = ctypes.WinDLL('kernel32', use_last_error=True).PeekNamedPipe
            peek.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32,
                             ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p)
            peek.restype = ctypes.c_int
            def available(stream):
                amount = ctypes.c_uint32()
                ok = peek(msvcrt.get_osfhandle(stream.fileno()), None, 0, None, ctypes.byref(amount), None)
                return amount.value if ok else 0
        else:
            import select
            def available(stream):
                return 4096 if select.select([stream], [], [], 0)[0] else 0
        while True:
            progressed = False
            for stream, target in ((process.stdout, buffer), (process.stderr, stderr)):
                count = available(stream)
                if count:
                    chunk = os.read(stream.fileno(), min(count, 4096))
                    target.extend(chunk)
                    progressed = bool(chunk) or progressed
            while b'\n' in buffer:
                line, _, rest = buffer.partition(b'\n')
                frames.append(bytes(line)+b'\n')
                event_bytes += len(line)+1
                buffer[:] = rest
                require(len(frames) <= end-start, 'extra native frame')
            require(len(buffer) <= 32768 and len(stderr) <= 32768, 'native pipe limit')
            require(event_bytes <= MAX_EVENT_BYTES, 'event memory resource limit')
            if process.poll() is not None and not progressed and not available(process.stdout) and not available(process.stderr):
                break
            require(time.monotonic() < deadline, 'native wall budget')
            time.sleep(0.002)
        require(not buffer, 'truncated native frame')
        result = checked_events(frames, start, end, max_t, max_total, complete=process.returncode == 0)
        if process.returncode == 0:
            if stderr != b'COMPLETE\n':
                raise NativeFailure('ambiguous native success', process.returncode, stderr, result)
        else:
            cursor = int(result['next_n'])
            match = re.fullmatch(rb'UNRESOLVED\|([1-9][0-9]*)\|(step_budget|total_budget|operand_limit|output_error)\|(0|[1-9][0-9]*)\|(0|[1-9][0-9]*)\|([1-9][0-9]*)\n', stderr)
            if process.returncode != 3 or cursor >= end or match is None:
                raise NativeFailure('missing/ambiguous native failure status', process.returncode, stderr, result)
            n_text, reason, steps_text, odd_text, last_text = [value.decode('ascii') for value in match.groups()]
            require(n_text == str(cursor), 'native failure cursor mismatch')
            steps, odd, last = int(steps_text), int(odd_text), cursor
            require(steps <= max_t and int(result['explicit_t_steps'])+steps <= max_total, 'native failure budget mismatch')
            computed_odd = 0
            for _ in range(steps):
                computed_odd += last % 2
                last = reference.T(last)
            require(odd == computed_odd and last_text == str(last), 'native failure exact-state disagreement')
            result['pending'] = dict(n=n_text, reason={'operand_limit':'resource_refusal', 'output_error':'native_failure'}.get(reason,reason),
                                     attempted_steps=steps_text, last_value=last_text)
            result['explicit_attempts'] = str(int(result['counts']['explicit_count']) +
                                             int(reference.classify(cursor) == 'EXPLICIT'))
        validate_summary(result, start, end, max_t, max_total)
        return result
    finally:
        if process.poll() is None:
            process.kill()
        process.wait(timeout=5)
        process.stdout.close()
        process.stderr.close()


def write_atomic(path, data, replace=False, fault=None):
    """Exclusive temporary, flush, atomic rename, directory flush, byte re-read.

    fault names one FAULT_POINTS member for acceptance tests; the CLI never sets it.
    """
    path = local_path(path)
    require(len(data) <= MAX_RECORD, 'atomic record size')
    require(fault is None or fault in FAULT_POINTS, 'unknown fault point')
    temp = path.parent / (path.name + '.' + uuid.uuid4().hex + '.tmp')
    def inject(phase):
        require(fault != phase, 'injected ' + phase)
    inject('before_create')
    with temp.open('xb', buffering=0) as stream:
        inject('before_write')
        if fault == 'during_write':
            stream.write(data[:len(data)//2])
            raise Refusal('injected during_write')
        require(stream.write(data) == len(data), 'short record write')
        inject('before_flush')
        os.fsync(stream.fileno())
        inject('after_flush')
    inject('before_rename')
    if os.name == 'nt':
        move = ctypes.WinDLL('kernel32', use_last_error=True).MoveFileExW
        move.argtypes, move.restype = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32), ctypes.c_int
        require(move(str(temp), str(path), 8 | int(replace)), 'atomic rename refused')
    elif replace:
        os.replace(temp, path)
    else:
        os.link(temp, path)
        temp.unlink()
    inject('after_rename')
    directory_flush(path.parent)
    inject('after_directory_flush')
    require(path.read_bytes() == data, 'atomic re-read mismatch')


def directory_flush(path):
    if os.name != 'nt':
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
            return True
        finally:
            os.close(descriptor)
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateFileW.argtypes = (ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
                                  ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_void_p)
    kernel.CreateFileW.restype = ctypes.c_void_p
    kernel.FlushFileBuffers.argtypes, kernel.FlushFileBuffers.restype = (ctypes.c_void_p,), ctypes.c_int
    kernel.CloseHandle.argtypes, kernel.CloseHandle.restype = (ctypes.c_void_p,), ctypes.c_int
    handle = kernel.CreateFileW(str(path), 0x40000000, 7, None, 3, 0x02000000, None)
    if handle == ctypes.c_void_p(-1).value:
        return False
    try:
        return bool(kernel.FlushFileBuffers(handle))
    finally:
        kernel.CloseHandle(handle)


def checkpoint_valid(obj, run):
    validate_shape(obj, 'checkpoint')
    require(obj == seal(obj, 'CHECKPOINT'), 'checkpoint hash mismatch')
    require(obj['run_digest'] == H('RUN', canonical(run)), 'checkpoint run mismatch')
    require(all(obj[key] == run[key] for key in BINDING), 'checkpoint identity mismatch')
    generation = int(obj['generation'])
    require(generation <= 2**64-1, 'generation overflow')
    require((generation == 0) == (obj['previous_checkpoint_digest'] is None), 'checkpoint parent mismatch')
    # The root asserts no progress, so accepting it alone can never promote anything.
    require(generation > 0 or (obj['next_n'] == run['batch_start'] and obj['pending'] is None),
            'root checkpoint is not the empty prefix')
    validate_summary(obj, int(run['batch_start']), int(run['batch_end']),
                     int(run['max_t_per_explicit']), int(run['max_total_t']))


class CheckpointStore:
    """Three rotating slots; generation g lives only in slot g mod 3 (protocol 4.3-4.5)."""

    def __init__(self, directory, run):
        self.directory, self.run = local_path(directory), run
        self.directory.mkdir(parents=True, exist_ok=True)

    def slot(self, index):
        return self.directory / f'ckpt.{index}.json'

    def read_slot(self, index):
        """None if ABSENT, DAMAGED for a torn file, else a canonical self-hashed record.

        Protocol 4.5. Only bytes that are not JSON, or a version-2 checkpoint object
        whose own digest fails, are DAMAGED. Any other parseable JSON is FOREIGN and
        refuses. A record whose digest verifies is self-hashed, so it must also be
        canonical and shape-valid; if it is not, that is a contradiction and refuses.
        """
        path = local_path(self.slot(index))
        if not path.exists():
            return None
        try:
            with path.open('rb') as stream:
                data = stream.read(MAX_RECORD + 1)
            if len(data) > MAX_RECORD:
                return DAMAGED
            obj = json.loads(data.decode('ascii'))
        except (OSError, ValueError, RecursionError):
            return DAMAGED
        require(isinstance(obj, dict) and obj.get('schema') == SCHEMA_IDS['checkpoint'],
                'foreign or cross-version checkpoint record')
        try:
            self_hashed = obj == seal(obj, 'CHECKPOINT')
        except Refusal:
            return DAMAGED
        if not self_hashed:
            return DAMAGED
        require(canonical(obj) == data, 'self-hashed checkpoint is not stored canonically')
        validate_shape(obj, 'checkpoint')
        return obj

    def recover(self):
        records, damaged, absent = [], [], []
        for index in range(SLOTS):
            found = self.read_slot(index)
            if found is None:
                absent.append(index)
            elif found is DAMAGED:
                damaged.append(index)
            else:
                # Canonical, self-hashed contradictory identities/logical claims are not torn writes.
                checkpoint_valid(found, self.run)
                require(int(found['generation']) % SLOTS == index, 'checkpoint slot/generation mismatch')
                records.append(found)
        require(records, 'no independently valid checkpoint')
        records.sort(key=lambda record: int(record['generation']))
        for old, new in zip(records, records[1:]):
            require(int(new['generation']) == int(old['generation'])+1 and
                    new['previous_checkpoint_digest'] == old['digest'], 'checkpoint fork/orphan/gap generation')
            require(int(new['next_n']) >= int(old['next_n']), 'checkpoint cursor rollback')
        newest = records[-1]
        # Only the root may stand alone: a later generation needs its verified, hash-linked parent.
        require(len(records) >= 2 or newest['generation'] == '0',
                'missing/damaged checkpoint predecessor generation')
        warnings = []
        if damaged:
            warnings.append('damaged checkpoint slot ' + ','.join(map(str, damaged)) +
                            '; recovered the newest hash-linked generation and its prefix is re-executed; '
                            'rollback detection requires an external root')
        if absent and int(newest['generation']) >= 2:
            warnings.append('absent checkpoint slot ' + ','.join(map(str, absent)) +
                            '; a retained generation is missing; rollback detection requires an external root')
        return newest, warnings

    def initialize(self, fault=None):
        """Write the empty-prefix root, generation 0, into a directory with no slot at all."""
        require(not any(self.slot(index).exists() for index in range(SLOTS)) and
                not (self.directory / 'certificate.json').exists(), 'checkpoint root already exists')
        start = int(self.run['batch_start'])
        empty = summary_reference(start, start, int(self.run['max_t_per_explicit']), int(self.run['max_total_t']))
        return self._store(empty, 0, None, fault)

    def write(self, summary, fault=None):
        old = self.recover()[0]
        generation = int(old['generation'])+1
        require(generation <= 2**64-1, 'generation overflow')
        require(int(summary['next_n']) >= int(old['next_n']), 'checkpoint cursor rollback')
        return self._store(summary, generation, old['digest'], fault)

    def _store(self, summary, generation, parent, fault):
        obj = dict(schema=SCHEMA_IDS['checkpoint'], run_digest=H('RUN', canonical(self.run)),
                   generation=str(generation), previous_checkpoint_digest=parent,
                   **{key: self.run[key] for key in BINDING}, **summary)
        obj = seal(obj, 'CHECKPOINT')
        checkpoint_valid(obj, self.run)
        # Slot g mod 3 never holds generation g-1 or g-2; the root is created without replacement.
        write_atomic(self.slot(generation % SLOTS), canonical(obj), generation > 0, fault)
        recovered = self.recover()[0]
        require(recovered == obj, 'checkpoint independent re-read mismatch')
        return obj


def checker_digest():
    digest = hashlib.sha3_256(DOMAIN + b'CHECKER\0')
    for name in ('tools/frontier/ceml_frontier.py', 'tools/frontier/reference.py'):
        data = (ROOT / name).read_bytes().replace(b'\r\n', b'\n')
        digest.update(name.encode('ascii')+b'\0'+len(data).to_bytes(8,'big')+data)
    return digest.hexdigest()


def fixture_marker(run):
    return dict(schema='CEML-L1-ACCEPTANCE-FIXTURE-2', scope='NONSCIENTIFIC',
                run_digest=H('RUN', canonical(run)), fixture=run['run_id'])


def is_fixture(directory):
    return (local_path(directory) / 'acceptance.json').exists()


def load_manifest(directory, test=False):
    """Read and fully validate run.json and snapshot.json; a fixture must carry its exact marker."""
    directory = local_path(directory)
    run = load_record(directory / 'run.json', 'run')
    snap = load_record(directory / 'snapshot.json', 'snapshot')
    if test:
        require(parse_bytes(read_bounded(directory/'acceptance.json')) == fixture_marker(run),
                'acceptance fixture marker mismatch')
    validate_manifest(run, snap, test)
    return run, snap


def read_only_gate(directory):
    """Gate for inspect and replay, checked before any slot is read or any start recomputed.

    A directory claiming to be a fixture must be a predesignated fixture in full.
    Anything else is science and needs RUN1 status and a valid scientific manifest.
    """
    test = is_fixture(directory)
    require(science_readable(test), 'L1 inspects and replays only predesignated fixtures')
    return load_manifest(directory, test)[0]


def load_context(directory, test=False):
    run, snap = load_manifest(directory, test)
    from f1_build import verify_build
    build = verify_build()
    require(build['digest'] == run['native_build_digest'], 'native build identity mismatch')
    return run, snap


def predecessor(directory, run, test=False, seen=None):
    if int(run['batch_start']) == int(run['base_B']):
        require(run['predecessor_digest'] == genesis(run), 'genesis mismatch')
        return
    matches = []
    for path in local_path(directory).parent.glob('*/certificate.json'):
        obj = load_record(path, 'certificate')
        if obj['digest'] == run['predecessor_digest']:
            matches.append(path)
    require(len(matches) == 1, 'missing/duplicate immutable predecessor')
    prior = verify_batch(matches[0], test, seen)
    require(all(prior[key] == run[key] for key in IDENTITY) and
            prior['batch_end'] == run['batch_start'], 'predecessor chain gap/identity mismatch')


def ensure_chain_slot(directory, run):
    """Batches of one local chain share a directory; refuse duplicate/active work."""
    directory = local_path(directory)
    paths = [path for path in directory.parent.glob('*/run.json') if path.parent != directory]
    # This batch plus its siblings may not exceed what verify_batch can traverse.
    require(len(paths) < MAX_CHAIN, 'local chain directory resource limit')
    for path in paths:
        prior = load_record(path, 'run')
        if prior['run_id'] != run['run_id']:
            continue
        require(all(prior[key] == run[key] for key in IDENTITY), 'run ID reused across chain roots')
        require(run['batch_start'] != run['base_B'] and
                int(prior['batch_end']) <= int(run['batch_start']), 'duplicate/overlapping batch; rerun needs a new run ID')
        certificate_path = path.parent/'certificate.json'
        require(certificate_path.exists(), 'another batch of this chain is uncommitted')
        certificate = load_record(certificate_path, 'certificate')
        require(certificate['run_digest'] == H('RUN', canonical(prior)), 'damaged prior batch identity')


def commit_batch(directory, run, summary, test=False, fault=None):
    directory = local_path(directory)
    context, _ = load_context(directory, test)
    require(context == run, 'commit context changed')
    predecessor(directory, run, test)
    start, end = int(run['batch_start']), int(run['batch_end'])
    max_t, max_total = int(run['max_t_per_explicit']), int(run['max_total_t'])
    require(summary['next_n'] == str(end) and summary['pending'] is None, 'incomplete batch cannot commit')
    # A separate second computational pass over every n, after native completion.
    replay = summary_reference(start, end, max_t, max_total)
    require(summary == replay, 'full independent replay disagreement')
    certificate = seal(dict(schema=SCHEMA_IDS['certificate'], status='conditional_complete',
                            run_digest=H('RUN', canonical(run)), **{key:run[key] for key in BINDING},
                            checker_source_digest=checker_digest(),
                            independent_replay_digest=replay['transcript_digest'],
                            **{key:summary[key] for key in TOTALS}, unresolved_count='0', pending=None), 'CERTIFICATE')
    validate_shape(certificate, 'certificate')
    # Revalidate inputs and predecessor immediately before immutable promotion.
    require(load_context(directory, test)[0] == run, 'context changed before commit')
    predecessor(directory, run, test)
    write_atomic(directory / 'certificate.json', canonical(certificate), False, fault)
    require(verify_batch(directory/'certificate.json', test) == certificate, 'final certificate re-read mismatch')
    return certificate


def verify_batch(certificate_path, test=False, seen=None, _ledger_predecessors=None):
    path = local_path(certificate_path)
    require(path.name == 'certificate.json', 'immutable certificate filename required')
    cert = load_record(path, 'certificate')
    seen = set() if seen is None else set(seen)
    require(cert['digest'] not in seen and len(seen) < MAX_CHAIN, 'certificate cycle/depth limit')
    seen.add(cert['digest'])
    run, _ = load_context(path.parent, test)
    require(cert['run_digest'] == H('RUN', canonical(run)) and
            all(cert[key] == run[key] for key in BINDING), 'certificate/run identity mismatch')
    require(cert['checker_source_digest'] == checker_digest(), 'checker source identity mismatch')
    if _ledger_predecessors is None:
        predecessor(path.parent, run, test, seen)
    elif run['batch_start'] == run['base_B']:
        require(run['predecessor_digest'] == genesis(run), 'ledger genesis mismatch')
    else:
        prior = _ledger_predecessors.get(run['predecessor_digest'])
        require(prior is not None and all(prior[key] == run[key] for key in IDENTITY) and
                prior['batch_end'] == run['batch_start'], 'ledger predecessor missing/gap/identity mismatch')
    result = summary_reference(int(run['batch_start']), int(run['batch_end']),
                               int(run['max_t_per_explicit']), int(run['max_total_t']))
    require(result['pending'] is None and result['next_n'] == run['batch_end'], 'replay unresolved')
    require(all(cert[key] == result[key] for key in TOTALS), 'certificate full replay mismatch')
    require(cert['independent_replay_digest'] == result['transcript_digest'], 'replay digest mismatch')
    return cert


def ledger(directory, test=False):
    paths = list(local_path(directory).glob('*/certificate.json'))
    require(paths, 'empty ledger')
    paths.sort(key=lambda path: int(load_record(path, 'certificate')['batch_start']))
    certificates, verified = [], {}
    for path in paths:
        certificate = verify_batch(path, test, _ledger_predecessors=verified)
        require(certificate['digest'] not in verified, 'ledger duplicate certificate')
        verified[certificate['digest']] = certificate
        certificates.append(certificate)
    first = certificates[0]
    require(first['batch_start'] == first['base_B'] and first['predecessor_digest'] == genesis(first),
            'ledger missing genesis')
    for before, after in zip(certificates, certificates[1:]):
        require(all(before[key] == after[key] for key in IDENTITY) and
                before['batch_end'] == after['batch_start'] and after['predecessor_digest'] == before['digest'],
                'ledger duplicate/fork/gap/identity mismatch')
    return dict(status='NONSCIENTIFIC_FIXTURE' if test else 'conditional_chain',
                batches=str(len(certificates)), start=first['batch_start'], end=certificates[-1]['batch_end'],
                genesis_digest=first['predecessor_digest'], latest_certificate_digest=certificates[-1]['digest'])


def reference_replay(directory):
    """Pure-Python recomputation of one committed batch; no build, chain or authority check."""
    directory = local_path(directory)
    run = read_only_gate(directory)
    cert = load_record(directory / 'certificate.json', 'certificate')
    require(cert['run_digest'] == H('RUN', canonical(run)) and
            all(cert[key] == run[key] for key in BINDING), 'certificate/run identity mismatch')
    result = summary_reference(int(run['batch_start']), int(run['batch_end']),
                               int(run['max_t_per_explicit']), int(run['max_total_t']))
    require(result['pending'] is None and result['next_n'] == run['batch_end'], 'replay unresolved')
    require(all(cert[key] == result[key] for key in TOTALS) and
            cert['independent_replay_digest'] == result['transcript_digest'], 'reference replay disagreement')
    return dict(status='REFERENCE_REPLAY_MATCH', scope='arithmetic only; not a chain, build or authority check',
                batch_start=run['batch_start'], batch_end=run['batch_end'], digest=cert['digest'],
                transcript_digest=result['transcript_digest'])


def inspect_batch(directory):
    """Read-only diagnosis of one batch directory; it changes and promotes nothing."""
    directory = local_path(directory)
    require(directory.is_dir(), 'batch directory missing')
    run = read_only_gate(directory)
    store = CheckpointStore(directory, run)
    slots = {}
    for index in range(SLOTS):
        try:
            found = store.read_slot(index)
        except Refusal as error:
            slots[str(index)] = 'REFUSED: ' + str(error)
            continue
        slots[str(index)] = ('ABSENT' if found is None else 'DAMAGED' if found is DAMAGED else
                             'RECORD generation ' + found['generation'] + ' next_n ' + found['next_n'])
    try:
        newest, warnings = store.recover()
        recovery = dict(status='RECOVERABLE', generation=newest['generation'], next_n=newest['next_n'],
                        pending=newest['pending'], warnings=warnings)
    except Refusal as error:
        recovery = dict(status='REFUSED', reason=str(error))
    names = sorted(path.name for path in directory.iterdir())
    return dict(status='INSPECTION_ONLY', run_id=run['run_id'], batch_start=run['batch_start'],
                batch_end=run['batch_end'], slots=slots, recovery=recovery,
                certificate='PRESENT-UNVERIFIED' if 'certificate.json' in names else 'ABSENT',
                temporaries=str(sum(name.endswith('.tmp') for name in names)))


def prepare_fixture(directory, run):
    directory = local_path(directory)
    require(not directory.exists(), 'fixture output already exists')
    directory.mkdir(parents=True)
    for name, obj in (('run.json', run), ('snapshot.json', snapshot()), ('acceptance.json', fixture_marker(run))):
        write_atomic(directory / name, canonical(obj))


def run_batch(directory, run, test=False):
    """Root checkpoint, one native scan, next generation, then commit only a complete result."""
    context, _ = load_context(directory, test)
    require(context == run, 'batch context changed')
    predecessor(directory, run, test)
    store = CheckpointStore(directory, run)
    store.initialize()
    started = time.perf_counter()
    summary = consume_native(int(run['batch_start']), int(run['batch_end']),
                             int(run['max_t_per_explicit']), int(run['max_total_t']))
    scanned = time.perf_counter() - started
    store.write(summary)
    if summary['pending'] is not None:
        return dict(status='INCOMPLETE', next_n=summary['next_n'], pending=summary['pending'])
    cert = commit_batch(directory, run, summary, test)
    return dict(status='NONSCIENTIFIC_FIXTURE' if test else 'COMMITTED', digest=cert['digest'],
                batch_end=run['batch_end'], scan_and_check_seconds=format(scanned, '.6f'))


def start_batch(manifest, out):
    """Create one scientific batch directory. Every gate is checked before anything is written."""
    run = load_record(manifest, 'run')
    authority = run1_gate(run)
    validate_manifest(run, snapshot())
    output = local_path(out)
    require(not output.exists(), 'batch directory already exists')
    ensure_chain_slot(output, run)
    # Build identity and predecessor are checked here too, so a refusal leaves no directory behind.
    from f1_build import verify_build
    require(verify_build()['digest'] == run['native_build_digest'], 'native build identity mismatch')
    predecessor(output, run)
    output.mkdir(parents=True)
    write_atomic(output/'run.json', canonical(run))
    write_atomic(output/'snapshot.json', canonical(snapshot()))
    write_atomic(output/'authority.json', authority)
    return run_batch(output, run)


def resume_batch(directory, test=False):
    run, _ = load_context(directory, test)
    if not test:
        run1_gate(run)
        ensure_chain_slot(directory, run)
    require(not (local_path(directory)/'certificate.json').exists(),
            'batch already has a final certificate; use verify-batch')
    predecessor(directory, run, test)
    store = CheckpointStore(directory, run)
    old, warnings = store.recover()
    start, end, cursor = int(run['batch_start']), int(run['batch_end']), int(old['next_n'])
    max_t, max_total = int(run['max_t_per_explicit']), int(run['max_total_t'])
    if cursor > start:
        replayed = consume_native(start, cursor, max_t, max_total)
        # The native prefix must be complete to the recovered cursor and agree on every total.
        require(replayed['next_n'] == old['next_n'] and replayed['pending'] is None,
                'resume native prefix mismatch')
        for key in TOTALS[:-1]:
            require(replayed[key] == old[key], 'resume native prefix mismatch')
    # Re-scan the whole small batch from its original start: avoids serializing hash state
    # or discounting failed attempts. The validated prefix is checked before suffix work.
    summary = consume_native(start, end, max_t, max_total)
    store.write(summary)
    if summary['pending'] is not None:
        return dict(status='INCOMPLETE', next_n=summary['next_n'], pending=summary['pending'], warnings=warnings)
    cert = commit_batch(directory, run, summary, test)
    return dict(status='NONSCIENTIFIC_FIXTURE' if test else 'COMMITTED', digest=cert['digest'], warnings=warnings)


def canonical_decimal(text, label):
    require(isinstance(text, str) and re.fullmatch(r'0|[1-9][0-9]{0,8191}', text) is not None,
            'noncanonical decimal: ' + label)
    return int(text)


def expected_acknowledgement(base_kind):
    snap = snapshot()
    require(base_kind in ('published', 'operational'), 'base kind')
    digest = validate_snapshot(snap)
    return snap, digest, ':'.join((digest, base_kind, snap[base_kind]['B']))


def prepare_authority(authority_id, base_kind, batch_start, batch_end, acknowledge, owner_instruction):
    """Record the operator's explicit authority for exactly one batch. Never fills in the acknowledgement."""
    run1_status()
    snap, digest, expected = expected_acknowledgement(base_kind)
    require(acknowledge == expected, 'acknowledgement is not snapshot_digest:base_kind:base_B')
    require(re.fullmatch(r'[a-zA-Z0-9_.:-]{1,128}', authority_id) is not None and
            authority_id != 'L1-NONSCIENTIFIC', 'authority identifier')
    require(isinstance(owner_instruction, str) and owner_instruction.isascii() and
            0 < len(owner_instruction.strip()) <= 2048, 'owner instruction must be nonempty ASCII')
    base = int(snap[base_kind]['B'])
    start, end = canonical_decimal(batch_start, 'batch start'), canonical_decimal(batch_end, 'batch end')
    require(base <= start < end and end - start <= 14400, 'invalid interval/base')
    require(start != base or end - start == 144, 'first RUN1 pilot is exactly 144 starts')
    record = dict(zip(AUTHORITY_KEYS, (authority_id, digest, base_kind, snap[base_kind]['B'], acknowledge,
                                       batch_start, batch_end, owner_instruction)))
    LOCAL.mkdir(parents=True, exist_ok=True)
    # The previous batch keeps its own copy as authority.json, so replacement loses no evidence.
    write_atomic(LOCAL / 'run1_authorization.json', canonical(record), True)
    return dict(status='AUTHORITY_RECORDED_NOT_EXECUTED', authority_id=authority_id,
                batch_start=batch_start, batch_end=batch_end)


def prepare_manifest(out, authority_id, acknowledge, max_t, max_total, run_id=None, base_kind=None,
                     after_certificate=None, width='144'):
    """Write one canonical run manifest. It executes nothing and accepts nothing by default."""
    run1_status()
    from f1_build import verify_build
    build = verify_build()
    if after_certificate is None:
        require(run_id is not None and base_kind is not None, 'first batch needs --run-id and --base-kind')
        snap, digest, expected = expected_acknowledgement(base_kind)
        start, previous = snap[base_kind]['B'], None
        require(width == '144', 'first RUN1 pilot is exactly 144 starts')
    else:
        require(run_id is None and base_kind is None, 'a continuation inherits run ID and base from its predecessor')
        prior = verify_batch(after_certificate)
        run_id, base_kind = prior['run_id'], prior['base_kind']
        snap, digest, expected = expected_acknowledgement(base_kind)
        require(prior['snapshot_digest'] == digest and prior['native_build_digest'] == build['digest'],
                'predecessor snapshot/build identity differs from the current tree')
        start, previous = prior['batch_end'], prior['digest']
    require(acknowledge == expected, 'acknowledgement is not snapshot_digest:base_kind:base_B')
    span = canonical_decimal(width, 'width')
    run = dict(schema=SCHEMA_IDS['run'], run_id=run_id, run1_authority_id=authority_id,
               snapshot_digest=digest, base_kind=base_kind, base_B=snap[base_kind]['B'],
               accepted_assumption_ack=acknowledge, batch_start=start, batch_end=str(int(start) + span),
               predecessor_digest='0'*64, ruleset_id=RULESET, table_digest=reference.table_digest(),
               native_build_digest=build['digest'], map_id='T-shortened-v1',
               max_t_per_explicit=max_t, max_total_t=max_total)
    run['predecessor_digest'] = genesis(run) if previous is None else previous
    validate_manifest(run, snap)
    write_atomic(out, canonical(run))
    return dict(status='MANIFEST_WRITTEN_NOT_EXECUTED', run_digest=H('RUN', canonical(run)),
                batch_start=run['batch_start'], batch_end=run['batch_end'],
                predecessor_digest=run['predecessor_digest'])


def selftest():
    """Predesignated small-integer engineering fixtures and overhead-inclusive timings only."""
    l1_gate()
    from f1_build import verify_build
    build = verify_build()
    root = LOCAL / 'acceptance' / ('session-' + uuid.uuid4().hex)
    results, previous = [], None
    for group, name in (('chain', 'L1-fixture-a'), ('chain', 'L1-fixture-successor'),
                        ('single-b', 'L1-fixture-b'), ('single-c', 'L1-fixture-c'),
                        ('single-wide', 'L1-fixture-wide')):
        run = fixture_run(name, build_digest=build['digest'])
        if name == 'L1-fixture-successor':
            run['predecessor_digest'] = previous
        directory = root / group / name
        prepare_fixture(directory, run)
        started = time.perf_counter()
        outcome = run_batch(directory, run, True)
        elapsed = time.perf_counter() - started
        require(outcome['status'] == 'NONSCIENTIFIC_FIXTURE', 'fixture did not complete')
        cert = load_record(directory / 'certificate.json', 'certificate')
        previous = cert['digest']
        results.append(dict(fixture=name, batch_size=str(int(run['batch_end'])-int(run['batch_start'])),
                            explicit_count=cert['counts']['explicit_count'], t_steps=cert['explicit_t_steps'],
                            scan_and_check_seconds=outcome['scan_and_check_seconds'],
                            elapsed_seconds=format(elapsed, '.6f'), digest=cert['digest']))
    started = time.perf_counter()
    chain = ledger(root / 'chain', True)
    report = dict(scope='L1-NONSCIENTIFIC', status='fixtures_pass', protocol=PROTOCOL,
                  native_build_digest=build['digest'],
                  directory_flush_supported='yes' if directory_flush(root) else 'no', results=results,
                  ledger=dict(chain, elapsed_seconds=format(time.perf_counter() - started, '.6f')))
    write_atomic(root/'report.json', canonical(report))
    return report


def main():
    sys.set_int_max_str_digits(10000)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('rules')
    p = sub.add_parser('snapshot'); p.add_argument('--file', required=True)
    sub.add_parser('selftest')
    p = sub.add_parser('prepare-authority')
    for name in ('authority-id', 'base-kind', 'batch-start', 'batch-end', 'acknowledge', 'owner-instruction'):
        p.add_argument('--' + name, required=True)
    p = sub.add_parser('prepare-manifest')
    for name in ('out', 'authority-id', 'acknowledge', 'max-t-per-explicit', 'max-total-t'):
        p.add_argument('--' + name, required=True)
    for name in ('run-id', 'base-kind', 'after-certificate'):
        p.add_argument('--' + name)
    p.add_argument('--width', default='144')
    p = sub.add_parser('pilot'); p.add_argument('--manifest', required=True); p.add_argument('--out', required=True)
    p = sub.add_parser('resume'); p.add_argument('--batch-dir', required=True)
    p = sub.add_parser('inspect'); p.add_argument('--batch-dir', required=True)
    p = sub.add_parser('replay'); p.add_argument('--batch-dir', required=True)
    p = sub.add_parser('verify-batch'); p.add_argument('--certificate', required=True)
    p = sub.add_parser('ledger'); p.add_argument('--dir', required=True)
    args = parser.parse_args()
    if args.command == 'rules':
        reference.check_rules()
        result = dict(status='rules_pass', scope='NONSCIENTIFIC', table_digest=reference.table_digest())
    elif args.command == 'snapshot':
        obj = parse_bytes(read_bounded(args.file))
        if isinstance(obj, dict) and obj.get('schema') == V1_SNAPSHOT_SCHEMA:
            obj, digest, _ = v1_snapshot(args.file)
            result = dict(status='frozen_version_1_research_only_not_runnable', digest=digest)
        else:
            obj = load_record(args.file, 'snapshot')
            result = dict(status='research_only_unaccepted', digest=validate_snapshot(obj),
                          provenance=obj['provenance'])
        result.update(observed_at_utc=obj['observed_at_utc'], published=obj['published'],
                      operational=obj['operational'])
    elif args.command == 'selftest':
        result = selftest()
    elif args.command == 'prepare-authority':
        result = prepare_authority(args.authority_id, args.base_kind, args.batch_start, args.batch_end,
                                   args.acknowledge, args.owner_instruction)
    elif args.command == 'prepare-manifest':
        result = prepare_manifest(args.out, args.authority_id, args.acknowledge, args.max_t_per_explicit,
                                  args.max_total_t, args.run_id, args.base_kind, args.after_certificate, args.width)
    elif args.command == 'pilot':
        result = start_batch(args.manifest, args.out)  # every gate refuses before any output exists
    elif args.command == 'resume':
        run = load_record(Path(args.batch_dir)/'run.json', 'run')
        run1_gate(run)
        result = resume_batch(args.batch_dir)
    elif args.command in ('inspect', 'replay'):
        # Both functions apply read_only_gate before reading any slot or recomputing any start.
        result = (inspect_batch if args.command == 'inspect' else reference_replay)(args.batch_dir)
    elif args.command == 'verify-batch':
        test = is_fixture(local_path(args.certificate).parent)
        require(science_readable(test), 'L1 verifies only predesignated fixtures')
        cert = verify_batch(args.certificate, test)
        result = dict(status='NONSCIENTIFIC_FIXTURE' if test else 'conditional_complete', digest=cert['digest'],
                      batch_start=cert['batch_start'], batch_end=cert['batch_end'])
    else:
        dirs = list(local_path(args.dir).glob('*/certificate.json'))
        test = bool(dirs) and all((p.parent/'acceptance.json').exists() for p in dirs)
        require(science_readable(test), 'L1 ledger accepts only fixtures')
        result = ledger(args.dir, test)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except NativeFailure as error:
        folder = LOCAL/'refusals'
        folder.mkdir(parents=True, exist_ok=True)
        write_atomic(folder/(uuid.uuid4().hex+'.json'), canonical(error.record))
        print(json.dumps(dict(status='REFUSED', reason=str(error), anomaly_digest=H('ANOMALY', canonical(error.record)))))
        sys.exit(2)
    except (Refusal, BuildRefusal, ValueError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps(dict(status='REFUSED', reason=str(error) if isinstance(error, (Refusal, BuildRefusal)) else type(error).__name__)))
        sys.exit(2)
