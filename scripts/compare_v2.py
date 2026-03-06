# -*- coding: utf-8 -*-
"""
接口对比测试脚本 v2
对比原 C# API (8900) 和 新 Python API (8080) 的返回结果
"""
import requests
import json
import time

OLD_BASE = "http://127.0.0.1:8900/api"
NEW_BASE = "http://127.0.0.1:8080/api"
TIMEOUT = 10

# 测试接口列表：(方法, 路径, 参数/body, 描述)
TEST_CASES = [
    # ===== Examine Controller =====
    ("GET", "/Examine/GetEXAMINEDetail", {"EXAMINEId": 1}, "考核明细"),
    ("GET", "/Examine/GetMEETINGDetail", {"MEETINGId": 1}, "晨会明细"),
    ("GET", "/Examine/GetPATROLDetail", {"PATROLId": 1}, "巡检明细"),
    ("POST", "/Examine/GetEXAMINEList", {"PageIndex": 1, "PageSize": 5}, "考核列表"),
    ("POST", "/Examine/GetMEETINGList", {"PageIndex": 1, "PageSize": 5}, "晨会列表"),
    ("POST", "/Examine/GetPATROLList", {"PageIndex": 1, "PageSize": 5}, "巡检列表"),
    ("GET", "/Examine/WeChat_GetExamineDetail", {"ExamineId": 1}, "微信考核明细"),

    # ===== Analysis Controller =====
    ("GET", "/Analysis/GetANALYSISINSDetail", {"ANALYSISINSId": 1}, "分析明细"),
    ("POST", "/Analysis/GetANALYSISINSList", {"PageIndex": 1, "PageSize": 5}, "分析列表"),
    ("GET", "/Analysis/GetShopMerchant", {"ShopName": "便利"}, "门店商家"),

    # ===== Budget Controller =====
    ("GET", "/Budget/GetBUDGETPROJECT_AHDetail", {"BUDGETPROJECT_AHId": 1}, "预算明细"),
    ("POST", "/Budget/GetBUDGETPROJECT_AHList", {"PageIndex": 1, "PageSize": 5}, "预算列表"),

    # ===== BaseInfo Controller (已实现的) =====
    ("GET", "/BaseInfo/GetSPRegionList", {"Province_Code": "3544"}, "片区列表"),
    ("GET", "/BaseInfo/GetBusinessTradeList", {"pushProvinceCode": "3544"}, "业态列表"),
    ("GET", "/BaseInfo/GetServerPartList", {"Province_Code": "3544"}, "服务区列表"),
    ("GET", "/BaseInfo/GetOwnerUnitListByProvinceCode", {"Province_Code": "3544"}, "业主单位"),
    ("GET", "/BaseInfo/GetBrandList", {"pushProvinceCode": "3544"}, "品牌列表"),
]

def call_api(base, method, path, params):
    """调用接口"""
    url = base + path
    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            resp = requests.post(url, json=params, timeout=TIMEOUT)
        return resp.status_code, resp.json()
    except requests.exceptions.Timeout:
        return 0, {"error": "TIMEOUT"}
    except Exception as e:
        return -1, {"error": str(e)}

def compare_result(old_data, new_data):
    """比较结果"""
    old_code = old_data.get("Result_Code", old_data.get("error"))
    new_code = new_data.get("Result_Code", new_data.get("error"))
    
    if old_code == new_code:
        # 进一步比对 Data 内容
        old_d = old_data.get("Result_Data")
        new_d = new_data.get("Result_Data")
        if old_d is None and new_d is None:
            return "PASS", "Code一致，无数据"
        if isinstance(old_d, dict) and isinstance(new_d, dict):
            old_total = old_d.get("TotalCount", "N/A")
            new_total = new_d.get("TotalCount", "N/A")
            if old_total != new_total and old_total != "N/A":
                return "WARN", f"Code一致, 总数不同: old={old_total} new={new_total}"
            return "PASS", f"Code一致, TotalCount={new_total}"
        return "PASS", f"Code一致={old_code}"
    else:
        return "DIFF", f"old_code={old_code}, new_code={new_code}"

def main():
    print(f"{'='*80}")
    print(f"接口对比测试 v2 | {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Old API: {OLD_BASE}")
    print(f"New API: {NEW_BASE}")
    print(f"{'='*80}\n")

    results = {"PASS": 0, "WARN": 0, "DIFF": 0, "SKIP": 0}
    details = []

    for method, path, params, desc in TEST_CASES:
        print(f"Testing: [{method}] {path} ({desc})...", end=" ", flush=True)
        
        old_status, old_data = call_api(OLD_BASE, method, path, params)
        new_status, new_data = call_api(NEW_BASE, method, path, params)

        if old_status == 0 or old_status == -1:
            status = "SKIP"
            msg = f"原API异常: {old_data.get('error', 'unknown')}"
        elif old_status == 404:
            status = "SKIP"
            msg = "原API返回404"
        elif new_status != 200:
            status = "DIFF"
            msg = f"新API HTTP {new_status}"
        else:
            status, msg = compare_result(old_data, new_data)

        icon = {"PASS": "✅", "WARN": "⚠️", "DIFF": "❌", "SKIP": "⏭️"}[status]
        print(f"{icon} {status}: {msg}")
        
        results[status] += 1
        details.append({
            "method": method, "path": path, "desc": desc,
            "status": status, "msg": msg,
            "old_code": old_data.get("Result_Code") if isinstance(old_data, dict) else None,
            "new_code": new_data.get("Result_Code") if isinstance(new_data, dict) else None
        })

    print(f"\n{'='*80}")
    print(f"测试完成: ✅PASS={results['PASS']} ⚠️WARN={results['WARN']} ❌DIFF={results['DIFF']} ⏭️SKIP={results['SKIP']}")
    print(f"{'='*80}")

    # 输出 DIFF 详情
    diff_items = [d for d in details if d["status"] == "DIFF"]
    if diff_items:
        print(f"\n--- DIFF 详情 ---")
        for d in diff_items:
            print(f"  [{d['method']}] {d['path']} ({d['desc']}): {d['msg']}")
            # 重新获取完整数据用于分析
            _, old_full = call_api(OLD_BASE, d["method"], d["path"], 
                                   next(p for m, pt, p, ds in TEST_CASES if pt == d["path"]))
            _, new_full = call_api(NEW_BASE, d["method"], d["path"],
                                   next(p for m, pt, p, ds in TEST_CASES if pt == d["path"]))
            print(f"    Old Result_Code: {old_full.get('Result_Code')}, Msg: {old_full.get('Result_Msg', '')[:80]}")
            print(f"    New Result_Code: {new_full.get('Result_Code')}, Msg: {new_full.get('Result_Msg', '')[:80]}")

    # 保存结果
    with open("scripts/test_results/compare_v2.json", "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到: scripts/test_results/compare_v2.json")

if __name__ == "__main__":
    main()
