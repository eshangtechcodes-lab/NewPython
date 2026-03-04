# -*- coding: utf-8 -*-
"""查询达梦中 T_BRAND 表的位置和数据"""
import dmPython

# 先用 DMNEW 查所有 T_BRAND 表
print("=== 用 DMNEW 查询 T_BRAND 表 ===")
conn = dmPython.connect(user='DMNEW', password='Dmnew@2025Aa', server='127.0.0.1', port=5236)
cur = conn.cursor()
cur.execute("SELECT OWNER, TABLE_NAME FROM ALL_TABLES WHERE TABLE_NAME = 'T_BRAND'")
rows = cur.fetchall()
print(f"找到 {len(rows)} 个 T_BRAND 表:")
for r in rows:
    print(f"  Schema: {r[0]}, Table: {r[1]}")

# 尝试直接查询各 schema 下的数据
for schema in [r[0] for r in rows]:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {schema}.T_BRAND")
        count = cur.fetchone()[0]
        print(f"\n  {schema}.T_BRAND 数据量: {count} 条")
        if count > 0:
            cur.execute(f"SELECT BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY FROM {schema}.T_BRAND WHERE ROWNUM <= 5")
            for row in cur.fetchall():
                print(f"    ID={row[0]}, 名称={row[1]}, 分类={row[2]}, 业态={row[3]}")
    except Exception as ex:
        print(f"  {schema}.T_BRAND 查询失败: {ex}")

cur.close()
conn.close()

# 也试试 NEWPYTHON 用户
print("\n=== 用 NEWPYTHON 查询 ===")
try:
    conn2 = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
    cur2 = conn2.cursor()
    cur2.execute("SELECT COUNT(*) FROM T_BRAND")
    count = cur2.fetchone()[0]
    print(f"NEWPYTHON.T_BRAND 数据量: {count} 条")
    if count > 0:
        cur2.execute("SELECT BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY FROM T_BRAND WHERE ROWNUM <= 5")
        for row in cur2.fetchall():
            print(f"  ID={row[0]}, 名称={row[1]}, 分类={row[2]}, 业态={row[3]}")
    cur2.close()
    conn2.close()
except Exception as ex:
    print(f"NEWPYTHON 查询失败: {ex}")
