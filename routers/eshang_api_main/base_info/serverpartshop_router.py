from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店 API 路由
对应原 BaseInfoController.cs 中 ServerpartShop 相关接口

原 C# 接口行为：
- GetServerpartShopList: POST, 入参 SearchModel<SERVERPARTSHOPModel>, 分页列表
- GetServerpartShopDetail: GET, 入参 ServerpartShopId (query), 门店明细
- SynchroServerpartShop: POST, 入参 SERVERPARTSHOPModel, 同步（新增/更新）
- DeleteServerpartShop: GET+POST, 入参 ServerpartShopId (query), 软删除 ISVALID=0
- DelServerpartShop: GET+POST, 入参 BaseOperateModel (body), 软删除
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from pydantic import BaseModel
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import serverpartshop_service
from routers.deps import get_db, get_int_header

router = APIRouter()


class BaseOperateModel(BaseModel):
    """基本操作模型（对应原 C# BaseOperateModel）"""
    Id: int = 0
    OperateId: Optional[float] = None      # 操作人内码
    OperateName: Optional[str] = None       # 操作人名称


@router.post("/BaseInfo/GetServerpartShopList")
async def get_serverpartshop_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取门店列表
    对应原: [Route("BaseInfo/GetServerpartShopList")] POST
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        # 原 C# L268-280: 从 Header 读取 ProvinceCode / ServerpartCodes / ServerpartShopIds
        if not search_model.SearchParameter.get("PROVINCE_CODE"):
            search_model.SearchParameter["PROVINCE_CODE"] = get_int_header(request, "ProvinceCode")
        if not search_model.SearchParameter.get("SERVERPART_CODE"):
            sc = request.headers.get("ServerpartCodes") or request.headers.get("serverpartcodes") or ""
            if sc:
                search_model.SearchParameter["SERVERPART_CODE"] = sc
        if not search_model.SearchParameter.get("SERVERPARTSHOP_IDS"):
            si = request.headers.get("ServerpartShopIds") or request.headers.get("serverpartshopids") or ""
            if si:
                search_model.SearchParameter["SERVERPARTSHOP_IDS"] = si
        total_count, shop_list = serverpartshop_service.get_serverpartshop_list(db, search_model)

        json_list = JsonListData.create(
            data_list=shop_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartShopList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.api_route("/BaseInfo/GetServerpartShopDetail", methods=["GET", "POST"])
async def get_serverpartshop_detail(
    ServerpartShopId: int = Query(..., description="门店内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取门店明细
    对应原: [Route("BaseInfo/GetServerpartShopDetail")] GET
    """
    try:
        detail = serverpartshop_service.get_serverpartshop_detail(db, ServerpartShopId)

        if detail:
            return Result.success(data=detail, msg="查询成功")
        else:
            return Result(Result_Code=200, Result_Desc="未找到数据")
    except Exception as ex:
        logger.error(f"GetServerpartShopDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BaseInfo/SynchroServerpartShop")
async def synchro_serverpartshop(
    serverpartshopModel: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步门店数据（新增/更新）
    对应原: [Route("BaseInfo/SynchroServerpartShop")] POST
    """
    try:
        success, updated_model = serverpartshop_service.synchro_serverpartshop(db, serverpartshopModel)

        if success:
            return Result.success(data=updated_model, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="同步失败")
    except Exception as ex:
        logger.error(f"SynchroServerpartShop 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BaseInfo/DeleteServerpartShop", methods=["GET", "POST"])
async def delete_serverpartshop(
    ServerpartShopId: int = Query(..., description="门店内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除门店（软删除 ISVALID=0）
    对应原: [Route("BaseInfo/DeleteServerpartShop")] GET+POST
    """
    try:
        success = serverpartshop_service.delete_serverpartshop(db, ServerpartShopId)

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteServerpartShop 删除失败: {ex}")
        return Result.fail(msg="删除失败")


@router.api_route("/BaseInfo/DelServerpartShop", methods=["GET", "POST"])
async def del_serverpartshop(
    model: BaseOperateModel,
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除门店（通过 BaseOperateModel, 软删除 ISVALID=0）
    对应原: [Route("BaseInfo/DelServerpartShop")] POST
    """
    try:
        success = serverpartshop_service.delete_serverpartshop(
            db, model.Id,
            operate_id=model.OperateId,
            operate_name=model.OperateName
        )

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DelServerpartShop 删除失败: {ex}")
        return Result.fail(msg="删除失败")
