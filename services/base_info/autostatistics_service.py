from __future__ import annotations
# -*- coding: utf-8 -*-
"""
自定义统计归口表业务服务
替代原 AUTOSTATISTICSHelper.cs 中通用的统计归口方法
与 BusinessTrade 共用 T_AUTOSTATISTICS 表，但不限定 AUTOSTATISTICS_TYPE
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper


# 表名常量
TABLE_NAME = "T_AUTOSTATISTICS"
PRIMARY_KEY = "AUTOSTATISTICS_ID"


def _process_row(row: dict) -> dict:
    """
    处理单行数据，与原 C# BindDataRowToModel 一致
    字符串字段 None → 空字符串，整数字段 None → 0
    """
    str_fields = ["AUTOSTATISTICS_NAME", "AUTOSTATISTICS_VALUE", "AUTOSTATISTICS_ICO",
                  "OWNERUNIT_NAME", "STAF_NAME", "AUTOSTATISTICS_DESC"]
    for field in str_fields:
        if field in row and row[field] is None:
            row[field] = ""

    int_fields = ["AUTOSTATISTICS_ID", "AUTOSTATISTICS_PID", "AUTOSTATISTICS_INDEX",
                  "AUTOSTATISTICS_TYPE", "STATISTICS_TYPE", "OWNERUNIT_ID",
                  "PROVINCE_CODE", "AUTOSTATISTICS_STATE", "STAFF_ID"]
    for field in int_fields:
        if field in row and row[field] is None:
            row[field] = 0

    return row


def get_autostatistics_tree_list(db: DatabaseHelper, autostatistics_pid: int = -1,
                                  province_code: int = None, ownerunit_id: int = None,
                                  autostatistics_type: int = None,
                                  autostatistics_state: int = None) -> tuple:
    """
    获取自定义统计归口树形列表
    对应原 AUTOSTATISTICSHelper.GetAutoStatisticsTreeList
    支持多种归口类型（1000=考核口径, 2000=经营业态, 2010=业态考核规则, 3000=考核部门, 4000=供应商类别）
    返回: (总数, 嵌套树列表)
    """
    # 构建 WHERE 条件（ProvinceCode 为必传参数）
    where_sql = f"WHERE PROVINCE_CODE = {province_code}"
    if autostatistics_type is not None:
        where_sql += f" AND AUTOSTATISTICS_TYPE = {autostatistics_type}"
    if ownerunit_id is not None:
        where_sql += f" AND OWNERUNIT_ID = {ownerunit_id}"
    if autostatistics_state is not None:
        where_sql += f" AND AUTOSTATISTICS_STATE = {autostatistics_state}"

    # 查询所有数据
    all_sql = f"SELECT * FROM {TABLE_NAME} {where_sql}"
    all_rows = db.execute_query(all_sql)

    # 获取父级节点
    parent_rows = [r for r in all_rows if r.get("AUTOSTATISTICS_PID") == autostatistics_pid]
    parent_rows.sort(key=lambda x: (x.get("AUTOSTATISTICS_INDEX") or 0, x.get("AUTOSTATISTICS_ID") or 0))
    total_count = len(parent_rows)

    result = []
    for row in parent_rows:
        node = _process_row(dict(row))
        node_id = node.get("AUTOSTATISTICS_ID")

        # 处理图标地址
        ico = node.get("AUTOSTATISTICS_ICO", "")
        if ico and ico.startswith("/"):
            node["AUTOSTATISTICS_ICO"] = "https://eshangtech.com:8443" + ico

        children = _build_tree_children(all_rows, node_id)

        result.append({
            "node": node,
            "children": children
        })

    return total_count, result


def _build_tree_children(all_rows: list, parent_id: int) -> list:
    """递归构建子级树"""
    children = []
    child_rows = [r for r in all_rows if r.get("AUTOSTATISTICS_PID") == parent_id]
    child_rows.sort(key=lambda x: (x.get("AUTOSTATISTICS_INDEX") or 0, x.get("AUTOSTATISTICS_ID") or 0))

    for row in child_rows:
        node = _process_row(dict(row))
        node_id = node.get("AUTOSTATISTICS_ID")

        # 处理图标地址
        ico = node.get("AUTOSTATISTICS_ICO", "")
        if ico and ico.startswith("/"):
            node["AUTOSTATISTICS_ICO"] = "https://eshangtech.com:8443" + ico

        # 判断子级是否有数据
        sub_children = _build_tree_children(all_rows, node_id)

        children.append({
            "node": node,
            "children": sub_children
        })

    return children


def get_autostatistics_detail(db: DatabaseHelper, autostatistics_id: int) -> Optional[dict]:
    """
    获取自定义统计归口明细
    对应原 AUTOSTATISTICSHelper.GetAUTOSTATISTICSDetail
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {autostatistics_id}"
    rows = db.execute_query(sql)
    if rows:
        row = _process_row(rows[0])
        # 处理图标地址
        ico = row.get("AUTOSTATISTICS_ICO", "")
        if ico and ico.startswith("/"):
            row["AUTOSTATISTICS_ICO"] = "https://eshangtech.com:8443" + ico
        return row
    return None


def synchro_autostatistics(db: DatabaseHelper, data: dict) -> bool:
    """
    同步自定义统计归口表（新增/更新）
    对应原 AUTOSTATISTICSHelper.SynchroAUTOSTATISTICS
    不强制限定 TYPE，前端传什么就存什么
    """
    # 处理 INELASTIC_DEMAND -> STATISTICS_TYPE 映射
    if data.get("AUTOSTATISTICS_TYPE") == 2000 and data.get("INELASTIC_DEMAND") is not None:
        data["STATISTICS_TYPE"] = data.pop("INELASTIC_DEMAND")
    elif "INELASTIC_DEMAND" in data:
        if data.get("STATISTICS_TYPE") is None:
            data.pop("INELASTIC_DEMAND")
        else:
            data.pop("INELASTIC_DEMAND")

    # 默认有效状态
    if data.get("AUTOSTATISTICS_STATE") is None:
        data["AUTOSTATISTICS_STATE"] = 1

    # 默认操作时间
    if data.get("OPERATE_DATE") is None:
        data["OPERATE_DATE"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    autostatistics_id = data.get("AUTOSTATISTICS_ID")

    if autostatistics_id is not None:
        # 更新
        check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {autostatistics_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False

        set_parts = []
        for key, value in data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {autostatistics_id}"
            db.execute_non_query(update_sql)
    else:
        # 新增
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}")
        new_id = (max_id or 0) + 1
        data["AUTOSTATISTICS_ID"] = new_id

        columns = []
        values = []
        for key, value in data.items():
            if value is None:
                continue
            columns.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True


def delete_autostatistics(db: DatabaseHelper, autostatistics_id: int) -> bool:
    """
    删除自定义统计归口表（软删除，AUTOSTATISTICS_STATE=0）
    对应原 AUTOSTATISTICSHelper.DeleteAUTOSTATISTICS
    """
    check_sql = f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {autostatistics_id}"
    count = db.execute_scalar(check_sql)
    if count == 0:
        return False

    sql = f"UPDATE {TABLE_NAME} SET AUTOSTATISTICS_STATE = 0 WHERE {PRIMARY_KEY} = {autostatistics_id}"
    db.execute_non_query(sql)
    return True
