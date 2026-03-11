from __future__ import annotations
# -*- coding: utf-8 -*-
"""
批量模块路由 Part2: Analysis + BusinessMan/Supplier + DataVerification/Sales + Picture
响应格式已统一为 Result 标准格式（Result_Code/Result_Desc/Result_Data/Message）
整改包：AN-01, BS-02, B1 Verification/Sales/Picture 响应格式统一
PKG-RESP-CORE-01: 路由工厂增加 try-except 保护
"""
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger
from routers.deps import get_db
from core.database import DatabaseHelper
from models.base import Result, JsonListData
from services.analysis import analysis_service
from services.businessman import businessman_service
from services.verification import verification_service
from services.picture import picture_service

# ============================================================
# Analysis (58 + 4 加密跳过 = 62)
# AN-01 整改完成: pk_val 已替换为实体专属参数名（使用 Query alias）
# ============================================================
analysis_router = APIRouter()

# CRUD 实体 — 11组 x 4
_A_ENTITIES = [
    "ANALYSISINS", "SENTENCE", "ASSETSPROFITS", "PROFITCONTRIBUTE",
    "PERIODMONTHPROFIT", "VEHICLEAMOUNT", "ANALYSISRULE",
    "PREFERRED_RATING", "PROMPT", "INVESTMENTANALYSIS", "INVESTMENTDETAIL"
]

for _e in _A_ENTITIES:
    _prefix = "Analysis"
    def _make_routes(ent):
        # 实体专属参数名：C# 原接口格式为 {EntityName}Id
        _param_name = f"{ent}Id"

        @analysis_router.post(f"/{_prefix}/Get{ent}List", name=f"get_{ent.lower()}_list")
        def _list(search_model: dict, db: DatabaseHelper = Depends(get_db), _ent=ent):
            try:
                rows, total = analysis_service.get_entity_list(db, _ent, search_model)
                pi = search_model.get("PageIndex", 1)
                ps = search_model.get("PageSize", 9)
                return Result.success(JsonListData.create(rows, total, page_index=pi, page_size=ps).model_dump(), msg="查询成功")
            except Exception as ex:
                logger.error(f"Get{_ent}List 查询失败: {ex}")
                return Result.fail(msg=f"查询失败{ex}")

        @analysis_router.get(f"/{_prefix}/Get{ent}Detail", name=f"get_{ent.lower()}_detail")
        def _detail(pk_val: int = Query(..., alias=_param_name),
                    db: DatabaseHelper = Depends(get_db), _ent=ent):
            try:
                return Result.success(analysis_service.get_entity_detail(db, _ent, pk_val), msg="查询成功")
            except Exception as ex:
                logger.error(f"Get{_ent}Detail 查询失败: {ex}")
                return Result.fail(msg=f"查询失败{ex}")

        @analysis_router.post(f"/{_prefix}/Synchro{ent}", name=f"synchro_{ent.lower()}")
        def _synchro(data: dict, db: DatabaseHelper = Depends(get_db), _ent=ent):
            try:
                ok, result = analysis_service.synchro_entity(db, _ent, data)
                if ok:
                    return Result.success(result)
                return Result.fail(msg="同步失败")
            except Exception as ex:
                logger.error(f"Synchro{_ent} 同步失败: {ex}")
                return Result.fail(msg=f"同步失败{ex}")

        @analysis_router.post(f"/{_prefix}/Delete{ent}", name=f"delete_{ent.lower()}")
        def _delete(pk_val: int = Query(..., alias=_param_name),
                    db: DatabaseHelper = Depends(get_db), _ent=ent):
            try:
                if analysis_service.delete_entity(db, _ent, pk_val):
                    return Result.success()
                return Result.fail(msg="删除失败")
            except Exception as ex:
                logger.error(f"Delete{_ent} 删除失败: {ex}")
                return Result.fail(msg=f"删除失败{ex}")
    _make_routes(_e)

# Analysis 散装接口
@analysis_router.post("/Analysis/GetASSETSPROFITSTreeList")
def get_assetsprofits_tree(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = analysis_service.get_assetsprofits_tree_list(db, search_model)
    ps = search_model.get("PageSize") or len(rows) or 999
    return Result.success(JsonListData.create(rows, total, page_size=ps).model_dump(), msg="查询成功")

@analysis_router.post("/Analysis/GetASSETSPROFITSBusinessTreeList")
def get_assetsprofits_biz_tree(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = analysis_service.get_assetsprofits_biz_tree_list(db, search_model)
    ps = search_model.get("PageSize") or len(rows) or 999
    return Result.success(JsonListData.create(rows, total, page_size=ps).model_dump(), msg="查询成功")

@analysis_router.get("/Analysis/GetASSETSPROFITSDateDetailList")
def get_assetsprofits_date_detail(
        serverPartId: int = 0, propertyAssetsId: int = 0,
        startDate: str = "", endDate: str = "", shopId: str = "",
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(analysis_service.get_assetsprofits_date_detail_list(
        db, serverPartId=serverPartId, propertyAssetsId=propertyAssetsId,
        startDate=startDate, endDate=endDate, shopId=shopId), msg="查询成功")

@analysis_router.get("/Analysis/GetAssetsLossProfitList")
def get_assets_loss_profit(
        serverPartId: int = 0, propertyAssetsId: int = 0,
        startDate: str = "", endDate: str = "", shopId: str = "",
        db: DatabaseHelper = Depends(get_db)):
    # C# 返回 NestingModel<AssetsProfitLossModel>
    result = analysis_service.get_assets_loss_profit_list(
        db, serverPartId=serverPartId, propertyAssetsId=propertyAssetsId,
        startDate=startDate, endDate=endDate, shopId=shopId)
    return Result.success(result, msg="查询成功")

@analysis_router.post("/Analysis/SyncPROFITCONTRIBUTEList")
def sync_profitcontribute_list(data_list: list, db: DatabaseHelper = Depends(get_db)):
    ok, msg = analysis_service.sync_profitcontribute_list(db, data_list)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@analysis_router.get("/Analysis/ReCalcCACost")
def recalc_ca_cost(db: DatabaseHelper = Depends(get_db)):
    return Result.success(analysis_service.recalc_ca_cost(db))

@analysis_router.get("/Analysis/GetShopSABFIList")
def get_shop_sabfi_list(
        ServerpartId: str = "", StatisticsMonth: str = "",
        calcSelf: bool = True,
        db: DatabaseHelper = Depends(get_db)):
    try:
        rows = analysis_service.get_shop_sabfi_list(
            db, ServerpartId=ServerpartId, StatisticsMonth=StatisticsMonth, calcSelf=calcSelf)
        ps = len(rows) or 1
        return Result.success(JsonListData.create(rows, len(rows), page_size=ps).model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopSABFIList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")

@analysis_router.post("/Analysis/SolidProfitAnalysis")
def solid_profit_analysis(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = analysis_service.solid_profit_analysis(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="固化失败")

@analysis_router.get("/Analysis/GetPeriodMonthlyList")
def get_period_monthly_list(
        StatisticsMonth: str = "", ServerpartId: str = "",
        ServerpartShopId: str = "", Business_Type: str = "",
        SettlementMode: str = "", BusinessState: str = "",
        ProjectId: str = "", ShowSelf: bool = False,
        db: DatabaseHelper = Depends(get_db)):
    try:
        rows = analysis_service.get_period_monthly_list(
            db, StatisticsMonth=StatisticsMonth, ServerpartId=ServerpartId,
            ServerpartShopId=ServerpartShopId, ProjectId=ProjectId,
            Business_Type=Business_Type, SettlementMode=SettlementMode,
            BusinessState=BusinessState, ShowSelf=ShowSelf)
        ps = len(rows) or 1
        return Result.success(JsonListData.create(rows, len(rows), page_size=ps).model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPeriodMonthlyList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")

@analysis_router.get("/Analysis/GetRevenueEstimateList")
def get_revenue_estimate_list(
        StatisticsMonth: str = "", ServerpartId: str = "",
        ProvinceName: str = "",
        db: DatabaseHelper = Depends(get_db)):
    try:
        rows = analysis_service.get_revenue_estimate_list(
            db, StatisticsMonth=StatisticsMonth, ServerpartId=ServerpartId, ProvinceName=ProvinceName)
        ps = len(rows) or 1
        return Result.success(JsonListData.create(rows, len(rows), page_size=ps).model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueEstimateList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")

@analysis_router.post("/Analysis/SolidShopSABFI")
def solid_shop_sabfi(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = analysis_service.solid_shop_sabfi(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="固化失败")

@analysis_router.post("/Analysis/SolidInvestmentAnalysis")
def solid_investment_analysis(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = analysis_service.solid_investment_analysis(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="固化失败")

@analysis_router.get("/Analysis/GetInvestmentReport")
def get_investment_report(
        ProvinceCode: str = "", ContainHoliday: int = 0,
        ServerpartId: str = "", ServerpartType: str = "",
        BusinessTrade: str = "", DueStartDate: str = "", DueEndDate: str = "",
        db: DatabaseHelper = Depends(get_db)):
    try:
        rows = analysis_service.get_investment_report(
            db, ProvinceCode=ProvinceCode, ContainHoliday=ContainHoliday,
            ServerpartId=ServerpartId)
        ps = len(rows) or 1
        return Result.success(JsonListData.create(rows, len(rows), page_size=ps).model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetInvestmentReport 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")

@analysis_router.get("/Analysis/GetNestingIAReport")
def get_nesting_ia_report(
        ProvinceCode: str = "", ContainHoliday: int = 0,
        ServerpartId: str = "", ServerpartType: str = "",
        BusinessTrade: str = "", DueStartDate: str = "", DueEndDate: str = "",
        db: DatabaseHelper = Depends(get_db)):
    try:
        rows = analysis_service.get_nesting_ia_report(
            db, ProvinceCode=ProvinceCode, ContainHoliday=ContainHoliday,
            ServerpartId=ServerpartId)
        flat_count = sum(len(n.get("children", []) or []) for n in rows)
        ps = flat_count or len(rows) or 1
        return Result.success(JsonListData.create(rows, flat_count, page_size=ps).model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetNestingIAReport 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ============================================================
# BusinessMan (26) + Supplier (13) = 39
# BS-02 整改完成: pk_val 已替换为实体专属参数名（使用 Query alias）
# ============================================================
businessman_router = APIRouter()

_BM_CRUD = {
    "BusinessMan": ["BUSINESSMAN", "Merchants"],
    "BusinessManDetail": ["BUSINESSMANDETAIL", "Merchants"],
    "Commodity": ["COMMODITY", "Merchants"],
    "CUSTOMTYPE": ["CUSTOMTYPE", "Merchants"],
    "COMMODITY_TEMP": ["COMMODITY_TEMP", "BusinessMan"],
    "Supplier": ["SUPPLIER", "Supplier"],
    "Qualification": ["QUALIFICATION", "Supplier"],
    "QUALIFICATION_HIS": ["QUALIFICATION_HIS", "Supplier"],  # 注意: C# 无 DeleteQUALIFICATION_HIS，此路由多出，不计入验收口径
}

for _name, (_ent, _prefix) in _BM_CRUD.items():
    def _make_bm(name, ent, prefix):
        # 实体专属参数名：C# 原接口格式为 {RouteName}Id
        _param_name = f"{name}Id"

        @businessman_router.post(f"/{prefix}/Get{name}List", name=f"get_{ent.lower()}_list_bm")
        def _list(search_model: dict = None, db: DatabaseHelper = Depends(get_db), _e=ent):
            try:
                if search_model is None:
                    raise Exception("未将对象引用设置到对象的实例。")
                rows, total = businessman_service.get_entity_list(db, _e, search_model)
                pi = search_model.get("PageIndex", 1)
                ps = search_model.get("PageSize", 10)
                return Result.success(JsonListData.create(rows, total, page_index=pi, page_size=ps).model_dump(), msg="查询成功")
            except Exception as ex:
                logger.error(f"Get{_e}List 查询失败: {ex}")
                return Result.fail(msg=f"查询失败{ex}")

        @businessman_router.get(f"/{prefix}/Get{name}Detail", name=f"get_{ent.lower()}_detail_bm")
        def _detail(pk_val: int = Query(..., alias=_param_name),
                    db: DatabaseHelper = Depends(get_db), _e=ent):
            try:
                return Result.success(businessman_service.get_entity_detail(db, _e, pk_val), msg="查询成功")
            except Exception as ex:
                logger.error(f"Get{_e}Detail 查询失败: {ex}")
                return Result.fail(msg=f"查询失败{ex}")

        @businessman_router.post(f"/{prefix}/Synchro{name}", name=f"synchro_{ent.lower()}_bm")
        def _synchro(data: dict, db: DatabaseHelper = Depends(get_db), _e=ent):
            try:
                ok, result = businessman_service.synchro_entity(db, _e, data)
                if ok:
                    return Result.success(result)
                return Result.fail(msg="同步失败")
            except Exception as ex:
                logger.error(f"Synchro{_e} 同步失败: {ex}")
                return Result.fail(msg=f"同步失败{ex}")

        @businessman_router.post(f"/{prefix}/Delete{name}", name=f"delete_{ent.lower()}_bm")
        def _delete(pk_val: int = Query(..., alias=_param_name),
                    db: DatabaseHelper = Depends(get_db), _e=ent):
            try:
                if businessman_service.delete_entity(db, _e, pk_val):
                    return Result.success()
                return Result.fail(msg="删除失败")
            except Exception as ex:
                logger.error(f"Delete{_e} 删除失败: {ex}")
                return Result.fail(msg=f"删除失败{ex}")
    _make_bm(_name, _ent, _prefix)

# BusinessMan/Supplier 散装
@businessman_router.post("/BusinessMan/AuthorizeQualification")
def authorize_qualification(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = businessman_service.authorize_qualification(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="授权失败")

@businessman_router.get("/Merchants/GetNestingCustomTypeLsit")
def get_nesting_custom_type(db: DatabaseHelper = Depends(get_db)):
    return Result.success(businessman_service.get_nesting_custom_type_list(db))

@businessman_router.get("/Merchants/GetCustomTypeDDL")
def get_custom_type_ddl(db: DatabaseHelper = Depends(get_db)):
    return Result.success(businessman_service.get_custom_type_ddl(db))

@businessman_router.post("/BusinessMan/CreateBusinessMan")
def create_businessman(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = businessman_service.create_businessman(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="创建失败")

@businessman_router.post("/BusinessMan/GetUserList")
def get_user_list_post(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = businessman_service.get_user_list(db, search_model)
    return Result.success(JsonListData.create(rows, total).model_dump(), msg="查询成功")

@businessman_router.get("/BusinessMan/GetUserList")
def get_user_list_get(
    BusinessManId: str = "", ProvinceCode: int = None, ServerpartId: str = "",
    ServerpartShopId: str = "", ValidState: int = None,
    SearchName: str = "", SearchValue: str = "",
    db: DatabaseHelper = Depends(get_db)):
    """获取经营单位账号列表 — C# GET 重载"""
    rows, total = businessman_service.get_user_list(db, {
        "BusinessManId": BusinessManId, "ProvinceCode": ProvinceCode,
        "ServerpartId": ServerpartId, "ServerpartShopId": ServerpartShopId,
        "ValidState": ValidState, "SearchName": SearchName, "SearchValue": SearchValue,
    })
    return Result.success(JsonListData.create(rows, total).model_dump(), msg="查询成功")

@businessman_router.post("/Supplier/GetSupplierTreeList")
def get_supplier_tree_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = businessman_service.get_supplier_tree_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@businessman_router.post("/Supplier/RelateBusinessCommodity")
def relate_business_commodity(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = businessman_service.relate_business_commodity(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)


# ============================================================
# DataVerification (23) + Sales (13) = 36
# ============================================================
verification_router = APIRouter()

@verification_router.get("/Verification/GetENDACCOUNTModel")
def get_endaccount_model(ServerpartShopId: str = "", StatisticsDate: str = "", db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_endaccount_model(db, ServerpartShopId=ServerpartShopId, StatisticsDate=StatisticsDate))

@verification_router.post("/Verification/SynchroENDACCOUNT")
def synchro_endaccount(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = verification_service.synchro_endaccount(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

@verification_router.post("/Verification/DeleteENDACCOUNT")
def delete_endaccount(ENDACCOUNTId: int, db: DatabaseHelper = Depends(get_db)):
    if verification_service.delete_endaccount(db, ENDACCOUNTId):
        return Result.success()
    return Result.fail(msg="删除失败")

@verification_router.post("/Verification/GetEndaccountList")
def get_endaccount_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = verification_service.get_endaccount_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@verification_router.post("/Verification/GetEndaccountDetail")
def get_endaccount_detail(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = verification_service.get_endaccount_detail(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@verification_router.post("/Verification/VerifyEndaccount")
def verify_endaccount(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.verify_endaccount(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.post("/Verification/ApproveEndaccount")
def approve_endaccount(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.approve_endaccount(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.post("/Verification/SubmitEndaccountState")
def submit_endaccount_state(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = verification_service.submit_endaccount_state(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="提交失败")

@verification_router.post("/Verification/GetEndaccountHisList")
def get_endaccount_his_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = verification_service.get_endaccount_his_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@verification_router.get("/Verification/GetSuppEndaccountList")
def get_supp_endaccount_list(
        ServerpartIds: str = "", ServerpartCode: str = "",
        ServerpartShopCode: str = "", StartDate: str = "", EndDate: str = "",
        EndaccountState: int = None, PageIndex: int = 1, PageSize: int = 10,
        SortStr: str = "", db: DatabaseHelper = Depends(get_db)):
    rows, total = verification_service.get_supp_endaccount_list(db,
        ServerpartIds=ServerpartIds, ServerpartCode=ServerpartCode,
        ServerpartShopCode=ServerpartShopCode, StartDate=StartDate, EndDate=EndDate,
        EndaccountState=EndaccountState, PageIndex=PageIndex, PageSize=PageSize, SortStr=SortStr)

    # C# 在每条记录上附加搜索回显字段 + 日期格式转换 + 排除多出字段
    exclude_fields = {"BUSINESS_TYPE", "SHOPSHORTNAME"}
    date_fields = {"ENDACCOUNT_DATE", "STATISTICS_DATE", "OPERATE_DATE", "AUDIT_DATE"}
    for row in rows:
        # 搜索回显（C# 中回显字段值为 null）
        row["SERVERPARTCODES"] = None
        row["SERVERPART_IDS"] = None
        row["SearchStartDate"] = None
        row["SearchEndDate"] = None
        row["SearchStatisticsStartDate"] = None
        row["SearchStatisticsEndDate"] = None
        # 排除多出字段
        for f in exclude_fields:
            row.pop(f, None)
        # 日期格式转换: ISO → yyyy/MM/dd HH:mm:ss
        for f in date_fields:
            v = row.get(f)
            if v and isinstance(v, str) and "T" in v:
                row[f] = v.replace("T", " ").replace("-", "/")

    # C# 用 JsonList.Success() 仅含 List/TotalCount/PageIndex/PageSize，无 OtherData/StaticsModel
    return Result.success(
        data={"List": rows, "TotalCount": total, "PageIndex": PageIndex, "PageSize": PageSize},
        msg="查询成功")

@verification_router.post("/Verification/ApplyEndaccountInvalid")
def apply_endaccount_invalid(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.apply_endaccount_invalid(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.post("/Verification/CancelEndaccount")
def cancel_endaccount(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.cancel_endaccount(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.get("/Verification/GetDataVerificationList")
def get_data_verification_list(
        RoleType: int = 1, ProvinceCode: int = 0, ServerpartId: str = "",
        StartDate: str = "", EndDate: str = "", Business_Type: str = "",
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_data_verification_list(db,
        RoleType=RoleType, ProvinceCode=ProvinceCode, ServerpartId=ServerpartId,
        StartDate=StartDate, EndDate=EndDate, Business_Type=Business_Type))

@verification_router.get("/Verification/GetShopEndaccountSum")
def get_shop_endaccount_sum(
        RoleType: int = 1, ServerpartId: int = 0,
        ServerpartShopCode: str = "", StartDate: str = "", EndDate: str = "",
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_shop_endaccount_sum(db,
        RoleType=RoleType, ServerpartId=ServerpartId,
        ServerpartShopCode=ServerpartShopCode, StartDate=StartDate, EndDate=EndDate),
        msg="查询成功")

@verification_router.get("/Verification/GetEndAccountData")
def get_endaccount_data(
        Data_Type: int = 0, Endaccount_ID: int = 0,
        CigaretteType: str = "", ReloadType: int = None,
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_endaccount_data(db,
        Data_Type=Data_Type, Endaccount_ID=Endaccount_ID,
        CigaretteType=CigaretteType, ReloadType=ReloadType))

@verification_router.get("/Verification/GetCommoditySaleList")
def get_commodity_sale_list_v(
        ServerpartCode: str = "", ShopCode: str = "", MachineCode: str = "",
        StartDate: str = "", EndDate: str = "", CommodityTypeId: str = "",
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_commodity_sale_list_v(db,
        ServerpartCode=ServerpartCode, ShopCode=ShopCode, MachineCode=MachineCode,
        StartDate=StartDate, EndDate=EndDate, CommodityTypeId=CommodityTypeId))

@verification_router.get("/Verification/GetMobilePayDataList")
def get_mobilepay_data_list(
        ExceptionType: int = 0, ServerpartCode: str = "", ShopCode: str = "",
        MachineCode: str = "", StartDate: str = "", EndDate: str = "",
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_mobilepay_data_list(db,
        ExceptionType=ExceptionType, ServerpartCode=ServerpartCode, ShopCode=ShopCode,
        MachineCode=MachineCode, StartDate=StartDate, EndDate=EndDate))

@verification_router.get("/Verification/GetEndaccountSupplement")
def get_endaccount_supplement(
        EndaccountId: int = 0, Revenue_Amount: float = 0,
        FactAmount_Mobilepayment: float = 0,
        db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.get_endaccount_supplement(db,
        EndaccountId=EndaccountId, Revenue_Amount=Revenue_Amount,
        FactAmount_Mobilepayment=FactAmount_Mobilepayment))

@verification_router.post("/Verification/SaveCorrectData")
def save_correct_data(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.save_correct_data(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.post("/Verification/SaveSaleSupplement")
def save_sale_supplement(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.save_sale_supplement(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.post("/Verification/ExceptionHandling")
def exception_handling(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, msg = verification_service.exception_handling(db, data)
    if ok:
        return Result.success()
    return Result.fail(msg=msg)

@verification_router.get("/Verification/RebuildDailyAccount")
def rebuild_daily_account(db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.rebuild_daily_account(db))

@verification_router.get("/Verification/CorrectDailyEndaccount")
def correct_daily_endaccount(db: DatabaseHelper = Depends(get_db)):
    return Result.success(verification_service.correct_daily_endaccount(db))

# Sales CRUD
@verification_router.post("/Sales/GetCOMMODITYSALEList")
def sales_get_list(search_model: dict = None, db: DatabaseHelper = Depends(get_db)):
    if search_model is None:
        return Result.fail(msg="查询失败未将对象引用设置到对象的实例。")
    rows, total = verification_service.get_entity_list(db, "COMMODITYSALE", search_model)
    return Result.success(JsonListData.create(rows, total), msg="查询成功")

@verification_router.get("/Sales/GetCOMMODITYSALEDetail")
def sales_get_detail(request: Request, COMMODITYSALEId: int = None, db: DatabaseHelper = Depends(get_db)):
    if COMMODITYSALEId is None:
        return {"Message": f'找不到与请求 URI\u201c{request.url}\u201d匹配的 HTTP 资源。'}
    return Result.success(verification_service.get_entity_detail(db, "COMMODITYSALE", COMMODITYSALEId), msg="查询成功")

@verification_router.post("/Sales/SynchroCOMMODITYSALE")
def sales_synchro(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = verification_service.synchro_entity(db, "COMMODITYSALE", data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

@verification_router.post("/Sales/DeleteCOMMODITYSALE")
def sales_delete(COMMODITYSALEId: int, db: DatabaseHelper = Depends(get_db)):
    if verification_service.delete_entity(db, "COMMODITYSALE", COMMODITYSALEId):
        return Result.success()
    return Result.fail(msg="删除失败")

# Sales 散装 — SA-02 深逻辑回迁
@verification_router.post("/Sales/GetEndaccountSaleInfo")
def get_endaccount_sale_info(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    """获取账期单品数据（C# EndaccountHelper.GetEndaccountSaleInfo）"""
    result = verification_service.get_endaccount_sale_info(db, **search_model)
    return Result.success(result)

@verification_router.post("/Sales/RecordSaleData")
def record_sale_data(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = verification_service.record_sale_data(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg=result)

@verification_router.post("/Sales/GetEndaccountError")
def get_endaccount_error(search_model: dict = None, db: DatabaseHelper = Depends(get_db)):
    if search_model is None:
        return Result.fail(msg="处理失败未将对象引用设置到对象的实例。")
    rows, total = verification_service.get_endaccount_error(db, search_model)
    return Result.success(JsonListData.create(rows, total), msg="查询成功")

@verification_router.post("/Sales/UpdateEndaccountError")
def update_endaccount_error(data: dict, db: DatabaseHelper = Depends(get_db)):
    eid = int(data.get("ENDACCOUNT_ID", 0))
    diff = float(data.get("amountdiffer", 0))
    ok, result = verification_service.update_endaccount_error(db, eid, diff)
    if ok:
        return Result.success(msg=result)
    return Result.fail(msg=result)

@verification_router.post("/Sales/GetCommoditySaleSummary")
def get_commodity_sale_summary(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    data, total, *extra = verification_service.get_commodity_sale_summary(db, **search_model)
    statics = extra[0] if extra else {}
    return Result.success(JsonListData.create(data, total, statics_model=statics))

@verification_router.post("/Sales/GetCommodityTypeSummary")
def get_commodity_type_summary(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    data, total, *extra = verification_service.get_commodity_type_summary(db, **search_model)
    statics = extra[0] if extra else {}
    return Result.success(JsonListData.create(data, total, statics_model=statics))

@verification_router.post("/Sales/GetCommodityTypeHistory")
def get_commodity_type_history(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    data, total, *extra = verification_service.get_commodity_type_history(db, **search_model)
    statics = extra[0] if extra else {}
    return Result.success(JsonListData.create(data, total, statics_model=statics))

@verification_router.post("/Sales/SaleRank")
def sale_rank(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    data, total, *extra = verification_service.sale_rank(db, **search_model)
    statics = extra[0] if extra else {}
    return Result.success(JsonListData.create(data, total, statics_model=statics))

@verification_router.post("/Sales/UpdateCommoditySale")
def update_commodity_sale(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = verification_service.update_commodity_sale(db, **data)
    if ok:
        return Result.success(msg=result)
    return Result.fail(msg=result)


# ============================================================
# Picture (9)
# ============================================================
picture_router = APIRouter()

@picture_router.post("/Picture/GetPictureList")
def get_picture_list(search_model: dict, db: DatabaseHelper = Depends(get_db)):
    rows, total = picture_service.get_picture_list(db, search_model)
    return Result.success(JsonListData.create(rows, total))

@picture_router.get("/Picture/GetPictureDetail")
def get_picture_detail(PictureId: int, db: DatabaseHelper = Depends(get_db)):
    return Result.success(picture_service.get_picture_detail(db, PictureId))

@picture_router.post("/Picture/SynchroPicture")
def synchro_picture(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = picture_service.synchro_picture(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="同步失败")

@picture_router.post("/Picture/DeletePicture")
def delete_picture(PictureId: int, db: DatabaseHelper = Depends(get_db)):
    if picture_service.delete_picture(db, PictureId):
        return Result.success()
    return Result.fail(msg="删除失败")

@picture_router.post("/Picture/UploadPicture")
def upload_picture(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = picture_service.upload_picture(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="上传失败")

@picture_router.get("/Picture/GetPictureTypeList")
def get_picture_type_list(db: DatabaseHelper = Depends(get_db)):
    return Result.success(picture_service.get_picture_type_list(db))

@picture_router.get("/Picture/GetPictureByShop")
def get_picture_by_shop(ShopId: str = "", PictureType: str = "", db: DatabaseHelper = Depends(get_db)):
    return Result.success(picture_service.get_picture_by_shop(db, ShopId, PictureType))

@picture_router.get("/Picture/GetPictureCount")
def get_picture_count(db: DatabaseHelper = Depends(get_db)):
    return Result.success(picture_service.get_picture_count(db))

@picture_router.post("/Picture/BatchDeletePicture")
async def batch_delete_picture(request: Request, db: DatabaseHelper = Depends(get_db)):
    ids = await request.json()
    ok, msg = picture_service.batch_delete_picture(db, ids if isinstance(ids, list) else [])
    if ok:
        return Result.success()
    return Result.fail(msg=msg)


# PI-02 补齐：C# PictureController 原有路由
@picture_router.api_route("/Picture/GetEndaccountEvidence", methods=["GET", "POST"])
def get_endaccount_evidence(EndaccountId: int, db: DatabaseHelper = Depends(get_db)):
    rows, total = picture_service.get_endaccount_evidence(db, EndaccountId)
    return Result.success(JsonListData.create(rows, total))


@picture_router.post("/Picture/UploadEndaccountEvidence")
def upload_endaccount_evidence(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = picture_service.upload_endaccount_evidence(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="上传失败")


@picture_router.api_route("/Picture/GetAuditEvidence", methods=["GET", "POST"])
def get_audit_evidence(AuditId: int, db: DatabaseHelper = Depends(get_db)):
    rows, total = picture_service.get_audit_evidence(db, AuditId)
    return Result.success(JsonListData.create(rows, total))


@picture_router.post("/Picture/UploadAuditEvidence")
def upload_audit_evidence(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = picture_service.upload_audit_evidence(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="上传失败")


@picture_router.post("/Picture/SaveImgFile")
def save_img_file(data: dict, db: DatabaseHelper = Depends(get_db)):
    ok, result = picture_service.save_img_file(db, data)
    if ok:
        return Result.success(result)
    return Result.fail(msg="保存失败")


@picture_router.post("/Picture/DeleteMultiPicture")
async def delete_multi_picture(request: Request, db: DatabaseHelper = Depends(get_db)):
    data = await request.json()
    ok, msg = picture_service.delete_multi_picture(db, data if isinstance(data, list) else [])
    if ok:
        return Result.success(msg="删除成功")
    return Result.fail(msg=msg)
