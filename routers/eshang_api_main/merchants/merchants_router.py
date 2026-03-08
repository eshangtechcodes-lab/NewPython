from __future__ import annotations
# -*- coding: utf-8 -*-
"""
MerchantsController 路由
替代原 C# MerchantsController，包含全部 15 个接口：
  - CoopMerchants CRUD (4个)
  - CoopMerchantsType (3个，复用 AUTOSTATISTICS)
  - CoopMerchantsLinker CRUD (4个)
  - RTCoopMerchants + TradeBrandMerchants (4个)
"""
from typing import Optional
from fastapi import APIRouter, Body, Query, Depends
from loguru import logger
from core.database import db_helper, DatabaseHelper
from models.common_model import SearchModel
from routers.deps import get_db

from services.merchants.coopmerchants_service import (
    get_coopmerchants_list, get_coopmerchants_detail,
    synchro_coopmerchants, delete_coopmerchants
)
from services.merchants.coopmerchants_linker_service import (
    get_coopmerchants_linker_list, get_coopmerchants_linker_detail,
    synchro_coopmerchants_linker, delete_coopmerchants_linker
)
from services.merchants.rtcoopmerchants_service import (
    get_rtcoopmerchants_list, get_tradebrand_merchants_list,
    synchro_rtcoopmerchants, delete_rtcoopmerchants
)
# CoopMerchantsType 复用已有的 AUTOSTATISTICS service
from services.base_info.autostatistics_service import (
    synchro_autostatistics, delete_autostatistics
)

router = APIRouter()


# ================================================================
# 1. CoopMerchants 经营商户 CRUD（4 个接口）
# ================================================================

@router.post("/Merchants/GetCoopMerchantsList")
async def get_coopmerchants_list_api(search_model: Optional[SearchModel] = None):
    """获取经营商户列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = get_coopmerchants_list(db_helper, search_model)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": total_count,
                "PageIndex": search_model.PageIndex or 0,
                "PageSize": search_model.PageSize or 0,
                "List": data_list
            }
        }
    except Exception as e:
        logger.error(f"GetCoopMerchantsList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.get("/Merchants/GetCoopMerchantsDetail")
async def get_coopmerchants_detail_api(CoopMerchantsId: int = Query(...)):
    """获取经营商户明细"""
    try:
        detail = get_coopmerchants_detail(db_helper, CoopMerchantsId)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": detail or {}
        }
    except Exception as e:
        logger.error(f"GetCoopMerchantsDetail 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.post("/Merchants/SynchroCoopMerchants")
async def synchro_coopmerchants_api(body: dict = Body(default={})):
    """同步经营商户"""
    try:
        success, data, msg = synchro_coopmerchants(db_helper, body)
        if success:
            return {"Result_Code": 100, "Result_Desc": "同步成功", "Result_Data": data}
        else:
            return {"Result_Code": 200, "Result_Desc": msg}
    except Exception as e:
        logger.error(f"SynchroCoopMerchants 同步失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"同步失败{e}"}


@router.api_route("/Merchants/DeleteCoopMerchants", methods=["GET", "POST"])
async def delete_coopmerchants_api(CoopMerchantsId: int = Query(...)):
    """删除经营商户（软删除）"""
    try:
        success = delete_coopmerchants(db_helper, CoopMerchantsId)
        if success:
            return {"Result_Code": 100, "Result_Desc": "删除成功"}
        else:
            return {"Result_Code": 200, "Result_Desc": "删除失败，数据不存在！"}
    except Exception as e:
        logger.error(f"DeleteCoopMerchants 删除失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"删除失败{e}"}


# ================================================================
# 2. CoopMerchantsType 商户类型（3 个接口，复用 AUTOSTATISTICS）
# ================================================================

@router.post("/Merchants/GetCoopMerchantsTypeList")
async def get_coopmerchants_type_list_api(search_model: Optional[SearchModel] = None):
    """获取商户类型列表（复用 AUTOSTATISTICS 表，固定 TYPE=5000）"""
    try:
        if search_model is None:
            search_model = SearchModel()
        # 原 C# 在此处强制设置 AUTOSTATISTICS_TYPE = 5000
        where_sql = "WHERE AUTOSTATISTICS_TYPE = 5000"
        if search_model.SearchParameter:
            province_code = search_model.SearchParameter.get("PROVINCE_CODE")
            if province_code:
                where_sql += f" AND PROVINCE_CODE = {province_code}"

        rows = db_helper.execute_query(f"SELECT * FROM T_AUTOSTATISTICS {where_sql}")
        # 排序
        if search_model.SortStr:
            sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
            is_desc = "DESC" in (search_model.SortStr or "").upper()
            rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)

        total_count = len(rows)
        page_index = search_model.PageIndex or 0
        page_size = search_model.PageSize or 0
        if page_index > 0 and page_size > 0:
            start = (page_index - 1) * page_size
            rows = rows[start:start + page_size]
        elif len(rows) > 10:
            rows = rows[:10]

        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": total_count,
                "PageIndex": page_index,
                "PageSize": page_size,
                "List": rows
            }
        }
    except Exception as e:
        logger.error(f"GetCoopMerchantsTypeList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.post("/Merchants/SynchroCoopMerchantsType")
async def synchro_coopmerchants_type_api(body: dict = Body(default={})):
    """同步商户类型（复用 AUTOSTATISTICS，强制 TYPE=5000）"""
    try:
        body["AUTOSTATISTICS_TYPE"] = 5000
        success = synchro_autostatistics(db_helper, body)
        if success:
            return {"Result_Code": 100, "Result_Desc": "同步成功", "Result_Data": body}
        else:
            return {"Result_Code": 200, "Result_Desc": "更新失败，数据不存在！"}
    except Exception as e:
        logger.error(f"SynchroCoopMerchantsType 同步失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"同步失败{e}"}


@router.api_route("/Merchants/DeleteCoopMerchantsType", methods=["GET", "POST"])
async def delete_coopmerchants_type_api(CoopMerchantsTypeId: int = Query(...)):
    """删除商户类型（复用 AUTOSTATISTICS 删除）"""
    try:
        success = delete_autostatistics(db_helper, CoopMerchantsTypeId)
        if success:
            return {"Result_Code": 100, "Result_Desc": "删除成功"}
        else:
            return {"Result_Code": 200, "Result_Desc": "删除失败，数据不存在！"}
    except Exception as e:
        logger.error(f"DeleteCoopMerchantsType 删除失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"删除失败{e}"}


# ================================================================
# 3. CoopMerchantsLinker 商户联系人 CRUD（4 个接口）
# ================================================================

@router.post("/Merchants/GetCoopMerchantsLinkerList")
async def get_coopmerchants_linker_list_api(search_model: Optional[SearchModel] = None):
    """获取经营商户联系人列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = get_coopmerchants_linker_list(db_helper, search_model)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": total_count,
                "PageIndex": search_model.PageIndex or 0,
                "PageSize": search_model.PageSize or 0,
                "List": data_list
            }
        }
    except Exception as e:
        logger.error(f"GetCoopMerchantsLinkerList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.get("/Merchants/GetCoopMerchantsLinkerDetail")
async def get_coopmerchants_linker_detail_api(CoopMerchantsLinkerId: int = Query(...)):
    """获取经营商户联系人明细"""
    try:
        detail = get_coopmerchants_linker_detail(db_helper, CoopMerchantsLinkerId)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": detail or {}
        }
    except Exception as e:
        logger.error(f"GetCoopMerchantsLinkerDetail 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.post("/Merchants/SynchroCoopMerchantsLinker")
async def synchro_coopmerchants_linker_api(body: dict = Body(default={})):
    """同步经营商户联系人"""
    try:
        success, data = synchro_coopmerchants_linker(db_helper, body)
        if success:
            return {"Result_Code": 100, "Result_Desc": "同步成功", "Result_Data": data}
        else:
            return {"Result_Code": 200, "Result_Desc": "更新失败，数据不存在！"}
    except Exception as e:
        logger.error(f"SynchroCoopMerchantsLinker 同步失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"同步失败{e}"}


@router.api_route("/Merchants/DeleteCoopMerchantsLinker", methods=["GET", "POST"])
async def delete_coopmerchants_linker_api(CoopMerchantsLinkerId: int = Query(...)):
    """删除经营商户联系人（真删除）"""
    try:
        success = delete_coopmerchants_linker(db_helper, CoopMerchantsLinkerId)
        if success:
            return {"Result_Code": 100, "Result_Desc": "删除成功"}
        else:
            return {"Result_Code": 200, "Result_Desc": "删除失败，数据不存在！"}
    except Exception as e:
        logger.error(f"DeleteCoopMerchantsLinker 删除失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"删除失败{e}"}


# ================================================================
# 4. RTCoopMerchants + TradeBrandMerchants（4 个接口）
# ================================================================

@router.api_route("/Merchants/GetRTCoopMerchantsList", methods=["GET", "POST"])
async def get_rtcoopmerchants_list_api(CoopMerchantsId: int = Query(...), SortStr: str = Query(default="")):
    """获取经营商户品牌关联列表"""
    try:
        total_count, data_list = get_rtcoopmerchants_list(db_helper, CoopMerchantsId, SortStr)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": total_count,
                "PageIndex": 1,
                "PageSize": total_count,
                "List": data_list
            }
        }
    except Exception as e:
        logger.error(f"GetRTCoopMerchantsList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.api_route("/Merchants/GetTradeBrandMerchantsList", methods=["GET", "POST"])
async def get_tradebrand_merchants_list_api(search_model: Optional[SearchModel] = None):
    """获取经营业态品牌下商户列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total_count, data_list = get_tradebrand_merchants_list(db_helper, search_model)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": total_count,
                "PageIndex": search_model.PageIndex or 0,
                "PageSize": search_model.PageSize or 0,
                "List": data_list
            }
        }
    except Exception as e:
        logger.error(f"GetTradeBrandMerchantsList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}


@router.post("/Merchants/SynchroRTCoopMerchants")
async def synchro_rtcoopmerchants_api(body: dict = Body(default={})):
    """同步经营商户品牌关联"""
    try:
        success, data = synchro_rtcoopmerchants(db_helper, body)
        if success:
            return {"Result_Code": 100, "Result_Desc": "同步成功", "Result_Data": data}
        else:
            return {"Result_Code": 200, "Result_Desc": "更新失败，数据不存在！"}
    except Exception as e:
        logger.error(f"SynchroRTCoopMerchants 同步失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"同步失败{e}"}


@router.api_route("/Merchants/DeleteRTCoopMerchants", methods=["GET", "POST"])
async def delete_rtcoopmerchants_api(RTCoopMerchantsId: int = Query(...)):
    """删除经营商户品牌关联（真删除）"""
    try:
        success = delete_rtcoopmerchants(db_helper, RTCoopMerchantsId)
        if success:
            return {"Result_Code": 100, "Result_Desc": "删除成功"}
        else:
            return {"Result_Code": 200, "Result_Desc": "删除失败，数据不存在！"}
    except Exception as e:
        logger.error(f"DeleteRTCoopMerchants 删除失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"删除失败{e}"}
