# -*- coding: utf-8 -*-
"""
旧API代理工具
对于尚未实现查询逻辑的接口，可直接代理到旧API
"""
import requests
import logging

logger = logging.getLogger(__name__)

OLD_API_BASE = "http://127.0.0.1:8900/CommercialApi"
PROXY_TIMEOUT = 15


def proxy_to_old_api(method: str, route: str, params: dict = None, headers: dict = None):
    """
    将请求代理到旧API
    method: GET 或 POST
    route: 路由路径，如 /Revenue/GetRevenueCompare
    params: 查询参数(GET)或body(POST)
    headers: 请求头
    返回: 旧API的JSON响应
    """
    url = f"{OLD_API_BASE}{route}"
    proxy_headers = {}
    if headers:
        # 只传递ProvinceCode
        pc = headers.get("provincecode") or headers.get("ProvinceCode")
        if pc:
            proxy_headers["ProvinceCode"] = pc

    try:
        # 过滤None和空字符串参数
        clean_params = {k: v for k, v in (params or {}).items() if v is not None and v != ""} if params else {}
        if method.upper() == "GET":
            r = requests.get(url, params=clean_params, headers=proxy_headers, timeout=PROXY_TIMEOUT)
        else:
            r = requests.post(url, json=params, headers=proxy_headers, timeout=PROXY_TIMEOUT)

        if r.status_code == 200:
            return r.json()
        else:
            logger.warning(f"代理旧API失败: {url} status={r.status_code}")
            return None
    except Exception as e:
        logger.error(f"代理旧API异常: {url} error={e}")
        return None
