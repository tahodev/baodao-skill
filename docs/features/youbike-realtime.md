# youbike-realtime

查 YouBike 2.0 站點即時可借車輛與可還空位。免 API 金鑰、免登入,`curl` + `jq` 即可。

**主要來源:官方統一 feed(全台 14 個服務區)**
- https://apis.youbike.com.tw/json/station-yb2.json — youbike.com.tw 地圖用的即時 JSON,約 9,500 站(2026-09-10 實測 9,521),涵蓋雙北、桃園、台中、台南、高雄、新竹、嘉義、苗栗、屏東、台東等 14 個服務區,每站含電輔車明細(`available_spaces_detail.eyb`)
- 非公開文件化 API,欄位可能無預警調整 → 下列各市府 feed 保留作為備援

**備援來源:各市政府開放資料**
- 台北市:https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json（約 1,800 站,數字型欄位 `available_rent_bikes`/`available_return_bikes`;無電輔車欄位,篩電輔車請用統一 feed）
- 新北市:https://data.ntpc.gov.tw/api/datasets/010E5B15-3823-4B20-B401-B1CF000550C5/json?page=0&size=5000（約 1,600 站,字串型欄位 `sbi_quantity`/`bemp`,含 `eyb_quantity` 電輔車）
- 台中市:https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=9468c0d0-e1ed-4ecc-a86f-ab5a9fd590ff（約 1,820 站,全量單次）
- 桃園市:https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json&limit=2000（不帶 limit 只回 20 站;全量約 700 站;回傳筆數等於 limit 時要加大再查）
- 台中/桃園共用 `sbi`/`bemp`/`tot` 字串欄位;電輔車在 `sbi_detail`（台中逗號字串 `一般,電輔`,桃園 JSON 字串）
- 高雄市政府 openapi.kcg.gov.tw 端點 2026-09-09 從台灣境外連線逾時、無法驗證,高雄請用統一 feed（`area_code=="12"`）

**共通注意事項**
- 站名「台 / 臺」混用（台北 147 站用「臺」,2026-09-10 實測）,搜尋前兩邊都 `gsub("臺";"台")`
- 更新時間格式各市不同（台北 `YYYY-MM-DD HH:MM:SS`、新北 `YYYYMMDDTHHMMSS`、台中/桃園 `YYYYMMDDHHMMSS`、統一 feed `updated_at` 同台北格式）,全部台灣時間 UTC+8
- 站數為 2026-09-10 實測約略值,會隨設站緩慢增加
- 回報務必附上資料更新時間;數量為 0 或暫停營運（`status`/`act` ≠ 1）要如實說明

完整欄位對照、服務區代碼表、查詢範例與錯誤處理請看 [SKILL.md](../../youbike-realtime/SKILL.md)。
