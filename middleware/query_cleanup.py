# -*- coding: utf-8 -*-
"""
查询参数清洗中间件

解决 C# ASP.NET 与 FastAPI 的参数兼容性问题：
- C# 的 int? 类型参数收到空字符串时自动当作 null
- FastAPI 的 Optional[int] 收到空字符串时会返回 422 验证错误

此中间件在请求到达路由之前，将空字符串的查询参数移除，
让 FastAPI 使用参数的默认值（通常是 None），完美兼容 C# 行为。
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from urllib.parse import urlencode, parse_qsl


class QueryParamCleanupMiddleware(BaseHTTPMiddleware):
    """清理空字符串查询参数，兼容 C# ASP.NET 的参数解析行为"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # 只处理带查询参数的请求
        if request.url.query:
            # 解析查询参数，过滤掉值为空字符串的参数
            original_params = parse_qsl(request.url.query, keep_blank_values=True)
            cleaned_params = [(k, v) for k, v in original_params if v != ""]

            # 如果有参数被清理掉了，重建查询字符串
            if len(cleaned_params) != len(original_params):
                new_query = urlencode(cleaned_params)
                # 修改 scope 中的 query_string
                request.scope["query_string"] = new_query.encode("utf-8")

        response = await call_next(request)
        return response
