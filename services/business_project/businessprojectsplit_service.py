from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营项目应收拆分表业务服务
替代原 BUSINESSPROJECTSPLITHelper.cs 中标准 CRUD 逻辑
对应 BusinessProjectController 中 BUSINESSPROJECTSPLIT 相关 4 个接口

注意：
- 原 GetList 有极其复杂的后处理逻辑（6668行），包括计算当日分润、门店费用等
  这里简化为标准 SQL 查询 + 分页，复杂计算逻辑留待后续优化
- 原 Synchro 有 21 个排除字段 + 3 个日期字段
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_BUSINESSPROJECTSPLIT"
PRIMARY_KEY = "BUSINESSPROJECTSPLIT_ID"

# 原 C# 中 21 个排除字段
EXCLUDE_FIELDS = {
    "BUSINESSPROJECT_IDS", "STATISTICS_DATE_Start", "STATISTICS_DATE_End",
    "STARTDATE_Start", "STARTDATE_End", "ENDDATE_Start", "ENDDATE_End",
    "CURMOBILEPAY_AMOUNT", "CURCASHPAY_AMOUNT",
    "CURROYALTY_PRICE", "CURSUBROYALTY_PRICE", "CURTICKET_FEE",
    "ShopRoyaltyId", "ACCOUNT_AMOUNT",
    "ShowAccount", "ExpenseAmount", "CalcExpiredDays",
    "CompleteState", "CalcAccumulate",
    "ExpenseList", "LogList",
}

DATE_FIELDS = {"STATISTICS_DATE", "STARTDATE", "ENDDATE"}

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_businessprojectsplit_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取经营项目应收拆分表列表（简化版）
    原 C# GetList 有极复杂的后处理，这里只做标准查询+分页
    """
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

        # BUSINESSPROJECT_IDS IN
        bp_ids = sp.get("BUSINESSPROJECT_IDS")
        if bp_ids and str(bp_ids).strip():
            conditions.append(f"BUSINESSPROJECT_ID IN ({bp_ids})")

        # 统计日期范围
        for field_prefix in ["STATISTICS_DATE", "STARTDATE", "ENDDATE"]:
            for suffix, op in [("_Start", ">="), ("_End", "<=")]:
                val = sp.get(f"{field_prefix}{suffix}")
                if val and str(val).strip():
                    try:
                        d = datetime.strptime(str(val).split(" ")[0], "%Y/%m/%d" if "/" in str(val) else "%Y-%m-%d")
                        conditions.append(f"SUBSTR({field_prefix},1,8) {op} {d.strftime('%Y%m%d')}")
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


def get_businessprojectsplit_detail(db: DatabaseHelper, bps_id: int) -> Optional[dict]:
    """获取经营项目应收拆分表明细"""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {bps_id}")
    if not rows:
        return None
    return rows[0]


def synchro_businessprojectsplit(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """同步经营项目应收拆分表"""
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
            new_id = db.execute_scalar("SELECT SEQ_BUSINESSPROJECTSPLIT.NEXTVAL FROM DUAL")
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


def delete_businessprojectsplit(db: DatabaseHelper, bps_id: int) -> bool:
    """删除经营项目应收拆分表（软删除 BUSINESSPROJECTSPLIT_STATE = 0）"""
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {bps_id}")
    if check == 0:
        return False
    affected = db.execute_non_query(
        f"UPDATE {TABLE_NAME} SET BUSINESSPROJECTSPLIT_STATE = 0 WHERE {PRIMARY_KEY} = {bps_id}")
    return affected > 0
