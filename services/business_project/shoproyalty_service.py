from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店提成营收(ShopRoyalty) + 应收拆分明细(SHOPROYALTYDETAIL) 业务服务
对应 C# SHOPROYALTYHelper.cs / SHOPROYALTYDETAILHelper.cs
"""
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# ===================================================================
# ShopRoyalty 通用 WHERE 构建
# ===================================================================

_SR_EXCLUDE = {"SHOPROYALTY_IDS", "BUSINESSPROJECT_IDS", "SEPARATE_STATE",
               "STARTDATESearch", "ENDDATESearch"}


def _build_shoproyalty_where(sp: dict, query_type: int = 0) -> str:
    """构建 T_SHOPROYALTY WHERE 子句"""
    parts = []
    for k, v in sp.items():
        if k in _SR_EXCLUDE or k in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if query_type == 0 and isinstance(v, str):
            parts.append(f"{k} LIKE '%{v}%'")
        elif isinstance(v, str):
            parts.append(f"{k} = '{v}'")
        else:
            parts.append(f"{k} = {v}")

    # SHOPROYALTY_IDS
    if sp.get("SHOPROYALTY_IDS"):
        parts.append(f"SHOPROYALTY_ID IN ({sp['SHOPROYALTY_IDS']})")
    # BUSINESSPROJECT_IDS
    if sp.get("BUSINESSPROJECT_IDS"):
        parts.append(f"BUSINESSPROJECT_ID IN ({sp['BUSINESSPROJECT_IDS']})")
    # 日期区间：STARTDATESearch → ENDDATE >= ?, ENDDATESearch → STARTDATE <= ?
    if sp.get("STARTDATESearch"):
        parts.append(f"ENDDATE >= TO_DATE('{sp['STARTDATESearch']}','YYYY/MM/DD')")
    if sp.get("ENDDATESearch"):
        parts.append(f"STARTDATE <= TO_DATE('{sp['ENDDATESearch']}','YYYY/MM/DD')")

    return " WHERE " + " AND ".join(parts) if parts else ""


# ===================================================================
# 1. GetShopRoyaltyList
# ===================================================================

def get_shoproyalty_list(db: DatabaseHelper, search_model: SearchModel):
    """获取门店提成营收表列表"""
    sp = search_model.SearchParameter or {}
    where_sql = _build_shoproyalty_where(sp, search_model.QueryType or 0)

    rows = db.execute_query(f"SELECT * FROM T_SHOPROYALTY{where_sql}")
    if not rows:
        return 0, []

    # SEPARATE_STATE 关联：当指定 BUSINESSPROJECT_ID 或 REGISTERCOMPACT_ID 时
    show_separate = bool(sp.get("BUSINESSPROJECT_ID") or sp.get("REGISTERCOMPACT_ID"))
    detail_ids = set()
    if show_separate:
        detail_where = []
        if sp.get("BUSINESSPROJECT_ID"):
            detail_where.append(f"BUSINESSPROJECT_ID = {sp['BUSINESSPROJECT_ID']}")
        if sp.get("REGISTERCOMPACT_ID"):
            detail_where.append(f"REGISTERCOMPACT_ID = {sp['REGISTERCOMPACT_ID']}")
        detail_where.append("SHOPROYALTYDETAIL_STATE = 1")
        detail_rows = db.execute_query(
            f"SELECT SHOPROYALTY_ID FROM T_SHOPROYALTYDETAIL WHERE {' AND '.join(detail_where)}")
        detail_ids = {str(r["SHOPROYALTY_ID"]) for r in (detail_rows or [])}

    for row in rows:
        if show_separate:
            row["SEPARATE_STATE"] = str(row.get("SHOPROYALTY_ID", "")) in detail_ids
        else:
            row["SEPARATE_STATE"] = False

    # keyword 过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            val = str(kw["Value"]).lower()
            rows = [r for r in rows if any(val in str(r.get(k, "")).lower() for k in keys)]

    # 排序（默认 BUSINESSPROJECT_ID,ENDDATE）
    sort_str = search_model.SortStr or "BUSINESSPROJECT_ID"
    is_desc = "DESC" in (sort_str or "").upper()
    sort_field = sort_str.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
    first_field = sort_field.split(",")[0].strip()
    try:
        rows.sort(key=lambda r: r.get(first_field) or "", reverse=is_desc)
    except Exception:
        pass

    total = len(rows)
    # 分页
    pi = search_model.PageIndex or 0
    ps = search_model.PageSize or 0
    if pi > 0 and ps > 0:
        start = (pi - 1) * ps
        rows = rows[start:start + ps]
    elif len(rows) > 10:
        rows = rows[:10]

    return total, rows


# ===================================================================
# 2. GetShopRoyaltyDetail
# ===================================================================

def get_shoproyalty_detail(db: DatabaseHelper, sr_id: int):
    """获取门店提成营收表明细"""
    rows = db.execute_query(
        f"SELECT * FROM T_SHOPROYALTY WHERE SHOPROYALTY_ID = {sr_id}")
    if not rows:
        return None
    row = rows[0]
    # 关联 SHOPROYALTYDETAIL 判断 SEPARATE_STATE
    detail_rows = db.execute_query(
        f"SELECT 1 FROM T_SHOPROYALTYDETAIL WHERE SHOPROYALTY_ID = {sr_id} AND SHOPROYALTYDETAIL_STATE = 1")
    row["SEPARATE_STATE"] = bool(detail_rows)
    return row


# ===================================================================
# 3. SynchroShopRoyalty
# C# 逻辑：计算 NATUREDAY（天数-装修期）、DAILY_AMOUNT，排除 SEPARATE_STATE/IDS
# ===================================================================

_SR_SYNCHRO_EXCLUDE = {"SEPARATE_STATE", "SHOPROYALTY_IDS", "BUSINESSPROJECT_IDS",
                        "STARTDATESearch", "ENDDATESearch"}


def synchro_shoproyalty(db: DatabaseHelper, data: dict):
    """同步门店提成营收表（新增/更新）"""
    sr_id = data.get("SHOPROYALTY_ID")

    # 计算 NATUREDAY
    start_date = data.get("STARTDATE")
    end_date = data.get("ENDDATE")
    if start_date and end_date:
        try:
            sd = datetime.strptime(str(start_date)[:10], "%Y/%m/%d" if "/" in str(start_date) else "%Y-%m-%d")
            ed = datetime.strptime(str(end_date)[:10], "%Y/%m/%d" if "/" in str(end_date) else "%Y-%m-%d")
            nature_day = (ed - sd).days + 1
            data["NATUREDAY"] = nature_day

            # DAILY_AMOUNT 计算
            rentfee = data.get("RENTFEE")
            minturnover = data.get("MINTURNOVER")
            guaranteeratio = data.get("GUARANTEERATIO")
            if nature_day > 0:
                if rentfee is not None and float(rentfee) != 0:
                    data["DAILY_AMOUNT"] = round(float(rentfee) * 10000 / nature_day, 2)
                elif minturnover is not None and guaranteeratio is not None and float(guaranteeratio) != 0:
                    data["DAILY_AMOUNT"] = round(
                        float(minturnover) * 10000 / (float(guaranteeratio) / 100) / nature_day, 2)
        except Exception as e:
            logger.debug(f"NATUREDAY 计算跳过: {e}")

    # 过滤排除字段
    db_data = {k: v for k, v in data.items() if k.upper() not in _SR_SYNCHRO_EXCLUDE}

    if sr_id is not None:
        # 更新
        check = db.execute_query(f"SELECT 1 FROM T_SHOPROYALTY WHERE SHOPROYALTY_ID = {sr_id}")
        if not check:
            return False, data
        set_parts = []
        for k, v in db_data.items():
            if k == "SHOPROYALTY_ID":
                continue
            if v is None:
                set_parts.append(f"{k} = NULL")
            elif isinstance(v, str):
                set_parts.append(f"{k} = '{v}'")
            else:
                set_parts.append(f"{k} = {v}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE T_SHOPROYALTY SET {', '.join(set_parts)} WHERE SHOPROYALTY_ID = {sr_id}")
    else:
        # 新增
        try:
            new_id = db.execute_scalar("SELECT SEQ_SHOPROYALTY.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar("SELECT MAX(SHOPROYALTY_ID) FROM T_SHOPROYALTY") or 0) + 1
        data["SHOPROYALTY_ID"] = new_id
        db_data["SHOPROYALTY_ID"] = new_id

        cols, vals = [], []
        for k, v in db_data.items():
            if v is None:
                continue
            cols.append(k)
            vals.append(f"'{v}'" if isinstance(v, str) else str(v))
        db.execute_non_query(f"INSERT INTO T_SHOPROYALTY ({', '.join(cols)}) VALUES ({', '.join(vals)})")

    return True, data


# ===================================================================
# 4. DeleteShopRoyalty
# C# 逻辑：真删除 + 先备份到历史库 + 级联更新 SHOPROYALTYDETAIL/REVENUECONFIRM/BUSINESSPROJECTSPLIT
# ===================================================================

def delete_shoproyalty(db: DatabaseHelper, sr_id: int):
    """删除门店提成营收表（真删除 + 级联）"""
    rows = db.execute_query(
        f"SELECT SHOPROYALTY_ID, BUSINESSPROJECT_ID FROM T_SHOPROYALTY WHERE SHOPROYALTY_ID = {sr_id}")
    if not rows:
        return False
    bp_id = rows[0].get("BUSINESSPROJECT_ID")

    # 级联更新（表可能不存在，安全处理）
    try:
        db.execute_non_query(
            f"UPDATE T_SHOPROYALTYDETAIL SET SHOPROYALTYDETAIL_STATE = 0 WHERE BUSINESSPROJECT_ID = {bp_id} AND SHOPROYALTY_ID = {sr_id}")
    except Exception:
        pass
    try:
        db.execute_non_query(
            f"UPDATE T_REVENUECONFIRM SET REVENUE_VALID = 0 WHERE BUSINESSPROJECT_ID = {bp_id} AND SHOPROYALTY_ID = {sr_id}")
    except Exception:
        pass
    try:
        db.execute_non_query(
            f"UPDATE T_BUSINESSPROJECTSPLIT SET BUSINESSPROJECTSPLIT_STATE = 0 WHERE BUSINESSPROJECT_ID = {bp_id} AND SHOPROYALTY_ID = {sr_id}")
    except Exception:
        pass

    # 真删除
    db.execute_non_query(f"DELETE FROM T_SHOPROYALTY WHERE SHOPROYALTY_ID = {sr_id}")
    return True


# ===================================================================
# ===================================================================
# SHOPROYALTYDETAIL（门店应收拆分明细表）
# ===================================================================
# ===================================================================

_SRD_EXCLUDE = {"SHOPROYALTY_IDS"}


def _build_shoproyaltydetail_where(sp: dict, query_type: int = 0) -> str:
    """构建 T_SHOPROYALTYDETAIL WHERE 子句"""
    parts = []
    for k, v in sp.items():
        if k in _SRD_EXCLUDE or k in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if query_type == 0 and isinstance(v, str):
            parts.append(f"{k} LIKE '%{v}%'")
        elif isinstance(v, str):
            parts.append(f"{k} = '{v}'")
        else:
            parts.append(f"{k} = {v}")

    if sp.get("SHOPROYALTY_IDS"):
        ids = sp["SHOPROYALTY_IDS"]
        parts.append(f"SHOPROYALTY_ID IN ({ids})")

    return " WHERE " + " AND ".join(parts) if parts else ""


# ===================================================================
# 5. GetSHOPROYALTYDETAILList
# ===================================================================

def get_shoproyaltydetail_list(db: DatabaseHelper, search_model: SearchModel):
    """获取门店应收拆分明细表列表"""
    sp = search_model.SearchParameter or {}
    where_sql = _build_shoproyaltydetail_where(sp, search_model.QueryType or 0)

    rows = db.execute_query(f"SELECT * FROM T_SHOPROYALTYDETAIL{where_sql}")
    if not rows:
        return 0, []

    # keyword 过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            val = str(kw["Value"]).lower()
            rows = [r for r in rows if any(val in str(r.get(k, "")).lower() for k in keys)]

    # 排序
    if search_model.SortStr:
        sf = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda r: r.get(sf, 0) or 0, reverse=is_desc)

    total = len(rows)
    pi = search_model.PageIndex or 0
    ps = search_model.PageSize or 0
    if pi > 0 and ps > 0:
        start = (pi - 1) * ps
        rows = rows[start:start + ps]
    elif len(rows) > 10:
        rows = rows[:10]

    return total, rows


# ===================================================================
# 6. GetSHOPROYALTYDETAILDetail
# ===================================================================

def get_shoproyaltydetail_detail(db: DatabaseHelper, srd_id: int):
    """获取门店应收拆分明细表明细"""
    rows = db.execute_query(
        f"SELECT * FROM T_SHOPROYALTYDETAIL WHERE SHOPROYALTYDETAIL_ID = {srd_id}")
    return rows[0] if rows else None


# ===================================================================
# 7. SynchroSHOPROYALTYDETAIL
# ===================================================================

def synchro_shoproyaltydetail(db: DatabaseHelper, data: dict):
    """同步门店应收拆分明细表（新增/更新）"""
    srd_id = data.get("SHOPROYALTYDETAIL_ID")

    if srd_id is not None:
        check = db.execute_query(
            f"SELECT 1 FROM T_SHOPROYALTYDETAIL WHERE SHOPROYALTYDETAIL_ID = {srd_id}")
        if not check:
            return False, data
        set_parts = []
        for k, v in data.items():
            if k == "SHOPROYALTYDETAIL_ID":
                continue
            if v is None:
                set_parts.append(f"{k} = NULL")
            elif isinstance(v, str):
                set_parts.append(f"{k} = '{v}'")
            else:
                set_parts.append(f"{k} = {v}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE T_SHOPROYALTYDETAIL SET {', '.join(set_parts)} WHERE SHOPROYALTYDETAIL_ID = {srd_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_SHOPROYALTYDETAIL.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar("SELECT MAX(SHOPROYALTYDETAIL_ID) FROM T_SHOPROYALTYDETAIL") or 0) + 1
        data["SHOPROYALTYDETAIL_ID"] = new_id

        cols, vals = [], []
        for k, v in data.items():
            if v is None:
                continue
            cols.append(k)
            vals.append(f"'{v}'" if isinstance(v, str) else str(v))
        db.execute_non_query(
            f"INSERT INTO T_SHOPROYALTYDETAIL ({', '.join(cols)}) VALUES ({', '.join(vals)})")

    return True, data


# ===================================================================
# 8. DeleteSHOPROYALTYDETAIL（软删除 STATE=0）
# ===================================================================

def delete_shoproyaltydetail(db: DatabaseHelper, srd_id: int):
    """删除门店应收拆分明细表（软删除 STATE=0）"""
    affected = db.execute_non_query(
        f"UPDATE T_SHOPROYALTYDETAIL SET SHOPROYALTYDETAIL_STATE = 0 WHERE SHOPROYALTYDETAIL_ID = {srd_id}")
    return affected > 0 if affected else False
