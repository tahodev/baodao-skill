# taiwan-garbage

查台北市與新北市的垃圾車清運點與停靠時間。免登入、免 API 金鑰。計畫停靠時間，不是即時 GPS。

- 台北市：data.taipei CSV（約 550KB,UTF-8 有 BOM，時間為 HHMM 字串；resource id 可能更換，404 時回資料集頁重取）
- 新北市：https://data.ntpc.gov.tw/api/datasets/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8/json?page=0&size=10000（分頁上限 10,000 列，全量約 26,655 列要抓 page=0,1,2；含 `garbage<weekday>`/`recycling<weekday>` 星期排程，可判斷今天有沒有收）
- 兩市資料都有經緯度，可算最近清運點
- 其他縣市尚未支援；停收日與颱風天異動以各市環保局公告為準

完整步驟、查詢範例與錯誤處理請看 [SKILL.md]（../../taiwan-garbage/SKILL.md）。
