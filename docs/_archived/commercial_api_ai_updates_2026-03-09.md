# CommercialApi AI Updates 2026-03-09

## 本轮新增结论

- `QueryParamCleanupMiddleware` 曾将 `StatisticsStartMonth` / `StatisticsEndMonth` 全局改写为 lower camel case。
- 部分 `Revenue` 路由实际使用 PascalCase 参数名，因此即使 URL 已带参数，FastAPI 仍返回参数缺失 `422`。
- 该问题不是脚本传参问题，而是公共中间件改写参数名导致的绑定失败。

## 已完成修复

- 文件：[query_cleanup.py](D:/Projects/Python/eshang_api/middleware/query_cleanup.py)
- 处理：移除 `statisticsstartmonth` 和 `statisticsendmonth` 的全局改写映射

## 修复验证

直接接口验证已通过：

- `GET /Revenue/GetMonthINCAnalysis`：`200`
- `GET /Revenue/GetMonthINCAnalysisSummary`：`200`
- `GET /Revenue/GetShopMonthSABFIList`：`200`

批量回归结果更新为：

- `Revenue/BigData`：`PASS=70/74`，`DIFF=1`，`FIELD_DIFF=3`

## 当前剩余重点问题

- `GET /Revenue/GetRevenueReport`
  - 问题：返回码差异
  - 现象：旧接口 `100`，新接口 `200`

- `GET /Revenue/GetMonthlySPINCAnalysis`
  - 问题：`TotalCount` 异常
  - 现象：旧接口 `1`，新接口 `141`

- `GET /Revenue/GetServerpartINCAnalysis`
  - 问题：`TotalCount` 异常
  - 现象：旧接口 `1`，新接口 `141`

- `POST /BigData/GetRevenueTrendChart`
  - 问题：`TotalCount` 差异
  - 现象：旧接口 `46`，新接口 `23`

- `GET /BaseInfo/GetBusinessTradeList`
  - 问题：内容差异
  - 现象：结构接近，但首批数据不一致

## 对后续 AI 的建议

- 遇到 `422` 时，不要先假设是样本错误，先检查中间件是否改写了查询参数名。
- 对同时存在 PascalCase 和 camelCase 参数风格的项目，不要做全局强制大小写归一化。
- 月度分析类接口后续优先继续看 `TotalCount` 口径，而不是先看字段缺失。
## T7 Additions

- Added stable conclusion: old API `TIMEOUT` / `HTTP404` means the parity case is `SKIP`, not a Python route blocker.
- Added stable conclusion: stale script cases, especially `old=HTTP404` with `new=HTTP422`, must be removed from blocker counting.
- Added workflow reference: `docs/commercial_api_parallel_task_f_acceptance_rules.md` is now the active acceptance-rule baseline for closeout.
