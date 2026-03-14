# -*- coding: utf-8 -*-
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
CommercialApi - 财务预算业务服务
从 budget_router.py 中抽取的 SQL 和业务逻辑
"""
from typing import Optional
from datetime import datetime
from calendar import monthrange
from core.database import DatabaseHelper


def get_budget_project_ah_list(db: DatabaseHelper, search_model: dict) -> tuple[int, list[dict]]:
    """获取安徽财务预算表列表"""
    search_model = search_model or {}
    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 20) or 20
    sort_str = search_model.get("SortStr", "BUDGETPROJECT_AH_ID DESC") or "BUDGETPROJECT_AH_ID DESC"
    search_param = search_model.get("SearchParameter") or {}

    conditions, params = [], []
    for field in ["BUDGETPROJECT_YEAR", "BUDGETPROJECT_TYPE", "BUDGETPROJECT_STATE",
                   "SERVERPART_ID", "SPREGIONTYPE_ID"]:
        val = search_param.get(field)
        if val is not None and str(val).strip():
            conditions.append(f'"{field}" = ?')
            params.append(val)

    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

    # 总数
    count_sql = f'SELECT COUNT(*) AS CNT FROM "T_BUDGETPROJECT_AH"{where_sql}'
    count_rows = db.execute_query(count_sql, params)
    total = count_rows[0]["CNT"] if count_rows else 0

    # 分页
    offset = (page_index - 1) * page_size
    data_sql = f'SELECT * FROM "T_BUDGETPROJECT_AH"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
    page_params = (params if params else []) + [page_size, offset]
    page_rows = db.execute_query(data_sql, page_params)

    # 格式化日期
    for r in page_rows:
        if r.get("BUDGETPROJECT_ENDDATE"):
            r["BUDGETPROJECT_ENDDATE"] = str(r["BUDGETPROJECT_ENDDATE"])
        if r.get("OPERATE_DATE"):
            r["OPERATE_DATE"] = str(r["OPERATE_DATE"])

    return int(total), page_rows


def get_budget_project_ah_detail(db: DatabaseHelper, budget_id: int) -> Optional[dict]:
    """获取安徽财务预算表明细"""
    sql = 'SELECT * FROM "T_BUDGETPROJECT_AH" WHERE "BUDGETPROJECT_AH_ID" = ?'
    rows = db.execute_query(sql, [budget_id])
    if not rows:
        return None
    data = rows[0]
    if data.get("BUDGETPROJECT_ENDDATE"):
        data["BUDGETPROJECT_ENDDATE"] = str(data["BUDGETPROJECT_ENDDATE"])
    if data.get("OPERATE_DATE"):
        data["OPERATE_DATE"] = str(data["OPERATE_DATE"])
    return data


def get_budget_project_detail_list(
    db: DatabaseHelper,
    budget_ah_id: Optional[int],
    budget_year: Optional[int],
    statistics_month: Optional[int],
    serverpart_id: Optional[str],
    account_code: Optional[str],
    statistics_date: Optional[str],
) -> list[dict]:
    """获取月度安徽财务预算明细表数据（含递归科目树）"""
    cur_degree = 100.0
    conditions = ["A.BUDGETPROJECT_AH_ID = B.BUDGETPROJECT_AH_ID"]
    params = {}

    if budget_ah_id:
        conditions.append("A.BUDGETPROJECT_AH_ID = :bpid")
        params["bpid"] = budget_ah_id
    if budget_year:
        conditions.append("A.BUDGETPROJECT_YEAR = :bpyear")
        params["bpyear"] = budget_year
    if statistics_date:
        try:
            sd = datetime.strptime(statistics_date.replace("/", "-"), "%Y-%m-%d")
            days_in_month = monthrange(sd.year, sd.month)[1]
            cur_degree = round(sd.day * 100 / days_in_month, 2)
        except Exception:
            pass
        smonth = statistics_date.replace("-", "").replace("/", "")[:6]
        conditions.append("B.STATISTICS_MONTH = :smonth")
        params["smonth"] = int(smonth)
    elif statistics_month:
        conditions.append("B.STATISTICS_MONTH = :smonth")
        params["smonth"] = statistics_month

    if serverpart_id:
        # --- SQL 参数化: serverpart_id 通过整数解析防注入 ---
        sp_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
        if sp_ids:
            conditions.append(f"A.SERVERPART_ID IN ({','.join(sp_ids)})")

    where_sql = " AND ".join(conditions)

    # 预算明细
    budget_sql = f"""SELECT A.SERVERPART_NAME, A.SPREGIONTYPE_NAME,
            B.ACCOUNT_PCODE, B.ACCOUNT_CODE,
            B.BUDGETDETAIL_AMOUNT, B.REVENUE_AMOUNT
        FROM T_BUDGETPROJECT_AH A, T_BUDGETDETAIL_AH B
        WHERE {where_sql}"""
    budget_rows = db.execute_query(budget_sql, params)

    # 科目代码字典
    enum_sql = """SELECT B.FIELDENUM_ID, B.FIELDENUM_PID, B.FIELDENUM_VALUE,
            B.FIELDENUM_NAME, B.FIELDENUM_INDEX
        FROM T_FIELDEXPLAIN A, T_FIELDENUM B
        WHERE A.FIELDEXPLAIN_ID = B.FIELDEXPLAIN_ID
            AND A.FIELDEXPLAIN_FIELD = 'ACCOUNT_CODE' AND B.FIELDENUM_STATUS > 0"""
    enum_rows = db.execute_query(enum_sql)

    # 实际营收
    revenue_rows = []
    if serverpart_id:
        # --- SQL 参数化: 实际营收查询 ---
        sp_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
        if not sp_ids:
            return _build_tree(-1, account_code or "")
        rev_conditions = [f"A.SERVERPART_ID IN ({','.join(sp_ids)})", "A.REVENUEDAILY_STATE = 1"]
        rev_params = {}
        if statistics_date:
            sdate = statistics_date.replace("-", "").replace("/", "")
            rev_conditions.append("A.STATISTICS_DATE >= :rev_sd")
            rev_params["rev_sd"] = f"{sdate[:6]}01"
            rev_conditions.append("A.STATISTICS_DATE <= :rev_ed")
            rev_params["rev_ed"] = sdate[:8]
        elif statistics_month:
            rev_conditions.append("A.STATISTICS_DATE >= :rev_sd")
            rev_params["rev_sd"] = f"{statistics_month}01"
            rev_conditions.append("A.STATISTICS_DATE <= :rev_ed")
            rev_params["rev_ed"] = f"{statistics_month}31"
        try:
            rev_sql = f"""SELECT A.BUSINESS_TYPE, A.SHOPTRADE,
                    SUM(A.REVENUE_AMOUNT) AS REVENUE_AMOUNT
                FROM T_REVENUEDAILY A
                WHERE {' AND '.join(rev_conditions)}
                GROUP BY A.BUSINESS_TYPE, A.SHOPTRADE"""
            revenue_rows = db.execute_query(rev_sql, rev_params if rev_params else {})
        except Exception:
            revenue_rows = []

    # 构建科目树
    budget_by_code = {}
    for r in budget_rows:
        code = r.get("ACCOUNT_CODE")
        if code:
            budget_by_code[str(code)] = r

    def _bind_revenue(account_code_val, node):
        if not revenue_rows:
            return
        rev_map = {
            "60010101": lambda r: str(r.get("BUSINESS_TYPE")) == "1000" and str(r.get("SHOPTRADE", "")) < "2000",
            "60010102": lambda r: str(r.get("BUSINESS_TYPE")) == "1000" and str(r.get("SHOPTRADE", "")) >= "2000" and str(r.get("SHOPTRADE", "")) not in ("7001", "7002"),
            "60010103": lambda r: str(r.get("BUSINESS_TYPE")) == "1000" and str(r.get("SHOPTRADE", "")) in ("7001", "7002"),
            "60010201": lambda r: str(r.get("BUSINESS_TYPE")) != "1000" and str(r.get("SHOPTRADE", "")) >= "2000",
            "60010202": lambda r: str(r.get("BUSINESS_TYPE")) != "1000" and str(r.get("SHOPTRADE", "")) < "2000",
        }
        filter_fn = rev_map.get(str(account_code_val))
        if filter_fn:
            matched = [r for r in revenue_rows if filter_fn(r)]
            if matched:
                total_rev = sum(float(r.get("REVENUE_AMOUNT") or 0) for r in matched)
                node["REVENUE_AMOUNT"] = round(total_rev, 2)
                budget_amt = node.get("BUDGETDETAIL_AMOUNT")
                if budget_amt and float(budget_amt) > 0:
                    node["Budget_Degree"] = round(total_rev / float(budget_amt) * 100, 2)
                    node["Growth_Rate"] = round(node["Budget_Degree"] - cur_degree, 2)
                if str(account_code_val).startswith("600102"):
                    node["ShowRevenue_Amount"] = True
                    node["ShowGrowth_Rate"] = False
                else:
                    node["ShowGrowth_Rate"] = True
            elif node.get("BUDGETDETAIL_AMOUNT") and float(node.get("BUDGETDETAIL_AMOUNT") or 0) > 0:
                node["REVENUE_AMOUNT"] = 0
                node["Budget_Degree"] = 0
                node["Growth_Rate"] = -cur_degree
                node["ShowGrowth_Rate"] = True if str(account_code_val).startswith("600101") else False
                if str(account_code_val).startswith("600102"):
                    node["ShowRevenue_Amount"] = True

    def _build_tree(parent_id, account_code_filter=""):
        children_enums = [e for e in enum_rows if e.get("FIELDENUM_PID") == parent_id]
        if account_code_filter:
            filter_codes = [c.strip() for c in account_code_filter.split(",")]
            children_enums = [e for e in children_enums if str(e.get("FIELDENUM_VALUE")) in filter_codes]
        children_enums.sort(key=lambda x: (x.get("FIELDENUM_INDEX") or 0, str(x.get("FIELDENUM_VALUE") or "")))

        result = []
        for enum in children_enums:
            code_value = str(enum.get("FIELDENUM_VALUE", ""))
            code_name = str(enum.get("FIELDENUM_NAME", ""))
            enum_id = enum.get("FIELDENUM_ID")

            budget_row = budget_by_code.get(code_value)
            node = {
                "BUDGETDETAIL_AH_ID": None, "BUDGETPROJECT_AH_ID": None,
                "ACCOUNT_PCODE": budget_row.get("ACCOUNT_PCODE") if budget_row else None,
                "ACCOUNT_CODE": code_name, "STATISTICS_MONTH": None,
                "BUDGETDETAIL_AMOUNT": budget_row.get("BUDGETDETAIL_AMOUNT") if budget_row else None,
                "REVENUE_AMOUNT": budget_row.get("REVENUE_AMOUNT") if budget_row else None,
                "SERVERPART_NAME": budget_row.get("SERVERPART_NAME") if budget_row else None,
                "SPREGIONTYPE_NAME": budget_row.get("SPREGIONTYPE_NAME") if budget_row else None,
                "Budget_Degree": None, "Growth_Rate": None,
                "ShowGrowth_Rate": False, "ShowRevenue_Amount": None,
            }
            if revenue_rows:
                _bind_revenue(code_value, node)
            elif budget_row and budget_row.get("REVENUE_AMOUNT") is not None:
                node["ShowGrowth_Rate"] = True

            sub_children = [e for e in enum_rows if e.get("FIELDENUM_PID") == enum_id]
            children_list = _build_tree(enum_id) if sub_children else None
            result.append({"node": node, "children": children_list})
        return result

    return _build_tree(-1, account_code or "")
