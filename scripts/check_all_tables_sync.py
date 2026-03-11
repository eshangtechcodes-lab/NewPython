# -*- coding: utf-8 -*-
"""
检查所有同步表在 Oracle 和达梦端的行数是否一致
"""
import sys
sys.path.insert(0, r"D:\Projects\Python\eshang_api")

import oracledb
try:
    oracledb.init_oracle_client(lib_dir=r"D:\instantclient_19_29")
except:
    pass

import dmPython

# ========== 连接配置 ==========
ORACLE_DSN = "192.168.1.99:1521/orcl"
ORACLE_USER = "highway_exchange"
ORACLE_PWD = "qrwl"

DM_HOST = "192.168.1.99"
DM_PORT = 5236
DM_USER = "NEWPYTHON"
DM_PWD = "NewPython@2025"

# 所有需要同步的表: (表名, Oracle schema)
TABLES = [
    ("T_MEETING",                  "HIGHWAY_STORAGE"),
    ("T_ANALYSISRULE",             "PLATFORM_DASHBOARD"),
    ("T_USERDEFINEDTYPE",          "HIGHWAY_STORAGE"),
    ("T_PROVINCEREVENUE",          "PLATFORM_DASHBOARD"),
    ("T_ACCOUNTRECEIVABLE",        "PLATFORM_DASHBOARD"),
    ("T_SECTIONFLOWMONTH",         "HIGHWAY_SELLDATA"),
    ("T_PERIODMONTHPROFIT",        "PLATFORM_DASHBOARD"),
    ("T_BAYONETSTAYDAILY_AH",      "HIGHWAY_SELLDATA"),
    ("T_STATEFEEDBACK",            "HIGHWAY_STORAGE"),
    ("T_SENTENCE",                 "PLATFORM_DASHBOARD"),
    ("T_BUSINESSWARNING",          "PLATFORM_DASHBOARD"),
    ("T_RTMEMBERSHIP",             "MOBILESERVICE_PLATFORM"),
    ("T_SERVERPARTSHOP_LOG",       "HIGHWAY_STORAGE"),
    ("T_YSSELLMASTER_YES",         "HIGHWAY_SELLDATA"),
    ("T_MERCHANTSPLIT",            "PLATFORM_DASHBOARD"),
    ("T_REVENUEMONTHLY",           "PLATFORM_DASHBOARD"),
    ("T_YSSELLDETAILS_YES",        "HIGHWAY_SELLDATA"),
    ("T_WEATHER",                  "HIGHWAY_STORAGE"),
    ("T_UREAMASTER",               "PLATFORM_DASHBOARD"),
    ("T_PATROLDAILY",              "PLATFORM_DASHBOARD"),
    ("T_ACCOUNTRECDETAIL",         "PLATFORM_DASHBOARD"),
    ("T_PROFITCONTRIBUTE",         "PLATFORM_DASHBOARD"),
    ("T_BAYONETPROVINCEMONTH_AH",  "HIGHWAY_SELLDATA"),
    ("T_BUSINESSREVENUE",          "PLATFORM_DASHBOARD"),
    ("T_CONSUMPTIONLEVEL",         "PLATFORM_DASHBOARD"),
    ("T_CUSTOMER_SHOP",            "PLATFORM_DASHBOARD"),
    ("T_WATERMASTER",              "PLATFORM_DASHBOARD"),
    ("T_MOBILEPAYSHARE",           "PLATFORM_DASHBOARD"),
    ("T_PATROLDETAIL",             "HIGHWAY_STORAGE"),
    ("T_BAYONETWARNING",           "PLATFORM_DASHBOARD"),
    ("T_ENDACCOUNT",               "HIGHWAY_SELLDATA"),
    ("T_TRANSACTIONANALYSIS",      "PLATFORM_DASHBOARD"),
    ("T_BAYONETHOURMONTH_AH",      "HIGHWAY_SELLDATA"),
    ("T_MONTHLYREVENUE",           "PLATFORM_DASHBOARD"),
    ("T_BAYONETDAILY_AH",          "HIGHWAY_SELLDATA"),
    ("T_BAYONETOWNERMONTH_AH",     "HIGHWAY_SELLDATA"),
    ("T_COMMODITYSALE",            "HIGHWAY_EXCHANGE"),
    ("T_HOLIDAYREVENUE",           "PLATFORM_DASHBOARD"),
    ("T_REVENUEDAILY",             "PLATFORM_DASHBOARD"),
    ("T_GASORDERINFO",             "PLATFORM_DASHBOARD"),
    ("T_CUSTOMERGROUP",            "PLATFORM_DASHBOARD"),
    ("T_SECTIONFLOW",              "HIGHWAY_SELLDATA"),
    ("T_BAYONETOWMONTHLY_AH",      "HIGHWAY_SELLDATA"),
]


def main():
    print("=" * 100)
    print("  Oracle ↔ 达梦 全表行数对比检查")
    print("=" * 100)

    # 连接 Oracle
    print("\n连接 Oracle...")
    ora_conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PWD, dsn=ORACLE_DSN)
    ora_cur = ora_conn.cursor()

    # 连接达梦
    print("连接达梦...")
    dm_conn = dmPython.connect(user=DM_USER, password=DM_PWD,
                               server=DM_HOST, port=DM_PORT)
    dm_cur = dm_conn.cursor()

    print(f"\n{'序号':<5} {'表名':<35} {'Oracle':>12} {'达梦':>12} {'差异':>10} {'状态':<6}")
    print("-" * 100)

    synced = 0
    not_synced = 0
    errors = 0
    need_sync_tables = []

    for i, (table, schema) in enumerate(TABLES, 1):
        ora_count = None
        dm_count = None

        # 查 Oracle
        try:
            ora_cur.execute(f"SELECT COUNT(*) FROM {schema}.{table}")
            ora_count = ora_cur.fetchone()[0]
        except Exception as e:
            ora_count = f"ERR"

        # 查达梦
        try:
            dm_cur.execute(f'SELECT COUNT(*) FROM "{table}"')
            dm_count = dm_cur.fetchone()[0]
        except Exception as e:
            dm_count = f"ERR"

        # 判断状态
        if isinstance(ora_count, int) and isinstance(dm_count, int):
            diff = ora_count - dm_count
            if diff == 0:
                status = "✅"
                synced += 1
            else:
                status = "❌"
                not_synced += 1
                need_sync_tables.append((table, schema, ora_count, dm_count, diff))
            print(f"{i:<5} {table:<35} {ora_count:>12,} {dm_count:>12,} {diff:>+10,} {status}")
        else:
            status = "⚠️"
            errors += 1
            print(f"{i:<5} {table:<35} {str(ora_count):>12} {str(dm_count):>12} {'---':>10} {status}")

    print("-" * 100)
    print(f"\n总计: {len(TABLES)} 张表")
    print(f"  ✅ 已同步: {synced} 张")
    print(f"  ❌ 未同步: {not_synced} 张")
    print(f"  ⚠️ 异常:   {errors} 张")

    if need_sync_tables:
        print(f"\n{'=' * 100}")
        print(f"  需要同步的表:")
        print(f"{'=' * 100}")
        for table, schema, ora_c, dm_c, diff in need_sync_tables:
            print(f"  {table:<35} Oracle={ora_c:>12,}  达梦={dm_c:>12,}  差={diff:>+10,}")

    ora_conn.close()
    dm_conn.close()


if __name__ == "__main__":
    main()
