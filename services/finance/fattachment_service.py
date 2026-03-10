from __future__ import annotations
# -*- coding: utf-8 -*-
"""
附件上传（Finance ATTACHMENT）业务服务
替代原 FATTACHMENTHelper.cs，保持相同的业务逻辑
对应 FinanceController 中 ATTACHMENT 相关 4 个接口

特殊逻辑：
- DataType=0 查 RUNNING 表（T_ATTACHMENT），DataType=1 查 STORAGE 表（CONTRACT_STORAGE.T_ATTACHMENT）
- 达梦中只有一张 T_ATTACHMENT 表，对应 RUNNING
- Synchro 仅操作 RUNNING 表
- Delete 为真删除
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper


# RUNNING 表名（DataType=0）
TABLE_RUNNING = "T_F_ATTACHMENT_RUNNING"
# STORAGE 表名（DataType=1）
TABLE_STORAGE = "T_F_ATTACHMENT_STORAGE"

PRIMARY_KEY = "ATTACHMENT_ID"

# 日期字段
DATE_FIELDS = {"CREATEDATE"}


def _get_table_name(data_type: int) -> str:
    """根据 DataType 返回表名：0=RUNNING, 1=STORAGE"""
    if data_type == 1:
        return TABLE_STORAGE
    return TABLE_RUNNING


# 字符串字段（C# .ToString() 将 null 转为空字符串）
STRING_FIELDS = {"ATTACHMENT_NAME", "ATTACHMENT_DESC", "PRESONNAME", "OTHER_NAME"}


def _convert_row(row: dict) -> dict:
    """转换单行数据：字符串字段 null→空字符串（匹配 C# .ToString() 行为）"""
    for field in STRING_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    return row


# ========== 1. GetATTACHMENTList ==========

def get_attachment_list(db: DatabaseHelper, finance_proinst_id: int, data_type: int) -> list[dict]:
    """
    获取附件上传列表
    对应原 FATTACHMENTHelper.GetATTACHMENTList（行23-53）
    SQL: SELECT * FROM T_ATTACHMENT [WHERE PROINST_ID = ?]
    """
    table_name = _get_table_name(data_type)
    where_sql = ""
    if finance_proinst_id is not None and finance_proinst_id != 0:
        where_sql = f" WHERE PROINST_ID = {finance_proinst_id}"

    sql = f"SELECT * FROM {table_name}{where_sql}"
    rows = db.execute_query(sql)
    return [_convert_row(r) for r in rows]


# ========== 2. GetATTACHMENTDetail ==========

def get_attachment_detail(db: DatabaseHelper, attachment_id: int, data_type: int) -> Optional[dict]:
    """
    获取附件上传明细
    对应原 FATTACHMENTHelper.GetATTACHMENTDetail（行91-127）
    SQL: SELECT * FROM T_ATTACHMENT WHERE ATTACHMENT_ID = ?
    """
    table_name = _get_table_name(data_type)
    sql = f"SELECT * FROM {table_name} WHERE {PRIMARY_KEY} = {attachment_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None
    # Detail 不做空值转换（C# Detail 直接赋值 Model 属性，null 保持 null）
    return rows[0]


# ========== 3. SynchroATTACHMENT ==========

def synchro_attachment(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步附件上传（新增或更新）——仅操作 RUNNING 表
    对应原 FATTACHMENTHelper.SynchroATTACHMENT（行136-161）
    """
    record_id = data.get(PRIMARY_KEY)

    if record_id is not None:
        # === 更新模式 ===
        check_sql = f"SELECT COUNT(*) FROM {TABLE_RUNNING} WHERE {PRIMARY_KEY} = {record_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, data

        set_parts = []
        for key, value in data.items():
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
            update_sql = f"UPDATE {TABLE_RUNNING} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}"
            db.execute_non_query(update_sql)
    else:
        # === 新增模式 ===
        try:
            new_id = db.execute_scalar("SELECT SEQ_ATTACHMENT.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_RUNNING}") or 0) + 1
        data[PRIMARY_KEY] = new_id

        columns = []
        values = []
        for key, value in data.items():
            if value is None:
                continue
            columns.append(key)
            if key in DATE_FIELDS:
                values.append(f"TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        insert_sql = f"INSERT INTO {TABLE_RUNNING} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. DeleteATTACHMENT ==========

def delete_attachment(db: DatabaseHelper, attachment_id: int) -> bool:
    """
    删除附件上传——真删除，仅操作 RUNNING 表
    对应原 FATTACHMENTHelper.DeleteATTACHMENT（行188-204）
    原 C# 代码: _ATTACHMENT.Delete()（真删除）
    """
    # 先检查记录是否存在
    check_sql = f"SELECT COUNT(*) FROM {TABLE_RUNNING} WHERE {PRIMARY_KEY} = {attachment_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    sql = f"DELETE FROM {TABLE_RUNNING} WHERE {PRIMARY_KEY} = {attachment_id}"
    affected = db.execute_non_query(sql)
    return affected > 0
