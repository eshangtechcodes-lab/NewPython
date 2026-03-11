# CommercialApi Regression Report

> Date: `2026-03-10`
>
> Scope: second regression pass with broad scripts plus fixed-sample replay
>
> New API used for validation: `http://127.0.0.1:8080/CommercialApi`
>
> Old API used for validation: `http://192.168.1.99:8900/CommercialApi`

## 1. High-Level Result

This round confirms the project is in late-stage closeout, but not yet ready for final acceptance.

Broad coverage:

- `compare_cached.py`
  - `PASS = 116/123`
  - `DIFF = 6`
  - `SKIP = 1`
- `compare_revenue_bigdata.py`
  - `PASS = 70/74`
  - `DIFF = 4`
- `compare_baseinfo.py`
  - current checked BaseInfo subset: pass

Key takeaway:

- Most routes are now code-aligned at the result-code layer.
- Remaining work should no longer be handled as one flat issue list.
- The remaining gaps split into 3 families:
  - environment / dependency issues
  - database runtime resource issues
  - deterministic route logic issues

## 2. Fixed-Sample Revalidation

### Revalidated as aligned on current `8080`

Using exact business samples, the following routes are currently aligned on the reachable `8080` instance:

- `GET /Revenue/GetSalableCommodity`
- `GET /Revenue/GetServerpartINCAnalysis`
- `GET /Revenue/GetMonthINCAnalysis`
- `GET /Revenue/GetShopSABFIList`
- `GET /BigData/GetBayonetOwnerAHTreeList`

Important note:

- Some of these routes showed earlier drift during previous replays.
- Current exact-sample replay shows they can produce old-compatible output.
- This means they should not be reopened blindly unless the same fixed sample fails again on the exact deployed process being investigated.

### Currently unstable under repeated replay

The following fixed-sample replays can fail with the same DM runtime error:

- `POST /Examine/GetMEETINGList`
- `GET /Revenue/GetServerpartINCAnalysis`
- `GET /Revenue/GetShopSABFIList`

Observed error pattern:

- `Result_Code = 999`
- `Result_Desc` contains:
  - `CODE:-544`
  - `超出全局排序空间`

Judgment:

- This is not a clean business-logic mismatch.
- It is a database runtime/resource issue that can mask true route behavior.
- Do not mix this failure mode into normal payload-alignment debugging.

## 3. Current Broad-Script DIFF List

### Environment / dependency issues

These should be solved before further route-logic debugging:

- `GET /Revenue/GetSPBayonetList`
  - current new-side error:
    - `No module named 'dateutil'`
- `GET /Revenue/GetProvinceAvgBayonetAnalysis`
  - current new-side error:
    - `No module named 'dateutil'`
- `POST /BigData/GetRevenueTrendChart`
  - current new-side error:
    - Redis connection refused at `127.0.0.1:6379`

Operational rule:

- These are not business-field alignment tasks yet.
- They are dependency/runtime prerequisites.

### Deterministic code issue

- `GET /BigData/GetProvinceVehicleTreeList`
  - current new-side error:
    - `CODE:-2007`
    - SQL syntax error near `SERVERPART_ID`

Operational rule:

- This is a real code-side SQL issue and should be treated as a true blocker.

### Broad-script-only diff, not yet a confirmed code blocker

- `POST /Examine/GetMEETINGList`
- `POST /Examine/GetPATROLList`

Current judgment:

- broad script shows `DIFF` because old-side response in that sample is `999`
- this is not enough to classify them as current Python blockers
- they need fixed business samples before any reopening

## 4. Efficiency Logic For Antigravity

Antigravity should stop treating all remaining items as one queue.

Use this order instead:

1. Solve prerequisites first
   - install/fix `dateutil`
   - fix Redis availability for `GetRevenueTrendChart`
2. Solve deterministic SQL blocker
   - `GetProvinceVehicleTreeList`
3. Only then revisit large-query business routes
   - and when revisiting them, use fixed samples instead of broad-script baseline only
4. Treat `CODE:-544` as a separate runtime class
   - if this appears, the task is database/runtime tuning or query-shape reduction first
   - do not keep comparing payload details on top of an unstable query execution path

## 5. Recommended Parallel Split

### Thread A: dependency prerequisites

- `GetSPBayonetList`
- `GetProvinceAvgBayonetAnalysis`
- `GetRevenueTrendChart`

Goal:

- clear `dateutil` and Redis blockers first

### Thread B: SQL blocker

- `GetProvinceVehicleTreeList`

Goal:

- fix deterministic SQL syntax issue

### Thread C: large-query runtime stability

- `GetMEETINGList`
- `GetServerpartINCAnalysis`
- `GetShopSABFIList`

Goal:

- determine whether `CODE:-544` must be handled through query optimization or DM runtime settings

### Thread D: final precise replay

After A/B/C are stable:

- rerun exact business samples
- rerun broad compare
- only then update acceptance state

## 6. Current Closeout Status

Current status should be described as:

- broad regression mostly green
- final acceptance not complete
- remaining blockers are concentrated
- current biggest efficiency gain is to separate dependency/runtime problems from route-alignment problems

