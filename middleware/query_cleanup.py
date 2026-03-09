# -*- coding: utf-8 -*-
"""
查询参数清洗中间件

解决 C# ASP.NET 与 FastAPI 的参数兼容性问题：
1. C# 的 int? 类型参数收到空字符串时自动当作 null
   → FastAPI 的 Optional[int] 收到空字符串时会返回 422 验证错误
   → 移除空字符串参数让 FastAPI 使用默认值

2. C# ASP.NET 的参数绑定是大小写不敏感的
   → FastAPI 是大小写敏感的
   → 将前端传来的参数名归一化为 Python 路由期望的大小写
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from urllib.parse import urlencode, parse_qsl


class QueryParamCleanupMiddleware(BaseHTTPMiddleware):
    """清理空字符串查询参数 + 参数名大小写归一化，兼容 C# ASP.NET 行为"""

    # 参数名映射表：小写 → Python 端实际定义的参数名
    # 对于大小写冲突的参数（如前端传 ServerPartId，Python 定义 serverPartId）
    PARAM_NAME_MAP = {
        "serverpartid": "serverPartId",
        "serverpart_id": "Serverpart_ID",
        "spregiontype_id": "SPREGIONTYPE_ID",
        "datattype": "dataType",
        "datatype": "dataType",
        "ranknum": "rankNum",
        "pageindex": "pageIndex",
        "pagesize": "pageSize",
        "issync": "isSync",
        "provincename": "provinceName",
        "cityname": "cityName",
        "statisticsstartmonth": "statisticsStartMonth",
        "statisticsendmonth": "statisticsEndMonth",
        "statisticsmonth": "StatisticsMonth",
        "pushprovincecode": "pushProvinceCode",
        "provincecode": "ProvinceCode",
        "businesstradetype": "BusinessTradeType",
        "businesstrade": "BusinessTrade",
        "accounttype": "accountType",
        "fieldexplainfield": "FieldExplainField",
        "explainfield": "ExplainField",
    }

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.query:
            original_params = parse_qsl(request.url.query, keep_blank_values=True)
            modified = False
            new_params = []

            for k, v in original_params:
                # 1. 过滤空字符串参数
                if v == "":
                    modified = True
                    continue

                # 2. 参数名大小写归一化
                k_lower = k.lower()
                if k_lower in self.PARAM_NAME_MAP:
                    expected_name = self.PARAM_NAME_MAP[k_lower]
                    if k != expected_name:
                        k = expected_name
                        modified = True

                new_params.append((k, v))

            if modified:
                new_query = urlencode(new_params)
                request.scope["query_string"] = new_query.encode("utf-8")

        response = await call_next(request)
        return response

