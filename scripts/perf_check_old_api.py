# -*- coding: utf-8 -*-
"""
原 C# API 性能分析脚本
测试 http://127.0.0.1:8900/CommercialApi 所有接口的响应时间
目的：找出慢接口，分析根因
"""
import requests
import json
import time
import sys
import os

OLD_BASE = "http://127.0.0.1:8900/CommercialApi"
TIMEOUT = 60  # 用较长超时来获取真实响应时间

# 需要测试的接口列表（从 compare_all.json 提取出所有非404接口）
TEST_CASES = [
    # BaseInfo
    ("GET",  "/BaseInfo/GetSPRegionList",            {"Province_Code": "340000"}),
    ("GET",  "/BaseInfo/GetBusinessTradeList",        {"Province_Code": "340000"}),
    ("POST", "/BaseInfo/GetBusinessTradeList",        {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("POST", "/BaseInfo/GetShopCountList",            {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/BaseInfo/GetBrandAnalysis",            {"Province_Code": "340000"}),
    ("GET",  "/BaseInfo/GetServerpartList",           {"Province_Code": "340000"}),
    ("POST", "/BaseInfo/GetServerpartServiceSummary", {"ProvinceCode": "340000"}),
    ("POST", "/BaseInfo/GetBrandStructureAnalysis",   {"ProvinceCode": "340000"}),
    
    # Examine
    ("POST", "/Examine/GetEXAMINEList",       {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/Examine/GetEXAMINEDetail",     {"ID": "1"}),
    ("POST", "/Examine/GetMEETINGList",       {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/Examine/GetMEETINGDetail",     {"ID": "1"}),
    ("POST", "/Examine/GetPATROLList",        {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/Examine/GetPATROLDetail",      {"ID": "1"}),
    ("GET",  "/Examine/WeChat_GetExamineList",{"Province_Code": "340000"}),
    ("GET",  "/Examine/WeChat_GetExamineDetail", {"ID": "1"}),
    ("GET",  "/Examine/WeChat_GetPatrolList", {"Province_Code": "340000"}),
    ("GET",  "/Examine/WeChat_GetMeetingList",{"Province_Code": "340000"}),
    ("GET",  "/Examine/GetPatrolAnalysis",    {"Province_Code": "340000"}),
    ("GET",  "/Examine/GetExamineAnalysis",   {"Province_Code": "340000"}),
    ("GET",  "/Examine/GetExamineResultList", {"Province_Code": "340000"}),
    ("GET",  "/Examine/GetPatrolResultList",  {"Province_Code": "340000"}),
    
    # Analysis
    ("POST", "/Analysis/GetANALYSISINSList",  {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/Analysis/GetANALYSISINSDetail",{"ID": "1"}),
    ("GET",  "/Analysis/GetShopRevenue",      {"Province_Code": "340000"}),
    ("GET",  "/Analysis/GetShopMerchant",     {"Province_Code": "340000", "SERVERPART_ID": "1"}),
    ("POST", "/Analysis/GetTransactionAnalysis", {"ProvinceCode": "340000"}),
    ("GET",  "/Analysis/TranslateSentence",   {"sentence": "test"}),
    ("GET",  "/Analysis/GetMapConfigByProvinceCode", {"Province_Code": "340000"}),
    ("POST", "/Analysis/GetServerpartTypeAnalysis",  {"ProvinceCode": "340000"}),
    
    # Budget
    ("POST", "/Budget/GetBUDGETPROJECT_AHList",  {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/Budget/GetBUDGETPROJECT_AHDetail", {"ID": "1"}),
    
    # BigData
    ("GET",  "/BigData/GetMonthAnalysis",         {"Province_Code": "340000"}),
    ("GET",  "/BigData/GetProvinceMonthAnalysis",  {"Province_Code": "340000"}),
    ("GET",  "/BigData/GetBayonetGrowthAnalysis",  {"Province_Code": "340000"}),
    ("GET",  "/BigData/GetBayonetCompare",         {"Province_Code": "340000"}),
    ("GET",  "/BigData/GetDateAnalysis",           {"Province_Code": "340000"}),
    ("GET",  "/BigData/CorrectBayonet",            {"Province_Code": "340000"}),
    
    # Revenue
    ("POST", "/Revenue/GetBudgetExpenseList",       {"ProvinceCode": "340000", "PageIndex": 1, "PageSize": 10}),
    ("GET",  "/Revenue/GetHolidayRevenueRatio",     {"Province_Code": "340000"}),
    ("POST", "/Revenue/GetBusinessRevenueList",     {"ProvinceCode": "340000"}),
    ("POST", "/Revenue/GetMonthlyBusinessRevenue",  {"ProvinceCode": "340000"}),
    ("GET",  "/Revenue/GetLastSyncDateTime",        {}),
    ("GET",  "/Revenue/GetTransactionDetailList",   {"Province_Code": "340000"}),
    
    # AbnormalAudit
    ("POST", "/AbnormalAudit/GetCurrentEarlyWarning", {"ProvinceCode": "340000"}),
    ("POST", "/AbnormalAudit/GetMonthEarlyWarning",   {"ProvinceCode": "340000"}),
    
    # Customer
    ("GET",  "/Customer/GetAnalysisDescList",   {"Province_Code": "340000"}),
    ("GET",  "/Customer/GetAnalysisDescDetail", {"ID": "1"}),
    
    # SupplyChain
    ("POST", "/SupplyChain/GetMemberDashboard",  {"ProvinceCode": "340000"}),
    ("POST", "/SupplyChain/GetSupplierTypeList", {"ProvinceCode": "340000"}),
    ("POST", "/SupplyChain/GetSupplierList",     {"ProvinceCode": "340000"}),
    ("POST", "/SupplyChain/GetMallOrderSummary", {"ProvinceCode": "340000"}),
    ("POST", "/SupplyChain/GetWelFareSummary",   {"ProvinceCode": "340000"}),
]

def test_endpoint(method, path, params):
    """测试单个接口的响应时间"""
    url = OLD_BASE + path
    start = time.time()
    try:
        if method == "GET":
            r = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            r = requests.post(url, json=params, timeout=TIMEOUT)
        elapsed = time.time() - start
        
        status_code = r.status_code
        try:
            data = r.json()
            result_code = data.get("Result_Code", None)
            total_count = data.get("TotalCount", data.get("Result_Data", {}).get("TotalCount", None)) if isinstance(data, dict) else None
        except:
            result_code = None
            total_count = None
        
        return {
            "method": method,
            "path": path,
            "http_status": status_code,
            "result_code": result_code,
            "total_count": total_count,
            "elapsed_sec": round(elapsed, 3),
            "status": "OK" if status_code == 200 else f"HTTP{status_code}"
        }
    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        return {
            "method": method,
            "path": path,
            "http_status": 0,
            "result_code": None,
            "total_count": None,
            "elapsed_sec": round(elapsed, 3),
            "status": f"TIMEOUT(>{TIMEOUT}s)"
        }
    except Exception as e:
        elapsed = time.time() - start
        return {
            "method": method,
            "path": path,
            "http_status": -1,
            "result_code": None,
            "total_count": None,
            "elapsed_sec": round(elapsed, 3),
            "status": f"ERROR: {str(e)[:60]}"
        }

def main():
    print(f"=== 原 C# API 性能分析 ===")
    print(f"地址: {OLD_BASE}")
    print(f"超时: {TIMEOUT}s")
    print(f"接口数: {len(TEST_CASES)}")
    print(f"{'='*100}")
    
    results = []
    slow_threshold = 5.0  # 5秒以上视为慢接口
    
    for i, (method, path, params) in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{len(TEST_CASES)}] {method} {path} ...", end="", flush=True)
        result = test_endpoint(method, path, params)
        results.append(result)
        
        # 根据耗时标记
        elapsed = result["elapsed_sec"]
        if "TIMEOUT" in result["status"]:
            tag = "⏰ TIMEOUT"
        elif elapsed > 30:
            tag = "🔴 极慢"
        elif elapsed > 10:
            tag = "🟡 慢"
        elif elapsed > 5:
            tag = "🟠 较慢"
        elif elapsed > 2:
            tag = "⚠️ 偏慢"
        else:
            tag = "✅ 正常"
        
        print(f" {elapsed:.3f}s [{result['status']}] RC={result['result_code']} {tag}")
    
    # 汇总报告
    print(f"\n{'='*100}")
    print(f"=== 性能汇总报告 ===\n")
    
    # 按耗时排序
    sorted_results = sorted(results, key=lambda x: x["elapsed_sec"], reverse=True)
    
    timeout_list = [r for r in results if "TIMEOUT" in r["status"]]
    very_slow = [r for r in results if r["elapsed_sec"] > 10 and "TIMEOUT" not in r["status"]]
    slow = [r for r in results if 5 < r["elapsed_sec"] <= 10]
    medium = [r for r in results if 2 < r["elapsed_sec"] <= 5]
    fast = [r for r in results if r["elapsed_sec"] <= 2 and "TIMEOUT" not in r["status"]]
    error_list = [r for r in results if r["http_status"] not in (0, 200)]
    
    print(f"⏰ 超时(>{TIMEOUT}s):     {len(timeout_list)} 个")
    print(f"🔴 极慢(>10s):          {len(very_slow)} 个")
    print(f"🟡 慢(5-10s):           {len(slow)} 个")
    print(f"🟠 较慢(2-5s):          {len(medium)} 个")
    print(f"✅ 正常(<2s):           {len(fast)} 个")
    print(f"❌ HTTP错误:            {len(error_list)} 个")
    
    # 输出慢接口明细
    if timeout_list:
        print(f"\n--- ⏰ 超时接口 ---")
        for r in timeout_list:
            print(f"  {r['method']:4s} {r['path']}")
    
    if very_slow:
        print(f"\n--- 🔴 极慢接口(>10s) ---")
        for r in very_slow:
            print(f"  {r['method']:4s} {r['path']}  耗时: {r['elapsed_sec']:.1f}s")
    
    if slow:
        print(f"\n--- 🟡 慢接口(5-10s) ---")
        for r in slow:
            print(f"  {r['method']:4s} {r['path']}  耗时: {r['elapsed_sec']:.1f}s")
    
    if medium:
        print(f"\n--- 🟠 较慢接口(2-5s) ---")
        for r in medium:
            print(f"  {r['method']:4s} {r['path']}  耗时: {r['elapsed_sec']:.1f}s")
    
    if error_list:
        print(f"\n--- ❌ HTTP错误接口 ---")
        for r in error_list:
            print(f"  {r['method']:4s} {r['path']}  状态: {r['status']}")
    
    # 按 Controller 汇总平均耗时
    print(f"\n--- 按 Controller 平均耗时排序 ---")
    ctrl_stats = {}
    for r in results:
        ctrl = r["path"].split("/")[1]
        if ctrl not in ctrl_stats:
            ctrl_stats[ctrl] = {"times": [], "timeouts": 0, "errors": 0}
        if "TIMEOUT" in r["status"]:
            ctrl_stats[ctrl]["timeouts"] += 1
        elif r["http_status"] != 200:
            ctrl_stats[ctrl]["errors"] += 1
        else:
            ctrl_stats[ctrl]["times"].append(r["elapsed_sec"])
    
    for ctrl, stats in sorted(ctrl_stats.items(), key=lambda x: (x[1]["timeouts"], -(sum(x[1]["times"])/max(len(x[1]["times"]),1)))):
        avg = sum(stats["times"])/max(len(stats["times"]),1)
        max_t = max(stats["times"]) if stats["times"] else 0
        print(f"  {ctrl:30s}  平均: {avg:.1f}s  最大: {max_t:.1f}s  超时: {stats['timeouts']}  HTTP错误: {stats['errors']}")
    
    # 保存结果
    os.makedirs("scripts/test_results", exist_ok=True)
    with open("scripts/test_results/perf_check.json", "w", encoding="utf-8") as f:
        json.dump(sorted_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细结果已保存: scripts/test_results/perf_check.json")

if __name__ == "__main__":
    main()
