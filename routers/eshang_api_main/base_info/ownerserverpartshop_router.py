from __future__ import annotations
# -*- coding: utf-8 -*-
"""
业主单位门店关联关系表 API 路由
对应原 BasicConfigController.cs 中 OWNERSERVERPARTSHOP 相关接口
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import ownerserverpartshop_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BasicConfig/GetOWNERSERVERPARTSHOPList")
async def get_ownerserverpartshop_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取业主单位门店关联关系表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = ownerserverpartshop_service.get_ownerserverpartshop_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetOWNERSERVERPARTSHOPList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BasicConfig/GetOWNERSERVERPARTSHOPDetail")
async def get_ownerserverpartshop_detail(
    OWNERSERVERPARTSHOPId: int = Query(..., description="业主单位门店关联关系表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业主单位门店关联关系表明细"""
    try:
        detail = ownerserverpartshop_service.get_ownerserverpartshop_detail(db, OWNERSERVERPARTSHOPId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetOWNERSERVERPARTSHOPDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BasicConfig/SynchroOWNERSERVERPARTSHOP")
async def synchro_ownerserverpartshop(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步业主单位门店关联关系表（新增/更新）"""
    try:
        success, result_data = ownerserverpartshop_service.synchro_ownerserverpartshop(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroOWNERSERVERPARTSHOP 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BasicConfig/DeleteOWNERSERVERPARTSHOP", methods=["GET", "POST"])
async def delete_ownerserverpartshop(
    OWNERSERVERPARTSHOPId: int = Query(..., description="业主单位门店关联关系表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除业主单位门店关联关系表（真删除）"""
    try:
        success = ownerserverpartshop_service.delete_ownerserverpartshop(db, OWNERSERVERPARTSHOPId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteOWNERSERVERPARTSHOP 删除失败: {ex}")
        return Result.fail(msg="删除失败")
