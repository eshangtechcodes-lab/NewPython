from __future__ import annotations
# -*- coding: utf-8 -*-
"""
FinanceController 散装接口路由（44 个接口）
对应原 C# FinanceController 中除 ATTACHMENT CRUD 以外的所有接口
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.finance import finance_scattered_service as fin_svc
from routers.deps import get_db

router = APIRouter()


# ==================== 1. GetProjectSplitSummary ====================
@router.get("/Finance/GetProjectSplitSummary")
async def get_project_split_summary(
    StartDate: str = Query(""), EndDate: str = Query(""),
    SPRegionTypeId: str = Query(""), ServerpartId: str = Query(""),
    MerchantId: str = Query(""), db: DatabaseHelper = Depends(get_db)
):
    """获取月度营收分润数据"""
    try:
        data = fin_svc.get_project_split_summary(db, StartDate, EndDate, SPRegionTypeId, ServerpartId, MerchantId)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetProjectSplitSummary 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 2. GetProjectSummary ====================
@router.get("/Finance/GetProjectSummary")
async def get_project_summary(
    StartDate: str = Query(""), EndDate: str = Query(""),
    SPRegionTypeId: str = Query(""), ServerpartId: str = Query(""),
    MerchantId: str = Query(""), BusinessType: str = Query(""),
    SettlementModes: str = Query(""), CompactType: str = Query(""),
    ShowOwnerDif: bool = Query(False), ShowSubDif: bool = Query(False),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区营收分润数据"""
    try:
        data, other_data = fin_svc.get_project_summary(
            db, StartDate, EndDate, SPRegionTypeId, ServerpartId, MerchantId,
            BusinessType, SettlementModes, CompactType, ShowOwnerDif, ShowSubDif)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=other_data))
    except Exception as e:
        logger.error(f"GetProjectSummary 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 3. GetRevenueSplitSummary ====================
@router.get("/Finance/GetRevenueSplitSummary")
async def get_revenue_split_summary(
    StartDate: str = Query(""), EndDate: str = Query(""),
    SPRegionTypeId: str = Query(""), ServerpartId: str = Query(""),
    MerchantId: str = Query(""), BusinessType: str = Query(""),
    SettlementModes: str = Query(""), CompactType: str = Query(""),
    ServerpartShopId: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区营收分润报表"""
    try:
        data, other_data = fin_svc.get_revenue_split_summary(
            db, StartDate, EndDate, SPRegionTypeId, ServerpartId, MerchantId,
            BusinessType, SettlementModes, CompactType, ServerpartShopId)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=other_data))
    except Exception as e:
        logger.error(f"GetRevenueSplitSummary 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 4. GetProjectMerchantSummary ====================
@router.get("/Finance/GetProjectMerchantSummary")
async def get_project_merchant_summary(
    StartDate: str = Query(""), EndDate: str = Query(""),
    SPRegionTypeId: str = Query(""), ServerpartId: str = Query(""),
    MerchantId: str = Query(""), BusinessType: str = Query(""),
    SettlementModes: str = Query(""), CompactType: str = Query(""),
    ShowOwnerDif: bool = Query(False), ShowSubDif: bool = Query(False),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营商户营收分润数据"""
    try:
        data, other_data = fin_svc.get_project_merchant_summary(
            db, StartDate, EndDate, SPRegionTypeId, ServerpartId, MerchantId,
            BusinessType, SettlementModes, CompactType, ShowOwnerDif, ShowSubDif)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=other_data))
    except Exception as e:
        logger.error(f"GetProjectMerchantSummary 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 5. CreateSingleProjectSplit ====================
@router.get("/Finance/CreateSingleProjectSplit")
async def create_single_project_split(
    StartDate: str = Query(""), EndDate: str = Query(""),
    ServerpartShopId: str = Query(""), CompactId: str = Query(""),
    ProjectId: str = Query(""), OutBusinessType: str = Query(""),
    BusinessStartDate: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """生成单个门店/合同/项目应收拆分数据"""
    try:
        ok = fin_svc.create_single_project_split(
            db, StartDate, EndDate, ServerpartShopId, CompactId, ProjectId,
            OutBusinessType, BusinessStartDate)
        if ok:
            return Result.success(msg="生成完成")
        return Result.fail("生成失败")
    except Exception as e:
        logger.error(f"CreateSingleProjectSplit 失败: {e}")
        return Result.fail(f"生成失败: {e}")


# ==================== 6. SolidMonthProjectSplit ====================
@router.get("/Finance/SolidMonthProjectSplit")
async def solid_month_project_split(
    StatisticsMonth: str = Query(""), ServerpartShopId: str = Query(""),
    CompactId: str = Query(""), ProjectId: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """重新生成月度应收拆分固化数据"""
    try:
        ok = fin_svc.solid_month_project_split(db, StatisticsMonth, ServerpartShopId, CompactId, ProjectId)
        if ok:
            return Result.success(msg="固化完成")
        return Result.fail("固化失败")
    except Exception as e:
        logger.error(f"SolidMonthProjectSplit 失败: {e}")
        return Result.fail(f"固化失败: {e}")


# ==================== 7. GetRoyaltyDateSumReport ====================
@router.get("/Finance/GetRoyaltyDateSumReport")
async def get_royalty_date_sum_report(
    StartDate: str = Query(""), EndDate: str = Query(""),
    ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
    CompareSplit: bool = Query(True), KeyWord: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取日度业主到账汇总数据"""
    try:
        data = fin_svc.get_royalty_date_sum_report(
            db, StartDate, EndDate, ServerpartIds, ServerpartShopIds, CompareSplit, KeyWord)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetRoyaltyDateSumReport 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 8. GetRoyaltyReport ====================
@router.get("/Finance/GetRoyaltyReport")
async def get_royalty_report(
    StartDate: str = Query(""), EndDate: str = Query(""),
    ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
    CompareSplit: bool = Query(True), KeyWord: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取日度业主到账汇总数据"""
    try:
        data = fin_svc.get_royalty_report(
            db, StartDate, EndDate, ServerpartIds, ServerpartShopIds, CompareSplit, KeyWord)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetRoyaltyReport 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 9. GetProjectShopIncome ====================
@router.get("/Finance/GetProjectShopIncome")
async def get_project_shop_income(
    StatisticsDate: str = Query(""), ContrastDate: str = Query(""),
    ServerpartIds: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """统计商铺收入明细表"""
    try:
        data = fin_svc.get_project_shop_income(db, StatisticsDate, ContrastDate, ServerpartIds)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetProjectShopIncome 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 10. GetContractMerchant ====================
@router.get("/Finance/GetContractMerchant")
async def get_contract_merchant(
    ServerpartIds: str = Query(""), Settlement_Modes: str = Query(""),
    startDate: str = Query(""), endDate: str = Query(""),
    keyword: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同商户信息"""
    try:
        data = fin_svc.get_contract_merchant(db, ServerpartIds, Settlement_Modes, startDate, endDate, keyword)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetContractMerchant 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 11. GetAccountReached ====================
@router.get("/Finance/GetAccountReached")
async def get_account_reached(
    ServerpartIds: str = Query(""), Settlement_Modes: str = Query(""),
    startDate: str = Query(""), endDate: str = Query(""),
    keyword: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取分账收银到账"""
    try:
        data = fin_svc.get_account_reached(db, ServerpartIds, Settlement_Modes, startDate, endDate, keyword)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetAccountReached 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 12. GetShopExpense ====================
@router.get("/Finance/GetShopExpense")
async def get_shop_expense(
    ServerpartIds: str = Query(""), Settlement_Modes: str = Query(""),
    startDate: str = Query(""), endDate: str = Query(""),
    keyword: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取分账收银扣费明细"""
    try:
        data = fin_svc.get_shop_expense(db, ServerpartIds, Settlement_Modes, startDate, endDate, keyword)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetShopExpense 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 13. GetReconciliation ====================
@router.get("/Finance/GetReconciliation")
async def get_reconciliation(
    BUSINESSPROJECT_ID: int = Query(0), ShopRoyaltyId: str = Query(""),
    StartMonth: str = Query(""), EndMonth: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合作商户月对账"""
    try:
        data, other_data = fin_svc.get_reconciliation(db, BUSINESSPROJECT_ID, ShopRoyaltyId, StartMonth, EndMonth)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=other_data))
    except Exception as e:
        logger.error(f"GetReconciliation 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 14. GetRevenueRecognition ====================
@router.get("/Finance/GetRevenueRecognition")
async def get_revenue_recognition(
    ServerpartIds: str = Query(""), StartDate: str = Query(""),
    EndDate: str = Query(""), Settlement_Modes: str = Query(""),
    BusinessProjectId: int = Query(None), ShopRoyaltyId: str = Query(""),
    KeyWord: str = Query(""), SolidType: bool = Query(False),
    ShowHisProject: bool = Query(False), ShowSelf: bool = Query(False),
    db: DatabaseHelper = Depends(get_db)
):
    """获取分账收银收入确认"""
    try:
        data, solid_date = fin_svc.get_revenue_recognition(
            db, ServerpartIds, StartDate, EndDate, Settlement_Modes,
            BusinessProjectId, ShopRoyaltyId, KeyWord, SolidType,
            ShowHisProject, ShowSelf)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=solid_date))
    except Exception as e:
        logger.error(f"GetRevenueRecognition 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 15. GetProjectPeriodIncome ====================
@router.get("/Finance/GetProjectPeriodIncome")
async def get_project_period_income(
    BusinessProjectId: int = Query(0), StatisticsMonth: str = Query(""),
    StatisticsMonthStart: str = Query(""), ShopRoyaltyId: str = Query(""),
    MobilePayCorrect: float = Query(None), CashPayCorrect: float = Query(None),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目分账收银收入"""
    try:
        data = fin_svc.get_project_period_income(
            db, BusinessProjectId, StatisticsMonth, StatisticsMonthStart,
            ShopRoyaltyId, MobilePayCorrect or 0, CashPayCorrect or 0)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetProjectPeriodIncome 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 16. GetProjectPeriodAccount ====================
@router.get("/Finance/GetProjectPeriodAccount")
async def get_project_period_account(
    BUSINESSPROJECT_ID: int = Query(0), SHOPROYALTY_ID: str = Query(""),
    BUSINESSAPPROVAL_ID: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """查询经营周期结算明细"""
    try:
        data = fin_svc.get_project_period_account(db, BUSINESSPROJECT_ID, SHOPROYALTY_ID, BUSINESSAPPROVAL_ID)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetProjectPeriodAccount 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 17. ApplyAccountProinst ====================
@router.post("/Finance/ApplyAccountProinst")
async def apply_account_proinst(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """发起商户年度结算审批"""
    try:
        ok, msg = fin_svc.apply_account_proinst(db, data)
        if ok:
            return Result.success(msg="发起审批成功！")
        return Result.fail(msg or "发起审批失败")
    except Exception as e:
        logger.error(f"ApplyAccountProinst 失败: {e}")
        return Result.fail(f"提交失败: {e}")


# ==================== 18. ApproveAccountProinst ====================
@router.api_route("/Finance/ApproveAccountProinst", methods=["GET", "POST"])
async def approve_account_proinst(
    businessApprovalID: int = Query(0), curProinstState: int = Query(0),
    approveedInfo: str = Query(""), approveedStaffId: int = Query(None),
    approveedStaffName: str = Query(""), nextId: int = Query(None),
    nextState: int = Query(None), SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """提交/审批商户对账"""
    try:
        ok, msg = fin_svc.approve_account_proinst(
            db, businessApprovalID, curProinstState, approveedInfo,
            approveedStaffId, approveedStaffName, nextId, nextState, SourcePlatform)
        approve_type = "提交" if curProinstState == 1000 else "审核"
        if ok:
            return Result.success(msg=f"{approve_type}成功！")
        return Result.fail(f"{approve_type}失败！{msg}")
    except Exception as e:
        logger.error(f"ApproveAccountProinst 失败: {e}")
        return Result.fail(f"提交失败: {e}")


# ==================== 19. RejectAccountProinst ====================
@router.api_route("/Finance/RejectAccountProinst", methods=["GET", "POST"])
async def reject_account_proinst(
    businessApprovalID: int = Query(0), approveedStaffId: int = Query(None),
    approveedStaffName: str = Query(""), approveedInfo: str = Query(""),
    targetProinstState: int = Query(None), rejectType: int = Query(1),
    endReject: bool = Query(False), SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """驳回商户对账审批业务"""
    try:
        ok, msg = fin_svc.reject_account_proinst(
            db, businessApprovalID, approveedStaffId, approveedStaffName,
            approveedInfo, targetProinstState, rejectType, endReject, SourcePlatform)
        if ok:
            return Result.success(msg="驳回成功")
        return Result.fail(f"驳回失败！{msg}")
    except Exception as e:
        logger.error(f"RejectAccountProinst 失败: {e}")
        return Result.fail(f"驳回失败: {e}")


# ==================== 20. GetMonthAccountProinst ====================
@router.post("/Finance/GetMonthAccountProinst")
async def get_month_account_proinst(
    data: dict = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目月度结算审批列表"""
    try:
        result_list, total, todo_count = fin_svc.get_month_account_proinst(db, data)
        return Result.success(JsonListData(List=result_list, TotalCount=total, OtherData=todo_count))
    except Exception as e:
        logger.error(f"GetMonthAccountProinst 失败: {e}")
        return Result.fail(f"查询失败: {e}")


# ==================== 21. ApplyMonthAccountProinst ====================
@router.post("/Finance/ApplyMonthAccountProinst")
async def apply_month_account_proinst(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """发起经营项目月度结算审批"""
    try:
        ok, msg = fin_svc.apply_month_account_proinst(db, data)
        if ok:
            return Result.success(msg="发起审批成功！")
        return Result.fail(f"发起审批失败，{msg}！")
    except Exception as e:
        logger.error(f"ApplyMonthAccountProinst 失败: {e}")
        return Result.fail(f"提交失败: {e}")


# ==================== 22. ApproveMonthAccountProinst ====================
@router.api_route("/Finance/ApproveMonthAccountProinst", methods=["GET", "POST"])
async def approve_month_account_proinst(
    businessApprovalID: int = Query(0), curProinstState: int = Query(0),
    approveedInfo: str = Query(""), approveedStaffId: int = Query(None),
    approveedStaffName: str = Query(""), nextId: int = Query(None),
    nextState: int = Query(None), SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """提交/审批经营项目月度结算流程"""
    try:
        ok, msg = fin_svc.approve_month_account_proinst(
            db, businessApprovalID, curProinstState, approveedInfo,
            approveedStaffId, approveedStaffName, nextId, nextState, SourcePlatform)
        approve_type = "提交" if curProinstState == 1000 else "审核"
        if ok:
            return Result.success(msg=f"{approve_type}成功！")
        return Result.fail(f"{approve_type}失败！{msg}")
    except Exception as e:
        logger.error(f"ApproveMonthAccountProinst 失败: {e}")
        return Result.fail(f"提交失败: {e}")


# ==================== 23. ApproveMAPList ====================
@router.api_route("/Finance/ApproveMAPList", methods=["GET", "POST"])
async def approve_map_list(
    businessApprovalID: str = Query(""), curProinstState: int = Query(0),
    approveedInfo: str = Query(""), approveedStaffId: int = Query(None),
    approveedStaffName: str = Query(""), nextId: int = Query(None),
    SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """批量审批经营项目月度结算流程"""
    try:
        ok, msg = fin_svc.approve_map_list(
            db, businessApprovalID, curProinstState, approveedInfo,
            approveedStaffId, approveedStaffName, nextId, SourcePlatform)
        if ok:
            return Result.success(msg="批量审批成功！")
        return Result.fail(f"审批失败！{msg}")
    except Exception as e:
        logger.error(f"ApproveMAPList 失败: {e}")
        return Result.fail(f"批量审批失败: {e}")


# ==================== 24. RejectMonthAccountProinst ====================
@router.api_route("/Finance/RejectMonthAccountProinst", methods=["GET", "POST"])
async def reject_month_account_proinst(
    businessApprovalID: int = Query(0), approveedStaffId: int = Query(None),
    approveedStaffName: str = Query(""), approveedInfo: str = Query(""),
    targetProinstState: int = Query(1000), rejectType: int = Query(1),
    endReject: bool = Query(False), SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """驳回经营项目月度结算流程"""
    try:
        ok, msg = fin_svc.reject_month_account_proinst(
            db, businessApprovalID, approveedStaffId, approveedStaffName,
            approveedInfo, targetProinstState, rejectType, endReject, SourcePlatform)
        if ok:
            return Result.success(msg="驳回成功")
        return Result.fail(f"驳回失败！{msg}")
    except Exception as e:
        logger.error(f"RejectMonthAccountProinst 失败: {e}")
        return Result.fail(f"驳回失败: {e}")


# ==================== 25. StorageMonthProjectAccount ====================
@router.post("/Finance/StorageMonthProjectAccount")
async def storage_month_project_account(
    data: list,
    db: DatabaseHelper = Depends(get_db)
):
    """固化月度分账收银收入数据"""
    try:
        if not data:
            return Result.fail("保存失败，请传入有效数据！")
        ok = fin_svc.storage_month_project_account(db, data)
        if ok:
            return Result.success(msg="保存成功")
        return Result.fail("保存失败，数据异常！")
    except Exception as e:
        logger.error(f"StorageMonthProjectAccount 失败: {e}")
        return Result.fail(f"保存失败: {e}")


# ==================== 26. GetMonthAccountDiff ====================
@router.get("/Finance/GetMonthAccountDiff")
async def get_month_account_diff(
    ServerpartId: str = Query(""), StatisticsMonth: str = Query(""),
    ShowDiff: bool = Query(False),
    db: DatabaseHelper = Depends(get_db)
):
    """对比分账收银收入累计营业额差异"""
    try:
        data, solid_date = fin_svc.get_month_account_diff(db, ServerpartId, StatisticsMonth, ShowDiff)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=solid_date))
    except Exception as e:
        logger.error(f"GetMonthAccountDiff 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 27. ApprovePeriodAccount ====================
@router.get("/Finance/ApprovePeriodAccount")
async def approve_period_account(
    ProjectId: int = Query(0), ShopRoyaltyId: str = Query(""),
    StartMonth: str = Query(""), EndMonth: str = Query(""),
    UserId: int = Query(None),
    db: DatabaseHelper = Depends(get_db)
):
    """生成经营项目月度结算审批数据"""
    try:
        ok = fin_svc.approve_period_account(db, ProjectId, ShopRoyaltyId, StartMonth, EndMonth, UserId)
        if ok:
            return Result.success(msg="生成成功")
        return Result.fail("生成失败，数据异常！")
    except Exception as e:
        logger.error(f"ApprovePeriodAccount 失败: {e}")
        return Result.fail(f"保存失败: {e}")


# ==================== 28. RejectPeriodAccount ====================
@router.get("/Finance/RejectPeriodAccount")
async def reject_period_account(
    ProjectId: int = Query(0), ShopRoyaltyId: str = Query(""),
    StartMonth: str = Query(""), EndMonth: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """批量驳回经营项目月度结算审批数据"""
    try:
        ok = fin_svc.reject_period_account(db, ProjectId, ShopRoyaltyId, StartMonth, EndMonth)
        if ok:
            return Result.success(msg="驳回成功")
        return Result.fail("驳回失败，数据异常！")
    except Exception as e:
        logger.error(f"RejectPeriodAccount 失败: {e}")
        return Result.fail(f"驳回失败: {e}")


# ==================== 29. GetPeriodSupplementList ====================
@router.get("/Finance/GetPeriodSupplementList")
async def get_period_supplement_list(
    BusinessProjectId: int = Query(0), ShopRoyaltyId: str = Query(""),
    ServerpartShopId: str = Query(""), StartDate: str = Query(""),
    EndDate: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目年度日结冲正记录"""
    try:
        data = fin_svc.get_period_supplement_list(db, BusinessProjectId, ShopRoyaltyId, ServerpartShopId, StartDate, EndDate)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetPeriodSupplementList 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 30. GetProjectExpenseList ====================
@router.get("/Finance/GetProjectExpenseList")
async def get_project_expense_list(
    BusinessProjectId: int = Query(0), ShopRoyaltyId: str = Query(""),
    StartMonth: str = Query(""), EndMonth: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营商户费用列表"""
    try:
        data = fin_svc.get_project_expense_list(db, BusinessProjectId, ShopRoyaltyId, StartMonth, EndMonth)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetProjectExpenseList 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 31. GetBankAccountAnalyseList ====================
@router.get("/Finance/GetBankAccountAnalyseList")
async def get_bank_account_analyse_list(
    searchMonth: str = Query(""), ServerpartIds: str = Query(""),
    ServerpartShopIds: str = Query(""), KeyWord: str = Query(""),
    SolidType: bool = Query(True),
    db: DatabaseHelper = Depends(get_db)
):
    """获取银行到账拆解明细表"""
    try:
        data = fin_svc.get_bank_account_analyse_list(db, searchMonth, ServerpartIds, ServerpartShopIds, KeyWord, SolidType)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetBankAccountAnalyseList 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 32. GetBankAccountAnalyseTreeList ====================
@router.get("/Finance/GetBankAccountAnalyseTreeList")
async def get_bank_account_analyse_tree_list(
    searchMonth: str = Query(""), ServerpartIds: str = Query(""),
    ServerpartShopIds: str = Query(""), KeyWord: str = Query(""),
    SolidType: bool = Query(True),
    db: DatabaseHelper = Depends(get_db)
):
    """获取银行到账拆解明细--树形列表"""
    try:
        data, solid_date = fin_svc.get_bank_account_analyse_tree_list(
            db, searchMonth, ServerpartIds, ServerpartShopIds, KeyWord, SolidType)
        return Result.success(JsonListData(List=data, TotalCount=len(data), OtherData=solid_date))
    except Exception as e:
        logger.error(f"GetBankAccountAnalyseTreeList 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 33. SolidBankAccountSplit ====================
@router.post("/Finance/SolidBankAccountSplit")
async def solid_bank_account_split(
    data: list,
    db: DatabaseHelper = Depends(get_db)
):
    """固化银行到账拆解明细表"""
    try:
        if not data:
            return Result.fail("保存失败，请传入有效数据！")
        ok = fin_svc.solid_bank_account_split(db, data)
        if ok:
            return Result.success(msg="保存成功")
        return Result.fail("保存失败")
    except Exception as e:
        logger.error(f"SolidBankAccountSplit 失败: {e}")
        return Result.fail(f"保存失败: {e}")


# ==================== 34. GetContractExcuteAnalysis ====================
@router.get("/Finance/GetContractExcuteAnalysis")
async def get_contract_excute_analysis(
    ServerpartIds: str = Query(""), StatisticsMonth: str = Query(""),
    Settlement_Modes: str = Query(""), keyword: str = Query(""),
    SolidType: bool = Query(False), ShowProjectNode: bool = Query(False),
    db: DatabaseHelper = Depends(get_db)
):
    """合作商户合同执行情况一览表"""
    try:
        data = fin_svc.get_contract_excute_analysis(
            db, ServerpartIds, StatisticsMonth, Settlement_Modes, keyword, SolidType, ShowProjectNode)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetContractExcuteAnalysis 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 35. RebuildSCSplit ====================
@router.api_route("/Finance/RebuildSCSplit", methods=["GET", "POST"])
async def rebuild_sc_split(
    StartDate: str = Query(""), EndDate: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """重新生成自营提成项目应收拆分数据"""
    try:
        ok = fin_svc.rebuild_sc_split(db, StartDate, EndDate)
        if ok:
            return Result.success(msg="生成完成")
        return Result.fail("生成失败")
    except Exception as e:
        logger.error(f"RebuildSCSplit 失败: {e}")
        return Result.fail(f"生成失败: {e}")


# ==================== 36. CorrectRevenueAccountData ====================
@router.post("/Finance/CorrectRevenueAccountData")
async def correct_revenue_account_data(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """更正分账收银收入差异数据"""
    try:
        ok = fin_svc.correct_revenue_account_data(db, data)
        if ok:
            return Result.success(msg="更正完成")
        return Result.fail("更正失败")
    except Exception as e:
        logger.error(f"CorrectRevenueAccountData 失败: {e}")
        return Result.fail(f"更正失败: {e}")


# ==================== 37. RebuildClosedPeriod ====================
@router.post("/Finance/RebuildClosedPeriod")
async def rebuild_closed_period(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """生成撤场经营周期结算数据"""
    try:
        ok, msg = fin_svc.rebuild_closed_period(db, data)
        if ok:
            return Result.success(msg="生成成功！")
        return Result.fail(msg or "生成失败")
    except Exception as e:
        logger.error(f"RebuildClosedPeriod 失败: {e}")
        return Result.fail(f"生成失败: {e}")


# ==================== 38. RebuildReductionPeriod ====================
@router.post("/Finance/RebuildReductionPeriod")
async def rebuild_reduction_period(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """生成经营周期免租情况结算数据"""
    try:
        ok, msg = fin_svc.rebuild_reduction_period(db, data)
        if ok:
            return Result.success(msg="生成成功！")
        return Result.fail(msg or "生成失败")
    except Exception as e:
        logger.error(f"RebuildReductionPeriod 失败: {e}")
        return Result.fail(f"生成失败: {e}")


# ==================== 39. SendSMSMessage ====================
@router.get("/Finance/SendSMSMessage")
async def send_sms_message(
    PhoneNumber: str = Query(""), UserName: str = Query(""),
    ProcessCount: int = Query(0)
):
    """发送业务审批短信提醒"""
    try:
        ok, msg = fin_svc.send_sms_message(PhoneNumber, UserName, ProcessCount)
        if ok:
            return Result.success(msg="发送成功")
        return Result.fail(f"发送失败: {msg}")
    except Exception as e:
        logger.error(f"SendSMSMessage 失败: {e}")
        return Result.fail(f"发送失败: {e}")


# ==================== 40. LadingBill ====================
@router.api_route("/Finance/LadingBill", methods=["GET", "POST"])
async def lading_bill(
    businessApprovalID: int = Query(0), approveedInfo: str = Query(""),
    approveedStaffId: int = Query(None), approveedStaffName: str = Query(""),
    SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """合同期结算流程提单"""
    try:
        ok, msg = fin_svc.lading_bill(db, businessApprovalID, approveedInfo,
                                       approveedStaffId, approveedStaffName, SourcePlatform)
        if ok:
            return Result.success(msg="提单成功！")
        return Result.fail(f"提单失败！{msg}")
    except Exception as e:
        logger.error(f"LadingBill 失败: {e}")
        return Result.fail(f"提单失败: {e}")


# ==================== 41. RejectLadingBill ====================
@router.api_route("/Finance/RejectLadingBill", methods=["GET", "POST"])
async def reject_lading_bill(
    businessApprovalID: int = Query(0), approveedStaffId: int = Query(None),
    approveedStaffName: str = Query(""), approveedInfo: str = Query(""),
    SourcePlatform: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """驳回合同期结算流程提单"""
    try:
        ok, msg = fin_svc.reject_lading_bill(db, businessApprovalID, approveedStaffId,
                                              approveedStaffName, approveedInfo, SourcePlatform)
        if ok:
            return Result.success(msg="驳回成功")
        return Result.fail(f"驳回失败！{msg}")
    except Exception as e:
        logger.error(f"RejectLadingBill 失败: {e}")
        return Result.fail(f"驳回失败: {e}")


# ==================== 42. GetAHJKtoken ====================
@router.post("/Finance/GetAHJKtoken")
async def get_ahjk_token(data: dict):
    """获取安徽交控token"""
    try:
        ok, result, msg = fin_svc.get_ahjk_token(data)
        if ok:
            return Result.success(result, msg="获取成功！")
        return Result.fail(msg or "获取失败")
    except Exception as e:
        logger.error(f"GetAHJKtoken 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 43. GetAccountCompare ====================
@router.get("/Finance/GetAccountCompare")
async def get_account_compare(
    StartDate: str = Query(""), EndDate: str = Query(""),
    ServerpartId: str = Query(""), CompareStartDate: str = Query(""),
    CompareEndDate: str = Query(""), CompareYear: int = Query(None),
    BusinessType: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营数据对比分析表"""
    try:
        data = fin_svc.get_account_compare(
            db, StartDate, EndDate, ServerpartId, CompareStartDate,
            CompareEndDate, CompareYear, BusinessType)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetAccountCompare 失败: {e}")
        return Result.fail(f"获取失败: {e}")


# ==================== 44. GetAnnualAccountList ====================
@router.get("/Finance/GetAnnualAccountList")
async def get_annual_account_list(
    StatisticsYear: str = Query(""), StartDate: str = Query(""),
    EndDate: str = Query(""), ServerpartId: str = Query(""),
    Settlement_Modes: str = Query(""), KeyWord: str = Query(""),
    SettlementState: int = Query(None), SettlementType: int = Query(None),
    db: DatabaseHelper = Depends(get_db)
):
    """获取年度结算汇总表"""
    try:
        data = fin_svc.get_annual_account_list(
            db, StatisticsYear, StartDate, EndDate, ServerpartId,
            Settlement_Modes, KeyWord, SettlementState, SettlementType)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetAnnualAccountList 失败: {e}")
        return Result.fail(f"获取失败: {e}")
