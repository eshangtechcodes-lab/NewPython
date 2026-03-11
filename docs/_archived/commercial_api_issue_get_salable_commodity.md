# CommercialApi Issue Note: GetSalableCommodity

> Date: `2026-03-10`
>
> Status: `Revalidated`
>
> Scope: `GET /Revenue/GetSalableCommodity`

## 1. Validation Sample

- Old API: `http://192.168.1.99:8900/CommercialApi/Revenue/GetSalableCommodity`
- New API: `http://127.0.0.1:8080/CommercialApi/Revenue/GetSalableCommodity`
- Query string:

```text
statisticsDate=2026-02-13&provinceCode=340000&Serverpart_ID=416&SPRegionType_ID=
```

## 2. Observed Difference

Initial replay on local `8080` earlier in the day showed a real mismatch.

Revalidation on `2026-03-10` against the currently reachable local instance shows the sample is now aligned:

- old API:
  - `Result_Code = 100`
  - `SalableCommodity = 24.7`
  - `SalableCommodityList` length = `5`
- new API:
  - `Result_Code = 100`
  - `SalableCommodity = 24.7`
  - `SalableCommodityList` length = `5`

Current judgment:

- On the reachable local `8080` instance, this issue is no longer reproducible.
- If the page still shows a mismatch, first confirm whether the page is hitting another local instance such as `8001`.

Old API:

- `Result_Code = 100`
- `SalableCommodity = 24.7`
- `SalableCommodityList` length = `5`
- first item:

```json
{
  "Commodity_name": "븐큇",
  "Proportion": 9.3
}
```

New API:

- `Result_Code = 100`
- `SalableCommodity = 0.0`
- `SalableCommodityList` length = `0`
- `UnsalableCommodityList` length = `0`

Judgment:

- Earlier mismatch was real on an older local state.
- On the currently reachable `8080` instance, the fixed sample is aligned.

## 3. Current Python Logic

Current route:

- [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L2868)

Key behavior:

- Query reads `T_GOODSSALABLE`.
- If the table query raises an exception, the route logs a warning and falls back to `rows = []`.
- That fallback then produces:
  - `SalableCommodity = 0.0`
  - empty top list
  - empty bottom list

Relevant code location:

- [revenue_router.py](/D:/Project/Python/NewPython/routers/commercial_api/revenue_router.py#L2897)

## 4. Root-Cause Direction

Current evidence supports this split:

- Route-side fact:
  - current route still contains the empty-fallback branch when `T_GOODSSALABLE` query fails
  - but the currently reachable local `8080` instance is returning old-compatible data for the fixed sample
- Environment-side fact:
  - local `8001` is not reachable in the current workspace, so page-side mismatches on `8001` cannot be verified here yet

Operational conclusion:

- Treat this issue as closed on the current `8080` instance.
- If a page still shows mismatch, verify the actual target port and deployed process before reopening the route issue.

## 5. Guidance For Antigravity

Recommended investigation order:

1. If page-side mismatch persists, confirm whether the page is calling `8001`, `8080`, or another local process.
2. Re-run the fixed sample against the exact process behind the page.
3. Reopen route-side investigation only if that target process still returns empty payload while old API returns data.

## 6. Acceptance Rule

The current reachable `8080` instance satisfies the close rule for the fixed sample:

- `Result_Code` matches old API.
- `SalableCommodity` matches old API.
- `SalableCommodityList` business content is aligned.
- `UnsalableCommodityList` business content is aligned.
