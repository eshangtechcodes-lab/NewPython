# CommercialApi T3 BaseInfo Acceptance Prep

> Date: `2026-03-09`
>
> Task ID: `T3`
>
> Scope: remaining `BaseInfo` APIs only
>
> Rule: investigation and documentation only, no code changes

## 1. Baseline

- `GET /BaseInfo/GetSPRegionList` and `GET /BaseInfo/GetBusinessTradeList` are already aligned and are not part of this prep round.
- Current dedicated script coverage is still narrow:
  - `scripts/compare_baseinfo.py` only covers `GetSPRegionList` and `GetBusinessTradeList(GET)`.
  - `scripts/check_baseinfo.py` can read global batch results, but it is not a dedicated closeout artifact for the remaining `BaseInfo` routes.
  - `scripts/check_baseinfo_detail.py` keeps useful sample hints, but part of the POST capture is incomplete.
- Historical records conflict:
  - `workLog/2026-03-06.md` once recorded `BaseInfo 9/9 PASS`.
  - the current `2026-03-09` task board and P0 acceptance board still treat most remaining `BaseInfo` routes as not yet first-pass accepted.
- For `T3`, the current source of truth is the `2026-03-09` task board. This note closes only the prep work: sample plan, dependency summary, and risk marks.

## 2. Existing Evidence

- Sample source:
  - `scripts/test_results/doc_params.json`
  - `scripts/check_baseinfo_detail.py`
- Historical diff source:
  - `scripts/test_results/issues_detail.json`
  - `scripts/test_results/last_run.txt`
  - `scripts/test_results/placeholder_analysis.txt`
- Dependency source:
  - `scripts/test_results/helper_tables_check.txt`
- Current acceptance baseline:
  - `docs/commercial_api_p0_acceptance.md`
  - `docs/commercial_api_parallel_task_board.md`

## 3. Remaining Route Inventory

| Order | Route | Method | Sample Plan | Key Dependencies | Risk Mark | Current Evidence | First-pass Goal |
|------|------|------|------|------|------|------|------|
| 1 | `/BaseInfo/GetBusinessTradeList` | POST | body sample `{"PageIndex":1,"PageSize":3}`; add one sort sample if needed | `T_AUTOSTATISTICS` | Script-Low | `last_run` shows `C=100,T=230`; dedicated BaseInfo compare script does not cover it | confirm POST body shape and pagination/sort behavior |
| 2 | `/BaseInfo/GetBrandStructureAnalysis` | POST AES | reuse AES ciphertext from `doc_params.json`; decrypted payload is fixed as `{"ProvinceCode":"340000","BusinessTrade":""}` | `T_BRAND`, `T_FIELDENUM`, `T_FIELDEXPLAIN` | AES/Data-Medium | baseline cache already has a successful old response `C=100,T=4`; latest broad run showed `C=999` on both sides | separate payload validity from table-sync impact |
| 3 | `/BaseInfo/GetServerpartServiceSummary` | POST AES | reuse AES ciphertext from `doc_params.json`; decrypted payload is fixed as `{"ProvinceCode":"340000","SPRegionType_ID":"","ServerpartId":""}` | `T_SERVERPART`, `T_SERVERPARTINFO`, `T_FIELDENUM`, `T_FIELDEXPLAIN` | AES/Data-Medium | baseline cache already has a successful old response `C=100`; later broad runs also recorded `C=999` on both sides | use the fixed payload first, then replay with one narrowed service-area sample if needed |
| 4 | `/BaseInfo/GetServerpartList` | GET | query sample `Province_Code=340000&Serverpart_ID=416&PageIndex=1&PageSize=10&ShowWeather=false&ShowService=false&SPRegionType_ID=` | `T_SERVERPART`, `T_SERVERPARTINFO`, `T_RTSERVERPART`, `T_SERVERPARTMAP`, `T_NOTICEINFO`, `T_ACCOUNTWARNING`, `T_BUSINESSPROJECT`, `T_FIELDENUM` | Code/Data-High | history shows `old C=100,T=10 -> new C=100,T=0`; `Province_Code` inner-code mapping is a known pitfall | verify list count, page count meaning, and `Province_Code` conversion |
| 5 | `/BaseInfo/GetServerpartInfo` | GET | query sample `ServerpartId=416` | `T_SERVERPART`, `T_RTSERVERPART`, `T_SERVERPARTINFO`, `T_SERVERPARTMAP`, `T_NOTICEINFO`, `T_ACCOUNTWARNING` | Data-High | history shows `old C=100 -> new C=101` | verify one list-to-detail linked sample after list route is stable |
| 6 | `/BaseInfo/GetServerInfoTree` | GET | query sample `ProvinceCode=340000&ServerpartIds=416&SPRegionTypeId=` plus header `ServerpartCodes: 341003` | `T_SERVERPART`, `T_SERVERPARTINFO` | Rule-Medium | `ServerpartId=416` maps to `SERVERPART_CODE=341003` in baseline cache; local replay on new API returned `C=100,T=1` with a non-empty tree | use this fixed header/query pair as the first-pass tree sample |
| 7 | `/BaseInfo/GetBrandAnalysis` | GET | query sample `ProvinceCode=340000&Serverpart_ID=416&Statistics_Date=2026-02-13&ShowAllShop=false&BusinessTradeIds=` | `T_BRAND`, `T_REGISTERCOMPACT`, `T_SERVERPARTSHOP` | Code-High | history shows `old C=100 -> new C=101`; placeholder analysis also marked it as open | treat as the highest code-gap route in this module |

## 4. Route-level Notes

### 4.1 POST `/BaseInfo/GetBusinessTradeList`

- Current usable sample does exist, but it comes from `scripts/check_baseinfo_detail.py`, not from the preserved document capture.
- `doc_params.json` stored a response-shaped placeholder for this route, so it must not be treated as the real POST request body.
- This route should be the first remaining `BaseInfo` route to replay because it extends an already aligned GET branch and has the smallest dependency surface.

### 4.2 POST AES routes

- `GetServerpartServiceSummary` and `GetBrandStructureAnalysis` already have reusable ciphertext samples in `doc_params.json`.
- For first-pass validation, each AES route should keep two artifacts together:
  - original ciphertext body
  - decrypted parameter map for replay explanation
- The decrypted payloads are now fixed:
  - `GetServerpartServiceSummary`: `{"ProvinceCode":"340000","SPRegionType_ID":"","ServerpartId":""}`
  - `GetBrandStructureAnalysis`: `{"ProvinceCode":"340000","BusinessTrade":""}`
- Baseline cache already preserved successful old responses for both AES routes, so they are no longer blocked by payload ambiguity.

### 4.3 Service-area list/detail/tree chain

- `GetServerpartList`, `GetServerpartInfo`, and `GetServerInfoTree` should be accepted as one chain instead of three isolated routes.
- Order matters:
  - first lock the list sample
  - then use one returned service-area record for detail replay
  - finally replay the tree route with the same service-area scope
- `GetServerInfoTree` header gap is now fixed:
  - baseline cache shows `ServerpartId=416 -> SERVERPART_CODE=341003`
  - local replay on the new API succeeded with `ServerpartCodes: 341003`
  - the first-pass tree sample is therefore stable enough for downstream validation

### 4.4 `GetBrandAnalysis`

- This route remains the clearest code-risk item in `BaseInfo`.
- It should be delayed until the list/detail/tree chain and both POST/AES routes have stable replay inputs, otherwise the comparison noise will stay high.

## 5. Dependency Summary

### 5.1 BaseInfo helper tables

- `BaseInfoHelper.cs`
  - `T_AUTOSTATISTICS`
  - `T_ENDACCOUNT_TEMP`
  - `T_SERVERPART`
  - `T_SERVERPARTSHOP`
- `ServerpartHelper.cs`
  - `T_ACCOUNTWARNING`
  - `T_BUSINESSPROJECT`
  - `T_NOTICEINFO`
  - `T_RTSERVERPART`
  - `T_SERVERPART`
  - `T_SERVERPARTINFO`
  - `T_SERVERPARTMAP`
  - `T_SERVERPARTSHOP`
- `BrandAnalysisHelper.cs`
  - `T_BRAND`
  - `T_REGISTERCOMPACT`
  - `T_SERVERPARTSHOP`

### 5.2 Dictionary tables used by current Python implementation

- `T_FIELDENUM`
- `T_FIELDEXPLAIN`

## 6. Acceptance Order

1. `POST /BaseInfo/GetBusinessTradeList`
2. `POST /BaseInfo/GetBrandStructureAnalysis`
3. `POST /BaseInfo/GetServerpartServiceSummary`
4. `GET /BaseInfo/GetServerpartList`
5. `GET /BaseInfo/GetServerpartInfo`
6. `GET /BaseInfo/GetServerInfoTree`
7. `GET /BaseInfo/GetBrandAnalysis`

## 7. Blockers And Pitfalls

- `GetBusinessTradeList(POST)` has a sample-capture gap in `doc_params.json`; the current usable request body comes from script fallback only.
- `GetServerpartList` must verify the `Province_Code -> FIELDENUM_ID` conversion before code blame.
- Historical status for both AES routes conflicts across different runs, so payload validity and data availability must be checked before calling them code issues.
- `GetBrandAnalysis` is still the only `BaseInfo` route in this prep set that already has a stable code-gap signal.

## 8. T3 Closeout

- Remaining `BaseInfo` APIs now all have:
  - a first-pass sample plan
  - dependency tables
  - a risk mark
  - an acceptance order
- Fixed replay materials now exist for:
  - `GetServerInfoTree` header sample: `ServerpartCodes: 341003`
  - `GetServerpartServiceSummary` decrypted payload
  - `GetBrandStructureAnalysis` decrypted payload
- `T3` prep output is ready for downstream first-pass validation.
