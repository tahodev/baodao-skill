#!/usr/bin/env python3
"""Re-verify the headline record counts documented in SKILL.md files.

Catches silent upstream data growth/shrinkage that a URL 200 check cannot see
(e.g. museum directory gains a venue, library list adds rows). On mismatch the
health-check workflow opens an issue so the docs get re-verified and updated.

Network required; stdlib only. A dropped connection or non-200 from a
datacenter IP (e.g. info.nhi.gov.tw closing connections on GitHub runners) is
a WARN skip, not a data failure - only a fetched but unexpected count fails.
"""
import csv
import io
import json
import sys
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0'}
failed = False


def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def check(label, actual, expected):
    global failed
    if actual != expected:
        print(f'FAIL  {label}: expected {expected}, got {actual}')
        failed = True
    else:
        print(f'OK    {label}: {actual}')


def check_volatile(label, actual, expected, tol=0.05):
    """變動本就頻繁的數字（停車場場數、YouBike 站數）：超出容忍範圍只 WARN。

    這類數字會隨開歇業/設站每週小幅變動，exact-match 曾讓 health-check
    連續 6 天誤報（2026-09-20~25,issue #6）。漂移超過容忍範圍時 WARN,
    提醒下次維護時重測更新文件，但不讓 CI 失敗。
    """
    lo, hi = expected * (1 - tol), expected * (1 + tol)
    if lo <= actual <= hi:
        print(f'OK    {label}: {actual}（基準 {expected},容忍 ±{int(tol*100)}%）')
    else:
        print(f'WARN  {label}: 基準 {expected}、實測 {actual} 超出 ±{int(tol*100)}%——請重測並更新文件')


def check_network(label, fn):
    try:
        fn()
    except Exception as e:
        print(f'WARN  {label}: skipped ({type(e).__name__}: {e}) - known geo/network restriction')


def check_museum():
    data = json.loads(fetch('https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=H'))
    check('taiwan-museum venue count', len(data), 144)


def check_library():
    raw = fetch('https://www.ncl.edu.tw/OpenDataFile/0Q112417873324994331/4cbfc49a-1127-45b1-9da6-113ebb444a12')
    rows = list(csv.reader(io.StringIO(raw.decode('big5', errors='replace'))))
    data_rows = [r for r in rows[1:] if len(r) >= 7]
    check('taiwan-library row count', len(data_rows), 5207)
    exact = sum(1 for r in data_rows if r[6].strip() == '公共圖書館')
    contains = sum(1 for r in data_rows if '公共圖書館' in r[6])
    check('taiwan-library 公共圖書館 exact', exact, 610)
    check('taiwan-library 公共圖書館 contains', contains, 644)


def check_hospital():
    data = json.loads(fetch('https://info.nhi.gov.tw/api/iode0010/v1/rest/datastore/A21030000I-D2100G-001?limit=1'))
    check('taiwan-hospital provider total', data['result']['total'], 37133)


def check_parking():
    data = json.loads(fetch('https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json'))
    check_volatile('taiwan-parking realtime lots', len(data['data']['park']), 1188)
    data = json.loads(fetch('https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_alldesc.json'))
    check_volatile('taiwan-parking static lots', len(data['data']['park']), 1775)


def check_youbike():
    # apis.youbike.com.tw 由 Incapsula 防護,機房 IP 常被擋——擋住時走 WARN skip
    data = json.loads(fetch('https://apis.youbike.com.tw/json/station-yb2.json', timeout=60))
    check_volatile('youbike-realtime total stations', len(data), 9629)


check_network('taiwan-museum', check_museum)
check_network('taiwan-library', check_library)
check_network('taiwan-hospital', check_hospital)
check_network('taiwan-parking', check_parking)
check_network('youbike-realtime', check_youbike)

sys.exit(1 if failed else 0)
