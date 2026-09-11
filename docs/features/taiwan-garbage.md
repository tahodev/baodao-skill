# taiwan-garbage

查台北市與新北市的垃圾車清運點與停靠時間。免登入、免 API 金鑰。計畫停靠時間，不是即時 GPS。

- 台北市：data.taipei CSV（約 550KB,UTF-8 有 BOM，時間為 HHMM 字串；resource id 可能更換，404 時回資料集頁重取）
- 新北市：https://data.ntpc.gov.tw/api/datasets/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8/json?page=0&size=10000（分頁上限 10,000 列，全量約 26,655 列要抓 page=0,1,2；含 `garbage<weekday>`/`recycling<weekday>` 星期排程，可判斷今天有沒有收）
- 兩市資料都有經緯度，可算最近清運點
- 其他縣市尚未支援；停收日與颱風天異動以各市環保局公告為準

### 其他縣市研究結果（2026-09-12 實測，暫不支援的原因）

- 桃園：data.tycg.gov.tw 檔案下載從海外機房連線逾時（HTTP 000）；opendata.tycg.gov.tw API 可連，但垃圾清運點的資料集 rid 尚未確認
- 台中：data.gov.tw 資料集 84004 的即時主機 newdatacenter.taichung.gov.tw 需授權（401 NO_AUTH）；僅有 2020 年舊鏡像，不作為資料源
- 台南：data.tainan.gov.tw 從海外機房不可達，無法驗證資料品質
- 高雄：api.kcg.gov.tw 從海外不可達（先前 YouBike 技能已記錄同問題）

待這些資料源能從海外穩定存取並完成實測後再擴充，避免收錄無法驗證的指令。

完整步驟、查詢範例與錯誤處理請看 [SKILL.md]（../../taiwan-garbage/SKILL.md）。
