# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, ".")
from core.database import DatabaseHelper
dm = DatabaseHelper(db_type="dm")

# 查 302 在明细表有没有记录
rows = dm.execute_query('SELECT COUNT(1) AS CNT FROM "T_BUDGETDETAIL_AH" WHERE "BUDGETPROJECT_AH_ID" = 302')
print("ID=302明细:", rows)

# 找有明细的ID
rows2 = dm.execute_query("""
    SELECT "BUDGETPROJECT_AH_ID", COUNT(1) AS CNT 
    FROM "T_BUDGETDETAIL_AH" 
    GROUP BY "BUDGETPROJECT_AH_ID" 
    ORDER BY CNT DESC 
    FETCH FIRST 5 ROWS ONLY
""")
print("有明细的ID:", rows2)
