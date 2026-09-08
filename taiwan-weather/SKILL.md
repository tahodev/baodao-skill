---
name: taiwan-weather
description: 用 Open-Meteo（免 API 金鑰）查台灣 22 縣市現在天氣與未來數日預報。天氣、氣溫、下雨、降雨機率、明天天氣、週末天氣的問題適用，是沒有金鑰時的快速備援。颱風警報、豪雨特報不支援（請看中央氣象署）;有 CWA 授權碼時正式預報請用 cwa-weather。
license: MIT
metadata:
  category: weather
  locale: zh-TW
---

# taiwan-weather

用 Open-Meteo 的免費 API 查台灣各地天氣。免 API 金鑰、免登入，`curl` 即可。

**定位:免金鑰的立即備援。** 有 CWA 授權碼時，正式預報請優先用 `cwa-weather` 技能（官方資料）;本技能適合手邊沒有金鑰、只要快速概況時使用。

**資料來源是 Open-Meteo 的國際氣象模式，不是中央氣象署（CWA）。** 颱風動態、豪雨特報、各種警報與正式預報，請一律以中央氣象署 https://www.cwa.gov.tw 為準。

## 基本流程

1. 決定地點的經緯度
2. 呼叫 forecast API
3. 解讀天氣代碼與數值

### 1. 全台 22 縣市座標

2026-09-09 以 Open-Meteo 地理編碼 API 逐一確認（注意:該 API **只認英文/拼音地名**，中文地名查不到;下表座標是用英文名稱查得）:

| 縣市 | 緯度 | 經度 |
| --- | --- | --- |
| 台北市 | 25.053 | 121.526 |
| 新北市（板橋） | 25.014 | 121.467 |
| 桃園市 | 24.994 | 121.297 |
| 新竹市 | 24.804 | 120.969 |
| 新竹縣（竹北） | 24.838 | 121.008 |
| 苗栗縣（苗栗市） | 24.564 | 120.824 |
| 台中市 | 24.147 | 120.684 |
| 彰化縣（彰化市） | 24.073 | 120.563 |
| 南投縣（南投市） | 23.916 | 120.664 |
| 雲林縣（斗六） | 23.709 | 120.543 |
| 嘉義市 | 23.479 | 120.449 |
| 嘉義縣（太保） | 23.459 | 120.332 |
| 台南市 | 22.991 | 120.213 |
| 高雄市 | 22.616 | 120.313 |
| 屏東縣（屏東市） | 22.671 | 120.488 |
| 宜蘭縣（宜蘭市） | 24.757 | 121.753 |
| 花蓮縣（花蓮市） | 23.977 | 121.604 |
| 台東縣（台東市） | 22.760 | 121.145 |
| 澎湖縣（馬公） | 23.565 | 119.586 |
| 金門縣 | 24.446 | 118.376 |
| 連江縣（南竿） | 26.150 | 119.933 |
| 基隆市 | 25.131 | 121.741 |
| 墾丁（以恆春計） | 22.004 | 120.744 |
| 埔里 | 23.966 | 120.970 |

表裡沒有的地點，用免金鑰的地理編碼 API 查，**`name` 請用英文或拼音**（例:`Hengchun`、`Lugang`）:

```bash
curl -sm 30 'https://geocoding-api.open-meteo.com/v1/search?name=<英文地名>&count=5&country_code=TW'
```

2026-09-09 實測:中文地名（「台北市」「嘉義」「墾丁」等）在此 API 一律查無結果;英文地名也要注意同名地點（`Nantou` 會先命中中國廣東，`Kenting` 不在庫），務必確認回傳的 `country_code` 是 `TW`、`admin1` 合理再使用。查不到或對不上時，不要猜座標，改用 cwa-weather（需金鑰）或請使用者確認中央氣象署預報。

### 2. 查詢

```bash
# 現在天氣(以台北市為例)
curl -sm 30 'https://api.open-meteo.com/v1/forecast?latitude=25.053&longitude=121.526&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=Asia%2FTaipei'

# 未來 3 天預報
curl -sm 30 'https://api.open-meteo.com/v1/forecast?latitude=25.053&longitude=121.526&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&forecast_days=3&timezone=Asia%2FTaipei'
```

2026-09-09 實測:HTTP 200,`current` 回傳溫度、濕度、降水量、天氣代碼，時間為 Asia/Taipei 當地時間。回報時附上回傳的 `time` 欄位。

### 3. 天氣代碼（WMO）對照

| 代碼 | 意義 |
| --- | --- |
| 0 | 晴 |
| 1 / 2 / 3 | 大致晴 / 局部多雲 / 多雲 |
| 45 / 48 | 霧 / 凍霧 |
| 51 / 53 / 55 | 毛毛雨（小/中/大） |
| 61 / 63 / 65 | 雨（小/中/大） |
| 66 / 67 | 凍雨 |
| 71 / 73 / 75 / 77 | 雪 |
| 80 / 81 / 82 | 陣雨 |
| 85 / 86 | 陣雪 |
| 95 | 雷雨 |
| 96 / 99 | 雷雨伴冰雹 |

## 錯誤與失敗時的處理

- **連線逾時 / 5xx**:`curl` 一律加 `-m 30`，重試 1~2 次;仍失敗就告知 Open-Meteo 暫時異常，正式預報請看中央氣象署。不要編造天氣。
- **回傳不是 JSON 或缺 `current`/`daily`**:視為失敗，不要用舊資料冒充。
- **座標不在台灣**:確認 `country_code=TW` 的地理編碼結果，回傳的 `name` 與使用者問的地點不符時，先回報找到的地名再給天氣。中文地名在地理編碼 API 查不到是已知限制，改用英文/拼音，仍查不到就照上一節指示降級，不要自行估座標。
- **颱風、警報相關問題**:本技能不提供。直接請使用者看中央氣象署或下載中央氣象署 App。

## English summary

Queries current weather and multi-day forecasts for Taiwanese cities through the keyless Open-Meteo API (`curl` only). Ships a geocoded coordinate table for major cities and a WMO weather-code table in Traditional Chinese. The data comes from international models, not the CWA - for typhoons, heavy-rain advisories, and any official warning, always direct the user to the Central Weather Administration (https://www.cwa.gov.tw). Quote the response's `time` field and never fabricate readings on failure.
