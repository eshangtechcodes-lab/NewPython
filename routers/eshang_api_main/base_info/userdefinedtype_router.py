from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商品自定义类别表 API 路由
对应原 BaseInfoController.cs 中 USERDEFINEDTYPE 相关接口（L1647-1828）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import userdefinedtype_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetUSERDEFINEDTYPEList")
async def get_userdefinedtype_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品自定义类别表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = userdefinedtype_service.get_userdefinedtype_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetUSERDEFINEDTYPEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetUSERDEFINEDTYPEDetail")
async def get_userdefinedtype_detail(
    USERDEFINEDTYPEId: int = Query(..., description="商品自定义类别表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品自定义类别表明细"""
    try:
        detail = userdefinedtype_service.get_userdefinedtype_detail(db, USERDEFINEDTYPEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetUSERDEFINEDTYPEDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroUSERDEFINEDTYPE")
async def synchro_userdefinedtype(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步商品自定义类别表（新增/更新）"""
    try:
        success = userdefinedtype_service.synchro_userdefinedtype(db, data)
        if success:
            return Result.success(msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroUSERDEFINEDTYPE 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteUSERDEFINEDTYPE", methods=["GET", "POST"])
async def delete_userdefinedtype(
    USERDEFINEDTYPEId: int = Query(..., description="商品自定义类别表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除商品自定义类别表（软删除，USERDEFINEDTYPE_STATE=0）"""
    try:
        success = userdefinedtype_service.delete_userdefinedtype(db, USERDEFINEDTYPEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteUSERDEFINEDTYPE 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


@router.post("/BaseInfo/CreatePriceType")
async def create_price_type(
    ServerpartId: str = Query(..., description="服务区内码"),
    BusinessType: str = Query(..., description="商品业态"),
    STAFF_ID: Optional[int] = Query(None, description="操作人内码"),
    STAFF_NAME: str = Query("", description="操作人姓名"),
    db: DatabaseHelper = Depends(get_db)
):
    """生成价格分类"""
    try:
        userdefinedtype_service.create_price_type(
            db, ServerpartId, BusinessType,
            staff_id=STAFF_ID, staff_name=STAFF_NAME
        )
        return Result.success(data="操作成功", msg="操作成功")
    except Exception as ex:
        logger.error(f"CreatePriceType 失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
