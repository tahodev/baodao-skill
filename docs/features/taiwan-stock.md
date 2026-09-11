# taiwan-stock

台股每日收盤行情快照。免登入、免 API 金鑰。資料是收盤後的每日統計，不是盤中即時報價。

- 上市全市場：`https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL`（JSON 陣列，最新交易日全部個股）
- 上櫃全市場：`https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes`（JSON 陣列）
- 個股本月每日成交：`https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=YYYYMMDD&stockNo=<代號>`
- 大盤與分類指數：`https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=YYYYMMDD&type=ALLBUT0999`
- 日期欄位是民國年（1150911＝2026-09-11）；非交易日會回空，往前找最近交易日
- 以上全部 2026-09-12 實測 HTTP 200

jq 查詢範例與錯誤處理請看 [SKILL.md](../../taiwan-stock/SKILL.md)。
