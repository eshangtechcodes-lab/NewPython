# -*- coding: utf-8 -*-
"""调 CommercialApi ContractController 原 API 获取基准"""
import json, requests, os
session = requests.Session()
session.trust_env = False
BASE = "http://localhost:8900/CommercialApi"
os.makedirs("scripts/baseline", exist_ok=True)

apis = [
    ("GET", "/Contract/GetContractAnalysis?statisticsDate=2025-01-01&provinceCode=340000", "GetContractAnalysis"),
    ("GET", "/Contract/GetMerchantAccountSplit?StatisticsMonth=2025-01&CompactTypes=340001", "GetMerchantAccountSplit"),
    ("GET", "/Contract/GetMerchantAccountDetail?MerchantId=1&StatisticsMonth=2025-01&CompactTypes=340001", "GetMerchantAccountDetail"),
]

for method, path, name in apis:
    url = BASE + path
    print(f"\n[{method}] {path}")
    try:
        resp = session.get(url, timeout=30)
        data = resp.json()
        code = data.get("Result_Code", "?")
        print(f"  Result_Code={code}, Result_Desc={data.get('Result_Desc','')}")
        rd = data.get("Result_Data")
        if isinstance(rd, dict):
            print(f"  Result_Data keys: {list(rd.keys())[:10]}")
        fp = f"scripts/baseline/{name}.json"
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  -> {fp}")
    except Exception as ex:
        print(f"  ERR: {ex}")
