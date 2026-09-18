# taiwan-uv

中央氣象署各測站每日紫外線指數最大值。**需免費授權碼**（opendata.cwa.gov.tw 註冊）。

- API：https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0005-001?Authorization=$KEY（2026-09-19 實測：有鑰 200、無鑰 401）
- 結構：records.weatherElement.location[]，每筆 StationID + UVIndex（當日最大值）
- 實測範例：20+ 測站回傳，466950 UVIndex 11.0（危險級）
- 等級：0-2 低 / 3-5 中 / 6-7 高 / 8-10 過量 / 11+ 危險
- 授權碼保密，不進 repo 不進回覆；success 是字串；站名需另查對照表
- 每日最大值非逐時即時值

完整步驟請看 [SKILL.md](../../taiwan-uv/SKILL.md)。
