from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营业态业务服务
替代原 AUTOSTATISTICSHelper.cs 中 BusinessTrade 相关方法
BusinessTrade 是 T_AUTOSTATISTICS 表中 AUTOSTATISTICS_TYPE=2000 的过滤视图
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_AUTOSTATISTICS"
PRIMARY_KEY = "AUTOSTATISTICS_ID"
# 经营业态固定类型
BUSINESS_TRADE_TYPE = 2000


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    排除非数据库字段：INELASTIC_DEMAND
    """
    conditions = []
    # 排除非数据库字段
    exclude_fields = {"INELASTIC_DEMAND"}

    for key, value in search_param.items():
        if key in exclude_fields:

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
    """
    处理单行数据，对应原 C# BindDataRowToModel 逻辑
    - 字符串字段：None -> 空字符串（与原 C# ToString() 一致）
    - AUTOSTATISTICS_TYPE=2000 时，INELASTIC_DEMAND = STATISTICS_TYPE
    """
    # 字符串字段列表（原 C# 中 ToString() 对 null 返回空字符串）
    str_fields = ["AUTOSTATISTICS_NAME", "AUTOSTATISTICS_VALUE", "AUTOSTATISTICS_ICO",
                  "OWNERUNIT_NAME", "STAF_NAME", "AUTOSTATISTICS_DESC"]
    for field in str_fields:
        if field in row and row[field] is None:
            row[field] = ""

    # 整数字段列表（原 C# TryParseToInt 对空值返回 0）
    int_fields = ["AUTOSTATISTICS_ID", "AUTOSTATISTICS_PID", "AUTOSTATISTICS_INDEX",
                  "AUTOSTATISTICS_TYPE", "STATISTICS_TYPE", "OWNERUNIT_ID",
                  "PROVINCE_CODE", "AUTOSTATISTICS_STATE", "STAFF_ID"]
    for field in int_fields:
        if field in row and row[field] is None:
            row[field] = 0

    # INELASTIC_DEMAND 处理
    if row.get("AUTOSTATISTICS_TYPE") == BUSINESS_TRADE_TYPE:
        row["INELASTIC_DEMAND"] = row.get("STATISTICS_TYPE", 0)
    else:
        row["INELASTIC_DEMAND"] = None
    return row


def get_businesstrade_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取经营业态列表
    对应原 AUTOSTATISTICSHelper.GetAUTOSTATISTICSList
    强制过滤 AUTOSTATISTICS_TYPE=2000
    返回: (总数, 数据列表)
    """
    # 强制设定经营业态类型
    if search_model.SearchParameter is None:
        search_model.SearchParameter = {}
    search_model.SearchParameter["AUTOSTATISTICS_TYPE"] = BUSINESS_TRADE_TYPE

    # 构建 WHERE 条件
    where_sql = ""
    where_clause = _build_where_sql(
        search_model.SearchParameter,
        search_model.QueryType or 0
    )

    # 处理 AUTOSTATISTICS_ID 子类型递归查询
    autostatistics_id = search_model.SearchParameter.get("AUTOSTATISTICS_ID")
    if autostatistics_id and autostatistics_id != 0:
        # 获取所有子类型 ID
        sub_ids = _get_sub_type_ids(db, autostatistics_id)
        if sub_ids:
            # 从通用条件中排除 AUTOSTATISTICS_ID 的等值条件
            parts = [c for c in where_clause.split(" AND ") if "AUTOSTATISTICS_ID" not in c]
            extra = f"AUTOSTATISTICS_ID IN ({sub_ids})"
            parts.append(extra)
            where_clause = " AND ".join(parts)

    # 处理 INELASTIC_DEMAND -> STATISTICS_TYPE 映射
    inelastic = search_model.SearchParameter.get("INELASTIC_DEMAND")
    if inelastic is not None:
        extra = f"STATISTICS_TYPE = {inelastic}"
        if where_clause:
            where_clause += f" AND {extra}"
        else:
            where_clause = extra

    if where_clause:
        where_sql = f" WHERE {where_clause}"

    # 构建基础查询 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 添加关键字过滤
    if search_model.keyWord:
        keyword_filter = _build_keyword_filter(
            search_model.keyWord.model_dump() if hasattr(search_model.keyWord, 'model_dump') else search_model.keyWord
        )
        if keyword_filter:
            if where_sql:
                base_sql += f" AND ({keyword_filter})"
            else:
                base_sql += f" WHERE ({keyword_filter})"

    # 查询总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 添加排序
    if search_model.SortStr:
        base_sql += f" ORDER BY {search_model.SortStr}"

    # 分页处理（原 C# 默认 PageIndex=0, PageSize=0 时返回前 10 条）
    page_index = search_model.PageIndex
    page_size = search_model.PageSize

    if page_index <= 0 or page_size <= 0:
        # 默认返回前10条，与原 C# CommonHelper.GetDataTableWithPageSize 一致
        limit_sql = f"""
            SELECT * FROM ({base_sql}) WHERE ROWNUM <= 10
        """
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

    # 处理每行数据
    for row in rows:
        _process_row(row)

    return int(total_count), rows


def _get_sub_type_ids(db: DatabaseHelper, parent_id: int) -> str:
    """
    递归获取所有子类型 ID（含自身）
    对应原 C# Business.AUTOSTATISTICS.GetSubType
    """
    all_ids = [str(parent_id)]
    sql = f"SELECT {PRIMARY_KEY} FROM {TABLE_NAME} WHERE AUTOSTATISTICS_PID = {parent_id} AND AUTOSTATISTICS_TYPE = {BUSINESS_TRADE_TYPE}"
    rows = db.execute_query(sql)
    for row in rows:
        child_id = row.get(PRIMARY_KEY)
        if child_id:
            sub = _get_sub_type_ids(db, child_id)
            all_ids.extend(sub.split(","))
    return ",".join(all_ids)


def get_businesstrade_tree(db: DatabaseHelper, business_trade_pid: int = -1,
                           province_code: int = None, owner_unit_id: int = None,
                           business_trade_state: int = None) -> tuple:
    """
    查询经营业态树
    对应原 AUTOSTATISTICSHelper.GetNestingBusinessTradeTree
    返回: (总数, 嵌套树列表)
    """
    # 构建 WHERE 条件
    where_sql = "WHERE AUTOSTATISTICS_TYPE = 2000"
    brand_where = ""
    if province_code is not None:
        where_sql += f" AND PROVINCE_CODE = {province_code}"
        brand_where += f" AND PROVINCE_CODE = {province_code}"
    if owner_unit_id is not None:
        where_sql += f" AND OWNERUNIT_ID = {owner_unit_id}"
        brand_where += f" AND OWNERUNIT_ID = {owner_unit_id}"
    if business_trade_state is not None:
        where_sql += f" AND AUTOSTATISTICS_STATE = {business_trade_state}"

    # 查询所有经营业态数据
    all_sql = f"SELECT * FROM {TABLE_NAME} {where_sql}"
    all_rows = db.execute_query(all_sql)

    # 查询品牌数量（用于 STATISTICS_TYPE 字段）
    brand_sql = f"""SELECT BRAND_ID, BRAND_INDUSTRY FROM T_BRAND
        WHERE BRAND_CATEGORY = 1000 AND BRAND_STATE = 1{brand_where}"""
    try:
        brand_rows = db.execute_query(brand_sql)
    except Exception:
        brand_rows = []

    # 统计每个业态的品牌数量
    brand_count_map = {}
    for br in brand_rows:
        industry = br.get("BRAND_INDUSTRY")
        if industry is not None:
            brand_count_map[industry] = brand_count_map.get(industry, 0) + 1

    # 获取父级节点
    parent_rows = [r for r in all_rows if r.get("AUTOSTATISTICS_PID") == business_trade_pid]
    # 按 AUTOSTATISTICS_INDEX, AUTOSTATISTICS_ID 排序
    parent_rows.sort(key=lambda x: (x.get("AUTOSTATISTICS_INDEX") or 0, x.get("AUTOSTATISTICS_ID") or 0))

    total_count = len(parent_rows)
    result = []

    for row in parent_rows:
        node = _process_row(dict(row))
        node_id = node.get("AUTOSTATISTICS_ID")
        # 品牌数量赋值到 STATISTICS_TYPE
        node["STATISTICS_TYPE"] = brand_count_map.get(node_id, 0)

        children = _build_tree_children(all_rows, node_id, brand_count_map)

        # 子级品牌数量累加到父级
        for child in children:
            node["STATISTICS_TYPE"] = (node["STATISTICS_TYPE"] or 0) + (child["node"].get("STATISTICS_TYPE") or 0)

        result.append({
            "node": node,
            "children": children
        })

    return total_count, result


def _build_tree_children(all_rows: list, parent_id: int, brand_count_map: dict) -> list:
    """递归构建子级树"""
    children = []
    child_rows = [r for r in all_rows if r.get("AUTOSTATISTICS_PID") == parent_id]
    child_rows.sort(key=lambda x: (x.get("AUTOSTATISTICS_INDEX") or 0, x.get("AUTOSTATISTICS_ID") or 0))

    for row in child_rows:
        node = _process_row(dict(row))
        node_id = node.get("AUTOSTATISTICS_ID")
        node["STATISTICS_TYPE"] = brand_count_map.get(node_id, 0)

        sub_children = _build_tree_children(all_rows, node_id, brand_count_map)

        # 子级品牌数量累加
        for sub in sub_children:
            node["STATISTICS_TYPE"] = (node["STATISTICS_TYPE"] or 0) + (sub["node"].get("STATISTICS_TYPE") or 0)

        children.append({
            "node": node,
            "children": sub_children
        })

    return children


def get_businesstrade_enum(db: DatabaseHelper, business_trade_pid: int = -1,
                           province_code: int = None, owner_unit_id: int = None,
                           business_trade_state: int = None, search_key: str = "") -> list:
    """
    查询经营业态枚举树
    对应原 AUTOSTATISTICSHelper.GetBusinessTradeEnum
    返回 CommonTypeModel 精简树结构: {node: {label, value, key, type, ico}, children: [...]}
    """
    # 构建 WHERE 条件
    where_sql = "WHERE AUTOSTATISTICS_TYPE = 2000"
    if province_code is not None:
        where_sql += f" AND PROVINCE_CODE = {province_code}"
    if owner_unit_id is not None:
        where_sql += f" AND OWNERUNIT_ID = {owner_unit_id}"
    if business_trade_state is not None:
        where_sql += f" AND AUTOSTATISTICS_STATE = {business_trade_state}"

    # 查询所有经营业态数据
    all_sql = f"SELECT * FROM {TABLE_NAME} {where_sql}"
    all_rows = db.execute_query(all_sql)

    if business_trade_pid == -1:
        # 从根节点开始构建
        return _build_enum_tree(all_rows, "-1", search_key)
    else:
        # 从指定父节点开始
        detail = get_businesstrade_detail(db, business_trade_pid)
        if detail and detail.get("AUTOSTATISTICS_ID"):
            node = {
                "label": detail.get("AUTOSTATISTICS_NAME", ""),
                "value": detail.get("AUTOSTATISTICS_ID"),
                "type": 1,
                "key": f"1-{detail.get('AUTOSTATISTICS_ID')}",
                "ico": detail.get("AUTOSTATISTICS_ICO", "")
            }
            children = _build_enum_tree(all_rows, str(detail["AUTOSTATISTICS_ID"]), search_key)
            # 模糊过滤
            if children or not search_key:
                return [{"node": node, "children": children}]
        return []


def _build_enum_tree(all_rows: list, parent_id: str, search_key: str) -> list:
    """递归构建枚举树"""
    result = []
    pid = int(parent_id) if parent_id != "-1" else -1
    child_rows = [r for r in all_rows if r.get("AUTOSTATISTICS_PID") == pid]
    child_rows.sort(key=lambda x: (x.get("AUTOSTATISTICS_INDEX") or 0, x.get("AUTOSTATISTICS_ID") or 0))

    for row in child_rows:
        node_id = row.get("AUTOSTATISTICS_ID")
        label = row.get("AUTOSTATISTICS_NAME", "")
        ico = row.get("AUTOSTATISTICS_ICO", "")

        node = {
            "label": label,
            "value": node_id,
            "type": 1,
            "key": f"1-{node_id}",
            "ico": ico if ico else None
        }

        # 递归获取子节点
        children = _build_enum_tree(all_rows, str(node_id), search_key)

        # 模糊过滤
        if children or not search_key or (search_key and search_key in label):
            result.append({
                "node": node,
                "children": children if children else None
            })

    return result


def get_businesstrade_detail(db: DatabaseHelper, businesstrade_id: int) -> Optional[dict]:
    """
    获取经营业态明细
    对应原 AUTOSTATISTICSHelper.GetAUTOSTATISTICSDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {businesstrade_id}"
    rows = db.execute_query(sql)
    if rows:
        return _process_row(rows[0])
    return None


def synchro_businesstrade(db: DatabaseHelper, data: dict) -> bool:
    """
    同步经营业态（新增/更新）
    对应原 AUTOSTATISTICSHelper.SynchroAUTOSTATISTICS
    强制设定 AUTOSTATISTICS_TYPE=2000
    """
    data["AUTOSTATISTICS_TYPE"] = BUSINESS_TRADE_TYPE

    # 处理 INELASTIC_DEMAND -> STATISTICS_TYPE 映射
    if data.get("AUTOSTATISTICS_TYPE") == BUSINESS_TRADE_TYPE and data.get("INELASTIC_DEMAND") is not None:
        data["STATISTICS_TYPE"] = data.pop("INELASTIC_DEMAND")
    elif "INELASTIC_DEMAND" in data:
        data.pop("INELASTIC_DEMAND")

    # 默认有效状态
    if data.get("AUTOSTATISTICS_STATE") is None:
        data["AUTOSTATISTICS_STATE"] = 1

    # 默认操作时间
    if data.get("OPERATE_DATE") is None:
        data["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    autostatistics_id = data.get("AUTOSTATISTICS_ID")

    if autostatistics_id is not None:
        # 更新
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {autostatistics_id}"
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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {autostatistics_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增：使用 MAX(ID)+1
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["AUTOSTATISTICS_ID"] = new_id

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

    return True


def delete_businesstrade(db: DatabaseHelper, businesstrade_id: int) -> bool:
    """
    删除经营业态（软删除，设 AUTOSTATISTICS_STATE=0）
    对应原 AUTOSTATISTICSHelper.DeleteAUTOSTATISTICS
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {businesstrade_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    sql = f"UPDATE {TABLE_NAME} SET AUTOSTATISTICS_STATE = 0 WHERE {PRIMARY_KEY} = {businesstrade_id}"
    db.execute_non_query(sql)
    return True
