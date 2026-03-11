# -*- coding: utf-8 -*-
"""查看 Budget 模块的所有 case 详情"""
import json

with open("docs/session4_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for case in data["cases"]:
    if not case["endpoint"].startswith("Budget/"):
        continue
    print("=" * 80)
    print("接口: {} / {}".format(case["endpoint"], case["case_name"]))
    print("方法: {}".format(case["method"]))
    print("状态: {}".format(case["status"]))
    print("C# HTTP: {}  Python HTTP: {}".format(case.get("old_status_code"), case.get("new_status_code")))
    if case.get("query"):
        print("Query: {}".format(case["query"]))
    if case.get("json_body"):
        print("Body: {}".format(json.dumps(case["json_body"], ensure_ascii=False)))
    print("差异:")
    for d in case.get("diffs", []):
        # 截断过长差异
        if len(d) > 200:
            d = d[:200] + "..."
        print("  - {}".format(d))
    print()
