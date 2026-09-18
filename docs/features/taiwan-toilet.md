# taiwan-toilet

環境部全國公廁建檔資料（位置、管理單位、評鑑等級、尿布台）。免註冊。

- 來源：data.gov.tw 資料集 30794 公布的 resource API key，打 data.moenv.gov.tw /api/v2/fac_p_07（2026-09-19 實測 200、每頁 1,000、offset 翻頁正常）
- 欄位：county 代碼、village、name、address、administration、lat/lng、grade（特優級…）、type、diaper
- 實測：中油鶯歌加油站-男廁（新北鶯歌，特優級）
- 金鑰失效時回資料集頁重取，不用註冊；建檔資料非即時開放狀態
- 部分缺經緯度；算距離先過濾

完整步驟請看 [SKILL.md](../../taiwan-toilet/SKILL.md)。
