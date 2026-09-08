# Changelog

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [0.1.0] - 2026-09-09

### Added

- `invoice-winning-numbers`:統一發票中獎號碼查詢與對獎(財政部電子發票整合服務平台公開頁面)
- `youbike-realtime`:台北市+新北市 YouBike 2.0 站點即時可借/可還查詢(官方公開 JSON)
- `taipei-garbage`:台北市垃圾清運路線與停靠時間查詢(臺北市資料大平臺 CSV)
- `taiwan-weather`:台灣各縣市天氣查詢(Open-Meteo,免金鑰)
- `cwa-weather`:中央氣象署開放資料天氣預報(F-C0032-001 / F-D0047 系列,免費即時發給的 API 金鑰)
- 初始倉庫結構:README(zh-TW + English)、AGENTS.md、CONTRIBUTING.md、docs/、issue templates
- CI:每日 health-check workflow(frontmatter lint + SKILL.md 內 URL 全數 curl 檢查,失敗自動開 issue)

### Fixed

- `invoice-winning-numbers`:HTML 標籤改為整個刪除(原先取代成空白會把 8 碼中獎號碼切成 3 碼碎片)
- `invoice-winning-numbers`:領獎期間只引用與期別同區塊的文字;取不到時依「開獎日次月 6 日起 3 個月」推算並註明需向官方確認(頁面殘留的領獎期間常是上一期)
- `taiwan-weather`:座標表擴充到 22 縣市(另收錄墾丁、埔里);地理編碼 API 只認英文/拼音地名,修正備援指引
