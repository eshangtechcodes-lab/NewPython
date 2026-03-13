"""
深度SQL诊断 — 查每个差异接口的具体SQL逻辑差异
对比旧API(C#)和新API(Python)的查询条件
"""
import json
import requests

NEW_BASE = "http://127.0.0.1:8080/CommercialApi"
OLD_BASE = "http://127.0.0.1:8900/CommercialApi"
DEBUG_URL = f"{NEW_BASE}/Debug/QuerySQL"

with open('scripts/test_results/baseline_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

session = requests.Session()
session.trust_env = False

def run_sql(sql):
    try:
        r = session.get(DEBUG_URL, params={"sql": sql, "db_type": "dm"}, timeout=15)
        d = r.json()
        return d.get("count", 0), d.get("data", [])
    except Exception as e:
        return -1, [str(e)]

def safe_get(url, params=None):
    try:
        r = session.get(url, params=params, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

print("=" * 80)
print("  深度SQL诊断")
print("=" * 80)

# ===== 1. GetRevenueTrend — 旧=0 新=12 =====
print("\n" + "─" * 80)
print("1. GetRevenueTrend (旧=0, 新=12)")
print("─" * 80)

entry = cache['results'].get('GET:/Revenue/GetRevenueTrend', {})
params = entry.get('params', {})
print(f"  参数: {json.dumps(params, ensure_ascii=False)}")

# 看新API的查询逻辑
# GetRevenueTrend查的是月度趋势
sm = params.get('StatisticsMonth', '')
province = params.get('pushProvinceCode', '')
print(f"  StatisticsMonth={sm}, pushProvinceCode={province}")

# 查底层data
cnt, data = run_sql(f"""SELECT STATISTICS_MONTH, SUM(REVENUE_AMOUNT) AS REV 
    FROM T_REVENUEMONTHLY A, T_SERVERPART B 
    WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.REVENUEMONTHLY_STATE = 1 AND B.STATISTIC_TYPE = 1000
    GROUP BY STATISTICS_MONTH ORDER BY STATISTICS_MONTH""")
print(f"  T_REVENUEMONTHLY 月份分布: {cnt}个月")
if data:
    for d in data[:3]:
        print(f"    月份={d.get('STATISTICS_MONTH')}, 营收={d.get('REV')}")
    print(f"    ... 共{cnt}个月")

# 看旧API的具体返回
old_resp = safe_get(f"{OLD_BASE}/Revenue/GetRevenueTrend", params=params)
old_data = old_resp.get("Result_Data", {})
old_code = old_resp.get("Result_Code", None)
print(f"  旧API返回: Code={old_code}, Data类型={type(old_data).__name__}")
if isinstance(old_data, dict):
    print(f"    TotalCount={old_data.get('TotalCount')}")
elif isinstance(old_data, str):
    print(f"    Data(str): {old_data[:100]}")
else:
    print(f"    Data: {str(old_data)[:100]}")

# ===== 2. GetSPRevenueRank — 旧=0 新=273 =====
print("\n" + "─" * 80)
print("2. GetSPRevenueRank (旧=0, 新=273)")
print("─" * 80)

entry = cache['results'].get('GET:/Revenue/GetSPRevenueRank', {})
params = entry.get('params', {})
print(f"  参数: {json.dumps(params, ensure_ascii=False)}")

old_resp = safe_get(f"{OLD_BASE}/Revenue/GetSPRevenueRank", params=params)
old_tc = old_resp.get("Result_Data", {})
old_code = old_resp.get("Result_Code", None)
if isinstance(old_tc, dict):
    print(f"  旧API: Code={old_code}, TotalCount={old_tc.get('TotalCount')}, ListLen={len(old_tc.get('List',[]))}")
else:
    print(f"  旧API: Code={old_code}, Data={str(old_tc)[:100]}")

new_resp = safe_get(f"{NEW_BASE}/Revenue/GetSPRevenueRank", params=params)
new_tc = new_resp.get("Result_Data", new_resp.get("data", {}))
if isinstance(new_tc, dict):
    print(f"  新API: TotalCount={new_tc.get('TotalCount')}, ListLen={len(new_tc.get('List',[]))}")

# ===== 3. GetTransactionDetailList — 旧=0 新=278 =====
print("\n" + "─" * 80)
print("3. GetTransactionDetailList (旧=0, 新=278)")
print("─" * 80)

entry = cache['results'].get('GET:/Revenue/GetTransactionDetailList', {})
params = entry.get('params', {})
print(f"  参数: {json.dumps(params, ensure_ascii=False)}")

old_resp = safe_get(f"{OLD_BASE}/Revenue/GetTransactionDetailList", params=params)
old_code = old_resp.get("Result_Code", None)
old_data = old_resp.get("Result_Data", {})
if isinstance(old_data, dict):
    print(f"  旧API: Code={old_code}, TotalCount={old_data.get('TotalCount')}, ListLen={len(old_data.get('List',[]))}")
else:
    print(f"  旧API: Code={old_code}, Data={str(old_data)[:100]}")

new_resp = safe_get(f"{NEW_BASE}/Revenue/GetTransactionDetailList", params=params)
new_data = new_resp.get("Result_Data", new_resp.get("data", {}))
if isinstance(new_data, dict):
    new_list = new_data.get("List", new_data.get("DataList", []))
    print(f"  新API: TotalCount={new_data.get('TotalCount')}, ListLen={len(new_list)}")
    if new_list:
        print(f"  新API第一条: {json.dumps(new_list[0], ensure_ascii=False)[:200]}")

# 查相关表数据
sp_id = params.get("ServerpartId", "416")
start_time = params.get("StartTime", "")
start_str = start_time.replace("-", "")

# 直接查T_ENDACCOUNT_TEMP
cnt1, _ = run_sql(f"SELECT COUNT(*) AS CNT FROM T_ENDACCOUNT_TEMP WHERE ENDACCOUNT_STATE = 1 AND SERVERPART_ID = {sp_id}")
print(f"\n  T_ENDACCOUNT_TEMP (SERVERPART_ID={sp_id}): {cnt1}条")
cnt2, _ = run_sql(f"SELECT COUNT(*) AS CNT FROM T_ENDACCOUNT_TEMP WHERE ENDACCOUNT_STATE = 1 AND SERVERPART_ID = {sp_id} AND STATISTICS_DATE >= {start_str}")
print(f"  T_ENDACCOUNT_TEMP (+ DATE>={start_str}): {cnt2}条")

# T_REVENUEDAILY
cnt3, _ = run_sql(f"SELECT COUNT(*) AS CNT FROM T_REVENUEDAILY WHERE REVENUEDAILY_STATE = 1 AND SERVERPART_ID = {sp_id} AND STATISTICS_DATE >= {start_str}")
print(f"  T_REVENUEDAILY (SERVERPART_ID={sp_id}, DATE>={start_str}): {cnt3}条")

# ===== 4. GetHolidaySPRAnalysis — 旧=8 新=7 =====
print("\n" + "─" * 80)
print("4. GetHolidaySPRAnalysis (旧=8, 新=7)")
print("─" * 80)

entry = cache['results'].get('GET:/Revenue/GetHolidaySPRAnalysis', {})
params = entry.get('params', {})
print(f"  参数: {json.dumps(params, ensure_ascii=False)}")

# 对比旧API和新API的详细列表
old_resp = safe_get(f"{OLD_BASE}/Revenue/GetHolidaySPRAnalysis", params=params)
old_data = old_resp.get("Result_Data", {})
old_list = old_data.get("List", []) if isinstance(old_data, dict) else []

new_resp = safe_get(f"{NEW_BASE}/Revenue/GetHolidaySPRAnalysis", params=params)
new_data = new_resp.get("Result_Data", new_resp.get("data", {}))
new_list = new_data.get("List", new_data.get("DataList", [])) if isinstance(new_data, dict) else []

print(f"  旧API: {len(old_list)}条")
for i, item in enumerate(old_list):
    node = item.get("node", {}) if isinstance(item, dict) else {}
    name = node.get("SPRegionTypeName", node.get("ServerpartName", ""))
    print(f"    [{i}] {name}")

print(f"  新API: {len(new_list)}条")
for i, item in enumerate(new_list):
    node = item.get("node", {}) if isinstance(item, dict) else {}
    name = node.get("SPRegionTypeName", node.get("ServerpartName", ""))
    print(f"    [{i}] {name}")

# 找出差异
old_names = set()
for item in old_list:
    node = item.get("node", {})
    old_names.add(node.get("SPRegionTypeName", "") or node.get("SPRegionTypeId", ""))
new_names = set()
for item in new_list:
    node = item.get("node", {})
    new_names.add(node.get("SPRegionTypeName", "") or node.get("SPRegionTypeId", ""))

missing = old_names - new_names
extra = new_names - old_names
if missing:
    print(f"  新API缺少: {missing}")
if extra:
    print(f"  新API多出: {extra}")

print("\n" + "=" * 80)
print("  诊断完成")
print("=" * 80)
