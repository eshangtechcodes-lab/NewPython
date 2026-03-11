# CommercialApi T3 BaseInfo First Pass

> Date: `2026-03-09`
>
> Scope: remaining `BaseInfo` APIs
>
> Source samples: [commercial_api_t3_baseinfo_prep.md](D:/Projects/Python/eshang_api/docs/commercial_api_t3_baseinfo_prep.md)

## 1. Replay Scope

- Replay target:
  - `POST /BaseInfo/GetBusinessTradeList`
  - `POST /BaseInfo/GetBrandStructureAnalysis`
  - `POST /BaseInfo/GetServerpartServiceSummary`
  - `GET /BaseInfo/GetServerpartList`
  - `GET /BaseInfo/GetServerpartInfo`
  - `GET /BaseInfo/GetServerInfoTree`
  - `GET /BaseInfo/GetBrandAnalysis`
- Replay endpoints:
  - old: `http://127.0.0.1:8900/CommercialApi`
  - new: `http://127.0.0.1:8080/CommercialApi`
- Fixed sample note:
  - `GetServerInfoTree` used header `ServerpartCodes: 341003`
  - both AES routes used the fixed ciphertext from `doc_params.json`

## 2. First-pass Result

| Route | Method | Old Result | New Result | Status | First Confirmed Diff | Initial Type |
|------|------|------|------|------|------|------|
| `/BaseInfo/GetBusinessTradeList` | POST | `C=100,T=230` | `C=100,T=230` | TBD | first page hits different records under the minimal sample, so content cannot yet be blamed on code | Sample/Rule TBD |
| `/BaseInfo/GetBrandStructureAnalysis` | POST AES | `C=100,T=4` | `C=100,T=4` | Pass | no diff in fixed sample replay | Pass |
| `/BaseInfo/GetServerpartServiceSummary` | POST AES | `C=100,ServerpartTotalCount=133` | `C=100,ServerpartTotalCount=135` | Diff | `AutoRepairCount` old=`120`, new=`122` | Code/Data TBD |
| `/BaseInfo/GetServerpartList` | GET | `C=100,T=10` | `C=100,T=10` | Diff | `HASCHARGE` old=`bool`, new=`int` | Code |
| `/BaseInfo/GetServerpartInfo` | GET | `C=100` | `C=100` | Diff | `ISCUR_SERVERPART` old=`0`, new=`null` | Code |
| `/BaseInfo/GetServerInfoTree` | GET | `C=100,T=1` | `C=100,T=1` | Diff | nested `children` old=`null`, new=`[]` | Code |
| `/BaseInfo/GetBrandAnalysis` | GET | `C=100` | `C=100` | Diff | `BrandTag` old=`list`, new=`string` | Code |

## 3. Stable Findings

- `GetBrandStructureAnalysis` is the first remaining `BaseInfo` route in this batch that fully aligns under a fixed sample.
- `GetServerInfoTree` can now be replayed stably when the request carries `ServerpartCodes: 341003`.
- `GetServerpartServiceSummary` is no longer blocked by AES ambiguity; the remaining issue is aggregate drift, not payload shape.
- The minimal pagination sample for `POST /BaseInfo/GetBusinessTradeList` is not enough to prove content alignment because old and new first pages are not stable on the same row set.

## 4. Next Split

1. Treat `GetBrandStructureAnalysis` as closed for first-pass content validation.
2. Open code-level issue notes for:
   - `GetServerpartList`
   - `GetServerpartInfo`
   - `GetServerInfoTree`
   - `GetBrandAnalysis`
3. Keep `GetBusinessTradeList(POST)` as `Sample/Rule TBD` until one explicit sort/filter sample is fixed.
4. Keep `GetServerpartServiceSummary` as `Code/Data TBD` until the two-count drift is separated from possible data freshness effects.
