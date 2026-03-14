# -*- coding: utf-8 -*-
"""
新 API 接口自验脚本 - 简洁版
直接验证 Python API (8080) 各接口能否查出真实数据
"""
import requests
import json
import time
import sys

BASE = "http://127.0.0.1:8080/CommercialApi"
TIMEOUT = 10

def call(method, path, params):
    url = BASE + path
    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            resp = requests.post(url, json=params, timeout=TIMEOUT)
        if resp.status_code != 200:
            return "FAIL", f"HTTP {resp.status_code}"
        data = resp.json()
        code = data.get("Result_Code")
        result_data = data.get("Result_Data")
        if code == 100:
            if isinstance(result_data, dict):
                total = result_data.get("TotalCount")
                items = result_data.get("Items")
                if total is not None:
                    return "PASS", f"TotalCount={total}"
                else:
                    keys = list(result_data.keys())[:3]
                    return "PASS", f"字段={keys}"
            return "PASS", "OK"
        elif code == 101:
            return "NODATA", "无数据"
        else:
            return "FAIL", f"Code={code}"
    except Exception as e:
        return "FAIL", str(e)[:60]

tests = [
    ("GET", "/BaseInfo/GetSPRegionList", {"Province_Code": "3544"}, "片区列表"),
    ("GET", "/BaseInfo/GetBusinessTradeList", {"pushProvinceCode": "3544"}, "业态列表"),
    ("GET", "/BaseInfo/GetServerPartList", {"Province_Code": "3544"}, "服务区列表"),
    ("GET", "/BaseInfo/GetOwnerUnitListByProvinceCode", {"Province_Code": "3544"}, "业主单位"),
    ("GET", "/BaseInfo/GetBrandList", {"pushProvinceCode": "3544"}, "品牌列表"),
    ("POST", "/Examine/GetEXAMINEList", {"PageIndex": 1, "PageSize": 3}, "考核列表"),
    ("GET", "/Examine/GetEXAMINEDetail", {"EXAMINEId": 10}, "考核明细"),
    ("POST", "/Examine/GetMEETINGList", {"PageIndex": 1, "PageSize": 3}, "晨会列表"),
    ("GET", "/Examine/GetMEETINGDetail", {"MEETINGId": 10}, "晨会明细"),
    ("POST", "/Examine/GetPATROLList", {"PageIndex": 1, "PageSize": 3}, "巡检列表"),
    ("GET", "/Examine/GetPATROLDetail", {"PATROLId": 10}, "巡检明细"),
    ("GET", "/Examine/WeChat_GetExamineDetail", {"ExamineId": 10}, "微信考核明细"),
    ("POST", "/Analysis/GetANALYSISINSList", {"PageIndex": 1, "PageSize": 3}, "分析列表"),
    ("GET", "/Analysis/GetANALYSISINSDetail", {"ANALYSISINSId": 1}, "分析明细"),
    ("GET", "/Analysis/GetShopMerchant", {"ShopName": "便利"}, "门店商家"),
    ("POST", "/Budget/GetBUDGETPROJECT_AHList", {"PageIndex": 1, "PageSize": 3}, "预算列表"),
    ("GET", "/Budget/GetBUDGETPROJECT_AHDetail", {"BUDGETPROJECT_AHId": 1}, "预算明细"),
    ("GET", "/Budget/GetBudgetMainShow", {"BUDGETPROJECT_AHId": 1}, "预算主页"),
]

results = {"PASS": 0, "FAIL": 0, "NODATA": 0}
print(f"\n{'='*70}")
print(f"接口自验 | {time.strftime('%H:%M:%S')} | {BASE}")
print(f"{'='*70}")
for method, path, params, desc in tests:
    status, msg = call(method, path, params)
    icon = {"PASS": "✅", "FAIL": "❌", "NODATA": "⚠️"}[status]
    print(f"{icon} {desc:12s} [{method:4s}] {path:50s} {msg}")
    results[status] += 1
    sys.stdout.flush()
print(f"{'='*70}")
print(f"结果: ✅PASS={results['PASS']} ❌FAIL={results['FAIL']} ⚠️NODATA={results['NODATA']}")
