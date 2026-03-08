from __future__ import annotations
# -*- coding: utf-8 -*-
"""
自定义类别表业务服务
严格参照原 C# AUTOTYPEHelper.cs 中的实现逻辑
使用 MOBILESERVICE_PLATFORM.T_AUTOTYPE 表（达梦中为 T_AUTOTYPE）
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_AUTOTYPE"
PRIMARY_KEY = "AUTOTYPE_ID"

# 同步时排除的字段（原 C# excludeField: "ServerpartList"）
EXCLUDE_FIELDS = {"ServerpartList"}

# 字符串字段（原 C# BindDataRowToModel 中直接 .ToString() 赋值的字段）
STR_FIELDS = [
    "AUTOTYPE_NAME", "AUTOTYPE_STAFF", "AUTOTYPE_CODE",
    "AUTOTYPE_TYPENAME", "OWNERUNIT_NAME", "STAFF_NAME", "AUTOTYPE_DESC"
]


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    构建 WHERE 条件
    对应 C# OperationDataHelper<AUTOTYPEModel>.GetWhereSQL(searchModel.SearchParameter, searchModel.QueryType, "", "ServerpartList")
    排除 ServerpartList 字段
    """
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS:
            continue
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        # QueryType=0 时用 LIKE，其他用精确匹配（与 C# GetWhereSQL 逻辑一致）
        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
    return " AND ".join(conditions)


def _build_keyword_filter(keyword: dict) -> str:
    """
    构建关键字过滤条件
    对应 C# 中 searchModel.keyWord.Key.Split(',') 遍历生成 OR 条件
    """
    if not keyword or not keyword.get("Key") or not keyword.get("Value"):
        return ""
    keys = keyword["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{keyword['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


def _process_row(row: dict) -> dict:
    """
    处理单行数据，对应 C# BindDataRowToModel
    - 字符串字段 None → 空字符串（C# .ToString()）
    - int 字段保持 None 或转 int（C# TryParseToInt）
    - short 字段保持 None 或转 int（C# TryParseToShort）
    """
    for field in STR_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    return row


def get_autotype_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取自定义类别表列表
    对应 C# AUTOTYPEHelper.GetAUTOTYPEList(transaction, ref TotalCount, searchModel)
    """
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter, search_model.QueryType or 0
        )
        if where_clause:
            where_sql = f" WHERE {where_clause}"

    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 关键字过滤（对应 C# RowFilterSQL）
    if search_model.keyWord:
        keyword_filter = _build_keyword_filter(
            search_model.keyWord.model_dump() if hasattr(search_model.keyWord, 'model_dump') else search_model.keyWord
        )
        if keyword_filter:
            if where_sql:
                base_sql += f" AND ({keyword_filter})"
            else:
                base_sql += f" WHERE ({keyword_filter})"

    # 获取总记录数（对应 C# TotalCount = dtAUTOTYPE.Rows.Count）
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 排序（对应 C# dtAUTOTYPE.DefaultView.Sort = searchModel.SortStr）
    if search_model.SortStr:
        base_sql += f" ORDER BY {search_model.SortStr}"

    # 分页（对应 C# CommonHelper.GetDataTableWithPageSize）
    page_index = search_model.PageIndex
    page_size = search_model.PageSize

    if page_index <= 0 or page_size <= 0:
        # 默认返回前10条（与 C# 默认行为一致）
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


def get_autotype_detail(db: DatabaseHelper, autotype_id: int) -> Optional[dict]:
    """
    获取自定义类别表明细
    对应 C# AUTOTYPEHelper.GetAUTOTYPEDetail(transaction, AUTOTYPEId)
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {autotype_id}"
    rows = db.execute_query(sql)
    if rows:
        return _process_row(rows[0])
    return None


def synchro_autotype(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步自定义类别表（新增/更新）
    对应 C# AUTOTYPEHelper.SynchroAUTOTYPE(transaction, autotypeModel)

    返回 (success: bool, data: dict)
    - ID 不为空且记录存在 → 更新 → (True, data)
    - ID 不为空但记录不存在 → (False, None)
    - ID 为空 → 新增 → (True, data)
    """
    # 排除非数据库字段（对应 C# excludeField.Add("ServerpartList")）
    for f in list(EXCLUDE_FIELDS):
        data.pop(f, None)

    autotype_id = data.get("AUTOTYPE_ID")

    if autotype_id is not None:
        # ID 存在时，检查记录是否存在（对应 C# dtAUTOTYPE.Rows.Count > 0）
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {autotype_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, None

        # 更新（对应 C# OperationDataHelper.GetTableExcuteSQL mode=1）
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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {autotype_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增：获取新 ID（对应 C# SEQ_AUTOTYPE.NEXTVAL FROM DUAL）
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["AUTOTYPE_ID"] = new_id

        # INSERT（对应 C# OperationDataHelper.GetTableExcuteSQL mode=0）
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


def delete_autotype(db: DatabaseHelper, autotype_id: int) -> bool:
    """
    删除自定义类别表（软删除）
    对应 C# AUTOTYPEHelper.DeleteAUTOTYPE(transaction, AUTOTYPEId)
    原 C# 逻辑：UPDATE T_AUTOTYPE SET AUTOTYPE_VALID = 0 WHERE AUTOTYPE_ID = ?
    """
    sql = f"UPDATE {TABLE_NAME} SET AUTOTYPE_VALID = 0 WHERE {PRIMARY_KEY} = {autotype_id}"
    affected = db.execute_non_query(sql)
    return affected > 0 if affected else False


def get_nesting_autotype_list(db: DatabaseHelper, autotype_typeid: int,
                               autotype_pid: int = -1, ownerunit_id: str = "",
                               search_key: str = "") -> list:
    """
    获取自定义类别表嵌套列表
    对应 C# AUTOTYPEHelper.GetNestingAUTOTYPEList(transaction, AUTOTYPE_TYPEID, AUTOTYPE_PID, OWNERUNIT_ID, "1", SearchKey)
    注意：C# Controller 传入 AUTOTYPE_VALID="1"（只查有效的）
    """
    # 构建 WHERE 条件（对应 C# WhereSQL 拼接）
    where_sql = f"WHERE AUTOTYPE_TYPEID = {autotype_typeid}"
    if ownerunit_id and ownerunit_id.strip():
        where_sql += f" AND OWNERUNIT_ID IN ({ownerunit_id})"
    # 固定只查有效数据（对应 C# Controller 传入 AUTOTYPE_VALID="1"）
    where_sql += " AND AUTOTYPE_VALID IN (1)"

    # 查询全部数据（对应 C# Business.AUTOTYPE(transaction).FillDataTable(WhereSQL)）
    all_sql = f"SELECT * FROM {TABLE_NAME} {where_sql}"
    all_rows = db.execute_query(all_sql)

    if autotype_pid == -1:
        # 从根节点开始递归（对应 C# BindNestingList(nestingModelList, "-1", dtAUTOTYPE, SearchKey)）
        return _build_nesting_list(all_rows, -1, search_key)
    else:
        # 从指定父节点开始（对应 C# GetAUTOTYPEDetail + BindNestingList）
        detail = get_autotype_detail(db, autotype_pid)
        if detail and detail.get("AUTOTYPE_ID") is not None:
            node = dict(detail)
            node_id = node["AUTOTYPE_ID"]
            # 检查是否有子节点
            has_children = any(r.get("AUTOTYPE_PID") == node_id for r in all_rows)
            children = None
            if has_children:
                children = _build_nesting_list(all_rows, node_id, search_key)

            # 模糊过滤（对应 C# 过滤逻辑）
            if (children and len(children) > 0) or not search_key:
                return [{"node": node, "children": children}]
            elif search_key and (
                (node.get("AUTOTYPE_NAME") or "").find(search_key) >= 0 or
                (node.get("AUTOTYPE_CODE") or "").find(search_key) >= 0
            ):
                return [{"node": node, "children": children}]
        return []


def _build_nesting_list(all_rows: list, parent_id: int, search_key: str) -> list:
    """
    递归构建嵌套列表
    对应 C# AUTOTYPEHelper.BindNestingList
    排序：AUTOTYPE_INDEX, AUTOTYPE_PID, AUTOTYPE_ID（对应 C# dtAUTOTYPE.Select 排序）
    """
    result = []
    # 筛选子节点（对应 C# dtAUTOTYPE.Select("AUTOTYPE_PID = " + parent_id)）
    child_rows = [r for r in all_rows if r.get("AUTOTYPE_PID") == parent_id]
    # 排序（对应 C# "AUTOTYPE_INDEX,AUTOTYPE_PID,AUTOTYPE_ID"）
    child_rows.sort(key=lambda x: (
        x.get("AUTOTYPE_INDEX") or 0,
        x.get("AUTOTYPE_PID") or 0,
        x.get("AUTOTYPE_ID") or 0
    ))

    for row in child_rows:
        node = _process_row(dict(row))
        node_id = node.get("AUTOTYPE_ID")

        # 递归子节点（对应 C# if dtAUTOTYPE.Select("AUTOTYPE_PID = " + autotypeModel.AUTOTYPE_ID).Length > 0）
        has_children = any(r.get("AUTOTYPE_PID") == node_id for r in all_rows)
        children_list = []
        if has_children:
            children_list = _build_nesting_list(all_rows, node_id, search_key)

        # 模糊过滤（对应 C# 过滤逻辑）
        if len(children_list) > 0 or not search_key:
            result.append({"node": node, "children": children_list if children_list else None})
        elif search_key and (
            (node.get("AUTOTYPE_NAME") or "").find(search_key) >= 0 or
            (node.get("AUTOTYPE_CODE") or "").find(search_key) >= 0
        ):
            result.append({"node": node, "children": children_list if children_list else None})

    return result


def get_nesting_autotype_tree(db: DatabaseHelper, autotype_typeid: int,
                               autotype_pid: int = -1, ownerunit_id: str = "",
                               search_key: str = "") -> list:
    """
    获取自定义类别表嵌套树
    对应 C# AUTOTYPEHelper.GetNestingAUTOTYPETree(transaction, AUTOTYPE_TYPEID, AUTOTYPE_PID, OWNERUNIT_ID, "1", SearchKey)
    返回 CommonTypeModel（label/value/key/type）结构
    """
    # WHERE 条件（与 NestingList 完全一致）
    where_sql = f"WHERE AUTOTYPE_TYPEID = {autotype_typeid}"
    if ownerunit_id and ownerunit_id.strip():
        where_sql += f" AND OWNERUNIT_ID IN ({ownerunit_id})"
    where_sql += " AND AUTOTYPE_VALID IN (1)"

    all_sql = f"SELECT * FROM {TABLE_NAME} {where_sql}"
    all_rows = db.execute_query(all_sql)

    if autotype_pid == -1:
        # 从根节点递归（对应 C# BindNestingTree(nestingModelList, "-1", dtAUTOTYPE, SearchKey)）
        return _build_nesting_tree(all_rows, -1, search_key)
    else:
        # 从指定父节点开始（对应 C# GetAUTOTYPEDetail + BindNestingTree）
        detail = get_autotype_detail(db, autotype_pid)
        if detail and detail.get("AUTOTYPE_ID") is not None:
            # CommonTypeModel 结构（对应 C# new CommonTypeModel { label, value, type, key }）
            node = {
                "label": detail.get("AUTOTYPE_NAME", ""),
                "value": detail.get("AUTOTYPE_ID"),
                "type": 1,  # 标识为子级节点
                "key": f"1-{detail.get('AUTOTYPE_ID')}"
            }
            node_id = detail["AUTOTYPE_ID"]
            has_children = any(r.get("AUTOTYPE_PID") == node_id for r in all_rows)
            children = None
            if has_children:
                children = _build_nesting_tree(all_rows, node_id, search_key)

            if (children and len(children) > 0) or not search_key:
                return [{"node": node, "children": children}]
            elif search_key and (
                (detail.get("AUTOTYPE_NAME") or "").find(search_key) >= 0 or
                (detail.get("AUTOTYPE_CODE") or "").find(search_key) >= 0
            ):
                return [{"node": node, "children": children}]
        return []


def _build_nesting_tree(all_rows: list, parent_id: int, search_key: str) -> list:
    """
    递归构建嵌套树（CommonTypeModel 精简结构）
    对应 C# AUTOTYPEHelper.BindNestingTree
    """
    result = []
    child_rows = [r for r in all_rows if r.get("AUTOTYPE_PID") == parent_id]
    child_rows.sort(key=lambda x: (
        x.get("AUTOTYPE_INDEX") or 0,
        x.get("AUTOTYPE_PID") or 0,
        x.get("AUTOTYPE_ID") or 0
    ))

    for row in child_rows:
        node_id = row.get("AUTOTYPE_ID")
        name = row.get("AUTOTYPE_NAME", "")
        # CommonTypeModel 结构（对应 C# new CommonTypeModel { label, value, type=1, key="1-"+value }）
        node = {
            "label": name,
            "value": node_id,
            "type": 1,
            "key": f"1-{node_id}"
        }

        has_children = any(r.get("AUTOTYPE_PID") == node_id for r in all_rows)
        children_list = []
        if has_children:
            children_list = _build_nesting_tree(all_rows, node_id, search_key)

        if len(children_list) > 0 or not search_key:
            result.append({"node": node, "children": children_list if children_list else None})
        elif search_key and (
            name.find(search_key) >= 0 or
            (row.get("AUTOTYPE_CODE") or "").find(search_key) >= 0
        ):
            result.append({"node": node, "children": children_list if children_list else None})

    return result
