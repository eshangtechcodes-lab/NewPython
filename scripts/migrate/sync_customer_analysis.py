# -*- coding: utf-8 -*-
import oracledb
import dmPython
import time

# Oracle 11g Thick 模式
ORA_CLIENT_DIR = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"
try:
    oracledb.init_oracle_client(lib_dir=ORA_CLIENT_DIR)
    print(f"Oracle Thick 模式初始化成功: {ORA_CLIENT_DIR}")
except Exception as ex:
    print(f"Oracle Thick 模式初始化: {ex}")

SCHEMA_ACCOUNTS = {
    "HIGHWAY_STORAGE": ("highway_storage", "qrwl"),
    "FINANCE_STORAGE": ("finance_storage", "qrwl"),
    "HIGHWAY_SELLDATA": ("highway_selldata", "qrwl"),
    "HIGHWAY_EXCHANGE": ("highway_exchange", "qrwl"),
    "PLATFORM_DASHBOARD": ("platform_dashboard", "qrwl"),
}
ORA_DSN = "127.0.0.1:1521/orcl"
DM_USER = "NEWPYTHON"
DM_PASS = "NewPython@2025"
DM_HOST = "127.0.0.1"
DM_PORT = 5236

# 需要处理的客群分析表（表名, schema, 是否需要重建）
TABLES = [
    ("T_CUSTOMERGROUP",        "HIGHWAY_SELLDATA", True),
    ("T_CUSTOMERGROUP_AMOUNT", "HIGHWAY_SELLDATA", True),
    ("T_CUSTOMER_CONSUME",     "HIGHWAY_SELLDATA", True),
    ("T_CUSTOMER_AGE",         "HIGHWAY_SELLDATA", True),
    ("T_CUSTOMER_GAC",         "HIGHWAY_SELLDATA", True),
    ("T_CUSTOMER_ANALYSIS",    "HIGHWAY_EXCHANGE", True),
]

def map_type(dt, dlen, prec, scale):
    dt = dt.upper()
    if dt in ("VARCHAR2","NVARCHAR2"):
        return f"VARCHAR({max(dlen or 50,1)})"
    elif dt in ("CHAR","NCHAR"):
        return f"CHAR({max(dlen or 1,1)})"
    elif dt == "NUMBER":
        if prec and scale and scale > 0:
            return f"DECIMAL({prec},{scale})"
        elif prec:
            if prec <= 5: return "SMALLINT"
            elif prec <= 10: return "INT"
            elif prec <= 19: return "BIGINT"
            else: return f"DECIMAL({prec})"
        else:
            return "DECIMAL(38,6)"
    elif dt == "FLOAT": return "DOUBLE"
    elif dt.startswith("DATE") or dt.startswith("TIMESTAMP"):
        return "TIMESTAMP"
    elif dt in ("CLOB","NCLOB","LONG"): return "CLOB"
    elif dt == "BLOB": return "BLOB"
    elif dt == "RAW": return f"VARBINARY({max(dlen or 16,1)})"
    else: return "VARCHAR(4000)"

def get_dm():
    return dmPython.connect(user=DM_USER, password=DM_PASS, server=DM_HOST, port=DM_PORT)

def get_ora(schema):
    user, pwd = SCHEMA_ACCOUNTS[schema]
    return oracledb.connect(user=user, password=pwd, dsn=ORA_DSN)

def rebuild_and_sync(table_name, schema, rebuild=False, batch_size=1000):
    print(f"\n{'='*70}")
    print(f"📦 {'重建+同步' if rebuild else '全量同步'}: {schema}.{table_name}")
    t0 = time.time()
    
    ora_conn = get_ora(schema)
    dm_conn = get_dm()
    ora_cur = ora_conn.cursor()
    dm_cur = dm_conn.cursor()
    
    try:
        # Oracle 行数
        ora_cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        ora_total = ora_cur.fetchone()[0]
        print(f"  Oracle 行数: {ora_total}")
        
        if rebuild:
            # Drop 达梦旧表
            try:
                dm_cur.execute(f'DROP TABLE "{table_name}"')
                dm_conn.commit()
                print(f"  🗑️ 达梦旧表已删除")
            except:
                print(f"  ⓘ 达梦表不存在，无需删除")
            
            # 从 Oracle 获取表结构并重建
            ora_cur.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE
                FROM USER_TAB_COLUMNS WHERE TABLE_NAME = '{table_name}' ORDER BY COLUMN_ID
            """)
            columns = ora_cur.fetchall()
            col_defs = []
            for c in columns:
                dm_type = map_type(c[1], c[2], c[3], c[4])
                null_str = "" if c[5] == "Y" else " NOT NULL"
                col_defs.append(f'    "{c[0]}" {dm_type}{null_str}')
            ddl = f'CREATE TABLE "{table_name}" (\n' + ",\n".join(col_defs) + "\n)"
            dm_cur.execute(ddl)
            dm_conn.commit()
            print(f"  ✅ 达梦表重建成功 ({len(columns)} 列)")
        else:
            # 清空旧数据
            try:
                dm_cur.execute(f'DELETE FROM "{table_name}"')
                dm_conn.commit()
                print(f"  🗑️ 达梦旧数据已清空")
            except Exception as e:
                print(f"  ❌ 清空失败: {e}")
                return False
        
        if ora_total == 0:
            print(f"  ⓘ Oracle 无数据")
            return True
        
        # 全量读取并插入
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
            clean_rows = []
            for row in rows:
                clean_row = tuple(v.read() if hasattr(v, 'read') else v for v in row)
                clean_rows.append(clean_row)
            try:
                dm_cur.executemany(insert_sql, clean_rows)
                dm_conn.commit()
                synced += len(clean_rows)
            except:
                for r in clean_rows:
                    try:
                        dm_cur.execute(insert_sql, r)
                        dm_conn.commit()
                        synced += 1
                    except:
                        errors += 1
            
            pct = synced * 100 // max(ora_total, 1)
            elapsed = time.time() - t0
            print(f"\r  ⏳ 进度: {synced}/{ora_total} ({pct}%) 耗时:{elapsed:.0f}s 错误:{errors}", end="", flush=True)
        
        print(f"\n  ✅ 完成: {synced}/{ora_total} 行, 错误 {errors}, 耗时 {time.time()-t0:.1f}s")
        return True
    except Exception as ex:
        print(f"\n  ❌ 失败: {ex}")
        return False
    finally:
        ora_cur.close(); dm_cur.close()
        ora_conn.close(); dm_conn.close()

def main():
    print("=" * 70)
    print("Oracle → Dameng 客群分析数据补充同步")
    print("=" * 70)
    results = []
    for table, schema, rebuild in TABLES:
        ok = rebuild_and_sync(table, schema, rebuild)
        results.append((table, schema, ok))
    print("\n" + "=" * 70)
    print("同步结果汇总:")
    for table, schema, ok in results:
        print(f"  {'✅' if ok else '❌'} {schema}.{table}")
    print("=" * 70)

if __name__ == "__main__":
    main()
