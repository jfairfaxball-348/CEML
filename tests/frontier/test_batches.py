"""Whole small-batch, transaction and rooted-chain acceptance; no science."""
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/frontier'))
import ceml_frontier as driver
import reference


class BatchTests(unittest.TestCase):
    def setUp(self):
        if not (driver.LOCAL/'build/ceml_frontier.exe').exists():
            self.skipTest('new pinned frontier worker not built')
        self.folder = tempfile.TemporaryDirectory(dir=driver.LOCAL, prefix='batch-tests-')
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.run = driver.fixture_run('L1-fixture-a')

    def prepare(self, name='batch', run=None):
        directory = self.root/name
        driver.prepare_fixture(directory, self.run if run is None else run)
        return directory

    def summary(self, end=146):
        return driver.summary_reference(2, end, 100000, 2000000)

    def test_native_first_pass_separate_full_replay_and_immutable_commit(self):
        directory = self.prepare()
        summary = driver.consume_native(2,146,100000,2000000)
        self.assertEqual(self.summary(), summary)
        store = driver.CheckpointStore(directory,self.run)
        store.write(summary)
        certificate = driver.commit_batch(directory,self.run,summary,True)
        self.assertEqual(certificate,driver.verify_batch(directory/'certificate.json',True))
        frozen = (directory/'certificate.json').read_bytes()
        with self.assertRaises(driver.Refusal):
            driver.commit_batch(directory,self.run,summary,True)
        self.assertEqual(frozen,(directory/'certificate.json').read_bytes())

    def test_resume_independently_reruns_prefix_then_equals_cold_certificate(self):
        directory = self.prepare('resume')
        driver.CheckpointStore(directory,self.run).write(self.summary(31))
        original = driver.consume_native
        calls = []
        def measured(*args,**kwargs):
            calls.append(args[:2])
            return original(*args,**kwargs)
        with patch.object(driver,'consume_native',measured):
            result = driver.resume_batch(directory,True)
        self.assertEqual([(2,31),(2,146)],calls)
        cold = self.prepare('cold')
        summary = original(2,146,100000,2000000)
        certificate = driver.commit_batch(cold,self.run,summary,True)
        self.assertEqual(result['digest'],certificate['digest'])

    def test_unresolved_attempt_remains_pending_outside_coverage(self):
        run = driver.fixture_run('L1-fixture-a',max_t=1)
        directory = self.prepare(run=run)
        summary = driver.consume_native(2,146,1,2000000)
        self.assertEqual('7',summary['next_n'])
        self.assertEqual('7',summary['pending']['n'])
        self.assertEqual('0',summary['counts']['explicit_count'])
        self.assertEqual('1',summary['explicit_attempts'])
        self.assertEqual(5,sum(map(int,summary['counts'].values())))
        self.assertEqual('0',summary['counts']['base_count'])
        self.assertEqual('0',summary['counts']['unresolved_count'])
        driver.CheckpointStore(directory,run).write(summary)
        with self.assertRaises(driver.Refusal):
            driver.commit_batch(directory,run,summary,True)
        self.assertFalse((directory/'certificate.json').exists())

    def test_partial_and_forged_full_certificates_refuse(self):
        directory = self.prepare()
        with self.assertRaises(driver.Refusal):
            driver.commit_batch(directory,self.run,self.summary(31),True)
        summary = self.summary()
        for field in ('counts','transcript_digest','explicit_t_steps','explicit_odd_steps',
                      'explicit_standard_steps','explicit_attempts','next_n'):
            forged = deepcopy(summary)
            if field == 'counts':
                forged[field]['e2_count'] = '71'
            elif field == 'transcript_digest':
                forged[field] = '0'*64
            else:
                forged[field] = str(int(forged[field])+1)
            with self.subTest(field=field),self.assertRaises(driver.Refusal):
                driver.commit_batch(directory,self.run,forged,True)
        cert = driver.commit_batch(directory,self.run,summary,True)
        cert['counts']['explicit_count'] = '14'
        (directory/'certificate.json').write_bytes(driver.canonical(driver.seal(cert,'CERTIFICATE')))
        with self.assertRaises(driver.Refusal):
            driver.verify_batch(directory/'certificate.json',True)

    def test_rooted_contiguous_chain_and_no_uncommitted_predecessor(self):
        first = self.prepare('first')
        certificate = driver.commit_batch(first,self.run,self.summary(),True)
        second_run = driver.fixture_run('L1-fixture-successor')
        second_run['predecessor_digest'] = certificate['digest']
        second = self.prepare('second',second_run)
        summary = driver.consume_native(146,290,100000,2000000)
        second_cert = driver.commit_batch(second,second_run,summary,True)
        self.assertEqual(second_cert,driver.verify_batch(second/'certificate.json',True))
        self.assertEqual('2',driver.ledger(self.root,True)['batches'])
        # A checkpoint alone cannot stand in for the committed first batch.
        (first/'certificate.json').unlink()
        driver.CheckpointStore(first,self.run).write(self.summary())
        with self.assertRaises(driver.Refusal):
            driver.verify_batch(second/'certificate.json',True)

    def test_fixture_is_never_accepted_as_production_base(self):
        with self.assertRaises(driver.Refusal):
            driver.validate_manifest(self.run,driver.snapshot(),False)
        with self.assertRaises(driver.Refusal):
            driver.run1_gate(self.run)
        driver.validate_manifest(self.run,driver.snapshot(),True)
        forged = deepcopy(self.run)
        forged['batch_end'] = '147'
        with self.assertRaises(driver.Refusal):
            driver.validate_manifest(forged,driver.snapshot(),True)

    def test_aborted_or_ambiguous_native_process_never_infers_budget_success(self):
        original = subprocess.Popen
        cases = ["import os; os._exit(99)",
                 "import sys; sys.stderr.write('UNRESOLVED garbage\\n'); sys.exit(3)",
                 "import sys; sys.stdout.write('2|E2|0|0|'); sys.exit(3)"]
        for script in cases:
            def launch(*args,**kwargs):
                return original([sys.executable,'-c',script],**kwargs)
            with self.subTest(script=script),patch.object(driver.subprocess,'Popen',launch),self.assertRaises(driver.Refusal):
                driver.consume_native(2,146,100000,2000000,exe=sys.executable)

    def test_ledger_full_replays_each_certificate_once(self):
        first = self.prepare('first')
        certificate = driver.commit_batch(first,self.run,self.summary(),True)
        second_run = driver.fixture_run('L1-fixture-successor')
        second_run['predecessor_digest'] = certificate['digest']
        second = self.prepare('second',second_run)
        summary = driver.consume_native(146,290,100000,2000000)
        driver.commit_batch(second,second_run,summary,True)
        original = driver.summary_reference
        calls = []
        def measured(*args,**kwargs):
            calls.append(args[:2])
            return original(*args,**kwargs)
        with patch.object(driver,'summary_reference',measured):
            driver.ledger(self.root,True)
        self.assertEqual([(2,146),(146,290)],calls)

    def test_one_active_batch_and_distinct_rerun_identity(self):
        first = self.prepare('first')
        next_run = driver.fixture_run('L1-fixture-successor')
        with self.assertRaises(driver.Refusal):
            driver.ensure_chain_slot(self.root/'second',next_run)
        certificate = driver.commit_batch(first,self.run,self.summary(),True)
        next_run['predecessor_digest'] = certificate['digest']
        driver.ensure_chain_slot(self.root/'second',next_run)
        with self.assertRaises(driver.Refusal):
            driver.ensure_chain_slot(self.root/'rerun',self.run)


if __name__ == '__main__':
    unittest.main()
