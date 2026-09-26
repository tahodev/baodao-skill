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
只使用官方 API 與公開資料：財政部電子發票整合服務平台、臺北市資料大平臺、新北市資料開放平臺、台中市政府資料開放平臺、桃園市政府資料開放平臺、YouBike 微笑單車公開資料與官方地圖即時 feed、Open-Meteo、中央氣象署開放資料平臺、環境部環境資料開放平臺、國家災害防救科技中心（NCDR CAP）。以不需要登入、不需要 API 金鑰就能安全使用的查詢型技能為核心；少數技能（cwa-weather、taiwan-uv、taiwan-aqi）使用免費申請的 API 金鑰。

Claude Code、Codex、OpenCode 等支援 `npx skills add` 的編碼代理（coding agent）都可以使用。

## 安裝

```bash
# 安裝全部技能
npx --yes skills add tahodev/baodao-skill --all -g

# 只安裝特定技能
npx --yes skills add tahodev/baodao-skill --skill invoice-winning-numbers -g
```

需要 Node.js 18 以上與 `npx`。詳見[安裝指南](docs/install.md);不知道從哪個技能開始請看[入門指南](docs/getting-started.md)。

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
| 統編與身分證字號檢核 | `taiwan-id-check` | 統一編號與身分證字號檢查碼驗證（純本地計算，零網路） | 不需要 | [taiwan-id-check 指南](docs/features/taiwan-id-check.md) |
| 台北市停車場剩位 | `taiwan-parking` | 停管處 TCMSV 公開 JSON：1,188 場即時剩位＋1,775 場靜態資料（費率、地址,2026-09-26 實測） | 不需要 | [taiwan-parking 指南](docs/features/taiwan-parking.md) |
| 中油每週油價 | `taiwan-oil-price` | 台灣中油歷史油價頁：92/95/98 無鉛與超柴週牌價 | 不需要 | [taiwan-oil-price 指南](docs/features/taiwan-oil-price.md) |
| 停班停課公告 | `taiwan-suspension` | 人事行政總處天然災害停班停課官方公告 | 不需要 | [taiwan-suspension 指南](docs/features/taiwan-suspension.md) |
| 農產品批發行情 | `taiwan-produce` | 農業部開放資料：全台 24 個批發市場蔬果行情（上中下價與交易量） | 不需要 | [taiwan-produce 指南](docs/features/taiwan-produce.md) |
| 健保特約院所查詢 | `taiwan-hospital` | 健保署開放資料 API：37,133 家特約醫院診所名錄（地址、電話、科別、服務時段姊妹集） | 不需要 | [taiwan-hospital 指南](docs/features/taiwan-hospital.md) |
| 郵資查詢 | `taiwan-postage` | 中華郵政資費表：國內信函/包裹/快捷/國際資費 | 不需要 | [taiwan-postage 指南](docs/features/taiwan-postage.md) |
| 紫外線指數 | `taiwan-uv` | 中央氣象署各測站每日紫外線指數最大值（O-A0005-001） | 需要（免費即時發給） | [taiwan-uv 指南](docs/features/taiwan-uv.md) |
| 空氣品質指標 | `taiwan-aqi` | 環境部每小時測站 AQI、主要污染物、PM2.5/PM10 與發布時間（AQX_P_432） | 需要（免費申請） | [taiwan-aqi 指南](docs/features/taiwan-aqi.md) |
| 台電電力供需 | `taiwan-power` | 台電開放資料：目前用電、預估尖峰、備轉容量率與供電燈號 | 不需要 | [taiwan-power 指南](docs/features/taiwan-power.md) |
| 實價登錄查詢 | `taiwan-real-estate` | 內政部實價登錄季度批次下載：全台買賣/預售屋/租賃成交資料 | 不需要 | [taiwan-real-estate 指南](docs/features/taiwan-real-estate.md) |
| 停水公告 | `taiwan-water` | 台灣自來水公司停水/降壓案件（起訖時間、範圍、戶數、原因） | 不需要 | [taiwan-water 指南](docs/features/taiwan-water.md) |
| 圖書館名錄 | `taiwan-library` | 國家圖書館彙編全台 5,207 館清單（公共/學校/專門圖書館） | 不需要 | [taiwan-library 指南](docs/features/taiwan-library.md) |
| 博物館名錄 | `taiwan-museum` | 文化部全台 144 間博物館（地址、票價、電話、經緯度） | 不需要 | [taiwan-museum 指南](docs/features/taiwan-museum.md) |
| 全國公廁查詢 | `taiwan-toilet` | 環境部全國公廁建檔資料（位置、管理單位、評鑑等級、尿布台） | 不需要 | [taiwan-toilet 指南](docs/features/taiwan-toilet.md) |
| 學校名錄與學生數 | `taiwan-schools` | 教育部統計處校別資料：國中/國小學校代碼、班級數、學生數 | 不需要 | [taiwan-schools 指南](docs/features/taiwan-schools.md) |
| 農曆與節氣換算 | `taiwan-lunar-cal` | 國曆轉農曆（1900-2100 含閏月）、二十四節氣日期、生肖（純本地計算） | 不需要 | [taiwan-lunar-cal 指南](docs/features/taiwan-lunar-cal.md) |

各技能的**正本是 `<技能名>/SKILL.md`**。`docs/features/` 的指南是摘要版，詳細步驟、參數與錯誤處理請務必參考 SKILL.md。

範圍說明：

- 防爬蟲嚴格的服務（蝦皮、momo、591、foodpanda 等）不在範圍內。
- 不改變外部狀態：不預約、不購買、不發文，只有查詢與計算。
- 資料是各官方來源公告的原始內容。重要判斷（領獎期限、停收日、颱風警報等）請務必回到官方網站確認。

## 30 天計畫

這個倉庫以「一天一技能」的速度成長中，目前有 25 個技能（見上方功能表）。候選清單與否決紀錄見 [docs/roadmap.md](docs/roadmap.md)。

## English

**baodao-skill** (寶島, "baodao" = treasure island, an affectionate name for Taiwan) is a collection of AI-agent skills for daily life in Taiwan. It focuses on read-only lookups built only on official APIs and public datasets, with no scraping or paid access. Most skills need no key. `cwa-weather` and `taiwan-uv` use a free CWA key; `taiwan-aqi` uses a free MOENV open-data key.

Works with any coding agent that supports `npx skills add` (Claude Code, Codex, OpenCode, ...).

### Install

```bash
# Install every skill
npx --yes skills add tahodev/baodao-skill --all -g

# Install a single skill
npx --yes skills add tahodev/baodao-skill --skill invoice-winning-numbers -g
```

Node.js 18+ and `npx` are required. See the [install guide](docs/install.md) for details, or the [getting-started guide](docs/getting-started.md) (Chinese) to pick skills by purpose.

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
| UBN and national ID checksum | `taiwan-id-check` | Uniform Business Number and national ID checksum validation (pure local computation, zero network) | Not required | [taiwan-id-check guide](docs/features/taiwan-id-check.md) |
| Taipei parking availability | `taiwan-parking` | TCMSV public JSON: real-time spaces for 1,188 lots plus static details for 1,775 (pricing, addresses; measured 2026-09-26) | Not required | [taiwan-parking guide](docs/features/taiwan-parking.md) |
| CPC weekly fuel prices | `taiwan-oil-price` | CPC history page: weekly list prices for 92/95/98 unleaded and premium diesel | Not required | [taiwan-oil-price guide](docs/features/taiwan-oil-price.md) |
| Work/class suspension notices | `taiwan-suspension` | DGPA official natural-disaster work and class suspension announcements | Not required | [taiwan-suspension guide](docs/features/taiwan-suspension.md) |
| Wholesale produce prices | `taiwan-produce` | MOA open data: high/mid/low prices and volumes across 24 wholesale markets | Not required | [taiwan-produce guide](docs/features/taiwan-produce.md) |
| NHI-contracted providers | `taiwan-hospital` | NHI open-data API: 37,133 contracted hospitals and clinics (address, phone; hours and departments via sibling datasets) | Not required | [taiwan-hospital guide](docs/features/taiwan-hospital.md) |
| Postage rates | `taiwan-postage` | Chunghwa Post rate tables: domestic letters, parcels, express, international | Not required | [taiwan-postage guide](docs/features/taiwan-postage.md) |
| UV index | `taiwan-uv` | CWA daily max UV index per station (O-A0005-001) | Free instant API key | [taiwan-uv guide](docs/features/taiwan-uv.md) |
| Air Quality Index | `taiwan-aqi` | Official hourly station AQI, dominant pollutant, PM2.5/PM10 and publication time (AQX_P_432) | Free API key | [taiwan-aqi guide](docs/features/taiwan-aqi.md) |
| Taipower supply/demand | `taiwan-power` | Taipower open data: current load, forecast peak, reserve rate and supply indicator | Not required | [taiwan-power guide](docs/features/taiwan-power.md) |
| Real-price registry | `taiwan-real-estate` | MOI real-price registry quarterly batch downloads: sales, pre-sale, rentals nationwide | Not required | [taiwan-real-estate guide](docs/features/taiwan-real-estate.md) |
| Water outage notices | `taiwan-water` | Taiwan Water Corp outage/pressure-reduction cases (times, areas, households, causes) | Not required | [taiwan-water guide](docs/features/taiwan-water.md) |
| Library directory | `taiwan-library` | NCL directory of 5,207 libraries nationwide (public, school, special) | Not required | [taiwan-library guide](docs/features/taiwan-library.md) |
| Museum directory | `taiwan-museum` | Ministry of Culture list of 144 museums (address, ticket info, phone, coordinates) | Not required | [taiwan-museum guide](docs/features/taiwan-museum.md) |
| Public toilet lookup | `taiwan-toilet` | MOENV national public toilet registry (locations, managing orgs, inspection grades, diaper stations) | Not required | [taiwan-toilet guide](docs/features/taiwan-toilet.md) |
| School directory & enrollment | `taiwan-schools` | MOE school-level data: codes, districts, class and student counts for elementary/junior-high schools | Not required | [taiwan-schools guide](docs/features/taiwan-schools.md) |
| Lunar calendar & solar terms | `taiwan-lunar-cal` | Gregorian-to-lunar conversion (1900-2100 incl. leap months), 24 solar terms, zodiac (pure local computation) | Not required | [taiwan-lunar-cal guide](docs/features/taiwan-lunar-cal.md) |

The canonical source for each skill is its `<skill>/SKILL.md`. The guides under `docs/features/` are summaries only - always refer to SKILL.md for full procedures, parameters, and error handling.

Scope notes:

- Services with heavy anti-scraping are out of scope.
- Nothing here changes state: no reservations, purchases, or posts. Lookups and calculations only.
- Data is quoted as-is from official sources. Confirm anything important (claim deadlines, collection holidays, typhoon warnings) on the official site.

This repo grows one skill per day - see [docs/roadmap.md](docs/roadmap.md) for the candidate list.

## 授權 / License

[MIT](LICENSE)
