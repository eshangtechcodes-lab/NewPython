# -*- coding: utf-8 -*-
"""
单独同步字典表 T_FIELDENUM + T_FIELDEXPLAIN 到达梦
"""
import oracledb
import dmPython
from datetime import datetime
import time

ORACLE_CONFIG = {
    "user": "highway_exchange",
    "password": "qrwl",
    "dsn": "192.168.1.99/orcl",
}
DM_CONFIG = {
    "user": "NEWPYTHON",
    "password": "NewPython@2025",
    "server": "192.168.1.99",
    "port": 5236,
}
ORACLE_CLIENT_PATH = r"E:\workfile\JAVA\NewAPI\oracle_client"

MIGRATE_TABLES = [
    {"oracle_schema": "PLATFORM_DICTIONARY", "table": "T_FIELDEXPLAIN", "sequence": "SEQ_FIELDEXPLAIN"},
    {"oracle_schema": "PLATFORM_DICTIONARY", "table": "T_FIELDENUM", "sequence": "SEQ_FIELDENUM"},
]

BATCH_SIZE = 2000


def map_oracle_type_to_dm(data_type, data_length, data_precision, data_scale):
    dt = data_type.upper()
    if dt == "NUMBER":
        if data_scale and data_scale > 0:
            p = data_precision or 38
            return f"DECIMAL({p},{data_scale})"
        elif data_precision:
            if data_precision <= 4:
                return "SMALLINT"
            elif data_precision <= 9:
                return "INT"
            else:
                return f"DECIMAL({data_precision},0)"
        else:
            return "DECIMAL(38,0)"
    elif dt in ("VARCHAR2", "NVARCHAR2"):
        length = data_length or 200
        return f"VARCHAR({length})"
    elif dt == "CHAR":
        length = data_length or 1
        return f"CHAR({length})"
    elif dt == "DATE":
        return "TIMESTAMP"
    elif "TIMESTAMP" in dt:
        return "TIMESTAMP"
    elif dt == "CLOB":
        return "TEXT"
    elif dt == "BLOB":
        return "BLOB"
    else:
        return f"VARCHAR({data_length or 500})"


def _convert_row(row):
    values = []
    for val in row:
        if val is None:
            values.append(None)
        elif isinstance(val, datetime):
            values.append(val.strftime("%Y-%m-%d %H:%M:%S"))
        elif isinstance(val, str):
            # 过滤不可编码字符
            values.append(val.encode('utf-8', errors='replace').decode('utf-8'))
        else:
            values.append(val)
    return values


def migrate_table(oracle_conn, schema, table_name, sequence_name):
    print(f"\n{'=' * 60}")
    print(f"  迁移表: {schema}.{table_name}")
    print(f"{'=' * 60}")

    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    table_exists = False
    existing_count = 0
    try:
        dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        existing_count = dm_cur.fetchone()[0]
        table_exists = True
        print(f"  已存在 {existing_count} 条数据，将自动合并差异")
    except:
        print(f"  表不存在，将新建并导入数据")
    dm_cur.close()
    dm_conn.close()

    # 读取 Oracle 表结构
    print(f"\n[1] 读取 Oracle 表结构...")
    ora_cur = oracle_conn.cursor()
    ora_cur.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE
        FROM ALL_TAB_COLUMNS
        WHERE OWNER = '{schema}' AND TABLE_NAME = '{table_name}'
        ORDER BY COLUMN_ID
    """)
    columns = []
    for row in ora_cur.fetchall():
        col = {
            "name": row[0],
            "oracle_type": row[1],
            "data_length": row[2],
            "data_precision": row[3],
            "data_scale": row[4],
            "nullable": row[5] == "Y",
            "dm_type": map_oracle_type_to_dm(row[1], row[2], row[3], row[4]),
        }
        columns.append(col)
        print(f"  {col['name']:35s} {col['oracle_type']:15s} -> {col['dm_type']}")
    ora_cur.close()
    print(f"  共 {len(columns)} 个字段")

    if not columns:
        print(f"  无法读取表结构，跳过")
        return False

    # 建表
    if table_exists:
        print(f"\n[2] 表已存在，跳过建表")
    else:
        print(f"\n[2] 在达梦中创建表...")
        dm_conn = dmPython.connect(**DM_CONFIG)
        dm_cur = dm_conn.cursor()
        try:
            pk_col = columns[0]["name"]
            col_defs = []
            for col in columns:
                nullable = "" if col["nullable"] else " NOT NULL"
                col_defs.append(f"    {col['name']} {col['dm_type']}{nullable}")
            create_sql = (
                f"CREATE TABLE {table_name} (\n"
                + ",\n".join(col_defs)
                + f",\n    PRIMARY KEY ({pk_col})\n)"
            )
            dm_cur.execute(create_sql)
            print(f"  创建表成功（{len(columns)} 个字段）")
            dm_conn.commit()

            # 同步注释
            print(f"\n  同步注释...")
            ora_cur2 = oracle_conn.cursor()
            ora_cur2.execute(f"""
                SELECT COMMENTS FROM ALL_TAB_COMMENTS
                WHERE OWNER = '{schema}' AND TABLE_NAME = '{table_name}'
            """)
            tab_comment = ora_cur2.fetchone()
            if tab_comment and tab_comment[0]:
                comment_text = tab_comment[0].replace("'", "''")
                dm_cur.execute(f"COMMENT ON TABLE {table_name} IS '{comment_text}'")
                print(f"  表注释: {tab_comment[0]}")

            ora_cur2.execute(f"""
                SELECT COLUMN_NAME, COMMENTS FROM ALL_COL_COMMENTS
                WHERE OWNER = '{schema}' AND TABLE_NAME = '{table_name}' AND COMMENTS IS NOT NULL
            """)
            col_comment_count = 0
            for col_row in ora_cur2.fetchall():
                try:
                    comment_text = col_row[1].replace("'", "''")
                    dm_cur.execute(f"COMMENT ON COLUMN {table_name}.{col_row[0]} IS '{comment_text}'")
                    col_comment_count += 1
                except Exception:
                    pass
            dm_conn.commit()
            ora_cur2.close()
            print(f"  字段注释: {col_comment_count} 个同步成功")
        finally:
            dm_cur.close()
            dm_conn.close()

    # 迁移数据
    print(f"\n[3] 迁移数据...")
    ora_cur = oracle_conn.cursor()
    col_names = [c["name"] for c in columns]
    ora_cur.execute(f"SELECT {','.join(col_names)} FROM {schema}.{table_name}")
    rows = ora_cur.fetchall()
    total = len(rows)
    print(f"  Oracle 源表数据: {total} 条")

    if total == 0:
        print(f"  源表无数据，跳过")
        ora_cur.close()
        return True

    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()

    pk_col = columns[0]["name"]
    if table_exists:
        src_cols = ",".join([f"? AS {c}" for c in col_names])
        on_clause = f"T.{pk_col} = S.{pk_col}"
        update_parts = ",".join([f"T.{c} = S.{c}" for c in col_names if c != pk_col])
        insert_cols = ",".join(col_names)
        insert_vals = ",".join([f"S.{c}" for c in col_names])
        exec_sql = (
            f"MERGE INTO {table_name} T "
            f"USING (SELECT {src_cols} FROM DUAL) S "
            f"ON ({on_clause}) "
            f"WHEN MATCHED THEN UPDATE SET {update_parts} "
            f"WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals})"
        )
        mode_label = "MERGE INTO"
    else:
        placeholders = ",".join(["?" for _ in columns])
        exec_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"
        mode_label = "INSERT"
    print(f"  模式: {mode_label}，批量大小: {BATCH_SIZE}")

    start_time = time.time()
    migrated = 0
    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        batch_values = [_convert_row(row) for row in batch]
        dm_cur.executemany(exec_sql, batch_values)
        dm_conn.commit()
        migrated += len(batch)
        elapsed = time.time() - start_time
        speed = migrated / elapsed if elapsed > 0 else 0
        print(f"  已迁移: {migrated}/{total} 条 ({speed:.0f}条/秒)")

    dm_cur.close()
    dm_conn.close()
    ora_cur.close()
    elapsed = time.time() - start_time
    print(f"  数据迁移完成: {migrated} 条，耗时 {elapsed:.1f} 秒")

    # 校验
    print(f"\n[4] 数据校验...")
    try:
        ora_verify = oracledb.connect(**ORACLE_CONFIG)
        ora_cur = ora_verify.cursor()
        ora_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}")
        ora_count = ora_cur.fetchone()[0]
        ora_cur.close()
        ora_verify.close()
    except Exception as e:
        print(f"  Oracle 校验连接失败: {e}")
        ora_count = -1

    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    dm_count = dm_cur.fetchone()[0]
    dm_cur.close()
    dm_conn.close()

    if ora_count < 0:
        print(f"  达梦: {dm_count} 条（Oracle 校验跳过）")
        return True

    print(f"  Oracle: {ora_count} 条")
    print(f"  达梦:   {dm_count} 条")
    match = ora_count == dm_count
    print(f"  {'✅ 行数一致' if match else '❌ 行数不一致！差异: ' + str(ora_count - dm_count)}")
    return match


def main():
    print("\n" + "=" * 60)
    print("  字典表同步: PLATFORM_DICTIONARY -> 达梦 NEWPYTHON")
    print("=" * 60)

    print(f"\n初始化 Oracle Client: {ORACLE_CLIENT_PATH}")
    try:
        oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
        print("  Oracle Client 初始化成功")
    except Exception as e:
        print(f"  Oracle Client 初始化: {e}")

    print("\n连接 Oracle...")
    oracle_conn = oracledb.connect(**ORACLE_CONFIG)
    print("  Oracle 连接成功")

    results = []
    for table_cfg in MIGRATE_TABLES:
        success = migrate_table(
            oracle_conn,
            table_cfg["oracle_schema"],
            table_cfg["table"],
            table_cfg["sequence"],
        )
        results.append((table_cfg["table"], success))

    oracle_conn.close()

    print(f"\n{'=' * 60}")
    print("  迁移结果汇总")
    print(f"{'=' * 60}")
    for table, success in results:
        status = "成功" if success else "失败"
        print(f"  {table:30s} {status}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
