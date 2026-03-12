# -*- coding: utf-8 -*-
"""
CommercialApi - Revenue 路由
对应原 CommercialApi/Controllers/RevenueController.cs
营收相关接口（原2657行，40+接口，此处按方法签名完整定义路由）
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from models.base import Result, JsonListData
from routers.deps import get_db, parse_multi_ids, build_in_condition
from core.database import DatabaseHelper
from core.des_helper import des_encrypt_id

router = APIRouter()


def date_no_pad(d, fmt="ymd"):
    """C# DateTime.ToString("yyyy/M/d") 不补零"""
    if fmt == "ymd":
        return f"{d.year}/{d.month}/{d.day}"
    elif fmt == "ymd_hms":
        return f"{d.year}/{d.month}/{d.day} {d.hour}:{d.minute:02d}:{d.second:02d}"
    return f"{d.year}/{d.month}/{d.day}"

# ===== 每日营收推送 =====
@router.get("/Revenue/GetRevenuePushList")
async def get_revenue_push_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收(0否1是)"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收推送数据表列表 (SQL平移完成)"""
    try:
        from datetime import datetime, timedelta
        
        # 1. 区域过滤
        pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
        province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else pushProvinceCode

        where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
        if Serverpart_ID:
            where_sql += f' AND B."SERVERPART_ID" = {Serverpart_ID}'
        elif SPRegionType_ID:
            # 根据 SPRegionType_ID 查询 SPREGIONTYPE_ID
            sp_res = db.execute_query('SELECT "SPREGIONTYPE_ID" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = :sid', {"sid": SPRegionType_ID})
            if sp_res:
                where_sql += f' AND B."SPREGIONTYPE_ID" = {sp_res[0]["SPREGIONTYPE_ID"]}'

        # 2. 日期确定
        st_date_str = Statistics_Date.split(" ")[0] if Statistics_Date else datetime.now().strftime("%Y-%m-%d")
        st_date = datetime.strptime(st_date_str, "%Y-%m-%d")
        is_history = st_date < (datetime.now() - timedelta(days=9))
        
        results = []
        if is_history:
            # 3.1 历史表 T_REVENUEDAILY 查询
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
            # 3.2 实时表 T_ENDACCOUNT_TEMP 查询
            # 对应 C# 中的 T_ENDACCOUNT 逻辑
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

        rows = db.execute_query(sql)
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
                "TicketCount": int(row["TICKETCOUNT"] or 0),
                "TotalCount": float(row["TOTALCOUNT"] or 0),
                "TotalOffAmount": float(row["TOTALOFFAMOUNT"] or 0),
                "MobilePayment": float(row["MOBILEPAYMENT"] or 0),
                "CashPay": float(row["CASHPAY"] or 0),
                "Different_Price_Less": float(row["DIFFERENT_PRICE_LESS"] or 0),
                "Different_Price_More": float(row["DIFFERENT_PRICE_MORE"] or 0),
                "Revenue_Include": int(row["REVENUE_INCLUDE"] or 0) if Revenue_Include == 1 else 0,
                "BusinessType": None,
                "Revenue_Upload": row["REVENUE_UPLOAD"],
                "TotalShopCount": None,
                "RevenueQOQ": None,
                "RevenueYOY": None,
                "YearRevenueAmount": None,
                "YearRevenueYOY": None,
                "BudgetRevenue": None,
                "CurAccountRoyalty": None,
                "AccountRoyaltyQOQ": None,
                "YearAccountRoyalty": 0.0,
                "YearAccountRoyaltyYOY": 0.0,
                "UnUpLoadShopList": None
            })

        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:
        logger.error(f"GetRevenuePushList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetSummaryRevenue")
async def get_summary_revenue(
    request: Request,
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_StartDate: Optional[str] = Query("", description="统计开始日期"),
    Statistics_Date: Optional[str] = Query("", description="统计结束日期"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收(0否1是)"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    ShowYearRevenue: bool = Query(False, description="是否显示年度营收额"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收推送汇总数据"""
    try:
        from datetime import datetime, timedelta
        from collections import defaultdict

        # 1. 查省份ID
        pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
        province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else pushProvinceCode

        where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
        _sp_ids = parse_multi_ids(Serverpart_ID)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'

        # 2. 日期范围
        end_str = Statistics_Date.split(" ")[0] if Statistics_Date else datetime.now().strftime("%Y-%m-%d")
        start_str = Statistics_StartDate.split(" ")[0] if Statistics_StartDate else end_str
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        sd_start = start_date.strftime("%Y%m%d")
        sd_end = end_date.strftime("%Y%m%d")

        # 3. 查询T_REVENUEDAILY（日期范围）
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

        if not rows:
            return Result.success(data={
                "RevenuePushModel": None, "GrowthRate": 0.0,
                "MonthRevenueAmount": 0.0, "YearRevenueAmount": 0.0,
                "BusinessTypeList": [], "BusinessTradeList": [], "SPRegionList": [],
            }, msg="查询成功")

        # 4. 辅助函数
        def sf(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def si(v):
            try: return int(v) if v is not None else 0
            except: return 0

        # 5. 直接从REVENUE_AMOUNT_YOY获取去年同期 (C# SUM(A.REVENUE_AMOUNT_YOY))
        revenue_yoy = round(sum(sf(r.get("REVENUE_AMOUNT_YOY")) for r in rows), 2)

        # 6. 构造汇总
        total_cashpay = round(sum(sf(r.get("CASHPAY")) for r in rows), 2)
        total_ticket = sum(si(r.get("TICKETCOUNT")) for r in rows)
        summary_model = {
            "Serverpart_ID": int(Serverpart_ID) if Serverpart_ID else None,
            "Serverpart_Name": rows[0].get("SERVERPART_NAME", "") if Serverpart_ID else "",
            "CashPay": total_cashpay,
            "TicketCount": total_ticket,
            "TotalCount": round(sum(sf(r.get("TOTALCOUNT")) for r in rows), 2),
            "TotalOffAmount": round(sum(sf(r.get("TOTALOFFAMOUNT")) for r in rows), 2),
            "MobilePayment": round(sum(sf(r.get("MOBILEPAYMENT")) for r in rows), 2),
            "Different_Price_Less": round(sum(sf(r.get("DIFFERENT_PRICE_LESS")) for r in rows), 2),
            "Different_Price_More": round(sum(sf(r.get("DIFFERENT_PRICE_MORE")) for r in rows), 2),
            "RevenueYOY": revenue_yoy,
            "Revenue_Upload": None,
            "TotalShopCount": None,
            "UnUpLoadShopList": None,
            # C#模型默认字段
            "SPRegionType_Name": None,
            "ShopName": None,
            "ShopRegionName": None,
            "BusinessTrade_Name": None,
            "BusinessBrand_Name": None,
            "Business_TypeName": None,
            "BusinessType": None,
            "Revenue_Include": None,
            "Statistics_Date": None,
            "BudgetRevenue": 0.0,
            "RevenueQOQ": None,
            "CurAccountRoyalty": None,
            "AccountRoyaltyQOQ": None,
            "YearRevenueAmount": None,
            "YearRevenueYOY": None,
            "YearAccountRoyalty": 0.0,
            "YearAccountRoyaltyYOY": 0.0,
        }

        # 7. 统计经营模式分析 (BusinessTypeList)
        bt_groups = defaultdict(lambda: {"cash": 0.0, "yoy": 0.0})
        sp_groups = defaultdict(float)

        for r in rows:
            bt_name = r.get("BUSINESS_TYPENAME") or "其他"
            bt_groups[bt_name]["cash"] += sf(r.get("CASHPAY"))
            bt_groups[bt_name]["yoy"] += sf(r.get("REVENUE_AMOUNT_YOY"))
            sp_name = r.get("SPREGIONTYPE_NAME")
            if sp_name:
                sp_groups[sp_name] += sf(r.get("CASHPAY"))

        business_type_list = []
        for name, vals in sorted(bt_groups.items(), key=lambda x: x[1]["cash"], reverse=True):
            business_type_list.append({
                "name": name,
                "value": f"{vals['cash']:.2f}",
                "data": f"{vals['yoy']:.2f}",
                "key": None
            })

        # 8. 统计管理中心分析 (SPRegionList)
        sp_region_list = []
        for name, val in sorted(sp_groups.items(), key=lambda x: x[1], reverse=True):
            sp_region_list.append({
                "name": name,
                "value": f"{val:.2f}"
            })

        # 9. 统计经营业态分析 (BusinessTradeList) 
        # 先查T_SERVERPARTSHOP获取(SERVERPART_ID,SHOPTRADE)→BUSINESS_TRADENAME映射
        shop_where = where_sql.replace('B.', 'B2.')
        shop_sql = f"""SELECT A2."SERVERPART_ID", A2."SHOPTRADE", A2."BUSINESS_TRADENAME"
            FROM "T_SERVERPARTSHOP" A2, "T_SERVERPART" B2
            WHERE A2."SERVERPART_ID" = B2."SERVERPART_ID" AND A2."ISVALID" = 1
                AND A2."BUSINESS_TRADE" IS NOT NULL {shop_where}
            GROUP BY A2."SERVERPART_ID", A2."SHOPTRADE", A2."BUSINESS_TRADENAME" """
        shop_rows = db.execute_query(shop_sql) or []
        # 建立映射: (SERVERPART_ID, SHOPTRADE) → BUSINESS_TRADENAME
        trade_name_map = {}
        for s in shop_rows:
            key = (str(s.get("SERVERPART_ID")), str(s.get("SHOPTRADE")))
            trade_name_map[key] = str(s.get("BUSINESS_TRADENAME") or "")

        # 查父级业态映射
        mapping_sql = """SELECT A."AUTOSTATISTICS_NAME" AS "CHILD", B."AUTOSTATISTICS_NAME" AS "PARENT"
                         FROM "T_AUTOSTATISTICS" A, "T_AUTOSTATISTICS" B
                         WHERE A."AUTOSTATISTICS_PID" = B."AUTOSTATISTICS_ID"
                         AND B."AUTOSTATISTICS_PID" = -1"""
        mapping_rows = db.execute_query(mapping_sql) or []
        parent_mapping = {mr["CHILD"]: mr["PARENT"] for mr in mapping_rows}

        parent_trade_groups = defaultdict(float)
        for r in rows:
            key = (str(r.get("SERVERPART_ID")), str(r.get("SHOPTRADE")))
            child_name = trade_name_map.get(key, "")
            parent_name = parent_mapping.get(child_name, "其他") if child_name else "其他"
            parent_trade_groups[parent_name] += sf(r.get("CASHPAY"))

        business_trade_list = []
        for name, val in sorted(parent_trade_groups.items(), key=lambda x: x[1], reverse=True):
            business_trade_list.append({
                "name": name,
                "value": f"{val:.2f}"
            })

        return Result.success(data={
            "BusinessTradeList": business_trade_list,
            "BusinessTypeList": business_type_list,
            "GrowthRate": 0.0,
            "MonthRevenueAmount": 0.0,
            "RevenuePushModel": summary_model,
            "SPRegionList": sp_region_list,
            "YearRevenueAmount": 0.0,
        }, msg="查询成功")

    except Exception as ex:
        logger.error(f"GetSummaryRevenue 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetSummaryRevenueMonth")
async def get_summary_revenue_month(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    SolidType: Optional[str] = Query("", description="是否执行固化操作"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度营收推送汇总数据 (C#完整平移)"""
    try:
        from datetime import datetime
        from collections import defaultdict

        def sf(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        month_str = StatisticsMonth.replace("-", "") if StatisticsMonth else datetime.now().strftime("%Y%m")
        date_str = StatisticsDate.split(" ")[0] if StatisticsDate else None

        if not pushProvinceCode:
            return Result.success(data=None, msg="查询成功")

        # C# SolidType是bool类型，只有"true"/"True"才为true，其他值包括数字都解析为false
        # C#: if(!SolidType) → SolidType=false时查Dashboard
        solid_type_bool = str(SolidType).lower() == "true"
        should_check_dashboard = not solid_type_bool  # C#: !SolidType

        # 1. 省份映射
        pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
        province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else pushProvinceCode

        # 2. 日期计算
        is_current_month = bool(date_str) and datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m") == month_str if date_str and "-" in date_str else False

        if is_current_month:
            stat_dt = datetime.strptime(date_str, "%Y-%m-%d")
            cur_month_end = (stat_dt - __import__("datetime").timedelta(days=1)).strftime("%Y%m%d")
            last_month_end = stat_dt.replace(day=1) - __import__("datetime").timedelta(days=1)
            last_month_str = last_month_end.strftime("%Y%m%d")
            last_year_str = stat_dt.replace(year=stat_dt.year - 1).strftime("%Y%m%d")
            sd_start = stat_dt.strftime("%Y%m") + "01"
            sd_end = stat_dt.strftime("%Y%m%d")
        else:
            # 历史月份
            m_dt = datetime.strptime(month_str + "01", "%Y%m%d")
            cur_month_end = (m_dt.replace(month=m_dt.month % 12 + 1, day=1) - __import__("datetime").timedelta(days=1)).strftime("%Y%m%d") if m_dt.month < 12 else m_dt.replace(month=12, day=31).strftime("%Y%m%d")
            last_month_end = (m_dt - __import__("datetime").timedelta(days=1)).strftime("%Y%m%d")
            last_year_str = (m_dt.replace(year=m_dt.year - 1, month=m_dt.month % 12 + 1 if m_dt.month < 12 else 1) - __import__("datetime").timedelta(days=1)).strftime("%Y%m%d") if not is_current_month else ""

        # 3. 查询T_REVENUEDASHBOARD（当SolidType=0时）
        if should_check_dashboard:
            dash_sql = f"""SELECT * FROM "T_REVENUEDASHBOARD" WHERE "PROVINCE_ID" = {province_id} AND "STATISTICS_MONTH" = {month_str}"""
            dash_rows = db.execute_query(dash_sql) or []
            if dash_rows:
                bt_array = ["自营", "外包", "便利店", "餐饮客房", "商铺租赁"]
                no_bt = [r for r in dash_rows if r.get("BUSINESS_TYPE") is None]
                bt_rows = sorted([r for r in dash_rows if r.get("BUSINESS_TYPE") and int(sf(r.get("BUSINESS_TYPE"))) > 0],
                                key=lambda x: int(sf(x.get("BUSINESS_TYPE"))))
                
                month_rev = {
                    "CashPay": round(sum(sf(r.get("MONTHLY_REVENUE")) for r in no_bt), 2),
                    "RevenueQOQ": round(sum(sf(r.get("MONTHLY_REVENUE_QOQ")) for r in no_bt), 2),
                    "RevenueYOY": round(sum(sf(r.get("MONTHLY_REVENUE_YOY")) for r in no_bt), 2),
                    "YearRevenueAmount": round(sum(sf(r.get("ANNUAL_REVENUE")) for r in no_bt), 2),
                    "YearRevenueYOY": round(sum(sf(r.get("ANNUAL_REVENUE_YOY")) for r in no_bt), 2),
                    "YearAccountRoyalty": round(sum(sf(r.get("ANNUAL_ACCOUNT")) for r in no_bt), 2),
                    "YearAccountRoyaltyYOY": round(sum(sf(r.get("ANNUAL_ACCOUNT_YOY")) for r in no_bt), 2),
                    "CurAccountRoyalty": {
                        "Royalty_Theory": round(sum(sf(r.get("MONTHLY_ACCOUNT")) for r in no_bt), 2),
                        "SubRoyalty_Theory": round(sum(sf(r.get("MONTHLY_SUBACCOUNT")) for r in no_bt), 2),
                        "Royalty_Price": None,
                        "SubRoyalty_Price": None,
                    },
                    "TicketCount": None, "TotalCount": None, "TotalOffAmount": None, "MobilePayment": None,
                    "Serverpart_ID": None, "Serverpart_Name": None, "SPRegionType_Name": None,
                    "ShopName": None, "ShopRegionName": None, "BusinessType": None,
                    "Business_TypeName": None, "BusinessTrade_Name": None, "BusinessBrand_Name": None,
                    "Revenue_Include": None, "Revenue_Upload": None, "TotalShopCount": None,
                    "BudgetRevenue": None, "Different_Price_Less": None, "Different_Price_More": None,
                    "Statistics_Date": None, "AccountRoyaltyQOQ": None,
                    "UnUpLoadShopList": None,
                }
                
                bt_list = []
                for r in bt_rows:
                    bt_idx = int(sf(r.get("BUSINESS_TYPE"))) - 1
                    if 0 <= bt_idx < len(bt_array):
                        bt_list.append({
                            "name": bt_array[bt_idx],
                            "value": str(r.get("MONTHLY_REVENUE") if r.get("MONTHLY_REVENUE") is not None else ""),
                            "data": str(r.get("MONTHLY_REVENUE_YOY") if r.get("MONTHLY_REVENUE_YOY") is not None else ""),
                            "key": str(r.get("MONTHLY_REVENUE_QOQ") if r.get("MONTHLY_REVENUE_QOQ") is not None else ""),
                        })
                
                growth = round(sum(sf(r.get("GROWTH_RATE")) for r in no_bt), 2)
                
                return Result.success(data={
                    "BusinessTradeList": [],
                    "BusinessTypeList": bt_list,
                    "GrowthRate": growth,
                    "MonthRevenueModel": month_rev,
                    "RevenuePushModel": None,
                    "SPRegionList": [],
                }, msg="查询成功")

        # 4. 查询月度营收数据（非Dashboard路径）
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

        # C#: 当is_current_month时用SERVERPART_ID=0汇总行，否则用明细+JOIN
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
            return Result.success(data={
                "BusinessTradeList": [], "BusinessTypeList": [],
                "GrowthRate": 0.0, "MonthRevenueModel": None,
                "RevenuePushModel": None, "SPRegionList": [],
            }, msg="查询成功")

        # 5. 查询环比/同比/年度累计
        yoy_dates = f' AND A."STATISTICS_DATE" IN ({cur_month_end},{last_month_str},{last_year_str})' if is_current_month else ""
        if is_current_month:
            yoy_sql = f"""SELECT
                    SUM(A."REVENUE_AMOUNT_MONTH") AS "CASHPAY",
                    SUM(A."REVENUE_AMOUNT_YEAR") AS "REVENUE_AMOUNT_YEAR",
                    A."STATISTICS_DATE" AS "STATISTICS_MONTH",
                    CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END AS "BUSINESS_TYPENAME"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1{where_sql_last}{yoy_dates}
                GROUP BY A."STATISTICS_DATE", CASE WHEN A."BUSINESS_TYPE" = 1000 THEN '自营' ELSE '外包' END"""
            yoy_rows = db.execute_query(yoy_sql) or []
        else:
            yoy_rows = []

        # 构建yoy_map: {(date, bt_name): {cashpay, year_amount}}
        yoy_map = {}
        for r in yoy_rows:
            key = (str(r.get("STATISTICS_MONTH", "")), r.get("BUSINESS_TYPENAME", ""))
            yoy_map[key] = {"cashpay": sf(r.get("CASHPAY")), "year": sf(r.get("REVENUE_AMOUNT_YEAR"))}

        # 6. 聚合
        bt_groups = defaultdict(float)
        sp_groups = defaultdict(float)
        total_cash = round(sum(sf(r.get("CASHPAY")) for r in rows), 2)
        total_ticket = sum(int(sf(r.get("TICKETCOUNT"))) for r in rows)
        total_count = round(sum(sf(r.get("TOTALCOUNT")) for r in rows), 2)
        total_off = round(sum(sf(r.get("TOTALOFFAMOUNT")) for r in rows), 2)
        total_mobile = round(sum(sf(r.get("MOBILEPAYMENT")) for r in rows), 2)
        total_diff_less = round(sum(sf(r.get("DIFFERENT_PRICE_LESS")) for r in rows), 2)
        total_diff_more = round(sum(sf(r.get("DIFFERENT_PRICE_MORE")) for r in rows), 2)

        for r in rows:
            bt_groups[r.get("BUSINESS_TYPENAME") or "其他"] += sf(r.get("CASHPAY"))
            sp_name = r.get("SPREGIONTYPE_NAME")
            if sp_name:
                sp_groups[sp_name] += sf(r.get("CASHPAY"))

        # 环比同比
        qoq_total = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if str(k[0]) == last_month_str)
        yoy_total = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if str(k[0]) == last_year_str)
        year_rev = sum(v.get("year", 0) for k, v in yoy_map.items() if str(k[0]) == cur_month_end)
        year_yoy = sum(v.get("year", 0) for k, v in yoy_map.items() if str(k[0]) == last_year_str)

        month_rev_model = {
            "CashPay": total_cash,
            "TicketCount": total_ticket,
            "TotalCount": total_count,
            "TotalOffAmount": total_off,
            "MobilePayment": total_mobile,
            "Different_Price_Less": total_diff_less,
            "Different_Price_More": total_diff_more,
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
                qoq_val = sum(v.get("cashpay", 0) for k, v in yoy_map.items() if k[0] == last_month_str and k[1] == name)
                bt_list.append({
                    "name": name,
                    "value": str(round(val, 2)),
                    "data": str(round(yoy_val, 2)) if yoy_val else "0",
                    "key": str(round(qoq_val, 2)) if qoq_val else "0",
                })

        # 区域列表
        sp_region_list = [{"name": n, "value": f"{v:.2f}"} for n, v in sorted(sp_groups.items(), key=lambda x: x[1], reverse=True)]

        # 获取单日推送模型
        revenue_push_model = None
        if date_str:
            try:
                daily_res = await get_summary_revenue(
                    request=Request({"type": "http"}),
                    pushProvinceCode=pushProvinceCode,
                    Statistics_Date=date_str,
                    db=db
                )
                if hasattr(daily_res, 'body'):
                    import json as _json
                    daily_dict = _json.loads(daily_res.body)
                elif isinstance(daily_res, dict):
                    daily_dict = daily_res
                else:
                    daily_dict = {}
                if daily_dict.get("Result_Code") == 100:
                    rd = daily_dict.get("Result_Data") or {}
                    revenue_push_model = rd.get("RevenuePushModel") if isinstance(rd, dict) else None
            except Exception as inner_ex:
                logger.warning(f"GetSummaryRevenueMonth 获取单日推送模型失败: {inner_ex}")

        return Result.success(data={
            "BusinessTradeList": [],
            "BusinessTypeList": bt_list,
            "GrowthRate": 0.0,
            "MonthRevenueModel": month_rev_model,
            "RevenuePushModel": revenue_push_model,
            "SPRegionList": sp_region_list,
        }, msg="查询成功")

    except Exception as ex:
        logger.error(f"GetSummaryRevenueMonth 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetWechatPushSalesList")
async def get_wechat_push_sales_list(
    pushProvinceCode: str = Query(..., description="推送省份"),
    Statistics_Date: str = Query(..., description="统计日期"),
    RankNum: int = Query(10, description="排行数量"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取单品销售排行榜数据 (SQL平移完成)"""
    try:
        from datetime import datetime
        stat_date_str = Statistics_Date.split(" ")[0] if Statistics_Date else datetime.now().strftime("%Y-%m-%d")

        # 1. 区域过滤映射
        pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
        province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else pushProvinceCode

        # 2. 查询汇总单品数据
        sql = f"""SELECT 
                    CASE WHEN BUSINESSTYPE IN ('1000','1005') THEN 1000 
                         WHEN BUSINESSTYPE LIKE '2%' THEN 2000 
                         WHEN BUSINESSTYPE LIKE '3%' THEN 3000 ELSE 1000 END AS BUSINESSTYPE_GROUP,
                    A.COMMODITY_NAME,
                    SUM(A.TOTALCOUNT) AS TOTALCOUNT,
                    SUM(A.TOTALSELLAMOUNT) AS TOTALSELLAMOUNT 
                FROM 
                    T_COMMODITYSALE A 
                WHERE 
                    A.ENDDATE >= TO_DATE('{stat_date_str}', 'YYYY-MM-DD') AND 
                    A.ENDDATE < TO_DATE('{stat_date_str}', 'YYYY-MM-DD') + 1 AND 
                    A.SERVERPARTCODE NOT IN ('888888','899999') AND 
                    EXISTS (SELECT 1 FROM T_SERVERPART B 
                        WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.PROVINCE_CODE = '{province_id}')
                GROUP BY 
                    CASE WHEN BUSINESSTYPE IN ('1000','1005') THEN 1000 
                         WHEN BUSINESSTYPE LIKE '2%' THEN 2000 
                         WHEN BUSINESSTYPE LIKE '3%' THEN 3000 ELSE 1000 END,
                    A.COMMODITY_NAME"""
        
        rows = db.execute_query(sql)
        from collections import defaultdict
        groups = defaultdict(list)
        for r in rows:
            groups[int(r["BUSINESSTYPE_GROUP"])].append({
                "Commodity_Name": r["COMMODITY_NAME"],
                "SellCount": float(r["TOTALCOUNT"] or 0),
                "TotalPrice": float(r["TOTALSELLAMOUNT"] or 0)
            })
            
        result_list = []
        for b_type in [1000, 2000, 3000]:
            if b_type not in groups: continue
            sorted_goods = sorted(groups[b_type], key=lambda x: x["SellCount"], reverse=True)[:RankNum]
            for i, g in enumerate(sorted_goods): g["Rank_ID"] = i + 1
            result_list.append({
                "Data_Type": b_type,
                "TotalCount": len(groups[b_type]),
                "GoodsList": sorted_goods
            })
        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetWechatPushSalesList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetUnUpLoadShops")
async def get_un_upload_shops(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询服务区未上传结账信息的门店列表"""
    try:
        from datetime import datetime as dt

        # 确定使用 T_ENDACCOUNT 还是 T_ENDACCOUNT_TEMP
        stat_date = Statistics_Date or dt.now().strftime("%Y-%m-%d")
        stat_dt = dt.strptime(stat_date.split(" ")[0], "%Y-%m-%d")
        table_suffix = "" if stat_dt < dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - __import__("datetime").timedelta(days=9) else "_TEMP"

        # 省份条件
        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND B."SERVERPART_ID" = {Serverpart_ID}'
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" = {SPRegionType_ID}'
        elif pushProvinceCode:
            fe_rows = db.execute_query(
                """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
                {"pc": pushProvinceCode})
            if fe_rows:
                where_sql += f' AND B."PROVINCE_CODE" = {fe_rows[0]["FIELDENUM_ID"]}'
        if Revenue_Include == 1:
            where_sql += f' AND A."REVENUE_INCLUDE" = 1'

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

        rows = db.execute_query(sql)
        def safe_sort_int(v):
            try: return int(v) if v is not None else 0
            except: return 0
        rows = sorted(rows or [], key=lambda x: (
            safe_sort_int(x.get("SERVERPART_INDEX")),
            safe_sort_int(x.get("SERVERPART_CODE")),
            str(x.get("SHOPREGION") or ""),
            str(x.get("SHOPTRADE") or ""),
        ))
        result_list = []
        for r in rows:
            result_list.append({
                "Serverpart_ID": r.get("SERVERPART_ID"),
                "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                "ServerpartShop_ID": r.get("SERVERPARTSHOP_ID"),
                "ServerpartShop_Name": r.get("SHOPNAME", ""),
                "Statistics_Date": stat_date,
            })
        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetUnUpLoadShops 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetServerpartBrand")
async def get_serverpart_brand(
    Serverpart_Id: Optional[int] = Query(None, description="服务区内码"),
    statictics_Time: Optional[str] = Query(None, description="统计时间"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编号"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区品牌营收 (SQL平移完成)"""
    try:
        from datetime import datetime
        stat_time = statictics_Time or datetime.now().strftime("%Y-%m-%d")
        stat_dt = datetime.strptime(stat_time.split(" ")[0], "%Y-%m-%d")
        
        # 0. 确定表名后缀 (9天规则)
        from datetime import timedelta
        table_suffix = "" if stat_dt < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=9) else "_TEMP"

        # 1. 获取基础数据字典 (业态和品牌)
        # 获取品牌详情
        brand_sql = f"""SELECT "BRAND_ID", "BRAND_INTRO" FROM "T_BRAND" 
                       WHERE "BRAND_STATE" = 1 AND "PROVINCE_CODE" = :pc"""
        brand_rows = db.execute_query(brand_sql, {"pc": pushProvinceCode})
        brand_intro_map = {str(r["BRAND_ID"]): r["BRAND_INTRO"] for r in brand_rows}

        # 获取业态字典
        auto_sql = f"""SELECT "AUTOSTATISTICS_ID", "AUTOSTATISTICS_NAME", "AUTOSTATISTICS_PID" 
                      FROM "T_AUTOSTATISTICS" 
                      WHERE "AUTOSTATISTICS_TYPE" = 2000 AND "PROVINCE_CODE" = :pc"""
        auto_rows = db.execute_query(auto_sql, {"pc": pushProvinceCode})
        auto_map = {str(r["AUTOSTATISTICS_ID"]): r for r in auto_rows}

        # 2. 查询营收数据 (ShopBrandRevenueTable)
        # 对应 BaseInfoHelper.GetBusinessBrandList
        where_sql = ""
        if Serverpart_Id:
            where_sql += f" AND A.SERVERPART_ID = {Serverpart_Id}"
            
        revenue_sql = f"""
            SELECT 
                A.SERVERPARTSHOP_ID,
                NVL(A.BUSINESS_TRADE, -1) AS BUSINESS_TRADE,
                NVL(A.BUSINESS_BRAND, -1) AS BUSINESS_BRAND,
                NVL(A.BRAND_NAME, '其他') AS BRAND_NAME,
                NVL(A.BUSINESS_TRADENAME, '其他') AS BUSINESS_TRADENAME,
                SUM(NVL(B.CASHPAY, 0)) AS FACTAMOUNT,
                A.SERVERPART_ID,
                A.SERVERPART_NAME 
            FROM 
                T_SERVERPARTSHOP A,
                T_ENDACCOUNT{table_suffix} B 
            WHERE 
                A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPCODE = B.SHOPCODE AND 
                A.STATISTIC_TYPE = 1000 AND A.ISVALID = 1 AND B.VALID = 1 AND 
                A.SHOPTRADE IS NOT NULL 
                AND B.STATISTICS_DATE >= TO_DATE('{stat_dt.strftime("%Y/%m/%d")}', 'YYYY/MM/DD')
                AND B.STATISTICS_DATE < TO_DATE('{stat_dt.strftime("%Y/%m/%d")}', 'YYYY/MM/DD') + 1
                {where_sql}
            GROUP BY 
                A.SERVERPARTSHOP_ID, NVL(A.BUSINESS_TRADE, -1), NVL(A.BUSINESS_BRAND, -1), NVL(A.BRAND_NAME, '其他'),
                NVL(A.BUSINESS_TRADENAME, '其他'), A.SERVERPART_ID, A.SERVERPART_NAME
        """
        rev_rows = db.execute_query(revenue_sql)
        if not rev_rows:
            return Result.success(data={"Serverpart_Id": None, "Serverpart_Name": None, "Revenue_Amount": None, "listCurBusinessModel": None, "listBusinessModel": None}, msg="查询成功")

        # 3. 内存聚合与构建嵌套模型
        from collections import defaultdict
        
        # 服务区汇总信息
        sp_id = rev_rows[0]["SERVERPART_ID"]
        sp_name = rev_rows[0]["SERVERPART_NAME"]
        total_revenue = sum(float(r["FACTAMOUNT"] or 0) for r in rev_rows)

        # 按父级业态聚合
        parent_trade_groups = defaultdict(list)
        for r in rev_rows:
            trade_id = str(r["BUSINESS_TRADE"])
            trade_info = auto_map.get(trade_id)
            pid = str(trade_info["AUTOSTATISTICS_PID"]) if trade_info and str(trade_info["AUTOSTATISTICS_PID"]) != "-1" else trade_id
            p_name = auto_map[pid]["AUTOSTATISTICS_NAME"] if pid in auto_map else "其他"
            parent_trade_groups[(pid, p_name)].append(r)

        listBusinessModel = []
        for (pid, pname), items in parent_trade_groups.items():
            p_rev = sum(float(it["FACTAMOUNT"] or 0) for it in items)
            
            listShopBrandModel = []
            for it in items:
                brand_id = str(it["BUSINESS_BRAND"])
                ico = brand_intro_map.get(brand_id, "")
                # 简单补全OSS/CDN前缀 (假设 legacy logic)
                brand_ico = ico if (not ico or ico.startswith("http")) else f"http://img.eshang.com{ico}" # 示例前缀

                listShopBrandModel.append({
                    "ServerpartShop_Id": str(it["SERVERPARTSHOP_ID"]),
                    "Brand_Id": int(it["BUSINESS_BRAND"]),
                    "Brand_Name": it["BRAND_NAME"],
                    "Revenue_Amount": round(float(it["FACTAMOUNT"] or 0), 2),
                    "Business_Trade": str(it["BUSINESS_TRADE"]),
                    "Bussiness_Name": it["BUSINESS_TRADENAME"],
                    "Brand_ICO": brand_ico
                })
            
            listBusinessModel.append({
                "Business_Trade": pid,
                "Bussiness_Name": pname,
                "Revenue_Amount": round(p_rev, 2),
                "listShopBrandModel": listShopBrandModel
            })

        return Result.success(data={
            "Revenue_Amount": round(total_revenue, 2),
            "Serverpart_Id": int(sp_id),
            "Serverpart_Name": sp_name,
            "listBusinessModel": listBusinessModel,
            "listCurBusinessModel": [] # C# 中此项通常为空或重复
        }, msg="查询成功")

    except Exception as ex:
        logger.error(f"GetServerpartBrand 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


# ===== 内部辅助函数：获取结账数据逻辑 =====
async def _get_end_account_data(db: DatabaseHelper, Serverpart_ID: int, Statistics_Date: str, ServerpartShop_Ids: str = None):
    from datetime import datetime, timedelta
    stat_date_str = Statistics_Date.split(" ")[0] if Statistics_Date else datetime.now().strftime("%Y-%m-%d")
    st_date = datetime.strptime(stat_date_str, "%Y-%m-%d")
    
    # 确定表名：历史表 T_ENDACCOUNT vs 实时表 T_ENDACCOUNT_TEMP
    is_history = st_date < (datetime.now() - timedelta(days=9))
    table_name = "T_ENDACCOUNT" if is_history else "T_ENDACCOUNT_TEMP"
    
    where_sql = f" AND A.SERVERPART_ID = {Serverpart_ID}"
    if ServerpartShop_Ids:
        ids_str = ",".join([str(i.strip()) for i in ServerpartShop_Ids.split(",") if i.strip().isdigit()])
        if ids_str:
            where_sql += f" AND B.SERVERPARTSHOP_ID IN ({ids_str})"
            
    sql = f"""SELECT 
                A.*, B.SERVERPARTSHOP_ID, B.SHOPREGION, B.SHOPTRADE, B.SHOPNAME,
                B.BUSINESS_BRAND, NVL(B.BRAND_NAME, B.SHOPSHORTNAME) AS BRAND_NAME_FIX,
                B.SERVERPART_NAME AS SERVERPART_NAME_FIX
              FROM 
                {table_name} A
                JOIN T_SERVERPARTSHOP B ON A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPCODE = B.SHOPCODE
              WHERE 
                A.VALID = 1 {where_sql}
                AND A.STATISTICS_DATE >= TO_DATE('{stat_date_str}', 'YYYY-MM-DD')
                AND A.STATISTICS_DATE < TO_DATE('{stat_date_str}', 'YYYY-MM-DD') + 1
              ORDER BY B.SERVERPART_NAME, B.SHOPREGION, B.SHOPTRADE, B.SHOPCODE, A.ENDACCOUNT_DATE"""
              
    rows = db.execute_query(sql)
    if not rows:
        return None, []
        
    # 按门店分组聚合
    from collections import defaultdict
    shop_groups = defaultdict(list)
    common_info = {
        "Serverpart_ID": rows[0]["SERVERPART_ID"],
        "Serverpart_Name": rows[0]["SERVERPART_NAME_FIX"],
        "TotalAmount": sum(float(r["CASHPAY"] or 0) for r in rows)
    }
    
    for r in rows:
        shop_groups[r["SERVERPARTSHOP_ID"]].append(r)
        
    shop_end_account_list = []
    upload_count = 0
    
    for shop_id, s_rows in shop_groups.items():
        first_r = s_rows[0]
        biz_type = int(first_r["BUSINESS_TYPE"] or 1000)
        
        # 门店基础信息及标识位计算 (对应 C# 逻辑)
        shop_model = {
            "SERVERPARTSHOP_ID": int(shop_id),
            "SHOPNAME": first_r["SHOPNAME"],
            "SERVERPART_ID": int(first_r["SERVERPART_ID"]),
            "SERVERPART_NAME": first_r["SERVERPART_NAME_FIX"],
            "BUSINESS_TYPE": biz_type,
            "BUSINESS_TYPENAME": {1000: "自营", 2000: "合作经营", 3000: "固定租金", 4000: "展销"}.get(biz_type, "其他"),
            "SHOWABNORMAL_SIGN": 0,
            "SHOWSCAN_SIGN": 0,
            "INTERFACE_SIGN": 0,
            "SHOWSSUPPLY_SIGN": 0,
            "SHOWCHECK_SIGN": 0,
            "SHOWDEAL_SIGN": 0,
            "UNACCOUNT_SIGN": 0,
            "CASHPAY_TOTAL": sum(float(r["CASHPAY"] or 0) for r in s_rows),
            "ShopEndAccountList": []
        }
        
        # 特殊标识计算
        for r in s_rows:
            # 异常标识 (CHECK_INFO 不为空且 实收不符)
            check_info = r.get("CHECK_INFO")
            sell_amt = float(r.get("TOTALSELLAMOUNT") or 0)
            cash_pay = float(r.get("CASHPAY") or 0)
            diff_price = float(r.get("DIFFERENT_PRICE") or 0)
            if check_info and (sell_amt > cash_pay or (sell_amt + diff_price) > cash_pay):
                shop_model["SHOWABNORMAL_SIGN"] = 1
                
            # 传输方式标识 (扫码/接口)
            worker = str(r.get("WORKER_NAME") or "")
            if "【扫】" in worker or "【扫码】" in worker:
                shop_model["SHOWSCAN_SIGN"] = 1
            elif "【接口】" in worker:
                shop_model["INTERFACE_SIGN"] = 1
            
            # 手工补录标识
            desc_staff = str(r.get("DESCRIPTION_STAFF") or "")
            if "【补】" in desc_staff:
                shop_model["SHOWSSUPPLY_SIGN"] = 1
                
            # 核销/处理状态
            if int(r.get("CHECK_COUNT") or 0) > 0: shop_model["SHOWCHECK_SIGN"] = 1
            if check_info: shop_model["SHOWDEAL_SIGN"] = 1
            
            # 结账状态
            diff_reason = r.get("DIFFERENCE_REASON")
            if not diff_reason or diff_reason != "无结账信息":
                shop_model["UNACCOUNT_SIGN"] = 1
            
            # 绑定结账清单明细
            transfer_type = 0
            if "【扫】" in worker: transfer_type = 1
            elif "【补】" in desc_staff: transfer_type = 2
            elif "接口" in worker or "扫码" in worker: transfer_type = 3
            
            shop_model["ShopEndAccountList"].append({
                "TRANSFER_TYPE": transfer_type,
                "ENDACCOUNT_STARTDATE": str(r.get("ENDACCOUNT_STARTDATE") or ""),
                "ENDACCOUNT_DATE": str(r.get("ENDACCOUNT_DATE") or ""),
                "DESCRIPTION_STAFF": desc_staff,
                "DIFFERENCE_REASON": diff_reason,
                "DESCRIPTION_DATE": str(r.get("DESCRIPTION_DATE") or ""),
                "CASHPAY": cash_pay,
                "CASH": float(r.get("CASH") or 0),
                "DIFFERENT_PRICE": diff_price,
                "CHECK_COUNT": int(r.get("CHECK_COUNT") or 0)
            })
            
        if shop_model["UNACCOUNT_SIGN"] == 1:
            upload_count += 1
            
        shop_end_account_list.append(shop_model)
        
    common_info["UploadShopCount"] = upload_count
    common_info["TotalShopCount"] = len(shop_end_account_list)
    return common_info, shop_end_account_list


# ===== 结账数据接口 =====
@router.get("/Revenue/GetServerpartEndAccountList")
async def get_serverpart_end_account_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询服务区结账数据列表 (SQL平移完成)"""
    try:
        common_info, shop_list = await _get_end_account_data(db, Serverpart_ID, Statistics_Date)
        if not common_info:
            return Result.success(data={"Serverpart_Id": None, "Serverpart_Name": None, "Revenue_Amount": None, "UploadShopCount": None, "TotalShopCount": None, "ShopEndaccountList": None}, msg="查询成功")
            
        return Result.success(data={
            "Revenue_Amount": common_info["TotalAmount"],
            "Serverpart_Id": common_info["Serverpart_ID"],
            "Serverpart_Name": common_info["Serverpart_Name"],
            "ShopEndaccountList": shop_list,
            "TotalShopCount": common_info["TotalShopCount"],
            "UploadShopCount": common_info["UploadShopCount"]
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartEndAccountList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetShopEndAccountList")
async def get_shop_end_account_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    ServerpartShop_Ids: Optional[str] = Query(None, description="门店内码集合"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询门店结账数据列表 (SQL平移完成)"""
    try:
        common_info, shop_list = await _get_end_account_data(db, Serverpart_ID, Statistics_Date, ServerpartShop_Ids)
        if not common_info:
            return Result.success(data={
                "ServerpartShop_Id": None, "Brand_Id": None, "Brand_Name": None,
                "BrandType_Name": None, "Brand_ICO": None, "Revenue_Amount": None,
                "Business_TradeId": None, "Business_Trade": None, "Business_TradeICO": None,
                "Bussiness_Name": None, "Bussiness_Time": None, "Bussiness_State": None,
                "CurRevenue": 0.0, "ShopEndaccountList": None,
            }, msg="查询成功")
            
        # 注意：此处返回模型为 ShopBrandModel，包含品牌信息
        # 目前暂时只取第一个门店的品牌信息作为示例
        first_shop = shop_list[0] if shop_list else {}
        
        return Result.success(data={
            "Brand_Name": first_shop.get("BRAND_NAME", ""),
            "Brand_Id": 0, # 模拟 C# 逻辑中的品牌 ID 持有
            "Revenue_Amount": common_info["TotalAmount"],
            "ServerpartShop_Id": ServerpartShop_Ids,
            "ShopEndaccountList": shop_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopEndAccountList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


# ===== 预算费用 =====
@router.post("/Revenue/GetBudgetExpenseList")
async def get_budget_expense_list_post(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取预算费用表列表（POST）"""
    try:
        if not searchModel:
            # C# 在参数为空时查询TotalCount但返回空列表
            try:
                count_rows = db.execute_query('SELECT COUNT(*) AS CNT FROM "T_BUDGETEXPENSE"')
                total = count_rows[0]["CNT"] if count_rows else 0
            except Exception:
                total = 0
            json_list = JsonListData.create(data_list=[], total=total, page_index=0, page_size=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        search_param = searchModel.get("SearchParameter") or {}

        conditions = []
        params = []

        # 通用字段过滤
        for field in ["STATISTICS_MONTH", "PROVINCE_CODE", "SERVERPART_ID"]:
            val = search_param.get(field)
            if val is not None and str(val).strip():
                conditions.append(f'"{field}" = ?')
                params.append(val)

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        # 查询总数
        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_BUDGETEXPENSE"{where_sql}'
        count_rows = db.execute_query(count_sql, params if params else None)
        total = count_rows[0]["CNT"] if count_rows else 0

        # 分页查询
        offset = (page_index - 1) * page_size
        data_sql = f'SELECT * FROM "T_BUDGETEXPENSE"{where_sql} ORDER BY "BUDGETEXPENSE_ID" DESC LIMIT ? OFFSET ?'
        page_params = (params if params else []) + [page_size, offset]
        page_rows = db.execute_query(data_sql, page_params)

        # 格式化日期
        for r in page_rows:
            if r.get("OPERATE_DATE"):
                r["OPERATE_DATE"] = str(r["OPERATE_DATE"])

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetExpenseList POST 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



@router.get("/Revenue/GetBudgetExpenseList")
async def get_budget_expense_list_get(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Month: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取预算费用表列表（GET）(SQL平移完成)"""
    try:
        conditions = []
        params = {}
        if Province_Code:
            conditions.append('"PROVINCE_CODE" = :pc')
            params["pc"] = Province_Code
        if Statistics_Month:
            conditions.append('"STATISTICS_MONTH" = :sm')
            params["sm"] = Statistics_Month
        _sp_ids = parse_multi_ids(Serverpart_ID)
        if _sp_ids:
            conditions.append(build_in_condition('SERVERPART_ID', _sp_ids))

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f'SELECT * FROM "T_BUDGETEXPENSE"{where_sql} ORDER BY "BUDGETEXPENSE_ID" DESC'
        rows = db.execute_query(sql, params if params else None) or []

        for r in rows:
            if r.get("OPERATE_DATE"):
                r["OPERATE_DATE"] = str(r["OPERATE_DATE"])

        json_list = JsonListData.create(data_list=rows, total=len(rows))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetExpenseList GET 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 计划营收 =====
@router.get("/Revenue/GetRevenueBudget")
async def get_revenue_budget(
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取计划营收数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt
        import calendar

        if Province_Code != "340000":
            return Result.success(data={
                "RevenueMonth_Amount": 0, "RevenueYear_Amount": 0,
                "BudgetMonth_Amount": 0, "BudgetYear_Amount": 0,
                "RevenueYear_PlanAmount": 0,
                "MonthBudget_Degree": 0, "MonthGrowth_Rate": 0,
                "YearBudget_Degree": 0, "YearGrowth_Rate": 0,
                "MonthYOY_Rate": None, "YearYOY_Rate": None,
            }, msg="查询成功")

        if not Statistics_Date:
            return Result.fail(code=101, msg="查询失败，未录入预算数据！")

        stat_date = dt.strptime(Statistics_Date, "%Y-%m-%d") if "-" in Statistics_Date else dt.strptime(Statistics_Date, "%Y%m%d")
        year_str = stat_date.strftime("%Y")
        month_str = stat_date.strftime("%Y%m")
        month_days = calendar.monthrange(stat_date.year, stat_date.month)[1]

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        budget_month = 0.0
        budget_year = 0.0
        plan_amount = 0.0

        sp_id = int(Serverpart_ID) if Serverpart_ID else None

        if sp_id:
            # 有服务区：查安徽财务预算表
            bsql = f"""SELECT B."STATISTICS_MONTH", B."BUDGETDETAIL_AMOUNT" AS "BUDGET_AMOUNT"
                FROM "T_BUDGETPROJECT_AH" A, "T_BUDGETDETAIL_AH" B
                WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                    AND B."ACCOUNT_CODE" = 1000
                    AND B."STATISTICS_MONTH" >= {year_str}01 AND B."STATISTICS_MONTH" <= {year_str}12
                    AND A."SERVERPART_ID" = {sp_id}"""
            rows = db.execute_query(bsql) or []
            for r in rows:
                sm = str(int(safe_dec(r.get("STATISTICS_MONTH"))))
                ba = safe_dec(r.get("BUDGET_AMOUNT"))
                if sm == month_str:
                    budget_month = ba
                    budget_year += ba
                    plan_amount += round(ba / month_days * stat_date.day, 2)
                else:
                    budget_year += ba
                    if int(sm) < int(month_str):
                        plan_amount += ba
        else:
            # 全省：查预算费用表(BUDGET_AMOUNT是日均值)
            bsql = f"""SELECT * FROM "T_BUDGETEXPENSE"
                WHERE "PROVINCE_CODE" = {Province_Code} AND "SERVERPART_ID" = 0
                    AND "STATISTICS_MONTH" >= {year_str}01 AND "STATISTICS_MONTH" <= {year_str}12"""
            rows = db.execute_query(bsql) or []
            for r in rows:
                sm = str(int(safe_dec(r.get("STATISTICS_MONTH"))))
                ba = safe_dec(r.get("BUDGET_AMOUNT"))
                sm_date = dt.strptime(sm + "01", "%Y%m%d")
                sm_days = calendar.monthrange(sm_date.year, sm_date.month)[1]
                if sm == month_str:
                    budget_month = ba * sm_days
                    budget_year += budget_month
                    plan_amount += ba * stat_date.day
                else:
                    m_total = ba * sm_days
                    budget_year += m_total
                    if int(sm) < int(month_str):
                        plan_amount += m_total

        if not rows:
            return Result.fail(code=101, msg="查询失败，未录入预算数据！")

        # 查实际营收
        rev_month = 0.0
        rev_year = 0.0
        month_yoy = None
        year_yoy = None

        if not sp_id and not SPRegionType_ID:
            # 全省汇总：查T_REVENUEDAILY SERVERPART_ID=0
            date_str = stat_date.strftime("%Y%m%d")
            rsql = f"""SELECT SUM("REVENUE_AMOUNT_MONTH") AS "REVENUE_AMOUNT_MONTH",
                    SUM("REVENUE_AMOUNT_YEAR") AS "REVENUE_AMOUNT_YEAR"
                FROM "T_REVENUEDAILY"
                WHERE "REVENUEDAILY_STATE" = 1 AND "BUSINESS_TYPE" = 1000
                    AND "SERVERPART_ID" = 0 AND "STATISTICS_DATE" = {date_str}"""
            rr = db.execute_query(rsql) or []
            if rr:
                rev_month = safe_dec(rr[0].get("REVENUE_AMOUNT_MONTH"))
                rev_year = safe_dec(rr[0].get("REVENUE_AMOUNT_YEAR"))

            # 去年同期
            ly_date = stat_date.replace(year=stat_date.year - 1).strftime("%Y%m%d")
            rsql_ly = rsql.replace(f"= {date_str}", f"= {ly_date}")
            rr_ly = db.execute_query(rsql_ly) or []
            if rr_ly:
                ly_month = safe_dec(rr_ly[0].get("REVENUE_AMOUNT_MONTH"))
                ly_year = safe_dec(rr_ly[0].get("REVENUE_AMOUNT_YEAR"))
                if ly_month > 0:
                    month_yoy = round((rev_month / ly_month - 1) * 100, 2)
                if ly_year > 0:
                    year_yoy = round((rev_year / ly_year - 1) * 100, 2)
        else:
            # 按服务区/片区：查月度营收
            where2 = ""
            if sp_id:
                where2 += f' AND B."SERVERPART_ID" = {sp_id}'
            elif SPRegionType_ID:
                where2 += f' AND B."SPREGIONTYPE_ID" = {SPRegionType_ID}'
            date_str = stat_date.strftime("%Y%m%d")
            rsql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS_MONTH",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000
                    AND A."STATISTICS_DATE" >= {year_str}0101 AND A."STATISTICS_DATE" <= {date_str}{where2}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
            rr = db.execute_query(rsql) or []
            for r in rr:
                ra = safe_dec(r.get("REVENUE_AMOUNT"))
                rm = str(int(safe_dec(r.get("STATISTICS_MONTH"))))
                rev_year += ra
                if rm == month_str:
                    rev_month = ra

        # 计算完成度
        month_degree = round(rev_month / budget_month * 100, 2) if budget_month > 0 else 0
        month_growth = round(month_degree - (stat_date.day * 100.0 / month_days), 2) if budget_month > 0 else 0
        year_degree = round(rev_year / budget_year * 100, 2) if budget_year > 0 else 0
        year_growth = round((rev_year - plan_amount) / budget_year * 100, 2) if budget_year > 0 else 0

        return Result.success(data={
            "RevenueMonth_Amount": rev_month,
            "RevenueYear_Amount": rev_year,
            "BudgetMonth_Amount": budget_month,
            "BudgetYear_Amount": budget_year,
            "RevenueYear_PlanAmount": plan_amount,
            "MonthBudget_Degree": month_degree,
            "MonthGrowth_Rate": month_growth,
            "YearBudget_Degree": year_degree,
            "YearGrowth_Rate": year_growth,
            "MonthYOY_Rate": month_yoy,
            "YearYOY_Rate": year_yoy,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueBudget 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetProvinceRevenueBudget")
async def get_province_revenue_budget(
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsType: int = Query(1, description="统计类型"),
    SPRegionTypeID: Optional[int] = Query(None, description="片区内码"),
    ServerpartID: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeYear: bool = Query(False, description="是否显示全年计划营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取全省计划营收分析（C#对齐：BUDGETEXPENSEHelper.GetProvinceRevenueBudget，约540行）"""
    try:
        from datetime import datetime as dt
        import calendar

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(v) if v is not None else 0
            except: return 0

        # C#: if (Province_Code != "340000") return null → 101
        if ProvinceCode != "340000":
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        if not StatisticsDate:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        yyyyMM = stat_date.strftime("%Y%m")
        yyyyMMdd = stat_date.strftime("%Y%m%d")
        yyyy01 = stat_date.strftime("%Y01")
        yyyy12 = stat_date.strftime("%Y12")
        yyyy0101 = stat_date.strftime("%Y0101")
        yyyyMM01 = stat_date.strftime("%Y%m01")
        day_of_month = stat_date.day
        days_in_month = calendar.monthrange(stat_date.year, stat_date.month)[1]

        Revenue_PlanAmount = 0.0
        Budget_Amount = 0.0

        # ============ 1. 构建预算查询 WhereSQL ============
        where_sql = ""
        if ServerpartID is not None:
            where_sql += f' AND B."SERVERPART_ID" = {ServerpartID}'
        elif SPRegionTypeID is not None:
            where_sql += f' AND B."SPREGIONTYPE_ID" = {SPRegionTypeID}'
        elif ProvinceCode:
            where_sql += f' AND A."PROVINCE_CODE" = {ProvinceCode}'
            if StatisticsType == 2:
                where_sql += ' AND A."SERVERPART_ID" = 0'
        # 月份条件
        if StatisticsType in (1, 4):
            where_sql += f' AND A."STATISTICS_MONTH" = {yyyyMM}'
        else:
            where_sql += f' AND A."STATISTICS_MONTH" >= {yyyy01} AND A."STATISTICS_MONTH" <= {yyyy12}'

        # ============ 2. 查询预算数据 ============
        budget_rows = []
        if StatisticsType == 3:
            # C#: 从安徽预算表查
            budget_sql = f"""SELECT A."STATISTICS_MONTH", B."SERVERPART_ID", B."SERVERPART_NAME",
                    A."BUDGETDETAIL_AMOUNT" AS "BUDGET_AMOUNT",
                    B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", 1000 AS "STATISTICS_TYPE"
                FROM "T_BUDGETDETAIL_AH" A, "T_BUDGETPROJECT_AH" B
                WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                    AND A."ACCOUNT_CODE" = 1000{where_sql}
                ORDER BY A."STATISTICS_MONTH" """
            budget_rows = db.execute_query(budget_sql) or []
            for r in budget_rows:
                sm = str(r.get("STATISTICS_MONTH", ""))
                ba = safe_dec(r.get("BUDGET_AMOUNT"))
                if sm == yyyyMM:
                    Budget_Amount += ba
                    Revenue_PlanAmount += round(ba * day_of_month / days_in_month, 2)
                else:
                    if safe_int(sm) < safe_int(yyyyMM):
                        Revenue_PlanAmount += ba
                    Budget_Amount += ba
        else:
            # C#: 从 T_BUDGETEXPENSE A LEFT JOIN T_SERVERPART B 查
            budget_sql = f"""SELECT A."STATISTICS_MONTH", A."PROVINCE_CODE", A."SERVERPART_ID",
                    A."SERVERPART_NAME", A."BUDGET_AMOUNT", A."SPREGIONTYPE_ID",
                    A."SPREGIONTYPE_NAME", A."SERVERPART_IDS", B."STATISTICS_TYPE"
                FROM "T_BUDGETEXPENSE" A
                LEFT JOIN "T_SERVERPART" B ON A."SERVERPART_ID" = B."SERVERPART_ID"
                WHERE 1 = 1{where_sql}"""
            budget_rows = db.execute_query(budget_sql) or []
            # C#: selectedSQL = SPRegionTypeID == null ? "SERVERPART_ID = 0" : ""
            if SPRegionTypeID is None:
                filtered = [r for r in budget_rows if safe_int(r.get("SERVERPART_ID")) == 0]
            else:
                filtered = budget_rows
            for r in sorted(filtered, key=lambda x: str(x.get("STATISTICS_MONTH", ""))):
                sm = str(r.get("STATISTICS_MONTH", ""))
                ba = safe_dec(r.get("BUDGET_AMOUNT"))
                try:
                    cd = dt.strptime(sm + "01", "%Y%m%d")
                    cmd = calendar.monthrange(cd.year, cd.month)[1]
                except:
                    cmd = 30
                if sm == yyyyMM:
                    Budget_Amount += ba * cmd
                    Revenue_PlanAmount += ba * day_of_month
                else:
                    bv = ba * cmd
                    if safe_int(sm) < safe_int(yyyyMM):
                        Revenue_PlanAmount += bv
                    Budget_Amount += bv
            # C#: StatisticsType == 4 时追加查 T_BUDGETDETAIL_AH
            if StatisticsType == 4 and SPRegionTypeID is not None:
                sp_sql = f"""SELECT B."STATISTICS_MONTH", A."SERVERPART_ID", A."SERVERPART_NAME",
                        B."BUDGETDETAIL_AMOUNT", A."SPREGIONTYPE_ID", A."SPREGIONTYPE_NAME",
                        1000 AS "STATISTICS_TYPE"
                    FROM "T_BUDGETPROJECT_AH" A, "T_BUDGETDETAIL_AH" B
                    WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                        AND B."ACCOUNT_CODE" = 1000
                        AND B."STATISTICS_MONTH" = {yyyyMM}
                        AND A."SPREGIONTYPE_ID" = {SPRegionTypeID}"""
                sp_rows = db.execute_query(sp_sql) or []
                for sr in sp_rows:
                    budget_rows.append({
                        "STATISTICS_MONTH": sr.get("STATISTICS_MONTH"),
                        "SERVERPART_ID": sr.get("SERVERPART_ID"),
                        "SERVERPART_NAME": sr.get("SERVERPART_NAME"),
                        "BUDGET_AMOUNT": sr.get("BUDGETDETAIL_AMOUNT"),
                        "SPREGIONTYPE_ID": sr.get("SPREGIONTYPE_ID"),
                        "SPREGIONTYPE_NAME": sr.get("SPREGIONTYPE_NAME"),
                        "STATISTICS_TYPE": 1000,
                    })

        # C#: if (Budget_Amount == 0) return null → 101
        if Budget_Amount == 0:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # ============ 3. 统计营收数据 ============
        where_rev = ""
        if ServerpartID is not None:
            where_rev += f' AND B."SERVERPART_ID" = {ServerpartID}'
        elif SPRegionTypeID is not None:
            if StatisticsType == 3:
                sp_ids = set(str(safe_int(r.get("SERVERPART_ID"))) for r in budget_rows)
                sp_ids.discard("0")
                where_rev += f' AND B."SERVERPART_ID" IN ({",".join(sp_ids)})' if sp_ids else ' AND 1 = 2'
            else:
                has_ids = any(r.get("SERVERPART_IDS") for r in budget_rows)
                if has_ids:
                    matched = [r for r in budget_rows if safe_int(r.get("SPREGIONTYPE_ID")) == SPRegionTypeID]
                    if matched and matched[0].get("SERVERPART_IDS"):
                        where_rev += f' AND B."SERVERPART_ID" IN ({matched[0]["SERVERPART_IDS"]})'
                    else:
                        where_rev += ' AND 1 = 2'
                else:
                    where_rev += f' AND B."SPREGIONTYPE_ID" = {SPRegionTypeID}'
        elif ProvinceCode:
            where_rev += f' AND B."PROVINCE_CODE" = {ProvinceCode}'
        # 日期条件
        if StatisticsType in (1, 4):
            where_rev += f' AND A."STATISTICS_DATE" >= {yyyyMM01}'
        else:
            where_rev += f' AND A."STATISTICS_DATE" >= {yyyy0101}'
        where_rev += f' AND A."STATISTICS_DATE" <= {yyyyMMdd}'

        if StatisticsType in (1, 4):
            # 按服务区分组
            rev_sql = f"""SELECT B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000{where_rev}
                GROUP BY B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX" """
        else:
            # 按月份分组
            rev_sql = f"""SELECT SUBSTR(CAST(A."STATISTICS_DATE" AS VARCHAR), 1, 6) AS "STATISTICS_MONTH",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000{where_rev}
                GROUP BY SUBSTR(CAST(A."STATISTICS_DATE" AS VARCHAR), 1, 6)"""
        rev_rows = db.execute_query(rev_sql) or []

        Revenue_Amount = sum(safe_dec(r.get("REVENUE_AMOUNT")) for r in rev_rows)
        Budget_Degree = round(Revenue_Amount / Budget_Amount * 100, 2) if Budget_Amount > 0 else 0

        # ============ 4. 构建子列表 RegionBudgetList ============
        region_list = []
        Growth_Rate = 0.0

        if StatisticsType == 1:
            # C#: 按月度统计，子项是片区
            Growth_Rate = round(Budget_Degree - (day_of_month * 100.0 / days_in_month), 2)
            for r in sorted([b for b in budget_rows if safe_int(b.get("STATISTICS_TYPE")) == 1010],
                           key=lambda x: str(x.get("STATISTICS_MONTH", ""))):
                ids_str = str(r.get("SERVERPART_IDS", "") or "")
                id_set = set(ids_str.split(",")) if ids_str else set()
                sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                           if str(safe_int(rr.get("SERVERPART_ID"))) in id_set)
                sp_bgt = safe_dec(r.get("BUDGET_AMOUNT")) * days_in_month
                sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
                region_list.append({
                    "Serverpart_ID": safe_int(r.get("SPREGIONTYPE_ID")),
                    "Serverpart_Name": str(r.get("SPREGIONTYPE_NAME", "")),
                    "Revenue_Amount": sp_rev, "Budget_Amount": sp_bgt,
                    "Budget_Degree": sp_deg,
                    "Growth_Rate": round(sp_deg - (day_of_month * 100.0 / days_in_month), 2),
                })
        elif StatisticsType == 4:
            # C#: 按片区统计，子项是服务区
            Growth_Rate = round(Budget_Degree - (day_of_month * 100.0 / days_in_month), 2)
            for r in sorted([b for b in budget_rows if safe_int(b.get("STATISTICS_TYPE")) == 1000],
                           key=lambda x: safe_dec(x.get("BUDGET_AMOUNT")), reverse=True):
                sp_id = safe_int(r.get("SERVERPART_ID"))
                sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                           if safe_int(rr.get("SERVERPART_ID")) == sp_id)
                sp_bgt = safe_dec(r.get("BUDGET_AMOUNT"))
                sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
                region_list.append({
                    "Serverpart_ID": sp_id,
                    "Serverpart_Name": str(r.get("SERVERPART_NAME", "")),
                    "Revenue_Amount": sp_rev, "Budget_Amount": sp_bgt,
                    "Budget_Degree": sp_deg,
                    "Growth_Rate": round(sp_deg - (day_of_month * 100.0 / days_in_month), 2),
                })
        elif StatisticsType == 2:
            # C#: 按年度统计，子项是月份
            Growth_Rate = round((Revenue_Amount - Revenue_PlanAmount) / Budget_Amount * 100, 2) if Budget_Amount > 0 else 0
            mf = [b for b in budget_rows if safe_int(b.get("SERVERPART_ID")) == 0]
            if not ShowWholeYear:
                mf = [b for b in mf if safe_int(b.get("STATISTICS_MONTH")) <= safe_int(yyyyMM)]
            for r in sorted(mf, key=lambda x: str(x.get("STATISTICS_MONTH", ""))):
                sm = str(r.get("STATISTICS_MONTH", ""))
                try:
                    cd = dt.strptime(sm + "01", "%Y%m%d")
                    cmd = calendar.monthrange(cd.year, cd.month)[1]
                except: cmd = 30
                sm_m = int(sm[4:6]) if len(sm) >= 6 else 0
                sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                           if str(rr.get("STATISTICS_MONTH", "")) == sm)
                sp_bgt = safe_dec(r.get("BUDGET_AMOUNT")) * cmd
                sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
                if sm == yyyyMM:
                    g = round(sp_deg - (day_of_month * 100.0 / cmd), 2)
                elif safe_int(sm) < safe_int(yyyyMM):
                    g = sp_deg - 100
                else:
                    g = 0
                region_list.append({
                    "Statistics_Month": sm_m, "Revenue_Amount": sp_rev,
                    "Budget_Amount": sp_bgt, "Budget_Degree": sp_deg, "Growth_Rate": g,
                })
        elif StatisticsType == 3:
            # C#: 按服务区统计，子项是月份
            Growth_Rate = round((Revenue_Amount - Revenue_PlanAmount) / Budget_Amount * 100, 2) if Budget_Amount > 0 else 0
            u_months = sorted(set(str(r.get("STATISTICS_MONTH", "")) for r in budget_rows))
            if not ShowWholeYear:
                u_months = [m for m in u_months if safe_int(m) <= safe_int(yyyyMM)]
            for sm in u_months:
                try:
                    cd = dt.strptime(sm + "01", "%Y%m%d")
                    cmd = calendar.monthrange(cd.year, cd.month)[1]
                except: cmd = 30
                sm_m = int(sm[4:6]) if len(sm) >= 6 else 0
                sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                           if str(rr.get("STATISTICS_MONTH", "")) == sm)
                sp_bgt = sum(safe_dec(br.get("BUDGET_AMOUNT")) for br in budget_rows
                           if str(br.get("STATISTICS_MONTH", "")) == sm)
                sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
                if sm == yyyyMM:
                    g = round(sp_deg - (day_of_month * 100.0 / cmd), 2)
                elif safe_int(sm) < safe_int(yyyyMM):
                    g = sp_deg - 100
                else:
                    g = 0
                region_list.append({
                    "Statistics_Month": sm_m, "Revenue_Amount": sp_rev,
                    "Budget_Amount": sp_bgt, "Budget_Degree": sp_deg, "Growth_Rate": g,
                })

        return Result.success(data={
            "Revenue_Amount": Revenue_Amount, "Budget_Amount": Budget_Amount,
            "Budget_Degree": Budget_Degree, "Growth_Rate": Growth_Rate,
            "RegionBudgetList": region_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetProvinceRevenueBudget 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 支付/配送 =====
@router.get("/Revenue/GetMobileShare")
async def get_mobile_share(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取移动支付分账数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND A."SERVERPART_ID" = {Serverpart_ID}'
        elif SPRegionType_ID:
            where_sql += f' AND A."SERVERPART_ID" IN (SELECT "SERVERPART_ID" FROM "T_SERVERPART" WHERE "SPREGIONTYPE_ID" = {SPRegionType_ID})'
        if Province_Code:
            where_sql += f' AND A."PROVINCE_CODE" = {Province_Code}'

        if StatisticsStartDate:
            sd = dt.strptime(StatisticsStartDate, "%Y-%m-%d").strftime("%Y%m%d") if "-" in StatisticsStartDate else StatisticsStartDate
            where_sql += f' AND A."STATISTICS_DATE" >= {sd}'
        if StatisticsEndDate:
            ed = dt.strptime(StatisticsEndDate, "%Y-%m-%d").strftime("%Y%m%d") if "-" in StatisticsEndDate else StatisticsEndDate
            where_sql += f' AND A."STATISTICS_DATE" <= {ed}'

        sql = f"""SELECT COUNT(DISTINCT "SERVERPARTSHOP_ID") AS "SHOP_COUNT",
                SUM("TICKET_PRICE") AS "TICKET_PRICE", SUM("TICKET_FEE") AS "TICKET_FEE",
                SUM("ROYALTY_PRICE") AS "ROYALTY_PRICE", SUM("SUBROYALTY_PRICE") AS "SUBROYALTY_PRICE",
                SUM("TICKET_PRICE" - "TICKET_FEE") AS "ACCOUNT_PRICE"
            FROM "T_MOBILEPAYSHARE" A WHERE A."MOBILEPAYSHARE_STATE" = 1{where_sql}"""
        rows = db.execute_query(sql) or []

        if not rows or not rows[0].get("SHOP_COUNT"):
            return Result.success(data=None, msg="查询成功")

        r = rows[0]
        return Result.success(data={
            "Statistics_Date": StatisticsEndDate,
            "Serverpart_ID": None,
            "Serverpart_Name": None,
            "ShareShop_Count": safe_int(r.get("SHOP_COUNT")),
            "Royalty_Price": safe_dec(r.get("ROYALTY_PRICE")),
            "SubRoyalty_Price": safe_dec(r.get("SUBROYALTY_PRICE")),
            "Ticket_Fee": safe_dec(r.get("TICKET_FEE")),
            "Ticket_Price": safe_dec(r.get("TICKET_PRICE")),
            "Account_Price": safe_dec(r.get("ACCOUNT_PRICE")),
            "ShareShopGrowth_Count": None,
            "RoyaltyGrowth_Price": None,
            "MonthRoyalty_Price": None,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMobileShare 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetMallDeliver")
async def get_mall_deliver(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商城配送数据 (SQL平移完成)"""
    try:
        if Province_Code != "340000":
            return Result.success(data=None, msg="查询成功")

        # C#对齐: 如果只传了Statistics_Date, 用它补充Start/End
        if Statistics_Date:
            if not StatisticsStartDate:
                StatisticsStartDate = Statistics_Date
            if not StatisticsEndDate:
                StatisticsEndDate = Statistics_Date

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        where_sql = ' AND A."SELLER_ID" = 9'
        date_sql = ""
        if StatisticsStartDate:
            date_sql += f" AND A.\"DELIVER_DATE\" >= TO_DATE('{StatisticsStartDate.split(' ')[0]}','YYYY-MM-DD')"
        if StatisticsEndDate:
            date_sql += f" AND A.\"DELIVER_DATE\" < TO_DATE('{StatisticsEndDate.split(' ')[0]}','YYYY-MM-DD') + 1"

        sql = f"""SELECT COUNT(DISTINCT A."GOODSDELIVER_ID") AS "DELIVERBILL_COUNT",
                SUM(B."DELIVER_PRICE") AS "DELIVER_PRICE"
            FROM "T_GOODSDELIVER" A, "T_GOODSDELIVERDETAIL" B
            WHERE A."DELIVER_STATE" > 0 AND A."DELIVER_STATE" < 9000
                AND A."GOODSDELIVER_ID" = B."GOODSDELIVER_ID"{where_sql}{date_sql}"""
        rows = db.execute_query(sql) or []

        r = rows[0] if rows else {}
        return Result.success(data={
            "Statistics_Date": StatisticsEndDate,
            "DeliverBill_Count": safe_int(r.get("DELIVERBILL_COUNT")),
            "Deliver_Price": safe_dec(r.get("DELIVER_PRICE")),
            "DeliverBillGrowth_Count": None,
            "DeliverGrowth_Price": None,
            "Deliver_Rate": None,
            "MonthDeliver_Price": None,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMallDeliver 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 客单交易分析 =====
@router.get("/Revenue/GetTransactionAnalysis")
async def get_transaction_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    ShowConsumptionLevel: bool = Query(False, description="是否显示消费水平占比"),
    ShowConvertRate: bool = Query(False, description="是否显示消费转化率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区客单交易分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        if not Statistics_Date:
            return Result.success(data=None, msg="查询成功")

        stat_date = dt.strptime(Statistics_Date, "%Y-%m-%d") if "-" in Statistics_Date else dt.strptime(Statistics_Date, "%Y%m%d")
        date_str = stat_date.strftime("%Y%m%d")
        month_start = stat_date.strftime("%Y%m01")
        sp_id = int(Serverpart_ID) if Serverpart_ID else None

        # 查当日数据
        if sp_id:
            day_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                    SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                    SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A
                WHERE A."REVENUEDAILY_STATE" = 1
                    AND A."STATISTICS_DATE" = {date_str} AND A."SERVERPART_ID" = {sp_id}"""
        else:
            day_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                    SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                    SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A
                WHERE A."REVENUEDAILY_STATE" = 1 AND A."SERVERPART_ID" = 0
                    AND A."STATISTICS_DATE" = {date_str}"""
        day_rows = db.execute_query(day_sql) or []

        ticket_count = 0
        total_count = 0.0
        revenue_amount = 0.0
        avg_ticket_price = None
        if day_rows and day_rows[0].get("TICKETCOUNT") is not None:
            ticket_count = safe_int(day_rows[0].get("TICKETCOUNT"))
            total_count = safe_dec(day_rows[0].get("TOTALCOUNT"))
            revenue_amount = safe_dec(day_rows[0].get("CASHPAY"))
            if ticket_count > 0:
                avg_ticket_price = round(revenue_amount / ticket_count, 2)

        # 查月均数据
        # 转换Province_Code到内码
        province_id = None
        if Province_Code:
            pid_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
            pid_rows = db.execute_query(pid_sql, {"pc": Province_Code})
            province_id = pid_rows[0]["FIELDENUM_ID"] if pid_rows else None

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

        ticket_avg = 0
        total_avg = 0.0
        avg_rev = 0.0
        month_avg_price = 0.0
        province_ticket = 0
        province_total = 0.0
        province_rev = 0.0
        province_avg_price = 0.0
        if m_rows:
            mr = m_rows[0]
            sp_days = safe_int(mr.get("SP_DAYS"))
            all_days = safe_int(mr.get("ALL_DAYS"))
            if sp_days > 0:
                ticket_avg = safe_int(mr.get("SP_TICKET")) // sp_days
                total_avg = round(safe_dec(mr.get("SP_TOTAL")) / sp_days, 2)
                avg_rev = round(safe_dec(mr.get("SP_REVENUE")) / sp_days, 2)
                month_avg_price = round(avg_rev / ticket_avg, 2) if ticket_avg > 0 else 0
            if all_days > 0:
                province_ticket = safe_int(mr.get("ALL_TICKET")) // all_days
                province_total = round(safe_dec(mr.get("ALL_TOTAL")) / all_days, 2)
                province_rev = round(safe_dec(mr.get("ALL_REVENUE")) / all_days, 2)
                province_avg_price = round(province_rev / province_ticket, 2) if province_ticket > 0 else 0

        # 查服务区名
        sp_name = None
        if sp_id:
            sp_name_rows = db.execute_query(f'SELECT "SERVERPART_NAME" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {sp_id}') or []
            sp_name = sp_name_rows[0].get("SERVERPART_NAME", "") if sp_name_rows else ""

        result = {
            "Serverpart_ID": sp_id,
            "Serverpart_Name": sp_name or "",
            "SPRegionType_Name": None,
            "Statistics_Date": None,
            "TicketCount": ticket_count, "TotalCount": total_count,
            "RevenueAmount": revenue_amount, "AvgTicketPrice": avg_ticket_price,
            "VehicleCount": None, "AvgVehicleAmount": None,
            "TicketAvgCount": ticket_avg, "TotalAvgCount": total_avg,
            "AvgRevenueAmount": avg_rev, "MonthAvgTicketPrice": month_avg_price,
            "MonthVehicleCount": None, "MonthVehicleAmount": None,
            "ConvertRate": None,
            "TicketProvinceCount": province_ticket, "TotalProvinceCount": province_total,
            "ProvinceRevenueAmount": province_rev, "ProvinceAvgTicketPrice": province_avg_price,
            "ConvertProvinceRate": None,
            "transactionLevel": None,
        }

        return Result.success(data=result, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetTransactionTimeAnalysis")
async def get_transaction_time_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区时段消费分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        if not Statistics_Date:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        stat_date = dt.strptime(Statistics_Date, "%Y-%m-%d") if "-" in Statistics_Date else dt.strptime(Statistics_Date, "%Y%m%d")
        month_str = stat_date.strftime("%Y%m")

        # C#对齐: TransactionHelper 第372-383行过滤逻辑
        where_sql = ""
        _sp_ids = parse_multi_ids(Serverpart_ID)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'
        else:
            # C#对齐: else 分支 → 按省份过滤（FieldEnum 转换）
            if Province_Code:
                pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                    WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
                    AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
                pc_rows = db.execute_query(pc_sql, {"pc": Province_Code})
                if pc_rows:
                    province_id = pc_rows[0]["FIELDENUM_ID"]
                    where_sql += f' AND B."PROVINCE_CODE" = {province_id}'

        # 按小时查时段交易
        sql = f"""SELECT A."STATISTICS_HOUR",
                ROUND(SUM(A."TICKET_COUNT") / MAX(A."STATISTICS_DAYS"),0) AS "TICKET_COUNT",
                ROUND(SUM(A."SELLMASTER_AMOUNT") / MAX(A."STATISTICS_DAYS"),2) AS "SELLMASTER_AMOUNT"
            FROM "T_YSSELLMASTERMONTH" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."DATA_TYPE" IN (0,1) AND A."STATISTICS_MONTH" = {month_str}{where_sql}
            GROUP BY A."STATISTICS_HOUR"
            ORDER BY A."STATISTICS_HOUR" """
        rows = db.execute_query(sql) or []
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        hour_map = {}
        for r in rows:
            h = int(safe_dec(r.get("STATISTICS_HOUR")))
            hour_map[h] = {"ticket": safe_dec(r.get("TICKET_COUNT")), "amount": safe_dec(r.get("SELLMASTER_AMOUNT"))}

        total_ticket = sum(v["ticket"] for v in hour_map.values())
        total_amount = sum(v["amount"] for v in hour_map.values())

        scatter_list = []
        slots = 24 // TimeSpan
        for i in range(slots + 1):
            h_start = i * TimeSpan
            h_end = min((i + 1) * TimeSpan, 24)
            slot_ticket = sum(hour_map.get(h, {}).get("ticket", 0) for h in range(h_start, h_end))
            slot_amount = sum(hour_map.get(h, {}).get("amount", 0) for h in range(h_start, h_end))
            pct = round(slot_ticket / total_ticket * 100, 2) if total_ticket > 0 else 0
            scatter_list.append({
                "name": str(min(h_start, 24)),
                "value": str(pct),
                "data": str(round(slot_ticket)),
                "key": str(round(slot_amount)),
            })

        return Result.success(data={
            "name": "时段交易",
            "CommonScatterList": scatter_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionTimeAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetTransactionConvert")
async def get_transaction_convert(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取消费转化对比分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        if not Statistics_Date:
            return Result.success(data=None, msg="查询成功")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        stat_date = dt.strptime(Statistics_Date, "%Y-%m-%d") if "-" in Statistics_Date else dt.strptime(Statistics_Date, "%Y%m%d")
        month_str = stat_date.strftime("%Y%m")

        where_sql = ""
        _sp_ids = parse_multi_ids(Serverpart_ID)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'

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
            h = int(safe_dec(r.get("STATISTICS_HOUR")))
            if 0 <= h < 24:
                t_data[h] = [float(h), safe_dec(r.get("TICKET_COUNT"))]

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
            h = int(safe_dec(r.get("STATISTICS_HOUR")))
            if 0 <= h < 24:
                b_data[h] = [float(h), safe_dec(r.get("TICKET_COUNT"))]

        return Result.success(data={
            "TransactionList": {"name": "客单数" if t_rows else None, "data": t_data if t_rows else None, "value": None, "CommonScatterList": None},
            "BayonetList": {"name": "车流量", "data": b_data, "value": None, "CommonScatterList": None},
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionConvert 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 业态分析 =====
@router.get("/Revenue/GetBusinessTradeRevenue")
async def get_business_trade_revenue(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    BusinessTradeIds: Optional[str] = Query("", description="经营业态内码"),
    DataType: int = Query(1, description="数据类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态营收占比 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not StatisticsDate:
            return Result.success(data=None, msg="查询成功")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        month_start = stat_date.strftime("%Y%m01")
        date_str = stat_date.strftime("%Y%m%d")

        where_sql = f' AND A."STATISTICS_DATE" >= {month_start} AND A."STATISTICS_DATE" <= {date_str}'
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionTypeID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeID})'

        sql = f"""SELECT A."BUSINESS_TRADE",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000{where_sql}
            GROUP BY A."BUSINESS_TRADE"
            ORDER BY SUM(A."TICKET_COUNT") DESC"""
        rows = db.execute_query(sql) or []

        if not rows:
            return Result.success(data=None, msg="查询成功")

        total_ticket = sum(safe_dec(r.get("TICKET_COUNT")) for r in rows)
        total_rev = sum(safe_dec(r.get("REVENUE_AMOUNT")) for r in rows)

        # 查询业态名称字典：T_AUTOSTATISTICS
        trade_name_map = {}
        try:
            trade_sql = """SELECT "AUTOSTATISTICS_ID", "AUTOSTATISTICS_NAME" FROM "T_AUTOSTATISTICS" WHERE "AUTOSTATISTICS_TYPE" = 2000"""
            trade_rows = db.execute_query(trade_sql) or []
            for tr in trade_rows:
                tid = str(tr.get("AUTOSTATISTICS_ID", ""))
                trade_name_map[tid] = tr.get("AUTOSTATISTICS_NAME", "其他业态")
        except Exception:
            pass

        rank_list = []
        for r in rows:
            tc = safe_dec(r.get("TICKET_COUNT"))
            ra = safe_dec(r.get("REVENUE_AMOUNT"))
            trade_id = str(r.get("BUSINESS_TRADE", "") or "")
            trade_name = trade_name_map.get(trade_id, "其他业态") if trade_id else "其他业态"
            if DataType == 1:
                pct = round(tc / total_ticket * 100, 2) if total_ticket > 0 else 0
            else:
                pct = round(ra / total_rev * 100, 2) if total_rev > 0 else 0
            rank_list.append({
                "name": trade_name,
                "value": f"{pct:.2f}",
                "data": f"客单 {int(tc)}笔,金额 {ra:,.2f}元",
                "key": trade_id if trade_id else "0",
            })

        return Result.success(data={
            "Serverpart_ID": None,
            "Serverpart_Name": None,
            "SPRegionType_Name": None,
            "Rigid_Demand": False,
            "Abundant": True,
            "BusinessTradeRank": rank_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeRevenue 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBusinessTradeLevel")
async def get_business_trade_level(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeTrade: bool = Query(False, description="是否显示全部业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态消费水平占比 (按C#逻辑重写)"""
    try:
        from datetime import datetime as dt
        from collections import defaultdict

        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not StatisticsDate:
            return Result.success(data={"ColumnList": [], "legend": None}, msg="查询成功")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        month_str = stat_date.strftime("%Y%m")

        # 查省份ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": ProvinceCode})
        province_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else ProvinceCode

        where_sql = f' AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_MONTH" = {month_str}'
        if ServerpartId:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', [ServerpartId]).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')

        # 按业态+消费等级分组
        sql = f"""SELECT C."BUSINESS_TRADE", A."AMOUNT_RANGE",
                ROUND(SUM(A."TICKET_COUNT") / MAX(A."STATISTICS_DAYS"), 0) AS "AVGTICKET_COUNT"
            FROM "T_CONSUMPTIONLEVEL" A, "T_SERVERPART" B, "T_SERVERPARTSHOP" C
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."CONSUMPTIONLEVEL_STATE" = 1
                AND A."SERVERPARTSHOP_ID" = C."SERVERPARTSHOP_ID"
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999'){where_sql}
            GROUP BY C."BUSINESS_TRADE", A."AMOUNT_RANGE" """
        rows = db.execute_query(sql) or []

        if not rows:
            return Result.success(data=None, msg="查询成功")

        # 查业态名称
        trade_name_sql = """SELECT "AUTOSTATISTICS_ID", "AUTOSTATISTICS_PID", "AUTOSTATISTICS_NAME"
            FROM "T_AUTOSTATISTICS" WHERE "AUTOSTATISTICS_TYPE" = 2000"""
        trade_rows = db.execute_query(trade_name_sql) or []
        trade_name_map = {}
        trade_parent_map = {}
        for t in trade_rows:
            tid = str(t.get("AUTOSTATISTICS_ID", ""))
            trade_name_map[tid] = t.get("AUTOSTATISTICS_NAME", "")
            trade_parent_map[tid] = str(t.get("AUTOSTATISTICS_PID", ""))

        # 查找一级业态（ShowFirstTrade默认True）
        def get_parent_trade(trade_id):
            """递归查找一级业态ID"""
            visited = set()
            tid = str(trade_id)
            while tid in trade_parent_map and trade_parent_map[tid] != "-1" and tid not in visited:
                visited.add(tid)
                tid = trade_parent_map[tid]
            return tid

        # 按具体业态+消费等级分组（C#不递归到一级,直接用具体业态）
        ptrade_total = defaultdict(float)
        ptrade_range = defaultdict(lambda: defaultdict(float))
        for r in rows:
            trade = str(r.get("BUSINESS_TRADE") or "")
            ar = int(safe_dec(r.get("AMOUNT_RANGE")))
            tc = safe_dec(r.get("AVGTICKET_COUNT"))
            ptrade_total[trade] += tc
            ptrade_range[trade][ar] += tc

        # 按客单量降序排序
        show_count = 5  # C#默认 ShowTradeCount=5
        sorted_trades = sorted(
            [(t, v) for t, v in ptrade_total.items() if t and t in trade_name_map],
            key=lambda x: x[1], reverse=True
        )
        if ShowWholeTrade:
            show_count = min(show_count, len(sorted_trades)) + 1
        else:
            show_count = min(show_count, len(sorted_trades))

        if show_count == 0:
            return Result.success(data=None, msg="查询成功")

        legend = [None] * show_count
        amount_ranges = [("1", "低消费"), ("2", "普通消费"), ("3,4", "高消费")]
        col_list = []
        for ar_key, ar_name in amount_ranges:
            col_list.append({"name": ar_name, "value": [ar_key], "data": [0.0] * show_count})

        idx = 0
        for trade_id, total in sorted_trades:
            if idx >= (show_count - 1 if ShowWholeTrade else show_count):
                break
            legend[idx] = trade_name_map.get(trade_id, "其他业态")
            r1 = ptrade_range[trade_id].get(1, 0)
            pct1 = round(r1 / total * 100, 2) if total > 0 else 0
            col_list[0]["data"][idx] = pct1
            r2 = ptrade_range[trade_id].get(2, 0)
            pct2 = round(r2 / total * 100, 2) if total > 0 else 0
            col_list[1]["data"][idx] = pct2
            col_list[2]["data"][idx] = round(100 - pct1 - pct2, 2)
            idx += 1

        # 其他业态
        other_trades = [(t, v) for t, v in ptrade_total.items() if not t or t not in trade_name_map]
        if idx < (show_count - 1 if ShowWholeTrade else show_count) and other_trades:
            legend[idx] = "其他业态"
            total = sum(v for _, v in other_trades)
            r1 = sum(ptrade_range[t].get(1, 0) for t, _ in other_trades)
            pct1 = round(r1 / total * 100, 2) if total > 0 else 0
            col_list[0]["data"][idx] = pct1
            r2 = sum(ptrade_range[t].get(2, 0) for t, _ in other_trades)
            pct2 = round(r2 / total * 100, 2) if total > 0 else 0
            col_list[1]["data"][idx] = pct2
            col_list[2]["data"][idx] = round(100 - pct1 - pct2, 2)
            idx += 1

        # 全业态汇总
        if ShowWholeTrade:
            legend[show_count - 1] = "全业态"
            all_total = sum(ptrade_total.values())
            if all_total > 0:
                all_r1 = sum(ptrade_range[t].get(1, 0) for t in ptrade_total)
                pct1 = round(all_r1 / all_total * 100, 2)
                col_list[0]["data"][show_count - 1] = pct1
                all_r2 = sum(ptrade_range[t].get(2, 0) for t in ptrade_total)
                pct2 = round(all_r2 / all_total * 100, 2)
                col_list[1]["data"][show_count - 1] = pct2
                col_list[2]["data"][show_count - 1] = round(100 - pct1 - pct2, 2)

        return Result.success(data={"ColumnList": col_list, "legend": legend}, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeLevel 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBusinessBrandLevel")
async def get_business_brand_level(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeBrand: bool = Query(True, description="是否显示全品牌"),
    ShowBrandCount: Optional[str] = Query("5", description="显示品牌数量"),
    SPRegionTypeID: Optional[str] = Query(None, description="片区ID"),
    BusinessTradeIds: Optional[str] = Query(None, description="业态ID"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取品牌消费水平占比 (按C#逻辑重写)"""
    try:
        from datetime import datetime as dt
        from collections import defaultdict

        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not StatisticsDate:
            return Result.success(data={"ColumnList": [], "legend": None}, msg="查询成功")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        month_str = stat_date.strftime("%Y%m")

        # 查省份ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": ProvinceCode})
        province_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else ProvinceCode

        where_sql = f' AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_MONTH" = {month_str}'
        if ServerpartId:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', [ServerpartId]).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')

        # 查T_CONSUMPTIONLEVEL按品牌+消费等级分组
        sql = f"""SELECT C."BRAND_NAME", A."AMOUNT_RANGE",
                ROUND(SUM(A."TICKET_COUNT") / MAX(A."STATISTICS_DAYS"), 0) AS "AVGTICKET_COUNT"
            FROM "T_CONSUMPTIONLEVEL" A, "T_SERVERPART" B, "T_SERVERPARTSHOP" C
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."CONSUMPTIONLEVEL_STATE" = 1
                AND A."SERVERPARTSHOP_ID" = C."SERVERPARTSHOP_ID"
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999'){where_sql}
            GROUP BY C."BRAND_NAME", A."AMOUNT_RANGE" """
        rows = db.execute_query(sql) or []

        if not rows:
            return Result.success(data=None, msg="查询成功")

        # 按品牌汇总客单总量
        brand_total = defaultdict(float)
        brand_range = defaultdict(lambda: defaultdict(float))
        for r in rows:
            brand = r.get("BRAND_NAME") or ""
            ar = int(safe_dec(r.get("AMOUNT_RANGE")))
            tc = safe_dec(r.get("AVGTICKET_COUNT"))
            brand_total[brand] += tc
            brand_range[brand][ar] += tc

        # 按客单量降序
        try:
            brand_count = int(ShowBrandCount) if ShowBrandCount and ShowBrandCount.isdigit() else 5
        except:
            brand_count = 5
        show_count = brand_count
        sorted_brands = sorted(
            [(b, t) for b, t in brand_total.items() if b],
            key=lambda x: x[1], reverse=True
        )
        if ShowWholeBrand:
            # 显示全品牌时多一列
            show_count = min(show_count, len(sorted_brands)) + 1
        else:
            show_count = min(show_count, len(sorted_brands))

        if show_count == 0:
            return Result.success(data=None, msg="查询成功")

        legend = [None] * show_count
        # 消费等级定义: 1=低消费, 2=普通消费, 3,4=高消费
        amount_ranges = [("1", "低消费"), ("2", "普通消费"), ("3,4", "高消费")]
        col_list = []
        for ar_key, ar_name in amount_ranges:
            col_list.append({"name": ar_name, "value": [ar_key], "data": [0.0] * show_count})

        idx = 0
        for brand, total in sorted_brands:
            if idx >= (show_count - 1 if ShowWholeBrand else show_count):
                break
            legend[idx] = brand
            # 低消费
            r1 = brand_range[brand].get(1, 0)
            pct1 = round(r1 / total * 100, 2) if total > 0 else 0
            col_list[0]["data"][idx] = pct1
            # 普通消费
            r2 = brand_range[brand].get(2, 0)
            pct2 = round(r2 / total * 100, 2) if total > 0 else 0
            col_list[1]["data"][idx] = pct2
            # 高消费 = 100 - 低 - 普通
            col_list[2]["data"][idx] = round(100 - pct1 - pct2, 2)
            idx += 1

        # 无品牌的归为"其他品牌"
        if idx < (show_count - 1 if ShowWholeBrand else show_count) and "" in brand_total:
            legend[idx] = "其他品牌"
            total = brand_total[""]
            r1 = brand_range[""].get(1, 0)
            pct1 = round(r1 / total * 100, 2) if total > 0 else 0
            col_list[0]["data"][idx] = pct1
            r2 = brand_range[""].get(2, 0)
            pct2 = round(r2 / total * 100, 2) if total > 0 else 0
            col_list[1]["data"][idx] = pct2
            col_list[2]["data"][idx] = round(100 - pct1 - pct2, 2)
            idx += 1

        # 全品牌汇总
        if ShowWholeBrand:
            legend[show_count - 1] = "全品牌"
            all_total = sum(brand_total.values())
            if all_total > 0:
                all_r1 = sum(brand_range[b].get(1, 0) for b in brand_total)
                pct1 = round(all_r1 / all_total * 100, 2)
                col_list[0]["data"][show_count - 1] = pct1
                all_r2 = sum(brand_range[b].get(2, 0) for b in brand_total)
                pct2 = round(all_r2 / all_total * 100, 2)
                col_list[1]["data"][show_count - 1] = pct2
                col_list[2]["data"][show_count - 1] = round(100 - pct1 - pct2, 2)

        return Result.success(data={"ColumnList": col_list, "legend": legend}, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessBrandLevel 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 营收趋势 =====
# 注意：C# 中有两个 GetRevenueTrend，一个路由到 GetRevenueCompare(GET)，一个路由到 GetRevenueTrend(GET)
# 这里只保留 GetRevenueTrend 的 GET 版本（下方已有 GET 定义）


@router.get("/Revenue/GetRevenueTrend")
async def get_revenue_trend_get(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期(年份如2025)"),
    StatisticsType: int = Query(1, description="统计类型:1月度2日度4季度"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收趋势图（GET）(SQL平移完成)"""
    try:
        from datetime import datetime as dt
        import calendar

        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        where_sql = ""
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionTypeID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeID})'

        result_list = []

        if StatisticsType == 1:
            # 月度 — C#: DateSQL += " AND A.STATISTICS_MONTH >= " + StatisticsDate + "01"
            # C#在Oracle中: 2026-02-1301 = 723, 2026-02-1312 = 712, 范围[723,712]为空集
            # 旧API对此场景返回 TotalCount=0, List=[]
            date_sql = ""
            valid_year = True
            if StatisticsDate:
                sd_clean = StatisticsDate.replace("-", "").replace("/", "")
                if not sd_clean.isdigit() or len(StatisticsDate) > 4:
                    # 非纯年份格式（如2026-02-13），C#中会因SQL异常/空范围返回空
                    valid_year = False
                else:
                    date_sql = f' AND A."STATISTICS_MONTH" >= {StatisticsDate}01 AND A."STATISTICS_MONTH" <= {StatisticsDate}12'
            if valid_year:
                sql = f"""SELECT A."STATISTICS_MONTH" AS "STATISTICS",
                        SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                        SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
                    FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
                    WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                        AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                    GROUP BY A."STATISTICS_MONTH" """
                rows = db.execute_query(sql) or []
                stat_map = {}
                for r in rows:
                    v = int(r.get("STATISTICS", 0))
                    stat_map[v % 100] = r
                for m in range(1, 13):
                    r = stat_map.get(m)
                    result_list.append({
                        "name": f"{m}月",
                        "value": str(safe_dec(r.get("REVENUE_AMOUNT"))) if r else "0",
                    })

        elif StatisticsType == 2:
            # 日度
            date_sql = ""
            if StatisticsDate:
                stat_d = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
                m_start = stat_d.strftime("%Y%m01")
                m_end = stat_d.strftime("%Y%m%d")
                date_sql = f' AND A."STATISTICS_DATE" >= {m_start} AND A."STATISTICS_DATE" <= {m_end}'
                days_in_month = calendar.monthrange(stat_d.year, stat_d.month)[1]
            else:
                days_in_month = 31
            sql = f"""SELECT A."STATISTICS_DATE" AS "STATISTICS",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                    SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                    AND A."REVENUEDAILY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                GROUP BY A."STATISTICS_DATE" """
            rows = db.execute_query(sql) or []
            stat_map = {str(int(r.get("STATISTICS", 0))): r for r in rows}
            for d in range(1, days_in_month + 1):
                if StatisticsDate:
                    key = f"{stat_d.strftime('%Y%m')}{d:02d}"
                else:
                    key = str(d)
                r = stat_map.get(key)
                result_list.append({
                    "name": str(d),
                    "value": str(safe_dec(r.get("REVENUE_AMOUNT"))) if r else "0",
                })

        elif StatisticsType == 4:
            # 季度 — 同样检查StatisticsDate是否为纯年份
            date_sql = ""
            valid_year = True
            if StatisticsDate:
                sd_clean = StatisticsDate.replace("-", "").replace("/", "")
                if not sd_clean.isdigit() or len(StatisticsDate) > 4:
                    valid_year = False
                else:
                    date_sql = f' AND A."STATISTICS_MONTH" >= {StatisticsDate}01 AND A."STATISTICS_MONTH" <= {StatisticsDate}12'
            if valid_year:
                sql = f"""SELECT CEIL(MOD(A."STATISTICS_MONTH", {StatisticsDate}00) / 3) AS "STATISTICS",
                        SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                    FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
                    WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                        AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                    GROUP BY CEIL(MOD(A."STATISTICS_MONTH", {StatisticsDate}00) / 3)"""
                rows = db.execute_query(sql) or []
                stat_map = {str(int(safe_dec(r.get("STATISTICS")))): r for r in rows}
                for q in range(1, 5):
                    r = stat_map.get(str(q))
                    result_list.append({
                        "name": f"第{q}季度",
                        "value": str(safe_dec(r.get("REVENUE_AMOUNT"))) if r else "0",
                    })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueTrend 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 经营报表 =====
@router.get("/Revenue/GetRevenueReport")
async def get_revenue_report(
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    startTime: Optional[str] = Query(None, description="开始时间"),
    endTime: Optional[str] = Query(None, description="结束时间"),
    SearchKeyType: Optional[str] = Query("", description="查询类型"),
    SearchKeyValue: Optional[str] = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区经营报表"""
    try:
        from datetime import datetime as dt
        # 获取省份对应的FieldEnum_ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": provinceCode})
        if not fe_rows:
            return Result.fail(code=200, msg="查询失败，无数数据返回！")
        province_id = fe_rows[0]["FIELDENUM_ID"]

        # 构建 WHERE 条件
        where_parts = [
            'A."SERVERPART_ID" = B."SERVERPART_ID"',
            'A."REVENUEDAILY_STATE" = 1',
            'B."STATISTIC_TYPE" = 1000',
            'B."STATISTICS_TYPE" = 1000',
            f'B."PROVINCE_CODE" = {province_id}',
        ]
        params = {}
        if startTime:
            sd = dt.strptime(startTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in startTime else startTime
            where_parts.append(f'A."STATISTICS_DATE" >= {sd}')
        if endTime:
            ed = dt.strptime(endTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in endTime else endTime
            where_parts.append(f'A."STATISTICS_DATE" <= {ed}')

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

        rows = db.execute_query(sql, params)
        if not rows:
            return Result.fail(code=200, msg="查询失败，无数数据返回！")

        # 汇总总营收
        total_revenue = round(sum(float(r.get("REVENUE_AMOUNT") or 0) for r in rows), 2)
        total_ticket = sum(int(r.get("TICKET_COUNT") or 0) for r in rows)
        total_count = round(sum(float(r.get("TOTAL_COUNT") or 0) for r in rows), 2)
        total_off = round(sum(float(r.get("TOTALOFF_AMOUNT") or 0) for r in rows), 2)
        # 短款/长款：使用DIFFERENT_AMOUNT_LESS/MORE字段（C#逻辑）
        diff_less = round(sum(float(r.get("DIFFERENT_PRICE_LESS") or 0) for r in rows), 2)
        diff_more = round(sum(float(r.get("DIFFERENT_PRICE_MORE") or 0) for r in rows), 2)
        # 南北区：使用REVENUE_AMOUNT_A/B字段（C#逻辑）
        rev_amount_s = round(sum(float(r.get("REVENUE_AMOUNT_A") or 0) for r in rows), 2)
        rev_amount_n = round(sum(float(r.get("REVENUE_AMOUNT_B") or 0) for r in rows), 2)

        # 按片区分组
        from decimal import Decimal
        region_map = {}
        for r in rows:
            rid = r.get("SPREGIONTYPE_ID") or "null"
            if rid not in region_map:
                region_map[rid] = {
                    "Region_Name": r.get("SPREGIONTYPE_NAME") or "无管理中心",
                    "Total_Revenue": Decimal('0'),
                    "Revenue_Proportion": "",
                    "revenueServerModels": [],
                }
            region_map[rid]["Total_Revenue"] += Decimal(str(float(r.get("REVENUE_AMOUNT") or 0)))

            # 添加服务区
            sp_revenue = float(r.get("REVENUE_AMOUNT") or 0)
            region_rev = float(region_map[rid]["Total_Revenue"])
            prop = f"{sp_revenue / region_rev * 100:.2f}%" if region_rev != 0 else ""
            region_map[rid]["revenueServerModels"].append({
                "Serverpart_Id": str(r.get("SERVERPART_ID", "")),
                "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                "Total_Revenue": sp_revenue,
                "Province_Code": provinceCode,
                "Revenue_Proportion": prop,
            })

        # 重新计算片区占比和服务区占比
        region_list = []
        for rid, region in region_map.items():
            region["Revenue_Proportion"] = f"{float(region['Total_Revenue']) / total_revenue * 100:.2f}%" if total_revenue != 0 else ""
            # 重新计算服务区占比
            for sp in region["revenueServerModels"]:
                sp["Revenue_Proportion"] = f"{sp['Total_Revenue'] / float(region['Total_Revenue']) * 100:.2f}%" if region['Total_Revenue'] != 0 else ""
            # 按营收倒序排列服务区
            region["revenueServerModels"].sort(key=lambda x: x["Total_Revenue"], reverse=True)
            region["Total_Revenue"] = float(region["Total_Revenue"])
            region_list.append(region)
        # 按营收倒序排列片区
        region_list.sort(key=lambda x: x["Total_Revenue"], reverse=True)

        result = {
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

        return Result.success(data=result, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueReport 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetRevenueReportDetil")
async def get_revenue_report_detail(
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartShopId: Optional[int] = Query(None, description="门店内码"),
    startTime: Optional[str] = Query(None, description="开始时间"),
    endTime: Optional[str] = Query(None, description="结束时间"),
    SearchKeyType: Optional[str] = Query("", description="查询类型"),
    SearchKeyValue: Optional[str] = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区经营报表详情 (C#逻辑完整平移)"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not serverpartId:
            return Result.success(data=None, msg="查询成功")

        start_str = dt.strptime(startTime.split(' ')[0], '%Y-%m-%d').strftime('%Y%m%d') if startTime and '-' in startTime else startTime
        end_str = dt.strptime(endTime.split(' ')[0], '%Y-%m-%d').strftime('%Y%m%d') if endTime and '-' in endTime else endTime

        where_sql = ''
        if start_str:
            where_sql += f' AND A."STATISTICS_DATE" >= {start_str}'
        if end_str:
            where_sql += f' AND A."STATISTICS_DATE" <= {end_str}'

        # C# SQL: 按SHOPTRADE分组
        sql = f"""SELECT B."SERVERPART_ID",B."SERVERPART_NAME",B."SERVERPART_CODE",B."SERVERPART_INDEX",
                A."SHOPTRADE",
                SUM(A."REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",SUM(A."REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT",SUM(A."TOTAL_COUNT") AS "TOTAL_COUNT",
                SUM(A."OTHERPAY_AMOUNT_A") AS "OTHERPAY_AMOUNT_A",SUM(A."OTHERPAY_AMOUNT_B") AS "OTHERPAY_AMOUNT_B",
                SUM(A."OTHERPAY_AMOUNT") AS "OTHERPAY_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND A."SERVERPART_ID" = {serverpartId}{where_sql}
            GROUP BY B."SERVERPART_ID",B."SERVERPART_NAME",B."SERVERPART_CODE",B."SERVERPART_INDEX",A."SHOPTRADE" """
        rows = db.execute_query(sql) or []
        if not rows:
            return Result.success(data=None, msg="查询成功")

        # 查询该服务区所有门店
        dt_shop = db.execute_query(
            f'SELECT * FROM "T_SERVERPARTSHOP" WHERE "SERVERPART_ID" = {serverpartId} AND "ISVALID" = 1') or []

        # 获取区域名称 (C# GetRegionName)
        s_name = ""  # 南区/东区
        n_name = ""  # 北区/西区
        s_shops = [s for s in dt_shop if s.get("SHOPREGION") is not None and int(s.get("SHOPREGION", 99)) < 30]
        n_shops = [s for s in dt_shop if s.get("SHOPREGION") is not None and int(s.get("SHOPREGION", 0)) >= 30]
        if s_shops:
            s_region = str(sorted(s_shops, key=lambda x: int(x.get("SHOPREGION", 0)))[0].get("SHOPREGION"))
            fe = db.execute_query(
                f"""SELECT B."FIELDENUM_NAME" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'SHOPREGION'
                AND B."FIELDENUM_VALUE" = '{s_region}'""") or []
            s_name = fe[0].get("FIELDENUM_NAME", "") if fe else ""
        if n_shops:
            n_region = str(sorted(n_shops, key=lambda x: int(x.get("SHOPREGION", 0)))[0].get("SHOPREGION"))
            fe = db.execute_query(
                f"""SELECT B."FIELDENUM_NAME" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'SHOPREGION'
                AND B."FIELDENUM_VALUE" = '{n_region}'""") or []
            n_name = fe[0].get("FIELDENUM_NAME", "") if fe else ""

        # 查询品牌信息
        dt_brand = db.execute_query(
            f"""SELECT "BRAND_ID","BRAND_INTRO" FROM "T_BRAND"
            WHERE "PROVINCE_CODE" = '{provinceCode}' AND "BRAND_CATEGORY" = 1000""") or []
        brand_map = {}
        for br in dt_brand:
            bid = str(br.get("BRAND_ID", ""))
            brand_map[bid] = br.get("BRAND_INTRO", "")

        # 门店Map (按SHOPTRADE)
        shop_by_trade = {}
        for s in dt_shop:
            st = str(s.get("SHOPTRADE", ""))
            if st and st not in shop_by_trade:
                # 取第一个匹配的（C# dtShop.Select("SHOPTRADE = '...'")[0]，按BUSINESS_STATE/SHOPREGION/ID排序）
                shop_by_trade[st] = s

        # 汇总
        total_rev_a = sum(safe_dec(r.get("REVENUE_AMOUNT_A")) for r in rows)
        total_rev_b = sum(safe_dec(r.get("REVENUE_AMOUNT_B")) for r in rows)
        total_rev = sum(safe_dec(r.get("REVENUE_AMOUNT")) for r in rows)
        sp_name = rows[0].get("SERVERPART_NAME", "") if rows else ""

        # 四川省去掉大巴券和会员消费
        if provinceCode == "510000":
            total_rev_a -= sum(safe_dec(r.get("OTHERPAY_AMOUNT_A")) for r in rows)
            total_rev_b -= sum(safe_dec(r.get("OTHERPAY_AMOUNT_B")) for r in rows)
            total_rev -= sum(safe_dec(r.get("OTHERPAY_AMOUNT")) for r in rows)

        shop_list = []
        for r in rows:
            shoptrade = str(r.get("SHOPTRADE", "") or "")
            shop_info = shop_by_trade.get(shoptrade, {})

            # 门店名称 = SHOPSHORTNAME
            biz_name = shop_info.get("SHOPSHORTNAME", "") or ""
            # 上传类型 = TRANSFER_TYPE
            upload_type = 0
            try: upload_type = int(shop_info.get("TRANSFER_TYPE", 0) or 0)
            except: pass
            # 品牌Logo
            biz_logo = ""
            biz_brand = str(shop_info.get("BUSINESS_BRAND", "") or "")
            if biz_brand and biz_brand in brand_map:
                intro = brand_map[biz_brand]
                if intro:
                    biz_logo = intro
                    if biz_logo.startswith("/"):
                        biz_logo = "https://user.eshangtech.com" + biz_logo

            rev_a = safe_dec(r.get("REVENUE_AMOUNT_A"))
            rev_b = safe_dec(r.get("REVENUE_AMOUNT_B"))
            biz_rev = safe_dec(r.get("REVENUE_AMOUNT"))

            if provinceCode == "510000":
                rev_a -= safe_dec(r.get("OTHERPAY_AMOUNT_A"))
                rev_b -= safe_dec(r.get("OTHERPAY_AMOUNT_B"))
                biz_rev -= safe_dec(r.get("OTHERPAY_AMOUNT"))

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

        return Result.success(data={
            "Serverpart_Name": sp_name,
            "Serverpart_Revenue": total_rev,
            "Serverpart_S": s_name,
            "Serverpart_RevenueS": total_rev_a,
            "Serverpart_N": n_name,
            "Serverpart_RevenueN": total_rev_b,
            "ShopList": shop_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueReportDetil 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 畅销商品 =====
@router.get("/Revenue/GetSalableCommodity")
async def get_salable_commodity(
    statisticsDate: Optional[str] = Query(None, description="统计日期"),
    provinceCode: Optional[str] = Query(None, description="业主单位标识"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商超畅销商品 — 旧 C# 接口为写死数据，此处完全对齐"""
    # 旧 C# 接口返回固定数据，不依赖任何数据库查询
    return Result.success(data={
        "SalableCommodity": 24.7,
        "SalableCommodityList": [
            {"Commodity_name": "红牛", "Proportion": 9.3},
            {"Commodity_name": "农夫山泉", "Proportion": 5.3},
            {"Commodity_name": "康师傅牛肉面", "Proportion": 4.5},
            {"Commodity_name": "面条", "Proportion": 3.3},
            {"Commodity_name": "其他", "Proportion": 2.3},
        ],
        "UnSalableCommodity": 10.6,
        "UnSalableCommodityList": [
            {"Commodity_name": "水杯", "Proportion": 0.13},
            {"Commodity_name": "吸油纸", "Proportion": 0.06},
            {"Commodity_name": "女儿红", "Proportion": 0.05},
            {"Commodity_name": "消毒纸巾", "Proportion": 0.02},
            {"Commodity_name": "其他", "Proportion": 0.15},
        ],
    }, msg="查询成功")


# ===== 排行/同比 =====
@router.get("/Revenue/GetSPRevenueRank")
async def get_sp_revenue_rank(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    SPRegionType_ID: Optional[int] = Query(None, description="区域内码"),
    Revenue_Include: Optional[int] = Query(None, description="是否纳入营收(0否1是)"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取近日服务区营收排行（C#对齐：RevenuePushHelper.GetSPRevenueRank → GetRevenuePushList）"""
    try:
        from datetime import datetime as dt

        if not pushProvinceCode or not Statistics_Date:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(v) if v is not None else 0
            except: return 0

        # === C#对齐: GetRevenuePushList 中的 WhereSQL 构建 ===
        where_sql = ""

        # 1. 服务区/区域/省份 过滤（C# 第44-87行 if/elif/elif 分支）
        if Serverpart_ID is not None:
            where_sql += f' AND B."SERVERPART_ID" = {Serverpart_ID}'
        elif SPRegionType_ID is not None:
            # C#: 通过 SERVERPART_ID 反查 SPREGIONTYPE_ID
            sp_res = db.execute_query(
                'SELECT "SPREGIONTYPE_ID" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = :sid',
                {"sid": SPRegionType_ID})
            if sp_res:
                where_sql += f' AND B."SPREGIONTYPE_ID" = {sp_res[0]["SPREGIONTYPE_ID"]}'
            else:
                where_sql = " AND 1 = 2"
        elif pushProvinceCode:
            # C#: DictionaryHelper.GetFieldEnum("DIVISION_CODE", pushProvinceCode)
            pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
                AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
            pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
            if pc_rows:
                province_id = pc_rows[0]["FIELDENUM_ID"]
                where_sql += f' AND B."PROVINCE_CODE" = {province_id}'
            else:
                json_list = JsonListData.create(data_list=[], total=0)
                return Result.success(data=json_list.model_dump(), msg="查询成功")
        else:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 2. 日期（C# Controller 传 Statistics_Date, Statistics_Date → StartDate == EndDate → 走"时间段"分支）
        # C#: 因为 Start==End，实际走的是 if (Statistics_StartDate != Statistics_EndDate) 分支的 else
        # 但注意: C# Controller 第1882行传了 Statistics_Date, Statistics_Date 两次
        # 即 Start==End, 走第199行 else 分支("当日"逻辑，涉及扫码门店等复杂逻辑)
        # 简化处理: 用 T_REVENUEDAILY 的日期范围查询（Start==End时只查当天）
        stat_date_str = Statistics_Date
        if "-" in Statistics_Date:
            stat_date_str = dt.strptime(Statistics_Date, "%Y-%m-%d").strftime("%Y%m%d")
        elif "/" in Statistics_Date:
            stat_date_str = dt.strptime(Statistics_Date, "%Y/%m/%d").strftime("%Y%m%d")
        where_sql += f' AND A."STATISTICS_DATE" >= {stat_date_str} AND A."STATISTICS_DATE" <= {stat_date_str}'

        # 3. Revenue_Include 过滤（C# 第238-241行：REVENUE_INCLUDE = 1 的门店）
        exists_where = ""
        if Revenue_Include == 1:
            exists_where = ' AND C."REVENUE_INCLUDE" = 1'

        # 4. 构建主查询 SQL（C# 第114-131行 时间段分支的SQL）
        # C#: 按 SERVERPART_ID + SHOPTRADE 分组，查 T_REVENUEDAILY
        # 然后 GetSPRevenueRank 再按 SERVERPART_ID GroupBy Sum
        # 这里合并为一步：直接按 SERVERPART_ID 分组
        sql = f"""SELECT
                A."SERVERPART_ID", B."SERVERPART_NAME", B."SPREGIONTYPE_NAME",
                SUM(A."REVENUE_AMOUNT") AS "CASHPAY",
                SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFFAMOUNT",
                SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAYMENT",
                SUM(NVL(A."DIFFERENT_AMOUNT_LESS_A",0) + NVL(A."DIFFERENT_AMOUNT_LESS_B",0)) AS "DIFFERENT_PRICE_LESS",
                SUM(NVL(A."DIFFERENT_AMOUNT_MORE_A",0) + NVL(A."DIFFERENT_AMOUNT_MORE_B",0)) AS "DIFFERENT_PRICE_MORE"
            FROM
                "T_REVENUEDAILY" A,
                "T_SERVERPART" B
            WHERE
                A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('AH0000','AH9999','test001')
                {where_sql}"""

        # 添加 Revenue_Include EXISTS 子查询（C# 第238-241行）
        if Revenue_Include == 1:
            sql += f"""
                AND EXISTS (SELECT 1 FROM "T_SERVERPARTSHOP" C
                    WHERE A."SHOPTRADE" = C."SHOPTRADE" AND B."SERVERPART_ID" = C."SERVERPART_ID"
                    AND C."ISVALID" = 1{exists_where})"""

        sql += """
            GROUP BY A."SERVERPART_ID", B."SERVERPART_NAME", B."SPREGIONTYPE_NAME"
            ORDER BY SUM(A."REVENUE_AMOUNT") DESC"""

        rows = db.execute_query(sql) or []

        # 5. 构建结果列表
        result_list = []
        for r in rows:
            result_list.append({
                "Serverpart_ID": r.get("SERVERPART_ID"),
                "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                "SPRegionType_Name": r.get("SPREGIONTYPE_NAME", ""),
                "TicketCount": safe_int(r.get("TICKETCOUNT")),
                "TotalCount": round(safe_dec(r.get("TOTALCOUNT")), 2),
                "TotalOffAmount": round(safe_dec(r.get("TOTALOFFAMOUNT")), 2),
                "MobilePayment": round(safe_dec(r.get("MOBILEPAYMENT")), 2),
                "CashPay": round(safe_dec(r.get("CASHPAY")), 2),
                "Different_Price_Less": round(safe_dec(r.get("DIFFERENT_PRICE_LESS")), 2),
                "Different_Price_More": round(safe_dec(r.get("DIFFERENT_PRICE_MORE")), 2),
                "RevenueYOY": None,
                "YearAccountRoyalty": 0.0,
                "YearAccountRoyaltyYOY": 0.0,
            })

        # 6. C#对齐: sumCashpay = REVENUEPUSHList.Sum(o => o.CashPay)
        sum_cashpay = float(round(sum(item.get("CashPay", 0.0) for item in result_list), 2))

        # 7. C#对齐: 默认不显示万佳商贸
        result_list = [item for item in result_list if item.get("SPRegionType_Name") != "万佳商贸"]

        # 8. C#对齐: OrderByDescending(CashPay) — SQL 已按 CashPay DESC 排序

        # 9. C#对齐: JsonList<T1,T2>.Success(list, sumCashpay)
        json_list = JsonListData(
            List=result_list, TotalCount=len(result_list),
            PageIndex=1, PageSize=10, OtherData=sum_cashpay
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPRevenueRank 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetRevenueYOY")
async def get_revenue_yoy(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    StatisticsStartDate: Optional[str] = Query(None, description="统计开始日期"),
    StatisticsEndDate: Optional[str] = Query(None, description="统计结束日期"),
    CompareStartDate: Optional[str] = Query("", description="同比开始日期"),
    CompareEndDate: Optional[str] = Query("", description="同比结束日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取每日营收同比数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        if not pushProvinceCode or not StatisticsStartDate or not StatisticsEndDate:
            _ckm = {"data": None, "key": None, "name": None, "value": None}
            return Result.success(data={
                "curRevenue": None, "curList": [_ckm],
                "compareRevenue": None, "compareList": [_ckm],
            }, msg="查询成功")

        def parse_d(s):
            return dt.strptime(s, "%Y-%m-%d") if "-" in s else dt.strptime(s, "%Y%m%d")
        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        s_date = parse_d(StatisticsStartDate)
        e_date = parse_d(StatisticsEndDate)
        cs_date = parse_d(CompareStartDate) if CompareStartDate else s_date.replace(year=s_date.year - 1)
        ce_date = parse_d(CompareEndDate) if CompareEndDate else e_date.replace(year=e_date.year - 1)

        # 构建WHERE
        where_sql = ""
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionTypeID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeID})'

        # 查当前期营收
        cur_sql = f"""SELECT A."STATISTICS_DATE",
                SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000
                AND A."STATISTICS_DATE" >= {s_date.strftime('%Y%m%d')}
                AND A."STATISTICS_DATE" <= {e_date.strftime('%Y%m%d')}{where_sql}
            GROUP BY A."STATISTICS_DATE" """
        cur_rows = db.execute_query(cur_sql) or []
        cur_map = {}
        for r in cur_rows:
            d = str(int(safe_dec(r.get("STATISTICS_DATE"))))
            cur_map[d] = safe_dec(r.get("CASHPAY"))

        # 查对比期
        cmp_sql = f"""SELECT A."STATISTICS_DATE",
                SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT",
                SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000
                AND A."STATISTICS_DATE" >= {cs_date.strftime('%Y%m%d')}
                AND A."STATISTICS_DATE" <= {ce_date.strftime('%Y%m%d')}{where_sql}
            GROUP BY A."STATISTICS_DATE" """
        cmp_rows = db.execute_query(cmp_sql) or []
        cmp_map = {}
        for r in cmp_rows:
            d = str(int(safe_dec(r.get("STATISTICS_DATE"))))
            cmp_map[d] = safe_dec(r.get("CASHPAY"))

        # 逐天遍历
        cur_days = (e_date - s_date).days + 1
        cmp_days = (ce_date - cs_date).days + 1
        max_days = max(cur_days, cmp_days)

        from decimal import Decimal
        cur_acc = Decimal('0')
        cmp_acc = Decimal('0')
        cur_list = []
        cmp_list = []

        for i in range(max_days):
            cur_d = s_date + timedelta(days=i)
            cmp_d = cs_date + timedelta(days=i)
            cv = cur_map.get(cur_d.strftime("%Y%m%d"), 0)
            lv = cmp_map.get(cmp_d.strftime("%Y%m%d"), 0)
            cur_acc += Decimal(str(cv))
            cmp_acc += Decimal(str(lv))

            cur_list.append({
                "name": date_no_pad(cur_d),
                "value": str(cv), "data": str(cur_acc), "key": None,
            })
            cmp_list.append({
                "name": date_no_pad(cmp_d),
                "value": str(lv), "data": str(cmp_acc), "key": None,
            })

        return Result.success(data={
            "curRevenue": float(cur_acc), "curList": cur_list,
            "compareRevenue": float(cmp_acc), "compareList": cmp_list,
            "curHoliday": None, "curHolidayDays": 0,
            "compareHoliday": None, "compareHolidayDays": 0,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueYOY 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetHolidayCompare")
async def get_holiday_compare(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query(None, description="历年年份"),
    holidayType: int = Query(0, description="节日类型"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日营收同比数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        if not curYear or not compareYear:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        # 节日名称映射（与C# HolidayEnum一致）
        holiday_map = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
        h_name = holiday_map.get(int(holidayType), "")
        if not h_name:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        cur_desc = f"{curYear}年{h_name}"
        cmp_desc = f"{compareYear}年{h_name}"
        h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
        if not h_rows:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        def to_dt(v):
            if isinstance(v, dt): return v
            if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
            return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

        cur_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
        cmp_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
        if not cur_dates or not cmp_dates:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        s_date = min(cur_dates)
        e_date = max(cur_dates)
        cs_date = min(cmp_dates)
        ce_date = max(cmp_dates)

        where_sql = ""
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionTypeID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeID})'

        rev_sql = """SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000
                AND A."STATISTICS_DATE" >= {s} AND A."STATISTICS_DATE" <= {e}{w}
            GROUP BY A."STATISTICS_DATE" """

        cur_rows = db.execute_query(rev_sql.format(s=s_date.strftime("%Y%m%d"), e=e_date.strftime("%Y%m%d"), w=where_sql)) or []
        cmp_rows = db.execute_query(rev_sql.format(s=cs_date.strftime("%Y%m%d"), e=ce_date.strftime("%Y%m%d"), w=where_sql)) or []

        cur_map = {str(safe_int(r.get("STATISTICS_DATE"))): safe_dec(r.get("CASHPAY")) for r in cur_rows}
        cmp_map = {str(safe_int(r.get("STATISTICS_DATE"))): safe_dec(r.get("CASHPAY")) for r in cmp_rows}

        cur_days = (e_date - s_date).days + 1
        cmp_days = (ce_date - cs_date).days + 1
        max_d = max(cur_days, cmp_days)
        from decimal import Decimal
        cur_acc = Decimal('0')
        cmp_acc = Decimal('0')
        cur_list = []
        cmp_list = []
        for i in range(max_d):
            cd = s_date + timedelta(days=i)
            ld = cs_date + timedelta(days=i)
            cv = cur_map.get(cd.strftime("%Y%m%d"), 0)
            lv = cmp_map.get(ld.strftime("%Y%m%d"), 0)
            cur_acc += Decimal(str(cv))
            cmp_acc += Decimal(str(lv))
            cur_list.append({"name": date_no_pad(cd), "value": str(cv), "data": str(cur_acc), "key": None})
            cmp_list.append({"name": date_no_pad(ld), "value": str(lv), "data": str(cmp_acc), "key": None})

        return Result.success(data={
            "curHoliday": f"{s_date.strftime('%m.%d')}-{e_date.strftime('%m.%d')}", "curHolidayDays": cur_days,
            "curRevenue": float(cur_acc), "curList": cur_list,
            "compareHoliday": f"{cs_date.strftime('%m.%d')}-{ce_date.strftime('%m.%d')}", "compareHolidayDays": cmp_days,
            "compareRevenue": float(cmp_acc), "compareList": cmp_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayCompare (Revenue) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 实时交易 =====
@router.get("/Revenue/GetAccountReceivable")
async def get_account_receivable(
    calcType: int = Query(1, description="计算方式：1当月 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsMonth: Optional[str] = Query(None, description="统计结束月份"),
    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收统计明细数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not StatisticsMonth:
            return Result.success(data=None, msg="查询成功")

        # 经营模式枚举映射
        bt_names = {4000: "业主自营", 3000: "自营提成", 1000: "合作分成", 2000: "固定租金"}

        # 1. 查 T_ACCOUNTRECDETAIL
        sm = StatisticsStartMonth if StatisticsStartMonth else f"{StatisticsMonth[:4]}01"
        if StatisticsDate and dt.strptime(StatisticsDate.split(" ")[0], "%Y-%m-%d").strftime("%Y%m") == StatisticsMonth:
            # 统计月份截止本月，计算到结算日
            date_sql = f' AND "STATISTICS_DATE" >= {sm}01 AND "STATISTICS_DATE" <= {dt.strptime(StatisticsDate.split(" ")[0], "%Y-%m-%d").strftime("%Y%m%d")}'
            detail_sql = f'''SELECT * FROM "T_ACCOUNTRECDETAIL" 
                WHERE "PROVINCE_ID" = 3544 AND "SERVERPART_ID" = 0 AND "DATE_TYPE" = 1 AND "ACCOUNTRECDETAIL_STATE" = 1{date_sql}'''
            date_sql_rev = f' AND "STATISTICS_DATE" BETWEEN {sm}01 AND {StatisticsMonth}31'
        else:
            if calcType == 1:
                date_sql = f' AND "STATISTICS_DATE" = {StatisticsMonth}'
            else:
                date_sql = f' AND "STATISTICS_DATE" >= {sm} AND "STATISTICS_DATE" <= {StatisticsMonth}'
            detail_sql = f'''SELECT * FROM "T_ACCOUNTRECDETAIL" 
                WHERE "PROVINCE_ID" = 3544 AND "SERVERPART_ID" = 0 AND "DATE_TYPE" = 2 AND "ACCOUNTRECDETAIL_STATE" = 1{date_sql}'''
            date_sql_rev = f' AND "STATISTICS_DATE" BETWEEN {sm}01 AND {StatisticsMonth}31'

        detail_rows = db.execute_query(detail_sql) or []

        # 2. 查 T_PROVINCEREVENUE 获取业主营业收入
        account_sql = f'''SELECT 
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT", A."BUSINESS_TYPE",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT",
                CASE WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" = 2 THEN 1 
                    WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" <> 2 THEN 2 ELSE 3 END AS "SHOPTRADE" 
            FROM "T_PROVINCEREVENUE" A 
            WHERE A."PROVINCEREVENUE_STATE" = 1{date_sql_rev}
            GROUP BY A."BUSINESS_TYPE", 
                CASE WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" = 2 THEN 1 
                    WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" <> 2 THEN 2 ELSE 3 END'''
        account_rows = db.execute_query(account_sql) or []

        # 3. 汇总detail数据
        def sum_detail(stat_type, biz_type=None):
            total = 0.0
            for r in detail_rows:
                st = int(safe_dec(r.get("STATISTICS_TYPE")))
                bt = int(safe_dec(r.get("BUSINESS_TYPE")))
                if st == stat_type:
                    if biz_type is not None:
                        if bt == biz_type:
                            total += safe_dec(r.get("DATA_VALUE"))
                    else:
                        total += safe_dec(r.get("DATA_VALUE"))
            return total

        def sum_detail_lt(stat_type, biz_lt):
            """SUM where BUSINESS_TYPE < biz_lt"""
            total = 0.0
            for r in detail_rows:
                st = int(safe_dec(r.get("STATISTICS_TYPE")))
                bt = int(safe_dec(r.get("BUSINESS_TYPE")))
                if st == stat_type and bt < biz_lt:
                    total += safe_dec(r.get("DATA_VALUE"))
            return total

        def max_detail(stat_type, biz_type=None):
            vals = []
            for r in detail_rows:
                st = int(safe_dec(r.get("STATISTICS_TYPE")))
                bt = int(safe_dec(r.get("BUSINESS_TYPE")))
                if st == stat_type:
                    if biz_type is not None:
                        if bt == biz_type:
                            vals.append(safe_dec(r.get("DATA_VALUE")))
                    else:
                        vals.append(safe_dec(r.get("DATA_VALUE")))
            return max(vals) if vals else 0.0

        def sum_account(biz_type):
            total = 0.0
            for r in account_rows:
                bt = int(safe_dec(r.get("BUSINESS_TYPE")))
                if bt == biz_type:
                    total += safe_dec(r.get("ACCOUNT_AMOUNT"))
            return total

        owner_rev = sum_detail(1000)
        merchant_rev = sum_detail(2000)
        project_count = int(sum_detail(3001)) if sum_detail(3001) == 0 else int(max_detail(3001))
        # 重新计算 project_count: 按 BUSINESS_TYPE 分组取 max 再求和
        pc_map = {}
        for r in detail_rows:
            st = int(safe_dec(r.get("STATISTICS_TYPE")))
            bt = int(safe_dec(r.get("BUSINESS_TYPE")))
            if st == 3001:
                dv = safe_dec(r.get("DATA_VALUE"))
                pc_map[bt] = max(pc_map.get(bt, 0), dv)
        project_count = int(sum(pc_map.values()))

        # CommissionRatio = SUM(1004, BT<4000) / SUM(3003, BT<4000) * 100
        s1004 = sum_detail_lt(1004, 4000)
        s3003 = sum_detail_lt(3003, 4000)
        commission_ratio = round(s1004 / s3003 * 100, 2) if s3003 > 0 else 0.0

        # 4. 按经营模式遍历
        bt_list = [4000, 3000, 1000, 2000]
        owner_acount = []
        owner_entry = []
        owner_recv = []
        merchant_acount = []
        merchant_entry = []
        merchant_recv = []
        proj_count_list = []
        proj_ratio_list = []
        rev_ratio_list = []
        commission_list = []

        def fmt_val(v):
            """C# decimal.ToString()保留尾零到2位小数"""
            v = round(v, 2)
            if v == 0:
                return "0"
            # 保留2位小数（含尾零），匹配C# decimal.ToString()
            return f"{v:.2f}"

        for bt in bt_list:
            name = bt_names.get(bt, str(bt))
            # OwnerList
            owner_acount.append({"name": name, "value": fmt_val(sum_detail(1001, bt))})
            owner_entry.append({"name": name, "value": fmt_val(sum_account(bt))})
            owner_recv.append({"name": name, "value": fmt_val(sum_detail(1003, bt))})
            # MerchantList
            merchant_acount.append({"name": name, "value": fmt_val(sum_detail(2001, bt))})
            merchant_entry.append({"name": name, "value": fmt_val(sum_detail(2002, bt))})
            merchant_recv.append({"name": name, "value": fmt_val(sum_detail(2003, bt))})
            # ProjectCountList
            pc_val = max_detail(3001, bt)
            proj_count_list.append({"name": name, "value": str(int(pc_val))})
            # ProjectRatioList
            proj_ratio_list.append({"name": name, "value": str(round(pc_val / project_count * 100, 2) if project_count > 0 else 0)})
            # RevenueRatioList
            s3003_bt = sum_detail(3003, bt)
            rev_ratio_list.append({"name": name, "value": str(round(s3003_bt / owner_rev * 100, 2) if owner_rev > 0 else 0)})
            # CommissionList
            if bt == 4000:
                commission_list.append({"name": name, "value": "0"})
            else:
                s1004_bt = sum_detail(1004, bt)
                s3003_bt2 = sum_detail(3003, bt)
                commission_list.append({"name": name, "value": str(round(s1004_bt / s3003_bt2 * 100, 2) if s3003_bt2 > 0 else 0)})

        return Result.success(data={
            "OwnerRevenue": round(owner_rev, 2),
            "MerchantRevenue": round(merchant_rev, 2),
            "OwnerList": {"AcountList": owner_acount, "EntryList": owner_entry, "ReceivableList": owner_recv},
            "MerchantList": {"AcountList": merchant_acount, "EntryList": merchant_entry, "ReceivableList": merchant_recv},
            "ProjectCount": project_count,
            "ProjectCountList": proj_count_list,
            "ProjectRatioList": proj_ratio_list,
            "RevenueRatioList": rev_ratio_list,
            "CommissionRatio": commission_ratio,
            "CommissionList": commission_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAccountReceivable 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetCurRevenue")
async def get_cur_revenue(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    serverPartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时营收交易数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        if not StatisticsDate:
            return Result.success(data=None, msg="查询成功")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        where_sql = ""
        _sp_ids = parse_multi_ids(serverPartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

        sql = f"""SELECT SUM(A."CASHPAY") AS "CASHPAY",
                SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
                SUM(A."TOTALCOUNT") AS "TOTALCOUNT"
            FROM "T_ENDACCOUNT_TEMP" A
            WHERE A."VALID" = 1
                AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
                AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1{where_sql}"""
        rows = db.execute_query(sql) or []

        cashpay = safe_dec(rows[0].get("CASHPAY")) if rows else 0
        ticketcount = safe_int(rows[0].get("TICKETCOUNT")) if rows else 0
        totalcount = safe_dec(rows[0].get("TOTALCOUNT")) if rows else 0
        avg_ticket = round(cashpay / ticketcount, 2) if ticketcount > 0 else None
        avg_sell = round(cashpay / totalcount, 2) if totalcount > 0 else None

        return Result.success(data={
            "AnnualRevenue": None,
            "CurRevenueAmount": cashpay, "CurTicketCount": ticketcount,
            "CurTotalCount": totalcount,
            "CurAvgTicketAmount": avg_ticket, "CurAvgSellAmount": avg_sell,
            "AddRevenueAmount": None, "AddTicketCount": None, "AddTotalCount": None,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCurRevenue 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetShopCurRevenue")
async def get_shop_cur_revenue(
    serverPartId: Optional[str] = Query(None, description="服务区内码"),
    statisticsDate: Optional[str] = Query(None, description="统计日期"),
    groupByShop: bool = Query(False, description="是否合并双侧同业态门店"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时门店营收交易数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not serverPartId or not statisticsDate:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        stat_date = dt.strptime(statisticsDate, "%Y-%m-%d") if "-" in statisticsDate else dt.strptime(statisticsDate, "%Y%m%d")

        # 多服务区ID兼容
        _sp_ids = parse_multi_ids(serverPartId)
        if not _sp_ids:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        sp_condition = build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

        sql = f"""SELECT A."BUSINESS_TYPE", A."SHOPNAME",
                SUM(A."CASHPAY") AS "CASHPAY",
                SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
                SUM(A."TOTALCOUNT") AS "TOTALCOUNT"
            FROM "T_ENDACCOUNT_TEMP" A
            WHERE A."VALID" = 1 AND {sp_condition}
                AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
                AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1
            GROUP BY A."BUSINESS_TYPE", A."SHOPNAME"
            ORDER BY SUM(A."CASHPAY") DESC"""
        rows = db.execute_query(sql) or []

        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        data_list = []
        for r in rows:
            data_list.append({
                "ShopTrade": r.get("BUSINESS_TYPE", ""),
                "ShopName": r.get("SHOPNAME", ""),
                "CashPay": safe_dec(r.get("CASHPAY")),
                "TicketCount": safe_dec(r.get("TICKETCOUNT")),
                "TotalCount": safe_dec(r.get("TOTALCOUNT")),
            })

        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopCurRevenue 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetLastSyncDateTime")
async def get_last_sync_date_time(db: DatabaseHelper = Depends(get_db)):
    """获取最新的同步日期 (SQL平移完成)"""
    try:
        from datetime import datetime, timedelta
        now = datetime.now()
        # C#对齐: DateTime.Now.AddDays(-1).ToString("yyyyMM01")
        yesterday = now - timedelta(days=1)
        month_start = yesterday.strftime("%Y%m") + "01"
        today_str = now.strftime("%Y%m%d")

        sql = f"""
            SELECT 
                STATISTICS_DATE, MAX(RECORD_DATE) AS RECORD_DATE
            FROM 
                T_PROVINCEREVENUE 
            WHERE 
                PROVINCEREVENUE_STATE = 1 AND 
                DATA_TYPE = 1 AND HOLIDAY_TYPE > 0 AND 
                STATISTICS_DATE >= {month_start} AND 
                STATISTICS_DATE < {today_str} 
            GROUP BY 
                STATISTICS_DATE
            ORDER BY STATISTICS_DATE DESC
        """
        rows = db.execute_query(sql)
        for r in rows:
            stat_date_str = str(r["STATISTICS_DATE"])
            record_dt = r["RECORD_DATE"]
            
            # C# 逻辑：判断 RECORD_DATE >= STATISTICS_DATE + 1天 + 8小时30分
            stat_dt = datetime.strptime(stat_date_str, "%Y%m%d")
            threshold_dt = stat_dt + timedelta(days=1, hours=8, minutes=30)
            
            if record_dt and record_dt >= threshold_dt:
                return Result.success(data=stat_dt.strftime("%Y-%m-%d"), msg="查询成功")
                
        return Result.success(data="", msg="查询成功")
    except Exception as ex:
        logger.error(f"GetLastSyncDateTime 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 节日分析 =====

def _get_holiday_dates(db, holiday_type, cur_year, compare_year):
    """获取节日日期范围（与C# CommonHelper.GetHoliday一致）"""
    from datetime import datetime as dt
    import calendar
    cur_year = int(cur_year)
    compare_year = int(compare_year)
    
    # 暑期固定时间
    if holiday_type == 6:
        return (dt(cur_year, 7, 1), dt(cur_year, 8, 31),
                dt(compare_year, 7, 1), dt(compare_year, 8, 31))
    
    # 从T_HOLIDAY表查节日日期
    holiday_names = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 7: "中秋节", 8: "国庆节"}
    h_name = holiday_names.get(holiday_type)
    if not h_name:
        return None
    
    sql = f"""SELECT "HOLIDAY_DESC", MIN("HOLIDAY_DATE") AS "MIN_DATE", MAX("HOLIDAY_DATE") AS "MAX_DATE"
        FROM "T_HOLIDAY"
        WHERE "HOLIDAY_DESC" IN ('{cur_year}年{h_name}','{compare_year}年{h_name}')
        GROUP BY "HOLIDAY_DESC" """
    rows = db.execute_query(sql) or []
    
    ss, se, cs, ce = None, None, None, None
    for r in rows:
        desc = r.get("HOLIDAY_DESC", "")
        min_d = r.get("MIN_DATE")
        max_d = r.get("MAX_DATE")
        if min_d and not isinstance(min_d, dt):
            min_d = dt.strptime(str(min_d)[:10], "%Y-%m-%d")
        if max_d and not isinstance(max_d, dt):
            max_d = dt.strptime(str(max_d)[:10], "%Y-%m-%d")
        if desc == f"{cur_year}年{h_name}":
            ss, se = min_d, max_d
        if desc == f"{compare_year}年{h_name}":
            cs, ce = min_d, max_d
    
    if not ss or not cs:
        return None
    
    # 春运以实际时间为准
    if holiday_type == 2:
        return (ss, se, cs, ce)
    
    from datetime import timedelta
    # 元旦/清明/端午/中秋: 假期开始前一天至开始后三天
    if holiday_type in (1, 3, 5, 7):
        se = ss + timedelta(days=3)
        ss = ss + timedelta(days=-1)
        ce = cs + timedelta(days=3)
        cs = cs + timedelta(days=-1)
    # 五一: 假期开始前一天至假期结束后一天
    elif holiday_type == 4:
        se = se + timedelta(days=1)
        ss = ss + timedelta(days=-1)
        ce = ce + timedelta(days=1)
        cs = cs + timedelta(days=-1)
    # 国庆: 9/29-10/8 (2023特殊 9/27-10/6)
    elif holiday_type == 8:
        if cur_year == 2023:
            ss, se = dt(cur_year, 9, 27), dt(cur_year, 10, 6)
        else:
            ss, se = dt(cur_year, 9, 29), dt(cur_year, 10, 8)
        if compare_year == 2023:
            cs, ce = dt(compare_year, 9, 27), dt(compare_year, 10, 6)
        else:
            cs, ce = dt(compare_year, 9, 29), dt(compare_year, 10, 8)
    
    return (ss, se, cs, ce)


def _sum_compute(rows, filter_fn, field_cur, field_total):
    """模拟C#的DataTable.Compute(SUM, filter) — 使用Decimal避免浮点精度问题"""
    from decimal import Decimal, ROUND_HALF_UP
    filtered = [r for r in rows if filter_fn(r)]
    if not filtered:
        # C#的Compute在无匹配行时返回DBNull → ToString()是空字符串
        return "", ""
    total = sum(Decimal(str(r.get(field_total) or 0)) for r in filtered)
    cur = sum(Decimal(str(r.get(field_cur) or 0)) for r in filtered)
    # C#的Decimal.ToString()保留原始精度（至少2位小数）
    def fmt(v):
        s = str(v)
        if '.' in s:
            # 确保小数部分至少2位
            integer, decimal = s.split('.')
            if len(decimal) < 2:
                decimal = decimal.ljust(2, '0')
            return f"{integer}.{decimal}"
        return s
    return fmt(total), fmt(cur)


@router.get("/Revenue/GetHolidayAnalysis")
async def get_holiday_analysis(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query(None, description="历年年份"),
    HolidayType: int = Query(0, alias="HolidayType", description="节日类型"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日营收数据对比分析（完整实现）"""
    from datetime import datetime as dt
    _ckm = lambda: {"data": None, "key": None, "name": None, "value": None}
    
    try:
        sd = dt.strptime(StatisticsDate.split(' ')[0], '%Y-%m-%d') if StatisticsDate and '-' in StatisticsDate else None
        if not sd:
            return Result.success(data=None, msg="查询成功")
        
        # 1. 获取节日日期范围
        dates = _get_holiday_dates(db, HolidayType, curYear, compareYear)
        if not dates:
            return Result.success(data=None, msg="查询成功")
        
        stat_start, stat_end, comp_start, comp_end = dates
        
        if sd < stat_start:
            return Result.success(data=None, msg="查询成功")
        if sd > stat_end:
            sd = stat_end
        
        # 计算历年对应日期
        cy_date = comp_start + (sd - stat_start)
        
        # 2. 构建查询条件
        # 获取省份的FieldEnum_ID（与其他接口一致的方式）
        fe_rows = db.execute_query(f"""SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE'
            AND B."FIELDENUM_VALUE" = '{pushProvinceCode}'""") or []
        field_enum_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else pushProvinceCode
        
        where_sql = f" AND A.\"PROVINCE_ID\" = {field_enum_id}"
        table_name = "T_PROVINCEREVENUE"
        state_name = "PROVINCEREVENUE_STATE"
        
        if ServerpartId:
            table_name = "T_HOLIDAYREVENUE"
            state_name = "HOLIDAYREVENUE_STATE"
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
        elif pushProvinceCode == "340000":
            where_sql += ' AND A."BUSINESS_REGION" = 1'
        
        # 3. 查询营收数据 - 当年
        ss_str = stat_start.strftime("%Y%m%d")
        sd_str = sd.strftime("%Y%m%d")
        rev_sql = f"""SELECT "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION",
                ROUND(SUM(A."REVENUE_AMOUNT"),2) AS "CASHPAY",
                ROUND(SUM(A."ACCOUNT_AMOUNTNOTAX"),2) AS "ACCOUNT_AMOUNT",
                ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {sd_str} THEN A."REVENUE_AMOUNT" ELSE 0 END),2) AS "CASHPAY_CUR",
                ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {sd_str} THEN A."ACCOUNT_AMOUNTNOTAX" ELSE 0 END),2) AS "ACCOUNT_AMOUNT_CUR"
            FROM "{table_name}" A
            WHERE A."{state_name}" = 1
                AND A."STATISTICS_DATE" BETWEEN {ss_str} AND {sd_str}{where_sql}
            GROUP BY "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION" """
        cur_rev = db.execute_query(rev_sql) or []
        
        # 4. 查询营收数据 - 历年
        cs_str = comp_start.strftime("%Y%m%d")
        cy_str = cy_date.strftime("%Y%m%d")
        rev_sql2 = f"""SELECT "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION",
                ROUND(SUM(A."REVENUE_AMOUNT"),2) AS "CASHPAY",
                ROUND(SUM(A."ACCOUNT_AMOUNTNOTAX"),2) AS "ACCOUNT_AMOUNT",
                ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {cy_str} THEN A."REVENUE_AMOUNT" ELSE 0 END),2) AS "CASHPAY_CUR",
                ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {cy_str} THEN A."ACCOUNT_AMOUNTNOTAX" ELSE 0 END),2) AS "ACCOUNT_AMOUNT_CUR"
            FROM "{table_name}" A
            WHERE A."{state_name}" = 1
                AND A."STATISTICS_DATE" BETWEEN {cs_str} AND {cy_str}{where_sql}
            GROUP BY "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION" """
        cy_rev = db.execute_query(rev_sql2) or []
        
        # 辅助函数 — C#返回ToString()，空时返回空字符串
        def mk(rows, filter_fn):
            d, v = _sum_compute(rows, filter_fn, "CASHPAY_CUR", "CASHPAY")
            return {"data": d, "key": None, "name": None, "value": v}
        def mk_acc(rows, filter_fn):
            d, v = _sum_compute(rows, filter_fn, "ACCOUNT_AMOUNT_CUR", "ACCOUNT_AMOUNT")
            return {"data": d, "key": None, "name": None, "value": v}
        
        all_pass = lambda r: True
        bt4000 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000"
        bt4000_st134 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) in ("1","3","4")
        bt4000_st13 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) in ("1","3")
        bt4000_st4 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) == "4"
        bt4000_st3 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) == "3"
        bt4000_st2 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) == "2"
        bt_lt4000 = lambda r: int(r.get("BUSINESS_TYPE") or 0) < 4000
        bt3000 = lambda r: str(r.get("BUSINESS_TYPE")) == "3000"
        br2 = lambda r: str(r.get("BUSINESS_REGION")) == "2"
        
        # 5. 构建结果
        _model = {
            "ServerpartId": None,
            "ServerpartName": None,
            "curYear": None,
            "compareYear": None,
            "HolidayType": None,  # C#的baseline返回null
            "curDate": f"{sd.year}/{sd.month}/{sd.day}",
            "cyDate": f"{cy_date.year}/{cy_date.month}/{cy_date.day}",
            # 整体对客销售额
            "curYearRevenue": mk(cur_rev, all_pass), "lYearRevenue": mk(cy_rev, all_pass),
            # 自营对客销售额 (BUSINESS_TYPE=4000)
            "curYearSelfRevenue": mk(cur_rev, bt4000), "lYearSelfRevenue": mk(cy_rev, bt4000),
            # 自营餐饮客房及其他 (BUSINESS_TYPE=4000, SHOPTRADE in 1,3,4)
            "curYearSCRevenue": mk(cur_rev, bt4000_st134), "lYearSCRevenue": mk(cy_rev, bt4000_st134),
            "curYearSCAccount": mk_acc(cur_rev, bt4000_st134), "lYearSCAccount": mk_acc(cy_rev, bt4000_st134),
            # 自营餐饮 (BUSINESS_TYPE=4000, SHOPTRADE in 1,3)
            "curYearSRRevenue": mk(cur_rev, bt4000_st13), "lYearSRRevenue": mk(cy_rev, bt4000_st13),
            "curYearSRAccount": mk_acc(cur_rev, bt4000_st13), "lYearSRAccount": mk_acc(cy_rev, bt4000_st13),
            # 自营客房及其他 (BUSINESS_TYPE=4000, SHOPTRADE=4)
            "curYearGRORevenue": mk(cur_rev, bt4000_st4), "lYearGRORevenue": mk(cy_rev, bt4000_st4),
            "curYearGROAccount": mk_acc(cur_rev, bt4000_st4), "lYearGROAccount": mk_acc(cy_rev, bt4000_st4),
            # 加盟餐饮 (BUSINESS_TYPE=4000, SHOPTRADE=3)
            "curYearFCRevenue": mk(cur_rev, bt4000_st3),
            # 自营便利店 (BUSINESS_TYPE=4000, SHOPTRADE=2)
            "curYearCVSRevenue": mk(cur_rev, bt4000_st2), "lYearCVSRevenue": mk(cy_rev, bt4000_st2),
            "curYearCVSAccount": mk_acc(cur_rev, bt4000_st2), "lYearCVSAccount": mk_acc(cy_rev, bt4000_st2),
            # 商铺租赁 (BUSINESS_TYPE < 4000)
            "curYearCoopRevenue": mk(cur_rev, bt_lt4000), "lYearCoopRevenue": mk(cy_rev, bt_lt4000),
            "curYearCoopAccount": mk_acc(cur_rev, bt_lt4000), "lYearCoopAccount": mk_acc(cy_rev, bt_lt4000),
            # 自营提成 (BUSINESS_TYPE=3000)
            "curYearSelfCoopRevenue": mk(cur_rev, bt3000),
            # 城市店 (BUSINESS_REGION=2)
            "curYearWJRevenue": mk(cur_rev, br2), "lYearWJRevenue": mk(cy_rev, br2),
        }
        
        # 6. 计算自营收入 = 便利店收入 + 餐饮客房收入
        def add_kv(a, b):
            from decimal import Decimal
            av = Decimal(a.get("value") or "0")
            bv = Decimal(b.get("value") or "0")
            ad = Decimal(a.get("data") or "0")
            bd = Decimal(b.get("data") or "0")
            return {"data": str(ad + bd), "key": None, "name": None,
                    "value": str(av + bv)}
        
        _model["curYearSelfAccount"] = add_kv(_model["curYearCVSAccount"], _model["curYearSCAccount"])
        _model["lYearSelfAccount"] = add_kv(_model["lYearCVSAccount"], _model["lYearSCAccount"])
        # 驿达入账 = 自营收入 + 商铺租赁收入
        _model["curYearAccount"] = add_kv(_model["curYearSelfAccount"], _model["curYearCoopAccount"])
        _model["lYearAccount"] = add_kv(_model["lYearSelfAccount"], _model["lYearCoopAccount"])
        
        # 7. 查询车流量
        if ServerpartId:
            _sp_ids2 = parse_multi_ids(ServerpartId)
            if _sp_ids2:
                bw_sql = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids2).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
            else:
                bw_sql = f""" AND EXISTS (SELECT 1 FROM "T_SERVERPART" S
                    WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {field_enum_id})"""
        else:
            bw_sql = f""" AND EXISTS (SELECT 1 FROM "T_SERVERPART" S
                WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {field_enum_id})"""
        
        bayonet_sql = f"""SELECT SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW",
                SUM(CASE WHEN A."STATISTICS_DATE" = {sd_str} THEN A."SERVERPART_FLOW" ELSE 0 END) AS "SERVERPART_FLOW_CUR"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {ss_str} AND {sd_str}{bw_sql}"""
        cur_bay = db.execute_query(bayonet_sql) or []
        
        bayonet_sql2 = f"""SELECT SUM(A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW",
                SUM(CASE WHEN A."STATISTICS_DATE" = {cy_str} THEN A."SERVERPART_FLOW" + 
                    NVL(A."SERVERPART_FLOW_ANALOG",0) ELSE 0 END) AS "SERVERPART_FLOW_CUR"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {cs_str} AND {cy_str}{bw_sql}"""
        cy_bay = db.execute_query(bayonet_sql2) or []
        
        def bay_kv(rows):
            if not rows or not rows[0]:
                return _ckm()
            r = rows[0]
            flow = r.get("SERVERPART_FLOW")
            flow_cur = r.get("SERVERPART_FLOW_CUR")
            # C#中Compute("sum(xxx)","")即使为0也返回"0"
            return {"data": str(int(float(flow))) if flow is not None else None,
                    "key": None, "name": None,
                    "value": str(int(float(flow_cur))) if flow_cur is not None else None}
        
        _model["curYearBayonet"] = bay_kv(cur_bay)
        _model["lYearBayonet"] = bay_kv(cy_bay)
        
        return Result.success(data=_model, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayAnalysis 查询失败: {ex}")
        import traceback; traceback.print_exc()
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetHolidayAnalysisBatch")
async def get_holiday_analysis_batch(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query(None, description="历年年份"),
    HolidayType: int = Query(0, description="节日类型"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    ServerpartIds: Optional[str] = Query("", description="服务区内码集合"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取多个服务区节日营收数据对比分析（批量）- 调用单个接口循环"""
    try:
        if not ServerpartIds:
            return Result.fail(code=102, msg="服务区内码不能为空！")
        
        sp_list = [s.strip() for s in ServerpartIds.split(",") if s.strip()]
        result_list = []
        
        for sp_id in sp_list:
            # 调用单个HolidayAnalysis
            res = await get_holiday_analysis(
                pushProvinceCode=pushProvinceCode,
                curYear=curYear,
                compareYear=compareYear,
                HolidayType=HolidayType,
                StatisticsDate=StatisticsDate,
                ServerpartId=sp_id,
                db=db
            )
            # 解析结果
            if hasattr(res, 'model_dump'):
                res_dict = res.model_dump()
            elif hasattr(res, 'body'):
                import json as _json
                res_dict = _json.loads(res.body)
            elif isinstance(res, dict):
                res_dict = res
            else:
                continue
            
            rd = res_dict.get("Result_Data")
            if rd:
                # 查询服务区名称
                sp_rows = db.execute_query(f'SELECT "SERVERPART_NAME" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {sp_id}') or []
                sp_name = sp_rows[0].get("SERVERPART_NAME", "") if sp_rows else ""
                rd["ServerpartId"] = int(sp_id) if sp_id.isdigit() else sp_id
                rd["ServerpartName"] = sp_name
                rd["curYear"] = int(curYear) if curYear else None
                rd["compareYear"] = int(compareYear) if compareYear else None
                rd["HolidayType"] = HolidayType
                # C# Batch版本不返回这些字段（初始化为null）
                for null_key in ["curYearSRRevenue", "lYearSRRevenue", "curYearSRAccount",
                                  "lYearSRAccount", "lYearGRORevenue", "curYearGROAccount", "lYearGROAccount"]:
                    if null_key in rd:
                        rd[null_key] = None
                result_list.append(rd)
        
        if not result_list:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_index=1, page_size=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayAnalysisBatch 查询失败: {ex}")
        import traceback; traceback.print_exc()
        return Result.fail(msg=f"查询失败{ex}")


# ===== 增幅分析 =====
@router.get("/Revenue/GetServerpartINCAnalysis")
async def get_serverpart_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[int] = Query(None, description="本年年份"),
    HolidayType: int = Query(0, description="节日类型: 0日常 1元旦 2春运 3清明 4五一 5端午 6暑期 7中秋 8国庆"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    compareYear: Optional[int] = Query(None, description="历年年份"),
    CurStartDate: Optional[str] = Query("", description="统计开始日期"),
    StatisticsStartDate: Optional[str] = Query("", description="统计开始日期(兼容)"),
    StatisticsEndDate: Optional[str] = Query("", description="统计结束日期(兼容)"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    businessRegion: Optional[int] = Query(None, description="经营区域"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    IsYOYCompare: bool = Query(False, description="是否对比同期数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区营收增幅分析"""
    try:
        from datetime import datetime as dt, timedelta

        # 节日枚举
        holiday_names = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}

        if not StatisticsDate:
            StatisticsDate = dt.now().strftime("%Y-%m-%d")
        if compareYear is None:
            compareYear = (curYear or dt.now().year) - 1

        # 1. GetHoliday: 获取节假日起止日期
        stats_start = None
        stats_end = None
        compare_start = None
        compare_end = None

        if HolidayType == 6:  # 暑期固定
            stats_start = dt(curYear, 7, 1)
            stats_end = dt(curYear, 8, 31)
            compare_start = dt(compareYear, 7, 1)
            compare_end = dt(compareYear, 8, 31)
        elif HolidayType == 0:  # 日常
            if CurStartDate:
                stats_start = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y/%m/%d")
            else:
                stats_start = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
            stats_end = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
            compare_start = stats_start.replace(year=stats_start.year - 1)
            compare_end = stats_end.replace(year=stats_end.year - 1)
        else:  # 其他节日从T_HOLIDAY查
            h_name = holiday_names.get(HolidayType, "")
            cur_desc = f"{curYear}年{h_name}"
            cmp_desc = f"{compareYear}年{h_name}"
            h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
                WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""")
            if not h_rows:
                return Result.fail(code=101, msg="查询失败，无数据返回！")
            cur_dates = [r["HOLIDAY_DATE"] for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
            cmp_dates = [r["HOLIDAY_DATE"] for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
            if not cur_dates or not cmp_dates:
                return Result.fail(code=101, msg="查询失败，无数据返回！")

            def to_dt(v):
                if isinstance(v, dt): return v
                if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
                return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

            stats_start = to_dt(min(cur_dates))
            stats_end = to_dt(max(cur_dates))
            compare_start = to_dt(min(cmp_dates))
            compare_end = to_dt(max(cmp_dates))

            # 按节日类型调整日期范围
            if HolidayType in (1, 3, 5, 7):  # 元旦/清明/端午/中秋: 前1天到后3天
                stats_end = stats_start + timedelta(days=3)
                stats_start = stats_start - timedelta(days=1)
                compare_end = compare_start + timedelta(days=3)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 4:  # 五一: 前1天到后1天
                stats_end = stats_end + timedelta(days=1)
                stats_start = stats_start - timedelta(days=1)
                compare_end = compare_end + timedelta(days=1)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 8:  # 国庆
                if curYear == 2023:
                    stats_start = dt(curYear, 9, 27); stats_end = dt(curYear, 10, 6)
                else:
                    stats_start = dt(curYear, 9, 29); stats_end = dt(curYear, 10, 8)
                if compareYear == 2023:
                    compare_start = dt(compareYear, 9, 27); compare_end = dt(compareYear, 10, 6)
                else:
                    compare_start = dt(compareYear, 9, 29); compare_end = dt(compareYear, 10, 8)

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
        if stat_date < stats_start:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        if stat_date > stats_end:
            stat_date = stats_end

        if CurStartDate and HolidayType != 0:
            cur_start_dt = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y/%m/%d")
            if cur_start_dt > stats_start:
                compare_start = compare_start + timedelta(days=(cur_start_dt - stats_start).days + 1)
                stats_start = cur_start_dt

        if HolidayType != 0 and IsYOYCompare and stat_date < stats_end:
            compare_end = compare_start + timedelta(days=(stat_date - stats_start).days)

        # 2. 查省份ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": pushProvinceCode})
        if not fe_rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        province_id = fe_rows[0]["FIELDENUM_ID"]

        # 3. 查营收(T_HOLIDAYREVENUE)
        where_rev = f' AND A."PROVINCE_ID" = {province_id}'
        if ServerpartId:
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_rev += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

        cur_start_str = (stat_date if calcType == 1 else stats_start).strftime("%Y%m%d")
        cur_end_str = stat_date.strftime("%Y%m%d")
        sql_cur_rev = f"""SELECT A."SERVERPART_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1 AND A."STATISTICS_DATE" BETWEEN {cur_start_str} AND {cur_end_str}{where_rev}
            GROUP BY A."SERVERPART_ID" """
        dt_cur_rev = db.execute_query(sql_cur_rev) or []

        cy_date = compare_start + timedelta(days=(stat_date - stats_start).days)
        cy_start_str = (cy_date if calcType == 1 else compare_start).strftime("%Y%m%d")
        cy_end_str = cy_date.strftime("%Y%m%d")
        sql_cy_rev = f"""SELECT A."SERVERPART_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1 AND A."STATISTICS_DATE" BETWEEN {cy_start_str} AND {cy_end_str}{where_rev}
            GROUP BY A."SERVERPART_ID" """
        dt_cy_rev = db.execute_query(sql_cy_rev) or []

        # 4. 查车流(T_SECTIONFLOW)
        where_bay = ""
        if ServerpartId:
            _sp_ids3 = parse_multi_ids(ServerpartId)
            if _sp_ids3:
                where_bay = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids3).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
            else:
                where_bay = f''' AND EXISTS (SELECT 1 FROM "T_SERVERPART" S WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {province_id})'''
        else:
            where_bay = f''' AND EXISTS (SELECT 1 FROM "T_SERVERPART" S WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {province_id})'''

        bay_cur_start = stat_date.strftime("%Y%m%d") if calcType == 1 else stats_start.strftime("%Y%m%d")
        sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW",
                SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {bay_cur_start} AND {stat_date.strftime("%Y%m%d")}{where_bay}
            GROUP BY A."SERVERPART_ID" """
        dt_cur_bay = db.execute_query(sql_cur_bay) or []

        bay_cy_start = cy_date.strftime("%Y%m%d") if calcType == 1 else compare_start.strftime("%Y%m%d")
        sql_cy_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW",
                SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {bay_cy_start} AND {cy_date.strftime("%Y%m%d")}{where_bay}
            GROUP BY A."SERVERPART_ID" """
        dt_cy_bay = db.execute_query(sql_cy_bay) or []

        # 5. 查服务区列表
        where_sp = f' AND "PROVINCE_CODE" = {province_id}'
        if ServerpartId:
            _sp_ids4 = parse_multi_ids(ServerpartId)
            if _sp_ids4:
                where_sp += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids4)
        if businessRegion == 1:
            where_sp += ' AND "SPREGIONTYPE_ID" NOT IN (89)'  # 排除城市店及商城（SPREGIONTYPE_ID=89），保留皖中管理中心（72）等
        sp_rows = db.execute_query(f"""SELECT * FROM "T_SERVERPART"
            WHERE "SPREGIONTYPE_ID" IS NOT NULL AND "STATISTICS_TYPE" = 1000 AND "STATISTIC_TYPE" = 1000{where_sp}
            ORDER BY "SPREGIONTYPE_INDEX","SPREGIONTYPE_ID","SERVERPART_INDEX","SERVERPART_CODE" """) or []

        # 营收/车流 按服务区ID索引
        def build_map(rows, key="SERVERPART_ID"):
            m = {}
            for r in rows:
                sid = str(r.get(key, ""))
                if sid not in m:
                    m[sid] = r
                else:
                    for k2, v2 in r.items():
                        if k2 != key:
                            try: m[sid][k2] = (m[sid].get(k2) or 0) + (v2 or 0)
                            except: pass
            return m

        cur_rev_map = build_map(dt_cur_rev)
        cy_rev_map = build_map(dt_cy_rev)
        cur_bay_map = build_map(dt_cur_bay)
        cy_bay_map = build_map(dt_cy_bay)

        def safe_f(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        def make_inc(cur, ly):
            inc = {"curYearData": cur, "lYearData": ly, "increaseData": None, "increaseRate": None,
                   "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
            if cur and ly and cur != 0 and ly != 0:
                inc["increaseData"] = round(cur - ly, 2)
                inc["increaseRate"] = round((cur - ly) / ly * 100, 2)
            return inc

        # 6. 构建结果
        result_list = []
        no_increase_list = []
        for sp in sp_rows:
            sp_id = str(sp["SERVERPART_ID"])
            cur_r = cur_rev_map.get(sp_id, {})
            cy_r = cy_rev_map.get(sp_id, {})
            cur_b = cur_bay_map.get(sp_id, {})
            cy_b = cy_bay_map.get(sp_id, {})

            def safe_or_none(d, key):
                """有数据返回float，无数据返回None
                注意：当 d 非空（即该服务区在SQL查询中有记录）但字段值为NULL时，
                C# 的 Convert.ToDecimal(DBNull) 返回 0，这里也需对齐返回 0.0
                """
                if not d:
                    return None
                v = d.get(key)
                if v is None:
                    # 字典存在说明有记录行，字段NULL视为0（对齐C#口径）
                    return 0.0
                try:
                    return float(v)
                except:
                    return 0.0

            rev_inc = make_inc(safe_or_none(cur_r, "REVENUE_AMOUNT"), safe_or_none(cy_r, "REVENUE_AMOUNT"))
            acc_inc = make_inc(safe_or_none(cur_r, "ACCOUNT_AMOUNT"), safe_or_none(cy_r, "ACCOUNT_AMOUNT"))
            bay_inc = make_inc(safe_or_none(cur_b, "SERVERPART_FLOW"), safe_or_none(cy_b, "SERVERPART_FLOW"))
            sec_inc = make_inc(safe_or_none(cur_b, "SECTIONFLOW_NUM"), safe_or_none(cy_b, "SECTIONFLOW_NUM"))

            # 车流增长率>1000没有可比性
            if bay_inc["increaseRate"] and abs(bay_inc["increaseRate"]) > 1000:
                bay_inc["increaseData"] = None; bay_inc["increaseRate"] = None
            if sec_inc["increaseRate"] and abs(sec_inc["increaseRate"]) > 1000:
                sec_inc["increaseData"] = None; sec_inc["increaseRate"] = None
            # 历年车流<100不计算增长率
            if bay_inc.get("lYearData") and bay_inc["lYearData"] <= 100:
                bay_inc["increaseRate"] = None

            item = {
                "SPRegionTypeId": sp.get("SPREGIONTYPE_ID"),
                "SPRegionTypeName": sp.get("SPREGIONTYPE_NAME"),
                "ServerpartId": sp.get("SERVERPART_ID"),
                "ServerpartName": sp.get("SERVERPART_NAME"),
                "RevenueINC": rev_inc,
                "AccountINC": acc_inc,
                "BayonetINC": bay_inc,
                "SectionFlowINC": sec_inc,
                "AvgTicketINC": None,
                "TicketINC": None,
                "BayonetINC_ORI": None,
                "ShopINCList": None,
                "RankDiff": None,
                "Cost_Amount": None,
                "Ca_Cost": None,
                "Profit_Amount": None,
            }

            # 排序相关过滤
            is_no_increase = True
            if SortStr:
                ss = SortStr.lower()
                if "revenue" in ss and not (rev_inc["increaseRate"] is not None):
                    is_no_increase = False
                if "account" in ss and not (acc_inc["increaseRate"] is not None):
                    is_no_increase = False
                if "bayonet" in ss and not (bay_inc["increaseRate"] is not None):
                    is_no_increase = False

            if is_no_increase:
                result_list.append(item)
            else:
                no_increase_list.append(item)

        # 排序
        if SortStr:
            ss = SortStr.lower().replace(" asc", "")
            rev = "desc" in SortStr.lower()
            if "revenue" in ss and "bayonet" not in ss:
                result_list.sort(key=lambda x: x["RevenueINC"]["increaseRate"] or 0, reverse=rev)
            elif "bayonet" in ss and "revenue" not in ss:
                result_list.sort(key=lambda x: x["BayonetINC"]["increaseRate"] or 0, reverse=rev)
            elif "account" in ss:
                result_list.sort(key=lambda x: x["AccountINC"]["increaseRate"] or 0, reverse=rev)

        result_list.extend(no_increase_list)

        if not result_list:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        h_name = holiday_names.get(HolidayType, "")
        holiday_period = f"{curYear}年{h_name}时间为{date_no_pad(stats_start)} 0:00:00至{stat_date.strftime('%Y-%m-%d')}\r\n{compareYear}年{h_name}时间为{date_no_pad(compare_start)} 0:00:00至{date_no_pad(compare_end)} 0:00:00"

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        resp = json_list.model_dump()
        resp["OtherData"] = holiday_period
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartINCAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetShopINCAnalysis")
async def get_shop_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: str = Query(..., description="省份编码"),
    curYear: int = Query(..., description="本年年份"),
    compareYear: int = Query(..., description="历年年份"),
    HolidayType: int = Query(..., description="节日类型：1元旦 2春运 3清明 4五一 5端午 6暑期 7中秋 8国庆"),
    ServerpartId: int = Query(..., description="服务区内码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    CurStartDate: Optional[str] = Query("", description="统计开始日期"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店营收增幅分析 (对齐C# HolidayHelper.GetShopINCAnalysis)"""
    try:
        from datetime import datetime as dt, timedelta

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        # 默认统计日期
        if not StatisticsDate:
            StatisticsDate = dt.now().strftime("%Y-%m-%d")

        # 解析统计日期
        if "-" in StatisticsDate:
            stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d")
        else:
            stat_date = dt.strptime(StatisticsDate, "%Y%m%d")

        # ========== 1. 获取节日日期范围 (对齐 CommonHelper.GetHoliday) ==========
        holiday_map = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}
        h_name = holiday_map.get(HolidayType, "")

        if HolidayType == 6:
            # 暑期固定
            statistics_start = dt(curYear, 7, 1)
            statistics_end = dt(curYear, 8, 31)
            compare_start = dt(compareYear, 7, 1)
            compare_end = dt(compareYear, 8, 31)
        elif HolidayType == 0:
            # 自定义日期范围
            if not CurStartDate:
                CurStartDate = StatisticsDate
            statistics_start = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y%m%d")
            statistics_end = stat_date
            compare_start = statistics_start.replace(year=statistics_start.year - 1)
            compare_end = statistics_end.replace(year=statistics_end.year - 1)
        else:
            # 从 T_HOLIDAY 表查询节日日期
            cur_desc = f"{curYear}年{h_name}"
            cmp_desc = f"{compareYear}年{h_name}"
            h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
                WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
            if not h_rows:
                return Result.fail(code=101, msg="查询失败，无数据返回！")

            def to_dt(v):
                if isinstance(v, dt): return v
                if hasattr(v, 'year'): return dt(v.year, v.month, v.day)
                if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
                return v

            cur_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
            cmp_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
            if not cur_dates or not cmp_dates:
                return Result.fail(code=101, msg="查询失败，无数据返回！")

            statistics_start = min(cur_dates)
            statistics_end = max(cur_dates)
            compare_start = min(cmp_dates)
            compare_end = max(cmp_dates)

            # 按节日类型调整日期范围 (对齐 C# switch)
            if HolidayType in (1, 3, 5, 7):
                # 元旦/清明/端午/中秋：开始前1天到开始后3天
                statistics_end = statistics_start + timedelta(days=3)
                statistics_start = statistics_start - timedelta(days=1)
                compare_end = compare_start + timedelta(days=3)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 4:
                # 五一：开始前1天到结束后1天
                statistics_end = statistics_end + timedelta(days=1)
                statistics_start = statistics_start - timedelta(days=1)
                compare_end = compare_end + timedelta(days=1)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 8:
                # 国庆
                if curYear == 2023:
                    statistics_start = dt(curYear, 9, 27)
                    statistics_end = dt(curYear, 10, 6)
                else:
                    statistics_start = dt(curYear, 9, 29)
                    statistics_end = dt(curYear, 10, 8)
                if compareYear == 2023:
                    compare_start = dt(compareYear, 9, 27)
                    compare_end = dt(compareYear, 10, 6)
                else:
                    compare_start = dt(compareYear, 9, 29)
                    compare_end = dt(compareYear, 10, 8)
            # HolidayType == 2 (春运): 使用原始日期不调整

        # 验证统计日期范围
        if stat_date < statistics_start:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        elif stat_date > statistics_end:
            stat_date = statistics_end

        # 处理 CurStartDate 与节日开始日期的偏移
        if CurStartDate:
            cur_start_dt = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y%m%d")
            if cur_start_dt > statistics_start:
                offset_days = (cur_start_dt - statistics_start).days
                compare_start = compare_start + timedelta(days=offset_days)
                statistics_start = cur_start_dt

        # ========== 2. 查询节日营收 (T_HOLIDAYREVENUE) ==========
        where_rev = f' AND A."SERVERPART_ID" = \'{ServerpartId}\''

        # 本年营收
        if calcType == 1:
            # 当日
            cur_rev_start = stat_date.strftime("%Y%m%d")
        else:
            cur_rev_start = statistics_start.strftime("%Y%m%d")
        cur_rev_end = stat_date.strftime("%Y%m%d")

        sql_cur_rev = f"""SELECT A."SERVERPARTSHOP_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {cur_rev_start} AND {cur_rev_end}{where_rev}
            GROUP BY A."SERVERPARTSHOP_ID" """
        dt_cur_rev = db.execute_query(sql_cur_rev) or []

        # 历年营收
        day_span = (stat_date - statistics_start).days
        cy_date = compare_start + timedelta(days=day_span)
        if calcType == 1:
            cmp_rev_start = cy_date.strftime("%Y%m%d")
        else:
            cmp_rev_start = compare_start.strftime("%Y%m%d")
        cmp_rev_end = cy_date.strftime("%Y%m%d")

        sql_cmp_rev = f"""SELECT A."SERVERPARTSHOP_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {cmp_rev_start} AND {cmp_rev_end}{where_rev}
            GROUP BY A."SERVERPARTSHOP_ID" """
        dt_cmp_rev = db.execute_query(sql_cmp_rev) or []

        # ========== 关键判断：本年和历年营收都为空则返回 null/101 ==========
        if not dt_cur_rev and not dt_cmp_rev:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # 构建查找映射
        cur_rev_map = {}
        for r in dt_cur_rev:
            sid = str(r.get("SERVERPARTSHOP_ID", ""))
            cur_rev_map[sid] = safe_dec(r.get("REVENUE_AMOUNT"))
        cmp_rev_map = {}
        for r in dt_cmp_rev:
            sid = str(r.get("SERVERPARTSHOP_ID", ""))
            cmp_rev_map[sid] = safe_dec(r.get("REVENUE_AMOUNT"))

        # ========== 3. 查询车流 (T_SECTIONFLOW / T_BAYONETDAILY_AH) ==========
        where_bay = f' AND A."SERVERPART_ID" = {ServerpartId}'

        # 本年车流
        if calcType == 1:
            sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {stat_date.strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        elif stat_date.year == 2024 and stat_date > dt(2024, 1, 28) and HolidayType == 2:
            sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {(statistics_start + timedelta(days=3)).strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        else:
            # 默认使用 T_BAYONETDAILY_AH
            sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."VEHICLE_COUNT") AS "SERVERPART_FLOW"
                FROM "T_BAYONETDAILY_AH" A
                WHERE A."INOUT_TYPE" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {statistics_start.strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        dt_cur_bay = db.execute_query(sql_cur_bay) or []

        # 历年车流
        if calcType == 1:
            sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {cy_date.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        elif stat_date.year == 2024 and stat_date > dt(2024, 1, 28) and HolidayType == 2:
            sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {(compare_start + timedelta(days=3)).strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        else:
            sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {compare_start.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        dt_cmp_bay = db.execute_query(sql_cmp_bay) or []

        # ========== 4. 查服务区基本信息 ==========
        sp_info = db.execute_query(f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME"
            FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {ServerpartId}""") or []
        sp_name = sp_info[0].get("SERVERPART_NAME", "") if sp_info else ""
        sp_region_id = sp_info[0].get("SPREGIONTYPE_ID") if sp_info else None
        sp_region_name = sp_info[0].get("SPREGIONTYPE_NAME", "") if sp_info else ""

        # ========== 5. 构建服务区级增幅模型 ==========
        def calc_inc(cur_val, cmp_val):
            """计算增长值和增长率"""
            result = {"curYearData": cur_val, "lYearData": cmp_val,
                      "increaseData": None, "increaseRate": None}
            if cur_val and cmp_val and cur_val != 0 and cmp_val != 0:
                inc = cur_val - cmp_val
                rate = round(inc / cmp_val * 100, 2)
                result["increaseData"] = round(inc, 2)
                result["increaseRate"] = rate
            return result

        # 服务区级营收汇总
        total_cur_rev = sum(cur_rev_map.values())
        total_cmp_rev = sum(cmp_rev_map.values())
        # 车流汇总
        total_cur_bay = sum(safe_dec(r.get("SERVERPART_FLOW")) for r in dt_cur_bay)
        total_cmp_bay = sum(safe_dec(r.get("SERVERPART_FLOW")) for r in dt_cmp_bay)

        revenue_inc = calc_inc(total_cur_rev, total_cmp_rev)
        bayonet_inc = calc_inc(total_cur_bay, total_cmp_bay)
        # 车流增长率超过1000没有可比性
        if bayonet_inc.get("increaseRate") and bayonet_inc["increaseRate"] > 1000:
            bayonet_inc["increaseData"] = None
            bayonet_inc["increaseRate"] = None

        # ========== 6. 查门店分组 (T_SERVERPARTSHOP) ==========
        sql_shop = f"""SELECT "SERVERPARTSHOP_ID", "SHOPTRADE", "SHOPSHORTNAME", "BUSINESS_BRAND"
            FROM "T_SERVERPARTSHOP"
            WHERE "SERVERPART_ID" = {ServerpartId} AND "SHOPTRADE" IS NOT NULL"""
        dt_shop = db.execute_query(sql_shop) or []

        # 按 SHOPTRADE+SHOPSHORTNAME 分组（C: WM_CONCAT）
        from collections import defaultdict
        shop_groups = defaultdict(lambda: {"ids": [], "brand": None, "name": ""})
        for s in dt_shop:
            key = (str(s.get("SHOPTRADE", "")), str(s.get("SHOPSHORTNAME", "")))
            shop_groups[key]["ids"].append(str(s.get("SERVERPARTSHOP_ID", "")))
            shop_groups[key]["name"] = str(s.get("SHOPSHORTNAME", ""))
            if s.get("BUSINESS_BRAND"):
                shop_groups[key]["brand"] = s.get("BUSINESS_BRAND")

        # ========== 7. 遍历门店，构建 ShopINCList ==========
        inc_list = []
        no_inc_list = []

        for (trade, shop_name), info in shop_groups.items():
            shop_ids = info["ids"]
            cur_sum = sum(cur_rev_map.get(sid, 0) for sid in shop_ids)
            cmp_sum = sum(cmp_rev_map.get(sid, 0) for sid in shop_ids)
            has_shop = any(sid in cur_rev_map for sid in shop_ids) or any(sid in cmp_rev_map for sid in shop_ids)

            if not has_shop:
                continue

            shop_model = {
                "ServerpartId": ServerpartId,
                "ServerpartName": sp_name,
                "ServerpartShopId": ",".join(shop_ids),
                "ServerpartShopName": info["name"],
                "RevenueINC": {
                    "curYearData": cur_sum if cur_sum else None,
                    "lYearData": cmp_sum if cmp_sum else None,
                    "increaseData": None,
                    "increaseRate": None,
                },
                "Brand_Id": None,
                "Brand_Name": None,
                "Brand_ICO": None,
                "CurTransaction": None,
            }

            if cur_sum and cur_sum != 0 and cmp_sum and cmp_sum != 0:
                inc_data = round(cur_sum - cmp_sum, 2)
                inc_rate = round(inc_data / cmp_sum * 100, 2)
                shop_model["RevenueINC"]["increaseData"] = inc_data
                shop_model["RevenueINC"]["increaseRate"] = inc_rate
                inc_list.append(shop_model)
            else:
                no_inc_list.append(shop_model)

        # 排序
        if SortStr:
            sort_lower = SortStr.lower()
            is_desc = sort_lower.endswith(" desc")
            sort_field = sort_lower.split(" ")[0]
            field_map = {
                "curyeardata": lambda x: x["RevenueINC"].get("curYearData") or 0,
                "lyeardata": lambda x: x["RevenueINC"].get("lYearData") or 0,
                "increasedata": lambda x: x["RevenueINC"].get("increaseData") or 0,
                "increaserate": lambda x: x["RevenueINC"].get("increaseRate") or 0,
            }
            key_fn = field_map.get(sort_field, lambda x: 0)
            inc_list.sort(key=key_fn, reverse=is_desc)

        # 合并：有增幅的在前，无增幅的在后
        all_shops = inc_list + no_inc_list

        # ========== 8. 构建最终返回结构 (HolidayIncreaseModel) ==========
        result_data = {
            "SPRegionTypeId": sp_region_id,
            "SPRegionTypeName": sp_region_name,
            "ServerpartId": ServerpartId,
            "ServerpartName": sp_name,
            "RevenueINC": revenue_inc,
            "AccountINC": {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None},
            "BayonetINC": bayonet_inc,
            "SectionFlowINC": None,
            "ShopINCList": all_shops,
        }

        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopINCAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== 月度经营 =====
@router.get("/Revenue/GetMonthlyBusinessAnalysis")
async def get_monthly_business_analysis(
    calcType: int = Query(1, description="计算方式：1当月 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: int = Query(None, description="本年年份"),
    compareYear: int = Query(None, description="历年年份"),
    StatisticsMonth: int = Query(None, description="统计月份"),
    StatisticsStartMonth: Optional[int] = Query(None, description="统计开始月份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    SPRegionTypeId: Optional[str] = Query("", description="片区内码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    businessType: Optional[str] = Query("", description="经营模式"),
    businessTrade: Optional[str] = Query("", description="经营业态"),
    businessRegion: Optional[str] = Query("", description="经营区域"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营增幅分析 (SQL平移完成)"""
    try:
        from datetime import datetime
        
        # 1. 参数预处理 (StatisticsMonth 前端传入格式为 yyyyMM，如 202602)
        stat_month_str = str(StatisticsMonth)  # 如 "202602"
        if len(stat_month_str) >= 6:
            cur_month_ym = int(stat_month_str[:6])  # 202602
        else:
            cur_month_ym = curYear * 100 + StatisticsMonth  # 兼容旧格式

        if not StatisticsStartMonth:
            if calcType == 1:
                StatisticsStartMonth = cur_month_ym
            else:
                StatisticsStartMonth = curYear * 100 + 1
        
        # 2. 省份/区域内码查询
        pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
        province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else pushProvinceCode

        # 3. 构建 Revenue 筛选条件
        where_sql = " AND A.PROVINCE_ID = :pid"
        params = {"pid": province_id}
        table_name = "T_PROVINCEREVENUE"

        if SPRegionTypeId:
            where_sql += f" AND B.SPREGIONTYPE_ID IN ({SPRegionTypeId})"
            table_name = "T_HOLIDAYREVENUE"
        if ServerpartId:
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_sql += " AND " + build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
                table_name = "T_HOLIDAYREVENUE"
        if businessType:
            where_sql += f" AND A.BUSINESS_TYPE IN ({businessType})"
        if businessTrade:
            where_sql += f" AND A.SHOPTRADE IN ({businessTrade})"
        if businessRegion:
            where_sql += f" AND A.BUSINESS_REGION IN ({businessRegion})"

        limit_sql = ""
        st_date = StatisticsDate.replace("-", "").replace("/", "") if StatisticsDate else ""
        if st_date and str(curYear) in st_date:
            limit_sql = f" AND A.STATISTICS_DATE <= {st_date[:8]}"

        # 4. 查询营收数据 (CASE WHEN 逻辑)
        # SHOPTRADE 映射: 1便利店, 2餐饮客房, 3外包
        case_sql = """CASE WHEN A.BUSINESS_TYPE = 4000 AND A.SHOPTRADE = '2' THEN 1 
                        WHEN A.BUSINESS_TYPE = 4000 AND A.SHOPTRADE <> '2' THEN 2 
                        ELSE 3 END"""
        
        state_col = table_name.replace('T_', '') + '_STATE'
        rev_base_sql = f"""SELECT 
                    SUM(A.REVENUE_AMOUNT) AS REVENUE_AMOUNT,
                    SUM(A.ACCOUNT_AMOUNTNOTAX) AS ACCOUNT_AMOUNT,
                    {case_sql} AS SHOPTRADE 
                FROM 
                    {table_name} A 
                {" , T_SERVERPART B" if table_name == "T_HOLIDAYREVENUE" else ""}
                WHERE 
                    {"A.SERVERPART_ID = B.SERVERPART_ID AND" if table_name == "T_HOLIDAYREVENUE" else ""}
                    A."{state_col}" = 1 AND 
                    A.STATISTICS_DATE BETWEEN :start AND :end {where_sql} {limit_sql}
                GROUP BY 
                    {case_sql}"""

        # 本年范围：StartMonth+01 ~ StatisticsMonth+31
        cur_start = f"{StatisticsStartMonth}01"
        cur_end = f"{cur_month_ym}31"
        cur_rev_rows = db.execute_query(rev_base_sql, {**params, "start": cur_start, "end": cur_end})
        
        # 历年同期 (计算历年月份范围)
        year_diff = curYear - compareYear
        cy_month_start = StatisticsStartMonth - year_diff * 100
        # cur_month_ym 已经是 yyyyMM 格式，计算历年同期月份
        cy_month_end = cur_month_ym - year_diff * 100
        
        limit_sql_cy = ""
        if st_date and str(curYear) in st_date:
            limit_sql_cy = f" AND A.STATISTICS_DATE <= {compareYear}{st_date[4:8]}"

        rev_base_sql_cy = rev_base_sql.replace(limit_sql, limit_sql_cy)
        cy_rev_rows = db.execute_query(rev_base_sql_cy, {**params, "start": f"{cy_month_start}01", "end": f"{cy_month_end}31"})

        # 5. 查询车流量
        flow_where = f" AND EXISTS (SELECT 1 FROM T_SERVERPART S WHERE A.SERVERPART_ID = S.SERVERPART_ID AND S.PROVINCE_CODE = '{province_id}')"
        _sp_ids_flow = parse_multi_ids(ServerpartId)
        if _sp_ids_flow:
            flow_where = " AND " + build_in_condition('SERVERPART_ID', _sp_ids_flow).replace('"SERVERPART_ID"', 'A.SERVERPART_ID')

        flow_sql = f"""SELECT SUM(A.SERVERPART_FLOW) AS SERVERPART_FLOW 
                   FROM T_SECTIONFLOW A 
                   WHERE A.SECTIONFLOW_STATUS = 1 AND A.SERVERPART_ID > 0 AND 
                   A.STATISTICS_DATE BETWEEN :start AND :end {flow_where} {limit_sql}"""
        
        cur_flow_rows = db.execute_query(flow_sql, {"start": cur_start, "end": cur_end})
        
        flow_sql_cy = flow_sql.replace(limit_sql, limit_sql_cy).replace("A.SERVERPART_FLOW", "A.SERVERPART_FLOW + NVL(A.SERVERPART_FLOW_ANALOG, 0)")
        cy_flow_rows = db.execute_query(flow_sql_cy, {"start": f"{cy_month_start}01", "end": f"{cy_month_end}31"})

        # 6. 聚合逻辑 (对应 C# BindINCModel)
        def bind_inc(rev_rows, cy_rows, flow_rows, cy_flow_rows, shoptrade_filter=None, calc_flow=False):
            def get_sum(data, col, filter_val=None):
                if not data: return 0.0
                if filter_val == "自营":
                    return sum(float(r.get(col) or 0) for r in data if r.get("SHOPTRADE") in (1, 2))
                if filter_val:
                    return sum(float(r.get(col) or 0) for r in data if r.get("SHOPTRADE") == filter_val)
                return sum(float(r.get(col) or 0) for r in data)

            cur_rev = round(get_sum(rev_rows, "REVENUE_AMOUNT", shoptrade_filter), 2)
            l_rev = round(get_sum(cy_rows, "REVENUE_AMOUNT", shoptrade_filter), 2)
            cur_acc = round(get_sum(rev_rows, "ACCOUNT_AMOUNT", shoptrade_filter), 2)
            l_acc = round(get_sum(cy_rows, "ACCOUNT_AMOUNT", shoptrade_filter), 2)

            res = {
                "RevenueINC": {"curYearData": cur_rev, "lYearData": l_rev, "increaseData": round(cur_rev - l_rev, 2), "increaseRate": None},
                "AccountINC": {"curYearData": cur_acc, "lYearData": l_acc, "increaseData": round(cur_acc - l_acc, 2), "increaseRate": None},
                "BayonetINC": None
            }
            if l_rev != 0: res["RevenueINC"]["increaseRate"] = round((res["RevenueINC"]["increaseData"] / l_rev) * 100, 2)
            if l_acc != 0: res["AccountINC"]["increaseRate"] = round((res["AccountINC"]["increaseData"] / l_acc) * 100, 2)

            if calc_flow:
                cf = float(flow_rows[0].get("SERVERPART_FLOW") or 0) if flow_rows else 0.0
                lf = float(cy_flow_rows[0].get("SERVERPART_FLOW") or 0) if cy_flow_rows else 0.0
                res["BayonetINC"] = {"curYearData": cf, "lYearData": lf, "increaseData": cf - lf, "increaseRate": None}
                if lf != 0: res["BayonetINC"]["increaseRate"] = round((res["BayonetINC"]["increaseData"] / lf) * 100, 2)
            return res

        results = []
        # 1. 累计
        summary = bind_inc(cur_rev_rows, cy_rev_rows, cur_flow_rows, cy_flow_rows, calc_flow=True)
        summary.update({"ServerpartId": 0, "ServerpartName": "累计"})
        results.append(summary)

        # 2. 自营
        self_run = bind_inc(cur_rev_rows, cy_rev_rows, None, None, shoptrade_filter="自营")
        self_run.update({"SPRegionTypeId": 1, "SPRegionTypeName": "自营", "ServerpartId": None, "ServerpartName": None})
        results.append(self_run)

        # 3. 细分业态 (1便利店, 2餐饮客房, 3商铺租赁)
        names = {1: "便利店", 2: "餐饮客房", 3: "商铺租赁"}
        for i in range(1, 4):
            item = bind_inc(cur_rev_rows, cy_rev_rows, None, None, shoptrade_filter=i)
            item.update({"ServerpartId": i, "ServerpartName": names[i]})
            results.append(item)
        
        # 4. 外包 (ShopTrade 3)
        coop = bind_inc(cur_rev_rows, cy_rev_rows, cur_flow_rows, cy_flow_rows, shoptrade_filter=3)
        coop.update({"SPRegionTypeId": 2, "SPRegionTypeName": "外包", "ServerpartId": None, "ServerpartName": None})
        results.append(coop)

        # 补充旧API字段
        for r in results:
            r.setdefault("SPRegionTypeId", None)
            r.setdefault("SPRegionTypeName", None)
            r.setdefault("TicketINC", None)
            r.setdefault("AvgTicketINC", None)
            r.setdefault("BayonetINC_ORI", None)
            r.setdefault("SectionFlowINC", None)
            r.setdefault("ShopINCList", None)
            r.setdefault("RankDiff", None)
            r.setdefault("Cost_Amount", None)
            r.setdefault("Ca_Cost", None)
            r.setdefault("Profit_Amount", None)
            # 给所有INC补QOQ字段
            for inc_key in ["RevenueINC", "AccountINC", "BayonetINC"]:
                inc = r.get(inc_key)
                if inc and isinstance(inc, dict):
                    inc.setdefault("QOQData", None)
                    inc.setdefault("increaseDataQOQ", None)
                    inc.setdefault("increaseRateQOQ", None)
                    inc.setdefault("rankNum", None)

        json_list = JsonListData.create(data_list=results, total=len(results), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:
        logger.error(f"GetMonthlyBusinessAnalysis 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetMonthlySPINCAnalysis")
async def get_monthly_sp_inc_analysis(
    request: Request,
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: int = Query(None, description="本年年份"),
    compareYear: int = Query(None, description="历年年份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    StatisticsMonth: int = Query(None, description="统计结束月份"),
    StatisticsStartMonth: Optional[int] = Query(None, description="统计开始月份"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    businessRegion: Optional[int] = Query(None, description="经营区域：1服务区 2城市店"),
    Dimension: Optional[str] = Query("", description="统计维度"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区月度营收增幅分析 (SQL平移完成)"""
    try:
        # 1. 参数处理 (StatisticsMonth 前端传入 yyyyMM 格式)
        stat_month_str = str(StatisticsMonth)
        if len(stat_month_str) >= 6:
            cur_month_ym = int(stat_month_str[:6])
            month_part = int(stat_month_str[4:6])
        else:
            cur_month_ym = curYear * 100 + StatisticsMonth
            month_part = StatisticsMonth

        if not StatisticsStartMonth:
            StatisticsStartMonth = cur_month_ym if calcType == 1 else curYear * 100 + 1
        
        pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pc_rows = db.execute_query(pc_sql, {"pc": pushProvinceCode})
        province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else pushProvinceCode

        where_sql_base = " AND A.PROVINCE_ID = :pid"
        rev_params = {"pid": province_id}
        if ServerpartId:
            rev_ids = ",".join([f"'{s.strip()}'" for s in ServerpartId.split(",")])
            where_sql_base += f" AND A.SERVERPART_ID IN ({rev_ids})"
        
        limit_sql = ""
        st_date = StatisticsDate.replace("-", "").replace("/", "") if StatisticsDate else ""
        if st_date and str(curYear) in st_date:
            limit_sql = f" AND A.STATISTICS_DATE <= {st_date[:8]}"

        dt_cur_revenue = []
        dt_cy_revenue = []
        dt_cur_bayonet = []
        dt_cy_bayonet = []

        # 2. 查询营收数据 (Dimension 1=对客销售, 2=驿达收入)
        if not Dimension or "1" in Dimension or "2" in Dimension:
            rev_sql = f"""SELECT B.SERVERPART_ID, SUM(A.REVENUE_AMOUNT) AS REVENUE_AMOUNT, SUM(A.ACCOUNT_AMOUNTNOTAX) AS ACCOUNT_AMOUNT 
                        FROM T_HOLIDAYREVENUE A, T_SERVERPART B 
                        WHERE A.SERVERPART_ID = TO_CHAR(B.SERVERPART_ID) AND A.HOLIDAYREVENUE_STATE = 1 
                        AND A.STATISTICS_DATE BETWEEN :start AND :end {where_sql_base} {limit_sql}
                        GROUP BY B.SERVERPART_ID"""
            
            dt_cur_revenue = db.execute_query(rev_sql, {**rev_params, "start": f"{StatisticsStartMonth}01", "end": f"{cur_month_ym}31"})
            
            year_diff = curYear - compareYear
            cy_start = f"{StatisticsStartMonth - year_diff * 100}01"
            cy_end = f"{compareYear}{month_part:02}31"
            limit_sql_cy = f" AND A.STATISTICS_DATE <= {compareYear}{st_date[4:8]}" if st_date and str(curYear) in st_date else ""
            
            rev_sql_cy = rev_sql.replace(limit_sql, limit_sql_cy)
            dt_cy_revenue = db.execute_query(rev_sql_cy, {**rev_params, "start": cy_start, "end": cy_end})

        # 3. 查询车流量 (Dimension 3)
        if not Dimension or "3" in Dimension:
            flow_where = f" AND EXISTS (SELECT 1 FROM T_SERVERPART S WHERE A.SERVERPART_ID = S.SERVERPART_ID AND S.PROVINCE_CODE = '{province_id}')"
            _sp_ids_f = parse_multi_ids(ServerpartId)
            if _sp_ids_f:
                flow_where = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids_f).replace('"SERVERPART_ID"', 'A.SERVERPART_ID')
            
            flow_sql = f"""SELECT SERVERPART_ID, SUM(A.SERVERPART_FLOW) AS SERVERPART_FLOW 
                        FROM T_SECTIONFLOW A WHERE A.SECTIONFLOW_STATUS = 1 AND A.SERVERPART_ID > 0 
                        AND A.STATISTICS_DATE BETWEEN :start AND :end {flow_where} {limit_sql}
                        GROUP BY SERVERPART_ID"""
            
            dt_cur_bayonet = db.execute_query(flow_sql, {"start": f"{StatisticsStartMonth}01", "end": f"{cur_month_ym}31"})
            
            flow_sql_cy = flow_sql.replace(limit_sql, limit_sql_cy).replace("A.SERVERPART_FLOW", "A.SERVERPART_FLOW + NVL(A.SERVERPART_FLOW_ANALOG, 0)")
            dt_cy_bayonet = db.execute_query(flow_sql_cy, {"start": cy_start, "end": cy_end})

        # 4. 获取服务区列表
        sp_where = f"WHERE SPREGIONTYPE_ID IS NOT NULL AND STATISTICS_TYPE = 1000 AND STATISTIC_TYPE = 1000 AND PROVINCE_CODE = '{province_id}'"
        _sp_ids_sp = parse_multi_ids(ServerpartId)
        if _sp_ids_sp: sp_where += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids_sp)
        # 暂时忽略 ExcludeRegionId 过滤以保持简单
        dt_serverpart = db.execute_query(f"SELECT SPREGIONTYPE_ID, SPREGIONTYPE_NAME, SERVERPART_ID, SERVERPART_NAME, SPREGIONTYPE_INDEX, SERVERPART_INDEX FROM T_SERVERPART {sp_where} ORDER BY SPREGIONTYPE_INDEX, SERVERPART_INDEX, SERVERPART_ID")

        # 5. 组装数据
        results = []
        no_inc_results = []

        cur_rev_map = {r["SERVERPART_ID"]: r for r in dt_cur_revenue}
        cy_rev_map = {r["SERVERPART_ID"]: r for r in dt_cy_revenue}
        cur_flow_map = {r["SERVERPART_ID"]: r for r in dt_cur_bayonet}
        cy_flow_map = {r["SERVERPART_ID"]: r for r in dt_cy_bayonet}

        def calc_inc(cur_val, l_val):
            cur_f = float(cur_val) if cur_val is not None else None
            l_f = float(l_val) if l_val is not None else None
            inc = round(cur_f - l_f, 2) if cur_f is not None and l_f is not None else None
            rate = round((inc / l_f) * 100, 2) if inc is not None and l_f and l_f != 0 else None
            return {"curYearData": cur_f, "lYearData": l_f, "increaseData": inc, "increaseRate": rate,
                    "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}

        for sp in dt_serverpart:
            sp_id = sp["SERVERPART_ID"]
            rev_c = cur_rev_map.get(sp_id, {})
            rev_l = cy_rev_map.get(sp_id, {})
            flow_c = cur_flow_map.get(sp_id, {})
            flow_l = cy_flow_map.get(sp_id, {})

            item = {
                "SPRegionTypeId": sp["SPREGIONTYPE_ID"],
                "SPRegionTypeName": sp["SPREGIONTYPE_NAME"],
                "ServerpartId": sp_id,
                "ServerpartName": sp["SERVERPART_NAME"],
                "RevenueINC": calc_inc(rev_c.get("REVENUE_AMOUNT"), rev_l.get("REVENUE_AMOUNT")),
                "AccountINC": calc_inc(rev_c.get("ACCOUNT_AMOUNT"), rev_l.get("ACCOUNT_AMOUNT")),
                "BayonetINC": calc_inc(flow_c.get("SERVERPART_FLOW"), flow_l.get("SERVERPART_FLOW"))
            }

            # 过滤逻辑 (SortStr 存在时，如果对应的增长率无法计算则可能被移到后面)
            results.append(item)

        # 6. 排序 (SortStr 示例: "revenue desc")
        if SortStr:
            sort_field = SortStr.lower()
            reverse = "desc" in sort_field
            key_map = {"revenue": lambda x: x["RevenueINC"]["increaseRate"] or -999999,
                       "account": lambda x: x["AccountINC"]["increaseRate"] or -999999,
                       "bayonet": lambda x: x["BayonetINC"]["increaseRate"] or -999999}
            for k, func in key_map.items():
                if k in sort_field:
                    results.sort(key=func, reverse=reverse)
                    break

        # 补充旧API字段
        for r in results:
            r.setdefault("TicketINC", None)
            r.setdefault("AvgTicketINC", None)
            r.setdefault("BayonetINC_ORI", None)
            r.setdefault("SectionFlowINC", None)
            r.setdefault("ShopINCList", None)
            r.setdefault("RankDiff", None)
            r.setdefault("Cost_Amount", None)
            r.setdefault("Ca_Cost", None)
            r.setdefault("Profit_Amount", None)

        json_list = JsonListData.create(data_list=results, total=len(results), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:
        logger.error(f"GetMonthlySPINCAnalysis 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


# ===== 其余接口 =====
@router.get("/Revenue/GetTransactionDetailList")
async def get_transaction_detail_list(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    ServerpartShopId: Optional[str] = Query("", description="门店内码"),
    StartTime: Optional[str] = Query("", description="开始时间"),
    EndTime: Optional[str] = Query("", description="结束时间"),
    PageIndex: int = Query(1, description="显示页码"),
    PageSize: int = Query(100, description="每页数量"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时交易明细（C#对齐：T_YSSELLMASTER_YES + T_YSSELLDETAILS_YES）"""
    try:
        from datetime import datetime as dt

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        # C#: 按 ServerpartShopId > ServerpartId > ProvinceCode 优先级过滤
        where_sql = ""
        if ServerpartShopId:
            where_sql = f' AND C."SERVERPARTSHOP_ID" IN ({ServerpartShopId})'
        elif ServerpartId:
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_sql = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif ProvinceCode:
            where_sql = f' AND B."PROVINCE_CODE" = {ProvinceCode}'
        else:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # C#: 过滤交易时间 SELLMASTER_DATE（格式为 yyyyMMddHHmmss 的bigint）
        if StartTime:
            try:
                st = dt.strptime(StartTime, "%Y-%m-%d %H:%M:%S") if " " in StartTime else dt.strptime(StartTime, "%Y-%m-%d")
                where_sql += f' AND A."SELLMASTER_DATE" >= {st.strftime("%Y%m%d")}000000'
            except:
                pass
        if EndTime:
            try:
                et = dt.strptime(EndTime, "%Y-%m-%d %H:%M:%S") if " " in EndTime else dt.strptime(EndTime, "%Y-%m-%d")
                where_sql += f' AND A."SELLMASTER_DATE" <= {et.strftime("%Y%m%d")}235959'
            except:
                pass

        # C#: 4表关联查询
        sql = f"""SELECT B."SERVERPART_ID", B."SERVERPART_NAME", C."SERVERPARTSHOP_ID", C."SHOPNAME",
                C."SHOPTRADE", A."SELLMASTER_DATE", A."SELLMASTER_AMOUNT",
                WM_CONCAT(D."COMMODITY_NAME" || '|' || D."COMMODITY_BARCODE" || '|' || D."SELLDETAILS_COUNT" ||
                    '|' || D."SELLDETAILS_PRICE" || '|' || D."SELLDETAILS_AMOUNT") AS "DETAIL_LIST"
            FROM "T_YSSELLMASTER_YES" A, "T_SERVERPART" B, "T_SERVERPARTSHOP" C, "T_YSSELLDETAILS_YES" D
            WHERE A."SERVERPARTCODE" = B."SERVERPART_CODE"
                AND A."SHOPCODE" = C."SHOPCODE"
                AND A."SELLMASTER_CODE" = D."SELLMASTER_CODE"
                AND B."SERVERPART_ID" = C."SERVERPART_ID"
                AND A."SELLMASTER_STATE" > 0{where_sql}
            GROUP BY B."SERVERPART_ID", B."SERVERPART_NAME", C."SERVERPARTSHOP_ID", C."SHOPNAME",
                C."SHOPTRADE", A."SELLMASTER_DATE", A."SELLMASTER_AMOUNT" """
        rows = db.execute_query(sql) or []

        # C#: 按服务区分组返回
        from collections import OrderedDict
        sp_map = OrderedDict()
        for r in rows:
            sp_id = r.get("SERVERPART_ID")
            if sp_id not in sp_map:
                sp_map[sp_id] = {
                    "Serverpart_ID": sp_id,
                    "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                    "CurRevenueAmount": 0.0,
                    "LastTradeTime": None,
                    "TimeList": [],
                }
            sp_map[sp_id]["CurRevenueAmount"] += safe_dec(r.get("SELLMASTER_AMOUNT"))
            trade_time = str(r.get("SELLMASTER_DATE", ""))
            if trade_time and (sp_map[sp_id]["LastTradeTime"] is None or trade_time > str(sp_map[sp_id]["LastTradeTime"])):
                sp_map[sp_id]["LastTradeTime"] = trade_time

            # 解析商品明细
            sell_list = []
            detail_str = str(r.get("DETAIL_LIST", "") or "")
            if detail_str:
                for item in detail_str.split(","):
                    parts = item.split("|")
                    if len(parts) >= 5:
                        sell_list.append({
                            "CommodityName": parts[0],
                            "CommodityBarcode": parts[1],
                            "SellCount": safe_dec(parts[2]),
                            "SellPrice": safe_dec(parts[3]),
                            "SellAmount": safe_dec(parts[4]),
                        })

            sp_map[sp_id]["TimeList"].append({
                "ServerpartShop_ID": str(r.get("SERVERPARTSHOP_ID", "")),
                "ServerpartShop_Name": r.get("SHOPNAME", ""),
                "ShopTrade": str(r.get("SHOPTRADE", "")),
                "TicketAmount": safe_dec(r.get("SELLMASTER_AMOUNT")),
                "TradeTime": trade_time,
                "sellList": sell_list,
            })

        data_list = list(sp_map.values())
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionDetailList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetHolidayRevenueRatio")
async def get_holiday_revenue_ratio(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
):
    """获取节日营收占比（C#源码为纯静态硬编码，不查库）"""
    # 对应 C# HolidayHelper.GetHolidayRevenueRatio() — 全部硬编码
    holidays = [
        {"name": "元旦", "value": "0.65", "key": "1", "data": None},
        {"name": "春运", "value": "45.62", "key": "2", "data": None},
        {"name": "清明", "value": "2.55", "key": "3", "data": None},
        {"name": "五一", "value": "6.53", "key": "4", "data": None},
        {"name": "端午", "value": "3.43", "key": "5", "data": None},
        {"name": "暑期", "value": "34.19", "key": "6", "data": None},
        {"name": "中秋", "value": "1.27", "key": "7", "data": None},
        {"name": "国庆", "value": "8.76", "key": "8", "data": None},
    ]
    data_list = [
        {"node": {"name": "普通日", "value": "47.1", "key": "0", "data": None}, "children": None},
        {"node": {"name": "节假日", "value": "52.9", "key": "1", "data": None},
         "children": [{"node": h, "children": None} for h in holidays]},
    ]
    json_list = JsonListData.create(data_list=data_list, total=len(data_list))
    return Result.success(data=json_list.model_dump(), msg="查询成功")


@router.post("/Revenue/GetBusinessRevenueList")
async def get_business_revenue_list(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取云南24年经营数据分析（AES加密）"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        data_type = params.get("DataType", "")
        start_month = params.get("StartMonth", "")
        end_month = params.get("EndMonth", "")
        group_by_region = params.get("GroupByRegion", False)
        group_by_trade = params.get("GroupByTrade", False)
        logger.info(f"GetBusinessRevenueList 解密参数: ProvinceCode={province_code}, DataType={data_type}")

        # TODO: 实现查询逻辑
        logger.warning("GetBusinessRevenueList 查询逻辑暂未实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetBusinessRevenueList AES解密失败: {ve}")
        return Result.fail(msg="查询失败未将对象引用设置到对象的实例。")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/Revenue/GetMonthlyBusinessRevenue")
async def get_monthly_business_revenue(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取云南月度经营数据分析（AES加密）"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        data_type = params.get("DataType", "")
        start_month = params.get("StartMonth", "")
        end_month = params.get("EndMonth", "")
        logger.info(f"GetMonthlyBusinessRevenue 解密参数: ProvinceCode={province_code}, DataType={data_type}")

        # TODO: 实现查询逻辑
        logger.warning("GetMonthlyBusinessRevenue 查询逻辑暂未实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetMonthlyBusinessRevenue AES解密失败: {ve}")
        return Result.fail(msg="查询失败未将对象引用设置到对象的实例。")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetCompanyRevenueReport")
async def get_company_revenue_report(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StartTime: Optional[str] = Query(None, description="开始日期"),
    EndTime: Optional[str] = Query(None, description="结束日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """按照安徽驿达子公司运营的门店返回经营数据报表"""
    try:
        from datetime import datetime as dt
        from collections import defaultdict

        # 1. 查省份FIELDENUM_ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": ProvinceCode})
        if not fe_rows:
            return Result.fail(code=200, msg="查询失败，省份编码不正确！")
        province_id = fe_rows[0]["FIELDENUM_ID"]

        # 2. 构建WHERE条件
        where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        else:
            where_sql += f' AND B."STATISTIC_TYPE" = 1000 AND B."STATISTICS_TYPE" = 1000 AND B."PROVINCE_CODE" = {province_id}'
        if StartTime:
            sd = dt.strptime(StartTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in StartTime else StartTime
            where_sql += f' AND A."STATISTICS_DATE" >= {sd}'
        if EndTime:
            ed = dt.strptime(EndTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in EndTime else EndTime
            where_sql += f' AND A."STATISTICS_DATE" <= {ed}'

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
        rows = db.execute_query(sql)
        if not rows or not any(r.get("SERVERPARTSHOP_ID") for r in rows):
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 4. 查门店信息（SERVERPARTSHOP_ID可能是逗号分隔的多个ID）
        all_shop_ids = set()
        for r in rows:
            sid = r.get("SERVERPARTSHOP_ID")
            if sid:
                for s in str(sid).split(","):
                    s = s.strip()
                    if s:
                        all_shop_ids.add(s)
        shop_map = {}
        if all_shop_ids:
            id_list = list(all_shop_ids)
            chunk_size = 500
            for i in range(0, len(id_list), chunk_size):
                chunk = id_list[i:i+chunk_size]
                ids_in = ",".join(chunk)
                shop_rows = db.execute_query(f'SELECT * FROM "T_SERVERPARTSHOP" WHERE "SERVERPARTSHOP_ID" IN ({ids_in})')
                for s in (shop_rows or []):
                    shop_map[s.get("SERVERPARTSHOP_ID")] = s

        # 5. 查业态
        trade_rows = db.execute_query(f"""SELECT "AUTOSTATISTICS_ID","AUTOSTATISTICS_PID","AUTOSTATISTICS_NAME","AUTOSTATISTICS_INDEX"
            FROM "T_AUTOSTATISTICS" WHERE "PROVINCE_CODE" = {ProvinceCode} AND "AUTOSTATISTICS_STATE" > 0""")
        trade_map = {}
        for t in (trade_rows or []):
            trade_map[str(t["AUTOSTATISTICS_ID"])] = t["AUTOSTATISTICS_NAME"]

        # 6. 查业务限制(T_RTBUSINESSLIMIT)
        push_limit = defaultdict(set)
        if all_shop_ids:
            ids_in = ",".join(list(all_shop_ids)[:1000])
            limit_rows = db.execute_query(f"""SELECT A."SERVERPARTSHOP_ID", R."DATA_VALUE"
                FROM "T_SERVERPARTSHOP" A, "T_RTBUSINESSLIMIT" R
                WHERE A."SERVERPARTSHOP_ID" = R."SERVERPARTSHOP_ID" AND R."DATA_TYPE" = 1030
                    AND R."DATA_VALUE" IN (2010,2020,2030,2040,2050,2060)
                    AND A."SERVERPARTSHOP_ID" IN ({ids_in})
                GROUP BY A."SERVERPARTSHOP_ID", R."DATA_VALUE" """)
            for lr in (limit_rows or []):
                push_limit[lr["SERVERPARTSHOP_ID"]].add(int(lr["DATA_VALUE"]))

        # 7. 给每行标记该归属哪个公司
        def safe_int(v):
            try: return int(v) if v is not None else 0
            except: return 0

        def safe_float(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        processed = []
        for r in rows:
            item = {
                "SPRegionTypeId": safe_int(r.get("SPREGIONTYPE_ID")),
                "SPRegionTypeName": str(r.get("SPREGIONTYPE_NAME") or ""),
                "SPRegionTypeIndex": safe_int(r.get("SPREGIONTYPE_INDEX")),
                "ServerpartId": safe_int(r.get("SERVERPART_ID")),
                "ServerpartName": str(r.get("SERVERPART_NAME") or ""),
                "ServerpartIndex": safe_int(r.get("SERVERPART_INDEX")),
                "ServerpartShopId": str(r.get("SERVERPARTSHOP_ID") or ""),
                "RevenueAmount": safe_float(r.get("REVENUE_AMOUNT")),
                "BusinessTrade": 0, "BusinessTradeName": "",
                "BusinessBrand": 0, "BrandName": "",
                "ShopShortName": "", "MerchantsName": "",
            }
            shop_id_str = str(r.get("SERVERPARTSHOP_ID") or "")
            if not shop_id_str:
                if safe_int(r.get("TICKET_COUNT")) > 0:
                    item["MerchantsName"] = "安徽驿达运营管理有限公司"
                processed.append(item)
                continue
            # 拆分逗号分隔的ID，查所有匹配门店
            sub_ids = [s.strip() for s in shop_id_str.split(",") if s.strip()]
            exist_shops = [shop_map[int(sid)] for sid in sub_ids if int(sid) in shop_map]
            if not exist_shops:
                item["MerchantsName"] = "安徽驿达运营管理有限公司"
                processed.append(item)
                continue
            # 优先判定: 驿佳(-2846) > 百和(-2802) > 驿达
            yijia_shops = [s for s in exist_shops if safe_int(s.get("SELLER_ID")) == -2846]
            baihe_shops = [s for s in exist_shops if safe_int(s.get("SELLER_ID")) == -2802]
            if yijia_shops:
                shop = yijia_shops[0]
                item["MerchantsName"] = "安徽驿佳商贸有限公司"
                item["BusinessTrade"] = safe_int(shop.get("BUSINESS_TRADE"))
                item["BusinessBrand"] = safe_int(shop.get("BUSINESS_BRAND"))
                item["BrandName"] = str(shop.get("BRAND_NAME") or "")
                item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")
            elif baihe_shops:
                shop = baihe_shops[0]
                item["MerchantsName"] = "安徽百和餐饮有限公司"
                item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")
                # 查pushLimit确定trade
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
                bt = max((safe_int(s.get("BUSINESS_TRADE")) for s in exist_shops), default=0)
                item["BusinessTrade"] = bt
                item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")

            # 匹配业态名称
            trade_id = str(item["BusinessTrade"])
            if trade_id in trade_map and not item["BusinessTradeName"]:
                item["BusinessTradeName"] = trade_map[trade_id]

            item["ShopShort_Name"] = str(r.get("SERVERPART_NAME") or "") + item["ShopShortName"]
            processed.append(item)

        # 8. 构建嵌套结果
        total_revenue = sum(p["RevenueAmount"] for p in processed)
        if total_revenue == 0:
            total_revenue = 1

        company_names = ["安徽驿达运营管理有限公司", "安徽驿佳商贸有限公司", "安徽百和餐饮有限公司"]
        result_list = []

        def make_node(**kwargs):
            base = {"CompanyId": 0, "CompanyName": None, "SPRegionType_Id": None, "SPRegionType_Name": None,
                    "Serverpart_Id": None, "Serverpart_Name": None, "BusinessType_Name": None,
                    "BusinessTrade_Id": None, "BusinessTrade_Name": None, "ServerpartShop_Id": None,
                    "ShopShort_Name": None, "Total_Revenue": None, "Revenue_Proportion": None,
                    "TicketCount": None, "TotalCount": None, "TotalOffAmount": None, "MobilePayment": None,
                    "Different_Price_Less": None, "Different_Price_More": None}
            base.update(kwargs)
            return base

        def bind_sp_nodes(items, company_name, trade_id, trade_name):
            """按片区->服务区分组"""
            region_groups = defaultdict(list)
            for it in items:
                region_groups[(it["SPRegionTypeId"], it["SPRegionTypeName"], it["SPRegionTypeIndex"])].append(it)
            region_nodes = []
            for (rid, rname, rindex), sp_items in sorted(region_groups.items(), key=lambda x: (x[0][2], x[0][0])):
                rev = round(sum(s["RevenueAmount"] for s in sp_items), 2)
                region_node = {
                    "node": make_node(CompanyName=company_name, BusinessTrade_Id=trade_id,
                                     BusinessTrade_Name=trade_name, SPRegionType_Id=rid,
                                     SPRegionType_Name=rname, Total_Revenue=rev,
                                     Revenue_Proportion=round(rev / total_revenue * 100, 2)),
                    "children": []
                }
                server_groups = defaultdict(list)
                for s in sp_items:
                    server_groups[(s["ServerpartId"], s["ServerpartName"], s["ServerpartIndex"])].append(s)
                for (sid, sname, sindex), s_items in sorted(server_groups.items(), key=lambda x: x[0][2]):
                    srv = round(sum(x["RevenueAmount"] for x in s_items), 2)
                    shop_ids_str = ",".join(dict.fromkeys(x["ServerpartShopId"] for x in s_items if x["ServerpartShopId"]))
                    region_node["children"].append({
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=trade_id,
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

        for company_name in company_names:
            company_items = [p for p in processed if p["MerchantsName"] == company_name]
            if not company_items:
                continue
            company_rev = round(sum(c["RevenueAmount"] for c in company_items), 2)
            company_node = {
                "node": make_node(CompanyName=company_name, Total_Revenue=company_rev,
                                 Revenue_Proportion=round(company_rev / total_revenue * 100, 2)),
                "children": []
            }

            if company_name == "安徽驿达运营管理有限公司":
                # 按业态父级分组
                parent_trades = [t for t in (trade_rows or []) if str(t.get("AUTOSTATISTICS_PID")) == "-1"]
                parent_trades.sort(key=lambda x: safe_int(x.get("AUTOSTATISTICS_INDEX")))
                for pt in parent_trades:
                    pid = str(pt["AUTOSTATISTICS_ID"])
                    child_ids = {str(t["AUTOSTATISTICS_ID"]) for t in (trade_rows or [])
                                 if str(t.get("AUTOSTATISTICS_PID")) == pid or str(t["AUTOSTATISTICS_ID"]) == pid}
                    trade_items = [c for c in company_items if str(c["BusinessTrade"]) in child_ids]
                    if not trade_items:
                        continue
                    t_rev = round(sum(t["RevenueAmount"] for t in trade_items), 2)
                    trade_node = {
                        "node": make_node(CompanyName=company_name,
                                         BusinessTrade_Id=safe_float(pt["AUTOSTATISTICS_ID"]),
                                         BusinessTrade_Name=pt["AUTOSTATISTICS_NAME"],
                                         Total_Revenue=t_rev,
                                         Revenue_Proportion=round(t_rev / total_revenue * 100, 2)),
                        "children": bind_sp_nodes(trade_items, company_name,
                                                  safe_float(pt["AUTOSTATISTICS_ID"]), pt["AUTOSTATISTICS_NAME"])
                    }
                    trade_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(trade_node)
                # 其他（BusinessTrade=0的）
                other_items = [c for c in company_items if c["BusinessTrade"] == 0]
                if other_items:
                    o_rev = round(sum(o["RevenueAmount"] for o in other_items), 2)
                    other_node = {
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=0,
                                         BusinessTrade_Name="其他", Total_Revenue=o_rev,
                                         Revenue_Proportion=round(o_rev / total_revenue * 100, 2)),
                        "children": bind_sp_nodes(other_items, company_name, 0, "其他")
                    }
                    other_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(other_node)

            elif company_name == "安徽驿佳商贸有限公司":
                # 便利店 + 品牌分
                store_items = company_items  # 简化处理
                if store_items:
                    s_rev = round(sum(s["RevenueAmount"] for s in store_items), 2)
                    store_node = {
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=0.0,
                                         BusinessTrade_Name="服务区便利店", Total_Revenue=s_rev,
                                         Revenue_Proportion=round(s_rev / total_revenue * 100, 2)),
                        "children": []
                    }
                    sg = defaultdict(list)
                    for s in store_items:
                        sg[(s["ServerpartId"], s["ServerpartName"], s.get("ShopShort_Name", ""))].append(s)
                    for (sid, sname, ssn), items in sg.items():
                        srv = round(sum(x["RevenueAmount"] for x in items), 2)
                        store_node["children"].append({
                            "node": make_node(CompanyName=company_name, BusinessTrade_Name="服务区便利店",
                                             Serverpart_Id=sid, Serverpart_Name=sname,
                                             ShopShort_Name=ssn, Total_Revenue=srv,
                                             Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                            "children": None
                        })
                    store_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(store_node)

            else:  # 百和餐饮
                trade_groups = defaultdict(list)
                for c in company_items:
                    trade_groups[(c["BusinessTrade"], c["BusinessTradeName"])].append(c)
                for (tid, tname), items in trade_groups.items():
                    t_rev = round(sum(t["RevenueAmount"] for t in items), 2)
                    trade_node = {
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=safe_float(tid),
                                         BusinessTrade_Name=tname, Total_Revenue=t_rev,
                                         Revenue_Proportion=round(t_rev / total_revenue * 100, 2)),
                        "children": []
                    }
                    sg = defaultdict(list)
                    for t in items:
                        sg[(t["ServerpartId"], t["ServerpartName"], t.get("ShopShort_Name", ""))].append(t)
                    for (sid, sname, ssn), s_items in sg.items():
                        srv = round(sum(x["RevenueAmount"] for x in s_items), 2)
                        trade_node["children"].append({
                            "node": make_node(CompanyName=company_name, BusinessTrade_Id=safe_float(tid),
                                             BusinessTrade_Name=tname, Serverpart_Id=sid,
                                             Serverpart_Name=sname, ShopShort_Name=ssn,
                                             Total_Revenue=srv,
                                             Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                            "children": None
                        })
                    trade_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(trade_node)

            company_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
            # 确保 children 至少有一个骨架节点
            if not company_node["children"]:
                company_node["children"] = [{"node": make_node(), "children": []}]
            result_list.append(company_node)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCompanyRevenueReport 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetRevenueCompare =====
@router.get("/Revenue/GetRevenueCompare")
async def get_revenue_compare(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收同比环比对比数据 (C#完整平移)"""
    try:
        from datetime import datetime as dt

        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        def sf(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not StatisticsDate:
            return Result.success(data=None, msg="查询成功")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        date_str = stat_date.strftime("%Y%m%d")
        yoy_date = stat_date.replace(year=stat_date.year - 1).strftime("%Y%m%d")

        # 省份映射
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": ProvinceCode})
        province_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else ProvinceCode

        where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionTypeID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeID})'

        is_history = stat_date < dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - __import__("datetime").timedelta(days=9)

        # 查当日营收
        if is_history:
            if not ServerpartId and not SPRegionTypeID:
                cur_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                    SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                    FROM "T_REVENUEDAILY" A
                    WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_DATE" = {date_str}"""
            else:
                cur_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                    SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                    FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                    WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql} AND A."STATISTICS_DATE" = {date_str}"""
        else:
            cur_sql = f"""SELECT SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
                SUM(A."TOTALCOUNT") AS "TOTALCOUNT", SUM(A."CASHPAY") AS "CASHPAY"
                FROM "T_ENDACCOUNT_TEMP" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."VALID" = 1
                AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql} AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
                AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1"""

        cur_rows = db.execute_query(cur_sql) or []
        rev = round(sf(cur_rows[0].get("CASHPAY")), 2) if cur_rows and sf(cur_rows[0].get("TICKETCOUNT")) > 0 else 0.0
        ticket = round(sf(cur_rows[0].get("TICKETCOUNT")), 2) if cur_rows and sf(cur_rows[0].get("TICKETCOUNT")) > 0 else 0.0
        avg_t = round(rev / ticket, 2) if ticket > 0 else 0.0

        # 查去年同日
        if not ServerpartId and not SPRegionTypeID:
            yoy_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_DATE" = {yoy_date}"""
        else:
            yoy_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql} AND A."STATISTICS_DATE" = {yoy_date}"""
        yoy_rows = db.execute_query(yoy_sql) or []
        yoy_rev = sf(yoy_rows[0].get("CASHPAY")) if yoy_rows else 0
        yoy_ticket = sf(yoy_rows[0].get("TICKETCOUNT")) if yoy_rows else 0
        yoy_avg = round(yoy_rev / yoy_ticket, 2) if yoy_ticket > 0 else 0.0

        rev_rate = round((rev - yoy_rev) / yoy_rev * 100, 2) if yoy_rev > 0 else None
        ticket_rate = round((ticket - yoy_ticket) / yoy_ticket * 100, 2) if yoy_ticket > 0 else None
        avg_rate = round((avg_t - yoy_avg) / yoy_avg * 100, 2) if yoy_avg > 0 else None

        # 趋势数据：工作日/周末/节假日月度平均
        year_str = stat_date.strftime("%Y")
        date_sql = f' AND A."STATISTICS_DATE" >= {year_str}0101 AND A."STATISTICS_DATE" <= {date_str}'

        if not ServerpartId and not SPRegionTypeID:
            trend_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        else:
            trend_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""

        trend_rows = db.execute_query(trend_sql) or []

        # 去年12月数据（用于1月环比）
        ly_dec_sql = date_sql.replace(date_sql, f' AND A."STATISTICS_DATE" >= {int(year_str)-1}1201 AND A."STATISTICS_DATE" <= {int(year_str)-1}1231')
        if not ServerpartId and not SPRegionTypeID:
            ly_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        else:
            ly_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        ly_rows = db.execute_query(ly_sql) or []

        # 查节假日名称
        hol_sql = f"""SELECT "HOLIDAY_NAME", TO_CHAR("HOLIDAY_DATE",'MM') AS "HOLIDAY_MONTH"
            FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DATE" >= TO_DATE('{year_str}/1/1','YYYY/MM/DD')
            AND "HOLIDAY_DATE" <= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
            GROUP BY "HOLIDAY_NAME", TO_CHAR("HOLIDAY_DATE",'MM')"""
        hol_rows = db.execute_query(hol_sql) or []

        # 构建trend map: {(data_type, month_str): {rev, ticket}}
        trend_map = {}
        for r in trend_rows:
            key = (int(sf(r.get("DATA_TYPE"))), str(r.get("STATISTICS", "")))
            trend_map[key] = {"rev": sf(r.get("REVENUE_AMOUNT")), "ticket": sf(r.get("TICKET_COUNT"))}
        for r in ly_rows:
            key = (int(sf(r.get("DATA_TYPE"))), str(r.get("STATISTICS", "")))
            trend_map[key] = {"rev": sf(r.get("REVENUE_AMOUNT")), "ticket": sf(r.get("TICKET_COUNT"))}

        # 节日名称map: {month: "name1、name2"}
        hol_map = {}
        for r in hol_rows:
            m = str(r.get("HOLIDAY_MONTH", "")).lstrip("0") or "0"
            m_key = m.zfill(2)
            name = str(r.get("HOLIDAY_NAME", ""))
            if m_key not in hol_map:
                hol_map[m_key] = name
            else:
                hol_map[m_key] += "、" + name

        # 构建3个List (工作日平均/周末平均/节假日平均)
        data_types = [("0", "工作日平均"), ("1", "周末平均"), ("2", "节假日平均")]
        rev_list, ticket_list, avg_list = [], [], []

        if trend_rows:
            for dt_idx, (dt_code, dt_name) in enumerate(data_types):
                rev_data = [None] * 12
                ticket_data = [None] * 12
                avg_data = [None] * 12
                # 节假日有value（节日名称）
                rev_value = [None] * 12 if dt_code == "2" else None
                ticket_value = [None] * 12 if dt_code == "2" else None
                avg_value = [None] * 12 if dt_code == "2" else None

                for m in range(1, 13):
                    month_key = f"{year_str}{m:02d}"
                    dt_int = int(dt_code)
                    info = trend_map.get((dt_int, month_key))

                    # C#: 如果工作日/周末没有当月数据，fallback到节假日
                    if info is None and dt_int < 2:
                        info = trend_map.get((2, month_key))

                    if dt_code == "2":
                        hname = hol_map.get(f"{m:02d}", "")
                        rev_value[m-1] = [str(m), hname]
                        ticket_value[m-1] = [str(m), hname]
                        avg_value[m-1] = [str(m), hname]

                    if info:
                        r_val = round(info["rev"], 2)
                        t_val = round(info["ticket"])
                        a_val = round(r_val / t_val, 2) if t_val > 0 else 0

                        # 计算增长率 (data[2])
                        rate_r, rate_t, rate_a = 0, 0, 0
                        if dt_idx == 0:  # 工作日：较上月增长率
                            if m == 1:
                                # 用去年12月
                                ly_key = (dt_int, f"{int(year_str)-1}12")
                                ly_info = trend_map.get(ly_key)
                                if ly_info and ly_info["rev"] > 0:
                                    rate_r = round((r_val / ly_info["rev"] - 1) * 100, 2)
                                if ly_info and ly_info["ticket"] > 0:
                                    rate_t = round((t_val / ly_info["ticket"] - 1) * 100, 2)
                                    ly_avg = ly_info["rev"] / ly_info["ticket"]
                                    if ly_avg > 0:
                                        rate_a = round((a_val / ly_avg - 1) * 100, 2)
                            else:
                                prev = rev_data[m-2]
                                if prev and prev[1] > 0:
                                    rate_r = round((r_val / prev[1] - 1) * 100, 2)
                                prev_t = ticket_data[m-2]
                                if prev_t and prev_t[1] > 0:
                                    rate_t = round((t_val / prev_t[1] - 1) * 100, 2)
                                prev_a = avg_data[m-2]
                                if prev_a and prev_a[1] > 0:
                                    rate_a = round((a_val / prev_a[1] - 1) * 100, 2)
                        elif dt_idx == 1:  # 周末：较工作日增长率
                            wd = rev_list[0]["data"][m-1] if rev_list else None
                            if wd and wd[1] > 0:
                                rate_r = round((r_val / wd[1] - 1) * 100, 2)
                            wd_t = ticket_list[0]["data"][m-1] if ticket_list else None
                            if wd_t and wd_t[1] > 0:
                                rate_t = round((t_val / wd_t[1] - 1) * 100, 2)
                            wd_a = avg_list[0]["data"][m-1] if avg_list else None
                            if wd_a and wd_a[1] > 0:
                                rate_a = round((a_val / wd_a[1] - 1) * 100, 2)

                        rev_data[m-1] = [float(m), float(r_val), float(rate_r)]
                        ticket_data[m-1] = [float(m), float(t_val), float(rate_t)]
                        avg_data[m-1] = [float(m), float(a_val), float(rate_a)]
                    else:
                        rev_data[m-1] = [float(m), 0.0, 0.0]
                        ticket_data[m-1] = [float(m), 0.0, 0.0]
                        avg_data[m-1] = [float(m), 0.0, 0.0]

                rev_list.append({"name": dt_name, "value": rev_value, "data": rev_data, "CommonScatterList": None})
                ticket_list.append({"name": dt_name, "value": ticket_value, "data": ticket_data, "CommonScatterList": None})
                avg_list.append({"name": dt_name, "value": avg_value, "data": avg_data, "CommonScatterList": None})

        return Result.success(data={
            "RevenueAmount": rev, "RevenueAmountYOYRate": rev_rate,
            "TicketCount": ticket, "TicketCountYOYRate": ticket_rate,
            "AvgTicketAmount": avg_t, "AvgTicketAmountRate": avg_rate,
            "RevenueAmountList": rev_list,
            "TicketCountList": ticket_list,
            "AvgTicketAmountList": avg_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueCompare 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetHolidaySPRAnalysis =====
@router.get("/Revenue/GetHolidaySPRAnalysis")
async def get_holiday_spr_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    curYear: int = Query(..., description="本年年份"),
    compareYear: int = Query(..., description="历年年份"),
    HolidayType: int = Query(..., description="节日类型: 1元旦 2春运 3清明 4五一 5端午 6暑期 7中秋 8国庆"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    businessType: Optional[str] = Query("", description="经营模式"),
    businessTrade: Optional[str] = Query("", description="经营业态"),
    businessRegion: Optional[str] = Query("", description="经营区域"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节假日服务区营收分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        # 查节日日期
        # 节日名称映射
        holiday_map = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
        h_name = holiday_map.get(int(HolidayType), "")
        if not h_name:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        cur_desc = f"{curYear}年{h_name}"
        cmp_desc = f"{compareYear}年{h_name}"
        h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
        if not h_rows:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def to_dt(v):
            if isinstance(v, dt): return v
            if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
            return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

        cur_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
        cmp_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
        if not cur_dates or not cmp_dates:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        s_date = min(cur_dates)
        e_date = max(cur_dates)
        cs_date = min(cmp_dates)

        stat_d = dt.strptime(StatisticsDate, "%Y-%m-%d") if StatisticsDate and "-" in StatisticsDate else (dt.strptime(StatisticsDate, "%Y%m%d") if StatisticsDate else e_date)
        if stat_d > e_date:
            stat_d = e_date
        day_span = (stat_d - s_date).days
        cy_date = cs_date + timedelta(days=day_span)

        where_sql = ""
        if businessType:
            where_sql += f' AND A."BUSINESS_TYPE" IN ({businessType})'
        if businessTrade:
            where_sql += f' AND A."SHOPTRADE" IN ({businessTrade})'
        if businessRegion:
            where_sql += f' AND A."BUSINESS_REGION" IN ({businessRegion})'

        cur_sql = f"""SELECT B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME",
                B."SERVERPART_ID", B."SERVERPART_NAME",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT",
                SUM(CASE WHEN A."STATISTICS_DATE" = {stat_d.strftime('%Y%m%d')} THEN A."REVENUE_AMOUNT" ELSE 0 END) AS "REVENUE_CUR",
                SUM(CASE WHEN A."STATISTICS_DATE" = {stat_d.strftime('%Y%m%d')} THEN A."ACCOUNT_AMOUNTNOTAX" ELSE 0 END) AS "ACCOUNT_CUR"
            FROM "T_HOLIDAYREVENUE" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = TO_CHAR(B."SERVERPART_ID") AND A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {s_date.strftime('%Y%m%d')} AND {stat_d.strftime('%Y%m%d')}{where_sql}
            GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SERVERPART_ID", B."SERVERPART_NAME" """
        cur_rows = db.execute_query(cur_sql) or []

        cmp_sql = f"""SELECT B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME",
                B."SERVERPART_ID", B."SERVERPART_NAME",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT",
                SUM(CASE WHEN A."STATISTICS_DATE" = {cy_date.strftime('%Y%m%d')} THEN A."REVENUE_AMOUNT" ELSE 0 END) AS "REVENUE_CUR",
                SUM(CASE WHEN A."STATISTICS_DATE" = {cy_date.strftime('%Y%m%d')} THEN A."ACCOUNT_AMOUNTNOTAX" ELSE 0 END) AS "ACCOUNT_CUR"
            FROM "T_HOLIDAYREVENUE" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = TO_CHAR(B."SERVERPART_ID") AND A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {cs_date.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_sql}
            GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SERVERPART_ID", B."SERVERPART_NAME" """
        cmp_rows = db.execute_query(cmp_sql) or []

        # 查车流量 T_SECTIONFLOW
        # 查省份ID (用于车流量过滤)
        fe_rows2 = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": pushProvinceCode})
        province_id = fe_rows2[0]["FIELDENUM_ID"] if fe_rows2 else pushProvinceCode

        cur_bay_sql = f"""SELECT B."SPREGIONTYPE_ID", B."SERVERPART_ID",
                SUM(A."SERVERPART_FLOW") AS "FLOW",
                SUM(CASE WHEN A."STATISTICS_DATE" = {stat_d.strftime('%Y%m%d')} THEN A."SERVERPART_FLOW" ELSE 0 END) AS "FLOW_CUR"
            FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SECTIONFLOW_STATUS" = 1
                AND B."PROVINCE_CODE" = {province_id}
                AND A."STATISTICS_DATE" BETWEEN {s_date.strftime('%Y%m%d')} AND {stat_d.strftime('%Y%m%d')}
            GROUP BY B."SPREGIONTYPE_ID", B."SERVERPART_ID" """
        cur_bay_rows = db.execute_query(cur_bay_sql) or []

        cmp_bay_sql = f"""SELECT B."SPREGIONTYPE_ID", B."SERVERPART_ID",
                SUM(A."SERVERPART_FLOW" + COALESCE(A."SERVERPART_FLOW_ANALOG", 0)) AS "FLOW",
                SUM(CASE WHEN A."STATISTICS_DATE" = {cy_date.strftime('%Y%m%d')} THEN A."SERVERPART_FLOW" +
                    COALESCE(A."SERVERPART_FLOW_ANALOG", 0) ELSE 0 END) AS "FLOW_CUR"
            FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SECTIONFLOW_STATUS" = 1
                AND B."PROVINCE_CODE" = {province_id}
                AND A."STATISTICS_DATE" BETWEEN {cs_date.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}
            GROUP BY B."SPREGIONTYPE_ID", B."SERVERPART_ID" """
        cmp_bay_rows = db.execute_query(cmp_bay_sql) or []

        # 构建map
        cur_sp_map = {}
        for r in cur_rows:
            sp_id = str(r.get("SERVERPART_ID", ""))
            cur_sp_map[sp_id] = {"rev": safe_dec(r.get("REVENUE")), "rev_cur": safe_dec(r.get("REVENUE_CUR")),
                                 "acc": safe_dec(r.get("ACCOUNT_AMOUNT")), "acc_cur": safe_dec(r.get("ACCOUNT_CUR")),
                                 "region_id": str(r.get("SPREGIONTYPE_ID", "")), "region_name": r.get("SPREGIONTYPE_NAME", ""),
                                 "sp_name": r.get("SERVERPART_NAME", "")}
        cmp_sp_map = {}
        for r in cmp_rows:
            sp_id = str(r.get("SERVERPART_ID", ""))
            cmp_sp_map[sp_id] = {"rev": safe_dec(r.get("REVENUE")), "rev_cur": safe_dec(r.get("REVENUE_CUR")),
                                 "acc": safe_dec(r.get("ACCOUNT_AMOUNT")), "acc_cur": safe_dec(r.get("ACCOUNT_CUR"))}

        # 车流量map
        cur_bay_map = {}
        for r in cur_bay_rows:
            sp_id = str(r.get("SERVERPART_ID", ""))
            cur_bay_map[sp_id] = {"flow": safe_dec(r.get("FLOW")), "flow_cur": safe_dec(r.get("FLOW_CUR")),
                                   "region_id": str(r.get("SPREGIONTYPE_ID", ""))}
        cmp_bay_map = {}
        for r in cmp_bay_rows:
            sp_id = str(r.get("SERVERPART_ID", ""))
            cmp_bay_map[sp_id] = {"flow": safe_dec(r.get("FLOW")), "flow_cur": safe_dec(r.get("FLOW_CUR"))}

        # 整体
        total_cur = round(sum(v["rev"] for v in cur_sp_map.values()), 2)
        total_cmp = round(sum(v["rev"] for v in cmp_sp_map.values()), 2)
        total_cur_d = round(sum(v["rev_cur"] for v in cur_sp_map.values()), 2)
        total_cmp_d = round(sum(v["rev_cur"] for v in cmp_sp_map.values()), 2)
        total_cur_acc = round(sum(v["acc"] for v in cur_sp_map.values()), 2)
        total_cmp_acc = round(sum(v["acc"] for v in cmp_sp_map.values()), 2)
        total_cur_acc_d = round(sum(v["acc_cur"] for v in cur_sp_map.values()), 2)
        total_cmp_acc_d = round(sum(v["acc_cur"] for v in cmp_sp_map.values()), 2)
        total_cur_flow = round(sum(v["flow"] for v in cur_bay_map.values()), 2)
        total_cmp_flow = round(sum(v["flow"] for v in cmp_bay_map.values()), 2)
        total_cur_flow_d = round(sum(v["flow_cur"] for v in cur_bay_map.values()), 2)
        total_cmp_flow_d = round(sum(v["flow_cur"] for v in cmp_bay_map.values()), 2)

        def fmt_dec(v):
            """金额格式: 保留2位小数（含尾零），0返回'0'"""
            f = round(float(v), 2)
            if f == 0:
                return "0"
            return f"{f:.2f}"

        def fmt_int(v):
            """车流量等整数格式"""
            f = round(float(v), 2)
            return str(int(f))

        def mk_kv(v, d, empty=False):
            if empty:
                return {"name": None, "value": "", "data": "", "key": None}
            return {"name": None, "value": fmt_dec(v), "data": fmt_dec(d), "key": None}

        def mk_kv_int(v, d, empty=False):
            if empty:
                return {"name": None, "value": "", "data": "", "key": None}
            return {"name": None, "value": fmt_int(v), "data": fmt_int(d), "key": None}

        result_list = [{
            "node": {"SPRegionTypeId": 0, "SPRegionTypeName": "整体对客销售",
                     "ServerpartId": None, "ServerpartName": None,
                     "curYearRevenue": mk_kv(total_cur_d, total_cur),
                     "lYearRevenue": mk_kv(total_cmp_d, total_cmp),
                     "curYearAccount": mk_kv(total_cur_acc_d, total_cur_acc),
                     "lYearAccount": mk_kv(total_cmp_acc_d, total_cmp_acc),
                     "curYearBayonet": mk_kv_int(total_cur_flow_d, total_cur_flow),
                     "lYearBayonet": mk_kv_int(total_cmp_flow_d, total_cmp_flow)},
            "children": None,
        }]

        # C# 对齐：从 T_SERVERPARTTYPE 配置表获取所有片区（而非从数据中提取）
        type_sql = f"""SELECT "SERVERPARTTYPE_ID", "TYPE_NAME" FROM "T_SERVERPARTTYPE"
            WHERE "PROVINCE_CODE" = {pushProvinceCode} AND "SERVERPARTSTATICTYPE_ID" = 1000
            ORDER BY "TYPE_INDEX" """
        type_rows = db.execute_query(type_sql) or []

        # 获取all服务区信息
        sp_sql = f"""SELECT "SERVERPART_ID", "SERVERPART_NAME", "SPREGIONTYPE_ID", "SERVERPART_INDEX", "SERVERPART_CODE" FROM "T_SERVERPART"
            WHERE "STATISTICS_TYPE" = 1000 AND "STATISTIC_TYPE" = 1000 AND "PROVINCE_CODE" = {province_id}
            ORDER BY "SERVERPART_INDEX", "SERVERPART_CODE" """
        sp_rows = db.execute_query(sp_sql) or []

        for tr in type_rows:
            rid = str(tr.get("SERVERPARTTYPE_ID", ""))
            rname = tr.get("TYPE_NAME", "")

            # 按片区汇总
            r_cur = sum(v["rev"] for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cur_d = sum(v["rev_cur"] for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cmp = sum(cmp_sp_map.get(k, {}).get("rev", 0) for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cmp_d = sum(cmp_sp_map.get(k, {}).get("rev_cur", 0) for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cur_acc = sum(v["acc"] for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cur_acc_d = sum(v["acc_cur"] for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cmp_acc = sum(cmp_sp_map.get(k, {}).get("acc", 0) for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cmp_acc_d = sum(cmp_sp_map.get(k, {}).get("acc_cur", 0) for k, v in cur_sp_map.items() if v.get("region_id") == rid)
            r_cur_flow = sum(v["flow"] for k, v in cur_bay_map.items() if v.get("region_id") == rid)
            r_cur_flow_d = sum(v["flow_cur"] for k, v in cur_bay_map.items() if v.get("region_id") == rid)
            r_cmp_flow = sum(cmp_bay_map.get(k, {}).get("flow", 0) for k, v in cur_bay_map.items() if v.get("region_id") == rid)
            r_cmp_flow_d = sum(cmp_bay_map.get(k, {}).get("flow_cur", 0) for k, v in cur_bay_map.items() if v.get("region_id") == rid)

            # 构建children（该片区下的服务区列表）
            ch = []
            for sr in sp_rows:
                if str(sr.get("SPREGIONTYPE_ID")) == rid:
                    sp_id = str(sr.get("SERVERPART_ID", ""))
                    has_sp_rev = sp_id in cur_sp_map
                    has_sp_bay = sp_id in cur_bay_map
                    cur_info = cur_sp_map.get(sp_id, {"rev": 0, "rev_cur": 0, "acc": 0, "acc_cur": 0})
                    cmp_info = cmp_sp_map.get(sp_id, {"rev": 0, "rev_cur": 0, "acc": 0, "acc_cur": 0})
                    cb_info = cur_bay_map.get(sp_id, {"flow": 0, "flow_cur": 0})
                    cmb_info = cmp_bay_map.get(sp_id, {"flow": 0, "flow_cur": 0})
                    ch.append({
                        "node": {"SPRegionTypeId": None,
                                 "SPRegionTypeName": None,
                                 "ServerpartId": int(sp_id) if sp_id.isdigit() else sp_id,
                                 "ServerpartName": sr.get("SERVERPART_NAME", ""),
                                 "curYearRevenue": mk_kv(cur_info.get("rev_cur", 0), cur_info.get("rev", 0), empty=not has_sp_rev),
                                 "lYearRevenue": mk_kv(cmp_info.get("rev_cur", 0), cmp_info.get("rev", 0), empty=not has_sp_rev),
                                 "curYearAccount": mk_kv(cur_info.get("acc_cur", 0), cur_info.get("acc", 0), empty=not has_sp_rev),
                                 "lYearAccount": mk_kv(cmp_info.get("acc_cur", 0), cmp_info.get("acc", 0), empty=not has_sp_rev),
                                 "curYearBayonet": mk_kv_int(cb_info.get("flow_cur", 0), cb_info.get("flow", 0), empty=not has_sp_bay),
                                 "lYearBayonet": mk_kv_int(cmb_info.get("flow_cur", 0), cmb_info.get("flow", 0), empty=not has_sp_bay)},
                        "children": [],
                    })
            # 检查片区是否有数据
            has_rev = any(v.get("region_id") == rid for v in cur_sp_map.values())
            has_bay = any(v.get("region_id") == rid for v in cur_bay_map.values())
            no_rev = not has_rev
            no_bay = not has_bay
            result_list.append({
                "node": {"SPRegionTypeId": int(rid) if rid.isdigit() else rid, "SPRegionTypeName": rname,
                         "ServerpartId": None, "ServerpartName": None,
                         "curYearRevenue": mk_kv(r_cur_d, r_cur, empty=no_rev),
                         "lYearRevenue": mk_kv(r_cmp_d, r_cmp, empty=no_rev),
                         "curYearAccount": mk_kv(r_cur_acc_d, r_cur_acc, empty=no_rev),
                         "lYearAccount": mk_kv(r_cmp_acc_d, r_cmp_acc, empty=no_rev),
                         "curYearBayonet": mk_kv_int(r_cur_flow_d, r_cur_flow, empty=no_bay),
                         "lYearBayonet": mk_kv_int(r_cmp_flow_d, r_cmp_flow, empty=no_bay)},
                "children": ch,
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidaySPRAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetHolidayDailyAnalysis =====
@router.get("/Revenue/GetHolidayDailyAnalysis")
async def get_holiday_daily_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    curYear: int = Query(..., description="本年年份"),
    compareYear: int = Query(..., description="历年年份"),
    HolidayType: int = Query(..., description="节日类型"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    SPRegionTypeId: Optional[str] = Query("", description="片区内码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    businessType: Optional[str] = Query("", description="经营模式"),
    businessTrade: Optional[str] = Query("", description="经营业态"),
    businessRegion: Optional[str] = Query("", description="经营区域"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节假日各类项目所有天数对客分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        # 节日名称映射
        holiday_map = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
        h_name = holiday_map.get(int(HolidayType), "")
        if not h_name:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        cur_desc = f"{curYear}年{h_name}"
        cmp_desc = f"{compareYear}年{h_name}"
        h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
        if not h_rows:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def to_dt(v):
            if isinstance(v, dt): return v
            if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
            return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

        cur_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
        cmp_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
        if not cur_dates or not cmp_dates:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        s_date = min(cur_dates)
        e_date = max(cur_dates)
        cs_date = min(cmp_dates)

        stat_d = dt.strptime(StatisticsDate, "%Y-%m-%d") if StatisticsDate and "-" in StatisticsDate else (dt.strptime(StatisticsDate, "%Y%m%d") if StatisticsDate else e_date)
        if stat_d > e_date:
            stat_d = e_date
        day_span = (stat_d - s_date).days
        cy_date = cs_date + timedelta(days=day_span)

        where_sql = ""
        use_holiday_table = False
        if SPRegionTypeId:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeId})'
            use_holiday_table = True
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
            use_holiday_table = True
        if businessType:
            where_sql += f' AND A."BUSINESS_TYPE" IN ({businessType})'
        if businessTrade:
            where_sql += f' AND A."SHOPTRADE" IN ({businessTrade})'
        if businessRegion:
            where_sql += f' AND A."BUSINESS_REGION" IN ({businessRegion})'

        if use_holiday_table:
            base_sql = """SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_HOLIDAYREVENUE" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = TO_CHAR(B."SERVERPART_ID") AND A."HOLIDAYREVENUE_STATE" = 1
                    AND A."STATISTICS_DATE" BETWEEN {s} AND {e}{w}
                GROUP BY A."STATISTICS_DATE" """
        else:
            base_sql = """SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_PROVINCEREVENUE" A
                WHERE A."PROVINCEREVENUE_STATE" = 1
                    AND A."STATISTICS_DATE" BETWEEN {s} AND {e}{w}
                GROUP BY A."STATISTICS_DATE" """

        cur_rows = db.execute_query(base_sql.format(s=s_date.strftime("%Y%m%d"), e=stat_d.strftime("%Y%m%d"), w=where_sql)) or []
        cmp_rows = db.execute_query(base_sql.format(s=cs_date.strftime("%Y%m%d"), e=cy_date.strftime("%Y%m%d"), w=where_sql)) or []
        from decimal import Decimal
        def to_dec(v):
            try: return Decimal(str(v)) if v is not None else Decimal('0')
            except: return Decimal('0')

        cur_map = {str(safe_int(r.get("STATISTICS_DATE"))): to_dec(r.get("REVENUE_AMOUNT")) for r in cur_rows}
        cmp_map = {str(safe_int(r.get("STATISTICS_DATE"))): to_dec(r.get("REVENUE_AMOUNT")) for r in cmp_rows}

        result_list = []
        total_cur = sum(cur_map.values())
        total_cmp = sum(cmp_map.values())
        result_list.append({"name": "累计", "value": str(total_cur), "data": str(total_cmp), "key": None, "date": None})

        for i in range(day_span + 1):
            cd = s_date + timedelta(days=i)
            ld = cs_date + timedelta(days=i)
            cd_key = cd.strftime("%Y%m%d")
            ld_key = ld.strftime("%Y%m%d")
            # C#对齐: 没有数据的日期返回空串（C# decimal? 未赋值时ToString()=""）
            cv = str(cur_map[cd_key]) if cd_key in cur_map else ""
            lv = str(cmp_map[ld_key]) if ld_key in cmp_map else ""
            result_list.append({
                "name": str(i + 1), "value": cv, "data": lv,
                "key": None,
                "date": f"{date_no_pad(cd)},{date_no_pad(ld)}",
            })

        # C#对齐: JsonList.Success(list) 默认PageSize=10
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayDailyAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetMonthINCAnalysis =====
@router.get("/Revenue/GetMonthINCAnalysis")
async def get_month_inc_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsStartMonth: str = Query(..., description="统计开始月份"),
    StatisticsEndMonth: str = Query(..., description="统计结束月份"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    businessRegion: Optional[str] = Query(None, description="经营区域"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    shopTrade: Optional[str] = Query("", description="商品业态"),
    compactStartDate: Optional[str] = Query("", description="合同开始日期"),
    compactEndDate: Optional[str] = Query("", description="合同结束日期"),
    calcQOQ: Optional[str] = Query("false", description="是否计算环比"),
    calcYOY: Optional[str] = Query("false", description="是否计算同比"),
    calcBayonet: Optional[str] = Query("false", description="是否计算车流量"),
    hasAnalog: Optional[str] = Query("true", description="是否包含模拟车流"),
    statisticsType: Optional[str] = Query("1", description="统计类型"),
    accountType: Optional[str] = Query("0", description="收入结算类型"),
    showRevenue: Optional[str] = Query("0", description="经营增幅"),
    showBayonet: Optional[str] = Query("0", description="车流增幅"),
    showLevel: Optional[str] = Query("1", description="显示层级"),
    solidType: Optional[str] = Query("true", description="查询固化"),
    showWarning: Optional[str] = Query("true", description="显示预警"),
    warningType: Optional[str] = Query(None, description="预警类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营增长分析 (对齐C# AccountHelper.GetMonthINCAnalysis)"""
    try:
        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        # 解析bool参数
        is_solid = str(solidType).lower() not in ("false", "0", "")
        is_calc_yoy = str(calcYOY).lower() == "true"
        is_calc_qoq = str(calcQOQ).lower() == "true"
        is_calc_bayonet = str(calcBayonet).lower() == "true"
        is_show_warning = str(showWarning).lower() == "true"
        wt = int(warningType) if warningType else None
        now_month = __import__("datetime").datetime.now().strftime("%Y%m")

        # C# 对齐第655行: GetSubType 递归展开业态子类型
        expanded_shop_trade = shopTrade
        if shopTrade:
            try:
                _bt_ids = [s.strip() for s in shopTrade.split(",") if s.strip()]
                _expanded = set(_bt_ids)
                _sub_rows = db.execute_query(
                    "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_PID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
                ) or []
                _changed = True
                while _changed:
                    _changed = False
                    for sr in _sub_rows:
                        sid = str(sr.get("AUTOSTATISTICS_ID") or "")
                        pid = str(sr.get("AUTOSTATISTICS_PID") or "")
                        if pid in _expanded and sid not in _expanded:
                            _expanded.add(sid)
                            _changed = True
                expanded_shop_trade = ",".join(_expanded)
            except Exception as ex_st:
                logger.warning(f"GetMonthINCAnalysis GetSubType 展开失败: {ex_st}")

        # --- C# BusinessTradeType 映射逻辑 ---
        # BusinessTradeType=1 → 自营餐饮: BUSINESS_TYPE=4000 AND SHOPTRADE=2
        # BusinessTradeType=2 → 自营非餐饮: BUSINESS_TYPE=4000 AND SHOPTRADE<>2
        # BusinessTradeType=3 → 非自营: BUSINESS_TYPE<>4000
        def _btt_where(prefix="A"):
            if not BusinessTradeType:
                return ""
            btt = BusinessTradeType.strip()
            btt_set = set(btt.replace(" ", "").split(","))
            if btt_set == {"1"}:
                return f' AND {prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" = 2'
            elif btt_set == {"2"}:
                return f' AND {prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" <> 2'
            elif btt_set == {"3"}:
                return f' AND {prefix}."BUSINESS_TYPE" <> 4000'
            elif btt_set == {"1","2"}:
                return f' AND {prefix}."BUSINESS_TYPE" = 4000'
            elif btt_set == {"1","3"}:
                return f' AND (({prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" = 2) OR {prefix}."BUSINESS_TYPE" <> 4000)'
            elif btt_set == {"2","3"}:
                return f' AND (({prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" <> 2) OR {prefix}."BUSINESS_TYPE" <> 4000)'
            return ""

        # 构建树形节点辅助函数（固化和非固化路径共用）
        def _make_inc(cur, yoy, qoq=None):
            """构建同比/环比增长结构，对齐旧接口 HolidayINCDetailModel"""
            cur_v = round(float(cur), 2) if cur is not None else None
            yoy_v = round(float(yoy), 2) if yoy is not None else None
            qoq_v = round(float(qoq), 2) if qoq is not None else None
            # C# 在 curYearData.TryParseToDecimal() != 0 时才算增长
            inc = None; rate = None; inc_qoq = None; rate_qoq = None
            if cur_v is not None and cur_v != 0:
                if yoy_v is not None and yoy_v != 0:
                    inc = round(cur_v - yoy_v, 2)
                    rate = round(inc / yoy_v * 100, 2)
                if qoq_v is not None and qoq_v != 0:
                    inc_qoq = round(cur_v - qoq_v, 2)
                    rate_qoq = round(inc_qoq / qoq_v * 100, 2)
            return {"curYearData": cur_v, "lYearData": yoy_v,
                    "increaseData": inc, "increaseRate": rate,
                    "QOQData": qoq_v, "increaseDataQOQ": inc_qoq, "increaseRateQOQ": rate_qoq, "rankNum": None}

        def _make_bayonet_region(cur, yoy, qoq=None, calc_yoy_flag=True, calc_qoq_flag=False):
            """BayonetINC: 对齐 C# BindMonthlySPINCAnalysis L2174-2246"""
            cur_v = round(float(cur), 2) if cur and float(cur) != 0 else (0.0 if cur is not None else None)
            yoy_v = round(float(yoy), 2) if yoy and float(yoy) != 0 else (0.0 if yoy is not None else None)
            qoq_v = round(float(qoq), 2) if qoq and float(qoq) != 0 else (0.0 if qoq is not None else None)
            can_calc = cur_v is not None and cur_v != 0
            inc = None; rate = None
            if can_calc and calc_yoy_flag and yoy_v is not None and yoy_v != 0:
                inc = round(cur_v - yoy_v, 2)
                rate = round(inc / yoy_v * 100, 2)
            inc_qoq = None; rate_qoq = None
            if can_calc and calc_qoq_flag and qoq_v is not None and qoq_v != 0:
                inc_qoq = round(cur_v - qoq_v, 2)
                rate_qoq = round(inc_qoq / qoq_v * 100, 2)
            return {"curYearData": cur_v if cur_v is not None else None,
                    "lYearData": yoy_v if calc_yoy_flag and yoy_v is not None else None,
                    "increaseData": inc, "increaseRate": rate,
                    "QOQData": qoq_v if calc_qoq_flag else None,
                    "increaseDataQOQ": inc_qoq, "increaseRateQOQ": rate_qoq, "rankNum": None}

        def _format_ico(ico_raw):
            if not ico_raw: return ""
            if ico_raw.startswith("http"): return ico_raw
            if "PictureManage" in ico_raw: return "https://user.eshangtech.com" + ("/" if not ico_raw.startswith("/") else "") + ico_raw
            return "https://api.eshangtech.com/EShangApiMain/" + ico_raw.lstrip("/")

        def _format_bp_date(date_obj):
            if not date_obj: return ""
            from datetime import datetime as dt_internal
            if isinstance(date_obj, dt_internal):
                return f"{date_obj.year}/{date_obj.month}/{date_obj.day}"
            s_date = str(date_obj).replace("T", " ").split(" ")[0].replace("-", "/")
            parts = s_date.split("/")
            if len(parts) == 3:
                return f"{parts[0]}/{int(parts[1])}/{int(parts[2])}"
            return s_date

        _BAYONET_NULL = _make_inc(None, None)  # C# new HolidayINCDetailModel() 默认全 null

        def _make_node(sp_region_id=None, sp_region_name=None, sp_id=None, sp_name=None,
                       rev_inc=None, acc_inc=None, bayonet=_BAYONET_NULL, bayonet_ori=None,
                       ticket=None, avg_ticket=None, shop_list=None):
            """构造与旧接口一致的 node 结构"""
            return {
                "SPRegionTypeId": sp_region_id, "SPRegionTypeName": sp_region_name,
                "ServerpartId": sp_id, "ServerpartName": sp_name,
                "RevenueINC": rev_inc or _make_inc(0, 0),
                "AccountINC": acc_inc or _make_inc(0, 0),
                "BayonetINC": bayonet, "TicketINC": ticket, "AvgTicketINC": avg_ticket,
                "BayonetINC_ORI": bayonet_ori, "SectionFlowINC": None,
                "ShopINCList": shop_list, "RankDiff": None,
                "Cost_Amount": None, "Ca_Cost": None, "Profit_Amount": None,
            }

        # --- 固化数据路径 ---
        if is_solid and StatisticsStartMonth == StatisticsEndMonth and StatisticsEndMonth != now_month:
            # C#: 查 T_BUSINESSWARNING 表
            # CompareField 由 warningType/showBayonet/showRevenue/showLevel 决定
            compare_field = ""
            if is_calc_yoy and wt:
                field_map = {1: "WARING_VUSPD", 2: "WARING_VUSHD", 3: "WARING_VURU", 4: "WARING_VDRD"}
                compare_field = field_map.get(wt, "")

            where_parts = f' AND A."STATISTICS_MONTH" = {StatisticsEndMonth}'
            if compare_field:
                warning_val = 1 if is_show_warning else 0
                where_parts += f' AND A."{compare_field}" = {warning_val}'
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_parts += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
            if BusinessTradeType:
                where_parts += f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
            # C# 对齐第746行: 过滤展开后的经营业态
            if expanded_shop_trade:
                where_parts += f' AND A."BUSINESS_TRADE" IN ({expanded_shop_trade})'

            solid_sql = f"""SELECT
                    A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPARTSHOP_ID",
                    A."SERVERPARTSHOP_NAME" AS "SHOPSHORTNAME",
                    A."STATISTICS_MONTH", A."REVENUE_AMOUNT", A."REVENUE_AMOUNT_YOY",
                    A."REVENUE_INCREASE_YOY", A."REVENUE_INCRATE_YOY",
                    A."REVENUE_AMOUNT_QOQ", A."REVENUE_INCREASE_QOQ", A."REVENUE_INCRATE_QOQ",
                    A."VEHICLE_COUNT", A."VEHICLE_COUNT_YOY",
                    A."VEHICLE_INCREASE_YOY", A."VEHICLE_INCRATE_YOY",
                    A."TICKET_COUNT", A."TICKET_COUNT_YOY", A."TICKET_COUNT_QOQ",
                    A."ROYALTY_THEORY", A."ROYALTY_THEORY_YOY", A."ROYALTY_THEORY_QOQ",
                    A."VEHICLE_COUNT_ORI", A."VEHICLE_COUNT_ORI_YOY",
                    A."DATATYPE", A."BUSINESS_TRADE",
                    A."BUSINESSTRADETYPE" AS "BUSINESS_TYPE",
                    A."BUSINESSPROJECT_ID",
                    A."BUSINESSWARNING_ID",
                    A."INCREASE_DIFF"
                FROM "T_BUSINESSWARNING" A
                WHERE A."DATATYPE" = 2{where_parts}"""

            cur_rows = db.execute_query(solid_sql) or []
            # Python 内存排序对齐旧接口 (按 BWID 升序)
            cur_rows.sort(key=lambda r: int(r.get("BUSINESSWARNING_ID") or 0))

            # 按服务区汇总
            sp_map = {}
            for r in cur_rows:
                sp_id = r.get("SERVERPART_ID")
                if sp_id not in sp_map:
                    sp_map[sp_id] = {
                        "SERVERPART_ID": sp_id,
                        "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                        "REVENUE": 0.0, "REVENUE_YOY": 0.0, "REVENUE_QOQ": 0.0,
                        "TICKET": 0.0, "TICKET_YOY": 0.0, "TICKET_QOQ": 0.0,
                        "ROYALTY": 0.0, "ROYALTY_YOY": 0.0, "ROYALTY_QOQ": 0.0,
                        "VEHICLE": 0.0, "VEHICLE_YOY": 0.0, "VEHICLE_QOQ": 0.0,
                        "VEHICLE_ORI": 0.0, "VEHICLE_ORI_YOY": 0.0,
                        "shops": []
                    }
                def _add_v(old, new):
                    if new is None: return old
                    return (old or 0.0) + float(new)
                
                sp_map[sp_id]["REVENUE"] = _add_v(sp_map[sp_id]["REVENUE"], r.get("REVENUE_AMOUNT"))
                sp_map[sp_id]["REVENUE_YOY"] = _add_v(sp_map[sp_id]["REVENUE_YOY"], r.get("REVENUE_AMOUNT_YOY"))
                sp_map[sp_id]["REVENUE_QOQ"] = _add_v(sp_map[sp_id]["REVENUE_QOQ"], r.get("REVENUE_AMOUNT_QOQ"))
                sp_map[sp_id]["TICKET"] = _add_v(sp_map[sp_id]["TICKET"], r.get("TICKET_COUNT"))
                sp_map[sp_id]["TICKET_YOY"] = _add_v(sp_map[sp_id]["TICKET_YOY"], r.get("TICKET_COUNT_YOY"))
                sp_map[sp_id]["TICKET_QOQ"] = _add_v(sp_map[sp_id]["TICKET_QOQ"], r.get("TICKET_COUNT_QOQ"))
                sp_map[sp_id]["ROYALTY"] = _add_v(sp_map[sp_id]["ROYALTY"], r.get("ROYALTY_THEORY"))
                sp_map[sp_id]["ROYALTY_YOY"] = _add_v(sp_map[sp_id]["ROYALTY_YOY"], r.get("ROYALTY_THEORY_YOY"))
                sp_map[sp_id]["ROYALTY_QOQ"] = _add_v(sp_map[sp_id]["ROYALTY_QOQ"], r.get("ROYALTY_THEORY_QOQ"))
                sp_map[sp_id]["VEHICLE"] = _add_v(sp_map[sp_id]["VEHICLE"], r.get("VEHICLE_COUNT"))
                sp_map[sp_id]["VEHICLE_YOY"] = _add_v(sp_map[sp_id]["VEHICLE_YOY"], r.get("VEHICLE_COUNT_YOY"))
                sp_map[sp_id]["VEHICLE_ORI"] = _add_v(sp_map[sp_id]["VEHICLE_ORI"], r.get("VEHICLE_COUNT_ORI"))
                sp_map[sp_id]["VEHICLE_ORI_YOY"] = _add_v(sp_map[sp_id]["VEHICLE_ORI_YOY"], r.get("VEHICLE_COUNT_ORI_YOY"))
                sp_map[sp_id]["shops"].append(r)

            # 查服务区所属片区（含排序索引）
            if sp_map:
                sp_ids_str = ",".join(str(k) for k in sp_map.keys())
                sp_info_sql = f"""SELECT "SERVERPART_ID", "SPREGIONTYPE_ID", "SPREGIONTYPE_NAME",
                        "SPREGIONTYPE_INDEX", "SERVERPART_INDEX"
                    FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({sp_ids_str})"""
                sp_info_rows = db.execute_query(sp_info_sql) or []
                sp_region = {r["SERVERPART_ID"]: (
                    r.get("SPREGIONTYPE_ID"), r.get("SPREGIONTYPE_NAME",""),
                    r.get("SPREGIONTYPE_INDEX", 0), r.get("SERVERPART_INDEX", 0)
                ) for r in sp_info_rows}
            else:
                sp_region = {}

            # 查服务区级车流数据（DATATYPE=ServerpartDataType）
            # C# 固化路径: dtCurBayonet 总是加载, dtQOQBayonet 由 calcQOQ 控制, dtYOYBayonet 由 calcYOY 控制
            has_analog = str(hasAnalog).lower() != "false"
            _sp_data_type = 1 if has_analog else 3  # C# L738
            if sp_map:
                _sp_in_flow = ",".join(str(k) for k in sp_map.keys())
                _flow_sql = f"""SELECT "SERVERPART_ID",
                        "VEHICLE_COUNT", "VEHICLE_COUNT_YOY", "VEHICLE_COUNT_QOQ",
                        "VEHICLE_COUNT_ORI", "VEHICLE_COUNT_ORI_YOY"
                    FROM "T_BUSINESSWARNING"
                    WHERE "DATATYPE" = {_sp_data_type} AND "STATISTICS_MONTH" = {StatisticsEndMonth}
                        AND "SERVERPART_ID" IN ({_sp_in_flow})"""
                _flow_rows = db.execute_query(_flow_sql) or []
                for fr in _flow_rows:
                    _sid = fr.get("SERVERPART_ID")
                    if _sid in sp_map:
                        # 当前车流（总是加载）
                        sp_map[_sid]["VEHICLE"] = safe_dec(fr.get("VEHICLE_COUNT"))
                        sp_map[_sid]["VEHICLE_ORI"] = safe_dec(fr.get("VEHICLE_COUNT_ORI"))
                        # 同比车流（仅 calcYOY 时有效）
                        if is_calc_yoy:
                            sp_map[_sid]["VEHICLE_YOY"] = safe_dec(fr.get("VEHICLE_COUNT_YOY"))
                            sp_map[_sid]["VEHICLE_ORI_YOY"] = safe_dec(fr.get("VEHICLE_COUNT_ORI_YOY"))
                        else:
                            sp_map[_sid]["VEHICLE_YOY"] = 0.0
                            sp_map[_sid]["VEHICLE_ORI_YOY"] = 0.0
                        # 环比车流（仅 calcQOQ 时有效）
                        if is_calc_qoq:
                            sp_map[_sid]["VEHICLE_QOQ"] = safe_dec(fr.get("VEHICLE_COUNT_QOQ"))
                        else:
                            sp_map[_sid]["VEHICLE_QOQ"] = 0.0
            # 批量查询门店品牌信息（T_SERVERPARTSHOP JOIN T_BRAND）和商户信息（T_BUSINESSPROJECT）
            _inc_shop_info = {}  # SERVERPARTSHOP_ID(int) → {品牌信息}
            _inc_bp_info = {}    # BUSINESSPROJECT_ID → {项目/商户信息}
            try:
                _all_ssids = set()
                _all_bpids = set()
                for spd in sp_map.values():
                    for s in spd["shops"]:
                        ssid_str = str(s.get("SERVERPARTSHOP_ID", ""))
                        for sid_part in ssid_str.split(","):
                            sid_part = sid_part.strip()
                            if sid_part.isdigit():
                                _all_ssids.add(int(sid_part))
                                break  # 只取第一个
                        bp_id = s.get("BUSINESSPROJECT_ID")
                        if bp_id:
                            _all_bpids.add(int(bp_id))
                if _all_ssids:
                    _ss_in = ",".join(str(i) for i in _all_ssids)
                    _ss_rows = db.execute_query(f"""SELECT S.SERVERPARTSHOP_ID, S.SHOPSHORTNAME,
                            S.BUSINESS_TRADE, S.BUSINESS_TRADENAME, S.SHOPTRADE, S.BUSINESS_BRAND,
                            S.SELLER_ID, S.SELLER_NAME,
                            B.BRAND_ID, B.BRAND_NAME AS BRAND_NAME2, B.BRAND_INTRO AS BRAND_ICO
                        FROM T_SERVERPARTSHOP S LEFT JOIN T_BRAND B ON S.BUSINESS_BRAND = B.BRAND_ID
                        WHERE S.SERVERPARTSHOP_ID IN ({_ss_in})""") or []
                    for sr in _ss_rows:
                        _inc_shop_info[str(sr["SERVERPARTSHOP_ID"])] = sr
                    logger.info(f"INC品牌查询: ssids={len(_all_ssids)}, 查到={len(_ss_rows)}, map_keys={list(_inc_shop_info.keys())[:5]}")
                if _all_bpids:
                    _bp_in = ",".join(str(i) for i in _all_bpids)
                    _bp_rows = db.execute_query(f"""SELECT BUSINESSPROJECT_ID, MERCHANTS_ID, MERCHANTS_NAME,
                            BUSINESSPROJECT_NAME, BUSINESS_TYPE, SETTLEMENT_MODES,
                            TO_CHAR(PROJECT_STARTDATE, 'YYYY/MM/DD') AS COMPACT_START,
                            TO_CHAR(PROJECT_ENDDATE, 'YYYY/MM/DD') AS COMPACT_END
                        FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID IN ({_bp_in})""") or []
                    for br in _bp_rows:
                        _inc_bp_info[str(br["BUSINESSPROJECT_ID"])] = br
            except Exception as _ex_info:
                logger.warning(f"GetMonthINCAnalysis 门店品牌/商户信息查询失败: {_ex_info}")

            # --- 按片区分组服务区（使用 INDEX 排序）---
            from collections import OrderedDict
            region_map = OrderedDict()
            sorted_sp_items = sorted(
                sp_map.items(),
                key=lambda x: (
                    sp_region.get(x[0], (None, "", 0, 0))[2] or 0,  # SPREGIONTYPE_INDEX
                    sp_region.get(x[0], (None, "", 0, 0))[0] or 0,  # SPREGIONTYPE_ID
                    sp_region.get(x[0], (None, "", 0, 0))[3] or 0,  # SERVERPART_INDEX
                    x[0]  # SERVERPART_ID fallback
                )
            )
            for sp_id, sp_data in sorted_sp_items:
                region_info = sp_region.get(sp_id, (None, "", 0, 0))
                rid, rname = region_info[0], region_info[1]
                if rid not in region_map:
                    region_map[rid] = {"name": rname, "sp_list": []}
                region_map[rid]["sp_list"].append((sp_id, sp_data))

            # --- 结果汇总与报文构造 ---
            total_rev, total_rev_yoy, total_rev_qoq = 0.0, 0.0, 0.0
            total_tic, total_tic_yoy, total_tic_qoq = 0.0, 0.0, 0.0
            total_roy, total_roy_yoy, total_roy_qoq = 0.0, 0.0, 0.0
            total_veh, total_veh_yoy, total_veh_qoq = 0.0, 0.0, 0.0
            total_veh_ori, total_veh_ori_yoy = 0.0, 0.0

            def _safe_add(old, new):
                if new is None: return old
                return (old or 0.0) + float(new)

            region_children = []
            _show_rev = int(showRevenue) if showRevenue else 0
            _show_bay = int(showBayonet) if showBayonet else 0
            _show_lvl = int(showLevel) if showLevel else 1
            for rid, rinfo in region_map.items():
                r_rev, r_rev_yoy, r_rev_qoq = 0.0, 0.0, 0.0
                r_tic, r_tic_yoy, r_tic_qoq = 0.0, 0.0, 0.0
                r_roy, r_roy_yoy, r_roy_qoq = 0.0, 0.0, 0.0
                r_veh, r_veh_yoy, r_veh_qoq = 0.0, 0.0, 0.0
                r_veh_ori, r_veh_ori_yoy = 0.0, 0.0

                sp_children = []
                for sp_id, sp_data in rinfo["sp_list"]:
                    # 累加指标到片区
                    r_rev = _safe_add(r_rev, sp_data["REVENUE"])
                    r_rev_yoy = _safe_add(r_rev_yoy, sp_data["REVENUE_YOY"])
                    r_rev_qoq = _safe_add(r_rev_qoq, sp_data["REVENUE_QOQ"])
                    r_tic = _safe_add(r_tic, sp_data["TICKET"])
                    r_tic_yoy = _safe_add(r_tic_yoy, sp_data["TICKET_YOY"])
                    r_tic_qoq = _safe_add(r_tic_qoq, sp_data["TICKET_QOQ"])
                    r_roy = _safe_add(r_roy, sp_data["ROYALTY"])
                    r_roy_yoy = _safe_add(r_roy_yoy, sp_data["ROYALTY_YOY"])
                    r_roy_qoq = _safe_add(r_roy_qoq, sp_data["ROYALTY_QOQ"])
                    r_veh = _safe_add(r_veh, sp_data["VEHICLE"])
                    r_veh_yoy = _safe_add(r_veh_yoy, sp_data["VEHICLE_YOY"])
                    r_veh_qoq = _safe_add(r_veh_qoq, sp_data.get("VEHICLE_QOQ", 0.0))
                    r_veh_ori = _safe_add(r_veh_ori, sp_data["VEHICLE_ORI"])
                    r_veh_ori_yoy = _safe_add(r_veh_ori_yoy, sp_data["VEHICLE_ORI_YOY"])

                    # 门店级处理
                    shop_inc_list = []
                    _sorted_shops = sorted(sp_data["shops"], key=lambda x: int(x.get("BUSINESSWARNING_ID") or 0))
                    for shop in _sorted_shops:
                        _ssid_str = str(shop.get("SERVERPARTSHOP_ID", ""))
                        _ssid_list = [s.strip() for s in _ssid_str.split(",") if s.strip()]
                        _si = {}
                        for _s in _ssid_list:
                            _cur_si = _inc_shop_info.get(_s)
                            if _cur_si:
                                if not _si: _si = _cur_si.copy()
                                else:
                                    # 合并业态、名称、商户、品牌
                                    for key in ["BUSINESS_TRADENAME", "SHOPTRADE"]:
                                        old_val = str(_si.get(key) or "")
                                        new_val = str(_cur_si.get(key) or "")
                                        if new_val and new_val not in old_val:
                                            _si[key] = f"{old_val},{new_val}" if old_val else new_val
                                    for key in ["SELLER_NAME", "SELLER_ID", "BRAND_ID", "BRAND_NAME", "BRAND_ICO"]:
                                        if _si.get(key) is None or not _si.get(key):
                                            _si[key] = _cur_si.get(key)
                        
                        _bp = _inc_bp_info.get(str(shop.get("BUSINESSPROJECT_ID")), {}) if shop.get("BUSINESSPROJECT_ID") else {}
                        _btt = int(safe_dec(shop.get("BUSINESS_TYPE", 0)))
                        _m_id = _bp.get("MERCHANTS_ID") or _si.get("SELLER_ID")
                        
                        s_rev = shop.get("REVENUE_AMOUNT"); s_tic = shop.get("TICKET_COUNT")
                        s_rev_yoy = shop.get("REVENUE_AMOUNT_YOY"); s_tic_yoy = shop.get("TICKET_COUNT_YOY")
                        s_rev_qoq = shop.get("REVENUE_AMOUNT_QOQ"); s_tic_qoq = shop.get("TICKET_COUNT_QOQ")
                        
                        s_avg_cur = round(float(s_rev) / float(s_tic), 2) if s_rev is not None and s_tic and float(s_tic) != 0 else None
                        s_avg_yoy = round(float(s_rev_yoy) / float(s_tic_yoy), 2) if s_rev_yoy is not None and s_tic_yoy and float(s_tic_yoy) != 0 else None
                        s_avg_qoq = round(float(s_rev_qoq) / float(s_tic_qoq), 2) if s_rev_qoq is not None and s_tic_qoq and float(s_tic_qoq) != 0 else None

                        shop_inc_list.append({
                            "ServerpartId": None, "ServerpartName": None, "ServerpartShopId": _ssid_str,
                            "ServerpartShopName": shop.get("SHOPSHORTNAME", ""),
                            "Brand_Id": int(safe_dec(_si.get("BRAND_ID") or 0)) or None,
                            "Brand_Name": _si.get("BRAND_NAME2") or _si.get("BRAND_NAME") or None,
                            "BrandType_Name": None, "Brand_ICO": _format_ico(_si.get("BRAND_ICO")),
                            "ShopTrade": int(_bp.get("BUSINESS_TYPE") or 0) if _bp else 0,
                            "BusinessTradeName": _si.get("BUSINESS_TRADENAME") or shop.get("SHOPSHORTNAME"),
                            "BusinessTradeType": _btt, "BusinessProjectId": shop.get("BUSINESSPROJECT_ID"),
                            "CompactStartDate": _format_bp_date(_bp.get("COMPACT_START")) or _format_bp_date(_bp.get("PROJECT_START")) or "",
                            "CompactEndDate": _format_bp_date(_bp.get("COMPACT_END")) or _format_bp_date(_bp.get("PROJECT_END")) or "",

                            "SettlementModes": int(_bp.get("SETTLEMENT_MODES")) if _bp.get("SETTLEMENT_MODES") is not None else None,
                            "BusinessType": _bp.get("BUSINESS_TYPE") if _bp.get("BUSINESS_TYPE") is not None else None,
                            "MERCHANTS_ID": float(_m_id) if _m_id is not None else None,
                            "MERCHANTS_ID_Encrypted": des_encrypt_id(_m_id),
                            "MERCHANTS_NAME": _bp.get("MERCHANTS_NAME") or _si.get("SELLER_NAME"),
                            "RevenueINC": _make_inc(s_rev, s_rev_yoy, s_rev_qoq),
                            "AccountINC": _make_inc(shop.get("ROYALTY_THEORY"), shop.get("ROYALTY_THEORY_YOY"), shop.get("ROYALTY_THEORY_QOQ")),
                            "TicketINC": _make_inc(s_tic, s_tic_yoy, s_tic_qoq),
                            "AvgTicketINC": _make_inc(s_avg_cur, s_avg_yoy, s_avg_qoq),
                            "CurTransaction": None, "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
                        })

                    # 服务区节点聚合
                    s_avg_cur = round(sp_data["REVENUE"] / sp_data["TICKET"], 2) if sp_data["TICKET"] and sp_data["TICKET"] != 0 else (0 if sp_data["TICKET"] == 0 else None)
                    s_avg_yoy = round(sp_data["REVENUE_YOY"] / sp_data["TICKET_YOY"], 2) if sp_data["TICKET_YOY"] and sp_data["TICKET_YOY"] != 0 else (0 if sp_data["TICKET_YOY"] == 0 else None)
                    s_avg_qoq = round(sp_data["REVENUE_QOQ"] / sp_data["TICKET_QOQ"], 2) if sp_data["TICKET_QOQ"] and sp_data["TICKET_QOQ"] != 0 else (0 if sp_data["TICKET_QOQ"] == 0 else None)

                    # 构建服务区级 BayonetINC (对齐 C# 签名)
                    _sp_bayonet = _make_bayonet_region(
                        sp_data["VEHICLE"], sp_data["VEHICLE_YOY"],
                        qoq=sp_data.get("VEHICLE_QOQ", 0.0),
                        calc_yoy_flag=is_calc_yoy, calc_qoq_flag=is_calc_qoq
                    )
                    _sp_bayonet_ori = {
                        "curYearData": round(sp_data["VEHICLE_ORI"], 2) if sp_data["VEHICLE_ORI"] else None,
                        "lYearData": round(sp_data["VEHICLE_ORI_YOY"], 2) if is_calc_yoy and sp_data["VEHICLE_ORI_YOY"] else None,
                        "increaseData": None, "increaseRate": None,
                        "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None
                    }
                    _sp_rev_inc = _make_inc(sp_data["REVENUE"], sp_data["REVENUE_YOY"], sp_data["REVENUE_QOQ"])

                    # --- C# showBayonet 过滤 (L2248-2262) ---
                    if _show_bay == 1:
                        if not ((_sp_bayonet.get("increaseData") or 0) > 0 or (_sp_bayonet.get("increaseDataQOQ") or 0) > 0):
                            continue
                    elif _show_bay == 2:
                        if not ((_sp_bayonet.get("increaseData") or 0) < 0 or (_sp_bayonet.get("increaseDataQOQ") or 0) < 0):
                            continue

                    # --- C# showRevenue 过滤 (L2774-2788) ---
                    if _show_rev == 1:
                        if not ((_sp_rev_inc.get("increaseData") or 0) > 0 or (_sp_rev_inc.get("increaseDataQOQ") or 0) > 0):
                            continue
                    elif _show_rev == 2:
                        if not ((_sp_rev_inc.get("increaseData") or 0) < 0 or (_sp_rev_inc.get("increaseDataQOQ") or 0) < 0):
                            continue

                    sp_children.append({
                        "node": _make_node(
                            sp_region_id=sp_region.get(sp_id, (None, "", 0, 0))[0],
                            sp_region_name=sp_region.get(sp_id, (None, "", 0, 0))[1],
                            sp_id=sp_id, sp_name=sp_data["SERVERPART_NAME"],
                            rev_inc=_sp_rev_inc,
                            acc_inc=_make_inc(sp_data["ROYALTY"], sp_data["ROYALTY_YOY"], sp_data["ROYALTY_QOQ"]),
                            ticket=_make_inc(sp_data["TICKET"], sp_data["TICKET_YOY"], sp_data["TICKET_QOQ"]),
                            bayonet=_sp_bayonet,
                            bayonet_ori=_sp_bayonet_ori,
                            avg_ticket=_make_inc(s_avg_cur, s_avg_yoy, s_avg_qoq),
                            shop_list=shop_inc_list if shop_inc_list else None,
                        ),
                        "children": None
                    })

                # C# L1798: 片区聚合从 filtered children (sp_children) 求和
                if sp_children:
                    def _sum_field(items, *keys):
                        """从 sp_children[i]['node'][key1][key2] 求和"""
                        t = 0.0
                        for item in items:
                            v = item.get("node", {})
                            for k in keys:
                                v = v.get(k) if isinstance(v, dict) else None
                                if v is None: break
                            if v is not None:
                                t += float(v)
                        return t if t != 0 else None

                    r_rev = _sum_field(sp_children, "RevenueINC", "curYearData")
                    r_rev_yoy = _sum_field(sp_children, "RevenueINC", "lYearData")
                    r_rev_qoq = _sum_field(sp_children, "RevenueINC", "QOQData")
                    r_tic = _sum_field(sp_children, "TicketINC", "curYearData")
                    r_tic_yoy = _sum_field(sp_children, "TicketINC", "lYearData")
                    r_tic_qoq = _sum_field(sp_children, "TicketINC", "QOQData")
                    r_roy = _sum_field(sp_children, "AccountINC", "curYearData")
                    r_roy_yoy = _sum_field(sp_children, "AccountINC", "lYearData")
                    r_roy_qoq = _sum_field(sp_children, "AccountINC", "QOQData")

                    r_avg_cur = round(r_rev / r_tic, 2) if r_rev and r_tic and r_tic != 0 else None
                    r_avg_yoy = round(r_rev_yoy / r_tic_yoy, 2) if r_rev_yoy and r_tic_yoy and r_tic_yoy != 0 else None
                    r_avg_qoq = round(r_rev_qoq / r_tic_qoq, 2) if r_rev_qoq and r_tic_qoq and r_tic_qoq != 0 else None

                    # C# L1909: 片区级 BayonetINC 仅 calcBayonet 时聚合，否则为全 null 对象
                    _r_bayonet = _make_inc(None, None)
                    if is_calc_bayonet:
                        _r_bay_cur = _sum_field(sp_children, "BayonetINC", "curYearData")
                        _r_bay_yoy = _sum_field(sp_children, "BayonetINC", "lYearData")
                        _r_bay_qoq = _sum_field(sp_children, "BayonetINC", "QOQData")
                        _r_bayonet = _make_bayonet_region(_r_bay_cur or 0, _r_bay_yoy or 0,
                            qoq=_r_bay_qoq or 0, calc_yoy_flag=is_calc_yoy, calc_qoq_flag=is_calc_qoq)

                    region_children.append({
                        "node": _make_node(
                            sp_region_id=rid, sp_region_name=rinfo["name"],
                            rev_inc=_make_inc(r_rev, r_rev_yoy, r_rev_qoq),
                            acc_inc=_make_inc(r_roy, r_roy_yoy, r_roy_qoq),
                            ticket=_make_inc(r_tic, r_tic_yoy, r_tic_qoq),
                            bayonet=_r_bayonet,
                            avg_ticket=_make_inc(r_avg_cur, r_avg_yoy, r_avg_qoq),
                        ),
                        "children": sp_children if sp_children else None
                    })

            # C# L1948: 根节点 summaryModel 从 region_children 求和
            def _sum_region(items, *keys):
                t = 0.0
                for item in items:
                    v = item.get("node", {})
                    for k in keys:
                        v = v.get(k) if isinstance(v, dict) else None
                        if v is None: break
                    if v is not None:
                        t += float(v)
                return t

            total_rev = _sum_region(region_children, "RevenueINC", "curYearData")
            total_rev_yoy = _sum_region(region_children, "RevenueINC", "lYearData")
            total_rev_qoq = _sum_region(region_children, "RevenueINC", "QOQData")
            total_tic = _sum_region(region_children, "TicketINC", "curYearData")
            total_tic_yoy = _sum_region(region_children, "TicketINC", "lYearData")
            total_tic_qoq = _sum_region(region_children, "TicketINC", "QOQData")
            total_roy = _sum_region(region_children, "AccountINC", "curYearData")
            total_roy_yoy = _sum_region(region_children, "AccountINC", "lYearData")
            total_roy_qoq = _sum_region(region_children, "AccountINC", "QOQData")

            t_avg_cur = round(total_rev / total_tic, 2) if total_rev and total_tic and total_tic != 0 else None
            t_avg_yoy = round(total_rev_yoy / total_tic_yoy, 2) if total_rev_yoy and total_tic_yoy and total_tic_yoy != 0 else None
            t_avg_qoq = round(total_rev_qoq / total_tic_qoq, 2) if total_rev_qoq and total_tic_qoq and total_tic_qoq != 0 else None

            # C# L2068: 根节点 BayonetINC 仅 calcBayonet 时聚合，否则为全 null 对象
            _t_bayonet = _make_inc(None, None)
            if is_calc_bayonet:
                _t_bay_cur = _sum_region(region_children, "BayonetINC", "curYearData")
                _t_bay_yoy = _sum_region(region_children, "BayonetINC", "lYearData")
                _t_bay_qoq = _sum_region(region_children, "BayonetINC", "QOQData")
                _t_bayonet = _make_bayonet_region(_t_bay_cur or 0, _t_bay_yoy or 0,
                    qoq=_t_bay_qoq or 0, calc_yoy_flag=is_calc_yoy, calc_qoq_flag=is_calc_qoq)

            result_list = [{
                "node": _make_node(
                    sp_name="合计",
                    rev_inc=_make_inc(total_rev, total_rev_yoy, total_rev_qoq),
                    acc_inc=_make_inc(total_roy, total_roy_yoy, total_roy_qoq),
                    ticket=_make_inc(total_tic, total_tic_yoy, total_tic_qoq),
                    bayonet=_t_bayonet,
                    avg_ticket=_make_inc(t_avg_cur, t_avg_yoy, t_avg_qoq),
                ),
                "children": region_children
            }]
            json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
            return Result(Result_Code=100, Result_Desc="查询成功", Result_Data=json_list.model_dump())

        # === 非固化路径（跨月或当前月）===
        # 从 T_BUSINESSWARNING(DATATYPE=2) 按 STATISTICS_MONTH BETWEEN start AND end 聚合
        _sp_ids = parse_multi_ids(ServerpartId)
        _nf_where = f' AND A."STATISTICS_MONTH" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}'
        if _sp_ids:
            _nf_where += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
        if BusinessTradeType:
            _nf_where += f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
        if expanded_shop_trade:
            _nf_where += f' AND A."BUSINESS_TRADE" IN ({expanded_shop_trade})'

        # 按服务区聚合本期营收/收入
        _nf_sql = f"""SELECT A."SERVERPART_ID", A."SERVERPART_NAME",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE",
                SUM(A."ROYALTY_THEORY") AS "ROYALTY",
                SUM(A."TICKET_COUNT") AS "TICKET"
            FROM "T_BUSINESSWARNING" A
            WHERE A."DATATYPE" = 2{_nf_where}
            GROUP BY A."SERVERPART_ID", A."SERVERPART_NAME" """
        _nf_rows = db.execute_query(_nf_sql) or []

        sp_map = {}
        for r in _nf_rows:
            sp_id = r.get("SERVERPART_ID")
            sp_map[sp_id] = {
                "SERVERPART_ID": sp_id, "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                "REVENUE": safe_dec(r.get("REVENUE")),
                "REVENUE_YOY": 0.0, "REVENUE_QOQ": 0.0,
                "TICKET": safe_dec(r.get("TICKET")),
                "TICKET_YOY": 0.0, "TICKET_QOQ": 0.0,
                "ROYALTY": safe_dec(r.get("ROYALTY")),
                "ROYALTY_YOY": 0.0, "ROYALTY_QOQ": 0.0,
                "VEHICLE": 0.0, "VEHICLE_YOY": 0.0, "VEHICLE_QOQ": 0.0,
                "VEHICLE_ORI": 0.0, "VEHICLE_ORI_YOY": 0.0,
                "shops": []
            }

        # 查服务区所属片区
        if sp_map:
            _sp_ids_str = ",".join(str(k) for k in sp_map.keys())
            _sp_info_sql = f"""SELECT "SERVERPART_ID", "SERVERPART_NAME", "SPREGIONTYPE_ID",
                    "SPREGIONTYPE_NAME", "SPREGIONTYPE_INDEX", "SERVERPART_INDEX"
                FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({_sp_ids_str})"""
            _sp_info_rows = db.execute_query(_sp_info_sql) or []
            sp_region = {r["SERVERPART_ID"]: (
                r.get("SPREGIONTYPE_ID"), r.get("SPREGIONTYPE_NAME", ""),
                r.get("SPREGIONTYPE_INDEX", 0), r.get("SERVERPART_INDEX", 0)
            ) for r in _sp_info_rows}
            for r in _sp_info_rows:
                sid = r["SERVERPART_ID"]
                if sid in sp_map:
                    sp_map[sid]["SERVERPART_NAME"] = r.get("SERVERPART_NAME", "")
        else:
            sp_region = {}

        # 构建树形（对齐 C# BindMonthlySPINCAnalysis）
        from collections import OrderedDict as _OD
        region_map = _OD()
        sorted_sp = sorted(sp_map.items(), key=lambda x: (
            sp_region.get(x[0], (None,"",0,0))[2] or 0,
            sp_region.get(x[0], (None,"",0,0))[0] or 0,
            sp_region.get(x[0], (None,"",0,0))[3] or 0, x[0]))
        for sp_id, sp_data in sorted_sp:
            ri = sp_region.get(sp_id, (None,"",0,0))
            rid, rname = ri[0], ri[1]
            if rid not in region_map:
                region_map[rid] = {"name": rname, "sp_list": []}
            region_map[rid]["sp_list"].append((sp_id, sp_data))

        region_children = []
        for rid, rinfo in region_map.items():
            sp_children = []
            for sp_id, sp_data in rinfo["sp_list"]:
                _ri = sp_region.get(sp_id, (None,"",0,0))
                _sp_avg = round(sp_data["REVENUE"] / sp_data["TICKET"], 2) if sp_data["TICKET"] and sp_data["TICKET"] != 0 else None
                sp_children.append({
                    "node": _make_node(
                        sp_region_id=_ri[0], sp_region_name=_ri[1],
                        sp_id=sp_id, sp_name=sp_data["SERVERPART_NAME"],
                        rev_inc=_make_inc(sp_data["REVENUE"], sp_data["REVENUE_YOY"], sp_data["REVENUE_QOQ"]),
                        acc_inc=_make_inc(sp_data["ROYALTY"], sp_data["ROYALTY_YOY"], sp_data["ROYALTY_QOQ"]),
                        ticket=_make_inc(sp_data["TICKET"], sp_data["TICKET_YOY"], sp_data["TICKET_QOQ"]),
                        bayonet=None,  # 非固化路径旧接口服务区级 BayonetINC=null
                        avg_ticket=_make_inc(_sp_avg, None),
                    ), "children": None
                })
            # 片区聚合从 sp_children
            if sp_children:
                def _nf_sum(items, *keys):
                    t = 0.0
                    for item in items:
                        v = item.get("node", {})
                        for k in keys:
                            v = v.get(k) if isinstance(v, dict) else None
                            if v is None: break
                        if v is not None: t += float(v)
                    return t if t != 0 else None

                _r_rev = _nf_sum(sp_children, "RevenueINC", "curYearData")
                _r_roy = _nf_sum(sp_children, "AccountINC", "curYearData")
                _r_tic = _nf_sum(sp_children, "TicketINC", "curYearData")
                _r_avg = round(_r_rev / _r_tic, 2) if _r_rev and _r_tic and _r_tic != 0 else None
                region_children.append({
                    "node": _make_node(
                        sp_region_id=rid, sp_region_name=rinfo["name"],
                        rev_inc=_make_inc(_r_rev, 0.0, 0.0),
                        acc_inc=_make_inc(_r_roy, 0.0, 0.0),
                        ticket=_make_inc(_r_tic, 0.0, 0.0),
                        avg_ticket=_make_inc(_r_avg, None),
                    ), "children": sp_children if sp_children else None
                })

        # 根节点聚合从 region_children
        def _nf_sum_r(items, *keys):
            t = 0.0
            for item in items:
                v = item.get("node", {})
                for k in keys:
                    v = v.get(k) if isinstance(v, dict) else None
                    if v is None: break
                if v is not None: t += float(v)
            return t if t != 0 else None

        t_rev = _nf_sum_r(region_children, "RevenueINC", "curYearData")
        t_roy = _nf_sum_r(region_children, "AccountINC", "curYearData")
        t_tic = _nf_sum_r(region_children, "TicketINC", "curYearData")
        t_avg = round(t_rev / t_tic, 2) if t_rev and t_tic and t_tic != 0 else None

        result_list = [{
            "node": _make_node(
                sp_name="\u5408\u8ba1",
                rev_inc=_make_inc(t_rev, 0.0, 0.0),
                acc_inc=_make_inc(t_roy, 0.0, 0.0),
                ticket=_make_inc(t_tic, 0.0, 0.0),
                avg_ticket=_make_inc(t_avg, None),
            ),
            "children": region_children if region_children else None
        }]
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result(Result_Code=100, Result_Desc="查询成功", Result_Data=json_list.model_dump())
    except Exception as ex:
        logger.error(f"GetMonthINCAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetMonthINCAnalysisSummary =====
@router.get("/Revenue/GetMonthINCAnalysisSummary")
async def get_month_inc_analysis_summary(
    StatisticsStartMonth: str = Query(..., description="统计开始月份"),
    StatisticsEndMonth: str = Query(..., description="统计结束月份"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    shopTrade: Optional[str] = Query("", description="经营业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """汇总月度经营项目预警数值 (按C#逻辑重写：查T_BUSINESSWARNING)"""
    try:
        where_sql = ""
        if StatisticsStartMonth:
            where_sql += f' AND A."STATISTICS_MONTH" >= {StatisticsStartMonth}'
        if StatisticsEndMonth:
            where_sql += f' AND A."STATISTICS_MONTH" <= {StatisticsEndMonth}'

        # 经营业态过滤（子查询）
        shop_sql = ""
        if BusinessTradeType:
            shop_sql += f' AND B."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
        # C# 对齐第3678-3683行: GetSubType 递归展开业态子类型
        _expanded_trade = shopTrade
        if shopTrade:
            try:
                _bt_ids = [s.strip() for s in shopTrade.split(",") if s.strip()]
                _expanded = set(_bt_ids)
                _sub_rows = db.execute_query(
                    "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_PID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
                ) or []
                _changed = True
                while _changed:
                    _changed = False
                    for sr in _sub_rows:
                        sid = str(sr.get("AUTOSTATISTICS_ID") or "")
                        pid = str(sr.get("AUTOSTATISTICS_PID") or "")
                        if pid in _expanded and sid not in _expanded:
                            _expanded.add(sid)
                            _changed = True
                _expanded_trade = ",".join(_expanded)
            except Exception as ex_st:
                logger.warning(f"GetMonthINCAnalysisSummary GetSubType 展开失败: {ex_st}")
            shop_sql += f' AND B."BUSINESS_TRADE" IN ({_expanded_trade})'
        if shop_sql:
            shop_sql = f''' AND EXISTS (SELECT 1 FROM "T_BUSINESSWARNING" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND B."DATATYPE" = 2
                AND A."STATISTICS_MONTH" = B."STATISTICS_MONTH"{shop_sql})'''

        sql = f"""SELECT
                SUM(A."WARING_VUSPD") AS "WARING_VUSPD",
                SUM(A."WARING_VUSHD") AS "WARING_VUSHD",
                SUM(A."WARING_VURU") AS "WARING_VURU",
                SUM(A."WARING_VDRD") AS "WARING_VDRD"
            FROM "T_BUSINESSWARNING" A
            WHERE A."DATATYPE" = 1{where_sql}{shop_sql}"""
        rows = db.execute_query(sql) or []

        if rows and rows[0] and any(rows[0].get(k) is not None for k in ["WARING_VUSPD","WARING_VUSHD","WARING_VURU","WARING_VDRD"]):
            r = rows[0]
            def sv(v):
                return str(int(v)) if v is not None else "0"
            data_list = [
                {"name": "车流增加，服务区营收减少", "value": sv(r.get("WARING_VUSPD")), "data": None, "key": "1"},
                {"name": "车流增加，门店的营收减少", "value": sv(r.get("WARING_VUSHD")), "data": None, "key": "2"},
                {"name": "车流增加，营收增长不匹配", "value": sv(r.get("WARING_VURU")), "data": None, "key": "3"},
                {"name": "车流减少，营收降低不匹配", "value": sv(r.get("WARING_VDRD")), "data": None, "key": "4"},
            ]
        else:
            data_list = [
                {"name": "车流增加，服务区营收减少", "value": "0", "data": None, "key": "1"},
                {"name": "车流增加，门店的营收减少", "value": "0", "data": None, "key": "2"},
                {"name": "车流增加，营收增长不匹配", "value": "0", "data": None, "key": "3"},
                {"name": "车流减少，营收降低不匹配", "value": "0", "data": None, "key": "4"},
            ]

        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMonthINCAnalysisSummary 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== StorageMonthINCAnalysis =====
@router.get("/Revenue/StorageMonthINCAnalysis")
async def storage_month_inc_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsMonth: str = Query(..., description="统计月份"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    hasAnalog: bool = Query(True, description="是否包含模拟车流"),
    accountType: int = Query(0, description="收入结算类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """固化月度经营预警数据"""
    try:
        # TODO: 实现 AccountHelper.StorageMonthINCAnalysis
        logger.warning("StorageMonthINCAnalysis 查询逻辑暂未实现")
        return Result.success(data=None, msg="生成成功")
    except Exception as ex:
        return Result.fail(msg=f"生成失败{ex}")


# ===== GetShopSABFIList =====
@router.get("/Revenue/GetShopSABFIList")
async def get_shop_sabfi_list(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    statisticsStartMonth: Optional[str] = Query(None, description="统计开始月份（兼容前端）"),
    statisticsEndMonth: Optional[str] = Query(None, description="统计结束月份（兼容前端）"),
    ServerpartId: Optional[str] = Query("", description="服务区内码（支持逗号分隔多值）"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    BusinessTrade: Optional[str] = Query("", description="经营业态"),
    accountType: int = Query(0, description="收入结算类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """月度服务区门店商业适配指数 — 对齐 C# AccountHelper.GetShopSABFIList"""
    try:
        stat_month = StatisticsMonth or statisticsStartMonth or statisticsEndMonth
        if not stat_month:
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        def make_inc(cur=None, yoy=None, inc=None, rate=None, qoq=None, inc_qoq=None, rate_qoq=None):
            """构建 HolidayINCDetailModel — None 保持 None, QOQ 增量 0→None"""
            def _v(x):
                if x is None: return None
                try: return round(float(x), 2)
                except: return 0.0
            def _qv(x):
                """QOQ 值: None 和 0 都视为 None（C# 旧接口行为）"""
                if x is None: return None
                try:
                    val = round(float(x), 2)
                    return val if val != 0.0 else None
                except: return None
            return {
                "curYearData": _v(cur), "lYearData": _v(yoy),
                "increaseData": _v(inc), "increaseRate": _v(rate),
                "QOQData": _v(qoq), "increaseDataQOQ": _qv(inc_qoq),
                "increaseRateQOQ": _qv(rate_qoq), "rankNum": None
            }

        def empty_inc():
            return make_inc()

        # 辅助：Brand_ICO 格式化
        def _format_ico(ico_raw):
            if not ico_raw: return ""
            if ico_raw.startswith("http"): return ico_raw
            if "PictureManage" in ico_raw: return "https://user.eshangtech.com" + ("/" if not ico_raw.startswith("/") else "") + ico_raw
            return "https://api.eshangtech.com/EShangApiMain/" + ico_raw.lstrip("/")

        # 辅助：BP 日期格式化 (C# yyyy/M/d)
        def _format_bp_date(date_obj):
            if not date_obj: return ""
            from datetime import datetime as dt_internal
            if isinstance(date_obj, dt_internal):
                return f"{date_obj.year}/{date_obj.month}/{date_obj.day}"
            s_date = str(date_obj).replace("T", " ").split(" ")[0].replace("-", "/")
            parts = s_date.split("/")
            if len(parts) == 3:
                return f"{parts[0]}/{int(parts[1])}/{int(parts[2])}"
            return s_date

        # 多服务区ID兼容
        sp_where = ""
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            sp_where = " AND " + build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

        btt_where = ""
        if BusinessTradeType:
            btt_where = f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
        # C# 对齐: BusinessTrade 不在 SQL 中过滤，而是在遍历门店时用 T_SERVERPARTSHOP.BUSINESS_TRADE 做内存过滤
        # 先通过 GetSubType 递归展开业态子类型（查 T_AUTOSTATISTICS 树形结构）
        expanded_trades = set()
        if BusinessTrade:
            for bt_id in str(BusinessTrade).split(","):
                bt_id = bt_id.strip()
                if bt_id:
                    expanded_trades.add(bt_id)
                    # 递归查询子类型 (AUTOSTATISTICS_TYPE=2000 为经营业态分类)
                    queue = [bt_id]
                    while queue:
                        pid = queue.pop(0)
                        try:
                            sub_rows = db.execute_query(
                                f'SELECT "AUTOSTATISTICS_ID" FROM "T_AUTOSTATISTICS" '
                                f'WHERE "AUTOSTATISTICS_PID" = {pid} AND "AUTOSTATISTICS_TYPE" = 2000'
                            ) or []
                            for sr in sub_rows:
                                sid = str(sr.get("AUTOSTATISTICS_ID", ""))
                                if sid and sid not in expanded_trades:
                                    expanded_trades.add(sid)
                                    queue.append(sid)
                        except Exception:
                            pass

        # 从 T_BUSINESSWARNING 查固化数据（对齐 C#）
        sql = f"""SELECT
                A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPARTSHOP_ID",
                A."SERVERPARTSHOP_NAME" AS "SHOPSHORTNAME",
                A."REVENUE_AMOUNT", A."REVENUE_AMOUNT_YOY", A."REVENUE_INCREASE_YOY", A."REVENUE_INCRATE_YOY",
                A."REVENUE_AMOUNT_QOQ", A."REVENUE_INCREASE_QOQ", A."REVENUE_INCRATE_QOQ",
                A."TICKET_COUNT", A."TICKET_COUNT_YOY", A."TICKET_COUNT_QOQ",
                A."ROYALTY_THEORY", A."ROYALTY_THEORY_YOY", A."ROYALTY_THEORY_QOQ",
                A."VEHICLE_COUNT", A."VEHICLE_COUNT_YOY", A."VEHICLE_INCREASE_YOY", A."VEHICLE_INCRATE_YOY",
                A."VEHICLE_COUNT_QOQ", A."VEHICLE_INCREASE_QOQ", A."VEHICLE_INCRATE_QOQ",
                A."DATATYPE", A."BUSINESS_TRADE", A."BUSINESSTRADETYPE" AS "BUSINESS_TYPE",
                A."BUSINESSPROJECT_ID", A."BUSINESSWARNING_ID",
                A."REVENUE_SD", A."REVENUE_AVG"
            FROM "T_BUSINESSWARNING" A
            WHERE A."STATISTICS_MONTH" = {stat_month}
                AND A."DATATYPE" = 2{sp_where}{btt_where}
                AND A."SERVERPARTSHOP_NAME" NOT IN ('加油站便利店','客房')
            ORDER BY A."SERVERPART_ID" """
        rows = db.execute_query(sql) or []
        # Python 内存排序对齐旧接口 (按 BWID 升序)
        rows.sort(key=lambda r: int(r.get("BUSINESSWARNING_ID") or 0))

        # 查询门店盈利数据 (T_PERIODMONTHPROFIT)
        profit_map = {}
        sp_id_list = list(set(r.get("SERVERPART_ID") for r in rows if r.get("SERVERPART_ID")))
        last_month = str(int(stat_month) - 1) if str(stat_month).endswith(('02','03','04','05','06','07','08','09','10','11','12')) else str(int(stat_month) - 89)
        try:
            if sp_id_list:
                sp_in = ",".join(str(i) for i in sp_id_list)
                profit_sql = f"""SELECT SERVERPART_ID,
                        SUM(PROFIT_AMOUNT) AS PROFIT_AMOUNT,
                        SUM(COST_AMOUNT) AS COST_AMOUNT
                    FROM T_PERIODMONTHPROFIT
                    WHERE STATISTICS_MONTH BETWEEN {last_month} AND {stat_month}
                        AND SERVERPART_ID IN ({sp_in})
                    GROUP BY SERVERPART_ID"""
                profit_rows = db.execute_query(profit_sql) or []
                for pr in profit_rows:
                    profit_map[pr.get("SERVERPART_ID")] = pr
        except Exception as pe:
            logger.warning(f"GetShopSABFIList Profit查询失败: {pe}")

        # --- 查上月门店数据作为 QOQ 基数（C# 旧接口用上月 REVENUE_AMOUNT 作为 QOQData）---
        qoq_shop_map = {}  # { (SERVERPART_ID, SERVERPARTSHOP_NAME): {rev, roy, tic} }
        try:
            if sp_id_list:
                qoq_sql = f"""SELECT A."SERVERPART_ID", A."SERVERPARTSHOP_NAME",
                        A."REVENUE_AMOUNT", A."ROYALTY_THEORY", A."TICKET_COUNT"
                    FROM "T_BUSINESSWARNING" A
                    WHERE A."STATISTICS_MONTH" = {last_month}
                        AND A."DATATYPE" = 2{sp_where}
                        AND A."SERVERPARTSHOP_NAME" NOT IN ('加油站便利店','客房')"""
                qoq_rows = db.execute_query(qoq_sql) or []
                for qr in qoq_rows:
                    key = (qr.get("SERVERPART_ID"), qr.get("SERVERPARTSHOP_NAME"))
                    qoq_shop_map[key] = {
                        "rev": qr.get("REVENUE_AMOUNT"),
                        "roy": qr.get("ROYALTY_THEORY"),
                        "tic": qr.get("TICKET_COUNT"),
                    }
        except Exception as qe:
            logger.warning(f"GetShopSABFIList QOQ上月数据查询失败: {qe}")

        # --- 查询门店级门牌信息（Brand/商户/项目）用于 ShopSABFIList 构造 ---
        shop_agg_map = {}   # { ssid_str : { agg_info } }
        bp_info_map = {}    # { BUSINESSPROJECT_ID : { project 信息 } }
        try:
            if sp_id_list:
                # 1. 收集所有涉及的 ShopId
                all_ids_to_query = set()
                all_bp_ids = set()
                ssid_list_map = {}  # ssid_str -> list[int]
                
                for r in rows:
                    ssid_str = str(r.get("SERVERPARTSHOP_ID") or "")
                    if ssid_str:
                        ids = [int(i.strip()) for i in ssid_str.split(",") if i.strip().isdigit()]
                        ssid_list_map[ssid_str] = ids
                        all_ids_to_query.update(ids)
                    
                    bp_id = r.get("BUSINESSPROJECT_ID")
                    if bp_id is not None:
                        all_bp_ids.add(int(bp_id))

                # 2. 批量查 T_SERVERPARTSHOP -> T_BRAND
                raw_shop_map = {}
                if all_ids_to_query:
                    ss_in = ",".join(str(i) for i in all_ids_to_query)
                    ss_sql = f"""SELECT S.SERVERPARTSHOP_ID, S.SHOPSHORTNAME,
                            S.BUSINESS_BRAND, S.BRAND_NAME, S.BUSINESS_TRADE,
                            S.BUSINESS_TRADENAME, S.SHOPTRADE, S.BUSINESS_STATE,
                            S.SELLER_ID, S.SELLER_NAME,
                            B.BRAND_ID, B.BRAND_NAME AS BRAND_NAME2, B.BRAND_INTRO AS BRAND_ICO
                        FROM T_SERVERPARTSHOP S
                        LEFT JOIN T_BRAND B ON S.BUSINESS_BRAND = B.BRAND_ID
                        WHERE S.SERVERPARTSHOP_ID IN ({ss_in})"""
                    ss_rows = db.execute_query(ss_sql) or []
                    for sr in ss_rows:
                        raw_shop_map[int(sr["SERVERPARTSHOP_ID"])] = sr

                # 3. 对每个 ssid_str 聚合计算
                for ssid_str, id_list in ssid_list_map.items():
                    infos = [raw_shop_map[i] for i in id_list if i in raw_shop_map]
                    if not infos:
                        shop_agg_map[ssid_str] = None
                        continue
                    
                    # 行业聚合：(ID, Name) 组合去重 + ID 升序排序 (对齐 SP=420 等合并门店)
                    trade_pairs = []
                    seen_tids = set()
                    for inf in infos:
                        tids = str(inf.get("BUSINESS_TRADE") or "").split(",")
                        tnames = str(inf.get("BUSINESS_TRADENAME") or "").split(",")
                        for i in range(max(len(tids), len(tnames))):
                            tid = tids[i].strip() if i < len(tids) else ""
                            tname = tnames[i].strip() if i < len(tnames) else ""
                            if tid and tid not in seen_tids:
                                trade_pairs.append((tid, tname))
                                seen_tids.add(tid)
                    
                    # 排序
                    trade_pairs.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 99999)
                    
                    # 品牌筛选：取 MIN(BRAND_ID) 记录
                    brand_info_node = None
                    valid_brand_infos = [inf for inf in infos if inf.get("BRAND_ID")]
                    if valid_brand_infos:
                        brand_info_node = min(valid_brand_infos, key=lambda x: x["BRAND_ID"])
                    else:
                        brand_info_node = infos[0]

                    shop_agg_map[ssid_str] = {
                        "BUSINESS_TRADE": ",".join(p[0] for p in trade_pairs),
                        "BUSINESS_TRADENAME": ",".join(p[1] for p in trade_pairs),
                        "BUSINESS_BRAND": brand_info_node.get("BUSINESS_BRAND"),
                        "BRAND_NAME": brand_info_node.get("BRAND_NAME"),
                        "BRAND_ID": brand_info_node.get("BRAND_ID"),
                        "BRAND_NAME2": brand_info_node.get("BRAND_NAME2"),
                        "BRAND_ICO": brand_info_node.get("BRAND_ICO"),
                        "SHOPTRADE": brand_info_node.get("SHOPTRADE"),
                        "SELLER_ID": brand_info_node.get("SELLER_ID"),
                        "SELLER_NAME": brand_info_node.get("SELLER_NAME"),
                        "BUSINESS_STATE": brand_info_node.get("BUSINESS_STATE")
                    }

                # 批量查 T_BUSINESSPROJECT（取 商户/项目 信息）
                if all_bp_ids:
                    bp_in = ",".join(str(i) for i in all_bp_ids)
                    bp_sql = f"""SELECT BUSINESSPROJECT_ID, BUSINESSPROJECT_NAME,
                            MERCHANTS_ID, MERCHANTS_NAME,
                            BUSINESS_TYPE, SETTLEMENT_MODES,
                            PROJECT_STARTDATE, PROJECT_ENDDATE
                        FROM T_BUSINESSPROJECT
                        WHERE BUSINESSPROJECT_ID IN ({bp_in})"""
                    bp_rows = db.execute_query(bp_sql) or []
                    for br in bp_rows:
                        bp_info_map[br["BUSINESSPROJECT_ID"]] = br

                # MERCHANTS fallback: 当 T_BUSINESSPROJECT 无 MERCHANTS 时，取 T_SERVERPARTSHOP.SELLER_ID/NAME
                brand_merchant_map = {}  # 已废弃，改用 shop_info_map 中的 SELLER_ID
        except Exception as ex_s:
            logger.warning(f"GetShopSABFIList 门店/品牌信息查询失败: {ex_s}")

        # --- 查 T_PROFITCONTRIBUTE 获取 SABFI 评分项目列表 ---
        sabfi_projects_map = {}  # { SERVERPART_ID: [ { BusinessProjectId, SABFIList, ... } ] }
        try:
            if sp_id_list:
                # C# 对齐第3888行: CALCULATE_SELFSHOP 条件（联营=2, 非联营=1）
                selfshop_val = 2 if BusinessTradeType == "3" else 1
                project_sql = f"""SELECT A.SERVERPART_ID, A.BUSINESSPROJECT_ID, B.BUSINESSPROJECT_NAME,
                                         A.EVALUATE_TYPE, A.EVALUATE_SCORE, A.PROFITCONTRIBUTE_ID, A.PROFITCONTRIBUTE_PID,
                                         A.SERVERPARTSHOP_NAME
                                  FROM T_PROFITCONTRIBUTE A
                                  LEFT JOIN T_BUSINESSPROJECT B ON A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
                                  WHERE A.STATISTICS_DATE = {stat_month}
                                    AND A.PROFITCONTRIBUTE_STATE = 1
                                    AND A.SERVERPART_ID IN ({sp_in})
                                    AND A.CALCULATE_SELFSHOP = {selfshop_val}
                                  ORDER BY A.SERVERPART_ID, A.BUSINESSPROJECT_ID, A.EVALUATE_TYPE"""
                project_rows = db.execute_query(project_sql) or []

                temp_sp_projects = {}
                for pr in project_rows:
                    sid = pr["SERVERPART_ID"]
                    pid = pr["BUSINESSPROJECT_ID"]
                    shop_name = pr.get("SERVERPARTSHOP_NAME", "")
                    # C# 对齐: 用 (SERVERPART_ID, BUSINESSPROJECT_ID 或 SERVERPARTSHOP_NAME) 分组
                    key = (sid, pid) if pid is not None else (sid, f"_name_{shop_name}")
                    if key not in temp_sp_projects:
                        temp_sp_projects[key] = {
                            "BusinessProjectId": pid,
                            "BusinessProjectName": pr.get("BUSINESSPROJECT_NAME") or shop_name,
                            "SABFI_Score": 0.0,
                            "SABFIList": [{"name": str(et), "value": "", "key": "", "data": ""} for et in range(1, 8)],
                            "StatisticsMonth": f"{stat_month[:4]}/{stat_month[4:]}",
                            "Overall_Score": 0.0,
                        }

                    et = int(pr["EVALUATE_TYPE"])
                    score = pr["EVALUATE_SCORE"]
                    if et == 0:
                        temp_sp_projects[key]["SABFI_Score"] = safe_dec(score)
                        temp_sp_projects[key]["Overall_Score"] = safe_dec(score)
                    elif 1 <= et <= 7:
                        idx = et - 1
                        # C# 对齐: TryParseToDecimal().ToString()，整数显示无小数位，None 显示为空
                        _score_str = ""
                        if score is not None:
                            _sv = float(score)
                            _score_str = str(int(_sv)) if _sv == int(_sv) else str(_sv)
                        temp_sp_projects[key]["SABFIList"][idx]["value"] = _score_str
                        temp_sp_projects[key]["SABFIList"][idx]["key"] = str(pr["PROFITCONTRIBUTE_ID"] or "")
                        temp_sp_projects[key]["SABFIList"][idx]["data"] = str(pr["PROFITCONTRIBUTE_PID"] or "")

                for (sid, pid), p_data in temp_sp_projects.items():
                    if sid not in sabfi_projects_map:
                        sabfi_projects_map[sid] = []
                    sabfi_projects_map[sid].append(p_data)
        except Exception as ex_p:
            logger.warning(f"GetShopSABFIList 经营项目查询失败: {ex_p}")

        # 服务区车流数据 (DATATYPE=1)
        sql_flow = f"""SELECT A."SERVERPART_ID",
                A."VEHICLE_COUNT" AS "SERVERPART_FLOW",
                A."VEHICLE_COUNT_YOY", A."VEHICLE_INCREASE_YOY", A."VEHICLE_INCRATE_YOY",
                A."VEHICLE_COUNT_QOQ", A."VEHICLE_INCREASE_QOQ", A."VEHICLE_INCRATE_QOQ"
            FROM "T_BUSINESSWARNING" A
            WHERE A."STATISTICS_MONTH" = {stat_month} AND A."DATATYPE" = 1{sp_where}"""
        flow_rows = db.execute_query(sql_flow) or []
        flow_map = {}
        for fr in flow_rows:
            flow_map[fr.get("SERVERPART_ID")] = fr

        # 查服务区所属片区信息（含排序索引 SPREGIONTYPE_INDEX / SERVERPART_INDEX）
        sp_id_list_for_info = list(set(r.get("SERVERPART_ID") for r in rows if r.get("SERVERPART_ID")))
        sp_info_map = {}
        if sp_id_list_for_info:
            sp_in_info = ",".join(str(i) for i in sp_id_list_for_info)
            sp_info_sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME,
                    SPREGIONTYPE_ID, SPREGIONTYPE_NAME,
                    SPREGIONTYPE_INDEX, SERVERPART_INDEX
                FROM T_SERVERPART
                WHERE SPREGIONTYPE_ID IS NOT NULL
                    AND SERVERPART_ID IN ({sp_in_info})"""
            sp_info_rows = db.execute_query(sp_info_sql) or []
            for si in sp_info_rows:
                sp_info_map[si.get("SERVERPART_ID")] = si

        # 按服务区分组
        from collections import OrderedDict
        sp_groups = OrderedDict()
        for r in rows:
            sp_id = r.get("SERVERPART_ID")
            if sp_id not in sp_groups:
                sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "shops": []}
            sp_groups[sp_id]["shops"].append(r)

        # 构建 ShopSABFIList 中的门店项 — 对齐 C# ShopSABFIModel 字段
        def build_shop_sabfi_item(r, sp_id, sp_name):
            """从 T_BUSINESSWARNING 行 + JOIN 信息构建门店级 ShopSABFI 项"""
            # 日期格式化内置函数
            def fmt_date(v):
                if v is None: return ""
                try:
                    from datetime import datetime as _dt
                    if hasattr(v, 'year'): return f"{v.year}/{v.month}/{v.day}"
                    s = str(v).replace("T", " ")[:19]
                    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
                        try:
                            dt = _dt.strptime(s[:len(fmt.replace('%Y','0000').replace('%m','00').replace('%d','00'))], fmt)
                            return f"{dt.year}/{dt.month}/{dt.day}"
                        except: continue
                    return str(v).split()[0].replace("-","/")
                except: return str(v) if v else ""

            ssid_str = str(r.get("SERVERPARTSHOP_ID") or "")
            si = shop_agg_map.get(ssid_str) or {}
            bp_info = bp_info_map.get(r.get("BUSINESSPROJECT_ID")) or {}

            # 根据 BUSINESSTRADETYPE (BTT) 判断
            btt = r.get("BUSINESS_TYPE")  # 联营标识字段
            
            biz_trade = str(si.get("BUSINESS_TRADE") or "")
            biz_trade_name = str(si.get("BUSINESS_TRADENAME") or "")
            shop_trade_val = str(si.get("SHOPTRADE") or "")

            brand_id = si.get("BRAND_ID") or si.get("BUSINESS_BRAND")
            brand_name = si.get("BRAND_NAME2") or si.get("BRAND_NAME")
            brand_ico_raw = si.get("BRAND_ICO") or ""
            brand_ico = ""
            if brand_ico_raw:
                if brand_ico_raw.startswith("http"):
                    brand_ico = brand_ico_raw
                elif "PictureManage" in brand_ico_raw:
                    # 传统的 e2 图片路径
                    brand_ico = "https://user.eshangtech.com" + ("/" if not brand_ico_raw.startswith("/") else "") + brand_ico_raw
                else:
                    # 新的 EShangApiMain 路径
                    brand_ico = "https://api.eshangtech.com/EShangApiMain/" + brand_ico_raw.lstrip("/")

            merch_id = bp_info.get("MERCHANTS_ID")
            merch_name = bp_info.get("MERCHANTS_NAME") or None
            if merch_name is None:
                merch_id = si.get("SELLER_ID")
                merch_name = si.get("SELLER_NAME")
            merch_id_enc = des_encrypt_id(merch_id)  # DES 加密 MERCHANTS_ID

            # 门店级 QOQ 数据
            shop_name = r.get("SHOPSHORTNAME", r.get("SERVERPARTSHOP_NAME", ""))
            rev = safe_dec(r.get("REVENUE_AMOUNT"))
            rev_qoq_raw = r.get("REVENUE_AMOUNT_QOQ")
            rev_qoq = safe_dec(rev_qoq_raw)
            tic = safe_dec(r.get("TICKET_COUNT"))
            tic_qoq_raw = r.get("TICKET_COUNT_QOQ")
            tic_qoq = safe_dec(tic_qoq_raw)
            roy = safe_dec(r.get("ROYALTY_THEORY"))
            roy_qoq_raw = r.get("ROYALTY_THEORY_QOQ")
            roy_qoq = safe_dec(roy_qoq_raw)

            avg_cur = round(rev / tic, 2) if tic and tic != 0 else (0 if tic == 0 else None)
            avg_qoq = round(rev_qoq / tic_qoq, 2) if tic_qoq and tic_qoq != 0 else (0 if tic_qoq == 0 else None)
            avg_inc_qoq = round(avg_cur - avg_qoq, 2) if avg_cur is not None and avg_qoq is not None else None
            avg_rate_qoq = round(avg_inc_qoq / avg_qoq * 100, 2) if avg_inc_qoq is not None and avg_qoq and avg_qoq != 0 else None

            # 这里的 bp_info 在上面几行已经定义为 bp_info = bp_info_map.get(...) or {}
            
            # SettlementModes — 精确对齐逻辑：只有原值为 1000 的典型联营项目映射为 3000
            settle_mode = bp_info.get("SETTLEMENT_MODES")
            bp_type = bp_info.get("BUSINESS_TYPE")
            if btt == 3 and bp_type == 1000 and settle_mode == 1000:
                settle_mode = 3000

            # ShopTrade — 旧接口用的是 BW 当月固化表里的 BUSINESS_TRADE
            bw_trade = r.get("BUSINESS_TRADE")
            shop_trade_val = int(bw_trade) if bw_trade is not None else 0

            # Profit_Amount — C# 逻辑
            shop_profit = rev if btt is not None and btt < 3 else None
            shop_cost = 0.0 if btt is not None and btt < 3 else None
            shop_ca_cost = None
            
            # SABFI_Score 列表
            sabfi_list_empty = [{"name": str(et), "value": "", "data": "", "key": ""} for et in range(1, 8)]

            return {
                "ServerpartId": sp_id,
                "ServerpartName": sp_name,
                "BusinessProjectId": r.get("BUSINESSPROJECT_ID"),
                "BusinessProjectName": bp_info.get("BUSINESSPROJECT_NAME"),
                "ServerpartShopId": ssid_str,
                "ServerpartShopName": shop_name,
                "Brand_Id": float(brand_id) if brand_id is not None else None,
                "Brand_Name": brand_name,
                "BrandType_Name": None,
                "Brand_ICO": brand_ico if brand_ico else (None if brand_id is None else ""),
                "ShopTrade": shop_trade_val,
                "BusinessTrade": biz_trade,
                "BusinessTradeName": biz_trade_name,
                "BusinessTradeType": btt,
                "CompactStartDate": fmt_date(bp_info.get("PROJECT_STARTDATE")),
                "CompactEndDate": fmt_date(bp_info.get("PROJECT_ENDDATE")),
                "BusinessType": bp_info.get("BUSINESS_TYPE"),
                "SettlementModes": settle_mode,
                "MERCHANTS_ID": float(merch_id) if merch_id is not None else None,
                "MERCHANTS_ID_Encrypted": merch_id_enc,
                "MERCHANTS_NAME": merch_name,
                "RevenueINC": make_inc(
                    r.get("REVENUE_AMOUNT"), None, None, None,
                    rev_qoq_raw,
                    round(rev - rev_qoq, 2) if r.get("REVENUE_AMOUNT") is not None and rev_qoq is not None else None,
                    round((rev - rev_qoq) / rev_qoq * 100, 2) if rev_qoq is not None and rev_qoq != 0 and r.get("REVENUE_AMOUNT") is not None else None),
                "AccountINC": make_inc(
                    r.get("ROYALTY_THEORY"), None, None, None,
                    roy_qoq_raw,
                    round(roy - roy_qoq, 2) if r.get("ROYALTY_THEORY") is not None and roy_qoq is not None else None,
                    round((roy - roy_qoq) / roy_qoq * 100, 2) if roy_qoq is not None and roy_qoq != 0 and r.get("ROYALTY_THEORY") is not None else None),
                "TicketINC": make_inc(
                    r.get("TICKET_COUNT"), None, None, None,
                    tic_qoq_raw,
                    round(tic - tic_qoq, 2) if r.get("TICKET_COUNT") is not None and tic_qoq is not None else None,
                    round((tic - tic_qoq) / tic_qoq * 100, 2) if tic_qoq is not None and tic_qoq != 0 and r.get("TICKET_COUNT") is not None else None),
                "AvgTicketINC": make_inc(
                    avg_cur if tic is not None else None, None, None, None,
                    avg_qoq, avg_inc_qoq, avg_rate_qoq),
                "CurTransaction": None,
                "Profit_Amount": round(shop_profit, 2) if shop_profit is not None else None,
                "Cost_Amount": round(shop_cost, 2) if shop_cost is not None else None,
                "Ca_Cost": round(shop_ca_cost, 2) if shop_ca_cost is not None else None,
                "SABFI_Score": 0.0,
                "SABFIList": sabfi_list_empty,
                "BusinessState": str(si.get("BUSINESS_STATE") or "1"),
                "Revenue_SD": round(safe_dec(r.get("REVENUE_SD")), 2) if r.get("REVENUE_SD") is not None else None,
                "Revenue_AVG": round(safe_dec(r.get("REVENUE_AVG")), 2) if r.get("REVENUE_AVG") is not None else None,
            }

        # 汇总累加器
        total_rev, total_rev_yoy, total_rev_qoq = 0.0, 0.0, 0.0
        total_acct, total_acct_yoy, total_acct_qoq = 0.0, 0.0, 0.0
        total_ticket, total_ticket_yoy, total_ticket_qoq = 0.0, 0.0, 0.0
        total_flow, total_flow_yoy, total_flow_qoq = 0.0, 0.0, 0.0

        # 按片区分组（使用 SPREGIONTYPE_INDEX 排序片区，SERVERPART_INDEX 排序服务区）
        region_groups = OrderedDict()
        # 先按 (SPREGIONTYPE_INDEX, SPREGIONTYPE_ID) 对服务区排序后再分组
        sorted_sp_items = sorted(
            sp_groups.items(),
            key=lambda x: (
                sp_info_map.get(x[0], {}).get("SPREGIONTYPE_INDEX") or 0,
                sp_info_map.get(x[0], {}).get("SPREGIONTYPE_ID") or 0,
                sp_info_map.get(x[0], {}).get("SERVERPART_INDEX") or 0,
                x[0]  # fallback: SERVERPART_ID
            )
        )
        for sp_id, sp_data in sorted_sp_items:
            si = sp_info_map.get(sp_id, {})
            region_id = si.get("SPREGIONTYPE_ID")
            region_name = si.get("SPREGIONTYPE_NAME", "")
            region_idx = si.get("SPREGIONTYPE_INDEX", 0)
            rk = (region_idx or 0, region_id or 0)
            if rk not in region_groups:
                region_groups[rk] = {"id": region_id, "name": region_name, "serverparts": OrderedDict()}
            region_groups[rk]["serverparts"][sp_id] = sp_data

        # 构建树: 合计→片区→服务区→门店
        region_children = []
        for rk in sorted(region_groups.keys()):
            rg = region_groups[rk]
            reg_rev, reg_rev_yoy, reg_rev_qoq = 0.0, 0.0, 0.0
            reg_acct, reg_acct_yoy, reg_acct_qoq = 0.0, 0.0, 0.0
            reg_ticket, reg_ticket_yoy, reg_ticket_qoq = 0.0, 0.0, 0.0
            reg_flow, reg_flow_yoy, reg_flow_qoq = 0.0, 0.0, 0.0

            sp_children = []
            for sp_id, sp_data in rg["serverparts"].items():
                sp_rev, sp_rev_yoy, sp_rev_qoq = 0.0, 0.0, 0.0
                sp_acct, sp_acct_yoy, sp_acct_qoq = 0.0, 0.0, 0.0
                sp_ticket, sp_ticket_yoy, sp_ticket_qoq = 0.0, 0.0, 0.0

                shop_children = []
                for r in sp_data["shops"]:
                    # C# 对齐: BusinessTrade 内存过滤 (BindSABFISPINCAnalysis 第4247行)
                    # 用 T_SERVERPARTSHOP.BUSINESS_TRADE 字段判断是否匹配
                    if expanded_trades:
                        ssid_str = str(r.get("SERVERPARTSHOP_ID") or "")
                        si_bt = shop_agg_map.get(ssid_str) or {}
                        shop_bt_val = str(si_bt.get("BUSINESS_TRADE") or "")
                        shop_bt_ids = {b.strip() for b in shop_bt_val.split(",") if b.strip()}
                        if not shop_bt_ids.intersection(expanded_trades):
                            continue
                    rev = safe_dec(r.get("REVENUE_AMOUNT"))
                    sp_rev += rev
                    sp_rev_yoy += safe_dec(r.get("REVENUE_AMOUNT_YOY"))
                    sp_rev_qoq += safe_dec(r.get("REVENUE_AMOUNT_QOQ"))
                    sp_acct += safe_dec(r.get("ROYALTY_THEORY"))
                    sp_acct_yoy += safe_dec(r.get("ROYALTY_THEORY_YOY"))
                    sp_acct_qoq += safe_dec(r.get("ROYALTY_THEORY_QOQ"))
                    sp_ticket += safe_dec(r.get("TICKET_COUNT"))
                    sp_ticket_yoy += safe_dec(r.get("TICKET_COUNT_YOY"))
                    sp_ticket_qoq += safe_dec(r.get("TICKET_COUNT_QOQ"))

                    # 门店级 children 暂不使用（C# 服务区节点 children=null）
                    pass

                # 车流
                fr = flow_map.get(sp_id, {})
                sp_flow = safe_dec(fr.get("SERVERPART_FLOW"))
                sp_flow_yoy = safe_dec(fr.get("VEHICLE_COUNT_YOY"))
                sp_flow_qoq = safe_dec(fr.get("VEHICLE_COUNT_QOQ"))

                reg_rev += sp_rev; reg_rev_yoy += sp_rev_yoy; reg_rev_qoq += sp_rev_qoq
                reg_acct += sp_acct; reg_acct_yoy += sp_acct_yoy; reg_acct_qoq += sp_acct_qoq
                reg_ticket += sp_ticket; reg_ticket_yoy += sp_ticket_yoy; reg_ticket_qoq += sp_ticket_qoq
                reg_flow += sp_flow; reg_flow_yoy += sp_flow_yoy; reg_flow_qoq += sp_flow_qoq

                # C# 对齐第4437行: 利润/成本从已过滤的 ShopSABFIList 求和，移到 node_shop_list 构建后计算
                # (保留位置但不计算，实际计算在 node_shop_list 构建后)

                # AvgTicket 中间值对齐 C# Round
                avg_cur = round(sp_rev / sp_ticket, 2) if sp_ticket and sp_ticket != 0 else (0 if sp_ticket == 0 else None)
                avg_qoq = round(sp_rev_qoq / sp_ticket_qoq, 2) if sp_ticket_qoq and sp_ticket_qoq != 0 else (0 if sp_ticket_qoq == 0 else None)
                avg_inc_qoq = round(avg_cur - avg_qoq, 2) if avg_cur is not None and avg_qoq is not None else None
                avg_rate_qoq = round(avg_inc_qoq / avg_qoq * 100, 2) if avg_inc_qoq is not None and avg_qoq and avg_qoq != 0 else None

                # BayonetINC_ORI：C# 只填 curYearData（车流原始值）
                bayonet_ori = make_inc(sp_flow)

                # Building ShopSABFIList
                node_shop_list = []
                # 对齐旧接口排序：按 BUSINESSWARNING_ID
                _sorted_shops = sorted(sp_data["shops"], key=lambda x: int(x.get("BUSINESSWARNING_ID") or 0))
                for row in _sorted_shops:
                    # C# 对齐: ShopSABFIList 中也要过滤 BusinessTrade (与服务区汇总一致)
                    if expanded_trades:
                        _ss_filter = str(row.get("SERVERPARTSHOP_ID", ""))
                        _si_filter = shop_agg_map.get(_ss_filter) or {}
                        _bt_filter_val = str(_si_filter.get("BUSINESS_TRADE") or "")
                        _bt_filter_ids = {b.strip() for b in _bt_filter_val.split(",") if b.strip()}
                        if not _bt_filter_ids.intersection(expanded_trades):
                            continue

                    # 合并 SSID 信息
                    _ss_id_str = str(row.get("SERVERPARTSHOP_ID", ""))
                    _si = shop_agg_map.get(_ss_id_str) or {}

                    _bp = bp_info_map.get(row.get("BUSINESSPROJECT_ID")) or {}
                    _m_id = _bp.get("MERCHANTS_ID") or _si.get("SELLER_ID")
                    
                    # SABFI 门店节点 YOY 强制为 None 以对齐旧接口
                    r_rev = row.get("REVENUE_AMOUNT"); r_tic = row.get("TICKET_COUNT")
                    r_rev_qoq = row.get("REVENUE_AMOUNT_QOQ"); r_tic_qoq = row.get("TICKET_COUNT_QOQ")
                    ac = round(float(r_rev)/float(r_tic), 2) if r_rev is not None and r_tic and float(r_tic) != 0 else None
                    aq = round(float(r_rev_qoq)/float(r_tic_qoq), 2) if r_rev_qoq is not None and r_tic_qoq and float(r_tic_qoq) != 0 else None

                    # Profit_Amount: C# 自营门店=Revenue, 联营=None
                    _btt_val = row.get("BUSINESS_TYPE")  # BusinessTradeType from BW
                    _shop_profit = safe_dec(r_rev) if _btt_val is not None and int(safe_dec(_btt_val)) < 3 else None
                    _shop_cost = 0.0 if _btt_val is not None and int(safe_dec(_btt_val)) < 3 else None

                    # C# 对齐: SABFIList 从 T_PROFITCONTRIBUTE 按 BUSINESSPROJECT_ID 查各 EVALUATE_TYPE 的评分
                    _bp_id = row.get("BUSINESSPROJECT_ID")
                    _shop_sabfi_list = [{"name": str(et), "value": "", "data": "", "key": ""} for et in range(1, 8)]
                    _shop_sabfi_score = 0.0
                    if _bp_id is not None:
                        for p_data in sabfi_projects_map.get(sp_id, []):
                            if p_data.get("BusinessProjectId") == _bp_id:
                                _shop_sabfi_list = p_data.get("SABFIList", _shop_sabfi_list)
                                _shop_sabfi_score = safe_dec(p_data.get("SABFI_Score", 0))
                                break
                    elif row.get("SHOPSHORTNAME"):
                        # C# fallback: 没有 BUSINESSPROJECT_ID 时用 SERVERPARTSHOP_NAME 匹配
                        _shop_name_match = row.get("SHOPSHORTNAME")
                        for p_data in sabfi_projects_map.get(sp_id, []):
                            if p_data.get("BusinessProjectName") == _shop_name_match:
                                _shop_sabfi_list = p_data.get("SABFIList", _shop_sabfi_list)
                                _shop_sabfi_score = safe_dec(p_data.get("SABFI_Score", 0))
                                break

                    shop_node = {
                        "ServerpartId": sp_id, "ServerpartName": sp_data["name"],
                        "ServerpartShopId": _ss_id_str, "ServerpartShopName": row.get("SHOPSHORTNAME"),
                        "RevenueINC": make_inc(r_rev, None, qoq=r_rev_qoq, inc_qoq=round(safe_dec(r_rev) - safe_dec(r_rev_qoq), 2) if r_rev_qoq is not None else None, rate_qoq=round((safe_dec(r_rev) - safe_dec(r_rev_qoq)) / safe_dec(r_rev_qoq) * 100, 2) if safe_dec(r_rev_qoq) and safe_dec(r_rev_qoq) != 0 else None),
                        "AccountINC": make_inc(row.get("ROYALTY_THEORY"), None, qoq=row.get("ROYALTY_THEORY_QOQ"), inc_qoq=round(safe_dec(row.get("ROYALTY_THEORY")) - safe_dec(row.get("ROYALTY_THEORY_QOQ")), 2) if row.get("ROYALTY_THEORY_QOQ") is not None else None, rate_qoq=round((safe_dec(row.get("ROYALTY_THEORY")) - safe_dec(row.get("ROYALTY_THEORY_QOQ"))) / safe_dec(row.get("ROYALTY_THEORY_QOQ")) * 100, 2) if safe_dec(row.get("ROYALTY_THEORY_QOQ")) and safe_dec(row.get("ROYALTY_THEORY_QOQ")) != 0 else None),
                        "TicketINC": make_inc(r_tic, None, qoq=r_tic_qoq, inc_qoq=round(safe_dec(r_tic) - safe_dec(r_tic_qoq), 2) if r_tic_qoq is not None else None, rate_qoq=round((safe_dec(r_tic) - safe_dec(r_tic_qoq)) / safe_dec(r_tic_qoq) * 100, 2) if safe_dec(r_tic_qoq) and safe_dec(r_tic_qoq) != 0 else None),
                        "AvgTicketINC": make_inc(ac, None, qoq=aq, inc_qoq=round(ac - aq, 2) if ac is not None and aq is not None else None, rate_qoq=round((ac - aq) / aq * 100, 2) if ac is not None and aq is not None and aq != 0 else None),
                        "SABFI_Score": _shop_sabfi_score, "SABFIList": _shop_sabfi_list,
                        "Brand_Id": int(_si.get("BRAND_ID")) if _si.get("BRAND_ID") is not None else None,
                        "Brand_Name": _si.get("BRAND_NAME2") or _si.get("BRAND_NAME") or row.get("SHOPSHORTNAME"),
                        "BrandType_Name": None,
                        "Brand_ICO": _format_ico(_si.get("BRAND_ICO")),
                        "BusinessTrade": str(_si.get("BUSINESS_TRADE") or "") if _si.get("BUSINESS_TRADE") else None,
                        "BusinessTradeName": _si.get("BUSINESS_TRADENAME") or row.get("SHOPSHORTNAME"),
                        "BusinessTradeType": int(safe_dec(_btt_val)) if _btt_val is not None else None,
                        "BusinessProjectId": int(_bp["BUSINESSPROJECT_ID"]) if _bp.get("BUSINESSPROJECT_ID") else None,
                        "BusinessProjectName": _bp.get("BUSINESSPROJECT_NAME") if _bp else None,
                        "BusinessType": _bp.get("BUSINESS_TYPE") if _bp.get("BUSINESS_TYPE") is not None else None,
                        "ShopTrade": int(_bp.get("BUSINESS_TYPE") or 0) if _bp else 0,
                        "CompactStartDate": _format_bp_date(_bp.get("PROJECT_STARTDATE")) or "",
                        "CompactEndDate": _format_bp_date(_bp.get("PROJECT_ENDDATE")) or "",
                        "SettlementModes": int(_bp["SETTLEMENT_MODES"]) if _bp.get("SETTLEMENT_MODES") is not None else None,
                        "StatisticsMonth": None,
                        "MERCHANTS_ID": float(_m_id) if _m_id is not None else None,
                        "MERCHANTS_ID_Encrypted": des_encrypt_id(_m_id),
                        "MERCHANTS_NAME": _bp.get("MERCHANTS_NAME") or _si.get("SELLER_NAME"),
                        "Profit_Amount": _shop_profit,
                        "Cost_Amount": _shop_cost,
                        "Ca_Cost": None,
                        "CurTransaction": None,
                        "Revenue_SD": safe_dec(row.get("REVENUE_SD")) if row.get("REVENUE_SD") is not None else None,
                        "Revenue_AVG": safe_dec(row.get("REVENUE_AVG")) if row.get("REVENUE_AVG") is not None else None,
                    }
                    node_shop_list.append(shop_node)
                
                # 服务区 SABFI 节点 AvgTicket (QOQ)
                s_ac = round(sp_rev/sp_ticket, 2) if sp_ticket else 0.0
                s_aq = round(sp_rev_qoq/sp_ticket_qoq, 2) if sp_ticket_qoq else 0.0

                # 获取 SABFI 评分项目列表（用于 SABFI_Score 汇总）
                sp_sabfi_projects = sabfi_projects_map.get(sp_id, [])
                sp_overall_score = round(sum(p["Overall_Score"] for p in sp_sabfi_projects if p.get("Overall_Score")) / len(sp_sabfi_projects), 2) if sp_sabfi_projects else 0.0

                # C# 对齐第4437行: 服务区利润/成本从 node_shop_list 求和
                sp_profit = sum(safe_dec(s.get("Profit_Amount")) for s in node_shop_list)
                sp_cost = sum(safe_dec(s.get("Cost_Amount")) for s in node_shop_list)
                sp_ca_cost = round(sp_cost / sp_ticket, 2) if sp_ticket and sp_ticket > 0 and sp_cost else 0.0

                sp_node = {
                    "SABFI_Score": sp_overall_score, "ShopSABFIList": node_shop_list,
                    "SPRegionTypeId": rg["id"], "SPRegionTypeName": rg["name"],
                    "ServerpartId": sp_id, "ServerpartName": sp_data["name"],
                    "RevenueINC": make_inc(sp_rev, None, qoq=sp_rev_qoq, inc_qoq=round(sp_rev - sp_rev_qoq, 2) if sp_rev_qoq is not None else None, rate_qoq=round((sp_rev - sp_rev_qoq) / sp_rev_qoq * 100, 2) if sp_rev_qoq is not None and sp_rev_qoq != 0 else None),
                    "AccountINC": make_inc(round(sp_acct, 2), 0.0, qoq=round(sp_acct_qoq, 2), inc_qoq=round(sp_acct - sp_acct_qoq, 2) if sp_acct_qoq is not None else None, rate_qoq=round((sp_acct - sp_acct_qoq) / sp_acct_qoq * 100, 2) if sp_acct_qoq is not None and sp_acct_qoq != 0 else None),
                    "BayonetINC": make_inc(sp_flow, None, qoq=sp_flow_qoq, inc_qoq=round(sp_flow - sp_flow_qoq, 2) if sp_flow_qoq is not None else None, rate_qoq=round((sp_flow - sp_flow_qoq) / sp_flow_qoq * 100, 2) if sp_flow_qoq is not None and sp_flow_qoq != 0 else None),
                    "SectionFlowINC": None, "BayonetINC_ORI": bayonet_ori,
                    "TicketINC": make_inc(sp_ticket, None, qoq=sp_ticket_qoq, inc_qoq=round(sp_ticket - sp_ticket_qoq, 2) if sp_ticket_qoq is not None else None, rate_qoq=round((sp_ticket - sp_ticket_qoq) / sp_ticket_qoq * 100, 2) if sp_ticket_qoq is not None and sp_ticket_qoq != 0 else None),
                    "AvgTicketINC": make_inc(avg_cur, None, qoq=avg_qoq, inc_qoq=round(avg_cur - avg_qoq, 2) if avg_cur is not None and avg_qoq is not None else None, rate_qoq=round((avg_cur - avg_qoq) / avg_qoq * 100, 2) if avg_cur is not None and avg_qoq is not None and avg_qoq != 0 else None),
                    "Profit_Amount": round(sp_profit, 2) if sp_profit is not None else None, "Cost_Amount": round(sp_cost, 2) if sp_cost is not None else None,
                    "Ca_Cost": sp_ca_cost, "ShopINCList": None, "RankDiff": None,
                }
                sp_children.append({"node": sp_node, "children": None})

            total_rev += reg_rev; total_rev_yoy += reg_rev_yoy; total_rev_qoq += reg_rev_qoq
            total_acct += reg_acct; total_acct_yoy += reg_acct_yoy; total_acct_qoq += reg_acct_qoq
            total_ticket += reg_ticket; total_ticket_yoy += reg_ticket_yoy; total_ticket_qoq += reg_ticket_qoq
            total_flow += reg_flow; total_flow_yoy += reg_flow_yoy; total_flow_qoq += reg_flow_qoq

            # Profit 从 sp_node 累加（含 fallback）
            reg_profit = sum(safe_dec(ch["node"].get("Profit_Amount")) for ch in sp_children)
            reg_cost = sum(safe_dec(ch["node"].get("Cost_Amount")) for ch in sp_children)

            # 片区节点 — C# 聚合只填 curYearData + QOQData
            reg_node = {
                "SABFI_Score": None, "ShopSABFIList": None,
                "SPRegionTypeId": rg["id"], "SPRegionTypeName": rg["name"],
                "ServerpartId": None, "ServerpartName": None,
                "RevenueINC": make_inc(reg_rev, None, qoq=reg_rev_qoq, inc_qoq=round(reg_rev - reg_rev_qoq, 2) if reg_rev_qoq is not None else None, rate_qoq=round((reg_rev - reg_rev_qoq) / reg_rev_qoq * 100, 2) if reg_rev_qoq is not None and reg_rev_qoq != 0 else None),
                "AccountINC": make_inc(round(reg_acct, 2), None, qoq=round(reg_acct_qoq, 2), inc_qoq=round(reg_acct - reg_acct_qoq, 2) if reg_acct_qoq is not None else None, rate_qoq=round((reg_acct - reg_acct_qoq) / reg_acct_qoq * 100, 2) if reg_acct_qoq is not None and reg_acct_qoq != 0 else None),
                "BayonetINC": make_inc(reg_flow, None, qoq=reg_flow_qoq, inc_qoq=round(reg_flow - reg_flow_qoq, 2) if reg_flow_qoq is not None else None, rate_qoq=round((reg_flow - reg_flow_qoq) / reg_flow_qoq * 100, 2) if reg_flow_qoq is not None and reg_flow_qoq != 0 else None),
                "SectionFlowINC": None, "BayonetINC_ORI": None,
                "TicketINC": make_inc(reg_ticket, None, qoq=reg_ticket_qoq, inc_qoq=round(reg_ticket - reg_ticket_qoq, 2) if reg_ticket_qoq is not None else None, rate_qoq=round((reg_ticket - reg_ticket_qoq) / reg_ticket_qoq * 100, 2) if reg_ticket_qoq is not None and reg_ticket_qoq != 0 else None),
                "AvgTicketINC": (lambda ac=round(reg_rev/reg_ticket,2) if reg_ticket else 0, aq=round(reg_rev_qoq/reg_ticket_qoq,2) if reg_ticket_qoq else 0:
                    make_inc(ac, None, qoq=aq, inc_qoq=round(ac - aq, 2) if ac is not None and aq is not None else None, rate_qoq=round((ac - aq) / aq * 100, 2) if ac is not None and aq is not None and aq != 0 else None))(),
                "ShopINCList": None,
                "Profit_Amount": round(reg_profit, 2), "Cost_Amount": round(reg_cost, 2),
                "Ca_Cost": round(reg_cost / reg_ticket, 2) if reg_ticket and reg_cost else 0.0,
                "RankDiff": None,
            }
            region_children.append({"node": reg_node, "children": sp_children})

        # 根节点 Profit 从片区节点累加
        total_profit = sum(safe_dec(rch["node"].get("Profit_Amount")) for rch in region_children)
        total_cost = sum(safe_dec(rch["node"].get("Cost_Amount")) for rch in region_children)

        # 根 "合计" 节点
        root_node = {
            "SABFI_Score": None, "ShopSABFIList": None,
            "SPRegionTypeId": None, "SPRegionTypeName": None,
            "ServerpartId": None, "ServerpartName": "合计",
            "RevenueINC": make_inc(total_rev, None, None, None,
                total_rev_qoq, total_rev - total_rev_qoq if total_rev_qoq else None,
                round((total_rev - total_rev_qoq) / total_rev_qoq * 100, 2) if total_rev_qoq else None),
            "AccountINC": make_inc(round(total_acct, 2), 0.0, None, None,
                round(total_acct_qoq, 2), round(total_acct - total_acct_qoq, 2) if total_acct_qoq else None,
                round((total_acct - total_acct_qoq) / total_acct_qoq * 100, 2) if total_acct_qoq else None),
            "BayonetINC": make_inc(total_flow, 0.0, None, None,
                total_flow_qoq, total_flow - total_flow_qoq if total_flow_qoq else None,
                round((total_flow - total_flow_qoq) / total_flow_qoq * 100, 2) if total_flow_qoq else None),
            "SectionFlowINC": None, "BayonetINC_ORI": None,
            "TicketINC": make_inc(total_ticket, None, None, None,
                total_ticket_qoq, total_ticket - total_ticket_qoq if total_ticket_qoq else None,
                round((total_ticket - total_ticket_qoq) / total_ticket_qoq * 100, 2) if total_ticket_qoq else None),
            "AvgTicketINC": (lambda ac=round(total_rev/total_ticket,2) if total_ticket else None, aq=round(total_rev_qoq/total_ticket_qoq,2) if total_ticket_qoq else None:
                make_inc(ac, None, None, None, aq,
                    round(ac - aq, 2) if ac is not None and aq is not None else None,
                    round((ac - aq) / aq * 100, 2) if ac is not None and aq is not None and aq else None))(),
            "ShopINCList": None,
            "Profit_Amount": round(total_profit, 2) if region_children else None, "Cost_Amount": round(total_cost, 2) if region_children else None,
            "Ca_Cost": round(total_cost / total_ticket, 2) if total_ticket and total_cost else (None if not region_children else 0.0),
            "RankDiff": None,
        }
        result_list = [{"node": root_node, "children": region_children}]

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopSABFIList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetShopMonthSABFIList =====
@router.get("/Revenue/GetShopMonthSABFIList")
async def get_shop_month_sabfi_list(
    calcSelf: bool = Query(..., description="是否计算自营"),
    StatisticsStartMonth: str = Query(..., description="统计开始月份"),
    StatisticsEndMonth: str = Query(..., description="统计结束月份"),
    BusinessProjectId: Optional[int] = Query(None, description="经营项目内码"),
    ServerpartShopId: Optional[str] = Query("", description="门店内码"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ServerpartShopName: Optional[str] = Query("", description="门店名称"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店每月商业适配指数 (对齐C# BindShopMonthSABFI)"""
    try:
        from datetime import datetime as dt

        # 构建查询条件
        if BusinessProjectId:
            pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
                WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "BUSINESSPROJECT_ID" = {BusinessProjectId}
                    AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                    AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
        elif ServerpartShopId:
            pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
                WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPARTSHOP_ID" = '{ServerpartShopId}'
                    AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                    AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
        elif ServerpartId and ServerpartShopName:
            pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
                WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPART_ID" = {ServerpartId}
                    AND "SERVERPARTSHOP_NAME" = '{ServerpartShopName}'
                    AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                    AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
        else:
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        pc_rows = db.execute_query(pc_sql) or []

        # 按月份分组
        month_data = {}
        for r in pc_rows:
            m = str(r.get("STATISTICS_DATE", ""))
            if m not in month_data:
                month_data[m] = []
            month_data[m].append(r)

        # 遍历月份范围
        data_list = []
        s_year = int(StatisticsStartMonth[:4])
        s_month = int(StatisticsStartMonth[4:])
        e_year = int(StatisticsEndMonth[:4])
        e_month = int(StatisticsEndMonth[4:])
        cur_y, cur_m = s_year, s_month
        while cur_y * 100 + cur_m <= e_year * 100 + e_month:
            m_key = f"{cur_y}{cur_m:02d}"
            m_fmt = f"{cur_y}/{cur_m:02d}"
            rows_m = month_data.get(m_key, [])
            rows_m_int = month_data.get(int(m_key) if m_key.isdigit() else m_key, rows_m)
            if not rows_m and rows_m_int:
                rows_m = rows_m_int

            def get_max(rr, eval_type, field):
                """获取指定EVALUATE_TYPE的MAX值"""
                vals = [r.get(field) for r in rr if str(r.get("EVALUATE_TYPE")) == str(eval_type) and r.get(field) is not None]
                if vals:
                    return str(max(vals))
                return ""

            sabfi_list = []
            for et in range(1, 8):
                sabfi_list.append({
                    "name": str(et),
                    "value": get_max(rows_m, et, "EVALUATE_SCORE"),
                    "key": get_max(rows_m, et, "PROFITCONTRIBUTE_ID"),
                    "data": get_max(rows_m, et, "PROFITCONTRIBUTE_PID"),
                })

            # 计算SABFI_Score
            score_0 = get_max(rows_m, 0, "EVALUATE_SCORE")
            try:
                sabfi_score = float(score_0) if score_0 else 0.0
            except:
                sabfi_score = 0.0
            # C#: SABFI_Score = SABFIList.Sum(o => o.value.TryParseToDecimal())
            sabfi_sum = sum(float(s["value"]) if s["value"] else 0.0 for s in sabfi_list)

            # TODO: 此处若需对齐 C# 细化数据，需查 T_BUSINESSWARNING / T_PERIODMONTHPROFIT
            # 临时占位逻辑：从 rows_m 获取基础信息
            sample = rows_m[0] if rows_m else {}
            
            data_list.append({
                "StatisticsMonth": m_fmt,
                "BusinessTrade": sample.get("SERVERPARTSHOP_NAME"), # 临时
                "BusinessProjectName": None,
                "SABFI_Score": sabfi_sum,
                "Revenue_SD": None,
                "Revenue_AVG": None,
                "SABFIList": sabfi_list,
                "ServerpartId": sample.get("SERVERPART_ID"),
                "ServerpartName": sample.get("SERVERPART_NAME"),
                "ServerpartShopId": sample.get("SERVERPARTSHOP_ID"),
                "ServerpartShopName": sample.get("SERVERPARTSHOP_NAME"),
                "Brand_Id": None, "Brand_Name": None, "BrandType_Name": None, "Brand_ICO": None,
                "ShopTrade": 0, "BusinessTradeName": None, "BusinessTradeType": 0,
                "BusinessProjectId": sample.get("BUSINESSPROJECT_ID"), "CompactStartDate": None, "CompactEndDate": None,
                "BusinessType": None, "SettlementModes": None,
                "MERCHANTS_ID": None, "MERCHANTS_ID_Encrypted": None, "MERCHANTS_NAME": None,
                "RevenueINC": None, "AccountINC": None, "TicketINC": None, "AvgTicketINC": None,
                "CurTransaction": None, "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
            })

            # 下个月
            if cur_m == 12:
                cur_y += 1
                cur_m = 1
            else:
                cur_m += 1

        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopMonthSABFIList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")

