# -*- coding: utf-8 -*-
"""
Step 1: 并发采集旧 API 基线数据
使用线程池并发调用旧 C# API，把全部响应缓存到本地 JSON 文件。
只需运行一次，后续对比直接读缓存。

用法: python scripts/baseline_collect.py
"""
import requests
import json
import time
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

OLD = "http://127.0.0.1:8900/CommercialApi"
TIMEOUT = 90  # 给旧API更长超时，尽量拿到真实响应
MAX_WORKERS = 2  # 并发线程数（旧API WCF架构并发能力弱，不宜高于2）
BASELINE_FILE = "scripts/test_results/baseline_cache.json"


def extract_routes():
    """从 router 文件自动提取所有路由"""
    router_dir = r"D:\Projects\Python\eshang_api\routers\commercial_api"
    routes = []
    for fname in sorted(os.listdir(router_dir)):
        if not fname.endswith(".py") or fname == "__init__.py":
            continue
        path_ = os.path.join(router_dir, fname)
        with open(path_, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r'@router\.(get|post)\(["\'](.*?)["\']', content):
            method = m.group(1).upper()
            route = m.group(2)
            routes.append((method, route))
    return routes


def get_test_params(method, route):
    """从接口文档提取的正确参数（doc_params.json）优先，兜底使用通用参数"""
    global _DOC_PARAMS
    if _DOC_PARAMS is None:
        doc_path = os.path.join(os.path.dirname(__file__), "test_results", "doc_params.json")
        if os.path.exists(doc_path):
            with open(doc_path, "r", encoding="utf-8") as f:
                _DOC_PARAMS = json.load(f)
        else:
            _DOC_PARAMS = {}

    key = f"{method}:{route}"
    if key in _DOC_PARAMS:
        return _DOC_PARAMS[key].get("params", {})

    # 兜底：文档中没有的接口，使用通用参数
    r = route.lower()
    if method == "POST" and ("list" in r or "getbusiness" in r):
        return {"PageIndex": 1, "PageSize": 3, "SearchParameter": {"SERVERPART_IDS": "416,417,418,419"}}
    if method == "POST":
        return {"name": "", "value": ""}
    return {"ProvinceCode": "340000"}

_DOC_PARAMS = None

# 旧 C# API 中路由与新 Python API 路由不一致的映射
# 原因：BigDataController 的卡口接口在旧API上路由前缀是 Revenue/ 而不是 BigData/
OLD_ROUTE_MAP = {
    "/BigData/GetBayonetEntryList": "/Revenue/GetBayonetEntryList",
    "/BigData/GetBayonetSTAList": "/Revenue/GetBayonetSTAList",
    "/BigData/GetBayonetOAList": "/Revenue/GetBayonetOAList",
    "/BigData/GetBayonetProvinceOAList": "/Revenue/GetBayonetProvinceOAList",
    "/BigData/GetSPBayonetList": "/Revenue/GetSPBayonetList",
    "/BigData/GetBayonetRankList": "/Revenue/GetBayonetRankList",
    "/BigData/GetAvgBayonetAnalysis": "/Revenue/GetAvgBayonetAnalysis",
    "/BigData/GetProvinceAvgBayonetAnalysis": "/Revenue/GetProvinceAvgBayonetAnalysis",
    "/BigData/GetBayonetSTAnalysis": "/Revenue/GetBayonetSTAnalysis",
}


def call_old_api(idx, method, route, params):
    """调用旧API并返回结构化结果"""
    # 使用旧API的路由（可能与新API不同）
    old_route = OLD_ROUTE_MAP.get(route, route)
    url = OLD + old_route

    key = f"{method}:{route}"
    start = time.time()
    try:
        if method == "GET":
            r = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            r = requests.post(url, json=params, timeout=TIMEOUT)
        elapsed = round(time.time() - start, 3)
        
        if r.status_code != 200:
            return {
                "key": key, "idx": idx, "method": method, "route": route,
                "params": params, "http_status": r.status_code,
                "response": None, "elapsed": elapsed, "error": None
            }
        try:
            data = r.json()
        except:
            data = {"_raw": r.text[:200]}
        
        return {
            "key": key, "idx": idx, "method": method, "route": route,
            "params": params, "http_status": 200,
            "response": data, "elapsed": elapsed, "error": None
        }
    except requests.exceptions.Timeout:
        return {
            "key": key, "idx": idx, "method": method, "route": route,
            "params": params, "http_status": 0,
            "response": None, "elapsed": round(time.time() - start, 3),
            "error": f"TIMEOUT(>{TIMEOUT}s)"
        }
    except Exception as e:
        return {
            "key": key, "idx": idx, "method": method, "route": route,
            "params": params, "http_status": -1,
            "response": None, "elapsed": round(time.time() - start, 3),
            "error": str(e)[:100]
        }


def main():
    routes = extract_routes()
    total = len(routes)
    
    print(f"{'='*80}")
    print(f"  旧 API 基线数据采集（并发={MAX_WORKERS}线程，超时={TIMEOUT}s）")
    print(f"  地址: {OLD}")
    print(f"  路由数: {total}")
    print(f"  输出: {BASELINE_FILE}")
    print(f"{'='*80}\n")
    
    # 构建任务列表
    tasks = []
    for idx, (method, route) in enumerate(routes, 1):
        params = get_test_params(method, route)
        tasks.append((idx, method, route, params))
    
    # 并发采集
    results = {}
    done_count = 0
    start_all = time.time()
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(call_old_api, idx, method, route, params): (idx, method, route)
            for idx, method, route, params in tasks
        }
        
        for future in as_completed(futures):
            done_count += 1
            idx, method, route = futures[future]
            result = future.result()
            key = f"{method}:{route}"
            results[key] = result
            
            # 实时进度
            elapsed = result["elapsed"]
            status = result["http_status"]
            if result["error"]:
                tag = f"⏰ {result['error']}"
            elif status != 200:
                tag = f"HTTP{status}"
            else:
                code = result["response"].get("Result_Code", "?") if isinstance(result["response"], dict) else "?"
                rd = result["response"].get("Result_Data", {}) if isinstance(result["response"], dict) else {}
                tc = rd.get("TotalCount", "") if isinstance(rd, dict) else ""
                tag = f"C={code}" + (f",T={tc}" if tc != "" else "")
            
            print(f"  [{done_count:3d}/{total}] {elapsed:6.1f}s  {method:4s} {route:55s} {tag}")
            sys.stdout.flush()
    
    total_time = round(time.time() - start_all, 1)
    
    # 统计
    ok_count = sum(1 for r in results.values() if r["http_status"] == 200)
    timeout_count = sum(1 for r in results.values() if r["http_status"] == 0)
    error_count = sum(1 for r in results.values() if r["http_status"] not in (0, 200))
    
    print(f"\n{'='*80}")
    print(f"  采集完成！耗时: {total_time}s（并发{MAX_WORKERS}线程）")
    print(f"  成功: {ok_count}  超时: {timeout_count}  HTTP错误: {error_count}")
    print(f"{'='*80}")
    
    # 保存缓存文件
    os.makedirs(os.path.dirname(BASELINE_FILE), exist_ok=True)
    cache_data = {
        "meta": {
            "api_base": OLD,
            "collect_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_routes": total,
            "total_time_sec": total_time,
            "timeout": TIMEOUT,
            "workers": MAX_WORKERS,
        },
        "results": results,
    }
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n  ✅ 基线缓存已保存: {BASELINE_FILE}")
    print(f"  后续运行 compare_cached.py 即可秒级对比！")


if __name__ == "__main__":
    main()
