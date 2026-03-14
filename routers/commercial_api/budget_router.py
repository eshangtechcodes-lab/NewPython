# -*- coding: utf-8 -*-
"""
CommercialApi - Budget 路由（重构版）
对应原 CommercialApi/Controllers/BudgetController.cs
财务预算相关接口（4个接口）
业务逻辑已移至 services/commercial/budget_service.py
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db
from services.commercial import budget_service

router = APIRouter()


@router.post("/Budget/GetBUDGETPROJECT_AHList")
async def get_budget_project_ah_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取安徽财务预算表列表"""
    try:
        total, page_rows = budget_service.get_budget_project_ah_list(db, searchModel)
        json_list = JsonListData.create(
            data_list=page_rows, total=total,
            page_index=(searchModel or {}).get("PageIndex", 1),
            page_size=(searchModel or {}).get("PageSize", 20))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBUDGETPROJECT_AHList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Budget/GetBUDGETPROJECT_AHDetail")
async def get_budget_project_ah_detail(
    BUDGETPROJECT_AHId: Optional[int] = Query(None, description="安徽财务预算表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细"""
    try:
        data = budget_service.get_budget_project_ah_detail(db, BUDGETPROJECT_AHId)
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBUDGETPROJECT_AHDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Budget/GetBudgetProjectDetailList")
async def get_budget_project_detail_list(
    BUDGETPROJECT_AH_ID: Optional[int] = Query(None, description="预算项目ID"),
    BUDGETPROJECT_YEAR: Optional[int] = Query(None, description="项目年份"),
    STATISTICS_MONTH: Optional[int] = Query(None, description="统计月份"),
    SERVERPART_ID: Optional[str] = Query("", description="服务区内码"),
    ACCOUNT_CODE: Optional[str] = Query("", description="一级科目代码"),
    STATISTICS_DATE: Optional[str] = Query("", description="结算日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度安徽财务预算明细表数据"""
    try:
        tree_list = budget_service.get_budget_project_detail_list(
            db, BUDGETPROJECT_AH_ID, BUDGETPROJECT_YEAR, STATISTICS_MONTH,
            SERVERPART_ID, ACCOUNT_CODE, STATISTICS_DATE)
        json_list = JsonListData.create(data_list=tree_list, total=len(tree_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetProjectDetailList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Budget/GetBudgetMainShow")
async def get_budget_main_show(
    serverpartId: Optional[str] = Query(None, description="服务区内码"),
    year: Optional[int] = Query(None, description="年份"),
    month: Optional[int] = Query(None, description="月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细（主页展示）"""
    try:
        # TODO: 实现查询逻辑后移至 budget_service
        logger.warning("GetBudgetMainShow 查询逻辑暂未实现")
        _cost_item = {"Name": None, "ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None, "PartRate": None}
        _income_item = {"Name": None, "ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None,
                         "ThisMonthIncome": None, "ThisMonthIncomeRate": None, "Details": None}
        return Result.success(data={
            "Cost": {"ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None, "InOutRate": None, "Items": [_cost_item]},
            "Income": {"ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None, "CostRate": None, "IncomeChangeRate": None, "ThisYearCost": None, "Items": [_income_item]},
            "monthAmount": {"ThisMonthIn": None, "ThisMonthOut": None, "CostInRate": None, "InOutRate": None, "IncomeChangeRate": None, "PayoutChangeRate": None},
            "yearProfit": {"ThisYearTotal": None, "ThisYearTotalC": None, "ThisYearBudget": None, "ThisYearBudgetC": None, "CompleteRate": None, "CompleteRateC": None, "TRate": None},
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetMainShow 查询失败: {ex}")
        return Result.fail(msg="查询失败")
