from __future__ import annotations
# -*- coding: utf-8 -*-
"""
物业资产操作日志表 API 路由
对应原 BaseInfoController.cs 中 PROPERTYASSETSLOG 相关接口（L2707-2770）

接口列表（2个）：
- GetPROPERTYASSETSLOGList: POST, 分页列表查询
- SynchroPROPERTYASSETSLOG: POST, 同步（新增/更新）
"""
from typing import Optional
from fastapi import APIRouter, Depends
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import propertyassetslog_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetPROPERTYASSETSLOGList")
async def get_propertyassetslog_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取物业资产操作日志表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = propertyassetslog_service.get_propertyassetslog_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROPERTYASSETSLOGList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroPROPERTYASSETSLOG")
async def synchro_propertyassetslog(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步物业资产操作日志表（新增/更新）"""
    try:
        success = propertyassetslog_service.synchro_propertyassetslog(db, data)
        if success:
            return Result.success(data=data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroPROPERTYASSETSLOG 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")
