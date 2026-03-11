# -*- coding: utf-8 -*-
"""快速诊断所有DIFF接口的具体错误"""
import requests, json
s = requests.Session()
s.trust_env = False
BASE = "http://127.0.0.1:8080/CommercialApi"
H = {"ProvinceCode": "340000"}
with open("scripts/test_results/baseline_cache.json", "r", encoding="utf-8") as f:
    cache = json.load(f)
with open("scripts/test_results/compare_revenue_bigdata.json", "r", encoding="utf-8") as f:
    result = json.load(f)
for d in result["diffs"]:
    method = d["method"]
    route = d["route"]
    key = method + ":" + route
    entry = cache["results"].get(key, {})
    params = entry.get("params", {})
    url = BASE + route
    try:
        if method == "GET":
            r = s.get(url, params=params, headers=H, timeout=15)
        else:
            r = s.post(url, json=params, headers=H, timeout=15)
        desc = r.json().get("Result_Desc", "")[:180]
    except Exception as e:
        desc = str(e)[:180]
    print(key + ": " + desc)
