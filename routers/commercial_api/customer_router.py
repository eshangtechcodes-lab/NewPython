# -*- coding: utf-8 -*-
"""
CommercialApi - Customer 路由（重构版）
对应原 CommercialApi/Controllers/CustomerController.cs
客群分析相关接口（8个接口）
业务逻辑已移至 services/commercial/customer_service.py
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db
from services.commercial import customer_service

router = APIRouter()


@router.get("/Customer/GetCustomerRatio")
async def get_customer_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份，格式如202110"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群分析占比（男/女/年龄层次占比）"""
    try:
        results = customer_service.get_customer_ratio(db, serverpartId, statisticsMonth)
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerConsumeRatio")
async def get_customer_consume_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群消费能力占比"""
    try:
        results = customer_service.get_customer_consume_ratio(db, serverpartId, statisticsMonth)
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerConsumeRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerAgeRatio")
async def get_customer_age_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群年龄层次占比"""
    try:
        results = customer_service.get_customer_age_ratio(db, serverpartId, statisticsMonth)
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerAgeRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerGroupRatio")
async def get_customer_group_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群特征分析（散点图数据）"""
    try:
        results = customer_service.get_customer_group_ratio(db, serverpartId, statisticsMonth)
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerGroupRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetAnalysisDescList")
async def get_analysis_desc_list(
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsType: Optional[int] = Query(None, description="统计类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群分析说明表列表"""
    try:
        results = customer_service.get_analysis_desc_list(
            db, serverpartId, serverpartCode, statisticsMonth, statisticsType)
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAnalysisDescList 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetAnalysisDescDetail")
async def get_analysis_desc_detail(
    statisticsType: Optional[int] = Query(None, description="统计类型"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    provinceCode: Optional[str] = Query("", description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群分析说明表明细"""
    try:
        detail = customer_service.get_analysis_desc_detail(
            db, serverpartId, serverpartCode, provinceCode, statisticsMonth, statisticsType)
        if detail is None:
            return Result.success(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAnalysisDescDetail 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerSaleRatio")
async def get_customer_sale_ratio(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    BusinessTradeId: Optional[str] = Query("", description="经营业态内码"),
    ShowDetail: int = Query(0, description="0不显示明细，否则显示"),
    sortStr: Optional[str] = Query("", description="排序字段"),
    fromRedis: bool = Query(False, description="从缓存取值"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群消费偏好数据"""
    try:
        # TODO: 实现查询逻辑后移至 customer_service
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")
        logger.warning("GetCustomerSaleRatio 暂未完整实现")
        _csl = {
            "SPRegionTypeId": None, "SPRegionTypeName": None,
            "ServerpartId": None, "ServerpartName": None,
            "BusinessTradeName": None, "BusinessTradeValue": None,
            "StatisticsMonth": None, "TotalRatio": None,
            "MaleRatio": None, "FemaleRatio": None,
            "MaleRatio_70": None, "MaleRatio_80": None, "MaleRatio_90": None, "MaleRatio_00": None,
            "FemaleRatio_70": None, "FemaleRatio_80": None, "FemaleRatio_90": None, "FemaleRatio_00": None,
            "Ratio_70": None, "Ratio_80": None, "Ratio_90": None, "Ratio_00": None,
            "CustomerSaleDetailList": None,
        }
        return Result.success(data={
            "CustomerSaleList": [_csl],
            "MaxAgeRatio": None, "MaxSexAgeRatio": None, "MaxSexRatio": None,
        }, msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")
