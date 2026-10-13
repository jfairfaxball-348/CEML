"""I2 boundary/adversarial tests. No scientific batches or owner acceptance."""
from contextlib import redirect_stdout
import importlib.util
import io
import itertools
import json
from pathlib import Path
import sys
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.session_i2 import identity
from tools.session_i2.session import Session
from tools.session_i2.pinned import IntegrityError
from tools.session_i2.client import Client
from tools.session_i2.audit import audit

spec = importlib.util.spec_from_file_location('continuous_operator', ROOT/'tools/operator/run_frontier.py')
operator = importlib.util.module_from_spec(spec); spec.loader.exec_module(operator)


class Continuous(unittest.TestCase):
    def test_lazy_plan_crosses_256_and_9999_without_gap(self):
        for existing in (256, 9999, 1000000):
            plan = operator.continuous_batches(12345, existing)
            self.assertFalse(isinstance(plan, list))
            first, second = list(itertools.islice(plan, 2))
            self.assertEqual(first, dict(number=existing+1, start=12345, end=22344, width=9999))
            self.assertEqual(second['start'], first['end'])
            self.assertEqual(second['number'], first['number']+1)

    def test_finite_extension_requires_explicit_profile(self):
        with self.assertRaises(operator.StopRun): operator.batch_plan(100, 10, 256, 10)
        self.assertEqual(operator.batch_plan(100, 15, 256, 10, unlimited=True)[-1]['end'], 115)

    def test_acceptance_has_no_quantity(self):
        self.assertEqual(operator.parse_arguments(['accept-continuous']).mode, 'accept')
        with patch('sys.stderr', io.StringIO()):
            with self.assertRaises(SystemExit): operator.parse_arguments(['accept-continuous', '1'])

    def test_i2_precedes_stale_i1_and_always_closes(self):
        client = MagicMock(); client.profile=identity.PROFILE; client.__enter__.return_value=client
        with tempfile.TemporaryDirectory() as folder:
            acceptance=Path(folder)/'acceptance'; acceptance.write_text('{}')
            with patch.object(identity,'ACCEPTANCE',acceptance),patch.object(identity,'accepted',return_value=True),patch('tools.session_i2.client.Client',return_value=client),redirect_stdout(io.StringIO()):
                with operator.verification_session(): self.assertTrue(operator.continuous_profile())
            client.__exit__.assert_called_once()
            self.assertIsNone(operator.SESSION_CLIENT)

    def test_stale_i2_never_falls_back(self):
        with tempfile.TemporaryDirectory() as folder:
            acceptance=Path(folder)/'acceptance'; acceptance.write_text('{}')
            with patch.object(identity,'ACCEPTANCE',acceptance):
                with self.assertRaises(ValueError):
                    with operator.verification_session(): self.fail('unsafe fallback')

    def test_prefix_anchor_cannot_be_replaced_by_a_count(self):
        session=Session.__new__(Session)
        session._certificates=[{}]*256
        for final in ({'digest':'0'*64,'batch_end':identity.PREFIX_END},
                      {'digest':identity.PREFIX_DIGEST,'batch_end':'3'}):
            session._certificates[-1]=final
            with self.assertRaises(IntegrityError): session.check_extension_anchor()
        session._certificates[-1]={'digest':identity.PREFIX_DIGEST,'batch_end':identity.PREFIX_END}
        session.check_extension_anchor()
        session._certificates.pop()
        with self.assertRaises(IntegrityError): session.check_extension_anchor()

    def test_new_slot_requires_exact_next_number_and_tip(self):
        session=Session.__new__(Session); session.chain=ROOT/'local/frontier/slot-fixture'
        session._certificates=[{}]*256;session.test=False
        session.guard=MagicMock();session.predecessor=MagicMock()
        session.ensure_chain_slot(session.chain/'batch-0257',{})
        for directory in (session.chain/'batch-0258', session.chain.parent/'batch-0257'):
            with self.assertRaises(IntegrityError):session.ensure_chain_slot(directory,{})
        session.predecessor.side_effect=IntegrityError('bad tip')
        with self.assertRaises(IntegrityError):session.ensure_chain_slot(session.chain/'batch-0257',{})

    def test_long_anchor_requires_verified_evidence(self):
        anchor=dict(batches='10000',end='10001',genesis_digest=operator.GENESIS,latest_certificate_digest='a'*64)
        ledger=dict(batches='10001',end='10002')
        with self.assertRaises(operator.StopRun):operator.check_anchor(anchor,ledger)
        with patch.object(operator,'driver') as driver:
            operator.check_anchor(anchor,ledger,{'10000':dict(digest='a'*64,batch_end='10001')})
            driver.assert_not_called()
        for evidence in ({},{'10000':dict(digest='b'*64,batch_end='10001')}):
            with self.assertRaises(operator.StopRun):operator.check_anchor(anchor,ledger,evidence)

    def test_unaccepted_pipe_worker_refuses_before_any_write(self):
        self.assertFalse(identity.ACCEPTANCE.exists())
        with self.assertRaisesRegex(ValueError,'SESSION_REFUSED'):Client(ROOT/operator.CHAIN)

    def test_orphan_manifest_blocks_even_without_an_unfinished_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);manifests=root/'manifests';manifests.mkdir()
            session=Session.__new__(Session);session.closed=False;session.chain=root/'chain';session.chain.mkdir()
            session._layout={};session.active=None;session.manifest_dir=manifests;session._manifest_names=set()
            session.guard()
            (manifests/'batch-0258.json').write_text('{}')
            with self.assertRaisesRegex(IntegrityError,'manifest'):session.guard()

    def test_readonly_plan_previews_one_admission_above_256(self):
        # Reuse the complete preflight simulation with no actual native work.
        sys.path.insert(0,str(ROOT/'tests/operator'))
        from test_run_frontier import OperatorTests
        helper=OperatorTests();args=operator.parse_arguments(['start','--plan'])
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);driver=helper.preflight_fixture(root,args)
            ledger=driver('ledger',status='conditional_chain');ledger['batches']='256'
            for number in range(4,257):(root/operator.CHAIN/f'batch-{number:04d}').mkdir()
            build=dict(digest=operator.BUILD,executable_sha3_256=operator.WORKER,table_digest=operator.TABLE)
            with patch.object(operator,'ROOT',root),patch.object(operator,'continuous_profile',return_value=True),patch.object(operator,'driver',side_effect=driver),patch.object(operator,'command',return_value=build),patch.object(operator.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'','')):
                checked,plan=operator.preflight(args)
            self.assertEqual(len(plan),1)
            self.assertEqual(plan[0]['number'],257)
            self.assertEqual(plan[0]['start'],int(checked['end']))

    def test_clean_stop_after_257_preserves_all_checks(self):
        # Simulated scientific responses only; no driver/native execution.
        sys.path.insert(0,str(ROOT/'tests/operator'))
        from test_run_frontier import SimulatedCLI
        args=operator.parse_arguments(['start']);sim=SimulatedCLI();sim.number=256
        sim.digest=identity.PREFIX_DIGEST
        ledger=dict(end=sim.end,batches='256',latest_certificate_digest=sim.digest,genesis_digest=operator.GENESIS)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'local/frontier').mkdir(parents=True)
            def response(argv,**kwargs):
                if argv[2]=='pilot':operator.request_stop()
                return sim.run(argv,**kwargs)
            with patch.object(operator,'ROOT',root),patch.object(operator,'continuous_profile',return_value=True),patch.object(operator.subprocess,'run',side_effect=response),redirect_stdout(io.StringIO()),operator.managed_run(args):
                result=operator.execute(args,ledger,operator.continuous_batches(int(sim.end),256))
                receipt=json.loads((root/operator.TIP).read_text())
        self.assertEqual(result['status'],'CLEAN_STOPPED')
        self.assertEqual(result['added_count'],'9999')
        self.assertEqual(receipt['batches'],'257')
        self.assertEqual(sim.calls,['ledger','prepare-authority','prepare-manifest','pilot','verify-batch','replay','ledger','inspect'])


if __name__=='__main__':unittest.main()
