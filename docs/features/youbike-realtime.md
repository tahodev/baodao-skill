# youbike-realtime

查台北市與新北市 YouBike 2.0 站點的即時可借車輛與可還空位。免 API 金鑰,官方公開 JSON。

- 台北市資料來源:https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json (約 1800 站,2026-09 實測,約 1 分鐘更新一次)
- 新北市資料來源:https://data.ntpc.gov.tw/api/datasets/010E5B15-3823-4B20-B401-B1CF000550C5/json (約 1600 站,2026-09 實測)
- **兩市欄位名稱不同**:新北用 `sbi_quantity`(可借)、`bemp`(可還)、`tot_quantity`、`lat`/`lng`,且數量是字串;對照表見 SKILL.md
- 台北主要欄位:`sna`(站名)、`sarea`(行政區)、`available_rent_bikes`、`available_return_bikes`、`Quantity`、`act`、`latitude`/`longitude`
- 用 `jq` 依行政區或站名篩選,或用經緯度找最近站點

完整欄位表、查詢範例與錯誤處理請看 [SKILL.md](../../youbike-realtime/SKILL.md)。
