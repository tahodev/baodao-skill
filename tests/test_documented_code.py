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


def run_python_block(code):
    """執行文件中的 python 區塊並回傳 stdout（不複製公式,直接跑文件程式）。"""
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {'__name__': '__main__'})
    return buf.getvalue()


def bash_blocks(path):
    return re.findall(r'```bash\n(.*?)```', path.read_text(encoding='utf-8'), re.S)


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
# Vectors documented in SKILL.md (verified 2026-09-19; 10000073 特例鑑別向量 2026-09-30 新增)
check('UBN 22099131 台積電', ns['ubn_ok']('22099131'), True)
check('UBN 96979933 中華電信', ns['ubn_ok']('96979933'), True)
check('UBN 97176270 合法(走一般路徑,不鑑別特例)', ns['ubn_ok']('97176270'), True)
check('UBN 10000073 特例鑑別(無特例實作會誤判非法)', ns['ubn_ok']('10000073'), True)
check('UBN 22099132 非法', ns['ubn_ok']('22099132'), False)
check('ID A123456789', ns['pid_ok']('A123456789'), True)
check('ID B221003265', ns['pid_ok']('B221003265'), True)
check('ID A123456788 非法', ns['pid_ok']('A123456788'), False)


# --- taiwan-schools（欄位切片回歸）-------------------------------------------
# 2026-09-19 修過 r[11:23] 誤切（多算 6 年級班級數、漏 6 年級女學生數）。
# 固定樣本改寫自 114_basec.csv 原列（淡江高中附設國小部,2026-09-26 對原檔重算：16 班、498 名學生）,
# 縣市改成臺南市以符合文件範例的篩選條件。這裡抽出並執行 SKILL.md 的篩選程式,不是複製公式。
import csv as _csv, contextlib as _cl, io as _io
SCHOOL_ROW = ['114', '01', '臺南市', '淡水區', '011301', '私立淡江高中附設國小部',
              '2', '2', '3', '3', '3', '3',
              '38', '32', '33', '36', '44', '49', '48', '55', '42', '40', '37', '44',
              '28', '37', '8', '16', '0', '3']
with open('/tmp/basec114.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    w = _csv.writer(fh)
    w.writerow(['學年度'] + ['c%d' % i for i in range(1, 30)])
    w.writerow(SCHOOL_ROW)
    w.writerow(['114', '01', '新北市'] + SCHOOL_ROW[3:])     # 非目標縣市,不應被輸出
out = run_python_block(python_blocks(ROOT / 'taiwan-schools' / 'SKILL.md')[0])
check('taiwan-schools 文件程式輸出', out.strip(), '私立淡江高中附設國小部 淡水區 16 班 498 名學生')

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

# --- taiwan-id-check 異常輸入（非 ASCII 不可丟例外）------------------------------
ns = {}
for block in heredoc_python_blocks(ROOT / 'taiwan-id-check' / 'SKILL.md'):
    exec(block, ns)
for bad in ['２２０９９１３１', '2209913\u00b9', '', None, '٢٢٠٩٩١٣١', '2209913']:
    try:
        check(f'UBN 異常輸入 {bad!r}', ns['ubn_ok'](bad), False)
    except Exception as e:  # noqa
        failures.append(f'UBN 異常輸入 {bad!r} 丟出 {type(e).__name__}')
for bad, want in [('Ａ１２３４５６７８９', False), ('A12345678\u0669', False), ('A12345678\u00b2', False),
                  ('A323456789', False), ('\u0131123456789', False), ('', False), (None, False),
                  ('a123456789', True)]:
    try:
        check(f'ID 輸入 {bad!r}', ns['pid_ok'](bad), want)
    except Exception as e:  # noqa
        failures.append(f'ID 輸入 {bad!r} 丟出 {type(e).__name__}')

# --- taiwan-stock 漲幅排序（比例,不是價差絕對值）-----------------------------------
import json as _json, subprocess as _sp, shutil as _sh
if _sh.which('jq'):
    STOCK = [
        {'Code': '1111', 'Name': '高價小漲', 'ClosingPrice': '1000.00', 'Change': '30.0000'},   # +3.09%
        {'Code': '2222', 'Name': '低價大漲', 'ClosingPrice': '11.00', 'Change': '1.0000'},      # +10%
        {'Code': '3333', 'Name': '停牌', 'ClosingPrice': '', 'Change': '0.0000'},
        {'Code': '4444', 'Name': '昨收為零', 'ClosingPrice': '5.00', 'Change': '5.0000'},
        {'Code': '5555', 'Name': '下跌', 'ClosingPrice': '9.00', 'Change': '-1.0000'},
    ]
    Path('/tmp/twse.json').write_text(_json.dumps(STOCK), encoding='utf-8')
    cmd = [b for b in bash_blocks(ROOT / 'taiwan-stock' / 'SKILL.md') if '漲幅前 10' in b][0]
    res = _sp.run(['bash', '-c', cmd], capture_output=True, text=True)
    lines = res.stdout.strip().splitlines()
    top = [l for l in lines if l.startswith(('1111', '2222', '3333', '4444', '5555'))]
    check('taiwan-stock 漲幅榜首為低價大漲', top[0].split()[0] if top else None, '2222')
    check('taiwan-stock 略過空值與昨收為零', [l.split()[0] for l in top], ['2222', '1111', '5555'])
else:
    print('SKIP  taiwan-stock: jq not installed')

# --- taiwan-suspension 解析（公告列+頁尾備註 fixture,合成）--------------------------
SUSP_HEAD = """<TABLE id="Table"><TR class="Table_Head"><TH>縣市名稱</TH><TH>是否停止上班上課情形</TH></TR>
<TBODY class="Table_Body">"""
SUSP_FOOT = """<TR style="background:#ccc"><TD colspan=3><p>4.適用範圍為各級政府機關…停止上班…</p></TD></TR></TBODY></TABLE>
<div class="alert_msg">二、全日或上午半日停止上班、停止上課…</div>"""
susp = python_blocks(ROOT / 'taiwan-suspension' / 'SKILL.md')[0]
Path('/tmp/nds.html').write_text(SUSP_HEAD + """<TR><TD headers='city_Name' colspan='2'><h2>無停班停課訊息。</h2></TD></TR>""" + SUSP_FOOT, encoding='utf-8')
check('suspension 正常日', run_python_block(susp).strip(), '全國正常上班上課（頁面無停班停課公告）')
Path('/tmp/nds.html').write_text(SUSP_HEAD + """<TR><TD>高雄市</TD><TD>今天停止上班、停止上課。</TD></TR>
<TR><TD>屏東縣</TD><TD>今天停止上課。</TD></TR>""" + SUSP_FOOT, encoding='utf-8')
out = run_python_block(susp).strip().splitlines()
check('suspension 有公告：縣市與內容', out, ['高雄市：今天停止上班、停止上課。', '屏東縣：今天停止上課。'])
check('suspension 不混入頁尾', any('適用範圍' in l or '二、' in l for l in out), False)

# --- taiwan-hospital 篩選程式讀得到分頁存檔 -----------------------------------------
hosp_blocks = python_blocks(ROOT / 'taiwan-hospital' / 'SKILL.md')
check('hospital 分頁區塊存 /tmp/hosp.json', "open('/tmp/hosp.json', 'w')" in hosp_blocks[0], True)
Path('/tmp/hosp.json').write_text(_json.dumps({'result': {'total': 2, 'records': [
    {'HOSP_NAME': '臺大醫院', 'HOSP_ADDR': '臺北市中正區', 'TEL_AREA': '02', 'TEL': '23123456'},
    {'HOSP_NAME': '某診所', 'HOSP_ADDR': '高雄市', 'TEL_AREA': '07', 'TEL': '1111111'}]}}), encoding='utf-8')
check('hospital 篩選程式輸出', run_python_block(hosp_blocks[1]).strip(), '臺大醫院 臺北市中正區 (02)23123456')

# --- taiwan-toilet nearest：跨頁合併後排序、經緯度任一缺值略過 ---------------------------
toilet = python_blocks(ROOT / 'taiwan-toilet' / 'SKILL.md')
rows = [
    {'name': '第一頁遠', 'address': 'A', 'grade': '優等級', 'latitude': '25.10', 'longitude': '121.60'},
    {'name': '缺經度', 'address': 'B', 'grade': '特優級', 'latitude': '25.04', 'longitude': ''},
    {'name': '缺緯度', 'address': 'C', 'grade': '特優級', 'latitude': '', 'longitude': '121.51'},
    {'name': '第二頁近', 'address': 'D', 'grade': '特優級', 'latitude': '25.0401', 'longitude': '121.5101'},
]
Path('/tmp/toilet_all.json').write_text(_json.dumps(rows, ensure_ascii=False), encoding='utf-8')
out = run_python_block(toilet[1]).strip().splitlines()
check('toilet 最近一筆來自後面頁面', out[0].split()[1] if out else None, '第二頁近')
check('toilet 缺值筆數被略過', any(('缺經度' in l or '缺緯度' in l) for l in out), False)

if failures:
    print('FAIL')
    for f in failures:
        print(' -', f)
    sys.exit(1)
print('OK    documented-code tests: lunar-cal, id-check (含異常輸入), schools (執行文件程式), invoice, stock, suspension, hospital, toilet')
