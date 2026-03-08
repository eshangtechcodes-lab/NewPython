from __future__ import annotations
# -*- coding: utf-8 -*-
"""
收银人员表业务服务
替代原 CashWorkerHelper.cs，保持相同的业务逻辑
对应 BaseInfoController 中 CASHWORKER 相关 4 个接口
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_CASHWORKER"
PRIMARY_KEY = "CASHWORKER_ID"

# Synchro 时需排除的字段（查询条件字段，非数据库列）
EXCLUDE_FIELDS = {"SERVERPART_IDS", "SERVERPART_CODES",
                  "OPERATE_DATE_Start", "OPERATE_DATE_End", "ServerPart_Name"}

# 日期字段
DATE_FIELDS = {"OPERATE_DATE"}


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


# ========== 1. GetCASHWORKERList ==========

def get_cashworker_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取收银人员表列表
    对应原 CashWorkerHelper.GetCASHWORKERList（L28-103）
    SQL: SELECT * FROM HIGHWAY_STORAGE.T_CASHWORKER + 动态 WHERE
    特殊处理：
    - SERVERPART_IDS → IN查询
    - SERVERPART_CODES → IN查询（字符串，需加引号）
    - OPERATE_DATE_Start / OPERATE_DATE_End → 日期范围
    注意：原C#在列表查询后会JOIN T_SERVERPART获取服务区名称
    返回: (总数, 数据列表)
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

        # 特殊处理：SERVERPART_IDS
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SERVERPART_ID IN ({sp_ids})"

        # 特殊处理：SERVERPART_CODES
        sp_codes = sp.get("SERVERPART_CODES")
        if sp_codes and str(sp_codes).strip():
            code_list = "','".join(str(sp_codes).split(","))
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"SERVERPART_CODE IN ('{code_list}')"

        # 操作时间范围
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

    # 关联服务区名称（对应原C#: dtServerPart.Select("SERVERPART_ID = xxx")）
    if rows:
        sp_ids_list = list(set(str(r.get("SERVERPART_ID")) for r in rows
                               if r.get("SERVERPART_ID") is not None))
        if sp_ids_list:
            sp_sql = f"SELECT SERVERPART_ID, SERVERPART_NAME FROM T_SERVERPART WHERE SERVERPART_ID IN ({','.join(sp_ids_list)})"
            sp_rows = db.execute_query(sp_sql)
            sp_map = {r.get("SERVERPART_ID"): r.get("SERVERPART_NAME") for r in sp_rows}
            for row in rows:
                row["ServerPart_Name"] = sp_map.get(row.get("SERVERPART_ID"), "")

    return int(total_count), rows


# ========== 2. GetCASHWORKERDetail ==========

def get_cashworker_detail(db: DatabaseHelper, cashworker_id: int) -> Optional[dict]:
    """
    获取收银人员表明细
    对应原 CashWorkerHelper.GetCASHWORKERDetail（L171-192）
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {cashworker_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroCASHWORKER ==========

def synchro_cashworker(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步收银人员表（新增或更新）
    对应原 CashWorkerHelper.SynchroCASHWORKER（L195-272）
    校验：员工工号(CASHWORKER_LOGINNAME) + 服务区(SERVERPART_ID) 不可重复
    返回: (是否成功, 数据对象)
    """
    record_id = data.get(PRIMARY_KEY)
    login_name = data.get("CASHWORKER_LOGINNAME")
    serverpart_id = data.get("SERVERPART_ID")

    # 验证必填字段
    if not login_name or serverpart_id is None:
        raise Exception("员工信息不完整，请填写后进行添加！")

    # 验证工号唯一性（同一服务区内不可重复）
    dup_sql = f"""SELECT {PRIMARY_KEY} FROM {TABLE_NAME}
        WHERE SERVERPART_ID = {serverpart_id}
        AND CASHWORKER_LOGINNAME = '{login_name}'"""
    dup_rows = db.execute_query(dup_sql)
    if dup_rows:
        existing_id = dup_rows[0].get(PRIMARY_KEY)
        if record_id is None or existing_id != record_id:
            raise Exception("员工编码已存在，请勿重复添加！")

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # 更新模式
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
        # 新增模式
        try:
            new_id = db.execute_scalar("SELECT SEQ_CASHWORKER.NEXTVAL FROM DUAL")
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


# ========== 4. DeleteCASHWORKER ==========

def delete_cashworker(db: DatabaseHelper, cashworker_id: int) -> bool:
    """
    删除收银人员表
    对应原 CashWorkerHelper.DeleteCASHWORKER（L275-291）
    注意：原 C# 该方法为空实现（始终返回 false），这里保持一致
    """
    # 原 C# 代码空实现，CASHWORKERId != null 时不做任何操作
    # 保持一致性，始终返回 false
    return False
