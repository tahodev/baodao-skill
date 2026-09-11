---
name: taiwan-holidays
description: 查台灣政府行政機關辦公日曆表——國定假日、連假、補班日。放假嗎、補班嗎、下個連假、春節幾號、國慶連假、人事行政總處日曆的問題適用。免 API 金鑰、免登入。公司行號自訂行事曆、學校行事曆的細節不適用（學校另有規定）。
license: MIT
metadata:
  category: government
  locale: zh-TW
---

# taiwan-holidays

用行政院人事行政總處公布的「政府行政機關辦公日曆表」查台灣的放假日與補班日。不需要 API 金鑰或登入。資料來源：https://www.dgpa.gov.tw/informationlist?uid=30 （每年公布次年日曆）。

## 資料形式（兩種，依年度而不同）

1. **當年度（115 年＝2026 年）：官方 xlsx 月曆**
   https://www.dgpa.gov.tw/uploads/dgpa/files/202511/1d88999f-f893-47dd-8757-ee7df20765a5.xlsx
   2026-09-12 實測：HTTP 200、19,770 bytes、`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`。放假日以**粉紅底色**標示（週六、週日與國定假日的儲存格 fill 為 FFFF99FF，樣式 id 31/34/38；一般上班日底色為無、樣式 9），補班日則是週六欄位中沒有粉紅底色的儲存格。

2. **114 年（2025）及更早：結構化 CSV**（欄位 `西元日期,星期,是否放假,備註`，是否放假 0=上班、2=放假，補班日為 0 且備註「補行上班」）。下載點在資料集頁 https://data.gov.tw/dataset/14718 ，114 年 CSV（2026-09-12 實測 HTTP 200、6,396 bytes）：
   https://www.dgpa.gov.tw/FileConversion?filename=dgpa/files/202407/22f9fcbc-fbb2-4387-8bcf-73b2279666c2.csv&nfix=&name=114.csv

## 查當年度（xlsx，python3 標準庫即可，不需 openpyxl）

```bash
curl -sm 30 -o /tmp/cal.xlsx 'https://www.dgpa.gov.tw/uploads/dgpa/files/202511/1d88999f-f893-47dd-8757-ee7df20765a5.xlsx'
```

```python
import zipfile, re, bisect, xml.etree.ElementTree as ET
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z=zipfile.ZipFile('/tmp/cal.xlsx')
ss=[t.text or '' for t in ET.fromstring(z.read('xl/sharedStrings.xml')).iter(NS+'t')]
sheet=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
def ci_of(ref):
    s=re.match(r'([A-Z]+)',ref).group(1); n=0
    for ch in s: n=n*26+ord(ch)-64
    return n-1
HDR=[3,17,31,45]          # 四個月份橫帶的標題列（1 起始列號；新版檔案若有變動，找含「月」字的列）
RED={'31','34','38'}      # 放假（粉紅底色 fillId=2）儲存格樣式 id；一般上班日是 '9'（無底色）
out=[]
for c in sheet.iter(NS+'c'):
    ref=c.get('r'); ri=int(re.search(r'\d+',ref).group()); ci=ci_of(ref)
    v=c.find(NS+'v')
    if v is None: continue
    val=(ss[int(v.text)] if c.get('t')=='s' else v.text).strip()
    if not re.fullmatch(r'\d{1,2}',val) or ci<1: continue
    block=(ci-1)//7; wd=(ci-1)%7     # 每橫帶 3 個月、每月 7 欄（日一二三四五六）
    if block>2: continue
    band=bisect.bisect_right(HDR,ri)-1
    if not 0<=band<=3: continue
    out.append((band*3+block+1, int(val), wd, c.get('s','0') in RED))
# out: (月, 日, 星期(0=日), 是否放假)
```

2026-09-12 實測：115 年檔案解析出 365 天，星期全部與實際日期吻合；平日放假日共 16 天（1/1、2/16-20 春節連假、2/27、4/3、4/6、5/1、6/19、9/25、9/28、10/9、10/26、12/25）。**月份不能讀標題文字**：十一月、十二月的「十」「一」分在兩個儲存格，直接用 `band*3+block+1` 推算最穩。補班日 = 星期欄是週六/週日但**沒有**粉紅底色的儲存格（115 年：無；若當年有，會出現在清單裡）。

## 查 114 年或更早（CSV）

```bash
curl -sm 30 -o /tmp/cal114.csv 'https://www.dgpa.gov.tw/FileConversion?filename=dgpa/files/202407/22f9fcbc-fbb2-4387-8bcf-73b2279666c2.csv&nfix=&name=114.csv'
awk -F, 'NR>1 && $3==2 {print $1, $2, $4}' /tmp/cal114.csv   # 放假日
awk -F, 'NR>1{sub(/\r$/,"",$4)} $4=="補行上班" {print $1, $2}' /tmp/cal114.csv  # 補班日（檔案是 CRLF，先去掉 \r）
```

CSV 為 UTF-8（含 BOM）、CRLF 換行——比對最後一欄（備註）時先 `sub(/\r$/,"",$4)` 去掉 \r，否則比對不到。`是否放假`：0=上班、2=放假；補班週六是 0 且備註「補行上班」。

## 錯誤與失敗時的處理

- **xlsx 連結 404**：人事總處每年換檔案 GUID。回到列表頁 https://www.dgpa.gov.tw/informationlist?uid=30 找當年度「政府行政機關辦公日曆表」公告，取其 xlsx 附件網址替換；解析邏輯不變，但要重驗 `HDR`（含「月」的列號）與 `RED`（粉紅底色樣式 id）兩個常數——驗法：1 月 1 日必須是有底色（RED 樣式）且星期正確（115 年為星期四；其他年份以該年實際星期為準）。
- **次年 CSV 找不到**：新年度初期 dgpa 可能只放 xlsx/PDF，CSV 後補在資料集 https://data.gov.tw/dataset/14718 ；過渡期請用 xlsx 流程。
- **學校、銀行、股市的休市日不同**：本技能是行政機關日曆；股市休市請用 taiwan-stock 的交易日資料反推，不要混用。
- 重要判斷（請假、排程截止日）請提醒使用者回 https://www.dgpa.gov.tw 確認原文。

## English summary

Looks up Taiwan's official government work calendar (DGPA): national holidays, long weekends, and makeup workdays. Keyless. Current year (ROC 115 = 2026) ships as a red-ink xlsx calendar - download the dgpa.gov.tw xlsx and parse it with the python3-stdlib recipe in this file (365 days verified 2026-09-12; holidays are pink-filled cells (style ids 31/34/38, fill FFFF99FF), month = band*3+block+1). ROC 114 (2025) and earlier ship as structured CSV (西元日期,星期,是否放假,備註; 0=workday, 2=off, makeup Saturdays are 0 + 補行上班) from data.gov.tw dataset 14718. School/bank/stock-market calendars differ - do not mix.
