from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BigData 模块路由（40 个接口）
包含 BigDataController (36) + CustomerController (4)
严格按照 C# BigDataController.cs 迁移

CRUD 实体:
  SECTIONFLOW / SECTIONFLOWMONTH / BAYONET / BAYONETDAILY_AH (BigData)
  BAYONETANALYSIS / BAYONETOAANALYSIS / BAYONETWARNING (Revenue路由前缀)
  CUSTOMERGROUP_AMOUNT (Customer)

散装接口:
  A2305052305180725 / GetDailyBayonetAnalysis / GetServerpartSectionFlow
  GetBayonetVehicleAnalysis / GetTimeIntervalList / GetBayonetOwnerAHList
  GetBayonetOwnerMonthAHList / GetUreaMasterList
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger
from routers.deps import get_db
from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.bigdata import bigdata_service

router = APIRouter()


# ============================================================
# 通用 CRUD 路由工厂 — 避免每个实体重复代码
# ============================================================
def _make_list_route(entity_name: str, route_path: str):
    """生成 GetXXXList 路由（POST）"""
    @router.post(route_path)
    async def _list(search_model: Optional[SearchModel] = None,
                    db: DatabaseHelper = Depends(get_db)):
        try:
            if search_model is None:
                search_model = SearchModel()
            if search_model.SearchParameter is None:
                search_model.SearchParameter = {}
            sm = search_model.model_dump()
            rows, total = bigdata_service.get_entity_list(db, entity_name, sm)
            json_list = JsonListData.create(
                data_list=rows, total=total,
                page_index=search_model.PageIndex,
                page_size=search_model.PageSize)
            return Result.success(data=json_list.model_dump(), msg="查询成功")
        except Exception as ex:
            logger.error(f"Get{entity_name}List 查询失败: {ex}")
            return Result.fail(msg="查询失败")
    _list.__name__ = f"get_{entity_name.lower()}_list"
    return _list

def _make_detail_route(entity_name: str, route_path: str, param_name: str):
    """生成 GetXXXDetail 路由（GET）"""
    @router.get(route_path)
    async def _detail(pk_val: int = Query(..., alias=param_name),
                      db: DatabaseHelper = Depends(get_db)):
        try:
            detail = bigdata_service.get_entity_detail(db, entity_name, pk_val)
            return Result.success(data=detail, msg="查询成功")
        except Exception as ex:
            logger.error(f"Get{entity_name}Detail 查询失败: {ex}")
            return Result.fail(msg="查询失败")
    _detail.__name__ = f"get_{entity_name.lower()}_detail"
    return _detail

def _make_synchro_route(entity_name: str, route_path: str):
    """生成 SynchroXXX 路由（POST）"""
    @router.post(route_path)
    async def _synchro(data: dict, db: DatabaseHelper = Depends(get_db)):
        try:
            ok, result = bigdata_service.synchro_entity(db, entity_name, data)
            if ok:
                return Result.success(data=result, msg="同步成功")
            else:
                return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
        except Exception as ex:
            logger.error(f"Synchro{entity_name} 同步失败: {ex}")
            return Result.fail(msg="同步失败")
    _synchro.__name__ = f"synchro_{entity_name.lower()}"
    return _synchro

def _make_delete_route(entity_name: str, route_path: str, param_name: str):
    """生成 DeleteXXX 路由（GET+POST，与 C# [AcceptVerbs("GET","POST")] 一致）"""
    @router.api_route(route_path, methods=["GET", "POST"])
    async def _delete(pk_val: int = Query(..., alias=param_name),
                      db: DatabaseHelper = Depends(get_db)):
        try:
            ok = bigdata_service.delete_entity(db, entity_name, pk_val)
            if ok:
                return Result.success(msg="删除成功")
            else:
                return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
        except Exception as ex:
            logger.error(f"Delete{entity_name} 删除失败: {ex}")
            return Result.fail(msg="删除失败")
    _delete.__name__ = f"delete_{entity_name.lower()}"
    return _delete


# ============================================================
# SECTIONFLOW — 断面流量表（C# BigDataController L18-159）
# 路由: BigData/GetSECTIONFLOWList(POST), GetSECTIONFLOWDetail(GET),
#       SynchroSECTIONFLOW(POST), DeleteSECTIONFLOW(GET+POST)
# ============================================================
_make_list_route("SECTIONFLOW", "/BigData/GetSECTIONFLOWList")
_make_detail_route("SECTIONFLOW", "/BigData/GetSECTIONFLOWDetail", "SECTIONFLOWId")
_make_synchro_route("SECTIONFLOW", "/BigData/SynchroSECTIONFLOW")
_make_delete_route("SECTIONFLOW", "/BigData/DeleteSECTIONFLOW", "SECTIONFLOWId")


# ============================================================
# SECTIONFLOWMONTH — 月度断面流量汇总表（C# BigDataController L161-303）
# ============================================================
_make_list_route("SECTIONFLOWMONTH", "/BigData/GetSECTIONFLOWMONTHList")
_make_detail_route("SECTIONFLOWMONTH", "/BigData/GetSECTIONFLOWMONTHDetail", "SECTIONFLOWMONTHId")
_make_synchro_route("SECTIONFLOWMONTH", "/BigData/SynchroSECTIONFLOWMONTH")
_make_delete_route("SECTIONFLOWMONTH", "/BigData/DeleteSECTIONFLOWMONTH", "SECTIONFLOWMONTHId")

# ============================================================
# BAYONET — 卡口流水表（C# BigDataController L305-446）
# ============================================================
_make_list_route("BAYONET", "/BigData/GetBAYONETList")
_make_detail_route("BAYONET", "/BigData/GetBAYONETDetail", "BAYONETId")
_make_synchro_route("BAYONET", "/BigData/SynchroBAYONET")
_make_delete_route("BAYONET", "/BigData/DeleteBAYONET", "BAYONETId")

# ============================================================
# BAYONETDAILY_AH — 卡口车辆进出日汇总表（C# BigDataController L448-589）
# ============================================================
_make_list_route("BAYONETDAILY_AH", "/BigData/GetBAYONETDAILY_AHList")
_make_detail_route("BAYONETDAILY_AH", "/BigData/GetBAYONETDAILY_AHDetail", "BAYONETDAILY_AHId")
_make_synchro_route("BAYONETDAILY_AH", "/BigData/SynchroBAYONETDAILY_AH")
_make_delete_route("BAYONETDAILY_AH", "/BigData/DeleteBAYONETDAILY_AH", "BAYONETDAILY_AHId")

# ============================================================
# BAYONETANALYSIS — AI智能车流分析（注意：C# 路由前缀是 Revenue）
# ============================================================
_make_list_route("BAYONETANALYSIS", "/Revenue/GetBAYONETANALYSISList")
_make_detail_route("BAYONETANALYSIS", "/Revenue/GetBAYONETANALYSISDetail", "BAYONETANALYSISId")
_make_synchro_route("BAYONETANALYSIS", "/Revenue/SynchroBAYONETANALYSIS")
_make_delete_route("BAYONETANALYSIS", "/Revenue/DeleteBAYONETANALYSIS", "BAYONETANALYSISId")

# ============================================================
# BAYONETOAANALYSIS — 业主方智能车流分析（C# 路由前缀 Revenue）
# ============================================================
_make_list_route("BAYONETOAANALYSIS", "/Revenue/GetBAYONETOAANALYSISList")
_make_detail_route("BAYONETOAANALYSIS", "/Revenue/GetBAYONETOAANALYSISDetail", "BAYONETOAANALYSISId")
_make_synchro_route("BAYONETOAANALYSIS", "/Revenue/SynchroBAYONETOAANALYSIS")
_make_delete_route("BAYONETOAANALYSIS", "/Revenue/DeleteBAYONETOAANALYSIS", "BAYONETOAANALYSISId")

# ============================================================
# BAYONETWARNING — 卡口预警 (BG-03: 4条CRUD补齐)
# ============================================================
_make_list_route("BAYONETWARNING", "/BigData/GetBAYONETWARNINGList")
_make_detail_route("BAYONETWARNING", "/BigData/GetBAYONETWARNINGDetail", "BAYONETWARNINGId")
_make_synchro_route("BAYONETWARNING", "/BigData/SynchroBAYONETWARNING")
_make_delete_route("BAYONETWARNING", "/BigData/DeleteBAYONETWARNING", "BAYONETWARNINGId")

# ============================================================
# CUSTOMERGROUP_AMOUNT — 客群流量（C# CustomerController）
# ============================================================
_make_list_route("CUSTOMERGROUP_AMOUNT", "/Customer/GetCUSTOMERGROUP_AMOUNTList")
_make_detail_route("CUSTOMERGROUP_AMOUNT", "/Customer/GetCUSTOMERGROUP_AMOUNTDetail", "CUSTOMERGROUP_AMOUNTId")
_make_synchro_route("CUSTOMERGROUP_AMOUNT", "/Customer/SynchroCUSTOMERGROUP_AMOUNT")
_make_delete_route("CUSTOMERGROUP_AMOUNT", "/Customer/DeleteCUSTOMERGROUP_AMOUNT", "CUSTOMERGROUP_AMOUNTId")


# ============================================================
# 散装接口 — 响应格式已统一为 Result（BG-01 整改）
# ============================================================

@router.get("/BigData/A2305052305180725")
def bayonet_daily_summary(
        SERVERPART_ID: str = "", SERVERPART_REGION: str = "",
        INOUT_TYPE: str = "", VEHICLE_TYPE: str = "",
        STATISTICS_DATE_Start: str = "", STATISTICS_DATE_End: str = "",
        PageIndex: Optional[int] = None, PageSize: Optional[int] = None,
        SortStr: str = "",
        db: DatabaseHelper = Depends(get_db)):
    """卡口车辆进出日汇总表汇总 — C# A2305052305180725Helper.A2305052305180725"""
    result, total = bigdata_service.get_bayonet_daily_summary(db,
        SERVERPART_ID=SERVERPART_ID, SERVERPART_REGION=SERVERPART_REGION,
        INOUT_TYPE=INOUT_TYPE, VEHICLE_TYPE=VEHICLE_TYPE,
        StartDate=STATISTICS_DATE_Start, EndDate=STATISTICS_DATE_End,
        PageIndex=PageIndex, PageSize=PageSize, SortStr=SortStr)
    return Result.success(JsonListData.create(result, total))

@router.get("/BigData/GetDailyBayonetAnalysis")
def daily_bayonet_analysis(
        SERVERPART_ID: str = "", SERVERPART_REGION: str = "",
        INOUT_TYPE: str = "", VEHICLE_TYPE: str = "",
        STATISTICS_DATE_Start: str = "", STATISTICS_DATE_End: str = "",
        ServerpartShopIds: str = "",
        PageIndex: Optional[int] = None, PageSize: Optional[int] = None,
        SortStr: str = "",
        db: DatabaseHelper = Depends(get_db)):
    """日度服务区车流分析 — C# SECTIONFLOWHelper.GetDailyBayonetAnalysis"""
    result = bigdata_service.get_daily_bayonet_analysis(db,
        SERVERPART_ID=SERVERPART_ID, SERVERPART_REGION=SERVERPART_REGION,
        INOUT_TYPE=INOUT_TYPE, VEHICLE_TYPE=VEHICLE_TYPE,
        StartDate=STATISTICS_DATE_Start, EndDate=STATISTICS_DATE_End,
        ServerpartShopIds=ServerpartShopIds,
        PageIndex=PageIndex, PageSize=PageSize, SortStr=SortStr)
    return Result.success(result)

@router.get("/BigData/GetServerpartSectionFlow")
def serverpart_section_flow(
        SERVERPART_ID: str = "", SERVERPART_REGION: str = "",
        INOUT_TYPE: str = "", VEHICLE_TYPE: str = "",
        STATISTICS_DATE_Start: str = "", STATISTICS_DATE_End: str = "",
        ServerpartShopIds: str = "",
        PageIndex: Optional[int] = None, PageSize: Optional[int] = None,
        SortStr: str = "",
        db: DatabaseHelper = Depends(get_db)):
    """月度服务区车流分析 — C# SECTIONFLOWHelper.GetServerpartSectionFlow"""
    result, total = bigdata_service.get_serverpart_section_flow(db,
        SERVERPART_ID=SERVERPART_ID, SERVERPART_REGION=SERVERPART_REGION,
        INOUT_TYPE=INOUT_TYPE, VEHICLE_TYPE=VEHICLE_TYPE,
        StartDate=STATISTICS_DATE_Start, EndDate=STATISTICS_DATE_End,
        ServerpartShopIds=ServerpartShopIds,
        PageIndex=PageIndex, PageSize=PageSize, SortStr=SortStr)
    return Result.success(JsonListData.create(result, total))

@router.get("/Revenue/GetBayonetVehicleAnalysis")
def bayonet_vehicle_analysis(ServerpartId: str = "", RankNum: int = 5,
                             db: DatabaseHelper = Depends(get_db)):
    """分析服务区的车流情况 — C# BigDataHelper.GetBayonetVehicleAnalysis（默认5）"""
    result = bigdata_service.get_bayonet_vehicle_analysis(db, ServerpartId, RankNum)
    return Result.success(result)

@router.get("/BigData/GetTimeIntervalList")
def time_interval_list(
        statisticsType: str = "0", serverPartId: str = "",
        statisticsMonth: str = "", vehicleType: str = "",
        DataType: str = "",
        pageIndex: Optional[int] = 1, pageSize: Optional[int] = 10,
        db: DatabaseHelper = Depends(get_db)):
    """获取时段卡口车流统计列表 — C# BAYONETHelper.GetTimeIntervalModelList"""
    result = bigdata_service.get_time_interval_list(db,
        StatisticsType=statisticsType, ServerPartIds=serverPartId,
        StatisticsMonth=statisticsMonth, VehicleType=vehicleType,
        DataType=DataType)
    total = len(result)
    return Result.success(JsonListData.create(result, total))

@router.get("/BigData/GetBayonetOwnerAHList")
def bayonet_owner_ah_list(
        serverPartId: Optional[int] = None, vehicleType: str = "",
        statisticsStartTime: str = "", statisticsEndTime: str = "",
        searchKey: str = "", searchValue: str = "",
        sortKey: str = "", sortStr: str = "",
        pageIndex: Optional[int] = 1, pageSize: Optional[int] = 10,
        db: DatabaseHelper = Depends(get_db)):
    """获取车辆归属地统计列表 — C# BAYONETOWNER_AHHelper.GetBayonetOwnerAHList"""
    result = bigdata_service.get_bayonet_owner_ah_list(db,
        serverPartId=serverPartId, vehicleType=vehicleType,
        statisticsStartTime=statisticsStartTime, statisticsEndTime=statisticsEndTime,
        searchKey=searchKey, searchValue=searchValue,
        sortKey=sortKey, sortStr=sortStr)
    total = len(result)
    return Result.success(JsonListData.create(result, total))

@router.get("/BigData/GetBayonetOwnerMonthAHList")
def bayonet_owner_month_ah_list(
        serverPartId: Optional[int] = None, vehicleType: str = "",
        searchKey: str = "", searchValue: str = "",
        sortKey: str = "", sortStr: str = "",
        statisticsStartMonth: str = "", statisticsEndMonth: str = "",
        pageIndex: Optional[int] = 1, pageSize: Optional[int] = 10,
        db: DatabaseHelper = Depends(get_db)):
    """获取月度车辆停留统计列表 — C# BAYONETOWNERMONTH_AHHelper.GetBayonetOwnerMonthAHList"""
    result = bigdata_service.get_bayonet_owner_month_ah_list(db,
        serverPartId=serverPartId, vehicleType=vehicleType,
        searchKey=searchKey, searchValue=searchValue,
        sortKey=sortKey, sortStr=sortStr,
        statisticsStartMonth=statisticsStartMonth, statisticsEndMonth=statisticsEndMonth)
    total = len(result)
    return Result.success(JsonListData.create(result, total))

@router.post("/BigData/GetUreaMasterList")
def urea_master_list(OperateDate: str = "", ProvinceCode: int = 0,
                     ServerpartID: str = "", DeviceName: str = "",
                     db: DatabaseHelper = Depends(get_db)):
    """查询尿素交易明细 — C# UREAMASTERHelper.GetUreaMasterList"""
    result = bigdata_service.get_urea_master_list(db,
        operate_date=OperateDate, province_code=ProvinceCode,
        serverpart_id=ServerpartID, device_name=DeviceName)
    total = len(result)
    return Result.success(JsonListData.create(result, total))

