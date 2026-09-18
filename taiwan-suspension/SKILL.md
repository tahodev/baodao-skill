---
name: taiwan-suspension
description: 天然災害停止上班上課查詢——颱風豪雨時各縣市是否停班停課（人事行政總處公告）。停班停課、今天有上班嗎、颱風假、明天要上課嗎的問題適用。免 API 金鑰、免登入。一般公司行號是否放假、學校個別公告不適用。
license: MIT
metadata:
  category: civic
  locale: zh-TW
---

# taiwan-suspension

查行政院人事行政總處的「天然災害停止上班及上課情形」官方公告頁。不需要 API 金鑰或登入。這是颱風天「到底放不放假」的唯一官方來源。

## 基本流程

1. 抓公告頁
2. 判斷目前狀態：出現「無停班停課訊息」代表全國正常上班上課；有公告時抽出各縣市文字
3. **逐字引用公告內容並註明查詢時間**——散布不實停班停課訊息是刑事責任（災害防救法第 53 條），絕對不能猜

### 1. 抓頁面

```bash
curl -sm 30 -A 'Mozilla/5.0' 'https://www.dgpa.gov.tw/typh/daily/nds.html' -o /tmp/nds.html
```

2026-09-19 實測：HTTP 200、約 15KB、UTF-8，頁面標題為「天然災害停止上班及上課情形查詢」。

### 2. 解析狀態

```python
import re
t = open('/tmp/nds.html', encoding='utf-8', errors='replace').read()
if '無停班停課訊息' in t:
    print('全國正常上班上課（頁面無停班停課公告）')
else:
    # 有公告:抽出公告區塊文字,逐字引用
    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    body = re.sub(r'<[^>]+>', '\n', body)
    lines = [ln.strip() for ln in body.splitlines() if '停止上班' in ln or '停止上課' in ln]
    print('\n'.join(lines))
```

2026-09-19 實測實測範例：當日頁面顯示「無停班停課訊息。」（正常上班上課）。

### 3. 回報原則

- 正常時：「人事行政總處目前沒有停班停課公告，全國正常上班上課（查詢時間 HH:MM）。」
- 有公告時：逐字貼出公告（如「高雄市：今天停止上班、停止上課」），附上查詢時間與資料來源。
- **公告時效**：全日停班停課通常前一日 19:00-22:00 發布；半天或當日補發可能清晨 04:30 前更新。用戶深夜問「明天放不放假」時，若尚未公告就如實說「還沒有公告」，不要預測。

## 錯誤與失敗時的處理

- **絕對禁止編造**：放假訊息錯誤涉及刑事責任（頁面明列刑法 211/360 條、災防法 53 條）。解析失敗或內容異常時，直接請用戶看官網，不要猜。
- **僅政府機關與學校基準**：民間公司是否放假依勞基法由雇主決定，此公告是參考基準，回報時說明。
- **編碼**：本頁為 UTF-8；同站其他歷史頁可能是 Big5，解析出亂碼先換編碼。
- **curl 失敗**：帶瀏覽器 UA 重試；持續失敗回報資料源異常，勿用舊記憶回答。
- **頁面只反映最新狀態**：歷史公告不在此頁，查過去颱風假要明說查不到。

## English summary

Taiwan official work/class suspension announcements (typhoon days), keyless. Fetch `https://www.dgpa.gov.tw/typh/daily/nds.html` (DGPA, UTF-8). If the page contains "無停班停課訊息" everything is normal; otherwise quote county announcements VERBATIM with the query time. Never predict or fabricate - spreading false suspension info is a criminal offense in Taiwan, and the page itself cites the statutes. Full-day announcements typically publish 19:00-22:00 the prior evening; late-night "tomorrow?" questions before that window get "no announcement yet". Verified 2026-09-19 (page live, showing no suspensions).
