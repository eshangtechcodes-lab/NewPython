"""
深入分析 SP=420 和 SP=433 的差异根因
"""
import requests
BASE = "http://127.0.0.1:8080/CommercialApi/Debug/QuerySQL"
def query(sql):
    r = requests.get(BASE, params={"sql": sql}, timeout=15).json()
    return r.get("data", []) if r.get("ok") else []

print("=== SP=420 合并门店分析 ===")
# SP=420 那个合并记录的 ShopIds
shop_ids_str = "2404,2405,2406,2407,2408,2409,2410,2411,2412,2413,2414,2415,2416,2417,2418,2419,2420,2421,1050,1051,2423"
sql_420 = f"""
SELECT SERVERPARTSHOP_ID, BUSINESS_BRAND, BRAND_NAME, BUSINESS_TRADE, BUSINESS_TRADENAME 
FROM T_SERVERPARTSHOP 
WHERE SERVERPARTSHOP_ID IN ({shop_ids_str})
"""
rows_420 = query(sql_420)
for r in rows_420:
    print(f"ShopId={r['SERVERPARTSHOP_ID']}, Brand={r['BUSINESS_BRAND']}({r['BRAND_NAME']}), Trade={r['BUSINESS_TRADE']}({r['BUSINESS_TRADENAME']})")

print("\n=== SP=433 结算模式分析 ===")
sql_433 = """
SELECT BUSINESSPROJECT_ID, BUSINESSPROJECT_NAME, BUSINESS_TYPE, SETTLEMENT_MODES 
FROM T_BUSINESSPROJECT 
WHERE BUSINESSPROJECT_ID IN (1282, 601)
"""
rows_433 = query(sql_433)
for r in rows_433:
    print(f"BP={r['BUSINESSPROJECT_ID']}, Name={r['BUSINESSPROJECT_NAME']}, BTT={r['BUSINESS_TYPE']}, Settle={r['SETTLEMENT_MODES']}")
