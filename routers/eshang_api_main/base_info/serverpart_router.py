from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区站点 API 路由
对应原 BaseInfoController.cs 中 SERVERPART 相关接口

原 C# 接口行为：
- GetSERVERPARTList: POST, 入参 SearchModel<SERVERPARTModel>
- DeleteSERVERPART: GET+POST, 入参 SERVERPARTId (query param), 真删除
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import serverpart_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetSERVERPARTList")
async def get_serverpart_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取服务区站点列表
    对应原: [Route("BaseInfo/GetSERVERPARTList")] POST
    """
    try:
        if search_model is None:
            search_model = SearchModel()

        total_count, serverpart_list = serverpart_service.get_serverpart_list(db, search_model)

        json_list = JsonListData.create(
            data_list=serverpart_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSERVERPARTList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.api_route("/BaseInfo/DeleteSERVERPART", methods=["GET", "POST"])
async def delete_serverpart(
    SERVERPARTId: int = Query(..., description="服务区站点内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除服务区站点（真删除）
    对应原: [Route("BaseInfo/DeleteSERVERPART")] GET+POST
    """
    try:
        success = serverpart_service.delete_serverpart(db, SERVERPARTId)

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteSERVERPART 删除失败: {ex}")
        return Result.fail(msg="删除失败")
