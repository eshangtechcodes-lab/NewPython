# -*- coding: utf-8 -*-
"""
ShopVideoController 路由（16 个接口）
严格按照 C# ShopVideoController.cs 迁移

CRUD 实体:
  EXTRANET (4) / EXTRANETDETAIL (4) / SHOPVIDEO (4)
VIDEOLOG:
  GetVIDEOLOGList (1) / SynchroVIDEOLOG (1)
聚合接口:
  GetShopVideoInfo (1) / GetYSShopVideoInfo (1)
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger
from routers.deps import get_db
from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.video import video_service

router = APIRouter()


# ============================================================
# 通用 CRUD 路由工厂（与 bigdata_router 一致）
# ============================================================
def _make_list_route(entity_name: str, route_path: str):
    """生成 GetXXXList 路由（POST）"""
    @router.post(route_path)
    async def _list(search_model: Optional[SearchModel] = None,
                    db: DatabaseHelper = Depends(get_db)):
        try:
            if search_model is None:
                search_model = SearchModel()
            if search_model.SearchParameter is None:
                search_model.SearchParameter = {}
            sm = search_model.model_dump()
            rows, total = video_service.get_entity_list(db, entity_name, sm)
            json_list = JsonListData.create(
                data_list=rows, total=total,
                page_index=search_model.PageIndex,
                page_size=search_model.PageSize)
            return Result.success(data=json_list.model_dump(), msg="查询成功")
        except Exception as ex:
            logger.error(f"Get{entity_name}List 查询失败: {ex}")
            return Result.fail(msg="查询失败")
    _list.__name__ = f"get_{entity_name.lower()}_list"
    return _list

def _make_detail_route(entity_name: str, route_path: str, param_name: str):
    """生成 GetXXXDetail 路由（GET）"""
    @router.get(route_path)
    async def _detail(pk_val: int = Query(..., alias=param_name),
                      db: DatabaseHelper = Depends(get_db)):
        try:
            detail = video_service.get_entity_detail(db, entity_name, pk_val)
            return Result.success(data=detail, msg="查询成功")
        except Exception as ex:
            logger.error(f"Get{entity_name}Detail 查询失败: {ex}")
            return Result.fail(msg="查询失败")
    _detail.__name__ = f"get_{entity_name.lower()}_detail"
    return _detail

def _make_synchro_route(entity_name: str, route_path: str):
    """生成 SynchroXXX 路由（POST）"""
    @router.post(route_path)
    async def _synchro(data: dict, db: DatabaseHelper = Depends(get_db)):
        try:
            ok, result = video_service.synchro_entity(db, entity_name, data)
            if ok:
                return Result.success(data=result, msg="同步成功")
            else:
                return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
        except Exception as ex:
            logger.error(f"Synchro{entity_name} 同步失败: {ex}")
            return Result.fail(msg="同步失败")
    _synchro.__name__ = f"synchro_{entity_name.lower()}"
    return _synchro

def _make_delete_route(entity_name: str, route_path: str, param_name: str):
    """生成 DeleteXXX 路由（GET+POST，与 C# [AcceptVerbs("GET","POST")] 一致）"""
    @router.api_route(route_path, methods=["GET", "POST"])
    async def _delete(pk_val: int = Query(..., alias=param_name),
                      db: DatabaseHelper = Depends(get_db)):
        try:
            ok = video_service.delete_entity(db, entity_name, pk_val)
            if ok:
                return Result.success(msg="删除成功")
            else:
                return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
        except Exception as ex:
            logger.error(f"Delete{entity_name} 删除失败: {ex}")
            return Result.fail(msg="删除失败")
    _delete.__name__ = f"delete_{entity_name.lower()}"
    return _delete


# ============================================================
# VI-01: EXTRANET — 服务区监控信息主表（C# ShopVideoController L18-159）
# ============================================================
_make_list_route("EXTRANET", "/ShopVideo/GetEXTRANETList")
_make_detail_route("EXTRANET", "/ShopVideo/GetEXTRANETDetail", "EXTRANETId")
_make_synchro_route("EXTRANET", "/ShopVideo/SynchroEXTRANET")
_make_delete_route("EXTRANET", "/ShopVideo/DeleteEXTRANET", "EXTRANETId")

# ============================================================
# VI-02: EXTRANETDETAIL — 服务区监控录像信息表（C# ShopVideoController L161-303）
# ============================================================
_make_list_route("EXTRANETDETAIL", "/ShopVideo/GetEXTRANETDETAILList")
_make_detail_route("EXTRANETDETAIL", "/ShopVideo/GetEXTRANETDETAILDetail", "EXTRANETDETAILId")
_make_synchro_route("EXTRANETDETAIL", "/ShopVideo/SynchroEXTRANETDETAIL")
_make_delete_route("EXTRANETDETAIL", "/ShopVideo/DeleteEXTRANETDETAIL", "EXTRANETDETAILId")

# ============================================================
# VI-03: SHOPVIDEO — 门店视频监控表（C# ShopVideoController L305-446）
# ============================================================
_make_list_route("SHOPVIDEO", "/ShopVideo/GetSHOPVIDEOList")
_make_detail_route("SHOPVIDEO", "/ShopVideo/GetSHOPVIDEODetail", "SHOPVIDEOId")
_make_synchro_route("SHOPVIDEO", "/ShopVideo/SynchroSHOPVIDEO")
_make_delete_route("SHOPVIDEO", "/ShopVideo/DeleteSHOPVIDEO", "SHOPVIDEOId")


# ============================================================
# VI-04: VIDEOLOG — 异常稽核查看日志表
# GetVIDEOLOGList（POST，含 Search_Type 多分支）
# SynchroVIDEOLOG（POST，纯 INSERT）
# ============================================================
@router.post("/ShopVideo/GetVIDEOLOGList")
async def get_videolog_list(search_model: Optional[SearchModel] = None,
                            db: DatabaseHelper = Depends(get_db)):
    """获取异常稽核查看日志表列表 — C# VIDEOLOGHelper.GetVIDEOLOGList"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        sm = search_model.model_dump()
        rows, total = video_service.get_videolog_list(db, sm)
        json_list = JsonListData.create(
            data_list=rows, total=total,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetVIDEOLOGList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/ShopVideo/SynchroVIDEOLOG")
async def synchro_videolog(data: dict, db: DatabaseHelper = Depends(get_db)):
    """记录异常稽核查看日志 — C# VIDEOLOGHelper.SynchroVIDEOLOG（纯 INSERT）"""
    try:
        ok = video_service.synchro_videolog(db, data)
        if ok:
            return Result.success(msg="同步成功")
        else:
            return Result.fail(msg="同步失败")
    except Exception as ex:
        logger.error(f"SynchroVIDEOLOG 同步失败: {ex}")
        return Result.fail(msg="同步失败")


# ============================================================
# VI-05: 聚合接口 — GetShopVideoInfo / GetYSShopVideoInfo
# C# ShopVideoController L448-632
# ============================================================
@router.api_route("/ShopVideo/GetShopVideoInfo", methods=["GET", "POST"])
async def get_shop_video_info(
        JsonString: str = "", ServerpartCode: str = "",
        ServerpartShopCode: str = "", MachineCode: str = "",
        AbnormalityCode: str = "",
        CheckEndaccount_ID: Optional[int] = None,
        AbnormalAudit_ID: Optional[int] = None,
        Endaccount_ID: Optional[int] = None,
        db: DatabaseHelper = Depends(get_db)):
    """获取门店异常稽核视频信息 — C# ShopVideoHelper.GetShopVideoInfo"""
    try:
        result = video_service.get_shop_video_info(
            db, ServerpartCode, ServerpartShopCode, MachineCode,
            AbnormalityCode, CheckEndaccount_ID, AbnormalAudit_ID,
            Endaccount_ID, use_ys_table=False)
        if result:
            return Result.success(data=result, msg="查询成功")
        else:
            return Result.success(data=None, msg="未查询到视频信息")
    except Exception as ex:
        logger.error(f"GetShopVideoInfo 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.api_route("/ShopVideo/GetYSShopVideoInfo", methods=["GET", "POST"])
async def get_ys_shop_video_info(
        JsonString: str = "", ServerpartCode: str = "",
        ServerpartShopCode: str = "", MachineCode: str = "",
        AbnormalityCode: str = "",
        CheckEndaccount_ID: Optional[int] = None,
        AbnormalAudit_ID: Optional[int] = None,
        Endaccount_ID: Optional[int] = None,
        db: DatabaseHelper = Depends(get_db)):
    """获取门店视频信息（萤石云新表）— C# ShopVideoHelper.GetYSShopVideoInfo"""
    try:
        result = video_service.get_shop_video_info(
            db, ServerpartCode, ServerpartShopCode, MachineCode,
            AbnormalityCode, CheckEndaccount_ID, AbnormalAudit_ID,
            Endaccount_ID, use_ys_table=True)
        if result:
            return Result.success(data=result, msg="查询成功")
        else:
            return Result.success(data=None, msg="未查询到视频信息")
    except Exception as ex:
        logger.error(f"GetYSShopVideoInfo 查询失败: {ex}")
        return Result.fail(msg="查询失败")
