# -*- coding: utf-8 -*-
"""MP-03 验证"""
import requests
BASE = "http://localhost:8080/EShangApiMain"
print("=== MP-03 CorrectSellMasterState ===")
# 用空列表测试（不修改数据，验证路由可达）
r = requests.post(BASE + "/MobilePay/CorrectSellMasterState",
    json=[],
    headers={"Content-Type": "application/json"})
print(f"  HTTP={r.status_code} Body={r.text[:200]}")
d = r.json()
code = d.get("Result_Code", "?")
print(f"  Result_Code={code}")
if r.status_code == 200 and code == 100:
    print("  [OK] MP-03 passed")
else:
    print("  [FAIL] MP-03 failed")
