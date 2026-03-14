from __future__ import annotations
# -*- coding: utf-8 -*-
"""
自定义统计归口表 API 路由
对应原 BaseInfoController.cs 中 AUTOSTATISTICS 相关接口（L1267-1420）

原 C# 接口行为：
- GetAutoStatisticsTreeList: GET+POST, 入参 ProvinceCode(必传)、OwnerUnit_Id(必传)、AutoStatistics_Type、AutoStatistics_PID、AutoStatistics_State
- GetAUTOSTATISTICSDetail: GET+POST, 入参 AUTOSTATISTICSId
- SynchroAUTOSTATISTICS: POST, 入参 AUTOSTATISTICSModel
- DeleteAUTOSTATISTICS: GET+POST, 入参 AUTOSTATISTICSId
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.base_info import autostatistics_service
from routers.deps import get_db, get_int_header

router = APIRouter()


@router.api_route("/BaseInfo/GetAutoStatisticsTreeList", methods=["GET", "POST"])
async def get_autostatistics_tree_list(
    request: Request,
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    OwnerUnit_Id: Optional[int] = Query(None, description="业主内码"),
    AutoStatistics_Type: Optional[int] = Query(None, description="归口类型(1000考核口径/2000经营业态/2010业态考核/3000考核部门/4000供应商类别)"),
    AutoStatistics_PID: int = Query(-1, description="统计归口父级内码"),
    AutoStatistics_State: Optional[int] = Query(None, description="有效状态"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取自定义统计归口树形列表
    对应原: [Route("BaseInfo/GetAutoStatisticsTreeList")] GET+POST
    """
    try:
        total_count, tree_list = autostatistics_service.get_autostatistics_tree_list(
            db,
            autostatistics_pid=AutoStatistics_PID,
            province_code=ProvinceCode,
            ownerunit_id=OwnerUnit_Id,
            autostatistics_type=AutoStatistics_Type,
            autostatistics_state=AutoStatistics_State
        )

        json_list = JsonListData.create(
            data_list=tree_list,
            total=total_count,
            page_index=1,
            page_size=total_count
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAutoStatisticsTreeList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.api_route("/BaseInfo/GetAUTOSTATISTICSDetail", methods=["GET", "POST"])
async def get_autostatistics_detail(
    AUTOSTATISTICSId: int = Query(..., description="自定义归口统计内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取自定义统计归口明细
    对应原: [Route("BaseInfo/GetAUTOSTATISTICSDetail")] GET+POST
    """
    try:
        detail = autostatistics_service.get_autostatistics_detail(db, AUTOSTATISTICSId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAUTOSTATISTICSDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/BaseInfo/SynchroAUTOSTATISTICS")
async def synchro_autostatistics(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """
    同步自定义统计归口表（新增/更新）
    对应原: [Route("BaseInfo/SynchroAUTOSTATISTICS")] POST
    """
    try:
        success = autostatistics_service.synchro_autostatistics(db, data)

        if success:
            return Result.success(msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroAUTOSTATISTICS 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/BaseInfo/DeleteAUTOSTATISTICS", methods=["GET", "POST"])
async def delete_autostatistics(
    AUTOSTATISTICSId: int = Query(..., description="自定义统计归口内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    删除自定义统计归口表（软删除，AUTOSTATISTICS_STATE=0）
    对应原: [Route("BaseInfo/DeleteAUTOSTATISTICS")] GET+POST
    """
    try:
        success = autostatistics_service.delete_autostatistics(db, AUTOSTATISTICSId)

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteAUTOSTATISTICS 删除失败: {ex}")
        return Result.fail(msg="删除失败")
