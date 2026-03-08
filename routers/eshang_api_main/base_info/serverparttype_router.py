from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区类别表 API 路由
对应原 BasicConfigController.cs 中 SERVERPARTTYPE 相关接口（含嵌套列表/树和 ModifyRT）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Header
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import serverparttype_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BasicConfig/GetSERVERPARTTYPEList")
async def get_serverparttype_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区类别表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = serverparttype_service.get_serverparttype_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTTYPEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BasicConfig/GetSERVERPARTTYPEDetail")
async def get_serverparttype_detail(
    SERVERPARTTYPEId: int = Query(..., description="服务区类别表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区类别表明细（含 RTServerpartList）"""
    try:
        detail = serverparttype_service.get_serverparttype_detail(db, SERVERPARTTYPEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTTYPEDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BasicConfig/SynchroSERVERPARTTYPE")
async def synchro_serverparttype(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步服务区类别表（新增/更新）"""
    try:
        success, result_data = serverparttype_service.synchro_serverparttype(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroSERVERPARTTYPE 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BasicConfig/DeleteSERVERPARTTYPE", methods=["GET", "POST"])
async def delete_serverparttype(
    SERVERPARTTYPEId: int = Query(..., description="服务区类别表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除服务区类别表（软删除，TYPE_STATE=0）"""
    try:
        success = serverparttype_service.delete_serverparttype(db, SERVERPARTTYPEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteSERVERPARTTYPE 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


@router.get("/BasicConfig/GetNestingSERVERPARTTYPEList")
async def get_nesting_serverparttype_list(
    SERVERPARTSTATICTYPE_ID: str = Query("1000,4000", alias="STATIC_TYPE", description="类别类型（1000区域/4000省份）"),
    TYPE_PID: str = Query("-1", description="上级类别"),
    TYPE_STATE: int = Query(None, description="有效状态"),
    SearchKey: str = Query(None, description="模糊查询"),
    ProvinceCode: str = Header("", description="省份标识"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区类别表嵌套列表（Header: ProvinceCode）"""
    try:
        data_list = serverparttype_service.get_nesting_serverparttype_list(
            db, ProvinceCode, SERVERPARTSTATICTYPE_ID, TYPE_PID, TYPE_STATE, SearchKey or ""
        )
        json_list = JsonListData.create(data_list=data_list, total=len(data_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingSERVERPARTTYPEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BasicConfig/GetNestingSERVERPARTTYPETree")
async def get_nesting_serverparttype_tree(
    SERVERPARTSTATICTYPE_ID: str = Query("1000,4000", alias="STATIC_TYPE", description="类别类型（1000区域/4000省份）"),
    TYPE_PID: str = Query("-1", description="上级类别"),
    TYPE_STATE: int = Query(None, description="有效状态"),
    SearchKey: str = Query(None, description="模糊查询"),
    ProvinceCode: str = Header("", description="省份标识"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区类别表嵌套树（Header: ProvinceCode）"""
    try:
        data_list = serverparttype_service.get_nesting_serverparttype_tree(
            db, ProvinceCode, SERVERPARTSTATICTYPE_ID, TYPE_PID, TYPE_STATE, SearchKey or ""
        )
        json_list = JsonListData.create(data_list=data_list, total=len(data_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingSERVERPARTTYPETree 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BasicConfig/ModifyRTServerpartType")
async def modify_rt_serverpart_type(
    ServerpartIds: str = Query(..., description="服务区内码列表（逗号分隔）"),
    ServerparttypeId: int = Query(..., description="服务区类别内码"),
    ServerpartType: int = Query(0, description="服务区类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """修改服务区类别关联"""
    try:
        success = serverparttype_service.modify_rt_serverpart_type(
            db, ServerpartIds, ServerparttypeId, ServerpartType
        )
        if success:
            return Result.success(data="操作成功", msg="操作成功")
        else:
            return Result(Result_Code=200, Result_Desc="操作失败！")
    except Exception as ex:
        logger.error(f"ModifyRTServerpartType 操作失败: {ex}")
        return Result.fail(msg=f"操作失败{ex}")
