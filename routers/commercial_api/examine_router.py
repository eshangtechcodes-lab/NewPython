# -*- coding: utf-8 -*-
"""
CommercialApi - Examine 路由（重构版）
对应原 CommercialApi/Controllers/ExamineController.cs
业务逻辑已移至 services/commercial/examine_service.py
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db
from services.commercial import examine_service

router = APIRouter()


@router.post("/Examine/GetEXAMINEList")
async def get_examine_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取考核管理表列表"""
    try:
        sm = searchModel or {}
        total, rows = examine_service.get_examine_list(db, sm)
        json_list = JsonListData.create(data_list=rows, total=total,
            page_index=sm.get("PageIndex", 1), page_size=sm.get("PageSize", 20))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXAMINEList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetEXAMINEDetail")
async def get_examine_detail(EXAMINEId: Optional[int] = Query(None), db: DatabaseHelper = Depends(get_db)):
    """获取考核管理表明细"""
    try:
        data = examine_service.get_examine_detail(db, EXAMINEId)
        if data is None: return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXAMINEDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Examine/GetMEETINGList")
async def get_meeting_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取晨会管理表列表"""
    try:
        sm = searchModel or {}
        total, rows = examine_service.get_meeting_list(db, sm)
        json_list = JsonListData.create(data_list=rows, total=total,
            page_index=sm.get("PageIndex", 1), page_size=sm.get("PageSize", 20))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMEETINGList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetMEETINGDetail")
async def get_meeting_detail(MEETINGId: Optional[int] = Query(None), db: DatabaseHelper = Depends(get_db)):
    """获取晨会管理表明细"""
    try:
        data = examine_service.get_meeting_detail(db, MEETINGId)
        if data is None: return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMEETINGDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Examine/GetPATROLList")
async def get_patrol_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取日常巡检表列表"""
    try:
        sm = searchModel or {}
        total, rows = examine_service.get_patrol_list(db, sm)
        json_list = JsonListData.create(data_list=rows, total=total,
            page_index=sm.get("PageIndex", 1), page_size=sm.get("PageSize", 20))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPATROLList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetPATROLDetail")
async def get_patrol_detail(PATROLId: Optional[int] = Query(None), db: DatabaseHelper = Depends(get_db)):
    """获取日常巡检表明细"""
    try:
        data = examine_service.get_patrol_detail(db, PATROLId)
        if data is None: return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPATROLDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/WeChat_GetExamineList")
async def wechat_get_examine_list(
    SPRegionType_ID: Optional[str] = Query(""), Serverpart_ID: Optional[str] = Query(""),
    SearchStartDate: Optional[str] = Query(""), SearchEndDate: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取小程序考核列表"""
    try:
        result = examine_service.wechat_get_examine_list(db, SPRegionType_ID, Serverpart_ID, SearchStartDate, SearchEndDate)
        json_list = JsonListData.create(data_list=result, total=len(result))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetExamineList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/WeChat_GetExamineDetail")
async def wechat_get_examine_detail(request: Request, db: DatabaseHelper = Depends(get_db)):
    """获取小程序考核明细数据"""
    try:
        params_lower = {k.lower(): v for k, v in request.query_params.items()}
        examine_id_str = params_lower.get("examineid")
        if not examine_id_str: return Result.fail(code=200, msg="查询失败，请传入考核内码！")
        result = examine_service.wechat_get_examine_detail(db, int(examine_id_str))
        json_list = JsonListData.create(data_list=result, total=len(result))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetExamineDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/WeChat_GetPatrolList")
async def wechat_get_patrol_list(
    SPRegionType_ID: Optional[str] = Query(""), Serverpart_ID: Optional[str] = Query(""),
    SearchStartDate: Optional[str] = Query(""), SearchEndDate: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取小程序日常巡检列表"""
    try:
        if not SearchStartDate and not SearchEndDate:
            return Result.fail(code=999, msg="查询失败，请传入有效的查询日期范围！")
        result = examine_service.wechat_get_patrol_list(db, SPRegionType_ID, Serverpart_ID, SearchStartDate, SearchEndDate)
        json_list = JsonListData.create(data_list=result, total=len(result))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetPatrolList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/WeChat_GetMeetingList")
async def wechat_get_meeting_list(
    SPRegionType_ID: Optional[str] = Query(""), Serverpart_ID: Optional[str] = Query(""),
    SearchStartDate: Optional[str] = Query(""), SearchEndDate: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取小程序晨会列表"""
    try:
        result = examine_service.wechat_get_meeting_list(db, SPRegionType_ID, Serverpart_ID, SearchStartDate, SearchEndDate)
        json_list = JsonListData.create(data_list=result, total=len(result))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetMeetingList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetPatrolAnalysis")
async def get_patrol_analysis(
    provinceCode: Optional[str] = Query(None), ServerpartId: Optional[str] = Query(""),
    SPRegionType_ID: Optional[str] = Query(""), StartDate: Optional[str] = Query(None),
    EndDate: Optional[str] = Query(None), db: DatabaseHelper = Depends(get_db)
):
    """获取日常巡检分析数据"""
    try:
        data = examine_service.get_patrol_analysis(db, provinceCode, ServerpartId, SPRegionType_ID, StartDate, EndDate)
        if data is None: return Result.fail(code=200, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPatrolAnalysis 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetExamineAnalysis")
async def get_examine_analysis(
    DataType: int = Query(1), StartMonth: Optional[str] = Query(None), EndMonth: Optional[str] = Query(None),
    provinceCode: Optional[str] = Query(None), ServerpartId: Optional[str] = Query(""),
    SPRegionType_ID: Optional[str] = Query(""), db: DatabaseHelper = Depends(get_db)
):
    """获取月度考核结果"""
    try:
        result = examine_service.get_examine_analysis(db, DataType, StartMonth, EndMonth, provinceCode, ServerpartId, SPRegionType_ID)
        json_list = JsonListData.create(data_list=result, total=len(result))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetExamineAnalysis 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetExamineResultList")
async def get_examine_result_list(
    DataType: Optional[int] = Query(None), StartMonth: Optional[str] = Query(None),
    EndMonth: Optional[str] = Query(None), provinceCode: Optional[str] = Query(None),
    ServerpartId: Optional[str] = Query(""), SPRegionType_ID: Optional[str] = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取驿达看板-首页考核列表"""
    try:
        result = examine_service.get_examine_result_list(db, DataType, StartMonth, EndMonth, provinceCode, ServerpartId, SPRegionType_ID)
        json_list = JsonListData.create(data_list=result, total=len(result))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetExamineResultList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Examine/GetPatrolResultList")
async def get_patrol_result_list(
    provinceCode: Optional[str] = Query(None), ServerpartId: Optional[str] = Query(""),
    SPRegionType_ID: Optional[str] = Query(""), StartDate: Optional[str] = Query(None),
    EndDate: Optional[str] = Query(None), db: DatabaseHelper = Depends(get_db)
):
    """获取驿达看板-首页巡查列表"""
    try:
        rows = examine_service.get_patrol_result_list(db, provinceCode, ServerpartId, SPRegionType_ID, StartDate, EndDate)
        json_list = JsonListData.create(data_list=rows, total=len(rows))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPatrolResultList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Examine/GetEvaluateResList")
async def get_evaluate_res_list(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取考评考核数据"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        evaluate_list = examine_service.get_evaluate_res_list(
            params.get("ProvinceCode", ""), int(params.get("RoleType", 1)),
            params.get("StatisticsMonth", ""), params.get("ServerpartId", ""))
        total = len(evaluate_list)
        json_list = JsonListData.create(data_list=evaluate_list, total=total, page_size=total if total > 0 else 10, page_index=1)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        return Result.fail(msg="解密失败")
    except Exception as ex:
        return Result.fail(msg="查询失败")
