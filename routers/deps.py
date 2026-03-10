# -*- coding: utf-8 -*-
"""
公共依赖
替代原 BaseController.cs 中的公共功能
"""
from core.database import DatabaseHelper, db_helper


def get_db() -> DatabaseHelper:
    """
    获取数据库实例（FastAPI 依赖注入）
    替代原 BaseController 中的 transaction
    """
    return db_helper


def parse_multi_ids(raw: str) -> list[int]:
    """解析逗号分隔的多值ID字符串，返回合法整数列表"""
    if not raw:
        return []
    ids = []
    for part in str(raw).split(","):
        part = part.strip()
        if part:
            try:
                ids.append(int(part))
            except (ValueError, TypeError):
                pass
    return ids


def build_in_condition(column: str, ids: list[int]) -> str:
    """构建 IN 或 = 条件表达式"""
    if not ids:
        return "1=1"
    if len(ids) == 1:
        return f'"{column}" = {ids[0]}'
    return f'"{column}" IN ({",".join(str(i) for i in ids)})'
