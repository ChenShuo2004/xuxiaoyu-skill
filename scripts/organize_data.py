"""Normalize extracted knowledge records offline. Python 3.9+, standard library only."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

FIELDS = ['text', 'url', 'source_file', 'title', 'date', 'accessed', 'speaker',
          'locator', 'topic', 'evidence_kind', 'read_scope', 'limitations']
KINDS = {'fact', 'quote', 'summary', 'user_statement', 'inference', 'lead', 'unknown'}
SCOPES = {'full', 'excerpt', 'summary', 'transcript', 'unread', 'unknown'}
PACKAGE = Path(__file__).resolve().parent.parent


def canonical_url(value):
    if not value:
        return ''
    parts = urlsplit(value)
    if parts.scheme.lower() not in {'https', 'http'} or not parts.hostname:
        raise ValueError('url must be an absolute http(s) address')
    if parts.username or parts.password:
        raise ValueError('url must not contain credentials')
    # Preserve meaningful parameter order; remove tracking and fragments only.
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if not k.lower().startswith('utm_') and k.lower() not in {'fbclid', 'gclid'}]
    query = parts.query if len(kept) == len(parse_qsl(parts.query, keep_blank_values=True)) else urlencode(kept)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, query, ''))


def stable_id(prefix, value):
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return prefix + hashlib.sha256(body.encode('utf-8')).hexdigest()[:20]


def load_rows(path):
    path = Path(path)
    if path.suffix.lower() == '.csv':
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
                raise ValueError('CSV needs unique field names')
            result = []
            for row in reader:
                if None in row:
                    raise ValueError('CSV has extra cells at line ' + str(reader.line_num))
                result.append((reader.line_num, row))
            return result
    body = path.read_text(encoding='utf-8-sig')
    if path.suffix.lower() == '.json':
        rows = json.loads(body)
        if not isinstance(rows, list):
            raise ValueError('JSON input must be an array of objects')
        return list(enumerate(rows, 1))
    if path.suffix.lower() != '.jsonl':
        raise ValueError('Input must be .json, .jsonl or .csv')
    rows = []
    for number, line in enumerate(body.splitlines(), 1):
        if line.strip():
            try:
                rows.append((number, json.loads(line)))
            except json.JSONDecodeError as exc:
                raise ValueError('Invalid JSONL at line ' + str(number) + ': ' + exc.msg) from exc
    return rows


def normalize(row):
    if not isinstance(row, dict) or not all(isinstance(k, str) for k in row):
        raise ValueError('Record must be an object with string keys')
    record = {}
    for field in FIELDS:
        value = row.get(field)
        if field == 'topic':
            value = [] if value is None else value
            if isinstance(value, str):
                value = value.split('|')
            if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
                raise ValueError('topic must be a string or array of strings')
            record[field] = sorted({unicodedata.normalize('NFC', x.strip()) for x in value if x.strip()})
        else:
            if value is not None and not isinstance(value, str):
                raise ValueError(field + ' must be a string or null')
            record[field] = unicodedata.normalize('NFC', (value or '').strip())
    if not record['text']:
        raise ValueError('Missing text; link-only rows belong in the unread lead list')
    if not record['url'] and not record['source_file']:
        raise ValueError('Missing source: provide url or source_file')
    record['url'] = canonical_url(record['url'])
    record['evidence_kind'] = record['evidence_kind'] or 'unknown'
    record['read_scope'] = record['read_scope'] or 'unknown'
    if record['evidence_kind'] not in KINDS:
        raise ValueError('Unsupported evidence_kind')
    if record['read_scope'] not in SCOPES:
        raise ValueError('Unsupported read_scope')
    record['extra'] = {k: v for k, v in row.items() if k not in FIELDS}
    return record


def spreadsheet_cell(value):
    text = json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict)) else str(value)
    return "'" + text if text.lstrip().startswith(('=', '+', '-', '@')) else text


def organize(input_path, output_path):
    output = Path(output_path).expanduser().absolute()
    resolved = output.resolve()
    if resolved == PACKAGE or resolved.is_relative_to(PACKAGE):
        raise ValueError('Output must be outside the installed Skill directory')
    if output.exists() or output.is_symlink():
        raise ValueError('Output exists; choose a new directory')
    rows = load_rows(input_path)  # Parse completely before creating any output.
    records, sources, warnings, rejected, duplicates = {}, {}, [], [], []
    for number, row in rows:
        try:
            record = normalize(row)
        except ValueError as exc:
            rejected.append({'input_row': number, 'reason': str(exc), 'original': row})
            continue
        source_id = stable_id('SRC-', record['url'] or record['source_file'])
        record_id = stable_id('REC-', record)
        if record_id in records:
            records[record_id]['input_rows'].append(number)
            duplicates.append({'input_row': number, 'kept_record': record_id})
            continue
        for field in ['title', 'date', 'speaker', 'locator']:
            if not record[field]:
                warnings.append({'record': record_id, 'input_row': number, 'field': field, 'issue': 'missing'})
        if record['evidence_kind'] == 'unknown' or record['read_scope'] in {'unknown', 'unread'}:
            warnings.append({'record': record_id, 'input_row': number, 'issue': 'not_verified'})
        if record['evidence_kind'] == 'quote' and record['read_scope'] == 'transcript':
            warnings.append({'record': record_id, 'input_row': number, 'issue': 'quote_needs_original_check'})
        record.update(id=record_id, source_id=source_id, input_rows=[number])
        records[record_id] = record
        source = sources.setdefault(source_id, {'id': source_id, 'url': record['url'],
                                    'files': [], 'titles': [], 'dates': [], 'record_ids': []})
        for key, field in [('files', 'source_file'), ('titles', 'title'), ('dates', 'date')]:
            if record[field] and record[field] not in source[key]:
                source[key].append(record[field])
        source['record_ids'].append(record_id)
    conflicts = [{'source': s['id'], 'titles': s['titles'], 'dates': s['dates']}
                 for s in sources.values() if len(s['titles']) > 1 or len(s['dates']) > 1]
    counts = {'input_rows': len(rows), 'records': len(records), 'sources': len(sources),
              'duplicate_rows': len(duplicates), 'rejected_rows': len(rejected),
              'warnings': len(warnings), 'source_conflicts': len(conflicts)}
    issues = dict(counts=counts, warnings=warnings, duplicates=duplicates,
                  rejected=rejected, source_conflicts=conflicts)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.organize-', dir=output.parent))
    try:
        def write_json(name, value):
            (stage / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (stage / 'records.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n'
                                                  for r in records.values()), encoding='utf-8')
        write_json('sources.json', list(sources.values()))
        write_json('issues.json', issues)
        csv_fields = ['id', 'source_id', *FIELDS, 'extra', 'input_rows']
        with (stage / 'records.csv').open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=csv_fields)
            writer.writeheader()
            for r in records.values():
                writer.writerow({k: spreadsheet_cell(r[k]) for k in csv_fields})
        topics = Counter(t for r in records.values() for t in r['topic'])
        lines = ['# 资料整理结果', '', '这是字段规范化与精确去重结果；未执行语义提取或事实核验。', '']
        lines.extend('- ' + k + ': ' + str(v) for k, v in counts.items())
        lines += ['', '## 主题分布', '', *['- ' + k.replace('\n', ' ') + ': ' + str(v) for k, v in topics.most_common()],
                  '', '缺字段、拒收原行及来源冲突见 issues.json；无损正文见 records.jsonl。', '']
        (stage / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
        # Claim a fresh directory atomically, preventing replacement of a concurrent output.
        output.mkdir()
        try:
            for file in stage.iterdir():
                os.replace(file, output / file.name)
        except OSError:
            shutil.rmtree(output)
            raise
    finally:
        shutil.rmtree(stage)
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(organize(args.input, args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, 'Organization failed: ' + str(exc) + '\n')
