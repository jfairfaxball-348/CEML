"""Harness refusal/identity tests; never alter the Windows firewall."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT/"tools/l1/run_offline_acceptance.ps1"
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

    def test_identity_ignores_only_line_ending_style(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/"src").mkdir()
            path = root/"src/frontier_main.c"
            path.write_bytes(b"int main(void) {\n    return 0;\n}\n")
            unix = helper.source_identity(root)
            path.write_bytes(b"int main(void) {\r\n    return 0;\r\n}\r\n")
            self.assertEqual(unix, helper.source_identity(root))
            path.write_bytes(b"int main(void) {\n    return 1;\n}\n")
            self.assertNotEqual(unix, helper.source_identity(root))

    def test_identity_binds_every_version_2_contract_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = ("docs/FRONTIER_PROTOCOL_V1.md", "docs/FRONTIER_PROTOCOL_V2.md",
                     "config/frontier_snapshot_v1.json", "config/frontier_snapshot_v2.json",
                     "schemas/frontier_checkpoint_v2.schema.json", "tools/l1/run_offline_acceptance.ps1",
                     "tools/l1/offline_acceptance.py", "tests/l1/test_offline_acceptance.py",
                     "tests/frontier/test_recovery.py", "tools/frontier/ceml_frontier.py")
            for name in names:
                (root/name).parent.mkdir(parents=True, exist_ok=True)
                (root/name).write_bytes(b"original")
            for name in names:
                before = helper.source_identity(root)
                (root/name).write_bytes(b"changed")
                with self.subTest(name=name):
                    self.assertNotEqual(before, helper.source_identity(root))
        for name in names:
            self.assertTrue((ROOT/name).is_file(), name)

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

    def test_expected_failure_fails_acceptance(self):
        result = self.suite_result('import unittest\nclass T(unittest.TestCase):\n @unittest.expectedFailure\n def test_a(self): self.fail()\n')
        self.assertEqual(("FAIL", 1), (result["status"], result["expected_failures"]))

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
            report = json.loads((path/"checks.json").read_text())
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(len(report["commands"]), 1)
            execute.assert_called_once()


class PlanTests(unittest.TestCase):
    """The final version-2 command plan and its evidence collection, with commands mocked."""

    SUMMARIES = {
        "build": {"digest": "d"*64}, "clean-reproduction": {"digest": "d"*64},
        "final-clean-reproduction": {"digest": "d"*64}, "snapshot": {"digest": "5"*64},
        "launcher-suite": {"status": "PASS", "tests": 3, "skips": 0},
        "frontier-suite": {"status": "PASS", "tests": 9, "skips": 0},
        "selftest-calibration": {"status": "fixtures_pass", "results": []},
    }

    def test_plan_covers_build_reproduction_both_suites_and_calibration(self):
        plan = dict(helper.commands())
        self.assertEqual(["build-command", "build", "clean-reproduction", "rules", "snapshot",
                          "snapshot-v1-frozen", "launcher-suite", "frontier-suite",
                          "selftest-calibration", "final-clean-reproduction"], list(plan))
        self.assertEqual(["tools/l1/offline_acceptance.py", "--suite", "frontier"], plan["frontier-suite"])
        self.assertEqual(["tools/l1/offline_acceptance.py", "--suite", "l1"], plan["launcher-suite"])
        self.assertEqual("config/frontier_snapshot_v2.json", plan["snapshot"][-1])
        self.assertEqual("config/frontier_snapshot_v1.json", plan["snapshot-v1-frozen"][-1])
        self.assertEqual({"frontier": "tests/frontier", "l1": "tests/l1"}, helper.SUITES)
        for folder in helper.SUITES.values():
            self.assertTrue(list((ROOT/folder).glob("test_*.py")))
        # Every recovery test file is inside the complete frontier suite.
        self.assertTrue((ROOT/"tests/frontier/test_recovery.py").is_file())

    def run_plan(self, summaries, manifest_digest="d"*64):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            def execute(arguments, stdout=None, **kwargs):
                label = Path(stdout.name).stem
                stdout.write(b"noise\n" + json.dumps(summaries.get(label, {"status": "ok"})).encode("ascii") + b"\n")
                return mock.Mock(returncode=0)
            manifest = dict(digest=manifest_digest, table_digest="7"*64, test_suite_revision="8"*64,
                            artifacts={"ceml_frontier.exe": {"sha3_256": "9"*64}})
            real_read = Path.read_bytes
            def read_bytes(target):
                if target.name == "build_manifest.json":
                    return json.dumps(manifest).encode("ascii")
                return real_read(target)
            with mock.patch.object(helper, "checked_directory", return_value=path), \
                 mock.patch.object(helper, "source_identity", return_value="a"*64), \
                 mock.patch.object(helper.subprocess, "run", side_effect=execute), \
                 mock.patch.object(Path, "read_bytes", read_bytes):
                try:
                    helper.run_checks(path, "a"*64)
                except Exception as error:
                    return json.loads(real_read(path/"checks.json")), type(error).__name__
            return json.loads(real_read(path/"checks.json")), None

    def test_passing_plan_records_totals_identities_and_calibration(self):
        report, error = self.run_plan(self.SUMMARIES)
        self.assertIsNone(error)
        self.assertEqual(("ENGINEERING-CHECKS-PASS", "CEML-L1-OFFLINE-CHECKS-2", "CEML-FRONTIER-2", "NOT_RUN"),
                         (report["status"], report["schema"], report["protocol"], report["scientific_execution"]))
        self.assertEqual(10, len(report["commands"]))
        self.assertEqual((9, 0, 3), (report["suites"]["frontier-suite"]["tests"],
                                     report["suites"]["frontier-suite"]["skips"],
                                     report["suites"]["launcher-suite"]["tests"]))
        self.assertEqual(("d"*64, ["d"*64]*3, "5"*64, "9"*64),
                         (report["native_build_digest"], report["build_digests"], report["snapshot_digest"],
                          report["artifact_sha3_256"]["ceml_frontier.exe"]))
        self.assertEqual("fixtures_pass", report["calibration"]["status"])

    def test_skipped_empty_or_failing_suite_and_unstable_build_fail_the_plan(self):
        cases = (("frontier-suite", {"status": "PASS", "tests": 9, "skips": 1}),
                 ("frontier-suite", {"status": "PASS", "tests": 0, "skips": 0}),
                 ("launcher-suite", {"status": "FAIL", "tests": 3, "skips": 0}),
                 ("selftest-calibration", {"status": "REFUSED"}),
                 ("final-clean-reproduction", {"digest": "e"*64}))
        for label, summary in cases:
            report, error = self.run_plan(dict(self.SUMMARIES, **{label: summary}))
            with self.subTest(label=label):
                self.assertIsNotNone(error)
                self.assertEqual("FAIL", report["status"])
                self.assertNotIn("native_build_digest", report)
        report, error = self.run_plan(self.SUMMARIES, manifest_digest="f"*64)
        self.assertEqual(("FAIL", "ValueError"), (report["status"], error))


@unittest.skipUnless(os.name == "nt", "Windows launcher")
class LauncherRefusalTests(unittest.TestCase):
    """Real launcher invocations that must refuse before changing anything.

    Neither call can reach the firewall or scheduler: Preflight is read-only and
    Run stops at the administrator or reviewed-hash check, whichever comes first.
    """

    def launch(self, *arguments):
        shell = Path(os.environ["SystemRoot"])/"System32/WindowsPowerShell/v1.0/powershell.exe"
        return subprocess.run([str(shell), "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                               "-File", str(LAUNCHER), "-PythonPath", sys.executable, *arguments],
                              cwd=ROOT, capture_output=True, timeout=180)

    def evidence(self):
        folder = ROOT/"local/frontier/os-offline"
        return sorted(path.name for path in folder.iterdir()) if folder.is_dir() else []

    def test_preflight_reports_current_identities_and_runs_nothing(self):
        before = self.evidence()
        result = self.launch("-Mode", "Preflight")
        self.assertEqual(0, result.returncode, result.stderr.decode("ascii", "replace"))
        report = json.loads(result.stdout)
        self.assertEqual(("PREPARED-NOT-EXECUTED", "L1-NONSCIENTIFIC", "PASS", "NOT_RUN"),
                         (report["status"], report["scope"], report["firewall_prerequisites"],
                          report["os_isolated_acceptance"]))
        self.assertEqual(helper.source_identity(), report["source_sha256"])
        self.assertEqual(hashlib.sha256(LAUNCHER.read_bytes()).hexdigest(), report["launcher_sha256"])
        self.assertEqual(before, self.evidence())

    def test_run_refuses_without_the_reviewed_hashes_and_leaves_no_evidence(self):
        current = helper.source_identity()
        launcher = hashlib.sha256(LAUNCHER.read_bytes()).hexdigest()
        for arguments in ((), ("-ExpectedSourceSha256", "0"*64, "-ExpectedLauncherSha256", "0"*64),
                          ("-ExpectedSourceSha256", current, "-ExpectedLauncherSha256", "0"*64),
                          ("-ExpectedSourceSha256", "0"*64, "-ExpectedLauncherSha256", launcher)):
            before = self.evidence()
            result = self.launch("-Mode", "Run", *arguments)
            with self.subTest(arguments=len(arguments)):
                self.assertNotEqual(0, result.returncode)
                self.assertNotIn(b"OS-BLOCKED-ENGINEERING-CHECKS-PASS", result.stdout)
                self.assertEqual(before, self.evidence())


class LauncherStaticTests(unittest.TestCase):
    """Reviewable properties of the elevated path that cannot be exercised unelevated."""

    @classmethod
    def setUpClass(cls):
        cls.text = LAUNCHER.read_bytes().decode("ascii").replace("\r\n", "\n")

    def test_only_its_own_two_rules_and_task_are_created_or_removed(self):
        for forbidden in ("Set-NetFirewallProfile", "Set-NetFirewallRule", "Disable-NetAdapter",
                          "Enable-NetAdapter", "Disable-NetFirewallRule", "netsh", "Restart-Computer",
                          "Stop-Service", "Set-Service", "Set-ExecutionPolicy", "Invoke-WebRequest",
                          "Invoke-RestMethod", "Remove-Item", "-PolicyStore GPO"):
            self.assertNotIn(forbidden.lower(), self.text.lower())
        self.assertEqual(2, self.text.count("New-NetFirewallRule -PolicyStore PersistentStore -Name $ruleNames["))
        # Exactly four removals: by this run's exact rule names, or fed by a list filtered to them.
        removals = re.findall(r"[^\n]*Remove-NetFirewallRule[^\n]*", self.text)
        self.assertEqual(
            ["    foreach (`$name in `$names) { try { Remove-NetFirewallRule -PolicyStore PersistentStore "
             "-Name `$name -ErrorAction Stop } catch { } }",
             "    if (`$found.Count -gt 0) { `$found | Remove-NetFirewallRule -ErrorAction Stop }",
             "        try { Remove-NetFirewallRule -PolicyStore PersistentStore -Name $name -ErrorAction Stop } catch { }",
             "        if ($present.Count -gt 0) { $present | Remove-NetFirewallRule -ErrorAction Stop }"],
            removals)
        self.assertIn("    foreach ($name in $ruleNames) {\n"
                      "        try { Remove-NetFirewallRule -PolicyStore PersistentStore -Name $name", self.text)
        self.assertIn("`$found = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop | "
                      "Where-Object { `$names -contains `$_.Name })", self.text)
        self.assertIn("$present = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop |\n"
                      "            Where-Object { $ruleNames -contains $_.Name })", self.text)
        self.assertIn("`$names = @('$($ruleNames[0])', '$($ruleNames[1])')", self.text)
        self.assertIn("$group = 'CEML-L1Offline-' + $runId", self.text)
        # Parenthesised on purpose: without the inner parentheses the comma binds tighter than +
        # and the "list" is one joined string. That was the failure of the first elevated attempt.
        self.assertIn("$ruleNames = @(($group + '-Inbound'), ($group + '-Outbound'))", self.text)
        self.assertNotIn("@($group + '-Inbound', $group + '-Outbound')", self.text)
        self.assertIn("throw 'Internal error: isolation rule names are not two distinct names'", self.text)
        self.assertEqual(1, self.text.count("Register-ScheduledTask "))

    def test_watchdog_precedes_blocking_and_cleanup_cannot_be_skipped(self):
        order = [self.text.index(marker) for marker in (
            "if ($Mode -eq 'Preflight')", "if (!$admin)", "Reviewed source/launcher hashes required",
            "$baseline = & $PythonPath $helper --probe", "Register-ScheduledTask ",
            "New-NetFirewallRule ", "$isolated = $true", "$child = Start-Process", "} finally {",
            "$present | Remove-NetFirewallRule", "$restored = $true", "$reconnected = ($LASTEXITCODE -eq 0)",
            "if ($restored -and $reconnected) {", "Unregister-ScheduledTask -TaskName $taskName",
            "$passed = (")]
        self.assertEqual(sorted(order), order)
        tail = self.text[self.text.index("} finally {"):]
        self.assertLess(tail.index("} catch { }"), tail.index("Remove-NetFirewallRule"))
        # Independent-review finding: an empty lookup must mean absent, never a failed query,
        # and the watchdog may go only after verified absence and an observed reconnection.
        for line in self.text.split("\n"):
            if "Get-NetFirewallRule" in line or "Unregister-ScheduledTask" in line:
                self.assertNotIn("SilentlyContinue", line)
        self.assertEqual(1, self.text.count("Unregister-ScheduledTask -TaskName $taskName"))
        self.assertIn("if (`$left.Count -ne 0) { exit 1 }", self.text)
        self.assertLess(self.text.index("if (`$left.Count -ne 0) { exit 1 }"),
                        self.text.index("Unregister-ScheduledTask -TaskName '$taskName'"))
        self.assertIn("-RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Hours 12)",
                      self.text)
        self.assertIn("(New-ScheduledTaskTrigger -AtStartup)", self.text)
        # Confirmation-review finding: the enumerations cleanup relies on are proven in the
        # prerequisites, which Preflight and every isolation check run before and during blocking,
        # and removal by exact name does not wait for an enumeration to succeed.
        prerequisites = self.text[self.text.index("function Assert-FirewallPrerequisites {"):
                                  self.text.index("Assert-FirewallPrerequisites\nif ($Mode -eq 'Preflight')")]
        for query in ("$null = @(Get-NetFirewallRule -PolicyStore PersistentStore -ErrorAction Stop)",
                      "$null = @(Get-NetFirewallRule -PolicyStore ActiveStore -ErrorAction Stop)",
                      "$null = @(Get-ScheduledTask -ErrorAction Stop)"):
            self.assertIn(query, prerequisites)
        self.assertLess(tail.index("try { Remove-NetFirewallRule -PolicyStore PersistentStore -Name $name"),
                        tail.index("$present = @(Get-NetFirewallRule"))
        self.assertLess(self.text.index("Block rules from an earlier run are still present"),
                        self.text.index("$runLock = [IO.File]::Open("))
        self.assertIn("-ArgumentList @('/PID', [string]$child.Id, '/T', '/F')", tail)
        self.assertIn("$passed = ($checksPassed -and $isolated -and $restored -and $watchdogRemoved -and $reconnected)",
                      self.text)
        self.assertIn("AddMinutes(25)", self.text)
        self.assertIn("[DateTime]::UtcNow.AddMinutes(20)", self.text)
        self.assertTrue(self.text.rstrip().endswith("if (!$passed) { exit 2 }\nexit 0"))


if __name__ == "__main__":
    unittest.main()
