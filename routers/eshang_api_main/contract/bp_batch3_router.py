from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营项目执行情况 / 经营项目应收拆分 / 月度拆分 / 项目预警 / 周期预警 API 路由
对应原 BusinessProjectController.cs 中相关接口
路由路径与原 Controller 完全一致

接口清单（第一批 - BUSINESSPAYMENT 4个）：
- POST  /BusinessProject/GetBusinessPaymentList       — 列表查询
- GET   /BusinessProject/GetBusinessPaymentDetail      — 明细查询
- POST  /BusinessProject/SynchroBusinessPayment        — 同步（新增/更新）
- POST  /BusinessProject/DeleteBusinessPayment         — 软删除
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.business_project import businesspayment_service as bp_svc
from services.business_project import projectwarning_service as pw_svc
from services.business_project import periodwarning_service as pdw_svc
from services.business_project import bizpsplitmonth_service as bsm_svc
from services.business_project import businessprojectsplit_service as bps_svc
from routers.deps import get_db

router = APIRouter()


# ==================== BUSINESSPAYMENT 经营项目执行情况表 ====================

@router.post("/BusinessProject/GetBusinessPaymentList")
async def get_businesspayment_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目执行情况表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = bp_svc.get_businesspayment_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessPaymentList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetBusinessPaymentDetail")
async def get_businesspayment_detail(
    BusinessPaymentId: int = Query(..., description="经营项目执行情况表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目执行情况表明细"""
    try:
        detail = bp_svc.get_businesspayment_detail(db, BusinessPaymentId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessPaymentDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroBusinessPayment")
async def synchro_businesspayment(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步经营项目执行情况表（新增/更新）"""
    try:
        success, result_data = bp_svc.synchro_businesspayment(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroBusinessPayment 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteBusinessPayment", methods=["GET", "POST"])
async def delete_businesspayment(
    BusinessPaymentId: int = Query(..., description="经营项目执行情况表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除经营项目执行情况表（软删除）"""
    try:
        success = bp_svc.delete_businesspayment(db, BusinessPaymentId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteBusinessPayment 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ==================== PROJECTWARNING 经营项目预警表 ====================

@router.post("/BusinessProject/GetPROJECTWARNINGList")
async def get_projectwarning_list(
    search_model: Optional[SearchModel] = None,
    ModuleGuid: str = Query("", description="用户审批权限GUID"),
    SourcePlatform: str = Query("", description="操作平台"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目预警表列表（含 DealMark 审批待办标记）"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total_count, data_list = pw_svc.get_projectwarning_list(
            db, search_model, ModuleGuid, SourcePlatform)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                        page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROJECTWARNINGList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetPROJECTWARNINGDetail")
async def get_projectwarning_detail(
    PROJECTWARNINGId: int = Query(..., description="经营项目预警表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目预警表明细"""
    try:
        detail = pw_svc.get_projectwarning_detail(db, PROJECTWARNINGId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROJECTWARNINGDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroPROJECTWARNING")
async def synchro_projectwarning(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步经营项目预警表（新增/更新）"""
    try:
        success, result_data = pw_svc.synchro_projectwarning(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroPROJECTWARNING 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeletePROJECTWARNING", methods=["GET", "POST"])
async def delete_projectwarning(
    PROJECTWARNINGId: int = Query(..., description="经营项目预警表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除经营项目预警表（软删除）"""
    try:
        success = pw_svc.delete_projectwarning(db, PROJECTWARNINGId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeletePROJECTWARNING 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ==================== PERIODWARNING 经营项目周期预警表 ====================

@router.post("/BusinessProject/GetPERIODWARNINGList")
async def get_periodwarning_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目周期预警表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total_count, data_list = pdw_svc.get_periodwarning_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                        page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPERIODWARNINGList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetPERIODWARNINGDetail")
async def get_periodwarning_detail(
    PERIODWARNINGId: int = Query(..., description="经营项目周期预警表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目周期预警表明细"""
    try:
        detail = pdw_svc.get_periodwarning_detail(db, PERIODWARNINGId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPERIODWARNINGDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroPERIODWARNING")
async def synchro_periodwarning(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步经营项目周期预警表（新增/更新）"""
    try:
        success, result_data = pdw_svc.synchro_periodwarning(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroPERIODWARNING 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeletePERIODWARNING", methods=["GET", "POST"])
async def delete_periodwarning(
    PERIODWARNINGId: int = Query(..., description="经营项目周期预警表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除经营项目周期预警表（原 C# 方法体为空，始终返回失败）"""
    try:
        success = pdw_svc.delete_periodwarning(db, PERIODWARNINGId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeletePERIODWARNING 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ==================== BIZPSPLITMONTH 月度经营项目应收拆分表 ====================

@router.post("/BusinessProject/GetBIZPSPLITMONTHList")
async def get_bizpsplitmonth_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营项目应收拆分表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total_count, data_list = bsm_svc.get_bizpsplitmonth_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                        page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBIZPSPLITMONTHList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetBIZPSPLITMONTHDetail")
async def get_bizpsplitmonth_detail(
    BIZPSPLITMONTHId: int = Query(..., description="月度拆分表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营项目应收拆分表明细"""
    try:
        detail = bsm_svc.get_bizpsplitmonth_detail(db, BIZPSPLITMONTHId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBIZPSPLITMONTHDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroBIZPSPLITMONTH")
async def synchro_bizpsplitmonth(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步月度经营项目应收拆分表（新增/更新）"""
    try:
        success, result_data = bsm_svc.synchro_bizpsplitmonth(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroBIZPSPLITMONTH 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteBIZPSPLITMONTH", methods=["GET", "POST"])
async def delete_bizpsplitmonth(
    BIZPSPLITMONTHId: int = Query(..., description="月度拆分表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除月度经营项目应收拆分表（软删除）"""
    try:
        success = bsm_svc.delete_bizpsplitmonth(db, BIZPSPLITMONTHId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteBIZPSPLITMONTH 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ==================== BUSINESSPROJECTSPLIT 经营项目应收拆分表 ====================

@router.post("/BusinessProject/GetBUSINESSPROJECTSPLITList")
async def get_businessprojectsplit_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目应收拆分表列表（简化版）"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total_count, data_list = bps_svc.get_businessprojectsplit_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total_count,
                                        page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBUSINESSPROJECTSPLITList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetBUSINESSPROJECTSPLITDetail")
async def get_businessprojectsplit_detail(
    BUSINESSPROJECTSPLITId: int = Query(..., description="经营项目应收拆分表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目应收拆分表明细"""
    try:
        detail = bps_svc.get_businessprojectsplit_detail(db, BUSINESSPROJECTSPLITId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBUSINESSPROJECTSPLITDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroBUSINESSPROJECTSPLIT")
async def synchro_businessprojectsplit(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步经营项目应收拆分表（新增/更新）"""
    try:
        success, result_data = bps_svc.synchro_businessprojectsplit(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroBUSINESSPROJECTSPLIT 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteBUSINESSPROJECTSPLIT", methods=["GET", "POST"])
async def delete_businessprojectsplit(
    BUSINESSPROJECTSPLITId: int = Query(..., description="经营项目应收拆分表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除经营项目应收拆分表（软删除）"""
    try:
        success = bps_svc.delete_businessprojectsplit(db, BUSINESSPROJECTSPLITId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteBUSINESSPROJECTSPLIT 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
