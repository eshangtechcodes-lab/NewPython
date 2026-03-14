# -*- coding: utf-8 -*-
"""
CommercialApi - BigData 路由
对应原 C# CommercialApi/Controllers/BigDataController.cs
大数据分析相关接口（车流分析、归属地分析、预警等）

Service 文件清单:
  bigdata_bayonet_service   — 卡口入区/停留/归属地分析 (8路由)
  bigdata_month_service     — 月度车流分析 (2路由)
  bigdata_warning_service   — 预警/增长/对比分析 (6路由)
  bigdata_detail_service    — 日分析/能源/车辆树 (6路由)
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from models.base import Result, JsonListData
from routers.deps import get_db, parse_multi_ids, build_in_condition
from core.database import DatabaseHelper

router = APIRouter()

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
    """业务逻辑见 bigdata_detail_service.get_revenue_trend_chart()"""

    try:

        from services.commercial import bigdata_detail_service

        data = bigdata_detail_service.get_revenue_trend_chart(db, postData)

        json_list = JsonListData.create(

            data_list=data if isinstance(data, list) else [data],

            total=len(data) if isinstance(data, list) else 1)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetRevenueTrendChart 查询失败: {ex}")

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
    """业务逻辑见 bigdata_detail_service.get_province_vehicle_tree_list()"""

    try:

        from services.commercial import bigdata_detail_service

        data = bigdata_detail_service.get_province_vehicle_tree_list(db, serverPartId, statisticsStartMonth, statisticsEndMonth, rankNum, pageIndex, pageSize)

        json_list = JsonListData.create(

            data_list=data if isinstance(data, list) else [data],

            total=len(data) if isinstance(data, list) else 1)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetProvinceVehicleTreeList 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")





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
    """业务逻辑见 bigdata_detail_service.get_province_vehicle_detail()"""

    try:

        from services.commercial import bigdata_detail_service

        data = bigdata_detail_service.get_province_vehicle_detail(db, statisticsStartMonth, statisticsEndMonth, provinceName, serverPartId, cityName, rankNum, pageIndex, pageSize)

        json_list = JsonListData.create(

            data_list=data if isinstance(data, list) else [data],

            total=len(data) if isinstance(data, list) else 1)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetProvinceVehicleDetail 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")





