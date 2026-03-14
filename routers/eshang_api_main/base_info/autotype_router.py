from __future__ import annotations
# -*- coding: utf-8 -*-
"""
自定义类别表 API 路由
对应原 BasicConfigController.cs 中 AUTOTYPE 相关接口（L18-L243）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import autotype_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BasicConfig/GetAUTOTYPEList")
async def get_autotype_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取自定义类别表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = autotype_service.get_autotype_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAUTOTYPEList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BasicConfig/GetAUTOTYPEDetail")
async def get_autotype_detail(
    AUTOTYPEId: int = Query(..., description="自定义类别表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取自定义类别表明细"""
    try:
        detail = autotype_service.get_autotype_detail(db, AUTOTYPEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAUTOTYPEDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BasicConfig/SynchroAUTOTYPE")
async def synchro_autotype(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步自定义类别表（新增/更新）"""
    try:
        success, result_data = autotype_service.synchro_autotype(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroAUTOTYPE 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BasicConfig/DeleteAUTOTYPE", methods=["GET", "POST"])
async def delete_autotype(
    AUTOTYPEId: int = Query(..., description="自定义类别表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除自定义类别表（软删除，AUTOTYPE_VALID=0）"""
    try:
        success = autotype_service.delete_autotype(db, AUTOTYPEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteAUTOTYPE 删除失败: {ex}")
        return Result.fail(msg="删除失败")


@router.get("/BasicConfig/GetNestingAUTOTYPEList")
async def get_nesting_autotype_list(
    AUTOTYPE_TYPEID: int = Query(..., description="类别类型：1000【组织架构】"),
    AUTOTYPE_PID: int = Query(-1, description="上级分类内码"),
    OWNERUNIT_ID: str = Query("", description="业主单位内码"),
    SearchKey: str = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取自定义类别表嵌套列表"""
    try:
        data_list = autotype_service.get_nesting_autotype_list(
            db, AUTOTYPE_TYPEID, AUTOTYPE_PID, OWNERUNIT_ID, SearchKey
        )
        json_list = JsonListData.create(data_list=data_list, total=len(data_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingAUTOTYPEList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BasicConfig/GetNestingAUTOTYPETree")
async def get_nesting_autotype_tree(
    AUTOTYPE_TYPEID: int = Query(..., description="类别类型：1000【组织架构】"),
    AUTOTYPE_PID: int = Query(-1, description="上级分类内码"),
    OWNERUNIT_ID: str = Query("", description="业主单位内码"),
    SearchKey: str = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取自定义类别表嵌套树"""
    try:
        data_list = autotype_service.get_nesting_autotype_tree(
            db, AUTOTYPE_TYPEID, AUTOTYPE_PID, OWNERUNIT_ID, SearchKey
        )
        json_list = JsonListData.create(data_list=data_list, total=len(data_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingAUTOTYPETree 查询失败: {ex}")
        return Result.fail(msg="查询失败")
