# -*- coding: utf-8 -*-
"""
直连达梦+Oracle 核验数据同步完整性
达梦: dmPython
Oracle: sqlplus 命令行（避免 thin 模式不兼容问题）
"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import DatabaseHelper

# 达梦连接
dm = DatabaseHelper(db_type="dm")
print("达梦连接测试:", "OK" if dm.test_connection() else "FAIL")

def count_dm(table):
    """达梦查表行数"""
    try:
        rows = dm.execute_query(f'SELECT COUNT(1) AS CNT FROM "{table}"')
        return rows[0]["CNT"] if rows else 0
    except Exception as e:
        return f"ERR:{str(e)[:60]}"

def count_ora(table, schema):
    """Oracle 通过 sqlplus 查行数"""
    try:
        sql = f"SELECT COUNT(1) FROM {schema}.{table};"
        cmd = f'echo {sql} | sqlplus -S highway_exchange/qrwl@orcl'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15, 
                               cwd="D:\\app\\YSKJ02\\product\\11.2.0\\dbhome_1\\BIN")
        output = result.stdout.strip()
        # 从输出中提取数字
        for line in output.split('\n'):
            line = line.strip()
            if line.isdigit():
                return int(line)
        return f"OUT:{output[:40]}"
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERR:{str(e)[:40]}"

print("\n" + "=" * 100)
print("数据同步完整性核验 - 达梦 vs Oracle")
print("=" * 100)

TABLES = [
    # (表名, Oracle schema, 说明, 关联接口)
    ("T_EXAMINE", "HIGHWAY_STORAGE", "考核表", "GetEXAMINEList"),
    ("T_EXAMINEDETAIL", "HIGHWAY_STORAGE", "考核明细子表", "WeChat_GetExamineDetail（空）"),
    ("T_MEETING", "HIGHWAY_STORAGE", "晨会表", "GetMEETINGList"),
    ("T_PATROL", "HIGHWAY_STORAGE", "巡检表", "GetPATROLList"),
    ("T_ANALYSISINS", "HIGHWAY_STORAGE", "分析表", "GetANALYSISINSList"),
    ("T_BUDGETPROJECT_AH", "FINANCE_STORAGE", "预算项目表", "GetBUDGETPROJECT_AHList"),
    ("T_BUDGETEXPENSE", "FINANCE_STORAGE", "预算费用表", "GetBudgetExpenseList（空）"),
    ("T_BUDGETPROJECTDETAIL", "FINANCE_STORAGE", "预算项目明细", "GetBudgetProjectDetailList（空）"),
    ("T_SERVERPART", "HIGHWAY_STORAGE", "服务区表", "GetServerpartList（TODO）"),
    ("T_SERVERPARTSHOP", "HIGHWAY_STORAGE", "门店表", "GetBrandAnalysis"),
    ("T_BRAND", "COOP_MERCHANT", "品牌表", "GetBrandAnalysis"),
    ("T_AUTOSTATISTICS", "COOP_MERCHANT", "经营业态表", "GetBusinessTradeList"),
    ("T_SERVERPARTTYPE", "HIGHWAY_STORAGE", "片区类型表", "GetSPRegionList"),
    ("T_SHOPCOUNT", "HIGHWAY_STORAGE", "门店数量表", "GetShopCountList"),
    ("T_REGISTERCOMPACT", "CONTRACT_STORAGE", "合同登记表", "ContractAnalysis"),
    ("T_SHOPREVENUE", "HIGHWAY_STORAGE", "门店营收表", "GetShopRevenue（T差异）"),
]

print(f"\n{'表名':<28s} {'Schema':<20s} {'达梦':>10s} {'Oracle':>10s} {'差异':>10s} 关联接口")
print("-" * 120)

diff_list = []
for table, schema, desc, api in TABLES:
    dm_cnt = count_dm(table)
    ora_cnt = count_ora(table, schema)

    if isinstance(dm_cnt, int) and isinstance(ora_cnt, int):
        if dm_cnt == ora_cnt:
            diff = "✅一致"
        elif dm_cnt == 0:
            diff = f"❌未同步"
            diff_list.append((table, schema, dm_cnt, ora_cnt, api))
        elif dm_cnt < ora_cnt:
            diff = f"⚠️差{ora_cnt-dm_cnt}"
            diff_list.append((table, schema, dm_cnt, ora_cnt, api))
        else:
            diff = f"➕多{dm_cnt-ora_cnt}"
    else:
        diff = "❓异常"
        diff_list.append((table, schema, dm_cnt, ora_cnt, api))

    print(f"{table:<28s} {schema:<20s} {str(dm_cnt):>10s} {str(ora_cnt):>10s} {diff:>10s} {api}")

if diff_list:
    print(f"\n{'='*100}")
    print(f"需要补充同步的表 ({len(diff_list)}个):")
    for table, schema, dm_cnt, ora_cnt, api in diff_list:
        print(f"  {schema}.{table}: 达梦={dm_cnt}, Oracle={ora_cnt}  -> {api}")
else:
    print(f"\n✅ 所有表数据完全一致！")

print(f"\n{'='*100}")
