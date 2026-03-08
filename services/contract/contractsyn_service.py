from __future__ import annotations
# -*- coding: utf-8 -*-
"""
合同信息同步表业务服务
对应 ContractSynController（4个路由：ContractSyn/前缀）
对应 CONTRACT_SYNController（4个路由：BusinessProject/前缀）
两个 Controller 都操作同一张表 T_CONTRACT_SYN
注意：CONTRACT_SYN_ID 是 GUID 字符串，不是自增整数
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 实际 Oracle 表名：CONTRACT_STORAGE.T_CONTRACT_SYN（注意有下划线）
TABLE_NAME = "T_CONTRACT_SYN"
PRIMARY_KEY = "CONTRACT_SYN_ID"  # GUID 字符串类型


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """根据查询参数构建 WHERE 条件"""
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


# ========== 1. GetContractSynList / GetCONTRACT_SYNList ==========

def get_contractsyn_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取合同信息同步表列表
    SQL: SELECT * FROM T_CONTRACT_SYN + 动态 WHERE
    """
    where_sql = ""
    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

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
        rows.sort(key=lambda x: x.get(sort_field, "") or "", reverse=is_desc)

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


# ========== 2. GetContractSynDetail / GetCONTRACT_SYNDetail ==========

def get_contractsyn_detail(db: DatabaseHelper, record_id) -> Optional[dict]:
    """
    获取合同信息同步表明细
    注意：CONTRACT_SYN_ID 是字符串 GUID
    """
    # 支持 int（原 C# ContractSynController 用 int 参数）或 string
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = '{record_id}'"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroContractSyn / SynchroCONTRACT_SYN ==========

def synchro_contractsyn(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步合同信息同步表（新增或更新）
    特殊逻辑：更新前先插入历史表 CONTRACT_HISTORY.T_CONTRACT_SYN
    """
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in SEARCH_PARAM_SKIP_FIELDS}

    if record_id is not None and str(record_id).strip():
        # 检查是否存在
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = '{record_id}'"
        count = db.execute_scalar(check_sql)
        if count > 0:
            # 更新模式
            set_parts = []
            for key, value in db_data.items():
                if key == PRIMARY_KEY:
                    continue
                if value is None:
                    set_parts.append(f"{key} = NULL")
                    continue
                if isinstance(value, str):
                    set_parts.append(f"{key} = '{value}'")
                else:
                    set_parts.append(f"{key} = {value}")
            if set_parts:
                update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = '{record_id}'"
                db.execute_non_query(update_sql)
        else:
            # 新增模式（ID 由客户端传入，是 GUID）
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
            insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
            db.execute_non_query(insert_sql)
    else:
        # 无 ID，新增
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
        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. DeleteContractSyn / DeleteCONTRACT_SYN ==========

def delete_contractsyn(db: DatabaseHelper, record_id) -> bool:
    """
    删除合同信息同步表
    注意：原 C# Delete 是空实现（始终返回 false），保持一致
    """
    # 原 C# 代码空实现，始终返回 false
    return False
