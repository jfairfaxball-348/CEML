"""Fresh full-chain replay for independent I2 publication; never executes a batch."""
import argparse
import json
from pathlib import Path
import sys

from .identity import ROOT
from .session import Session, require


def audit(chain, anchors, *, test=False):
    # A fresh process/session establishes trust from every certificate, never a
    # runner receipt or a prior session's RAM cache. All replay primitives are V2.
    with Session(chain, test=test) as session:
        ledger = session.ledger()
        verified_anchors = {}
        for number in anchors:
            require(1 <= number <= int(ledger['batches']), 'Audit anchor outside chain')
            path = session.chain / f'batch-{number:04d}' / 'certificate.json'
            cert = session.cached_certificate(path)
            verified_anchors[str(number)] = dict(digest=cert['digest'], batch_end=cert['batch_end'])
        final = session.chain / f"batch-{int(ledger['batches']):04d}"
        cert = session.verify_existing(final / 'certificate.json')
        replay = session.f.reference_replay(final)
        inspection = session.f.inspect_batch(final)
        session.guard()
        return dict(status='I2_PUBLICATION_AUDIT', ledger=ledger, anchors=verified_anchors,
                    verified=dict(digest=cert['digest'], batch_end=cert['batch_end']),
                    replay=replay, inspection=inspection)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir', required=True)
    parser.add_argument('--anchor', type=int, action='append', default=[])
    args = parser.parse_args()
    try:
        chain = Path(args.dir).absolute()
        require(chain == ROOT / 'local/frontier/run1/RUN1-operational-0001', 'Audit chain refused')
        print(json.dumps(audit(chain, args.anchor), sort_keys=True))
        return 0
    except Exception as error:
        print(json.dumps(dict(status='AUDIT_REFUSED', reason=str(error))))
        return 2


if __name__ == '__main__':
    sys.exit(main())
