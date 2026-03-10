# -*- coding: utf-8 -*-
"""
Video 模块数据表迁移脚本
Oracle → 达梦：T_EXTRANET, T_EXTRANETDETAIL, T_SHOPVIDEO, T_VIDEOLOG
同时处理 V_SHOPVIDEO 视图
"""
import oracledb
import dmPython
from datetime import datetime

# === 连接配置 ===
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

# 要迁移的表（Video 模块相关）
MIGRATE_TABLES = [
    {"oracle_schema": "HIGHWAY_EXCHANGE", "table": "T_EXTRANET", "sequence": "SEQ_EXTRANET"},
    {"oracle_schema": "HIGHWAY_EXCHANGE", "table": "T_EXTRANETDETAIL", "sequence": "SEQ_EXTRANETDETAIL"},
    {"oracle_schema": "HIGHWAY_EXCHANGE", "table": "T_SHOPVIDEO", "sequence": "SEQ_SHOPVIDEO"},
    {"oracle_schema": "HIGHWAY_EXCHANGE", "table": "T_VIDEOLOG", "sequence": "SEQ_VIDEOLOG"},
]


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


def migrate_table(oracle_conn, schema, table_name, sequence_name):
    """迁移单张表：读结构 → 建表 → 迁移数据 → 校验"""
    print(f"\n{'=' * 60}")
    print(f"  迁移表: {schema}.{table_name}")
    print(f"{'=' * 60}")

    # 检查达梦中是否已存在该表且有数据
    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    try:
        dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        existing_count = dm_cur.fetchone()[0]
        if existing_count > 0:
            print(f"  ⚠️ 表 {table_name} 已存在且有 {existing_count} 条数据，跳过迁移")
            dm_cur.close()
            dm_conn.close()
            return
    except:
        pass  # 表不存在，继续迁移
    dm_cur.close()
    dm_conn.close()

    # 步骤1：读取 Oracle 表结构
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
        print(f"  {col['name']:35s} {col['oracle_type']:15s} → {col['dm_type']}")
    ora_cur.close()
    print(f"  共 {len(columns)} 个字段")

    if not columns:
        print(f"  ❌ 无法读取表结构，跳过")
        return

    # 步骤2：在达梦中创建表
    print(f"\n[2] 在达梦中创建表...")
    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    try:
        try:
            dm_cur.execute(f"DROP TABLE {table_name}")
            print(f"  已删除旧表")
        except:
            pass
        try:
            dm_cur.execute(f"DROP SEQUENCE {sequence_name}")
            print(f"  已删除旧序列")
        except:
            pass
        dm_conn.commit()

        pk_col = columns[0]["name"]
        col_defs = []
        for col in columns:
            nullable = "" if col["nullable"] else " NOT NULL"
            col_defs.append(f"    {col['name']} {col['dm_type']}{nullable}")
        create_sql = f"CREATE TABLE {table_name} (\n" + ",\n".join(col_defs) + f",\n    PRIMARY KEY ({pk_col})\n)"
        dm_cur.execute(create_sql)
        print(f"  ✅ 创建表成功（{len(columns)} 个字段）")

        dm_cur.execute(f"CREATE SEQUENCE {sequence_name} START WITH 1 INCREMENT BY 1")
        print(f"  ✅ 创建序列成功")
        dm_conn.commit()
    finally:
        dm_cur.close()
        dm_conn.close()

    # 步骤3：迁移数据
    print(f"\n[3] 迁移数据...")
    ora_cur = oracle_conn.cursor()
    col_names = [c["name"] for c in columns]
    ora_cur.execute(f"SELECT {','.join(col_names)} FROM {schema}.{table_name}")
    rows = ora_cur.fetchall()
    total = len(rows)
    print(f"  Oracle 源表数据: {total} 条")

    if total == 0:
        print(f"  ⚠️ 源表无数据，跳过")
        ora_cur.close()
        return

    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    placeholders = ",".join(["?" for _ in columns])
    insert_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"

    batch_size = 500
    migrated = 0
    for i in range(0, total, batch_size):
        batch = rows[i:i + batch_size]
        for row in batch:
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

    # 步骤4：校验
    print(f"\n[4] 数据校验...")
    ora_cur = oracle_conn.cursor()
    ora_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}")
    ora_count = ora_cur.fetchone()[0]

    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    dm_count = dm_cur.fetchone()[0]

    print(f"  Oracle: {ora_count} 条")
    print(f"  达梦:   {dm_count} 条")
    if ora_count == dm_count:
        print(f"  ✅ 行数一致")
    else:
        print(f"  ❌ 行数不一致！差异: {ora_count - dm_count}")

    # 更新序列到最大 ID
    dm_cur.execute(f"SELECT MAX({columns[0]['name']}) FROM {table_name}")
    max_id = dm_cur.fetchone()[0]
    if max_id:
        try:
            dm_cur.execute(f"DROP SEQUENCE {sequence_name}")
            dm_cur.execute(f"CREATE SEQUENCE {sequence_name} START WITH {int(max_id) + 1} INCREMENT BY 1")
            dm_conn.commit()
            print(f"  ✅ 序列重置为 {int(max_id) + 1}")
        except Exception as e:
            print(f"  ⚠️ 序列重置失败: {e}")

    ora_cur.close()
    dm_cur.close()
    dm_conn.close()


def migrate_view(oracle_conn):
    """迁移 V_SHOPVIDEO 视图定义"""
    print(f"\n{'=' * 60}")
    print(f"  迁移视图: V_SHOPVIDEO")
    print(f"{'=' * 60}")

    # 先读取 Oracle 视图定义
    ora_cur = oracle_conn.cursor()
    ora_cur.execute("""
        SELECT TEXT FROM ALL_VIEWS WHERE OWNER = 'HIGHWAY_EXCHANGE' AND VIEW_NAME = 'V_SHOPVIDEO'
    """)
    row = ora_cur.fetchone()
    ora_cur.close()

    if not row:
        print("  ⚠️ Oracle 中未找到 V_SHOPVIDEO 视图，尝试用 JOIN 方式创建...")
        # 根据 C# 代码中对 V_SHOPVIDEO 的使用，手动构建视图
        view_sql = """
CREATE OR REPLACE VIEW V_SHOPVIDEO AS
SELECT
    S.SHOPVIDEO_ID, S.EXTRANETDETAIL_ID, S.SERVERPARTCODE, S.SHOPCODE,
    S.MACHINENAME, S.MACHINE_IP, S.VIDEO_IP, S.VIDEOPORT AS SV_VIDEOPORT,
    S.CHANEL_NAME, S.SHOPVIDEO_DESC,
    D.EXTRANET_ID, D.EQUIPMENT_TYPE, D.VEDIO_TYPE,
    D.VIDEOIP, D.VIDEO_PUBLICIP, D.VIDEO_INTRANETIP,
    D.VIDEOPORT, D.LOGUSERNAME, D.LOGPASSWORD, D.LOGINPORT,
    E.EXTRANET_IP
FROM T_SHOPVIDEO S
LEFT JOIN T_EXTRANETDETAIL D ON S.EXTRANETDETAIL_ID = D.EXTRANETDETAIL_ID
LEFT JOIN T_EXTRANET E ON D.EXTRANET_ID = E.EXTRANET_ID
"""
    else:
        view_text = row[0] if isinstance(row[0], str) else row[0].read()
        print(f"  Oracle 视图定义:\n{view_text[:500]}...")
        view_sql = f"CREATE OR REPLACE VIEW V_SHOPVIDEO AS {view_text}"

    # 在达梦中创建视图
    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    try:
        dm_cur.execute(view_sql)
        dm_conn.commit()
        print(f"  ✅ 视图创建成功")

        # 验证视图可查询
        dm_cur.execute("SELECT COUNT(*) FROM V_SHOPVIDEO")
        cnt = dm_cur.fetchone()[0]
        print(f"  ✅ 视图可查询，当前 {cnt} 条数据")
    except Exception as e:
        print(f"  ❌ 视图创建失败: {e}")
    finally:
        dm_cur.close()
        dm_conn.close()


def main():
    print("\n" + "=" * 60)
    print("  Video 模块 Oracle → 达梦 数据迁移")
    print("=" * 60)

    # 连接 Oracle（thin 模式）
    print("\n连接 Oracle（thin 模式）...")
    oracle_conn = oracledb.connect(**ORACLE_CONFIG)
    print("  ✅ Oracle 连接成功")

    # 逐表迁移
    for table_cfg in MIGRATE_TABLES:
        migrate_table(
            oracle_conn,
            table_cfg["oracle_schema"],
            table_cfg["table"],
            table_cfg["sequence"],
        )

    # 迁移视图
    migrate_view(oracle_conn)

    oracle_conn.close()
    print(f"\n{'=' * 60}")
    print("  Video 模块迁移完成！")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
