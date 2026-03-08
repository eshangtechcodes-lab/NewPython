from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营业态 API 路由
对应原 BaseInfoController.cs 中 BusinessTrade 相关接口（L1026-1265）

原 C# 接口行为：
- GetBusinessTradeList: POST, 入参 SearchModel<AUTOSTATISTICSModel>，强制 AUTOSTATISTICS_TYPE=2000
- GetBusinessTradeTree: GET+POST, 入参 Query 参数（BusinessTrade_PID, ProvinceCode, OwnerUnitId, BusinessTradeState）
- GetBusinessTradeEnum: GET+POST, 入参 Query 参数（同上 + SearchKey）
- GetBusinessTradeDetail: GET+POST, 入参 BusinessTradeId
- SynchroBusinessTrade: POST, 入参 AUTOSTATISTICSModel，强制 AUTOSTATISTICS_TYPE=2000
- DeleteBusinessTrade: GET+POST, 入参 BusinessTradeId
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import businesstrade_service
from routers.deps import get_db, get_int_header

router = APIRouter()


@router.post("/BaseInfo/GetBusinessTradeList")
async def get_businesstrade_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营业态列表
    对应原: [Route("BaseInfo/GetBusinessTradeList")] POST
    强制过滤 AUTOSTATISTICS_TYPE=2000
    """
    try:
        if search_model is None:
            search_model = SearchModel()

        # 原 C# L1044: searchModel.SearchParameter.PROVINCE_CODE = GetIntHeader("ProvinceCode", ...)
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        if not search_model.SearchParameter.get("PROVINCE_CODE"):
            search_model.SearchParameter["PROVINCE_CODE"] = get_int_header(request, "ProvinceCode")
        total_count, data_list = businesstrade_service.get_businesstrade_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.api_route("/BaseInfo/GetBusinessTradeTree", methods=["GET", "POST"])
async def get_businesstrade_tree(
    request: Request,
    BusinessTrade_PID: int = Query(-1, description="经营业态父级内码"),
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    OwnerUnitId: Optional[int] = Query(None, description="业主单位内码"),
    BusinessTradeState: Optional[int] = Query(None, description="有效状态"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    查询经营业态树
    对应原: [Route("BaseInfo/GetBusinessTradeTree")] GET+POST
    返回嵌套树结构，每个节点含品牌数量
    """
    try:
        # 原 C# L1089: ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        if ProvinceCode is None:
            header_val = request.headers.get("provincecode") or request.headers.get("ProvinceCode")
            if header_val:
                try:
                    ProvinceCode = int(header_val)
                except (ValueError, TypeError):
                    pass

        total_count, tree_list = businesstrade_service.get_businesstrade_tree(
            db,
            business_trade_pid=BusinessTrade_PID,
            province_code=ProvinceCode,
            owner_unit_id=OwnerUnitId,
            business_trade_state=BusinessTradeState
        )

        json_list = JsonListData.create(
            data_list=tree_list,
            total=total_count,
            page_index=1,
            page_size=total_count
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeTree 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.api_route("/BaseInfo/GetBusinessTradeEnum", methods=["GET", "POST"])
async def get_businesstrade_enum(
    request: Request,
    BusinessTrade_PID: int = Query(-1, description="经营业态父级内码"),
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    OwnerUnitId: Optional[int] = Query(None, description="业主单位内码"),
    BusinessTradeState: Optional[int] = Query(None, description="有效状态"),
    SearchKey: str = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    查询经营业态枚举树
    对应原: [Route("BaseInfo/GetBusinessTradeEnum")] GET+POST
    返回 CommonTypeModel 精简树：{node: {label, value, key, type, ico}, children: [...]}
    """
    try:
        # 原 C# L1134: ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        if ProvinceCode is None:
            header_val = request.headers.get("provincecode") or request.headers.get("ProvinceCode")
            if header_val:
                try:
                    ProvinceCode = int(header_val)
                except (ValueError, TypeError):
                    pass

        tree_list = businesstrade_service.get_businesstrade_enum(
            db,
            business_trade_pid=BusinessTrade_PID,
            province_code=ProvinceCode,
            owner_unit_id=OwnerUnitId,
            business_trade_state=BusinessTradeState,
            search_key=SearchKey
        )

        json_list = JsonListData.create(
            data_list=tree_list,
            total=0,
            page_index=1,
            page_size=0
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeEnum 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.api_route("/BaseInfo/GetBusinessTradeDetail", methods=["GET", "POST"])
async def get_businesstrade_detail(
    BusinessTradeId: int = Query(..., description="经营业态内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营业态明细
    对应原: [Route("BaseInfo/GetBusinessTradeDetail")] GET+POST
    """
    try:
        detail = businesstrade_service.get_businesstrade_detail(db, BusinessTradeId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroBusinessTrade")
async def synchro_businesstrade(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步经营业态（新增/更新）
    对应原: [Route("BaseInfo/SynchroBusinessTrade")] POST
    强制 AUTOSTATISTICS_TYPE=2000
    """
    try:
        success = businesstrade_service.synchro_businesstrade(db, data)

        if success:
            return Result.success(msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroBusinessTrade 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BaseInfo/DeleteBusinessTrade", methods=["GET", "POST"])
async def delete_businesstrade(
    BusinessTradeId: int = Query(..., description="经营业态内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除经营业态（软删除，AUTOSTATISTICS_STATE=0）
    对应原: [Route("BaseInfo/DeleteBusinessTrade")] GET+POST
    """
    try:
        success = businesstrade_service.delete_businesstrade(db, BusinessTradeId)

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteBusinessTrade 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
