# Changelog

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [0.3.1] - 2026-09-11

### Fixed

- CI:`scripts/check-urls.sh` 修正模板 URL 擷取 — 含 `<...>` 佔位符的 URL(如 `ETW183W2_<期別>`、`pdf/<檔名>.pdf`、`name=<英文地名>`)先前在 `<` 處被截斷,殘段(`ETW183W2_`、`pdf/` 等)被當真網址 curl 而 404/403,是 health-check 連續失敗的主因;現在整段擷取後以 templated 跳過
- `taiwan-weather` / `cwa-weather`:錯誤處理一節過時的「颱風、警報相關問題:本技能不提供,直接請使用者看中央氣象署」改為指向 NCDR CAP 免金鑰段(該能力 0.2.0 已加入,條目未同步)
- `docs/install.md`:技能名範例 `taipei-garbage` 更正為 `taiwan-garbage`(0.2.0 改名後未同步)
- CI:health-check 失敗自動開的 issue,標題日期現在會在既有 issue 上同步更新,不再停留在第一次失敗的日期

### Added

- `docs/install.md`:新增「乾淨環境安裝實測(2026-09-11)」— `--all -g` 非互動可裝;單一技能在無 TTY 環境需加 `-y`,否則提示取消、什麼都不裝;Eve / PromptScript 不支援全域安裝會被略過
- `docs/install.md`:補上執行期需求(curl、jq、python3、pdftotext、awk/sed)
- README:30 天計畫新增「評估後否決」區塊 — 台銀匯率(bot 防護,2026-09-11 實測回 Challenge Validation 頁)、TDX 三項(高鐵/台鐵/公車,需註冊 Client ID/Secret),避免重複研究

### Changed

- 5 個 SKILL.md、README、docs/features/、docs/install.md:zh-TW 標點統一為全形(，：；（）？!),程式碼區塊、行內 code、URL 與英文段落維持半形

## [0.3.0] - 2026-09-10

### Added

- `youbike-realtime`:新增官方統一即時 feed(apis.youbike.com.tw/json/station-yb2.json,youbike.com.tw 地圖使用的 JSON)作為主要資料源 — 一次取回全台 14 個服務區約 9,500 站(2026-09-10 實測 9,521 站),新增高雄、台南、新竹、嘉義、苗栗、屏東、台東等縣市;每站含電輔車明細 `available_spaces_detail`(yb1/yb2/eyb),台北電輔車篩選從「不支援」變成可用;雙北邊界查詢可用 `area_code` 一次完成。各市府 feed 保留為備援,統一 feed 為非公開文件化 API 的注意事項已記載
- `youbike-realtime`:站名「台 / 臺」正規化指引(台北 147 站用「臺」、新北兩者混用、統一 feed 全台 385 站含「臺」),搜尋範例改用 `gsub("臺";"台")`
- `youbike-realtime`:更新時間欄位格式對照表(台北 `YYYY-MM-DD HH:MM:SS`、新北 `YYYYMMDDTHHMMSS`、台中/桃園 `YYYYMMDDHHMMSS`、統一 feed `updated_at`,全部 UTC+8)
- `youbike-realtime`:雙北市府 feed 合併查詢範例(`jq -sr` 欄位正規化後合併)
- CI:`scripts/check-urls.sh` 新增 YouBike feed 深度驗證 — JSON 解析 + 各 feed 最低站數門檻,抓出「HTTP 200 但回錯誤頁或空 JSON」的沉默失敗;深度驗證過的 URL 不再重複做一般 curl 檢查

### Changed

- `youbike-realtime`:站數改為約略值並標註實測日(2026-09-10),避免設站增加造成文件數字失真(桃園 702 → 約 700,實測 703)
- `youbike-realtime`:高雄市改為經統一 feed 支援(`area_code=="12"`);高雄市政府 openapi.kcg.gov.tw 端點 2026-09-09 從台灣境外連線逾時、無法驗證,標註為不可依賴
- `youbike-realtime`:桃園 `limit` 注意事項強化 — 回傳筆數等於 `limit` 時可能被截斷,要加大再查

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
