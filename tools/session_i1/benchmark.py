"""Read-only before/after benchmark of existing certificates. Executes no science."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time

from identity import ROOT, V2_BUILD, digest
from session import Session


def inventory(chain):
    paths=[*chain.rglob('*'),*(chain.parent/(chain.name+'-manifests')).glob('*.json')]
    return {p.relative_to(ROOT).as_posix():hashlib.sha3_256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--batches',nargs='+',type=int,default=[3,64,208])
    args=parser.parse_args()
    sys.path.insert(0,str(ROOT/'tools/operator'))
    from run_frontier import operator_lock, CHAIN
    chain=ROOT/CHAIN
    before=inventory(chain)
    result=dict(scope='read-only existing certificates; no scientific batches',v2_build_digest=V2_BUILD,profile_digest=digest(),cases=[])
    with operator_lock():
        sys.path.insert(0,str(ROOT/'tools/frontier'))
        import ceml_frontier as legacy
        for number in args.batches:
            path=chain/f'batch-{number:04d}'/'certificate.json'
            started=time.perf_counter();certificate=legacy.verify_batch(path);elapsed=time.perf_counter()-started
            case=dict(batch=number,width=int(certificate['batch_end'])-int(certificate['batch_start']),
                      legacy_seconds=elapsed,digest=certificate['digest'])
            result['cases'].append(case);print(json.dumps(case),flush=True)
        started=time.perf_counter()
        with Session(chain) as session:
            result['full_startup_seconds']=time.perf_counter()-started
            for case in result['cases']:
                times=[]
                for _ in range(3):
                    started=time.perf_counter()
                    cert=session.verify_existing(chain/f"batch-{case['batch']:04d}"/'certificate.json')
                    times.append(time.perf_counter()-started)
                    assert cert['digest']==case['digest']
                case.update(i1_seconds=statistics.median(times),i1_samples=times)
                case['speedup']=case['legacy_seconds']/case['i1_seconds']
                print(json.dumps(case),flush=True)
            times=[]
            for _ in range(10):
                started=time.perf_counter();session.ledger();times.append(time.perf_counter()-started)
            result['cached_ledger_median_seconds']=statistics.median(times)
        assert before==inventory(chain),'Historical record inventory changed'
    result['historical_files_unchanged']=len(before)
    Path(args.out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='ascii')
    print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':main()
