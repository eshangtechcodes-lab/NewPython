# -*- coding: utf-8 -*-
"""
批量调用 CommercialApi BaseInfoController 所有接口，获取基准数据
"""
import json
import requests
import os

# 禁用代理，避免 localhost 请求走系统代理超时
session = requests.Session()
session.trust_env = False

BASE = "http://localhost:8900/CommercialApi"
os.makedirs("scripts/baseline", exist_ok=True)

apis = [
    # (方法, 路径, 文件名)
    ("GET", "/BaseInfo/GetSPRegionList?Province_Code=340000", "GetSPRegionList"),
    ("GET", "/BaseInfo/GetBusinessTradeList?pushProvinceCode=340000", "GetBusinessTradeList_GET"),
    ("POST", "/BaseInfo/GetBusinessTradeList", "GetBusinessTradeList_POST"),
    ("GET", "/BaseInfo/GetShopCountList?pushProvinceCode=340000&Statistics_Date=2025-01-01", "GetShopCountList_GET"),
    ("GET", "/BaseInfo/GetServerpartList?Province_Code=340000", "GetServerpartList"),
    ("GET", "/BaseInfo/GetServerpartInfo?ServerpartId=440", "GetServerpartInfo"),
    ("GET", "/BaseInfo/GetServerInfoTree?ProvinceCode=340000", "GetServerInfoTree"),
    ("GET", "/BaseInfo/GetBrandAnalysis?ProvinceCode=340000&Serverpart_ID=440", "GetBrandAnalysis"),
]

print("=" * 60)
print("  批量获取 BaseInfoController 原 API 基准数据")
print("=" * 60)

for method, path, name in apis:
    url = BASE + path
    print(f"\n[{method}] {path}")
    try:
        if method == "GET":
            resp = session.get(url, timeout=15)
        else:
            resp = session.post(url, json={}, headers={"Content-Type": "application/json"}, timeout=15)
        
        data = resp.json()
        code = data.get("Result_Code", "?")
        rd = data.get("Result_Data", {})
        
        if isinstance(rd, dict) and "List" in rd:
            lst = rd.get("List", [])
            print(f"  Result_Code={code}, TotalCount={rd.get('TotalCount')}, List={len(lst)}条")
            if lst:
                print(f"  字段: {list(lst[0].keys())}")
        else:
            print(f"  Result_Code={code}")
            
        # 保存基准
        filepath = f"scripts/baseline/{name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ 已保存 → {filepath}")
    except Exception as ex:
        print(f"  ❌ 失败: {ex}")
