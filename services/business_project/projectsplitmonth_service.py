from __future__ import annotations
# -*- coding: utf-8 -*-
"""
月度经营项目应收拆分汇总表业务服务
替代原 PROJECTSPLITMONTHHelper.cs 中标准 CRUD 逻辑
对应 BusinessProjectController 中 PROJECTSPLITMONTH 相关 4 个接口
表: PLATFORM_DASHBOARD.T_PROJECTSPLITMONTH
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from core.format_utils import format_row_dates
from models.common_model import SearchModel


TABLE_NAME = "T_PROJECTSPLITMONTH"
PRIMARY_KEY = "PROJECTSPLITMONTH_ID"

EXCLUDE_FIELDS = {
    "STATISTICS_MONTH_Start", "STATISTICS_MONTH_End",
    "SHOPROYALTY_IDS", "REGISTERCOMPACT_IDS",
    "BUSINESSPROJECT_IDS", "MERCHANTS_IDS", "SERVERPART_IDS",
}

# 8 个日期字段
DATE_FIELDS = {
    "STATISTICS_MONTH", "COMPACT_STARTDATE", "COMPACT_ENDDATE",
    "SWITCH_DATE", "STARTDATE", "ENDDATE",
    "DECORATE_STARTDATE", "DECORATE_ENDDATE",
}
# 日期格式映射
DATE_FORMAT = {"STATISTICS_MONTH": "%Y%m"}  # 其余默认 %Y%m%d

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_projectsplitmonth_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """获取月度经营项目应收拆分汇总表列表"""
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

        # STATISTICS_MONTH 日期范围
        sm_start = sp.get("STATISTICS_MONTH_Start")
        if sm_start and str(sm_start).strip():
            try:
                d = datetime.strptime(str(sm_start).split(" ")[0], "%Y/%m/%d" if "/" in str(sm_start) else "%Y-%m-%d")
                conditions.append(f"STATISTICS_MONTH >= {d.strftime('%Y%m')}")
            except Exception:
                pass

        sm_end = sp.get("STATISTICS_MONTH_End")
        if sm_end and str(sm_end).strip():
            try:
                d = datetime.strptime(str(sm_end).split(" ")[0], "%Y/%m/%d" if "/" in str(sm_end) else "%Y-%m-%d")
                conditions.append(f"STATISTICS_MONTH <= {d.strftime('%Y%m')}")
            except Exception:
                pass

        # 多个 IN 查询
        for param, col in [
            ("SHOPROYALTY_IDS", "SHOPROYALTY_ID"),
            ("REGISTERCOMPACT_IDS", "REGISTERCOMPACT_ID"),
            ("BUSINESSPROJECT_IDS", "BUSINESSPROJECT_ID"),
            ("MERCHANTS_IDS", "MERCHANTS_ID"),
            ("SERVERPART_IDS", "SERVERPART_ID"),
        ]:
            val = sp.get(param)
            if val and str(val).strip():
                conditions.append(f"{col} IN ({val})")

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

    # C# TranslateDateTime: int 日期→格式化字符串
    for r in rows:
        format_row_dates(r, DATE_FIELDS)
    return int(total_count), rows


def get_projectsplitmonth_detail(db: DatabaseHelper, psm_id: int) -> Optional[dict]:
    """获取月度经营项目应收拆分汇总表明细"""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {psm_id}")
    if not rows:
        return None
    format_row_dates(rows[0], DATE_FIELDS)
    return rows[0]


def synchro_projectsplitmonth(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """同步月度经营项目应收拆分汇总表，含 8 个日期字段处理"""
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    def _fmt_date(key, val):
        if val is None:
            return None
        s = str(val).strip()
        if not s:
            return None
        fmt = DATE_FORMAT.get(key, "%Y%m%d")
        try:
            dt = datetime.strptime(s.split(" ")[0], "%Y/%m/%d" if "/" in s else "%Y-%m-%d")
            return dt.strftime(fmt)
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
                fv = _fmt_date(key, value)
                set_parts.append(f"{key} = {fv}" if fv else f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_PROJECTSPLITMONTH.NEXTVAL FROM DUAL")
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
                fv = _fmt_date(key, value)
                values.append(str(fv) if fv else "NULL")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    return True, data


def delete_projectsplitmonth(db: DatabaseHelper, psm_id: int) -> bool:
    """删除月度经营项目应收拆分汇总表（软删除 PROJECTSPLITMONTH_STATE=0）"""
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {psm_id}")
    if check == 0:
        return False
    affected = db.execute_non_query(
        f"UPDATE {TABLE_NAME} SET PROJECTSPLITMONTH_STATE = 0 WHERE {PRIMARY_KEY} = {psm_id}")
    return affected > 0
