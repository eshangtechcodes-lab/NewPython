# -*- coding: utf-8 -*-
"""
查找 T_OWNERUNIT 所在 Schema
"""
import oracledb

ORA_CLIENT_DIR = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"
try:
    oracledb.init_oracle_client(lib_dir=ORA_CLIENT_DIR)
except:
    pass

ORA_DSN = "127.0.0.1:1521/orcl"
ORA_PASS = "qrwl"
SCHEMAS = [
    "HIGHWAY_STORAGE", "HIGHWAY_SELLDATA", "COOP_MERCHANT", 
    "PLATFORM_DASHBOARD", "PLATFORM_FRAMEWORK", "CONTRACT_STORAGE", 
    "FINANCE_STORAGE", "HIGHWAY_EXCHANGE", "PLATFORM_DICTIONARY",
    "PLATFORM_MODULE", "WORKFLOW_SUPPORT", "WORKFLOW_INSTANCE"
]

def find_table():
    for s in SCHEMAS:
        try:
            conn = oracledb.connect(user=s.lower(), password=ORA_PASS, dsn=ORA_DSN)
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = 'T_OWNERUNIT'")
            row = cur.fetchone()
            if row[0] > 0:
                print(f"FOUND IN: {s}")
                cur.close()
                conn.close()
                return
            cur.close()
            conn.close()
        except:
            pass
    print("NOT FOUND ANYWHERE")

if __name__ == "__main__":
    find_table()
