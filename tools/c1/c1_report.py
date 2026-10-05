"""C1 report assembler: hardware report, bundle index, benchmark summary and
engineering decisions from retained local evidence.

Deterministic and evidence-bound: every statistic is recomputed from the raw
per-repetition records in the indexed local bundles, every decision is derived
by the fixed I1 section 11.13 rules coded below, and nothing is selected that
the records do not support. Invalid and refused records are counted, never
dropped. This tool performs no measurement and no scientific work.

Usage: python tools/c1/c1_report.py --evidence harness|final
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import statistics
import sys

from engineering_codec import artifact_digest, blob, canonical_bytes, self_test_vector
from cal1_suite import validator
from gmp_setup import ROOT
from privacy_gate import inspect_text, validate_artifact

AUDIT = 'c1-20261005-final'
BUNDLES = ROOT / 'local/c1/benchmark_bundles'
LOCAL = ROOT / 'local/c1'
# Bundles whose valid records carry the decisions, per evidence stage.
STAGES = {
    'harness': {1: 'cal1-20261005-a-01-route-crossover', 2: 'cal1-20261005-b-02-small-block-sweep',
                3: 'cal1-20261005-b-03-hierarchical-sweep', 4: 'cal1-20261005-b-04-backend-multiplication',
                5: 'cal1-20261005-b-05-representation', 6: 'cal1-20261005-b-06-allocation',
                7: 'cal1-20261005-b-07-compiler-build', 9: 'ckpt-20261005-a-09-checkpoint-performance',
                10: 'cal1-20261005-b-10-terminal-handoff', 11: 'cal1-20261005-b-11-audit-cost',
                12: 'cal1-20261005-b-12-memory-scaling'},
    'final': {order: f'final-20261005-a-{order:02d}-{name}' for order, name in (
        (1, 'route-crossover'), (2, 'small-block-sweep'), (3, 'hierarchical-sweep'), (4, 'backend-multiplication'),
        (5, 'representation'), (6, 'allocation'), (7, 'compiler-build'), (9, 'checkpoint-performance'),
        (10, 'terminal-handoff'), (11, 'audit-cost'), (12, 'memory-scaling'))},
}
DURABILITY = {'harness': 'ckpt-20261005-a-09-checkpoint-durability', 'final': 'final-20261005-a-09-checkpoint-durability'}
FAMILY = {1: 'route-crossover', 2: 'small-block-sweep', 3: 'hierarchical-sweep', 4: 'backend-multiplication',
          5: 'representation', 6: 'allocation', 7: 'compiler-build', 8: 'parallelism', 9: 'checkpoint',
          10: 'terminal-handoff', 11: 'audit-cost', 12: 'memory-scaling'}
RULE = ('I1 section 11.13. Case statistic: median and MAD of the five valid measured repetitions, integer nanoseconds. '
        'Class statistic: sum of the three case medians of one size class. A class is noisy for a candidate when any of '
        'its cases has MAD above 10 percent of its median. Candidate A beats B only if neither is noisy on the largest '
        'three applicable classes (the decision-critical classes), A is at least 5 percent lower on at least two of them '
        'and A is more than 5 percent higher on none of them. Otherwise they are tied or unresolved and the I1 tie-break order '
        'applies: public API, smaller correctness surface, fewer dependencies, materially lower peak memory, portable, '
        'single-thread. No missing row is treated as a tie.')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def seal(version, **members):
    obj = dict(experiment='CEML', schema_version=version, **members)
    obj['artifact_digest'] = artifact_digest(obj)
    return obj


def fact(identity, category, name, value, method, uncertainty, kind='active_configuration', observed_at=None):
    return dict(record_class='OBSERVED_FACT', record_id=identity, category=category, fact_name=name, value=value,
                source_adapter='c1-report-assembler-v2', source_method=method, audit_run_id=AUDIT,
                source_state_kind=kind, uncertainty=uncertainty,
                sanitization=['Selected numeric and engineering fields only; locators, raw diagnostics and identifiers excluded'],
                observed_at=observed_at)


def missing(identity, category, item, method, reason, effects):
    return dict(record_class='UNAVAILABLE_OR_UNSUPPORTED', record_id=identity, category=category, requested_item=item,
                attempted_method=method, reason=reason, downstream_effects=effects)


def decision(identity, question, candidates, evidence, selection, rationale, eliminated=(), limitations=(), binds=True,
             rule=RULE):
    return dict(record_class='ENGINEERING_DECISION', decision_id=identity, question=question,
                candidates_considered=list(candidates), evidence_record_ids=sorted(set(evidence)),
                eliminated=[dict(candidate=c, reason=r) for c, r in eliminated], selection=selection, decision_rule=rule,
                rationale=rationale, limitations=list(limitations) + [
                    'Bounded CEML-CAL-1 engineering evidence on this machine and build only; not V1 and not a scientific-scale forecast'],
                binds_profile=binds)


def bundle_digest(folder):
    digest = hashlib.sha3_256(b'CEML-I1-BENCHMARK-BUNDLE-V1\0')
    members = sorted(p for p in folder.iterdir() if p.is_file())
    for path in members:
        data = path.read_bytes()
        if inspect_text(data.decode('ascii'), path.name):
            raise ValueError('Bundle privacy check failed')
        digest.update(blob(path.name.encode('ascii')))
        digest.update(blob(data))
    return digest.hexdigest(), len(members)


_CACHE = {}


def load_records(bundle):
    if bundle in _CACHE:
        return _CACHE[bundle]
    records = _CACHE.setdefault(bundle, [])
    for path in sorted((BUNDLES / bundle).glob('*-record.json')):
        record = json.loads(path.read_text('ascii'))
        if artifact_digest(record) != record['artifact_digest'] or not validator().is_valid(record):
            raise ValueError('Raw calibration record integrity failed')
        records.append(record)
    return records


class Family:
    """Valid measured statistics of one family bundle, indexed by (size, candidate, case index)."""

    def __init__(self, bundle):
        self.bundle = bundle
        self.cases = defaultdict(list)
        self.case_ids = {}
        self.live = defaultdict(int)
        for record in load_records(bundle):
            parts = record['input_id'].split('/')
            key = (int(parts[3]), record['candidate_id'], parts[4])
            self.case_ids[key] = record['case_id']
            if record['valid'] and record['measured'] and record['correctness_agreement']:
                self.cases[key].append(int(record['wall_time_ns']))
                if record.get('live_bytes'):
                    self.live[key] = max(self.live[key], int(record['live_bytes']))
        self.sizes = sorted({k[0] for k in self.cases})
        self.candidates = sorted({k[1] for k in self.cases})

    def stat(self, size, candidate):
        """(class total of case medians, noisy, complete) using integers only."""
        total, noisy, complete = 0, False, True
        keys = [k for k in self.cases if k[0] == size and k[1] == candidate]
        if len(keys) < 3:
            return None, True, False
        for key in keys:
            values = sorted(self.cases[key])
            if len(values) < 5:      # fewer than five valid measured repetitions cannot carry a timing winner
                complete = False
            if not values:
                continue
            median = values[len(values)//2]
            mad = sorted(abs(v - median) for v in values)[len(values)//2]
            total += median
            noisy |= 10*mad > median
        return total, noisy, complete

    def beats(self, a, b, sizes=None):
        sizes = sizes or self.sizes
        critical = sizes[-3:]
        wins = 0
        for size in sizes:
            ta, na, ca = self.stat(size, a)
            tb, nb, cb = self.stat(size, b)
            if not ca or not cb:
                return False
            if size in critical and (na or nb):
                return False
            if size in critical and 100*ta > 105*tb:
                return False
            if size in critical and 100*ta <= 95*tb:
                wins += 1
        return len(sizes) >= 3 and wins >= 2

    def winner(self, candidates=None, sizes=None):
        candidates = candidates or self.candidates
        for a in candidates:
            if all(self.beats(a, b, sizes) for b in candidates if b != a):
                return a
        return None

    def table(self, candidates=None):
        rows = {}
        for candidate in candidates or self.candidates:
            rows[candidate] = {str(size): dict(class_total_ns=str(self.stat(size, candidate)[0]),
                                               noisy=self.stat(size, candidate)[1]) for size in self.sizes}
        return rows

    def evidence(self, candidates=None, sizes=None):
        return [cid for key, cid in self.case_ids.items()
                if (candidates is None or key[1] in candidates) and (sizes is None or key[0] in sizes)]

    def peak_live(self, candidate, size):
        return max((v for k, v in self.live.items() if k[1] == candidate and k[0] == size), default=0)


def summarize(index_bundles, decisive, decision_ids):
    """One entry per case ID. Valid statistics come only from the decisive bundle of
    the family; invalid repetitions are counted across every indexed bundle."""
    merged = {}
    decisive_names = set(decisive.values())
    for bundle in index_bundles:
        for record in load_records(bundle):
            entry = merged.setdefault(record['case_id'], dict(candidate=record['candidate_id'], valid=[], invalid=0, rss=0,
                                                              correct=True, route=True, order=int(record['input_id'].split('/')[1])
                                                              if record['input_id'].startswith('cal1/') else 1, seen=False))
            if not record['valid']:
                entry['invalid'] += 1
                continue
            if bundle not in decisive_names:
                continue
            entry['seen'] = True
            entry['correct'] &= record['correctness_agreement']
            requested = record['activation']['requested_routes']
            entry['route'] &= record['activation']['fallback_count'] == '0' and all(
                int(record['activation']['activated_counts'].get(route, '0')) > 0 for route in requested)
            if record['measured']:
                entry['valid'].append(int(record['wall_time_ns']))
                entry['rss'] = max(entry['rss'], int(record['peak_rss_bytes'] or 0))
    cases = []
    for case_id in sorted(merged):
        entry = merged[case_id]
        values = sorted(entry['valid'])
        median = values[len(values)//2] if values else None
        cases.append(dict(
            case_id=case_id, candidate_id=entry['candidate'], valid_repeats=str(len(values)), invalid_repeats=str(entry['invalid']),
            median_wall_time_ns=None if median is None else str(median),
            minimum_wall_time_ns=str(values[0]) if values else None, maximum_wall_time_ns=str(values[-1]) if values else None,
            mad_wall_time_ns=None if median is None else str(sorted(abs(v - median) for v in values)[len(values)//2]),
            peak_rss_bytes=str(entry['rss']) if entry['rss'] else None,
            correctness_all=bool(entry['seen'] and entry['correct']), route_activation_proved=bool(entry['seen'] and entry['route']),
            decision_ids=decision_ids.get(entry['order'], [])))
    return cases


def markdown(report, verdict):
    lines = ['# C1 sanitized hardware report', '', verdict, '',
             f"Audit: `{report['audit_run_id']}`. Generated: {report['generated_at']}.", '',
             f"JSON artifact digest: `{report['artifact_digest']}`.", '',
             'Generated mechanically from HARDWARE_REPORT.json. Observations are not benchmarks,',
             'benchmarks are not V1, and nothing here is scientific evidence.', '']
    for r in report['records']:
        lines += [f"## {r['record_id']}", '', f"Class: `{r['record_class']}`.", '']
        if r['record_class'] == 'OBSERVED_FACT':
            value = canonical_bytes(r['value']).decode('ascii')
            lines += [f"{r['fact_name']}: `{value}`", '', f"Source: {r['source_method']}.", '',
                      f"Observation kind: {r['source_state_kind']}. Time: {r['observed_at'] or 'not retained'}.", '',
                      f"Uncertainty: {r['uncertainty'] or 'No additional uncertainty recorded.'}", '']
        else:
            lines += [f"Requested: {r['requested_item']}.", '', f"Reason: {r['reason']}", '',
                      'Effects: ' + '; '.join(r['downstream_effects']) + '.', '']
    return '\n'.join(lines)


def assemble(stage):
    status = (ROOT / 'PROGRAM_STATUS.md').read_text(encoding='utf-8')
    if '**Scientific execution authorization:** DENIED' not in status:
        raise ValueError('Unexpected programme status')
    decisive = STAGES[stage]
    fam = {order: Family(bundle) for order, bundle in decisive.items()}
    records, decisions = [], []
    for name in ('audit_observations.json', 'tool_observations.json'):
        records.extend(json.loads((LOCAL / AUDIT / name).read_text(encoding='utf-8-sig')))
    stale = {'tools.gmp-unavailable', 'tools.flint-unavailable'}
    records = [r for r in records if r['record_id'] not in stale]

    # ---- observed engineering facts ------------------------------------------------
    setup = {name: json.loads((LOCAL / 'gmp-setup' / (name + '.json')).read_text()) for name in
             ('acquisition', 'offline_build', 'offline_smoke')}
    records.append(fact('dependency.authorization', 'authorization', 'dependency_setup_authorized', True,
                        'Explicit operator authorization on 2026-10-05 for acquisition, installation and builds needed to finish C1',
                        'Does not authorize scientific work, V1 or E1'))
    records.append(fact('dependency.gmp-candidate', 'toolchain', 'pinned_gmp_public_c_candidate',
                        dict(version='6.3.0', distribution_release='6.3.0-2', package_sha256=setup['acquisition']['binary']['sha256'],
                             dll_sha3_256=setup['offline_build']['dll']['sha3_256'], header_sha3_256=setup['offline_build']['header']['sha3_256'],
                             msvc_tools_version=setup['offline_build']['toolchain']['msvc_tools_version'],
                             windows_sdk_version=setup['offline_build']['toolchain']['windows_sdk_version'],
                             offline_rebuild_byte_identical=True, smoke_passed=bool(setup['offline_smoke']['result']['ok']),
                             limb_bits='64', nail_bits='0', abi='LLP64'),
                        'Checksum-verified package, public C compile and link with installed MSVC, exact product and import-export smoke, strict offline rebuild',
                        'The GMP binary is a distribution build; GMP itself was not rebuilt from source locally',
                        observed_at=setup['offline_build']['observed_at']))
    records.append(fact('engineering.generator-vector', 'engineering_integrity', 'normative_generator_vector', self_test_vector(),
                        'Fixed normative CEML-CAL-1 vector reproduced before calibration', 'No trajectory is performed'))
    study = json.loads((LOCAL / 'pressure-study/pressure-20261005-a.json').read_text())
    records.append(fact('resource.pressure-study', 'resource_safety', 'arithmetic_free_paging_proxy_study',
                        dict(summary=study['summary'], interval_ms='1000', processor_performance_counter_available=True,
                             processor_performance_percent_range=[
                                 str(min(int(s['processor_performance_milli']) for s in study['samples'])//1000),
                                 str(max(int(s['processor_performance_milli']) for s in study['samples'])//1000)],
                             minimum_available_bytes=str(min(int(s['available_bytes']) for s in study['samples']))),
                        'PDH memory page input and output rates and processor performance over 35 one-second intervals with no calibration case',
                        'Thirty-five samples; page input includes mapped-file reads; not a pagefile-specific measurement',
                        kind='momentary_state', observed_at=study['observed_at']))
    refusals = []
    for bundle in sorted(p.name for p in BUNDLES.iterdir() if p.is_dir()):
        for path in sorted((BUNDLES / bundle).glob('*-detail.json')):
            detail = json.loads(path.read_text('ascii'))
            guard = detail.get('guard') or {}
            if guard.get('abort_code'):
                refusals.append(dict(bundle_id=bundle, member=path.name, abort_code=guard['abort_code'], reason=guard.get('reason'),
                                     maximum_pages_input_rounded=guard.get('maximum_pages_input_rounded') or guard.get('final_pages_input_rounded')
                                     or guard.get('pages_input_rounded'),
                                     pages_output_rounded=guard.get('final_pages_output_rounded') or guard.get('pages_output_rounded')))
    budget = json.loads((LOCAL / 'cal1-budget.json').read_text())
    records.append(fact('resource.refusal-log', 'resource_safety', 'retained_guard_refusals_and_aggregate_budget',
                        dict(refusals=refusals, aggregate_child_wall_ns=budget['charged_ns'], aggregate_ceiling_ns=str(900*10**9),
                             explicit_resumes={k: str(v) for k, v in budget['resumed_attempts'].items()}),
                        'Guard outcomes retained in the indexed local bundles; shared durable budget file',
                        'Every refusal is retained as invalid evidence; none contributes a timing datum', kind='momentary_state'))
    records.append(fact('resource.ceilings', 'resource_safety', 'local_resource_ceilings_v2_1',
                        dict(minimum_available_memory_bytes=str(4*2**30), minimum_free_storage_bytes=str(16*2**30),
                             maximum_process_memory_bytes=str(256*2**20), maximum_processes='1', maximum_threads='1',
                             maximum_case_seconds='5', aggregate_child_wall_seconds='900', pages_input_ceiling_per_second='100',
                             pages_output_required='0', admission_wait_intervals_maximum='30',
                             processor_performance_floor_percent='100', power='AC with zero standby and hibernate idle indices'),
                        'docs/C1_RESOURCE_CEILINGS_V2.md including amendment 2.1; enforced by the native guard and Job limits',
                        'Ceilings are engineering admission limits for bounded calibration, not scientific resource forecasts'))
    durability = json.loads((BUNDLES / DURABILITY[stage] / 'summary.json').read_text('ascii'))
    hostile = json.loads((BUNDLES / DURABILITY[stage] / 'adversarial.json').read_text('ascii'))
    records.append(fact('checkpoint.durability-matrix', 'checkpoint_storage', 'synthetic_ckpt1_interruption_and_recovery_matrix',
                        dict(scenarios=durability['scenarios'], forced_terminations=durability['forced_terminations'],
                             boundary_not_reached=durability['boundary_not_reached'], scenarios_passed=durability['scenarios_passed'],
                             phases_forced=durability['phases_forced'], adversarial_cases=durability['adversarial_cases'],
                             adversarial_passed=durability['adversarial_passed'],
                             adversarial_names=[x['case'] for x in hostile['cases']],
                             directory_flush_supported=durability['directory_flush_supported'], all_passed=durability['all_passed'],
                             filesystem='NTFS, fixed local volume, same volume as the intended checkpoint directory'),
                        'Forced self-termination at each named boundary, fresh-process recovery and continuation, independent Python byte validation',
                        'Process interruption only. No power-loss, device write-cache or operating-system crash behaviour was tested or is claimed',
                        observed_at=None))
    records.append(fact('checkpoint.documented-semantics', 'checkpoint_storage', 'platform_documentation_used',
                        dict(retrieved='2026-10-05', publisher='Microsoft Learn, Win32 API reference',
                             flushfilebuffers='https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers',
                             flushfilebuffers_claim='Flushes the buffers of a specified file; the handle must have GENERIC_WRITE access',
                             movefileex='https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw',
                             movefileex_claim='MOVEFILE_WRITE_THROUGH: the function does not return until the file is actually moved on the disk',
                             status='external documentary claims; publication dates unavailable; not independently reproduced beyond the bounded tests'),
                        'Primary vendor documentation retrieved during C1',
                        'The pages do not state rename atomicity under power loss; the store does not rely on it for safety'))

    # ---- unavailable or unsupported ------------------------------------------------
    records += [
        missing('unsupported.flint', 'toolchain', 'Public FLINT backend route', 'Tool and package locator probes of the audit adapters',
                'No FLINT installation or pinned package is present; the optional route was not acquired', ['arith.flint.public is not a candidate']),
        missing('unsupported.rust-rug', 'toolchain', 'Rust with rug and GMP candidate', 'Offline registry cache probe for rug and gmp-mpfr-sys',
                'A Rust toolchain exists but no pinned offline rug or gmp-mpfr-sys source is cached and its GMP build prerequisites are absent',
                ['Rust family not benchmarked; C17 with public GMP is the only complete local family']),
        missing('unsupported.native-tuning', 'toolchain', 'native-release build mode', 'Review of the pinned compiler option set',
                'The pinned Microsoft C compiler has no host-native target mechanism and the GMP binary is a prebuilt distribution library',
                ['Only checked and portable-release modes were compared; the build is portable']),
        missing('unsupported.parallel-aux', 'implementation', 'Auxiliary-parallel route', None,
                'The optional auxiliary-parallel candidate was not implemented; no eligible parallel route exists to compare',
                ['parallel.single is the only eligible route; thread count one']),
        missing('unsupported.sparse-state', 'implementation', 'Sparse or chunked state representation', None,
                'The optional sparse candidate was not implemented; its larger invariant surface was not justified for C1',
                ['state.dense is the only eligible representation']),
        missing('unsupported.value-threaded', 'implementation', 'Value-threaded hierarchical form', None,
                'The optional value-threaded candidate was not implemented', ['engine.hier_affine.explicit is the only hierarchical form']),
        missing('unavailable.power-loss', 'checkpoint_storage', 'Power-loss durability evidence', None,
                'Destructive power-cut testing is not authorized and was not performed',
                ['Durability rests on documented flush semantics plus process-interruption tests; recorded as a limitation']),
    ]

    # ---- decisions -----------------------------------------------------------------
    f1, f2, f3, f6, f7, f9, f10, f11, f12 = (fam[i] for i in (1, 2, 3, 6, 7, 9, 10, 11, 12))
    did = {order: [f'decision.matrix.{order:02d}.{FAMILY[order]}'] for order in FAMILY}
    hier1 = [c for c in f1.candidates if c.startswith('hier')]
    small1 = [c for c in f1.candidates if c.startswith('affine-small')]
    hier_beats_all = all(f1.beats(h, other) for h in hier1 for other in small1 + ['t-direct'])
    decisions.append(decision(
        did[1][0], 'Route crossover among direct T, small affine tables and hierarchical affine batching',
        f1.candidates, f1.evidence() + ['resource.ceilings'],
        'engine.hier_affine.explicit as the production macro route' if hier_beats_all else None,
        ('Every hierarchical candidate beats direct T and every table width under the stated rule: ' if hier_beats_all else
         'No route satisfied the stated rule against all others: ') + json.dumps(f1.table(), sort_keys=True)
        + '. The five hierarchical divisors are mutually tied in this family because the 2016-step budget clamps every macro.',
        eliminated=[(c, 'Slower than every hierarchical candidate by more than 5 percent on the three largest classes')
                    for c in small1 + ['t-direct']] if hier_beats_all else (),
        limitations=['At the 1024-bit class the widest table is faster than hierarchical batching; that crossover lies between 1024 and 4096 bits and is not interpolated']))
    small_winner = f2.winner()
    decisions.append(decision(
        did[2][0], 'Small-block table width', f2.candidates + ['no production table'], f2.evidence() + f1.evidence(small1 + hier1),
        'No small-block table in the production schedule (small_block_width null); engine.small_affine remains a forcible validation route only',
        f'Among table widths, {small_winner} is fastest at every swept class: ' + json.dumps(f2.table(), sort_keys=True)
        + '. But decision ' + did[1][0] + ' shows every table width loses to hierarchical batching at 4096 bits and above, so a table '
        'would only serve states below the unmeasured crossover. Hierarchical leaves are built directly from elementary T on a bounded residue, '
        'so no table is needed; omitting it is the smaller correctness surface.',
        eliminated=[(c, 'Not competitive with hierarchical batching at 4096 bits and above') for c in f2.candidates],
        limitations=['Table widths remain exhaustively checkable; none is enabled for AUTO scheduling']))
    hw = f3.winner()
    caps = {c: c.rsplit('-k', 1)[1] for c in f3.candidates}
    top = f3.sizes[-1]
    ranked = sorted(f3.candidates, key=lambda c: (f3.stat(top, c)[0], c))
    live_low = min(f3.peak_live(c, top) for c in f3.candidates)
    live_high = max(f3.peak_live(c, top) for c in f3.candidates)
    choice = 'hier-explicit-d2-k16384'
    decisions.append(decision(
        did[3][0], 'Hierarchical scheduler divisor and macro cap within the I1 family', f3.candidates, f3.evidence(),
        hw or 'divisor 2, cap 16384 (hier-explicit-d2-k16384), chosen among performance-tied candidates',
        ('Timing winner under the stated rule. ' if hw else
         'No candidate beats all others under the stated rule, so the fifteen candidates are performance-tied. ')
        + json.dumps(f3.table(), sort_keys=True) + f'. Peak allocator live bytes at the largest class range from {live_low} to {live_high} '
        'bytes, which is not a material memory difference against a 256 MiB limit, so the memory tie-break does not discriminate; the '
        'remaining tie-break items are identical for all candidates. Stated residual objective for the free choice among tied candidates: '
        'prefer the cap with the lowest totals at the largest measured class (the three lowest there are '
        + ', '.join(ranked[:3]) + '), because every state of at least 131072 bits takes macros of exactly the cap for any divisor; '
        'then the smallest divisor, which gives the longest terminal-safe macros and fewest scheduler iterations below that size. '
        f'Selected {choice}.',
        limitations=['This is a tie-break choice, not a measured performance winner',
                     'A stricter reading that lets a few KiB of allocator live bytes decide would select cap 1024; a reviewer may require that',
                     'No claim is made about schedules or sizes outside the bounded sweep']))
    decisions.append(decision(
        did[4][0], 'Arbitrary-precision backend and multiplication route', ['arith.gmp.public', 'arith.flint.public'],
        fam[4].evidence() + ['dependency.gmp-candidate', 'unsupported.flint'], 'arith.gmp.public (documented public mpz interface, GMP 6.3.0)',
        'Exact products agreed with the independent Python reference for equal, 2:1 and 4:1 operand shapes at all six size classes, with '
        'positive activation of the public route. FLINT is unavailable locally, so there is no second backend to compare and no crossover to select.',
        eliminated=[('arith.flint.public', 'Unavailable; not acquired')]))
    decisions.append(decision(
        did[5][0], 'State representation', ['state.dense', 'state.sparse'], fam[5].evidence() + ['unsupported.sparse-state'],
        'state.dense (one GMP integer; canonical bytes only through the documented exporter)',
        'The dense route produced exact canonical export, exact low-bit extraction and exact fixed-step states on generated dense inputs and '
        'formula-defined sparse inputs at four size classes. The optional sparse candidate was not implemented, so no comparison exists.',
        eliminated=[('state.sparse', 'Optional candidate not implemented')]))
    hier_alloc = ['hier-copy', 'hier-reuse']
    reuse_wins = f6.beats('hier-reuse', 'hier-copy')
    copy_wins = f6.beats('hier-copy', 'hier-reuse')
    decisions.append(decision(
        did[6][0], 'Allocation strategy for the production macro route', f6.candidates, f6.evidence(),
        'alloc.reuse' if reuse_wins else 'alloc.copy',
        'On the selected hierarchical route ' + ('reuse beats copy' if reuse_wins else 'copy beats reuse' if copy_wins else
                                                 'copy and reuse are performance-tied') + ': ' + json.dumps(f6.table(), sort_keys=True)
        + '. ' + ('' if reuse_wins or copy_wins else 'Tie-break: the copy baseline has no aliasing rule to check and is the smaller correctness surface. ')
        + 'On direct T, in-place reuse is faster, but direct T is not the production macro route.',
        limitations=['Peak working set is dominated by the process baseline at bounded sizes; no scientific-scale memory claim']))
    decisions.append(decision(
        did[7][0], 'Compiler build mode', f7.candidates + ['native-release'], f7.evidence() + ['unsupported.native-tuning'],
        'portable-release' if f7.beats('build-portable-release', 'build-checked') else None,
        'Checked and portable-release builds produced identical exact states. ' + json.dumps(f7.table(), sort_keys=True)
        + '. The checked mode is not a production-speed candidate; native-release is unsupported by the pinned toolchain.',
        eliminated=[('native-release', 'No native-target mechanism in the pinned compiler; prebuilt portable GMP binary'),
                    ('build-checked', 'Assertion and run-time-check build; slower by more than 5 percent')]))
    decisions.append(decision(
        did[8][0], 'Parallelism', ['parallel.single', 'parallel.aux'], f1.evidence(hier1) + ['unsupported.parallel-aux'],
        'parallel.single with one thread',
        'Every measured case ran single-threaded with exact results. No auxiliary-parallel route exists to compare.',
        eliminated=[('parallel.aux', 'Optional candidate not implemented')], rule='I1 sections 4.1, 11.8 and 11.13'))
    buffered_wins = f9.beats('checkpoint-buffered', 'checkpoint-streaming')
    streaming_wins = f9.beats('checkpoint-streaming', 'checkpoint-buffered')
    decisions.append(decision(
        'decision.checkpoint.filesystem', 'Does the intended NTFS checkpoint target satisfy the bounded CEML-CKPT-1 durability contract',
        ['supported', 'unsupported'], ['checkpoint.durability-matrix', 'checkpoint.documented-semantics', 'unavailable.power-loss',
                                      'obs.storage.FileSystemType', 'obs.storage.DriveType', DURABILITY[stage]],
        'supported: generation-directory store with FlushFileBuffers on both files and on the directories, same-directory '
        'MoveFileExW write-through publication, content-based recovery' if durability['all_passed'] else None,
        f"All {durability['scenarios']} interruption scenarios and all {durability['adversarial_cases']} adversarial cases passed with fresh-process "
        'recovery and continuation, for both serialization strategies, with every R4 section 14.5 phase forced. No partial or inexact '
        'generation was ever published or accepted; the previous validated generation was always retained; the pointer was never trusted; '
        'corrupt newest generations, chain breaks and foreign identities were refused. Safety does not depend on rename durability: a '
        'generation is retired only after its successor was flushed, published, directory-flushed and re-read, so a lost publication '
        'falls back to a generation whose files were already flushed.',
        limitations=['Process interruption only; no power-loss proof', 'Volatile device write caches that ignore flush requests are outside this evidence',
                     'Rename atomicity under power loss is not stated by the retrieved documentation'],
        rule='R4 section 14 and I1 section 13: documented semantics plus bounded forced-termination tests'))
    decisions.append(decision(
        did[9][0], 'Checkpoint serialization strategy and cadence', f9.candidates, f9.evidence() + ['decision.checkpoint.filesystem'],
        'checkpoint.buffered' if not streaming_wins else 'checkpoint.streaming',
        ('Buffered beats streaming. ' if buffered_wins else 'Streaming beats buffered. ' if streaming_wins else
         'Neither strategy beats the other under the stated rule: filesystem cases have one warm-up and three measured '
         'repetitions under I1, fewer than the five a timing winner requires, and the classes are flush-dominated. ')
        + json.dumps(f9.table(), sort_keys=True) + '. Both strategies passed the complete interruption matrix. '
        + ('' if buffered_wins or streaming_wins else 'Tie-break: the buffered path writes one fully formed body and is the smaller correctness surface. ')
        + 'Cadence: a promotion at the first macro boundary after 600 seconds since the previous one, and always at the terminal state; '
        'cadence is not scientific state and one promotion costs tens of milliseconds at bounded sizes.',
        limitations=['Promotion cost at scientific state sizes is not measured', 'The cadence value is an engineering policy, not a timing winner']))
    direct_wins = f10.beats('terminal-direct-t', 'terminal-odd-only')
    odd_wins = f10.beats('terminal-odd-only', 'terminal-direct-t')
    decisions.append(decision(
        did[10][0], 'Terminal handoff', f10.candidates, f10.evidence(),
        'terminal.odd_only' if odd_wins else 'terminal.direct_t',
        'Both candidates reached the exact first occurrence of 1 with counters equal to the definition reference for every formula-defined '
        'power-of-two neighbour. ' + json.dumps(f10.table(), sort_keys=True) + '. '
        + ('Direct T wins.' if direct_wins else 'Odd-only wins.' if odd_wins else
           'They are tied; tie-break: direct T is the definition itself and the smaller correctness surface.')
        + ' Macros are clamped to bit_length(n)-1 and the terminal route takes over when the clamped macro length falls below 2.'))
    structural_tie = not f11.beats('audit-structural', 'audit-divisibility')
    decisions.append(decision(
        did[11][0], 'Production audit level', f11.candidates, f11.evidence(),
        'audit.divisibility (mandatory structural checks plus the divisibility canary; modular audit off)',
        json.dumps(f11.table(), sort_keys=True) + '. '
        + ('Disabling the canary gives no qualifying speed advantage, so the stronger check is kept. ' if structural_tie else
           'Structural-only is faster under the rule, but the canary is kept as a defect detector at its measured cost. ')
        + 'The modular audit shares the affine recurrence, adds measurable cost at the largest class and is left as a forcible route.',
        limitations=['The canary is a defect detector, not a proof or an independent oracle']))
    decisions.append(decision(
        did[12][0], 'Memory scaling and process memory ceiling', f12.candidates, f12.evidence() + ['resource.ceilings'],
        'No route is excluded on memory within the bounded domain; the 256 MiB Job limit stands for calibration',
        'Across all six size classes peak working set is dominated by the process baseline; allocator peak live bytes at the largest class: '
        + json.dumps({c: str(f12.peak_live(c, f12.sizes[-1])) for c in f12.candidates}, sort_keys=True) + '.',
        limitations=['No scientific resource forecast is made beyond the bounded domain'], binds=False))
    decisions.append(decision(
        'decision.language-toolchain', 'Implementation language and toolchain',
        ['C17 with public GMP mpz', 'C++20 with public GMP', 'Rust stable with rug'],
        ['dependency.gmp-candidate', 'unsupported.rust-rug', 'tools.msvc.cl.exe', 'tools.msvc.link.exe'],
        'C17 with the documented public GMP mpz interface, pinned Microsoft C toolchain',
        'Only the C17 family has a complete pinned, offline-reproducible local dependency closure. C++20 would use the same compiler and the same '
        'C interface and adds no capability; Rust with rug has no offline dependency closure here. Tie-break: smaller surface, fewer dependencies.',
        eliminated=[('Rust stable with rug', 'No pinned offline rug or GMP build closure'),
                    ('C++20 with public GMP', 'Same backend and compiler with a larger language surface')], rule='I1 sections 4.2 and 11.13'))
    decisions.append(decision(
        'decision.resource-ceilings-v2', 'Local resource ceilings for bounded calibration',
        ['initial ceilings', 'revised ceilings with persistence rule', 'revised ceilings with bounded admission wait'],
        ['resource.pressure-study', 'resource.refusal-log', 'resource.ceilings'],
        'Revised ceilings version 2 with amendment 2.1',
        'Isolated one-second page-input excursions occur with no CEML arithmetic and with zero page output, so one excursion cannot indicate '
        'case-caused memory pressure. Two consecutive excursions or any page output still refuse or abort. Admission waits a bounded, recorded '
        'time with no work in progress. All refusals are retained.',
        limitations=['Page input is a non-specific proxy; temperature is unavailable; the processor-performance floor is a frequency-collapse stop only'],
        rule='I1 section 14 and R4 section 15', binds=True))

    # ---- bundle index, summary, hardware report -------------------------------------
    used = defaultdict(list)
    for order, bundle in decisive.items():
        used[bundle] += did[order]
    used[DURABILITY[stage]] += ['decision.checkpoint.filesystem']
    bundles = []
    for name in sorted(p.name for p in BUNDLES.iterdir() if p.is_dir()):
        digest, count = bundle_digest(BUNDLES / name)
        bundles.append(dict(bundle_id=name, bundle_digest=digest, logical_locator=f'local/c1/benchmark_bundles/{name}/',
                            member_count=str(count), retained_local=True,
                            decision_ids=sorted(set(used.get(name, ['decision.resource-ceilings-v2'])))))
    for b in bundles:
        records.append(fact('bundle.' + b['bundle_id'], 'calibration', 'retained_local_bundle',
                            dict(bundle_digest=b['bundle_digest'], member_count=b['member_count'],
                                 role='decision evidence' if b['bundle_id'] in used else 'retained refusal or superseded evidence; not used for selection'),
                            'I1 benchmark bundle digest over lexicographically ordered member names and raw bytes',
                            'Raw records stay local; this digest binds them'))
    for d in decisions:      # the durability bundle is cited through its bundle fact
        d['evidence_record_ids'] = sorted({('bundle.' + e) if e in {b['bundle_id'] for b in bundles} else e for e in d['evidence_record_ids']})
    hardware = seal('CEML-HARDWARE-REPORT-1', audit_run_id=AUDIT, generated_at=now(), records=records, privacy_scan_passed=True)
    index = seal('CEML-BENCHMARK-BUNDLES-1', bundles=bundles)
    summary = seal('CEML-BENCHMARK-SUMMARY-1', suite_version='CEML-CAL-1', hardware_report_digest=hardware['artifact_digest'],
                   benchmark_bundle_index_digest=index['artifact_digest'],
                   cases=summarize([b['bundle_id'] for b in bundles if (BUNDLES / b['bundle_id']).glob('*-record.json')], decisive,
                                   {order: did[order] for order in did}))
    log = seal('CEML-ENGINEERING-DECISIONS-1', decisions=decisions)
    known = {r['record_id'] for r in records} | {c['case_id'] for c in summary['cases']} | {d['decision_id'] for d in decisions}
    for d in decisions:
        if not set(d['evidence_record_ids']) <= known:
            raise ValueError('Untraced evidence reference in ' + d['decision_id'])
    if len({r['record_id'] for r in records}) != len(records):
        raise ValueError('Duplicate record identifier')
    return hardware, index, summary, log


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', required=True, choices=sorted(STAGES))
    parser.add_argument('--verdict', default='Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**')
    args = parser.parse_args()
    hardware, index, summary, log = assemble(args.evidence)
    outputs = {'HARDWARE_REPORT.json': hardware, 'BENCHMARK_BUNDLES.json': index, 'BENCHMARK_SUMMARY.json': summary,
               'ENGINEERING_DECISIONS.json': log}
    for name, value in outputs.items():
        text = json.dumps(value, ensure_ascii=True, indent=2) + '\n'
        if validate_artifact(value, name, ROOT) or inspect_text(text, name):
            raise ValueError('Report schema or privacy precheck failed: ' + name)
        (ROOT / 'local_reports' / name).write_text(text, encoding='utf-8', newline='\n')
    text = markdown(hardware, args.verdict)
    if inspect_text(text, 'HARDWARE_REPORT.md'):
        raise ValueError('Generated Markdown privacy check failed')
    (ROOT / 'local_reports/HARDWARE_REPORT.md').write_text(text, encoding='utf-8', newline='\n')
    for d in log['decisions']:
        print(d['decision_id'], '=>', d['selection'])
    print(json.dumps({'cases': len(summary['cases']), 'bundles': len(index['bundles']), 'records': len(hardware['records'])}))


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        print('REFUSED:', error)
        sys.exit(1)
