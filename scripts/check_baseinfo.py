# -*- coding: utf-8 -*-
import json

with open(r"scripts/test_results/compare_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("BaseInfo 接口测试结果：")
print(f"{'No':>3s}  {'Method':<5s}  {'Route':<55s}  {'Old':<20s}  {'New':<20s}  {'Result':<6s}")
print("-" * 115)
for r in data:
    if r["ctrl"] == "BaseInfo":
        print(f"{r['idx']:>3d}  {r['method']:<5s}  {r['route']:<55s}  {r['old']:<20s}  {r['new']:<20s}  {r['result']:<6s}")
