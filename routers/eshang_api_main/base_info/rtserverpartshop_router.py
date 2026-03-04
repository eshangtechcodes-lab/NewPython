from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店经营时间表 API 路由
对应原 BaseInfoController.cs 中 RTSERVERPARTSHOP 相关 4 个接口
路由路径与原 Controller 完全一致

接口清单：
- POST      /BaseInfo/GetRTSERVERPARTSHOPList      — 列表查询
- GET       /BaseInfo/GetRTSERVERPARTSHOPDetail     — 明细查询
- POST      /BaseInfo/SynchroRTSERVERPARTSHOP       — 同步（新增/更新）
- GET+POST  /BaseInfo/DeleteRTSERVERPARTSHOP         — 删除（真删除）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import rtserverpartshop_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetRTSERVERPARTSHOPList")
async def get_rtserverpartshop_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取门店经营时间表列表
    对应原: [Route("BaseInfo/GetRTSERVERPARTSHOPList")]
    入参: SearchModel<RTSERVERPARTSHOPModel>（直接 JSON）
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = rtserverpartshop_service.get_rtserverpartshop_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRTSERVERPARTSHOPList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetRTSERVERPARTSHOPDetail")
async def get_rtserverpartshop_detail(
    RTSERVERPARTSHOPId: int = Query(..., description="门店经营时间表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取门店经营时间表明细
    对应原: [Route("BaseInfo/GetRTSERVERPARTSHOPDetail")]
    """
    try:
        detail = rtserverpartshop_service.get_rtserverpartshop_detail(db, RTSERVERPARTSHOPId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRTSERVERPARTSHOPDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroRTSERVERPARTSHOP")
async def synchro_rtserverpartshop(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步门店经营时间表（新增/更新）
    对应原: [Route("BaseInfo/SynchroRTSERVERPARTSHOP")]
    入参: RTSERVERPARTSHOPModel 直接 JSON
    """
    try:
        success, result_data = rtserverpartshop_service.synchro_rtserverpartshop(db, data)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroRTSERVERPARTSHOP 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteRTSERVERPARTSHOP", methods=["GET", "POST"])
async def delete_rtserverpartshop(
    RTSERVERPARTSHOPId: int = Query(..., description="门店经营时间表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除门店经营时间表（真删除）
    对应原: [Route("BaseInfo/DeleteRTSERVERPARTSHOP")]
    """
    try:
        success = rtserverpartshop_service.delete_rtserverpartshop(db, RTSERVERPARTSHOPId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteRTSERVERPARTSHOP 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
