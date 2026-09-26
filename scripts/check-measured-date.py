#!/usr/bin/env python3
"""檢查各 SKILL.md 的「實測日」是否過舊。

實測日距今超過 STALE_AFTER_DAYS（預設 90 天）的技能算失敗。
排程執行時由 health-check.yml 自動開 issue，作為再實測的提醒。
沒有實測日標頭的技能只警告（應補上標頭）。
"""
from datetime import date
from pathlib import Path
import re, sys

STALE_AFTER_DAYS = 90
HEADER_RE = re.compile(r'實測日[:：]\s*(\d{4}-\d{2}-\d{2})')

root = Path(__file__).resolve().parents[1]
today = date.today()
stale, missing = [], []
for path in sorted(root.glob('*/SKILL.md')):
    m = HEADER_RE.search(path.read_text(encoding='utf-8'))
    if not m:
        missing.append(path.parent.name)
        continue
    d = date.fromisoformat(m.group(1))
    age = (today - d).days
    status = 'OK  ' if age <= STALE_AFTER_DAYS else 'STALE'
    print(f'{status} {path.parent.name}: 實測日 {d}（{age} 天前）')
    if age > STALE_AFTER_DAYS:
        stale.append((path.parent.name, d, age))

if missing:
    print('WARN  無實測日標頭：' + ', '.join(missing))
if stale:
    print(f'STALE 超過 {STALE_AFTER_DAYS} 天未實測：' + ', '.join(f'{n}（{d}，{a} 天前）' for n, d, a in stale))
    sys.exit(1)
print('OK    全部技能的實測日都在 90 天以內')
