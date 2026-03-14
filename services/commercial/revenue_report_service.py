# -*- coding: utf-8 -*-
"""
CommercialApi - 经营报表 Service
从 revenue_router.py 中抽取:
  GetRevenueReport       — 服务区经营报表（片区占比计算）
  GetRevenueReportDetil  — 报表详情（南北区名称+品牌Logo+门店明细）
  GetCompanyRevenueReport — 子公司树形结构（驿达/驿佳/百和公司分组）
"""
from __future__ import annotations
from datetime import datetime as dt
from decimal import Decimal
from collections import defaultdict

from core.database import DatabaseHelper
from services.commercial.service_utils import safe_float as _sf, safe_int as _si
from services.commercial.service_utils import get_province_id
from routers.deps import parse_multi_ids, build_in_condition


# ===================================================================
# 1. GetRevenueReport — 服务区经营报表
# ===================================================================

def get_revenue_report(db: DatabaseHelper, province_code: str,
                       start_time: str | None, end_time: str | None) -> dict | None:
    """获取服务区经营报表（按片区分组，计算营收占比）

    Args:
        db: 数据库连接
        province_code: 省份编码
        start_time: 开始时间
        end_time: 结束时间

    Returns:
        dict: 包含总营收、片区列表等信息的字典，无数据返回 None
    """
    # 获取省份对应的 FieldEnum_ID
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
            AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    if not fe_rows:
        return None
    province_id = fe_rows[0]["FIELDENUM_ID"]

    # --- SQL 参数化: 经营报表 WHERE 条件 ---
    where_parts = [
        'A."SERVERPART_ID" = B."SERVERPART_ID"',
        'A."REVENUEDAILY_STATE" = 1',
        'B."STATISTIC_TYPE" = 1000',
        'B."STATISTICS_TYPE" = 1000',
        'B."PROVINCE_CODE" = :province_id',
    ]
    rpt_params = {"province_id": province_id}
    if start_time:
        sd = dt.strptime(start_time, "%Y-%m-%d").strftime("%Y%m%d") if "-" in start_time else start_time
        where_parts.append('A."STATISTICS_DATE" >= :sd')
        rpt_params["sd"] = sd
    if end_time:
        ed = dt.strptime(end_time, "%Y-%m-%d").strftime("%Y%m%d") if "-" in end_time else end_time
        where_parts.append('A."STATISTICS_DATE" <= :ed')
        rpt_params["ed"] = ed

    where_sql = " AND ".join(where_parts)

    sql = f"""SELECT B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX",
            B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX",
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAY_AMOUNT",
            SUM(A."CASHPAY_AMOUNT") AS "CASHPAY_AMOUNT",
            SUM(A."OTHERPAY_AMOUNT") AS "OTHERPAY_AMOUNT",
            SUM(A."TICKET_COUNT") AS "TICKET_COUNT",
            SUM(A."TOTAL_COUNT") AS "TOTAL_COUNT",
            SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFF_AMOUNT",
            SUM(NVL(A."DIFFERENT_AMOUNT_LESS_A",0) + NVL(A."DIFFERENT_AMOUNT_LESS_B",0)) AS "DIFFERENT_PRICE_LESS",
            SUM(NVL(A."DIFFERENT_AMOUNT_MORE_A",0) + NVL(A."DIFFERENT_AMOUNT_MORE_B",0)) AS "DIFFERENT_PRICE_MORE",
            SUM(A."REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",
            SUM(A."REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE {where_sql}
        GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX",
            B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX"
        ORDER BY B."SPREGIONTYPE_INDEX", B."SPREGIONTYPE_ID", B."SERVERPART_INDEX", B."SERVERPART_CODE" """

    rows = db.execute_query(sql, rpt_params)
    if not rows:
        return None

    # 汇总总营收
    total_revenue = round(sum(_sf(r.get("REVENUE_AMOUNT")) for r in rows), 2)
    total_ticket = sum(int(r.get("TICKET_COUNT") or 0) for r in rows)
    total_count = round(sum(_sf(r.get("TOTAL_COUNT")) for r in rows), 2)
    total_off = round(sum(_sf(r.get("TOTALOFF_AMOUNT")) for r in rows), 2)
    # 短款/长款
    diff_less = round(sum(_sf(r.get("DIFFERENT_PRICE_LESS")) for r in rows), 2)
    diff_more = round(sum(_sf(r.get("DIFFERENT_PRICE_MORE")) for r in rows), 2)
    # 南北区
    rev_amount_s = round(sum(_sf(r.get("REVENUE_AMOUNT_A")) for r in rows), 2)
    rev_amount_n = round(sum(_sf(r.get("REVENUE_AMOUNT_B")) for r in rows), 2)

    # 按片区分组
    region_map: dict[str, dict] = {}
    for r in rows:
        rid = r.get("SPREGIONTYPE_ID") or "null"
        if rid not in region_map:
            region_map[rid] = {
                "Region_Name": r.get("SPREGIONTYPE_NAME") or "无管理中心",
                "Total_Revenue": Decimal('0'),
                "Revenue_Proportion": "",
                "revenueServerModels": [],
            }
        region_map[rid]["Total_Revenue"] += Decimal(str(_sf(r.get("REVENUE_AMOUNT"))))

        # 添加服务区
        sp_revenue = _sf(r.get("REVENUE_AMOUNT"))
        region_rev = float(region_map[rid]["Total_Revenue"])
        prop = f"{sp_revenue / region_rev * 100:.2f}%" if region_rev != 0 else ""
        region_map[rid]["revenueServerModels"].append({
            "Serverpart_Id": str(r.get("SERVERPART_ID", "")),
            "Serverpart_Name": r.get("SERVERPART_NAME", ""),
            "Total_Revenue": sp_revenue,
            "Province_Code": province_code,
            "Revenue_Proportion": prop,
        })

    # 重新计算片区占比和服务区占比
    region_list = []
    for rid, region in region_map.items():
        region["Revenue_Proportion"] = (
            f"{float(region['Total_Revenue']) / total_revenue * 100:.2f}%"
            if total_revenue != 0 else ""
        )
        for sp in region["revenueServerModels"]:
            sp["Revenue_Proportion"] = (
                f"{sp['Total_Revenue'] / float(region['Total_Revenue']) * 100:.2f}%"
                if region['Total_Revenue'] != 0 else ""
            )
        # 按营收倒序排列服务区
        region["revenueServerModels"].sort(key=lambda x: x["Total_Revenue"], reverse=True)
        region["Total_Revenue"] = float(region["Total_Revenue"])
        region_list.append(region)
    # 按营收倒序排列片区
    region_list.sort(key=lambda x: x["Total_Revenue"], reverse=True)

    return {
        "Total_Revenue": total_revenue,
        "TicketCount": total_ticket,
        "TotalCount": total_count,
        "TotalOffAmount": total_off,
        "Different_Price_Less": diff_less,
        "Different_Price_More": diff_more,
        "MobilePayment": None,
        "Province_InsideAmount": total_revenue,
        "Province_ExternalAmount": 0.0,
        "Revenue_AmountN": rev_amount_n,
        "Revenue_AmountS": rev_amount_s,
        "SearchResult": None,
        "revenueRegionModels": region_list,
        "revenueInsideRegionModels": None,
    }


# ===================================================================
# 2. GetRevenueReportDetil — 服务区经营报表详情
# ===================================================================

def get_revenue_report_detail(db: DatabaseHelper, province_code: str,
                              serverpart_id: int | None,
                              start_time: str | None, end_time: str | None) -> dict | None:
    """获取服务区经营报表详情（南北区名称+品牌Logo+门店明细）

    Args:
        db: 数据库连接
        province_code: 省份编码
        serverpart_id: 服务区内码
        start_time: 开始时间
        end_time: 结束时间

    Returns:
        dict | None: 报表详情数据
    """
    if not serverpart_id:
        return None

    # 日期格式化
    start_str = (dt.strptime(start_time.split(' ')[0], '%Y-%m-%d').strftime('%Y%m%d')
                 if start_time and '-' in start_time else start_time)
    end_str = (dt.strptime(end_time.split(' ')[0], '%Y-%m-%d').strftime('%Y%m%d')
               if end_time and '-' in end_time else end_time)

    # --- SQL 参数化: 报表详情 WHERE 条件 ---
    where_sql = ''
    detail_params = {"sp_id": serverpart_id}
    if start_str:
        where_sql += ' AND A."STATISTICS_DATE" >= :start_str'
        detail_params["start_str"] = start_str
    if end_str:
        where_sql += ' AND A."STATISTICS_DATE" <= :end_str'
        detail_params["end_str"] = end_str

    # 按 SHOPTRADE 分组查询
    sql = f"""SELECT B."SERVERPART_ID",B."SERVERPART_NAME",B."SERVERPART_CODE",B."SERVERPART_INDEX",
            A."SHOPTRADE",
            SUM(A."REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",SUM(A."REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B",
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM(A."TICKET_COUNT") AS "TICKET_COUNT",SUM(A."TOTAL_COUNT") AS "TOTAL_COUNT",
            SUM(A."OTHERPAY_AMOUNT_A") AS "OTHERPAY_AMOUNT_A",SUM(A."OTHERPAY_AMOUNT_B") AS "OTHERPAY_AMOUNT_B",
            SUM(A."OTHERPAY_AMOUNT") AS "OTHERPAY_AMOUNT"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
            AND A."SERVERPART_ID" = :sp_id{where_sql}
        GROUP BY B."SERVERPART_ID",B."SERVERPART_NAME",B."SERVERPART_CODE",B."SERVERPART_INDEX",A."SHOPTRADE" """
    rows = db.execute_query(sql, detail_params) or []
    if not rows:
        return None

    # 查询该服务区所有门店
    # --- SQL 参数化: 门店查询 ---
    dt_shop = db.execute_query(
        'SELECT * FROM "T_SERVERPARTSHOP" WHERE "SERVERPART_ID" = :sp_id AND "ISVALID" = 1',
        {"sp_id": serverpart_id}) or []

    # 获取区域名称（南区/东区 vs 北区/西区）
    s_name, n_name = _get_region_names(db, dt_shop)

    # 查询品牌信息
    # --- SQL 参数化: 品牌信息查询 ---
    dt_brand = db.execute_query(
        """SELECT "BRAND_ID","BRAND_INTRO" FROM "T_BRAND"
        WHERE "PROVINCE_CODE" = :pc AND "BRAND_CATEGORY" = 1000""",
        {"pc": province_code}) or []
    brand_map = {}
    for br in dt_brand:
        bid = str(br.get("BRAND_ID", ""))
        brand_map[bid] = br.get("BRAND_INTRO", "")

    # 门店 Map（按 SHOPTRADE）
    shop_by_trade: dict[str, dict] = {}
    for s in dt_shop:
        st = str(s.get("SHOPTRADE", ""))
        if st and st not in shop_by_trade:
            shop_by_trade[st] = s

    # 汇总
    total_rev_a = sum(_sf(r.get("REVENUE_AMOUNT_A")) for r in rows)
    total_rev_b = sum(_sf(r.get("REVENUE_AMOUNT_B")) for r in rows)
    total_rev = sum(_sf(r.get("REVENUE_AMOUNT")) for r in rows)
    sp_name = rows[0].get("SERVERPART_NAME", "") if rows else ""

    # 四川省去掉大巴券和会员消费
    if province_code == "510000":
        total_rev_a -= sum(_sf(r.get("OTHERPAY_AMOUNT_A")) for r in rows)
        total_rev_b -= sum(_sf(r.get("OTHERPAY_AMOUNT_B")) for r in rows)
        total_rev -= sum(_sf(r.get("OTHERPAY_AMOUNT")) for r in rows)

    shop_list = []
    for r in rows:
        shoptrade = str(r.get("SHOPTRADE", "") or "")
        shop_info = shop_by_trade.get(shoptrade, {})

        # 门店名称 = SHOPSHORTNAME
        biz_name = shop_info.get("SHOPSHORTNAME", "") or ""
        # 上传类型 = TRANSFER_TYPE
        upload_type = _si(shop_info.get("TRANSFER_TYPE", 0))
        # 品牌 Logo
        biz_logo = ""
        biz_brand = str(shop_info.get("BUSINESS_BRAND", "") or "")
        if biz_brand and biz_brand in brand_map:
            intro = brand_map[biz_brand]
            if intro:
                biz_logo = intro
                if biz_logo.startswith("/"):
                    biz_logo = "https://user.eshangtech.com" + biz_logo

        rev_a = _sf(r.get("REVENUE_AMOUNT_A"))
        rev_b = _sf(r.get("REVENUE_AMOUNT_B"))
        biz_rev = _sf(r.get("REVENUE_AMOUNT"))

        if province_code == "510000":
            rev_a -= _sf(r.get("OTHERPAY_AMOUNT_A"))
            rev_b -= _sf(r.get("OTHERPAY_AMOUNT_B"))
            biz_rev -= _sf(r.get("OTHERPAY_AMOUNT"))

        shop_list.append({
            "BusinessType_Name": biz_name,
            "BusinessType_Revenue": biz_rev,
            "BusinessType_Logo": biz_logo if biz_logo else None,
            "Serverpart_S": s_name,
            "Serverpart_RevenueS": rev_a,
            "Serverpart_N": n_name,
            "Serverpart_RevenueN": rev_b,
            "Upload_Type": upload_type,
        })

    # 按营收降序排序
    shop_list.sort(key=lambda x: x.get("BusinessType_Revenue", 0), reverse=True)

    return {
        "Serverpart_Name": sp_name,
        "Serverpart_Revenue": total_rev,
        "Serverpart_S": s_name,
        "Serverpart_RevenueS": total_rev_a,
        "Serverpart_N": n_name,
        "Serverpart_RevenueN": total_rev_b,
        "ShopList": shop_list,
    }


def _get_region_names(db: DatabaseHelper, dt_shop: list) -> tuple[str, str]:
    """获取南/北区域名称（C# GetRegionName 逻辑）

    Args:
        db: 数据库连接
        dt_shop: 门店列表

    Returns:
        tuple[str, str]: (南区名称, 北区名称)
    """
    s_name = ""
    n_name = ""
    s_shops = [s for s in dt_shop if s.get("SHOPREGION") is not None and int(s.get("SHOPREGION", 99)) < 30]
    n_shops = [s for s in dt_shop if s.get("SHOPREGION") is not None and int(s.get("SHOPREGION", 0)) >= 30]
    if s_shops:
        s_region = str(sorted(s_shops, key=lambda x: int(x.get("SHOPREGION", 0)))[0].get("SHOPREGION"))
        # --- SQL 参数化: 区域名称查询 ---
        fe = db.execute_query(
            """SELECT B."FIELDENUM_NAME" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'SHOPREGION'
            AND B."FIELDENUM_VALUE" = :region_val""",
            {"region_val": s_region}) or []
        s_name = fe[0].get("FIELDENUM_NAME", "") if fe else ""
    if n_shops:
        n_region = str(sorted(n_shops, key=lambda x: int(x.get("SHOPREGION", 0)))[0].get("SHOPREGION"))
        fe = db.execute_query(
            """SELECT B."FIELDENUM_NAME" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'SHOPREGION'
            AND B."FIELDENUM_VALUE" = :region_val""",
            {"region_val": n_region}) or []
        n_name = fe[0].get("FIELDENUM_NAME", "") if fe else ""
    return s_name, n_name


# ===================================================================
# 3. GetCompanyRevenueReport — 子公司经营数据报表
# ===================================================================

def get_company_revenue_report(db: DatabaseHelper, province_code: str,
                               start_time: str | None, end_time: str | None,
                               serverpart_id: str | None) -> list:
    """按照安徽驿达子公司运营的门店返回经营数据报表（树形结构）

    子公司归属判定优先级: 驿佳(-2846) > 百和(-2802) > 驿达

    Args:
        db: 数据库连接
        province_code: 省份编码
        start_time: 开始日期
        end_time: 结束日期
        serverpart_id: 服务区内码（可多个逗号分隔）

    Returns:
        list: 树形结构节点列表（公司→业态/分类→片区→服务区）
    """
    # 1. 查省份 FIELDENUM_ID
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
            AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    if not fe_rows:
        return []
    province_id = fe_rows[0]["FIELDENUM_ID"]

    # 2. 构建 WHERE 条件
    # --- SQL 参数化: 子公司报表动态 WHERE ---
    where_sql = ' AND B."PROVINCE_CODE" = :province_id'
    co_params = {"province_id": province_id}
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        # f-string: 安全 — build_in_condition 已通过 int() 转换
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace(
            '"SERVERPART_ID"', 'B."SERVERPART_ID"')
    else:
        where_sql += (' AND B."STATISTIC_TYPE" = 1000 AND B."STATISTICS_TYPE" = 1000'
                      ' AND B."PROVINCE_CODE" = :province_id')
    if start_time:
        sd = dt.strptime(start_time, "%Y-%m-%d").strftime("%Y%m%d") if "-" in start_time else start_time
        where_sql += ' AND A."STATISTICS_DATE" >= :sd'
        co_params["sd"] = sd
    if end_time:
        ed = dt.strptime(end_time, "%Y-%m-%d").strftime("%Y%m%d") if "-" in end_time else end_time
        where_sql += ' AND A."STATISTICS_DATE" <= :ed'
        co_params["ed"] = ed

    # 3. 查询营收数据
    sql = f"""SELECT
            B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX", B."STATISTICS_TYPE",
            B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX",
            A."SERVERPARTSHOP_ID", A."BUSINESS_TYPE", A."SHOPTRADE",
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT", SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAY_AMOUNT",
            SUM(A."CASHPAY_AMOUNT") AS "CASHPAY_AMOUNT", SUM(A."OTHERPAY_AMOUNT") AS "OTHERPAY_AMOUNT",
            SUM(A."TICKET_COUNT") AS "TICKET_COUNT", SUM(A."TOTAL_COUNT") AS "TOTAL_COUNT",
            SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFF_AMOUNT", SUM(A."DIFFERENT_AMOUNT") AS "DIFFERENT_AMOUNT"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1{where_sql}
        GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX", B."STATISTICS_TYPE",
            B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX",
            A."SERVERPARTSHOP_ID", A."BUSINESS_TYPE", A."SHOPTRADE"
        ORDER BY B."SPREGIONTYPE_INDEX", B."SERVERPART_INDEX", A."SERVERPARTSHOP_ID" """
    rows = db.execute_query(sql, co_params)
    if not rows or not any(r.get("SERVERPARTSHOP_ID") for r in rows):
        return []

    # 4. 查门店信息
    shop_map = _load_shop_map(db, rows)

    # 5. 查业态
    # --- SQL 参数化: 业态查询 ---
    trade_rows = db.execute_query(
        """SELECT "AUTOSTATISTICS_ID","AUTOSTATISTICS_PID","AUTOSTATISTICS_NAME","AUTOSTATISTICS_INDEX"
        FROM "T_AUTOSTATISTICS" WHERE "PROVINCE_CODE" = :pc AND "AUTOSTATISTICS_STATE" > 0""",
        {"pc": province_code})
    trade_map = {}
    for t in (trade_rows or []):
        trade_map[str(t["AUTOSTATISTICS_ID"])] = t["AUTOSTATISTICS_NAME"]

    # 6. 查业务限制（T_RTBUSINESSLIMIT）
    push_limit = _load_push_limit(db, rows)

    # 7. 给每行标记归属公司
    processed = _classify_rows(rows, shop_map, push_limit, trade_map)

    # 8. 构建嵌套结果
    total_revenue = sum(p["RevenueAmount"] for p in processed)
    if total_revenue == 0:
        total_revenue = 1

    company_names = ["安徽驿达运营管理有限公司", "安徽驿佳商贸有限公司", "安徽百和餐饮有限公司"]
    result_list = []

    for company_name in company_names:
        company_items = [p for p in processed if p["MerchantsName"] == company_name]
        if not company_items:
            continue
        company_rev = round(sum(c["RevenueAmount"] for c in company_items), 2)
        company_node = {
            "node": _make_node(CompanyName=company_name, Total_Revenue=company_rev,
                               Revenue_Proportion=round(company_rev / total_revenue * 100, 2)),
            "children": []
        }

        if company_name == "安徽驿达运营管理有限公司":
            _build_yida_children(company_node, company_items, trade_rows, trade_map,
                                 total_revenue, company_name)
        elif company_name == "安徽驿佳商贸有限公司":
            _build_yijia_children(company_node, company_items, total_revenue, company_name)
        else:  # 百和餐饮
            _build_baihe_children(company_node, company_items, total_revenue, company_name)

        company_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
        if not company_node["children"]:
            company_node["children"] = [{"node": _make_node(), "children": []}]
        result_list.append(company_node)

    return result_list


# --------------- 以下为 GetCompanyRevenueReport 的内部辅助函数 ---------------

def _make_node(**kwargs) -> dict:
    """创建标准树节点（所有字段默认 None）"""
    base = {
        "CompanyId": 0, "CompanyName": None, "SPRegionType_Id": None, "SPRegionType_Name": None,
        "Serverpart_Id": None, "Serverpart_Name": None, "BusinessType_Name": None,
        "BusinessTrade_Id": None, "BusinessTrade_Name": None, "ServerpartShop_Id": None,
        "ShopShort_Name": None, "Total_Revenue": None, "Revenue_Proportion": None,
        "TicketCount": None, "TotalCount": None, "TotalOffAmount": None, "MobilePayment": None,
        "Different_Price_Less": None, "Different_Price_More": None,
    }
    base.update(kwargs)
    return base


def _load_shop_map(db: DatabaseHelper, rows: list) -> dict:
    """批量加载门店信息（SERVERPARTSHOP_ID 可能是逗号分隔的多个 ID）"""
    all_shop_ids: set[str] = set()
    for r in rows:
        sid = r.get("SERVERPARTSHOP_ID")
        if sid:
            for s in str(sid).split(","):
                s = s.strip()
                if s:
                    all_shop_ids.add(s)
    shop_map: dict[int, dict] = {}
    if all_shop_ids:
        id_list = list(all_shop_ids)
        chunk_size = 500
        for i in range(0, len(id_list), chunk_size):
            chunk = id_list[i:i + chunk_size]
            ids_in = ",".join(chunk)
            shop_rows = db.execute_query(
                f'SELECT * FROM "T_SERVERPARTSHOP" WHERE "SERVERPARTSHOP_ID" IN ({ids_in})')
            for s in (shop_rows or []):
                shop_map[s.get("SERVERPARTSHOP_ID")] = s
    return shop_map


def _load_push_limit(db: DatabaseHelper, rows: list) -> dict:
    """加载业务限制（T_RTBUSINESSLIMIT），返回 {shop_id: {limit_values}}"""
    all_shop_ids: set[str] = set()
    for r in rows:
        sid = r.get("SERVERPARTSHOP_ID")
        if sid:
            for s in str(sid).split(","):
                s = s.strip()
                if s:
                    all_shop_ids.add(s)
    push_limit: dict[int, set] = defaultdict(set)
    if all_shop_ids:
        ids_in = ",".join(list(all_shop_ids)[:1000])
        limit_rows = db.execute_query(
            f"""SELECT A."SERVERPARTSHOP_ID", R."DATA_VALUE"
            FROM "T_SERVERPARTSHOP" A, "T_RTBUSINESSLIMIT" R
            WHERE A."SERVERPARTSHOP_ID" = R."SERVERPARTSHOP_ID" AND R."DATA_TYPE" = 1030
                AND R."DATA_VALUE" IN (2010,2020,2030,2040,2050,2060)
                AND A."SERVERPARTSHOP_ID" IN ({ids_in})
            GROUP BY A."SERVERPARTSHOP_ID", R."DATA_VALUE" """)
        for lr in (limit_rows or []):
            push_limit[lr["SERVERPARTSHOP_ID"]].add(int(lr["DATA_VALUE"]))
    return push_limit


def _classify_rows(rows: list, shop_map: dict, push_limit: dict, trade_map: dict) -> list:
    """给每行数据标记归属公司（驿佳/百和/驿达）"""
    processed = []
    for r in rows:
        item = {
            "SPRegionTypeId": _si(r.get("SPREGIONTYPE_ID")),
            "SPRegionTypeName": str(r.get("SPREGIONTYPE_NAME") or ""),
            "SPRegionTypeIndex": _si(r.get("SPREGIONTYPE_INDEX")),
            "ServerpartId": _si(r.get("SERVERPART_ID")),
            "ServerpartName": str(r.get("SERVERPART_NAME") or ""),
            "ServerpartIndex": _si(r.get("SERVERPART_INDEX")),
            "ServerpartShopId": str(r.get("SERVERPARTSHOP_ID") or ""),
            "RevenueAmount": _sf(r.get("REVENUE_AMOUNT")),
            "BusinessTrade": 0, "BusinessTradeName": "",
            "BusinessBrand": 0, "BrandName": "",
            "ShopShortName": "", "MerchantsName": "",
        }
        shop_id_str = str(r.get("SERVERPARTSHOP_ID") or "")
        if not shop_id_str:
            if _si(r.get("TICKET_COUNT")) > 0:
                item["MerchantsName"] = "安徽驿达运营管理有限公司"
            processed.append(item)
            continue

        sub_ids = [s.strip() for s in shop_id_str.split(",") if s.strip()]
        exist_shops = [shop_map[int(sid)] for sid in sub_ids if int(sid) in shop_map]
        if not exist_shops:
            item["MerchantsName"] = "安徽驿达运营管理有限公司"
            processed.append(item)
            continue

        # 优先判定: 驿佳(-2846) > 百和(-2802) > 驿达
        yijia_shops = [s for s in exist_shops if _si(s.get("SELLER_ID")) == -2846]
        baihe_shops = [s for s in exist_shops if _si(s.get("SELLER_ID")) == -2802]
        if yijia_shops:
            shop = yijia_shops[0]
            item["MerchantsName"] = "安徽驿佳商贸有限公司"
            item["BusinessTrade"] = _si(shop.get("BUSINESS_TRADE"))
            item["BusinessBrand"] = _si(shop.get("BUSINESS_BRAND"))
            item["BrandName"] = str(shop.get("BRAND_NAME") or "")
            item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")
        elif baihe_shops:
            shop = baihe_shops[0]
            item["MerchantsName"] = "安徽百和餐饮有限公司"
            item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")
            # 查 pushLimit 确定 trade
            for sid in sub_ids:
                limits = push_limit.get(int(sid), set())
                if 2040 in limits:
                    item["BusinessTrade"] = 2040; item["BusinessTradeName"] = "咖啡"; break
                elif 2050 in limits:
                    item["BusinessTrade"] = 2050; item["BusinessTradeName"] = "老乡鸡"; break
                elif 2060 in limits:
                    item["BusinessTrade"] = 2060; item["BusinessTradeName"] = "肯德基"; break
            else:
                item["BusinessTrade"] = 2000; item["BusinessTradeName"] = "餐饮"
        else:
            shop = exist_shops[0]
            item["MerchantsName"] = "安徽驿达运营管理有限公司"
            bt = max((_si(s.get("BUSINESS_TRADE")) for s in exist_shops), default=0)
            item["BusinessTrade"] = bt
            item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")

        # 匹配业态名称
        trade_id = str(item["BusinessTrade"])
        if trade_id in trade_map and not item["BusinessTradeName"]:
            item["BusinessTradeName"] = trade_map[trade_id]

        item["ShopShort_Name"] = str(r.get("SERVERPART_NAME") or "") + item["ShopShortName"]
        processed.append(item)

    return processed


def _bind_sp_nodes(items: list, company_name: str, trade_id, trade_name: str,
                   total_revenue: float) -> list:
    """按片区→服务区分组构建子节点"""
    region_groups: dict[tuple, list] = defaultdict(list)
    for it in items:
        region_groups[(it["SPRegionTypeId"], it["SPRegionTypeName"], it["SPRegionTypeIndex"])].append(it)
    region_nodes = []
    for (rid, rname, rindex), sp_items in sorted(region_groups.items(), key=lambda x: (x[0][2], x[0][0])):
        rev = round(sum(s["RevenueAmount"] for s in sp_items), 2)
        region_node = {
            "node": _make_node(CompanyName=company_name, BusinessTrade_Id=trade_id,
                               BusinessTrade_Name=trade_name, SPRegionType_Id=rid,
                               SPRegionType_Name=rname, Total_Revenue=rev,
                               Revenue_Proportion=round(rev / total_revenue * 100, 2)),
            "children": []
        }
        server_groups: dict[tuple, list] = defaultdict(list)
        for s in sp_items:
            server_groups[(s["ServerpartId"], s["ServerpartName"], s["ServerpartIndex"])].append(s)
        for (sid, sname, sindex), s_items in sorted(server_groups.items(), key=lambda x: x[0][2]):
            srv = round(sum(x["RevenueAmount"] for x in s_items), 2)
            shop_ids_str = ",".join(
                dict.fromkeys(x["ServerpartShopId"] for x in s_items if x["ServerpartShopId"]))
            region_node["children"].append({
                "node": _make_node(CompanyName=company_name, BusinessTrade_Id=trade_id,
                                   BusinessTrade_Name=trade_name, SPRegionType_Id=rid,
                                   SPRegionType_Name=rname, Serverpart_Id=sid,
                                   Serverpart_Name=sname, ServerpartShop_Id=shop_ids_str or None,
                                   Total_Revenue=srv,
                                   Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                "children": None
            })
        region_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
        region_nodes.append(region_node)
    return region_nodes


def _build_yida_children(company_node: dict, company_items: list,
                         trade_rows: list | None, trade_map: dict,
                         total_revenue: float, company_name: str):
    """驿达：按业态父级分组"""
    parent_trades = [t for t in (trade_rows or []) if str(t.get("AUTOSTATISTICS_PID")) == "-1"]
    parent_trades.sort(key=lambda x: _si(x.get("AUTOSTATISTICS_INDEX")))
    for pt in parent_trades:
        pid = str(pt["AUTOSTATISTICS_ID"])
        child_ids = {str(t["AUTOSTATISTICS_ID"]) for t in (trade_rows or [])
                     if str(t.get("AUTOSTATISTICS_PID")) == pid or str(t["AUTOSTATISTICS_ID"]) == pid}
        trade_items = [c for c in company_items if str(c["BusinessTrade"]) in child_ids]
        if not trade_items:
            continue
        t_rev = round(sum(t["RevenueAmount"] for t in trade_items), 2)
        trade_node = {
            "node": _make_node(CompanyName=company_name,
                               BusinessTrade_Id=_sf(pt["AUTOSTATISTICS_ID"]),
                               BusinessTrade_Name=pt["AUTOSTATISTICS_NAME"],
                               Total_Revenue=t_rev,
                               Revenue_Proportion=round(t_rev / total_revenue * 100, 2)),
            "children": _bind_sp_nodes(trade_items, company_name,
                                       _sf(pt["AUTOSTATISTICS_ID"]), pt["AUTOSTATISTICS_NAME"],
                                       total_revenue)
        }
        trade_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
        company_node["children"].append(trade_node)

    # 其他（BusinessTrade=0 的）
    other_items = [c for c in company_items if c["BusinessTrade"] == 0]
    if other_items:
        o_rev = round(sum(o["RevenueAmount"] for o in other_items), 2)
        other_node = {
            "node": _make_node(CompanyName=company_name, BusinessTrade_Id=0,
                               BusinessTrade_Name="其他", Total_Revenue=o_rev,
                               Revenue_Proportion=round(o_rev / total_revenue * 100, 2)),
            "children": _bind_sp_nodes(other_items, company_name, 0, "其他", total_revenue)
        }
        other_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
        company_node["children"].append(other_node)


def _build_yijia_children(company_node: dict, company_items: list,
                          total_revenue: float, company_name: str):
    """驿佳：便利店 + 品牌分组"""
    store_items = company_items
    if store_items:
        s_rev = round(sum(s["RevenueAmount"] for s in store_items), 2)
        store_node = {
            "node": _make_node(CompanyName=company_name, BusinessTrade_Id=0.0,
                               BusinessTrade_Name="服务区便利店", Total_Revenue=s_rev,
                               Revenue_Proportion=round(s_rev / total_revenue * 100, 2)),
            "children": []
        }
        sg: dict[tuple, list] = defaultdict(list)
        for s in store_items:
            sg[(s["ServerpartId"], s["ServerpartName"], s.get("ShopShort_Name", ""))].append(s)
        for (sid, sname, ssn), items in sg.items():
            srv = round(sum(x["RevenueAmount"] for x in items), 2)
            store_node["children"].append({
                "node": _make_node(CompanyName=company_name, BusinessTrade_Name="服务区便利店",
                                   Serverpart_Id=sid, Serverpart_Name=sname,
                                   ShopShort_Name=ssn, Total_Revenue=srv,
                                   Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                "children": None
            })
        store_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
        company_node["children"].append(store_node)


def _build_baihe_children(company_node: dict, company_items: list,
                          total_revenue: float, company_name: str):
    """百和餐饮：按业态分组"""
    trade_groups: dict[tuple, list] = defaultdict(list)
    for c in company_items:
        trade_groups[(c["BusinessTrade"], c["BusinessTradeName"])].append(c)
    for (tid, tname), items in trade_groups.items():
        t_rev = round(sum(t["RevenueAmount"] for t in items), 2)
        trade_node = {
            "node": _make_node(CompanyName=company_name, BusinessTrade_Id=_sf(tid),
                               BusinessTrade_Name=tname, Total_Revenue=t_rev,
                               Revenue_Proportion=round(t_rev / total_revenue * 100, 2)),
            "children": []
        }
        sg: dict[tuple, list] = defaultdict(list)
        for t in items:
            sg[(t["ServerpartId"], t["ServerpartName"], t.get("ShopShort_Name", ""))].append(t)
        for (sid, sname, ssn), s_items in sg.items():
            srv = round(sum(x["RevenueAmount"] for x in s_items), 2)
            trade_node["children"].append({
                "node": _make_node(CompanyName=company_name, BusinessTrade_Id=_sf(tid),
                                   BusinessTrade_Name=tname, Serverpart_Id=sid,
                                   Serverpart_Name=sname, ShopShort_Name=ssn,
                                   Total_Revenue=srv,
                                   Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                "children": None
            })
        trade_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
        company_node["children"].append(trade_node)
