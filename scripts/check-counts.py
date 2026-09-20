#!/usr/bin/env python3
"""Re-verify the headline record counts documented in SKILL.md files.

Catches silent upstream data growth/shrinkage that a URL 200 check cannot see
(e.g. museum directory gains a venue, library list adds rows). On mismatch the
health-check workflow opens an issue so the docs get re-verified and updated.
Network required; stdlib only.
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


# taiwan-museum: 144 venues
data = json.loads(fetch('https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=H'))
check('taiwan-museum venue count', len(data), 144)

# taiwan-library: 5,207 rows; 公共圖書館 exact 610, contains 644
raw = fetch('https://www.ncl.edu.tw/OpenDataFile/0Q112417873324994331/4cbfc49a-1127-45b1-9da6-113ebb444a12')
rows = list(csv.reader(io.StringIO(raw.decode('big5', errors='replace'))))
data_rows = [r for r in rows[1:] if len(r) >= 7]
check('taiwan-library row count', len(data_rows), 5207)
exact = sum(1 for r in data_rows if r[6].strip() == '公共圖書館')
contains = sum(1 for r in data_rows if '公共圖書館' in r[6])
check('taiwan-library 公共圖書館 exact', exact, 610)
check('taiwan-library 公共圖書館 contains', contains, 644)

# taiwan-hospital: 37,127 providers
data = json.loads(fetch('https://info.nhi.gov.tw/api/iode0010/v1/rest/datastore/A21030000I-D2100G-001?limit=1'))
check('taiwan-hospital provider total', data['result']['total'], 37133)

# taiwan-parking: 1,177 real-time lots, 1,773 static lots
data = json.loads(fetch('https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json'))
check('taiwan-parking realtime lots', len(data['data']['park']), 1174)
data = json.loads(fetch('https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_alldesc.json'))
check('taiwan-parking static lots', len(data['data']['park']), 1773)

sys.exit(1 if failed else 0)
