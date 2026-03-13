# -*- coding: utf-8 -*-
"""
CommercialApi - 节假日分析 Service
从 revenue_router.py 中抽取:
  GetHolidayCompare       — 节日营收同比对比
  GetHolidayDailyAnalysis — 节假日逐日对客分析
"""
from __future__ import annotations
from datetime import datetime as dt, timedelta
from decimal import Decimal

from core.database import DatabaseHelper
from services.commercial.service_utils import safe_float as _sf, safe_int as _si
from routers.deps import parse_multi_ids, build_in_condition


# ===== 共用辅助函数 =====

HOLIDAY_MAP = {
    1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节",
    5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节",
}


def _to_dt(v):
    """将各种日期格式转为 datetime"""
    if isinstance(v, dt):
        return v
    if isinstance(v, str):
        return dt.strptime(v[:10], "%Y-%m-%d")
    return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v


def _query_holiday_dates(db, holiday_type, cur_year, compare_year):
    """从 T_HOLIDAY 查节日日期范围，返回 (cur_dates, cmp_dates) 或 None"""
    h_name = HOLIDAY_MAP.get(int(holiday_type), "")
    if not h_name:
        return None
    cur_desc = f"{cur_year}年{h_name}"
    cmp_desc = f"{compare_year}年{h_name}"
    h_rows = db.execute_query(
        f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
        WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
    if not h_rows:
        return None
    cur_dates = [_to_dt(r["HOLIDAY_DATE"]) for r in h_rows
                 if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
    cmp_dates = [_to_dt(r["HOLIDAY_DATE"]) for r in h_rows
                 if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
    if not cur_dates or not cmp_dates:
        return None
    return cur_dates, cmp_dates


def _build_holiday_where(serverpart_id, sp_region_type_id=None):
    """构建节日查询的服务区/片区 WHERE 条件"""
    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition(
            'SERVERPART_ID', _sp_ids
        ).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    return where_sql


def _dnp(d):
    """日期格式化（月日不补零）"""
    return f"{d.year}/{d.month}/{d.day}"


# ===================================================================
# 1. GetHolidayCompare — 节日营收同比对比
# ===================================================================

def get_holiday_compare(db, province_code, cur_year, compare_year,
                        holiday_type, statistics_date,
                        serverpart_id, sp_region_type_id):
    """获取节日营收同比数据，无数据返回 None"""
    if not cur_year or not compare_year:
        return None

    result = _query_holiday_dates(db, holiday_type, cur_year, compare_year)
    if not result:
        return None
    cur_dates, cmp_dates = result

    s_date = min(cur_dates)
    e_date = max(cur_dates)
    cs_date = min(cmp_dates)
    ce_date = max(cmp_dates)

    where_sql = _build_holiday_where(serverpart_id, sp_region_type_id)

    rev_sql = """SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
        FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
            AND B."STATISTIC_TYPE" = 1000
            AND A."STATISTICS_DATE" >= {s} AND A."STATISTICS_DATE" <= {e}{w}
        GROUP BY A."STATISTICS_DATE" """

    cur_rows = db.execute_query(rev_sql.format(
        s=s_date.strftime("%Y%m%d"), e=e_date.strftime("%Y%m%d"), w=where_sql)) or []
    cmp_rows = db.execute_query(rev_sql.format(
        s=cs_date.strftime("%Y%m%d"), e=ce_date.strftime("%Y%m%d"), w=where_sql)) or []

    cur_map = {str(_si(r.get("STATISTICS_DATE"))): _sf(r.get("CASHPAY")) for r in cur_rows}
    cmp_map = {str(_si(r.get("STATISTICS_DATE"))): _sf(r.get("CASHPAY")) for r in cmp_rows}

    cur_days = (e_date - s_date).days + 1
    cmp_days = (ce_date - cs_date).days + 1
    max_d = max(cur_days, cmp_days)
    cur_acc = Decimal('0')
    cmp_acc = Decimal('0')
    cur_list = []
    cmp_list = []

    for i in range(max_d):
        cd = s_date + timedelta(days=i)
        ld = cs_date + timedelta(days=i)
        cv = cur_map.get(cd.strftime("%Y%m%d"), 0)
        lv = cmp_map.get(ld.strftime("%Y%m%d"), 0)
        cur_acc += Decimal(str(cv))
        cmp_acc += Decimal(str(lv))
        cur_list.append({"name": _dnp(cd), "value": str(cv), "data": str(cur_acc), "key": None})
        cmp_list.append({"name": _dnp(ld), "value": str(lv), "data": str(cmp_acc), "key": None})

    return {
        "curHoliday": f"{s_date.strftime('%m.%d')}-{e_date.strftime('%m.%d')}",
        "curHolidayDays": cur_days,
        "curRevenue": float(cur_acc),
        "curList": cur_list,
        "compareHoliday": f"{cs_date.strftime('%m.%d')}-{ce_date.strftime('%m.%d')}",
        "compareHolidayDays": cmp_days,
        "compareRevenue": float(cmp_acc),
        "compareList": cmp_list,
    }


# ===================================================================
# 2. GetHolidayDailyAnalysis — 节假日逐日对客分析
# ===================================================================

def get_holiday_daily_analysis(db, province_code, cur_year, compare_year,
                               holiday_type, statistics_date,
                               sp_region_type_id, serverpart_id,
                               business_type, business_trade, business_region):
    """获取节假日各类项目所有天数对客分析，返回列表"""
    result = _query_holiday_dates(db, holiday_type, cur_year, compare_year)
    if not result:
        return []
    cur_dates, cmp_dates = result

    s_date = min(cur_dates)
    e_date = max(cur_dates)
    cs_date = min(cmp_dates)

    # 统计日期截止
    stat_d = (dt.strptime(statistics_date, "%Y-%m-%d")
              if statistics_date and "-" in statistics_date
              else (dt.strptime(statistics_date, "%Y%m%d") if statistics_date else e_date))
    if stat_d > e_date:
        stat_d = e_date
    day_span = (stat_d - s_date).days
    cy_date = cs_date + timedelta(days=day_span)

    # 构建 WHERE 条件
    where_sql = ""
    use_holiday_table = False
    if sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
        use_holiday_table = True
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition(
            'SERVERPART_ID', _sp_ids
        ).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
        use_holiday_table = True
    if business_type:
        where_sql += f' AND A."BUSINESS_TYPE" IN ({business_type})'
    if business_trade:
        where_sql += f' AND A."SHOPTRADE" IN ({business_trade})'
    if business_region:
        where_sql += f' AND A."BUSINESS_REGION" IN ({business_region})'

    if use_holiday_table:
        base_sql = """SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_HOLIDAYREVENUE" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = TO_CHAR(B."SERVERPART_ID") AND A."HOLIDAYREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {s} AND {e}{w}
            GROUP BY A."STATISTICS_DATE" """
    else:
        base_sql = """SELECT A."STATISTICS_DATE", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
            FROM "T_PROVINCEREVENUE" A
            WHERE A."PROVINCEREVENUE_STATE" = 1
                AND A."STATISTICS_DATE" BETWEEN {s} AND {e}{w}
            GROUP BY A."STATISTICS_DATE" """

    cur_rows = db.execute_query(base_sql.format(
        s=s_date.strftime("%Y%m%d"), e=stat_d.strftime("%Y%m%d"), w=where_sql)) or []
    cmp_rows = db.execute_query(base_sql.format(
        s=cs_date.strftime("%Y%m%d"), e=cy_date.strftime("%Y%m%d"), w=where_sql)) or []

    def to_dec(v):
        try:
            return Decimal(str(v)) if v is not None else Decimal('0')
        except Exception:
            return Decimal('0')

    cur_map = {str(_si(r.get("STATISTICS_DATE"))): to_dec(r.get("REVENUE_AMOUNT")) for r in cur_rows}
    cmp_map = {str(_si(r.get("STATISTICS_DATE"))): to_dec(r.get("REVENUE_AMOUNT")) for r in cmp_rows}

    result_list = []
    total_cur = sum(cur_map.values())
    total_cmp = sum(cmp_map.values())
    result_list.append({"name": "累计", "value": str(total_cur), "data": str(total_cmp), "key": None, "date": None})

    for i in range(day_span + 1):
        cd = s_date + timedelta(days=i)
        ld = cs_date + timedelta(days=i)
        cd_key = cd.strftime("%Y%m%d")
        ld_key = ld.strftime("%Y%m%d")
        cv = str(cur_map[cd_key]) if cd_key in cur_map else ""
        lv = str(cmp_map[ld_key]) if ld_key in cmp_map else ""
        result_list.append({
            "name": str(i + 1), "value": cv, "data": lv,
            "key": None,
            "date": f"{_dnp(cd)},{_dnp(ld)}",
        })

    return result_list
