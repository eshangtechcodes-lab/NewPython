# -*- coding: utf-8 -*-
"""
T_BUSINESSWARNING 表全量同步：Oracle → 达梦
来源：PLATFORM_DASHBOARD.T_BUSINESSWARNING
目标：NEWPYTHON.T_BUSINESSWARNING
"""
import sys
sys.path.insert(0, r"D:\Projects\Python\eshang_api")

import oracledb
try:
    oracledb.init_oracle_client(lib_dir=r"D:\instantclient_19_29")
except:
    pass

import dmPython
import time

# ========== 连接配置 ==========
ORACLE_DSN = "192.168.1.99:1521/orcl"
ORACLE_USER = "highway_exchange"
ORACLE_PWD = "qrwl"
ORACLE_SCHEMA = "PLATFORM_DASHBOARD"

DM_HOST = "192.168.1.99"
DM_PORT = 5236
DM_USER = "NEWPYTHON"
DM_PWD = "NewPython@2025"

TABLE_NAME = "T_BUSINESSWARNING"
BATCH_SIZE = 5000


def main():
    print("=" * 80)
    print(f"  T_BUSINESSWARNING 全量同步：Oracle → 达梦")
    print("=" * 80)

    # ========== 步骤1: 查 Oracle 端总行数和字段列表 ==========
    print("\n[步骤1] 连接 Oracle，查询表结构和总行数...")
    ora_conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    ora_cur = ora_conn.cursor()

    # 总行数
    ora_cur.execute(f"SELECT COUNT(*) FROM {ORACLE_SCHEMA}.{TABLE_NAME}")
    ora_total = ora_cur.fetchone()[0]
    print(f"  Oracle 总行数: {ora_total:,}")

    # 字段列表
    ora_cur.execute(f"SELECT * FROM {ORACLE_SCHEMA}.{TABLE_NAME} WHERE ROWNUM = 1")
    columns = [desc[0] for desc in ora_cur.description]
    col_types = [(desc[0], desc[1].__name__ if hasattr(desc[1], '__name__') else str(desc[1])) for desc in ora_cur.description]
    print(f"  字段数: {len(columns)}")
    print(f"  字段列表: {', '.join(columns)}")
    print(f"  字段类型:")
    for cname, ctype in col_types:
        print(f"    {cname:<30s} {ctype}")

    # ========== 步骤2: 查达梦端总行数 ==========
    print(f"\n[步骤2] 连接达梦，查询当前数据量...")
    dm_conn = dmPython.connect(user=DM_USER, password=DM_PWD,
                               server=DM_HOST, port=DM_PORT)
    dm_cur = dm_conn.cursor()

    dm_cur.execute(f'SELECT COUNT(*) FROM "{TABLE_NAME}"')
    dm_total_before = dm_cur.fetchone()[0]
    print(f"  达梦当前行数: {dm_total_before:,}")

    if dm_total_before == ora_total:
        print(f"\n  ✅ 数据已一致 ({dm_total_before:,} 条)，无需同步。")
        # 仍然执行验证
        do_verification(ora_cur, dm_cur, ora_total)
        ora_conn.close()
        dm_conn.close()
        return

    # ========== 步骤3: 清空达梦端表 ==========
    print(f"\n[步骤3] 清空达梦端 {TABLE_NAME}...")
    dm_cur.execute(f'DELETE FROM "{TABLE_NAME}"')
    dm_conn.commit()
    print(f"  已清空（删除 {dm_total_before:,} 条）")

    # ========== 步骤4: 分批同步 ==========
    print(f"\n[步骤4] 开始分批同步（每批 {BATCH_SIZE:,} 条）...")
    placeholders = ", ".join(["?" for _ in columns])
    col_list = ", ".join([f'"{c}"' for c in columns])
    insert_sql = f'INSERT INTO "{TABLE_NAME}" ({col_list}) VALUES ({placeholders})'

    offset = 0
    imported = 0
    failed_rows = 0
    start_time = time.time()

    while offset < ora_total:
        ora_cur.execute(f"""
            SELECT * FROM (
                SELECT a.*, ROWNUM rnum FROM {ORACLE_SCHEMA}.{TABLE_NAME} a
                WHERE ROWNUM <= {offset + BATCH_SIZE}
            ) WHERE rnum > {offset}
        """)
        rows = ora_cur.fetchall()
        if not rows:
            break

        # 去掉rnum列（最后一列是ROWNUM别名）
        clean_rows = [row[:-1] for row in rows]

        try:
            dm_cur.executemany(insert_sql, clean_rows)
            dm_conn.commit()
            imported += len(clean_rows)
        except Exception as e:
            print(f"    ⚠️ 批量插入失败 offset={offset}: {e}")
            dm_conn.rollback()
            # 逐条插入，跳过失败行
            for row in clean_rows:
                try:
                    dm_cur.execute(insert_sql, row)
                    dm_conn.commit()
                    imported += 1
                except Exception as e2:
                    failed_rows += 1
                    if failed_rows <= 5:
                        print(f"    ❌ 单条插入失败: {e2}")

        elapsed = time.time() - start_time
        pct = imported * 100 // ora_total if ora_total > 0 else 0
        speed = imported / elapsed if elapsed > 0 else 0
        eta = (ora_total - imported) / speed if speed > 0 else 0
        print(f"    {imported:>10,}/{ora_total:>10,} ({pct:>3d}%)  "
              f"速度: {speed:,.0f} 条/秒  预计剩余: {eta:.0f}秒")

        offset += BATCH_SIZE

    elapsed_total = time.time() - start_time
    print(f"\n  同步完成! 耗时: {elapsed_total:.1f}秒, "
          f"成功: {imported:,} 条, 失败: {failed_rows:,} 条")

    # ========== 步骤5: 验证 ==========
    do_verification(ora_cur, dm_cur, ora_total)

    ora_conn.close()
    dm_conn.close()


def do_verification(ora_cur, dm_cur, ora_total):
    """同步后验证"""
    print(f"\n{'=' * 80}")
    print(f"  [步骤5] 数据验证")
    print(f"{'=' * 80}")

    # 5.1 总行数验证
    print("\n  [5.1] 总行数验证...")
    dm_cur.execute(f'SELECT COUNT(*) FROM "{TABLE_NAME}"')
    dm_final = dm_cur.fetchone()[0]
    if dm_final == ora_total:
        print(f"    ✅ 行数一致: Oracle={ora_total:,}, 达梦={dm_final:,}")
    else:
        print(f"    ❌ 行数不一致: Oracle={ora_total:,}, 达梦={dm_final:,}, 差={ora_total - dm_final:,}")

    # 5.2 抽样检查: DATATYPE=1, STATISTICS_MONTH=202602, SERVERPART_ID IN (377,417,432)
    #     验证 VEHICLE_COUNT_YOY 和 VEHICLE_COUNT_QOQ 不为 null
    print("\n  [5.2] 抽样检查: DATATYPE=1, STATISTICS_MONTH=202602, SERVERPART_ID IN (377,417,432)")
    print("        验证 VEHICLE_COUNT_YOY, VEHICLE_COUNT_QOQ 不为 null...")

    sample_sql = """
        SELECT "SERVERPART_ID", "VEHICLE_COUNT_YOY", "VEHICLE_COUNT_QOQ"
        FROM "{table}"
        WHERE "DATATYPE" = 1
          AND "STATISTICS_MONTH" = '202602'
          AND "SERVERPART_ID" IN (377, 417, 432)
        ORDER BY "SERVERPART_ID"
    """.format(table=TABLE_NAME)

    # Oracle 端
    ora_sample_sql = f"""
        SELECT SERVERPART_ID, VEHICLE_COUNT_YOY, VEHICLE_COUNT_QOQ
        FROM {ORACLE_SCHEMA}.{TABLE_NAME}
        WHERE DATATYPE = 1
          AND STATISTICS_MONTH = '202602'
          AND SERVERPART_ID IN (377, 417, 432)
        ORDER BY SERVERPART_ID
    """
    ora_cur.execute(ora_sample_sql)
    ora_rows = ora_cur.fetchall()
    print(f"    Oracle 端结果 ({len(ora_rows)} 条):")
    for r in ora_rows:
        yoy_ok = "✅" if r[1] is not None else "❌ NULL"
        qoq_ok = "✅" if r[2] is not None else "❌ NULL"
        print(f"      SERVERPART_ID={r[0]:>5}, YOY={str(r[1]):>12s} {yoy_ok}, QOQ={str(r[2]):>12s} {qoq_ok}")

    # 达梦端
    dm_cur.execute(sample_sql)
    dm_rows = dm_cur.fetchall()
    print(f"    达梦端结果 ({len(dm_rows)} 条):")
    for r in dm_rows:
        yoy_ok = "✅" if r[1] is not None else "❌ NULL"
        qoq_ok = "✅" if r[2] is not None else "❌ NULL"
        print(f"      SERVERPART_ID={r[0]:>5}, YOY={str(r[1]):>12s} {yoy_ok}, QOQ={str(r[2]):>12s} {qoq_ok}")

    if len(dm_rows) == len(ora_rows):
        print(f"    ✅ 抽样记录数一致: {len(dm_rows)} 条")
    else:
        print(f"    ❌ 抽样记录数不一致: Oracle={len(ora_rows)}, 达梦={len(dm_rows)}")

    # 5.3 抽样检查: DATATYPE=2, STATISTICS_MONTH=202602, SERVERPART_ID=377
    #     验证 SUM(REVENUE_AMOUNT_YOY) 近似一致
    print("\n  [5.3] 抽样检查: DATATYPE=2, STATISTICS_MONTH=202602, SERVERPART_ID=377")
    print("        验证 SUM(REVENUE_AMOUNT_YOY) 值近似...")

    ora_sum_sql = f"""
        SELECT SUM(REVENUE_AMOUNT_YOY) 
        FROM {ORACLE_SCHEMA}.{TABLE_NAME}
        WHERE DATATYPE = 2
          AND STATISTICS_MONTH = '202602'
          AND SERVERPART_ID = 377
    """
    ora_cur.execute(ora_sum_sql)
    ora_sum = ora_cur.fetchone()[0]

    dm_sum_sql = f"""
        SELECT SUM("REVENUE_AMOUNT_YOY") 
        FROM "{TABLE_NAME}"
        WHERE "DATATYPE" = 2
          AND "STATISTICS_MONTH" = '202602'
          AND "SERVERPART_ID" = 377
    """
    dm_cur.execute(dm_sum_sql)
    dm_sum = dm_cur.fetchone()[0]

    print(f"    Oracle SUM(REVENUE_AMOUNT_YOY) = {ora_sum}")
    print(f"    达梦   SUM(REVENUE_AMOUNT_YOY) = {dm_sum}")

    if ora_sum is not None and dm_sum is not None:
        # 允许浮点误差
        diff = abs(float(ora_sum) - float(dm_sum))
        if diff < 0.01:
            print(f"    ✅ 值完全一致 (差值={diff})")
        elif diff < 1.0:
            print(f"    ✅ 值近似一致 (差值={diff:.6f})")
        else:
            print(f"    ⚠️ 值有差异 (差值={diff:.4f})")
    elif ora_sum is None and dm_sum is None:
        print(f"    ⚠️ 两端均为 NULL（可能没有匹配数据）")
    else:
        print(f"    ❌ 一端为 NULL: Oracle={ora_sum}, 达梦={dm_sum}")

    print(f"\n{'=' * 80}")
    print(f"  验证完成!")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
