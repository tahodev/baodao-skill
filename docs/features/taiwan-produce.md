# taiwan-produce

全台 24 個果菜批發市場行情。免金鑰，農業部開放資料 CSV。

- 來源：https://data.moa.gov.tw/Service/OpenData/FromM/FarmTransData.aspx?FOTT=CSV&IsTransData=1&UnitId=037（2026-09-19 實測 200、約 608KB、UTF-8 BOM、8,782 筆）
- 涵蓋 4 個交易日（民國年日期）、944 種作物；欄位：上價/中價/下價/平均價/交易量(kg)
- 實測範例：115.09.18 台北二香蕉 平均 29.8 元/公斤、量 11,047 公斤
- 批發價非零售價；當日資料邊交易邊更新
- 用 utf-8-sig 解 BOM；作物名要精確（944 種），查不到先列相近名

完整步驟請看 [SKILL.md](../../taiwan-produce/SKILL.md)。
