# -*- coding: utf-8 -*-
"""
CommercialApi - BaseInfo 路由（重构版）
对应原 CommercialApi/Controllers/BaseInfoController.cs
业务逻辑已移至 services/commercial/base_info_service.py
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db
from services.commercial import base_info_service

router = APIRouter()


@router.get("/BaseInfo/GetSPRegionList")
async def get_sp_region_list(Province_Code: Optional[str] = Query(None), db: DatabaseHelper = Depends(get_db)):
    """获取片区列表"""
    try:
        region_list = base_info_service.get_sp_region_list(db, Province_Code)
        json_list = JsonListData.create(data_list=region_list, total=len(region_list), page_index=1, page_size=len(region_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPRegionList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetBusinessTradeList")
async def get_business_trade_list_get(
    pushProvinceCode: Optional[str] = Query(None), BusinessTradeId: Optional[int] = Query(None),
    BusinessTradeName: Optional[str] = Query(""), BusinessTradePId: Optional[int] = Query(None),
    BusinessTradePName: Optional[str] = Query(""), db: DatabaseHelper = Depends(get_db)
):
    """获取经营业态列表（GET）"""
    try:
        trade_list = base_info_service.get_business_trade_list_get(
            db, pushProvinceCode, BusinessTradeId, BusinessTradeName, BusinessTradePId, BusinessTradePName)
        json_list = JsonListData.create(data_list=trade_list, total=len(trade_list), page_index=1, page_size=len(trade_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeList(GET) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/GetBusinessTradeList")
async def get_business_trade_list_post(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取经营业态列表（POST）"""
    try:
        sm = searchModel or {}
        total, trade_list = base_info_service.get_business_trade_list_post(db, sm)
        json_list = JsonListData.create(data_list=trade_list, total=total,
            page_index=int(sm.get("PageIndex", 0) or 0), page_size=int(sm.get("PageSize", 0) or 0))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeList(POST) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetBrandAnalysis")
async def get_brand_analysis(
    ProvinceCode: Optional[str] = Query(None), Serverpart_ID: Optional[str] = Query(None),
    Statistics_Date: Optional[str] = Query(""), BusinessTradeIds: Optional[str] = Query(""),
    BrandType: Optional[str] = Query(""), ShowAllShop: bool = Query(True),
    db: DatabaseHelper = Depends(get_db)
):
    """服务区经营品牌分析"""
    try:
        data = base_info_service.get_brand_analysis(db, ProvinceCode, Serverpart_ID, BusinessTradeIds, BrandType, ShowAllShop)
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBrandAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetServerpartList")
async def get_serverpart_list(
    Province_Code: Optional[str] = Query(None), SPRegionType_ID: Optional[str] = Query(""),
    Serverpart_Name: Optional[str] = Query(""), ServerpartType: Optional[str] = Query(""),
    Serverpart_ID: Optional[int] = Query(None),
    longitude: Optional[str] = Query(""), latitude: Optional[str] = Query(""),
    BusinessTrade: Optional[str] = Query(""), BusinessBrand: Optional[str] = Query(""),
    MerchantName: Optional[str] = Query(""), ShopName: Optional[str] = Query(""),
    ProjectName: Optional[str] = Query(""), BusinessType: Optional[str] = Query(""),
    WarningType: Optional[str] = Query(""), ShowWeather: bool = Query(False),
    ShowService: bool = Query(False), HasScanOrder: Optional[bool] = Query(None),
    HasDriverHome: Optional[bool] = Query(None), excludeProperty: bool = Query(True),
    PageIndex: Optional[int] = Query(None), PageSize: Optional[int] = Query(None),
    SearchKeyName: Optional[str] = Query(""), SearchKeyValue: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区列表"""
    try:
        rows, total = base_info_service.get_serverpart_list(
            db, Province_Code, SPRegionType_ID, Serverpart_Name, ServerpartType, Serverpart_ID, PageIndex, PageSize)
        json_list = JsonListData.create(data_list=rows, total=total, page_index=PageIndex or 1, page_size=PageSize or total)
        resp = json_list.model_dump()
        resp["OtherData"] = []
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetServerpartInfo")
async def get_serverpart_info(
    ServerpartId: Optional[int] = Query(None), longitude: Optional[str] = Query(""),
    latitude: Optional[str] = Query(""), excludeProperty: bool = Query(True),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区基本信息"""
    try:
        if not ServerpartId:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        result = base_info_service.get_serverpart_info(db, ServerpartId)
        if result is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=result, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartInfo 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetServerInfoTree")
async def get_server_info_tree(
    request: Request, ProvinceCode: Optional[int] = Query(None),
    SPRegionTypeId: Optional[str] = Query(""), ServerpartIds: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """绑定区域服务区基本信息树"""
    try:
        if ProvinceCode is None:
            header_pc = request.headers.get("ProvinceCode", "")
            if header_pc:
                try: ProvinceCode = int(header_pc)
                except ValueError: pass
        if ProvinceCode is None:
            return Result.fail(code=200, msg="查询失败，请传入正确的省份编码！")

        serverpart_codes = request.headers.get("ServerpartCodes", "")
        result_list = base_info_service.get_server_info_tree(db, ProvinceCode, SPRegionTypeId, ServerpartIds or "", serverpart_codes)
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_index=1, page_size=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerInfoTree 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/GetServerpartServiceSummary")
async def get_serverpart_service_summary(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取服务区基础设施汇总数据"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        data = base_info_service.get_serverpart_service_summary(
            db, params.get("ProvinceCode", ""), params.get("SPRegionType_ID", ""), params.get("ServerpartId", ""))
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except ValueError as ve:
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        logger.error(f"GetServerpartServiceSummary 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/GetBrandStructureAnalysis")
async def get_brand_structure_analysis(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取经营品牌结构分析"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        result_list = base_info_service.get_brand_structure_analysis(
            db, params.get("ProvinceCode", ""), params.get("BusinessTrade", ""))
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_index=1, page_size=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        logger.error(f"GetBrandStructureAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
