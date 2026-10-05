"""Stage: hardware characterization; assemble the initial incomplete C1 audit.

This session-specific assembler cannot create a build/profile or accept a
benchmark. Collectors must run first. All emitted JSON uses frozen I1 envelopes.
"""
from __future__ import annotations

from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path

from engineering_codec import artifact_digest, canonical_bytes, self_test_vector
from privacy_gate import inspect_text, validate_artifact

ROOT = Path(__file__).resolve().parents[2]
AUDIT = 'c1-20261004-a'
BASELINE = 'e2148e47f4cc71ba33bfc5c05140d2adef32f479'


def fact(identity, category, name, value, method, uncertainty, observed_at=None):
    return dict(record_class='OBSERVED_FACT', record_id=identity, category=category,
                fact_name=name, value=value, source_adapter='c1-initial-session',
                source_method=method, audit_run_id=AUDIT,
                source_state_kind='active_configuration', uncertainty=uncertainty,
                sanitization=['Only explicitly permitted fields retained; paths and identifiers excluded'],
                observed_at=observed_at)


def missing(identity, category, item, reason, effects):
    return dict(record_class='UNAVAILABLE_OR_UNSUPPORTED', record_id=identity,
                category=category, requested_item=item, attempted_method=None,
                reason=reason, downstream_effects=effects)


def decision(identity, question, candidates, evidence, rationale, selection=None, eliminated=None):
    return dict(record_class='ENGINEERING_DECISION', decision_id=identity,
                question=question, candidates_considered=candidates,
                evidence_record_ids=evidence, eliminated=eliminated or [],
                selection=selection, decision_rule='I1 sections 1, 4, 11.13, 14 and 18; no unsupported selection',
                rationale=rationale,
                limitations=['Initial hardware characterization only; no production profile binding',
                             'C1 remains open; no V1 or scientific execution'], binds_profile=False)


def seal(version, **members):
    obj = dict(experiment='CEML', schema_version=version, **members)
    obj['artifact_digest'] = artifact_digest(obj)
    return obj


def markdown(report):
    lines = ['# C1 sanitized hardware report', '',
             'Stage: **hardware characterization**. **CEML-C1 REMAINS OPEN.**', '',
             f"Audit: `{report['audit_run_id']}`. Generated: {report['generated_at']}.", '',
             f"JSON artifact digest: `{report['artifact_digest']}`.", '',
             'Generated mechanically from HARDWARE_REPORT.json. Observations are not benchmarks.',
             'No production build/profile or checkpoint durability acceptance is implied.', '']
    for r in report['records']:
        lines += [f"## {r['record_id']}", '', f"Class: `{r['record_class']}`.", '']
        if r['record_class'] == 'OBSERVED_FACT':
            value = canonical_bytes(r['value']).decode('ascii')
            lines += [f"{r['fact_name']}: `{value}`", '', f"Source: {r['source_method']}.", '',
                      f"Observation kind: {r['source_state_kind']}. Time: {r['observed_at'] or 'initial audit session; exact timestamp not retained'}.", '',
                      f"Uncertainty: {r['uncertainty'] or 'No additional uncertainty recorded.'}", '']
        else:
            lines += [f"Requested: {r['requested_item']}.", '', f"Reason: {r['reason']}", '',
                      'Effects: ' + '; '.join(r['downstream_effects']) + '.', '']
    return '\n'.join(lines)


def main():
    status = (ROOT / 'PROGRAM_STATUS.md').read_text(encoding='utf-8')
    if '**Authoritative current phase:** C1' not in status or '**Scientific execution authorization:** DENIED' not in status:
        raise ValueError('C1 authorization missing')
    if (ROOT / 'local_reports/BUILD_MANIFEST.json').exists() or (ROOT / 'config/local_machine_profile.json').exists():
        raise ValueError('Initial refusal assembler cannot replace a later build/profile event')
    records = []
    for name in ('audit_observations.json', 'tool_observations.json'):
        records += json.loads((ROOT / 'local/c1' / name).read_text(encoding='utf-8'))
    if not any(r['record_id'] == 'tools.gmp-unavailable' for r in records):
        raise ValueError('This initial refusal is no longer supported; reassess C1')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    initial = fact('initial.resource-observation', 'resource_safety', 'initial_selected_resource_fields',
                   {'installed_memory_bytes':'17179869184', 'os_visible_memory_bytes':'16866881536',
                    'free_physical_memory_bytes':'5730615296', 'free_target_storage_bytes':'208232972288',
                    'later_available_bytes':'5612523520', 'pages_input_per_second':'1566',
                    'pages_output_per_second':'0', 'page_reads_per_second':'948',
                    'ac_connected':True, 'standby_ac_seconds':'0', 'standby_dc_seconds':'0',
                    'hibernate_ac_seconds':'0', 'hibernate_dc_seconds':'0'},
                   'Initial field-selective CIM, target-volume, kernel32 power/installed-memory APIs and filtered powercfg indices before dependency discovery',
                   'Two successive initial snapshots, distinct from later collector samples; exact timestamps not retained; paging includes mapped-file activity')
    initial['source_state_kind'] = 'momentary_state'
    records.append(initial)
    records.append(fact('initial.authorization', 'authorization', 'verified_local_main_baseline', BASELINE,
                        'git status, git log main and merge-base ancestry; controlling-document read',
                        'Local main and local remote-tracking state inspected; no network fetch performed'))
    records.append(fact('tools.jsonschema', 'toolchain', 'jsonschema_version', importlib.metadata.version('jsonschema'),
                        'Existing Python importlib.metadata version query', 'Audit schema checker only; no dependency installation', now))
    records.append(fact('engineering.generator-vector', 'engineering_integrity', 'normative_generator_vector', self_test_vector(),
                        'Fixed-vector engineering_codec.self_test_vector against frozen CEML-CAL-1',
                        'No trajectory step, timing case, route comparison or V1 class executed', now))
    records.append(missing('c1.monitor-unavailable', 'resource_safety', 'Enforced non-trivial calibration admission and mid-case monitoring',
                           'Ceilings recorded, but benchmark supervisor not implemented and first pressure sample fails selected threshold',
                           ['No non-trivial calibration or filesystem interruption test admitted']))
    records.append(missing('c1.checkpoint-unestablished', 'checkpoint_storage', 'CEML-CKPT-1 durability and recovery acceptance',
                           'Stopped at earlier dependency and monitoring prerequisites; no synthetic durability or interruption case executed',
                           ['Scientific checkpoint storage unsupported pending evidence; no conclusion that the filesystem is inherently incapable']))
    rows = [
        ('route-crossover', ['direct T','small affine','hierarchical affine']),
        ('small-block-sweep', ['width 4','width 8','width 12','width 16']),
        ('hierarchical-sweep', ['I1 divisor and k-cap grid']),
        ('backend-multiplication', ['public GMP','optional public FLINT']),
        ('representation', ['public-library dense','optional sparse']),
        ('allocation', ['copy','public-API reuse']),
        ('compiler-build', ['checked','portable-release','native-release']),
        ('parallelism', ['single thread','optional auxiliary threads']),
        ('checkpoint', ['buffered','streaming']),
        ('terminal-handoff', ['direct T','odd-only']),
        ('audit-cost', ['structural','divisibility','divisibility plus modular']),
        ('memory-scaling', ['I1 six bounded size classes']),
    ]
    decisions = [decision('decision.initial-safety', 'Initial admission limits before non-trivial calibration',
                          ['Conservative restricted subset','No non-trivial work'],
                          ['initial.resource-observation','c1.monitor-unavailable','unavailable.thermal.temperature'],
                          'Reserve 4 GiB memory and 16 GiB storage, cap child memory at 256 MiB and scratch at 64 MiB; one arithmetic process/thread; 5-second cases and 60-second aggregate; full detail in docs/C1_RESOURCE_CEILINGS.md. Initial paging sample fails the policy, and monitors are absent.',
                          'Record initial ceilings; refuse non-trivial work until all admission and monitoring conditions hold'),
                 decision('decision.production-stack', 'Eligible locally supported offline production stack',
                          ['C17 and public GMP','C++20 and public GMP','Rust stable and rug/GMP'],
                          ['tools.path','tools.rug-cache','tools.gmp-locators','tools.gmp-unavailable'],
                          'No usable GMP package established in checked scope; candidate compiler presence alone cannot select a production stack. No components acquired.',
                          eliminated=[{'candidate':'Python bigint production core','reason':'I1 section 4.3 restricts Python to reference/orchestration'}])]
    for order, (family, candidates) in enumerate(rows, 1):
        rid = f'c1.matrix.{order:02d}.{family}'
        did = f'decision.matrix.{order:02d}.{family}'
        reason = 'Required candidate harness, eligible dependency/build provenance and enforced safety monitors are not established; zero cases executed'
        if family == 'checkpoint':
            reason = 'Prior calibration prerequisites unmet; exact codec/store, documented durability semantics and interruption/recovery tests have not been established'
        records.append(missing(rid, 'calibration', 'CEML-CAL-1 '+family, reason,
                               ['No route activation or performance winner; '+did+' refuses selection']))
        decisions.append(decision(did, 'CEML-CAL-1 '+family+' selection', candidates,
                                  [rid,'tools.gmp-unavailable','c1.monitor-unavailable'] + (['c1.checkpoint-unestablished'] if family == 'checkpoint' else []),
                                  reason+'; no timing tie-break can substitute for absent evidence'))
    ids = [r['record_id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate observation IDs')
    for d in decisions:
        if not set(d['evidence_record_ids']) <= set(ids):
            raise ValueError('Dangling decision evidence')
    report = seal('CEML-HARDWARE-REPORT-1', audit_run_id=AUDIT, generated_at=now,
                  records=records, privacy_scan_passed=True)
    bundles = seal('CEML-BENCHMARK-BUNDLES-1', bundles=[])
    summary = seal('CEML-BENCHMARK-SUMMARY-1', suite_version='CEML-CAL-1',
                   hardware_report_digest=report['artifact_digest'],
                   benchmark_bundle_index_digest=bundles['artifact_digest'], cases=[])
    log = seal('CEML-ENGINEERING-DECISIONS-1', decisions=decisions)
    artifacts = {'HARDWARE_REPORT.json':report, 'BENCHMARK_BUNDLES.json':bundles,
                 'BENCHMARK_SUMMARY.json':summary, 'ENGINEERING_DECISIONS.json':log}
    payloads = {}
    for name, obj in artifacts.items():
        logical = 'local_reports/'+name
        text = json.dumps(obj, ensure_ascii=True, indent=2)+'\n'
        if validate_artifact(obj, logical, ROOT) or inspect_text(text, logical):
            raise ValueError('Artifact schema or privacy gate refused '+name)
        if artifact_digest(obj) != obj['artifact_digest']:
            raise ValueError('Digest reproduction failed')
        payloads[logical] = text
    md = markdown(report)
    if inspect_text(md, 'local_reports/HARDWARE_REPORT.md'):
        raise ValueError('Generated Markdown privacy gate refused')
    payloads['local_reports/HARDWARE_REPORT.md'] = md
    for logical, text in payloads.items():
        (ROOT / logical).write_text(text, encoding='utf-8', newline='\n')
    print('Initial C1 refusal package: schemas, privacy precheck and four artifact digests PASS; zero benchmarks; no build/profile.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError) as exc:
        # Controlled failure messages contain no captured local values.
        print('Initial report assembly REFUSED: '+type(exc).__name__)
        raise SystemExit(1)
