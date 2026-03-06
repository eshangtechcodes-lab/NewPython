# -*- coding: utf-8 -*-
"""
CommercialApi - Revenue 路由
对应原 CommercialApi/Controllers/RevenueController.cs
营收相关接口（原2657行，40+接口，此处按方法签名完整定义路由）
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


# ===== 每日营收推送 =====
@router.get("/Revenue/GetRevenuePushList")
async def get_revenue_push_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收(0否1是)"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收推送数据表列表"""
    logger.warning("GetRevenuePushList 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


@router.get("/Revenue/GetSummaryRevenue")
async def get_summary_revenue(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_StartDate: Optional[str] = Query("", description="统计开始日期"),
    Statistics_Date: Optional[str] = Query("", description="统计结束日期"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    ShowYearRevenue: bool = Query(False, description="是否显示年度营收额"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收推送汇总数据"""
    logger.warning("GetSummaryRevenue 暂未完整实现")
    _push = {
        "AccountRoyaltyQOQ": None, "BudgetRevenue": None,
        "BusinessBrand_Name": None, "BusinessTrade_Name": None,
        "BusinessType": None, "Business_TypeName": None,
        "CashPay": None, "CurAccountRoyalty": None,
        "Different_Price_Less": None, "Different_Price_More": None,
        "MobilePayment": None, "RevenueQOQ": None, "RevenueYOY": None,
        "Revenue_Include": None, "Revenue_Upload": None,
        "SPRegionType_Name": None, "Serverpart_ID": None, "Serverpart_Name": None,
        "ShopName": None, "ShopRegionName": None, "Statistics_Date": None,
        "TicketCount": None, "TotalCount": None, "TotalOffAmount": None,
        "TotalShopCount": None, "UnUpLoadShopList": None,
        "YearAccountRoyalty": None, "YearAccountRoyaltyYOY": None,
        "YearRevenueAmount": None, "YearRevenueYOY": None,
    }
    _ckm = {"data": None, "key": None, "name": None, "value": None}
    _nv = {"name": None, "value": None}
    return Result.success(data={
        "BusinessTradeList": [_nv], "BusinessTypeList": [_ckm],
        "GrowthRate": None, "MonthRevenueAmount": None,
        "RevenuePushModel": _push,
        "SPRegionList": [_nv], "YearRevenueAmount": None,
    }, msg="查询成功")


@router.get("/Revenue/GetSummaryRevenueMonth")
async def get_summary_revenue_month(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    SolidType: int = Query(0, description="是否执行固化操作"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度营收推送汇总数据"""
    logger.warning("GetSummaryRevenueMonth 暂未完整实现")
    _month = {
        "AccountRoyaltyQOQ": None, "BudgetRevenue": None,
        "BusinessBrand_Name": None, "BusinessTrade_Name": None,
        "BusinessType": None, "Business_TypeName": None,
        "CashPay": None,
        "CurAccountRoyalty": {"Royalty_Price": None, "Royalty_Theory": None, "SubRoyalty_Price": None, "SubRoyalty_Theory": None},
        "Different_Price_Less": None, "Different_Price_More": None,
        "MobilePayment": None, "RevenueQOQ": None, "RevenueYOY": None,
        "Revenue_Include": None, "Revenue_Upload": None,
        "SPRegionType_Name": None, "Serverpart_ID": None, "Serverpart_Name": None,
        "ShopName": None, "ShopRegionName": None, "Statistics_Date": None,
        "TicketCount": None, "TotalCount": None, "TotalOffAmount": None,
        "TotalShopCount": None, "UnUpLoadShopList": None,
        "YearAccountRoyalty": None, "YearAccountRoyaltyYOY": None,
        "YearRevenueAmount": None, "YearRevenueYOY": None,
    }
    _ckm2 = {"data": None, "key": None, "name": None, "value": None}
    return Result.success(data={
        "BusinessTradeList": None, "BusinessTypeList": [_ckm2],
        "GrowthRate": None, "MonthRevenueModel": _month,
        "RevenuePushModel": None, "SPRegionList": None,
    }, msg="查询成功")


@router.get("/Revenue/GetWechatPushSalesList")
async def get_wechat_push_sales_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    RankNum: int = Query(100, description="显示单品行数"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收推送单品销售排行【甘肃】"""
    logger.warning("GetWechatPushSalesList 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


@router.get("/Revenue/GetUnUpLoadShops")
async def get_un_upload_shops(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询服务区未上传结账信息的门店列表"""
    try:
        from datetime import datetime as dt

        # 确定使用 T_ENDACCOUNT 还是 T_ENDACCOUNT_TEMP
        stat_date = Statistics_Date or dt.now().strftime("%Y-%m-%d")
        stat_dt = dt.strptime(stat_date.split(" ")[0], "%Y-%m-%d")
        table_suffix = "" if stat_dt < dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - __import__("datetime").timedelta(days=9) else "_TEMP"

        # 省份条件
        where_sql = ""
        if Serverpart_ID:
            where_sql += f' AND B."SERVERPART_ID" = {Serverpart_ID}'
        elif SPRegionType_ID:
            where_sql += f' AND B."SPREGIONTYPE_ID" = {SPRegionType_ID}'
        elif pushProvinceCode:
            fe_rows = db.execute_query(
                """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
                {"pc": pushProvinceCode})
            if fe_rows:
                where_sql += f' AND B."PROVINCE_CODE" = {fe_rows[0]["FIELDENUM_ID"]}'
        if Revenue_Include == 1:
            where_sql += f' AND A."REVENUE_INCLUDE" = 1'

        date_str = stat_date.split(" ")[0]

        sql = f"""SELECT B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX", B."SERVERPART_CODE",
                A."SERVERPARTSHOP_ID", A."SHOPREGION", A."SHOPTRADE", A."SHOPCODE", A."SHOPNAME"
            FROM "T_SERVERPARTSHOP" A, "T_SERVERPART" B
            WHERE COALESCE(A."BUSINESS_DATE", TO_DATE('{date_str}','YYYY-MM-DD')) < TO_DATE('{date_str}','YYYY-MM-DD') + 1
                AND COALESCE(A."BUSINESS_ENDDATE", TO_DATE('{date_str}','YYYY-MM-DD')) >= TO_DATE('{date_str}','YYYY-MM-DD')
                AND COALESCE(A."STATISTIC_TYPE", 1000) = 1000
                AND COALESCE(A."BUSINESS_STATE", 1000) = 1000
                AND A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."SHOPTRADE" NOT IN ('9032','9999')
                AND A."ISVALID" = 1
                AND NOT EXISTS (SELECT 1 FROM "T_ENDACCOUNT{table_suffix}" C
                    WHERE A."SERVERPART_ID" = C."SERVERPART_ID" AND A."SHOPCODE" = C."SHOPCODE"
                        AND C."VALID" = 1 AND TRUNC(C."STATISTICS_DATE") = TO_DATE('{date_str}','YYYY-MM-DD')){where_sql}
            UNION ALL
            SELECT B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX", B."SERVERPART_CODE",
                A."SERVERPARTSHOP_ID", A."SHOPREGION", A."SHOPTRADE", A."SHOPCODE", A."SHOPNAME"
            FROM "T_SERVERPARTSHOP" A, "T_SERVERPART" B
            WHERE COALESCE(A."STATISTIC_TYPE", 1000) = 1000
                AND COALESCE(A."BUSINESS_STATE", 1000) = 1000
                AND A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."SHOPTRADE" NOT IN ('9032','9999')
                AND A."ISVALID" = 1
                AND EXISTS (SELECT 1 FROM "T_ENDACCOUNT{table_suffix}" C
                    WHERE A."SERVERPART_ID" = C."SERVERPART_ID" AND A."SHOPCODE" = C."SHOPCODE"
                        AND C."VALID" = 1 AND TRUNC(C."STATISTICS_DATE") = TO_DATE('{date_str}','YYYY-MM-DD')
                        AND C."DIFFERENCE_REASON" = '无结账信息' AND C."CASHPAY" = 0){where_sql}"""

        rows = db.execute_query(sql)
        result_list = []
        for r in rows:
            result_list.append({
                "Serverpart_ID": r.get("SERVERPART_ID"),
                "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                "ServerpartShop_ID": r.get("SERVERPARTSHOP_ID"),
                "ServerpartShop_Name": r.get("SHOPNAME", ""),
                "Statistics_Date": stat_date,
            })
        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetUnUpLoadShops 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetServerpartBrand")
async def get_serverpart_brand(
    Serverpart_Id: Optional[int] = Query(None, description="服务区内码"),
    statictics_Time: Optional[str] = Query(None, description="统计时间"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编号"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区品牌营收"""
    logger.warning("GetServerpartBrand 暂未完整实现")
    return Result.success(data={
        "Revenue_Amount": None,
        "Serverpart_Id": Serverpart_Id,
        "Serverpart_Name": None,
        "listBusinessModel": [],
        "listCurBusinessModel": [],
    }, msg="查询成功")


# ===== 结账数据 =====
@router.get("/Revenue/GetServerpartEndAccountList")
async def get_serverpart_end_account_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询服务区结账数据列表"""
    logger.warning("GetServerpartEndAccountList 暂未完整实现")
    return Result.success(data={
        "Revenue_Amount": None,
        "Serverpart_Id": Serverpart_ID,
        "Serverpart_Name": None,
        "ShopEndaccountList": [],
        "TotalShopCount": 0,
        "UploadShopCount": 0,
    }, msg="查询成功")


@router.get("/Revenue/GetShopEndAccountList")
async def get_shop_end_account_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    ServerpartShop_Ids: Optional[str] = Query(None, description="门店内码集合"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询门店结账数据列表"""
    logger.warning("GetShopEndAccountList 暂未完整实现")
    return Result.success(data={
        "BrandType_Name": None,
        "Brand_ICO": None,
        "Brand_Id": None,
        "Brand_Name": None,
        "Business_Trade": None,
        "Business_TradeICO": None,
        "Business_TradeId": None,
        "Bussiness_Name": None,
        "Bussiness_State": None,
        "Bussiness_Time": None,
        "CurRevenue": None,
        "Revenue_Amount": None,
        "ServerpartShop_Id": None,
        "ShopEndaccountList": [],
    }, msg="查询成功")


# ===== 预算费用 =====
@router.post("/Revenue/GetBudgetExpenseList")
async def get_budget_expense_list_post(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取预算费用表列表（POST）"""
    try:
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        search_param = searchModel.get("SearchParameter") or {}

        conditions = []
        params = []

        # 通用字段过滤
        for field in ["STATISTICS_MONTH", "PROVINCE_CODE", "SERVERPART_ID"]:
            val = search_param.get(field)
            if val is not None and str(val).strip():
                conditions.append(f'"{field}" = ?')
                params.append(val)

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        # 查询总数
        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_BUDGETEXPENSE"{where_sql}'
        count_rows = db.execute_query(count_sql, params if params else None)
        total = count_rows[0]["CNT"] if count_rows else 0

        # 分页查询
        offset = (page_index - 1) * page_size
        data_sql = f'SELECT * FROM "T_BUDGETEXPENSE"{where_sql} ORDER BY "BUDGETEXPENSE_ID" DESC LIMIT ? OFFSET ?'
        page_params = (params if params else []) + [page_size, offset]
        page_rows = db.execute_query(data_sql, page_params)

        # 格式化日期
        for r in page_rows:
            if r.get("OPERATE_DATE"):
                r["OPERATE_DATE"] = str(r["OPERATE_DATE"])

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetExpenseList POST 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



@router.get("/Revenue/GetBudgetExpenseList")
async def get_budget_expense_list_get(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Month: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取预算费用表列表（GET）"""
    logger.warning("GetBudgetExpenseList GET 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


# ===== 计划营收 =====
@router.get("/Revenue/GetRevenueBudget")
async def get_revenue_budget(
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取计划营收数据"""
    logger.warning("GetRevenueBudget 暂未完整实现")
    return Result.fail(code=101, msg="查询失败，未录入预算数据！")


@router.get("/Revenue/GetProvinceRevenueBudget")
async def get_province_revenue_budget(
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsType: int = Query(1, description="统计类型"),
    SPRegionTypeID: Optional[int] = Query(None, description="片区内码"),
    ServerpartID: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeYear: bool = Query(False, description="是否显示全年计划营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取全省计划营收分析"""
    logger.warning("GetProvinceRevenueBudget 暂未完整实现")
    return Result.fail(code=101, msg="查询失败，无数据返回！")


# ===== 支付/配送 =====
@router.get("/Revenue/GetMobileShare")
async def get_mobile_share(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取移动支付分账数据"""
    logger.warning("GetMobileShare 暂未完整实现")
    return Result.success(data={
        "Account_Price": None, "MonthRoyalty_Price": None,
        "RoyaltyGrowth_Price": None, "Royalty_Price": None,
        "Serverpart_ID": None, "Serverpart_Name": None,
        "ShareShopGrowth_Count": None, "ShareShop_Count": None,
        "Statistics_Date": None, "SubRoyalty_Price": None,
        "Ticket_Fee": None, "Ticket_Price": None,
    }, msg="查询成功")


@router.get("/Revenue/GetMallDeliver")
async def get_mall_deliver(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商城配送数据"""
    logger.warning("GetMallDeliver 暂未完整实现")
    return Result.success(data={
        "DeliverBillGrowth_Count": None, "DeliverBill_Count": None,
        "DeliverGrowth_Price": None, "Deliver_Price": None,
        "Deliver_Rate": None, "MonthDeliver_Price": None,
        "Statistics_Date": None,
    }, msg="查询成功")


# ===== 客单交易分析 =====
@router.get("/Revenue/GetTransactionAnalysis")
async def get_transaction_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    ShowConsumptionLevel: bool = Query(False, description="是否显示消费水平占比"),
    ShowConvertRate: bool = Query(False, description="是否显示消费转化率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区客单交易分析"""
    logger.warning("GetTransactionAnalysis 暂未完整实现")
    return Result.success(data={
        "AvgRevenueAmount": None, "AvgTicketPrice": None, "AvgVehicleAmount": None,
        "ConvertRate": None, "ConvertProvinceRate": None,
        "MonthAvgTicketPrice": None, "MonthVehicleAmount": None, "MonthVehicleCount": None,
        "ProvinceAvgTicketPrice": None, "ProvinceRevenueAmount": None,
        "RevenueAmount": None, "SPRegionType_Name": None,
        "Serverpart_ID": None, "Serverpart_Name": None,
        "Statistics_Date": None, "TicketAvgCount": None, "TicketCount": None,
        "TicketProvinceCount": None, "TotalAvgCount": None, "TotalCount": None,
        "TotalProvinceCount": None, "VehicleCount": None, "transactionLevel": None,
    }, msg="查询成功")


@router.get("/Revenue/GetTransactionTimeAnalysis")
async def get_transaction_time_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区时段消费分析"""
    logger.warning("GetTransactionTimeAnalysis 暂未完整实现")
    return Result.fail(code=101, msg="查询失败，无数据返回！")


@router.get("/Revenue/GetTransactionConvert")
async def get_transaction_convert(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取消费转化对比分析"""
    logger.warning("GetTransactionConvert 暂未完整实现")
    return Result.success(data={
        "BayonetList": {"data": None, "name": None, "value": None, "CommonScatterList": None},
        "TransactionList": {"data": None, "name": None, "value": None, "CommonScatterList": None},
    }, msg="查询成功")


# ===== 业态分析 =====
@router.get("/Revenue/GetBusinessTradeRevenue")
async def get_business_trade_revenue(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    BusinessTradeIds: Optional[str] = Query("", description="经营业态内码"),
    DataType: int = Query(1, description="数据类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态营收占比"""
    # 从Header获取省份编码（页面权限验证来源）
    if not ProvinceCode:
        ProvinceCode = request.headers.get("ProvinceCode", "")
    logger.warning("GetBusinessTradeRevenue 暂未完整实现")
    _ckm = {"data": None, "key": None, "name": None, "value": None}
    return Result.success(data={
        "Abundant": None, "Rigid_Demand": None,
        "SPRegionType_Name": None, "Serverpart_ID": None, "Serverpart_Name": None,
        "BusinessTradeRank": [_ckm],
    }, msg="查询成功")


@router.get("/Revenue/GetBusinessTradeLevel")
async def get_business_trade_level(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeTrade: bool = Query(True, description="是否显示全部业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态消费水平占比"""
    if not ProvinceCode:
        ProvinceCode = request.headers.get("ProvinceCode", "")
    logger.warning("GetBusinessTradeLevel 暂未完整实现")
    _ckm2 = {"data": None, "key": None, "name": None, "value": None}
    return Result.success(data={
        "ColumnList": [_ckm2], "legend": None,
    }, msg="查询成功")


@router.get("/Revenue/GetBusinessBrandLevel")
async def get_business_brand_level(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeTrade: bool = Query(True, description="是否显示全部业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取品牌消费水平占比"""
    if not ProvinceCode:
        ProvinceCode = request.headers.get("ProvinceCode", "")
    logger.warning("GetBusinessBrandLevel 暂未完整实现")
    _ckm3 = {"data": None, "key": None, "name": None, "value": None}
    return Result.success(data={
        "ColumnList": [_ckm3], "legend": None,
    }, msg="查询成功")


# ===== 营收趋势 =====
# 注意：C# 中有两个 GetRevenueTrend，一个路由到 GetRevenueCompare(GET)，一个路由到 GetRevenueTrend(GET)
# 这里只保留 GetRevenueTrend 的 GET 版本（下方已有 GET 定义）


@router.get("/Revenue/GetRevenueTrend")
async def get_revenue_trend_get(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsType: int = Query(1, description="统计类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收趋势图（GET）"""
    if not ProvinceCode:
        ProvinceCode = request.headers.get("ProvinceCode", "")
    logger.warning("GetRevenueTrend GET 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


# ===== 经营报表 =====
@router.get("/Revenue/GetRevenueReport")
async def get_revenue_report(
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    startTime: Optional[str] = Query(None, description="开始时间"),
    endTime: Optional[str] = Query(None, description="结束时间"),
    SearchKeyType: Optional[str] = Query("", description="查询类型"),
    SearchKeyValue: Optional[str] = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区经营报表"""
    try:
        from datetime import datetime as dt
        # 获取省份对应的FieldEnum_ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": provinceCode})
        if not fe_rows:
            return Result.fail(code=200, msg="查询失败，无数数据返回！")
        province_id = fe_rows[0]["FIELDENUM_ID"]

        # 构建 WHERE 条件
        where_parts = [
            'A."SERVERPART_ID" = B."SERVERPART_ID"',
            'A."REVENUEDAILY_STATE" = 1',
            'B."STATISTIC_TYPE" = 1000',
            'B."STATISTICS_TYPE" = 1000',
            f'B."PROVINCE_CODE" = {province_id}',
        ]
        params = {}
        if startTime:
            sd = dt.strptime(startTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in startTime else startTime
            where_parts.append(f'A."STATISTICS_DATE" >= {sd}')
        if endTime:
            ed = dt.strptime(endTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in endTime else endTime
            where_parts.append(f'A."STATISTICS_DATE" <= {ed}')

        where_sql = " AND ".join(where_parts)

        sql = f"""SELECT B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX",
                B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAY_AMOUNT",
                SUM(A."CASHPAY_AMOUNT") AS "CASHPAY_AMOUNT",
                SUM(A."OTHERPAY_AMOUNT") AS "OTHERPAY_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT",
                SUM(A."TOTAL_COUNT") AS "TOTAL_COUNT",
                SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFF_AMOUNT",
                SUM(A."DIFFERENT_AMOUNT") AS "DIFFERENT_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE {where_sql}
            GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX",
                B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX"
            ORDER BY B."SPREGIONTYPE_INDEX", B."SPREGIONTYPE_ID", B."SERVERPART_INDEX", B."SERVERPART_CODE" """

        rows = db.execute_query(sql, params)
        if not rows:
            return Result.fail(code=200, msg="查询失败，无数数据返回！")

        # 汇总总营收
        total_revenue = round(sum(float(r.get("REVENUE_AMOUNT") or 0) for r in rows), 2)
        total_ticket = sum(int(r.get("TICKET_COUNT") or 0) for r in rows)
        total_count = round(sum(float(r.get("TOTAL_COUNT") or 0) for r in rows), 2)
        total_off = round(sum(float(r.get("TOTALOFF_AMOUNT") or 0) for r in rows), 2)
        total_diff = round(sum(float(r.get("DIFFERENT_AMOUNT") or 0) for r in rows), 2)

        # 按片区分组
        region_map = {}
        for r in rows:
            rid = r.get("SPREGIONTYPE_ID") or "null"
            if rid not in region_map:
                region_map[rid] = {
                    "Region_Name": r.get("SPREGIONTYPE_NAME") or "无管理中心",
                    "Total_Revenue": 0,
                    "Revenue_Proportion": "",
                    "revenueServerModels": [],
                }
            region_map[rid]["Total_Revenue"] += float(r.get("REVENUE_AMOUNT") or 0)

            # 添加服务区
            sp_revenue = float(r.get("REVENUE_AMOUNT") or 0)
            region_rev = region_map[rid]["Total_Revenue"]
            prop = f"{sp_revenue / region_rev * 100:.2f}%" if region_rev != 0 else ""
            region_map[rid]["revenueServerModels"].append({
                "Serverpart_Id": str(r.get("SERVERPART_ID", "")),
                "Serverpart_Name": r.get("SERVERPART_NAME", ""),
                "Total_Revenue": sp_revenue,
                "Province_Code": provinceCode,
                "Revenue_Proportion": prop,
            })

        # 重新计算片区占比和服务区占比
        region_list = []
        for rid, region in region_map.items():
            region["Revenue_Proportion"] = f"{region['Total_Revenue'] / total_revenue * 100:.2f}%" if total_revenue != 0 else ""
            # 重新计算服务区占比
            for sp in region["revenueServerModels"]:
                sp["Revenue_Proportion"] = f"{sp['Total_Revenue'] / region['Total_Revenue'] * 100:.2f}%" if region['Total_Revenue'] != 0 else ""
            # 按营收倒序排列服务区
            region["revenueServerModels"].sort(key=lambda x: x["Total_Revenue"], reverse=True)
            region_list.append(region)
        # 按营收倒序排列片区
        region_list.sort(key=lambda x: x["Total_Revenue"], reverse=True)

        result = {
            "Total_Revenue": total_revenue,
            "TicketCount": total_ticket,
            "TotalCount": total_count,
            "TotalOffAmount": total_off,
            "Different_Price_Less": 0,
            "Different_Price_More": 0,
            "MobilePayment": None,
            "Province_InsideAmount": total_revenue,
            "Province_ExternalAmount": None,
            "Revenue_AmountN": None,
            "Revenue_AmountS": None,
            "SearchResult": None,
            "revenueRegionModels": region_list,
            "revenueInsideRegionModels": None,
        }

        return Result.success(data=result, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueReport 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetRevenueReportDetil")
async def get_revenue_report_detail(
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartShopId: Optional[int] = Query(None, description="门店内码"),
    startTime: Optional[str] = Query(None, description="开始时间"),
    endTime: Optional[str] = Query(None, description="结束时间"),
    SearchKeyType: Optional[str] = Query("", description="查询类型"),
    SearchKeyValue: Optional[str] = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区经营报表详情"""
    logger.warning("GetRevenueReportDetil 暂未完整实现")
    return Result.success(data={
        "Serverpart_N": None, "Serverpart_Name": None,
        "Serverpart_Revenue": None, "Serverpart_RevenueN": None, "Serverpart_RevenueS": None,
        "Serverpart_S": None,
        "ShopList": [{"BusinessType_Logo": None, "BusinessType_Name": None, "BusinessType_Revenue": None,
                      "Serverpart_N": None, "Serverpart_RevenueN": None, "Serverpart_RevenueS": None,
                      "Serverpart_S": None, "Upload_Type": None}],
    }, msg="查询成功")


# ===== 畅销商品 =====
@router.get("/Revenue/GetSalableCommodity")
async def get_salable_commodity(
    statisticsDate: Optional[str] = Query(None, description="统计日期"),
    provinceCode: Optional[str] = Query(None, description="业主单位标识"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商超畅销商品"""
    logger.warning("GetSalableCommodity 暂未完整实现")
    _sc = {"Commodity_name": None, "Proportion": None}
    return Result.success(data={
        "SalableCommodity": None, "SalableCommodityList": [_sc],
        "UnSalableCommodity": None, "UnSalableCommodityList": [_sc],
    }, msg="查询成功")


# ===== 排行/同比 =====
@router.get("/Revenue/GetSPRevenueRank")
async def get_sp_revenue_rank(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_StartDate: Optional[str] = Query(None, description="统计开始日期"),
    Statistics_Date: Optional[str] = Query(None, description="统计结束日期"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取近日服务区营收排行"""
    logger.warning("GetSPRevenueRank 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    resp = json_list.model_dump()
    resp["OtherData"] = None
    return Result.success(data=resp, msg="查询成功")


@router.get("/Revenue/GetRevenueYOY")
async def get_revenue_yoy(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    StatisticsStartDate: Optional[str] = Query(None, description="统计开始日期"),
    StatisticsEndDate: Optional[str] = Query(None, description="统计结束日期"),
    CompareStartDate: Optional[str] = Query("", description="同比开始日期"),
    CompareEndDate: Optional[str] = Query("", description="同比结束日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取每日营收同比数据"""
    logger.warning("GetRevenueYOY 暂未完整实现")
    _ckm = {"data": None, "key": None, "name": None, "value": None}
    return Result.success(data={
        "curHoliday": None, "curHolidayDays": None, "curRevenue": None, "curList": [_ckm],
        "compareHoliday": None, "compareHolidayDays": None, "compareRevenue": None, "compareList": [_ckm],
    }, msg="查询成功")


@router.get("/Revenue/GetHolidayCompare")
async def get_holiday_compare(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query(None, description="历年年份"),
    holidayType: int = Query(0, description="节日类型"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日营收同比数据"""
    logger.warning("GetHolidayCompare 暂未完整实现")
    _ckm2 = {"data": None, "key": None, "name": None, "value": None}
    return Result.success(data={
        "curHoliday": None, "curHolidayDays": None, "curRevenue": None, "curList": [_ckm2],
        "compareHoliday": None, "compareHolidayDays": None, "compareRevenue": None, "compareList": [_ckm2],
    }, msg="查询成功")


# ===== 实时交易 =====
@router.get("/Revenue/GetAccountReceivable")
async def get_account_receivable(
    calcType: int = Query(1, description="计算方式：1当月 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsMonth: Optional[str] = Query(None, description="统计结束月份"),
    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收统计明细数据"""
    logger.warning("GetAccountReceivable 暂未完整实现")
    _nv = {"name": None, "value": None}
    return Result.success(data={
        "CommissionList": [_nv], "CommissionRatio": None,
        "MerchantList": {"AcountList": [_nv], "EntryList": [_nv], "ReceivableList": [_nv]},
        "MerchantRevenue": None,
        "OwnerList": {"AcountList": [_nv], "EntryList": [_nv], "ReceivableList": [_nv]},
        "OwnerRevenue": None,
        "ProjectCount": None, "ProjectCountList": [_nv],
        "ProjectRatioList": [_nv], "RevenueRatioList": [_nv],
    }, msg="查询成功")


@router.get("/Revenue/GetCurRevenue")
async def get_cur_revenue(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    serverPartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时营收交易数据"""
    logger.warning("GetCurRevenue 暂未完整实现")
    return Result.success(data={
        "AddRevenueAmount": None, "AddTicketCount": None, "AddTotalCount": None,
        "AnnualRevenue": None, "CurAvgSellAmount": None, "CurAvgTicketAmount": None,
        "CurRevenueAmount": None, "CurTicketCount": None, "CurTotalCount": None,
    }, msg="查询成功")


@router.get("/Revenue/GetShopCurRevenue")
async def get_shop_cur_revenue(
    serverPartId: Optional[str] = Query(None, description="服务区内码"),
    statisticsDate: Optional[str] = Query(None, description="统计日期"),
    groupByShop: bool = Query(False, description="是否合并双侧同业态门店"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时门店营收交易数据"""
    logger.warning("GetShopCurRevenue 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.fail(code=101, msg="查询失败，无数据返回！")


@router.get("/Revenue/GetLastSyncDateTime")
async def get_last_sync_date_time(db: DatabaseHelper = Depends(get_db)):
    """获取最新的同步日期"""
    logger.warning("GetLastSyncDateTime 暂未完整实现")
    return Result.success(data="", msg="查询成功")


# ===== 节日分析 =====
@router.get("/Revenue/GetHolidayAnalysis")
async def get_holiday_analysis(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query(None, description="历年年份"),
    holidayType: int = Query(0, description="节日类型"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节日营收数据对比分析"""
    _ckm = lambda: {"data": None, "key": None, "name": None, "value": None}
    _model = {
        "ServerpartId": None, "ServerpartName": None,
        "curYear": curYear, "compareYear": compareYear,
        "HolidayType": holidayType, "curDate": None, "cyDate": None,
        "curYearRevenue": _ckm(), "lYearRevenue": _ckm(),
        "curYearAccount": _ckm(), "lYearAccount": _ckm(),
        "curYearBayonet": _ckm(), "lYearBayonet": _ckm(),
        "curYearSelfRevenue": _ckm(), "lYearSelfRevenue": _ckm(),
        "curYearSelfAccount": _ckm(), "lYearSelfAccount": _ckm(),
        "curYearSCRevenue": _ckm(), "lYearSCRevenue": _ckm(),
        "curYearSCAccount": _ckm(), "lYearSCAccount": _ckm(),
        "curYearSRRevenue": _ckm(), "lYearSRRevenue": _ckm(),
        "curYearSRAccount": _ckm(), "lYearSRAccount": _ckm(),
        "curYearGRORevenue": _ckm(), "lYearGRORevenue": _ckm(),
        "curYearGROAccount": _ckm(), "lYearGROAccount": _ckm(),
        "curYearFCRevenue": _ckm(),
        "curYearCVSRevenue": _ckm(), "lYearCVSRevenue": _ckm(),
        "curYearCVSAccount": _ckm(), "lYearCVSAccount": _ckm(),
        "curYearCoopRevenue": _ckm(), "lYearCoopRevenue": _ckm(),
        "curYearCoopAccount": _ckm(), "lYearCoopAccount": _ckm(),
        "curYearSelfCoopRevenue": _ckm(),
        "curYearWJRevenue": _ckm(), "lYearWJRevenue": _ckm(),
    }
    return Result.success(data=_model, msg="查询成功")


@router.get("/Revenue/GetHolidayAnalysisBatch")
async def get_holiday_analysis_batch(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query(None, description="历年年份"),
    holidayType: int = Query(0, description="节日类型"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    ServerpartIds: Optional[str] = Query("", description="服务区内码集合"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取多个服务区节日营收数据对比分析（批量）"""
    _ckm = lambda: {"data": None, "key": None, "name": None, "value": None}
    _model = {
        "ServerpartId": None, "ServerpartName": None,
        "curYear": curYear, "compareYear": compareYear,
        "HolidayType": holidayType, "curDate": None, "cyDate": None,
        "curYearRevenue": _ckm(), "lYearRevenue": _ckm(),
        "curYearAccount": _ckm(), "lYearAccount": _ckm(),
        "curYearBayonet": _ckm(), "lYearBayonet": _ckm(),
        "curYearSelfRevenue": _ckm(), "lYearSelfRevenue": _ckm(),
        "curYearSelfAccount": _ckm(), "lYearSelfAccount": _ckm(),
        "curYearSCRevenue": _ckm(), "lYearSCRevenue": _ckm(),
        "curYearSCAccount": _ckm(), "lYearSCAccount": _ckm(),
        "curYearSRRevenue": _ckm(), "lYearSRRevenue": _ckm(),
        "curYearSRAccount": _ckm(), "lYearSRAccount": _ckm(),
        "curYearGRORevenue": _ckm(), "lYearGRORevenue": _ckm(),
        "curYearGROAccount": _ckm(), "lYearGROAccount": _ckm(),
        "curYearFCRevenue": _ckm(),
        "curYearCVSRevenue": _ckm(), "lYearCVSRevenue": _ckm(),
        "curYearCVSAccount": _ckm(), "lYearCVSAccount": _ckm(),
        "curYearCoopRevenue": _ckm(), "lYearCoopRevenue": _ckm(),
        "curYearCoopAccount": _ckm(), "lYearCoopAccount": _ckm(),
        "curYearSelfCoopRevenue": _ckm(),
        "curYearWJRevenue": _ckm(), "lYearWJRevenue": _ckm(),
    }
    json_list = JsonListData.create(data_list=[_model], total=1)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


# ===== 增幅分析 =====
@router.get("/Revenue/GetServerpartINCAnalysis")
async def get_serverpart_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[int] = Query(None, description="本年年份"),
    HolidayType: int = Query(0, description="节日类型: 0日常 1元旦 2春运 3清明 4五一 5端午 6暑期 7中秋 8国庆"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    compareYear: Optional[int] = Query(None, description="历年年份"),
    CurStartDate: Optional[str] = Query("", description="统计开始日期"),
    StatisticsStartDate: Optional[str] = Query("", description="统计开始日期(兼容)"),
    StatisticsEndDate: Optional[str] = Query("", description="统计结束日期(兼容)"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    businessRegion: Optional[int] = Query(None, description="经营区域"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    IsYOYCompare: bool = Query(False, description="是否对比同期数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区营收增幅分析"""
    try:
        from datetime import datetime as dt, timedelta

        # 节日枚举
        holiday_names = {1: "元旦", 2: "春运", 3: "清明", 4: "五一", 5: "端午", 6: "暑期", 7: "中秋", 8: "国庆"}

        if not StatisticsDate:
            StatisticsDate = dt.now().strftime("%Y-%m-%d")
        if compareYear is None:
            compareYear = (curYear or dt.now().year) - 1

        # 1. GetHoliday: 获取节假日起止日期
        stats_start = None
        stats_end = None
        compare_start = None
        compare_end = None

        if HolidayType == 6:  # 暑期固定
            stats_start = dt(curYear, 7, 1)
            stats_end = dt(curYear, 8, 31)
            compare_start = dt(compareYear, 7, 1)
            compare_end = dt(compareYear, 8, 31)
        elif HolidayType == 0:  # 日常
            if CurStartDate:
                stats_start = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y/%m/%d")
            else:
                stats_start = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
            stats_end = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
            compare_start = stats_start.replace(year=stats_start.year - 1)
            compare_end = stats_end.replace(year=stats_end.year - 1)
        else:  # 其他节日从T_HOLIDAY查
            h_name = holiday_names.get(HolidayType, "")
            cur_desc = f"{curYear}年{h_name}"
            cmp_desc = f"{compareYear}年{h_name}"
            h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
                WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""")
            if not h_rows:
                return Result.fail(code=101, msg="查询失败，无数据返回！")
            cur_dates = [r["HOLIDAY_DATE"] for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
            cmp_dates = [r["HOLIDAY_DATE"] for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
            if not cur_dates or not cmp_dates:
                return Result.fail(code=101, msg="查询失败，无数据返回！")

            def to_dt(v):
                if isinstance(v, dt): return v
                if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
                return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

            stats_start = to_dt(min(cur_dates))
            stats_end = to_dt(max(cur_dates))
            compare_start = to_dt(min(cmp_dates))
            compare_end = to_dt(max(cmp_dates))

            # 按节日类型调整日期范围
            if HolidayType in (1, 3, 5, 7):  # 元旦/清明/端午/中秋: 前1天到后3天
                stats_end = stats_start + timedelta(days=3)
                stats_start = stats_start - timedelta(days=1)
                compare_end = compare_start + timedelta(days=3)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 4:  # 五一: 前1天到后1天
                stats_end = stats_end + timedelta(days=1)
                stats_start = stats_start - timedelta(days=1)
                compare_end = compare_end + timedelta(days=1)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 8:  # 国庆
                if curYear == 2023:
                    stats_start = dt(curYear, 9, 27); stats_end = dt(curYear, 10, 6)
                else:
                    stats_start = dt(curYear, 9, 29); stats_end = dt(curYear, 10, 8)
                if compareYear == 2023:
                    compare_start = dt(compareYear, 9, 27); compare_end = dt(compareYear, 10, 6)
                else:
                    compare_start = dt(compareYear, 9, 29); compare_end = dt(compareYear, 10, 8)

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
        if stat_date < stats_start:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        if stat_date > stats_end:
            stat_date = stats_end

        if CurStartDate and HolidayType != 0:
            cur_start_dt = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y/%m/%d")
            if cur_start_dt > stats_start:
                compare_start = compare_start + timedelta(days=(cur_start_dt - stats_start).days + 1)
                stats_start = cur_start_dt

        if HolidayType != 0 and IsYOYCompare and stat_date < stats_end:
            compare_end = compare_start + timedelta(days=(stat_date - stats_start).days)

        # 2. 查省份ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": pushProvinceCode})
        if not fe_rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        province_id = fe_rows[0]["FIELDENUM_ID"]

        # 3. 查营收(T_HOLIDAYREVENUE)
        where_rev = f' AND A."PROVINCE_ID" = {province_id}'
        if ServerpartId:
            sp_list = "'" + ServerpartId.replace(",", "','") + "'"
            where_rev += f' AND A."SERVERPART_ID" IN ({sp_list})'

        cur_start_str = (stat_date if calcType == 1 else stats_start).strftime("%Y%m%d")
        cur_end_str = stat_date.strftime("%Y%m%d")
        sql_cur_rev = f"""SELECT A."SERVERPART_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1 AND A."STATISTICS_DATE" BETWEEN {cur_start_str} AND {cur_end_str}{where_rev}
            GROUP BY A."SERVERPART_ID" """
        dt_cur_rev = db.execute_query(sql_cur_rev) or []

        cy_date = compare_start + timedelta(days=(stat_date - stats_start).days)
        cy_start_str = (cy_date if calcType == 1 else compare_start).strftime("%Y%m%d")
        cy_end_str = cy_date.strftime("%Y%m%d")
        sql_cy_rev = f"""SELECT A."SERVERPART_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1 AND A."STATISTICS_DATE" BETWEEN {cy_start_str} AND {cy_end_str}{where_rev}
            GROUP BY A."SERVERPART_ID" """
        dt_cy_rev = db.execute_query(sql_cy_rev) or []

        # 4. 查车流(T_SECTIONFLOW)
        where_bay = ""
        if ServerpartId:
            where_bay = f' AND A."SERVERPART_ID" IN ({ServerpartId})'
        else:
            where_bay = f''' AND EXISTS (SELECT 1 FROM "T_SERVERPART" S WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {province_id})'''

        bay_cur_start = stat_date.strftime("%Y%m%d") if calcType == 1 else stats_start.strftime("%Y%m%d")
        sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW",
                SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {bay_cur_start} AND {stat_date.strftime("%Y%m%d")}{where_bay}
            GROUP BY A."SERVERPART_ID" """
        dt_cur_bay = db.execute_query(sql_cur_bay) or []

        bay_cy_start = cy_date.strftime("%Y%m%d") if calcType == 1 else compare_start.strftime("%Y%m%d")
        sql_cy_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW",
                SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {bay_cy_start} AND {cy_date.strftime("%Y%m%d")}{where_bay}
            GROUP BY A."SERVERPART_ID" """
        dt_cy_bay = db.execute_query(sql_cy_bay) or []

        # 5. 查服务区列表
        where_sp = f' AND "PROVINCE_CODE" = {province_id}'
        if ServerpartId:
            where_sp += f' AND "SERVERPART_ID" IN ({ServerpartId})'
        if businessRegion == 1:
            where_sp += ' AND "SPREGIONTYPE_ID" NOT IN (72)'  # 排除城市店片区
        sp_rows = db.execute_query(f"""SELECT * FROM "T_SERVERPART"
            WHERE "SPREGIONTYPE_ID" IS NOT NULL AND "STATISTICS_TYPE" = 1000 AND "STATISTIC_TYPE" = 1000{where_sp}
            ORDER BY "SPREGIONTYPE_INDEX","SPREGIONTYPE_ID","SERVERPART_INDEX","SERVERPART_CODE" """) or []

        # 营收/车流 按服务区ID索引
        def build_map(rows, key="SERVERPART_ID"):
            m = {}
            for r in rows:
                sid = str(r.get(key, ""))
                if sid not in m:
                    m[sid] = r
                else:
                    for k2, v2 in r.items():
                        if k2 != key:
                            try: m[sid][k2] = (m[sid].get(k2) or 0) + (v2 or 0)
                            except: pass
            return m

        cur_rev_map = build_map(dt_cur_rev)
        cy_rev_map = build_map(dt_cy_rev)
        cur_bay_map = build_map(dt_cur_bay)
        cy_bay_map = build_map(dt_cy_bay)

        def safe_f(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        def make_inc(cur, ly):
            inc = {"curYearData": cur, "lYearData": ly, "increaseData": None, "increaseRate": None,
                   "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
            if cur and ly and cur != 0 and ly != 0:
                inc["increaseData"] = round(cur - ly, 2)
                inc["increaseRate"] = round((cur - ly) / ly * 100, 2)
            return inc

        # 6. 构建结果
        result_list = []
        no_increase_list = []
        for sp in sp_rows:
            sp_id = str(sp["SERVERPART_ID"])
            cur_r = cur_rev_map.get(sp_id, {})
            cy_r = cy_rev_map.get(sp_id, {})
            cur_b = cur_bay_map.get(sp_id, {})
            cy_b = cy_bay_map.get(sp_id, {})

            rev_inc = make_inc(safe_f(cur_r.get("REVENUE_AMOUNT")), safe_f(cy_r.get("REVENUE_AMOUNT")))
            acc_inc = make_inc(safe_f(cur_r.get("ACCOUNT_AMOUNT")), safe_f(cy_r.get("ACCOUNT_AMOUNT")))
            bay_inc = make_inc(safe_f(cur_b.get("SERVERPART_FLOW")), safe_f(cy_b.get("SERVERPART_FLOW")))
            sec_inc = make_inc(safe_f(cur_b.get("SECTIONFLOW_NUM")), safe_f(cy_b.get("SECTIONFLOW_NUM")))

            # 车流增长率>1000没有可比性
            if bay_inc["increaseRate"] and abs(bay_inc["increaseRate"]) > 1000:
                bay_inc["increaseData"] = None; bay_inc["increaseRate"] = None
            if sec_inc["increaseRate"] and abs(sec_inc["increaseRate"]) > 1000:
                sec_inc["increaseData"] = None; sec_inc["increaseRate"] = None
            # 历年车流<100不计算增长率
            if bay_inc.get("lYearData") and bay_inc["lYearData"] <= 100:
                bay_inc["increaseRate"] = None

            item = {
                "SPRegionTypeId": sp.get("SPREGIONTYPE_ID"),
                "SPRegionTypeName": sp.get("SPREGIONTYPE_NAME"),
                "ServerpartId": sp.get("SERVERPART_ID"),
                "ServerpartName": sp.get("SERVERPART_NAME"),
                "RevenueINC": rev_inc,
                "AccountINC": acc_inc,
                "BayonetINC": bay_inc,
                "SectionFlowINC": sec_inc,
                "AvgTicketINC": None,
                "TicketINC": None,
                "BayonetINC_ORI": None,
                "ShopINCList": None,
                "RankDiff": None,
                "Cost_Amount": None,
                "Ca_Cost": None,
                "Profit_Amount": None,
            }

            # 排序相关过滤
            is_no_increase = True
            if SortStr:
                ss = SortStr.lower()
                if "revenue" in ss and not (rev_inc["increaseRate"] is not None):
                    is_no_increase = False
                if "account" in ss and not (acc_inc["increaseRate"] is not None):
                    is_no_increase = False
                if "bayonet" in ss and not (bay_inc["increaseRate"] is not None):
                    is_no_increase = False

            if is_no_increase:
                result_list.append(item)
            else:
                no_increase_list.append(item)

        # 排序
        if SortStr:
            ss = SortStr.lower().replace(" asc", "")
            rev = "desc" in SortStr.lower()
            if "revenue" in ss and "bayonet" not in ss:
                result_list.sort(key=lambda x: x["RevenueINC"]["increaseRate"] or 0, reverse=rev)
            elif "bayonet" in ss and "revenue" not in ss:
                result_list.sort(key=lambda x: x["BayonetINC"]["increaseRate"] or 0, reverse=rev)
            elif "account" in ss:
                result_list.sort(key=lambda x: x["AccountINC"]["increaseRate"] or 0, reverse=rev)

        result_list.extend(no_increase_list)

        if not result_list:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        h_name = holiday_names.get(HolidayType, "")
        holiday_period = f"{curYear}年{h_name}时间为{stats_start.strftime('%Y/%m/%d')}至{stat_date.strftime('%Y/%m/%d')}\r\n{compareYear}年{h_name}时间为{compare_start.strftime('%Y/%m/%d')}至{compare_end.strftime('%Y/%m/%d')}"

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        resp = json_list.model_dump()
        resp["Remark"] = holiday_period
        resp["OtherData"] = None
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartINCAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetShopINCAnalysis")
async def get_shop_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query("", description="历年年份"),
    serverpartId: Optional[str] = Query(None, description="服务区内码"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店营收增幅分析"""
    logger.warning("GetShopINCAnalysis 暂未完整实现")
    return Result.fail(code=101, msg="查询失败，无数据返回！")


# ===== 月度经营 =====
@router.get("/Revenue/GetMonthlyBusinessAnalysis")
async def get_monthly_business_analysis(
    calcType: int = Query(1, description="计算方式：1当月 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query("", description="历年年份"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    businessRegion: int = Query(1, description="经营区域：1服务区 2城市店"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营增幅分析"""
    _inc = lambda: {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None,
                     "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
    _item = {
        "SPRegionTypeId": None, "SPRegionTypeName": None,
        "ServerpartId": None, "ServerpartName": None,
        "RevenueINC": _inc(), "AccountINC": _inc(), "BayonetINC": _inc(), "SectionFlowINC": _inc(),
        "AvgTicketINC": None, "TicketINC": None,
        "BayonetINC_ORI": None, "ShopINCList": None,
        "RankDiff": None, "Cost_Amount": None, "Ca_Cost": None, "Profit_Amount": None,
    }
    json_list = JsonListData.create(data_list=[_item], total=0)
    resp = json_list.model_dump()
    resp["Abundant"] = None
    resp["Average"] = None
    resp["Rigid_Demand"] = None
    resp["RevenueINC"] = _inc()
    resp["AccountINC"] = _inc()
    resp["BayonetINC"] = _inc()
    resp["SectionFlowINC"] = _inc()
    resp["AvgTicketINC"] = _inc()
    resp["TicketINC"] = _inc()
    resp["SPRegionList"] = []
    resp["BusinessTradeList"] = []
    return Result.success(data=resp, msg="查询成功")


@router.get("/Revenue/GetMonthlySPINCAnalysis")
async def get_monthly_sp_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区月度营收增幅分析"""
    _inc = lambda: {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None,
                     "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
    _item = {
        "SPRegionTypeId": None, "SPRegionTypeName": None,
        "ServerpartId": None, "ServerpartName": None,
        "RevenueINC": _inc(), "AccountINC": _inc(), "BayonetINC": _inc(), "SectionFlowINC": _inc(),
        "AvgTicketINC": None, "TicketINC": None,
        "BayonetINC_ORI": None, "ShopINCList": None,
        "RankDiff": None, "Cost_Amount": None, "Ca_Cost": None, "Profit_Amount": None,
    }
    json_list = JsonListData.create(data_list=[_item], total=0)
    resp = json_list.model_dump()
    resp["OtherData"] = None
    return Result.success(data=resp, msg="查询成功")


# ===== 其余接口 =====
@router.get("/Revenue/GetTransactionDetailList")
async def get_transaction_detail_list(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    ServerpartShopId: Optional[str] = Query("", description="门店内码"),
    StartTime: Optional[str] = Query("", description="开始时间"),
    EndTime: Optional[str] = Query("", description="结束时间"),
    PageIndex: int = Query(1, description="显示页码"),
    PageSize: int = Query(100, description="每页数量"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时交易明细"""
    logger.warning("GetTransactionDetailList 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0, page_index=PageIndex, page_size=PageSize)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


@router.get("/Revenue/GetHolidayRevenueRatio")
async def get_holiday_revenue_ratio(db: DatabaseHelper = Depends(get_db)):
    """获取节日营收占比"""
    logger.warning("GetHolidayRevenueRatio 暂未完整实现")
    _ckm = {"data": None, "key": None, "name": None, "value": None}
    _tree = {"node": _ckm, "children": [{"node": _ckm, "children": []}]}
    json_list = JsonListData.create(data_list=[_tree], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


@router.post("/Revenue/GetBusinessRevenueList")
async def get_business_revenue_list(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取云南24年经营数据分析（AES加密）"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        data_type = params.get("DataType", "")
        start_month = params.get("StartMonth", "")
        end_month = params.get("EndMonth", "")
        group_by_region = params.get("GroupByRegion", False)
        group_by_trade = params.get("GroupByTrade", False)
        logger.info(f"GetBusinessRevenueList 解密参数: ProvinceCode={province_code}, DataType={data_type}")

        # TODO: 实现查询逻辑
        logger.warning("GetBusinessRevenueList 查询逻辑暂未实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetBusinessRevenueList AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/Revenue/GetMonthlyBusinessRevenue")
async def get_monthly_business_revenue(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取云南月度经营数据分析（AES加密）"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        serverpart_id = params.get("ServerpartId", "")
        data_type = params.get("DataType", "")
        start_month = params.get("StartMonth", "")
        end_month = params.get("EndMonth", "")
        logger.info(f"GetMonthlyBusinessRevenue 解密参数: ProvinceCode={province_code}, DataType={data_type}")

        # TODO: 实现查询逻辑
        logger.warning("GetMonthlyBusinessRevenue 查询逻辑暂未实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetMonthlyBusinessRevenue AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetCompanyRevenueReport")
async def get_company_revenue_report(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StartTime: Optional[str] = Query(None, description="开始日期"),
    EndTime: Optional[str] = Query(None, description="结束日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """按照安徽驿达子公司运营的门店返回经营数据报表"""
    try:
        from datetime import datetime as dt
        from collections import defaultdict

        # 1. 查省份FIELDENUM_ID
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": ProvinceCode})
        if not fe_rows:
            return Result.fail(code=200, msg="查询失败，省份编码不正确！")
        province_id = fe_rows[0]["FIELDENUM_ID"]

        # 2. 构建WHERE条件
        where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
        if ServerpartId:
            where_sql += f' AND B."SERVERPART_ID" IN ({ServerpartId})'
        else:
            where_sql += f' AND B."STATISTIC_TYPE" = 1000 AND B."STATISTICS_TYPE" = 1000 AND B."PROVINCE_CODE" = {province_id}'
        if StartTime:
            sd = dt.strptime(StartTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in StartTime else StartTime
            where_sql += f' AND A."STATISTICS_DATE" >= {sd}'
        if EndTime:
            ed = dt.strptime(EndTime, "%Y-%m-%d").strftime("%Y%m%d") if "-" in EndTime else EndTime
            where_sql += f' AND A."STATISTICS_DATE" <= {ed}'

        # 3. 查询营收数据
        sql = f"""SELECT 
                B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX", B."STATISTICS_TYPE",
                B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX",
                A."SERVERPARTSHOP_ID", A."BUSINESS_TYPE", A."SHOPTRADE",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT", SUM(A."MOBILEPAY_AMOUNT") AS "MOBILEPAY_AMOUNT",
                SUM(A."CASHPAY_AMOUNT") AS "CASHPAY_AMOUNT", SUM(A."OTHERPAY_AMOUNT") AS "OTHERPAY_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT", SUM(A."TOTAL_COUNT") AS "TOTAL_COUNT",
                SUM(A."TOTALOFF_AMOUNT") AS "TOTALOFF_AMOUNT", SUM(A."DIFFERENT_AMOUNT") AS "DIFFERENT_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1{where_sql}
            GROUP BY B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", B."SPREGIONTYPE_INDEX", B."STATISTICS_TYPE",
                B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_CODE", B."SERVERPART_INDEX",
                A."SERVERPARTSHOP_ID", A."BUSINESS_TYPE", A."SHOPTRADE" """
        rows = db.execute_query(sql)
        if not rows or not any(r.get("SERVERPARTSHOP_ID") for r in rows):
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 4. 查门店信息（SERVERPARTSHOP_ID可能是逗号分隔的多个ID）
        all_shop_ids = set()
        for r in rows:
            sid = r.get("SERVERPARTSHOP_ID")
            if sid:
                for s in str(sid).split(","):
                    s = s.strip()
                    if s:
                        all_shop_ids.add(s)
        shop_map = {}
        if all_shop_ids:
            id_list = list(all_shop_ids)
            chunk_size = 500
            for i in range(0, len(id_list), chunk_size):
                chunk = id_list[i:i+chunk_size]
                ids_in = ",".join(chunk)
                shop_rows = db.execute_query(f'SELECT * FROM "T_SERVERPARTSHOP" WHERE "SERVERPARTSHOP_ID" IN ({ids_in})')
                for s in (shop_rows or []):
                    shop_map[s.get("SERVERPARTSHOP_ID")] = s

        # 5. 查业态
        trade_rows = db.execute_query(f"""SELECT "AUTOSTATISTICS_ID","AUTOSTATISTICS_PID","AUTOSTATISTICS_NAME","AUTOSTATISTICS_INDEX"
            FROM "T_AUTOSTATISTICS" WHERE "PROVINCE_CODE" = {province_id} AND "AUTOSTATISTICS_STATE" > 0""")
        trade_map = {}
        for t in (trade_rows or []):
            trade_map[str(t["AUTOSTATISTICS_ID"])] = t["AUTOSTATISTICS_NAME"]

        # 6. 查业务限制(T_RTBUSINESSLIMIT)
        push_limit = defaultdict(set)
        if all_shop_ids:
            ids_in = ",".join(list(all_shop_ids)[:1000])
            limit_rows = db.execute_query(f"""SELECT A."SERVERPARTSHOP_ID", R."DATA_VALUE"
                FROM "T_SERVERPARTSHOP" A, "T_RTBUSINESSLIMIT" R
                WHERE A."SERVERPARTSHOP_ID" = R."SERVERPARTSHOP_ID" AND R."DATA_TYPE" = 1030
                    AND R."DATA_VALUE" IN (2010,2020,2030,2040,2050,2060)
                    AND A."SERVERPARTSHOP_ID" IN ({ids_in})
                GROUP BY A."SERVERPARTSHOP_ID", R."DATA_VALUE" """)
            for lr in (limit_rows or []):
                push_limit[lr["SERVERPARTSHOP_ID"]].add(int(lr["DATA_VALUE"]))

        # 7. 给每行标记该归属哪个公司
        def safe_int(v):
            try: return int(v) if v is not None else 0
            except: return 0

        def safe_float(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        processed = []
        for r in rows:
            item = {
                "SPRegionTypeId": safe_int(r.get("SPREGIONTYPE_ID")),
                "SPRegionTypeName": str(r.get("SPREGIONTYPE_NAME") or ""),
                "SPRegionTypeIndex": safe_int(r.get("SPREGIONTYPE_INDEX")),
                "ServerpartId": safe_int(r.get("SERVERPART_ID")),
                "ServerpartName": str(r.get("SERVERPART_NAME") or ""),
                "ServerpartIndex": safe_int(r.get("SERVERPART_INDEX")),
                "ServerpartShopId": str(r.get("SERVERPARTSHOP_ID") or ""),
                "RevenueAmount": safe_float(r.get("REVENUE_AMOUNT")),
                "BusinessTrade": 0, "BusinessTradeName": "",
                "BusinessBrand": 0, "BrandName": "",
                "ShopShortName": "", "MerchantsName": "",
            }
            shop_id_str = str(r.get("SERVERPARTSHOP_ID") or "")
            if not shop_id_str:
                if safe_int(r.get("TICKET_COUNT")) > 0:
                    item["MerchantsName"] = "安徽驿达运营管理有限公司"
                processed.append(item)
                continue
            # 拆分逗号分隔的ID，查所有匹配门店
            sub_ids = [s.strip() for s in shop_id_str.split(",") if s.strip()]
            exist_shops = [shop_map[int(sid)] for sid in sub_ids if int(sid) in shop_map]
            if not exist_shops:
                item["MerchantsName"] = "安徽驿达运营管理有限公司"
                processed.append(item)
                continue
            # 优先判定: 驿佳(-2846) > 百和(-2802) > 驿达
            yijia_shops = [s for s in exist_shops if safe_int(s.get("SELLER_ID")) == -2846]
            baihe_shops = [s for s in exist_shops if safe_int(s.get("SELLER_ID")) == -2802]
            if yijia_shops:
                shop = yijia_shops[0]
                item["MerchantsName"] = "安徽驿佳商贸有限公司"
                item["BusinessTrade"] = safe_int(shop.get("BUSINESS_TRADE"))
                item["BusinessBrand"] = safe_int(shop.get("BUSINESS_BRAND"))
                item["BrandName"] = str(shop.get("BRAND_NAME") or "")
                item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")
            elif baihe_shops:
                shop = baihe_shops[0]
                item["MerchantsName"] = "安徽百和餐饮有限公司"
                item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")
                # 查pushLimit确定trade
                for sid in sub_ids:
                    limits = push_limit.get(int(sid), set())
                    if 2040 in limits:
                        item["BusinessTrade"] = 2040; item["BusinessTradeName"] = "咖啡"; break
                    elif 2050 in limits:
                        item["BusinessTrade"] = 2050; item["BusinessTradeName"] = "老乡鸡"; break
                    elif 2060 in limits:
                        item["BusinessTrade"] = 2060; item["BusinessTradeName"] = "肯德基"; break
                else:
                    item["BusinessTrade"] = 2000; item["BusinessTradeName"] = "餐饮"
            else:
                shop = exist_shops[0]
                item["MerchantsName"] = "安徽驿达运营管理有限公司"
                bt = max((safe_int(s.get("BUSINESS_TRADE")) for s in exist_shops), default=0)
                item["BusinessTrade"] = bt
                item["ShopShortName"] = str(shop.get("SHOPSHORTNAME") or "")

            # 匹配业态名称
            trade_id = str(item["BusinessTrade"])
            if trade_id in trade_map and not item["BusinessTradeName"]:
                item["BusinessTradeName"] = trade_map[trade_id]

            item["ShopShort_Name"] = str(r.get("SERVERPART_NAME") or "") + item["ShopShortName"]
            processed.append(item)

        # 8. 构建嵌套结果
        total_revenue = sum(p["RevenueAmount"] for p in processed)
        if total_revenue == 0:
            total_revenue = 1

        company_names = ["安徽驿达运营管理有限公司", "安徽驿佳商贸有限公司", "安徽百和餐饮有限公司"]
        result_list = []

        def make_node(**kwargs):
            base = {"CompanyId": 0, "CompanyName": None, "SPRegionType_Id": None, "SPRegionType_Name": None,
                    "Serverpart_Id": None, "Serverpart_Name": None, "BusinessType_Name": None,
                    "BusinessTrade_Id": None, "BusinessTrade_Name": None, "ServerpartShop_Id": None,
                    "ShopShort_Name": None, "Total_Revenue": None, "Revenue_Proportion": None,
                    "TicketCount": None, "TotalCount": None, "TotalOffAmount": None, "MobilePayment": None,
                    "Different_Price_Less": None, "Different_Price_More": None}
            base.update(kwargs)
            return base

        def bind_sp_nodes(items, company_name, trade_id, trade_name):
            """按片区->服务区分组"""
            region_groups = defaultdict(list)
            for it in items:
                region_groups[(it["SPRegionTypeId"], it["SPRegionTypeName"], it["SPRegionTypeIndex"])].append(it)
            region_nodes = []
            for (rid, rname, rindex), sp_items in sorted(region_groups.items(), key=lambda x: (x[0][2], x[0][0])):
                rev = round(sum(s["RevenueAmount"] for s in sp_items), 2)
                region_node = {
                    "node": make_node(CompanyName=company_name, BusinessTrade_Id=trade_id,
                                     BusinessTrade_Name=trade_name, SPRegionType_Id=rid,
                                     SPRegionType_Name=rname, Total_Revenue=rev,
                                     Revenue_Proportion=round(rev / total_revenue * 100, 2)),
                    "children": []
                }
                server_groups = defaultdict(list)
                for s in sp_items:
                    server_groups[(s["ServerpartId"], s["ServerpartName"], s["ServerpartIndex"])].append(s)
                for (sid, sname, sindex), s_items in sorted(server_groups.items(), key=lambda x: x[0][2]):
                    srv = round(sum(x["RevenueAmount"] for x in s_items), 2)
                    shop_ids_str = ",".join(set(x["ServerpartShopId"] for x in s_items if x["ServerpartShopId"]))
                    region_node["children"].append({
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=trade_id,
                                         BusinessTrade_Name=trade_name, SPRegionType_Id=rid,
                                         SPRegionType_Name=rname, Serverpart_Id=sid,
                                         Serverpart_Name=sname, ServerpartShop_Id=shop_ids_str or None,
                                         Total_Revenue=srv,
                                         Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                        "children": []
                    })
                region_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                region_nodes.append(region_node)
            return region_nodes

        for company_name in company_names:
            company_items = [p for p in processed if p["MerchantsName"] == company_name]
            if not company_items:
                continue
            company_rev = round(sum(c["RevenueAmount"] for c in company_items), 2)
            company_node = {
                "node": make_node(CompanyName=company_name, Total_Revenue=company_rev,
                                 Revenue_Proportion=round(company_rev / total_revenue * 100, 2)),
                "children": []
            }

            if company_name == "安徽驿达运营管理有限公司":
                # 按业态父级分组
                parent_trades = [t for t in (trade_rows or []) if str(t.get("AUTOSTATISTICS_PID")) == "-1"]
                parent_trades.sort(key=lambda x: safe_int(x.get("AUTOSTATISTICS_INDEX")))
                for pt in parent_trades:
                    pid = str(pt["AUTOSTATISTICS_ID"])
                    child_ids = {str(t["AUTOSTATISTICS_ID"]) for t in (trade_rows or [])
                                 if str(t.get("AUTOSTATISTICS_PID")) == pid or str(t["AUTOSTATISTICS_ID"]) == pid}
                    trade_items = [c for c in company_items if str(c["BusinessTrade"]) in child_ids]
                    if not trade_items:
                        continue
                    t_rev = round(sum(t["RevenueAmount"] for t in trade_items), 2)
                    trade_node = {
                        "node": make_node(CompanyName=company_name,
                                         BusinessTrade_Id=safe_float(pt["AUTOSTATISTICS_ID"]),
                                         BusinessTrade_Name=pt["AUTOSTATISTICS_NAME"],
                                         Total_Revenue=t_rev,
                                         Revenue_Proportion=round(t_rev / total_revenue * 100, 2)),
                        "children": bind_sp_nodes(trade_items, company_name,
                                                  safe_float(pt["AUTOSTATISTICS_ID"]), pt["AUTOSTATISTICS_NAME"])
                    }
                    trade_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(trade_node)
                # 其他（BusinessTrade=0的）
                other_items = [c for c in company_items if c["BusinessTrade"] == 0]
                if other_items:
                    o_rev = round(sum(o["RevenueAmount"] for o in other_items), 2)
                    other_node = {
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=0,
                                         BusinessTrade_Name="其他", Total_Revenue=o_rev,
                                         Revenue_Proportion=round(o_rev / total_revenue * 100, 2)),
                        "children": bind_sp_nodes(other_items, company_name, 0, "其他")
                    }
                    other_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(other_node)

            elif company_name == "安徽驿佳商贸有限公司":
                # 便利店 + 品牌分
                store_items = company_items  # 简化处理
                if store_items:
                    s_rev = round(sum(s["RevenueAmount"] for s in store_items), 2)
                    store_node = {
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=0,
                                         BusinessTrade_Name="服务区便利店", Total_Revenue=s_rev,
                                         Revenue_Proportion=round(s_rev / total_revenue * 100, 2)),
                        "children": []
                    }
                    sg = defaultdict(list)
                    for s in store_items:
                        sg[(s["ServerpartId"], s["ServerpartName"], s.get("ShopShort_Name", ""))].append(s)
                    for (sid, sname, ssn), items in sg.items():
                        srv = round(sum(x["RevenueAmount"] for x in items), 2)
                        store_node["children"].append({
                            "node": make_node(CompanyName=company_name, BusinessTrade_Name="服务区便利店",
                                             Serverpart_Id=sid, Serverpart_Name=sname,
                                             ShopShort_Name=ssn, Total_Revenue=srv,
                                             Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                            "children": []
                        })
                    store_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(store_node)

            else:  # 百和餐饮
                trade_groups = defaultdict(list)
                for c in company_items:
                    trade_groups[(c["BusinessTrade"], c["BusinessTradeName"])].append(c)
                for (tid, tname), items in trade_groups.items():
                    t_rev = round(sum(t["RevenueAmount"] for t in items), 2)
                    trade_node = {
                        "node": make_node(CompanyName=company_name, BusinessTrade_Id=tid,
                                         BusinessTrade_Name=tname, Total_Revenue=t_rev,
                                         Revenue_Proportion=round(t_rev / total_revenue * 100, 2)),
                        "children": []
                    }
                    sg = defaultdict(list)
                    for t in items:
                        sg[(t["ServerpartId"], t["ServerpartName"], t.get("ShopShort_Name", ""))].append(t)
                    for (sid, sname, ssn), s_items in sg.items():
                        srv = round(sum(x["RevenueAmount"] for x in s_items), 2)
                        trade_node["children"].append({
                            "node": make_node(CompanyName=company_name, BusinessTrade_Id=tid,
                                             BusinessTrade_Name=tname, Serverpart_Id=sid,
                                             Serverpart_Name=sname, ShopShort_Name=ssn,
                                             Total_Revenue=srv,
                                             Revenue_Proportion=round(srv / total_revenue * 100, 2)),
                            "children": []
                        })
                    trade_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
                    company_node["children"].append(trade_node)

            company_node["children"].sort(key=lambda x: x["node"]["Total_Revenue"] or 0, reverse=True)
            result_list.append(company_node)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCompanyRevenueReport 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetRevenueCompare =====
@router.get("/Revenue/GetRevenueCompare")
async def get_revenue_compare(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收同比环比对比数据"""
    try:
        # 从Header读取ProvinceCode
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")
        # TODO: 实现 RevenuePushHelper.GetRevenueCompare
        logger.warning("GetRevenueCompare 查询逻辑暂未实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetHolidaySPRAnalysis =====
@router.get("/Revenue/GetHolidaySPRAnalysis")
async def get_holiday_spr_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    curYear: int = Query(..., description="本年年份"),
    compareYear: int = Query(..., description="历年年份"),
    HolidayType: int = Query(..., description="节日类型: 1元旦 2春运 3清明 4五一 5端午 6暑期 7中秋 8国庆"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    businessType: Optional[str] = Query("", description="经营模式"),
    businessTrade: Optional[str] = Query("", description="经营业态"),
    businessRegion: Optional[str] = Query("", description="经营区域"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节假日服务区营收分析"""
    try:
        # TODO: 实现 HolidayHelper.GetHolidaySPRAnalysis
        logger.warning("GetHolidaySPRAnalysis 查询逻辑暂未实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetHolidayDailyAnalysis =====
@router.get("/Revenue/GetHolidayDailyAnalysis")
async def get_holiday_daily_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    curYear: int = Query(..., description="本年年份"),
    compareYear: int = Query(..., description="历年年份"),
    HolidayType: int = Query(..., description="节日类型"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    SPRegionTypeId: Optional[str] = Query("", description="片区内码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    businessType: Optional[str] = Query("", description="经营模式"),
    businessTrade: Optional[str] = Query("", description="经营业态"),
    businessRegion: Optional[str] = Query("", description="经营区域"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取节假日各类项目所有天数对客分析"""
    try:
        # TODO: 实现 HolidayHelper.GetHolidayDailyAnalysis
        logger.warning("GetHolidayDailyAnalysis 查询逻辑暂未实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetMonthINCAnalysis =====
@router.get("/Revenue/GetMonthINCAnalysis")
async def get_month_inc_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsStartMonth: str = Query(..., description="统计开始月份"),
    StatisticsEndMonth: str = Query(..., description="统计结束月份"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    businessRegion: Optional[str] = Query(None, description="经营区域"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    shopTrade: Optional[str] = Query("", description="商品业态"),
    compactStartDate: Optional[str] = Query("", description="合同开始日期"),
    compactEndDate: Optional[str] = Query("", description="合同结束日期"),
    calcQOQ: Optional[str] = Query("false", description="是否计算环比"),
    calcYOY: Optional[str] = Query("false", description="是否计算同比"),
    calcBayonet: Optional[str] = Query("false", description="是否计算车流量"),
    hasAnalog: Optional[str] = Query("true", description="是否包含模拟车流"),
    statisticsType: Optional[str] = Query("1", description="统计类型"),
    accountType: Optional[str] = Query("0", description="收入结算类型"),
    showRevenue: Optional[str] = Query("0", description="经营增幅"),
    showBayonet: Optional[str] = Query("0", description="车流增幅"),
    showLevel: Optional[str] = Query("1", description="显示层级"),
    solidType: Optional[str] = Query("true", description="查询固化"),
    showWarning: Optional[str] = Query("true", description="显示预警"),
    warningType: Optional[str] = Query(None, description="预警类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度经营增长分析（含车流量对比）"""
    try:
        # TODO: 实现 AccountHelper.GetMonthINCAnalysis（4800行极复杂逻辑）
        logger.warning("GetMonthINCAnalysis 查询逻辑暂未实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetMonthINCAnalysisSummary =====
@router.get("/Revenue/GetMonthINCAnalysisSummary")
async def get_month_inc_analysis_summary(
    StatisticsStartMonth: str = Query(..., description="统计开始月份"),
    StatisticsEndMonth: str = Query(..., description="统计结束月份"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    shopTrade: Optional[str] = Query("", description="经营业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """汇总月度经营项目预警数值"""
    try:
        # TODO: 实现 AccountHelper.GetMonthINCAnalysisSummary
        logger.warning("GetMonthINCAnalysisSummary 查询逻辑暂未实现")
        _ckm = {"data": None, "key": None, "name": None, "value": None}
        json_list = JsonListData.create(data_list=[_ckm], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== StorageMonthINCAnalysis =====
@router.get("/Revenue/StorageMonthINCAnalysis")
async def storage_month_inc_analysis(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsMonth: str = Query(..., description="统计月份"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    hasAnalog: bool = Query(True, description="是否包含模拟车流"),
    accountType: int = Query(0, description="收入结算类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """固化月度经营预警数据"""
    try:
        # TODO: 实现 AccountHelper.StorageMonthINCAnalysis
        logger.warning("StorageMonthINCAnalysis 查询逻辑暂未实现")
        return Result.success(data={}, msg="生成成功")
    except Exception as ex:
        return Result.fail(msg=f"生成失败{ex}")


# ===== GetShopSABFIList =====
@router.get("/Revenue/GetShopSABFIList")
async def get_shop_sabfi_list(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsMonth: str = Query(..., description="统计月份"),
    ServerpartId: str = Query(..., description="服务区内码"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    BusinessTrade: Optional[str] = Query("", description="经营业态"),
    accountType: int = Query(0, description="收入结算类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """月度服务区门店商业适配指数（SABFI）"""
    try:
        # TODO: 实现 AccountHelper.GetShopSABFIList
        logger.warning("GetShopSABFIList 查询逻辑暂未实现")
        _inc = lambda: {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None,
                         "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
        _node = {
            "SPRegionTypeId": None, "SPRegionTypeName": None,
            "ServerpartId": None, "ServerpartName": None,
            "RevenueINC": _inc(), "AccountINC": _inc(), "BayonetINC": _inc(),
            "AvgTicketINC": _inc(), "TicketINC": _inc(),
            "SectionFlowINC": None, "BayonetINC_ORI": None,
            "ShopINCList": None, "ShopSABFIList": None,
            "RankDiff": None, "Cost_Amount": None, "Ca_Cost": None, "Profit_Amount": None,
            "SABFI_Score": None,
        }
        _tree = {"node": _node, "children": [{"node": _node, "children": []}]}
        json_list = JsonListData.create(data_list=[_tree], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== GetShopMonthSABFIList =====
@router.get("/Revenue/GetShopMonthSABFIList")
async def get_shop_month_sabfi_list(
    calcSelf: bool = Query(..., description="是否计算自营"),
    StatisticsStartMonth: str = Query(..., description="统计开始月份"),
    StatisticsEndMonth: str = Query(..., description="统计结束月份"),
    BusinessProjectId: Optional[int] = Query(None, description="经营项目内码"),
    ServerpartShopId: Optional[str] = Query("", description="门店内码"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ServerpartShopName: Optional[str] = Query("", description="门店名称"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店每月商业适配指数（SABFI）"""
    try:
        # TODO: 实现 AccountHelper.GetShopMonthSABFIList
        logger.warning("GetShopMonthSABFIList 查询逻辑暂未实现")
        _inc2 = lambda: {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None,
                          "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
        _ckm = {"data": None, "key": None, "name": None, "value": None}
        _shop_item = {
            "ServerpartId": None, "ServerpartName": None,
            "ServerpartShopId": None, "ServerpartShopName": None,
            "Brand_Id": None, "Brand_Name": None, "BrandType_Name": None, "Brand_ICO": None,
            "ShopTrade": None, "BusinessTrade": None, "BusinessTradeName": None, "BusinessTradeType": None,
            "BusinessProjectId": None, "BusinessProjectName": None,
            "BusinessType": None, "SettlementModes": None,
            "CompactStartDate": None, "CompactEndDate": None,
            "MERCHANTS_ID": None, "MERCHANTS_ID_Encrypted": None, "MERCHANTS_NAME": None,
            "RevenueINC": _inc2(), "AccountINC": _inc2(),
            "TicketINC": _inc2(), "AvgTicketINC": _inc2(),
            "CurTransaction": None,
            "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
            "Revenue_AVG": None, "Revenue_SD": None,
            "SABFI_Score": None, "SABFIList": [_ckm],
            "StatisticsMonth": None,
        }
        json_list = JsonListData.create(data_list=[_shop_item], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")
