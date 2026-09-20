#!/usr/bin/env python3
"""Execute the code documented in SKILL.md files against known-good vectors.

Catches regressions where an edit changes documented code or data-shape
examples away from their verified behavior (e.g. the taiwan-schools slice bug).
Run: python3 tests/test_documented_code.py  (stdlib only, no network)
"""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failures = []


def check(label, actual, expected):
    if actual != expected:
        failures.append(f'{label}: expected {expected!r}, got {actual!r}')


def python_blocks(path):
    text = path.read_text(encoding='utf-8')
    return re.findall(r'```python\n(.*?)```', text, re.S)


def heredoc_python_blocks(path):
    """Extract python code from ```bash blocks that use python3 - <<'PY'."""
    text = path.read_text(encoding='utf-8')
    out = []
    for block in re.findall(r'```bash\n(.*?)```', text, re.S):
        m = re.search(r"<<'PY'\n(.*?)\nPY", block, re.S)
        if m:
            out.append(m.group(1))
    return out


# --- taiwan-lunar-cal -------------------------------------------------------
ns = {}
for block in python_blocks(ROOT / 'taiwan-lunar-cal' / 'SKILL.md')[:2]:
    exec(block, ns)
check('LUNAR_INFO length', len(ns['LUNAR_INFO']), 201)
to_lunar = ns['to_lunar']
# Anchors documented in SKILL.md (verified 2026-09-19 vs CWA tables)
check('2026-02-17 春節', to_lunar(datetime.date(2026, 2, 17)), (2026, 1, 1, False))
check('2026-09-25 中秋', to_lunar(datetime.date(2026, 9, 25)), (2026, 8, 15, False))
check('2025-10-06 中秋', to_lunar(datetime.date(2025, 10, 6)), (2025, 8, 15, False))
check('2025-07-25 閏六月初一', to_lunar(datetime.date(2025, 7, 25)), (2025, 6, 1, True))
check('2026-02-16 除夕(小月廿九)', to_lunar(datetime.date(2026, 2, 16)), (2025, 12, 29, False))
std = ns['solar_term_date']
check('2026 清明', std(2026, '清明'), datetime.date(2026, 4, 5))
check('2026 冬至', std(2026, '冬至'), datetime.date(2026, 12, 22))
check('2026 秋分', std(2026, '秋分'), datetime.date(2026, 9, 23))
check('2024 春分', std(2024, '春分'), datetime.date(2024, 3, 20))
check('zodiac 2026', ns['zodiac'](2026), '馬')

# --- taiwan-id-check --------------------------------------------------------
ns = {}
for block in heredoc_python_blocks(ROOT / 'taiwan-id-check' / 'SKILL.md'):
    exec(block, ns)
# Vectors documented in SKILL.md (verified 2026-09-19)
check('UBN 22099131 台積電', ns['ubn_ok']('22099131'), True)
check('UBN 96979933 中華電信', ns['ubn_ok']('96979933'), True)
check('UBN 97176270 特例', ns['ubn_ok']('97176270'), True)
check('UBN 22099132 非法', ns['ubn_ok']('22099132'), False)
check('ID A123456789', ns['pid_ok']('A123456789'), True)
check('ID B221003265', ns['pid_ok']('B221003265'), True)
check('ID A123456788 非法', ns['pid_ok']('A123456788'), False)

if failures:
    print('FAIL')
    for f in failures:
        print(' -', f)
    sys.exit(1)
print('OK    documented-code tests: taiwan-lunar-cal (10), taiwan-id-check (7)')
