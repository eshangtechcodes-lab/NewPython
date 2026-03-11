from __future__ import annotations
# -*- coding: utf-8 -*-
"""
第五批 b：BusinessProjectController 散装接口路由（18 个复杂接口）
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.business_project import bp_scattered_complex_service as bpc_svc
from routers.deps import get_db

router = APIRouter()


# 1. GetMerchantsReceivablesList
@router.get("/BusinessProject/GetMerchantsReceivablesList")
async def get_merchants_receivables_list(
    ProvinceCode: str = Query(""), MerchantsId: str = Query(""),
    MerchantsName: str = Query(""), ShowJustPayable: int = Query(0),
    PageIndex: int = Query(1), PageSize: int = Query(10),
    SortStr: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, total = bpc_svc.get_merchants_receivables_list(
            db, ProvinceCode, MerchantsId, MerchantsName, ShowJustPayable, PageIndex, PageSize, SortStr)
        json_list = JsonListData.create(data_list=data_list, total=total, page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantsReceivablesList 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 2. GetMerchantsReceivables
@router.get("/BusinessProject/GetMerchantsReceivables")
async def get_merchants_receivables(
    MerchantsId: str = Query(""), ServerpartShopIds: str = Query(""),
    StartDate: str = Query(""), ShowRevenueSplit: bool = Query(True),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data = bpc_svc.get_merchants_receivables(db, MerchantsId, ServerpartShopIds, StartDate, ShowRevenueSplit)
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantsReceivables 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 3. GetBrandReceivables
@router.get("/BusinessProject/GetBrandReceivables")
async def get_brand_receivables(
    BusinessTradeId: str = Query(""),
    BusinessBrandId: str = Query(""),
    ServerpartId: str = Query(""),
    StartDate: str = Query(""),
    ShowProjectSplit: bool = Query(True),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, other_data = bpc_svc.get_brand_receivables(
            db, BusinessTradeId, BusinessBrandId, ServerpartId, StartDate, ShowProjectSplit)
        # C# 返回 JsonList<AccountReceivablesModel, List<AccountReceivablesModel>>
        # TotalCount = List count, PageSize = 10（C# 默认），PageIndex = 1
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=10)
        result_data = json_list.model_dump()
        result_data["OtherData"] = other_data
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBrandReceivables 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 4. GetMerchantsReceivablesReport
@router.get("/BusinessProject/GetMerchantsReceivablesReport")
async def get_merchants_receivables_report(
    ProvinceCode: str = Query(""), MerchantsId: str = Query(""),
    AccountDate: str = Query(""), PaymentDate: str = Query(""),
    SearchKeyName: str = Query(""), SearchKeyValue: str = Query(""),
    BusinessType: str = Query(""), SortStr: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list = bpc_svc.get_merchants_receivables_report(
            db, ProvinceCode, MerchantsId, AccountDate, PaymentDate,
            SearchKeyName, SearchKeyValue, BusinessType, SortStr)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=999)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMerchantsReceivablesReport 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 5. GetExpenseSummary
@router.get("/BusinessProject/GetExpenseSummary")
async def get_expense_summary(
    serverpart_ids: str = Query(...), shopShortName: str = Query(""),
    BusinessUnit: str = Query(""), statistics_month: str = Query(""),
    StartMonth: str = Query(""), EndMonth: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, other_data, total = bpc_svc.get_expense_summary(
            db, serverpart_ids, shopShortName, BusinessUnit, statistics_month, StartMonth, EndMonth)
        json_list = JsonListData.create(data_list=data_list, total=total, page_index=1, page_size=9999)
        result_data = json_list.model_dump()
        result_data["OtherData"] = other_data
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetExpenseSummary 失败: {ex}")
        return Result.fail(msg=f"获取失败{ex}")


# 6. GetShopExpenseSummary
@router.get("/BusinessProject/GetShopExpenseSummary")
async def get_shop_expense_summary(
    serverpartshop_id: str = Query(...),
    statistics_month_start: str = Query(""),
    statistics_month_end: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list = bpc_svc.get_shop_expense_summary(db, serverpartshop_id, statistics_month_start, statistics_month_end)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=9999)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopExpenseSummary 失败: {ex}")
        return Result.fail(msg=f"获取失败{ex}")


# 7. GetMonthSummaryList
@router.get("/BusinessProject/GetMonthSummaryList")
async def get_month_summary_list(
    StatisticsMonth: str = Query(...), ServerpartId: str = Query(""),
    BusinessType: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list = bpc_svc.get_month_summary_list(db, StatisticsMonth, ServerpartId, BusinessType)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=9999)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMonthSummaryList 失败: {ex}")
        return Result.fail(msg=f"获取失败{ex}")


# 8. GetAnnualSplit
@router.get("/BusinessProject/GetAnnualSplit")
async def get_annual_split(
    DataType: int = Query(...), BusinessProjectId: int = Query(...),
    ShopRoyaltyId: str = Query(""), BusinessDate: str = Query(""),
    StartDate: str = Query(""), EndDate: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, other_data = bpc_svc.get_annual_split(
            db, DataType, BusinessProjectId, ShopRoyaltyId, BusinessDate, StartDate, EndDate)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=9999)
        result_data = json_list.model_dump()
        result_data["OtherData"] = other_data
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAnnualSplit 失败: {ex}")
        return Result.fail(msg=f"获取失败{ex}")


# 9. GetProjectAccountList
@router.get("/BusinessProject/GetProjectAccountList")
async def get_project_account_list(
    ServerpartId: str = Query(""), ServerpartShopId: str = Query(""),
    StartDate: str = Query(""), EndDate: str = Query(""),
    SettlementMode: str = Query(""), SettlementType: int = Query(None),
    SettlementState: str = Query(""),
    PageIndex: int = Query(1), PageSize: int = Query(10),
    SortStr: str = Query(""), SearchKeyName: str = Query(""),
    SearchKeyValue: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, total = bpc_svc.get_project_account_list(
            db, ServerpartId, ServerpartShopId, StartDate, EndDate,
            SettlementMode, SettlementType, SettlementState,
            PageIndex, PageSize, SortStr, SearchKeyName, SearchKeyValue)
        json_list = JsonListData.create(data_list=data_list, total=total, page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetProjectAccountList 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 10. GetProjectAccountTree
@router.get("/BusinessProject/GetProjectAccountTree")
async def get_project_account_tree(
    ServerpartId: str = Query(""), SettlementMode: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list = bpc_svc.get_project_account_tree(db, ServerpartId, SettlementMode)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=9999)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetProjectAccountTree 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 11. GetProjectAccountDetail
@router.get("/BusinessProject/GetProjectAccountDetail")
async def get_project_account_detail(
    BusinessApprovalId: int = Query(0), BusinessProjectId: int = Query(0),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data = bpc_svc.get_project_account_detail(db, BusinessApprovalId, BusinessProjectId)
        if data:
            return Result.success(data=data, msg="查询成功")
        else:
            return {"Result_Code": 200, "Result_Desc": "查询失败，无数据返回！", "Result_Data": None}
    except Exception as ex:
        logger.error(f"GetProjectAccountDetail 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 12. GetAccountWarningList
@router.get("/BusinessProject/GetAccountWarningList")
async def get_account_warning_list(
    ServerpartId: str = Query(""), WarningType: str = Query(""),
    Business_Type: str = Query(""), SettlementMode: str = Query(""),
    BusinessState: str = Query(""), FormatType: str = Query(""),
    PageIndex: int = Query(1), PageSize: int = Query(10),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, total = bpc_svc.get_account_warning_list(
            db, ServerpartId, WarningType, Business_Type, SettlementMode,
            BusinessState, FormatType, PageIndex, PageSize)
        json_list = JsonListData.create(data_list=data_list, total=total, page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAccountWarningList 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 13. SolidAccountWarningList
@router.get("/BusinessProject/SolidAccountWarningList")
async def solid_account_warning_list(
    ServerpartId: str = Query(""), WarningType: str = Query(""),
    Business_Type: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    try:
        params = {"ServerpartId": ServerpartId, "WarningType": WarningType, "Business_Type": Business_Type}
        success = bpc_svc.solid_account_warning_list(db, params)
        if success:
            return Result.success(msg="生成成功")
        else:
            return {"Result_Code": 200, "Result_Desc": "生成失败！", "Result_Data": None}
    except Exception as ex:
        logger.error(f"SolidAccountWarningList 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")


# 14. SolidProjectRevenue
@router.get("/BusinessProject/SolidProjectRevenue")
async def solid_project_revenue(
    StatisticsMonth: str = Query(...), ServerpartId: str = Query(""),
    ProjectId: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    try:
        success = bpc_svc.solid_project_revenue(db, StatisticsMonth, ServerpartId, ProjectId)
        if success:
            return Result.success(msg="生成成功")
        else:
            return {"Result_Code": 200, "Result_Desc": "生成失败！", "Result_Data": None}
    except Exception as ex:
        logger.error(f"SolidProjectRevenue 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")


# 15. SolidPeriodAnalysis
@router.post("/BusinessProject/SolidPeriodAnalysis")
async def solid_period_analysis(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        success = bpc_svc.solid_period_analysis(db, data)
        if success:
            return Result.success(msg="生成成功")
        else:
            return {"Result_Code": 200, "Result_Desc": "生成失败！", "Result_Data": None}
    except Exception as ex:
        logger.error(f"SolidPeriodAnalysis 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")


# 16. GetPeriodWarningList
@router.get("/BusinessProject/GetPeriodWarningList")
async def get_period_warning_list(
    ServerpartId: str = Query(""), BusinessType: str = Query(""),
    WarningState: str = Query(""), StartDate: str = Query(""),
    EndDate: str = Query(""), SearchKeyName: str = Query(""),
    SearchKeyValue: str = Query(""),
    PageIndex: int = Query(1), PageSize: int = Query(10),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list, total, other_data = bpc_svc.get_period_warning_list(
            db, ServerpartId, BusinessType, WarningState, StartDate, EndDate,
            SearchKeyName, SearchKeyValue, PageIndex, PageSize)
        json_list = JsonListData.create(data_list=data_list, total=total, page_index=PageIndex, page_size=PageSize)
        result_data = json_list.model_dump()
        result_data["OtherData"] = other_data
        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPeriodWarningList 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# 17. ReconfigureProfit
@router.get("/BusinessProject/ReconfigureProfit")
async def reconfigure_profit(
    ServerpartId: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    try:
        params = {"ServerpartId": ServerpartId}
        success = bpc_svc.reconfigure_profit(db, params)
        if success:
            return Result.success(msg="生成成功")
        else:
            return {"Result_Code": 200, "Result_Desc": "生成失败！", "Result_Data": None}
    except Exception as ex:
        logger.error(f"ReconfigureProfit 失败: {ex}")
        return Result.fail(msg=f"生成失败{ex}")


# 18. GetWillSettleProject
@router.get("/BusinessProject/GetWillSettleProject")
async def get_will_settle_project(
    StartDate: str = Query(...), EndDate: str = Query(...),
    ServerpartId: str = Query(""), SettlementType: int = Query(None),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        data_list = bpc_svc.get_will_settle_project(db, StartDate, EndDate, ServerpartId, SettlementType)
        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_index=1, page_size=9999)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetWillSettleProject 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
