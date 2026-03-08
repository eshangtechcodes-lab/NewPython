from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区门店对照表 API 路由
对应原 BasicConfigController.cs 中 SERVERPARTSHOPCRT 相关接口
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import serverpartshopcrt_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BasicConfig/GetSERVERPARTSHOPCRTList")
async def get_serverpartshopcrt_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区门店对照表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = serverpartshopcrt_service.get_serverpartshopcrt_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTSHOPCRTList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BasicConfig/GetSERVERPARTSHOPCRTDetail")
async def get_serverpartshopcrt_detail(
    SERVERPARTSHOPCRTId: int = Query(..., description="服务区门店对照表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区门店对照表明细"""
    try:
        detail = serverpartshopcrt_service.get_serverpartshopcrt_detail(db, SERVERPARTSHOPCRTId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTSHOPCRTDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BasicConfig/SynchroSERVERPARTSHOPCRT")
async def synchro_serverpartshopcrt(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步服务区门店对照表（新增/更新）"""
    try:
        success, result_data = serverpartshopcrt_service.synchro_serverpartshopcrt(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroSERVERPARTSHOPCRT 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BasicConfig/DeleteSERVERPARTSHOPCRT", methods=["GET", "POST"])
async def delete_serverpartshopcrt(
    SERVERPARTSHOPCRTId: int = Query(..., description="服务区门店对照表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除服务区门店对照表（原C#未实现，始终返回失败）"""
    try:
        success = serverpartshopcrt_service.delete_serverpartshopcrt(db, SERVERPARTSHOPCRTId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败！")
    except Exception as ex:
        logger.error(f"DeleteSERVERPARTSHOPCRT 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
