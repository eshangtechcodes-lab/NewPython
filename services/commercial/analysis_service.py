from __future__ import annotations
# -*- coding: utf-8 -*-
"""
CommercialApi - 分析说明业务服务
从 analysis_router.py 中抽取的 SQL 和业务逻辑
"""
from typing import Optional
from core.database import DatabaseHelper


def get_analysisins_list(db: DatabaseHelper, search_model: dict) -> tuple[int, list[dict]]:
    """获取分析说明表列表（分页）"""
    search_model = search_model or {}
    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 20) or 20
    sort_str = search_model.get("SortStr", "ANALYSISINS_ID DESC") or "ANALYSISINS_ID DESC"
    search_param = search_model.get("SearchParameter") or {}

    conditions, params = [], []
    formats = search_param.get("ANALYSISINS_FORMATS")
    if formats:
        conditions.append(f'"ANALYSISINS_FORMAT" IN ({formats})')
    types = search_param.get("ANALYSISINS_TYPES")
    if types:
        conditions.append(f'"ANALYSISINS_TYPE" IN ({types})')
    sp_ids = search_param.get("SERVERPART_IDS")
    if sp_ids:
        conditions.append(f'"SERVERPART_ID" IN ({sp_ids})')

    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    count_sql = f'SELECT COUNT(*) AS CNT FROM "T_ANALYSISINS"{where_sql}'
    count_rows = db.execute_query(count_sql, params)
    total = count_rows[0]["CNT"] if count_rows else 0

    offset = (page_index - 1) * page_size
    data_sql = f'SELECT * FROM "T_ANALYSISINS"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
    page_params = (params if params else []) + [page_size, offset]
    page_rows = db.execute_query(data_sql, page_params)

    for r in page_rows:
        if r.get("OPERATE_DATE"):
            r["OPERATE_DATE"] = str(r["OPERATE_DATE"])
        r["ANALYSISINS_FORMATS"] = formats
        r["ANALYSISINS_TYPES"] = types
        r["SERVERPART_IDS"] = sp_ids

    return int(total), page_rows


def get_analysisins_detail(db: DatabaseHelper, analysisins_id: int) -> Optional[dict]:
    """获取分析说明表明细"""
    sql = 'SELECT * FROM "T_ANALYSISINS" WHERE "ANALYSISINS_ID" = ?'
    rows = db.execute_query(sql, [analysisins_id])
    if not rows:
        return None
    data = rows[0]
    if data.get("OPERATE_DATE"):
        data["OPERATE_DATE"] = str(data["OPERATE_DATE"])
    data["ANALYSISINS_FORMATS"] = None
    data["ANALYSISINS_TYPES"] = None
    data["SERVERPART_IDS"] = None
    return data


def get_transaction_analysis(db: DatabaseHelper, tap_model: dict) -> list[dict]:
    """获取时段客单交易分析数据"""
    tap_model = tap_model or {}
    conditions, params = [], []

    shop_id = tap_model.get("ServerpartShopId")
    sp_id = tap_model.get("ServerpartId")
    if shop_id:
        ids = [x.strip() for x in str(shop_id).split(",") if x.strip()]
        placeholders = ",".join(["?" for _ in ids])
        conditions.append(f'"A"."SERVERPARTSHOP_ID" IN ({placeholders})')
        params.extend(ids)
    elif sp_id:
        ids = [x.strip() for x in str(sp_id).split(",") if x.strip()]
        placeholders = ",".join(["?" for _ in ids])
        conditions.append(f'"A"."SERVERPART_ID" IN ({placeholders})')
        params.extend(ids)

    start_month = tap_model.get("StartMonth")
    end_month = tap_model.get("EndMonth")
    if start_month:
        conditions.append('"A"."STATISTICS_MONTH" >= ?')
        params.append(start_month)
    if end_month:
        conditions.append('"A"."STATISTICS_MONTH" <= ?')
        params.append(end_month)

    where_sql = (" AND " + " AND ".join(conditions)) if conditions else ""
    sql = f"""SELECT
        "A"."STATISTICS_HOUR", "A"."AMOUNT_STARTRANGE", "A"."AMOUNT_ENDRANGE",
        SUM("A"."TOTAL_COUNT") AS "TOTAL_COUNT",
        SUM("A"."TICKET_COUNT") AS "TICKET_COUNT",
        SUM("A"."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
    FROM "T_TRANSACTIONANALYSIS" "A", "T_SERVERPARTSHOP" "B"
    WHERE "A"."SERVERPARTSHOP_ID" = "B"."SERVERPARTSHOP_ID"{where_sql}
    GROUP BY "A"."STATISTICS_HOUR", "A"."AMOUNT_STARTRANGE", "A"."AMOUNT_ENDRANGE"
    """
    rows = db.execute_query(sql, params if params else None)
    if not rows:
        return []

    range_set = set()
    for r in rows:
        range_set.add((r.get("AMOUNT_STARTRANGE"), r.get("AMOUNT_ENDRANGE")))
    range_list = sorted(range_set, key=lambda x: (x[0] or 0))

    data_map = {}
    for r in rows:
        key = (r.get("STATISTICS_HOUR"), r.get("AMOUNT_STARTRANGE"), r.get("AMOUNT_ENDRANGE"))
        data_map[key] = r

    data_type = tap_model.get("DataType", 0)
    result_list = []
    for hour in range(24):
        for (start_range, end_range) in range_list:
            if start_range is not None and end_range is not None:
                sr = int(start_range) if start_range == int(start_range) else start_range
                er = int(end_range) if end_range == int(end_range) else end_range
                type_name = f"{sr}-{er}元"
            elif start_range is not None:
                sr = int(start_range) if start_range == int(start_range) else start_range
                type_name = f"{sr}元以上"
            elif end_range is not None:
                er = int(end_range) if end_range == int(end_range) else end_range
                type_name = f"{er}元以下"
            else:
                continue

            key = (hour, start_range, end_range)
            if key in data_map:
                r = data_map[key]
                ticket = r.get("TICKET_COUNT") or 0
                revenue = r.get("REVENUE_AMOUNT") or 0
                if data_type == 1:
                    value = str(ticket)
                elif data_type == 2:
                    value = str(revenue)
                else:
                    value = str(round(revenue / ticket, 2)) if ticket else "0"
            else:
                value = "0"

            result_list.append({"name": f"{hour}时", "value": value, "key": type_name, "data": None})

    return result_list


def get_map_config(db: DatabaseHelper, province_code: str) -> Optional[dict]:
    """获取地图参数配置"""
    sql = 'SELECT * FROM "T_MAPCONFIG" WHERE "PROVINCE_CODE" = ?'
    rows = db.execute_query(sql, [province_code])
    return rows[0] if rows else None


def get_serverpart_type_analysis(db: DatabaseHelper, province_code: str) -> list[dict]:
    """获取服务区分类定级情况"""
    # 省份编码转内码
    pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID" AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = :pc"""
    pc_rows = db.execute_query(pc_sql, {"pc": province_code})
    province_id = pc_rows[0]["FIELDENUM_ID"] if pc_rows else province_code

    rows = []
    for schema_prefix in ["", "PLATFORM_DASHBOARD.", "NEWPYTHON."]:
        try:
            sql = f"""SELECT A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_TYPE, A.THEORY_TYPE,
                             A.NOMINAL_BIAS, A.ECONOMIC_BENIFITRATE
                      FROM {schema_prefix}V_SPCONTRIBUTION A, T_SERVERPART B
                      WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.PROVINCE_CODE = :pid"""
            rows = db.execute_query(sql, {"pid": province_id})
            break
        except Exception:
            continue

    type_names = {1000: "立标杆", 2000: "提能级", 3000: "稳赢收", 4000: "保功能"}
    result_list = []
    for tp, name in type_names.items():
        count = sum(1 for r in rows if str(r.get("SERVERPART_TYPE")) == str(tp))
        result_list.append({"name": name, "value": str(tp), "data": str(count), "key": "1"})

    no_bias = sum(1 for r in rows if float(r.get("NOMINAL_BIAS") or 0) == 0)
    has_bias = sum(1 for r in rows if float(r.get("NOMINAL_BIAS") or 0) != 0)
    result_list.append({"name": "无偏差", "value": "0", "data": str(no_bias), "key": "2"})
    result_list.append({"name": "偏差", "value": "1", "data": str(has_bias), "key": "2"})

    return result_list
