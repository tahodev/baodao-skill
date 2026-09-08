---
name: youbike-realtime
description: 查台北市 YouBike 2.0 站點的即時可借車輛與可還空位。免 API 金鑰、免登入,官方公開 JSON。
license: MIT
metadata:
  category: transport
  locale: zh-TW
---

# youbike-realtime

從官方公開 JSON 查台北市 YouBike 2.0 站點的即時狀態:可借幾台、可還幾個空位。免 API 金鑰,`curl` + `jq` 即可。

## 基本流程

1. 下載即時 JSON
2. 用 `jq` 依行政區、站名或經緯度篩選

### 1. 下載

```bash
curl -sm 30 https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json -o /tmp/youbike.json
```

2026-09-09 實測:HTTP 200、約 940KB、1800 個站點,涵蓋台北市各行政區與臺大公館校區。約 1 分鐘更新一次。檔案不小,短時間內重複查詢請用同一份快取(1~2 分鐘),不要連續請求。

### 2. 欄位

| 欄位 | 意義 |
| --- | --- |
| `sno` | 站點編號 |
| `sna` / `snaen` | 站名(中文 / 英文) |
| `sarea` / `sareaen` | 行政區(中文 / 英文) |
| `ar` / `aren` | 地址(中文 / 英文) |
| `Quantity` | 總車位數 |
| `available_rent_bikes` | 可借車輛數 |
| `available_return_bikes` | 可還空位數 |
| `act` | `1` = 營運中,其他 = 暫停營運 |
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

回報時附上資料更新時間(`srcUpdateTime`),讓使用者知道資訊有多新。

## 錯誤與失敗時的處理

- **連線逾時 / 5xx**:`curl` 一律加 `-m 30`,隔幾秒重試 1~2 次;仍失敗就告知公開資料源可能暫時異常,建議改用 YouBike 官方 App 或 https://www.youbike.com.tw 確認。
- **回傳空陣列或不是 JSON**:視為失敗,不要用舊資料冒充即時資料。
- **`act` 不是 `1`**:該站暫停營運,明確告知,不要只回報 0 台可借。
- **數量為 0**:如實回報「目前無車可借 / 無位可還」,數量變動很快,建議出發前再查一次。

## English summary

Looks up real-time YouBike 2.0 station availability in Taipei City from the official public JSON feed (no API key; `curl` + `jq`). Covers ~1,800 stations, updated about once a minute. Key fields: `available_rent_bikes`, `available_return_bikes`, `act` (operating status), `latitude`/`longitude`. Always quote the feed's update time, cache responses for 1-2 minutes instead of polling, and treat non-JSON or empty responses as failures - never pass stale data off as live.
