# taiwan-weather

用 Open-Meteo（免金鑰）查台灣各縣市現在天氣與未來數日預報。

- 資料來源:https://api.open-meteo.com/v1/forecast （國際氣象模式，非中央氣象署）
- 內建主要城市經緯度表，直接 `curl` 帶座標查詢
- 颱風、豪雨特報、警報請一律以中央氣象署 https://www.cwa.gov.tw 為準

城市座標表、天氣代碼對照與錯誤處理請看 [SKILL.md](../../taiwan-weather/SKILL.md)。
