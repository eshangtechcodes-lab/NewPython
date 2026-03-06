---
description: C# API 接口平移到 Python FastAPI 的标准工作流
---

# API 接口迁移工作流

> 适用于 EShangApi C# → Python FastAPI 的逐接口迁移。每迁移一个接口，严格按以下步骤执行。
>
> ⚠️ **关键约束**：达梦数据库初始是空库，没有任何表结构和数据。必须先完成「第零步：数据库表同步」，确保达梦中有对应的表和数据后，才能开始接口代码迁移和对比验证。

## 前置条件

- 原 C# API 服务已启动（`http://localhost:8900`）
- 新 Python API 服务已启动（`http://localhost:8080`）
- 原项目代码路径：`D:\Project\000_通用版本\000_通用版本\030_EShangApi`
- 达梦数据库：`127.0.0.1:5236`，用户 `NEWPYTHON`，密码 `NewPython@2025`

---

## 第零步：数据库表同步（每个接口迁移前必做）

> **达梦初始无表结构**，必须先把接口依赖的所有表（结构+数据）从 Oracle 同步到达梦，否则无法验证。

### 0.1 梳理依赖表

阅读原 Helper 代码中的 SQL，列出该接口涉及的**所有表**：

- **主表**：SELECT 的主表
- **JOIN 表**：LEFT JOIN / INNER JOIN 的表
- **字典表**：用于翻译 ID 为名称的表
- **子查询表**：嵌套查询中的表

记录到 `docs/table_dependencies.md`：

```markdown
| Controller | 接口 | 主表 | JOIN 表 | 字典表 |
|------------|------|------|---------|--------|
| BaseInfoController | GetBrandList | T_BRAND | T_MERCHANTS, T_SERVERPART | T_BUSINESSTRADE |
```

### 0.2 检查达梦中是否已有这些表

```python
# scripts/check_dm_tables.py — 按需修改 tables 列表
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()
tables = ['T_BRAND', 'T_MERCHANTS', 'T_SERVERPART', 'T_BUSINESSTRADE']
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  ✅ {t:30s} {cur.fetchone()[0]:>8} 条")
    except:
        print(f"  ❌ {t:30s} 不存在 → 需要同步")
```

### 0.3 同步缺失的表

通过达梦 DTS 工具或手动方式从 Oracle 导入：

1. 用 DTS 连接 Oracle（`127.0.0.1/orcl`，`highway_exchange/qrwl`）
2. 选择需要的表，导出到达梦 NEWPYTHON 用户
3. 导入后验证行数一致

### 0.4 校验字段类型

导入后必须检查字段类型是否正确（已知问题 P1：DTS 可能把 NUMBER 列导为 VARCHAR）：

```sql
-- 查看达梦表字段类型
SELECT COLUMN_NAME, DATA_TYPE FROM USER_TAB_COLUMNS WHERE TABLE_NAME='T_BRAND' ORDER BY COLUMN_ID;

-- 若数值列被导为 VARCHAR，修正：
ALTER TABLE T_BRAND MODIFY BRAND_ID INT;
ALTER TABLE T_BRAND MODIFY BRAND_PID INT;
ALTER TABLE T_BRAND MODIFY BRAND_CATEGORY INT;
-- 修正前确认该列数据能转为整数
```

### 0.5 确认通过后才进入第一步

所有依赖表 ✅ 存在 + 数据量一致 + 字段类型正确 → 才可以开始接口代码迁移。

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
搜索路径：EShang.Common/ 或 EShangApiMain/Helper/
搜索关键词：GetBrandList 或 T_BRAND
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

## 第三步：创建达梦对应表

### 3.1 确认达梦表已存在

检查 NEWPYTHON 用户下是否已有对应的表和数据：

```python
# 在 scripts/check_dm_xxx.py 中验证
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM T_XXX")
print(f"数据量: {cur.fetchone()[0]}")
# 打印字段列表和类型
cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM USER_TAB_COLUMNS WHERE TABLE_NAME='T_XXX' ORDER BY COLUMN_ID")
for row in cur.fetchall():
    print(f"  {row[0]:30s} {row[1]}")
```

### 3.2 字段类型校验

对比达梦字段类型与原 Oracle 表，确保数值列为 INT/DECIMAL 而非 VARCHAR。若类型不对，修改达梦表结构：

```sql
ALTER TABLE T_XXX MODIFY BRAND_ID INTEGER;
```

---

## 第四步：实现 Python 接口

按照第一步读取的原代码，创建以下文件：

### 4.1 Model（若尚不存在）

文件：`models/auto_build/xxx.py`

- 使用 Pydantic BaseModel
- 字段名与原 C# Model 完全一致
- 字段类型与原 API 返回类型对齐

### 4.2 Service

文件：`services/auto_build/xxx_service.py`

- **SQL 必须参考原 Helper 中的查询**，不能自己猜测
- 包含 JOIN、默认排序、默认分页逻辑
- 保持与原 Helper 完全一致的业务行为

### 4.3 Router

文件：`routers/eshang_api_main/auto_build/xxx_router.py`

- 路由路径与原 Controller 完全一致（注意大小写）
- 入参格式与原 Controller 一致
- 在 `main.py` 中注册路由时加 `prefix="/EShangApiMain"`

---

## 第五步：对比验证

### 5.1 运行对比脚本

**CommercialApi 接口（推荐使用缓存对比，~3分钟完成全量对比）：**

```powershell
# 快速对比（读旧 API 缓存 + 调新 API）
python scripts/compare_cached.py
```

> 首次运行前需先采集基线缓存：`python scripts/baseline_collect.py`（~15分钟）
> 详细说明见 `/api-testing` 工作流。

> 接口文档参考：`D:\CSharp\Project\000_通用版本\000_通用版本\030_EShangApi\docs\CommercialApi接口文档说明.md`
> 文档包含每个接口的精确参数定义、测试用例和参考耗时。

**EShangApiMain 接口（传统对比）：**

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

### 🔴 P9: Schema 前缀不能用（2026-03-05 新增）

**现象**: SQL 写 `HIGHWAY_SELLDATA.T_CUSTOMERGROUP` 报错"对象不存在"
**根因**: C# 代码中 SQL 带 Oracle schema 前缀，但达梦中所有表统一在 NEWPYTHON 下
**解决方案**: SQL 中**不要加任何 schema 前缀**，直接用表名
**检查时机**: 第四步 4.2（实现 Service 时，从 C# SQL 翻译时）

### 🔴 P10: Province_Code 是内码不是编码（2026-03-05 新增）

**现象**: `Province_Code=340000` 查到 0 条
**根因**: T_SERVERPART.PROVINCE_CODE 存的是数据字典内码（如 3544），不是行政区划编码
**解决方案**: 先查 `SELECT FIELDENUM_ID FROM T_FIELDENUM WHERE FIELDENUM_VALUE = '340000'` 转换
**检查时机**: 所有涉及 Province_Code 参数的接口

### 🔴 P11: 达梦字段名与 Oracle 不同（2026-03-05 新增）

**现象**: SQL 报"无效的列名 STATISTIC_TYPE"
**根因**: Oracle 有 `STATISTIC_TYPE`，达梦中只有 `STATISTICS_TYPE`（多一个S）
**解决方案**: 实现前先 `SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME='xxx'` 验证
**检查时机**: 第四步 4.2 开始写 SQL 前

### 🟡 P12: 参数名相似但含义不同（2026-03-05 新增）

**现象**: `GetServerpartList` 只返回 1 条
**根因**: C# 中 `Serverpart_ID`(带下划线)是"当前服务区标记"不参与 WHERE，`ServerpartId`(无下划线)才是过滤条件
**解决方案**: 仔细看 C# 代码哪些参数参与 WHERE 构建，哪些仅用于业务逻辑
**检查时机**: 第一步 1.1 和第四步 4.3

### 🟡 P13: 测试数据 ID 在达梦中不存在（2026-03-05 新增）

**现象**: `GetPATROLDetail` C=101（无数据）
**根因**: 测试参数用 `PATROLId=10`，达梦最小 ID 是 687379
**解决方案**: 实现前先查达梦中有效 ID：`SELECT xxx_ID FROM T_xxx ORDER BY xxx_ID DESC FETCH FIRST 5 ROWS ONLY`
**检查时机**: 第五步 5.1 对比前，确认 doc_params.json 中的 ID 有效

> 📄 完整踩坑记录详见 **docs/api_migration_pitfalls.md**

---

## 迁移进度跟踪

> 在 `docs/migration_progress.md` 中维护，记录每个接口的迁移状态。

格式示例：

```markdown
| 接口路径 | 状态 | 日期 | 遇到的问题 | 备注 |
|----------|------|------|-----------|------|
| BaseInfo/GetBrandList | 🟡 部分完成 | 2026-03-04 | P1,P2,P3,P4,P5,P6 | 缺少7个关联字段待补 |
| BaseInfo/GetBrandDetail | ⬜ 待开始 | | | |
| BaseInfo/SynchroBrand | ⬜ 待开始 | | | |
```

状态说明：⬜待开始 → 🔵进行中 → 🟡部分完成 → ✅已完成

