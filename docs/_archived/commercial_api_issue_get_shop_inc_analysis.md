# CommercialApi Issue Note: Revenue/GetShopINCAnalysis

> Task ID: `T1`
>
> Date: `2026-03-09`
>
> Status: `Confirmed`
>
> Scope: `CommercialApi` only

## 1. API

- Route: `/Revenue/GetShopINCAnalysis`
- Method: `GET`
- Baseline params:

```json
{
  "calcType": "1",
  "pushProvinceCode": "340000",
  "curYear": "2026",
  "compareYear": "2026",
  "HolidayType": "2",
  "ServerpartId": "416",
  "StatisticsDate": "2026-02-13",
  "CurStartDate": "2026-01-15"
}
```

## 2. Observed Diff

- Old API result:
  - `Result_Code = 101`
  - `Result_Data = null`
- Current Python result:
  - `Result_Code = 100`
  - returns `TotalCount = 24`
  - returns grouped revenue rows by `SHOPTRADE` and `BUSINESS_TYPE`

## 3. Old C# Logic

Old entry:

- [RevenueController.cs](D:/CSharp/Project/000_通用版本/000_通用版本/030_EShangApi/CommercialApi/Controllers/RevenueController.cs)
- Controller action directly calls `HolidayHelper.GetShopINCAnalysis(...)`

Old helper:

- [HolidayHelper.cs](D:/CSharp/Project/000_通用版本/000_通用版本/030_EShangApi/CommercialApi/GeneralMethod/Revenue/HolidayHelper.cs)

Confirmed behavior:

1. Resolve holiday date range with `HolidayType`, `curYear`, `compareYear`, `StatisticsDate`, `CurStartDate`.
2. Query holiday revenue from `T_HOLIDAYREVENUE` by `SERVERPARTSHOP_ID`.
3. Query traffic from `T_SECTIONFLOW` or `T_BAYONETDAILY_AH` depending on mode/date rules.
4. Group service-area shops by `SHOPTRADE + SHOPSHORTNAME` from `T_SERVERPARTSHOP`.
5. Join brand info and current transaction info.
6. If both current-year and compare-year holiday revenue datasets are empty, return `null`.
7. Controller converts `null` into `Result_Code = 101`.

## 4. Current Python Logic

Current route:

- [revenue_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/revenue_router.py#L4214)

Confirmed behavior:

1. Route signature does not match old API input shape.
2. Current Python route uses:
   - `serverpartId`
   - `StatisticsStartDate`
   - `StatisticsEndDate`
3. It does not implement the old holiday-specific logic for:
   - `HolidayType`
   - `StatisticsDate`
   - `CurStartDate`
4. It queries `T_REVENUEDAILY` directly.
5. It groups by `SHOPTRADE` and `BUSINESS_TYPE`.
6. It returns success as long as that simplified query has rows.

## 5. Root Cause

This is a confirmed code-alignment issue, not a simple parameter bug.

Root cause details:

1. The Python route is not a faithful migration of the old C# helper.
2. The old route is holiday-window based and shop-level.
3. The Python route is daily revenue summary based and trade/business-type level.
4. The old route returns `101` when holiday revenue datasets are empty.
5. The Python route ignores that rule and returns `100` because unrelated daily revenue data exists.

## 6. Data Findings

DM validation for the baseline sample already confirmed:

- current holiday revenue window rows: `0`
- compare holiday revenue window rows: `0`

This matches the old controller behavior that would return `101` when both holiday revenue datasets are empty.

Additional data risk found during the same round:

- `T_GOODSSALABLE` is currently missing in DM for direct query validation

## 7. Impact

- This issue is a true blocker for `Revenue` content acceptance.
- It should remain `P0`.
- It is not safe to close using parameter remapping only.

## 8. Remediation Proposal

Recommended remediation order:

1. Rebuild Python route to match old C# parameter contract:
   - `calcType`
   - `pushProvinceCode`
   - `curYear`
   - `compareYear`
   - `HolidayType`
   - `ServerpartId`
   - `StatisticsDate`
   - `CurStartDate`
   - `SortStr`
2. Re-implement the old holiday date-range logic.
3. Re-query holiday revenue from `T_HOLIDAYREVENUE`.
4. Rebuild shop grouping from `T_SERVERPARTSHOP`.
5. Reproduce old empty-data rule:
   - if both current-year and compare-year holiday revenue sets are empty, return `101`
6. Re-attach current transaction info only after the main holiday result is aligned.

## 9. Acceptance Criteria

This issue can be closed only when all of the following are true:

1. Baseline sample returns `101` in Python.
2. Route input shape matches old API.
3. Output structure matches old `HolidayIncreaseModel`.
4. Empty-data behavior matches old controller exactly.
5. No fallback to unrelated `T_REVENUEDAILY` summary logic remains.
