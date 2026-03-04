# -*- coding: utf-8 -*-
"""
CommercialApi - Contract 路由
对应原 CommercialApi/Controllers/ContractController.cs
经营合同分析相关接口
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result
from routers.deps import get_db

router = APIRouter()


# ===== 1. GetContractAnalysis =====
@router.get("/Contract/GetContractAnalysis")
async def get_contract_analysis(
    statisticsDate: str = Query(..., description="统计日期，格式：yyyy-MM-dd"),
    provinceCode: str = Query(..., description="省份编码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营合同分析
    原路由: [Route("Contract/GetContractAnalysis")] GET
    原注释: 显示在驿达数智化小程序-经营画像：营收分析板块，显示当月经营合同相关数据
    原 Helper: ContractAnalysisHelper.GetContractAnalysis
    依赖表: CONTRACT_STORAGE.T_REGISTERCOMPACT, T_REGISTERCOMPACTSUB, T_PAYMENTCONFIRM,
            HIGHWAY_STORAGE.T_SERVERPART
    返回: ContractAnalysisModel（ContractProfitLoss/ShopCount/SalesPerSquareMeter/
          ExpiredShopCount/ContractList/ContractCompletionDegree/ConvertRate）
    """
    try:
        # TODO: 实现完整的合同分析逻辑（涉及3张跨schema表关联+聚合计算）
        # 原始返回模型字段：
        result_data = {
            "ContractProfitLoss": 0,        # 合同总金额
            "ShopCount": 0,                  # 在营门店数量
            "SalesPerSquareMeter": 0,        # 欠款总金额（万元）
            "ExpiredShopCount": 0,           # 半年内到期合同数量
            "ContractList": [],              # 到期合同列表 [{name, value}]
            "ContractCompletionDegree": 67.1,  # 合同完成度（原代码写死67.1）
            "ConvertRate": 50.5,             # 转化率（原代码写死50.5）
        }
        logger.warning(f"GetContractAnalysis 复杂查询暂未完整实现（需同步 CONTRACT_STORAGE 表）")
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetContractAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 2. GetMerchantAccountSplit =====
@router.get("/Contract/GetMerchantAccountSplit")
async def get_merchant_account_split(
    StatisticsMonth: str = Query(..., description="统计结束月份，格式：yyyy-MM"),
    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),
    calcType: int = Query(1, description="计算方式：1=当月，2=累计"),
    CompactTypes: str = Query("340001", description="合同类型"),
    BusinessTypes: Optional[str] = Query("", description="经营模式"),
    SettlementMods: Optional[str] = Query("", description="结算模式"),
    MerchantIds: Optional[str] = Query("", description="经营商户"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营商户应收拆分数据
    原路由: [Route("Contract/GetMerchantAccountSplit")] GET
    原 Helper: AccountHelper.GetMerchantAccountSplit
    依赖表: CONTRACT_STORAGE 相关表
    返回: MerchantAccountSummaryModel
    """
    try:
        # TODO: 实现 AccountHelper.GetMerchantAccountSplit 逻辑
        logger.warning(f"GetMerchantAccountSplit 暂未完整实现（需同步 CONTRACT_STORAGE 表）")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        logger.error(f"GetMerchantAccountSplit 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 3. GetMerchantAccountDetail =====
@router.get("/Contract/GetMerchantAccountDetail")
async def get_merchant_account_detail(
    MerchantId: int = Query(..., description="经营商户内码"),
    StatisticsMonth: str = Query(..., description="统计结束月份，格式：yyyy-MM"),
    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),
    calcType: int = Query(1, description="计算方式：1=当月，2=累计"),
    CompactTypes: str = Query("340001", description="合同类型"),
    BusinessTypes: Optional[str] = Query("", description="经营模式"),
    SettlementMods: Optional[str] = Query("", description="结算模式"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营商户应收拆分明细数据
    原路由: [Route("Contract/GetMerchantAccountDetail")] GET
    原 Helper: AccountHelper.GetMerchantAccountDetail
    依赖表: CONTRACT_STORAGE 相关表
    返回: MerchantAccountModel
    """
    try:
        # TODO: 实现 AccountHelper.GetMerchantAccountDetail 逻辑
        logger.warning(f"GetMerchantAccountDetail 暂未完整实现（需同步 CONTRACT_STORAGE 表）")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        logger.error(f"GetMerchantAccountDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
