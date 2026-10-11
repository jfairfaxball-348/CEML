"""Bounded build-integrity and native refusal fixtures; no science."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"tools/frontier"))
import f1_build as build


class BuildIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dependency = build.dependency_check()
        cls.raw_manifest = (build.BUILD/build.MANIFEST_NAME).read_bytes()
        cls.manifest = json.loads(cls.raw_manifest)

    def altered_manifest(self, edit):
        value = copy.deepcopy(self.manifest)
        edit(value)
        value.pop("digest", None)
        value["digest"] = build.domain_hash("BUILD", build.canonical(value))
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            folder = Path(directory)
            (folder/build.MANIFEST_NAME).write_bytes(build.canonical(value))
            with mock.patch.object(build, "BUILD", folder), mock.patch.object(build, "dependency_check", return_value=self.dependency):
                with self.assertRaises(build.Refusal):
                    build.verify_build()

    def test_current_manifest_and_inputs_match(self):
        with mock.patch.object(build, "dependency_check", return_value=self.dependency):
            value = build.verify_build()
        self.assertEqual(value["digest"], self.manifest["digest"])
        self.assertEqual(value["table_text"].encode("ascii"), build.table_bytes())
        self.assertIn("tools/c1/gmp_smoke.c", value["inputs"])
        self.assertIn("tests/frontier/test_build.py", value["inputs"])
        self.assertEqual("CEML-FRONTIER-2-BUILD", value["schema"])
        for name in ("config/frontier_snapshot_v1.json", "config/frontier_snapshot_v2.json",
                     "docs/FRONTIER_PROTOCOL_V1.md", "docs/FRONTIER_PROTOCOL_V2.md",
                     "tests/frontier/test_recovery.py", "tests/frontier/test_operator.py"):
            self.assertIn(name, value["inputs"])
        schemas = sorted(name for name in value["inputs"] if name.startswith("schemas/"))
        self.assertEqual(sorted(f"schemas/frontier_{kind}_v{version}.schema.json" for version in (1, 2)
                                for kind in ("snapshot", "run", "checkpoint", "certificate")), schemas)

    def test_identity_is_line_ending_independent_but_content_sensitive(self):
        CR, LF = bytes([13]), bytes([10])
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            root = Path(directory)
            names = build.input_paths()
            def identity(transform):
                for name in names:
                    target = root/name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(transform(name, (ROOT/name).read_bytes().replace(CR + LF, LF)))
                with mock.patch.object(build, "ROOT", root), mock.patch.object(build, "input_paths", return_value=names):
                    return build.inputs()
            plain = identity(lambda name, raw: raw)
            windows = identity(lambda name, raw: raw.replace(LF, CR + LF))
            self.assertEqual(plain, windows)
            self.assertEqual(plain, build.inputs())
            self.assertEqual({"lf"}, set(plain["src/frontier_worker.c"]))
            edited = identity(lambda name, raw: raw + b" " if name == "docs/FRONTIER_PROTOCOL_V2.md" else raw)
            self.assertNotEqual(plain, edited)

    def test_unexpected_or_missing_frontier_schema_refuses(self):
        real = build.ROOT
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            root = Path(directory)
            (root/"schemas").mkdir()
            for path in (real/"schemas").glob("frontier_*.schema.json"):
                (root/"schemas"/path.name).write_bytes(path.read_bytes())
            for folder in ("tools/frontier", "tests/frontier", "src"):
                (root/folder).mkdir(parents=True)
            with mock.patch.object(build, "ROOT", root):
                self.assertEqual(8, len([p for p in build.input_paths() if p.startswith("schemas/")]))
                (root/"schemas/frontier_run_v3.schema.json").write_bytes(b"{}")
                with self.assertRaises(build.Refusal):
                    build.input_paths()
                (root/"schemas/frontier_run_v3.schema.json").unlink()
                (root/"schemas/frontier_checkpoint_v2.schema.json").unlink()
                with self.assertRaises(build.Refusal):
                    build.input_paths()

    def test_tool_binaries_are_rehashed_on_every_call_despite_cached_location(self):
        env, bindir, metadata = build.toolchain()
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            fake = Path(directory)
            for name in ("cl.exe", "link.exe", "lib.exe", "c1.dll", "c2.dll"):
                (fake/name).write_bytes((bindir/name).read_bytes())
            located = (env, fake, metadata["msvc_tools_version"], metadata["windows_sdk_version"])
            with mock.patch.object(build, "_LOCATED", located):
                self.assertEqual(metadata, build.toolchain()[2])
                (fake/"c2.dll").write_bytes(b"changed compiler back end")
                self.assertNotEqual(metadata, build.toolchain()[2])
                with self.assertRaisesRegex(build.Refusal, "compiler content"):
                    build.dependency_check()

    def test_altered_table_with_rehashed_manifest_refuses(self):
        self.altered_manifest(lambda value: value.__setitem__("table_text", value["table_text"].replace("3|1100|9|5|2", "3|1100|9|6|2")))

    def test_altered_source_identity_refuses(self):
        self.altered_manifest(lambda value: value["inputs"]["src/frontier_worker.c"]["lf"].__setitem__("sha3_256", "0"*64))

    def test_altered_artifact_identity_refuses(self):
        with mock.patch.object(build, "dependency_check", return_value=self.dependency), \
             mock.patch.object(build, "artifact_hashes", return_value={"forged.exe": {}}):
            with self.assertRaises(build.Refusal):
                build.verify_build()

    def test_unknown_manifest_key_refuses_even_rehashed(self):
        self.altered_manifest(lambda value: value.__setitem__("ignored_extra", "yes"))

    def test_missing_and_mismatched_local_cache_refuse(self):
        pin_bytes = build.PIN.read_bytes()
        pin = self.dependency[0]
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            root = Path(directory)
            path = root/"pin.toml"
            path.write_bytes(pin_bytes)
            with mock.patch.object(build, "ROOT", root), mock.patch.object(build, "PIN", path):
                with self.assertRaisesRegex(build.Refusal, "operator provisioning"):
                    build.dependency_check()
                archive = root/"local/c1/cache/sha256"/pin["binary_sha256"]/"mingw-w64-ucrt-x86_64-gmp-6.3.0-2-any.pkg.tar.zst"
                archive.parent.mkdir(parents=True)
                archive.write_bytes(b"a deliberately corrupt cached archive")
                with self.assertRaisesRegex(build.Refusal, "checksum mismatch"):
                    build.dependency_check()

    def test_mismatched_compiler_pin_refuses(self):
        pin, extracted, env, bindir, metadata = self.dependency
        wrong = copy.deepcopy(metadata)
        wrong["tool_sha3_256"]["cl.exe"] = "0"*64
        with mock.patch.object(build, "toolchain", return_value=(env, bindir, wrong)):
            with self.assertRaisesRegex(build.Refusal, "compiler content"):
                build.dependency_check()

    def test_checked_warning_is_fatal_without_replacing_worker(self):
        _, _, env, bindir, _ = self.dependency
        before = (build.BUILD/"ceml_frontier.exe").read_bytes()
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            folder = Path(directory)
            (folder/"warning.c").write_text("int main(void) { int unused; return 0; }\n", encoding="ascii")
            with self.assertRaises(build.Refusal):
                build.invoke([str(bindir/"cl.exe"), *build.FLAGS, "warning.c", "-Fe:warning.exe"], env, folder)
        self.assertEqual(before, (build.BUILD/"ceml_frontier.exe").read_bytes())


class NativeRefusals(unittest.TestCase):
    def invoke(self, arguments, checked=False, env=None):
        name = "ceml_frontier_checked.exe" if checked else "ceml_frontier.exe"
        return subprocess.run([str(build.BUILD/name), *arguments], stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, env=env)

    def scan(self, start="7", end="8", per="100000", total="2000000"):
        return ["--start", start, "--end", end, "--max-t-per-explicit", per, "--max-total-t", total]

    def test_release_and_checked_frames_identical(self):
        arguments = self.scan("2", "146")
        normal = self.invoke(arguments)
        checked = self.invoke(arguments, checked=True)
        self.assertEqual((normal.returncode, checked.returncode), (0, 0))
        self.assertEqual(normal.stdout, checked.stdout)
        self.assertEqual(normal.stderr, b"COMPLETE\n")
        self.assertEqual(checked.stderr, b"COMPLETE\n")
        self.assertEqual(len(normal.stdout.splitlines()), 144)

    def test_bad_unknown_duplicate_negative_zero_overflow_arguments(self):
        cases = [self.scan("-7"), self.scan("07"), self.scan("0"), self.scan(per="0"),
                 self.scan(per="100001"), self.scan(total="2000001"), self.scan(per=str(2**32)),
                 self.scan(total=str(2**64)), self.scan("7.0"), self.scan("+7"),
                 self.scan("9"*8193, "9"*8193), self.scan("8", "7"), self.scan("7", "7"),
                 self.scan("2", "14403"), ["--unknown", "1"],
                 ["--start", "7", "--start", "8", "--max-t-per-explicit", "2", "--max-total-t", "2"]]
        for arguments in cases:
            with self.subTest(arguments=arguments[:2]):
                result = self.invoke(arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertTrue(result.stderr.startswith(b"REFUSED"))

    def test_raw_high_bit_scans_refuse_but_bounded_identity_works(self):
        for n in (2**64, 2**71, 2**128+1):
            with self.subTest(n=n):
                scan = self.invoke(self.scan(str(n), str(n+1)))
                self.assertEqual(scan.returncode, 2)
                self.assertEqual(scan.stdout, b"")
                self.assertIn(b"RUN1 authority absent", scan.stderr)
                identity = self.invoke(["--identity", str(n), "4"])
                self.assertEqual(identity.returncode, 0)
                self.assertEqual(len(identity.stdout.splitlines()), 1)

    def test_no_infinite_identity_or_zero_step_success(self):
        for n, steps in (("0", "1"), ("7", "0"), ("7", "129"), ("7", str(2**64))):
            result = self.invoke(["--identity", n, steps])
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b"")

    def test_raw_gate_lookalikes_duplicate_and_oversized_status_refuse(self):
        phase = "**Authoritative current phase:** RUN1\n"
        science = "**Scientific execution authorization:** AUTHORISED\n"
        cases = [phase.replace("RUN1", "RUN10")+science,
                 phase+science.replace("AUTHORISED", "AUTHORISED-NOT"),
                 phase+science.replace("AUTHORISED", "AUTHORISED extra"),
                 phase.replace("RUN1", "RUN1x")+science,
                 phase+phase+science, phase+science+science,
                 phase+phase.replace(": RUN1", ":RUN10")+science,
                 phase+science+"\x00hidden", phase+science+"x"*(128*1024)]
        with tempfile.TemporaryDirectory(dir=ROOT/"local/frontier") as directory:
            path = Path(directory)/"status.md"
            env = dict(os.environ, CEML_FRONTIER_DRIVER_MODE="RUN1-AUTHORIZED",
                       CEML_FRONTIER_STATUS_PATH=str(path))
            for text in cases:
                with self.subTest(prefix=text[:70]):
                    path.write_bytes(text.encode("ascii"))
                    # Single algebraic start outside the native L1 test cap;
                    # every injected status must refuse before any frame.
                    result = self.invoke(self.scan("10000", "10001"), env=env)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, b"")
                    self.assertIn(b"RUN1 authority absent", result.stderr)

    def test_resource_ceiling_and_budget_pending_never_success(self):
        resource = self.invoke(["--identity", "9"*8192, "1"])
        self.assertEqual(resource.returncode, 3)
        self.assertEqual(resource.stdout, b"")
        for per, total, reason in (("1", "1", "total_budget"), ("1", "2", "step_budget")):
            result = self.invoke(self.scan(per=per, total=total))
            self.assertEqual(result.returncode, 3)
            self.assertEqual(result.stdout, b"")
            self.assertEqual(result.stderr, f"UNRESOLVED|7|{reason}|1|1|11\n".encode("ascii"))


if __name__ == "__main__":
    unittest.main()
