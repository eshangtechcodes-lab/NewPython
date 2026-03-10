# -*- coding: utf-8 -*-
"""
通用格式化工具 — 用于对齐 C# 的数据输出格式
C# 的 HCC.Common.TranslateDateTime() 将数值型日期转换为 yyyy/MM/dd 或 yyyy/MM/dd HH:mm:ss 格式
"""

from __future__ import annotations
from typing import Optional


def format_int_date(value, include_time: bool = False) -> Optional[str]:
    """
    将 int/str 类型的日期（达梦数据库存储格式）转换为 C# 一致的格式。

    输入示例:
      - 20230526 → '2023/05/26'
      - 20230526155250 → '2023/05/26 15:52:50'

    参数:
      value: 日期值（int 或 str）
      include_time: 是否强制包含时间部分

    返回:
      格式化后的日期字符串，如果输入无效则返回 None
    """
    if value is None:
        return None
    s = str(value).strip()
    if not s or s == '0':
        return None

    try:
        if len(s) == 6:
            # 年月: 202406 → 2024/06
            return f"{s[:4]}/{s[4:6]}"
        elif len(s) == 8:
            # 纯日期: 20230526 → 2023/05/26
            return f"{s[:4]}/{s[4:6]}/{s[6:8]}"
        elif len(s) == 14:
            # 日期+时间: 20230526155250 → 2023/05/26 15:52:50
            return f"{s[:4]}/{s[4:6]}/{s[6:8]} {s[8:10]}:{s[10:12]}:{s[12:14]}"
        elif len(s) >= 10 and ('/' in s or '-' in s):
            # 已经是格式化的日期字符串，直接返回
            return s
        else:
            return s
    except Exception:
        return str(value)


def format_row_dates(row: dict, date_fields: set, time_fields: set = None) -> dict:
    """
    将字典中的指定日期字段从 int 格式转换为 C# 一致的字符串格式。

    参数:
      row: 数据字典
      date_fields: 纯日期字段集合（格式化为 yyyy/MM/dd）
      time_fields: 日期+时间字段集合（格式化为 yyyy/MM/dd HH:mm:ss），默认为空

    返回:
      修改后的 row（原地修改）
    """
    if time_fields is None:
        time_fields = set()

    for field in date_fields | time_fields:
        if field in row and row[field] is not None:
            v = row[field]
            if isinstance(v, int):
                row[field] = format_int_date(v, include_time=(field in time_fields))
    return row
