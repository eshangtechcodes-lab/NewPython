from __future__ import annotations
# -*- coding: utf-8 -*-
"""
物业资产操作日志表服务
替代原 PROPERTYASSETSLOGHelper.cs，保持相同的业务逻辑

接口列表（2个）：
- GetPROPERTYASSETSLOGList: POST, 分页列表查询
- SynchroPROPERTYASSETSLOG: POST, 同步（新增/更新）

表: HIGHWAY_STORAGE.T_PROPERTYASSETSLOG
序列: SEQ_PROPERTYASSETSLOG（达梦无权限，使用 MAX+1 降级）
"""
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS

# 表名常量
TABLE_NAME = "T_PROPERTYASSETSLOG"
PRIMARY_KEY = "PROPERTYASSETSLOG_ID"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    query_type: 0=模糊查询, 1=精确查询
    """
    conditions = []
    for key, value in search_param.items():
        if key in SEARCH_PARAM_SKIP_FIELDS:
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


def _build_keyword_filter(keyword: dict) -> str:
    """构建关键字过滤条件（对应原 C# 的 RowFilter 模糊搜索）"""
    if not keyword or not keyword.get("Key") or not keyword.get("Value"):
        return ""
    keys = keyword["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{keyword['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


def get_propertyassetslog_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取物业资产操作日志表列表
    对应原 PROPERTYASSETSLOGHelper.GetPROPERTYASSETSLOGList

    原 C# 逻辑：
    1. SELECT * FROM T_PROPERTYASSETSLOG + WHERE 条件
    2. 内存关键字模糊搜索（RowFilter）
    3. 排序（SortStr）
    4. 分页（PageIndex, PageSize）

    返回: (总数, 数据列表)
    """
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter,
            search_model.QueryType or 0
        )
        if where_clause:
            where_sql = f" WHERE {where_clause}"

    # 基础查询 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 添加关键字过滤（对应原 C# 的 keyWord.Key/Value）
    if search_model.keyWord:
        keyword_filter = _build_keyword_filter(search_model.keyWord.model_dump())
        if keyword_filter:
            if where_sql:
                base_sql += f" AND ({keyword_filter})"
            else:
                base_sql += f" WHERE ({keyword_filter})"

    # 查询总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 添加排序
    if search_model.SortStr:
        base_sql += f" ORDER BY {search_model.SortStr}"

    # 分页处理
    page_index = search_model.PageIndex
    page_size = search_model.PageSize

    if page_index <= 0 or page_size <= 0:
        rows = db.execute_query(base_sql)
    else:
        start_row = (page_index - 1) * page_size + 1
        end_row = page_index * page_size
        paged_sql = f"""
            SELECT * FROM (
                SELECT A.*, ROWNUM RN FROM ({base_sql}) A
                WHERE ROWNUM <= {end_row}
            ) WHERE RN >= {start_row}
        """
        rows = db.execute_query(paged_sql)
        for row in rows:
            row.pop("RN", None)

    return int(total_count), rows


def synchro_propertyassetslog(db: DatabaseHelper, model: dict) -> bool:
    """
    同步物业资产操作日志表（新增/更新）
    对应原 PROPERTYASSETSLOGHelper.SynchroPROPERTYASSETSLOG

    原 C# 逻辑：
    1. 有 PROPERTYASSETSLOG_ID → 检查是否存在 → 存在则更新，不存在则返回 false
    2. 无 PROPERTYASSETSLOG_ID → 序列获取新 ID → 插入
    序列无权限时使用 MAX+1 降级

    返回: 是否成功
    """
    propertyassetslog_id = model.get("PROPERTYASSETSLOG_ID")

    if propertyassetslog_id is not None:
        # 更新：先检查是否存在
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {propertyassetslog_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False

        # 构建 UPDATE
        set_parts = []
        for key, value in model.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                set_parts.append(f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {propertyassetslog_id}"
            db.execute_non_query(update_sql)
        return True
    else:
        # 新增：使用 MAX+1 降级（序列无权限）
        id_sql = f"SELECT COALESCE(MAX({PRIMARY_KEY}), 0) + 1 FROM {TABLE_NAME}"
        new_id = db.execute_scalar(id_sql)
        model["PROPERTYASSETSLOG_ID"] = new_id

        cols = []
        vals = []
        for key, value in model.items():
            if value is None:
                continue
            cols.append(key)
            if isinstance(value, str):
                vals.append(f"'{value}'")
            else:
                vals.append(str(value))

        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        db.execute_non_query(insert_sql)
        return True
