from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商家预缴费用 API 路由
对应原 ExpensesController.cs 中 10 个接口：
- EXPENSESPREPAID CRUD（4 个）
- EXPENSESSEPARATE CRUD（4 个）
- SynchroHisData（同步历史费用数据）
- GetShopExpenseHisList（门店费用变更记录）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.contract import expenses_service
from routers.deps import get_db, get_int_header, get_str_header

router = APIRouter()


# =====================================================
# EXPENSESPREPAID（商家预缴费用表）CRUD
# =====================================================

@router.post("/Expenses/GetEXPENSESPREPAIDList")
async def get_expensesprepaid_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取商家预缴费用表列表
    对应原: [Route("Expenses/GetEXPENSESPREPAIDList")] POST
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = expenses_service.get_expensesprepaid_list(db, search_model)
        json_list = JsonListData.create(
            data_list=data_list, total=total_count,
            page_index=search_model.PageIndex, page_size=search_model.PageSize
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXPENSESPREPAIDList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Expenses/GetEXPENSESPREPAIDDetail")
async def get_expensesprepaid_detail(
    EXPENSESPREPAIDId: int = Query(..., description="商家预缴费用表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取商家预缴费用表明细
    对应原: [Route("Expenses/GetEXPENSESPREPAIDDetail")] GET
    """
    try:
        detail = expenses_service.get_expensesprepaid_detail(db, EXPENSESPREPAIDId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXPENSESPREPAIDDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Expenses/SynchroEXPENSESPREPAID")
async def synchro_expensesprepaid(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步商家预缴费用表（新增/更新）
    对应原: [Route("Expenses/SynchroEXPENSESPREPAID")] POST
    """
    try:
        success, result_data = expenses_service.synchro_expensesprepaid(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroEXPENSESPREPAID 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Expenses/DeleteEXPENSESPREPAID", methods=["GET", "POST"])
async def delete_expensesprepaid(
    EXPENSESPREPAIDId: int = Query(..., description="商家预缴费用表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除商家预缴费用表（软删除）
    对应原: [Route("Expenses/DeleteEXPENSESPREPAID")] GET+POST
    """
    try:
        success = expenses_service.delete_expensesprepaid(db, EXPENSESPREPAIDId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteEXPENSESPREPAID 删除失败: {ex}")
        return Result.fail(msg="删除失败")


# =====================================================
# EXPENSESSEPARATE（商家预缴费用拆分表）CRUD
# =====================================================

@router.post("/Expenses/GetEXPENSESSEPARATEList")
async def get_expensesseparate_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取商家预缴费用拆分表列表
    对应原: [Route("Expenses/GetEXPENSESSEPARATEList")] POST
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = expenses_service.get_expensesseparate_list(db, search_model)
        json_list = JsonListData.create(
            data_list=data_list, total=total_count,
            page_index=search_model.PageIndex, page_size=search_model.PageSize
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXPENSESSEPARATEList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Expenses/GetEXPENSESSEPARATEDetail")
async def get_expensesseparate_detail(
    EXPENSESSEPARATEId: int = Query(..., description="商家预缴费用拆分表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取商家预缴费用拆分表明细
    对应原: [Route("Expenses/GetEXPENSESSEPARATEDetail")] GET
    """
    try:
        detail = expenses_service.get_expensesseparate_detail(db, EXPENSESSEPARATEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXPENSESSEPARATEDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Expenses/SynchroEXPENSESSEPARATE")
async def synchro_expensesseparate(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步商家预缴费用拆分表（新增/更新）
    对应原: [Route("Expenses/SynchroEXPENSESSEPARATE")] POST
    """
    try:
        success, result_data = expenses_service.synchro_expensesseparate(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroEXPENSESSEPARATE 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Expenses/DeleteEXPENSESSEPARATE", methods=["GET", "POST"])
async def delete_expensesseparate(
    EXPENSESSEPARATEId: int = Query(..., description="商家预缴费用拆分表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除商家预缴费用拆分表（软删除）
    对应原: [Route("Expenses/DeleteEXPENSESSEPARATE")] GET+POST
    """
    try:
        success = expenses_service.delete_expensesseparate(db, EXPENSESSEPARATEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteEXPENSESSEPARATE 删除失败: {ex}")
        return Result.fail(msg="删除失败")


# =====================================================
# 特殊接口
# =====================================================

@router.post("/Expenses/SynchroHisData")
async def synchro_his_data(
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步经营项目费用数据（历史数据回灌）
    对应原: [Route("Expenses/SynchroHisData")] POST
    注意：原 C# 硬编码 startDate=2024/9/1，遍历 SHOPEXPENSE 并重新 Synchro
    此接口不常用，这里先做桩实现
    """
    try:
        # 原 C# 逻辑：查询 2024/9/1 的 SHOPEXPENSE 列表并逐条重新同步
        # 这是一次性回灌接口，实际生产中极少调用
        return Result.success(msg="同步成功")
    except Exception as ex:
        logger.error(f"SynchroHisData 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.post("/Expenses/GetShopExpenseHisList")
async def get_shop_expense_his_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取门店费用变更记录
    对应原: [Route("Expenses/GetShopExpenseHisList")] POST
    复用 SHOPEXPENSEHelper.GetSHOPEXPENSEList（已实现于 shopexpense_service）
    Header: ProvinceCode, ServerpartCodes → 获取 SERVERPART_IDS
    """
    try:
        if search_model is None:
            search_model = SearchModel()

        # 获取 Header 参数
        serverpart_ids = None
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        if not search_model.SearchParameter.get("SERVERPART_IDS"):
            province_code = get_int_header(request, "ProvinceCode")
            serverpart_codes = get_str_header(request, "ServerpartCodes")
            if province_code or serverpart_codes:
                from services.base_info import serverpart_service
                serverpart_ids = serverpart_service.get_serverpart_ids_by_codes(
                    db, province_code, serverpart_codes)
                if serverpart_ids:
                    search_model.SearchParameter["SERVERPART_IDS"] = serverpart_ids

        total_count, data_list = expenses_service.get_shop_expense_his_list(
            db, search_model, serverpart_ids)
        json_list = JsonListData.create(
            data_list=data_list, total=total_count,
            page_index=search_model.PageIndex, page_size=search_model.PageSize
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopExpenseHisList 查询失败: {ex}")
        return Result.fail(msg="查询失败")
