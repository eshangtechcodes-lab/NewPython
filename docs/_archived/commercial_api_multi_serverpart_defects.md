# CommercialApi 多服务区 ID 兼容问题清单

更新时间：2026-03-09

## 背景

前端在部分页面会把多个服务区内码以逗号分隔形式传入 `ServerpartId` / `serverPartId`，例如：

- `ServerpartId=416,417`

旧 C# 接口在部分路由上支持这种调用方式；当前 Python 平移版有一批接口仍按“单个整型 ID”处理，导致：

- SQL 被拼成 `= 416,417`，DM 直接报语法错
- 或代码执行 `int("416,417")`，直接抛异常
- 最终统一表现为 `Result_Code=999`

本清单只整理“旧接口支持多服务区 ID、但新接口不兼容”的同类问题，供 `Antigravity` 一次性修复。

## 已确认缺陷

| 序号 | 接口 | 复现参数 | 旧接口结果 | 新接口结果 | 根因 |
|---|---|---|---|---|---|
| 1 | `GET /Revenue/GetShopSABFIList` | `pushProvinceCode=340000&StatisticsMonth=202602&ServerpartId=416,417&BusinessTradeType=&BusinessTrade=` | `100` | `999` | SQL 仍写成 `A."SERVERPART_ID" = 416,417`，且响应组装里直接 `int(ServerpartId)` |
| 2 | `GET /Revenue/GetShopCurRevenue` | `serverPartId=416,417&statisticsDate=2026-02-14` | `101` | `999` | SQL 仍写成 `A."SERVERPART_ID" = 416,417` |
| 3 | `GET /Examine/GetPatrolAnalysis` | `provinceCode=340000&ServerpartId=416,417&StartDate=2026-01-15&EndDate=2026-02-13` | `200` | `999` | 代码执行 `int(ServerpartId)` |
| 4 | `GET /Examine/GetExamineAnalysis` | `DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416,417` | `100` | `999` | 代码执行 `int(ServerpartId)` |
| 5 | `GET /Examine/GetExamineResultList` | `DataType=1&StartMonth=202502&EndMonth=202502&provinceCode=340000&ServerpartId=416,417` | `100` | `999` | 代码执行 `int(ServerpartId)` |
| 6 | `GET /Examine/GetPatrolResultList` | `provinceCode=340000&ServerpartId=416,417&StartDate=2026-01-15&EndDate=2026-02-13` | `100` | `999` | 代码执行 `int(ServerpartId)` |

## 代码定位

### 1. Revenue/GetShopSABFIList

文件：

- `routers/commercial_api/revenue_router.py:6535`

关键问题点：

- `routers/commercial_api/revenue_router.py:6561`
  - `where_sql += f' AND A."SERVERPART_ID" = {ServerpartId}'`
- `routers/commercial_api/revenue_router.py:6593`
  - `"ServerpartId": int(ServerpartId) if ServerpartId else None`
- `routers/commercial_api/revenue_router.py:6607`
  - `"ServerpartId": int(ServerpartId) if ServerpartId else None`

补充说明：

- 这条不只是“多 ID 报 999”。
- 当前 Python 返回结构也没有对齐旧 C#。
- 旧接口根节点/子节点字段包含：
  - `RevenueINC`
  - `AccountINC`
  - `BayonetINC`
  - `SectionFlowINC`
  - `TicketINC`
  - `AvgTicketINC`
  - `ShopINCList`
- 当前 Python 只有：
  - `ServerpartShopId`
  - `ServerpartShopName`
  - `RevenueAmount`
  - `TicketCount`

因此这条修复不能只把 `=` 改成 `IN`，还要把返回树结构对齐旧接口。

### 2. Revenue/GetShopCurRevenue

文件：

- `routers/commercial_api/revenue_router.py:3454`

关键问题点：

- `routers/commercial_api/revenue_router.py:3479`
  - `WHERE A."VALID" = 1 AND A."SERVERPART_ID" = {serverPartId}`

### 3. Examine/GetPatrolAnalysis

文件：

- `routers/commercial_api/examine_router.py:594`

关键问题点：

- `routers/commercial_api/examine_router.py:609`
  - `conditions.append("B.\"SERVERPART_ID\" = ?")`
- `routers/commercial_api/examine_router.py:610`
  - `params.append(int(ServerpartId))`

### 4. Examine/GetExamineAnalysis

文件：

- `routers/commercial_api/examine_router.py:665`

关键问题点：

- `routers/commercial_api/examine_router.py:684`
  - `conditions.append("B.\"SERVERPART_ID\" = ?")`
- `routers/commercial_api/examine_router.py:685`
  - `params.append(int(ServerpartId))`

### 5. Examine/GetExamineResultList

文件：

- `routers/commercial_api/examine_router.py:732`

关键问题点：

- `routers/commercial_api/examine_router.py:751`
  - `conditions.append("B.\"SERVERPART_ID\" = ?")`
- `routers/commercial_api/examine_router.py:752`
  - `params.append(int(ServerpartId))`

### 6. Examine/GetPatrolResultList

文件：

- `routers/commercial_api/examine_router.py:788`

关键问题点：

- `routers/commercial_api/examine_router.py:808`
  - `conditions.append('B."SERVERPART_ID" = ?')`
- `routers/commercial_api/examine_router.py:809`
  - `params.append(int(ServerpartId))`

## 统一整改方案

建议 `Antigravity` 把这 6 条按一个问题族统一处理，不要逐条零散修。

### 统一规则

1. 对所有“旧接口支持多服务区 ID”的路由：
   - 先把 `ServerpartId` / `serverPartId` 解析成整数列表
   - 过滤空串、空格、非法字符
   - 保留原有顺序即可

2. 查询条件统一按列表长度分流：
   - 单个 ID：允许继续用 `=`
   - 多个 ID：必须改成 `IN (...)`

3. 禁止直接做：
   - `int(ServerpartId)`
   - `int(serverPartId)`
   - `A."SERVERPART_ID" = {ServerpartId}` 当 `ServerpartId` 可能是逗号串

4. 如果前端传了空值或解析后没有合法 ID：
   - 返回旧接口兼容结果
   - 不要落成 `999`

5. 修完后必须用“多服务区 ID”样本回归，而不是只测单个 ID。

### GetShopSABFIList 的额外要求

这条不能只修参数兼容，还必须同步处理：

1. 返回树结构对齐旧 C#
2. 根节点、服务区节点、门店节点字段名对齐旧接口
3. 根节点 `ServerpartId` / `ServerpartName` 行为对齐旧接口
4. 不要保留当前简化版 `RevenueAmount` / `TicketCount` 结构作为最终返回

## 明确排除项

### Revenue/GetShopINCAnalysis 不属于这批问题

复核结果：

- 旧接口对 `ServerpartId=416,417` 直接返回 `400`
- 当前 Python 返回 `422`

说明：

- 旧 C# 本身就按单个 `Int32 ServerpartId` 设计
- 这条不能按“多服务区兼容缺陷”处理
- 除非业务明确要求扩展能力，否则不要顺手改成支持多值

## 建议交付给 Antigravity 的执行顺序

1. 先统一封装 `ServerpartId` 多值解析规则
2. 先修 `Examine` 四条
   - 这四条根因一致，收敛最快
3. 再修 `Revenue/GetShopCurRevenue`
4. 最后修 `Revenue/GetShopSABFIList`
   - 因为这条除了多值兼容，还有返回结构未对齐问题

## 验收建议

每条至少验这两类样本：

1. 单服务区
   - 如 `ServerpartId=416`
2. 多服务区
   - 如 `ServerpartId=416,417`

验收标准：

- 不再返回 `999`
- 结果码与旧接口一致
- 返回结构与旧接口一致
- `GetShopSABFIList` 额外要求字段模型完全对齐旧接口
