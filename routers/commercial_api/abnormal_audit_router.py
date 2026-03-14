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
from core.aes_util import decrypt_post_data
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
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        logger.info(f"GetCurrentEarlyWarning 解密参数: ProvinceCode={province_code}, ServerpartId={serverpart_id}")

        if not province_code:
            return Result.fail(code=205, msg="查询失败,请传入省份编码！")

        # TODO: 实现查询逻辑（需要 Redis 缓存支持）
        logger.warning("GetCurrentEarlyWarning 查询逻辑暂未实现（需Redis）")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetCurrentEarlyWarning AES解密失败: {ve}")
        return Result.fail(msg="解密失败")
    except Exception as ex:
        return Result.fail(msg="查询失败")


@router.post("/AbnormalAudit/GetMonthEarlyWarning")
async def get_month_early_warning(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    查询月度的异常稽核数据
    入参(AES加密)：ProvinceCode省份编码, ServerpartId服务区内码, YearMonth年月(yyyyMM)
    原Helper: EarlyWarningHelper.GetMonthException（使用Redis缓存）
    """
    try:
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        year_month = params.get("YearMonth", "")
        logger.info(f"GetMonthEarlyWarning 解密参数: ProvinceCode={province_code}, ServerpartId={serverpart_id}, YearMonth={year_month}")

        if not province_code:
            return Result.fail(code=205, msg="查询失败,请传入省份编码！")

        # TODO: 实现查询逻辑（需要 Redis 缓存支持）
        logger.warning("GetMonthEarlyWarning 查询逻辑暂未实现（需Redis）")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetMonthEarlyWarning AES解密失败: {ve}")
        return Result.fail(msg="解密失败")
    except Exception as ex:
        return Result.fail(msg="查询失败")
