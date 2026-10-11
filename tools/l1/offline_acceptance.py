"""Bounded L1 engineering acceptance; OS isolation is supplied by the PS launcher.

This helper never grants L1 PASS or RUN1 authority. Only the launcher's separate
isolation/restoration record can establish that these checks ran OS-blocked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / "local/frontier/os-offline"


def source_identity(root=ROOT):
    """Bind portable source bytes, including this harness, without machine IDs."""
    names = set()
    for folder, patterns in (
        ("src", ("frontier_*.c", "frontier_*.h", "ceml_oracle.*")),
        ("tools/frontier", ("*.py",)), ("tests/frontier", ("*.py",)),
        ("tools/l1", ("*.py", "*.ps1")), ("tests/l1", ("*.py",)),
        ("schemas", ("frontier_*.schema.json",)),
        ("config", ("frontier_snapshot_*.json", "c1_gmp_pin.toml", "c1_dependency_manifest.toml")),
        ("docs", ("FRONTIER_PROTOCOL_V*.md", "P1_EXCLUSION_PROOFS.md", "P2_PROTOCOL_AUDIT.md")),
        ("tools/c1", ("gmp_smoke.c",)),
    ):
        for pattern in patterns:
            names.update(p.relative_to(root).as_posix() for p in (root/folder).glob(pattern))
    if not names:
        raise ValueError("Missing acceptance sources")
    values = {}
    for name in sorted(names):
        path = root/name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 2*1024*1024:
            raise ValueError("Invalid acceptance source")
        values[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    raw = json.dumps(values, sort_keys=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def probe():
    """Connect and close without sending application data; never used by RUN1."""
    try:
        with socket.create_connection(("1.1.1.1", 443), timeout=3):
            return True
    except OSError:
        return False


def checked_directory(path):
    path = Path(path).absolute()
    if path.is_symlink() or not path.resolve().is_relative_to(LOCAL.resolve()):
        raise ValueError("Evidence must remain in ignored local OS-offline directory")
    path.mkdir(parents=True, exist_ok=True)
    if (path/"checks.json").exists():
        raise ValueError("Existing evidence cannot be overwritten")
    return path


def run_suite(folder=ROOT/"tests/frontier"):
    suite = unittest.defaultTestLoader.discover(str(folder), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return dict(tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                skips=len(result.skipped), expected_failures=len(result.expectedFailures),
                unexpected_successes=len(result.unexpectedSuccesses),
                status="PASS" if result.testsRun > 0 and result.wasSuccessful()
                and not result.skipped and not result.expectedFailures else "FAIL")


def commands():
    snapshot = "config/frontier_snapshot_v2.json" if (ROOT/"config/frontier_snapshot_v2.json").is_file() else "config/frontier_snapshot_v1.json"
    return (
        ("build-command", ["tools/frontier/f1_build.py", "--show-command"]),
        ("build", ["tools/frontier/f1_build.py"]),
        ("clean-reproduction", ["tools/frontier/f1_build.py", "--verify"]),
        ("rules", ["tools/frontier/ceml_frontier.py", "rules"]),
        ("snapshot", ["tools/frontier/ceml_frontier.py", "snapshot", "--file", snapshot]),
        ("launcher-tests", ["-m", "unittest", "discover", "-s", "tests/l1", "-v"]),
        ("full-suite", ["tools/l1/offline_acceptance.py", "--suite"]),
        ("selftest-calibration", ["tools/frontier/ceml_frontier.py", "selftest"]),
        ("final-clean-reproduction", ["tools/frontier/f1_build.py", "--verify"]),
    )


def run_checks(directory, expected_source):
    directory = checked_directory(directory)
    before = source_identity()
    if before != expected_source:
        raise ValueError("Reviewed source identity changed")
    report = dict(schema="CEML-L1-OFFLINE-CHECKS-PREP-1", scope="L1-NONSCIENTIFIC",
                  source_sha256=before, status="FAIL", os_isolation="EXTERNAL-LAUNCHER-REQUIRED",
                  commands=[], scientific_execution="NOT_RUN")
    try:
        for label, args in commands():
            started = time.monotonic()
            with (directory/(label+".log")).open("xb") as log:
                process = subprocess.run([sys.executable, *args], cwd=ROOT,
                                         stdin=subprocess.DEVNULL, stdout=log,
                                         stderr=subprocess.STDOUT, timeout=600)
            report["commands"].append(dict(check=label, exit_code=process.returncode,
                                            seconds=format(time.monotonic()-started, ".6f")))
            if process.returncode != 0:
                raise RuntimeError("Engineering check failed")
        if source_identity() != before:
            raise ValueError("Sources changed during acceptance")
        manifest = json.loads((ROOT/"local/frontier/build/build_manifest.json").read_bytes())
        report["native_build_digest"] = manifest["digest"]
        report["status"] = "ENGINEERING-CHECKS-PASS"
    except Exception as error:
        report["failure_kind"] = type(error).__name__
        raise
    finally:
        with (directory/"checks.json").open("x", encoding="ascii") as output:
            json.dump(report, output, sort_keys=True, separators=(",", ":"))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--plan", action="store_true")
    modes.add_argument("--probe", action="store_true")
    modes.add_argument("--suite", action="store_true")
    modes.add_argument("--run", action="store_true")
    parser.add_argument("--output-dir")
    parser.add_argument("--expected-source")
    args = parser.parse_args()
    if args.plan:
        print(json.dumps(dict(scope="L1-NONSCIENTIFIC", source_sha256=source_identity(),
                              python_version=".".join(map(str, sys.version_info[:3])),
                              commands=[label for label, _ in commands()]), sort_keys=True))
        return 0
    if args.probe:
        connected = probe()
        print(json.dumps(dict(connected=connected)))
        return 0 if connected else 2
    if args.suite:
        result = run_suite()
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "PASS" else 2
    if not args.output_dir or not args.expected_source:
        parser.error("--run requires --output-dir and --expected-source")
    print(json.dumps(run_checks(args.output_dir, args.expected_source), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(json.dumps(dict(status="REFUSED", failure_kind=type(error).__name__)))
        sys.exit(2)
