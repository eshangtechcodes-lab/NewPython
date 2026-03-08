from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营商户经营项目执行情况表业务服务
替代原 BUSINESSPAYMENTHelper.cs，保持相同的业务逻辑
对应 BusinessProjectController 中 BUSINESSPAYMENT 相关 4 个接口
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_BUSINESSPAYMENT"
PRIMARY_KEY = "BUSINESSPAYMENT_ID"

# Synchro 时需排除的字段（查询条件字段，非数据库列）
EXCLUDE_FIELDS = set()

# 搜索参数中需跳过的通用字段
SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


# ========== 1. GetBUSINESSPAYMENTList ==========

def get_businesspayment_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取经营项目执行情况表列表
    对应原 BUSINESSPAYMENTHelper.GetBUSINESSPAYMENTList
    SQL: SELECT * FROM T_BUSINESSPAYMENT + WHERE 条件
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        conditions = []
        for k, v in sp.items():
            if k in EXCLUDE_FIELDS or k in SEARCH_PARAM_SKIP_FIELDS:
                continue
            if v is None or (isinstance(v, str) and v.strip() == ""):
                continue
            qt = search_model.QueryType or 0
            if qt == 0 and isinstance(v, str):
                conditions.append(f"{k} LIKE '%{v}%'")
            elif isinstance(v, str):
                conditions.append(f"{k} = '{v}'")
            else:
                conditions.append(f"{k} = {v}")
        if conditions:
            where_sql = " WHERE " + " AND ".join(conditions)

    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME}{where_sql}")

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
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "desc" in (search_model.SortStr or "").lower()
        try:
            rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)
        except Exception:
            pass

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


# ========== 2. GetBUSINESSPAYMENTDetail ==========

def get_businesspayment_detail(db: DatabaseHelper, bp_id: int) -> Optional[dict]:
    """
    获取经营项目执行情况表明细
    对应原 BUSINESSPAYMENTHelper.GetBUSINESSPAYMENTDetail
    """
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {bp_id}")
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroBUSINESSPAYMENT ==========

def synchro_businesspayment(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步经营项目执行情况表（新增或更新）
    对应原 BUSINESSPAYMENTHelper.SynchroBUSINESSPAYMENT
    无排除字段，无日期 TO_DATE 处理（日期存储为数字格式）
    """
    record_id = data.get(PRIMARY_KEY)

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # 更新模式
        check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}")
        if check == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}")
    else:
        # 新增模式
        try:
            new_id = db.execute_scalar("SELECT SEQ_BUSINESSPAYMENT.NEXTVAL FROM DUAL")
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
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    return True, data


# ========== 4. DeleteBUSINESSPAYMENT ==========

def delete_businesspayment(db: DatabaseHelper, bp_id: int) -> bool:
    """
    删除经营项目执行情况表（软删除 BUSINESSPAYMENT_STATUS = 0）
    对应原 BUSINESSPAYMENTHelper.DeleteBUSINESSPAYMENT
    """
    # 先检查是否存在
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {bp_id}")
    if check == 0:
        return False
    affected = db.execute_non_query(
        f"UPDATE {TABLE_NAME} SET BUSINESSPAYMENT_STATUS = 0 WHERE {PRIMARY_KEY} = {bp_id}")
    return affected > 0
