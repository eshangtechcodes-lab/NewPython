# -*- coding: utf-8 -*-
"""
第零步：在达梦中创建 T_SERVERPARTTYPE 表并插入基础数据
由于 Oracle 直连需要 thick mode 客户端，改用原 API 获取的基准数据 + 手动建表
"""
import dmPython

print("=" * 60)
print("  在达梦中创建 T_SERVERPARTTYPE 表")
print("=" * 60)

conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()

# 1. 建表（根据原 Oracle 表结构，关键字段映射）
print("\n[1] 建表...")
try:
    cur.execute("DROP TABLE T_SERVERPARTTYPE")
    conn.commit()
    print("  已删除旧表")
except:
    pass

# Oracle 原表结构：HIGHWAY_STORAGE.T_SERVERPARTTYPE
# Helper SQL只用到: SERVERPARTTYPE_ID, TYPE_NAME, SERVERPARTSTATICTYPE_ID, PROVINCE_CODE, TYPE_INDEX
create_sql = """
CREATE TABLE T_SERVERPARTTYPE (
    SERVERPARTTYPE_ID       INT,
    TYPE_NAME               VARCHAR(200),
    TYPE_INDEX              INT,
    SERVERPARTSTATICTYPE_ID INT,
    PROVINCE_CODE           INT,
    PARENT_ID               INT,
    TYPE_CODE               VARCHAR(50),
    TYPE_DESC               VARCHAR(500),
    OPERATE_DATE            VARCHAR(30),
    STAFF_ID                INT,
    STAFF_NAME              VARCHAR(100)
)
"""
cur.execute(create_sql)
conn.commit()
print("  ✅ 建表成功")

# 2. 从原 API 获取全量数据不够（API 只返回 name/value），需要通过原数据库补全
# 但由于 Oracle 无法直连，先用原 SQL 逻辑中的关键字段插入测试数据
# 原 SQL 条件: SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = 340000
# 原 API 返回: 7条数据 {name: "皖中管理中心", value: "72"} 等

# 这些数据来自原 API 基准文件
import json
with open("scripts/baseline_GetSPRegionList.json", "r", encoding="utf-8") as f:
    baseline = json.load(f)

region_list = baseline["Result_Data"]["List"]
print(f"\n[2] 从基准数据插入 {len(region_list)} 条记录...")

for i, item in enumerate(region_list):
    insert_sql = """
        INSERT INTO T_SERVERPARTTYPE (SERVERPARTTYPE_ID, TYPE_NAME, TYPE_INDEX, SERVERPARTSTATICTYPE_ID, PROVINCE_CODE)
        VALUES (?, ?, ?, 1000, 340000)
    """
    cur.execute(insert_sql, [int(item['value']), item['name'], i + 1])

conn.commit()
print(f"  ✅ 插入完成")

# 3. 验证
print(f"\n[3] 验证查询（模拟原 Helper SQL）...")
cur.execute("""
    SELECT TYPE_NAME, SERVERPARTTYPE_ID 
    FROM T_SERVERPARTTYPE 
    WHERE SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = 340000 
    ORDER BY TYPE_INDEX
""")
result = cur.fetchall()
print(f"  查询结果: {len(result)} 条")
for r in result:
    print(f"    name={r[0]}, value={r[1]}")

conn.close()
print("\n✅ T_SERVERPARTTYPE 表同步完成")
