# CommercialApi Parallel Task F Acceptance Rules

> Task ID: `T6`
>
> Date: `2026-03-09`
>
> Scope: `CommercialApi` validation rules only
>
> Rule: documentation and alignment only, no code changes in this task

## 1. Goal

Lock one validation standard for all parallel threads so that:

- the same route is judged by the same acceptance rule
- time-sensitive output does not become a false blocker
- stale script cases do not stay in daily closeout
- old API environment failures are separated from Python route defects

## 2. Confirmed Inputs

The rules below are based on confirmed repository facts only:

- `scripts/compare_revenue_bigdata.py` already treats `/BigData/GetRevenueTrendChart` as a time-sensitive `TotalCount` route
- `scripts/test_results/compare_revenue_bigdata.json` records one ignored note for `POST /BigData/GetRevenueTrendChart`
- `scripts/test_results/compare_cached.json` shows the current stable `CommercialApi` baseline for broad route comparison
- `docs/commercial_api_parallel_task_board.md` already records that stale script cases and time-sensitive false positives were identified before closeout
- `docs/commercial_api_ai_context.md` already records the confirmed parameter alias rule, BaseInfo GET field rule, and time-sensitive `TotalCount` rule

## 3. Acceptance Checklist

Use this checklist in every thread before calling a route `PASS`, `DIFF`, `BLOCKER`, or `SKIP`.

### 3.1 Baseline readiness

- Confirm the route exists in the current Python router list.
- Confirm the comparison sample came from the current baseline cache or a newly verified real sample.
- Confirm the request method matches the old route method.
- Confirm the sample is tagged as GET, POST, or AES/POST correctly.

### 3.2 Request validation

- Confirm parameter names follow the old route contract and accepted alias behavior.
- Do not classify a route as a code bug only because of casing differences before checking the alias rule.
- For POST/AES routes, confirm the compared payload is the decrypted real payload shape, not a guessed body.
- If the sample is stale, undocumented, or no longer reproducible, mark it `SKIP` and remove it from acceptance runs.

### 3.3 Response validation

- Compare `Result_Code` first.
- Compare `Result_Data` top-level structure next.
- Compare `TotalCount` only when the route is not in the approved time-sensitive list.
- Compare first-page list shape and key fields only after `Result_Code` is aligned.
- Treat old and new both returning the same stable business code as acceptable even if the code is `101`, `200`, or `999`.

### 3.4 Root-cause classification

- `Code`: old API returns stable output, Python route does not.
- `Data`: route logic is aligned, but sample depends on missing or unsynced DM data.
- `Rule/Script`: the mismatch comes from stale samples, outdated comparison rules, or time-sensitive outputs.
- `TBD`: use only when the evidence is not yet enough to separate code from data.

### 3.5 Closeout gate

Call a thread output complete only when:

- the route result is classified as `PASS`, `DIFF`, `BLOCKER`, or `SKIP`
- the issue type is assigned
- the reason is written as a confirmed fact, not a guess
- blocker routes have a next step
- noisy cases are excluded from the blocker list

## 4. Noisy-Case List

These cases must not be promoted to route-level code blockers unless new evidence shows otherwise.

| Case | Current Handling | Why |
|------|------|------|
| Time-sensitive `TotalCount` on `/BigData/GetRevenueTrendChart` | Ignore `TotalCount` diff during acceptance | Both old C# and Python depend on the current half-hour window |
| Old API timeout in broad comparison | Mark `SKIP`, do not blame Python route | Old side cannot provide a stable comparison result |
| Old API `HTTP404` in broad comparison | Mark `SKIP`, do not blame Python route | Old route baseline is unavailable for direct parity check |
| New API `HTTP422` paired with old `HTTP404` on stale script cases | Mark `SKIP`, remove the case from daily acceptance | The sample itself is no longer a valid parity case |
| Historical script cases that were already removed from active runs | Keep out of blocker count | They create repeated noise without producing a current reproducible defect |

## 5. Approved Time-Sensitive API List

Only the following route is currently approved as time-sensitive by confirmed evidence:

| Route | Sensitive Field | Accepted Rule | Evidence |
|------|------|------|------|
| `POST /BigData/GetRevenueTrendChart` | `Result_Data.TotalCount` | ignore `TotalCount` diff, still compare `Result_Code` and structure | `scripts/compare_revenue_bigdata.py`, `scripts/test_results/compare_revenue_bigdata.json`, `docs/commercial_api_ai_context.md` |

If another route appears time-sensitive later, it must stay `TBD` until T6 or T8 writes a confirmed update.

## 6. Unified Judgment Matrix

| Old API | Python API | Judgment | Notes |
|------|------|------|------|
| stable response | same `Result_Code`, same structure, same non-sensitive counts | `PASS` | normal acceptance pass |
| stable response | same `Result_Code`, diff only on approved time-sensitive field | `PASS` | add note, do not open blocker |
| stable response | different `Result_Code` or structural gap | `DIFF` or `BLOCKER` | classify as code or data after verification |
| timeout / 404 / unavailable | any | `SKIP` | old side is not a valid parity baseline |
| stale sample / invalid script case | any | `SKIP` | remove from active comparison set |

## 7. Thread Usage Rule

All parallel threads should reuse this rule set as follows:

- `T1`, `T2`, `T3`, `T4`, `T5` use this checklist before opening or closing findings
- `T7` may capture only the rules in this document that are already confirmed
- `T8` uses this document as the single acceptance-rule source during daily closeout

## 8. Final T6 Output

T6 is considered complete for `2026-03-09` because all required deliverables now exist in one place:

- acceptance checklist: this document section 3
- noisy-case list: this document section 4
- time-sensitive API list: this document section 5
