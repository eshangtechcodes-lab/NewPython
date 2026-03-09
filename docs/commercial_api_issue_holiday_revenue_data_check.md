# CommercialApi Issue Note: Holiday Revenue Data Check

> Task ID: `T2`
>
> Date: `2026-03-09`
>
> Status: `In Progress`
>
> Scope: `CommercialApi` holiday revenue data line only

## 1. Baseline Sample

- Related route: `/Revenue/GetShopINCAnalysis`
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

## 2. Confirmed DM Findings

### Table availability

- `T_HOLIDAYREVENUE` exists in DM.
- `T_HOLIDAY` exists in DM.
- `T_GOODSSALABLE` is currently missing in DM.

### Sample data check

- `T_HOLIDAYREVENUE` has existing data for `SERVERPART_ID = 416` in DM:
  - total rows: `27593`
- The baseline sample date itself has no holiday revenue rows:
  - `SERVERPART_ID = 416`
  - `STATISTICS_DATE = 20260213`
  - row count: `0`

This confirms the sample is a date-window data gap, not a full-table absence.

### Holiday calendar check

- `T_HOLIDAY` contains Spring Festival entries for `2025` and `2026`.
- For both years, DM currently stores two spring-festival ranges under the same holiday description:
  - `HOLIDAY_TYPE = 2000`
  - `HOLIDAY_TYPE = 9000`
- Old C# `CommonHelper.GetHoliday(...)` filters by `HOLIDAY_DESC` only, then takes `MIN(HOLIDAY_DATE)` and `MAX(HOLIDAY_DATE)`.
- Observed DM ranges:
  - `2025` Spring Festival: `2025-01-14` to `2025-02-22`
  - `2026` Spring Festival: `2026-02-02` to `2026-03-13`

Implication:

- Old logic uses the full min/max range for the `2026` Spring Festival entry, not a single `HOLIDAY_TYPE`.
- Any Python rewrite or data replay that filters only one spring-festival subtype may produce the wrong holiday window.

## 3. Old Logic Impact On Data Judgment

Old C# `HolidayHelper.GetShopINCAnalysis(...)` confirms:

1. `calcType = 1` queries `T_HOLIDAYREVENUE` only for the current sample date.
2. It returns `null` when both current and compare holiday revenue result sets are empty.
3. The controller converts that `null` into `Result_Code = 101`.

For the baseline sample:

- current holiday revenue rows on `20260213`: `0`
- compare holiday revenue rows are effectively the same sample basis here because baseline `compareYear = 2026`

Judgment:

- The old API's `101` result is reproducible from data alone for this sample.
- But the current Python mismatch is still not a pure data issue, because the Python route does not read the same dataset or follow the same empty-data rule.

## 4. Code/Data Separation

- Data-side confirmed fact:
  - the baseline sample date has no matching holiday revenue rows in DM
- Code-side confirmed fact:
  - current Python `/Revenue/GetShopINCAnalysis` reads `T_REVENUEDAILY`, not `T_HOLIDAYREVENUE`
  - current Python returns `100` as long as simplified summary data exists

Final separation:

- `T2` conclusion: the empty-data condition is real and reproducible in DM
- `T1` conclusion: the current blocker remains a code-alignment issue because Python ignores the old holiday-data path

## 5. Sync-Risk List

- `T_GOODSSALABLE`
  - missing in DM
  - separate sync-risk item
  - should not be mixed into the `GetShopINCAnalysis` route-level root cause
- `T_HOLIDAY`
  - exists in DM
  - dual spring-festival subtype records (`2000` and `9000`) make holiday-window derivation sensitive to old helper behavior
- `T_HOLIDAYREVENUE`
  - table exists and has historical data
  - baseline sample date for `ServerpartId=416` has zero rows
  - this supports the old API empty-data branch

## 6. Oracle Comparison Need List

Oracle-side verification is still required for final data closure:

1. Verify whether Oracle `T_HOLIDAYREVENUE` also has `0` rows for:
   - `SERVERPART_ID = 416`
   - `STATISTICS_DATE = 20260213`
2. Verify whether Oracle `T_HOLIDAY` has the same spring-festival date ranges and subtype mix.
3. Verify whether the old API baseline really ran with `compareYear = 2026` and no hidden normalization.
4. Verify whether `T_GOODSSALABLE` exists in Oracle and whether DM is missing a required sync.

Current blocker for direct Oracle verification in this environment:

- local Oracle access is not available through the current Python path
- observed errors:
  - `DPI-1047` Oracle client architecture mismatch
  - `DPY-3010` Oracle thin-mode server version unsupported

## 7. Current Conclusion

- DM evidence is sufficient to prove the sample date has no holiday revenue rows.
- DM evidence is not sufficient to blame the full blocker on data only.
- The production mismatch must stay split:
  - data condition: confirmed
  - route mismatch: confirmed code issue
- T2 should remain open until Oracle-side sample verification is completed.
