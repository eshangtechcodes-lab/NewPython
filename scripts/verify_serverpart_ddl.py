# -*- coding: utf-8 -*-
"""SOP 步骤 5 - GetServerpartDDL 对比验证脚本"""
import requests
import json

API_OLD = "http://192.168.1.99:8900/EShangApiMain"
API_NEW = "http://localhost:8080/EShangApiMain"

params = {"ServerpartType": "1000"}

print("=" * 60)
print("  SOP 步骤 5: GetServerpartDDL 对比验证")
print("=" * 60)

# 步骤 5.2: 调原 API
print("\n[1] 调用原 C# API...")
try:
    r1 = requests.get(f"{API_OLD}/BaseInfo/GetServerpartDDL", params=params, timeout=60)
    d1 = r1.json()
    print(f"  Result_Code: {d1.get('Result_Code')}")
    rd1 = d1.get("Result_Data", {})
    list1 = rd1.get("List", []) if isinstance(rd1, dict) else []
    print(f"  TotalCount: {rd1.get('TotalCount')}")
    print(f"  List 条数: {len(list1)}")
except Exception as e:
    print(f"  调用失败: {e}")
    d1 = None
    list1 = []

# 步骤 5.3: 调新 API
print("\n[2] 调用新 Python API...")
try:
    r2 = requests.get(f"{API_NEW}/BaseInfo/GetServerpartDDL", params=params, timeout=15)
    d2 = r2.json()
    print(f"  Result_Code: {d2.get('Result_Code')}")
    rd2 = d2.get("Result_Data", {})
    list2 = rd2.get("List", []) if isinstance(rd2, dict) else []
    print(f"  TotalCount: {rd2.get('TotalCount')}")
    print(f"  List 条数: {len(list2)}")
except Exception as e:
    print(f"  调用失败: {e}")
    d2 = None
    list2 = []

if not d1 or not d2:
    print("\n❌ 无法完成对比（至少一个 API 调用失败）")
    exit(1)

# SOP 步骤 5.5: 对比清单
print("\n" + "=" * 60)
print("  SOP 步骤 5.5 对比清单")
print("=" * 60)

checks = []

# 1. Result_Code
code_ok = d1["Result_Code"] == d2["Result_Code"]
checks.append(("Result_Code", code_ok, f"{d1['Result_Code']} vs {d2['Result_Code']}"))

# 2. TotalCount
tc1 = rd1.get("TotalCount", 0)
tc2 = rd2.get("TotalCount", 0)
tc_ok = tc1 == tc2
checks.append(("TotalCount", tc_ok, f"{tc1} vs {tc2}"))

# 3. List 条数
lc_ok = len(list1) == len(list2)
checks.append(("List 条数", lc_ok, f"{len(list1)} vs {len(list2)}"))

# 4. 字段列表
if list1 and list2:
    keys1 = set(list1[0].keys())
    keys2 = set(list2[0].keys())
    fields_ok = keys1 == keys2
    missing = keys1 - keys2
    extra = keys2 - keys1
    detail = f"字段: {keys1}"
    if missing:
        detail += f" | 缺失: {missing}"
    if extra:
        detail += f" | 多余: {extra}"
    checks.append(("字段列表", fields_ok, detail))
else:
    checks.append(("字段列表", False, "无数据可比"))

# 5. 字段值类型
if list1 and list2:
    type_issues = []
    for key in list1[0]:
        v1 = list1[0].get(key)
        v2 = list2[0].get(key)
        if type(v1) != type(v2) and v1 is not None and v2 is not None:
            type_issues.append(f"{key}: {type(v1).__name__} vs {type(v2).__name__}")
    types_ok = len(type_issues) == 0
    checks.append(("字段值类型", types_ok, ", ".join(type_issues) if type_issues else "一致"))

# 6. 排序（前5条）
if list1 and list2:
    first5_1 = [(d["label"], d["value"]) for d in list1[:5]]
    first5_2 = [(d["label"], d["value"]) for d in list2[:5]]
    sort_ok = first5_1 == first5_2
    checks.append(("排序(前5条)", sort_ok, f"原:{first5_1}\n新:{first5_2}"))

# 7. 数据内容完整性
if list1 and list2 and len(list1) == len(list2):
    set1 = set((d["label"], d["value"]) for d in list1)
    set2 = set((d["label"], d["value"]) for d in list2)
    content_ok = set1 == set2
    diff = set1.symmetric_difference(set2)
    checks.append(("数据内容", content_ok, f"差异: {len(diff)}条" if diff else "完全一致"))

# 输出结果
all_pass = True
for name, ok, detail in checks:
    status = "✅" if ok else "❌"
    if not ok:
        all_pass = False
    print(f"  {status} {name}: {detail}")

print(f"\n{'=' * 60}")
print(f"  总结: {'全部通过 ✅' if all_pass else '有差异 ❌ — 需回步骤4修复'}")
print(f"{'=' * 60}")
