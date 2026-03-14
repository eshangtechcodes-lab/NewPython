# -*- coding: utf-8 -*-
"""
CommercialApi - 大数据车流预警 + 对比 Service
从 bigdata_router.py 中抽取: GetBayonetWarning, GetHolidayBayonetWarning,
GetBayonetGrowthAnalysis, GetBayonetCompare, GetHolidayCompare, GetBayonetOAAnalysis
每个函数独立、可单独迁移
"""
from typing import Optional
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition

from services.commercial.service_utils import (
    date_no_pad,
    safe_int as _si,
)



def _safe_dec(v):
    try: return float(v) if v is not None else 0.0
    except: return 0.0


# ===== 1. GetBayonetWarning =====
def get_bayonet_warning(db: DatabaseHelper, statistics_date, statistics_hour,
                         statistics_type, show_count) -> list[dict]:
    """获取车流预警数据"""
    from datetime import datetime as dt
    if not statistics_date:
        return None  # 调用方返回错误信息
    date_str = dt.strptime(statistics_date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in statistics_date else statistics_date
    sql = f"""SELECT * FROM "T_BAYONETWARNING"
        WHERE "BAYONETWARNING_STATE" = 1
        AND "STATISTICS_DATE" = {date_str}
        AND "STATISTICS_HOUR" = :hour"""
    rows = db.execute_query(sql, {"hour": statistics_hour}) or []

    result_list = []
    if statistics_type == 1:
        filtered = [r for r in rows if _si(r.get("VEHICLE_COUNT")) > 100
                    and 1.5 < _safe_dec(r.get("VEHICLE_RATE")) < 10]
        filtered.sort(key=lambda x: _si(x.get("VEHICLE_COUNT")), reverse=True)
        for r in filtered:
            result_list.append({
                "SERVERPART_ID": _si(r.get("SERVERPART_ID")),
                "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                "VEHICLE_COUNT": _si(r.get("VEHICLE_COUNT")),
                "MONTHVEHICLE_COUNT": _si(r.get("MONTHVEHICLE_COUNT")),
                "VEHICLE_RATE": round(_safe_dec(r.get("VEHICLE_RATE")) * 100, 2),
            })
    elif statistics_type == 2:
        filtered = [r for r in rows if 1 < _safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) < 10]
        filtered.sort(key=lambda x: _si(x.get("VEHICLE_TOTALCOUNT")), reverse=True)
        for r in filtered[:show_count]:
            result_list.append({
                "SERVERPART_ID": _si(r.get("SERVERPART_ID")),
                "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                "VEHICLE_COUNT": _si(r.get("VEHICLE_TOTALCOUNT")),
                "MONTHVEHICLE_COUNT": _si(r.get("MONTHVEHICLE_TOTALCOUNT")),
                "VEHICLE_RATE": round(_safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) * 100, 2),
            })
    return result_list


# ===== 2. GetHolidayBayonetWarning =====
def get_holiday_bayonet_warning(db: DatabaseHelper, statistics_date, statistics_hour,
                                 statistics_type, holiday_type, cur_year, compare_year,
                                 show_count) -> list[dict]:
    """获取节日车流预警数据"""
    from datetime import datetime as dt, timedelta
    if not statistics_date:
        return None
    date_str = dt.strptime(statistics_date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in statistics_date else statistics_date
    stat_date = dt.strptime(date_str, "%Y%m%d")

    # 查当日预警数据
    sql_today = f"""SELECT * FROM "T_BAYONETWARNING"
        WHERE "BAYONETWARNING_STATE" = 1
        AND "STATISTICS_DATE" = {date_str} AND "STATISTICS_HOUR" = :hour"""
    dt_warning = db.execute_query(sql_today, {"hour": statistics_hour}) or []

    # 确定对比日期
    compare_date_str = None
    if statistics_type in (3, 4):
        try:
            holiday_names = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
            h_name = holiday_names.get(int(holiday_type), "")
            if h_name:
                cur_desc = f"{cur_year}年{h_name}"
                cmp_desc = f"{compare_year}年{h_name}"
                h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
                    WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
                def to_dtx(v):
                    if isinstance(v, dt): return v
                    if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
                    return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v
                cur_dates = [to_dtx(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
                cmp_dates = [to_dtx(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
                if cur_dates and cmp_dates:
                    c_s = min(cur_dates)
                    cm_s = min(cmp_dates)
                    days_offset = (stat_date - c_s).days
                    compare_date = cm_s + timedelta(days=days_offset)
                    compare_date_str = compare_date.strftime("%Y%m%d")
        except Exception:
            pass
    elif statistics_type in (5, 6):
        compare_date_str = (stat_date - timedelta(days=1)).strftime("%Y%m%d")

    if not compare_date_str:
        return []

    sql_compare = f"""SELECT * FROM "T_BAYONETWARNING"
        WHERE "BAYONETWARNING_STATE" = 1
        AND "STATISTICS_DATE" = {compare_date_str} AND "STATISTICS_HOUR" = :hour"""
    dt_compare = db.execute_query(sql_compare, {"hour": statistics_hour}) or []
    if not dt_compare:
        return []

    cmp_map = {}
    for c in dt_compare:
        key = (_si(c.get("SERVERPART_ID")), c.get("SERVERPART_REGION", ""))
        cmp_map[key] = c

    for w in dt_warning:
        key = (_si(w.get("SERVERPART_ID")), w.get("SERVERPART_REGION", ""))
        if key in cmp_map:
            c = cmp_map[key]
            w["MONTHVEHICLE_COUNT"] = c.get("VEHICLE_COUNT")
            cvc = _safe_dec(c.get("VEHICLE_COUNT"))
            w["VEHICLE_RATE"] = round(_safe_dec(w.get("VEHICLE_COUNT")) / cvc, 2) if cvc > 0 else 0
            if _safe_dec(w.get("VEHICLE_RATE")) > 10: w["VEHICLE_RATE"] = 0
            w["MONTHVEHICLE_TOTALCOUNT"] = c.get("VEHICLE_TOTALCOUNT")
            ctc = _safe_dec(c.get("VEHICLE_TOTALCOUNT"))
            w["MONTHVEHICLE_TOTALRATE"] = round(_safe_dec(w.get("VEHICLE_TOTALCOUNT")) / ctc, 2) if ctc > 0 else 0
            if _safe_dec(w.get("MONTHVEHICLE_TOTALRATE")) > 10: w["MONTHVEHICLE_TOTALRATE"] = 0
        else:
            w["VEHICLE_RATE"] = 0
            w["MONTHVEHICLE_TOTALRATE"] = 0

    result_list = []
    if statistics_type in (3, 5):
        filtered = [r for r in dt_warning if _si(r.get("VEHICLE_COUNT")) > 100
                    and _safe_dec(r.get("VEHICLE_RATE")) > 1.5]
        filtered.sort(key=lambda x: _si(x.get("VEHICLE_COUNT")), reverse=True)
        for r in filtered:
            result_list.append({
                "SERVERPART_ID": _si(r.get("SERVERPART_ID")),
                "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                "VEHICLE_COUNT": _si(r.get("VEHICLE_COUNT")),
                "MONTHVEHICLE_COUNT": _si(r.get("MONTHVEHICLE_COUNT")),
                "VEHICLE_RATE": round(_safe_dec(r.get("VEHICLE_RATE")) * 100, 2),
            })
    elif statistics_type in (4, 6):
        filtered = [r for r in dt_warning if _safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) > 1]
        filtered.sort(key=lambda x: _si(x.get("VEHICLE_TOTALCOUNT")), reverse=True)
        for r in filtered[:show_count]:
            result_list.append({
                "SERVERPART_ID": _si(r.get("SERVERPART_ID")),
                "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                "VEHICLE_COUNT": _si(r.get("VEHICLE_TOTALCOUNT")),
                "MONTHVEHICLE_COUNT": _si(r.get("MONTHVEHICLE_TOTALCOUNT")),
                "VEHICLE_RATE": round(_safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) * 100, 2),
            })
    return result_list


# ===== 3. GetBayonetGrowthAnalysis =====
def get_bayonet_growth_analysis(db: DatabaseHelper, push_province_code, statistics_start_date,
                                 statistics_end_date, sp_region_type_id, serverpart_id,
                                 serverpart_region, show_growth_rate) -> dict:
    """获取当日服务区车流量分析"""
    from datetime import datetime as dt, timedelta
    from collections import defaultdict

    if not statistics_start_date or not statistics_end_date:
        return {"EntryList": [], "GrowthList": None, "sumEntryCount": 0}

    s_date = dt.strptime(statistics_start_date, "%Y-%m-%d") if "-" in statistics_start_date else dt.strptime(statistics_start_date, "%Y%m%d")
    e_date = dt.strptime(statistics_end_date, "%Y-%m-%d") if "-" in statistics_end_date else dt.strptime(statistics_end_date, "%Y%m%d")

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    if serverpart_region:
        regions_in = ",".join(f"'{r}'" for r in serverpart_region.split(","))
        where_sql += f' AND A."SERVERPART_REGION" IN ({regions_in})'

    sql1 = f"""SELECT B."SERVERPART_ID",B."SERVERPART_NAME",A."SERVERPART_REGION",
            B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX",
            SUM(A."SERVERPART_FLOW") AS "VEHICLE_COUNT"
        FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SERVERPART_FLOW" > 0
            AND A."STATISTICS_DATE" >= {s_date.strftime('%Y%m%d')}
            AND A."STATISTICS_DATE" <= {e_date.strftime('%Y%m%d')}{where_sql}
        GROUP BY B."SERVERPART_ID",B."SERVERPART_NAME",A."SERVERPART_REGION",B."SPREGIONTYPE_ID",B."SPREGIONTYPE_NAME",B."SPREGIONTYPE_INDEX" """
    rows = db.execute_query(sql1) or []

    if not rows:
        return {"EntryList": [], "GrowthList": None, "sumEntryCount": 0}

    yes_map = {}
    if show_growth_rate:
        yes_s = (s_date - timedelta(days=1)).strftime("%Y%m01")
        yes_e = (e_date - timedelta(days=1)).strftime("%Y%m%d")
        sql2 = f"""SELECT B."SERVERPART_ID",A."SERVERPART_REGION",
                SUM(A."SERVERPART_FLOW") AS "VEHICLE_COUNT",
                COUNT(DISTINCT A."STATISTICS_DATE") AS "COUNT_DATE"
            FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SERVERPART_FLOW" > 0
                AND A."STATISTICS_DATE" >= {yes_s}
                AND A."STATISTICS_DATE" <= {yes_e}{where_sql}
            GROUP BY B."SERVERPART_ID",A."SERVERPART_REGION" """
        yes_rows = db.execute_query(sql2) or []
        for r in yes_rows:
            key = (_si(r.get("SERVERPART_ID")), r.get("SERVERPART_REGION", ""))
            yes_map[key] = r

    entry_list = []
    for r in rows:
        sp_id = _si(r.get("SERVERPART_ID"))
        region = r.get("SERVERPART_REGION", "")
        vc = _safe_dec(r.get("VEHICLE_COUNT"))
        growth = 0.0
        if show_growth_rate:
            yr = yes_map.get((sp_id, region))
            if yr:
                cd = _safe_dec(yr.get("COUNT_DATE"))
                if cd > 0:
                    avg_vc = round(_safe_dec(yr.get("VEHICLE_COUNT")) / cd, 0)
                    if vc > 100 and avg_vc > 100:
                        growth = round(vc / avg_vc * 100, 2)
        entry_list.append({
            "Serverpart_ID": sp_id, "Serverpart_Name": r.get("SERVERPART_NAME", ""),
            "Serverpart_Region": region + "区",
            "SPRegionType_Id": r.get("SPREGIONTYPE_ID"), "SPRegionType_Name": r.get("SPREGIONTYPE_NAME", ""),
            "SPRegionType_Index": r.get("SPREGIONTYPE_INDEX"), "Serverpart_Index": None,
            "Vehicle_Count": vc, "Entry_GrowthRate": growth if growth != 0.0 else None,
            "Entry_Rate": None,
            "LargeVehicleEntry_GrowthRate": None, "LargeVehicleEntry_Rate": None, "LargeVehicle_Count": None,
            "MediumVehicleEntry_GrowthRate": None, "MediumVehicleEntry_Rate": None, "MediumVehicle_Count": None,
            "MinVehicleEntry_GrowthRate": None, "MinVehicleEntry_Rate": None, "MinVehicle_Count": None,
            "SectionFlow_Count": None,
        })

    sum_entry = sum(e["Vehicle_Count"] for e in entry_list)
    growth_list = sorted(entry_list, key=lambda x: (-(x["Entry_GrowthRate"] or 0), -x["Vehicle_Count"])) if show_growth_rate else None

    sp_agg = defaultdict(lambda: {"name": "", "vc": 0.0, "rid": None, "rname": "", "rindex": None})
    for e in entry_list:
        sp_agg[e["Serverpart_ID"]]["name"] = e["Serverpart_Name"]
        sp_agg[e["Serverpart_ID"]]["vc"] += e["Vehicle_Count"]

    merged_list = sorted([
        {"Serverpart_ID": sid, "Serverpart_Name": v["name"], "Serverpart_Region": "",
         "Serverpart_Index": None, "SPRegionType_Id": None, "SPRegionType_Name": None, "SPRegionType_Index": None,
         "Vehicle_Count": v["vc"], "Entry_GrowthRate": None, "Entry_Rate": None,
         "LargeVehicleEntry_GrowthRate": None, "LargeVehicleEntry_Rate": None, "LargeVehicle_Count": None,
         "MediumVehicleEntry_GrowthRate": None, "MediumVehicleEntry_Rate": None, "MediumVehicle_Count": None,
         "MinVehicleEntry_GrowthRate": None, "MinVehicleEntry_Rate": None, "MinVehicle_Count": None, "SectionFlow_Count": None}
        for sid, v in sp_agg.items()
    ], key=lambda x: -x["Vehicle_Count"])

    return {"EntryList": merged_list, "GrowthList": growth_list, "sumEntryCount": sum_entry}


# ===== 4. GetBayonetCompare =====
def get_bayonet_compare(db: DatabaseHelper, push_province_code, statistics_start_date, statistics_end_date,
                         compare_start_date, compare_end_date, sp_region_type_id,
                         serverpart_id, serverpart_region) -> Optional[dict]:
    """获取服务区车流量同比分析"""
    from datetime import datetime as dt, timedelta

    if push_province_code != "340000":
        return None
    if not statistics_start_date or not statistics_end_date:
        return None

    def parse_d(s):
        return dt.strptime(s, "%Y-%m-%d") if "-" in s else dt.strptime(s, "%Y%m%d")

    s_date = parse_d(statistics_start_date)
    e_date = parse_d(statistics_end_date)
    cs_date = parse_d(compare_start_date) if compare_start_date else s_date.replace(year=s_date.year - 1)
    ce_date = parse_d(compare_end_date) if compare_end_date else e_date.replace(year=e_date.year - 1)

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    if serverpart_region:
        regions_in = ",".join(f"'{r}'" for r in serverpart_region.split(","))
        where_sql += f' AND A."SERVERPART_REGION" IN ({regions_in})'

    sql_base = """SELECT A."STATISTICS_DATE",COUNT(DISTINCT A."SERVERPART_ID") AS "SERVERPART_COUNT",
            SUM(A."SERVERPART_FLOW") AS "VEHICLE_COUNT"
        FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SERVERPART_FLOW" > 0
            AND A."STATISTICS_DATE" >= {s} AND A."STATISTICS_DATE" <= {e}{w}
        GROUP BY A."STATISTICS_DATE" """

    cur_rows = db.execute_query(sql_base.format(s=s_date.strftime("%Y%m%d"), e=e_date.strftime("%Y%m%d"), w=where_sql)) or []
    cmp_rows = db.execute_query(sql_base.format(s=cs_date.strftime("%Y%m%d"), e=ce_date.strftime("%Y%m%d"), w=where_sql)) or []

    def build_map(rows):
        m = {}
        for r in rows:
            d = str(_si(r.get("STATISTICS_DATE")))
            sc = _si(r.get("SERVERPART_COUNT"))
            vc = _si(r.get("VEHICLE_COUNT"))
            m[d] = vc // sc if sc > 0 else 0
        return m

    cur_map = build_map(cur_rows)
    cmp_map = build_map(cmp_rows)

    cur_days = (e_date - s_date).days + 1
    cmp_days = (ce_date - cs_date).days + 1
    max_days = max(cur_days, cmp_days)

    cur_list, cmp_list = [], []
    for i in range(max_days):
        cd = s_date + timedelta(days=i)
        ld = cs_date + timedelta(days=i)
        cur_list.append({"name": date_no_pad(cd), "value": str(cur_map.get(cd.strftime("%Y%m%d"), 0)), "data": None, "key": None})
        cmp_list.append({"name": date_no_pad(ld), "value": str(cmp_map.get(ld.strftime("%Y%m%d"), 0)), "data": None, "key": None})

    return {
        "curHoliday": None, "curHolidayDays": 0, "curList": cur_list,
        "compareHoliday": None, "compareHolidayDays": 0, "compareList": cmp_list,
    }


# ===== 5. GetHolidayCompare (BigData) =====
def get_holiday_compare(db: DatabaseHelper, push_province_code, holiday_type, cur_year, compare_year,
                          sp_region_type_id, serverpart_id, serverpart_region) -> Optional[dict]:
    """获取节日服务区平均入区流量对比数据"""
    from datetime import datetime as dt, timedelta

    if not cur_year or not compare_year:
        return None

    holiday_names = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
    h_name = holiday_names.get(int(holiday_type), "")
    if not h_name:
        return None

    cur_desc = f"{cur_year}年{h_name}"
    cmp_desc = f"{compare_year}年{h_name}"
    h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
        WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
    if not h_rows:
        return None

    def to_dt2(v):
        if isinstance(v, dt): return v
        if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
        return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

    cur_dates = [to_dt2(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
    cmp_dates = [to_dt2(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
    if not cur_dates or not cmp_dates:
        return None

    s_date = min(cur_dates); e_date = max(cur_dates)
    cs_date = min(cmp_dates); ce_date = max(cmp_dates)
    cur_holiday = f"{s_date.strftime('%m.%d')}-{e_date.strftime('%m.%d')}"
    cmp_holiday = f"{cs_date.strftime('%m.%d')}-{ce_date.strftime('%m.%d')}"
    cur_days = (e_date - s_date).days + 1
    cmp_days = (ce_date - cs_date).days + 1

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    if serverpart_region:
        regions_in = ",".join(f"'{r}'" for r in serverpart_region.split(","))
        where_sql += f' AND A."SERVERPART_REGION" IN ({regions_in})'

    sql_base = """SELECT A."STATISTICS_DATE",COUNT(DISTINCT A."SERVERPART_ID") AS "SERVERPART_COUNT",
            SUM(A."SERVERPART_FLOW") AS "VEHICLE_COUNT"
        FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SERVERPART_FLOW" > 0
            AND A."STATISTICS_DATE" >= {s} AND A."STATISTICS_DATE" <= {e}{w}
        GROUP BY A."STATISTICS_DATE" """

    cur_rows = db.execute_query(sql_base.format(s=s_date.strftime("%Y%m%d"), e=e_date.strftime("%Y%m%d"), w=where_sql)) or []
    cmp_rows = db.execute_query(sql_base.format(s=cs_date.strftime("%Y%m%d"), e=ce_date.strftime("%Y%m%d"), w=where_sql)) or []

    def build_map(rows):
        m = {}
        for r in rows:
            d = str(_si(r.get("STATISTICS_DATE")))
            sc = _si(r.get("SERVERPART_COUNT"))
            vc = _si(r.get("VEHICLE_COUNT"))
            m[d] = vc // sc if sc > 0 else 0
        return m

    cur_map = build_map(cur_rows)
    cmp_map = build_map(cmp_rows)

    max_d = max(cur_days, cmp_days)
    cur_list, cmp_list = [], []
    for i in range(max_d):
        cd = s_date + timedelta(days=i); ld = cs_date + timedelta(days=i)
        cur_list.append({"name": date_no_pad(cd), "value": str(cur_map.get(cd.strftime("%Y%m%d"), 0)), "data": None, "key": None})
        cmp_list.append({"name": date_no_pad(ld), "value": str(cmp_map.get(ld.strftime("%Y%m%d"), 0)), "data": None, "key": None})

    return {
        "curHoliday": cur_holiday, "curHolidayDays": cur_days, "curList": cur_list,
        "compareHoliday": cmp_holiday, "compareHolidayDays": cmp_days, "compareList": cmp_list,
    }


# ===== 6. GetBayonetOAAnalysis =====
def get_bayonet_oa_analysis(db: DatabaseHelper, holiday_type, start_month, end_month,
                             vehicle_type) -> tuple[list[dict], list]:
    """获取日均车流归属地数据分析（月度版）"""
    from collections import defaultdict

    # 1. 查断面流量月度汇总
    where_sql = ""
    if holiday_type == 1:
        where_sql += ' AND B."HOLIDAY_TYPE" IN (2,4,6,8)'
    elif holiday_type == 2:
        where_sql += ' AND B."HOLIDAY_TYPE" NOT IN (2,4,6,8)'
    if start_month: where_sql += f' AND B."STATISTICS_MONTH" >= {start_month}'
    if end_month: where_sql += f' AND B."STATISTICS_MONTH" <= {end_month}'

    sf_sql = f"""SELECT A."SERVERPART_ID",A."SERVERPART_NAME",B."SERVERPART_REGION",
            SUM(B."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
            SUM(B."SERVERPART_FLOW") AS "SERVERPART_FLOW",
            SUM(B."STATISTICS_DAYS") AS "STATISTICS_DAYS",
            SUM(B."MINVEHICLE_COUNT") AS "MINVEHICLE_COUNT",
            SUM(B."MEDIUMVEHICLE_COUNT") AS "MEDIUMVEHICLE_COUNT",
            SUM(B."LARGEVEHICLE_COUNT") AS "LARGEVEHICLE_COUNT",
            MIN("STATISTICS_MONTH") AS "START_MONTH", MAX("STATISTICS_MONTH") AS "END_MONTH"
        FROM "T_SERVERPART" A, "T_SECTIONFLOWMONTH" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND B."SECTIONFLOWMONTH_STATE" = 1{where_sql}
        GROUP BY A."SERVERPART_ID",A."SERVERPART_NAME",B."SERVERPART_REGION" """
    dt_sf = db.execute_query(sf_sql) or []

    # 2. 查归属地省份数据
    oa_where = ""
    if holiday_type == 1: oa_where = ' AND "STATISTICS_MONTH" = 202402'
    elif holiday_type == 2: oa_where = ' AND "STATISTICS_MONTH" = 202403'
    else: oa_where = ' AND "STATISTICS_MONTH" = 202401'
    oa_where += ' AND "SERVERPART_ID" > 0'
    if vehicle_type:
        oa_where += f" AND \"VEHICLE_TYPE\" = '{vehicle_type}'"
    else:
        oa_where += ' AND "VEHICLE_TYPE" IS NULL'

    oa_sql = f"""SELECT "SERVERPART_ID","PROVINCE_NAME","VEHICLE_COUNT","AVGVEHICLE_COUNT","RANK_NUM"
        FROM "T_BAYONETPROVINCEMONTH_AH" WHERE "SERVERPART_REGION" IS NULL{oa_where}"""
    dt_oa = db.execute_query(oa_sql) or []

    # 3. 查出区车流
    out_where = ""
    if holiday_type == 1: out_where = ' AND "STATISTICS_DATE" BETWEEN 20240201 AND 20240228'
    elif holiday_type == 2: out_where = ' AND "STATISTICS_DATE" BETWEEN 20240301 AND 20240331'
    else: out_where = ' AND "STATISTICS_DATE" BETWEEN 20240101 AND 20240131'
    out_where += ' AND "SERVERPART_ID" > 0'

    out_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION",
            SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT",
            COUNT(DISTINCT "STATISTICS_DATE") AS "STATISTICS_DAYS"
        FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0{out_where}
        GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
    dt_out = db.execute_query(out_sql) or []

    # 构建索引
    sf_map = defaultdict(list)
    for r in dt_sf: sf_map[_si(r.get("SERVERPART_ID"))].append(r)
    oa_map = defaultdict(list)
    for r in dt_oa: oa_map[_si(r.get("SERVERPART_ID"))].append(r)
    out_map = {}
    for r in dt_out: out_map[(_si(r.get("SERVERPART_ID")), r.get("SERVERPART_REGION", ""))] = r

    sp_set = {}
    for r in dt_sf:
        sp_id = _si(r.get("SERVERPART_ID"))
        if sp_id not in sp_set: sp_set[sp_id] = r.get("SERVERPART_NAME", "")

    regions = ["东", "南", "西", "北"]
    result_list = []
    start_month_val, end_month_val = None, None

    for sp_id, sp_name in sp_set.items():
        vc_total = 0; mini_vc = 0; medium_vc = 0; large_vc = 0; out_vc_total = 0
        for region in regions:
            sf_rows = [r for r in sf_map[sp_id] if r.get("SERVERPART_REGION") == region]
            if sf_rows:
                s = sf_rows[0]; days = _si(s.get("STATISTICS_DAYS"))
                if days > 0:
                    vc_total += _si(s.get("SERVERPART_FLOW")) // days
                    mini_vc += _si(s.get("MINVEHICLE_COUNT")) // days
                    medium_vc += _si(s.get("MEDIUMVEHICLE_COUNT")) // days
                    large_vc += _si(s.get("LARGEVEHICLE_COUNT")) // days
                sm = s.get("START_MONTH"); em = s.get("END_MONTH")
                if sm: start_month_val = min(start_month_val, _si(sm)) if start_month_val else _si(sm)
                if em: end_month_val = max(end_month_val, _si(em)) if end_month_val else _si(em)
            out_row = out_map.get((sp_id, region))
            if out_row:
                od = _si(out_row.get("STATISTICS_DAYS"))
                if od > 0: out_vc_total += _si(out_row.get("VEHICLE_COUNT")) // od

        oa_rows = sorted(oa_map.get(sp_id, []), key=lambda x: _si(x.get("RANK_NUM")))
        total_avg_oa = sum(_si(r.get("AVGVEHICLE_COUNT")) for r in oa_rows)
        if total_avg_oa > out_vc_total: out_vc_total = total_avg_oa

        province_list, province_names = [], []
        for r in oa_rows:
            pname = r.get("PROVINCE_NAME", "")
            province_names.append(pname)
            avg_c = _si(r.get("AVGVEHICLE_COUNT"))
            pv = (avg_c * vc_total // out_vc_total) if out_vc_total > 0 else 0
            province_list.append({"name": pname, "value": str(pv)})

        display_vc = vc_total
        if vehicle_type == "小型车": display_vc = mini_vc
        elif vehicle_type == "中型车": display_vc = medium_vc
        elif vehicle_type == "大型车": display_vc = large_vc

        result_list.append({
            "Serverpart_ID": sp_id, "Serverpart_Name": sp_name,
            "Vehicle_Count": display_vc, "OwnerProvince": province_names, "OwnerProvinceList": province_list,
        })

    other_data = [str(start_month_val) if start_month_val else "", str(end_month_val) if end_month_val else ""]
    return result_list, other_data
