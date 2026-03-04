# -*- coding: utf-8 -*-
"""达梦数据库建表和测试数据初始化"""
import dmPython

conn = dmPython.connect(user='DMNEW', password='Dmnew@2025Aa', server='127.0.0.1', port=5236)
cur = conn.cursor()

# 删除旧表和序列
for sql in ['DROP TABLE T_BRAND', 'DROP SEQUENCE SEQ_BRAND']:
    try:
        cur.execute(sql)
        print(f'执行成功: {sql}')
    except Exception:
        print(f'跳过: {sql}（不存在）')
conn.commit()

# 创建序列
cur.execute('CREATE SEQUENCE SEQ_BRAND START WITH 1 INCREMENT BY 1')
print('创建序列 SEQ_BRAND 成功')

# 创建品牌表
cur.execute("""CREATE TABLE T_BRAND (
    BRAND_ID INT PRIMARY KEY,
    BRAND_PID INT,
    BRAND_INDEX INT,
    BRAND_NAME VARCHAR(200),
    BRAND_CATEGORY INT,
    BRAND_INDUSTRY VARCHAR(200),
    BRAND_TYPE INT,
    BRAND_INTRO VARCHAR(500),
    BRAND_STATE SMALLINT DEFAULT 1,
    WECHATAPPSIGN_ID INT,
    WECHATAPPSIGN_NAME VARCHAR(200),
    WECHATAPP_APPID VARCHAR(200),
    OWNERUNIT_ID INT,
    OWNERUNIT_NAME VARCHAR(200),
    PROVINCE_CODE INT,
    STAFF_ID INT,
    STAFF_NAME VARCHAR(100),
    OPERATE_DATE TIMESTAMP,
    BRAND_DESC VARCHAR(2000),
    COMMISSION_RATIO VARCHAR(50)
)""")
print('创建表 T_BRAND 成功')

# 插入测试数据
test_data = [
    ('星巴克', 1000, '餐饮', 1, 1, '浙江高速服务区', '管理员'),
    ('肯德基', 1000, '餐饮', 1, 1, '浙江高速服务区', '管理员'),
    ('全家便利店', 1000, '零售', 2, 1, '浙江高速服务区', '管理员'),
    ('天猫优选', 2000, '电商', 3, 2, '杭州服务区', '操作员'),
    ('中石化', 1000, '油品', 4, 1, '浙江高速服务区', '管理员'),
]
for name, cat, ind, btype, oid, oname, staff in test_data:
    cur.execute('SELECT SEQ_BRAND.NEXTVAL')
    bid = cur.fetchone()[0]
    sql = (f"INSERT INTO T_BRAND (BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY, "
           f"BRAND_TYPE, BRAND_STATE, OWNERUNIT_ID, OWNERUNIT_NAME, STAFF_NAME, OPERATE_DATE) "
           f"VALUES ({bid}, '{name}', {cat}, '{ind}', {btype}, 1, {oid}, '{oname}', '{staff}', SYSDATE)")
    cur.execute(sql)

conn.commit()
print('插入 5 条测试数据成功')

# 验证
cur.execute('SELECT COUNT(*) FROM T_BRAND')
print(f'当前表中数据: {cur.fetchone()[0]} 条')

cur.execute('SELECT BRAND_ID, BRAND_NAME, BRAND_CATEGORY, BRAND_INDUSTRY FROM T_BRAND')
for row in cur.fetchall():
    print(f'  ID={row[0]}, 名称={row[1]}, 分类={row[2]}, 业态={row[3]}')

cur.close()
conn.close()
print('建表和测试数据初始化完成！')
