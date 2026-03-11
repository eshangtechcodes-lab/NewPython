# -*- coding: utf-8 -*-
"""检查 BigData/Revenue 相关表"""
import dmPython

conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()

tables_to_check = [
    'T_SECTIONFLOW', 'T_SECTIONFLOWMONTH', 'T_ENDACCOUNT_DAILY',
    'T_TRANSACTIONANALYSIS', 'T_BAYONETDAILY_AH',
    'T_BAYONETHOURMONTH_AH', 'T_BAYONETOWMONTHLY_AH',
    'T_BAYONETPROVINCEMONTH_AH', 'T_BAYONETOWNERMONTH_AH',
]

print("=== BigData/Revenue 相关表检查 ===")
for t in tables_to_check:
    try:
        cur.execute(f'SELECT COUNT(*) FROM "{t}"')
        count = cur.fetchone()[0]
        print(f"  {t}: {count} 行")
    except Exception as e:
        print(f"  {t}: ❌ 不存在 ({e})")

conn.close()
