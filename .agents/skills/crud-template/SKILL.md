---
name: CRUD 接口模板
description: 从 api-migration-sop 中提炼的 Service + Router 标准代码模板，用于快速创建新的 CRUD 接口
---

# CRUD 接口模板

> 本 Skill 提供创建新 CRUD 接口的标准代码模板。包含 Service 层和 Router 层的完整模板，所有需要定制的地方用 `⬅️` 标记。

## 适用场景

- 迁移新的 EShangApiMain 实体接口
- 新增 CRUD 类型的 API 接口
- 参考已有模式快速实现相似功能

---

## Service 模板

文件路径：`services/{模块名}/{实体名小写}_service.py`

```python
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
{实体中文名}业务服务
替代原 {实体名}Helper.cs，保持相同的业务逻辑
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# ==================== 常量配置 ====================

TABLE_NAME = "T_XXX"                    # ⬅️ 实际表名
PRIMARY_KEY = "XXX_ID"                  # ⬅️ 主键字段名

# Synchro 时需排除的字段（查询条件字段，非数据库列）
EXCLUDE_FIELDS = {"SERVERPART_IDS", "SERVERPART_CODES"}  # ⬅️ 参考原 Helper

# 日期字段（需要 TO_DATE 处理）
DATE_FIELDS = {"OPERATE_DATE"}          # ⬅️ 实际日期字段

# C# Model 回显属性（DB表没有，C# Model有，值为 null）
EXTRA_FIELDS = {"SERVERPART_IDS": None, "OPERATE_DATE_Start": None}  # ⬅️ 参考 C# Model

# C# Model 字符串字段，DBNull → ''
STRING_FIELDS = {"XXX_DESC", "XXX_NAME"}  # ⬅️ 参考 C# Model


# ==================== 工具函数 ====================

def _format_date(val):
    """将日期格式从 ISO 转为 C# 风格: 2023/3/30 14:02:47"""
    if val is None:
        return None
    s = str(val)
    try:
        if 'T' in s:
            dt = datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        elif '-' in s and len(s) >= 10:
            dt = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
        else:
            return s
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute:02d}:{dt.second:02d}"
    except Exception:
        return s


def _convert_row(row: dict) -> dict:
    """转换行数据：补 C# Model 回显字段 + 字符串 null→'' + 日期格式化"""
    if not row:
        return row
    # 1. 补 C# Model 回显属性
    for k, v in EXTRA_FIELDS.items():
        if k not in row:
            row[k] = v
    # 2. 字符串字段 null→''
    for f in STRING_FIELDS:
        if f in row and row[f] is None:
            row[f] = ""
    # 3. 日期格式化  ⬅️ 按实际日期字段修改
    for df in DATE_FIELDS:
        if df in row:
            row[df] = _format_date(row[df])
    return row


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """根据查询参数构建通用 WHERE 条件"""
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS:
            continue
        if value is None or (isinstance(value, str) and value.strip() == ""):
            continue
        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
    return " AND ".join(conditions)


# ==================== 1. GetList ====================

def get_xxx_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取{实体中文名}列表
    SQL: ⬅️ 参考原 Helper 中的完整 SQL（含 JOIN、ORDER BY）
    """
    where_sql = ""
    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause
        # ⬅️ 在此添加特殊条件（SERVERPART_IDS IN查询、日期范围等）

    # ⬅️ 如原 Helper 有 JOIN，改为完整 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    rows = db.execute_query(base_sql)

    # 关键字过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            search_value = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(search_value in str(r.get(k, "")) for k in keys)]

    # 排序
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field, 0) or 0, reverse=is_desc)

    total_count = len(rows)

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    # 转换行数据
    rows = [_convert_row(r) for r in rows]

    return int(total_count), rows


# ==================== 2. GetDetail ====================

def get_xxx_detail(db: DatabaseHelper, xxx_id: int) -> Optional[dict]:
    """获取{实体中文名}明细"""
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {xxx_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return _convert_row(rows[0])


# ==================== 3. Synchro ====================

def synchro_xxx(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """同步{实体中文名}（新增或更新）"""
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # 更新
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
        # 新增（序列降级为 MAX+1）
        try:
            new_id = db.execute_scalar("SELECT SEQ_XXX.NEXTVAL FROM DUAL")  # ⬅️ 改序列名
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        data[PRIMARY_KEY] = new_id
        db_data[PRIMARY_KEY] = new_id

        columns, values = [], []
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


# ==================== 4. Delete ====================

def delete_xxx(db: DatabaseHelper, xxx_id: int) -> bool:
    """删除{实体中文名}"""
    # ⬅️ 选择：软删除（UPDATE STATE=0）或真删除（DELETE FROM）
    # 方式A - 软删除：
    sql = f"UPDATE {TABLE_NAME} SET XXX_STATE = 0 WHERE {PRIMARY_KEY} = {xxx_id}"
    # 方式B - 真删除：
    # sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {xxx_id}"
    affected = db.execute_non_query(sql)
    return affected > 0
```

---

## Router 模板

文件路径：`routers/eshang_api_main/{模块名}/{实体名小写}_router.py`

```python
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
{实体中文名} API 路由
路由路径与原 Controller 完全一致

接口清单：
- POST      /BaseInfo/GetXXXList       — 列表查询     # ⬅️ 改路由
- GET       /BaseInfo/GetXXXDetail     — 明细查询
- POST      /BaseInfo/SynchroXXX       — 同步
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


@router.post("/BaseInfo/GetXXXList")               # ⬅️ 精确大小写
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
    XXXId: int = Query(..., description="实体内码"),  # ⬅️ 改参数名
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
    """同步{实体中文名}"""
    try:
        success, result_data = xxx_service.synchro_xxx(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroXXX 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteXXX", methods=["GET", "POST"])  # ⬅️ 改路由
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

---

## 注册到 main.py

```python
from routers.eshang_api_main.base_info.xxx_router import router as xxx_router
app.include_router(xxx_router, prefix="/EShangApiMain", tags=["实体中文名 (XXX)"])
```

---

## 定制检查清单

使用模板前，逐项确认：

- [ ] `TABLE_NAME` 和 `PRIMARY_KEY` 已替换为实际值
- [ ] `EXCLUDE_FIELDS` 参考原 Helper 的查询条件字段  
- [ ] `DATE_FIELDS` 列出所有日期类型字段
- [ ] `EXTRA_FIELDS` 对照 C# Model 补齐回显属性
- [ ] `STRING_FIELDS` 对照 C# Model 标注字符串字段
- [ ] 路由路径大小写与原 `[Route()]` 注解完全一致
- [ ] Service 中 SQL 参考原 Helper 而非自创
- [ ] Delete 方式已确认（软删除 vs 真删除）
- [ ] 文件头有 `from __future__ import annotations`
- [ ] 已在 `main.py` 注册路由

---

## 参考已完成文件

| 复杂度 | Service | Router |
|--------|---------|--------|
| 简单 CRUD（4接口） | `cashworker_service.py` | `cashworker_router.py` |
| 含关联查询（5接口） | `serverpartshop_service.py` | `serverpartshop_router.py` |
| 复杂业务（6接口） | `brand_service.py` | `brand_router.py` |
| 树形结构（6接口） | `businesstrade_service.py` | `businesstrade_router.py` |
