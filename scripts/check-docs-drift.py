#!/usr/bin/env python3
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
skills=sorted(p.parent.name for p in root.glob('*/SKILL.md'))
guides=sorted(p.stem for p in (root/'docs/features').glob('*.md'))
readme=(root/'README.md').read_text(encoding='utf-8')
# Feature table links are present once in each language; compare unique names.
listed=sorted(set(re.findall(r'docs/features/([a-z0-9-]+)\.md', readme)))
failed=False
for label, actual in [('docs/features',guides),('README feature table',listed)]:
    missing=sorted(set(skills)-set(actual)); extra=sorted(set(actual)-set(skills))
    if missing or extra:
        print(f'FAIL  {label} drift: missing={missing} extra={extra}'); failed=True
    else: print(f'OK    {label}: {len(actual)} skills')
# Any explicit current-total statement must match the filesystem.
patterns=[r'目前有\s*(\d+)\s*個技能',r'currently has\s*(\d+)\s*skills',r'全\s*(\d+)\s*スキル']
for pat in patterns:
    for m in re.finditer(pat,readme,re.I):
        if int(m.group(1)) != len(skills):
            print(f'FAIL  README current skill count says {m.group(1)}; filesystem has {len(skills)}'); failed=True
print(f'OK    canonical skill count: {len(skills)}')
sys.exit(1 if failed else 0)
