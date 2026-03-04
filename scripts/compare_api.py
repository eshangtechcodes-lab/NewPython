# -*- coding: utf-8 -*-
"""调用原 C# API 和新 Python API，结果保存到文件对比"""
import json
import requests

OLD_API = "http://localhost:8900/EShangApiMain/BaseInfo/GetBrandList"
NEW_API = "http://localhost:8080/EShangApiMain/BaseInfo/GetBrandList"

output = []

def log(msg):
    print(msg)
    output.append(msg)

log("=" * 70)
log("  原 C# API vs 新 Python API 真实对比")
log("=" * 70)

# ===== 调用原 C# API =====
log("\n[1] 调用原 C# API:")
try:
    old_resp = requests.post(OLD_API, json={}, headers={"Content-Type": "application/json"}, timeout=10)
    old_data = old_resp.json()
    old_rd = old_data.get("Result_Data", {})
    old_list = old_rd.get("List", [])
    log(f"  Result_Code: {old_data.get('Result_Code')}")
    log(f"  Result_Desc: {old_data.get('Result_Desc')}")
    log(f"  PageIndex:   {old_rd.get('PageIndex')}")
    log(f"  PageSize:    {old_rd.get('PageSize')}")
    log(f"  TotalCount:  {old_rd.get('TotalCount')}")
    log(f"  List条数:    {len(old_list)}")
    if old_list:
        log(f"  字段列表:    {list(old_list[0].keys())}")
        log(f"  第一条: {json.dumps(old_list[0], ensure_ascii=False)}")
except Exception as ex:
    old_data = None
    old_list = []
    log(f"  调用失败: {ex}")

# ===== 调用新 Python API =====
log("\n[2] 调用新 Python API:")
try:
    new_resp = requests.post(NEW_API, json={}, headers={"Content-Type": "application/json"}, timeout=10)
    new_data = new_resp.json()
    new_rd = new_data.get("Result_Data", {})
    new_list = new_rd.get("List", [])
    log(f"  Result_Code: {new_data.get('Result_Code')}")
    log(f"  Result_Desc: {new_data.get('Result_Desc')}")
    log(f"  PageIndex:   {new_rd.get('PageIndex')}")
    log(f"  PageSize:    {new_rd.get('PageSize')}")
    log(f"  TotalCount:  {new_rd.get('TotalCount')}")
    log(f"  List条数:    {len(new_list)}")
    if new_list:
        log(f"  字段列表:    {list(new_list[0].keys())}")
        log(f"  第一条: {json.dumps(new_list[0], ensure_ascii=False)}")
except Exception as ex:
    new_data = None
    new_list = []
    log(f"  调用失败: {ex}")

# ===== 对比 =====
if old_data and new_data:
    log(f"\n{'=' * 70}")
    log("  差异分析")
    log(f"{'=' * 70}")
    old_rd = old_data.get("Result_Data", {})
    new_rd = new_data.get("Result_Data", {})
    for name, o, n in [
        ("Result_Code", old_data.get("Result_Code"), new_data.get("Result_Code")),
        ("Result_Desc", old_data.get("Result_Desc"), new_data.get("Result_Desc")),
        ("PageIndex", old_rd.get("PageIndex"), new_rd.get("PageIndex")),
        ("PageSize", old_rd.get("PageSize"), new_rd.get("PageSize")),
        ("TotalCount", old_rd.get("TotalCount"), new_rd.get("TotalCount")),
        ("List条数", len(old_list), len(new_list)),
    ]:
        match = "✅" if str(o) == str(n) else "❌"
        log(f" {match} {name:15s} 原:{o}  新:{n}")

    # 字段差异
    if old_list and new_list:
        old_keys = set(old_list[0].keys())
        new_keys = set(new_list[0].keys())
        missing = old_keys - new_keys
        extra = new_keys - old_keys
        if missing:
            log(f" ❌ 新API缺少字段: {missing}")
        if extra:
            log(f" ⚠️ 新API多出字段: {extra}")
        if not missing and not extra:
            log(f" ✅ 字段列表完全一致")

# 保存结果
with open("scripts/compare_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
log("\n结果已保存到 scripts/compare_result.txt")
