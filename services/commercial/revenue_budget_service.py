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
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition
from services.commercial.service_utils import safe_int


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
        # --- SQL 参数化: 预算明细查询 (按服务区) ---
        bsql = """SELECT B."STATISTICS_MONTH", B."BUDGETDETAIL_AMOUNT" AS "BUDGET_AMOUNT"
            FROM "T_BUDGETPROJECT_AH" A, "T_BUDGETDETAIL_AH" B
            WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                AND B."ACCOUNT_CODE" = 1000
                AND B."STATISTICS_MONTH" >= :m_start AND B."STATISTICS_MONTH" <= :m_end
                AND A."SERVERPART_ID" = :sp_id"""
        rows = db.execute_query(bsql, {"m_start": f"{year_str}01", "m_end": f"{year_str}12", "sp_id": sp_id}) or []
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
        # --- SQL 参数化: 预算费用查询 (全省) ---
        bsql = """SELECT * FROM "T_BUDGETEXPENSE"
            WHERE "PROVINCE_CODE" = :pc AND "SERVERPART_ID" = 0
                AND "STATISTICS_MONTH" >= :m_start AND "STATISTICS_MONTH" <= :m_end"""
        rows = db.execute_query(bsql, {"pc": province_code, "m_start": f"{year_str}01", "m_end": f"{year_str}12"}) or []
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
        # --- SQL 参数化: 日营收查询 (全省汇总) ---
        rsql = """SELECT SUM("REVENUE_AMOUNT_MONTH") AS "REVENUE_AMOUNT_MONTH",
                SUM("REVENUE_AMOUNT_YEAR") AS "REVENUE_AMOUNT_YEAR"
            FROM "T_REVENUEDAILY"
            WHERE "REVENUEDAILY_STATE" = 1 AND "BUSINESS_TYPE" = 1000
                AND "SERVERPART_ID" = 0 AND "STATISTICS_DATE" = :stat_date"""
        rr = db.execute_query(rsql, {"stat_date": date_str}) or []
        if rr:
            rev_month = safe_dec(rr[0].get("REVENUE_AMOUNT_MONTH"))
            rev_year = safe_dec(rr[0].get("REVENUE_AMOUNT_YEAR"))
        # --- SQL 参数化: 同比营收查询 ---
        ly_date = stat_date.replace(year=stat_date.year - 1).strftime("%Y%m%d")
        rr_ly = db.execute_query(rsql, {"stat_date": ly_date}) or []
        if rr_ly:
            ly_month = safe_dec(rr_ly[0].get("REVENUE_AMOUNT_MONTH"))
            ly_year = safe_dec(rr_ly[0].get("REVENUE_AMOUNT_YEAR"))
            if ly_month > 0: month_yoy = round((rev_month / ly_month - 1) * 100, 2)
            if ly_year > 0: year_yoy = round((rev_year / ly_year - 1) * 100, 2)
    else:
        # --- SQL 参数化: 日营收按月分组查询 ---
        where2 = ""
        rev_params = {"y_start": f"{year_str}0101", "d_end": stat_date.strftime("%Y%m%d")}
        if sp_id:
            where2 += ' AND B."SERVERPART_ID" = :sp_id'
            rev_params["sp_id"] = sp_id
        elif sp_region_type_id:
            where2 += ' AND B."SPREGIONTYPE_ID" = :srt_id'
            rev_params["srt_id"] = sp_region_type_id
        rsql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS_MONTH",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000
                AND A."STATISTICS_DATE" >= :y_start AND A."STATISTICS_DATE" <= :d_end{where2}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
        rr = db.execute_query(rsql, rev_params) or []
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


# ===== 5. GetProvinceRevenueBudget =====
def get_province_revenue_budget(db: DatabaseHelper, statistics_date, province_code,
                                 statistics_type, sp_region_type_id, serverpart_id,
                                 show_whole_year) -> dict | None:
    """获取全省计划营收分析（4种 StatisticsType 分支）
    返回 dict 数据或 None (表示无数据/非340000)
    """
    from datetime import datetime as dt
    import calendar

    def safe_dec(v):
        try: return float(v) if v is not None else 0.0
        except: return 0.0

    if province_code != "340000":
        return None
    if not statistics_date:
        return None

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    yyyyMM = stat_date.strftime("%Y%m")
    yyyyMMdd = stat_date.strftime("%Y%m%d")
    yyyy01 = stat_date.strftime("%Y01")
    yyyy12 = stat_date.strftime("%Y12")
    yyyy0101 = stat_date.strftime("%Y0101")
    yyyyMM01 = stat_date.strftime("%Y%m01")
    day_of_month = stat_date.day
    days_in_month = calendar.monthrange(stat_date.year, stat_date.month)[1]

    Revenue_PlanAmount = 0.0
    Budget_Amount = 0.0

    # 1. 构建预算查询 WhereSQL
    # --- SQL 参数化: 预算查询动态 WHERE ---
    where_sql = ""
    budget_params = {}
    if serverpart_id is not None:
        where_sql += ' AND B."SERVERPART_ID" = :sp_id'
        budget_params["sp_id"] = serverpart_id
    elif sp_region_type_id is not None:
        where_sql += ' AND B."SPREGIONTYPE_ID" = :srt_id'
        budget_params["srt_id"] = sp_region_type_id
    elif province_code:
        where_sql += ' AND A."PROVINCE_CODE" = :pc'
        budget_params["pc"] = province_code
        if statistics_type == 2:
            where_sql += ' AND A."SERVERPART_ID" = 0'
    if statistics_type in (1, 4):
        where_sql += ' AND A."STATISTICS_MONTH" = :stat_month'
        budget_params["stat_month"] = yyyyMM
    else:
        where_sql += ' AND A."STATISTICS_MONTH" >= :m_start AND A."STATISTICS_MONTH" <= :m_end'
        budget_params["m_start"] = yyyy01
        budget_params["m_end"] = yyyy12

    # 2. 查询预算数据
    budget_rows = []
    if statistics_type == 3:
        budget_sql = f"""SELECT A."STATISTICS_MONTH", B."SERVERPART_ID", B."SERVERPART_NAME",
                A."BUDGETDETAIL_AMOUNT" AS "BUDGET_AMOUNT",
                B."SPREGIONTYPE_ID", B."SPREGIONTYPE_NAME", 1000 AS "STATISTICS_TYPE"
            FROM "T_BUDGETDETAIL_AH" A, "T_BUDGETPROJECT_AH" B
            WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                AND A."ACCOUNT_CODE" = 1000{where_sql}
            ORDER BY A."STATISTICS_MONTH" """
        budget_rows = db.execute_query(budget_sql, budget_params) or []
        for r in budget_rows:
            sm = str(r.get("STATISTICS_MONTH", ""))
            ba = safe_dec(r.get("BUDGET_AMOUNT"))
            if sm == yyyyMM:
                Budget_Amount += ba
                Revenue_PlanAmount += round(ba * day_of_month / days_in_month, 2)
            else:
                if safe_int(sm) < safe_int(yyyyMM):
                    Revenue_PlanAmount += ba
                Budget_Amount += ba
    else:
        budget_sql = f"""SELECT A."STATISTICS_MONTH", A."PROVINCE_CODE", A."SERVERPART_ID",
                A."SERVERPART_NAME", A."BUDGET_AMOUNT", A."SPREGIONTYPE_ID",
                A."SPREGIONTYPE_NAME", A."SERVERPART_IDS", B."STATISTICS_TYPE"
            FROM "T_BUDGETEXPENSE" A
            LEFT JOIN "T_SERVERPART" B ON A."SERVERPART_ID" = B."SERVERPART_ID"
            WHERE 1 = 1{where_sql}"""
        budget_rows = db.execute_query(budget_sql, budget_params) or []
        if sp_region_type_id is None:
            filtered = [r for r in budget_rows if safe_int(r.get("SERVERPART_ID")) == 0]
        else:
            filtered = budget_rows
        for r in sorted(filtered, key=lambda x: str(x.get("STATISTICS_MONTH", ""))):
            sm = str(r.get("STATISTICS_MONTH", ""))
            ba = safe_dec(r.get("BUDGET_AMOUNT"))
            try:
                cd = dt.strptime(sm + "01", "%Y%m%d")
                cmd = calendar.monthrange(cd.year, cd.month)[1]
            except:
                cmd = 30
            if sm == yyyyMM:
                Budget_Amount += ba * cmd
                Revenue_PlanAmount += ba * day_of_month
            else:
                bv = ba * cmd
                if safe_int(sm) < safe_int(yyyyMM):
                    Revenue_PlanAmount += bv
                Budget_Amount += bv
        if statistics_type == 4 and sp_region_type_id is not None:
            # --- SQL 参数化: 片区预算明细查询 ---
            sp_sql = """SELECT B."STATISTICS_MONTH", A."SERVERPART_ID", A."SERVERPART_NAME",
                    B."BUDGETDETAIL_AMOUNT", A."SPREGIONTYPE_ID", A."SPREGIONTYPE_NAME",
                    1000 AS "STATISTICS_TYPE"
                FROM "T_BUDGETPROJECT_AH" A, "T_BUDGETDETAIL_AH" B
                WHERE A."BUDGETPROJECT_AH_ID" = B."BUDGETPROJECT_AH_ID"
                    AND B."ACCOUNT_CODE" = 1000
                    AND B."STATISTICS_MONTH" = :stat_month
                    AND A."SPREGIONTYPE_ID" = :srt_id"""
            sp_rows = db.execute_query(sp_sql, {"stat_month": yyyyMM, "srt_id": sp_region_type_id}) or []
            for sr in sp_rows:
                budget_rows.append({
                    "STATISTICS_MONTH": sr.get("STATISTICS_MONTH"),
                    "SERVERPART_ID": sr.get("SERVERPART_ID"),
                    "SERVERPART_NAME": sr.get("SERVERPART_NAME"),
                    "BUDGET_AMOUNT": sr.get("BUDGETDETAIL_AMOUNT"),
                    "SPREGIONTYPE_ID": sr.get("SPREGIONTYPE_ID"),
                    "SPREGIONTYPE_NAME": sr.get("SPREGIONTYPE_NAME"),
                    "STATISTICS_TYPE": 1000,
                })

    if Budget_Amount == 0:
        return None

    # 3. 统计营收数据
    # --- SQL 参数化: 营收查询动态 WHERE ---
    where_rev = ""
    rev_params = {}
    if serverpart_id is not None:
        where_rev += ' AND B."SERVERPART_ID" = :sp_id'
        rev_params["sp_id"] = serverpart_id
    elif sp_region_type_id is not None:
        if statistics_type == 3:
            sp_ids = set(str(safe_int(r.get("SERVERPART_ID"))) for r in budget_rows)
            sp_ids.discard("0")
            # f-string: 安全 — sp_ids 来自 safe_int() 转换后的字符串
            where_rev += f' AND B."SERVERPART_ID" IN ({",".join(sp_ids)})' if sp_ids else ' AND 1 = 2'
        else:
            has_ids = any(r.get("SERVERPART_IDS") for r in budget_rows)
            if has_ids:
                matched = [r for r in budget_rows if safe_int(r.get("SPREGIONTYPE_ID")) == sp_region_type_id]
                if matched and matched[0].get("SERVERPART_IDS"):
                    # f-string: 安全 — SERVERPART_IDS 来自数据库字段
                    where_rev += f' AND B."SERVERPART_ID" IN ({matched[0]["SERVERPART_IDS"]})'
                else:
                    where_rev += ' AND 1 = 2'
            else:
                where_rev += ' AND B."SPREGIONTYPE_ID" = :srt_id'
                rev_params["srt_id"] = sp_region_type_id
    elif province_code:
        where_rev += ' AND B."PROVINCE_CODE" = :pc'
        rev_params["pc"] = province_code
    if statistics_type in (1, 4):
        where_rev += ' AND A."STATISTICS_DATE" >= :d_start'
        rev_params["d_start"] = yyyyMM01
    else:
        where_rev += ' AND A."STATISTICS_DATE" >= :d_start'
        rev_params["d_start"] = yyyy0101
    where_rev += ' AND A."STATISTICS_DATE" <= :d_end'
    rev_params["d_end"] = yyyyMMdd

    if statistics_type in (1, 4):
        rev_sql = f"""SELECT B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000{where_rev}
            GROUP BY B."SERVERPART_ID", B."SERVERPART_NAME", B."SERVERPART_INDEX" """
    else:
        rev_sql = f"""SELECT SUBSTR(CAST(A."STATISTICS_DATE" AS VARCHAR), 1, 6) AS "STATISTICS_MONTH",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000 AND A."BUSINESS_TYPE" = 1000{where_rev}
            GROUP BY SUBSTR(CAST(A."STATISTICS_DATE" AS VARCHAR), 1, 6)"""
    rev_rows = db.execute_query(rev_sql, rev_params) or []

    Revenue_Amount = sum(safe_dec(r.get("REVENUE_AMOUNT")) for r in rev_rows)
    Budget_Degree = round(Revenue_Amount / Budget_Amount * 100, 2) if Budget_Amount > 0 else 0

    # 4. 构建 RegionBudgetList
    region_list = []
    Growth_Rate = 0.0

    if statistics_type == 1:
        Growth_Rate = round(Budget_Degree - (day_of_month * 100.0 / days_in_month), 2)
        for r in sorted([b for b in budget_rows if safe_int(b.get("STATISTICS_TYPE")) == 1010],
                       key=lambda x: str(x.get("STATISTICS_MONTH", ""))):
            ids_str = str(r.get("SERVERPART_IDS", "") or "")
            id_set = set(ids_str.split(",")) if ids_str else set()
            sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                       if str(safe_int(rr.get("SERVERPART_ID"))) in id_set)
            sp_bgt = safe_dec(r.get("BUDGET_AMOUNT")) * days_in_month
            sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
            region_list.append({
                "Serverpart_ID": safe_int(r.get("SPREGIONTYPE_ID")),
                "Serverpart_Name": str(r.get("SPREGIONTYPE_NAME", "")),
                "Revenue_Amount": sp_rev, "Budget_Amount": sp_bgt,
                "Budget_Degree": sp_deg,
                "Growth_Rate": round(sp_deg - (day_of_month * 100.0 / days_in_month), 2),
            })
    elif statistics_type == 4:
        Growth_Rate = round(Budget_Degree - (day_of_month * 100.0 / days_in_month), 2)
        for r in sorted([b for b in budget_rows if safe_int(b.get("STATISTICS_TYPE")) == 1000],
                       key=lambda x: safe_dec(x.get("BUDGET_AMOUNT")), reverse=True):
            sp_id = safe_int(r.get("SERVERPART_ID"))
            sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                       if safe_int(rr.get("SERVERPART_ID")) == sp_id)
            sp_bgt = safe_dec(r.get("BUDGET_AMOUNT"))
            sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
            region_list.append({
                "Serverpart_ID": sp_id,
                "Serverpart_Name": str(r.get("SERVERPART_NAME", "")),
                "Revenue_Amount": sp_rev, "Budget_Amount": sp_bgt,
                "Budget_Degree": sp_deg,
                "Growth_Rate": round(sp_deg - (day_of_month * 100.0 / days_in_month), 2),
            })
    elif statistics_type == 2:
        Growth_Rate = round((Revenue_Amount - Revenue_PlanAmount) / Budget_Amount * 100, 2) if Budget_Amount > 0 else 0
        mf = [b for b in budget_rows if safe_int(b.get("SERVERPART_ID")) == 0]
        if not show_whole_year:
            mf = [b for b in mf if safe_int(b.get("STATISTICS_MONTH")) <= safe_int(yyyyMM)]
        for r in sorted(mf, key=lambda x: str(x.get("STATISTICS_MONTH", ""))):
            sm = str(r.get("STATISTICS_MONTH", ""))
            try:
                cd = dt.strptime(sm + "01", "%Y%m%d")
                cmd = calendar.monthrange(cd.year, cd.month)[1]
            except: cmd = 30
            sm_m = int(sm[4:6]) if len(sm) >= 6 else 0
            sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                       if str(rr.get("STATISTICS_MONTH", "")) == sm)
            sp_bgt = safe_dec(r.get("BUDGET_AMOUNT")) * cmd
            sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
            if sm == yyyyMM:
                g = round(sp_deg - (day_of_month * 100.0 / cmd), 2)
            elif safe_int(sm) < safe_int(yyyyMM):
                g = sp_deg - 100
            else:
                g = 0
            region_list.append({
                "Statistics_Month": sm_m, "Revenue_Amount": sp_rev,
                "Budget_Amount": sp_bgt, "Budget_Degree": sp_deg, "Growth_Rate": g,
            })
    elif statistics_type == 3:
        Growth_Rate = round((Revenue_Amount - Revenue_PlanAmount) / Budget_Amount * 100, 2) if Budget_Amount > 0 else 0
        u_months = sorted(set(str(r.get("STATISTICS_MONTH", "")) for r in budget_rows))
        if not show_whole_year:
            u_months = [m for m in u_months if safe_int(m) <= safe_int(yyyyMM)]
        for sm in u_months:
            try:
                cd = dt.strptime(sm + "01", "%Y%m%d")
                cmd = calendar.monthrange(cd.year, cd.month)[1]
            except: cmd = 30
            sm_m = int(sm[4:6]) if len(sm) >= 6 else 0
            sp_rev = sum(safe_dec(rr.get("REVENUE_AMOUNT")) for rr in rev_rows
                       if str(rr.get("STATISTICS_MONTH", "")) == sm)
            sp_bgt = sum(safe_dec(br.get("BUDGET_AMOUNT")) for br in budget_rows
                       if str(br.get("STATISTICS_MONTH", "")) == sm)
            sp_deg = round(sp_rev / sp_bgt * 100, 2) if sp_bgt > 0 else 0
            if sm == yyyyMM:
                g = round(sp_deg - (day_of_month * 100.0 / cmd), 2)
            elif safe_int(sm) < safe_int(yyyyMM):
                g = sp_deg - 100
            else:
                g = 0
            region_list.append({
                "Statistics_Month": sm_m, "Revenue_Amount": sp_rev,
                "Budget_Amount": sp_bgt, "Budget_Degree": sp_deg, "Growth_Rate": g,
            })

    return {
        "Revenue_Amount": Revenue_Amount, "Budget_Amount": Budget_Amount,
        "Budget_Degree": Budget_Degree, "Growth_Rate": Growth_Rate,
        "RegionBudgetList": region_list,
    }
