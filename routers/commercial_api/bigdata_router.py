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

from config import settings
from models.base import Result, JsonListData
from routers.deps import get_db, parse_multi_ids, build_in_condition
from core.database import DatabaseHelper

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
    """业务逻辑见 bigdata_bayonet_service.get_bayonet_entry_list()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_bayonet_entry_list(db, StatisticsDate, Serverpart_ID, Serverpart_Region, ShowAddUpCount)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_bayonet_service.get_bayonet_sta_list()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_bayonet_sta_list(db, StatisticsDate, Serverpart_ID, Serverpart_Region, ContainWhole)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_bayonet_service.get_bayonet_oa_list()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_bayonet_oa_list(db, StatisticsMonth, Serverpart_ID, Serverpart_Region, OwnerCityLength, OwnerProvinceLenth, ContainWhole)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
    """业务逻辑见 bigdata_bayonet_service.get_bayonet_province_oa_list()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_bayonet_province_oa_list(db, StatisticsMonth, Serverpart_ID, Serverpart_Region, OwnerCityLength, ContainWhole, isExclude)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
    """业务逻辑见 bigdata_bayonet_service.get_sp_bayonet_list()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_sp_bayonet_list(db, Statistics_Date, Province_Code, SPRegionType_ID, Serverpart_ID, Serverpart_Region, ShowGrowthRate, GroupType)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_bayonet_service.get_avg_bayonet_analysis()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_avg_bayonet_analysis(db, Statistics_Date, Province_Code, SPRegionType_ID, Serverpart_ID, Serverpart_Region)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAvgBayonetAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetProvinceAvgBayonetAnalysis")
async def get_province_avg_bayonet_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期/月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """业务逻辑见 bigdata_bayonet_service.get_province_avg_bayonet_analysis()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_province_avg_bayonet_analysis(db, Province_Code, Statistics_Date)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_bayonet_service.get_bayonet_st_analysis()"""
    try:
        from services.commercial import bigdata_bayonet_service
        data = bigdata_bayonet_service.get_bayonet_st_analysis(db, StartMonth, EndMonth, Province_Code, SPRegionType_ID, Serverpart_ID, TimeSpan)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_month_service.get_month_analysis()"""
    try:
        from services.commercial import bigdata_month_service
        data = bigdata_month_service.get_month_analysis(db, ProvinceCode, StatisticsDate, StartDate, EndDate, SPRegionType_ID, Serverpart_ID, Serverpart_Region, ServerpartShopIds)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
    """业务逻辑见 bigdata_month_service.get_province_month_analysis()"""
    try:
        from services.commercial import bigdata_month_service
        data = bigdata_month_service.get_province_month_analysis(db, StatisticsMonth, ProvinceCode, SPRegion_ID, Serverpart_ID, SortStr, FromRedis)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_warning_service.get_bayonet_warning()"""
    try:
        from services.commercial import bigdata_warning_service
        data = bigdata_warning_service.get_bayonet_warning(db, StatisticsDate, StatisticsHour, StatisticsType, ShowCount)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_warning_service.get_holiday_bayonet_warning()"""
    try:
        from services.commercial import bigdata_warning_service
        data = bigdata_warning_service.get_holiday_bayonet_warning(db, StatisticsDate, StatisticsHour, StatisticsType, HolidayType, curYear, compareYear, ShowCount)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
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
    """业务逻辑见 bigdata_warning_service.get_bayonet_growth_analysis()"""
    try:
        from services.commercial import bigdata_warning_service
        data = bigdata_warning_service.get_bayonet_growth_analysis(db, pushProvinceCode, StatisticsStartDate, StatisticsEndDate, SPRegionType_ID, Serverpart_ID, Serverpart_Region, ShowGrowthRate)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
    """业务逻辑见 bigdata_warning_service.get_bayonet_compare()"""
    try:
        from services.commercial import bigdata_warning_service
        data = bigdata_warning_service.get_bayonet_compare(db, pushProvinceCode, StatisticsStartDate, StatisticsEndDate, CompareStartDate, CompareEndDate, SPRegionType_ID, Serverpart_ID, Serverpart_Region)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
    """业务逻辑见 bigdata_warning_service.get_holiday_compare()"""
    try:
        from services.commercial import bigdata_warning_service
        data = bigdata_warning_service.get_holiday_compare(db, pushProvinceCode, holidayType, curYear, compareYear, SPRegionType_ID, Serverpart_ID, Serverpart_Region)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidayCompare 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BigData/GetBayonetOAAnalysis")
async def get_bayonet_oa_analysis(
    HolidayType: int = Query(0, description="节日类型：0全部 1节假日 2非节假日"),
    StartMonth: Optional[str] = Query(None, description="统计开始月份，格式yyyyMM"),
    EndMonth: Optional[str] = Query(None, description="统计结束月份，格式yyyyMM"),
    VehicleType: Optional[str] = Query("", description="车辆类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """业务逻辑见 bigdata_warning_service.get_bayonet_oa_analysis()"""
    try:
        from services.commercial import bigdata_warning_service
        data = bigdata_warning_service.get_bayonet_oa_analysis(db, HolidayType, StartMonth, EndMonth, VehicleType)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
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
    """业务逻辑见 bigdata_detail_service.get_date_analysis()"""
    try:
        from services.commercial import bigdata_detail_service
        data = bigdata_detail_service.get_date_analysis(db, StartDate, EndDate, Serverpart_ID)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetDateAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


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
        except Exception as redis_ex:
            logger.warning(
                f"GetRevenueTrendChart Redis unavailable: "
                f"{settings.REDIS_HOST}:{settings.REDIS_PORT}/db{settings.REDIS_REVENUE_TREND_DB} {redis_ex}"
            )

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
    """业务逻辑见 bigdata_detail_service.get_energy_revenue_info()"""
    try:
        from services.commercial import bigdata_detail_service
        data = bigdata_detail_service.get_energy_revenue_info(db)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEnergyRevenueInfo 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


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
    """业务逻辑见 bigdata_detail_service.get_bayonet_owner_ah_tree_list()"""
    try:
        from services.commercial import bigdata_detail_service
        data = bigdata_detail_service.get_bayonet_owner_ah_tree_list(db, dataType, serverPartId, statisticsStartMonth, statisticsEndMonth, rankNum, isSync, pageIndex, pageSize)
        json_list = JsonListData.create(
            data_list=data if isinstance(data, list) else [data],
            total=len(data) if isinstance(data, list) else 1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBayonetOwnerAHTreeList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


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
    except Exception as ex:
        logger.error(f"GetProvinceVehicleDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


