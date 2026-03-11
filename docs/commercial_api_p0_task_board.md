# CommercialApi P0 任务板

> 适用范围：`Revenue`、`BaseInfo`、`Contract`、`Examine`
>
> 目标：完成 P0 模块的首轮内容级验收、问题归因和回归闭环。
>
> 更新时间：2026-03-09

## 1. P0 范围概览

| 模块 | 路由数 | 主要风险 | 推荐脚本 | 当前状态 |
|------|------:|----------|----------|----------|
| Revenue | 50 | 聚合统计、历史/实时口径、POST+AES、列表明细联动 | `compare_cached.py` `compare_revenue_bigdata.py` `check_timeout.py` | 待验收 |
| BaseInfo | 9 | 树结构、筛选参数、POST+AES、基础字典口径 | `compare_baseinfo.py` `check_baseinfo.py` `check_baseinfo_detail.py` | 待验收 |
| Contract | 3 | 明细字段、账户拆分、列表联动 | `compare_cached.py` | 待验收 |
| Examine | 15 | 列表/明细、WeChat 路径、POST+AES、数据同步问题 | `compare_cached.py` `check_list_then_detail.py` `check_timeout.py` | 待验收 |

P0 汇总：

- 总路由数：`77`
- 明确 AES 接口：`5`
- 首轮建议并行任务数：`4`

## 2. 并行任务卡

### Task-P0-01

- 任务名称：`Revenue` 首轮内容验收
- 负责人：待分配
- 范围：`/Revenue/*`
- 输入：
  - [commercial_api_inventory.md](D:/Projects/Python/eshang_api/docs/commercial_api_inventory.md)
  - [commercial_api_workflow.md](D:/Projects/Python/eshang_api/docs/commercial_api_workflow.md)
  - `scripts/compare_cached.py`
  - `scripts/compare_revenue_bigdata.py`
- 输出：
  - `Revenue` 差异清单
  - `Revenue` 业务规则补充
  - `Revenue` 问题单
- 高风险：
  - `GetMonthINCAnalysis`
  - `GetRevenueReport`
  - `GetRevenueReportDetil`
  - `GetRevenueCompare`
  - `GetBusinessRevenueList`
  - `GetMonthlyBusinessRevenue`
- 首轮重点依赖表：
  - `T_REVENUEDAILY`
  - `T_REVENUEMONTHLY`
  - `T_REVENUEDASHBOARD`
  - `T_BUSINESSWARNING`
  - `T_SERVERPART`
  - `T_SERVERPARTSHOP`
  - `T_FIELDENUM`
  - `T_FIELDEXPLAIN`
  - `T_GOODSSALABLE`
- 完成标准：
  - 50 个接口完成首轮验收状态标记
  - 所有差异项完成初步归因
  - 至少补充 3 条稳定业务/技术结论到 AI Context

### Task-P0-02

- 任务名称：`BaseInfo + Contract` 首轮内容验收
- 负责人：待分配
- 范围：`/BaseInfo/*`、`/Contract/*`
- 输入：
  - [commercial_api_inventory.md](D:/Projects/Python/eshang_api/docs/commercial_api_inventory.md)
  - `scripts/compare_baseinfo.py`
  - `scripts/check_baseinfo.py`
  - `scripts/check_baseinfo_detail.py`
- 输出：
  - `BaseInfo` 与 `Contract` 差异清单
  - 基础字典/服务区树规则说明
- 高风险：
  - `GetServerInfoTree`
  - `GetServerpartList`
  - `GetServerpartServiceSummary`
  - `GetBrandStructureAnalysis`
  - `GetMerchantAccountSplit`
  - `GetMerchantAccountDetail`
- 首轮重点依赖表：
  - `T_SERVERPARTTYPE`
  - `T_AUTOSTATISTICS`
  - `T_SERVERPART`
  - `T_RTSERVERPART`
  - `T_SERVERPARTINFO`
  - `T_FIELDENUM`
  - `T_FIELDEXPLAIN`
  - `T_BRAND`
- 完成标准：
  - 12 个接口完成首轮状态标记
  - 树结构和明细接口全部完成至少一组样本验证

### Task-P0-03

- 任务名称：`Examine` 首轮内容验收
- 负责人：待分配
- 范围：`/Examine/*`
- 输入：
  - [commercial_api_inventory.md](D:/Projects/Python/eshang_api/docs/commercial_api_inventory.md)
  - `scripts/compare_cached.py`
  - `scripts/check_list_then_detail.py`
  - `scripts/check_timeout.py`
- 输出：
  - `Examine` 差异清单
  - 列表/明细联动问题清单
  - 数据同步问题和代码问题拆分结果
- 高风险：
  - `GetMEETINGList`
  - `GetMEETINGDetail`
  - `GetEXAMINEList`
  - `GetPATROLList`
  - `GetEvaluateResList`
- 完成标准：
  - 15 个接口完成首轮状态标记
  - `T_MEETING` 问题从代码问题中单独剥离

### Task-P0-04

- 任务名称：P0 公共收口
- 负责人：待分配
- 范围：P0 全模块
- 输入：
  - Task-P0-01/02/03 输出
  - 公共脚本、公共中间件、AES 工具
- 输出：
  - 公共问题汇总
  - 统一回归结果
  - P0 风险结论
- 约束：
  - 仅在并行任务首轮归因完成后开始
  - 统一处理公共逻辑问题，不接受并行期间分散修改公共层
- 完成标准：
  - 公共问题合并处理
  - 完成一次 P0 统一回归

## 3. P0 验收顺序

建议顺序：

1. `Revenue`
2. `BaseInfo`
3. `Contract`
4. `Examine`
5. P0 公共收口与统一回归

## 4. P0 统一要求

- 每个接口至少有空参样本、文档样本、真实样本三类样本
- 每个接口必须标记验收状态：`未开始 / 进行中 / 有差异 / 阻塞 / 通过`
- 每个差异项必须标记问题类型：`代码 / 数据 / 待确认`
- 每个任务结束前必须补充：
  - 当日 `workLog`
  - AI Context 稳定结论
  - 可复用坑点

## 5. P0 重点记录项

执行过程中，重点沉淀以下信息：

- 参数真实业务含义
- 默认排序和默认分页
- 列表与明细的跳转链路
- 历史口径与实时口径分流
- AES 解密后的真实参数结构
- 依赖表、关键字段、时间范围
- 新旧库差异是否来自数据同步

## 6. P0 结束标准

P0 阶段视为完成，需要同时满足：

- 77 个接口全部完成首轮状态标记
- 阻塞项已明确归因
- 公共问题已统一收口
- 完成一轮统一回归
- 关键技术要点、业务规则、踩坑结论已沉淀
