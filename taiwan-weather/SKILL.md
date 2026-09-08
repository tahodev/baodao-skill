---
name: taiwan-weather
description: 用 Open-Meteo(免 API 金鑰)查台灣各縣市現在天氣與未來數日預報。颱風與警報請以中央氣象署為準。
license: MIT
metadata:
  category: weather
  locale: zh-TW
---

# taiwan-weather

用 Open-Meteo 的免費 API 查台灣各地天氣。免 API 金鑰、免登入,`curl` 即可。

**定位:免金鑰的立即備援。** 有 CWA 授權碼時,正式預報請優先用 `cwa-weather` 技能(官方資料);本技能適合手邊沒有金鑰、只要快速概況時使用。

**資料來源是 Open-Meteo 的國際氣象模式,不是中央氣象署(CWA)。** 颱風動態、豪雨特報、各種警報與正式預報,請一律以中央氣象署 https://www.cwa.gov.tw 為準。

## 基本流程

1. 決定地點的經緯度
2. 呼叫 forecast API
3. 解讀天氣代碼與數值

### 1. 主要城市座標

2026-09-09 以 Open-Meteo 地理編碼 API 確認:

| 城市 | 緯度 | 經度 |
| --- | --- | --- |
| 台北市 | 25.053 | 121.526 |
| 新北市(板橋) | 25.014 | 121.467 |
| 桃園市 | 24.994 | 121.297 |
| 新竹市 | 24.804 | 120.969 |
| 台中市 | 24.147 | 120.684 |
| 台南市 | 22.991 | 120.213 |
| 高雄市 | 22.616 | 120.313 |
| 基隆市 | 25.131 | 121.741 |
| 宜蘭市 | 24.757 | 121.753 |
| 花蓮市 | 23.977 | 121.604 |
| 台東市 | 22.760 | 121.145 |

表裡沒有的地點,用免金鑰的地理編碼 API 查:

```bash
curl -sm 30 'https://geocoding-api.open-meteo.com/v1/search?name=<地名>&count=1&country_code=TW'
```

### 2. 查詢

```bash
# 現在天氣(以台北市為例)
curl -sm 30 'https://api.open-meteo.com/v1/forecast?latitude=25.053&longitude=121.526&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=Asia%2FTaipei'

# 未來 3 天預報
curl -sm 30 'https://api.open-meteo.com/v1/forecast?latitude=25.053&longitude=121.526&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&forecast_days=3&timezone=Asia%2FTaipei'
```

2026-09-09 實測:HTTP 200,`current` 回傳溫度、濕度、降水量、天氣代碼,時間為 Asia/Taipei 當地時間。回報時附上回傳的 `time` 欄位。

### 3. 天氣代碼(WMO)對照

| 代碼 | 意義 |
| --- | --- |
| 0 | 晴 |
| 1 / 2 / 3 | 大致晴 / 局部多雲 / 多雲 |
| 45 / 48 | 霧 / 凍霧 |
| 51 / 53 / 55 | 毛毛雨(小/中/大) |
| 61 / 63 / 65 | 雨(小/中/大) |
| 66 / 67 | 凍雨 |
| 71 / 73 / 75 / 77 | 雪 |
| 80 / 81 / 82 | 陣雨 |
| 85 / 86 | 陣雪 |
| 95 | 雷雨 |
| 96 / 99 | 雷雨伴冰雹 |

## 錯誤與失敗時的處理

- **連線逾時 / 5xx**:`curl` 一律加 `-m 30`,重試 1~2 次;仍失敗就告知 Open-Meteo 暫時異常,正式預報請看中央氣象署。不要編造天氣。
- **回傳不是 JSON 或缺 `current`/`daily`**:視為失敗,不要用舊資料冒充。
- **座標不在台灣**:確認 `country_code=TW` 的地理編碼結果,回傳的 `name` 與使用者問的地點不符時,先回報找到的地名再給天氣。
- **颱風、警報相關問題**:本技能不提供。直接請使用者看中央氣象署或下載中央氣象署 App。

## English summary

Queries current weather and multi-day forecasts for Taiwanese cities through the keyless Open-Meteo API (`curl` only). Ships a geocoded coordinate table for major cities and a WMO weather-code table in Traditional Chinese. The data comes from international models, not the CWA - for typhoons, heavy-rain advisories, and any official warning, always direct the user to the Central Weather Administration (https://www.cwa.gov.tw). Quote the response's `time` field and never fabricate readings on failure.
