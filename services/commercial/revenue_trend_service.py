# -*- coding: utf-8 -*-
"""
CommercialApi - 营收趋势/报表/排行/同比 Service
从 revenue_router.py 中抽取:
  GetRevenueTrend, GetRevenueReport, GetRevenueReportDetil,
  GetSalableCommodity, GetSPRevenueRank, GetRevenueYOY
每个函数独立、可单独迁移

注意: GetRevenueReport/GetRevenueReportDetil 逻辑复杂（各 150+ 行）,
      暂保留在 Router 层; 此处抽取较简洁的趋势/畅销/排行/同比
"""
from __future__ import annotations
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition
from services.commercial.service_utils import (
    date_no_pad,
    safe_float as _sf,
)


# ===== 1. GetRevenueTrend =====
def get_revenue_trend(db: DatabaseHelper, province_code, statistics_date,
                       statistics_type, serverpart_id, sp_region_type_id) -> list[dict]:
    """获取营收趋势图数据，返回结果列表"""
    import calendar
    from datetime import datetime as dt

    # --- SQL 参数化: 服务区/片区 WHERE 条件 ---
    where_sql = ""
    trend_params = {}
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        # f-string: 安全 — build_in_condition 已通过 int() 转换
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += ' AND B."SPREGIONTYPE_ID" = :srt_id'
        trend_params["srt_id"] = sp_region_type_id

    result_list = []
    if statistics_type == 1:
        # 月度
        date_sql = ""
        valid_year = True
        if statistics_date:
            sd_clean = statistics_date.replace("-", "").replace("/", "")
            if not sd_clean.isdigit() or len(statistics_date) > 4:
                valid_year = False
            else:
                # --- SQL 参数化: 年份范围条件 ---
                date_sql = ' AND A."STATISTICS_MONTH" >= :m_start AND A."STATISTICS_MONTH" <= :m_end'
                trend_params["m_start"] = f"{statistics_date}01"
                trend_params["m_end"] = f"{statistics_date}12"
        if valid_year:
            sql = f"""SELECT A."STATISTICS_MONTH" AS "STATISTICS",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                    SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
                FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                    AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                GROUP BY A."STATISTICS_MONTH" """
            rows = db.execute_query(sql, trend_params if trend_params else None) or []
            stat_map = {int(r.get("STATISTICS", 0)) % 100: r for r in rows}
            for m in range(1, 13):
                r = stat_map.get(m)
                result_list.append({"name": f"{m}月", "value": str(_sf(r.get("REVENUE_AMOUNT"))) if r else "0"})

    elif statistics_type == 2:
        # 日度
        date_sql = ""
        days_in_month = 31
        if statistics_date:
            stat_d = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
            m_start = stat_d.strftime("%Y%m01"); m_end = stat_d.strftime("%Y%m%d")
            # --- SQL 参数化: 日度日期范围 ---
            date_sql = ' AND A."STATISTICS_DATE" >= :d_start AND A."STATISTICS_DATE" <= :d_end'
            trend_params["d_start"] = m_start
            trend_params["d_end"] = m_end
            days_in_month = calendar.monthrange(stat_d.year, stat_d.month)[1]
        sql = f"""SELECT A."STATISTICS_DATE" AS "STATISTICS",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."REVENUEDAILY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
            GROUP BY A."STATISTICS_DATE" """
        rows = db.execute_query(sql, trend_params if trend_params else None) or []
        stat_map = {str(int(r.get("STATISTICS", 0))): r for r in rows}
        for d in range(1, days_in_month + 1):
            key = f"{stat_d.strftime('%Y%m')}{d:02d}" if statistics_date else str(d)
            r = stat_map.get(key)
            result_list.append({"name": str(d), "value": str(_sf(r.get("REVENUE_AMOUNT"))) if r else "0"})

    elif statistics_type == 4:
        # 季度
        date_sql = ""
        valid_year = True
        if statistics_date:
            sd_clean = statistics_date.replace("-", "").replace("/", "")
            if not sd_clean.isdigit() or len(statistics_date) > 4:
                valid_year = False
            else:
                # --- SQL 参数化: 季度年份范围 ---
                date_sql = ' AND A."STATISTICS_MONTH" >= :m_start AND A."STATISTICS_MONTH" <= :m_end'
                trend_params["m_start"] = f"{statistics_date}01"
                trend_params["m_end"] = f"{statistics_date}12"
        if valid_year:
            # f-string: 安全 — statistics_date 已验证为纯数字年份，用于 MOD 算术计算
            year_base = f"{statistics_date}00"
            sql = f"""SELECT CEIL(MOD(A."STATISTICS_MONTH", {year_base}) / 3) AS "STATISTICS",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                    AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                GROUP BY CEIL(MOD(A."STATISTICS_MONTH", {year_base}) / 3)"""
            rows = db.execute_query(sql, trend_params if trend_params else None) or []
            stat_map = {str(int(_sf(r.get("STATISTICS")))): r for r in rows}
            for q in range(1, 5):
                r = stat_map.get(str(q))
                result_list.append({"name": f"第{q}季度", "value": str(_sf(r.get("REVENUE_AMOUNT"))) if r else "0"})

    return result_list


# ===== 2. GetSalableCommodity =====
def get_salable_commodity() -> dict:
    """获取商超畅销商品 — C# 接口返回固定数据"""
    return {
        "SalableCommodity": 24.7,
        "SalableCommodityList": [
            {"Commodity_name": "红牛", "Proportion": 9.3},
            {"Commodity_name": "农夫山泉", "Proportion": 5.3},
            {"Commodity_name": "康师傅牛肉面", "Proportion": 4.5},
            {"Commodity_name": "面条", "Proportion": 3.3},
            {"Commodity_name": "其他", "Proportion": 2.3},
        ],
        "UnSalableCommodity": 10.6,
        "UnSalableCommodityList": [
            {"Commodity_name": "水杯", "Proportion": 0.13},
            {"Commodity_name": "吸油纸", "Proportion": 0.06},
            {"Commodity_name": "女儿红", "Proportion": 0.05},
            {"Commodity_name": "消毒纸巾", "Proportion": 0.02},
            {"Commodity_name": "其他", "Proportion": 0.15},
        ],
    }


# ===== 3. GetRevenueYOY =====
def get_revenue_yoy(db: DatabaseHelper, push_province_code, statistics_start_date,
                     statistics_end_date, compare_start_date, compare_end_date,
                     serverpart_id, sp_region_type_id) -> dict:
    """获取每日营收同比数据"""
    from datetime import datetime as dt, timedelta
    from decimal import Decimal
    # TODO: 函数体较长(~55行)，已迁移到 Router 层直接调用
    # 暂保留函数签名，后续完整迁移
    pass

# ===== 4-5. GetRevenueReport / GetRevenueReportDetil =====
# 这两个路由各约 150-200 行，含复杂聚合和品牌/区域/门店嵌套逻辑
# 暂保留在 Router 层，后续重写 Router 时整体迁移


# ===== 6. GetSPRevenueRank =====
# 约 140 行，含复杂 EXISTS 子查询和排行过滤
# 暂保留在 Router 层，后续重写 Router 时整体迁移
