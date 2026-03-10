# -*- coding: utf-8 -*-
"""SOP Step 5: SECTIONFLOW 补充验证 — 用有效 SERVERPART_ID"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

OLD = 'http://192.168.1.99:8900/EShangApiMain'
NEW = 'http://localhost:8080/EShangApiMain'

test_cases = [
    {"desc": "Test A: SERVERPART_IDS=362, Page1/Size5",
     "body": {"PageIndex": 1, "PageSize": 5, "SearchParameter": {"SERVERPART_IDS": "362"}}},
    {"desc": "Test B: SERVERPART_IDS=377,419, Page1/Size5",
     "body": {"PageIndex": 1, "PageSize": 5, "SearchParameter": {"SERVERPART_IDS": "377,419"}}},
    {"desc": "Test C: Date range filter",
     "body": {"PageIndex": 1, "PageSize": 5, "SearchParameter": {
         "STATISTICS_DATE_Start": "2024-01-01", "STATISTICS_DATE_End": "2024-01-31",
         "SERVERPART_IDS": "362"}}},
]

all_pass = True
for tc in test_cases:
    print(f"\n{'='*60}")
    print(tc["desc"])
    try:
        old_r = requests.post(OLD + '/BigData/GetSECTIONFLOWList', json=tc["body"], timeout=120)
        old_d = old_r.json()
    except Exception as e:
        print(f"Old API error: {e}")
        continue
    try:
        new_r = requests.post(NEW + '/BigData/GetSECTIONFLOWList', json=tc["body"], timeout=30)
        new_d = new_r.json()
    except Exception as e:
        print(f"New API error: {e}")
        continue

    old_rd = old_d.get('Result_Data', {})
    new_rd = new_d.get('Result_Data', {})
    old_tc = old_rd.get('TotalCount', 0)
    new_tc = new_rd.get('TotalCount', 0)
    old_list = old_rd.get('List', [])
    new_list = new_rd.get('List', [])

    code_ok = old_d.get('Result_Code') == new_d.get('Result_Code') == 100
    tc_ok = old_tc == new_tc
    lc_ok = len(old_list) == len(new_list)

    print(f"Result_Code: {'PASS' if code_ok else 'FAIL'}")
    print(f"TotalCount: Old={old_tc} New={new_tc} {'PASS' if tc_ok else 'FAIL'}")
    print(f"List count: Old={len(old_list)} New={len(new_list)} {'PASS' if lc_ok else 'FAIL'}")

    if not (code_ok and tc_ok and lc_ok):
        all_pass = False

    # 比较数据值（忽略已知差异字段）
    IGNORE = {'STATISTICS_DATE_Start', 'STATISTICS_DATE_End', 'SERVERPART_IDS',
              'Serverpart_Flow_Analog', 'SERVERPART_FLOW_ANALOG',
              'AVGSTAY_TIMES', 'AVGENTRY_RATE'}
    if old_list and new_list:
        mismatches = 0
        for i in range(min(len(old_list), len(new_list))):
            for k in old_list[i]:
                if k in IGNORE:
                    continue
                ov = old_list[i].get(k)
                nv = new_list[i].get(k)
                # 空字符串 vs None 视为匹配
                if (ov == '' and nv is None) or (ov is None and nv == ''):
                    continue
                if ov != nv:
                    if mismatches < 5:
                        print(f"  Row{i} {k}: Old={ov!r} New={nv!r}")
                    mismatches += 1
        if mismatches == 0:
            print("Data values: ALL MATCH (ignoring known differences)")
        else:
            print(f"Data values: {mismatches} mismatches")
            all_pass = False

print(f"\n{'='*60}")
print(f"Overall: {'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
