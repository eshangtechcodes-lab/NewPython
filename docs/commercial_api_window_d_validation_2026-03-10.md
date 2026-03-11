# CommercialApi Window D Validation

> Date: `2026-03-10`
>
> Scope: exact-sample regression validation at the current checkpoint
>
> Old API: `http://192.168.1.99:8900/CommercialApi`
>
> New API: `http://127.0.0.1:8080/CommercialApi`

## 1. Important Runtime Note

Window D validation did not fail only at the route level.

During this validation round:

- local `8001` was unreachable from the workspace
- local `8080` was reachable for part of the run
- later in the same round, local `8080` also became unreachable

Operational implication:

- the current local validation target is not stable enough to treat all mid-run results as one continuous steady-state baseline

## 2. Routes Confirmed Exact-Pass During This Round

Using fixed business samples, the following routes were observed as exact-pass against old API while `8080` was reachable:

- `GET /Revenue/GetSalableCommodity`
- `POST /Examine/GetMEETINGList`
- `GET /Revenue/GetServerpartINCAnalysis`

Observed state at that checkpoint:

- `Result_Code` matched
- `TotalCount` matched where applicable
- full response payload matched for the fixed sample at that moment

## 3. Routes Returning `100` But Still Not Exact-Equal

The following routes returned successful result codes and matched top-level counts, but the full payload was not byte-for-byte equal:

- `GET /Revenue/GetMonthINCAnalysis`
- `GET /Revenue/GetShopSABFIList`
- `GET /BigData/GetBayonetOwnerAHTreeList`

Judgment:

- These routes are not blocked at the result-code layer.
- They still require structural/value-level closeout if final acceptance requires exact parity.

## 4. Routes Blocked By New-Side `999`

These routes are currently blocked before any meaningful payload comparison:

- `GET /Revenue/GetSPBayonetList`
  - `No module named 'dateutil'`
- `GET /Revenue/GetProvinceAvgBayonetAnalysis`
  - `No module named 'dateutil'`
- `POST /BigData/GetRevenueTrendChart`
  - Redis connection refused at `127.0.0.1:6379`
- `GET /BigData/GetProvinceVehicleTreeList`
  - DM SQL syntax error
  - `CODE:-2007`

Operational implication:

- These are not yet payload-alignment tasks.
- They are dependency / environment / SQL unblock tasks.

## 5. Why Window D Cannot Be Treated As Final Acceptance Yet

Window D depends on a stable local target.

Current blockers to final closeout are:

1. local target process instability
2. unresolved new-side `999` prerequisites
3. payload-level differences still remaining on several successful routes

## 6. Immediate Next Rule

Do not continue broad final acceptance until the following is true:

1. the exact local target port is confirmed
2. the target process remains reachable and stable through one full validation pass
3. dependency and SQL blockers are cleared

Only after that should Window D be rerun as the final regression gate.

