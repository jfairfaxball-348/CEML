"""Whole small-batch, transaction and rooted-chain acceptance; no science."""
from copy import deepcopy
import json
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

    def checkpointed(self, name, cursors, run=None):
        """A prepared fixture with its root and one further generation per cursor."""
        directory = self.prepare(name, run)
        store = driver.CheckpointStore(directory, self.run if run is None else run)
        store.initialize()
        for cursor in cursors:
            store.write(self.summary(cursor))
        return directory, store

    def test_native_first_pass_separate_full_replay_and_immutable_commit(self):
        directory = self.prepare()
        summary = driver.consume_native(2,146,100000,2000000)
        self.assertEqual(self.summary(), summary)
        store = driver.CheckpointStore(directory,self.run)
        store.initialize()
        store.write(summary)
        certificate = driver.commit_batch(directory,self.run,summary,True)
        self.assertEqual(certificate,driver.verify_batch(directory/'certificate.json',True))
        frozen = (directory/'certificate.json').read_bytes()
        with self.assertRaises(driver.Refusal):
            driver.commit_batch(directory,self.run,summary,True)
        self.assertEqual(frozen,(directory/'certificate.json').read_bytes())

    def test_run_batch_writes_root_then_one_generation_then_certificate(self):
        directory = self.prepare()
        outcome = driver.run_batch(directory, self.run, True)
        self.assertEqual('NONSCIENTIFIC_FIXTURE', outcome['status'])
        names = sorted(path.name for path in directory.iterdir())
        self.assertEqual(['acceptance.json', 'certificate.json', 'ckpt.0.json', 'ckpt.1.json',
                          'run.json', 'snapshot.json'], names)
        root = driver.load_record(directory/'ckpt.0.json', 'checkpoint')
        final = driver.load_record(directory/'ckpt.1.json', 'checkpoint')
        self.assertEqual(('0', '2', '1', '146', root['digest']),
                         (root['generation'], root['next_n'], final['generation'], final['next_n'],
                          final['previous_checkpoint_digest']))
        certificate = driver.verify_batch(directory/'certificate.json', True)
        self.assertEqual((outcome['digest'], 'CEML-FRONTIER-2-CERTIFICATE'),
                         (certificate['digest'], certificate['schema']))
        # A second attempt in the same directory can neither restart nor recommit.
        with self.assertRaises(driver.Refusal):
            driver.run_batch(directory, self.run, True)
        with self.assertRaises(driver.Refusal):
            driver.resume_batch(directory, True)
        self.assertEqual(driver.canonical(certificate), (directory/'certificate.json').read_bytes())

    def test_resume_independently_reruns_prefix_then_equals_cold_certificate(self):
        directory, _ = self.checkpointed('resume', (31,))
        original = driver.consume_native
        calls = []
        def measured(*args,**kwargs):
            calls.append(args[:2])
            return original(*args,**kwargs)
        with patch.object(driver,'consume_native',measured):
            result = driver.resume_batch(directory,True)
        self.assertEqual([(2,31),(2,146)],calls)
        self.assertEqual([], result['warnings'])
        cold = self.prepare('cold')
        summary = original(2,146,100000,2000000)
        certificate = driver.commit_batch(cold,self.run,summary,True)
        self.assertEqual(result['digest'],certificate['digest'])
        self.assertEqual((cold/'certificate.json').read_bytes(), (directory/'certificate.json').read_bytes())

    def test_cold_and_resumed_certificates_are_equal_from_fallback_recoveries(self):
        cold = self.prepare('cold')
        expected = driver.run_batch(cold, self.run, True)['digest']
        cold_bytes = (cold/'certificate.json').read_bytes()
        # (name, cursors of generations 1.., slot to damage, slot to delete, recovered generation)
        cases = (('torn-newest', (7, 15, 31, 55), 1, None, '3'),
                 ('lost-newest', (7, 15, 31, 55, 79), None, 2, '4'),
                 ('torn-oldest', (7, 15, 31, 55, 79), 0, None, '5'),
                 ('root-after-torn-first', (7,), 1, None, '0'))
        for name, cursors, torn, deleted, generation in cases:
            with self.subTest(case=name):
                directory, store = self.checkpointed(name, cursors)
                if torn is not None:
                    (directory/f'ckpt.{torn}.json').write_bytes(b'torn')
                if deleted is not None:
                    (directory/f'ckpt.{deleted}.json').unlink()
                recovered, warnings = store.recover()
                self.assertEqual(generation, recovered['generation'])
                self.assertTrue(warnings)
                result = driver.resume_batch(directory, True)
                self.assertEqual((expected, 'NONSCIENTIFIC_FIXTURE'), (result['digest'], result['status']))
                self.assertTrue(result['warnings'])
                self.assertEqual(cold_bytes, (directory/'certificate.json').read_bytes())
                newest = store.recover()[0]
                self.assertEqual((str(int(generation)+1), '146'), (newest['generation'], newest['next_n']))

    def test_resume_refuses_unauthenticated_checkpoint_history_and_never_commits(self):
        def sole_later(directory):
            (directory/'ckpt.0.json').unlink()
            (directory/'ckpt.1.json').write_bytes(b'torn')
        def torn_middle(directory):
            (directory/'ckpt.1.json').write_bytes(b'torn')
        def all_torn(directory):
            for slot in range(3):
                (directory/f'ckpt.{slot}.json').write_bytes(b'')
        def foreign(directory):
            (directory/'ckpt.0.json').write_bytes(driver.canonical(self.run))
        def no_root(directory):
            for slot in range(3):
                (directory/f'ckpt.{slot}.json').unlink()
        for index, spoil in enumerate((sole_later, torn_middle, all_torn, foreign, no_root)):
            with self.subTest(case=spoil.__name__):
                directory, _ = self.checkpointed(f'refused-{index}', (7, 15))
                spoil(directory)
                with patch.object(driver, 'consume_native') as scan:
                    with self.assertRaises(driver.Refusal):
                        driver.resume_batch(directory, True)
                    scan.assert_not_called()
                self.assertFalse((directory/'certificate.json').exists())

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
        store = driver.CheckpointStore(directory,run)
        store.initialize()
        store.write(summary)
        with self.assertRaises(driver.Refusal):
            driver.commit_batch(directory,run,summary,True)
        self.assertFalse((directory/'certificate.json').exists())

    def test_pending_batch_stays_incomplete_through_generation_4_of_repeated_resume(self):
        run = driver.fixture_run('L1-fixture-a', max_t=1)
        directory = self.prepare(run=run)
        first = driver.run_batch(directory, run, True)
        self.assertEqual(('INCOMPLETE', '7'), (first['status'], first['next_n']))
        store = driver.CheckpointStore(directory, run)
        for generation in (2, 3, 4):
            result = driver.resume_batch(directory, True)
            self.assertEqual(('INCOMPLETE', '7', 'step_budget'),
                             (result['status'], result['next_n'], result['pending']['reason']))
            newest = store.recover()[0]
            self.assertEqual((str(generation), '7', '0', '1'),
                             (newest['generation'], newest['next_n'],
                              newest['counts']['explicit_count'], newest['explicit_attempts']))
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
        chain = driver.ledger(self.root,True)
        self.assertEqual(('2', '2', '290', driver.genesis(self.run), second_cert['digest']),
                         (chain['batches'], chain['start'], chain['end'],
                          chain['genesis_digest'], chain['latest_certificate_digest']))
        # A checkpoint alone cannot stand in for the committed first batch.
        (first/'certificate.json').unlink()
        store = driver.CheckpointStore(first,self.run)
        store.initialize()
        store.write(self.summary())
        with self.assertRaises(driver.Refusal):
            driver.verify_batch(second/'certificate.json',True)
        with self.assertRaises(driver.Refusal):
            driver.ledger(self.root,True)

    def test_version_1_certificate_cannot_be_spliced_in_as_a_predecessor(self):
        first = self.prepare('first')
        certificate = driver.commit_batch(first,self.run,self.summary(),True)
        import hashlib
        old = {key: value for key, value in certificate.items() if key != 'digest'}
        old['schema'] = 'CEML-FRONTIER-1-CERTIFICATE'
        old['digest'] = hashlib.sha3_256(b'CEML-FRONTIER-1/CERTIFICATE\0' + driver.canonical(old)).hexdigest()
        (first/'certificate.json').write_bytes(driver.canonical(old))
        second_run = driver.fixture_run('L1-fixture-successor')
        second_run['predecessor_digest'] = old['digest']
        second = self.prepare('second',second_run)
        summary = driver.consume_native(146,290,100000,2000000)
        with self.assertRaises(driver.Refusal):
            driver.commit_batch(second,second_run,summary,True)
        with self.assertRaises(driver.Refusal):
            driver.run_batch(second,second_run,True)
        self.assertFalse((second/'certificate.json').exists())
        self.assertFalse((second/'ckpt.0.json').exists())

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

    def test_native_death_after_the_root_leaves_a_resumable_uncommitted_batch(self):
        directory = self.prepare()
        failure = driver.NativeFailure('missing/ambiguous native failure status', 99, b'', self.summary(2))
        with patch.object(driver, 'consume_native', side_effect=failure):
            with self.assertRaises(driver.NativeFailure):
                driver.run_batch(directory, self.run, True)
        self.assertFalse((directory/'certificate.json').exists())
        recovered, warnings = driver.CheckpointStore(directory, self.run).recover()
        self.assertEqual(('0', '2', []), (recovered['generation'], recovered['next_n'], warnings))
        result = driver.resume_batch(directory, True)
        cold = self.prepare('cold')
        self.assertEqual(driver.run_batch(cold, self.run, True)['digest'], result['digest'])

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

    def test_wide_fixture_crosses_many_pipe_reads_and_matches_checked_worker(self):
        run = driver.fixture_run('L1-fixture-wide')
        directory = self.prepare('wide', run)
        start, end = driver.FIXTURES['L1-fixture-wide']
        self.assertEqual((2, 9602), (start, end))
        outcome = driver.run_batch(directory, run, True)
        certificate = driver.verify_batch(directory/'certificate.json', True)
        self.assertEqual(outcome['digest'], certificate['digest'])
        self.assertEqual({key: str(value) for key, value in reference.expected_counts(start, end).items()},
                         certificate['counts'])
        self.assertEqual(9600, sum(map(int, certificate['counts'].values())))
        frames = b''.join(reference.iter_events(start, end))
        self.assertGreater(len(frames), 16 * 4096)
        for name in ('ceml_frontier.exe', 'ceml_frontier_checked.exe'):
            result = subprocess.run([str(driver.LOCAL/'build'/name), '--start', str(start), '--end', str(end),
                                     '--max-t-per-explicit', '100000', '--max-total-t', '2000000'],
                                    capture_output=True, timeout=60)
            self.assertEqual((0, b'COMPLETE\n'), (result.returncode, result.stderr))
            self.assertEqual(frames, result.stdout)
        self.assertEqual(driver.H('EVENTS', frames), certificate['transcript_digest'])

    def test_inspection_and_reference_replay_are_read_only(self):
        directory, _ = self.checkpointed('inspected', (7, 15, 31))
        (directory/'ckpt.0.json').write_bytes(b'torn')
        before = {path.name: path.read_bytes() for path in directory.iterdir()}
        report = driver.inspect_batch(directory)
        self.assertEqual(before, {path.name: path.read_bytes() for path in directory.iterdir()})
        self.assertEqual(('INSPECTION_ONLY', 'DAMAGED', 'RECOVERABLE', '2', 'ABSENT'),
                         (report['status'], report['slots']['0'], report['recovery']['status'],
                          report['recovery']['generation'], report['certificate']))
        self.assertTrue(report['recovery']['warnings'])
        json.dumps(report)
        (directory/'ckpt.2.json').write_bytes(driver.canonical(self.run))
        refused = driver.inspect_batch(directory)
        self.assertEqual('REFUSED', refused['recovery']['status'])
        self.assertEqual('REFUSED: foreign or cross-version checkpoint record', refused['slots']['2'])
        with self.assertRaises((driver.Refusal, OSError)):
            driver.reference_replay(directory)
        cold = self.prepare('cold')
        digest = driver.run_batch(cold, self.run, True)['digest']
        before = {path.name: path.read_bytes() for path in cold.iterdir()}
        replayed = driver.reference_replay(cold)
        self.assertEqual(('REFERENCE_REPLAY_MATCH', digest), (replayed['status'], replayed['digest']))
        self.assertEqual(before, {path.name: path.read_bytes() for path in cold.iterdir()})
        certificate = driver.load_record(cold/'certificate.json', 'certificate')
        certificate['explicit_t_steps'] = str(int(certificate['explicit_t_steps']) + 1)
        (cold/'certificate.json').write_bytes(driver.canonical(driver.seal(certificate, 'CERTIFICATE')))
        with self.assertRaises(driver.Refusal):
            driver.reference_replay(cold)


if __name__ == '__main__':
    unittest.main()
