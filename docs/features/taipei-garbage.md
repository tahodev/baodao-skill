# taipei-garbage

查台北市各里的垃圾車停靠點與抵達、離開時間。免登入,臺北市資料大平臺公開 CSV。

- 資料集:臺北市垃圾車點位路線資訊 https://data.taipei/dataset/detail?id=6bb3304b-4f46-4bb0-8cd1-60c66dcd1cae
- 欄位:行政區、里別、路線、車次、抵達時間(HHMM)、離開時間、地點、經度、緯度
- 時間是計畫停靠時間;停收日與異動以臺北市環保局公告為準
- 下載連結的 resource id 可能更換,404 時回資料集頁重新解析

完整查詢範例(找出「下一班車」)與錯誤處理請看 [SKILL.md](../../taipei-garbage/SKILL.md)。
