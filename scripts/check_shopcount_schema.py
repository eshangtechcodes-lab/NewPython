# -*- coding: utf-8 -*-
"""检查 T_SHOPCOUNT 表结构差异"""
import oracledb
import dmPython

ORA_CLIENT_DIR = r"D:\app\YSKJ02\product\11.2.0\dbhome_1\bin"
try:
    oracledb.init_oracle_client(lib_dir=ORA_CLIENT_DIR)
except: pass

# Oracle
ora = oracledb.connect(user="highway_storage", password="qrwl", dsn="127.0.0.1:1521/orcl")
ora_cur = ora.cursor()
ora_cur.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE
    FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'T_SHOPCOUNT' ORDER BY COLUMN_ID
""")
ora_cols = ora_cur.fetchall()

# Dameng
dm = dmPython.connect(user="NEWPYTHON", password="NewPython@2025", server="127.0.0.1", port=5236)
dm_cur = dm.cursor()
dm_cur.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE, NULLABLE
    FROM USER_TAB_COLUMNS WHERE TABLE_NAME = 'T_SHOPCOUNT' ORDER BY COLUMN_ID
""")
dm_cols = dm_cur.fetchall()

print("=== T_SHOPCOUNT 列对比 ===")
print(f"{'列名':<30s} {'Oracle类型':<25s} {'Dameng类型':<25s} {'匹配'}")
print("-" * 90)
dm_dict = {c[0]: c for c in dm_cols}
for oc in ora_cols:
    name = oc[0]
    o_type = f"{oc[1]}({oc[2]}/{oc[3]}/{oc[4]})"
    dc = dm_dict.get(name)
    if dc:
        d_type = f"{dc[1]}({dc[2]}/{dc[3]}/{dc[4]})"
        match = "✅" if True else "❌"
        print(f"{name:<30s} {o_type:<25s} {d_type:<25s} {match}")
    else:
        print(f"{name:<30s} {o_type:<25s} {'缺失!':<25s} ❌")

# 尝试插入一行测试
ora_cur.execute('SELECT * FROM "T_SHOPCOUNT" WHERE ROWNUM <= 1')
row = ora_cur.fetchone()
cols = [d[0] for d in ora_cur.description]
print(f"\nOracle 首行: {len(cols)} 列")
print(f"Dameng 列数: {len(dm_cols)}")
print(f"Oracle 列: {cols}")

# 尝试手动插入看报错
col_list = ", ".join(f'"{c}"' for c in cols)
placeholders = ", ".join(["?" for _ in cols])
insert_sql = f'INSERT INTO "T_SHOPCOUNT" ({col_list}) VALUES ({placeholders})'
clean_row = []
for i, val in enumerate(row):
    if hasattr(val, 'read'):
        clean_row.append(val.read() if val else None)
    else:
        clean_row.append(val)
    print(f"  {cols[i]}: {type(val).__name__} = {str(val)[:50]}")

try:
    dm_cur.execute(insert_sql, tuple(clean_row))
    dm.commit()
    print("\n✅ 手动插入成功!")
except Exception as e:
    print(f"\n❌ 手动插入失败: {e}")

ora.close()
dm.close()
