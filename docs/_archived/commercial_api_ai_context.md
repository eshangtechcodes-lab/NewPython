# CommercialApi AI Context

> 用途：沉淀 `CommercialApi` 已验证、可复用、适合后续 AI 直接读取的稳定结论。

## 1. 当前阶段

- 项目：`CommercialApi`
- 目标：完成 Python 版本内容级验收、问题归因、回归和联调准备
- 当前阶段：`P0 验收进行中`
- 最近更新：`2026-03-09`

## 2. 当前真实状态

- `Revenue + BigData` 最近一次批量对比结果为 `PASS=73/74`，当前只剩 1 个真实代码差异：`GET /Revenue/GetShopINCAnalysis`
- `BaseInfo` 当前专项脚本已全绿：`GetSPRegionList`、`GetBusinessTradeList(GET)` 都已对齐
- `GetRevenueTrendChart` 的 `TotalCount` 不应作为稳定验收指标，因为旧 C# 与 Python 都按当前时间生成半小时桶

## 3. 已确认技术结论

### 参数兼容

- `query_cleanup.py` 不能把歧义参数统一重写成单一大小写。
- `serverpartid`、`provincecode`、`pageindex`、`pagesize` 这类参数必须做别名扩展，而不是强制改名。
- 原因：不同平移路由使用的参数名大小写并不一致，强制重写会让部分路由丢失筛选条件。

### BaseInfo GET 字段口径

- `/BaseInfo/GetBusinessTradeList` 的 GET 版本只应输出：
  - `BUSINESSTRADE_NAME`
  - `BUSINESSTRADE_PNAME`
- 其余字段应保持 `null`。
- 原因：旧 C# GET helper 只绑定这两个字段。

### 时间敏感接口

- `/BigData/GetRevenueTrendChart` 的 `TotalCount` 与当前时刻有关。
- 旧 C# helper 与 Python 都是从 `0.5` 小时累加到 `DateTime.Now.TimeOfDay.TotalHours`。
- 因此同一份基线在不同时刻回放时，`TotalCount` 可以自然不同。

## 4. 已确认业务逻辑

### BusinessTradeType

- `BusinessTradeType=1/2/3` 是业务映射条件，不是数据库字段的直接枚举值。
- 典型适用接口：`Revenue/GetMonthINCAnalysis` 等统计类接口。
- Python 不能直接把它当成 `BUSINESS_TYPE IN (...)` 使用，必须复刻旧 C# 的组合条件逻辑。

### solidType

- `solidType=true` 时，部分收入分析接口需要走固化口径，不是实时口径。
- 典型适用接口：`Revenue/GetMonthINCAnalysis`
- 旧 C# 在固化和实时模式之间存在数据源分流。

## 5. 当前已确认坑点

### 坑点 1：全局参数重写

- 现象：接口能返回，但筛选范围明显过大或完全失效。
- 根因：中间件把不同大小写风格的参数统一重写，破坏了 FastAPI 绑定。
- 处理规则：对歧义参数做别名扩展，对非歧义参数才做兼容重写。

### 坑点 2：时间窗口型对比误报

- 现象：新旧接口返回码一致，但 `TotalCount` 随运行时间波动。
- 根因：接口结果本身依赖当前时间。
- 处理规则：验收时把这类接口标记为时间敏感，不把动态 `TotalCount` 当成固定基线。

### 坑点 3：旧 GET helper 只回填部分字段

- 现象：Python 返回结构更“完整”，但反而和旧接口不一致。
- 根因：旧 C# 某些 GET helper 只填充部分字段，其余字段序列化为 `null`。
- 处理规则：优先对齐旧接口真实输出，不要默认补满所有模型字段。

## 6. 当前阻塞项

| 日期 | 阻塞项 | 范围 | 归因 |
|------|--------|------|------|
| 2026-03-09 | `/Revenue/GetShopINCAnalysis` 新旧返回码不一致 | Revenue | 代码 |
| 2026-03-09 | `T_GOODSSALABLE` 数据同步风险 | Revenue | 数据 |
| 2026-03-09 | `T_MEETING` 数据量异常少 | Examine | 数据 |

## 7. 下一步建议

1. 优先重实现 `/Revenue/GetShopINCAnalysis`，直接对齐旧 C# `HolidayHelper.GetShopINCAnalysis`。
2. 并行推进 `BaseInfo POST`、`Contract`、`Examine` 的样本准备和首轮验收。
3. 所有公共层改动继续串行收口，避免并行阶段互相覆盖。
## 8. Stable Conclusions 2026-03-09 T7

### Validation SKIP Rule For Old API Unavailable

- Scope: all `CommercialApi` parity checks
- Conclusion: when the old API side is `TIMEOUT`, `HTTP404`, or otherwise unavailable, the case must be marked `SKIP` instead of being promoted to a Python route blocker
- Reason: parity judgment needs a stable old-side baseline; without that baseline, the result is a comparison-environment issue, not confirmed Python route drift
- Validation:
  - `scripts/test_results/compare_cached.json` contains `SKIP` cases such as `/Debug/QuerySQL` and `/Examine/GetMEETINGList`
  - `docs/commercial_api_parallel_task_f_acceptance_rules.md` section 4 and section 6 publish the unified handling rule
- Date: `2026-03-09`
- Status: Verified

### Stale Script Case Handling Rule

- Scope: all active acceptance runs
- Conclusion: stale script cases, especially cases where old API is already `HTTP404` and new API returns `HTTP422`, must be removed from blocker counting and daily acceptance output
- Reason: the sample itself is no longer a valid parity sample, so the case creates noise rather than a reproducible route defect
- Validation:
  - `docs/commercial_api_parallel_task_board.md` records stale script cases as an identified noisy source for `T6`
  - `docs/commercial_api_parallel_task_f_acceptance_rules.md` section 4 records the approved noisy-case rule
- Date: `2026-03-09`
- Status: Verified
