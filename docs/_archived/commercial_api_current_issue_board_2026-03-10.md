# CommercialApi Current Issue Board

> Date: `2026-03-10`
>
> Scope: current working baseline after live replay and targeted validation

## 1. Closed Code Issues

- `GET /Revenue/GetShopINCAnalysis`
- `POST /Examine/GetEvaluateResList`
- `POST /BaseInfo/GetServerpartServiceSummary`

Evidence basis:

- current code state
- targeted live replay
- [verify_service_summary.json](/D:/Project/Python/NewPython/scripts/test_results/verify_service_summary.json)

## 2. Active Interface Issues

### `GET /Revenue/GetServerpartINCAnalysis`

- Status: `Active`
- Problem type: `holiday mapping mismatch`
- Current note:
  - [commercial_api_issue_get_serverpart_inc_analysis_2026-03-10.md](/D:/Project/Python/NewPython/docs/commercial_api_issue_get_serverpart_inc_analysis_2026-03-10.md)

### `GET /Revenue/GetSalableCommodity`

- Status: `Closed on current 8080 instance`
- Current note:
  - [commercial_api_issue_get_salable_commodity.md](/D:/Project/Python/NewPython/docs/commercial_api_issue_get_salable_commodity.md)

### `POST /Examine/GetMEETINGList`

- Status: `Closed on current 8080 instance`
- Current note:
  - [commercial_api_issue_get_meeting_list.md](/D:/Project/Python/NewPython/docs/commercial_api_issue_get_meeting_list.md)

## 3. Background Data Items

- `T_GOODSSALABLE`
  - still needs server-side availability and sync confirmation
- `T_MEETING`
  - historical Oracle/DM count gap still exists as a background data item
  - but it no longer fully explains current route mismatch

## 4. Validation Infrastructure Risks

- broad compare is not final truth for all routes
- cached POST samples are not always strong business samples
- `baseline_collect.py` is still on stale environment settings

Reference:

- [commercial_api_validation_script_gaps_2026-03-10.md](/D:/Project/Python/NewPython/docs/commercial_api_validation_script_gaps_2026-03-10.md)

## 5. Current Execution Priority

1. `GetServerpartINCAnalysis`
2. `GetMonthINCAnalysis`
3. `GetShopSABFIList`
4. validation script cleanup
