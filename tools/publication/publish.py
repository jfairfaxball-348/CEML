"""Owner-invoked verify-and-publish command; executes no scientific batch."""
import argparse
from contextlib import contextmanager
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

from github_transport import ROOT, REPO, PublicationError, api, authenticate, commit_files, run
import website_progress

spec = importlib.util.spec_from_file_location('frontier_operator', ROOT / 'tools/operator/run_frontier.py')
operator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator)
sys.path.insert(0, str(ROOT))
from tools.session_i2.pinned import IntegrityError
KEYS = ('e2_count', 'q4_count', 'p3_count', 'm9_count', 's2_count', 'explicit_count')
FILES = ('docs/RUN1_PROGRESS.md', 'frontier_progress_for_website.json', 'PROGRAM_STATUS.md', 'START_HERE.md')


def require(condition, message):
    if not condition:
        raise PublicationError(message)


def git(*args):
    return run(['git', *args])


def stamp(path):
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


@contextmanager
def publication_leases(force=False):
    """Keep extended scientific record bytes pinned through derivation and merge."""
    chain = ROOT / operator.CHAIN
    if not force and len(list(chain.glob('*/certificate.json'))) <= 256:
        yield
        return
    sys.path.insert(0, str(ROOT))
    from tools.session_i2.pinned import ReadLeases
    with ReadLeases(ROOT) as leases:
        for path in [*chain.glob('*/*'), *(ROOT / operator.MANIFESTS).iterdir()]:
            require(path.is_file(), 'Nested or unexpected scientific record layout')
            leases.pin(path)
        yield


def verify_chain():
    """The frozen CLI remains the authority, not this publication layer."""
    build = operator.command(['tools/frontier/f1_build.py', '--verify'], 'PASS')
    require(build['digest'] == operator.BUILD and build['executable_sha3_256'] == operator.WORKER
            and build['table_digest'] == operator.TABLE, 'Accepted build identity mismatch')
    require(operator.driver('rules', status='rules_pass')['table_digest'] == operator.TABLE, 'Rule table mismatch')
    snapshot = operator.driver('snapshot', '--file', 'config/frontier_snapshot_v2.json', status='research_only_unaccepted')
    require(snapshot['digest'] == operator.SNAPSHOT and snapshot['operational']['B'] == operator.BASE, 'Snapshot mismatch')
    print('Auditing the full immutable chain; this can take several minutes.', flush=True)
    receipt = ROOT / operator.TIP
    require(receipt.exists() and receipt.stat().st_size <= 131072, 'Retained continuation receipt is missing or oversized')
    saved = json.loads(receipt.read_text(encoding='ascii'))
    published = operator.published_anchor()
    extended = len(list((ROOT / operator.CHAIN).glob('*/certificate.json'))) > 256
    audit = None
    if extended:
        sys.path.insert(0, str(ROOT))
        from tools.session_i2.identity import accepted
        require(accepted(), 'Extended publication requires accepted SESSION-I2')
        audit = operator.command(['-m', 'tools.session_i2.audit', '--dir', str(operator.CHAIN),
                                  '--anchor', str(published['batches']), '--anchor', str(saved['batches'])],
                                 'I2_PUBLICATION_AUDIT')
        ledger = audit['ledger']
        require(ledger['status'] == 'conditional_chain', 'Independent I2 ledger refused')
    else:
        ledger = operator.driver('ledger', '--dir', operator.CHAIN, status='conditional_chain')
    require(ledger['start'] == operator.BASE and ledger['genesis_digest'] == operator.GENESIS, 'Chain root mismatch')
    operator.check_anchor(published, ledger, audit['anchors'] if audit else None)
    require(saved == {key: ledger[key] for key in saved} and set(saved) == {
        'batches', 'end', 'genesis_digest', 'latest_certificate_digest'}, 'Receipt does not exactly match chain')
    count = int(ledger['batches'])
    require({p.name for p in (ROOT / operator.CHAIN).iterdir() if p.is_dir()} ==
            {f'batch-{i:04d}' for i in range(1, count + 1)}, 'Uncommitted or unexpected batch directory')
    require({p.name for p in (ROOT / operator.MANIFESTS).glob('batch-*.json')} ==
            {f'batch-{i:04d}.json' for i in range(1, count + 1)}, 'Uncommitted or unexpected manifest')
    final = operator.CHAIN / f'batch-{count:04d}'
    verified = audit['verified'] if audit else operator.driver('verify-batch', '--certificate', final / 'certificate.json', status='conditional_complete')
    replay = audit['replay'] if audit else operator.driver('replay', '--batch-dir', final, status='REFERENCE_REPLAY_MATCH')
    require(verified['digest'] == replay['digest'] == ledger['latest_certificate_digest'] and
            verified['batch_end'] == replay['batch_end'] == ledger['end'], 'Final verification mismatch')
    inspection = audit['inspection'] if audit else operator.driver('inspect', '--batch-dir', final, status='INSPECTION_ONLY')
    recovery = inspection.get('recovery', {})
    require(recovery.get('status') == 'RECOVERABLE' and recovery.get('pending') is None and
            not recovery.get('warnings') and inspection['temporaries'] == '0', 'Final checkpoint needs attention')
    certificates = [json.loads((ROOT / operator.CHAIN / f'batch-{i:04d}/certificate.json').read_text(encoding='ascii'))
                    for i in range(1, count + 1)]
    require(all(c['status'] == 'conditional_complete' and int(c['unresolved_count']) == 0 for c in certificates),
            'Unresolved or uncommitted certificate')
    return ledger, certificates


def replace_field(text, pattern, value):
    updated, count = re.subn(pattern, lambda _: value, text, flags=re.MULTILINE)
    require(count == 1, 'Aggregate record field is missing or ambiguous')
    return updated


def derive_files(contents, certificates, ledger, source_commit, last_time):
    """Preserve historical prose/tables and update the one current claim block."""
    progress = contents['docs/RUN1_PROGRESS.md']
    old = website_progress.build(progress)
    old_count = len(old['batches'])
    count = len(certificates)
    require(count >= old_count, 'Local chain is shorter than published record')
    for batch, cert in zip(old['batches'], certificates):
        require(batch['start'] == cert['batch_start'] and batch['end'] == cert['batch_end'] and
                batch['certificate_digest'] == cert['digest'], 'Published batch differs from saved certificate')
    if count == old_count:
        return {}
    total = int(ledger['end']) - int(operator.BASE)
    rows = [f"| {i} | `[{c['batch_start']},{c['batch_end']})` | {int(c['batch_end'])-int(c['batch_start'])} | `{c['digest']}` |"
            for i, c in enumerate(certificates, 1) if i > old_count]
    added = int(ledger['end']) - int(old['coverage']['end'])
    paragraph = (f"Owner-run continuation recorded by the publication command: batches {old_count + 1}–{count} "
                 f"add {added} integers in `[{old['coverage']['end']},{ledger['end']})`. Full chain audit, accepted "
                 "build verification, final certificate verification, reference replay and checkpoint inspection passed. "
                 "The retained receipt matches; no scientific batch was executed by the publisher.\n\n"
                 "| Batch | Half-open interval | Width | Certificate digest |\n|---|---|---:|---|\n" + '\n'.join(rows) + '\n\n')
    if count > 256:
        paragraph = ("Execution profile: **CEML-SESSION-I2 extension using unchanged V2-format certificates**. "
                     "The frozen V2 admission cap remains 256; this separately accepted profile extends its audited prefix. "
                     "Independent publication replays every retained batch through frozen V2 arithmetic in a fresh audit.\n\n" + paragraph)
    marker = '```text\nCEML-FRONTIER-2 conditional batch chain'
    require(progress.count(marker) == 1, 'Claim block missing or ambiguous')
    progress = progress.replace(marker, paragraph + marker, 1)
    fields = {
        r'^Verified conditional on that assumption:.*$': f"Verified conditional on that assumption: every integer in [{operator.BASE},{ledger['end']}) converges",
        r'^Batches:.*$': f'Batches: {count} ({total} integers)',
        r'^Latest certificate digest:.*$': f"Latest certificate digest: {ledger['latest_certificate_digest']}",
        r'^Rule counts \(E2, Q4, P3, M9, S2K4-03, EXPLICIT\):.*$': 'Rule counts (E2, Q4, P3, M9, S2K4-03, EXPLICIT): ' + ', '.join(str(sum(int(c['counts'][k]) for c in certificates)) for k in KEYS),
        r'^Explicit shortened-map steps computed:.*$': 'Explicit shortened-map steps computed: {} ({} odd; {} standard-map steps)'.format(*(sum(int(c[k]) for c in certificates) for k in ('explicit_t_steps', 'explicit_odd_steps', 'explicit_standard_steps'))),
        r'^Run dates \(UTC\):.*$': f'Run dates (UTC): {last_time[:10]}; chain began 2026-10-12; latest certificate filesystem timestamp {last_time} (batch {count}); not an end-to-end timer',
    }
    for pattern, value in fields.items():
        progress = replace_field(progress, pattern, value)
    anchor_line = f'Source commit at automated confirmation: {source_commit} (records bind the build digest, not a Git SHA)'
    if re.search(r'^Source commit at automated confirmation:', progress, re.MULTILINE):
        progress = replace_field(progress, r'^Source commit at automated confirmation:.*$', anchor_line)
    else:
        progress = progress.replace('Rule counts (E2,', anchor_line + '\nRule counts (E2,', 1)
    data = website_progress.build(progress)
    require(data['coverage']['end'] == ledger['end'] and data['latest_certificate_digest'] == ledger['latest_certificate_digest'],
            'Derived website record mismatch')
    status = replace_field(contents['PROGRAM_STATUS.md'], r'^\*\*Latest verified publication — .*?\*\*.*$',
        f"**Latest verified publication — {count} batches.** The owner-run chain covers `[{operator.BASE},{ledger['end']})` "
        f"({total} integers), latest certificate `{ledger['latest_certificate_digest']}`, with zero unresolved. "
        "Full-chain audit, accepted build verification, final verification, replay and inspection passed; the retained receipt matches. "
        "The separate owner-invoked publisher updates this aggregate and the derived website feed without scientific execution. "
        "Historical completion records retain their original endpoints. See `docs/RUN1_PROGRESS.md`.")
    status = replace_field(status, r'^\*\*New batch-verifier implementation:.*$',
        f'**New batch-verifier implementation:** VERSION-2 GMP/PYTHON VERIFIER, L1 PASS OWNER-ACCEPTED 2026-10-12; {count} COMMITTED AND VERIFIED BATCHES, {total} INTEGERS; SEE docs/RUN1_PROGRESS.md')
    start = replace_field(contents['START_HERE.md'], r'^\*\*Latest published result:.*$',
        f"**Latest published result:** {count} committed and verified batches, covering {total} integers through exclusive endpoint `{ledger['end']}`, "
        "conditional on the accepted author-reported operational base. See [RUN1 progress](docs/RUN1_PROGRESS.md). "
        "The offline runner logs locally; the separate publication command verifies and updates GitHub and the website feed.")
    return dict(zip(FILES, (progress, website_progress.render(data), status, start)))


def publish(files, base, ledger):
    commit = api(f'repos/{REPO}/git/commits/{base}')
    branch = f"codex/frontier-publish-{ledger['batches']}-{ledger['latest_certificate_digest'][:12]}"
    head = commit_files(base, commit['tree']['sha'], files, f"CEML-RUN1: publish {ledger['batches']} verified batches")
    api(f'repos/{REPO}/git/refs', 'POST', {'ref': 'refs/heads/' + branch, 'sha': head})
    pr = api(f'repos/{REPO}/pulls', 'POST', {
        'base': 'main', 'head': branch,
        'title': f"CEML-RUN1: publish {ledger['batches']} verified batches",
        'body': f"Owner-invoked publication after full chain audit, unchanged accepted build verification, final certificate verification, reference replay and inspection. Latest endpoint {ledger['end']}; latest certificate {ledger['latest_certificate_digest']}. Raw batch data remains local. Conditional on the accepted author-reported base; no independent reproduction or world-frontier claim. No scientific batch executed. Derived website feed validated against the complete aggregate record."})
    # Keep a concrete retry/review reference if GitHub requires a check or review.
    receipt = ROOT / 'local/frontier/publication-pr.json'
    receipt.write_text(json.dumps({'url': pr['html_url'], 'number': pr['number'], 'head': head}) + '\n', encoding='ascii')
    print('Created ' + pr['html_url'], flush=True)
    for _ in range(12):
        info = api(f"repos/{REPO}/pulls/{pr['number']}")
        if info.get('mergeable') is not None:
            break
        time.sleep(1)
    statuses = api(f'repos/{REPO}/commits/{head}/status')
    checks = api(f'repos/{REPO}/commits/{head}/check-runs')['check_runs']
    require(not statuses['total_count'] or statuses['state'] == 'success', 'GitHub status checks need attention; PR retained')
    require(all(c['status'] == 'completed' and c['conclusion'] in ('success', 'neutral', 'skipped') for c in checks),
            'GitHub checks need attention; PR retained')
    require(info['head']['sha'] == head and info.get('mergeable') is True, 'PR changed or needs review; PR retained')
    merged = api(f"repos/{REPO}/pulls/{pr['number']}/merge", 'PUT', {'sha': head, 'merge_method': 'merge'})
    require(merged.get('merged') is True, 'GitHub did not merge; PR retained')
    git('fetch', '--no-tags', 'origin', 'main')
    git('merge', '--ff-only', 'origin/main')
    return pr['html_url']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true', help='verify and show the proposed aggregate without network or changes')
    args = parser.parse_args()
    try:
        require(not git('status', '--porcelain=v1'), 'Working tree must be clean')
        source = git('rev-parse', 'HEAD')
        git('merge-base', '--is-ancestor', operator.ACCEPTED_SOURCE, source)
        if not args.preview:
            require(git('branch', '--show-current') == 'main', 'Run publication from main')
            authenticate()
            git('fetch', '--no-tags', 'origin', 'main')
            require(source == git('rev-parse', 'origin/main'), 'Local main differs from GitHub; synchronize before publishing')
        with operator.operator_lock(), publication_leases():
            ledger, certificates = verify_chain()
            contents = {p: (ROOT / p).read_text(encoding='utf-8') for p in FILES}
            latest = ROOT / operator.CHAIN / f"batch-{int(ledger['batches']):04d}/certificate.json"
            files = derive_files(contents, certificates, ledger, source, stamp(latest))
            if args.preview:
                print(json.dumps({**ledger, 'status': 'PUBLICATION_PREVIEW', 'changed_files': list(files)}))
            elif not files:
                print(json.dumps({**ledger, 'status': 'ALREADY_PUBLISHED'}))
            else:
                url = publish(files, source, ledger)
                print(json.dumps({**ledger, 'status': 'PUBLISHED', 'pull_request': url}))
        return 0
    except (PublicationError, website_progress.PublicationError, operator.StopRun, IntegrityError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print('PUBLICATION_STOPPED: ' + str(error), file=sys.stderr)
        print('No scientific batch executed. Any created PR is retained for review.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
