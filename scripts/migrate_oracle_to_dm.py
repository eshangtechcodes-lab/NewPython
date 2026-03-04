# -*- coding: utf-8 -*-
"""
Oracle → 达梦数据迁移脚本
先迁移 COOP_MERCHANT.T_BRAND 表作为 PoC 验证
"""
import oracledb
import dmPython
from datetime import datetime

# === 连接配置 ===
ORACLE_CONFIG = {
    "user": "highway_exchange",
    "password": "qrwl",
    "dsn": "127.0.0.1/orcl",
}

DM_CONFIG = {
    "user": "DMNEW",
    "password": "Dmnew@2025Aa",
    "server": "127.0.0.1",
    "port": 5236,
}

# 达梦新用户（与其他表分开）
DM_NEW_USER = "NEWPYTHON"
DM_NEW_PASSWORD = "NewPython@2025"

# 要迁移的表
MIGRATE_TABLES = [
    {"oracle_schema": "COOP_MERCHANT", "table": "T_BRAND", "sequence": "SEQ_BRAND"},
]

# Oracle → 达梦类型映射
def map_oracle_type_to_dm(data_type, data_length, data_precision, data_scale):
    """Oracle 数据类型转达梦"""
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


def step_1_verify_dm_user():
    """步骤1: 验证达梦用户 NEWPYTHON 连接"""
    print("=" * 60)
    print(f"步骤1: 验证达梦用户 {DM_NEW_USER}")
    try:
        conn = dmPython.connect(
            user=DM_NEW_USER, password=DM_NEW_PASSWORD,
            server=DM_CONFIG["server"], port=DM_CONFIG["port"]
        )
        conn.close()
        print(f"  ✅ 用户 {DM_NEW_USER} 连接成功")
    except Exception as ex:
        print(f"  ❌ 用户 {DM_NEW_USER} 连接失败: {ex}")
        raise


def step_2_read_oracle_structure(oracle_conn, schema, table_name):
    """步骤2: 读取 Oracle 表结构"""
    print("=" * 60)
    print(f"步骤2: 读取 Oracle 表结构 {schema}.{table_name}")
    cur = oracle_conn.cursor()
    cur.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE
        FROM ALL_TAB_COLUMNS
        WHERE OWNER = '{schema}' AND TABLE_NAME = '{table_name}'
        ORDER BY COLUMN_ID
    """)
    columns = []
    for row in cur.fetchall():
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
        print(f"  {col['name']:30s} {col['oracle_type']:15s} → {col['dm_type']}")
    cur.close()
    print(f"  共 {len(columns)} 个字段")
    return columns


def step_3_create_dm_table(columns, table_name, sequence_name):
    """步骤3: 在达梦中创建对应表"""
    print("=" * 60)
    print(f"步骤3: 在达梦中创建表 {DM_NEW_USER}.{table_name}")
    conn = dmPython.connect(
        user=DM_NEW_USER, password=DM_NEW_PASSWORD,
        server=DM_CONFIG["server"], port=DM_CONFIG["port"]
    )
    cur = conn.cursor()
    try:
        # 删除旧表
        try:
            cur.execute(f"DROP TABLE {table_name}")
            print(f"  已删除旧表 {table_name}")
        except:
            pass
        # 删除旧序列
        try:
            cur.execute(f"DROP SEQUENCE {sequence_name}")
            print(f"  已删除旧序列 {sequence_name}")
        except:
            pass
        conn.commit()

        # 构建建表 SQL
        col_defs = []
        pk_col = columns[0]["name"]  # 假设第一列为主键
        for col in columns:
            nullable = "" if col["nullable"] else " NOT NULL"
            col_defs.append(f"    {col['name']} {col['dm_type']}{nullable}")

        create_sql = f"CREATE TABLE {table_name} (\n"
        create_sql += ",\n".join(col_defs)
        create_sql += f",\n    PRIMARY KEY ({pk_col})"
        create_sql += "\n)"
        cur.execute(create_sql)
        print(f"  ✅ 创建表 {table_name} 成功（{len(columns)} 个字段）")

        # 创建序列
        cur.execute(f"CREATE SEQUENCE {sequence_name} START WITH 1 INCREMENT BY 1")
        print(f"  ✅ 创建序列 {sequence_name} 成功")

        conn.commit()
    finally:
        cur.close()
        conn.close()


def step_4_migrate_data(oracle_conn, schema, table_name, columns):
    """步骤4: 迁移数据"""
    print("=" * 60)
    print(f"步骤4: 迁移数据 {schema}.{table_name}")

    # 从 Oracle 读取全量数据
    ora_cur = oracle_conn.cursor()
    col_names = [c["name"] for c in columns]
    ora_cur.execute(f"SELECT {','.join(col_names)} FROM {schema}.{table_name}")
    rows = ora_cur.fetchall()
    total = len(rows)
    print(f"  Oracle 源表数据: {total} 条")

    if total == 0:
        print("  ⚠️ 源表无数据，跳过迁移")
        ora_cur.close()
        return 0

    # 写入达梦
    dm_conn = dmPython.connect(
        user=DM_NEW_USER, password=DM_NEW_PASSWORD,
        server=DM_CONFIG["server"], port=DM_CONFIG["port"]
    )
    dm_cur = dm_conn.cursor()

    # 构建参数化 INSERT
    placeholders = ",".join(["?" for _ in columns])
    insert_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"

    batch_size = 500
    migrated = 0
    for i in range(0, total, batch_size):
        batch = rows[i:i + batch_size]
        for row in batch:
            # 处理数据类型转换
            values = []
            for j, val in enumerate(row):
                if val is None:
                    values.append(None)
                elif isinstance(val, datetime):
                    values.append(val.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    values.append(val)
            dm_cur.execute(insert_sql, values)
        dm_conn.commit()
        migrated += len(batch)
        print(f"  已迁移: {migrated}/{total} 条")

    dm_cur.close()
    dm_conn.close()
    ora_cur.close()
    print(f"  ✅ 数据迁移完成: {migrated} 条")
    return migrated


def step_5_verify(oracle_conn, schema, table_name, columns):
    """步骤5: 数据校验"""
    print("=" * 60)
    print(f"步骤5: 数据校验 {table_name}")

    # Oracle 行数
    ora_cur = oracle_conn.cursor()
    ora_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}")
    ora_count = ora_cur.fetchone()[0]

    # 达梦行数
    dm_conn = dmPython.connect(
        user=DM_NEW_USER, password=DM_NEW_PASSWORD,
        server=DM_CONFIG["server"], port=DM_CONFIG["port"]
    )
    dm_cur = dm_conn.cursor()
    dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    dm_count = dm_cur.fetchone()[0]

    print(f"  Oracle 行数: {ora_count}")
    print(f"  达梦 行数:   {dm_count}")

    if ora_count == dm_count:
        print(f"  ✅ 行数一致")
    else:
        print(f"  ❌ 行数不一致！差异: {ora_count - dm_count}")

    # 抽样比对前5条
    pk = columns[0]["name"]
    ora_cur.execute(f"SELECT * FROM {schema}.{table_name} WHERE ROWNUM <= 5 ORDER BY {pk}")
    ora_sample = ora_cur.fetchall()
    dm_cur.execute(f"SELECT * FROM {table_name} ORDER BY {pk} FETCH FIRST 5 ROWS ONLY")
    dm_sample = dm_cur.fetchall()

    print(f"  抽样比对（前5条主键值）:")
    for i, (o, d) in enumerate(zip(ora_sample, dm_sample)):
        match = "✅" if str(o[0]) == str(d[0]) else "❌"
        print(f"    {match} Oracle={o[0]}, 达梦={d[0]}")

    ora_cur.close()
    dm_cur.close()
    dm_conn.close()
    oracle_conn.close()


def main():
    print("\n" + "=" * 60)
    print("  Oracle → 达梦 数据迁移工具")
    print("=" * 60 + "\n")

    # 步骤1: 创建达梦用户
    step_1_verify_dm_user()
    print()

    # 连接 Oracle
    print("连接 Oracle...")
    oracle_conn = oracledb.connect(**ORACLE_CONFIG)
    print("  ✅ Oracle 连接成功\n")

    # 逐表迁移
    for table_cfg in MIGRATE_TABLES:
        schema = table_cfg["oracle_schema"]
        table = table_cfg["table"]
        seq = table_cfg["sequence"]

        # 步骤2: 读取表结构
        columns = step_2_read_oracle_structure(oracle_conn, schema, table)
        print()

        # 步骤3: 达梦建表
        step_3_create_dm_table(columns, table, seq)
        print()

        # 步骤4: 数据迁移
        step_4_migrate_data(oracle_conn, schema, table, columns)
        print()

        # 步骤5: 校验
        # 需要重新连接 Oracle（之前的游标可能已关闭）
        oracle_conn2 = oracledb.connect(**ORACLE_CONFIG)
        step_5_verify(oracle_conn2, schema, table, columns)
        print()

    print("=" * 60)
    print("  迁移完成！")
    print(f"  达梦用户: {DM_NEW_USER} / {DM_NEW_PASSWORD}")
    print("=" * 60)


if __name__ == "__main__":
    main()
