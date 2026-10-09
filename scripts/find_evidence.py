"""Optional offline keyword lookup. No embedding service or model required."""
import json
from pathlib import Path
import sys

root=Path(__file__).resolve().parent.parent
terms=[s.casefold() for s in sys.argv[1:]]
sources={s['id']:s for s in json.loads((root/'references/sources.json').read_text(encoding='utf-8'))}
claims=[json.loads(s) for s in (root/'references/claims.jsonl').read_text(encoding='utf-8').splitlines()]
ranked=[]
for c in claims:
    hay=' '.join([c['paraphrase'],c['topic'],sources[c['source']]['title']]).casefold()
    score=sum(t in hay for t in terms)
    if score or not terms:ranked.append((score,c))
for _,c in sorted(ranked,key=lambda x:(-x[0],x[1]['id']))[:12]:
    s=sources[c['source']]
    print(json.dumps({**c,'url':s['url']},ensure_ascii=False))
if not ranked: print('没有匹配命题；换关键词或阅读 references/source-cards.md。')
