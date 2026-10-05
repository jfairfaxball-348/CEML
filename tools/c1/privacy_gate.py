"""I1 deterministic staged-data gate; hardware characterization, never calibration.

This is a recognizer, not a proof that arbitrary prose contains no identity. It
requires the I1 human diff review as well. No value exceptions, entropy-based
guesses, network schema lookups, report mutations, or index mutations are used.
Source is scanned too, including decoded Python literals and dictionary labels.
Rule names and regular expressions are not captured hardware labels; mentioning
one in explanatory prose is consequently different from emitting a labelled value.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from datetime import datetime
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
I1_BASELINE = "e2148e47f4cc71ba33bfc5c05140d2adef32f479"
MARKDOWN = "local_reports/HARDWARE_REPORT.md"
SCHEMA_VERSIONS = {
    "CEML-HARDWARE-REPORT-1": "schemas/c1_evidence.schema.json",
    "CEML-CALIBRATION-RECORD-1": "schemas/c1_evidence.schema.json",
    "CEML-BENCHMARK-SUMMARY-1": "schemas/c1_evidence.schema.json",
    "CEML-ENGINEERING-DECISIONS-1": "schemas/c1_evidence.schema.json",
    "CEML-BENCHMARK-BUNDLES-1": "schemas/c1_evidence.schema.json",
    "CEML-BUILD-MANIFEST-1": "schemas/c1_evidence.schema.json",
    "CEML-LOCAL-MACHINE-PROFILE-1": "schemas/hardware_profile.schema.json",
}
FORBIDDEN_LABELS = (
    "hostname", "computer_name", "device_name", "username", "user", "home",
    "account_id", "serial", "serial_number", "uuid", "unique_id", "mac",
    "ip_address", "ssid", "wifi", "token", "secret", "password", "cookie",
    "private_key", "userprofile", "computername", "csname", "pscomputername",
    "host_name", "ipaddress", "serialnumber", "uniqueid", "accountid",
    "privatekey", "wi_fi", "api_key", "access_key", "client_secret",
)
LABEL_VALUE_FIELDS = {"fact_name", "category", "requested_item"}
PATTERNS = (
    ("home_path", r"(?i)(?:/(?:home|Users)/[^\s/]+|[a-z]:[\\/]+Users[\\/]+[^\s\\/]+)"),
    ("absolute_path", r"(?i)(?<![\w])[a-z]:[\\/]+"),
    ("absolute_path", r"(?<![/#:\w])/(?![/*])[A-Za-z0-9._~-]+(?:/[^\s\"'`<>|]*)?"),
    ("absolute_path", r"\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9._-]+"),
    ("mac_address", r"(?i)(?<![\w:])(?:[0-9a-f]{2}:){5}[0-9a-f]{2}(?![\w:])"),
    ("mac_address", r"(?i)(?<![\w-])(?:[0-9a-f]{2}-){5}[0-9a-f]{2}(?![\w-])"),
    ("mac_address", r"(?i)(?<![\w.])(?:[0-9a-f]{4}\.){2}[0-9a-f]{4}(?![\w.])"),
    ("uuid", r"(?i)(?<![\w-])[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}(?![\w-])"),
    ("email", r"(?i)(?<![\w.+-])[\w.!#$%&'*+/=?^`{|}~-]+@[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}(?![\w.-])"),
    ("private_key", r"-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----"),
    ("credential", r"\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    ("credential", r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|\bAIza[A-Za-z0-9_-]{35}\b"),
    ("credential", r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b|\bsk-[A-Za-z0-9_-]{20,}\b"),
    ("credential", r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    ("environment_dump", r"(?im)^\s*(?:HOME|USERNAME|USERPROFILE|COMPUTERNAME|LOGNAME|USER)\s*="),
    ("raw_inventory", r"(?im)^\s*(?:Windows IP Configuration|System Information|Computer Information|Hardware Overview|Network Configuration)\s*:?\s*$"),
    ("raw_inventory", r"(?im)^\s*(?:PS\s+[^>\r\n]+>\s*)?(?:Get-ComputerInfo|system_profiler\s+-detailLevel\s+full|ipconfig\s+[/]all|printenv)\s*$"),
)
COMPILED_PATTERNS = tuple((kind, re.compile(pattern)) for kind, pattern in PATTERNS)
IPV4_CANDIDATE = re.compile(r"(?<![\w.])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![\w.])")
IPV6_CANDIDATE = re.compile(r"(?i)(?<![\w:])(?:[0-9a-f]{0,4}:){2,}[0-9a-f:.]*(?:%[A-Za-z0-9_.-]+)?(?![\w:])")
LABEL_LINE = re.compile(
    r"(?m)^\s*(?:[-*]\s+)?[\"'`]?([A-Za-z][A-Za-z0-9_ .-]{0,80})[\"'`]?\s*[:=]\s*\S"
)
TABLE_LABEL = re.compile(r"(?m)^\s*\|\s*([A-Za-z][A-Za-z0-9_ .-]{0,80})\s*\|\s*\S")


@dataclass(frozen=True, order=True)
class Finding:
    category: str
    location: str


class GateFailure(Exception):
    """The message is always a fixed category, never subprocess output."""


def _git(root: Path, *args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False,
        )
    except OSError as exc:
        raise GateFailure("git_unavailable") from exc
    if result.returncode:
        raise GateFailure("git_read_failed")
    return result.stdout


def _forbidden_label(label: str) -> bool:
    label = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", label)
    normalized = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
    # Component boundaries catch hashes of identifiers as well as the identifier.
    wrapped = "_" + normalized + "_"
    return any("_" + item + "_" in wrapped for item in FORBIDDEN_LABELS)


def _value_findings(text: str, prefix: str = "") -> list[Finding]:
    found = []
    for category, pattern in COMPILED_PATTERNS:
        for match in pattern.finditer(text):
            found.append(Finding(category, prefix + "line:" + str(text.count("\n", 0, match.start()) + 1)))
    for category, pattern in (("ipv4", IPV4_CANDIDATE), ("ipv6", IPV6_CANDIDATE)):
        for match in pattern.finditer(text):
            try:
                ipaddress.ip_address(match.group())
            except ValueError:
                continue
            found.append(Finding(category, prefix + "line:" + str(text.count("\n", 0, match.start()) + 1)))
    for pattern in (LABEL_LINE, TABLE_LABEL):
        for match in pattern.finditer(text):
            if _forbidden_label(match.group(1)):
                found.append(Finding("forbidden_label", prefix + "line:" + str(text.count("\n", 0, match.start()) + 1)))
    return found


def _object_findings(value: object, location: str = "object") -> list[Finding]:
    found = []
    if isinstance(value, dict):
        for index, (key, item) in enumerate(value.items()):
            here = location + ":member:" + str(index)
            if isinstance(key, str):
                if _forbidden_label(key):
                    found.append(Finding("forbidden_key", here))
                found.extend(_value_findings(key, here + ":key:"))
                if key in LABEL_VALUE_FIELDS and isinstance(item, str) and _forbidden_label(item):
                    found.append(Finding("forbidden_label", here))
            found.extend(_object_findings(item, here))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(_object_findings(item, location + ":item:" + str(index)))
    elif isinstance(value, str):
        found.extend(_value_findings(value, location + "/"))
    return found


def _reject_constant(_: str) -> None:
    raise ValueError("non_json_number")


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def parse_json(text: str) -> object:
    return json.loads(text, object_pairs_hook=_unique_object, parse_constant=_reject_constant)


def inspect_text(text: str, logical_path: str = "<artifact>") -> list[Finding]:
    """Recognize prohibited forms without ever returning the matched value."""
    found = _value_findings(text)
    if Path(logical_path).suffix.lower() == ".json":
        try:
            found.extend(_object_findings(parse_json(text)))
        except (ValueError, RecursionError):
            found.append(Finding("invalid_json", "document"))
    if Path(logical_path).suffix.lower() == ".py":
        try:
            tree = ast.parse(text)
        except (SyntaxError, ValueError, RecursionError):
            found.append(Finding("source_parse_failed", "document"))
        else:
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    found.extend(_value_findings(node.value, "literal:" + str(node.lineno) + "/"))
                elif isinstance(node, ast.Dict):
                    for key in node.keys:
                        if isinstance(key, ast.Constant) and isinstance(key.value, str) and _forbidden_label(key.value):
                            found.append(Finding("forbidden_key", "literal:" + str(key.lineno)))
    return sorted(set(found))


def validate_artifact(value: object, logical_path: str = "<artifact>", root: Path | None = None) -> list[Finding]:
    """Validate a C1 JSON object using the immutable I1 baseline, wholly offline.

    The baseline mapping is deliberately closed. Unknown generated JSON, schema
    documents, and unversioned configuration cannot silently become C1 evidence.
    Any additional source-configuration schema needs a reviewed mapping change.
    """
    found = _object_findings(value)
    version = value.get("schema_version") if isinstance(value, dict) else None
    if not isinstance(version, str) or version not in SCHEMA_VERSIONS:
        return sorted(set(found + [Finding("unknown_json_schema", "document")]))
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        schema_bytes = _git(root or ROOT, "show", I1_BASELINE + ":" + SCHEMA_VERSIONS[version])
        schema = parse_json(schema_bytes.decode("utf-8"))
        Draft202012Validator.check_schema(schema)
        checker = FormatChecker()

        @checker.checks("date-time")
        def audit_timestamp(item):
            # jsonschema's optional date dependency may be absent. Never silently
            # skip the format constraint. Audit timestamps use this conservative
            # RFC 3339 subset; leap-second spellings are refused.
            if not isinstance(item, str):
                return True
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})", item):
                return False
            try:
                datetime.fromisoformat(item.upper().replace("Z", "+00:00"))
            except ValueError:
                return False
            return True

        validator = Draft202012Validator(schema, format_checker=checker)
        if not validator.is_valid(value):
            # jsonschema messages and key paths can contain the offending value.
            found.append(Finding("schema_invalid", "document"))
    except ImportError:
        found.append(Finding("schema_validator_unavailable", "document"))
    except (GateFailure, ValueError, UnicodeError, RecursionError):
        found.append(Finding("frozen_schema_unavailable", "document"))
    return sorted(set(found))


def _decode(blob: bytes) -> str:
    if b"\x00" in blob:
        raise GateFailure("unsupported_nontext")
    try:
        return blob.decode("utf-8-sig")
    except UnicodeError as exc:
        raise GateFailure("unsupported_nontext") from exc


def _display_path(path: str, number: int) -> str:
    if _value_findings(path) or any(ord(char) < 32 for char in path):
        return "<redacted-file-" + str(number) + ">"
    return path


def scan_staged(root: Path, schema_root: Path | None = None) -> tuple[list[str], list[tuple[str, Finding]]]:
    """Scan every staged changed blob plus generated Markdown; do not stage files.

    Scanning every staged file is a conservative C1 scope: no extension/path
    heuristic can accidentally omit a newly introduced C1 source or lock file.
    Deleted entries have no blob. Symlinks, gitlinks and unmerged entries refuse.
    """
    start = _git(root, "diff", "--cached", "--raw", "--no-abbrev", "--no-renames", "-z")
    names = _git(root, "diff", "--cached", "--name-only", "--no-renames", "--diff-filter=ACMRTUXB", "-z")
    try:
        paths = sorted(part.decode("utf-8") for part in names.split(b"\x00") if part)
    except UnicodeError as exc:
        raise GateFailure("unsupported_filename") from exc
    index = {}
    for entry in _git(root, "ls-files", "--stage", "-z").split(b"\x00"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, _, stage = metadata.split()
            index.setdefault(path.decode("utf-8"), []).append((mode, stage))
    findings = []
    inspected = []
    staged_markdown = None
    for number, path in enumerate(paths, 1):
        display = _display_path(path, number)
        inspected.append(display)
        if index.get(path) not in ([(b"100644", b"0")], [(b"100755", b"0")]):
            findings.append((display, Finding("unsupported_index_entry", "document")))
            continue
        try:
            blob = _git(root, "show", ":" + path)
            text = _decode(blob)
        except GateFailure as exc:
            findings.append((display, Finding(str(exc), "document")))
            continue
        if path == MARKDOWN:
            staged_markdown = blob
        file_findings = inspect_text(text, path)
        if Path(path).suffix.lower() == ".json":
            try:
                value = parse_json(text)
                file_findings.extend(validate_artifact(value, path, schema_root or root))
            except (ValueError, RecursionError):
                file_findings.append(Finding("invalid_json", "document"))
        findings.extend((display, finding) for finding in sorted(set(file_findings)))
    try:
        generated = (root / MARKDOWN).read_bytes()
        if staged_markdown is not None and generated != staged_markdown:
            findings.append((MARKDOWN, Finding("markdown_worktree_mismatch", "document")))
        if staged_markdown is None:
            inspected.append(MARKDOWN)
            findings.extend((MARKDOWN, item) for item in inspect_text(_decode(generated), MARKDOWN))
    except (OSError, GateFailure):
        findings.append((MARKDOWN, Finding("generated_markdown_unavailable", "document")))
    if start != _git(root, "diff", "--cached", "--raw", "--no-abbrev", "--no-renames", "-z"):
        findings.append(("<index>", Finding("index_changed_during_scan", "document")))
    return inspected, sorted(set(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        inspected, findings = scan_staged(args.repo)
    except (GateFailure, OSError, UnicodeError, ValueError, RecursionError):
        print("FAIL <gate> scan_unavailable document")
        return 1
    for path, finding in findings:
        print("FAIL", path, finding.category, finding.location)
    if findings:
        return 1
    print("PASS staged C1 text and generated Markdown; files=" + str(len(inspected)))
    print("Human staged-diff review remains required by I1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
