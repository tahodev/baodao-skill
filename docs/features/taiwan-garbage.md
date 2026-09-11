# taiwan-garbage

查台北市與新北市的垃圾車清運點與停靠時間。免登入、免 API 金鑰。計畫停靠時間，不是即時 GPS。

- 台北市：data.taipei CSV（約 550KB,UTF-8 有 BOM，時間為 HHMM 字串；resource id 可能更換，404 時回資料集頁重取）
- 新北市：https://data.ntpc.gov.tw/api/datasets/EDC3AD26-8AE7-4916-A00B-BC6048D19BF8/json?page=0&size=10000（分頁上限 10,000 列，全量約 26,655 列要抓 page=0,1,2；含 `garbage<weekday>`/`recycling<weekday>` 星期排程，可判斷今天有沒有收）
- 兩市資料都有經緯度，可算最近清運點
- 其他縣市尚未支援；停收日與颱風天異動以各市環保局公告為準

### 其他縣市研究結果（2026-09-12 複驗更新）

- 台中（**有可用來源，列為擴充候選**）：data.gov.tw 資料集 84004 的資源可從免驗證路徑下載——`https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=<資源 rid>`，資源 rid 從資料集頁 https://data.gov.tw/dataset/84004 取得（2026-09-12 實測：CSV 4.7MB、JSON 13.7MB，欄位含 area、village、car_licence、caption、task_type、g_d1_time_s/e 等星期排程）。注意：用資料集 id（84004）直接打 API 會得到 `{"code":401,"s_message":"NO_AUTH"}`，要走資源 rid 的下載路徑。資料時效欄位未找到，擴充前需再確認更新頻率。
- 台南：data.tainan.gov.tw 用 curl 可連（2026-09-12 實測 200）；先前記錄的「不可達」只發生在雲端瀏覽器的代理（該網域被 proxy 黑名單）。尚未找到垃圾清運點的機讀資料集，暫不支援。
- 桃園：data.tycg.gov.tw 檔案下載從海外機房連線逾時（HTTP 000，2026-09-12 複測同）；data.gov.tw 搜尋頁是 JS 渲染，curl 拿不到結果，資料集 rid 尚未確認。
- 高雄：api.kcg.gov.tw 從海外不可達（2026-09-12 複測同；先前 YouBike 技能已記錄同問題）。

台中擴充需另案評估（資料時效驗證＋排程欄位對齊）；其餘縣市待資料源穩定可連後再擴充，避免收錄無法驗證的指令。

完整步驟、查詢範例與錯誤處理請看 [SKILL.md]（../../taiwan-garbage/SKILL.md）。
