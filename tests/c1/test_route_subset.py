"""Stage: hardware characterization; orchestration checks, no trajectories."""
from pathlib import Path
import sys
import tempfile
import unittest
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/c1'))
if sys.platform == 'win32':
    import route_subset as subset


@unittest.skipUnless(sys.platform == 'win32', 'Windows-only orchestration')
class SubsetTests(unittest.TestCase):
    def test_generated_input_scope_and_repeat_identity(self):
        for bits in (1024, 4096):
            n, descriptor, digest = subset.engineering_input(bits, 0)
            self.assertEqual(n.bit_length(), bits)
            self.assertEqual(n & 1, 1)
            self.assertEqual(subset.engineering_input(bits, 0), (n, descriptor, digest))
            self.assertNotEqual(subset.engineering_input(bits, 1)[2], digest)
        for bits, index in ((256, 0), (16384, 0), (4096, 3), (4096, -1)):
            with self.assertRaises(subset.Refusal):
                subset.engineering_input(bits, index)

    def test_budget_update_replaces_and_survives_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'budget'
            with path.open('w+b') as stream:
                subset.save_budget(stream, 5000000000)
                subset.save_budget(stream, 10)
            self.assertEqual(json.loads(path.read_bytes()), {'charged_ns': '10'})


if __name__ == '__main__':
    unittest.main()
