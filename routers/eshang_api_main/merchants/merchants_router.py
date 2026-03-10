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
from fastapi import APIRouter, Body, Query, Depends, Request
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
    synchro_autostatistics, delete_autostatistics, _process_row as _process_autostatistics_row
)
# AUTOSTATISTICS_ICO 的 URL 前缀（C# Config.AppSettings.CoopMerchantUrls）
COOP_MERCHANT_URLS = "https://eshangtech.com:8443"

router = APIRouter()


# ================================================================
# 1. CoopMerchants 经营商户 CRUD（4 个接口）
# ================================================================

@router.post("/Merchants/GetCoopMerchantsList")
async def get_coopmerchants_list_api(request: Request, search_model: Optional[SearchModel] = None):
    """获取经营商户列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        # C# Controller: searchModel.SearchParameter.PROVINCE_CODE = GetIntHeader("ProvinceCode", ...)
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        header_pc = request.headers.get("provincecode") or request.headers.get("ProvinceCode")
        if header_pc and not search_model.SearchParameter.get("PROVINCE_CODE"):
            try:
                search_model.SearchParameter["PROVINCE_CODE"] = int(header_pc)
            except (ValueError, TypeError):
                pass
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

def _bind_autostatistics_model(row: dict) -> dict:
    """
    复制 C# AUTOSTATISTICSHelper.GetAUTOSTATISTICSList 中的 BindDataRowToModel 逻辑
    - 按固定字段顺序输出
    - AUTOSTATISTICS_TYPE==2000 时设置 INELASTIC_DEMAND = STATISTICS_TYPE
    - AUTOSTATISTICS_ICO 以 / 开头时加 CoopMerchantUrls 前缀
    """
    model = {}
    model["AUTOSTATISTICS_ID"] = row.get("AUTOSTATISTICS_ID") or 0
    model["AUTOSTATISTICS_PID"] = row.get("AUTOSTATISTICS_PID") or 0
    model["AUTOSTATISTICS_NAME"] = row.get("AUTOSTATISTICS_NAME") or ""
    model["AUTOSTATISTICS_VALUE"] = row.get("AUTOSTATISTICS_VALUE") or ""
    model["AUTOSTATISTICS_INDEX"] = row.get("AUTOSTATISTICS_INDEX") or 0
    model["AUTOSTATISTICS_TYPE"] = row.get("AUTOSTATISTICS_TYPE") or 0
    model["STATISTICS_TYPE"] = row.get("STATISTICS_TYPE") or 0
    # C#: if (autostatisticsModel.AUTOSTATISTICS_TYPE == 2000) INELASTIC_DEMAND = STATISTICS_TYPE
    if model["AUTOSTATISTICS_TYPE"] == 2000:
        model["INELASTIC_DEMAND"] = row.get("STATISTICS_TYPE") or 0
    else:
        model["INELASTIC_DEMAND"] = None
    # AUTOSTATISTICS_ICO: / 开头时拼接商户平台地址
    ico = row.get("AUTOSTATISTICS_ICO") or ""
    if ico and ico.startswith("/"):
        ico = COOP_MERCHANT_URLS + ico
    model["AUTOSTATISTICS_ICO"] = ico
    model["OWNERUNIT_ID"] = row.get("OWNERUNIT_ID") or 0
    model["OWNERUNIT_NAME"] = row.get("OWNERUNIT_NAME") or ""
    model["PROVINCE_CODE"] = row.get("PROVINCE_CODE") or 0
    model["AUTOSTATISTICS_STATE"] = row.get("AUTOSTATISTICS_STATE") or 0
    model["STAFF_ID"] = row.get("STAFF_ID") or 0
    model["STAF_NAME"] = row.get("STAF_NAME") or ""
    # 日期格式由 database.py 统一处理为 ISO 格式（与 C# 一致）
    model["OPERATE_DATE"] = row.get("OPERATE_DATE")
    model["AUTOSTATISTICS_DESC"] = row.get("AUTOSTATISTICS_DESC") or ""
    return model


@router.post("/Merchants/GetCoopMerchantsTypeList")
async def get_coopmerchants_type_list_api(request: Request, search_model: Optional[SearchModel] = None):
    """获取商户类型列表（复用 AUTOSTATISTICS 表，固定 TYPE=5000）"""
    try:
        if search_model is None:
            search_model = SearchModel()
        # C# Controller: searchModel.SearchParameter.PROVINCE_CODE = GetIntHeader("ProvinceCode", ...)
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        header_pc = request.headers.get("provincecode") or request.headers.get("ProvinceCode")
        if header_pc and not search_model.SearchParameter.get("PROVINCE_CODE"):
            try:
                search_model.SearchParameter["PROVINCE_CODE"] = int(header_pc)
            except (ValueError, TypeError):
                pass
        # C# 在 Controller 中强制设置 AUTOSTATISTICS_TYPE = 5000
        where_parts = ["AUTOSTATISTICS_TYPE = 5000"]
        province_code = search_model.SearchParameter.get("PROVINCE_CODE")
        if province_code:
            where_parts.append(f"PROVINCE_CODE = {province_code}")
        # C# GetWhereSQL 对 SearchParameter 的普通字段做 = 过滤
        # 排除 AUTOSTATISTICS_ID 和 INELASTIC_DEMAND（C# 显式跳过这两个）
        skip_fields = {"AUTOSTATISTICS_ID", "INELASTIC_DEMAND", "PROVINCE_CODE",
                       "AUTOSTATISTICS_TYPE", "current", "pageSize", "total"}
        for k, v in search_model.SearchParameter.items():
            if k in skip_fields or v is None or v == "":
                continue
            if isinstance(v, str):
                where_parts.append(f"{k} LIKE '%{v}%'")
            else:
                where_parts.append(f"{k} = {v}")
        # C# 的 INELASTIC_DEMAND 参数映射到 STATISTICS_TYPE
        inelastic = search_model.SearchParameter.get("INELASTIC_DEMAND")
        if inelastic is not None and inelastic != "":
            where_parts.append(f"STATISTICS_TYPE = {inelastic}")

        where_sql = " AND ".join(where_parts)
        rows = db_helper.execute_query(f"SELECT * FROM T_AUTOSTATISTICS WHERE {where_sql}")

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

        # C# 风格的 field-by-field 绑定
        data_list = [_bind_autostatistics_model(r) for r in rows]

        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": total_count,
                "PageIndex": page_index,
                "PageSize": page_size,
                "List": data_list
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
async def get_tradebrand_merchants_list_api(request: Request, search_model: Optional[SearchModel] = None):
    """获取经营业态品牌下商户列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        # C# Controller: searchModel.SearchParameter.PROVINCE_CODE = GetIntHeader("ProvinceCode", ...)
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        header_pc = request.headers.get("provincecode") or request.headers.get("ProvinceCode")
        if header_pc and not search_model.SearchParameter.get("PROVINCE_CODE"):
            try:
                search_model.SearchParameter["PROVINCE_CODE"] = int(header_pc)
            except (ValueError, TypeError):
                pass
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


# ================================================================
# 5. BM-03 补齐: GetCoopMerchantsDDL 商户下拉框
# ================================================================

@router.get("/Merchants/GetCoopMerchantsDDL")
async def get_coopmerchants_ddl(
    ProvinceCode: int = Query(None),
    OwnerUnitId: int = Query(None),
    CoopMerchantsState: int = Query(1),
    ServerpartId: int = Query(None),
    CoopMerchantsName: str = Query("")
):
    """绑定商户下拉框"""
    try:
        # 直接查询 T_COOPMERCHANTS 表
        conditions = []
        if CoopMerchantsState is not None:
            conditions.append(f"COOPMERCHANTS_STATE = {CoopMerchantsState}")
        if ProvinceCode is not None:
            conditions.append(f"PROVINCE_CODE = {ProvinceCode}")
        if OwnerUnitId is not None:
            conditions.append(f"OWNERUNIT_ID = {OwnerUnitId}")
        if ServerpartId is not None:
            conditions.append(f"SERVERPART_ID = {ServerpartId}")
        if CoopMerchantsName:
            conditions.append(f"COOPMERCHANTS_NAME LIKE '%{CoopMerchantsName}%'")
        where = " AND ".join(conditions) if conditions else "1=1"
        sql = f"SELECT COOPMERCHANTS_ID, COOPMERCHANTS_NAME FROM T_COOPMERCHANTS WHERE {where} ORDER BY COOPMERCHANTS_NAME"
        rows = db_helper.execute_query(sql) or []
        # 返回 CommonModel 兼容格式
        result = [{"Id": r.get("COOPMERCHANTS_ID"), "Name": r.get("COOPMERCHANTS_NAME")} for r in rows]
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "TotalCount": len(result),
                "PageIndex": 1,
                "PageSize": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetCoopMerchantsDDL 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{e}"}

