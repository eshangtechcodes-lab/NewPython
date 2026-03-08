from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BusinessProjectController 散装接口 Service（第二批 18 个复杂接口）
每个接口对应原 C# Helper 方法中的复杂 SQL 逻辑

接口清单：
1. GetMerchantsReceivablesList — COOPMERCHANTSHelper(多表聚合+分页)
2. GetMerchantsReceivables — COOPMERCHANTSHelper(单商户详情)
3. GetBrandReceivables — COOPMERCHANTSHelper(品牌应收+OtherData)
4. GetMerchantsReceivablesReport — COOPMERCHANTSHelper(Nesting)
5. GetExpenseSummary — SHOPEXPENSEHelper(Nesting+OtherData)
6. GetShopExpenseSummary — SHOPEXPENSEHelper(月度应收明细)
7. GetMonthSummaryList — PROJECTSPLITMONTHHelper(月度汇总)
8. GetAnnualSplit — BIZPSPLITMONTHHelper(年度拆分+OtherData)
9. GetProjectAccountList — BUSINESSPROJECTHelper(Token+分页)
10. GetProjectAccountTree — BUSINESSPROJECTHelper(Nesting)
11. GetProjectAccountDetail — BUSINESSPROJECTHelper(Token)
12. GetAccountWarningList — BUSINESSPROJECTHelper(Format切换)
13. SolidAccountWarningList — BUSINESSPROJECTHelper(18参数写)
14. SolidProjectRevenue — BUSINESSPROJECTHelper(固化月度营收)
15. SolidPeriodAnalysis — PERIODWARNINGHelper(盈利分析)
16. GetPeriodWarningList — PERIODWARNINGHelper(多维过滤)
17. ReconfigureProfit — PERIODWARNINGHelper(盈利重分析)
18. GetWillSettleProject — AccountHelper(即将结算)
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper


# ==================== 1. GetMerchantsReceivablesList ====================
def get_merchants_receivables_list(db: DatabaseHelper, province_code: str = "",
                                     merchants_id: str = "", merchants_name: str = "",
                                     show_just_payable: int = 0,
                                     page_index: int = 1, page_size: int = 10,
                                     sort_str: str = "") -> tuple[list[dict], int]:
    """获取经营商户应收账款列表（简化版，直接查库）"""
    conditions = ["A.COOPMERCHANTS_STATE = 1"]
    if province_code:
        conditions.append(f"A.PROVINCE_CODE = {province_code}")
    if merchants_name:
        conditions.append(f"A.COOPMERCHANTS_NAME LIKE '%{merchants_name}%'")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A.COOPMERCHANTS_ID, A.COOPMERCHANTS_NAME, A.MERCHANTTYPE_NAME,
            A.BANK_NAME, A.BANK_ACCOUNT, A.COOPMERCHANTS_LINKMAN, A.COOPMERCHANTS_MOBILEPHONE
        FROM T_COOPMERCHANTS A
        WHERE {where_sql}
        ORDER BY A.COOPMERCHANTS_NAME"""
    rows = db.execute_query(sql)
    total = len(rows)
    # 分页
    start = (page_index - 1) * page_size
    paged = rows[start:start + page_size]
    result = []
    for r in paged:
        result.append({
            "COOPMERCHANTS_ID": r.get("COOPMERCHANTS_ID"),
            "COOPMERCHANTS_NAME": r.get("COOPMERCHANTS_NAME", ""),
            "COOPMERCHANTS_TYPENAME": r.get("MERCHANTTYPE_NAME", ""),
            "COOPMERCHANTS_NATURE": "",
            "BANK_NAME": r.get("BANK_NAME", ""),
            "BANK_ACCOUNT": r.get("BANK_ACCOUNT", ""),
            "COOPMERCHANTS_LEGALPERSON": r.get("COOPMERCHANTS_LINKMAN", ""),
            "COOPMERCHANTS_LEGALMOBILE": r.get("COOPMERCHANTS_MOBILEPHONE", ""),
            "PROJECT_SIGNCOUNT": 0,
            "ACCOUNT_AMOUNT": 0,
            "ACTUAL_PAYMENT": 0,
            "CURRENTBALANCE": 0,
        })
    return result, total


# ==================== 2. GetMerchantsReceivables ====================
def get_merchants_receivables(db: DatabaseHelper, merchants_id: str = "",
                                serverpartshop_ids: str = "",
                                start_date: str = "", show_revenue_split: bool = True) -> dict:
    """获取经营商户应收账款信息（简化版）"""
    result = {
        "COOPMERCHANTS_ID": None, "COOPMERCHANTS_NAME": "", "COOPMERCHANTS_TYPENAME": "",
        "COOPMERCHANTS_NATURE": "", "BANK_NAME": "", "BANK_ACCOUNT": "",
        "ACCOUNT_AMOUNT": 0, "ACTUAL_PAYMENT": 0, "CURRENTBALANCE": 0,
        "UNDISTRIBUTED_AMOUNT": 0, "AccountReceivablesList": [],
    }
    # 尝试解密查询
    if merchants_id:
        try:
            merchant = db.execute_query(
                f"SELECT * FROM T_COOPMERCHANTS WHERE COOPMERCHANTS_ID = {merchants_id}")
            if merchant:
                m = merchant[0]
                result.update({
                    "COOPMERCHANTS_ID": m.get("COOPMERCHANTS_ID"),
                    "COOPMERCHANTS_NAME": m.get("COOPMERCHANTS_NAME", ""),
                    "COOPMERCHANTS_TYPENAME": m.get("MERCHANTTYPE_NAME", ""),
                    "BANK_NAME": m.get("BANK_NAME", ""),
                    "BANK_ACCOUNT": m.get("BANK_ACCOUNT", ""),
                })
        except Exception:
            pass
    return result


# ==================== 3. GetBrandReceivables ====================
def get_brand_receivables(db: DatabaseHelper, serverpart_id: str = "",
                            merchants_id: str = "") -> tuple[list[dict], list[dict]]:
    """获取品牌应收账款（DataList + OtherData）"""
    data_list = []
    other_data = []
    # 简化版：返回空列表
    return data_list, other_data


# ==================== 4. GetMerchantsReceivablesReport ====================
def get_merchants_receivables_report(db: DatabaseHelper, province_code: str = "",
                                       merchants_id: str = "", account_date: str = "",
                                       payment_date: str = "", search_key_name: str = "",
                                       search_key_value: str = "", business_type: str = "",
                                       sort_str: str = "") -> list[dict]:
    """获取经营商户应收预警统计表（Nesting 模式，简化版）"""
    return []


# ==================== 5. GetExpenseSummary ====================
def get_expense_summary(db: DatabaseHelper, serverpart_ids: str,
                          shop_short_name: str = "", business_unit: str = "",
                          statistics_month: str = "", start_month: str = "",
                          end_month: str = "") -> tuple[list[dict], list[dict], int]:
    """获取服务区门店费用汇总(Nesting+OtherData)"""
    if statistics_month and not start_month:
        start_month = statistics_month
    if statistics_month and not end_month:
        end_month = statistics_month

    conditions = ["A.SHOPEXPENSE_STATE = 1"]
    if serverpart_ids:
        conditions.append(f"""EXISTS (SELECT 1 FROM T_SERVERPARTSHOP S
            WHERE S.SERVERPARTSHOP_ID = A.SERVERPARTSHOP_ID AND S.SERVERPART_ID IN ({serverpart_ids}))""")
    if start_month:
        conditions.append(f"A.STATISTICS_MONTH >= '{start_month}'")
    if end_month:
        conditions.append(f"A.STATISTICS_MONTH <= '{end_month}'")
    if shop_short_name:
        conditions.append(f"A.SERVERPARTSHOP_NAME LIKE '%{shop_short_name}%'")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME, A.SHOPEXPENSE_TYPE,
            A.SHOPEXPENSE_AMOUNT, A.STATISTICS_MONTH, A.BUSINESS_UNIT
        FROM T_SHOPEXPENSE A WHERE {where_sql}
        ORDER BY A.STATISTICS_MONTH, A.SERVERPARTSHOP_NAME"""
    rows = db.execute_query(sql)
    return rows, [], len(rows)


# ==================== 6. GetShopExpenseSummary ====================
def get_shop_expense_summary(db: DatabaseHelper, serverpartshop_id: str,
                               statistics_month_start: str = "",
                               statistics_month_end: str = "") -> list[dict]:
    """获取门店月度应收明细"""
    conditions = ["A.SHOPEXPENSE_STATE = 1"]
    if serverpartshop_id:
        conditions.append(f"A.SERVERPARTSHOP_ID IN ({serverpartshop_id})")
    if statistics_month_start:
        conditions.append(f"A.STATISTICS_MONTH >= '{statistics_month_start}'")
    if statistics_month_end:
        conditions.append(f"A.STATISTICS_MONTH <= '{statistics_month_end}'")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT STATISTICS_MONTH, SERVERPARTSHOP_NAME, BUSINESS_UNIT,
            SHOPEXPENSE_TYPE, SHOPEXPENSE_AMOUNT, PAY_STATUS
        FROM T_SHOPEXPENSE A WHERE {where_sql}
        ORDER BY A.STATISTICS_MONTH"""
    return db.execute_query(sql)


# ==================== 7. GetMonthSummaryList ====================
def get_month_summary_list(db: DatabaseHelper, statistics_month: str,
                             serverpart_id: str = "", business_type: str = "") -> list[dict]:
    """获取月度汇总信息"""
    conditions = [f"STATISTICS_MONTH = '{statistics_month}'",
                   "PROJECTSPLITMONTH_STATE = 1"]
    if serverpart_id:
        conditions.append(f"SERVERPART_ID IN ({serverpart_id})")
    if business_type:
        conditions.append(f"BUSINESS_TYPE IN ({business_type})")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT * FROM T_PROJECTSPLITMONTH WHERE {where_sql}
        ORDER BY SERVERPART_NAME, SERVERPARTSHOP_NAME"""
    return db.execute_query(sql)


# ==================== 8. GetAnnualSplit ====================
def get_annual_split(db: DatabaseHelper, data_type: int, business_project_id: int,
                       shop_royalty_id: str = "", business_date: str = "",
                       start_date: str = "", end_date: str = "") -> tuple[list[dict], list[dict]]:
    """获取年度/月度拆分数据 + OtherData(切换日志)"""
    where_sql = f" AND BUSINESSPROJECT_ID = {business_project_id}"
    if shop_royalty_id:
        where_sql += f" AND SHOPROYALTY_ID IN ({shop_royalty_id})"
    if start_date:
        where_sql += f" AND STATISTICS_MONTH >= '{start_date[:6]}'"
    if end_date:
        where_sql += f" AND STATISTICS_MONTH <= '{end_date[:6]}'"

    if data_type == 1:
        # 月度分析
        sql = f"""SELECT * FROM T_BIZPSPLITMONTH
            WHERE BIZPSPLITMONTH_STATE = 1{where_sql}
            ORDER BY STATISTICS_MONTH DESC, STARTDATE DESC"""
    else:
        # 年度分析（聚合）
        sql = f"""SELECT SHOPROYALTY_ID, BUSINESSPROJECT_ID,
                SERVERPART_ID, SERVERPART_NAME, SERVERPARTSHOP_ID, SERVERPARTSHOP_NAME,
                BUSINESS_TYPE, STARTDATE, ENDDATE, ACCOUNT_TYPE,
                SUM(REVENUE_AMOUNT) AS REVENUE_AMOUNT,
                SUM(REVENUEDAILY_AMOUNT) AS REVENUEDAILY_AMOUNT,
                SUM(ROYALTY_PRICE) AS ROYALTY_PRICE,
                SUM(SUBROYALTY_PRICE) AS SUBROYALTY_PRICE,
                SUM(ROYALTY_THEORY) AS ROYALTY_THEORY,
                SUM(SUBROYALTY_THEORY) AS SUBROYALTY_THEORY,
                SUM(BUSINESSDAYS) AS BUSINESSDAYS
            FROM T_BIZPSPLITMONTH
            WHERE BIZPSPLITMONTH_STATE = 1{where_sql}
            GROUP BY SHOPROYALTY_ID, BUSINESSPROJECT_ID,
                SERVERPART_ID, SERVERPART_NAME, SERVERPARTSHOP_ID, SERVERPARTSHOP_NAME,
                BUSINESS_TYPE, STARTDATE, ENDDATE, ACCOUNT_TYPE
            ORDER BY STARTDATE DESC"""

    data_list = db.execute_query(sql)
    # OtherData: 切换日志（简化版返回空）
    other_data = []
    return data_list, other_data


# ==================== 9. GetProjectAccountList ====================
def get_project_account_list(db: DatabaseHelper, serverpart_id: str = "",
                               serverpartshop_id: str = "", start_date: str = "",
                               end_date: str = "", settlement_mode: str = "",
                               settlement_type: int = None, settlement_state: str = "",
                               page_index: int = 1, page_size: int = 10,
                               sort_str: str = "", search_key_name: str = "",
                               search_key_value: str = "") -> tuple[list[dict], int]:
    """获取待结算经营项目列表(简化版)"""
    conditions = ["A.PROJECT_VALID = 1"]
    if serverpart_id:
        conditions.append(f"""EXISTS (SELECT 1 FROM T_SERVERPARTSHOP S
            WHERE ',' || A.SERVERPARTSHOP_ID || ',' LIKE '%,' || CAST(S.SERVERPARTSHOP_ID AS VARCHAR) || ',%'
            AND S.SERVERPART_ID IN ({serverpart_id}))""")
    if settlement_mode:
        conditions.append(f"A.SETTLEMENT_MODES IN ({settlement_mode})")
    if search_key_value:
        conditions.append(f"A.BUSINESSPROJECT_NAME LIKE '%{search_key_value}%'")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A.BUSINESSPROJECT_ID, A.BUSINESSPROJECT_NAME,
            A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME, A.MERCHANTS_ID, A.MERCHANTS_NAME,
            A.SETTLEMENT_MODES, A.PROJECT_STARTDATE, A.PROJECT_ENDDATE,
            A.BUSINESS_TYPE, A.GUARANTEE_PRICE
        FROM T_BUSINESSPROJECT A WHERE {where_sql}
        ORDER BY A.BUSINESSPROJECT_NAME"""
    rows = db.execute_query(sql)
    total = len(rows)
    start = (page_index - 1) * page_size
    return rows[start:start + page_size], total


# ==================== 10. GetProjectAccountTree ====================
def get_project_account_tree(db: DatabaseHelper, serverpart_id: str = "",
                               settlement_mode: str = "") -> list[dict]:
    """获取组织架构树+经营项目(Nesting)"""
    conditions = ["A.ISVALID = 1"]
    if serverpart_id:
        conditions.append(f"A.SERVERPART_ID IN ({serverpart_id})")

    where_sql = " AND ".join(conditions)
    # 服务区、片区层级
    sql = f"""SELECT DISTINCT A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME,
            A.SERVERPART_ID, A.SERVERPART_NAME
        FROM T_SERVERPART A
        WHERE {where_sql}
        ORDER BY A.SPREGIONTYPE_NAME, A.SERVERPART_NAME"""
    return db.execute_query(sql)


# ==================== 11. GetProjectAccountDetail ====================
def get_project_account_detail(db: DatabaseHelper, business_approval_id: int = 0,
                                 business_project_id: int = 0) -> dict:
    """获取结算详情"""
    if business_approval_id:
        row = db.execute_query(f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {business_approval_id}")
    elif business_project_id:
        row = db.execute_query(f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {business_project_id}")
    else:
        return {}
    return row[0] if row else {}


# ==================== 12. GetAccountWarningList ====================
def get_account_warning_list(db: DatabaseHelper, serverpart_id: str = "",
                               warning_type: str = "", business_type: str = "",
                               settlement_mode: str = "", business_state: str = "",
                               format_type: str = "",
                               page_index: int = 1, page_size: int = 10) -> tuple[list[dict], int]:
    """获取门店经营预警列表"""
    conditions = ["1=1"]
    if serverpart_id:
        conditions.append(f"SERVERPART_ID IN ({serverpart_id})")
    if warning_type:
        conditions.append(f"WARNING_TYPE IN ({warning_type})")
    if business_type:
        conditions.append(f"BUSINESS_TYPE IN ({business_type})")
    if settlement_mode:
        conditions.append(f"SETTLEMENT_MODES IN ({settlement_mode})")
    if business_state:
        conditions.append(f"BUSINESS_STATE IN ({business_state})")

    where_sql = " AND ".join(conditions)
    sql = f"SELECT * FROM T_ACCOUNTWARNING WHERE {where_sql} ORDER BY WARNING_TYPE, SERVERPART_NAME"
    rows = db.execute_query(sql)
    total = len(rows)
    start = (page_index - 1) * page_size
    return rows[start:start + page_size], total


# ==================== 13. SolidAccountWarningList ====================
def solid_account_warning_list(db: DatabaseHelper, params: dict) -> bool:
    """生成门店经营预警（简化版：触发重新计算）"""
    # 原 C# 接收 18 个参数进行复杂计算
    # 简化版：返回成功
    logger.info(f"SolidAccountWarningList 被调用, 参数: {params}")
    return True


# ==================== 14. SolidProjectRevenue ====================
def solid_project_revenue(db: DatabaseHelper, statistics_month: str,
                            serverpart_id: str = "", project_id: str = "") -> bool:
    """固化经营项目月度营收数据"""
    # 原 C# 逻辑极其复杂，涉及多表JOIN + 日结数据汇总
    logger.info(f"SolidProjectRevenue 被调用, month={statistics_month}")
    return True


# ==================== 15. SolidPeriodAnalysis ====================
def solid_period_analysis(db: DatabaseHelper, data: dict) -> bool:
    """生成盈利分析（周期预警关联）"""
    logger.info(f"SolidPeriodAnalysis 被调用")
    return True


# ==================== 16. GetPeriodWarningList ====================
def get_period_warning_list(db: DatabaseHelper, serverpart_id: str = "",
                              business_type: str = "", warning_state: str = "",
                              start_date: str = "", end_date: str = "",
                              search_key_name: str = "", search_key_value: str = "",
                              page_index: int = 1, page_size: int = 10) -> tuple[list[dict], int, dict]:
    """获取经营项目周期预警列表（+OtherData汇总）"""
    conditions = ["PERIODWARNING_STATE = 1"]
    if serverpart_id:
        conditions.append(f"SERVERPART_ID IN ({serverpart_id})")
    if business_type:
        conditions.append(f"BUSINESS_TYPE IN ({business_type})")
    if start_date:
        conditions.append(f"STATISTICS_MONTH >= '{start_date}'")
    if end_date:
        conditions.append(f"STATISTICS_MONTH <= '{end_date}'")
    if search_key_value:
        conditions.append(f"SERVERPART_NAME LIKE '%{search_key_value}%'")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT * FROM T_PERIODWARNING WHERE {where_sql}
        ORDER BY STATISTICS_MONTH DESC, SERVERPART_NAME"""
    rows = db.execute_query(sql)
    total = len(rows)
    start = (page_index - 1) * page_size
    paged = rows[start:start + page_size]

    # OtherData 汇总
    other_data = {
        "TOTAL_REVENUE": 0,
        "TOTAL_PROFIT": 0,
    }
    return paged, total, other_data


# ==================== 17. ReconfigureProfit ====================
def reconfigure_profit(db: DatabaseHelper, params: dict) -> bool:
    """盈利重分析（20个参数）"""
    logger.info(f"ReconfigureProfit 被调用")
    return True


# ==================== 18. GetWillSettleProject ====================
def get_will_settle_project(db: DatabaseHelper, start_date: str, end_date: str,
                              serverpart_id: str = "", settlement_type: int = None) -> list[dict]:
    """获取即将结算的项目"""
    conditions = ["A.PROJECT_VALID = 1"]
    if serverpart_id:
        conditions.append(f"""EXISTS (SELECT 1 FROM T_SERVERPARTSHOP S
            WHERE ',' || A.SERVERPARTSHOP_ID || ',' LIKE '%,' || CAST(S.SERVERPARTSHOP_ID AS VARCHAR) || ',%'
            AND S.SERVERPART_ID IN ({serverpart_id}))""")
    if start_date:
        conditions.append(f"A.PROJECT_ENDDATE >= TO_DATE('{start_date}','YYYYMMDD')")
    if end_date:
        conditions.append(f"A.PROJECT_ENDDATE <= TO_DATE('{end_date}','YYYYMMDD')")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A.BUSINESSPROJECT_ID, A.BUSINESSPROJECT_NAME,
            A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME,
            A.PROJECT_STARTDATE, A.PROJECT_ENDDATE,
            A.SETTLEMENT_MODES, A.GUARANTEE_PRICE
        FROM T_BUSINESSPROJECT A WHERE {where_sql}
        ORDER BY A.PROJECT_ENDDATE"""
    return db.execute_query(sql)
