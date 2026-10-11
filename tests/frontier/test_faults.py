"""Adversarial record, stream, recovery and immutable-commit acceptance."""

import copy
import hashlib
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
import reference


SNAPSHOT_FILE = ROOT / "config/frontier_snapshot_v2.json"
V1_SNAPSHOT_FILE = ROOT / "config/frontier_snapshot_v1.json"


class CanonicalRecordFaultTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-record-")
        self.path = Path(self.scratch.name) / "snapshot.json"
        self.snapshot = json.loads(SNAPSHOT_FILE.read_bytes())

    def tearDown(self):
        self.scratch.cleanup()

    def load(self, raw):
        self.path.write_bytes(raw)
        return driver.load_record(self.path, "snapshot")

    def test_frozen_canonical_record_and_exact_digest(self):
        raw = SNAPSHOT_FILE.read_bytes()
        self.assertEqual(raw, driver.canonical(self.snapshot))
        self.assertEqual(self.snapshot, self.load(raw))
        self.assertEqual("538d319bad77b58ec3b37d653df3213312e260167ad26861e8870e48b276b729",
                         driver.H("SNAPSHOT", raw))
        self.assertEqual(driver.H("SNAPSHOT", raw), driver.validate_snapshot(self.snapshot))

    def test_frozen_version_1_snapshot_bytes_and_digest_are_preserved(self):
        raw = V1_SNAPSHOT_FILE.read_bytes()
        self.assertEqual(632, len(raw))
        frozen = "a511d6b80fc0ea6c85f3926b065e27acc696449af49cfa675d7c1315e85a2d66"
        self.assertEqual(frozen, hashlib.sha3_256(b"CEML-FRONTIER-1/SNAPSHOT\0" + raw).hexdigest())
        obj, digest, plain = driver.v1_snapshot()
        self.assertEqual((frozen, hashlib.sha3_256(raw).hexdigest()), (digest, plain))
        self.assertEqual(self.snapshot["provenance"],
                         {"kind": "carried_forward_without_new_observation",
                          "source_schema": "CEML-FRONTIER-1-SNAPSHOT",
                          "source_file": "config/frontier_snapshot_v1.json",
                          "source_digest": digest, "source_sha3_256": plain})
        for key in ("observed_at_utc", "published", "operational"):
            self.assertEqual(obj[key], self.snapshot[key])
        # The version-2 domain gives the same bytes a different identity.
        self.assertNotEqual(frozen, driver.H("SNAPSHOT", raw))

    def test_version_1_snapshot_is_never_a_version_2_record(self):
        with self.assertRaises(driver.Refusal):
            self.load(V1_SNAPSHOT_FILE.read_bytes())
        with self.assertRaises(driver.Refusal):
            driver.validate_snapshot(json.loads(V1_SNAPSHOT_FILE.read_bytes()))

    def test_provenance_must_match_the_frozen_version_1_file(self):
        for key, value in (("source_digest", "1" * 64), ("source_sha3_256", "1" * 64),
                           ("kind", "new_observation"), ("source_file", "config/other.json")):
            altered = copy.deepcopy(self.snapshot)
            altered["provenance"][key] = value
            with self.subTest(field=key), self.assertRaises(driver.Refusal):
                driver.validate_snapshot(altered)
        altered = copy.deepcopy(self.snapshot)
        del altered["provenance"]
        with self.assertRaises(driver.Refusal):
            driver.validate_snapshot(altered)
        changed = json.loads(V1_SNAPSHOT_FILE.read_bytes())
        changed["observed_at_utc"] = "2026-10-11T12:38:07Z"
        (Path(self.scratch.name) / "v1.json").write_bytes(driver.canonical(changed))
        with mock.patch.object(driver, "V1_SNAPSHOT_FILE", str(Path(self.scratch.name) / "v1.json")):
            with self.assertRaises(driver.Refusal):
                driver.validate_snapshot(self.snapshot)

    def test_noncanonical_encodings_and_duplicate_members_refuse(self):
        canonical = driver.canonical(self.snapshot)
        cases = [
            canonical + b"\n", b" " + canonical,
            json.dumps(self.snapshot, indent=2).encode("ascii"),
            b"\xef\xbb\xbf" + canonical,
            canonical.replace(b'"research_only":"yes"',
                              b'"research_only":"yes","research_only":"yes"'),
            canonical.replace(b'"yes"', b'"y\\u0065s"'),
            canonical[:-1],
        ]
        for index, raw in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(driver.Refusal):
                self.load(raw)

    def test_missing_unknown_and_nonascii_fields_refuse(self):
        cases = []
        value = copy.deepcopy(self.snapshot)
        del value["research_only"]
        cases.append(value)
        value = copy.deepcopy(self.snapshot)
        value["unrecognised"] = "yes"
        cases.append(value)
        value = copy.deepcopy(self.snapshot)
        value["published"]["source_url"] = "https://example.invalid/\u00e9"
        cases.append(value)
        for index, value in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(driver.Refusal):
                self.load(driver.canonical(value))

    def test_integral_quantities_cannot_be_numbers_floats_or_bad_decimals(self):
        for quantity in (2, 2.0, -2, "-2", "+2", "02", " 2", "2 ", "2.0", "2e1", "", "1" * 8193):
            value = copy.deepcopy(self.snapshot)
            value["published"]["B"] = quantity
            with self.subTest(kind=type(quantity).__name__, length=len(str(quantity))), self.assertRaises(driver.Refusal):
                self.load(driver.canonical(value))

    def test_record_and_nesting_resource_limits_refuse(self):
        with self.assertRaises(driver.Refusal):
            self.load(b" " * (128 * 1024 + 1))
        with self.assertRaises(driver.Refusal):
            self.load(b'{"value":' + b"[" * 1000 + b"0" + b"]" * 1000 + b"}")
        for token in (b"NaN", b"Infinity", b"-Infinity"):
            with self.subTest(token=token), self.assertRaises(driver.Refusal):
                self.load(b'{"value":' + token + b"}")

    def test_shape_supports_protocol_decimal_limit_without_truncating(self):
        value = copy.deepcopy(self.snapshot)
        value["published"]["B"] = "1" * 8192
        driver.validate_shape(value, "snapshot")
        value["published"]["B"] += "1"
        with self.assertRaises(driver.Refusal):
            driver.validate_shape(value, "snapshot")

    def test_local_paths_reject_traversal_urls_and_resolved_network_paths(self):
        for path in ("folder/../snapshot.json", "https://example.invalid/snapshot.json",
                     chr(92) * 2 + "example.invalid" + chr(92) + "share"):
            with self.subTest(kind=path[:6]), self.assertRaises(driver.Refusal):
                driver.local_path(path)
        resolved = Path(chr(92) * 2 + "example.invalid" + chr(92) + "share" + chr(92) + "snapshot.json")
        with mock.patch.object(Path, "resolve", return_value=resolved):
            with self.assertRaises(driver.Refusal):
                driver.local_path(self.path)


class SnapshotArithmeticFaultTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads(SNAPSHOT_FILE.read_bytes())

    def refuse_mutation(self, branch, key, value):
        altered = copy.deepcopy(self.snapshot)
        target = altered if branch is None else altered[branch]
        target[key] = value
        with self.assertRaises(driver.Refusal):
            driver.validate_snapshot(altered)

    def test_baseline_and_work_unit_arithmetic_refuse_changed_values(self):
        for branch, key in (("published", "B"), ("operational", "B"),
                            ("operational", "first_incomplete_end"),
                            ("operational", "first_incomplete_unit"),
                            ("operational", "work_unit_size")):
            with self.subTest(branch=branch, key=key):
                self.refuse_mutation(branch, key, str(int(self.snapshot[branch][key]) + 1))

    def test_headline_cannot_exceed_lowest_incomplete_bound(self):
        self.refuse_mutation("operational", "headline_B", str(int(self.snapshot["operational"]["B"]) + 1))

    def test_assignment_is_not_a_verified_basin(self):
        self.refuse_mutation("operational", "first_unassigned_unit",
                             str(int(self.snapshot["operational"]["first_incomplete_unit"]) - 1))

    def test_actual_calendar_dates_and_times_are_checked(self):
        for value in ("2026-02-30T12:00:00Z", "2026-10-11T24:00:00Z",
                      "2026-13-11T12:00:00Z", "2026-10-11T12:00:60Z"):
            with self.subTest(timestamp=value):
                self.refuse_mutation(None, "observed_at_utc", value)
                self.refuse_mutation("operational", "site_generated_utc", value)
        self.refuse_mutation("published", "publication_date", "2025-02-30")

    def test_source_times_cannot_postdate_snapshot_observation(self):
        self.refuse_mutation("operational", "site_generated_utc", "2026-10-12T00:00:00Z")

    def test_source_urls_are_ascii_https_without_whitespace(self):
        for value in ("http://example.invalid/", "https://example.invalid/ a", "https://example.invalid/\t", "https:///", "https://example.invalid/\\file"):
            with self.subTest(kind=value[:12]):
                self.refuse_mutation("published", "source_url", value)


class EventFaultTests(unittest.TestCase):
    def setUp(self):
        self.frames = list(reference.iter_events(2, 146))

    def check(self, frames, complete=True):
        return driver.checked_events(frames, 2, 146, 100000, 2000000, complete)

    def test_omitted_repeated_extra_and_out_of_order_events_refuse(self):
        cases = [self.frames[1:], self.frames[:31] + self.frames[32:],
                 self.frames + self.frames[-1:], self.frames[:12] + self.frames[11:]]
        altered = self.frames.copy()
        altered[6], altered[7] = altered[7], altered[6]
        cases.append(altered)
        for index, frames in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(driver.Refusal):
                self.check(frames)

    def test_forged_priority_witness_steps_odd_and_first_descent_refuse(self):
        # n=7 first descends at T^7(7)=5 with four odd T steps.
        for frame in (b"7|EXPLICIT|8|4|6\n", b"7|EXPLICIT|9|4|8\n",
                      b"7|EXPLICIT|8|3|5\n", b"7|EXPLICIT|0|0|5\n",
                      b"7|Q4|0|0|5\n", b"7|EXPLICIT|008|4|5\n",
                      b"7|EXPLICIT|8|4|5|extra\n", b"7|EXPLICIT|8|4|5\r\n"):
            altered = self.frames.copy()
            altered[5] = frame
            with self.subTest(frame=frame), self.assertRaises(driver.Refusal):
                self.check(altered)
        for index, frame in ((0, b"2|E2|1|0|1\n"),
                             (9, b"11|P3|0|0|8\n")):
            altered = self.frames.copy()
            altered[index] = frame
            with self.subTest(index=index), self.assertRaises(driver.Refusal):
                self.check(altered)

    def test_truncated_nonascii_and_oversized_event_refuse(self):
        for frame in (self.frames[0][:-1], b"\xff\n", b"1" * 32768 + b"\n"):
            with self.subTest(length=len(frame)), self.assertRaises(driver.Refusal):
                self.check([frame] + self.frames[1:])

    def test_budget_exhaustion_cannot_be_a_successful_event(self):
        with self.assertRaises(driver.Refusal):
            driver.checked_events(self.frames, 2, 146, 1, 2000000)
        with self.assertRaises(driver.Refusal):
            driver.checked_events(self.frames, 2, 146, 100000, 1)

    def test_forged_summary_fields_refuse_independent_prefix_replay(self):
        summary = driver.summary_reference(2, 146, 100000, 2000000)
        for key in ("next_n", "explicit_t_steps", "explicit_odd_steps",
                    "explicit_standard_steps", "explicit_attempts"):
            altered = copy.deepcopy(summary)
            altered[key] = str(int(altered[key]) + 1)
            with self.subTest(field=key), self.assertRaises(driver.Refusal):
                driver.validate_summary(altered, 2, 146, 100000, 2000000)
        for key in reference.COUNT_KEYS:
            altered = copy.deepcopy(summary)
            altered["counts"][key] = str(int(altered["counts"][key]) + 1)
            with self.subTest(field=key), self.assertRaises(driver.Refusal):
                driver.validate_summary(altered, 2, 146, 100000, 2000000)
        summary["transcript_digest"] = "0" * 64
        with self.assertRaises(driver.Refusal):
            driver.validate_summary(summary, 2, 146, 100000, 2000000)

    def test_pending_attempt_is_outside_successful_coverage(self):
        summary = driver.summary_reference(2, 146, 1, 2000000)
        driver.validate_summary(summary, 2, 146, 1, 2000000)
        self.assertEqual("7", summary["next_n"])
        self.assertEqual("7", summary["pending"]["n"])
        self.assertEqual("1", summary["explicit_attempts"])
        self.assertEqual("0", summary["counts"]["explicit_count"])
        self.assertEqual("0", summary["counts"]["unresolved_count"])
        self.assertEqual(5, sum(map(int, summary["counts"].values())))
        for key, value in (("n", "8"), ("last_value", "12"),
                           ("attempted_steps", "0"), ("reason", "unknown")):
            altered = copy.deepcopy(summary)
            altered["pending"][key] = value
            with self.subTest(field=key), self.assertRaises(driver.Refusal):
                driver.validate_summary(altered, 2, 146, 1, 2000000)


class CertificateFaultTests(unittest.TestCase):
    """Transaction simulations with a mocked build, labelled acceptance-only."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-certificate-")
        self.directory = Path(self.scratch.name) / "batch"
        self.run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        driver.prepare_fixture(self.directory, self.run)
        self.build_patch = mock.patch.object(f1_build, "verify_build", return_value={"digest": "0" * 64})
        self.build_patch.start()
        self.complete = driver.summary_reference(2, 146, 100000, 2000000)

    def tearDown(self):
        self.build_patch.stop()
        self.scratch.cleanup()

    def commit(self, summary=None, fault=None):
        return driver.commit_batch(self.directory, self.run,
                                   self.complete if summary is None else summary, True, fault)

    def test_partial_or_pending_summary_cannot_commit(self):
        for summary in (driver.summary_reference(2, 7, 100000, 2000000),
                        driver.summary_reference(2, 146, 1, 2000000)):
            with self.assertRaises(driver.Refusal):
                self.commit(summary)
            self.assertFalse((self.directory / "certificate.json").exists())

    def test_interrupted_certificate_write_never_promotes_temporary(self):
        for fault in driver.FAULT_POINTS[:6]:
            with self.subTest(fault=fault), self.assertRaises(driver.Refusal):
                self.commit(fault=fault)
            self.assertFalse((self.directory / "certificate.json").exists())
        # before_create leaves no temporary; the other five leave one orphan each.
        self.assertEqual(5, len(list(self.directory.glob("certificate.json.*.tmp"))))
        # Orphans are never evidence and never block the real commit.
        self.assertEqual(self.commit(), driver.verify_batch(self.directory / "certificate.json", True))

    def test_exception_after_rename_is_not_a_returned_commit(self):
        for fault in driver.FAULT_POINTS[6:]:
            directory = Path(self.scratch.name) / fault
            driver.prepare_fixture(directory, self.run)
            with self.subTest(fault=fault), self.assertRaises(driver.Refusal):
                driver.commit_batch(directory, self.run, self.complete, True, fault)
            # Revalidation may recover this immutable file; the failed call did not
            # return COMMITTED or create any descendant.
            cert = driver.verify_batch(directory / "certificate.json", True)
            self.assertEqual(self.complete["transcript_digest"], cert["independent_replay_digest"])
            with self.assertRaises((driver.Refusal, OSError)):
                driver.commit_batch(directory, self.run, self.complete, True)

    def test_immutable_certificate_cannot_be_replaced_even_by_same_result(self):
        cert = self.commit()
        original = (self.directory / "certificate.json").read_bytes()
        with self.assertRaises((driver.Refusal, OSError)):
            self.commit()
        self.assertEqual(original, (self.directory / "certificate.json").read_bytes())
        self.assertEqual(cert, driver.verify_batch(self.directory / "certificate.json", True))

    def test_valid_hash_is_insufficient_without_fresh_full_replay(self):
        cert = self.commit()
        for key, value in (("transcript_digest", "1" * 64),
                           ("independent_replay_digest", "1" * 64),
                           ("explicit_t_steps", str(int(cert["explicit_t_steps"]) + 1)),
                           ("checker_source_digest", "1" * 64)):
            changed = copy.deepcopy(cert)
            changed[key] = value
            (self.directory / "certificate.json").write_bytes(driver.canonical(driver.seal(changed, "CERTIFICATE")))
            with self.subTest(field=key), self.assertRaises(driver.Refusal):
                driver.verify_batch(self.directory / "certificate.json", True)

    def test_changed_build_snapshot_and_missing_fixture_marker_refuse(self):
        self.commit()
        with mock.patch.object(f1_build, "verify_build", return_value={"digest": "1" * 64}):
            with self.assertRaises(driver.Refusal):
                driver.verify_batch(self.directory / "certificate.json", True)
        snapshot = json.loads((self.directory / "snapshot.json").read_bytes())
        snapshot["observed_at_utc"] = "2026-10-11T12:38:07Z"
        (self.directory / "snapshot.json").write_bytes(driver.canonical(snapshot))
        with self.assertRaises(driver.Refusal):
            driver.verify_batch(self.directory / "certificate.json", True)
        (self.directory / "snapshot.json").write_bytes(V1_SNAPSHOT_FILE.read_bytes())
        with self.assertRaises(driver.Refusal):
            driver.verify_batch(self.directory / "certificate.json", True)
        (self.directory / "snapshot.json").write_bytes(SNAPSHOT_FILE.read_bytes())
        driver.verify_batch(self.directory / "certificate.json", True)
        (self.directory / "acceptance.json").unlink()
        with self.assertRaises((driver.Refusal, OSError)):
            driver.verify_batch(self.directory / "certificate.json", True)

    def test_corrupt_existing_final_filename_is_never_auto_repaired(self):
        path = self.directory / "certificate.json"
        path.write_bytes(b"torn")
        with self.assertRaises((driver.Refusal, OSError)):
            self.commit()
        self.assertEqual(b"torn", path.read_bytes())


class Run1AuthorityGateTests(unittest.TestCase):
    """Only simulate high-bit record binding; never run or replay its interval."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="ceml-frontier-run1-gate-")
        self.root = Path(self.scratch.name)
        self.local = self.root / "local"
        self.local.mkdir()
        self.snapshot = driver.snapshot()
        self.run = driver.fixture_run("L1-fixture-a", build_digest="0" * 64)
        base = self.snapshot["published"]["B"]
        self.run.update(run_id="RUN1-gate-simulation", run1_authority_id="RUN1-owner-test",
                        base_B=base, batch_start=base, batch_end=str(int(base) + 144),
                        accepted_assumption_ack=self.run["snapshot_digest"] + ":published:" + base)
        self.run["predecessor_digest"] = driver.genesis(self.run)
        driver.validate_manifest(self.run, self.snapshot)
        self.evidence = {"authority_id": self.run["run1_authority_id"],
                         **{key: self.run[key] for key in ("snapshot_digest", "base_kind", "base_B",
                                "accepted_assumption_ack", "batch_start", "batch_end")},
                         "owner_instruction": "SIMULATED ACCEPTANCE GATE ONLY"}
        self.write_status()
        self.write_evidence()
        self.root_patch = mock.patch.object(driver, "status_path", return_value=self.root / "PROGRAM_STATUS.md")
        self.local_patch = mock.patch.object(driver, "LOCAL", self.local)
        self.root_patch.start()
        self.local_patch.start()

    def tearDown(self):
        self.local_patch.stop()
        self.root_patch.stop()
        self.scratch.cleanup()

    def write_status(self, phase="RUN1", authorization="AUTHORISED"):
        (self.root / "PROGRAM_STATUS.md").write_text(
            "**Authoritative current phase:** " + phase + "\n"
            "**Scientific execution authorization:** " + authorization + "\n", encoding="ascii")

    def write_evidence(self, value=None):
        (self.local / "run1_authorization.json").write_bytes(driver.canonical(self.evidence if value is None else value))

    def test_exact_owner_phase_and_acknowledgement_gate_binding(self):
        driver.run1_gate(self.run)
        self.assertFalse((self.local / "certificate.json").exists())

    def test_lookalike_or_denied_status_cannot_authorize(self):
        for phase, authorization in (("RUN10", "AUTHORISED"), ("L1", "AUTHORISED"),
                                     ("RUN1", "DENIED"), ("RUN1", "AUTHORISED-NOT")):
            self.write_status(phase, authorization)
            with self.subTest(phase=phase, authorization=authorization), self.assertRaises(driver.Refusal):
                driver.run1_gate(self.run)

    def test_missing_and_noncanonical_evidence_refuse(self):
        path = self.local / "run1_authorization.json"
        path.unlink()
        with self.assertRaises((driver.Refusal, OSError)):
            driver.run1_gate(self.run)
        self.write_evidence()
        path.write_bytes(path.read_bytes() + b"\n")
        with self.assertRaises(driver.Refusal):
            driver.run1_gate(self.run)

    def test_wrong_owner_acknowledgement_base_or_interval_refuse(self):
        for key, value in (("authority_id", "wrong"), ("owner_instruction", ""),
                           ("owner_instruction", "   "), ("owner_instruction", {"nested": "yes"}),
                           ("owner_instruction", None), ("authority_id", None),
                           ("accepted_assumption_ack", "wrong"), ("snapshot_digest", "1" * 64),
                           ("base_kind", "operational"), ("base_B", "2"),
                           ("batch_end", str(int(self.run["batch_end"]) + 144))):
            altered = copy.deepcopy(self.evidence)
            altered[key] = value
            self.write_evidence(altered)
            with self.subTest(field=key), self.assertRaises(driver.Refusal):
                driver.run1_gate(self.run)

    def test_scientific_first_batch_width_is_part_of_manifest_validity(self):
        # The rule binds verification and the ledger too, not only the execution gate.
        driver.validate_manifest(self.run, self.snapshot)
        for width in (1, 143, 145, 14400):
            run = copy.deepcopy(self.run)
            run["batch_end"] = str(int(run["batch_start"]) + width)
            with self.subTest(width=width), self.assertRaisesRegex(driver.Refusal, "exactly 144 starts"):
                driver.validate_manifest(run, self.snapshot)
        later = copy.deepcopy(self.run)
        later.update(batch_start=self.run["batch_end"], batch_end=str(int(self.run["batch_end"]) + 288),
                     predecessor_digest="a" * 64)
        driver.validate_manifest(later, self.snapshot)

    def test_initial_pilot_is_exactly_one_144_start_interval(self):
        for width in (1, 143, 145, 14400):
            run = copy.deepcopy(self.run)
            run["batch_end"] = str(int(run["batch_start"]) + width)
            evidence = copy.deepcopy(self.evidence)
            evidence["batch_end"] = run["batch_end"]
            self.write_evidence(evidence)
            with self.subTest(width=width), self.assertRaises(driver.Refusal):
                driver.run1_gate(run)


if __name__ == "__main__":
    unittest.main()
