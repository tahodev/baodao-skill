# invoice-winning-numbers

從財政部電子發票整合服務平台的公開頁面取得統一發票最新中獎號碼，並用手上的發票號碼對獎。免 API 金鑰、免登入，`curl` 即可。

- 資料來源:https://invoice.etax.nat.gov.tw/lastNumber.html
- 頁面含最新期別的中獎號碼單（特別獎、特獎、頭獎、領獎期間）
- 號碼可能分散在多個 HTML 標籤裡，務必先移除標籤再解析
- 對獎規則:特別獎/特獎 8 碼全對;頭獎 8 碼全對 20 萬，末 7~3 碼依序為二~六獎
- 民國年 = 西元年 - 1911

完整步驟、解析範例與錯誤處理請看 [SKILL.md](../../invoice-winning-numbers/SKILL.md)。
