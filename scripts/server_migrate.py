# -*- coding: utf-8 -*-
"""
Oracle → 达梦数据迁移脚本
在服务器上执行，利用 Oracle 本地连接完成表同步

用法：
  全量迁移:    python scripts/server_migrate.py
  指定表迁移:  python scripts/server_migrate.py T_SHOPROYALTY
  多表迁移:    python scripts/server_migrate.py T_SHOPROYALTY T_BRAND
  
  注意：指定的表必须先添加到 MIGRATE_TABLES 列表中
"""
import oracledb
import dmPython
from datetime import datetime

# === 连接配置 ===
ORACLE_CONFIG = {
    "user": "highway_exchange",
    "password": "qrwl",
    "dsn": "192.168.1.99/orcl",  # 远程连接（已开放）
}

DM_CONFIG = {
    "user": "NEWPYTHON",
    "password": "NewPython@2025",
    "server": "192.168.1.99",
    "port": 5236,
}

# Oracle Instant Client 路径（本机）
ORACLE_CLIENT_PATH = r"E:\workfile\JAVA\NewAPI\oracle_client"

# 要迁移的表列表（需要新迁移的表，已有的会自动跳过）
MIGRATE_TABLES = [
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SERVERPART", "sequence": "SEQ_SERVERPART"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SERVERPARTSHOP", "sequence": "SEQ_SERVERPARTSHOP"},
    {"oracle_schema": "COOP_MERCHANT", "table": "T_BRAND", "sequence": "SEQ_BRAND"},
    {"oracle_schema": "COOP_MERCHANT", "table": "T_AUTOSTATISTICS", "sequence": "SEQ_AUTOSTATISTICS"},
    {"oracle_schema": "COOP_MERCHANT", "table": "T_COOPMERCHANTS", "sequence": "SEQ_COOPMERCHANTS"},
    {"oracle_schema": "COOP_MERCHANT", "table": "T_RTCOOPMERCHANTS", "sequence": "SEQ_RTCOOPMERCHANTS"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_RTSERVERPARTSHOP", "sequence": "SEQ_RTSERVERPARTSHOP"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SERVERPARTSHOP_LOG", "sequence": "SEQ_SERVERPARTSHOP_LOG"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_CASHWORKER", "sequence": "SEQ_CASHWORKER"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_COMMODITYTYPE", "sequence": "SEQ_COMMODITYTYPE"},
    {"oracle_schema": "COOP_MERCHANT", "table": "T_USERDEFINEDTYPE", "sequence": "SEQ_USERDEFINEDTYPE"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SERVERPARTCRT", "sequence": "SEQ_SERVERPARTCRT"},
    # COMMODITY 在售商品相关
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_COMMODITY", "sequence": "SEQ_COMMODITY"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_RTCOMMODITYBUSINESS", "sequence": "SEQ_RTCOMMODITYBUSINESS"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_COMMODITY_BUSINESS", "sequence": "SEQ_COMMODITY_BUSINESS"},
    # 字典相关
    {"oracle_schema": "PLATFORM_DICTIONARY", "table": "T_FIELDENUM", "sequence": "SEQ_FIELDENUM"},
    {"oracle_schema": "PLATFORM_DICTIONARY", "table": "T_FIELDEXPLAIN", "sequence": "SEQ_FIELDEXPLAIN"},
    # 合同相关 - GetShopReceivables 接口依赖
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_SHOPROYALTY", "sequence": "SEQ_SHOPROYALTY"},
    # 资产操作日志
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_PROPERTYASSETSLOG", "sequence": "SEQ_PROPERTYASSETSLOG"},
    # 物业资产与商户对照
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_PROPERTYSHOP", "sequence": "SEQ_PROPERTYSHOP"},
    # 服务区资产表
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_PROPERTYASSETS", "sequence": "SEQ_PROPERTYASSETS"},
    # BasicConfigController 相关表
    {"oracle_schema": "MOBILESERVICE_PLATFORM", "table": "T_AUTOTYPE", "sequence": "SEQ_AUTOTYPE"},
    {"oracle_schema": "MOBILESERVICE_PLATFORM", "table": "T_OWNERSERVERPART", "sequence": "SEQ_OWNERSERVERPART"},
    {"oracle_schema": "MOBILESERVICE_PLATFORM", "table": "T_OWNERSERVERPARTSHOP", "sequence": "SEQ_OWNERSERVERPARTSHOP"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SPSTATICTYPE", "sequence": "SEQ_SPSTATICTYPE"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SERVERPARTSHOPCRT", "sequence": "SEQ_SERVERPARTSHOPCRT"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SERVERPARTTYPE", "sequence": "SEQ_SERVERPARTTYPE"},
    # ContractController 相关表
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_ATTACHMENT", "sequence": "SEQ_ATTACHMENT"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_CONTRACT_SYN", "sequence": "SEQ_CONTRACT_SYN"},
    # BusinessProjectController 相关表
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_SHOPROYALTYDETAIL", "sequence": "SEQ_SHOPROYALTYDETAIL"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_REVENUECONFIRM", "sequence": "SEQ_REVENUECONFIRM"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_RTPAYMENTRECORD", "sequence": "SEQ_RTPAYMENTRECORD"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_REMARKS", "sequence": "SEQ_REMARKS"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_BUSINESSPAYMENT", "sequence": "SEQ_BUSINESSPAYMENT"},
    {"oracle_schema": "PLATFORM_DASHBOARD", "table": "T_BUSINESSPROJECTSPLIT", "sequence": "SEQ_BUSINESSPROJECTSPLIT"},
    {"oracle_schema": "PLATFORM_DASHBOARD", "table": "T_BIZPSPLITMONTH", "sequence": "SEQ_BIZPSPLITMONTH"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_PROJECTWARNING", "sequence": "SEQ_PROJECTWARNING"},
    {"oracle_schema": "PLATFORM_DASHBOARD", "table": "T_PERIODWARNING", "sequence": "SEQ_PERIODWARNING"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_APPROVED", "sequence": "SEQ_APPROVED"},
    {"oracle_schema": "HIGHWAY_STORAGE", "table": "T_SHOPEXPENSE", "sequence": "SEQ_SHOPEXPENSE"},
    {"oracle_schema": "PLATFORM_DASHBOARD", "table": "T_PROJECTSPLITMONTH", "sequence": "SEQ_PROJECTSPLITMONTH"},
    # ExpensesController 相关表
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_EXPENSESPREPAID", "sequence": "SEQ_EXPENSESPREPAID"},
    {"oracle_schema": "CONTRACT_STORAGE", "table": "T_EXPENSESSEPARATE", "sequence": "SEQ_EXPENSESSEPARATE"},
    # MerchantsController 相关表
    {"oracle_schema": "COOP_MERCHANT", "table": "T_COOPMERCHANTS_LINKER", "sequence": "SEQ_COOPMERCHANTS_LINKER"},
]

# 运行配置
BATCH_SIZE = 2000       # 批量大小（原 500，提升后减少 commit 次数）
# 智能模式：表不存在→CREATE+INSERT，表存在→MERGE INTO 自动合并差异


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


def _convert_row(row):
    """转换单行数据：datetime → 字符串，其余保持原值"""
    values = []
    for val in row:
        if val is None:
            values.append(None)
        elif isinstance(val, datetime):
            values.append(val.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            values.append(val)
    return values


def _build_merge_sql(table_name, col_names, pk_col):
    """构建 MERGE INTO SQL（增量同步用）"""
    placeholders = ",".join(["?" for _ in col_names])
    src_cols = ",".join([f"? AS {c}" for c in col_names])
    on_clause = f"T.{pk_col} = S.{pk_col}"
    update_parts = ",".join([f"T.{c} = S.{c}" for c in col_names if c != pk_col])
    insert_cols = ",".join(col_names)
    insert_vals = ",".join([f"S.{c}" for c in col_names])
    return (
        f"MERGE INTO {table_name} T "
        f"USING (SELECT {src_cols} FROM DUAL) S "
        f"ON ({on_clause}) "
        f"WHEN MATCHED THEN UPDATE SET {update_parts} "
        f"WHEN NOT MATCHED THEN INSERT ({insert_cols}) VALUES ({insert_vals})"
    )


def migrate_table(oracle_conn, schema, table_name, sequence_name):
    """迁移单张表：读结构 → 建表 → 迁移数据 → 校验"""
    print(f"\n{'=' * 60}")
    print(f"  迁移表: {schema}.{table_name}")
    print(f"{'=' * 60}")

    # 检查达梦中表是否已存在数据
    dm_conn = dmPython.connect(**DM_CONFIG)
    dm_cur = dm_conn.cursor()
    table_exists = False
    existing_count = 0
    try:
        dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        existing_count = dm_cur.fetchone()[0]
        table_exists = True
        if existing_count > 0:
            print(f"  已存在 {existing_count} 条数据，将自动合并差异")
        else:
            print(f"  表已存在但无数据，将全量插入")
    except:
        print(f"  表不存在，将新建并导入数据")
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
        print(f"  {col['name']:35s} {col['oracle_type']:15s} -> {col['dm_type']}")
    ora_cur.close()
    print(f"  共 {len(columns)} 个字段")

    if not columns:
        print(f"  无法读取表结构，跳过")
        return False

    # 步骤2：在达梦中创建表（表已存在时跳过）
    if table_exists:
        print(f"\n[2] 表已存在，跳过建表")
    else:
        print(f"\n[2] 在达梦中创建表...")
        dm_conn = dmPython.connect(**DM_CONFIG)
        dm_cur = dm_conn.cursor()
        try:
            try:
                dm_cur.execute(f"DROP TABLE {table_name}")
            except:
                pass
            try:
                dm_cur.execute(f"DROP SEQUENCE {sequence_name}")
            except:
                pass
            dm_conn.commit()

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

            # 序列创建可能因权限不足失败，不影响数据迁移
            try:
                dm_cur.execute(f"CREATE SEQUENCE {sequence_name} START WITH 1 INCREMENT BY 1")
                print(f"  创建序列成功")
                dm_conn.commit()
            except Exception as seq_err:
                print(f"  序列创建跳过（可能无权限）: {seq_err}")
                dm_conn.commit()

            # 从 Oracle 同步表注释和字段注释
            print(f"\n  同步注释...")
            ora_cur2 = oracle_conn.cursor()
            # 表注释
            ora_cur2.execute(f"""
                SELECT COMMENTS FROM ALL_TAB_COMMENTS
                WHERE OWNER = '{schema}' AND TABLE_NAME = '{table_name}'
            """)
            tab_comment = ora_cur2.fetchone()
            if tab_comment and tab_comment[0]:
                comment_text = tab_comment[0].replace("'", "''")
                dm_cur.execute(f"COMMENT ON TABLE {table_name} IS '{comment_text}'")
                print(f"  表注释: {tab_comment[0]}")
            # 字段注释
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

    # 步骤3：迁移数据
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

    # 根据表是否已存在选择 SQL（存在→MERGE，不存在→INSERT）
    pk_col = columns[0]["name"]
    if table_exists:
        exec_sql = _build_merge_sql(table_name, col_names, pk_col)
        mode_label = "MERGE INTO（自动合并差异）"
    else:
        placeholders = ",".join(["?" for _ in columns])
        exec_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"
        mode_label = "INSERT（全量插入）"
    print(f"  模式: {mode_label}，批量大小: {BATCH_SIZE}")

    import time
    start_time = time.time()
    migrated = 0
    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        # 批量转换数据类型
        batch_values = [_convert_row(row) for row in batch]
        # executemany 批量执行（核心提速：一次网络请求处理整批数据）
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

    # 步骤4：校验（重建 Oracle 连接，避免长事务导致 ORA-03113）
    print(f"\n[4] 数据校验...")
    try:
        ora_verify = oracledb.connect(**ORACLE_CONFIG)
        ora_cur = ora_verify.cursor()
        ora_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table_name}")
        ora_count = ora_cur.fetchone()[0]
        ora_cur.close()
        ora_verify.close()
    except Exception as e:
        print(f"  Oracle 校验连接失败: {e}，跳过校验")
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
    import sys

    print("\n" + "=" * 60)
    print("  Oracle -> 达梦 数据迁移")
    print("=" * 60)

    # 支持命令行参数指定表名（只迁移指定的表）
    # 用法: python server_migrate.py T_SHOPROYALTY T_BRAND
    #       不带参数则全量迁移所有表
    target_tables = [t.upper() for t in sys.argv[1:]] if len(sys.argv) > 1 else []

    if target_tables:
        tables_to_migrate = [t for t in MIGRATE_TABLES if t["table"] in target_tables]
        # 检查是否有未在列表中的表名
        known = {t["table"] for t in tables_to_migrate}
        unknown = [t for t in target_tables if t not in known]
        if unknown:
            print(f"\n  ⚠️ 以下表不在 MIGRATE_TABLES 列表中: {', '.join(unknown)}")
            print(f"  请先将表添加到 MIGRATE_TABLES 列表中再执行")
            return
        print(f"\n  指定迁移 {len(tables_to_migrate)} 张表: {', '.join(target_tables)}")
    else:
        tables_to_migrate = MIGRATE_TABLES
        print(f"\n  全量迁移 {len(tables_to_migrate)} 张表")

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
    for table_cfg in tables_to_migrate:
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
