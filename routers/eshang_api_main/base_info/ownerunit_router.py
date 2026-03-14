# -*- coding: utf-8 -*-
"""
业主单位管理表 API 路由
对应原 BaseInfoController.cs 中 OWNERUNIT 相关接口

原 C# 接口行为：
- GetOWNERUNITList: POST, 入参 SearchModel<OWNERUNITModel>
- GetOWNERUNITDetail: GET, 入参 OWNERUNITId (query param)
- SynchroOWNERUNIT: POST, 入参 OWNERUNITModel
- DeleteOWNERUNIT: GET+POST, 入参 OWNERUNITId (query param)
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import ownerunit_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetOWNERUNITList")
async def get_ownerunit_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取业主单位管理表列表
    对应原: [Route("BaseInfo/GetOWNERUNITList")] POST
    """
    try:
        if search_model is None:
            search_model = SearchModel()

        total_count, ownerunit_list = ownerunit_service.get_ownerunit_list(db, search_model)

        json_list = JsonListData.create(
            data_list=ownerunit_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetOWNERUNITList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BaseInfo/GetOWNERUNITDetail")
async def get_ownerunit_detail(
    OWNERUNITId: int = Query(..., description="业主单位管理表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取业主单位管理表明细
    对应原: [Route("BaseInfo/GetOWNERUNITDetail")] GET
    """
    try:
        ownerunit = ownerunit_service.get_ownerunit_detail(db, OWNERUNITId)
        return Result.success(data=ownerunit, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetOWNERUNITDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BaseInfo/SynchroOWNERUNIT")
async def synchro_ownerunit(
    ownerunit_data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步业主单位管理表（新增/更新）
    对应原: [Route("BaseInfo/SynchroOWNERUNIT")] POST
    """
    try:
        success, result_data = ownerunit_service.synchro_ownerunit(db, ownerunit_data)

        if success:
            return Result.success(msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroOWNERUNIT 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BaseInfo/DeleteOWNERUNIT", methods=["GET", "POST"])
async def delete_ownerunit(
    OWNERUNITId: int = Query(..., description="业主单位管理表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除业主单位管理表（软删除）
    对应原: [Route("BaseInfo/DeleteOWNERUNIT")] GET+POST
    """
    try:
        success = ownerunit_service.delete_ownerunit(db, OWNERUNITId)

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteOWNERUNIT 删除失败: {ex}")
        return Result.fail(msg="删除失败")
