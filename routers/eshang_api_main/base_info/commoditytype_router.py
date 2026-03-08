from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商品类别 API 路由
对应原 BaseInfoController.cs 中 COMMODITYTYPE 相关接口（L1421-1646）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import commoditytype_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetCOMMODITYTYPEList")
async def get_commoditytype_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品类别列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = commoditytype_service.get_commoditytype_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCOMMODITYTYPEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetCOMMODITYTYPEDetail")
async def get_commoditytype_detail(
    COMMODITYTYPEId: int = Query(..., description="商品类别内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品类别明细"""
    try:
        detail = commoditytype_service.get_commoditytype_detail(db, COMMODITYTYPEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCOMMODITYTYPEDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroCOMMODITYTYPE")
async def synchro_commoditytype(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步商品类别（新增/更新）"""
    try:
        success = commoditytype_service.synchro_commoditytype(db, data)
        if success:
            return Result.success(msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroCOMMODITYTYPE 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteCOMMODITYTYPE", methods=["GET", "POST"])
async def delete_commoditytype(
    COMMODITYTYPEId: int = Query(..., description="商品类别内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除商品类别（软删除，COMMODITYTYPE_VALID=0）"""
    try:
        success = commoditytype_service.delete_commoditytype(db, COMMODITYTYPEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteCOMMODITYTYPE 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


@router.get("/BaseInfo/GetNestingCOMMODITYTYPEList")
async def get_nesting_commoditytype_list(
    COMMODITYTYPE_PID: str = Query("-1", description="上级分类"),
    PROVINCE_CODE: Optional[str] = Query(None, description="省份编码"),
    COMMODITYTYPE_VALID: Optional[str] = Query(None, description="分类是否有效"),
    SearchKey: Optional[str] = Query(None, description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品类别嵌套列表"""
    try:
        tree_list = commoditytype_service.get_nesting_commoditytype_list(
            db, commoditytype_pid=COMMODITYTYPE_PID, province_code=PROVINCE_CODE,
            commoditytype_valid=COMMODITYTYPE_VALID, search_key=SearchKey
        )
        json_list = JsonListData.create(data_list=tree_list, total=0, page_index=1, page_size=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingCOMMODITYTYPEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetNestingCOMMODITYTYPETree")
async def get_nesting_commoditytype_tree(
    COMMODITYTYPE_PID: str = Query("-1", description="上级分类"),
    PROVINCE_CODE: Optional[str] = Query(None, description="省份编码"),
    COMMODITYTYPE_VALID: Optional[str] = Query(None, description="分类是否有效"),
    SearchKey: Optional[str] = Query(None, description="模糊查询内容"),
    ShowCode: bool = Query(False, description="是否显示商品类型代码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品类别嵌套树（CommonTypeModel 精简结构）"""
    try:
        tree_list = commoditytype_service.get_nesting_commoditytype_tree(
            db, commoditytype_pid=COMMODITYTYPE_PID, province_code=PROVINCE_CODE,
            commoditytype_valid=COMMODITYTYPE_VALID, search_key=SearchKey, show_code=ShowCode
        )
        json_list = JsonListData.create(data_list=tree_list, total=0, page_index=1, page_size=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingCOMMODITYTYPETree 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
