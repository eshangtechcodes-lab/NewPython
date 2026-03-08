from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区类别表业务服务
严格参照原 C# SERVERPARTTYPEHelper.cs 中的实现逻辑
使用 HIGHWAY_STORAGE.T_SERVERPARTTYPE 表（达梦中为 T_SERVERPARTTYPE）
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_SERVERPARTTYPE"
PRIMARY_KEY = "SERVERPARTTYPE_ID"

# 同步时排除的字段（原 C# excludeField.Add("RTServerpartList")）
EXCLUDE_FIELDS = {"RTServerpartList"}

# 字符串字段（Oracle 原始列名，同步后达梦已完整）
STR_FIELDS = [
    "TYPE_NAME", "TYPE_CODE", "TYPE_DESC",
    "STAFF_NAME", "MAP_ICON", "SETUPPOINT"
]


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """构建 WHERE 条件，排除 RTServerpartList"""
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
    """处理单行数据"""
    for field in STR_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    return row


def get_serverparttype_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区类别表列表
    对应 C# SERVERPARTTYPEHelper.GetSERVERPARTTYPEList
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

    for row in rows:
        _process_row(row)

    return int(total_count), rows


def get_serverparttype_detail(db: DatabaseHelper, serverparttype_id: int) -> Optional[dict]:
    """
    获取服务区类别表明细
    对应 C# SERVERPARTTYPEHelper.GetSERVERPARTTYPEDetail
    注意：原 C# 还会额外查询 RTServerpartList（SPSTATICTYPE 列表）
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverparttype_id}"
    rows = db.execute_query(sql)
    if rows:
        detail = _process_row(rows[0])
        # 对应 C# serverparttypeModel.RTServerpartList = SPSTATICTYPEHelper.GetSPSTATICTYPEList(...)
        rt_sql = f"SELECT * FROM T_SPSTATICTYPE WHERE SERVERPARTTYPE_ID = {serverparttype_id}"
        rt_rows = db.execute_query(rt_sql)
        detail["RTServerpartList"] = rt_rows if rt_rows else []
        return detail
    return None


def synchro_serverparttype(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步服务区类别表（新增/更新）
    对应 C# SERVERPARTTYPEHelper.SynchroSERVERPARTTYPE
    """
    for f in list(EXCLUDE_FIELDS):
        data.pop(f, None)

    serverparttype_id = data.get("SERVERPARTTYPE_ID")

    if serverparttype_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverparttype_id}"
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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {serverparttype_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["SERVERPARTTYPE_ID"] = new_id

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


def delete_serverparttype(db: DatabaseHelper, serverparttype_id: int) -> bool:
    """
    删除服务区类别表（软删除）
    对应 C# SERVERPARTTYPEHelper.DeleteSERVERPARTTYPE
    原 C# 逻辑：UPDATE T_SERVERPARTTYPE SET TYPE_STATE = 0 WHERE SERVERPARTTYPE_ID = ?
    """
    sql = f"UPDATE {TABLE_NAME} SET TYPE_STATE = 0 WHERE {PRIMARY_KEY} = {serverparttype_id}"
    affected = db.execute_non_query(sql)
    return affected > 0 if affected else False


def get_nesting_serverparttype_list(db: DatabaseHelper, province_code: str = "",
                                      serverpartstatictype_id: str = "1000,4000",
                                      type_pid: str = "-1",
                                      type_state: int = None,
                                      search_key: str = "") -> list:
    """
    获取服务区类别表嵌套列表
    对应 C# SERVERPARTTYPEHelper.GetNestingSERVERPARTTYPEList
    C# 控制器参数：
      PROVINCE_CODE(从Header)，STATIC_TYPE(默认"1000,4000")，
      TYPE_PID(默认"-1")，TYPE_STATE(可空int)，SearchKey(可空)
    """
    where_sql = ""
    if province_code and province_code.strip():
        where_sql += f" WHERE PROVINCE_CODE IN ({province_code})"
    if serverpartstatictype_id and serverpartstatictype_id.strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}SERVERPARTSTATICTYPE_ID IN ({serverpartstatictype_id})"
    if type_state is not None:
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}TYPE_STATE = {type_state}"

    all_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    all_rows = db.execute_query(all_sql)

    # C# 中 type_pid 默认 "-1"，表示从根节点开始
    pid = int(type_pid) if type_pid else -1
    return _build_nesting_list(all_rows, pid, search_key or "")


def _build_nesting_list(all_rows: list, parent_id: int, search_key: str) -> list:
    """
    递归构建嵌套列表
    对应 C# BindNestingList，排序 TYPE_INDEX, SERVERPARTTYPE_ID
    C# 使用 TYPE_PID 字段，达梦表中对应 PARENT_ID
    """
    result = []
    # 达梦中根节点 PARENT_ID 为 None，C# 中用 TYPE_PID=-1 表示根节点
    if parent_id == -1:
        child_rows = [r for r in all_rows if r.get("TYPE_PID") is None or r.get("TYPE_PID") == -1]
    else:
        child_rows = [r for r in all_rows if r.get("TYPE_PID") == parent_id]
    child_rows.sort(key=lambda x: (
        x.get("TYPE_INDEX") or 0,
        x.get("SERVERPARTTYPE_ID") or 0
    ))

    for row in child_rows:
        node = _process_row(dict(row))
        node_id = node.get("SERVERPARTTYPE_ID")

        has_children = any(r.get("TYPE_PID") == node_id for r in all_rows)
        children_list = []
        if has_children:
            children_list = _build_nesting_list(all_rows, node_id, search_key)

        if len(children_list) > 0 or not search_key:
            result.append({"node": node, "children": children_list if children_list else None})
        elif search_key and (
            (node.get("TYPE_NAME") or "").find(search_key) >= 0
        ):
            result.append({"node": node, "children": children_list if children_list else None})

    return result


def get_nesting_serverparttype_tree(db: DatabaseHelper, province_code: str = "",
                                      serverpartstatictype_id: str = "1000,4000",
                                      type_pid: str = "-1",
                                      type_state: int = None,
                                      search_key: str = "") -> list:
    """
    获取服务区类别表嵌套树（CommonTypeModel 结构）
    对应 C# SERVERPARTTYPEHelper.GetNestingSERVERPARTTYPETree
    """
    where_sql = ""
    if province_code and province_code.strip():
        where_sql += f" WHERE PROVINCE_CODE IN ({province_code})"
    if serverpartstatictype_id and serverpartstatictype_id.strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}SERVERPARTSTATICTYPE_ID IN ({serverpartstatictype_id})"
    if type_state is not None:
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}TYPE_STATE = {type_state}"

    all_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    all_rows = db.execute_query(all_sql)

    pid = int(type_pid) if type_pid else -1
    return _build_nesting_tree(all_rows, pid, search_key or "")


def _build_nesting_tree(all_rows: list, parent_id: int, search_key: str) -> list:
    """
    递归构建嵌套树（CommonTypeModel + ico 字段）
    对应 C# BindNestingTree，字段名使用达梦实际列名
    """
    result = []
    # 达梦中根节点 PARENT_ID 为 None，C# 中用 TYPE_PID=-1 表示根节点
    if parent_id == -1:
        child_rows = [r for r in all_rows if r.get("TYPE_PID") is None or r.get("TYPE_PID") == -1]
    else:
        child_rows = [r for r in all_rows if r.get("TYPE_PID") == parent_id]
    child_rows.sort(key=lambda x: (
        x.get("TYPE_INDEX") or 0,
        x.get("SERVERPARTTYPE_ID") or 0
    ))

    for row in child_rows:
        node_id = row.get("SERVERPARTTYPE_ID")
        name = row.get("TYPE_NAME", "")
        # 达梦表无 MAP_ICON 列，C# 中 CommonTypeModel.ico = serverparttypeModel.MAP_ICON
        ico = row.get("MAP_ICON", "")

        # CommonTypeModel 结构（对应 C# new CommonTypeModel { label, value, type=1, key, ico }）
        node = {
            "label": name,
            "value": node_id,
            "type": 1,
            "key": f"1-{node_id}",
            "ico": ico if ico else None
        }

        has_children = any(r.get("TYPE_PID") == node_id for r in all_rows)
        children_list = []
        if has_children:
            children_list = _build_nesting_tree(all_rows, node_id, search_key)

        if len(children_list) > 0 or not search_key:
            result.append({"node": node, "children": children_list if children_list else None})
        elif search_key and name.find(search_key) >= 0:
            result.append({"node": node, "children": children_list if children_list else None})

    return result


def modify_rt_serverpart_type(db: DatabaseHelper, serverpart_ids: str,
                                serverparttype_id: int, serverpart_type: int = 0) -> bool:
    """
    修改服务区类别关联
    对应 C# SERVERPARTTYPEHelper.ModifyRTServerpartType(transaction, ServerpartIds, ServerparttypeId, ServerpartType)

    原 C# 逻辑：
    1. 删除旧的关联：DELETE FROM T_SPSTATICTYPE WHERE SERVERPARTTYPE_ID = ?
    2. 遍历 ServerpartIds，为每个服务区新增关联记录到 T_SPSTATICTYPE
    3. 如果 ServerpartType > 0，更新 T_SERVERPART.SERVERPART_TYPE
    """
    # 步骤1：删除旧关联（对应 C# DELETE FROM HIGHWAY_STORAGE.T_SPSTATICTYPE WHERE SERVERPARTTYPE_ID = ?）
    del_sql = f"DELETE FROM T_SPSTATICTYPE WHERE SERVERPARTTYPE_ID = {serverparttype_id}"
    db.execute_non_query(del_sql)

    # 步骤2：遍历新增关联（对应 C# foreach ServerpartId in ServerpartIds.Split(',')）
    if serverpart_ids and serverpart_ids.strip():
        for sp_id in serverpart_ids.split(","):
            sp_id = sp_id.strip()
            if not sp_id:
                continue
            # 获取新 ID
            max_id = db.execute_scalar("SELECT MAX(SPSTATICTYPE_ID) FROM T_SPSTATICTYPE")
            new_id = (max_id or 0) + 1

            insert_sql = (
                f"INSERT INTO T_SPSTATICTYPE (SPSTATICTYPE_ID, SERVERPART_ID, SERVERPARTTYPE_ID) "
                f"VALUES ({new_id}, {sp_id}, {serverparttype_id})"
            )
            db.execute_non_query(insert_sql)

            # 步骤3：如果 ServerpartType > 0，更新 T_SERVERPART.SERVERPART_TYPE
            # 对应 C# if (ServerpartType > 0) UPDATE T_SERVERPART SET SERVERPART_TYPE = ? WHERE SERVERPART_ID = ?
            if serverpart_type > 0:
                update_sql = f"UPDATE T_SERVERPART SET SERVERPART_TYPE = {serverpart_type} WHERE SERVERPART_ID = {sp_id}"
                db.execute_non_query(update_sql)

    return True
