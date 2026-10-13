"""Long-chain publication routing and observer layout; simulated records only."""
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools/publication'))
import live
import publish
from tools.session_i2 import identity


class Publication(unittest.TestCase):
    def test_publication_keeps_record_bytes_pinned_until_completion(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'local/frontier') as folder:
            root=Path(folder);chain=root/publish.operator.CHAIN
            (chain/'batch-0001').mkdir(parents=True)
            cert=chain/'batch-0001/certificate.json';cert.write_bytes(b'fixture')
            manifests=root/publish.operator.MANIFESTS;manifests.mkdir()
            (manifests/'batch-0001.json').write_bytes(b'fixture')
            with patch.object(publish,'ROOT',root),publish.publication_leases(force=True):
                with self.assertRaises(OSError):cert.write_bytes(b'corrupt')
                with self.assertRaises(OSError):cert.unlink()
            cert.write_bytes(b'released')

    def test_extended_publication_requires_fresh_audit_and_exact_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);chain=root/publish.operator.CHAIN;chain.mkdir(parents=True)
            manifests=root/publish.operator.MANIFESTS;manifests.mkdir()
            for number in range(1,258):
                directory=chain/f'batch-{number:04d}';directory.mkdir()
                (directory/'certificate.json').write_text(json.dumps(dict(status='conditional_complete',unresolved_count='0')))
                (manifests/f'batch-{number:04d}.json').write_text('{}')
            ledger=dict(status='conditional_chain',batches='257',start=publish.operator.BASE,end='10001',genesis_digest=publish.operator.GENESIS,latest_certificate_digest='b'*64)
            receipt={key:ledger[key] for key in ('batches','end','genesis_digest','latest_certificate_digest')}
            (root/publish.operator.TIP).write_text(json.dumps(receipt))
            anchor=dict(batches='256',end='10000',genesis_digest=publish.operator.GENESIS,latest_certificate_digest=identity.PREFIX_DIGEST)
            final=dict(digest='b'*64,batch_end='10001')
            response=dict(status='I2_PUBLICATION_AUDIT',ledger=ledger,anchors={'256':dict(digest=identity.PREFIX_DIGEST,batch_end='10000'),'257':final},verified=final,replay=final,
                          inspection=dict(recovery=dict(status='RECOVERABLE',pending=None,warnings=[]),temporaries='0'))
            calls=[]
            def command(args,status):
                calls.append(args)
                if args[0]=='tools/frontier/f1_build.py':return dict(digest=publish.operator.BUILD,executable_sha3_256=publish.operator.WORKER,table_digest=publish.operator.TABLE)
                self.assertEqual(args[:2],['-m','tools.session_i2.audit'])
                return response
            def driver(operation,*args,**kwargs):
                if operation=='rules':return dict(table_digest=publish.operator.TABLE)
                if operation=='snapshot':return dict(digest=publish.operator.SNAPSHOT,operational=dict(B=publish.operator.BASE))
                self.fail('A long chain must never use recursive verification or a runner cache')
            with patch.object(publish,'ROOT',root),patch.object(publish.operator,'ROOT',root),patch.object(publish.operator,'published_anchor',return_value=anchor),patch.object(publish.operator,'command',side_effect=command),patch.object(publish.operator,'driver',side_effect=driver),patch.object(identity,'accepted',return_value=True),redirect_stdout(io.StringIO()):
                result,certs=publish.verify_chain()
                self.assertEqual(result,ledger);self.assertEqual(len(certs),257)
                response['verified']={'digest':'0'*64,'batch_end':'10001'}
                with self.assertRaises(publish.PublicationError):publish.verify_chain()
                response['verified']=final
                receipt['latest_certificate_digest']='c'*64
                (root/publish.operator.TIP).write_text(json.dumps(receipt))
                with self.assertRaises(publish.PublicationError):publish.verify_chain()
            self.assertIn('--anchor',calls[1])

    def test_observer_handles_numeric_order_after_9999(self):
        with tempfile.TemporaryDirectory() as folder:
            chain=Path(folder)
            for number in (9999,10000,257):
                (chain/f'batch-{number:04d}').mkdir()
                (chain/f'batch-{number:04d}'/'certificate.json').write_text('{}')
            def record(path,tag):
                number=int(path.parent.name[6:])
                return dict(status='conditional_complete',pending=None,unresolved_count='0',batch_start=str(number*4),batch_end=str(number*4+4))
            with patch.object(live,'read_record',side_effect=record):
                report=live.snapshot(chain,None,1)
            self.assertEqual([b['number'] for b in report['recent_batches']],[10000,9999,257])
            (chain/'batch-000257').mkdir()
            with self.assertRaises(ValueError):live.snapshot(chain,None,1)


if __name__=='__main__':unittest.main()
