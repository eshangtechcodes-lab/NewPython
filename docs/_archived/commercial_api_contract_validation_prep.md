# CommercialApi Contract Validation Prep

> Date: `2026-03-09`
>
> Scope: `/Contract/*`
>
> Rule: confirmed facts only; unknown items remain `TBD`

## 1. Readiness

- Route count: `3`
- Method mix: all `GET`
- Latest batch reference: `scripts/test_results/compare_cached.json` shows `Contract 3/3 PASS` on `2026-03-09`
- Prep conclusion: `Contract` is ready for first-pass validation
- Important caveat: code-level pass does not mean content-level readiness; `GetContractAnalysis` and `GetMerchantAccountDetail` still show placeholder risk in current Python code/logs

## 2. Route Inventory

| Route | Method | Current Python status | Sample params for first pass | Notes |
|------|------|------|------|------|
| `/Contract/GetContractAnalysis` | GET | returns a fixed response shape; route log still warns "not fully implemented" | `statisticsDate=2026-02-13` `provinceCode=340000` `Serverpart_ID=416` `SPRegionType_ID=` | use one province + one service-area sample first |
| `/Contract/GetMerchantAccountSplit` | GET | query path exists and latest cached compare is aligned at result-code level | `StatisticsMonth=202602` `StatisticsStartMonth=202602` `calcType=1` `CompactTypes=340001` `BusinessTypes=` `SettlementMods=` `MerchantIds=` `SortStr=` | safest first-pass entry because current Python has real SQL |
| `/Contract/GetMerchantAccountDetail` | GET | still placeholder; current Python directly returns `Result_Code=101` | `MerchantId=-1104` `StatisticsMonth=202602` `StatisticsStartMonth=202602` `calcType=1` `CompactTypes=340001` `BusinessTypes=` `SettlementMods=` `SortStr=` | use a real merchant from `GetMerchantAccountSplit`; `MerchantId=1` is not a strong validation sample |

## 3. Dependency Table List

| Route | Confirmed dependency tables | Source |
|------|------|------|
| `/Contract/GetContractAnalysis` | `T_REGISTERCOMPACT`, `T_REGISTERCOMPACTSUB`, `T_PAYMENTCONFIRM`, `T_RTREGISTERCOMPACT`, `T_SERVERPART` | current router comment + `helper_tables_check.txt` + `table_sync_report.txt` |
| `/Contract/GetMerchantAccountSplit` | `T_MERCHANTSPLIT`, `T_COOPMERCHANTS` | current Python SQL + `table_sync_report.txt` + `workLog/2026-03-04.md` |
| `/Contract/GetMerchantAccountDetail` | `TBD` | current Python route has no real SQL; final old-C# helper dependency list still needs to be recovered |

## 4. High-Risk Notes

- `/Contract/GetContractAnalysis` is not a finished migration yet. Current Python returns hard-coded fields and logs a warning instead of reproducing the old helper flow.
- `/Contract/GetMerchantAccountDetail` is also not finished. Current Python returns `101`, so it cannot be treated as content-validated even if some historical compare runs no longer flag it as a blocker.
- Historical artifacts for `Contract` are stale. `scripts/baseline/GetMerchantAccountSplit.json` and `scripts/baseline/GetMerchantAccountDetail.json` still show older `101` snapshots and should not be used as the single source of truth.
- `GetContractAnalysis` is a cross-table/cross-schema route. Validation must separate "placeholder code" from any future table-sync discussion.
- `GetMerchantAccountDetail` has old-sample ambiguity. Earlier issue snapshots recorded old `HTTP404`, while the latest cached compare records old `101`; this needs one fixed baseline sample before root-cause classification.

## 5. Suggested Acceptance Order

1. `/Contract/GetMerchantAccountSplit`
2. `/Contract/GetContractAnalysis`
3. `/Contract/GetMerchantAccountDetail`

Reason:
`GetMerchantAccountSplit` already has executable SQL and stable sample params, so it is the best first-pass anchor. `GetContractAnalysis` should be checked next because it is clearly a placeholder and likely the main Contract code risk. `GetMerchantAccountDetail` should be validated last after the old-route sample basis is locked.

## 6. First-Pass Output Checklist

- one stable sample record for each Contract route
- one old/new result snapshot for each route
- one confirmed dependency summary for `GetMerchantAccountDetail`
- one note separating placeholder-code risk from data-sync risk

## 7. First-Pass Validation Result 2026-03-09

| Route | Repro sample | Old C# | New Python | Conclusion |
|------|------|------|------|------|
| `/Contract/GetMerchantAccountSplit` | `StatisticsMonth=202602` `StatisticsStartMonth=202602` `calcType=1` `CompactTypes=340001` | `100`, `ProjectCount=366`, merchant rows=`101` | `100`, `ProjectCount=366`, merchant rows=`102` | totals align, but Python adds one extra blank merchant row with `MerchantId=0`; non-blocking follow-up |
| `/Contract/GetContractAnalysis` | `statisticsDate=2026-02-13` `provinceCode=340000` `Serverpart_ID=416` | `100`, `ContractProfitLoss=5992.56`, `SalesPerSquareMeter=5781.24`, `ContractList=null` | `100`, `ContractProfitLoss=0`, `SalesPerSquareMeter=0`, `ContractList=[]` | confirmed code gap; current Python is still placeholder logic |
| `/Contract/GetMerchantAccountDetail` | `MerchantId=-1104` + same month filters | `100`, `ProjectDetailList=21` | `101`, `Result_Data=null` | confirmed blocker; weak sample `MerchantId=1` had created a false-green impression |

## 8. Stable Conclusions From This Pass

- `GetMerchantAccountDetail` must be validated with a merchant ID returned by `GetMerchantAccountSplit`. Using `MerchantId=1` is not sufficient.
- `GetContractAnalysis` is a true route-level code issue even when result codes are both `100`, because key business fields still differ.
- `GetMerchantAccountSplit` is close to aligned, but Python currently keeps one `MerchantId=0` empty merchant group that old C# does not return.
