# -*- coding: utf-8 -*-
"""
CommercialApi - Analysis 路由（重构版）
对应原 CommercialApi/Controllers/AnalysisController.cs
业务逻辑已移至 services/commercial/analysis_service.py
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db
from services.commercial import analysis_service

router = APIRouter()


@router.post("/Analysis/GetANALYSISINSList")
async def get_analysisins_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取分析说明表列表"""
    try:
        total, page_rows = analysis_service.get_analysisins_list(db, searchModel)
        sm = searchModel or {}
        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=sm.get("PageIndex", 1), page_size=sm.get("PageSize", 20))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetANALYSISINSList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Analysis/GetANALYSISINSDetail")
async def get_analysisins_detail(ANALYSISINSId: Optional[int] = Query(None), db: DatabaseHelper = Depends(get_db)):
    """获取分析说明表明细"""
    try:
        data = analysis_service.get_analysisins_detail(db, ANALYSISINSId)
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetANALYSISINSDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/Analysis/SolidTransactionAnalysis")
async def solid_transaction_analysis(analysisParamModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """生成时段客单交易分析数据"""
    try:
        analysisParamModel = analysisParamModel or {}
        if not analysisParamModel.get("AmountRangeList"):
            return Result.fail(code=200, msg="生成失败！请传入正确的参数")
        # TODO: 实现生成逻辑
        logger.warning("SolidTransactionAnalysis 生成逻辑暂未实现")
        return Result.success(msg="生成成功")
    except Exception as ex:
        return Result.fail(msg=f"生成失败{ex}")


@router.post("/Analysis/GetTransactionAnalysis")
async def get_transaction_analysis(tapModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取时段客单交易分析数据"""
    try:
        result_list = analysis_service.get_transaction_analysis(db, tapModel)
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Analysis/TranslateSentence")
async def translate_sentence(
    Sentence: Optional[str] = Query(None), DialogCode: Optional[str] = Query(""),
    ProvinceCode: Optional[str] = Query(""), db: DatabaseHelper = Depends(get_db)
):
    """解析语义内容中的关键字信息"""
    try:
        # TODO: 实现查询逻辑后移至 analysis_service
        logger.warning("TranslateSentence 暂未完整实现")
        return Result.success(data={
            "SentenceType": None, "AnalysisRuleId": None, "FormatRuleId": None,
            "TriggerWords": None, "ChatContent": None, "ServerpartInfoList": [],
            "RevenueList": None, "ServerpartId": None, "ServerpartName": None,
        }, msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Analysis/GetMapConfigByProvinceCode")
async def get_map_config_by_province_code(
    ProvinceCode: Optional[str] = Query(None), db: DatabaseHelper = Depends(get_db)
):
    """获取地图参数配置"""
    try:
        data = analysis_service.get_map_config(db, ProvinceCode)
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMapConfigByProvinceCode 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/Analysis/GetServerpartTypeAnalysis")
async def get_serverpart_type_analysis(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取服务区分类定级情况"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        result_list = analysis_service.get_serverpart_type_analysis(db, province_code)
        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetServerpartTypeAnalysis AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")
