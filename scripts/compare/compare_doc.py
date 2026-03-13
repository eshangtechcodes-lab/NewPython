# -*- coding: utf-8 -*-
"""
新旧 API 对比测试（基于接口文档的正确参数）
旧 API: http://127.0.0.1:8900/CommercialApi/
新 API: http://127.0.0.1:8080/CommercialApi/
超时 30s 适应原 API 延时
"""
import requests
import json
import time
import sys

OLD = "http://127.0.0.1:8900/CommercialApi"
NEW = "http://127.0.0.1:8080/CommercialApi"
TIMEOUT = 30

# 文档中的真实测试参数
TESTS = [
    # BaseInfo — 文档中的真实参数
    ("GET", "/BaseInfo/GetBrandAnalysis",
     {"ProvinceCode": "340000", "Serverpart_ID": "416", "Statistics_Date": "2026-02-13", "ShowAllShop": "false"},
     "品牌分析"),
    ("GET", "/BaseInfo/GetSPRegionList",
     {"Province_Code": "340000"},
     "片区列表"),
    ("GET", "/BaseInfo/GetBusinessTradeList",
     {"pushProvinceCode": "340000"},
     "业态列表"),
    ("GET", "/BaseInfo/GetServerPartList",
     {"Province_Code": "340000"},
     "服务区列表"),
    ("GET", "/BaseInfo/GetOwnerUnitListByProvinceCode",
     {"Province_Code": "340000"},
     "业主单位"),

    # Examine
    ("POST", "/Examine/GetEXAMINEList",
     {"PageIndex": 1, "PageSize": 5},
     "考核列表"),
    ("GET", "/Examine/GetEXAMINEDetail",
     {"EXAMINEId": 10},
     "考核明细"),
    ("POST", "/Examine/GetMEETINGList",
     {"PageIndex": 1, "PageSize": 5},
     "晨会列表"),
    ("GET", "/Examine/GetMEETINGDetail",
     {"MEETINGId": 10},
     "晨会明细"),
    ("POST", "/Examine/GetPATROLList",
     {"PageIndex": 1, "PageSize": 5},
     "巡检列表"),
    ("GET", "/Examine/GetPATROLDetail",
     {"PATROLId": 10},
     "巡检明细"),

    # Analysis
    ("POST", "/Analysis/GetANALYSISINSList",
     {"PageIndex": 1, "PageSize": 5},
     "分析列表"),
    ("GET", "/Analysis/GetANALYSISINSDetail",
     {"ANALYSISINSId": 1},
     "分析明细"),
    ("GET", "/Analysis/GetShopMerchant",
     {"ShopName": "便利"},
     "门店商家"),
    ("GET", "/Analysis/GetMapConfigByProvinceCode",
     {"ProvinceCode": "340000"},
     "地图配置"),

    # Budget
    ("POST", "/Budget/GetBUDGETPROJECT_AHList",
     {"PageIndex": 1, "PageSize": 5},
     "预算列表"),
    ("GET", "/Budget/GetBUDGETPROJECT_AHDetail",
     {"BUDGETPROJECT_AHId": 1},
     "预算明细"),
]

def call(base, method, path, params):
    url = base + path
    try:
        if method == "GET":
            r = requests.get(url, params=params, timeout=TIMEOUT)
        else:
            r = requests.post(url, json=params, timeout=TIMEOUT)
        if r.status_code != 200:
            return r.status_code, {}
        return 200, r.json()
    except requests.exceptions.Timeout:
        return 0, {"_": "TIMEOUT"}
    except Exception as e:
        return -1, {"_": str(e)[:60]}

def info(data):
    """提取摘要信息"""
    code = data.get("Result_Code")
    rd = data.get("Result_Data")
    if isinstance(rd, dict):
        total = rd.get("TotalCount")
        if total is not None:
            return f"C={code},T={total}"
        keys = list(rd.keys())[:3]
        return f"C={code},{keys}"
    return f"C={code}"

def main():
    print(f"\n{'='*100}")
    print(f"新旧 API 对比 | {time.strftime('%H:%M:%S')} | Timeout={TIMEOUT}s")
    print(f"Old: {OLD}")
    print(f"New: {NEW}")
    print(f"{'='*100}")
    print(f"{'描述':8s} {'方法':5s} {'路径':48s} {'旧API':20s} {'新API':20s} {'结果'}")
    print(f"{'-'*100}")

    stats = {"PASS": 0, "DIFF": 0, "SKIP": 0}
    all_details = []

    for method, path, params, desc in TESTS:
        sys.stdout.write(f"{desc:8s} [{method:4s}] {path:48s} ")
        sys.stdout.flush()

        os, od = call(OLD, method, path, params)
        ns, nd = call(NEW, method, path, params)

        if os == 0:
            oi = "TIMEOUT"
        elif os != 200:
            oi = f"HTTP{os}"
        else:
            oi = info(od)

        if ns == 0:
            ni = "TIMEOUT"
        elif ns != 200:
            ni = f"HTTP{ns}"
        else:
            ni = info(nd)

        # 判断结果
        if os != 200:
            result = "SKIP"
        elif ns != 200:
            result = "DIFF"
        else:
            oc = od.get("Result_Code")
            nc = nd.get("Result_Code")
            if oc == nc:
                ord_d = od.get("Result_Data") or {}
                nrd_d = nd.get("Result_Data") or {}
                ot = ord_d.get("TotalCount") if isinstance(ord_d, dict) else None
                nt = nrd_d.get("TotalCount") if isinstance(nrd_d, dict) else None
                if ot is not None and nt is not None and ot != nt:
                    result = "DIFF"
                else:
                    result = "PASS"
            else:
                result = "DIFF"

        icon = {"PASS": "✅", "DIFF": "❌", "SKIP": "⏭️"}[result]
        print(f"{oi:20s} {ni:20s} {icon}{result}")
        sys.stdout.flush()
        stats[result] += 1
        all_details.append({"desc": desc, "path": path, "old": oi, "new": ni, "result": result})

    print(f"{'='*100}")
    print(f"汇总: ✅PASS={stats['PASS']} ❌DIFF={stats['DIFF']} ⏭️SKIP={stats['SKIP']} / 共{len(TESTS)}个")
    print(f"{'='*100}")

    diffs = [d for d in all_details if d["result"] == "DIFF"]
    if diffs:
        print(f"\n--- DIFF 详情 ---")
        for d in diffs:
            print(f"  {d['desc']:8s} {d['path']:48s} old={d['old']}  new={d['new']}")

    with open("scripts/test_results/compare_doc.json", "w", encoding="utf-8") as f:
        json.dump(all_details, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
