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


# --- taiwan-schools（欄位切片回歸）-------------------------------------------
# 2026-09-19 修過 r[11:23] 誤切（多算 6 年級班級數、漏 6 年級女學生數）。
# 固定樣本：114 學年度私立淡江高中附設國小部（新北市淡水區,代碼 011301）,
# 取自 114_basec.csv 原列（2026-09-26 對原檔重算：16 班、498 名學生）。
SCHOOL_ROW = ['114', '01', '新北市', '淡水區', '011301', '私立淡江高中附設國小部',
              '2', '2', '3', '3', '3', '3',
              '38', '32', '33', '36', '44', '49', '48', '55', '42', '40', '37', '44',
              '28', '37', '8', '16', '0', '3']
classes = sum(int(x) for x in SCHOOL_ROW[6:12] if x.isdigit())   # 欄 6-11:1-6 年級班級數
students = sum(int(x) for x in SCHOOL_ROW[12:24] if x.isdigit())  # 欄 12-23:1-6 年級男+女學生數
check('taiwan-schools 011301 班級數', classes, 16)
check('taiwan-schools 011301 學生數', students, 498)

# --- invoice-winning-numbers（分頁連結誤配回歸）------------------------------
# 2026-09-26 實測重現：頁首/頁尾分頁連結含「115年05-06月特別獎、特獎中獎清冊」,
# 從期別標籤直接往後掃會把「特獎」對到清冊連結,讀出特別獎的號碼。
# 下面 fixture 重現同樣的版面結構（號碼為虛構）。SKILL.md 的解析流程是
# 從期別標籤後第一個「獎別」表格起點開始,此測試執行文件中的程式驗證不誤配。
INVOICE_FIXTURE = """
115年07-08月中獎號碼單 115年05-06月中獎號碼單 115年05-06月特別獎、特獎中獎清冊 Previous
115年07-08月中獎號碼單 115年05-06月中獎號碼單 115年05-06月特別獎、特獎中獎清冊 Next
獎別 中獎號碼 特別獎 38548029 同期統一發票收執聯8位數號碼與特別獎號碼相同者獎金1,000萬元
特獎 10138845 同期統一發票收執聯8位數號碼與特獎號碼相同者獎金200萬元
頭獎 24121106 28589937 83663333 同期統一發票收執聯8位數號碼與頭獎號碼相同者獎金20萬元
領獎期間自115年08月06日起至115年11月05日止
"""
# 執行 SKILL.md 記載的解析程式（heredoc 第一段）,fixture 寫到它讀取的 /tmp 路徑
import contextlib as _cl, io as _io
Path('/tmp/lastNumber.html').write_text(INVOICE_FIXTURE, encoding='utf-8')
ns = {'__name__': '__main__'}
block = heredoc_python_blocks(ROOT / 'invoice-winning-numbers' / 'SKILL.md')[0]
buf = _io.StringIO()
with _cl.redirect_stdout(buf):
    exec(block, ns)
out = buf.getvalue()
check('invoice fixture 期別', '115年07-08月' in out, True)
check('invoice fixture 特別獎', '特別獎 38548029' in out, True)
check('invoice fixture 特獎（不誤配清冊連結）', '特獎 10138845' in out, True)
check('invoice fixture 頭獎 3 組', "頭獎 ['24121106', '28589937', '83663333']" in out, True)

if failures:
    print('FAIL')
    for f in failures:
        print(' -', f)
    sys.exit(1)
print('OK    documented-code tests: taiwan-lunar-cal (10), taiwan-id-check (7), taiwan-schools (2), invoice-winning-numbers (4)')
