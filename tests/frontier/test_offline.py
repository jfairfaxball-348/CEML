"""Offline acceptance checks; no scientific interval is started here."""

import ast
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
FRONTIER = ROOT / "tools" / "frontier"
NETWORK_MODULES = {
    "socket", "http", "urllib", "ftplib", "telnetlib", "smtplib",
    "requests", "aiohttp", "websockets", "xmlrpc",
}


class OfflineSourceTests(unittest.TestCase):
    def test_frontier_modules_have_only_local_standard_library_imports(self):
        sources = sorted(FRONTIER.glob("*.py"))
        self.assertGreaterEqual(len(sources), 3)
        for source in sources:
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    modules = [node.module]
                for module in modules:
                    with self.subTest(source=source.name, module=module):
                        top = module.split(".")[0]
                        self.assertNotIn(top, NETWORK_MODULES)
                        self.assertTrue(
                            top in sys.stdlib_module_names
                            or module in {"reference", "ceml_frontier", "f1_build"}
                            or module.startswith("tools.frontier"),
                            "nonstandard or non-frontier import",
                        )
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"eval", "exec", "__import__"})

    def test_native_worker_has_no_network_or_telemetry_entry_points(self):
        for name in ("frontier_main.c", "frontier_worker.c", "frontier_worker.h"):
            text = (ROOT / "src" / name).read_text(encoding="ascii").lower()
            for token in ("winsock", "winhttp", "wininet", "curl_", "socket(",
                          "telemetry", "internetopen", "urldownload"):
                with self.subTest(source=name, token=token):
                    self.assertNotIn(token, text)

    def test_driver_has_no_shell_or_git_mutation_path(self):
        forbidden = {"commit", "push", "fetch", "pull", "checkout", "reset", "merge"}
        for source in sorted(FRONTIER.glob("*.py")):
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                for keyword in node.keywords:
                    if keyword.arg == "shell":
                        self.assertIsInstance(keyword.value, ast.Constant)
                        self.assertIs(keyword.value.value, False)
                if node.args and isinstance(node.args[0], (ast.List, ast.Tuple)):
                    values = [item.value for item in node.args[0].elts
                              if isinstance(item, ast.Constant) and isinstance(item.value, str)]
                    if values and Path(values[0]).stem.lower() == "git":
                        self.assertTrue(set(values[1:]).isdisjoint(forbidden))


class NetworkBlockedCliTests(unittest.TestCase):
    # A new interpreter runs each real CLI command with both forbidden imports
    # and the CPython socket audit events denied. No host adapter is modified.
    WRAPPER = r'''
import builtins
from pathlib import Path
import runpy
import sys
blocked = {"socket", "http", "urllib", "ftplib", "telnetlib", "smtplib", "requests", "aiohttp", "websockets", "xmlrpc"}
original = builtins.__import__
def deny_import(name, *args, **kwargs):
    if name.split(".")[0] in blocked:
        raise RuntimeError("offline import refusal")
    return original(name, *args, **kwargs)
def audit(event, arguments):
    if event.startswith("socket."):
        raise RuntimeError("offline network refusal")
sys.addaudithook(audit)
builtins.__import__ = deny_import
root = Path(sys.argv[1])
sys.path.insert(0, str(root))
sys.path.insert(0, str(root / "tools/frontier"))
sys.argv = [str(root / "tools/frontier/ceml_frontier.py"), *sys.argv[2:]]
runpy.run_path(sys.argv[0], run_name="__main__")
'''

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, "-c", self.WRAPPER, str(ROOT), *arguments],
            cwd=ROOT, capture_output=True, timeout=30, check=False,
        )

    def test_rules_runs_with_all_network_paths_denied(self):
        result = self.run_cli("rules")
        self.assertEqual(0, result.returncode, result.stderr.decode("ascii", "replace"))
        self.assertTrue(result.stdout)

    def test_frozen_snapshot_inspection_runs_offline(self):
        result = self.run_cli("snapshot", "--file", "config/frontier_snapshot_v2.json")
        self.assertEqual(0, result.returncode, result.stderr.decode("ascii", "replace"))
        report = json.loads(result.stdout)
        self.assertEqual(("research_only_unaccepted",
                          "538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729"),
                         (report["status"], report["digest"]))
        self.assertEqual("a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66",
                         report["provenance"]["source_digest"])

    def test_version_1_snapshot_is_reported_frozen_and_not_runnable(self):
        result = self.run_cli("snapshot", "--file", "config/frontier_snapshot_v1.json")
        self.assertEqual(0, result.returncode, result.stderr.decode("ascii", "replace"))
        report = json.loads(result.stdout)
        self.assertEqual(("frozen_version_1_research_only_not_runnable",
                          "a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66"),
                         (report["status"], report["digest"]))

    def test_l1_refuses_operator_commands_and_nonfixture_inspection(self):
        with tempfile.TemporaryDirectory(prefix="ceml-frontier-cli-denied-") as scratch:
            out = Path(scratch) / "manifest.json"
            commands = (
                ("prepare-authority", "--authority-id", "RUN1-denied", "--base-kind", "published",
                 "--batch-start", "2361183241434822606848", "--batch-end", "2361183241434822606992",
                 "--acknowledge", "not-an-acknowledgement", "--owner-instruction", "SIMULATED DENIAL ONLY"),
                ("prepare-manifest", "--out", str(out), "--authority-id", "RUN1-denied",
                 "--acknowledge", "not-an-acknowledgement", "--max-t-per-explicit", "100000",
                 "--max-total-t", "2000000", "--run-id", "RUN1-denied", "--base-kind", "published"),
            )
            for arguments in commands:
                result = self.run_cli(*arguments)
                with self.subTest(command=arguments[0]):
                    self.assertEqual(2, result.returncode)
                    self.assertEqual("RUN1 not owner-authorised", json.loads(result.stdout)["reason"])
            self.assertFalse(out.exists())
            for command in ("inspect", "replay"):
                result = self.run_cli(command, "--batch-dir", scratch)
                with self.subTest(command=command):
                    self.assertEqual(2, result.returncode)
                    self.assertIn("only predesignated fixtures", json.loads(result.stdout)["reason"])

    def test_marker_file_does_not_open_inspect_or_replay_for_a_nonfixture_interval(self):
        # Independent-review finding: the mere presence of acceptance.json used to be enough.
        sys.path.insert(0, str(FRONTIER))
        import ceml_frontier as driver
        run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        run.update(base_B="5000", batch_start="5000", batch_end="5010",
                   accepted_assumption_ack=run["snapshot_digest"] + ":published:5000")
        run["predecessor_digest"] = driver.genesis(run)
        for marker in (b"", b"{}", driver.canonical(driver.fixture_marker(run))):
            with tempfile.TemporaryDirectory(prefix="ceml-frontier-cli-marker-") as scratch:
                directory = Path(scratch)
                (directory / "run.json").write_bytes(driver.canonical(run))
                (directory / "snapshot.json").write_bytes((ROOT / "config/frontier_snapshot_v2.json").read_bytes())
                (directory / "acceptance.json").write_bytes(marker)
                before = sorted(path.name for path in directory.iterdir())
                for command in ("inspect", "replay"):
                    result = self.run_cli(command, "--batch-dir", scratch)
                    with self.subTest(command=command, marker=len(marker)):
                        self.assertEqual(2, result.returncode)
                        self.assertEqual("REFUSED", json.loads(result.stdout)["status"])
                self.assertEqual(before, sorted(path.name for path in directory.iterdir()))

    def test_scientific_pilot_refuses_without_run1_evidence(self):
        sys.path.insert(0, str(FRONTIER))
        import ceml_frontier as driver
        snapshot = driver.snapshot()
        run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        base = snapshot["published"]["B"]
        run.update(run_id="RUN1-denial-fixture", run1_authority_id="RUN1-no-authority",
                   base_B=base, batch_start=base, batch_end=str(int(base) + 144),
                   accepted_assumption_ack=run["snapshot_digest"] + ":published:" + base)
        run["predecessor_digest"] = driver.genesis(run)
        driver.validate_manifest(run, snapshot)
        with tempfile.TemporaryDirectory(prefix="ceml-frontier-cli-gate-") as scratch:
            directory = Path(scratch)
            manifest, output = directory / "run.json", directory / "out"
            manifest.write_bytes(driver.canonical(run))
            result = self.run_cli("pilot", "--manifest", str(manifest), "--out", str(output))
            self.assertNotEqual(0, result.returncode)
            self.assertIn("RUN1 not owner-authorised", json.loads(result.stdout)["reason"])
            self.assertFalse(output.exists())

    def test_offline_build_command_inspection_imports_no_network_module(self):
        wrapper = self.WRAPPER.replace("tools/frontier/ceml_frontier.py", "tools/frontier/f1_build.py")
        result = subprocess.run([sys.executable, "-c", wrapper, str(ROOT), "--show-command"],
                                cwd=ROOT, capture_output=True, timeout=30)
        self.assertEqual(0, result.returncode, result.stderr.decode("ascii", "replace"))
        report = json.loads(result.stdout)
        self.assertIn("-std:c17", report["release"])
        self.assertIn("-WX", report["checked"])


if __name__ == "__main__":
    unittest.main()
