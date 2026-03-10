# CommercialApi Validation Script Gaps

> Date: `2026-03-10`
>
> Scope: current broad comparison scripts and cached baselines

## 1. Current Judgment

Broad compare results should not be treated as final parity truth for all routes.

They are still useful for:

- result-code scans
- first-pass route coverage
- catching obvious `TotalCount` regressions

They are not sufficient for:

- top-level business-field parity
- routes that return `List` instead of `DataList`
- fixed-sample structure validation

## 2. Confirmed Missed Cases

### `GET /Revenue/GetSalableCommodity`

- Real diff exists:
  - old API returns `SalableCommodity = 24.7`
  - new API returns `SalableCommodity = 0.0`
- This diff is easy to miss because it is a top-level business field, not a `TotalCount` change.

### `POST /Examine/GetMEETINGList`

- Real diff exists:
  - count is aligned
  - row structure and formatting are not aligned
- This diff is easy to miss because current broad compare does not deeply validate `List` payloads.

## 3. Script-Level Gaps

### `compare_cached.py`

Relevant locations:

- [compare_cached.py](/D:/Project/Python/NewPython/scripts/compare_cached.py#L67)
- [compare_cached.py](/D:/Project/Python/NewPython/scripts/compare_cached.py#L92)
- [compare_cached.py](/D:/Project/Python/NewPython/scripts/compare_cached.py#L98)

Current limitations:

- summary output mainly highlights `Result_Code` and `TotalCount`
- row-field comparison is only against `Result_Data.DataList`
- it does not deeply compare top-level custom fields such as `SalableCommodity`
- it does not deeply compare routes whose rows are under `List`

### `baseline_collect.py`

Relevant locations:

- [baseline_collect.py](/D:/Project/Python/NewPython/scripts/baseline_collect.py#L17)
- [baseline_collect.py](/D:/Project/Python/NewPython/scripts/baseline_collect.py#L25)

Current limitations:

- old API host is still `127.0.0.1:8900`
- router directory still points to the old `eshang_api` path
- this script should not be used for fresh baseline rebuild until environment settings are corrected

### Cached POST samples

Current baseline strength is also limited by weak cached samples.

Example:

- `POST /Examine/GetMEETINGList` cached params are empty or non-business-grade
- this weakens any acceptance claim based only on cached replay

## 4. Practical Rule

Use broad compare as a coverage tool, not as the final acceptance tool.

Precise replay is mandatory when any of the following applies:

- route returns important top-level business fields
- route returns rows under `List` rather than `DataList`
- user requires exact structure parity
- route was previously blocked and is being formally closed

