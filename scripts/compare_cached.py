# -*- coding: utf-8 -*-
"""
Step 2: 基于缓存的快速对比
读取旧 API 基线缓存 + 实时调用新 API → 秒级完成全量对比

用法: python scripts/compare_cached.py
"""
import requests
import json
import time
import os
import re
import sys

NEW = "http://127.0.0.1:8080/CommercialApi"
TIMEOUT = 15
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


def call_new(method, route, params):
    """调用新API"""
    url = NEW + route
    try:
        if method == "GET":
            r = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            r = requests.post(url, json=params, timeout=TIMEOUT)
        if r.status_code != 200:
            return r.status_code, {}
        try:
            data = r.json()
            if not isinstance(data, dict):
                return 200, {"_raw": str(data)[:50]}
            return 200, data
        except:
            return 200, {"_raw": r.text[:50]}
    except requests.exceptions.Timeout:
        return 0, {}
    except Exception as e:
        return -1, {"_err": str(e)[:50]}


def info_str(status, data):
    """生成状态摘要"""
    if status == 0: return "TIMEOUT"
    if status != 200: return f"HTTP{status}"
    if not isinstance(data, dict): return "OK"
    code = data.get("Result_Code")
    rd = data.get("Result_Data")
    if isinstance(rd, dict):
        total = rd.get("TotalCount")
        if total is not None:
            return f"C={code},T={total}"
    return f"C={code}"


def deep_compare(old_data, new_data):
    """深度对比两个响应的数据内容"""
    diffs = []
    
    if not isinstance(old_data, dict) or not isinstance(new_data, dict):
        return diffs
    
    oc = old_data.get("Result_Code")
    nc = new_data.get("Result_Code")
    if oc != nc:
        diffs.append(f"Result_Code: 旧={oc} 新={nc}")
    
    ord_d = old_data.get("Result_Data", {})
    nrd_d = new_data.get("Result_Data", {})
    
    if isinstance(ord_d, dict) and isinstance(nrd_d, dict):
        ot = ord_d.get("TotalCount")
        nt = nrd_d.get("TotalCount")
        if ot is not None and nt is not None and ot != nt:
            diffs.append(f"TotalCount: 旧={ot} 新={nt}")
        
        # 对比数据列表的第一条记录的字段
        old_list = ord_d.get("DataList", [])
        new_list = nrd_d.get("DataList", [])
        if old_list and new_list:
            old_keys = set(old_list[0].keys()) if isinstance(old_list[0], dict) else set()
            new_keys = set(new_list[0].keys()) if isinstance(new_list[0], dict) else set()
            missing = old_keys - new_keys
            extra = new_keys - old_keys
            if missing:
                diffs.append(f"新API缺少字段: {missing}")
            if extra:
                diffs.append(f"新API多出字段: {extra}")
    
    return diffs


def main():
    # 加载基线缓存
    if not os.path.exists(BASELINE_FILE):
        print(f"❌ 基线缓存文件不存在: {BASELINE_FILE}")
        print(f"   请先运行: python scripts/baseline_collect.py")
        return
    
    with open(BASELINE_FILE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    
    meta = cache["meta"]
    baseline = cache["results"]
    
    routes = extract_routes()
    total = len(routes)
    
    print(f"\n{'='*120}")
    print(f"  快速对比（旧API使用缓存，新API实时调用）")
    print(f"  缓存采集时间: {meta['collect_time']}  |  缓存接口数: {meta['total_routes']}")
    print(f"  新 API: {NEW}  |  当前路由数: {total}")
    print(f"{'='*120}\n")
    
    stats = {"PASS": 0, "DIFF": 0, "SKIP": 0, "NEW_ONLY": 0}
    all_results = []
    diff_details = []
    
    start = time.time()
    
    for i, (method, route) in enumerate(routes, 1):
        key = f"{method}:{route}"
        parts = route.split("/")
        ctrl = parts[1] if len(parts) > 1 else "?"
        
        # 从缓存读取旧API结果
        old_entry = baseline.get(key)
        if old_entry is None:
            # 缓存中没有的路由（可能是新增的）
            sys.stdout.write(f"[{i:3d}/{total}] {method:4s} {route:55s} {'(无缓存)':18s} ")
            params_new = {"ProvinceCode": "340000"}  # 默认参数
            ns_code, nd = call_new(method, route, params_new)
            ni = info_str(ns_code, nd)
            result = "NEW_ONLY"
            print(f"{ni:18s} [🆕]NEW_ONLY")
        else:
            os_code = old_entry["http_status"]
            od = old_entry["response"] or {}
            params = old_entry["params"]
            
            oi = info_str(os_code, od)
            
            # 实时调用新API
            ns_code, nd = call_new(method, route, params)
            ni = info_str(ns_code, nd)
            
            # 判定结果
            if os_code != 200:
                result = "SKIP"  # 旧API本身就有错误
            elif ns_code != 200:
                result = "DIFF"
            else:
                oc = od.get("Result_Code") if isinstance(od, dict) else None
                nc = nd.get("Result_Code") if isinstance(nd, dict) else None
                if oc == nc:
                    ord_d = od.get("Result_Data") or {} if isinstance(od, dict) else {}
                    nrd_d = nd.get("Result_Data") or {} if isinstance(nd, dict) else {}
                    if isinstance(ord_d, dict) and isinstance(nrd_d, dict):
                        ot = ord_d.get("TotalCount")
                        nt = nrd_d.get("TotalCount")
                        if ot is not None and nt is not None and ot != nt:
                            result = "DIFF"
                        else:
                            result = "PASS"
                    else:
                        result = "PASS"
                else:
                    result = "DIFF"
            
            icon = {"PASS": "✅", "DIFF": "❌", "SKIP": "⏭️"}[result]
            print(f"[{i:3d}/{total}] {method:4s} {route:55s} {oi:18s} {ni:18s} {icon}{result}")
            
            # 深度对比
            if result == "PASS" and os_code == 200:
                diffs = deep_compare(od, nd)
                if diffs:
                    result = "WARN"
                    diff_details.append({"route": f"{method} {route}", "diffs": diffs})
        
        stats[result] = stats.get(result, 0) + 1
        all_results.append({
            "idx": i, "method": method, "route": route, "ctrl": ctrl,
            "old": oi if old_entry else "(无缓存)",
            "new": ni, "result": result
        })
    
    elapsed = round(time.time() - start, 1)
    
    # 汇总
    print(f"\n{'='*120}")
    total_tested = sum(stats.values())
    print(f"  对比完成！耗时: {elapsed}s（旧API读缓存，新API实时调用）")
    print(f"  ✅ PASS={stats.get('PASS',0)}/{total_tested}  ❌ DIFF={stats.get('DIFF',0)}  "
          f"⏭️ SKIP={stats.get('SKIP',0)}  🆕 NEW_ONLY={stats.get('NEW_ONLY',0)}  "
          f"⚠️ WARN={stats.get('WARN',0)}")
    print(f"{'='*120}")
    
    # 按 controller 分组
    from collections import defaultdict
    ctrl_stats = defaultdict(lambda: {"PASS": 0, "DIFF": 0, "SKIP": 0, "WARN": 0, "NEW_ONLY": 0, "total": 0})
    for r in all_results:
        ctrl_stats[r["ctrl"]][r["result"]] += 1
        ctrl_stats[r["ctrl"]]["total"] += 1
    
    print(f"\n--- 按 Controller 汇总 ---")
    print(f"{'Controller':25s} {'总数':>5s} {'PASS':>5s} {'DIFF':>5s} {'SKIP':>5s} {'WARN':>5s}")
    for ctrl in sorted(ctrl_stats.keys()):
        s = ctrl_stats[ctrl]
        print(f"{ctrl:25s} {s['total']:5d} {s['PASS']:5d} {s['DIFF']:5d} {s['SKIP']:5d} {s.get('WARN',0):5d}")
    
    # DIFF 详情
    diffs_list = [r for r in all_results if r["result"] == "DIFF"]
    if diffs_list:
        print(f"\n--- ❌ DIFF 详情 ({len(diffs_list)}个) ---")
        for d in diffs_list:
            print(f"  {d['method']:4s} {d['route']:55s} 旧={d['old']:18s} 新={d['new']}")
    
    # WARN 详情（Code一致但数据有差异）
    if diff_details:
        print(f"\n--- ⚠️ WARN 详情（Code一致但数据有异） ---")
        for dd in diff_details:
            print(f"  {dd['route']}")
            for diff in dd["diffs"]:
                print(f"    → {diff}")
    
    # 保存结果
    os.makedirs("scripts/test_results", exist_ok=True)
    with open("scripts/test_results/compare_cached.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n  结果已保存: scripts/test_results/compare_cached.json")


if __name__ == "__main__":
    main()
