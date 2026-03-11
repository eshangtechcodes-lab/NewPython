# CommercialApi Parallel Task Templates

> Purpose: standardize parallel investigation, daily reporting, and issue collection for `CommercialApi`.

## 1. Parallel Task Assignment

| Task ID | Owner | Workstream | Scope | Input | Output | Done Criteria | Priority |
|------|------|------|------|------|------|------|------|
| T1 |  | Revenue true issue line | `/Revenue/GetShopINCAnalysis` | old C# controller/helper, current Python route, baseline params | issue note, old/new logic diff, remediation proposal | root cause and impact are confirmed | P0 |
| T2 |  | Revenue data risk line | holiday revenue related tables | `T_HOLIDAYREVENUE`, `T_HOLIDAY`, `T_GOODSSALABLE`, baseline dates | data verification note, sync-risk list | code issues and data issues are separated | P0 |
| T3 |  | BaseInfo closeout line | remaining `BaseInfo` APIs | router list, current scripts, inventory | acceptance prep note, POST/AES sample list | all remaining APIs have sample plan and risk mark | P1 |
| T4 |  | Contract preheat line | all `Contract` APIs | router list, old C# APIs, dependency tables | acceptance inventory, sample plan, dependency summary | `Contract` is ready for first-pass validation | P1 |
| T5 |  | Examine preheat line | all `Examine` APIs | router list, old C# APIs, dependency tables | acceptance inventory, sample plan, data-risk summary | `T_MEETING` risk is isolated and range is clear | P1 |
| T6 |  | Acceptance rules line | common validation rules | compare scripts, baseline cache, current findings | validation rules, noisy-case list, time-sensitive API list | all threads use the same acceptance criteria | P0 |
| T7 |  | AI context line | confirmed findings only | worklogs, issue notes, stable conclusions | AI context updates, pitfalls updates | reusable conclusions are captured for AI reuse | P1 |
| T8 |  | Daily closeout line | all workstreams | outputs from T1-T7 | daily summary, blocker list, next-day priority list | only one daily version of truth exists | P0 |

## 2. Daily Status Board

| Task ID | Owner | Module/API | Status | Today Goal | Findings | Root Cause | Type | Blocking | Next Step | Due Date |
|------|------|------|------|------|------|------|------|------|------|------|
| T1 |  | `/Revenue/GetShopINCAnalysis` | Not Started |  |  |  | Code/Data/TBD | Yes/No |  |  |
| T2 |  | holiday revenue data check | Not Started |  |  |  | Data/TBD | Yes/No |  |  |
| T3 |  | remaining `BaseInfo` APIs | Not Started |  |  |  | Code/Script/TBD | Yes/No |  |  |
| T4 |  | `Contract` prep | Not Started |  |  |  | Code/Data/TBD | Yes/No |  |  |
| T5 |  | `Examine` prep | Not Started |  |  |  | Code/Data/TBD | Yes/No |  |  |
| T6 |  | validation rules | Not Started |  |  |  | Rule/Script | Yes/No |  |  |
| T7 |  | AI knowledge capture | Not Started |  |  |  | Document | No |  |  |
| T8 |  | daily closeout | Not Started |  |  |  | Management | Yes/No |  |  |

## 3. Issue Note Template

```md
## Issue: <module/api>

- Task ID:
- Owner:
- API:
- Method:
- Repro params:
- Old API result:
- Python result:
- Observed diff:
- Old C# logic summary:
- Python current logic summary:
- Dependency tables:
- Initial root cause:
- Final root cause:
- Issue type: Code / Data / Script / Rule / TBD
- Blocking: Yes / No
- Remediation proposal:
- Verification method:
- Status: New / In Progress / Confirmed / Closed
- Date:
```

## 4. Daily Summary Template

```md
# Daily Summary YYYY-MM-DD

## New Issues
- Count:
- Notes:

## Confirmed Root Causes
- Code:
- Data:
- Script/Rule:

## Closed Today
- Count:
- Notes:

## Current Blockers
- Item:
- Scope:
- Owner:

## Next Day P0
- Item:
- Expected output:
```

## 5. AI Context Update Template

```md
## Stable Conclusion

- Title:
- Scope:
- Conclusion:
- Reason:
- Validation:
- Date:
- Status: Verified
```

## 6. Rules For Parallel Execution

1. Parallel threads may investigate, reproduce, compare old/new logic, verify data, and write notes.
2. Parallel threads must not change common middleware, shared helpers, or global validation scripts.
3. Every thread records only confirmed facts. Assumptions must be marked `TBD`.
4. Final priority, final root-cause classification, and final remediation order are closed by T8 only.
5. AI context accepts only stable conclusions, never temporary guesses.

## 7. Suggested Daily Rhythm

1. Morning: T1-T7 run in parallel.
2. Afternoon: T8 performs unified closeout.
3. End of day outputs:
   - updated status board
   - new issue notes
   - daily summary
   - AI context updates for verified conclusions only
