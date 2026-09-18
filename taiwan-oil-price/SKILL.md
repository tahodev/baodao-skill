---
name: taiwan-oil-price
description: 台灣中油歷史油價查詢——92/95/98 無鉛汽油與超級柴油的每週牌價。油價、汽油多少錢、柴油價格、加油、下週油價的問題適用。免 API 金鑰、免登入。即時國際油價、預測漲跌、加油站個別售價不適用。
license: MIT
metadata:
  category: finance
  locale: zh-TW
---

# taiwan-oil-price

抓台灣中油（CPC）官網的歷史油價頁，取得 92/95/98 無鉛汽油與超級/高級柴油的每週調價牌價。不需要 API 金鑰或登入。

## 基本流程

1. 抓歷史油價頁
2. 解析表格第一個資料列（最新一週）取得當期牌價
3. 回報時註明調價日期（民國年格式），因為油價是**每週一零時生效**的週牌價

### 1. 抓頁面

```bash
curl -sm 30 -A 'Mozilla/5.0' 'https://www.cpc.com.tw/historyprice.aspx?n=2890' -o /tmp/cpc.html
```

2026-09-19 實測：HTTP 200、約 134KB，內含近 7 週調價表（欄：調價日期、92 無鉛、95 無鉛、98 無鉛、超級/高級柴油）。需帶瀏覽器 UA；日期為民國年（115/09/14 = 2026-09-14）。

### 2. 解析最新一列

```python
import re, html
t = open('/tmp/cpc.html', encoding='utf-8', errors='replace').read()
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S)
for r in rows:
    cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip()
             for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', r, re.S)]
    cells = [c for c in cells if c]
    if cells and re.match(r'\d+/', cells[0]):   # 第一列資料 = 最新調價
        print(cells)  # ['115/09/14', '31.2', '32.7', '34.7', '29.9']
        break
```

2026-09-19 實測範例：2026-09-14 當週牌價 92 無鉛 31.2、95 無鉛 32.7、98 無鉛 34.7、超柴 29.9 元/公升。

### 3. 回報範式

「本週（09/14 生效）中油牌價：92 無鉛 31.2 元、95 無鉛 32.7 元、98 無鉛 34.7 元、超級柴油 29.9 元。」用戶問「下週會不會漲」時：此資料源是歷史牌價，**不能預測**；如實說明。

## 錯誤與失敗時的處理

- **頁面結構變動**：CPC 改版會讓表格解析失敗。解析不到資料列時不要編造數字，回報資料源結構異常。
- **只列近 7 週**：更早的歷史需分頁 POST 查詢（本 skill 範圍外），如實說明。
- **民國年換算**：115/09/14 = 2026-09-14（民國年 + 1911），回報西元日期時要換算。
- **台塑石化另有牌價**：本資料源是中油；用戶指名台塑時說明差異（通常差 0.1 元）。
- **curl 403/逾時**：確認有帶 `-A 'Mozilla/5.0'`；持續失敗回報資料源異常。

## English summary

Taiwan CPC fuel prices, keyless. Fetch `https://www.cpc.com.tw/historyprice.aspx?n=2890` with a browser UA, parse the first table row for the latest weekly prices of 92/95/98 unleaded and premium diesel. Prices are weekly list prices effective Monday 00:00; dates are in ROC calendar (115/09/14 = 2026-09-14). Verified 2026-09-19 (week of 2026-09-14: 92=31.2, 95=32.7, 98=34.7, diesel=29.9 TWD/liter). History page shows ~7 recent weeks only; cannot predict next week's adjustment - say so if asked.
