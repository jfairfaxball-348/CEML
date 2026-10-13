"""Persistent local pipe worker; its trust never survives process exit."""
import argparse
import json
from pathlib import Path
import sys

from identity import PROFILE, digest, accepted
from session import Session, require


def dispatch(session, arguments):
    parser=argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('operation', choices=('ledger','verify-batch','prepare-manifest','pilot','replay','inspect'))
    for option in ('dir','certificate','out','authority-id','acknowledge','max-t-per-explicit',
                   'max-total-t','after-certificate','width','manifest','batch-dir'):
        parser.add_argument('--'+option)
    args=parser.parse_args(arguments)
    session.guard()
    if args.operation=='ledger':
        require(Path(args.dir).absolute()==session.chain,'Ledger outside session')
        return session.ledger()
    if args.operation=='verify-batch':
        cert=session.cached_certificate(args.certificate)
        return dict(status='conditional_complete',digest=cert['digest'],batch_start=cert['batch_start'],batch_end=cert['batch_end'])
    if args.operation=='prepare-manifest':
        return session.prepare_manifest(args.out,args.authority_id,args.acknowledge,args.max_t_per_explicit,
                                        args.max_total_t,args.after_certificate,args.width)
    if args.operation=='pilot':
        return session.execute(args.out,session.f.load_record(args.manifest,'run'))
    directory=Path(args.batch_dir).absolute()
    require(directory in session._layout,'Unverified batch path')
    return (session.f.reference_replay if args.operation=='replay' else session.f.inspect_batch)(directory)


def send(value):
    print(json.dumps(value,sort_keys=True),flush=True)


def main():
    try:
        require(len(sys.argv)==2,'Worker needs one chain')
        require(accepted(),'Owner acceptance of SESSION-I1 required')
        with Session(sys.argv[1]) as session:
            send(dict(status='SESSION_READY',profile=PROFILE,profile_digest=digest(),ledger=session.ledger()))
            while True:
                line=sys.stdin.buffer.readline(131073)
                if not line: break
                require(len(line)<=131072 and line.endswith(b'\n'),'Oversized/truncated request')
                request=json.loads(line)
                if request=={'close':True}: break
                require(isinstance(request,list) and all(isinstance(x,str) for x in request),'Invalid request')
                result=dispatch(session,request)
                send(result)
                if session.closed: break
        return 0
    except BaseException as error:
        # Never continue using trust after any exception. Native anomalies remain local.
        if hasattr(error,'record'):
            from identity import ROOT
            import uuid
            folder=ROOT/'local/frontier/refusals';folder.mkdir(exist_ok=True)
            session.f.write_atomic(folder/(uuid.uuid4().hex+'.json'),session.f.canonical(error.record))
        send(dict(status='SESSION_REFUSED',reason=str(error)))
        return 2


if __name__=='__main__': sys.exit(main())
