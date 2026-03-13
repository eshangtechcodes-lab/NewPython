# -*- coding: utf-8 -*-
"""从全量 manifest 中提取 BusinessMan 模块，生成临时 manifest，然后调用 compare_api.py"""
import json, os

MODULE_PREFIX = "BusinessMan/"

with open("scripts/manifests/endpoint_case_library.json", "r", encoding="utf-8") as f:
    full = json.load(f)

module_eps = {k: v for k, v in full["endpoints"].items() if k.startswith(MODULE_PREFIX)}

mini = {
    "version": full.get("version", "1.0"),
    "default_headers": full.get("default_headers", {}),
    "default_timeout": full.get("default_timeout", 15),
    "ignore_paths": ["USER_ID_Encrypted"],
    "endpoints": module_eps
}

tmp_path = "scripts/manifests/_tmp_businessman.json"
report_path = "docs/session4_businessman.md"

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(mini, f, ensure_ascii=False, indent=2)

print(f"BusinessMan manifest: {len(module_eps)} endpoints")
print("Running compare_api.py ...")
os.system(f'python scripts/compare_api.py --manifest {tmp_path} --report {report_path}')
