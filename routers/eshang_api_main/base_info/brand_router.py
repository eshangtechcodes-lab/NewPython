from __future__ import annotations
# -*- coding: utf-8 -*-
"""
品牌表 API 路由
对应原 BaseInfoController.cs 中 Brand 相关 6 个接口
路由路径与原 Controller 完全一致

接口清单：
- POST /BaseInfo/GetBrandList        — 品牌列表（SearchModel 直接 JSON）
- GET  /BaseInfo/GetCombineBrandList  — 组合品牌列表（Query 参数）
- GET+POST /BaseInfo/GetTradeBrandTree — 经营品牌树（Query 参数）
- GET  /BaseInfo/GetBrandDetail       — 品牌明细
- POST /BaseInfo/SynchroBrand         — 同步品牌（BRANDModel 直接 JSON）
- GET+POST /BaseInfo/DeleteBrand      — 删除品牌（软删除）
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import brand_service
from routers.deps import get_db, get_int_header

router = APIRouter()


@router.post("/BaseInfo/GetBrandList")
async def get_brand_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取品牌表列表
    对应原: [Route("BaseInfo/GetBrandList")]
    入参: SearchModel<BRANDModel>（直接 JSON）
    注意: 原 Controller 会从 Header 获取 ProvinceCode 默认值
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        # 原 C# L801: searchModel.SearchParameter.PROVINCE_CODE = GetIntHeader("ProvinceCode", ...)
        if not search_model.SearchParameter.get("PROVINCE_CODE"):
            search_model.SearchParameter["PROVINCE_CODE"] = get_int_header(request, "ProvinceCode")
        total_count, brand_list = brand_service.get_brand_list(db, search_model)

        json_list = JsonListData.create(
            data_list=brand_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBrandList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetCombineBrandList")
async def get_combine_brand_list(
    request: Request,
    PROVINCE_CODE: Optional[int] = Query(None, description="省份编码"),
    SPREGIONTYPE_IDS: str = Query("", description="片区内码"),
    SERVERPART_IDS: str = Query("", description="服务区内码"),
    BRAND_INDUSTRY: str = Query("", description="经营业态"),
    BRAND_TYPE: str = Query("", description="品牌类型"),
    BRAND_STATE: str = Query("", description="有效状态"),
    BRAND_NAME: str = Query("", description="品牌名称（模糊查询）"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取组合品牌列表
    对应原: [Route("BaseInfo/GetCombineBrandList")]
    入参: GET Query 参数 + Header: ProvinceCode
    """
    try:
        # 原 C# L845: PROVINCE_CODE = GetIntHeader("ProvinceCode", PROVINCE_CODE)
        if PROVINCE_CODE is None:
            header_val = request.headers.get("provincecode") or request.headers.get("ProvinceCode")
            if header_val:
                try:
                    PROVINCE_CODE = int(header_val)
                except (ValueError, TypeError):
                    PROVINCE_CODE = 0
            else:
                PROVINCE_CODE = 0

        brand_list, his_project_list = brand_service.get_combine_brand_list(
            db, PROVINCE_CODE, SPREGIONTYPE_IDS, SERVERPART_IDS,
            BRAND_INDUSTRY, BRAND_TYPE, BRAND_STATE, BRAND_NAME
        )

        # 原 C# 使用 JsonList<T, List<T>> 双列表响应，第二列表为 OtherData
        json_list = {
            "List": brand_list,
            "TotalCount": len(brand_list),
            "PageIndex": 1,
            "PageSize": len(brand_list),
            "OtherData": his_project_list,
        }

        return Result.success(data=json_list, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCombineBrandList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.api_route("/BaseInfo/GetTradeBrandTree", methods=["GET", "POST"])
async def get_trade_brand_tree(
    request: Request,
    BusinessTrade_PID: int = Query(-1, description="经营业态父级内码"),
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    OwnerUnitId: Optional[int] = Query(None, description="业主单位内码"),
    BrandState: Optional[int] = Query(None, description="有效状态"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营品牌树
    对应原: [Route("BaseInfo/GetTradeBrandTree")]
    """
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        tree = brand_service.get_trade_brand_tree(
            db, BusinessTrade_PID, ProvinceCode, OwnerUnitId, BrandState
        )
        total_count = len(tree)

        json_list = {
            "List": tree,
            "TotalCount": total_count,
            "PageIndex": 1,
            "PageSize": total_count,
        }

        return Result.success(data=json_list, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTradeBrandTree 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BaseInfo/GetBrandDetail")
async def get_brand_detail(
    BrandId: int = Query(..., description="品牌内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取品牌表明细
    对应原: [Route("BaseInfo/GetBrandDetail")]
    """
    try:
        brand = brand_service.get_brand_detail(db, BrandId)
        return Result.success(data=brand, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBrandDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroBrand")
async def synchro_brand(
    brand_data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步品牌表（新增/更新）
    对应原: [Route("BaseInfo/SynchroBrand")]
    入参: BRANDModel 直接 JSON（非 AES 加密）
    注意: 原 Controller 强制设置 BRAND_CATEGORY = 1000
    """
    try:
        # 原 Controller 强制设置默认值
        brand_data["BRAND_CATEGORY"] = 1000

        success, result_data, failure_msg = brand_service.synchro_brand(db, brand_data)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc=failure_msg)
    except Exception as ex:
        logger.error(f"SynchroBrand 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteBrand", methods=["GET", "POST"])
async def delete_brand(
    BrandId: int = Query(..., description="品牌内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除品牌表（软删除）
    对应原: [Route("BaseInfo/DeleteBrand")]
    """
    try:
        success = brand_service.delete_brand(db, BrandId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteBrand 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
