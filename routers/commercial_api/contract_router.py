# -*- coding: utf-8 -*-
"""
CommercialApi - Contract 路由（重构版）
对应原 CommercialApi/Controllers/ContractController.cs
业务逻辑已移至 services/commercial/contract_service.py
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result
from routers.deps import get_db
from services.commercial import contract_service

router = APIRouter()


@router.get("/Contract/GetContractAnalysis")
async def get_contract_analysis(
    statisticsDate: Optional[str] = Query(None, description="统计日期"),
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营合同分析"""
    try:
        result_data = contract_service.get_contract_analysis(
            db, statisticsDate, provinceCode, Serverpart_ID, SPRegionType_ID)
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetContractAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Contract/GetMerchantAccountSplit")
async def get_merchant_account_split(
    StatisticsMonth: Optional[str] = Query(None), StatisticsStartMonth: Optional[str] = Query(""),
    calcType: int = Query(1), CompactTypes: str = Query("340001"),
    BusinessTypes: Optional[str] = Query(""), SettlementMods: Optional[str] = Query(""),
    MerchantIds: Optional[str] = Query(""), SortStr: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营商户应收拆分数据"""
    try:
        data = contract_service.get_merchant_account_split(
            db, StatisticsMonth, StatisticsStartMonth, calcType,
            CompactTypes, BusinessTypes, SettlementMods, MerchantIds, SortStr)
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantAccountSplit 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Contract/GetMerchantAccountDetail")
async def get_merchant_account_detail(
    MerchantId: int = Query(...), StatisticsMonth: str = Query(...),
    StatisticsStartMonth: Optional[str] = Query(""), calcType: int = Query(1),
    CompactTypes: str = Query("340001"), BusinessTypes: Optional[str] = Query(""),
    SettlementMods: Optional[str] = Query(""), SortStr: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营商户应收拆分明细"""
    try:
        data = contract_service.get_merchant_account_detail(
            db, MerchantId, StatisticsMonth, StatisticsStartMonth,
            calcType, CompactTypes, BusinessTypes, SettlementMods, SortStr)
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantAccountDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
