from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营商户业务服务
替代原 COOPMERCHANTSHelper.cs，保持相同的业务逻辑
对应 MerchantsController 中 COOPMERCHANTS 相关 4 个接口
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_COOPMERCHANTS"
PRIMARY_KEY = "COOPMERCHANTS_ID"

# Synchro 时需排除的字段（查询条件字段或非数据库列）
EXCLUDE_FIELDS = {"SERVERPART_IDS", "SERVERPART_CODES", "BrandList",
                  "LINKER_NAME", "LINKER_MOBILEPHONE",
                  "current", "pageSize", "total"}

# 前端搜索参数中需跳过的非数据库字段
SEARCH_PARAM_SKIP_FIELDS = {"current", "pageSize", "total",
                             "BrandList", "LINKER_NAME", "LINKER_MOBILEPHONE"}

# 日期字段（需要 TO_DATE 处理）
DATE_FIELDS = {"OPERATE_DATE"}


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """根据查询参数构建通用 WHERE 条件"""
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS or key in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
    return " AND ".join(conditions)


# ========== 1. GetCoopMerchantsList ==========

def get_coopmerchants_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """
    获取经营商户列表
    对应原 COOPMERCHANTSHelper.GetCOOPMERCHANTSList
    SQL: SELECT * FROM T_COOPMERCHANTS {WhereSQL}
    默认排序: OPERATE_DATE desc
    关联查询: 从 T_COOPMERCHANTS_LINKER 获取第一条联系人信息 (LINKER_NAME, LINKER_MOBILEPHONE)
    """
    where_sql = ""

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_sql = " WHERE " + where_clause

    # 执行查询
    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"
    rows = db.execute_query(base_sql)

    # 关键字过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            search_value = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(
                search_value in str(r.get(k, "")) for k in keys
            )]

    # 排序（默认 OPERATE_DATE desc）
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field) or "", reverse=is_desc)
    else:
        rows.sort(key=lambda x: x.get("OPERATE_DATE") or "", reverse=True)

    # 总数
    total_count = len(rows)

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    # 关联查询: 从 T_COOPMERCHANTS_LINKER 获取联系人信息
    # 原 C# 中对每条商户查询其联系人(只取第一条)
    if rows:
        ids = [str(r.get("COOPMERCHANTS_ID", 0)) for r in rows if r.get("COOPMERCHANTS_ID")]
        if ids:
            linker_sql = f"SELECT * FROM T_COOPMERCHANTS_LINKER WHERE COOPMERCHANTS_ID IN ({','.join(ids)}) ORDER BY OPERATE_DATE DESC"
            linkers = db.execute_query(linker_sql)
            # 按商户ID分组，取第一条
            linker_map = {}
            for lk in linkers:
                mid = lk.get("COOPMERCHANTS_ID")
                if mid not in linker_map:
                    linker_map[mid] = lk

            for row in rows:
                mid = row.get("COOPMERCHANTS_ID")
                lk = linker_map.get(mid)
                if lk:
                    row["LINKER_NAME"] = lk.get("LINKER_NAME", "")
                    # 优先手机号，无则用座机
                    mobile = lk.get("LINKER_MOBILEPHONE", "")
                    tel = lk.get("LINKER_TELEPHONE", "")
                    row["LINKER_MOBILEPHONE"] = mobile if mobile and str(mobile).strip() else (
                        tel if tel and str(tel).strip() else "")
                else:
                    row["LINKER_NAME"] = None
                    row["LINKER_MOBILEPHONE"] = None

    return int(total_count), rows


# ========== 2. GetCoopMerchantsDetail ==========

def get_coopmerchants_detail(db: DatabaseHelper, coopmerchants_id: int) -> Optional[dict]:
    """
    获取经营商户明细
    对应原 COOPMERCHANTSHelper.GetCOOPMERCHANTSDetail
    额外返回 BrandList: 从 T_RTCOOPMERCHANTS + T_BRAND 获取品牌列表
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {coopmerchants_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    detail = rows[0]

    # 品牌列表 - 原 C# SQL:
    # SELECT B.BRAND_ID, B.BRAND_INDEX, B.BRAND_NAME, B.BRAND_INTRO
    # FROM COOP_MERCHANT.T_RTCOOPMERCHANTS A, COOP_MERCHANT.T_BRAND B
    # WHERE A.BUSINESS_BRAND = B.BRAND_ID AND A.COOPMERCHANTS_ID = {id}
    brand_sql = f"""SELECT B.BRAND_ID, B.BRAND_INDEX, B.BRAND_NAME, B.BRAND_INTRO
        FROM T_RTCOOPMERCHANTS A, T_BRAND B
        WHERE A.BUSINESS_BRAND = B.BRAND_ID AND A.COOPMERCHANTS_ID = {coopmerchants_id}
        ORDER BY B.BRAND_INDEX, B.BRAND_ID"""
    brand_rows = db.execute_query(brand_sql)
    brand_list = []
    for br in brand_rows:
        brand_item = {
            "label": br.get("BRAND_NAME", ""),
            "value": br.get("BRAND_ID"),
            "ico": br.get("BRAND_INTRO", "")
        }
        brand_list.append(brand_item)
    detail["BrandList"] = brand_list

    return detail


# ========== 3. SynchroCoopMerchants ==========

def synchro_coopmerchants(db: DatabaseHelper, data: dict) -> tuple[bool, dict, str]:
    """
    同步经营商户（新增或更新）
    对应原 COOPMERCHANTSHelper.SynchroCOOPMERCHANTS
    唯一性校验: COOPMERCHANTS_NAME 在同省份(PROVINCE_CODE)下不能重复
    """
    record_id = data.get(PRIMARY_KEY)
    coopmerchants_name = data.get("COOPMERCHANTS_NAME", "")
    province_code = data.get("PROVINCE_CODE")

    # 唯一性校验
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE COOPMERCHANTS_STATE = 1 AND COOPMERCHANTS_NAME = '{coopmerchants_name}'"
    if record_id is not None:
        check_sql += f" AND COOPMERCHANTS_ID <> {record_id}"
    if province_code is not None:
        check_sql += f" AND PROVINCE_CODE = {province_code}"
    dup_count = db.execute_scalar(check_sql)
    if dup_count and int(dup_count) > 0:
        return False, data, "商户信息已存在，请勿重复录入！"

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    if record_id is not None:
        # === 更新模式 ===
        exist_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}"
        count = db.execute_scalar(exist_sql)
        if count == 0:
            return False, data, "更新失败，数据不存在！"

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                if key in DATE_FIELDS:
                    set_parts.append(f"{key} = NULL")
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
            new_id = db.execute_scalar("SELECT SEQ_COOPMERCHANTS.NEXTVAL FROM DUAL")
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

    return True, data, ""


# ========== 4. DeleteCoopMerchants ==========

def delete_coopmerchants(db: DatabaseHelper, coopmerchants_id: int) -> bool:
    """
    删除经营商户（软删除: COOPMERCHANTS_STATE = 0）
    对应原 COOPMERCHANTSHelper.DeleteCOOPMERCHANTS
    """
    sql = f"UPDATE {TABLE_NAME} SET COOPMERCHANTS_STATE = 0 WHERE {PRIMARY_KEY} = {coopmerchants_id}"
    affected = db.execute_non_query(sql)
    return affected > 0
