from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店变更日志表业务服务
替代原 SERVERPARTSHOP_LOGHelper.cs
对应 BaseInfoController 中 SERVERPARTSHOP_LOG 相关 1 个接口
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_SERVERPARTSHOP_LOG"

# GetWhereSQL 中排除的字段（特殊处理）
EXCLUDE_FIELDS = {"SERVERPARTSHOP_IDS", "SHOPTRADES", "SERVERPART_IDS",
                  "OPERATE_DATE_Start", "OPERATE_DATE_End"}


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


# ========== 1. GetSERVERPARTSHOP_LOGList ==========

def get_serverpartshop_log_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取门店变更日志表列表
    对应原 SERVERPARTSHOP_LOGHelper.GetSERVERPARTSHOP_LOGList（L24-99）
    SQL: SELECT * FROM HIGHWAY_STORAGE.T_SERVERPARTSHOP_LOG + 动态 WHERE
    特殊处理：
    - SERVERPARTSHOP_IDS → IN查询
    - SHOPTRADES → IN查询（字符串，需加引号）
    - SERVERPART_IDS → IN查询
    - OPERATE_DATE_Start / OPERATE_DATE_End → 日期范围查询
    返回: (总数, 数据列表)
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        # 通用条件构建
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

        # 特殊处理：SERVERPARTSHOP_IDS
        shop_ids = sp.get("SERVERPARTSHOP_IDS")
        if shop_ids and str(shop_ids).strip():
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SERVERPARTSHOP_ID IN ({shop_ids})"

        # 特殊处理：SHOPTRADES（字符串 IN 查询，需加引号）
        shoptrades = sp.get("SHOPTRADES")
        if shoptrades and str(shoptrades).strip():
            # 将 "a,b,c" 转为 "'a','b','c'"
            trade_list = "','".join(str(shoptrades).split(","))
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SHOPTRADE IN ('{trade_list}')"

        # 特殊处理：SERVERPART_IDS
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SERVERPART_ID IN ({sp_ids})"

        # 特殊处理：操作时间范围
        date_start = sp.get("OPERATE_DATE_Start")
        if date_start and str(date_start).strip():
            date_val = str(date_start).split(" ")[0]
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"OPERATE_DATE >= TO_DATE('{date_val}', 'YYYY/MM/DD')"

        date_end = sp.get("OPERATE_DATE_End")
        if date_end and str(date_end).strip():
            date_val = str(date_end).split(" ")[0]
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"OPERATE_DATE < TO_DATE('{date_val}', 'YYYY/MM/DD') + 1"

    # 执行查询
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
            rows = [r for r in rows if any(
                search_value in str(r.get(k, "")) for k in keys
            )]

    # 排序
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field, 0) or 0, reverse=is_desc)

    # 总数
    total_count = len(rows)

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    return int(total_count), rows
