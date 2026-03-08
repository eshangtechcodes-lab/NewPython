from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店费用表业务服务
替代原 SHOPEXPENSEHelper.cs（1765行）中标准 CRUD 逻辑
对应 BusinessProjectController 中 SHOPEXPENSE 相关 5 个接口

注意：
- 原 Synchro 有极复杂的级联逻辑（写 BUSINESSPROJECTSPLIT + 多次合同查询），这里简化为标准更新
- 原 Delete 有级联作废 BUSINESSPROJECTSPLIT + 备份到历史库，这里简化为标准软删除
- 原 GetList 有 summaryList 聚合返回，需特殊处理
- ApproveSHOPEXPENSE 接口对应审批流程（实际调用 Synchro 带 ApprovalProcess=true）
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


TABLE_NAME = "T_SHOPEXPENSE"
PRIMARY_KEY = "SHOPEXPENSE_ID"

EXCLUDE_FIELDS = {
    "SERVERPART_IDS", "SPREGIONTYPE_IDS", "SERVERPARTSHOP_IDS",
    "STATISTICS_MONTH_Start", "STATISTICS_MONTH_End",
    "PREPAID_AMOUNT", "PREPAIDLAST_AMOUNT", "notExist",
    "ShowRevenue", "RevenueAmount", "ApprovalProcess",
    "ChangeFlag", "ImageFlag", "SHOPEXPENSE_TYPE",
}

DATE_FIELDS = {"STATISTICS_MONTH"}

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_shopexpense_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """获取门店费用列表"""
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

        # SERVERPART_IDS IN
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            conditions.append(f"SERVERPART_ID IN ({sp_ids})")

        # SERVERPARTSHOP_IDS IN
        sps_ids = sp.get("SERVERPARTSHOP_IDS")
        if sps_ids and str(sps_ids).strip():
            conditions.append(f"SERVERPARTSHOP_ID IN ({sps_ids})")

        # STATISTICS_MONTH 日期范围
        sm_start = sp.get("STATISTICS_MONTH_Start")
        if sm_start and str(sm_start).strip():
            try:
                d = datetime.strptime(str(sm_start).split(" ")[0], "%Y/%m/%d" if "/" in str(sm_start) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(STATISTICS_MONTH,1,6) >= {d.strftime('%Y%m')}")
            except Exception:
                pass

        sm_end = sp.get("STATISTICS_MONTH_End")
        if sm_end and str(sm_end).strip():
            try:
                d = datetime.strptime(str(sm_end).split(" ")[0], "%Y/%m/%d" if "/" in str(sm_end) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(STATISTICS_MONTH,1,6) <= {d.strftime('%Y%m')}")
            except Exception:
                pass

        # SHOPEXPENSE_TYPE 费用类型（原 C# 查子枚举，简化为直接 IN）
        se_type = sp.get("SHOPEXPENSE_TYPE")
        if se_type and str(se_type).strip():
            conditions.append(f"SHOPEXPENSE_TYPE IN ({se_type})")

        # notExist 排除费用类型
        not_exist = sp.get("notExist")
        if not_exist and str(not_exist).strip():
            conditions.append(f"SHOPEXPENSE_TYPE NOT IN ({not_exist})")

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


def get_shopexpense_detail(db: DatabaseHelper, se_id: int) -> Optional[dict]:
    """获取门店费用明细"""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {se_id}")
    if not rows:
        return None
    return rows[0]


def synchro_shopexpense(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步门店费用（简化版：不含级联写 BUSINESSPROJECTSPLIT 逻辑）
    原 C# 在 Synchro 后会根据费用类型自动创建对应的拆分记录
    """
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    # 默认有效状态
    if db_data.get("SHOPEXPENSE_STATE") is None:
        db_data["SHOPEXPENSE_STATE"] = 1

    def _fmt_month(val):
        if val is None:
            return None
        s = str(val).strip()
        if not s:
            return None
        try:
            dt = datetime.strptime(s.split(" ")[0], "%Y/%m/%d" if "/" in s else "%Y-%m-%d")
            return dt.strftime("%Y%m")
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
                continue
            if key in DATE_FIELDS:
                fv = _fmt_month(value)
                set_parts.append(f"{key} = {fv}" if fv else f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_SHOPEXPENSE.NEXTVAL FROM DUAL")
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
                fv = _fmt_month(value)
                values.append(str(fv) if fv else "NULL")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    return True, data


def delete_shopexpense(db: DatabaseHelper, se_id: int) -> bool:
    """
    删除门店费用（简化版软删除 SHOPEXPENSE_STATE=0）
    注意：原 C# 还会级联作废 BUSINESSPROJECTSPLIT + 备份到历史库
    """
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {se_id}")
    if check == 0:
        return False
    affected = db.execute_non_query(
        f"UPDATE {TABLE_NAME} SET SHOPEXPENSE_STATE = 0 WHERE {PRIMARY_KEY} = {se_id}")
    return affected > 0


def approve_shopexpense(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    审批门店费用（对应 ApproveSHOPEXPENSE 接口）
    原 C# 中 Approve 实际调用 SynchroSHOPEXPENSE 并带 ApprovalProcess=true
    """
    data["ApprovalProcess"] = True
    return synchro_shopexpense(db, data)
