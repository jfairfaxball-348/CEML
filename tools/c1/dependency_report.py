"""Stage: hardware characterization; reconcile authorized GMP setup and refusal.

This session-specific report cannot select a production stack or create a profile.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from engineering_codec import artifact_digest, blob, canonical_bytes, self_test_vector
from gmp_setup import ROOT, LOCAL
from initial_refusal_report import decision, markdown, missing, seal
from privacy_gate import inspect_text, validate_artifact

AUDIT = 'c1-20261005-post-setup'
BUNDLE_ID = 'c1-20261005-route-subset'
BUNDLE = ROOT / 'local/c1/benchmark_bundles' / BUNDLE_ID


def observed(identity, category, name, value, method, uncertainty, timestamp=None):
    return dict(record_class='OBSERVED_FACT', record_id=identity, category=category,
                fact_name=name, value=value, source_adapter='c1-authorized-dependency-session',
                source_method=method, audit_run_id=AUDIT,
                source_state_kind='momentary_state' if category == 'resource_safety' else 'active_configuration',
                uncertainty=uncertainty, sanitization=['Selected dependency and engineering fields only; locators and raw diagnostics excluded'],
                observed_at=timestamp)


def main():
    status = (ROOT / 'PROGRAM_STATUS.md').read_text(encoding='utf-8')
    if '**Authoritative current phase:** C1' not in status or '**Scientific execution authorization:** DENIED' not in status:
        raise ValueError('C1 authorization absent')
    if (ROOT/'config/local_machine_profile.json').exists() or (ROOT/'local_reports/BUILD_MANIFEST.json').exists():
        raise ValueError('Incomplete-session assembler cannot overwrite a completed build event')
    records = []
    for name in ('audit_observations.json', 'tool_observations.json'):
        records.extend(json.loads((ROOT / 'local/c1' / AUDIT / name).read_text(encoding='utf-8')))
    before = json.loads((ROOT/'local/c1/c1-20261005-pre-setup/audit_observations.json').read_text(encoding='utf-8'))
    admitted = {r['record_id']:r['value'] for r in before if r['record_class']=='OBSERVED_FACT' and
                ('memory.performance.' in r['record_id'] or 'power.' in r['record_id'])}
    records.append(observed('dependency.pre-setup', 'resource_safety', 'before_setup_resource_snapshot', admitted,
                            'Narrow Windows collector before acquisition and compilation',
                            'Transient conditions; initial calibration ceilings remain in force'))
    records.append(observed('dependency.authorization', 'authorization', 'dependency_setup_authorized', True,
                            'Explicit operator message on 2026-10-05 authorizing installation, builds and required setup',
                            'Authorization persists; it does not authorize scientific work or production selection'))
    files = ('acquisition', 'source_provenance', 'probe_build', 'probe_smoke', 'offline_build', 'offline_smoke', 'calibration_build')
    setup = {name:json.loads((LOCAL/(name+'.json')).read_text()) for name in files}
    for name, value in setup.items():
        records.append(observed('dependency.'+name.replace('_','-'), 'toolchain', name, value,
                                'Explicit acquisition, safe archive inspection, public C compile/link and fixed arithmetic capability probe',
                                'Engineering candidate evidence only; offline production toolchain closure and stack selection remain open',
                                value['observed_at']))
    if setup['probe_build']['executable'] != setup['offline_build']['executable']:
        raise ValueError('Offline executable reproduction failed')
    if not setup['offline_smoke']['result']['ok']:
        raise ValueError('Offline smoke did not pass')
    records.append(observed('engineering.generator-vector', 'engineering_integrity', 'normative_generator_vector', self_test_vector(),
                            'Fixed normative CEML-CAL-1 vector self-test before the subset',
                            'The vector self-test performs no trajectory'))
    raw = [json.loads(p.read_text()) for p in sorted(BUNDLE.glob('*-record.json'))]
    if len(raw) != 1 or raw[0]['abort_code'] != 'C1_RESOURCE_ABORT' or not raw[0]['warmup'] or raw[0]['valid']:
        raise ValueError('This session report expects the retained first-warmup resource refusal')
    sample = raw[0]
    detail = json.loads((BUNDLE/'1024-affine-small-public-0-0-detail.json').read_text())
    if detail['guard']['reason'] != 'paging-pressure':
        raise ValueError('Expected resource evidence absent')
    for r in raw:
        if validate_artifact(r, 'calibration_record.json', ROOT) or artifact_digest(r) != r['artifact_digest']:
            raise ValueError('Raw calibration record integrity failed')
    records.append(observed('calibration.first-attempt', 'resource_safety', 'guarded_initial_warmup_outcome',
                            {'record_id':sample['record_id'], 'abort_code':sample['abort_code'],
                             'preflight_samples':'2', 'preflight_pages_input_rounded':'0',
                             'final_pages_input_rounded':detail['guard']['final_pages_input_rounded'],
                             'final_pages_output_rounded':detail['guard']['final_pages_output_rounded'],
                             'rate_units':'pages_per_second', 'available_bytes':detail['guard']['available_bytes'],
                             'free_storage_bytes':detail['guard']['free_storage_bytes'],
                             'child_wall_time_ns':str(int(detail['guard']['process_wall_ticks'])*1000000000//int(detail['guard']['qpc_frequency'])),
                             'candidate_reference_agreement':sample['correctness_agreement'],
                             'requested_affine_blocks':detail['candidate']['activated_count'], 'fallback_count':'0',
                             'shortcut_steps':detail['candidate']['shortcut_steps'], 'odd_steps':detail['candidate']['odd_steps'],
                             'standard_steps':detail['candidate']['standard_steps'], 'accepted_for_performance':False},
                            'Native Job-guarded 1024-bit public engineering warmup; PDH preflight and post-child observation',
                            'Paging includes mapped-file reads. Short rate interval can amplify bursts. No claim of actual pagefile pressure. Invalid raw CPU/RSS zeros are suppressed placeholders, not measurements. No accepted timing or V1 evidence'))
    records.append(missing('c1.checkpoint-unestablished', 'checkpoint_storage', 'CEML-CKPT-1 filesystem durability and recovery acceptance',
                           'Ordered calibration stopped at its first resource refusal; no synthetic filesystem interruption matrix executed',
                           ['No checkpoint strategy, production engine, final build or machine profile selected']))
    records.append(missing('c1.production-unselected', 'implementation', 'Production architecture and complete final offline build/profile',
                           'Dependency capability is established but valid decision-relevant calibration and checkpoint acceptance are absent',
                           ['Remain at C1 hardware characterization; V1 and scientific execution remain denied']))
    choices = [decision('decision.dependency-candidate', 'Locally usable GMP public-C candidate for bounded calibration',
                        ['Pinned UCRT64 GMP DLL with installed MSVC','Larger alternative toolchain acquisition'],
                        ['dependency.authorization','dependency.acquisition','dependency.probe-build','dependency.offline-build','dependency.offline-smoke'],
                        'Observed public-C compatibility and exact smoke agreement, pinned inputs and byte-identical offline smoke rebuild establish candidate availability only.',
                        'Retain the pinned public-C candidate for bounded calibration; no production stack selection'),
               decision('decision.resource-refusal', 'Accept or refuse the first guarded route warmup',
                        ['Accept as timing evidence','Retain invalid and stop ordered subset'],
                        ['calibration.first-attempt',sample['record_id']],
                        'The observed page-input rate exceeded the existing 100 pages per second ceiling. Correct arithmetic and positive activation cannot override the resource refusal.',
                        'Retain C1_RESOURCE_ABORT; accept no timing; stop the ordered subset')]
    families = ['route-crossover','small-block-sweep','hierarchical-sweep','backend-multiplication','representation','allocation',
                'compiler-build','parallelism','checkpoint','terminal-handoff','audit-cost','memory-scaling']
    for order, family in enumerate(families, 1):
        rid = f'c1.matrix.{order:02d}.{family}'
        reason = 'Not reached after the first resource refusal; required evidence remains unavailable'
        if order == 1:
            reason = 'First 1024-bit affine warmup invalidated by resource check; no measured repetitions. Two admitted size classes are insufficient for the I1 three-class timing rule.'
        records.append(missing(rid, 'calibration', 'CEML-CAL-1 '+family, reason, ['No justified production selection or winner']))
        choices.append(decision(f'decision.matrix.{order:02d}.{family}', 'CEML-CAL-1 '+family+' selection',
                                ['Eligible public-API I1 candidates within locally safe bounds'], [rid,'calibration.first-attempt'],
                                reason+'; missing measurements are not a tie'))
    generated = datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
    hardware = seal('CEML-HARDWARE-REPORT-1', audit_run_id=AUDIT, generated_at=generated, records=records, privacy_scan_passed=True)
    members = sorted(p for p in BUNDLE.iterdir() if p.is_file())
    digest = hashlib.sha3_256(b'CEML-I1-BENCHMARK-BUNDLE-V1\0')
    for p in members:
        data = p.read_bytes()
        if inspect_text(data.decode('ascii'), p.name):
            raise ValueError('Bundle privacy gate failed')
        digest.update(blob(p.name.encode('ascii')))
        digest.update(blob(data))
    bundle_index = seal('CEML-BENCHMARK-BUNDLES-1', bundles=[dict(bundle_id=BUNDLE_ID, bundle_digest=digest.hexdigest(),
                        logical_locator='local/c1/benchmark_bundles/'+BUNDLE_ID+'/', member_count=str(len(members)), retained_local=True,
                        decision_ids=['decision.resource-refusal','decision.matrix.01.route-crossover'])])
    summary = seal('CEML-BENCHMARK-SUMMARY-1', suite_version='CEML-CAL-1', hardware_report_digest=hardware['artifact_digest'],
                   benchmark_bundle_index_digest=bundle_index['artifact_digest'], cases=[dict(case_id=sample['case_id'], candidate_id=sample['candidate_id'],
                   valid_repeats='0', invalid_repeats='1', median_wall_time_ns=None, minimum_wall_time_ns=None,
                   maximum_wall_time_ns=None, mad_wall_time_ns=None, peak_rss_bytes=None,
                   correctness_all=False, route_activation_proved=False, decision_ids=['decision.resource-refusal','decision.matrix.01.route-crossover'])])
    decision_log = seal('CEML-ENGINEERING-DECISIONS-1', decisions=choices)
    ids = {r['record_id'] for r in records+raw}
    if len(ids) != len(records)+len(raw) or any(not set(d['evidence_record_ids']) <= ids for d in choices):
        raise ValueError('Evidence reference failure')
    outputs = {'HARDWARE_REPORT.json':hardware, 'BENCHMARK_SUMMARY.json':summary,
               'BENCHMARK_BUNDLES.json':bundle_index,'ENGINEERING_DECISIONS.json':decision_log}
    for name, value in outputs.items():
        text = json.dumps(value, ensure_ascii=True, indent=2)+'\n'
        if validate_artifact(value, name, ROOT) or inspect_text(text, name):
            raise ValueError('Report schema or privacy precheck failed: '+name)
        (ROOT / 'local_reports' / name).write_text(text, encoding='utf-8', newline='\n')
    md = markdown(hardware)
    if inspect_text(md, 'HARDWARE_REPORT.md'):
        raise ValueError('Generated Markdown privacy gate failed')
    (ROOT/'local_reports/HARDWARE_REPORT.md').write_text(md, encoding='utf-8', newline='\n')
    print('Dependency/refusal reports assembled: four schema-valid artifacts; one invalid warmup; zero measured repeats; C1 open.')


if __name__ == '__main__':
    main()
