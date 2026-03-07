# -*- coding: utf-8 -*-
"""
Revenue/BigData 接口入参对齐检查 + 新API vs 基线缓存对比
   
用法: python scripts/compare_revenue_bigdata.py
"""
import requests
import json
import time
import os
import sys

NEW = "http://127.0.0.1:8080/CommercialApi"
HEADERS = {"ProvinceCode": "340000"}
TIMEOUT = 30
BASELINE_FILE = "scripts/test_results/baseline_cache.json"

# 禁用代理
session = requests.Session()
session.trust_env = False


def call_new(method, route, params):
    """调用新API"""
    url = NEW + route
    try:
        if method == "GET":
            r = session.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        else:
            r = session.post(url, json=params, headers=HEADERS, timeout=TIMEOUT)
        if r.status_code != 200:
            return r.status_code, None, r.text[:200]
        try:
            return 200, r.json(), None
        except:
            return 200, None, r.text[:200]
    except requests.exceptions.Timeout:
        return 0, None, "TIMEOUT"
    except Exception as e:
        return -1, None, str(e)[:100]


def compare_fields(old_data, new_data):
    """对比两个响应的字段结构"""
    diffs = []
    
    if not isinstance(old_data, dict) or not isinstance(new_data, dict):
        return diffs
    
    oc = old_data.get("Result_Code")
    nc = new_data.get("Result_Code")
    if oc != nc:
        diffs.append(f"Result_Code: 旧={oc} 新={nc}")
    
    ord_d = old_data.get("Result_Data")
    nrd_d = new_data.get("Result_Data")
    
    if ord_d is None and nrd_d is None:
        return diffs
    
    if isinstance(ord_d, dict) and isinstance(nrd_d, dict):
        # TotalCount 对比
        ot = ord_d.get("TotalCount")
        nt = nrd_d.get("TotalCount")
        if ot is not None and nt is not None and ot != nt:
            diffs.append(f"TotalCount: 旧={ot} 新={nt}")
        
        # List/DataList 字段对比
        for list_key in ["List", "DataList"]:
            old_list = ord_d.get(list_key, [])
            new_list = nrd_d.get(list_key, [])
            if old_list and isinstance(old_list, list) and old_list[0] and isinstance(old_list[0], dict):
                old_keys = set(old_list[0].keys())
                if new_list and isinstance(new_list, list) and new_list[0] and isinstance(new_list[0], dict):
                    new_keys = set(new_list[0].keys())
                    missing = old_keys - new_keys
                    extra = new_keys - old_keys
                    if missing:
                        diffs.append(f"新API缺少字段: {missing}")
                    if extra:
                        diffs.append(f"新API多出字段: {extra}")
                elif not new_list:
                    diffs.append(f"新API {list_key} 为空, 旧API有{len(old_list)}条")
        
        # 对比 Result_Data 顶层字段
        old_top_keys = set(ord_d.keys())
        new_top_keys = set(nrd_d.keys()) 
        top_missing = old_top_keys - new_top_keys
        top_extra = new_top_keys - old_top_keys
        if top_missing:
            diffs.append(f"Result_Data缺少顶层字段: {top_missing}")
        if top_extra:
            diffs.append(f"Result_Data多出顶层字段: {top_extra}")
    
    elif isinstance(ord_d, list) and isinstance(nrd_d, dict):
        diffs.append(f"返回类型不同: 旧=list 新=dict")
    elif isinstance(ord_d, dict) and isinstance(nrd_d, list):
        diffs.append(f"返回类型不同: 旧=dict 新=list")
    
    return diffs


def main():
    # 加载基线缓存
    if not os.path.exists(BASELINE_FILE):
        print(f"❌ 基线缓存不存在: {BASELINE_FILE}")
        return
    
    with open(BASELINE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    
    baseline = cache["results"]
    
    # 只测试 Revenue 和 BigData 相关接口
    test_routes = []
    for key, entry in baseline.items():
        route = entry.get("route", "")
        if "/Revenue/" in route or "/BigData/" in route:
            test_routes.append(entry)
    
    test_routes.sort(key=lambda x: x.get("route", ""))
    total = len(test_routes)
    
    print(f"\n{'='*130}")
    print(f"  Revenue + BigData 接口对比测试（新API实时调用 vs 基线缓存）")
    print(f"  新 API: {NEW}  |  接口数: {total}")
    print(f"{'='*130}\n")
    
    stats = {"PASS": 0, "DIFF": 0, "SKIP": 0, "FIELD_DIFF": 0}
    diff_list = []
    field_diff_list = []
    
    start = time.time()
    
    for i, entry in enumerate(test_routes, 1):
        method = entry["method"]
        route = entry["route"]
        params = entry.get("params", {})
        old_status = entry.get("http_status", 0)
        old_resp = entry.get("response")
        
        # 调用新API
        ns, nd, nerr = call_new(method, route, params)
        
        # 判定
        if old_status != 200:
            result = "SKIP"
            icon = "⏭️"
            detail = f"旧API={old_status}"
        elif ns != 200:
            result = "DIFF"
            icon = "❌"
            detail = f"新HTTP={ns} err={nerr}"
        else:
            oc = old_resp.get("Result_Code") if isinstance(old_resp, dict) else None
            nc = nd.get("Result_Code") if isinstance(nd, dict) else None
            
            if oc == nc:
                # 深度对比字段
                field_diffs = compare_fields(old_resp, nd)
                if field_diffs:
                    result = "FIELD_DIFF"
                    icon = "⚠️"
                    detail = "; ".join(field_diffs[:2])
                    field_diff_list.append({"route": f"{method} {route}", "diffs": field_diffs})
                else:
                    result = "PASS"
                    icon = "✅"
                    detail = f"Code={oc}"
            else:
                result = "DIFF"
                icon = "❌"
                detail = f"Code: 旧={oc} 新={nc}"
                diff_list.append({"method": method, "route": route, "detail": detail})
        
        stats[result] = stats.get(result, 0) + 1
        
        print(f"  [{i:3d}/{total}] {icon} {method:4s} {route:60s} {detail}")
        sys.stdout.flush()
    
    elapsed = round(time.time() - start, 1)
    
    # 汇总
    print(f"\n{'='*130}")
    print(f"  测试完成！耗时: {elapsed}s")
    print(f"  ✅ PASS={stats['PASS']}/{total}  ❌ DIFF={stats['DIFF']}  ⚠️ FIELD_DIFF={stats['FIELD_DIFF']}  ⏭️ SKIP={stats['SKIP']}")
    print(f"{'='*130}")
    
    if diff_list:
        print(f"\n--- ❌ DIFF 详情 ({len(diff_list)}个) ---")
        for d in diff_list:
            print(f"  {d['method']:4s} {d['route']:60s} {d['detail']}")
    
    if field_diff_list:
        print(f"\n--- ⚠️ 字段差异详情 ({len(field_diff_list)}个) ---")
        for dd in field_diff_list:
            print(f"  {dd['route']}")
            for diff in dd["diffs"]:
                print(f"    → {diff}")
    
    # 保存
    os.makedirs("scripts/test_results", exist_ok=True)
    result_data = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed": elapsed,
        "stats": stats,
        "diffs": diff_list,
        "field_diffs": field_diff_list,
    }
    with open("scripts/test_results/compare_revenue_bigdata.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    print(f"\n  结果已保存: scripts/test_results/compare_revenue_bigdata.json")


if __name__ == "__main__":
    main()
