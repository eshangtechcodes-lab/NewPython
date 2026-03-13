# -*- coding: utf-8 -*-
"""
CommercialApi - 预算费用 Service
从 revenue_router.py 中抽取:
  GetBudgetExpenseList (POST/GET), GetRevenueBudget, GetProvinceRevenueBudget
每个函数独立、可单独迁移

注意: GetProvinceRevenueBudget 逻辑约 300 行, 含 StatisticsType 分支走向,
      暂保留在 Router 层, 此处仅提供声明
"""
from __future__ import annotations
from typing import Optional
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition
from services.commercial.service_utils import safe_float as _sf


# ===== 1. GetBudgetExpenseList (POST) =====
def get_budget_expense_list_post(db: DatabaseHelper, search_model: dict) -> tuple[list, int]:
    """获取预算费用表列表（POST），返回 (rows, total)"""
    if not search_model:
        try:
            count_rows = db.execute_query('SELECT COUNT(*) AS CNT FROM "T_BUDGETEXPENSE"')
            total = count_rows[0]["CNT"] if count_rows else 0
        except Exception:
            total = 0
        return [], total

    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 20) or 20
    search_param = search_model.get("SearchParameter") or {}

    conditions = []
    params = []
    for field in ["STATISTICS_MONTH", "PROVINCE_CODE", "SERVERPART_ID"]:
        val = search_param.get(field)
        if val is not None and str(val).strip():
            conditions.append(f'"{field}" = ?')
            params.append(val)

    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    count_sql = f'SELECT COUNT(*) AS CNT FROM "T_BUDGETEXPENSE"{where_sql}'
    count_rows = db.execute_query(count_sql, params if params else None)
    total = count_rows[0]["CNT"] if count_rows else 0

    offset = (page_index - 1) * page_size
    data_sql = f'SELECT * FROM "T_BUDGETEXPENSE"{where_sql} ORDER BY "BUDGETEXPENSE_ID" DESC LIMIT ? OFFSET ?'
    page_params = (params if params else []) + [page_size, offset]
    page_rows = db.execute_query(data_sql, page_params) or []

    for r in page_rows:
        if r.get("OPERATE_DATE"): r["OPERATE_DATE"] = str(r["OPERATE_DATE"])

    return page_rows, total


# ===== 2. GetBudgetExpenseList (GET) =====
def get_budget_expense_list_get(db: DatabaseHelper, province_code, statistics_month, serverpart_id) -> list:
    """获取预算费用表列表（GET），返回 rows"""
    conditions = []
    params = {}
    if province_code:
        conditions.append('"PROVINCE_CODE" = :pc')
        params["pc"] = province_code
    if statistics_month:
        conditions.append('"STATISTICS_MONTH" = :sm')
        params["sm"] = statistics_month
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition('SERVERPART_ID', _sp_ids))

    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    sql = f'SELECT * FROM "T_BUDGETEXPENSE"{where_sql} ORDER BY "BUDGETEXPENSE_ID" DESC'
    rows = db.execute_query(sql, params if params else None) or []

    for r in rows:
        if r.get("OPERATE_DATE"): r["OPERATE_DATE"] = str(r["OPERATE_DATE"])
    return rows


# ===== 3. GetRevenueBudget =====
def get_revenue_budget(db: DatabaseHelper, statistics_date, province_code, serverpart_id,
                        sp_region_type_id, revenue_include) -> dict:
    """获取计划营收数据"""
    from datetime import datetime as dt
    import calendar

    def safe_dec(v):
        try: return float(v) if v is not None else 0.0
        except: return 0.0

    empty_result = {
        "RevenueMonth_Amount": 0, "RevenueYear_Amount": 0,
        "BudgetMonth_Amount": 0, "BudgetYear_Amount": 0,
        "RevenueYear_PlanAmount": 0,
        "MonthBudget_Degree": 0, "MonthGrowth_Rate": 0,
        "YearBudget_Degree": 0, "YearGrowth_Rate": 0,
        "MonthYOY_Rate": None, "YearYOY_Rate": None,
    }

    if province_code != "340000":
        return empty_result
    if not statistics_date:
        return None  # Router 层返回 Result.fail

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    year_str = stat_date.strftime("%Y")
    month_str = stat_date.strftime("%Y%m")
    month_days = calendar.monthrange(stat_date.year, stat_date.month)[1]

    budget_month = 0.0
    budget_year = 0.0
    plan_amount = 0.0
    sp_id = int(serverpart_id) if serverpart_id else None

    if sp_id:
        bsql = f"""SELECT B."STATISTICS_MONTH", B."BUDGETDETAIL_AMOUNT" AS "BUDGET_AMOUNT"
            FROM "T_BUDGETPROJECT_AH" A, "T_BUDGETDETAIL_AH" B
            WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                AND B."ACCOUNT_CODE" = 1000
                AND B."STATISTICS_MONTH" >= {year_str}01 AND B."STATISTICS_MONTH" <= {year_str}12
                AND A."SERVERPART_ID" = {sp_id}"""
        rows = db.execute_query(bsql) or []
        for r in rows:
            sm = str(int(safe_dec(r.get("STATISTICS_MONTH"))))
            ba = safe_dec(r.get("BUDGET_AMOUNT"))
            if sm == month_str:
                budget_month = ba
                budget_year += ba
                plan_amount += round(ba / month_days * stat_date.day, 2)
            else:
                budget_year += ba
                if int(sm) < int(month_str): plan_amount += ba
    else:
        bsql = f"""SELECT * FROM "T_BUDGETEXPENSE"
            WHERE "PROVINCE_CODE" = {province_code} AND "SERVERPART_ID" = 0
                AND "STATISTICS_MONTH" >= {year_str}01 AND "STATISTICS_MONTH" <= {year_str}12"""
        rows = db.execute_query(bsql) or []
        for r in rows:
            sm = str(int(safe_dec(r.get("STATISTICS_MONTH"))))
            ba = safe_dec(r.get("BUDGET_AMOUNT"))
            sm_date = dt.strptime(sm + "01", "%Y%m%d")
            sm_days = calendar.monthrange(sm_date.year, sm_date.month)[1]
            if sm == month_str:
                budget_month = ba * sm_days
                budget_year += budget_month
                plan_amount += ba * stat_date.day
            else:
                m_total = ba * sm_days
                budget_year += m_total
                if int(sm) < int(month_str): plan_amount += m_total

    if not rows:
        return None  # Router 层返回 Result.fail

    # 查实际营收
    rev_month = 0.0
    rev_year = 0.0
    month_yoy = None
    year_yoy = None

    if not sp_id and not sp_region_type_id:
        date_str = stat_date.strftime("%Y%m%d")
        rsql = f"""SELECT SUM("REVENUE_AMOUNT_MONTH") AS "REVENUE_AMOUNT_MONTH",
                SUM("REVENUE_AMOUNT_YEAR") AS "REVENUE_AMOUNT_YEAR"
            FROM "T_REVENUEDAILY"
            WHERE "REVENUEDAILY_STATE" = 1 AND "BUSINESS_TYPE" = 1000
                AND "SERVERPART_ID" = 0 AND "STATISTICS_DATE" = {date_str}"""
        rr = db.execute_query(rsql) or []
        if rr:
            rev_month = safe_dec(rr[0].get("REVENUE_AMOUNT_MONTH"))
            rev_year = safe_dec(rr[0].get("REVENUE_AMOUNT_YEAR"))
        ly_date = stat_date.replace(year=stat_date.year - 1).strftime("%Y%m%d")
        rsql_ly = rsql.replace(f"= {date_str}", f"= {ly_date}")
        rr_ly = db.execute_query(rsql_ly) or []
        if rr_ly:
            ly_month = safe_dec(rr_ly[0].get("REVENUE_AMOUNT_MONTH"))
            ly_year = safe_dec(rr_ly[0].get("REVENUE_AMOUNT_YEAR"))
            if ly_month > 0: month_yoy = round((rev_month / ly_month - 1) * 100, 2)
            if ly_year > 0: year_yoy = round((rev_year / ly_year - 1) * 100, 2)
    else:
        where2 = ""
        if sp_id: where2 += f' AND B."SERVERPART_ID" = {sp_id}'
        elif sp_region_type_id: where2 += f' AND B."SPREGIONTYPE_ID" = {sp_region_type_id}'
        date_str = stat_date.strftime("%Y%m%d")
        rsql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS_MONTH",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000
                AND A."STATISTICS_DATE" >= {year_str}0101 AND A."STATISTICS_DATE" <= {date_str}{where2}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        rr = db.execute_query(rsql) or []
        for r in rr:
            ra = safe_dec(r.get("REVENUE_AMOUNT"))
            rm = str(int(safe_dec(r.get("STATISTICS_MONTH"))))
            rev_year += ra
            if rm == month_str: rev_month = ra

    month_degree = round(rev_month / budget_month * 100, 2) if budget_month > 0 else 0
    month_growth = round(month_degree - (stat_date.day * 100.0 / month_days), 2) if budget_month > 0 else 0
    year_degree = round(rev_year / budget_year * 100, 2) if budget_year > 0 else 0
    year_growth = round((rev_year - plan_amount) / budget_year * 100, 2) if budget_year > 0 else 0

    return {
        "RevenueMonth_Amount": rev_month, "RevenueYear_Amount": rev_year,
        "BudgetMonth_Amount": budget_month, "BudgetYear_Amount": budget_year,
        "RevenueYear_PlanAmount": plan_amount,
        "MonthBudget_Degree": month_degree, "MonthGrowth_Rate": month_growth,
        "YearBudget_Degree": year_degree, "YearGrowth_Rate": year_growth,
        "MonthYOY_Rate": month_yoy, "YearYOY_Rate": year_yoy,
    }


# ===== 4. GetProvinceRevenueBudget =====
# 此路由约 300 行，含 4 种 StatisticsType 分支，逻辑过长暂保留在 Router 层
# 后续重写 Router 时整体迁移
