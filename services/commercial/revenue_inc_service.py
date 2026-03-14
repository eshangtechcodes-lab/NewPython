# -*- coding: utf-8 -*-
"""
CommercialApi - 增幅分析 Service
从 revenue_router.py 中抽取:
  GetServerpartINCAnalysis — 服务区营收增幅分析
  GetShopINCAnalysis       — 门店营收增幅分析
"""
from __future__ import annotations
from datetime import datetime as dt, timedelta

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import parse_multi_ids, build_in_condition
from services.commercial.service_utils import date_no_pad


# ===================================================================
# 1. GetServerpartINCAnalysis — 服务区营收增幅分析
# ===================================================================

def get_serverpart_inc_analysis(db, calc_type, province_code, cur_year,
                                holiday_type, statistics_date, compare_year,
                                cur_start_date, statistics_start_date, statistics_end_date,
                                serverpart_id, sp_region_type_id, business_region,
                                sort_str, is_yoy_compare, date_no_pad_fn):
    """获取服务区营收增幅分析，返回 (result_list, holiday_period) 或抛出异常"""
    from datetime import datetime as dt, timedelta

    # 参数别名映射（函数签名 snake_case → 函数体 PascalCase）
    calcType = calc_type
    pushProvinceCode = province_code
    curYear = cur_year or dt.now().year
    HolidayType = holiday_type
    StatisticsDate = statistics_date
    compareYear = compare_year
    CurStartDate = cur_start_date
    ServerpartId = serverpart_id
    IsYOYCompare = is_yoy_compare
    businessRegion = business_region
    SortStr = sort_str

    # 节日枚举
    holiday_names = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}

    if not StatisticsDate:
        StatisticsDate = dt.now().strftime("%Y-%m-%d")
    if compareYear is None:
        compareYear = (curYear or dt.now().year) - 1

    # 1. GetHoliday: 获取节假日起止日期
    stats_start = None
    stats_end = None
    compare_start = None
    compare_end = None

    if HolidayType == 6:  # 暑期固定
        stats_start = dt(curYear, 7, 1)
        stats_end = dt(curYear, 8, 31)
        compare_start = dt(compareYear, 7, 1)
        compare_end = dt(compareYear, 8, 31)
    elif HolidayType == 0:  # 日常
        if CurStartDate:
            stats_start = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y/%m/%d")
        else:
            stats_start = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
        stats_end = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
        compare_start = stats_start.replace(year=stats_start.year - 1)
        compare_end = stats_end.replace(year=stats_end.year - 1)
    else:  # 其他节日从T_HOLIDAY查
        h_name = holiday_names.get(HolidayType, "")
        cur_desc = f"{curYear}年{h_name}"
        cmp_desc = f"{compareYear}年{h_name}"
        h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""")
        if not h_rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        cur_dates = [r["HOLIDAY_DATE"] for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
        cmp_dates = [r["HOLIDAY_DATE"] for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
        if not cur_dates or not cmp_dates:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        def to_dt(v):
            if isinstance(v, dt): return v
            if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
            return dt(v.year, v.month, v.day) if hasattr(v, 'year') else v

        stats_start = to_dt(min(cur_dates))
        stats_end = to_dt(max(cur_dates))
        compare_start = to_dt(min(cmp_dates))
        compare_end = to_dt(max(cmp_dates))

        # 按节日类型调整日期范围
        if HolidayType in (1, 3, 5, 7):  # 元旦/清明/端午/中秋: 前1天到后3天
            stats_end = stats_start + timedelta(days=3)
            stats_start = stats_start - timedelta(days=1)
            compare_end = compare_start + timedelta(days=3)
            compare_start = compare_start - timedelta(days=1)
        elif HolidayType == 4:  # 五一: 前1天到后1天
            stats_end = stats_end + timedelta(days=1)
            stats_start = stats_start - timedelta(days=1)
            compare_end = compare_end + timedelta(days=1)
            compare_start = compare_start - timedelta(days=1)
        elif HolidayType == 8:  # 国庆
            if curYear == 2023:
                stats_start = dt(curYear, 9, 27); stats_end = dt(curYear, 10, 6)
            else:
                stats_start = dt(curYear, 9, 29); stats_end = dt(curYear, 10, 8)
            if compareYear == 2023:
                compare_start = dt(compareYear, 9, 27); compare_end = dt(compareYear, 10, 6)
            else:
                compare_start = dt(compareYear, 9, 29); compare_end = dt(compareYear, 10, 8)

    stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d") if "-" in StatisticsDate else dt.strptime(StatisticsDate, "%Y/%m/%d")
    if stat_date < stats_start:
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    if stat_date > stats_end:
        stat_date = stats_end

    if CurStartDate and HolidayType != 0:
        cur_start_dt = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y/%m/%d")
        if cur_start_dt > stats_start:
            compare_start = compare_start + timedelta(days=(cur_start_dt - stats_start).days + 1)
            stats_start = cur_start_dt

    if HolidayType != 0 and IsYOYCompare and stat_date < stats_end:
        compare_end = compare_start + timedelta(days=(stat_date - stats_start).days)

    # 2. 查省份ID
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": pushProvinceCode})
    if not fe_rows:
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    province_id = fe_rows[0]["FIELDENUM_ID"]

    # 3. 查营收(T_HOLIDAYREVENUE)
    where_rev = f' AND A."PROVINCE_ID" = {province_id}'
    if ServerpartId:
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            where_rev += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

    cur_start_str = (stat_date if calcType == 1 else stats_start).strftime("%Y%m%d")
    cur_end_str = stat_date.strftime("%Y%m%d")
    sql_cur_rev = f"""SELECT A."SERVERPART_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT"
        FROM "T_HOLIDAYREVENUE" A
        WHERE A."HOLIDAYREVENUE_STATE" = 1 AND A."STATISTICS_DATE" BETWEEN {cur_start_str} AND {cur_end_str}{where_rev}
        GROUP BY A."SERVERPART_ID" """
    dt_cur_rev = db.execute_query(sql_cur_rev) or []

    cy_date = compare_start + timedelta(days=(stat_date - stats_start).days)
    cy_start_str = (cy_date if calcType == 1 else compare_start).strftime("%Y%m%d")
    cy_end_str = cy_date.strftime("%Y%m%d")
    sql_cy_rev = f"""SELECT A."SERVERPART_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT"
        FROM "T_HOLIDAYREVENUE" A
        WHERE A."HOLIDAYREVENUE_STATE" = 1 AND A."STATISTICS_DATE" BETWEEN {cy_start_str} AND {cy_end_str}{where_rev}
        GROUP BY A."SERVERPART_ID" """
    dt_cy_rev = db.execute_query(sql_cy_rev) or []

    # 4. 查车流(T_SECTIONFLOW)
    where_bay = ""
    if ServerpartId:
        _sp_ids3 = parse_multi_ids(ServerpartId)
        if _sp_ids3:
            where_bay = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids3).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
        else:
            where_bay = f''' AND EXISTS (SELECT 1 FROM "T_SERVERPART" S WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {province_id})'''
    else:
        where_bay = f''' AND EXISTS (SELECT 1 FROM "T_SERVERPART" S WHERE A."SERVERPART_ID" = S."SERVERPART_ID" AND S."PROVINCE_CODE" = {province_id})'''

    bay_cur_start = stat_date.strftime("%Y%m%d") if calcType == 1 else stats_start.strftime("%Y%m%d")
    sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW",
            SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
        FROM "T_SECTIONFLOW" A
        WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
            AND A."STATISTICS_DATE" BETWEEN {bay_cur_start} AND {stat_date.strftime("%Y%m%d")}{where_bay}
        GROUP BY A."SERVERPART_ID" """
    dt_cur_bay = db.execute_query(sql_cur_bay) or []

    bay_cy_start = cy_date.strftime("%Y%m%d") if calcType == 1 else compare_start.strftime("%Y%m%d")
    sql_cy_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW" + NVL(A."SERVERPART_FLOW_ANALOG",0)) AS "SERVERPART_FLOW",
            SUM(A."SECTIONFLOW_NUM") AS "SECTIONFLOW_NUM"
        FROM "T_SECTIONFLOW" A
        WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
            AND A."STATISTICS_DATE" BETWEEN {bay_cy_start} AND {cy_date.strftime("%Y%m%d")}{where_bay}
        GROUP BY A."SERVERPART_ID" """
    dt_cy_bay = db.execute_query(sql_cy_bay) or []

    # 5. 查服务区列表
    where_sp = f' AND "PROVINCE_CODE" = {province_id}'
    if ServerpartId:
        _sp_ids4 = parse_multi_ids(ServerpartId)
        if _sp_ids4:
            where_sp += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids4)
    if businessRegion == 1:
        where_sp += ' AND "SPREGIONTYPE_ID" NOT IN (89)'  # 排除城市店及商城（SPREGIONTYPE_ID=89），保留皖中管理中心（72）等
    sp_rows = db.execute_query(f"""SELECT * FROM "T_SERVERPART"
        WHERE "SPREGIONTYPE_ID" IS NOT NULL AND "STATISTICS_TYPE" = 1000 AND "STATISTIC_TYPE" = 1000{where_sp}
        ORDER BY "SPREGIONTYPE_INDEX","SPREGIONTYPE_ID","SERVERPART_INDEX","SERVERPART_CODE" """) or []

    # 营收/车流 按服务区ID索引
    def build_map(rows, key="SERVERPART_ID"):
        m = {}
        for r in rows:
            sid = str(r.get(key, ""))
            if sid not in m:
                m[sid] = r
            else:
                for k2, v2 in r.items():
                    if k2 != key:
                        try: m[sid][k2] = (m[sid].get(k2) or 0) + (v2 or 0)
                        except: pass
        return m

    cur_rev_map = build_map(dt_cur_rev)
    cy_rev_map = build_map(dt_cy_rev)
    cur_bay_map = build_map(dt_cur_bay)
    cy_bay_map = build_map(dt_cy_bay)

    def safe_f(v):
        try: return float(v) if v is not None else 0.0
        except: return 0.0

    def make_inc(cur, ly):
        inc = {"curYearData": cur, "lYearData": ly, "increaseData": None, "increaseRate": None,
               "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}
        if cur and ly and cur != 0 and ly != 0:
            inc["increaseData"] = round(cur - ly, 2)
            inc["increaseRate"] = round((cur - ly) / ly * 100, 2)
        return inc

    # 6. 构建结果
    result_list = []
    no_increase_list = []
    for sp in sp_rows:
        sp_id = str(sp["SERVERPART_ID"])
        cur_r = cur_rev_map.get(sp_id, {})
        cy_r = cy_rev_map.get(sp_id, {})
        cur_b = cur_bay_map.get(sp_id, {})
        cy_b = cy_bay_map.get(sp_id, {})

        def safe_or_none(d, key):
            """有数据返回float，无数据返回None
            注意：当 d 非空（即该服务区在SQL查询中有记录）但字段值为NULL时，
            C# 的 Convert.ToDecimal(DBNull) 返回 0，这里也需对齐返回 0.0
            """
            if not d:
                return None
            v = d.get(key)
            if v is None:
                # 字典存在说明有记录行，字段NULL视为0（对齐C#口径）
                return 0.0
            try:
                return float(v)
            except:
                return 0.0

        rev_inc = make_inc(safe_or_none(cur_r, "REVENUE_AMOUNT"), safe_or_none(cy_r, "REVENUE_AMOUNT"))
        acc_inc = make_inc(safe_or_none(cur_r, "ACCOUNT_AMOUNT"), safe_or_none(cy_r, "ACCOUNT_AMOUNT"))
        bay_inc = make_inc(safe_or_none(cur_b, "SERVERPART_FLOW"), safe_or_none(cy_b, "SERVERPART_FLOW"))
        sec_inc = make_inc(safe_or_none(cur_b, "SECTIONFLOW_NUM"), safe_or_none(cy_b, "SECTIONFLOW_NUM"))

        # 车流增长率>1000没有可比性
        if bay_inc["increaseRate"] and abs(bay_inc["increaseRate"]) > 1000:
            bay_inc["increaseData"] = None; bay_inc["increaseRate"] = None
        if sec_inc["increaseRate"] and abs(sec_inc["increaseRate"]) > 1000:
            sec_inc["increaseData"] = None; sec_inc["increaseRate"] = None
        # 历年车流<100不计算增长率
        if bay_inc.get("lYearData") and bay_inc["lYearData"] <= 100:
            bay_inc["increaseRate"] = None

        item = {
            "SPRegionTypeId": sp.get("SPREGIONTYPE_ID"),
            "SPRegionTypeName": sp.get("SPREGIONTYPE_NAME"),
            "ServerpartId": sp.get("SERVERPART_ID"),
            "ServerpartName": sp.get("SERVERPART_NAME"),
            "RevenueINC": rev_inc,
            "AccountINC": acc_inc,
            "BayonetINC": bay_inc,
            "SectionFlowINC": sec_inc,
            "AvgTicketINC": None,
            "TicketINC": None,
            "BayonetINC_ORI": None,
            "ShopINCList": None,
            "RankDiff": None,
            "Cost_Amount": None,
            "Ca_Cost": None,
            "Profit_Amount": None,
        }

        # 排序相关过滤
        is_no_increase = True
        if SortStr:
            ss = SortStr.lower()
            if "revenue" in ss and not (rev_inc["increaseRate"] is not None):
                is_no_increase = False
            if "account" in ss and not (acc_inc["increaseRate"] is not None):
                is_no_increase = False
            if "bayonet" in ss and not (bay_inc["increaseRate"] is not None):
                is_no_increase = False

        if is_no_increase:
            result_list.append(item)
        else:
            no_increase_list.append(item)

    # 排序
    if SortStr:
        ss = SortStr.lower().replace(" asc", "")
        rev = "desc" in SortStr.lower()
        if "revenue" in ss and "bayonet" not in ss:
            result_list.sort(key=lambda x: x["RevenueINC"]["increaseRate"] or 0, reverse=rev)
        elif "bayonet" in ss and "revenue" not in ss:
            result_list.sort(key=lambda x: x["BayonetINC"]["increaseRate"] or 0, reverse=rev)
        elif "account" in ss:
            result_list.sort(key=lambda x: x["AccountINC"]["increaseRate"] or 0, reverse=rev)

    result_list.extend(no_increase_list)

    if not result_list:
        return Result.fail(code=101, msg="查询失败，无数据返回！")

    h_name = holiday_names.get(HolidayType, "")
    holiday_period = f"{curYear}年{h_name}时间为{date_no_pad(stats_start)} 0:00:00至{stat_date.strftime('%Y-%m-%d')}\r\n{compareYear}年{h_name}时间为{date_no_pad(compare_start)} 0:00:00至{date_no_pad(compare_end)} 0:00:00"

    json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_size=10)
    resp = json_list.model_dump()
    resp["OtherData"] = holiday_period
    return Result.success(data=resp, msg="查询成功")


# ===================================================================
# 2. GetShopINCAnalysis — 门店营收增幅分析
# ===================================================================

def get_shop_inc_analysis(db, calc_type, province_code, cur_year, compare_year,
                          holiday_type, serverpart_id, statistics_date,
                          cur_start_date, sort_str):
    """获取门店营收增幅分析，返回 result_list 或抛出异常"""
    from datetime import datetime as dt, timedelta

    # 参数别名映射（函数签名 snake_case → 函数体 PascalCase）
    calcType = calc_type
    curYear = cur_year or dt.now().year
    compareYear = compare_year
    HolidayType = holiday_type
    ServerpartId = serverpart_id
    StatisticsDate = statistics_date
    CurStartDate = cur_start_date
    SortStr = sort_str

    def safe_dec(v):
        try: return float(v) if v is not None else 0.0
        except: return 0.0

    # 默认统计日期
    if not StatisticsDate:
        StatisticsDate = dt.now().strftime("%Y-%m-%d")

    # 解析统计日期
    if "-" in StatisticsDate:
        stat_date = dt.strptime(StatisticsDate, "%Y-%m-%d")
    else:
        stat_date = dt.strptime(StatisticsDate, "%Y%m%d")

    # ========== 1. 获取节日日期范围 (对齐 CommonHelper.GetHoliday) ==========
    holiday_map = {1: "元旦", 2: "春运", 3: "清明节", 4: "劳动节", 5: "端午节", 6: "暑期", 7: "中秋节", 8: "国庆节"}
    h_name = holiday_map.get(HolidayType, "")

    if HolidayType == 6:
        # 暑期固定
        statistics_start = dt(curYear, 7, 1)
        statistics_end = dt(curYear, 8, 31)
        compare_start = dt(compareYear, 7, 1)
        compare_end = dt(compareYear, 8, 31)
    elif HolidayType == 0:
        # 自定义日期范围
        if not CurStartDate:
            CurStartDate = StatisticsDate
        statistics_start = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y%m%d")
        statistics_end = stat_date
        compare_start = statistics_start.replace(year=statistics_start.year - 1)
        compare_end = statistics_end.replace(year=statistics_end.year - 1)
    else:
        # 从 T_HOLIDAY 表查询节日日期
        cur_desc = f"{curYear}年{h_name}"
        cmp_desc = f"{compareYear}年{h_name}"
        h_rows = db.execute_query(f"""SELECT "HOLIDAY_DATE","HOLIDAY_DESC" FROM "T_HOLIDAY"
            WHERE "HOLIDAY_DESC" IN ('{cur_desc}','{cmp_desc}')""") or []
        if not h_rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        def to_dt(v):
            if isinstance(v, dt): return v
            if hasattr(v, 'year'): return dt(v.year, v.month, v.day)
            if isinstance(v, str): return dt.strptime(v[:10], "%Y-%m-%d")
            return v

        cur_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cur_desc and r.get("HOLIDAY_DATE")]
        cmp_dates = [to_dt(r["HOLIDAY_DATE"]) for r in h_rows if r.get("HOLIDAY_DESC") == cmp_desc and r.get("HOLIDAY_DATE")]
        if not cur_dates or not cmp_dates:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        statistics_start = min(cur_dates)
        statistics_end = max(cur_dates)
        compare_start = min(cmp_dates)
        compare_end = max(cmp_dates)

        # 按节日类型调整日期范围 (对齐 C# switch)
        if HolidayType in (1, 3, 5, 7):
            # 元旦/清明/端午/中秋：开始前1天到开始后3天
            statistics_end = statistics_start + timedelta(days=3)
            statistics_start = statistics_start - timedelta(days=1)
            compare_end = compare_start + timedelta(days=3)
            compare_start = compare_start - timedelta(days=1)
        elif HolidayType == 4:
            # 五一：开始前1天到结束后1天
            statistics_end = statistics_end + timedelta(days=1)
            statistics_start = statistics_start - timedelta(days=1)
            compare_end = compare_end + timedelta(days=1)
            compare_start = compare_start - timedelta(days=1)
        elif HolidayType == 8:
            # 国庆
            if curYear == 2023:
                statistics_start = dt(curYear, 9, 27)
                statistics_end = dt(curYear, 10, 6)
            else:
                statistics_start = dt(curYear, 9, 29)
                statistics_end = dt(curYear, 10, 8)
            if compareYear == 2023:
                compare_start = dt(compareYear, 9, 27)
                compare_end = dt(compareYear, 10, 6)
            else:
                compare_start = dt(compareYear, 9, 29)
                compare_end = dt(compareYear, 10, 8)
        # HolidayType == 2 (春运): 使用原始日期不调整

    # 验证统计日期范围
    if stat_date < statistics_start:
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    elif stat_date > statistics_end:
        stat_date = statistics_end

    # 处理 CurStartDate 与节日开始日期的偏移
    if CurStartDate:
        cur_start_dt = dt.strptime(CurStartDate, "%Y-%m-%d") if "-" in CurStartDate else dt.strptime(CurStartDate, "%Y%m%d")
        if cur_start_dt > statistics_start:
            offset_days = (cur_start_dt - statistics_start).days
            compare_start = compare_start + timedelta(days=offset_days)
            statistics_start = cur_start_dt

    # ========== 2. 查询节日营收 (T_HOLIDAYREVENUE) ==========
    where_rev = f' AND A."SERVERPART_ID" = \'{ServerpartId}\''

    # 本年营收
    if calcType == 1:
        # 当日
        cur_rev_start = stat_date.strftime("%Y%m%d")
    else:
        cur_rev_start = statistics_start.strftime("%Y%m%d")
    cur_rev_end = stat_date.strftime("%Y%m%d")

    sql_cur_rev = f"""SELECT A."SERVERPARTSHOP_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
        FROM "T_HOLIDAYREVENUE" A
        WHERE A."HOLIDAYREVENUE_STATE" = 1
            AND A."STATISTICS_DATE" BETWEEN {cur_rev_start} AND {cur_rev_end}{where_rev}
        GROUP BY A."SERVERPARTSHOP_ID" """
    dt_cur_rev = db.execute_query(sql_cur_rev) or []

    # 历年营收
    day_span = (stat_date - statistics_start).days
    cy_date = compare_start + timedelta(days=day_span)
    if calcType == 1:
        cmp_rev_start = cy_date.strftime("%Y%m%d")
    else:
        cmp_rev_start = compare_start.strftime("%Y%m%d")
    cmp_rev_end = cy_date.strftime("%Y%m%d")

    sql_cmp_rev = f"""SELECT A."SERVERPARTSHOP_ID", SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
        FROM "T_HOLIDAYREVENUE" A
        WHERE A."HOLIDAYREVENUE_STATE" = 1
            AND A."STATISTICS_DATE" BETWEEN {cmp_rev_start} AND {cmp_rev_end}{where_rev}
        GROUP BY A."SERVERPARTSHOP_ID" """
    dt_cmp_rev = db.execute_query(sql_cmp_rev) or []

    # ========== 关键判断：本年和历年营收都为空则返回 null/101 ==========
    if not dt_cur_rev and not dt_cmp_rev:
        return Result.fail(code=101, msg="查询失败，无数据返回！")

    # 构建查找映射
    cur_rev_map = {}
    for r in dt_cur_rev:
        sid = str(r.get("SERVERPARTSHOP_ID", ""))
        cur_rev_map[sid] = safe_dec(r.get("REVENUE_AMOUNT"))
    cmp_rev_map = {}
    for r in dt_cmp_rev:
        sid = str(r.get("SERVERPARTSHOP_ID", ""))
        cmp_rev_map[sid] = safe_dec(r.get("REVENUE_AMOUNT"))

    # ========== 3. 查询车流 (T_SECTIONFLOW / T_BAYONETDAILY_AH) ==========
    where_bay = f' AND A."SERVERPART_ID" = {ServerpartId}'

    # 本年车流
    if calcType == 1:
        sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {stat_date.strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
            GROUP BY A."SERVERPART_ID" """
    elif stat_date.year == 2024 and stat_date > dt(2024, 1, 28) and HolidayType == 2:
        sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {(statistics_start + timedelta(days=3)).strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
            GROUP BY A."SERVERPART_ID" """
    else:
        # 默认使用 T_BAYONETDAILY_AH
        sql_cur_bay = f"""SELECT A."SERVERPART_ID", SUM(A."VEHICLE_COUNT") AS "SERVERPART_FLOW"
            FROM "T_BAYONETDAILY_AH" A
            WHERE A."INOUT_TYPE" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {statistics_start.strftime('%Y%m%d')} AND {stat_date.strftime('%Y%m%d')}{where_bay}
            GROUP BY A."SERVERPART_ID" """
    dt_cur_bay = db.execute_query(sql_cur_bay) or []

    # 历年车流
    if calcType == 1:
        sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {cy_date.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
            GROUP BY A."SERVERPART_ID" """
    elif stat_date.year == 2024 and stat_date > dt(2024, 1, 28) and HolidayType == 2:
        sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {(compare_start + timedelta(days=3)).strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
            GROUP BY A."SERVERPART_ID" """
    else:
        sql_cmp_bay = f"""SELECT A."SERVERPART_ID", SUM(A."SERVERPART_FLOW") AS "SERVERPART_FLOW"
            FROM "T_SECTIONFLOW" A
            WHERE A."SECTIONFLOW_STATUS" = 1 AND A."SERVERPART_ID" > 0
                AND A."STATISTICS_DATE" BETWEEN {compare_start.strftime('%Y%m%d')} AND {cy_date.strftime('%Y%m%d')}{where_bay}
            GROUP BY A."SERVERPART_ID" """
    dt_cmp_bay = db.execute_query(sql_cmp_bay) or []

    # ========== 4. 查服务区基本信息 ==========
    sp_info = db.execute_query(f"""SELECT "SERVERPART_ID","SERVERPART_NAME","SPREGIONTYPE_ID","SPREGIONTYPE_NAME"
        FROM "T_SERVERPART" WHERE "SERVERPART_ID" = {ServerpartId}""") or []
    sp_name = sp_info[0].get("SERVERPART_NAME", "") if sp_info else ""
    sp_region_id = sp_info[0].get("SPREGIONTYPE_ID") if sp_info else None
    sp_region_name = sp_info[0].get("SPREGIONTYPE_NAME", "") if sp_info else ""

    # ========== 5. 构建服务区级增幅模型 ==========
    def calc_inc(cur_val, cmp_val):
        """计算增长值和增长率"""
        result = {"curYearData": cur_val, "lYearData": cmp_val,
                  "increaseData": None, "increaseRate": None}
        if cur_val and cmp_val and cur_val != 0 and cmp_val != 0:
            inc = cur_val - cmp_val
            rate = round(inc / cmp_val * 100, 2)
            result["increaseData"] = round(inc, 2)
            result["increaseRate"] = rate
        return result

    # 服务区级营收汇总
    total_cur_rev = sum(cur_rev_map.values())
    total_cmp_rev = sum(cmp_rev_map.values())
    # 车流汇总
    total_cur_bay = sum(safe_dec(r.get("SERVERPART_FLOW")) for r in dt_cur_bay)
    total_cmp_bay = sum(safe_dec(r.get("SERVERPART_FLOW")) for r in dt_cmp_bay)

    revenue_inc = calc_inc(total_cur_rev, total_cmp_rev)
    bayonet_inc = calc_inc(total_cur_bay, total_cmp_bay)
    # 车流增长率超过1000没有可比性
    if bayonet_inc.get("increaseRate") and bayonet_inc["increaseRate"] > 1000:
        bayonet_inc["increaseData"] = None
        bayonet_inc["increaseRate"] = None

    # ========== 6. 查门店分组 (T_SERVERPARTSHOP) ==========
    sql_shop = f"""SELECT "SERVERPARTSHOP_ID", "SHOPTRADE", "SHOPSHORTNAME", "BUSINESS_BRAND"
        FROM "T_SERVERPARTSHOP"
        WHERE "SERVERPART_ID" = {ServerpartId} AND "SHOPTRADE" IS NOT NULL"""
    dt_shop = db.execute_query(sql_shop) or []

    # 按 SHOPTRADE+SHOPSHORTNAME 分组（C: WM_CONCAT）
    from collections import defaultdict
    shop_groups = defaultdict(lambda: {"ids": [], "brand": None, "name": ""})
    for s in dt_shop:
        key = (str(s.get("SHOPTRADE", "")), str(s.get("SHOPSHORTNAME", "")))
        shop_groups[key]["ids"].append(str(s.get("SERVERPARTSHOP_ID", "")))
        shop_groups[key]["name"] = str(s.get("SHOPSHORTNAME", ""))
        if s.get("BUSINESS_BRAND"):
            shop_groups[key]["brand"] = s.get("BUSINESS_BRAND")

    # ========== 7. 遍历门店，构建 ShopINCList ==========
    inc_list = []
    no_inc_list = []

    for (trade, shop_name), info in shop_groups.items():
        shop_ids = info["ids"]
        cur_sum = sum(cur_rev_map.get(sid, 0) for sid in shop_ids)
        cmp_sum = sum(cmp_rev_map.get(sid, 0) for sid in shop_ids)
        has_shop = any(sid in cur_rev_map for sid in shop_ids) or any(sid in cmp_rev_map for sid in shop_ids)

        if not has_shop:
            continue

        shop_model = {
            "ServerpartId": ServerpartId,
            "ServerpartName": sp_name,
            "ServerpartShopId": ",".join(shop_ids),
            "ServerpartShopName": info["name"],
            "RevenueINC": {
                "curYearData": cur_sum if cur_sum else None,
                "lYearData": cmp_sum if cmp_sum else None,
                "increaseData": None,
                "increaseRate": None,
            },
            "Brand_Id": None,
            "Brand_Name": None,
            "Brand_ICO": None,
            "CurTransaction": None,
        }

        if cur_sum and cur_sum != 0 and cmp_sum and cmp_sum != 0:
            inc_data = round(cur_sum - cmp_sum, 2)
            inc_rate = round(inc_data / cmp_sum * 100, 2)
            shop_model["RevenueINC"]["increaseData"] = inc_data
            shop_model["RevenueINC"]["increaseRate"] = inc_rate
            inc_list.append(shop_model)
        else:
            no_inc_list.append(shop_model)

    # 排序
    if SortStr:
        sort_lower = SortStr.lower()
        is_desc = sort_lower.endswith(" desc")
        sort_field = sort_lower.split(" ")[0]
        field_map = {
            "curyeardata": lambda x: x["RevenueINC"].get("curYearData") or 0,
            "lyeardata": lambda x: x["RevenueINC"].get("lYearData") or 0,
            "increasedata": lambda x: x["RevenueINC"].get("increaseData") or 0,
            "increaserate": lambda x: x["RevenueINC"].get("increaseRate") or 0,
        }
        key_fn = field_map.get(sort_field, lambda x: 0)
        inc_list.sort(key=key_fn, reverse=is_desc)

    # 合并：有增幅的在前，无增幅的在后
    all_shops = inc_list + no_inc_list

    # ========== 8. 构建最终返回结构 (HolidayIncreaseModel) ==========
    result_data = {
        "SPRegionTypeId": sp_region_id,
        "SPRegionTypeName": sp_region_name,
        "ServerpartId": ServerpartId,
        "ServerpartName": sp_name,
        "RevenueINC": revenue_inc,
        "AccountINC": {"curYearData": None, "lYearData": None, "increaseData": None, "increaseRate": None},
        "BayonetINC": bayonet_inc,
        "SectionFlowINC": None,
        "ShopINCList": all_shops,
    }

    return Result.success(data=result_data, msg="查询成功")
