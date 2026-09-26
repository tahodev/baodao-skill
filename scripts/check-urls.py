#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import json, re, subprocess, sys, threading, time
root=Path(__file__).resolve().parents[1]
MAX_WORKERS=8; TIMEOUT=20
# 已知會依來源 IP 擋連線的網域：000/401/403/429/5xx 降為 WARN。
# 404 不在此列——白名單網域上的 404 是真的連結失效,要 FAIL。
WARN_HOSTS={'you-bike.com.tw', 'invoice.etax.nat.gov.tw', 'info.nhi.gov.tw', 'data.ntpc.gov.tw', 'data.taipei', 'etax.nat.gov.tw', 'opendata.cwa.gov.tw', 'alerts.ncdr.nat.gov.tw', 'opendata.tycg.gov.tw', 'youbike.com.tw', 'data.gov.tw', 'newdatacenter.taichung.gov.tw', 'stats.moe.gov.tw'}
OPENAPI_HOSTS={'opendata.cwa.gov.tw'}
# 文件裡的 URL 模式（帶 <期別> 等占位說明、或參數空著的前綴）不是可抓取的端點,跳過。
SKIP_URLS={
 'https://www.etax.nat.gov.tw/etw-main/ETW183W2_',  # URL 規則前綴,實際網址帶期別（JS 頁面）
 'https://alerts.ncdr.nat.gov.tw/RssAtomFeed.ashx?AlertType=',  # 類型代碼空參數的說明用前綴
}
url_re=re.compile(r'https?://[^ )"`\'。，、；：（）<>]+')
# 本倉庫實際用到的模板變數（台灣技能）：CWA 授權碼與 MOENV API 金鑰
placeholders={'CWA_API_KEY':'INVALID_CI_KEY','MOENV_API_KEY':'INVALID_CI_KEY'}
items={}
for path in root.glob('*/SKILL.md'):
    for raw in url_re.findall(path.read_text(encoding='utf-8')):
        url=raw.rstrip('.,;。,)}')
        if 'schemas.openxmlformats.org' in url: continue
        if url in SKIP_URLS: continue
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
    pats=[r'ERROR-[0-9]+',r'"(?:resultCode|returnCode)"\s*:\s*"?(?!00\b|INFO-000\b|0\b)([A-Z0-9_-]+)',r'<resultCode>\s*(?!00<)([^<]+)',
          r'該 API KEY [^。]*',r'API KEY\s*(不存在|已經到期|無效)']  # MOENV：HTTP 200 但回純文字金鑰錯誤
    for p in pats:
        m=re.search(p,body,re.I)
        if m: return m.group(0)[:120]
    return None

# 輸出時遮蔽 URL 裡的金鑰值（data.gov.tw 公布的資料集 key 雖非個人秘密,也不刷進 CI 記錄）
def redact(url):
    return re.sub(r'(api_key=)[0-9a-fA-F-]{8,}', r'\1***', url)

# NCDR 公開 feed 有 3 秒速率限制（429 限制存取間隔時間為3秒）：同網域請求逐一排隊
_ncdr_lock=threading.Lock()
_ncdr_last=[0.0]
def ncdr_throttle(h):
    if h!='alerts.ncdr.nat.gov.tw': return
    with _ncdr_lock:
        wait=3.0-(time.time()-_ncdr_last[0])
        if wait>0: time.sleep(wait)
        _ncdr_last[0]=time.time()

def check(pair):
    original,owners=pair; url=materialize(original)
    owner=', '.join(sorted(owners))
    if not url: return ('SKIP',f'{owner}: {redact(original)} (runtime shell variable)')
    h=host(url)
    ncdr_throttle(h)
    try:
        p=subprocess.run(['curl','-sS','-L','--connect-timeout','8','--max-time',str(TIMEOUT),'-A','skill-repo-health-check/1.0','-w','\n%{http_code}',url],capture_output=True,timeout=TIMEOUT+5)
        p.stdout=p.stdout.decode('utf-8','replace')
        body,_,code=p.stdout.rpartition('\n'); code=code.strip() or '000'
    except subprocess.TimeoutExpired: body=''; code='000'
    templated=original!=url
    disp=redact(original)
    if warning_host(h) and (code=='000' or code in ('401','403','429') or code.startswith('5')): return ('WARN',f'{owner}: {code} {disp} (known geo/network restriction)')
    if code=='000': return ('FAIL',f'{owner}: 000 {disp}')
    if code.startswith(('2','3')):
        err=api_error(body[:200000])
        if err:
            if templated and openapi_host(h): return ('OK',f'{owner}: {code} {disp} (template probe returned expected API status: {err})')
            # MOENV：金鑰錯誤是 HTTP 200+純文字。占位/空金鑰的探測回此錯誤屬預期;
            # 但文件中實際刊載的公布金鑰若回此錯誤,代表金鑰失效,要 FAIL。
            if h.endswith('data.moenv.gov.tw') and re.search(r'(INVALID_CI_KEY|ci-probe|api_key=$|api_key={})', url):
                return ('OK',f'{owner}: {code} {disp} (endpoint exists; API key required: {err})')
            return ('FAIL',f'{owner}: {code} {disp} (API-level error: {err})')
        return ('OK',f'{owner}: {code} {disp}')
    if code in ('400','401','403') and openapi_host(h): return ('OK',f'{owner}: {code} {disp} (endpoint exists; auth/parameters required)')
    return ('FAIL',f'{owner}: {code} {disp}')

failed=False
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures=[pool.submit(check,x) for x in items.items()]
    for f in as_completed(futures):
        status,msg=f.result(); print(f'{status:5} {msg}')
        failed |= status=='FAIL'
print(f'Checked {len(items)} unique URLs with {MAX_WORKERS} workers and {TIMEOUT}s/request cap')
sys.exit(1 if failed else 0)
