---
name: taiwan-lunar-cal
description: 農曆與節氣換算——國曆轉農曆（含閏月）、二十四節氣日期推算、生肖。今天農曆幾號、什麼時候過年、中秋節是哪天、節氣、生肖的問題適用。純本地計算，零網路、免金鑰。精確到分的節氣時刻（天文觀測值）不適用——公式給日期。
license: MIT
metadata:
  category: calendar
  locale: zh-TW
---

# taiwan-lunar-cal

純本地計算：國曆轉農曆（1900-2100，含閏月）、二十四節氣日期（1901-2100 通用公式）、生肖。零網路。

## 農曆換算

用公開的 1900-2100 農曆資料表（每年一個 17-bit 整數：12 個月大小月 + 閏月位置與大小）。完整實作：

```python
import datetime

LUNAR_INFO = [
0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
0x06ca0,0x0b550,0x15355,0x04da0,0x0a5b0,0x14573,0x052b0,0x0a9a8,0x0e950,0x06aa0,
0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b6a0,0x195a6,
0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x05ac0,0x0ab60,0x096d5,0x092e0,
0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
0x05aa0,0x076a3,0x096d0,0x04afb,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0,
0x14b63,0x09370,0x049f8,0x04970,0x064b0,0x168a6,0x0ea50,0x06b20,0x1a6c4,0x0aae0,
0x0a2e0,0x0d2e3,0x0c960,0x0d557,0x0d4a0,0x0da50,0x05d55,0x056a0,0x0a6d0,0x055d4,
0x052d0,0x0a9b8,0x0a950,0x0b4a0,0x0b6a6,0x0ad50,0x055a0,0x0aba4,0x0a5b0,0x052b0,
0x0b273,0x06930,0x07337,0x06aa0,0x0ad50,0x14b55,0x04b60,0x0a570,0x054e4,0x0d160,
0x0e968,0x0d520,0x0daa0,0x16aa6,0x056d0,0x04ae0,0x0a9d4,0x0a2d0,0x0d150,0x0f252,
0x0d520]

def leap_month(y): return LUNAR_INFO[y-1900] & 0xf
def leap_days(y): return (30 if LUNAR_INFO[y-1900] & 0x10000 else 29) if leap_month(y) else 0
def month_days(y, m): return 30 if (LUNAR_INFO[y-1900] & (0x10000 >> m)) else 29
def year_days(y):
    return 348 + sum(1 for m in range(1, 13) if LUNAR_INFO[y-1900] & (0x10000 >> m)) + leap_days(y)

def to_lunar(d):
    """國曆 date -> (農曆年, 月, 日, 是否閏月);範圍 1900-01-31 ~ 2100-12-31"""
    offset = (d - datetime.date(1900, 1, 31)).days   # 1900-01-31 = 農曆1900年正月初一
    if offset < 0 or d.year > 2100: return None
    y = 1900
    while offset >= year_days(y):
        offset -= year_days(y); y += 1
    leap = leap_month(y)
    for m in range(1, 13):
        md = month_days(y, m)
        if offset < md: return (y, m, offset + 1, False)
        offset -= md
        if leap == m:
            ld = leap_days(y)
            if offset < ld: return (y, m, offset + 1, True)
            offset -= ld
    return None

ZODIAC = '鼠牛虎兔龍蛇馬羊猴雞狗豬'
def zodiac(lunar_year): return ZODIAC[(lunar_year - 1900) % 12]
```

2026-09-19 實測驗證（9 個錨點全過）：2026-02-17 = 丙午年正月初一（115 春節）、2026-09-25 = 八月十五（115 中秋）、2025-10-06 = 乙巳年八月十五（114 中秋，該年有閏六月）、2025-07-25 = 閏六月初一、2026-02-16 = 114 年十二月廿九（除夕，該月小月）。

## 節氣日期

1901-2100 通用公式：`日 = int(Y * 0.2422 + C) - int((Y-1) // 4)`，Y = 年 % 100。

```python
C21 = {'立春':3.87,'雨水':18.73,'驚蟄':5.63,'春分':20.646,'清明':4.81,'穀雨':20.1,
'立夏':5.52,'小滿':21.04,'芒種':5.678,'夏至':21.37,'小暑':7.108,'大暑':22.83,
'立秋':7.5,'處暑':23.13,'白露':7.646,'秋分':23.042,'寒露':8.318,'霜降':23.438,
'立冬':7.438,'小雪':22.36,'大雪':7.18,'冬至':21.94,'小寒':6.11,'大寒':20.84}
def solar_term_day(year, term):
    Y = year % 100
    return int(Y * 0.2422 + C21[term]) - int((Y - 1) // 4)
```

2026-09-19 實測驗證：2026 清明 = 4/5、立春 = 2/4、夏至 = 6/21、冬至 = 12/22、2025 清明 = 4/4，全部正確。

## 錯誤與失敗時的處理

- **節氣公式有 ±1 天的罕見例外**（少數年份/節氣的常數例外，如 2026 小寒例外 +1）。一般問答可用；涉及祭典、正式文件的精確日期時，建議對照中央氣象署或官方日曆並如實說明這是公式推算。
- **範圍外日期**：農曆表只涵蓋 1900-2100；範圍外回 None，不要硬算。
- **閏月表達**：回報時講「閏六月」而非「六月之二」；生肖以農曆年（非國曆元旦）起算。
- **農曆年的歸屬**：國曆 1-2 月常落在前一個農曆年（如 2026-02-16 仍是乙巳年），生肖判斷要用換算後的農曆年。

## English summary

ROC lunar calendar and solar terms, pure local computation (zero network). Lunar conversion uses the public 1900-2100 packed table (12 big/small months + leap month bits per year); implementation included, verified 2026-09-19 against 9 anchors (2026 Lunar New Year 2026-02-17, Mid-Autumn 2026-09-25, the 2025 leap-6th-month, New Year's Eve 2026-02-16 = 12/29 small month). Solar terms use the 1901-2100 common formula day = int(Y*0.2422 + C) - int((Y-1)//4) with the 21st-century constants (verified: Qingming 2026 = Apr 5, Winter Solstice 2026 = Dec 22). Caveats: rare ±1-day formula exceptions for specific year/term combos - for ceremonial or legal dates, cross-check the CWA or official calendar and say the value is computed; zodiac follows the lunar year, not Jan 1.
