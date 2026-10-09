"""Freeze hashes after intentional source updates."""
import hashlib
import json
import re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
files={}
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root)
    if not p.is_file() or p.name=='manifest.json' or any(x.startswith('.') or x=='__pycache__' for x in rel.parts):continue
    if p.suffix=='.pyc':continue
    files[rel.as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
version=re.search(r'^  version: "([^"]+)"$',(root/'SKILL.md').read_text(encoding='utf-8'),re.M).group(1)
(root/'manifest.json').write_text(json.dumps({'name':'xuxiaoyu-skill','version':version,'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Manifest files:',len(files))
