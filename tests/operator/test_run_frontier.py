"""Operator orchestration tests using simulated command results, never scientific runs."""

from contextlib import redirect_stdout, nullcontext
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import sys
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
    def test_continuous_commands_need_no_quantity_and_use_9999(self):
        start=operator.parse_arguments(['start'])
        self.assertEqual((start.mode,start.count,start.batch_width),('continuous',None,9999))
        self.assertEqual(operator.parse_arguments(['stop']).mode,'stop')
        self.assertEqual(operator.parse_arguments(['100000']).batch_width,9999)

    def test_continuous_preflight_stays_inside_accepted_chain_limit(self):
        args=operator.parse_arguments(['start'])
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); driver=self.preflight_fixture(root,args)
            ledger,plan=self.check_preflight(root,args,driver)
        self.assertEqual(plan[0]['start'],int(ledger['end']))
        self.assertEqual(plan[-1]['number'],256)
        self.assertTrue(all(b['width']==9999 for b in plan))

    def managed_simulation(self, request_at=None, fail=None, local_signal=False):
        args=operator.parse_arguments(['start'])
        simulation=SimulatedCLI(fail=fail)
        ledger=dict(end=simulation.end,batches='3',latest_certificate_digest=operator.PILOT3,genesis_digest=operator.GENESIS)
        plan=operator.batch_plan(int(simulation.end),9999*2,3,9999)
        output=io.StringIO()
        request_results=[]
        def simulated(argv,**kwargs):
            if argv[2]==request_at:
                if local_signal:
                    operator.signal.getsignal(operator.signal.SIGINT)(operator.signal.SIGINT,None)
                else:
                    request_results.append(operator.request_stop()['status'])
            return simulation.run(argv,**kwargs)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'local/frontier').mkdir(parents=True)
            with patch.object(operator,'ROOT',root),redirect_stdout(output),operator.managed_run(args):
                operator.remember_tip({**ledger,'genesis_digest':operator.GENESIS})
                if request_at=='before':request_results.append(operator.request_stop()['status'])
                with patch.object(operator.subprocess,'run',side_effect=simulated):
                    summary=operator.execute(args,ledger,plan)
                receipt=json.loads((root/operator.TIP).read_text())
            self.assertFalse(json.loads((root/operator.CONTROL).read_text())['active'])
        return simulation,summary,receipt,request_results,output.getvalue()

    def test_stop_before_admission_creates_no_batch(self):
        for stage in ('before','ledger'):
            with self.subTest(stage=stage):
                sim,summary,receipt,requests,_=self.managed_simulation(stage)
                self.assertEqual(summary['status'],'CLEAN_STOPPED')
                self.assertEqual(summary['added_count'],'0')
                self.assertNotIn('prepare-authority',sim.calls)
                self.assertEqual(receipt['batches'],'3')
                self.assertIn('STOP_REQUESTED',requests)

    def test_stop_during_batch_finishes_all_checks_and_saves_receipt(self):
        for stage in ('prepare-authority','prepare-manifest','pilot','verify-batch','replay','inspect'):
            with self.subTest(stage=stage):
                sim,summary,receipt,requests,_=self.managed_simulation(stage)
                self.assertEqual(summary['status'],'CLEAN_STOPPED')
                self.assertEqual(summary['added_count'],'9999')
                self.assertEqual(sim.calls,['ledger','prepare-authority','prepare-manifest','pilot','verify-batch','replay','ledger','inspect'])
                self.assertEqual(receipt['latest_certificate_digest'],sim.digest)
                self.assertEqual(receipt['batches'],'4')
                self.assertEqual(requests,['STOP_REQUESTED'])

    def test_local_ctrl_c_requests_clean_stop_without_interrupting_checks(self):
        sim,summary,receipt,_,_=self.managed_simulation('pilot',local_signal=True)
        self.assertEqual(summary['status'],'CLEAN_STOPPED')
        self.assertEqual(sim.number,4)
        self.assertEqual(receipt['batches'],'4')

    def test_clean_stop_does_not_hide_incomplete_batch(self):
        with self.assertRaisesRegex(operator.StopRun,'INCOMPLETE'):
            self.managed_simulation('pilot',fail='pilot')

    def test_readiness_is_reported_after_releasing_operator_lock(self):
        args=operator.parse_arguments(['start'])
        sim=SimulatedCLI()
        ledger=dict(end=sim.end,batches='3',latest_certificate_digest=operator.PILOT3,genesis_digest=operator.GENESIS)
        observed=[]
        def summary(value):
            observed.append((value['status'],operator.operator_running()))
        def execute(args,ledger,plan):
            args.session_outcome='CLEAN_STOPPED'
            return dict(status='CLEAN_STOPPED')
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'local/frontier').mkdir(parents=True)
            with patch.object(operator,'ROOT',root),patch.object(operator,'verification_session',return_value=nullcontext()),patch.object(operator,'parse_arguments',return_value=args),patch.object(operator,'preflight',return_value=(ledger,[])),patch.object(operator,'execute',side_effect=execute),patch.object(operator,'print_summary',side_effect=summary):
                self.assertEqual(operator.main(),0)
        self.assertEqual(observed,[('CLEAN_STOPPED',False)])

    def test_last_accepted_batch_stops_at_256(self):
        args=operator.parse_arguments(['start'])
        sim=SimulatedCLI();sim.number=255;sim.digest='f'*64
        ledger=dict(end=sim.end,batches='255',latest_certificate_digest=sim.digest)
        plan=operator.batch_plan(int(sim.end),9999,255,9999)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'local/frontier').mkdir(parents=True)
            with patch.object(operator,'ROOT',root),patch.object(operator.subprocess,'run',side_effect=sim.run),redirect_stdout(io.StringIO()):
                summary=operator.execute(args,ledger,plan)
        self.assertEqual(summary['status'],'CHAIN_LIMIT_REACHED')
        self.assertEqual(sim.number,256)
        self.assertEqual(sim.calls.count('prepare-authority'),1)

    def test_stop_command_works_across_processes_without_running_driver(self):
        args=operator.parse_arguments(['start'])
        source=Path(operator.__file__).resolve()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'local/frontier').mkdir(parents=True)
            script="import importlib.util,json; from pathlib import Path; s=importlib.util.spec_from_file_location('op',"+repr(str(source))+"); m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.ROOT=Path("+repr(str(root))+"); print(json.dumps(m.request_stop()))"
            with patch.object(operator,'ROOT',root),operator.managed_run(args):
                result=subprocess.run([sys.executable,'-c',script],capture_output=True,text=True,timeout=15)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'],'STOP_REQUESTED')
                self.assertTrue(operator.stop_requested(args))
            with patch.object(operator,'ROOT',root):
                self.assertEqual(operator.request_stop()['status'],'NO_ACTIVE_RUN')

    def test_old_stop_request_does_not_stop_the_next_session(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'local/frontier').mkdir(parents=True)
            with patch.object(operator,'ROOT',root):
                first=operator.parse_arguments(['start'])
                with operator.managed_run(first):
                    operator.request_stop()
                    self.assertTrue(operator.stop_requested(first))
                second=operator.parse_arguments(['start'])
                with operator.managed_run(second):
                    self.assertNotEqual(first.session_token,second.session_token)
                    self.assertFalse(operator.stop_requested(second))

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
        for count, existing, width in [(0, 3, 14400), (3643201, 3, 14400), (100000, 250, 14400),
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
            (Path(directory) / 'local/frontier').mkdir(parents=True)
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
        (root / 'docs').mkdir()
        (root / 'docs/RUN1_PROGRESS.md').write_text(
            f"Batches: 3\nVerified conditional on that assumption: every integer in [{operator.BASE},{ledger['end']}) converges\n"
            f"Latest certificate digest: {latest}\nGenesis digest: {operator.GENESIS}\n", encoding='utf-8')

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

    def test_quantity_only_command_and_legacy_options(self):
        args = operator.parse_arguments(['1440'])
        self.assertEqual(args.count, 1440)
        self.assertIsNone(args.acknowledge)
        self.assertIsNone(args.expected_latest)
        self.assertEqual(operator.parse_arguments(['check-next', '1440']).count, 1440)
        legacy = operator.parse_arguments(['--count', '1440', '--acknowledge', operator.ACK])
        self.assertEqual(legacy.count, 1440)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(operator.batch_plan(100, 100001, 3, 14400)[-1]['end'], 100101)

    def test_dynamic_tip_continues_above_current_committed_end(self):
        args = operator.parse_arguments(['check-next', '1440'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            driver = self.preflight_fixture(root, args, latest='a' * 64)
            ledger, plan = self.check_preflight(root, args, driver)
            self.assertEqual(plan[0]['start'], int(ledger['end']))
            self.assertEqual(plan[-1]['end'] - plan[0]['start'], 1440)
            self.assertEqual(args.acknowledge, operator.ACK)
            self.assertFalse((root / operator.TIP).exists())

    def test_retained_tip_detects_shortened_chain(self):
        args = operator.parse_arguments(['check-next', '1440'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            driver = self.preflight_fixture(root, args)
            receipt = dict(batches='4', end='2392518188130438772400',
                           latest_certificate_digest='b' * 64, genesis_digest=operator.GENESIS)
            (root / operator.TIP).write_text(json.dumps(receipt), encoding='ascii')
            with self.assertRaisesRegex(operator.StopRun, 'rolled back'):
                self.check_preflight(root, args, driver)

    def test_advanced_chain_accepts_older_published_and_local_anchors(self):
        args = operator.parse_arguments(['1000'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = self.preflight_fixture(root, args)
            for number in (4, 5):
                (root / operator.CHAIN / f'batch-{number:04d}').mkdir()
            tip = dict(batches='4', end='2392518188130438772400',
                       latest_certificate_digest='4' * 64, genesis_digest=operator.GENESIS)
            (root / operator.TIP).write_text(json.dumps(tip), encoding='ascii')
            ledger = dict(batches='5', end='2392518188130438786800', start=operator.BASE,
                          latest_certificate_digest='5' * 64, genesis_digest=operator.GENESIS)

            def driver(name, *arguments, status):
                if name == 'ledger':
                    return ledger
                if name == 'verify-batch' and 'batch-0004' in str(arguments[-1]):
                    return dict(digest=tip['latest_certificate_digest'], batch_end=tip['end'])
                if name == 'verify-batch' and 'batch-0005' in str(arguments[-1]):
                    return dict(digest=ledger['latest_certificate_digest'], batch_end=ledger['end'])
                return original(name, *arguments, status=status)

            actual, plan = self.check_preflight(root, args, driver)
            self.assertEqual(actual['batches'], '5')
            self.assertEqual(plan[0]['number'], 6)
            self.assertEqual(plan[0]['start'], int(ledger['end']))

    def test_atomic_receipt_matches_verified_ledger(self):
        simulation = SimulatedCLI()
        ledger = dict(batches='10', end=simulation.end,
                      latest_certificate_digest=simulation.digest, genesis_digest=operator.GENESIS)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'local/frontier').mkdir(parents=True)
            with patch.object(operator, 'ROOT', root):
                operator.remember_tip(ledger)
            self.assertEqual(json.loads((root / operator.TIP).read_text()), ledger)
            self.assertEqual(list((root / 'local/frontier').glob('operator-tip-*.tmp')), [])

    def test_receipt_replace_failure_preserves_previous_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'local/frontier').mkdir(parents=True)
            old = dict(batches='3', end='2392518188130438758000',
                       latest_certificate_digest=operator.PILOT3, genesis_digest=operator.GENESIS)
            (root / operator.TIP).write_text(json.dumps(old), encoding='ascii')
            new = dict(old, batches='4', end='2392518188130438772400', latest_certificate_digest='4' * 64)
            with patch.object(operator, 'ROOT', root), patch.object(operator.os, 'replace', side_effect=OSError('locked')):
                with self.assertRaises(OSError):
                    operator.remember_tip(new)
            self.assertEqual(json.loads((root / operator.TIP).read_text()), old)

    def test_ambiguous_published_anchor_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.preflight_fixture(root, self.args())
            path = root / 'docs/RUN1_PROGRESS.md'
            path.write_text(path.read_text() + '\nBatches: 4\n')
            with patch.object(operator, 'ROOT', root):
                with self.assertRaisesRegex(operator.StopRun, 'ambiguous'):
                    operator.published_anchor()

    def test_malformed_local_receipt_refuses_clearly(self):
        for value in (None, [], 12, 'not a receipt', {'batches': 3}):
            with self.subTest(value=value):
                with self.assertRaisesRegex(operator.StopRun, 'shape mismatch'):
                    operator.check_anchor(value, {'batches': '10'})

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
