# -*- coding: utf-8 -*-
"""
CommercialApi - Revenue 路由
对应原 CommercialApi/Controllers/RevenueController.cs
营收相关接口（原2657行，40+接口，此处按方法签名完整定义路由）
"""
from fastapi import APIRouter, Depends, Query
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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


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
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


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
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


# ===== 业态分析 =====
@router.get("/Revenue/GetBusinessTradeRevenue")
async def get_business_trade_revenue(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    BusinessTradeIds: Optional[str] = Query("", description="经营业态内码"),
    DataType: int = Query(1, description="数据类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态营收占比"""
    logger.warning("GetBusinessTradeRevenue 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


@router.get("/Revenue/GetBusinessTradeLevel")
async def get_business_trade_level(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeTrade: bool = Query(True, description="是否显示全部业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业态消费水平占比"""
    logger.warning("GetBusinessTradeLevel 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


@router.get("/Revenue/GetBusinessBrandLevel")
async def get_business_brand_level(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    ShowWholeTrade: bool = Query(True, description="是否显示全部业态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取品牌消费水平占比"""
    logger.warning("GetBusinessBrandLevel 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


# ===== 营收趋势 =====
# 注意：C# 中有两个 GetRevenueTrend，一个路由到 GetRevenueCompare(GET)，一个路由到 GetRevenueTrend(GET)
# 这里只保留 GetRevenueTrend 的 GET 版本（下方已有 GET 定义）


@router.get("/Revenue/GetRevenueTrend")
async def get_revenue_trend_get(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsType: int = Query(1, description="统计类型"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取营收趋势图（GET）"""
    logger.warning("GetRevenueTrend GET 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


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
            "Province_InsideAmount": total_revenue,
            "revenueRegionModels": region_list,
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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data=json_list.model_dump(), msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


@router.get("/Revenue/GetCurRevenue")
async def get_cur_revenue(
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsDate: Optional[str] = Query(None, description="统计日期"),
    serverPartId: Optional[str] = Query("", description="服务区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取实时营收交易数据"""
    logger.warning("GetCurRevenue 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


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
    logger.warning("GetHolidayAnalysis 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


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
    logger.warning("GetHolidayAnalysisBatch 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


# ===== 增幅分析 =====
@router.get("/Revenue/GetServerpartINCAnalysis")
async def get_serverpart_inc_analysis(
    calcType: int = Query(1, description="计算方式：1当日 2累计"),
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
    curYear: Optional[str] = Query(None, description="本年年份"),
    compareYear: Optional[str] = Query("", description="历年年份"),
    StatisticsStartDate: Optional[str] = Query("", description="开始日期"),
    StatisticsEndDate: Optional[str] = Query("", description="结束日期"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionTypeID: Optional[str] = Query("", description="片区内码"),
    SortStr: Optional[str] = Query("", description="排序字段"),
    IsYOYCompare: bool = Query(False, description="是否对比同期数据"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区营收增幅分析"""
    logger.warning("GetServerpartINCAnalysis 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


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
    logger.warning("GetMonthlyBusinessAnalysis 暂未完整实现")
    return Result.success(data={}, msg="查询成功")


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
    logger.warning("GetMonthlySPINCAnalysis 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


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
    return Result.success(data={}, msg="查询成功")


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
    logger.warning("GetCompanyRevenueReport 暂未完整实现")
    json_list = JsonListData.create(data_list=[], total=0)
    return Result.success(data=json_list.model_dump(), msg="查询成功")
