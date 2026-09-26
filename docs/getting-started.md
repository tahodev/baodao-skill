# 入門指南（getting started）

25 個技能怎麼挑？依目的分成六組。只有 3 個技能需要免費申請的 API 金鑰（`cwa-weather`、`taiwan-uv` 用 CWA 授權碼;`taiwan-aqi` 用 MOENV 金鑰）,其他全部免金鑰免登入。

## 天氣與災害

- `cwa-weather`：各縣市 36 小時與鄉鎮官方預報（需 CWA 金鑰）
- `taiwan-weather`：免金鑰天氣（Open-Meteo）+ 颱風/地震/海嘯警報（NCDR CAP）
- `taiwan-uv`：紫外線指數（需 CWA 金鑰）
- `taiwan-aqi`：每小時空氣品質（需 MOENV 金鑰）
- `taiwan-suspension`：停班停課公告

## 通勤出門

- `youbike-realtime`：全台 14 個服務區 YouBike 即時可借/可還
- `taiwan-parking`：台北市停車場即時剩位
- `taiwan-garbage`：台北/新北/台中垃圾車路線與停靠時間
- `taiwan-toilet`：全國公廁位置與評鑑

## 生活與錢

- `invoice-winning-numbers`：統一發票對獎（每期開獎日主動對）
- `taiwan-oil-price`：中油每週油價
- `taiwan-postage`：郵資查詢
- `taiwan-stock`：台股每日收盤快照
- `taiwan-power`：台電電力供需與供電燈號
- `taiwan-produce`：蔬果批發行情

## 行政與文件

- `postal-address`：郵遞區號與地址英譯
- `taiwan-id-check`：統編與身分證字號檢核（純本地）
- `taiwan-holidays`：國定假日、連假、補班日
- `taiwan-lunar-cal`：農曆與節氣換算（純本地）

## 查資料

- `taiwan-hospital`：健保特約院所 37,133 家
- `taiwan-library`：全台 5,207 館圖書館名錄
- `taiwan-museum`：全台 144 間博物館
- `taiwan-schools`：國中/國小名錄與班級學生數
- `taiwan-real-estate`：實價登錄季度批次
- `taiwan-water`：停水公告

各技能的詳細流程與錯誤處理,以根目錄 `<技能名>/SKILL.md` 為正本;摘要見 [features/](features/)。安裝方式見 [install.md](install.md)。
