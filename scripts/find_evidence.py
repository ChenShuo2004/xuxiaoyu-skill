"""Offline corpus lookup; evidence and original applications remain labelled."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

def search(root, terms=(), kind='claims', limit=12, source=None, topic=None):
    refs = Path(root) / 'references'
    sources = {s['id']: s for s in json.loads((refs / 'sources.json').read_text(encoding='utf-8'))}
    claims = read_jsonl(refs / 'claims.jsonl')
    claim_map = {c['id']: c for c in claims}
    topics = json.loads((refs / 'topics.json').read_text(encoding='utf-8'))
    aliases = {word.casefold(): t['key'] for t in topics for word in t['keywords']}
    terms = [word.casefold() for part in terms for word in part.split()]
    expanded = set(terms) | {aliases[t] for t in terms if t in aliases}
    collections = {'claims': claims, 'cases': json.loads((refs / 'case-library.json').read_text(encoding='utf-8')), 'scenarios': read_jsonl(refs / 'scenarios.jsonl'), 'topics': topics}
    ranked = []
    for record_kind, rows in collections.items():
        if kind != 'all' and kind != record_kind:
            continue
        for row in rows:
            anchors = [row] if record_kind == 'claims' else [claim_map[c] for c in row['claim_ids']]
            source_ids = sorted({c['source'] for c in anchors})
            topic_keys = {c['topic'] for c in anchors} | {row.get('key'), row.get('topic')}
            if source and source not in source_ids:
                continue
            if topic and topic not in topic_keys:
                continue
            fields = ('paraphrase', 'topic', 'title', 'question', 'response', 'mechanism', 'experiment', 'opening', 'workflow', 'keywords', 'key')
            hay = ' '.join(str(row.get(f, '')) for f in fields).casefold()
            score = sum(3 for t in terms if t in hay) + sum(1 for t in expanded - set(terms) if t in topic_keys)
            if not terms or score:
                ranked.append((score, record_kind, row, source_ids))
    ranked.sort(key=lambda item: (-item[0], item[2]['id']))
    results = []
    for score, record_kind, row, source_ids in ranked[:limit]:
        urls = [{'source': sid, 'url': sources[sid]['url'], 'date': sources[sid]['date'], 'independence_group': sources[sid]['independence_group']} for sid in source_ids]
        result = dict(row, record_type=record_kind, match_score=score, source_links=urls)
        if record_kind == 'claims':
            result['url'] = sources[row['source']]['url']
        results.append(result)
    return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('terms', nargs='*')
    parser.add_argument('--kind', choices=['claims', 'cases', 'scenarios', 'topics', 'all'], default='claims')
    parser.add_argument('--limit', type=int, default=12)
    parser.add_argument('--source', help='Source ID such as S16')
    parser.add_argument('--topic', help='Topic key such as capital')
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be between 1 and 100')
    results = search(ROOT, args.terms, args.kind, args.limit, args.source, args.topic)
    for result in results:
        print(json.dumps(result, ensure_ascii=False))
    if not results:
        print('没有匹配记录；换关键词或阅读 references/knowledge-index.md。')

if __name__ == '__main__':
    main()
