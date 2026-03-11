# -*- coding: utf-8 -*-
"""
在达梦中创建 BaseInfoController 依赖的表
方案：根据原 API 返回的字段格式和 C# Model 定义，手动建表
后续完整数据通过达梦 DTS 工具从 Oracle 导入
"""
import dmPython

print("=" * 60)
print("  在达梦中创建 BaseInfoController 依赖表")
print("=" * 60)

conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()


def create_table(cur, conn, table_name, create_sql, comment_sql_list):
    """建表 + 添加注释"""
    try:
        cur.execute(f"DROP TABLE {table_name}")
        conn.commit()
    except:
        pass
    
    cur.execute(create_sql)
    conn.commit()
    print(f"  ✅ {table_name} 建表成功")
    
    for sql in comment_sql_list:
        try:
            cur.execute(sql)
        except Exception as ex:
            print(f"  ⚠️ 注释失败: {ex}")
    conn.commit()
    if comment_sql_list:
        print(f"  ✅ {len(comment_sql_list)} 条注释已添加")


# ====== T_AUTOSTATISTICS（经营业态/自定义统计表，COOP_MERCHANT schema）======
print("\n[1] T_AUTOSTATISTICS")
create_table(cur, conn, "T_AUTOSTATISTICS", """
CREATE TABLE T_AUTOSTATISTICS (
    AUTOSTATISTICS_ID       INT,
    AUTOSTATISTICS_PID      INT,
    AUTOSTATISTICS_NAME     VARCHAR(200),
    AUTOSTATISTICS_VALUE    VARCHAR(200),
    AUTOSTATISTICS_INDEX    INT,
    AUTOSTATISTICS_ICO      VARCHAR(500),
    AUTOSTATISTICS_TYPE     INT,
    AUTOSTATISTICS_STATE    INT,
    AUTOSTATISTICS_DESC     VARCHAR(500),
    OWNERUNIT_ID            INT,
    OWNERUNIT_NAME          VARCHAR(200),
    PROVINCE_CODE           INT,
    OPERATE_DATE            VARCHAR(30),
    STAFF_ID                INT,
    STAFF_NAME              VARCHAR(100)
)
""", [
    "COMMENT ON TABLE T_AUTOSTATISTICS IS '自定义统计归口表（经营业态等）'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_ID IS '内码'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_PID IS '父级内码'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_NAME IS '名称'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_VALUE IS '值'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_INDEX IS '排序索引'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_ICO IS '图标URL'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_TYPE IS '类型（2000=经营业态）'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_STATE IS '有效状态'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.AUTOSTATISTICS_DESC IS '备注说明'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.OWNERUNIT_ID IS '业主单位内码'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.OWNERUNIT_NAME IS '业主单位名称'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.PROVINCE_CODE IS '省份编码'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.OPERATE_DATE IS '操作时间'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.STAFF_ID IS '操作人内码'",
    "COMMENT ON COLUMN T_AUTOSTATISTICS.STAFF_NAME IS '操作人姓名'",
])

# 从原 API 基准数据填充 T_AUTOSTATISTICS
# GetBusinessTradeList GET 返回 35 条，字段: BUSINESSTRADE_NAME -> AUTOSTATISTICS_NAME, BUSINESSTRADE_PNAME -> parent name
# 但这个基准不够完整，需要直接用 API 的 SQL 查询结构来推断数据
# 简单方案：先用原 API 数据创建测试记录
import json

# 读取 GET 版本基准（只有 name 和 parent name）
try:
    with open("scripts/baseline/GetBusinessTradeList_GET.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data["Result_Data"]["List"]
    
    # 先插入父级（AUTOSTATISTICS_TYPE=2000, AUTOSTATISTICS_PID=0）
    parent_names = list(set(item.get("BUSINESSTRADE_PNAME", "") for item in items if item.get("BUSINESSTRADE_PNAME")))
    pid_map = {}
    for i, pname in enumerate(parent_names, 1):
        pid = 90000 + i  # 临时父级 ID
        pid_map[pname] = pid
        cur.execute("""
            INSERT INTO T_AUTOSTATISTICS (AUTOSTATISTICS_ID, AUTOSTATISTICS_PID, AUTOSTATISTICS_NAME, 
                AUTOSTATISTICS_TYPE, PROVINCE_CODE)
            VALUES (?, 0, ?, 2000, 340000)
        """, [pid, pname])
    
    # 插入子级
    for i, item in enumerate(items, 1):
        aid = 80000 + i
        pname = item.get("BUSINESSTRADE_PNAME", "")
        pid = pid_map.get(pname, 0)
        cur.execute("""
            INSERT INTO T_AUTOSTATISTICS (AUTOSTATISTICS_ID, AUTOSTATISTICS_PID, AUTOSTATISTICS_NAME,
                AUTOSTATISTICS_INDEX, AUTOSTATISTICS_ICO, AUTOSTATISTICS_TYPE, AUTOSTATISTICS_STATE,
                OWNERUNIT_ID, OWNERUNIT_NAME, PROVINCE_CODE, OPERATE_DATE, AUTOSTATISTICS_DESC)
            VALUES (?, ?, ?, ?, ?, 2000, ?, ?, ?, ?, ?, ?)
        """, [aid, pid, 
              item.get("BUSINESSTRADE_NAME", ""),
              item.get("BUSINESSTRADE_INDEX"),
              item.get("BUSINESSTRADE_ICO"),
              item.get("BUSINESSTRADE_STATE"),
              item.get("OWNERUNIT_ID"),
              item.get("OWNERUNIT_NAME"),
              item.get("PROVINCE_CODE"),
              item.get("OPERATE_DATE"),
              item.get("BUSINESSTRADE_DESC")])
    conn.commit()
    print(f"  ✅ 插入 {len(parent_names)} 个父级 + {len(items)} 个子级")
except Exception as ex:
    print(f"  ⚠️ 数据导入失败: {ex}")

# ====== T_SHOPCOUNT（门店商家数量统计表，HIGHWAY_STORAGE schema）======
print("\n[2] T_SHOPCOUNT")
create_table(cur, conn, "T_SHOPCOUNT", """
CREATE TABLE T_SHOPCOUNT (
    SHOPCOUNT_ID            INT,
    SERVERPART_ID           INT,
    SPREGIONTYPE_NAME       VARCHAR(200),
    SHOP_TOTALCOUNT         INT,
    SHOP_BUSINESSCOUNT      INT,
    SHOP_REVENUECOUNT       INT,
    OPERATE_DATE            DECIMAL(20,0),
    PROVINCE_CODE           INT,
    STATISTICS_DATE         VARCHAR(30)
)
""", [
    "COMMENT ON TABLE T_SHOPCOUNT IS '服务区门店商家数量统计表'",
    "COMMENT ON COLUMN T_SHOPCOUNT.SHOPCOUNT_ID IS '内码'",
    "COMMENT ON COLUMN T_SHOPCOUNT.SERVERPART_ID IS '服务区内码'",
    "COMMENT ON COLUMN T_SHOPCOUNT.SPREGIONTYPE_NAME IS '片区名称'",
    "COMMENT ON COLUMN T_SHOPCOUNT.SHOP_TOTALCOUNT IS '门店总数量'",
    "COMMENT ON COLUMN T_SHOPCOUNT.SHOP_BUSINESSCOUNT IS '在营门店数量'",
    "COMMENT ON COLUMN T_SHOPCOUNT.SHOP_REVENUECOUNT IS '纳入营收统计门店数量'",
    "COMMENT ON COLUMN T_SHOPCOUNT.OPERATE_DATE IS '修改时间'",
    "COMMENT ON COLUMN T_SHOPCOUNT.PROVINCE_CODE IS '省份编码'",
    "COMMENT ON COLUMN T_SHOPCOUNT.STATISTICS_DATE IS '统计日期'",
])

# 从基准数据导入
try:
    with open("scripts/baseline/GetShopCountList_GET.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data["Result_Data"]["List"]
    
    for item in items:
        cur.execute("""
            INSERT INTO T_SHOPCOUNT (SHOPCOUNT_ID, SERVERPART_ID, SPREGIONTYPE_NAME,
                SHOP_TOTALCOUNT, SHOP_BUSINESSCOUNT, SHOP_REVENUECOUNT, OPERATE_DATE)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            item.get("SHOPCOUNT_ID"),
            item.get("SERVERPART_ID"),
            item.get("SPREGIONTYPE_NAME"),
            item.get("SHOP_TOTALCOUNT"),
            item.get("SHOP_BUSINESSCOUNT"),
            item.get("SHOP_REVENUECOUNT"),
            item.get("OPERATE_DATE"),
        ])
    conn.commit()
    print(f"  ✅ 插入 {len(items)} 条")
except Exception as ex:
    print(f"  ⚠️ 数据导入失败: {ex}")

# 验证
print("\n[验证]")
for t in ["T_AUTOSTATISTICS", "T_SHOPCOUNT", "T_SERVERPARTTYPE"]:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        c = cur.fetchone()[0]
        print(f"  ✅ {t:25s} {c:>5} 条")
    except:
        print(f"  ❌ {t:25s} 不存在")

conn.close()
print("\n✅ 全部完成")
