# -*- coding: utf-8 -*-
"""
CommercialApi - 营收同比环比趋势 Service
从 revenue_router.py 中抽取:
  GetRevenueCompare — 营收同比环比对比（含日均趋势折线图）
"""
from __future__ import annotations
from datetime import datetime as dt, timedelta

from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


def _sf(v):
    """安全浮点转换"""
    try: return float(v) if v is not None else 0.0
    except: return 0.0


# ===================================================================
# GetRevenueCompare — 营收同比环比对比
# ===================================================================

def get_revenue_compare(db, province_code, statistics_date,
                        serverpart_id, sp_region_type_id):
    """获取营收同比环比对比数据，返回 dict 或 None
    从 Router get_revenue_compare 迁移（~311 行核心逻辑）
    """
    if not statistics_date:
        return None

    stat_date = (dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date
                 else dt.strptime(statistics_date, "%Y%m%d"))
    date_str = stat_date.strftime("%Y%m%d")
    yoy_date = stat_date.replace(year=stat_date.year - 1).strftime("%Y%m%d")

    # 省份映射
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
        WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    province_id = fe_rows[0]["FIELDENUM_ID"] if fe_rows else province_code

    where_sql = f' AND B."PROVINCE_CODE" = {province_id}'
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition(
            'SERVERPART_ID', _sp_ids
        ).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND B."SPREGIONTYPE_ID" IN ({sp_region_type_id})'

    is_history = stat_date < dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=9)

    # ========== 1. 查当日营收 ==========
    if is_history:
        if not serverpart_id and not sp_region_type_id:
            cur_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A
                WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_DATE" = {date_str}"""
        else:
            cur_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
                SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
                FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
                WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql} AND A."STATISTICS_DATE" = {date_str}"""
    else:
        cur_sql = f"""SELECT SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
            SUM(A."TOTALCOUNT") AS "TOTALCOUNT", SUM(A."CASHPAY") AS "CASHPAY"
            FROM "T_ENDACCOUNT_TEMP" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."VALID" = 1
            AND B."STATISTIC_TYPE" = 1000
            AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
            {where_sql} AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
            AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1"""

    cur_rows = db.execute_query(cur_sql) or []
    rev = round(_sf(cur_rows[0].get("CASHPAY")), 2) if cur_rows and _sf(cur_rows[0].get("TICKETCOUNT")) > 0 else 0.0
    ticket = round(_sf(cur_rows[0].get("TICKETCOUNT")), 2) if cur_rows and _sf(cur_rows[0].get("TICKETCOUNT")) > 0 else 0.0
    avg_t = round(rev / ticket, 2) if ticket > 0 else 0.0

    # ========== 2. 查去年同日 ==========
    if not serverpart_id and not sp_region_type_id:
        yoy_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
            SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A
            WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
            AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_DATE" = {yoy_date}"""
    else:
        yoy_sql = f"""SELECT SUM(A."TICKET_COUNT") AS "TICKETCOUNT",
            SUM(A."TOTAL_COUNT") AS "TOTALCOUNT", SUM(A."REVENUE_AMOUNT") AS "CASHPAY"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
            AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
            AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
            {where_sql} AND A."STATISTICS_DATE" = {yoy_date}"""
    yoy_rows = db.execute_query(yoy_sql) or []
    yoy_rev = _sf(yoy_rows[0].get("CASHPAY")) if yoy_rows else 0
    yoy_ticket = _sf(yoy_rows[0].get("TICKETCOUNT")) if yoy_rows else 0
    yoy_avg = round(yoy_rev / yoy_ticket, 2) if yoy_ticket > 0 else 0.0

    rev_rate = round((rev - yoy_rev) / yoy_rev * 100, 2) if yoy_rev > 0 else None
    ticket_rate = round((ticket - yoy_ticket) / yoy_ticket * 100, 2) if yoy_ticket > 0 else None
    avg_rate = round((avg_t - yoy_avg) / yoy_avg * 100, 2) if yoy_avg > 0 else None

    # ========== 3. 趋势数据：工作日/周末/节假日月度平均 ==========
    year_str = stat_date.strftime("%Y")
    date_sql = f' AND A."STATISTICS_DATE" >= {year_str}0101 AND A."STATISTICS_DATE" <= {date_str}'

    if not serverpart_id and not sp_region_type_id:
        trend_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A
            WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND A."PROVINCE_ID" = {province_id}{date_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
            UNION ALL
            SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A
            WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND A."PROVINCE_ID" = {province_id}{date_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
    else:
        trend_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql}{date_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
            UNION ALL
            SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql}{date_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""

    trend_rows = db.execute_query(trend_sql) or []

    # ========== 4. 去年12月数据（用于1月环比） ==========
    ly_dec_sql = f' AND A."STATISTICS_DATE" >= {int(year_str)-1}1201 AND A."STATISTICS_DATE" <= {int(year_str)-1}1231'
    if not serverpart_id and not sp_region_type_id:
        ly_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A
            WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND A."PROVINCE_ID" = {province_id}{ly_dec_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
            UNION ALL
            SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A
            WHERE A."SERVERPART_ID" = 0 AND A."REVENUEDAILY_STATE" = 1
                AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND A."PROVINCE_ID" = {province_id}{ly_dec_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
    else:
        ly_sql = f"""SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", A."DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND NOT EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql}{ly_dec_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6), A."DATA_TYPE"
            UNION ALL
            SELECT SUBSTR(A."STATISTICS_DATE",1,6) AS "STATISTICS", 2 AS "DATA_TYPE",
                FLOOR(SUM(A."REVENUE_AMOUNT") * 100 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) / 100.0 AS "REVENUE_AMOUNT",
                FLOOR(SUM(A."TICKET_COUNT") * 1.0 / COUNT(DISTINCT A."STATISTICS_DATE") + 0.5) AS "TICKET_COUNT"
            FROM "T_REVENUEDAILY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."REVENUEDAILY_STATE" = 1
                AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
                AND EXISTS (SELECT 1 FROM "T_HOLIDAY" C WHERE A."STATISTICS_DATE" = TO_CHAR(C."HOLIDAY_DATE",'YYYYMMDD'))
                AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999')
                {where_sql}{ly_dec_sql}
            GROUP BY SUBSTR(A."STATISTICS_DATE",1,6)"""
    ly_rows = db.execute_query(ly_sql) or []

    # ========== 5. 查节假日名称 ==========
    hol_sql = f"""SELECT "HOLIDAY_NAME", TO_CHAR("HOLIDAY_DATE",'MM') AS "HOLIDAY_MONTH"
        FROM "T_HOLIDAY"
        WHERE "HOLIDAY_DATE" >= TO_DATE('{year_str}/1/1','YYYY/MM/DD')
        AND "HOLIDAY_DATE" <= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
        GROUP BY "HOLIDAY_NAME", TO_CHAR("HOLIDAY_DATE",'MM')"""
    hol_rows = db.execute_query(hol_sql) or []

    # ========== 6. 构建 trend map ==========
    trend_map = {}
    for r in trend_rows:
        key = (int(_sf(r.get("DATA_TYPE"))), str(r.get("STATISTICS", "")))
        trend_map[key] = {"rev": _sf(r.get("REVENUE_AMOUNT")), "ticket": _sf(r.get("TICKET_COUNT"))}
    for r in ly_rows:
        key = (int(_sf(r.get("DATA_TYPE"))), str(r.get("STATISTICS", "")))
        trend_map[key] = {"rev": _sf(r.get("REVENUE_AMOUNT")), "ticket": _sf(r.get("TICKET_COUNT"))}

    # 节日名称 map: {month: "name1、name2"}
    hol_map = {}
    for r in hol_rows:
        m = str(r.get("HOLIDAY_MONTH", "")).lstrip("0") or "0"
        m_key = m.zfill(2)
        name = str(r.get("HOLIDAY_NAME", ""))
        if m_key not in hol_map:
            hol_map[m_key] = name
        else:
            hol_map[m_key] += "\u3001" + name  # 、

    # ========== 7. 构建3个 List (工作日平均/周末平均/节假日平均) ==========
    data_types = [("0", "工作日平均"), ("1", "周末平均"), ("2", "节假日平均")]
    rev_list, ticket_list, avg_list = [], [], []

    if trend_rows:
        for dt_idx, (dt_code, dt_name) in enumerate(data_types):
            rev_data = [None] * 12
            ticket_data = [None] * 12
            avg_data = [None] * 12
            rev_value = [None] * 12 if dt_code == "2" else None
            ticket_value = [None] * 12 if dt_code == "2" else None
            avg_value = [None] * 12 if dt_code == "2" else None

            for m in range(1, 13):
                month_key = f"{year_str}{m:02d}"
                dt_int = int(dt_code)
                info = trend_map.get((dt_int, month_key))

                # C#: 如果工作日/周末没有当月数据，fallback到节假日
                if info is None and dt_int < 2:
                    info = trend_map.get((2, month_key))

                if dt_code == "2":
                    hname = hol_map.get(f"{m:02d}", "")
                    rev_value[m-1] = [str(m), hname]
                    ticket_value[m-1] = [str(m), hname]
                    avg_value[m-1] = [str(m), hname]

                if info:
                    r_val = round(info["rev"], 2)
                    t_val = round(info["ticket"])
                    a_val = round(r_val / t_val, 2) if t_val > 0 else 0

                    # 计算增长率
                    rate_r, rate_t, rate_a = 0, 0, 0
                    if dt_idx == 0:  # 工作日：较上月增长率
                        if m == 1:
                            ly_key = (dt_int, f"{int(year_str)-1}12")
                            ly_info = trend_map.get(ly_key)
                            if ly_info and ly_info["rev"] > 0:
                                rate_r = round((r_val / ly_info["rev"] - 1) * 100, 2)
                            if ly_info and ly_info["ticket"] > 0:
                                rate_t = round((t_val / ly_info["ticket"] - 1) * 100, 2)
                                ly_avg = ly_info["rev"] / ly_info["ticket"]
                                if ly_avg > 0:
                                    rate_a = round((a_val / ly_avg - 1) * 100, 2)
                        else:
                            prev = rev_data[m-2]
                            if prev and prev[1] > 0:
                                rate_r = round((r_val / prev[1] - 1) * 100, 2)
                            prev_t = ticket_data[m-2]
                            if prev_t and prev_t[1] > 0:
                                rate_t = round((t_val / prev_t[1] - 1) * 100, 2)
                            prev_a = avg_data[m-2]
                            if prev_a and prev_a[1] > 0:
                                rate_a = round((a_val / prev_a[1] - 1) * 100, 2)
                    elif dt_idx == 1:  # 周末：较工作日增长率
                        wd = rev_list[0]["data"][m-1] if rev_list else None
                        if wd and wd[1] > 0:
                            rate_r = round((r_val / wd[1] - 1) * 100, 2)
                        wd_t = ticket_list[0]["data"][m-1] if ticket_list else None
                        if wd_t and wd_t[1] > 0:
                            rate_t = round((t_val / wd_t[1] - 1) * 100, 2)
                        wd_a = avg_list[0]["data"][m-1] if avg_list else None
                        if wd_a and wd_a[1] > 0:
                            rate_a = round((a_val / wd_a[1] - 1) * 100, 2)

                    rev_data[m-1] = [float(m), float(r_val), float(rate_r)]
                    ticket_data[m-1] = [float(m), float(t_val), float(rate_t)]
                    avg_data[m-1] = [float(m), float(a_val), float(rate_a)]
                else:
                    rev_data[m-1] = [float(m), 0.0, 0.0]
                    ticket_data[m-1] = [float(m), 0.0, 0.0]
                    avg_data[m-1] = [float(m), 0.0, 0.0]

            rev_list.append({"name": dt_name, "value": rev_value, "data": rev_data, "CommonScatterList": None})
            ticket_list.append({"name": dt_name, "value": ticket_value, "data": ticket_data, "CommonScatterList": None})
            avg_list.append({"name": dt_name, "value": avg_value, "data": avg_data, "CommonScatterList": None})

    return {
        "RevenueAmount": rev, "RevenueAmountYOYRate": rev_rate,
        "TicketCount": ticket, "TicketCountYOYRate": ticket_rate,
        "AvgTicketAmount": avg_t, "AvgTicketAmountRate": avg_rate,
        "RevenueAmountList": rev_list,
        "TicketCountList": ticket_list,
        "AvgTicketAmountList": avg_list,
    }
