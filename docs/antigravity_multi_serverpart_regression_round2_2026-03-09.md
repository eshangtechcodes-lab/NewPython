# Antigravity 多服务区兼容问题二次复验结果

复验时间：2026-03-09  
复验版本：`97592cb`

## 本轮范围

上一轮回归后未通过的 2 条：

- `GET /Examine/GetExamineAnalysis`
- `GET /Examine/GetExamineResultList`

本轮同时复验：

- 单服务区样本：`ServerpartId=416`
- 多服务区样本：`ServerpartId=416,417`

## 本轮结论

- `GET /Examine/GetExamineAnalysis`：通过
- `GET /Examine/GetExamineResultList`：未通过

更新后的整批状态：

- 多服务区兼容问题总计：`6`
- 已通过：`5`
- 未通过：`1`

## 复验明细

### 1. GET /Examine/GetExamineAnalysis

#### 单服务区

- 旧接口：`Result_Code=100`，`TotalCount=1`，`List.Count=1`
- 新接口：`Result_Code=100`，`TotalCount=1`，`List.Count=1`

#### 多服务区

- 旧接口：`Result_Code=100`，`TotalCount=3`，`List.Count=3`
- 新接口：`Result_Code=100`，`TotalCount=3`，`List.Count=3`

结论：

- 本条已收口

### 2. GET /Examine/GetExamineResultList

#### 单服务区

- 样本：`DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416`
- 旧接口：`Result_Code=100`，`TotalCount=1`，`List.Count=1`
- 新接口：`Result_Code=100`，`TotalCount=2`，`List.Count=2`

#### 多服务区

- 样本：`DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416,417`
- 旧接口：`Result_Code=100`，`TotalCount=124`，`List.Count=124`
- 新接口：`Result_Code=100`，`TotalCount=141`，`List.Count=141`

结论：

- 本条仍未收口
- 当前不是“查少了”，而是“查多了”

## 关键差异判断

### GetExamineResultList 的问题不是单纯多服务区兼容

单服务区已经出现差异：

- 旧接口 `1`
- 新接口 `2`

这说明当前问题不只是多值 `ServerpartId` 分支。

### 当前返回口径仍未对齐旧接口

旧接口首项字段：

- `SPREGIONTYPE_ID`
- `SPREGIONTYPE_NAME`
- `SPREGIONTYPE_INDEX`
- `SERVERPART_ID`
- `SERVERPART_INDEX`
- `SERVERPART_NAME`
- `SERVERPART_TAG`
- `EXAMINE_MQUARTER`
- `EXAMINE_DESC`
- `list`

新接口首项字段：

- `EXAMINE_ID`
- `SPREGIONTYPE_ID`
- `SPREGIONTYPE_NAME`
- `SERVERPART_ID`
- `SERVERPART_NAME`
- `SERVERPART_REGION`
- `EXAMINE_MYEAR`
- `EXAMINE_MONTH`
- `EXAMINE_COUNT`
- `EXAMINE_MQUARTER`
- `EXAMINE_SCORE`
- `EXAMINE_LINENUM`
- `EXAMINE_PERSON`
- `EXAMINE_DATE`
- `EXAMINE_TYPE`
- `EXAMINE_GUID`
- `EXAMINE_STATE`
- `EXAMINE_STAFFID`
- `EXAMINE_STAFFNAME`
- `EXAMINE_OPERATEDATE`
- `EXAMINE_DESC`

判断：

- 旧接口返回的是“按服务区聚合后的树形结果”
- 新接口当前返回的是“`T_EXAMINE` 主表明细列表”
- 因此这条的本质问题是：
  - 返回口径没对齐旧接口
  - 不只是 `ServerpartId` 多值解析问题

## 代码观察

当前实现位置：

- `routers/commercial_api/examine_router.py:732`

当前实现特征：

- 单值只处理了 `len(_sp_ids) == 1`
- 多值没有显式补 `IN (...)`
- 查询直接 `SELECT A.*`
- 返回直接把 `rows` 输出为列表

关键代码段：

- `routers/commercial_api/examine_router.py:786`
- `routers/commercial_api/examine_router.py:805`
- `routers/commercial_api/examine_router.py:810`

当前判断：

1. 多服务区过滤条件没有完整落地
2. 即使单服务区命中过滤，返回模型也仍不是旧接口的聚合树结构

## 下一步建议发回 Antigravity

只回修这一条：

- `GET /Examine/GetExamineResultList`

整改要求：

1. 不要继续在当前 `SELECT A.*` 明细列表上小修小补
2. 需要重新对齐旧接口返回口径
3. 需要同时修正：
   - 单服务区结果数量
   - 多服务区结果数量
   - 返回字段模型
   - 聚合层级结构

## 当前最终状态

- `GET /Revenue/GetShopSABFIList`：通过
- `GET /Revenue/GetShopCurRevenue`：通过
- `GET /Examine/GetPatrolAnalysis`：通过
- `GET /Examine/GetExamineAnalysis`：通过
- `GET /Examine/GetPatrolResultList`：通过
- `GET /Examine/GetExamineResultList`：未通过
