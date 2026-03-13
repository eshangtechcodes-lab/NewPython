# -*- coding: utf-8 -*-
"""
CommercialApi - 月度经营分析 Service
从 revenue_router.py 中抽取:
  GetMonthlyBusinessAnalysis  — 月度经营增幅分析
  GetMonthlySPINCAnalysis     — 服务区月度营收增幅分析
"""
from __future__ import annotations

from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


# ===================================================================
# 1. GetMonthlyBusinessAnalysis — 月度经营增幅分析
# ===================================================================

def get_monthly_business_analysis(db, calc_type, province_code,
                                   cur_year, compare_year,
                                   statistics_month, statistics_start_month,
                                   statistics_date, sp_region_type_id,
                                   serverpart_id, business_type,
                                   business_trade, business_region):
    """获取月度经营增幅分析，返回结果列表"""

    # 1. 参数预处理
    stat_month_str = str(statistics_month)
    if len(stat_month_str) >= 6:
        cur_month_ym = int(stat_month_str[:6])
    else:
        cur_month_ym = cur_year * 100 + statistics_month

    if not statistics_start_month:
        if calc_type == 1:
            statistics_start_month = cur_month_ym
        else:
            statistics_start_month = cur_year * 100 + 1

    # 2. 省份/区域内码查询
    pc_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
        WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
        AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else province_code

    # 3. 构建筛选条件
    where_sql = " AND A.PROVINCE_ID = :pid"
    params = {"pid": province_id}
    table_name = "T_PROVINCEREVENUE"

    if sp_region_type_id:
        where_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
        table_name = "T_HOLIDAYREVENUE"
    if serverpart_id:
        _sp_ids = parse_multi_ids(serverpart_id)
        if _sp_ids:
            where_sql += " AND " + build_in_condition(
                "SERVERPART_ID", _sp_ids
            ).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
            table_name = "T_HOLIDAYREVENUE"
    if business_type:
        where_sql += f" AND A.BUSINESS_TYPE IN ({business_type})"
    if business_trade:
        where_sql += f" AND A.SHOPTRADE IN ({business_trade})"
    if business_region:
        where_sql += f" AND A.BUSINESS_REGION IN ({business_region})"

    limit_sql = ""
    st_date = statistics_date.replace("-", "").replace("/", "") if statistics_date else ""
    if st_date and str(cur_year) in st_date:
        limit_sql = f" AND A.STATISTICS_DATE <= {st_date[:8]}"

    # 4. 查询营收数据
    case_sql = """CASE WHEN A.BUSINESS_TYPE = 4000 AND A.SHOPTRADE = '2' THEN 1
                    WHEN A.BUSINESS_TYPE = 4000 AND A.SHOPTRADE <> '2' THEN 2
                    ELSE 3 END"""

    state_col = table_name.replace('T_', '') + '_STATE'
    join_part = " , T_SERVERPART B" if table_name == "T_HOLIDAYREVENUE" else ""
    join_cond = "A.SERVERPART_ID = B.SERVERPART_ID AND" if table_name == "T_HOLIDAYREVENUE" else ""

    rev_base_sql = f"""SELECT
                SUM(A.REVENUE_AMOUNT) AS REVENUE_AMOUNT,
                SUM(A.ACCOUNT_AMOUNTNOTAX) AS ACCOUNT_AMOUNT,
                {case_sql} AS SHOPTRADE
            FROM
                {table_name} A {join_part}
            WHERE
                {join_cond}
                A."{state_col}" = 1 AND
                A.STATISTICS_DATE BETWEEN :start AND :end {where_sql} {limit_sql}
            GROUP BY
                {case_sql}"""

    cur_start = f"{statistics_start_month}01"
    cur_end = f"{cur_month_ym}31"
    cur_rev_rows = db.execute_query(rev_base_sql, {**params, "start": cur_start, "end": cur_end})

    year_diff = cur_year - compare_year
    cy_month_start = statistics_start_month - year_diff * 100
    cy_month_end = cur_month_ym - year_diff * 100

    limit_sql_cy = ""
    if st_date and str(cur_year) in st_date:
        limit_sql_cy = f" AND A.STATISTICS_DATE <= {compare_year}{st_date[4:8]}"

    rev_base_sql_cy = rev_base_sql.replace(limit_sql, limit_sql_cy)
    cy_rev_rows = db.execute_query(rev_base_sql_cy, {**params, "start": f"{cy_month_start}01", "end": f"{cy_month_end}31"})

    # 5. 查询车流量
    flow_where = f" AND EXISTS (SELECT 1 FROM T_SERVERPART S WHERE A.SERVERPART_ID = S.SERVERPART_ID AND S.PROVINCE_CODE = '{province_id}')"
    _sp_ids_flow = parse_multi_ids(serverpart_id)
    if _sp_ids_flow:
        flow_where = " AND " + build_in_condition(
            'SERVERPART_ID', _sp_ids_flow
        ).replace('"SERVERPART_ID"', 'A.SERVERPART_ID')

    flow_sql = f"""SELECT SUM(A.SERVERPART_FLOW) AS SERVERPART_FLOW
               FROM T_SECTIONFLOW A
               WHERE A.SECTIONFLOW_STATUS = 1 AND A.SERVERPART_ID > 0 AND
               A.STATISTICS_DATE BETWEEN :start AND :end {flow_where} {limit_sql}"""

    cur_flow_rows = db.execute_query(flow_sql, {"start": cur_start, "end": cur_end})

    flow_sql_cy = flow_sql.replace(limit_sql, limit_sql_cy).replace(
        "A.SERVERPART_FLOW", "A.SERVERPART_FLOW + NVL(A.SERVERPART_FLOW_ANALOG, 0)")
    cy_flow_rows = db.execute_query(flow_sql_cy, {"start": f"{cy_month_start}01", "end": f"{cy_month_end}31"})

    # 6. 聚合逻辑
    def bind_inc(rev_rows, cy_rows, flow_rows, cy_flow_rows, shoptrade_filter=None, calc_flow=False):
        def get_sum(data, col, filter_val=None):
            if not data:
                return 0.0
            if filter_val == "自营":
                return sum(float(r.get(col) or 0) for r in data if r.get("SHOPTRADE") in (1, 2))
            if filter_val:
                return sum(float(r.get(col) or 0) for r in data if r.get("SHOPTRADE") == filter_val)
            return sum(float(r.get(col) or 0) for r in data)

        cur_rev = round(get_sum(rev_rows, "REVENUE_AMOUNT", shoptrade_filter), 2)
        l_rev = round(get_sum(cy_rows, "REVENUE_AMOUNT", shoptrade_filter), 2)
        cur_acc = round(get_sum(rev_rows, "ACCOUNT_AMOUNT", shoptrade_filter), 2)
        l_acc = round(get_sum(cy_rows, "ACCOUNT_AMOUNT", shoptrade_filter), 2)

        res = {
            "RevenueINC": {"curYearData": cur_rev, "lYearData": l_rev,
                           "increaseData": round(cur_rev - l_rev, 2), "increaseRate": None},
            "AccountINC": {"curYearData": cur_acc, "lYearData": l_acc,
                           "increaseData": round(cur_acc - l_acc, 2), "increaseRate": None},
            "BayonetINC": None
        }
        if l_rev != 0:
            res["RevenueINC"]["increaseRate"] = round((res["RevenueINC"]["increaseData"] / l_rev) * 100, 2)
        if l_acc != 0:
            res["AccountINC"]["increaseRate"] = round((res["AccountINC"]["increaseData"] / l_acc) * 100, 2)

        if calc_flow:
            cf = float(flow_rows[0].get("SERVERPART_FLOW") or 0) if flow_rows else 0.0
            lf = float(cy_flow_rows[0].get("SERVERPART_FLOW") or 0) if cy_flow_rows else 0.0
            res["BayonetINC"] = {"curYearData": cf, "lYearData": lf, "increaseData": cf - lf, "increaseRate": None}
            if lf != 0:
                res["BayonetINC"]["increaseRate"] = round((res["BayonetINC"]["increaseData"] / lf) * 100, 2)
        return res

    results = []
    summary = bind_inc(cur_rev_rows, cy_rev_rows, cur_flow_rows, cy_flow_rows, calc_flow=True)
    summary.update({"ServerpartId": 0, "ServerpartName": "累计"})
    results.append(summary)

    self_run = bind_inc(cur_rev_rows, cy_rev_rows, None, None, shoptrade_filter="自营")
    self_run.update({"SPRegionTypeId": 1, "SPRegionTypeName": "自营", "ServerpartId": None, "ServerpartName": None})
    results.append(self_run)

    names = {1: "便利店", 2: "餐饮客房", 3: "商铺租赁"}
    for i in range(1, 4):
        item = bind_inc(cur_rev_rows, cy_rev_rows, None, None, shoptrade_filter=i)
        item.update({"ServerpartId": i, "ServerpartName": names[i]})
        results.append(item)

    coop = bind_inc(cur_rev_rows, cy_rev_rows, cur_flow_rows, cy_flow_rows, shoptrade_filter=3)
    coop.update({"SPRegionTypeId": 2, "SPRegionTypeName": "外包", "ServerpartId": None, "ServerpartName": None})
    results.append(coop)

    # 补充旧API字段
    for r in results:
        r.setdefault("SPRegionTypeId", None)
        r.setdefault("SPRegionTypeName", None)
        for k in ("TicketINC", "AvgTicketINC", "BayonetINC_ORI", "SectionFlowINC",
                   "ShopINCList", "RankDiff", "Cost_Amount", "Ca_Cost", "Profit_Amount"):
            r.setdefault(k, None)
        for inc_key in ("RevenueINC", "AccountINC", "BayonetINC"):
            inc = r.get(inc_key)
            if inc and isinstance(inc, dict):
                for qk in ("QOQData", "increaseDataQOQ", "increaseRateQOQ", "rankNum"):
                    inc.setdefault(qk, None)

    return results


# ===================================================================
# 2. GetMonthlySPINCAnalysis — 服务区月度营收增幅分析
# ===================================================================

def get_monthly_sp_inc_analysis(db, calc_type, province_code,
                                cur_year, compare_year,
                                statistics_date, statistics_month,
                                statistics_start_month, serverpart_id,
                                business_region, dimension,
                                sp_region_type_id, sort_str):
    """获取服务区月度营收增幅分析，返回结果列表"""

    # 1. 参数处理
    stat_month_str = str(statistics_month)
    if len(stat_month_str) >= 6:
        cur_month_ym = int(stat_month_str[:6])
        month_part = int(stat_month_str[4:6])
    else:
        cur_month_ym = cur_year * 100 + statistics_month
        month_part = statistics_month

    if not statistics_start_month:
        statistics_start_month = cur_month_ym if calc_type == 1 else cur_year * 100 + 1

    pc_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
        WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
        AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else province_code

    where_sql_base = " AND A.PROVINCE_ID = :pid"
    rev_params = {"pid": province_id}
    if serverpart_id:
        rev_ids = ",".join([f"'{s.strip()}'" for s in serverpart_id.split(",")])
        where_sql_base += f" AND A.SERVERPART_ID IN ({rev_ids})"

    limit_sql = ""
    st_date = statistics_date.replace("-", "").replace("/", "") if statistics_date else ""
    if st_date and str(cur_year) in st_date:
        limit_sql = f" AND A.STATISTICS_DATE <= {st_date[:8]}"

    dt_cur_revenue = []
    dt_cy_revenue = []
    dt_cur_bayonet = []
    dt_cy_bayonet = []
    limit_sql_cy = ""

    # 2. 查询营收数据
    if not dimension or "1" in dimension or "2" in dimension:
        rev_sql = f"""SELECT B.SERVERPART_ID, SUM(A.REVENUE_AMOUNT) AS REVENUE_AMOUNT,
                    SUM(A.ACCOUNT_AMOUNTNOTAX) AS ACCOUNT_AMOUNT
                FROM T_HOLIDAYREVENUE A, T_SERVERPART B
                WHERE A.SERVERPART_ID = TO_CHAR(B.SERVERPART_ID) AND A.HOLIDAYREVENUE_STATE = 1
                AND A.STATISTICS_DATE BETWEEN :start AND :end {where_sql_base} {limit_sql}
                GROUP BY B.SERVERPART_ID"""

        dt_cur_revenue = db.execute_query(
            rev_sql, {**rev_params, "start": f"{statistics_start_month}01", "end": f"{cur_month_ym}31"})

        year_diff = cur_year - compare_year
        cy_start = f"{statistics_start_month - year_diff * 100}01"
        cy_end = f"{compare_year}{month_part:02}31"
        limit_sql_cy = (f" AND A.STATISTICS_DATE <= {compare_year}{st_date[4:8]}"
                        if st_date and str(cur_year) in st_date else "")

        rev_sql_cy = rev_sql.replace(limit_sql, limit_sql_cy)
        dt_cy_revenue = db.execute_query(
            rev_sql_cy, {**rev_params, "start": cy_start, "end": cy_end})

    # 3. 查询车流量
    if not dimension or "3" in dimension:
        flow_where = (f" AND EXISTS (SELECT 1 FROM T_SERVERPART S "
                      f"WHERE A.SERVERPART_ID = S.SERVERPART_ID AND S.PROVINCE_CODE = '{province_id}')")
        _sp_ids_f = parse_multi_ids(serverpart_id)
        if _sp_ids_f:
            flow_where = ' AND ' + build_in_condition(
                'SERVERPART_ID', _sp_ids_f
            ).replace('"SERVERPART_ID"', 'A.SERVERPART_ID')

        flow_sql = f"""SELECT SERVERPART_ID, SUM(A.SERVERPART_FLOW) AS SERVERPART_FLOW
                    FROM T_SECTIONFLOW A WHERE A.SECTIONFLOW_STATUS = 1 AND A.SERVERPART_ID > 0
                    AND A.STATISTICS_DATE BETWEEN :start AND :end {flow_where} {limit_sql}
                    GROUP BY SERVERPART_ID"""

        dt_cur_bayonet = db.execute_query(
            flow_sql, {"start": f"{statistics_start_month}01", "end": f"{cur_month_ym}31"})

        flow_sql_cy = flow_sql.replace(limit_sql, limit_sql_cy).replace(
            "A.SERVERPART_FLOW", "A.SERVERPART_FLOW + NVL(A.SERVERPART_FLOW_ANALOG, 0)")
        dt_cy_bayonet = db.execute_query(flow_sql_cy, {"start": cy_start, "end": cy_end})

    # 4. 获取服务区列表
    sp_where = (f"WHERE SPREGIONTYPE_ID IS NOT NULL AND STATISTICS_TYPE = 1000 "
                f"AND STATISTIC_TYPE = 1000 AND PROVINCE_CODE = '{province_id}'")
    _sp_ids_sp = parse_multi_ids(serverpart_id)
    if _sp_ids_sp:
        sp_where += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids_sp)
    dt_serverpart = db.execute_query(
        f"SELECT SPREGIONTYPE_ID, SPREGIONTYPE_NAME, SERVERPART_ID, SERVERPART_NAME, "
        f"SPREGIONTYPE_INDEX, SERVERPART_INDEX FROM T_SERVERPART {sp_where} "
        f"ORDER BY SPREGIONTYPE_INDEX, SERVERPART_INDEX, SERVERPART_ID")

    # 5. 组装数据
    cur_rev_map = {r["SERVERPART_ID"]: r for r in (dt_cur_revenue or [])}
    cy_rev_map = {r["SERVERPART_ID"]: r for r in (dt_cy_revenue or [])}
    cur_flow_map = {r["SERVERPART_ID"]: r for r in (dt_cur_bayonet or [])}
    cy_flow_map = {r["SERVERPART_ID"]: r for r in (dt_cy_bayonet or [])}

    def calc_inc(cur_val, l_val):
        cur_f = float(cur_val) if cur_val is not None else None
        l_f = float(l_val) if l_val is not None else None
        inc = round(cur_f - l_f, 2) if cur_f is not None and l_f is not None else None
        rate = round((inc / l_f) * 100, 2) if inc is not None and l_f and l_f != 0 else None
        return {"curYearData": cur_f, "lYearData": l_f, "increaseData": inc, "increaseRate": rate,
                "QOQData": None, "increaseDataQOQ": None, "increaseRateQOQ": None, "rankNum": None}

    results = []
    for sp in (dt_serverpart or []):
        sp_id = sp["SERVERPART_ID"]
        rev_c = cur_rev_map.get(sp_id, {})
        rev_l = cy_rev_map.get(sp_id, {})
        flow_c = cur_flow_map.get(sp_id, {})
        flow_l = cy_flow_map.get(sp_id, {})

        item = {
            "SPRegionTypeId": sp["SPREGIONTYPE_ID"],
            "SPRegionTypeName": sp["SPREGIONTYPE_NAME"],
            "ServerpartId": sp_id,
            "ServerpartName": sp["SERVERPART_NAME"],
            "RevenueINC": calc_inc(rev_c.get("REVENUE_AMOUNT"), rev_l.get("REVENUE_AMOUNT")),
            "AccountINC": calc_inc(rev_c.get("ACCOUNT_AMOUNT"), rev_l.get("ACCOUNT_AMOUNT")),
            "BayonetINC": calc_inc(flow_c.get("SERVERPART_FLOW"), flow_l.get("SERVERPART_FLOW"))
        }
        results.append(item)

    # 6. 排序
    if sort_str:
        sort_field = sort_str.lower()
        reverse = "desc" in sort_field
        key_map = {
            "revenue": lambda x: x["RevenueINC"]["increaseRate"] or -999999,
            "account": lambda x: x["AccountINC"]["increaseRate"] or -999999,
            "bayonet": lambda x: x["BayonetINC"]["increaseRate"] or -999999,
        }
        for k, func in key_map.items():
            if k in sort_field:
                results.sort(key=func, reverse=reverse)
                break

    # 补充旧API字段
    for r in results:
        for k in ("TicketINC", "AvgTicketINC", "BayonetINC_ORI", "SectionFlowINC",
                   "ShopINCList", "RankDiff", "Cost_Amount", "Ca_Cost", "Profit_Amount"):
            r.setdefault(k, None)

    return results
