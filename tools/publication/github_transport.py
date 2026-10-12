"""GitHub CLI transport for optional publishing, never imported by the runner."""
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REPO = 'jfairfaxball-348/CEML'
ACCOUNT = 'jfairfaxball-348'


class PublicationError(Exception):
    pass


def run(args, *, data=None, cwd=ROOT, timeout=60):
    result = subprocess.run(args, cwd=cwd, input=data, capture_output=True,
                            text=True, encoding='utf-8', timeout=timeout)
    if result.returncode:
        # Do not echo credentials, process command lines or HTTP request bodies.
        raise PublicationError(f'{Path(args[0]).name} {args[1]} failed (exit {result.returncode})')
    return result.stdout.strip()


def api(endpoint, method='GET', body=None):
    gh = shutil.which('gh')
    if not gh:
        raise PublicationError('Install GitHub CLI, then run gh auth login')
    args = [gh, 'api', '--hostname', 'github.com', '--method', method, endpoint]
    data = None
    if body is not None:
        args += ['--input', '-']
        data = json.dumps(body, ensure_ascii=False)
    output = run(args, data=data)
    return json.loads(output) if output else None


def authenticate():
    try:
        user = api('user')
    except (PublicationError, subprocess.TimeoutExpired) as error:
        raise PublicationError('Sign in first: gh auth login --hostname github.com --git-protocol https --web') from error
    if user['login'] != ACCOUNT:
        raise PublicationError(f'Switch GitHub CLI to the repository owner account {ACCOUNT}')


def commit_files(parent, base_tree, files, message):
    entries = []
    for path, content in files.items():
        blob = api(f'repos/{REPO}/git/blobs', 'POST', {'content': content, 'encoding': 'utf-8'})
        entries.append(dict(path=path, mode='100644', type='blob', sha=blob['sha']))
    body = {'tree': entries}
    if base_tree:
        body['base_tree'] = base_tree
    tree = api(f'repos/{REPO}/git/trees', 'POST', body)
    return api(f'repos/{REPO}/git/commits', 'POST',
               {'message': message, 'tree': tree['sha'], 'parents': [parent] if parent else []})['sha']
