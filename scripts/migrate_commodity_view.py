# -*- coding: utf-8 -*-
"""迁移省份分表并创建 V_WHOLE_COMMODITY 视图"""
import oracledb
import dmPython
import time

ORACLE_CLIENT_PATH = r"E:\workfile\JAVA\NewAPI\oracle_client"
oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)

ORACLE_CONFIG = {"user": "highway_exchange", "password": "qrwl", "dsn": "192.168.1.99/orcl"}
DM_CONFIG = {"user": "NEWPYTHON", "password": "NewPython@2025", "server": "192.168.1.99", "port": 5236}
BATCH_SIZE = 2000

# V_WHOLE_COMMODITY 视图涉及的省份分表
PROVINCE_TABLES = [
    "T_COMMODITY_340000",
]


def migrate_province_table(ora_conn, dm_conn, table_name):
    """迁移省份分表（与主表结构完全一致）"""
    ora_cur = ora_conn.cursor()
    dm_cur = dm_conn.cursor()

    # 检查达梦是否已存在
    table_exists = False
    try:
        dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        dm_cnt = dm_cur.fetchone()[0]
        table_exists = True
        # 清空已有数据，重新全量导入
        print(f"  {table_name}: 达梦已存在 {dm_cnt} 条，清空后重新导入")
        dm_cur.execute(f"DELETE FROM {table_name}")
        dm_conn.commit()
    except Exception:
        pass  # 表不存在，需要创建

    # 检查 Oracle 中是否存在
    try:
        ora_cur.execute(f"SELECT COUNT(*) FROM HIGHWAY_STORAGE.{table_name}")
        ora_cnt = ora_cur.fetchone()[0]
    except Exception as e:
        print(f"  {table_name}: Oracle 中不存在，跳过 ({e})")
        return False

    print(f"\n  迁移 {table_name}... (Oracle: {ora_cnt} 条)")

    if not table_exists:
        # 用主表 T_COMMODITY 的结构创建（结构完全一致）
        dm_cur.execute("SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'T_COMMODITY' ORDER BY COLUMN_ID")
        cols = dm_cur.fetchall()

        col_defs = []
        for col_name, data_type, data_length in cols:
            if data_type in ('INT', 'SMALLINT', 'BIGINT'):
                col_defs.append(f'"{col_name}" {data_type}')
            elif 'CHAR' in data_type:
                col_defs.append(f'"{col_name}" {data_type}({data_length})')
            elif 'DECIMAL' in data_type or 'NUMERIC' in data_type:
                col_defs.append(f'"{col_name}" {data_type}')
            elif 'TIMESTAMP' in data_type or 'DATE' in data_type:
                col_defs.append(f'"{col_name}" TIMESTAMP')
            else:
                col_defs.append(f'"{col_name}" {data_type}')

        create_sql = f'CREATE TABLE {table_name} ({", ".join(col_defs)})'
        try:
            dm_cur.execute(create_sql)
            dm_conn.commit()
            print(f"  建表成功 ({len(cols)} 字段)")
        except Exception as e:
            print(f"  建表失败: {e}")
            return False

    # 导入数据
    ora_cur.execute(f"SELECT * FROM HIGHWAY_STORAGE.{table_name}")
    col_names = [desc[0] for desc in ora_cur.description]
    placeholders = ",".join(["?" for _ in col_names])
    insert_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({placeholders})"

    total = 0
    start_time = time.time()
    batch = []
    for row in ora_cur:
        converted = []
        for val in row:
            if hasattr(val, 'strftime'):
                converted.append(val.strftime("%Y-%m-%d %H:%M:%S"))
            elif isinstance(val, str):
                try:
                    val.encode('gbk')
                    converted.append(val)
                except UnicodeEncodeError:
                    converted.append(val.encode('gbk', errors='replace').decode('gbk'))
            else:
                converted.append(val)
        batch.append(tuple(converted))

        if len(batch) >= BATCH_SIZE:
            dm_cur.executemany(insert_sql, batch)
            dm_conn.commit()
            total += len(batch)
            elapsed = time.time() - start_time
            speed = int(total / elapsed) if elapsed > 0 else 0
            print(f"    已插入: {total}/{ora_cnt} ({speed}条/秒)")
            batch = []

    if batch:
        dm_cur.executemany(insert_sql, batch)
        dm_conn.commit()
        total += len(batch)

    elapsed = time.time() - start_time
    print(f"  导入完成: {total} 条，耗时 {elapsed:.1f} 秒")

    # 校验
    dm_cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    dm_cnt = dm_cur.fetchone()[0]
    match = ora_cnt == dm_cnt
    print(f"  校验: Oracle={ora_cnt}, 达梦={dm_cnt} {'✅' if match else '❌'}")
    return match


def create_view(dm_conn):
    """在达梦中创建 V_WHOLE_COMMODITY 视图（完整复制 Oracle 定义）"""
    dm_cur = dm_conn.cursor()

    # 先删除旧视图
    try:
        dm_cur.execute("DROP VIEW V_WHOLE_COMMODITY")
        dm_conn.commit()
    except Exception:
        pass

    # 读取保存的视图定义（去掉 HIGHWAY_STORAGE. 前缀，因为达梦用户不需要）
    with open("scripts/baseline/v_whole_commodity_view.sql", "r", encoding="utf-8") as f:
        view_sql = f.read()

    # 去掉 Oracle schema 前缀
    view_sql = view_sql.replace("HIGHWAY_STORAGE.", "")

    print(f"\n创建视图 V_WHOLE_COMMODITY...")
    try:
        dm_cur.execute(view_sql)
        dm_conn.commit()
        print("✅ 视图创建成功")

        # 验证视图
        dm_cur.execute("SELECT COUNT(*) FROM V_WHOLE_COMMODITY")
        cnt = dm_cur.fetchone()[0]
        print(f"视图总行数: {cnt}")
    except Exception as e:
        print(f"❌ 视图创建失败: {e}")
        return False
    return True


if __name__ == "__main__":
    ora = oracledb.connect(**ORACLE_CONFIG)
    dm = dmPython.connect(**DM_CONFIG)

    # 1. 迁移省份分表
    print("=" * 60)
    print("  迁移省份分表")
    print("=" * 60)
    all_ok = True
    for table_name in PROVINCE_TABLES:
        if not migrate_province_table(ora, dm, table_name):
            all_ok = False

    # 2. 创建视图
    if not create_view(dm):
        all_ok = False

    ora.close()
    dm.close()

    if all_ok:
        print("\n✅ 全部完成！")
    else:
        print("\n⚠️ 部分操作可能未成功，请检查上方日志")
