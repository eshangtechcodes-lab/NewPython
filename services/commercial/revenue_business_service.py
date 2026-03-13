# -*- coding: utf-8 -*-
"""
CommercialApi - 业态/品牌消费水平分析 Service
从 revenue_router.py 中抽取:
  GetBusinessTradeLevel, GetBusinessBrandLevel
"""
from __future__ import annotations
from collections import defaultdict
from core.database import DatabaseHelper
from services.commercial.service_utils import safe_float as _sf
from routers.deps import build_in_condition


def _get_province_id(db: DatabaseHelper, province_code: str):
    """省份编码 → 省份内码"""
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
            AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    return fe_rows[0]["FIELDENUM_ID"] if fe_rows else province_code


def _build_level_result(groups_total, groups_range, sorted_items, show_whole, show_count,
                         whole_label, other_label):
    """通用消费水平分组结果构建（业态和品牌共用逻辑）"""
    if show_whole:
        show_count = min(show_count, len(sorted_items)) + 1
    else:
        show_count = min(show_count, len(sorted_items))

    if show_count == 0:
        return None

    legend = [None] * show_count
    amount_ranges = [("1", "低消费"), ("2", "普通消费"), ("3,4", "高消费")]
    col_list = [{"name": ar_name, "value": [ar_key], "data": [0.0] * show_count}
                for ar_key, ar_name in amount_ranges]

    idx = 0
    limit = show_count - 1 if show_whole else show_count
    for item_key, total in sorted_items:
        if idx >= limit:
            break
        legend[idx] = item_key if item_key else other_label
        if total > 0:
            r1 = groups_range[item_key].get(1, 0)
            pct1 = round(r1 / total * 100, 2)
            col_list[0]["data"][idx] = pct1
            r2 = groups_range[item_key].get(2, 0)
            pct2 = round(r2 / total * 100, 2)
            col_list[1]["data"][idx] = pct2
            col_list[2]["data"][idx] = round(100 - pct1 - pct2, 2)
        idx += 1

    # 全量汇总列
    if show_whole:
        legend[show_count - 1] = whole_label
        all_total = sum(groups_total.values())
        if all_total > 0:
            all_r1 = sum(groups_range[k].get(1, 0) for k in groups_total)
            pct1 = round(all_r1 / all_total * 100, 2)
            col_list[0]["data"][show_count - 1] = pct1
            all_r2 = sum(groups_range[k].get(2, 0) for k in groups_total)
            pct2 = round(all_r2 / all_total * 100, 2)
            col_list[1]["data"][show_count - 1] = pct2
            col_list[2]["data"][show_count - 1] = round(100 - pct1 - pct2, 2)

    return {"ColumnList": col_list, "legend": legend}


# ===== 1. GetBusinessTradeLevel =====
def get_business_trade_level(db: DatabaseHelper, province_code, statistics_date,
                              serverpart_id, show_whole_trade) -> dict | None:
    """获取业态消费水平占比"""
    from datetime import datetime as dt

    if not statistics_date:
        return {"ColumnList": [], "legend": None}

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    month_str = stat_date.strftime("%Y%m")
    province_id = _get_province_id(db, province_code)

    where_sql = f' AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_MONTH" = {month_str}'
    if serverpart_id:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', [serverpart_id]).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')

    # 按业态+消费等级分组
    sql = f"""SELECT C."BUSINESS_TRADE", A."AMOUNT_RANGE",
            ROUND(SUM(A."TICKET_COUNT") / MAX(A."STATISTICS_DAYS"), 0) AS "AVGTICKET_COUNT"
        FROM "T_CONSUMPTIONLEVEL" A, "T_SERVERPART" B, "T_SERVERPARTSHOP" C
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."CONSUMPTIONLEVEL_STATE" = 1
            AND A."SERVERPARTSHOP_ID" = C."SERVERPARTSHOP_ID"
            AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
            AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999'){where_sql}
        GROUP BY C."BUSINESS_TRADE", A."AMOUNT_RANGE" """
    rows = db.execute_query(sql) or []

    if not rows:
        return None

    # 查业态名称字典
    trade_rows = db.execute_query(
        """SELECT "AUTOSTATISTICS_ID", "AUTOSTATISTICS_PID", "AUTOSTATISTICS_NAME"
            FROM "T_AUTOSTATISTICS" WHERE "AUTOSTATISTICS_TYPE" = 2000""") or []
    trade_name_map = {str(t["AUTOSTATISTICS_ID"]): t.get("AUTOSTATISTICS_NAME", "") for t in trade_rows}

    # 按业态聚合
    trade_total = defaultdict(float)
    trade_range = defaultdict(lambda: defaultdict(float))
    for r in rows:
        trade = str(r.get("BUSINESS_TRADE") or "")
        ar = int(_sf(r.get("AMOUNT_RANGE")))
        tc = _sf(r.get("AVGTICKET_COUNT"))
        trade_total[trade] += tc
        trade_range[trade][ar] += tc

    # 按客单量降序，只取在字典中有名称的业态
    sorted_trades = sorted(
        [(t, v) for t, v in trade_total.items() if t and t in trade_name_map],
        key=lambda x: x[1], reverse=True
    )
    # 替换 ID → 名称
    sorted_named = [(trade_name_map.get(t, "其他业态"), v) for t, v in sorted_trades]

    return _build_level_result(
        {trade_name_map.get(t, t): v for t, v in trade_total.items()},
        {trade_name_map.get(t, t): trade_range[t] for t in trade_total},
        sorted_named, show_whole_trade, 5, "全业态", "其他业态"
    )


# ===== 2. GetBusinessBrandLevel =====
def get_business_brand_level(db: DatabaseHelper, province_code, statistics_date,
                              serverpart_id, show_whole_brand, show_brand_count) -> dict | None:
    """获取品牌消费水平占比"""
    from datetime import datetime as dt

    if not statistics_date:
        return {"ColumnList": [], "legend": None}

    stat_date = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    month_str = stat_date.strftime("%Y%m")
    province_id = _get_province_id(db, province_code)

    where_sql = f' AND A."PROVINCE_ID" = {province_id} AND A."STATISTICS_MONTH" = {month_str}'
    if serverpart_id:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', [serverpart_id]).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')

    # 按品牌+消费等级分组
    sql = f"""SELECT C."BRAND_NAME", A."AMOUNT_RANGE",
            ROUND(SUM(A."TICKET_COUNT") / MAX(A."STATISTICS_DAYS"), 0) AS "AVGTICKET_COUNT"
        FROM "T_CONSUMPTIONLEVEL" A, "T_SERVERPART" B, "T_SERVERPARTSHOP" C
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID" AND A."CONSUMPTIONLEVEL_STATE" = 1
            AND A."SERVERPARTSHOP_ID" = C."SERVERPARTSHOP_ID"
            AND B."STATISTICS_TYPE" = 1000 AND B."STATISTIC_TYPE" = 1000
            AND B."SERVERPART_CODE" NOT IN ('348888','349999','638888','888888','899999'){where_sql}
        GROUP BY C."BRAND_NAME", A."AMOUNT_RANGE" """
    rows = db.execute_query(sql) or []

    if not rows:
        return None

    # 按品牌聚合
    brand_total = defaultdict(float)
    brand_range = defaultdict(lambda: defaultdict(float))
    for r in rows:
        brand = r.get("BRAND_NAME") or ""
        ar = int(_sf(r.get("AMOUNT_RANGE")))
        tc = _sf(r.get("AVGTICKET_COUNT"))
        brand_total[brand] += tc
        brand_range[brand][ar] += tc

    try:
        brand_count = int(show_brand_count) if show_brand_count and str(show_brand_count).isdigit() else 5
    except:
        brand_count = 5

    sorted_brands = sorted(
        [(b, t) for b, t in brand_total.items() if b],
        key=lambda x: x[1], reverse=True
    )

    return _build_level_result(
        brand_total, brand_range, sorted_brands,
        show_whole_brand, brand_count, "全品牌", "其他品牌"
    )
