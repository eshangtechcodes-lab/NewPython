# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, '.')
from core.database import DatabaseHelper
dm = DatabaseHelper(db_type='dm')

# 直接查数据量
rows = dm.execute_query('SELECT COUNT(1) AS CNT FROM "T_BUDGETEXPENSE"')
print("T_BUDGETEXPENSE 数据量:", rows)

# 看前2条数据结构
rows2 = dm.execute_query('SELECT * FROM "T_BUDGETEXPENSE" FETCH FIRST 2 ROWS ONLY')
if rows2:
    print("列名:", list(rows2[0].keys()))
    for r in rows2:
        print(r)
else:
    print("无数据")

# 检查 T_ENDACCOUNT_TEMP
try:
    rows3 = dm.execute_query('SELECT COUNT(1) AS CNT FROM "T_ENDACCOUNT_TEMP"')
    print("\nT_ENDACCOUNT_TEMP 数据量:", rows3)
except Exception as e:
    print(f"\nT_ENDACCOUNT_TEMP 不存在: {e}")

# 检查 T_BUDGETDETAIL_AH (就是 GetBudgetProjectDetailList 查的表)
rows4 = dm.execute_query('SELECT COUNT(1) AS CNT FROM "T_BUDGETDETAIL_AH"')
print("T_BUDGETDETAIL_AH 数据量:", rows4)
