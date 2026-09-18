# taiwan-real-estate

內政部實價登錄季度批次下載（買賣/預售屋/租賃全台 CSV）。免金鑰。

- 下載：https://plvr.land.moi.gov.tw/DownloadSeason?season=115S2&type=zip&fileName=lvr_landcsv.zip（2026-09-19 實測 200、14.7MB）
- 季代碼 = 民國年+S+季；當季沒有就往前推；檔名 `<縣市碼>_lvr_land_a/b/c.csv`
- UTF-8 BOM、**雙標頭**（第 2 列英文要跳過）、日期民國年（1150601）
- 欄位含 總價元、單價元平方公尺（×3.30579 = 坪價）；實測：台北市檔 5,609 列，中山區車位 115/06/01 總價 370 萬
- 申報制有 1-2 個月落差；門牌去識別化；特殊交易看備註

完整步驟請看 [SKILL.md](../../taiwan-real-estate/SKILL.md)。
