from __future__ import annotations
# -*- coding: utf-8 -*-
"""
业主单位服务区关联关系表业务服务
严格参照原 C# OWNERSERVERPARTHelper.cs 中的实现逻辑
使用 MOBILESERVICE_PLATFORM.T_OWNERSERVERPART 表（达梦中为 T_OWNERSERVERPART）
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_OWNERSERVERPART"
PRIMARY_KEY = "OWNERSERVERPART_ID"

# 同步时排除的字段（原 C# excludeField: "ShopList", "AUTOTYPE_IDS"）
EXCLUDE_FIELDS = {"ShopList", "AUTOTYPE_IDS"}

# 字符串字段（原 C# BindDataRowToModel 中 .ToString() 赋值的字段）
STR_FIELDS = [
    "AUTOTYPE_NAME", "OWNERUNIT_NAME", "SERVERPART_CODE",
    "SERVERPART_NAME", "STAFF_NAME", "OWNERSERVERPART_DESC"
]


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    构建 WHERE 条件
    对应 C# OperationDataHelper.GetWhereSQL(searchModel.SearchParameter, searchModel.QueryType, "", "ShopList", "AUTOTYPE_IDS")
    排除 ShopList 和 AUTOTYPE_IDS 字段
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


def _process_row(row: dict) -> dict:
    """处理单行数据，对应 C# BindDataRowToModel"""
    for field in STR_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    return row


def get_ownerserverpart_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取业主单位服务区关联关系表列表
    对应 C# OWNERSERVERPARTHelper.GetOWNERSERVERPARTList
    注意：C# 代码中有 AUTOTYPE_IDS 的特殊 IN 查询逻辑
    """
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter, search_model.QueryType or 0
        )

        # 特殊处理 AUTOTYPE_IDS（对应 C# searchModel.SearchParameter.AUTOTYPE_IDS.TryParseToString() != ""）
        sp = search_model.SearchParameter
        autotype_ids = sp.get("AUTOTYPE_IDS")
        if autotype_ids and str(autotype_ids).strip():
            extra = f"AUTOTYPE_ID IN ({autotype_ids})"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra

        if where_clause:
            where_sql = f" WHERE {where_clause}"

    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 关键字过滤
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

    for row in rows:
        _process_row(row)

    return int(total_count), rows


def get_ownerserverpart_detail(db: DatabaseHelper, ownerserverpart_id: int) -> Optional[dict]:
    """
    获取业主单位服务区关联关系表明细
    对应 C# OWNERSERVERPARTHelper.GetOWNERSERVERPARTDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {ownerserverpart_id}"
    rows = db.execute_query(sql)
    if rows:
        return _process_row(rows[0])
    return None


def synchro_ownerserverpart(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步业主单位服务区关联关系表（新增/更新）
    对应 C# OWNERSERVERPARTHelper.SynchroOWNERSERVERPART
    """
    for f in list(EXCLUDE_FIELDS):
        data.pop(f, None)

    ownerserverpart_id = data.get("OWNERSERVERPART_ID")

    if ownerserverpart_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {ownerserverpart_id}"
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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {ownerserverpart_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["OWNERSERVERPART_ID"] = new_id

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


def delete_ownerserverpart(db: DatabaseHelper, ownerserverpart_id: int) -> bool:
    """
    删除业主单位服务区关联关系表（真删除）
    对应 C# OWNERSERVERPARTHelper.DeleteOWNERSERVERPART
    原 C# 逻辑：
    1. 先查询记录获取 AUTOTYPE_ID 和 SERVERPART_HOSTID
    2. 先删关联门店：DELETE FROM T_OWNERSERVERPARTSHOP WHERE AUTOTYPE_ID=? AND SERVERPART_HOSTID=?
    3. 再删自身记录
    """
    # 先查记录（对应 C# _OWNERSERVERPART.Select()）
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {ownerserverpart_id}"
    rows = db.execute_query(sql)
    if not rows:
        return False

    row = rows[0]
    autotype_id = row.get("AUTOTYPE_ID")
    serverpart_hostid = row.get("SERVERPART_HOSTID")

    # 先删关联门店（对应 C# DELETE FROM T_OWNERSERVERPARTSHOP WHERE AUTOTYPE_ID=? AND SERVERPART_HOSTID=?）
    if autotype_id is not None and serverpart_hostid is not None:
        del_shop_sql = (
            f"DELETE FROM T_OWNERSERVERPARTSHOP "
            f"WHERE AUTOTYPE_ID = {autotype_id} AND SERVERPART_HOSTID = {serverpart_hostid}"
        )
        db.execute_non_query(del_shop_sql)

    # 再删自身记录（对应 C# _OWNERSERVERPART.Delete()）
    del_sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {ownerserverpart_id}"
    db.execute_non_query(del_sql)

    return True
