import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from find_evidence import search


class CorpusTests(unittest.TestCase):
    def test_applications_are_labelled_and_references_resolve(self):
        claims = {json.loads(s)['id'] for s in (ROOT / 'references/claims.jsonl').read_text().splitlines()}
        for name in ['case-library.json', 'topics.json']:
            for row in json.loads((ROOT / 'references' / name).read_text()):
                self.assertTrue(row['claim_ids'])
                self.assertTrue(set(row['claim_ids']) <= claims)
                self.assertTrue(row['evidence_kind'].startswith('editorial-'))
        for line in (ROOT / 'references/scenarios.jsonl').read_text().splitlines():
            row = json.loads(line)
            self.assertEqual(row['evidence_kind'], 'synthetic-application')
            self.assertTrue(set(row['claim_ids']) <= claims)
            self.assertIn('不是徐霄羽原话', row['attribution'])

    def test_related_versions_share_evidence_groups(self):
        sources = {s['id']: s for s in json.loads((ROOT / 'references/sources.json').read_text())}
        self.assertEqual(sources['S03']['independence_group'], sources['S24']['independence_group'])
        self.assertEqual(sources['S11']['independence_group'], sources['S25']['independence_group'])
        for lead in json.loads((ROOT / 'references/research-gaps.json').read_text()):
            self.assertFalse(lead['used_for_claims'])

    def test_search_finds_new_evidence_and_source_filters(self):
        results = search(ROOT, ['第一笔融资'])
        self.assertTrue(any(r['source'] == 'S18' for r in results))
        results = search(ROOT, [], source='S16', limit=100)
        self.assertTrue(results)
        self.assertTrue(all(r['source'] == 'S16' and r['url'].startswith('https://') for r in results))
        self.assertEqual(search(ROOT, ['nonexistent-unique-token']), [])

    def test_search_separates_generated_scenarios(self):
        results = search(ROOT, ['融资'], kind='scenarios', limit=20)
        self.assertTrue(results)
        self.assertTrue(all(r['record_type'] == 'scenarios' for r in results))
        self.assertTrue(all(r['evidence_kind'] == 'synthetic-application' for r in results))
        results = search(ROOT, [], kind='topics', topic='health')
        self.assertTrue(any(r['key'] == 'health' for r in results))


if __name__ == '__main__':
    unittest.main()
