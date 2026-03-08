# -*- coding: utf-8 -*-
"""
公共依赖
替代原 BaseController.cs 中的公共功能
"""
from typing import Optional
from fastapi import Request
from core.database import DatabaseHelper, db_helper


def get_db() -> DatabaseHelper:
    """
    获取数据库实例（FastAPI 依赖注入）
    替代原 BaseController 中的 transaction
    """
    return db_helper


def get_int_header(request: Request, header_name: str, default: Optional[int] = None) -> Optional[int]:
    """
    从请求头读取整数值，复现原 C# BaseController.GetIntHeader
    HTTP Header 名称不区分大小写，尝试原始名和小写名
    """
    val = request.headers.get(header_name) or request.headers.get(header_name.lower())
    if val:
        try:
            return int(val)
        except (ValueError, TypeError):
            pass
    return default


def get_str_header(request: Request, header_name: str, default: str = "") -> str:
    """
    从请求头读取字符串值，复现原 C# BaseController.GetStringHeader
    """
    return request.headers.get(header_name) or request.headers.get(header_name.lower()) or default

