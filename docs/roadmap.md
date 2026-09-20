# 30 天計畫（roadmap）

這個倉庫以「一天一技能」的速度成長中。候選項目分兩類：**全新技能**與**既有技能的擴充**；打勾代表該項目完成，完成一個擴充項目不代表新增一個技能。

### 新技能候選（24 項，已完成 20 項）

- [x] 中央氣象署天氣預報（免費 API 金鑰）→ `cwa-weather`
- [x] 國定假日與連假查詢（行政院人事行政總處辦公日曆表）→ `taiwan-holidays`
- [x] 空氣品質指標 AQI → `taiwan-aqi`（2026-09-20）
- [x] 停車場剩餘車位 → `taiwan-parking`（台北市,2026-09-19）
- [x] 郵遞區號查詢 → `postal-address`（含地址英譯對照）
- [x] 台電電力供需資訊 → `taiwan-power`（2026-09-19）
- [x] 油價查詢（台灣中油）→ `taiwan-oil-price`（2026-09-19）
- [x] 停班停課公告 → `taiwan-suspension`（2026-09-19）
- [x] 農產品交易行情 → `taiwan-produce`（2026-09-19）
- [ ] 綜合所得稅試算
- [x] 統一編號與身分證字號檢核 → `taiwan-id-check`（2026-09-19）
- [x] 醫院診所查詢 → `taiwan-hospital`（2026-09-19）
- [ ] 公共圖書館館藏查詢（名錄已支援 → `taiwan-library`；館藏查詢待支援）
- [ ] 國道即時路況
- [x] 紫外線指數 → `taiwan-uv`（2026-09-19）
- [x] 停水公告 → `taiwan-water`（2026-09-19）
- [x] 節氣與農曆換算 → `taiwan-lunar-cal`（2026-09-19）
- [ ] 勞健保費率計算
- [x] 郵資計算 → `taiwan-postage`（2026-09-19）
- [x] 台股行情快照（TWSE/TPEX 每日收盤）→ `taiwan-stock`

- [x] 實價登錄查詢 → `taiwan-real-estate`（2026-09-19）
- [x] 博物館名錄 → `taiwan-museum`（2026-09-19）
- [x] 全國公廁查詢 → `taiwan-toilet`（2026-09-19）
- [x] 學校名錄與學生數 → `taiwan-schools`（2026-09-19）

### 既有技能的擴充（3 項，已完成 2 項）

- [x] 雲端發票專屬獎中獎號碼 → `invoice-winning-numbers`（PDF 清單解析，2026-09-09）
- [x] 地震速報與颱風動態 → `taiwan-weather` 的 NCDR CAP 段（2026-09-09）
- [ ] 其他縣市垃圾車 → `taiwan-garbage`（新北、台中已支援；桃園、台南、高雄待支援）

評估後否決（來源不合，不再重複評估）：

- 匯率查詢（台灣銀行牌告匯率）：台銀網站有 bot 防護，程式存取會被導到 JS 驗證頁、拿不到資料（2026-09-11 實測 HTTP 200 但回 Challenge Validation 頁）。
- 高鐵時刻表與票價、台鐵時刻表、公車動態查詢（TDX 運輸資料流通服務）：需要註冊會員取得 Client ID / Secret 才能呼叫（2026-09-11 實測 token 端點無憑證回 invalid_client），不符合本倉庫免金鑰的原則。

回功能表：[README](../README.md)
