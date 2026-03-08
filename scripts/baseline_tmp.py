# -*- coding: utf-8 -*-
"""查找有效的 ServerpartShopIds 并测试基准数据"""
import requests
import dmPython

# 1. 达梦数据库
conn = dmPython.connect(user='SYSDBA', password='NewPython@2025', server='192.168.1.99', port=5236)
cur = conn.cursor()

# 检查 T_BRAND 表
try:
    cur.execute("SELECT COUNT(*) FROM COOP_MERCHANT.T_BRAND")
    cnt = cur.fetchone()[0]
    print(f"COOP_MERCHANT.T_BRAND: {cnt} 条")
except Exception as e:
    print(f"COOP_MERCHANT.T_BRAND 不存在或无权限: {e}")

# 查 T_SERVERPARTSHOP 有 BUSINESS_BRAND 的门店
cur.execute("""SELECT SERVERPARTSHOP_ID, BUSINESS_BRAND, BRAND_NAME 
    FROM T_SERVERPARTSHOP 
    WHERE BUSINESS_BRAND IS NOT NULL 
    ORDER BY SERVERPARTSHOP_ID 
    FETCH FIRST 10 ROWS ONLY""")
rows = cur.fetchall()
print(f"\n有 BUSINESS_BRAND 的门店(前10):")
ids = []
for r in rows:
    print(f"  ID={r[0]}, BRAND={r[1]}, NAME={r[2]}")
    ids.append(str(r[0]))

cur.close()
conn.close()

# 2. 调原 API
if ids:
    id_str = ",".join(ids[:5])
    print(f"\n测试 IDs: {id_str}")
    url = f"http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBusinessBrandList?ServerpartShopIds={id_str}&ShowWholePower=true"
    r = requests.get(url, timeout=60)
    d = r.json()
    rd = d.get("Result_Data", {})
    lst = rd.get("List", [])
    print(f"Code: {d.get('Result_Code')}, TC: {rd.get('TotalCount')}, Count: {len(lst)}")
    if lst:
        print(f"字段: {list(lst[0].keys())}")
        first = {k: v for k, v in lst[0].items() if k != "ServerpartList"}
        print(f"First: {first}")
        slist = lst[0].get("ServerpartList", [])
        print(f"ServerpartList: {slist}")
else:
    print("无有效数据")
