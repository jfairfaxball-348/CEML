"""Gate, chain-limit and native-boundary refusals found untested by independent review.

Engineering fixtures only. No frontier integer is scanned or replayed: the two
records that carry 2^71 fields are refused while every arithmetic entry point is
replaced by a failing sentinel, and the one native scan above the L1 cap is the
single even integer 10000 under a synthetic status file.
"""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "frontier"))
import ceml_frontier as driver
import f1_build
import reference

RUN1 = "**Authoritative current phase:** RUN1\n**Scientific execution authorization:** AUTHORISED\n"
L1 = "**Authoritative current phase:** L1\n**Scientific execution authorization:** DENIED\n"
DASH = chr(8212)


def summary(start, end):
    return driver.summary_reference(start, end, 100000, 2000000)


def rebased(start, end):
    """A shape-valid manifest for an interval that is not a predesignated fixture."""
    run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
    run.update(base_B=str(start), batch_start=str(start), batch_end=str(end),
               accepted_assumption_ack=run["snapshot_digest"] + ":published:" + str(start))
    run["predecessor_digest"] = driver.genesis(run)
    return run


class ReadOnlyCommandGateTests(unittest.TestCase):
    """inspect and replay validate a fixture in full before reading a slot or recomputing a start."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-read-gate-")
        self.addCleanup(self.scratch.cleanup)
        self.count = 0
        sentinel = AssertionError("arithmetic or slot access before the gate")
        for target, name in ((driver, "summary_reference"), (reference, "replay"), (reference, "event"),
                             (driver.CheckpointStore, "read_slot"), (driver.CheckpointStore, "recover")):
            patcher = mock.patch.object(target, name, side_effect=sentinel)
            setattr(self, "spy_" + name, patcher.start())
            self.addCleanup(patcher.stop)

    def directory(self, run, marker):
        self.count += 1
        directory = Path(self.scratch.name) / f"batch-{self.count}"
        directory.mkdir()
        (directory / "run.json").write_bytes(driver.canonical(run))
        (directory / "snapshot.json").write_bytes((ROOT / "config/frontier_snapshot_v2.json").read_bytes())
        if marker is not None:
            (directory / "acceptance.json").write_bytes(marker)
        # Shape-valid, self-sealed, correctly bound records. Nothing but the gate
        # stands between these and a recomputation of the manifest's interval.
        bound = dict(run_digest=driver.H("RUN", driver.canonical(run)),
                     **{key: run[key] for key in driver.BINDING},
                     counts=dict.fromkeys(reference.COUNT_KEYS, "0"), transcript_digest="0" * 64,
                     explicit_t_steps="0", explicit_odd_steps="0", explicit_standard_steps="0",
                     explicit_attempts="0", pending=None)
        root = driver.seal(dict(bound, schema=driver.SCHEMA_IDS["checkpoint"], generation="0",
                                previous_checkpoint_digest=None, next_n=run["batch_start"]), "CHECKPOINT")
        certificate = driver.seal(dict(bound, schema=driver.SCHEMA_IDS["certificate"],
                                       status="conditional_complete", checker_source_digest="0" * 64,
                                       independent_replay_digest="0" * 64, unresolved_count="0"), "CERTIFICATE")
        driver.validate_shape(root, "checkpoint")
        driver.validate_shape(certificate, "certificate")
        (directory / "ckpt.0.json").write_bytes(driver.canonical(root))
        (directory / "certificate.json").write_bytes(driver.canonical(certificate))
        return directory

    def assert_gate_refuses(self, directory):
        for command in (driver.inspect_batch, driver.reference_replay):
            with self.subTest(command=command.__name__), self.assertRaises((driver.Refusal, OSError)):
                command(directory)
        for spy in (self.spy_summary_reference, self.spy_replay, self.spy_event,
                    self.spy_read_slot, self.spy_recover):
            spy.assert_not_called()

    def test_marker_file_alone_never_opens_a_nonfixture_interval(self):
        fixture = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        small = rebased(5000, 5010)
        for index, marker in enumerate((b"", b"{}", b"null", driver.canonical(driver.fixture_marker(fixture)),
                                        driver.canonical(driver.fixture_marker(small)),
                                        driver.canonical(driver.fixture_marker(small)) + b"\n")):
            with self.subTest(marker=index):
                self.assert_gate_refuses(self.directory(small, marker))
        # The exact marker for a real fixture name still needs that fixture's exact interval.
        renamed = dict(small, run_id="L1-fixture-wide")
        renamed["predecessor_digest"] = driver.genesis(renamed)
        self.assert_gate_refuses(self.directory(renamed, driver.canonical(driver.fixture_marker(renamed))))

    def test_frontier_magnitude_manifest_is_refused_before_any_arithmetic(self):
        base = int(driver.snapshot()["published"]["B"])
        high = rebased(base, base + 144)
        for marker in (None, b"", driver.canonical(driver.fixture_marker(high))):
            self.assert_gate_refuses(self.directory(high, marker))
        science = dict(high, run1_authority_id="RUN1-synthetic")
        self.assert_gate_refuses(self.directory(science, None))

    def test_run1_status_still_requires_a_valid_scientific_manifest(self):
        with mock.patch.object(driver, "status_text", return_value=RUN1):
            self.assert_gate_refuses(self.directory(rebased(5000, 5010), None))
            wrong_base = dict(rebased(5000, 5010), run1_authority_id="RUN1-synthetic")
            self.assert_gate_refuses(self.directory(wrong_base, None))

    def test_phase_alone_never_opens_read_only_commands_on_science(self):
        # Confirmation-review note: RUN1 as a phase with science still denied used to be enough.
        base = int(driver.snapshot()["published"]["B"])
        science = dict(rebased(base, base + 144), run1_authority_id="RUN1-synthetic")
        directory = self.directory(science, None)
        for status in (RUN1.replace("AUTHORISED", "DENIED"), RUN1.replace("AUTHORISED", "AUTHORISED-NOT"),
                       RUN1 + RUN1, L1, ""):
            with mock.patch.object(driver, "status_text", return_value=status):
                with self.subTest(status=status[:60]):
                    self.assertFalse(driver.science_readable(False))
                    self.assert_gate_refuses(directory)
        # Positive control: full RUN1 status and a valid scientific manifest pass the gate
        # itself, which reads two records and computes nothing.
        with mock.patch.object(driver, "status_text", return_value=RUN1):
            self.assertTrue(driver.science_readable(False))
            self.assertEqual(science, driver.read_only_gate(directory))
        self.assertTrue(driver.science_readable(True))
        self.spy_summary_reference.assert_not_called()

    def test_only_listed_run_ids_and_intervals_are_fixtures(self):
        self.assertEqual({"L1-fixture-a": {(2, 146), (146, 290)}, "L1-fixture-b": {(143, 287)},
                          "L1-fixture-c": {(17, 113)}, "L1-fixture-wide": {(2, 9602)}}, driver.FIXTURE_INTERVALS)
        # The successor is the second batch of the L1-fixture-a chain, never a chain of its own.
        lone = rebased(146, 290)
        lone["run_id"] = "L1-fixture-successor"
        lone["predecessor_digest"] = driver.genesis(lone)
        with self.assertRaisesRegex(driver.Refusal, "not a predesignated L1 fixture"):
            driver.validate_manifest(lone, driver.snapshot(), True)
        self.assert_gate_refuses(self.directory(lone, driver.canonical(driver.fixture_marker(lone))))
        for name in ("L1-fixture-a", "L1-fixture-successor", "L1-fixture-b", "L1-fixture-c", "L1-fixture-wide"):
            driver.validate_manifest(driver.fixture_run(name, build_digest="0" * 64), driver.snapshot(), True)

    def test_valid_fixture_passes_the_gate_and_reaches_the_reader(self):
        fixture = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        directory = self.directory(fixture, driver.canonical(driver.fixture_marker(fixture)))
        self.assertEqual(fixture, driver.read_only_gate(directory))
        with self.assertRaises(AssertionError):
            driver.inspect_batch(directory)
        self.spy_read_slot.assert_called_once()


class ChainIntegrityTests(unittest.TestCase):
    """Two committed fixture batches with a mocked build; each refusal is checked by reason."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-chain-")
        self.addCleanup(self.scratch.cleanup)
        self.chain = Path(self.scratch.name) / "chain"
        patcher = mock.patch.object(f1_build, "verify_build", return_value={"digest": "0" * 64})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.first_run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        self.first = self.chain / "first"
        driver.prepare_fixture(self.first, self.first_run)
        self.first_cert = driver.commit_batch(self.first, self.first_run, summary(2, 146), True)
        self.second_run = driver.fixture_run("L1-fixture-successor", build_digest="0" * 64)
        self.second_run["predecessor_digest"] = self.first_cert["digest"]
        self.second = self.chain / "second"
        driver.prepare_fixture(self.second, self.second_run)
        self.second_cert = driver.commit_batch(self.second, self.second_run, summary(146, 290), True)

    def test_duplicate_or_missing_predecessor_refuses(self):
        self.assertEqual(self.second_cert, driver.verify_batch(self.second / "certificate.json", True))
        shutil.copytree(self.first, self.chain / "first-copy")
        with self.assertRaisesRegex(driver.Refusal, "missing/duplicate immutable predecessor"):
            driver.verify_batch(self.second / "certificate.json", True)
        shutil.rmtree(self.chain / "first-copy")
        self.first.rename(Path(self.scratch.name) / "moved-away")
        with self.assertRaisesRegex(driver.Refusal, "missing/duplicate immutable predecessor"):
            driver.verify_batch(self.second / "certificate.json", True)

    def test_predecessor_gap_or_identity_drift_refuses(self):
        driver.predecessor(self.second, self.second_run, True)
        for change in (dict(batch_end="145"), dict(batch_end="147"), dict(table_digest="1" * 64),
                       dict(native_build_digest="1" * 64), dict(snapshot_digest="1" * 64),
                       dict(base_B="3"), dict(run_id="other"), dict(base_kind="operational")):
            with mock.patch.object(driver, "verify_batch", return_value=dict(self.first_cert, **change)):
                with self.subTest(change=sorted(change)), \
                     self.assertRaisesRegex(driver.Refusal, "predecessor chain gap/identity mismatch"):
                    driver.predecessor(self.second, self.second_run, True)

    def test_ledger_refuses_duplicate_mixed_and_rootless_chains(self):
        self.assertEqual("2", driver.ledger(self.chain, True)["batches"])
        shutil.copytree(self.second, self.chain / "second-copy")
        with self.assertRaisesRegex(driver.Refusal, "ledger duplicate certificate"):
            driver.ledger(self.chain, True)
        shutil.rmtree(self.chain / "second-copy")
        other_run = driver.fixture_run("L1-fixture-b", build_digest="0" * 64)
        other = self.chain / "other-root"
        driver.prepare_fixture(other, other_run)
        driver.commit_batch(other, other_run, summary(143, 287), True)
        with self.assertRaisesRegex(driver.Refusal, "ledger duplicate/fork/gap/identity mismatch"):
            driver.ledger(self.chain, True)
        shutil.rmtree(other)
        self.first.rename(Path(self.scratch.name) / "moved-away")
        with self.assertRaisesRegex(driver.Refusal, "ledger predecessor missing"):
            driver.ledger(self.chain, True)

    def test_chain_slot_refuses_reused_run_id_overlap_and_active_sibling(self):
        drifted = dict(self.second_run, table_digest="1" * 64)
        with self.assertRaisesRegex(driver.Refusal, "run ID reused across chain roots"):
            driver.ensure_chain_slot(self.chain / "third", drifted)
        with self.assertRaisesRegex(driver.Refusal, "duplicate/overlapping batch"):
            driver.ensure_chain_slot(self.chain / "again", self.first_run)
        with self.assertRaisesRegex(driver.Refusal, "duplicate/overlapping batch"):
            driver.ensure_chain_slot(self.chain / "again", self.second_run)
        (self.first / "certificate.json").rename(self.first / "certificate.moved")
        shutil.rmtree(self.second)
        with self.assertRaisesRegex(driver.Refusal, "another batch of this chain is uncommitted"):
            driver.ensure_chain_slot(self.chain / "second", self.second_run)

    def test_cycle_and_depth_limits_refuse(self):
        path = self.second / "certificate.json"
        with self.assertRaisesRegex(driver.Refusal, "certificate cycle/depth limit"):
            driver.verify_batch(path, True, seen={self.second_cert["digest"]})
        with self.assertRaisesRegex(driver.Refusal, "certificate cycle/depth limit"):
            driver.verify_batch(path, True, seen={str(index) for index in range(driver.MAX_CHAIN)})
        driver.verify_batch(path, True, seen={str(index) for index in range(driver.MAX_CHAIN - 2)})

    def test_directory_limit_equals_the_verifiable_chain_length(self):
        self.assertEqual(256, driver.MAX_CHAIN)
        # With a limit of 2 the chain is full: both members verify and resume, no third may start.
        with mock.patch.object(driver, "MAX_CHAIN", 2):
            driver.verify_batch(self.second / "certificate.json", True)
            driver.ensure_chain_slot(self.second, self.second_run)
            with self.assertRaisesRegex(driver.Refusal, "local chain directory resource limit"):
                driver.ensure_chain_slot(self.chain / "third", self.second_run)
        # With a limit of 1 the second member could never have been created, and is unverifiable.
        with mock.patch.object(driver, "MAX_CHAIN", 1):
            with self.assertRaisesRegex(driver.Refusal, "local chain directory resource limit"):
                driver.ensure_chain_slot(self.chain / "anything", self.second_run)
            with self.assertRaisesRegex(driver.Refusal, "certificate cycle/depth limit"):
                driver.verify_batch(self.second / "certificate.json", True)

    def test_resume_beside_a_certificate_refuses_before_any_scan_or_write(self):
        store = driver.CheckpointStore(self.first, self.first_run)
        (self.first / "certificate.json").rename(self.first / "certificate.moved")
        store.initialize()
        store.write(summary(2, 31))
        (self.first / "certificate.moved").rename(self.first / "certificate.json")
        before = {path.name: path.read_bytes() for path in self.first.iterdir()}
        with mock.patch.object(driver, "consume_native") as scan:
            with self.assertRaisesRegex(driver.Refusal, "already has a final certificate"):
                driver.resume_batch(self.first, True)
            scan.assert_not_called()
        self.assertEqual(before, {path.name: path.read_bytes() for path in self.first.iterdir()})

    def test_resume_requires_complete_and_equal_native_prefix(self):
        (self.second / "certificate.json").unlink()
        store = driver.CheckpointStore(self.second, self.second_run)
        store.initialize()
        store.write(summary(146, 200))
        honest = summary(146, 200)
        lies = []
        for key in ("explicit_t_steps", "explicit_odd_steps", "explicit_standard_steps"):
            lies.append(dict(honest, **{key: str(int(honest[key]) + 1)}))
        lies.append(dict(honest, transcript_digest="1" * 64))
        lies.append(dict(honest, counts=dict(honest["counts"], e2_count="0")))
        lies.append(dict(honest, next_n="199"))
        lies.append(dict(honest, pending=dict(n="200", reason="native_failure", attempted_steps="0",
                                              last_value="200")))
        for index, lie in enumerate(lies):
            before = {path.name: path.read_bytes() for path in self.second.iterdir()}
            with mock.patch.object(driver, "consume_native", return_value=lie) as scan:
                with self.subTest(lie=index), self.assertRaisesRegex(driver.Refusal, "resume native prefix mismatch"):
                    driver.resume_batch(self.second, True)
                scan.assert_called_once_with(146, 200, 100000, 2000000)
            self.assertEqual(before, {path.name: path.read_bytes() for path in self.second.iterdir()})


class FakeChild:
    """Replace the worker with a short Python child so the pipe reader's limits can be reached."""

    def __init__(self, script):
        self.script, self.real, self.started = script, subprocess.Popen, []

    def __call__(self, *args, **kwargs):
        process = self.real([sys.executable, "-c", self.script], **kwargs)
        self.started.append(process)
        return process


class NativeBoundaryTests(unittest.TestCase):
    def scan(self, script, start=2, end=4, **limits):
        child = FakeChild(script)
        patches = [mock.patch.object(driver.subprocess, "Popen", child)]
        patches += [mock.patch.object(driver, name, value) for name, value in limits.items()]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        try:
            return driver.consume_native(start, end, 100000, 2000000, exe=sys.executable)
        finally:
            for patcher in patches:
                patcher.stop()
            self.assertEqual(1, len(child.started))
            self.assertIsNotNone(child.started[0].poll())

    def test_wall_budget_stops_a_silent_worker(self):
        started = time.monotonic()
        with self.assertRaisesRegex(driver.Refusal, "native wall budget"):
            self.scan("import time; time.sleep(60)", NATIVE_WALL_SECONDS=0.4)
        self.assertLess(time.monotonic() - started, 20)

    def test_unterminated_or_flooding_output_refuses(self):
        for script in ("import sys, time; sys.stdout.write('1' * 40000); sys.stdout.flush(); time.sleep(60)",
                       "import sys, time; sys.stderr.write('x' * 40000); sys.stderr.flush(); time.sleep(60)"):
            with self.subTest(stream=script[25:31]), self.assertRaisesRegex(driver.Refusal, "native pipe limit"):
                self.scan(script, NATIVE_WALL_SECONDS=20)

    def test_event_memory_and_extra_frame_limits_refuse(self):
        lines = "import sys; sys.stdout.write('2|E2|0|0|1\\n' * 3); sys.stdout.flush()"
        with self.assertRaisesRegex(driver.Refusal, "extra native frame"):
            self.scan(lines, start=2, end=4)
        with self.assertRaisesRegex(driver.Refusal, "event memory resource limit"):
            self.scan(lines, start=2, end=10, MAX_EVENT_BYTES=20)

    def test_scan_ending_above_the_l1_cap_refuses_before_any_process_starts(self):
        self.assertEqual(10000, driver.NATIVE_L1_CAP)
        for start, end in ((10000, 10001), (9999, 10001), (9000, 10001), (2 ** 71, 2 ** 71 + 1)):
            with mock.patch.object(driver.subprocess, "Popen") as launch:
                with self.subTest(start=start), self.assertRaisesRegex(driver.Refusal, "RUN1 not owner-authorised"):
                    driver.consume_native(start, end, 100000, 2000000, exe=sys.executable)
                launch.assert_not_called()

    def test_last_interval_under_the_l1_cap_is_scanned_by_the_real_worker(self):
        result = driver.consume_native(9999, 10000, 100000, 2000000)
        self.assertEqual(("10000", None), (result["next_n"], result["pending"]))

    def test_driver_gate_needs_full_run1_status_and_then_only_passes_it_on(self):
        # No worker is started here. Under a synthetic RUN1 status the driver would hand
        # the worker the authority environment; that hand-off is observed on a mock.
        # The accepting branch of the worker itself is deliberately not executed in L1.
        with tempfile.TemporaryDirectory(dir=driver.LOCAL, prefix="gate-status-") as scratch:
            path = Path(scratch) / "status.md"
            for text in (L1, RUN1.replace("AUTHORISED", "DENIED"), RUN1.replace("RUN1", "RUN10"),
                         RUN1.replace("AUTHORISED", "AUTHORISED-NOT"), RUN1 + RUN1, ""):
                path.write_bytes(text.encode("utf-8"))
                with mock.patch.object(driver, "status_path", return_value=path), \
                     mock.patch.object(driver.subprocess, "Popen") as launch:
                    with self.subTest(refused=text[:48]), self.assertRaises(driver.Refusal):
                        driver.consume_native(10000, 10001, 100000, 2000000, exe=sys.executable)
                    launch.assert_not_called()
            for text in (RUN1, RUN1.replace("RUN1\n", "RUN1 " + DASH + " synthetic gate fixture\n")):
                path.write_bytes(text.encode("utf-8"))
                stop = RuntimeError("mock: no worker is started in this test")
                with mock.patch.object(driver, "status_path", return_value=path), \
                     mock.patch.object(driver.subprocess, "Popen", side_effect=stop) as launch:
                    with self.subTest(passed=len(text)), self.assertRaises(RuntimeError):
                        driver.consume_native(10000, 10001, 100000, 2000000, exe=sys.executable)
                    environment = launch.call_args.kwargs["env"]
                    self.assertEqual(("RUN1-AUTHORIZED", str(path)),
                                     (environment["CEML_FRONTIER_DRIVER_MODE"],
                                      environment["CEML_FRONTIER_STATUS_PATH"]))
        # Below the cap the driver passes no authority at all, whatever the environment held.
        with mock.patch.dict(driver.os.environ, {"CEML_FRONTIER_DRIVER_MODE": "RUN1-AUTHORIZED",
                                                 "CEML_FRONTIER_STATUS_PATH": "anything"}), \
             mock.patch.object(driver.subprocess, "Popen", side_effect=RuntimeError("mock")) as launch:
            with self.assertRaises(RuntimeError):
                driver.consume_native(2, 146, 100000, 2000000, exe=sys.executable)
            environment = launch.call_args.kwargs["env"]
            self.assertNotIn("CEML_FRONTIER_DRIVER_MODE", environment)
            self.assertNotIn("CEML_FRONTIER_STATUS_PATH", environment)


class L1GateTests(unittest.TestCase):
    GOOD = dict(scope="L1-IMPLEMENTATION-ACCEPTANCE-ONLY", owner_instruction="SIMULATED GATE FIXTURE ONLY",
                entry_main="abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016",
                p2_merge="abd5d5bd0c6bb3a5cfbd1b83d52122b04d324016", authorized_on="2026-10-11")

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-l1-gate-")
        self.addCleanup(self.scratch.cleanup)
        self.local = Path(self.scratch.name)
        self.status = L1
        for name, value in (("LOCAL", self.local), ("status_text", lambda: self.status)):
            patcher = mock.patch.object(driver, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.write(self.GOOD)

    def write(self, value):
        (self.local / "l1_authorization.json").write_bytes(driver.canonical(value))

    def test_exact_phase_and_invocation_evidence_pass(self):
        driver.l1_gate()
        self.status = L1.replace("L1\n", "L1 " + DASH + " OPEN\n").replace("DENIED\n", "DENIED (RUN1 separately gated)\n")
        driver.l1_gate()

    def test_other_phases_and_authorised_science_refuse(self):
        for status in (RUN1, L1.replace("DENIED", "AUTHORISED"), L1.replace("L1\n", "L10\n"),
                       L1.replace("L1\n", "P2\n"), L1 + L1, ""):
            self.status = status
            with self.subTest(status=status[:50]), self.assertRaises(driver.Refusal):
                driver.l1_gate()

    def test_missing_altered_or_noncanonical_evidence_refuses(self):
        for change in (dict(scope="RUN1"), dict(owner_instruction=""), dict(entry_main="0" * 40),
                       dict(p2_merge="0" * 40), dict(extra="yes")):
            self.write(dict(self.GOOD, **change))
            with self.subTest(change=sorted(change)), self.assertRaises(driver.Refusal):
                driver.l1_gate()
        self.write({key: value for key, value in self.GOOD.items() if key != "authorized_on"})
        with self.assertRaises(driver.Refusal):
            driver.l1_gate()
        path = self.local / "l1_authorization.json"
        path.write_bytes(driver.canonical(self.GOOD) + b"\n")
        with self.assertRaises(driver.Refusal):
            driver.l1_gate()
        path.write_bytes(b"[]")
        with self.assertRaises(driver.Refusal):
            driver.l1_gate()
        path.unlink()
        with self.assertRaises((driver.Refusal, OSError)):
            driver.l1_gate()


class SelftestTests(unittest.TestCase):
    def test_selftest_commits_five_fixtures_and_audits_the_two_batch_chain(self):
        # The invocation-evidence gate has its own tests; here it is mocked so the test does
        # not depend on an ignored local file, and the session it creates is removed again.
        folder = driver.LOCAL / "acceptance"
        before = set(folder.iterdir()) if folder.is_dir() else set()
        self.addCleanup(lambda: [shutil.rmtree(path) for path in set(folder.iterdir()) - before])
        with mock.patch.object(driver, "l1_gate") as gate:
            report = driver.selftest()
        gate.assert_called_once_with()
        self.assertEqual(("L1-NONSCIENTIFIC", "fixtures_pass", "CEML-FRONTIER-2", f1_build.build_digest()),
                         (report["scope"], report["status"], report["protocol"], report["native_build_digest"]))
        sizes = {item["fixture"]: item["batch_size"] for item in report["results"]}
        self.assertEqual({"L1-fixture-a": "144", "L1-fixture-successor": "144", "L1-fixture-b": "144",
                          "L1-fixture-c": "96", "L1-fixture-wide": "9600"}, sizes)
        self.assertEqual(("NONSCIENTIFIC_FIXTURE", "2", "2", "290"),
                         (report["ledger"]["status"], report["ledger"]["batches"],
                          report["ledger"]["start"], report["ledger"]["end"]))
        self.assertEqual(report["results"][1]["digest"], report["ledger"]["latest_certificate_digest"])
        json.dumps(report)

    def test_selftest_refuses_outside_the_l1_phase(self):
        with mock.patch.object(driver, "status_text", return_value=RUN1), \
             mock.patch.object(driver, "run_batch") as execute:
            with self.assertRaises(driver.Refusal):
                driver.selftest()
            execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
