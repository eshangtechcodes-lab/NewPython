from __future__ import annotations
# -*- coding: utf-8 -*-
"""
第五批 a：BusinessProjectController 散装接口路由（8 个简单接口）

接口清单：
1. GET  /BusinessProject/GetNoProjectShopList
2. GET  /BusinessProject/GetAccountWarningListSummary
3. GET  /BusinessProject/GetMerchantSplit
4. POST /BusinessProject/SolidPeriodWarningList
5. POST /BusinessProject/UploadRevenueConfirmList
6. POST /BusinessProject/SaveHisPaymentAccount
7. POST /BusinessProject/CreateRevenueAccount
8. GET  /BusinessProject/ApproveProinst
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.business_project import bp_scattered_service as bps_svc
from routers.deps import get_db

router = APIRouter()


# ==================== 1. GetNoProjectShopList ====================
@router.get("/BusinessProject/GetNoProjectShopList")
async def get_no_project_shop_list(
    ProvinceCode: str = Query("", description="省份编码"),
    SPRegionTypeID: str = Query("", description="片区内码"),
    ServerpartID: str = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取没有设置经营项目的移动支付分账门店"""
    try:
        data_list = bps_svc.get_no_project_shop_list(db, ProvinceCode, SPRegionTypeID, ServerpartID)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list),
                                         page_index=1, page_size=len(data_list) or 10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNoProjectShopList 失败: {ex}")
        return Result.fail(msg=f"获取失败{ex}")


# ==================== 2. GetAccountWarningListSummary ====================
@router.get("/BusinessProject/GetAccountWarningListSummary")
async def get_account_warning_summary(
    Business_Type: str = Query("", description="经营模式"),
    SettlementMode: str = Query("", description="结算模式"),
    BusinessState: str = Query("", description="经营状态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店经营预警汇总"""
    try:
        data_list = bps_svc.get_account_warning_summary(db, Business_Type, SettlementMode, BusinessState)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list),
                                         page_index=1, page_size=len(data_list) or 10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAccountWarningListSummary 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ==================== 3. GetMerchantSplit ====================
@router.get("/BusinessProject/GetMerchantSplit")
async def get_merchant_split(
    MerchantId: str = Query(..., description="经营商户内码"),
    ServerpartId: str = Query("", description="服务区内码"),
    StartDate: str = Query("", description="结算开始日期"),
    EndDate: str = Query("", description="结算结束日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营商户项目拆分结果"""
    try:
        data_list = bps_svc.get_merchant_split(db, MerchantId, ServerpartId, StartDate, EndDate)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list),
                                         page_index=1, page_size=len(data_list) or 10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantSplit 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ==================== 4. SolidPeriodWarningList ====================
@router.post("/BusinessProject/SolidPeriodWarningList")
async def solid_period_warning_list(
    periodwarningList: List[dict],
    db: DatabaseHelper = Depends(get_db)
):
    """批量同步经营项目周期预警"""
    try:
        success = bps_svc.solid_period_warning_list(db, periodwarningList)
        if success:
            return Result.success(msg="生成成功")
        else:
            return Result(Result_Code=200, Result_Desc="生成失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SolidPeriodWarningList 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")


# ==================== 5. UploadRevenueConfirmList ====================
@router.post("/BusinessProject/UploadRevenueConfirmList")
async def upload_revenueconfirm_list(
    revenueconfirmList: List[dict],
    db: DatabaseHelper = Depends(get_db)
):
    """批量上传退场结算应收拆分数据"""
    try:
        success, result_data = bps_svc.upload_revenueconfirm_list(db, revenueconfirmList)
        if success:
            return Result.success(data=result_data, msg="同步完成")
        else:
            return Result(Result_Code=200, Result_Desc="同步失败！")
    except Exception as ex:
        logger.error(f"UploadRevenueConfirmList 失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


# ==================== 6. SaveHisPaymentAccount ====================
@router.post("/BusinessProject/SaveHisPaymentAccount")
async def save_his_payment_account(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """存储商家缴款历史数据"""
    try:
        success = bps_svc.save_his_payment_account(db, data)
        if success:
            return Result.success(data=data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SaveHisPaymentAccount 失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


# ==================== 7. CreateRevenueAccount ====================
@router.post("/BusinessProject/CreateRevenueAccount")
async def create_revenue_account(
    ShopRoyaltyId: int = Query(..., description="应收拆分内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """根据门店提成比例生成应收账款信息"""
    try:
        success = bps_svc.create_revenue_account(db, ShopRoyaltyId)
        if success:
            return Result.success(msg="生成成功")
        else:
            return Result(Result_Code=200, Result_Desc="生成失败，日结数据未完成校验！")
    except Exception as ex:
        logger.error(f"CreateRevenueAccount 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")


# ==================== 8. ApproveProinst ====================
@router.get("/BusinessProject/ApproveProinst")
async def approve_proinst(
    BusinessId: int = Query(..., description="预警记录内码"),
    StaffId: int = Query(..., description="操作人内码"),
    StaffName: str = Query(..., description="操作人名称"),
    SwitchRate: int = Query(..., description="切换比例"),
    ApproveState: int = Query(..., description="审批状态"),
    SourcePlatform: str = Query("minProgram", description="操作平台"),
    db: DatabaseHelper = Depends(get_db)
):
    """审批移动支付分账比例切换流程"""
    try:
        success, msg = bps_svc.approve_proinst(db, BusinessId, StaffId, StaffName,
                                                SwitchRate, ApproveState, SourcePlatform)
        if success:
            return Result.success(msg="审批成功")
        else:
            return Result(Result_Code=200, Result_Desc=f"审批失败！{msg}")
    except Exception as ex:
        logger.error(f"ApproveProinst 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")
