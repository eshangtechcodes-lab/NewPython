# -*- coding: utf-8 -*-
"""
对比达梦和Oracle中已同步表的数据量，找出数据不一致的表
Oracle 使用 Thick 模式（instantclient_19_29）
"""
import sys
sys.path.insert(0, r"D:\Projects\Python\eshang_api")

# 初始化 Oracle Thick 模式
import oracledb
try:
    oracledb.init_oracle_client(lib_dir=r"D:\instantclient_19_29")
    print("Oracle Thick 模式初始化成功")
except Exception as e:
    print(f"Oracle Thick 初始化: {e}")

def get_dm_tables():
    """获取达梦中所有表及行数"""
    from core.database import DatabaseHelper
    db = DatabaseHelper(db_type="dm")
    rows = db.execute_query("""
        SELECT TABLE_NAME FROM ALL_TABLES 
        WHERE OWNER = 'NEWPYTHON' 
        ORDER BY TABLE_NAME
    """)
    result = {}
    for r in rows:
        tname = r['TABLE_NAME']
        try:
            cnt = db.execute_query(f"SELECT COUNT(*) AS CNT FROM \"{tname}\"")
            result[tname] = cnt[0]['CNT']
        except:
            result[tname] = -1
    return result

def get_oracle_counts(table_names, schemas):
    """批量从Oracle查询表的行数（Thick模式）"""
    conn = oracledb.connect(user="highway_exchange", password="qrwl",
                            dsn="127.0.0.1:1521/orcl")
    cur = conn.cursor()
    
    result = {}
    for tname in table_names:
        for schema in schemas:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {schema}.{tname}")
                count = cur.fetchone()[0]
                result[tname] = (count, schema)
                break
            except:
                continue
    
    conn.close()
    return result

def main():
    print("=" * 100)
    print("  达梦 vs Oracle 数据量对比")
    print("=" * 100)
    
    # 1. 获取达梦表
    print("\n正在查询达梦表...")
    dm_tables = get_dm_tables()
    print(f"达梦表总数: {len(dm_tables)}")
    
    # 2. Oracle schema 搜索顺序
    schemas = [
        "HIGHWAY_STORAGE", "HIGHWAY_SELLDATA", "HIGHWAY_EXCHANGE",
        "CONTRACT_STORAGE", "FINANCE_STORAGE", "PLATFORM_DASHBOARD",
        "MOBILESERVICE_PLATFORM", "COMMERCIALAPI_STORAGE"
    ]
    
    # 3. 批量查Oracle
    print("正在查询Oracle表（这可能需要几分钟...）")
    ora_data = get_oracle_counts(list(dm_tables.keys()), schemas)
    print(f"Oracle中找到: {len(ora_data)} 张表\n")
    
    # 4. 分类
    matched = []
    partial = []
    dm_only = []
    dm_more = []
    
    for tname, dm_count in sorted(dm_tables.items()):
        if tname in ora_data:
            ora_count, schema = ora_data[tname]
            if dm_count == ora_count:
                matched.append((tname, dm_count, ora_count, schema))
            elif dm_count < ora_count:
                diff_pct = round((ora_count - dm_count) * 100 / max(ora_count, 1), 1)
                partial.append((tname, dm_count, ora_count, schema, diff_pct))
            else:
                dm_more.append((tname, dm_count, ora_count, schema))
        else:
            dm_only.append((tname, dm_count))
    
    # 输出结果
    print(f"{'─' * 100}")
    print(f"  ✅ 数据完全一致: {len(matched)} 张表")
    print(f"{'─' * 100}")
    for tname, dm, ora, schema in matched:
        print(f"  {tname:45s} DM={dm:>10,}  ORA={ora:>10,}  ({schema})")
    
    print(f"\n{'─' * 100}")
    print(f"  ⚠️ 数据不完整（达梦 < Oracle）: {len(partial)} 张表  ← 需要补同步")
    print(f"{'─' * 100}")
    for tname, dm, ora, schema, pct in sorted(partial, key=lambda x: -x[4]):
        missing = ora - dm
        print(f"  {tname:45s} DM={dm:>10,}  ORA={ora:>10,}  缺 {missing:>10,} 条({pct}%)  ({schema})")
    
    if dm_more:
        print(f"\n{'─' * 100}")
        print(f"  ❓ 达梦多于Oracle: {len(dm_more)} 张表")
        print(f"{'─' * 100}")
        for tname, dm, ora, schema in dm_more:
            print(f"  {tname:45s} DM={dm:>10,}  ORA={ora:>10,}  ({schema})")
    
    if dm_only:
        print(f"\n{'─' * 100}")
        print(f"  📦 Oracle中未找到: {len(dm_only)} 张表（可能是达梦专有）")
        print(f"{'─' * 100}")
        for tname, dm in dm_only:
            print(f"  {tname:45s} DM={dm:>10,}")
    
    # 汇总
    total_partial_ora = sum(o for _, _, o, _, _ in partial)
    total_partial_dm = sum(d for _, d, _, _, _ in partial)
    total_matched_dm = sum(d for _, d, _, _ in matched)
    
    print(f"\n{'=' * 100}")
    print(f"  汇总统计")
    print(f"{'=' * 100}")
    print(f"  达梦总表数:        {len(dm_tables)}")
    print(f"  Oracle找到:        {len(ora_data)} 张")
    print(f"  ✅ 完全一致:       {len(matched)} 张 ({total_matched_dm:,} 条)")
    print(f"  ⚠️ 数据不完整:    {len(partial)} 张 (达梦 {total_partial_dm:,} 条 / Oracle {total_partial_ora:,} 条, 缺 {total_partial_ora - total_partial_dm:,} 条)")
    if dm_more:
        print(f"  ❓ 达梦多于Oracle: {len(dm_more)} 张")
    print(f"  📦 Oracle未找到:   {len(dm_only)} 张")

if __name__ == "__main__":
    main()
