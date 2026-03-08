from __future__ import annotations
# -*- coding: utf-8 -*-
"""
在售商品业务服务
替代原 SaleCommodityHelper.cs（1139行）
使用 HIGHWAY_STORAGE.V_WHOLE_COMMODITY 视图 + T_COMMODITY 表
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名/视图常量
VIEW_NAME = "V_WHOLE_COMMODITY"
PRIMARY_KEY = "COMMODITY_ID"

# 排除字段（非数据库字段）
EXCLUDE_FIELDS = {
    "COMMODITY_TYPE", "SERVERPART_IDS", "SERVERPARTSHOP_IDS", "QUALIFICATION_ID",
    "HIGHWAYPROINST_ID", "SHOPNAME", "SERVERPART_NAME",
    "COMMODITY_BUSINESS_ID", "originCommodity", "DATATYPE",
}


def _get_commodity_table(province_code) -> str:
    """
    根据省份编码获取实际商品表名
    原 C#: ProvinceCode == 620000 ? "" : "_" + ProvinceCode
    620000（甘肃）用主表 T_COMMODITY，其他省份用分表 T_COMMODITY_{省份编码}
    """
    if province_code is None or int(province_code) == 620000:
        return "T_COMMODITY"
    return f"T_COMMODITY_{province_code}"


def _build_where_sql(search_param: dict, query_type: int = 0, prefix: str = "") -> str:
    """构建 WHERE 条件，排除特殊字段"""
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS:
            continue
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        col = prefix + key
        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{col} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{col} = '{value}'")
            else:
                conditions.append(f"{col} = {value}")
    return " AND ".join(conditions)


def _build_keyword_filter(keyword: dict) -> str:
    """构建关键字过滤条件"""
    if not keyword or not keyword.get("Key") or not keyword.get("Value"):
        return ""
    keys = keyword["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{keyword['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


# ========== 1. GetCOMMODITYList ==========

def get_commodity_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取在售商品列表
    对应原 SaleCommodityHelper.GetCOMMODITYList（L28-232）
    查询 V_WHOLE_COMMODITY 视图，关联 T_RTCOMMODITYBUSINESS、T_COMMODITY_BUSINESS、T_SERVERPART
    """
    where_sql = ""
    shop_where_sql = ""
    qualification_search = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter

        # 通用条件（带 A. 前缀）
        where_clause = _build_where_sql(sp, search_model.QueryType or 0, "A.")
        if where_clause:
            where_sql = " AND " + where_clause

        # 商品类型（含子类型递归查询）
        commodity_type = sp.get("COMMODITY_TYPE")
        if commodity_type and str(commodity_type).strip():
            # 查询该类型及所有子类型
            type_ids = _get_sub_commodity_types(db, str(commodity_type))
            type_in = "','".join(type_ids)
            where_sql += f" AND COMMODITY_TYPE IN ('{type_in}')"

        # 服务区内码
        serverpart_id = sp.get("SERVERPART_ID")
        serverpart_ids = sp.get("SERVERPART_IDS")
        if serverpart_id is not None:
            shop_where_sql += f" WHERE SERVERPART_ID = {serverpart_id}" if not shop_where_sql else f" AND SERVERPART_ID = {serverpart_id}"
            where_sql += f" AND A.SERVERPART_ID = {serverpart_id}"
        elif serverpart_ids and str(serverpart_ids).strip():
            shop_where_sql += f" WHERE SERVERPART_ID IN ({serverpart_ids})" if not shop_where_sql else f" AND SERVERPART_ID IN ({serverpart_ids})"
            where_sql += f" AND A.SERVERPART_ID IN ({serverpart_ids})"

        # 商家门店
        shop_ids = sp.get("SERVERPARTSHOP_IDS")
        if shop_ids and str(shop_ids).strip():
            shop_where_sql += f" WHERE SERVERPARTSHOP_ID IN ({shop_ids})" if not shop_where_sql else f" AND SERVERPARTSHOP_ID IN ({shop_ids})"
            where_sql += f" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP E WHERE A.SERVERPART_ID = E.SERVERPART_ID AND A.BUSINESSTYPE = E.SHOPTRADE AND E.SERVERPARTSHOP_ID IN ({shop_ids}))"

        # 资质证书筛选
        qualification_search = sp.get("QUALIFICATION_ID") or ""

    # 查询门店数据源（用于关联门店名称）
    shop_sql = f"SELECT SERVERPART_ID, SHOPTRADE, SHOPSHORTNAME FROM T_SERVERPARTSHOP{' ' + shop_where_sql if shop_where_sql else ''}"
    try:
        shop_rows = db.execute_query(shop_sql)
    except Exception:
        shop_rows = []

    # 构建门店 map: (SERVERPART_ID, SHOPTRADE) -> SHOPSHORTNAME
    shop_map = {}
    for s in shop_rows:
        key = (s.get("SERVERPART_ID"), str(s.get("SHOPTRADE") or ""))
        shop_map[key] = s.get("SHOPSHORTNAME") or ""

    # 查询商品数据源（和原 C# 完全一致的 SQL）
    base_sql = f"""SELECT
            A.*, C.COMMODITY_BUSINESS_ID,
            NVL(A.COMMODITY_BRAND, TO_CHAR(C.QUALIFICATION_ID)) AS QUALIFICATION_ID,
            D.SERVERPART_NAME
        FROM
            V_WHOLE_COMMODITY A,
            T_RTCOMMODITYBUSINESS B,
            T_COMMODITY_BUSINESS C,
            T_SERVERPART D
        WHERE
            A.COMMODITY_ID = B.COMMODITY_ID AND A.SERVERPART_ID = D.SERVERPART_ID AND
            B.COMMODITY_BUSINESS_ID = C.COMMODITY_BUSINESS_ID{where_sql}
        UNION ALL
        SELECT
            A.*, NULL, A.COMMODITY_BRAND, D.SERVERPART_NAME
        FROM
            V_WHOLE_COMMODITY A,
            T_SERVERPART D
        WHERE
            A.SERVERPART_ID = D.SERVERPART_ID AND
            NOT EXISTS (SELECT 1 FROM T_RTCOMMODITYBUSINESS B
                WHERE A.COMMODITY_ID = B.COMMODITY_ID){where_sql}"""

    # 关键字过滤（内存过滤，和原 C# 一致使用 RowFilter）
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        keyword_filter = _build_keyword_filter(kw)
        if keyword_filter:
            base_sql = f"SELECT * FROM ({base_sql}) WHERE ({keyword_filter})"

    # 资质证书过滤
    if qualification_search == "0":
        base_sql = f"SELECT * FROM ({base_sql}) WHERE QUALIFICATION_ID IS NOT NULL"
    elif qualification_search == "-1":
        base_sql = f"SELECT * FROM ({base_sql}) WHERE QUALIFICATION_ID IS NULL"
    elif qualification_search:
        base_sql = f"SELECT * FROM ({base_sql}) WHERE QUALIFICATION_ID IN ({qualification_search})"

    # 排序
    order_sql = ""
    if search_model.SortStr:
        order_sql = f" ORDER BY {search_model.SortStr}"

    # 总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start_row = (page_index - 1) * page_size + 1
        end_row = page_index * page_size
        paged_sql = f"""
            SELECT * FROM (
                SELECT A2.*, ROWNUM RN FROM ({base_sql}{order_sql}) A2
                WHERE ROWNUM <= {end_row}
            ) WHERE RN >= {start_row}
        """
        rows = db.execute_query(paged_sql)
        for row in rows:
            row.pop("RN", None)
    else:
        rows = db.execute_query(base_sql + order_sql)

    # 补充门店名称
    for row in rows:
        sp_id = row.get("SERVERPART_ID")
        btype = str(row.get("BUSINESSTYPE") or "")
        row["SHOPNAME"] = shop_map.get((sp_id, btype), "")

    return int(total_count), rows


def _get_sub_commodity_types(db: DatabaseHelper, type_id: str) -> list:
    """
    递归获取商品类型及所有子类型
    对应原 Business.COMMODITYTYPE.GetSubCommodityType
    """
    result = [type_id]
    try:
        sql = f"SELECT COMMODITYTYPE_ID FROM T_COMMODITYTYPE WHERE PARENT_ID = '{type_id}'"
        rows = db.execute_query(sql)
        for row in rows:
            child_id = str(row.get("COMMODITYTYPE_ID") or "")
            if child_id and child_id not in result:
                result.extend(_get_sub_commodity_types(db, child_id))
    except Exception:
        pass
    return result


# ========== 2. GetCOMMODITYDetail ==========

def get_commodity_detail(db: DatabaseHelper, commodity_id: int) -> Optional[dict]:
    """
    获取在售商品明细
    对应原 SaleCommodityHelper.GetCOMMODITYDetail（L526-565）
    直接查 V_WHOLE_COMMODITY 视图
    """
    sql = f"SELECT * FROM {VIEW_NAME} WHERE {PRIMARY_KEY} = {commodity_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    return rows[0]


# ========== 3. SynchroCOMMODITY ==========

def synchro_commodity(db: DatabaseHelper, data: dict) -> bool:
    """
    同步在售商品（新增/更新）
    对应原 SaleCommodityHelper.SynchroCOMMODITY（L574-609）
    注意：原方法含 WebSocket 指令下发到收银机（PostCommandToSocketService），Python 版跳过
    """
    commodity_id = data.get("COMMODITY_ID")
    province_code = data.get("PROVINCE_CODE")
    table_name = _get_commodity_table(province_code)

    # 移除非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS and v is not None}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if commodity_id is not None:
        # 更新模式
        check = db.execute_query(f"SELECT * FROM {table_name} WHERE {PRIMARY_KEY} = {commodity_id}")
        if not check:
            return False

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {commodity_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增模式
        try:
            new_id = db.execute_scalar("SELECT SEQ_COMMODITY.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {table_name}") or 0) + 1

        db_data["COMMODITY_ID"] = new_id
        db_data["ADDTIME"] = now

        columns = []
        values = []
        for key, value in db_data.items():
            columns.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)
        data["COMMODITY_ID"] = new_id

    # 原 C# 这里会查门店信息然后下发 WebSocket 指令到收银机，Python 版跳过
    logger.debug(f"商品同步完成，COMMODITY_ID={commodity_id or data.get('COMMODITY_ID')}, WebSocket 指令跳过")

    return True


# ========== 4. DeleteCOMMODITY ==========

def delete_commodity(db: DatabaseHelper, commodity_id: int) -> bool:
    """
    删除在售商品（软删除 COMMODITY_STATE=0）
    对应原 SaleCommodityHelper.DeleteCOMMODITY（L657-673）
    """
    # 先检查记录存在
    check = db.execute_query(f"SELECT PROVINCE_CODE FROM {VIEW_NAME} WHERE {PRIMARY_KEY} = {commodity_id}")
    if not check:
        return False

    province_code = check[0].get("PROVINCE_CODE")
    table_name = _get_commodity_table(province_code)

    sql = f"UPDATE {table_name} SET COMMODITY_STATE = 0 WHERE {PRIMARY_KEY} = {commodity_id}"
    affected = db.execute_non_query(sql)
    return affected is not None and affected > 0


# ========== 5. OnShelfCommodity ==========

def on_shelf_commodity(db: DatabaseHelper, province_code, commodity_ids: str, staff_name: str) -> bool:
    """
    上架在售商品
    对应原 SaleCommodityHelper.OnShelfCommodity（L684-739）
    1. 先备份当前数据到 HIGHWAY_HISTORY.T_COMMODITY
    2. 更新 COMMODITY_STATE=1，记录操作描述
    3. 下发 WebSocket 指令到收银机（跳过）
    """
    if not commodity_ids:
        return False

    table_name = _get_commodity_table(province_code)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_count = 0

    # 1. 备份到历史表
    try:
        backup_sql = f"""INSERT INTO T_COMMODITY_HISTORY (
                COMMODITY_ID, COMMODITY_TYPE, COMMODITY_CODE, COMMODITY_NAME, COMMODITY_BARCODE,
                COMMODITY_EN, COMMODITY_UNIT, COMMODITY_RULE, COMMODITY_ORI, COMMODITY_GRADE,
                COMMODITY_RETAILPRICE, COMMODITY_MEMBERPRICE, COMMODITY_PURCHASEPRICE,
                DUTY_PARAGRAPH, RETAIL_DUTY, ADDTIME, CANSALE, SERVERPART_ID, PROVINCE_CODE,
                BUSINESSTYPE, ISBULK, METERINGMETHOD, OPERATE_DATE, COMMODITY_SYMBOL,
                COMMODITY_HOTKEY, USERDEFINEDTYPE_ID, COMMODITY_STATE, COMMODITY_DESC)
            SELECT
                COMMODITY_ID, COMMODITY_TYPE, COMMODITY_CODE, COMMODITY_NAME, COMMODITY_BARCODE,
                COMMODITY_EN, COMMODITY_UNIT, COMMODITY_RULE, COMMODITY_ORI, COMMODITY_GRADE,
                COMMODITY_RETAILPRICE, COMMODITY_MEMBERPRICE, COMMODITY_PURCHASEPRICE,
                DUTY_PARAGRAPH, RETAIL_DUTY, ADDTIME, CANSALE, SERVERPART_ID, PROVINCE_CODE,
                BUSINESSTYPE, ISBULK, METERINGMETHOD, OPERATE_DATE, COMMODITY_SYMBOL,
                COMMODITY_HOTKEY, USERDEFINEDTYPE_ID, COMMODITY_STATE, COMMODITY_DESC
            FROM {table_name}
            WHERE COMMODITY_ID IN ({commodity_ids})"""
        result = db.execute_non_query(backup_sql)
        execute_count += (result or 0)
    except Exception as e:
        logger.warning(f"备份商品到历史表失败（可能缺少历史表）: {e}")

    # 2. 更新状态为上架（STATE=1），追加操作描述
    desc = f"{staff_name or ''}于{now}重新上架了商品"
    update_sql = f"""UPDATE {table_name}
        SET COMMODITY_STATE = 1,
            OPERATE_DATE = TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
            COMMODITY_DESC = CASE WHEN COMMODITY_DESC IS NULL THEN '{desc}'
                ELSE COMMODITY_DESC || '　' || '{desc}' END
        WHERE COMMODITY_ID IN ({commodity_ids})"""
    result = db.execute_non_query(update_sql)
    execute_count += (result or 0)

    # 3. WebSocket 指令下发（跳过）
    logger.debug(f"商品上架完成，IDs={commodity_ids}, WebSocket 指令跳过")

    return execute_count > 0


# ========== 6. LowerShelfCommodity ==========

def lower_shelf_commodity(db: DatabaseHelper, province_code, commodity_ids: str, commodity_state: int = 0) -> bool:
    """
    下架在售商品
    对应原 SaleCommodityHelper.LowerShelfCommodity（L750-800）
    1. 先备份当前数据到 HIGHWAY_HISTORY.T_COMMODITY
    2. 更新 COMMODITY_STATE=指定值（默认0）
    3. 更新 T_RTCOMMODITYBUSINESS VALID_STATUS=0
    4. 下发 WebSocket 指令到收银机（跳过）
    """
    if not commodity_ids:
        return False

    table_name = _get_commodity_table(province_code)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_count = 0

    # 1. 备份到历史表
    try:
        backup_sql = f"""INSERT INTO T_COMMODITY_HISTORY (
                COMMODITY_ID, COMMODITY_TYPE, COMMODITY_CODE, COMMODITY_NAME, COMMODITY_BARCODE,
                COMMODITY_EN, COMMODITY_UNIT, COMMODITY_RULE, COMMODITY_ORI, COMMODITY_GRADE,
                COMMODITY_RETAILPRICE, COMMODITY_MEMBERPRICE, COMMODITY_PURCHASEPRICE,
                DUTY_PARAGRAPH, RETAIL_DUTY, ADDTIME, CANSALE, SERVERPART_ID, PROVINCE_CODE,
                BUSINESSTYPE, ISBULK, METERINGMETHOD, OPERATE_DATE, COMMODITY_SYMBOL,
                COMMODITY_HOTKEY, USERDEFINEDTYPE_ID, COMMODITY_STATE, COMMODITY_DESC)
            SELECT
                COMMODITY_ID, COMMODITY_TYPE, COMMODITY_CODE, COMMODITY_NAME, COMMODITY_BARCODE,
                COMMODITY_EN, COMMODITY_UNIT, COMMODITY_RULE, COMMODITY_ORI, COMMODITY_GRADE,
                COMMODITY_RETAILPRICE, COMMODITY_MEMBERPRICE, COMMODITY_PURCHASEPRICE,
                DUTY_PARAGRAPH, RETAIL_DUTY, ADDTIME, CANSALE, SERVERPART_ID, PROVINCE_CODE,
                BUSINESSTYPE, ISBULK, METERINGMETHOD, OPERATE_DATE, COMMODITY_SYMBOL,
                COMMODITY_HOTKEY, USERDEFINEDTYPE_ID, COMMODITY_STATE, COMMODITY_DESC
            FROM {table_name}
            WHERE COMMODITY_ID IN ({commodity_ids})"""
        result = db.execute_non_query(backup_sql)
        execute_count += (result or 0)
    except Exception as e:
        logger.warning(f"备份商品到历史表失败（可能缺少历史表）: {e}")

    # 2. 更新状态为下架
    update_sql = f"""UPDATE {table_name}
        SET COMMODITY_STATE = {commodity_state},
            OPERATE_DATE = TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS')
        WHERE COMMODITY_ID IN ({commodity_ids})"""
    result = db.execute_non_query(update_sql)
    execute_count += (result or 0)

    # 3. 更新 T_RTCOMMODITYBUSINESS VALID_STATUS=0
    try:
        rt_sql = f"UPDATE T_RTCOMMODITYBUSINESS SET VALID_STATUS = 0 WHERE COMMODITY_ID IN ({commodity_ids})"
        result = db.execute_non_query(rt_sql)
        execute_count += (result or 0)
    except Exception as e:
        logger.warning(f"更新 T_RTCOMMODITYBUSINESS 失败: {e}")

    # 4. WebSocket 指令下发（跳过）
    logger.debug(f"商品下架完成，IDs={commodity_ids}, WebSocket 指令跳过")

    return execute_count > 0
