# -*- coding: utf-8 -*-
"""
品牌表业务服务
替代原 BRANDHelper.cs，保持相同的业务逻辑
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.auto_build.brand import BRANDModel
from models.common_model import SearchModel


# 表名常量（达梦中使用当前用户 NEWPYTHON 下的表，无需 schema 前缀）
TABLE_NAME = "T_BRAND"
PRIMARY_KEY = "BRAND_ID"
SEQUENCE_NAME = "SEQ_BRAND"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    query_type: 0=模糊查询, 1=精确查询
    """
    conditions = []
    for key, value in search_param.items():
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        if query_type == 0 and isinstance(value, str):
            # 模糊查询
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            # 精确查询
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


def get_brand_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取品牌表列表
    对应原 BRANDHelper.GetBRANDList
    返回: (总数, 数据列表)
    """
    # 构建 WHERE 条件
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter,
            search_model.QueryType or 0
        )
        if where_clause:
            where_sql = f" WHERE {where_clause}"

    # 构建基础查询 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 添加关键字过滤
    keyword_filter = ""
    if search_model.keyWord:
        keyword_filter = _build_keyword_filter(search_model.keyWord.model_dump())
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

    # 分页处理：PageIndex=0 或 PageSize=0 时默认返回前10条（与原 C# API 一致）
    page_index = search_model.PageIndex
    page_size = search_model.PageSize

    if page_index <= 0 or page_size <= 0:
        # 不分页参数时，默认返回前10条（原 C# API 行为）
        default_limit = 10
        limit_sql = f"SELECT * FROM ({base_sql}) WHERE ROWNUM <= {default_limit}"
        rows = db.execute_query(limit_sql)
    else:
        # 分页查询（使用 ROWNUM 分页，达梦兼容 Oracle 分页语法）
        start_row = (page_index - 1) * page_size + 1
        end_row = page_index * page_size
        paged_sql = f"""
            SELECT * FROM (
                SELECT A.*, ROWNUM RN FROM ({base_sql}) A
                WHERE ROWNUM <= {end_row}
            ) WHERE RN >= {start_row}
        """
        rows = db.execute_query(paged_sql)
        # 移除分页辅助列 RN
        for row in rows:
            row.pop("RN", None)

    return int(total_count), rows


def get_brand_detail(db: DatabaseHelper, brand_id: int) -> Optional[dict]:
    """
    获取品牌表明细
    对应原 BRANDHelper.GetBRANDDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {brand_id}"
    rows = db.execute_query(sql)
    return rows[0] if rows else None


def synchro_brand(db: DatabaseHelper, brand_data: dict) -> tuple[bool, dict]:
    """
    同步品牌表（新增或更新）
    对应原 BRANDHelper.SynchroBRAND
    返回: (是否成功, 数据对象)
    """
    brand_id = brand_data.get("BRAND_ID")

    if brand_id is not None:
        # 更新：检查记录是否存在
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {brand_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, brand_data

        # 构建 UPDATE 语句
        set_parts = []
        for key, value in brand_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {brand_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增：获取序列下一个值
        seq_sql = f"SELECT {SEQUENCE_NAME}.NEXTVAL"
        new_id = db.execute_scalar(seq_sql)
        brand_data["BRAND_ID"] = new_id

        # 构建 INSERT 语句
        columns = []
        values = []
        for key, value in brand_data.items():
            if value is None:
                continue
            columns.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, brand_data


def delete_brand(db: DatabaseHelper, brand_id: int) -> bool:
    """
    删除品牌表（软删除，设 BRAND_STATE=0）
    对应原 BRANDHelper.DeleteBRAND
    """
    sql = f"UPDATE {TABLE_NAME} SET BRAND_STATE = 0 WHERE {PRIMARY_KEY} = {brand_id}"
    count = db.execute_non_query(sql)
    return count > 0
