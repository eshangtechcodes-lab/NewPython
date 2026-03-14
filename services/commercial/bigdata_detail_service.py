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
from loguru import logger
from core.database import DatabaseHelper
from config import settings
from routers.deps import parse_multi_ids, build_in_condition
from models.base import Result, JsonListData

from services.commercial.service_utils import (
    safe_float as _sf,
    safe_int as _si,
)




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
        return sum(_si(r.get("VEHICLE_COUNT")) for r in rows
                   if vtype_contains in str(r.get("VEHICLE_TYPE", ""))
                   and str(r.get("SERVERPART_REGION", "")) in region_set)

    sp_info = dt_sp[0] if dt_sp else {}
    east_light = count_vehicles(dt_bayonet, "小", east)
    east_mid = count_vehicles(dt_bayonet, "中", east)
    east_large = count_vehicles(dt_bayonet, "大", east)
    west_light = count_vehicles(dt_bayonet, "小", west)
    west_mid = count_vehicles(dt_bayonet, "中", west)
    west_large = count_vehicles(dt_bayonet, "大", west)
    total_count = sum(_si(r.get("VEHICLE_COUNT")) for r in dt_bayonet)

    sf_total = sum(_si(r.get("SECTIONFLOW_NUM")) for r in dt_sf)
    sf_east = sum(_si(r.get("SECTIONFLOW_NUM")) for r in dt_sf if str(r.get("SERVERPART_REGION", "")) in east)
    sf_west = sum(_si(r.get("SECTIONFLOW_NUM")) for r in dt_sf if str(r.get("SERVERPART_REGION", "")) in west)
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
        "SPRegionTypeIndex": _si(sp_info.get("SPREGIONTYPE_INDEX")),
        "SPRegionTypeId": _si(sp_info.get("SPREGIONTYPE_ID")),
        "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
        "ServerPartId": _si(sp_info.get("SERVERPART_ID")),
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
    prov_sorted = sorted(prov_map.items(), key=lambda x: sum(_si(r.get("VEHICLE_COUNT")) for r in x[1]), reverse=True)

    def _build_city_node(city_name, city_rows, prov_name):
        c_total = sum(_si(r.get("VEHICLE_COUNT")) for r in city_rows)
        cel = count_vehicles(city_rows, "小", east); cem = count_vehicles(city_rows, "中", east); cea = count_vehicles(city_rows, "大", east)
        cwl = count_vehicles(city_rows, "小", west); cwm = count_vehicles(city_rows, "中", west); cwa = count_vehicles(city_rows, "大", west)
        return {"node": {
            "Index": 999 if not city_name else 1, "ServerPartLevel": 2,
            "SPRegionTypeIndex": _si(sp_info.get("SPREGIONTYPE_INDEX")),
            "SPRegionTypeId": _si(sp_info.get("SPREGIONTYPE_ID")),
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
        p_total = sum(_si(r.get("VEHICLE_COUNT")) for r in prov_rows)
        prov_node = {
            "Index": 999 if not prov_name_raw else 1, "ServerPartLevel": 1,
            "SPRegionTypeIndex": _si(sp_info.get("SPREGIONTYPE_INDEX")),
            "SPRegionTypeId": _si(sp_info.get("SPREGIONTYPE_ID")),
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
        city_sorted = sorted(city_map.items(), key=lambda x: sum(_si(r.get("VEHICLE_COUNT")) for r in x[1]), reverse=True)

        city_children = []
        if rank_num and rank_num > 0 and len(city_sorted) >= rank_num:
            top_cities = [c for c in city_sorted if c[0]][:rank_num]
            top_total = 0; top_counts = {"el": 0, "em": 0, "ea": 0, "wl": 0, "wm": 0, "wa": 0}
            for cn, cr in top_cities:
                city_children.append(_build_city_node(cn, cr, prov_name))
                top_total += sum(_si(r.get("VEHICLE_COUNT")) for r in cr)
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
                "SPRegionTypeIndex": _si(sp_info.get("SPREGIONTYPE_INDEX")),
                "SPRegionTypeId": _si(sp_info.get("SPREGIONTYPE_ID")),
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


# ===================================================================
# GetRevenueTrendChart — 营收趋势图
# ===================================================================

def get_revenue_trend_chart(db, post_data):
    """获取营收趋势图数据"""
    from core.aes_util import decrypt_post_data
    params = decrypt_post_data(postData)
    province_code = params.get("ProvinceCode", "")
    serverpart_id = params.get("ServerpartId", "")
    serverpart_code = params.get("ServerpartCode", "")
    logger.info(f"GetRevenueTrendChart 解密参数: ProvinceCode={province_code}")

    if not province_code:
        return Result.fail(code=205, msg="查询失败,请传入省份编码！")

    import math
    from datetime import datetime as dt

    # 获取服务区编码列表
    serverpart_codes = []
    if serverpart_code:
        serverpart_codes = [serverpart_code]
    elif serverpart_id:
        _sp_ids_rt = parse_multi_ids(serverpart_id)
        if _sp_ids_rt:
            rows = db.execute_query(
                f'SELECT "SERVERPART_CODE" FROM "T_SERVERPART" WHERE ' + build_in_condition('SERVERPART_ID', _sp_ids_rt))
        else:
            rows = []
        serverpart_codes = [r["SERVERPART_CODE"] for r in rows if r.get("SERVERPART_CODE")]
    else:
        # 获取省份对应的FieldEnum_ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": province_code})
        if fe_rows:
            province_id = fe_rows[0]["FIELDENUM_ID"]
            rows = db.execute_query(
                f'SELECT "SERVERPART_CODE" FROM "T_SERVERPART" WHERE "STATISTICS_TYPE" = 1000 AND "STATISTIC_TYPE" = 1000 AND "PROVINCE_CODE" = {province_id}')
            serverpart_codes = [r["SERVERPART_CODE"] for r in rows if r.get("SERVERPART_CODE")]
            # C#对齐: ServerpartCodes.Remove("510206"); ServerpartCodes.Remove("510505");
            for exclude_code in ["510206", "510505"]:
                if exclude_code in serverpart_codes:
                    serverpart_codes.remove(exclude_code)

    # 从 Redis 读取营收趋势数据
    import redis
    table_name = f"RevenueTrend:{dt.now().strftime('%Y%m%d')}"
    all_data = {}
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_REVENUE_TREND_DB,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_timeout=2,
        )
        all_data = redis_client.hgetall(table_name) or {}
    except Exception as ex:
        logger.warning(f"Redis 连接失败: {ex}")
        all_data = {}

    # 汇总各服务区的营收趋势数据
    result_list = []
    for sp_code in serverpart_codes:
        val = all_data.get(sp_code, "")
        if val:
            try:
                import json
                item = json.loads(val)
                result_list.append(item)
            except Exception:
                pass

    return result_list
# ===================================================================
# GetProvinceVehicleTreeList — 各省入区车辆统计树
# ===================================================================

def get_province_vehicle_tree_list(db, serverPartId, statisticsStartMonth, statisticsEndMonth, rankNum, pageIndex, pageSize):
    """获取各省入区车辆统计树形列表"""
    from collections import defaultdict

    where_sql = ""
    _sp_ids = parse_multi_ids(serverPartId)
    if _sp_ids:
        where_sql = " AND " + build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'T."SERVERPART_ID"')

    # 1. 查车辆归属地月度固化数据(按省份/城市/片区分组)
    sql = f"""SELECT T."PROVINCE_NAME", T."CITY_NAME", T1."SPREGIONTYPE_ID",
            SUM(ROUND(T."VEHICLE_COUNT" * T."ANOLOG_RATIO")) AS "VEHICLE_COUNT"
        FROM "T_BAYONETOWMONTHLY_AH" T, "T_SERVERPART" T1
        WHERE T."SERVERPART_ID" = T1."SERVERPART_ID"
            AND T."STATISTICS_MONTH" BETWEEN {statisticsStartMonth} AND {statisticsEndMonth}{where_sql}
        GROUP BY T."PROVINCE_NAME", T."CITY_NAME", T1."SPREGIONTYPE_ID" """
    dt_data = db.execute_query(sql) or []

    if not dt_data:
        json_list = JsonListData.create(data_list=[], total=0, page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    # 2. 查片区信息
    rt_ids = list(set(str(r["SPREGIONTYPE_ID"]) for r in dt_data if r.get("SPREGIONTYPE_ID")))
    sp_where = ""
    if serverPartId:
        _sp_ids_pv = parse_multi_ids(serverPartId)
        if _sp_ids_pv:
            sp_where = " OR " + build_in_condition('SERVERPART_ID', _sp_ids_pv)
    sql_sp = f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME","SPREGIONTYPE_INDEX"
        FROM "T_SERVERPART" WHERE "SPREGIONTYPE_ID" IN ({','.join(rt_ids)}){sp_where}"""
    dt_sp = db.execute_query(sql_sp) or []

    # 片区基础信息
    rt_map = {}
    for r in dt_sp:
        rt_id = r.get("SPREGIONTYPE_ID")
        if rt_id and rt_id not in rt_map:
            rt_map[rt_id] = {
                "SPRegionTypeIndex": r.get("SPREGIONTYPE_INDEX"),
                "SPRegionTypeId": rt_id,
                "SPRegionTypeName": r.get("SPREGIONTYPE_NAME"),
            }

    # 3. 构建城市嵌套(按省份+城市分组,每个含各片区车辆数)
    city_groups = defaultdict(lambda: defaultdict(int))  # (province, city) -> {rt_id: count}
    for r in dt_data:
        prov = r.get("PROVINCE_NAME") or ""
        city = r.get("CITY_NAME") or ""
        rt_id = r.get("SPREGIONTYPE_ID")
        vc = int(r.get("VEHICLE_COUNT") or 0)
        city_groups[(prov, city)][rt_id] = city_groups[(prov, city)].get(rt_id, 0) + vc

    # 城市节点
    city_nodes = []
    for (prov, city), rt_counts in city_groups.items():
        total_vc = sum(rt_counts.values())
        sp_list = []
        for rt_id, info in sorted(rt_map.items(), key=lambda x: x[1].get("SPRegionTypeIndex") or 99):
            sp_list.append({
                "SPRegionTypeIndex": info["SPRegionTypeIndex"],
                "SPRegionTypeId": info["SPRegionTypeId"],
                "SPRegionTypeName": info["SPRegionTypeName"],
                "ProvinceName": prov,
                "VehicleCount": rt_counts.get(rt_id, 0),
                "CityName": city or "其他",
                "IsOther": True if not city else False,
                "ServerPartId": None,
                "ServerPartIds": None,
                "ServerPartName": None,
            })
        city_nodes.append({
            "node": {
                "Index": 999 if not city else 1,
                "ProvinceOrCityName": "其他" if not city else city,
                "ProvinceOrCityPName": prov,
                "TotalCount": total_vc,
                "SPRegionTypeList": sp_list,
            },
            "children": None,
        })

    # 4. 按省份汇总
    prov_groups = defaultdict(list)
    for cn in city_nodes:
        prov_groups[cn["node"]["ProvinceOrCityPName"]].append(cn)

    province_nodes = []
    for prov, children in prov_groups.items():
        children.sort(key=lambda x: (x["node"]["Index"], -(x["node"]["TotalCount"] or 0)))
        total_vc = sum(c["node"]["TotalCount"] for c in children)
        # 汇总片区数据
        rt_totals = defaultdict(int)
        for c in children:
            for sp in c["node"].get("SPRegionTypeList", []):
                rt_totals[sp["SPRegionTypeId"]] = rt_totals.get(sp["SPRegionTypeId"], 0) + sp.get("VehicleCount", 0)
        sp_list = []
        for rt_id, info in sorted(rt_map.items(), key=lambda x: x[1].get("SPRegionTypeIndex") or 99):
            sp_list.append({
                "SPRegionTypeIndex": info["SPRegionTypeIndex"],
                "SPRegionTypeId": info["SPRegionTypeId"],
                "SPRegionTypeName": info["SPRegionTypeName"],
                "ProvinceName": prov,
                "CityName": None,
                "IsOther": False,
                "ServerPartId": None,
                "ServerPartIds": None,
                "ServerPartName": None,
                "VehicleCount": rt_totals.get(rt_id, 0),
            })
        province_nodes.append({
            "node": {
                "Index": 999 if not prov else 1,
                "ProvinceOrCityName": "其他" if not prov else prov,
                "ProvinceOrCityPName": None,
                "TotalCount": total_vc,
                "SPRegionTypeList": sp_list,
            },
            "children": children,
        })
    province_nodes.sort(key=lambda x: (x["node"]["Index"], -(x["node"]["TotalCount"] or 0)))

    # 5. 顶层"全部省份"
    all_total = sum(p["node"]["TotalCount"] for p in province_nodes)
    rt_all = defaultdict(int)
    for p in province_nodes:
        for sp in p["node"].get("SPRegionTypeList", []):
            rt_all[sp["SPRegionTypeId"]] = rt_all.get(sp["SPRegionTypeId"], 0) + sp.get("VehicleCount", 0)
    all_sp = []
    for rt_id, info in sorted(rt_map.items(), key=lambda x: x[1].get("SPRegionTypeIndex") or 99):
        all_sp.append({
            "SPRegionTypeIndex": info["SPRegionTypeIndex"],
            "SPRegionTypeId": info["SPRegionTypeId"],
            "SPRegionTypeName": info["SPRegionTypeName"],
            "ProvinceName": None,
            "CityName": None,
            "IsOther": False,
            "ServerPartId": None,
            "ServerPartIds": None,
            "ServerPartName": None,
            "VehicleCount": rt_all.get(rt_id, 0),
        })

    result = [{
        "node": {
            "Index": 1,
            "ProvinceOrCityName": "全部省份",
            "ProvinceOrCityPName": None,
            "TotalCount": all_total,
            "SPRegionTypeList": all_sp,
        },
        "children": province_nodes,
    }]

    json_list = JsonListData.create(data_list=result, total=len(result), page_size=10)
    return Result.success(data=json_list.model_dump(), msg="成功")


# ===================================================================
# GetProvinceVehicleDetail — 各省入区车辆明细
# ===================================================================

def get_province_vehicle_detail(db, statisticsStartMonth, statisticsEndMonth, provinceName, serverPartId, cityName, rankNum, pageIndex, pageSize):
    """获取各省入区车辆统计明细"""
    from collections import defaultdict

    # ---- 构建 WHERE 条件 (与C#完全一致) ----
    where_sql = ""
    if provinceName != "其他":
        where_sql += f""" AND "PROVINCE_NAME" = '{provinceName}'"""
    else:
        where_sql += """ AND "PROVINCE_NAME" IS NULL"""
        # 省份和城市同时为"其他"，表示未匹配到省份及城市的车流信息
        if cityName and cityName == "其他":
            where_sql += """ AND "CITY_NAME" IS NULL"""
    _sp_ids_d = parse_multi_ids(serverPartId)
    if _sp_ids_d:
        where_sql += " AND " + build_in_condition('SERVERPART_ID', _sp_ids_d)
    if cityName and cityName != "" and cityName != "其他":
        where_sql += f""" AND "CITY_NAME" = '{cityName}'"""

    # ---- C# SQL: 按 SERVERPART_ID, CITY_NAME 分组 ----
    sql = f"""SELECT "SERVERPART_ID", "CITY_NAME",
            SUM(ROUND("VEHICLE_COUNT" * "ANOLOG_RATIO")) AS "VEHICLE_COUNT"
        FROM "T_BAYONETOWMONTHLY_AH"
        WHERE "STATISTICS_MONTH" BETWEEN {statisticsStartMonth} AND {statisticsEndMonth}{where_sql}
        GROUP BY "SERVERPART_ID", "CITY_NAME" """
    dt_data = db.execute_query(sql) or []

    # ---- cityName=="其他" 且 provinceName!="其他" 时的特殊过滤 ----
    # C# 逻辑: 先取 Top N 城市，然后把这些城市的数据剔除，留下"其他"城市的数据
    if cityName == "其他" and provinceName != "其他" and rankNum:
        city_totals = defaultdict(int)
        for r in dt_data:
            cn = str(r.get("CITY_NAME") or "")
            city_totals[cn] += int(r.get("VEHICLE_COUNT") or 0)
        # 取 Top N 城市名
        top_cities = sorted(city_totals.items(), key=lambda x: x[1], reverse=True)[:rankNum]
        top_city_names = [c[0] for c in top_cities]
        # 过滤掉 Top N 城市，保留剩余数据
        dt_data = [r for r in dt_data if str(r.get("CITY_NAME") or "") not in top_city_names]

    if not dt_data:
        json_list = JsonListData.create(data_list=[], total=0, page_index=pageIndex or 1, page_size=pageSize or 10)
        return Result.success(data=json_list.model_dump())

    # ---- 获取所有服务区内码（按车辆总数降序排列） ----
    sp_totals = defaultdict(int)
    for r in dt_data:
        sp_totals[int(r.get("SERVERPART_ID") or 0)] += int(r.get("VEHICLE_COUNT") or 0)
    server_part_id_list = sorted(sp_totals.keys(), key=lambda x: sp_totals[x], reverse=True)

    # ---- 查询服务区信息 ----
    sp_id_str = ",".join(str(s) for s in server_part_id_list)
    sql_sp = f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME","SPREGIONTYPE_INDEX"
        FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({sp_id_str})"""
    dt_sp = db.execute_query(sql_sp) or []
    sp_map = {int(r["SERVERPART_ID"]): r for r in dt_sp}

    # ---- 构建服务区排名列表(rankNumServerPartList) ----
    rank_sp_list = []  # 每项: {info, sp_ids, is_other}

    if rankNum and rankNum > 0 and len(server_part_id_list) > rankNum:
        # Top N 服务区
        top_sp_ids = server_part_id_list[:rankNum]
        for sp_id in top_sp_ids:
            info = sp_map.get(sp_id, {})
            rank_sp_list.append({
                "SPRegionTypeIndex": info.get("SPREGIONTYPE_INDEX"),
                "SPRegionTypeId": info.get("SPREGIONTYPE_ID"),
                "SPRegionTypeName": info.get("SPREGIONTYPE_NAME"),
                "ServerPartId": sp_id,
                "ServerPartIds": [sp_id],
                "ServerPartName": info.get("SERVERPART_NAME"),
                "IsOther": False,
            })
        # "其他"服务区 = 所有不在 Top N 中的
        other_sp_ids = [s for s in server_part_id_list if s not in top_sp_ids]
        rank_sp_list.append({
            "SPRegionTypeIndex": None,
            "SPRegionTypeId": None,
            "SPRegionTypeName": None,
            "ServerPartId": None,
            "ServerPartIds": other_sp_ids,
            "ServerPartName": "其他",
            "IsOther": True,
        })
    else:
        # 无排名限制，所有服务区都直接列出
        for sp_id in server_part_id_list:
            info = sp_map.get(sp_id, {})
            rank_sp_list.append({
                "SPRegionTypeIndex": info.get("SPREGIONTYPE_INDEX"),
                "SPRegionTypeId": info.get("SPREGIONTYPE_ID"),
                "SPRegionTypeName": info.get("SPREGIONTYPE_NAME"),
                "ServerPartId": sp_id,
                "ServerPartIds": [sp_id],
                "ServerPartName": info.get("SERVERPART_NAME"),
                "IsOther": False,
            })

    # ---- 获取全部城市 ----
    city_list = list(set(str(r.get("CITY_NAME") or "") for r in dt_data))

    # ---- 组合 服务区×城市 交叉 → 平铺列表 (对齐C# LINQ交叉查询) ----
    result = []
    for sp_info in rank_sp_list:
        for city in city_list:
            # 计算该服务区组 × 该城市的车辆数
            vc = sum(
                int(r.get("VEHICLE_COUNT") or 0)
                for r in dt_data
                if int(r.get("SERVERPART_ID") or 0) in sp_info["ServerPartIds"]
                and str(r.get("CITY_NAME") or "") == city
            )
            result.append({
                "SPRegionTypeIndex": sp_info["SPRegionTypeIndex"],
                "SPRegionTypeId": sp_info["SPRegionTypeId"],
                "SPRegionTypeName": sp_info["SPRegionTypeName"],
                "ServerPartId": sp_info["ServerPartId"],
                "ServerPartIds": sp_info["ServerPartIds"],
                "ServerPartName": sp_info["ServerPartName"],
                "ProvinceName": provinceName if provinceName != "其他" else "",
                "CityName": city if city else "其他",
                "IsOther": sp_info["IsOther"],
                "VehicleCount": vc,
            })

    # ---- C# 排序: IsOther升序 → SPRegionTypeIndex升序 → VehicleCount降序 ----
    result.sort(key=lambda x: (
        1 if x["IsOther"] else 0,
        x["SPRegionTypeIndex"] if x["SPRegionTypeIndex"] is not None else 99,
        -(x["VehicleCount"] or 0)
    ))

    # ---- C# Controller层分页 ----
    total_count = len(result)
    json_list = JsonListData.create(data_list=result, total=total_count,
                                     page_index=pageIndex or 1, page_size=pageSize or 10)
    return Result.success(data=json_list.model_dump())
