# CONTRIBUTING

歡迎貢獻。這個倉庫收集台灣日常生活查詢的 AI 代理技能。

## 原則

- 只用官方 API 與公開資料,且不需要登入(可即時免費申請的 API 金鑰可接受)。
- 只有查詢與計算,不改變外部狀態。
- SKILL.md 裡的指令與 URL 都必須實測過。

## 新增技能的步驟

1. 在根目錄建立 `<技能名>/SKILL.md`(frontmatter 需要 name、description、license;英文 kebab-case 命名)。
2. 內容用台灣繁體中文,包含:基本流程、欄位或參數說明、錯誤與失敗時的處理、English summary。
3. 在 `docs/features/<技能名>.md` 寫一頁摘要。
4. 更新 README 的功能表與 30 天計畫。
5. 更新 CHANGELOG.md。

## 回報問題

端點失效、欄位變更、數值錯誤等,請開 issue,並附上實際執行的指令與回應。
