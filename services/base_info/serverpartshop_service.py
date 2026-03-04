from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店业务服务
替代原 ServerpartShopHelper.cs，保持相同的业务逻辑

接口列表（5个）：
- GetServerpartShopList: POST, 分页列表查询
- GetServerpartShopDetail: GET, 门店明细查询
- SynchroServerpartShop: POST, 同步（新增/更新）
- DeleteServerpartShop: GET, 软删除（ISVALID=0）
- DelServerpartShop: POST, 软删除（批量，入参 BaseOperateModel）

注意：
1. Delete 为软删除（ISVALID=0），非真删除
2. GetList 中 BUSINESS_ENDDATE 展示时 +1天
3. GetList 有特殊过滤：UserPattern==2000 且无 SERVERPARTSHOP_IDS 时返回空列表
   （此逻辑依赖登录凭证的 UserPattern 字段，Python 侧暂无此概念，先不做处理）
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel

# 表名常量
TABLE_NAME = "T_SERVERPARTSHOP"
PRIMARY_KEY = "SERVERPARTSHOP_ID"


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """
    根据查询参数构建 WHERE 条件
    query_type: 0=模糊查询, 1=精确查询
    跳过搜索辅助字段（SERVERPARTSHOP_IDS, SERVERPART_IDS, SERVERPART_CODE, PROVINCE_CODE）
    这些字段在外层单独处理
    """
    # 需要跳过的辅助字段（在外层做特殊 IN 查询）
    skip_fields = {
        "SERVERPARTSHOP_IDS", "SERVERPART_IDS", "SERVERPART_CODE", "PROVINCE_CODE"
    }
    conditions = []
    for key, value in search_param.items():
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        if key in skip_fields:
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


def get_serverpartshop_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取门店列表
    对应原 ServerpartShopHelper.GetSERVERPARTSHOPList
    返回: (总数, 数据列表)

    特殊处理（对应原 C# 逻辑）：
    - SERVERPARTSHOP_IDS: IN 查询门店内码
    - SERVERPART_IDS: IN 查询服务区内码
    - SERVERPART_CODE: IN 查询服务区编码（逗号分隔转 IN）
    - PROVINCE_CODE: EXISTS 子查询关联 T_SERVERPART
    - 默认附加 SERVERPART_ID IS NOT NULL（无 PROVINCE_CODE 时）
    - BUSINESS_ENDDATE 展示时 +1天
    """
    where_sql = ""
    if search_model.SearchParameter:
        # 基础条件构建
        where_clause = _build_where_sql(
            search_model.SearchParameter,
            search_model.QueryType or 0
        )
        if where_clause:
            where_sql = f" WHERE {where_clause}"

        # 特殊处理 SERVERPARTSHOP_IDS：IN 查询
        shop_ids = search_model.SearchParameter.get("SERVERPARTSHOP_IDS")
        if shop_ids and str(shop_ids).strip():
            extra = f"SERVERPARTSHOP_ID IN ({shop_ids})"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

        # 特殊处理 SERVERPART_IDS：IN 查询
        sp_ids = search_model.SearchParameter.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            extra = f"SERVERPART_ID IN ({sp_ids})"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"
        else:
            # SERVERPART_CODE：仅当无 SERVERPART_IDS 时处理
            sp_code = search_model.SearchParameter.get("SERVERPART_CODE")
            if sp_code and str(sp_code).strip():
                codes = "','".join(str(sp_code).split(","))
                extra = f"SERVERPART_CODE IN ('{codes}')"
                where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

        # PROVINCE_CODE：EXISTS 子查询
        province_code = search_model.SearchParameter.get("PROVINCE_CODE")
        if province_code is not None:
            extra = (
                f"EXISTS (SELECT 1 FROM T_SERVERPART "
                f"WHERE T_SERVERPART.SERVERPART_ID = T_SERVERPARTSHOP.SERVERPART_ID "
                f"AND PROVINCE_CODE = {province_code})"
            )
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"
        else:
            # 默认附加 SERVERPART_ID IS NOT NULL
            extra = "SERVERPART_ID IS NOT NULL"
            where_sql += f" AND {extra}" if where_sql else f" WHERE {extra}"

    # 构建基础查询 SQL
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 添加关键字过滤（对应原 C# 的 RowFilter）
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

    # BUSINESS_ENDDATE 展示时 +1天（对应原 C# 的 .AddDays(1)）
    for row in rows:
        if row.get("BUSINESS_ENDDATE"):
            try:
                from datetime import timedelta
                row["BUSINESS_ENDDATE"] = row["BUSINESS_ENDDATE"] + timedelta(days=1)
            except Exception:
                pass

    return int(total_count), rows


def get_serverpartshop_detail(db: DatabaseHelper, serverpartshop_id: int) -> dict:
    """
    获取门店明细
    对应原 ServerpartShopHelper.GetSERVERPARTSHOPDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpartshop_id}"
    rows = db.execute_query(sql)
    if rows:
        return rows[0]
    return {}


def synchro_serverpartshop(db: DatabaseHelper, model: dict) -> tuple:
    """
    同步门店数据（新增/更新）
    对应原 ServerpartShopHelper.SynchroSERVERPARTSHOP

    逻辑：
    1. 如果有 SERVERPART_ID 但无 SERVERPART_CODE，自动从 T_SERVERPART 补全关联信息
    2. 如果无 OPERATE_DATE，设置为当前时间
    3. 有 SERVERPARTSHOP_ID → 更新；无 → 新增

    返回: (成功标志, 更新后的 model)
    """
    from datetime import datetime

    # 补全服务区信息
    if model.get("SERVERPART_ID") and not model.get("SERVERPART_CODE"):
        sp_sql = (
            f"SELECT SERVERPART_CODE, SERVERPART_NAME, OWNERUNIT_ID, OWNERUNIT_NAME "
            f"FROM T_SERVERPART WHERE SERVERPART_ID = {model['SERVERPART_ID']}"
        )
        sp_rows = db.execute_query(sp_sql)
        if sp_rows:
            sp = sp_rows[0]
            model["SERVERPART_CODE"] = sp.get("SERVERPART_CODE")
            model["SERVERPART_NAME"] = sp.get("SERVERPART_NAME")
            model["OWNERUNIT_ID"] = sp.get("OWNERUNIT_ID")
            model["OWNERUNIT_NAME"] = sp.get("OWNERUNIT_NAME")

    # 设置默认操作时间
    if not model.get("OPERATE_DATE"):
        model["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 排除搜索辅助字段，不写入数据库
    exclude_fields = {
        "SERVERPARTSHOP_IDS", "SERVERPART_IDS", "PROVINCE_CODE",
        "TAXPAYER_IDENTIFYCODE", "BANK_NAME", "BANK_ACCOUNT"
    }

    serverpartshop_id = model.get("SERVERPARTSHOP_ID")
    if serverpartshop_id:
        # 更新：先检查是否存在
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpartshop_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, model

        # 构建 UPDATE 语句
        set_parts = []
        for key, value in model.items():
            if key == PRIMARY_KEY or key in exclude_fields:
                continue
            if value is None:
                set_parts.append(f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {serverpartshop_id}"
            db.execute_non_query(update_sql)
        return True, model
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

        insert_sql = (
            f"INSERT INTO {TABLE_NAME} ({PRIMARY_KEY}, {', '.join(cols)}) "
            f"VALUES (SEQ_SERVERPARTSHOP.NEXTVAL, {', '.join(vals)})"
        )
        db.execute_non_query(insert_sql)

        # 获取新插入的 ID
        id_sql = "SELECT SEQ_SERVERPARTSHOP.CURRVAL FROM DUAL"
        try:
            new_id = db.execute_scalar(id_sql)
            model["SERVERPARTSHOP_ID"] = new_id
        except Exception:
            pass

        return True, model


def delete_serverpartshop(db: DatabaseHelper, serverpartshop_id: int,
                          operate_id: Optional[float] = None,
                          operate_name: Optional[str] = None) -> bool:
    """
    软删除门店（ISVALID=0）
    对应原 ServerpartShopHelper.DeleteSERVERPARTSHOP

    注意：原 C# 代码是软删除，设置 ISVALID=0 + 更新操作员信息
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {serverpartshop_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    # 构建更新 SQL：ISVALID=0 + 操作员信息
    set_parts = ["ISVALID = 0"]
    if operate_id is not None:
        set_parts.append(f"STAFF_ID = {operate_id}")
    if operate_name:
        set_parts.append(f"STAFF_NAME = '{operate_name}'")

    sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {serverpartshop_id}"
    db.execute_non_query(sql)
    return True
