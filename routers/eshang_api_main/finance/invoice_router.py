from __future__ import annotations
# -*- coding: utf-8 -*-
"""
InvoiceController 路由（12 个接口）
BILL CRUD (4) + BILLDETAIL CRUD (4) + 散装接口 (4)
注: INVOICEINFO / GOODSTAXINFO / APPLYAPPROVE 各4个 = 12 个加密接口跳过
"""
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.finance import invoice_service as inv_svc
from routers.deps import get_db

router = APIRouter()


# ==================== BILL CRUD ====================

@router.post("/Invoice/GetBILLList")
async def get_bill_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    """获取票据信息表列表"""
    try:
        rows, total = inv_svc.get_bill_list(db, data)
        page_index = data.get("PageIndex", 1)
        page_size = data.get("PageSize", 15)
        return Result.success(JsonListData(
            List=rows, TotalCount=total,
            PageIndex=page_index, PageSize=page_size))
    except Exception as e:
        logger.error(f"GetBILLList 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Invoice/GetBILLDetail")
async def get_bill_detail(
    BILLId: int = Query(None), BillNo: str = Query(""),
    db: DatabaseHelper = Depends(get_db)
):
    """获取票据信息表明细"""
    try:
        row = inv_svc.get_bill_detail(db, BILLId, BillNo)
        return Result.success(row)
    except Exception as e:
        logger.error(f"GetBILLDetail 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.post("/Invoice/SynchroBILL")
async def synchro_bill(data: dict, db: DatabaseHelper = Depends(get_db)):
    """同步票据信息表"""
    try:
        ok, result = inv_svc.synchro_bill(db, data)
        if ok:
            return Result.success(result, msg="同步成功")
        return Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"SynchroBILL 失败: {e}")
        return Result.fail(f"同步失败{e}")


@router.api_route("/Invoice/DeleteBILL", methods=["GET", "POST"])
async def delete_bill(BILLId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    """删除票据信息表"""
    try:
        ok = inv_svc.delete_bill(db, BILLId)
        if ok:
            return Result.success(msg="删除成功")
        return Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"DeleteBILL 失败: {e}")
        return Result.fail(f"删除失败{e}")


# ==================== BILLDETAIL CRUD ====================

@router.post("/Invoice/GetBILLDETAILList")
async def get_billdetail_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    """获取发票明细表列表"""
    try:
        rows, total = inv_svc.get_billdetail_list(db, data)
        page_index = data.get("PageIndex", 1)
        page_size = data.get("PageSize", 15)
        return Result.success(JsonListData(
            List=rows, TotalCount=total,
            PageIndex=page_index, PageSize=page_size))
    except Exception as e:
        logger.error(f"GetBILLDETAILList 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.get("/Invoice/GetBILLDETAILDetail")
async def get_billdetail_detail(BILLDETAILId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    """获取发票明细表明细"""
    try:
        row = inv_svc.get_billdetail_detail(db, BILLDETAILId)
        return Result.success(row)
    except Exception as e:
        logger.error(f"GetBILLDETAILDetail 失败: {e}")
        return Result.fail(f"查询失败{e}")


@router.post("/Invoice/SynchroBILLDETAIL")
async def synchro_billdetail(data: dict, db: DatabaseHelper = Depends(get_db)):
    """同步发票明细表"""
    try:
        ok, result = inv_svc.synchro_billdetail(db, data)
        if ok:
            return Result.success(result, msg="同步成功")
        return Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"SynchroBILLDETAIL 失败: {e}")
        return Result.fail(f"同步失败{e}")


@router.api_route("/Invoice/DeleteBILLDETAIL", methods=["GET", "POST"])
async def delete_billdetail(BILLDETAILId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    """删除发票明细表"""
    try:
        ok = inv_svc.delete_billdetail(db, BILLDETAILId)
        if ok:
            return Result.success(msg="删除成功")
        return Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        logger.error(f"DeleteBILLDETAIL 失败: {e}")
        return Result.fail(f"删除失败{e}")


# ==================== 散装接口 ====================

@router.post("/Invoice/WriteBackInvoice")
async def write_back_invoice(data: dict, db: DatabaseHelper = Depends(get_db)):
    """回写票据开票结果信息"""
    try:
        ok, msg = inv_svc.write_back_invoice(db, data)
        if ok:
            return Result.success(msg="回写成功！")
        return Result.fail(f"回写失败，{msg}！", code=200)
    except Exception as e:
        logger.error(f"WriteBackInvoice 失败: {e}")
        return Result.fail(f"回写失败{e}")


@router.post("/Invoice/SendHXInvoiceInfo")
async def send_hx_invoice_info(request: Request):
    """发送开票信息至航行开票系统"""
    try:
        data = await request.json()
        ok, msg = inv_svc.send_hx_invoice_info(data if isinstance(data, list) else [data])
        if ok:
            return Result.success(msg="请求成功！")
        return Result.fail(f"请求失败，{msg}", code=200)
    except Exception as e:
        logger.error(f"SendHXInvoiceInfo 失败: {e}")
        return Result.fail(f"请求失败{e}")


@router.post("/Invoice/RewriteJDPJInfo")
async def rewrite_jdpj_info(data: dict, db: DatabaseHelper = Depends(get_db)):
    """回写金蝶开票结果信息"""
    try:
        ok, msg = inv_svc.rewrite_jdpj_info(db, data)
        if ok:
            # 原 C# 返回的是自定义 JSON 格式
            return {"message": "成功", "errorCode": "0000", "success": True}
        return Result.fail(f"回写失败，{msg}！", code=200)
    except Exception as e:
        logger.error(f"RewriteJDPJInfo 失败: {e}")
        return Result.fail(f"回写失败{e}")


@router.post("/Invoice/ForwardJDPJInterface")
async def forward_jdpj_interface(data: dict):
    """金蝶开票/红冲申请（接口转发）"""
    try:
        ok, result, msg = inv_svc.forward_jdpj_interface(data)
        if ok:
            import json as _json
            try:
                return _json.loads(result)
            except Exception:
                return Result.success(result)
        return Result.fail(f"转发失败{msg}")
    except Exception as e:
        logger.error(f"ForwardJDPJInterface 失败: {e}")
        return Result.fail(f"转发失败{e}")
