# -*- coding: utf-8 -*-
"""
CommercialApi - BusinessProcess 路由
对应原 CommercialApi/Controllers/BusinessProcessController.cs
业务审批相关接口（1个接口）
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


@router.get("/BusinessProcess/GetBusinessProcessList")
async def get_business_process_list(
    MembershipId: Optional[int] = Query(None, description="会员内码"),
    OperationType: Optional[str] = Query(None, description="业务类型"),
    BusinessProcessState: Optional[str] = Query("", description="流程状态"),
    StartDate: Optional[str] = Query("", description="查询开始时间"),
    EndDate: Optional[str] = Query("", description="查询结束时间"),
    ModuleGuid: Optional[str] = Query("", description="模块权限"),
    PageIndex: int = Query(1, description="查询页码数"),
    PageSize: int = Query(10, description="每页显示行数"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取业务审批列表
    原Helper: BusinessProcessHelper.GetBusinessProcessList
    """
    try:
        logger.warning("GetBusinessProcessList 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0, page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg="查询失败")
