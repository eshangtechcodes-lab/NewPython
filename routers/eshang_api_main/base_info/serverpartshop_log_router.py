from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店变更日志表 API 路由
对应原 BaseInfoController.cs 中 SERVERPARTSHOP_LOG 相关 1 个接口

接口清单：
- POST /BaseInfo/GetSERVERPARTSHOP_LOGList — 列表查询
"""
from typing import Optional
from fastapi import APIRouter, Depends
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import serverpartshop_log_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetSERVERPARTSHOP_LOGList")
async def get_serverpartshop_log_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取门店变更日志表列表
    对应原: [Route("BaseInfo/GetSERVERPARTSHOP_LOGList")]
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = serverpartshop_log_service.get_serverpartshop_log_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTSHOP_LOGList 查询失败: {ex}")
        return Result.fail(msg="查询失败")
