# -*- coding: utf-8 -*-
"""
CommercialApi - Revenue 路由
对应原 CommercialApi/Controllers/RevenueController.cs
营收相关接口（原2657行，40+接口，此处按方法签名完整定义路由）
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from models.base import Result, JsonListData
from routers.deps import get_db, parse_multi_ids, build_in_condition
from core.database import DatabaseHelper
from core.des_helper import des_encrypt_id
# Service 层导入 — 逐步将 Router 中的内联逻辑迁移到 Service
from services.commercial import revenue_trend_service
from services.commercial import revenue_transaction_service
from services.commercial import revenue_push_service
from services.commercial import revenue_brand_service
from services.commercial import revenue_budget_service
from services.commercial import revenue_business_service
from services.commercial import revenue_report_service
from services.commercial import revenue_holiday_service
from services.commercial import revenue_account_service
from services.commercial import revenue_monthly_service





router = APIRouter()


def date_no_pad(d, fmt="ymd"):
    """C# DateTime.ToString("yyyy/M/d") 不补零"""
    if fmt == "ymd":
        return f"{d.year}/{d.month}/{d.day}"
    elif fmt == "ymd_hms":
        return f"{d.year}/{d.month}/{d.day} {d.hour}:{d.minute:02d}:{d.second:02d}"
    return f"{d.year}/{d.month}/{d.day}"

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
    """获取营收推送数据表列表 — 业务逻辑见 revenue_push_service.get_revenue_push_list()"""
    try:
        results = revenue_push_service.get_revenue_push_list(
            db, pushProvinceCode, Statistics_Date, Serverpart_ID,
            SPRegionType_ID, Revenue_Include
        )
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenuePushList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")



@router.get("/Revenue/GetSummaryRevenue")
async def get_summary_revenue(
    request: Request,
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_StartDate: Optional[str] = Query("", description="统计开始日期"),
    Statistics_Date: Optional[str] = Query("", description="统计结束日期"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收(0否1是)"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    ShowYearRevenue: bool = Query(False, description="是否显示年度营收额"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收推送汇总数据 — 业务逻辑见 revenue_push_service.get_summary_revenue()"""
    try:
        if not pushProvinceCode:
            pushProvinceCode = request.headers.get("ProvinceCode", "")
        data = revenue_push_service.get_summary_revenue(
            db, pushProvinceCode, Statistics_StartDate, Statistics_Date,
            SPRegionType_ID, Serverpart_ID, Revenue_Include,
            ShowCompareRate, ShowYearRevenue
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSummaryRevenue 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")



@router.get("/Revenue/GetSummaryRevenueMonth")
async def get_summary_revenue_month(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    StatisticsDate: Optional[str] = Query("", description="统计日期"),
    SolidType: Optional[str] = Query("", description="是否执行固化操作"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度营收推送汇总数据 — 业务逻辑见 revenue_push_service.get_summary_revenue_month()"""
    try:
        data = revenue_push_service.get_summary_revenue_month(
            db, pushProvinceCode, StatisticsMonth, StatisticsDate, SolidType
        )
        if data is None:
            return Result.success(data=None, msg="查询成功")

        # 嵌套调用：获取单日推送模型（RevenuePushModel）
        date_str = StatisticsDate.split(" ")[0] if StatisticsDate else None
        if date_str and data.get("RevenuePushModel") is None:
            try:
                daily_data = revenue_push_service.get_summary_revenue(
                    db, pushProvinceCode, date_str
                )
                if daily_data:
                    data["RevenuePushModel"] = daily_data.get("RevenuePushModel")
            except Exception as inner_ex:
                logger.warning(f"GetSummaryRevenueMonth 获取单日推送模型失败: {inner_ex}")

        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSummaryRevenueMonth 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")



@router.get("/Revenue/GetWechatPushSalesList")
async def get_wechat_push_sales_list(
    pushProvinceCode: str = Query(..., description="推送省份"),
    Statistics_Date: str = Query(..., description="统计日期"),
    RankNum: int = Query(10, description="排行数量"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取单品销售排行榜数据 — 业务逻辑见 revenue_push_service.get_wechat_push_sales_list()"""
    try:
        result_list = revenue_push_service.get_wechat_push_sales_list(
            db, pushProvinceCode, Statistics_Date, RankNum
        )
        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetWechatPushSalesList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetUnUpLoadShops")
async def get_un_upload_shops(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询服务区未上传结账信息的门店列表 — 业务逻辑见 revenue_push_service.get_un_upload_shops()"""
    try:
        result_list = revenue_push_service.get_un_upload_shops(
            db, pushProvinceCode, Statistics_Date, Serverpart_ID,
            SPRegionType_ID, Revenue_Include
        )
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
    """获取服务区品牌营收 — 业务逻辑见 revenue_brand_service.get_serverpart_brand()"""
    try:
        data = revenue_brand_service.get_serverpart_brand(
            db, Serverpart_Id, statictics_Time, pushProvinceCode
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartBrand 失败: {ex}")


# ===== 结账数据接口 =====
@router.get("/Revenue/GetServerpartEndAccountList")
async def get_serverpart_end_account_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询服务区结账数据列表 (SQL平移完成)"""
    try:
        common_info, shop_list = revenue_brand_service.get_end_account_data(db, Serverpart_ID, Statistics_Date)
        if not common_info:
            return Result.success(data={"Serverpart_Id": None, "Serverpart_Name": None, "Revenue_Amount": None, "UploadShopCount": None, "TotalShopCount": None, "ShopEndaccountList": None}, msg="查询成功")
            
        return Result.success(data={
            "Revenue_Amount": common_info["TotalAmount"],
            "Serverpart_Id": common_info["Serverpart_ID"],
            "Serverpart_Name": common_info["Serverpart_Name"],
            "ShopEndaccountList": shop_list,
            "TotalShopCount": common_info["TotalShopCount"],
            "UploadShopCount": common_info["UploadShopCount"]
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartEndAccountList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


@router.get("/Revenue/GetShopEndAccountList")
async def get_shop_end_account_list(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    ServerpartShop_Ids: Optional[str] = Query(None, description="门店内码集合"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """查询门店结账数据列表 (SQL平移完成)"""
    try:
        common_info, shop_list = revenue_brand_service.get_end_account_data(db, Serverpart_ID, Statistics_Date, ServerpartShop_Ids)
        if not common_info:
            return Result.success(data={
                "ServerpartShop_Id": None, "Brand_Id": None, "Brand_Name": None,
                "BrandType_Name": None, "Brand_ICO": None, "Revenue_Amount": None,
                "Business_TradeId": None, "Business_Trade": None, "Business_TradeICO": None,
                "Bussiness_Name": None, "Bussiness_Time": None, "Bussiness_State": None,
                "CurRevenue": 0.0, "ShopEndaccountList": None,
            }, msg="查询成功")
            
        # 注意：此处返回模型为 ShopBrandModel，包含品牌信息
        # 目前暂时只取第一个门店的品牌信息作为示例
        first_shop = shop_list[0] if shop_list else {}
        
        return Result.success(data={
            "Brand_Name": first_shop.get("BRAND_NAME", ""),
            "Brand_Id": 0, # 模拟 C# 逻辑中的品牌 ID 持有
            "Revenue_Amount": common_info["TotalAmount"],
            "ServerpartShop_Id": ServerpartShop_Ids,
            "ShopEndaccountList": shop_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopEndAccountList 失败: {ex}")
        return Result.fail(msg=f"查询失败: {ex}")


# ===== 预算费用 =====
@router.post("/Revenue/GetBudgetExpenseList")
async def get_budget_expense_list_post(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取预算费用表列表（POST） — 业务逻辑见 revenue_budget_service.get_budget_expense_list_post()"""
    try:
        rows, total = revenue_budget_service.get_budget_expense_list_post(db, searchModel)
        page_index = (searchModel or {}).get("PageIndex", 1) or 1
        page_size = (searchModel or {}).get("PageSize", 20) or 20
        json_list = JsonListData.create(data_list=rows, total=total,
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
    """获取预算费用表列表（GET） — 业务逻辑见 revenue_budget_service.get_budget_expense_list_get()"""
    try:
        rows = revenue_budget_service.get_budget_expense_list_get(
            db, Province_Code, Statistics_Month, Serverpart_ID
        )
        json_list = JsonListData.create(data_list=rows, total=len(rows))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetExpenseList GET 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetRevenueBudget")
async def get_revenue_budget(
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="区域内码"),
    Revenue_Include: int = Query(1, description="是否纳入营收"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取计划营收数据 — 业务逻辑见 revenue_budget_service.get_revenue_budget()"""
    try:
        data = revenue_budget_service.get_revenue_budget(
            db, Statistics_Date, Province_Code, Serverpart_ID,
            SPRegionType_ID, Revenue_Include
        )
        if data is None:
            return Result.fail(code=101, msg="查询失败，未录入预算数据！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueBudget 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")




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
    """获取全省计划营收分析 — 业务逻辑见 revenue_budget_service.get_province_revenue_budget()"""
    try:
        data = revenue_budget_service.get_province_revenue_budget(
            db, StatisticsDate, ProvinceCode, StatisticsType,
            SPRegionTypeID, ServerpartID, ShowWholeYear
        )
        if data is None:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetProvinceRevenueBudget 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== 支付/配送 =====
# 业务逻辑已迁移至 revenue_transaction_service
@router.get("/Revenue/GetMobileShare")
async def get_mobile_share(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取移动支付分账数据 — 业务逻辑见 revenue_transaction_service.get_mobile_share()"""
    try:
        start_d = StatisticsStartDate or Statistics_Date
        end_d = StatisticsEndDate or Statistics_Date
        data = revenue_transaction_service.get_mobile_share(
            db, Province_Code, start_d, end_d, Serverpart_ID, SPRegionType_ID
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMobileShare 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetMallDeliver")
async def get_mall_deliver(
    Province_Code: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    ShowCompareRate: bool = Query(False, description="是否计算增长率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商城配送数据 — 业务逻辑见 revenue_transaction_service.get_mall_deliver()"""
    try:
        start_d = StatisticsStartDate or Statistics_Date
        end_d = StatisticsEndDate or Statistics_Date
        data = revenue_transaction_service.get_mall_deliver(
            db, Province_Code, start_d, end_d, ShowCompareRate
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMallDeliver 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 客单交易分析 =====
# 业务逻辑已迁移至 revenue_transaction_service
@router.get("/Revenue/GetTransactionAnalysis")
async def get_transaction_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    ShowConsumptionLevel: bool = Query(False, description="是否显示消费水平占比"),
    ShowConvertRate: bool = Query(False, description="是否显示消费转化率"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区客单交易分析 — 业务逻辑见 revenue_transaction_service.get_transaction_analysis()"""
    try:
        data = revenue_transaction_service.get_transaction_analysis(
            db, Province_Code, Statistics_Date, Serverpart_ID
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetTransactionTimeAnalysis")
async def get_transaction_time_analysis(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区时段消费分析 — 业务逻辑见 revenue_transaction_service.get_transaction_time_analysis()"""
    try:
        data = revenue_transaction_service.get_transaction_time_analysis(
            db, Province_Code, Statistics_Date, Serverpart_ID, SPRegionType_ID, TimeSpan
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionTimeAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetTransactionConvert")
async def get_transaction_convert(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    TimeSpan: int = Query(4, description="时间间隔，默认4h"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取消费转化对比分析 — 业务逻辑见 revenue_transaction_service.get_transaction_convert()"""
    try:
        data = revenue_transaction_service.get_transaction_convert(
            db, Province_Code, Statistics_Date, Serverpart_ID, SPRegionType_ID, TimeSpan
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionConvert 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== 业态分析 =====
# 业务逻辑已迁移至 revenue_transaction_service
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
    """获取业态营收占比 — 业务逻辑见 revenue_transaction_service.get_business_trade_revenue()"""
    try:
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")
        data = revenue_transaction_service.get_business_trade_revenue(
            db, ProvinceCode, StatisticsDate, ServerpartId, SPRegionTypeID, BusinessTradeIds, DataType
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeRevenue 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBusinessTradeLevel")
async def get_business_trade_level(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeTrade: bool = Query(False, description="是否显示全部业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态消费水平占比 — 业务逻辑见 revenue_business_service.get_business_trade_level()"""
    try:
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")
        data = revenue_business_service.get_business_trade_level(
            db, ProvinceCode, StatisticsDate, ServerpartId, ShowWholeTrade
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeLevel 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetBusinessBrandLevel")
async def get_business_brand_level(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeBrand: bool = Query(True, description="是否显示全品牌"),
    ShowBrandCount: Optional[str] = Query("5", description="显示品牌数量"),
    SPRegionTypeID: Optional[str] = Query(None, description="片区ID"),
    BusinessTradeIds: Optional[str] = Query(None, description="业态ID"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取品牌消费水平占比 — 业务逻辑见 revenue_business_service.get_business_brand_level()"""
    try:
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")
        data = revenue_business_service.get_business_brand_level(
            db, ProvinceCode, StatisticsDate, ServerpartId, ShowWholeBrand, ShowBrandCount
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessBrandLevel 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== 营收趋势 =====
# 业务逻辑已迁移至 revenue_trend_service.get_revenue_trend()
# Router 只负责：参数解析 → 调用 Service → Result 包装


@router.get("/Revenue/GetRevenueTrend")
async def get_revenue_trend_get(
    request: Request,
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期(年份如2025)"),
    StatisticsType: int = Query(1, description="统计类型:1月度2日度4季度"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收趋势图（GET）— 业务逻辑见 revenue_trend_service.get_revenue_trend()"""
    try:
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        result_list = revenue_trend_service.get_revenue_trend(
            db, ProvinceCode, StatisticsDate, StatisticsType, ServerpartId, SPRegionTypeID
        )
        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueTrend 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 经营报表 =====

# 业务逻辑已迁移至 revenue_report_service

@router.get("/Revenue/GetRevenueReport")

async def get_revenue_report(

    provinceCode: Optional[str] = Query(None, description="省份编码"),

    startTime: Optional[str] = Query(None, description="开始时间"),

    endTime: Optional[str] = Query(None, description="结束时间"),

    SearchKeyType: Optional[str] = Query("", description="查询类型"),

    SearchKeyValue: Optional[str] = Query("", description="模糊查询内容"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取服务区经营报表 -- 业务逻辑见 revenue_report_service.get_revenue_report()"""

    try:

        data = revenue_report_service.get_revenue_report(db, provinceCode, startTime, endTime)

        if data is None:

            return Result.fail(code=200, msg="查询失败，无数数据返回！")

        return Result.success(data=data, msg="查询成功")

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

    """获取服务区经营报表详情 -- 业务逻辑见 revenue_report_service.get_revenue_report_detail()"""

    try:

        data = revenue_report_service.get_revenue_report_detail(

            db, provinceCode, serverpartId, startTime, endTime

        )

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetRevenueReportDetil 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")



# ===== 畅销商品 =====
# 业务逻辑已迁移至 revenue_trend_service.get_salable_commodity()
@router.get("/Revenue/GetSalableCommodity")
async def get_salable_commodity(
    statisticsDate: Optional[str] = Query(None, description="统计日期"),
    provinceCode: Optional[str] = Query(None, description="业主单位标识"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取商超畅销商品 — 业务逻辑见 revenue_trend_service.get_salable_commodity()"""
    return Result.success(data=revenue_trend_service.get_salable_commodity(), msg="查询成功")


# ===== 排行/同比 =====
@router.get("/Revenue/GetSPRevenueRank")
async def get_sp_revenue_rank(
    pushProvinceCode: Optional[str] = Query(None, description="推送省份"),
    Statistics_Date: Optional[str] = Query(None, description="统计日期"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    SPRegionType_ID: Optional[int] = Query(None, description="区域内码"),
    Revenue_Include: Optional[int] = Query(None, description="是否纳入营收(0否1是)"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取近日服务区营收排行 — 业务逻辑见 revenue_push_service.get_sp_revenue_rank()"""
    try:
        result_list, sum_cashpay = revenue_push_service.get_sp_revenue_rank(
            db, pushProvinceCode, Statistics_Date, Serverpart_ID,
            SPRegionType_ID, Revenue_Include
        )
        json_list = JsonListData(
            List=result_list, TotalCount=len(result_list),
            PageIndex=1, PageSize=10, OtherData=sum_cashpay
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPRevenueRank 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



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
    """获取每日营收同比数据 — 业务逻辑见 revenue_trend_service.get_revenue_yoy()"""
    try:
        data = revenue_trend_service.get_revenue_yoy(
            db, pushProvinceCode, StatisticsStartDate, StatisticsEndDate,
            CompareStartDate, CompareEndDate, ServerpartId, SPRegionTypeID
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueYOY 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


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

    """获取节日营收同比数据 -- 业务逻辑见 revenue_holiday_service.get_holiday_compare()"""

    try:

        data = revenue_holiday_service.get_holiday_compare(

            db, pushProvinceCode, curYear, compareYear,

            holidayType, StatisticsDate, ServerpartId, SPRegionTypeID

        )

        if data is None:

            return Result.fail(code=200, msg="查询失败，无数据返回！")

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetHolidayCompare (Revenue) 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")



# ===== 实时交易 =====

# 业务逻辑已迁移至 revenue_account_service

@router.get("/Revenue/GetAccountReceivable")

async def get_account_receivable(

    calcType: int = Query(1, description="计算方式：1当月 2累计"),

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsMonth: Optional[str] = Query(None, description="统计结束月份"),

    StatisticsStartMonth: Optional[str] = Query("", description="统计开始月份"),

    StatisticsDate: Optional[str] = Query("", description="统计日期"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取营收统计明细数据 -- 业务逻辑见 revenue_account_service.get_account_receivable()"""

    try:

        data = revenue_account_service.get_account_receivable(

            db, calcType, pushProvinceCode, StatisticsMonth,

            StatisticsStartMonth, StatisticsDate

        )

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetAccountReceivable 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")



@router.get("/Revenue/GetCurRevenue")

async def get_cur_revenue(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsDate: Optional[str] = Query(None, description="统计日期"),

    serverPartId: Optional[str] = Query("", description="服务区内码"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取实时营收交易数据 -- 业务逻辑见 revenue_account_service.get_cur_revenue()"""

    try:

        data = revenue_account_service.get_cur_revenue(db, pushProvinceCode, StatisticsDate, serverPartId)

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetCurRevenue 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")



@router.get("/Revenue/GetShopCurRevenue")

async def get_shop_cur_revenue(

    serverPartId: Optional[str] = Query(None, description="服务区内码"),

    statisticsDate: Optional[str] = Query(None, description="统计日期"),

    groupByShop: bool = Query(False, description="是否合并双侧同业态门店"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取实时门店营收交易数据 -- 业务逻辑见 revenue_account_service.get_shop_cur_revenue()"""

    try:

        data = revenue_account_service.get_shop_cur_revenue(db, serverPartId, statisticsDate, groupByShop)

        if data is None:

            return Result.fail(code=101, msg="查询失败，无数据返回！")

        json_list = JsonListData.create(data_list=data, total=len(data), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetShopCurRevenue 查询失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")



@router.get("/Revenue/GetLastSyncDateTime")

async def get_last_sync_date_time(db: DatabaseHelper = Depends(get_db)):

    """获取最新的同步日期 -- 业务逻辑见 revenue_account_service.get_last_sync_date_time()"""

    try:

        data = revenue_account_service.get_last_sync_date_time(db)

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetLastSyncDateTime 失败: {ex}")

        return Result.fail(msg=f"查询失败{ex}")



# ===== 节日分析 =====


# ===== 节日分析 =====

# _get_holiday_dates, _sum_compute 已迁移至 revenue_holiday_service

# GetHolidayAnalysis 核心逻辑已迁移至 revenue_holiday_service.get_holiday_analysis()



@router.get("/Revenue/GetHolidayAnalysis")

async def get_holiday_analysis(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    curYear: Optional[str] = Query(None, description="本年年份"),

    compareYear: Optional[str] = Query(None, description="历年年份"),

    HolidayType: int = Query(0, alias="HolidayType", description="节日类型"),

    StatisticsDate: Optional[str] = Query("", description="统计日期"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取节日营收数据对比分析 — 业务逻辑见 revenue_holiday_service.get_holiday_analysis()"""

    try:

        data = revenue_holiday_service.get_holiday_analysis(

            db, pushProvinceCode, curYear, compareYear,

            HolidayType, StatisticsDate, ServerpartId

        )

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetHolidayAnalysis 查询失败: {ex}")

        import traceback; traceback.print_exc()

        return Result.fail(msg=f"查询失败{ex}")





@router.get("/Revenue/GetHolidayAnalysisBatch")

async def get_holiday_analysis_batch(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    curYear: Optional[str] = Query(None, description="本年年份"),

    compareYear: Optional[str] = Query(None, description="历年年份"),

    HolidayType: int = Query(0, description="节日类型"),

    StatisticsDate: Optional[str] = Query("", description="统计日期"),

    ServerpartIds: Optional[str] = Query("", description="服务区内码集合"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取多个服务区节日营收数据对比分析（批量） — 循环调用 Service"""

    try:

        if not ServerpartIds:

            return Result.fail(code=102, msg="服务区内码不能为空！")



        sp_list = [s.strip() for s in ServerpartIds.split(",") if s.strip()]

        result_list = []



        for sp_id in sp_list:

            data = revenue_holiday_service.get_holiday_analysis(

                db, pushProvinceCode, curYear, compareYear,

                HolidayType, StatisticsDate, sp_id

            )

            if data:

                # 查询服务区名称

                sp_rows = db.execute_query(f'SELECT "SERVERPART_NAME" FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {sp_id}') or []

                sp_name = sp_rows[0].get("SERVERPART_NAME", "") if sp_rows else ""

                data["ServerpartId"] = int(sp_id) if sp_id.isdigit() else sp_id

                data["ServerpartName"] = sp_name

                data["curYear"] = int(curYear) if curYear else None

                data["compareYear"] = int(compareYear) if compareYear else None

                data["HolidayType"] = HolidayType

                # C# Batch版本不返回这些字段（初始化为null）

                for null_key in ["curYearSRRevenue", "lYearSRRevenue", "curYearSRAccount",

                                  "lYearSRAccount", "lYearGRORevenue", "curYearGROAccount", "lYearGROAccount"]:

                    if null_key in data:

                        data[null_key] = None

                result_list.append(data)



        if not result_list:

            return Result.fail(code=101, msg="查询失败，无数据返回！")



        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_index=1, page_size=len(result_list))

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetHolidayAnalysisBatch 查询失败: {ex}")

        import traceback; traceback.print_exc()

        return Result.fail(msg=f"查询失败{ex}")



        return Result.fail(msg=f"查询失败{ex}")


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
        holiday_names = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}

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
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_rev += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

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
            _sp_ids3 = parse_multi_ids(ServerpartId)
            if _sp_ids3:
                where_bay = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids3).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
            else:
                where_bay = f''' AND EXISTS (SELECT 1 FROM "T_SERVERPART" S WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {province_id})'''
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
            _sp_ids4 = parse_multi_ids(ServerpartId)
            if _sp_ids4:
                where_sp += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids4)
        if businessRegion == 1:
            where_sp += ' AND "SPREGIONTYPE_ID" NOT IN (89)'  # 排除城市店及商城（SPREGIONTYPE_ID=89），保留皖中管理中心（72）等
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

            def safe_or_none(d, key):
                """有数据返回float，无数据返回None
                注意：当 d 非空（即该服务区在SQL查询中有记录）但字段值为NULL时，
                C# 的 Convert.ToDecimal(DBNull) 返回 0，这里也需对齐返回 0.0
                """
                if not d:
                    return None
                v = d.get(key)
                if v is None:
                    # 字典存在说明有记录行，字段NULL视为0（对齐C#口径）
                    return 0.0
                try:
                    return float(v)
                except:
                    return 0.0

            rev_inc = make_inc(safe_or_none(cur_r, "REVENUE_AMOUNT"), safe_or_none(cy_r, "REVENUE_AMOUNT"))
            acc_inc = make_inc(safe_or_none(cur_r, "ACCOUNT_AMOUNT"), safe_or_none(cy_r, "ACCOUNT_AMOUNT"))
            bay_inc = make_inc(safe_or_none(cur_b, "SERVERPART_FLOW"), safe_or_none(cy_b, "SERVERPART_FLOW"))
            sec_inc = make_inc(safe_or_none(cur_b, "SECTIONFLOW_NUM"), safe_or_none(cy_b, "SECTIONFLOW_NUM"))

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
        holiday_period = f"{curYear}年{h_name}时间为{date_no_pad(stats_start)} 0:00:00至{stat_date.strftime('%Y-%m-%d')}\r\n{compareYear}年{h_name}时间为{date_no_pad(compare_start)} 0:00:00至{date_no_pad(compare_end)} 0:00:00"

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        resp = json_list.model_dump()
        resp["OtherData"] = holiday_period
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartINCAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Revenue/GetShopINCAnalysis")
async def get_shop_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: str = Query(..., description="省份编码"),
    curYear: int = Query(..., description="本年年份"),
    compareYear: int = Query(..., description="历年年份"),
    HolidayType: int = Query(..., description="节日类型：1元旦 2春运 3清明 4五一 5端午 6暑期 7中秋 8国庆"),
    ServerpartId: int = Query(..., description="服务区内码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    CurStartDate: Optional[str] = Query("", description="统计开始日期"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店营收增幅分析 (对齐C# HolidayHelper.GetShopINCAnalysis)"""
    try:
        from datetime import datetime as dt, timedelta

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        # 默认统计日期
        if not StatisticsDate:
            StatisticsDate = dt.now().strftime("%Y-%m-%d")

        # 解析统计日期
        if "-" in StatisticsDate:
            stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d")
        else:
            stat_date = dt.strptime(StatisticsDate, "%Y%m%d")

        # ========== 1. 获取节日日期范围 (对齐 CommonHelper.GetHoliday) ==========
        holiday_map = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}
        h_name = holiday_map.get(HolidayType, "")

        if HolidayType == 6:
            # 暑期固定
            statistics_start = dt(curYear, 7, 1)
            statistics_end = dt(curYear, 8, 31)
            compare_start = dt(compareYear, 7, 1)
            compare_end = dt(compareYear, 8, 31)
        elif HolidayType == 0:
            # 自定义日期范围
            if not CurStartDate:
                CurStartDate = StatisticsDate
            statistics_start = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y%m%d")
            statistics_end = stat_date
            compare_start = statistics_start.replace(year=statistics_start.year - 1)
            compare_end = statistics_end.replace(year=statistics_end.year - 1)
        else:
            # 从 T_HOLIDAY 表查询节日日期
            cur_desc = f"{curYear}年{h_name}"
            cmp_desc = f"{compareYear}年{h_name}"
            h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
                WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
            if not h_rows:
                return Result.fail(code=101, msg="查询失败，无数据返回！")

            def to_dt(v):
                if isinstance(v, dt): return v
                if hasattr(v, 'year'): return dt(v.year, v.month, v.day)
                if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
                return v

            cur_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
            cmp_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
            if not cur_dates or not cmp_dates:
                return Result.fail(code=101, msg="查询失败，无数据返回！")

            statistics_start = min(cur_dates)
            statistics_end = max(cur_dates)
            compare_start = min(cmp_dates)
            compare_end = max(cmp_dates)

            # 按节日类型调整日期范围 (对齐 C# switch)
            if HolidayType in (1, 3, 5, 7):
                # 元旦/清明/端午/中秋：开始前1天到开始后3天
                statistics_end = statistics_start + timedelta(days=3)
                statistics_start = statistics_start - timedelta(days=1)
                compare_end = compare_start + timedelta(days=3)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 4:
                # 五一：开始前1天到结束后1天
                statistics_end = statistics_end + timedelta(days=1)
                statistics_start = statistics_start - timedelta(days=1)
                compare_end = compare_end + timedelta(days=1)
                compare_start = compare_start - timedelta(days=1)
            elif HolidayType == 8:
                # 国庆
                if curYear == 2023:
                    statistics_start = dt(curYear, 9, 27)
                    statistics_end = dt(curYear, 10, 6)
                else:
                    statistics_start = dt(curYear, 9, 29)
                    statistics_end = dt(curYear, 10, 8)
                if compareYear == 2023:
                    compare_start = dt(compareYear, 9, 27)
                    compare_end = dt(compareYear, 10, 6)
                else:
                    compare_start = dt(compareYear, 9, 29)
                    compare_end = dt(compareYear, 10, 8)
            # HolidayType == 2 (春运): 使用原始日期不调整

        # 验证统计日期范围
        if stat_date < statistics_start:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        elif stat_date > statistics_end:
            stat_date = statistics_end

        # 处理 CurStartDate 与节日开始日期的偏移
        if CurStartDate:
            cur_start_dt = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y%m%d")
            if cur_start_dt > statistics_start:
                offset_days = (cur_start_dt - statistics_start).days
                compare_start = compare_start + timedelta(days=offset_days)
                statistics_start = cur_start_dt

        # ========== 2. 查询节日营收 (T_HOLIDAYREVENUE) ==========
        where_rev = f' AND A."SERVERPART_ID" = \'{ServerpartId}\''

        # 本年营收
        if calcType == 1:
            # 当日
            cur_rev_start = stat_date.strftime("%Y%m%d")
        else:
            cur_rev_start = statistics_start.strftime("%Y%m%d")
        cur_rev_end = stat_date.strftime("%Y%m%d")

        sql_cur_rev = f"""SELECT A."SERVERPARTSHOP_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {cur_rev_start} AND {cur_rev_end}{where_rev}
            GROUP BY A."SERVERPARTSHOP_ID" """
        dt_cur_rev = db.execute_query(sql_cur_rev) or []

        # 历年营收
        day_span = (stat_date - statistics_start).days
        cy_date = compare_start + timedelta(days=day_span)
        if calcType == 1:
            cmp_rev_start = cy_date.strftime("%Y%m%d")
        else:
            cmp_rev_start = compare_start.strftime("%Y%m%d")
        cmp_rev_end = cy_date.strftime("%Y%m%d")

        sql_cmp_rev = f"""SELECT A."SERVERPARTSHOP_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A
            WHERE A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {cmp_rev_start} AND {cmp_rev_end}{where_rev}
            GROUP BY A."SERVERPARTSHOP_ID" """
        dt_cmp_rev = db.execute_query(sql_cmp_rev) or []

        # ========== 关键判断：本年和历年营收都为空则返回 null/101 ==========
        if not dt_cur_rev and not dt_cmp_rev:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        # 构建查找映射
        cur_rev_map = {}
        for r in dt_cur_rev:
            sid = str(r.get("SERVERPARTSHOP_ID", ""))
            cur_rev_map[sid] = safe_dec(r.get("REVENUE_AMOUNT"))
        cmp_rev_map = {}
        for r in dt_cmp_rev:
            sid = str(r.get("SERVERPARTSHOP_ID", ""))
            cmp_rev_map[sid] = safe_dec(r.get("REVENUE_AMOUNT"))

        # ========== 3. 查询车流 (T_SECTIONFLOW / T_BAYONETDAILY_AH) ==========
        where_bay = f' AND A."SERVERPART_ID" = {ServerpartId}'

        # 本年车流
        if calcType == 1:
            sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {stat_date.strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        elif stat_date.year == 2024 and stat_date > dt(2024, 1, 28) and HolidayType == 2:
            sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {(statistics_start + timedelta(days=3)).strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        else:
            # 默认使用 T_BAYONETDAILY_AH
            sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."VEHICLE_COUNT") AS "SERVERPART_FLOW"
                FROM "T_BAYONETDAILY_AH" A
                WHERE A."INOUT_TYPE" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {statistics_start.strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        dt_cur_bay = db.execute_query(sql_cur_bay) or []

        # 历年车流
        if calcType == 1:
            sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {cy_date.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        elif stat_date.year == 2024 and stat_date > dt(2024, 1, 28) and HolidayType == 2:
            sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {(compare_start + timedelta(days=3)).strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        else:
            sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
                FROM "T_SECTIONFLOW" A
                WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                    AND A."STATISTICS_DATE" BETWEEN {compare_start.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
                GROUP BY A."SERVERPART_ID" """
        dt_cmp_bay = db.execute_query(sql_cmp_bay) or []

        # ========== 4. 查服务区基本信息 ==========
        sp_info = db.execute_query(f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME"
            FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {ServerpartId}""") or []
        sp_name = sp_info[0].get("SERVERPART_NAME", "") if sp_info else ""
        sp_region_id = sp_info[0].get("SPREGIONTYPE_ID") if sp_info else None
        sp_region_name = sp_info[0].get("SPREGIONTYPE_NAME", "") if sp_info else ""

        # ========== 5. 构建服务区级增幅模型 ==========
        def calc_inc(cur_val, cmp_val):
            """计算增长值和增长率"""
            result = {"curYearData": cur_val, "lYearData": cmp_val,
                      "increaseData": None, "increaseRate": None}
            if cur_val and cmp_val and cur_val != 0 and cmp_val != 0:
                inc = cur_val - cmp_val
                rate = round(inc / cmp_val * 100, 2)
                result["increaseData"] = round(inc, 2)
                result["increaseRate"] = rate
            return result

        # 服务区级营收汇总
        total_cur_rev = sum(cur_rev_map.values())
        total_cmp_rev = sum(cmp_rev_map.values())
        # 车流汇总
        total_cur_bay = sum(safe_dec(r.get("SERVERPART_FLOW")) for r in dt_cur_bay)
        total_cmp_bay = sum(safe_dec(r.get("SERVERPART_FLOW")) for r in dt_cmp_bay)

        revenue_inc = calc_inc(total_cur_rev, total_cmp_rev)
        bayonet_inc = calc_inc(total_cur_bay, total_cmp_bay)
        # 车流增长率超过1000没有可比性
        if bayonet_inc.get("increaseRate") and bayonet_inc["increaseRate"] > 1000:
            bayonet_inc["increaseData"] = None
            bayonet_inc["increaseRate"] = None

        # ========== 6. 查门店分组 (T_SERVERPARTSHOP) ==========
        sql_shop = f"""SELECT "SERVERPARTSHOP_ID", "SHOPTRADE", "SHOPSHORTNAME", "BUSINESS_BRAND"
            FROM "T_SERVERPARTSHOP"
            WHERE "SERVERPART_ID" = {ServerpartId} AND "SHOPTRADE" IS NOT NULL"""
        dt_shop = db.execute_query(sql_shop) or []

        # 按 SHOPTRADE+SHOPSHORTNAME 分组（C: WM_CONCAT）
        from collections import defaultdict
        shop_groups = defaultdict(lambda: {"ids": [], "brand": None, "name": ""})
        for s in dt_shop:
            key = (str(s.get("SHOPTRADE", "")), str(s.get("SHOPSHORTNAME", "")))
            shop_groups[key]["ids"].append(str(s.get("SERVERPARTSHOP_ID", "")))
            shop_groups[key]["name"] = str(s.get("SHOPSHORTNAME", ""))
            if s.get("BUSINESS_BRAND"):
                shop_groups[key]["brand"] = s.get("BUSINESS_BRAND")

        # ========== 7. 遍历门店，构建 ShopINCList ==========
        inc_list = []
        no_inc_list = []

        for (trade, shop_name), info in shop_groups.items():
            shop_ids = info["ids"]
            cur_sum = sum(cur_rev_map.get(sid, 0) for sid in shop_ids)
            cmp_sum = sum(cmp_rev_map.get(sid, 0) for sid in shop_ids)
            has_shop = any(sid in cur_rev_map for sid in shop_ids) or any(sid in cmp_rev_map for sid in shop_ids)

            if not has_shop:
                continue

            shop_model = {
                "ServerpartId": ServerpartId,
                "ServerpartName": sp_name,
                "ServerpartShopId": ",".join(shop_ids),
                "ServerpartShopName": info["name"],
                "RevenueINC": {
                    "curYearData": cur_sum if cur_sum else None,
                    "lYearData": cmp_sum if cmp_sum else None,
                    "increaseData": None,
                    "increaseRate": None,
                },
                "Brand_Id": None,
                "Brand_Name": None,
                "Brand_ICO": None,
                "CurTransaction": None,
            }

            if cur_sum and cur_sum != 0 and cmp_sum and cmp_sum != 0:
                inc_data = round(cur_sum - cmp_sum, 2)
                inc_rate = round(inc_data / cmp_sum * 100, 2)
                shop_model["RevenueINC"]["increaseData"] = inc_data
                shop_model["RevenueINC"]["increaseRate"] = inc_rate
                inc_list.append(shop_model)
            else:
                no_inc_list.append(shop_model)

        # 排序
        if SortStr:
            sort_lower = SortStr.lower()
            is_desc = sort_lower.endswith(" desc")
            sort_field = sort_lower.split(" ")[0]
            field_map = {
                "curyeardata": lambda x: x["RevenueINC"].get("curYearData") or 0,
                "lyeardata": lambda x: x["RevenueINC"].get("lYearData") or 0,
                "increasedata": lambda x: x["RevenueINC"].get("increaseData") or 0,
                "increaserate": lambda x: x["RevenueINC"].get("increaseRate") or 0,
            }
            key_fn = field_map.get(sort_field, lambda x: 0)
            inc_list.sort(key=key_fn, reverse=is_desc)

        # 合并：有增幅的在前，无增幅的在后
        all_shops = inc_list + no_inc_list

        # ========== 8. 构建最终返回结构 (HolidayIncreaseModel) ==========
        result_data = {
            "SPRegionTypeId": sp_region_id,
            "SPRegionTypeName": sp_region_name,
            "ServerpartId": ServerpartId,
            "ServerpartName": sp_name,
            "RevenueINC": revenue_inc,
            "AccountINC": {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None},
            "BayonetINC": bayonet_inc,
            "SectionFlowINC": None,
            "ShopINCList": all_shops,
        }

        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopINCAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== 月度经营 =====

# 业务逻辑已迁移至 revenue_monthly_service

@router.get("/Revenue/GetMonthlyBusinessAnalysis")

async def get_monthly_business_analysis(

    calcType: int = Query(1, description="计算方式：1当月 2累计"),

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    curYear: int = Query(None, description="本年年份"),

    compareYear: int = Query(None, description="历年年份"),

    StatisticsMonth: int = Query(None, description="统计月份"),

    StatisticsStartMonth: Optional[int] = Query(None, description="统计开始月份"),

    StatisticsDate: Optional[str] = Query("", description="统计日期"),

    SPRegionTypeId: Optional[str] = Query("", description="片区内码"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    businessType: Optional[str] = Query("", description="经营模式"),

    businessTrade: Optional[str] = Query("", description="经营业态"),

    businessRegion: Optional[str] = Query("", description="经营区域"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取月度经营增幅分析 -- 业务逻辑见 revenue_monthly_service.get_monthly_business_analysis()"""

    try:

        results = revenue_monthly_service.get_monthly_business_analysis(

            db, calcType, pushProvinceCode, curYear, compareYear,

            StatisticsMonth, StatisticsStartMonth, StatisticsDate,

            SPRegionTypeId, ServerpartId, businessType, businessTrade, businessRegion

        )

        json_list = JsonListData.create(data_list=results, total=len(results), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetMonthlyBusinessAnalysis 失败: {ex}")

        return Result.fail(msg=f"查询失败: {ex}")



@router.get("/Revenue/GetMonthlySPINCAnalysis")

async def get_monthly_sp_inc_analysis(

    request: Request,

    calcType: int = Query(1, description="计算方式：1当日 2累计"),

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    curYear: int = Query(None, description="本年年份"),

    compareYear: int = Query(None, description="历年年份"),

    StatisticsDate: Optional[str] = Query("", description="统计日期"),

    StatisticsMonth: int = Query(None, description="统计结束月份"),

    StatisticsStartMonth: Optional[int] = Query(None, description="统计开始月份"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    businessRegion: Optional[int] = Query(None, description="经营区域：1服务区 2城市店"),

    Dimension: Optional[str] = Query("", description="统计维度"),

    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),

    SortStr: Optional[str] = Query("", description="排序字段"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取服务区月度营收增幅分析 -- 业务逻辑见 revenue_monthly_service.get_monthly_sp_inc_analysis()"""

    try:

        results = revenue_monthly_service.get_monthly_sp_inc_analysis(

            db, calcType, pushProvinceCode, curYear, compareYear,

            StatisticsDate, StatisticsMonth, StatisticsStartMonth,

            ServerpartId, businessRegion, Dimension, SPRegionTypeID, SortStr

        )

        json_list = JsonListData.create(data_list=results, total=len(results), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetMonthlySPINCAnalysis 失败: {ex}")

        return Result.fail(msg=f"查询失败: {ex}")



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
    """获取实时交易明细 — 业务逻辑见 revenue_transaction_service.get_transaction_detail_list()"""
    try:
        data_list = revenue_transaction_service.get_transaction_detail_list(
            db, ProvinceCode, ServerpartId, ServerpartShopId, StartTime, EndTime
        )
        json_list = JsonListData.create(data_list=data_list, total=len(data_list),
                                        page_index=PageIndex, page_size=PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionDetailList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



@router.get("/Revenue/GetHolidayRevenueRatio")
async def get_holiday_revenue_ratio(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
):
    """获取节日营收占比（C#源码为纯静态硬编码，不查库）"""
    # 对应 C# HolidayHelper.GetHolidayRevenueRatio() — 全部硬编码
    holidays = [
        {"name": "元旦", "value": "0.65", "key": "1", "data": None},
        {"name": "春运", "value": "45.62", "key": "2", "data": None},
        {"name": "清明", "value": "2.55", "key": "3", "data": None},
        {"name": "五一", "value": "6.53", "key": "4", "data": None},
        {"name": "端午", "value": "3.43", "key": "5", "data": None},
        {"name": "暑期", "value": "34.19", "key": "6", "data": None},
        {"name": "中秋", "value": "1.27", "key": "7", "data": None},
        {"name": "国庆", "value": "8.76", "key": "8", "data": None},
    ]
    data_list = [
        {"node": {"name": "普通日", "value": "47.1", "key": "0", "data": None}, "children": None},
        {"node": {"name": "节假日", "value": "52.9", "key": "1", "data": None},
         "children": [{"node": h, "children": None} for h in holidays]},
    ]
    json_list = JsonListData.create(data_list=data_list, total=len(data_list))
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
        return Result.fail(msg="查询失败未将对象引用设置到对象的实例。")
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
        return Result.fail(msg="查询失败未将对象引用设置到对象的实例。")
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

    """按照安徽驿达子公司运营的门店返回经营数据报表 -- 业务逻辑见 revenue_report_service.get_company_revenue_report()"""

    try:

        result_list = revenue_report_service.get_company_revenue_report(

            db, ProvinceCode, StartTime, EndTime, ServerpartId

        )

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
    """获取营收同比环比对比数据 (C#完整平移)"""
    try:
        from datetime import datetime as dt

        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")

        def sf(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        if not StatisticsDate:
            return Result.success(data=None, msg="查询成功")

        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y%m%d")
        date_str = stat_date.strftime("%Y%m%d")
        yoy_date = stat_date.replace(year=stat_date.year - 1).strftime("%Y%m%d")

        # 省份映射
        fe_rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
            {"pc": ProvinceCode})
        province_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else ProvinceCode

        where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        elif SPRegionTypeID:
            where_sql += f' AND B."SPREGIONTYPE_ID" IN ({SPRegionTypeID})'

        is_history = stat_date < dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - __import__("datetime").timedelta(days=9)

        # 查当日营收
        if is_history:
            if not ServerpartId and not SPRegionTypeID:
                cur_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                    SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                    FROM "T_REVENUEDAILY" A
                    WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_DATE" = {date_str}"""
            else:
                cur_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                    SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                    FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                    WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql} AND A."STATISTICS_DATE" = {date_str}"""
        else:
            cur_sql = f"""SELECT SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
                SUM(A."TOTALCOUNT") AS "TOTALCOUNT", SUM(A."CASHPAY") AS "CASHPAY"
                FROM "T_ENDACCOUNT_TEMP" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."VALID" = 1
                AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql} AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
                AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1"""

        cur_rows = db.execute_query(cur_sql) or []
        rev = round(sf(cur_rows[0].get("CASHPAY")), 2) if cur_rows and sf(cur_rows[0].get("TICKETCOUNT")) > 0 else 0.0
        ticket = round(sf(cur_rows[0].get("TICKETCOUNT")), 2) if cur_rows and sf(cur_rows[0].get("TICKETCOUNT")) > 0 else 0.0
        avg_t = round(rev / ticket, 2) if ticket > 0 else 0.0

        # 查去年同日
        if not ServerpartId and not SPRegionTypeID:
            yoy_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_DATE" = {yoy_date}"""
        else:
            yoy_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql} AND A."STATISTICS_DATE" = {yoy_date}"""
        yoy_rows = db.execute_query(yoy_sql) or []
        yoy_rev = sf(yoy_rows[0].get("CASHPAY")) if yoy_rows else 0
        yoy_ticket = sf(yoy_rows[0].get("TICKETCOUNT")) if yoy_rows else 0
        yoy_avg = round(yoy_rev / yoy_ticket, 2) if yoy_ticket > 0 else 0.0

        rev_rate = round((rev - yoy_rev) / yoy_rev * 100, 2) if yoy_rev > 0 else None
        ticket_rate = round((ticket - yoy_ticket) / yoy_ticket * 100, 2) if yoy_ticket > 0 else None
        avg_rate = round((avg_t - yoy_avg) / yoy_avg * 100, 2) if yoy_avg > 0 else None

        # 趋势数据：工作日/周末/节假日月度平均
        year_str = stat_date.strftime("%Y")
        date_sql = f' AND A."STATISTICS_DATE" >= {year_str}0101 AND A."STATISTICS_DATE" <= {date_str}'

        if not ServerpartId and not SPRegionTypeID:
            trend_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        else:
            trend_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{date_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""

        trend_rows = db.execute_query(trend_sql) or []

        # 去年12月数据（用于1月环比）
        ly_dec_sql = date_sql.replace(date_sql, f' AND A."STATISTICS_DATE" >= {int(year_str)-1}1201 AND A."STATISTICS_DATE" <= {int(year_str)-1}1231')
        if not ServerpartId and not SPRegionTypeID:
            ly_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND A."PROVINCE_ID" = {province_id}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        else:
            ly_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
                UNION ALL
                SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                    FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                    FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                    AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                    AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                    AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                    {where_sql}{ly_dec_sql}
                GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        ly_rows = db.execute_query(ly_sql) or []

        # 查节假日名称
        hol_sql = f"""SELECT "HOLIDAY_NAME", TO_CHAR("HOLIDAY_DATE",'MM') AS "HOLIDAY_MONTH"
            FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DATE" >= TO_DATE('{year_str}/1/1','YYYY/MM/DD')
            AND "HOLIDAY_DATE" <= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
            GROUP BY "HOLIDAY_NAME", TO_CHAR("HOLIDAY_DATE",'MM')"""
        hol_rows = db.execute_query(hol_sql) or []

        # 构建trend map: {(data_type, month_str): {rev, ticket}}
        trend_map = {}
        for r in trend_rows:
            key = (int(sf(r.get("DATA_TYPE"))), str(r.get("STATISTICS", "")))
            trend_map[key] = {"rev": sf(r.get("REVENUE_AMOUNT")), "ticket": sf(r.get("TICKET_COUNT"))}
        for r in ly_rows:
            key = (int(sf(r.get("DATA_TYPE"))), str(r.get("STATISTICS", "")))
            trend_map[key] = {"rev": sf(r.get("REVENUE_AMOUNT")), "ticket": sf(r.get("TICKET_COUNT"))}

        # 节日名称map: {month: "name1、name2"}
        hol_map = {}
        for r in hol_rows:
            m = str(r.get("HOLIDAY_MONTH", "")).lstrip("0") or "0"
            m_key = m.zfill(2)
            name = str(r.get("HOLIDAY_NAME", ""))
            if m_key not in hol_map:
                hol_map[m_key] = name
            else:
                hol_map[m_key] += "、" + name

        # 构建3个List (工作日平均/周末平均/节假日平均)
        data_types = [("0", "工作日平均"), ("1", "周末平均"), ("2", "节假日平均")]
        rev_list, ticket_list, avg_list = [], [], []

        if trend_rows:
            for dt_idx, (dt_code, dt_name) in enumerate(data_types):
                rev_data = [None] * 12
                ticket_data = [None] * 12
                avg_data = [None] * 12
                # 节假日有value（节日名称）
                rev_value = [None] * 12 if dt_code == "2" else None
                ticket_value = [None] * 12 if dt_code == "2" else None
                avg_value = [None] * 12 if dt_code == "2" else None

                for m in range(1, 13):
                    month_key = f"{year_str}{m:02d}"
                    dt_int = int(dt_code)
                    info = trend_map.get((dt_int, month_key))

                    # C#: 如果工作日/周末没有当月数据，fallback到节假日
                    if info is None and dt_int < 2:
                        info = trend_map.get((2, month_key))

                    if dt_code == "2":
                        hname = hol_map.get(f"{m:02d}", "")
                        rev_value[m-1] = [str(m), hname]
                        ticket_value[m-1] = [str(m), hname]
                        avg_value[m-1] = [str(m), hname]

                    if info:
                        r_val = round(info["rev"], 2)
                        t_val = round(info["ticket"])
                        a_val = round(r_val / t_val, 2) if t_val > 0 else 0

                        # 计算增长率 (data[2])
                        rate_r, rate_t, rate_a = 0, 0, 0
                        if dt_idx == 0:  # 工作日：较上月增长率
                            if m == 1:
                                # 用去年12月
                                ly_key = (dt_int, f"{int(year_str)-1}12")
                                ly_info = trend_map.get(ly_key)
                                if ly_info and ly_info["rev"] > 0:
                                    rate_r = round((r_val / ly_info["rev"] - 1) * 100, 2)
                                if ly_info and ly_info["ticket"] > 0:
                                    rate_t = round((t_val / ly_info["ticket"] - 1) * 100, 2)
                                    ly_avg = ly_info["rev"] / ly_info["ticket"]
                                    if ly_avg > 0:
                                        rate_a = round((a_val / ly_avg - 1) * 100, 2)
                            else:
                                prev = rev_data[m-2]
                                if prev and prev[1] > 0:
                                    rate_r = round((r_val / prev[1] - 1) * 100, 2)
                                prev_t = ticket_data[m-2]
                                if prev_t and prev_t[1] > 0:
                                    rate_t = round((t_val / prev_t[1] - 1) * 100, 2)
                                prev_a = avg_data[m-2]
                                if prev_a and prev_a[1] > 0:
                                    rate_a = round((a_val / prev_a[1] - 1) * 100, 2)
                        elif dt_idx == 1:  # 周末：较工作日增长率
                            wd = rev_list[0]["data"][m-1] if rev_list else None
                            if wd and wd[1] > 0:
                                rate_r = round((r_val / wd[1] - 1) * 100, 2)
                            wd_t = ticket_list[0]["data"][m-1] if ticket_list else None
                            if wd_t and wd_t[1] > 0:
                                rate_t = round((t_val / wd_t[1] - 1) * 100, 2)
                            wd_a = avg_list[0]["data"][m-1] if avg_list else None
                            if wd_a and wd_a[1] > 0:
                                rate_a = round((a_val / wd_a[1] - 1) * 100, 2)

                        rev_data[m-1] = [float(m), float(r_val), float(rate_r)]
                        ticket_data[m-1] = [float(m), float(t_val), float(rate_t)]
                        avg_data[m-1] = [float(m), float(a_val), float(rate_a)]
                    else:
                        rev_data[m-1] = [float(m), 0.0, 0.0]
                        ticket_data[m-1] = [float(m), 0.0, 0.0]
                        avg_data[m-1] = [float(m), 0.0, 0.0]

                rev_list.append({"name": dt_name, "value": rev_value, "data": rev_data, "CommonScatterList": None})
                ticket_list.append({"name": dt_name, "value": ticket_value, "data": ticket_data, "CommonScatterList": None})
                avg_list.append({"name": dt_name, "value": avg_value, "data": avg_data, "CommonScatterList": None})

        return Result.success(data={
            "RevenueAmount": rev, "RevenueAmountYOYRate": rev_rate,
            "TicketCount": ticket, "TicketCountYOYRate": ticket_rate,
            "AvgTicketAmount": avg_t, "AvgTicketAmountRate": avg_rate,
            "RevenueAmountList": rev_list,
            "TicketCountList": ticket_list,
            "AvgTicketAmountList": avg_list,
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueCompare 查询失败: {ex}")
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
    """获取节假日服务区营收分析 — 业务逻辑见 revenue_holiday_service.get_holiday_spr_analysis()"""
    try:
        data = revenue_holiday_service.get_holiday_spr_analysis(
            db, pushProvinceCode, curYear, compareYear,
            HolidayType, StatisticsDate, businessType, businessTrade, businessRegion
        )
        json_list = JsonListData.create(data_list=data, total=len(data), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetHolidaySPRAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== GetHolidayDailyAnalysis =====

# 业务逻辑已迁移至 revenue_holiday_service

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

    """获取节假日各类项目所有天数对客分析 -- 业务逻辑见 revenue_holiday_service.get_holiday_daily_analysis()"""

    try:

        result_list = revenue_holiday_service.get_holiday_daily_analysis(

            db, pushProvinceCode, curYear, compareYear,

            HolidayType, StatisticsDate, SPRegionTypeId, ServerpartId,

            businessType, businessTrade, businessRegion

        )

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetHolidayDailyAnalysis 查询失败: {ex}")

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
    """获取月度经营增长分析 (对齐C# AccountHelper.GetMonthINCAnalysis)"""
    try:
        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        # 解析bool参数
        is_solid = str(solidType).lower() not in ("false", "0", "")
        is_calc_yoy = str(calcYOY).lower() == "true"
        is_calc_qoq = str(calcQOQ).lower() == "true"
        is_calc_bayonet = str(calcBayonet).lower() == "true"
        is_show_warning = str(showWarning).lower() == "true"
        wt = int(warningType) if warningType else None
        now_month = __import__("datetime").datetime.now().strftime("%Y%m")

        # C# 对齐第655行: GetSubType 递归展开业态子类型
        expanded_shop_trade = shopTrade
        if shopTrade:
            try:
                _bt_ids = [s.strip() for s in shopTrade.split(",") if s.strip()]
                _expanded = set(_bt_ids)
                _sub_rows = db.execute_query(
                    "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_PID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
                ) or []
                _changed = True
                while _changed:
                    _changed = False
                    for sr in _sub_rows:
                        sid = str(sr.get("AUTOSTATISTICS_ID") or "")
                        pid = str(sr.get("AUTOSTATISTICS_PID") or "")
                        if pid in _expanded and sid not in _expanded:
                            _expanded.add(sid)
                            _changed = True
                expanded_shop_trade = ",".join(_expanded)
            except Exception as ex_st:
                logger.warning(f"GetMonthINCAnalysis GetSubType 展开失败: {ex_st}")

        # --- C# BusinessTradeType 映射逻辑 ---
        # BusinessTradeType=1 → 自营餐饮: BUSINESS_TYPE=4000 AND SHOPTRADE=2
        # BusinessTradeType=2 → 自营非餐饮: BUSINESS_TYPE=4000 AND SHOPTRADE<>2
        # BusinessTradeType=3 → 非自营: BUSINESS_TYPE<>4000
        def _btt_where(prefix="A"):
            if not BusinessTradeType:
                return ""
            btt = BusinessTradeType.strip()
            btt_set = set(btt.replace(" ", "").split(","))
            if btt_set == {"1"}:
                return f' AND {prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" = 2'
            elif btt_set == {"2"}:
                return f' AND {prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" <> 2'
            elif btt_set == {"3"}:
                return f' AND {prefix}."BUSINESS_TYPE" <> 4000'
            elif btt_set == {"1","2"}:
                return f' AND {prefix}."BUSINESS_TYPE" = 4000'
            elif btt_set == {"1","3"}:
                return f' AND (({prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" = 2) OR {prefix}."BUSINESS_TYPE" <> 4000)'
            elif btt_set == {"2","3"}:
                return f' AND (({prefix}."BUSINESS_TYPE" = 4000 AND {prefix}."SHOPTRADE" <> 2) OR {prefix}."BUSINESS_TYPE" <> 4000)'
            return ""

        # 构建树形节点辅助函数（固化和非固化路径共用）
        def _make_inc(cur, yoy, qoq=None):
            """构建同比/环比增长结构，对齐旧接口 HolidayINCDetailModel"""
            cur_v = round(float(cur), 2) if cur is not None else None
            yoy_v = round(float(yoy), 2) if yoy is not None else None
            qoq_v = round(float(qoq), 2) if qoq is not None else None
            # C# 在 curYearData.TryParseToDecimal() != 0 时才算增长
            inc = None; rate = None; inc_qoq = None; rate_qoq = None
            if cur_v is not None and cur_v != 0:
                if yoy_v is not None and yoy_v != 0:
                    inc = round(cur_v - yoy_v, 2)
                    rate = round(inc / yoy_v * 100, 2)
                if qoq_v is not None and qoq_v != 0:
                    inc_qoq = round(cur_v - qoq_v, 2)
                    rate_qoq = round(inc_qoq / qoq_v * 100, 2)
            return {"curYearData": cur_v, "lYearData": yoy_v,
                    "increaseData": inc, "increaseRate": rate,
                    "QOQData": qoq_v, "increaseDataQOQ": inc_qoq, "increaseRateQOQ": rate_qoq, "rankNum": None}

        def _make_bayonet_region(cur, yoy, qoq=None, calc_yoy_flag=True, calc_qoq_flag=False):
            """BayonetINC: 对齐 C# BindMonthlySPINCAnalysis L2174-2246"""
            cur_v = round(float(cur), 2) if cur and float(cur) != 0 else (0.0 if cur is not None else None)
            yoy_v = round(float(yoy), 2) if yoy and float(yoy) != 0 else (0.0 if yoy is not None else None)
            qoq_v = round(float(qoq), 2) if qoq and float(qoq) != 0 else (0.0 if qoq is not None else None)
            can_calc = cur_v is not None and cur_v != 0
            inc = None; rate = None
            if can_calc and calc_yoy_flag and yoy_v is not None and yoy_v != 0:
                inc = round(cur_v - yoy_v, 2)
                rate = round(inc / yoy_v * 100, 2)
            inc_qoq = None; rate_qoq = None
            if can_calc and calc_qoq_flag and qoq_v is not None and qoq_v != 0:
                inc_qoq = round(cur_v - qoq_v, 2)
                rate_qoq = round(inc_qoq / qoq_v * 100, 2)
            return {"curYearData": cur_v if cur_v is not None else None,
                    "lYearData": yoy_v if calc_yoy_flag and yoy_v is not None else None,
                    "increaseData": inc, "increaseRate": rate,
                    "QOQData": qoq_v if calc_qoq_flag else None,
                    "increaseDataQOQ": inc_qoq, "increaseRateQOQ": rate_qoq, "rankNum": None}

        def _format_ico(ico_raw):
            if not ico_raw: return ""
            if ico_raw.startswith("http"): return ico_raw
            if "PictureManage" in ico_raw: return "https://user.eshangtech.com" + ("/" if not ico_raw.startswith("/") else "") + ico_raw
            return "https://api.eshangtech.com/EShangApiMain/" + ico_raw.lstrip("/")

        def _format_bp_date(date_obj):
            if not date_obj: return ""
            from datetime import datetime as dt_internal
            if isinstance(date_obj, dt_internal):
                return f"{date_obj.year}/{date_obj.month}/{date_obj.day}"
            s_date = str(date_obj).replace("T", " ").split(" ")[0].replace("-", "/")
            parts = s_date.split("/")
            if len(parts) == 3:
                return f"{parts[0]}/{int(parts[1])}/{int(parts[2])}"
            return s_date

        _BAYONET_NULL = _make_inc(None, None)  # C# new HolidayINCDetailModel() 默认全 null

        def _make_node(sp_region_id=None, sp_region_name=None, sp_id=None, sp_name=None,
                       rev_inc=None, acc_inc=None, bayonet=_BAYONET_NULL, bayonet_ori=None,
                       ticket=None, avg_ticket=None, shop_list=None):
            """构造与旧接口一致的 node 结构"""
            return {
                "SPRegionTypeId": sp_region_id, "SPRegionTypeName": sp_region_name,
                "ServerpartId": sp_id, "ServerpartName": sp_name,
                "RevenueINC": rev_inc or _make_inc(0, 0),
                "AccountINC": acc_inc or _make_inc(0, 0),
                "BayonetINC": bayonet, "TicketINC": ticket, "AvgTicketINC": avg_ticket,
                "BayonetINC_ORI": bayonet_ori, "SectionFlowINC": None,
                "ShopINCList": shop_list, "RankDiff": None,
                "Cost_Amount": None, "Ca_Cost": None, "Profit_Amount": None,
            }

        # --- 固化数据路径 ---
        if is_solid and StatisticsStartMonth == StatisticsEndMonth and StatisticsEndMonth != now_month:
            # C#: 查 T_BUSINESSWARNING 表
            # CompareField 由 warningType/showBayonet/showRevenue/showLevel 决定
            compare_field = ""
            if is_calc_yoy and wt:
                field_map = {1: "WARING_VUSPD", 2: "WARING_VUSHD", 3: "WARING_VURU", 4: "WARING_VDRD"}
                compare_field = field_map.get(wt, "")

            where_parts = f' AND A."STATISTICS_MONTH" = {StatisticsEndMonth}'
            if compare_field:
                warning_val = 1 if is_show_warning else 0
                where_parts += f' AND A."{compare_field}" = {warning_val}'
            _sp_ids = parse_multi_ids(ServerpartId)
            if _sp_ids:
                where_parts += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
            if BusinessTradeType:
                where_parts += f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
            # C# 对齐第746行: 过滤展开后的经营业态
            if expanded_shop_trade:
                where_parts += f' AND A."BUSINESS_TRADE" IN ({expanded_shop_trade})'

            solid_sql = f"""SELECT
                    A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPARTSHOP_ID",
                    A."SERVERPARTSHOP_NAME" AS "SHOPSHORTNAME",
                    A."STATISTICS_MONTH", A."REVENUE_AMOUNT", A."REVENUE_AMOUNT_YOY",
                    A."REVENUE_INCREASE_YOY", A."REVENUE_INCRATE_YOY",
                    A."REVENUE_AMOUNT_QOQ", A."REVENUE_INCREASE_QOQ", A."REVENUE_INCRATE_QOQ",
                    A."VEHICLE_COUNT", A."VEHICLE_COUNT_YOY",
                    A."VEHICLE_INCREASE_YOY", A."VEHICLE_INCRATE_YOY",
                    A."TICKET_COUNT", A."TICKET_COUNT_YOY", A."TICKET_COUNT_QOQ",
                    A."ROYALTY_THEORY", A."ROYALTY_THEORY_YOY", A."ROYALTY_THEORY_QOQ",
                    A."VEHICLE_COUNT_ORI", A."VEHICLE_COUNT_ORI_YOY",
                    A."DATATYPE", A."BUSINESS_TRADE",
                    A."BUSINESSTRADETYPE" AS "BUSINESS_TYPE",
                    A."BUSINESSPROJECT_ID",
                    A."BUSINESSWARNING_ID",
                    A."INCREASE_DIFF"
                FROM "T_BUSINESSWARNING" A
                WHERE A."DATATYPE" = 2{where_parts}"""

            cur_rows = db.execute_query(solid_sql) or []
            # Python 内存排序对齐旧接口 (按 BWID 升序)
            cur_rows.sort(key=lambda r: int(r.get("BUSINESSWARNING_ID") or 0))

            # 按服务区汇总
            sp_map = {}
            for r in cur_rows:
                sp_id = r.get("SERVERPART_ID")
                if sp_id not in sp_map:
                    sp_map[sp_id] = {
                        "SERVERPART_ID": sp_id,
                        "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                        "REVENUE": 0.0, "REVENUE_YOY": 0.0, "REVENUE_QOQ": 0.0,
                        "TICKET": 0.0, "TICKET_YOY": 0.0, "TICKET_QOQ": 0.0,
                        "ROYALTY": 0.0, "ROYALTY_YOY": 0.0, "ROYALTY_QOQ": 0.0,
                        "VEHICLE": 0.0, "VEHICLE_YOY": 0.0, "VEHICLE_QOQ": 0.0,
                        "VEHICLE_ORI": 0.0, "VEHICLE_ORI_YOY": 0.0,
                        "shops": []
                    }
                def _add_v(old, new):
                    if new is None: return old
                    return (old or 0.0) + float(new)
                
                sp_map[sp_id]["REVENUE"] = _add_v(sp_map[sp_id]["REVENUE"], r.get("REVENUE_AMOUNT"))
                sp_map[sp_id]["REVENUE_YOY"] = _add_v(sp_map[sp_id]["REVENUE_YOY"], r.get("REVENUE_AMOUNT_YOY"))
                sp_map[sp_id]["REVENUE_QOQ"] = _add_v(sp_map[sp_id]["REVENUE_QOQ"], r.get("REVENUE_AMOUNT_QOQ"))
                sp_map[sp_id]["TICKET"] = _add_v(sp_map[sp_id]["TICKET"], r.get("TICKET_COUNT"))
                sp_map[sp_id]["TICKET_YOY"] = _add_v(sp_map[sp_id]["TICKET_YOY"], r.get("TICKET_COUNT_YOY"))
                sp_map[sp_id]["TICKET_QOQ"] = _add_v(sp_map[sp_id]["TICKET_QOQ"], r.get("TICKET_COUNT_QOQ"))
                sp_map[sp_id]["ROYALTY"] = _add_v(sp_map[sp_id]["ROYALTY"], r.get("ROYALTY_THEORY"))
                sp_map[sp_id]["ROYALTY_YOY"] = _add_v(sp_map[sp_id]["ROYALTY_YOY"], r.get("ROYALTY_THEORY_YOY"))
                sp_map[sp_id]["ROYALTY_QOQ"] = _add_v(sp_map[sp_id]["ROYALTY_QOQ"], r.get("ROYALTY_THEORY_QOQ"))
                sp_map[sp_id]["VEHICLE"] = _add_v(sp_map[sp_id]["VEHICLE"], r.get("VEHICLE_COUNT"))
                sp_map[sp_id]["VEHICLE_YOY"] = _add_v(sp_map[sp_id]["VEHICLE_YOY"], r.get("VEHICLE_COUNT_YOY"))
                sp_map[sp_id]["VEHICLE_ORI"] = _add_v(sp_map[sp_id]["VEHICLE_ORI"], r.get("VEHICLE_COUNT_ORI"))
                sp_map[sp_id]["VEHICLE_ORI_YOY"] = _add_v(sp_map[sp_id]["VEHICLE_ORI_YOY"], r.get("VEHICLE_COUNT_ORI_YOY"))
                sp_map[sp_id]["shops"].append(r)

            # 查服务区所属片区（含排序索引）
            if sp_map:
                sp_ids_str = ",".join(str(k) for k in sp_map.keys())
                sp_info_sql = f"""SELECT "SERVERPART_ID", "SPREGIONTYPE_ID", "SPREGIONTYPE_NAME",
                        "SPREGIONTYPE_INDEX", "SERVERPART_INDEX"
                    FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({sp_ids_str})"""
                sp_info_rows = db.execute_query(sp_info_sql) or []
                sp_region = {r["SERVERPART_ID"]: (
                    r.get("SPREGIONTYPE_ID"), r.get("SPREGIONTYPE_NAME",""),
                    r.get("SPREGIONTYPE_INDEX", 0), r.get("SERVERPART_INDEX", 0)
                ) for r in sp_info_rows}
            else:
                sp_region = {}

            # 查服务区级车流数据（DATATYPE=ServerpartDataType）
            # C# 固化路径: dtCurBayonet 总是加载, dtQOQBayonet 由 calcQOQ 控制, dtYOYBayonet 由 calcYOY 控制
            has_analog = str(hasAnalog).lower() != "false"
            _sp_data_type = 1 if has_analog else 3  # C# L738
            if sp_map:
                _sp_in_flow = ",".join(str(k) for k in sp_map.keys())
                _flow_sql = f"""SELECT "SERVERPART_ID",
                        "VEHICLE_COUNT", "VEHICLE_COUNT_YOY", "VEHICLE_COUNT_QOQ",
                        "VEHICLE_COUNT_ORI", "VEHICLE_COUNT_ORI_YOY"
                    FROM "T_BUSINESSWARNING"
                    WHERE "DATATYPE" = {_sp_data_type} AND "STATISTICS_MONTH" = {StatisticsEndMonth}
                        AND "SERVERPART_ID" IN ({_sp_in_flow})"""
                _flow_rows = db.execute_query(_flow_sql) or []
                for fr in _flow_rows:
                    _sid = fr.get("SERVERPART_ID")
                    if _sid in sp_map:
                        # 当前车流（总是加载）
                        sp_map[_sid]["VEHICLE"] = safe_dec(fr.get("VEHICLE_COUNT"))
                        sp_map[_sid]["VEHICLE_ORI"] = safe_dec(fr.get("VEHICLE_COUNT_ORI"))
                        # 同比车流（仅 calcYOY 时有效）
                        if is_calc_yoy:
                            sp_map[_sid]["VEHICLE_YOY"] = safe_dec(fr.get("VEHICLE_COUNT_YOY"))
                            sp_map[_sid]["VEHICLE_ORI_YOY"] = safe_dec(fr.get("VEHICLE_COUNT_ORI_YOY"))
                        else:
                            sp_map[_sid]["VEHICLE_YOY"] = 0.0
                            sp_map[_sid]["VEHICLE_ORI_YOY"] = 0.0
                        # 环比车流（仅 calcQOQ 时有效）
                        if is_calc_qoq:
                            sp_map[_sid]["VEHICLE_QOQ"] = safe_dec(fr.get("VEHICLE_COUNT_QOQ"))
                        else:
                            sp_map[_sid]["VEHICLE_QOQ"] = 0.0
            # 批量查询门店品牌信息（T_SERVERPARTSHOP JOIN T_BRAND）和商户信息（T_BUSINESSPROJECT）
            _inc_shop_info = {}  # SERVERPARTSHOP_ID(int) → {品牌信息}
            _inc_bp_info = {}    # BUSINESSPROJECT_ID → {项目/商户信息}
            try:
                _all_ssids = set()
                _all_bpids = set()
                for spd in sp_map.values():
                    for s in spd["shops"]:
                        ssid_str = str(s.get("SERVERPARTSHOP_ID", ""))
                        for sid_part in ssid_str.split(","):
                            sid_part = sid_part.strip()
                            if sid_part.isdigit():
                                _all_ssids.add(int(sid_part))
                                break  # 只取第一个
                        bp_id = s.get("BUSINESSPROJECT_ID")
                        if bp_id:
                            _all_bpids.add(int(bp_id))
                if _all_ssids:
                    _ss_in = ",".join(str(i) for i in _all_ssids)
                    _ss_rows = db.execute_query(f"""SELECT S.SERVERPARTSHOP_ID, S.SHOPSHORTNAME,
                            S.BUSINESS_TRADE, S.BUSINESS_TRADENAME, S.SHOPTRADE, S.BUSINESS_BRAND,
                            S.SELLER_ID, S.SELLER_NAME,
                            B.BRAND_ID, B.BRAND_NAME AS BRAND_NAME2, B.BRAND_INTRO AS BRAND_ICO
                        FROM T_SERVERPARTSHOP S LEFT JOIN T_BRAND B ON S.BUSINESS_BRAND = B.BRAND_ID
                        WHERE S.SERVERPARTSHOP_ID IN ({_ss_in})""") or []
                    for sr in _ss_rows:
                        _inc_shop_info[str(sr["SERVERPARTSHOP_ID"])] = sr
                    logger.info(f"INC品牌查询: ssids={len(_all_ssids)}, 查到={len(_ss_rows)}, map_keys={list(_inc_shop_info.keys())[:5]}")
                if _all_bpids:
                    _bp_in = ",".join(str(i) for i in _all_bpids)
                    _bp_rows = db.execute_query(f"""SELECT BUSINESSPROJECT_ID, MERCHANTS_ID, MERCHANTS_NAME,
                            BUSINESSPROJECT_NAME, BUSINESS_TYPE, SETTLEMENT_MODES,
                            TO_CHAR(PROJECT_STARTDATE, 'YYYY/MM/DD') AS COMPACT_START,
                            TO_CHAR(PROJECT_ENDDATE, 'YYYY/MM/DD') AS COMPACT_END
                        FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID IN ({_bp_in})""") or []
                    for br in _bp_rows:
                        _inc_bp_info[str(br["BUSINESSPROJECT_ID"])] = br
            except Exception as _ex_info:
                logger.warning(f"GetMonthINCAnalysis 门店品牌/商户信息查询失败: {_ex_info}")

            # --- 按片区分组服务区（使用 INDEX 排序）---
            from collections import OrderedDict
            region_map = OrderedDict()
            sorted_sp_items = sorted(
                sp_map.items(),
                key=lambda x: (
                    sp_region.get(x[0], (None, "", 0, 0))[2] or 0,  # SPREGIONTYPE_INDEX
                    sp_region.get(x[0], (None, "", 0, 0))[0] or 0,  # SPREGIONTYPE_ID
                    sp_region.get(x[0], (None, "", 0, 0))[3] or 0,  # SERVERPART_INDEX
                    x[0]  # SERVERPART_ID fallback
                )
            )
            for sp_id, sp_data in sorted_sp_items:
                region_info = sp_region.get(sp_id, (None, "", 0, 0))
                rid, rname = region_info[0], region_info[1]
                if rid not in region_map:
                    region_map[rid] = {"name": rname, "sp_list": []}
                region_map[rid]["sp_list"].append((sp_id, sp_data))

            # --- 结果汇总与报文构造 ---
            total_rev, total_rev_yoy, total_rev_qoq = 0.0, 0.0, 0.0
            total_tic, total_tic_yoy, total_tic_qoq = 0.0, 0.0, 0.0
            total_roy, total_roy_yoy, total_roy_qoq = 0.0, 0.0, 0.0
            total_veh, total_veh_yoy, total_veh_qoq = 0.0, 0.0, 0.0
            total_veh_ori, total_veh_ori_yoy = 0.0, 0.0

            def _safe_add(old, new):
                if new is None: return old
                return (old or 0.0) + float(new)

            region_children = []
            _show_rev = int(showRevenue) if showRevenue else 0
            _show_bay = int(showBayonet) if showBayonet else 0
            _show_lvl = int(showLevel) if showLevel else 1
            for rid, rinfo in region_map.items():
                r_rev, r_rev_yoy, r_rev_qoq = 0.0, 0.0, 0.0
                r_tic, r_tic_yoy, r_tic_qoq = 0.0, 0.0, 0.0
                r_roy, r_roy_yoy, r_roy_qoq = 0.0, 0.0, 0.0
                r_veh, r_veh_yoy, r_veh_qoq = 0.0, 0.0, 0.0
                r_veh_ori, r_veh_ori_yoy = 0.0, 0.0

                sp_children = []
                for sp_id, sp_data in rinfo["sp_list"]:
                    # 累加指标到片区
                    r_rev = _safe_add(r_rev, sp_data["REVENUE"])
                    r_rev_yoy = _safe_add(r_rev_yoy, sp_data["REVENUE_YOY"])
                    r_rev_qoq = _safe_add(r_rev_qoq, sp_data["REVENUE_QOQ"])
                    r_tic = _safe_add(r_tic, sp_data["TICKET"])
                    r_tic_yoy = _safe_add(r_tic_yoy, sp_data["TICKET_YOY"])
                    r_tic_qoq = _safe_add(r_tic_qoq, sp_data["TICKET_QOQ"])
                    r_roy = _safe_add(r_roy, sp_data["ROYALTY"])
                    r_roy_yoy = _safe_add(r_roy_yoy, sp_data["ROYALTY_YOY"])
                    r_roy_qoq = _safe_add(r_roy_qoq, sp_data["ROYALTY_QOQ"])
                    r_veh = _safe_add(r_veh, sp_data["VEHICLE"])
                    r_veh_yoy = _safe_add(r_veh_yoy, sp_data["VEHICLE_YOY"])
                    r_veh_qoq = _safe_add(r_veh_qoq, sp_data.get("VEHICLE_QOQ", 0.0))
                    r_veh_ori = _safe_add(r_veh_ori, sp_data["VEHICLE_ORI"])
                    r_veh_ori_yoy = _safe_add(r_veh_ori_yoy, sp_data["VEHICLE_ORI_YOY"])

                    # 门店级处理
                    shop_inc_list = []
                    _sorted_shops = sorted(sp_data["shops"], key=lambda x: int(x.get("BUSINESSWARNING_ID") or 0))
                    for shop in _sorted_shops:
                        _ssid_str = str(shop.get("SERVERPARTSHOP_ID", ""))
                        _ssid_list = [s.strip() for s in _ssid_str.split(",") if s.strip()]
                        _si = {}
                        for _s in _ssid_list:
                            _cur_si = _inc_shop_info.get(_s)
                            if _cur_si:
                                if not _si: _si = _cur_si.copy()
                                else:
                                    # 合并业态、名称、商户、品牌
                                    for key in ["BUSINESS_TRADENAME", "SHOPTRADE"]:
                                        old_val = str(_si.get(key) or "")
                                        new_val = str(_cur_si.get(key) or "")
                                        if new_val and new_val not in old_val:
                                            _si[key] = f"{old_val},{new_val}" if old_val else new_val
                                    for key in ["SELLER_NAME", "SELLER_ID", "BRAND_ID", "BRAND_NAME", "BRAND_ICO"]:
                                        if _si.get(key) is None or not _si.get(key):
                                            _si[key] = _cur_si.get(key)
                        
                        _bp = _inc_bp_info.get(str(shop.get("BUSINESSPROJECT_ID")), {}) if shop.get("BUSINESSPROJECT_ID") else {}
                        _btt = int(safe_dec(shop.get("BUSINESS_TYPE", 0)))
                        _m_id = _bp.get("MERCHANTS_ID") or _si.get("SELLER_ID")
                        
                        s_rev = shop.get("REVENUE_AMOUNT"); s_tic = shop.get("TICKET_COUNT")
                        s_rev_yoy = shop.get("REVENUE_AMOUNT_YOY"); s_tic_yoy = shop.get("TICKET_COUNT_YOY")
                        s_rev_qoq = shop.get("REVENUE_AMOUNT_QOQ"); s_tic_qoq = shop.get("TICKET_COUNT_QOQ")
                        
                        s_avg_cur = round(float(s_rev) / float(s_tic), 2) if s_rev is not None and s_tic and float(s_tic) != 0 else None
                        s_avg_yoy = round(float(s_rev_yoy) / float(s_tic_yoy), 2) if s_rev_yoy is not None and s_tic_yoy and float(s_tic_yoy) != 0 else None
                        s_avg_qoq = round(float(s_rev_qoq) / float(s_tic_qoq), 2) if s_rev_qoq is not None and s_tic_qoq and float(s_tic_qoq) != 0 else None

                        shop_inc_list.append({
                            "ServerpartId": None, "ServerpartName": None, "ServerpartShopId": _ssid_str,
                            "ServerpartShopName": shop.get("SHOPSHORTNAME", ""),
                            "Brand_Id": int(safe_dec(_si.get("BRAND_ID") or 0)) or None,
                            "Brand_Name": _si.get("BRAND_NAME2") or _si.get("BRAND_NAME") or None,
                            "BrandType_Name": None, "Brand_ICO": _format_ico(_si.get("BRAND_ICO")),
                            "ShopTrade": int(_bp.get("BUSINESS_TYPE") or 0) if _bp else 0,
                            "BusinessTradeName": _si.get("BUSINESS_TRADENAME") or shop.get("SHOPSHORTNAME"),
                            "BusinessTradeType": _btt, "BusinessProjectId": shop.get("BUSINESSPROJECT_ID"),
                            "CompactStartDate": _format_bp_date(_bp.get("COMPACT_START")) or _format_bp_date(_bp.get("PROJECT_START")) or "",
                            "CompactEndDate": _format_bp_date(_bp.get("COMPACT_END")) or _format_bp_date(_bp.get("PROJECT_END")) or "",

                            "SettlementModes": int(_bp.get("SETTLEMENT_MODES")) if _bp.get("SETTLEMENT_MODES") is not None else None,
                            "BusinessType": _bp.get("BUSINESS_TYPE") if _bp.get("BUSINESS_TYPE") is not None else None,
                            "MERCHANTS_ID": float(_m_id) if _m_id is not None else None,
                            "MERCHANTS_ID_Encrypted": des_encrypt_id(_m_id),
                            "MERCHANTS_NAME": _bp.get("MERCHANTS_NAME") or _si.get("SELLER_NAME"),
                            "RevenueINC": _make_inc(s_rev, s_rev_yoy, s_rev_qoq),
                            "AccountINC": _make_inc(shop.get("ROYALTY_THEORY"), shop.get("ROYALTY_THEORY_YOY"), shop.get("ROYALTY_THEORY_QOQ")),
                            "TicketINC": _make_inc(s_tic, s_tic_yoy, s_tic_qoq),
                            "AvgTicketINC": _make_inc(s_avg_cur, s_avg_yoy, s_avg_qoq),
                            "CurTransaction": None, "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
                        })

                    # 服务区节点聚合
                    s_avg_cur = round(sp_data["REVENUE"] / sp_data["TICKET"], 2) if sp_data["TICKET"] and sp_data["TICKET"] != 0 else (0 if sp_data["TICKET"] == 0 else None)
                    s_avg_yoy = round(sp_data["REVENUE_YOY"] / sp_data["TICKET_YOY"], 2) if sp_data["TICKET_YOY"] and sp_data["TICKET_YOY"] != 0 else (0 if sp_data["TICKET_YOY"] == 0 else None)
                    s_avg_qoq = round(sp_data["REVENUE_QOQ"] / sp_data["TICKET_QOQ"], 2) if sp_data["TICKET_QOQ"] and sp_data["TICKET_QOQ"] != 0 else (0 if sp_data["TICKET_QOQ"] == 0 else None)

                    # 构建服务区级 BayonetINC (对齐 C# 签名)
                    _sp_bayonet = _make_bayonet_region(
                        sp_data["VEHICLE"], sp_data["VEHICLE_YOY"],
                        qoq=sp_data.get("VEHICLE_QOQ", 0.0),
                        calc_yoy_flag=is_calc_yoy, calc_qoq_flag=is_calc_qoq
                    )
                    _sp_bayonet_ori = {
                        "curYearData": round(sp_data["VEHICLE_ORI"], 2) if sp_data["VEHICLE_ORI"] else None,
                        "lYearData": round(sp_data["VEHICLE_ORI_YOY"], 2) if is_calc_yoy and sp_data["VEHICLE_ORI_YOY"] else None,
                        "increaseData": None, "increaseRate": None,
                        "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None
                    }
                    _sp_rev_inc = _make_inc(sp_data["REVENUE"], sp_data["REVENUE_YOY"], sp_data["REVENUE_QOQ"])

                    # --- C# showBayonet 过滤 (L2248-2262) ---
                    if _show_bay == 1:
                        if not ((_sp_bayonet.get("increaseData") or 0) > 0 or (_sp_bayonet.get("increaseDataQOQ") or 0) > 0):
                            continue
                    elif _show_bay == 2:
                        if not ((_sp_bayonet.get("increaseData") or 0) < 0 or (_sp_bayonet.get("increaseDataQOQ") or 0) < 0):
                            continue

                    # --- C# showRevenue 过滤 (L2774-2788) ---
                    if _show_rev == 1:
                        if not ((_sp_rev_inc.get("increaseData") or 0) > 0 or (_sp_rev_inc.get("increaseDataQOQ") or 0) > 0):
                            continue
                    elif _show_rev == 2:
                        if not ((_sp_rev_inc.get("increaseData") or 0) < 0 or (_sp_rev_inc.get("increaseDataQOQ") or 0) < 0):
                            continue

                    sp_children.append({
                        "node": _make_node(
                            sp_region_id=sp_region.get(sp_id, (None, "", 0, 0))[0],
                            sp_region_name=sp_region.get(sp_id, (None, "", 0, 0))[1],
                            sp_id=sp_id, sp_name=sp_data["SERVERPART_NAME"],
                            rev_inc=_sp_rev_inc,
                            acc_inc=_make_inc(sp_data["ROYALTY"], sp_data["ROYALTY_YOY"], sp_data["ROYALTY_QOQ"]),
                            ticket=_make_inc(sp_data["TICKET"], sp_data["TICKET_YOY"], sp_data["TICKET_QOQ"]),
                            bayonet=_sp_bayonet,
                            bayonet_ori=_sp_bayonet_ori,
                            avg_ticket=_make_inc(s_avg_cur, s_avg_yoy, s_avg_qoq),
                            shop_list=shop_inc_list if shop_inc_list else None,
                        ),
                        "children": None
                    })

                # C# L1798: 片区聚合从 filtered children (sp_children) 求和
                if sp_children:
                    def _sum_field(items, *keys):
                        """从 sp_children[i]['node'][key1][key2] 求和"""
                        t = 0.0
                        for item in items:
                            v = item.get("node", {})
                            for k in keys:
                                v = v.get(k) if isinstance(v, dict) else None
                                if v is None: break
                            if v is not None:
                                t += float(v)
                        return t if t != 0 else None

                    r_rev = _sum_field(sp_children, "RevenueINC", "curYearData")
                    r_rev_yoy = _sum_field(sp_children, "RevenueINC", "lYearData")
                    r_rev_qoq = _sum_field(sp_children, "RevenueINC", "QOQData")
                    r_tic = _sum_field(sp_children, "TicketINC", "curYearData")
                    r_tic_yoy = _sum_field(sp_children, "TicketINC", "lYearData")
                    r_tic_qoq = _sum_field(sp_children, "TicketINC", "QOQData")
                    r_roy = _sum_field(sp_children, "AccountINC", "curYearData")
                    r_roy_yoy = _sum_field(sp_children, "AccountINC", "lYearData")
                    r_roy_qoq = _sum_field(sp_children, "AccountINC", "QOQData")

                    r_avg_cur = round(r_rev / r_tic, 2) if r_rev and r_tic and r_tic != 0 else None
                    r_avg_yoy = round(r_rev_yoy / r_tic_yoy, 2) if r_rev_yoy and r_tic_yoy and r_tic_yoy != 0 else None
                    r_avg_qoq = round(r_rev_qoq / r_tic_qoq, 2) if r_rev_qoq and r_tic_qoq and r_tic_qoq != 0 else None

                    # C# L1909: 片区级 BayonetINC 仅 calcBayonet 时聚合，否则为全 null 对象
                    _r_bayonet = _make_inc(None, None)
                    if is_calc_bayonet:
                        _r_bay_cur = _sum_field(sp_children, "BayonetINC", "curYearData")
                        _r_bay_yoy = _sum_field(sp_children, "BayonetINC", "lYearData")
                        _r_bay_qoq = _sum_field(sp_children, "BayonetINC", "QOQData")
                        _r_bayonet = _make_bayonet_region(_r_bay_cur or 0, _r_bay_yoy or 0,
                            qoq=_r_bay_qoq or 0, calc_yoy_flag=is_calc_yoy, calc_qoq_flag=is_calc_qoq)

                    region_children.append({
                        "node": _make_node(
                            sp_region_id=rid, sp_region_name=rinfo["name"],
                            rev_inc=_make_inc(r_rev, r_rev_yoy, r_rev_qoq),
                            acc_inc=_make_inc(r_roy, r_roy_yoy, r_roy_qoq),
                            ticket=_make_inc(r_tic, r_tic_yoy, r_tic_qoq),
                            bayonet=_r_bayonet,
                            avg_ticket=_make_inc(r_avg_cur, r_avg_yoy, r_avg_qoq),
                        ),
                        "children": sp_children if sp_children else None
                    })

            # C# L1948: 根节点 summaryModel 从 region_children 求和
            def _sum_region(items, *keys):
                t = 0.0
                for item in items:
                    v = item.get("node", {})
                    for k in keys:
                        v = v.get(k) if isinstance(v, dict) else None
                        if v is None: break
                    if v is not None:
                        t += float(v)
                return t

            total_rev = _sum_region(region_children, "RevenueINC", "curYearData")
            total_rev_yoy = _sum_region(region_children, "RevenueINC", "lYearData")
            total_rev_qoq = _sum_region(region_children, "RevenueINC", "QOQData")
            total_tic = _sum_region(region_children, "TicketINC", "curYearData")
            total_tic_yoy = _sum_region(region_children, "TicketINC", "lYearData")
            total_tic_qoq = _sum_region(region_children, "TicketINC", "QOQData")
            total_roy = _sum_region(region_children, "AccountINC", "curYearData")
            total_roy_yoy = _sum_region(region_children, "AccountINC", "lYearData")
            total_roy_qoq = _sum_region(region_children, "AccountINC", "QOQData")

            t_avg_cur = round(total_rev / total_tic, 2) if total_rev and total_tic and total_tic != 0 else None
            t_avg_yoy = round(total_rev_yoy / total_tic_yoy, 2) if total_rev_yoy and total_tic_yoy and total_tic_yoy != 0 else None
            t_avg_qoq = round(total_rev_qoq / total_tic_qoq, 2) if total_rev_qoq and total_tic_qoq and total_tic_qoq != 0 else None

            # C# L2068: 根节点 BayonetINC 仅 calcBayonet 时聚合，否则为全 null 对象
            _t_bayonet = _make_inc(None, None)
            if is_calc_bayonet:
                _t_bay_cur = _sum_region(region_children, "BayonetINC", "curYearData")
                _t_bay_yoy = _sum_region(region_children, "BayonetINC", "lYearData")
                _t_bay_qoq = _sum_region(region_children, "BayonetINC", "QOQData")
                _t_bayonet = _make_bayonet_region(_t_bay_cur or 0, _t_bay_yoy or 0,
                    qoq=_t_bay_qoq or 0, calc_yoy_flag=is_calc_yoy, calc_qoq_flag=is_calc_qoq)

            result_list = [{
                "node": _make_node(
                    sp_name="合计",
                    rev_inc=_make_inc(total_rev, total_rev_yoy, total_rev_qoq),
                    acc_inc=_make_inc(total_roy, total_roy_yoy, total_roy_qoq),
                    ticket=_make_inc(total_tic, total_tic_yoy, total_tic_qoq),
                    bayonet=_t_bayonet,
                    avg_ticket=_make_inc(t_avg_cur, t_avg_yoy, t_avg_qoq),
                ),
                "children": region_children
            }]
            json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
            return Result(Result_Code=100, Result_Desc="查询成功", Result_Data=json_list.model_dump())

        # === 非固化路径（跨月或当前月）===
        # 从 T_BUSINESSWARNING(DATATYPE=2) 按 STATISTICS_MONTH BETWEEN start AND end 聚合
        _sp_ids = parse_multi_ids(ServerpartId)
        _nf_where = f' AND A."STATISTICS_MONTH" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}'
        if _sp_ids:
            _nf_where += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
        if BusinessTradeType:
            _nf_where += f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
        if expanded_shop_trade:
            _nf_where += f' AND A."BUSINESS_TRADE" IN ({expanded_shop_trade})'

        # 按服务区聚合本期营收/收入
        _nf_sql = f"""SELECT A."SERVERPART_ID", A."SERVERPART_NAME",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE",
                SUM(A."ROYALTY_THEORY") AS "ROYALTY",
                SUM(A."TICKET_COUNT") AS "TICKET"
            FROM "T_BUSINESSWARNING" A
            WHERE A."DATATYPE" = 2{_nf_where}
            GROUP BY A."SERVERPART_ID", A."SERVERPART_NAME" """
        _nf_rows = db.execute_query(_nf_sql) or []

        sp_map = {}
        for r in _nf_rows:
            sp_id = r.get("SERVERPART_ID")
            sp_map[sp_id] = {
                "SERVERPART_ID": sp_id, "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                "REVENUE": safe_dec(r.get("REVENUE")),
                "REVENUE_YOY": 0.0, "REVENUE_QOQ": 0.0,
                "TICKET": safe_dec(r.get("TICKET")),
                "TICKET_YOY": 0.0, "TICKET_QOQ": 0.0,
                "ROYALTY": safe_dec(r.get("ROYALTY")),
                "ROYALTY_YOY": 0.0, "ROYALTY_QOQ": 0.0,
                "VEHICLE": 0.0, "VEHICLE_YOY": 0.0, "VEHICLE_QOQ": 0.0,
                "VEHICLE_ORI": 0.0, "VEHICLE_ORI_YOY": 0.0,
                "shops": []
            }

        # 查服务区所属片区
        if sp_map:
            _sp_ids_str = ",".join(str(k) for k in sp_map.keys())
            _sp_info_sql = f"""SELECT "SERVERPART_ID", "SERVERPART_NAME", "SPREGIONTYPE_ID",
                    "SPREGIONTYPE_NAME", "SPREGIONTYPE_INDEX", "SERVERPART_INDEX"
                FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({_sp_ids_str})"""
            _sp_info_rows = db.execute_query(_sp_info_sql) or []
            sp_region = {r["SERVERPART_ID"]: (
                r.get("SPREGIONTYPE_ID"), r.get("SPREGIONTYPE_NAME", ""),
                r.get("SPREGIONTYPE_INDEX", 0), r.get("SERVERPART_INDEX", 0)
            ) for r in _sp_info_rows}
            for r in _sp_info_rows:
                sid = r["SERVERPART_ID"]
                if sid in sp_map:
                    sp_map[sid]["SERVERPART_NAME"] = r.get("SERVERPART_NAME", "")
        else:
            sp_region = {}

        # 构建树形（对齐 C# BindMonthlySPINCAnalysis）
        from collections import OrderedDict as _OD
        region_map = _OD()
        sorted_sp = sorted(sp_map.items(), key=lambda x: (
            sp_region.get(x[0], (None,"",0,0))[2] or 0,
            sp_region.get(x[0], (None,"",0,0))[0] or 0,
            sp_region.get(x[0], (None,"",0,0))[3] or 0, x[0]))
        for sp_id, sp_data in sorted_sp:
            ri = sp_region.get(sp_id, (None,"",0,0))
            rid, rname = ri[0], ri[1]
            if rid not in region_map:
                region_map[rid] = {"name": rname, "sp_list": []}
            region_map[rid]["sp_list"].append((sp_id, sp_data))

        region_children = []
        for rid, rinfo in region_map.items():
            sp_children = []
            for sp_id, sp_data in rinfo["sp_list"]:
                _ri = sp_region.get(sp_id, (None,"",0,0))
                _sp_avg = round(sp_data["REVENUE"] / sp_data["TICKET"], 2) if sp_data["TICKET"] and sp_data["TICKET"] != 0 else None
                sp_children.append({
                    "node": _make_node(
                        sp_region_id=_ri[0], sp_region_name=_ri[1],
                        sp_id=sp_id, sp_name=sp_data["SERVERPART_NAME"],
                        rev_inc=_make_inc(sp_data["REVENUE"], sp_data["REVENUE_YOY"], sp_data["REVENUE_QOQ"]),
                        acc_inc=_make_inc(sp_data["ROYALTY"], sp_data["ROYALTY_YOY"], sp_data["ROYALTY_QOQ"]),
                        ticket=_make_inc(sp_data["TICKET"], sp_data["TICKET_YOY"], sp_data["TICKET_QOQ"]),
                        bayonet=None,  # 非固化路径旧接口服务区级 BayonetINC=null
                        avg_ticket=_make_inc(_sp_avg, None),
                    ), "children": None
                })
            # 片区聚合从 sp_children
            if sp_children:
                def _nf_sum(items, *keys):
                    t = 0.0
                    for item in items:
                        v = item.get("node", {})
                        for k in keys:
                            v = v.get(k) if isinstance(v, dict) else None
                            if v is None: break
                        if v is not None: t += float(v)
                    return t if t != 0 else None

                _r_rev = _nf_sum(sp_children, "RevenueINC", "curYearData")
                _r_roy = _nf_sum(sp_children, "AccountINC", "curYearData")
                _r_tic = _nf_sum(sp_children, "TicketINC", "curYearData")
                _r_avg = round(_r_rev / _r_tic, 2) if _r_rev and _r_tic and _r_tic != 0 else None
                region_children.append({
                    "node": _make_node(
                        sp_region_id=rid, sp_region_name=rinfo["name"],
                        rev_inc=_make_inc(_r_rev, 0.0, 0.0),
                        acc_inc=_make_inc(_r_roy, 0.0, 0.0),
                        ticket=_make_inc(_r_tic, 0.0, 0.0),
                        avg_ticket=_make_inc(_r_avg, None),
                    ), "children": sp_children if sp_children else None
                })

        # 根节点聚合从 region_children
        def _nf_sum_r(items, *keys):
            t = 0.0
            for item in items:
                v = item.get("node", {})
                for k in keys:
                    v = v.get(k) if isinstance(v, dict) else None
                    if v is None: break
                if v is not None: t += float(v)
            return t if t != 0 else None

        t_rev = _nf_sum_r(region_children, "RevenueINC", "curYearData")
        t_roy = _nf_sum_r(region_children, "AccountINC", "curYearData")
        t_tic = _nf_sum_r(region_children, "TicketINC", "curYearData")
        t_avg = round(t_rev / t_tic, 2) if t_rev and t_tic and t_tic != 0 else None

        result_list = [{
            "node": _make_node(
                sp_name="\u5408\u8ba1",
                rev_inc=_make_inc(t_rev, 0.0, 0.0),
                acc_inc=_make_inc(t_roy, 0.0, 0.0),
                ticket=_make_inc(t_tic, 0.0, 0.0),
                avg_ticket=_make_inc(t_avg, None),
            ),
            "children": region_children if region_children else None
        }]
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result(Result_Code=100, Result_Desc="查询成功", Result_Data=json_list.model_dump())
    except Exception as ex:
        logger.error(f"GetMonthINCAnalysis 查询失败: {ex}")
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
    """汇总月度经营项目预警数值 (按C#逻辑重写：查T_BUSINESSWARNING)"""
    try:
        where_sql = ""
        if StatisticsStartMonth:
            where_sql += f' AND A."STATISTICS_MONTH" >= {StatisticsStartMonth}'
        if StatisticsEndMonth:
            where_sql += f' AND A."STATISTICS_MONTH" <= {StatisticsEndMonth}'

        # 经营业态过滤（子查询）
        shop_sql = ""
        if BusinessTradeType:
            shop_sql += f' AND B."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
        # C# 对齐第3678-3683行: GetSubType 递归展开业态子类型
        _expanded_trade = shopTrade
        if shopTrade:
            try:
                _bt_ids = [s.strip() for s in shopTrade.split(",") if s.strip()]
                _expanded = set(_bt_ids)
                _sub_rows = db.execute_query(
                    "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_PID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
                ) or []
                _changed = True
                while _changed:
                    _changed = False
                    for sr in _sub_rows:
                        sid = str(sr.get("AUTOSTATISTICS_ID") or "")
                        pid = str(sr.get("AUTOSTATISTICS_PID") or "")
                        if pid in _expanded and sid not in _expanded:
                            _expanded.add(sid)
                            _changed = True
                _expanded_trade = ",".join(_expanded)
            except Exception as ex_st:
                logger.warning(f"GetMonthINCAnalysisSummary GetSubType 展开失败: {ex_st}")
            shop_sql += f' AND B."BUSINESS_TRADE" IN ({_expanded_trade})'
        if shop_sql:
            shop_sql = f''' AND EXISTS (SELECT 1 FROM "T_BUSINESSWARNING" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND B."DATATYPE" = 2
                AND A."STATISTICS_MONTH" = B."STATISTICS_MONTH"{shop_sql})'''

        sql = f"""SELECT
                SUM(A."WARING_VUSPD") AS "WARING_VUSPD",
                SUM(A."WARING_VUSHD") AS "WARING_VUSHD",
                SUM(A."WARING_VURU") AS "WARING_VURU",
                SUM(A."WARING_VDRD") AS "WARING_VDRD"
            FROM "T_BUSINESSWARNING" A
            WHERE A."DATATYPE" = 1{where_sql}{shop_sql}"""
        rows = db.execute_query(sql) or []

        if rows and rows[0] and any(rows[0].get(k) is not None for k in ["WARING_VUSPD","WARING_VUSHD","WARING_VURU","WARING_VDRD"]):
            r = rows[0]
            def sv(v):
                return str(int(v)) if v is not None else "0"
            data_list = [
                {"name": "车流增加，服务区营收减少", "value": sv(r.get("WARING_VUSPD")), "data": None, "key": "1"},
                {"name": "车流增加，门店的营收减少", "value": sv(r.get("WARING_VUSHD")), "data": None, "key": "2"},
                {"name": "车流增加，营收增长不匹配", "value": sv(r.get("WARING_VURU")), "data": None, "key": "3"},
                {"name": "车流减少，营收降低不匹配", "value": sv(r.get("WARING_VDRD")), "data": None, "key": "4"},
            ]
        else:
            data_list = [
                {"name": "车流增加，服务区营收减少", "value": "0", "data": None, "key": "1"},
                {"name": "车流增加，门店的营收减少", "value": "0", "data": None, "key": "2"},
                {"name": "车流增加，营收增长不匹配", "value": "0", "data": None, "key": "3"},
                {"name": "车流减少，营收降低不匹配", "value": "0", "data": None, "key": "4"},
            ]

        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMonthINCAnalysisSummary 查询失败: {ex}")
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
        return Result.success(data=None, msg="生成成功")
    except Exception as ex:
        return Result.fail(msg=f"生成失败{ex}")


# ===== GetShopSABFIList =====
@router.get("/Revenue/GetShopSABFIList")
async def get_shop_sabfi_list(
    pushProvinceCode: str = Query(..., description="省份编码"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    statisticsStartMonth: Optional[str] = Query(None, description="统计开始月份（兼容前端）"),
    statisticsEndMonth: Optional[str] = Query(None, description="统计结束月份（兼容前端）"),
    ServerpartId: Optional[str] = Query("", description="服务区内码（支持逗号分隔多值）"),
    BusinessTradeType: Optional[str] = Query("", description="经营业态大类"),
    BusinessTrade: Optional[str] = Query("", description="经营业态"),
    accountType: int = Query(0, description="收入结算类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """月度服务区门店商业适配指数 — 对齐 C# AccountHelper.GetShopSABFIList"""
    try:
        stat_month = StatisticsMonth or statisticsStartMonth or statisticsEndMonth
        if not stat_month:
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        def safe_dec(v):
            try: return float(v) if v is not None else 0.0
            except: return 0.0

        def make_inc(cur=None, yoy=None, inc=None, rate=None, qoq=None, inc_qoq=None, rate_qoq=None):
            """构建 HolidayINCDetailModel — None 保持 None, QOQ 增量 0→None"""
            def _v(x):
                if x is None: return None
                try: return round(float(x), 2)
                except: return 0.0
            def _qv(x):
                """QOQ 值: None 和 0 都视为 None（C# 旧接口行为）"""
                if x is None: return None
                try:
                    val = round(float(x), 2)
                    return val if val != 0.0 else None
                except: return None
            return {
                "curYearData": _v(cur), "lYearData": _v(yoy),
                "increaseData": _v(inc), "increaseRate": _v(rate),
                "QOQData": _v(qoq), "increaseDataQOQ": _qv(inc_qoq),
                "increaseRateQOQ": _qv(rate_qoq), "rankNum": None
            }

        def empty_inc():
            return make_inc()

        # 辅助：Brand_ICO 格式化
        def _format_ico(ico_raw):
            if not ico_raw: return ""
            if ico_raw.startswith("http"): return ico_raw
            if "PictureManage" in ico_raw: return "https://user.eshangtech.com" + ("/" if not ico_raw.startswith("/") else "") + ico_raw
            return "https://api.eshangtech.com/EShangApiMain/" + ico_raw.lstrip("/")

        # 辅助：BP 日期格式化 (C# yyyy/M/d)
        def _format_bp_date(date_obj):
            if not date_obj: return ""
            from datetime import datetime as dt_internal
            if isinstance(date_obj, dt_internal):
                return f"{date_obj.year}/{date_obj.month}/{date_obj.day}"
            s_date = str(date_obj).replace("T", " ").split(" ")[0].replace("-", "/")
            parts = s_date.split("/")
            if len(parts) == 3:
                return f"{parts[0]}/{int(parts[1])}/{int(parts[2])}"
            return s_date

        # 多服务区ID兼容
        sp_where = ""
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            sp_where = " AND " + build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

        btt_where = ""
        if BusinessTradeType:
            btt_where = f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
        # C# 对齐: BusinessTrade 不在 SQL 中过滤，而是在遍历门店时用 T_SERVERPARTSHOP.BUSINESS_TRADE 做内存过滤
        # 先通过 GetSubType 递归展开业态子类型（查 T_AUTOSTATISTICS 树形结构）
        expanded_trades = set()
        if BusinessTrade:
            for bt_id in str(BusinessTrade).split(","):
                bt_id = bt_id.strip()
                if bt_id:
                    expanded_trades.add(bt_id)
                    # 递归查询子类型 (AUTOSTATISTICS_TYPE=2000 为经营业态分类)
                    queue = [bt_id]
                    while queue:
                        pid = queue.pop(0)
                        try:
                            sub_rows = db.execute_query(
                                f'SELECT "AUTOSTATISTICS_ID" FROM "T_AUTOSTATISTICS" '
                                f'WHERE "AUTOSTATISTICS_PID" = {pid} AND "AUTOSTATISTICS_TYPE" = 2000'
                            ) or []
                            for sr in sub_rows:
                                sid = str(sr.get("AUTOSTATISTICS_ID", ""))
                                if sid and sid not in expanded_trades:
                                    expanded_trades.add(sid)
                                    queue.append(sid)
                        except Exception:
                            pass

        # 从 T_BUSINESSWARNING 查固化数据（对齐 C#）
        sql = f"""SELECT
                A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPARTSHOP_ID",
                A."SERVERPARTSHOP_NAME" AS "SHOPSHORTNAME",
                A."REVENUE_AMOUNT", A."REVENUE_AMOUNT_YOY", A."REVENUE_INCREASE_YOY", A."REVENUE_INCRATE_YOY",
                A."REVENUE_AMOUNT_QOQ", A."REVENUE_INCREASE_QOQ", A."REVENUE_INCRATE_QOQ",
                A."TICKET_COUNT", A."TICKET_COUNT_YOY", A."TICKET_COUNT_QOQ",
                A."ROYALTY_THEORY", A."ROYALTY_THEORY_YOY", A."ROYALTY_THEORY_QOQ",
                A."VEHICLE_COUNT", A."VEHICLE_COUNT_YOY", A."VEHICLE_INCREASE_YOY", A."VEHICLE_INCRATE_YOY",
                A."VEHICLE_COUNT_QOQ", A."VEHICLE_INCREASE_QOQ", A."VEHICLE_INCRATE_QOQ",
                A."DATATYPE", A."BUSINESS_TRADE", A."BUSINESSTRADETYPE" AS "BUSINESS_TYPE",
                A."BUSINESSPROJECT_ID", A."BUSINESSWARNING_ID",
                A."REVENUE_SD", A."REVENUE_AVG"
            FROM "T_BUSINESSWARNING" A
            WHERE A."STATISTICS_MONTH" = {stat_month}
                AND A."DATATYPE" = 2{sp_where}{btt_where}
                AND A."SERVERPARTSHOP_NAME" NOT IN ('加油站便利店','客房')
            ORDER BY A."SERVERPART_ID" """
        rows = db.execute_query(sql) or []
        # Python 内存排序对齐旧接口 (按 BWID 升序)
        rows.sort(key=lambda r: int(r.get("BUSINESSWARNING_ID") or 0))

        # 查询门店盈利数据 (T_PERIODMONTHPROFIT)
        profit_map = {}
        sp_id_list = list(set(r.get("SERVERPART_ID") for r in rows if r.get("SERVERPART_ID")))
        last_month = str(int(stat_month) - 1) if str(stat_month).endswith(('02','03','04','05','06','07','08','09','10','11','12')) else str(int(stat_month) - 89)
        try:
            if sp_id_list:
                sp_in = ",".join(str(i) for i in sp_id_list)
                profit_sql = f"""SELECT SERVERPART_ID,
                        SUM(PROFIT_AMOUNT) AS PROFIT_AMOUNT,
                        SUM(COST_AMOUNT) AS COST_AMOUNT
                    FROM T_PERIODMONTHPROFIT
                    WHERE STATISTICS_MONTH BETWEEN {last_month} AND {stat_month}
                        AND SERVERPART_ID IN ({sp_in})
                    GROUP BY SERVERPART_ID"""
                profit_rows = db.execute_query(profit_sql) or []
                for pr in profit_rows:
                    profit_map[pr.get("SERVERPART_ID")] = pr
        except Exception as pe:
            logger.warning(f"GetShopSABFIList Profit查询失败: {pe}")

        # --- 查上月门店数据作为 QOQ 基数（C# 旧接口用上月 REVENUE_AMOUNT 作为 QOQData）---
        qoq_shop_map = {}  # { (SERVERPART_ID, SERVERPARTSHOP_NAME): {rev, roy, tic} }
        try:
            if sp_id_list:
                qoq_sql = f"""SELECT A."SERVERPART_ID", A."SERVERPARTSHOP_NAME",
                        A."REVENUE_AMOUNT", A."ROYALTY_THEORY", A."TICKET_COUNT"
                    FROM "T_BUSINESSWARNING" A
                    WHERE A."STATISTICS_MONTH" = {last_month}
                        AND A."DATATYPE" = 2{sp_where}
                        AND A."SERVERPARTSHOP_NAME" NOT IN ('加油站便利店','客房')"""
                qoq_rows = db.execute_query(qoq_sql) or []
                for qr in qoq_rows:
                    key = (qr.get("SERVERPART_ID"), qr.get("SERVERPARTSHOP_NAME"))
                    qoq_shop_map[key] = {
                        "rev": qr.get("REVENUE_AMOUNT"),
                        "roy": qr.get("ROYALTY_THEORY"),
                        "tic": qr.get("TICKET_COUNT"),
                    }
        except Exception as qe:
            logger.warning(f"GetShopSABFIList QOQ上月数据查询失败: {qe}")

        # --- 查询门店级门牌信息（Brand/商户/项目）用于 ShopSABFIList 构造 ---
        shop_agg_map = {}   # { ssid_str : { agg_info } }
        bp_info_map = {}    # { BUSINESSPROJECT_ID : { project 信息 } }
        try:
            if sp_id_list:
                # 1. 收集所有涉及的 ShopId
                all_ids_to_query = set()
                all_bp_ids = set()
                ssid_list_map = {}  # ssid_str -> list[int]
                
                for r in rows:
                    ssid_str = str(r.get("SERVERPARTSHOP_ID") or "")
                    if ssid_str:
                        ids = [int(i.strip()) for i in ssid_str.split(",") if i.strip().isdigit()]
                        ssid_list_map[ssid_str] = ids
                        all_ids_to_query.update(ids)
                    
                    bp_id = r.get("BUSINESSPROJECT_ID")
                    if bp_id is not None:
                        all_bp_ids.add(int(bp_id))

                # 2. 批量查 T_SERVERPARTSHOP -> T_BRAND
                raw_shop_map = {}
                if all_ids_to_query:
                    ss_in = ",".join(str(i) for i in all_ids_to_query)
                    ss_sql = f"""SELECT S.SERVERPARTSHOP_ID, S.SHOPSHORTNAME,
                            S.BUSINESS_BRAND, S.BRAND_NAME, S.BUSINESS_TRADE,
                            S.BUSINESS_TRADENAME, S.SHOPTRADE, S.BUSINESS_STATE,
                            S.SELLER_ID, S.SELLER_NAME,
                            B.BRAND_ID, B.BRAND_NAME AS BRAND_NAME2, B.BRAND_INTRO AS BRAND_ICO
                        FROM T_SERVERPARTSHOP S
                        LEFT JOIN T_BRAND B ON S.BUSINESS_BRAND = B.BRAND_ID
                        WHERE S.SERVERPARTSHOP_ID IN ({ss_in})"""
                    ss_rows = db.execute_query(ss_sql) or []
                    for sr in ss_rows:
                        raw_shop_map[int(sr["SERVERPARTSHOP_ID"])] = sr

                # 3. 对每个 ssid_str 聚合计算
                for ssid_str, id_list in ssid_list_map.items():
                    infos = [raw_shop_map[i] for i in id_list if i in raw_shop_map]
                    if not infos:
                        shop_agg_map[ssid_str] = None
                        continue
                    
                    # 行业聚合：(ID, Name) 组合去重 + ID 升序排序 (对齐 SP=420 等合并门店)
                    trade_pairs = []
                    seen_tids = set()
                    for inf in infos:
                        tids = str(inf.get("BUSINESS_TRADE") or "").split(",")
                        tnames = str(inf.get("BUSINESS_TRADENAME") or "").split(",")
                        for i in range(max(len(tids), len(tnames))):
                            tid = tids[i].strip() if i < len(tids) else ""
                            tname = tnames[i].strip() if i < len(tnames) else ""
                            if tid and tid not in seen_tids:
                                trade_pairs.append((tid, tname))
                                seen_tids.add(tid)
                    
                    # 排序
                    trade_pairs.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 99999)
                    
                    # 品牌筛选：取 MIN(BRAND_ID) 记录
                    brand_info_node = None
                    valid_brand_infos = [inf for inf in infos if inf.get("BRAND_ID")]
                    if valid_brand_infos:
                        brand_info_node = min(valid_brand_infos, key=lambda x: x["BRAND_ID"])
                    else:
                        brand_info_node = infos[0]

                    shop_agg_map[ssid_str] = {
                        "BUSINESS_TRADE": ",".join(p[0] for p in trade_pairs),
                        "BUSINESS_TRADENAME": ",".join(p[1] for p in trade_pairs),
                        "BUSINESS_BRAND": brand_info_node.get("BUSINESS_BRAND"),
                        "BRAND_NAME": brand_info_node.get("BRAND_NAME"),
                        "BRAND_ID": brand_info_node.get("BRAND_ID"),
                        "BRAND_NAME2": brand_info_node.get("BRAND_NAME2"),
                        "BRAND_ICO": brand_info_node.get("BRAND_ICO"),
                        "SHOPTRADE": brand_info_node.get("SHOPTRADE"),
                        "SELLER_ID": brand_info_node.get("SELLER_ID"),
                        "SELLER_NAME": brand_info_node.get("SELLER_NAME"),
                        "BUSINESS_STATE": brand_info_node.get("BUSINESS_STATE")
                    }

                # 批量查 T_BUSINESSPROJECT（取 商户/项目 信息）
                if all_bp_ids:
                    bp_in = ",".join(str(i) for i in all_bp_ids)
                    bp_sql = f"""SELECT BUSINESSPROJECT_ID, BUSINESSPROJECT_NAME,
                            MERCHANTS_ID, MERCHANTS_NAME,
                            BUSINESS_TYPE, SETTLEMENT_MODES,
                            PROJECT_STARTDATE, PROJECT_ENDDATE
                        FROM T_BUSINESSPROJECT
                        WHERE BUSINESSPROJECT_ID IN ({bp_in})"""
                    bp_rows = db.execute_query(bp_sql) or []
                    for br in bp_rows:
                        bp_info_map[br["BUSINESSPROJECT_ID"]] = br

                # MERCHANTS fallback: 当 T_BUSINESSPROJECT 无 MERCHANTS 时，取 T_SERVERPARTSHOP.SELLER_ID/NAME
                brand_merchant_map = {}  # 已废弃，改用 shop_info_map 中的 SELLER_ID
        except Exception as ex_s:
            logger.warning(f"GetShopSABFIList 门店/品牌信息查询失败: {ex_s}")

        # --- 查 T_PROFITCONTRIBUTE 获取 SABFI 评分项目列表 ---
        sabfi_projects_map = {}  # { SERVERPART_ID: [ { BusinessProjectId, SABFIList, ... } ] }
        try:
            if sp_id_list:
                # C# 对齐第3888行: CALCULATE_SELFSHOP 条件（联营=2, 非联营=1）
                selfshop_val = 2 if BusinessTradeType == "3" else 1
                project_sql = f"""SELECT A.SERVERPART_ID, A.BUSINESSPROJECT_ID, B.BUSINESSPROJECT_NAME,
                                         A.EVALUATE_TYPE, A.EVALUATE_SCORE, A.PROFITCONTRIBUTE_ID, A.PROFITCONTRIBUTE_PID,
                                         A.SERVERPARTSHOP_NAME
                                  FROM T_PROFITCONTRIBUTE A
                                  LEFT JOIN T_BUSINESSPROJECT B ON A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
                                  WHERE A.STATISTICS_DATE = {stat_month}
                                    AND A.PROFITCONTRIBUTE_STATE = 1
                                    AND A.SERVERPART_ID IN ({sp_in})
                                    AND A.CALCULATE_SELFSHOP = {selfshop_val}
                                  ORDER BY A.SERVERPART_ID, A.BUSINESSPROJECT_ID, A.EVALUATE_TYPE"""
                project_rows = db.execute_query(project_sql) or []

                temp_sp_projects = {}
                for pr in project_rows:
                    sid = pr["SERVERPART_ID"]
                    pid = pr["BUSINESSPROJECT_ID"]
                    shop_name = pr.get("SERVERPARTSHOP_NAME", "")
                    # C# 对齐: 用 (SERVERPART_ID, BUSINESSPROJECT_ID 或 SERVERPARTSHOP_NAME) 分组
                    key = (sid, pid) if pid is not None else (sid, f"_name_{shop_name}")
                    if key not in temp_sp_projects:
                        temp_sp_projects[key] = {
                            "BusinessProjectId": pid,
                            "BusinessProjectName": pr.get("BUSINESSPROJECT_NAME") or shop_name,
                            "SABFI_Score": 0.0,
                            "SABFIList": [{"name": str(et), "value": "", "key": "", "data": ""} for et in range(1, 8)],
                            "StatisticsMonth": f"{stat_month[:4]}/{stat_month[4:]}",
                            "Overall_Score": 0.0,
                        }

                    et = int(pr["EVALUATE_TYPE"])
                    score = pr["EVALUATE_SCORE"]
                    if et == 0:
                        temp_sp_projects[key]["SABFI_Score"] = safe_dec(score)
                        temp_sp_projects[key]["Overall_Score"] = safe_dec(score)
                    elif 1 <= et <= 7:
                        idx = et - 1
                        # C# 对齐: TryParseToDecimal().ToString()，整数显示无小数位，None 显示为空
                        _score_str = ""
                        if score is not None:
                            _sv = float(score)
                            _score_str = str(int(_sv)) if _sv == int(_sv) else str(_sv)
                        temp_sp_projects[key]["SABFIList"][idx]["value"] = _score_str
                        temp_sp_projects[key]["SABFIList"][idx]["key"] = str(pr["PROFITCONTRIBUTE_ID"] or "")
                        temp_sp_projects[key]["SABFIList"][idx]["data"] = str(pr["PROFITCONTRIBUTE_PID"] or "")

                for (sid, pid), p_data in temp_sp_projects.items():
                    if sid not in sabfi_projects_map:
                        sabfi_projects_map[sid] = []
                    sabfi_projects_map[sid].append(p_data)
        except Exception as ex_p:
            logger.warning(f"GetShopSABFIList 经营项目查询失败: {ex_p}")

        # 服务区车流数据 (DATATYPE=1)
        sql_flow = f"""SELECT A."SERVERPART_ID",
                A."VEHICLE_COUNT" AS "SERVERPART_FLOW",
                A."VEHICLE_COUNT_YOY", A."VEHICLE_INCREASE_YOY", A."VEHICLE_INCRATE_YOY",
                A."VEHICLE_COUNT_QOQ", A."VEHICLE_INCREASE_QOQ", A."VEHICLE_INCRATE_QOQ"
            FROM "T_BUSINESSWARNING" A
            WHERE A."STATISTICS_MONTH" = {stat_month} AND A."DATATYPE" = 1{sp_where}"""
        flow_rows = db.execute_query(sql_flow) or []
        flow_map = {}
        for fr in flow_rows:
            flow_map[fr.get("SERVERPART_ID")] = fr

        # 查服务区所属片区信息（含排序索引 SPREGIONTYPE_INDEX / SERVERPART_INDEX）
        sp_id_list_for_info = list(set(r.get("SERVERPART_ID") for r in rows if r.get("SERVERPART_ID")))
        sp_info_map = {}
        if sp_id_list_for_info:
            sp_in_info = ",".join(str(i) for i in sp_id_list_for_info)
            sp_info_sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME,
                    SPREGIONTYPE_ID, SPREGIONTYPE_NAME,
                    SPREGIONTYPE_INDEX, SERVERPART_INDEX
                FROM T_SERVERPART
                WHERE SPREGIONTYPE_ID IS NOT NULL
                    AND SERVERPART_ID IN ({sp_in_info})"""
            sp_info_rows = db.execute_query(sp_info_sql) or []
            for si in sp_info_rows:
                sp_info_map[si.get("SERVERPART_ID")] = si

        # 按服务区分组
        from collections import OrderedDict
        sp_groups = OrderedDict()
        for r in rows:
            sp_id = r.get("SERVERPART_ID")
            if sp_id not in sp_groups:
                sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "shops": []}
            sp_groups[sp_id]["shops"].append(r)

        # 构建 ShopSABFIList 中的门店项 — 对齐 C# ShopSABFIModel 字段
        def build_shop_sabfi_item(r, sp_id, sp_name):
            """从 T_BUSINESSWARNING 行 + JOIN 信息构建门店级 ShopSABFI 项"""
            # 日期格式化内置函数
            def fmt_date(v):
                if v is None: return ""
                try:
                    from datetime import datetime as _dt
                    if hasattr(v, 'year'): return f"{v.year}/{v.month}/{v.day}"
                    s = str(v).replace("T", " ")[:19]
                    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
                        try:
                            dt = _dt.strptime(s[:len(fmt.replace('%Y','0000').replace('%m','00').replace('%d','00'))], fmt)
                            return f"{dt.year}/{dt.month}/{dt.day}"
                        except: continue
                    return str(v).split()[0].replace("-","/")
                except: return str(v) if v else ""

            ssid_str = str(r.get("SERVERPARTSHOP_ID") or "")
            si = shop_agg_map.get(ssid_str) or {}
            bp_info = bp_info_map.get(r.get("BUSINESSPROJECT_ID")) or {}

            # 根据 BUSINESSTRADETYPE (BTT) 判断
            btt = r.get("BUSINESS_TYPE")  # 联营标识字段
            
            biz_trade = str(si.get("BUSINESS_TRADE") or "")
            biz_trade_name = str(si.get("BUSINESS_TRADENAME") or "")
            shop_trade_val = str(si.get("SHOPTRADE") or "")

            brand_id = si.get("BRAND_ID") or si.get("BUSINESS_BRAND")
            brand_name = si.get("BRAND_NAME2") or si.get("BRAND_NAME")
            brand_ico_raw = si.get("BRAND_ICO") or ""
            brand_ico = ""
            if brand_ico_raw:
                if brand_ico_raw.startswith("http"):
                    brand_ico = brand_ico_raw
                elif "PictureManage" in brand_ico_raw:
                    # 传统的 e2 图片路径
                    brand_ico = "https://user.eshangtech.com" + ("/" if not brand_ico_raw.startswith("/") else "") + brand_ico_raw
                else:
                    # 新的 EShangApiMain 路径
                    brand_ico = "https://api.eshangtech.com/EShangApiMain/" + brand_ico_raw.lstrip("/")

            merch_id = bp_info.get("MERCHANTS_ID")
            merch_name = bp_info.get("MERCHANTS_NAME") or None
            if merch_name is None:
                merch_id = si.get("SELLER_ID")
                merch_name = si.get("SELLER_NAME")
            merch_id_enc = des_encrypt_id(merch_id)  # DES 加密 MERCHANTS_ID

            # 门店级 QOQ 数据
            shop_name = r.get("SHOPSHORTNAME", r.get("SERVERPARTSHOP_NAME", ""))
            rev = safe_dec(r.get("REVENUE_AMOUNT"))
            rev_qoq_raw = r.get("REVENUE_AMOUNT_QOQ")
            rev_qoq = safe_dec(rev_qoq_raw)
            tic = safe_dec(r.get("TICKET_COUNT"))
            tic_qoq_raw = r.get("TICKET_COUNT_QOQ")
            tic_qoq = safe_dec(tic_qoq_raw)
            roy = safe_dec(r.get("ROYALTY_THEORY"))
            roy_qoq_raw = r.get("ROYALTY_THEORY_QOQ")
            roy_qoq = safe_dec(roy_qoq_raw)

            avg_cur = round(rev / tic, 2) if tic and tic != 0 else (0 if tic == 0 else None)
            avg_qoq = round(rev_qoq / tic_qoq, 2) if tic_qoq and tic_qoq != 0 else (0 if tic_qoq == 0 else None)
            avg_inc_qoq = round(avg_cur - avg_qoq, 2) if avg_cur is not None and avg_qoq is not None else None
            avg_rate_qoq = round(avg_inc_qoq / avg_qoq * 100, 2) if avg_inc_qoq is not None and avg_qoq and avg_qoq != 0 else None

            # 这里的 bp_info 在上面几行已经定义为 bp_info = bp_info_map.get(...) or {}
            
            # SettlementModes — 精确对齐逻辑：只有原值为 1000 的典型联营项目映射为 3000
            settle_mode = bp_info.get("SETTLEMENT_MODES")
            bp_type = bp_info.get("BUSINESS_TYPE")
            if btt == 3 and bp_type == 1000 and settle_mode == 1000:
                settle_mode = 3000

            # ShopTrade — 旧接口用的是 BW 当月固化表里的 BUSINESS_TRADE
            bw_trade = r.get("BUSINESS_TRADE")
            shop_trade_val = int(bw_trade) if bw_trade is not None else 0

            # Profit_Amount — C# 逻辑
            shop_profit = rev if btt is not None and btt < 3 else None
            shop_cost = 0.0 if btt is not None and btt < 3 else None
            shop_ca_cost = None
            
            # SABFI_Score 列表
            sabfi_list_empty = [{"name": str(et), "value": "", "data": "", "key": ""} for et in range(1, 8)]

            return {
                "ServerpartId": sp_id,
                "ServerpartName": sp_name,
                "BusinessProjectId": r.get("BUSINESSPROJECT_ID"),
                "BusinessProjectName": bp_info.get("BUSINESSPROJECT_NAME"),
                "ServerpartShopId": ssid_str,
                "ServerpartShopName": shop_name,
                "Brand_Id": float(brand_id) if brand_id is not None else None,
                "Brand_Name": brand_name,
                "BrandType_Name": None,
                "Brand_ICO": brand_ico if brand_ico else (None if brand_id is None else ""),
                "ShopTrade": shop_trade_val,
                "BusinessTrade": biz_trade,
                "BusinessTradeName": biz_trade_name,
                "BusinessTradeType": btt,
                "CompactStartDate": fmt_date(bp_info.get("PROJECT_STARTDATE")),
                "CompactEndDate": fmt_date(bp_info.get("PROJECT_ENDDATE")),
                "BusinessType": bp_info.get("BUSINESS_TYPE"),
                "SettlementModes": settle_mode,
                "MERCHANTS_ID": float(merch_id) if merch_id is not None else None,
                "MERCHANTS_ID_Encrypted": merch_id_enc,
                "MERCHANTS_NAME": merch_name,
                "RevenueINC": make_inc(
                    r.get("REVENUE_AMOUNT"), None, None, None,
                    rev_qoq_raw,
                    round(rev - rev_qoq, 2) if r.get("REVENUE_AMOUNT") is not None and rev_qoq is not None else None,
                    round((rev - rev_qoq) / rev_qoq * 100, 2) if rev_qoq is not None and rev_qoq != 0 and r.get("REVENUE_AMOUNT") is not None else None),
                "AccountINC": make_inc(
                    r.get("ROYALTY_THEORY"), None, None, None,
                    roy_qoq_raw,
                    round(roy - roy_qoq, 2) if r.get("ROYALTY_THEORY") is not None and roy_qoq is not None else None,
                    round((roy - roy_qoq) / roy_qoq * 100, 2) if roy_qoq is not None and roy_qoq != 0 and r.get("ROYALTY_THEORY") is not None else None),
                "TicketINC": make_inc(
                    r.get("TICKET_COUNT"), None, None, None,
                    tic_qoq_raw,
                    round(tic - tic_qoq, 2) if r.get("TICKET_COUNT") is not None and tic_qoq is not None else None,
                    round((tic - tic_qoq) / tic_qoq * 100, 2) if tic_qoq is not None and tic_qoq != 0 and r.get("TICKET_COUNT") is not None else None),
                "AvgTicketINC": make_inc(
                    avg_cur if tic is not None else None, None, None, None,
                    avg_qoq, avg_inc_qoq, avg_rate_qoq),
                "CurTransaction": None,
                "Profit_Amount": round(shop_profit, 2) if shop_profit is not None else None,
                "Cost_Amount": round(shop_cost, 2) if shop_cost is not None else None,
                "Ca_Cost": round(shop_ca_cost, 2) if shop_ca_cost is not None else None,
                "SABFI_Score": 0.0,
                "SABFIList": sabfi_list_empty,
                "BusinessState": str(si.get("BUSINESS_STATE") or "1"),
                "Revenue_SD": round(safe_dec(r.get("REVENUE_SD")), 2) if r.get("REVENUE_SD") is not None else None,
                "Revenue_AVG": round(safe_dec(r.get("REVENUE_AVG")), 2) if r.get("REVENUE_AVG") is not None else None,
            }

        # 汇总累加器
        total_rev, total_rev_yoy, total_rev_qoq = 0.0, 0.0, 0.0
        total_acct, total_acct_yoy, total_acct_qoq = 0.0, 0.0, 0.0
        total_ticket, total_ticket_yoy, total_ticket_qoq = 0.0, 0.0, 0.0
        total_flow, total_flow_yoy, total_flow_qoq = 0.0, 0.0, 0.0

        # 按片区分组（使用 SPREGIONTYPE_INDEX 排序片区，SERVERPART_INDEX 排序服务区）
        region_groups = OrderedDict()
        # 先按 (SPREGIONTYPE_INDEX, SPREGIONTYPE_ID) 对服务区排序后再分组
        sorted_sp_items = sorted(
            sp_groups.items(),
            key=lambda x: (
                sp_info_map.get(x[0], {}).get("SPREGIONTYPE_INDEX") or 0,
                sp_info_map.get(x[0], {}).get("SPREGIONTYPE_ID") or 0,
                sp_info_map.get(x[0], {}).get("SERVERPART_INDEX") or 0,
                x[0]  # fallback: SERVERPART_ID
            )
        )
        for sp_id, sp_data in sorted_sp_items:
            si = sp_info_map.get(sp_id, {})
            region_id = si.get("SPREGIONTYPE_ID")
            region_name = si.get("SPREGIONTYPE_NAME", "")
            region_idx = si.get("SPREGIONTYPE_INDEX", 0)
            rk = (region_idx or 0, region_id or 0)
            if rk not in region_groups:
                region_groups[rk] = {"id": region_id, "name": region_name, "serverparts": OrderedDict()}
            region_groups[rk]["serverparts"][sp_id] = sp_data

        # 构建树: 合计→片区→服务区→门店
        region_children = []
        for rk in sorted(region_groups.keys()):
            rg = region_groups[rk]
            reg_rev, reg_rev_yoy, reg_rev_qoq = 0.0, 0.0, 0.0
            reg_acct, reg_acct_yoy, reg_acct_qoq = 0.0, 0.0, 0.0
            reg_ticket, reg_ticket_yoy, reg_ticket_qoq = 0.0, 0.0, 0.0
            reg_flow, reg_flow_yoy, reg_flow_qoq = 0.0, 0.0, 0.0

            sp_children = []
            for sp_id, sp_data in rg["serverparts"].items():
                sp_rev, sp_rev_yoy, sp_rev_qoq = 0.0, 0.0, 0.0
                sp_acct, sp_acct_yoy, sp_acct_qoq = 0.0, 0.0, 0.0
                sp_ticket, sp_ticket_yoy, sp_ticket_qoq = 0.0, 0.0, 0.0

                shop_children = []
                for r in sp_data["shops"]:
                    # C# 对齐: BusinessTrade 内存过滤 (BindSABFISPINCAnalysis 第4247行)
                    # 用 T_SERVERPARTSHOP.BUSINESS_TRADE 字段判断是否匹配
                    if expanded_trades:
                        ssid_str = str(r.get("SERVERPARTSHOP_ID") or "")
                        si_bt = shop_agg_map.get(ssid_str) or {}
                        shop_bt_val = str(si_bt.get("BUSINESS_TRADE") or "")
                        shop_bt_ids = {b.strip() for b in shop_bt_val.split(",") if b.strip()}
                        if not shop_bt_ids.intersection(expanded_trades):
                            continue
                    rev = safe_dec(r.get("REVENUE_AMOUNT"))
                    sp_rev += rev
                    sp_rev_yoy += safe_dec(r.get("REVENUE_AMOUNT_YOY"))
                    sp_rev_qoq += safe_dec(r.get("REVENUE_AMOUNT_QOQ"))
                    sp_acct += safe_dec(r.get("ROYALTY_THEORY"))
                    sp_acct_yoy += safe_dec(r.get("ROYALTY_THEORY_YOY"))
                    sp_acct_qoq += safe_dec(r.get("ROYALTY_THEORY_QOQ"))
                    sp_ticket += safe_dec(r.get("TICKET_COUNT"))
                    sp_ticket_yoy += safe_dec(r.get("TICKET_COUNT_YOY"))
                    sp_ticket_qoq += safe_dec(r.get("TICKET_COUNT_QOQ"))

                    # 门店级 children 暂不使用（C# 服务区节点 children=null）
                    pass

                # 车流
                fr = flow_map.get(sp_id, {})
                sp_flow = safe_dec(fr.get("SERVERPART_FLOW"))
                sp_flow_yoy = safe_dec(fr.get("VEHICLE_COUNT_YOY"))
                sp_flow_qoq = safe_dec(fr.get("VEHICLE_COUNT_QOQ"))

                reg_rev += sp_rev; reg_rev_yoy += sp_rev_yoy; reg_rev_qoq += sp_rev_qoq
                reg_acct += sp_acct; reg_acct_yoy += sp_acct_yoy; reg_acct_qoq += sp_acct_qoq
                reg_ticket += sp_ticket; reg_ticket_yoy += sp_ticket_yoy; reg_ticket_qoq += sp_ticket_qoq
                reg_flow += sp_flow; reg_flow_yoy += sp_flow_yoy; reg_flow_qoq += sp_flow_qoq

                # C# 对齐第4437行: 利润/成本从已过滤的 ShopSABFIList 求和，移到 node_shop_list 构建后计算
                # (保留位置但不计算，实际计算在 node_shop_list 构建后)

                # AvgTicket 中间值对齐 C# Round
                avg_cur = round(sp_rev / sp_ticket, 2) if sp_ticket and sp_ticket != 0 else (0 if sp_ticket == 0 else None)
                avg_qoq = round(sp_rev_qoq / sp_ticket_qoq, 2) if sp_ticket_qoq and sp_ticket_qoq != 0 else (0 if sp_ticket_qoq == 0 else None)
                avg_inc_qoq = round(avg_cur - avg_qoq, 2) if avg_cur is not None and avg_qoq is not None else None
                avg_rate_qoq = round(avg_inc_qoq / avg_qoq * 100, 2) if avg_inc_qoq is not None and avg_qoq and avg_qoq != 0 else None

                # BayonetINC_ORI：C# 只填 curYearData（车流原始值）
                bayonet_ori = make_inc(sp_flow)

                # Building ShopSABFIList
                node_shop_list = []
                # 对齐旧接口排序：按 BUSINESSWARNING_ID
                _sorted_shops = sorted(sp_data["shops"], key=lambda x: int(x.get("BUSINESSWARNING_ID") or 0))
                for row in _sorted_shops:
                    # C# 对齐: ShopSABFIList 中也要过滤 BusinessTrade (与服务区汇总一致)
                    if expanded_trades:
                        _ss_filter = str(row.get("SERVERPARTSHOP_ID", ""))
                        _si_filter = shop_agg_map.get(_ss_filter) or {}
                        _bt_filter_val = str(_si_filter.get("BUSINESS_TRADE") or "")
                        _bt_filter_ids = {b.strip() for b in _bt_filter_val.split(",") if b.strip()}
                        if not _bt_filter_ids.intersection(expanded_trades):
                            continue

                    # 合并 SSID 信息
                    _ss_id_str = str(row.get("SERVERPARTSHOP_ID", ""))
                    _si = shop_agg_map.get(_ss_id_str) or {}

                    _bp = bp_info_map.get(row.get("BUSINESSPROJECT_ID")) or {}
                    _m_id = _bp.get("MERCHANTS_ID") or _si.get("SELLER_ID")
                    
                    # SABFI 门店节点 YOY 强制为 None 以对齐旧接口
                    r_rev = row.get("REVENUE_AMOUNT"); r_tic = row.get("TICKET_COUNT")
                    r_rev_qoq = row.get("REVENUE_AMOUNT_QOQ"); r_tic_qoq = row.get("TICKET_COUNT_QOQ")
                    ac = round(float(r_rev)/float(r_tic), 2) if r_rev is not None and r_tic and float(r_tic) != 0 else None
                    aq = round(float(r_rev_qoq)/float(r_tic_qoq), 2) if r_rev_qoq is not None and r_tic_qoq and float(r_tic_qoq) != 0 else None

                    # Profit_Amount: C# 自营门店=Revenue, 联营=None
                    _btt_val = row.get("BUSINESS_TYPE")  # BusinessTradeType from BW
                    _shop_profit = safe_dec(r_rev) if _btt_val is not None and int(safe_dec(_btt_val)) < 3 else None
                    _shop_cost = 0.0 if _btt_val is not None and int(safe_dec(_btt_val)) < 3 else None

                    # C# 对齐: SABFIList 从 T_PROFITCONTRIBUTE 按 BUSINESSPROJECT_ID 查各 EVALUATE_TYPE 的评分
                    _bp_id = row.get("BUSINESSPROJECT_ID")
                    _shop_sabfi_list = [{"name": str(et), "value": "", "data": "", "key": ""} for et in range(1, 8)]
                    _shop_sabfi_score = 0.0
                    if _bp_id is not None:
                        for p_data in sabfi_projects_map.get(sp_id, []):
                            if p_data.get("BusinessProjectId") == _bp_id:
                                _shop_sabfi_list = p_data.get("SABFIList", _shop_sabfi_list)
                                _shop_sabfi_score = safe_dec(p_data.get("SABFI_Score", 0))
                                break
                    elif row.get("SHOPSHORTNAME"):
                        # C# fallback: 没有 BUSINESSPROJECT_ID 时用 SERVERPARTSHOP_NAME 匹配
                        _shop_name_match = row.get("SHOPSHORTNAME")
                        for p_data in sabfi_projects_map.get(sp_id, []):
                            if p_data.get("BusinessProjectName") == _shop_name_match:
                                _shop_sabfi_list = p_data.get("SABFIList", _shop_sabfi_list)
                                _shop_sabfi_score = safe_dec(p_data.get("SABFI_Score", 0))
                                break

                    shop_node = {
                        "ServerpartId": sp_id, "ServerpartName": sp_data["name"],
                        "ServerpartShopId": _ss_id_str, "ServerpartShopName": row.get("SHOPSHORTNAME"),
                        "RevenueINC": make_inc(r_rev, None, qoq=r_rev_qoq, inc_qoq=round(safe_dec(r_rev) - safe_dec(r_rev_qoq), 2) if r_rev_qoq is not None else None, rate_qoq=round((safe_dec(r_rev) - safe_dec(r_rev_qoq)) / safe_dec(r_rev_qoq) * 100, 2) if safe_dec(r_rev_qoq) and safe_dec(r_rev_qoq) != 0 else None),
                        "AccountINC": make_inc(row.get("ROYALTY_THEORY"), None, qoq=row.get("ROYALTY_THEORY_QOQ"), inc_qoq=round(safe_dec(row.get("ROYALTY_THEORY")) - safe_dec(row.get("ROYALTY_THEORY_QOQ")), 2) if row.get("ROYALTY_THEORY_QOQ") is not None else None, rate_qoq=round((safe_dec(row.get("ROYALTY_THEORY")) - safe_dec(row.get("ROYALTY_THEORY_QOQ"))) / safe_dec(row.get("ROYALTY_THEORY_QOQ")) * 100, 2) if safe_dec(row.get("ROYALTY_THEORY_QOQ")) and safe_dec(row.get("ROYALTY_THEORY_QOQ")) != 0 else None),
                        "TicketINC": make_inc(r_tic, None, qoq=r_tic_qoq, inc_qoq=round(safe_dec(r_tic) - safe_dec(r_tic_qoq), 2) if r_tic_qoq is not None else None, rate_qoq=round((safe_dec(r_tic) - safe_dec(r_tic_qoq)) / safe_dec(r_tic_qoq) * 100, 2) if safe_dec(r_tic_qoq) and safe_dec(r_tic_qoq) != 0 else None),
                        "AvgTicketINC": make_inc(ac, None, qoq=aq, inc_qoq=round(ac - aq, 2) if ac is not None and aq is not None else None, rate_qoq=round((ac - aq) / aq * 100, 2) if ac is not None and aq is not None and aq != 0 else None),
                        "SABFI_Score": _shop_sabfi_score, "SABFIList": _shop_sabfi_list,
                        "Brand_Id": int(_si.get("BRAND_ID")) if _si.get("BRAND_ID") is not None else None,
                        "Brand_Name": _si.get("BRAND_NAME2") or _si.get("BRAND_NAME") or row.get("SHOPSHORTNAME"),
                        "BrandType_Name": None,
                        "Brand_ICO": _format_ico(_si.get("BRAND_ICO")),
                        "BusinessTrade": str(_si.get("BUSINESS_TRADE") or "") if _si.get("BUSINESS_TRADE") else None,
                        "BusinessTradeName": _si.get("BUSINESS_TRADENAME") or row.get("SHOPSHORTNAME"),
                        "BusinessTradeType": int(safe_dec(_btt_val)) if _btt_val is not None else None,
                        "BusinessProjectId": int(_bp["BUSINESSPROJECT_ID"]) if _bp.get("BUSINESSPROJECT_ID") else None,
                        "BusinessProjectName": _bp.get("BUSINESSPROJECT_NAME") if _bp else None,
                        "BusinessType": _bp.get("BUSINESS_TYPE") if _bp.get("BUSINESS_TYPE") is not None else None,
                        "ShopTrade": int(_bp.get("BUSINESS_TYPE") or 0) if _bp else 0,
                        "CompactStartDate": _format_bp_date(_bp.get("PROJECT_STARTDATE")) or "",
                        "CompactEndDate": _format_bp_date(_bp.get("PROJECT_ENDDATE")) or "",
                        "SettlementModes": int(_bp["SETTLEMENT_MODES"]) if _bp.get("SETTLEMENT_MODES") is not None else None,
                        "StatisticsMonth": None,
                        "MERCHANTS_ID": float(_m_id) if _m_id is not None else None,
                        "MERCHANTS_ID_Encrypted": des_encrypt_id(_m_id),
                        "MERCHANTS_NAME": _bp.get("MERCHANTS_NAME") or _si.get("SELLER_NAME"),
                        "Profit_Amount": _shop_profit,
                        "Cost_Amount": _shop_cost,
                        "Ca_Cost": None,
                        "CurTransaction": None,
                        "Revenue_SD": safe_dec(row.get("REVENUE_SD")) if row.get("REVENUE_SD") is not None else None,
                        "Revenue_AVG": safe_dec(row.get("REVENUE_AVG")) if row.get("REVENUE_AVG") is not None else None,
                    }
                    node_shop_list.append(shop_node)
                
                # 服务区 SABFI 节点 AvgTicket (QOQ)
                s_ac = round(sp_rev/sp_ticket, 2) if sp_ticket else 0.0
                s_aq = round(sp_rev_qoq/sp_ticket_qoq, 2) if sp_ticket_qoq else 0.0

                # 获取 SABFI 评分项目列表（用于 SABFI_Score 汇总）
                sp_sabfi_projects = sabfi_projects_map.get(sp_id, [])
                sp_overall_score = round(sum(p["Overall_Score"] for p in sp_sabfi_projects if p.get("Overall_Score")) / len(sp_sabfi_projects), 2) if sp_sabfi_projects else 0.0

                # C# 对齐第4437行: 服务区利润/成本从 node_shop_list 求和
                sp_profit = sum(safe_dec(s.get("Profit_Amount")) for s in node_shop_list)
                sp_cost = sum(safe_dec(s.get("Cost_Amount")) for s in node_shop_list)
                sp_ca_cost = round(sp_cost / sp_ticket, 2) if sp_ticket and sp_ticket > 0 and sp_cost else 0.0

                sp_node = {
                    "SABFI_Score": sp_overall_score, "ShopSABFIList": node_shop_list,
                    "SPRegionTypeId": rg["id"], "SPRegionTypeName": rg["name"],
                    "ServerpartId": sp_id, "ServerpartName": sp_data["name"],
                    "RevenueINC": make_inc(sp_rev, None, qoq=sp_rev_qoq, inc_qoq=round(sp_rev - sp_rev_qoq, 2) if sp_rev_qoq is not None else None, rate_qoq=round((sp_rev - sp_rev_qoq) / sp_rev_qoq * 100, 2) if sp_rev_qoq is not None and sp_rev_qoq != 0 else None),
                    "AccountINC": make_inc(round(sp_acct, 2), 0.0, qoq=round(sp_acct_qoq, 2), inc_qoq=round(sp_acct - sp_acct_qoq, 2) if sp_acct_qoq is not None else None, rate_qoq=round((sp_acct - sp_acct_qoq) / sp_acct_qoq * 100, 2) if sp_acct_qoq is not None and sp_acct_qoq != 0 else None),
                    "BayonetINC": make_inc(sp_flow, None, qoq=sp_flow_qoq, inc_qoq=round(sp_flow - sp_flow_qoq, 2) if sp_flow_qoq is not None else None, rate_qoq=round((sp_flow - sp_flow_qoq) / sp_flow_qoq * 100, 2) if sp_flow_qoq is not None and sp_flow_qoq != 0 else None),
                    "SectionFlowINC": None, "BayonetINC_ORI": bayonet_ori,
                    "TicketINC": make_inc(sp_ticket, None, qoq=sp_ticket_qoq, inc_qoq=round(sp_ticket - sp_ticket_qoq, 2) if sp_ticket_qoq is not None else None, rate_qoq=round((sp_ticket - sp_ticket_qoq) / sp_ticket_qoq * 100, 2) if sp_ticket_qoq is not None and sp_ticket_qoq != 0 else None),
                    "AvgTicketINC": make_inc(avg_cur, None, qoq=avg_qoq, inc_qoq=round(avg_cur - avg_qoq, 2) if avg_cur is not None and avg_qoq is not None else None, rate_qoq=round((avg_cur - avg_qoq) / avg_qoq * 100, 2) if avg_cur is not None and avg_qoq is not None and avg_qoq != 0 else None),
                    "Profit_Amount": round(sp_profit, 2) if sp_profit is not None else None, "Cost_Amount": round(sp_cost, 2) if sp_cost is not None else None,
                    "Ca_Cost": sp_ca_cost, "ShopINCList": None, "RankDiff": None,
                }
                sp_children.append({"node": sp_node, "children": None})

            total_rev += reg_rev; total_rev_yoy += reg_rev_yoy; total_rev_qoq += reg_rev_qoq
            total_acct += reg_acct; total_acct_yoy += reg_acct_yoy; total_acct_qoq += reg_acct_qoq
            total_ticket += reg_ticket; total_ticket_yoy += reg_ticket_yoy; total_ticket_qoq += reg_ticket_qoq
            total_flow += reg_flow; total_flow_yoy += reg_flow_yoy; total_flow_qoq += reg_flow_qoq

            # Profit 从 sp_node 累加（含 fallback）
            reg_profit = sum(safe_dec(ch["node"].get("Profit_Amount")) for ch in sp_children)
            reg_cost = sum(safe_dec(ch["node"].get("Cost_Amount")) for ch in sp_children)

            # 片区节点 — C# 聚合只填 curYearData + QOQData
            reg_node = {
                "SABFI_Score": None, "ShopSABFIList": None,
                "SPRegionTypeId": rg["id"], "SPRegionTypeName": rg["name"],
                "ServerpartId": None, "ServerpartName": None,
                "RevenueINC": make_inc(reg_rev, None, qoq=reg_rev_qoq, inc_qoq=round(reg_rev - reg_rev_qoq, 2) if reg_rev_qoq is not None else None, rate_qoq=round((reg_rev - reg_rev_qoq) / reg_rev_qoq * 100, 2) if reg_rev_qoq is not None and reg_rev_qoq != 0 else None),
                "AccountINC": make_inc(round(reg_acct, 2), None, qoq=round(reg_acct_qoq, 2), inc_qoq=round(reg_acct - reg_acct_qoq, 2) if reg_acct_qoq is not None else None, rate_qoq=round((reg_acct - reg_acct_qoq) / reg_acct_qoq * 100, 2) if reg_acct_qoq is not None and reg_acct_qoq != 0 else None),
                "BayonetINC": make_inc(reg_flow, None, qoq=reg_flow_qoq, inc_qoq=round(reg_flow - reg_flow_qoq, 2) if reg_flow_qoq is not None else None, rate_qoq=round((reg_flow - reg_flow_qoq) / reg_flow_qoq * 100, 2) if reg_flow_qoq is not None and reg_flow_qoq != 0 else None),
                "SectionFlowINC": None, "BayonetINC_ORI": None,
                "TicketINC": make_inc(reg_ticket, None, qoq=reg_ticket_qoq, inc_qoq=round(reg_ticket - reg_ticket_qoq, 2) if reg_ticket_qoq is not None else None, rate_qoq=round((reg_ticket - reg_ticket_qoq) / reg_ticket_qoq * 100, 2) if reg_ticket_qoq is not None and reg_ticket_qoq != 0 else None),
                "AvgTicketINC": (lambda ac=round(reg_rev/reg_ticket,2) if reg_ticket else 0, aq=round(reg_rev_qoq/reg_ticket_qoq,2) if reg_ticket_qoq else 0:
                    make_inc(ac, None, qoq=aq, inc_qoq=round(ac - aq, 2) if ac is not None and aq is not None else None, rate_qoq=round((ac - aq) / aq * 100, 2) if ac is not None and aq is not None and aq != 0 else None))(),
                "ShopINCList": None,
                "Profit_Amount": round(reg_profit, 2), "Cost_Amount": round(reg_cost, 2),
                "Ca_Cost": round(reg_cost / reg_ticket, 2) if reg_ticket and reg_cost else 0.0,
                "RankDiff": None,
            }
            region_children.append({"node": reg_node, "children": sp_children})

        # 根节点 Profit 从片区节点累加
        total_profit = sum(safe_dec(rch["node"].get("Profit_Amount")) for rch in region_children)
        total_cost = sum(safe_dec(rch["node"].get("Cost_Amount")) for rch in region_children)

        # 根 "合计" 节点
        root_node = {
            "SABFI_Score": None, "ShopSABFIList": None,
            "SPRegionTypeId": None, "SPRegionTypeName": None,
            "ServerpartId": None, "ServerpartName": "合计",
            "RevenueINC": make_inc(total_rev, None, None, None,
                total_rev_qoq, total_rev - total_rev_qoq if total_rev_qoq else None,
                round((total_rev - total_rev_qoq) / total_rev_qoq * 100, 2) if total_rev_qoq else None),
            "AccountINC": make_inc(round(total_acct, 2), 0.0, None, None,
                round(total_acct_qoq, 2), round(total_acct - total_acct_qoq, 2) if total_acct_qoq else None,
                round((total_acct - total_acct_qoq) / total_acct_qoq * 100, 2) if total_acct_qoq else None),
            "BayonetINC": make_inc(total_flow, 0.0, None, None,
                total_flow_qoq, total_flow - total_flow_qoq if total_flow_qoq else None,
                round((total_flow - total_flow_qoq) / total_flow_qoq * 100, 2) if total_flow_qoq else None),
            "SectionFlowINC": None, "BayonetINC_ORI": None,
            "TicketINC": make_inc(total_ticket, None, None, None,
                total_ticket_qoq, total_ticket - total_ticket_qoq if total_ticket_qoq else None,
                round((total_ticket - total_ticket_qoq) / total_ticket_qoq * 100, 2) if total_ticket_qoq else None),
            "AvgTicketINC": (lambda ac=round(total_rev/total_ticket,2) if total_ticket else None, aq=round(total_rev_qoq/total_ticket_qoq,2) if total_ticket_qoq else None:
                make_inc(ac, None, None, None, aq,
                    round(ac - aq, 2) if ac is not None and aq is not None else None,
                    round((ac - aq) / aq * 100, 2) if ac is not None and aq is not None and aq else None))(),
            "ShopINCList": None,
            "Profit_Amount": round(total_profit, 2) if region_children else None, "Cost_Amount": round(total_cost, 2) if region_children else None,
            "Ca_Cost": round(total_cost / total_ticket, 2) if total_ticket and total_cost else (None if not region_children else 0.0),
            "RankDiff": None,
        }
        result_list = [{"node": root_node, "children": region_children}]

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopSABFIList 查询失败: {ex}")
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
    """获取门店每月商业适配指数 (对齐C# BindShopMonthSABFI)"""
    try:
        from datetime import datetime as dt

        # 构建查询条件
        if BusinessProjectId:
            pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
                WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "BUSINESSPROJECT_ID" = {BusinessProjectId}
                    AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                    AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
        elif ServerpartShopId:
            pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
                WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPARTSHOP_ID" = '{ServerpartShopId}'
                    AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                    AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
        elif ServerpartId and ServerpartShopName:
            pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
                WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPART_ID" = {ServerpartId}
                    AND "SERVERPARTSHOP_NAME" = '{ServerpartShopName}'
                    AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                    AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
        else:
            json_list = JsonListData.create(data_list=[], total=0, page_size=10)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        pc_rows = db.execute_query(pc_sql) or []

        # 按月份分组
        month_data = {}
        for r in pc_rows:
            m = str(r.get("STATISTICS_DATE", ""))
            if m not in month_data:
                month_data[m] = []
            month_data[m].append(r)

        # 遍历月份范围
        data_list = []
        s_year = int(StatisticsStartMonth[:4])
        s_month = int(StatisticsStartMonth[4:])
        e_year = int(StatisticsEndMonth[:4])
        e_month = int(StatisticsEndMonth[4:])
        cur_y, cur_m = s_year, s_month
        while cur_y * 100 + cur_m <= e_year * 100 + e_month:
            m_key = f"{cur_y}{cur_m:02d}"
            m_fmt = f"{cur_y}/{cur_m:02d}"
            rows_m = month_data.get(m_key, [])
            rows_m_int = month_data.get(int(m_key) if m_key.isdigit() else m_key, rows_m)
            if not rows_m and rows_m_int:
                rows_m = rows_m_int

            def get_max(rr, eval_type, field):
                """获取指定EVALUATE_TYPE的MAX值"""
                vals = [r.get(field) for r in rr if str(r.get("EVALUATE_TYPE")) == str(eval_type) and r.get(field) is not None]
                if vals:
                    return str(max(vals))
                return ""

            sabfi_list = []
            for et in range(1, 8):
                sabfi_list.append({
                    "name": str(et),
                    "value": get_max(rows_m, et, "EVALUATE_SCORE"),
                    "key": get_max(rows_m, et, "PROFITCONTRIBUTE_ID"),
                    "data": get_max(rows_m, et, "PROFITCONTRIBUTE_PID"),
                })

            # 计算SABFI_Score
            score_0 = get_max(rows_m, 0, "EVALUATE_SCORE")
            try:
                sabfi_score = float(score_0) if score_0 else 0.0
            except:
                sabfi_score = 0.0
            # C#: SABFI_Score = SABFIList.Sum(o => o.value.TryParseToDecimal())
            sabfi_sum = sum(float(s["value"]) if s["value"] else 0.0 for s in sabfi_list)

            # TODO: 此处若需对齐 C# 细化数据，需查 T_BUSINESSWARNING / T_PERIODMONTHPROFIT
            # 临时占位逻辑：从 rows_m 获取基础信息
            sample = rows_m[0] if rows_m else {}
            
            data_list.append({
                "StatisticsMonth": m_fmt,
                "BusinessTrade": sample.get("SERVERPARTSHOP_NAME"), # 临时
                "BusinessProjectName": None,
                "SABFI_Score": sabfi_sum,
                "Revenue_SD": None,
                "Revenue_AVG": None,
                "SABFIList": sabfi_list,
                "ServerpartId": sample.get("SERVERPART_ID"),
                "ServerpartName": sample.get("SERVERPART_NAME"),
                "ServerpartShopId": sample.get("SERVERPARTSHOP_ID"),
                "ServerpartShopName": sample.get("SERVERPARTSHOP_NAME"),
                "Brand_Id": None, "Brand_Name": None, "BrandType_Name": None, "Brand_ICO": None,
                "ShopTrade": 0, "BusinessTradeName": None, "BusinessTradeType": 0,
                "BusinessProjectId": sample.get("BUSINESSPROJECT_ID"), "CompactStartDate": None, "CompactEndDate": None,
                "BusinessType": None, "SettlementModes": None,
                "MERCHANTS_ID": None, "MERCHANTS_ID_Encrypted": None, "MERCHANTS_NAME": None,
                "RevenueINC": None, "AccountINC": None, "TicketINC": None, "AvgTicketINC": None,
                "CurTransaction": None, "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
            })

            # 下个月
            if cur_m == 12:
                cur_y += 1
                cur_m = 1
            else:
                cur_m += 1

        json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopMonthSABFIList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")

