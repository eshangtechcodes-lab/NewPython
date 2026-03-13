# -*- coding: utf-8 -*-
"""
全量接口对比测试 - 覆盖全部 124 个路由
旧 API: http://127.0.0.1:8900/CommercialApi
新 API: http://127.0.0.1:8080/CommercialApi
超时 30s
"""
import requests, json, time, sys, os, re

OLD = "http://127.0.0.1:8900/CommercialApi"
NEW = "http://127.0.0.1:8080/CommercialApi"
TIMEOUT = 15

# 自动从 router 文件提取所有路由
def extract_routes():
    router_dir = r"D:\Projects\Python\eshang_api\routers\commercial_api"
    routes = []
    for fname in sorted(os.listdir(router_dir)):
        if not fname.endswith(".py") or fname == "__init__.py":
            continue
        path_ = os.path.join(router_dir, fname)
        with open(path_, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r'@router\.(get|post)\(["\'](.+?)["\']', content):
            method = m.group(1).upper()
            route = m.group(2)
            routes.append((method, route))
    return routes

# 为不同接口构造默认测试参数
def get_test_params(method, route):
    """根据路由和方法返回合理的测试参数"""
    r = route.lower()
    
    # POST list 接口用分页参数 + 服务区过滤（加速旧API）
    if method == "POST" and ("list" in r or "getbusiness" in r):
        return {"PageIndex": 1, "PageSize": 3, "SearchParameter": {"SERVERPART_IDS": "416,417,418,419"}}
    
    # POST 加密接口用空 body
    if method == "POST":
        return {"name": "", "value": ""}
    
    # GET detail 接口 - 根据表名猜测 ID 参数
    if "examinedetail" in r:
        return {"EXAMINEId": 10}
    if "meetingdetail" in r:
        return {"MEETINGId": 10}
    if "patroldetail" in r:
        return {"PATROLId": 10}
    if "analysisinsdetail" in r:
        return {"ANALYSISINSId": 1}
    if "budgetproject_ahdetail" in r:
        return {"BUDGETPROJECT_AHId": 303}
    if "budgetmainshow" in r:
        return {"BUDGETPROJECT_AHId": 17}
    if "deletebudgetproject" in r or "deletebudget" in r:
        return {"BUDGETPROJECT_AHId": 99999}
    
    # BaseInfo 接口
    if "spregionlist" in r:
        return {"Province_Code": "340000"}
    if "businesstradelist" in r:
        return {"pushProvinceCode": "340000"}
    if "shopcountlist" in r:
        return {"Province_Code": "340000"}
    if "serverpartinfo" in r:
        return {"Province_Code": "340000", "Serverpart_ID": "416"}
    if "brandanalysis" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "serverpartlist" in r or "serverpartinfo" in r or "serverinfotree" in r:
        return {"Province_Code": "340000"}
    if "serverpartservicesummary" in r or "brandstructure" in r:
        return {"name": "", "value": ""}
    
    # Analysis
    if "shoprevenue" in r:
        return {"ShopName": "便利", "StartDate": "2026-01-01", "EndDate": "2026-03-01"}
    if "shopmerchant" in r:
        return {"ShopName": "便利"}
    if "translatesentence" in r:
        return {"Sentence": "test", "DialogCode": "", "ProvinceCode": "340000"}
    if "mapconfigbyprovinc" in r:
        return {"ProvinceCode": "340000"}
    if "verifywxcode" in r:
        return {"msg_signature": "", "timestamp": "", "nonce": "", "echostr": ""}
    
    # BigData - 按具体接口构造参数
    if "monthanalysis" in r and "province" not in r:
        return {"ProvinceCode": "340000", "StatisticsDate": "2026-01-15", "Serverpart_ID": "416"}
    if "provincemonthanalysis" in r:
        return {"StatisticsMonth": "202601", "ProvinceCode": "340000"}
    if "dateanalysis" in r:
        return {"StartDate": "2026-01-01", "EndDate": "2026-01-31", "Serverpart_ID": 416}
    if "correctbayonet" in r:
        return {"ServerpartId": 416, "StartDate": "2026-01-01", "EndDate": "2026-01-31", "ReferenceStartDate": "2025-12-01", "ReferenceEndDate": "2025-12-31"}
    if "bayonetentry" in r or "bayonetstalist" in r:
        return {"StatisticsDate": "2026-01-15", "Serverpart_ID": 416}
    if "bayonetoalist" in r or "bayonetprovinceoa" in r:
        return {"StatisticsMonth": "202601", "Serverpart_ID": 416}
    if "spbayonet" in r or "bayonetrank" in r or "avgbayonet" in r:
        return {"Statistics_Date": "2026-01-15", "Province_Code": "340000"}
    if "provinceavgbayonet" in r:
        return {"Province_Code": "340000", "Statistics_Date": "2026-01-15"}
    if "bayonetstanalysis" in r:
        return {"StartMonth": "202601", "EndMonth": "202603", "Province_Code": "340000"}
    if "bayonetwarning" in r and "holiday" not in r:
        return {"StatisticsDate": "2026-01-15"}
    if "holidaybayonetwarning" in r:
        return {"StatisticsDate": "2026-01-15"}
    if "bayonetgrowth" in r:
        return {"pushProvinceCode": "340000", "StatisticsStartDate": "2026-01-01", "StatisticsEndDate": "2026-01-31"}
    if "bayonetcompare" in r:
        return {"pushProvinceCode": "340000", "StatisticsStartDate": "2026-01-01", "StatisticsEndDate": "2026-01-31"}
    if "holidaycompare" in r and "bigdata" in r:
        return {"pushProvinceCode": "340000"}
    if "bayonetoaanalysis" in r:
        return {"StartMonth": "202601", "EndMonth": "202603"}
    if "bigdata" in r or "bayonet" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    
    # Contract
    if "contractanalysis" in r:
        return {"ProvinceCode": "340000", "StartMonth": "202601", "EndMonth": "202603"}
    if "merchantaccountsplit" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416}
    if "merchantaccountdetail" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416}
    
    # Customer - 按具体接口构造参数
    if "analysisdesclist" in r:
        return {"statisticsMonth": "202601", "serverpartId": 416, "statisticsType": 1}
    if "analysisdescdetail" in r:
        return {"statisticsType": 1, "statisticsMonth": "202601", "serverpartId": 416}
    if "customersaleratio" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "customer" in r or "analysisdesc" in r:
        return {"serverpartId": 416, "statisticsMonth": "202601"}
    
    # Examine WeChat
    if "wechat_getexaminedetail" in r:
        return {"ExamineId": 10}
    if "wechat_getexaminelist" in r:
        return {"SPRegionType_ID": "", "Serverpart_ID": "", "SearchStartDate": "", "SearchEndDate": ""}
    if "wechat_getpatrollist" in r:
        return {"SPRegionType_ID": "", "Serverpart_ID": "", "SearchStartDate": "", "SearchEndDate": ""}
    if "wechat_getmeetinglist" in r:
        return {"SPRegionType_ID": "", "Serverpart_ID": "", "SearchStartDate": "", "SearchEndDate": ""}
    if "wechat_" in r:
        return {"ExamineId": 10}
    if "patrolanalysis" in r:
        return {"provinceCode": "340000", "StartDate": "2026-01-01", "EndDate": "2026-03-01"}
    if "examineanalysis" in r:
        return {"provinceCode": "340000", "StartMonth": "202601", "EndMonth": "202603"}
    if "examineresultlist" in r:
        return {"provinceCode": "340000", "StartMonth": "202601", "EndMonth": "202603"}
    if "patrolresultlist" in r:
        return {"provinceCode": "340000", "StartDate": "2026-01-01", "EndDate": "2026-03-01"}
    if "resultlist" in r:
        return {"provinceCode": "340000", "StartMonth": "202601", "EndMonth": "202603"}
    
    # Revenue - 按具体接口构造
    if "revenuepush" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416", "StatisticsMonth": "202601"}
    if "summaryrevenuemonth" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601", "Serverpart_ID": "416"}
    if "summaryrevenue" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "wechatpushsales" in r:
        return {"ProvinceCode": "340000", "pushDate": "2026-01-15", "Serverpart_ID": "416"}
    if "unuploadshops" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416", "Statistics_Date": "2026-01-15"}
    if "serverpartbrand" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416}
    if "serverpartendaccountlist" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "shopendaccountlist" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "getbudgetexpenselist" in r and method == "GET":
        return {"ProvinceCode": "340000"}
    if "revenuebudget" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601", "Serverpart_ID": "416"}
    if "mobileshare" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601", "Serverpart_ID": "416"}
    if "malldeliver" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601", "Serverpart_ID": "416"}
    if "transactiondetail" in r:
        return {"ProvinceCode": "340000", "ServerpartId": "416"}
    if "transactiontime" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "transactionconvert" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "transactionanalysis" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "businesstradelevel" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "businessbrandlevel" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "revenuereportdetil" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "revenuereport" in r and "company" not in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "sprevenuerank" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "revenueyoy" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "companyrevenuereport" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "accountreceivable" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416}
    if "shopcurrevenue" in r:
        return {"serverPartId": "416", "statisticsDate": "2026-01-15"}
    if "currevenue" in r:
        return {"pushProvinceCode": "340000", "StatisticsDate": "2026-01-15"}
    if "lastsync" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "holidayanalysisbatch" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "holidayanalysis" in r and "batch" not in r:
        return {"ProvinceCode": "340000", "holidayType": 0}
    if "holidaycompare" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416}
    if "serverpartincanalysis" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "shopincanalysis" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "monthlybusinessanalysis" in r:
        return {"ProvinceCode": "340000", "StatisticsMonth": "202601"}
    if "monthlyspincanalysis" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416, "StatisticsMonth": "202601"}
    if "holidayrevenueratio" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "revenue" in r or "budget" in r or "mobile" in r or "mall" in r or "transaction" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "upload" in r or "endaccount" in r or "brand" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "sync" in r or "cur" in r or "last" in r or "holiday" in r or "inc" in r or "monthly" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": "416"}
    if "company" in r:
        return {"ProvinceCode": "340000"}
    
    # BusinessProcess
    if "businessprocesslist" in r:
        return {"ProvinceCode": "340000", "Serverpart_ID": 416}
    if "businessprocess" in r:
        return {"ProvinceCode": "340000"}
    
    # Suggestion
    if "memberunread" in r:
        return {"ProvinceCode": "340000", "Member_ID": 1}
    if "suggestion" in r or "member" in r:
        return {"ProvinceCode": "340000"}
    
    # SupplyChain
    if "supplychain" in r or "supplier" in r or "dashboard" in r or "mallorder" in r or "welfare" in r:
        return {"name": "", "value": ""}
    
    # Budget
    if "deletebudget" in r:
        return {"BUDGETPROJECT_AHId": 99999}  # 不存在的ID避免误删
    if "synchrobudget" in r:
        return {}
    
    # 默认
    return {"ProvinceCode": "340000"}

def call(base, method, path, params):
    url = base + path
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

def info(status, data):
    if status == 0:
        return "TIMEOUT"
    if status != 200:
        return f"HTTP{status}"
    code = data.get("Result_Code")
    rd = data.get("Result_Data")
    if isinstance(rd, dict):
        total = rd.get("TotalCount")
        if total is not None:
            return f"C={code},T={total}"
    return f"C={code}"

def main():
    routes = extract_routes()
    print(f"\n{'='*110}")
    print(f"全量接口对比 | {time.strftime('%H:%M:%S')} | 共{len(routes)}个路由 | Timeout={TIMEOUT}s")
    print(f"Old: {OLD}")
    print(f"New: {NEW}")
    print(f"{'='*110}")
    
    stats = {"PASS": 0, "DIFF": 0, "SKIP": 0}
    all_results = []
    
    for i, (method, route) in enumerate(routes, 1):
        params = get_test_params(method, route)
        # 提取 controller 名
        parts = route.split("/")
        ctrl = parts[1] if len(parts) > 1 else "?"
        action = parts[2] if len(parts) > 2 else route
        
        sys.stdout.write(f"[{i:3d}/{len(routes)}] {method:4s} {route:55s} ")
        sys.stdout.flush()
        
        os_code, od = call(OLD, method, route, params)
        ns_code, nd = call(NEW, method, route, params)
        
        oi = info(os_code, od)
        ni = info(ns_code, nd)
        
        if os_code != 200:
            result = "SKIP"
        elif ns_code != 200:
            result = "DIFF"
        else:
            oc = od.get("Result_Code")
            nc = nd.get("Result_Code")
            if oc == nc:
                # 进一步比对TotalCount
                ord_d = od.get("Result_Data") or {}
                nrd_d = nd.get("Result_Data") or {}
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
        
        icon = {"PASS": "V", "DIFF": "X", "SKIP": "-"}[result]
        print(f"{oi:18s} {ni:18s} [{icon}]{result}")
        sys.stdout.flush()
        stats[result] += 1
        all_results.append({
            "idx": i, "method": method, "route": route, "ctrl": ctrl,
            "old": oi, "new": ni, "result": result
        })
    
    print(f"\n{'='*110}")
    total = sum(stats.values())
    print(f"全量对比完成: PASS={stats['PASS']}/{total}  DIFF={stats['DIFF']}  SKIP={stats['SKIP']}")
    print(f"{'='*110}")
    
    # 按 controller 分组汇总
    from collections import defaultdict
    ctrl_stats = defaultdict(lambda: {"PASS": 0, "DIFF": 0, "SKIP": 0, "total": 0})
    for r in all_results:
        ctrl_stats[r["ctrl"]][r["result"]] += 1
        ctrl_stats[r["ctrl"]]["total"] += 1
    
    print(f"\n--- 按 Controller 汇总 ---")
    print(f"{'Controller':25s} {'总数':5s} {'PASS':5s} {'DIFF':5s} {'SKIP':5s}")
    for ctrl in sorted(ctrl_stats.keys()):
        s = ctrl_stats[ctrl]
        print(f"{ctrl:25s} {s['total']:5d} {s['PASS']:5d} {s['DIFF']:5d} {s['SKIP']:5d}")
    
    # DIFF 详情
    diffs = [r for r in all_results if r["result"] == "DIFF"]
    if diffs:
        print(f"\n--- DIFF 详情 ({len(diffs)}个) ---")
        for d in diffs:
            print(f"  {d['method']:4s} {d['route']:55s} old={d['old']:18s} new={d['new']}")
    
    # 保存完整结果
    os.makedirs("scripts/test_results", exist_ok=True)
    with open("scripts/test_results/compare_all.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n完整结果已保存: scripts/test_results/compare_all.json")

if __name__ == "__main__":
    main()
