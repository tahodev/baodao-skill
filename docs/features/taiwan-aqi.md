# taiwan-aqi

環境部官方每小時空氣品質指標（AQI），可依縣市或測站查詢。

- 資料集：`AQX_P_432`，https://data.moenv.gov.tw/dataset/detail/AQX_P_432
- API：`https://data.moenv.gov.tw/api/v2/aqx_p_432`（需免費 MOENV API 金鑰）
- 欄位：測站、縣市、AQI、狀態、主要污染物、PM2.5、PM10、氣體濃度、發布時間與座標
- 2026-09-20 有效金鑰實測：HTTP 200，回傳 JSON 陣列；汐止/基隆樣本 AQI 52、普通、主要污染物為細懸浮微粒
- 依縣市查詢時正規化「台/臺」並列出多個測站，不把第一站當成全縣市單一 AQI
- 回報時附 `publishtime`；缺值或延遲要明說，不自行推估
- 金鑰只放環境變數或安全儲存，不進 repo、issue、PR、日誌或回覆

AQI 等級與完整命令、欄位、錯誤處理請看 [SKILL.md](../../taiwan-aqi/SKILL.md)。
