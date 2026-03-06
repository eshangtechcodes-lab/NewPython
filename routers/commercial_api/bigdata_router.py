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
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


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
    prov_sorted = sorted(prov_map.items(), key=lambda x: x[1], reverse=True)[:prov_top]
    prov_list = [{"name": p[0], "value": str(int(p[1]))} for p in prov_sorted]

    return {
        "Serverpart_ID": sp_id,
        "Serverpart_Name": sp_name,
        "Serverpart_Region": region,
        "OwnerCityList": city_list,
        "OwnerProvinceList": prov_list,
    }


def _build_province_oa_model(city_rows, prov_rows, sp_id, sp_name, region, city_top, is_exclude):
    """构建省份归属地分析模型（省份->城市嵌套）"""
    # 省份聚合
    prov_map = {}
    for r in prov_rows:
        pn = r.get("PROVINCE_NAME") or ""
        prov_map[pn] = prov_map.get(pn, 0) + float(r.get("VEHICLE_COUNT") or 0)
    prov_sorted = sorted(prov_map.items(), key=lambda x: x[1], reverse=True)

    prov_list = []
    for pn, pv in prov_sorted:
        # 省内城市排名
        p_cities = {}
        for r in city_rows:
            if r.get("PROVINCE_NAME") == pn:
                cn = r.get("CITY_NAME") or ""
                p_cities[cn] = p_cities.get(cn, 0) + float(r.get("VEHICLE_COUNT") or 0)
        city_sorted = sorted(p_cities.items(), key=lambda x: x[1], reverse=True)[:city_top]
        prov_list.append({
            "name": pn,
            "value": str(int(pv)),
            "CityList": [{"name": c[0], "value": str(int(c[1]))} for c in city_sorted],
        })

    return {
        "Serverpart_ID": sp_id,
        "Serverpart_Name": sp_name,
        "Serverpart_Region": region,
        "ProvinceList": prov_list,
    }


@router.get("/BigData/GetBayonetEntryList")
async def get_bayonet_entry_list(
    StatisticsDate: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowAddUpCount: bool = Query(False, description="是否统计累计数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """服务区入区车流分析"""
    try:
        logger.warning("GetBayonetEntryList 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetSTAList")
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


@router.get("/BigData/GetBayonetOAList")
async def get_bayonet_oa_list(
    StatisticsMonth: Optional[str] = Query(None, description="统计月份，格式yyyyMM"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    OwnerCityLength: int = Query(10, description="显示车牌所在城市数量"),
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
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetOAList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetProvinceOAList")
async def get_bayonet_province_oa_list(
    StatisticsMonth: Optional[str] = Query(None, description="统计月份，格式yyyyMM"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    OwnerCityLength: int = Query(10, description="显示城市数量"),
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
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetProvinceOAList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetSPBayonetList")
async def get_sp_bayonet_list(
    Statistics_Date: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowServerpartRegion: bool = Query(False, description="是否显示服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车流量分析"""
    try:
        logger.warning("GetSPBayonetList 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetRankList")
async def get_bayonet_rank_list(
    Statistics_Date: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ShowServerpartRegion: bool = Query(False, description="是否显示服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车流量排行"""
    try:
        logger.warning("GetBayonetRankList 暂未完整实现")
        return Result.fail(code=200, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetAvgBayonetAnalysis")
async def get_avg_bayonet_analysis(
    Statistics_Date: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区平均车流量分析"""
    try:
        logger.warning("GetAvgBayonetAnalysis 暂未完整实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetProvinceAvgBayonetAnalysis")
async def get_province_avg_bayonet_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期/月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取全省平均车流量分析"""
    try:
        logger.warning("GetProvinceAvgBayonetAnalysis 暂未完整实现")
        return Result.success(data={}, msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetSTAnalysis")
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
                out_time = min(slot * TimeSpan, 24)
                slot_row = next((r for r in vt_rows if r.get("STATISTICS_HOUR") == slot), None)
                stay = 0
                if slot_row:
                    count = int(slot_row.get("STAY_TIMESCOUNT") or 0)
                    if count > 0:
                        stay = round(float(slot_row.get("STAY_TIMESTOTAL") or 0) / count / 3600, 2)
                    else:
                        stay = round(float(slot_row.get("STAY_TIMES") or 0) / 3600, 2)
                data.append([out_time, stay])
            result_list.append({"name": vt, "data": data})

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetSTAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetMonthAnalysis")
async def get_month_analysis(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期，格式yyyy-MM-dd"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    ServerpartShopIds: Optional[str] = Query("", description="门店内码集合"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度车流分析数据"""
    try:
        logger.warning("GetMonthAnalysis 暂未完整实现")
        return Result.success(data={}, msg="查询成功")
    except Exception as ex:
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
            "B"."SPREGIONTYPE_NAME", "B"."SERVERPART_ID", "B"."SERVERPART_NAME",
            COUNT(DISTINCT "A"."STATISTICS_DATE") AS "DATE_COUNT",
            SUM("A"."SERVERPART_FLOW") AS "VEHICLE_COUNT",
            SUM("A"."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
        FROM "T_SECTIONFLOW" "A", "T_SERVERPART" "B"
        WHERE "A"."SERVERPART_ID" = "B"."SERVERPART_ID" AND {where_sql}
        GROUP BY "B"."SPREGIONTYPE_NAME", "B"."SERVERPART_ID", "B"."SERVERPART_NAME"
        """
        rows = db.execute_query(sql, params if params else None)

        if not rows:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 计算月度天数
        year = int(StatisticsMonth[:4])
        month = int(StatisticsMonth[4:6])
        import calendar
        from datetime import datetime
        now = datetime.now()
        # 如果是当月，用昨天的天数
        if StatisticsMonth == now.strftime("%Y%m"):
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

            model = {
                "Statistics_Year": year,
                "Statistics_Month": month,
                "SPRegionType_Name": r.get("SPREGIONTYPE_NAME"),
                "Serverpart_ID": r.get("SERVERPART_ID"),
                "Serverpart_Name": r.get("SERVERPART_NAME"),
                "Vehicle_Count": total_vehicle,
                "SectionFlow_Count": total_section,
                "Entry_Rate": entry_rate,
                "RevenueAmount": None,
                "AvgVehicleAmount": None,
            }
            result_list.append(model)

        # 排序
        if SortStr:
            sort_field = SortStr.split(" ")[0]
            desc = SortStr.lower().endswith(" desc")
            if sort_field in ["SectionFlow_Count", "Vehicle_Count", "Entry_Rate"]:
                result_list.sort(key=lambda x: x.get(sort_field) or 0, reverse=desc)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
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
    """获取车流预警数据"""
    try:
        logger.warning("GetBayonetWarning 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetHolidayBayonetWarning")
async def get_holiday_bayonet_warning(
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    StatisticsHour: Optional[str] = Query("", description="统计时段"),
    StatisticsType: int = Query(1, description="统计方式"),
    curYear: Optional[str] = Query("", description="本年年份"),
    compareYear: Optional[str] = Query("", description="历年年份"),
    ShowCount: int = Query(20, description="排行显示行数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日车流预警数据"""
    try:
        logger.warning("GetHolidayBayonetWarning 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
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
    """获取当日服务区车流量分析"""
    try:
        logger.warning("GetBayonetGrowthAnalysis 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetCompare")
async def get_bayonet_compare(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsStartDate: Optional[str] = Query(None, description="统计开始日期"),
    StatisticsEndDate: Optional[str] = Query(None, description="统计结束日期"),
    CompareStartDate: Optional[str] = Query("", description="对比开始日期"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区车流量同比分析"""
    try:
        logger.warning("GetBayonetCompare 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetHolidayCompare")
async def get_holiday_compare(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    holidayType: int = Query(0, description="节日类型"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Serverpart_Region: Optional[str] = Query("", description="服务区方位"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日服务区平均入区流量对比数据"""
    try:
        logger.warning("GetHolidayCompare 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetOAAnalysis")
async def get_bayonet_oa_analysis(
    HolidayType: int = Query(0, description="节日类型：0全部 1节假日 2非节假日"),
    StartMonth: Optional[str] = Query(None, description="统计开始月份，格式yyyyMM"),
    EndMonth: Optional[str] = Query(None, description="统计结束月份，格式yyyyMM"),
    VehicleType: Optional[str] = Query("", description="车辆类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取日均车流归属地数据分析"""
    try:
        logger.warning("GetBayonetOAAnalysis 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
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

        # 遍历日期范围组装数据
        result_list = []
        cur_date = start_dt
        while cur_date <= end_dt:
            date_num = int(cur_date.strftime("%Y%m%d"))
            ly_date_num = int(cur_date.replace(year=cur_date.year - 1).strftime("%Y%m%d"))

            model = {
                "STATISTICS_DATE": cur_date.strftime("%m-%d"),
                "ThisYearTotalSECTIONFLOW_NUM": 0,
                "ThisYearTotalSERVERPART_FLOW": 0,
                "LastYearTotalSECTIONFLOW_NUM": 0,
                "LastYearTotalSERVERPART_FLOW": 0,
                "ThisYearSouthEastSECTIONFLOW_NUM": 0,
                "ThisYearSouthEastSERVERPART_FLOW": 0,
                "ThisYearNorthWestSECTIONFLOW_NUM": 0,
                "ThisYearNorthWestSERVERPART_FLOW": 0,
                "LastYearSouthEastSECTIONFLOW_NUM": 0,
                "LastYearSouthEastSERVERPART_FLOW": 0,
                "LastYearNorthWestSECTIONFLOW_NUM": 0,
                "LastYearNorthWestSERVERPART_FLOW": 0,
            }

            for region in ['东', '南', '西', '北']:
                # 今年数据
                r = flow_map.get((date_num, region))
                if r:
                    sf = r.get("SECTIONFLOW_NUM") or 0
                    sp = r.get("SERVERPART_FLOW") or 0
                    model["ThisYearTotalSECTIONFLOW_NUM"] += sf
                    model["ThisYearTotalSERVERPART_FLOW"] += sp
                    if region in south_east:
                        model["ThisYearSouthEastSECTIONFLOW_NUM"] += sf
                        model["ThisYearSouthEastSERVERPART_FLOW"] += sp
                    else:
                        model["ThisYearNorthWestSECTIONFLOW_NUM"] += sf
                        model["ThisYearNorthWestSERVERPART_FLOW"] += sp
                # 去年数据
                r_ly = flow_map.get((ly_date_num, region))
                if r_ly:
                    sf = r_ly.get("SECTIONFLOW_NUM") or 0
                    sp = r_ly.get("SERVERPART_FLOW") or 0
                    model["LastYearTotalSECTIONFLOW_NUM"] += sf
                    model["LastYearTotalSERVERPART_FLOW"] += sp
                    if region in south_east:
                        model["LastYearSouthEastSECTIONFLOW_NUM"] += sf
                        model["LastYearSouthEastSERVERPART_FLOW"] += sp
                    else:
                        model["LastYearNorthWestSECTIONFLOW_NUM"] += sf
                        model["LastYearNorthWestSERVERPART_FLOW"] += sp

            # 计算差值
            model["TotalDiffSECTIONFLOW_NUM"] = (
                model["ThisYearTotalSECTIONFLOW_NUM"] - model["LastYearTotalSECTIONFLOW_NUM"])
            model["TotalDiffSERVERPART_FLOW"] = (
                model["ThisYearTotalSERVERPART_FLOW"] - model["LastYearTotalSERVERPART_FLOW"])

            result_list.append(model)
            cur_date += timedelta(days=1)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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

        # TODO: 实现查询逻辑（需要 Redis）
        logger.warning("GetRevenueTrendChart 查询逻辑暂未实现（需Redis）")
        json_list = JsonListData.create(data_list=[], total=0)
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
        params = decrypt_post_data(postData)
        data_type = int(params.get("DataType", 0))
        statistics_date = params.get("StatisticsDate", "")
        logger.info(f"GetEnergyRevenueInfo 解密参数: DataType={data_type}, Date={statistics_date}")

        # TODO: 实现查询逻辑
        logger.warning("GetEnergyRevenueInfo 查询逻辑暂未实现")
        return Result.success(data={}, msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetEnergyRevenueInfo AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")

