from __future__ import annotations
# -*- coding: utf-8 -*-
"""
批量模块路由 Part1：Audit + MobilePay
响应格式已统一为 Result 标准格式（Result_Code/Result_Desc/Result_Data）
整改包：AU-01（Audit 契约修复）、B1 MobilePay 响应格式统一
"""
from fastapi import APIRouter, Depends, Request
from routers.deps import get_db
from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.audit import audit_service
from services.mobilepay import mobilepay_service

# ============================================================
# Audit (24 个接口) — 响应格式已统一为 Result
# ============================================================
audit_router = APIRouter()

# YSABNORMALITY
@audit_router.post("/Audit/GetYSABNORMALITYList")
def get_ysabnormality_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_entity_list(db, "YSABNORMALITY", search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.get("/Audit/GetYSABNORMALITYDetail")
def get_ysabnormality_detail(YSABNORMALITYId: int, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_entity_detail(db, "YSABNORMALITY", YSABNORMALITYId))

@audit_router.post("/Audit/GetYSABNORMALITYDETAILList")
def get_ysabnormality_detail_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_ysabnormality_detail_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

# ABNORMALAUDIT
@audit_router.post("/Audit/GetABNORMALAUDITList")
def get_abnormalaudit_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_entity_list(db, "ABNORMALAUDIT", search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.get("/Audit/GetAbnormalAuditDetail")
def get_abnormal_audit_detail(AbnormalAuditId: int, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_entity_detail(db, "ABNORMALAUDIT", AbnormalAuditId))

@audit_router.post("/Audit/SynchroAbnormalAudit")
def synchro_abnormal_audit(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = audit_service.synchro_entity(db, "ABNORMALAUDIT", data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

@audit_router.post("/Audit/DeleteAbnormalAudit")
def delete_abnormal_audit(AbnormalAuditId: int, db: DatabaseHelper = Depends(get_db)):
    if audit_service.delete_entity(db, "ABNORMALAUDIT", AbnormalAuditId):
        return Result.success()
    return Result.fail(msg="删除失败")

# CHECKACCOUNT
@audit_router.post("/Audit/GetCHECKACCOUNTList")
def get_checkaccount_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_entity_list(db, "CHECKACCOUNT", search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.get("/Audit/GetCHECKACCOUNTDetail")
def get_checkaccount_detail(CHECKACCOUNTId: int, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_entity_detail(db, "CHECKACCOUNT", CHECKACCOUNTId))

@audit_router.post("/Audit/SynchroCHECKACCOUNT")
def synchro_checkaccount(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = audit_service.synchro_entity(db, "CHECKACCOUNT", data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

@audit_router.post("/Audit/DeleteCHECKACCOUNT")
def delete_checkaccount(CHECKACCOUNTId: int, db: DatabaseHelper = Depends(get_db)):
    if audit_service.delete_entity(db, "CHECKACCOUNT", CHECKACCOUNTId):
        return Result.success()
    return Result.fail(msg="删除失败")

# AUDITTASKS
@audit_router.post("/Audit/GetAUDITTASKSList")
def get_audittasks_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_entity_list(db, "AUDITTASKS", search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.get("/Audit/GetAUDITTASKSDetail")
def get_audittasks_detail(AUDITTASKSId: int, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_entity_detail(db, "AUDITTASKS", AUDITTASKSId))

@audit_router.post("/Audit/SynchroAUDITTASKS")
def synchro_audittasks(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = audit_service.synchro_entity(db, "AUDITTASKS", data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

# 散装接口
@audit_router.post("/Audit/GetAuditList")
def get_audit_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_audit_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.post("/Audit/GetAuditDetils")
def get_audit_details(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_audit_details(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.post("/Audit/UpLoadAuditExplain")
def upload_audit_explain(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = audit_service.upload_audit_explain(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="上传失败")

@audit_router.post("/Audit/GetCheckAccountReport")
def get_check_account_report(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_check_account_report(db, search_model))

@audit_router.post("/Audit/GetYsabnormalityReport")
def get_ysabnormality_report(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_ysabnormality_report(db, search_model))

@audit_router.post("/Audit/GetSpecialBehaviorReport")
def get_special_behavior_report(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_special_behavior_report(db, search_model))

@audit_router.post("/Audit/GetAbnormalRateReport")
def get_abnormal_rate_report(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_abnormal_rate_report(db, search_model))

@audit_router.post("/Audit/GetAuditTasksReport")
def get_audit_tasks_report(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    return Result.success(audit_service.get_audit_tasks_report(db, search_model))

@audit_router.post("/Audit/GetAuditTasksDetailList")
def get_audit_tasks_detail_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = audit_service.get_audit_tasks_detail_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@audit_router.post("/Audit/IssueAuditTasks")
def issue_audit_tasks(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = audit_service.issue_audit_tasks(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="下发失败")


# ============================================================
# MobilePay (17 个接口) — 响应格式已统一为 Result
# ============================================================
mobilepay_router = APIRouter()

@mobilepay_router.post("/MobilePay/SetKwyRoyaltyRate")
def set_kwy_royalty_rate(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = mobilepay_service.set_kwy_royalty_rate(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@mobilepay_router.post("/MobilePay/GetKwyRoyaltyRate")
def get_kwy_royalty_rate(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_kwy_royalty_rate(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/RoyaltyWithdraw")
def royalty_withdraw(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = mobilepay_service.royalty_withdraw(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@mobilepay_router.get("/MobilePay/GetKwyRoyalty")
def get_kwy_royalty(ServerpartIds: str = "", db: DatabaseHelper = Depends(get_db)):
    return Result.success(mobilepay_service.get_kwy_royalty(db, ServerpartIds=ServerpartIds))

@mobilepay_router.get("/MobilePay/GetKwyRoyaltyForAll")
def get_kwy_royalty_for_all(ServerpartIds: str = "", db: DatabaseHelper = Depends(get_db)):
    return Result.success(mobilepay_service.get_kwy_royalty_for_all(db, ServerpartIds=ServerpartIds))

@mobilepay_router.get("/MobilePay/GetMobilePayRoyaltyReport")
def get_mobilepay_royalty_report(db: DatabaseHelper = Depends(get_db)):
    return Result.success(mobilepay_service.get_mobilepay_royalty_report(db))

@mobilepay_router.post("/MobilePay/SynchroBANKACCOUNTVERIFY")
def synchro_bankaccountverify(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = mobilepay_service.synchro_bankaccountverify(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

@mobilepay_router.post("/MobilePay/GetBANKACCOUNTVERIFYList")
def get_bankaccountverify_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_bankaccountverify_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetBANKACCOUNTVERIFYRegionList")
def get_bankaccountverify_region_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_bankaccountverify_region_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetBANKACCOUNTVERIFYServerList")
def get_bankaccountverify_server_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_bankaccountverify_server_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.get("/MobilePay/GetBANKACCOUNTVERIFYTreeList")
def get_bankaccountverify_tree_list(db: DatabaseHelper = Depends(get_db)):
    return Result.success(mobilepay_service.get_bankaccountverify_tree_list(db))

@mobilepay_router.post("/MobilePay/GetRoyaltyRecordList")
def get_royalty_record_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_royalty_record_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetMobilePayResult")
def get_mobilepay_result(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_mobilepay_result(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetChinaUmsSubMaster")
def get_chinaums_sub_master(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_chinaums_sub_master(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetChinaUmsSubAccountDetail")
def get_chinaums_sub_account_detail(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_chinaums_sub_account_detail(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetChinaUmsSubAccountSummary")
def get_chinaums_sub_account_summary(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_chinaums_sub_account_summary(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@mobilepay_router.post("/MobilePay/GetChinaUmsSubSummary")
def get_chinaums_sub_summary(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = mobilepay_service.get_chinaums_sub_summary(db, search_model)
    return Result.success(JsonListData.create(rows, total))


@mobilepay_router.post("/MobilePay/CorrectSellMasterState")
async def correct_sellmaster_state(request: Request, db: DatabaseHelper = Depends(get_db)):
    """处理移动支付差异流水（纠偏销售主单状态）
    入参: [{label: 订单号, value: 交易结果(0=失败,9=成功)}, ...]
    """
    sell_master_list = await request.json()
    mobilepay_service.correct_sellmaster_state(db, sell_master_list)
    return Result.success(msg="处理完成")

