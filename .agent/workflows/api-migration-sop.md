---
description: 单个接口迁移的完整操作步骤（SOP），新 AI 只需阅读本文件即可独立完成迁移
---

# 接口迁移操作手册（SOP）

> **目标读者**：任何新接手的 AI 或开发者。只需阅读本文件 + `/api-migration` 工作流，即可独立完成一个接口实体的迁移。
>
> **一个"迁移单元"** = 一个实体的所有接口（通常是 CRUD 四件套：GetList、GetDetail、Synchro、Delete）

// turbo-all

---

> [!CAUTION]
> **必读！迁移接口必须严格按照本 SOP 的步骤顺序逐步执行，不允许跳步、合并步骤或省略记录！**
> - 每个步骤必须完整执行并记录结果后，才能进入下一步
> - 步骤 1 的分析结果必须按表格格式完整记录
> - 步骤 2 的基准数据关键指标必须逐项记录
> - 步骤 5 的对比清单必须全部 ✅ 才能进入步骤 6
> - 步骤 6 必须更新所有进度文件（包括工作日志和修改记录）
> - **违反以上规则的迁移视为无效，必须重新执行**

> [!IMPORTANT]
> **自动连续执行规则（必读且必须执行）**
> - 每完成一批接口的迁移（步骤 1-6 全部走完）后，**不需要询问用户、不需要等待确认**，直接自动开始下一批接口的迁移
> - 持续循环执行 SOP 步骤 1→2→3→4→5→6，直到 `collaboration_plan.md` 中当前 Controller 的所有 ❌ 接口全部变为 ✅
> - 只有在遇到 **无法自行解决的错误** 或 **需要用户提供信息**（如密码、权限等）时才停下来询问用户
> - 完成一批后的过渡：直接查看 `collaboration_plan.md` 找到下一组 ❌ 接口，立即开始新一轮 SOP

## 步骤 0：确认待迁移接口

### 0.1 查看进度表

```
view_file .agent/workflows/api-migration.md
```

拉到底部「迁移进度跟踪」表，找到**状态为 ⬜ 的第一个实体**，这就是你要迁移的目标。

### 0.2 查看总计划

```
view_file docs/collaboration_plan.md
```

在「阶段一」表格中确认目标实体属于哪个批次。

### 0.3 确认目标

记录以下信息（后续步骤全部围绕它）：

```
实体名称: ___________（例如：COOPMERCHANTS）
所属 Controller: ___________（例如：BaseInfoController）
预计接口数: ___________（例如：4）
```

---

## 步骤 1：读原 C# 代码（只读不写）

### 1.1 在接口文档中搜索实体

先在接口文档中搜索，快速了解该实体有哪些接口：

```
grep_search 搜索路径="E:\workfile\JAVA\NewAPI\EShangApiMain接口文档.md" 关键词="实体名"
```

> ⚠️ 接口文档很大（60万字节），文件编码可能不标准，搜索时用**大小写不敏感**模式。

### 1.2 定位原 Controller

在原 C# 项目中找到对应的 Controller 文件：

```
搜索路径: E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\
搜索关键词: 实体名（如 GetXXXList）
```

**必须确认并记录**（这是最关键的信息）：

| 必须确认项 | 说明 | 示例 |
|-----------|------|------|
| 路由路径 | `[Route("BaseInfo/GetXXXList")]` 的**精确大小写** | `BaseInfo/GetCASHWORKERList` |
| HTTP 方法 | POST / GET / GET+POST | POST |
| 入参格式 | `SearchModel<T>` 直接 JSON 还是 `CommonModel` AES加密 | SearchModel 直接 JSON |
| Header 读取 | 搜索 `GetIntHeader` / `GetStringHeader` 确认是否从 Header 读取额外参数 | `ProvinceCode` |
| Delete 方式 | 看 Delete 方法体，是 `_XXX.Update()` 还是 `_XXX.Delete()` | 软删除 STATE=0 |

> [!IMPORTANT]
> **Header 读取检查必须执行！** 在原 C# Controller 中搜索 `GetIntHeader` 和 `GetStringHeader`，
> 常见的 Header 参数有：
> - `ProvinceCode` — 省份编码（几乎所有查询接口都有）
> - `ServerpartCodes` — 服务区编码权限
> - `ServerpartShopIds` — 门店权限
> - `UserPattern` — 用户类型（2000=商户账号）
>
> Python 侧使用 `deps.py` 中的公共函数：
> ```python
> from routers.deps import get_int_header, get_str_header
> # GET 接口: 参数默认值回退
> ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)
> # POST 接口: 设置到 SearchParameter
> search_model.SearchParameter["PROVINCE_CODE"] = get_int_header(request, "ProvinceCode")
> ```

**逐个接口记录为表格**：

```markdown
| 路由 | 方法 | 入参 | 说明 |
|------|------|------|------|
| BaseInfo/GetXXXList | POST | SearchModel<XXXModel> | 列表 |
| BaseInfo/GetXXXDetail | GET | XXXId (query) | 明细 |
| BaseInfo/SynchroXXX | POST | XXXModel (body) | 同步 |
| BaseInfo/DeleteXXX | GET+POST | XXXId (query) | 软删除/真删除 |
```

### 1.3 定位原 Helper（Service 层）

```
搜索路径: E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\
搜索关键词: 实体名Helper（如 CASHWORKERHelper）
```

**必须从 Helper 中提取**：

1. **完整 SQL 查询** — 包含所有 JOIN、子查询、WHERE 条件
2. **默认排序** — ORDER BY 子句（很多 Helper 里有默认排序）
3. **默认分页** — 不传参数时的行为（通常默认 10 条）
4. **关联表** — JOIN 了哪些表（如 T_SERVERPART 获取服务区名称）
5. **特殊处理** — 日期 +1 天、EXISTS 子查询、WM_CONCAT 等
6. **Delete 实现** — 软删除（UPDATE SET STATE=0）还是真删除（DELETE FROM）
7. **Synchro 排除字段** — 哪些字段不入库（查询条件字段）
8. **Synchro 唯一性校验** — 是否校验某个字段的唯一性
9. **Synchro 新增 ID** — 使用哪个序列（`SEQ_XXX.NEXTVAL`）

> ⚠️ **关键规则**：`FillDataTable(WhereSQL)` 等价于 `SELECT * FROM T_XXX {WhereSQL}`

### 1.4 定位原 Model

```
搜索路径: E:\workfile\JAVA\API\CSharp\EShangApi.Common\Model\
搜索关键词: 实体名Model
```

确认字段列表和类型（int / string / datetime）。

---

## 步骤 2：调原 API 获取基准数据

### 2.1 调用原接口

原 C# API 地址：`http://192.168.1.99:8900`

用空参数 `{}` 调用原接口，获取基准响应：

```powershell
# GetList 接口（POST）
Invoke-RestMethod -Uri "http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetXXXList" -Method Post -Body '{}' -ContentType 'application/json' | ConvertTo-Json -Depth 10
```

```powershell
# GetDetail 接口（GET）— 用一个已知的 ID
Invoke-RestMethod -Uri "http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetXXXDetail?XXXId=1" -Method Get | ConvertTo-Json -Depth 10
```

### 2.2 记录关键指标

从基准响应中提取并**记录**以下信息：

```
Result_Code: ___（正常应为 100）
TotalCount: ___（总数据量）
List 条数: ___（不传参数时默认返回多少条）
PageIndex 默认值: ___
PageSize 默认值: ___
字段列表: [完整列出所有字段名]
第一条数据的排序依据: ___（确认默认排序）
字段类型: ___（哪些是 int、哪些是 string、哪些是 null）
```

> ⚠️ 如果 List 条数为 10，说明原 API 有默认分页限制（不传参数时返回前 10 条）。

---

## 步骤 3：同步数据库表

> 确保原 Oracle 的表数据已同步到达梦 NEWPYTHON。

### 3.1 确认需要哪些表

根据步骤 1.3 中分析的 Helper SQL，列出：
- **主表**：`T_XXX`
- **JOIN 关联表**：`T_YYY`、`T_ZZZ`
- **已知 Oracle schema 映射**：
  - `COOP_MERCHANT` → 业主、品牌、商户等
  - `HIGHWAY_STORAGE` → 服务区、门店、收银等

### 3.2 检查达梦是否已有数据

如果不确定表是否已存在，可以先检查：

```powershell
python -c "import dmPython; conn=dmPython.connect(user='NEWPYTHON',password='NewPython@2025',server='192.168.1.99',port=5236); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM T_XXX'); print(cur.fetchone()[0]); conn.close()"
```

### 3.3 添加到迁移脚本

如果表还未迁移，编辑 `scripts/server_migrate.py`，在 `MIGRATE_TABLES` 列表中添加：

```python
# 在 MIGRATE_TABLES 列表末尾追加
{"oracle_schema": "HIGHWAY_STORAGE", "table": "T_XXX", "sequence": "SEQ_XXX"},
```

**如何确定 oracle_schema**：
- 看原 Helper SQL 中表前缀：`HIGHWAY_STORAGE.T_XXX` 或 `COOP_MERCHANT.T_XXX`
- 常见规则：服务区/门店/收银/商品 → `HIGHWAY_STORAGE`；品牌/商户/业主 → `COOP_MERCHANT`

### 3.4 执行迁移

> [!CAUTION]
> **禁止不带参数运行 `python scripts/server_migrate.py`！** 不带参数会全量重跑所有旧表，耗时极长且无意义。
> 必须指定当前接口需要的表名：

```powershell
# 只迁移当前接口需要的表（可指定多张）
python scripts/server_migrate.py T_XXX
python scripts/server_migrate.py T_XXX T_YYY
```

脚本会自动：
1. 读 Oracle 表结构
2. 在达梦建表（已存在则 MERGE INTO 合并差异）
3. 同步表注释和字段注释
4. 迁移数据（每 2000 条批量提交）
5. 校验行数是否一致

### 3.5 验证迁移结果

脚本输出中必须看到：
```
✅ 行数一致
```

如果看到 `❌ 行数不一致`，需要排查原因。

---

## 步骤 4：实现 Python 接口

### 4.1 创建 Service 文件

**文件路径**：`services/base_info/{实体名小写}_service.py`

**完整代码模板**（复制后按实际情况修改标注了 `⬅️ 改这里` 的行）：

```python
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
{实体中文名}业务服务
替代原 {实体名}Helper.cs，保持相同的业务逻辑
对应 BaseInfoController 中 {实体名} 相关 N 个接口
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_XXX"                    # ⬅️ 改这里：实际表名
PRIMARY_KEY = "XXX_ID"                  # ⬅️ 改这里：主键字段名

# Synchro 时需排除的字段（查询条件字段，非数据库列）
EXCLUDE_FIELDS = {"SERVERPART_IDS", "SERVERPART_CODES"}  # ⬅️ 改这里：参考原 Helper

# 日期字段（需要 TO_DATE 处理）
DATE_FIELDS = {"OPERATE_DATE"}          # ⬅️ 改这里：实际日期字段


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """根据查询参数构建通用 WHERE 条件"""
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS:
            continue
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
    return " AND ".join(conditions)


# ========== 1. GetXXXList ==========          # ⬅️ 改函数名

def get_xxx_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取{实体中文名}列表
    对应原 XXXHelper.GetXXXList（行号范围）
    SQL: 参考原 Helper 中的完整 SQL              # ⬅️ 写出原 Helper 的 SQL
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

        # ⬅️ 在此添加特殊条件处理（SERVERPART_IDS IN查询、日期范围等）
        # 参考 cashworker_service.py 的写法

    # 执行查询（⬅️ 如果原 Helper 有 JOIN，改为完整 SQL）
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    rows = db.execute_query(base_sql)

    # 关键字过滤（通用，无需修改）
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            search_value = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(
                search_value in str(r.get(k, "")) for k in keys
            )]

    # 排序（通用，无需修改）
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field, 0) or 0, reverse=is_desc)

    # 总数
    total_count = len(rows)

    # 分页（通用，无需修改）
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    # ⬅️ 如果原 Helper 有关联查询（如 JOIN T_SERVERPART 获取名称），在这里补充

    return int(total_count), rows


# ========== 2. GetXXXDetail ==========         # ⬅️ 改函数名

def get_xxx_detail(db: DatabaseHelper, xxx_id: int) -> Optional[dict]:
    """
    获取{实体中文名}明细
    对应原 XXXHelper.GetXXXDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {xxx_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroXXX ==========           # ⬅️ 改函数名

def synchro_xxx(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步{实体中文名}（新增或更新）
    对应原 XXXHelper.SynchroXXX
    """
    record_id = data.get(PRIMARY_KEY)

    # ⬅️ 如有唯一性校验，在此添加（参考 cashworker_service.py）

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # === 更新模式 ===
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                if key in DATE_FIELDS:
                    set_parts.append(f"{key} = NULL")
                continue
            if key in DATE_FIELDS:
                set_parts.append(f"{key} = TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # === 新增模式 ===
        try:
            new_id = db.execute_scalar("SELECT SEQ_XXX.NEXTVAL FROM DUAL")  # ⬅️ 改序列名
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        data[PRIMARY_KEY] = new_id
        db_data[PRIMARY_KEY] = new_id

        columns = []
        values = []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if key in DATE_FIELDS:
                values.append(f"TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. DeleteXXX ==========             # ⬅️ 改函数名

def delete_xxx(db: DatabaseHelper, xxx_id: int) -> bool:
    """
    删除{实体中文名}
    对应原 XXXHelper.DeleteXXX
    """
    # ⬅️ 根据原 Helper 的 Delete 方法选择下面两种之一：

    # 方式A - 软删除（原 Helper 里是 Update + STATE=0）：
    sql = f"UPDATE {TABLE_NAME} SET XXX_STATE = 0 WHERE {PRIMARY_KEY} = {xxx_id}"

    # 方式B - 真删除（原 Helper 里是 _XXX.Delete()）：
    # sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {xxx_id}"

    affected = db.execute_non_query(sql)
    return affected > 0
```

### 4.2 创建 Router 文件

**文件路径**：`routers/eshang_api_main/base_info/{实体名小写}_router.py`

**完整代码模板**：

```python
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
{实体中文名} API 路由
对应原 BaseInfoController.cs 中 {实体名} 相关 N 个接口
路由路径与原 Controller 完全一致

接口清单：
- POST      /BaseInfo/GetXXXList      — 列表查询     # ⬅️ 改路由
- GET       /BaseInfo/GetXXXDetail     — 明细查询
- POST      /BaseInfo/SynchroXXX       — 同步（新增/更新）
- GET+POST  /BaseInfo/DeleteXXX        — 删除
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import xxx_service        # ⬅️ 改 import
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetXXXList")               # ⬅️ 改路由（精确大小写！）
async def get_xxx_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取{实体中文名}列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        # ⬅️ 如原 Controller 从 Header 读参数，参考 cashworker_router.py 添加

        total_count, data_list = xxx_service.get_xxx_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetXXXList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetXXXDetail")               # ⬅️ 改路由
async def get_xxx_detail(
    XXXId: int = Query(..., description="实体内码"),  # ⬅️ 改参数名（与原 Controller 一致）
    db: DatabaseHelper = Depends(get_db)
):
    """获取{实体中文名}明细"""
    try:
        detail = xxx_service.get_xxx_detail(db, XXXId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetXXXDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroXXX")                # ⬅️ 改路由
async def synchro_xxx(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步{实体中文名}（新增/更新）"""
    try:
        success, result_data = xxx_service.synchro_xxx(db, data)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroXXX 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteXXX", methods=["GET", "POST"])  # ⬅️ 改路由和方法
async def delete_xxx(
    XXXId: int = Query(..., description="实体内码"),  # ⬅️ 改参数名
    db: DatabaseHelper = Depends(get_db)
):
    """删除{实体中文名}"""
    try:
        success = xxx_service.delete_xxx(db, XXXId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteXXX 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
```

### 4.3 注册路由到 main.py

在 `main.py` 中添加路由注册（在 `# 后续在这里注册更多路由...` 注释之前）：

```python
from routers.eshang_api_main.base_info.xxx_router import router as xxx_router
app.include_router(xxx_router, prefix="/EShangApiMain", tags=["实体中文名 (XXX)"])
```

### 4.4 文件检查清单

- [ ] Service 和 Router 文件头都有 `from __future__ import annotations`
- [ ] 路由路径大小写与原 Controller `[Route()]` 注解**完全一致**
- [ ] Service 中的 SQL 参考自原 Helper（不是自己猜的）
- [ ] Delete 方式已确认（软删除 vs 真删除）
- [ ] 已在 `main.py` 注册路由

---

## 步骤 5：对比验证

### 5.1 启动 Python 服务

确保新 Python API 正在运行（已在 `http://localhost:8080`）：

```powershell
python main.py
```

观察启动日志，确认新路由已加载（看到对应的路由路径）。

### 5.2 快速冒烟测试

先用浏览器或 curl 快速调一下新接口，确认不报 500 错误：

```powershell
# 测试 GetList
Invoke-RestMethod -Uri "http://localhost:8080/EShangApiMain/BaseInfo/GetXXXList" -Method Post -Body '{}' -ContentType 'application/json' | ConvertTo-Json -Depth 5
```

如果报错，先排查修复，常见错误：
- 表不存在 → 回步骤 3 迁移表
- 字段不存在 → SQL 拼写错误，核对原 Helper
- import 报错 → 检查 `__init__.py` 和 import 路径

### 5.3 修改对比脚本

编辑 `scripts/compare_api.py`，修改 `ENDPOINT` 变量：

```python
ENDPOINT = "BaseInfo/GetXXXList"    # ⬅️ 改为当前接口路由
```

> 注意：对比脚本默认使用 POST 方法。如果接口是 GET 方法，需要修改脚本中的 `requests.post` 为 `requests.get`。

### 5.4 执行对比（必须使用 3 组不同参数）

> [!IMPORTANT]
> **必须使用 3 组不同的参数进行对比验证，全部通过才算验证通过。**
> 例如 GetXXXList 接口，用 3 个不同的主键/筛选条件调用，确保不同数据场景都能匹配。

使用 Python `requests` 直接对比两个 API（避免终端编码问题）：

```python
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# “不影响业务”的已知差异字段（如环境配置 URL、数据库函数排序差异）
IGNORE_FIELDS = set()  # ⬅️ 根据实际情况填写

test_params_list = [
    {"param1": "value1"},  # ⬅️ 改为实际参数
    {"param1": "value2"},
    {"param1": "value3"},
]

for params in test_params_list:
    old = requests.get("http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetXXX", params=params).json()
    new = requests.get("http://localhost:8080/EShangApiMain/BaseInfo/GetXXX", params=params).json()
    old_list = old["Result_Data"]["List"]
    new_list = new["Result_Data"]["List"]
    # 逐条逐字段对比，输出差异
```

### 5.5 对比清单（**3 组数据全部** ✅ 才算通过）

| 检查项 | 要求 | 不通过时怎么办 |
|--------|------|---------------|
| Result_Code | 一致（都是100） | 检查服务是否正常 |
| TotalCount | 一致 | 检查 WHERE 条件是否遗漏 |
| List 条数 | 一致 | 检查默认分页逻辑 |
| 字段列表 | 完全一致 | 缺失 → 检查 JOIN；多余 → 添加到 EXCLUDE |
| 字段值类型 | 一致（int vs string） | 达梦类型不对 → ALTER TABLE MODIFY |
| 排序 | 第一条数据相同 | 检查 ORDER BY |
| 空值处理 | null 字段一致 | 检查 SQL 是否有 NVL |
| Warning标记 | CompactWarning/ProjectWarning 一致 | 检查空值判定和精度问题 |

> [!WARNING]
> **常见坑（必须注意）**：
> - **Python `not 0.0` 为 True**：检查空值判定不能用 `not val`，必须用 `val is None or str(val) == ""`
> - **C# `TryParseToInt()` null→0**：Python `_safe_int(None)` 返回 None，需用 `_safe_int_zero()` 匹配
> - **C# `.ToString()` null→`""`**：Python `str(None)` 是 `"None"` 不是空串
> - **float 精度丢失**：金额比较必须用 `Decimal` 而非 `float`

### 5.6 修复不通过项

**最常见的问题和解决方案**：

1. **TotalCount 不一致**：WHERE 条件漏了，回去对比原 Helper SQL
2. **List 条数不一致**：默认分页不对，原 API 不传参默认返回 10 条
3. **字段缺失**：原 Helper 有 JOIN 关联查询，你的 SQL 写的是 `SELECT *` 没有 JOIN
4. **字段值类型不一致**：达梦把 NUMBER 导成了 VARCHAR，用 `ALTER TABLE` 修复
5. **排序不一致**：原 Helper 有 `ORDER BY XXX_ID DESC`，你没加

---

## 步骤 6：更新进度并提交代码

### 6.1 更新迁移进度表

编辑 `.agent/workflows/api-migration.md`，在「迁移进度跟踪」表中**添加新行**：

```markdown
| 新实体名称（中文） | 接口数 | ✅ | 2026-03-XX | 遇到的问题编号 |
```

### 6.2 更新实施计划（强制！每次迁移后必须执行）

> [!IMPORTANT]
> **每次迁移完成后必须立即更新 `docs/collaboration_plan.md`，不可跳过！**
> 这是确保实施计划始终与最新进度同步的唯一手段。

编辑 `docs/collaboration_plan.md`，逐一检查并更新以下 **5 处**：

**✅ 更新检查清单：**

- [ ] **① 最后更新时间**：`> **最后更新时间**：2026-MM-DD` 改为当天日期
- [ ] **② 已完成标题**：`### 已完成（N 个实体 + M 个散装接口，共 X 个接口）` 更新计数
- [ ] **③ 已完成接口明细表**：在表格末尾添加新行

```markdown
| BaseInfo/GetXXX | 接口说明 | HTTP方法 | 所属实体或"散装" |
```

- [ ] **④ 待迁移表 + 进度总览**：更新以下字段
  - `BaseInfoController` 行的 `已完成` 和 `剩余` 列
  - 进度总览的 `已完成`、`剩余`、`完成率`、`已完成实体数`

- [ ] **⑤ 阶段一批次表**：更新对应批次状态
  - 全部完成 → `✅ 已完成`
  - 部分完成 → `🔄 进行中（已完成 N / 剩余 M）`

**计算公式：**
```
总已完成接口数 = 已完成接口明细表中的行数
完成率 = 总已完成接口数 / 551 × 100%
阶段一完成率 = BaseInfoController已完成 / ~145 × 100%
```

### 6.3 记录遇到的问题（如有）

如果迁移过程中遇到新问题，在 `.agent/workflows/api-migration.md` 的「已知问题速查表」中追加：

```markdown
### 🟡 P{序号}: 问题简述

**现象**: 具体描述
**根因**: 为什么会出现
**解决方案**: 如何修复
**检查时机**: 第几步
```

### 6.4 更新工作日志

编辑 `docs/work_log_YYYYMMDD.md`（当天日期），追加本次迁移的接口记录：

```markdown
### N. 接口名 ✅
- 路由: `BaseInfo/GetXXX` | 方法
- 参数: 参数列表
- 返回: 返回类型描述
- 关键实现: 特殊逻辑说明
- 基准数据: N 条
- 对比结果: 通过
```

### 6.5 更新修改记录

编辑 `docs/change_log.md`，追加本次修改的文件记录：

```markdown
### [接口名] 修改说明
- **文件**: 文件路径 (行号范围)
- **修改内容**: 具体修改了什么
- **原因**: 为什么要这样修改
```

### 6.6 提交 Git（如需要）

```powershell
git add -A
git commit -m "feat: 迁移 {实体名} {接口数}接口 - 对比验证通过"
```

### 6.7 继续下一个

回到**步骤 0**，查看进度表，找到下一个待迁移的实体，重复整个流程。

---

## 附录A：项目关键路径速查

| 类型 | 路径 |
|------|------|
| Python 项目根目录 | `E:\workfile\JAVA\NewAPI\` |
| C# 原项目根目录 | `E:\workfile\JAVA\API\CSharp\` |
| C# Controller 目录 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\` |
| C# Helper 目录 | `E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\` |
| C# Model 目录 | `E:\workfile\JAVA\API\CSharp\EShangApi.Common\Model\` |
| Service 目录 | `E:\workfile\JAVA\NewAPI\services\base_info\` |
| Router 目录 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\base_info\` |
| 迁移脚本 | `E:\workfile\JAVA\NewAPI\scripts\server_migrate.py` |
| 对比脚本 | `E:\workfile\JAVA\NewAPI\scripts\compare_api.py` |
| 工作流（进度表） | `E:\workfile\JAVA\NewAPI\.agent\workflows\api-migration.md` |
| 总计划 | `E:\workfile\JAVA\NewAPI\docs\collaboration_plan.md` |
| 接口文档 | `E:\workfile\JAVA\NewAPI\EShangApiMain接口文档.md` |

## 附录B：已知问题速查（迁移前必读）

| ID | 问题 | 关键解决方案 |
|----|------|-------------|
| P1 | 达梦 NUMBER→VARCHAR | `ALTER TABLE MODIFY 列名 INT` |
| P2 | 关联字段缺失 | 必须完整阅读原 Helper SQL 的 JOIN |
| P3 | 默认分页 | 不传参时 `rows[:10]` 限制 10 条 |
| P4 | 路由大小写 | 看原 `[Route()]` 注解，不要猜 |
| P7 | Oracle→达梦语法 | `(+)` → LEFT JOIN |
| P10 | Python 3.8 类型 | 文件头 `from __future__ import annotations` |
| P11 | 无序列权限 | `MAX(ID)+1` 降级 |
| P14 | 软/真删除 | 看原 Helper Delete 方法体 |
| P16 | Header 参数遗漏 | 原 C# 用 `GetIntHeader`/`GetStringHeader` 从请求头读 ProvinceCode 等参数，Python 必须用 `get_int_header` 复现 |
| P17 | 前端非数据库字段 | 前端 SearchParameter 常带 current/pageSize 等非数据库字段，必须通过 SEARCH_PARAM_SKIP_FIELDS 过滤 |

## 附录C：参考已完成文件

需要参考实现模式时，优先查看这些已完成的文件：

- **简单 CRUD**（4接口）：`cashworker_service.py` + `cashworker_router.py`
- **含关联查询**（5接口）：`serverpartshop_service.py` + `serverpartshop_router.py`
- **复杂业务**（6接口）：`brand_service.py` + `brand_router.py`
- **树形结构**（6接口）：`businesstrade_service.py` + `businesstrade_router.py`
- **含 Header 参数**：`cashworker_router.py`（从 Header 读 ServerpartCodes）
- **含批量操作**：`serverpartshop_router.py`（DelServerpartShop 批量删除）

---

## 历史踩坑注意事项

> [!CAUTION]
> **以下问题均为实际迁移中发生过的线上 bug，每次迁移必须逐条自查！**

### P-SOP-1：`_build_where_sql` 中变量名未定义

- **现象**：GetList 接口传入 `SearchParameter` 时报错 `name 'skip_fields' is not defined`，空参调用不报错
- **根因**：`_build_where_sql` 函数中引用了 `skip_fields` 变量，但该变量从未定义。正确的变量名应为模块顶部的 `EXCLUDE_FIELDS` 常量
- **影响**：历史上 **11 个 service 文件** 都存在此 bug（空参调用不触发，只有传参才会暴露）
- **自查方法**：完成 service 编写后，搜索文件中所有变量引用，确认无未定义变量。特别注意 `_build_where_sql` 函数内引用的排除字段集合名称必须与模块顶部定义的常量名一致
- **修复模板**：
```python
# ❌ 错误
if key in skip_fields:
# ✅ 正确（使用模块顶部定义的常量）
if key in EXCLUDE_FIELDS:
```

### P-SOP-2：步骤 3 漏同步关联表

- **现象**：接口运行报错 `无效的表或视图名[T_XXX]`
- **根因**：步骤 3（同步数据库）只同步了当前实体的主表，但 service 代码中还依赖了其他关联表（如 `T_PROPERTYASSETS` 是 PROPERTYASSETS 实体的主表，在实现该实体时已写了代码但忘记同步表）
- **自查方法**：步骤 3 执行前，先检查 service 代码中 **所有 SQL 语句引用的表名**，确认每张表都已存在于达梦数据库中。使用以下命令快速检查：
```python
# 在 service 文件中搜索所有表名引用
grep -oP 'FROM\s+(\w+)' services/base_info/xxx_service.py | sort -u
# 在达梦中验证表是否存在
SELECT TABLE_NAME FROM USER_TABLES WHERE TABLE_NAME = 'T_XXX';
```
- **关联检查清单**：迁移实体 A 时，如果 A 的 GetDetail/GetList 关联查询了表 B，则表 B 也必须在达梦中存在。常见关联：
  - `T_PROPERTYASSETS` → `T_PROPERTYSHOP`、`T_SERVERPARTSHOP`
  - `T_COMMODITY` → `T_RTCOMMODITYBUSINESS`、`T_COMMODITY_BUSINESS`
  - `T_BRAND` → `T_AUTOSTATISTICS`、`T_COOPMERCHANTS`
