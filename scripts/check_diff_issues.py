# -*- coding: utf-8 -*-
"""
分析所有 DIFF 状态的接口——找出需要修复的代码问题
"""
import json

with open("scripts/test_results/compare_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== DIFF 状态接口汇总 ===\n")
print(f"{'No':>3s}  {'Method':<5s}  {'Route':<55s}  {'Old':<20s}  {'New':<20s}")
print("-" * 110)
cnt = 0
for r in data:
    if r["result"] == "DIFF":
        cnt += 1
        old = r.get("old", "?")[:20]
        new = r.get("new", "?")[:20]
        print(f"{r['idx']:>3d}  {r['method']:<5s}  {r['route']:<55s}  {old:<20s}  {new:<20s}")

print(f"\n共 {cnt} 个 DIFF 接口")

# 再看 SKIP 但新API返回422的
print("\n\n=== 新API返回422 (参数不匹配) ===\n")
for r in data:
    if "422" in str(r.get("new", "")):
        print(f"  {r['idx']:>3d} {r['method']:<5s} {r['route']}")
