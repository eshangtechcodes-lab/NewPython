from __future__ import annotations
# -*- coding: utf-8 -*-
"""
品牌表业务服务
替代原 BRANDHelper.cs，保持相同的业务逻辑
对应 BaseInfoController 中 Brand 相关 6 个接口
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_BRAND"
PRIMARY_KEY = "BRAND_ID"

# Synchro 时需排除的字段（非数据库字段，仅展示用）
EXCLUDE_FIELDS = {
    "BUSINESSTRADE_NAME", "SPREGIONTYPE_IDS", "SERVERPART_IDS",
    "MerchantID", "MerchantID_Encrypt", "MerchantName", "ServerpartList",
    "RN",
}


def _build_where_sql(search_param: dict, query_type: int = 0,
                     exclude_keys: set = None) -> str:
    """
    根据查询参数构建 WHERE 条件
    query_type: 0=模糊查询, 1=精确查询
    exclude_keys: 需要排除的字段名（由业务层特殊处理）
    """
    if exclude_keys is None:
        exclude_keys = set()
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS or key in exclude_keys:

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


# ========== 1. GetBrandList ==========

def get_brand_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取品牌表列表
    对应原 BRANDHelper.GetBRANDList（L40-210）
    返回: (总数, 数据列表)
    """
    where_sql = ""
    # 需要特殊处理的字段，不走通用 WHERE 构建
    special_keys = {"BRAND_INDUSTRY", "SPREGIONTYPE_IDS", "SERVERPART_IDS"}

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        # 通用条件构建
        where_clause = _build_where_sql(sp, search_model.QueryType or 0, special_keys)
        if where_clause:
            where_sql = " WHERE " + where_clause

        # 特殊处理：BRAND_INDUSTRY（经营业态，含子类型）
        brand_industry = sp.get("BRAND_INDUSTRY")
        if brand_industry is not None:
            # 查询子类型（递归获取所有子级业态 ID）
            industry_ids = _get_sub_type_ids(db, str(brand_industry))
            where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                f"BRAND_INDUSTRY IN ({industry_ids})"

        # 特殊处理：SPREGIONTYPE_IDS / SERVERPART_IDS（通过门店关联筛选品牌）
        sp_where = ""
        spregiontype_ids = sp.get("SPREGIONTYPE_IDS")
        serverpart_ids = sp.get("SERVERPART_IDS")
        if spregiontype_ids and str(spregiontype_ids).strip():
            sp_where += f" AND A.SPREGIONTYPE_ID IN ({spregiontype_ids})"
        if serverpart_ids and str(serverpart_ids).strip():
            sp_where += f" AND A.SERVERPART_ID IN ({serverpart_ids})"
        if sp_where:
            brand_ids_sql = f"""SELECT WM_CONCAT(DISTINCT BUSINESS_BRAND)
                FROM T_SERVERPART A, T_SERVERPARTSHOP B
                WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.ISVALID = 1
                    AND B.BUSINESS_BRAND IS NOT NULL
                    AND B.BUSINESS_STATE IN (1000,2000){sp_where}"""
            rows = db.execute_query(brand_ids_sql)
            if rows and rows[0] and list(rows[0].values())[0]:
                brand_id_list = list(rows[0].values())[0]
                where_sql += (" WHERE " if where_sql == "" else " AND ") + \
                    f"BRAND_ID IN ({brand_id_list})"
            else:
                where_sql += (" WHERE " if where_sql == "" else " AND ") + "1 = 2"

    # 判断是否为商城品牌分支（BRAND_CATEGORY=2000 走 SQL 级分页）
    brand_category = None
    if search_model.SearchParameter:
        brand_category = search_model.SearchParameter.get("BRAND_CATEGORY")

    if brand_category == 2000:
        # 商城品牌：SQL 级关键字过滤 + 分页
        keyword_filter = _build_keyword_sql(search_model)
        if keyword_filter:
            where_sql += (" WHERE " if where_sql == "" else " AND ") + f"({keyword_filter})"
        if search_model.SortStr:
            where_sql += f" ORDER BY {search_model.SortStr}"

        # 查询总数
        count_sql = f"SELECT COUNT(1) FROM {TABLE_NAME}{where_sql}"
        total_count = db.execute_scalar(count_sql) or 0

        # 分页查询
        page_index = search_model.PageIndex or 1
        page_size = search_model.PageSize or 10
        end_row = page_index * page_size
        start_row = (page_index - 1) * page_size
        paged_sql = f"""SELECT * FROM (SELECT A.*, ROWNUM AS RN FROM (
            SELECT * FROM {TABLE_NAME}{where_sql}) A WHERE ROWNUM <= {end_row}) WHERE RN > {start_row}"""
        rows = db.execute_query(paged_sql)
        for row in rows:
            row.pop("RN", None)
    else:
        # 经营品牌：先查全量，Python 侧过滤 + 分页
        base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
        rows = db.execute_query(base_sql)

        # 关键字过滤（DataView.RowFilter 模拟）
        keyword_filter = _build_keyword_sql(search_model)
        if keyword_filter:
            rows = [r for r in rows if _match_keyword(r, search_model)]

        # 排序
        if search_model.SortStr:
            sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").strip()
            is_desc = "DESC" in (search_model.SortStr or "").upper()
            rows.sort(key=lambda x: x.get(sort_field, 0) or 0, reverse=is_desc)

        # 总数
        total_count = len(rows)

        # 分页
        page_index = search_model.PageIndex or 0
        page_size = search_model.PageSize or 0
        if page_index > 0 and page_size > 0:
            start = (page_index - 1) * page_size
            rows = rows[start:start + page_size]
        elif len(rows) > 10:
            rows = rows[:10]  # 默认返回前 10 条

    # 关联查询：经营业态名称、商户、服务区
    if rows:
        rows = _enrich_brand_list(db, rows)
        # 最终排序：按关联服务区数量降序
        rows.sort(key=lambda x: len(x.get("ServerpartList", [])), reverse=True)

    return int(total_count), rows


# ========== 2. GetCombineBrandList ==========

def get_combine_brand_list(db: DatabaseHelper, province_code: int,
                           spregiontype_ids: str = "", serverpart_ids: str = "",
                           brand_industry: str = "", brand_type: str = "",
                           brand_state: str = "", brand_name: str = "") -> tuple[list[dict], list[dict]]:
    """
    获取组合品牌列表
    对应原 BRANDHelper.GetCombineBrandList（L224-738）
    返回: (组合品牌列表, 历史经营项目列表)

    注意：此接口极复杂，涉及跨 4 个 schema 查询。
    当前实现核心数据分组逻辑，营收分润部分依赖 CONTRACT_STORAGE 和 PLATFORM_DASHBOARD 表。
    """
    his_project_list = []

    # 构建品牌查询条件
    where_sql = f" AND PROVINCE_CODE = {province_code}"

    if brand_industry and brand_industry.strip():
        industry_ids = _get_sub_type_ids(db, brand_industry)
        where_sql += f" AND BRAND_INDUSTRY IN ({industry_ids})"
    if brand_type and brand_type.strip():
        where_sql += f" AND BRAND_TYPE IN ({brand_type})"
    if brand_state and brand_state.strip():
        where_sql += f" AND BRAND_STATE IN ({brand_state})"

    # 通过门店关联筛选品牌
    sp_where = ""
    if spregiontype_ids and spregiontype_ids.strip():
        sp_where += f" AND A.SPREGIONTYPE_ID IN ({spregiontype_ids})"
    if serverpart_ids and serverpart_ids.strip():
        sp_where += f" AND A.SERVERPART_ID IN ({serverpart_ids})"
    if sp_where:
        brand_ids_sql = f"""SELECT WM_CONCAT(DISTINCT BUSINESS_BRAND)
            FROM T_SERVERPART A, T_SERVERPARTSHOP B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.ISVALID = 1
                AND B.BUSINESS_BRAND IS NOT NULL{sp_where}"""
        rows = db.execute_query(brand_ids_sql)
        if rows and rows[0] and list(rows[0].values())[0]:
            brand_id_list = list(rows[0].values())[0]
            where_sql += f" AND BRAND_ID IN ({brand_id_list})"
        else:
            return [], []

    # 查询品牌数据（只查 BRAND_CATEGORY=1000 经营品牌）
    brand_sql = f"SELECT * FROM {TABLE_NAME} WHERE BRAND_CATEGORY = 1000{where_sql}"
    brand_rows = db.execute_query(brand_sql)

    # 品牌名称模糊过滤
    if brand_name and brand_name.strip():
        brand_rows = [r for r in brand_rows if brand_name in (r.get("BRAND_NAME") or "")]

    if not brand_rows:
        return [], []

    # 按 WECHATAPPSIGN_ID 分组（组合品牌）
    groups = {}
    for row in brand_rows:
        wechat_id = row.get("WECHATAPPSIGN_ID")
        if wechat_id not in groups:
            groups[wechat_id] = []
        groups[wechat_id].append(row)

    # 查询全部品牌数据（用于聚合 BRAND_INDUSTRY/BRAND_TYPE）
    total_sql = f"""SELECT * FROM {TABLE_NAME}
        WHERE PROVINCE_CODE = {province_code}"""
    if brand_state and brand_state.strip():
        total_sql += f" AND BRAND_STATE = {brand_state}"
    total_brands = db.execute_query(total_sql)
    total_by_wechat = {}
    for tb in total_brands:
        wid = tb.get("WECHATAPPSIGN_ID")
        if wid not in total_by_wechat:
            total_by_wechat[wid] = []
        total_by_wechat[wid].append(tb)

    # 查询经营业态数据源
    trade_rows = db.execute_query(
        f"SELECT * FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000 AND PROVINCE_CODE = {province_code}")
    trade_map = {r.get("AUTOSTATISTICS_ID"): r.get("AUTOSTATISTICS_NAME") for r in trade_rows}

    # 查询商户数据
    merchant_sql = """SELECT A.COOPMERCHANTS_ID, A.COOPMERCHANTS_NAME, B.BUSINESS_BRAND
        FROM T_COOPMERCHANTS A, T_RTCOOPMERCHANTS B
        WHERE A.COOPMERCHANTS_ID = B.COOPMERCHANTS_ID AND A.COOPMERCHANTS_STATE = 1"""
    merchant_rows = db.execute_query(merchant_sql)
    merchant_by_brand = {}
    for mr in merchant_rows:
        bid = mr.get("BUSINESS_BRAND")
        if bid is not None:
            merchant_by_brand[bid] = mr

    # 查询服务区门店数据
    sp_filter = ""
    if serverpart_ids and serverpart_ids.strip():
        sp_filter = f" AND SERVERPART_ID IN ({serverpart_ids})"
    shop_sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME, BUSINESS_BRAND,
            WM_CONCAT(DISTINCT SHOPTRADE) AS SHOPTRADE,
            MIN(BUSINESS_TYPE) AS BUSINESS_TYPE,
            MIN(BUSINESS_STATE) AS BUSINESS_STATE
        FROM T_SERVERPARTSHOP
        WHERE ISVALID = 1 AND BUSINESS_BRAND IS NOT NULL
            AND SERVERPART_CODE NOT IN ('348888','538888'){sp_filter}
        GROUP BY SERVERPART_ID, SERVERPART_NAME, BUSINESS_BRAND"""
    shop_rows = db.execute_query(shop_sql)
    shop_by_brand = {}
    for sr in shop_rows:
        bid = sr.get("BUSINESS_BRAND")
        if bid is not None:
            if bid not in shop_by_brand:
                shop_by_brand[bid] = []
            shop_by_brand[bid].append(sr)

    # 构建组合品牌列表
    combine_list = []
    for wechat_id, brand_group in groups.items():
        first = brand_group[0]
        # 聚合 BRAND_INDUSTRY 和 BRAND_TYPE
        total_group = total_by_wechat.get(wechat_id, brand_group)
        all_brand_ids = [str(b.get("BRAND_ID")) for b in total_group]
        all_industries = list(set(str(b.get("BRAND_INDUSTRY")) for b in total_group if b.get("BRAND_INDUSTRY")))
        all_types = list(set(str(b.get("BRAND_TYPE")) for b in total_group if b.get("BRAND_TYPE")))

        combine_item = {
            "WECHATAPPSIGN_ID": wechat_id,
            "WECHATAPPSIGN_NAME": ",".join(all_brand_ids),
            "BRAND_ID": first.get("BRAND_ID"),
            "BRAND_PID": first.get("BRAND_PID"),
            "BRAND_INDEX": first.get("BRAND_INDEX"),
            "BRAND_NAME": first.get("BRAND_NAME"),
            "BRAND_CATEGORY": first.get("BRAND_CATEGORY"),
            "BRAND_INTRO": first.get("BRAND_INTRO"),
            "OWNERUNIT_ID": first.get("OWNERUNIT_ID"),
            "OWNERUNIT_NAME": first.get("OWNERUNIT_NAME"),
            "PROVINCE_CODE": first.get("PROVINCE_CODE"),
            "STAFF_ID": first.get("STAFF_ID"),
            "STAFF_NAME": first.get("STAFF_NAME"),
            "OPERATE_DATE": first.get("OPERATE_DATE"),
            "BRAND_INDUSTRY": ",".join(all_industries),
            "BRAND_TYPE": ",".join(all_types),
            "BRAND_STATE": max((b.get("BRAND_STATE") or 0) for b in total_group),
            "BRAND_DESC": max((b.get("BRAND_DESC") or "") for b in total_group),
        }

        # 解析经营业态名称
        trade_names = [trade_map.get(int(i), "") for i in all_industries if i.isdigit() and int(i) in trade_map]
        combine_item["BUSINESSTRADE_NAME"] = ",".join(trade_names)

        # 绑定经营商户名称
        for bid_str in all_brand_ids:
            bid = int(bid_str) if bid_str.isdigit() else None
            if bid and bid in merchant_by_brand:
                combine_item["MerchantName"] = merchant_by_brand[bid].get("COOPMERCHANTS_NAME")
                break

        # 获取门店经营状态
        business_states = []
        for bid_str in all_brand_ids:
            bid = int(bid_str) if bid_str.isdigit() else None
            if bid and bid in shop_by_brand:
                for s in shop_by_brand[bid]:
                    business_states.append(s.get("BUSINESS_STATE") or 9999)
        combine_item["BusinessState"] = min(business_states) if business_states else None

        # 服务区列表
        if not (serverpart_ids and serverpart_ids.strip()):
            serverpart_list = []
            seen_sp = set()
            for bid_str in all_brand_ids:
                bid = int(bid_str) if bid_str.isdigit() else None
                if bid and bid in shop_by_brand:
                    for s in shop_by_brand[bid]:
                        sp_id = str(s.get("SERVERPART_ID"))
                        if sp_id not in seen_sp and (s.get("BUSINESS_STATE") or 0) == 1000:
                            seen_sp.add(sp_id)
                            serverpart_list.append({
                                "label": s.get("SERVERPART_NAME"),
                                "value": sp_id
                            })
            combine_item["ServerpartList"] = serverpart_list

        combine_list.append(combine_item)

    # 排序
    if serverpart_ids and serverpart_ids.strip():
        combine_list.sort(key=lambda x: x.get("REVENUE_DAILYAMOUNT") or 0, reverse=True)
    else:
        combine_list.sort(key=lambda x: len(x.get("ServerpartList", [])), reverse=True)

    return combine_list, his_project_list


# ========== 3. GetTradeBrandTree ==========

def get_trade_brand_tree(db: DatabaseHelper, business_trade_pid: int = -1,
                         province_code: int = None, ownerunit_id: int = None,
                         brand_state: int = None) -> list[dict]:
    """
    获取经营品牌树（嵌套结构：经营业态 → 品牌）
    对应原 BRANDHelper.GetNestingTradeBrandTree（L1113-1185）
    返回: 嵌套树列表
    """
    # 查询经营业态数据
    trade_where = "WHERE AUTOSTATISTICS_TYPE = 2000"
    if province_code is not None:
        trade_where += f" AND PROVINCE_CODE = {province_code}"
    if ownerunit_id is not None:
        trade_where += f" AND OWNERUNIT_ID = {ownerunit_id}"
    trade_rows = db.execute_query(f"SELECT * FROM T_AUTOSTATISTICS {trade_where}")

    # 查询品牌数据
    brand_where = ""
    if brand_state is not None:
        brand_where = f"WHERE BRAND_STATE = {brand_state}"
    brand_rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} {brand_where}")

    # 递归构建树
    tree = []
    _build_tree(business_trade_pid, trade_rows, brand_rows, tree)
    return tree


def _build_tree(parent_id: int, trade_rows: list, brand_rows: list, result: list):
    """递归构建经营业态-品牌树"""
    # 过滤当前级别的经营业态
    children = [t for t in trade_rows if (t.get("AUTOSTATISTICS_PID") or -1) == parent_id]
    children.sort(key=lambda x: (x.get("AUTOSTATISTICS_INDEX") or 0, x.get("AUTOSTATISTICS_ID") or 0))

    for trade in children:
        trade_id = trade.get("AUTOSTATISTICS_ID")
        node = {
            "node": {
                "BusinessTrade_Id": trade_id,
                "BusinessTrade_Name": trade.get("AUTOSTATISTICS_NAME"),
                "BusinessTrade_ICO": trade.get("AUTOSTATISTICS_ICO"),
                "BrandTreeList": _get_brands_for_trade(trade_id, brand_rows),
            },
            "children": []
        }
        # 递归子级
        _build_tree(trade_id, trade_rows, brand_rows, node["children"])
        result.append(node)


def _get_brands_for_trade(trade_id: int, brand_rows: list) -> list[dict]:
    """获取某经营业态下的品牌列表"""
    brands = []
    for b in brand_rows:
        if str(b.get("BRAND_INDUSTRY")) == str(trade_id) and b.get("BRAND_CATEGORY") == 1000:
            brands.append({
                "BRAND_ID": b.get("BRAND_ID"),
                "BRAND_NAME": b.get("BRAND_NAME"),
                "BRAND_INTRO": b.get("BRAND_INTRO"),
                "BRAND_STATE": b.get("BRAND_STATE"),
            })
    brands.sort(key=lambda x: (x.get("BRAND_INDEX") or 0, x.get("BRAND_ID") or 0))
    return brands


# ========== 4. GetBrandDetail ==========

def get_brand_detail(db: DatabaseHelper, brand_id: int) -> Optional[dict]:
    """
    获取品牌表明细
    对应原 BRANDHelper.GetBRANDDetail（L826-897）
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {brand_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None

    brand = rows[0]

    # 解析经营业态名称
    if brand.get("BRAND_INDUSTRY"):
        trade_sql = f"SELECT AUTOSTATISTICS_NAME FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_ID = {brand['BRAND_INDUSTRY']}"
        trade_rows = db.execute_query(trade_sql)
        if trade_rows:
            brand["BUSINESSTRADE_NAME"] = trade_rows[0].get("AUTOSTATISTICS_NAME")

    # 查询经营商户
    merchant_sql = f"""SELECT A.COOPMERCHANTS_ID, A.COOPMERCHANTS_NAME
        FROM T_COOPMERCHANTS A, T_RTCOOPMERCHANTS B
        WHERE A.COOPMERCHANTS_ID = B.COOPMERCHANTS_ID
            AND A.COOPMERCHANTS_STATE = 1 AND B.BUSINESS_BRAND = {brand_id}"""
    merchant_rows = db.execute_query(merchant_sql)
    if merchant_rows:
        brand["MerchantID"] = str(merchant_rows[0].get("COOPMERCHANTS_ID"))
        brand["MerchantName"] = merchant_rows[0].get("COOPMERCHANTS_NAME")

    # 查询关联服务区
    brand["ServerpartList"] = []
    shop_sql = f"""SELECT DISTINCT SERVERPART_ID, SERVERPART_NAME
        FROM T_SERVERPARTSHOP
        WHERE ISVALID = 1 AND BUSINESS_STATE = 1000
            AND BUSINESS_BRAND = {brand_id}"""
    shop_rows = db.execute_query(shop_sql)
    seen = set()
    for s in shop_rows:
        sp_id = str(s.get("SERVERPART_ID"))
        if sp_id not in seen:
            seen.add(sp_id)
            brand["ServerpartList"].append({
                "label": s.get("SERVERPART_NAME"),
                "value": sp_id
            })

    return brand


# ========== 5. SynchroBrand ==========

def synchro_brand(db: DatabaseHelper, brand_data: dict) -> tuple[bool, dict, str]:
    """
    同步品牌表（新增或更新）
    对应原 BRANDHelper.SynchroBRAND（L944-1006）
    返回: (是否成功, 数据对象, 失败原因)
    """
    brand_id = brand_data.get("BRAND_ID")

    # 验证经营业态是否为子级
    brand_industry = brand_data.get("BRAND_INDUSTRY")
    if brand_industry is not None:
        check_sql = f"SELECT COUNT(*) FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_PID = {brand_industry}"
        child_count = db.execute_scalar(check_sql) or 0
        if child_count > 0:
            return False, brand_data, "同步失败，请选择子级经营业态"

    # 默认操作时间
    if brand_data.get("OPERATE_DATE") is None:
        brand_data["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 过滤非数据库字段
    db_data = {k: v for k, v in brand_data.items() if k not in EXCLUDE_FIELDS}

    if brand_id is not None:
        # 更新模式
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {brand_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, brand_data, "更新失败，数据不存在"

        set_parts = []
        for key, value in db_data.items():
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
        # 新增模式（MAX+1 降级方案）
        try:
            new_id = db.execute_scalar("SELECT SEQ_BRAND.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        brand_data["BRAND_ID"] = new_id
        db_data["BRAND_ID"] = new_id

        columns = []
        values = []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, brand_data, ""


# ========== 6. DeleteBrand ==========

def delete_brand(db: DatabaseHelper, brand_id: int) -> bool:
    """
    删除品牌表（软删除，BRAND_STATE=0）
    对应原 BRANDHelper.DeleteBRAND（L1010-1026）
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {brand_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False
    sql = f"UPDATE {TABLE_NAME} SET BRAND_STATE = 0 WHERE {PRIMARY_KEY} = {brand_id}"
    db.execute_non_query(sql)
    return True


# ========== 辅助函数 ==========

def _get_sub_type_ids(db: DatabaseHelper, industry_id: str) -> str:
    """
    递归获取经营业态的子级 ID 列表（含自身）
    对应 AUTOSTATISTICS.GetSubType 递归查询
    """
    all_ids = set()
    if industry_id:
        for id_str in industry_id.split(","):
            id_str = id_str.strip()
            if id_str:
                all_ids.add(id_str)
    # 递归查子级
    to_check = list(all_ids)
    while to_check:
        current = to_check.pop(0)
        child_sql = f"SELECT AUTOSTATISTICS_ID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_PID = {current}"
        children = db.execute_query(child_sql)
        for c in children:
            cid = str(c.get("AUTOSTATISTICS_ID"))
            if cid not in all_ids:
                all_ids.add(cid)
                to_check.append(cid)
    return ",".join(all_ids) if all_ids else industry_id


def _build_keyword_sql(search_model: SearchModel) -> str:
    """构建关键字过滤 SQL 片段"""
    if not search_model.keyWord:
        return ""
    kw = search_model.keyWord
    if hasattr(kw, 'model_dump'):
        kw = kw.model_dump()
    if not kw.get("Key") or not kw.get("Value"):
        return ""
    keys = kw["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{kw['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


def _match_keyword(row: dict, search_model: SearchModel) -> bool:
    """Python 侧关键字匹配（模拟 DataView.RowFilter）"""
    if not search_model.keyWord:
        return True
    kw = search_model.keyWord
    if hasattr(kw, 'model_dump'):
        kw = kw.model_dump()
    if not kw.get("Key") or not kw.get("Value"):
        return True
    search_value = kw["Value"]
    for key in kw["Key"].split(","):
        key = key.strip()
        if key and search_value in str(row.get(key, "")):
            return True
    return False


def _enrich_brand_list(db: DatabaseHelper, rows: list[dict]) -> list[dict]:
    """
    为品牌列表补充关联数据：经营业态名称、商户、服务区
    对应原 GetBRANDList L144-206 的关联查询逻辑
    """
    # 查询商户数据
    merchant_sql = """SELECT A.COOPMERCHANTS_ID, A.COOPMERCHANTS_NAME, B.BUSINESS_BRAND
        FROM T_COOPMERCHANTS A, T_RTCOOPMERCHANTS B
        WHERE A.COOPMERCHANTS_ID = B.COOPMERCHANTS_ID AND A.COOPMERCHANTS_STATE = 1"""
    merchant_rows = db.execute_query(merchant_sql)
    merchant_map = {}
    for m in merchant_rows:
        bid = m.get("BUSINESS_BRAND")
        if bid is not None:
            merchant_map[bid] = m

    # 查询服务区门店数据
    shop_sql = """SELECT SERVERPART_ID, SERVERPART_NAME, BUSINESS_BRAND
        FROM T_SERVERPARTSHOP
        WHERE ISVALID = 1 AND BUSINESS_STATE IN (1000)
            AND SERVERPART_CODE NOT IN ('348888')
        GROUP BY SERVERPART_ID, SERVERPART_NAME, BUSINESS_BRAND"""
    shop_rows = db.execute_query(shop_sql)
    shop_by_brand = {}
    for s in shop_rows:
        bid = s.get("BUSINESS_BRAND")
        if bid is not None:
            if bid not in shop_by_brand:
                shop_by_brand[bid] = []
            shop_by_brand[bid].append(s)

    # 批量预加载经营业态（避免循环内逐条 SQL 导致 N+1 查询卡死）
    trade_sql = "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_NAME FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
    trade_rows = db.execute_query(trade_sql)
    trade_map = {r.get("AUTOSTATISTICS_ID"): r.get("AUTOSTATISTICS_NAME") for r in trade_rows}

    # 遍历品牌，补充关联数据
    for brand in rows:
        brand_id = brand.get("BRAND_ID")

        # 解析经营业态名称（从预加载 map 查找）
        industry = brand.get("BRAND_INDUSTRY")
        if industry:
            brand["BUSINESSTRADE_NAME"] = trade_map.get(industry, "")

        # 商户信息
        if brand_id in merchant_map:
            brand["MerchantID"] = str(merchant_map[brand_id].get("COOPMERCHANTS_ID"))
            brand["MerchantName"] = merchant_map[brand_id].get("COOPMERCHANTS_NAME")

        # 服务区列表
        brand["ServerpartList"] = []
        if brand_id in shop_by_brand:
            seen = set()
            for s in shop_by_brand[brand_id]:
                sp_id = str(s.get("SERVERPART_ID"))
                if sp_id not in seen:
                    seen.add(sp_id)
                    brand["ServerpartList"].append({
                        "label": s.get("SERVERPART_NAME"),
                        "value": sp_id
                    })

    return rows
