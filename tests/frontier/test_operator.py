"""Operator-package commands on synthetic gates and small fixtures only.

Nothing here scans, replays or certifies a frontier integer. High-bit values
appear only as record fields while every execution path is mocked or refused.
"""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "frontier"))
import ceml_frontier as driver
import f1_build

RUN1 = "**Authoritative current phase:** RUN1\n**Scientific execution authorization:** AUTHORISED\n"
L1 = "**Authoritative current phase:** L1\n**Scientific execution authorization:** DENIED\n"
INSTRUCTION = "SIMULATED ACCEPTANCE GATE ONLY"


class SyntheticGate(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-operator-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.local = self.root / "local"
        self.local.mkdir()
        self.status = RUN1
        self.snapshot = driver.snapshot()
        self.digest = driver.validate_snapshot(self.snapshot)
        self.base = self.snapshot["published"]["B"]
        self.end = str(int(self.base) + 144)
        self.ack = self.digest + ":published:" + self.base
        self.scan = mock.Mock(side_effect=AssertionError("no native scan in a synthetic gate test"))
        for target, name, value in ((driver, "LOCAL", self.local),
                                    (driver, "status_text", lambda: self.status),
                                    (driver, "consume_native", self.scan),
                                    (f1_build, "verify_build", lambda *a, **k: {"digest": "0" * 64})):
            patcher = mock.patch.object(target, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def authority(self, **changes):
        values = dict(authority_id="RUN1-synthetic", base_kind="published", batch_start=self.base,
                      batch_end=self.end, acknowledge=self.ack, owner_instruction=INSTRUCTION)
        values.update(changes)
        return driver.prepare_authority(**values)

    def manifest(self, name="manifest.json", **changes):
        values = dict(out=self.root / name, authority_id="RUN1-synthetic", acknowledge=self.ack,
                      max_t="100000", max_total="2000000", run_id="RUN1-synthetic-chain", base_kind="published")
        values.update(changes)
        return driver.prepare_manifest(**values)


class AuthorityTests(SyntheticGate):
    def test_acknowledgement_is_exactly_snapshot_digest_kind_and_bound(self):
        for kind in ("published", "operational"):
            snap, digest, expected = driver.expected_acknowledgement(kind)
            self.assertEqual(digest + ":" + kind + ":" + snap[kind]["B"], expected)
        self.assertEqual(self.ack, driver.expected_acknowledgement("published")[2])
        with self.assertRaises(driver.Refusal):
            driver.expected_acknowledgement("headline")

    def test_authority_record_is_canonical_and_covers_exactly_one_batch(self):
        report = self.authority()
        self.assertEqual("AUTHORITY_RECORDED_NOT_EXECUTED", report["status"])
        raw = (self.local / "run1_authorization.json").read_bytes()
        record = driver.parse_bytes(raw)
        self.assertEqual(set(driver.AUTHORITY_KEYS), set(record))
        self.assertEqual((self.ack, self.base, self.end, INSTRUCTION),
                         (record["accepted_assumption_ack"], record["batch_start"],
                          record["batch_end"], record["owner_instruction"]))
        # A later batch needs its own record; the old one is replaced, not extended.
        later = str(int(self.end) + 144)
        self.authority(batch_start=self.end, batch_end=later)
        record = driver.parse_bytes((self.local / "run1_authorization.json").read_bytes())
        self.assertEqual((self.end, later), (record["batch_start"], record["batch_end"]))

    def test_authority_refuses_everything_but_an_explicit_exact_acknowledgement(self):
        operational = driver.expected_acknowledgement("operational")[2]
        cases = (dict(acknowledge=""), dict(acknowledge=operational), dict(acknowledge=self.ack + " "),
                 dict(acknowledge="1" * 64 + ":published:" + self.base), dict(base_kind="headline"),
                 dict(authority_id="L1-NONSCIENTIFIC"), dict(authority_id="has space"),
                 dict(owner_instruction=""), dict(owner_instruction="   "),
                 dict(owner_instruction="caf" + chr(233)), dict(batch_end=str(int(self.base) + 143)),
                 dict(batch_end=str(int(self.base) + 14400)), dict(batch_start=str(int(self.base) - 1)),
                 dict(batch_start="0" + self.base), dict(batch_end=self.base),
                 dict(batch_start=self.end, batch_end=str(int(self.end) + 14401)))
        for case in cases:
            with self.subTest(case=sorted(case)), self.assertRaises(driver.Refusal):
                self.authority(**case)
            self.assertFalse((self.local / "run1_authorization.json").exists())

    def test_authority_and_manifest_refuse_outside_run1_status(self):
        for status in (L1, RUN1.replace("AUTHORISED", "DENIED"), RUN1.replace("RUN1", "RUN10"),
                       RUN1.replace("AUTHORISED", "AUTHORISED-NOT"), RUN1 + RUN1, ""):
            self.status = status
            with self.subTest(status=status[:60]):
                with self.assertRaises(driver.Refusal):
                    self.authority()
                with self.assertRaises(driver.Refusal):
                    self.manifest()
                self.assertEqual([], list(self.local.iterdir()))
                self.assertFalse((self.root / "manifest.json").exists())


class ManifestTests(SyntheticGate):
    def test_first_manifest_is_canonical_rooted_and_covered_by_its_authority(self):
        report = self.manifest()
        self.assertEqual(("MANIFEST_WRITTEN_NOT_EXECUTED", self.base, self.end),
                         (report["status"], report["batch_start"], report["batch_end"]))
        run = driver.load_record(self.root / "manifest.json", "run")
        self.assertEqual(driver.genesis(run), run["predecessor_digest"])
        self.assertEqual(report["run_digest"], driver.H("RUN", driver.canonical(run)))
        self.assertEqual(("CEML-FRONTIER-2-RUN", self.ack, "0" * 64),
                         (run["schema"], run["accepted_assumption_ack"], run["native_build_digest"]))
        driver.validate_manifest(run, self.snapshot)
        with self.assertRaises((driver.Refusal, OSError)):
            driver.run1_gate(run)
        self.authority()
        self.assertEqual((self.local / "run1_authorization.json").read_bytes(), driver.run1_gate(run))
        self.scan.assert_not_called()

    def test_manifest_never_replaces_a_file_and_refuses_bad_requests(self):
        self.manifest()
        frozen = (self.root / "manifest.json").read_bytes()
        with self.assertRaises((driver.Refusal, OSError)):
            self.manifest()
        self.assertEqual(frozen, (self.root / "manifest.json").read_bytes())
        operational = driver.expected_acknowledgement("operational")[2]
        cases = (dict(acknowledge=operational), dict(acknowledge=""), dict(width="143"), dict(width="14400"),
                 dict(run_id=None), dict(base_kind=None), dict(authority_id="L1-NONSCIENTIFIC"),
                 dict(max_t="0"), dict(max_t="100001"), dict(max_total="2000001"), dict(max_t="1e5"),
                 dict(run_id="bad id"))
        for index, case in enumerate(cases):
            name = f"refused-{index}.json"
            with self.subTest(case=sorted(case)), self.assertRaises(driver.Refusal):
                self.manifest(name, **case)
            self.assertFalse((self.root / name).exists())

    def prior(self, **changes):
        value = dict(run_id="RUN1-synthetic-chain", base_kind="published", snapshot_digest=self.digest,
                     native_build_digest="0" * 64, batch_end=self.end, digest="a" * 64)
        value.update(changes)
        return value

    def test_continuation_inherits_identity_from_a_verified_predecessor(self):
        with mock.patch.object(driver, "verify_batch", return_value=self.prior()) as verify:
            report = self.manifest("next.json", run_id=None, base_kind=None,
                                   after_certificate="previous/certificate.json", width="288")
            verify.assert_called_once_with("previous/certificate.json")
        run = driver.load_record(self.root / "next.json", "run")
        self.assertEqual((self.end, str(int(self.end) + 288), "a" * 64, "RUN1-synthetic-chain", self.base),
                         (run["batch_start"], run["batch_end"], run["predecessor_digest"],
                          run["run_id"], run["base_B"]))
        self.assertEqual(report["predecessor_digest"], "a" * 64)
        driver.validate_manifest(run, self.snapshot)

    def test_continuation_refuses_identity_drift_overrides_and_bad_widths(self):
        cases = ((self.prior(snapshot_digest="1" * 64), {}), (self.prior(native_build_digest="1" * 64), {}),
                 (self.prior(), dict(run_id="other-chain")), (self.prior(), dict(base_kind="published")),
                 (self.prior(), dict(width="0")), (self.prior(), dict(width="14401")),
                 (self.prior(), dict(width="0144")),
                 (self.prior(base_kind="operational"), {}))
        for index, (prior, overrides) in enumerate(cases):
            arguments = dict(run_id=None, base_kind=None, after_certificate="previous/certificate.json")
            arguments.update(overrides)
            name = f"drift-{index}.json"
            with mock.patch.object(driver, "verify_batch", return_value=prior):
                with self.subTest(case=index), self.assertRaises(driver.Refusal):
                    self.manifest(name, **arguments)
            self.assertFalse((self.root / name).exists())

    def test_unverifiable_predecessor_blocks_a_continuation_manifest(self):
        with mock.patch.object(driver, "verify_batch", side_effect=driver.Refusal("missing predecessor")):
            with self.assertRaises(driver.Refusal):
                self.manifest("next.json", run_id=None, base_kind=None, after_certificate="x/certificate.json")
        self.assertFalse((self.root / "next.json").exists())


class StartBatchGateTests(SyntheticGate):
    """start_batch with run_batch mocked: gates and recorded evidence, never a scan."""

    def setUp(self):
        super().setUp()
        self.manifest()
        self.authority()
        self.chain = self.root / "chain"
        patcher = mock.patch.object(driver, "run_batch", return_value={"status": "MOCKED-NOT-EXECUTED"})
        self.execute = patcher.start()
        self.addCleanup(patcher.stop)

    def start(self, name="batch-0001"):
        return driver.start_batch(self.root / "manifest.json", self.chain / name)

    def test_gates_pass_then_evidence_is_recorded_before_execution(self):
        self.assertEqual({"status": "MOCKED-NOT-EXECUTED"}, self.start())
        directory = self.chain / "batch-0001"
        self.assertEqual(["authority.json", "run.json", "snapshot.json"],
                         sorted(path.name for path in directory.iterdir()))
        self.assertEqual((self.local / "run1_authorization.json").read_bytes(),
                         (directory / "authority.json").read_bytes())
        self.assertEqual((self.root / "manifest.json").read_bytes(), (directory / "run.json").read_bytes())
        self.assertEqual((ROOT / "config/frontier_snapshot_v2.json").read_bytes(),
                         (directory / "snapshot.json").read_bytes())
        run = driver.load_record(directory / "run.json", "run")
        self.execute.assert_called_once_with(directory.resolve(), run)
        self.scan.assert_not_called()

    def test_every_refusal_happens_before_any_directory_exists(self):
        def no_authority():
            (self.local / "run1_authorization.json").unlink()
        def other_batch():
            self.authority(batch_start=self.end, batch_end=str(int(self.end) + 144))
        def other_authority():
            self.authority(authority_id="RUN1-someone-else")
        def phase_l1():
            self.status = L1
        def science_denied():
            self.status = RUN1.replace("AUTHORISED", "DENIED")
        def noncanonical_authority():
            path = self.local / "run1_authorization.json"
            path.write_bytes(path.read_bytes() + b"\n")
        def changed_manifest():
            run = json.loads((self.root / "manifest.json").read_bytes())
            run["batch_end"] = str(int(run["batch_end"]) + 1)
            (self.root / "manifest.json").write_bytes(driver.canonical(run))
        def fixture_authority():
            run = json.loads((self.root / "manifest.json").read_bytes())
            run["run1_authority_id"] = "L1-NONSCIENTIFIC"
            (self.root / "manifest.json").write_bytes(driver.canonical(run))
        for spoil in (no_authority, other_batch, other_authority, phase_l1, science_denied,
                      noncanonical_authority, changed_manifest, fixture_authority):
            original = {path: path.read_bytes() for path in (self.root / "manifest.json",
                                                             self.local / "run1_authorization.json")}
            spoil()
            with self.subTest(case=spoil.__name__):
                with self.assertRaises((driver.Refusal, OSError)):
                    self.start()
                self.assertFalse(self.chain.exists())
                self.execute.assert_not_called()
            self.status = RUN1
            for path, data in original.items():
                path.write_bytes(data)

    def test_stale_build_or_broken_predecessor_refuses_before_any_directory_exists(self):
        with mock.patch.object(f1_build, "verify_build", return_value={"digest": "1" * 64}):
            with self.assertRaisesRegex(driver.Refusal, "native build identity mismatch"):
                self.start()
        self.assertFalse(self.chain.exists())
        with mock.patch.object(driver, "predecessor", side_effect=driver.Refusal("missing predecessor")):
            with self.assertRaisesRegex(driver.Refusal, "missing predecessor"):
                self.start()
        self.assertFalse(self.chain.exists())
        self.execute.assert_not_called()

    def test_existing_directory_and_second_active_batch_refuse(self):
        self.start()
        with self.assertRaises(driver.Refusal):
            self.start()
        # The first batch has no certificate, so the chain has one active batch already.
        with self.assertRaises(driver.Refusal):
            self.start("batch-0001-again")
        self.assertFalse((self.chain / "batch-0001-again").exists())
        self.assertEqual(1, self.execute.call_count)

    def test_uncommitted_attempt_moved_out_of_the_chain_allows_an_identical_restart(self):
        self.start()
        quarantine = self.root / "quarantine"
        quarantine.mkdir()
        (self.chain / "batch-0001").rename(quarantine / "batch-0001")
        self.start("batch-0001-retry")
        self.assertEqual((quarantine / "batch-0001" / "run.json").read_bytes(),
                         (self.chain / "batch-0001-retry" / "run.json").read_bytes())
        self.assertEqual(2, self.execute.call_count)


class CliOnFixtureTests(unittest.TestCase):
    """The documented read-only commands, end to end, on a committed two-batch fixture chain."""

    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory(dir=driver.LOCAL, prefix="operator-tests-")
        cls.chain = Path(cls.folder.name) / "chain"
        first_run = driver.fixture_run("L1-fixture-a")
        cls.first = cls.chain / "batch-0001"
        driver.prepare_fixture(cls.first, first_run)
        cls.first_digest = driver.run_batch(cls.first, first_run, True)["digest"]
        second_run = driver.fixture_run("L1-fixture-successor")
        second_run["predecessor_digest"] = cls.first_digest
        cls.second = cls.chain / "batch-0002"
        driver.prepare_fixture(cls.second, second_run)
        cls.second_digest = driver.run_batch(cls.second, second_run, True)["digest"]
        cls.genesis = driver.genesis(first_run)

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def cli(self, *arguments):
        result = subprocess.run([sys.executable, str(ROOT / "tools/frontier/ceml_frontier.py"), *arguments],
                                cwd=ROOT, capture_output=True, timeout=120)
        return result.returncode, json.loads(result.stdout)

    def test_inspect_replay_verify_and_ledger_report_the_fixture_chain(self):
        before = {path: path.read_bytes() for path in self.chain.rglob("*") if path.is_file()}
        code, report = self.cli("inspect", "--batch-dir", str(self.second))
        self.assertEqual((0, "INSPECTION_ONLY", "RECOVERABLE", "1", "290", "PRESENT-UNVERIFIED"),
                         (code, report["status"], report["recovery"]["status"],
                          report["recovery"]["generation"], report["recovery"]["next_n"], report["certificate"]))
        code, report = self.cli("replay", "--batch-dir", str(self.second))
        self.assertEqual((0, "REFERENCE_REPLAY_MATCH", self.second_digest),
                         (code, report["status"], report["digest"]))
        code, report = self.cli("verify-batch", "--certificate", str(self.second / "certificate.json"))
        self.assertEqual((0, "NONSCIENTIFIC_FIXTURE", self.second_digest, "146", "290"),
                         (code, report["status"], report["digest"], report["batch_start"], report["batch_end"]))
        code, report = self.cli("ledger", "--dir", str(self.chain))
        self.assertEqual((0, "NONSCIENTIFIC_FIXTURE", "2", "2", "290", self.genesis, self.second_digest),
                         (code, report["status"], report["batches"], report["start"], report["end"],
                          report["genesis_digest"], report["latest_certificate_digest"]))
        self.assertEqual(before, {path: path.read_bytes() for path in self.chain.rglob("*") if path.is_file()})

    def test_cli_resume_and_pilot_stay_refused_for_fixtures_in_l1(self):
        code, report = self.cli("resume", "--batch-dir", str(self.second))
        self.assertEqual((2, "RUN1 not owner-authorised"), (code, report["reason"]))
        with tempfile.TemporaryDirectory(dir=driver.LOCAL, prefix="operator-pilot-") as scratch:
            out = Path(scratch) / "out"
            code, report = self.cli("pilot", "--manifest", str(self.second / "run.json"), "--out", str(out))
            self.assertEqual((2, "RUN1 not owner-authorised"), (code, report["reason"]))
            self.assertFalse(out.exists())

    def test_damaged_chain_member_is_reported_and_blocks_the_ledger(self):
        with tempfile.TemporaryDirectory(dir=driver.LOCAL, prefix="operator-damaged-") as scratch:
            import shutil
            chain = Path(scratch) / "chain"
            shutil.copytree(self.chain, chain)
            certificate = json.loads((chain / "batch-0001" / "certificate.json").read_bytes())
            forged = copy.deepcopy(certificate)
            forged["explicit_t_steps"] = str(int(forged["explicit_t_steps"]) + 1)
            (chain / "batch-0001" / "certificate.json").write_bytes(
                driver.canonical(driver.seal(forged, "CERTIFICATE")))
            for arguments in (("ledger", "--dir", str(chain)),
                              ("verify-batch", "--certificate", str(chain / "batch-0002" / "certificate.json")),
                              ("replay", "--batch-dir", str(chain / "batch-0001"))):
                code, report = self.cli(*arguments)
                with self.subTest(command=arguments[0]):
                    self.assertEqual((2, "REFUSED"), (code, report["status"]))


if __name__ == "__main__":
    unittest.main()
