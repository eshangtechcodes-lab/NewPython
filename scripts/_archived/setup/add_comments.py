"""为达梦中的 T_OWNERUNIT 和 T_SERVERPART 添加表注释和字段注释"""
import dmPython

conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='192.168.1.99', port=5236)
cur = conn.cursor()

# ===== T_OWNERUNIT 表注释和字段注释 =====
OWNERUNIT_COMMENTS = {
    "__table__": "业主单位管理表",
    "OWNERUNIT_ID": "业主内码",
    "OWNERUNIT_PID": "父级内码",
    "PROVINCE_CODE": "省份标识",
    "PROVINCE_BUSINESSCODE": "业务省份标识",
    "OWNERUNIT_NAME": "业主单位名称",
    "OWNERUNIT_EN": "业主简称",
    "OWNERUNIT_NATURE": "业主单位性质(1000:管理单位;2000:经营单位)",
    "OWNERUNIT_GUID": "业主标识",
    "OWNERUNIT_INDEX": "排序字段",
    "OWNERUNIT_ICO": "业主图标",
    "OWNERUNIT_STATE": "有效状态",
    "STAFF_ID": "操作人员内码",
    "STAFF_NAME": "操作人员名称",
    "OPERATE_DATE": "操作时间",
    "OWNERUNIT_DESC": "备注",
    "ISSUPPORTPOINT": "是否支持积分功能",
    "DOWNLOAD_DATE": "下载时间",
    "WECHATPUBLICSIGN_ID": "公众号ID",
}

# ===== T_SERVERPART 表注释和字段注释 =====
SERVERPART_COMMENTS = {
    "__table__": "服务区站点表",
    "SERVERPART_ID": "服务区内码",
    "SERVERPART_NAME": "服务区名称",
    "SERVERPART_ADDRESS": "服务区地址",
    "SERVERPART_INDEX": "排序索引",
    "EXPRESSWAY_NAME": "所在高速路",
    "SELLERCOUNT": "商家服务数",
    "SERVERPART_AREA": "服务区面积",
    "SERVERPART_X": "坐标X(经度)",
    "SERVERPART_Y": "坐标Y(纬度)",
    "SERVERPART_TEL": "电话号码",
    "SERVERPART_INFO": "服务区说明",
    "PROVINCE_CODE": "省份编码",
    "CITY_CODE": "城市编码",
    "COUNTY_CODE": "区县编码",
    "SERVERPART_CODE": "服务区编码",
    "FIELDENUM_ID": "枚举内码",
    "SERVERPART_IPADDRESS": "IP地址描述",
    "SERVERPART_TYPE": "服务区类型",
    "DAYINCAR": "日均入区车辆",
    "HKBL": "入区车辆客货比例",
    "STARTDATE": "开业时间",
    "OWNEDCOMPANY": "所属公司",
    "FLOORAREA": "占地面积",
    "BUSINESSAREA": "经营面积",
    "SHAREAREA": "公共区域面积",
    "TOTALPARKING": "车位数",
    "MANAGERCOMPANY": "管理公司",
    "SHORTNAME": "服务区简称",
    "REGIONTYPE_ID": "附属管辖内码",
    "STATISTIC_TYPE": "统计类型(1000:正式;2000:测试;3000:替代)",
    "PROVINCE_NAME": "省份名称",
    "SPREGIONTYPE_ID": "归属区域内码",
    "SPREGIONTYPE_NAME": "归属区域名称",
    "SPREGIONTYPE_INDEX": "归属区域索引",
    "REGIONTYPE_NAME": "附属管辖名称",
    "STATISTICS_TYPE": "站点类型(服务区、加油站、单位部门)",
    "STAFF_ID": "操作员内码",
    "STAFF_NAME": "操作人员",
    "OPERATE_DATE": "操作时间",
    "SERVERPART_DESC": "备注说明",
    "OWNERUNIT_ID": "业主单位内码",
    "OWNERUNIT_NAME": "业主单位名称",
}


def add_comments(table_name, comments_dict):
    """添加表注释和字段注释"""
    # 表注释
    table_comment = comments_dict.pop("__table__", None)
    if table_comment:
        sql = f"COMMENT ON TABLE {table_name} IS '{table_comment}'"
        cur.execute(sql)
        print(f"  表注释: {table_comment}")

    # 字段注释
    count = 0
    for col, comment in comments_dict.items():
        try:
            sql = f"COMMENT ON COLUMN {table_name}.{col} IS '{comment}'"
            cur.execute(sql)
            count += 1
        except Exception as e:
            print(f"  跳过 {col}: {e}")

    conn.commit()
    print(f"  字段注释: {count} 个添加成功")


print("=" * 60)
print("  添加表和字段注释")
print("=" * 60)

print(f"\n[1] T_OWNERUNIT")
add_comments("T_OWNERUNIT", OWNERUNIT_COMMENTS)

print(f"\n[2] T_SERVERPART")
add_comments("T_SERVERPART", SERVERPART_COMMENTS)

# 验证
print(f"\n{'='*60}")
print("  验证结果")
print(f"{'='*60}")
for table in ['T_OWNERUNIT', 'T_SERVERPART']:
    cur.execute(f"SELECT COMMENTS FROM USER_TAB_COMMENTS WHERE TABLE_NAME='{table}'")
    row = cur.fetchone()
    print(f"\n{table} 表注释: {row[0] if row and row[0] else '无'}")
    cur.execute(f"SELECT COLUMN_NAME, COMMENTS FROM USER_COL_COMMENTS WHERE TABLE_NAME='{table}'")
    rows = cur.fetchall()
    has = sum(1 for r in rows if r[1])
    print(f"  字段注释: {has}/{len(rows)} 有注释")

cur.close()
conn.close()
print("\n完成！")
