from __future__ import annotations
# -*- coding: utf-8 -*-
"""
附件上传（Finance ATTACHMENT）API 路由
对应原 FinanceController.cs 中 ATTACHMENT 相关 4 个接口
路由路径与原 Controller 完全一致

接口清单：
- GET+POST  /Finance/GetATTACHMENTList      — 列表查询（按财务流程内码+数据类型）
- GET+POST  /Finance/GetATTACHMENTDetail     — 明细查询
- POST      /Finance/SynchroATTACHMENT       — 同步（新增/更新，仅 RUNNING 表）
- GET+POST  /Finance/DeleteATTACHMENT        — 删除（真删除，仅 RUNNING 表）
"""
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.finance import fattachment_service
from routers.deps import get_db

router = APIRouter()


@router.api_route("/Finance/GetATTACHMENTList", methods=["GET", "POST"])
async def get_attachment_list(
    FinanceProinstId: int = Query(..., description="财务流程内码"),
    DataType: int = Query(..., description="数据类型：0=RUNNING，1=STORAGE"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取附件上传列表"""
    try:
        data_list = fattachment_service.get_attachment_list(db, FinanceProinstId, DataType)

        json_list = JsonListData.create(
            data_list=data_list,
            total=len(data_list),
            page_index=0,
            page_size=len(data_list)
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetATTACHMENTList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.api_route("/Finance/GetATTACHMENTDetail", methods=["GET", "POST"])
async def get_attachment_detail(
    ATTACHMENTId: int = Query(..., description="附件上传内码"),
    DataType: int = Query(..., description="数据类型：0=RUNNING，1=STORAGE"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取附件上传明细"""
    try:
        detail = fattachment_service.get_attachment_detail(db, ATTACHMENTId, DataType)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetATTACHMENTDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Finance/SynchroATTACHMENT")
async def synchro_attachment(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步附件上传（新增/更新）——仅 RUNNING 表"""
    try:
        success, result_data = fattachment_service.synchro_attachment(db, data)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroATTACHMENT 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Finance/DeleteATTACHMENT", methods=["GET", "POST"])
async def delete_attachment(
    ATTACHMENTId: int = Query(..., description="附件上传内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除附件上传（真删除）——仅 RUNNING 表"""
    try:
        success = fattachment_service.delete_attachment(db, ATTACHMENTId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteATTACHMENT 删除失败: {ex}")
        return Result.fail(msg="删除失败")
