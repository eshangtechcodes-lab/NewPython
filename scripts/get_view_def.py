# -*- coding: utf-8 -*-
"""查询 Oracle 视图定义并保存"""
import oracledb

ORACLE_CLIENT_PATH = r"E:\workfile\JAVA\NewAPI\oracle_client"
oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)

conn = oracledb.connect(user="highway_exchange", password="qrwl", dsn="192.168.1.99/orcl")
cur = conn.cursor()

# 获取视图完整定义（LONG 类型，需要设置 arraysize）
cur.execute("SELECT TEXT FROM ALL_VIEWS WHERE VIEW_NAME = 'V_WHOLE_COMMODITY' AND OWNER = 'HIGHWAY_STORAGE'")
row = cur.fetchone()
if row:
    view_text = row[0]
    # 保存到文件
    with open("scripts/baseline/v_whole_commodity_view.sql", "w", encoding="utf-8") as f:
        f.write("CREATE OR REPLACE VIEW V_WHOLE_COMMODITY AS\n")
        f.write(view_text)
    print(f"View definition saved, length: {len(view_text)} chars")
    print("--- VIEW TEXT ---")
    print(view_text)
else:
    print("View not found")
conn.close()
