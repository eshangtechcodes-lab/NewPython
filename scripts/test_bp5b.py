# -*- coding: utf-8 -*-
"""SOP Step 5: 对比 Batch 5b 18个复杂散装接口 Python vs C#"""
import sys, requests, json
sys.stdout.reconfigure(encoding='utf-8')

PY = 'http://localhost:8080/EShangApiMain'
CS = 'http://192.168.1.99:8900/EShangApiMain'
results = []

def compare(name, path, method='GET'):
    try:
        url_py = PY + path
        url_cs = CS + path
        if method == 'GET':
            rpy = requests.get(url_py, timeout=30).json()
            rcs = requests.get(url_cs, timeout=30).json()
        else:
            rpy = requests.post(url_py, json={}, timeout=30).json()
            rcs = requests.post(url_cs, json={}, timeout=30).json()

        py_code = rpy.get('Result_Code')
        cs_code = rcs.get('Result_Code')
        code_ok = py_code == cs_code
        status = 'OK' if code_ok else 'DIFF'
        py_desc = str(rpy.get('Result_Desc', ''))[:40]
        cs_desc = str(rcs.get('Result_Desc', ''))[:40]
        print(f'  [{status}] {name}: PY={py_code}({py_desc}) CS={cs_code}({cs_desc})')
        results.append((name, status))
    except Exception as e:
        print(f'  [ERR] {name}: {e}')
        results.append((name, 'ERR'))

print('=' * 80)
print('Batch 5b 18个复杂散装接口对比验证')
print('=' * 80)

compare('GetMerchantsReceivablesList', '/BusinessProject/GetMerchantsReceivablesList?PageIndex=1&PageSize=5')
compare('GetMerchantsReceivables', '/BusinessProject/GetMerchantsReceivables?MerchantsId=31')
compare('GetBrandReceivables', '/BusinessProject/GetBrandReceivables?ServerpartId=1')
compare('GetMerchantsReceivablesReport', '/BusinessProject/GetMerchantsReceivablesReport')
compare('GetExpenseSummary', '/BusinessProject/GetExpenseSummary?serverpart_ids=1')
compare('GetShopExpenseSummary', '/BusinessProject/GetShopExpenseSummary?serverpartshop_id=1')
compare('GetMonthSummaryList', '/BusinessProject/GetMonthSummaryList?StatisticsMonth=202501')
compare('GetAnnualSplit', '/BusinessProject/GetAnnualSplit?DataType=1&BusinessProjectId=1')
compare('GetProjectAccountList', '/BusinessProject/GetProjectAccountList?PageIndex=1&PageSize=5')
compare('GetProjectAccountTree', '/BusinessProject/GetProjectAccountTree')
compare('GetProjectAccountDetail', '/BusinessProject/GetProjectAccountDetail?BusinessApprovalId=1')
compare('GetAccountWarningList', '/BusinessProject/GetAccountWarningList?ServerpartId=1')
compare('SolidAccountWarningList', '/BusinessProject/SolidAccountWarningList')
compare('SolidProjectRevenue', '/BusinessProject/SolidProjectRevenue?StatisticsMonth=202501')
compare('SolidPeriodAnalysis', '/BusinessProject/SolidPeriodAnalysis', 'POST')
compare('GetPeriodWarningList', '/BusinessProject/GetPeriodWarningList?ServerpartId=1')
compare('ReconfigureProfit', '/BusinessProject/ReconfigureProfit')
compare('GetWillSettleProject', '/BusinessProject/GetWillSettleProject?StartDate=20250101&EndDate=20251231&ServerpartId=1')

print()
print('=' * 80)
ok_count = sum(1 for _, s in results if s == 'OK')
diff_count = sum(1 for _, s in results if s == 'DIFF')
err_count = sum(1 for _, s in results if s == 'ERR')
print(f'汇总: OK={ok_count} DIFF={diff_count} ERR={err_count} / Total={len(results)}')
for name, status in results:
    icon = {'OK': '✅', 'DIFF': '⚠️', 'ERR': '❌'}.get(status, '?')
    print(f'  {icon} {name}')
print('=' * 80)
