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

# Content-level checks: every fact a feature note states must exist in its SKILL.md.
# 1) URLs in the feature note must also appear in the SKILL.
# 2) Numbers carrying a unit (館/校/列/筆/站/場/縣市/學年度) in the feature note
#    must also appear in the SKILL (catches count drift like 144 vs 145).
# Dates (2026-09-19) and version-like numbers are ignored.
def urls(t):
    # Compare scheme://host/path only; query strings often carry placeholder
    # params ($KEY, <代號>, YYYYMMDD, ...) that legitimately differ between
    # the SKILL's worked example and the feature note's template.
    out=set()
    for u in re.findall(r'https?://[^\s)\]>"\'`（）【】、，。；：「」]+', t):
        out.add(u.split('?')[0].rstrip('/').lower())
    return out
def unit_numbers(t):
    out=set()
    for m in re.finditer(r'(\d[\d,]*)\s*(館|校|列|筆|站|場|縣市|學年度)', t):
        out.add(m.group(1).replace(',',''))
    return out
for s in skills:
    sk=(root/s/'SKILL.md').read_text(encoding='utf-8')
    fn=(root/'docs/features'/f'{s}.md').read_text(encoding='utf-8')
    extra_urls=urls(fn)-urls(sk)
    if extra_urls:
        print(f'FAIL  {s}: feature note URL not in SKILL: {sorted(extra_urls)[:3]}'); failed=True
    extra_nums=unit_numbers(fn)-unit_numbers(sk)
    if extra_nums:
        print(f'FAIL  {s}: feature note unit-number not in SKILL: {sorted(extra_nums)}'); failed=True
print(f'OK    content check: {len(skills)} feature notes vs SKILLs (URLs, unit numbers)')
sys.exit(1 if failed else 0)
