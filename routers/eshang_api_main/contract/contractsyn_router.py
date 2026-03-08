from __future__ import annotations
# -*- coding: utf-8 -*-
"""
合同信息同步表 API 路由
对应原 ContractSynController（ContractSyn/前缀 4个）
     + CONTRACT_SYNController（BusinessProject/前缀 4个）
两个 Controller 共用同一张表 T_CONTRACTSYN
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.contract import contractsyn_service
from routers.deps import get_db

router = APIRouter()


# =====================================================
# ContractSynController（ContractSyn/前缀）
# =====================================================

@router.post("/ContractSyn/GetContractSynList")
async def get_contractsyn_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同信息同步表列表 - ContractSyn/前缀"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total, data_list = contractsyn_service.get_contractsyn_list(db, search_model)
        json_list = JsonListData.create(
            data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetContractSynList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/ContractSyn/GetContractSynDetail")
async def get_contractsyn_detail(
    ContractSynId: int = Query(..., description="合同信息同步表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同信息同步表明细 - ContractSyn/前缀"""
    try:
        detail = contractsyn_service.get_contractsyn_detail(db, ContractSynId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetContractSynDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/ContractSyn/SynchroContractSyn")
async def synchro_contractsyn(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步合同信息同步表 - ContractSyn/前缀"""
    try:
        success, result_data = contractsyn_service.synchro_contractsyn(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroContractSyn 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/ContractSyn/DeleteContractSyn", methods=["GET", "POST"])
async def delete_contractsyn(
    ContractSynId: int = Query(..., description="合同信息同步表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除合同信息同步表 - ContractSyn/前缀"""
    try:
        success = contractsyn_service.delete_contractsyn(db, ContractSynId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteContractSyn 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# =====================================================
# CONTRACT_SYNController（BusinessProject/前缀）
# 同一张表 T_CONTRACTSYN，不同路由前缀
# =====================================================

@router.post("/BusinessProject/GetCONTRACT_SYNList")
async def get_contract_syn_list_bp(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同信息同步表列表 - BusinessProject/前缀"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total, data_list = contractsyn_service.get_contractsyn_list(db, search_model)
        json_list = JsonListData.create(
            data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCONTRACT_SYNList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetCONTRACT_SYNDetail")
async def get_contract_syn_detail_bp(
    CONTRACT_SYNId: int = Query(..., description="合同信息同步表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同信息同步表明细 - BusinessProject/前缀"""
    try:
        detail = contractsyn_service.get_contractsyn_detail(db, CONTRACT_SYNId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCONTRACT_SYNDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroCONTRACT_SYN")
async def synchro_contract_syn_bp(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步合同信息同步表 - BusinessProject/前缀"""
    try:
        success, result_data = contractsyn_service.synchro_contractsyn(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroCONTRACT_SYN 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteCONTRACT_SYN", methods=["GET", "POST"])
async def delete_contract_syn_bp(
    CONTRACT_SYNId: int = Query(..., description="合同信息同步表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除合同信息同步表 - BusinessProject/前缀"""
    try:
        success = contractsyn_service.delete_contractsyn(db, CONTRACT_SYNId)
        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteCONTRACT_SYN 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
