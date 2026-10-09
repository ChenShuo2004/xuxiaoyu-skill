"""Create a merged conversation prompt for hosts without local file tools."""
from pathlib import Path
import re
root=Path(__file__).resolve().parent.parent
body=(root/'SKILL.md').read_text(encoding='utf-8').split('---',2)[2]
body=body.split('## 需要细节时才读取')[0]
pieces=['# 徐霄羽 · 单文件对话版\n\n将本文作为对话说明使用。所有必要资料已经内嵌，无需读取任何本地文件或访问网站；外部链接仅用于用户主动核验。默认与用户自然对话，直到用户退出人物模式。本文是公开材料的模拟视角，不是本人。',body]
for rel in ['references/persona.md','references/dialogue.md','references/source-cards.md']:
    text=(root/rel).read_text(encoding='utf-8')
    text=re.sub(r'\[([^]]+)\]\((?!https?://)[^)]+\)',r'\1（见本文对应部分）',text)
    pieces.append(text)
target=root/'portable/徐霄羽-单文件对话版.md'
target.parent.mkdir(exist_ok=True)
target.write_text('\n\n---\n\n'.join(pieces).strip()+'\n',encoding='utf-8')
print('Portable prompt created.')
