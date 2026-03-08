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
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS

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
    # 需要跳过的辅助字段（在外层做特殊 IN 查询 / 前端分页参数非数据库字段）
    skip_fields = {
        "SERVERPARTSHOP_IDS", "SERVERPART_IDS", "SERVERPART_CODE", "PROVINCE_CODE",
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


# ====================================================================
# ServerPartShopNew 相关接口（4个）
# 对应原 ServerpartShopHelper.cs 中 "New" 后缀方法
# ====================================================================

VIEW_NAME = "V_SERVERPARTSHOP_COMBINE"


def get_server_part_shop_new_list(db: DatabaseHelper,
                                  province_code=None,
                                  server_part_id=None,
                                  server_part_codes: str = None,
                                  shop_name: str = None,
                                  business_state=None,
                                  business_type=None,
                                  page_index: int = 0,
                                  page_size: int = 0) -> tuple:
    """
    获取门店组合列表（业主端使用）
    对应原 ServerpartShopHelper.GetServerPartShopNewList
    查询视图 V_SERVERPARTSHOP_COMBINE

    逻辑：
    1. 先根据 provinceCode / serverPartCodes 获取 serverPartIds
    2. 查视图 + 各种筛选条件
    3. 模糊搜索 shopName
    4. 分页

    返回: (总数, 列表)
    """
    conditions = []

    # 获取 serverPartIds（通过 provinceCode 或 serverPartCodes）
    server_part_ids = None
    if server_part_id:
        server_part_ids = str(server_part_id)
    elif server_part_codes:
        # 通过 codes 查 ids
        codes_in = "','".join(str(server_part_codes).split(","))
        id_sql = f"SELECT SERVERPART_ID FROM T_SERVERPART WHERE SERVERPART_CODE IN ('{codes_in}')"
        id_rows = db.execute_query(id_sql)
        if id_rows:
            server_part_ids = ",".join([str(r["SERVERPART_ID"]) for r in id_rows])
    elif province_code:
        id_sql = f"SELECT SERVERPART_ID FROM T_SERVERPART WHERE PROVINCE_CODE = {province_code}"
        id_rows = db.execute_query(id_sql)
        if id_rows:
            server_part_ids = ",".join([str(r["SERVERPART_ID"]) for r in id_rows])

    if server_part_ids:
        conditions.append(f"SERVERPART_ID IN ({server_part_ids})")

    if business_state is not None:
        conditions.append(f"BUSINESS_STATE = {business_state}")

    if business_type is not None:
        conditions.append(f"BUSINESS_TYPE = {business_type}")

    # 模糊搜索门店名称
    if shop_name and str(shop_name).strip():
        conditions.append(f"SHOPNAME LIKE '%{shop_name}%'")

    where_sql = ""
    if conditions:
        where_sql = " WHERE " + " AND ".join(conditions)

    base_sql = f"SELECT * FROM {VIEW_NAME}{where_sql} ORDER BY SERVERPART_INDEX, SERVERPART_ID"

    # 查询总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 分页
    if page_index > 0 and page_size > 0:
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
    else:
        rows = db.execute_query(base_sql)

    return int(total_count), rows


def get_server_part_shop_new_detail(db: DatabaseHelper, server_part_shop_id: int) -> dict:
    """
    获取门店明细（业主端使用，返回含经营状态列表和附属记录）
    对应原 ServerpartShopHelper.GetServerPartShopNewDetail

    逻辑：
    1. 查 T_SERVERPARTSHOP 获取门店基础信息
    2. 关联 COOPMERCHANTS 获取统一信用代码、银行信息
    3. 根据 BUSINESS_REGION（1000=双侧）加载对向门店
    4. 构建 ShopBusinessStateList（PascalCase 字段名）
    5. 查 T_RTSERVERPARTSHOP 获取附属记录

    返回: {"ServerPartShop": {...}, "ShopBusinessStateList": [...], "RtServerPartShopList": [...]}
    """
    from datetime import timedelta

    # 查门店基础信息
    shop_sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {server_part_shop_id}"
    rows = db.execute_query(shop_sql)
    if not rows:
        return {}

    shop = rows[0]

    # 关联查 COOPMERCHANTS 获取银行信息（通过 SELLER_ID）
    seller_id = shop.get("SELLER_ID")
    if seller_id:
        merchant_sql = (
            f"SELECT TAXPAYER_IDENTIFYCODE, BANK_NAME, BANK_ACCOUNT "
            f"FROM T_COOPMERCHANTS WHERE COOPMERCHANTS_ID = {seller_id}"
        )
        merchant_rows = db.execute_query(merchant_sql)
        if merchant_rows:
            m = merchant_rows[0]
            shop["TAXPAYER_IDENTIFYCODE"] = m.get("TAXPAYER_IDENTIFYCODE")
            shop["BANK_NAME"] = m.get("BANK_NAME")
            shop["BANK_ACCOUNT"] = m.get("BANK_ACCOUNT")

    # 经营合同名称（通过 REGISTERCOMPACT_ID 关联 T_COOPMERCHANTS）
    compact_id = shop.get("REGISTERCOMPACT_ID")
    if compact_id:
        compact_sql = f"SELECT COOPMERCHANTS_NAME FROM T_COOPMERCHANTS WHERE COOPMERCHANTS_ID = {compact_id}"
        compact_rows = db.execute_query(compact_sql)
        if compact_rows:
            shop["REGISTERCOMPACT_NAME"] = compact_rows[0].get("COOPMERCHANTS_NAME", "")
    else:
        shop["REGISTERCOMPACT_NAME"] = ""

    # 构建 ShopBusinessStateList
    shop_business_state_list = []

    # 当前门店的经营状态
    state_item = _build_shop_business_state(db, shop)
    shop_business_state_list.append(state_item)

    # 双侧门店逻辑：BUSINESS_REGION == 1000 或 2000 时，查对向门店
    # 对应原 C# 逻辑：按 SHOPSHORTNAME 匹配，或按 BUSINESS_BRAND+SELLER_ID 匹配
    business_region = shop.get("BUSINESS_REGION")
    if business_region in (1000, 2000):
        sql_where = ""
        shop_shortname = shop.get("SHOPSHORTNAME", "")
        if shop_shortname and str(shop_shortname).strip():
            sql_where = (
                f" WHERE SERVERPART_ID = {shop.get('SERVERPART_ID')} "
                f"AND SHOPSHORTNAME = '{shop_shortname}'"
            )
        elif shop.get("BUSINESS_BRAND") and shop.get("SELLER_ID"):
            sql_where = (
                f" WHERE SERVERPART_ID = {shop.get('SERVERPART_ID')} "
                f"AND BUSINESS_BRAND = {shop.get('BUSINESS_BRAND')} "
                f"AND SELLER_ID = {shop.get('SELLER_ID')}"
            )

        if sql_where:
            # 附加商品业态和有效性过滤
            if shop.get("SHOPTRADE") and str(shop.get("SHOPTRADE", "")).strip():
                sql_where += f" AND SHOPTRADE = '{shop['SHOPTRADE']}'"
            sql_where += f" AND ISVALID = 1 AND {PRIMARY_KEY} <> {server_part_shop_id}"

            opposite_sql = (
                f"SELECT SERVERPARTSHOP_ID, SHOPREGION, SHOPNAME, "
                f"BUSINESS_TYPE, BUSINESS_STATE, BUSINESS_DATE, BUSINESS_ENDDATE "
                f"FROM {TABLE_NAME}{sql_where}"
            )
            opposite_rows = db.execute_query(opposite_sql)
            if opposite_rows:
                import copy
                opp = opposite_rows[0]
                # 深拷贝原门店状态，仅覆盖特定字段
                opp_state = copy.deepcopy(state_item)
                if opp.get("SERVERPARTSHOP_ID"):
                    opp_state["ServerPartShopId"] = opp["SERVERPARTSHOP_ID"]
                if opp.get("SHOPREGION") is not None:
                    opp_state["ShopRegion"] = opp["SHOPREGION"]
                if opp.get("BUSINESS_TYPE") is not None:
                    opp_state["BusinessType"] = opp["BUSINESS_TYPE"]
                if opp.get("BUSINESS_STATE") is not None:
                    opp_state["BusinessState"] = opp["BUSINESS_STATE"]
                if opp.get("BUSINESS_DATE") is not None:
                    opp_state["BusinessDate"] = _format_datetime_iso(opp["BUSINESS_DATE"])
                if opp.get("BUSINESS_ENDDATE") is not None:
                    opp_state["BusinessEndDate"] = _format_datetime_iso(opp["BUSINESS_ENDDATE"])
                opp_state["ShopName"] = opp.get("SHOPNAME", "")
                shop_business_state_list.append(opp_state)

    # 查附属记录 T_RTSERVERPARTSHOP（所有门店 ID，含对向门店）
    all_shop_ids = [str(s["ServerPartShopId"]) for s in shop_business_state_list if s.get("ServerPartShopId")]
    rt_sql = (
        f"SELECT SERVERPARTSHOP_ID, SHOPNAME, BUSINESS_DATE, BUSINESS_ENDDATE, STAFF_NAME, OPERATE_DATE "
        f"FROM T_RTSERVERPARTSHOP WHERE SERVERPARTSHOP_ID IN ({','.join(all_shop_ids)}) "
        f"ORDER BY SERVERPARTSHOP_ID, BUSINESS_ENDDATE DESC"
    )
    rt_rows = db.execute_query(rt_sql)

    # 格式化 RtServerPartShopList（PascalCase 字段名 + 日期格式化）
    rt_list = []
    for rt in rt_rows:
        rt_item = {
            "ServerPartShopId": rt.get("SERVERPARTSHOP_ID"),
            "ShopName": rt.get("SHOPNAME"),
            "BusinessDate": _format_date_chinese(rt.get("BUSINESS_DATE")),
            "BusinessEndDate": _format_date_chinese(rt.get("BUSINESS_ENDDATE")),
            "StaffName": rt.get("STAFF_NAME", ""),
            "OperateDate": _format_datetime(rt.get("OPERATE_DATE")),
        }
        rt_list.append(rt_item)

    # BUSINESS_ENDDATE 展示时 +1天（对应原 C# 的 .AddDays(1)）
    if shop.get("BUSINESS_ENDDATE"):
        try:
            shop["BUSINESS_ENDDATE"] = shop["BUSINESS_ENDDATE"] + timedelta(days=1)
        except Exception:
            pass

    return {
        "ServerPartShop": shop,
        "ShopBusinessStateList": shop_business_state_list,
        "RtServerPartShopList": rt_list,
    }


def _build_shop_business_state(db: DatabaseHelper, shop: dict) -> dict:
    """构建 ShopBusinessStateModel（PascalCase 字段名，对应原 C# ShopBusinessStateModel）"""
    # 获取关联信息
    seller_id = shop.get("SELLER_ID")
    seller_name = ""
    if seller_id:
        seller_sql = f"SELECT SELLER_NAME FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {shop.get(PRIMARY_KEY)}"
        s_rows = db.execute_query(seller_sql)
        if s_rows:
            seller_name = s_rows[0].get("SELLER_NAME", "")

    return {
        "ServerPartId": shop.get("SERVERPART_ID"),
        "ServerPartName": shop.get("SERVERPART_NAME", ""),
        "ServerPartCode": shop.get("SERVERPART_CODE", ""),
        "ServerPartShopId": shop.get(PRIMARY_KEY),
        "SellerId": shop.get("SELLER_ID"),
        "SellerName": seller_name or shop.get("SELLER_NAME", ""),
        "TaxPayerIdEntityCode": shop.get("TAXPAYER_IDENTIFYCODE"),
        "BankAccount": shop.get("BANK_ACCOUNT"),
        "BusinessBrand": shop.get("BUSINESS_BRAND"),
        "BankName": shop.get("BANK_NAME"),
        "TopPerson": shop.get("TOPPERSON", ""),
        "TopPersonMobile": shop.get("TOPPERSON_MOBILE", ""),
        "LinkMan": shop.get("LINKMAN", ""),
        "LinkManMobile": shop.get("LINKMAN_MOBILE", ""),
        "ShopTrade": shop.get("SHOPTRADE", ""),
        "BusinessTrade": shop.get("BUSINESS_TRADE", ""),
        "BrandName": shop.get("BRAND_NAME", ""),
        "ShopShortName": shop.get("SHOPSHORTNAME", ""),
        "ServerPartShopDesc": shop.get("SERVERPARTSHOP_DESC", ""),
        "IsValid": shop.get("ISVALID"),
        "SaleCountLimit": shop.get("SALECOUNT_LIMIT"),
        "SaleAmountLimit": shop.get("SALEAMOUNT_LIMIT"),
        "RecordDiscount": shop.get("RECORD_DISCOUNT"),
        "BusinessRegion": shop.get("BUSINESS_REGION"),
        "ShopRegion": shop.get("SHOPREGION"),
        "ShopName": shop.get("SHOPNAME", ""),
        "ShopCode": shop.get("SHOPCODE", ""),
        "BusinessDate": _format_datetime_iso(shop.get("BUSINESS_DATE")),
        "BusinessEndDate": _format_datetime_iso(shop.get("BUSINESS_ENDDATE")),
        "BusinessType": shop.get("BUSINESS_TYPE"),
        "BusinessState": shop.get("BUSINESS_STATE"),
    }


def _format_date_chinese(dt) -> str:
    """日期格式化为中文格式（如：2015年9月2日）"""
    if dt is None:
        return ""
    try:
        from datetime import datetime
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt.replace("T", " "))
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except Exception:
        return str(dt) if dt else ""


def _format_datetime(dt) -> str:
    """日期时间格式化（如：2026/3/6 0:00:00）"""
    if dt is None:
        return ""
    try:
        from datetime import datetime
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt.replace("T", " "))
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute}:{dt.second}"
    except Exception:
        return str(dt) if dt else ""


def _format_datetime_iso(dt) -> str:
    """日期时间格式化为 ISO 格式（如：2015-09-02T00:00:00）"""
    if dt is None:
        return None
    try:
        from datetime import datetime
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    except Exception:
        return str(dt) if dt else None


def server_part_shop_new_save_state(db: DatabaseHelper, model: dict, user_id: int = None) -> tuple:
    """
    设置门店经营状态（业主端使用）
    对应原 ServerpartShopHelper.ServerPartShopNewSaveState

    逻辑：
    1. 校验经营状态只能是 1000/2000/3000
    2. 获取门店详情
    3. 构建 SERVERPARTSHOPModel（使用详情中的信息 + 新状态）
    4. 调用 synchro_serverpartshop 执行保存

    返回: (成功标志, 消息)
    """
    from datetime import datetime

    server_part_shop_id = model.get("ServerPartShopId")
    business_state = model.get("BusinessState")

    # 校验
    if server_part_shop_id is None:
        return False, "门店内码不能为空"

    valid_states = [1000, 2000, 3000]
    if business_state not in valid_states:
        return False, f"经营状态值无效，仅支持: {valid_states}"

    # 获取门店详情
    detail_sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {server_part_shop_id}"
    rows = db.execute_query(detail_sql)
    if not rows:
        return False, "门店不存在"

    shop = rows[0]

    # 构建更新模型
    shop["BUSINESS_STATE"] = business_state
    if user_id:
        shop["STAFF_ID"] = user_id
    shop["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 调用已有的同步方法
    success, _ = synchro_serverpartshop(db, shop)
    return success, "操作成功" if success else "操作失败"


def synchro_server_part_shop_new(db: DatabaseHelper, model: dict) -> bool:
    """
    同步门店（业主端使用，支持 ShopBusinessStateList 批量更新）
    对应原 ServerpartShopHelper.SynchroServerPartShopNew

    逻辑：
    1. 获取 ServerPartShop 基础信息
    2. 遍历 ShopBusinessStateList
    3. 对每个门店合并基础信息 + 经营状态信息
    4. 调用 synchro_serverpartshop 执行保存

    返回: 是否成功
    """
    from datetime import datetime

    server_part_shop = model.get("ServerPartShop", {})
    shop_business_state_list = model.get("ShopBusinessStateList", [])

    if not shop_business_state_list:
        # 若无 ShopBusinessStateList，直接同步 ServerPartShop
        if server_part_shop:
            success, _ = synchro_serverpartshop(db, server_part_shop)
            return success
        return False

    # 遍历 ShopBusinessStateList
    all_success = True
    for state_item in shop_business_state_list:
        # 合并基础信息和经营状态信息
        shop_model = {}

        # PascalCase → UPPER_CASE 映射
        field_map = {
            "ServerPartShopId": "SERVERPARTSHOP_ID",
            "ServerPartId": "SERVERPART_ID",
            "ServerPartName": "SERVERPART_NAME",
            "ServerPartCode": "SERVERPART_CODE",
            "SellerId": "SELLER_ID",
            "SellerName": "SELLER_NAME",
            "BusinessBrand": "BUSINESS_BRAND",
            "TopPerson": "TOPPERSON",
            "TopPersonMobile": "TOPPERSON_MOBILE",
            "LinkMan": "LINKMAN",
            "LinkManMobile": "LINKMAN_MOBILE",
            "ShopTrade": "SHOPTRADE",
            "BusinessTrade": "BUSINESS_TRADE",
            "BrandName": "BRAND_NAME",
            "ShopShortName": "SHOPSHORTNAME",
            "ServerPartShopDesc": "SERVERPARTSHOP_DESC",
            "IsValid": "ISVALID",
            "SaleCountLimit": "SALECOUNT_LIMIT",
            "SaleAmountLimit": "SALEAMOUNT_LIMIT",
            "RecordDiscount": "RECORD_DISCOUNT",
            "BusinessRegion": "BUSINESS_REGION",
            "ShopRegion": "SHOPREGION",
            "ShopName": "SHOPNAME",
            "ShopCode": "SHOPCODE",
            "BusinessDate": "BUSINESS_DATE",
            "BusinessEndDate": "BUSINESS_ENDDATE",
            "BusinessType": "BUSINESS_TYPE",
            "BusinessState": "BUSINESS_STATE",
        }

        for pascal_key, upper_key in field_map.items():
            val = state_item.get(pascal_key)
            if val is not None:
                shop_model[upper_key] = val

        # 从基础信息补充字段
        for key, value in server_part_shop.items():
            if key not in shop_model and value is not None:
                shop_model[key] = value

        # 设置操作时间
        shop_model["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        success, _ = synchro_serverpartshop(db, shop_model)
        if not success:
            all_success = False

    return all_success
