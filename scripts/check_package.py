"""Check portable package integrity without network or third-party libraries."""
import hashlib
import json
from pathlib import Path
import re
import sys

def check(root):
    root=Path(root).resolve()
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    files=manifest['files']
    for rel,digest in files.items():
        path=root/rel
        if Path(rel).is_absolute() or '..' in Path(rel).parts or path.is_symlink():
            raise ValueError('Unsafe resource path: '+rel)
        if not path.resolve().is_relative_to(root):
            raise ValueError('Resource escaped package: '+rel)
        data=path.read_bytes()
        if hashlib.sha256(data).hexdigest()!=digest:raise ValueError('Changed or missing file: '+rel)
        if path.suffix in ['.md','.json','.jsonl','.yaml','.py']:
            body=data.decode('utf-8')
            if re.search(r'/Users/[A-Za-z0-9_.-]+/',body):raise ValueError('Owner-specific path: '+rel)
        if path.suffix=='.md':
            for link in re.findall(r'\]\(([^)]+)\)',body):
                if re.match(r'[a-z]+:',link) or link.startswith('#'):continue
                dest=path.parent/link.split('#')[0]
                if not dest.resolve().is_relative_to(root) or not dest.exists():
                    raise ValueError('Missing local link: '+rel+' -> '+link)
    sources=json.loads((root/'references/sources.json').read_text(encoding='utf-8'))
    source_ids={x['id'] for x in sources}
    if len(source_ids)!=len(sources):raise ValueError('Duplicate source ID')
    if any(s['independence_group'] not in source_ids for s in sources):raise ValueError('Invalid evidence group')
    claims=[json.loads(line) for line in (root/'references/claims.jsonl').read_text(encoding='utf-8').splitlines()]
    if len({x['id'] for x in claims})!=len(claims):raise ValueError('Duplicate claim ID')
    for c in claims:
        if c['source'] not in source_ids or not c['locator'] or c['is_verbatim']:
            raise ValueError('Invalid claim: '+c['id'])
    claim_ids={c['id'] for c in claims}
    claim_map={c['id']:c for c in claims}
    topics=json.loads((root/'references/topics.json').read_text(encoding='utf-8'))
    cases=json.loads((root/'references/case-library.json').read_text(encoding='utf-8'))
    scenarios=[json.loads(line) for line in (root/'references/scenarios.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    groups=[(topics,'editorial-framework'),(cases,'editorial-application'),(scenarios,'synthetic-application')]
    for records,kind in groups:
        if len({r['id'] for r in records})!=len(records):raise ValueError('Duplicate application ID')
        for r in records:
            if r['evidence_kind']!=kind or not r['claim_ids'] or not set(r['claim_ids'])<=claim_ids:
                raise ValueError('Invalid application references: '+r['id'])
    for t in topics:
        rel='references/'+t['file']
        if rel not in files:raise ValueError('Unbundled topic: '+rel)
    for c in cases:
        if set(c['source_ids'])!={claim_map[i]['source'] for i in c['claim_ids']}:
            raise ValueError('Case source mismatch: '+c['id'])
    stats=json.loads((root/'references/corpus-stats.json').read_text(encoding='utf-8'))
    expected={'source_entries':len(sources),'independent_source_groups':len({s['independence_group'] for s in sources}),
              'claim_records':len(claims),'topic_dossiers':len(topics),'historical_case_records':len(cases),
              'original_dialogue_scenarios':len(scenarios)}
    if any(stats[k]!=v for k,v in expected.items()):raise ValueError('Corpus statistics mismatch')
    skill=(root/'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\nname: xuxiaoyu-skill\n'):raise ValueError('Invalid skill identity')
    version=re.search(r'^  version: "([^"]+)"$',skill,re.M)
    if not version or version.group(1)!=manifest['version']:raise ValueError('Version mismatch')
    if 'TODO' in skill:raise ValueError('Unfinished entrypoint')
    return {'files':len(files),'sources':len(sources),'claims':len(claims),'topics':len(topics),'cases':len(cases),'scenarios':len(scenarios),'offline_resources':'ok'}

if __name__=='__main__':
    try: print(json.dumps(check(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent.parent),ensure_ascii=False))
    except (OSError,ValueError,KeyError) as e:
        print('Package check failed: '+str(e),file=sys.stderr);sys.exit(1)
