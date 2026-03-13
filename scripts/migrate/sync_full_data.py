# -*- coding: utf-8 -*-
"""
补充全量同步 - 之前只同步了 5000 条的表，现在全量补齐
策略：先清空达梦中旧数据，再从 Oracle 全量导入
"""
import oracledb
import dmPython
import time

# Oracle 11g 必须使用 Thick 模式
ORA_CLIENT_DIR = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"
try:
    oracledb.init_oracle_client(lib_dir=ORA_CLIENT_DIR)
    print(f"Oracle Thick 模式初始化成功: {ORA_CLIENT_DIR}")
except Exception as ex:
    print(f"Oracle Thick 模式初始化: {ex}")


# Oracle 连接信息（按 schema 分别连接）
SCHEMA_ACCOUNTS = {
    "HIGHWAY_STORAGE": ("highway_storage", "qrwl"),
    "FINANCE_STORAGE": ("finance_storage", "qrwl"),
    "HIGHWAY_SELLDATA": ("highway_selldata", "qrwl"),
    "HIGHWAY_EXCHANGE": ("highway_exchange", "qrwl"),
    "PLATFORM_DASHBOARD": ("platform_dashboard", "qrwl"),
}
ORA_DSN = "127.0.0.1:1521/orcl"

# Dameng 连接信息
DM_USER = "NEWPYTHON"
DM_PASS = "NewPython@2025"
DM_HOST = "127.0.0.1"
DM_PORT = 5236

# 需要全量补同步的表（表名, Oracle schema）
TABLES = [
    ("T_EXAMINEDETAIL",    "HIGHWAY_STORAGE"),
    ("T_MEETING",          "HIGHWAY_STORAGE"),
    ("T_PATROL",           "HIGHWAY_STORAGE"),
    ("T_SHOPCOUNT",        "HIGHWAY_STORAGE"),
    ("T_BUDGETDETAIL_AH",  "FINANCE_STORAGE"),
    ("T_ENDACCOUNT_TEMP",  "HIGHWAY_SELLDATA"),
    ("T_BUDGETPROJECT_AH", "FINANCE_STORAGE"),
    ("T_BUDGETEXPENSE",    "HIGHWAY_STORAGE"),
    ("T_SECTIONFLOW",      "HIGHWAY_SELLDATA"),
    ("T_ANALYSISINS",      "PLATFORM_DASHBOARD"),
    ("T_CUSTOMERGROUP",    "HIGHWAY_SELLDATA"),
    ("T_CUSTOMERGROUP_AMOUNT", "HIGHWAY_SELLDATA"),
    ("T_CUSTOMER_CONSUME", "HIGHWAY_SELLDATA"),
    ("T_CUSTOMER_AGE",     "HIGHWAY_SELLDATA"),
    ("T_CUSTOMER_GAC",     "HIGHWAY_SELLDATA"),
    ("T_CUSTOMER_ANALYSIS","HIGHWAY_EXCHANGE"),
]

def get_dm():
    return dmPython.connect(user=DM_USER, password=DM_PASS, server=DM_HOST, port=DM_PORT)

def get_ora(schema):
    user, pwd = SCHEMA_ACCOUNTS.get(schema, ("highway_exchange", "qrwl"))
    conn = oracledb.connect(user=user, password=pwd, dsn=ORA_DSN)
    return conn

def sync_full(table_name, schema, batch_size=1000):
    """全量同步：如果数量不一致，则清空达梦 -> 从Oracle全量导入"""
    print(f"\n{'='*70}")
    print(f"📦 检查同步: {schema}.{table_name}")
    t0 = time.time()
    
    # 连接
    try:
        ora_conn = get_ora(schema)
    except Exception as e:
        print(f"  ❌ Oracle 连接失败({schema}): {e}")
        return False
    
    dm_conn = get_dm()
    ora_cur = ora_conn.cursor()
    dm_cur = dm_conn.cursor()
    
    try:
        # 1. 查 Oracle 总行数
        ora_cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        ora_total = ora_cur.fetchone()[0]
        
        # 2. 查达梦总行数
        dm_total = 0
        try:
            dm_cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            dm_total = dm_cur.fetchone()[0]
        except:
            print(f"  ⚠️ 达梦表不存在或查询失败")
        
        print(f"  Oracle 行数: {ora_total}")
        print(f"  达梦   行数: {dm_total}")
        
        if ora_total == dm_total and ora_total > 0:
            print(f"  ✅ 数量一致，跳过同步")
            return True

        if ora_total == 0:
            print(f"  ⓘ Oracle 无数据，跳过")
            return True
        
        # 3. 清空达梦旧数据
        try:
            dm_cur.execute(f'DELETE FROM "{table_name}"')
            dm_conn.commit()
            print(f"  🗑️ 数量不一致，达梦旧数据已清空，开始同步...")
        except Exception as e:
            print(f"  ❌ 清空达梦失败: {e}")
            dm_conn.rollback()
            return False
        
        # 4. 从 Oracle 读取全部数据
        ora_cur.execute(f'SELECT * FROM "{table_name}"')
        columns = [desc[0] for desc in ora_cur.description]
        col_list = ", ".join(f'"{c}"' for c in columns)
        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f'INSERT INTO "{table_name}" ({col_list}) VALUES ({placeholders})'
        
        synced = 0
        errors = 0
        while True:
            rows = ora_cur.fetchmany(batch_size)
            if not rows:
                break
            
            # 处理 LOB 类型
            clean_rows = []
            for row in rows:
                clean_row = []
                for val in row:
                    if hasattr(val, 'read'):  # LOB
                        clean_row.append(val.read() if val else None)
                    else:
                        clean_row.append(val)
                clean_rows.append(tuple(clean_row))
            
            try:
                dm_cur.executemany(insert_sql, clean_rows)
                dm_conn.commit()
                synced += len(clean_rows)
            except Exception as ex:
                # 批量失败，逐行插入
                for r in clean_rows:
                    try:
                        dm_cur.execute(insert_sql, r)
                        dm_conn.commit()
                        synced += 1
                    except:
                        errors += 1
            
            # 进度
            pct = synced * 100 // ora_total
            elapsed = time.time() - t0
            print(f"\r  ⏳ 进度: {synced}/{ora_total} ({pct}%) 耗时:{elapsed:.0f}s 错误:{errors}", end="", flush=True)
        
        print(f"\n  ✅ 完成: 同步 {synced}/{ora_total} 行, 错误 {errors}, 耗时 {time.time()-t0:.1f}s")
        return True
        
    except Exception as ex:
        print(f"\n  ❌ 同步失败: {ex}")
        return False
    finally:
        ora_cur.close()
        dm_cur.close()
        ora_conn.close()
        dm_conn.close()


def main():
    print("=" * 70)
    print("Oracle → Dameng 全量数据补充同步")
    print("=" * 70)
    
    results = []
    for table, schema in TABLES:
        ok = sync_full(table, schema)
        results.append((table, schema, ok))
    
    print("\n" + "=" * 70)
    print("同步结果汇总:")
    for table, schema, ok in results:
        status = "✅" if ok else "❌"
        print(f"  {status} {schema}.{table}")
    print("=" * 70)


if __name__ == "__main__":
    main()
