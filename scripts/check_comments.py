"""检查达梦表注释和字段注释"""
import dmPython

conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='192.168.1.99', port=5236)
cur = conn.cursor()

for table in ['T_OWNERUNIT', 'T_SERVERPART']:
    print(f"\n{'='*60}")
    print(f"  {table}")
    print(f"{'='*60}")
    
    # 表注释
    cur.execute(f"SELECT COMMENTS FROM USER_TAB_COMMENTS WHERE TABLE_NAME='{table}'")
    row = cur.fetchone()
    print(f"表注释: {row[0] if row and row[0] else '无'}")
    
    # 字段注释
    cur.execute(f"SELECT COLUMN_NAME, COMMENTS FROM USER_COL_COMMENTS WHERE TABLE_NAME='{table}' ORDER BY COLUMN_ID")
    rows = cur.fetchall()
    has_comment = sum(1 for r in rows if r[1])
    print(f"字段注释: {has_comment}/{len(rows)} 有注释")
    for r in rows:
        print(f"  {r[0]:35s} {r[1] or '(无注释)'}")

cur.close()
conn.close()
