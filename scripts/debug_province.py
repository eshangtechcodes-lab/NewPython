"""调试: 检查 _get_province_id_by_code 的映射"""
from core.database import DatabaseHelper

db = DatabaseHelper()

# 查询 FIELDENUM_ID 映射
sql = "SELECT FIELDENUM_ID, FIELDENUM_VALUE FROM T_FIELDENUM WHERE FIELDEXPLAIN_ID = 154 AND FIELDENUM_VALUE = '340000'"
rows = db.execute_query(sql)
print(f"直接查 340000: {rows}")

# 查看 FIELDEXPLAIN_ID=154 有哪些值
sql2 = "SELECT FIELDENUM_ID, FIELDENUM_VALUE FROM T_FIELDENUM WHERE FIELDEXPLAIN_ID = 154"
rows2 = db.execute_query(sql2)
print(f"\nFIELDEXPLAIN_ID=154 共 {len(rows2)} 条:")
for r in rows2[:10]:
    print(f"  ID={r.get('FIELDENUM_ID')}, VALUE={r.get('FIELDENUM_VALUE')}")

# 查看 T_SERVERPART 的 PROVINCE_CODE 分布
sql3 = "SELECT PROVINCE_CODE, COUNT(*) AS CNT FROM T_SERVERPART WHERE STATISTICS_TYPE = 1000 GROUP BY PROVINCE_CODE ORDER BY CNT DESC"
rows3 = db.execute_query(sql3)
print(f"\nT_SERVERPART PROVINCE_CODE 分布:")
for r in rows3[:10]:
    print(f"  PROVINCE_CODE={r.get('PROVINCE_CODE')}, COUNT={r.get('CNT')}")
