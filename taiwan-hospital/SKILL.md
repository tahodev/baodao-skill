---
name: taiwan-hospital
description: 健保特約醫療院所查詢——全台三萬七千家醫院診所的名稱、地址、電話、類型（健保署開放資料）。附近放資料）。附近診所、醫院電話、牙醫診所地址、看診掛號電話的問題適用。免 API 金鑰、免登入。即時看診進度、掛號、醫師排班不適用。
license: MIT
metadata:
  category: health
  locale: zh-TW
---

# taiwan-hospital

用健保署開放資料 API 查全台健保特約醫療院所（醫院、診所、藥局、護理機構…）的基本資料。不需要 API 金鑰或登入。

## 基本流程

1. 大量下載資料集（一次 limit 拉高）或帶參數查詢
2. 依院名、縣市（地址開頭）、類型篩選
3. 回報名稱、地址、電話；註明資料為健保特約院所名錄（非即時看診資訊）

### 1. API 端點

```bash
# 院所基本資料(37,127 筆,2026-09-19 實測)
curl -sm 30 -A 'Mozilla/5.0' 'https://info.nhi.gov.tw/api/iode0010/v1/rest/datastore/A21030000I-D2100G-001?limit=40000' -o /tmp/hosp.json

# 資料集目錄
curl -sm 30 -A 'Mozilla/5.0' 'https://info.nhi.gov.tw/api/iode0010/v1/rest/dataset?limit=100' -o /tmp/datasets.json
```

2026-09-19 實測：HTTP 200、`{"success": true, "result": {...}}`。欄位：BRANCH_CODE（分區）、HOSP_ID、HOSP_ATTR_NAME（如 部立及直轄市立醫院）、HOSP_NAME、HOSP_ADDR、TEL_AREA/TEL、HOSP_CNT_TYPE、HOSP_TYPE、CONT_ORIG_DATE（簽約起日）。首筆實測範例：臺北市立聯合醫院、臺北市大同區鄭州路１４５號（代表）、(02)25553000。

有用的姊妹資料集（dataset 目錄可查）：D21006 固定服務時段（各院所門診時段表）、D2100C 診療科別。

### 2. 篩選範例

```python
import json
d = json.load(open('/tmp/hosp.json'))
recs = d['result']['records']
# 找名稱含「台大」的院所
for r in recs:
    if '台大' in r['HOSP_NAME'] or '臺大' in r['HOSP_NAME']:
        print(r['HOSP_NAME'], r['HOSP_ADDR'], f"({r['TEL_AREA']}){r['TEL']}")
```

### 3. 進階：服務時段與科別

D21006（固定服務時段）與 D2100C（診療科別）用同一 API 形式，把 resource id 換掉即可。要回答「這家診所週六有沒有看診」時，先從基本資料拿 HOSP_ID，再查服務時段資料集比對。

## 錯誤與失敗時的處理

- **這是名錄不是即時資訊**：看診進度（目前看到幾號）、網路掛號、臨時休診查不到，如實說明。
- **地址含全形字元與「（代表）」**：多分院體系只有代表地址；回報前不要自行刪改。
- **資料更新頻率**：健保署定期更新，新開業或歇業可能有落差；重要就醫決策建議電話確認。
- **success=false 或 HTTP 非 200**：帶瀏覽器 UA 重試；失敗回報資料源異常，不要背院所電話。
- **37,127 筆全量約 8MB**：頻寬受限時用參數查詢（如 `?HOSP_NAME=台大`），但參數過濾行為可能因資料集而異，比對結果是否合理。

## English summary

Taiwan NHI-contracted medical providers directory, keyless. `GET https://info.nhi.gov.tw/api/iode0010/v1/rest/datastore/A21030000I-D2100G-001?limit=40000` returns {"success":true, result:{records:[...]}} - 37,127 hospitals/clinics/pharmacies with name, address, phone, type, contract dates (verified 2026-09-19). Dataset catalog at `/api/iode0010/v1/rest/dataset?limit=100`; useful siblings: D21006 (service hours), D2100C (departments). Directory data only - no real-time queue status or appointment booking; say so when asked.
