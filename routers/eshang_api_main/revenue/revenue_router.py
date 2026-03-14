from __future__ import annotations
# -*- coding: utf-8 -*-
"""
RevenueController 路由（60 个接口）
7 组 CRUD (28) + 散装报表 (32，含 GetBusinessDate)
"""
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.revenue import revenue_service as rev_svc
from routers.deps import get_db

router = APIRouter()


# ============================================================
# 宏：批量生成 CRUD 路由
# ============================================================
def _make_crud_routes(entity_name: str, route_prefix: str, pk_param: str):
    """为 CRUD 实体生成 4 个路由"""

    @router.post(f"/{route_prefix}/Get{entity_name}List",
                 name=f"get_{entity_name.lower()}_list")
    async def _get_list(data: dict, db: DatabaseHelper = Depends(get_db),
                        _en=entity_name):
        try:
            rows, total = rev_svc.get_entity_list(db, _en, data)
            return Result.success(JsonListData(
                List=rows, TotalCount=total,
                PageIndex=data.get("PageIndex", 1),
                PageSize=data.get("PageSize", 15)))
        except Exception as e:
            logger.error(f"Get{_en}List 失败: {e}")
            return Result.fail(msg="查询失败")

    @router.get(f"/{route_prefix}/Get{entity_name}Detail",
                name=f"get_{entity_name.lower()}_detail")
    async def _get_detail(db: DatabaseHelper = Depends(get_db),
                          _en=entity_name, _pk=pk_param, **kwargs):
        try:
            pk_val = kwargs.get(_pk, 0)
            row = rev_svc.get_entity_detail(db, _en, pk_val)
            return Result.success(row)
        except Exception as e:
            logger.error(f"Get{_en}Detail 失败: {e}")
            return Result.fail(msg="查询失败")

    @router.post(f"/{route_prefix}/Synchro{entity_name}",
                 name=f"synchro_{entity_name.lower()}")
    async def _synchro(data: dict, db: DatabaseHelper = Depends(get_db),
                       _en=entity_name):
        try:
            ok, result = rev_svc.synchro_entity(db, _en, data)
            if ok:
                return Result.success(result, msg="同步成功")
            return Result.fail("更新失败，数据不存在！", code=200)
        except Exception as e:
            logger.error(f"Synchro{_en} 失败: {e}")
            return Result.fail(msg="同步失败")

    @router.api_route(f"/{route_prefix}/Delete{entity_name}", methods=["GET", "POST"],
                      name=f"delete_{entity_name.lower()}")
    async def _delete(db: DatabaseHelper = Depends(get_db),
                      _en=entity_name, _pk=pk_param, **kwargs):
        try:
            pk_val = kwargs.get(_pk, 0)
            ok = rev_svc.delete_entity(db, _en, pk_val)
            if ok:
                return Result.success(msg="删除成功")
            return Result.fail("删除失败，数据不存在！", code=200)
        except Exception as e:
            logger.error(f"Delete{_en} 失败: {e}")
            return Result.fail(msg="删除失败")


# 由于 FastAPI 路由闭包问题，改用显式定义每组 CRUD

# ==================== REVENUEDAILYSPLIT CRUD ====================
@router.post("/Revenue/GetREVENUEDAILYSPLITList")
async def get_revenuedailysplit_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "REVENUEDAILYSPLIT", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetREVENUEDAILYSPLITDetail")
async def get_revenuedailysplit_detail(REVENUEDAILYSPLITId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "REVENUEDAILYSPLIT", REVENUEDAILYSPLITId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroREVENUEDAILYSPLIT")
async def synchro_revenuedailysplit(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "REVENUEDAILYSPLIT", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeleteREVENUEDAILYSPLIT", methods=["GET", "POST"])
async def delete_revenuedailysplit(REVENUEDAILYSPLITId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "REVENUEDAILYSPLIT", REVENUEDAILYSPLITId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")

# ==================== PERSONSELL CRUD ====================
@router.post("/Revenue/GetPERSONSELLList")
async def get_personsell_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "PERSONSELL", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetPERSONSELLDetail")
async def get_personsell_detail(PERSONSELLId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "PERSONSELL", PERSONSELLId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroPERSONSELL")
async def synchro_personsell(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "PERSONSELL", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeletePERSONSELL", methods=["GET", "POST"])
async def delete_personsell(PERSONSELLId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "PERSONSELL", PERSONSELLId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")

# ==================== BUSINESSANALYSIS CRUD ====================
@router.post("/Revenue/GetBUSINESSANALYSISList")
async def get_businessanalysis_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "BUSINESSANALYSIS", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBUSINESSANALYSISDetail")
async def get_businessanalysis_detail(BUSINESSANALYSISId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "BUSINESSANALYSIS", BUSINESSANALYSISId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroBUSINESSANALYSIS")
async def synchro_businessanalysis(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "BUSINESSANALYSIS", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeleteBUSINESSANALYSIS", methods=["GET", "POST"])
async def delete_businessanalysis(BUSINESSANALYSISId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "BUSINESSANALYSIS", BUSINESSANALYSISId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")

# ==================== BRANDANALYSIS CRUD ====================
@router.post("/Revenue/GetBRANDANALYSISList")
async def get_brandanalysis_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "BRANDANALYSIS", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBRANDANALYSISDetail")
async def get_brandanalysis_detail(BRANDANALYSISId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "BRANDANALYSIS", BRANDANALYSISId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroBRANDANALYSIS")
async def synchro_brandanalysis(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "BRANDANALYSIS", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeleteBRANDANALYSIS", methods=["GET", "POST"])
async def delete_brandanalysis(BRANDANALYSISId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "BRANDANALYSIS", BRANDANALYSISId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")

# ==================== SITUATIONANALYSIS CRUD ====================
@router.post("/Revenue/GetSITUATIONANALYSISList")
async def get_situationanalysis_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "SITUATIONANALYSIS", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetSITUATIONANALYSISDetail")
async def get_situationanalysis_detail(SITUATIONANALYSISId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "SITUATIONANALYSIS", SITUATIONANALYSISId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroSITUATIONANALYSIS")
async def synchro_situationanalysis(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "SITUATIONANALYSIS", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeleteSITUATIONANALYSIS", methods=["GET", "POST"])
async def delete_situationanalysis(SITUATIONANALYSISId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "SITUATIONANALYSIS", SITUATIONANALYSISId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")

# ==================== BUSINESSWARNING CRUD ====================
@router.post("/Revenue/GetBUSINESSWARNINGList")
async def get_businesswarning_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "BUSINESSWARNING", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBUSINESSWARNINGDetail")
async def get_businesswarning_detail(BUSINESSWARNINGId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "BUSINESSWARNING", BUSINESSWARNINGId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroBUSINESSWARNING")
async def synchro_businesswarning(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "BUSINESSWARNING", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeleteBUSINESSWARNING", methods=["GET", "POST"])
async def delete_businesswarning(BUSINESSWARNINGId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "BUSINESSWARNING", BUSINESSWARNINGId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")

# ==================== ACCOUNTWARNING CRUD ====================
@router.post("/Revenue/GetACCOUNTWARNINGList")
async def get_accountwarning_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_entity_list(db, "ACCOUNTWARNING", data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetACCOUNTWARNINGDetail")
async def get_accountwarning_detail(ACCOUNTWARNINGId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        return Result.success(rev_svc.get_entity_detail(db, "ACCOUNTWARNING", ACCOUNTWARNINGId))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/SynchroACCOUNTWARNING")
async def synchro_accountwarning(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, r = rev_svc.synchro_entity(db, "ACCOUNTWARNING", data)
        return Result.success(r, msg="同步成功") if ok else Result.fail("更新失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="同步失败")

@router.api_route("/Revenue/DeleteACCOUNTWARNING", methods=["GET", "POST"])
async def delete_accountwarning(ACCOUNTWARNINGId: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        ok = rev_svc.delete_entity(db, "ACCOUNTWARNING", ACCOUNTWARNINGId)
        return Result.success(msg="删除成功") if ok else Result.fail("删除失败，数据不存在！", code=200)
    except Exception as e:
        return Result.fail(msg="删除失败")


# ==================== 散装接口 ====================

@router.post("/Revenue/ModifyRevenueDailySplitList")
async def modify_revenue_daily_split_list(request: Request, db: DatabaseHelper = Depends(get_db)):
    try:
        data = await request.json()
        ok, msg = rev_svc.modify_revenue_daily_split_list(db, data if isinstance(data, list) else [data])
        return Result.success(msg="更新成功") if ok else Result.fail(f"更新失败，{msg}", code=200)
    except Exception as e:
        return Result.fail(msg="更新失败")

@router.post("/Revenue/GetRevenuePushList")
async def get_revenue_push_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_push_list(db, data.get("pushProvinceCode",""), data.get("Statistics_Date",""))
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetHisCommoditySaleList")
async def get_his_commodity_sale_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_his_commodity_sale_list(db, data.get("ProvinceCode",""), data.get("startMonth",""), data.get("endMonth",""), data.get("ServerpartShopIds",""))
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetRevenueDataList")
async def get_revenue_data_list(ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
                                StartDate: str = Query(""), EndDate: str = Query(""),
                                DataSourceType: int = Query(1), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_data_list(db, ServerpartIds, ServerpartShopIds, StartDate, EndDate, DataSourceType)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetRevenueReport")
async def get_revenue_report(DataType: int = Query(1), ServerpartIds: str = Query(""),
                             ServerpartShopIds: str = Query(""), StartDate: str = Query(""),
                             EndDate: str = Query(""), GroupBy: str = Query(""),
                             SearchKeyValue: str = Query(""), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_report(db, DataType=DataType, ServerpartIds=ServerpartIds,
                                          ServerpartShopIds=ServerpartShopIds, StartDate=StartDate,
                                          EndDate=EndDate, GroupBy=GroupBy, SearchKeyValue=SearchKeyValue)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetRevenueReportByDate")
async def get_revenue_report_by_date(ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
                                     StartDate: str = Query(""), EndDate: str = Query(""),
                                     GroupBy: str = Query(""), SearchKeyValue: str = Query(""),
                                     wrapType: int = Query(0), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_report_by_date(db, ServerpartIds=ServerpartIds, StartDate=StartDate, EndDate=EndDate)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetMerchantRevenueReport")
async def get_merchant_revenue_report(DataType: int = Query(1), ServerpartIds: str = Query(""),
                                      ServerpartShopIds: str = Query(""), StartDate: str = Query(""),
                                      EndDate: str = Query(""), GroupByDaily: bool = Query(False),
                                      CalculateStartDate: bool = Query(False), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_merchant_revenue_report(db, DataType=DataType, ServerpartIds=ServerpartIds, StartDate=StartDate, EndDate=EndDate)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/BankAccountCompare")
async def bank_account_compare(AccountDate: str = Query(""), ServerpartCode: str = Query(""),
                               ShopCode: str = Query(""), MachineCode: str = Query(""),
                               db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.bank_account_compare(db, AccountDate, ServerpartCode, ShopCode, MachineCode)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBankAccountReport")
async def get_bank_account_report(ServerpartShopIds: str = Query(""), StartDate: str = Query(""),
                                  EndDate: str = Query(""), Payment_Channel: str = Query(""),
                                  db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_bank_account_report(db, ServerpartShopIds, StartDate, EndDate, Payment_Channel)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBankAccountList")
async def get_bank_account_list(ServerpartShopIds: str = Query(""), StartDate: str = Query(""),
                                EndDate: str = Query(""), Payment_Channel: str = Query(""),
                                db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_bank_account_list(db, ServerpartShopIds, StartDate, EndDate, Payment_Channel)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetCurTotalRevenue")
async def get_cur_total_revenue(ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
                                db: DatabaseHelper = Depends(get_db)):
    try:
        data = rev_svc.get_cur_total_revenue(db, ServerpartIds, ServerpartShopIds)
        return Result.success(data)
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetTotalRevenue")
async def get_total_revenue(ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
                            StartDate: str = Query(""), EndDate: str = Query(""),
                            DataSourceType: int = Query(1), db: DatabaseHelper = Depends(get_db)):
    try:
        data = rev_svc.get_total_revenue(db, ServerpartIds, ServerpartShopIds, StartDate, EndDate, DataSourceType)
        return Result.success(data)
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBusinessDate")
async def get_business_date(ServerpartIds: str = Query(""), ServerpartShopIds: str = Query(""),
                            db: DatabaseHelper = Depends(get_db)):
    try:
        data = rev_svc.get_business_date(db, ServerpartIds, ServerpartShopIds)
        return Result.success(data)
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetYSSellMasterList")
async def get_ys_sell_master_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        result = rev_svc.get_ys_sell_master_list(db, data)
        # C# 原逻辑: 返回 JsonList<YSSELLMASTERModel, YSSELLMASTERTotalModel>
        if len(result) == 3:
            rows, total, total_model = result
            resp = JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15))
            resp.OtherModel = total_model
            return Result.success(resp)
        else:
            rows, total = result
            return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetSellMasterCompareList")
async def get_sell_master_compare_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_sell_master_compare_list(db, data.get("serverpartShopIds",""), data.get("startDate",""), data.get("endDate",""), data.get("isNew",0))
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetYSSellDetailsList")
async def get_ys_sell_details_list(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows, total = rev_svc.get_ys_sell_details_list(db, data)
        return Result.success(JsonListData(List=rows, TotalCount=total, PageIndex=data.get("PageIndex",1), PageSize=data.get("PageSize",15)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetTransactionCustomer")
async def get_transaction_customer(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_transaction_customer(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetTransactionCustomerByDate")
async def get_transaction_customer_by_date(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_transaction_customer_by_date(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetRevenueYOYQOQ")
async def get_revenue_yoy_qoq(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_yoy_qoq(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetRevenueYOYQOQByDate")
async def get_revenue_yoy_qoq_by_date(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_yoy_qoq_by_date(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetRevenueQOQ")
async def get_revenue_qoq(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_qoq(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetRevenueQOQByDate")
async def get_revenue_qoq_by_date(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_qoq_by_date(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetMonthCompare")
async def get_month_compare(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_month_compare(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/GetBusinessAnalysisReport")
async def get_business_analysis_report(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_business_analysis_report(db, **data)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetSituationAnalysis")
async def get_situation_analysis(ServerpartId: str = Query(""), db: DatabaseHelper = Depends(get_db)):
    try:
        data = rev_svc.get_situation_analysis(db, ServerpartId)
        return Result.success(data)
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBusinessTradeAnalysis")
async def get_business_trade_analysis(ServerpartId: str = Query(""), ServerpartShopId: str = Query(""),
                                      db: DatabaseHelper = Depends(get_db)):
    try:
        data = rev_svc.get_business_trade_analysis(db, ServerpartId, ServerpartShopId)
        return Result.success(data)
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBrandAnalysis")
async def get_brand_analysis(ServerpartId: str = Query(""), ServerpartShopId: str = Query(""),
                             db: DatabaseHelper = Depends(get_db)):
    try:
        data = rev_svc.get_brand_analysis(db, ServerpartId, ServerpartShopId)
        return Result.success(data)
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetMonthINCAnalysis")
async def get_month_inc_analysis(ServerpartId: str = Query(""), StatisticsStartMonth: str = Query(""),
                                 StatisticsEndMonth: str = Query(""), ServerpartShopIds: str = Query(""),
                                 DataType: int = Query(1), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_month_inc_analysis(db, ServerpartId=ServerpartId, StatisticsStartMonth=StatisticsStartMonth,
                                               StatisticsEndMonth=StatisticsEndMonth, ServerpartShopIds=ServerpartShopIds, DataType=DataType)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetRevenueReportByBIZPSPLITMONTH")
async def get_revenue_report_by_bizp_split_month(ServerpartIds: str = Query(""), StartDate: str = Query(""),
                                                  EndDate: str = Query(""), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_revenue_report_by_bizp_split_month(db, ServerpartIds=ServerpartIds, StartDate=StartDate, EndDate=EndDate)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.post("/Revenue/CorrectShopCigarette")
async def correct_shop_cigarette(data: dict, db: DatabaseHelper = Depends(get_db)):
    try:
        ok, msg = rev_svc.correct_shop_cigarette(db, data)
        return Result.success(msg="修正成功") if ok else Result.fail(f"修正失败，{msg}", code=200)
    except Exception as e:
        return Result.fail(msg="修正失败")

@router.get("/Revenue/GetCigaretteReport")
async def get_cigarette_report(ServerpartIds: str = Query(""), StartDate: str = Query(""),
                               EndDate: str = Query(""), db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_cigarette_report(db, ServerpartIds=ServerpartIds, StartDate=StartDate, EndDate=EndDate)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")

@router.get("/Revenue/GetBusinessItemSummary")
async def get_business_item_summary(DataType: int = Query(1), ProvinceCode: str = Query(""),
                                    ServerpartIds: str = Query(""),
                                    StartDate: str = Query(""), EndDate: str = Query(""),
                                    CompareStartDate: str = Query(""), CompareEndDate: str = Query(""),
                                    AccStartDate: str = Query(""), AccEndDate: str = Query(""),
                                    AccCompareStartDate: str = Query(""), AccCompareEndDate: str = Query(""),
                                    db: DatabaseHelper = Depends(get_db)):
    try:
        rows = rev_svc.get_business_item_summary(db, DataType=DataType, ProvinceCode=ProvinceCode,
                                                  ServerpartIds=ServerpartIds, StartDate=StartDate, EndDate=EndDate,
                                                  CompareStartDate=CompareStartDate, CompareEndDate=CompareEndDate,
                                                  AccStartDate=AccStartDate, AccEndDate=AccEndDate,
                                                  AccCompareStartDate=AccCompareStartDate, AccCompareEndDate=AccCompareEndDate)
        return Result.success(JsonListData(List=rows, TotalCount=len(rows)))
    except Exception as e:
        return Result.fail(msg="查询失败")
