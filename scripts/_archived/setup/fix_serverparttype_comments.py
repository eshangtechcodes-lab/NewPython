# -*- coding: utf-8 -*-
"""为 T_SERVERPARTTYPE 补充表注释和字段注释"""
import dmPython

conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()

# 表注释
cur.execute("COMMENT ON TABLE T_SERVERPARTTYPE IS '服务区类型表（片区/区域分类）'")
print("表注释已添加")

# 字段注释
comments = {
    'SERVERPARTTYPE_ID': '类型内码',
    'TYPE_NAME': '类型名称',
    'TYPE_INDEX': '排序索引',
    'SERVERPARTSTATICTYPE_ID': '静态类型内码（1000=片区）',
    'PROVINCE_CODE': '省份编码',
    'PARENT_ID': '父级内码',
    'TYPE_CODE': '类型编码',
    'TYPE_DESC': '类型描述',
    'OPERATE_DATE': '操作时间',
    'STAFF_ID': '操作人内码',
    'STAFF_NAME': '操作人姓名',
}
count = 0
for col, comment in comments.items():
    try:
        safe = comment.replace("'", "''")
        cur.execute(f"COMMENT ON COLUMN T_SERVERPARTTYPE.{col} IS '{safe}'")
        count += 1
    except Exception as ex:
        print(f"  跳过 {col}: {ex}")
conn.commit()
print(f"{count} 个字段注释已添加")

# 验证
cur.execute("SELECT COLUMN_NAME, COMMENTS FROM USER_COL_COMMENTS WHERE TABLE_NAME='T_SERVERPARTTYPE'")
for row in cur.fetchall():
    c = row[1] if row[1] else "(无)"
    print(f"  {row[0]:30s} {c}")
conn.close()
print("\n✅ T_SERVERPARTTYPE 注释同步完成")
