# CommercialApi Issue Note: GetServerpartINCAnalysis Holiday Mapping

> Date: `2026-03-10`
>
> Status: `Confirmed`
>
> Scope: `GET /Revenue/GetServerpartINCAnalysis`

## 1. Fixed Reproduction Sample

- Old API:
  - `http://192.168.1.99:8900/CommercialApi/Revenue/GetServerpartINCAnalysis`
- New API:
  - `http://127.0.0.1:8080/CommercialApi/Revenue/GetServerpartINCAnalysis`

Primary sample:

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

## 2. Observed Difference

Primary sample result:

- old API:
  - `Result_Code = 100`
  - `TotalCount = 133`
  - `List length = 133`
- new API:
  - `Result_Code = 101`

Single-service-area replay also reproduces the same issue:

- sample:
  - `calcType=2`
  - `pushProvinceCode=340000`
  - `curYear=2025`
  - `compareYear=2024`
  - `HolidayType=7`
  - `StatisticsDate=2025-10-09`
  - `CurStartDate=2025-09-30`
  - `ServerpartId=416`
- old API: `100`
- new API: `101`

This proves the issue is not caused by the large multi-ID input itself.

## 3. Root Cause

Current route:

- [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L3945)

Confirmed mismatch:

- `GetServerpartINCAnalysis` uses:

```python
{1: "元旦", 2: "春运", 3: "清明", 4: "五一", 5: "端午", 6: "暑期", 7: "中秋", 8: "国庆"}
```

- other aligned holiday routes use:

```python
{1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}
```

Relevant references:

- broken mapping:
  - [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L3968)
- aligned mappings:
  - [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L3581)
  - [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L4289)
  - [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L5825)
  - [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L6099)

Operational impact:

- this route builds `HOLIDAY_DESC` with the wrong holiday names
- query against `T_HOLIDAY` then returns no matching rows
- route exits early with `Result_Code = 101`

## 4. Confirmed Impact Range

Using fixed single-service-area replay on local new API:

- `HolidayType = 1`:
  - `Result_Code = 100`
- `HolidayType = 3`:
  - `Result_Code = 101`
- `HolidayType = 4`:
  - `Result_Code = 101`
- `HolidayType = 5`:
  - `Result_Code = 101`
- `HolidayType = 7`:
  - `Result_Code = 101`
- `HolidayType = 8`:
  - `Result_Code = 101`

Judgment:

- the issue is not limited to Mid-Autumn
- it affects all holiday types whose old description includes `节` or uses `劳动节` rather than `五一`

## 5. Similar-Issue Scan Result

Current scan result in this repository:

- the simplified broken holiday-name mapping is only confirmed in `GetServerpartINCAnalysis`
- aligned holiday routes already use the correct mapping or shared helper logic
- local replay confirms:
  - [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L4263) `GetShopINCAnalysis` returns `100` for the same `HolidayType=7` and `HolidayType=8` samples

## 6. Guidance For Antigravity

Recommended action:

1. Replace the local holiday-name mapping in `GetServerpartINCAnalysis` with the same mapping already used by aligned holiday routes.
2. Prefer reusing shared holiday helper logic instead of maintaining a separate hard-coded map here.
3. Re-run at least these samples after the change:
   - `HolidayType=4`, `ServerpartId=416`
   - `HolidayType=7`, `ServerpartId=416`
   - the full multi-ID `HolidayType=7` sample from this note

## 7. Acceptance Rule

This issue can be closed only when:

- the fixed `HolidayType=7` multi-ID sample returns `Result_Code = 100`
- `TotalCount` matches old API
- `List` structure and business content align with old API
- `HolidayType=3/4/5/7/8` no longer fail early because of holiday description mismatch

