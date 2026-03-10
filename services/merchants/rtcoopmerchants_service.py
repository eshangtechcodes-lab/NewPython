from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营商户品牌关联 / 业态品牌商户业务服务
替代原 RTCOOPMERCHANTSHelper.cs
对应 MerchantsController 中 RTCoopMerchants / TradeBrandMerchants 相关 4 个接口
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_RTCOOPMERCHANTS"
PRIMARY_KEY = "RTCOOPMERCHANTS_ID"

# 日期字段
DATE_FIELDS = {"OPERATE_DATE"}
# 非数据库字段
EXCLUDE_FIELDS = {"current", "pageSize", "total",
                  "BUSINESSTRADE_NAME", "BRAND_NAME", "BRAND_ICO",
                  "COOPMERCHANTS_NAME", "OWNERUNIT_NAME",
                  "COOPMERCHANTS_LINKMAN", "COOPMERCHANTS_TELEPHONE",
                  "COOPMERCHANTS_MOBILEPHONE"}


# ========== 1. GetRTCoopMerchantsList ==========

def get_rtcoopmerchants_list(db: DatabaseHelper, coopmerchants_id: int, sort_str: str = "") -> tuple[int, list[dict]]:
    """
    获取经营商户品牌关联列表
    对应原 RTCOOPMERCHANTSHelper.GetRTCOOPMERCHANTSList
    SQL: SELECT * FROM T_RTCOOPMERCHANTS WHERE COOPMERCHANTS_ID = {id}
    附加: 从 T_AUTOSTATISTICS 获取业态名称，从 T_BRAND 获取品牌名称+图标
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE COOPMERCHANTS_ID = {coopmerchants_id}"
    rows = db.execute_query(sql)

    # 排序
    if sort_str:
        sort_field = sort_str.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "DESC" in sort_str.upper()
        rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)

    total_count = len(rows)

    # 附加关联信息: 业态名称、品牌名称/图标
    for row in rows:
        # 查询经营业态名称
        trade_id = row.get("BUSINESS_TRADE")
        if trade_id:
            trade_sql = f"SELECT AUTOSTATISTICS_NAME FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_ID = {trade_id}"
            trade_rows = db.execute_query(trade_sql)
            row["BUSINESSTRADE_NAME"] = trade_rows[0]["AUTOSTATISTICS_NAME"] if trade_rows else None
        else:
            row["BUSINESSTRADE_NAME"] = None

        # 查询经营品牌信息
        brand_id = row.get("BUSINESS_BRAND")
        if brand_id:
            brand_sql = f"SELECT BRAND_NAME, BRAND_INTRO FROM T_BRAND WHERE BRAND_ID = {brand_id}"
            brand_rows = db.execute_query(brand_sql)
            if brand_rows:
                row["BRAND_NAME"] = brand_rows[0]["BRAND_NAME"]
                row["BRAND_ICO"] = brand_rows[0].get("BRAND_INTRO", "")
            else:
                row["BRAND_NAME"] = None
                row["BRAND_ICO"] = None
        else:
            row["BRAND_NAME"] = None
            row["BRAND_ICO"] = None

    return int(total_count), rows


# ========== 2. GetTradeBrandMerchantsList ==========

def get_tradebrand_merchants_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取经营业态品牌下商户列表
    对应原 RTCOOPMERCHANTSHelper.GetTradeBrandMerchantsList
    使用 UNION ALL SQL:
      (有品牌关联的商户) UNION ALL (无品牌关联的商户)
    C# 中 PROVINCE_CODE 通过 GetWhereSQL 应用到外层 WHERE
    """
    province_code = None
    where_parts = []
    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        province_code = sp.get("PROVINCE_CODE")
        for key, value in sp.items():
            if key in EXCLUDE_FIELDS:
                continue
            if value is None or (isinstance(value, str) and value.strip() == ""):
                continue
            # C# GetWhereSQL 把所有字段（含 PROVINCE_CODE）放到外层 WHERE
            if isinstance(value, str):
                where_parts.append(f"{key} = '{value}'")
            else:
                where_parts.append(f"{key} = {value}")

    where_sql = ""
    if where_parts:
        where_sql = " WHERE " + " AND ".join(where_parts)

    # 原 C# 中的 UNION ALL SQL
    # 第一段: 有品牌关联的商户
    first_sql = """SELECT A.COOPMERCHANTS_ID, A.COOPMERCHANTS_NAME, A.OWNERUNIT_ID, A.OWNERUNIT_NAME, A.PROVINCE_CODE,
            A.COOPMERCHANTS_LINKMAN, A.COOPMERCHANTS_TELEPHONE, A.COOPMERCHANTS_MOBILEPHONE,
            B.BUSINESS_TRADE AS BUSINESSTRADE_ID, D.AUTOSTATISTICS_NAME AS BUSINESSTRADE_NAME,
            B.BUSINESS_BRAND AS BRAND_ID, C.BRAND_NAME, B.RTCOOPMERCHANTS_ID
        FROM T_COOPMERCHANTS A, T_RTCOOPMERCHANTS B, T_BRAND C, T_AUTOSTATISTICS D
        WHERE A.COOPMERCHANTS_ID = B.COOPMERCHANTS_ID
            AND B.BUSINESS_TRADE = D.AUTOSTATISTICS_ID
            AND B.BUSINESS_BRAND = C.BRAND_ID
            AND A.COOPMERCHANTS_STATE = 1"""

    # 第二段: 无品牌关联的商户（需要 province_code）
    if province_code is not None:
        second_sql = f"""
        UNION ALL
        SELECT A.COOPMERCHANTS_ID, A.COOPMERCHANTS_NAME, A.OWNERUNIT_ID, A.OWNERUNIT_NAME, A.PROVINCE_CODE,
            A.COOPMERCHANTS_LINKMAN, A.COOPMERCHANTS_TELEPHONE, A.COOPMERCHANTS_MOBILEPHONE,
            NULL, NULL, NULL, NULL, A.COOPMERCHANTS_ID
        FROM T_COOPMERCHANTS A
        WHERE NOT EXISTS (SELECT 1 FROM T_RTCOOPMERCHANTS B WHERE A.COOPMERCHANTS_ID = B.COOPMERCHANTS_ID)
            AND A.PROVINCE_CODE = {province_code}
            AND A.COOPMERCHANTS_STATE = 1"""
    else:
        second_sql = ""

    union_sql = f"SELECT * FROM ({first_sql}{second_sql}){where_sql}"

    rows = db.execute_query(union_sql)

    # 关键字过滤
    if search_model.keyWord:
        if hasattr(search_model.keyWord, 'model_dump'):
            kw = search_model.keyWord.model_dump()
        else:
            kw = search_model.keyWord
        if kw.get("Key") and kw.get("Value"):
            search_value = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(
                search_value in str(r.get(k, "")) for k in keys
            )]

    # 排序
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)

    total_count = len(rows)

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    # 补充联系人信息：当 COOPMERCHANTS_LINKMAN 为空时从 T_COOPMERCHANTS_LINKER 获取
    linker_data = db.execute_query("SELECT * FROM T_COOPMERCHANTS_LINKER")
    linker_map = {}
    for lk in linker_data:
        mid = lk.get("COOPMERCHANTS_ID")
        if mid not in linker_map:
            linker_map[mid] = lk

    # C# BrandMerchantsModel field-by-field 绑定
    result_list = []
    for row in rows:
        model = {}
        model["RTCOOPMERCHANTS_ID"] = row.get("RTCOOPMERCHANTS_ID")
        model["COOPMERCHANTS_ID"] = row.get("COOPMERCHANTS_ID")
        model["COOPMERCHANTS_NAME"] = row.get("COOPMERCHANTS_NAME") or ""
        model["OWNERUNIT_ID"] = row.get("OWNERUNIT_ID")
        model["OWNERUNIT_NAME"] = row.get("OWNERUNIT_NAME") or ""
        model["PROVINCE_CODE"] = row.get("PROVINCE_CODE")
        # C#: 当 COOPMERCHANTS_LINKMAN 为空时从 LINKER 表补充
        linkman = row.get("COOPMERCHANTS_LINKMAN")
        if not linkman or str(linkman).strip() == "":
            lk = linker_map.get(row.get("COOPMERCHANTS_ID"))
            if lk:
                model["COOPMERCHANTS_LINKMAN"] = lk.get("LINKER_NAME") or ""
                model["COOPMERCHANTS_MOBILEPHONE"] = lk.get("LINKER_MOBILEPHONE") or ""
            else:
                model["COOPMERCHANTS_LINKMAN"] = None
                model["COOPMERCHANTS_MOBILEPHONE"] = None
        else:
            model["COOPMERCHANTS_LINKMAN"] = linkman or ""
            model["COOPMERCHANTS_MOBILEPHONE"] = row.get("COOPMERCHANTS_MOBILEPHONE") or ""
        model["BUSINESSTRADE_ID"] = row.get("BUSINESSTRADE_ID") or 0
        model["BUSINESSTRADE_NAME"] = row.get("BUSINESSTRADE_NAME") or ""
        model["BRAND_ID"] = row.get("BRAND_ID") or 0
        model["BRAND_NAME"] = row.get("BRAND_NAME") or ""
        result_list.append(model)

    return int(total_count), result_list


# ========== 3. SynchroRTCoopMerchants ==========

def synchro_rtcoopmerchants(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步经营商户品牌关联（新增或更新）
    对应原 RTCOOPMERCHANTSHelper.SynchroRTCOOPMERCHANTS
    """
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # === 更新模式 ===
        exist_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}"
        count = db.execute_scalar(exist_sql)
        if count == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if key in DATE_FIELDS:
                set_parts.append(f"{key} = TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # === 新增模式 ===
        try:
            new_id = db.execute_scalar("SELECT SEQ_RTCOOPMERCHANTS.NEXTVAL FROM DUAL")
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
                values.append(f"TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. DeleteRTCoopMerchants ==========

def delete_rtcoopmerchants(db: DatabaseHelper, rtcoopmerchants_id: int) -> bool:
    """
    删除经营商户品牌关联（真删除: DELETE）
    对应原 RTCOOPMERCHANTSHelper.DeleteRTCOOPMERCHANTS
    注意原 C# 始终返回 true
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {rtcoopmerchants_id}"
    count = db.execute_scalar(check_sql)
    if count and int(count) > 0:
        delete_sql = f"DELETE FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {rtcoopmerchants_id}"
        db.execute_non_query(delete_sql)
    return True
