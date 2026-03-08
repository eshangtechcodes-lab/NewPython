from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区成本核算对照表 API 路由
对应原 BaseInfoController.cs 中 SERVERPARTCRT 相关接口（L1978-2158）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import serverpartcrt_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetSERVERPARTCRTList")
async def get_serverpartcrt_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区成本核算对照表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = serverpartcrt_service.get_serverpartcrt_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTCRTList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/GetSERVERPARTCRTTreeList")
async def get_serverpartcrt_tree_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区成本核算对照表 树形列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, tree_list = serverpartcrt_service.get_serverpartcrt_tree_list(db, search_model)
        json_list = JsonListData.create(data_list=tree_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTCRTTreeList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetSERVERPARTCRTDetail")
async def get_serverpartcrt_detail(
    SERVERPARTCRTId: Optional[int] = Query(None, description="成本核算对照表内码"),
    SERVERPARTTId: Optional[int] = Query(None, description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区成本核算对照表明细"""
    try:
        detail = serverpartcrt_service.get_serverpartcrt_detail(db, SERVERPARTCRTId, SERVERPARTTId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTCRTDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroSERVERPARTCRT")
async def synchro_serverpartcrt(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步服务区成本核算对照表（新增/更新）"""
    try:
        success = serverpartcrt_service.synchro_serverpartcrt(db, data)
        if success:
            return Result.success(data=data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroSERVERPARTCRT 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.post("/BaseInfo/DeleteSERVERPARTCRT")
async def delete_serverpartcrt(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """删除服务区成本核算对照表（真删除，接收 BaseOperateModel）"""
    try:
        serverpartcrt_id = data.get("Id")
        if serverpartcrt_id is None:
            return Result(Result_Code=200, Result_Desc="删除失败，缺少Id参数！")

        success = serverpartcrt_service.delete_serverpartcrt(db, serverpartcrt_id)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteSERVERPARTCRT 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
