# -*- coding: utf-8 -*-
"""查询达梦 NEWPYTHON 用户下所有已有表和数据量"""
import dmPython

print("=" * 60)
print("  达梦 NEWPYTHON 用户 - 表清单")
print("=" * 60)

try:
    conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='192.168.1.99', port=5236)
    cur = conn.cursor()

    # 查询当前用户下所有表
    cur.execute("""
        SELECT TABLE_NAME 
        FROM USER_TABLES 
        ORDER BY TABLE_NAME
    """)
    tables = [row[0] for row in cur.fetchall()]
    print(f"\n共 {len(tables)} 张表:\n")

    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            count = cur.fetchone()[0]
            print(f"  {'✅' if count > 0 else '⚠️'} {t:40s} {count:>8} 条")
        except Exception as ex:
            print(f"  ❌ {t:40s} 查询失败: {ex}")

    cur.close()
    conn.close()
    print(f"\n{'=' * 60}")
except Exception as ex:
    print(f"❌ 连接失败: {ex}")
