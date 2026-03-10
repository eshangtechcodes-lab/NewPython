from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营项目预警表业务服务
替代原 PROJECTWARNINGHelper.cs（704行），保持标准 CRUD 逻辑
对应 BusinessProjectController 中 PROJECTWARNING 相关 4 个接口

注意：
- 原 GetList 有 SourcePlatform 和审批权限判定（DealMark），这里简化为标准查询
- 原 GetDetail 是四表 JOIN，这里简化为单表+基本字段
- 原 Helper 还有 ApproveProinst 审批方法，不在这 4 个路由范围内
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from core.format_utils import format_row_dates
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_PROJECTWARNING"
PRIMARY_KEY = "PROJECTWARNING_ID"

# Synchro 排除字段（不入库的查询条件/计算字段）
EXCLUDE_FIELDS = {
    "SERVERPART_IDS", "WARNING_DATE_Start", "WARNING_DATE_End",
    "PROJECTWARNING_STATES", "MerchantRatio", "DealMark",
    "BUSINESSPROJECT_ICO", "COOPMERCHANTS_LINKMAN",
    "COOPMERCHANTS_MOBILEPHONE", "COMPACT_STARTDATE", "COMPACT_ENDDATE",
}

# 日期字段（存储为数字格式 yyyyMMdd，非 TO_DATE）
DATE_FIELDS = {"STARTDATE", "ENDDATE", "WARNING_DATE"}
DATETIME_FIELDS = {"SWITCH_DATE"}

# 通用跳过字段
SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


# ========== 1. GetPROJECTWARNINGList ==========

def get_projectwarning_list(db: DatabaseHelper, search_model: SearchModel,
                            module_guid: str = "", source_platform: str = "") -> tuple[int, list[dict]]:
    """
    获取经营项目预警表列表
    对应原 PROJECTWARNINGHelper.GetPROJECTWARNINGList
    含 DealMark 审批待办标记 + SourcePlatform(minProgram) 分组去重
    """
    conditions = ["PROJECTWARNING_STATE > 0"]

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

        # PROJECTWARNING_STATES IN 查询
        states = sp.get("PROJECTWARNING_STATES")
        if states and str(states).strip():
            conditions.append(f"PROJECTWARNING_STATE IN ({states})")

        # SERVERPART_IDS IN 查询
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            conditions.append(f"SERVERPART_ID IN ({sp_ids})")

        # WARNING_DATE 日期范围
        wd_start = sp.get("WARNING_DATE_Start")
        if wd_start and str(wd_start).strip():
            try:
                d = datetime.strptime(str(wd_start).split(" ")[0], "%Y/%m/%d" if "/" in str(wd_start) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(WARNING_DATE,1,8) >= {d.strftime('%Y%m%d')}")
            except Exception:
                pass

        wd_end = sp.get("WARNING_DATE_End")
        if wd_end and str(wd_end).strip():
            try:
                d = datetime.strptime(str(wd_end).split(" ")[0], "%Y/%m/%d" if "/" in str(wd_end) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(WARNING_DATE,1,8) <= {d.strftime('%Y%m%d')}")
            except Exception:
                pass

    where_sql = " WHERE " + " AND ".join(conditions) if conditions else ""

    # SourcePlatform == minProgram 时使用分组去重（C# L72-84）
    if source_platform == "minProgram":
        sql = f"""SELECT PROJECTWARNING_ID, BUSINESSPROJECTSPLIT_ID, BUSINESSPROJECT_NAME,
                SHOPROYALTY_ID, SERVERPART_ID, SERVERPART_NAME, SERVERPARTSHOP_NAME,
                BUSINESS_TYPE, STARTDATE, ENDDATE, MINTURNOVER, ROYALTY_PRICE, ROYALTY_CRATE,
                EXPIREDAYS, WARNING_DATE, PROJECTWARNING_STATE, RECORD_DATE,
                PROJECTWARNING_DESC, SWITCH_DATE, EXPENSE_AMOUNT,
                ROW_NUMBER() OVER (PARTITION BY SHOPROYALTY_ID ORDER BY WARNING_DATE DESC) AS COLNUM
            FROM {TABLE_NAME}{where_sql}"""
        all_rows = db.execute_query(sql)
        rows = [r for r in all_rows if r.get("COLNUM") == 1]
    else:
        rows = db.execute_query(f"SELECT * FROM {TABLE_NAME}{where_sql}")

    # DealMark 审批待办标记（C# L91-114）
    for r in rows:
        r["DealMark"] = 1  # 默认已办
        state = int(r.get("PROJECTWARNING_STATE", 0) or 0)
        # 经管部审批权限
        if "f0889950-f98a-40de-a369-613efeed2579" in module_guid:
            if state == 1000:
                r["DealMark"] = 0  # 待办
        # 财务部审批权限
        if "c021bbca-3c0a-478d-81e7-87e81ef80e05" in module_guid:
            if state == 2000:
                r["DealMark"] = 0  # 待办

    # 关键字过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            search_value = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(search_value in str(r.get(k, "")) for k in keys)]

    # 排序
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "desc" in (search_model.SortStr or "").lower()
        try:
            rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)
        except Exception:
            pass

    total_count = len(rows)

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    # C# TranslateDateTime: int 日期→格式化字符串
    for r in rows:
        format_row_dates(r, DATE_FIELDS, DATETIME_FIELDS)
    return int(total_count), rows


# ========== 2. GetPROJECTWARNINGDetail ==========

def get_projectwarning_detail(db: DatabaseHelper, pw_id: int) -> Optional[dict]:
    """
    获取经营项目预警表明细
    对应原 PROJECTWARNINGHelper.GetPROJECTWARNINGDetail — 四表 JOIN
    T_PROJECTWARNING + T_SHOPROYALTY + T_REGISTERCOMPACT + T_REGISTERCOMPACTSUB
    """
    sql = f"""SELECT A.*, B.GUARANTEERATIO,
                C.SECONDPART_LINKMAN, C.SECONDPART_MOBILE,
                C.COMPACT_STARTDATE, C.COMPACT_ENDDATE,
                D.BUSINESS_BRAND
            FROM T_PROJECTWARNING A, T_SHOPROYALTY B,
                T_REGISTERCOMPACT C, T_REGISTERCOMPACTSUB D
            WHERE A.SHOPROYALTY_ID = B.SHOPROYALTY_ID
                AND B.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
                AND C.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
                AND A.{PRIMARY_KEY} = {pw_id}"""
    rows = db.execute_query(sql)
    if not rows:
        # 回退到单表查询
        rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {pw_id}")
        if not rows:
            return None
        return rows[0]
    r = rows[0]
    # 担保比例计算（C# L302-316）
    guarantee = r.get("GUARANTEERATIO")
    if guarantee is not None and str(guarantee).strip():
        g = float(guarantee)
        r["ROYALTY_CRATE"] = int(g * 100)
        r["MerchantRatio"] = f"{g}:{100 - g}"
    elif str(r.get("BUSINESS_TYPE", "")) == "2000":
        r["ROYALTY_CRATE"] = 500
        r["MerchantRatio"] = "5:95"
    # 商户联系人（C# L317-319）
    r["COOPMERCHANTS_LINKMAN"] = r.get("SECONDPART_LINKMAN", "")
    r["COOPMERCHANTS_MOBILEPHONE"] = r.get("SECONDPART_MOBILE", "")
    # 合同周期（C# L321-330）
    for dt_field in ("COMPACT_STARTDATE", "COMPACT_ENDDATE"):
        val = r.get(dt_field)
        if val and str(val).strip():
            try:
                from datetime import datetime as _dt
                r[dt_field] = _dt.strptime(str(val).split(" ")[0], "%Y-%m-%d").strftime("%Y/%m/%d")
            except Exception:
                pass
    # 品牌图标（C# L333-341，简化版：仅查品牌名）
    brand_id = r.get("BUSINESS_BRAND")
    if brand_id and str(brand_id).strip():
        try:
            brand = db.execute_query(f"SELECT BRAND_INTRO FROM T_BRAND WHERE BRAND_ID = {brand_id}")
            if brand and brand[0].get("BRAND_INTRO"):
                r["BUSINESSPROJECT_ICO"] = brand[0]["BRAND_INTRO"]
        except Exception:
            pass
    # 审批待办标记
    r["DealMark"] = 1
    # C# TranslateDateTime: int 日期→格式化字符串
    format_row_dates(r, DATE_FIELDS, DATETIME_FIELDS)
    return r


# ========== 3. SynchroPROJECTWARNING ==========

def synchro_projectwarning(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步经营项目预警表（新增或更新）
    对应原 PROJECTWARNINGHelper.SynchroPROJECTWARNING
    排除字段: SERVERPART_IDS 等 11 个
    日期字段: STARTDATE, ENDDATE, WARNING_DATE（存为 yyyyMMdd 数字）
    """
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    def _format_date_value(val):
        """将日期字符串转为 yyyyMMdd 数字"""
        if val is None:
            return None
        s = str(val).strip()
        if not s:
            return None
        try:
            dt = datetime.strptime(s.split(" ")[0], "%Y/%m/%d" if "/" in s else "%Y-%m-%d")
            return dt.strftime("%Y%m%d")
        except Exception:
            return s  # 已经是数字格式

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
                fv = _format_date_value(value)
                set_parts.append(f"{key} = {fv}" if fv else f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_PROJECTWARNING.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        data[PRIMARY_KEY] = new_id
        db_data[PRIMARY_KEY] = new_id

        columns = []
        values = []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if key in DATE_FIELDS:
                fv = _format_date_value(value)
                values.append(str(fv) if fv else "NULL")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    return True, data


# ========== 4. DeletePROJECTWARNING ==========

def delete_projectwarning(db: DatabaseHelper, pw_id: int) -> bool:
    """
    删除经营项目预警表（软删除 PROJECTWARNING_STATE = 0）
    对应原 PROJECTWARNINGHelper.DeletePROJECTWARNING
    """
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {pw_id}")
    if check == 0:
        return False
    affected = db.execute_non_query(
        f"UPDATE {TABLE_NAME} SET PROJECTWARNING_STATE = 0 WHERE {PRIMARY_KEY} = {pw_id}")
    return affected > 0
