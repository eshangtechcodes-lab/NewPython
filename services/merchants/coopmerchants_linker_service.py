from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营商户联系人业务服务
替代原 COOPMERCHANTS_LINKERHelper.cs
对应 MerchantsController 中 COOPMERCHANTS_LINKER 相关 4 个接口
"""
from typing import Optional
from datetime import datetime as _dt
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_COOPMERCHANTS_LINKER"
PRIMARY_KEY = "COOPMERCHANTS_LINKER_ID"

# 日期字段
DATE_FIELDS = {"OPERATE_DATE"}
# 非数据库字段（在搜索/同步中跳过）
EXCLUDE_FIELDS = {"current", "pageSize", "total"}

# C# Model 中 System.String 类型的字段（.ToString() → DBNull变''}）
_STR_FIELDS = {
    "BANK_NAME", "BANK_ACCOUNT", "COOPMERCHANTS_DRAWER",
    "LINKER_NAME", "LINKER_TELEPHONE", "LINKER_MOBILEPHONE",
    "LINKER_ADDRESS", "STAFF_NAME", "COOPMERCHANTS_LINKER_DESC",
}


def _bind_linker_row(row: dict) -> dict:
    """对照 C# Helper 的 field-by-field 绑定"""
    for f in _STR_FIELDS:
        if f in row and row[f] is None:
            row[f] = ""
    # 日期格式由 database.py 统一处理为 ISO 格式（与 C# 一致）
    return row


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """构建 WHERE 条件"""
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


# ========== 1. GetCoopMerchantsLinkerList ==========

def get_coopmerchants_linker_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取经营商户联系人列表
    对应原 COOPMERCHANTS_LINKERHelper.GetCOOPMERCHANTS_LINKERList
    SQL: SELECT * FROM T_COOPMERCHANTS_LINKER {WhereSQL}
    默认排序: 无（原 C# DefaultView.Sort = searchModel.SortStr，无默认值）
    """
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(search_model.SearchParameter, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    rows = db.execute_query(base_sql)

    # 关键字过滤
    if search_model.keyWord:
        if hasattr(search_model.keyWord, 'model_dump'):
            kw = search_model.keyWord.model_dump()
        else:
            kw = search_model.keyWord
        if kw.get("Key") and kw.get("Value"):
            search_value = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(
                search_value in str(r.get(k, "")) for k in keys
            )]

    # 排序
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)

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

    for row in rows:
        _bind_linker_row(row)

    return int(total_count), rows


# ========== 2. GetCoopMerchantsLinkerDetail ==========

def get_coopmerchants_linker_detail(db: DatabaseHelper, linker_id: int) -> Optional[dict]:
    """
    获取经营商户联系人明细
    对应原 COOPMERCHANTS_LINKERHelper.GetCOOPMERCHANTS_LINKERDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {linker_id}"
    # C# Detail 直接赋 entity 属性，null string 保持 null
    rows = db.execute_query(sql, null_to_empty=False)
    if not rows:
        return None
    detail = rows[0]
    # 日期格式由 database.py 统一处理为 ISO 格式（与 C# 一致）
    return detail


# ========== 3. SynchroCoopMerchantsLinker ==========

def synchro_coopmerchants_linker(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步经营商户联系人（新增或更新）
    对应原 COOPMERCHANTS_LINKERHelper.SynchroCOOPMERCHANTS_LINKER
    """
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # === 更新模式 ===
        exist_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}"
        count = db.execute_scalar(exist_sql)
        if count == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
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
            new_id = db.execute_scalar("SELECT SEQ_COOPMERCHANTS_LINKER.NEXTVAL FROM DUAL")
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


# ========== 4. DeleteCoopMerchantsLinker ==========

def delete_coopmerchants_linker(db: DatabaseHelper, linker_id: int) -> bool:
    """
    删除经营商户联系人（真删除: DELETE）
    对应原 COOPMERCHANTS_LINKERHelper.DeleteCOOPMERCHANTS_LINKER
    """
    # 先检查是否存在
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {linker_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False
    delete_sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {linker_id}"
    db.execute_non_query(delete_sql)
    return True
