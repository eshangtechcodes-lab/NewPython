from __future__ import annotations
# -*- coding: utf-8 -*-
"""SOP Step 2: 调原 API 获取 Finance 散装接口基准数据"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

base = 'http://192.168.1.99:8900/EShangApiMain'

tests = [
    ('GetProjectSplitSummary', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetProjectSummary', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetRevenueSplitSummary', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetProjectMerchantSummary', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetRoyaltyDateSumReport', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetRoyaltyReport', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetProjectShopIncome', {'StatisticsDate':'2025-01-15','ContrastDate':'2024-01-15'}),
    ('GetContractMerchant', {}),
    ('GetAccountReached', {}),
    ('GetShopExpense', {}),
    ('GetReconciliation', {'BUSINESSPROJECT_ID': 1}),
    ('GetRevenueRecognition', {}),
    ('GetProjectPeriodIncome', {'BusinessProjectId':1, 'ShopRoyaltyId':1}),
    ('GetProjectPeriodAccount', {'BUSINESSPROJECT_ID':1, 'SHOPROYALTY_ID':1}),
    ('GetMonthAccountDiff', {'ServerpartId':'520', 'StatisticsMonth':'202501'}),
    ('GetPeriodSupplementList', {'BusinessProjectId':1}),
    ('GetProjectExpenseList', {'BusinessProjectId':1, 'ShopRoyaltyId':1, 'StartMonth':'202501', 'EndMonth':'202501'}),
    ('GetBankAccountAnalyseList', {'searchMonth':'202501'}),
    ('GetBankAccountAnalyseTreeList', {'searchMonth':'202501'}),
    ('GetContractExcuteAnalysis', {'ServerpartIds':'520', 'StatisticsMonth':'202501'}),
    ('GetAccountCompare', {'StartDate':'2025-01-01','EndDate':'2025-01-31'}),
    ('GetAnnualAccountList', {'StatisticsYear':'2025','StartDate':'2025-01-01','EndDate':'2025-12-31'}),
]

for name, params in tests:
    print(f'=== Finance/{name} ===')
    try:
        r = requests.get(f'{base}/Finance/{name}', params=params, timeout=30)
        d = r.json()
        code = d.get('Result_Code')
        rd = d.get('Result_Data', {})
        if isinstance(rd, dict):
            lst = rd.get('List', [])
            total = rd.get('TotalCount', 0)
            print(f'  Code={code}, Total={total}, ListLen={len(lst)}')
            if lst and isinstance(lst[0], dict):
                keys = list(lst[0].keys())
                print(f'  Fields({len(keys)}): {keys[:8]}...' if len(keys) > 8 else f'  Fields({len(keys)}): {keys}')
        else:
            print(f'  Code={code}, Data type={type(rd).__name__}')
    except Exception as e:
        print(f'  Error: {e}')
    print()
