from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店提成营收(ShopRoyalty) + 应收拆分明细(SHOPROYALTYDETAIL) API 路由
路由前缀：/BusinessProject/
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.business_project import shoproyalty_service as sr_svc
from routers.deps import get_db

router = APIRouter()


# ========== ShopRoyalty 4 个接口 ==========

@router.post("/BusinessProject/GetShopRoyaltyList")
async def get_shoproyalty_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店提成营收表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total, data_list = sr_svc.get_shoproyalty_list(db, search_model)
        json_list = JsonListData.create(
            data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopRoyaltyList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetShopRoyaltyDetail")
async def get_shoproyalty_detail(
    ShopRoyaltyId: int = Query(..., description="门店提成营收表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店提成营收表明细"""
    try:
        detail = sr_svc.get_shoproyalty_detail(db, ShopRoyaltyId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopRoyaltyDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroShopRoyalty")
async def synchro_shoproyalty(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步门店提成营收表（新增/更新）"""
    try:
        success, result_data = sr_svc.synchro_shoproyalty(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroShopRoyalty 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteShopRoyalty", methods=["GET", "POST"])
async def delete_shoproyalty(
    ShopRoyaltyId: int = Query(..., description="门店提成营收表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除门店提成营收表"""
    try:
        success = sr_svc.delete_shoproyalty(db, ShopRoyaltyId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteShopRoyalty 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ========== SHOPROYALTYDETAIL 4 个接口 ==========

@router.post("/BusinessProject/GetSHOPROYALTYDETAILList")
async def get_shoproyaltydetail_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店应收拆分明细表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total, data_list = sr_svc.get_shoproyaltydetail_list(db, search_model)
        json_list = JsonListData.create(
            data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSHOPROYALTYDETAILList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetSHOPROYALTYDETAILDetail")
async def get_shoproyaltydetail_detail(
    SHOPROYALTYDETAILId: int = Query(..., description="门店应收拆分明细表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店应收拆分明细表明细"""
    try:
        detail = sr_svc.get_shoproyaltydetail_detail(db, SHOPROYALTYDETAILId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSHOPROYALTYDETAILDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroSHOPROYALTYDETAIL")
async def synchro_shoproyaltydetail(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步门店应收拆分明细表（新增/更新）"""
    try:
        success, result_data = sr_svc.synchro_shoproyaltydetail(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroSHOPROYALTYDETAIL 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteSHOPROYALTYDETAIL", methods=["GET", "POST"])
async def delete_shoproyaltydetail(
    SHOPROYALTYDETAILId: int = Query(..., description="门店应收拆分明细表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除门店应收拆分明细表"""
    try:
        success = sr_svc.delete_shoproyaltydetail(db, SHOPROYALTYDETAILId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteSHOPROYALTYDETAIL 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
