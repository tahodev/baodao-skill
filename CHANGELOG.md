# Changelog

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [0.2.0] - 2026-09-09

### Added

- `invoice-winning-numbers`:批次對獎腳本（多張發票一次對）、雲端發票專屬獎完整查法（cloudNowNumber.html → 各獎別 PDF 清單 → pdftotext,獎別依 PDF 標題行識別,字軌+8碼全碼比對）、歷年專屬獎（cloudListNumber.html）、一般發票歷史期別指引（ETW183W2_<期別>,JS 頁面僅供手動確認）、每期開獎日（單月 25 日）自動對獎流程
- `youbike-realtime`:新增台中市（newdatacenter.taichung.gov.tw,1,824 站）與桃園市（opendata.tycg.gov.tw,需帶 limit=2000,702 站）;電輔車篩選（新北 `eyb_quantity`、台中/桃園 `sbi_detail`）
- `taipei-garbage` → 改名 `taiwan-garbage`:新增新北市（data.ntpc.gov.tw JSON API,分頁上限 10,000 列、全量約 26,655 列,含 `garbage<weekday>`/`recycling<weekday>` 星期排程欄位,可判斷「今天有沒有收」）;兩市皆加入依經緯度找最近清運點範例
- `taiwan-weather`:新增災害警報查詢（NCDR CAP 公開 feed,免金鑰;AlertType 5=颱風、6=地震、7=海嘯、8=淹水、9=土石流及大規模崩塌、10=降雨、11=河川高水位;3 秒速率限制）、Open-Meteo vs CWA 選擇對照表
- `cwa-weather`:新增警特報指引（免金鑰走 NCDR CAP;CWA 官網 2026-09-09 實測 403 Bot 防護）

### Notes

- 高雄市 YouBike:已知來源 data.kcg.gov.tw 於 2026-09-09 連線逾時無法驗證,暫未收錄

## [0.1.0] - 2026-09-09

### Added

- `invoice-winning-numbers`:統一發票中獎號碼查詢與對獎（財政部電子發票整合服務平台公開頁面）
- `youbike-realtime`:台北市+新北市 YouBike 2.0 站點即時可借/可還查詢（官方公開 JSON）
- `taipei-garbage`:台北市垃圾清運路線與停靠時間查詢（臺北市資料大平臺 CSV）
- `taiwan-weather`:台灣各縣市天氣查詢（Open-Meteo，免金鑰）
- `cwa-weather`:中央氣象署開放資料天氣預報（F-C0032-001 / F-D0047 系列，免費即時發給的 API 金鑰）
- 初始倉庫結構:README（zh-TW + English）、AGENTS.md、CONTRIBUTING.md、docs/、issue templates
- CI:每日 health-check workflow（frontmatter lint + SKILL.md 內 URL 全數 curl 檢查，失敗自動開 issue）

### Fixed

- `invoice-winning-numbers`:HTML 標籤改為整個刪除（原先取代成空白會把 8 碼中獎號碼切成 3 碼碎片）
- `invoice-winning-numbers`:領獎期間只引用與期別同區塊的文字;取不到時依「開獎日次月 6 日起 3 個月」推算並註明需向官方確認（頁面殘留的領獎期間常是上一期）
- `taiwan-weather`:座標表擴充到 22 縣市（另收錄墾丁、埔里）;地理編碼 API 只認英文/拼音地名，修正備援指引
