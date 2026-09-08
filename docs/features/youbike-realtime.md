# youbike-realtime

查台北市 YouBike 2.0 站點的即時可借車輛與可還空位。免 API 金鑰,官方公開 JSON。

- 資料來源:https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json
- 涵蓋台北市約 1800 個站點(2026-09 實測),約 1 分鐘更新一次
- 主要欄位:`sna`(站名)、`sarea`(行政區)、`available_rent_bikes`、`available_return_bikes`、`Quantity`、`act`、`latitude`/`longitude`
- 用 `jq` 依行政區或站名篩選,或用經緯度找最近站點

完整欄位表、查詢範例與錯誤處理請看 [SKILL.md](../../youbike-realtime/SKILL.md)。
