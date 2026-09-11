<p align="center">
  <a href="https://tahodev.github.io/baodao-skill/">
    <img src="https://tahodev.github.io/baodao-skill/emblem.png" alt="baodao-skill 青花台字印章標誌" width="120">
  </a>
</p>

<h1 align="center">baodao-skill</h1>

<p align="center">
  台灣日常，交給 AI 代理。<br>
  <a href="https://tahodev.github.io/baodao-skill/"><strong>介紹網站 — tahodev.github.io/baodao-skill</strong></a>
</p>


台灣日常生活查詢的 AI 代理技能組合（寶島 = 台灣的美稱）。
只使用官方 API 與公開資料：財政部電子發票整合服務平台、臺北市資料大平臺、新北市資料開放平臺、台中市政府資料開放平臺、桃園市政府資料開放平臺、YouBike 微笑單車公開資料與官方地圖即時 feed、Open-Meteo、中央氣象署開放資料平臺、國家災害防救科技中心（NCDR CAP）。以不需要登入、不需要 API 金鑰就能安全使用的查詢型技能為核心；少數技能（cwa-weather）使用免費、即時發給的 API 金鑰。

Claude Code、Codex、OpenCode 等支援 `npx skills add` 的編碼代理（coding agent）都可以使用。

## 安裝

```bash
# 安裝全部技能
npx --yes skills add tahodev/baodao-skill --all -g

# 只安裝特定技能
npx --yes skills add tahodev/baodao-skill --skill invoice-winning-numbers -g
```

需要 Node.js 18 以上與 `npx`。詳見[安裝指南]（docs/install.md）。

## 功能

「登入」欄只表示使用者本人是否需要帳號或密鑰。

| 功能 | 技能名 | 說明 | 登入 | 文件 |
| --- | --- | --- | --- | --- |
| 統一發票對獎 | `invoice-winning-numbers` | 最新中獎號碼對獎、批次對獎、雲端發票專屬獎（PDF 清單）、歷史期別指引 | 不需要 | [invoice-winning-numbers 指南](docs/features/invoice-winning-numbers.md) |
| YouBike 站點即時查詢 | `youbike-realtime` | 全台 14 個服務區（雙北、桃園、台中、台南、高雄等）YouBike 2.0 站點的可借車輛、可還空位即時數量，含電輔車篩選 | 不需要 | [youbike-realtime 指南](docs/features/youbike-realtime.md) |
| 台北/新北/台中垃圾車路線 | `taiwan-garbage` | 台北市（CSV）、新北市（JSON API）與台中市（data.gov.tw 84004 資源下載）的垃圾清運點與停靠時間；新北、台中含星期排程，可判斷今天有沒有收 | 不需要 | [taiwan-garbage 指南](docs/features/taiwan-garbage.md) |
| 中央氣象署天氣預報 | `cwa-weather` | 用 CWA 開放資料 API 查各縣市 36 小時與鄉鎮預報（官方資料） | 需要（免費即時發給） | [cwa-weather 指南](docs/features/cwa-weather.md) |
| 台灣天氣查詢 | `taiwan-weather` | 用 Open-Meteo（免金鑰）查天氣，並用 NCDR CAP feed（免金鑰）查颱風/地震/海嘯等災害警報（cwa-weather 的免金鑰備援） | 不需要 | [taiwan-weather 指南](docs/features/taiwan-weather.md) |
| 國定假日與連假查詢 | `taiwan-holidays` | 行政院人事行政總處辦公日曆表：國定假日、連假、補班日（當年度 xlsx 月曆 + 歷年結構化 CSV） | 不需要 | [taiwan-holidays 指南](docs/features/taiwan-holidays.md) |
| 台股行情快照 | `taiwan-stock` | 上市（TWSE）與上櫃（TPEX）每日收盤行情、個股本月每日成交、大盤指數（收盤統計，非盤中報價） | 不需要 | [taiwan-stock 指南](docs/features/taiwan-stock.md) |
| 郵遞區號與地址英譯 | `postal-address` | 中華郵政官方對照表：3 碼郵遞區號、縣市鄉鎮/村里/路街中英對照（漢語拼音） | 不需要 | [postal-address 指南](docs/features/postal-address.md) |

各技能的**正本是 `<技能名>/SKILL.md`**。`docs/features/` 的指南是摘要版，詳細步驟、參數與錯誤處理請務必參考 SKILL.md。

範圍說明：

- 防爬蟲嚴格的服務（蝦皮、momo、591、foodpanda 等）不在範圍內。
- 不改變外部狀態：不預約、不購買、不發文，只有查詢與計算。
- 資料是各官方來源公告的原始內容。重要判斷（領獎期限、停收日、颱風警報等）請務必回到官方網站確認。

## 30 天計畫

這個倉庫以「一天一技能」的速度成長中，目前有 5 個技能（見上方功能表）。候選項目分兩類：**全新技能**與**既有技能的擴充**；打勾代表該項目完成，完成一個擴充項目不代表新增一個技能。

### 新技能候選（20 項，已完成 4 項）

- [x] 中央氣象署天氣預報（免費 API 金鑰）→ `cwa-weather`
- [x] 國定假日與連假查詢（行政院人事行政總處辦公日曆表）→ `taiwan-holidays`
- [ ] 空氣品質指標 AQI
- [ ] 停車場剩餘車位
- [x] 郵遞區號查詢 → `postal-address`（含地址英譯對照）
- [ ] 台電電力供需資訊
- [ ] 油價查詢（台灣中油）
- [ ] 停班停課公告
- [ ] 農產品交易行情
- [ ] 綜合所得稅試算
- [ ] 統一編號與身分證字號檢核
- [ ] 醫院診所查詢
- [ ] 公共圖書館館藏查詢
- [ ] 國道即時路況
- [ ] 紫外線指數
- [ ] 停水公告
- [ ] 節氣與農曆換算
- [ ] 勞健保費率計算
- [ ] 郵資計算
- [x] 台股行情快照（TWSE/TPEX 每日收盤）→ `taiwan-stock`

### 既有技能的擴充（3 項，已完成 2 項）

- [x] 雲端發票專屬獎中獎號碼 → `invoice-winning-numbers`（PDF 清單解析，2026-09-09）
- [x] 地震速報與颱風動態 → `taiwan-weather` 的 NCDR CAP 段（2026-09-09）
- [ ] 其他縣市垃圾車 → `taiwan-garbage`（新北、台中已支援；桃園、台南、高雄待支援）

評估後否決（來源不合，不再重複評估）：

- 匯率查詢（台灣銀行牌告匯率）：台銀網站有 bot 防護，程式存取會被導到 JS 驗證頁、拿不到資料（2026-09-11 實測 HTTP 200 但回 Challenge Validation 頁）。
- 高鐵時刻表與票價、台鐵時刻表、公車動態查詢（TDX 運輸資料流通服務）：需要註冊會員取得 Client ID / Secret 才能呼叫（2026-09-11 實測 token 端點無憑證回 invalid_client），不符合本倉庫免金鑰的原則。

## English

**baodao-skill** (寶島, "baodao" = treasure island, an affectionate name for Taiwan) is a collection of AI-agent skills for daily life in Taiwan. It focuses on read-only lookups built only on official APIs and public datasets: no login walls, no API keys, no scraping. One exception: `cwa-weather` uses a CWA API key - free and issued instantly on registration (the other four skills need no key).

Works with any coding agent that supports `npx skills add` (Claude Code, Codex, OpenCode, ...).

### Install

```bash
# Install every skill
npx --yes skills add tahodev/baodao-skill --all -g

# Install a single skill
npx --yes skills add tahodev/baodao-skill --skill invoice-winning-numbers -g
```

Node.js 18+ and `npx` are required. See the [install guide](docs/install.md) for details.

### What you can do

| What you can do | Skill | Description | Login | Docs |
| --- | --- | --- | --- | --- |
| Check Taiwan uniform-invoice winning numbers | `invoice-winning-numbers` | Latest winning numbers, batch matching, cloud-invoice exclusive prizes (PDF lists), and history pointers from the Ministry of Finance's public pages | Not required | [invoice-winning-numbers guide](docs/features/invoice-winning-numbers.md) |
| Look up YouBike station availability | `youbike-realtime` | Real-time rentable bikes and return docks for YouBike 2.0 stations across 14 service areas nationwide (Taipei, New Taipei, Taoyuan, Taichung, Tainan, Kaohsiung, and more), incl. e-bike filtering | Not required | [youbike-realtime guide](docs/features/youbike-realtime.md) |
| Look up garbage truck routes | `taiwan-garbage` | Collection stops and times for Taipei (CSV), New Taipei (JSON API), and Taichung (data.gov.tw 84004 download); New Taipei and Taichung carry weekday schedules so you can tell whether there is collection today | Not required | [taiwan-garbage guide](docs/features/taiwan-garbage.md) |
| Look up official CWA forecasts | `cwa-weather` | 36-hour county and township forecasts from the CWA open-data API (official source) | Free instant API key | [cwa-weather guide](docs/features/cwa-weather.md) |
| Look up weather in Taiwan | `taiwan-weather` | Keyless Open-Meteo weather plus keyless disaster alerts (typhoon, earthquake, tsunami) via the NCDR CAP feeds (fallback for cwa-weather) | Not required | [taiwan-weather guide](docs/features/taiwan-weather.md) |
| Look up Taiwan public holidays | `taiwan-holidays` | DGPA government work calendar: national holidays, long weekends, makeup workdays (current-year xlsx + historical structured CSV) | Not required | [taiwan-holidays guide](docs/features/taiwan-holidays.md) |
| Taiwan stock daily-close snapshot | `taiwan-stock` | TWSE/TPEX daily closing quotes, per-stock daily rows, index levels (close statistics, not intraday) | Not required | [taiwan-stock guide](docs/features/taiwan-stock.md) |
| Postal codes and address transliteration | `postal-address` | Chunghwa Post tables: 3-digit postal codes plus county/village/road Chinese-English tables (Hanyu Pinyin) | Not required | [postal-address guide](docs/features/postal-address.md) |

The canonical source for each skill is its `<skill>/SKILL.md`. The guides under `docs/features/` are summaries only - always refer to SKILL.md for full procedures, parameters, and error handling.

Scope notes:

- Services with heavy anti-scraping are out of scope.
- Nothing here changes state: no reservations, purchases, or posts. Lookups and calculations only.
- Data is quoted as-is from official sources. Confirm anything important (claim deadlines, collection holidays, typhoon warnings) on the official site.

This repo grows one skill per day - see the roadmap above.

## 授權 / License

[MIT](LICENSE)
