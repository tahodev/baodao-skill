---
name: invoice-winning-numbers
description: 從財政部電子發票整合服務平台查統一發票最新中獎號碼並對獎。發票對獎、統一發票、中獎號碼、特別獎、特獎、頭獎、增開六獎、兌獎期限的問題適用。免 API 金鑰、免登入。雲端發票專屬獎在另一頁（cloudNowNumber.html），本技能內有對應查法。發票以外的稅務申報、記帳問題不適用。
license: MIT
metadata:
  category: finance
  locale: zh-TW
---

# invoice-winning-numbers

從財政部電子發票整合服務平台（https://invoice.etax.nat.gov.tw）的公開頁面取得統一發票中獎號碼，並用手上的發票號碼對獎。不需要 API 金鑰或登入，`curl` 即可。

## 基本流程

1. 下載最新中獎號碼頁
2. 移除 HTML 標籤後解析期別與各獎號碼
3. 用使用者的 8 位發票號碼對獎

### 1. 下載頁面

```bash
curl -sm 30 https://invoice.etax.nat.gov.tw/lastNumber.html -o /tmp/lastNumber.html
```

2026-09-09 實測:HTTP 200、約 20KB、不需特殊 User-Agent。頁面含最新一期的「中獎號碼單」（當日為 115年05-06月，特別獎 19531471、特獎 85941329、頭獎 07225810 / 20231230 / 83518781，無增開六獎），以及特別獎、特獎中獎清冊連結。雲端發票專屬獎在 `cloudNowNumber.html`。

**領獎期間陷阱:** 頁面上的「領獎期間」文字只屬於它所在區塊的期別。2026-09-09 實測時，最新號碼單已是 115年05-06月，頁面殘留的「領獎期間自115年06月06日起至115年09月07日止」卻是上一期（115年03-04月）的，直接配對會讓使用者錯過領獎。領獎期間只能引用與期別標籤同一區塊的文字;取不到對應區塊時，依規則說明「開獎日（單月 25 日）次月 6 日起算 3 個月」（例:115年05-06月期，115年7月25日開獎，領獎期間為115年8月6日至11月5日），並請使用者到 https://invoice.etax.nat.gov.tw 確認實際期限。

### 2. 解析

**務必先把 HTML 標籤「整個刪掉」（取代成空字串）再取數字。** 號碼會被標籤切開（例如頭獎 07225810 在原始碼中被拆成 `072</span><span ...>25810` 兩段）。如果把標籤取代成空白，數字會斷成 3 碼碎片（`072`、`258`、`10`），對獎會全錯;直接對原始 HTML 下正則也會漏。

```bash
python3 - <<'PY'
import re
h = open('/tmp/lastNumber.html', encoding='utf-8').read()
text = re.sub(r'<[^>]+>', '', h)   # 標籤整個刪除,不要取代成空白
text = re.sub(r'\s+', ' ', text)
m = re.search(r'(1\d\d年\d\d-\d\d月)中獎號碼單', text)
print('期別:', m.group(1) if m else '找不到')
if m:
    seg = text[m.end():m.end()+1200]
    for prize in ['特別獎', '特獎']:
        i = seg.find(prize)
        n = re.search(r'\d{8}', seg[i:i+100]) if i >= 0 else None
        print(prize, n.group(0) if n else '找不到')
    i = seg.find('頭獎')
    if i >= 0:
        j = seg.find('同期', i)          # 頭獎可能多組,取到說明文字前為止
        print('頭獎', re.findall(r'\d{8}', seg[i:j if j > i else i+200]))
    i = seg.find('增開六獎')
    if i >= 0:                            # 不是每期都有
        print('增開六獎', re.findall(r'(?<!\d)\d{3}(?!\d)', seg[i:i+100]))
PY
```

2026-09-09 實測（115年05-06月期）:特別獎 `19531471`、特獎 `85941329`、頭獎 `07225810` `20231230` `83518781` 三組皆完整取出，無增開六獎。

獎項結構（2026-09-09 實測頁面記載）:

| 獎項 | 條件 | 獎金 |
| --- | --- | --- |
| 特別獎 | 8 碼全同 | 1,000 萬元 |
| 特獎 | 8 碼全同 | 200 萬元 |
| 頭獎 | 8 碼全同（可能有多組） | 20 萬元 |
| 二獎 | 末 7 碼與任一頭獎末 7 碼相同 | 4 萬元 |
| 三獎 | 末 6 碼相同 | 1 萬元 |
| 四獎 | 末 5 碼相同 | 4 千元 |
| 五獎 | 末 4 碼相同 | 1 千元 |
| 六獎 | 末 3 碼相同 | 2 百元 |

### 3. 對獎

拿到使用者的 8 位發票號碼後:

1. 先比對特別獎、特獎的完整 8 碼。
2. 再比對每一組頭獎:8 碼全同 → 頭獎;否則取使用者號碼末 7 碼與頭獎末 7 碼比，中則二獎;依此類推到末 3 碼（六獎）。
3. 若有「增開六獎」的 3 碼，另比末 3 碼。
4. 一張發票同時對中多個獎項時，以兌領一個獎項為限（頁面領獎說明記載），回報時以最高獎金者為主。

回報時附上:期別、中獎號碼、領獎期間（只引用與該期別同區塊的文字，否則依上述規則推算並加註需向官方確認）、出處 URL。民國年 = 西元年 - 1911（例:115年 = 2026年）。

## 錯誤與失敗時的處理

- **連線逾時**:`curl` 一律加 `-m 30`。逾時或 5xx 時隔幾秒重試 1~2 次;仍失敗就告知「財政部電子發票整合服務平台可能暫時異常，請直接到 https://invoice.etax.nat.gov.tw 確認」，不要自己編號碼。
- **頁面結構改變**:解析不到「中獎號碼單」或獎項標籤時，停止解析，告知頁面結構可能改版，請使用者到官方網站直接確認。不要用舊快取冒充最新資料。
- **期別混淆**:頁面同時出現多個期別（號碼單與清冊連結）。永遠以「○○○年○○-○○月中獎號碼單」標籤正下方的表格為準，並把期別一起回報。
- **領獎期間錯配**:頁面殘留的領獎期間常是上一期的。不要把與期別標籤不同區塊的領獎期間當成本期的;取不到時依「開獎日次月 6 日起 3 個月」推算並註明請向官方確認，不要把推算值說成官方公告。
- **開獎時間**:統一發票每兩個月一期，單月 25 日開獎。開獎日前頁面顯示的是上一期，這是正常現象。

## English summary

Fetches the latest Taiwan uniform-invoice winning numbers from the Ministry of Finance's public e-invoice page (no API key, no login; `curl` is enough) and matches an 8-digit invoice number against them. Always strip HTML tags before extracting numbers (they are split across tags), report the period label and claim window with the numbers, and never invent numbers when the fetch or parse fails - point the user to the official site instead.
