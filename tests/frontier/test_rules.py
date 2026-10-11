"""Bounded proof-witness fixtures; these do not verify a scientific frontier."""
import collections
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "frontier"))
import reference as ref

NATIVE = ROOT / "local" / "frontier" / "build" / "ceml_frontier.exe"


class RuleTests(unittest.TestCase):
    def test_boundary_and_exact_precedence(self):
        for invalid in (0, 1, -1, True, 2.0, "2"):
            with self.assertRaises(ref.Refusal):
                ref.classify(invalid)
        for n, rule in ((2, "E2"), (3, "S2K4-03"), (4, "E2"), (5, "Q4"),
                        (7, "EXPLICIT"), (11, "P3"), (31, "M9"), (35, "P3")):
            self.assertEqual(ref.classify(n), rule)
        self.assertEqual((ref.C(1), ref.T(1), ref.U(1)), (4, 2, (1, 2)))

    def test_complete_144_pinned_ledger(self):
        table = ref.truth_table()
        self.assertEqual(len(table), 144)
        self.assertEqual(collections.Counter(table),
                         {"E2": 72, "Q4": 36, "P3": 12, "M9": 4,
                          "S2K4-03": 5, "EXPLICIT": 15})
        for rule, residues in ref.PINNED_RESIDUES.items():
            self.assertEqual(tuple(i for i, value in enumerate(table) if value == rule), residues)
        report = ref.check_rules()
        self.assertEqual((report["scope"], report["parity_rows"], report["priority_residues"]),
                         ("NONSCIENTIFIC", 16, 144))

    def test_independent_bit_predicates_and_fixed_witnesses(self):
        # Bit tests and the independently pinned disjoint ledger constitute
        # a separate reference to the modulo predicate implementation.
        for n in range(2, 10001):
            residue = n % 144
            expected = ("E2" if (n & 1) == 0 else
                        "Q4" if (n & 3) == 1 else
                        next(rule for rule, residues in ref.PINNED_RESIDUES.items()
                             if residue in residues))
            self.assertEqual(ref.classify(n), expected)
            if expected != "EXPLICIT":
                witness = ref.algebraic_witness(n)
                self.assertTrue(0 < witness < n)
                if expected == "P3":
                    self.assertEqual(ref.T(witness), n)
                elif expected == "M9":
                    self.assertEqual(ref.T(ref.T(ref.T(witness))), n)
                else:
                    steps = {"E2": 1, "Q4": 2, "S2K4-03": 4}[expected]
                    self.assertEqual(ref.identity(n, steps)["value"], witness)

    def test_reverse_rules_include_preempted_domain_boundaries(self):
        # Test theorem domains separately from rule priority: E2 owns n=2/4,
        # while the underlying P3/M9 identities still hold at those bounds.
        for k in (0, 1, 9, 1 << 64, 1 << 128):
            n = 3 * k + 2
            predecessor = (2 * n - 1) // 3
            self.assertEqual((predecessor, ref.T(predecessor)), (2 * k + 1, n))
            self.assertTrue(0 < predecessor < n)
        for h in (0, 1, 19, 1 << 71, 1 << 160):
            n = 9 * h + 4
            predecessor = (8 * n - 5) // 9
            self.assertEqual(predecessor, 8 * h + 3)
            self.assertEqual(ref.T(ref.T(ref.T(predecessor))), n)
            self.assertTrue(0 < predecessor < n)

    def test_high_rule_witnesses_only_finite_identities(self):
        for bits in (32, 64, 71, 128, 160):
            base = 1 << bits
            for residue in (0, 1, 3, 11, 31):
                n = base + ((residue - base) % 144)
                self.assertEqual(ref.classify(n), ref.truth_table()[residue])
                self.assertTrue(0 < ref.algebraic_witness(n) < n)

    def test_sixteen_parity_words_and_affine_quotients(self):
        rows = ref.table_rows()
        self.assertEqual(len({row["parity_lsb_first"] for row in rows}), 16)
        for row in rows:
            for q in (0, 1, 3, 29, 1 << 128):
                n = 16 * q + row["residue"]
                value = n
                parity = []
                for _ in range(4):
                    parity.append(str(value % 2))
                    value = value // 2 if value % 2 == 0 else (3 * value + 1) // 2
                self.assertEqual("".join(parity), row["parity_lsb_first"])
                numerator = row["affine_a"] * n + row["affine_b"]
                self.assertEqual(numerator % 16, 0)
                self.assertEqual(numerator // 16, value)
        self.assertEqual([r["residue"] for r in rows
                          if r["residue"] % 4 == 3 and r["universal_q0"]], [3])

    def test_k_through_seven_bounded_affine_identities(self):
        for k in range(1, 8):
            modulus = 1 << k
            for row in ref.table_rows(k):
                for q in (0, 1, 3):
                    value = modulus * q + row["residue"]
                    for _ in range(k):
                        value = value // 2 if value % 2 == 0 else (3 * value + 1) // 2
                    self.assertEqual(value, row["affine_a"] * q + row["T4_r"])

    def test_table_mismatch_refuses(self):
        raw = ref.table_bytes()
        self.assertEqual(ref.verify_table(raw), ref.table_digest())
        for mutation in (raw.replace(b"3|1100|9|5|2", b"3|1000|9|5|2"),
                         raw.replace(b"3|1100|9|5|2", b"3|1100|8|5|2"),
                         raw.replace(b"3|1100|9|5|2", b"3|1100|9|6|2"),
                         raw[:-1], raw + b"\n", b"unexpected"):
            with self.assertRaises(ref.Refusal):
                ref.verify_table(mutation)

    def test_exact_floor_counts_across_boundaries(self):
        for start, width in ((2, 0), (2, 144), (143, 144), (140, 300),
                             (1 << 32, 287), ((1 << 64) - 3, 149),
                             ((1 << 71) + 1, 143), ((1 << 160) - 71, 287)):
            with self.subTest(start=start, width=width):
                direct = dict.fromkeys(ref.COUNT_KEYS, 0)
                for n in range(start, start + width):
                    direct[ref.RULE_COUNT_KEYS[ref.classify(n)]] += 1
                self.assertEqual(ref.expected_counts(start, start + width), direct)
                self.assertEqual(sum(direct.values()), width)
                self.assertEqual((direct["base_count"], direct["unresolved_count"]), (0, 0))

    @unittest.skipUnless(NATIVE.is_file(), "new pinned frontier worker not built")
    def test_native_independent_table(self):
        completed = subprocess.run([str(NATIVE), "--table"], capture_output=True, timeout=20)
        self.assertEqual(completed.returncode, 0, completed.stderr.decode("ascii", errors="replace"))
        self.assertEqual(completed.stdout, ref.table_bytes())


if __name__ == "__main__":
    unittest.main()
