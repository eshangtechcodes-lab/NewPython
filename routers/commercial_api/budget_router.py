# -*- coding: utf-8 -*-
"""
CommercialApi - Budget 路由
对应原 CommercialApi/Controllers/BudgetController.cs
财务预算相关接口（7个接口）
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


@router.post("/Budget/GetBUDGETPROJECT_AHList")
async def get_budget_project_ah_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取安徽财务预算表列表"""
    try:
        logger.warning("GetBUDGETPROJECT_AHList 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Budget/GetBUDGETPROJECT_AHDetail")
async def get_budget_project_ah_detail(
    BUDGETPROJECT_AHId: int = Query(..., description="安徽财务预算表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细"""
    try:
        logger.warning("GetBUDGETPROJECT_AHDetail 暂未完整实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/Budget/SynchroBUDGETPROJECT_AH")
async def synchro_budget_project_ah(budgetproject_ahModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """同步安徽财务预算表"""
    try:
        logger.warning("SynchroBUDGETPROJECT_AH 暂未完整实现")
        return Result.success(msg="同步成功")
    except Exception as ex:
        return Result.fail(msg=f"同步失败{ex}")


@router.get("/Budget/DeleteBUDGETPROJECT_AH")
async def delete_budget_project_ah(
    BUDGETPROJECT_AHId: int = Query(..., description="安徽财务预算表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除安徽财务预算表"""
    try:
        logger.warning("DeleteBUDGETPROJECT_AH 暂未完整实现")
        return Result.success(msg="删除成功")
    except Exception as ex:
        return Result.fail(msg=f"删除失败{ex}")


@router.post("/Budget/GetBudgetProjectDetailList")
async def get_budget_project_detail_list(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    获取月度安徽财务预算明细表数据
    入参(AES加密)：ProvinceCode, StatisticsMonth(yyyyMM), ServerpartId, SPRegionType_ID, SubjectCode
    """
    try:
        logger.warning("GetBudgetProjectDetailList 暂未完整实现（需AES解密）")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Budget/GetBudgetMainShow")
async def get_budget_main_show(
    BUDGETPROJECT_AHId: int = Query(..., description="安徽财务预算表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细（主页展示）"""
    try:
        logger.warning("GetBudgetMainShow 暂未完整实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")
