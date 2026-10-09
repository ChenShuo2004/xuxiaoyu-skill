import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from organize_data import canonical_url, organize


class DataTests(unittest.TestCase):
    def run_input(self, rows, td, suffix='.jsonl'):
        path = Path(td) / ('input' + suffix)
        if suffix == '.json':
            path.write_text(json.dumps(rows), encoding='utf-8')
        elif suffix == '.csv':
            with path.open('w', encoding='utf-8', newline='') as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
        else:
            path.write_text(''.join(json.dumps(x) + '\n' for x in rows), encoding='utf-8')
        out = Path(td) / 'result'
        return path, out, organize(path, out)

    def test_dedup_preserves_attribution_and_extra(self):
        base = dict(text='测试观点', url='https://example.com/a?id=1&utm_source=x#p',
                    speaker='嘉宾A', locator='00:10', title='访谈', date='2026-01-01',
                    read_scope='excerpt', evidence_kind='summary', custom={'keep': True})
        same = dict(base, url='https://example.com/a?id=1')
        different_speaker = dict(same, speaker='嘉宾B')
        different_source = dict(same, url='https://example.org/a')
        with tempfile.TemporaryDirectory() as td:
            _, out, counts = self.run_input([base, same, different_speaker, different_source], td)
            records = [json.loads(x) for x in (out / 'records.jsonl').read_text().splitlines()]
            self.assertEqual(counts['records'], 3)
            self.assertEqual(counts['sources'], 2)
            self.assertEqual(records[0]['input_rows'], [1, 2])
            self.assertEqual(records[0]['extra']['custom'], {'keep': True})

    def test_missing_and_bad_records_remain_traceable(self):
        rows = [dict(text='缺日期', source_file='notes.md'), dict(url='https://example.com'),
                dict(text='错误类型', source_file='n', speaker=5), dict(text='另一观点',
                source_file='notes.md', title='版本B', date='2026-01-01'), dict(text='旧观点',
                source_file='notes.md', title='版本A', date='2025-01-01')]
        with tempfile.TemporaryDirectory() as td:
            _, out, counts = self.run_input(rows, td)
            issues = json.loads((out / 'issues.json').read_text())
            self.assertEqual(counts['rejected_rows'], 2)
            self.assertEqual(counts['source_conflicts'], 1)
            self.assertEqual(issues['rejected'][0]['original'], rows[1])
            self.assertEqual(issues['warnings'][0]['field'], 'title')

    def test_csv_formula_neutralized_json_is_lossless(self):
        with tempfile.TemporaryDirectory() as td:
            _, out, _ = self.run_input([dict(text='=1+1', source_file='demo', topic='AI|产品')], td, '.csv')
            with (out / 'records.csv').open(encoding='utf-8-sig', newline='') as f:
                row = next(csv.DictReader(f))
            self.assertEqual(row['text'], "'=1+1")
            self.assertEqual(json.loads((out / 'records.jsonl').read_text())['text'], '=1+1')

    def test_no_overwrite_and_parse_failure_creates_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            path, out, _ = self.run_input([dict(text='test', source_file='n')], td, '.json')
            sentinel = out / 'keep'
            sentinel.write_text('preserved')
            with self.assertRaises(ValueError):
                organize(path, out)
            self.assertEqual(sentinel.read_text(), 'preserved')
            path = Path(td) / 'bad.jsonl'
            path.write_text('{bad}\n')
            with self.assertRaisesRegex(ValueError, 'line 1'):
                organize(path, Path(td) / 'never-created')
            self.assertFalse((Path(td) / 'never-created').exists())

    def test_output_cannot_modify_skill_and_url_keeps_meaning(self):
        with self.assertRaises(ValueError):
            organize(ROOT / 'examples/records.input.jsonl', ROOT / 'new-output')
        self.assertEqual(canonical_url('https://example.com/a?b=2&a=1&utm_source=x#z'),
                         'https://example.com/a?b=2&a=1')
        with self.assertRaises(ValueError):
            canonical_url('https://name:secret@example.com')


if __name__ == '__main__':
    unittest.main()
