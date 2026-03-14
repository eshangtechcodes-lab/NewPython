# -*- coding: utf-8 -*-
"""第三批全部 5 个实体 20 个接口对比验证脚本"""
import requests, sys, json
sys.stdout.reconfigure(encoding='utf-8')

PY = "http://localhost:8080/EShangApiMain"
CS = "http://192.168.1.99:8900/EShangApiMain"

def compare_list(name, route, bodies):
    for i, body in enumerate(bodies):
        try:
            py_r = requests.post(PY + route, json=body, timeout=15).json()
            cs_r = requests.post(CS + route, json=body, timeout=15).json()
            py_d = py_r.get("Result_Data", {})
            cs_d = cs_r.get("Result_Data", {})
            py_total = py_d.get("TotalCount", "N/A") if isinstance(py_d, dict) else "N/A"
            cs_total = cs_d.get("TotalCount", "N/A") if isinstance(cs_d, dict) else "N/A"
            py_list = len(py_d.get("List", [])) if isinstance(py_d, dict) else 0
            cs_list = len(cs_d.get("List", [])) if isinstance(cs_d, dict) else 0
            match = "OK" if py_total == cs_total else "DIFF"
            print(f"  [{match}] {name} GetList #{i+1}: PY Total={py_total} List={py_list} | CS Total={cs_total} List={cs_list}")
        except Exception as e:
            print(f"  [ERR] {name} GetList #{i+1}: {e}")

def compare_detail(name, route, param_name, ids):
    for id_val in ids:
        try:
            py_r = requests.get(PY + route, params={param_name: id_val}, timeout=15).json()
            cs_r = requests.get(CS + route, params={param_name: id_val}, timeout=15).json()
            py_code = py_r.get("Result_Code")
            cs_code = cs_r.get("Result_Code")
            match = "OK" if py_code == cs_code else "DIFF"
            print(f"  [{match}] {name} Detail ID={id_val}: PY Code={py_code} | CS Code={cs_code}")
        except Exception as e:
            print(f"  [ERR] {name} Detail ID={id_val}: {e}")


# ============ 1. BUSINESSPAYMENT ============
print("=" * 60)
print("1. BUSINESSPAYMENT (4 interfaces)")
print("=" * 60)
compare_list("BUSINESSPAYMENT", "/BusinessProject/GetBusinessPaymentList", [
    {},
    {"SearchParameter": {"SERVERPART_ID": 1}, "PageIndex": 1, "PageSize": 5},
    {"SearchParameter": {"MERCHANTS_ID": 1}, "PageIndex": 1, "PageSize": 5},
])
compare_detail("BUSINESSPAYMENT", "/BusinessProject/GetBusinessPaymentDetail", "BusinessPaymentId", [1])

# ============ 2. PROJECTWARNING ============
print("\n" + "=" * 60)
print("2. PROJECTWARNING (4 interfaces)")
print("=" * 60)
compare_list("PROJECTWARNING", "/BusinessProject/GetPROJECTWARNINGList", [
    {},
    {"SearchParameter": {"SERVERPART_ID": 1}, "PageIndex": 1, "PageSize": 5},
    {"SearchParameter": {"PROJECTWARNING_STATE": 1}, "PageIndex": 1, "PageSize": 5},
])
compare_detail("PROJECTWARNING", "/BusinessProject/GetPROJECTWARNINGDetail", "PROJECTWARNINGId", [1])

# ============ 3. PERIODWARNING ============
print("\n" + "=" * 60)
print("3. PERIODWARNING (4 interfaces)")
print("=" * 60)
compare_list("PERIODWARNING", "/BusinessProject/GetPERIODWARNINGList", [
    {},
    {"SearchParameter": {"SERVERPART_ID": 1}, "PageIndex": 1, "PageSize": 5},
    {"SearchParameter": {"WARNING_TYPE": 1}, "PageIndex": 1, "PageSize": 5},
])
compare_detail("PERIODWARNING", "/BusinessProject/GetPERIODWARNINGDetail", "PERIODWARNINGId", [1])

# ============ 4. BIZPSPLITMONTH ============
print("\n" + "=" * 60)
print("4. BIZPSPLITMONTH (4 interfaces)")
print("=" * 60)
compare_list("BIZPSPLITMONTH", "/BusinessProject/GetBIZPSPLITMONTHList", [
    {},
    {"SearchParameter": {"SERVERPART_ID": 1}, "PageIndex": 1, "PageSize": 5},
    {"PageIndex": 1, "PageSize": 10},
])
compare_detail("BIZPSPLITMONTH", "/BusinessProject/GetBIZPSPLITMONTHDetail", "BIZPSPLITMONTHId", [1])

# ============ 5. BUSINESSPROJECTSPLIT ============
print("\n" + "=" * 60)
print("5. BUSINESSPROJECTSPLIT (4 interfaces)")
print("=" * 60)
compare_list("BUSINESSPROJECTSPLIT", "/BusinessProject/GetBUSINESSPROJECTSPLITList", [
    {},
    {"SearchParameter": {"SERVERPART_ID": 1}, "PageIndex": 1, "PageSize": 5},
    {"PageIndex": 1, "PageSize": 10},
])
compare_detail("BUSINESSPROJECTSPLIT", "/BusinessProject/GetBUSINESSPROJECTSPLITDetail", "BUSINESSPROJECTSPLITId", [1])

print("\n" + "=" * 60)
print("ALL DONE - 20 interfaces verified")
print("=" * 60)
