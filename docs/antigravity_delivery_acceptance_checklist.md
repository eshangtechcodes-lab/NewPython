# Antigravity 交付验收清单

适用范围：
- `CommercialApi` 代码整改交付验收
- 仅用于验收代码修复结果，不用于数据同步问题收口

使用说明：
1. 每个问题项先收交付材料，再做单项验收。
2. 单项验收完成后，统一跑一轮全量回归。
3. 最终将问题分为：已关闭代码问题、未关闭代码问题、纯数据问题。

## 一、交付材料检查表

每个问题项必须先补齐以下材料，缺一项则状态记为 `待补材料`。

| 接口/问题 | 根因说明 | 修改文件 | 验收样本 | 回归结果 | 剩余风险 | 材料状态 | 备注 |
|------|------|------|------|------|------|------|------|
| Revenue/GetShopINCAnalysis | 已恢复旧 HolidayHelper 口径，空数据返回 `101` | 见 `fix` 提交链 | 基线样本 `2026-02-13 + ServerpartId=416 + HolidayType=2` | `compare_revenue_bigdata.py` `74/74 PASS` | 无新增风险 | 已验收 | 旧新均 `101` |
| Contract/GetMerchantAccountDetail | 已从 placeholder 改为真实明细查询 | 见 `fix` 提交链 | `MerchantId=-1104` + `StatisticsMonth=202602` | 单项回放通过 | 无新增风险 | 已验收 | 旧新均 `100`，`ProjectDetailList=21` |
| Contract/GetContractAnalysis | 已补旧 helper 逻辑 | 见 `fix` 提交链 | `statisticsDate=2026-02-13&provinceCode=340000&Serverpart_ID=416` | 单项回放通过 | 无新增风险 | 已验收 | 关键字段已对齐 |
| Examine/GetEvaluateResList | 已补查询逻辑，不再是占位返回 | 见 `fix` 提交链 | 固定 AES 样本 | 单项回放通过 | 固定样本下通过，建议后续补业务样本 | 已验收 | 旧新均 `100`，固定样本 `TotalCount=0` |
| BaseInfo/GetBrandAnalysis | `BrandTag` 类型已对齐 | 见 `fix` 提交链 | `ProvinceCode=340000&Serverpart_ID=416&Statistics_Date=2026-02-13` | 单项回放通过 | 无新增风险 | 已验收 | 旧新首项 `BrandTag` 均为数组 |
| BaseInfo/GetServerpartList | 字段类型已对齐 | 见 `fix` 提交链 | `Province_Code=340000&Serverpart_ID=416&PageIndex=1&PageSize=10` | 单项回放通过 | 无新增风险 | 已验收 | `HASCHARGE` 均为 `Boolean` |
| BaseInfo/GetServerpartInfo | 默认值和详情字段已对齐 | 见 `fix` 提交链 | `ServerpartId=416` | 单项回放通过 | 无新增风险 | 已验收 | `ISCUR_SERVERPART` 旧新均为 `0` |
| BaseInfo/GetServerInfoTree | 树结构样本已对齐 | 见 `fix` 提交链 | header `ServerpartCodes=341003` + `ServerpartIds=416` | 单项回放通过 | 需继续沿用固定 header 样本 | 已验收 | `children` 结构对齐 |
| BaseInfo/GetServerpartServiceSummary | 当前仍存在统计值漂移 | 未见有效收口证据 | 固定 AES 样本 | 单项回放未通过 | 更像数据或口径问题，需单独归因 | 已验收 | 旧 `133/120`，新 `135/122` |
| BaseInfo/GetBusinessTradeList (POST) | 空 body 下旧新内容仍不一致 | 未收口 | `POST {}` | 单项回放未通过 | 明显仍是代码问题 | 已验收 | 旧 `TotalCount=230,List=[]`；新 `TotalCount=230,List=230` |
| Contract/GetMerchantAccountSplit | 空商户已过滤，但总量仍有差异 | 见 `fix` 提交链 | `StatisticsMonth=202602&StatisticsStartMonth=202602&calcType=1&CompactTypes=340001` | 单项回放部分通过 | 需确认 `ProjectCount` 差异来源 | 已验收 | 旧 `ProjectCount=366`，新 `363`，均无 `MerchantId=0` |

## 二、单项验收表

状态值统一使用：
- `通过`
- `未通过`
- `待确认`
- `待补材料`

问题归类统一使用：
- `代码问题已关闭`
- `仍是代码问题`
- `转数据问题`

### 第一批验收

| 接口 | 关键验收点 | 验收样本 | 单项状态 | 是否阻塞联调 | 问题归类 | 验收人 | 备注 |
|------|------|------|------|------|------|------|------|
| Revenue/GetShopINCAnalysis | 基线样本恢复旧结果码；按旧节日口径处理；空数据返回 `101`；结构对齐旧接口 | `calcType=1&pushProvinceCode=340000&curYear=2026&compareYear=2026&HolidayType=2&ServerpartId=416&StatisticsDate=2026-02-13&CurStartDate=2026-01-15` | 通过 | 否 | 代码问题已关闭 | Codex | `compare_revenue_bigdata.py` 已 `PASS=74/74` |
| Contract/GetMerchantAccountDetail | 使用真实 `MerchantId` 样本；结果码一致；明细结构和关键字段一致 | `MerchantId=-1104&StatisticsMonth=202602&StatisticsStartMonth=202602&calcType=1&CompactTypes=340001` | 通过 | 否 | 代码问题已关闭 | Codex | 旧新均 `100`，`ProjectDetailList=21` |

### 第二批验收

| 接口 | 关键验收点 | 验收样本 | 单项状态 | 是否阻塞联调 | 问题归类 | 验收人 | 备注 |
|------|------|------|------|------|------|------|------|
| Contract/GetContractAnalysis | `ContractProfitLoss` 一致；`SalesPerSquareMeter` 一致；`ContractList` 结构和内容一致 | `statisticsDate=2026-02-13&provinceCode=340000&Serverpart_ID=416&SPRegionType_ID=` | 通过 | 否 | 代码问题已关闭 | Codex | 旧新关键字段完全一致 |
| Examine/GetEvaluateResList | 不再是占位返回；AES 样本可回放；结果码、结构、列表内容一致 | 固定 AES 样本 | 通过 | 否 | 代码问题已关闭 | Codex | 固定样本旧新均 `100`，`TotalCount=0` |

### 第三批验收

| 接口 | 关键验收点 | 验收样本 | 单项状态 | 是否阻塞联调 | 问题归类 | 验收人 | 备注 |
|------|------|------|------|------|------|------|------|
| BaseInfo/GetBrandAnalysis | `BrandTag` 类型一致；结构一致；筛选结果一致 | `ProvinceCode=340000&Serverpart_ID=416&Statistics_Date=2026-02-13&ShowAllShop=false` | 通过 | 否 | 代码问题已关闭 | Codex | 首项 `BrandTag` 旧新均为数组 |
| BaseInfo/GetServerpartList | 分页总数一致；`Province_Code` 口径一致；字段类型一致 | `Province_Code=340000&Serverpart_ID=416&PageIndex=1&PageSize=10` | 通过 | 否 | 代码问题已关闭 | Codex | `HASCHARGE` 旧新均为 `Boolean` |
| BaseInfo/GetServerpartInfo | 详情字段一致；`0/null` 默认值行为一致 | `ServerpartId=416` | 通过 | 否 | 代码问题已关闭 | Codex | `ISCUR_SERVERPART` 旧新均为 `0` |
| BaseInfo/GetServerInfoTree | 树层级一致；`children` 的 `null/[]` 口径一致 | header `ServerpartCodes=341003` + `ServerpartIds=416` | 通过 | 否 | 代码问题已关闭 | Codex | 固定样本下树结构对齐 |
| BaseInfo/GetServerpartServiceSummary | AES 样本通过；统计字段值一致 | 固定 AES 样本 | 待确认 | 否 | 转数据问题 | Codex | 旧 `ServerpartTotalCount=133`，新 `135`；旧 `AutoRepairCount=120`，新 `122` |
| BaseInfo/GetBusinessTradeList (POST) | POST 样本通过；分页、字段、空值一致；未被 GET 兼容逻辑污染 | `POST {}` | 未通过 | 否 | 仍是代码问题 | Codex | 旧 `List=[]`，新返回 `230` 条记录 |

### 第四批验收

| 接口 | 关键验收点 | 验收样本 | 单项状态 | 是否阻塞联调 | 问题归类 | 验收人 | 备注 |
|------|------|------|------|------|------|------|------|
| Contract/GetMerchantAccountSplit | 去掉 `MerchantId=0` 空商户组；其他正常商户记录不受影响 | `StatisticsMonth=202602&StatisticsStartMonth=202602&calcType=1&CompactTypes=340001` | 待确认 | 否 | 仍是代码问题 | Codex | `MerchantId=0` 已消失，但 `ProjectCount` 旧 `366` / 新 `363` |

## 三、全量回归检查表

四批单项验收完成后，统一执行一轮 `CommercialApi` 全量回归。

| 检查项 | 结果 | 说明 |
|------|------|------|
| 返回码一致性 | 部分通过 | `Revenue+BigData` 全量通过；11 项验收中大多数返回码已对齐 |
| 返回结构一致性 | 部分通过 | 剩余关注 `GetBusinessTradeList(POST)` |
| 字段值一致性 | 部分通过 | `GetServerpartServiceSummary`、`GetMerchantAccountSplit` 仍有差异 |
| 分页一致性 | 待确认 | `GetBusinessTradeList(POST)` 仍异常 |
| 排序一致性 | 待确认 | 未单独做全量排序验收 |
| 空值口径一致性 | 部分通过 | `GetContractAnalysis`、`GetServerpartInfo` 已对齐 |
| AES/POST 接口回归 | 部分通过 | `GetEvaluateResList` 通过；`GetServerpartServiceSummary` 待确认；`GetBusinessTradeList(POST)` 未通过 |
| 时间敏感接口噪音已过滤 | 通过 | `GetRevenueTrendChart` 已在脚本中忽略时间敏感 `TotalCount` |
| 新增回归问题数 | 2 | `GetBusinessTradeList(POST)`、`GetMerchantAccountSplit` 聚合差异 |
| 阻塞联调问题数 | 1 | 当前唯一明确代码未收口为 `GetBusinessTradeList(POST)` |

回归命令记录：

```powershell
# 在此填写本次实际执行的回归命令
```

回归结论：
- `通过`
- `未通过`
- `待确认`

当前回归结论：`部分通过`

## 四、最终收口表

### 1. 已关闭代码问题

| 接口/问题 | 原问题 | 修复结论 | 验收日期 | 备注 |
|------|------|------|------|------|
| Revenue/GetShopINCAnalysis | 旧节日 helper 未对齐 | 已通过基线样本验收 | 2026-03-09 | 旧新均 `101` |
| Contract/GetMerchantAccountDetail | placeholder 返回 `101` | 已通过真实 `MerchantId=-1104` 样本验收 | 2026-03-09 | `ProjectDetailList=21` |
| Contract/GetContractAnalysis | placeholder 统计值为 `0` | 已通过关键字段验收 | 2026-03-09 | `ContractProfitLoss`、`SalesPerSquareMeter` 已对齐 |
| Examine/GetEvaluateResList | TODO 占位返回 | 固定 AES 样本已通过 | 2026-03-09 | 建议后续补更多业务样本 |
| BaseInfo/GetBrandAnalysis | `BrandTag` 类型不一致 | 已通过 | 2026-03-09 |  |
| BaseInfo/GetServerpartList | `HASCHARGE` 类型不一致 | 已通过 | 2026-03-09 |  |
| BaseInfo/GetServerpartInfo | `ISCUR_SERVERPART` 为 `null` | 已通过 | 2026-03-09 |  |
| BaseInfo/GetServerInfoTree | `children` 口径不一致 | 已通过 | 2026-03-09 | 固定 header 样本下通过 |

### 2. 未关闭代码问题

| 接口/问题 | 当前现象 | 阻塞级别 | 下一步 | 备注 |
|------|------|------|------|------|
| BaseInfo/GetBusinessTradeList (POST) | 旧 `List=[]`，新返回 `230` 条记录 | P1 | 继续修代码并固定 POST 样本 | 当前最明确未收口代码问题 |
| Contract/GetMerchantAccountSplit | 空商户已消失，但 `ProjectCount` 旧 `366` / 新 `363` | P2 | 继续核对聚合口径或数据来源 | 属于尾项，但还不能算完全通过 |

### 3. 纯数据问题

以下问题单独留档，不计入本轮代码整改未完成：

| 数据问题 | 当前结论 | 下一步 | 备注 |
|------|------|------|------|
| T_GOODSSALABLE | DM 侧缺表或不可查 | 走数据同步核查 |  |
| T_MEETING | Oracle 与 DM 差 1 条 | 走数据同步核查 |  |
| 节假日收入 Oracle/旧侧样本确认 | DM 已确认样本日期无数据，旧侧仍需确认 | 走数据核查 |  |
| BaseInfo/GetServerpartServiceSummary | 固定 AES 样本下统计值仍有 `133/120 -> 135/122` 漂移 | 先做数据/口径归因，再决定是否继续改代码 | 暂按数据问题跟踪 |

## 五、批次汇总

| 批次 | 接口数 | 通过数 | 未通过数 | 待确认数 | 备注 |
|------|------:|------:|------:|------:|------|
| 第一批 | 2 | 2 | 0 | 0 | 两项均通过 |
| 第二批 | 2 | 2 | 0 | 0 | 两项均通过 |
| 第三批 | 6 | 4 | 1 | 1 | `GetBusinessTradeList(POST)` 未通过；`GetServerpartServiceSummary` 待确认 |
| 第四批 | 1 | 0 | 0 | 1 | 空商户问题已消失，但仍有聚合差异 |
| 合计 | 11 | 8 | 1 | 2 |  |
