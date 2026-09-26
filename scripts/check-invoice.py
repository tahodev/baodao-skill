#!/usr/bin/env python3
"""對財政部電子發票整合服務平台 lastNumber.html 做煙霧測試。

用 SKILL.md 記載的解析流程（期別標籤 → 第一個「獎別」表格起點）實際解析，
檢查：期別標籤存在、特別獎/特獎都是 8 碼且不重複、頭獎至少一組 8 碼。
分頁連結含「特別獎、特獎中獎清冊」字樣，不從「獎別」起點解析會誤配特獎
（2026-09-26 實測重現），本檢查就是要攔這類版面變化。

網路失敗或地區性擋 IP（部分機房 IP 被 etax 擋）是 WARN skip，不算資料失敗；
只有抓到了頁面但解析結果不合預期才 FAIL。
"""
import re
import sys
import urllib.request

URL = 'https://invoice.etax.nat.gov.tw/lastNumber.html'
UA = {'User-Agent': 'skill-repo-health-check/1.0'}

try:
    req = urllib.request.Request(URL, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        html = r.read().decode('utf-8', 'replace')
except Exception as e:
    print(f'WARN  invoice lastNumber: skipped ({type(e).__name__}: {e}) - known geo/network restriction')
    sys.exit(0)

text = re.sub(r'<[^>]+>', '', html)
text = re.sub(r'\s+', ' ', text)
m = re.search(r'(1\d\d年\d\d-\d\d月)中獎號碼單', text)
if not m:
    print('FAIL  invoice lastNumber: 找不到期別標籤（版面可能改版）')
    sys.exit(1)
start = text.find('獎別', m.end())
if start < 0:
    print(f'FAIL  invoice lastNumber: 期別 {m.group(1)} 後找不到「獎別」表格起點')
    sys.exit(1)
seg = text[start:start + 1200]

def prize8(label):
    i = seg.find(label)
    n = re.search(r'\d{8}', seg[i:i + 100]) if i >= 0 else None
    return n.group(0) if n else None

sp, st = prize8('特別獎'), prize8('特獎')
i = seg.find('頭獎')
j = seg.find('同期', i)
heads = re.findall(r'\d{8}', seg[i:j if j > i else i + 200]) if i >= 0 else []

failed = False
if not sp or not st:
    print(f'FAIL  invoice lastNumber: 特別獎={sp} 特獎={st}（應各為 8 碼）')
    failed = True
elif sp == st:
    print(f'FAIL  invoice lastNumber: 特別獎與特獎同號 {sp}（分頁連結誤配？）')
    failed = True
if not heads:
    print('FAIL  invoice lastNumber: 找不到頭獎號碼')
    failed = True

if failed:
    sys.exit(1)
print(f'OK    invoice lastNumber: {m.group(1)} 特別獎 {sp}、特獎 {st}、頭獎 {len(heads)} 組')
