# -*- coding: utf-8 -*-
"""
先查列表获取真实ID，再测试明细接口
覆盖旧API超时的12个接口 + 关联的明细接口
"""
import requests, json, os

os.environ["NO_PROXY"] = "*"
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

NEW = "http://127.0.0.1:8080/CommercialApi"
T = 60

def get(path, params):
    r = requests.get(NEW + path, params=params, timeout=T)
    return r.status_code, r.json() if r.status_code == 200 else {}

def post(path, params):
    r = requests.post(NEW + path, json=params, timeout=T)
    return r.status_code, r.json() if r.status_code == 200 else {}

def show(desc, status, data):
    code = data.get("Result_Code", "?")
    rd = data.get("Result_Data")
    if isinstance(rd, dict) and "TotalCount" in rd:
        print(f"  {desc}: HTTP {status}, Code={code}, TotalCount={rd['TotalCount']}")
    elif isinstance(rd, dict):
        keys = list(rd.keys())[:5]
        print(f"  {desc}: HTTP {status}, Code={code}, keys={keys}")
    elif isinstance(rd, list):
        print(f"  {desc}: HTTP {status}, Code={code}, list len={len(rd)}")
    else:
        print(f"  {desc}: HTTP {status}, Code={code}")
    return rd

print("=" * 90)
print("先列表后明细 - 旧API超时接口验证")
print("=" * 90)

# ===== 1. Examine - 考核 =====
print("\n【考核 Examine】")
s, d = post("/Examine/GetEXAMINEList", {"PageIndex": 1, "PageSize": 3})
rd = show("考核列表", s, d)
if isinstance(rd, dict) and rd.get("List"):
    eid = rd["List"][0].get("EXAMINE_ID")
    print(f"  -> 取到 EXAMINE_ID = {eid}")
    s2, d2 = get("/Examine/GetEXAMINEDetail", {"EXAMINEId": eid})
    show("考核明细", s2, d2)
    # WeChat版
    s3, d3 = get("/Examine/WeChat_GetExamineDetail", {"ExamineId": eid})
    show("微信考核明细", s3, d3)
    # WeChat列表
    s4, d4 = get("/Examine/WeChat_GetExamineList", {"ExamineId": eid})
    show("微信考核列表", s4, d4)

# ===== 2. Examine - 晨会 =====
print("\n【晨会 Meeting】")
s, d = post("/Examine/GetMEETINGList", {"PageIndex": 1, "PageSize": 3})
rd = show("晨会列表", s, d)
if isinstance(rd, dict) and rd.get("List"):
    mid = rd["List"][0].get("MEETING_ID")
    print(f"  -> 取到 MEETING_ID = {mid}")
    s2, d2 = get("/Examine/GetMEETINGDetail", {"MEETINGId": mid})
    show("晨会明细", s2, d2)
    # WeChat
    s3, d3 = get("/Examine/WeChat_GetMeetingList", {"ExamineId": mid})
    show("微信晨会列表", s3, d3)

# ===== 3. Examine - 巡检 =====
print("\n【巡检 Patrol】")
s, d = post("/Examine/GetPATROLList", {"PageIndex": 1, "PageSize": 3})
rd = show("巡检列表", s, d)
if isinstance(rd, dict) and rd.get("List"):
    pid = rd["List"][0].get("PATROL_ID")
    print(f"  -> 取到 PATROL_ID = {pid}")
    s2, d2 = get("/Examine/GetPATROLDetail", {"PATROLId": pid})
    show("巡检明细", s2, d2)
    # WeChat
    s3, d3 = get("/Examine/WeChat_GetPatrolList", {"ExamineId": pid})
    show("微信巡检列表", s3, d3)

# ===== 4. Analysis =====
print("\n【分析 Analysis】")
s, d = post("/Analysis/GetANALYSISINSList", {"PageIndex": 1, "PageSize": 3})
rd = show("分析列表", s, d)
if isinstance(rd, dict) and rd.get("List"):
    aid = rd["List"][0].get("ANALYSISINS_ID")
    print(f"  -> 取到 ANALYSISINS_ID = {aid}")
    s2, d2 = get("/Analysis/GetANALYSISINSDetail", {"ANALYSISINSId": aid})
    show("分析明细", s2, d2)

# ===== 5. Budget =====
print("\n【预算 Budget】")
s, d = post("/Budget/GetBUDGETPROJECT_AHList", {"PageIndex": 1, "PageSize": 3})
rd = show("预算列表", s, d)
if isinstance(rd, dict) and rd.get("List"):
    bid = rd["List"][0].get("BUDGETPROJECT_AH_ID")
    print(f"  -> 取到 BUDGETPROJECT_AH_ID = {bid}")
    s2, d2 = get("/Budget/GetBUDGETPROJECT_AHDetail", {"BUDGETPROJECT_AHId": bid})
    show("预算明细", s2, d2)
    # 预算明细数据
    s3, d3 = post("/Budget/GetBudgetProjectDetailList", {"PageIndex": 1, "PageSize": 3})
    show("预算明细数据列表", s3, d3)

# ===== 6. BaseInfo 门店数量 =====
print("\n【门店数量 ShopCount】")
s, d = post("/BaseInfo/GetShopCountList", {"PageIndex": 1, "PageSize": 3})
rd = show("门店数量(POST)", s, d)

# ===== 7. Revenue 预算费用 =====
print("\n【Revenue 预算费用】")
s, d = post("/Revenue/GetBudgetExpenseList", {"PageIndex": 1, "PageSize": 3})
show("预算费用(POST)", s, d)

# ===== 8. Revenue 最后同步时间 =====
print("\n【Revenue 最后同步】")
s, d = get("/Revenue/GetLastSyncDateTime", {"ProvinceCode": "340000", "Serverpart_ID": "416"})
show("最后同步时间", s, d)

# ===== 9. Analysis 翻译 =====
print("\n【Analysis 翻译】")
s, d = get("/Analysis/TranslateSentence", {"Sentence": "test", "DialogCode": "", "ProvinceCode": "340000"})
show("翻译", s, d)

print("\n" + "=" * 90)
