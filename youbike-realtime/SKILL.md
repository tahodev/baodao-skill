---
name: youbike-realtime
description: 查台北市、新北市、台中市、桃園市 YouBike 2.0 站點的即時可借車輛與可還空位,含電輔車篩選與最近站點查詢。YouBike、微笑單車、公共自行車、借車、還車、站點、哪裡有車的問題適用。免 API 金鑰、免登入,官方公開資料。高雄市來源 2026-09-09 連線失敗未收錄;雙北台中桃園以外縣市、預約租車、費用計算不適用。
license: MIT
metadata:
  category: transport
  locale: zh-TW
---

# youbike-realtime

從官方公開資料查 YouBike 2.0 站點即時狀態:可借幾台、可還幾個空位。涵蓋台北市、新北市、台中市、桃園市。免 API 金鑰,`curl` + `jq` 即可。**四個城市的 feed 欄位命名分兩派**,不要混用 jq 篩選式:

- 台北派:`available_rent_bikes` / `available_return_bikes` / `Quantity`(數字型)
- 其他三市派:`sbi` / `bemp` / `tot`(字串型;新北另叫 `sbi_quantity` / `bemp` / `tot_quantity`)

## 基本流程

1. 依城市下載即時 JSON
2. 用 `jq` 依行政區、站名或經緯度篩選
3. 回報時附上資料更新時間,讓使用者知道資訊有多新

## 台北市

```bash
curl -sm 30 https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json -o /tmp/youbike.json
```

2026-09-09 實測:HTTP 200、約 940KB、1800 個站點,涵蓋台北市各行政區與臺大公館校區。約 1 分鐘更新一次。檔案不小,短時間內重複查詢請用同一份快取(1~2 分鐘),不要連續請求。

### 欄位

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

### 查詢範例

```bash
# 大安區還有車可借的站
jq -r '.[] | select(.sarea=="大安區" and .act=="1" and .available_rent_bikes>0)
  | "\(.sna) 可借\(.available_rent_bikes) 可還\(.available_return_bikes)"' /tmp/youbike.json

# 找離指定座標最近且有車的 5 站(以緯度 25.033、經度 121.565 為例)
jq -r --argjson la 25.033 --argjson lo 121.565 '
  [.[] | select(.act=="1" and .available_rent_bikes>0)
   | . + {d: ((.latitude-$la)*(.latitude-$la) + (.longitude-$lo)*(.longitude-$lo))}]
  | sort_by(.d) | .[0:5][]
  | "\(.sna) 可借\(.available_rent_bikes) 可還\(.available_return_bikes) \(.ar)"' /tmp/youbike.json
```

## 新北市(data.ntpc.gov.tw)

```bash
curl -sm 30 'https://data.ntpc.gov.tw/api/datasets/010E5B15-3823-4B20-B401-B1CF000550C5/json?page=0&size=5000' -o /tmp/youbike_ntpc.json
```

2026-09-09 實測:HTTP 200、`size=5000` 一次取回全部 1600 站(約 700KB)。分頁參數 `page`(0 起)與 `size`。

欄位對照(新北 → 台北):

| 新北欄位 | 台北欄位 | 意義 |
| --- | --- | --- |
| `sbi_quantity` | `available_rent_bikes` | 可借車輛數 |
| `bemp` | `available_return_bikes` | 可還空位數 |
| `tot_quantity` | `Quantity` | 總車位數 |
| `lat` / `lng` | `latitude` / `longitude` | 站點座標 |
| `act` | `act` | `1` = 營運中 |
| `mday` | `mday` | 資料更新時間 |
| `yb2_quantity` / `eyb_quantity` | (無) | 可借中一般車 / 電輔車數 |

```bash
# 板橋區還有電輔車可借的站
jq -r '.[] | select(.sarea=="板橋區" and .act=="1" and (.eyb_quantity|tonumber)>0)
  | "\(.sna) 電輔車\(.eyb_quantity) 一般\(.yb2_quantity) 可還\(.bemp)"' /tmp/youbike_ntpc.json
```

注意:新北 feed 的數量欄位是字串(`"9"` 不是 `9`),比較前用 `tonumber`。

## 台中市(newdatacenter.taichung.gov.tw)

```bash
curl -sm 30 'https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=9468c0d0-e1ed-4ecc-a86f-ab5a9fd590ff' -o /tmp/youbike_tc.json
```

2026-09-09 實測:HTTP 200、約 750KB、1,824 站、一次全量下載不分頁。

## 桃園市(opendata.tycg.gov.tw)

```bash
curl -sm 30 'https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json&limit=2000' -o /tmp/youbike_ty.json
```

2026-09-09 實測:HTTP 200;**不帶 `limit` 只回 20 站**,帶 `limit=2000` 取回全部 702 站。

## 台中 / 桃園的共同欄位

兩市 feed 欄位命名相同(與新北不同):

| 欄位 | 意義 |
| --- | --- |
| `scity` / `scityen` | 城市(中文 / 英文) |
| `sna` / `snaen` | 站名(中文 / 英文) |
| `sarea` / `sareaen` | 行政區 |
| `ar` / `aren` | 地址 |
| `sno` | 站點編號 |
| `tot` | 總車位數(字串) |
| `sbi` | 可借車輛數(字串) |
| `bemp` | 可還空位數(字串) |
| `lat` / `lng` | 站點座標(字串) |
| `act` | `1` = 營運中 |
| `mday` | 資料更新時間 `YYYYMMDDHHMMSS` |
| `sbi_detail` | 可借明細:**台中是 `"14,1"`(一般,電輔),桃園是 JSON 字串 `{"yb2":"14","eyb":"1"}`**,兩市格式不同 |

```bash
# 台中西區有可借車的站
jq -r '.[] | select(.sarea=="西區" and .act=="1" and (.sbi|tonumber)>0)
  | "\(.sna) 可借\(.sbi) 可還\(.bemp)"' /tmp/youbike_tc.json

# 桃園找有電輔車的站(sbi_detail 是 JSON 字串,要 fromjson)
jq -r '.[] | select(.act=="1" and ((.sbi_detail|fromjson|.eyb|tonumber) // 0) > 0)
  | "\(.sna) 電輔車\(.sbi_detail|fromjson|.eyb) 可還\(.bemp)"' /tmp/youbike_ty.json

# 台中找離指定座標最近且有空位可還的 5 站(以緯度 24.147、經度 120.683 為例)
jq -r --argjson la 24.147 --argjson lo 120.683 '
  [.[] | select(.act=="1" and (.bemp|tonumber)>0)
   | . + {d: ((.lat|tonumber)-$la)*((.lat|tonumber)-$la) + ((.lng|tonumber)-$lo)*((.lng|tonumber)-$lo)}]
  | sort_by(.d) | .[0:5][] | "\(.sna) 可還\(.bemp) 可借\(.sbi) \(.ar)"' /tmp/youbike_tc.json
```

## 錯誤與失敗時的處理

- **連線逾時 / 5xx**:`curl` 一律加 `-m 30`,隔幾秒重試 1~2 次;仍失敗就告知公開資料源可能暫時異常,建議改用 YouBike 官方 App 或 https://www.youbike.com.tw 確認。
- **回傳空陣列或不是 JSON**:視為失敗,不要用舊資料冒充即時資料。
- **`act` 不是 `1`**:該站暫停營運,明確告知,不要只回報 0 台可借。
- **數量為 0**:如實回報「目前無車可借 / 無位可還」,數量變動很快,建議出發前再查一次。
- **桃園只查到 20 站**:忘了帶 `limit` 參數。預設只回 20 筆,全量 702 站要 `limit=2000`(2026-09-09 實測)。
- **`sbi_detail` 格式**:台中是逗號字串 `一般,電輔`,桃園是 JSON 字串。桃園要 `fromjson` 再取值;台中用 `split(",")`。
- **高雄市**:已知來源(data.kcg.gov.tw 的 YouBike 即時資料)2026-09-09 從一般網路連線逾時,無法驗證,本技能暫不收錄。使用者問高雄時請回報尚未支援,不要編造站點資料。
- **欄位混用**:四市欄位名分兩派(見開頭說明),把台北的 `available_rent_bikes` 套到台中資料會得到空結果,先確認城市再選篩選式。

## English summary

Looks up real-time YouBike 2.0 station availability for Taipei, New Taipei, Taichung, and Taoyuan (no API key; `curl` + `jq`). Field names split into two families: Taipei uses numeric `available_rent_bikes`/`available_return_bikes`, while the other three cities use string-typed `sbi`/`bemp`/`tot` (New Taipei calls them `sbi_quantity`/`bemp`/`tot_quantity`). Taoyuan paginates at 20 rows unless you pass `limit=2000` (702 stations, verified 2026-09-09); Taichung returns all 1,824 stations in one call. E-bike counts come from NTPC's `eyb_quantity` or the `sbi_detail` field (comma string in Taichung, JSON string in Taoyuan - `fromjson` it). Kaohsiung is excluded: its known source (data.kcg.gov.tw) was unreachable on 2026-09-09 and could not be verified. Always quote the feed's update time, cache responses for 1-2 minutes instead of polling, and treat non-JSON or empty responses as failures - never pass stale data off as live.
