"""Bounded developer tests for the CEML-CAL-1 driver; not calibration, not V1."""
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/c1'))

import cal1_suite as suite  # noqa: E402


class Cal1SuiteTests(unittest.TestCase):
    def test_normative_generator_vector(self):
        vector = json.loads((ROOT / 'config/calibration_suite_v1.json').read_text())['generator_test_vector']
        operands, (descriptor, digest) = suite.state_input('route-crossover', 256, 0)
        self.assertEqual(format(operands[0], 'x'), vector['state_hex'])
        self.assertEqual(suite.canonical_bytes(descriptor).decode(), vector['descriptor_jcs'])
        self.assertEqual(digest, vector['input_digest'])
        self.assertEqual(suite.state_digest(operands[0], 0, 0), vector['initial_state_digest'])

    def test_definition_reference_fixtures(self):
        self.assertEqual(suite.reference_state(27, None), (1, 70, 41))
        self.assertEqual(suite.reference_state((1 << 127) - 1, None), (1, 1067, 593))
        self.assertEqual(suite.reference_state(1, None), (1, 0, 0))
        self.assertEqual(suite.reference_state(8, 2), (2, 2, 0))
        self.assertEqual(suite.reference_state(8, 100), (1, 3, 0))

    def test_matrix_respects_suite_bounds_and_order(self):
        rows = suite.matrix()
        bounds = json.loads((ROOT / 'config/calibration_suite_v1.json').read_text())['bounds']
        last = None
        for family, bits, candidate, index, maker, executable, args, required, kind, budget in rows:
            key = (suite.FAMILIES[family], bits, candidate, index)
            if last is not None:
                self.assertLess(last, key)
            last = key
            self.assertLessEqual(bits, int(bounds['max_generated_operand_bits']))
            self.assertTrue(required)
            if budget is not None:
                limit = bounds['max_affine_macro_shortcut_steps'] if 'hier' in args else bounds['max_fixed_shortcut_steps_per_case']
                self.assertLessEqual(budget, int(limit))
            if 'small' in args:
                self.assertEqual(budget % int(args[2]), 0)
                self.assertLessEqual(int(args[2]), int(bounds['max_small_table_width']))

    def test_inputs_are_engineering_only_and_shared_between_candidates(self):
        seen = {}
        for row in suite.matrix():
            family, bits, candidate, index, maker = row[:5]
            operands, (descriptor, digest) = maker(bits, index)
            self.assertEqual(descriptor['suite_version'], 'CEML-CAL-1')
            self.assertNotIn('candidate', json.dumps(descriptor))
            self.assertEqual(seen.setdefault(descriptor['input_id'], digest), digest)
            for value in operands:
                self.assertLessEqual(value.bit_length(), 131072)

    def test_product_shapes(self):
        for index, ratio in ((0, 1), (4, 2), (8, 4)):
            (left, right), _ = suite.product_input(4096, index)
            self.assertEqual(left.bit_length(), 4096)
            self.assertEqual(right.bit_length(), 4096//ratio)


if __name__ == '__main__':
    unittest.main()
