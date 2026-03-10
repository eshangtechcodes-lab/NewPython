# -*- coding: utf-8 -*-
"""CT-05 + BM-03 缺失路由验证"""
import requests
BASE = "http://localhost:8080/EShangApiMain"
tests = [
    ("GET",  "/Contract/GetContractYearList", None),
    ("GET",  "/Contract/GetShopBusinessTypeRatio", None),
    ("GET",  "/Merchants/GetCoopMerchantsDDL", None),
]
print("=== CT-05 + BM-03 (3 routes) ===")
ok = 0
for m, p, b in tests:
    url = BASE + p
    try:
        r = requests.get(url, timeout=10)
        d = r.json()
        code = d.get("Result_Code", "?")
        desc = str(d.get("Result_Desc", ""))[:60]
        if r.status_code == 200:
            ok += 1
        tag = p.split("?")[0]
        print(f"  [{'OK' if r.status_code==200 else 'FAIL'}] {m:4s} {tag:45s} HTTP={r.status_code} Code={code} {desc}")
    except Exception as e:
        tag = p.split("?")[0]
        print(f"  [FAIL] {m:4s} {tag:45s} {e}")
print(f"\n=== {ok}/3 passed ===")
