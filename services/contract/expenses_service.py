from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商家预缴费用 + 费用拆分 业务服务
替代原 EXPENSESPREPAIDHelper.cs + EXPENSESSEPARATEHelper.cs
对应 ExpensesController 中 8 个 CRUD 接口
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# =====================================================
# EXPENSESPREPAID（商家预缴费用表）
# =====================================================
PREPAID_TABLE = "T_EXPENSESPREPAID"
PREPAID_PK = "EXPENSESPREPAID_ID"

# Synchro 时需排除的字段（查询条件字段，非数据库列）
PREPAID_EXCLUDE_FIELDS = {"PREPAID_DATE_Start", "PREPAID_DATE_End"}

# 日期字段（SUBSTR 方式存储 yyyyMMdd，不同于 TO_DATE）
PREPAID_DATE_FIELDS = {"PREPAID_DATE"}


def _build_where_sql(search_param: dict, query_type: int = 0,
                     exclude_fields: set = None,
                     date_range_fields: list = None) -> str:
    """根据查询参数构建通用 WHERE 条件"""
    if exclude_fields is None:
        exclude_fields = set()
    conditions = []
    for key, value in search_param.items():
        if key in exclude_fields or key in SEARCH_PARAM_SKIP_FIELDS:
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


# ========== 1. GetEXPENSESPREPAIDList ==========

def get_expensesprepaid_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取商家预缴费用表列表
    对应原 EXPENSESPREPAIDHelper.GetEXPENSESPREPAIDList
    SQL: SELECT * FROM T_EXPENSESPREPAID + 动态 WHERE
    特殊处理：PREPAID_DATE_Start/End → SUBSTR(PREPAID_DATE,1,8) 范围查询
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0,
                                        PREPAID_EXCLUDE_FIELDS)
        if where_clause:
            where_sql = " WHERE " + where_clause

        # 预缴日期范围查询（原 C# 使用 SUBSTR(PREPAID_DATE,1,8)）
        date_start = sp.get("PREPAID_DATE_Start")
        if date_start and str(date_start).strip():
            try:
                date_val = datetime.strptime(str(date_start).split(" ")[0].replace("-", "/"),
                                             "%Y/%m/%d").strftime("%Y%m%d")
            except Exception:
                date_val = str(date_start).replace("/", "").replace("-", "")[:8]
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SUBSTR(PREPAID_DATE,1,8) >= '{date_val}'"

        date_end = sp.get("PREPAID_DATE_End")
        if date_end and str(date_end).strip():
            try:
                date_val = datetime.strptime(str(date_end).split(" ")[0].replace("-", "/"),
                                             "%Y/%m/%d").strftime("%Y%m%d")
            except Exception:
                date_val = str(date_end).replace("/", "").replace("-", "")[:8]
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SUBSTR(PREPAID_DATE,1,8) <= '{date_val}'"

    # 执行查询
    base_sql = f"SELECT * FROM {PREPAID_TABLE}{where_sql}"
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


# ========== 2. GetEXPENSESPREPAIDDetail ==========

def get_expensesprepaid_detail(db: DatabaseHelper, prepaid_id: int) -> Optional[dict]:
    """
    获取商家预缴费用表明细
    对应原 EXPENSESPREPAIDHelper.GetEXPENSESPREPAIDDetail
    """
    sql = f"SELECT * FROM {PREPAID_TABLE} WHERE {PREPAID_PK} = {prepaid_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroEXPENSESPREPAID ==========

def synchro_expensesprepaid(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步商家预缴费用表（新增或更新）
    对应原 EXPENSESPREPAIDHelper.SynchroEXPENSESPREPAID
    日期字段 PREPAID_DATE 特殊处理：存储为 yyyyMMdd 格式
    """
    record_id = data.get(PREPAID_PK)

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items()
               if k not in PREPAID_EXCLUDE_FIELDS and k not in SEARCH_PARAM_SKIP_FIELDS}

    # 处理 PREPAID_DATE（原 C# 将日期转为 yyyyMMdd 格式存储）
    prepaid_date = db_data.get("PREPAID_DATE")
    if prepaid_date and str(prepaid_date).strip():
        try:
            dt = datetime.strptime(str(prepaid_date).split(" ")[0].replace("-", "/"), "%Y/%m/%d")
            db_data["PREPAID_DATE"] = dt.strftime("%Y%m%d")
        except Exception:
            pass  # 保持原值
    elif prepaid_date is not None and str(prepaid_date).strip() == "":
        db_data["PREPAID_DATE"] = None

    if record_id is not None:
        # 更新模式
        check_sql = f"SELECT COUNT(*) FROM {PREPAID_TABLE} WHERE {PREPAID_PK} = {record_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == PREPAID_PK:
                continue
            if value is None:
                set_parts.append(f"{key} = NULL")
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            update_sql = f"UPDATE {PREPAID_TABLE} SET {', '.join(set_parts)} WHERE {PREPAID_PK} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增模式
        try:
            new_id = db.execute_scalar("SELECT SEQ_EXPENSESPREPAID.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PREPAID_PK}) FROM {PREPAID_TABLE}") or 0) + 1
        data[PREPAID_PK] = new_id
        db_data[PREPAID_PK] = new_id

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
        insert_sql = f"INSERT INTO {PREPAID_TABLE} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. DeleteEXPENSESPREPAID ==========

def delete_expensesprepaid(db: DatabaseHelper, prepaid_id: int) -> bool:
    """
    删除商家预缴费用表（软删除，STATE=0）
    对应原 EXPENSESPREPAIDHelper.DeleteEXPENSESPREPAID
    """
    sql = f"UPDATE {PREPAID_TABLE} SET EXPENSESPREPAID_STATE = 0 WHERE {PREPAID_PK} = {prepaid_id}"
    affected = db.execute_non_query(sql)
    return affected > 0


# =====================================================
# EXPENSESSEPARATE（商家预缴费用拆分表）
# =====================================================
SEPARATE_TABLE = "T_EXPENSESSEPARATE"
SEPARATE_PK = "EXPENSESSEPARATE_ID"

# 拆分表无需排除的特殊字段，也没有日期字段需要特殊处理
SEPARATE_EXCLUDE_FIELDS = set()


# ========== 5. GetEXPENSESSEPARATEList ==========

def get_expensesseparate_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取商家预缴费用拆分表列表
    对应原 EXPENSESSEPARATEHelper.GetEXPENSESSEPARATEList
    SQL: SELECT * FROM T_EXPENSESSEPARATE + 动态 WHERE
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0,
                                        SEPARATE_EXCLUDE_FIELDS)
        if where_clause:
            where_sql = " WHERE " + where_clause

    base_sql = f"SELECT * FROM {SEPARATE_TABLE}{where_sql}"
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


# ========== 6. GetEXPENSESSEPARATEDetail ==========

def get_expensesseparate_detail(db: DatabaseHelper, separate_id: int) -> Optional[dict]:
    """
    获取商家预缴费用拆分表明细
    对应原 EXPENSESSEPARATEHelper.GetEXPENSESSEPARATEDetail
    """
    sql = f"SELECT * FROM {SEPARATE_TABLE} WHERE {SEPARATE_PK} = {separate_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 7. SynchroEXPENSESSEPARATE ==========

def synchro_expensesseparate(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步商家预缴费用拆分表（新增或更新）
    对应原 EXPENSESSEPARATEHelper.SynchroEXPENSESSEPARATE
    无特殊日期字段处理
    """
    record_id = data.get(SEPARATE_PK)

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in SEARCH_PARAM_SKIP_FIELDS}

    if record_id is not None:
        # 更新模式
        check_sql = f"SELECT COUNT(*) FROM {SEPARATE_TABLE} WHERE {SEPARATE_PK} = {record_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == SEPARATE_PK:
                continue
            if value is None:
                set_parts.append(f"{key} = NULL")
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            update_sql = f"UPDATE {SEPARATE_TABLE} SET {', '.join(set_parts)} WHERE {SEPARATE_PK} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增模式
        try:
            new_id = db.execute_scalar("SELECT SEQ_EXPENSESSEPARATE.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({SEPARATE_PK}) FROM {SEPARATE_TABLE}") or 0) + 1
        data[SEPARATE_PK] = new_id
        db_data[SEPARATE_PK] = new_id

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
        insert_sql = f"INSERT INTO {SEPARATE_TABLE} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 8. DeleteEXPENSESSEPARATE ==========

def delete_expensesseparate(db: DatabaseHelper, separate_id: int) -> bool:
    """
    删除商家预缴费用拆分表（软删除，STATE=0）
    对应原 EXPENSESSEPARATEHelper.DeleteEXPENSESSEPARATE
    """
    sql = f"UPDATE {SEPARATE_TABLE} SET EXPENSESSEPARATE_STATE = 0 WHERE {SEPARATE_PK} = {separate_id}"
    affected = db.execute_non_query(sql)
    return affected > 0


# =====================================================
# 特殊接口：GetShopExpenseHisList（门店费用变更记录）
# =====================================================

def get_shop_expense_his_list(db: DatabaseHelper, search_model: SearchModel,
                              serverpart_ids: str = None) -> tuple:
    """
    获取门店费用变更记录
    对应原 ExpensesController.GetShopExpenseHisList
    复用 SHOPEXPENSEHelper.GetSHOPEXPENSEList（已在 bp_batch4 中实现）
    Header 参数：ProvinceCode, ServerpartCodes → 获取 SERVERPART_IDS
    """
    from services.business_project import shopexpense_service

    # 如果 SearchParameter 中没有 SERVERPART_IDS，使用传入的
    if search_model.SearchParameter is None:
        search_model.SearchParameter = {}
    if not search_model.SearchParameter.get("SERVERPART_IDS") and serverpart_ids:
        search_model.SearchParameter["SERVERPART_IDS"] = serverpart_ids

    return shopexpense_service.get_shopexpense_list(db, search_model)
