#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json, re, subprocess, sys
root=Path(__file__).resolve().parents[1]
MAX_WORKERS=8; TIMEOUT=20
WARN_HOSTS={'you-bike.com.tw', 'invoice.etax.nat.gov.tw', 'info.nhi.gov.tw', 'data.ntpc.gov.tw', 'data.taipei', 'etax.nat.gov.tw', 'opendata.cwa.gov.tw', 'alerts.ncdr.nat.gov.tw', 'opendata.tycg.gov.tw', 'youbike.com.tw', 'data.gov.tw', 'newdatacenter.taichung.gov.tw'}
OPENAPI_HOSTS={'opendata.cwa.gov.tw'}
url_re=re.compile(r'https?://[^ )"`\'。，、；：（）<>]+')
placeholders={'KEY':'INVALID_CI_KEY','SEOUL_KEY':'sample','KEXIM_KEY':'INVALID_CI_KEY','ECOS_KEY':'sample','CONTENT_ID':'126508','STATION_ID':'SUB0002','STN_ID':'108','TM_SEQ':'1','DEP_ID':'NAEK010','ARR_ID':'NAEK300','LON':'126.9780','LAT':'37.5665','START':'20260901','END':'20260930','AREA_NM':'%EB%AA%85%EB%8F%99','BASE_DATE':'20260919','TRAVEL_DATE':'20260919','RATE_DATE':'20260919','MONTH':'2026-09','TM_FC':'202609190600','CWA_API_KEY':'INVALID_CI_KEY'}
items={}
for path in root.glob('*/SKILL.md'):
    for raw in url_re.findall(path.read_text(encoding='utf-8')):
        url=raw.rstrip('.,;。,)}')
        if 'schemas.openxmlformats.org' in url: continue
        items.setdefault(url,set()).add(str(path.relative_to(root)))

def materialize(url):
    def sub(m): return placeholders.get(m.group(1),'ci-probe')
    url=re.sub(r'\{([A-Za-z_][A-Za-z0-9_]*)\}',sub,url)
    url=re.sub(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}',sub,url)
    return re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)',sub,url)

def host(url): return re.match(r'https?://([^/:]+)',url).group(1).lower()
def warning_host(h): return any(h==x or h.endswith('.'+x) for x in WARN_HOSTS)
def openapi_host(h): return any(h==x or h.endswith('.'+x) for x in OPENAPI_HOSTS)
def api_error(body):
    pats=[r'ERROR-[0-9]+',r'"(?:resultCode|returnCode)"\s*:\s*"?(?!00\b|INFO-000\b|0\b)([A-Z0-9_-]+)',r'<resultCode>\s*(?!00<)([^<]+)']
    for p in pats:
        m=re.search(p,body,re.I)
        if m: return m.group(0)[:120]
    return None

def check(pair):
    original,owners=pair; url=materialize(original)
    owner=', '.join(sorted(owners))
    if not url: return ('SKIP',f'{owner}: {original} (runtime shell variable)')
    h=host(url)
    try:
        p=subprocess.run(['curl','-sS','-L','--connect-timeout','8','--max-time',str(TIMEOUT),'-A','skill-repo-health-check/1.0','-w','\n%{http_code}',url],capture_output=True,timeout=TIMEOUT+5)
        p.stdout=p.stdout.decode('utf-8','replace')
        body,_,code=p.stdout.rpartition('\n'); code=code.strip() or '000'
    except subprocess.TimeoutExpired: body=''; code='000'
    templated=original!=url
    if warning_host(h) and (code=='000' or not code.startswith(('2','3'))): return ('WARN',f'{owner}: {code} {original} (known geo/network restriction)')
    if code=='000': return ('FAIL',f'{owner}: 000 {original}')
    if code.startswith(('2','3')):
        err=api_error(body[:200000])
        if err:
            if templated and openapi_host(h): return ('OK',f'{owner}: {code} {original} (template probe returned expected API status: {err})')
            return ('FAIL',f'{owner}: {code} {original} (API-level error: {err})')
        return ('OK',f'{owner}: {code} {original}')
    if code in ('400','401','403') and openapi_host(h): return ('OK',f'{owner}: {code} {original} (endpoint exists; auth/parameters required)')
    return ('FAIL',f'{owner}: {code} {original}')

failed=False
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures=[pool.submit(check,x) for x in items.items()]
    for f in as_completed(futures):
        status,msg=f.result(); print(f'{status:5} {msg}')
        failed |= status=='FAIL'
print(f'Checked {len(items)} unique URLs with {MAX_WORKERS} workers and {TIMEOUT}s/request cap')
sys.exit(1 if failed else 0)
