# -*- coding: utf-8 -*-
"""
从 Oracle 批量同步表结构和数据到 Dameng（NEWPYTHON schema）
- 使用 oracledb Thin 模式连接 Oracle
- 多 Oracle schema 访问（通过同一个有 DBA 权限的账户或 synonym）
- 自动创建表结构、复制字段注释、批量导入数据
"""
import oracledb
import dmPython
import json

# 使用本地 Oracle 11g 的 OCI 库进行 Thick 模式连接
ORA_CLIENT_DIR = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"
try:
    oracledb.init_oracle_client(lib_dir=ORA_CLIENT_DIR)
    print(f"Oracle Thick 模式初始化成功: {ORA_CLIENT_DIR}")
except Exception as ex:
    print(f"Oracle Thick 模式初始化: {ex}")
import os
import sys
from datetime import datetime

# Oracle 连接信息 — 所有 schema 密码统一为 qrwl
ORA_SCHEMAS_USERS = {
    "HIGHWAY_STORAGE": ("highway_storage", "qrwl"),
    "HIGHWAY_SELLDATA": ("highway_selldata", "qrwl"),
    "HIGHWAY_EXCHANGE": ("highway_exchange", "qrwl"),
    "CONTRACT_STORAGE": ("contract_storage", "qrwl"),
    "PLATFORM_DASHBOARD": ("platform_dashboard", "qrwl"),
    "PLATFORM_FRAMEWORK": ("platform_framework", "qrwl"),
    "MOBILESERVICE_PLATFORM": ("mobileservice_platform", "qrwl"),
    "FINANCE_STORAGE": ("finance_storage", "qrwl"),
    "WORKFLOW_SUPPORT": ("workflow_support", "qrwl"),
    "SELLER_STORAGE": ("seller_storage", "qrwl"),
    "COOP_MERCHANT": ("coop_merchant", "qrwl"),
}
ORA_DSN = "127.0.0.1:1521/orcl"

# Dameng 连接信息
DM_USER = "NEWPYTHON"
DM_PASS = "NewPython@2025"
DM_HOST = "127.0.0.1"
DM_PORT = 5236

# Dameng 已有表
DM_EXISTING = set()

# Oracle 类型 → Dameng 类型映射
TYPE_MAP = {
    "VARCHAR2": "VARCHAR",
    "NVARCHAR2": "VARCHAR",
    "CHAR": "CHAR",
    "NCHAR": "CHAR",
    "NUMBER": "DECIMAL",
    "FLOAT": "DOUBLE",
    "DATE": "TIMESTAMP",
    "TIMESTAMP(6)": "TIMESTAMP",
    "TIMESTAMP(3)": "TIMESTAMP",
    "CLOB": "CLOB",
    "NCLOB": "CLOB",
    "BLOB": "BLOB",
    "RAW": "VARBINARY",
    "LONG": "CLOB",
}

# 需要同步的目标表（按 Controller 优先级排序）
TABLES_BY_SCHEMA = {}

# 统计
stats = {"created": 0, "data_synced": 0, "skipped": 0, "errors": [], "total_rows": 0}


def get_dm_connection():
    return dmPython.connect(user=DM_USER, password=DM_PASS, server=DM_HOST, port=DM_PORT, autoCommit=True)


def get_dm_existing_tables():
    """获取 Dameng 中已存在的表"""
    conn = get_dm_connection()
    cur = conn.cursor()
    cur.execute("SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = 'NEWPYTHON'")
    tables = set(row[0] for row in cur.fetchall())
    cur.close()
    conn.close()
    return tables


def get_oracle_table_structure(ora_conn, table_name):
    """获取 Oracle 表结构"""
    cur = ora_conn.cursor()
    cur.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE
        FROM USER_TAB_COLUMNS
        WHERE TABLE_NAME = '{table_name}'
        ORDER BY COLUMN_ID
    """)
    columns = cur.fetchall()
    cur.close()
    return columns


def get_oracle_table_comments(ora_conn, table_name):
    """获取表注释和字段注释"""
    cur = ora_conn.cursor()
    # 表注释
    cur.execute(f"SELECT COMMENTS FROM USER_TAB_COMMENTS WHERE TABLE_NAME = '{table_name}'")
    row = cur.fetchone()
    table_comment = row[0] if row and row[0] else ""

    # 字段注释
    cur.execute(f"SELECT COLUMN_NAME, COMMENTS FROM USER_COL_COMMENTS WHERE TABLE_NAME = '{table_name}'")
    col_comments = {r[0]: r[1] for r in cur.fetchall() if r[1]}
    cur.close()
    return table_comment, col_comments


def map_column_type(data_type, data_length, data_precision, data_scale):
    """Oracle 列类型映射为 Dameng 类型"""
    dt = data_type.upper()

    if dt in ("VARCHAR2", "NVARCHAR2"):
        length = max(data_length or 50, 1)
        return f"VARCHAR({length})"
    elif dt in ("CHAR", "NCHAR"):
        length = max(data_length or 1, 1)
        return f"CHAR({length})"
    elif dt == "NUMBER":
        if data_precision and data_scale and data_scale > 0:
            return f"DECIMAL({data_precision},{data_scale})"
        elif data_precision:
            if data_precision <= 5:
                return "SMALLINT"
            elif data_precision <= 10:
                return "INT"
            elif data_precision <= 19:
                return "BIGINT"
            else:
                return f"DECIMAL({data_precision})"
        else:
            return "DECIMAL(38,6)"
    elif dt == "FLOAT":
        return "DOUBLE"
    elif dt in ("DATE", "TIMESTAMP(6)", "TIMESTAMP(3)", "TIMESTAMP(0)"):
        return "TIMESTAMP"
    elif dt.startswith("TIMESTAMP"):
        return "TIMESTAMP"
    elif dt in ("CLOB", "NCLOB", "LONG"):
        return "CLOB"
    elif dt == "BLOB":
        return "BLOB"
    elif dt == "RAW":
        length = max(data_length or 16, 1)
        return f"VARBINARY({length})"
    else:
        return f"VARCHAR(4000)"


def create_table_in_dm(dm_conn, table_name, columns, table_comment, col_comments):
    """在 Dameng 中创建表"""
    cur = dm_conn.cursor()

    col_defs = []
    for col in columns:
        col_name, data_type, data_length, data_precision, data_scale, nullable = col
        dm_type = map_column_type(data_type, data_length, data_precision, data_scale)
        null_str = "" if nullable == "Y" else " NOT NULL"
        col_defs.append(f'    "{col_name}" {dm_type}{null_str}')

    ddl = f'CREATE TABLE "{table_name}" (\n' + ",\n".join(col_defs) + "\n)"
    try:
        cur.execute(ddl)
        print(f"    ✅ 表创建成功: {table_name}")
    except Exception as ex:
        if "已存在" in str(ex) or "already exists" in str(ex).lower():
            print(f"    ⏭️ 表已存在: {table_name}")
            cur.close()
            return False
        else:
            print(f"    ❌ 建表失败: {table_name} - {ex}")
            print(f"       DDL: {ddl[:200]}")
            stats["errors"].append(f"建表失败 {table_name}: {ex}")
            cur.close()
            return False

    # 添加表注释
    if table_comment:
        try:
            cur.execute(f"COMMENT ON TABLE \"{table_name}\" IS '{table_comment.replace(chr(39), chr(39)+chr(39))}'")
        except:
            pass

    # 添加字段注释
    for col_name, comment in col_comments.items():
        if comment:
            try:
                safe_comment = comment.replace("'", "''").replace('\n', ' ').replace('\r', '')
                cur.execute(f"COMMENT ON COLUMN \"{table_name}\".\"{col_name}\" IS '{safe_comment}'")
            except:
                pass

    cur.close()
    return True


def sync_table_data(ora_conn, dm_conn, table_name, batch_size=500, max_rows=5000):
    """从 Oracle 同步数据到 Dameng（限制行数避免过慢）"""
    ora_cur = ora_conn.cursor()
    dm_cur = dm_conn.cursor()

    try:
        # 获取行数
        ora_cur.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
        total = ora_cur.fetchone()[0]
        if total == 0:
            print(f"    ⓘ 表无数据: {table_name}")
            return 0

        actual_rows = min(total, max_rows)
        print(f"    📊 数据量: {total} 行" + (f" (只同步前{max_rows}行)" if total > max_rows else ""))

        # 读取数据（限制行数）
        ora_cur.execute(f"SELECT * FROM \"{table_name}\" WHERE ROWNUM <= {max_rows}")
        columns = [desc[0] for desc in ora_cur.description]
        col_list = ", ".join(f'"{c}"' for c in columns)
        placeholders = ", ".join(["?" for _ in columns])
        insert_sql = f'INSERT INTO "{table_name}" ({col_list}) VALUES ({placeholders})'

        synced = 0
        while True:
            rows = ora_cur.fetchmany(batch_size)
            if not rows:
                break
            # 转换数据类型
            clean_rows = []
            for row in rows:
                clean_row = []
                for val in row:
                    if isinstance(val, oracledb.LOB):
                        clean_row.append(val.read() if val else None)
                    else:
                        clean_row.append(val)
                clean_rows.append(tuple(clean_row))
            try:
                dm_cur.executemany(insert_sql, clean_rows)
                dm_conn.commit()
                synced += len(clean_rows)
            except Exception as ex:
                # 尝试逐行插入
                for r in clean_rows:
                    try:
                        dm_cur.execute(insert_sql, r)
                        dm_conn.commit()
                        synced += 1
                    except:
                        pass

        print(f"    ✅ 同步 {synced}/{actual_rows} 行")
        return synced
    except Exception as ex:
        print(f"    ❌ 数据同步失败: {ex}")
        stats["errors"].append(f"数据同步失败 {table_name}: {ex}")
        return 0
    finally:
        ora_cur.close()
        dm_cur.close()


def sync_schema_tables(schema_name, user, password, table_list):
    """同步某个 schema 下的所有目标表"""
    print(f"\n{'='*60}")
    print(f"同步 Schema: {schema_name}")
    print(f"{'='*60}")

    # 连接 Oracle
    try:
        ora_conn = oracledb.connect(user=user, password=password, dsn=ORA_DSN)
        print(f"  Oracle 连接成功 ({user}@{ORA_DSN})")
    except Exception as ex:
        print(f"  ❌ Oracle 连接失败 ({user}): {ex}")
        for t in table_list:
            stats["errors"].append(f"Oracle连接失败 {schema_name}.{t}: {ex}")
            stats["skipped"] += 1
        return

    # 连接 Dameng
    dm_conn = get_dm_connection()

    for table_name in table_list:
        print(f"\n  [{table_name}]")
        if table_name in DM_EXISTING:
            print(f"    ⏭️ Dameng 已存在")
            stats["skipped"] += 1
            continue

        # 获取表结构
        try:
            columns = get_oracle_table_structure(ora_conn, table_name)
            if not columns:
                print(f"    ⚠️ Oracle 中表不存在或无列: {table_name}")
                stats["errors"].append(f"Oracle中不存在 {schema_name}.{table_name}")
                stats["skipped"] += 1
                continue
        except Exception as ex:
            print(f"    ❌ 获取结构失败: {ex}")
            stats["errors"].append(f"获取结构失败 {schema_name}.{table_name}: {ex}")
            stats["skipped"] += 1
            continue

        # 获取注释
        table_comment, col_comments = get_oracle_table_comments(ora_conn, table_name)

        # 建表
        created = create_table_in_dm(dm_conn, table_name, columns, table_comment, col_comments)
        if created:
            stats["created"] += 1
            # 同步数据
            rows = sync_table_data(ora_conn, dm_conn, table_name)
            if rows > 0:
                stats["data_synced"] += 1
                stats["total_rows"] += rows
        else:
            stats["skipped"] += 1

    ora_conn.close()
    dm_conn.close()


def main():
    global DM_EXISTING, TABLES_BY_SCHEMA

    print(f"开始同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 获取 Dameng 已有表
    DM_EXISTING = get_dm_existing_tables()
    print(f"Dameng 已有表: {len(DM_EXISTING)} 张")
    for t in sorted(DM_EXISTING):
        print(f"  {t}")

    # 加载目标表列表
    with open("scripts/test_results/table_deps.json", "r", encoding="utf-8") as f:
        deps = json.load(f)

    TABLES_BY_SCHEMA = deps["schema_tables"]

    # 逐个 schema 同步
    for schema_name in sorted(TABLES_BY_SCHEMA.keys()):
        table_list = TABLES_BY_SCHEMA[schema_name]
        if not table_list:
            continue

        if schema_name not in ORA_SCHEMAS_USERS:
            print(f"\n⚠️ 未配置 Oracle 用户: {schema_name}, 跳过 {len(table_list)} 张表")
            for t in table_list:
                stats["skipped"] += 1
            continue

        user, password = ORA_SCHEMAS_USERS[schema_name]
        sync_schema_tables(schema_name, user, password, table_list)

    # 汇总
    print("\n" + "=" * 60)
    print("同步完成汇总")
    print("=" * 60)
    print(f"  新建表: {stats['created']}")
    print(f"  同步数据: {stats['data_synced']} 张表, {stats['total_rows']} 行")
    print(f"  跳过: {stats['skipped']}")
    if stats["errors"]:
        print(f"  错误: {len(stats['errors'])}")
        for e in stats["errors"]:
            print(f"    - {e}")

    # 验证 - 重新统计
    dm_tables = get_dm_existing_tables()
    print(f"\n同步后 Dameng 表数量: {len(dm_tables)} 张")

    # 保存结果
    with open("scripts/test_results/sync_result.json", "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "dm_tables": sorted(dm_tables),
                   "time": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    print(f"结果已保存: scripts/test_results/sync_result.json")


if __name__ == "__main__":
    main()
