from __future__ import annotations
# -*- coding: utf-8 -*-
"""
收银人员表 API 路由
对应原 BaseInfoController.cs 中 CASHWORKER 相关 4 个接口
路由路径与原 Controller 完全一致

接口清单：
- POST      /BaseInfo/GetCASHWORKERList      — 列表查询
- GET       /BaseInfo/GetCASHWORKERDetail     — 明细查询
- POST      /BaseInfo/SynchroCASHWORKER       — 同步（新增/更新）
- GET+POST  /BaseInfo/DeleteCASHWORKER        — 删除
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Header
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import cashworker_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetCASHWORKERList")
async def get_cashworker_list(
    search_model: Optional[SearchModel] = None,
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取收银人员表列表
    对应原: [Route("BaseInfo/GetCASHWORKERList")]
    注意: 原 Controller 从 Header 获取 ServerpartCodes 赋值给 SERVERPART_CODES
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        # 原 Controller: searchModel.SearchParameter.SERVERPART_CODES = GetStringHeader("ServerpartCodes", ...)
        if serverpartcodes and not search_model.SearchParameter.get("SERVERPART_CODES"):
            search_model.SearchParameter["SERVERPART_CODES"] = serverpartcodes

        total_count, data_list = cashworker_service.get_cashworker_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCASHWORKERList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BaseInfo/GetCASHWORKERDetail")
async def get_cashworker_detail(
    CASHWORKERId: int = Query(..., description="收银人员表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取收银人员表明细
    对应原: [Route("BaseInfo/GetCASHWORKERDetail")]
    """
    try:
        detail = cashworker_service.get_cashworker_detail(db, CASHWORKERId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCASHWORKERDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BaseInfo/SynchroCASHWORKER")
async def synchro_cashworker(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步收银人员表（新增/更新）
    对应原: [Route("BaseInfo/SynchroCASHWORKER")]
    注意: 原 Controller 返回 model data (ReturnJson(100, msg, cashworkerModel))
    """
    try:
        success, result_data = cashworker_service.synchro_cashworker(db, data)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroCASHWORKER 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BaseInfo/DeleteCASHWORKER", methods=["GET", "POST"])
async def delete_cashworker(
    CASHWORKERId: int = Query(..., description="收银人员表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除收银人员表
    对应原: [Route("BaseInfo/DeleteCASHWORKER")]
    注意: 原 C# 实现中 Delete 方法为空实现，始终返回 false
    """
    try:
        success = cashworker_service.delete_cashworker(db, CASHWORKERId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteCASHWORKER 删除失败: {ex}")
        return Result.fail(msg="删除失败")
