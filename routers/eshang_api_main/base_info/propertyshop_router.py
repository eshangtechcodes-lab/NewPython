from __future__ import annotations
# -*- coding: utf-8 -*-
"""
物业资产与商户对照表 API 路由
对应原 BaseInfoController.cs 中 PROPERTYSHOP 相关 5 个接口（L2489-2691）

接口清单：
- POST  /BaseInfo/GetPROPERTYSHOPList       — 列表查询
- GET   /BaseInfo/GetPROPERTYSHOPDetail      — 明细查询（含关联门店）
- POST  /BaseInfo/SynchroPROPERTYSHOP        — 同步（新增/更新）
- POST  /BaseInfo/BatchPROPERTYSHOP          — 批量同步
- POST  /BaseInfo/DeletePROPERTYSHOP         — 删除（软删除）
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import propertyshop_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetPROPERTYSHOPList")
async def get_propertyshop_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取物业资产与商户对照表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = propertyshop_service.get_propertyshop_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROPERTYSHOPList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetPROPERTYSHOPDetail")
async def get_propertyshop_detail(
    PROPERTYSHOPId: int = Query(..., description="物业资产与商户对照表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取物业资产与商户对照表明细（含关联门店信息）"""
    try:
        detail = propertyshop_service.get_propertyshop_detail(db, PROPERTYSHOPId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROPERTYSHOPDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroPROPERTYSHOP")
async def synchro_propertyshop(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步物业资产与商户对照表（新增/更新）"""
    try:
        success, result = propertyshop_service.synchro_propertyshop(db, data)

        if success:
            return Result.success(data=result, msg="同步成功")
        else:
            msg = result if isinstance(result, str) else "更新失败，数据不存在！"
            return Result(Result_Code=200, Result_Desc=msg)
    except Exception as ex:
        logger.error(f"SynchroPROPERTYSHOP 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.post("/BaseInfo/BatchPROPERTYSHOP")
async def batch_propertyshop(
    data: List[dict],
    db: DatabaseHelper = Depends(get_db)
):
    """批量同步物业资产与商户对照表"""
    try:
        success, result = propertyshop_service.batch_propertyshop(db, data)

        if success:
            return Result.success(data=result, msg="同步成功")
        else:
            msg = result if isinstance(result, str) else "更新失败，数据不存在！"
            return Result(Result_Code=200, Result_Desc=msg)
    except Exception as ex:
        logger.error(f"BatchPROPERTYSHOP 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.post("/BaseInfo/DeletePROPERTYSHOP")
async def delete_propertyshop(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """删除物业资产与商户对照表（软删除，入参 BaseOperateModel）"""
    try:
        # 入参映射：Id=PROPERTYASSETS_ID, RelatedId=PROPERTYSHOP_ID, ShopId=SERVERPARTSHOP_ID
        propertyassets_id = data.get("Id")
        propertyshop_id = data.get("RelatedId")
        serverpartshop_id = data.get("ShopId")
        operate_id = data.get("OperateId", 0)
        operate_name = data.get("OperateName", "")

        success, msg = propertyshop_service.delete_propertyshop(
            db,
            propertyassets_id=propertyassets_id,
            propertyshop_id=propertyshop_id,
            serverpartshop_id=serverpartshop_id,
            operate_id=operate_id,
            operate_name=operate_name
        )

        if success:
            return Result.success(msg=msg)
        else:
            return Result(Result_Code=200, Result_Desc=msg)
    except Exception as ex:
        logger.error(f"DeletePROPERTYSHOP 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
