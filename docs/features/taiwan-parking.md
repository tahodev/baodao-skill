# taiwan-parking

台北市停車場即時剩餘車位。免金鑰，停管處 TCMSV 公開 JSON。

- 即時剩位：https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json（2026-09-19 實測 200、約 474KB、1,177 場、近即時 UPDATETIME）
- 靜態場站：https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_alldesc.json（約 2.8MB、1,773 場：場名、行政區、地址、費率、總格數、TWD97 坐標）
- 兩表以 id 組合；`-9` = 無該車種資料（實測 87 場），不是停滿
- 部分場含充電樁狀態（待機中/充電中）；tw97x/y 是 TWD97 投影坐標非經緯度
- 僅台北市停車場；路邊停車格無公開即時資料

完整步驟請看 [SKILL.md](../../taiwan-parking/SKILL.md)。
