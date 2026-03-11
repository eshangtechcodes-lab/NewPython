# -*- coding: utf-8 -*-
"""对比 CommercialApi GetSPRegionList 新旧接口"""
import json
import requests

OLD = "http://localhost:8900/CommercialApi/BaseInfo/GetSPRegionList?Province_Code=340000"
NEW = "http://localhost:8080/CommercialApi/BaseInfo/GetSPRegionList?Province_Code=340000"

output = []
def log(msg):
    print(msg)
    output.append(msg)

log("=" * 60)
log("  GetSPRegionList 新旧 API 对比")
log("=" * 60)

try:
    old_data = requests.get(OLD, timeout=15).json()
    log(f"\n[原API] Result_Code={old_data.get('Result_Code')}")
except Exception as ex:
    log(f"\n[原API] 调用失败: {ex}")
    old_data = None

try:
    new_data = requests.get(NEW, timeout=15).json()
    log(f"[新API] Result_Code={new_data.get('Result_Code')}")
except Exception as ex:
    log(f"[新API] 调用失败: {ex}")
    new_data = None

if old_data and new_data:
    old_rd = old_data.get("Result_Data", {})
    new_rd = new_data.get("Result_Data", {})
    old_list = old_rd.get("List", [])
    new_list = new_rd.get("List", [])

    log(f"\n--- 结构对比 ---")
    for name, o, n in [
        ("Result_Code", old_data.get("Result_Code"), new_data.get("Result_Code")),
        ("Result_Desc", old_data.get("Result_Desc"), new_data.get("Result_Desc")),
        ("TotalCount", old_rd.get("TotalCount"), new_rd.get("TotalCount")),
        ("PageIndex", old_rd.get("PageIndex"), new_rd.get("PageIndex")),
        ("PageSize", old_rd.get("PageSize"), new_rd.get("PageSize")),
        ("List条数", len(old_list), len(new_list)),
    ]:
        match = "✅" if str(o) == str(n) else "❌"
        log(f" {match} {name:15s} 原:{o}  新:{n}")

    log(f"\n--- 数据逐条对比 ---")
    for i in range(max(len(old_list), len(new_list))):
        old_item = old_list[i] if i < len(old_list) else None
        new_item = new_list[i] if i < len(new_list) else None
        match = "✅" if old_item == new_item else "❌"
        log(f" {match} [{i+1}] 原:{json.dumps(old_item, ensure_ascii=False):40s} 新:{json.dumps(new_item, ensure_ascii=False)}")

with open("scripts/compare_spregion_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
log("\n结果已保存")
