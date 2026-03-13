'''
Author: smoking shuffleman@live.com
Date: 2026-03-05 15:08:32
LastEditors: smoking shuffleman@live.com
LastEditTime: 2026-03-05 16:31:02
FilePath: \Python\eshang_api\scripts\check_422.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# -*- coding: utf-8 -*-
"""清晰版 422 检测"""
import requests, os, json

os.environ['NO_PROXY'] = '*'
BASE = "http://127.0.0.1:8080/CommercialApi"

test_cases = [
    ("GET", "/Revenue/GetSummaryRevenue", {"pushProvinceCode": "340000"}),
    ("GET", "/Revenue/GetRevenueBudget", {"Statistics_Date": "2026-01-01", "Province_Code": "340000"}),
    ("GET", "/Revenue/GetMobileShare", {"Province_Code": "340000", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetDeliveryList", {"pushProvinceCode": "340000", "Serverpart_ID": "416", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetDeliveryServerpartList", {"pushProvinceCode": "340000", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetShopRevenue", {"pushProvinceCode": "340000", "Serverpart_ID": "416", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetTransactionAnalysis", {"Province_Code": "340000", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetCurRevenue", {"Province_Code": "340000", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetShopCurRevenue", {"Serverpart_ID": "416", "Statistics_Date": "2026-01-01"}),
    ("GET", "/Revenue/GetTransactionDetailList", {"Serverpart_ID": "416"}),
]

for method, path, params in test_cases:
    try:
        r = requests.get(BASE + path, params=params, timeout=10)
        if r.status_code == 422:
            detail = r.json().get("detail", [])
            missing = [d['loc'][-1] for d in detail if d.get('type') == 'missing']
            print(f"422 {path}")
            print(f"    缺少参数: {missing}")
        elif r.status_code == 200:
            code = r.json().get("Result_Code", "?")
            print(f"OK  {path}  C={code}")
        else:
            print(f"{r.status_code} {path}")
    except Exception as e:
        print(f"ERR {path}: {e}")
