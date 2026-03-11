# CommercialApi P0 验收台账

> 范围：`Revenue`、`BaseInfo`、`Contract`、`Examine`
>
> 状态值：`未开始` / `进行中` / `有差异` / `阻塞` / `通过`
>
> 问题类型：`代码` / `数据` / `脚本` / `待确认`

## 1. 当前结论

### Revenue / BigData

- 最近一次批量结果：`2026-03-09`
- 脚本：`scripts/compare_revenue_bigdata.py`
- 当前结果：`PASS=73/74`，`DIFF=1`，`FIELD_DIFF=0`
- 已确认完成：
  - `GetRevenueReport` 已对齐，返回码恢复为 `100`
  - `GetMonthlySPINCAnalysis` 已对齐
  - `GetServerpartINCAnalysis` 已对齐
  - `BigData/GetRevenueTrendChart` 属于时间窗口敏感接口，脚本已忽略 `TotalCount` 假差异
- 当前唯一真实阻塞：
  - `GET /Revenue/GetShopINCAnalysis`

### BaseInfo

- 最近一次批量结果：`2026-03-09`
- 脚本：`scripts/compare_baseinfo.py`
- 当前结果：专项脚本全部通过
- 已确认完成：
  - `GetSPRegionList` 通过
  - `GetBusinessTradeList(GET)` 已对齐
- 已处理脚本噪音：
  - 已移除脚本中的 `GetShopCountList_GET` 失效用例，避免误报

## 2. 关键修复记录

| 日期 | 项目 | 结论 |
|------|------|------|
| 2026-03-09 | `middleware/query_cleanup.py` | 不再强制重写 `serverpartid`、`provincecode` 等歧义参数，改为补充多种别名，避免破坏不同路由的大小写绑定 |
| 2026-03-09 | `/Revenue/GetRevenueReport` | 中间件错误重写 `provinceCode` 是根因，修复后返回码恢复为 `100` |
| 2026-03-09 | `/Revenue/GetMonthlySPINCAnalysis` | 中间件错误重写导致筛选失效，修复后 `TotalCount` 已对齐 |
| 2026-03-09 | `/Revenue/GetServerpartINCAnalysis` | 中间件错误重写导致筛选失效，修复后 `TotalCount` 已对齐 |
| 2026-03-09 | `/BaseInfo/GetBusinessTradeList` | GET 路径只应填充 `BUSINESSTRADE_NAME`、`BUSINESSTRADE_PNAME`，其余字段应为 `null` |
| 2026-03-09 | `/BigData/GetRevenueTrendChart` | 旧 C# 与 Python 都按当前时间生成半小时桶，`TotalCount` 对比属于时间敏感假差异 |

## 3. Revenue

| 接口 | 方法 | 风险 | 状态 | 问题类型 | 备注 |
|------|------|------|------|----------|------|
| `/Revenue/GetRevenueReport` | GET | 报表 | 通过 |  | 已修复 `provinceCode` 参数兼容问题 |
| `/Revenue/GetMonthlySPINCAnalysis` | GET | 月度分析 | 通过 |  | 已修复参数兼容问题 |
| `/Revenue/GetServerpartINCAnalysis` | GET | 增长分析 | 通过 |  | 已修复参数兼容问题 |
| `/Revenue/GetShopINCAnalysis` | GET | 增长分析 | 有差异 | 代码 | 旧接口走 `HolidayHelper.GetShopINCAnalysis`，Python 当前实现仍是简化查询，需按 C# 逻辑重写 |
| `/Revenue/GetMonthINCAnalysis` | GET | 固化/实时双口径 | 通过 |  | 已修复 `422` 问题 |
| `/Revenue/GetMonthINCAnalysisSummary` | GET | 汇总 | 通过 |  | 已修复 `422` 问题 |
| `/Revenue/GetShopMonthSABFIList` | GET | 列表 | 通过 |  | 已修复 `422` 问题 |
| `/Revenue/GetSalableCommodity` | GET | 依赖表 | 未开始 | 数据 | 仍需确认 `T_GOODSSALABLE` 数据同步情况 |

## 4. BaseInfo

| 接口 | 方法 | 风险 | 状态 | 问题类型 | 备注 |
|------|------|------|------|----------|------|
| `/BaseInfo/GetSPRegionList` | GET | 基础字典 | 通过 |  | 专项脚本已通过 |
| `/BaseInfo/GetBusinessTradeList` | GET | 基础字典 | 通过 |  | GET 路由字段已与旧接口对齐 |
| `/BaseInfo/GetBusinessTradeList` | POST | POST | 有差异 | 待确认 | 最小分页样本下旧新第一页命中不同记录；需补显式排序/过滤样本后再做代码归因 |
| `/BaseInfo/GetBrandAnalysis` | GET | 品牌分析 | 有差异 | 代码 | `BrandTag` 结构不一致：旧接口为列表，新接口为字符串 |
| `/BaseInfo/GetServerpartList` | GET | 筛选/分页 | 有差异 | 代码 | 首轮固定样本下 `HASCHARGE` 等字段存在布尔/整型口径差异 |
| `/BaseInfo/GetServerpartInfo` | GET | 详情 | 有差异 | 代码 | `ISCUR_SERVERPART` 旧接口为 `0`，新接口为 `null` |
| `/BaseInfo/GetServerInfoTree` | GET | 树结构 | 有差异 | 代码 | 首轮固定样本已可回放；嵌套 `children` 结构为 `null` vs `[]` |
| `/BaseInfo/GetServerpartServiceSummary` | POST | AES/POST | 有差异 | 代码/待确认 | 固定 AES 样本下 `ServerpartTotalCount` `133 -> 135`，`AutoRepairCount` `120 -> 122` |
| `/BaseInfo/GetBrandStructureAnalysis` | POST | AES/POST | 通过 |  | 固定 AES 样本首轮回放已对齐 |

## 5. Contract

| 接口 | 方法 | 风险 | 状态 | 问题类型 | 备注 |
|------|------|------|------|----------|------|
| `/Contract/GetContractAnalysis` | GET | 聚合 | 未开始 |  | 待补样本 |
| `/Contract/GetMerchantAccountSplit` | GET | 拆分规则 | 未开始 |  | 待补样本 |
| `/Contract/GetMerchantAccountDetail` | GET | 明细联动 | 未开始 |  | 待补样本 |

## 6. Examine

| 接口 | 方法 | 风险 | 状态 | 问题类型 | 备注 |
|------|------|------|------|----------|------|
| `/Examine/GetMEETINGList` | POST | POST/数据同步 | 未开始 | 数据 | `T_MEETING` 仍是已知风险 |
| `/Examine/GetMEETINGDetail` | GET | 明细/数据同步 | 未开始 |  | 待补样本 |
| `/Examine/GetEXAMINEList` | POST | POST | 未开始 |  | 待补样本 |
| `/Examine/GetPATROLList` | POST | POST | 未开始 |  | 待补样本 |
| `/Examine/GetEvaluateResList` | POST | AES/POST | 未开始 |  | 待补样本 |

## 7. 下一步

1. 以 `GetShopINCAnalysis` 为唯一真实代码阻塞，按旧 C# `HolidayHelper` 逻辑重实现。
2. 并行补齐 `BaseInfo POST`、`Contract`、`Examine` 的样本和首轮对比。
3. 保持公共层修改串行，继续避免在并行阶段同时改中间件和公共脚本。
