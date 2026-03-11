# Antigravity 多服务区兼容问题回归结果

回归时间：2026-03-09  
回归版本：`97592cb`

## 回归范围

本次只回归之前整理给 `Antigravity` 的 6 条“多服务区 `ServerpartId` 兼容问题”。

对比方式：

- 旧接口：`http://127.0.0.1:8900`
- 新接口：`http://127.0.0.1:8080`

核心验证点：

1. 多服务区参数 `ServerpartId=416,417` 不再返回 `999`
2. 结果码与旧接口一致
3. 关键返回结构或数量与旧接口一致

## 结论总览

- 通过：`4`
- 未通过：`2`

当前结论：

- 6 条问题里，“多服务区传参后直接报错/报 999” 的问题基本已经修掉
- 但 `Examine` 模块里还有 2 条属于“结果码已对齐，但内容仍未对齐”

## 单项结果

| 接口 | 多服务区结果 | 结论 | 说明 |
|---|---|---|---|
| `GET /Revenue/GetShopSABFIList` | 旧 `100`，新 `100` | 通过 | 结果码、总数、树结构字段、层级数量已对齐 |
| `GET /Revenue/GetShopCurRevenue` | 旧 `101`，新 `101` | 通过 | 多服务区不再报 `999` |
| `GET /Examine/GetPatrolAnalysis` | 旧 `200`，新 `200` | 通过 | 多服务区不再报 `999` |
| `GET /Examine/GetExamineAnalysis` | 旧 `100 / TotalCount=3`，新 `100 / TotalCount=0` | 未通过 | 结果码虽对齐，但多服务区查询结果为空 |
| `GET /Examine/GetExamineResultList` | 旧 `100 / TotalCount=124`，新 `100 / TotalCount=0` | 未通过 | 结果码虽对齐，但多服务区查询结果为空 |
| `GET /Examine/GetPatrolResultList` | 旧 `100 / TotalCount=0`，新 `100 / TotalCount=0` | 通过 | 多服务区不再报 `999` |

## 重点说明

### 1. GetShopSABFIList 已通过

本次重点复核了：

- 根节点字段名
- 子节点字段名
- 根节点子级数量
- 第一层子节点下的门店数量

结果：

- 根节点字段一致
- 子节点字段一致
- `TotalCount` 一致
- 根节点 children 数量一致
- 第一层 children 数量一致

说明：

- 这条不仅“参数兼容”已恢复
- 返回树结构也已经基本对齐旧接口

### 2. GetExamineAnalysis 未通过

多服务区样本：

- `DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416,417`

结果：

- 旧接口：`Result_Code=100`，`TotalCount=3`
- 新接口：`Result_Code=100`，`TotalCount=0`

补充验证：

- 单服务区 `ServerpartId=416` 时，旧新都为 `TotalCount=1`

判断：

- 当前不是“单值逻辑整体错”
- 更像“多服务区分支的过滤或组装逻辑仍有问题”

### 3. GetExamineResultList 未通过

多服务区样本：

- `DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416,417`

结果：

- 旧接口：`Result_Code=100`，`TotalCount=124`
- 新接口：`Result_Code=100`，`TotalCount=0`

补充验证：

- 单服务区 `ServerpartId=416`
  - 旧接口：`TotalCount=1`
  - 新接口：`TotalCount=16`

判断：

- 这条不只是“多服务区分支没修完”
- 单服务区内容也没有对齐旧接口
- 说明当前 `ServerpartId` 过滤或列表组装逻辑仍存在更深层问题

## 建议返回给 Antigravity 的整改重点

1. `GET /Examine/GetExamineAnalysis`
   - 继续排查多服务区 ID 条件拼装
   - 重点检查 `IN (...)` 分支是否真正参与查询
   - 重点检查结果过滤和列表组装是否把数据筛空

2. `GET /Examine/GetExamineResultList`
   - 不要只看多服务区
   - 单服务区结果已经与旧接口不一致
   - 重点检查：
     - `ServerpartId` 过滤条件是否正确落表
     - 明细列表组装是否放大了结果
     - 多服务区分支是否错误过滤成空

## 当前可下的结论

- 这一轮回归不能判定“6 条问题全部收口”
- 目前准确状态是：
  - `4/6` 已通过
  - `2/6` 未通过

下一步应该只把未通过的 2 条重新发回 `Antigravity`，不需要整批回滚。
