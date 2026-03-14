# -*- coding: utf-8 -*-
"""快速验证 fetch_one/fetch_scalar 修复效果"""
import requests

H = {"ProvinceCode": "340000"}
base = "http://localhost:8080/EShangApiMain"
tests = [
    ("GET", "/Analysis/GetANALYSISINSDetail?ANALYSISINSId=1805", None),
    ("GET", "/Analysis/GetANALYSISRULEDetail?ANALYSISRULEId=19", None),
    ("POST", "/Analysis/GetANALYSISINSList", {"SearchParameter":{"ANALYSISINS_ID":"1805"},"PageIndex":1,"PageSize":9}),
    ("POST", "/Analysis/GetVEHICLEAMOUNTList", {"SearchParameter":{},"PageIndex":1,"PageSize":9}),
    ("GET", "/Budget/GetbudgetProjectDetail?BudgetProjectId=128", None),
    ("POST", "/Budget/GetBudgetDetailList", {"SearchParameter":{"BUDGETDETAIL_AH_ID":"132"},"PageIndex":1,"PageSize":9}),
    ("GET", "/BusinessMan/GetCOMMODITY_TEMPDetail?COMMODITY_TEMPId=43", None),
    ("GET", "/Merchants/GetCUSTOMTYPEDetail?CUSTOMTYPEId=49", None),
    ("POST", "/Merchants/GetCUSTOMTYPEList", {"SearchParameter":{"CUSTOMTYPE_ID":"49"},"PageIndex":1,"PageSize":9}),
    ("GET", "/Merchants/GetBusinessManDetail?BusinessManId=123", None),
    ("POST", "/Merchants/GetCommodityList", {"SearchParameter":{},"PageIndex":1,"PageSize":9}),
    ("GET", "/Audit/GetAbnormalAuditDetail?AbnormalAuditId=1", None),
    ("POST", "/Audit/GetAUDITTASKSList", {"SearchParameter":{"AUDITTASKS_ID":"3675"},"PageIndex":1,"PageSize":9}),
]

passed = 0
failed = 0
for t in tests:
    m, path_q, body = t
    url = base + path_q
    name = path_q.split("?")[0]
    try:
        if m == "GET":
            r = requests.get(url, headers=H, timeout=10)
        else:
            r = requests.post(url, json=body, headers=H, timeout=10)
        d = r.json()
        code = d.get("Result_Code", "?")
        desc = str(d.get("Result_Desc", ""))[:60]
        status = "PASS" if code == 100 else "FAIL"
        if code == 100:
            passed += 1
        else:
            failed += 1
        print("[{}] {:<50s} Code={} Desc={}".format(status, name, code, desc))
    except Exception as e:
        failed += 1
        print("[ERR]  {:<50s} {}".format(name, e))

print("\n总计: PASS {} / FAIL {} / TOTAL {}".format(passed, failed, len(tests)))
