# -*- coding: utf-8 -*-
"""
差异同步 9 张已有表的数据
"""
import oracledb
import dmPython
import json
import os
from datetime import datetime

# Oracle Thick Mode 初始化
ORA_CLIENT_DIR = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"
try:
    oracledb.init_oracle_client(lib_dir=ORA_CLIENT_DIR)
    print(f"Oracle Thick 模式初始化成功: {ORA_CLIENT_DIR}")
except Exception as ex:
    print(f"Oracle Thick 模式初始化 (可能是由于已初始化过): {ex}")

# 数据库连接信息
ORA_DSN = "127.0.0.1:1521/orcl"
ORA_PASS = "qrwl"

DM_USER = "NEWPYTHON"
DM_PASS = "NewPython@2025"
DM_HOST = "127.0.0.1"
DM_PORT = 5236

# 配置：表名 -> (Oracle Schema, 主键字段)
EXISTING_TABLES_CONFIG = {
    "T_AUTOSTATISTICS": ("COOP_MERCHANT", "AUTOSTATISTICS_ID"),
    "T_BRAND": ("COOP_MERCHANT", "BRAND_ID"),
    "T_COOPMERCHANTS": ("COOP_MERCHANT", "COOPMERCHANTS_ID"),
    "T_RTCOOPMERCHANTS": ("COOP_MERCHANT", "RTCOOPMERCHANTS_ID"),
    "T_OWNERUNIT": ("COOP_MERCHANT", "OWNERUNIT_ID"), # 修正为 COOP_MERCHANT
    "T_SERVERPART": ("HIGHWAY_STORAGE", "SERVERPART_ID"),
    "T_SERVERPARTSHOP": ("HIGHWAY_STORAGE", "SERVERPARTSHOP_ID"),
    "T_SERVERPARTTYPE": ("HIGHWAY_STORAGE", "SERVERPARTTYPE_ID"),
    "T_SHOPCOUNT": ("HIGHWAY_STORAGE", "SHOPCOUNT_ID"),
}

def get_dm_connection():
    return dmPython.connect(user=DM_USER, password=DM_PASS, server=DM_HOST, port=DM_PORT, autoCommit=True)

def get_common_columns(ora_cur, dm_cur, table_name):
    """获取 Oracle 和 Dameng 的共有列名"""
    # 获取 Oracle 列
    ora_cur.execute(f'SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = \'{table_name}\'')
    ora_cols = set(row[0].upper() for row in ora_cur.fetchall())
    
    # 获取 Dameng 列
    dm_cur.execute(f"SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{table_name}'")
    dm_cols = set(row[0].upper() for row in dm_cur.fetchall())
    
    common = sorted(list(ora_cols.intersection(dm_cols)))
    return common

def sync_diff(table_name, schema, pk_col):
    print(f"\n--- 同步差异: {schema}.{table_name} (PK: {pk_col}) ---")
    
    # 1. 连接数据库
    dm_conn = get_dm_connection()
    dm_cur = dm_conn.cursor()
    
    try:
        ora_conn = oracledb.connect(user=schema.lower(), password=ORA_PASS, dsn=ORA_DSN)
    except Exception as e:
        print(f"  ❌ Oracle 连接失败 ({schema}): {e}")
        dm_cur.close()
        dm_conn.close()
        return

    ora_cur = ora_conn.cursor()
    
    # 2. 获取共有列
    common_cols = get_common_columns(ora_cur, dm_cur, table_name)
    if not common_cols:
        print(f"  ❌ 未找到共有列")
        ora_cur.close()
        ora_conn.close()
        dm_cur.close()
        dm_conn.close()
        return
    print(f"  共有列数: {len(common_cols)}")

    # 3. 获取 Dameng 已有主键
    dm_cur.execute(f'SELECT "{pk_col}" FROM "{table_name}"')
    existing_pks = set(row[0] for row in dm_cur.fetchall())
    print(f"  Dameng 现有记录: {len(existing_pks)}")
    
    # 4. 统计 Oracle 记录并获取主键
    try:
        ora_cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        ora_total = ora_cur.fetchone()[0]
        print(f"  Oracle 总记录: {ora_total}")
        
        ora_cur.execute(f'SELECT "{pk_col}" FROM "{table_name}"')
        ora_pks = [row[0] for row in ora_cur.fetchall()]
    except Exception as e:
        print(f"  ❌ Oracle 查询失败: {e}")
        ora_cur.close()
        ora_conn.close()
        dm_cur.close()
        dm_conn.close()
        return

    # 5. 找出缺失的主键
    missing_pks = [pk for pk in ora_pks if pk not in existing_pks]
    print(f"  缺失记录数: {len(missing_pks)}")
    
    if not missing_pks:
        print("  ✅ 数据已同步")
        ora_cur.close()
        ora_conn.close()
        dm_cur.close()
        dm_conn.close()
        return

    # 6. 分批同步缺失数据 (限制 5000 行样本)
    to_sync = missing_pks[:5000]
    if len(missing_pks) > 5000:
        print(f"  ⚠️ 缺失较多，本次仅同步前 5000 条")

    col_str = ", ".join(f'"{c}"' for c in common_cols)
    placeholders = ", ".join(["?" for _ in common_cols])
    insert_sql = f'INSERT INTO "{table_name}" ({col_str}) VALUES ({placeholders})'

    synced_count = 0
    batch_size = 500
    for i in range(0, len(to_sync), batch_size):
        batch_pks = to_sync[i:i+batch_size]
        in_pks = ", ".join([str(p) if isinstance(p, (int, float)) else f"'{p}'" for p in batch_pks])
        
        ora_cur.execute(f'SELECT {col_str} FROM "{table_name}" WHERE "{pk_col}" IN ({in_pks})')
        rows = ora_cur.fetchall()
        
        clean_rows = []
        for row in rows:
            clean_row = []
            for val in row:
                if isinstance(val, oracledb.LOB):
                    clean_row.append(val.read())
                else:
                    clean_row.append(val)
            clean_rows.append(tuple(clean_row))
            
        try:
            dm_cur.executemany(insert_sql, clean_rows)
            dm_conn.commit()
            synced_count += len(clean_rows)
        except Exception as e:
            print(f"  ❌ 批量插入失败: {e}，尝试逐行插入...")
            for r in clean_rows:
                try:
                    dm_cur.execute(insert_sql, r)
                    dm_conn.commit()
                    synced_count += 1
                except:
                    pass

    print(f"  ✅ 同步完成: {synced_count} 行")
    
    ora_cur.close()
    ora_conn.close()
    dm_cur.close()
    dm_conn.close()

def main():
    print(f"开始差异同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for table, cfg in EXISTING_TABLES_CONFIG.items():
        sync_diff(table, cfg[0], cfg[1])
    print(f"\n全部差异同步完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
