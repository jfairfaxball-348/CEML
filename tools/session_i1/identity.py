"""Versioned candidate identity and explicit owner acceptance for session I1."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE = 'CEML-SESSION-I1'
V2_BUILD = 'c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032'
ACCEPTANCE = ROOT / 'local/frontier/session-i1-owner-acceptance.json'


def identity_paths():
    return sorted([*Path(__file__).parent.glob('*.py'), *(ROOT/'tests/session_i1').glob('*.py'),
                   ROOT/'docs/SESSION_I1_PROTOCOL.md', ROOT/'tools/operator/run_frontier.py'])


def digest():
    values = {p.relative_to(ROOT).as_posix(): hashlib.sha3_256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
              for p in identity_paths()}
    return hashlib.sha3_256(b'CEML-SESSION-I1/PROFILE\0'+json.dumps(values,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def accepted():
    if not ACCEPTANCE.exists():
        return False
    data = json.loads(ACCEPTANCE.read_text(encoding='ascii'))
    expected = {'profile':PROFILE,'profile_digest':digest(),'v2_build_digest':V2_BUILD,'acknowledgement':'ACCEPT-SESSION-I1'}
    if data != expected:
        raise ValueError('I1 acceptance identity mismatch; no automatic fallback')
    return True
