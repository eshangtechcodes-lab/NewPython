# -*- coding: utf-8 -*-
"""快速验证 Finance 模块 FAIL 接口"""
import json, os

with open("scripts/manifests/endpoint_case_library.json", "r", encoding="utf-8") as f:
    full = json.load(f)

module_eps = {k: v for k, v in full["endpoints"].items()
              if k.startswith("Finance/GetAccountCompare") or k.startswith("Finance/GetAHJKtoken")}

mini = {
    "version": full.get("version", "1.0"),
    "default_headers": full.get("default_headers", {}),
    "default_timeout": full.get("default_timeout", 15),
    "ignore_paths": [],
    "endpoints": module_eps
}

tmp_path = "scripts/manifests/_tmp_finance.json"
report_path = "docs/session4_finance.md"

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(mini, f, ensure_ascii=False, indent=2)

print(f"Finance manifest: {len(module_eps)} endpoints")
print("Running compare_api.py ...")
os.system(f'python scripts/compare_api.py --manifest {tmp_path} --report {report_path}')
