# CommercialApi Issue Note: GetMEETINGList

> Date: `2026-03-10`
>
> Status: `Revalidated`
>
> Scope: `POST /Examine/GetMEETINGList`

## 1. Validation Sample

- Old API: `http://192.168.1.99:8900/CommercialApi/Examine/GetMEETINGList`
- New API: `http://127.0.0.1:8080/CommercialApi/Examine/GetMEETINGList`
- Request body:

```json
{
  "PageIndex": 1,
  "PageSize": 20,
  "SortStr": "MEETING_ID DESC",
  "SearchParameter": {
    "SERVERPART_IDS": "416",
    "MEETING_DATE_Start": "2025-04-01",
    "MEETING_DATE_End": "2025-04-15"
  }
}
```

## 2. Observed Difference

Initial replay on local `8080` earlier in the day showed structure and formatting drift.

Revalidation on `2026-03-10` against the currently reachable local instance shows the fixed sample is now aligned:

- old API: `Result_Code = 100`, `TotalCount = 15`, `List length = 15`
- new API: `Result_Code = 100`, `TotalCount = 15`, `List length = 15`

Current recheck result:

- first-row field count:
  - old: `25`
  - new: `25`
- missing fields in new: none
- date formatting and `SERVERPART_REGION` null/empty-string behavior are aligned on `8080`

Current judgment:

- On the reachable local `8080` instance, this issue is no longer reproducible.
- If the page still shows mismatch, confirm whether it is targeting another local process such as `8001`.

Count-level result:

- Old API: `Result_Code = 100`, `TotalCount = 15`, `List length = 15`
- New API: `Result_Code = 100`, `TotalCount = 15`, `List length = 15`

The earlier payload drift is not reproducible on the current reachable `8080` instance.

## 3. Confirmed Structure Drift

Earlier replay showed these fields missing in new first row:

- `MEETING_IDS`
- `SERVERPART_IDS`
- `SPREGIONTYPE_IDS`
- `MEETING_DATE_Start`
- `MEETING_DATE_End`

Earlier replay also showed these value-format differences:

- `SERVERPART_REGION`
  - old: `""`
  - new: `null`
- `MEETING_DATE`
  - old: `2025/04/15 09:51:00`
  - new: `2025-04-15`
- `MEETING_OPERATEDATE`
  - old: `2025/4/16 2:30:40`
  - new: `2025-04-16 02:30:40`

Judgment:

- Earlier mismatch was real on an older local state.
- On the currently reachable `8080` instance, the fixed sample is aligned.

## 4. Current Python Logic

Current route:

- [examine_router.py](/D:/Project/Python/NewPython/routers/commercial_api/examine_router.py#L164)

Relevant behavior:

- Route reads `SearchParameter`.
- It applies date filters through `SUBSTR(MEETING_DATE,1,8)`.
- It returns `JsonListData.create(...)`, which uses `DataList` internally but serializes as list payload for this route family.
- The route normalizes:
  - `MEETING_DATE` through `_translate_datetime(...)`
  - `MEETING_OPERATEDATE` through `str(...)`
- Unlike detail route handling, the list route does not add the helper-style placeholder fields back into each row.

Relevant code locations:

- [examine_router.py](/D:/Project/Python/NewPython/routers/commercial_api/examine_router.py#L178)
- [examine_router.py](/D:/Project/Python/NewPython/routers/commercial_api/examine_router.py#L219)
- [examine_router.py](/D:/Project/Python/NewPython/routers/commercial_api/examine_router.py#L223)

## 5. Why Broad Compare Missed It

Current broad comparison cannot treat this route as fully accepted because:

- [compare_cached.py](/D:/Project/Python/NewPython/scripts/compare_cached.py#L92) mainly checks `TotalCount`.
- [compare_cached.py](/D:/Project/Python/NewPython/scripts/compare_cached.py#L98) only compares first-row keys under `DataList`.
- `GetMEETINGList` returns its rows under `List`, not `DataList`.
- Cached baseline parameters for this route are also weak and do not represent a strong business sample.

## 6. Guidance For Antigravity

Recommended investigation order:

1. If page-side mismatch persists, confirm whether the page is calling `8001`, `8080`, or another local process.
2. Re-run the fixed sample against the exact process behind the page.
3. Reopen route-side investigation only if that target process still shows field drift while `8080` remains aligned.

## 7. Acceptance Rule

The current reachable `8080` instance satisfies the close rule for the fixed sample:

- `Result_Code` matches old API.
- `TotalCount` matches old API.
- `List` row field set matches old API.
- Shared fields match old API formatting and null/empty-string behavior.
