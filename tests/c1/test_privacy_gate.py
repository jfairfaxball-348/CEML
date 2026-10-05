"""Bounded gate tests; synthetic prohibited forms are assembled only in memory."""

import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tools.c1 import privacy_gate as gate


def synthetic_forms():
    slash = chr(47)
    backslash = chr(92)
    # Keep labels neutral so this test source is itself safe to stage; the
    # sensitive forms are assembled only as values in memory.
    return [
        ("hpath", slash + "home" + slash + "sample" + slash + "item"),
        ("wpath", "Q:" + backslash + "Users" + backslash + "sample" + backslash + "item"),
        ("upath", slash + "opt" + slash + "item"),
        ("unc", backslash * 2 + "sample" + backslash + "share"),
        ("mac1", ":".join(["02", "ab", "34", "56", "78", "9a"])),
        ("mac2", "-".join(["02", "ab", "34", "56", "78", "9a"])),
        ("mac3", ".".join(["02ab", "3456", "789a"])),
        ("ipv4", ".".join(map(str, [192, 0, 2, 17]))),
        ("ipv6", ":".join(["2001", "db8", "", "42"])),
        ("loop", ":" * 2 + "1"),
        ("id", "-".join(["12345678", "1234", "4234", "8234", "123456789abc"])),
        ("mail", "audit" + "@" + "example.invalid"),
        ("pem", "-----BEGIN " + "PRIVATE KEY-----"),
        ("gh", "gh" + "p_" + "x" * 36),
        ("ak", "AK" + "IA" + "X" * 16),
        ("env", "HOME" + "=" + "sample"),
        ("inventory", "Windows IP " + "Configuration"),
    ]


def minimal_report():
    return {
        "experiment": "CEML",
        "schema_version": "CEML-HARDWARE-REPORT-1",
        "artifact_digest": "0" * 64,
        "audit_run_id": "bounded-test",
        "generated_at": "2026-10-04T00:00:00Z",
        "records": [],
        "privacy_scan_passed": True,
    }


class RecognizerTests(unittest.TestCase):
    def test_sensitive_forms_are_detected_without_echo(self):
        for name, value in synthetic_forms():
            with self.subTest(kind=name):
                findings = gate.inspect_text(value)
                self.assertTrue(findings, name)
                self.assertNotIn(value, repr(findings))

    def test_json_keys_and_semantic_labels_including_hashed_identity(self):
        for parts in (["host", "name"], ["user", "name"], ["serial", "_number"], ["device", "_name"], ["host", "name_sha256"]):
            name = "".join(parts)
            value = {name: "f" * 64}
            findings = gate.inspect_text(json.dumps(value), "example.json")
            self.assertTrue(any(item.category == "forbidden_key" for item in findings))
            findings = gate.inspect_text(json.dumps({"fact_name": name, "value": "x"}), "example.json")
            self.assertTrue(any(item.category == "forbidden_label" for item in findings))

    def test_markdown_table_and_camel_case_labels(self):
        for name in ("Host" + "name", "Computer" + "Name", "MAC" + " Address", "Host" + " name"):
            self.assertTrue(gate.inspect_text("| " + name + " | sample |"))
            self.assertTrue(gate.inspect_text(name + ": sample"))

    def test_source_decodes_python_literals_and_dictionary_labels(self):
        value = dict(synthetic_forms())["wpath"]
        text = "captured = " + repr(value)
        self.assertTrue(gate.inspect_text(text, "example.py"))
        name = "host" + "name"
        text = "captured = " + repr({name: "sample"})
        self.assertTrue(any(item.category == "forbidden_key" for item in gate.inspect_text(text, "example.py")))

    def test_plain_source_values_are_scanned(self):
        value = dict(synthetic_forms())["ipv4"]
        self.assertTrue(gate.inspect_text('const auto captured = "' + value + '";', "example.cpp"))

    def test_no_false_matches_for_nonidentifying_capabilities_and_rule_source(self):
        for text in ("Windows 11 version 10.0.26200", "Python 3.12.10", "local/c1/benchmark_records/", "SHA3-256 " + "f" * 64, "https://example.invalid/reference"):
            self.assertEqual([], gate.inspect_text(text))
        for path in (Path(gate.__file__), Path(__file__)):
            self.assertEqual([], gate.inspect_text(path.read_text(encoding="utf-8"), path.name))

    def test_json_duplicate_and_nonfinite_values_refuse(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}'):
            self.assertTrue(any(item.category == "invalid_json" for item in gate.inspect_text(text, "example.json")))


class SchemaTests(unittest.TestCase):
    def test_valid_frozen_hardware_envelope(self):
        self.assertEqual([], gate.validate_artifact(minimal_report(), "example.json"))

    def test_unknown_generated_json_and_wrong_schema_are_rejected(self):
        self.assertEqual("unknown_json_schema", gate.validate_artifact({"schema_version": "UNREVIEWED-1"})[0].category)
        self.assertEqual("unknown_json_schema", gate.validate_artifact({"value": 2})[0].category)
        value = minimal_report()
        value["unreviewed_field"] = True
        self.assertTrue(any(item.category == "schema_invalid" for item in gate.validate_artifact(value)))
        value = minimal_report()
        value["generated_at"] = "not-a-date"
        self.assertTrue(any(item.category == "schema_invalid" for item in gate.validate_artifact(value)))

    def test_schema_failure_contains_no_values(self):
        value = minimal_report()
        value["records"] = [dict(synthetic_forms())["mail"]]
        findings = gate.validate_artifact(value)
        self.assertNotIn(value["records"][0], repr(findings))
        self.assertTrue(any(item.category == "schema_invalid" for item in findings))


class StagedTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-privacy-test-")
        self.repo = Path(self.scratch.name)
        self.git("init", "--quiet")
        (self.repo / "local_reports").mkdir()
        (self.repo / gate.MARKDOWN).write_text("# Sanitized engineering report\n", encoding="utf-8")

    def tearDown(self):
        self.scratch.cleanup()

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True).stdout

    def stage(self, path, content):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
        self.git("add", "--", path)

    def scan(self):
        return gate.scan_staged(self.repo, schema_root=gate.ROOT)

    def test_staged_sensitive_worktree_clean_still_fails(self):
        self.stage("evidence.txt", dict(synthetic_forms())["mail"])
        (self.repo / "evidence.txt").write_text("clean", encoding="utf-8")
        paths, findings = self.scan()
        self.assertIn("evidence.txt", paths)
        self.assertTrue(any(item.category == "email" for _, item in findings))

    def test_clean_index_sensitive_unstaged_and_untracked_are_not_scanned(self):
        self.stage("evidence.txt", "clean")
        (self.repo / "evidence.txt").write_text(dict(synthetic_forms())["mail"], encoding="utf-8")
        (self.repo / "untracked.txt").write_text(dict(synthetic_forms())["mail"], encoding="utf-8")
        paths, findings = self.scan()
        self.assertEqual([], findings)
        self.assertEqual(["evidence.txt", gate.MARKDOWN], paths)

    def test_generated_markdown_scanned_and_staged_bytes_reconciled(self):
        self.stage(gate.MARKDOWN, "# Report\n")
        (self.repo / gate.MARKDOWN).write_text("# Regenerated report\n", encoding="utf-8")
        _, findings = self.scan()
        self.assertTrue(any(item.category == "markdown_worktree_mismatch" for _, item in findings))

    def test_unknown_json_and_invalid_json_fail(self):
        self.stage("unknown.json", '{"schema_version":"UNREVIEWED-1"}')
        self.stage("bad.json", "{")
        _, findings = self.scan()
        self.assertTrue(any(item.category == "unknown_json_schema" for _, item in findings))
        self.assertTrue(any(item.category == "invalid_json" for _, item in findings))

    def test_binary_refuses(self):
        self.stage("evidence.bin", bytes([0, 1, 2, 3]))
        _, findings = self.scan()
        self.assertTrue(any(item.category == "unsupported_nontext" for _, item in findings))

    def test_schema_valid_staged_report(self):
        self.stage("local_reports/HARDWARE_REPORT.json", json.dumps(minimal_report()))
        self.assertEqual([], self.scan()[1])

    def test_cli_failure_does_not_echo_sensitive_value(self):
        value = dict(synthetic_forms())["mail"]
        self.stage("evidence.txt", value)
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            code = gate.main(["--repo", str(self.repo)])
        self.assertEqual(1, code)
        self.assertNotIn(value, stream.getvalue())
        self.assertIn("email", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
