# -*- coding: utf-8 -*-
"""
CommercialApi - Suggestion 路由
对应原 CommercialApi/Controllers/SuggestionController.cs
投诉建议相关接口（2个接口）
"""
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result
from routers.deps import get_db

router = APIRouter()


@router.get("/Suggestion/GetMemberUnreadData")
async def get_member_unread_data(
    ModuleGuids: str = Query(..., description="用户投诉建议模块权限，多个用逗号隔开"),
    ProvinceCode: str = Query(..., description="省份编码"),
    MembershipId: int = Query(..., description="会员内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取用户投诉建议浏览日志
    原Helper: SuggestionHelper.GetMemberUnreadData
    """
    try:
        logger.warning("GetMemberUnreadData 暂未完整实现")
        return Result.success(data={}, msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.api_route("/Suggestion/RecordReadingLog", methods=["GET", "POST"])
async def record_reading_log(
    MemberShipId: int = Query(..., description="会员内码"),
    SuggestionIds: str = Query(..., description="投诉建议内码，多个用逗号隔开"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    记录用户浏览投诉建议的日志
    返参：name记录名称 value已读待处理记录内码 key未读待处理记录内码 data未读数量
    """
    try:
        logger.warning("RecordReadingLog 暂未完整实现")
        return Result.success(msg="记录成功")
    except Exception as ex:
        return Result.fail(msg=f"记录失败{ex}")
