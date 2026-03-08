from __future__ import annotations
# -*- coding: utf-8 -*-
"""
REVENUECONFIRM + PAYMENTCONFIRM + RTPAYMENTRECORD + REMARKS 路由
路由前缀：/BusinessProject/
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.business_project import revenueconfirm_service as rc_svc
from services.business_project import paymentconfirm_service as pc_svc
from routers.deps import get_db

router = APIRouter()


# ========== RevenueConfirm 5 个接口 ==========

@router.post("/BusinessProject/GetRevenueConfirmList")
async def get_revenueconfirm_list_post(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收回款确认表列表（POST）"""
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total, data_list = rc_svc.get_revenueconfirm_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueConfirmList POST 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetRevenueConfirmList")
async def get_revenueconfirm_list_get(
    ServerpartId: str = Query("", description="服务区内码"),
    MerchantsId: str = Query("", description="经营商户内码"),
    BusinessType: str = Query("", description="经营模式"),
    StartDate: str = Query("", description="统计开始日期"),
    EndDate: str = Query("", description="统计结束日期"),
    PageSize: Optional[int] = Query(None), PageIndex: Optional[int] = Query(None),
    SortStr: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区应收回款信息（GET 三表 JOIN）"""
    try:
        total, data_list = rc_svc.get_revenueconfirm_list_get(
            db, ServerpartId, MerchantsId, BusinessType, StartDate, EndDate,
            PageSize, PageIndex, SortStr)
        pi = PageIndex or 1
        ps = PageSize or len(data_list) if data_list else 0
        json_list = JsonListData.create(data_list=data_list, total=total, page_index=pi, page_size=ps)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueConfirmList GET 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetRevenueConfirmDetail")
async def get_revenueconfirm_detail(
    RevenueConfirmId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        detail = rc_svc.get_revenueconfirm_detail(db, RevenueConfirmId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueConfirmDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroRevenueConfirm")
async def synchro_revenueconfirm(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        success = rc_svc.synchro_revenueconfirm(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroRevenueConfirm 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteRevenueConfirm", methods=["GET", "POST"])
async def delete_revenueconfirm(
    RevenueConfirmId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        success = rc_svc.delete_revenueconfirm(db, RevenueConfirmId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteRevenueConfirm 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ========== PaymentConfirm 6 个接口 ==========

@router.post("/BusinessProject/GetPaymentConfirmList")
async def get_paymentconfirm_list_post(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total, data_list = pc_svc.get_paymentconfirm_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPaymentConfirmList POST 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetPaymentConfirmList")
async def get_paymentconfirm_list_get(
    MerchantsId: str = Query(""), ServerpartShopIds: str = Query(""),
    BusinessProjectId: str = Query(""), AccountDate: str = Query(""),
    ShowJustPayable: int = Query(0), WholeAccountType: int = Query(1),
    AccountType: str = Query(""), StartDate: str = Query(""),
    EndDate: str = Query(""), ShowRemarks: bool = Query(False),
    SortStr: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        if not MerchantsId and not ServerpartShopIds and not BusinessProjectId:
            return Result(Result_Code=200, Result_Desc="查询失败，请传入经营商户内码或门店内码集合或经营项目内码！")
        data_list, summary_list = pc_svc.get_paymentconfirm_list_get(
            db, MerchantsId, ServerpartShopIds, BusinessProjectId, AccountDate,
            ShowJustPayable, WholeAccountType, AccountType, StartDate, EndDate,
            ShowRemarks, SortStr)
        json_list = {"TotalCount": len(data_list), "DataList": data_list, "OtherData": summary_list}
        return Result.success(data=json_list, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPaymentConfirmList GET 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetPaymentConfirmDetail")
async def get_paymentconfirm_detail(
    PaymentConfirmId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        detail = pc_svc.get_paymentconfirm_detail(db, PaymentConfirmId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPaymentConfirmDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SeparatePaymentRecord")
async def separate_payment_record(data: list, db: DatabaseHelper = Depends(get_db)):
    try:
        success = pc_svc.separate_payment_record(db, data)
        if success:
            return Result.success(msg="保存成功")
        return Result(Result_Code=200, Result_Desc="保存失败！")
    except Exception as ex:
        logger.error(f"SeparatePaymentRecord 保存失败: {ex}")
        return Result.fail(msg=f"保存失败{ex}")


@router.post("/BusinessProject/SynchroPaymentConfirm")
async def synchro_paymentconfirm(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        success = pc_svc.synchro_paymentconfirm(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroPaymentConfirm 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeletePaymentConfirm", methods=["GET", "POST"])
async def delete_paymentconfirm(
    PaymentConfirmId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        success, msg = pc_svc.delete_paymentconfirm(db, PaymentConfirmId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc=msg or "删除失败！")
    except Exception as ex:
        logger.error(f"DeletePaymentConfirm 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ========== RTPaymentRecord 4 个接口 ==========

@router.post("/BusinessProject/GetRTPaymentRecordList")
async def get_rtpaymentrecord_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total, data_list = pc_svc.get_rtpaymentrecord_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRTPaymentRecordList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetRTPaymentRecordDetail")
async def get_rtpaymentrecord_detail(
    RTPaymentRecordId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        detail = pc_svc.get_rtpaymentrecord_detail(db, RTPaymentRecordId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRTPaymentRecordDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroRTPaymentRecord")
async def synchro_rtpaymentrecord(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        success = pc_svc.synchro_rtpaymentrecord(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroRTPaymentRecord 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteRTPaymentRecord", methods=["GET", "POST"])
async def delete_rtpaymentrecord(
    RTPaymentRecordId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        success = pc_svc.delete_rtpaymentrecord(db, RTPaymentRecordId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteRTPaymentRecord 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")


# ========== Remarks 4 个接口 ==========

@router.post("/BusinessProject/GetRemarksList")
async def get_remarks_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    try:
        if search_model is None:
            search_model = SearchModel()
        if search_model.SearchParameter is None:
            search_model.SearchParameter = {}
        total, data_list = pc_svc.get_remarks_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRemarksList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/BusinessProject/GetRemarksDetail")
async def get_remarks_detail(
    RemarksId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        detail = pc_svc.get_remarks_detail(db, RemarksId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRemarksDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BusinessProject/SynchroRemarks")
async def synchro_remarks(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        success = pc_svc.synchro_remarks(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroRemarks 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.api_route("/BusinessProject/DeleteRemarks", methods=["GET", "POST"])
async def delete_remarks(
    RemarksId: int = Query(...),
    db: DatabaseHelper = Depends(get_db)
):
    try:
        success = pc_svc.delete_remarks(db, RemarksId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteRemarks 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
