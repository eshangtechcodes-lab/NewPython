# -*- coding: utf-8 -*-
"""Merchants 迁移验证脚本"""
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

base_old = 'http://192.168.1.99:8900/EShangApiMain'
base_new = 'http://localhost:8080/EShangApiMain'

def test(name, method, path, **kwargs):
    print(f'\n=== {name} ===')
    try:
        if method == 'POST':
            old = requests.post(f'{base_old}{path}', timeout=15, **kwargs).json()
            new = requests.post(f'{base_new}{path}', timeout=15, **kwargs).json()
        else:
            old = requests.get(f'{base_old}{path}', timeout=15, **kwargs).json()
            new = requests.get(f'{base_new}{path}', timeout=15, **kwargs).json()
        
        old_code = old.get('Result_Code')
        new_code = new.get('Result_Code')
        old_rd = old.get('Result_Data', {})
        new_rd = new.get('Result_Data', {})
        
        old_total = old_rd.get('TotalCount') if isinstance(old_rd, dict) else 'N/A'
        new_total = new_rd.get('TotalCount') if isinstance(new_rd, dict) else 'N/A'
        
        old_list = old_rd.get('List', []) if isinstance(old_rd, dict) else []
        new_list = new_rd.get('List', []) if isinstance(new_rd, dict) else []
        
        code_match = '✅' if old_code == new_code else '❌'
        total_match = '✅' if str(old_total) == str(new_total) else '❌'
        
        print(f'  {code_match} Code: OLD={old_code} NEW={new_code}')
        if old_total != 'N/A':
            print(f'  {total_match} Total: OLD={old_total} NEW={new_total}')
            print(f'  List: OLD={len(old_list)} NEW={len(new_list)}')
    except Exception as e:
        print(f'  ❌ Error: {e}')

# 1. GetCoopMerchantsList
test('GetCoopMerchantsList', 'POST', '/Merchants/GetCoopMerchantsList', json={})

# 2. GetCoopMerchantsDetail
test('GetCoopMerchantsDetail', 'GET', '/Merchants/GetCoopMerchantsDetail?CoopMerchantsId=1')

# 3. GetCoopMerchantsTypeList
test('GetCoopMerchantsTypeList', 'POST', '/Merchants/GetCoopMerchantsTypeList', json={})

# 4. GetCoopMerchantsLinkerList
test('GetCoopMerchantsLinkerList', 'POST', '/Merchants/GetCoopMerchantsLinkerList', json={})

# 5. GetCoopMerchantsLinkerDetail (id=1)
test('GetCoopMerchantsLinkerDetail', 'GET', '/Merchants/GetCoopMerchantsLinkerDetail?CoopMerchantsLinkerId=1')

# 6. GetRTCoopMerchantsList (id=1)
test('GetRTCoopMerchantsList', 'GET', '/Merchants/GetRTCoopMerchantsList?CoopMerchantsId=1')

# 7. GetTradeBrandMerchantsList
test('GetTradeBrandMerchantsList', 'POST', '/Merchants/GetTradeBrandMerchantsList',
     json={"SearchParameter": {"PROVINCE_CODE": 340000}})

print('\n=== DONE ===')
