# CommercialApi Antigravity Open Actions

> Date: `2026-03-10`
>
> Scope: active interface mismatches that still need code-side investigation or alignment

## 1. Priority Order

1. `GET /Revenue/GetServerpartINCAnalysis`
2. `GET /Revenue/GetMonthINCAnalysis`
3. `GET /Revenue/GetShopSABFIList`

## 2. Action: GetServerpartINCAnalysis

Reference:

- [commercial_api_issue_get_serverpart_inc_analysis_2026-03-10.md](/D:/Project/Python/NewPython/docs/commercial_api_issue_get_serverpart_inc_analysis_2026-03-10.md)

Environment:

- old API: `http://192.168.1.99:8900/CommercialApi`
- new API: `http://127.0.0.1:8080/CommercialApi`

Primary replay sample:

```text
calcType=2
pushProvinceCode=340000
curYear=2025
compareYear=2024
HolidayType=7
StatisticsDate=2025-10-09
CurStartDate=2025-09-30
ServerpartId=416,417,419,418,420,435,433,421,436,495,498,510,594,422,466,489,501,511,600,706,707,716,811,520,492,525,524,518,503,505,508,499,522,516,473,490,517,474,475,658,659,656,694,521,519,514,967,515,963,513,1552,652,1553,500,362,502,363,369,480,494,496,507,509,364,365,367,368,372,476,477,478,479,366,370,371,373,710,504,646,756,708,803,805,1560,1566,377,378,380,430,444,445,376,379,381,382,383,429,440,442,446,448,426,428,439,450,451,714,819,941,951,955,1508,1509,1542,1543,432,443,460,471,431,606,465,456,462,463,464,468,470,592,384,385,434,453,943,1562,650,680,897,841,1492,1550,1538
businessRegion=1
```

Current old/new result:

- old: `Result_Code=100`, `TotalCount=133`
- new: `Result_Code=101`

Confirmed cause direction:

- local route uses a simplified holiday-name map
- this mismatches the actual `T_HOLIDAY.HOLIDAY_DESC` naming used by aligned routes
- affected holiday types already confirmed: `3`, `4`, `5`, `7`, `8`

Investigation order:

1. Replace local route holiday-name mapping with the same naming used by aligned routes or shared helper logic.
2. Re-run:
   - single-ID `HolidayType=4`
   - single-ID `HolidayType=7`
   - multi-ID `HolidayType=7`
3. After result code is restored, compare `TotalCount`, row structure, and key business fields against old API.

Close rule:

- fixed multi-ID sample must reproduce old API success result and aligned payload
## 3. Action: GetMonthINCAnalysis

Environment:

- old API: `http://192.168.1.99:8900/CommercialApi`
- new API: confirm the actual local process port before testing

Replay sample:

```text
statisticsType=1&sorterType=1&StatisticsStartMonth=202602&StatisticsEndMonth=202602&pushProvinceCode=340000&ServerpartId=416,417,419,418,420,435,433,421,436,495,498,510,594,422,466,489,501,511,600,706,707,716,811,520,492,525,524,518,503,505,508,499,522,516,473,490,517,474,475,658,659,656,694,521,519,514,967,515,963,513,1552,652,1553,500,362,502,363,369,480,494,496,507,509,364,365,367,368,372,476,477,478,479,366,370,371,373,710,504,646,756,708,803,805,1560,1566,377,378,380,430,444,445,376,379,381,382,383,429,440,442,446,448,426,428,439,450,451,714,819,941,951,955,1508,1509,1542,1543,432,443,460,471,431,606,465,456,462,463,464,468,470,592,384,385,434,453,943,1562,650,680,897,841,1492,1550,1538&BusinessTradeType=&calcYOY=true&calcQOQ=false&calcBayonet=true
```

Current old/new result on reachable `8080` instance:

- old: root children = `6` region nodes
- new: root children = `137` service-area nodes
- old root `ServerpartId = null`
- new root `ServerpartId = 0`

Close rule:

- root and first-level tree semantics must align with old API

## 4. Action: GetShopSABFIList

Environment:

- old API: `http://192.168.1.99:8900/CommercialApi`
- new API: confirm the actual local process port before testing

Replay sample:

```text
pushProvinceCode=340000&StatisticsMonth=202602&ServerpartId=416,417,419,418,420,435,433,421,436,495,498,510,594,422,466,489,501,511,600,706,707,716,811,520,492,525,524,518,503,505,508,499,522,516,473,490,517,474,475,658,659,656,694,521,519,514,967,515,963,513,1552,652,1553,500,362,502,363,369,480,494,496,507,509,364,365,367,368,372,476,477,478,479,366,370,371,373,710,504,646,756,708,803,805,1560,1566,377,378,380,430,444,445,376,379,381,382,383,429,440,442,446,448,426,428,439,450,451,714,819,941,951,955,1508,1509,1542,1543,432,443,460,471,431,606,465,456,462,463,464,468,470,592,384,385,434,453,943,1562,650,680,897,841,1492,1550,1538&BusinessTradeType=&BusinessTrade=
```

Current old/new result on reachable `8080` instance:

- old: first region child = `72 / 皖中管理中心`
- new: first region child = `45 / 皖东管理中心`

Close rule:

- tree grouping and ordering must align with old API
## 5. Validation Note

Do not rely only on broad compare output when closing either item.

Reference:

- [commercial_api_validation_script_gaps_2026-03-10.md](/D:/Project/Python/NewPython/docs/commercial_api_validation_script_gaps_2026-03-10.md)
