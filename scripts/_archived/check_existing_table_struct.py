# -*- coding: utf-8 -*-
"""
查看 9 张已有表的结构，确定主键
"""
import dmPython

DM_USER = "NEWPYTHON"
DM_PASS = "NewPython@2025"
DM_HOST = "127.0.0.1"
DM_PORT = 5236

EXISTING_TABLES = [
    "T_AUTOSTATISTICS", "T_BRAND", "T_OWNERUNIT", "T_SERVERPART",
    "T_SERVERPARTSHOP", "T_SERVERPARTTYPE", "T_SHOPCOUNT",
    "T_COOPMERCHANTS", "T_RTCOOPMERCHANTS"
]

def check_structure():
    conn = dmPython.connect(user=DM_USER, password=DM_PASS, server=DM_HOST, port=DM_PORT)
    cur = conn.cursor()
    
    for table_name in EXISTING_TABLES:
        print(f"\n[{table_name}]")
        # 获取列名
        try:
            cur.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{table_name}'")
            cols = cur.fetchall()
            for col in cols:
                print(f"  {col[0]} ({col[1]})")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_structure()
