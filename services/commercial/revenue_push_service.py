# -*- coding: utf-8 -*-
"""
CommercialApi - 营收推送 Service
从 revenue_router.py 中抽取: GetRevenuePushList, GetSummaryRevenue,
GetSummaryRevenueMonth, GetWechatPushSalesList, GetUnUpLoadShops
每个函数独立、可单独迁移
"""
from __future__ import annotations
from collections import defaultdict
from core.database import DatabaseHelper
from services.commercial.service_utils import (
    safe_float as _sf, safe_int as _si,
    get_province_id as _get_province_id,
    build_sp_where as _build_where_sql,
    date_no_pad,
)


# ===== 1. GetRevenuePushList =====
def get_revenue_push_list(db: DatabaseHelper, push_province_code, statistics_date,
                           serverpart_id, sp_region_type_id, revenue_include) -> list[dict]:
    """获取营收推送数据表列表"""
    from datetime import datetime, timedelta

    province_id = _get_province_id(db, push_province_code)
    where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
    if serverpart_id:
        where_sql += f' AND B."SERVERPART_ID" = {serverpart_id}'
    elif sp_region_type_id:
        sp_res = db.execute_query('SELECT "SPREGIONTYPE_ID" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = :sid', {"sid": sp_region_type_id})
        if sp_res:
            where_sql += f' AND B."SPREGIONTYPE_ID" = {sp_res[0]["SPREGIONTYPE_ID"]}'

    st_date_str = statistics_date.split(" ")[0] if statistics_date else datetime.now().strftime("%Y-%m-%d")
    st_date = datetime.strptime(st_date_str, "%Y-%m-%d")
    is_history = st_date < (datetime.now() - timedelta(days=9))

    if is_history:
        sql = f"""SELECT
                    B."SPREGIONTYPE_NAME", B."SERVERPART_NAME", A."SERVERPART_ID",
                    C."SHOPNAME", C."SHOPREGION" AS "SHOPREGIONNAME",
                    C."BUSINESS_TRADENAME" AS "BUSINESSTRADE_NAME", C."BRAND_NAME" AS "BUSINESSBRAND_NAME",
                    SUM(A."TICKET_COUNT") AS "TICKETCOUNT", SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                    SUM(A."REVENUE_AMOUNT") AS "CASHPAY", SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
                    SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
                    SUM(CASE WHEN A."DIFFERENT_AMOUNT" < 0 THEN A."DIFFERENT_AMOUNT" ELSE 0 END) AS "DIFFERENT_PRICE_LESS",
                    SUM(CASE WHEN A."DIFFERENT_AMOUNT" > 0 THEN A."DIFFERENT_AMOUNT" ELSE 0 END) AS "DIFFERENT_PRICE_MORE",
                    CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME",
                    C."REVENUE_INCLUDE", 1 AS "REVENUE_UPLOAD"
                  FROM "T_REVENUEDAILY" A
                    JOIN "T_SERVERPART" B ON A."SERVERPART_ID" = B."SERVERPART_ID"
                    LEFT JOIN "T_SERVERPARTSHOP" C ON A."SERVERPART_ID" = C."SERVERPART_ID"
                  WHERE A."REVENUEDAILY_STATE" = 1 AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND A."STATISTICS_DATE" = {st_date.strftime('%Y%m%d')}
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}
                  GROUP BY B."SPREGIONTYPE_NAME", B."SERVERPART_NAME", A."SERVERPART_ID", C."SHOPNAME",
                    C."SHOPREGION", C."BUSINESS_TRADENAME", C."BRAND_NAME", A."BUSINESS_TYPE", C."REVENUE_INCLUDE" """
    else:
        sql = f"""SELECT
                    B.SPREGIONTYPE_NAME, B.SERVERPART_NAME, A.SERVERPART_ID,
                    C.SHOPNAME, C.SHOPREGION AS SHOPREGIONNAME,
                    C.BUSINESS_TRADENAME AS BUSINESSTRADE_NAME, C.BRAND_NAME AS BUSINESSBRAND_NAME,
                    SUM(A.TICKETCOUNT) AS TICKETCOUNT, SUM(A.TOTALCOUNT) AS TOTALCOUNT,
                    SUM(A.CASHPAY) AS CASHPAY, SUM(A.CASHPAY - A.CASH) AS MOBILEPAYMENT,
                    SUM(A.TOTALOFFAMOUNT) AS TOTALOFFAMOUNT,
                    SUM(CASE WHEN A.DIFFERENT_PRICE < 0 THEN A.DIFFERENT_PRICE ELSE 0 END) AS DIFFERENT_PRICE_LESS,
                    SUM(CASE WHEN A.DIFFERENT_PRICE > 0 THEN A.DIFFERENT_PRICE ELSE 0 END) AS DIFFERENT_PRICE_MORE,
                    CASE WHEN A.BUSINESS_TYPE = 1000 THEN '自营' ELSE '外包' END AS BUSINESS_TYPENAME,
                    C.REVENUE_INCLUDE, 1 AS REVENUE_UPLOAD
                  FROM T_ENDACCOUNT_TEMP A
                    JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                    JOIN T_SERVERPARTSHOP C ON A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPCODE = C.SHOPCODE
                  WHERE A.VALID = 1 AND B.STATISTIC_TYPE = 1000 AND C.ISVALID = 1
                    AND A.STATISTICS_DATE >= TO_DATE('{st_date_str}', 'YYYY-MM-DD')
                    AND A.STATISTICS_DATE < TO_DATE('{st_date_str}', 'YYYY-MM-DD') + 1
                    AND B.SERVERPART_CODE NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}
                  GROUP BY B.SPREGIONTYPE_NAME, B.SERVERPART_NAME, A.SERVERPART_ID, C.SHOPNAME,
                    C.SHOPREGION, C.BUSINESS_TRADENAME, C.BRAND_NAME, A.BUSINESS_TYPE, C.REVENUE_INCLUDE"""

    rows = db.execute_query(sql) or []


    results = []
    for row in rows:
        results.append({
            "Serverpart_ID": row["SERVERPART_ID"],
            "Serverpart_Name": row["SERVERPART_NAME"],
            "SPRegionType_Name": row["SPREGIONTYPE_NAME"],
            "ShopName": row["SHOPNAME"],
            "ShopRegionName": row["SHOPREGIONNAME"],
            "Business_TypeName": row["BUSINESS_TYPENAME"],
            "BusinessTrade_Name": row["BUSINESSTRADE_NAME"],
            "BusinessBrand_Name": row["BUSINESSBRAND_NAME"],
            "Statistics_Date": date_no_pad(st_date, "ymd_hms"),
            "TicketCount": _si(row["TICKETCOUNT"]),
            "TotalCount": _sf(row["TOTALCOUNT"]),
            "TotalOffAmount": _sf(row["TOTALOFFAMOUNT"]),
            "MobilePayment": _sf(row["MOBILEPAYMENT"]),
            "CashPay": _sf(row["CASHPAY"]),
            "Different_Price_Less": _sf(row["DIFFERENT_PRICE_LESS"]),
            "Different_Price_More": _sf(row["DIFFERENT_PRICE_MORE"]),
            "Revenue_Include": _si(row["REVENUE_INCLUDE"]) if revenue_include == 1 else 0,
            "BusinessType": None, "Revenue_Upload": row["REVENUE_UPLOAD"],
            "TotalShopCount": None, "RevenueQOQ": None, "RevenueYOY": None,
            "YearRevenueAmount": None, "YearRevenueYOY": None,
            "BudgetRevenue": None, "CurAccountRoyalty": None, "AccountRoyaltyQOQ": None,
            "YearAccountRoyalty": 0.0, "YearAccountRoyaltyYOY": 0.0, "UnUpLoadShopList": None,
        })
    return results


# ===== 2. GetSummaryRevenue =====
def get_summary_revenue(db: DatabaseHelper, push_province_code, statistics_start_date,
                         statistics_date, sp_region_type_id, serverpart_id,
                         revenue_include, show_compare_rate, show_year_revenue) -> dict:
    """获取营收推送汇总数据"""
    from datetime import datetime

    province_id = _get_province_id(db, push_province_code)
    where_sql = _build_where_sql(province_id, serverpart_id, sp_region_type_id)

    end_str = statistics_date.split(" ")[0] if statistics_date else datetime.now().strftime("%Y-%m-%d")
    start_str = statistics_start_date.split(" ")[0] if statistics_start_date else end_str
    end_date = datetime.strptime(end_str, "%Y-%m-%d")
    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    sd_start = start_date.strftime("%Y%m%d")
    sd_end = end_date.strftime("%Y%m%d")

    sql = f"""SELECT
                B."SPREGIONTYPE_NAME", B."SERVERPART_NAME", A."SERVERPART_ID",
                SUM(A."TICKET_COUNT") AS "TICKETCOUNT", SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                SUM(A."REVENUE_AMOUNT") AS "CASHPAY", SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
                SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
                SUM(CASE WHEN A."DIFFERENT_AMOUNT" < 0 THEN A."DIFFERENT_AMOUNT" ELSE 0 END) AS "DIFFERENT_PRICE_LESS",
                SUM(CASE WHEN A."DIFFERENT_AMOUNT" > 0 THEN A."DIFFERENT_AMOUNT" ELSE 0 END) AS "DIFFERENT_PRICE_MORE",
                CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME",
                A."SHOPTRADE", SUM(A."REVENUE_AMOUNT_YOY") AS "REVENUE_AMOUNT_YOY"
              FROM "T_REVENUEDAILY" A
                JOIN "T_SERVERPART" B ON A."SERVERPART_ID" = B."SERVERPART_ID"
              WHERE A."REVENUEDAILY_STATE" = 1 AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND A."STATISTICS_DATE" BETWEEN {sd_start} AND {sd_end}
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql}
              GROUP BY B."SPREGIONTYPE_NAME", B."SERVERPART_NAME", A."SERVERPART_ID",
                A."BUSINESS_TYPE", A."SHOPTRADE" """
    rows = db.execute_query(sql) or []

    empty_result = {
        "RevenuePushModel": None, "GrowthRate": 0.0,
        "MonthRevenueAmount": 0.0, "YearRevenueAmount": 0.0,
        "BusinessTypeList": [], "BusinessTradeList": [], "SPRegionList": [],
    }
    if not rows:
        return empty_result

    revenue_yoy = round(sum(_sf(r.get("REVENUE_AMOUNT_YOY")) for r in rows), 2)
    total_cashpay = round(sum(_sf(r.get("CASHPAY")) for r in rows), 2)
    total_ticket = sum(_si(r.get("TICKETCOUNT")) for r in rows)

    summary_model = {
        "Serverpart_ID": int(serverpart_id) if serverpart_id else None,
        "Serverpart_Name": rows[0].get("SERVERPART_NAME", "") if serverpart_id else "",
        "CashPay": total_cashpay, "TicketCount": total_ticket,
        "TotalCount": round(sum(_sf(r.get("TOTALCOUNT")) for r in rows), 2),
        "TotalOffAmount": round(sum(_sf(r.get("TOTALOFFAMOUNT")) for r in rows), 2),
        "MobilePayment": round(sum(_sf(r.get("MOBILEPAYMENT")) for r in rows), 2),
        "Different_Price_Less": round(sum(_sf(r.get("DIFFERENT_PRICE_LESS")) for r in rows), 2),
        "Different_Price_More": round(sum(_sf(r.get("DIFFERENT_PRICE_MORE")) for r in rows), 2),
        "RevenueYOY": revenue_yoy, "Revenue_Upload": None, "TotalShopCount": None,
        "UnUpLoadShopList": None, "SPRegionType_Name": None, "ShopName": None,
        "ShopRegionName": None, "BusinessTrade_Name": None, "BusinessBrand_Name": None,
        "Business_TypeName": None, "BusinessType": None, "Revenue_Include": None,
        "Statistics_Date": None, "BudgetRevenue": 0.0, "RevenueQOQ": None,
        "CurAccountRoyalty": None, "AccountRoyaltyQOQ": None,
        "YearRevenueAmount": None, "YearRevenueYOY": None,
        "YearAccountRoyalty": 0.0, "YearAccountRoyaltyYOY": 0.0,
    }

    # 经营模式分析
    bt_groups = defaultdict(lambda: {"cash": 0.0, "yoy": 0.0})
    sp_groups = defaultdict(float)
    for r in rows:
        bt_name = r.get("BUSINESS_TYPENAME") or "其他"
        bt_groups[bt_name]["cash"] += _sf(r.get("CASHPAY"))
        bt_groups[bt_name]["yoy"] += _sf(r.get("REVENUE_AMOUNT_YOY"))
        sp_name = r.get("SPREGIONTYPE_NAME")
        if sp_name: sp_groups[sp_name] += _sf(r.get("CASHPAY"))

    business_type_list = [{"name": n, "value": f"{v['cash']:.2f}", "data": f"{v['yoy']:.2f}", "key": None}
                          for n, v in sorted(bt_groups.items(), key=lambda x: x[1]["cash"], reverse=True)]
    sp_region_list = [{"name": n, "value": f"{v:.2f}"}
                      for n, v in sorted(sp_groups.items(), key=lambda x: x[1], reverse=True)]

    # 经营业态分析
    shop_where = where_sql.replace('B.', 'B2.')
    shop_sql = f"""SELECT A2."SERVERPART_ID", A2."SHOPTRADE", A2."BUSINESS_TRADENAME"
        FROM "T_SERVERPARTSHOP" A2, "T_SERVERPART" B2
        WHERE A2."SERVERPART_ID" = B2."SERVERPART_ID" AND A2."ISVALID" = 1
            AND A2."BUSINESS_TRADE" IS NOT NULL {shop_where}
        GROUP BY A2."SERVERPART_ID", A2."SHOPTRADE", A2."BUSINESS_TRADENAME" """
    shop_rows = db.execute_query(shop_sql) or []
    trade_name_map = {(str(s.get("SERVERPART_ID")), str(s.get("SHOPTRADE"))): str(s.get("BUSINESS_TRADENAME") or "")
                      for s in shop_rows}

    mapping_sql = """SELECT A."AUTOSTATISTICS_NAME" AS "CHILD", B."AUTOSTATISTICS_NAME" AS "PARENT"
                     FROM "T_AUTOSTATISTICS" A, "T_AUTOSTATISTICS" B
                     WHERE A."AUTOSTATISTICS_PID" = B."AUTOSTATISTICS_ID" AND B."AUTOSTATISTICS_PID" = -1"""
    mapping_rows = db.execute_query(mapping_sql) or []
    parent_mapping = {mr["CHILD"]: mr["PARENT"] for mr in mapping_rows}

    parent_trade_groups = defaultdict(float)
    for r in rows:
        key = (str(r.get("SERVERPART_ID")), str(r.get("SHOPTRADE")))
        child_name = trade_name_map.get(key, "")
        parent_name = parent_mapping.get(child_name, "其他") if child_name else "其他"
        parent_trade_groups[parent_name] += _sf(r.get("CASHPAY"))

    business_trade_list = [{"name": n, "value": f"{v:.2f}"}
                           for n, v in sorted(parent_trade_groups.items(), key=lambda x: x[1], reverse=True)]

    return {
        "BusinessTradeList": business_trade_list, "BusinessTypeList": business_type_list,
        "GrowthRate": 0.0, "MonthRevenueAmount": 0.0,
        "RevenuePushModel": summary_model, "SPRegionList": sp_region_list,
        "YearRevenueAmount": 0.0,
    }


# ===== 3. GetWechatPushSalesList =====
def get_wechat_push_sales_list(db: DatabaseHelper, push_province_code, statistics_date, rank_num) -> list[dict]:
    """获取单品销售排行榜数据"""
    from datetime import datetime
    stat_date_str = statistics_date.split(" ")[0] if statistics_date else datetime.now().strftime("%Y-%m-%d")
    province_id = _get_province_id(db, push_province_code)

    sql = f"""SELECT
                CASE WHEN BUSINESSTYPE IN ('1000','1005') THEN 1000
                     WHEN BUSINESSTYPE LIKE '2%' THEN 2000
                     WHEN BUSINESSTYPE LIKE '3%' THEN 3000 ELSE 1000 END AS BUSINESSTYPE_GROUP,
                A.COMMODITY_NAME,
                SUM(A.TOTALCOUNT) AS TOTALCOUNT,
                SUM(A.TOTALSELLAMOUNT) AS TOTALSELLAMOUNT
            FROM T_COMMODITYSALE A
            WHERE A.ENDDATE >= TO_DATE('{stat_date_str}', 'YYYY-MM-DD')
                AND A.ENDDATE < TO_DATE('{stat_date_str}', 'YYYY-MM-DD') + 1
                AND A.SERVERPARTCODE NOT IN ('888888','899999')
                AND EXISTS (SELECT 1 FROM T_SERVERPART B WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.PROVINCE_CODE = '{province_id}')
            GROUP BY
                CASE WHEN BUSINESSTYPE IN ('1000','1005') THEN 1000
                     WHEN BUSINESSTYPE LIKE '2%' THEN 2000
                     WHEN BUSINESSTYPE LIKE '3%' THEN 3000 ELSE 1000 END,
                A.COMMODITY_NAME"""

    rows = db.execute_query(sql) or []
    groups = defaultdict(list)
    for r in rows:
        groups[int(r["BUSINESSTYPE_GROUP"])].append({
            "Commodity_Name": r["COMMODITY_NAME"],
            "SellCount": _sf(r["TOTALCOUNT"]),
            "TotalPrice": _sf(r["TOTALSELLAMOUNT"]),
        })

    result_list = []
    for b_type in [1000, 2000, 3000]:
        if b_type not in groups: continue
        sorted_goods = sorted(groups[b_type], key=lambda x: x["SellCount"], reverse=True)[:rank_num]
        for i, g in enumerate(sorted_goods): g["Rank_ID"] = i + 1
        result_list.append({"Data_Type": b_type, "TotalCount": len(groups[b_type]), "GoodsList": sorted_goods})
    return result_list


# ===== 4. GetUnUpLoadShops =====
def get_un_upload_shops(db: DatabaseHelper, push_province_code, statistics_date,
                         sp_region_type_id, serverpart_id, revenue_include) -> list[dict]:
    """查询服务区未上传结账信息的门店列表"""
    from datetime import datetime as dt, timedelta

    stat_date = statistics_date or dt.now().strftime("%Y-%m-%d")
    stat_dt = dt.strptime(stat_date.split(" ")[0], "%Y-%m-%d")
    table_suffix = "" if stat_dt < dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=9) else "_TEMP"

    where_sql = ""
    if serverpart_id:
        where_sql += f' AND B."SERVERPART_ID" = {serverpart_id}'
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" = {sp_region_type_id}'
    elif push_province_code:
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": push_province_code})
        if fe_rows:
            where_sql += f' AND B."PROVINCE_CODE" = {fe_rows[0]["FIELDENUM_ID"]}'
    if revenue_include == 1:
        where_sql += ' AND A."REVENUE_INCLUDE" = 1'

    date_str = stat_date.split(" ")[0]
    sql = f"""SELECT B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX", B."SERVERPART_CODE",
            A."SERVERPARTSHOP_ID", A."SHOPREGION", A."SHOPTRADE", A."SHOPCODE", A."SHOPNAME"
        FROM "T_SERVERPARTSHOP" A, "T_SERVERPART" B
        WHERE COALESCE(A."BUSINESS_DATE", TO_DATE('{date_str}','YYYY-MM-DD')) < TO_DATE('{date_str}','YYYY-MM-DD') + 1
            AND COALESCE(A."BUSINESS_ENDDATE", TO_DATE('{date_str}','YYYY-MM-DD')) >= TO_DATE('{date_str}','YYYY-MM-DD')
            AND COALESCE(A."STATISTIC_TYPE", 1000) = 1000
            AND COALESCE(A."BUSINESS_STATE", 1000) = 1000
            AND A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."SHOPTRADE" NOT IN ('9032','9999')
            AND A."ISVALID" = 1
            AND NOT EXISTS (SELECT 1 FROM "T_ENDACCOUNT{table_suffix}" C
                WHERE A."SERVERPART_ID" = C."SERVERPART_ID" AND A."SHOPCODE" = C."SHOPCODE"
                    AND C."VALID" = 1 AND TRUNC(C."STATISTICS_DATE") = TO_DATE('{date_str}','YYYY-MM-DD')){where_sql}
        UNION ALL
        SELECT B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX", B."SERVERPART_CODE",
            A."SERVERPARTSHOP_ID", A."SHOPREGION", A."SHOPTRADE", A."SHOPCODE", A."SHOPNAME"
        FROM "T_SERVERPARTSHOP" A, "T_SERVERPART" B
        WHERE COALESCE(A."STATISTIC_TYPE", 1000) = 1000
            AND COALESCE(A."BUSINESS_STATE", 1000) = 1000
            AND A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."SHOPTRADE" NOT IN ('9032','9999')
            AND A."ISVALID" = 1
            AND EXISTS (SELECT 1 FROM "T_ENDACCOUNT{table_suffix}" C
                WHERE A."SERVERPART_ID" = C."SERVERPART_ID" AND A."SHOPCODE" = C."SHOPCODE"
                    AND C."VALID" = 1 AND TRUNC(C."STATISTICS_DATE") = TO_DATE('{date_str}','YYYY-MM-DD')
                    AND C."DIFFERENCE_REASON" = '无结账信息' AND C."CASHPAY" = 0){where_sql}"""

    rows = db.execute_query(sql) or []
    rows = sorted(rows, key=lambda x: (
        _si(x.get("SERVERPART_INDEX")), _si(x.get("SERVERPART_CODE")),
        str(x.get("SHOPREGION") or ""), str(x.get("SHOPTRADE") or "")))

    return [{"Serverpart_ID": r.get("SERVERPART_ID"),
             "Serverpart_Name": r.get("SERVERPART_NAME", ""),
             "ServerpartShop_ID": r.get("SERVERPARTSHOP_ID"),
             "ServerpartShop_Name": r.get("SHOPNAME", ""),
             "Statistics_Date": stat_date} for r in rows]


# ===== 6. GetSPRevenueRank =====
def get_sp_revenue_rank(db: DatabaseHelper, push_province_code, statistics_date,
                         serverpart_id, sp_region_type_id, revenue_include) -> tuple[list, float]:
    """获取近日服务区营收排行，返回 (result_list, sum_cashpay)"""
    from datetime import datetime as dt

    if not push_province_code or not statistics_date:
        return [], 0.0

    # 构建过滤条件
    where_sql = ""
    if serverpart_id is not None:
        where_sql += f' AND B."SERVERPART_ID" = {serverpart_id}'
    elif sp_region_type_id is not None:
        sp_res = db.execute_query(
            'SELECT "SPREGIONTYPE_ID" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = :sid',
            {"sid": sp_region_type_id})
        if sp_res:
            where_sql += f' AND B."SPREGIONTYPE_ID" = {sp_res[0]["SPREGIONTYPE_ID"]}'
        else:
            return [], 0.0
    elif push_province_code:
        province_id = _get_province_id(db, push_province_code)
        if not province_id:
            return [], 0.0
        where_sql += f' AND B."PROVINCE_CODE" = {province_id}'
    else:
        return [], 0.0

    # 日期标准化
    stat_date_str = statistics_date
    if "-" in statistics_date:
        stat_date_str = dt.strptime(statistics_date, "%Y-%m-%d").strftime("%Y%m%d")
    elif "/" in statistics_date:
        stat_date_str = dt.strptime(statistics_date, "%Y/%m/%d").strftime("%Y%m%d")
    where_sql += f' AND A."STATISTICS_DATE" >= {stat_date_str} AND A."STATISTICS_DATE" <= {stat_date_str}'

    # Revenue_Include 过滤
    exists_where = ""
    if revenue_include == 1:
        exists_where = ' AND C."REVENUE_INCLUDE" = 1'

    # 按服务区分组汇总
    sql = f"""SELECT A."SERVERPART_ID", B."SERVERPART_NAME", B."SPREGIONTYPE_NAME",
            SUM(A."REVENUE_AMOUNT") AS "CASHPAY",
            SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
            SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
            SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
            SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
            SUM(NVL(A."DIFFERENT_AMOUNT_LESS_A",0) + NVL(A."DIFFERENT_AMOUNT_LESS_B",0)) AS "DIFFERENT_PRICE_LESS",
            SUM(NVL(A."DIFFERENT_AMOUNT_MORE_A",0) + NVL(A."DIFFERENT_AMOUNT_MORE_B",0)) AS "DIFFERENT_PRICE_MORE"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
            AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
            AND B."SERVERPART_CODE" NOT IN ('AH0000','AH9999','test001')
            {where_sql}"""

    if revenue_include == 1:
        sql += f"""
            AND EXISTS (SELECT 1 FROM "T_SERVERPARTSHOP" C
                WHERE A."SHOPTRADE" = C."SHOPTRADE" AND B."SERVERPART_ID" = C."SERVERPART_ID"
                AND C."ISVALID" = 1{exists_where})"""

    sql += """
        GROUP BY A."SERVERPART_ID", B."SERVERPART_NAME", B."SPREGIONTYPE_NAME"
        ORDER BY SUM(A."REVENUE_AMOUNT") DESC"""

    rows = db.execute_query(sql) or []

    result_list = []
    for r in rows:
        result_list.append({
            "Serverpart_ID": r.get("SERVERPART_ID"),
            "Serverpart_Name": r.get("SERVERPART_NAME", ""),
            "SPRegionType_Name": r.get("SPREGIONTYPE_NAME", ""),
            "TicketCount": _si(r.get("TICKETCOUNT")),
            "TotalCount": round(_sf(r.get("TOTALCOUNT")), 2),
            "TotalOffAmount": round(_sf(r.get("TOTALOFFAMOUNT")), 2),
            "MobilePayment": round(_sf(r.get("MOBILEPAYMENT")), 2),
            "CashPay": round(_sf(r.get("CASHPAY")), 2),
            "Different_Price_Less": round(_sf(r.get("DIFFERENT_PRICE_LESS")), 2),
            "Different_Price_More": round(_sf(r.get("DIFFERENT_PRICE_MORE")), 2),
            "RevenueYOY": None,
            "YearAccountRoyalty": 0.0,
            "YearAccountRoyaltyYOY": 0.0,
        })

    # 汇总 CashPay
    sum_cashpay = float(round(sum(item.get("CashPay", 0.0) for item in result_list), 2))
    # 排除万佳商贸
    result_list = [item for item in result_list if item.get("SPRegionType_Name") != "万佳商贸"]

    return result_list, sum_cashpay


# ===== 7. GetSummaryRevenueMonth =====
def get_summary_revenue_month(db: DatabaseHelper, push_province_code, statistics_month,
                                statistics_date, solid_type) -> dict:
    """获取月度营收推送汇总数据
    返回完整的 Result_Data dict，Router 层直接 Result.success(data=...) 包装
    """
    from datetime import datetime, timedelta
    from collections import defaultdict

    if not push_province_code:
        return None

    month_str = statistics_month.replace("-", "") if statistics_month else datetime.now().strftime("%Y%m")
    date_str = statistics_date.split(" ")[0] if statistics_date else None

    # SolidType 解析（C# bool 类型）
    solid_type_bool = str(solid_type).lower() == "true"
    should_check_dashboard = not solid_type_bool

    # 1. 省份映射
    province_id = _get_province_id(db, push_province_code)

    # 2. 日期计算
    is_current_month = False
    if date_str and "-" in date_str:
        is_current_month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m") == month_str

    if is_current_month:
        stat_dt = datetime.strptime(date_str, "%Y-%m-%d")
        cur_month_end = (stat_dt - timedelta(days=1)).strftime("%Y%m%d")
        last_month_end = (stat_dt.replace(day=1) - timedelta(days=1)).strftime("%Y%m%d")
        last_year_str = stat_dt.replace(year=stat_dt.year - 1).strftime("%Y%m%d")
        sd_start = stat_dt.strftime("%Y%m") + "01"
        sd_end = stat_dt.strftime("%Y%m%d")
    else:
        m_dt = datetime.strptime(month_str + "01", "%Y%m%d")
        if m_dt.month < 12:
            cur_month_end = (m_dt.replace(month=m_dt.month + 1, day=1) - timedelta(days=1)).strftime("%Y%m%d")
        else:
            cur_month_end = m_dt.replace(month=12, day=31).strftime("%Y%m%d")
        last_month_end = (m_dt - timedelta(days=1)).strftime("%Y%m%d")
        if m_dt.month < 12:
            last_year_str = (m_dt.replace(year=m_dt.year - 1, month=m_dt.month + 1, day=1) - timedelta(days=1)).strftime("%Y%m%d")
        else:
            last_year_str = m_dt.replace(year=m_dt.year - 1, month=12, day=31).strftime("%Y%m%d")
        sd_start = sd_end = ""

    # 3. Dashboard 快速路径
    if should_check_dashboard:
        dash_sql = f"""SELECT * FROM "T_REVENUEDASHBOARD" WHERE "PROVINCE_ID" = {province_id} AND "STATISTICS_MONTH" = {month_str}"""
        dash_rows = db.execute_query(dash_sql) or []
        if dash_rows:
            bt_array = ["自营", "外包", "便利店", "餐饮客房", "商铺租赁"]
            no_bt = [r for r in dash_rows if r.get("BUSINESS_TYPE") is None]
            bt_rows = sorted([r for r in dash_rows if r.get("BUSINESS_TYPE") and int(_sf(r.get("BUSINESS_TYPE"))) > 0],
                            key=lambda x: int(_sf(x.get("BUSINESS_TYPE"))))

            month_rev = {
                "CashPay": round(sum(_sf(r.get("MONTHLY_REVENUE")) for r in no_bt), 2),
                "RevenueQOQ": round(sum(_sf(r.get("MONTHLY_REVENUE_QOQ")) for r in no_bt), 2),
                "RevenueYOY": round(sum(_sf(r.get("MONTHLY_REVENUE_YOY")) for r in no_bt), 2),
                "YearRevenueAmount": round(sum(_sf(r.get("ANNUAL_REVENUE")) for r in no_bt), 2),
                "YearRevenueYOY": round(sum(_sf(r.get("ANNUAL_REVENUE_YOY")) for r in no_bt), 2),
                "YearAccountRoyalty": round(sum(_sf(r.get("ANNUAL_ACCOUNT")) for r in no_bt), 2),
                "YearAccountRoyaltyYOY": round(sum(_sf(r.get("ANNUAL_ACCOUNT_YOY")) for r in no_bt), 2),
                "CurAccountRoyalty": {
                    "Royalty_Theory": round(sum(_sf(r.get("MONTHLY_ACCOUNT")) for r in no_bt), 2),
                    "SubRoyalty_Theory": round(sum(_sf(r.get("MONTHLY_SUBACCOUNT")) for r in no_bt), 2),
                    "Royalty_Price": None, "SubRoyalty_Price": None,
                },
                "TicketCount": None, "TotalCount": None, "TotalOffAmount": None, "MobilePayment": None,
                "Serverpart_ID": None, "Serverpart_Name": None, "SPRegionType_Name": None,
                "ShopName": None, "ShopRegionName": None, "BusinessType": None,
                "Business_TypeName": None, "BusinessTrade_Name": None, "BusinessBrand_Name": None,
                "Revenue_Include": None, "Revenue_Upload": None, "TotalShopCount": None,
                "BudgetRevenue": None, "Different_Price_Less": None, "Different_Price_More": None,
                "Statistics_Date": None, "AccountRoyaltyQOQ": None, "UnUpLoadShopList": None,
            }

            bt_list = []
            for r in bt_rows:
                bt_idx = int(_sf(r.get("BUSINESS_TYPE"))) - 1
                if 0 <= bt_idx < len(bt_array):
                    bt_list.append({
                        "name": bt_array[bt_idx],
                        "value": str(r.get("MONTHLY_REVENUE") if r.get("MONTHLY_REVENUE") is not None else ""),
                        "data": str(r.get("MONTHLY_REVENUE_YOY") if r.get("MONTHLY_REVENUE_YOY") is not None else ""),
                        "key": str(r.get("MONTHLY_REVENUE_QOQ") if r.get("MONTHLY_REVENUE_QOQ") is not None else ""),
                    })

            growth = round(sum(_sf(r.get("GROWTH_RATE")) for r in no_bt), 2)

            return {
                "BusinessTradeList": [], "BusinessTypeList": bt_list,
                "GrowthRate": growth, "MonthRevenueModel": month_rev,
                "RevenuePushModel": None, "SPRegionList": [],
            }

    # 4. 非 Dashboard 路径：查询月度营收数据
    where_sql_last = f' AND A."PROVINCE_ID" = {province_id}'
    where_sql = f' AND B."PROVINCE_CODE" = {province_id}'

    if is_current_month:
        table_name = '"T_REVENUEDAILY"'
        state_name = '"REVENUEDAILY_STATE"'
        date_sql = f' AND A."STATISTICS_DATE" >= {sd_start} AND A."STATISTICS_DATE" < {sd_end}'
    else:
        table_name = '"T_REVENUEMONTHLY"'
        state_name = '"REVENUEMONTHLY_STATE"'
        date_sql = f' AND A."STATISTICS_MONTH" = {month_str}'

    if is_current_month:
        rev_sql = f"""SELECT
                SUM(A."REVENUE_AMOUNT") AS "CASHPAY", SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
                SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
                SUM(NVL(A."DIFFERENT_AMOUNT_LESS_A",0) + NVL(A."DIFFERENT_AMOUNT_LESS_B",0)) AS "DIFFERENT_PRICE_LESS",
                SUM(NVL(A."DIFFERENT_AMOUNT_MORE_A",0) + NVL(A."DIFFERENT_AMOUNT_MORE_B",0)) AS "DIFFERENT_PRICE_MORE",
                CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME",
                NULL AS "SPREGIONTYPE_NAME", NULL AS "SERVERPART_ID", NULL AS "SHOPTRADE", '' AS "BUSINESS_TRADENAME"
            FROM {table_name} A
            WHERE A."SERVERPART_ID" = 0 AND A.{state_name} = 1{where_sql_last}{date_sql}
            GROUP BY CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END"""
    else:
        rev_sql = f"""SELECT
                SUM(A."REVENUE_AMOUNT") AS "CASHPAY", SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
                SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
                SUM(NVL(A."DIFFERENT_AMOUNT_LESS_A",0) + NVL(A."DIFFERENT_AMOUNT_LESS_B",0)) AS "DIFFERENT_PRICE_LESS",
                SUM(NVL(A."DIFFERENT_AMOUNT_MORE_A",0) + NVL(A."DIFFERENT_AMOUNT_MORE_B",0)) AS "DIFFERENT_PRICE_MORE",
                CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME",
                B."SPREGIONTYPE_NAME", A."SERVERPART_ID", A."SHOPTRADE", '' AS "BUSINESS_TRADENAME"
            FROM {table_name} A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A.{state_name} = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999'){where_sql}{date_sql}
            GROUP BY A."SERVERPART_ID", A."SHOPTRADE", B."SPREGIONTYPE_NAME",
                CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END"""

    rows = db.execute_query(rev_sql) or []
    if not rows:
        return {
            "BusinessTradeList": [], "BusinessTypeList": [],
            "GrowthRate": 0.0, "MonthRevenueModel": None,
            "RevenuePushModel": None, "SPRegionList": [],
        }

    # 5. 环比/同比/年度累计
    yoy_map = {}
    if is_current_month:
        yoy_dates = f' AND A."STATISTICS_DATE" IN ({cur_month_end},{last_month_end},{last_year_str})'
        yoy_sql = f"""SELECT
                SUM(A."REVENUE_AMOUNT_MONTH") AS "CASHPAY",
                SUM(A."REVENUE_AMOUNT_YEAR") AS "REVENUE_AMOUNT_YEAR",
                A."STATISTICS_DATE" AS "STATISTICS_MONTH",
                CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME"
            FROM "T_REVENUEDAILY" A
            WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1{where_sql_last}{yoy_dates}
            GROUP BY A."STATISTICS_DATE", CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END"""
        yoy_rows = db.execute_query(yoy_sql) or []
        for r in yoy_rows:
            key = (str(r.get("STATISTICS_MONTH", "")), r.get("BUSINESS_TYPENAME", ""))
            yoy_map[key] = {"cashpay": _sf(r.get("CASHPAY")), "year": _sf(r.get("REVENUE_AMOUNT_YEAR"))}

    # 6. 聚合
    bt_groups = defaultdict(float)
    sp_groups = defaultdict(float)
    total_cash = round(sum(_sf(r.get("CASHPAY")) for r in rows), 2)
    total_ticket = sum(int(_sf(r.get("TICKETCOUNT"))) for r in rows)
    total_count = round(sum(_sf(r.get("TOTALCOUNT")) for r in rows), 2)
    total_off = round(sum(_sf(r.get("TOTALOFFAMOUNT")) for r in rows), 2)
    total_mobile = round(sum(_sf(r.get("MOBILEPAYMENT")) for r in rows), 2)
    total_diff_less = round(sum(_sf(r.get("DIFFERENT_PRICE_LESS")) for r in rows), 2)
    total_diff_more = round(sum(_sf(r.get("DIFFERENT_PRICE_MORE")) for r in rows), 2)

    for r in rows:
        bt_groups[r.get("BUSINESS_TYPENAME") or "其他"] += _sf(r.get("CASHPAY"))
        sp_name = r.get("SPREGIONTYPE_NAME")
        if sp_name:
            sp_groups[sp_name] += _sf(r.get("CASHPAY"))

    qoq_total = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if str(k[0]) == last_month_end)
    yoy_total = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if str(k[0]) == last_year_str)
    year_rev = sum(v.get("year", 0) for k, v in yoy_map.items() if str(k[0]) == cur_month_end)
    year_yoy = sum(v.get("year", 0) for k, v in yoy_map.items() if str(k[0]) == last_year_str)

    month_rev_model = {
        "CashPay": total_cash, "TicketCount": total_ticket,
        "TotalCount": total_count, "TotalOffAmount": total_off,
        "MobilePayment": total_mobile,
        "Different_Price_Less": total_diff_less, "Different_Price_More": total_diff_more,
        "RevenueQOQ": round(qoq_total, 2) if qoq_total else None,
        "RevenueYOY": round(yoy_total, 2) if yoy_total else None,
        "YearRevenueAmount": round(year_rev, 2) if year_rev else None,
        "YearRevenueYOY": round(year_yoy, 2) if year_yoy else None,
        "Serverpart_ID": None, "Serverpart_Name": None, "SPRegionType_Name": None,
        "ShopName": None, "ShopRegionName": None, "BusinessType": None,
        "Business_TypeName": None, "BusinessTrade_Name": None, "BusinessBrand_Name": None,
        "Revenue_Include": None, "Revenue_Upload": None, "TotalShopCount": None,
        "BudgetRevenue": None, "Statistics_Date": None,
        "CurAccountRoyalty": None, "AccountRoyaltyQOQ": None,
        "YearAccountRoyalty": None, "YearAccountRoyaltyYOY": None,
        "UnUpLoadShopList": None,
    }

    # 经营模式列表
    bt_array = ["自营", "外包", "便利店", "餐饮客房", "商铺租赁"]
    bt_list = []
    for name in bt_array:
        val = bt_groups.get(name)
        if val is not None and val != 0:
            yoy_val = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if k[0] == last_year_str and k[1] == name)
            qoq_val = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if k[0] == last_month_end and k[1] == name)
            bt_list.append({
                "name": name,
                "value": str(round(val, 2)),
                "data": str(round(yoy_val, 2)) if yoy_val else "0",
                "key": str(round(qoq_val, 2)) if qoq_val else "0",
            })

    # 区域列表
    sp_region_list = [{"name": n, "value": f"{v:.2f}"} for n, v in sorted(sp_groups.items(), key=lambda x: x[1], reverse=True)]

    return {
        "BusinessTradeList": [], "BusinessTypeList": bt_list,
        "GrowthRate": 0.0, "MonthRevenueModel": month_rev_model,
        "RevenuePushModel": None,  # Router 层负责嵌套调用 get_summary_revenue
        "SPRegionList": sp_region_list,
    }


# ===== 8. GetRevenuePushList =====
def get_revenue_push_list(db: DatabaseHelper, push_province_code, statistics_date,
                           serverpart_id, sp_region_type_id, revenue_include) -> list:
    """获取营收推送数据表列表（历史表/实时表两路径）"""
    from datetime import datetime, timedelta

    # 省份映射
    province_id = _get_province_id(db, push_province_code)

    where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
    if serverpart_id:
        where_sql += f' AND B."SERVERPART_ID" = {serverpart_id}'
    elif sp_region_type_id:
        sp_res = db.execute_query(
            'SELECT "SPREGIONTYPE_ID" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = :sid',
            {"sid": sp_region_type_id})
        if sp_res:
            where_sql += f' AND B."SPREGIONTYPE_ID" = {sp_res[0]["SPREGIONTYPE_ID"]}'

    # 日期确定
    st_date_str = statistics_date.split(" ")[0] if statistics_date else datetime.now().strftime("%Y-%m-%d")
    st_date = datetime.strptime(st_date_str, "%Y-%m-%d")
    is_history = st_date < (datetime.now() - timedelta(days=9))

    if is_history:
        sql = f"""SELECT
                    B."SPREGIONTYPE_NAME", B."SERVERPART_NAME", A."SERVERPART_ID",
                    C."SHOPNAME", C."SHOPREGION" AS "SHOPREGIONNAME",
                    C."BUSINESS_TRADENAME" AS "BUSINESSTRADE_NAME", C."BRAND_NAME" AS "BUSINESSBRAND_NAME",
                    SUM(A."TICKET_COUNT") AS "TICKETCOUNT", SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                    SUM(A."REVENUE_AMOUNT") AS "CASHPAY", SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
                    SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
                    SUM(CASE WHEN A."DIFFERENT_AMOUNT" < 0 THEN A."DIFFERENT_AMOUNT" ELSE 0 END) AS "DIFFERENT_PRICE_LESS",
                    SUM(CASE WHEN A."DIFFERENT_AMOUNT" > 0 THEN A."DIFFERENT_AMOUNT" ELSE 0 END) AS "DIFFERENT_PRICE_MORE",
                    CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME",
                    C."REVENUE_INCLUDE", 1 AS "REVENUE_UPLOAD"
                  FROM
                    "T_REVENUEDAILY" A
                    JOIN "T_SERVERPART" B ON A."SERVERPART_ID" = B."SERVERPART_ID"
                    LEFT JOIN "T_SERVERPARTSHOP" C ON A."SERVERPART_ID" = C."SERVERPART_ID"
                  WHERE
                    A."REVENUEDAILY_STATE" = 1 AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND A."STATISTICS_DATE" = {st_date.strftime('%Y%m%d')}
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}
                  GROUP BY
                    B."SPREGIONTYPE_NAME", B."SERVERPART_NAME", A."SERVERPART_ID", C."SHOPNAME", C."SHOPREGION",
                    C."BUSINESS_TRADENAME", C."BRAND_NAME", A."BUSINESS_TYPE", C."REVENUE_INCLUDE" """
    else:
        sql = f"""SELECT
                    B.SPREGIONTYPE_NAME, B.SERVERPART_NAME, A.SERVERPART_ID,
                    C.SHOPNAME, C.SHOPREGION AS SHOPREGIONNAME,
                    C.BUSINESS_TRADENAME AS BUSINESSTRADE_NAME, C.BRAND_NAME AS BUSINESSBRAND_NAME,
                    SUM(A.TICKETCOUNT) AS TICKETCOUNT, SUM(A.TOTALCOUNT) AS TOTALCOUNT,
                    SUM(A.CASHPAY) AS CASHPAY, SUM(A.CASHPAY - A.CASH) AS MOBILEPAYMENT,
                    SUM(A.TOTALOFFAMOUNT) AS TOTALOFFAMOUNT,
                    SUM(CASE WHEN A.DIFFERENT_PRICE < 0 THEN A.DIFFERENT_PRICE ELSE 0 END) AS DIFFERENT_PRICE_LESS,
                    SUM(CASE WHEN A.DIFFERENT_PRICE > 0 THEN A.DIFFERENT_PRICE ELSE 0 END) AS DIFFERENT_PRICE_MORE,
                    CASE WHEN A.BUSINESS_TYPE = 1000 THEN '自营' ELSE '外包' END AS BUSINESS_TYPENAME,
                    C.REVENUE_INCLUDE, 1 AS REVENUE_UPLOAD
                  FROM
                    T_ENDACCOUNT_TEMP A
                    JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                    JOIN T_SERVERPARTSHOP C ON A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPCODE = C.SHOPCODE
                  WHERE
                    A.VALID = 1 AND B.STATISTIC_TYPE = 1000 AND C.ISVALID = 1
                    AND A.STATISTICS_DATE >= TO_DATE('{st_date_str}', 'YYYY-MM-DD')
                    AND A.STATISTICS_DATE < TO_DATE('{st_date_str}', 'YYYY-MM-DD') + 1
                    AND B.SERVERPART_CODE NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}
                  GROUP BY
                    B.SPREGIONTYPE_NAME, B.SERVERPART_NAME, A.SERVERPART_ID, C.SHOPNAME, C.SHOPREGION,
                    C.BUSINESS_TRADENAME, C.BRAND_NAME, A.BUSINESS_TYPE, C.REVENUE_INCLUDE"""

    rows = db.execute_query(sql) or []
    results = []
    for row in rows:
        results.append({
            "Serverpart_ID": row.get("SERVERPART_ID"),
            "Serverpart_Name": row.get("SERVERPART_NAME", ""),
            "SPRegionType_Name": row.get("SPREGIONTYPE_NAME", ""),
            "ShopName": row.get("SHOPNAME", ""),
            "ShopRegionName": row.get("SHOPREGIONNAME", ""),
            "Business_TypeName": row.get("BUSINESS_TYPENAME", ""),
            "BusinessTrade_Name": row.get("BUSINESSTRADE_NAME", ""),
            "BusinessBrand_Name": row.get("BUSINESSBRAND_NAME", ""),
            "Statistics_Date": st_date.strftime("%Y-%m-%d 00:00:00"),
            "TicketCount": _si(row.get("TICKETCOUNT")),
            "TotalCount": _sf(row.get("TOTALCOUNT")),
            "TotalOffAmount": _sf(row.get("TOTALOFFAMOUNT")),
            "MobilePayment": _sf(row.get("MOBILEPAYMENT")),
            "CashPay": _sf(row.get("CASHPAY")),
            "Different_Price_Less": _sf(row.get("DIFFERENT_PRICE_LESS")),
            "Different_Price_More": _sf(row.get("DIFFERENT_PRICE_MORE")),
            "Revenue_Include": _si(row.get("REVENUE_INCLUDE")) if revenue_include == 1 else 0,
            "BusinessType": None, "Revenue_Upload": row.get("REVENUE_UPLOAD"),
            "TotalShopCount": None, "RevenueQOQ": None, "RevenueYOY": None,
            "YearRevenueAmount": None, "YearRevenueYOY": None, "BudgetRevenue": None,
            "CurAccountRoyalty": None, "AccountRoyaltyQOQ": None,
            "YearAccountRoyalty": 0.0, "YearAccountRoyaltyYOY": 0.0, "UnUpLoadShopList": None,
        })
    return results
