from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区站点业务服务
替代原 ServerpartHelper.cs，保持相同的业务逻辑
注意：SERVERPART 只有 GetList 和 Delete 两个标准接口
Delete 为真删除（_SERVERPART.Delete()），非软删除
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_SERVERPART"
PRIMARY_KEY = "SERVERPART_ID"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    query_type: 0=模糊查询, 1=精确查询
    额外处理 SERVERPART_IDS 和 SERVERPART_CODES 字段（原 C# 中做了特殊处理）
    """
    conditions = []
    for key, value in search_param.items():
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        # SERVERPART_IDS 和 SERVERPART_CODES 不走普通查询逻辑，单独处理
        if key in ("SERVERPART_IDS", "SERVERPART_CODES"):
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
    """构建关键字过滤条件"""
    if not keyword or not keyword.get("Key") or not keyword.get("Value"):
        return ""
    keys = keyword["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{keyword['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


def get_serverpart_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区站点列表
    对应原 ServerpartHelper.GetSERVERPARTList
    返回: (总数, 数据列表)
    """
    # 构建 WHERE 条件
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter,
            search_model.QueryType or 0
        )
        if where_clause:
            where_sql = f" WHERE {where_clause}"

        # 特殊处理 SERVERPART_IDS：IN 查询
        serverpart_ids = search_model.SearchParameter.get("SERVERPART_IDS")
        if serverpart_ids and str(serverpart_ids).strip():
            extra = f"SERVERPART_ID IN ({serverpart_ids})"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

        # 特殊处理 SERVERPART_CODES：IN 查询
        serverpart_codes = search_model.SearchParameter.get("SERVERPART_CODES")
        if serverpart_codes and str(serverpart_codes).strip():
            codes = "','".join(str(serverpart_codes).split(","))
            extra = f"SERVERPART_CODE IN ('{codes}')"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

    # 构建基础查询 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 添加关键字过滤
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


def delete_serverpart(db: DatabaseHelper, serverpart_id: int) -> bool:
    """
    删除服务区站点（真删除）
    对应原 ServerpartHelper.DeleteSERVERPART
    注意：原 C# 代码是真删除 _SERVERPART.Delete()，非软删除
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpart_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpart_id}"
    db.execute_non_query(sql)
    return True
