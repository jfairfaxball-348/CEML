"""Exact finite identities, bounded first descents, and full tiny replay."""
import hashlib
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "frontier"))
import reference as ref

NATIVE = ROOT / "local" / "frontier" / "build" / "ceml_frontier.exe"
FIXTURES = ((2, 146), (143, 287), (37, 101))


class ExactnessTests(unittest.TestCase):
    def test_independent_c_t_boundaries_and_standard_steps(self):
        high = tuple(value + offset for bits in (32, 64, 71, 128, 160)
                     for value in (1 << bits,) for offset in (-1, 0, 1, 3))
        for n in (1, 2, 3, 4, 5, 7, 31) + high:
            direct_c = n
            shortcut = n
            standard = odd = 0
            for t_steps in range(1, 17):
                before = direct_c
                if before % 2:
                    direct_c = ref.C(direct_c)
                    standard += 1
                    odd += 1
                    self.assertEqual(direct_c % 2, 0)
                direct_c = ref.C(direct_c)
                standard += 1
                shortcut = ref.T(shortcut)
                self.assertEqual(direct_c, shortcut)
                self.assertEqual(standard, t_steps + odd)
                self.assertEqual(ref.identity(n, t_steps),
                                 {"value": shortcut, "steps": t_steps, "odd": odd, "standard": standard})

    def test_odd_only_exact_halving_counts(self):
        for n in (1, 3, 5, 7, 31, (1 << 64) - 1, (1 << 71) + 1, (1 << 128) + 3):
            odd_value, halvings = ref.U(n)
            self.assertEqual(odd_value % 2, 1)
            self.assertEqual(odd_value * (1 << halvings), 3 * n + 1)
            direct_t = n
            parity = 0
            for _ in range(halvings):
                parity += direct_t % 2
                direct_t = ref.T(direct_t)
            self.assertEqual((direct_t, parity), (odd_value, 1))
        with self.assertRaises(ref.Refusal):
            ref.U(2)

    def test_first_descent_frame_and_finite_budget(self):
        raw = ref.event(7)
        self.assertEqual(raw, b"7|EXPLICIT|7|4|5\n")
        value = 7
        for step in range(1, 8):
            value = ref.T(value)
            self.assertEqual(value < 7, step == 7)
        for n in (2, 3, 5, 11, 31):
            fields = ref.event(n).decode("ascii").strip().split("|")
            self.assertEqual(fields[2:4], ["0", "0"])
            self.assertEqual(int(fields[4]), ref.algebraic_witness(n))
        with self.assertRaises(ref.Unresolved) as caught:
            ref.event(7, max_t=6)
        self.assertEqual(caught.exception.pending(),
                         {"n": "7", "reason": "step_budget", "attempted_steps": "6", "last_value": "10"})

    def test_tiny_full_replay_digest_and_counter_reconciliation(self):
        for start, end in FIXTURES:
            replay = ref.replay(start, end, max_t=1000, max_total=200000)
            frames = list(ref.iter_events(start, end, max_t=1000))
            self.assertTrue(replay["complete"])
            self.assertIsNone(replay["pending"])
            self.assertEqual(replay["next_n"], end)
            self.assertEqual(replay["counts"], ref.expected_counts(start, end))
            self.assertEqual(replay["transcript_digest"],
                             hashlib.sha3_256(b"CEML-FRONTIER-1/EVENTS\0" + b"".join(frames)).hexdigest())
            t_steps = odd = 0
            explicit = 0
            for n, frame in zip(range(start, end), frames):
                parts = frame.decode("ascii").rstrip("\n").split("|")
                self.assertEqual(parts[0], str(n))
                t_steps += int(parts[2])
                odd += int(parts[3])
                explicit += parts[1] == "EXPLICIT"
            self.assertEqual((replay["explicit_t_steps"], replay["explicit_odd_steps"],
                              replay["explicit_standard_steps"], replay["explicit_attempts"]),
                             (t_steps, odd, t_steps + odd, explicit))

    def test_unresolved_never_advances_or_counts_attempt(self):
        for max_t, max_total, reason in ((6, 100, "step_budget"), (100, 6, "total_budget")):
            replay = ref.replay(2, 16, max_t=max_t, max_total=max_total)
            self.assertFalse(replay["complete"])
            self.assertEqual(replay["next_n"], 7)
            self.assertEqual(replay["pending"]["reason"], reason)
            self.assertEqual(replay["counts"], ref.expected_counts(2, 7))
            self.assertEqual(replay["explicit_attempts"], 1)
            self.assertEqual(replay["counts"]["explicit_count"], 0)
            self.assertEqual(replay["counts"]["unresolved_count"], 0)
            self.assertEqual(replay["explicit_t_steps"], 0)

    def test_total_exhaustion_keeps_algebraic_frames_until_next_explicit(self):
        replay = ref.replay(2, 20, max_t=100, max_total=7)
        self.assertEqual(replay["next_n"], 15)
        self.assertEqual(replay["pending"],
                         {"n": "15", "reason": "total_budget", "attempted_steps": "0", "last_value": "15"})
        self.assertEqual(replay["counts"], ref.expected_counts(2, 15))
        self.assertEqual((replay["explicit_attempts"], replay["counts"]["explicit_count"],
                          replay["explicit_t_steps"]), (2, 1, 7))

    def test_refuse_invalid_budgets_and_domains(self):
        for max_t in (0, -1, 100001, True, 1.5):
            with self.assertRaises(ref.Refusal):
                ref.event(7, max_t=max_t)
        for start, end in ((1, 146), (0, 10), (2, 14403), (3, 2)):
            with self.assertRaises(ref.Refusal):
                ref.replay(start, end)
        for total in (0, -1, 2000001, True, 1.1):
            with self.assertRaises(ref.Refusal):
                ref.replay(2, 10, max_total=total)

    def test_empty_replay_is_only_an_empty_prefix(self):
        result = ref.replay(2, 2, 1, 1)
        self.assertEqual(result["counts"], dict.fromkeys(ref.COUNT_KEYS, 0))
        self.assertEqual(result["next_n"], 2)
        self.assertTrue(result["complete"])
        self.assertEqual(result["explicit_attempts"], 0)
        self.assertEqual(result["transcript_digest"],
                         hashlib.sha3_256(b"CEML-FRONTIER-1/EVENTS\0").hexdigest())

    def test_large_decimal_format_is_exact_without_global_policy_change(self):
        value = 10 ** 8191 + (1 << 160) + 7
        rendered = ref.decimal(value)
        self.assertEqual(len(rendered), 8192)
        self.assertTrue(rendered.startswith("1"))
        self.assertTrue(rendered.endswith(str((1 << 160) + 7)))
        self.assertEqual(ref.decimal(0), "0")

    @unittest.skipUnless(NATIVE.is_file(), "new pinned frontier worker not built")
    def test_native_full_small_batches_match_separate_replay(self):
        for start, end in FIXTURES:
            result = subprocess.run([str(NATIVE), "--start", str(start), "--end", str(end),
                                     "--max-t-per-explicit", "1000", "--max-total-t", "200000"],
                                    capture_output=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr.decode("ascii", errors="replace"))
            # A fresh second pass through every n, after the native exit.
            self.assertEqual(result.stdout, b"".join(ref.iter_events(start, end, max_t=1000)))
            self.assertTrue(ref.replay(start, end, 1000, 200000)["complete"])

    @unittest.skipUnless(NATIVE.is_file(), "new pinned frontier worker not built")
    def test_native_high_values_only_fixed_step_identities(self):
        for bits in (32, 64, 71, 128, 160):
            for offset in (-1, 0, 1, 3):
                n = (1 << bits) + offset
                identity = ref.identity(n, 16)
                result = subprocess.run([str(NATIVE), "--identity", str(n), "16"],
                                        capture_output=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr.decode("ascii", errors="replace"))
                expected = (f"{n}|IDENTITY|16|{identity['odd']}|{identity['value']}|"
                            f"{identity['standard']}\n").encode("ascii")
                self.assertEqual(result.stdout, expected)


if __name__ == "__main__":
    unittest.main()
