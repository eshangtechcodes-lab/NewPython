from __future__ import annotations
# -*- coding: utf-8 -*-
"""
Finance ATTACHMENT 表迁移脚本
将 Oracle FINANCE_RUNNING.T_ATTACHMENT 和 FINANCE_STORAGE.T_ATTACHMENT
迁移到达梦的 T_F_ATTACHMENT_RUNNING 和 T_F_ATTACHMENT_STORAGE

因达梦中已有 CONTRACT_STORAGE.T_ATTACHMENT（同名但不同结构），使用别名避免冲突
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import oracledb
import dmPython
from datetime import datetime

ORACLE_CONFIG = {"user": "highway_exchange", "password": "qrwl", "dsn": "192.168.1.99/orcl"}
DM_CONFIG = {"user": "NEWPYTHON", "password": "NewPython@2025", "server": "192.168.1.99", "port": 5236}

# 排除 BLOB 列（ATTACHMENT_CONTENT），API 不需要文件内容
COLUMNS = "ATTACHMENT_ID, ATTACHMENT_NAME, ATTACHMENT_DESC, CREATEDATE, PROINST_ID, PRESONNAME, OTHER_NAME"

TABLES = [
    ("FINANCE_RUNNING", "T_ATTACHMENT", "T_F_ATTACHMENT_RUNNING"),
    ("FINANCE_STORAGE", "T_ATTACHMENT", "T_F_ATTACHMENT_STORAGE"),
]


def migrate_finance_attachment():
    print("初始化 Oracle Client...")
    oracledb.init_oracle_client(lib_dir=r"E:\workfile\JAVA\NewAPI\oracle_client")
    
    ora_conn = oracledb.connect(**ORACLE_CONFIG)
    print("Oracle 连接成功")
    
    for oracle_schema, oracle_table, dm_table in TABLES:
        print(f"\n{'='*50}")
        print(f"  迁移: {oracle_schema}.{oracle_table} -> {dm_table}")
        print(f"{'='*50}")
        
        dm_conn = dmPython.connect(**DM_CONFIG)
        dm_cur = dm_conn.cursor()
        
        # 1. 建表
        try:
            dm_cur.execute(f"SELECT COUNT(*) FROM {dm_table}")
            count = dm_cur.fetchone()[0]
            print(f"  表已存在，{count} 条数据，将清空重建")
            dm_cur.execute(f"DROP TABLE {dm_table}")
            dm_conn.commit()
        except:
            print(f"  表不存在，将新建")
        
        create_sql = f"""
        CREATE TABLE {dm_table} (
            ATTACHMENT_ID INT NOT NULL,
            ATTACHMENT_NAME VARCHAR(200),
            ATTACHMENT_DESC VARCHAR(1000),
            CREATEDATE TIMESTAMP,
            PROINST_ID INT,
            PRESONNAME VARCHAR(200),
            OTHER_NAME VARCHAR(500),
            PRIMARY KEY (ATTACHMENT_ID)
        )
        """
        dm_cur.execute(create_sql)
        dm_conn.commit()
        print(f"  建表成功")
        
        # 表注释
        dm_cur.execute(f"COMMENT ON TABLE {dm_table} IS '财务附件（{oracle_schema}）'")
        dm_conn.commit()
        
        # 2. 迁移数据
        ora_cur = ora_conn.cursor()
        ora_cur.execute(f"SELECT {COLUMNS} FROM {oracle_schema}.{oracle_table}")
        rows = ora_cur.fetchall()
        total = len(rows)
        print(f"  Oracle 源数据: {total} 条")
        
        if total > 0:
            placeholders = ",".join(["?" for _ in range(7)])
            insert_sql = f"INSERT INTO {dm_table} ({COLUMNS}) VALUES ({placeholders})"
            
            batch_size = 2000
            migrated = 0
            for i in range(0, total, batch_size):
                batch = rows[i:i+batch_size]
                batch_values = []
                for row in batch:
                    vals = []
                    for v in row:
                        if isinstance(v, datetime):
                            vals.append(v.strftime("%Y-%m-%d %H:%M:%S"))
                        elif isinstance(v, str):
                            # 处理无法编码为 GBK 的特殊字符（如欧元符号 €）
                            try:
                                v.encode('gbk')
                                vals.append(v)
                            except UnicodeEncodeError:
                                vals.append(v.encode('gbk', errors='replace').decode('gbk'))
                        else:
                            vals.append(v)
                    batch_values.append(vals)
                dm_cur.executemany(insert_sql, batch_values)
                dm_conn.commit()
                migrated += len(batch)
                print(f"  已迁移: {migrated}/{total} 条")
        
        # 3. 校验
        dm_cur.execute(f"SELECT COUNT(*) FROM {dm_table}")
        dm_count = dm_cur.fetchone()[0]
        print(f"  达梦数据: {dm_count} 条")
        print(f"  {'✅ 行数一致' if dm_count == total else '❌ 行数不一致'}")
        
        ora_cur.close()
        dm_cur.close()
        dm_conn.close()
    
    ora_conn.close()
    print("\n迁移完成！")


if __name__ == "__main__":
    migrate_finance_attachment()
