# -*- coding: utf-8 -*-
"""
全局异常处理中间件
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理，返回统一的错误格式"""
    logger.error(f"未处理的异常: {request.method} {request.url} - {exc}")
    return JSONResponse(
        status_code=200,  # 保持 200 状态码，错误通过 Result_Code 区分
        content={
            "Result_Code": 999,
            "Result_Desc": f"服务器内部错误: {str(exc)}",
            "Result_Data": None
        }
    )
