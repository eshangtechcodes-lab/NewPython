from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店管理（业主端 New）API 路由
对应原 BaseInfoController.cs 中 ServerPartShopNew 相关接口（L3765-3900）

接口列表（4个）：
- GetServerPartShopNewList:     GET,  门店组合列表（查视图 V_SERVERPARTSHOP_COMBINE）
- GetServerPartShopNewDetail:   GET,  门店明细（含经营状态+附属记录）
- ServerPartShopNewSaveState:   POST, 设置门店经营状态
- SynchroServerPartShopNew:     POST, 同步门店数据

注意：GetList 和 GetDetail 的参数来自 Query/Header，而非 Body
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Header
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.base_info import serverpartshop_service
from routers.deps import get_db

router = APIRouter()


@router.get("/BaseInfo/GetServerPartShopNewList")
async def get_server_part_shop_new_list(
    provinceCode: Optional[int] = Query(None, description="省份编码"),
    serverPartId: Optional[int] = Query(None, description="服务区内码"),
    shopName: Optional[str] = Query(None, description="门店名称（模糊搜索）"),
    businessState: Optional[int] = Query(None, description="经营状态(1000/2000/3000)"),
    businessType: Optional[int] = Query(None, description="经营模式"),
    pageIndex: int = Query(0, description="页码"),
    pageSize: int = Query(0, description="每页条数"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店组合列表（业主端使用，查视图 V_SERVERPARTSHOP_COMBINE）"""
    try:
        total_count, data_list = serverpartshop_service.get_server_part_shop_new_list(
            db,
            province_code=provinceCode,
            server_part_id=serverPartId,
            server_part_codes=serverpartcodes,
            shop_name=shopName,
            business_state=businessState,
            business_type=businessType,
            page_index=pageIndex,
            page_size=pageSize,
        )
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=pageIndex, page_size=pageSize)
        return Result.success(data=json_list.model_dump(), msg="成功")
    except Exception as ex:
        logger.error(f"GetServerPartShopNewList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BaseInfo/GetServerPartShopNewDetail")
async def get_server_part_shop_new_detail(
    serverPartShopId: int = Query(..., description="门店内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店明细（含经营状态列表 + 附属记录）"""
    try:
        detail = serverpartshop_service.get_server_part_shop_new_detail(db, serverPartShopId)
        if not detail:
            return Result(Result_Code=200, Result_Desc="门店不存在")
        return Result.success(data=detail, msg="成功")
    except Exception as ex:
        logger.error(f"GetServerPartShopNewDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BaseInfo/ServerPartShopNewSaveState")
async def server_part_shop_new_save_state(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """设置门店经营状态（仅支持 1000/2000/3000）"""
    try:
        success, msg = serverpartshop_service.server_part_shop_new_save_state(db, data)
        if success:
            return Result.success(msg=msg)
        else:
            return Result(Result_Code=200, Result_Desc=msg)
    except Exception as ex:
        logger.error(f"ServerPartShopNewSaveState 操作失败: {ex}")
        return Result.fail(msg="操作失败")


@router.post("/BaseInfo/SynchroServerPartShopNew")
async def synchro_server_part_shop_new(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步门店数据（遍历 ShopBusinessStateList 批量更新）"""
    try:
        success = serverpartshop_service.synchro_server_part_shop_new(db, data)
        if success:
            return Result.success(data=data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="同步失败")
    except Exception as ex:
        logger.error(f"SynchroServerPartShopNew 同步失败: {ex}")
        return Result.fail(msg="同步失败")
