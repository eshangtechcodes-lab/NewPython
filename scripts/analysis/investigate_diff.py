# -*- coding: utf-8 -*-
"""
调查不一致接口的原 API 返回格式
"""
import requests, json

session = requests.Session()
session.trust_env = False
OLD_BASE = "http://localhost:8900/CommercialApi"
TIMEOUT = 30

tests = [
    ("GET", "/Customer/GetCustomerRatio", {"serverpartId": 416, "statisticsMonth": "202501"}),
    ("GET", "/Customer/GetCustomerConsumeRatio", {"serverpartId": 416, "statisticsMonth": "202501"}),
    ("GET", "/Customer/GetCustomerAgeRatio", {"serverpartId": 416, "statisticsMonth": "202501"}),
    ("GET", "/BigData/GetBayonetWarning", {"StatisticsDate": "2025-01-01"}),
    ("GET", "/BaseInfo/GetServerInfoTree", {"Province_Code": "340000"}),
    ("GET", "/Budget/GetBUDGETPROJECT_AHDetail", {"BUDGETPROJECT_AHId": 1}),
    ("GET", "/Budget/GetBudgetMainShow", {"BUDGETPROJECT_AHId": 1}),
    ("GET", "/Examine/GetEXAMINEDetail", {"EXAMINEId": 1}),
    ("GET", "/Examine/GetMEETINGDetail", {"MEETINGId": 1}),
    ("GET", "/Examine/GetPATROLDetail", {"PATROLId": 1}),
    ("GET", "/Analysis/GetANALYSISINSDetail", {"ANALYSISINSId": 1}),
]

for method, path, params in tests:
    url = OLD_BASE + path
    print(f"\n{'='*60}")
    print(f"[{method}] {path}")
    print(f"Params: {params}")
    try:
        r = session.get(url, params=params, timeout=TIMEOUT)
        print(f"Status: {r.status_code}")
        # 尝试解析为 JSON
        try:
            data = r.json()
            # 只打印前500字符
            txt = json.dumps(data, ensure_ascii=False, indent=2)
            if len(txt) > 1000:
                print(txt[:1000] + "\n... (截断)")
            else:
                print(txt)
        except:
            txt = r.text[:500]
            print(f"非JSON: {txt}")
    except Exception as ex:
        print(f"异常: {ex}")
