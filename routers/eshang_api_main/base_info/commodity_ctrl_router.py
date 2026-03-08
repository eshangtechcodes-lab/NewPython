from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商品管理 API 路由（CommodityController 专属）
路由前缀：/Commodity/
对应 C# CommodityController.cs 中 6 个非加密接口

与 BaseInfo 下的 commodity_router.py（/BaseInfo/GetCOMMODITYList 等）不同！
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Header, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.base_info import commodity_ctrl_service
from routers.deps import get_db

router = APIRouter()


# ========== 1. GetCOMMODITYList ==========
@router.post("/Commodity/GetCOMMODITYList")
async def get_commodity_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取商品管理列表
    C# 参数：SearchModel<COMMODITYSearchModel> + Header(ServerpartCodes, ProvinceCode)
    """
    try:
        if search_model is None:
            search_model = SearchModel()
        sp = search_model.SearchParameter or {}

        # Header: ServerpartCodes -> SERVERPART_IDS（如果 SearchParameter 中没有传）
        if not sp.get("SERVERPART_IDS"):
            serverpart_codes = request.headers.get("ServerpartCodes", "")
            if serverpart_codes:
                try:
                    codes_in = ",".join([f"'{c.strip()}'" for c in serverpart_codes.split(",") if c.strip()])
                    ids_sql = f"SELECT SERVERPART_ID FROM T_SERVERPART WHERE SERVERPART_CODE IN ({codes_in})"
                    id_rows = db.execute_query(ids_sql)
                    if id_rows:
                        sp["SERVERPART_IDS"] = ",".join([str(r["SERVERPART_ID"]) for r in id_rows])
                except Exception as e:
                    logger.warning(f"ServerpartCodes 转 IDS 失败: {e}")

        # Header: ProvinceCode
        province_code = request.headers.get("ProvinceCode", "")

        # keyWord
        kw = None
        if search_model.keyWord:
            kw = search_model.keyWord.model_dump() if hasattr(search_model.keyWord, 'model_dump') else search_model.keyWord

        total_count, data_list = commodity_ctrl_service.get_commodity_list(
            db, sp, province_code, "", "",
            keyword=kw,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize,
            sort_str=search_model.SortStr or ""
        )
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Commodity/GetCOMMODITYList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ========== 2. GetCOMMODITYDetail ==========
@router.get("/Commodity/GetCOMMODITYDetail")
async def get_commodity_detail(
    COMMODITYId: int = Query(..., description="商品管理内码"),
    ProvinceCode: str = Header("", description="省份标识"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品管理明细"""
    try:
        detail = commodity_ctrl_service.get_commodity_detail(db, COMMODITYId, ProvinceCode)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"Commodity/GetCOMMODITYDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ========== 3. SynchroCOMMODITY ==========
@router.post("/Commodity/SynchroCOMMODITY")
async def synchro_commodity(
    data: dict,
    ProvinceCode: str = Header("", description="省份标识"),
    db: DatabaseHelper = Depends(get_db)
):
    """同步商品管理（新增/更新）"""
    try:
        success, result_data = commodity_ctrl_service.synchro_commodity(db, data, ProvinceCode)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Commodity/SynchroCOMMODITY 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


# ========== 4. DeleteCOMMODITY ==========
@router.api_route("/Commodity/DeleteCOMMODITY", methods=["GET", "POST"])
async def delete_commodity(
    COMMODITYId: int = Query(..., description="商品管理内码"),
    ProvinceCode: str = Header("", description="省份标识"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除商品管理（软删除 COMMODITY_STATE=0）"""
    try:
        success = commodity_ctrl_service.delete_commodity(db, COMMODITYId, ProvinceCode)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Commodity/DeleteCOMMODITY 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ========== 5. GetCommodityList (SearchType switch) ==========
@router.get("/Commodity/GetCommodityList")
async def get_commodity_list_by_type(
    SearchType: int = Query(..., description="查询类型(0=商品库/1=标准信息/2=标价签/其他=全字段)"),
    ProvinceCode: int = Query(None, description="省份编码"),
    SPRegionTypeID: str = Query("", description="片区内码"),
    ServerpartID: str = Query("", description="服务区内码"),
    ServerpartShopID: str = Query("", description="门店内码"),
    ShopTrade: str = Query("", description="商品业态"),
    CommodityTypeId: str = Query("", description="商品类型内码"),
    CommodityState: str = Query("", description="商品状态"),
    UserDefinedTypeId: str = Query("", description="商品自定义类"),
    ShowJustUDType: bool = Query(None, description="是否只显示有归类的商品"),
    OperateDate_Start: str = Query("", description="审核时间开始"),
    OperateDate_End: str = Query("", description="审核时间结束"),
    SearchKey: str = Query("", description="模糊查询字段"),
    SearchValue: str = Query("", description="模糊查询内容"),
    PageIndex: int = Query(1, description="页码"),
    PageSize: int = Query(10, description="每页行数"),
    SortStr: str = Query("", description="排序字段"),
    request: Request = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取商品信息列表（多种 SearchType 分支）"""
    try:
        # C# 从 Header 获取 ProvinceCode
        if ProvinceCode is None:
            header_pc = request.headers.get("ProvinceCode", "") if request else ""
            if header_pc:
                try:
                    ProvinceCode = int(header_pc)
                except:
                    pass

        if ProvinceCode is None:
            return Result(Result_Code=200, Result_Desc="查询失败，请传入商品表省份标识！")

        # C# 从 Header 获取 ServerpartCodes -> ServerpartID
        if not ServerpartID and request:
            serverpart_codes = request.headers.get("ServerpartCodes", "")
            if serverpart_codes:
                try:
                    codes_in = ",".join([f"'{c.strip()}'" for c in serverpart_codes.split(",") if c.strip()])
                    ids_sql = f"SELECT SERVERPART_ID FROM T_SERVERPART WHERE SERVERPART_CODE IN ({codes_in})"
                    id_rows = db.execute_query(ids_sql)
                    if id_rows:
                        ServerpartID = ",".join([str(r["SERVERPART_ID"]) for r in id_rows])
                except Exception as e:
                    logger.warning(f"ServerpartCodes 转 IDS 失败: {e}")

        total_count, data_list = commodity_ctrl_service.get_commodity_list_by_type(
            db, SearchType, ProvinceCode,
            SPRegionTypeID, ServerpartID, ServerpartShopID, ShopTrade,
            CommodityTypeId, CommodityState,
            UserDefinedTypeId, ShowJustUDType,
            OperateDate_Start, OperateDate_End,
            SearchKey, SearchValue,
            PageIndex, PageSize, SortStr
        )

        if total_count == -1:
            return Result(Result_Code=200, Result_Desc="查询失败，请传入商品表省份标识！")

        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                         page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Commodity/GetCommodityList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ========== 6. SyncCommodityInfo_AHJG ==========
@router.get("/Commodity/SyncCommodityInfo_AHJG")
async def sync_commodity_info_ahjg(
    LastTime: str = Query(..., description="上次更新时间"),
    db: DatabaseHelper = Depends(get_db)
):
    """更新安徽建工待审核商品数据"""
    try:
        commodity_ctrl_service.sync_commodity_info_ahjg(db, LastTime)
        return Result.success(msg="同步完成")
    except Exception as ex:
        logger.error(f"SyncCommodityInfo_AHJG 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")
