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
        # 动态 WHERE（参照 C# BUDGETDETAIL_AHHelper.GetBudgetProjectDetailList）
        conditions = ["A.BUDGETPROJECT_AH_ID = B.BUDGETPROJECT_AH_ID"]
        params = {}
        if BUDGETPROJECT_AH_ID:
            conditions.append("A.BUDGETPROJECT_AH_ID = :bpid")
            params["bpid"] = BUDGETPROJECT_AH_ID
        if BUDGETPROJECT_YEAR:
            conditions.append("A.BUDGETPROJECT_YEAR = :bpyear")
            params["bpyear"] = BUDGETPROJECT_YEAR
        if STATISTICS_MONTH:
            conditions.append("B.STATISTICS_MONTH = :smonth")
            params["smonth"] = STATISTICS_MONTH
        elif STATISTICS_DATE:
            # 从日期提取月份 yyyyMM
            smonth = STATISTICS_DATE.replace("-", "")[:6]
            conditions.append("B.STATISTICS_MONTH = :smonth")
            params["smonth"] = smonth
        if SERVERPART_ID:
            conditions.append(f"A.SERVERPART_ID IN ({SERVERPART_ID})")

        where_sql = " AND ".join(conditions)
        sql = f"""SELECT 
                A.SERVERPART_NAME, A.SPREGIONTYPE_NAME, B.ACCOUNT_PCODE, B.ACCOUNT_CODE,
                B.BUDGETDETAIL_AMOUNT, B.REVENUE_AMOUNT
            FROM T_BUDGETPROJECT_AH A, T_BUDGETDETAIL_AH B
            WHERE {where_sql}"""

        rows = db.execute_query(sql, params)
        # 构建tree结构(C#返回的是node/children树)
        tree_list = []
        for r in rows:
            node = {
                "SERVERPART_NAME": r.get("SERVERPART_NAME"),
                "SPREGIONTYPE_NAME": r.get("SPREGIONTYPE_NAME"),
                "ACCOUNT_CODE": r.get("ACCOUNT_CODE") or r.get("ACCOUNT_PCODE"),
                "BUDGETDETAIL_AH_ID": r.get("BUDGETDETAIL_AH_ID"),
                "BUDGETPROJECT_AH_ID": r.get("BUDGETPROJECT_AH_ID"),
                "BUDGETDETAIL_AMOUNT": r.get("BUDGETDETAIL_AMOUNT"),
                "REVENUE_AMOUNT": r.get("REVENUE_AMOUNT"),
                "STATISTICS_MONTH": r.get("STATISTICS_MONTH"),
                "Budget_Degree": None,
                "Growth_Rate": None,
                "ShowGrowth_Rate": None,
                "ShowRevenue_Amount": None,
            }
            tree_list.append({"node": node, "children": []})
        json_list = JsonListData.create(data_list=tree_list, total=len(tree_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
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
