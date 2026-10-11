"""Harness refusal/identity tests; never alter the Windows firewall."""
import contextlib
import importlib.util
import io
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("offline_acceptance", ROOT/"tools/l1/offline_acceptance.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class HarnessTests(unittest.TestCase):
    def test_source_change_changes_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"src").mkdir()
            path = root/"src/frontier_main.c"
            path.write_bytes(b"first")
            before = helper.source_identity(root)
            path.write_bytes(b"second")
            self.assertNotEqual(before, helper.source_identity(root))

    def test_sources_required(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                helper.source_identity(Path(directory))

    def test_logs_cannot_escape_local_root(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                helper.checked_directory(Path(directory))

    def test_wrong_source_refuses_before_command(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.object(helper, "checked_directory", return_value=Path(directory)), \
                 mock.patch.object(helper, "source_identity", return_value="a"*64), \
                 mock.patch.object(helper.subprocess, "run") as execute:
                with self.assertRaises(ValueError):
                    helper.run_checks(directory, "b"*64)
                execute.assert_not_called()

    def suite_result(self, source):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path/"test_fixture.py").write_text(source, encoding="ascii")
            sys.modules.pop("test_fixture", None)
            loader = unittest.TestLoader()
            suite = loader.discover(str(path))
            with mock.patch.object(helper.unittest.defaultTestLoader, "discover", return_value=suite), \
                 contextlib.redirect_stderr(io.StringIO()):
                result = helper.run_suite(path)
            sys.modules.pop("test_fixture", None)
            return result

    def test_skip_fails_acceptance(self):
        result = self.suite_result('import unittest\nclass T(unittest.TestCase):\n @unittest.skip("missing")\n def test_a(self): pass\n')
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["skips"], 1)

    def test_zero_tests_fails_acceptance(self):
        self.assertEqual(self.suite_result('import unittest\n')["status"], "FAIL")

    def test_passing_test_is_counted(self):
        result = self.suite_result('import unittest\nclass T(unittest.TestCase):\n def test_a(self): self.assertEqual(2+2,4)\n')
        self.assertEqual((result["status"], result["tests"]), ("PASS", 1))

    def test_failed_command_retains_failure_and_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            with mock.patch.object(helper, "checked_directory", return_value=path), \
                 mock.patch.object(helper, "source_identity", return_value="a"*64), \
                 mock.patch.object(helper.subprocess, "run", return_value=mock.Mock(returncode=2)) as execute:
                with self.assertRaises(RuntimeError):
                    helper.run_checks(path, "a"*64)
            import json
            report = json.loads((path/"checks.json").read_text())
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["commands"]), 1)
            execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
