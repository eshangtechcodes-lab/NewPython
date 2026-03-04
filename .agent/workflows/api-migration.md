---
description: C# API 接口平移到 Python FastAPI 的标准工作流
---

# API 接口迁移工作流

> 适用于 EShangApi C# → Python FastAPI 的逐接口迁移。每迁移一个接口，严格按以下 5 步执行。

## 前置条件

- 原 C# API 服务已启动（`http://192.168.1.99:8900`）
- 新 Python API 服务已启动（`http://localhost:8080`）
- 原项目代码路径：`E:\workfile\JAVA\API\CSharp`
- Helper 层代码路径：`E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\`
- Model 代码路径：`E:\workfile\JAVA\API\CSharp\EShangApi.Common\Model\`
- Python 版本：3.8（注意类型注解兼容性，需 `from __future__ import annotations`）
- 达梦用户 NEWPYTHON 无 CREATE SEQUENCE 权限（新增时使用 MAX(ID)+1 降级方案）
- Oracle 可从本机直连（Thick 模式，Instant Client 路径：`E:\workfile\JAVA\NewAPI\oracle_client`）
- 已知 Oracle schema：`COOP_MERCHANT`（业主相关）、`HIGHWAY_STORAGE`（服务区相关）

---

## 第一步：读原代码（只读不写）

// turbo-all

### 1.1 定位原 Controller

在原 C# 项目中找到对应的 Controller 文件，确认：

- **路由路径**：`[Route("BaseInfo/GetXxxList")]` 的确切大小写拼写
- **入参格式**：是 `SearchModel<T>` 直接 JSON，还是 `CommonModel`（AES 加密的 `value`）
- **HTTP 方法**：POST / GET

```
# 示例：查找 BRAND 相关的 Controller
搜索路径：EShangApiMain/Controllers/ 或 EShangApiMain/Areas/
搜索关键词：GetBrandList 或 BRAND
```

### 1.2 定位原 Helper（Service 层）

找到对应的 Helper 文件，确认：

- **SQL 查询语句**：完整的 SELECT（含 JOIN、子查询）
- **默认排序**：ORDER BY 子句
- **默认分页**：不传参数时的默认行为（通常默认 10 条）
- **关联表**：JOIN 了哪些表，额外拼接了哪些字段

```
# 示例：查找 BRAND 的业务逻辑
搜索路径：EShangApi.Common/GeneralMethod/BaseInfo/
搜索关键词：GetBrandList 或 T_BRAND
# 注意：实际 SQL 在 Business 类的 FillDataTable(WhereSQL) 中
# FillDataTable 等价于 SELECT * FROM T_XXX {WhereSQL}
```

### 1.3 定位原 Model

确认返回的字段列表和类型（int / string / datetime / 嵌套对象）。

---

## 第二步：调原 API 获取基准数据

### 2.1 调用原接口记录基准响应

用空参数 `{}` 调用原接口，保存完整 JSON 响应作为基准：

```powershell
# 获取基准数据
Invoke-RestMethod -Uri "http://localhost:8900/EShangApiMain/BaseInfo/GetXxxList" -Method Post -Body '{}' -ContentType 'application/json' | ConvertTo-Json -Depth 10 > scripts/baseline/xxx_list_baseline.json
```

### 2.2 记录关键指标

从基准响应中提取并记录：

| 指标 | 值 |
|------|-----|
| Result_Code | ? |
| TotalCount | ? |
| List 条数 | ?（不传参数时的默认值） |
| PageIndex 默认值 | ? |
| PageSize 默认值 | ? |
| 字段列表 | [完整字段名列表] |
| 第一条数据排序依据 | ?（确认默认排序） |
| 字段类型 | int? string? datetime? |

---

## 第三步：同步数据库表

> Oracle 已可从本机直连，迁移脚本直接在本机执行即可。

### 3.1 修改迁移脚本

修改 `scripts/server_migrate.py` 中的 MIGRATE_TABLES 列表，添加要迁移的表：

```python
# 已知 Oracle schema 映射：
# COOP_MERCHANT  → 业主相关表（T_OWNERUNIT 等）
# HIGHWAY_STORAGE → 服务区相关表（T_SERVERPART、T_SERVERPARTSHOP 等）
MIGRATE_TABLES = [
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_XXX", "sequence": "SEQ_XXX"},
]
```

### 3.2 在本机执行迁移

// turbo
```powershell
python scripts/server_migrate.py
```

脚本会自动：
1. 读 Oracle 表结构
2. 在达梦建表
3. **从 Oracle 同步表注释和字段注释到达梦**
4. 迁移数据（每 500 条批量提交）
5. 校验行数

> **注意**：序列创建可能因权限不足失败，脚本已做降级处理（仅警告不中断）。

---

## 第四步：实现 Python 接口

按照第一步读取的原代码，创建以下文件：

### 4.1 Model（若尚不存在）

文件按模块分目录：`models/{模块名}/xxx.py`
- BaseInfo 模块 → `models/base_info/ownerunit.py`

规范：
- 使用 Pydantic BaseModel
- 文件头加 `from __future__ import annotations`（Python 3.8 兼容）
- 字段名与原 C# Model 完全一致
- 所有字段使用 `Optional[类型] = None`
- 中文注释标注字段含义

### 4.2 Service

文件：`services/{模块名}/xxx_service.py`

- 文件头加 `from __future__ import annotations`（Python 3.8 兼容）
- **SQL 必须参考原 Helper 中的查询**，不能自己猜测
- 包含 JOIN、默认排序、默认分页逻辑
- 保持与原 Helper 完全一致的业务行为
- **新增逻辑**：序列不可用时降级为 `MAX(ID)+1`
- **删除逻辑**：注意区分软删除和真删除
  - 软删除：`UPDATE SET XXX_STATE = 0`（如 OWNERUNIT）
  - 真删除：`DELETE FROM`（如 SERVERPART，原 C# `_SERVERPART.Delete()`）
  - 必须阅读原 Helper 的 Delete 方法确认

### 4.3 Router

文件：`routers/eshang_api_main/{模块名}/xxx_router.py`

- 路由路径与原 Controller 完全一致（注意大小写）
- HTTP 方法与原 Controller 一致（注意 Delete 可能同时支持 GET+POST，用 `@router.api_route(methods=["GET", "POST"])`）
- GetDetail 通常是 GET 方法，参数通过 `Query()` 接收
- 入参格式与原 Controller 一致
- 新建模块目录时，需创建 `__init__.py`
- 在 `main.py` 中注册路由时加 `prefix="/EShangApiMain"` 和对应 `tags`

---

## 第五步：对比验证

### 5.1 运行对比脚本

修改 `scripts/compare_api.py`，替换为当前接口的路径，然后执行：

```powershell
python scripts/compare_api.py
```

### 5.2 对比清单（全部 ✅ 才算通过）

| 检查项 | 要求 |
|--------|------|
| Result_Code | 一致 |
| Result_Desc | 一致 |
| TotalCount | 一致 |
| List 条数 | 一致（默认分页行为相同） |
| PageIndex / PageSize | 一致 |
| 字段列表 | 完全一致（无缺失、无多余） |
| 字段值类型 | 一致（int/string/null） |
| 排序 | 第一条数据相同 |
| 空值处理 | null 的字段一致 |

### 5.3 提交代码

```powershell
git add -A
git commit -m "feat: 迁移 XxxList 接口 - 对比验证通过"
git push
```

---

## 注意事项

1. **绝不假设入参格式**，必须看原 Controller 代码确认
2. **绝不假设 SQL 查询**，必须看原 Helper 代码中的完整 SQL
3. **绝不假设默认行为**，必须先调用原 API 确认
4. **字段顺序不重要**，但字段名、类型、值必须完全一致
5. **每完成一个接口就提交一次 Git**，保持原子性
6. **遇到新问题必须记录**，更新本工作流和问题日志

---

## 第六步：问题标注与经验积累

> **核心原则**：遇到的每个问题都是后续迁移的宝贵经验。必须记录，不能只修复就跳过。

### 6.1 记录问题到日志

在 `docs/migration_issues.md` 中追加记录，格式如下：

```markdown
### [接口名] 问题描述
- **发现时间**: 2026-03-04
- **问题分类**: [数据类型 | SQL差异 | 入参格式 | 字段缺失 | 排序差异 | 分页行为 | 数据库兼容 | 其他]
- **现象**: 描述原API和新API的具体差异
- **根因**: 分析为什么会出现这个差异
- **解决方案**: 具体的修复方式
- **是否通用**: 是/否（其他接口是否会遇到同样问题）
- **预防措施**: 后续如何避免（如需要，更新工作流步骤）
```

### 6.2 更新工作流

如果问题具有通用性（标记"是否通用: 是"），必须将预防措施补充到本工作流对应步骤中。

### 6.3 更新已知问题速查表

每次遇到新的通用问题，追加到下方速查表。

---

## 已知问题速查表

> 迁移过程中积累的通用问题和解决方案。每次遇到新问题，在此追加。

### 🔴 P1: 数据类型不一致

**现象**: 达梦返回 `"BRAND_ID": "1"`（字符串），原 API 返回 `"BRAND_ID": 1`（整数）
**根因**: 达梦导入工具将 Oracle 的 NUMBER 列导为 VARCHAR
**解决方案**: 
- 方案A: 在达梦中修改列类型 `ALTER TABLE T_XXX MODIFY COLUMN_NAME INT`
- 方案B: 在 Python Service 层做类型转换
**检查时机**: 第三步 3.2（字段类型校验）

### 🔴 P2: 关联字段缺失

**现象**: 原 API 返回 `BUSINESSTRADE_NAME`、`ServerpartList` 等字段，新 API 没有
**根因**: 原 C# Helper 中的 SQL 包含 JOIN 其他表，而新接口只做了 `SELECT * FROM T_XXX`
**解决方案**: 必须在第一步 1.2 中完整阅读原 Helper 的 SQL，包含所有 JOIN 和子查询
**检查时机**: 第一步 1.2（定位原 Helper）

### 🟡 P3: 默认分页行为

**现象**: 原 API 不传分页参数时默认返回 10 条，新 API 返回全部
**根因**: 未阅读原 C# 的默认分页逻辑就实现
**解决方案**: 不传参时 `PageIndex=0, PageSize=0`，默认用 `ROWNUM <= 10` 限制
**检查时机**: 第一步 1.2（确认默认分页）+ 第二步 2.2（记录 List 条数）

### 🟡 P4: 路由路径大小写

**现象**: 写成 `GetBRANDList` 而非 `GetBrandList`
**根因**: 按表名猜测路由，未看原 Controller 代码
**解决方案**: 必须看原 Controller 的 `[Route]` 注解
**检查时机**: 第一步 1.1（确认路由路径）

### 🟡 P5: 入参加密方式判断错误

**现象**: 以为所有接口都用 AES 加密的 CommonModel.value，实际 AutoBuild 接口用直接 JSON
**根因**: 未区分 AutoBuild Controller 和手动 Controller 的入参差异
**解决方案**: AutoBuild 生成的 Controller 通常用 `SearchModel<T>` 直接接收 JSON；手动 Controller 才用 `CommonModel` + AES
**检查时机**: 第一步 1.1（确认入参格式）

### 🟢 P6: 排序差异

**现象**: 原 API 第一条是「艾比克」，新 API 第一条是「业主品牌」
**根因**: 原 SQL 有默认 ORDER BY，新 SQL 没有
**解决方案**: 阅读原 Helper 的 SQL，复制其 ORDER BY 逻辑
**检查时机**: 第一步 1.2（确认默认排序）

### 🟢 P7: Oracle → 达梦 SQL 语法兼容

**现象**: 部分 Oracle 特有语法在达梦中不兼容
**解决方案**: 达梦兼容大部分 Oracle 语法（ROWNUM、SYSDATE、NVL、DECODE），但需注意：
- `(+)` 外连接语法 → 改用 `LEFT JOIN`
- `CONNECT BY` 树形查询 → 改用 `WITH RECURSIVE` 或达梦的 `START WITH`
- `LISTAGG` → 达梦支持 `WM_CONCAT` 或 `LISTAGG`
**检查时机**: 第四步 4.2（实现 Service 时）

### 🟢 P8: 数据库连接配置

**现象**: 达梦端口号错误（18071 应为 5236）、SYSDBA 密码错误
**解决方案**: 连接参数统一在 `config.py` 管理，首次连接时先 `test_connection()` 验证
**检查时机**: 前置条件

### ✅ P9: Oracle 不可从本机直连（已解决）

**现象**: oracledb thin 模式报 `DPY-4011`，Thick 模式报 `ORA-12537: TNS:connection closed`
**根因**: Oracle 服务端限制了来源 IP（sqlnet.ora 白名单或防火墙策略）
**最终解决**: 用户在服务器端开放了访问限制，现在本机可直连 Oracle
**连接方式**: Thick 模式，Instant Client 路径 `E:\workfile\JAVA\NewAPI\oracle_client`
**当前状态**: ✅ 已解决，迁移脚本可直接在本机执行

### 🟡 P10: Python 3.8 类型注解不兼容

**现象**: `list[dict]`、`tuple[int, list]` 报 `TypeError: 'type' object is not subscriptable`
**根因**: Python 3.8 不支持内置类型的泛型标注（3.9+ 才支持）
**解决方案**: 在每个 .py 文件头添加 `from __future__ import annotations`
**影响范围**: 所有使用 `list[xxx]`、`tuple[xxx]`、`dict[xxx]` 类型标注的文件
**检查时机**: 第四步（创建新文件时）

### 🟡 P11: 达梦 NEWPYTHON 用户无 CREATE SEQUENCE 权限

**现象**: `CREATE SEQUENCE SEQ_XXX` 报 `CODE:-5519 没有创建序列权限`
**根因**: NEWPYTHON 用户权限不足
**解决方案**: Service 层新增记录时使用 `MAX(PRIMARY_KEY)+1` 降级方案
**检查时机**: 第三步（建表）+ 第四步（Service 新增逻辑）

### 🟢 P12: 文件共享权限

**现象**: `write_to_file` 和 `Copy-Item` 写服务器共享目录报 Access Denied
**根因**: 文件共享默认只读
**解决方案**: 用户已开放写入权限，使用 `Copy-Item -Force` 命令复制文件
**检查时机**: 第三步（复制脚本到服务器时）

### 🟡 P13: 迁移后无表注释和字段注释

**现象**: 迁移脚本建表后，达梦表无表注释和字段注释
**根因**: 初始版本脚本只迁移表结构和数据，未迁移注释
**解决方案**: 已在 `server_migrate.py` 建表后自动从 Oracle `ALL_TAB_COMMENTS` 和 `ALL_COL_COMMENTS` 同步注释
**当前状态**: ✅ 已修复，后续新表自动同步注释

### 🟢 P14: 删除方式差异（软删除 vs 真删除）

**现象**: OWNERUNIT 使用软删除（`OWNERUNIT_STATE=0`），SERVERPART 使用真删除（`DELETE`）
**根因**: 不同实体的业务逻辑不同
**解决方案**: 必须阅读原 C# Helper 的 Delete 方法确认删除方式
- 看到 `_XXX.Delete()` → 真删除
- 看到 `_XXX.Update()` + 设 STATE=0 → 软删除
**检查时机**: 第一步 1.2（读 Helper）+ 第四步 4.2（实现 Service）

---

## 迁移进度跟踪

| 接口路径 | 状态 | 日期 | 遇到的问题 | 备注 |
|----------|------|------|-----------|------|
| BaseInfo/GetBrandList | 🟡 PoC | 2026-03-04 | P1-P6 | PoC 验证，缺少关联字段 |
| BaseInfo/GetBrandDetail | 🟡 PoC | 2026-03-04 | | |
| BaseInfo/SynchroBrand | 🟡 PoC | 2026-03-04 | | |
| BaseInfo/DeleteBrand | 🟡 PoC | 2026-03-04 | | |
| **BaseInfo/GetOWNERUNITList** | **✅ 完成** | **2026-03-04** | **P9,P10,P11,P12** | **592条，18字段** |
| **BaseInfo/GetOWNERUNITDetail** | **✅ 完成** | **2026-03-04** | | |
| **BaseInfo/SynchroOWNERUNIT** | **✅ 完成** | **2026-03-04** | | |
| **BaseInfo/DeleteOWNERUNIT** | **✅ 完成** | **2026-03-04** | | 软删除 |
| **BaseInfo/GetSERVERPARTList** | **✅ 完成** | **2026-03-04** | **P13,P14** | **1168条，42字段** |
| **BaseInfo/DeleteSERVERPART** | **✅ 完成** | **2026-03-04** | | 真删除 |
| BaseInfo/GetServerpartShopList | ⬜ 待开始 | | | |

状态说明：⬜待开始 → 🔵进行中 → 🟡部分完成 → ✅已完成