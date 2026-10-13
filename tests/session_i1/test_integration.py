"""Integration tests for I1 selection and existing operator controls, no science."""
from contextlib import redirect_stdout, redirect_stderr
import importlib.util
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch, MagicMock

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/session_i1'))
import identity
from client import Client
spec=importlib.util.spec_from_file_location('operator_i1',ROOT/'tools/operator/run_frontier.py')
operator=importlib.util.module_from_spec(spec);spec.loader.exec_module(operator)

class Integration(unittest.TestCase):
    def test_default_and_stale_acceptance(self):
        with patch('identity.accepted',return_value=False):
            with operator.verification_session():self.assertIsNone(operator.SESSION_CLIENT)
        with patch('identity.accepted',side_effect=ValueError('stale')):
            with self.assertRaisesRegex(ValueError,'stale'):
                with operator.verification_session():self.fail('unsafe fallback')

    def test_selected_session_closes_and_routes(self):
        client=MagicMock();client.__enter__.return_value=client
        client.call.return_value={'status':'conditional_chain'}
        with patch('identity.accepted',return_value=True),patch('client.Client',return_value=client),redirect_stdout(io.StringIO()):
            with operator.verification_session():
                self.assertIs(operator.SESSION_CLIENT,client)
                operator.driver('ledger','--dir',operator.CHAIN,status='conditional_chain')
                client.call.assert_called_once()
                with patch.object(operator,'command',return_value={}) as original:
                    operator.driver('rules',status='rules_pass');original.assert_called_once()
        self.assertIsNone(operator.SESSION_CLIENT);client.__exit__.assert_called_once()

    def test_bad_worker_result_stops_operator(self):
        client=SimpleNamespace(call=lambda _:dict(status='SESSION_REFUSED',reason='tamper'))
        with patch.object(operator,'SESSION_CLIENT',client):
            with self.assertRaisesRegex(operator.StopRun,'SESSION_REFUSED'):
                operator.driver('ledger',status='conditional_chain')

    def test_acceptance_is_separate_and_quantity_free(self):
        self.assertEqual(operator.parse_arguments(['accept-incremental']).mode,'accept')
        self.assertEqual(operator.parse_arguments(['start']).mode,'continuous')
        self.assertEqual(operator.parse_arguments(['stop']).mode,'stop')
        self.assertEqual(operator.parse_arguments(['100']).count,100)
        with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):operator.parse_arguments(['accept-incremental','100'])

    def test_real_pipe_worker_refuses_without_owner_acceptance(self):
        if identity.ACCEPTANCE.exists():self.skipTest('owner has independently accepted')
        with self.assertRaisesRegex(ValueError,'SESSION_REFUSED'):
            Client(ROOT/operator.CHAIN)

if __name__=='__main__':unittest.main()
