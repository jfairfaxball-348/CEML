"""Website progress derivation tests: text transforms only, never scientific runs."""

import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location('website_progress',
    Path(__file__).resolve().parents[2] / 'tools/publication/website_progress.py')
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


class WebsiteProgressTests(unittest.TestCase):
    def setUp(self):
        self.text = publication.SOURCE.read_text(encoding='utf-8')

    def test_committed_file_matches_published_record(self):
        expected = publication.render(publication.build(self.text))
        self.assertEqual(publication.OUTPUT.read_text(encoding='utf-8'), expected)

    def test_totals_and_contiguity(self):
        data = publication.build(self.text)
        batches = data['batches']
        self.assertEqual(batches[0]['start'], data['base']['value'])
        self.assertEqual(batches[-1]['end'], data['coverage']['end'])
        self.assertEqual(sum(batch['width'] for batch in batches), int(data['coverage']['integers']))
        self.assertEqual(sum(data['rule_counts'].values()), int(data['coverage']['integers']))

    def test_gap_between_batches_is_refused(self):
        tampered = self.text.replace('| 2 | `[2392518188130438742160,', '| 2 | `[2392518188130438742161,', 1)
        self.assertNotEqual(tampered, self.text)
        with self.assertRaises(publication.PublicationError):
            publication.build(tampered)

    def test_latest_digest_mismatch_is_refused(self):
        tampered = self.text.replace('Latest certificate digest: c', 'Latest certificate digest: d', 1)
        self.assertNotEqual(tampered, self.text)
        with self.assertRaises(publication.PublicationError):
            publication.build(tampered)


if __name__ == '__main__':
    unittest.main()
