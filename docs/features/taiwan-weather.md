# taiwan-weather

用 Open-Meteo（免 API 金鑰）查台灣各縣市現在天氣與未來預報，是 cwa-weather 的免金鑰備援。

- 全台 22 縣市座標表內建；其他地點用 Open-Meteo 地理編碼 API（只認英文/拼音地名，確認 country_code=TW）
- 現在天氣與未來數日預報：`https://api.open-meteo.com/v1/forecast?latitude=...&longitude=...&current=...&daily=...`
- 災害警報（颱風、地震、海嘯、淹水、土石流、降雨、河川高水位）：NCDR CAP 公開 feed，免金鑰 — https://alerts.ncdr.nat.gov.tw/RssAtomFeed.ashx?AlertType=5 （代碼 5~11,3 秒速率限制，注意每則警報的 updated/expires）
- 正式預報與警報以中央氣象署公告為準

完整步驟、座標表、天氣代碼對照與錯誤處理請看 [SKILL.md]（../../taiwan-weather/SKILL.md）。
