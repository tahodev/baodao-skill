# taiwan-oil-price

台灣中油每週牌價。免金鑰，主路徑是官方 open data JSON。

- 主路徑：https://vipmbr.cpc.com.tw/opendata/sixtypeoillistprice （data.gov.tw 資料集 166537；2026-09-20 實測 200、51 列、免 UA）——篩 `型別名稱=="汽柴油零售"` 得 92/95/98、酒精汽油、超柴
- 生效日期：週日中午公告次週牌價、週一零時生效；`牌價生效日期`（民國 yyyMMdd）未到之前本週沿用舊價
- 實測範例：1150921 生效 92=31.2、95=32.7、98=34.7、超柴=29.9 元/公升
- 歷史近 7 週：https://www.cpc.com.tw/historyprice.aspx?n=2890（需瀏覽器 UA）；更早需分頁 POST（範圍外）
- 台塑牌價不同源；同一 JSON 還有燃料油/天然氣/液化石油氣（單位各異）

完整步驟請看 [SKILL.md](../../taiwan-oil-price/SKILL.md)。
