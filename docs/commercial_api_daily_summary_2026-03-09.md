# Daily Summary 2026-03-09

> Scope: `CommercialApi`
>
> Source of truth date: `2026-03-09`

## New Issues

- Count: `3`
- Notes:
  - confirmed code issue: `GET /Revenue/GetShopINCAnalysis`
  - confirmed data risk: `T_GOODSSALABLE` is missing in DM for direct validation support
  - confirmed data risk: `T_MEETING` remains an isolated sync-risk area on the list side

## Confirmed Root Causes

- Code:
  - `/Revenue/GetShopINCAnalysis` is not aligned with old C# `HolidayHelper.GetShopINCAnalysis`
  - current Python route uses a simplified daily revenue query instead of the old holiday-window logic
- Data:
  - baseline holiday sample `2026-02-13` with `ServerpartId=416` is reproducibly empty in DM for holiday revenue rows
  - `T_GOODSSALABLE` cannot yet support direct DM-side parity validation
  - `T_MEETING` still needs data-sync separation before route blame is finalized
- Script/Rule:
  - `/BigData/GetRevenueTrendChart` `TotalCount` is time-sensitive and must not be treated as a fixed blocker signal
  - stale script cases and old-side unavailable cases must be handled as `SKIP`

## Closed Today

- Count: `3`
- Notes:
  - `T4` Contract validation prep completed
  - `T6` acceptance rules completed
  - `T7` AI context and pitfalls sync completed

## Current Blockers

- Item: `/Revenue/GetShopINCAnalysis`
- Scope: Revenue route logic alignment
- Owner: `T1`

- Item: holiday revenue data basis and related sync-risk review
- Scope: `T_HOLIDAYREVENUE`, `T_HOLIDAY`, `T_GOODSSALABLE`
- Owner: `T2`

- Item: `T_MEETING` sync-risk and `GetEvaluateResList` first-pass separation
- Scope: Examine data/code split
- Owner: `T5`

## Next Day P0

- Item: finish implementation-ready remediation note for `/Revenue/GetShopINCAnalysis`
- Expected output: old/new flow diff plus rewrite checklist

- Item: verify holiday revenue sample basis on Oracle or old-side evidence
- Expected output: clear judgment on expected zero-data vs sync gap

- Item: run first-pass Examine validation with prepared samples
- Expected output: `T_MEETING` data note and separate `GetEvaluateResList` route note

- Item: start BaseInfo POST/AES replay in the documented acceptance order
- Expected output: first-pass pass/diff status for remaining `BaseInfo` routes
