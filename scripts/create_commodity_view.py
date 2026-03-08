# -*- coding: utf-8 -*-
"""为缺失的省份分表创建空表（结构与 T_COMMODITY 完全一致）"""
import dmPython

DM_CONFIG = {"user": "NEWPYTHON", "password": "NewPython@2025", "server": "192.168.1.99", "port": 5236}
dm = dmPython.connect(**DM_CONFIG)
cur = dm.cursor()

# 获取 T_COMMODITY 的列信息
cur.execute("SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'T_COMMODITY' ORDER BY COLUMN_ID")
cols = cur.fetchall()

missing = ['T_COMMODITY_500000', 'T_COMMODITY_510000', 'T_COMMODITY_520000',
           'T_COMMODITY_530000', 'T_COMMODITY_630000', 'T_COMMODITY_734100']

for tname in missing:
    col_defs = []
    for cn, dt, dl in cols:
        if dt in ('INT', 'SMALLINT', 'BIGINT'):
            col_defs.append(f'"{cn}" {dt}')
        elif 'CHAR' in dt:
            col_defs.append(f'"{cn}" {dt}({dl})')
        elif 'DECIMAL' in dt or 'NUMERIC' in dt:
            col_defs.append(f'"{cn}" {dt}')
        elif 'TIMESTAMP' in dt or 'DATE' in dt:
            col_defs.append(f'"{cn}" TIMESTAMP')
        else:
            col_defs.append(f'"{cn}" {dt}')

    create_sql = f'CREATE TABLE {tname} ({", ".join(col_defs)})'
    try:
        cur.execute(create_sql)
        dm.commit()
        print(f'{tname}: 创建成功（空表）')
    except Exception as e:
        print(f'{tname}: 失败 - {e}')

# 创建视图
print()
try:
    cur.execute("DROP VIEW V_WHOLE_COMMODITY")
    dm.commit()
except Exception:
    pass

with open("scripts/baseline/v_whole_commodity_view.sql", "r", encoding="utf-8") as f:
    view_sql = f.read()
view_sql = view_sql.replace("HIGHWAY_STORAGE.", "")

try:
    cur.execute(view_sql)
    dm.commit()
    print("V_WHOLE_COMMODITY 视图创建成功!")
    cur.execute("SELECT COUNT(*) FROM V_WHOLE_COMMODITY")
    print(f"视图总行数: {cur.fetchone()[0]}")
except Exception as e:
    print(f"视图创建失败: {e}")

dm.close()
