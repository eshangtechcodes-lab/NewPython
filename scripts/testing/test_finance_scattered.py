from __future__ import annotations
# -*- coding: utf-8 -*-
"""验证 Finance 散装接口是否在 Python 端正常注册和响应"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'http://127.0.0.1:8080/EShangApiMain'

tests = [
    ('GET', 'Finance/GetProjectSplitSummary', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GET', 'Finance/GetRoyaltyDateSumReport', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GET', 'Finance/GetProjectShopIncome', {'StatisticsDate':'20250115','ContrastDate':'20240115'}),
    ('GET', 'Finance/GetContractMerchant', {}),
    ('GET', 'Finance/GetAccountReached', {}),
    ('GET', 'Finance/GetShopExpense', {}),
    ('GET', 'Finance/GetReconciliation', {'BUSINESSPROJECT_ID': 1}),
    ('GET', 'Finance/GetRevenueRecognition', {}),
    ('GET', 'Finance/GetProjectPeriodIncome', {'BusinessProjectId':1, 'StatisticsMonth':'202501'}),
    ('GET', 'Finance/GetProjectPeriodAccount', {'BUSINESSPROJECT_ID':1}),
    ('GET', 'Finance/GetMonthAccountDiff', {'ServerpartId':'520', 'StatisticsMonth':'202501'}),
    ('GET', 'Finance/GetPeriodSupplementList', {'BusinessProjectId':1, 'ShopRoyaltyId':'1', 'ServerpartShopId':'1', 'StartDate':'2025-01-01', 'EndDate':'2025-01-31'}),
    ('GET', 'Finance/GetProjectExpenseList', {'BusinessProjectId':1, 'ShopRoyaltyId':'1'}),
    ('GET', 'Finance/GetBankAccountAnalyseList', {'searchMonth':'202501'}),
    ('GET', 'Finance/GetBankAccountAnalyseTreeList', {'searchMonth':'202501'}),
    ('GET', 'Finance/GetContractExcuteAnalysis', {}),
    ('GET', 'Finance/GetAccountCompare', {'StartDate':'2025-01-01','EndDate':'2025-01-31','ServerpartId':'520'}),
    ('GET', 'Finance/GetAnnualAccountList', {'StatisticsYear':'2025','StartDate':'2025-01-01','EndDate':'2025-12-31'}),
    ('GET', 'Finance/SendSMSMessage', {'PhoneNumber':'13800138000','UserName':'test','ProcessCount':1}),
    ('GET', 'Finance/CreateSingleProjectSplit', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GET', 'Finance/SolidMonthProjectSplit', {'StatisticsMonth':'202501'}),
    ('GET', 'Finance/ApprovePeriodAccount', {'ProjectId':1,'ShopRoyaltyId':'1','StartMonth':'202501','EndMonth':'202501'}),
    ('GET', 'Finance/RejectPeriodAccount', {'ProjectId':1,'ShopRoyaltyId':'1','StartMonth':'202501','EndMonth':'202501'}),
]

passed = 0
failed = 0
for method, path, params in tests:
    print(f'=== {path} ===')
    try:
        if method == 'GET':
            r = requests.get(f'{base}/{path}', params=params, timeout=10)
        else:
            r = requests.post(f'{base}/{path}', json=params, timeout=10)
        d = r.json()
        code = d.get('Result_Code')
        if code is not None:
            print(f'  Code={code} ✅')
            passed += 1
        else:
            print(f'  响应异常: {str(d)[:100]} ❌')
            failed += 1
    except Exception as e:
        print(f'  Error: {e} ❌')
        failed += 1

print(f'\n=== 总结 ===')
print(f'通过: {passed}/{len(tests)}, 失败: {failed}/{len(tests)}')
