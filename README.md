# baodao-skill

台灣日常生活查詢的 AI 代理技能組合（寶島 = 台灣的美稱）。
只使用官方 API 與公開資料:財政部電子發票整合服務平台、臺北市資料大平臺、YouBike 微笑單車公開資料、Open-Meteo、中央氣象署開放資料平臺。以不需要登入、不需要 API 金鑰就能安全使用的查詢型技能為核心;少數技能（cwa-weather）使用免費、即時發給的 API 金鑰。

Claude Code、Codex、OpenCode 等支援 `npx skills add` 的編碼代理（coding agent）都可以使用。

## 安裝

```bash
# 安裝全部技能
npx --yes skills add tahodev/baodao-skill --all -g

# 只安裝特定技能
npx --yes skills add tahodev/baodao-skill --skill invoice-winning-numbers -g
```

需要 Node.js 18 以上與 `npx`。詳見[安裝指南](docs/install.md)。

## 功能

「登入」欄只表示使用者本人是否需要帳號或密鑰。

| 功能 | 技能名 | 說明 | 登入 | 文件 |
| --- | --- | --- | --- | --- |
| 統一發票對獎 | `invoice-winning-numbers` | 從財政部電子發票整合服務平台公開頁面取得最新中獎號碼並對獎 | 不需要 | [invoice-winning-numbers 指南](docs/features/invoice-winning-numbers.md) |
| YouBike 站點即時查詢 | `youbike-realtime` | 台北市+新北市 YouBike 2.0 站點的可借車輛、可還空位即時數量（其他縣市未支援） | 不需要 | [youbike-realtime 指南](docs/features/youbike-realtime.md) |
| 台北市垃圾車路線 | `taipei-garbage` | 臺北市資料大平臺的垃圾清運路線 CSV:各里清運點與抵達時間 | 不需要 | [taipei-garbage 指南](docs/features/taipei-garbage.md) |
| 中央氣象署天氣預報 | `cwa-weather` | 用 CWA 開放資料 API 查各縣市 36 小時與鄉鎮預報（官方資料） | 需要（免費即時發給） | [cwa-weather 指南](docs/features/cwa-weather.md) |
| 台灣天氣查詢 | `taiwan-weather` | 用 Open-Meteo（免金鑰）查台灣各縣市現在天氣與未來預報（cwa-weather 的免金鑰備援） | 不需要 | [taiwan-weather 指南](docs/features/taiwan-weather.md) |

各技能的**正本是 `<技能名>/SKILL.md`**。`docs/features/` 的指南是摘要版，詳細步驟、參數與錯誤處理請務必參考 SKILL.md。

範圍說明:

- 防爬蟲嚴格的服務（蝦皮、momo、591、foodpanda 等）不在範圍內。
- 不改變外部狀態:不預約、不購買、不發文，只有查詢與計算。
- 資料是各官方來源公告的原始內容。重要判斷（領獎期限、停收日、颱風警報等）請務必回到官方網站確認。

## 30 天計畫

這個倉庫以「一天一技能」的速度成長中。以下是候選技能，順序未定，完成後會打勾:

- [ ] 國定假日與連假查詢（行政院人事行政總處辦公日曆表）
- [x] 中央氣象署天氣預報（免費 API 金鑰）→ `cwa-weather`
- [ ] 雲端發票專屬獎中獎號碼
- [ ] 其他縣市垃圾車（新北、桃園、台中、台南、高雄）
- [ ] 高鐵時刻表與票價（TDX，免費 API 金鑰）
- [ ] 台鐵時刻表（TDX，免費 API 金鑰）
- [ ] 公車動態查詢（TDX）
- [ ] 空氣品質指標 AQI
- [ ] 地震速報與颱風動態
- [ ] 停車場剩餘車位
- [ ] 郵遞區號查詢
- [ ] 台電電力供需資訊
- [ ] 油價查詢（台灣中油）
- [ ] 匯率查詢
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

## English

**baodao-skill** (寶島, "baodao" = treasure island, an affectionate name for Taiwan) is a collection of AI-agent skills for daily life in Taiwan. It focuses on read-only lookups built only on official APIs and public datasets: no login walls, no API keys, no scraping.

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
| Check Taiwan uniform-invoice winning numbers | `invoice-winning-numbers` | Latest winning numbers from the Ministry of Finance's public e-invoice pages, plus a prize-matching procedure | Not required | [invoice-winning-numbers guide](docs/features/invoice-winning-numbers.md) |
| Look up YouBike station availability | `youbike-realtime` | Real-time rentable bikes and return docks for Taipei + New Taipei YouBike 2.0 stations (other cities not supported) | Not required | [youbike-realtime guide](docs/features/youbike-realtime.md) |
| Look up Taipei garbage truck routes | `taipei-garbage` | Collection stops and arrival times per neighborhood from the Taipei open-data CSV | Not required | [taipei-garbage guide](docs/features/taipei-garbage.md) |
| Look up official CWA forecasts | `cwa-weather` | 36-hour county and township forecasts from the CWA open-data API (official source) | Free instant API key | [cwa-weather guide](docs/features/cwa-weather.md) |
| Look up weather in Taiwan | `taiwan-weather` | Current weather and forecasts for Taiwanese cities via the keyless Open-Meteo API (keyless fallback for cwa-weather) | Not required | [taiwan-weather guide](docs/features/taiwan-weather.md) |

The canonical source for each skill is its `<skill>/SKILL.md`. The guides under `docs/features/` are summaries only - always refer to SKILL.md for full procedures, parameters, and error handling.

Scope notes:

- Services with heavy anti-scraping are out of scope.
- Nothing here changes state: no reservations, purchases, or posts. Lookups and calculations only.
- Data is quoted as-is from official sources. Confirm anything important (claim deadlines, collection holidays, typhoon warnings) on the official site.

This repo grows one skill per day - see the roadmap above.

## 授權 / License

[MIT](LICENSE)
