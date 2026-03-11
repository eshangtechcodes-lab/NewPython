# Antigravity 多服务区兼容问题三次复验结果

复验时间：2026-03-09  
复验版本：`3290d27`

## 本轮结论

- 总问题数：`6`
- 已通过：`5`
- 未通过：`1`

当前唯一未通过接口：

- `GET /Examine/GetExamineResultList`

## 其余 5 条通过情况

| 接口 | 旧接口 | 新接口 | 结论 |
|---|---|---|---|
| `GET /Revenue/GetShopSABFIList` | `100 / TotalCount=1 / List=1` | `100 / TotalCount=1 / List=1` | 通过 |
| `GET /Revenue/GetShopCurRevenue` | `101` | `101` | 通过 |
| `GET /Examine/GetPatrolAnalysis` | `200` | `200` | 通过 |
| `GET /Examine/GetExamineAnalysis` | `100 / TotalCount=3 / List=3` | `100 / TotalCount=3 / List=3` | 通过 |
| `GET /Examine/GetPatrolResultList` | `100 / TotalCount=0 / List=0` | `100 / TotalCount=0 / List=0` | 通过 |

## 未通过项

### GET /Examine/GetExamineResultList

#### 单服务区

样本：

- `DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416`

结果：

- 旧接口：`Result_Code=100`，`TotalCount=1`，`List.Count=1`
- 新接口：`Result_Code=100`，`TotalCount=2`，`List.Count=2`

#### 多服务区

样本：

- `DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416,417`

结果：

- 旧接口：`Result_Code=100`，`TotalCount=124`，`List.Count=124`
- 新接口：`Result_Code=100`，`TotalCount=141`，`List.Count=141`

结论：

- 本条仍未收口
- 当前不是“查少了”，而是“查多了”

## 当前定位到的具体问题

### 1. 多服务区分支没有真正落过滤

当前代码：

- `routers/commercial_api/examine_router.py:786`
- `routers/commercial_api/examine_router.py:805`

可见逻辑：

- 只处理了 `len(_sp_ids) == 1`
- 没有为多服务区显式补 `IN (...)`

因此当传 `ServerpartId=416,417` 时：

- 没有真正按这两个服务区过滤
- 结果被放大到 `141`

### 2. 顶层字段名虽然对齐了，但嵌套 `list` 口径仍未对齐

旧接口顶层字段：

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

新接口顶层字段：

- 已与旧接口一致

但 `list` 内部结构不一致：

- 旧接口 `list[0]` 字段：
  - `REGION_NAME`
  - `EXAMINE_SCORE`
  - `SERVERPARTList`
- 新接口 `list[0]` 字段：
  - `EXAMINEDETAIL_ID`
  - `EXAMINE_POSITION`
  - `EXAMINE_CONTENT`
  - `DEDUCTION_REASON`
  - `DEDUCTION_SCORE`
  - `EXAMINEDETAIL_DESC`
  - `EXAMINEDETAIL_URL`
  - `EXAMINEDEAL_URL`

说明：

- 旧接口 `list` 存的是“区域分组 + SERVERPARTList”
- 新接口 `list` 存的是“考核明细 DetailList”

也就是说：

- 现在只是把顶层字段名改像了
- 但内部层级和语义仍不是旧接口口径

### 3. 单服务区仍偏大，也说明不是纯多值问题

单服务区 `ServerpartId=416`：

- 旧接口：`1`
- 新接口：`2`

说明当前还有：

- 聚合口径不一致
- 或组装层级不一致

## 建议返回给 Antigravity 的结论

当前不要再把这条当成“多服务区兼容小修补”。

正确处理方式应该是：

1. 补齐多服务区 `IN (...)` 过滤
2. 按旧接口重新组装 `list`
   - `list` 里应该是 `REGION_NAME + EXAMINE_SCORE + SERVERPARTList`
   - `SERVERPARTList` 里再挂 `DetailList`
3. 单服务区和多服务区都重新按旧接口验收

## 当前可下的最终判断

- 这批问题不能判定为 `6/6` 通过
- 当前准确状态仍是：
  - `5/6` 已通过
  - `1/6` 未通过
