from __future__ import annotations
# -*- coding: utf-8 -*-
"""
物业资产与商户对照表业务服务
替代原 PROPERTYSHOPHelper.cs，保持相同的业务逻辑
对应 BaseInfoController 中 PROPERTYSHOP 相关 5 个接口

接口：GetList、GetDetail（含关联 ServerpartShop）、Synchro（校验+日志）、Batch、Delete（软删除+日志）
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# 表名常量
TABLE_NAME = "T_PROPERTYSHOP"
PRIMARY_KEY = "PROPERTYSHOP_ID"

# Synchro 时排除的字段（查询条件字段，非数据库列）
EXCLUDE_FIELDS = {
    "SERVERPART_IDS", "PROPERTYASSETS_IDS", "SERVERPARTSHOP_IDS",
    "STARTDATE_Start", "STARTDATE_End", "ENDDATE_Start", "ENDDATE_End",
    "PROPERTYSHOP_STATE",  # PROPERTYSHOP_STATE 在 GetList WHERE 中做特殊处理
    "ServerpartShop",  # Detail 关联对象，不入库
}

# 日期字段（TIMESTAMP 类型，需 TO_DATE 处理）
DATE_FIELDS = {"CREATE_DATE", "OPERATE_DATE"}

# STARTDATE / ENDDATE 是 NUMBER 类型（yyyyMMdd 整数），不是 DATE
NUMBER_DATE_FIELDS = {"STARTDATE", "ENDDATE"}


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """根据查询参数构建通用 WHERE 条件"""
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS or key in NUMBER_DATE_FIELDS:
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


# ========== 1. GetPROPERTYSHOPList ==========

def get_propertyshop_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取物业资产与商户对照表列表
    对应原 PROPERTYSHOPHelper.GetPROPERTYSHOPList（L26-128）

    特殊逻辑：
    - SERVERPART_IDS、PROPERTYASSETS_IDS、SERVERPARTSHOP_IDS → IN 查询
    - PROPERTYSHOP_STATE 为 null 时默认 != 0
    - STARTDATE_Start/End、ENDDATE_Start/End → 范围查询（NUMBER 比较）
    """
    where_parts = []

    if search_model.SearchParameter:
        sp = search_model.SearchParameter

        # 通用 WHERE 条件
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)
        if where_clause:
            where_parts.append(where_clause)

        # SERVERPART_IDS → IN 查询
        server_ids = sp.get("SERVERPART_IDS")
        if server_ids and str(server_ids).strip():
            ids = ",".join(str(server_ids).split(","))
            where_parts.append(f"SERVERPART_ID IN ({ids})")

        # PROPERTYASSETS_IDS → IN 查询
        assets_ids = sp.get("PROPERTYASSETS_IDS")
        if assets_ids and str(assets_ids).strip():
            ids = ",".join(str(assets_ids).split(","))
            where_parts.append(f"PROPERTYASSETS_ID IN ({ids})")

        # SERVERPARTSHOP_IDS → IN 查询
        shop_ids = sp.get("SERVERPARTSHOP_IDS")
        if shop_ids and str(shop_ids).strip():
            ids = ",".join(str(shop_ids).split(","))
            where_parts.append(f"SERVERPARTSHOP_ID IN ({ids})")

        # PROPERTYSHOP_STATE 特殊处理：null 时默认 != 0
        state = sp.get("PROPERTYSHOP_STATE")
        if state is None:
            where_parts.append("PROPERTYSHOP_STATE != 0")
        else:
            where_parts.append(f"PROPERTYSHOP_STATE = {state}")

        # 日期范围查询（STARTDATE 和 ENDDATE 是 NUMBER 类型 yyyyMMdd）
        for date_field, param_prefix in [("STARTDATE", "STARTDATE"), ("ENDDATE", "ENDDATE")]:
            start_val = sp.get(f"{param_prefix}_Start")
            if start_val and str(start_val).strip():
                try:
                    dt = datetime.strptime(str(start_val).strip()[:10], "%Y-%m-%d")
                    where_parts.append(f"{date_field} >= {dt.strftime('%Y%m%d')}")
                except Exception:
                    where_parts.append(f"{date_field} >= {start_val}")
            end_val = sp.get(f"{param_prefix}_End")
            if end_val and str(end_val).strip():
                try:
                    dt = datetime.strptime(str(end_val).strip()[:10], "%Y-%m-%d")
                    where_parts.append(f"{date_field} <= {dt.strftime('%Y%m%d')}")
                except Exception:
                    where_parts.append(f"{date_field} <= {end_val}")
    else:
        # SearchParameter 为 null 时，原 C# 不加任何过滤（直接 SELECT * FROM T_PROPERTYSHOP）
        pass

    where_sql = ""
    if where_parts:
        where_sql = " WHERE " + " AND ".join(where_parts)

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

    # 排序
    if search_model.SortStr:
        sort_field = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").strip()
        is_desc = "DESC" in (search_model.SortStr or "").upper()
        rows.sort(key=lambda x: x.get(sort_field, 0) or 0, reverse=is_desc)

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

    return int(total_count), rows


# ========== 2. GetPROPERTYSHOPDetail ==========

def get_propertyshop_detail(db: DatabaseHelper, propertyshop_id: int) -> Optional[dict]:
    """
    获取物业资产与商户对照表明细（含关联门店信息）
    对应原 PROPERTYSHOPHelper.GetPROPERTYSHOPDetail（L200-222）

    逻辑：查主表 + 如果 SERVERPARTSHOP_ID > 0，关联查 T_SERVERPARTSHOP 填充 ServerpartShop
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {propertyshop_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None

    detail = rows[0]

    # 关联查门店信息
    shop_id = detail.get("SERVERPARTSHOP_ID")
    if shop_id and int(shop_id) > 0:
        shop_sql = f"SELECT * FROM T_SERVERPARTSHOP WHERE SERVERPARTSHOP_ID = {shop_id}"
        shop_rows = db.execute_query(shop_sql)
        if shop_rows:
            detail["ServerpartShop"] = shop_rows[0]
        else:
            detail["ServerpartShop"] = None
    else:
        detail["ServerpartShop"] = None

    return detail


# ========== 3. SynchroPROPERTYSHOP ==========

def synchro_propertyshop(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步物业资产与商户对照表（新增或更新）
    对应原 PROPERTYSHOPHelper.SynchroPROPERTYSHOP（L260-438）

    逻辑：
    1. 校验 SERVERPARTSHOP_ID 和 PROPERTYASSETS_ID 必传
    2. 检查门店状态：门店已关闭(3000)则状态改为历史(2)
    3. 更新模式：按 PROPERTYSHOP_ID 查找并更新
    4. 新增模式：先查重(PROPERTYASSETS_ID+SERVERPARTSHOP_ID)，存在则先软删除再新增
    5. 记录操作日志到 T_PROPERTYASSETSLOG
    """
    shop_id = data.get("SERVERPARTSHOP_ID")
    assets_id = data.get("PROPERTYASSETS_ID")

    if shop_id is None or assets_id is None:
        return False, "必填参数不能为空"

    # 检查门店状态
    shop_sql = f"SELECT BUSINESS_STATE FROM T_SERVERPARTSHOP WHERE SERVERPARTSHOP_ID = {shop_id}"
    shop_rows = db.execute_query(shop_sql)
    if not shop_rows:
        return False, "服务区门店Id不正确"

    business_state = shop_rows[0].get("BUSINESS_STATE")
    prop_state = data.get("PROPERTYSHOP_STATE")
    if prop_state == 1 and business_state == 3000:
        data["PROPERTYSHOP_STATE"] = 2

    data["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}

    record_id = data.get(PRIMARY_KEY)

    if record_id is not None:
        # === 更新模式 ===
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, "操作记录不存在"

        # 保留原来的创建人信息
        ori_sql = f"SELECT STAFF_ID, STAFF_NAME FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}"
        ori_rows = db.execute_query(ori_sql)
        if ori_rows:
            data["STAFF_ID"] = ori_rows[0].get("STAFF_ID")
            data["STAFF_NAME"] = ori_rows[0].get("STAFF_NAME")
            db_data["STAFF_ID"] = data["STAFF_ID"]
            db_data["STAFF_NAME"] = data["STAFF_NAME"]

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                if key in DATE_FIELDS:
                    set_parts.append(f"{key} = NULL")
                continue
            if key in DATE_FIELDS:
                set_parts.append(f"{key} = TO_DATE('{value}', 'YYYY-MM-DD HH24:MI:SS')")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # === 新增模式 ===
        # 查重：PROPERTYASSETS_ID + SERVERPARTSHOP_ID（有效状态）
        dup_sql = (
            f"SELECT {PRIMARY_KEY}, PROPERTYASSETS_ID FROM {TABLE_NAME} "
            f"WHERE PROPERTYSHOP_STATE != 0 AND PROPERTYASSETS_ID = {assets_id} "
            f"AND SERVERPARTSHOP_ID = {shop_id}"
        )
        dup_rows = db.execute_query(dup_sql)
        if dup_rows:
            # 存在有效记录，先软删除
            old_id = dup_rows[0].get("PROPERTYASSETS_ID")
            old_shop_id = dup_rows[0].get(PRIMARY_KEY)
            op_id = data.get("OPERATOR_ID", 0)
            op_name = data.get("OPERATOR_NAME", "")
            del_sql = (
                f"UPDATE {TABLE_NAME} SET PROPERTYSHOP_STATE = 0, "
                f"OPERATOR_ID = '{op_id}', OPERATOR_NAME = '{op_name}' "
                f"WHERE PROPERTYSHOP_STATE != 0 AND PROPERTYASSETS_ID = {assets_id} "
                f"AND SERVERPARTSHOP_ID = {shop_id}"
            )
            db.execute_non_query(del_sql)

        # 获取新 ID
        try:
            new_id = db.execute_scalar("SELECT SEQ_PROPERTYSHOP.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        data[PRIMARY_KEY] = new_id
        db_data[PRIMARY_KEY] = new_id
        data["CREATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_data["CREATE_DATE"] = data["CREATE_DATE"]

        columns = []
        values = []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if key in DATE_FIELDS:
                values.append(f"TO_DATE('{value}', 'YYYY-MM-DD HH24:MI:SS')")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. BatchPROPERTYSHOP ==========

def batch_propertyshop(db: DatabaseHelper, model_list: list) -> tuple:
    """
    批量同步物业资产与商户对照表
    对应原 BaseInfoController.BatchPROPERTYSHOP（L2612-2653）

    逻辑：遍历列表，逐个调用 synchro_propertyshop
    """
    for model in model_list:
        success, result = synchro_propertyshop(db, model)
        if not success:
            msg = result if isinstance(result, str) else "更新失败，数据不存在！"
            return False, msg
        # 回填 PROPERTYSHOP_ID
        if isinstance(result, dict):
            model[PRIMARY_KEY] = result.get(PRIMARY_KEY)
    return True, model_list


# ========== 5. DeletePROPERTYSHOP ==========

def delete_propertyshop(db: DatabaseHelper,
                        propertyassets_id: int,
                        propertyshop_id: int = None,
                        serverpartshop_id: int = None,
                        operate_id: int = 0,
                        operate_name: str = "") -> tuple:
    """
    删除物业资产与商户对照表（软删除 PROPERTYSHOP_STATE=0）
    对应原 PROPERTYSHOPHelper.DeletePROPERTYSHOP（L455-495）

    入参对应 BaseOperateModel: Id=PROPERTYASSETS_ID, RelatedId=PROPERTYSHOP_ID, ShopId=SERVERPARTSHOP_ID
    """
    if not propertyassets_id or propertyassets_id == 0:
        return False, "资产内码不能为空"

    where_parts = [f"PROPERTYASSETS_ID = {propertyassets_id}"]

    if propertyshop_id and propertyshop_id > 0:
        where_parts.append(f"PROPERTYSHOP_ID = {propertyshop_id}")

    if serverpartshop_id and serverpartshop_id > 0:
        where_parts.append(f"SERVERPARTSHOP_ID = {serverpartshop_id}")

    # 默认只删除有效和历史记录（状态 != 0）
    where_parts.append("PROPERTYSHOP_STATE != 0")

    where_sql = " WHERE " + " AND ".join(where_parts)

    sql = (
        f"UPDATE {TABLE_NAME} SET PROPERTYSHOP_STATE = 0, "
        f"OPERATOR_ID = '{operate_id}', OPERATOR_NAME = '{operate_name}'"
        f"{where_sql}"
    )
    affected = db.execute_non_query(sql)

    if affected and affected > 0:
        # 记录操作日志
        try:
            log_sql = (
                f"INSERT INTO T_PROPERTYASSETSLOG "
                f"(PROPERTYASSETSLOG_ID, TABLE_NAME, TABLE_ID, CHANGE_TYPE, "
                f"OPERATE_DATE, OPERATE_DESC, OPERATE_TYPE, OPERATE_VALUE, OPERATE_NEWVALUE, "
                f"OPERATE_ID, OPERATE_NAME) VALUES ("
                f"(SELECT COALESCE(MAX(PROPERTYASSETSLOG_ID), 0) + 1 FROM T_PROPERTYASSETSLOG), "
                f"'T_PROPERTYSHOP', '{propertyassets_id}', '2', SYSDATE, "
                f"'状态:[有效]改为[无效]，', '修改', "
                f"'{{\"PROPERTYSHOP_STATE\":\"有效\"}}', '{{\"PROPERTYSHOP_STATE\":\"无效\"}}', "
                f"'{operate_id}', '{operate_name}')"
            )
            db.execute_non_query(log_sql)
        except Exception as e:
            logger.warning(f"记录操作日志失败: {e}")
        return True, "删除成功"
    else:
        return False, "删除失败，数据不存在！"
