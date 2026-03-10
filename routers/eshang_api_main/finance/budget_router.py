from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BudgetProjectAHController 路由（16 个接口）
BUDGETPROJECT_AH CRUD (4) + BUDGETDETAIL_AH CRUD (4)
+ SetBudgetDetailAHList (1) + 报表接口 (7)
"""
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.finance import budget_service as bud_svc
from routers.deps import get_db

router = APIRouter()


# ==================== BUDGETPROJECT_AH CRUD ====================

@router.post("/Budget/GetBudgetProjectList")
async def get_budget_project_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    """获取安徽财务预算表列表"""
    try:
        rows, total = bud_svc.get_budget_project_list(db, data)
        page_index = data.get("PageIndex", 1)
        page_size = data.get("PageSize", 15)
        return Result.success(JsonListData(
            List=rows, TotalCount=total,
            PageIndex=page_index, PageSize=page_size))
    except Exception as e:
        logger.error(f"GetBudgetProjectList 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectDetail")
async def get_budget_project_detail(
    BUDGETPROJECT_AHId: int = Query(0),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细"""
    try:
        row = bud_svc.get_budget_project_detail(db, BUDGETPROJECT_AHId)
        return Result.success(row)
    except Exception as e:
        logger.error(f"GetbudgetProjectDetail 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.post("/Budget/SynchroBudgetProject")
async def synchro_budget_project(data: dict, db: DatabaseHelper = Depends(get_db)):
    """同步安徽财务预算表"""
    try:
        ok, result = bud_svc.synchro_budget_project(db, data)
        if ok:
            return Result.success(result, msg="同步成功")
        return Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"SynchroBudgetProject 失败: {e}")
        return Result.fail(f"同步失败{e}")


@router.api_route("/Budget/DeleteBudgetProject", methods=["GET", "POST"])
async def delete_budget_project(
    BUDGETPROJECT_AHId: int = Query(0),
    db: DatabaseHelper = Depends(get_db)
):
    """删除安徽财务预算表"""
    try:
        ok = bud_svc.delete_budget_project(db, BUDGETPROJECT_AHId)
        if ok:
            return Result.success(msg="删除成功")
        return Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"DeleteBudgetProject 失败: {e}")
        return Result.fail(f"删除失败{e}")


# ==================== BUDGETDETAIL_AH CRUD ====================

@router.post("/Budget/GetBudgetDetailList")
async def get_budget_detail_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    """获取安徽财务预算明细表列表（含合计）"""
    try:
        rows, total, summary = bud_svc.get_budget_detail_list(db, data)
        page_index = data.get("PageIndex", 1)
        page_size = data.get("PageSize", 15)
        return Result.success(JsonListData(
            List=rows, TotalCount=total,
            PageIndex=page_index, PageSize=page_size,
            OtherData=summary))
    except Exception as e:
        logger.error(f"GetBudgetDetailList 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetBudgetDetailDetail")
async def get_budget_detail_detail(
    BUDGETDETAIL_AHId: int = Query(0),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算明细表明细"""
    try:
        row = bud_svc.get_budget_detail_detail(db, BUDGETDETAIL_AHId)
        return Result.success(row)
    except Exception as e:
        logger.error(f"GetBudgetDetailDetail 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.post("/Budget/SynchroBudgetDetail")
async def synchro_budget_detail(data: dict, db: DatabaseHelper = Depends(get_db)):
    """同步安徽财务预算明细表"""
    try:
        ok, result = bud_svc.synchro_budget_detail(db, data)
        if ok:
            return Result.success(result, msg="同步成功")
        return Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"SynchroBudgetDetail 失败: {e}")
        return Result.fail(f"同步失败{e}")


@router.api_route("/Budget/DeleteBudgetDetail", methods=["GET", "POST"])
async def delete_budget_detail(
    BUDGETDETAIL_AHId: int = Query(0),
    db: DatabaseHelper = Depends(get_db)
):
    """删除安徽财务预算明细表"""
    try:
        ok = bud_svc.delete_budget_detail(db, BUDGETDETAIL_AHId)
        if ok:
            return Result.success(msg="删除成功")
        return Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"DeleteBudgetDetail 失败: {e}")
        return Result.fail(f"删除失败{e}")


# ==================== 散装接口 ====================

@router.post("/Budget/SetBudgetDetailAHList")
async def set_budget_detail_ah_list(request: Request, db: DatabaseHelper = Depends(get_db)):
    """财务预算批量保存"""
    try:
        data = await request.json()
        if not isinstance(data, list):
            data = [data]
        ok, msg = bud_svc.set_budget_detail_ah_list(db, data)
        if ok:
            return Result.success(msg="保存成功")
        return Result.fail(f"保存失败，{msg}！", code=200)
    except Exception as e:
        logger.error(f"SetBudgetDetailAHList 失败: {e}")
        return Result.fail(f"保存失败{e}")


@router.get("/Budget/GetBudgetProjectReportOfMonth")
async def get_budget_project_report_of_month(
    SERVERPART_ID: str = Query(""), Year: int = Query(0),
    Account_Code: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取财务预算月度统计报表"""
    try:
        data = bud_svc.get_budget_project_report_of_month(db, SERVERPART_ID, Year, Account_Code)
        return Result.success(JsonListData(List=data, TotalCount=len(data)))
    except Exception as e:
        logger.error(f"GetBudgetProjectReportOfMonth 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectReport")
async def get_budget_project_report(
    Month: int = Query(0), db: DatabaseHelper = Depends(get_db)
):
    """获取财务营收报表"""
    try:
        data = bud_svc.get_budget_project_report(db, Month)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetbudgetProjectReport 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectReportDynamic")
async def get_budget_project_report_dynamic(
    Month: int = Query(0), db: DatabaseHelper = Depends(get_db)
):
    """获取财务营收报表（动态）"""
    try:
        data = bud_svc.get_budget_project_report_dynamic(db, Month)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetbudgetProjectReportDynamic 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectReportIn")
async def get_budget_project_report_in(
    Month: int = Query(0), db: DatabaseHelper = Depends(get_db)
):
    """获取财务营收报表-收入部分"""
    try:
        data = bud_svc.get_budget_project_report_in(db, Month)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetbudgetProjectReportIn 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectReportInDynamic")
async def get_budget_project_report_in_dynamic(
    Month: int = Query(0), db: DatabaseHelper = Depends(get_db)
):
    """获取财务营收报表-收入部分(动态)"""
    try:
        data = bud_svc.get_budget_project_report_in_dynamic(db, Month)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetbudgetProjectReportInDynamic 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectReportOut")
async def get_budget_project_report_out(
    Month: int = Query(0), db: DatabaseHelper = Depends(get_db)
):
    """获取财务营收报表-支出部分"""
    try:
        data = bud_svc.get_budget_project_report_out(db, Month)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetbudgetProjectReportOut 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Budget/GetbudgetProjectReportOutDynamic")
async def get_budget_project_report_out_dynamic(
    Month: int = Query(0), db: DatabaseHelper = Depends(get_db)
):
    """获取财务营收报表-支出部分(动态)"""
    try:
        data = bud_svc.get_budget_project_report_out_dynamic(db, Month)
        return Result.success(data)
    except Exception as e:
        logger.error(f"GetbudgetProjectReportOutDynamic 失败: {e}")
        return Result.fail(f"查询失败{e}")
