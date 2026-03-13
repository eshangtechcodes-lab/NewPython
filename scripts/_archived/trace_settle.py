"""
再查一下 BP=603 和 1698 的信息 (SP=433 曹阿瞒等)
"""
import requests
BASE = "http://127.0.0.1:8080/CommercialApi/Debug/QuerySQL"
def query(sql):
    r = requests.get(BASE, params={"sql": sql}, timeout=15).json()
    return r.get("data", []) if r.get("ok") else []

print("=== SP=433 实测原始 BP 映射 ===")
# 从 BW 取实时的 BP_ID
sql_bw = "SELECT DISTINCT BUSINESSPROJECT_ID, SERVERPARTSHOP_NAME, BUSINESSTRADETYPE FROM T_BUSINESSWARNING WHERE STATISTICS_MONTH=202602 AND SERVERPART_ID=433"
rows_bw = query(sql_bw)
for r in rows_bw:
    bpid = r.get("BUSINESSPROJECT_ID")
    if bpid:
        bp_info = query(f"SELECT BUSINESSPROJECT_NAME, BUSINESS_TYPE, SETTLEMENT_MODES FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID={bpid}")
        if bp_info:
            b = bp_info[0]
            print(f"Shop={r['SERVERPARTSHOP_NAME']}, BP={bpid}, BTT_BW={r['BUSINESSTRADETYPE']}, BTT_BP={b['BUSINESS_TYPE']}, Settle_BP={b['SETTLEMENT_MODES']}")
        else:
            print(f"Shop={r['SERVERPARTSHOP_NAME']}, BP={bpid}, (无T_BUSINESSPROJECT信息)")
