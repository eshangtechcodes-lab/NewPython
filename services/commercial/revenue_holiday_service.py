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


# ===================================================================
# 辅助函数：扩展版节日日期查询（支持暑期/国庆特殊逻辑）
# 从 Router _get_holiday_dates 迁移
# ===================================================================

def _get_holiday_dates_ext(db, holiday_type, cur_year, compare_year):
    """获取节日日期范围（与C# CommonHelper.GetHoliday一致）
    返回 (ss, se, cs, ce) 四元组或 None
    """
    import calendar
    cur_year = int(cur_year)
    compare_year = int(compare_year)

    # 暑期固定时间
    if holiday_type == 6:
        return (dt(cur_year, 7, 1), dt(cur_year, 8, 31),
                dt(compare_year, 7, 1), dt(compare_year, 8, 31))

    # 从T_HOLIDAY表查节日日期
    holiday_names = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节",
                     5: "端午节", 7: "中秋节", 8: "国庆节"}
    h_name = holiday_names.get(holiday_type)
    if not h_name:
        return None

    sql = f"""SELECT "HOLIDAY_DESC", MIN("HOLIDAY_DATE") AS "MIN_DATE", MAX("HOLIDAY_DATE") AS "MAX_DATE"
        FROM "T_HOLIDAY"
        WHERE "HOLIDAY_DESC" IN ('{cur_year}年{h_name}','{compare_year}年{h_name}')
        GROUP BY "HOLIDAY_DESC" """
    rows = db.execute_query(sql) or []

    ss, se, cs, ce = None, None, None, None
    for r in rows:
        desc = r.get("HOLIDAY_DESC", "")
        min_d = r.get("MIN_DATE")
        max_d = r.get("MAX_DATE")
        if min_d and not isinstance(min_d, dt):
            min_d = dt.strptime(str(min_d)[:10], "%Y-%m-%d")
        if max_d and not isinstance(max_d, dt):
            max_d = dt.strptime(str(max_d)[:10], "%Y-%m-%d")
        if desc == f"{cur_year}年{h_name}":
            ss, se = min_d, max_d
        if desc == f"{compare_year}年{h_name}":
            cs, ce = min_d, max_d

    if not ss or not cs:
        return None

    # 春运以实际时间为准
    if holiday_type == 2:
        return (ss, se, cs, ce)

    # 元旦/清明/端午/中秋: 假期开始前一天至开始后三天
    if holiday_type in (1, 3, 5, 7):
        se = ss + timedelta(days=3)
        ss = ss + timedelta(days=-1)
        ce = cs + timedelta(days=3)
        cs = cs + timedelta(days=-1)
    # 五一: 假期开始前一天至假期结束后一天
    elif holiday_type == 4:
        se = se + timedelta(days=1)
        ss = ss + timedelta(days=-1)
        ce = ce + timedelta(days=1)
        cs = cs + timedelta(days=-1)
    # 国庆: 9/29-10/8 (2023特殊 9/27-10/6)
    elif holiday_type == 8:
        if cur_year == 2023:
            ss, se = dt(cur_year, 9, 27), dt(cur_year, 10, 6)
        else:
            ss, se = dt(cur_year, 9, 29), dt(cur_year, 10, 8)
        if compare_year == 2023:
            cs, ce = dt(compare_year, 9, 27), dt(compare_year, 10, 6)
        else:
            cs, ce = dt(compare_year, 9, 29), dt(compare_year, 10, 8)

    return (ss, se, cs, ce)


def _sum_compute(rows, filter_fn, field_cur, field_total):
    """模拟C#的DataTable.Compute(SUM, filter) — 使用Decimal避免浮点精度问题"""
    filtered = [r for r in rows if filter_fn(r)]
    if not filtered:
        # C#的Compute在无匹配行时返回DBNull → ToString()是空字符串
        return "", ""
    total = sum(Decimal(str(r.get(field_total) or 0)) for r in filtered)
    cur = sum(Decimal(str(r.get(field_cur) or 0)) for r in filtered)

    def fmt(v):
        s = str(v)
        if '.' in s:
            integer, decimal = s.split('.')
            if len(decimal) < 2:
                decimal = decimal.ljust(2, '0')
            return f"{integer}.{decimal}"
        return s
    return fmt(total), fmt(cur)


# ===================================================================
# 3. GetHolidayAnalysis — 节日营收数据对比分析（完整逻辑）
# ===================================================================

def get_holiday_analysis(db, province_code, cur_year, compare_year,
                         holiday_type, statistics_date, serverpart_id):
    """获取节日营收数据对比分析，返回 dict 或 None
    从 Router get_holiday_analysis 迁移（~198行核心逻辑）
    """
    from services.commercial.service_utils import get_province_id as _get_province_id

    _ckm = lambda: {"data": None, "key": None, "name": None, "value": None}

    sd = (dt.strptime(statistics_date.split(' ')[0], '%Y-%m-%d')
          if statistics_date and '-' in statistics_date else None)
    if not sd:
        return None

    # 1. 获取节日日期范围
    dates = _get_holiday_dates_ext(db, holiday_type, cur_year, compare_year)
    if not dates:
        return None
    stat_start, stat_end, comp_start, comp_end = dates

    if sd < stat_start:
        return None
    if sd > stat_end:
        sd = stat_end

    # 计算历年对应日期
    cy_date = comp_start + (sd - stat_start)

    # 2. 构建查询条件
    fe_rows = db.execute_query(f"""SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
        WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE'
        AND B."FIELDENUM_VALUE" = '{province_code}'""") or []
    field_enum_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else province_code

    where_sql = f' AND A."PROVINCE_ID" = {field_enum_id}'
    table_name = "T_PROVINCEREVENUE"
    state_name = "PROVINCEREVENUE_STATE"

    if serverpart_id:
        table_name = "T_HOLIDAYREVENUE"
        state_name = "HOLIDAYREVENUE_STATE"
        _sp_ids = parse_multi_ids(serverpart_id)
        if _sp_ids:
            where_sql += ' AND ' + build_in_condition(
                'SERVERPART_ID', _sp_ids
            ).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
    elif province_code == "340000":
        where_sql += ' AND A."BUSINESS_REGION" = 1'

    # 3. 查询营收数据 - 当年
    ss_str = stat_start.strftime("%Y%m%d")
    sd_str = sd.strftime("%Y%m%d")
    rev_sql = f"""SELECT "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION",
            ROUND(SUM(A."REVENUE_AMOUNT"),2) AS "CASHPAY",
            ROUND(SUM(A."ACCOUNT_AMOUNTNOTAX"),2) AS "ACCOUNT_AMOUNT",
            ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {sd_str} THEN A."REVENUE_AMOUNT" ELSE 0 END),2) AS "CASHPAY_CUR",
            ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {sd_str} THEN A."ACCOUNT_AMOUNTNOTAX" ELSE 0 END),2) AS "ACCOUNT_AMOUNT_CUR"
        FROM "{table_name}" A
        WHERE A."{state_name}" = 1
            AND A."STATISTICS_DATE" BETWEEN {ss_str} AND {sd_str}{where_sql}
        GROUP BY "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION" """
    cur_rev = db.execute_query(rev_sql) or []

    # 4. 查询营收数据 - 历年
    cs_str = comp_start.strftime("%Y%m%d")
    cy_str = cy_date.strftime("%Y%m%d")
    rev_sql2 = f"""SELECT "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION",
            ROUND(SUM(A."REVENUE_AMOUNT"),2) AS "CASHPAY",
            ROUND(SUM(A."ACCOUNT_AMOUNTNOTAX"),2) AS "ACCOUNT_AMOUNT",
            ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {cy_str} THEN A."REVENUE_AMOUNT" ELSE 0 END),2) AS "CASHPAY_CUR",
            ROUND(SUM(CASE WHEN A."STATISTICS_DATE" = {cy_str} THEN A."ACCOUNT_AMOUNTNOTAX" ELSE 0 END),2) AS "ACCOUNT_AMOUNT_CUR"
        FROM "{table_name}" A
        WHERE A."{state_name}" = 1
            AND A."STATISTICS_DATE" BETWEEN {cs_str} AND {cy_str}{where_sql}
        GROUP BY "BUSINESS_TYPE","SHOPTRADE","BUSINESS_REGION" """
    cy_rev = db.execute_query(rev_sql2) or []

    # 5. 构建过滤器和辅助函数
    def mk(rows, filter_fn):
        d, v = _sum_compute(rows, filter_fn, "CASHPAY_CUR", "CASHPAY")
        return {"data": d, "key": None, "name": None, "value": v}

    def mk_acc(rows, filter_fn):
        d, v = _sum_compute(rows, filter_fn, "ACCOUNT_AMOUNT_CUR", "ACCOUNT_AMOUNT")
        return {"data": d, "key": None, "name": None, "value": v}

    all_pass = lambda r: True
    bt4000 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000"
    bt4000_st134 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) in ("1", "3", "4")
    bt4000_st13 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) in ("1", "3")
    bt4000_st4 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) == "4"
    bt4000_st3 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) == "3"
    bt4000_st2 = lambda r: str(r.get("BUSINESS_TYPE")) == "4000" and str(r.get("SHOPTRADE")) == "2"
    bt_lt4000 = lambda r: int(r.get("BUSINESS_TYPE") or 0) < 4000
    bt3000 = lambda r: str(r.get("BUSINESS_TYPE")) == "3000"
    br2 = lambda r: str(r.get("BUSINESS_REGION")) == "2"

    # 6. 构建结果模型
    _model = {
        "ServerpartId": None, "ServerpartName": None,
        "curYear": None, "compareYear": None, "HolidayType": None,
        "curDate": _dnp(sd), "cyDate": _dnp(cy_date),
        # 整体对客销售额
        "curYearRevenue": mk(cur_rev, all_pass), "lYearRevenue": mk(cy_rev, all_pass),
        # 自营对客销售额 (BUSINESS_TYPE=4000)
        "curYearSelfRevenue": mk(cur_rev, bt4000), "lYearSelfRevenue": mk(cy_rev, bt4000),
        # 自营餐饮客房及其他 (BUSINESS_TYPE=4000, SHOPTRADE in 1,3,4)
        "curYearSCRevenue": mk(cur_rev, bt4000_st134), "lYearSCRevenue": mk(cy_rev, bt4000_st134),
        "curYearSCAccount": mk_acc(cur_rev, bt4000_st134), "lYearSCAccount": mk_acc(cy_rev, bt4000_st134),
        # 自营餐饮 (BUSINESS_TYPE=4000, SHOPTRADE in 1,3)
        "curYearSRRevenue": mk(cur_rev, bt4000_st13), "lYearSRRevenue": mk(cy_rev, bt4000_st13),
        "curYearSRAccount": mk_acc(cur_rev, bt4000_st13), "lYearSRAccount": mk_acc(cy_rev, bt4000_st13),
        # 自营客房及其他 (BUSINESS_TYPE=4000, SHOPTRADE=4)
        "curYearGRORevenue": mk(cur_rev, bt4000_st4), "lYearGRORevenue": mk(cy_rev, bt4000_st4),
        "curYearGROAccount": mk_acc(cur_rev, bt4000_st4), "lYearGROAccount": mk_acc(cy_rev, bt4000_st4),
        # 加盟餐饮 (BUSINESS_TYPE=4000, SHOPTRADE=3)
        "curYearFCRevenue": mk(cur_rev, bt4000_st3),
        # 自营便利店 (BUSINESS_TYPE=4000, SHOPTRADE=2)
        "curYearCVSRevenue": mk(cur_rev, bt4000_st2), "lYearCVSRevenue": mk(cy_rev, bt4000_st2),
        "curYearCVSAccount": mk_acc(cur_rev, bt4000_st2), "lYearCVSAccount": mk_acc(cy_rev, bt4000_st2),
        # 商铺租赁 (BUSINESS_TYPE < 4000)
        "curYearCoopRevenue": mk(cur_rev, bt_lt4000), "lYearCoopRevenue": mk(cy_rev, bt_lt4000),
        "curYearCoopAccount": mk_acc(cur_rev, bt_lt4000), "lYearCoopAccount": mk_acc(cy_rev, bt_lt4000),
        # 自营提成 (BUSINESS_TYPE=3000)
        "curYearSelfCoopRevenue": mk(cur_rev, bt3000),
        # 城市店 (BUSINESS_REGION=2)
        "curYearWJRevenue": mk(cur_rev, br2), "lYearWJRevenue": mk(cy_rev, br2),
    }

    # 7. 计算自营收入 = 便利店收入 + 餐饮客房收入
    def add_kv(a, b):
        av = Decimal(a.get("value") or "0")
        bv = Decimal(b.get("value") or "0")
        ad = Decimal(a.get("data") or "0")
        bd = Decimal(b.get("data") or "0")
        return {"data": str(ad + bd), "key": None, "name": None, "value": str(av + bv)}

    _model["curYearSelfAccount"] = add_kv(_model["curYearCVSAccount"], _model["curYearSCAccount"])
    _model["lYearSelfAccount"] = add_kv(_model["lYearCVSAccount"], _model["lYearSCAccount"])
    # 驿达入账 = 自营收入 + 商铺租赁收入
    _model["curYearAccount"] = add_kv(_model["curYearSelfAccount"], _model["curYearCoopAccount"])
    _model["lYearAccount"] = add_kv(_model["lYearSelfAccount"], _model["lYearCoopAccount"])

    # 8. 查询车流量
    if serverpart_id:
        _sp_ids2 = parse_multi_ids(serverpart_id)
        if _sp_ids2:
            bw_sql = ' AND ' + build_in_condition(
                'SERVERPART_ID', _sp_ids2
            ).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
        else:
            bw_sql = f""" AND EXISTS (SELECT 1 FROM "T_SERVERPART" S
                WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {field_enum_id})"""
    else:
        bw_sql = f""" AND EXISTS (SELECT 1 FROM "T_SERVERPART" S
            WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {field_enum_id})"""

    bayonet_sql = f"""SELECT SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW",
            SUM(CASE WHEN A."STATISTICS_DATE" = {sd_str} THEN A."SERVERPART_FLOW" ELSE 0 END) AS "SERVERPART_FLOW_CUR"
        FROM "T_SECTIONFLOW" A
        WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
            AND A."STATISTICS_DATE" BETWEEN {ss_str} AND {sd_str}{bw_sql}"""
    cur_bay = db.execute_query(bayonet_sql) or []

    bayonet_sql2 = f"""SELECT SUM(A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW",
            SUM(CASE WHEN A."STATISTICS_DATE" = {cy_str} THEN A."SERVERPART_FLOW" +
                NVL(A."SERVERPART_FLOW_ANALOG",0) ELSE 0 END) AS "SERVERPART_FLOW_CUR"
        FROM "T_SECTIONFLOW" A
        WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
            AND A."STATISTICS_DATE" BETWEEN {cs_str} AND {cy_str}{bw_sql}"""
    cy_bay = db.execute_query(bayonet_sql2) or []

    def bay_kv(rows):
        if not rows or not rows[0]:
            return _ckm()
        r = rows[0]
        flow = r.get("SERVERPART_FLOW")
        flow_cur = r.get("SERVERPART_FLOW_CUR")
        return {"data": str(int(float(flow))) if flow is not None else None,
                "key": None, "name": None,
                "value": str(int(float(flow_cur))) if flow_cur is not None else None}

    _model["curYearBayonet"] = bay_kv(cur_bay)
    _model["lYearBayonet"] = bay_kv(cy_bay)

    return _model
