from __future__ import annotations
# -*- coding: utf-8 -*-
"""确认 ATTACHMENT 表在达梦中是否存在"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import dmPython
    conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='192.168.1.99', port=5236)
    cur = conn.cursor()
    
    # 检查 T_ATTACHMENT 是否存在于 RUNNING 和 STORAGE schema
    tables_to_check = [
        'T_ATTACHMENT',
        'CONTRACT_RUNNING.T_ATTACHMENT',
        'CONTRACT_STORAGE.T_ATTACHMENT', 
        'FINANCE_RUNNING.T_ATTACHMENT',
        'FINANCE_STORAGE.T_ATTACHMENT',
    ]
    
    for t in tables_to_check:
        try:
            cur.execute(f'SELECT COUNT(*) FROM {t}')
            count = cur.fetchone()[0]
            print(f'  ✅ {t:45s} {count:>8} 条')
        except Exception as e:
            print(f'  ❌ {t:45s} {str(e)[:60]}')
    
    # 查找所有包含 ATTACHMENT 的表
    print('\n=== 搜索所有包含 ATTACHMENT 的表 ===')
    cur.execute("""
        SELECT OWNER, TABLE_NAME 
        FROM ALL_TABLES 
        WHERE TABLE_NAME LIKE '%ATTACHMENT%'
        ORDER BY OWNER, TABLE_NAME
    """)
    for row in cur.fetchall():
        print(f'  {row[0]}.{row[1]}')
    
    conn.close()
except Exception as e:
    print(f'Error: {e}')
