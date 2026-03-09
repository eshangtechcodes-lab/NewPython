# -*- coding: utf-8 -*-
"""
CommercialApi - BigData 路由
对应原 CommercialApi/Controllers/BigDataController.cs
大数据分析相关接口（车流分析、归属地分析、预警等）
注意：原 Controller 1503行，34个接口，此处按方法签名完整定义路由
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
# from core.old_api_proxy import proxy_to_old_api  # 已全部完成SQL平移，不再需要代理
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


def date_no_pad(d, fmt="ymd"):
    """C# DateTime.ToString("yyyy/M/d") 不补零。Python Windows不支持%-m"""
    if fmt == "ymd":
        return f"{d.year}/{d.month}/{d.day}"
    elif fmt == "ymd_hms":
        return f"{d.year}/{d.month}/{d.day} {d.hour}:{d.minute:02d}:{d.second:02d}"
    return f"{d.year}/{d.month}/{d.day}"


def _build_sta_model(rows, vehicle_types, sp_id, sp_name, region):
    """构建车辆停留时长分析模型（按方位聚合）"""
    vc_list = []
    st_list = []
    valid_types = []
    for vt in vehicle_types:
        vt_rows = [r for r in rows if r.get("VEHICLE_TYPE") == vt]
        if not vt_rows:
            continue
        valid_types.append(vt)
        # 统计天数
        dates = set(r.get("STATISTICS_DATE") for r in vt_rows)
        total_days = max(len(dates), 1)
        # 日均车流量 = 总车流/天数
        total_vc = sum(r.get("VEHICLE_COUNT") or 0 for r in vt_rows)
        avg_vc = int(total_vc / total_days)
        vc_list.append({"name": vt, "value": str(avg_vc)})
        # 平均停留时长 = 总停留时长/记录条数/60
        total_st_count = sum(int(r.get("STAY_TIMESCOUNT") or 0) for r in vt_rows)
        if total_st_count > 0:
            total_st = sum(float(r.get("STAY_TIMES") or 0) for r in vt_rows)
            avg_st = total_st / total_st_count / 60
        else:
            avg_st = 0
        st_list.append({"name": vt, "value": f"{avg_st:.2f}"})

    return {
        "Serverpart_ID": sp_id,
        "Serverpart_Name": sp_name,
        "Serverpart_Region": region,
        "Vehicle_Type": valid_types,
        "VehicleCountList": vc_list,
        "StayTimesList": st_list,
    }


def _build_oa_model(city_rows, prov_rows, sp_id, sp_name, region, city_top, prov_top):
    """构建车辆归属地分析模型（城市Top-N + 省份Top-N）"""
    # 城市聚合
    city_map = {}
    for r in city_rows:
        cn = r.get("CITY_NAME") or ""
        city_map[cn] = city_map.get(cn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    city_sorted = sorted(city_map.items(), key=lambda x: x[1], reverse=True)[:city_top]
    city_list = [{"name": c[0], "value": str(int(c[1]))} for c in city_sorted]

    # 省份聚合
    prov_map = {}
    for r in prov_rows:
        pn = r.get("PROVINCE_NAME") or ""
        prov_map[pn] = prov_map.get(pn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    prov_sorted_all = sorted(prov_map.items(), key=lambda x: x[1], reverse=True)
    prov_sorted = prov_sorted_all[:prov_top]
    prov_list = [{"name": p[0], "value": str(int(p[1]))} for p in prov_sorted]
    # 追加"其他"汇总（C#逻辑：topN之外的省份归入"其他"）
    if len(prov_sorted_all) > prov_top:
        other_count = sum(p[1] for p in prov_sorted_all[prov_top:])
        prov_list.append({"name": "其他", "value": str(int(other_count))})

    total_vc = sum(float(r.get("VEHICLE_COUNT") or 0) for r in city_rows)
    return {
        "Serverpart_ID": sp_id,
        "Serverpart_Name": sp_name,
        "Serverpart_Region": region,
        "OwnerCity": [c[0] for c in city_sorted],
        "OwnerProvince": [p[0] for p in prov_sorted] + (["其他"] if len(prov_sorted_all) > prov_top else []),
        "Vehicle_Count": int(total_vc),
        "OwnerCityList": city_list if city_list else [{"name": None, "value": None}],
        "OwnerProvinceList": prov_list,
    }


def _build_province_oa_model(city_rows, prov_rows, sp_id, sp_name, region, city_top, is_exclude, prov_top=0):
    """构建省份归属地分析模型（省份->城市嵌套）
    prov_top: 显示省份数量。C#的ProvinceOAList传0，所以所有省份都归为"其他"
    """
    # 省份聚合
    prov_map = {}
    for r in prov_rows:
        pn = r.get("PROVINCE_NAME") or ""
        prov_map[pn] = prov_map.get(pn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    prov_sorted = sorted(prov_map.items(), key=lambda x: x[1], reverse=True)

    total_vc = sum(float(r.get("VEHICLE_COUNT") or 0) for r in prov_rows)
    # 城市归属表的总数
    city_total = sum(float(r.get("VEHICLE_COUNT") or 0) for r in city_rows)
    # Vehicle_Count取city_total和prov总的最大值（与C#一致）
    vehicle_count = int(max(total_vc, city_total))

    prov_list = []
    other_count = vehicle_count
    if prov_top > 0:
        # 正常展示省份明细
        show_provs = prov_sorted[:prov_top]
        for pn, pv in show_provs:
            p_cities = {}
            for r in city_rows:
                if r.get("PROVINCE_NAME") == pn:
                    cn = r.get("CITY_NAME") or ""
                    p_cities[cn] = p_cities.get(cn, 0) + float(r.get("VEHICLE_COUNT") or 0)
            city_sorted = sorted(p_cities.items(), key=lambda x: x[1], reverse=True)[:city_top]
            _cities = [{"name": c[0], "value": str(int(c[1]))} for c in city_sorted]
            prov_list.append({"name": pn, "value": str(int(pv))})
            other_count -= int(pv)
    # 剩余归为"其他"
    if other_count > 0:
        prov_list.append({"name": "其他", "value": str(other_count)})

    owner_province = [p["name"] for p in prov_list]

    # 顶层城市列表
    city_map = {}
    for r in city_rows:
        cn = r.get("CITY_NAME") or ""
        city_map[cn] = city_map.get(cn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    city_sorted_top = sorted(city_map.items(), key=lambda x: x[1], reverse=True)[:city_top]
    top_city_list = [{"name": c[0], "value": str(int(c[1]))} for c in city_sorted_top]
    if not top_city_list:
        top_city_list = [{"name": None, "value": None}]
    return {
        "Serverpart_ID": sp_id,
        "Serverpart_Name": sp_name,
        "Serverpart_Region": region,
        "OwnerCity": [c[0] for c in city_sorted_top],
        "OwnerProvince": owner_province,
        "Vehicle_Count": vehicle_count,
        "OwnerProvinceList": prov_list,
        "OwnerCityList": top_city_list,
    }


@router.get("/Revenue/GetBayonetEntryList")
async def get_bayonet_entry_list(
    StatisticsDate: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowAddUpCount: bool = Query(False, description="是否统计累计数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """服务区入区车流分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        if not StatisticsDate:
            StatisticsDate = dt.now().strftime("%Y-%m-%d")
        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        date_str = stat_date.strftime("%Y%m%d")
        ydate_str = (stat_date - timedelta(days=1)).strftime("%Y%m%d")

        where_sql = ""
        if Serverpart_ID is not None:
            where_sql += f' AND "SERVERPART_ID" = {Serverpart_ID}'
        if Serverpart_Region:
            where_sql += f" AND \"SERVERPART_REGION\" = '{Serverpart_Region}'"

        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        # 1. 今日入区车流
        if Serverpart_ID is not None:
            iv_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
                FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = {date_str}{where_sql}
                GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
        else:
            iv_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
                FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = {date_str}{where_sql}"""
        dt_in = db.execute_query(iv_sql) or []

        # 2. 今日断面流量
        if Serverpart_ID is not None:
            sf_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","SERVERPART_NAME",
                    "SECTIONFLOW_NUM","SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0) AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = {date_str}{where_sql}"""
        else:
            sf_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION",'' AS "SERVERPART_NAME",
                    SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
                    SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = {date_str}{where_sql}"""
        dt_sf = db.execute_query(sf_sql) or []

        # 3. 昨日入区车流
        if Serverpart_ID is not None:
            ivy_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
                FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = {ydate_str}{where_sql}
                GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
        else:
            ivy_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION", SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT"
                FROM "T_BAYONETDAILY_AH" WHERE "INOUT_TYPE" = 0 AND "STATISTICS_DATE" = {ydate_str}{where_sql}"""
        dt_in_y = db.execute_query(ivy_sql) or []

        # 4. 昨日断面流量
        if Serverpart_ID is not None:
            sfy_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","SERVERPART_NAME",
                    "SECTIONFLOW_NUM","SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0) AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = {ydate_str}{where_sql}"""
        else:
            sfy_sql = f"""SELECT NULL AS "SERVERPART_ID",'' AS "SERVERPART_REGION",'' AS "SERVERPART_NAME",
                    SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
                    SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" WHERE "STATISTICS_DATE" = {ydate_str}{where_sql}"""
        dt_sf_y = db.execute_query(sfy_sql) or []

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
            sp_flow = safe_int(sf_row.get("SERVERPART_FLOW"))
            section_num = safe_int(sf_row.get("SECTIONFLOW_NUM"))
            # 入区车流量 = max(服务区流量, 卡口入区数)
            in_vc = safe_int(in_map.get(key, {}).get("VEHICLE_COUNT"))
            vc = max(sp_flow, in_vc)
            # 入区率
            entry_rate = round(vc / section_num * 100, 2) if section_num > 0 and vc > 0 else 0
            # 昨日比较
            vy = safe_int(in_y_map.get(key, {}).get("VEHICLE_COUNT"))
            sy = safe_int(sf_y_map.get(key, {}).get("SECTIONFLOW_NUM"))
            spy = safe_int(sf_y_map.get(key, {}).get("SERVERPART_FLOW"))
            vy = max(vy, spy)

            vg_rate = None
            eg_rate = None
            if vy > 0 and sy > 0:
                vg_rate = round((vc - vy) / vy * 100, 2)
                ey = round(vy / sy * 100, 2)
                eg_rate = round((entry_rate - ey) / ey * 100, 2) if ey > 0 else 100
            elif vy > 0:
                vg_rate = round((vc - vy) / vy * 100, 2)
                eg_rate = 100
            else:
                vg_rate = 100
                eg_rate = 100

            return {
                "Serverpart_ID": sf_row.get("SERVERPART_ID"),
                "Serverpart_Name": sf_row.get("SERVERPART_NAME", ""),
                "Serverpart_Region": sf_row.get("SERVERPART_REGION", ""),
                "Vehicle_Count": vc,
                "SectionFlow_Count": section_num,
                "Entry_Rate": entry_rate,
                "Vehicle_GrowthRate": vg_rate,
                "Entry_GrowthRate": eg_rate,
                "Stay_Times": None,
            }

        if Serverpart_ID is not None:
            # 按方位排序输出
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

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetEntryList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBayonetSTAList")
async def get_bayonet_sta_list(
    StatisticsDate: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ContainWhole: bool = Query(False, description="是否显示全服务区数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取车辆停留时长分析"""
    try:
        if not StatisticsDate:
            from datetime import datetime as dt
            StatisticsDate = dt.now().strftime("%Y-%m-%d")
        date_str = StatisticsDate.replace("-", "")
        month_start = date_str[:6] + "00"

        conditions = [f'"STATISTICS_DATE" >= {month_start}', f'"STATISTICS_DATE" <= {date_str}', '"INOUT_TYPE" = 0']
        params = {}
        if Serverpart_ID:
            conditions.append('"SERVERPART_ID" = :spid')
            params["spid"] = Serverpart_ID
        if Serverpart_Region:
            conditions.append('"SERVERPART_REGION" = :region')
            params["region"] = Serverpart_Region
        where = " AND ".join(conditions)

        if Serverpart_ID:
            # 有服务区内码：按方位分组
            sql = f"""SELECT SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT", "STATISTICS_DATE",
                    SUM("STAY_TIMES") AS "STAY_TIMES", SUM("STAY_TIMESCOUNT") AS "STAY_TIMESCOUNT",
                    "SERVERPART_ID", "SERVERPART_NAME", "SERVERPART_REGION", "VEHICLE_TYPE"
                FROM "T_BAYONETDAILY_AH" WHERE {where}
                GROUP BY "SERVERPART_ID", "SERVERPART_NAME", "SERVERPART_REGION", "VEHICLE_TYPE", "STATISTICS_DATE" """
            rows = db.execute_query(sql, params)
            # 过滤 VEHICLE_COUNT > 0
            rows = [r for r in rows if (r.get("VEHICLE_COUNT") or 0) > 0]

            vehicle_types = ["小型车", "中型车", "大型车"]
            regions_order = ["东", "南", "西", "北"]
            result_list = []

            # 获取存在的方位列表
            existing_regions = list(dict.fromkeys(r.get("SERVERPART_REGION", "") for r in rows))
            sp_name = rows[0].get("SERVERPART_NAME", "") if rows else ""

            # 是否显示全服务区汇总
            if ContainWhole:
                sta_model = _build_sta_model(rows, vehicle_types, Serverpart_ID, "全部", "")
                result_list.append(sta_model)

            # 按方位分组
            for region in regions_order:
                region_rows = [r for r in rows if r.get("SERVERPART_REGION") == region]
                if not region_rows:
                    continue
                sta_model = _build_sta_model(region_rows, vehicle_types, Serverpart_ID, sp_name, region)
                result_list.append(sta_model)
        else:
            # 没有服务区内码：全省聚合
            sql = f"""SELECT ROUND(SUM("VEHICLE_COUNT") / COUNT(DISTINCT "STATISTICS_DATE"), 0) AS "VEHICLE_COUNT",
                    CASE WHEN SUM("STAY_TIMESCOUNT") > 0
                        THEN ROUND(SUM("STAY_TIMES") / SUM("STAY_TIMESCOUNT"), 2) END AS "STAY_TIMES",
                    "SERVERPART_ID", "VEHICLE_TYPE"
                FROM "T_BAYONETDAILY_AH" WHERE "VEHICLE_COUNT" > 0 AND {where}
                GROUP BY "SERVERPART_ID", "VEHICLE_TYPE" """
            rows = db.execute_query(sql, params)

            vehicle_types = ["小型车", "中型车", "大型车"]
            vc_list = []
            st_list = []
            valid_types = []
            for vt in vehicle_types:
                vt_rows = [r for r in rows if r.get("VEHICLE_TYPE") == vt]
                if not vt_rows:
                    continue
                valid_types.append(vt)
                avg_vc = sum(r.get("VEHICLE_COUNT") or 0 for r in vt_rows) / max(len(vt_rows), 1)
                avg_st = sum(float(r.get("STAY_TIMES") or 0) for r in vt_rows) / max(len(vt_rows), 1) / 60
                vc_list.append({"name": vt, "value": str(int(avg_vc))})
                st_list.append({"name": vt, "value": f"{avg_st:.2f}"})

            result_list = [{
                "Vehicle_Type": valid_types,
                "VehicleCountList": vc_list,
                "StayTimesList": st_list,
            }]

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetSTAList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBayonetOAList")
async def get_bayonet_oa_list(
    StatisticsMonth: Optional[str] = Query(None, description="统计月份，格式yyyyMM"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    OwnerCityLength: int = Query(6, description="显示车牌所在城市数量"),
    OwnerProvinceLenth: int = Query(4, description="显示车牌所在省份数量"),
    ContainWhole: bool = Query(False, description="是否显示全服务区数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取车辆归属地分析"""
    try:
        from datetime import datetime as dt
        import calendar
        # 计算本月实际天数
        sm = StatisticsMonth or dt.now().strftime("%Y%m")
        if sm == dt.now().strftime("%Y%m"):
            cur_days = (dt.now().day - 1) or 1
        else:
            year, month = int(sm[:4]), int(sm[4:6])
            cur_days = calendar.monthrange(year, month)[1]

        conditions = [f'A."STATISTICS_MONTH" = :sm']
        params = {"sm": int(sm)}
        if Serverpart_ID:
            conditions.append('A."SERVERPART_ID" = :spid')
            params["spid"] = Serverpart_ID
        else:
            conditions.append('A."SERVERPART_ID" = 0')
        if Serverpart_Region:
            conditions.append('A."SERVERPART_REGION" = :region')
            params["region"] = Serverpart_Region
        conditions.append('A."VEHICLE_TYPE" IS NULL')
        where = " AND ".join(conditions)

        # 查城市归属地
        sql = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
                B."CITY_NAME", B."PROVINCE_NAME",
                A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
            FROM "T_BAYONETOWNERMONTH_AH" A, "T_VEHICLEOWNER" B
            WHERE A."LICENSE_PLATE" = B."LICENSE_PLATE" AND {where}"""
        city_rows = db.execute_query(sql, params)

        # 查省份归属地
        sql2 = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
                A."PROVINCE_NAME",
                A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
            FROM "T_BAYONETPROVINCEMONTH_AH" A
            WHERE {where}"""
        prov_rows = db.execute_query(sql2, params)

        regions_order = ["东", "南", "西", "北"]
        result_list = []

        if not Serverpart_ID:
            # 全省聚合
            oa = _build_oa_model(city_rows, prov_rows, 0, "全部", "", OwnerCityLength, OwnerProvinceLenth)
            result_list.append(oa)
        else:
            if ContainWhole:
                oa = _build_oa_model(city_rows, prov_rows, Serverpart_ID, "全部", "", OwnerCityLength, OwnerProvinceLenth)
                result_list.append(oa)
            sp_name = city_rows[0].get("SERVERPART_NAME", "") if city_rows else ""
            for region in regions_order:
                r_city = [r for r in city_rows if r.get("SERVERPART_REGION") == region]
                r_prov = [r for r in prov_rows if r.get("SERVERPART_REGION") == region]
                if not r_city and not r_prov:
                    continue
                oa = _build_oa_model(r_city, r_prov, Serverpart_ID, sp_name, region, OwnerCityLength, OwnerProvinceLenth)
                result_list.append(oa)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        resp = json_list.model_dump()
        resp["OtherData"] = ["小型车", "大型车"]
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetOAList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBayonetProvinceOAList")
async def get_bayonet_province_oa_list(
    StatisticsMonth: Optional[str] = Query(None, description="统计月份，格式yyyyMM"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    OwnerCityLength: int = Query(6, description="显示城市数量"),
    ContainWhole: bool = Query(False, description="是否显示全服务区数据"),
    isExclude: bool = Query(False, description="是否统计其他省份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取车辆省份地市归属地分析"""
    try:
        from datetime import datetime as dt
        import calendar
        sm = StatisticsMonth or dt.now().strftime("%Y%m")
        if sm == dt.now().strftime("%Y%m"):
            cur_days = (dt.now().day - 1) or 1
        else:
            year, month = int(sm[:4]), int(sm[4:6])
            cur_days = calendar.monthrange(year, month)[1]

        conditions = [f'A."STATISTICS_MONTH" = :sm']
        params = {"sm": int(sm)}
        if Serverpart_ID:
            conditions.append('A."SERVERPART_ID" = :spid')
            params["spid"] = Serverpart_ID
        else:
            conditions.append('A."SERVERPART_ID" = 0')
        if Serverpart_Region:
            conditions.append('A."SERVERPART_REGION" = :region')
            params["region"] = Serverpart_Region
        conditions.append('A."VEHICLE_TYPE" IS NULL')
        where = " AND ".join(conditions)

        # 查省份归属地
        sql = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
                A."PROVINCE_NAME",
                A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
            FROM "T_BAYONETPROVINCEMONTH_AH" A
            WHERE {where}"""
        prov_rows = db.execute_query(sql, params)

        # 查城市归属地（用于省内城市排名）
        city_conditions = conditions.copy()
        ci_where = " AND ".join(city_conditions)
        sql2 = f"""SELECT A."AVGVEHICLE_COUNT" * {cur_days} AS "VEHICLE_COUNT",
                B."CITY_NAME", B."PROVINCE_NAME",
                A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION"
            FROM "T_BAYONETOWNERMONTH_AH" A, "T_VEHICLEOWNER" B
            WHERE A."LICENSE_PLATE" = B."LICENSE_PLATE" AND {ci_where}"""
        city_rows = db.execute_query(sql2, params)

        regions_order = ["东", "南", "西", "北"]
        result_list = []

        if not Serverpart_ID:
            oa = _build_province_oa_model(city_rows, prov_rows, 0, "全部", "", OwnerCityLength, isExclude)
            result_list.append(oa)
        else:
            if ContainWhole:
                oa = _build_province_oa_model(city_rows, prov_rows, Serverpart_ID, "全部", "", OwnerCityLength, isExclude)
                result_list.append(oa)
            sp_name = prov_rows[0].get("SERVERPART_NAME", "") if prov_rows else ""
            for region in regions_order:
                r_city = [r for r in city_rows if r.get("SERVERPART_REGION") == region]
                r_prov = [r for r in prov_rows if r.get("SERVERPART_REGION") == region]
                if not r_city and not r_prov:
                    continue
                oa = _build_province_oa_model(r_city, r_prov, Serverpart_ID, sp_name, region, OwnerCityLength, isExclude)
                result_list.append(oa)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        resp = json_list.model_dump()
        resp["OtherData"] = ["小型车", "大型车", None, None]
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetProvinceOAList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetSPBayonetList")
async def get_sp_bayonet_list(
    Statistics_Date: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowGrowthRate: bool = Query(False, description="是否显示增长率"),
    GroupType: int = Query(1, description="统计方式：1当日 2当月 3当年"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车流量分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt
        from dateutil.relativedelta import relativedelta

        # 仅安徽有车流数据
        if Province_Code and Province_Code != "340000":
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        if not Statistics_Date:
            return Result.fail(code=200, msg="查询失败，请传入统计日期！")

        stat_date = dt.strptime(Statistics_Date, "%Y-%m-%d") if "-" in Statistics_Date else dt.strptime(Statistics_Date, "%Y%m%d")
        # 根据GroupType确定开始日期
        if GroupType == 2:
            start_date = stat_date.replace(day=1)
        elif GroupType == 3:
            start_date = stat_date.replace(month=1, day=1)
        else:
            start_date = stat_date

        start_str = start_date.strftime("%Y%m%d")
        end_str = stat_date.strftime("%Y%m%d")

        # 构建WHERE条件
        where_sql = ""
        if Serverpart_ID:
            where_sql += f" AND B.\"SERVERPART_ID\" IN ({Serverpart_ID})"
        elif SPRegionType_ID:
            where_sql += f" AND B.\"SPREGIONTYPE_ID\" IN ({SPRegionType_ID})"
        if Serverpart_Region:
            regions = ",".join([f"'{r.strip()}'" for r in Serverpart_Region.split(",")])
            where_sql += f" AND A.\"SERVERPART_REGION\" IN ({regions})"

        # 是否需要方位字段
        field_sql = "" if ShowGrowthRate else ',A."SERVERPART_REGION"'

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        result_list = []

        if ShowGrowthRate and not Serverpart_ID:
            # 汇总模式：全省汇总不按服务区分组
            sql = f"""SELECT
                    SUM(A."VEHICLE_COUNT") AS "VEHICLE_COUNT",
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

            # 上月同期
            lm_start = (start_date - relativedelta(months=1)).strftime("%Y%m%d")
            lm_end = (stat_date - relativedelta(months=1)).strftime("%Y%m%d")
            sql_lm = sql.replace(f">= {start_str}", f">= {lm_start}").replace(f"<= {end_str}", f"<= {lm_end}")
            rows_lm = db.execute_query(sql_lm) or []

            if rows and rows[0].get("VEHICLE_COUNT"):
                r = rows[0]
                vc = safe_dec(r.get("VEHICLE_COUNT"))
                sf = safe_dec(r.get("SECTIONFLOW_NUM"))
                item = {
                    "SPRegionType_Id": None, "SPRegionType_Index": None, "SPRegionType_Name": None,
                    "Serverpart_ID": None, "Serverpart_Index": None, "Serverpart_Name": None,
                    "Serverpart_Region": None,
                    "Vehicle_Count": vc, "MinVehicle_Count": safe_dec(r.get("MINVEHICLE_COUNT")),
                    "MediumVehicle_Count": safe_dec(r.get("MEDIUMVEHICLE_COUNT")),
                    "LargeVehicle_Count": safe_dec(r.get("LARGEVEHICLE_COUNT")),
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
                # 上月增长率
                if rows_lm and rows_lm[0].get("VEHICLE_COUNT"):
                    rl = rows_lm[0]
                    lsf = safe_dec(rl.get("SECTIONFLOW_NUM"))
                    if lsf > 0 and item["Entry_Rate"]:
                        last_rate = round(safe_dec(rl.get("VEHICLE_COUNT")) / lsf * 100, 2)
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

            # 断面流量
            sf_sql = f"""SELECT B."SERVERPART_ID"{field_sql}, SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
                FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                    AND A."STATISTICS_DATE" >= {start_str} AND A."STATISTICS_DATE" <= {end_str}{where_sql}
                GROUP BY B."SERVERPART_ID"{field_sql}"""
            dt_sf = db.execute_query(sf_sql) or []
            sf_map = {}
            for s in dt_sf:
                key = (s["SERVERPART_ID"], s.get("SERVERPART_REGION", ""))
                sf_map[key] = safe_dec(s.get("SECTIONFLOW_NUM"))

            # 上月数据(ShowGrowthRate时)
            lm_bayonet_map = {}
            lm_sf_map = {}
            if ShowGrowthRate:
                lm_start = (start_date - relativedelta(months=1)).strftime("%Y%m%d")
                lm_end = (stat_date - relativedelta(months=1)).strftime("%Y%m%d")
                lm_b_sql = bayonet_sql.replace(f">= {start_str}", f">= {lm_start}").replace(f"<= {end_str}", f"<= {lm_end}")
                lm_b = db.execute_query(lm_b_sql) or []
                for lb in lm_b:
                    key = (lb["SERVERPART_ID"], lb.get("SERVERPART_REGION", ""))
                    lm_bayonet_map[key] = lb
                lm_sf_sql = sf_sql.replace(f">= {start_str}", f">= {lm_start}").replace(f"<= {end_str}", f"<= {lm_end}")
                lm_s = db.execute_query(lm_sf_sql) or []
                for ls in lm_s:
                    key = (ls["SERVERPART_ID"], ls.get("SERVERPART_REGION", ""))
                    lm_sf_map[key] = safe_dec(ls.get("SECTIONFLOW_NUM"))

            for r in dt_bayonet:
                sp_id = r["SERVERPART_ID"]
                region = r.get("SERVERPART_REGION", "")
                key = (sp_id, region)
                vc_min = safe_dec(r.get("MINVEHICLE_COUNT"))
                vc_med = safe_dec(r.get("MEDIUMVEHICLE_COUNT"))
                vc_lrg = safe_dec(r.get("LARGEVEHICLE_COUNT"))
                vc = vc_min + vc_med + vc_lrg
                sf = sf_map.get(key, 0)

                item = {
                    "SPRegionType_Id": r.get("SPREGIONTYPE_ID"), "SPRegionType_Index": r.get("SPREGIONTYPE_INDEX"),
                    "SPRegionType_Name": r.get("SPREGIONTYPE_NAME"),
                    "Serverpart_ID": sp_id, "Serverpart_Index": r.get("SERVERPART_INDEX"),
                    "Serverpart_Name": r.get("SERVERPART_NAME"),
                    "Serverpart_Region": region if not ShowGrowthRate else None,
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
                # 增长率
                if ShowGrowthRate and sf > 0:
                    lb = lm_bayonet_map.get(key)
                    lsf = lm_sf_map.get(key, 0)
                    if lb and lsf > 0:
                        l_vc = safe_dec(lb.get("MINVEHICLE_COUNT")) + safe_dec(lb.get("MEDIUMVEHICLE_COUNT")) + safe_dec(lb.get("LARGEVEHICLE_COUNT"))
                        l_rate = round(l_vc / lsf * 100, 2)
                        item["Entry_GrowthRate"] = round(item["Entry_Rate"] - l_rate, 2) if item["Entry_Rate"] else None

                result_list.append(item)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPBayonetList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBayonetRankList")
async def get_bayonet_rank_list(
    Statistics_Date: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowGrowthRate: bool = Query(False, description="是否显示增长率"),
    GroupType: int = Query(1, description="统计方式：1当日 2当月 3当年"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车流量排行 (SQL平移完成)"""
    try:
        # 仅安徽有数据
        if Province_Code and Province_Code != "340000":
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        # 复用 GetSPBayonetList 的内部查询逻辑
        sp_result = await get_sp_bayonet_list(
            Statistics_Date=Statistics_Date, Province_Code=Province_Code,
            SPRegionType_ID=SPRegionType_ID, Serverpart_ID=Serverpart_ID,
            Serverpart_Region=Serverpart_Region, ShowGrowthRate=ShowGrowthRate,
            GroupType=GroupType, db=db)

        # 从返回结果中提取列表
        sp_data = sp_result.body if hasattr(sp_result, 'body') else None
        import json as json_mod
        if sp_data:
            resp = json_mod.loads(sp_data)
            data_list = resp.get("data", {}).get("DataList", [])
        else:
            data_list = []

        if not data_list:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        # 按入区车流量排行
        flow_list = sorted(data_list, key=lambda x: x.get("Vehicle_Count") or 0, reverse=True)
        # 按断面流量排行
        section_list = sorted(data_list, key=lambda x: x.get("SectionFlow_Count") or 0, reverse=True)
        # 按入区率排行(过滤入区率<100的)
        entry_list = sorted(
            [x for x in data_list if (x.get("Entry_Rate") or 0) < 100],
            key=lambda x: x.get("Entry_Rate") or 0, reverse=True)

        result = {
            "ServerpartFlowList": flow_list,
            "SectionFlowList": section_list,
            "EntryRateList": entry_list,
        }
        return Result.success(data=result, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetRankList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetAvgBayonetAnalysis")
async def get_avg_bayonet_analysis(
    Statistics_Date: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区平均车流量分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        if Province_Code and Province_Code != "340000":
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        if not Statistics_Date:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        def safe_f(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        where_sql = ""
        # 无服务区和片区参数时：查汇总行
        if not Serverpart_ID and not SPRegionType_ID:
            date_str = Statistics_Date.replace("-", "")
            if len(date_str) == 6:
                # 按月查询
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
                return Result.success(data={
                    "Vehicle_Count": safe_f(r.get("SERVERPART_FLOW")),
                    "Entry_Rate": safe_f(r.get("AVGENTRY_RATE")),
                    "Stay_Times": safe_f(r.get("AVGSTAY_TIMES")),
                }, msg="查询成功")
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # 有服务区/片区参数时：查明细后求平均
        if Serverpart_ID:
            where_sql += f' AND C."SERVERPART_ID" IN ({Serverpart_ID})'
        elif SPRegionType_ID:
            where_sql += f' AND C."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'
        if Serverpart_Region:
            regions = ",".join([f"'{r.strip()}'" for r in Serverpart_Region.split(",")])
            where_sql += f' AND A."SERVERPART_REGION" IN ({regions})'

        stat_str = dt.strptime(Statistics_Date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in Statistics_Date else Statistics_Date

        # 入区车流+断面流量
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
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # 按服务区分组聚合
        from collections import defaultdict
        sp_groups = defaultdict(lambda: {"vc": 0, "sf": 0})
        for r in rows:
            sp_id = r["SERVERPART_ID"]
            sp_groups[sp_id]["vc"] += safe_f(r.get("VEHICLE_COUNT"))
            sp_groups[sp_id]["sf"] += safe_f(r.get("SECTIONFLOW_NUM"))

        rates = []
        vcs = []
        for sp_id, g in sp_groups.items():
            vcs.append(g["vc"])
            if g["sf"] > 0:
                rates.append(round(g["vc"] / g["sf"] * 100, 2))

        avg_vc = round(sum(vcs) / len(vcs)) if vcs else 0
        avg_rate = round(sum(rates) / len(rates), 2) if rates else 0

        # 停留时长
        sta_sql = f"""SELECT A."SERVERPART_ID", ROUND(SUM(A."STAY_TIMES") / SUM(A."STAY_TIMESCOUNT"), 2) AS "AVGSTAY_TIMES"
            FROM "T_BAYONETDAILY_AH" A, "T_SERVERPART" C
            WHERE A."SERVERPART_ID" = C."SERVERPART_ID" AND A."STAY_TIMESCOUNT" > 0
                AND A."INOUT_TYPE" = 0 AND A."STATISTICS_DATE" = {stat_str}{where_sql}
            GROUP BY A."SERVERPART_ID" """
        sta_rows = db.execute_query(sta_sql) or []
        avg_stay = 0
        if sta_rows:
            stay_vals = [safe_f(r.get("AVGSTAY_TIMES")) for r in sta_rows if safe_f(r.get("AVGSTAY_TIMES")) > 0]
            if stay_vals:
                avg_stay = round(sum(stay_vals) / len(stay_vals) / 60, 2)

        return Result.success(data={
            "Vehicle_Count": avg_vc,
            "Entry_Rate": avg_rate,
            "Stay_Times": avg_stay,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAvgBayonetAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetProvinceAvgBayonetAnalysis")
async def get_province_avg_bayonet_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期/月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取全省平均车流量分析（与C#的GetAvgBayonetAnalysis全省版一致）"""
    try:
        from datetime import datetime as dt
        from dateutil.relativedelta import relativedelta

        if Province_Code != "340000":
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        if not Statistics_Date:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def safe_f(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        is_month = len(Statistics_Date) == 6  # yyyyMM格式
        if is_month:
            cur_month = Statistics_Date
            last_month = (dt.strptime(Statistics_Date + "01", "%Y%m%d") - relativedelta(months=1)).strftime("%Y%m")
            last_year = (dt.strptime(Statistics_Date + "01", "%Y%m%d") - relativedelta(years=1)).strftime("%Y%m")
        else:
            stat_date = dt.strptime(Statistics_Date, "%Y-%m-%d") if "-" in Statistics_Date else dt.strptime(Statistics_Date, "%Y%m%d")
            cur_month = stat_date.strftime("%Y%m%d")
            last_month = (stat_date - relativedelta(months=1)).strftime("%Y%m")
            last_year = (stat_date - relativedelta(years=1)).strftime("%Y%m")

        if is_month:
            # 月度查询
            months_in = f"{cur_month},{last_month},{last_year}"
            flow_sql = f"""SELECT SUM("SECTIONFLOW_NUM") AS "SUM_SECTIONFLOW_NUM",
                    SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SUM_SERVERPART_FLOW",
                    SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" <> 0 AND SUBSTR("STATISTICS_DATE",1,6) IN ({months_in})
                GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""
            avg_sql = f"""SELECT ROUND(AVG("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)),0) AS "SERVERPART_FLOW",
                    ROUND(AVG("AVGENTRY_RATE"),2) AS "AVGENTRY_RATE",
                    ROUND(AVG("AVGSTAY_TIMES"),2) AS "AVGSTAY_TIMES",
                    SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" = 0 AND SUBSTR("STATISTICS_DATE",1,6) IN ({months_in})
                GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""
        else:
            # 日期查询：当月到该日 + 上月 + 去年同月
            month_start = stat_date.strftime("%Y%m01")
            lm_end = last_month + cur_month[6:8]  # 上月同日
            ly_end = last_year + cur_month[6:8]    # 去年同月同日
            flow_sql = f"""SELECT SUM("SECTIONFLOW_NUM") AS "SUM_SECTIONFLOW_NUM",
                    SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SUM_SERVERPART_FLOW",
                    '{cur_month}' AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" <> 0 AND "STATISTICS_DATE" BETWEEN {month_start} AND {cur_month}
                UNION ALL
                SELECT SUM("SECTIONFLOW_NUM") AS "SUM_SECTIONFLOW_NUM",
                    SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SUM_SERVERPART_FLOW",
                    SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" <> 0 AND "STATISTICS_DATE" BETWEEN {last_month}01 AND {lm_end}
                GROUP BY SUBSTR("STATISTICS_DATE",1,6)
                UNION ALL
                SELECT SUM("SECTIONFLOW_NUM") AS "SUM_SECTIONFLOW_NUM",
                    SUM("SERVERPART_FLOW" + NVL("SERVERPART_FLOW_ANALOG",0)) AS "SUM_SERVERPART_FLOW",
                    SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" <> 0 AND "STATISTICS_DATE" BETWEEN {last_year}01 AND {ly_end}
                GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""
            avg_sql = f"""SELECT ROUND(AVG("SERVERPART_FLOW"),0) AS "SERVERPART_FLOW",
                    ROUND(AVG("AVGENTRY_RATE"),2) AS "AVGENTRY_RATE",
                    ROUND(AVG("AVGSTAY_TIMES"),2) AS "AVGSTAY_TIMES",
                    '{cur_month}' AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" = 0 AND "STATISTICS_DATE" >= {month_start} AND "STATISTICS_DATE" <= {cur_month}
                UNION ALL
                SELECT ROUND(AVG("SERVERPART_FLOW"),0) AS "SERVERPART_FLOW",
                    ROUND(AVG("AVGENTRY_RATE"),2) AS "AVGENTRY_RATE",
                    ROUND(AVG("AVGSTAY_TIMES"),2) AS "AVGSTAY_TIMES",
                    SUBSTR("STATISTICS_DATE",1,6) AS "STATISTICS_DATE"
                FROM "T_SECTIONFLOW"
                WHERE "SERVERPART_ID" = 0 AND SUBSTR("STATISTICS_DATE",1,6) IN ({last_month},{last_year})
                GROUP BY SUBSTR("STATISTICS_DATE",1,6)"""

        flow_rows = db.execute_query(flow_sql) or []
        avg_rows = db.execute_query(avg_sql) or []

        # 按STATISTICS_DATE降序排列
        avg_rows.sort(key=lambda r: str(r.get("STATISTICS_DATE", "")), reverse=True)

        # 构建flow的映射
        flow_map = {}
        for r in flow_rows:
            sd = str(r.get("STATISTICS_DATE", ""))
            flow_map[sd] = {
                "sf": safe_f(r.get("SUM_SECTIONFLOW_NUM")),
                "spf": safe_f(r.get("SUM_SERVERPART_FLOW"))
            }

        # 获取当月的平均入区率和停留时长（用于GrowthRate计算）
        cur_avg = None
        cur_flow = None
        for r in avg_rows:
            if str(r.get("STATISTICS_DATE", "")) == str(cur_month):
                cur_avg = r
                break
        cur_entry = safe_f(cur_avg.get("AVGENTRY_RATE")) if cur_avg else 0
        cur_stay = safe_f(cur_avg.get("AVGSTAY_TIMES")) if cur_avg else 0
        cur_spf = flow_map.get(str(cur_month), {}).get("spf", 0)

        data_list = []
        for r in avg_rows:
            sd = str(r.get("STATISTICS_DATE", ""))
            vc = safe_f(r.get("SERVERPART_FLOW"))
            entry = safe_f(r.get("AVGENTRY_RATE"))
            stay = safe_f(r.get("AVGSTAY_TIMES"))
            addup_sf = int(flow_map.get(sd, {}).get("sf", 0))
            addup_vc = int(flow_map.get(sd, {}).get("spf", 0))

            # 增长率计算
            vc_growth = round((cur_spf / addup_vc - 1) * 100, 2) if addup_vc else 0.0
            entry_growth = round(cur_entry - entry, 2) if entry else 0.0
            stay_growth = round((cur_stay / stay - 1) * 100, 2) if stay else 0.0

            # 名称：根据日期判断
            if sd == last_month:
                name = "QOQ"
            elif sd == last_year:
                name = "YOY"
            else:
                name = "Current"

            data_list.append({
                "Serverpart_ID": None, "Serverpart_Name": name, "Serverpart_Region": None,
                "Vehicle_Count": int(vc), "Vehicle_GrowthRate": vc_growth,
                "SectionFlow_Count": None, "Entry_Rate": entry, "Entry_GrowthRate": entry_growth,
                "Stay_Times": stay, "StayTimes_GrowthRate": stay_growth,
                "Vehicle_AddUpCount": addup_vc, "SectionFlow_AddUpCount": addup_sf,
                "EntryAddUp_Rate": None,
            })

        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetProvinceAvgBayonetAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBayonetSTAnalysis")
async def get_bayonet_st_analysis(
    StartMonth: Optional[str] = Query(None, description="统计开始月份"),
    EndMonth: Optional[str] = Query(None, description="统计结束月份"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车辆时段停留时长分析（返参：name车辆类型, data数组[时间段,停留时长]）"""
    try:
        import math
        # 构建 CASE WHEN 时段分组字段
        group_parts = []
        for i in range(0, math.ceil(24 / TimeSpan)):
            start_h = i * TimeSpan
            end_h = (i + 1) * TimeSpan
            if i == 0:
                group_parts.append(f"CASE WHEN \"STATISTICS_HOUR\" >= 0 AND \"STATISTICS_HOUR\" < {end_h} THEN {i}")
            elif end_h >= 24:
                group_parts.append(f" WHEN \"STATISTICS_HOUR\" >= {start_h} AND \"STATISTICS_HOUR\" < 24 THEN {i} END")
            else:
                group_parts.append(f" WHEN \"STATISTICS_HOUR\" >= {start_h} AND \"STATISTICS_HOUR\" < {end_h} THEN {i}")
        group_field = "".join(group_parts)

        # 构建 WHERE 条件
        conditions = ['A."SERVERPART_ID" = B."SERVERPART_ID"',
                       'A."INOUT_TYPE" = 0', 'A."DATA_TYPE" IN (0,1)']
        params = []
        if StartMonth:
            conditions.append(f'A."STATISTICS_MONTH" >= ?')
            params.append(int(StartMonth.replace("-", "")))
        if EndMonth:
            conditions.append(f'A."STATISTICS_MONTH" <= ?')
            params.append(int(EndMonth.replace("-", "")))
        if Serverpart_ID:
            conditions.append(f'B."SERVERPART_ID" IN ({Serverpart_ID})')
        elif SPRegionType_ID:
            conditions.append(f'B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})')

        where_sql = " AND ".join(conditions)
        sql = f"""SELECT A."VEHICLE_TYPE", {group_field} AS "STATISTICS_HOUR",
            ROUND(AVG(A."STAY_TIMES" / NULLIF(A."STATISTICS_DAYS", 0)), 2) AS "STAY_TIMES",
            SUM(A."STAY_TIMESTOTAL") AS "STAY_TIMESTOTAL",
            SUM(A."STAY_TIMESCOUNT") AS "STAY_TIMESCOUNT"
        FROM "T_BAYONETHOURMONTH_AH" A, "T_SERVERPART" B
        WHERE {where_sql}
        GROUP BY A."VEHICLE_TYPE", {group_field}"""

        rows = db.execute_query(sql, params)

        # 按车辆类型分组构建散点图数据
        vehicle_types = ["小型车", "中型车", "大型车"]
        result_list = []
        num_slots = math.ceil(24 / TimeSpan)

        for vt in vehicle_types:
            vt_rows = [r for r in rows if r.get("VEHICLE_TYPE") == vt]
            if not vt_rows:
                continue
            data = []
            for slot in range(num_slots):
                out_time = float(min(slot * TimeSpan, 24))
                slot_row = next((r for r in vt_rows if r.get("STATISTICS_HOUR") == slot), None)
                stay = 0
                if slot_row:
                    count = int(slot_row.get("STAY_TIMESCOUNT") or 0)
                    if count > 0:
                        stay = round(float(slot_row.get("STAY_TIMESTOTAL") or 0) / count / 3600, 2)
                    else:
                        stay = round(float(slot_row.get("STAY_TIMES") or 0) / 3600, 2)
                data.append([out_time, stay])
            result_list.append({"name": vt, "data": data, "value": None, "CommonScatterList": None})

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetSTAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetMonthAnalysis")
async def get_month_analysis(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    StartDate: Optional[str] = Query("", description="统计开始日期"),
    EndDate: Optional[str] = Query("", description="统计结束日期"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ServerpartShopIds: Optional[str] = Query("", description="门店内码集合"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度车流分析数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt
        import calendar

        if not StatisticsDate:
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def safe_f(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        start = dt(stat_date.year, 1, 1).strftime("%Y%m%d")
        end = stat_date.strftime("%Y%m%d")

        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND A."SERVERPART_ID" = {Serverpart_ID}'
        elif SPRegionType_ID:
            where_sql += f' AND C."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'

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
        # 按月汇总（所有方位合计）+ 按月+方位分组
        sf_map = {}
        sf_region_map = {}  # key: (month, region)
        for r in sf_rows:
            m = str(r.get("STATISTICS_MONTH", "")).strip()
            region = str(r.get("SERVERPART_REGION", "")).strip()
            vc = safe_f(r.get("VEHICLE_COUNT"))
            sf = safe_f(r.get("SECTIONFLOW_NUM"))
            days = int(safe_f(r.get("DATE_COUNT")))
            # 月汇总
            if m not in sf_map:
                sf_map[m] = {"days": 0, "vc": 0.0, "sf": 0.0}
            sf_map[m]["days"] = max(sf_map[m]["days"], days)
            sf_map[m]["vc"] += vc
            sf_map[m]["sf"] += sf
            # 月+方位
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
            mv_map[m] = {"days": int(safe_f(r.get("DATE_COUNT"))), "vc": safe_f(r.get("VEHICLE_COUNT")), "min": safe_f(r.get("MINVEHICLE_COUNT"))}

        # 查营收 按月
        rev_where = ""
        if Serverpart_ID:
            rev_where += f' AND A."SERVERPART_ID" = {Serverpart_ID}'
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
            rev_map[m] = {"days": int(safe_f(r.get("DATE_COUNT"))), "rev": safe_f(r.get("REVENUE_AMOUNT"))}

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
            # MinVehicle_Count: 小型车日均量 × 月天数
            m_info = mv_map.get(m_key, {})
            m_days = m_info.get("days", 0)
            min_vc = int(m_info.get("min", 0) / m_days) if m_days > 0 else 0
            min_vc_total = min_vc * cur_days

            # AvgVehicleAmount: C# 用入区流量(out类型)计算
            mv_vc = int(m_info.get("vc", 0) / m_days) if m_days > 0 else 0
            mv_total = mv_vc * cur_days
            avg_vehicle_amount = 0.0
            if mv_total > 0 and rev_days > 0:
                avg_vehicle_amount = round(rev_amount / rev_days / mv_vc, 2) if mv_vc > 0 else 0.0

            # 构建方向车流的RegionList
            region_list = []
            for region in server_regions:
                rkey = (m_key, region)
                if rkey in sf_region_map:
                    r_info = sf_region_map[rkey]
                    r_days = r_info.get("days", 0)
                    r_vc = int(r_info.get("vc", 0) / r_days * cur_days) if r_days > 0 else 0
                    region_list.append({"name": region, "value": str(r_vc)})

            result_list.append({
                "Statistics_Year": cur.year,
                "Statistics_Month": cur.month,
                "Vehicle_Count": total_vc,
                "SectionFlow_Count": total_sf,
                "Entry_Rate": entry_rate,
                "RevenueAmount": rev_amount,
                "AvgVehicleAmount": avg_vehicle_amount,
                "MinVehicle_Count": min_vc_total,
                "RegionList": region_list,
            })
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)

        # 补充List item缺失字段（与旧API对齐）
        for item in result_list:
            item.setdefault("SPRegionType_Id", None)
            item.setdefault("SPRegionType_Name", None)
            item.setdefault("Serverpart_ID", None)
            item.setdefault("Serverpart_Name", None)
            item.setdefault("ShopRevenueAmount", 0.0)
            item.setdefault("Stay_Times", None)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        resp = json_list.model_dump()
        resp["OtherData"] = True if result_list else False
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMonthAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetProvinceMonthAnalysis")
async def get_province_month_analysis(
    StatisticsMonth: Optional[str] = Query(None, description="统计月份，格式yyyyMM"),
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    SPRegion_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SortStr: Optional[str] = Query("", description="排序内容"),
    FromRedis: bool = Query(False, description="读取redis缓存"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取全省月度车流分析数据
    涉及表：T_SECTIONFLOW JOIN T_SERVERPART
    按服务区分组，统计月度总车流、总断面流量，计算日均值和入区率
    """
    try:
        conditions = []
        params = []

        # 月份过滤：STATISTICS_DATE BETWEEN yyyyMM01 AND yyyyMM31
        month_start = int(StatisticsMonth + "01")
        month_end = int(StatisticsMonth + "31")
        conditions.append('"A"."STATISTICS_DATE" >= ?')
        params.append(month_start)
        conditions.append('"A"."STATISTICS_DATE" <= ?')
        params.append(month_end)

        # 过滤条件
        if Serverpart_ID:
            conditions.append(f'"B"."SERVERPART_ID" IN ({Serverpart_ID})')
        elif SPRegion_ID:
            conditions.append(f'"B"."SPREGIONTYPE_ID" IN ({SPRegion_ID})')

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

        # 查营收数据 按SERVERPART_ID分组
        rev_conditions = []
        rev_params = []
        rev_conditions.append('"A"."STATISTICS_DATE" >= ?')
        rev_params.append(month_start)
        rev_conditions.append('"A"."STATISTICS_DATE" <= ?')
        rev_params.append(month_end)
        if Serverpart_ID:
            rev_conditions.append(f'"B"."SERVERPART_ID" = {Serverpart_ID}')
        elif SPRegion_ID:
            rev_conditions.append(f'"B"."SPREGIONTYPE_ID" IN ({SPRegion_ID})')
        else:
            # 省份过滤
            pid_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
            pid_rows = db.execute_query(pid_sql, {"pc": ProvinceCode or "340000"})
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
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 计算月度天数
        year = int(StatisticsMonth[:4])
        month = int(StatisticsMonth[4:6])
        import calendar
        from datetime import datetime
        now = datetime.now()
        # 如果是当月，用昨天的天数
        if StatisticsMonth == (now - __import__('datetime').timedelta(days=1)).strftime("%Y%m"):
            cur_days = (now - __import__('datetime').timedelta(days=1)).day
        elif StatisticsMonth == now.strftime("%Y%m"):
            cur_days = (now.day - 1) if now.day > 1 else 1
        else:
            cur_days = calendar.monthrange(year, month)[1]

        result_list = []
        for r in rows:
            date_count = int(r.get("DATE_COUNT") or 0)
            vehicle_count = int(r.get("VEHICLE_COUNT") or 0)
            sectionflow_num = int(r.get("SECTIONFLOW_NUM") or 0)

            # 日均值
            avg_vehicle = vehicle_count // date_count if date_count > 0 else 0
            avg_section = sectionflow_num // date_count if date_count > 0 else 0

            # 模拟全月车流量
            total_vehicle = avg_vehicle * cur_days
            total_section = avg_section * cur_days

            # 入区率 = 入区车流 / 断面流量 * 100
            entry_rate = round(total_vehicle * 100 / total_section, 2) if total_section > 0 else 0

            # 营收数据
            sp_id = r.get("SERVERPART_ID")
            rev_info = rev_map.get(sp_id, {})
            revenue_amount = rev_info.get("rev", 0.0)
            rev_days = rev_info.get("days", 0)
            avg_vehicle_amount = 0.0
            if avg_vehicle > 0 and rev_days > 0:
                avg_vehicle_amount = round(revenue_amount / rev_days / avg_vehicle, 2)

            sp_region_id = r.get("SPREGIONTYPE_ID")

            model = {
                "Statistics_Year": year,
                "Statistics_Month": month,
                "SPRegionType_Id": int(sp_region_id) if sp_region_id else None,
                "SPRegionType_Name": r.get("SPREGIONTYPE_NAME"),
                "Serverpart_ID": r.get("SERVERPART_ID"),
                "Serverpart_Name": r.get("SERVERPART_NAME"),
                "Vehicle_Count": total_vehicle,
                "MinVehicle_Count": None,
                "SectionFlow_Count": total_section,
                "Entry_Rate": entry_rate,
                "RevenueAmount": revenue_amount,
                "ShopRevenueAmount": 0.0,
                "AvgVehicleAmount": avg_vehicle_amount,
                "Stay_Times": None,
                "RegionList": [],
            }
            result_list.append(model)

        # 排序
        if SortStr:
            sort_field = SortStr.split(" ")[0]
            desc = SortStr.lower().endswith(" desc")
            if sort_field in ["SectionFlow_Count", "Vehicle_Count", "Entry_Rate"]:
                result_list.sort(key=lambda x: x.get(sort_field) or 0, reverse=desc)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetProvinceMonthAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetWarning")
async def get_bayonet_warning(
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    StatisticsHour: Optional[str] = Query("", description="统计时段"),
    StatisticsType: int = Query(1, description="统计方式：1即时预警 2当日排行"),
    ShowCount: int = Query(20, description="排行显示行数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取车流预警数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt

        if not StatisticsDate:
            return Result.fail(code=200, msg="查询失败，请传入统计日期！")

        date_str = dt.strptime(StatisticsDate, "%Y-%m-%d").strftime("%Y%m%d") if "-" in StatisticsDate else StatisticsDate

        sql = f"""SELECT * FROM "T_BAYONETWARNING"
            WHERE "BAYONETWARNING_STATE" = 1
            AND "STATISTICS_DATE" = {date_str}
            AND "STATISTICS_HOUR" = :hour"""
        rows = db.execute_query(sql, {"hour": StatisticsHour}) or []

        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0
        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        result_list = []
        if StatisticsType == 1:
            # 即时预警：时段车流>100 且 倍率>1.5 且<10
            filtered = [r for r in rows if safe_int(r.get("VEHICLE_COUNT")) > 100
                        and 1.5 < safe_dec(r.get("VEHICLE_RATE")) < 10]
            filtered.sort(key=lambda x: safe_int(x.get("VEHICLE_COUNT")), reverse=True)
            for r in filtered:
                result_list.append({
                    "SERVERPART_ID": safe_int(r.get("SERVERPART_ID")),
                    "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                    "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                    "VEHICLE_COUNT": safe_int(r.get("VEHICLE_COUNT")),
                    "MONTHVEHICLE_COUNT": safe_int(r.get("MONTHVEHICLE_COUNT")),
                    "VEHICLE_RATE": round(safe_dec(r.get("VEHICLE_RATE")) * 100, 2),
                })
        elif StatisticsType == 2:
            # 当日车流排行：累计倍率>1 且<10
            filtered = [r for r in rows if 1 < safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) < 10]
            filtered.sort(key=lambda x: safe_int(x.get("VEHICLE_TOTALCOUNT")), reverse=True)
            for r in filtered[:ShowCount]:
                result_list.append({
                    "SERVERPART_ID": safe_int(r.get("SERVERPART_ID")),
                    "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                    "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                    "VEHICLE_COUNT": safe_int(r.get("VEHICLE_TOTALCOUNT")),
                    "MONTHVEHICLE_COUNT": safe_int(r.get("MONTHVEHICLE_TOTALCOUNT")),
                    "VEHICLE_RATE": round(safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) * 100, 2),
                })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetWarning 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetHolidayBayonetWarning")
async def get_holiday_bayonet_warning(
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    StatisticsHour: Optional[str] = Query("", description="统计时段"),
    StatisticsType: int = Query(1, description="统计方式"),
    HolidayType: int = Query(0, description="节日类型"),
    curYear: Optional[str] = Query("", description="本年年份"),
    compareYear: Optional[str] = Query("", description="历年年份"),
    ShowCount: int = Query(20, description="排行显示行数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日车流预警数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        if not StatisticsDate:
            return Result.fail(code=200, msg="查询失败，请传入统计日期！")

        date_str = dt.strptime(StatisticsDate, "%Y-%m-%d").strftime("%Y%m%d") if "-" in StatisticsDate else StatisticsDate
        stat_date = dt.strptime(date_str, "%Y%m%d")

        # 查当日预警数据
        sql_today = f"""SELECT * FROM "T_BAYONETWARNING"
            WHERE "BAYONETWARNING_STATE" = 1
            AND "STATISTICS_DATE" = {date_str} AND "STATISTICS_HOUR" = :hour"""
        dt_warning = db.execute_query(sql_today, {"hour": StatisticsHour}) or []

        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0
        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        # 确定对比日期
        compare_date_str = None
        if StatisticsType in (3, 4):
            # 去年同期：通过节日映射
            try:
                holiday_names = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
                h_name = holiday_names.get(int(HolidayType), "")
                if h_name:
                    cur_desc = f"{curYear}年{h_name}"
                    cmp_desc = f"{compareYear}年{h_name}"
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
        elif StatisticsType in (5, 6):
            # 昨日
            compare_date_str = (stat_date - timedelta(days=1)).strftime("%Y%m%d")

        if not compare_date_str:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 查对比日期的预警数据
        sql_compare = f"""SELECT * FROM "T_BAYONETWARNING"
            WHERE "BAYONETWARNING_STATE" = 1
            AND "STATISTICS_DATE" = {compare_date_str} AND "STATISTICS_HOUR" = :hour"""
        dt_compare = db.execute_query(sql_compare, {"hour": StatisticsHour}) or []

        if not dt_compare:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 构建对比索引
        cmp_map = {}
        for c in dt_compare:
            key = (safe_int(c.get("SERVERPART_ID")), c.get("SERVERPART_REGION", ""))
            cmp_map[key] = c

        # 计算同环比
        for w in dt_warning:
            key = (safe_int(w.get("SERVERPART_ID")), w.get("SERVERPART_REGION", ""))
            if key in cmp_map:
                c = cmp_map[key]
                w["MONTHVEHICLE_COUNT"] = c.get("VEHICLE_COUNT")
                cvc = safe_dec(c.get("VEHICLE_COUNT"))
                w["VEHICLE_RATE"] = round(safe_dec(w.get("VEHICLE_COUNT")) / cvc, 2) if cvc > 0 else 0
                if safe_dec(w.get("VEHICLE_RATE")) > 10: w["VEHICLE_RATE"] = 0
                w["MONTHVEHICLE_TOTALCOUNT"] = c.get("VEHICLE_TOTALCOUNT")
                ctc = safe_dec(c.get("VEHICLE_TOTALCOUNT"))
                w["MONTHVEHICLE_TOTALRATE"] = round(safe_dec(w.get("VEHICLE_TOTALCOUNT")) / ctc, 2) if ctc > 0 else 0
                if safe_dec(w.get("MONTHVEHICLE_TOTALRATE")) > 10: w["MONTHVEHICLE_TOTALRATE"] = 0
            else:
                w["VEHICLE_RATE"] = 0
                w["MONTHVEHICLE_TOTALRATE"] = 0

        result_list = []
        if StatisticsType in (3, 5):
            # 即时预警
            filtered = [r for r in dt_warning if safe_int(r.get("VEHICLE_COUNT")) > 100
                        and safe_dec(r.get("VEHICLE_RATE")) > 1.5]
            filtered.sort(key=lambda x: safe_int(x.get("VEHICLE_COUNT")), reverse=True)
            for r in filtered:
                result_list.append({
                    "SERVERPART_ID": safe_int(r.get("SERVERPART_ID")),
                    "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                    "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                    "VEHICLE_COUNT": safe_int(r.get("VEHICLE_COUNT")),
                    "MONTHVEHICLE_COUNT": safe_int(r.get("MONTHVEHICLE_COUNT")),
                    "VEHICLE_RATE": round(safe_dec(r.get("VEHICLE_RATE")) * 100, 2),
                })
        elif StatisticsType in (4, 6):
            # 当日排行
            filtered = [r for r in dt_warning if safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) > 1]
            filtered.sort(key=lambda x: safe_int(x.get("VEHICLE_TOTALCOUNT")), reverse=True)
            for r in filtered[:ShowCount]:
                result_list.append({
                    "SERVERPART_ID": safe_int(r.get("SERVERPART_ID")),
                    "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                    "SERVERPART_REGION": r.get("SERVERPART_REGION", ""),
                    "VEHICLE_COUNT": safe_int(r.get("VEHICLE_TOTALCOUNT")),
                    "MONTHVEHICLE_COUNT": safe_int(r.get("MONTHVEHICLE_TOTALCOUNT")),
                    "VEHICLE_RATE": round(safe_dec(r.get("MONTHVEHICLE_TOTALRATE")) * 100, 2),
                })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayBayonetWarning 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetGrowthAnalysis")
async def get_bayonet_growth_analysis(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsStartDate: Optional[str] = Query(None, description="统计开始日期"),
    StatisticsEndDate: Optional[str] = Query(None, description="统计结束日期"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowGrowthRate: bool = Query(False, description="是否显示入区流量增幅"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取当日服务区车流量分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta
        from collections import defaultdict

        if not StatisticsStartDate or not StatisticsEndDate:
            return Result.success(data={"EntryList": [], "GrowthList": None, "sumEntryCount": 0}, msg="查询成功")

        s_date = dt.strptime(StatisticsStartDate, "%Y-%m-%d") if "-" in StatisticsStartDate else dt.strptime(StatisticsStartDate, "%Y%m%d")
        e_date = dt.strptime(StatisticsEndDate, "%Y-%m-%d") if "-" in StatisticsEndDate else dt.strptime(StatisticsEndDate, "%Y%m%d")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND B."SERVERPART_ID" IN ({Serverpart_ID})'
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'
        if Serverpart_Region:
            regions_in = ",".join(f"'{r}'" for r in Serverpart_Region.split(","))
            where_sql += f' AND A."SERVERPART_REGION" IN ({regions_in})'

        # 查当日车流
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
            return Result.success(data={"EntryList": [], "GrowthList": None, "sumEntryCount": 0}, msg="查询成功")

        # 如果需要增幅，查月均数据
        yes_map = {}
        if ShowGrowthRate:
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
                key = (safe_int(r.get("SERVERPART_ID")), r.get("SERVERPART_REGION", ""))
                yes_map[key] = r

        entry_list = []
        for r in rows:
            sp_id = safe_int(r.get("SERVERPART_ID"))
            region = r.get("SERVERPART_REGION", "")
            vc = safe_dec(r.get("VEHICLE_COUNT"))
            growth = 0.0

            if ShowGrowthRate:
                yr = yes_map.get((sp_id, region))
                if yr:
                    cd = safe_dec(yr.get("COUNT_DATE"))
                    if cd > 0:
                        avg_vc = round(safe_dec(yr.get("VEHICLE_COUNT")) / cd, 0)
                        if vc > 100 and avg_vc > 100:
                            growth = round(vc / avg_vc * 100, 2)

            entry_list.append({
                "Serverpart_ID": sp_id,
                "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                "Serverpart_Region": region + "区",
                "SPRegionType_Id": r.get("SPREGIONTYPE_ID"),
                "SPRegionType_Name": r.get("SPREGIONTYPE_NAME", ""),
                "SPRegionType_Index": r.get("SPREGIONTYPE_INDEX"),
                "Serverpart_Index": None,
                "Vehicle_Count": vc,
                "Entry_GrowthRate": growth if growth != 0.0 else None,
                "Entry_Rate": None,
                "LargeVehicleEntry_GrowthRate": None,
                "LargeVehicleEntry_Rate": None,
                "LargeVehicle_Count": None,
                "MediumVehicleEntry_GrowthRate": None,
                "MediumVehicleEntry_Rate": None,
                "MediumVehicle_Count": None,
                "MinVehicleEntry_GrowthRate": None,
                "MinVehicleEntry_Rate": None,
                "MinVehicle_Count": None,
                "SectionFlow_Count": None,
            })

        sum_entry = sum(e["Vehicle_Count"] for e in entry_list)

        growth_list = None
        if ShowGrowthRate:
            growth_list = sorted(entry_list, key=lambda x: (-(x["Entry_GrowthRate"] or 0), -x["Vehicle_Count"]))

        # 按服务区合并
        sp_agg = defaultdict(lambda: {"name": "", "vc": 0.0, "rid": None, "rname": "", "rindex": None})
        for e in entry_list:
            sp_agg[e["Serverpart_ID"]]["name"] = e["Serverpart_Name"]
            sp_agg[e["Serverpart_ID"]]["vc"] += e["Vehicle_Count"]
            sp_agg[e["Serverpart_ID"]]["rid"] = e.get("SPRegionType_Id")
            sp_agg[e["Serverpart_ID"]]["rname"] = e.get("SPRegionType_Name", "")
            sp_agg[e["Serverpart_ID"]]["rindex"] = e.get("SPRegionType_Index")

        merged_list = sorted([
            {"Serverpart_ID": sid, "Serverpart_Name": v["name"], "Serverpart_Region": "",
             "Serverpart_Index": None,
             "SPRegionType_Id": None, "SPRegionType_Name": None, "SPRegionType_Index": None,
             "Vehicle_Count": v["vc"], "Entry_GrowthRate": None, "Entry_Rate": None,
             "LargeVehicleEntry_GrowthRate": None, "LargeVehicleEntry_Rate": None,
             "LargeVehicle_Count": None, "MediumVehicleEntry_GrowthRate": None,
             "MediumVehicleEntry_Rate": None, "MediumVehicle_Count": None,
             "MinVehicleEntry_GrowthRate": None, "MinVehicleEntry_Rate": None,
             "MinVehicle_Count": None, "SectionFlow_Count": None}
            for sid, v in sp_agg.items()
        ], key=lambda x: -x["Vehicle_Count"])

        return Result.success(data={
            "EntryList": merged_list,
            "GrowthList": growth_list,
            "sumEntryCount": sum_entry,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetGrowthAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetCompare")
async def get_bayonet_compare(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsStartDate: Optional[str] = Query(None, description="统计开始日期"),
    StatisticsEndDate: Optional[str] = Query(None, description="统计结束日期"),
    CompareStartDate: Optional[str] = Query("", description="对比开始日期"),
    CompareEndDate: Optional[str] = Query("", description="对比结束日期"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车流量同比分析 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        if pushProvinceCode != "340000":
            return Result.fail(code=200, msg="查询失败，无数据返回！")
        if not StatisticsStartDate or not StatisticsEndDate:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        def parse_d(s):
            return dt.strptime(s, "%Y-%m-%d") if "-" in s else dt.strptime(s, "%Y%m%d")
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        s_date = parse_d(StatisticsStartDate)
        e_date = parse_d(StatisticsEndDate)
        cs_date = parse_d(CompareStartDate) if CompareStartDate else s_date.replace(year=s_date.year - 1)
        ce_date = parse_d(CompareEndDate) if CompareEndDate else e_date.replace(year=e_date.year - 1)

        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND B."SERVERPART_ID" IN ({Serverpart_ID})'
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'
        if Serverpart_Region:
            regions_in = ",".join(f"'{r}'" for r in Serverpart_Region.split(","))
            where_sql += f' AND A."SERVERPART_REGION" IN ({regions_in})'

        # 查当前期
        sql_base = """SELECT A."STATISTICS_DATE",COUNT(DISTINCT A."SERVERPART_ID") AS "SERVERPART_COUNT",
                SUM(A."SERVERPART_FLOW") AS "VEHICLE_COUNT"
            FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SERVERPART_FLOW" > 0
                AND A."STATISTICS_DATE" >= {s} AND A."STATISTICS_DATE" <= {e}{w}
            GROUP BY A."STATISTICS_DATE" """

        cur_rows = db.execute_query(sql_base.format(
            s=s_date.strftime("%Y%m%d"), e=e_date.strftime("%Y%m%d"), w=where_sql)) or []
        cmp_rows = db.execute_query(sql_base.format(
            s=cs_date.strftime("%Y%m%d"), e=ce_date.strftime("%Y%m%d"), w=where_sql)) or []

        cur_map = {}
        for r in cur_rows:
            d = str(safe_int(r.get("STATISTICS_DATE")))
            sc = safe_int(r.get("SERVERPART_COUNT"))
            vc = safe_int(r.get("VEHICLE_COUNT"))
            cur_map[d] = vc // sc if sc > 0 else 0

        cmp_map = {}
        for r in cmp_rows:
            d = str(safe_int(r.get("STATISTICS_DATE")))
            sc = safe_int(r.get("SERVERPART_COUNT"))
            vc = safe_int(r.get("VEHICLE_COUNT"))
            cmp_map[d] = vc // sc if sc > 0 else 0

        cur_days = (e_date - s_date).days + 1
        cmp_days = (ce_date - cs_date).days + 1
        max_days = max(cur_days, cmp_days)

        cur_list = []
        cmp_list = []
        for i in range(max_days):
            cd = s_date + timedelta(days=i)
            ld = cs_date + timedelta(days=i)
            cur_list.append({
                "name": date_no_pad(cd),
                "value": str(cur_map.get(cd.strftime("%Y%m%d"), 0)),
                "data": None, "key": None,
            })
            cmp_list.append({
                "name": date_no_pad(ld),
                "value": str(cmp_map.get(ld.strftime("%Y%m%d"), 0)),
                "data": None, "key": None,
            })

        return Result.success(data={
            "curHoliday": None, "curHolidayDays": 0,
            "curList": cur_list,
            "compareHoliday": None, "compareHolidayDays": 0,
            "compareList": cmp_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetCompare 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetHolidayCompare")
async def get_holiday_compare(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    holidayType: int = Query(0, description="节日类型"),
    curYear: Optional[int] = Query(None, description="当前年份"),
    compareYear: Optional[int] = Query(None, description="对比年份"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日服务区平均入区流量对比数据 (SQL平移完成)"""
    try:
        from datetime import datetime as dt, timedelta

        if not curYear or not compareYear:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        # 查节日日期（C#使用 WORKFLOW_SUPPORT.T_HOLIDAY + HOLIDAY_DESC）
        holiday_names = {1:"元旦",2:"春运",3:"清明节",4:"劳动节",5:"端午节",6:"暑期",7:"中秋节",8:"国庆节"}
        h_name = holiday_names.get(int(holidayType), "")
        if not h_name:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        cur_desc = f"{curYear}年{h_name}"
        cmp_desc = f"{compareYear}年{h_name}"
        h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
        if not h_rows:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        def to_dt2(v):
            if isinstance(v, dt): return v
            if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
            return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

        cur_dates = [to_dt2(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
        cmp_dates = [to_dt2(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]

        if not cur_dates or not cmp_dates:
            return Result.fail(code=200, msg="查询失败，无数据返回！")

        s_date = min(cur_dates)
        e_date = max(cur_dates)
        cs_date = min(cmp_dates)
        ce_date = max(cmp_dates)

        cur_holiday = f"{s_date.strftime('%m.%d')}-{e_date.strftime('%m.%d')}"
        cmp_holiday = f"{cs_date.strftime('%m.%d')}-{ce_date.strftime('%m.%d')}"
        cur_days = (e_date - s_date).days + 1
        cmp_days = (ce_date - cs_date).days + 1

        # 复用 BayonetCompare 查询逻辑
        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND B."SERVERPART_ID" IN ({Serverpart_ID})'
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionType_ID})'
        if Serverpart_Region:
            regions_in = ",".join(f"'{r}'" for r in Serverpart_Region.split(","))
            where_sql += f' AND A."SERVERPART_REGION" IN ({regions_in})'

        sql_base = """SELECT A."STATISTICS_DATE",COUNT(DISTINCT A."SERVERPART_ID") AS "SERVERPART_COUNT",
                SUM(A."SERVERPART_FLOW") AS "VEHICLE_COUNT"
            FROM "T_SECTIONFLOW" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."SERVERPART_FLOW" > 0
                AND A."STATISTICS_DATE" >= {s} AND A."STATISTICS_DATE" <= {e}{w}
            GROUP BY A."STATISTICS_DATE" """

        cur_rows = db.execute_query(sql_base.format(
            s=s_date.strftime("%Y%m%d"), e=e_date.strftime("%Y%m%d"), w=where_sql)) or []
        cmp_rows = db.execute_query(sql_base.format(
            s=cs_date.strftime("%Y%m%d"), e=ce_date.strftime("%Y%m%d"), w=where_sql)) or []

        cur_map = {}
        for r in cur_rows:
            d = str(safe_int(r.get("STATISTICS_DATE")))
            sc = safe_int(r.get("SERVERPART_COUNT"))
            vc = safe_int(r.get("VEHICLE_COUNT"))
            cur_map[d] = vc // sc if sc > 0 else 0
        cmp_map = {}
        for r in cmp_rows:
            d = str(safe_int(r.get("STATISTICS_DATE")))
            sc = safe_int(r.get("SERVERPART_COUNT"))
            vc = safe_int(r.get("VEHICLE_COUNT"))
            cmp_map[d] = vc // sc if sc > 0 else 0

        max_d = max(cur_days, cmp_days)
        cur_list = []
        cmp_list = []
        for i in range(max_d):
            cd = s_date + timedelta(days=i)
            ld = cs_date + timedelta(days=i)
            cur_list.append({"name": date_no_pad(cd), "value": str(cur_map.get(cd.strftime("%Y%m%d"), 0)), "data": None, "key": None})
            cmp_list.append({"name": date_no_pad(ld), "value": str(cmp_map.get(ld.strftime("%Y%m%d"), 0)), "data": None, "key": None})

        return Result.success(data={
            "curHoliday": cur_holiday, "curHolidayDays": cur_days,
            "curList": cur_list,
            "compareHoliday": cmp_holiday, "compareHolidayDays": cmp_days,
            "compareList": cmp_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayCompare (BigData) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetOAAnalysis")
async def get_bayonet_oa_analysis(
    HolidayType: int = Query(0, description="节日类型：0全部 1节假日 2非节假日"),
    StartMonth: Optional[str] = Query(None, description="统计开始月份，格式yyyyMM"),
    EndMonth: Optional[str] = Query(None, description="统计结束月份，格式yyyyMM"),
    VehicleType: Optional[str] = Query("", description="车辆类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取日均车流归属地数据分析 (SQL平移完成)"""
    try:
        def safe_int(v):
            try: return int(float(v)) if v is not None else 0
            except: return 0

        # 1. 查断面流量月度汇总
        where_sql = ""
        if HolidayType == 1:
            where_sql += " AND B.\"HOLIDAY_TYPE\" IN (2,4,6,8)"
        elif HolidayType == 2:
            where_sql += " AND B.\"HOLIDAY_TYPE\" NOT IN (2,4,6,8)"
        if StartMonth:
            where_sql += f" AND B.\"STATISTICS_MONTH\" >= {StartMonth}"
        if EndMonth:
            where_sql += f" AND B.\"STATISTICS_MONTH\" <= {EndMonth}"

        sf_sql = f"""SELECT
                A."SERVERPART_ID",A."SERVERPART_NAME",B."SERVERPART_REGION",
                SUM(B."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM",
                SUM(B."SERVERPART_FLOW") AS "SERVERPART_FLOW",
                SUM(B."STATISTICS_DAYS") AS "STATISTICS_DAYS",
                SUM(B."MINVEHICLE_COUNT") AS "MINVEHICLE_COUNT",
                SUM(B."MEDIUMVEHICLE_COUNT") AS "MEDIUMVEHICLE_COUNT",
                SUM(B."LARGEVEHICLE_COUNT") AS "LARGEVEHICLE_COUNT",
                MIN("STATISTICS_MONTH") AS "START_MONTH",
                MAX("STATISTICS_MONTH") AS "END_MONTH"
            FROM "T_SERVERPART" A, "T_SECTIONFLOWMONTH" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND B."SECTIONFLOWMONTH_STATE" = 1{where_sql}
            GROUP BY A."SERVERPART_ID",A."SERVERPART_NAME",B."SERVERPART_REGION" """
        dt_sf = db.execute_query(sf_sql) or []

        # 2. 查归属地省份数据
        oa_where = ""
        if HolidayType == 1:
            oa_where = ' AND "STATISTICS_MONTH" = 202402'
        elif HolidayType == 2:
            oa_where = ' AND "STATISTICS_MONTH" = 202403'
        else:
            oa_where = ' AND "STATISTICS_MONTH" = 202401'
        oa_where += ' AND "SERVERPART_ID" > 0'
        if VehicleType:
            oa_where += f" AND \"VEHICLE_TYPE\" = '{VehicleType}'"
        else:
            oa_where += ' AND "VEHICLE_TYPE" IS NULL'

        oa_sql = f"""SELECT "SERVERPART_ID","PROVINCE_NAME","VEHICLE_COUNT","AVGVEHICLE_COUNT","RANK_NUM"
            FROM "T_BAYONETPROVINCEMONTH_AH"
            WHERE "SERVERPART_REGION" IS NULL{oa_where}"""
        dt_oa = db.execute_query(oa_sql) or []

        # 3. 查出区车流（计算日均出区车流）
        out_where = ""
        if HolidayType == 1:
            out_where = " AND \"STATISTICS_DATE\" BETWEEN 20240201 AND 20240228"
        elif HolidayType == 2:
            out_where = " AND \"STATISTICS_DATE\" BETWEEN 20240301 AND 20240331"
        else:
            out_where = " AND \"STATISTICS_DATE\" BETWEEN 20240101 AND 20240131"
        out_where += ' AND "SERVERPART_ID" > 0'

        out_sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION",
                SUM("VEHICLE_COUNT") AS "VEHICLE_COUNT",
                COUNT(DISTINCT "STATISTICS_DATE") AS "STATISTICS_DAYS"
            FROM "T_BAYONETDAILY_AH"
            WHERE "INOUT_TYPE" = 0{out_where}
            GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
        dt_out = db.execute_query(out_sql) or []

        # 构建索引
        from collections import defaultdict
        sf_map = defaultdict(list)
        for r in dt_sf:
            sf_map[safe_int(r.get("SERVERPART_ID"))].append(r)

        oa_map = defaultdict(list)
        for r in dt_oa:
            oa_map[safe_int(r.get("SERVERPART_ID"))].append(r)

        out_map = {}
        for r in dt_out:
            key = (safe_int(r.get("SERVERPART_ID")), r.get("SERVERPART_REGION", ""))
            out_map[key] = r

        # 获取服务区列表
        sp_set = {}
        for r in dt_sf:
            sp_id = safe_int(r.get("SERVERPART_ID"))
            if sp_id not in sp_set:
                sp_set[sp_id] = r.get("SERVERPART_NAME", "")

        regions = ["东", "南", "西", "北"]
        result_list = []
        start_month_val = None
        end_month_val = None

        for sp_id, sp_name in sp_set.items():
            vc_total = 0
            mini_vc = 0
            medium_vc = 0
            large_vc = 0
            out_vc_total = 0

            for region in regions:
                sf_rows = [r for r in sf_map[sp_id] if r.get("SERVERPART_REGION") == region]
                if sf_rows:
                    s = sf_rows[0]
                    days = safe_int(s.get("STATISTICS_DAYS"))
                    if days > 0:
                        vc_total += safe_int(s.get("SERVERPART_FLOW")) // days
                        mini_vc += safe_int(s.get("MINVEHICLE_COUNT")) // days
                        medium_vc += safe_int(s.get("MEDIUMVEHICLE_COUNT")) // days
                        large_vc += safe_int(s.get("LARGEVEHICLE_COUNT")) // days
                    sm = s.get("START_MONTH")
                    em = s.get("END_MONTH")
                    if sm: start_month_val = min(start_month_val, safe_int(sm)) if start_month_val else safe_int(sm)
                    if em: end_month_val = max(end_month_val, safe_int(em)) if end_month_val else safe_int(em)

                out_row = out_map.get((sp_id, region))
                if out_row:
                    od = safe_int(out_row.get("STATISTICS_DAYS"))
                    if od > 0:
                        out_vc_total += safe_int(out_row.get("VEHICLE_COUNT")) // od

            # 归属地省份
            oa_rows = sorted(oa_map.get(sp_id, []), key=lambda x: safe_int(x.get("RANK_NUM")))
            total_avg_oa = sum(safe_int(r.get("AVGVEHICLE_COUNT")) for r in oa_rows)
            if total_avg_oa > out_vc_total:
                out_vc_total = total_avg_oa

            province_list = []
            province_names = []
            for r in oa_rows:
                pname = r.get("PROVINCE_NAME", "")
                province_names.append(pname)
                avg_c = safe_int(r.get("AVGVEHICLE_COUNT"))
                pv = (avg_c * vc_total // out_vc_total) if out_vc_total > 0 else 0
                province_list.append({"name": pname, "value": str(pv)})

            display_vc = vc_total
            if VehicleType == "小型车":
                display_vc = mini_vc
            elif VehicleType == "中型车":
                display_vc = medium_vc
            elif VehicleType == "大型车":
                display_vc = large_vc

            result_list.append({
                "Serverpart_ID": sp_id,
                "Serverpart_Name": sp_name,
                "Vehicle_Count": display_vc,
                "OwnerProvince": province_names,
                "OwnerProvinceList": province_list,
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        resp = json_list.model_dump()
        resp["OtherData"] = [
            str(start_month_val) if start_month_val else "",
            str(end_month_val) if end_month_val else "",
        ]
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetOAAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetDateAnalysis")
async def get_date_analysis(
    StartDate: Optional[str] = Query(None, description="统计开始日期，格式yyyy-MM-dd"),
    EndDate: Optional[str] = Query(None, description="统计结束日期，格式yyyy-MM-dd"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取日度车流分析数据
    涉及表：T_SECTIONFLOW（日度断面流量）JOIN T_ENDACCOUNT_DAILY（日营业额）
    按日期遍历，聚合东南/西北方位的断面流量和入区流量，并计算同比数据
    """
    try:
        from datetime import datetime, timedelta

        start_dt = datetime.strptime(StartDate.split(" ")[0], "%Y-%m-%d")
        end_dt = datetime.strptime(EndDate.split(" ")[0], "%Y-%m-%d")
        start_str = start_dt.strftime("%Y%m%d")
        end_str = end_dt.strftime("%Y%m%d")
        # 去年同期
        ly_start_dt = start_dt.replace(year=start_dt.year - 1)
        ly_end_dt = end_dt.replace(year=end_dt.year - 1)
        ly_start_str = ly_start_dt.strftime("%Y%m%d")
        ly_end_str = ly_end_dt.strftime("%Y%m%d")

        south_east = ['东', '南']
        north_west = ['西', '北']

        # 查询本年度+去年同期的断面流量（UNION ALL）
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
            Serverpart_ID, int(start_str), int(end_str),
            Serverpart_ID, int(ly_start_str), int(ly_end_str)
        ])

        # 构建 {(date, region): row} 字典
        flow_map = {}
        for r in (rows or []):
            key = (r.get("STATISTICS_DATE"), r.get("SERVERPART_REGION"))
            flow_map[key] = r

        # 查询营收数据 (今年+去年)，含A/B拆分
        rev_sql = f"""SELECT "STATISTICS_DATE", SUM("REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM("REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",
                SUM("REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B"
            FROM "T_REVENUEDAILY"
            WHERE "REVENUEDAILY_STATE" = 1 AND "SERVERPART_ID" = {Serverpart_ID}
                AND "STATISTICS_DATE" >= {start_str} AND "STATISTICS_DATE" <= {end_str}
            GROUP BY "STATISTICS_DATE"
            UNION ALL
            SELECT "STATISTICS_DATE", SUM("REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM("REVENUE_AMOUNT_A") AS "REVENUE_AMOUNT_A",
                SUM("REVENUE_AMOUNT_B") AS "REVENUE_AMOUNT_B"
            FROM "T_REVENUEDAILY"
            WHERE "REVENUEDAILY_STATE" = 1 AND "SERVERPART_ID" = {Serverpart_ID}
                AND "STATISTICS_DATE" >= {ly_start_str} AND "STATISTICS_DATE" <= {ly_end_str}
            GROUP BY "STATISTICS_DATE" """
        rev_rows = db.execute_query(rev_sql) or []
        rev_map = {}
        for r in rev_rows:
            d = r.get("STATISTICS_DATE")
            rev_map[d] = {
                "rev": float(r.get("REVENUE_AMOUNT", 0) or 0),
                "rev_a": float(r.get("REVENUE_AMOUNT_A", 0) or 0),
                "rev_b": float(r.get("REVENUE_AMOUNT_B", 0) or 0),
            }

        # 遍历日期范围组装数据
        result_list = []
        cur_date = start_dt
        while cur_date <= end_dt:
            date_num = int(cur_date.strftime("%Y%m%d"))
            ly_date_num = int(cur_date.replace(year=cur_date.year - 1).strftime("%Y%m%d"))

            cur_rev = rev_map.get(date_num, {})
            ly_rev = rev_map.get(ly_date_num, {})

            model = {
                "STATISTICS_DATE": cur_date.strftime("%m-%d"),
                "ThisYearTotalSECTIONFLOW_NUM": 0.0,
                "ThisYearTotalSERVERPART_FLOW": 0.0,
                "LastYearTotalSECTIONFLOW_NUM": 0.0,
                "LastYearTotalSERVERPART_FLOW": 0.0,
                "ThisYearSouthEastSECTIONFLOW_NUM": 0.0,
                "ThisYearSouthEastSERVERPART_FLOW": 0.0,
                "ThisYearNorthWestSECTIONFLOW_NUM": 0.0,
                "ThisYearNorthWestSERVERPART_FLOW": 0.0,
                "LastYearSouthEastSECTIONFLOW_NUM": 0.0,
                "LastYearSouthEastSERVERPART_FLOW": 0.0,
                "LastYearNorthWestSECTIONFLOW_NUM": 0.0,
                "LastYearNorthWestSERVERPART_FLOW": 0.0,
                "ThisYearTotalANALOG": 0.0,
                "ThisYearSouthEastANALOG": 0.0,
                "ThisYearNorthWestANALOG": 0.0,
                "LastYearTotalANALOG": 0.0,
                "LastYearSouthEastANALOG": 0.0,
                "LastYearNorthWestANALOG": 0.0,
                "CurRevenueAmount": cur_rev.get("rev", 0.0),
                "CurRevenueAmount_A": cur_rev.get("rev_a", 0.0),
                "CurRevenueAmount_B": cur_rev.get("rev_b", 0.0),
                "LyRevenueAmount": ly_rev.get("rev", 0.0),
                "LyRevenueAmount_A": ly_rev.get("rev_a", 0.0),
                "LyRevenueAmount_B": ly_rev.get("rev_b", 0.0),
            }

            for region in ['东', '南', '西', '北']:
                # 今年数据
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
                # 去年数据
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

            # 计算差值
            model["TotalDiffSECTIONFLOW_NUM"] = (
                model["ThisYearTotalSECTIONFLOW_NUM"] - model["LastYearTotalSECTIONFLOW_NUM"])
            model["TotalDiffSERVERPART_FLOW"] = (
                model["ThisYearTotalSERVERPART_FLOW"] - model["LastYearTotalSERVERPART_FLOW"])
            model["SouthEastDiffSECTIONFLOW_NUM"] = (
                model["ThisYearSouthEastSECTIONFLOW_NUM"] - model["LastYearSouthEastSECTIONFLOW_NUM"])
            model["SouthEastDiffSERVERPART_FLOW"] = (
                model["ThisYearSouthEastSERVERPART_FLOW"] - model["LastYearSouthEastSERVERPART_FLOW"])
            model["NorthWestDiffSECTIONFLOW_NUM"] = (
                model["ThisYearNorthWestSECTIONFLOW_NUM"] - model["LastYearNorthWestSECTIONFLOW_NUM"])
            model["NorthWestDiffSERVERPART_FLOW"] = (
                model["ThisYearNorthWestSERVERPART_FLOW"] - model["LastYearNorthWestSERVERPART_FLOW"])

            result_list.append(model)
            cur_date += timedelta(days=1)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        resp = json_list.model_dump()
        # OtherData汇总所有日期
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
        # ANALOG字段在C#中OtherData不汇总（返回None）
        analog_keys = {"ThisYearTotalANALOG", "ThisYearSouthEastANALOG", "ThisYearNorthWestANALOG",
                        "LastYearTotalANALOG", "LastYearSouthEastANALOG", "LastYearNorthWestANALOG"}
        _oth = {"STATISTICS_DATE": None}
        for k in sum_keys:
            if k in analog_keys:
                _oth[k] = None
            else:
                _oth[k] = round(sum(float(m.get(k, 0) or 0) for m in result_list), 2)
        resp["OtherData"] = [_oth]
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetDateAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== POST+AES 接口 =====

@router.post("/BigData/GetCurBusyRank")
async def get_cur_busy_rank(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    获取服务区繁忙排行
    入参(AES加密)：ProvinceCode, ServerpartId, ServerpartCode, DataType
    """
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        data_type = int(params.get("DataType", 0))
        logger.info(f"GetCurBusyRank 解密参数: ProvinceCode={province_code}, DataType={data_type}")

        if not province_code:
            return Result.fail(code=205, msg="查询失败,请传入省份编码！")

        # TODO: 实现查询逻辑（需要 Redis）
        logger.warning("GetCurBusyRank 查询逻辑暂未实现（需Redis）")
        json_list = JsonListData.create(data_list=[], total=0)
        resp = json_list.model_dump()
        # C#对齐: summaryModel = new CommonKeyModel { name="服务承载", value=count>30, data=count<=30 }
        resp["OtherData"] = {"data": "0", "key": None, "name": "服务承载", "value": "0"}
        return Result.success(data=resp, msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetCurBusyRank AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BigData/GetRevenueTrendChart")
async def get_revenue_trend_chart(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    获取今日营收趋势图
    入参(AES加密)：ProvinceCode, ServerpartId, ServerpartCode
    """
    try:
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
            rows = db.execute_query(
                f'SELECT "SERVERPART_CODE" FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({serverpart_id})')
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
        redis_client = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
        table_name = f"RevenueTrend:{dt.now().strftime('%Y%m%d')}"
        all_data = redis_client.hgetall(table_name)

        # 解析 Redis 数据
        import json as json_lib
        trend_list = []
        for k, v in all_data.items():
            try:
                item = json_lib.loads(v)
                trend_list.append(item)
            except:
                pass

        # 按每半小时统计营收趋势
        now_hours = dt.now().hour + dt.now().minute / 60.0
        result_list = []
        last_time = "0000"

        half_time = 0.5
        while half_time <= now_hours:
            hour_part = int(math.floor(half_time))
            min_part = int(half_time * 60 % 60)
            now_time = f"{hour_part:02d}{min_part:02d}"

            total_amount = 0.0
            ticket_count = 0.0
            total_count = 0.0

            # 遍历匹配的数据
            for item in trend_list:
                sc = item.get("ServerpartCode", "")
                td = item.get("TradeDate", "")
                if sc in serverpart_codes:
                    try:
                        td_val = float(td) if td else 0
                        lt_val = float(last_time)
                        nt_val = float(now_time)
                        if td_val > lt_val and td_val <= nt_val:
                            total_amount += float(item.get("TotalAmount", 0) or 0)
                            ticket_count += float(item.get("TicketCount", 0) or 0)
                            total_count += float(item.get("TotalCount", 0) or 0)
                    except:
                        pass

            avg_ticket = round(total_amount / ticket_count, 2) if ticket_count > 0 else 0.0
            result_list.append({
                "TradeDate": now_time,
                "TotalAmount": total_amount,
                "TicketCount": ticket_count,
                "TotalCount": total_count,
                "AvgTicketAmount": avg_ticket,
                "ConnectState": None,
            })
            last_time = now_time
            half_time += 0.5

        # C#对齐: JsonList.Success默认PageSize=10
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetRevenueTrendChart AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BigData/GetEnergyRevenueInfo")
async def get_energy_revenue_info(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    获取当日全业态营收数据
    入参(AES加密)：DataType(1000门店/2000油品/3000加水/4000尿素/5000新能源),
                   StatisticsDate, ShowWY, ShowLargeUnit
    """
    try:
        from core.aes_util import decrypt_post_data
        from datetime import datetime as dt
        params = decrypt_post_data(postData)
        data_type = int(params.get("DataType", 0))
        statistics_date = params.get("StatisticsDate", "")
        show_wy = str(params.get("ShowWY", "false")).lower() == "true"
        show_large_unit = str(params.get("ShowLargeUnit", "false")).lower() == "true"
        logger.info(f"GetEnergyRevenueInfo 解密参数: DataType={data_type}, Date={statistics_date}")

        cur_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
        cur_date_str = cur_date.strftime("%Y-%m-%d")
        next_date_str = (cur_date + __import__('datetime').timedelta(days=1)).strftime("%Y-%m-%d")

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

        elif data_type == 5000:  # 新能源 - C#只设了name但没数据查询
            name = "新能源"

        # C#对齐: value = ShowWY ? TotalAmount/10000+"" : TotalAmount.ToString()
        # C# decimal.ToString() 整数时不带小数点
        def dec_to_str(v):
            if v == int(v):
                return str(int(v))
            return str(v)
        value_str = dec_to_str(total_amount / 10000) if show_wy else dec_to_str(total_amount)
        # C#对齐: data = ShowLargeUnit ? TotalCount/1000+"" : TotalCount.ToString()
        data_str = dec_to_str(total_count / 1000) if show_large_unit else dec_to_str(total_count)

        return Result.success(data={
            "data": data_str, "key": str(data_type),
            "name": name if name else None,
            "value": value_str
        }, msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetEnergyRevenueInfo AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== _bayonet_owner_ah_tree_detail (dataType=1时调用) =====
async def _bayonet_owner_ah_tree_detail(db, sp_id: int, start_month: int, end_month: int,
                                         rank_num, page_index, page_size):
    """C# GetBayonetOwnerAHTreeDetail: 服务区→省份→城市 树形"""
    # 查询该服务区的车辆归属地明细数据（含省份、城市）
    sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE","PROVINCE_NAME","CITY_NAME",
            SUM(ROUND("VEHICLE_COUNT" * "ANOLOG_RATIO")) AS "VEHICLE_COUNT"
        FROM "T_BAYONETOWMONTHLY_AH"
        WHERE "STATISTICS_MONTH" BETWEEN {start_month} AND {end_month} AND "SERVERPART_ID" = {sp_id}
        GROUP BY "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE","PROVINCE_NAME","CITY_NAME" """
    dt_bayonet = db.execute_query(sql) or []
    if not dt_bayonet:
        json_list = JsonListData.create(data_list=[], total=0, page_size=page_size or 10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    # 查询服务区断面流量
    sql_sf = f"""SELECT "SERVERPART_ID","SERVERPART_REGION",SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
        FROM "T_SECTIONFLOW"
        WHERE "STATISTICS_DATE" BETWEEN {start_month}01 AND {end_month}31
            AND "SERVERPART_ID" = {sp_id}
        GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
    dt_sf = db.execute_query(sql_sf) or []

    # 查询服务区基本信息
    sql_sp = f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME","SPREGIONTYPE_INDEX"
        FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {sp_id}"""
    dt_sp = db.execute_query(sql_sp) or []

    east = "东南"
    west = "西北"

    def safe_int(v):
        try: return int(v) if v is not None else 0
        except: return 0

    def count_vehicles(rows, vtype_contains, region_set):
        """统计指定车型+方位的车辆数"""
        return sum(safe_int(r.get("VEHICLE_COUNT")) for r in rows
                   if vtype_contains in str(r.get("VEHICLE_TYPE", ""))
                   and str(r.get("SERVERPART_REGION", "")) in region_set)

    # 构建服务区根节点 (ServerPartLevel=0)
    sp_info = dt_sp[0] if dt_sp else {}
    east_light = count_vehicles(dt_bayonet, "小", east)
    east_mid = count_vehicles(dt_bayonet, "中", east)
    east_large = count_vehicles(dt_bayonet, "大", east)
    west_light = count_vehicles(dt_bayonet, "小", west)
    west_mid = count_vehicles(dt_bayonet, "中", west)
    west_large = count_vehicles(dt_bayonet, "大", west)
    total_count = sum(safe_int(r.get("VEHICLE_COUNT")) for r in dt_bayonet)

    # 断面流量
    sf_total = sum(safe_int(r.get("SECTIONFLOW_NUM")) for r in dt_sf)
    sf_east = sum(safe_int(r.get("SECTIONFLOW_NUM")) for r in dt_sf if str(r.get("SERVERPART_REGION", "")) in east)
    sf_west = sum(safe_int(r.get("SECTIONFLOW_NUM")) for r in dt_sf if str(r.get("SERVERPART_REGION", "")) in west)
    section_flow = {"total": float(sf_total), "RegionA": float(sf_east), "RegionB": float(sf_west)} if dt_sf else None
    entry_rate = None
    if section_flow and sf_total and sf_total > 0:
        entry_rate = {
            "total": round(total_count / sf_total * 100, 2),
            "RegionA": round((east_light + east_mid + east_large) / sf_east * 100, 2) if sf_east > 0 else None,
            "RegionB": round((west_light + west_mid + west_large) / sf_west * 100, 2) if sf_west > 0 else None,
        }

    root_node = {
        "Index": 1,
        "ServerPartLevel": 0,
        "SPRegionTypeIndex": safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
        "SPRegionTypeId": safe_int(sp_info.get("SPREGIONTYPE_ID")),
        "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
        "ServerPartId": safe_int(sp_info.get("SERVERPART_ID")),
        "ServerPartName": sp_info.get("SERVERPART_NAME"),
        "ProvinceName": None,
        "CityName": None,
        "SectionFlow": section_flow,
        "EntryRate": entry_rate,
        "EastLightDutyCount": east_light,
        "EastMidSizeCount": east_mid,
        "EastLargeCount": east_large,
        "WestLightDutyCount": west_light,
        "WestMidSizeCount": west_mid,
        "WestLargeCount": west_large,
        "LightDutyTotalCount": east_light + west_light,
        "MidSizeTotalCount": east_mid + west_mid,
        "LargeTotalCount": east_large + west_large,
        "TotalCount": total_count,
    }

    # 按省份分组，构建省份children
    from collections import defaultdict
    prov_map = defaultdict(list)
    for r in dt_bayonet:
        pn = str(r.get("PROVINCE_NAME") or "")
        prov_map[pn].append(r)

    # 省份按总量降序排
    prov_sorted = sorted(prov_map.items(), key=lambda x: sum(safe_int(r.get("VEHICLE_COUNT")) for r in x[1]), reverse=True)

    province_children = []
    for prov_name_raw, prov_rows in prov_sorted:
        prov_name = prov_name_raw if prov_name_raw else "其他"
        p_total = sum(safe_int(r.get("VEHICLE_COUNT")) for r in prov_rows)
        prov_node = {
            "Index": 999 if not prov_name_raw else 1,
            "ServerPartLevel": 1,
            "SPRegionTypeIndex": safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
            "SPRegionTypeId": safe_int(sp_info.get("SPREGIONTYPE_ID")),
            "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
            "ServerPartId": sp_id,
            "ServerPartName": sp_info.get("SERVERPART_NAME"),
            "ProvinceName": prov_name,
            "CityName": None,
            "SectionFlow": None,
            "EntryRate": None,
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

        # 城市children
        city_map = defaultdict(list)
        for r in prov_rows:
            cn = str(r.get("CITY_NAME") or "")
            city_map[cn].append(r)
        city_sorted = sorted(city_map.items(), key=lambda x: sum(safe_int(r.get("VEHICLE_COUNT")) for r in x[1]), reverse=True)

        city_children = []
        if rank_num and rank_num > 0 and len(city_sorted) >= rank_num:
            # 取Top N
            top_cities = [c for c in city_sorted if c[0]][:rank_num]
            top_total = 0
            top_el = 0; top_em = 0; top_ea = 0
            top_wl = 0; top_wm = 0; top_wa = 0
            for city_name, city_rows in top_cities:
                c_total = sum(safe_int(r.get("VEHICLE_COUNT")) for r in city_rows)
                cel = count_vehicles(city_rows, "小", east)
                cem = count_vehicles(city_rows, "中", east)
                cea = count_vehicles(city_rows, "大", east)
                cwl = count_vehicles(city_rows, "小", west)
                cwm = count_vehicles(city_rows, "中", west)
                cwa = count_vehicles(city_rows, "大", west)
                top_total += c_total
                top_el += cel; top_em += cem; top_ea += cea
                top_wl += cwl; top_wm += cwm; top_wa += cwa
                city_children.append({"node": {
                    "Index": 1, "ServerPartLevel": 2,
                    "SPRegionTypeIndex": safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
                    "SPRegionTypeId": safe_int(sp_info.get("SPREGIONTYPE_ID")),
                    "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
                    "ServerPartId": sp_id, "ServerPartName": sp_info.get("SERVERPART_NAME"),
                    "ProvinceName": prov_name, "CityName": city_name,
                    "SectionFlow": None, "EntryRate": None,
                    "EastLightDutyCount": cel, "EastMidSizeCount": cem, "EastLargeCount": cea,
                    "WestLightDutyCount": cwl, "WestMidSizeCount": cwm, "WestLargeCount": cwa,
                    "LightDutyTotalCount": cel+cwl, "MidSizeTotalCount": cem+cwm, "LargeTotalCount": cea+cwa,
                    "TotalCount": c_total,
                }, "children": None})
            # 添加其余为"其他"
            other_el = max(0, prov_node["EastLightDutyCount"] - top_el)
            other_em = max(0, prov_node["EastMidSizeCount"] - top_em)
            other_ea = max(0, prov_node["EastLargeCount"] - top_ea)
            other_wl = max(0, prov_node["WestLightDutyCount"] - top_wl)
            other_wm = max(0, prov_node["WestMidSizeCount"] - top_wm)
            other_wa = max(0, prov_node["WestLargeCount"] - top_wa)
            city_children.append({"node": {
                "Index": 999, "ServerPartLevel": 2,
                "SPRegionTypeIndex": safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
                "SPRegionTypeId": safe_int(sp_info.get("SPREGIONTYPE_ID")),
                "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
                "ServerPartId": sp_id, "ServerPartName": sp_info.get("SERVERPART_NAME"),
                "ProvinceName": prov_name, "CityName": "其他",
                "SectionFlow": None, "EntryRate": None,
                "EastLightDutyCount": other_el, "EastMidSizeCount": other_em, "EastLargeCount": other_ea,
                "WestLightDutyCount": other_wl, "WestMidSizeCount": other_wm, "WestLargeCount": other_wa,
                "LightDutyTotalCount": other_el+other_wl, "MidSizeTotalCount": other_em+other_wm, "LargeTotalCount": other_ea+other_wa,
                "TotalCount": p_total - top_total,
            }, "children": []})
        else:
            for city_name_raw, city_rows in city_sorted:
                city_name = city_name_raw if city_name_raw else "其他"
                c_total = sum(safe_int(r.get("VEHICLE_COUNT")) for r in city_rows)
                cel = count_vehicles(city_rows, "小", east)
                cem = count_vehicles(city_rows, "中", east)
                cea = count_vehicles(city_rows, "大", east)
                cwl = count_vehicles(city_rows, "小", west)
                cwm = count_vehicles(city_rows, "中", west)
                cwa = count_vehicles(city_rows, "大", west)
                city_children.append({"node": {
                    "Index": 999 if not city_name_raw else 1,
                    "ServerPartLevel": 2,
                    "SPRegionTypeIndex": safe_int(sp_info.get("SPREGIONTYPE_INDEX")),
                    "SPRegionTypeId": safe_int(sp_info.get("SPREGIONTYPE_ID")),
                    "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
                    "ServerPartId": sp_id, "ServerPartName": sp_info.get("SERVERPART_NAME"),
                    "ProvinceName": prov_name, "CityName": city_name,
                    "SectionFlow": None, "EntryRate": None,
                    "EastLightDutyCount": cel, "EastMidSizeCount": cem, "EastLargeCount": cea,
                    "WestLightDutyCount": cwl, "WestMidSizeCount": cwm, "WestLargeCount": cwa,
                    "LightDutyTotalCount": cel+cwl, "MidSizeTotalCount": cem+cwm, "LargeTotalCount": cea+cwa,
                    "TotalCount": c_total,
                }, "children": None})
        # 城市排序: Index升序, TotalCount降序
        city_children.sort(key=lambda x: (x["node"]["Index"], -(x["node"]["TotalCount"] or 0)))

        province_children.append({"node": prov_node, "children": city_children})

    # 省份排序: Index升序, TotalCount降序
    province_children.sort(key=lambda x: (x["node"]["Index"], -(x["node"]["TotalCount"] or 0)))

    result_list = [{"node": root_node, "children": province_children}]
    json_list = JsonListData.create(data_list=result_list, total=len(result_list),
                                     page_index=page_index or 1, page_size=page_size or 10)
    return Result.success(data=json_list.model_dump())


# ===== GetBayonetOwnerAHTreeList =====
@router.get("/BigData/GetBayonetOwnerAHTreeList")
async def get_bayonet_owner_ah_tree_list(
    dataType: int = Query(..., description="数据类型: 1=明细, 其他=汇总"),
    serverPartId: str = Query(..., description="服务区内码"),
    statisticsStartMonth: int = Query(..., description="开始日期(yyyyMM)"),
    statisticsEndMonth: int = Query(..., description="结束日期(yyyyMM)"),
    rankNum: Optional[int] = Query(None, description="城市top排名"),
    isSync: bool = Query(True, description="是否异步执行"),
    pageIndex: Optional[int] = Query(1, description="页码"),
    pageSize: Optional[int] = Query(10, description="每页条数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽卡口所有者树形数据"""
    try:
        # dataType=1: 明细模式（C# GetBayonetOwnerAHTreeDetail）
        if dataType == 1:
            if not serverPartId:
                return Result.fail(code=200, msg="查询失败：服务区信息不能为空")
            sp_id = serverPartId.split(",")[0].strip()
            return await _bayonet_owner_ah_tree_detail(db, int(sp_id), statisticsStartMonth, statisticsEndMonth, rankNum, pageIndex, pageSize)

        # dataType!=1: 汇总模式（C# GetBayonetOwnerAHTreeList）
        # 构建过滤条件
        where_sql = ""
        if serverPartId:
            where_sql = f' AND "SERVERPART_ID" IN ({serverPartId})'

        # 1. 查询车辆归属地月度固化数据
        if isSync:
            sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE",
                    SUM(ROUND("VEHICLE_COUNT" * "ANOLOG_RATIO")) AS "VEHICLE_COUNT"
                FROM "T_BAYONETOWMONTHLY_AH"
                WHERE "STATISTICS_MONTH" BETWEEN {statisticsStartMonth} AND {statisticsEndMonth}{where_sql}
                GROUP BY "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE" """
        else:
            sql = f"""SELECT "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE","PROVINCE_NAME",
                    SUM(ROUND("VEHICLE_COUNT" * "ANOLOG_RATIO")) AS "VEHICLE_COUNT"
                FROM "T_BAYONETOWMONTHLY_AH"
                WHERE "STATISTICS_MONTH" BETWEEN {statisticsStartMonth} AND {statisticsEndMonth}{where_sql}
                GROUP BY "SERVERPART_ID","SERVERPART_REGION","VEHICLE_TYPE","PROVINCE_NAME" """
        dt_bayonet = db.execute_query(sql) or []

        if not dt_bayonet:
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 2. 查断面流量
        sql_sf = f"""SELECT "SERVERPART_ID","SERVERPART_REGION",SUM("SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
            FROM "T_SECTIONFLOW"
            WHERE "STATISTICS_DATE" BETWEEN {statisticsStartMonth}01 AND {statisticsEndMonth}31{where_sql}
            GROUP BY "SERVERPART_ID","SERVERPART_REGION" """
        dt_section = db.execute_query(sql_sf) or []

        # 3. 查服务区信息
        sp_ids = list(set(str(r["SERVERPART_ID"]) for r in dt_bayonet if r.get("SERVERPART_ID")))
        sql_sp = f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME","SPREGIONTYPE_INDEX"
            FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({','.join(sp_ids)})"""
        dt_sp = db.execute_query(sql_sp) or []
        sp_map = {str(r["SERVERPART_ID"]): r for r in dt_sp}

        # 辅助函数: 按方位+车型统计
        def calc_counts(rows):
            east = "东南"
            west = "西北"
            counts = {"EastLightDutyCount": 0, "EastMidSizeCount": 0, "EastLargeCount": 0,
                      "WestLightDutyCount": 0, "WestMidSizeCount": 0, "WestLargeCount": 0, "TotalCount": 0}
            for r in rows:
                vt = str(r.get("VEHICLE_TYPE", ""))
                region = str(r.get("SERVERPART_REGION", ""))
                vc = int(r.get("VEHICLE_COUNT") or 0)
                counts["TotalCount"] += vc
                is_east = region in east
                is_west = region in west
                if "小" in vt:
                    if is_east: counts["EastLightDutyCount"] += vc
                    if is_west: counts["WestLightDutyCount"] += vc
                elif "中" in vt:
                    if is_east: counts["EastMidSizeCount"] += vc
                    if is_west: counts["WestMidSizeCount"] += vc
                elif "大" in vt:
                    if is_east: counts["EastLargeCount"] += vc
                    if is_west: counts["WestLargeCount"] += vc
            # 添加计算字段(东+西合计)
            counts["LightDutyTotalCount"] = counts["EastLightDutyCount"] + counts["WestLightDutyCount"]
            counts["MidSizeTotalCount"] = counts["EastMidSizeCount"] + counts["WestMidSizeCount"]
            counts["LargeTotalCount"] = counts["EastLargeCount"] + counts["WestLargeCount"]
            return counts

        # 4. 按服务区分组
        from collections import defaultdict
        sp_groups = defaultdict(list)
        for r in dt_bayonet:
            sp_groups[str(r["SERVERPART_ID"])].append(r)

        sf_groups = defaultdict(list)
        for r in dt_section:
            sf_groups[str(r["SERVERPART_ID"])].append(r)

        # 构建服务区节点
        sp_nodes = []
        for sp_id, rows in sp_groups.items():
            sp_info = sp_map.get(sp_id, {})
            counts = calc_counts(rows)
            sf_rows = sf_groups.get(sp_id, [])
            sf_total = sum(int(r.get("SECTIONFLOW_NUM") or 0) for r in sf_rows)

            east_chars = "东南"
            west_chars = "西北"
            sf_east = sum(int(r.get("SECTIONFLOW_NUM") or 0) for r in sf_rows if str(r.get("SERVERPART_REGION","")) in east_chars)
            sf_west = sum(int(r.get("SECTIONFLOW_NUM") or 0) for r in sf_rows if str(r.get("SERVERPART_REGION","")) in west_chars)

            node = {
                "Index": 1,
                "ServerPartLevel": 0,
                "SPRegionTypeIndex": sp_info.get("SPREGIONTYPE_INDEX"),
                "SPRegionTypeId": sp_info.get("SPREGIONTYPE_ID"),
                "SPRegionTypeNAME": sp_info.get("SPREGIONTYPE_NAME"),
                "ServerPartId": sp_info.get("SERVERPART_ID"),
                "ServerPartName": sp_info.get("SERVERPART_NAME"),
                "ProvinceName": None,
                "CityName": None,
                "SectionFlow": {"total": None, "RegionA": None, "RegionB": None},
                "EntryRate": {"total": None, "RegionA": None, "RegionB": None},
                **counts,
            }
            if sf_total > 0:
                node["SectionFlow"] = {"total": sf_total, "RegionA": sf_east, "RegionB": sf_west}
                entry_total = round(counts["TotalCount"] / sf_total * 100, 2) if sf_total > 0 else 0
                east_vc = sum(int(r.get("VEHICLE_COUNT") or 0) for r in rows if str(r.get("SERVERPART_REGION","")) in east_chars)
                west_vc = sum(int(r.get("VEHICLE_COUNT") or 0) for r in rows if str(r.get("SERVERPART_REGION","")) in west_chars)
                node["EntryRate"] = {
                    "total": entry_total,
                    "RegionA": round(east_vc / sf_east * 100, 2) if sf_east > 0 else None,
                    "RegionB": round(west_vc / sf_west * 100, 2) if sf_west > 0 else None,
                }
            sp_nodes.append({"node": node, "children": []})

        # 5. 按片区分组构建树
        region_groups = defaultdict(list)
        for sn in sp_nodes:
            key = (sn["node"].get("SPRegionTypeId"), sn["node"].get("SPRegionTypeNAME"))
            region_groups[key].append(sn)

        center_list = []
        for (rt_id, rt_name), children in region_groups.items():
            children.sort(key=lambda x: x["node"]["TotalCount"] or 0, reverse=True)
            east_light = sum(c["node"]["EastLightDutyCount"] for c in children)
            east_mid = sum(c["node"]["EastMidSizeCount"] for c in children)
            east_large = sum(c["node"]["EastLargeCount"] for c in children)
            west_light = sum(c["node"]["WestLightDutyCount"] for c in children)
            west_mid = sum(c["node"]["WestMidSizeCount"] for c in children)
            west_large = sum(c["node"]["WestLargeCount"] for c in children)
            center_node = {
                "Index": 1,
                "ServerPartLevel": -1,
                "SPRegionTypeIndex": children[0]["node"].get("SPRegionTypeIndex") if children else None,
                "SPRegionTypeId": rt_id,
                "SPRegionTypeNAME": rt_name,
                "ServerPartId": None,
                "ServerPartName": None,
                "ProvinceName": None,
                "CityName": None,
                "SectionFlow": {"total": None, "RegionA": None, "RegionB": None},
                "EntryRate": {"total": None, "RegionA": None, "RegionB": None},
                "EastLightDutyCount": east_light,
                "EastMidSizeCount": east_mid,
                "EastLargeCount": east_large,
                "WestLightDutyCount": west_light,
                "WestMidSizeCount": west_mid,
                "WestLargeCount": west_large,
                "LightDutyTotalCount": east_light + west_light,
                "MidSizeTotalCount": east_mid + west_mid,
                "LargeTotalCount": east_large + west_large,
                "TotalCount": sum(c["node"]["TotalCount"] for c in children),
            }
            center_list.append({"node": center_node, "children": children})

        center_list.sort(key=lambda x: (x["node"].get("SPRegionTypeIndex") or 99, -(x["node"]["TotalCount"] or 0)))

        # 分页
        total = len(center_list)
        start = (pageIndex - 1) * pageSize
        paged = center_list[start:start + pageSize]

        json_list = JsonListData.create(data_list=paged, total=total, page_size=10)
        return Result.success(data=json_list.model_dump(), msg="成功")
    except Exception as ex:
        logger.error(f"GetBayonetOwnerAHTreeList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetProvinceVehicleTreeList =====
@router.get("/BigData/GetProvinceVehicleTreeList")
async def get_province_vehicle_tree_list(
    serverPartId: Optional[str] = Query("", description="服务区内码集合"),
    statisticsStartMonth: int = Query(..., description="开始日期(yyyyMM)"),
    statisticsEndMonth: int = Query(..., description="结束日期(yyyyMM)"),
    rankNum: Optional[int] = Query(None, description="城市top排名"),
    pageIndex: Optional[int] = Query(1, description="页码"),
    pageSize: Optional[int] = Query(10, description="每页条数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取各省入区车辆统计表(树形)"""
    try:
        from collections import defaultdict

        where_sql = ""
        if serverPartId:
            where_sql = f' AND T."SERVERPART_ID" IN ({serverPartId})'

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
            sp_where = f" OR \"SERVERPART_ID\" IN ({serverPartId})"
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
    except Exception as ex:
        logger.error(f"GetProvinceVehicleTreeList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetProvinceVehicleDetail =====
# C# 返回 List<SPRegionTypeModel>，是"服务区×城市"交叉组合的平铺列表
@router.get("/BigData/GetProvinceVehicleDetail")
async def get_province_vehicle_detail(
    statisticsStartMonth: int = Query(..., description="开始日期(yyyyMM)"),
    statisticsEndMonth: int = Query(..., description="结束日期(yyyyMM)"),
    provinceName: str = Query(..., description="省份名称"),
    serverPartId: Optional[str] = Query("", description="服务区内码"),
    cityName: Optional[str] = Query("", description="城市名称"),
    rankNum: Optional[int] = Query(None, description="城市top排名"),
    pageIndex: Optional[int] = Query(1, description="页码"),
    pageSize: Optional[int] = Query(10, description="每页条数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取各省入区车辆统计表明细（对齐C# BayonetHelper.GetProvinceVehicleDetail）"""
    try:
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
        if serverPartId:
            where_sql += f""" AND "SERVERPART_ID" IN ({serverPartId})"""
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
    except Exception as ex:
        logger.error(f"GetProvinceVehicleDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


