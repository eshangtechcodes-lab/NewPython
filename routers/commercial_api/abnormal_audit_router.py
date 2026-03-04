# -*- coding: utf-8 -*-
"""
CommercialApi - AbnormalAudit 路由
对应原 CommercialApi/Controllers/AbnormalAuditController.cs
异常稽查相关接口（2个接口，均需AES解密）
"""
from fastapi import APIRouter, Depends
from loguru import logger

from models.base import Result, JsonListData
from core.database import DatabaseHelper
from routers.deps import get_db

router = APIRouter()


@router.post("/AbnormalAudit/GetCurrentEarlyWarning")
async def get_current_early_warning(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    查询当日的异常稽核数据
    入参(AES加密)：ProvinceCode省份编码, ServerpartId服务区内码
    原Helper: EarlyWarningHelper.GetCurrentException（使用Redis缓存）
    """
    try:
        logger.warning("GetCurrentEarlyWarning 暂未完整实现（需AES解密+Redis）")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/AbnormalAudit/GetMonthEarlyWarning")
async def get_month_early_warning(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    查询月度的异常稽核数据
    入参(AES加密)：ProvinceCode省份编码, ServerpartId服务区内码, YearMonth年月(yyyyMM)
    原Helper: EarlyWarningHelper.GetMonthException（使用Redis缓存）
    """
    try:
        logger.warning("GetMonthEarlyWarning 暂未完整实现（需AES解密+Redis）")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")
