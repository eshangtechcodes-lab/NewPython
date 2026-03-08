from __future__ import annotations
# -*- coding: utf-8 -*-
"""
第四批：APPROVED / SHOPEXPENSE / PROJECTSPLITMONTH API 路由
对应原 BusinessProjectController.cs 中相关接口

接口清单（共 10 个）：
- POST  /BusinessProject/GetAPPROVEDList               — APPROVED 列表
- POST  /BusinessProject/GetSHOPEXPENSEList             — SHOPEXPENSE 列表
- GET   /BusinessProject/GetSHOPEXPENSEDetail            — SHOPEXPENSE 明细
- POST  /BusinessProject/SynchroSHOPEXPENSE              — SHOPEXPENSE 同步
- POST  /BusinessProject/DeleteSHOPEXPENSE               — SHOPEXPENSE 软删除
- POST  /BusinessProject/ApproveSHOPEXPENSE              — SHOPEXPENSE 审批
- POST  /BusinessProject/GetPROJECTSPLITMONTHList        — PROJECTSPLITMONTH 列表
- GET   /BusinessProject/GetPROJECTSPLITMONTHDetail      — PROJECTSPLITMONTH 明细
- POST  /BusinessProject/SynchroPROJECTSPLITMONTH        — PROJECTSPLITMONTH 同步
- POST  /BusinessProject/DeletePROJECTSPLITMONTH         — PROJECTSPLITMONTH 软删除
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.business_project import approved_service as ap_svc
from services.business_project import shopexpense_service as se_svc
from services.business_project import projectsplitmonth_service as psm_svc
from routers.deps import get_db

router = APIRouter()


# ==================== APPROVED 审批意见表 ====================

@router.post("/BusinessProject/GetAPPROVEDList")
async def get_approved_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取审批意见列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = ap_svc.get_approved_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAPPROVEDList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ==================== SHOPEXPENSE 门店费用表 ====================

@router.post("/BusinessProject/GetSHOPEXPENSEList")
async def get_shopexpense_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店费用列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = se_svc.get_shopexpense_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSHOPEXPENSEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetSHOPEXPENSEDetail")
async def get_shopexpense_detail(
    SHOPEXPENSEId: int = Query(..., description="门店费用内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店费用明细"""
    try:
        detail = se_svc.get_shopexpense_detail(db, SHOPEXPENSEId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSHOPEXPENSEDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroSHOPEXPENSE")
async def synchro_shopexpense(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步门店费用（新增/更新，简化版不含级联逻辑）"""
    try:
        success, result_data = se_svc.synchro_shopexpense(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroSHOPEXPENSE 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteSHOPEXPENSE", methods=["GET", "POST"])
async def delete_shopexpense(
    SHOPEXPENSEId: int = Query(..., description="门店费用内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除门店费用（简化版软删除）"""
    try:
        success = se_svc.delete_shopexpense(db, SHOPEXPENSEId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteSHOPEXPENSE 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


@router.post("/BusinessProject/ApproveSHOPEXPENSE")
async def approve_shopexpense(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """审批门店费用（实际调用 Synchro 带 ApprovalProcess=true）"""
    try:
        success, result_data = se_svc.approve_shopexpense(db, data)
        if success:
            return Result.success(data=result_data, msg="审批成功")
        else:
            return Result(Result_Code=200, Result_Desc="审批失败！")
    except Exception as ex:
        logger.error(f"ApproveSHOPEXPENSE 审批失败: {ex}")
        return Result.fail(msg=f"审批失败{ex}")


# ==================== PROJECTSPLITMONTH 月度经营项目应收拆分汇总表 ====================

@router.post("/BusinessProject/GetPROJECTSPLITMONTHList")
async def get_projectsplitmonth_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营项目应收拆分汇总表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}

        total_count, data_list = psm_svc.get_projectsplitmonth_list(db, search_model)

        json_list = JsonListData.create(
            data_list=data_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROJECTSPLITMONTHList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetPROJECTSPLITMONTHDetail")
async def get_projectsplitmonth_detail(
    PROJECTSPLITMONTHId: int = Query(..., description="月度拆分汇总表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营项目应收拆分汇总表明细"""
    try:
        detail = psm_svc.get_projectsplitmonth_detail(db, PROJECTSPLITMONTHId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPROJECTSPLITMONTHDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroPROJECTSPLITMONTH")
async def synchro_projectsplitmonth(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步月度经营项目应收拆分汇总表（新增/更新）"""
    try:
        success, result_data = psm_svc.synchro_projectsplitmonth(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroPROJECTSPLITMONTH 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeletePROJECTSPLITMONTH", methods=["GET", "POST"])
async def delete_projectsplitmonth(
    PROJECTSPLITMONTHId: int = Query(..., description="月度拆分汇总表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除月度经营项目应收拆分汇总表（软删除）"""
    try:
        success = psm_svc.delete_projectsplitmonth(db, PROJECTSPLITMONTHId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeletePROJECTSPLITMONTH 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
