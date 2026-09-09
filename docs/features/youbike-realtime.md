# youbike-realtime

查 YouBike 2.0 站點即時可借車輛與可還空位。免 API 金鑰、免登入,`curl` + `jq` 即可。

- 台北市:https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json（約 1,800 站,數字型欄位 `available_rent_bikes`/`available_return_bikes`）
- 新北市:https://data.ntpc.gov.tw/api/datasets/010E5B15-3823-4B20-B401-B1CF000550C5/json?page=0&size=5000（約 1,600 站,字串型欄位 `sbi_quantity`/`bemp`,含 `eyb_quantity` 電輔車）
- 台中市:https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=9468c0d0-e1ed-4ecc-a86f-ab5a9fd590ff（1,824 站,全量單次）
- 桃園市:https://opendata.tycg.gov.tw/api/v1/dataset.api_access?rid=08274d61-edbe-419d-8fcc-7a643831283d&format=json&limit=2000（不帶 limit 只回 20 站;全量 702 站）
- 台中/桃園共用 `sbi`/`bemp`/`tot` 字串欄位;電輔車在 `sbi_detail`（台中逗號字串 `一般,電輔`,桃園 JSON 字串）
- 高雄市來源 2026-09-09 連線失敗,未收錄
- 回報務必附上資料更新時間;數量為 0 或 `act!=1`（暫停營運）要如實說明

完整欄位對照、查詢範例與錯誤處理請看 [SKILL.md](../../youbike-realtime/SKILL.md)。
