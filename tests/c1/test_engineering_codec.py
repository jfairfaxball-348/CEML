"""Bounded developer checks for engineering framing/vector; not CEML-V1."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.c1 import engineering_codec as codec


class EngineeringCodecTests(unittest.TestCase):
    def test_frozen_generator_vector(self):
        result = codec.self_test_vector()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["represented_shortcut_steps"], "0")
        self.assertEqual(result["input_digest"], "84b55262e1b0543c0201479122d92f19cf8ab38550db60a3075c5564b3b7fc0a")
        self.assertEqual(result["initial_state_digest"], "95eef319edc55bd8a1aa5f9f210fea3f3b9bae480913f7ae1af9bc59332e6271")

    def test_minimal_unsigned_framing(self):
        vectors = {
            0: "000000000000000100", 1: "000000000000000101",
            255: "0000000000000001ff", 256: "00000000000000020100",
        }
        for value, encoded in vectors.items():
            with self.subTest(value=value):
                self.assertEqual(codec.uenc(value), bytes.fromhex(encoded))
                self.assertEqual(codec.decode_uenc(bytes.fromhex(encoded)), value)
        self.assertEqual(codec.blob(b""), b"\0" * 8)
        self.assertEqual(codec.blob(b"ab"), bytes.fromhex("0000000000000002") + b"ab")
        self.assertEqual(codec.u64be(2**64 - 1), b"\xff" * 8)

    def test_framing_refuses_noncanonical_input(self):
        for value in (-1, True, 1.0, "1"):
            with self.subTest(value=value), self.assertRaises(codec.CodecRefusal):
                codec.uenc(value)
        for encoded in (b"", b"\0" * 8, bytes.fromhex("00000000000000020001"),
                        bytes.fromhex("000000000000000201"), bytes.fromhex("00000000000000010100")):
            with self.subTest(encoded=encoded), self.assertRaises(codec.CodecRefusal):
                codec.decode_uenc(encoded)
        with self.assertRaises(codec.CodecRefusal):
            codec.u64be(2**64)
        with self.assertRaises(codec.CodecRefusal):
            codec.blob(bytearray(b"a"))

    def test_ascii_canonical_subset(self):
        obj = {"z": [True, False, None, "0"], "a": ''.join(map(chr, [34, 92, 8, 9, 10, 12, 13, 0, 47, 127]))}
        expected = bytes.fromhex(
            '7b2261223a225c225c5c5c625c745c6e5c665c725c75303030302f7f'
            '222c227a223a5b747275652c66616c73652c6e756c6c2c2230225d7d')
        self.assertEqual(codec.canonical_bytes(obj), expected)
        shared = ["allowed"]
        self.assertEqual(codec.canonical_bytes([shared, shared]), b'[["allowed"],["allowed"]]')

    def test_canonical_subset_refuses_unsupported_values(self):
        unsupported = [0, 1.0, float("nan"), float("inf"), b"ascii", ("tuple",),
                       {1: "key"}, {"a": "\u00e9"}, {"\u00e9": "a"}, {"a": "\ud800"}]
        for obj in unsupported:
            with self.subTest(kind=type(obj).__name__), self.assertRaises(codec.CodecRefusal):
                codec.canonical_bytes(obj)
        cycle = []
        cycle.append(cycle)
        with self.assertRaises(codec.CodecRefusal):
            codec.canonical_bytes(cycle)

    def test_canonical_decimal(self):
        for value in ("0", "1", "256", "9" * 5000):
            self.assertEqual(codec.canonical_decimal(value), value)
        for value in ("", "01", "+1", "-1", "1.0", "1e2", " 1", "1\n", "\u0661", 1, True):
            with self.subTest(value_type=type(value).__name__), self.assertRaises(codec.CodecRefusal):
                codec.canonical_decimal(value)

    def test_artifact_domain_framing_and_top_level_omission(self):
        obj = {"schema_version": "TEST-1", "nested": {"artifact_digest": "kept"}, "artifact_digest": "omitted"}
        body = b'{"nested":{"artifact_digest":"kept"},"schema_version":"TEST-1"}'
        preimage = (b"CEML-I1-ENGINEERING-ARTIFACT-V1\0" + b"\0" * 7 + b"\x06TEST-1"
                    + len(body).to_bytes(8, "big") + body)
        self.assertEqual(codec.artifact_digest(obj), hashlib.sha3_256(preimage).hexdigest())
        obj["artifact_digest"] = "changed"
        self.assertEqual(codec.artifact_digest(obj), hashlib.sha3_256(preimage).hexdigest())
        self.assertEqual(obj["artifact_digest"], "changed")
        for bad in ({}, {"schema_version": ""}, {"schema_version": "TEST-1", "build_digest": "x"},
                    {"schema_version": "TEST-1", "machine_profile_digest": "x"}):
            with self.subTest(keys=list(bad)), self.assertRaises(codec.CodecRefusal):
                codec.artifact_digest(bad)

    def test_vector_refuses_changed_workload_before_generating(self):
        source = Path(__file__).resolve().parents[2] / "config/calibration_suite_v1.json"
        suite = json.loads(source.read_text(encoding="utf-8"))
        suite["generator_test_vector"]["size_bits"] = "1024"
        with tempfile.TemporaryDirectory(prefix="ceml-cal-codec-") as directory:
            fixture = Path(directory) / "suite.json"
            fixture.write_text(json.dumps(suite), encoding="utf-8")
            with patch.object(codec.hashlib, "shake_256", side_effect=AssertionError("unexpected generation")):
                with self.assertRaises(codec.CodecRefusal):
                    codec.self_test_vector(fixture)

    def test_vector_rejects_wrong_digest_and_duplicate_keys(self):
        source = Path(__file__).resolve().parents[2] / "config/calibration_suite_v1.json"
        suite = json.loads(source.read_text(encoding="utf-8"))
        suite["generator_test_vector"]["input_digest"] = "0" * 64
        with tempfile.TemporaryDirectory(prefix="ceml-cal-codec-") as directory:
            fixture = Path(directory) / "suite.json"
            fixture.write_text(json.dumps(suite), encoding="utf-8")
            with self.assertRaises(codec.CodecRefusal):
                codec.self_test_vector(fixture)
            fixture.write_text('{"suite_version":"CEML-CAL-1","suite_version":"CEML-CAL-1"}', encoding="utf-8")
            with self.assertRaises(codec.CodecRefusal):
                codec.self_test_vector(fixture)


if __name__ == "__main__":
    unittest.main()
