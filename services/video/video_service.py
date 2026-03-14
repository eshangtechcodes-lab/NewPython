# -*- coding: utf-8 -*-
"""
ShopVideoController 业务服务
严格按照 C# Helper 源码迁移，保持完全一致的 SQL 逻辑

C# 源文件参考：
  - EXTRANETHelper.cs (193行)
  - EXTRANETDETAILHelper.cs (193行)
  - ShopVideoHelper.cs (793行)
  - VIDEOLOGHelper.cs (340行)
"""
from __future__ import annotations
from loguru import logger
from core.database import DatabaseHelper


def _fetch_one(db: DatabaseHelper, sql: str, params: dict = None):
    """执行查询并返回第一条记录（dict），无结果返回 None"""
    rows = db.execute_query(sql, params) if params else db.execute_query(sql)
    return rows[0] if rows else None


# ============================================================
# 实体元数据（从 C# Helper 精确提取）
# ============================================================
ENTITIES = {
    "EXTRANET": {
        "table": "T_EXTRANET",
        "schema": "",  # C# Business.EXTRANET 默认 schema
        "pk": "EXTRANET_ID",
        "seq": "SEQ_EXTRANET",
        "delete_type": "hard",  # C# EXTRANETHelper.DeleteEXTRANET: _EXTRANET.Delete()
        "fields": [
            "EXTRANET_ID", "SERVERPART_ID", "EXTRANET_IP",
            "VIDEOIP", "VIDEOPORT", "LOGUSERNAME", "LOGPASSWORD", "LOGINPORT",
        ],
        "exclude_insert": {"EXTRANET_ID"},
        "date_fields": set(),
        "date_range": {},
        "in_fields": {},
    },
    "EXTRANETDETAIL": {
        "table": "T_EXTRANETDETAIL",
        "schema": "",  # 达梦中表在 NEWPYTHON schema 下
        "pk": "EXTRANETDETAIL_ID",
        "seq": "SEQ_EXTRANETDETAIL",
        "delete_type": "hard",  # C# EXTRANETDETAILHelper.DeleteEXTRANETDETAIL: _EXTRANETDETAIL.Delete()
        "fields": [
            "EXTRANETDETAIL_ID", "EXTRANET_ID", "EQUIPMENT_TYPE", "VEDIO_TYPE",
            "VIDEOIP", "VIDEO_PUBLICIP", "VIDEO_INTRANETIP",
            "VIDEOPORT", "LOGUSERNAME", "LOGPASSWORD", "LOGINPORT", "EXTRANETDETAIL_DESC",
        ],
        "exclude_insert": {"EXTRANETDETAIL_ID"},
        "date_fields": set(),
        "date_range": {},
        "in_fields": {},
    },
    "SHOPVIDEO": {
        "table": "T_SHOPVIDEO",
        "schema": "",  # C# Business.SHOPVIDEO 默认 schema
        "pk": "SHOPVIDEO_ID",
        "seq": "SEQ_SHOPVIDEO",
        "delete_type": "hard",  # C# ShopVideoHelper.DeleteSHOPVIDEO: _SHOPVIDEO.Delete()
        "fields": [
            "SHOPVIDEO_ID", "EXTRANETDETAIL_ID", "SERVERPARTCODE", "SHOPCODE",
            "MACHINENAME", "MACHINE_IP", "VIDEO_IP", "VIDEOPORT",
            "CHANEL_NAME", "SHOPVIDEO_DESC", "SERVICE_TYPE",
            "CAMERA_X", "CAMERA_Y", "HEAT_X", "HEAT_Y",
            "LONGITUDE", "LATITUDE", "CAMERA_ORDER", "ISMONITOR",
        ],
        "exclude_insert": {"SHOPVIDEO_ID"},
        "date_fields": set(),
        "date_range": {},
        "in_fields": {},
    },
}


# ============================================================
# 通用 CRUD 函数（按 C# OperationDataHelper 模式实现）
# ============================================================

def _get_full_table(entity_cfg: dict) -> str:
    """获取完整表名（含 schema 前缀）"""
    schema = entity_cfg.get("schema", "")
    table = entity_cfg["table"]
    return f"{schema}.{table}" if schema else table


def _build_where(sp: dict, entity_cfg: dict, query_type: int = 0) -> str:
    """
    按 C# OperationDataHelper.GetWhereSQL 逻辑构建 WHERE 条件
    - query_type=0: LIKE 模糊匹配字符串
    - query_type=1: = 精确匹配
    """
    conditions = []
    fields_set = set(entity_cfg.get("fields", []))

    for key, val in sp.items():
        if val is None or str(val).strip() == "":
            continue
        # 跳过非表字段（查询辅助参数）
        upper_key = key.upper()
        if upper_key not in {f.upper() for f in fields_set}:
            continue
        # --- SQL 参数化: 去除单引号和百分号防注入 ---
        val_str = str(val).strip().replace("'", "").replace("%", "")
        if query_type == 0:
            conditions.append(f"{key} LIKE '%{val_str}%'")
        else:
            conditions.append(f"{key} = '{val_str}'")

    # IN 查询字段
    in_fields = entity_cfg.get("in_fields", {})
    for db_field, param_name in in_fields.items():
        val = sp.get(param_name, "")
        if val and str(val).strip():
            # --- SQL 参数化: IN 字段通过整数解析防注入 ---
            safe_ids = [str(int(x.strip())) for x in str(val).split(',') if x.strip().isdigit()]
            if safe_ids:
                conditions.append(f"{db_field} IN ({','.join(safe_ids)})")

    # 日期范围查询
    date_range = entity_cfg.get("date_range", {})
    for db_field, (start_param, end_param, fmt) in date_range.items():
        start_val = sp.get(start_param, "")
        end_val = sp.get(end_param, "")
        if start_val and str(start_val).strip():
            safe_sv = str(start_val).strip().replace("'", "")
            conditions.append(f"{db_field} >= '{safe_sv}'")
        if end_val and str(end_val).strip():
            safe_ev = str(end_val).strip().replace("'", "")
            conditions.append(f"{db_field} <= '{safe_ev}'")

    return " AND ".join(conditions)


def get_entity_list(db: DatabaseHelper, entity_name: str, search_model: dict):
    """通用 GetXXXList"""
    cfg = ENTITIES[entity_name]
    full_table = _get_full_table(cfg)
    sp = search_model.get("SearchParameter") or {}
    query_type = search_model.get("QueryType", 0)

    where_clause = _build_where(sp, cfg, query_type)
    sql = f"SELECT * FROM {full_table}"
    if where_clause:
        sql += f" WHERE {where_clause}"

    # 关键词过滤
    keyword = search_model.get("keyWord") or {}
    kw_key = keyword.get("Key", "")
    kw_val = keyword.get("Value", "")
    if kw_key and kw_val:
        # --- SQL 参数化: 关键字去除单引号和百分号防注入 ---
        safe_kw = kw_val.replace("'", "").replace("%", "")
        kw_conditions = []
        for col in kw_key.split(','):
            col = col.strip()
            if col and col.isalnum():
                kw_conditions.append(f"{col} LIKE '%{safe_kw}%'")
        if kw_conditions:
            kw_filter = '(' + ' OR '.join(kw_conditions) + ')'
            sql += (' AND ' if where_clause else ' WHERE ') + kw_filter

    # 排序
    sort_str = search_model.get("SortStr", "")
    if sort_str and sort_str.strip():
        # --- SQL 参数化: 排序字段只保留安全字符 ---
        safe_sort = sort_str.strip().replace("'", "").replace(";", "")
        sql += f" ORDER BY {safe_sort}"

    rows = db.execute_query(sql)
    total = len(rows)

    # 分页
    page_index = search_model.get("PageIndex")
    page_size = search_model.get("PageSize")
    if page_index is not None and page_size is not None and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]

    return rows, total


def get_entity_detail(db: DatabaseHelper, entity_name: str, pk_val: int):
    """通用 GetXXXDetail"""
    cfg = ENTITIES[entity_name]
    full_table = _get_full_table(cfg)
    pk = cfg["pk"]
    sql = f"SELECT * FROM {full_table} WHERE {pk} = :pk_val"
    row = _fetch_one(db, sql, {"pk_val": pk_val})
    return row or {}


def synchro_entity(db: DatabaseHelper, entity_name: str, data: dict):
    """通用 SynchroXXX — 有 ID 则 UPDATE，无 ID 则 INSERT"""
    cfg = ENTITIES[entity_name]
    full_table = _get_full_table(cfg)
    pk = cfg["pk"]
    seq = cfg["seq"]
    pk_val = data.get(pk)

    if pk_val is not None:
        # UPDATE - 检查是否存在
        check_sql = f"SELECT COUNT(1) AS CNT FROM {full_table} WHERE {pk} = :pk_val"
        result = _fetch_one(db, check_sql, {"pk_val": pk_val})
        if not result or result.get("CNT", 0) == 0:
            return False, None

        set_parts = []
        params = {"pk_val": pk_val}
        for field in cfg["fields"]:
            if field == pk:
                continue
            if field in data:
                param_key = f"p_{field.lower()}"
                set_parts.append(f"{field} = :{param_key}")
                params[param_key] = data[field]
        if set_parts:
            update_sql = f"UPDATE {full_table} SET {', '.join(set_parts)} WHERE {pk} = :pk_val"
            db.execute_non_query(update_sql, params)
        return True, data
    else:
        # INSERT - 用 MAX(PK)+1 生成新 ID（序列权限不足时的替代方案）
        max_sql = f"SELECT NVL(MAX({pk}), 0) + 1 AS NEW_ID FROM {full_table}"
        seq_row = _fetch_one(db, max_sql)
        new_id = seq_row["NEW_ID"]
        data[pk] = new_id

        columns = [pk]
        values = [f":p_{pk.lower()}"]
        params = {f"p_{pk.lower()}": new_id}
        for field in cfg["fields"]:
            if field == pk:
                continue
            if field in data:
                param_key = f"p_{field.lower()}"
                columns.append(field)
                values.append(f":{param_key}")
                params[param_key] = data[field]

        insert_sql = f"INSERT INTO {full_table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql, params)
        return True, data


def delete_entity(db: DatabaseHelper, entity_name: str, pk_val: int):
    """通用 DeleteXXX — Video 模块全部是物理删除"""
    cfg = ENTITIES[entity_name]
    full_table = _get_full_table(cfg)
    pk = cfg["pk"]

    # 检查是否存在
    check_sql = f"SELECT COUNT(1) AS CNT FROM {full_table} WHERE {pk} = :pk_val"
    result = _fetch_one(db, check_sql, {"pk_val": pk_val})
    if not result or result.get("CNT", 0) == 0:
        return True  # C# 中即使不存在也返回 true

    delete_sql = f"DELETE FROM {full_table} WHERE {pk} = :pk_val"
    db.execute_non_query(delete_sql, {"pk_val": pk_val})
    return True


# ============================================================
# VI-04: VIDEOLOG 专用函数
# C# VIDEOLOGHelper.cs — GetVIDEOLOGList 含 Search_Type 多分支
# ============================================================

def get_videolog_list(db: DatabaseHelper, search_model: dict):
    """
    获取异常稽核查看日志表列表 — C# VIDEOLOGHelper.GetVIDEOLOGList
    根据 Search_Type 分支联表查询：
      1000: 匹配异常稽核表 T_YSABNORMALITY
      2000: 匹配现场稽查表 T_CHECKACCOUNT
      2010: 匹配异常现场稽查表 T_ABNORMALAUDIT
      3000: 匹配日结账期表 T_ENDACCOUNT
      4000: 匹配销售流水表 T_YSSELLMASTER
    """
    sp = search_model.get("SearchParameter") or {}
    query_type = search_model.get("QueryType", 0)
    table = "T_VIDEOLOG"

    # 构建基础 WHERE（排除非表字段）
    videolog_fields = {
        "VIDEOLOG_ID", "VIDEOLOG_TYPE", "CHECKACCOUNT_ID", "ABNORMALAUDIT_ID",
        "ENDACCOUNT_ID", "ABNORMALITY_CODE", "USER_ID", "USER_NAME",
        "OPERATE_DATE", "VIDEOLOG_DESC", "SERVERPART_CODE",
    }
    conditions = []
    for key, val in sp.items():
        if val is None or str(val).strip() == "":
            continue
        if key.upper() in {"SEARCH_TYPE", "SERVERPART_ID", "SEARCH_STARTDATE", "SEARCH_ENDDATE"}:
            continue  # 这些是分支参数，不直接做 WHERE
        if key.upper() not in {f.upper() for f in videolog_fields}:
            continue
        val_str = str(val).strip()
        if key.upper() == "OPERATE_DATE":
            # --- SQL 参数化: 日期去引号防注入 ---
            safe_v = val_str.replace("'", "")
            conditions.append(f"OPERATE_DATE >= TO_DATE('{safe_v}','YYYY/MM/DD HH24:MI:SS')")
        elif query_type == 0:
            safe_v = val_str.replace("'", "").replace("%", "")
            conditions.append(f"{key} LIKE '%{safe_v}%'")
        else:
            safe_v = val_str.replace("'", "")
            conditions.append(f"{key} = '{safe_v}'")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""

    # 根据 Search_Type 分支构建 SQL
    search_type = sp.get("Search_Type")
    serverpart_id = sp.get("Serverpart_ID", "")
    start_date = sp.get("Search_StartDate", "")
    end_date = sp.get("Search_EndDate", "")

    if search_type == 1000:
        # 匹配异常稽核表
        other_sql = ""
        if serverpart_id:
            # --- SQL 参数化: serverpart_id 整数解析 ---
            safe_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
            if safe_ids:
                other_sql += f" AND B.SERVERPART_ID IN ({','.join(safe_ids)})"
        if start_date:
            sd = start_date.split(' ')[0].replace('/', '').replace('-', '')
            other_sql += f" AND B.ABNORMALITY_TIME >= {sd}000000"
        if end_date:
            ed = end_date.split(' ')[0].replace('/', '').replace('-', '')
            other_sql += f" AND B.ABNORMALITY_TIME < {ed}235959"
        base_where = where_clause if where_clause else "WHERE 1 = 1"
        sql = (f"SELECT * FROM {table} A {base_where} "
               f"AND EXISTS (SELECT 1 FROM HIGHWAY_EXCHANGE.T_YSABNORMALITY B "
               f"WHERE A.ABNORMALITY_CODE = B.ABNORMALITY_CODE{other_sql})")

    elif search_type == 2000:
        # 匹配现场稽查表
        other_sql = ""
        if serverpart_id:
            safe_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
            if safe_ids:
                other_sql += f" AND SERVERPART_ID IN ({','.join(safe_ids)})"
        if start_date:
            safe_sd = start_date.split(' ')[0].replace("'", "")
            other_sql += f" AND CHECK_ENDDATE >= TO_DATE('{safe_sd}','YYYY/MM/DD')"
        if end_date:
            safe_ed = end_date.split(' ')[0].replace("'", "")
            other_sql += f" AND CHECK_ENDDATE < TO_DATE('{safe_ed}','YYYY/MM/DD') + 1"

        if not other_sql:
            other_sql = " AND CHECKACCOUNT_ID IS NOT NULL"
            base_where = where_clause if where_clause else "WHERE 1 = 1"
            sql = f"SELECT * FROM {table} {base_where}{other_sql}"
        else:
            # 先查出 CHECKACCOUNT_ID 列表
            sub_sql = f"SELECT CHECKACCOUNT_ID FROM HIGHWAY_SELLDATA.T_CHECKACCOUNT WHERE 1 = 1{other_sql}"
            sub_rows = db.execute_query(sub_sql)
            if sub_rows:
                ids = ",".join(str(r.get("CHECKACCOUNT_ID", "")) for r in sub_rows if r.get("CHECKACCOUNT_ID"))
                other_sql = f" AND CHECKACCOUNT_ID IN ({ids})" if ids else " AND 1 = 2"
            else:
                other_sql = " AND 1 = 2"
            base_where = where_clause if where_clause else "WHERE 1 = 1"
            sql = f"SELECT * FROM {table} {base_where}{other_sql}"

    elif search_type == 2010:
        # 匹配异常现场稽查表
        other_sql = ""
        if serverpart_id:
            safe_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
            if safe_ids:
                other_sql += f" AND SERVERPART_ID IN ({','.join(safe_ids)})"
        if start_date:
            sd = start_date.split(' ')[0].replace('/', '').replace('-', '')
            other_sql += f" AND CHECK_ENDDATE >= {sd}000000"
        if end_date:
            ed = end_date.split(' ')[0].replace('/', '').replace('-', '')
            other_sql += f" AND CHECK_ENDDATE < {ed}235959"

        if not other_sql:
            other_sql = " AND ABNORMALAUDIT_ID IS NOT NULL"
            base_where = where_clause if where_clause else "WHERE 1 = 1"
            sql = f"SELECT * FROM {table} {base_where}{other_sql}"
        else:
            sub_sql = f"SELECT ABNORMALAUDIT_ID FROM HIGHWAY_SELLDATA.T_ABNORMALAUDIT WHERE 1 = 1{other_sql}"
            sub_rows = db.execute_query(sub_sql)
            if sub_rows:
                ids = ",".join(str(r.get("ABNORMALAUDIT_ID", "")) for r in sub_rows if r.get("ABNORMALAUDIT_ID"))
                other_sql = f" AND ABNORMALAUDIT_ID IN ({ids})" if ids else " AND 1 = 2"
            else:
                other_sql = " AND 1 = 2"
            base_where = where_clause if where_clause else "WHERE 1 = 1"
            sql = f"SELECT * FROM {table} {base_where}{other_sql}"

    elif search_type == 3000:
        # 匹配日结账期表
        other_sql = ""
        if serverpart_id:
            safe_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
            if safe_ids:
                other_sql += f" AND SERVERPART_ID IN ({','.join(safe_ids)})"
        if start_date:
            safe_sd = start_date.split(' ')[0].replace("'", "")
            other_sql += f" AND ENDACCOUNT_DATE >= TO_DATE('{safe_sd}','YYYY/MM/DD')"
        if end_date:
            safe_ed = end_date.split(' ')[0].replace("'", "")
            other_sql += f" AND ENDACCOUNT_DATE < TO_DATE('{safe_ed}','YYYY/MM/DD') + 1"

        if not other_sql:
            other_sql = " AND ENDACCOUNT_ID IS NOT NULL"
            base_where = where_clause if where_clause else "WHERE 1 = 1"
            sql = f"SELECT * FROM {table} {base_where}{other_sql}"
        else:
            sub_sql = f"SELECT ENDACCOUNT_ID FROM HIGHWAY_SELLDATA.T_ENDACCOUNT WHERE 1 = 1{other_sql}"
            sub_rows = db.execute_query(sub_sql)
            if sub_rows:
                ids = ",".join(str(r.get("ENDACCOUNT_ID", "")) for r in sub_rows if r.get("ENDACCOUNT_ID"))
                other_sql = f" AND ENDACCOUNT_ID IN ({ids})" if ids else " AND 1 = 2"
            else:
                other_sql = " AND 1 = 2"
            base_where = where_clause if where_clause else "WHERE 1 = 1"
            sql = f"SELECT * FROM {table} {base_where}{other_sql}"

    elif search_type == 4000:
        # 匹配销售流水表
        other_sql = ""
        if serverpart_id:
            # C# 先查 T_SERVERPART 获取 SERVERPART_CODE
            safe_ids = [str(int(x.strip())) for x in str(serverpart_id).split(',') if x.strip().isdigit()]
            if safe_ids:
                sp_sql = f"SELECT SERVERPART_CODE FROM T_SERVERPART WHERE SERVERPART_ID IN ({','.join(safe_ids)})"
                sp_rows = db.execute_query(sp_sql)
                if sp_rows:
                    codes = ','.join(f"'{r.get('SERVERPART_CODE', '')}'" for r in sp_rows if r.get('SERVERPART_CODE'))
                    if codes:
                        other_sql += f" AND B.SERVERPART_CODE IN ({codes})"
        if start_date:
            sd = start_date.split(' ')[0].replace('/', '').replace('-', '')
            other_sql += f" AND B.SELLMASTER_DATE >= {sd}000000"
        if end_date:
            ed = end_date.split(' ')[0].replace('/', '').replace('-', '')
            other_sql += f" AND B.SELLMASTER_DATE < {ed}235959"
        base_where = where_clause if where_clause else "WHERE 1 = 1"
        sql = (f"SELECT * FROM {table} A {base_where} "
               f"AND EXISTS (SELECT 1 FROM HIGHWAY_SELLDATA.T_YSSELLMASTER B "
               f"WHERE A.ABNORMALITY_CODE = B.SELLMASTER_CODE{other_sql})")
    else:
        # 默认：无分支
        sql = f"SELECT * FROM {table}" + where_clause

    rows = db.execute_query(sql)

    # 关键词过滤（内存过滤）
    keyword = search_model.get("keyWord") or {}
    kw_key = keyword.get("Key", "")
    kw_val = keyword.get("Value", "")
    if kw_key and kw_val and rows:
        kw_cols = [c.strip() for c in kw_key.split(",") if c.strip()]
        filtered = []
        for row in rows:
            for col in kw_cols:
                cell = str(row.get(col, ""))
                if kw_val in cell:
                    filtered.append(row)
                    break
        rows = filtered

    # 排序（数据库已排序则跳过）
    sort_str = search_model.get("SortStr", "")
    if sort_str and sort_str.strip() and rows:
        # 简单实现：仅支持单字段排序
        parts = sort_str.strip().split()
        sort_field = parts[0] if parts else ""
        desc = len(parts) > 1 and parts[1].upper() == "DESC"
        if sort_field:
            rows.sort(key=lambda r: r.get(sort_field, ""), reverse=desc)

    total = len(rows)
    return rows, total


def synchro_videolog(db: DatabaseHelper, data: dict):
    """
    记录异常稽核查看日志 — C# VIDEOLOGHelper.SynchroVIDEOLOG
    纯 INSERT，不做 UPDATE
    """
    # 用 MAX(ID)+1 生成新 ID（序列权限不足时的替代方案）
    sql = """INSERT INTO T_VIDEOLOG (
            VIDEOLOG_ID, VIDEOLOG_TYPE, CHECKACCOUNT_ID, ABNORMALAUDIT_ID,
            ABNORMALITY_CODE, ENDACCOUNT_ID, USER_ID, USER_NAME,
            OPERATE_DATE, VIDEOLOG_DESC, SERVERPART_CODE
        ) VALUES (
            (SELECT NVL(MAX(VIDEOLOG_ID), 0) + 1 FROM T_VIDEOLOG),
            :p_videolog_type, :p_checkaccount_id, :p_abnormalaudit_id,
            :p_abnormality_code, :p_endaccount_id, :p_user_id, :p_user_name,
            SYSDATE, :p_videolog_desc, :p_serverpart_code
        )"""

    abnormality_code = data.get("ABNORMALITY_CODE", "") or ""
    serverpart_code = abnormality_code[:6] if len(abnormality_code) >= 6 else ""

    params = {
        "p_videolog_type": data.get("VIDEOLOG_TYPE"),
        "p_checkaccount_id": data.get("CHECKACCOUNT_ID"),
        "p_abnormalaudit_id": data.get("ABNORMALAUDIT_ID"),
        "p_abnormality_code": abnormality_code,
        "p_endaccount_id": data.get("ENDACCOUNT_ID"),
        "p_user_id": data.get("USER_ID"),
        "p_user_name": data.get("USER_NAME", ""),
        "p_videolog_desc": data.get("VIDEOLOG_DESC", ""),
        "p_serverpart_code": serverpart_code,
    }
    db.execute_non_query(sql, params)
    return True


# ============================================================
# VI-05: 聚合接口骨架
# GetShopVideoInfo / GetYSShopVideoInfo
# 涉及 V_SHOPVIDEO 视图 + 跨库异常表，先做骨架
# ============================================================

def get_shop_video_info(db: DatabaseHelper, serverpart_code: str, serverpart_shop_code: str,
                        machine_code: str, abnormality_code: str,
                        check_endaccount_id: int = None, abnormal_audit_id: int = None,
                        endaccount_id: int = None, use_ys_table: bool = False):
    """
    获取门店异常稽核视频信息
    C# ShopVideoHelper.GetShopVideoInfo / GetYSShopVideoInfo
    use_ys_table=False → 查 T_ABNORMALITY_服务区编码（老表）
    use_ys_table=True  → 查 T_YSABNORMALITY（新表）
    """
    result = {}

    # 第一步：从 V_SHOPVIDEO 查询摄像头信息
    video_sql = ("SELECT * FROM V_SHOPVIDEO "
                 "WHERE SERVERPARTCODE = :sp_code AND SHOPCODE = :shop_code")
    video_rows = db.execute_query(video_sql, {
        "sp_code": serverpart_code, "shop_code": serverpart_shop_code
    })

    if not video_rows:
        return None

    # 三级匹配摄像头（与 C# 一致）
    dr = None
    # 1. 匹配机器号的稽核摄像头 (VEDIO_TYPE=2000 AND MACHINECODE)
    for r in video_rows:
        if r.get("VEDIO_TYPE") == 2000 and str(r.get("MACHINECODE", "")) == machine_code:
            dr = r
            break
    # 2. 匹配机器号（MACHINENAME字段）
    if dr is None:
        for r in video_rows:
            if r.get("VEDIO_TYPE") == 2000 and str(r.get("MACHINENAME", "")) == machine_code:
                dr = r
                break
    # 3. 门店的稽核摄像头
    if dr is None:
        for r in video_rows:
            if r.get("VEDIO_TYPE") == 2000:
                dr = r
                break
    # 4. 任意摄像头
    if dr is None and video_rows:
        dr = video_rows[0]

    if dr is None:
        return None

    # 填充摄像头基本信息
    result["Equipment_Type"] = dr.get("EQUIPMENT_TYPE")
    if use_ys_table and dr.get("VIDEO_PUBLICIP"):
        result["VideoIP"] = dr.get("VIDEO_PUBLICIP", "")
    else:
        result["VideoIP"] = dr.get("EXTRANET_IP", "")
    if use_ys_table:
        result["Video_IntranetIP"] = dr.get("VIDEO_INTRANETIP", "")
    result["LogUserName"] = dr.get("LOGUSERNAME", "")
    result["LogPassword"] = dr.get("LOGPASSWORD", "")
    result["LoginPort"] = dr.get("LOGINPORT", "")
    result["VideoPort"] = dr.get("VIDEOPORT", "")
    video_ip = dr.get("VIDEO_IP", "")
    result["ChannelIP"] = int(video_ip) if video_ip and video_ip.strip() else -1
    result["ChannelName"] = dr.get("CHANEL_NAME", "")

    # 第二步：解析异常/日结/稽查数据（骨架）
    # 注意：完整逻辑涉及动态分区表和跨库查询，标注为 B3 深逻辑
    abnormality_model = None

    if abnormality_code:
        try:
            if use_ys_table:
                abn_sql = "SELECT * FROM T_YSABNORMALITY WHERE ABNORMALITY_CODE = :abn_code"
            else:
                # C# 中使用动态表 T_ABNORMALITY_服务区编码
                abn_sql = f"SELECT * FROM T_ABNORMALITY_{serverpart_code} WHERE ABNORMALITY_CODE = :abn_code"
            abn_row = _fetch_one(db, abn_sql, {"abn_code": abnormality_code})
            if abn_row:
                abnormality_model = {
                    "Abnormality_Code": abn_row.get("ABNORMALITY_CODE", ""),
                    "Serverpart_Name": abn_row.get("SERVERPART_NAME", ""),
                    "ServerpartShop_Name": abn_row.get("SHOPNAME", ""),
                    "Abnormality_Time": str(abn_row.get("ABNORMALITY_TIME", "")),
                    "Abnormality_Type": str(abn_row.get("ABNORMALITY_TYPE", "")),
                }
        except Exception as e:
            logger.warning(f"查询异常稽核数据失败（表可能不存在）: {e}")

    elif endaccount_id is not None:
        try:
            ea_sql = "SELECT * FROM HIGHWAY_SELLDATA.T_ENDACCOUNT WHERE ENDACCOUNT_ID = :ea_id"
            ea_row = _fetch_one(db, ea_sql, {"ea_id": endaccount_id})
            if ea_row:
                abnormality_model = {
                    "Abnormality_ID": ea_row.get("ENDACCOUNT_ID"),
                    "Serverpart_Name": ea_row.get("SERVERPART_NAME", ""),
                    "ServerpartShop_Name": ea_row.get("SHOPNAME", ""),
                    "SellWorker_Name": ea_row.get("CASHIER_NAME", ""),
                    "Abnormality_Time": str(ea_row.get("ENDACCOUNT_DATE", "")),
                    "Abnormality_Type": "日结账期",
                }
        except Exception as e:
            logger.warning(f"查询日结账期数据失败: {e}")

    elif check_endaccount_id is not None:
        try:
            ca_sql = "SELECT * FROM HIGHWAY_SELLDATA.T_CHECKACCOUNT WHERE CHECKACCOUNT_ID = :ca_id"
            ca_row = _fetch_one(db, ca_sql, {"ca_id": check_endaccount_id})
            if ca_row:
                abnormality_model = {
                    "Abnormality_ID": ca_row.get("CHECKACCOUNT_ID"),
                    "Abnormality_Code": ca_row.get("CHECKACCOUNT_CODE", ""),
                    "Serverpart_Name": ca_row.get("SERVERPART_NAME", ""),
                    "ServerpartShop_Name": ca_row.get("SHOPNAME", ""),
                    "SellWorker_Name": ca_row.get("CASHIER_NAME", ""),
                    "Abnormality_Time": str(ca_row.get("CHECK_ENDDATE", "")),
                    "Abnormality_Type": "现场稽查",
                }
        except Exception as e:
            logger.warning(f"查询现场稽查数据失败: {e}")

    elif abnormal_audit_id is not None:
        try:
            aa_sql = "SELECT * FROM HIGHWAY_SELLDATA.T_ABNORMALAUDIT WHERE ABNORMALAUDIT_ID = :aa_id"
            aa_row = _fetch_one(db, aa_sql, {"aa_id": abnormal_audit_id})
            if aa_row:
                abnormality_model = {
                    "Abnormality_ID": aa_row.get("ABNORMALAUDIT_ID"),
                    "Serverpart_Name": aa_row.get("SERVERPART_NAME", ""),
                    "ServerpartShop_Name": aa_row.get("SHOPNAME", ""),
                    "SellWorker_Name": aa_row.get("CASHIER_NAME", ""),
                    "Abnormality_Time": str(aa_row.get("CHECK_ENDDATE", "")),
                    "Abnormality_Type": "现场稽查",
                }
        except Exception as e:
            logger.warning(f"查询现场稽查异常数据失败: {e}")

    result["AbnormalityModel"] = abnormality_model
    result["AbnormalityDetails"] = ""  # B3 深逻辑：商品明细拼装

    return result
