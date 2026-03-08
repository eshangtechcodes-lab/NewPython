from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区成本核算对照表业务服务
替代原 SERVERPARTCRTHelper.cs
使用 HIGHWAY_STORAGE.T_SERVERPARTCRT 表
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_SERVERPARTCRT"
PRIMARY_KEY = "SERVERPARTCRT_ID"

# 排除字段（非数据库字段）
EXCLUDE_FIELDS = {
    "SERVERPART_CODES", "SERVERPART_IDS", "SPREGIONTYPE_INDEX",
    "SERVERPART_INDEX", "SPREGIONTYPE_ID", "SPREGIONTYPE_NAME", "SERVERPART_NAME"
}


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """构建 WHERE 条件"""
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
    """处理单行数据：字符串字段 None→空字符串"""
    str_fields = [
        "ACCOUNTBODY_CODE", "ACCOUNTBODY_NAME", "DEPARTMENT_CODE",
        "COSTCENTER_CODE", "COSTCENTER_NAME", "SERVERPART_CODE",
        "RESPONSIBLEDEP_CODE", "STAFF_NAME"
    ]
    for field in str_fields:
        if field in row and row[field] is None:
            row[field] = ""
    return row


def get_serverpartcrt_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """获取服务区成本核算对照表列表"""
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter, search_model.QueryType or 0
        )
        sp = search_model.SearchParameter

        # SERVERPART_CODES 条件
        codes = sp.get("SERVERPART_CODES")
        if codes and str(codes).strip():
            code_list = "','".join(codes.split(","))
            extra = f"SERVERPART_CODE IN ('{code_list}')"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra

        # SERVERPART_IDS 条件
        ids = sp.get("SERVERPART_IDS")
        if ids and str(ids).strip():
            extra = f"SERVERPART_ID IN ({ids})"
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


def get_serverpartcrt_tree_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区成本核算对照表 树形列表
    一级：区域 → 二级：服务区成本核算对照
    """
    total_count, result_list = get_serverpartcrt_list(db, search_model)
    tree_list = []

    if not result_list:
        return total_count, tree_list

    # 获取服务区信息列表
    sp_ids = search_model.SearchParameter.get("SERVERPART_IDS") if search_model.SearchParameter else None
    sp_where = ""
    if sp_ids and str(sp_ids).strip():
        sp_where = f" WHERE SERVERPART_ID IN ({sp_ids})"

    sp_sql = f"SELECT * FROM T_SERVERPART{sp_where}"
    sp_rows = db.execute_query(sp_sql)

    if not sp_rows:
        return total_count, tree_list

    # 按区域排序
    sp_rows.sort(key=lambda x: (
        x.get("SPREGIONTYPE_INDEX") or 0,
        x.get("SPREGIONTYPE_ID") or 0,
        x.get("SERVERPART_INDEX") or 0,
        x.get("SERVERPART_ID") or 0
    ))

    # 构建一级区域节点
    seen_regions = {}
    for sp in sp_rows:
        region_id = sp.get("SPREGIONTYPE_ID")
        if region_id not in seen_regions:
            seen_regions[region_id] = {
                "sp_list": [],
                "info": sp
            }
        seen_regions[region_id]["sp_list"].append(sp)

    # 构建 CRT ID → CRT 记录的映射
    crt_by_spid = {}
    for crt in result_list:
        sp_id = crt.get("SERVERPART_ID")
        if sp_id:
            crt_by_spid[sp_id] = crt

    for region_id, region_data in seen_regions.items():
        info = region_data["info"]
        region_node = {
            "node": {
                "SPREGIONTYPE_INDEX": info.get("SPREGIONTYPE_INDEX"),
                "SPREGIONTYPE_NAME": info.get("SPREGIONTYPE_NAME"),
                "SPREGIONTYPE_ID": info.get("SPREGIONTYPE_ID"),
            },
            "children": []
        }

        for sp in region_data["sp_list"]:
            sp_id = sp.get("SERVERPART_ID")
            crt = crt_by_spid.get(sp_id)
            if crt:
                crt["SPREGIONTYPE_INDEX"] = info.get("SPREGIONTYPE_INDEX")
                crt["SPREGIONTYPE_NAME"] = info.get("SPREGIONTYPE_NAME")
                crt["SPREGIONTYPE_ID"] = info.get("SPREGIONTYPE_ID")
                crt["SERVERPART_NAME"] = sp.get("SERVERPART_NAME")
                region_node["children"].append({"node": crt})

        tree_list.append(region_node)

    return total_count, tree_list


def get_serverpartcrt_detail(db: DatabaseHelper, serverpartcrt_id: int = None,
                              serverpart_id: int = None) -> Optional[dict]:
    """获取服务区成本核算对照表明细（可按 CRT_ID 或 SERVERPART_ID 查询）"""
    if serverpartcrt_id is not None:
        where = f"WHERE SERVERPARTCRT_ID = {serverpartcrt_id}"
    elif serverpart_id is not None:
        where = f"WHERE SERVERPART_ID = {serverpart_id}"
    else:
        return None

    sql = f"SELECT * FROM {TABLE_NAME} {where}"
    rows = db.execute_query(sql)
    if rows:
        return _process_row(rows[0])
    return None


def synchro_serverpartcrt(db: DatabaseHelper, data: dict) -> bool:
    """同步服务区成本核算对照表（新增/更新）"""
    # 移除非数据库字段
    for f in list(EXCLUDE_FIELDS):
        data.pop(f, None)

    serverpartcrt_id = data.get("SERVERPARTCRT_ID")

    if serverpartcrt_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpartcrt_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False

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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {serverpartcrt_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["SERVERPARTCRT_ID"] = new_id

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

    # Synchro 成功后更新门店营业税率（原 C# 逻辑）
    sp_id = data.get("SERVERPART_ID")
    account_tax = data.get("ACCOUNTTAX")
    if sp_id is not None and account_tax is not None:
        try:
            tax_sql = f"UPDATE T_SERVERPARTSHOP SET BUSINESSAREA = {account_tax} WHERE SERVERPART_ID = {sp_id}"
            db.execute_non_query(tax_sql)
        except Exception as e:
            logger.warning(f"更新门店营业税率失败: {e}")

    return True


def delete_serverpartcrt(db: DatabaseHelper, serverpartcrt_id: int) -> bool:
    """删除服务区成本核算对照表（真删除）"""
    sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpartcrt_id}"
    affected = db.execute_non_query(sql)
    return affected > 0 if affected else False
