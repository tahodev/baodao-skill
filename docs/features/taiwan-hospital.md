# taiwan-hospital

健保特約醫療院所名錄。免金鑰，健保署開放資料 API。

- 基本資料：https://info.nhi.gov.tw/api/iode0010/v1/rest/datastore/A21030000I-D2100G-001（2026-09-20 實測 200、total 37,133 筆；API 單次 limit 封頂 1,000，全量用 offset 分頁）
- 欄位：HOSP_NAME/ADDR/TEL/類型/簽約日；姊妹集：D21006 固定服務時段、D2100C 診療科別
- 目錄：https://info.nhi.gov.tw/api/iode0010/v1/rest/dataset?limit=100
- 名錄非即時資訊：看診進度、掛號、臨時休診查不到
- 地址含全形字元與「（代表）」，勿自行刪改；新開/歇業可能有落差

完整步驟請看 [SKILL.md](../../taiwan-hospital/SKILL.md)。
