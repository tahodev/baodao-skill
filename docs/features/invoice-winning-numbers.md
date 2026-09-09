# invoice-winning-numbers

從財政部電子發票整合服務平台的公開頁面取得統一發票中獎號碼並對獎。免 API 金鑰、免登入,`curl` 即可。

- 最新期:https://invoice.etax.nat.gov.tw/lastNumber.html
- 雲端發票專屬獎:https://invoice.etax.nat.gov.tw/cloudNowNumber.html → 各獎別 PDF 清單,用 pdftotext 取出「字軌+8碼」全碼比對;歷年專屬獎在 cloudListNumber.html
- 一般發票歷史期別:https://www.etax.nat.gov.tw/etw-main/ETW183W2_<民國年3碼+起始月2碼>（JS 頁面,手動確認用）
- 支援批次對獎（多張發票一次對）;統一發票單月 25 日開獎,代理可在開獎日主動重對使用者的固定號碼
- 頁面解析務必先移除 HTML 標籤再取數字;領獎期間只引用與期別同區塊的文字
- 民國年 = 西元年 - 1911

完整步驟、解析範例與錯誤處理請看 [SKILL.md](../../invoice-winning-numbers/SKILL.md)。
