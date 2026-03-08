from __future__ import annotations
# -*- coding: utf-8 -*-
"""
审批意见表业务服务
替代原 APPROVEDHelper.cs（259行），标准 CRUD
对应 BusinessProjectController 中 APPROVED 相关 1 个接口（仅 GetList）

注意：虽然 Helper 中有 GetDetail/Synchro/Delete，但 Controller 只暴露了 GetAPPROVEDList
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_APPROVED"
PRIMARY_KEY = "APPROVED_ID"

EXCLUDE_FIELDS = {
    "TABLE_IDS", "APPROVED_TYPES", "APPROVED_DATE_Start", "APPROVED_DATE_End",
}

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_approved_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取审批意见列表
    SELECT * FROM CONTRACT_STORAGE.T_APPROVED + WHERE
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

        # APPROVED_DATE 日期范围（SUBSTR yyyyMMdd）
        ad_start = sp.get("APPROVED_DATE_Start")
        if ad_start and str(ad_start).strip():
            try:
                d = datetime.strptime(str(ad_start).split(" ")[0], "%Y/%m/%d" if "/" in str(ad_start) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(APPROVED_DATE,1,8) >= {d.strftime('%Y%m%d')}")
            except Exception:
                pass

        ad_end = sp.get("APPROVED_DATE_End")
        if ad_end and str(ad_end).strip():
            try:
                d = datetime.strptime(str(ad_end).split(" ")[0], "%Y/%m/%d" if "/" in str(ad_end) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(APPROVED_DATE,1,8) <= {d.strftime('%Y%m%d')}")
            except Exception:
                pass

        # APPROVED_TYPES IN
        at = sp.get("APPROVED_TYPES")
        if at and str(at).strip():
            conditions.append(f"APPROVED_TYPE IN ({at})")

        # TABLE_IDS IN
        ti = sp.get("TABLE_IDS")
        if ti and str(ti).strip():
            conditions.append(f"TABLE_ID IN ({ti})")

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
