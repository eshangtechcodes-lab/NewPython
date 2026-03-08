# -*- coding: utf-8 -*-
"""修复两张表的行数不一致：清空并重新全量导入"""
import oracledb
import dmPython
import time

ORACLE_CLIENT_PATH = r"E:\workfile\JAVA\NewAPI\oracle_client"
oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)

ORACLE_CONFIG = {"user": "highway_exchange", "password": "qrwl", "dsn": "192.168.1.99/orcl"}
DM_CONFIG = {"user": "NEWPYTHON", "password": "NewPython@2025", "server": "192.168.1.99", "port": 5236}
BATCH_SIZE = 2000

def fix_table(ora_conn, dm_conn, schema, table_name):
    """清空达梦表并重新全量导入"""
    print(f"\n{'='*60}")
    print(f"  修复表: {schema}.{table_name}")
    print(f"{'='*60}")

    ora_cur = ora_conn.cursor()
    dm_cur = dm_conn.cursor()

    # 1. 清空达梦表
    print(f"  [1] 清空达梦表 {table_name}...")
    dm_cur.execute(f"DELETE FROM {table_name}")
    dm_conn.commit()
    print(f"  清空完成")

    # 2. 读取 Oracle 全量数据
    print(f"  [2] 读取 Oracle 全量数据...")
    ora_cur.execute(f"SELECT * FROM {schema}.{table_name}")
    col_names = [desc[0] for desc in ora_cur.description]
    print(f"  字段数: {len(col_names)}")

    # 3. 批量插入到达梦
    print(f"  [3] 全量插入到达梦...")
    placeholders = ",".join(["?" for _ in col_names])
    insert_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"

    total = 0
    start_time = time.time()
    batch = []
    for row in ora_cur:
        # 转换数据类型 + 处理 GBK 不兼容的 Unicode 字符
        converted = []
        for val in row:
            if hasattr(val, 'strftime'):
                converted.append(val.strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(val, str):
                # 将 GBK 无法编码的字符（如 PUA 区域 \ue771）替换为 ?
                try:
                    val.encode('gbk')
                    converted.append(val)
                except UnicodeEncodeError:
                    cleaned = val.encode('gbk', errors='replace').decode('gbk')
                    converted.append(cleaned)
            else:
                converted.append(val)
        batch.append(tuple(converted))

        if len(batch) >= BATCH_SIZE:
            dm_cur.executemany(insert_sql, batch)
            dm_conn.commit()
            total += len(batch)
            elapsed = time.time() - start_time
            speed = int(total / elapsed) if elapsed > 0 else 0
            print(f"  已插入: {total} 条 ({speed}条/秒)")
            batch = []

    if batch:
        dm_cur.executemany(insert_sql, batch)
        dm_conn.commit()
        total += len(batch)

    elapsed = time.time() - start_time
    print(f"  插入完成: {total} 条，耗时 {elapsed:.1f} 秒")

    # 4. 校验
    print(f"  [4] 数据校验...")
    ora_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}")
    ora_cnt = ora_cur.fetchone()[0]
    dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    dm_cnt = dm_cur.fetchone()[0]
    match = ora_cnt == dm_cnt
    print(f"  Oracle: {ora_cnt} 条")
    print(f"  达梦:   {dm_cnt} 条")
    print(f"  {'✅ 行数一致' if match else f'❌ 仍不一致！差异: {ora_cnt - dm_cnt}'}")

    return match


if __name__ == "__main__":
    ora = oracledb.connect(**ORACLE_CONFIG)
    dm = dmPython.connect(**DM_CONFIG)

    tables = [
        ("HIGHWAY_STORAGE", "T_COMMODITY"),
        ("HIGHWAY_STORAGE", "T_COMMODITY_BUSINESS"),
    ]

    all_ok = True
    for schema, table in tables:
        if not fix_table(ora, dm, schema, table):
            all_ok = False

    ora.close()
    dm.close()

    if all_ok:
        print("\n✅ 全部修复成功！")
    else:
        print("\n❌ 仍有表行数不一致！")
