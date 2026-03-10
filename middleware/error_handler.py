# -*- coding: utf-8 -*-
"""
全局异常处理中间件
异常时返回 Result 格式 + Message 字段（与 C# 行为一致）
"""
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger


async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"未处理的异常: {request.method} {request.url} - {exc}")
    return JSONResponse(
        status_code=200,
        content={
            "Result_Code": 999,
            "Result_Desc": "服务器内部错误",
            "Result_Data": None,
            "Message": "服务器内部错误"
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理 FastAPI 请求校验异常（422）"""
    logger.warning(f"请求校验失败: {request.method} {request.url} - {exc.errors()}")
    return JSONResponse(
        status_code=200,
        content={
            "Result_Code": 999,
            "Result_Desc": "请求参数校验失败",
            "Result_Data": None,
            "Message": "请求参数校验失败"
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理 HTTPException（404/405 等）"""
    logger.warning(f"HTTP 异常: {request.method} {request.url} - {exc.status_code} {exc.detail}")
    error_msg = str(exc.detail)
    return JSONResponse(
        status_code=200,
        content={
            "Result_Code": 999,
            "Result_Desc": error_msg,
            "Result_Data": None,
            "Message": error_msg
        }
    )
