# CONTRIBUTING

歡迎貢獻。這個倉庫收集台灣日常生活查詢的 AI 代理技能。

## 原則

- 只用官方 API 與公開資料，且不需要登入（可即時免費申請的 API 金鑰可接受）。個人金鑰不提交進倉庫；政府資料平臺公布的資料集公用 key（如 taiwan-toilet 用的 data.gov.tw resource key）例外，但要在 SKILL.md 註明來源頁。
- 只有查詢與計算，不改變外部狀態。
- SKILL.md 裡的指令與 URL 都必須實測過。

## 新增技能的步驟

1. 在根目錄建立 `<技能名>/SKILL.md`（frontmatter 需要 name、description、license;英文 kebab-case 命名）。
2. 內容用台灣繁體中文，包含:基本流程、欄位或參數說明、錯誤與失敗時的處理、English summary。
3. 在 `docs/features/<技能名>.md` 寫一頁摘要。
4. 更新 README 的功能表與 30 天計畫。
5. 更新 CHANGELOG.md。

## 共同慣例

回報給使用者的共通規則（附資料時間、缺值處理、常見陷阱）見 [docs/response-contract.md](docs/response-contract.md)。

民國年換算、Big5 編碼、curl 習慣、時區等跨技能共通處理，見 [docs/conventions.md](docs/conventions.md)。

## 回報問題

端點失效、欄位變更、數值錯誤等，請開 issue，並附上實際執行的指令與回應。
