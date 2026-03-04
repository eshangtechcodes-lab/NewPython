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
