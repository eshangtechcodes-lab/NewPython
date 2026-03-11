# -*- coding: utf-8 -*-
"""
新旧 API 对比测试脚本
对比原 C# API (8900) 和 新 Python API (8080) 的返回结果
超时设为 30 秒以适应原 API 延时
"""
import requests
import json
import time
import sys

OLD_BASE = "http://127.0.0.1:8900/api"
NEW_BASE = "http://127.0.0.1:8080/CommercialApi"
TIMEOUT = 30  # 原 API 有延时，增大超时

# 测试用例：(方法, 路径, 参数, 描述)
TESTS = [
    # BaseInfo
    ("GET", "/BaseInfo/GetSPRegionList", {"Province_Code": "3544"}, "片区列表"),
    ("GET", "/BaseInfo/GetBusinessTradeList", {"pushProvinceCode": "3544"}, "业态列表"),
    ("GET", "/BaseInfo/GetServerPartList", {"Province_Code": "3544"}, "服务区列表"),
    ("GET", "/BaseInfo/GetOwnerUnitListByProvinceCode", {"Province_Code": "3544"}, "业主单位"),

    # Examine
    ("POST", "/Examine/GetEXAMINEList", {"PageIndex": 1, "PageSize": 5}, "考核列表"),
    ("GET", "/Examine/GetEXAMINEDetail", {"EXAMINEId": 10}, "考核明细"),
    ("POST", "/Examine/GetMEETINGList", {"PageIndex": 1, "PageSize": 5}, "晨会列表"),
    ("GET", "/Examine/GetMEETINGDetail", {"MEETINGId": 10}, "晨会明细"),
    ("POST", "/Examine/GetPATROLList", {"PageIndex": 1, "PageSize": 5}, "巡检列表"),
    ("GET", "/Examine/GetPATROLDetail", {"PATROLId": 10}, "巡检明细"),
    ("GET", "/Examine/WeChat_GetExamineDetail", {"ExamineId": 10}, "微信考核明细"),

    # Analysis
    ("POST", "/Analysis/GetANALYSISINSList", {"PageIndex": 1, "PageSize": 5}, "分析列表"),
    ("GET", "/Analysis/GetANALYSISINSDetail", {"ANALYSISINSId": 1}, "分析明细"),
    ("GET", "/Analysis/GetShopMerchant", {"ShopName": "便利"}, "门店商家"),

    # Budget
    ("POST", "/Budget/GetBUDGETPROJECT_AHList", {"PageIndex": 1, "PageSize": 5}, "预算列表"),
    ("GET", "/Budget/GetBUDGETPROJECT_AHDetail", {"BUDGETPROJECT_AHId": 1}, "预算明细"),
]

def call_api(base, method, path, params):
    url = base + path
    try:
        if method == "GET":
            r = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            r = requests.post(url, json=params, timeout=TIMEOUT)
        return r.status_code, r.json() if r.status_code == 200 else {}
    except requests.exceptions.Timeout:
        return 0, {"_err": "TIMEOUT"}
    except Exception as e:
        return -1, {"_err": str(e)[:80]}

def extract_info(data):
    """提取关键信息用于对比"""
    code = data.get("Result_Code")
    rd = data.get("Result_Data")
    if isinstance(rd, dict):
        total = rd.get("TotalCount")
        items = rd.get("Items")
        item_count = len(items) if isinstance(items, list) else None
        return code, total, item_count
    return code, None, None

def main():
    print(f"\n{'='*90}")
    print(f"新旧 API 对比测试 | {time.strftime('%Y-%m-%d %H:%M:%S')} | Timeout={TIMEOUT}s")
    print(f"Old: {OLD_BASE}")
    print(f"New: {NEW_BASE}")
    print(f"{'='*90}")
    print(f"{'描述':12s} {'方法':5s} {'路径':50s} {'旧API':15s} {'新API':15s} {'结果':6s}")
    print(f"{'-'*90}")

    stats = {"PASS": 0, "DIFF": 0, "SKIP": 0}
    details = []

    for method, path, params, desc in TESTS:
        sys.stdout.write(f"{desc:12s} [{method:4s}] {path:50s} ")
        sys.stdout.flush()

        old_status, old_data = call_api(OLD_BASE, method, path, params)
        new_status, new_data = call_api(NEW_BASE, method, path, params)

        old_code, old_total, old_items = extract_info(old_data)
        new_code, new_total, new_items = extract_info(new_data)

        # 旧 API 异常
        if old_status == 0:
            result = "SKIP"
            old_info = "TIMEOUT"
            new_info = f"C={new_code}"
        elif old_status == 404:
            result = "SKIP"
            old_info = "404"
            new_info = f"C={new_code}"
        elif old_status != 200:
            result = "SKIP"
            old_info = f"HTTP{old_status}"
            new_info = f"C={new_code}"
        elif new_status != 200:
            result = "DIFF"
            old_info = f"C={old_code}"
            new_info = f"HTTP{new_status}"
        else:
            # 两端都正常
            old_info = f"C={old_code}"
            new_info = f"C={new_code}"
            if old_total is not None:
                old_info += f",T={old_total}"
            if new_total is not None:
                new_info += f",T={new_total}"

            if old_code == new_code:
                if old_total is not None and new_total is not None:
                    if old_total == new_total:
                        result = "PASS"
                    else:
                        result = "DIFF"
                else:
                    result = "PASS"
            else:
                result = "DIFF"

        icon = {"PASS": "✅", "DIFF": "❌", "SKIP": "⏭️"}[result]
        print(f"{old_info:15s} {new_info:15s} {icon}{result}")
        stats[result] += 1

        details.append({
            "desc": desc, "method": method, "path": path,
            "old_code": old_code, "old_total": old_total,
            "new_code": new_code, "new_total": new_total,
            "result": result
        })

    print(f"{'='*90}")
    print(f"汇总: ✅PASS={stats['PASS']} ❌DIFF={stats['DIFF']} ⏭️SKIP={stats['SKIP']}")
    print(f"{'='*90}")

    # 打印 DIFF 详情
    diffs = [d for d in details if d["result"] == "DIFF"]
    if diffs:
        print(f"\n--- DIFF 详情 ---")
        for d in diffs:
            print(f"  {d['desc']}: old(Code={d['old_code']}, Total={d['old_total']}) vs new(Code={d['new_code']}, Total={d['new_total']})")

    # 保存结果
    with open("scripts/test_results/compare_final.json", "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
