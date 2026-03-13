from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding='utf-8')
import oracledb

# 查找 Oracle 中所有包含 ATTACHMENT 的表及其 schema
oracledb.init_oracle_client(lib_dir=r"E:\workfile\JAVA\NewAPI\oracle_client")
conn = oracledb.connect(user='highway_exchange', password='qrwl', dsn='192.168.1.99/orcl')
cur = conn.cursor()

print('=== Oracle 中所有包含 ATTACHMENT 的表 ===')
cur.execute("""
    SELECT OWNER, TABLE_NAME 
    FROM ALL_TABLES 
    WHERE TABLE_NAME LIKE '%ATTACHMENT%'
    ORDER BY OWNER, TABLE_NAME
""")
for row in cur.fetchall():
    print(f'  {row[0]}.{row[1]}')

# FINANCE_RUNNING 下的表
schemas_to_check = ['FINANCE_RUNNING', 'FINANCE_STORAGE']
for schema in schemas_to_check:
    print(f'\n=== {schema}.T_ATTACHMENT 列结构 ===')
    cur.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION
        FROM ALL_TAB_COLUMNS
        WHERE OWNER = '{schema}' AND TABLE_NAME = 'T_ATTACHMENT'
        ORDER BY COLUMN_ID
    """)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f'  {row[0]:30s} {row[1]:15s} len={row[2]} prec={row[3]}')
        # 获取数据条数
        cur.execute(f"SELECT COUNT(*) FROM {schema}.T_ATTACHMENT")
        print(f'  数据量: {cur.fetchone()[0]} 条')
    else:
        print('  表不存在或无权限')

conn.close()
