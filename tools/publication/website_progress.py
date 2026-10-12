"""Derive the public website progress file from the published RUN1 aggregate record.

Usage (repository root, standard library only, no network):
    python tools/publication/website_progress.py           # rewrite the JSON file
    python tools/publication/website_progress.py --check   # fail if the JSON file is stale

`docs/RUN1_PROGRESS.md` stays the authoritative aggregate record. This tool only
re-expresses its verified, already published tables and claim block as
`frontier_progress_for_website.json`, which the public website fetches. It reads
no batch directory, checkpoint, receipt or local file, and executes nothing.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'docs/RUN1_PROGRESS.md'
OUTPUT = ROOT / 'frontier_progress_for_website.json'
RECORD_URL = 'https://github.com/jfairfaxball-348/CEML/blob/main/docs/RUN1_PROGRESS.md'
REPOSITORY_URL = 'https://github.com/jfairfaxball-348/CEML'

ROW = re.compile(r'^\| (\d+) \| `\[(\d+),(\d+)\)` \| (\d+) \|(?: [^|]+ \|)? `([0-9a-f]{64})` \|$')
RULES = ('E2', 'Q4', 'P3', 'M9', 'S2K4-03', 'EXPLICIT')


class PublicationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise PublicationError(message)


def field(text, pattern, label):
    values = re.findall(pattern, text, flags=re.MULTILINE)
    require(len(values) == 1, f'{label} missing or ambiguous in {SOURCE.name}')
    return values[0]


def build(text):
    batches = []
    for line in text.splitlines():
        match = ROW.match(line)
        if match:
            number, start, end, width, digest = match.groups()
            batches.append(dict(number=int(number), start=start, end=end,
                                width=int(width), certificate_digest=digest))

    require(batches, 'No batch rows found')
    for index, batch in enumerate(batches):
        require(batch['number'] == index + 1, 'Batch numbers are not consecutive from 1')
        require(int(batch['end']) - int(batch['start']) == batch['width'], f'Batch {index + 1} width mismatch')
        if index:
            require(batch['start'] == batches[index - 1]['end'], f'Batch {index + 1} is not contiguous')

    base = field(text, r'^Assumed, not verified by CEML: every positive integer below B = (\d+) converges$', 'Base')
    start, end = field(text, r'^Verified conditional on that assumption: every integer in \[(\d+),(\d+)\) converges$',
                       'Verified interval')
    count, total = field(text, r'^Batches: (\d+) \((\d+) integers\)$', 'Batch count')
    latest = field(text, r'^Latest certificate digest: ([0-9a-f]{64})$', 'Latest digest')
    genesis = field(text, r'^Genesis digest: ([0-9a-f]{64})$', 'Genesis digest')
    unresolved = field(text, r'^Unresolved: (\d+)$', 'Unresolved count')
    rule_values = field(text, r'^Rule counts \(E2, Q4, P3, M9, S2K4-03, EXPLICIT\): ([\d, ]+)$', 'Rule counts')
    run_id = field(text, r'^Run identifier: (\S+)$', 'Run identifier')
    source_url, generated = field(text, r"^  Source and its date: author's project homepage (\S+), generated (\S+)$",
                                  'Base source')
    observed = field(text, r'^  CEML observation time \(UTC\): (\S+)$', 'Observation time')
    run_date = field(text, r'^Run dates \(UTC\): (\d{4}-\d{2}-\d{2})', 'Run date')

    rule_counts = dict(zip(RULES, (int(value) for value in rule_values.split(','))))
    require(len(rule_counts) == len(RULES), 'Rule count arity mismatch')
    require(start == base == batches[0]['start'], 'Coverage does not begin at the base')
    require(end == batches[-1]['end'] and int(count) == len(batches), 'Coverage does not match batch tables')
    require(int(total) == int(end) - int(start) == sum(rule_counts.values()), 'Integer totals disagree')
    require(latest == batches[-1]['certificate_digest'], 'Latest digest does not match final batch')
    require(int(unresolved) == 0, 'A published record with unresolved starts cannot be shown as verified')

    return {
        'schema_version': 1,
        'title': 'Collatz frontier verification',
        'protocol': 'CEML-FRONTIER-2',
        'run_id': run_id,
        'updated': run_date,
        'repository_url': REPOSITORY_URL,
        'record_url': RECORD_URL,
        'base': {
            'value': base,
            'kind': 'operational',
            'description': 'Author-reported operational bound of the distributed Collatz verification project; '
                           'assumed by CEML, not replicated.',
            'source_url': source_url,
            'source_generated_at': generated,
            'observed_at': observed,
        },
        'peer_reviewed_bound': {
            'value': '2361183241434822606848',
            'label': '2^71',
            'citation': 'Bařina (2025)',
        },
        'coverage': {'start': start, 'end': end, 'integers': total},
        'unresolved': int(unresolved),
        'genesis_digest': genesis,
        'latest_certificate_digest': latest,
        'rule_counts': rule_counts,
        'batches': batches,
        'claim': 'Every integer in the covered interval reaches 1, conditional on the author-reported base. '
                 'This is a finite, conditional computational result: not a proof of the Collatz conjecture, '
                 'not a reproduction of the base, and not a claim of a world first or of global frontier extension.',
    }


def render(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--check', action='store_true', help='fail if the website file is missing or stale')
    args = parser.parse_args()
    try:
        expected = render(build(SOURCE.read_text(encoding='utf-8')))
    except PublicationError as error:
        print(f'website_progress: REFUSED: {error}', file=sys.stderr)
        return 2
    if args.check:
        current = OUTPUT.read_text(encoding='utf-8') if OUTPUT.exists() else None
        if current != expected:
            print(f'website_progress: STALE: regenerate {OUTPUT.name}', file=sys.stderr)
            return 1
        print('website_progress: PASS')
        return 0
    OUTPUT.write_text(expected, encoding='utf-8', newline='\n')
    print(f'website_progress: wrote {OUTPUT.name}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
