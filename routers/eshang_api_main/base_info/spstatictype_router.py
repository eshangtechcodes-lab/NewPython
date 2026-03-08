from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区类别关联表 API 路由
对应原 BasicConfigController.cs 中 SPSTATICTYPE 相关接口
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import spstatictype_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BasicConfig/GetSPSTATICTYPEList")
async def get_spstatictype_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区类别关联表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = spstatictype_service.get_spstatictype_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPSTATICTYPEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BasicConfig/GetSPSTATICTYPEDetail")
async def get_spstatictype_detail(
    SPSTATICTYPEId: int = Query(..., description="服务区类别关联表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区类别关联表明细"""
    try:
        detail = spstatictype_service.get_spstatictype_detail(db, SPSTATICTYPEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPSTATICTYPEDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BasicConfig/SynchroSPSTATICTYPE")
async def synchro_spstatictype(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步服务区类别关联表（新增/更新）"""
    try:
        success, result_data = spstatictype_service.synchro_spstatictype(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroSPSTATICTYPE 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BasicConfig/DeleteSPSTATICTYPE", methods=["GET", "POST"])
async def delete_spstatictype(
    SPSTATICTYPEId: int = Query(..., description="服务区类别关联表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除服务区类别关联表（真删除）"""
    try:
        success = spstatictype_service.delete_spstatictype(db, SPSTATICTYPEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteSPSTATICTYPE 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
