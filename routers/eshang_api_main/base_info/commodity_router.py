from __future__ import annotations
# -*- coding: utf-8 -*-
"""
在售商品 API 路由
对应原 BaseInfoController.cs 中 COMMODITY 相关接口（L2831-3117）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import commodity_service
from routers.deps import get_db, get_int_header

router = APIRouter()


@router.post("/BaseInfo/GetCOMMODITYList")
async def get_commodity_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取在售商品列表（含 Header 权限过滤）"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        # 判断当前账户是否为商户（从 header 获取 UserPattern）
        user_pattern = request.headers.get("UserPattern")
        if user_pattern != "2000":
            # 非商户账户，从 header 获取 ServerpartCodes
            if not search_model.SearchParameter.get("SERVERPART_IDS"):
                serverpart_codes = request.headers.get("ServerpartCodes", "")
                if serverpart_codes:
                    # 根据 ServerpartCodes 查询对应的 SERVERPART_IDS
                    try:
                        codes_in = ",".join([f"'{c.strip()}'" for c in serverpart_codes.split(",") if c.strip()])
                        ids_sql = f"SELECT SERVERPART_ID FROM T_SERVERPART WHERE SERVERPART_CODE IN ({codes_in})"
                        id_rows = db.execute_query(ids_sql)
                        if id_rows:
                            search_model.SearchParameter["SERVERPART_IDS"] = ",".join(
                                [str(r["SERVERPART_ID"]) for r in id_rows])
                    except Exception as e:
                        logger.warning(f"根据 ServerpartCodes 查询 IDS 失败: {e}")

        total_count, data_list = commodity_service.get_commodity_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCOMMODITYList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/BaseInfo/GetCOMMODITYDetail")
async def get_commodity_detail(
    COMMODITYId: int = Query(..., description="在售商品内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取在售商品明细"""
    try:
        detail = commodity_service.get_commodity_detail(db, COMMODITYId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCOMMODITYDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BaseInfo/SynchroCOMMODITY")
async def synchro_commodity(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步在售商品（新增/更新）"""
    try:
        success = commodity_service.synchro_commodity(db, data)
        if success:
            return Result.success(data=data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroCOMMODITY 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.post("/BaseInfo/OnShelfCommodity")
async def on_shelf_commodity(
    request: Request,
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    上架在售商品
    原 C# 从表单读参数（Pub.Request），Python 改为接收 JSON body
    """
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        province_code = data.get("ProvinceCode")
        commodity_ids = data.get("commodityIds")
        staff_name = data.get("staffName", "")

        if not commodity_ids:
            return Result(Result_Code=200, Result_Desc="上架失败，缺少 commodityIds 参数！")

        success = commodity_service.on_shelf_commodity(db, province_code, commodity_ids, staff_name)
        if success:
            return Result.success(msg="上架成功")
        else:
            return Result(Result_Code=200, Result_Desc="上架失败，数据不存在！")
    except Exception as ex:
        logger.error(f"OnShelfCommodity 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.post("/BaseInfo/LowerShelfCommodity")
async def lower_shelf_commodity(
    request: Request,
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    下架在售商品
    原 C# 从表单读参数（Pub.Request），Python 改为接收 JSON body
    """
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        province_code = data.get("ProvinceCode")
        commodity_ids = data.get("commodityIds")
        commodity_state = data.get("commodityState", 0)

        if not commodity_ids:
            return Result(Result_Code=200, Result_Desc="下架失败，缺少 commodityIds 参数！")

        success = commodity_service.lower_shelf_commodity(db, province_code, commodity_ids, int(commodity_state))
        if success:
            return Result.success(msg="下架成功")
        else:
            return Result(Result_Code=200, Result_Desc="下架失败，数据不存在！")
    except Exception as ex:
        logger.error(f"LowerShelfCommodity 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BaseInfo/DeleteCOMMODITY", methods=["GET", "POST"])
async def delete_commodity(
    COMMODITYId: int = Query(..., description="在售商品内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除在售商品（软删除 COMMODITY_STATE=0，支持 GET/POST）"""
    try:
        success = commodity_service.delete_commodity(db, COMMODITYId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteCOMMODITY 删除失败: {ex}")
        return Result.fail(msg="删除失败")
