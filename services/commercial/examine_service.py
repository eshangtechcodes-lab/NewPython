# -*- coding: utf-8 -*-
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
CommercialApi - 考核管理业务服务
从 examine_router.py 中抽取的 SQL 和业务逻辑
"""
from typing import Optional
from datetime import datetime
from collections import OrderedDict
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


def _translate_datetime(val):
    """将 Oracle yyyyMMddHHmmss 数字格式日期转为可读字符串"""
    if val is None: return ""
    s = str(val).strip()
    if len(s) >= 8:
        try: return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
        except: return s
    return s


def _translate_meeting_date(raw_date):
    """晨会日期格式转换"""
    if raw_date is None: return ""
    s = str(raw_date).strip()
    if len(s) >= 14:
        try: return f"{s[:4]}/{s[4:6]}/{s[6:8]} {s[8:10]}:{s[10:12]}:{s[12:14]}"
        except: return s
    elif len(s) >= 8:
        return f"{s[:4]}/{s[4:6]}/{s[6:8]} 00:00:00"
    return s


def _translate_meeting_operate_date(raw_op):
    """晨会操作日期（datetime → C# 不补零格式）"""
    if raw_op is None: return ""
    try:
        if isinstance(raw_op, datetime):
            dt_val = raw_op
        else:
            dt_val = datetime.strptime(str(raw_op)[:19], "%Y-%m-%d %H:%M:%S")
        return f"{dt_val.year}/{dt_val.month}/{dt_val.day} {dt_val.hour}:{dt_val.minute:02d}:{dt_val.second:02d}"
    except:
        return str(raw_op)


def _build_search_where(search_param: dict, prefix: str = ""):
    """构建通用搜索 WHERE 条件"""
    conditions, params = [], []
    p = prefix + "." if prefix else ""
    date_start = search_param.get(f"{prefix.upper() if prefix else ''}EXAMINE_DATE_Start") or search_param.get("EXAMINE_DATE_Start")
    date_end = search_param.get(f"{prefix.upper() if prefix else ''}EXAMINE_DATE_End") or search_param.get("EXAMINE_DATE_End")
    if date_start:
        try:
            ds = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
            conditions.append(f"SUBSTR({p}EXAMINE_DATE,1,8) >= ?"); params.append(ds)
        except: pass
    if date_end:
        try:
            de = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
            conditions.append(f"SUBSTR({p}EXAMINE_DATE,1,8) <= ?"); params.append(de)
        except: pass
    for field, col in [("EXAMINE_IDS", "EXAMINE_ID"), ("EXAMINE_TYPES", "EXAMINE_TYPE"),
                       ("SERVERPART_IDS", "SERVERPART_ID"), ("SPREGIONTYPE_IDS", "SPREGIONTYPE_ID")]:
        val = search_param.get(field)
        if val: conditions.append(f"{p}{col} IN ({val})")
    return conditions, params


def _resolve_province_id(db, province_code: str):
    if not province_code: return None
    try:
        rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
                AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND B."FIELDENUM_VALUE" = ?""", [province_code])
        if rows: return rows[0]["FIELDENUM_ID"]
    except: pass
    return province_code


# ===== 1. 考核列表 =====
def get_examine_list(db: DatabaseHelper, search_model: dict) -> tuple[int, list[dict]]:
    search_model = search_model or {}
    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 20) or 20
    sort_str = search_model.get("SortStr", "EXAMINE_ID DESC") or "EXAMINE_ID DESC"
    search_param = search_model.get("SearchParameter") or {}
    conditions, params = _build_search_where(search_param)
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    count_sql = f'SELECT COUNT(*) AS CNT FROM "T_EXAMINE"{where_sql}'
    total = (db.execute_query(count_sql, params) or [{}])[0].get("CNT", 0)
    offset = (page_index - 1) * page_size
    data_sql = f'SELECT * FROM "T_EXAMINE"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
    page_rows = db.execute_query(data_sql, (params or []) + [page_size, offset])
    for r in page_rows:
        r["EXAMINE_DATE"] = _translate_datetime(r.get("EXAMINE_DATE"))
        if r.get("EXAMINE_OPERATEDATE"): r["EXAMINE_OPERATEDATE"] = str(r["EXAMINE_OPERATEDATE"])
    return int(total), page_rows


# ===== 2. 考核明细 =====
def get_examine_detail(db: DatabaseHelper, examine_id: int) -> Optional[dict]:
    rows = db.execute_query('SELECT * FROM "T_EXAMINE" WHERE "EXAMINE_ID" = ?', [examine_id])
    if not rows: return None
    data = rows[0]
    data["EXAMINE_DATE"] = _translate_datetime(data.get("EXAMINE_DATE"))
    if data.get("EXAMINE_OPERATEDATE"): data["EXAMINE_OPERATEDATE"] = str(data["EXAMINE_OPERATEDATE"])
    for k in ["DetailList", "EXAMINE_DATE_Start", "EXAMINE_DATE_End", "EXAMINE_IDS", "EXAMINE_TYPES", "SERVERPART_IDS", "SPREGIONTYPE_IDS"]:
        data[k] = None
    return data


# ===== 3. 晨会列表 =====
def get_meeting_list(db: DatabaseHelper, search_model: dict) -> tuple[int, list[dict]]:
    search_model = search_model or {}
    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 20) or 20
    sort_str = search_model.get("SortStr", "MEETING_ID DESC") or "MEETING_ID DESC"
    search_param = search_model.get("SearchParameter") or {}
    conditions, params = [], []
    for field, col, date_field in [("MEETING_DATE_Start", "MEETING_DATE", True), ("MEETING_DATE_End", "MEETING_DATE", True)]:
        val = search_param.get(field)
        if val and date_field:
            try:
                d = datetime.strptime(val, "%Y-%m-%d").strftime("%Y%m%d")
                op = ">=" if "Start" in field else "<="
                conditions.append(f"SUBSTR(MEETING_DATE,1,8) {op} ?"); params.append(d)
            except: pass
    for field, col in [("MEETING_IDS", "MEETING_ID"), ("SERVERPART_IDS", "SERVERPART_ID"), ("SPREGIONTYPE_IDS", "SPREGIONTYPE_ID")]:
        val = search_param.get(field)
        if val: conditions.append(f"{col} IN ({val})")
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    total = (db.execute_query(f'SELECT COUNT(*) AS CNT FROM "T_MEETING"{where_sql}', params) or [{}])[0].get("CNT", 0)
    offset = (page_index - 1) * page_size
    page_rows = db.execute_query(f'SELECT * FROM "T_MEETING"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?', (params or []) + [page_size, offset])
    for r in page_rows:
        r["MEETING_DATE"] = _translate_meeting_date(r.get("MEETING_DATE"))
        r["MEETING_OPERATEDATE"] = _translate_meeting_operate_date(r.get("MEETING_OPERATEDATE"))
        for k in ["MEETING_IDS", "SERVERPART_IDS", "SPREGIONTYPE_IDS", "MEETING_DATE_Start", "MEETING_DATE_End"]:
            r[k] = None
        for nk in ("SERVERPART_REGION", "MEETING_DESC", "MEETING_STAFFNAME"):
            if r.get(nk) is None: r[nk] = ""
    return int(total), page_rows


# ===== 4. 晨会明细 =====
def get_meeting_detail(db: DatabaseHelper, meeting_id: int) -> Optional[dict]:
    rows = db.execute_query('SELECT * FROM "T_MEETING" WHERE "MEETING_ID" = ?', [meeting_id])
    if not rows: return None
    data = rows[0]
    data["MEETING_DATE"] = _translate_datetime(data.get("MEETING_DATE"))
    if data.get("MEETING_OPERATEDATE"): data["MEETING_OPERATEDATE"] = str(data["MEETING_OPERATEDATE"])
    for k in ["MEETING_DATE_Start", "MEETING_DATE_End", "MEETING_IDS", "SERVERPART_IDS", "SPREGIONTYPE_IDS"]:
        data[k] = None
    return data


# ===== 5. 巡检列表 =====
def get_patrol_list(db: DatabaseHelper, search_model: dict) -> tuple[int, list[dict]]:
    search_model = search_model or {}
    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 20) or 20
    sort_str = search_model.get("SortStr", "PATROL_ID DESC") or "PATROL_ID DESC"
    search_param = search_model.get("SearchParameter") or {}
    conditions, params = [], []
    for field, op in [("PATROL_DATE_Start", ">="), ("PATROL_DATE_End", "<=")]:
        val = search_param.get(field)
        if val:
            try:
                d = datetime.strptime(val, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append(f"SUBSTR(PATROL_DATE,1,8) {op} ?"); params.append(d)
            except: pass
    for field, col in [("PATROL_IDS", "PATROL_ID"), ("PATROL_TYPES", "PATROL_TYPE"),
                       ("SERVERPART_IDS", "SERVERPART_ID"), ("SPREGIONTYPE_IDS", "SPREGIONTYPE_ID")]:
        val = search_param.get(field)
        if val: conditions.append(f"{col} IN ({val})")
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    total = (db.execute_query(f'SELECT COUNT(*) AS CNT FROM "T_PATROL"{where_sql}', params) or [{}])[0].get("CNT", 0)
    offset = (page_index - 1) * page_size
    page_rows = db.execute_query(f'SELECT * FROM "T_PATROL"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?', (params or []) + [page_size, offset])
    for r in page_rows:
        r["PATROL_DATE"] = _translate_datetime(r.get("PATROL_DATE"))
        if r.get("PATROL_OPERATEDATE"): r["PATROL_OPERATEDATE"] = str(r["PATROL_OPERATEDATE"])
    return int(total), page_rows


# ===== 6. 巡检明细 =====
def get_patrol_detail(db: DatabaseHelper, patrol_id: int) -> Optional[dict]:
    rows = db.execute_query('SELECT * FROM "T_PATROL" WHERE "PATROL_ID" = ?', [patrol_id])
    if not rows: return None
    data = rows[0]
    data["PATROL_DATE"] = _translate_datetime(data.get("PATROL_DATE"))
    if data.get("PATROL_OPERATEDATE"): data["PATROL_OPERATEDATE"] = str(data["PATROL_OPERATEDATE"])
    for k in ["PATROL_DATE_Start", "PATROL_DATE_End", "PATROL_IDS", "PATROL_IMG", "PATROL_TYPES", "SERVERPART_IDS", "SPREGIONTYPE_IDS"]:
        data[k] = None
    return data


# ===== 7. WeChat 考核列表 =====
def wechat_get_examine_list(db: DatabaseHelper, sp_region_type_id, serverpart_id, start_date, end_date) -> list[dict]:
    conditions, params = [], []
    if sp_region_type_id: conditions.append(f"SPREGIONTYPE_ID IN ({sp_region_type_id})")
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids: conditions.append(build_in_condition('SERVERPART_ID', _sp_ids))
    for date_val, op in [(start_date, ">="), (end_date, "<=")]:
        if date_val:
            try:
                d = datetime.strptime(date_val, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append(f"SUBSTR(EXAMINE_DATE,1,8) {op} ?"); params.append(d)
            except: pass
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    rows = db.execute_query(f'SELECT * FROM "T_EXAMINE"{where_sql} ORDER BY EXAMINE_SCORE, SPREGIONTYPE_NAME, SERVERPART_NAME, EXAMINE_DATE DESC LIMIT 200', params)
    for r in rows: r["EXAMINE_DATE"] = _translate_datetime(r.get("EXAMINE_DATE"))

    server_groups = OrderedDict()
    for r in rows:
        sp_name = r.get("SERVERPART_NAME", "")
        server_groups.setdefault(sp_name, []).append(r)

    result = []
    for sp_name, sp_rows in server_groups.items():
        region_list = [{"REGION_NAME": rg, "SERVERPARTList": [r for r in sp_rows if r.get("SERVERPART_REGION") == rg]}
                       for rg in ["东", "南", "西", "北"] if any(r.get("SERVERPART_REGION") == rg for r in sp_rows)]
        result.append({"SERVERPART_NAME": sp_name, "EXAMINE_MQUARTER": sp_rows[0].get("EXAMINE_MQUARTER", ""), "list": region_list})
    return result


# ===== 8. WeChat 考核明细 =====
def wechat_get_examine_detail(db: DatabaseHelper, examine_id: int) -> list[dict]:
    rows = db.execute_query('SELECT * FROM "T_EXAMINEDETAIL" WHERE "EXAMINE_ID" = ? ORDER BY "EXAMINEDETAIL_ID"', [examine_id])
    position_groups = OrderedDict()
    for r in (rows or []):
        position_groups.setdefault(r.get("EXAMINE_POSITION", ""), []).append(r)
    return [{"REGION_NAME": pos, "SERVERPARTList": pos_rows} for pos, pos_rows in position_groups.items()]


# ===== 9. WeChat 巡检列表 =====
def wechat_get_patrol_list(db: DatabaseHelper, sp_region_type_id, serverpart_id, start_date, end_date) -> list[dict]:
    conditions, params = [], []
    if sp_region_type_id: conditions.append(f"SPREGIONTYPE_ID IN ({sp_region_type_id})")
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids: conditions.append(build_in_condition('SERVERPART_ID', _sp_ids))
    for date_val, op in [(start_date, ">="), (end_date, "<=")]:
        if date_val:
            try:
                d = datetime.strptime(date_val, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append(f"SUBSTR(PATROL_DATE,1,8) {op} ?"); params.append(d)
            except: pass
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    rows = db.execute_query(f'SELECT * FROM "T_PATROL"{where_sql} ORDER BY SPREGIONTYPE_NAME, SERVERPART_NAME, PATROL_DATE DESC LIMIT 200', params)
    for r in rows: r["PATROL_DATE"] = _translate_datetime(r.get("PATROL_DATE"))
    server_groups = OrderedDict()
    for r in rows: server_groups.setdefault(r.get("SERVERPART_NAME", ""), []).append(r)
    result = []
    for sp_name, sp_rows in server_groups.items():
        region_list = [{"REGION_NAME": rg, "SERVERPARTList": [r for r in sp_rows if r.get("SERVERPART_REGION") == rg]}
                       for rg in ["东", "南", "西", "北"] if any(r.get("SERVERPART_REGION") == rg for r in sp_rows)]
        result.append({"SERVERPART_NAME": sp_name, "list": region_list})
    return result


# ===== 10. WeChat 晨会列表 =====
def wechat_get_meeting_list(db: DatabaseHelper, sp_region_type_id, serverpart_id, start_date, end_date) -> list[dict]:
    conditions, params = [], []
    if sp_region_type_id: conditions.append(f"SPREGIONTYPE_ID IN ({sp_region_type_id})")
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids: conditions.append(build_in_condition('SERVERPART_ID', _sp_ids))
    for date_val, op in [(start_date, ">="), (end_date, "<=")]:
        if date_val:
            try:
                d = datetime.strptime(date_val, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append(f"SUBSTR(MEETING_DATE,1,8) {op} ?"); params.append(d)
            except: pass
    where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    rows = db.execute_query(f'SELECT * FROM "T_MEETING"{where_sql} ORDER BY SPREGIONTYPE_NAME, SERVERPART_NAME, MEETING_DATE DESC LIMIT 200', params)
    for r in rows: r["MEETING_DATE"] = _translate_datetime(r.get("MEETING_DATE"))
    server_groups = OrderedDict()
    for r in rows: server_groups.setdefault(r.get("SERVERPART_NAME", ""), []).append(r)
    result = [{"SERVERPART_NAME": sp, "list": [{"SERVERPARTList": rws}]} for sp, rws in server_groups.items()]
    result.sort(key=lambda x: x.get("SERVERPART_NAME", ""))
    return result


# ===== 11. 巡检分析 =====
def get_patrol_analysis(db: DatabaseHelper, province_code, serverpart_id, sp_region_type_id, start_date, end_date) -> Optional[dict]:
    conditions = ['A."SERVERPART_ID" = B."SERVERPART_ID"', 'A."PATROLDAILY_STATE" = 1']
    params = []
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"'))
    elif sp_region_type_id:
        conditions.append('B."SPREGIONTYPE_ID" = ?'); params.append(int(sp_region_type_id))
    elif province_code:
        conditions.append('B."PROVINCE_CODE" = ?'); params.append(province_code)
    for date_val, op in [(start_date, ">="), (end_date, "<=")]:
        if date_val:
            try:
                d = datetime.strptime(date_val, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append(f'A."STATISTICS_DATE" {op} ?'); params.append(d)
            except: pass
    sql = f"""SELECT SUM("PATROLTOTAL_COUNT") AS "TotalCount", SUM("PATROLABNORMAL_COUNT") AS "AbnormalCount",
        SUM("PATROLRECTIFY_COUNT") AS "RectifyCount" FROM "T_PATROLDAILY" A, "T_SERVERPART" B
        WHERE {" AND ".join(conditions)}"""
    rows = db.execute_query(sql, params)
    if not rows or rows[0].get("TotalCount") is None: return None
    total = int(rows[0]["TotalCount"] or 0); abnormal = int(rows[0]["AbnormalCount"] or 0)
    rectify = int(rows[0]["RectifyCount"] or 0); un_rectify = abnormal - rectify
    return {"TotalCount": total, "AbnormalCount": abnormal, "RectifyCount": rectify,
            "UnRectifyCount": un_rectify, "CompleteRate": round(100 - un_rectify * 100.0 / total, 2) if total > 0 else 0}


# ===== 12. 考核分析 =====
def get_examine_analysis(db: DatabaseHelper, data_type, start_month, end_month, province_code, serverpart_id, sp_region_type_id) -> list[dict]:
    conditions = ['A."SERVERPART_ID" = B."SERVERPART_ID"', 'A."EXAMINE_STATE" = 1', 'A."EXAMINE_TYPE" = ?']
    params = [data_type]
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"'))
    elif sp_region_type_id:
        conditions.append('B."SPREGIONTYPE_ID" = ?'); params.append(int(sp_region_type_id))
    elif province_code:
        pid = _resolve_province_id(db, province_code); conditions.append(f'B."PROVINCE_CODE" = {pid}')
    if start_month: conditions.append('A."EXAMINE_DATE" >= ?'); params.append(f"{start_month}01000000")
    if end_month: conditions.append('A."EXAMINE_DATE" <= ?'); params.append(f"{end_month}32000000")
    sql = f"""SELECT COUNT(1) AS "EXAMINE_COUNT",
        CASE WHEN "EXAMINE_SCORE" >= 90 THEN 'A' WHEN "EXAMINE_SCORE" >= 80 THEN 'B' ELSE 'C' END AS "EXAMINE_SCORE",
        CASE WHEN "EXAMINE_SCORE" >= 90 THEN '优秀' WHEN "EXAMINE_SCORE" >= 80 THEN '良好' ELSE '一般' END AS "EXAMINE_RESULT"
    FROM "T_EXAMINE" A, "T_SERVERPART" B WHERE {" AND ".join(conditions)}
    GROUP BY CASE WHEN "EXAMINE_SCORE" >= 90 THEN 'A' WHEN "EXAMINE_SCORE" >= 80 THEN 'B' ELSE 'C' END,
        CASE WHEN "EXAMINE_SCORE" >= 90 THEN '优秀' WHEN "EXAMINE_SCORE" >= 80 THEN '良好' ELSE '一般' END ORDER BY "EXAMINE_SCORE" """
    rows = db.execute_query(sql, params)
    return [{"name": r.get("EXAMINE_RESULT", ""), "value": str(r.get("EXAMINE_COUNT", "")), "data": r.get("EXAMINE_SCORE", "")} for r in rows]


# ===== 13. 考核结果列表 =====
def get_examine_result_list(db: DatabaseHelper, data_type, start_month, end_month, province_code, serverpart_id, sp_region_type_id) -> list[dict]:
    conditions = ['A."SERVERPART_ID" = B."SERVERPART_ID"', 'A."EXAMINE_STATE" = 1']
    params = []
    if data_type is not None: conditions.append('A."EXAMINE_TYPE" = ?'); params.append(data_type)
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition("B.SERVERPART_ID", _sp_ids).replace('"B.SERVERPART_ID"', 'B."SERVERPART_ID"'))
    elif sp_region_type_id:
        conditions.append('B."SPREGIONTYPE_ID" = ?'); params.append(int(sp_region_type_id))
    elif province_code:
        pid = _resolve_province_id(db, province_code); conditions.append(f'B."PROVINCE_CODE" = {pid}')
    if start_month: conditions.append('A."EXAMINE_DATE" >= ?'); params.append(f"{start_month}01000000")
    if end_month: conditions.append('A."EXAMINE_DATE" <= ?'); params.append(f"{end_month}32000000")

    sql = f"""SELECT A."EXAMINE_ID", A."EXAMINE_MQUARTER", A."EXAMINE_DESC", A."EXAMINE_SCORE", A."EXAMINE_DATE",
        A."SPREGIONTYPE_ID", A."SPREGIONTYPE_NAME", A."SERVERPART_ID", A."SERVERPART_NAME",
        B."SPREGIONTYPE_INDEX", B."SERVERPART_INDEX"
    FROM "T_EXAMINE" A, "T_SERVERPART" B WHERE {" AND ".join(conditions)}
    ORDER BY B."SERVERPART_INDEX", A."EXAMINE_SCORE" DESC"""
    rows = db.execute_query(sql, params)

    examine_ids = [r.get("EXAMINE_ID") for r in rows if r.get("EXAMINE_ID")]
    detail_map = {}
    if examine_ids:
        ids_str = ",".join(str(eid) for eid in examine_ids)
        detail_rows = db.execute_query(
            f"""SELECT "EXAMINEDETAIL_ID","EXAMINE_ID","EXAMINE_POSITION","EXAMINE_CONTENT",
            "DEDUCTION_REASON","DEDUCTION_SCORE","EXAMINEDETAIL_DESC","EXAMINEDETAIL_URL","EXAMINEDEAL_URL"
            FROM "T_EXAMINEDETAIL" WHERE "EXAMINE_ID" IN ({ids_str}) ORDER BY "EXAMINEDETAIL_ID" """) or []
        for d in detail_rows: detail_map.setdefault(d.get("EXAMINE_ID"), []).append(d)

    sp_groups = OrderedDict()
    for r in rows:
        sp_id = r.get("SERVERPART_ID")
        sp_groups.setdefault(sp_id, {"info": r, "examines": []})
        sp_groups[sp_id]["examines"].append(r)

    result_list = []
    for sp_id, group in sp_groups.items():
        info = group["info"]
        region_map = OrderedDict()
        for exam in group["examines"]:
            for d in detail_map.get(exam.get("EXAMINE_ID"), []):
                pos = d.get("EXAMINE_POSITION", "")
                region_map.setdefault(pos, {"score": 0.0, "details": []})
                try: region_map[pos]["score"] += float(d.get("DEDUCTION_SCORE") or 0)
                except: pass
                region_map[pos]["details"].append({k: d.get(k) for k in ["EXAMINEDETAIL_ID","EXAMINE_POSITION","EXAMINE_CONTENT","DEDUCTION_REASON","DEDUCTION_SCORE","EXAMINEDETAIL_DESC","EXAMINEDETAIL_URL","EXAMINEDEAL_URL"]})
        result_list.append({
            "SPREGIONTYPE_ID": info.get("SPREGIONTYPE_ID"), "SPREGIONTYPE_NAME": info.get("SPREGIONTYPE_NAME"),
            "SPREGIONTYPE_INDEX": info.get("SPREGIONTYPE_INDEX"), "SERVERPART_ID": info.get("SERVERPART_ID"),
            "SERVERPART_INDEX": info.get("SERVERPART_INDEX"), "SERVERPART_NAME": info.get("SERVERPART_NAME"),
            "SERVERPART_TAG": None, "EXAMINE_MQUARTER": info.get("EXAMINE_MQUARTER"), "EXAMINE_DESC": info.get("EXAMINE_DESC"),
            "list": [{"REGION_NAME": rn, "EXAMINE_SCORE": rd["score"], "SERVERPARTList": rd["details"]} for rn, rd in region_map.items()]
        })
    return result_list


# ===== 14. 巡检结果列表 =====
def get_patrol_result_list(db: DatabaseHelper, province_code, serverpart_id, sp_region_type_id, start_date, end_date) -> list[dict]:
    conditions = ['A."SERVERPART_ID" = B."SERVERPART_ID"', 'A."PATROL_ID" = C."PATROL_ID"',
                   'A."PATROL_STATE" = 1', 'C."PATROLDETAIL_STATE" <> 1']
    params = []
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        conditions.append(build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"'))
    elif sp_region_type_id:
        conditions.append('B."SPREGIONTYPE_ID" = ?'); params.append(int(sp_region_type_id))
    elif province_code:
        conditions.append('B."PROVINCE_CODE" = ?'); params.append(province_code)
    for date_val, op, fmt in [(start_date, ">=", "%Y%m%d000000"), (end_date, "<=", "%Y%m%d240000")]:
        if date_val:
            try:
                d = datetime.strptime(date_val, "%Y-%m-%d").strftime(fmt)
                conditions.append(f'A."PATROL_DATE" {op} ?'); params.append(d)
            except: pass
    sql = f"""SELECT A."PATROL_ID", A."SPREGIONTYPE_ID", A."SPREGIONTYPE_NAME",
        A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION",
        A."PATROL_PERSON", A."PATROL_DATE", C."PATROLDETAIL_ID", C."PATROL_POSITION",
        C."PATROL_SITUATION", C."PATROLDETAIL_STATE", C."RECTIFICATION_PERIOD",
        C."PATROLDETAIL_URL", C."PATROLDEAL_URL"
    FROM "T_PATROL" A, "T_SERVERPART" B, "T_PATROLDETAIL" C WHERE {" AND ".join(conditions)}"""
    rows = db.execute_query(sql, params)
    for r in rows: r["PATROL_DATE"] = _translate_datetime(r.get("PATROL_DATE"))
    return rows


# ===== 15. 考评列表（Redis） =====
def get_evaluate_res_list(province_code, role_type, statistics_month, serverpart_id) -> list[dict]:
    evaluate_list = []
    try:
        import redis, json as json_mod
        redis_host, redis_port = "127.0.0.1", 6379
        try:
            from core.config import settings
            if hasattr(settings, 'REVENUE_REDIS_HOST'): redis_host = settings.REVENUE_REDIS_HOST
            if hasattr(settings, 'REVENUE_REDIS_PORT'): redis_port = settings.REVENUE_REDIS_PORT
        except: pass
        r = redis.Redis(host=redis_host, port=redis_port, db=3, decode_responses=True)
        table_name = f"{province_code}:evaluate:{role_type}:{statistics_month}"
        raw_list = r.lrange(table_name, 0, -1)
        for item in raw_list:
            try: evaluate_list.append(json_mod.loads(item) if isinstance(item, str) else item)
            except: continue
        if serverpart_id:
            sp_ids = [s.strip() for s in str(serverpart_id).split(",")]
            evaluate_list = [e for e in evaluate_list if str(e.get("ServerpartId", "")) in sp_ids]
        if evaluate_list:
            evaluate_list.sort(key=lambda x: float(x.get("EvaluateScore", 0) or 0), reverse=True)
    except: pass
    return evaluate_list
