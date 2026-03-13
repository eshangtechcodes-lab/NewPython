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
from typing import Optional
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


def _sf(v):
    try: return float(v) if v is not None else 0.0
    except: return 0.0

def _si(v):
    try: return int(v) if v is not None else 0
    except: return 0


def _get_province_id(db: DatabaseHelper, province_code: str):
    pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
    pc_rows = db.execute_query(pc_sql, {"pc": province_code})
    return pc_rows[0]["FIELDENUM_ID"] if pc_rows else province_code


# ===== 1. GetRevenueTrend =====
def get_revenue_trend(db: DatabaseHelper, province_code, statistics_date,
                       statistics_type, serverpart_id, sp_region_type_id) -> list[dict]:
    """获取营收趋势图数据，返回结果列表"""
    import calendar
    from datetime import datetime as dt

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'

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
                date_sql = f' AND A."STATISTICS_MONTH" >= {statistics_date}01 AND A."STATISTICS_MONTH" <= {statistics_date}12'
        if valid_year:
            sql = f"""SELECT A."STATISTICS_MONTH" AS "STATISTICS",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                    SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
                FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                    AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                GROUP BY A."STATISTICS_MONTH" """
            rows = db.execute_query(sql) or []
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
            date_sql = f' AND A."STATISTICS_DATE" >= {m_start} AND A."STATISTICS_DATE" <= {m_end}'
            days_in_month = calendar.monthrange(stat_d.year, stat_d.month)[1]
        sql = f"""SELECT A."STATISTICS_DATE" AS "STATISTICS",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."REVENUEDAILY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
            GROUP BY A."STATISTICS_DATE" """
        rows = db.execute_query(sql) or []
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
                date_sql = f' AND A."STATISTICS_MONTH" >= {statistics_date}01 AND A."STATISTICS_MONTH" <= {statistics_date}12'
        if valid_year:
            sql = f"""SELECT CEIL(MOD(A."STATISTICS_MONTH", {statistics_date}00) / 3) AS "STATISTICS",
                    SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
                FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                    AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000{where_sql}{date_sql}
                GROUP BY CEIL(MOD(A."STATISTICS_MONTH", {statistics_date}00) / 3)"""
            rows = db.execute_query(sql) or []
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

    def _date_no_pad(d):
        return f"{d.year}/{d.month}/{d.day}"

    def parse_d(s):
        return dt.strptime(s, "%Y-%m-%d") if "-" in s else dt.strptime(s, "%Y%m%d")

    empty = {"data": None, "key": None, "name": None, "value": None}
    if not push_province_code or not statistics_start_date or not statistics_end_date:
        return {"curRevenue": None, "curList": [empty], "compareRevenue": None, "compareList": [empty]}

    s_date = parse_d(statistics_start_date)
    e_date = parse_d(statistics_end_date)
    cs_date = parse_d(compare_start_date) if compare_start_date else s_date.replace(year=s_date.year - 1)
    ce_date = parse_d(compare_end_date) if compare_end_date else e_date.replace(year=e_date.year - 1)

    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'

    def _query_period(sd, ed):
        sql = f"""SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTIC_TYPE" = 1000
                AND A."STATISTICS_DATE" >= {sd.strftime('%Y%m%d')}
                AND A."STATISTICS_DATE" <= {ed.strftime('%Y%m%d')}{where_sql}
            GROUP BY A."STATISTICS_DATE" """
        rows = db.execute_query(sql) or []
        return {str(int(_sf(r.get("STATISTICS_DATE")))): _sf(r.get("CASHPAY")) for r in rows}

    cur_map = _query_period(s_date, e_date)
    cmp_map = _query_period(cs_date, ce_date)

    max_days = max((e_date - s_date).days + 1, (ce_date - cs_date).days + 1)
    cur_acc = Decimal('0'); cmp_acc = Decimal('0')
    cur_list = []; cmp_list = []

    for i in range(max_days):
        cur_d = s_date + timedelta(days=i); cmp_d = cs_date + timedelta(days=i)
        cv = cur_map.get(cur_d.strftime("%Y%m%d"), 0)
        lv = cmp_map.get(cmp_d.strftime("%Y%m%d"), 0)
        cur_acc += Decimal(str(cv)); cmp_acc += Decimal(str(lv))
        cur_list.append({"name": _date_no_pad(cur_d), "value": str(cv), "data": str(cur_acc), "key": None})
        cmp_list.append({"name": _date_no_pad(cmp_d), "value": str(lv), "data": str(cmp_acc), "key": None})

    return {
        "curRevenue": float(cur_acc), "curList": cur_list,
        "compareRevenue": float(cmp_acc), "compareList": cmp_list,
        "curHoliday": None, "curHolidayDays": 0,
        "compareHoliday": None, "compareHolidayDays": 0,
    }


# ===== 4-5. GetRevenueReport / GetRevenueReportDetil =====
# 这两个路由各约 150-200 行，含复杂聚合和品牌/区域/门店嵌套逻辑
# 暂保留在 Router 层，后续重写 Router 时整体迁移


# ===== 6. GetSPRevenueRank =====
# 约 140 行，含复杂 EXISTS 子查询和排行过滤
# 暂保留在 Router 层，后续重写 Router 时整体迁移
