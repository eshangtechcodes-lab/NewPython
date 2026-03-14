# -*- coding: utf-8 -*-
"""
测试使用 Oracle 11g 本地安装的 OCI 库进行 Thick 模式连接
"""
import oracledb

ORA_HOME = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"

print(f"尝试使用 Oracle 11g Thick 模式: {ORA_HOME}")
try:
    oracledb.init_oracle_client(lib_dir=ORA_HOME)
    print("✅ Oracle Thick 模式初始化成功!")
except Exception as ex:
    print(f"❌ 初始化失败: {ex}")
    import sys
    sys.exit(1)

# 测试连接
print("\n测试连接 highway_storage...")
try:
    conn = oracledb.connect(user="highway_storage", password="qrwl", dsn="10.0.0.201:1521/orcl")
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    r = cur.fetchone()
    print(f"✅ 连接成功! SELECT 1 = {r[0]}")

    # 查看有多少表
    cur.execute("SELECT COUNT(*) FROM USER_TABLES")
    cnt = cur.fetchone()[0]
    print(f"📊 highway_storage 表数量: {cnt}")

    # 列出前20张表
    cur.execute("SELECT TABLE_NAME FROM USER_TABLES ORDER BY TABLE_NAME FETCH FIRST 20 ROWS ONLY")
    rows = cur.fetchall()
    for row in rows:
        print(f"  {row[0]}")

    cur.close()
    conn.close()
except Exception as ex:
    print(f"❌ 连接失败: {ex}")
    # 尝试 127.0.0.1
    print("\n尝试 127.0.0.1...")
    try:
        conn = oracledb.connect(user="highway_storage", password="qrwl", dsn="127.0.0.1:1521/orcl")
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM DUAL")
        r = cur.fetchone()
        print(f"✅ 127.0.0.1 连接成功! SELECT 1 = {r[0]}")
        cur.execute("SELECT COUNT(*) FROM USER_TABLES")
        cnt = cur.fetchone()[0]
        print(f"📊 highway_storage 表数量: {cnt}")
        cur.close()
        conn.close()
    except Exception as ex2:
        print(f"❌ 127.0.0.1 也失败: {ex2}")
