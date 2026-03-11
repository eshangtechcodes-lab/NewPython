# CommercialApi T5 Examine Prep

> Date: `2026-03-09`
>
> Task ID: `T5`
>
> Scope: `CommercialApi / Examine`
>
> Rule: investigation and documentation only, no code changes

## 1. Confirmed Facts

- `Examine` currently has 15 routes in Python and the old C# controller exposes the same 15 routes.
- Latest cached comparison shows `14/15` routes `PASS`; only `POST /Examine/GetMEETINGList` is not closed because the old API timed out during the latest run.
- Live Oracle/DM verification points to a data-side count gap on `T_MEETING`, not a route logic gap:
  - Oracle `HIGHWAY_STORAGE.T_MEETING`: `70994`
  - DM `T_MEETING`: `70993`
  - gap: `1`
- Real DM samples are available and reusable:
  - `ServerpartId=416`
  - `EXAMINEId=4076`
  - `MEETINGId=71953`
  - `PATROLId=781609`
- `GET /Examine/GetMEETINGDetail` has been rechecked with `MEETINGId=71953` and returns `Result_Code=100`.
- `POST /Examine/GetEvaluateResList` is not ready for first-pass acceptance:
  - old C# calls `EvaluateHelper.GetEvaluateResList`
  - current Python route still logs `TODO` and returns an empty success payload after AES decrypt
  - this is a separate code/TBD item, not part of the `T_MEETING` data-sync issue

## 2. Route Inventory

| Route | Method | Old C# entry | Main dependency tables | Current prep status | Notes |
|------|------|------|------|------|------|
| `/Examine/GetEXAMINEList` | POST | `GetEXAMINEList -> EXAMINEHelper.GetEXAMINEList` | `T_EXAMINE` | Ready | Real sample body prepared |
| `/Examine/GetEXAMINEDetail` | GET | `GetEXAMINEDetail -> EXAMINEHelper.GetEXAMINEDetail` | `T_EXAMINE` | Ready | Use `EXAMINEId=4076` |
| `/Examine/GetMEETINGList` | POST | `GetMEETINGList -> MEETINGHelper.GetMEETINGList` | `T_MEETING` | Data-risk isolated | Count diff is limited to table sync |
| `/Examine/GetMEETINGDetail` | GET | `GetMEETINGDetail -> MEETINGHelper.GetMEETINGDetail` | `T_MEETING` | Ready | Use `MEETINGId=71953`; detail path is not blocked |
| `/Examine/GetPATROLList` | POST | `GetPATROLList -> PATROLHelper.GetPATROLList` | `T_PATROL` | Ready | Real sample body prepared |
| `/Examine/GetPATROLDetail` | GET | `GetPATROLDetail -> PATROLHelper.GetPATROLDetail` | `T_PATROL` | Ready | Use `PATROLId=781609` |
| `/Examine/WeChat_GetExamineList` | GET | `WeChat_GetExamineList -> EXAMINEHelper.WeChat_GetExamineList` | `T_EXAMINE` | Ready | Use `Serverpart_ID=416` and date window |
| `/Examine/WeChat_GetExamineDetail` | GET | `WeChat_GetExamineDetail -> EXAMINEHelper.GetExamineDetail` | `T_EXAMINEDETAIL` | Ready | Use `ExamineId=4076` |
| `/Examine/WeChat_GetPatrolList` | GET | `WeChat_GetPatrolList -> PATROLHelper.WeChat_GetPatrolList` | `T_PATROL` | Ready | Requires explicit date range |
| `/Examine/WeChat_GetMeetingList` | GET | `WeChat_GetMeetingList -> MEETINGHelper.WeChat_GetMeetingList` | `T_MEETING` | Data-risk isolated | Same table risk as meeting list |
| `/Examine/GetPatrolAnalysis` | GET | `GetPatrolAnalysis -> PATROLHelper.GetPatrolAnalysis` | `T_PATROLDAILY`, `T_SERVERPART` | Ready | Analysis sample prepared |
| `/Examine/GetExamineAnalysis` | GET | `GetExamineAnalysis -> EXAMINEHelper.GetExamineAnalysis` | `T_EXAMINE`, `T_SERVERPART` | Ready | Month-based sample prepared |
| `/Examine/GetExamineResultList` | GET | `GetExamineResultList -> EXAMINEHelper.GetExamineResultList` | `T_EXAMINE`, `T_EXAMINEDETAIL`, `T_SERVERPART` | Ready | Left join detail path |
| `/Examine/GetPatrolResultList` | GET | `GetPatrolResultList -> PATROLHelper.GetPatrolResultList` | `T_PATROL`, `T_PATROLDETAIL`, `T_SERVERPART` | Ready | Detail-state filter is in route SQL |
| `/Examine/GetEvaluateResList` | POST | `GetEvaluateResList -> EvaluateHelper.GetEvaluateResList` | `Evaluate*` helper dependencies, AES payload | Blocked | Python route is placeholder and needs separate validation |

## 3. T_MEETING Risk Isolation

### 3.1 Affected scope

- Direct table users:
  - `POST /Examine/GetMEETINGList`
  - `GET /Examine/GetMEETINGDetail`
  - `GET /Examine/WeChat_GetMeetingList`
- Not affected by `T_MEETING`:
  - `EXAMINE*` list/detail/analysis/result routes
  - `PATROL*` list/detail/analysis/result routes
  - `GetEvaluateResList`

### 3.2 Evidence

- Live database verification:
  - Oracle `HIGHWAY_STORAGE.T_MEETING=70994`
  - DM `T_MEETING=70993`
  - only `1` row difference
- Scope recheck on both sides:
  - `ServerpartId=416` count is `793` in Oracle and `793` in DM
  - `MEETINGId=71953` exists in Oracle and DM
- Latest cached compare:
  - `POST /Examine/GetMEETINGList`: old `TIMEOUT`, new `C=100,T=70993`, `SKIP`
- Earlier compare record kept in repo:
  - `POST /Examine/GetMEETINGList`: old `C=100,T=70994`, new `C=100,T=70993`, `DIFF`
- Live route check in current workspace:
  - `GET /Examine/GetMEETINGDetail?MEETINGId=71953` returns `100`

### 3.3 Conclusion

- `T_MEETING` risk is currently isolated to list-side data completeness and count consistency.
- It is not enough evidence to blame Python route logic.
- `GetMEETINGDetail` can proceed with real IDs even before table re-sync.
- `WeChat_GetMeetingList` should be treated as the same data-risk family as `GetMEETINGList`.

## 4. List/Detail Linkage Note

- `EXAMINE` thread:
  - use `POST /Examine/GetEXAMINEList` to obtain `EXAMINEId`
  - verify the same entity through `GET /Examine/GetEXAMINEDetail`
  - then verify `GET /Examine/WeChat_GetExamineDetail` on the same `ExamineId`
- `MEETING` thread:
  - list count check belongs to data verification
  - detail validation should use a known-good ID such as `71953`, not wait for count alignment
- `PATROL` thread:
  - use `POST /Examine/GetPATROLList` to obtain `PATROLId`
  - verify `GET /Examine/GetPATROLDetail`
  - then verify result aggregation through `GET /Examine/GetPatrolResultList`

## 5. Real Sample Plan

### 5.1 Core IDs

- `ServerpartId=416`
- `EXAMINEId=4076`
- `MEETINGId=71953`
- `PATROLId=781609`

### 5.2 POST list samples

`POST /Examine/GetEXAMINEList`

```json
{
  "PageIndex": 1,
  "PageSize": 20,
  "SortStr": "EXAMINE_ID DESC",
  "SearchParameter": {
    "SERVERPART_IDS": "416",
    "EXAMINE_DATE_Start": "2025-02-01",
    "EXAMINE_DATE_End": "2025-02-28"
  }
}
```

`POST /Examine/GetMEETINGList`

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

`POST /Examine/GetPATROLList`

```json
{
  "PageIndex": 1,
  "PageSize": 20,
  "SortStr": "PATROL_ID DESC",
  "SearchParameter": {
    "SERVERPART_IDS": "416",
    "PATROL_DATE_Start": "2025-04-01",
    "PATROL_DATE_End": "2025-04-15"
  }
}
```

### 5.3 GET detail and WeChat samples

- `/Examine/GetEXAMINEDetail?EXAMINEId=4076`
- `/Examine/GetMEETINGDetail?MEETINGId=71953`
- `/Examine/GetPATROLDetail?PATROLId=781609`
- `/Examine/WeChat_GetExamineList?Serverpart_ID=416&SearchStartDate=2025-02-01&SearchEndDate=2025-02-28`
- `/Examine/WeChat_GetExamineDetail?ExamineId=4076`
- `/Examine/WeChat_GetPatrolList?Serverpart_ID=416&SearchStartDate=2025-04-01&SearchEndDate=2025-04-15`
- `/Examine/WeChat_GetMeetingList?Serverpart_ID=416&SearchStartDate=2025-04-01&SearchEndDate=2025-04-15`

### 5.4 Analysis/result samples

- `/Examine/GetPatrolAnalysis?provinceCode=340000&ServerpartId=416&StartDate=2026-01-15&EndDate=2026-02-13`
- `/Examine/GetExamineAnalysis?DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416`
- `/Examine/GetExamineResultList?DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416`
- `/Examine/GetPatrolResultList?provinceCode=340000&ServerpartId=416&StartDate=2026-01-15&EndDate=2026-02-13`

### 5.5 AES sample for `GetEvaluateResList`

Plain payload:

```json
{
  "ProvinceCode": "340000",
  "RoleType": 1,
  "StatisticsMonth": "202502",
  "ServerpartId": "416"
}
```

Encrypted request body:

```json
{
  "value": "HGNvR1g5B0VGGjJORmEEEgs1DgIxfgMtA3orJ2I8LRFoOCwWSjMXREgWMD9gbxweLDgXBGAJTHJbMitONn9rSCl5dUcbUlgIbxtgcyU/Xk9seW5SYB9McjxmbxouDhgq"
}
```

Current note:

- Python can decrypt this payload.
- Current Python route still returns `Result_Code=100` with empty `List`, because query logic is marked `TODO`.
- This route must stay out of the "ready for first-pass validation" list until helper logic is implemented or old/new real-output comparison is completed.

## 6. Acceptance Order

1. `GetEXAMINEList` + `GetEXAMINEDetail` + `WeChat_GetExamineDetail`
2. `GetPATROLList` + `GetPATROLDetail` + `GetPatrolResultList`
3. `GetMEETINGDetail` + `WeChat_GetMeetingList`
4. `GetMEETINGList` count check after `T_MEETING` sync review
5. `GetPatrolAnalysis` + `GetExamineAnalysis` + `GetExamineResultList`
6. `GetEvaluateResList` only after AES sample and helper logic are both confirmed

## 7. Output Summary For T5

- `Examine` route inventory: complete
- `T_MEETING` risk note: complete
- list/detail linkage note: complete
- real sample plan: complete
- open blockers:
  - `T_MEETING` data sync gap of `1`
  - `GetEvaluateResList` implementation/sample validation gap
