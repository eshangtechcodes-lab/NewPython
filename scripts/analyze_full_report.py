# -*- coding: utf-8 -*-
"""分析全量对比 JSON 报告，汇总各模块 PASS/FAIL 分布"""
import json
from collections import defaultdict

with open("docs/session4_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 按模块统计
modules = defaultdict(lambda: {"pass": 0, "fail": 0, "skip": 0, "total": 0, "fail_types": defaultdict(int)})

for case in data["cases"]:
    ep = case["endpoint"]
    module = ep.split("/")[0] if "/" in ep else "Unknown"
    status = case["status"]
    modules[module]["total"] += 1
    modules[module][status] += 1

    if status == "fail":
        diffs = case.get("diffs", [])
        desc_diff = [d for d in diffs if "Result_Desc" in d]
        old_sc = case.get("old_status_code")
        new_sc = case.get("new_status_code")

        if old_sc == 404 or new_sc == 404:
            if old_sc == 404:
                modules[module]["fail_types"]["C#端404"] += 1
            else:
                modules[module]["fail_types"]["Python端404"] += 1
        elif desc_diff:
            desc = desc_diff[0]
            if "fetch_one" in desc or "fetch_scalar" in desc:
                modules[module]["fail_types"]["DB方法缺失"] += 1
            elif "查询成功" in desc and "成功" in desc and len(desc) < 80:
                modules[module]["fail_types"]["Desc措辞差异"] += 1
            elif "查询失败" in desc:
                modules[module]["fail_types"]["Python查询报错"] += 1
            elif "422" in str(new_sc) or "405" in str(new_sc):
                modules[module]["fail_types"]["HTTP方法/参数错误"] += 1
            else:
                modules[module]["fail_types"]["其他Desc差异"] += 1
        elif any("类型不一致" in d for d in diffs):
            modules[module]["fail_types"]["类型差异"] += 1
        elif any("缺少该字段" in d or "多出该字段" in d for d in diffs):
            modules[module]["fail_types"]["字段差异"] += 1
        elif any("值不一致" in d for d in diffs):
            modules[module]["fail_types"]["值差异"] += 1
        else:
            modules[module]["fail_types"]["其他"] += 1

# 打印汇总
print("=" * 100)
header = "{:<25} {:>5} {:>5} {:>5} {:>6}  {}".format("模块", "PASS", "FAIL", "SKIP", "TOTAL", "失败类型")
print(header)
print("=" * 100)
for mod in sorted(modules.keys()):
    m = modules[mod]
    fail_info = ", ".join("{}:{}".format(k, v) for k, v in sorted(m["fail_types"].items(), key=lambda x: -x[1]))
    line = "{:<25} {:>5} {:>5} {:>5} {:>6}  {}".format(mod, m["pass"], m["fail"], m["skip"], m["total"], fail_info)
    print(line)
print("=" * 100)
total_line = "{:<25} {:>5} {:>5} {:>5} {:>6}".format(
    "总计", data["counts"]["pass"], data["counts"]["fail"], data["counts"]["skip"], data["counts"]["total"])
print(total_line)

# 列出 PASS 的接口
print("\n" + "=" * 60)
print("PASS 的接口列表:")
print("=" * 60)
for case in data["cases"]:
    if case["status"] == "pass":
        print("  [PASS] {} / {}".format(case["endpoint"], case["case_name"]))
