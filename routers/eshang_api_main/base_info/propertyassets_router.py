from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区资产表 API 路由
对应原 BaseInfoController.cs 中 PROPERTYASSETS 相关接口（L2159-2485）
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import propertyassets_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetPROPERTYASSETSList")
async def get_propertyassets_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区资产表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = propertyassets_service.get_propertyassets_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROPERTYASSETSList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/GetPROPERTYASSETSTreeList")
async def get_propertyassets_tree_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区资产 树形分组列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, tree_list = propertyassets_service.get_propertyassets_tree_list(db, search_model)
        json_list = JsonListData.create(data_list=tree_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROPERTYASSETSTreeList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetAssetsRevenueAmount")
async def get_assets_revenue_amount(
    searchMonth: str = Query(..., description="查询收益月份 yyyyMM"),
    ServerpartIds: str = Query(..., description="服务区ID"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区资产总效益（每平米效益）"""
    try:
        result_list = propertyassets_service.get_assets_revenue_amount(db, searchMonth, ServerpartIds)
        total_count = len(result_list)
        json_list = JsonListData.create(data_list=result_list, total=total_count)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAssetsRevenueAmount 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetPROPERTYASSETSDetail")
async def get_propertyassets_detail(
    PROPERTYASSETSId: int = Query(..., description="服务区资产表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区资产表明细"""
    try:
        detail = propertyassets_service.get_propertyassets_detail(db, PROPERTYASSETSId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROPERTYASSETSDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroPROPERTYASSETS")
async def synchro_propertyassets(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步服务区资产表（新增/更新，含资产编码唯一性验证）"""
    try:
        # 必填校验
        if not data.get("PROPERTYASSETS_CODE") or data.get("SERVERPART_ID") is None:
            return Result(Result_Code=999, Result_Desc="同步失败：资产编码,服务区内码必填")

        success, assets_id, message = propertyassets_service.synchro_propertyassets(db, data)
        if success:
            return Result.success(data=data, msg=f"同步成功{message}")
        else:
            return Result(Result_Code=200, Result_Desc=message or "更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroPROPERTYASSETS 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.post("/BaseInfo/BatchPROPERTYASSETS")
async def batch_propertyassets(
    model_list: list,
    db: DatabaseHelper = Depends(get_db)
):
    """批量同步服务区资产表（含关联门店）"""
    try:
        if not model_list:
            return Result(Result_Code=999, Result_Desc="同步失败：资产编码,服务区内码必填")

        # 校验必填
        for m in model_list:
            if not m.get("PROPERTYASSETS_CODE") or m.get("SERVERPART_ID") is None:
                return Result(Result_Code=999, Result_Desc="同步失败：资产编码,服务区内码必填")

        success, message = propertyassets_service.batch_propertyassets(db, model_list)
        if success:
            return Result.success(data=model_list, msg=f"同步成功{message}")
        else:
            return Result(Result_Code=200, Result_Desc=message or "更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"BatchPROPERTYASSETS 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.post("/BaseInfo/DeletePROPERTYASSETS")
async def delete_propertyassets(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """删除服务区资产表（软删除，接收 BaseOperateModel）"""
    try:
        propertyassets_id = data.get("Id")
        if propertyassets_id is None:
            return Result(Result_Code=200, Result_Desc="删除失败，缺少Id参数！")

        operate_id = data.get("OperateId", 0)
        operate_name = data.get("OperateName", "")

        success = propertyassets_service.delete_propertyassets(db, propertyassets_id, operate_id, operate_name)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeletePROPERTYASSETS 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
