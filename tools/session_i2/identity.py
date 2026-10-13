"""Versioned candidate identity and explicit owner acceptance for session I2."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROFILE = 'CEML-SESSION-I2'
V2_BUILD = 'c0263b353e05b9f3d09730e67d321254952c7dbdc2a6d892f7ffe2b14b89c032'
ACCEPTANCE = ROOT / 'local/frontier/session-i2-owner-acceptance.json'
PREFIX_BATCHES = 256
PREFIX_END = '2392518188130441801866'
PREFIX_DIGEST = 'a6ab30751d0762f10f783bebf858f846aaf948098db2879a38099b2881e61565'


def identity_paths():
    return sorted([*Path(__file__).parent.glob('*.py'), *(ROOT/'tests/session_i2').glob('*.py'),
                   ROOT/'docs/SESSION_I2_PROTOCOL.md', ROOT/'tools/operator/run_frontier.py', ROOT/'tools/publication/publish.py'])


def digest():
    values = {p.relative_to(ROOT).as_posix(): hashlib.sha3_256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
              for p in identity_paths()}
    return hashlib.sha3_256(b'CEML-SESSION-I2/PROFILE\0'+json.dumps(values,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def accepted():
    if not ACCEPTANCE.exists():
        return False
    data = json.loads(ACCEPTANCE.read_text(encoding='ascii'))
    expected = {'profile':PROFILE,'profile_digest':digest(),'v2_build_digest':V2_BUILD,'acknowledgement':'ACCEPT-SESSION-I2'}
    if data != expected:
        raise ValueError('I2 acceptance identity mismatch; no automatic fallback')
    return True
