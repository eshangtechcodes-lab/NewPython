from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区类别关联表业务服务
严格参照原 C# SPSTATICTYPEHelper.cs 中的实现逻辑
使用 HIGHWAY_STORAGE.T_SPSTATICTYPE 表（仅 3 个字段：SPSTATICTYPE_ID, SERVERPART_ID, SERVERPARTTYPE_ID）
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_SPSTATICTYPE"
PRIMARY_KEY = "SPSTATICTYPE_ID"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """构建 WHERE 条件"""
    conditions = []
    for key, value in search_param.items():
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
    """构建关键字过滤条件"""
    if not keyword or not keyword.get("Key") or not keyword.get("Value"):
        return ""
    keys = keyword["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{keyword['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


def get_spstatictype_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区类别关联表列表
    对应 C# SPSTATICTYPEHelper.GetSPSTATICTYPEList
    """
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter, search_model.QueryType or 0
        )
        if where_clause:
            where_sql = f" WHERE {where_clause}"

    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    if search_model.keyWord:
        keyword_filter = _build_keyword_filter(
            search_model.keyWord.model_dump() if hasattr(search_model.keyWord, 'model_dump') else search_model.keyWord
        )
        if keyword_filter:
            if where_sql:
                base_sql += f" AND ({keyword_filter})"
            else:
                base_sql += f" WHERE ({keyword_filter})"

    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    if search_model.SortStr:
        base_sql += f" ORDER BY {search_model.SortStr}"

    page_index = search_model.PageIndex
    page_size = search_model.PageSize

    if page_index <= 0 or page_size <= 0:
        limit_sql = f"SELECT * FROM ({base_sql}) WHERE ROWNUM <= 10"
        rows = db.execute_query(limit_sql)
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


def get_spstatictype_detail(db: DatabaseHelper, spstatictype_id: int) -> Optional[dict]:
    """获取服务区类别关联表明细"""
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {spstatictype_id}"
    rows = db.execute_query(sql)
    if rows:
        return rows[0]
    return None


def synchro_spstatictype(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步服务区类别关联表（新增/更新）
    对应 C# SPSTATICTYPEHelper.SynchroSPSTATICTYPE
    """
    spstatictype_id = data.get("SPSTATICTYPE_ID")

    if spstatictype_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {spstatictype_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, None

        set_parts = []
        for key, value in data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {spstatictype_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["SPSTATICTYPE_ID"] = new_id

        columns = []
        values = []
        for key, value in data.items():
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


def delete_spstatictype(db: DatabaseHelper, spstatictype_id: int) -> bool:
    """
    删除服务区类别关联表（真删除）
    对应 C# SPSTATICTYPEHelper.DeleteSPSTATICTYPE
    原 C# 逻辑：Select() 确认存在 → Delete()
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {spstatictype_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    del_sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {spstatictype_id}"
    db.execute_non_query(del_sql)
    return True
