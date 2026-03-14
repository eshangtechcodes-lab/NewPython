# -*- coding: utf-8 -*-
"""用实际 C# 对比接口验证 Budget 模块的 4 个 CRUD 接口"""
import requests, json

H = {"ProvinceCode": "340000"}
OLD = "http://192.168.1.99:8900/EShangApiMain"
NEW = "http://localhost:8080/EShangApiMain"

cases = [
    {
        "name": "GetBudgetProjectList",
        "method": "POST",
        "path": "/Budget/GetBudgetProjectList",
        "body": {"SearchParameter": {"SERVERPART_IDS": "416"}, "PageIndex": 1, "PageSize": 9},
    },
    {
        "name": "GetbudgetProjectDetail",
        "method": "GET",
        "path": "/Budget/GetbudgetProjectDetail?BUDGETPROJECT_AHId=128",
        "body": None,
    },
    {
        "name": "GetBudgetDetailList",
        "method": "POST",
        "path": "/Budget/GetBudgetDetailList",
        "body": {"SearchParameter": {"BUDGETDETAIL_AH_ID": "132"}, "PageIndex": 1, "PageSize": 9},
    },
    {
        "name": "GetBudgetDetailDetail",
        "method": "GET",
        "path": "/Budget/GetBudgetDetailDetail?BUDGETDETAIL_AHId=132",
        "body": None,
    },
]

for case in cases:
    print("=" * 70)
    print("接口: {}".format(case["name"]))
    try:
        if case["method"] == "GET":
            old_r = requests.get(OLD + case["path"], headers=H, timeout=15)
            new_r = requests.get(NEW + case["path"], headers=H, timeout=15)
        else:
            old_r = requests.post(OLD + case["path"], json=case["body"], headers=H, timeout=15)
            new_r = requests.post(NEW + case["path"], json=case["body"], headers=H, timeout=15)

        old_d = old_r.json()
        new_d = new_r.json()

        old_code = old_d.get("Result_Code")
        new_code = new_d.get("Result_Code")
        old_desc = old_d.get("Result_Desc", "")
        new_desc = new_d.get("Result_Desc", "")

        print("  C# Code={} Desc={}".format(old_code, old_desc))
        print("  Py Code={} Desc={}".format(new_code, new_desc))

        # 比对 Result_Data
        old_data = old_d.get("Result_Data")
        new_data = new_d.get("Result_Data")

        if old_code != new_code:
            print("  [FAIL] Result_Code 不一致!")
            continue

        # Result_Desc 对比
        if old_desc != new_desc:
            print("  [WARN] Result_Desc: C#='{}' vs Py='{}'".format(old_desc, new_desc))

        if old_data is None and new_data is None:
            print("  [PASS] 两端都无数据")
            continue

        if type(old_data) != type(new_data):
            print("  [FAIL] Result_Data 类型不同: {} vs {}".format(type(old_data).__name__, type(new_data).__name__))
            continue

        # 对比字段
        if isinstance(old_data, dict):
            # 可能是 Detail（直接是 dict）或 List（有 PageIndex/List）
            if "List" in old_data:
                # List 对比
                old_list = old_data.get("List", [])
                new_list = new_data.get("List", [])
                if len(old_list) != len(new_list):
                    print("  [FAIL] List 长度不同: {} vs {}".format(len(old_list), len(new_list)))
                else:
                    diffs = []
                    for i, (o, n) in enumerate(zip(old_list, new_list)):
                        for k in set(list(o.keys()) + list(n.keys())):
                            ov = o.get(k)
                            nv = n.get(k)
                            if str(ov) != str(nv):
                                diffs.append("  row[{}].{}: C#={} vs Py={}".format(i, k, repr(ov), repr(nv)))
                    if diffs:
                        print("  [FAIL] {} 处字段差异:".format(len(diffs)))
                        for d in diffs[:10]:
                            print(d)
                        if len(diffs) > 10:
                            print("  ... 还有 {} 处".format(len(diffs) - 10))
                    else:
                        print("  [PASS] List 数据完全一致!")

                # OtherData 对比
                old_other = old_data.get("OtherData")
                new_other = new_data.get("OtherData")
                if old_other and new_other:
                    other_diffs = []
                    for k in set(list(old_other.keys()) + list(new_other.keys())):
                        ov = old_other.get(k)
                        nv = new_other.get(k)
                        if str(ov) != str(nv):
                            other_diffs.append("  OtherData.{}: C#={} vs Py={}".format(k, repr(ov), repr(nv)))
                    if other_diffs:
                        print("  [WARN] OtherData 差异:")
                        for d in other_diffs[:10]:
                            print(d)
                    else:
                        print("  [PASS] OtherData 一致!")
                elif old_other and not new_other:
                    print("  [FAIL] Python 缺少 OtherData")
                elif not old_other and new_other:
                    print("  [WARN] Python 多出 OtherData")
            else:
                # Detail 对比
                diffs = []
                for k in set(list(old_data.keys()) + list(new_data.keys())):
                    ov = old_data.get(k)
                    nv = new_data.get(k)
                    if str(ov) != str(nv):
                        diffs.append("  {}: C#={} vs Py={}".format(k, repr(ov), repr(nv)))
                if diffs:
                    print("  [FAIL] {} 处字段差异:".format(len(diffs)))
                    for d in diffs[:15]:
                        print(d)
                else:
                    print("  [PASS] Detail 数据完全一致!")
        else:
            print("  [INFO] Result_Data 类型: {}".format(type(old_data).__name__))

    except Exception as e:
        print("  [ERR] {}".format(e))
    print()
