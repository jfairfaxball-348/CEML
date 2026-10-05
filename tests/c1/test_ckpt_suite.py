"""Bounded developer tests for the checkpoint test driver's independent codec; not V1."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/c1'))

import ckpt_suite as suite  # noqa: E402


class CheckpointDriverTests(unittest.TestCase):
    def test_frozen_body_vector(self):
        suite.frozen_vector()

    def test_synthetic_metadata_is_schema_valid_and_self_consistent(self):
        ident = suite.identity('unit', 'a'*40)
        first = suite.metadata_object(ident, 0, None, 1, 70, 41)
        self.assertTrue(suite.schema_valid(first))
        self.assertTrue(first['terminal_reached'])
        self.assertEqual(first['standard_steps'], '111')
        second = suite.metadata_object(ident, 1, first['metadata_digest'], 27, 0, 0)
        self.assertTrue(suite.schema_valid(second))
        self.assertFalse(second['terminal_reached'])
        self.assertNotEqual(first['metadata_digest'], second['metadata_digest'])

    def test_checkpoint_inputs_have_exact_magnitudes_within_generator_bound(self):
        for magnitude in (1024, 4096, 16384, 32768):
            value, descriptor, _ = suite.checkpoint_input(magnitude, 0)
            self.assertEqual((value.bit_length() + 7)//8, magnitude)
            self.assertEqual(value & 1, 1)
            for role in descriptor['operand_roles']:
                self.assertLessEqual(int(role['size_bits']), 131072)

    def test_every_r4_phase_is_mapped(self):
        self.assertEqual(set(suite.R4_PHASES), set(suite.PRE_PUBLICATION + suite.POST_PUBLICATION))
        self.assertEqual(len(set(suite.R4_PHASES.values())), 7)


if __name__ == '__main__':
    unittest.main()
