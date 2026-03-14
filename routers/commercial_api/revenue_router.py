# -*- coding: utf-8 -*-
"""
CommercialApi - Revenue 路由
对应原 C# CommercialApi/Controllers/RevenueController.cs
营收相关接口（50 个路由；核心逻辑已迁移到 services/commercial/ 下的各 Service 文件）

Service 文件清单:
  revenue_trend_service      — 营收趋势、同比
  revenue_transaction_service — 交易分析
  revenue_push_service       — 每日推送
  revenue_brand_service      — 品牌排行
  revenue_budget_service     — 预算对比
  revenue_business_service   — 经营模式/业态分析
  revenue_report_service     — 营收报表
  revenue_holiday_service    — 节假日分析
  revenue_account_service    — 应收/当日营收/同步
  revenue_monthly_service    — 月度经营分析
  revenue_compare_service    — 营收同比环比趋势
  revenue_inc_service        — 增幅分析
  revenue_month_inc_service  — 月度增幅分析
  revenue_sabfi_service      — 商品助力分析
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from models.base import Result, JsonListData
from routers.deps import get_db
from core.database import DatabaseHelper

# Service 层导入
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
from services.commercial import revenue_compare_service

# 公共工具
from services.commercial.service_utils import date_no_pad

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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")




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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")


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

        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")


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

        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")



@router.get("/Revenue/GetLastSyncDateTime")

async def get_last_sync_date_time(db: DatabaseHelper = Depends(get_db)):

    """获取最新的同步日期 -- 业务逻辑见 revenue_account_service.get_last_sync_date_time()"""

    try:

        data = revenue_account_service.get_last_sync_date_time(db)

        return Result.success(data=data, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetLastSyncDateTime 失败: {ex}")

        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")





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

        return Result.fail(msg="查询失败")



        return Result.fail(msg="查询失败")


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

    """获取服务区营收增幅分析 — 业务逻辑见 revenue_inc_service.get_serverpart_inc_analysis()"""

    try:

        from services.commercial import revenue_inc_service

        result_list, holiday_period = revenue_inc_service.get_serverpart_inc_analysis(

            db, calcType, pushProvinceCode, curYear,

            HolidayType, StatisticsDate, compareYear,

            CurStartDate, StatisticsStartDate, StatisticsEndDate,

            ServerpartId, SPRegionTypeID, businessRegion,

            SortStr, IsYOYCompare, date_no_pad

        )

        if not result_list:

            return Result.fail(code=101, msg="查询失败，无数据返回！")

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)

        resp = json_list.model_dump()

        resp["OtherData"] = holiday_period

        return Result.success(data=resp, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetServerpartINCAnalysis 查询失败: {ex}")

        return Result.fail(msg="查询失败")





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

    """获取门店营收增幅分析 — 业务逻辑见 revenue_inc_service.get_shop_inc_analysis()"""

    try:

        from services.commercial import revenue_inc_service

        result_list = revenue_inc_service.get_shop_inc_analysis(

            db, calcType, pushProvinceCode, curYear, compareYear,

            HolidayType, ServerpartId, StatisticsDate, CurStartDate, SortStr

        )

        if not result_list:

            return Result.fail(code=101, msg="查询失败，无数据返回！")

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetShopINCAnalysis 查询失败: {ex}")

        return Result.fail(msg="查询失败")






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

        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")



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
        return Result.fail(msg="查询失败")


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
        return Result.fail(msg="查询失败")


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

        return Result.fail(msg="查询失败")



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
    """获取营收同比环比对比数据 — 业务逻辑见 revenue_compare_service.get_revenue_compare()"""
    try:
        if not ProvinceCode:
            ProvinceCode = request.headers.get("ProvinceCode", "")
        data = revenue_compare_service.get_revenue_compare(
            db, ProvinceCode, StatisticsDate, ServerpartId, SPRegionTypeID
        )
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetRevenueCompare 查询失败: {ex}")
        return Result.fail(msg="查询失败")

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
        return Result.fail(msg="查询失败")



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

        return Result.fail(msg="查询失败")





# ===== 月度增幅分析 =====



@router.get("/Revenue/GetMonthINCAnalysis")

async def get_month_inc_analysis(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsMonth: Optional[str] = Query(None, description="统计月份 YYYYMM"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),

    businessRegion: Optional[int] = Query(None, description="经营区域"),

    SortStr: Optional[str] = Query("", description="排序字段"),

    DataType: Optional[str] = Query("", description="数据类型"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取月度增幅分析 — 业务逻辑见 revenue_month_inc_service.get_month_inc_analysis()"""

    try:

        from services.commercial import revenue_month_inc_service

        result_list = revenue_month_inc_service.get_month_inc_analysis(

            db, pushProvinceCode, StatisticsMonth, ServerpartId,

            SPRegionTypeID, businessRegion, SortStr, DataType

        )

        if not result_list:

            return Result.fail(code=101, msg="查询失败，无数据返回！")

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetMonthINCAnalysis 查询失败: {ex}")

        return Result.fail(msg="查询失败")





@router.get("/Revenue/GetMonthINCAnalysisSummary")

async def get_month_inc_analysis_summary(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsMonth: Optional[str] = Query(None, description="统计月份 YYYYMM"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),

    businessRegion: Optional[int] = Query(None, description="经营区域"),

    DataType: Optional[str] = Query("", description="数据类型"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取月度增幅分析汇总 — 业务逻辑见 revenue_month_inc_service.get_month_inc_analysis_summary()"""

    try:

        from services.commercial import revenue_month_inc_service

        result = revenue_month_inc_service.get_month_inc_analysis_summary(

            db, pushProvinceCode, StatisticsMonth, ServerpartId,

            SPRegionTypeID, businessRegion, DataType

        )

        return Result.success(data=result, msg="查询成功")

    except Exception as ex:

        logger.error(f"GetMonthINCAnalysisSummary 查询失败: {ex}")

        return Result.fail(msg="查询失败")





@router.get("/Revenue/StorageMonthINCAnalysis")

async def storage_month_inc_analysis(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsMonth: Optional[str] = Query(None, description="统计月份 YYYYMM"),

    db: DatabaseHelper = Depends(get_db)

):

    """存储月度增幅分析数据 — 业务逻辑见 revenue_month_inc_service.storage_month_inc_analysis()"""

    try:

        from services.commercial import revenue_month_inc_service

        result = revenue_month_inc_service.storage_month_inc_analysis(

            db, pushProvinceCode, StatisticsMonth

        )

        return Result.success(data=result, msg="查询成功")

    except Exception as ex:

        logger.error(f"StorageMonthINCAnalysis 查询失败: {ex}")

        return Result.fail(msg="查询失败")





# ===== 门店 SABFI 分析 =====



@router.get("/Revenue/GetShopSABFIList")

async def get_shop_sabfi_list(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsDate: Optional[str] = Query(None, description="统计日期"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),

    businessRegion: Optional[int] = Query(None, description="经营区域"),

    SortStr: Optional[str] = Query("", description="排序字段"),

    businessType: Optional[str] = Query("", description="经营模式"),

    businessTrade: Optional[str] = Query("", description="经营业态"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取门店 SABFI 列表 — 业务逻辑见 revenue_sabfi_service.get_shop_sabfi_list()"""

    try:

        from services.commercial import revenue_sabfi_service

        result_list = revenue_sabfi_service.get_shop_sabfi_list(

            db, pushProvinceCode, StatisticsDate, ServerpartId,

            SPRegionTypeID, businessRegion, SortStr, businessType, businessTrade

        )

        if not result_list:

            return Result.fail(code=101, msg="查询失败，无数据返回！")

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetShopSABFIList 查询失败: {ex}")

        return Result.fail(msg="查询失败")





@router.get("/Revenue/GetShopMonthSABFIList")

async def get_shop_month_sabfi_list(

    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),

    StatisticsMonth: Optional[str] = Query(None, description="统计月份 YYYYMM"),

    ServerpartId: Optional[str] = Query("", description="服务区内码"),

    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),

    businessRegion: Optional[int] = Query(None, description="经营区域"),

    SortStr: Optional[str] = Query("", description="排序字段"),

    db: DatabaseHelper = Depends(get_db)

):

    """获取门店月度 SABFI 列表 — 业务逻辑见 revenue_sabfi_service.get_shop_month_sabfi_list()"""

    try:

        from services.commercial import revenue_sabfi_service

        result_list = revenue_sabfi_service.get_shop_month_sabfi_list(

            db, pushProvinceCode, StatisticsMonth, ServerpartId,

            SPRegionTypeID, businessRegion, SortStr

        )

        if not result_list:

            return Result.fail(code=101, msg="查询失败，无数据返回！")

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)

        return Result.success(data=json_list.model_dump(), msg="查询成功")

    except Exception as ex:

        logger.error(f"GetShopMonthSABFIList 查询失败: {ex}")

        return Result.fail(msg="查询失败")


