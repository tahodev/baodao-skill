---
name: youbike-realtime
description: 查台北市與新北市 YouBike 2.0 站點的即時可借車輛與可還空位。YouBike、微笑單車、公共自行車、借車、還車、站點、哪裡有車的問題適用。免 API 金鑰、免登入，官方公開 JSON。雙北以外的縣市、預約租車、費用計算不適用。
license: MIT
metadata:
  category: transport
  locale: zh-TW
---

# youbike-realtime

從官方公開 JSON 查台北市與新北市 YouBike 2.0 站點的即時狀態:可借幾台、可還幾個空位。免 API 金鑰，`curl` + `jq` 即可。兩市 feed 欄位不同，見下方各自章節。

## 基本流程

1. 下載即時 JSON
2. 用 `jq` 依行政區、站名或經緯度篩選

### 1. 下載

```bash
curl -sm 30 https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json -o /tmp/youbike.json
```

2026-09-09 實測:HTTP 200、約 940KB、1800 個站點，涵蓋台北市各行政區與臺大公館校區。約 1 分鐘更新一次。檔案不小，短時間內重複查詢請用同一份快取（1~2 分鐘），不要連續請求。

### 2. 欄位

| 欄位 | 意義 |
| --- | --- |
| `sno` | 站點編號 |
| `sna` / `snaen` | 站名（中文 / 英文） |
| `sarea` / `sareaen` | 行政區（中文 / 英文） |
| `ar` / `aren` | 地址（中文 / 英文） |
| `Quantity` | 總車位數 |
| `available_rent_bikes` | 可借車輛數 |
| `available_return_bikes` | 可還空位數 |
| `act` | `1` = 營運中，其他 = 暫停營運 |
| `latitude` / `longitude` | 站點座標 |
| `srcUpdateTime` / `mday` | 資料更新時間 |

### 3. 查詢範例

```bash
# 大安區還有車可借的站
jq -r '.[] | select(.sarea=="大安區" and .act=="1" and .available_rent_bikes>0)
  | "\(.sna) 可借\(.available_rent_bikes) 可還\(.available_return_bikes)"' /tmp/youbike.json

# 依站名關鍵字找
jq -r '.[] | select(.sna | contains("捷運科技大樓站"))
  | "\(.sna) 可借\(.available_rent_bikes) 可還\(.available_return_bikes)"' /tmp/youbike.json

# 找離指定座標最近且有車的 5 站(以緯度 25.033、經度 121.565 為例)
jq -r --argjson la 25.033 --argjson lo 121.565 '
  [.[] | select(.act=="1" and .available_rent_bikes>0)
   | . + {d: ((.latitude-$la)*(.latitude-$la) + (.longitude-$lo)*(.longitude-$lo))}]
  | sort_by(.d) | .[0:5][]
  | "\(.sna) 可借\(.available_rent_bikes) 可還\(.available_return_bikes) \(.ar)"' /tmp/youbike.json
```

回報時附上資料更新時間（`srcUpdateTime`），讓使用者知道資訊有多新。

## 新北市（data.ntpc.gov.tw）

新北市 YouBike 2.0 用新北市資料平臺的公開 JSON，**欄位名稱與台北市不同**，不能直接共用 jq 篩選式:

```bash
curl -sm 30 'https://data.ntpc.gov.tw/api/datasets/010E5B15-3823-4B20-B401-B1CF000550C5/json?page=0&size=5000' -o /tmp/youbike_ntpc.json
```

2026-09-09 實測:HTTP 200、`size=5000` 一次取回全部 1600 站（約 700KB）。分頁參數 `page`（0 起）與 `size`。

欄位對照（新北 → 台北）:

| 新北欄位 | 台北欄位 | 意義 |
| --- | --- | --- |
| `sbi_quantity` | `available_rent_bikes` | 可借車輛數 |
| `bemp` | `available_return_bikes` | 可還空位數 |
| `tot_quantity` | `Quantity` | 總車位數 |
| `lat` / `lng` | `latitude` / `longitude` | 站點座標 |
| `act` | `act` | `1` = 營運中 |
| `mday` | `mday` | 資料更新時間 |
| `yb2_quantity` / `eyb_quantity` | （無） | 可借中一般車 / 電輔車數 |

新北查詢範例:

```bash
# 板橋區還有車可借的站
jq -r '.[] | select(.sarea=="板橋區" and .act=="1" and .sbi_quantity!="0")
  | "\(.sna) 可借\(.sbi_quantity) 可還\(.bemp)"' /tmp/youbike_ntpc.json
```

注意:新北 feed 的數量欄位是字串（`"9"` 不是 `9`），比較前用 `tonumber` 或字串比對。雙北都查時分別下載、分別解析，回報時註明各市的資料時間。

## 錯誤與失敗時的處理

- **連線逾時 / 5xx**:`curl` 一律加 `-m 30`，隔幾秒重試 1~2 次;仍失敗就告知公開資料源可能暫時異常，建議改用 YouBike 官方 App 或 https://www.youbike.com.tw 確認。
- **回傳空陣列或不是 JSON**:視為失敗，不要用舊資料冒充即時資料。
- **`act` 不是 `1`**:該站暫停營運，明確告知，不要只回報 0 台可借。
- **數量為 0**:如實回報「目前無車可借 / 無位可還」，數量變動很快，建議出發前再查一次。

## English summary

Looks up real-time YouBike 2.0 station availability in Taipei City and New Taipei City from the official public JSON feeds (no API key; `curl` + `jq`). Taipei covers ~1,800 stations, updated about once a minute; New Taipei (~1,600 stations) uses a different field naming (sbi_quantity/bemp/tot_quantity, string-typed numbers) - see the mapping table. Key fields: `available_rent_bikes`, `available_return_bikes`, `act` (operating status), `latitude`/`longitude`. Always quote the feed's update time, cache responses for 1-2 minutes instead of polling, and treat non-JSON or empty responses as failures - never pass stale data off as live.
