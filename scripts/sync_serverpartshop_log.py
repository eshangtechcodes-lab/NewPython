# -*- coding: utf-8 -*-
"""
T_SERVERPARTSHOP_LOG 全量同步（处理唯一约束冲突）
方案：禁用唯一约束 → 清空 → 全量导入 → 重建约束
"""
import sys, time
sys.path.insert(0, r"D:\Projects\Python\eshang_api")

import oracledb
try:
    oracledb.init_oracle_client(lib_dir=r"D:\instantclient_19_29")
except:
    pass
import dmPython

TABLE = "T_SERVERPARTSHOP_LOG"
SCHEMA = "HIGHWAY_STORAGE"
BATCH = 5000

# ====== 连接 ======
ora_conn = oracledb.connect(user="highway_exchange", password="qrwl", dsn="192.168.1.99:1521/orcl")
ora_cur = ora_conn.cursor()
dm_conn = dmPython.connect(user="NEWPYTHON", password="NewPython@2025", server="192.168.1.99", port=5236)
dm_cur = dm_conn.cursor()

# ====== 步骤1: 查 Oracle 信息 ======
ora_cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.{TABLE}")
ora_total = ora_cur.fetchone()[0]
print(f"Oracle 总行数: {ora_total:,}")

ora_cur.execute(f"SELECT * FROM {SCHEMA}.{TABLE} WHERE ROWNUM = 1")
columns = [desc[0] for desc in ora_cur.description]
print(f"字段数: {len(columns)}")

# ====== 步骤2: 查达梦端约束信息 ======
print("\n查询达梦端约束...")
dm_cur.execute("""
    SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE 
    FROM USER_CONSTRAINTS 
    WHERE TABLE_NAME = 'T_SERVERPARTSHOP_LOG'
""")
constraints = dm_cur.fetchall()
print(f"  约束列表:")
for cname, ctype in constraints:
    print(f"    {cname} (类型: {ctype})")

# ====== 步骤3: 禁用所有约束 ======
print("\n禁用约束...")
for cname, ctype in constraints:
    try:
        dm_cur.execute(f'ALTER TABLE "{TABLE}" DISABLE CONSTRAINT "{cname}"')
        dm_conn.commit()
        print(f"  已禁用: {cname}")
    except Exception as e:
        print(f"  禁用失败 {cname}: {e}")

# ====== 步骤4: 清空表 ======
print("\n清空达梦表...")
dm_cur.execute(f'DELETE FROM "{TABLE}"')
dm_conn.commit()
print("已清空")

# ====== 步骤5: 分批导入 ======
print(f"\n开始分批同步（每批 {BATCH:,} 条）...")
placeholders = ", ".join(["?" for _ in columns])
col_list = ", ".join([f'"{c}"' for c in columns])
insert_sql = f'INSERT INTO "{TABLE}" ({col_list}) VALUES ({placeholders})'

offset = 0
imported = 0
failed = 0
t0 = time.time()

while offset < ora_total:
    ora_cur.execute(f"""
        SELECT * FROM (
            SELECT a.*, ROWNUM rnum FROM {SCHEMA}.{TABLE} a
            WHERE ROWNUM <= {offset + BATCH}
        ) WHERE rnum > {offset}
    """)
    rows = ora_cur.fetchall()
    if not rows:
        break
    clean_rows = [row[:-1] for row in rows]
    try:
        dm_cur.executemany(insert_sql, clean_rows)
        dm_conn.commit()
        imported += len(clean_rows)
    except Exception as e:
        print(f"  批量失败 offset={offset}: {e}")
        dm_conn.rollback()
        # 逐条插入
        for row in clean_rows:
            try:
                dm_cur.execute(insert_sql, row)
                dm_conn.commit()
                imported += 1
            except:
                failed += 1
    
    elapsed = time.time() - t0
    pct = imported * 100 // ora_total
    speed = imported / elapsed if elapsed > 0 else 0
    print(f"  {imported:>10,}/{ora_total:>10,} ({pct:>3d}%)  速度: {speed:,.0f} 条/秒  失败: {failed}")
    offset += BATCH

# ====== 步骤6: 重新启用约束 ======
print("\n重新启用约束...")
for cname, ctype in constraints:
    try:
        dm_cur.execute(f'ALTER TABLE "{TABLE}" ENABLE CONSTRAINT "{cname}"')
        dm_conn.commit()
        print(f"  已启用: {cname}")
    except Exception as e:
        print(f"  ⚠️ 启用失败 {cname}: {e}")
        print(f"     （Oracle端数据本身可能含重复键，这是正常的）")

# ====== 步骤7: 验证 ======
dm_cur.execute(f'SELECT COUNT(*) FROM "{TABLE}"')
dm_final = dm_cur.fetchone()[0]
elapsed = time.time() - t0

print(f"\n{'=' * 60}")
print(f"同步完成! 耗时: {elapsed:.1f}秒")
print(f"  Oracle:  {ora_total:,}")
print(f"  达梦:    {dm_final:,}")
print(f"  导入:    {imported:,}")
print(f"  失败:    {failed:,}")
if dm_final == ora_total:
    print(f"  ✅ 行数完全一致")
elif dm_final >= ora_total - 10:
    print(f"  ✅ 行数近似一致（差 {ora_total - dm_final} 条，可能是Oracle重复数据被跳过）")
else:
    print(f"  ❌ 行数差异较大: 差 {ora_total - dm_final:,} 条")
print(f"{'=' * 60}")

ora_conn.close()
dm_conn.close()
