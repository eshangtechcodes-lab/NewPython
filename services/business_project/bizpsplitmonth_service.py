from __future__ import annotations
# -*- coding: utf-8 -*-
"""
月度经营项目应收拆分表业务服务
替代原 BIZPSPLITMONTHHelper.cs 中标准 CRUD 逻辑
对应 BusinessProjectController 中 BIZPSPLITMONTH 相关 4 个接口

注意：
- 原 GetDetail 需要 JOIN T_BUSINESSAPPROVAL 取审批状态，这里简化为单表查询
- 原 Helper 还有 GetAnnualSplit 等复杂方法，不在标准 CRUD 范围内
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_BIZPSPLITMONTH"
PRIMARY_KEY = "BIZPSPLITMONTH_ID"

EXCLUDE_FIELDS = {
    "BIZPSPLITMONTH_IDS", "STATISTICS_MONTH_Start", "STATISTICS_MONTH_End",
    "SHOPROYALTY_IDS", "Approvalstate",
}

DATE_FIELDS = {"STATISTICS_MONTH", "STARTDATE", "ENDDATE"}
DATE_FORMAT = {"STATISTICS_MONTH": "%Y%m", "STARTDATE": "%Y%m%d", "ENDDATE": "%Y%m%d"}

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_bizpsplitmonth_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """获取月度经营项目应收拆分表列表"""
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

        # BIZPSPLITMONTH_IDS IN
        bids = sp.get("BIZPSPLITMONTH_IDS")
        if bids and str(bids).strip():
            conditions.append(f"BIZPSPLITMONTH_ID IN ({bids})")

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

        # SHOPROYALTY_IDS IN
        sr_ids = sp.get("SHOPROYALTY_IDS")
        if sr_ids and str(sr_ids).strip():
            conditions.append(f"SHOPROYALTY_ID IN ({sr_ids})")

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


def get_bizpsplitmonth_detail(db: DatabaseHelper, bsm_id: int) -> Optional[dict]:
    """获取月度经营项目应收拆分表明细（简化版：单表）"""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {bsm_id}")
    if not rows:
        return None
    return rows[0]


def synchro_bizpsplitmonth(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """同步月度经营项目应收拆分表"""
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
            new_id = db.execute_scalar("SELECT SEQ_BIZPSPLITMONTH.NEXTVAL FROM DUAL")
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


def delete_bizpsplitmonth(db: DatabaseHelper, bsm_id: int) -> bool:
    """删除月度经营项目应收拆分表（软删除 BIZPSPLITMONTH_STATE = 0）"""
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {bsm_id}")
    if check == 0:
        return False
    affected = db.execute_non_query(
        f"UPDATE {TABLE_NAME} SET BIZPSPLITMONTH_STATE = 0 WHERE {PRIMARY_KEY} = {bsm_id}")
    return affected > 0
