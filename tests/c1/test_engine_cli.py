"""Bounded developer tests of the production executable's command gates; not V1.

Skipped when the pinned offline engine build is absent (for example in a fresh
clone before `python tools/c1/engine_build.py`)."""
import json
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENGINE = ROOT / 'local/c1/engine/bin/ceml.exe'


def run(*arguments, cwd=ROOT, stdin=b''):
    process = subprocess.run([str(ENGINE), *arguments], cwd=cwd, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=120)
    return process.returncode, json.loads(process.stdout.splitlines()[0])


@unittest.skipUnless(ENGINE.is_file(), 'pinned engine build not present')
class EngineCommandTests(unittest.TestCase):
    def test_scientific_and_validation_commands_are_gated(self):
        for arguments, reason in ((('validate',), 'V1-not-authorized-by-PROGRAM_STATUS'),
                                  (('prepare', 'manifest.json'), 'E1-not-authorized-by-PROGRAM_STATUS'),
                                  (('run', 'manifest.json', 'checkpoints'), 'E1-not-authorized-by-PROGRAM_STATUS')):
            code, output = run(*arguments)
            self.assertEqual(code, 3)
            self.assertEqual(output['status'], 'refused')
            self.assertEqual(output['reason'], reason)

    def test_gates_fail_closed_without_a_readable_status(self):
        with tempfile.TemporaryDirectory() as empty:
            for arguments in (('validate',), ('run', 'm', 'd'), ('prepare', 'm')):
                self.assertEqual(run(*arguments, cwd=empty)[0], 3)

    def test_status_reports_c1_and_changes_nothing(self):
        code, output = run('status')
        self.assertEqual((code, output['phase'], output['validate_enabled'], output['scientific_run_enabled']),
                         (0, 'C1', False, False))

    def test_checkpoint_refuses_identities_not_marked_nonscientific(self):
        lines = ['somewhere', 'ladder-rung-0'] + ['a'*64, 'a'*64, 'a'*40, 'a'*40, 'a'*64, 'a'*64, 'a'*64, '1b', '0', '0']
        code, output = run('checkpoint', 'buffered', stdin=''.join(x + '\n' for x in lines).encode())
        self.assertEqual((code, output['status']), (3, 'refused'))

    def test_calibration_entry_refuses_out_of_bound_work(self):
        operand = (format((1 << 1023) | 1, 'x') + '\n').encode()
        for arguments in (('route', 'direct', '1', '1', '1', '4097', 'reuse', 'divisibility', 'fixed'),
                          ('route', 'hier', '1', '2', '32768', '2016', 'reuse', 'divisibility', 'fixed'),
                          ('route', 'small', '20', '1', '1', '2016', 'reuse', 'divisibility', 'fixed')):
            process = subprocess.run([str(ENGINE), '--calibration-only', *arguments], input=operand, stdout=subprocess.PIPE)
            self.assertEqual(process.returncode, 2)

    def test_bounded_self_test_passes(self):
        with tempfile.TemporaryDirectory() as scratch:
            code, output = run('self-test', 'self-test.tmp', cwd=scratch)
        self.assertEqual((code, output['status'], len(output['classes'])), (0, 'PASS', 12))
        self.assertTrue(all(c['failures'] == '0' and int(c['cases']) > 0 for c in output['classes'].values()))


if __name__ == '__main__':
    unittest.main()
