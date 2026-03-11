# CommercialApi Parallel Task Board

> Baseline date: `2026-03-09`
>
> Scope: `CommercialApi` only
>
> Rule: investigation and documentation only, no code changes in this workstream

## 1. Current Status Board

| Task ID | Owner | Module/API | Status | Today Goal | Findings | Root Cause | Type | Blocking | Next Step | Due Date |
|------|------|------|------|------|------|------|------|------|------|------|
| T1 | Revenue lead | `/Revenue/GetShopINCAnalysis` | In Progress | confirm old/new logic gap and remediation scope | old API returns `101`, current Python returns `100`; old C# uses `HolidayHelper.GetShopINCAnalysis`; current Python path was implemented as simplified query | likely code gap, not just parameter issue | Code | Yes | finish old C# logic拆解 and output专项整改方案 | 2026-03-10 |
| T2 | Data lead | holiday revenue data check | In Progress | separate data-only reproducibility from route logic gap | DM confirms `T_HOLIDAYREVENUE` and `T_HOLIDAY` exist, `T_GOODSSALABLE` is missing, and baseline sample `2026-02-13` + `ServerpartId=416` has `0` holiday revenue rows while the table still has historical data | sample-date empty data is reproducible in DM, but final blocker still needs separation from the `T1` code gap; Oracle-side sample basis is still pending | Data | Yes | verify the same sample in Oracle or via old API evidence, then decide whether this is expected zero-data or a sync gap in `T_HOLIDAYREVENUE`/related tables | 2026-03-10 |
| T3 | BaseInfo lead | remaining `BaseInfo` APIs | Completed | close sample plan, dependency summary, acceptance order, and replay materials for all remaining routes | all 7 remaining `BaseInfo` routes now have sample plan and risk mark; fixed materials now include AES decrypted payloads and `GetServerInfoTree` header sample `ServerpartCodes: 341003` | blocker was documentation/script coverage gap rather than shared middleware; `GetBrandAnalysis` remains the clearest code-risk route | Script/Code | No | use `commercial_api_t3_baseinfo_prep.md` as the single input for first-pass execution | 2026-03-10 |
| T4 | Contract lead | `Contract` prep | Completed | finish prep and run first-pass spot validation | prep is complete; first-pass confirms `GetContractAnalysis` content gap, `GetMerchantAccountDetail` placeholder blocker, and one low-risk extra `MerchantId=0` row in `GetMerchantAccountSplit` | inventory gap is closed; remaining issues are route-level code gaps plus one likely filtering difference | Document/Prep | No | hand off confirmed issues `commercial_api_issue_contract_get_contract_analysis.md` and `commercial_api_issue_contract_get_merchant_account_detail.md`; keep `GetMerchantAccountSplit` as non-blocking follow-up | 2026-03-09 |
| T5 | Examine lead | `Examine` prep | In Progress | isolate `T_MEETING` data risk and prepare real acceptance samples | `T_MEETING` is isolated to list-side data sync; real samples are ready for `EXAMINE/MEETING/PATROL`; `GetEvaluateResList` is still a placeholder route pending AES-based validation | data gap on `T_MEETING`; separate code/TBD risk on `GetEvaluateResList` | Data/Code/TBD | Yes | use prepared samples for first-pass validation; escalate `GetEvaluateResList` separately from `T_MEETING` | 2026-03-10 |
| T6 | QA rules lead | validation rules | Completed | lock acceptance criteria for all threads | final acceptance checklist, noisy-case list, and time-sensitive API list were published in `docs/commercial_api_parallel_task_f_acceptance_rules.md` | rules gap was causing noisy comparison output | Rule/Script | No | T8 should use the published rule set as the single closeout baseline | 2026-03-09 |
| T7 | AI context lead | AI knowledge capture | Completed | capture verified conclusions only | parameter alias issue, BaseInfo GET field behavior, time-sensitive `TotalCount` rule, and the new `SKIP` / stale-script handling rules are now captured in AI context and pitfalls docs | N/A | Document | No | T8 should reuse the updated AI context plus pitfalls rules during closeout | 2026-03-09 |
| T8 | Closeout lead | daily closeout | Completed | produce single version of truth for today | daily summary, blocker list, and next-day priority order were published; today closes with one confirmed code blocker and a small set of isolated data risks | N/A | Management | No | execute next-day P0 order from `docs/commercial_api_daily_summary_2026-03-09.md` | 2026-03-09 |

## 2. Priority Order

1. `T1` `/Revenue/GetShopINCAnalysis`
2. `T2` holiday revenue data verification
3. `T6` acceptance rules closeout
4. `T8` daily unified closeout
5. `T3` `BaseInfo` POST/AES sample prep
6. `T4` `Contract` validation prep
7. `T5` `Examine` validation prep
8. `T7` AI context sync

## 3. Known Facts

### Revenue

- `Revenue + BigData` latest batch result is `PASS=73/74`
- current only confirmed route-level blocker is `/Revenue/GetShopINCAnalysis`
- `GetRevenueReport`, `GetMonthlySPINCAnalysis`, and `GetServerpartINCAnalysis` are no longer open blockers

### BaseInfo

- current dedicated validation is green for:
  - `GetSPRegionList`
  - `GetBusinessTradeList(GET)`
- remaining work is mainly unvalidated POST/AES routes

### Contract

- first-pass spot validation is now available in `commercial_api_contract_validation_prep.md`
- confirmed blockers are `/Contract/GetContractAnalysis` and `/Contract/GetMerchantAccountDetail`
- `/Contract/GetMerchantAccountSplit` is close to aligned, but Python currently returns one extra blank merchant row with `MerchantId=0`

### Data Risks

- `T_GOODSSALABLE` remains a known sync-risk table
- `T_MEETING` remains a known sync-risk table
- holiday revenue samples need explicit DM/Oracle consistency check before code blame is finalized

### Rules

- `/BigData/GetRevenueTrendChart` must be treated as time-sensitive for `TotalCount`
- stale or out-of-scope script cases must be removed from acceptance runs

## 4. Thread Deliverables

### T1 Deliverables

- old C# method flow
- Python current flow
- dependency table list
- route input/output diff
- remediation proposal without code changes

### T2 Deliverables

- DM sample data verification result
- Oracle comparison need list
- table sync-risk list
- judgment on whether the blocker is reproducible from data alone

### T3 Deliverables

- `BaseInfo` POST/AES sample list
- dependency table list
- acceptance order

### T4 Deliverables

- `Contract` route inventory
- sample params
- dependency table list
- high-risk notes

### T5 Deliverables

- `Examine` route inventory
- `T_MEETING` risk note
- list/detail linkage note
- sample params

### T6 Deliverables

- acceptance checklist
- noisy-case list
- time-sensitive API list
- published file: `docs/commercial_api_parallel_task_f_acceptance_rules.md`

### T7 Deliverables

- AI context update entries
- pitfalls update entries
- stable parameter/business-rule notes

### T8 Deliverables

- daily summary
- blocker list
- next-day `P0` order

## 5. Daily Closeout Template For This Board

```md
## Closeout YYYY-MM-DD

- New confirmed code issues:
- New confirmed data issues:
- Closed today:
- Current blockers:
- Next-day P0:
```

## 6. Closeout 2026-03-09

- New confirmed code issues: `1` -> `/Revenue/GetShopINCAnalysis`
- New confirmed data issues: isolated holiday revenue sample-data risk, `T_GOODSSALABLE` DM gap, and `T_MEETING` sync risk remain open
- Closed today: `T4`, `T6`, `T7`
- Current blockers: `T1` route logic alignment, `T2` holiday revenue data verification, `T5` Examine data/code split
- Next-day P0:
  - `/Revenue/GetShopINCAnalysis`
  - holiday revenue Oracle/old-side verification
  - Examine first-pass validation
  - BaseInfo POST/AES replay
