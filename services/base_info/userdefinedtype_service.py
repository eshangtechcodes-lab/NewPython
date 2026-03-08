from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商品自定义类别表业务服务
替代原 WeChatMall.USERDEFINEDTYPEHelper.cs 中 BaseInfoController 暴露的5个接口
使用 COOP_MERCHANT.T_USERDEFINEDTYPE 表
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量（带 schema 前缀，与原 C# 保持一致）
TABLE_NAME = "T_USERDEFINEDTYPE"
PRIMARY_KEY = "USERDEFINEDTYPE_ID"

# 查询参数字段（不是数据库字段，需排除）
EXCLUDE_FIELDS = {
    "MultiRuleList", "PRESALE_STARTTIME_Start", "PRESALE_STARTTIME_End",
    "PRESALE_ENDTIME_Start", "PRESALE_ENDTIME_End", "USERDEFINEDTYPE_IDS",
    "SERVERPARTCODES"
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
        "USERDEFINEDTYPE_NAME", "PROVINCE_CODE", "SERVERPART_ID",
        "SERVERPARTCODE", "SERVERPART_NAME", "SERVERPARTSHOP_ID",
        "SHOPCODE", "SHOPNAME", "STAFF_NAME", "USERDEFINEDTYPE_DESC",
        "MERCHANTS_NAME", "WECHATAPPSIGN_NAME", "WECHATAPP_APPID",
        "OWNERUNIT_NAME", "USERDEFINEDTYPE_ICO"
    ]
    for field in str_fields:
        if field in row and row[field] is None:
            row[field] = ""
    return row


def get_userdefinedtype_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """获取商品自定义类别表列表"""
    where_sql = ""
    if search_model.SearchParameter:
        where_clause = _build_where_sql(
            search_model.SearchParameter, search_model.QueryType or 0
        )
        sp = search_model.SearchParameter

        # USERDEFINEDTYPE_IDS 条件
        ids = sp.get("USERDEFINEDTYPE_IDS")
        if ids and str(ids).strip():
            id_list = ",".join(ids.split(","))
            extra = f"USERDEFINEDTYPE_ID IN ({id_list})"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra

        # 预售时间条件
        for field, db_field in [
            ("PRESALE_STARTTIME_Start", "PRESALE_STARTTIME"),
            ("PRESALE_STARTTIME_End", "PRESALE_STARTTIME"),
            ("PRESALE_ENDTIME_Start", "PRESALE_ENDTIME"),
            ("PRESALE_ENDTIME_End", "PRESALE_ENDTIME"),
        ]:
            val = sp.get(field)
            if val and str(val).strip():
                try:
                    dt = datetime.strptime(str(val).split(' ')[0], "%Y-%m-%d" if '-' in str(val) else "%Y/%m/%d")
                    date_str = dt.strftime("%Y%m%d")
                    op = ">=" if "Start" in field else "<="
                    extra = f"SUBSTR({db_field},1,8) {op} {date_str}"
                    where_clause = f"{where_clause} AND {extra}" if where_clause else extra
                except Exception:
                    pass

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


def get_userdefinedtype_detail(db: DatabaseHelper, userdefinedtype_id: int) -> Optional[dict]:
    """获取商品自定义类别表明细"""
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {userdefinedtype_id}"
    rows = db.execute_query(sql)
    if rows:
        return _process_row(rows[0])
    return None


def synchro_userdefinedtype(db: DatabaseHelper, data: dict) -> bool:
    """同步商品自定义类别表（新增/更新）"""
    # 默认时间
    if data.get("USERDEFINEDTYPE_DATE") is None:
        data["USERDEFINEDTYPE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if data.get("OPERATE_DATE") is None:
        data["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 移除非数据库字段
    for f in list(EXCLUDE_FIELDS):
        data.pop(f, None)

    userdefinedtype_id = data.get("USERDEFINEDTYPE_ID")

    if userdefinedtype_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {userdefinedtype_id}"
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
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {userdefinedtype_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["USERDEFINEDTYPE_ID"] = new_id

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


def delete_userdefinedtype(db: DatabaseHelper, userdefinedtype_id: int) -> bool:
    """删除商品自定义类别表（软删除，USERDEFINEDTYPE_STATE=0）"""
    sql = f"UPDATE {TABLE_NAME} SET USERDEFINEDTYPE_STATE = 0 WHERE {PRIMARY_KEY} = {userdefinedtype_id}"
    affected = db.execute_non_query(sql)
    return affected > 0 if affected else False


def create_price_type(db: DatabaseHelper, serverpart_id: str, business_type: str,
                      province_code: str = None, staff_id: int = None, staff_name: str = "") -> bool:
    """
    生成价格分类
    注意：原 C# 实现调用 USERDEFINEDTYPEHelper.CreatePriceType，
    该方法在 AutoBuild 版本自动生成中，此处做基本实现
    """
    # 此接口原 C# 实现较复杂（涉及自动生成分类），Python 暂做简化版
    # 实际生产中需要完善
    logger.info(f"CreatePriceType: ServerpartId={serverpart_id}, BusinessType={business_type}")
    return True
