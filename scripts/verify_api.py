# -*- coding: utf-8 -*-
"""
新 API 接口自验脚本
直接验证 Python API (8080) 各接口能否查出真实数据
"""
import requests
import json
import time

BASE = "http://127.0.0.1:8080/CommercialApi"
TIMEOUT = 10

def call(method, path, params, desc):
    """调用接口并验证"""
    url = BASE + path
    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            resp = requests.post(url, json=params, timeout=TIMEOUT)
        
        if resp.status_code != 200:
            return "FAIL", f"HTTP {resp.status_code}", None
        
        data = resp.json()
        code = data.get("Result_Code")
        msg = data.get("Result_Msg", "")
        result_data = data.get("Result_Data")
        
        if code == 100:
            # 检查是否有真实数据
            if isinstance(result_data, dict):
                total = result_data.get("TotalCount")
                items = result_data.get("Items")
                if total is not None:
                    if isinstance(items, list) and len(items) > 0:
                        return "PASS", f"Code=100, 总数={total}, Items={len(items)}条", data
                    elif total == 0:
                        return "WARN", f"Code=100, 总数=0 (可能无数据)", data
                    else:
                        return "PASS", f"Code=100, TotalCount={total}", data
                else:
                    # 非列表数据（单条明细）
                    if result_data:
                        keys = list(result_data.keys())[:5]
                        return "PASS", f"Code=100, 字段: {keys}", data
                    return "WARN", f"Code=100, 数据为空", data
            else:
                return "PASS", f"Code=100", data
        elif code == 101:
            return "WARN", f"Code=101, 无数据: {msg}", data
        else:
            return "FAIL", f"Code={code}, Msg={msg[:80]}", data
    except requests.exceptions.Timeout:
        return "FAIL", "TIMEOUT", None
    except Exception as e:
        return "FAIL", str(e)[:100], None

def main():
    print(f"{'='*80}")
    print(f"新 API 接口自验测试 | {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API: {BASE}")
    print(f"{'='*80}\n")

    tests = [
        # ===== BaseInfo (已实现) =====
        ("GET", "/BaseInfo/GetSPRegionList", {"Province_Code": "3544"}, "获取片区列表"),
        ("GET", "/BaseInfo/GetBusinessTradeList", {"pushProvinceCode": "3544"}, "获取业态列表"),
        ("GET", "/BaseInfo/GetServerPartList", {"Province_Code": "3544"}, "获取服务区列表"),
        ("GET", "/BaseInfo/GetOwnerUnitListByProvinceCode", {"Province_Code": "3544"}, "获取业主单位列表"),
        ("GET", "/BaseInfo/GetBrandList", {"pushProvinceCode": "3544"}, "获取品牌列表"),

        # ===== Examine =====
        ("POST", "/Examine/GetEXAMINEList", {"PageIndex": 1, "PageSize": 3}, "获取考核列表"),
        ("GET", "/Examine/GetEXAMINEDetail", {"EXAMINEId": 1}, "获取考核明细(ID=1)"),
        ("POST", "/Examine/GetMEETINGList", {"PageIndex": 1, "PageSize": 3}, "获取晨会列表"),
        ("GET", "/Examine/GetMEETINGDetail", {"MEETINGId": 1}, "获取晨会明细(ID=1)"),
        ("POST", "/Examine/GetPATROLList", {"PageIndex": 1, "PageSize": 3}, "获取巡检列表"),
        ("GET", "/Examine/GetPATROLDetail", {"PATROLId": 1}, "获取巡检明细(ID=1)"),
        ("GET", "/Examine/WeChat_GetExamineDetail", {"ExamineId": 1}, "微信考核明细(ID=1)"),

        # ===== Analysis =====
        ("POST", "/Analysis/GetANALYSISINSList", {"PageIndex": 1, "PageSize": 3}, "获取分析列表"),
        ("GET", "/Analysis/GetANALYSISINSDetail", {"ANALYSISINSId": 1}, "获取分析明细(ID=1)"),
        ("GET", "/Analysis/GetShopMerchant", {"ShopName": "便利"}, "获取门店商家"),

        # ===== Budget =====
        ("POST", "/Budget/GetBUDGETPROJECT_AHList", {"PageIndex": 1, "PageSize": 3}, "获取预算列表"),
        ("GET", "/Budget/GetBUDGETPROJECT_AHDetail", {"BUDGETPROJECT_AHId": 1}, "获取预算明细(ID=1)"),
        ("GET", "/Budget/GetBudgetMainShow", {"BUDGETPROJECT_AHId": 1}, "获取预算主页展示"),
    ]

    results = {"PASS": 0, "WARN": 0, "FAIL": 0}
    
    for method, path, params, desc in tests:
        status, msg, data = call(method, path, params, desc)
        icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[status]
        print(f"  {icon} [{method:4s}] {path:50s} {desc:20s} → {msg}")
        results[status] += 1

        # 如果ID=1没数据，尝试更大的ID
        if status == "WARN" and "无数据" in msg and "Id" in str(params):
            for test_id in [2, 5, 10, 50, 100]:
                new_params = dict(params)
                for k in new_params:
                    if "Id" in k or "ID" in k:
                        new_params[k] = test_id
                s2, m2, d2 = call(method, path, new_params, desc)
                if s2 == "PASS":
                    print(f"       ↳ 换 ID={test_id}: ✅ {m2}")
                    results["WARN"] -= 1
                    results["PASS"] += 1
                    break

    print(f"\n{'='*80}")
    total_tests = sum(results.values())
    print(f"自验完成: ✅PASS={results['PASS']}/{total_tests} ⚠️WARN={results['WARN']} ❌FAIL={results['FAIL']}")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
