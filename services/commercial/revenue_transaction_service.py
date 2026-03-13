# -*- coding: utf-8 -*-
"""
CommercialApi - 交易分析 Service
从 revenue_router.py 中抽取:
  GetMobileShare, GetMallDeliver, GetTransactionAnalysis,
  GetTransactionTimeAnalysis, GetTransactionConvert,
  GetBusinessTradeRevenue, GetBusinessTradeLevel, GetBusinessBrandLevel
每个函数独立、可单独迁移

注意: 这些路由逻辑各 100-200 行, 且与 Router 参数格式紧耦合
      此处仅抽取核心查询+聚合逻辑, Router 层负责参数解析和 Result 包装
"""
from __future__ import annotations
from typing import Optional
from collections import defaultdict
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition
from services.commercial.service_utils import (
    safe_float as _sf, safe_int as _si,
    get_province_id as _get_province_id,
)


# ===== 1. GetMobileShare =====
def get_mobile_share(db: DatabaseHelper, province_code, statistics_start_date,
                      statistics_end_date, serverpart_id, sp_region_type_id) -> Optional[dict]:
    """获取移动支付分账数据"""
    from datetime import datetime as dt

    where_sql = ""
    if serverpart_id:
        where_sql += f' AND A."SERVERPART_ID" = {serverpart_id}'
    elif sp_region_type_id:
        where_sql += f' AND A."SERVERPART_ID" IN (SELECT "SERVERPART_ID" FROM "T_SERVERPART" WHERE "SPREGIONTYPE_ID" = {sp_region_type_id})'
    if province_code:
        where_sql += f' AND A."PROVINCE_CODE" = {province_code}'

    if statistics_start_date:
        sd = dt.strptime(statistics_start_date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in statistics_start_date else statistics_start_date
        where_sql += f' AND A."STATISTICS_DATE" >= {sd}'
    if statistics_end_date:
        ed = dt.strptime(statistics_end_date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in statistics_end_date else statistics_end_date
        where_sql += f' AND A."STATISTICS_DATE" <= {ed}'

    sql = f"""SELECT COUNT(DISTINCT "SERVERPARTSHOP_ID") AS "SHOP_COUNT",
            SUM("TICKET_PRICE") AS "TICKET_PRICE", SUM("TICKET_FEE") AS "TICKET_FEE",
            SUM("ROYALTY_PRICE") AS "ROYALTY_PRICE", SUM("SUBROYALTY_PRICE") AS "SUBROYALTY_PRICE",
            SUM("TICKET_PRICE" - "TICKET_FEE") AS "ACCOUNT_PRICE"
        FROM "T_MOBILEPAYSHARE" A WHERE A."MOBILEPAYSHARE_STATE" = 1{where_sql}"""
    rows = db.execute_query(sql) or []

    if not rows or not rows[0].get("SHOP_COUNT"):
        return None

    r = rows[0]
    return {
        "Statistics_Date": statistics_end_date,
        "Serverpart_ID": None, "Serverpart_Name": None,
        "ShareShop_Count": _si(r.get("SHOP_COUNT")),
        "Royalty_Price": _sf(r.get("ROYALTY_PRICE")),
        "SubRoyalty_Price": _sf(r.get("SUBROYALTY_PRICE")),
        "Ticket_Fee": _sf(r.get("TICKET_FEE")),
        "Ticket_Price": _sf(r.get("TICKET_PRICE")),
        "Account_Price": _sf(r.get("ACCOUNT_PRICE")),
        "ShareShopGrowth_Count": None, "RoyaltyGrowth_Price": None, "MonthRoyalty_Price": None,
    }


# ===== 2. GetMallDeliver =====
def get_mall_deliver(db: DatabaseHelper, province_code, statistics_start_date,
                      statistics_end_date) -> Optional[dict]:
    """获取商城配送数据"""
    if province_code != "340000":
        return None

    where_sql = ' AND A."SELLER_ID" = 9'
    date_sql = ""
    if statistics_start_date:
        date_sql += f" AND A.\"DELIVER_DATE\" >= TO_DATE('{statistics_start_date.split(' ')[0]}','YYYY-MM-DD')"
    if statistics_end_date:
        date_sql += f" AND A.\"DELIVER_DATE\" < TO_DATE('{statistics_end_date.split(' ')[0]}','YYYY-MM-DD') + 1"

    sql = f"""SELECT COUNT(DISTINCT A."GOODSDELIVER_ID") AS "DELIVERBILL_COUNT",
            SUM(B."DELIVER_PRICE") AS "DELIVER_PRICE"
        FROM "T_GOODSDELIVER" A, "T_GOODSDELIVERDETAIL" B
        WHERE A."DELIVER_STATE" > 0 AND A."DELIVER_STATE" < 9000
            AND A."GOODSDELIVER_ID" = B."GOODSDELIVER_ID"{where_sql}{date_sql}"""
    rows = db.execute_query(sql) or []
    r = rows[0] if rows else {}
    return {
        "Statistics_Date": statistics_end_date,
        "DeliverBill_Count": _si(r.get("DELIVERBILL_COUNT")),
        "Deliver_Price": _sf(r.get("DELIVER_PRICE")),
        "DeliverBillGrowth_Count": None, "DeliverGrowth_Price": None,
        "Deliver_Rate": None, "MonthDeliver_Price": None,
    }


# ===== 3. GetTransactionAnalysis =====
def get_transaction_analysis(db: DatabaseHelper, province_code, statistics_date,
                              serverpart_id) -> Optional[dict]:
    """获取服务区客单交易分析"""
    from datetime import datetime as dt

    if not statistics_date:
        return None

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    date_str = stat_date.strftime("%Y%m%d")
    month_start = stat_date.strftime("%Y%m01")
    sp_id = int(serverpart_id) if serverpart_id else None

    # 当日数据
    if sp_id:
        day_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A
            WHERE A."REVENUEDAILY_STATE" = 1 AND A."STATISTICS_DATE" = {date_str} AND A."SERVERPART_ID" = {sp_id}"""
    else:
        day_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A
            WHERE A."REVENUEDAILY_STATE" = 1 AND A."SERVERPART_ID" = 0 AND A."STATISTICS_DATE" = {date_str}"""
    day_rows = db.execute_query(day_sql) or []

    ticket_count = 0; total_count = 0.0; revenue_amount = 0.0; avg_ticket_price = None
    if day_rows and day_rows[0].get("TICKETCOUNT") is not None:
        ticket_count = _si(day_rows[0].get("TICKETCOUNT"))
        total_count = _sf(day_rows[0].get("TOTALCOUNT"))
        revenue_amount = _sf(day_rows[0].get("CASHPAY"))
        if ticket_count > 0: avg_ticket_price = round(revenue_amount / ticket_count, 2)

    # 月均数据
    province_id = _get_province_id(db, province_code) if province_code else None
    sp_filter = f'= {sp_id}' if sp_id else '> 0'
    prov_where = f' AND A."PROVINCE_ID" = {province_id}' if province_id else ''
    month_sql = f"""SELECT
            COUNT(DISTINCT CASE WHEN A."SERVERPART_ID" {sp_filter} THEN A."STATISTICS_DATE" END) AS "SP_DAYS",
            SUM(CASE WHEN A."SERVERPART_ID" {sp_filter} THEN A."TICKET_COUNT" ELSE 0 END) AS "SP_TICKET",
            SUM(CASE WHEN A."SERVERPART_ID" {sp_filter} THEN A."TOTAL_COUNT" ELSE 0 END) AS "SP_TOTAL",
            SUM(CASE WHEN A."SERVERPART_ID" {sp_filter} THEN A."REVENUE_AMOUNT" ELSE 0 END) AS "SP_REVENUE",
            COUNT(DISTINCT A."STATISTICS_DATE") AS "ALL_DAYS",
            SUM(A."TICKET_COUNT") AS "ALL_TICKET",
            SUM(A."TOTAL_COUNT") AS "ALL_TOTAL",
            SUM(A."REVENUE_AMOUNT") AS "ALL_REVENUE"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."TICKET_COUNT" > 0
            AND A."REVENUEDAILY_STATE" = 1 AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
            AND B."SERVERPART_CODE" NOT IN ('S000','S092','S093','S094'){prov_where}
            AND A."STATISTICS_DATE" >= {month_start} AND A."STATISTICS_DATE" <= {date_str}"""
    m_rows = db.execute_query(month_sql) or []

    ticket_avg = 0; total_avg = 0.0; avg_rev = 0.0; month_avg_price = 0.0
    province_ticket = 0; province_total = 0.0; province_rev = 0.0; province_avg_price = 0.0
    if m_rows:
        mr = m_rows[0]
        sp_days = _si(mr.get("SP_DAYS")); all_days = _si(mr.get("ALL_DAYS"))
        if sp_days > 0:
            ticket_avg = _si(mr.get("SP_TICKET")) // sp_days
            total_avg = round(_sf(mr.get("SP_TOTAL")) / sp_days, 2)
            avg_rev = round(_sf(mr.get("SP_REVENUE")) / sp_days, 2)
            month_avg_price = round(avg_rev / ticket_avg, 2) if ticket_avg > 0 else 0
        if all_days > 0:
            province_ticket = _si(mr.get("ALL_TICKET")) // all_days
            province_total = round(_sf(mr.get("ALL_TOTAL")) / all_days, 2)
            province_rev = round(_sf(mr.get("ALL_REVENUE")) / all_days, 2)
            province_avg_price = round(province_rev / province_ticket, 2) if province_ticket > 0 else 0

    sp_name = None
    if sp_id:
        sp_name_rows = db.execute_query(f'SELECT "SERVERPART_NAME" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {sp_id}') or []
        sp_name = sp_name_rows[0].get("SERVERPART_NAME", "") if sp_name_rows else ""

    return {
        "Serverpart_ID": sp_id, "Serverpart_Name": sp_name or "",
        "SPRegionType_Name": None, "Statistics_Date": None,
        "TicketCount": ticket_count, "TotalCount": total_count,
        "RevenueAmount": revenue_amount, "AvgTicketPrice": avg_ticket_price,
        "VehicleCount": None, "AvgVehicleAmount": None,
        "TicketAvgCount": ticket_avg, "TotalAvgCount": total_avg,
        "AvgRevenueAmount": avg_rev, "MonthAvgTicketPrice": month_avg_price,
        "MonthVehicleCount": None, "MonthVehicleAmount": None, "ConvertRate": None,
        "TicketProvinceCount": province_ticket, "TotalProvinceCount": province_total,
        "ProvinceRevenueAmount": province_rev, "ProvinceAvgTicketPrice": province_avg_price,
        "ConvertProvinceRate": None, "transactionLevel": None,
    }


# ===== 4. GetTransactionTimeAnalysis =====
def get_transaction_time_analysis(db: DatabaseHelper, province_code, statistics_date,
                                   serverpart_id, sp_region_type_id, time_span) -> Optional[dict]:
    """获取时段消费分析"""
    from datetime import datetime as dt

    if not statistics_date: return None

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    month_str = stat_date.strftime("%Y%m")

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    elif province_code:
        pid = _get_province_id(db, province_code)
        where_sql += f' AND B."PROVINCE_CODE" = {pid}'

    sql = f"""SELECT A."STATISTICS_HOUR",
            ROUND(SUM(A."TICKET_COUNT") / MAX(A."STATISTICS_DAYS"),0) AS "TICKET_COUNT",
            ROUND(SUM(A."SELLMASTER_AMOUNT") / MAX(A."STATISTICS_DAYS"),2) AS "SELLMASTER_AMOUNT"
        FROM "T_YSSELLMASTERMONTH" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."DATA_TYPE" IN (0,1) AND A."STATISTICS_MONTH" = {month_str}{where_sql}
        GROUP BY A."STATISTICS_HOUR" ORDER BY A."STATISTICS_HOUR" """
    rows = db.execute_query(sql) or []
    if not rows: return None

    hour_map = {}
    for r in rows:
        h = int(_sf(r.get("STATISTICS_HOUR")))
        hour_map[h] = {"ticket": _sf(r.get("TICKET_COUNT")), "amount": _sf(r.get("SELLMASTER_AMOUNT"))}

    total_ticket = sum(v["ticket"] for v in hour_map.values())
    scatter_list = []
    slots = 24 // time_span
    for i in range(slots + 1):
        h_start = i * time_span; h_end = min((i + 1) * time_span, 24)
        slot_ticket = sum(hour_map.get(h, {}).get("ticket", 0) for h in range(h_start, h_end))
        slot_amount = sum(hour_map.get(h, {}).get("amount", 0) for h in range(h_start, h_end))
        pct = round(slot_ticket / total_ticket * 100, 2) if total_ticket > 0 else 0
        scatter_list.append({"name": str(min(h_start, 24)), "value": str(pct),
                             "data": str(round(slot_ticket)), "key": str(round(slot_amount))})
    return {"name": "时段交易", "CommonScatterList": scatter_list}


# ===== 5. GetTransactionConvert =====
def get_transaction_convert(db: DatabaseHelper, statistics_date, serverpart_id,
                             sp_region_type_id) -> dict:
    """获取消费转化对比分析"""
    from datetime import datetime as dt

    if not statistics_date:
        return {"TransactionList": None, "BayonetList": None}

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    month_str = stat_date.strftime("%Y%m")

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'

    # 时段客单
    t_sql = f"""SELECT A."STATISTICS_HOUR",
            FLOOR(SUM(A."TICKET_COUNT") * 1.0 / MAX(A."STATISTICS_DAYS") + 0.5) AS "TICKET_COUNT"
        FROM "T_YSSELLMASTERMONTH" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."DATA_TYPE" IN (0,1) AND A."STATISTICS_MONTH" = {month_str}{where_sql}
        GROUP BY A."STATISTICS_HOUR" ORDER BY A."STATISTICS_HOUR" """
    t_rows = db.execute_query(t_sql) or []
    t_data = [[float(h), 0] for h in range(24)]
    for r in t_rows:
        h = int(_sf(r.get("STATISTICS_HOUR")))
        if 0 <= h < 24: t_data[h] = [float(h), _sf(r.get("TICKET_COUNT"))]

    # 时段车流
    b_sql = f"""SELECT A."STATISTICS_HOUR",
            FLOOR(SUM(A."VEHICLE_COUNT") * 1.0 / MAX(A."STATISTICS_DAYS") + 0.5) AS "TICKET_COUNT"
        FROM "T_BAYONETHOURMONTH_AH" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."INOUT_TYPE" = 0 AND A."DATA_TYPE" IN (0,1)
            AND A."STATISTICS_MONTH" = {month_str}{where_sql}
        GROUP BY A."STATISTICS_HOUR" ORDER BY A."STATISTICS_HOUR" """
    b_rows = db.execute_query(b_sql) or []
    b_data = [[float(h), 0] for h in range(24)]
    for r in b_rows:
        h = int(_sf(r.get("STATISTICS_HOUR")))
        if 0 <= h < 24: b_data[h] = [float(h), _sf(r.get("TICKET_COUNT"))]

    return {
        "TransactionList": {"name": "客单数" if t_rows else None, "data": t_data if t_rows else None, "value": None, "CommonScatterList": None},
        "BayonetList": {"name": "车流量", "data": b_data, "value": None, "CommonScatterList": None},
    }


# ===== 6. GetBusinessTradeRevenue =====
def get_business_trade_revenue(db: DatabaseHelper, province_code, statistics_date,
                                serverpart_id, sp_region_type_id, business_trade_ids,
                                data_type) -> Optional[dict]:
    """获取业态营收占比"""
    from datetime import datetime as dt

    if not statistics_date: return None

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    month_start = stat_date.strftime("%Y%m01")
    date_str = stat_date.strftime("%Y%m%d")

    where_sql = f' AND A."STATISTICS_DATE" >= {month_start} AND A."STATISTICS_DATE" <= {date_str}'
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'

    sql = f"""SELECT A."BUSINESS_TRADE",
            SUM(A."TICKET_COUNT") AS "TICKET_COUNT",
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
            AND B."STATISTIC_TYPE" = 1000{where_sql}
        GROUP BY A."BUSINESS_TRADE" ORDER BY SUM(A."TICKET_COUNT") DESC"""
    rows = db.execute_query(sql) or []
    if not rows: return None

    total_ticket = sum(_sf(r.get("TICKET_COUNT")) for r in rows)
    total_rev = sum(_sf(r.get("REVENUE_AMOUNT")) for r in rows)

    # 业态名称字典
    trade_name_map = {}
    try:
        trade_rows = db.execute_query('SELECT "AUTOSTATISTICS_ID", "AUTOSTATISTICS_NAME" FROM "T_AUTOSTATISTICS" WHERE "AUTOSTATISTICS_TYPE" = 2000') or []
        trade_name_map = {str(t.get("AUTOSTATISTICS_ID", "")): t.get("AUTOSTATISTICS_NAME", "其他业态") for t in trade_rows}
    except Exception: pass

    rank_list = []
    for r in rows:
        tc = _sf(r.get("TICKET_COUNT")); ra = _sf(r.get("REVENUE_AMOUNT"))
        trade_id = str(r.get("BUSINESS_TRADE", "") or "")
        trade_name = trade_name_map.get(trade_id, "其他业态") if trade_id else "其他业态"
        pct = round(tc / total_ticket * 100, 2) if data_type == 1 and total_ticket > 0 else (round(ra / total_rev * 100, 2) if total_rev > 0 else 0)
        rank_list.append({"name": trade_name, "value": f"{pct:.2f}",
                          "data": f"客单 {int(tc)}笔,金额 {ra:,.2f}元", "key": trade_id or "0"})

    return {"Serverpart_ID": None, "Serverpart_Name": None, "SPRegionType_Name": None,
            "Rigid_Demand": False, "Abundant": True, "BusinessTradeRank": rank_list}


# ===== 7-8. GetBusinessTradeLevel & GetBusinessBrandLevel =====
# 这两个路由各约 150 行, 含复杂消费等级聚合, 暂保留在 Router 层
# 后续重写 Router 时整体迁移
