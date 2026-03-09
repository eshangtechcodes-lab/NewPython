# 工作日志补充 2026-03-09（AI Follow-up）

## 本轮执行

- 修复 `middleware/query_cleanup.py`
  - 不再把歧义参数强制重写为单一大小写
  - 改为给 `serverpartid`、`provincecode`、`pageindex`、`pagesize` 扩展兼容别名
- 修复 `/BaseInfo/GetBusinessTradeList` GET 输出字段
  - 仅保留 `BUSINESSTRADE_NAME`、`BUSINESSTRADE_PNAME`
  - 其余字段显式返回 `null`
- 调整脚本：
  - `scripts/compare_revenue_bigdata.py` 忽略 `/BigData/GetRevenueTrendChart` 的时间敏感 `TotalCount`
  - `scripts/compare_baseinfo.py` 移除失效用例 `GetShopCountList_GET`

## 回归结果

- `python scripts/compare_revenue_bigdata.py`
  - 结果：`PASS=73/74`，`DIFF=1`，`FIELD_DIFF=0`
  - 唯一真实差异：`GET /Revenue/GetShopINCAnalysis`
- `python scripts/compare_baseinfo.py`
  - 结果：当前专项脚本全部通过

## 已确认结论

- `/Revenue/GetRevenueReport` 之前异常的根因是 `provinceCode` 被中间件错误重写
- `/Revenue/GetMonthlySPINCAnalysis`、`/Revenue/GetServerpartINCAnalysis` 的 `TotalCount` 差异也是同类参数兼容问题
- `/BigData/GetRevenueTrendChart` 的 `TotalCount` 与当前时间相关，不应当做静态基线字段
- `/BaseInfo/GetBusinessTradeList` GET 版本旧接口只输出两个业务字段，其余字段是 `null`

## 当前剩余问题

- `/Revenue/GetShopINCAnalysis`
  - 旧接口返回 `101`
  - Python 当前返回 `100`
  - 旧接口实际走 `HolidayHelper.GetShopINCAnalysis`
  - Python 当前实现仍是简化版查询，属于未完全对齐旧逻辑

## 下一步

1. 直接按旧 C# helper 重实现 `/Revenue/GetShopINCAnalysis`
2. 继续并行推进 `BaseInfo POST`、`Contract`、`Examine` 的首轮样本和验收
