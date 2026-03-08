from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店经营时间表业务服务
替代原 RTSERVERPARTSHOPHelper.cs，保持相同的业务逻辑
对应 BaseInfoController 中 RTSERVERPARTSHOP 相关 4 个接口
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_RTSERVERPARTSHOP"
PRIMARY_KEY = "RTSERVERPARTSHOP_ID"

# Synchro 时需排除的字段（查询条件字段，非数据库列）
EXCLUDE_FIELDS = {"SERVERPARTSHOP_IDS", "BUSINESS_TYPES"}

# 日期字段列表（Synchro 时使用 TO_DATE 处理）
DATE_FIELDS = {"BUSINESS_DATE", "BUSINESS_ENDDATE", "OPERATE_DATE"}


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    对应原 OperationDataHelper.GetWhereSQL 通用方法
    排除 SERVERPARTSHOP_IDS 和 BUSINESS_TYPES（由业务层特殊处理）
    """
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS:

            continue

        if value is None:

            continue

        if isinstance(value, str) and value.strip() == "":

            continue

        if query_type == 0 and isinstance(value, str):
            # 模糊查询
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            # 精确查询
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
    return " AND ".join(conditions)


# ========== 1. GetRTSERVERPARTSHOPList ==========

def get_rtserverpartshop_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取门店经营时间表列表
    对应原 RTSERVERPARTSHOPHelper.GetRTSERVERPARTSHOPList（L24-83）
    SQL: SELECT * FROM HIGHWAY_STORAGE.T_RTSERVERPARTSHOP + 动态 WHERE
    特殊处理：SERVERPARTSHOP_IDS（IN查询）、BUSINESS_TYPES（IN查询）
    返回: (总数, 数据列表)
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        # 通用条件构建
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

        # 特殊处理：SERVERPARTSHOP_IDS（门店内码批量查询）
        shop_ids = sp.get("SERVERPARTSHOP_IDS")
        if shop_ids and str(shop_ids).strip():
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SERVERPARTSHOP_ID IN ({shop_ids})"

        # 特殊处理：BUSINESS_TYPES（经营模式批量查询）
        biz_types = sp.get("BUSINESS_TYPES")
        if biz_types and str(biz_types).strip():
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"BUSINESS_TYPE IN ({biz_types})"

    # 执行查询
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    rows = db.execute_query(base_sql)

    # 关键字过滤（模拟原 DataView.RowFilter）
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

    # 分页（对应原 CommonHelper.GetDataTableWithPageSize）
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]  # 默认返回前 10 条

    return int(total_count), rows


# ========== 2. GetRTSERVERPARTSHOPDetail ==========

def get_rtserverpartshop_detail(db: DatabaseHelper, rtserverpartshop_id: int) -> Optional[dict]:
    """
    获取门店经营时间表明细
    对应原 RTSERVERPARTSHOPHelper.GetRTSERVERPARTSHOPDetail（L163-184）
    SQL: SELECT * FROM T_RTSERVERPARTSHOP WHERE RTSERVERPARTSHOP_ID = ?
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {rtserverpartshop_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroRTSERVERPARTSHOP ==========

def synchro_rtserverpartshop(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步门店经营时间表（新增或更新）
    对应原 RTSERVERPARTSHOPHelper.SynchroRTSERVERPARTSHOP（L187-267）
    新增时使用序列 SEQ_RTSERVERPARTSHOP，失败降级为 MAX(ID)+1
    日期字段使用 TO_DATE 处理
    返回: (是否成功, 数据对象)
    """
    record_id = data.get(PRIMARY_KEY)

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # 更新模式：先检查记录是否存在
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
                # 日期字段使用 TO_DATE
                set_parts.append(f"{key} = TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增模式（序列 → MAX+1 降级）
        try:
            new_id = db.execute_scalar("SELECT SEQ_RTSERVERPARTSHOP.NEXTVAL FROM DUAL")
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


# ========== 4. DeleteRTSERVERPARTSHOP ==========

def delete_rtserverpartshop(db: DatabaseHelper, rtserverpartshop_id: int) -> bool:
    """
    删除门店经营时间表（真删除）
    对应原 RTSERVERPARTSHOPHelper.DeleteRTSERVERPARTSHOP（L270-292）
    注意：原 C# 使用 _RTSERVERPARTSHOP.Delete()，即真删除
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {rtserverpartshop_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False
    sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {rtserverpartshop_id}"
    db.execute_non_query(sql)
    return True
