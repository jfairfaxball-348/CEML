"""Windows integrity and compatibility tests on designated small fixtures only."""
import copy
import json
import mmap
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/session_i1'))
from identity import accepted, digest
from pinned import ReadLeases, IntegrityError
from session import Session
from worker import dispatch


@unittest.skipUnless(os.name=='nt','I1 deliberately requires Windows read leases')
class Leases(unittest.TestCase):
    def test_protected_files_and_ancestors_allow_new_children(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'local/frontier') as tmp:
            directory=Path(tmp)/'sealed';directory.mkdir();path=directory/'data';path.write_bytes(b'a')
            with ReadLeases(ROOT) as leases:
                self.assertEqual(leases.pin(path),b'a')
                for operation in (lambda:path.write_bytes(b'b'),path.unlink,
                                  lambda:path.rename(directory/'renamed'),lambda:directory.rename(Path(tmp)/'renamed')):
                    with self.assertRaises(OSError):operation()
                (Path(tmp)/'next').mkdir()
                (directory/'extra').write_bytes(b'x')
            path.write_bytes(b'b')

    def test_existing_writer_refuses_lease(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'local/frontier') as tmp:
            path=Path(tmp)/'data';path.write_bytes(b'a')
            with path.open('r+b'),ReadLeases(ROOT) as leases:
                with self.assertRaises(IntegrityError): leases.pin(path)

    def test_existing_writable_mapping_and_hardlink_cannot_bypass(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'local/frontier') as tmp:
            path=Path(tmp)/'data';path.write_bytes(b'abc')
            handle=path.open('r+b');view=mmap.mmap(handle.fileno(),0,access=mmap.ACCESS_WRITE);handle.close()
            try:
                with ReadLeases(ROOT) as leases:
                    with self.assertRaises(IntegrityError):leases.pin(path)
            finally:view.close()
            alias=Path(tmp)/'alias';os.link(path,alias)
            with ReadLeases(ROOT) as leases:
                leases.pin(path)
                with self.assertRaises(OSError):alias.write_bytes(b'xyz')

    def test_external_path_refused(self):
        with ReadLeases(ROOT) as leases:
            with self.assertRaises(IntegrityError):leases.pin(ROOT.parent/'anything')

    def test_reparse_point_refused(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'local/frontier') as tmp:
            path=Path(tmp)/'data';path.write_bytes(b'a');link=Path(tmp)/'link'
            try:link.symlink_to(path)
            except OSError:
                target=Path(tmp)/'directory';target.mkdir()
                result=subprocess.run(['cmd.exe','/c','mklink','/J',str(link),str(target)],capture_output=True)
                self.assertEqual(result.returncode,0)
            with ReadLeases(ROOT) as leases:
                with self.assertRaises(IntegrityError):leases.pin(link)


@unittest.skipUnless(os.name=='nt','Windows execution profile')
class Incremental(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved=tempfile.TemporaryDirectory(dir=ROOT/'local/frontier')
        with Session(cls.saved.name,test=True,allow_empty=True) as session:
            cls.f=session.f
            run=session.f.fixture_run('L1-fixture-a')
            session.execute(Path(cls.saved.name)/'a',run)
            cls.first=session.cached_certificate(Path(cls.saved.name)/'a/certificate.json')
            cls.successor=session.f.fixture_run('L1-fixture-successor')
            cls.successor['predecessor_digest']=cls.first['digest']

    @classmethod
    def tearDownClass(cls):cls.saved.cleanup()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'local/frontier')
        self.root=Path(self.tmp.name)
        shutil.copytree(Path(self.saved.name)/'a',self.root/'a')

    def tearDown(self):self.tmp.cleanup()

    def test_startup_replay_and_only_new_arithmetic(self):
        with Session(self.root,test=True) as session:
            with patch.object(session.f,'summary_reference',wraps=session.f.summary_reference) as replay:
                result=session.execute(self.root/'b',self.successor)
                self.assertEqual(result['status'],'NONSCIENTIFIC_FIXTURE')
                # Checkpoint recovery also independently checks new-batch prefixes.
                self.assertGreaterEqual(replay.call_count,2)
                self.assertTrue(all(args.args[0]==146 and 146<=args.args[1]<=290 for args in replay.call_args_list))
                calls=replay.call_count
                session.ledger();session.cached_certificate(self.root/'a/certificate.json')
                self.assertEqual(replay.call_count,calls)
            self.assertEqual(session.f.ledger(self.root,True),session.ledger())
            with self.assertRaises(TypeError):session._verified[self.first['digest']]['batch_end']='0'
        with Session(self.root,test=True) as reopened:
            self.assertEqual(reopened.ledger()['batches'],'2')

    def test_identical_certificates_to_legacy(self):
        with Session(self.root,test=True) as session:
            result=session.execute(self.root/'b',self.successor)
            legacy=self.root.parent/(self.root.name+'-legacy')
            try:
                legacy.mkdir();shutil.copytree(self.root/'a',legacy/'a')
                session.f.prepare_fixture(legacy/'b',self.successor)
                old=session.f.run_batch(legacy/'b',self.successor,True)
                self.assertEqual(old['digest'],result['digest'])
                self.assertEqual((legacy/'b/certificate.json').read_bytes(),(self.root/'b/certificate.json').read_bytes())
            finally:shutil.rmtree(legacy)

    def test_unexpected_file_and_directory_stop(self):
        with Session(self.root,test=True) as session:
            extra=self.root/'a/extra';extra.write_bytes(b'x')
            with self.assertRaises(IntegrityError):session.ledger()
            extra.unlink();(self.root/'unfinished').mkdir()
            with self.assertRaises(IntegrityError):session.ledger()

    def test_corrupt_and_forged_certificates_refuse_restart(self):
        certificate=self.root/'a/certificate.json';raw=certificate.read_bytes()
        corrupt=json.loads(raw);corrupt['digest']='0'*64
        certificate.write_bytes(self.f.canonical(corrupt))
        with self.assertRaisesRegex(Exception,'record digest mismatch'):Session(self.root,test=True)
        forged=json.loads(raw);forged['explicit_t_steps']=str(int(forged['explicit_t_steps'])+1)
        forged=self.f.seal(forged,'CERTIFICATE')
        certificate.write_bytes(self.f.canonical(forged))
        with self.assertRaisesRegex(Exception,'replay mismatch'):Session(self.root,test=True)

    def test_duplicate_and_missing_genesis_refuse(self):
        shutil.copytree(self.root/'a',self.root/'duplicate')
        with self.assertRaisesRegex(Exception,'Duplicate/fork'):Session(self.root,test=True)
        shutil.rmtree(self.root/'duplicate')
        with Session(self.root,test=True) as session:session.execute(self.root/'b',self.successor)
        shutil.rmtree(self.root/'a')
        with self.assertRaisesRegex(Exception,'predecessor missing'):Session(self.root,test=True)

    def test_wrong_successor_never_creates_batch(self):
        for key,value in (('predecessor_digest','0'*64),('batch_start','147'),('run_id','L1-fixture-b')):
            run=copy.deepcopy(self.successor);run[key]=value
            with Session(self.root,test=True) as session:
                with self.assertRaises((session.f.Refusal,IntegrityError)):session.execute(self.root/'b',run)
                self.assertTrue(session.closed)
            self.assertFalse((self.root/'b').exists())

    def test_native_replay_mismatch_preserves_uncommitted_files(self):
        with Session(self.root,test=True) as session:
            original=session.f.summary_reference
            def corrupt(start,end,*args):
                result=original(start,end,*args)
                if end>start:result['explicit_t_steps']=str(int(result['explicit_t_steps'])+1)
                return result
            with patch.object(session.f,'summary_reference',side_effect=corrupt):
                with self.assertRaisesRegex(Exception,'replay'):session.execute(self.root/'b',self.successor)
            self.assertTrue(session.closed)
            self.assertFalse((self.root/'b/certificate.json').exists())
        with self.assertRaises(IntegrityError):Session(self.root,test=True)

    def test_pending_is_never_promoted(self):
        with Session(self.root,test=True) as session:
            run=copy.deepcopy(self.successor);run['max_t_per_explicit']='1';run['max_total_t']='1'
            result=session.execute(self.root/'b',run)
            self.assertEqual(result['status'],'INCOMPLETE');self.assertTrue(session.closed)
            self.assertFalse((self.root/'b/certificate.json').exists())

    def test_failure_after_atomic_certificate_requires_restart_audit(self):
        with Session(self.root,test=True) as session:
            with patch.object(session.f,'inspect_batch',side_effect=OSError('injected inspection loss')):
                with self.assertRaises(OSError):session.execute(self.root/'b',self.successor)
            self.assertTrue(session.closed)
        self.assertTrue((self.root/'b/certificate.json').exists())
        with Session(self.root,test=True) as restarted:self.assertEqual(restarted.ledger()['batches'],'2')

    def test_bad_checkpoint_warning_prevents_promotion(self):
        with Session(self.root,test=True) as session:
            with patch.object(session.f,'inspect_batch',return_value={'recovery':{'status':'RECOVERABLE','pending':None,'warnings':['damage']},'temporaries':'0'}):
                with self.assertRaises(IntegrityError):session.execute(self.root/'b',self.successor)
            self.assertTrue(session.closed)

    def test_rpc_rejects_external_paths_and_unknown_operations(self):
        with Session(self.root,test=True) as session:
            with self.assertRaises(IntegrityError):dispatch(session,['ledger','--dir',str(self.root.parent)])
            with self.assertRaises(IntegrityError):dispatch(session,['verify-batch','--certificate',str(self.root.parent/'certificate.json')])
            with self.assertRaises((SystemExit,Exception)):dispatch(session,['resume'])

    def test_scientific_write_requires_acceptance(self):
        with Session(self.root,test=True) as session:
            session.test=False
            with patch('session.accepted',return_value=False):
                with self.assertRaises(IntegrityError):session.execute(self.root/'b',self.successor)
            self.assertFalse((self.root/'b').exists())

    def test_profile_acceptance_fail_closed(self):
        path=self.root/'acceptance'
        with patch('identity.ACCEPTANCE',path):
            self.assertFalse(accepted())
            path.write_text('{}',encoding='ascii')
            with self.assertRaises(ValueError):accepted()
            self.assertEqual(len(digest()),64)


if __name__=='__main__':unittest.main()
