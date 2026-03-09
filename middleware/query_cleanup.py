# -*- coding: utf-8 -*-
"""
Query parameter cleanup middleware.

This keeps C#-style requests compatible with FastAPI while avoiding unsafe
global rewrites that break routes using different casing conventions.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from urllib.parse import urlencode, parse_qsl


class QueryParamCleanupMiddleware(BaseHTTPMiddleware):
    """Remove empty query values and expand a few ambiguous parameter aliases."""

    # Some migrated routers use different casing for the same logical parameter.
    # Add aliases instead of rewriting to a single target name.
    PARAM_ALIAS_MAP = {
        "serverpartid": ["ServerpartId", "serverpartId", "serverPartId"],
        "provincecode": ["ProvinceCode", "provinceCode"],
        "pageindex": ["PageIndex", "pageIndex"],
        "pagesize": ["PageSize", "pageSize"],
    }

    # Non-ambiguous compatibility rewrites.
    PARAM_NAME_MAP = {
        "serverpart_id": "Serverpart_ID",
        "spregiontype_id": "SPREGIONTYPE_ID",
        "datattype": "dataType",
        "datatype": "dataType",
        "ranknum": "rankNum",
        "issync": "isSync",
        "provincename": "provinceName",
        "cityname": "cityName",
        "statisticsmonth": "StatisticsMonth",
        "pushprovincecode": "pushProvinceCode",
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
            seen_pairs = set()

            for key, value in original_params:
                if value == "":
                    modified = True
                    continue

                key_lower = key.lower()

                if key_lower in self.PARAM_ALIAS_MAP:
                    for alias in self.PARAM_ALIAS_MAP[key_lower]:
                        pair = (alias, value)
                        if pair not in seen_pairs:
                            new_params.append(pair)
                            seen_pairs.add(pair)
                    modified = True
                    continue

                if key_lower in self.PARAM_NAME_MAP:
                    expected_name = self.PARAM_NAME_MAP[key_lower]
                    if key != expected_name:
                        key = expected_name
                        modified = True

                pair = (key, value)
                if pair not in seen_pairs:
                    new_params.append(pair)
                    seen_pairs.add(pair)

            if modified:
                request.scope["query_string"] = urlencode(new_params).encode("utf-8")

        response = await call_next(request)
        return response
