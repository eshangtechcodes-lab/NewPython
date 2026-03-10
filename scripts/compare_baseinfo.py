# -*- coding: utf-8 -*-
"""批量对比 BaseInfoController 所有已实现接口"""
import json
import sys
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

session = requests.Session()
session.trust_env = False

OLD = "http://192.168.1.99:8900/CommercialApi"
NEW = "http://127.0.0.1:8080/CommercialApi"

output = []
def log(msg):
    print(msg)
    output.append(msg)

apis = [
    ("GET", "/BaseInfo/GetSPRegionList?Province_Code=340000", "GetSPRegionList"),
    ("GET", "/BaseInfo/GetBusinessTradeList?pushProvinceCode=340000", "GetBusinessTradeList_GET"),
]

log("=" * 60)
log("  BaseInfoController 新旧 API 批量对比")
log("=" * 60)

all_pass = True
for method, path, name in apis:
    log(f"\n--- {name} ---")
    try:
        old_resp = session.get(OLD + path, timeout=15).json()
        new_resp = session.get(NEW + path, timeout=15).json()
        
        old_rd = old_resp.get("Result_Data", {})
        new_rd = new_resp.get("Result_Data", {})
        old_list = old_rd.get("List", [])
        new_list = new_rd.get("List", [])
        
        checks = [
            ("Result_Code", old_resp.get("Result_Code"), new_resp.get("Result_Code")),
            ("TotalCount", old_rd.get("TotalCount"), new_rd.get("TotalCount")),
            ("List条数", len(old_list), len(new_list)),
        ]
        
        for k, o, n in checks:
            match = "✅" if str(o) == str(n) else "❌"
            if str(o) != str(n):
                all_pass = False
            log(f" {match} {k:15s} 原:{o}  新:{n}")
        
        # 逐条对比前 3 条
        for i in range(min(3, len(old_list), len(new_list))):
            match = "✅" if old_list[i] == new_list[i] else "❌"
            if old_list[i] != new_list[i]:
                all_pass = False
                log(f" {match} [{i+1}] 原:{json.dumps(old_list[i], ensure_ascii=False)[:80]}")
                log(f"       新:{json.dumps(new_list[i], ensure_ascii=False)[:80]}")
            else:
                log(f" {match} [{i+1}] 数据一致")
    except Exception as ex:
        log(f" ❌ 失败: {ex}")
        all_pass = False

log(f"\n{'=' * 60}")
log(f"  {'✅ 全部通过！' if all_pass else '❌ 存在差异'}")
log(f"{'=' * 60}")

with open("scripts/compare_baseinfo_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))
