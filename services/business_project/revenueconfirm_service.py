from __future__ import annotations
# -*- coding: utf-8 -*-
"""
营收回款确认表(RevenueConfirm) 业务服务
对应 C# REVENUECONFIRMHelper.cs
"""
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 排除的搜索字段
_RC_EXCLUDE = {"MERCHANTS_ID", "MERCHANTS_NAME", "BUSINESSPROJECT_IDS", "SHOPROYALTY_IDS",
               "BUSINESS_TRADES", "BUSINESS_BRANDS", "BUSINESSAPPROVAL_IDS",
               "BUSINESS_STARTDATE_Start", "BUSINESS_STARTDATE_End",
               "BUSINESS_ENDDATE_Start", "BUSINESS_ENDDATE_End", "BUSINESSPROJECT_NAME"}


def _build_rc_where(sp: dict, query_type: int = 0) -> str:
    """构建 T_REVENUECONFIRM WHERE 子句（POST 版本）"""
    parts = []
    for k, v in sp.items():
        if k in _RC_EXCLUDE or k in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if query_type == 0 and isinstance(v, str):
            parts.append(f"{k} LIKE '%{v}%'")
        elif isinstance(v, str):
            parts.append(f"{k} = '{v}'")
        else:
            parts.append(f"{k} = {v}")

    # BUSINESSPROJECT_IDS
    if sp.get("BUSINESSPROJECT_IDS"):
        parts.append(f"BUSINESSPROJECT_ID IN ({sp['BUSINESSPROJECT_IDS']})")
    # SHOPROYALTY_IDS
    if sp.get("SHOPROYALTY_IDS"):
        parts.append(f"SHOPROYALTY_ID IN ({sp['SHOPROYALTY_IDS']})")
    # BUSINESSAPPROVAL_IDS
    if sp.get("BUSINESSAPPROVAL_IDS"):
        parts.append(f"BUSINESSAPPROVAL_ID IN ({sp['BUSINESSAPPROVAL_IDS']})")
    # BUSINESS_TRADES
    if sp.get("BUSINESS_TRADES"):
        trades_in = sp["BUSINESS_TRADES"].replace(",", "','")
        parts.append(f"BUSINESS_TRADE IN ('{trades_in}')")
    # BUSINESS_BRANDS
    if sp.get("BUSINESS_BRANDS"):
        brands_in = sp["BUSINESS_BRANDS"].replace(",", "','")
        parts.append(f"BUSINESS_BRAND IN ('{brands_in}')")
    # 日期区间
    if sp.get("BUSINESS_STARTDATE_Start"):
        parts.append(f"BUSINESS_STARTDATE >= TO_DATE('{sp['BUSINESS_STARTDATE_Start'].split(' ')[0]}','YYYY/MM/DD')")
    if sp.get("BUSINESS_STARTDATE_End"):
        parts.append(f"BUSINESS_STARTDATE < TO_DATE('{sp['BUSINESS_STARTDATE_End'].split(' ')[0]}','YYYY/MM/DD') + 1")
    if sp.get("BUSINESS_ENDDATE_Start"):
        parts.append(f"BUSINESS_ENDDATE >= TO_DATE('{sp['BUSINESS_ENDDATE_Start'].split(' ')[0]}','YYYY/MM/DD')")
    if sp.get("BUSINESS_ENDDATE_End"):
        parts.append(f"BUSINESS_ENDDATE < TO_DATE('{sp['BUSINESS_ENDDATE_End'].split(' ')[0]}','YYYY/MM/DD') + 1")

    return " WHERE " + " AND ".join(parts) if parts else ""


def _apply_keyword_sort_page(rows, search_model, default_sort="BUSINESS_ENDDATE"):
    """通用 keyword 过滤、排序、分页"""
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            val = str(kw["Value"]).lower()
            rows = [r for r in rows if any(val in str(r.get(k, "")).lower() for k in keys)]

    sort_str = search_model.SortStr or default_sort
    sf = sort_str.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip().split(",")[0].strip()
    is_desc = "desc" in (sort_str or "").lower()
    try:
        rows.sort(key=lambda r: r.get(sf) or "", reverse=is_desc)
    except Exception:
        pass

    total = len(rows)
    pi = search_model.PageIndex or 0
    ps = search_model.PageSize or 0
    if pi > 0 and ps > 0:
        start = (pi - 1) * ps
        rows = rows[start:start + ps]

    return total, rows


# ===================================================================
# 1. GetRevenueConfirmList (POST 版本 - SearchModel)
# ===================================================================

def get_revenueconfirm_list(db: DatabaseHelper, search_model: SearchModel):
    """获取营收回款确认表列表（POST 版本）"""
    sp = search_model.SearchParameter or {}
    where_sql = _build_rc_where(sp, search_model.QueryType or 0)
    rows = db.execute_query(f"SELECT * FROM T_REVENUECONFIRM{where_sql}")
    if not rows:
        return 0, []
    return _apply_keyword_sort_page(rows, search_model, "BUSINESS_ENDDATE")


# ===================================================================
# 2. GetRevenueConfirmList (GET 版本 - 三表 JOIN)
# ===================================================================

def get_revenueconfirm_list_get(db: DatabaseHelper, serverpart_id: str = "", merchants_id: str = "",
                                 business_type: str = "", start_date: str = "", end_date: str = "",
                                 page_size: int = None, page_index: int = None, sort_str: str = ""):
    """获取服务区应收回款信息（GET 版本 - 三表 JOIN）"""
    where_sql = ""
    if serverpart_id:
        where_sql += f""" AND EXISTS (SELECT 1 FROM T_RTREGISTERCOMPACT C,
                    T_RTBUSINESSPROJECT D
            WHERE A.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID AND
                C.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID AND
                C.SERVERPART_ID IN ({serverpart_id}))"""
    if merchants_id:
        where_sql += f" AND A.MERCHANTS_ID IN ({merchants_id})"
    if business_type:
        where_sql += f" AND A.BUSINESS_TYPE IN ({business_type})"
    if start_date:
        where_sql += f" AND B.BUSINESS_ENDDATE >= TO_DATE('{start_date.split(' ')[0]}','YYYY/MM/DD')"
    if end_date:
        where_sql += f" AND B.BUSINESS_ENDDATE < TO_DATE('{end_date.split(' ')[0]}','YYYY/MM/DD') + 1"

    sql = f"""SELECT
            A.MERCHANTS_ID,A.MERCHANTS_NAME,A.BUSINESSPROJECT_ID,A.BUSINESSPROJECT_NAME,
            B.REVENUECONFIRM_ID,B.SHOPROYALTY_ID,B.SERVERPARTSHOP_ID,
            B.BUSINESS_MONTH,B.BUSINESS_STARTDATE,B.BUSINESS_ENDDATE,B.BUSINESS_DAYS,
            B.GUARANTEE_AMOUNT,B.ACTUAL_REVENUE,B.PARTYA_SHAREPROFIT,B.PARTYB_SHAREPROFIT,
            B.PARTYC_SHAREPROFIT,B.LIQUIDATION_AMOUNT,B.ACTUAL_ACCOUNTS,B.REVENUE_VALID,
            B.REDUCTION_AMOUNT,B.CORRECT_AMOUNT,B.REVENUECONFIRM_DESC,E.GUARANTEERATIO
        FROM
            T_BUSINESSPROJECT A,
            T_REVENUECONFIRM B,
            T_SHOPROYALTY E
        WHERE
            A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID AND
            B.SHOPROYALTY_ID = E.SHOPROYALTY_ID AND
            A.PROJECT_VALID = 1{where_sql}"""

    rows = db.execute_query(sql)
    if not rows:
        return 0, []

    sort_f = sort_str or "BUSINESS_ENDDATE"
    is_desc = "desc" in sort_f.lower()
    sf = sort_f.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip().split(",")[0].strip()
    try:
        rows.sort(key=lambda r: r.get(sf) or "", reverse=is_desc)
    except Exception:
        pass

    total = len(rows)
    if page_size and page_index:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]

    return total, rows


# ===================================================================
# 3. GetRevenueConfirmDetail
# ===================================================================

def get_revenueconfirm_detail(db: DatabaseHelper, rc_id: int):
    """获取营收回款确认表明细"""
    rows = db.execute_query(f"SELECT * FROM T_REVENUECONFIRM WHERE REVENUECONFIRM_ID = {rc_id}")
    return rows[0] if rows else None


# ===================================================================
# 4. SynchroRevenueConfirm
# ===================================================================

def synchro_revenueconfirm(db: DatabaseHelper, data: dict):
    """同步营收回款确认表（新增/更新）"""
    rc_id = data.get("REVENUECONFIRM_ID")

    # 过滤排除字段
    db_data = {k: v for k, v in data.items() if k.upper() not in _RC_EXCLUDE}

    # 日期字段处理
    date_fields = {"BUSINESS_STARTDATE", "BUSINESS_ENDDATE"}

    if rc_id is not None:
        check = db.execute_query(f"SELECT 1 FROM T_REVENUECONFIRM WHERE REVENUECONFIRM_ID = {rc_id}")
        if not check:
            return False
        set_parts = []
        for k, v in db_data.items():
            if k == "REVENUECONFIRM_ID":
                continue
            if k in date_fields:
                if v:
                    set_parts.append(f"{k} = TO_DATE('{v}','YYYY/MM/DD HH24:MI:SS')")
                else:
                    set_parts.append(f"{k} = NULL")
            elif v is None:
                set_parts.append(f"{k} = NULL")
            elif isinstance(v, str):
                set_parts.append(f"{k} = '{v}'")
            else:
                set_parts.append(f"{k} = {v}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE T_REVENUECONFIRM SET {', '.join(set_parts)} WHERE REVENUECONFIRM_ID = {rc_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_REVENUECONFIRM.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar("SELECT MAX(REVENUECONFIRM_ID) FROM T_REVENUECONFIRM") or 0) + 1
        db_data["REVENUECONFIRM_ID"] = new_id

        cols, vals = [], []
        for k, v in db_data.items():
            if v is None:
                continue
            cols.append(k)
            if k in date_fields:
                vals.append(f"TO_DATE('{v}','YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(v, str):
                vals.append(f"'{v}'")
            else:
                vals.append(str(v))
        db.execute_non_query(f"INSERT INTO T_REVENUECONFIRM ({', '.join(cols)}) VALUES ({', '.join(vals)})")

    return True


# ===================================================================
# 5. DeleteRevenueConfirm（真删除）
# ===================================================================

def delete_revenueconfirm(db: DatabaseHelper, rc_id: int):
    """删除营收回款确认表（真删除）"""
    check = db.execute_query(f"SELECT 1 FROM T_REVENUECONFIRM WHERE REVENUECONFIRM_ID = {rc_id}")
    if not check:
        return False
    db.execute_non_query(f"DELETE FROM T_REVENUECONFIRM WHERE REVENUECONFIRM_ID = {rc_id}")
    return True
