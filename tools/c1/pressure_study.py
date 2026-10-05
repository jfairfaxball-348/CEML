"""Stage: hardware characterization; one bounded monitor-method observation.

Builds and runs the arithmetic-free paging-proxy study once per study ID. It
is an observation of the resource monitor, not calibration: no CEML-CAL-1 case
runs and nothing is charged or released in the arithmetic budget. An existing
study is never overwritten or repeated under the same ID.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys

from gmp_setup import FLAGS, LOCAL, ROOT, Refusal, build, hashes, invoke, msvc_environment, now, require_authorization

STUDIES = ROOT / 'local/c1/pressure-study'


def run(study_id):
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', study_id):
        raise Refusal('Study ID must contain only lowercase letters, digits and hyphens')
    target = STUDIES / (study_id + '.json')
    if target.exists():
        raise Refusal('Existing study retained; no overwrite or repeat under one ID')
    build(True)
    env, bindir, toolchain = msvc_environment()
    folder = LOCAL / 'calibration'
    if not (folder / 'cal_candidate.exe').is_file():
        raise Refusal('Arithmetic-free launch target unavailable')
    source = (ROOT / 'tools/c1/pressure_study.c').read_bytes()
    (folder / 'pressure_study.c').write_bytes(source)
    invoke([str(bindir / 'cl.exe'), *FLAGS, 'pressure_study.c', 'pdh.lib', '-Fe:pressure_study.exe',
            '-Fo:pressure_study.obj', '-link', '-Brepro'], env, folder)
    executable = (folder / 'pressure_study.exe').read_bytes()
    raw = invoke([str(folder / 'pressure_study.exe')], cwd=folder, timeout=90)
    lines = [json.loads(line) for line in raw.splitlines() if line]
    samples = [x for x in lines if x['kind'] == 'sample']
    summary = {}
    for phase in ('idle', 'arithmetic-free-launch', 'idle-after'):
        values = sorted(int(x['pages_input_milli']) for x in samples if x['phase'] == phase)
        outputs = [int(x['pages_output_milli']) for x in samples if x['phase'] == phase]
        summary[phase] = dict(count=str(len(values)), minimum_pages_input_milli=str(values[0]),
                              median_pages_input_milli=str(int(statistics.median_low(values))),
                              maximum_pages_input_milli=str(values[-1]),
                              intervals_above_100_pages=str(sum(v > 100000 for v in values)),
                              maximum_pages_output_milli=str(max(outputs)))
    result = dict(stage='hardware characterization', purpose='monitor-method observation; not calibration',
                  study_id=study_id, observed_at=now(), source=hashes(source), executable=hashes(executable),
                  launch_target=hashes((folder / 'cal_candidate.exe').read_bytes()),
                  toolchain=dict(msvc_tools_version=toolchain['msvc_tools_version'],
                                 windows_sdk_version=toolchain['windows_sdk_version']),
                  header=[x for x in lines if x['kind'] == 'study'][0], samples=samples, summary=summary)
    STUDIES.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=1) + '\n', encoding='ascii')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-id', required=True)
    args = parser.parse_args()
    require_authorization()
    result = run(args.study_id)
    print(json.dumps({'status': 'ok', 'summary': result['summary'], 'header': result['header']}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'status': 'refused', 'reason': str(error) if isinstance(error, Refusal) else 'Study refused; raw diagnostic suppressed'}))
        sys.exit(1)
