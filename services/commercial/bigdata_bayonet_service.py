# -*- coding: utf-8 -*-
"""
CommercialApi - 大数据车流分析 Service
从 bigdata_router.py 中抽取: 车流入区/停留时长/归属地/排行/平均分析
每个函数独立、可单独迁移
"""
from typing import Optional
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition

from services.commercial.service_utils import (
    date_no_pad,
    safe_float as _sf,
    safe_int as _si,
)




# ===== Helper: 车辆停留时长模型 =====
def build_sta_model(rows, vehicle_types, sp_id, sp_name, region):
    """构建车辆停留时长分析模型（按方位聚合）"""
    vc_list, st_list, valid_types = [], [], []
    for vt in vehicle_types:
        vt_rows = [r for r in rows if r.get("VEHICLE_TYPE") == vt]
        if not vt_rows: continue
        valid_types.append(vt)
        dates = set(r.get("STATISTICS_DATE") for r in vt_rows)
        total_days = max(len(dates), 1)
        total_vc = sum(r.get("VEHICLE_COUNT") or 0 for r in vt_rows)
        avg_vc = int(total_vc / total_days)
        vc_list.append({"name": vt, "value": str(avg_vc)})
        total_st_count = sum(int(r.get("STAY_TIMESCOUNT") or 0) for r in vt_rows)
        if total_st_count > 0:
            total_st = sum(float(r.get("STAY_TIMES") or 0) for r in vt_rows)
            avg_st = total_st / total_st_count / 60
        else:
            avg_st = 0
        st_list.append({"name": vt, "value": f"{avg_st:.2f}"})
    return {
        "Serverpart_ID": sp_id, "Serverpart_Name": sp_name, "Serverpart_Region": region,
        "Vehicle_Type": valid_types, "VehicleCountList": vc_list, "StayTimesList": st_list,
    }


# ===== Helper: 归属地模型 =====
def build_oa_model(city_rows, prov_rows, sp_id, sp_name, region, city_top, prov_top):
    """构建车辆归属地分析模型（城市Top-N + 省份Top-N）"""
    city_map = {}
    for r in city_rows:
        cn = r.get("CITY_NAME") or ""
        city_map[cn] = city_map.get(cn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    city_sorted = sorted(city_map.items(), key=lambda x: x[1], reverse=True)[:city_top]
    city_list = [{"name": c[0], "value": str(int(c[1]))} for c in city_sorted]

    prov_map = {}
    for r in prov_rows:
        pn = r.get("PROVINCE_NAME") or ""
        prov_map[pn] = prov_map.get(pn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    prov_sorted_all = sorted(prov_map.items(), key=lambda x: x[1], reverse=True)
    prov_sorted = prov_sorted_all[:prov_top]
    prov_list = [{"name": p[0], "value": str(int(p[1]))} for p in prov_sorted]
    if len(prov_sorted_all) > prov_top:
        other_count = sum(p[1] for p in prov_sorted_all[prov_top:])
        prov_list.append({"name": "其他", "value": str(int(other_count))})

    total_vc = sum(float(r.get("VEHICLE_COUNT") or 0) for r in city_rows)
    return {
        "Serverpart_ID": sp_id, "Serverpart_Name": sp_name, "Serverpart_Region": region,
        "OwnerCity": [c[0] for c in city_sorted],
        "OwnerProvince": [p[0] for p in prov_sorted] + (["其他"] if len(prov_sorted_all) > prov_top else []),
        "Vehicle_Count": int(total_vc),
        "OwnerCityList": city_list if city_list else [{"name": None, "value": None}],
        "OwnerProvinceList": prov_list,
    }


# ===== Helper: 省份归属地模型 =====
def build_province_oa_model(city_rows, prov_rows, sp_id, sp_name, region, city_top, is_exclude, prov_top=0):
    """构建省份归属地分析模型（省份->城市嵌套）"""
    prov_map = {}
    for r in prov_rows:
        pn = r.get("PROVINCE_NAME") or ""
        prov_map[pn] = prov_map.get(pn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    prov_sorted = sorted(prov_map.items(), key=lambda x: x[1], reverse=True)

    total_vc = sum(float(r.get("VEHICLE_COUNT") or 0) for r in prov_rows)
    city_total = sum(float(r.get("VEHICLE_COUNT") or 0) for r in city_rows)
    vehicle_count = int(max(total_vc, city_total))

    prov_list = []
    other_count = vehicle_count
    if prov_top > 0:
        show_provs = prov_sorted[:prov_top]
        for pn, pv in show_provs:
            prov_list.append({"name": pn, "value": str(int(pv))})
            other_count -= int(pv)
    if other_count > 0:
        prov_list.append({"name": "其他", "value": str(other_count)})

    owner_province = [p["name"] for p in prov_list]

    city_map = {}
    for r in city_rows:
        cn = r.get("CITY_NAME") or ""
        city_map[cn] = city_map.get(cn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    city_sorted_top = sorted(city_map.items(), key=lambda x: x[1], reverse=True)[:city_top]
    top_city_list = [{"name": c[0], "value": str(int(c[1]))} for c in city_sorted_top]
    if not top_city_list:
        top_city_list = [{"name": None, "value": None}]
    return {
        "Serverpart_ID": sp_id, "Serverpart_Name": sp_name, "Serverpart_Region": region,
        "OwnerCity": [c[0] for c in city_sorted_top],
        "OwnerProvince": owner_province, "Vehicle_Count": vehicle_count,
        "OwnerProvinceList": prov_list, "OwnerCityList": top_city_list,
    }


# ===== 1. GetBayonetEntryList =====
def get_bayonet_entry_list(db: DatabaseHelper, statistics_date, serverpart_id, serverpart_region, show_addup_count) -> list[dict]:
    """服务区入区车流分析"""
    from datetime import datetime as dt, timedelta

    if not statistics_date:
        statistics_date = dt.now().strftime("%Y-%m-%d")
    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    date_str = stat_date.strftime("%Y%m%d")
    ydate_str = (stat_date - timedelta(days=1)).strftime("%Y%m%d")

    # --- SQL 参数化: 入区车流 WHERE 条件 ---
    where_sql = ""
    entry_params = {"d_str": date_str, "yd_str": ydate_str}
    if serverpart_id is not None:
        where_sql += ' AND "SERVERPART_ID" = :sp_id'
        entry_params["sp_id"] = serverpart_id
    if serverpart_region:
        where_sql += ' AND "SERVERPART_REGION" = :region'
        entry_params["region"] = serverpart_region

    # 今日入区车流
    if serverpart_id is not None:
        iv_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
            FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = :d_str{where_sql}
            GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
    else:
        iv_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
            FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = :d_str{where_sql}"""
    dt_in = db.execute_query(iv_sql, entry_params) or []

    # 今日断面流量
    if serverpart_id is not None:
        sf_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","SERVERPART_NAME",
                "SECTIONFLOW_NUM","SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0) AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = :d_str{where_sql}"""
    else:
        sf_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION",'' AS "SERVERPART_NAME",
                SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
                SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = :d_str{where_sql}"""
    dt_sf = db.execute_query(sf_sql, entry_params) or []

    # 昨日入区车流
    # 重用 entry_params 但用 yd_str 代替 d_str
    y_params = {**entry_params, "d_str": ydate_str}
    if serverpart_id is not None:
        ivy_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
            FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = :d_str{where_sql}
            GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
    else:
        ivy_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
            FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = :d_str{where_sql}"""
    dt_in_y = db.execute_query(ivy_sql, y_params) or []

    # 昨日断面流量
    if serverpart_id is not None:
        sfy_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","SERVERPART_NAME",
                "SECTIONFLOW_NUM","SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0) AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = :d_str{where_sql}"""
    else:
        sfy_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION",'' AS "SERVERPART_NAME",
                SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
                SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = :d_str{where_sql}"""
    dt_sf_y = db.execute_query(sfy_sql, y_params) or []

    # 构建索引
    def build_map(rows):
        m = {}
        for r in rows:
            key = (r.get("SERVERPART_ID"), r.get("SERVERPART_REGION", ""))
            m[key] = r
        return m
    in_map = build_map(dt_in)
    in_y_map = build_map(dt_in_y)
    sf_y_map = build_map(dt_sf_y)

    result_list = []
    regions_order = ["东", "南", "西", "北"]

    def bind_model(sf_row, key):
        sp_flow = _si(sf_row.get("SERVERPART_FLOW"))
        section_num = _si(sf_row.get("SECTIONFLOW_NUM"))
        in_vc = _si(in_map.get(key, {}).get("VEHICLE_COUNT"))
        vc = max(sp_flow, in_vc)
        entry_rate = round(vc / section_num * 100, 2) if section_num > 0 and vc > 0 else 0
        vy = _si(in_y_map.get(key, {}).get("VEHICLE_COUNT"))
        sy = _si(sf_y_map.get(key, {}).get("SECTIONFLOW_NUM"))
        spy = _si(sf_y_map.get(key, {}).get("SERVERPART_FLOW"))
        vy = max(vy, spy)
        vg_rate, eg_rate = None, None
        if vy > 0 and sy > 0:
            vg_rate = round((vc - vy) / vy * 100, 2)
            ey = round(vy / sy * 100, 2)
            eg_rate = round((entry_rate - ey) / ey * 100, 2) if ey > 0 else 100
        elif vy > 0:
            vg_rate = round((vc - vy) / vy * 100, 2); eg_rate = 100
        else:
            vg_rate = 100; eg_rate = 100
        return {
            "Serverpart_ID": sf_row.get("SERVERPART_ID"),
            "Serverpart_Name": sf_row.get("SERVERPART_NAME", ""),
            "Serverpart_Region": sf_row.get("SERVERPART_REGION", ""),
            "Vehicle_Count": vc, "SectionFlow_Count": section_num, "Entry_Rate": entry_rate,
            "Vehicle_GrowthRate": vg_rate, "Entry_GrowthRate": eg_rate, "Stay_Times": None,
        }

    if serverpart_id is not None:
        for region in regions_order:
            for sf_row in dt_sf:
                if sf_row.get("SERVERPART_REGION") == region:
                    key = (sf_row.get("SERVERPART_ID"), region)
                    item = bind_model(sf_row, key)
                    if item["Vehicle_Count"] > 0 or item["SectionFlow_Count"] > 0:
                        result_list.append(item)
    elif dt_sf:
        key = (None, "")
        item = bind_model(dt_sf[0], key)
        result_list.append(item)

    return result_list


# ===== 2. GetBayonetSTAList =====
def get_bayonet_sta_list(db: DatabaseHelper, statistics_date, serverpart_id, serverpart_region, contain_whole) -> list[dict]:
    """获取车辆停留时长分析"""
    from datetime import datetime as dt
    if not statistics_date:
        statistics_date = dt.now().strftime("%Y-%m-%d")
    date_str = statistics_date.replace("-", "")
    month_start = date_str[:6] + "00"

    conditions = [f'"STATISTICS_DATE" >= {month_start}', f'"STATISTICS_DATE" <= {date_str}', '"INOUT_TYPE" = 0']
    params = {}
    if serverpart_id:
        conditions.append('"SERVERPART_ID" = :spid'); params["spid"] = serverpart_id
    if serverpart_region:
        conditions.append('"SERVERPART_REGION" = :region'); params["region"] = serverpart_region
    where = " AND ".join(conditions)

    vehicle_types = ["小型车", "中型车", "大型车"]
    regions_order = ["东", "南", "西", "北"]

    if serverpart_id:
        sql = f"""SELECT SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT", "STATISTICS_DATE",
                SUM("STAY_TIMES") AS "STAY_TIMES", SUM("STAY_TIMESCOUNT") AS "STAY_TIMESCOUNT",
                "SERVERPART_ID", "SERVERPART_NAME", "SERVERPART_REGION", "VEHICLE_TYPE"
            FROM "T_BAYONETDAILY_AH" WHERE {where}
            GROUP BY "SERVERPART_ID", "SERVERPART_NAME", "SERVERPART_REGION", "VEHICLE_TYPE", "STATISTICS_DATE" """
        rows = db.execute_query(sql, params)
        rows = [r for r in rows if (r.get("VEHICLE_COUNT") or 0) > 0]

        result_list = []
        sp_name = rows[0].get("SERVERPART_NAME", "") if rows else ""
        if contain_whole:
            result_list.append(build_sta_model(rows, vehicle_types, serverpart_id, "全部", ""))
        for region in regions_order:
            region_rows = [r for r in rows if r.get("SERVERPART_REGION") == region]
            if region_rows:
                result_list.append(build_sta_model(region_rows, vehicle_types, serverpart_id, sp_name, region))
    else:
        sql = f"""SELECT ROUND(SUM("VEHICLE_COUNT") / COUNT(DISTINCT "STATISTICS_DATE"), 0) AS "VEHICLE_COUNT",
                CASE WHEN SUM("STAY_TIMESCOUNT") > 0
                    THEN ROUND(SUM("STAY_TIMES") / SUM("STAY_TIMESCOUNT"), 2) END AS "STAY_TIMES",
                "SERVERPART_ID", "VEHICLE_TYPE"
            FROM "T_BAYONETDAILY_AH" WHERE "VEHICLE_COUNT" > 0 AND {where}
            GROUP BY "SERVERPART_ID", "VEHICLE_TYPE" """
        rows = db.execute_query(sql, params)
        vc_list, st_list, valid_types = [], [], []
        for vt in vehicle_types:
            vt_rows = [r for r in rows if r.get("VEHICLE_TYPE") == vt]
            if not vt_rows: continue
            valid_types.append(vt)
            avg_vc = sum(r.get("VEHICLE_COUNT") or 0 for r in vt_rows) / max(len(vt_rows), 1)
            avg_st = sum(float(r.get("STAY_TIMES") or 0) for r in vt_rows) / max(len(vt_rows), 1) / 60
            vc_list.append({"name": vt, "value": str(int(avg_vc))})
            st_list.append({"name": vt, "value": f"{avg_st:.2f}"})
        result_list = [{"Vehicle_Type": valid_types, "VehicleCountList": vc_list, "StayTimesList": st_list}]

    return result_list


# ===== 3. GetBayonetOAList =====
def get_bayonet_oa_list(db: DatabaseHelper, statistics_month, serverpart_id, serverpart_region,
                        owner_city_length, owner_province_length, contain_whole) -> tuple[list[dict], list]:
    """获取车辆归属地分析，返回 (result_list, other_data)"""
    from datetime import datetime as dt
    import calendar
    sm = statistics_month or dt.now().strftime("%Y%m")
    if sm == dt.now().strftime("%Y%m"):
        cur_days = (dt.now().day - 1) or 1
    else:
        year, month = int(sm[:4]), int(sm[4:6])
        cur_days = calendar.monthrange(year, month)[1]

    conditions = [f'A."STATISTICS_MONTH" = :sm']
    params = {"sm": int(sm)}
    if serverpart_id:
        conditions.append('A."SERVERPART_ID" = :spid'); params["spid"] = serverpart_id
    else:
        conditions.append('A."SERVERPART_ID" = 0')
    if serverpart_region:
        conditions.append('A."SERVERPART_REGION" = :region'); params["region"] = serverpart_region
    conditions.append('A."VEHICLE_TYPE" IS NULL')
    where = " AND ".join(conditions)

    sql = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
            B."CITY_NAME", B."PROVINCE_NAME",
            A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
        FROM "T_BAYONETOWNERMONTH_AH" A, "T_VEHICLEOWNER" B
        WHERE A."LICENSE_PLATE" = B."LICENSE_PLATE" AND {where}"""
    city_rows = db.execute_query(sql, params)

    sql2 = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
            A."PROVINCE_NAME", A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
        FROM "T_BAYONETPROVINCEMONTH_AH" A WHERE {where}"""
    prov_rows = db.execute_query(sql2, params)

    regions_order = ["东", "南", "西", "北"]
    result_list = []
    if not serverpart_id:
        result_list.append(build_oa_model(city_rows, prov_rows, 0, "全部", "", owner_city_length, owner_province_length))
    else:
        if contain_whole:
            result_list.append(build_oa_model(city_rows, prov_rows, serverpart_id, "全部", "", owner_city_length, owner_province_length))
        sp_name = city_rows[0].get("SERVERPART_NAME", "") if city_rows else ""
        for region in regions_order:
            r_city = [r for r in city_rows if r.get("SERVERPART_REGION") == region]
            r_prov = [r for r in prov_rows if r.get("SERVERPART_REGION") == region]
            if r_city or r_prov:
                result_list.append(build_oa_model(r_city, r_prov, serverpart_id, sp_name, region, owner_city_length, owner_province_length))
    return result_list, ["小型车", "大型车"]


# ===== 4. GetBayonetProvinceOAList =====
def get_bayonet_province_oa_list(db: DatabaseHelper, statistics_month, serverpart_id, serverpart_region,
                                  owner_city_length, contain_whole, is_exclude) -> tuple[list[dict], list]:
    """获取车辆省份地市归属地分析"""
    from datetime import datetime as dt
    import calendar
    sm = statistics_month or dt.now().strftime("%Y%m")
    if sm == dt.now().strftime("%Y%m"):
        cur_days = (dt.now().day - 1) or 1
    else:
        year, month = int(sm[:4]), int(sm[4:6])
        cur_days = calendar.monthrange(year, month)[1]

    conditions = [f'A."STATISTICS_MONTH" = :sm']
    params = {"sm": int(sm)}
    if serverpart_id:
        conditions.append('A."SERVERPART_ID" = :spid'); params["spid"] = serverpart_id
    else:
        conditions.append('A."SERVERPART_ID" = 0')
    if serverpart_region:
        conditions.append('A."SERVERPART_REGION" = :region'); params["region"] = serverpart_region
    conditions.append('A."VEHICLE_TYPE" IS NULL')
    where = " AND ".join(conditions)

    prov_sql = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
            A."PROVINCE_NAME", A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
        FROM "T_BAYONETPROVINCEMONTH_AH" A WHERE {where}"""
    prov_rows = db.execute_query(prov_sql, params)

    city_sql = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
            B."CITY_NAME", B."PROVINCE_NAME",
            A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
        FROM "T_BAYONETOWNERMONTH_AH" A, "T_VEHICLEOWNER" B
        WHERE A."LICENSE_PLATE" = B."LICENSE_PLATE" AND {where}"""
    city_rows = db.execute_query(city_sql, params)

    regions_order = ["东", "南", "西", "北"]
    result_list = []
    if not serverpart_id:
        result_list.append(build_province_oa_model(city_rows, prov_rows, 0, "全部", "", owner_city_length, is_exclude))
    else:
        if contain_whole:
            result_list.append(build_province_oa_model(city_rows, prov_rows, serverpart_id, "全部", "", owner_city_length, is_exclude))
        sp_name = prov_rows[0].get("SERVERPART_NAME", "") if prov_rows else ""
        for region in regions_order:
            r_city = [r for r in city_rows if r.get("SERVERPART_REGION") == region]
            r_prov = [r for r in prov_rows if r.get("SERVERPART_REGION") == region]
            if r_city or r_prov:
                result_list.append(build_province_oa_model(r_city, r_prov, serverpart_id, sp_name, region, owner_city_length, is_exclude))
    return result_list, ["小型车", "大型车", None, None]


# ===== 5. GetSPBayonetList =====
def get_sp_bayonet_list(db: DatabaseHelper, statistics_date, province_code, sp_region_type_id,
                        serverpart_id, serverpart_region, show_growth_rate, group_type) -> list[dict]:
    """获取服务区车流量分析"""
    from datetime import datetime as dt
    from dateutil.relativedelta import relativedelta

    if province_code and province_code != "340000":
        return []
    if not statistics_date:
        return None  # 调用方判断返回错误

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    if group_type == 2:
        start_date = stat_date.replace(day=1)
    elif group_type == 3:
        start_date = stat_date.replace(month=1, day=1)
    else:
        start_date = stat_date

    start_str = start_date.strftime("%Y%m%d")
    end_str = stat_date.strftime("%Y%m%d")

    # --- SQL 参数化: 片区 + 方位条件 ---
    where_sql = ""
    if _sp_ids:
        # f-string: 安全 — build_in_condition 已通过 int() 转换
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        srt_ids = parse_multi_ids(sp_region_type_id)
        if srt_ids:
            where_sql += ' AND ' + build_in_condition('SPREGIONTYPE_ID', srt_ids).replace('"SPREGIONTYPE_ID"', 'B."SPREGIONTYPE_ID"')
    if serverpart_region:
        # serverpart_region 通过筛选安全值防注入
        safe_regions = [r.strip() for r in serverpart_region.split(',') if r.strip() in ('东', '南', '西', '北')]
        if safe_regions:
            regions = ','.join([f"'{r}'" for r in safe_regions])
            where_sql += f' AND A."SERVERPART_REGION" IN ({regions})'

    field_sql = "" if show_growth_rate else ',A."SERVERPART_REGION"'

    result_list = []

    if show_growth_rate and not serverpart_id:
        # 汇总模式
        sql = f"""SELECT SUM(A."VEHICLE_COUNT") AS "VEHICLE_COUNT",
                SUM(C."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
                SUM(CASE WHEN A."VEHICLE_TYPE" = '小型车' THEN A."VEHICLE_COUNT" END) AS "MINVEHICLE_COUNT",
                SUM(CASE WHEN A."VEHICLE_TYPE" = '中型车' THEN A."VEHICLE_COUNT" END) AS "MEDIUMVEHICLE_COUNT",
                SUM(CASE WHEN A."VEHICLE_TYPE" = '大型车' THEN A."VEHICLE_COUNT" END) AS "LARGEVEHICLE_COUNT"
            FROM "T_BAYONETDAILY_AH" A, "T_SERVERPART" B, "T_SECTIONFLOW" C
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."SERVERPART_ID" = C."SERVERPART_ID"
                AND A."SERVERPART_REGION" = C."SERVERPART_REGION"
                AND A."STATISTICS_DATE" = C."STATISTICS_DATE"
                AND A."VEHICLE_COUNT" > 0 AND C."SECTIONFLOW_NUM" > 0
                AND A."INOUT_TYPE" = 0
                AND A."STATISTICS_DATE" >= {start_str} AND A."STATISTICS_DATE" <= {end_str}{where_sql}"""
        rows = db.execute_query(sql) or []

        lm_start = (start_date - relativedelta(months=1)).strftime("%Y%m%d")
        lm_end = (stat_date - relativedelta(months=1)).strftime("%Y%m%d")
        sql_lm = sql.replace(f">= {start_str}", f">= {lm_start}").replace(f"<= {end_str}", f"<= {lm_end}")
        rows_lm = db.execute_query(sql_lm) or []

        if rows and rows[0].get("VEHICLE_COUNT"):
            r = rows[0]
            vc = _sf(r.get("VEHICLE_COUNT")); sf = _sf(r.get("SECTIONFLOW_NUM"))
            item = {
                "SPRegionType_Id": None, "SPRegionType_Index": None, "SPRegionType_Name": None,
                "Serverpart_ID": None, "Serverpart_Index": None, "Serverpart_Name": None, "Serverpart_Region": None,
                "Vehicle_Count": vc, "MinVehicle_Count": _sf(r.get("MINVEHICLE_COUNT")),
                "MediumVehicle_Count": _sf(r.get("MEDIUMVEHICLE_COUNT")),
                "LargeVehicle_Count": _sf(r.get("LARGEVEHICLE_COUNT")),
                "SectionFlow_Count": sf,
                "Entry_Rate": round(vc / sf * 100, 2) if sf > 0 else None,
                "MinVehicleEntry_Rate": None, "MediumVehicleEntry_Rate": None, "LargeVehicleEntry_Rate": None,
                "Entry_GrowthRate": None, "MinVehicleEntry_GrowthRate": None,
                "MediumVehicleEntry_GrowthRate": None, "LargeVehicleEntry_GrowthRate": None,
            }
            if sf > 0:
                if item["MinVehicle_Count"]: item["MinVehicleEntry_Rate"] = round(item["MinVehicle_Count"] / sf * 100, 2)
                if item["MediumVehicle_Count"]: item["MediumVehicleEntry_Rate"] = round(item["MediumVehicle_Count"] / sf * 100, 2)
                if item["LargeVehicle_Count"]: item["LargeVehicleEntry_Rate"] = round(item["LargeVehicle_Count"] / sf * 100, 2)
            if rows_lm and rows_lm[0].get("VEHICLE_COUNT"):
                rl = rows_lm[0]; lsf = _sf(rl.get("SECTIONFLOW_NUM"))
                if lsf > 0 and item["Entry_Rate"]:
                    last_rate = round(_sf(rl.get("VEHICLE_COUNT")) / lsf * 100, 2)
                    item["Entry_GrowthRate"] = round(item["Entry_Rate"] - last_rate, 2)
            result_list.append(item)
    else:
        # 按服务区分组模式
        bayonet_sql = f"""SELECT
                B."SPREGIONTYPE_ID", B."SPREGIONTYPE_INDEX", B."SPREGIONTYPE_NAME",
                B."SERVERPART_ID", B."SERVERPART_INDEX", B."SERVERPART_NAME"{field_sql},
                SUM(CASE WHEN A."VEHICLE_TYPE" = '小型车' THEN A."VEHICLE_COUNT" ELSE 0 END) AS "MINVEHICLE_COUNT",
                SUM(CASE WHEN A."VEHICLE_TYPE" = '中型车' THEN A."VEHICLE_COUNT" ELSE 0 END) AS "MEDIUMVEHICLE_COUNT",
                SUM(CASE WHEN A."VEHICLE_TYPE" = '大型车' THEN A."VEHICLE_COUNT" ELSE 0 END) AS "LARGEVEHICLE_COUNT"
            FROM "T_BAYONETDAILY_AH" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."STATISTICS_DATE" >= {start_str} AND A."STATISTICS_DATE" <= {end_str}{where_sql}
            GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_INDEX", B."SPREGIONTYPE_NAME",
                B."SERVERPART_ID", B."SERVERPART_INDEX", B."SERVERPART_NAME"{field_sql}"""
        dt_bayonet = db.execute_query(bayonet_sql) or []

        sf_sql = f"""SELECT B."SERVERPART_ID"{field_sql}, SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
            FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."STATISTICS_DATE" >= {start_str} AND A."STATISTICS_DATE" <= {end_str}{where_sql}
            GROUP BY B."SERVERPART_ID"{field_sql}"""
        dt_sf = db.execute_query(sf_sql) or []
        sf_map = {}
        for s in dt_sf:
            key = (s["SERVERPART_ID"], s.get("SERVERPART_REGION", ""))
            sf_map[key] = _sf(s.get("SECTIONFLOW_NUM"))

        lm_bayonet_map, lm_sf_map = {}, {}
        if show_growth_rate:
            lm_start = (start_date - relativedelta(months=1)).strftime("%Y%m%d")
            lm_end = (stat_date - relativedelta(months=1)).strftime("%Y%m%d")
            lm_b_sql = bayonet_sql.replace(f">= {start_str}", f">= {lm_start}").replace(f"<= {end_str}", f"<= {lm_end}")
            for lb in (db.execute_query(lm_b_sql) or []):
                lm_bayonet_map[(lb["SERVERPART_ID"], lb.get("SERVERPART_REGION", ""))] = lb
            lm_sf_sql = sf_sql.replace(f">= {start_str}", f">= {lm_start}").replace(f"<= {end_str}", f"<= {lm_end}")
            for ls in (db.execute_query(lm_sf_sql) or []):
                lm_sf_map[(ls["SERVERPART_ID"], ls.get("SERVERPART_REGION", ""))] = _sf(ls.get("SECTIONFLOW_NUM"))

        for r in dt_bayonet:
            sp_id = r["SERVERPART_ID"]
            region = r.get("SERVERPART_REGION", "")
            key = (sp_id, region)
            vc_min = _sf(r.get("MINVEHICLE_COUNT")); vc_med = _sf(r.get("MEDIUMVEHICLE_COUNT")); vc_lrg = _sf(r.get("LARGEVEHICLE_COUNT"))
            vc = vc_min + vc_med + vc_lrg; sf = sf_map.get(key, 0)
            item = {
                "SPRegionType_Id": r.get("SPREGIONTYPE_ID"), "SPRegionType_Index": r.get("SPREGIONTYPE_INDEX"),
                "SPRegionType_Name": r.get("SPREGIONTYPE_NAME"),
                "Serverpart_ID": sp_id, "Serverpart_Index": r.get("SERVERPART_INDEX"),
                "Serverpart_Name": r.get("SERVERPART_NAME"),
                "Serverpart_Region": region if not show_growth_rate else None,
                "Vehicle_Count": vc, "MinVehicle_Count": vc_min,
                "MediumVehicle_Count": vc_med, "LargeVehicle_Count": vc_lrg,
                "SectionFlow_Count": sf,
                "Entry_Rate": round(vc / sf * 100, 2) if sf > 0 else None,
                "MinVehicleEntry_Rate": round(vc_min / sf * 100, 2) if sf > 0 and vc_min > 0 else None,
                "MediumVehicleEntry_Rate": round(vc_med / sf * 100, 2) if sf > 0 and vc_med > 0 else None,
                "LargeVehicleEntry_Rate": round(vc_lrg / sf * 100, 2) if sf > 0 and vc_lrg > 0 else None,
                "Entry_GrowthRate": None, "MinVehicleEntry_GrowthRate": None,
                "MediumVehicleEntry_GrowthRate": None, "LargeVehicleEntry_GrowthRate": None,
            }
            if show_growth_rate and sf > 0:
                lb = lm_bayonet_map.get(key); lsf = lm_sf_map.get(key, 0)
                if lb and lsf > 0:
                    l_vc = _sf(lb.get("MINVEHICLE_COUNT")) + _sf(lb.get("MEDIUMVEHICLE_COUNT")) + _sf(lb.get("LARGEVEHICLE_COUNT"))
                    l_rate = round(l_vc / lsf * 100, 2)
                    item["Entry_GrowthRate"] = round(item["Entry_Rate"] - l_rate, 2) if item["Entry_Rate"] else None
            result_list.append(item)

    return result_list


# ===== 6. GetBayonetRankList — 直接在 Router 中复用 get_sp_bayonet_list =====
# (不需要单独的 Service 方法，Router 层调用 get_sp_bayonet_list 后排序即可)


# ===== 7. GetAvgBayonetAnalysis =====
def get_avg_bayonet_analysis(db: DatabaseHelper, statistics_date, province_code, sp_region_type_id,
                              serverpart_id, serverpart_region) -> Optional[dict]:
    """获取服务区平均车流量分析"""
    from datetime import datetime as dt

    if province_code and province_code != "340000":
        return None
    if not statistics_date:
        return None

    where_sql = ""
    if not serverpart_id and not sp_region_type_id:
        date_str = statistics_date.replace("-", "")
        if len(date_str) == 6:
            sql = f"""SELECT ROUND(AVG("SERVERPART_FLOW"),0) AS "SERVERPART_FLOW",
                    ROUND(AVG("AVGENTRY_RATE"),2) AS "AVGENTRY_RATE",
                    ROUND(AVG("AVGSTAY_TIMES"),2) AS "AVGSTAY_TIMES"
                FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" = 0
                    AND "STATISTICS_DATE" >= {date_str}01 AND "STATISTICS_DATE" <= {date_str}31"""
        else:
            sql = f'SELECT * FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" = 0 AND "STATISTICS_DATE" = {date_str}'
        rows = db.execute_query(sql) or []
        if rows and rows[0].get("SERVERPART_FLOW"):
            r = rows[0]
            return {"Vehicle_Count": _sf(r.get("SERVERPART_FLOW")),
                    "Entry_Rate": _sf(r.get("AVGENTRY_RATE")), "Stay_Times": _sf(r.get("AVGSTAY_TIMES"))}
        return None

    # --- SQL 参数化: 片区 + 方位条件 ---
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        # f-string: 安全 — build_in_condition 已通过 int() 转换
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'C."SERVERPART_ID"')
    elif sp_region_type_id:
        srt_ids = parse_multi_ids(sp_region_type_id)
        if srt_ids:
            where_sql += ' AND ' + build_in_condition('SPREGIONTYPE_ID', srt_ids).replace('"SPREGIONTYPE_ID"', 'C."SPREGIONTYPE_ID"')
    if serverpart_region:
        safe_regions = [r.strip() for r in serverpart_region.split(',') if r.strip() in ('东', '南', '西', '北')]
        if safe_regions:
            regions = ','.join([f"'{r}'" for r in safe_regions])
            where_sql += f' AND A."SERVERPART_REGION" IN ({regions})'

    stat_str = dt.strptime(statistics_date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in statistics_date else statistics_date

    sql = f"""SELECT A."SERVERPART_ID", A."SERVERPART_REGION", B."SECTIONFLOW_NUM",
            SUM(A."VEHICLE_COUNT") AS "VEHICLE_COUNT"
        FROM "T_BAYONETDAILY_AH" A, "T_SECTIONFLOW" B, "T_SERVERPART" C
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND B."SERVERPART_ID" = C."SERVERPART_ID"
            AND A."SERVERPART_REGION" = B."SERVERPART_REGION"
            AND A."STATISTICS_DATE" = B."STATISTICS_DATE"
            AND A."VEHICLE_COUNT" > 0 AND B."SECTIONFLOW_NUM" > 0
            AND A."INOUT_TYPE" = 0 AND A."STATISTICS_DATE" = {stat_str}{where_sql}
        GROUP BY A."SERVERPART_ID", A."SERVERPART_REGION", B."SECTIONFLOW_NUM" """
    rows = db.execute_query(sql) or []
    if not rows:
        return None

    from collections import defaultdict
    sp_groups = defaultdict(lambda: {"vc": 0, "sf": 0})
    for r in rows:
        sp_id = r["SERVERPART_ID"]
        sp_groups[sp_id]["vc"] += _sf(r.get("VEHICLE_COUNT"))
        sp_groups[sp_id]["sf"] += _sf(r.get("SECTIONFLOW_NUM"))

    rates, vcs = [], []
    for sp_id, g in sp_groups.items():
        vcs.append(g["vc"])
        if g["sf"] > 0: rates.append(round(g["vc"] / g["sf"] * 100, 2))

    avg_vc = round(sum(vcs) / len(vcs)) if vcs else 0
    avg_rate = round(sum(rates) / len(rates), 2) if rates else 0

    sta_sql = f"""SELECT A."SERVERPART_ID", ROUND(SUM(A."STAY_TIMES") / SUM(A."STAY_TIMESCOUNT"), 2) AS "AVGSTAY_TIMES"
        FROM "T_BAYONETDAILY_AH" A, "T_SERVERPART" C
        WHERE A."SERVERPART_ID" = C."SERVERPART_ID" AND A."STAY_TIMESCOUNT" > 0
            AND A."INOUT_TYPE" = 0 AND A."STATISTICS_DATE" = {stat_str}{where_sql}
        GROUP BY A."SERVERPART_ID" """
    sta_rows = db.execute_query(sta_sql) or []
    avg_stay = 0
    if sta_rows:
        stay_vals = [_sf(r.get("AVGSTAY_TIMES")) for r in sta_rows if _sf(r.get("AVGSTAY_TIMES")) > 0]
        if stay_vals: avg_stay = round(sum(stay_vals) / len(stay_vals) / 60, 2)

    return {"Vehicle_Count": avg_vc, "Entry_Rate": avg_rate, "Stay_Times": avg_stay}


# ===== 8. GetProvinceAvgBayonetAnalysis =====
def get_province_avg_bayonet_analysis(db: DatabaseHelper, province_code, statistics_date) -> list[dict]:
    """获取全省平均车流量分析"""
    from datetime import datetime as dt
    from dateutil.relativedelta import relativedelta

    if province_code != "340000":
        return []
    if not statistics_date:
        return []

    is_month = len(statistics_date) == 6
    if is_month:
        cur_month = statistics_date
        last_month = (dt.strptime(statistics_date + "01", "%Y%m%d") - relativedelta(months=1)).strftime("%Y%m")
        last_year = (dt.strptime(statistics_date + "01", "%Y%m%d") - relativedelta(years=1)).strftime("%Y%m")
    else:
        stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
        cur_month = stat_date.strftime("%Y%m%d")
        last_month = (stat_date - relativedelta(months=1)).strftime("%Y%m")
        last_year = (stat_date - relativedelta(years=1)).strftime("%Y%m")

    if is_month:
        months_in = f"{cur_month},{last_month},{last_year}"
        flow_sql = f"""SELECT SUM("SECTIONFLOW_NUM") AS "SUM_SECTIONFLOW_NUM",
                SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SUM_SERVERPART_FLOW",
                SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
            FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" <> 0 AND SUBSTR("STATISTICS_DATE",1,6) IN ({months_in})
            GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""
        avg_sql = f"""SELECT ROUND(AVG("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)),0) AS "SERVERPART_FLOW",
                ROUND(AVG("AVGENTRY_RATE"),2) AS "AVGENTRY_RATE",
                ROUND(AVG("AVGSTAY_TIMES"),2) AS "AVGSTAY_TIMES",
                SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
            FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" = 0 AND SUBSTR("STATISTICS_DATE",1,6) IN ({months_in})
            GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""
    else:
        month_start = stat_date.strftime("%Y%m01")
        lm_end = last_month + cur_month[6:8]
        ly_end = last_year + cur_month[6:8]
        flow_sql = f"""SELECT SUM("SECTIONFLOW_NUM") AS "SUM_SECTIONFLOW_NUM",
                SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SUM_SERVERPART_FLOW",
                '{cur_month}' AS "STATISTICS_DATE"
            FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" <> 0 AND "STATISTICS_DATE" BETWEEN {month_start} AND {cur_month}
            UNION ALL
            SELECT SUM("SECTIONFLOW_NUM"), SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)),
                SUBSTR("STATISTICS_DATE",1,6) FROM "T_SECTIONFLOW"
            WHERE "SERVERPART_ID" <> 0 AND "STATISTICS_DATE" BETWEEN {last_month}01 AND {lm_end}
            GROUP BY SUBSTR("STATISTICS_DATE",1,6)
            UNION ALL
            SELECT SUM("SECTIONFLOW_NUM"), SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)),
                SUBSTR("STATISTICS_DATE",1,6) FROM "T_SECTIONFLOW"
            WHERE "SERVERPART_ID" <> 0 AND "STATISTICS_DATE" BETWEEN {last_year}01 AND {ly_end}
            GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""
        avg_sql = f"""SELECT ROUND(AVG("SERVERPART_FLOW"),0) AS "SERVERPART_FLOW",
                ROUND(AVG("AVGENTRY_RATE"),2) AS "AVGENTRY_RATE",
                ROUND(AVG("AVGSTAY_TIMES"),2) AS "AVGSTAY_TIMES",
                '{cur_month}' AS "STATISTICS_DATE"
            FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" = 0
                AND "STATISTICS_DATE" >= {month_start} AND "STATISTICS_DATE" <= {cur_month}
            UNION ALL
            SELECT ROUND(AVG("SERVERPART_FLOW"),0), ROUND(AVG("AVGENTRY_RATE"),2),
                ROUND(AVG("AVGSTAY_TIMES"),2), SUBSTR("STATISTICS_DATE",1,6)
            FROM "T_SECTIONFLOW" WHERE "SERVERPART_ID" = 0
                AND SUBSTR("STATISTICS_DATE",1,6) IN ({last_month},{last_year})
            GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""

    flow_rows = db.execute_query(flow_sql) or []
    avg_rows = db.execute_query(avg_sql) or []
    avg_rows.sort(key=lambda r: str(r.get("STATISTICS_DATE", "")), reverse=True)

    flow_map = {}
    for r in flow_rows:
        sd = str(r.get("STATISTICS_DATE", ""))
        flow_map[sd] = {"sf": _sf(r.get("SUM_SECTIONFLOW_NUM")), "spf": _sf(r.get("SUM_SERVERPART_FLOW"))}

    cur_avg = next((r for r in avg_rows if str(r.get("STATISTICS_DATE", "")) == str(cur_month)), None)
    cur_entry = _sf(cur_avg.get("AVGENTRY_RATE")) if cur_avg else 0
    cur_stay = _sf(cur_avg.get("AVGSTAY_TIMES")) if cur_avg else 0
    cur_spf = flow_map.get(str(cur_month), {}).get("spf", 0)


# ===== 9. GetBayonetSTAnalysis =====
def get_bayonet_st_analysis(db: DatabaseHelper, start_month, end_month, province_code,
                             sp_region_type_id, serverpart_id, time_span) -> list[dict]:
    """获取服务区车辆时段停留时长分析"""
    import math
    group_parts = []
    for i in range(0, math.ceil(24 / time_span)):
        start_h = i * time_span; end_h = (i + 1) * time_span
        if i == 0:
            group_parts.append(f'CASE WHEN "STATISTICS_HOUR" >= 0 AND "STATISTICS_HOUR" < {end_h} THEN {i}')
        elif end_h >= 24:
            group_parts.append(f' WHEN "STATISTICS_HOUR" >= {start_h} AND "STATISTICS_HOUR" < 24 THEN {i} END')
        else:
            group_parts.append(f' WHEN "STATISTICS_HOUR" >= {start_h} AND "STATISTICS_HOUR" < {end_h} THEN {i}')
    group_field = "".join(group_parts)

    conditions = ['A."SERVERPART_ID" = B."SERVERPART_ID"', 'A."INOUT_TYPE" = 0', 'A."DATA_TYPE" IN (0,1)']
    params = []
    if start_month: conditions.append('A."STATISTICS_MONTH" >= ?'); params.append(int(start_month.replace("-", "")))
    if end_month: conditions.append('A."STATISTICS_MONTH" <= ?'); params.append(int(end_month.replace("-", "")))
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"'))
    elif sp_region_type_id:
        srt_ids = parse_multi_ids(sp_region_type_id)
        if srt_ids:
            conditions.append(build_in_condition('SPREGIONTYPE_ID', srt_ids).replace('"SPREGIONTYPE_ID"', 'B."SPREGIONTYPE_ID"'))

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A."VEHICLE_TYPE", {group_field} AS "STATISTICS_HOUR",
        ROUND(AVG(A."STAY_TIMES" / NULLIF(A."STATISTICS_DAYS", 0)), 2) AS "STAY_TIMES",
        SUM(A."STAY_TIMESTOTAL") AS "STAY_TIMESTOTAL", SUM(A."STAY_TIMESCOUNT") AS "STAY_TIMESCOUNT"
    FROM "T_BAYONETHOURMONTH_AH" A, "T_SERVERPART" B WHERE {where_sql}
    GROUP BY A."VEHICLE_TYPE", {group_field}"""
    rows = db.execute_query(sql, params)

    vehicle_types = ["小型车", "中型车", "大型车"]
    result_list = []
    num_slots = math.ceil(24 / time_span)
    for vt in vehicle_types:
        vt_rows = [r for r in rows if r.get("VEHICLE_TYPE") == vt]
        if not vt_rows: continue
        data = []
        for slot in range(num_slots):
            out_time = float(min(slot * time_span, 24))
            slot_row = next((r for r in vt_rows if r.get("STATISTICS_HOUR") == slot), None)
            stay = 0
            if slot_row:
                count = int(slot_row.get("STAY_TIMESCOUNT") or 0)
                if count > 0: stay = round(float(slot_row.get("STAY_TIMESTOTAL") or 0) / count / 3600, 2)
                else: stay = round(float(slot_row.get("STAY_TIMES") or 0) / 3600, 2)
            data.append([out_time, stay])
        result_list.append({"name": vt, "data": data, "value": None, "CommonScatterList": None})
    return result_list
