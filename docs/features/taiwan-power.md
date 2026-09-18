# taiwan-power

台電今日系統供需狀況（目前用電、預估尖峰、備轉容量率、供電燈號）。免金鑰。

- 來源：https://service.taipower.com.tw/data/opendata/apply/file/d006020/001.json（2026-09-19 實測 200；**主站 www 會 403，務必走 service 主機**）
- records 4 段：目前用電/使用率、今日預估（含燈號）、昨日實績、即時尖峰
- 實測：115.09.19 03:10 發布，目前用電 2,733.5 萬瓩、預估備轉率 26.21% 綠燈
- 燈號：G 綠 ≥10% / Y 黃 6-10% / O 橘 <6% / R 紅 / B 黑；單位萬瓩（=10 MW）
- success 是字串；publish_time 民國年、real_hr_peak_time 西元並存

完整步驟請看 [SKILL.md](../../taiwan-power/SKILL.md)。
