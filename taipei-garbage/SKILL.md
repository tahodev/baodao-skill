---
name: taipei-garbage
description: 查台北市各里的垃圾車停靠點、路線與抵達、離開時間。免登入,臺北市資料大平臺公開 CSV。
license: MIT
metadata:
  category: city
  locale: zh-TW
---

# taipei-garbage

從臺北市資料大平臺(data.taipei)的「臺北市垃圾車點位路線資訊」資料集下載 CSV,查各里的垃圾車停靠點與抵達時間。免登入、免 API 金鑰。

## 基本流程

1. 下載路線 CSV
2. 依行政區、里別或地址篩選
3. 用現在時間找出「下一班車」

### 1. 下載

```bash
curl -sLm 30 'https://data.taipei/api/dataset/6bb3304b-4f46-4bb0-8cd1-60c66dcd1cae/resource/a6e90031-7ec4-4089-afb5-361a4efe7202/download' -o /tmp/tpe_garbage.csv
```

2026-09-09 實測:HTTP 200、`text/csv`、約 550KB、UTF-8(有 BOM)。這是計畫停靠時間的靜態路線資料,不是即時 GPS;每次使用重新下載即可。

**下載連結的 resource id 可能更換。** 若 404,打開資料集頁 https://data.taipei/dataset/detail?id=6bb3304b-4f46-4bb0-8cd1-60c66dcd1cae ,在頁面原始碼找 `/api/dataset/<資料集id>/resource/<新的resource id>/download` 形式的連結替換。

### 2. 欄位

```
行政區,里別,分隊,局編,車號,路線,車次,抵達時間,離開時間,地點,經度,緯度
```

- `抵達時間` / `離開時間` 是 `HHMM` 字串(例如 `1630` = 16:30)。
- 一個里可能有多個停靠點、多個車次。

### 3. 查詢範例

```bash
# 去掉 BOM 後,查某個里的所有停靠點
sed '1s/^\xef\xbb\xbf//' /tmp/tpe_garbage.csv > /tmp/g.csv
awk -F',' '$2=="天壽里" {print $10, "抵達", $8, "離開", $9, "(" $6 " " $7 ")"}' /tmp/g.csv

# 找出大安區今天 18:00 之後還會到的點(時間是 HHMM 字串,可直接比字串)
awk -F',' '$1=="大安區" && $8>="1800" {print $2, $10, "抵達", $8}' /tmp/g.csv | sort -t' ' -k3
```

「下一班車」的做法:把現在時間(Asia/Taipei)轉成 `HHMM`,篩出同里且 `抵達時間` 大於現在的列,取最早的一班,回報地點、抵達時間、路線與車次。

回報時說明這是計畫時間,實際抵達會受路況影響;停收日、國定假日與颱風天的異動以臺北市政府環境保護局公告為準。

## 錯誤與失敗時的處理

- **HTTP 404**:resource id 已更換。依上面的步驟回資料集頁重新解析下載連結;解析不到就如實告知資料集頁結構改變,請使用者到 data.taipei 手動下載。
- **下載到 HTML 而不是 CSV**(例如錯誤頁):視為失敗,重試 1~2 次,仍失敗就告知來源異常。
- **BOM / 編碼**:檔案開頭有 UTF-8 BOM,解析前先去掉(上面的 `sed` 範例),否則第一欄欄名比對會失敗。
- **查不到某個里**:確認里名寫法(「里」結尾、繁體),再用行政區擴大範圍列出可選的里,讓使用者挑;不要猜最近似的一筆直接回報。
- **非台北市**:此技能只涵蓋台北市。其他縣市請回報尚未支援,或查閱該縣市開放資料平台。

## English summary

Looks up Taipei City garbage-truck collection stops and scheduled arrival/departure times per neighborhood from the Taipei open-data CSV (no login, no API key). Times are `HHMM` planned stops, not live GPS. The download URL's resource id can rotate - on 404, re-resolve it from the dataset page HTML. Strip the UTF-8 BOM before parsing, and always say that collection holidays and typhoon-day changes follow the official DEP announcements.
