# cwa-weather

用中央氣象署（CWA）開放資料 API 查各縣市 36 小時預報與鄉鎮預報。

- 資料來源:https://opendata.cwa.gov.tw （官方資料;需免費申請 API 金鑰，即時發給）
- 縣市 36 小時預報用 `F-C0032-001`，鄉鎮預報用各縣市的 `F-D0047-xxx`
- 無金鑰會回 401;免金鑰備援是 taiwan-weather（Open-Meteo）
- 颱風、豪雨特報、警報、地震速報:免金鑰可用 taiwan-weather 的 NCDR CAP 段（2026-09-09 實測;CWA 官網有 Bot 防護）;正式公告以中央氣象署 https://www.cwa.gov.tw 為準

金鑰申請方式、參數、回傳結構與錯誤處理請看 [SKILL.md](../../cwa-weather/SKILL.md)。
