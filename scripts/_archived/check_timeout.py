# -*- coding: utf-8 -*-
import json

with open("scripts/test_results/compare_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("旧API超时(TIMEOUT)的接口：")
print(f"{'No':>3s}  {'Method':<5s}  {'Route':<55s}  {'NewAPI':<20s}")
print("-" * 90)
cnt = 0
for r in data:
    if r["old"] == "TIMEOUT":
        cnt += 1
        print(f"{r['idx']:>3d}  {r['method']:<5s}  {r['route']:<55s}  {r['new']:<20s}")

print(f"\n共 {cnt} 个接口旧API超时")
