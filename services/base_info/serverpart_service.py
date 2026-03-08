from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区站点业务服务
替代原 ServerpartHelper.cs，保持相同的业务逻辑
注意：SERVERPART 只有 GetList 和 Delete 两个标准接口
Delete 为真删除（_SERVERPART.Delete()），非软删除
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_SERVERPART"
PRIMARY_KEY = "SERVERPART_ID"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    query_type: 0=模糊查询, 1=精确查询
    额外处理 SERVERPART_IDS 和 SERVERPART_CODES 字段（原 C# 中做了特殊处理）
    """
    skip_fields = {
        "SERVERPART_IDS", "SERVERPART_CODES",
    } | SEARCH_PARAM_SKIP_FIELDS
    conditions = []
    for key, value in search_param.items():
        if key in skip_fields:
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


def get_serverpart_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区站点列表
    对应原 ServerpartHelper.GetSERVERPARTList
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

        # 特殊处理 SERVERPART_IDS：IN 查询
        serverpart_ids = search_model.SearchParameter.get("SERVERPART_IDS")
        if serverpart_ids and str(serverpart_ids).strip():
            extra = f"SERVERPART_ID IN ({serverpart_ids})"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

        # 特殊处理 SERVERPART_CODES：IN 查询
        serverpart_codes = search_model.SearchParameter.get("SERVERPART_CODES")
        if serverpart_codes and str(serverpart_codes).strip():
            codes = "','".join(str(serverpart_codes).split(","))
            extra = f"SERVERPART_CODE IN ('{codes}')"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

    # 构建基础查询 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 添加关键字过滤
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

    # 分页处理
    page_index = search_model.PageIndex
    page_size = search_model.PageSize

    if page_index <= 0 or page_size <= 0:
        rows = db.execute_query(base_sql)
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


def delete_serverpart(db: DatabaseHelper, serverpart_id: int) -> bool:
    """
    删除服务区站点（真删除）
    对应原 ServerpartHelper.DeleteSERVERPART
    注意：原 C# 代码是真删除 _SERVERPART.Delete()，非软删除
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpart_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpart_id}"
    db.execute_non_query(sql)
    return True


def synchro_serverpart(db: DatabaseHelper, model: dict) -> tuple:
    """
    同步服务区数据（新增/更新）
    对应原 ServerpartHelper.SynchroSERVERPART (L905-1013)

    逻辑：
    1. 有 SERVERPART_ID → 更新；无 → 新增
    2. PROVINCE_CODE 仅新增时设置（已有不覆盖）
    3. 如果有 SPREGIONTYPE_ID，同步 T_SPSTATICTYPE 片区关联
    4. 子表同步 (RTSERVERPART / SERVERPARTINFO) 暂标记 TODO

    返回: (成功标志, 更新后的 model)
    """
    from datetime import datetime

    # 排除非数据库字段
    exclude_fields = {
        "RtServerPart", "ServerPartInfo",  # 子对象
        "SPREGIONTYPE_ID",  # 在外层单独处理
    } | SEARCH_PARAM_SKIP_FIELDS

    serverpart_id = model.get("SERVERPART_ID")
    if serverpart_id:
        # 更新：先检查是否存在
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpart_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, model

        # 获取现有记录，检查 PROVINCE_CODE 是否已有值
        existing = db.execute_query(
            f"SELECT PROVINCE_CODE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpart_id}"
        )
        existing_province = existing[0].get("PROVINCE_CODE") if existing else None

        # 构建 UPDATE 语句
        set_parts = []
        for key, value in model.items():
            if key == PRIMARY_KEY or key in exclude_fields:
                continue
            # PROVINCE_CODE 已有不覆盖（原 C# L1033-1036）
            if key == "PROVINCE_CODE" and existing_province is not None:
                continue
            if value is None:
                set_parts.append(f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {serverpart_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增
        cols = []
        vals = []
        for key, value in model.items():
            if key == PRIMARY_KEY or key in exclude_fields:
                continue
            if value is None:
                continue
            cols.append(key)
            if isinstance(value, str):
                vals.append(f"'{value}'")
            else:
                vals.append(str(value))

        # 尝试用序列，失败则用 MAX+1
        try:
            insert_sql = (
                f"INSERT INTO {TABLE_NAME} ({PRIMARY_KEY}, {', '.join(cols)}) "
                f"VALUES (SEQ_SERVERPART.NEXTVAL, {', '.join(vals)})"
            )
            db.execute_non_query(insert_sql)
            new_id = db.execute_scalar("SELECT SEQ_SERVERPART.CURRVAL FROM DUAL")
        except Exception:
            max_id = db.execute_scalar(f"SELECT NVL(MAX({PRIMARY_KEY}), 0) + 1 FROM {TABLE_NAME}") or 1
            insert_sql = (
                f"INSERT INTO {TABLE_NAME} ({PRIMARY_KEY}, {', '.join(cols)}) "
                f"VALUES ({max_id}, {', '.join(vals)})"
            )
            db.execute_non_query(insert_sql)
            new_id = max_id

        model["SERVERPART_ID"] = new_id
        serverpart_id = new_id

    # 同步 T_SPSTATICTYPE 片区关联（原 C# L966-991）
    spregiontype_id = model.get("SPREGIONTYPE_ID")
    if spregiontype_id is not None and serverpart_id:
        sp_count = db.execute_scalar(
            f"SELECT COUNT(*) FROM T_SPSTATICTYPE WHERE SERVERPART_ID = {serverpart_id}"
        ) or 0
        if sp_count == 0:
            # 无关联记录，直接插入
            try:
                db.execute_non_query(
                    f"INSERT INTO T_SPSTATICTYPE (SERVERPART_ID, SERVERPARTTYPE_ID) "
                    f"VALUES ({serverpart_id}, {spregiontype_id})"
                )
            except Exception as e:
                logger.warning(f"插入 SPSTATICTYPE 失败: {e}")
        else:
            # 有关联但无当前片区类型，先删旧的再插新的
            same_count = db.execute_scalar(
                f"SELECT COUNT(*) FROM T_SPSTATICTYPE WHERE SERVERPART_ID = {serverpart_id} "
                f"AND SERVERPARTTYPE_ID = {spregiontype_id}"
            ) or 0
            if same_count == 0:
                try:
                    db.execute_non_query(
                        f"DELETE FROM T_SPSTATICTYPE WHERE SERVERPART_ID = {serverpart_id}"
                    )
                    db.execute_non_query(
                        f"INSERT INTO T_SPSTATICTYPE (SERVERPART_ID, SERVERPARTTYPE_ID) "
                        f"VALUES ({serverpart_id}, {spregiontype_id})"
                    )
                except Exception as e:
                    logger.warning(f"更新 SPSTATICTYPE 失败: {e}")

    # TODO: 子表同步
    # - RTSERVERPARTHelper.SynchroRTSERVERPART (原 L998)
    # - SERVERPARTINFOHelper.SynchroSERVERPARTINFO (原 L1001-1009)

    return True, model
