# -*- coding: utf-8 -*-
import requests, os
os.environ["NO_PROXY"] = "*"
for k in ["HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy"]:
    os.environ.pop(k, None)

NEW = "http://127.0.0.1:8080/CommercialApi"

print("=== 修复验证 ===")

# 1. GetBudgetExpenseList POST (之前返回 T=0，现在应查到158条)
print("\n--- GetBudgetExpenseList POST ---")
r = requests.post(NEW + "/Revenue/GetBudgetExpenseList", json={"PageIndex":1,"PageSize":5}, timeout=10)
d = r.json()
rd = d["Result_Data"]
total = rd.get("TotalCount")
items = rd.get("List", [])
print(f"  Code={d['Result_Code']}, TotalCount={total}, 本页={len(items)}")
if items:
    print(f"  首条keys: {list(items[0].keys())[:6]}")

# 2. GetBudgetMainShow (之前T_BUDGETPROJECTDETAIL_AH不存在)
print("\n--- GetBudgetMainShow ---")
r = requests.get(NEW + "/Budget/GetBudgetMainShow", params={"BUDGETPROJECT_AHId": 302}, timeout=10)
d = r.json()
detail_list = d.get("Result_Data", {}).get("DetailList", [])
print(f"  Code={d['Result_Code']}, DetailList={len(detail_list)}条")

# 3. GetBudgetProjectDetailList POST (之前 TODO)
print("\n--- GetBudgetProjectDetailList POST ---")
r = requests.post(NEW + "/Budget/GetBudgetProjectDetailList", json={"PageIndex":1,"PageSize":5}, timeout=10)
d = r.json()
print(f"  Code={d['Result_Code']}, TotalCount={d.get('Result_Data',{}).get('TotalCount','?')}")
