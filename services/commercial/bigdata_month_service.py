# -*- coding: utf-8 -*-
"""
CommercialApi - 大数据月度分析 Service
从 bigdata_router.py 中抽取: GetMonthAnalysis, GetProvinceMonthAnalysis
"""
from typing import Optional
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition

from services.commercial.service_utils import (
    safe_float as _sf,
)




def get_month_analysis(db: DatabaseHelper, statistics_date, province_code, start_date, end_date,
                       sp_region_type_id, serverpart_id, serverpart_region, serverpart_shop_ids) -> list[dict]:
    """获取月度车流分析数据"""
    from datetime import datetime as dt
    import calendar

    if not statistics_date:
        return []

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    start = dt(stat_date.year, 1, 1).strftime("%Y%m%d")
    end = stat_date.strftime("%Y%m%d")

    where_sql = ""
    if serverpart_id:
        where_sql += f' AND A."SERVERPART_ID" = {serverpart_id}'
    elif sp_region_type_id:
        where_sql += f' AND C."SPREGIONTYPE_ID" IN ({sp_region_type_id})'

    # 查断面+出区流量 按月+方位
    sf_sql = f"""SELECT A."SERVERPART_REGION", SUBSTR(TO_CHAR(A."STATISTICS_DATE"),1,6) AS "STATISTICS_MONTH",
            COUNT(DISTINCT A."STATISTICS_DATE") AS "DATE_COUNT",
            SUM(A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0)) AS "VEHICLE_COUNT",
            SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
        FROM "T_SECTIONFLOW" A, "T_SERVERPART" C
        WHERE A."SERVERPART_ID" = C."SERVERPART_ID"
            AND A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0) > 0
            AND A."SECTIONFLOW_STATUS" = 1 AND A."SECTIONFLOW_NUM" > 0
            AND A."STATISTICS_DATE" BETWEEN {start} AND {end}{where_sql}
        GROUP BY A."SERVERPART_REGION", SUBSTR(TO_CHAR(A."STATISTICS_DATE"),1,6)"""
    sf_rows = db.execute_query(sf_sql) or []

    sf_map = {}
    sf_region_map = {}
    for r in sf_rows:
        m = str(r.get("STATISTICS_MONTH", "")).strip()
        region = str(r.get("SERVERPART_REGION", "")).strip()
        vc = _sf(r.get("VEHICLE_COUNT"))
        sf = _sf(r.get("SECTIONFLOW_NUM"))
        days = int(_sf(r.get("DATE_COUNT")))
        if m not in sf_map:
            sf_map[m] = {"days": 0, "vc": 0.0, "sf": 0.0}
        sf_map[m]["days"] = max(sf_map[m]["days"], days)
        sf_map[m]["vc"] += vc
        sf_map[m]["sf"] += sf
        sf_region_map[(m, region)] = {"days": days, "vc": vc, "sf": sf}

    # 查小型车入区 按月
    mv_sql = f"""SELECT SUBSTR(TO_CHAR(A."STATISTICS_DATE"),1,6) AS "STATISTICS_MONTH",
            COUNT(DISTINCT A."STATISTICS_DATE") AS "DATE_COUNT",
            SUM(A."VEHICLE_COUNT") AS "VEHICLE_COUNT",
            SUM(CASE WHEN A."VEHICLE_TYPE" = '小型车' THEN A."VEHICLE_COUNT" END) AS "MINVEHICLE_COUNT"
        FROM "T_BAYONETDAILY_AH" A, "T_SERVERPART" C
        WHERE A."SERVERPART_ID" = C."SERVERPART_ID"
            AND A."INOUT_TYPE" = 0 AND A."VEHICLE_COUNT" > 0
            AND A."STATISTICS_DATE" BETWEEN {start} AND {end}{where_sql}
        GROUP BY SUBSTR(TO_CHAR(A."STATISTICS_DATE"),1,6)"""
    mv_rows = db.execute_query(mv_sql) or []
    mv_map = {}
    for r in mv_rows:
        m = str(r.get("STATISTICS_MONTH", "")).strip()
        mv_map[m] = {"days": int(_sf(r.get("DATE_COUNT"))), "vc": _sf(r.get("VEHICLE_COUNT")), "min": _sf(r.get("MINVEHICLE_COUNT"))}

    # 查营收 按月
    rev_where = ""
    if serverpart_id:
        rev_where += f' AND A."SERVERPART_ID" = {serverpart_id}'
    rev_sql = f"""SELECT SUBSTR(TO_CHAR(A."STATISTICS_DATE"),1,6) AS "STATISTICS_MONTH",
            COUNT(DISTINCT A."STATISTICS_DATE") AS "DATE_COUNT",
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."REVENUEDAILY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000
            AND A."STATISTICS_DATE" >= {start} AND A."STATISTICS_DATE" <= {end}{rev_where}
        GROUP BY SUBSTR(TO_CHAR(A."STATISTICS_DATE"),1,6)"""
    rev_rows = db.execute_query(rev_sql) or []
    rev_map = {}
    for r in rev_rows:
        m = str(r.get("STATISTICS_MONTH", "")).strip()
        rev_map[m] = {"days": int(_sf(r.get("DATE_COUNT"))), "rev": _sf(r.get("REVENUE_AMOUNT"))}

    server_regions = ["东", "南", "西", "北"]
    result_list = []
    last_month_int = stat_date.year * 100 + stat_date.month
    cur = dt(stat_date.year, 1, 1)
    while cur.year * 100 + cur.month <= last_month_int:
        m_key = cur.strftime("%Y%m")
        cur_days = calendar.monthrange(cur.year, cur.month)[1]
        if cur.year * 100 + cur.month == last_month_int:
            cur_days = stat_date.day

        sf_info = sf_map.get(m_key, {})
        mv_info = mv_map.get(m_key, {})
        rev_info = rev_map.get(m_key, {})

        v_days = sf_info.get("days", 0)
        avg_vc = int(sf_info.get("vc", 0) / v_days) if v_days > 0 else 0
        avg_sf = int(sf_info.get("sf", 0) / v_days) if v_days > 0 else 0
        total_vc = avg_vc * cur_days
        total_sf = avg_sf * cur_days
        entry_rate = round(total_vc / total_sf * 100, 2) if total_sf > 0 else 0

        rev_amount = rev_info.get("rev", 0)
        rev_days = rev_info.get("days", 0)
        m_info = mv_map.get(m_key, {})
        m_days = m_info.get("days", 0)
        min_vc = int(m_info.get("min", 0) / m_days) if m_days > 0 else 0
        min_vc_total = min_vc * cur_days

        mv_vc = int(m_info.get("vc", 0) / m_days) if m_days > 0 else 0
        mv_total = mv_vc * cur_days
        avg_vehicle_amount = 0.0
        if mv_total > 0 and rev_days > 0:
            avg_vehicle_amount = round(rev_amount / rev_days / mv_vc, 2) if mv_vc > 0 else 0.0

        region_list = []
        for region in server_regions:
            rkey = (m_key, region)
            if rkey in sf_region_map:
                r_info = sf_region_map[rkey]
                r_days = r_info.get("days", 0)
                r_vc = int(r_info.get("vc", 0) / r_days * cur_days) if r_days > 0 else 0
                region_list.append({"name": region, "value": str(r_vc)})

        result_list.append({
            "Statistics_Year": cur.year, "Statistics_Month": cur.month,
            "Vehicle_Count": total_vc, "SectionFlow_Count": total_sf,
            "Entry_Rate": entry_rate, "RevenueAmount": rev_amount,
            "AvgVehicleAmount": avg_vehicle_amount, "MinVehicle_Count": min_vc_total,
            "RegionList": region_list,
            "SPRegionType_Id": None, "SPRegionType_Name": None,
            "Serverpart_ID": None, "Serverpart_Name": None,
            "ShopRevenueAmount": 0.0, "Stay_Times": None,
        })
        if cur.month == 12:
            cur = cur.replace(year=cur.year + 1, month=1)
        else:
            cur = cur.replace(month=cur.month + 1)

    return result_list


def get_province_month_analysis(db: DatabaseHelper, statistics_month, province_code,
                                sp_region_id, serverpart_id, sort_str, from_redis) -> list[dict]:
    """获取全省月度车流分析数据"""
    import calendar
    from datetime import datetime

    conditions = []
    params = []

    month_start = int(statistics_month + "01")
    month_end = int(statistics_month + "31")
    conditions.append('"A"."STATISTICS_DATE" >= ?')
    params.append(month_start)
    conditions.append('"A"."STATISTICS_DATE" <= ?')
    params.append(month_end)

    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', '"B"."SERVERPART_ID"'))
    elif sp_region_id:
        conditions.append(f'"B"."SPREGIONTYPE_ID" IN ({sp_region_id})')

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT
        "B"."SPREGIONTYPE_INDEX", "B"."SPREGIONTYPE_ID", "B"."SERVERPART_INDEX", "B"."SERVERPART_CODE",
        "B"."SPREGIONTYPE_NAME", "B"."SERVERPART_ID", "B"."SERVERPART_NAME",
        COUNT(DISTINCT "A"."STATISTICS_DATE") AS "DATE_COUNT",
        SUM("A"."SERVERPART_FLOW") AS "VEHICLE_COUNT",
        SUM("A"."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
    FROM "T_SECTIONFLOW" "A", "T_SERVERPART" "B"
    WHERE "A"."SERVERPART_ID" = "B"."SERVERPART_ID" AND {where_sql}
    GROUP BY "B"."SPREGIONTYPE_INDEX", "B"."SPREGIONTYPE_ID", "B"."SERVERPART_INDEX", "B"."SERVERPART_CODE",
        "B"."SPREGIONTYPE_NAME", "B"."SERVERPART_ID", "B"."SERVERPART_NAME"
    """
    rows = db.execute_query(sql, params if params else None)

    # 查营收数据
    rev_conditions = []
    rev_params = []
    rev_conditions.append('"A"."STATISTICS_DATE" >= ?')
    rev_params.append(month_start)
    rev_conditions.append('"A"."STATISTICS_DATE" <= ?')
    rev_params.append(month_end)
    if serverpart_id:
        rev_conditions.append(f'"B"."SERVERPART_ID" = {serverpart_id}')
    elif sp_region_id:
        rev_conditions.append(f'"B"."SPREGIONTYPE_ID" IN ({sp_region_id})')
    else:
        pid_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
        pid_rows = db.execute_query(pid_sql, {"pc": province_code or "340000"})
        if pid_rows:
            rev_conditions.append(f'"B"."PROVINCE_CODE" = {pid_rows[0]["FIELDENUM_ID"]}')
    rev_where = " AND ".join(rev_conditions)
    rev_sql = f"""SELECT "A"."SERVERPART_ID",
            COUNT(DISTINCT "A"."STATISTICS_DATE") AS "DATE_COUNT",
            SUM("A"."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
        FROM "T_REVENUEDAILY" "A", "T_SERVERPART" "B"
        WHERE "A"."SERVERPART_ID" = "B"."SERVERPART_ID"
            AND "A"."REVENUEDAILY_STATE" = 1 AND "B"."STATISTIC_TYPE" = 1000
            AND "B"."SERVERPART_CODE" NOT IN ('S000','S092','S093','S094')
            AND {rev_where}
        GROUP BY "A"."SERVERPART_ID" """
    rev_rows = db.execute_query(rev_sql, rev_params if rev_params else None) or []
    rev_map = {}
    for rr in rev_rows:
        sp_id = rr.get("SERVERPART_ID")
        rev_map[sp_id] = {"days": int(rr.get("DATE_COUNT") or 0), "rev": float(rr.get("REVENUE_AMOUNT") or 0)}

    if not rows:
        return []

    # 计算月度天数
    year = int(statistics_month[:4])
    month = int(statistics_month[4:6])
    now = datetime.now()
    import datetime as dt_mod
    if statistics_month == (now - dt_mod.timedelta(days=1)).strftime("%Y%m"):
        cur_days = (now - dt_mod.timedelta(days=1)).day
    elif statistics_month == now.strftime("%Y%m"):
        cur_days = (now.day - 1) if now.day > 1 else 1
    else:
        cur_days = calendar.monthrange(year, month)[1]

    result_list = []
    for r in rows:
        date_count = int(r.get("DATE_COUNT") or 0)
        vehicle_count = int(r.get("VEHICLE_COUNT") or 0)
        sectionflow_num = int(r.get("SECTIONFLOW_NUM") or 0)
        avg_vehicle = vehicle_count // date_count if date_count > 0 else 0
        avg_section = sectionflow_num // date_count if date_count > 0 else 0
        total_vehicle = avg_vehicle * cur_days
        total_section = avg_section * cur_days
        entry_rate = round(total_vehicle * 100 / total_section, 2) if total_section > 0 else 0

        sp_id = r.get("SERVERPART_ID")
        rev_info = rev_map.get(sp_id, {})
        revenue_amount = rev_info.get("rev", 0.0)
        rev_days = rev_info.get("days", 0)
        avg_vehicle_amount = 0.0
        if avg_vehicle > 0 and rev_days > 0:
            avg_vehicle_amount = round(revenue_amount / rev_days / avg_vehicle, 2)

        sp_region_id_val = r.get("SPREGIONTYPE_ID")
        result_list.append({
            "Statistics_Year": year, "Statistics_Month": month,
            "SPRegionType_Id": int(sp_region_id_val) if sp_region_id_val else None,
            "SPRegionType_Name": r.get("SPREGIONTYPE_NAME"),
            "Serverpart_ID": r.get("SERVERPART_ID"),
            "Serverpart_Name": r.get("SERVERPART_NAME"),
            "Vehicle_Count": total_vehicle, "MinVehicle_Count": None,
            "SectionFlow_Count": total_section, "Entry_Rate": entry_rate,
            "RevenueAmount": revenue_amount, "ShopRevenueAmount": 0.0,
            "AvgVehicleAmount": avg_vehicle_amount, "Stay_Times": None,
            "RegionList": [],
        })

    if sort_str:
        sort_field = sort_str.split(" ")[0]
        desc = sort_str.lower().endswith(" desc")
        if sort_field in ["SectionFlow_Count", "Vehicle_Count", "Entry_Rate"]:
            result_list.sort(key=lambda x: x.get(sort_field) or 0, reverse=desc)

    return result_list
