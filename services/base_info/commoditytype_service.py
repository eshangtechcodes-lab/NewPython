from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商品类别业务服务
替代原 COMMODITYTYPEHelper.cs
使用 T_COMMODITYTYPE 表（标准CRUD）和 V_COMMODITYTYPE 视图（嵌套列表/树）
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名和视图常量
TABLE_NAME = "T_COMMODITYTYPE"
VIEW_NAME = "V_COMMODITYTYPE"
PRIMARY_KEY = "COMMODITYTYPE_ID"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """构建 WHERE 条件，排除非数据库字段"""
    conditions = []
    exclude_fields = {"OPERATE_DATE_Start", "OPERATE_DATE_End"}
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
    处理单行数据
    - 字符串字段 None → 空字符串
    - 原 C# 有 TryParseToInt/TryParseToDecimal 转换 VARCHAR 字段为数值
    - 添加查询参数字段（原 C# Model 中包含这些字段返回 null）
    """
    str_fields = ["COMMODITYTYPE_NAME", "COMMODITYTYPE_EN", "COMMODITYTYPE_DESC", "STAFF_NAME"]
    for field in str_fields:
        if field in row and row[field] is None:
            row[field] = ""

    # VARCHAR 字段转数值（原 C# TryParseToInt / TryParseToDecimal）
    # COMMODITYTYPE_VALID -> TryParseToShort, COMMODITYTYPE_PID -> TryParseToInt
    # COMMODITYTYPE_INDEX -> TryParseToInt, COMMODITYTYPE_CODE -> TryParseToDecimal
    int_parse_fields = ["COMMODITYTYPE_VALID", "COMMODITYTYPE_PID"]
    for field in int_parse_fields:
        if field in row and row[field] is not None:
            try:
                row[field] = int(float(str(row[field])))
            except (ValueError, TypeError):
                pass

    # COMMODITYTYPE_INDEX -> C# Model 中是 decimal 类型，序列化为 float
    if "COMMODITYTYPE_INDEX" in row and row["COMMODITYTYPE_INDEX"] is not None:
        try:
            row["COMMODITYTYPE_INDEX"] = float(str(row["COMMODITYTYPE_INDEX"]))
        except (ValueError, TypeError):
            pass

    # COMMODITYTYPE_CODE -> TryParseToDecimal（返回浮点数）
    if "COMMODITYTYPE_CODE" in row and row["COMMODITYTYPE_CODE"] is not None:
        try:
            row["COMMODITYTYPE_CODE"] = float(str(row["COMMODITYTYPE_CODE"]))
        except (ValueError, TypeError):
            pass

    # 添加查询参数字段（原 C# Model 中包含这些字段返回 null）
    row.setdefault("OPERATE_DATE_Start", None)
    row.setdefault("OPERATE_DATE_End", None)

    return row


def get_commoditytype_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取商品类别列表
    对应原 COMMODITYTYPEHelper.GetCOMMODITYTYPEList
    """
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter, search_model.QueryType or 0
        )
        # 处理操作时间范围查询
        start_date = search_model.SearchParameter.get("OPERATE_DATE_Start")
        end_date = search_model.SearchParameter.get("OPERATE_DATE_End")
        if start_date:
            date_val = start_date.split(' ')[0] if ' ' in str(start_date) else start_date
            extra = f"OPERATE_DATE >= TO_DATE('{date_val}','YYYY/MM/DD')"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra
        if end_date:
            date_val = end_date.split(' ')[0] if ' ' in str(end_date) else end_date
            extra = f"OPERATE_DATE < TO_DATE('{date_val}','YYYY/MM/DD') + 1"
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


def get_commoditytype_detail(db: DatabaseHelper, commoditytype_id: int) -> Optional[dict]:
    """获取商品类别明细"""
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {commoditytype_id}"
    rows = db.execute_query(sql)
    if rows:
        row = rows[0]
        # 保存原始 null 值（C# Detail 中不对这些字段做 ToString() 转换）
        null_fields = {k: row.get(k) for k in ["COMMODITYTYPE_EN", "STAFF_NAME"]}
        _process_row(row)
        # 恢复 C# Detail 中保持 null 的字段
        for k, v in null_fields.items():
            if v is None:
                row[k] = None
        return row
    return None


def synchro_commoditytype(db: DatabaseHelper, data: dict) -> bool:
    """
    同步商品类别（新增/更新）
    注意：原 C# 有下发收银机逻辑，Python 暂跳过
    """
    # 默认香烟类型
    if data.get("CIGARETTE_TYPE") is None:
        data["CIGARETTE_TYPE"] = 1
    # 默认添加时间
    if data.get("ADDTIME") is None:
        data["ADDTIME"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 移除查询条件字段
    data.pop("OPERATE_DATE_Start", None)
    data.pop("OPERATE_DATE_End", None)

    commoditytype_id = data.get("COMMODITYTYPE_ID")

    if commoditytype_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {commoditytype_id}"
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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {commoditytype_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["COMMODITYTYPE_ID"] = new_id

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


def delete_commoditytype(db: DatabaseHelper, commoditytype_id: int) -> bool:
    """删除商品类别（软删除，COMMODITYTYPE_VALID=0）"""
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {commoditytype_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    sql = f"UPDATE {TABLE_NAME} SET COMMODITYTYPE_VALID = 0 WHERE {PRIMARY_KEY} = {commoditytype_id}"
    db.execute_non_query(sql)
    return True


def get_nesting_commoditytype_list(db: DatabaseHelper, commoditytype_pid: str = "-1",
                                    province_code: str = None, commoditytype_valid: str = None,
                                    search_key: str = None) -> list:
    """
    获取商品类别嵌套列表
    使用 V_COMMODITYTYPE 视图
    """
    where_sql = ""
    if province_code:
        where_sql += f" WHERE PROVINCE_CODE IN ({province_code})"
    if commoditytype_valid:
        valid_values = "','".join(commoditytype_valid.split(","))
        if where_sql:
            where_sql += f" AND COMMODITYTYPE_VALID IN ('{valid_values}')"
        else:
            where_sql += f" WHERE COMMODITYTYPE_VALID IN ('{valid_values}')"

    # 尝试使用视图，如果视图不存在则用基表
    try:
        all_sql = f"SELECT * FROM {VIEW_NAME}{where_sql}"
        all_rows = db.execute_query(all_sql)
    except Exception:
        all_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
        all_rows = db.execute_query(all_sql)

    if commoditytype_pid == "-1":
        return _build_nesting_list(all_rows, "-1", search_key)
    else:
        # 从指定父节点开始
        detail = get_commoditytype_detail(db, int(commoditytype_pid))
        if detail and detail.get("COMMODITYTYPE_ID"):
            node = _process_row(dict(detail))
            children = _build_nesting_list(all_rows, str(detail["COMMODITYTYPE_ID"]), search_key)
            if children or not search_key:
                return [{"node": node, "children": children}]
        return []


def _build_nesting_list(all_rows: list, parent_id: str, search_key: str) -> list:
    """递归构建嵌套列表"""
    result = []
    pid = int(parent_id) if parent_id != "-1" else -1
    child_rows = [r for r in all_rows if r.get("COMMODITYTYPE_PID") == pid]
    child_rows.sort(key=lambda x: (
        x.get("COMMODITYTYPE_INDEX") or 0,
        x.get("COMMODITYTYPE_CODE") or 0,
        x.get("PROVINCE_CODE") or 0
    ))

    for row in child_rows:
        node = _process_row(dict(row))
        node_id = node.get("COMMODITYTYPE_ID")

        # 检查是否有子节点
        has_children = any(r.get("COMMODITYTYPE_PID") == node_id for r in all_rows)
        children = None
        if has_children:
            children = _build_nesting_list(all_rows, str(node_id), search_key)

        # 模糊过滤
        if (children and len(children) > 0) or not search_key:
            result.append({"node": node, "children": children})

    return result


def get_nesting_commoditytype_tree(db: DatabaseHelper, commoditytype_pid: str = "-1",
                                    province_code: str = None, commoditytype_valid: str = None,
                                    search_key: str = None, show_code: bool = False) -> list:
    """
    获取商品类别嵌套树（CommonTypeModel 精简结构）
    使用 V_COMMODITYTYPE 视图
    """
    where_sql = ""
    if province_code:
        where_sql += f" WHERE PROVINCE_CODE IN ({province_code})"
    if commoditytype_valid:
        valid_values = "','".join(commoditytype_valid.split(","))
        if where_sql:
            where_sql += f" AND COMMODITYTYPE_VALID IN ('{valid_values}')"
        else:
            where_sql += f" WHERE COMMODITYTYPE_VALID IN ('{valid_values}')"

    try:
        all_sql = f"SELECT * FROM {VIEW_NAME}{where_sql}"
        all_rows = db.execute_query(all_sql)
    except Exception:
        all_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
        all_rows = db.execute_query(all_sql)

    if commoditytype_pid == "-1":
        return _build_nesting_tree(all_rows, "-1", search_key, show_code)
    else:
        detail = get_commoditytype_detail(db, int(commoditytype_pid))
        if detail and detail.get("COMMODITYTYPE_ID"):
            label = detail.get("COMMODITYTYPE_NAME", "")
            if show_code:
                label = f"[{detail.get('COMMODITYTYPE_CODE', '')}]{label}"
            node = {
                "label": label,
                "value": detail.get("COMMODITYTYPE_ID"),
                "type": 1,
                "key": f"1-{detail.get('COMMODITYTYPE_ID')}"
            }
            children = _build_nesting_tree(all_rows, str(detail["COMMODITYTYPE_ID"]), search_key, show_code)
            if children or not search_key:
                return [{"node": node, "children": children}]
        return []


def _build_nesting_tree(all_rows: list, parent_id: str, search_key: str, show_code: bool) -> list:
    """递归构建嵌套树（CommonTypeModel）"""
    result = []
    pid = int(parent_id) if parent_id != "-1" else -1
    child_rows = [r for r in all_rows if r.get("COMMODITYTYPE_PID") == pid]
    child_rows.sort(key=lambda x: (
        x.get("COMMODITYTYPE_INDEX") or 0,
        x.get("COMMODITYTYPE_CODE") or 0,
        x.get("PROVINCE_CODE") or 0
    ))

    for row in child_rows:
        name = row.get("COMMODITYTYPE_NAME", "")
        node_id = row.get("COMMODITYTYPE_ID")
        label = name
        if show_code:
            label = f"[{row.get('COMMODITYTYPE_CODE', '')}]{name}"

        node = {
            "label": label,
            "value": node_id,
            "type": 1,
            "key": f"1-{node_id}"
        }

        has_children = any(r.get("COMMODITYTYPE_PID") == node_id for r in all_rows)
        children = None
        if has_children:
            children = _build_nesting_tree(all_rows, str(node_id), search_key, show_code)

        if (children and len(children) > 0) or not search_key:
            result.append({"node": node, "children": children})

    return result
