# CommercialApi 接口平移踩坑记录

> 最后更新: 2026-03-05  
> 适用范围: C# .NET → Python FastAPI 接口平移（Oracle → 达梦）

---

## 一、数据库 Schema 差异

### 坑1: HIGHWAY_SELLDATA 前缀不能用
- **现象**: Customer 接口全部 C=999
- **原因**: C# 代码中 SQL 写 `HIGHWAY_SELLDATA.T_CUSTOMERGROUP`，但达梦中表在 `NEWPYTHON` schema 下，不存在 `HIGHWAY_SELLDATA` schema
- **修复**: 去掉所有 schema 前缀，直接用表名 `T_CUSTOMERGROUP`
- **规则**: **达梦中所有表都在 NEWPYTHON schema 下，SQL 中不要加任何 schema 前缀**

### 坑2: Province_Code 存的是内码不是编码
- **现象**: `GetServerpartList` 传 `Province_Code=340000` 查到 0 条
- **原因**: C# 中 `T_SERVERPART.PROVINCE_CODE` 字段存的是**数据字典内码**（如 3544），不是行政区划编码（340000）
- **C# 做法**: 先通过 `DictionaryHelper.GetFieldEnum("DIVISION_CODE", "340000")` 将编码转为内码 3544，再用内码查
- **修复**: Python 中先查 `T_FIELDENUM` 表获取内码：
  ```sql
  SELECT FIELDENUM_ID FROM T_FIELDENUM WHERE FIELDENUM_VALUE = '340000'
  ```
  340000 → 内码 3544
- **规则**: **凡是涉及 Province_Code 的查询，都要先转内码**

### 坑3: 达梦字段名和 Oracle 不完全一致
- **现象**: SQL 报错 "无效的列名"
- **原因**: C# 中用了 `STATISTIC_TYPE` 字段，但达梦中只有 `STATISTICS_TYPE`（多了个 S）
- **修复**: 每个接口实现前，先查达梦表的实际列名：
  ```sql
  SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = 'T_SERVERPART' AND OWNER = 'NEWPYTHON'
  ```
- **规则**: **不要直接复制 C# 中的字段名，先验证达梦中是否存在该字段**

---

## 二、参数格式差异

### 坑4: C# nullable int 传空字符串不报错，Python 会 422
- **现象**: 大量接口 HTTP 422 Unprocessable Entity
- **原因**: C# Web API 中 `int? Serverpart_ID = null`，前端传空字符串 `""` 时自动忽略。Python FastAPI 用 `Query(...)` 标记必填后，传空字符串会报类型错误
- **修复**: 所有 `int/bool/float` 类型参数都用 `Query(None)` 标记为可选：
  ```python
  Serverpart_ID: Optional[int] = Query(None, description="服务区内码")
  ```
- **规则**: **新 API 参数默认都用 Optional + Query(None)，不要用 Query(...) 标记必填**

### 坑5: AES 加密的 POST 接口
- **现象**: POST 接口的 `value` 字段是 AES 加密字符串，如 `HGNvR1g5B0VGGjJORmEEEgs1DgI...`
- **原因**: C# 中 `ESCG.AES.AESUtil.ToSimplifyDecrypt(postData.value)` 先解密再提取参数
- **状态**: 需要用相同的 AES 密钥和算法实现解密
- **规则**: **POST 接口的 value 字段必须先 AES 解密才能获取真实参数**
- **涉及接口**: `GetServerpartTypeAnalysis`, `GetServerpartServiceSummary`, `GetBrandStructureAnalysis`, `GetRevenueTrendChart` 等

### 坑6: Serverpart_ID vs ServerpartId 是两个不同参数
- **现象**: `GetServerpartList` 只返回 1 条
- **原因**: C# 中 `Serverpart_ID` 是"当前服务区内码"（用于计算距离排序），`ServerpartId` 才是 WHERE 过滤条件。代码把 `Serverpart_ID` 错当成了过滤条件
- **修复**: 区分参数名的含义：
  - `Serverpart_ID` (带下划线) → 仅用于标记当前服务区，不加 WHERE
  - `ServerpartId` (无划线) → 用于 WHERE 过滤 `A.SERVERPART_ID IN (...)`
- **规则**: **仔细看 C# 参数名，哪些参与 WHERE，哪些不参与**

---

## 三、路由映射差异

### 坑7: BigData 旧接口路由前缀是 Revenue/ 不是 BigData/
- **现象**: 9 个 BigData 卡口接口旧 API 404
- **原因**: C# `BigDataController` 中卡口接口的 `[Route]` 写的是 `Revenue/GetBayonetXxx`，不是 `BigData/GetBayonetXxx`
- **修复**: 在 `baseline_collect.py` 中加路由映射表 `OLD_ROUTE_MAP`：
  ```python
  OLD_ROUTE_MAP = {
      "GET:/BigData/GetBayonetSTAList": "GET:/Revenue/GetBayonetSTAList",
      ...
  }
  ```
- **规则**: **新旧 API 路由前缀可能不一致，实现前先确认 C# 的 [Route] 标注**

---

## 四、数据同步差异

### 坑8: 达梦与 Oracle 数据时间范围不一致
- **现象**: Customer 接口 T=0（旧 API 有数据）
- **原因**: 达梦 T_CUSTOMERGROUP 中 SERVERPART_ID=416 的数据最新到 202512，没有 202602 的数据。旧 API 用 Oracle 有 202602 数据
- **修复**: 不传 `serverpartId` 改查全省，或改用达梦中有数据的条件
- **规则**: **测试参数中的日期和 ID 要确保在达梦中有对应数据**

### 坑9: 测试用的实体 ID 在达梦中不存在
- **现象**: `GetPATROLDetail` C=101, `GetEXAMINEDetail` C=101
- **原因**: 测试参数用了 `PATROLId=10`, `ExamineId=10`，达梦中最小 ID 是 687379 和 999
- **修复**: 先查达梦中的有效 ID：
  ```sql
  SELECT PATROL_ID FROM T_PATROL ORDER BY PATROL_ID DESC FETCH FIRST 5 ROWS ONLY
  ```
- **规则**: **实现接口前先验证测试参数中的 ID 在达梦中是否存在**

### 坑10: 表名确实存在但脚本以为不存在
- **现象**: 误判"达梦表缺失"导致接口 T=0
- **原因**: C# 代码中引用的表名是 `T_BAYONETDAILY_AH`（实际存在），但分析脚本找的是 `T_BAYONET_STA`（自己编的名字）
- **修复**: 以 C# Helper 代码中的 SQL 表名为准，不要猜测
- **规则**: **永远回到 C# 源码确认表名，不要凭猜测**

---

## 五、返回值格式差异

### 坑11: C# 返回码含义不同于 HTTP 状态码
- **C=100**: 查询成功（有数据）
- **C=101**: 查询成功但无数据（部分接口用 101 表示"无记录"）
- **C=200**: 部分接口用 200 表示"查询失败/无数据"（不是 HTTP 200）
- **C=999**: 查询异常
- **规则**: **新 API 统一用 100=成功(有数据), 101=成功(无数据), 999=异常**

### 坑12: TotalCount 含义不统一
- **现象**: 旧 API `GetServerpartList` T=10（实际 144 条），新 API T=144
- **原因**: 旧 API 部分接口的 `TotalCount` 返回的是分页后的数量，不是总数
- **规则**: **对比时注意旧 API 的 T 可能是页内数量而非总数**

### 坑13: serverpartId 为空时要走不同的查询逻辑
- **现象**: Customer 接口 T=0
- **原因**: C# 中 `serverpartId` 为 null 时不加 WHERE 条件（查全省汇总），新 API 代码直接写死 `WHERE SERVERPART_ID = :serverpartId` 导致 NULL 匹配不到任何行
- **修复**: 动态构建 WHERE 条件：
  ```python
  if serverpartId:
      conditions.append("SERVERPART_ID = :serverpartId")
      params["serverpartId"] = serverpartId
  ```
- **规则**: **所有可选参数都要动态拼 WHERE，不传就不加条件**

---

## 六、测试流程最佳实践

### 实现新接口前的检查清单
1. ✅ 读 C# Controller 确认路由、HTTP 方法、参数定义
2. ✅ 读 C# Helper 确认 SQL 用了哪些表、字段名
3. ✅ 查达梦确认表存在、字段名一致
4. ✅ 查达梦确认测试参数有对应数据
5. ✅ 检查是否涉及 Province_Code 内码转换
6. ✅ 检查是否涉及 AES 加密
7. ✅ 检查参数名含义（是过滤条件还是辅助标记）
8. ✅ 所有参数用 `Optional + Query(None)` 可选

### 对比测试后的排查顺序
1. 先看是否 HTTP 422 → 参数类型问题
2. 再看是否 C=999 → SQL 报错，查日志
3. 再看是否 T=0 → SQL 条件不对或表/字段名错误
4. 再看是否 C=101 → 测试数据 ID 不存在
5. 最后看 T 数量差异 → 分页逻辑或 WHERE 条件差异

---

## 七、关键表的 Schema 来源映射

| 达梦表名 | Oracle Schema | 说明 |
| :--- | :--- | :--- |
| T_SERVERPART | HIGHWAY_STORAGE | 服务区主表 |
| T_SERVERPARTSHOP | HIGHWAY_STORAGE | 服务区门店 |
| T_RTSERVERPART | HIGHWAY_STORAGE | 服务区扩展信息 |
| T_SERVERPARTINFO | HIGHWAY_STORAGE | 设施服务信息 |
| T_CUSTOMERGROUP | HIGHWAY_SELLDATA | 客群统计 |
| T_CUSTOMER_AGE | HIGHWAY_SELLDATA | 客群年龄 |
| T_CUSTOMER_CONSUME | HIGHWAY_SELLDATA | 客群消费 |
| T_CUSTOMER_GAC | HIGHWAY_SELLDATA | 客群特征 |
| T_BUDGETPROJECT_AH | FINANCE_STORAGE | 预算项目 |
| T_BUDGETDETAIL_AH | FINANCE_STORAGE | 预算明细 |
| T_REGISTERCOMPACT | CONTRACT_STORAGE | 合同主表 |
| T_BAYONETDAILY_AH | HIGHWAY_SELLDATA | 卡口日报 |
| T_REVENUEDAILY | HIGHWAY_SELLDATA | 营收日报 |
| T_FIELDENUM | 数据字典 | Province_Code 内码转换 |

> **重要**: 达梦中所有表统一在 NEWPYTHON schema 下，SQL 不加 schema 前缀！
---

## 八、Validation And Comparison Pitfalls

### 坑13: 旧 API 不可用时不能直接怪 Python
- **发现日期**: `2026-03-09`
- **适用范围**: 所有新旧接口对比脚本
- **现象**: 旧 API 返回 `TIMEOUT`、`HTTP404` 或其他不可用状态时，容易把新 API 的任意结果误判成代码差异
- **根因**: 对比前提被破坏，旧侧已经不是可用基线
- **错误做法**: 把这类 case 继续记入 blocker 或代码问题
- **正确做法**: 统一标记为 `SKIP`，并从当日 blocker 列表剔除
- **是否通用**: 是
- **是否已纳入工作流**: 是

### 坑14: 失效脚本样例会制造 422 噪声
- **发现日期**: `2026-03-09`
- **适用范围**: 所有依赖历史脚本样例的验收任务
- **现象**: 旧 API 已 `HTTP404` 的历史样例，在新 API 侧常表现为 `HTTP422`，看起来像参数绑定问题
- **根因**: 样例本身已经不再是有效的同口径对比样例
- **错误做法**: 直接把新 API 的 `HTTP422` 记为路由缺陷
- **正确做法**: 将该样例标记为 stale case，移出当前验收与 blocker 统计
- **是否通用**: 是
- **是否已纳入工作流**: 是
