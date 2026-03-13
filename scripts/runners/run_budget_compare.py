# -*- coding: utf-8 -*-
"""从全量 manifest 中提取 Budget 模块，生成临时 manifest，然后调用 compare_api.py"""
import json, sys, os

# 读取全量 manifest
with open("scripts/manifests/endpoint_case_library.json", "r", encoding="utf-8") as f:
    full = json.load(f)

# 提取 Budget 相关 endpoints
budget_eps = {k: v for k, v in full["endpoints"].items() if k.startswith("Budget/")}

# 构造临时 manifest
mini = {
    "version": full.get("version", "1.0"),
    "default_headers": full.get("default_headers", {}),
    "default_timeout": full.get("default_timeout", 15),
    "endpoints": budget_eps
}

tmp_path = "scripts/manifests/_tmp_budget.json"
with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(mini, f, ensure_ascii=False, indent=2)

print("Budget manifest: {} endpoints".format(len(budget_eps)))
print("Running compare_api.py ...")
os.system('python scripts/compare_api.py --manifest {} --report docs/session4_budget.md'.format(tmp_path))
