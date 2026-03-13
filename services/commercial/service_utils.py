# -*- coding: utf-8 -*-
"""
CommercialApi Service 公共工具函数
消除 Service 文件间的重复代码
"""
from __future__ import annotations
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


# ===== 安全类型转换 =====

def safe_float(v) -> float:
    """安全转浮点，None/异常值 → 0.0"""
    try:
        return float(v) if v is not None else 0.0
    except (ValueError, TypeError):
        return 0.0


def safe_int(v) -> int:
    """安全转整数，None/异常值 → 0"""
    try:
        return int(v) if v is not None else 0
    except (ValueError, TypeError):
        return 0


# 向后兼容别名（旧代码用 _sf/_si）
_sf = safe_float
_si = safe_int


# ===== 省份编码查询 =====

def get_province_id(db: DatabaseHelper, province_code: str) -> int:
    """通过省份编码获取省份 FieldEnum ID

    从 T_FIELDEXPLAIN + T_FIELDENUM 中查找 DIVISION_CODE 对应的枚举 ID。
    返回值强制为 int，防止 SQL 注入。

    Args:
        db: 数据库连接
        province_code: 省份编码（如 "340000"）

    Returns:
        int: 省份枚举 ID
    """
    pc_sql = """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
              AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE'
              AND B."FIELDENUM_VALUE" = :pc"""
    pc_rows = db.execute_query(pc_sql, {"pc": province_code})
    return int(pc_rows[0]["FIELDENUM_ID"]) if pc_rows else int(province_code)


# ===== WHERE 条件构建 =====

def build_sp_where(province_id: int, serverpart_id=None, sp_region_type_id=None,
                   table_alias: str = "B") -> str:
    """构建服务区相关的通用 WHERE 条件

    Args:
        province_id: 省份 ID（int，来自 get_province_id）
        serverpart_id: 服务区 ID（可多个，逗号分隔）
        sp_region_type_id: 区域类型 ID
        table_alias: 表别名（默认 "B"）

    Returns:
        str: 以 ' AND ...' 开头的 WHERE 子句片段
    """
    alias = table_alias
    where_sql = f' AND {alias}."PROVINCE_CODE" = {province_id}'

    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        in_cond = build_in_condition('SERVERPART_ID', _sp_ids)
        where_sql += ' AND ' + in_cond.replace('"SERVERPART_ID"', f'{alias}."SERVERPART_ID"')
    elif sp_region_type_id:
        where_sql += f' AND {alias}."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    elif serverpart_id:
        where_sql += f' AND {alias}."SERVERPART_ID" = {safe_int(serverpart_id)}'

    return where_sql


# ===== 日期格式化 =====

def format_date_no_pad(val) -> str | None:
    """C# 风格日期格式化（月日不补零）

    输入: datetime 或字符串
    输出: "2025/3/30 14:02:47" 格式

    Args:
        val: 日期值

    Returns:
        str | None: 格式化后的日期字符串
    """
    if val is None:
        return None
    from datetime import datetime
    if isinstance(val, str):
        val = datetime.strptime(val[:19], "%Y-%m-%d %H:%M:%S")
    return f"{val.year}/{val.month}/{val.day} {val.hour}:{val.minute:02d}:{val.second:02d}"


def format_date_short(val) -> str | None:
    """C# 风格短日期（月日不补零）

    输出: "2025/3/30" 格式
    """
    if val is None:
        return None
    from datetime import datetime
    if isinstance(val, str):
        val = datetime.strptime(val[:10], "%Y-%m-%d")
    return f"{val.year}/{val.month}/{val.day}"
