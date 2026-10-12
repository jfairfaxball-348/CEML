"""Operator orchestration tests using simulated command results, never scientific runs."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location('run_frontier',
    Path(__file__).resolve().parents[2] / 'tools/operator/run_frontier.py')
operator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator)


class SimulatedCLI:
    def __init__(self, fail=None, mismatch=False):
        self.end = '2392518188130438758000'
        self.digest = operator.PILOT3
        self.number = 3
        self.start = None
        self.next_end = None
        self.calls = []
        self.fail = fail
        self.mismatch = mismatch

    def run(self, argv, **kwargs):
        self.assert_python(argv)
        name = argv[2]
        self.calls.append(name)
        options = dict(zip(argv[3::2], argv[4::2]))
        if name == self.fail:
            result = dict(status='INCOMPLETE', pending=dict(n=self.end, reason='step_budget'))
        elif name == 'ledger':
            result = dict(status='conditional_chain', batches=str(self.number), start=operator.BASE,
                          end=self.end, genesis_digest=operator.GENESIS, latest_certificate_digest=self.digest)
        elif name == 'prepare-authority':
            result = dict(status='AUTHORITY_RECORDED_NOT_EXECUTED')
        elif name == 'prepare-manifest':
            self.start = self.end
            self.next_end = str(int(self.end) + int(options['--width']))
            result = dict(status='MANIFEST_WRITTEN_NOT_EXECUTED', batch_start=self.start,
                          batch_end=self.next_end, predecessor_digest=self.digest)
        elif name == 'pilot':
            self.number += 1
            self.end = self.next_end
            self.digest = f'{self.number:064x}'
            result = dict(status='COMMITTED', digest=self.digest, batch_end=self.end)
        elif name in ('verify-batch', 'replay'):
            result = dict(status='conditional_complete' if name == 'verify-batch' else 'REFERENCE_REPLAY_MATCH',
                          digest='0' * 64 if self.mismatch and name == 'replay' else self.digest,
                          batch_start=self.start, batch_end=self.end)
        elif name == 'inspect':
            result = dict(status='INSPECTION_ONLY', recovery=dict(status='RECOVERABLE', pending=None,
                          warnings=[]), temporaries='0')
        else:
            raise AssertionError('Unexpected command: ' + name)
        return subprocess.CompletedProcess(argv, 0, json.dumps(result), '')

    @staticmethod
    def assert_python(argv):
        assert argv[1] == operator.DRIVER


class OperatorTests(unittest.TestCase):
    def args(self, count=100000):
        return SimpleNamespace(count=count, batch_width=14400, acknowledge=operator.ACK,
                               expected_latest=operator.PILOT3)

    def test_100k_exact_contiguous_seven_batch_plan(self):
        start = 2392518188130438758000
        plan = operator.batch_plan(start, 100000, 3, 14400)
        self.assertEqual([p['width'] for p in plan], [14400] * 6 + [13600])
        self.assertEqual([p['number'] for p in plan], list(range(4, 11)))
        self.assertEqual(plan[-1]['end'], 2392518188130438858000)
        self.assertTrue(all(a['end'] == b['start'] for a, b in zip(plan, plan[1:])))

    def test_resource_bounds_refuse(self):
        for count, existing, width in [(0, 3, 14400), (100001, 3, 14400), (100000, 250, 14400),
                                       (1, 256, 1), (1, 3, 14401), (1, 3, 0)]:
            with self.subTest(count=count, existing=existing, width=width):
                with self.assertRaises(operator.StopRun):
                    operator.batch_plan(100, count, existing, width)

    def execute_simulation(self, simulation, count=100000):
        args = self.args(count)
        ledger = dict(end=simulation.end, batches='3', latest_certificate_digest=operator.PILOT3)
        plan = operator.batch_plan(int(simulation.end), count, 3, 14400)
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(operator, 'ROOT', Path(directory)), \
                 patch.object(operator.subprocess, 'run', side_effect=simulation.run), redirect_stdout(output):
                operator.execute(args, ledger, plan)
        return output.getvalue()

    def test_success_requires_all_checks_between_batches(self):
        simulation = SimulatedCLI()
        output = self.execute_simulation(simulation)
        self.assertIn('CONDITIONAL_RUN_COMPLETE', output)
        self.assertEqual(simulation.number, 10)
        self.assertEqual(simulation.end, '2392518188130438858000')
        expected = ['ledger', 'prepare-authority', 'prepare-manifest', 'pilot',
                    'verify-batch', 'replay', 'ledger', 'inspect']
        self.assertEqual(simulation.calls, expected * 7)

    def test_incomplete_stops_before_any_successor(self):
        simulation = SimulatedCLI(fail='pilot')
        with self.assertRaisesRegex(operator.StopRun, 'INCOMPLETE'):
            self.execute_simulation(simulation)
        self.assertEqual(simulation.calls.count('prepare-authority'), 1)
        self.assertNotIn('verify-batch', simulation.calls)
        self.assertEqual(simulation.number, 3)

    def test_post_commit_replay_mismatch_stops_before_successor(self):
        simulation = SimulatedCLI(mismatch=True)
        with self.assertRaisesRegex(operator.StopRun, 'verification disagrees'):
            self.execute_simulation(simulation)
        self.assertEqual(simulation.calls.count('prepare-authority'), 1)
        self.assertEqual(simulation.number, 4)

    def preflight_fixture(self, root, args, latest=operator.PILOT3):
        chain = root / operator.CHAIN
        for i in range(1, 4):
            (chain / f'batch-{i:04d}').mkdir(parents=True)
        ledger = dict(start=operator.BASE, end='2392518188130438758000', batches='3',
                      genesis_digest=operator.GENESIS, latest_certificate_digest=latest)

        def driver(name, *arguments, status):
            if name == 'rules':
                return dict(table_digest=operator.TABLE)
            if name == 'snapshot':
                return dict(digest=operator.SNAPSHOT, operational=dict(B=operator.BASE))
            if name == 'ledger':
                return ledger
            if name == 'verify-batch':
                return dict(digest=latest, batch_end=ledger['end'])
            raise AssertionError('Preflight must not execute: ' + name)

        return driver

    def check_preflight(self, root, args, driver):
        build = dict(digest=operator.BUILD, executable_sha3_256=operator.WORKER, table_digest=operator.TABLE)
        with patch.object(operator, 'ROOT', root), patch.object(operator, 'driver', side_effect=driver), \
             patch.object(operator, 'command', return_value=build), \
             patch.object(operator.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')):
            return operator.preflight(args)

    def test_stale_external_digest_refuses_before_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            driver = self.preflight_fixture(root, self.args(), latest='0' * 64)
            before = sorted(str(p.relative_to(root)) for p in root.rglob('*'))
            with self.assertRaisesRegex(operator.StopRun, 'expected certificate'):
                self.check_preflight(root, self.args(), driver)
            self.assertEqual(before, sorted(str(p.relative_to(root)) for p in root.rglob('*')))

    def test_uncommitted_directory_refuses_without_edit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            driver = self.preflight_fixture(root, self.args())
            (root / operator.CHAIN / 'batch-0004').mkdir()
            with self.assertRaisesRegex(operator.StopRun, 'Uncommitted'):
                self.check_preflight(root, self.args(), driver)
            self.assertTrue((root / operator.CHAIN / 'batch-0004').exists())

    def test_existing_manifest_refuses_without_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            driver = self.preflight_fixture(root, self.args())
            manifests = root / operator.MANIFESTS
            manifests.mkdir()
            manifest = manifests / 'batch-0004.json'
            manifest.write_text('preserve this abandoned preparation')
            with self.assertRaisesRegex(operator.StopRun, 'already exists'):
                self.check_preflight(root, self.args(), driver)
            self.assertEqual(manifest.read_text(), 'preserve this abandoned preparation')

    def test_wrong_acknowledgement_refuses_without_command(self):
        args = self.args()
        args.acknowledge = 'incorrect'
        with patch.object(operator.subprocess, 'run') as run:
            with self.assertRaisesRegex(operator.StopRun, 'Acknowledgement'):
                operator.preflight(args)
            run.assert_not_called()

    def test_concurrent_operator_invocation_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'local/frontier').mkdir(parents=True)
            with patch.object(operator, 'ROOT', root):
                with operator.operator_lock():
                    with self.assertRaisesRegex(operator.StopRun, 'Another operator'):
                        with operator.operator_lock():
                            self.fail('second invocation acquired the lock')


if __name__ == '__main__':
    unittest.main()
