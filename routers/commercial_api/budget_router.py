# -*- coding: utf-8 -*-
"""
CommercialApi - Budget 路由
对应原 CommercialApi/Controllers/BudgetController.cs
财务预算相关接口（6个接口）
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from core.old_api_proxy import proxy_to_old_api
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


# ===== 1. GetBUDGETPROJECT_AHList =====
@router.post("/Budget/GetBUDGETPROJECT_AHList")
async def get_budget_project_ah_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取安徽财务预算表列表"""
    try:
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        sort_str = searchModel.get("SortStr", "BUDGETPROJECT_AH_ID DESC") or "BUDGETPROJECT_AH_ID DESC"
        search_param = searchModel.get("SearchParameter") or {}

        conditions = []
        params = []

        # 通用字段过滤（基于 SearchParameter 中的非空值）
        for field in ["BUDGETPROJECT_YEAR", "BUDGETPROJECT_TYPE", "BUDGETPROJECT_STATE",
                       "SERVERPART_ID", "SPREGIONTYPE_ID"]:
            val = search_param.get(field)
            if val is not None and str(val).strip():
                conditions.append(f'"{field}" = ?')
                params.append(val)

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        # 查询总数
        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_BUDGETPROJECT_AH"{where_sql}'
        count_rows = db.execute_query(count_sql, params)
        total = count_rows[0]["CNT"] if count_rows else 0

        # 分页查询
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

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBUDGETPROJECT_AHList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 2. GetBUDGETPROJECT_AHDetail =====
@router.get("/Budget/GetBUDGETPROJECT_AHDetail")
async def get_budget_project_ah_detail(
    BUDGETPROJECT_AHId: Optional[int] = Query(None, description="安徽财务预算表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细"""
    try:
        sql = 'SELECT * FROM "T_BUDGETPROJECT_AH" WHERE "BUDGETPROJECT_AH_ID" = ?'
        rows = db.execute_query(sql, [BUDGETPROJECT_AHId])
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        data = rows[0]
        if data.get("BUDGETPROJECT_ENDDATE"):
            data["BUDGETPROJECT_ENDDATE"] = str(data["BUDGETPROJECT_ENDDATE"])
        if data.get("OPERATE_DATE"):
            data["OPERATE_DATE"] = str(data["OPERATE_DATE"])

        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBUDGETPROJECT_AHDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")



# ===== 5. GetBudgetProjectDetailList =====
@router.get("/Budget/GetBudgetProjectDetailList")
async def get_budget_project_detail_list(
    BUDGETPROJECT_AH_ID: Optional[int] = Query(None, description="预算项目ID"),
    BUDGETPROJECT_YEAR: Optional[int] = Query(None, description="项目年份"),
    STATISTICS_MONTH: Optional[int] = Query(None, description="统计月份"),
    SERVERPART_ID: Optional[str] = Query("", description="服务区内码"),
    ACCOUNT_CODE: Optional[str] = Query("", description="一级科目代码"),
    STATISTICS_DATE: Optional[str] = Query("", description="结算日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度安徽财务预算明细表数据"""
    try:
        import math
        from datetime import datetime
        from calendar import monthrange

        # 1. 构建 WHERE 条件（对应C# 逻辑）
        cur_degree = 100.0  # 默认计划完成度100%
        conditions = ["A.BUDGETPROJECT_AH_ID = B.BUDGETPROJECT_AH_ID"]
        params = {}
        if BUDGETPROJECT_AH_ID:
            conditions.append("A.BUDGETPROJECT_AH_ID = :bpid")
            params["bpid"] = BUDGETPROJECT_AH_ID
        if BUDGETPROJECT_YEAR:
            conditions.append("A.BUDGETPROJECT_YEAR = :bpyear")
            params["bpyear"] = BUDGETPROJECT_YEAR
        if STATISTICS_DATE:
            # 从日期计算理论完成度
            try:
                sd = datetime.strptime(STATISTICS_DATE.replace("/", "-"), "%Y-%m-%d")
                days_in_month = monthrange(sd.year, sd.month)[1]
                cur_degree = round(sd.day * 100 / days_in_month, 2)
            except Exception:
                pass
            smonth = STATISTICS_DATE.replace("-", "").replace("/", "")[:6]
            conditions.append("B.STATISTICS_MONTH = :smonth")
            params["smonth"] = int(smonth)
        elif STATISTICS_MONTH:
            conditions.append("B.STATISTICS_MONTH = :smonth")
            params["smonth"] = STATISTICS_MONTH

        if SERVERPART_ID:
            conditions.append(f"A.SERVERPART_ID IN ({SERVERPART_ID})")

        where_sql = " AND ".join(conditions)

        # 2. 查询预算明细数据
        budget_sql = f"""SELECT A.SERVERPART_NAME, A.SPREGIONTYPE_NAME, 
                B.ACCOUNT_PCODE, B.ACCOUNT_CODE,
                B.BUDGETDETAIL_AMOUNT, B.REVENUE_AMOUNT
            FROM T_BUDGETPROJECT_AH A, T_BUDGETDETAIL_AH B
            WHERE {where_sql}"""
        budget_rows = db.execute_query(budget_sql, params)

        # 3. 查询科目代码字典
        enum_sql = """SELECT B.FIELDENUM_ID, B.FIELDENUM_PID, B.FIELDENUM_VALUE, 
                B.FIELDENUM_NAME, B.FIELDENUM_INDEX 
            FROM T_FIELDEXPLAIN A, T_FIELDENUM B
            WHERE A.FIELDEXPLAIN_ID = B.FIELDEXPLAIN_ID 
                AND A.FIELDEXPLAIN_FIELD = 'ACCOUNT_CODE' AND B.FIELDENUM_STATUS > 0"""
        enum_rows = db.execute_query(enum_sql)

        # 4. 查询实际营收（如果指定了服务区）
        revenue_rows = []
        if SERVERPART_ID:
            rev_conditions = [f"A.SERVERPART_ID IN ({SERVERPART_ID})", "A.REVENUEDAILY_STATE = 1"]
            rev_params = {}
            if STATISTICS_DATE:
                sdate = STATISTICS_DATE.replace("-", "").replace("/", "")
                rev_conditions.append(f"A.STATISTICS_DATE >= {sdate[:6]}01")
                rev_conditions.append(f"A.STATISTICS_DATE <= {sdate[:8]}")
            elif STATISTICS_MONTH:
                rev_conditions.append(f"A.STATISTICS_DATE >= {STATISTICS_MONTH}01")
                rev_conditions.append(f"A.STATISTICS_DATE <= {STATISTICS_MONTH}31")
            rev_where = " AND ".join(rev_conditions)
            try:
                rev_sql = f"""SELECT A.BUSINESS_TYPE, A.SHOPTRADE,
                        SUM(A.REVENUE_AMOUNT) AS REVENUE_AMOUNT
                    FROM T_REVENUEDAILY A
                    WHERE {rev_where}
                    GROUP BY A.BUSINESS_TYPE, A.SHOPTRADE"""
                revenue_rows = db.execute_query(rev_sql, rev_params)
            except Exception:
                revenue_rows = []

        # 5. 递归构建科目代码树（对应C# BindAccountCodeData）
        # 将budget数据按ACCOUNT_CODE索引
        budget_by_code = {}
        for r in budget_rows:
            code = r.get("ACCOUNT_CODE")
            if code:
                budget_by_code[str(code)] = r

        def bind_revenue_data(account_code, node):
            """绑定实际营收数据（对应C# BindRevenueData）"""
            if not revenue_rows:
                return
            rev_map = {
                "60010101": lambda r: str(r.get("BUSINESS_TYPE")) == "1000" and str(r.get("SHOPTRADE", "")) < "2000",
                "60010102": lambda r: str(r.get("BUSINESS_TYPE")) == "1000" and str(r.get("SHOPTRADE", "")) >= "2000" and str(r.get("SHOPTRADE", "")) not in ("7001", "7002"),
                "60010103": lambda r: str(r.get("BUSINESS_TYPE")) == "1000" and str(r.get("SHOPTRADE", "")) in ("7001", "7002"),
                "60010201": lambda r: str(r.get("BUSINESS_TYPE")) != "1000" and str(r.get("SHOPTRADE", "")) >= "2000",
                "60010202": lambda r: str(r.get("BUSINESS_TYPE")) != "1000" and str(r.get("SHOPTRADE", "")) < "2000",
            }
            filter_fn = rev_map.get(str(account_code))
            if filter_fn:
                matched = [r for r in revenue_rows if filter_fn(r)]
                if matched:
                    total_rev = sum(float(r.get("REVENUE_AMOUNT") or 0) for r in matched)
                    node["REVENUE_AMOUNT"] = round(total_rev, 2)
                    budget_amt = node.get("BUDGETDETAIL_AMOUNT")
                    if budget_amt and float(budget_amt) > 0:
                        node["Budget_Degree"] = round(total_rev / float(budget_amt) * 100, 2)
                        node["Growth_Rate"] = round(node["Budget_Degree"] - cur_degree, 2)
                    if str(account_code).startswith("600102"):
                        node["ShowRevenue_Amount"] = True
                        node["ShowGrowth_Rate"] = False
                    else:
                        node["ShowGrowth_Rate"] = True
                elif node.get("BUDGETDETAIL_AMOUNT") and float(node.get("BUDGETDETAIL_AMOUNT") or 0) > 0:
                    node["REVENUE_AMOUNT"] = 0
                    node["Budget_Degree"] = 0
                    node["Growth_Rate"] = -cur_degree
                    node["ShowGrowth_Rate"] = True if str(account_code).startswith("600101") else False
                    if str(account_code).startswith("600102"):
                        node["ShowRevenue_Amount"] = True

        def build_tree(parent_id, account_code_filter=""):
            """递归构建科目代码树"""
            # 按父级ID筛选子节点
            children_enums = [e for e in enum_rows if e.get("FIELDENUM_PID") == parent_id]
            if account_code_filter:
                filter_codes = [c.strip() for c in account_code_filter.split(",")]
                children_enums = [e for e in children_enums if str(e.get("FIELDENUM_VALUE")) in filter_codes]
            # 排序
            children_enums.sort(key=lambda x: (x.get("FIELDENUM_INDEX") or 0, str(x.get("FIELDENUM_VALUE") or "")))

            result = []
            for enum in children_enums:
                code_value = str(enum.get("FIELDENUM_VALUE", ""))
                code_name = str(enum.get("FIELDENUM_NAME", ""))
                enum_id = enum.get("FIELDENUM_ID")

                # 构建节点
                budget_row = budget_by_code.get(code_value)
                if budget_row:
                    node = {
                        "BUDGETDETAIL_AH_ID": None,
                        "BUDGETPROJECT_AH_ID": None,
                        "ACCOUNT_PCODE": budget_row.get("ACCOUNT_PCODE"),
                        "ACCOUNT_CODE": code_name,
                        "STATISTICS_MONTH": None,
                        "BUDGETDETAIL_AMOUNT": budget_row.get("BUDGETDETAIL_AMOUNT"),
                        "REVENUE_AMOUNT": budget_row.get("REVENUE_AMOUNT"),
                        "SERVERPART_NAME": budget_row.get("SERVERPART_NAME"),
                        "SPREGIONTYPE_NAME": budget_row.get("SPREGIONTYPE_NAME"),
                        "Budget_Degree": None,
                        "Growth_Rate": None,
                        "ShowGrowth_Rate": False,
                        "ShowRevenue_Amount": None,
                    }
                    if revenue_rows:
                        bind_revenue_data(code_value, node)
                    elif budget_row.get("REVENUE_AMOUNT") is not None:
                        node["ShowGrowth_Rate"] = True
                else:
                    node = {
                        "BUDGETDETAIL_AH_ID": None,
                        "BUDGETPROJECT_AH_ID": None,
                        "ACCOUNT_PCODE": None,
                        "ACCOUNT_CODE": code_name,
                        "STATISTICS_MONTH": None,
                        "BUDGETDETAIL_AMOUNT": None,
                        "REVENUE_AMOUNT": None,
                        "SERVERPART_NAME": None,
                        "SPREGIONTYPE_NAME": None,
                        "Budget_Degree": None,
                        "Growth_Rate": None,
                        "ShowGrowth_Rate": False,
                        "ShowRevenue_Amount": None,
                    }
                    if revenue_rows:
                        bind_revenue_data(code_value, node)

                # 递归构建子树
                sub_children = [e for e in enum_rows if e.get("FIELDENUM_PID") == enum_id]
                children_list = build_tree(enum_id) if sub_children else None

                result.append({"node": node, "children": children_list})
            return result

        # 构建树（-1 为根节点的父ID）
        tree_list = build_tree(-1, ACCOUNT_CODE or "")

        json_list = JsonListData.create(data_list=tree_list, total=len(tree_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetProjectDetailList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 6. GetBudgetMainShow =====
@router.get("/Budget/GetBudgetMainShow")
async def get_budget_main_show(
    serverpartId: Optional[str] = Query(None, description="服务区内码"),
    year: Optional[int] = Query(None, description="年份"),
    month: Optional[int] = Query(None, description="月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取安徽财务预算表明细（主页展示）"""
    try:
        # TODO: 实现查询逻辑 - ESCG.BudgetShowAhHelper.GetBudgetMainShow
        logger.warning("GetBudgetMainShow 查询逻辑暂未实现")
        _cost_item = {"Name": None, "ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None, "PartRate": None}
        _income_item = {"Name": None, "ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None,
                         "ThisMonthIncome": None, "ThisMonthIncomeRate": None, "Details": None}
        return Result.success(data={
            "Cost": {
                "ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None,
                "InOutRate": None, "Items": [_cost_item],
            },
            "Income": {
                "ThisYearBudget": None, "ThisYearTotal": None, "CompleteRate": None,
                "CostRate": None, "IncomeChangeRate": None, "ThisYearCost": None,
                "Items": [_income_item],
            },
            "monthAmount": {
                "ThisMonthIn": None, "ThisMonthOut": None,
                "CostInRate": None, "InOutRate": None,
                "IncomeChangeRate": None, "PayoutChangeRate": None,
            },
            "yearProfit": {
                "ThisYearTotal": None, "ThisYearTotalC": None,
                "ThisYearBudget": None, "ThisYearBudgetC": None,
                "CompleteRate": None, "CompleteRateC": None, "TRate": None,
            },
        }, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBudgetMainShow 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
