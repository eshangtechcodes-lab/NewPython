# -*- coding: utf-8 -*-
"""
CommercialApi - 大数据日度分析 + 散点图 + 树形 Service
从 bigdata_router.py 中抽取: GetDateAnalysis, GetCurBusyRank, GetRevenueTrendChart,
GetEnergyRevenueInfo, GetBayonetOwnerAHTreeList, GetProvinceVehicleTreeList, GetProvinceVehicleDetail
每个函数独立、可单独迁移

注意: GetCurBusyRank/GetRevenueTrendChart/GetEnergyRevenueInfo 使用 AES 加密入参,
      需在 Router 层解密后传入; 树形路由逻辑较复杂, 整体迁移到此处
"""
from typing import Optional
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


def _safe_int(v):
    try: return int(float(v)) if v is not None else 0
    except: return 0

def _safe_f(v):
    try: return float(v) if v is not None else 0.0
    except: return 0.0


# ===== 1. GetDateAnalysis =====
def get_date_analysis(db: DatabaseHelper, start_date, end_date, serverpart_id) -> tuple[list[dict], list]:
    """获取日度车流分析数据，返回 (result_list, other_data_summary)"""
    from datetime import datetime, timedelta

    start_dt = datetime.strptime(start_date.split(" ")[0], "%Y-%m-%d")
    end_dt = datetime.strptime(end_date.split(" ")[0], "%Y-%m-%d")
    start_str = start_dt.strftime("%Y%m%d")
    end_str = end_dt.strftime("%Y%m%d")
    ly_start_dt = start_dt.replace(year=start_dt.year - 1)
    ly_end_dt = end_dt.replace(year=end_dt.year - 1)
    ly_start_str = ly_start_dt.strftime("%Y%m%d")
    ly_end_str = ly_end_dt.strftime("%Y%m%d")

    south_east = ['东', '南']
    north_west = ['西', '北']

    # 查断面流量
    sql = """SELECT "STATISTICS_DATE", "SERVERPART_REGION",
        SUM(COALESCE("SERVERPART_FLOW_ANALOG", 0)) AS "SERVERPART_FLOW_ANALOG",
        SUM("SERVERPART_FLOW" + COALESCE("SERVERPART_FLOW_ANALOG", 0)) AS "SERVERPART_FLOW",
        SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
    FROM "T_SECTIONFLOW"
    WHERE "SERVERPART_ID" = ? AND "STATISTICS_DATE" >= ? AND "STATISTICS_DATE" <= ?
    GROUP BY "STATISTICS_DATE", "SERVERPART_REGION"
    UNION ALL
    SELECT "STATISTICS_DATE", "SERVERPART_REGION",
        SUM(COALESCE("SERVERPART_FLOW_ANALOG", 0)) AS "SERVERPART_FLOW_ANALOG",
        SUM("SERVERPART_FLOW" + COALESCE("SERVERPART_FLOW_ANALOG", 0)) AS "SERVERPART_FLOW",
        SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
    FROM "T_SECTIONFLOW"
    WHERE "SERVERPART_ID" = ? AND "STATISTICS_DATE" >= ? AND "STATISTICS_DATE" <= ?
    GROUP BY "STATISTICS_DATE", "SERVERPART_REGION"
    """
    rows = db.execute_query(sql, [
        serverpart_id, int(start_str), int(end_str),
        serverpart_id, int(ly_start_str), int(ly_end_str)
    ])
    flow_map = {}
    for r in (rows or []):
        key = (r.get("STATISTICS_DATE"), r.get("SERVERPART_REGION"))
        flow_map[key] = r

    # 查营收
    rev_sql = f"""SELECT "STATISTICS_DATE", SUM("REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM("REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",
            SUM("REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B"
        FROM "T_REVENUEDAILY"
        WHERE "REVENUEDAILY_STATE" = 1 AND "SERVERPART_ID" = {serverpart_id}
            AND "STATISTICS_DATE" >= {start_str} AND "STATISTICS_DATE" <= {end_str}
        GROUP BY "STATISTICS_DATE"
        UNION ALL
        SELECT "STATISTICS_DATE", SUM("REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM("REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",
            SUM("REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B"
        FROM "T_REVENUEDAILY"
        WHERE "REVENUEDAILY_STATE" = 1 AND "SERVERPART_ID" = {serverpart_id}
            AND "STATISTICS_DATE" >= {ly_start_str} AND "STATISTICS_DATE" <= {ly_end_str}
        GROUP BY "STATISTICS_DATE" """
    rev_rows = db.execute_query(rev_sql) or []
    rev_map = {}
    for r in rev_rows:
        d = r.get("STATISTICS_DATE")
        rev_map[d] = {"rev": float(r.get("REVENUE_AMOUNT", 0) or 0),
                      "rev_a": float(r.get("REVENUE_AMOUNT_A", 0) or 0),
                      "rev_b": float(r.get("REVENUE_AMOUNT_B", 0) or 0)}

    # 遍历日期
    result_list = []
    cur_date = start_dt
    while cur_date <= end_dt:
        date_num = int(cur_date.strftime("%Y%m%d"))
        ly_date_num = int(cur_date.replace(year=cur_date.year - 1).strftime("%Y%m%d"))
        cur_rev = rev_map.get(date_num, {})
        ly_rev = rev_map.get(ly_date_num, {})

        model = {
            "STATISTICS_DATE": cur_date.strftime("%m-%d"),
            "ThisYearTotalSECTIONFLOW_NUM": 0.0, "ThisYearTotalSERVERPART_FLOW": 0.0,
            "LastYearTotalSECTIONFLOW_NUM": 0.0, "LastYearTotalSERVERPART_FLOW": 0.0,
            "ThisYearSouthEastSECTIONFLOW_NUM": 0.0, "ThisYearSouthEastSERVERPART_FLOW": 0.0,
            "ThisYearNorthWestSECTIONFLOW_NUM": 0.0, "ThisYearNorthWestSERVERPART_FLOW": 0.0,
            "LastYearSouthEastSECTIONFLOW_NUM": 0.0, "LastYearSouthEastSERVERPART_FLOW": 0.0,
            "LastYearNorthWestSECTIONFLOW_NUM": 0.0, "LastYearNorthWestSERVERPART_FLOW": 0.0,
            "ThisYearTotalANALOG": 0.0, "ThisYearSouthEastANALOG": 0.0, "ThisYearNorthWestANALOG": 0.0,
            "LastYearTotalANALOG": 0.0, "LastYearSouthEastANALOG": 0.0, "LastYearNorthWestANALOG": 0.0,
            "CurRevenueAmount": cur_rev.get("rev", 0.0),
            "CurRevenueAmount_A": cur_rev.get("rev_a", 0.0), "CurRevenueAmount_B": cur_rev.get("rev_b", 0.0),
            "LyRevenueAmount": ly_rev.get("rev", 0.0),
            "LyRevenueAmount_A": ly_rev.get("rev_a", 0.0), "LyRevenueAmount_B": ly_rev.get("rev_b", 0.0),
        }

        for region in ['东', '南', '西', '北']:
            r = flow_map.get((date_num, region))
            if r:
                sf = float(r.get("SECTIONFLOW_NUM") or 0)
                sp = float(r.get("SERVERPART_FLOW") or 0)
                analog = float(r.get("SERVERPART_FLOW_ANALOG") or 0)
                model["ThisYearTotalSECTIONFLOW_NUM"] += sf
                model["ThisYearTotalSERVERPART_FLOW"] += sp
                model["ThisYearTotalANALOG"] += analog
                if region in south_east:
                    model["ThisYearSouthEastSECTIONFLOW_NUM"] += sf
                    model["ThisYearSouthEastSERVERPART_FLOW"] += sp
                    model["ThisYearSouthEastANALOG"] += analog
                else:
                    model["ThisYearNorthWestSECTIONFLOW_NUM"] += sf
                    model["ThisYearNorthWestSERVERPART_FLOW"] += sp
                    model["ThisYearNorthWestANALOG"] += analog
            r_ly = flow_map.get((ly_date_num, region))
            if r_ly:
                sf = float(r_ly.get("SECTIONFLOW_NUM") or 0)
                sp = float(r_ly.get("SERVERPART_FLOW") or 0)
                analog = float(r_ly.get("SERVERPART_FLOW_ANALOG") or 0)
                model["LastYearTotalSECTIONFLOW_NUM"] += sf
                model["LastYearTotalSERVERPART_FLOW"] += sp
                model["LastYearTotalANALOG"] += analog
                if region in south_east:
                    model["LastYearSouthEastSECTIONFLOW_NUM"] += sf
                    model["LastYearSouthEastSERVERPART_FLOW"] += sp
                    model["LastYearSouthEastANALOG"] += analog
                else:
                    model["LastYearNorthWestSECTIONFLOW_NUM"] += sf
                    model["LastYearNorthWestSERVERPART_FLOW"] += sp
                    model["LastYearNorthWestANALOG"] += analog

        # 差值
        model["TotalDiffSECTIONFLOW_NUM"] = model["ThisYearTotalSECTIONFLOW_NUM"] - model["LastYearTotalSECTIONFLOW_NUM"]
        model["TotalDiffSERVERPART_FLOW"] = model["ThisYearTotalSERVERPART_FLOW"] - model["LastYearTotalSERVERPART_FLOW"]
        model["SouthEastDiffSECTIONFLOW_NUM"] = model["ThisYearSouthEastSECTIONFLOW_NUM"] - model["LastYearSouthEastSECTIONFLOW_NUM"]
        model["SouthEastDiffSERVERPART_FLOW"] = model["ThisYearSouthEastSERVERPART_FLOW"] - model["LastYearSouthEastSERVERPART_FLOW"]
        model["NorthWestDiffSECTIONFLOW_NUM"] = model["ThisYearNorthWestSECTIONFLOW_NUM"] - model["LastYearNorthWestSECTIONFLOW_NUM"]
        model["NorthWestDiffSERVERPART_FLOW"] = model["ThisYearNorthWestSERVERPART_FLOW"] - model["LastYearNorthWestSERVERPART_FLOW"]

        result_list.append(model)
        cur_date += timedelta(days=1)

    # OtherData 汇总
    sum_keys = ["ThisYearTotalSECTIONFLOW_NUM", "ThisYearTotalSERVERPART_FLOW",
                "LastYearTotalSECTIONFLOW_NUM", "LastYearTotalSERVERPART_FLOW",
                "ThisYearSouthEastSECTIONFLOW_NUM", "ThisYearSouthEastSERVERPART_FLOW",
                "ThisYearNorthWestSECTIONFLOW_NUM", "ThisYearNorthWestSERVERPART_FLOW",
                "LastYearSouthEastSECTIONFLOW_NUM", "LastYearSouthEastSERVERPART_FLOW",
                "LastYearNorthWestSECTIONFLOW_NUM", "LastYearNorthWestSERVERPART_FLOW",
                "ThisYearTotalANALOG", "ThisYearSouthEastANALOG", "ThisYearNorthWestANALOG",
                "LastYearTotalANALOG", "LastYearSouthEastANALOG", "LastYearNorthWestANALOG",
                "CurRevenueAmount", "CurRevenueAmount_A", "CurRevenueAmount_B",
                "LyRevenueAmount", "LyRevenueAmount_A", "LyRevenueAmount_B",
                "TotalDiffSECTIONFLOW_NUM", "TotalDiffSERVERPART_FLOW",
                "SouthEastDiffSECTIONFLOW_NUM", "SouthEastDiffSERVERPART_FLOW",
                "NorthWestDiffSECTIONFLOW_NUM", "NorthWestDiffSERVERPART_FLOW"]
    analog_keys = {"ThisYearTotalANALOG", "ThisYearSouthEastANALOG", "ThisYearNorthWestANALOG",
                   "LastYearTotalANALOG", "LastYearSouthEastANALOG", "LastYearNorthWestANALOG"}
    _oth = {"STATISTICS_DATE": None}
    for k in sum_keys:
        if k in analog_keys:
            _oth[k] = None
        else:
            _oth[k] = round(sum(float(m.get(k, 0) or 0) for m in result_list), 2)
    return result_list, [_oth]


# ===== 2. GetEnergyRevenueInfo =====
def get_energy_revenue_info(db: DatabaseHelper, data_type: int, statistics_date: str,
                             show_wy: bool, show_large_unit: bool) -> dict:
    """获取当日全业态营收数据"""
    from datetime import datetime as dt, timedelta

    cur_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    cur_date_str = cur_date.strftime("%Y-%m-%d")
    next_date_str = (cur_date + timedelta(days=1)).strftime("%Y-%m-%d")

    total_amount = 0.0
    total_count = 0.0
    name = ""

    if data_type == 2000:  # 油品
        name = "油品"
        sql = f"""SELECT SUM(CASE WHEN A."PAY_DIRECTION" = 2 THEN -1 ELSE 1 END * B."MONEY")
            FROM "T_GASORDERINFO" A, "T_GASORDERDETAIL" B
            WHERE A."GASORDERINFO_ID" = B."GASORDERINFO_ID" AND B."GOODS_TYPE" = 1
                AND A."PAY_TIME" >= TO_DATE('{cur_date_str}','YYYY-MM-DD')
                AND A."PAY_TIME" < TO_DATE('{next_date_str}','YYYY-MM-DD')"""
        rows = db.execute_query(sql) or []
        if rows and rows[0]:
            v = list(rows[0].values())[0]
            total_amount = float(v) if v is not None else 0.0
        sql2 = f"""SELECT SUM(CASE WHEN "PAY_DIRECTION" = 2 THEN -1 ELSE 1 END * "LITTER")
            FROM "T_GASORDERINFO" A
            WHERE "PAY_TIME" >= TO_DATE('{cur_date_str}','YYYY-MM-DD')
                AND "PAY_TIME" < TO_DATE('{next_date_str}','YYYY-MM-DD')"""
        rows2 = db.execute_query(sql2) or []
        if rows2 and rows2[0]:
            v = list(rows2[0].values())[0]
            total_count = float(v) if v is not None else 0.0
    elif data_type == 3000:  # 加水
        name = "加水"
        sql = f"""SELECT SUM("PRICE" - "REFUND_MONEY"), SUM("USE_FLOW")
            FROM "T_WATERMASTER" A
            WHERE "PAY_TIME" >= TO_DATE('{cur_date_str}','YYYY-MM-DD')
                AND "PAY_TIME" < TO_DATE('{cur_date_str}','YYYY-MM-DD') + 1"""
        rows = db.execute_query(sql) or []
        if rows and rows[0]:
            vals = list(rows[0].values())
            total_amount = float(vals[0]) if vals[0] is not None else 0.0
            total_count = float(vals[1]) if len(vals) > 1 and vals[1] is not None else 0.0
    elif data_type == 4000:  # 尿素
        name = "尿素"
        sql = f"""SELECT SUM("SALE"), SUM("LITER")
            FROM "T_UREAMASTER" A
            WHERE "UREAMASTER_DATE" = '{cur_date_str}'"""
        rows = db.execute_query(sql) or []
        if rows and rows[0]:
            vals = list(rows[0].values())
            total_amount = float(vals[0]) if vals[0] is not None else 0.0
            total_count = float(vals[1]) if len(vals) > 1 and vals[1] is not None else 0.0
    elif data_type == 5000:  # 新能源
        name = "新能源"

    def dec_to_str(v):
        if v == int(v): return str(int(v))
        return str(v)

    value_str = dec_to_str(total_amount / 10000) if show_wy else dec_to_str(total_amount)
    data_str = dec_to_str(total_count / 1000) if show_large_unit else dec_to_str(total_count)

    return {"data": data_str, "key": str(data_type), "name": name if name else None, "value": value_str}


# ===== 3. GetBayonetOwnerAHTreeDetail (内部方法, dataType=1时调用) =====
def get_bayonet_owner_ah_tree_detail(db: DatabaseHelper, sp_id: int, start_month: int, end_month: int,
                                      rank_num, page_index, page_size) -> tuple[list[dict], int]:
    """服务区→省份→城市 树形明细，返回 (result_list, total)"""
    from collections import defaultdict

    sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE","PROVINCE_NAME","CITY_NAME",
            SUM(ROUND("VEHICLE_COUNT" * "ANOLOG_RATIO")) AS "VEHICLE_COUNT"
        FROM "T_BAYONETOWMONTHLY_AH"
        WHERE "STATISTICS_MONTH" BETWEEN {start_month} AND {end_month} AND "SERVERPART_ID" = {sp_id}
        GROUP BY "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE","PROVINCE_NAME","CITY_NAME" """
    dt_bayonet = db.execute_query(sql) or []
    if not dt_bayonet:
        return [], 0

    sql_sf = f"""SELECT "SERVERPART_ID","SERVERPART_REGION",SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
        FROM "T_SECTIONFLOW"
        WHERE "STATISTICS_DATE" BETWEEN {start_month}01 AND {end_month}31 AND "SERVERPART_ID" = {sp_id}
        GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
    dt_sf = db.execute_query(sql_sf) or []

    sql_sp = f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME","SPREGIONTYPE_INDEX"
        FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {sp_id}"""
    dt_sp = db.execute_query(sql_sp) or []

    east = "东南"
    west = "西北"

    def count_vehicles(rows, vtype_contains, region_set):
        return sum(_safe_int(r.get("VEHICLE_COUNT")) for r in rows
                   if vtype_contains in str(r.get("VEHICLE_TYPE", ""))
                   and str(r.get("SERVERPART_REGION", "")) in region_set)

    sp_info = dt_sp[0] if dt_sp else {}
    east_light = count_vehicles(dt_bayonet, "小", east)
    east_mid = count_vehicles(dt_bayonet, "中", east)
    east_large = count_vehicles(dt_bayonet, "大", east)
    west_light = count_vehicles(dt_bayonet, "小", west)
    west_mid = count_vehicles(dt_bayonet, "中", west)
    west_large = count_vehicles(dt_bayonet, "大", west)
    total_count = sum(_safe_int(r.get("VEHICLE_COUNT")) for r in dt_bayonet)

    sf_total = sum(_safe_int(r.get("SECTIONFLOW_NUM")) for r in dt_sf)
    sf_east = sum(_safe_int(r.get("SECTIONFLOW_NUM")) for r in dt_sf if str(r.get("SERVERPART_REGION", "")) in east)
    sf_west = sum(_safe_int(r.get("SECTIONFLOW_NUM")) for r in dt_sf if str(r.get("SERVERPART_REGION", "")) in west)
    section_flow = {"total": float(sf_total), "RegionA": float(sf_east), "RegionB": float(sf_west)} if dt_sf else None
    entry_rate = None
    if section_flow and sf_total > 0:
        entry_rate = {
            "total": round(total_count / sf_total * 100, 2),
            "RegionA": round((east_light + east_mid + east_large) / sf_east * 100, 2) if sf_east > 0 else None,
            "RegionB": round((west_light + west_mid + west_large) / sf_west * 100, 2) if sf_west > 0 else None,
        }

    root_node = {
        "Index": 1, "ServerPartLevel": 0,
        "SPRegionTypeIndex": _safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
        "SPRegionTypeId": _safe_int(sp_info.get("SPREGIONTYPE_ID")),
        "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
        "ServerPartId": _safe_int(sp_info.get("SERVERPART_ID")),
        "ServerPartName": sp_info.get("SERVERPART_NAME"),
        "ProvinceName": None, "CityName": None,
        "SectionFlow": section_flow, "EntryRate": entry_rate,
        "EastLightDutyCount": east_light, "EastMidSizeCount": east_mid, "EastLargeCount": east_large,
        "WestLightDutyCount": west_light, "WestMidSizeCount": west_mid, "WestLargeCount": west_large,
        "LightDutyTotalCount": east_light + west_light, "MidSizeTotalCount": east_mid + west_mid,
        "LargeTotalCount": east_large + west_large, "TotalCount": total_count,
    }

    # 按省份分组
    prov_map = defaultdict(list)
    for r in dt_bayonet: prov_map[str(r.get("PROVINCE_NAME") or "")].append(r)
    prov_sorted = sorted(prov_map.items(), key=lambda x: sum(_safe_int(r.get("VEHICLE_COUNT")) for r in x[1]), reverse=True)

    def _build_city_node(city_name, city_rows, prov_name):
        c_total = sum(_safe_int(r.get("VEHICLE_COUNT")) for r in city_rows)
        cel = count_vehicles(city_rows, "小", east); cem = count_vehicles(city_rows, "中", east); cea = count_vehicles(city_rows, "大", east)
        cwl = count_vehicles(city_rows, "小", west); cwm = count_vehicles(city_rows, "中", west); cwa = count_vehicles(city_rows, "大", west)
        return {"node": {
            "Index": 999 if not city_name else 1, "ServerPartLevel": 2,
            "SPRegionTypeIndex": _safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
            "SPRegionTypeId": _safe_int(sp_info.get("SPREGIONTYPE_ID")),
            "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
            "ServerPartId": sp_id, "ServerPartName": sp_info.get("SERVERPART_NAME"),
            "ProvinceName": prov_name, "CityName": city_name or "其他",
            "SectionFlow": None, "EntryRate": None,
            "EastLightDutyCount": cel, "EastMidSizeCount": cem, "EastLargeCount": cea,
            "WestLightDutyCount": cwl, "WestMidSizeCount": cwm, "WestLargeCount": cwa,
            "LightDutyTotalCount": cel+cwl, "MidSizeTotalCount": cem+cwm, "LargeTotalCount": cea+cwa,
            "TotalCount": c_total,
        }, "children": None}

    province_children = []
    for prov_name_raw, prov_rows in prov_sorted:
        prov_name = prov_name_raw if prov_name_raw else "其他"
        p_total = sum(_safe_int(r.get("VEHICLE_COUNT")) for r in prov_rows)
        prov_node = {
            "Index": 999 if not prov_name_raw else 1, "ServerPartLevel": 1,
            "SPRegionTypeIndex": _safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
            "SPRegionTypeId": _safe_int(sp_info.get("SPREGIONTYPE_ID")),
            "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
            "ServerPartId": sp_id, "ServerPartName": sp_info.get("SERVERPART_NAME"),
            "ProvinceName": prov_name, "CityName": None, "SectionFlow": None, "EntryRate": None,
            "EastLightDutyCount": count_vehicles(prov_rows, "小", east),
            "EastMidSizeCount": count_vehicles(prov_rows, "中", east),
            "EastLargeCount": count_vehicles(prov_rows, "大", east),
            "WestLightDutyCount": count_vehicles(prov_rows, "小", west),
            "WestMidSizeCount": count_vehicles(prov_rows, "中", west),
            "WestLargeCount": count_vehicles(prov_rows, "大", west),
            "LightDutyTotalCount": count_vehicles(prov_rows, "小", east) + count_vehicles(prov_rows, "小", west),
            "MidSizeTotalCount": count_vehicles(prov_rows, "中", east) + count_vehicles(prov_rows, "中", west),
            "LargeTotalCount": count_vehicles(prov_rows, "大", east) + count_vehicles(prov_rows, "大", west),
            "TotalCount": p_total,
        }

        city_map = defaultdict(list)
        for r in prov_rows: city_map[str(r.get("CITY_NAME") or "")].append(r)
        city_sorted = sorted(city_map.items(), key=lambda x: sum(_safe_int(r.get("VEHICLE_COUNT")) for r in x[1]), reverse=True)

        city_children = []
        if rank_num and rank_num > 0 and len(city_sorted) >= rank_num:
            top_cities = [c for c in city_sorted if c[0]][:rank_num]
            top_total = 0; top_counts = {"el": 0, "em": 0, "ea": 0, "wl": 0, "wm": 0, "wa": 0}
            for cn, cr in top_cities:
                city_children.append(_build_city_node(cn, cr, prov_name))
                top_total += sum(_safe_int(r.get("VEHICLE_COUNT")) for r in cr)
                top_counts["el"] += count_vehicles(cr, "小", east)
                top_counts["em"] += count_vehicles(cr, "中", east)
                top_counts["ea"] += count_vehicles(cr, "大", east)
                top_counts["wl"] += count_vehicles(cr, "小", west)
                top_counts["wm"] += count_vehicles(cr, "中", west)
                top_counts["wa"] += count_vehicles(cr, "大", west)
            # 其他
            oel = max(0, prov_node["EastLightDutyCount"] - top_counts["el"])
            oem = max(0, prov_node["EastMidSizeCount"] - top_counts["em"])
            oea = max(0, prov_node["EastLargeCount"] - top_counts["ea"])
            owl = max(0, prov_node["WestLightDutyCount"] - top_counts["wl"])
            owm = max(0, prov_node["WestMidSizeCount"] - top_counts["wm"])
            owa = max(0, prov_node["WestLargeCount"] - top_counts["wa"])
            city_children.append({"node": {
                "Index": 999, "ServerPartLevel": 2,
                "SPRegionTypeIndex": _safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
                "SPRegionTypeId": _safe_int(sp_info.get("SPREGIONTYPE_ID")),
                "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
                "ServerPartId": sp_id, "ServerPartName": sp_info.get("SERVERPART_NAME"),
                "ProvinceName": prov_name, "CityName": "其他", "SectionFlow": None, "EntryRate": None,
                "EastLightDutyCount": oel, "EastMidSizeCount": oem, "EastLargeCount": oea,
                "WestLightDutyCount": owl, "WestMidSizeCount": owm, "WestLargeCount": owa,
                "LightDutyTotalCount": oel+owl, "MidSizeTotalCount": oem+owm, "LargeTotalCount": oea+owa,
                "TotalCount": p_total - top_total,
            }, "children": []})
        else:
            for cn, cr in city_sorted:
                city_children.append(_build_city_node(cn, cr, prov_name))
        city_children.sort(key=lambda x: (x["node"]["Index"], -(x["node"]["TotalCount"] or 0)))
        province_children.append({"node": prov_node, "children": city_children})

    province_children.sort(key=lambda x: (x["node"]["Index"], -(x["node"]["TotalCount"] or 0)))
    result_list = [{"node": root_node, "children": province_children}]
    return result_list, len(result_list)


# ===== 4. GetBayonetOwnerAHTreeList (汇总模式) =====
# 此函数逻辑过长（~200行）且与 Router 响应格式紧耦合, 保留在 Router 层
# 仅在此提供声明, 后续迁移时再抽取


# ===== 5. GetProvinceVehicleTreeList =====
# 同上, 树形构建逻辑（~170行）保留在 Router 层


# ===== 6. GetProvinceVehicleDetail =====
# 同上, 交叉查询逻辑（~150行）保留在 Router 层
