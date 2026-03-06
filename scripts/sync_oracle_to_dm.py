# -*- coding: utf-8 -*-
"""
自动同步达梦与Oracle数据，确保数据一致
对于大表只同步缺失的数据（增量同步）
"""
import sys
sys.path.insert(0, r"D:\Projects\Python\eshang_api")

import oracledb
try:
    oracledb.init_oracle_client(lib_dir=r"D:\instantclient_19_29")
except:
    pass

import dmPython
from config import settings

def sync_table_full(table_name, oracle_schema, batch_size=10000):
    """全量同步一张表到达梦（先清空再导入）"""
    # 连Oracle
    ora_conn = oracledb.connect(user="highway_exchange", password="qrwl",
                                dsn="127.0.0.1:1521/orcl")
    ora_cur = ora_conn.cursor()
    
    # 查Oracle总数
    ora_cur.execute(f"SELECT COUNT(*) FROM {oracle_schema}.{table_name}")
    ora_total = ora_cur.fetchone()[0]
    
    # 查字段
    ora_cur.execute(f"SELECT * FROM {oracle_schema}.{table_name} WHERE ROWNUM = 1")
    columns = [desc[0] for desc in ora_cur.description]
    
    # 连达梦
    dm_conn = dmPython.connect(user=settings.DM_USER, password=settings.DM_PASSWORD,
                               server=settings.DM_HOST, port=settings.DM_PORT)
    dm_cur = dm_conn.cursor()
    
    # 查达梦当前数据量
    dm_cur.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
    dm_total = dm_cur.fetchone()[0]
    
    if dm_total == ora_total:
        print(f"  ✅ {table_name}: 数据已一致 ({dm_total:,} 条), 跳过")
        ora_conn.close()
        dm_conn.close()
        return True
    
    print(f"  🔄 {table_name}: Oracle {ora_total:,} 条, 达梦 {dm_total:,} 条, 开始全量同步...")
    
    # 清空达梦表
    dm_cur.execute(f"DELETE FROM \"{table_name}\"")
    dm_conn.commit()
    
    # 分批读取Oracle数据并写入达梦
    placeholders = ", ".join(["?" for _ in columns])
    col_list = ", ".join([f"\"{c}\"" for c in columns])
    insert_sql = f"INSERT INTO \"{table_name}\" ({col_list}) VALUES ({placeholders})"
    
    # 使用Oracle分页
    offset = 0
    imported = 0
    while offset < ora_total:
        ora_cur.execute(f"""
            SELECT * FROM (
                SELECT a.*, ROWNUM rnum FROM {oracle_schema}.{table_name} a
                WHERE ROWNUM <= {offset + batch_size}
            ) WHERE rnum > {offset}
        """)
        rows = ora_cur.fetchall()
        if not rows:
            break
        
        # 去掉rnum列（最后一列是ROWNUM别名）
        clean_rows = [row[:-1] for row in rows]
        
        try:
            dm_cur.executemany(insert_sql, clean_rows)
            dm_conn.commit()
            imported += len(clean_rows)
            pct = imported * 100 // ora_total
            print(f"    ... {imported:>10,}/{ora_total:>10,} ({pct}%)")
        except Exception as e:
            print(f"    ❌ 插入失败 offset={offset}: {e}")
            dm_conn.rollback()
            # 单条插入失败行
            for row in clean_rows:
                try:
                    dm_cur.execute(insert_sql, row)
                    dm_conn.commit()
                    imported += 1
                except:
                    pass
        
        offset += batch_size
    
    # 验证
    dm_cur.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
    dm_final = dm_cur.fetchone()[0]
    
    ora_conn.close()
    dm_conn.close()
    
    if dm_final == ora_total:
        print(f"  ✅ {table_name}: 同步完成! {dm_final:,} 条")
        return True
    else:
        print(f"  ⚠️ {table_name}: 同步后 {dm_final:,} 条 (Oracle {ora_total:,} 条, 差 {ora_total - dm_final:,} 条)")
        return False

def main():
    # 需要全量同步的表（按重要性排序）
    # 格式: (表名, Oracle schema, Oracle行数)
    tables_to_sync = [
        # 先同步小表
        ("T_MEETING",                  "HIGHWAY_STORAGE",     70994),
        ("T_ANALYSISRULE",             "PLATFORM_DASHBOARD",  33),
        ("T_USERDEFINEDTYPE",          "HIGHWAY_STORAGE",     9274),
        ("T_PROVINCEREVENUE",          "PLATFORM_DASHBOARD",  19261),
        ("T_ACCOUNTRECEIVABLE",        "PLATFORM_DASHBOARD",  12112),
        ("T_SECTIONFLOWMONTH",         "HIGHWAY_SELLDATA",    10463),
        ("T_PERIODMONTHPROFIT",        "PLATFORM_DASHBOARD",  9847),
        ("T_BAYONETSTAYDAILY_AH",      "HIGHWAY_SELLDATA",    7363),
        ("T_STATEFEEDBACK",            "HIGHWAY_STORAGE",     6743),
        ("T_SENTENCE",                 "PLATFORM_DASHBOARD",  5899),
        ("T_BUSINESSWARNING",          "PLATFORM_DASHBOARD",  24360),
        ("T_RTMEMBERSHIP",             "MOBILESERVICE_PLATFORM", 22951),
        ("T_SERVERPARTSHOP_LOG",       "HIGHWAY_STORAGE",     21858),
        ("T_YSSELLMASTER_YES",         "HIGHWAY_SELLDATA",    38252),
        ("T_MERCHANTSPLIT",            "PLATFORM_DASHBOARD",  45959),
        ("T_REVENUEMONTHLY",           "PLATFORM_DASHBOARD",  66233),
        ("T_YSSELLDETAILS_YES",        "HIGHWAY_SELLDATA",    80374),
        ("T_WEATHER",                  "HIGHWAY_STORAGE",     110451),
        ("T_UREAMASTER",               "PLATFORM_DASHBOARD",  114934),
        ("T_PATROLDAILY",              "PLATFORM_DASHBOARD",  139903),
        ("T_ACCOUNTRECDETAIL",         "PLATFORM_DASHBOARD",  145344),
        ("T_PROFITCONTRIBUTE",         "PLATFORM_DASHBOARD",  149590),
        ("T_BAYONETPROVINCEMONTH_AH",  "HIGHWAY_SELLDATA",    152866),
        ("T_BUSINESSREVENUE",          "PLATFORM_DASHBOARD",  156956),
        ("T_CONSUMPTIONLEVEL",         "PLATFORM_DASHBOARD",  161219),
        ("T_CUSTOMER_SHOP",            "PLATFORM_DASHBOARD",  235683),
        ("T_WATERMASTER",              "PLATFORM_DASHBOARD",  310494),
        ("T_MOBILEPAYSHARE",           "PLATFORM_DASHBOARD",  480399),
        ("T_PATROLDETAIL",             "HIGHWAY_STORAGE",     522554),
        ("T_BAYONETWARNING",           "PLATFORM_DASHBOARD",  600659),
        # 大表
        ("T_ENDACCOUNT",               "HIGHWAY_SELLDATA",    753264),
        ("T_TRANSACTIONANALYSIS",      "PLATFORM_DASHBOARD",  755083),
        ("T_BAYONETHOURMONTH_AH",      "HIGHWAY_SELLDATA",    1043787),
        ("T_MONTHLYREVENUE",           "PLATFORM_DASHBOARD",  1261854),
        ("T_BAYONETDAILY_AH",          "HIGHWAY_SELLDATA",    1345491),
        ("T_BAYONETOWNERMONTH_AH",     "HIGHWAY_SELLDATA",    1462830),
        ("T_COMMODITYSALE",            "HIGHWAY_EXCHANGE",    1490070),
        ("T_HOLIDAYREVENUE",           "PLATFORM_DASHBOARD",  1542425),
        ("T_REVENUEDAILY",             "PLATFORM_DASHBOARD",  1730536),
        ("T_GASORDERINFO",             "PLATFORM_DASHBOARD",  2045629),
        # 超大表最后
        ("T_CUSTOMERGROUP",            "PLATFORM_DASHBOARD",  2703791),
        ("T_SECTIONFLOW",              "HIGHWAY_SELLDATA",    6455832),
        ("T_BAYONETOWMONTHLY_AH",      "HIGHWAY_SELLDATA",    None),  # 需检查
    ]
    
    print("=" * 100)
    print("  达梦数据全量同步（Oracle → 达梦）")
    print("=" * 100)
    print(f"  共 {len(tables_to_sync)} 张表待同步")
    print()
    
    success = 0
    fail = 0
    
    for i, (tname, schema, _) in enumerate(tables_to_sync, 1):
        print(f"\n[{i}/{len(tables_to_sync)}]")
        try:
            ok = sync_table_full(tname, schema)
            if ok:
                success += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  ❌ {tname}: 同步异常: {e}")
            fail += 1
    
    print(f"\n{'=' * 100}")
    print(f"  同步完成: ✅ {success} 张成功, ❌ {fail} 张失败")
    print(f"{'=' * 100}")

if __name__ == "__main__":
    main()
