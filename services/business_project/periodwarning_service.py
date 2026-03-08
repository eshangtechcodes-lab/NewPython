from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营项目周期预警表业务服务
替代原 PERIODWARNINGHelper.cs 中标准 CRUD 逻辑
对应 BusinessProjectController 中 PERIODWARNING 相关 4 个接口

注意：
- 原 GetList 有非常复杂的 PERIOD_PROGRESS / GUARANTEED_PROGRESS 计算，已简化为从数据库取值
- 原 Delete 方法体为空（始终返回 false），Python 侧也保持同样行为
- 原 Helper 还有 SolidPeriodAnalysis 方法（生成盈利分析），不在标准 CRUD 范围内
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_PERIODWARNING"
PRIMARY_KEY = "PERIODWARNING_ID"

EXCLUDE_FIELDS = {
    "WARNING_TYPES", "BUSINESSPROJECT_IDS", "SERVERPART_IDS",
    "SERVERPARTSHOP_IDS", "BUSINESS_STATES", "BUSINESS_TRADES",
    "MERCHANTS_IDS", "PROJECT_ENDDATE_Start", "PROJECT_ENDDATE_End",
    "SHOPROYALTY_IDS", "ENDDATE_Start", "ENDDATE_End",
    "PERIOD_PROGRESS", "GUARANTEED_PROGRESS",
}

DATE_FIELDS = {"PROJECT_STARTDATE", "PROJECT_ENDDATE", "STARTDATE", "ENDDATE"}

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_periodwarning_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """获取经营项目周期预警表列表"""
    conditions = []

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        for k, v in sp.items():
            if k in EXCLUDE_FIELDS or k in SEARCH_PARAM_SKIP_FIELDS:
                continue
            if v is None or (isinstance(v, str) and v.strip() == ""):
                continue
            qt = search_model.QueryType or 0
            if qt == 0 and isinstance(v, str):
                conditions.append(f"{k} LIKE '%{v}%'")
            elif isinstance(v, str):
                conditions.append(f"{k} = '{v}'")
            else:
                conditions.append(f"{k} = {v}")

        # WARNING_TYPES IN
        wt = sp.get("WARNING_TYPES")
        if wt and str(wt).strip():
            conditions.append(f"WARNING_TYPE IN ({wt})")

        # BUSINESSPROJECT_IDS IN
        bp_ids = sp.get("BUSINESSPROJECT_IDS")
        if bp_ids and str(bp_ids).strip():
            conditions.append(f"BUSINESSPROJECT_ID IN ({bp_ids})")

        # SERVERPART_IDS IN
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            conditions.append(f"SERVERPART_ID IN ({sp_ids})")

        # BUSINESS_STATES IN
        bs = sp.get("BUSINESS_STATES")
        if bs and str(bs).strip():
            conditions.append(f"BUSINESS_STATE IN ({bs})")

        # MERCHANTS_IDS IN
        mi = sp.get("MERCHANTS_IDS")
        if mi and str(mi).strip():
            conditions.append(f"MERCHANTS_ID IN ({mi})")

        # SHOPROYALTY_IDS IN
        sr = sp.get("SHOPROYALTY_IDS")
        if sr and str(sr).strip():
            conditions.append(f"SHOPROYALTY_ID IN ({sr})")

        # PROJECT_ENDDATE 日期范围
        for suffix, op in [("_Start", ">="), ("_End", "<=")]:
            val = sp.get(f"PROJECT_ENDDATE{suffix}")
            if val and str(val).strip():
                try:
                    d = datetime.strptime(str(val).split(" ")[0], "%Y/%m/%d" if "/" in str(val) else "%Y-%m-%d")
                    conditions.append(f"PROJECT_ENDDATE {op} {d.strftime('%Y%m%d')}")
                except Exception:
                    pass

        # ENDDATE 日期范围
        for suffix, op in [("_Start", ">="), ("_End", "<=")]:
            val = sp.get(f"ENDDATE{suffix}")
            if val and str(val).strip():
                try:
                    d = datetime.strptime(str(val).split(" ")[0], "%Y/%m/%d" if "/" in str(val) else "%Y-%m-%d")
                    conditions.append(f"ENDDATE {op} {d.strftime('%Y%m%d')}")
                except Exception:
                    pass

    where_sql = " WHERE " + " AND ".join(conditions) if conditions else ""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME}{where_sql}")

    # 关键字过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            sv = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(sv in str(r.get(k, "")) for k in keys)]

    # 排序
    if search_model.SortStr:
        sf = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "desc" in (search_model.SortStr or "").lower()
        try:
            rows.sort(key=lambda x: x.get(sf) or "", reverse=is_desc)
        except Exception:
            pass

    total_count = len(rows)

    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    return int(total_count), rows


def get_periodwarning_detail(db: DatabaseHelper, pw_id: int) -> Optional[dict]:
    """获取经营项目周期预警表明细"""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {pw_id}")
    if not rows:
        return None
    return rows[0]


def synchro_periodwarning(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """同步经营项目周期预警表（新增或更新），含日期字段处理"""
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    def _fmt_date(val):
        if val is None:
            return None
        s = str(val).strip()
        if not s:
            return None
        try:
            dt = datetime.strptime(s.split(" ")[0], "%Y/%m/%d" if "/" in s else "%Y-%m-%d")
            return dt.strftime("%Y%m%d")
        except Exception:
            return s

    if record_id is not None:
        check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}")
        if check == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                if key in DATE_FIELDS:
                    set_parts.append(f"{key} = NULL")
                continue
            if key in DATE_FIELDS:
                fv = _fmt_date(value)
                set_parts.append(f"{key} = {fv}" if fv else f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_PERIODWARNING.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        data[PRIMARY_KEY] = new_id
        db_data[PRIMARY_KEY] = new_id

        columns, values = [], []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if key in DATE_FIELDS:
                fv = _fmt_date(value)
                values.append(str(fv) if fv else "NULL")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    return True, data


def delete_periodwarning(db: DatabaseHelper, pw_id: int) -> bool:
    """
    删除经营项目周期预警表
    注意：原 C# 的 DeletePERIODWARNING 方法体为空（始终返回 false）
    Python 侧保持相同行为
    """
    return False
