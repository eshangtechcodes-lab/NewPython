from __future__ import annotations
# -*- coding: utf-8 -*-
"""SOP Step 5: 对比验证 Finance ATTACHMENT 接口"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

OLD_BASE = 'http://192.168.1.99:8900/EShangApiMain'
NEW_BASE = 'http://localhost:8080/EShangApiMain'

def compare_response(name, old_data, new_data, ignore_fields=None):
    """对比两个 API 响应"""
    ignore_fields = ignore_fields or set()
    print(f'\n--- {name} ---')
    
    # 对比 Result_Code
    old_code = old_data.get('Result_Code')
    new_code = new_data.get('Result_Code')
    print(f'  Result_Code: old={old_code}, new={new_code} {"✅" if old_code == new_code else "❌"}')
    
    # 对比 Result_Data
    old_rd = old_data.get('Result_Data', {})
    new_rd = new_data.get('Result_Data', {})
    
    if old_rd is None and new_rd is None:
        print(f'  Result_Data: both None ✅')
        return True
    
    # 对比 List 数据
    old_list = old_rd.get('List', []) if isinstance(old_rd, dict) else []
    new_list = new_rd.get('List', []) if isinstance(new_rd, dict) else []
    
    old_total = old_rd.get('TotalCount', 0) if isinstance(old_rd, dict) else 0
    new_total = new_rd.get('TotalCount', 0) if isinstance(new_rd, dict) else 0
    
    print(f'  TotalCount: old={old_total}, new={new_total} {"✅" if old_total == new_total else "❌"}')
    print(f'  List count: old={len(old_list)}, new={len(new_list)} {"✅" if len(old_list) == len(new_list) else "❌"}')
    
    if old_list and new_list:
        # 对比字段列表
        old_keys = set(old_list[0].keys()) - ignore_fields
        new_keys = set(new_list[0].keys()) - ignore_fields
        missing = old_keys - new_keys
        extra = new_keys - old_keys
        if missing:
            print(f'  ❌ 缺失字段: {missing}')
        if extra:
            print(f'  ⚠️ 多余字段: {extra}')
        if not missing and not extra:
            print(f'  字段列表: ✅ 一致 ({len(old_keys)} 个字段)')
        
        # 对比前3条数据
        for i in range(min(3, len(old_list), len(new_list))):
            diffs = []
            for key in old_keys:
                old_val = old_list[i].get(key)
                new_val = new_list[i].get(key)
                # 处理类型差异
                if old_val != new_val:
                    if str(old_val) == str(new_val):
                        continue  # 字符串化相同
                    diffs.append(f'{key}: old={old_val!r}, new={new_val!r}')
            if diffs:
                print(f'  第{i+1}条差异: {"; ".join(diffs[:5])}')
            else:
                print(f'  第{i+1}条: ✅ 一致')
    
    return True


# ===== 测试 1: GetATTACHMENTList (FinanceProinstId=99, DataType=0) =====
print('='*60)
print('测试组 1: GetATTACHMENTList (FinanceProinstId=99, DataType=0)')
params = {'FinanceProinstId': 99, 'DataType': 0}
try:
    old = requests.get(f'{OLD_BASE}/Finance/GetATTACHMENTList', params=params, timeout=10).json()
    new = requests.get(f'{NEW_BASE}/Finance/GetATTACHMENTList', params=params, timeout=10).json()
    compare_response('GetATTACHMENTList(99,0)', old, new)
except Exception as e:
    print(f'Error: {e}')

# ===== 测试 2: GetATTACHMENTList (FinanceProinstId=100, DataType=0) =====
print('\n' + '='*60)
print('测试组 2: GetATTACHMENTList (FinanceProinstId=100, DataType=0)')
params = {'FinanceProinstId': 100, 'DataType': 0}
try:
    old = requests.get(f'{OLD_BASE}/Finance/GetATTACHMENTList', params=params, timeout=10).json()
    new = requests.get(f'{NEW_BASE}/Finance/GetATTACHMENTList', params=params, timeout=10).json()
    compare_response('GetATTACHMENTList(100,0)', old, new)
except Exception as e:
    print(f'Error: {e}')

# ===== 测试 3: GetATTACHMENTList (FinanceProinstId=200, DataType=0) =====
print('\n' + '='*60)
print('测试组 3: GetATTACHMENTList (FinanceProinstId=200, DataType=0)')
params = {'FinanceProinstId': 200, 'DataType': 0}
try:
    old = requests.get(f'{OLD_BASE}/Finance/GetATTACHMENTList', params=params, timeout=10).json()
    new = requests.get(f'{NEW_BASE}/Finance/GetATTACHMENTList', params=params, timeout=10).json()
    compare_response('GetATTACHMENTList(200,0)', old, new)
except Exception as e:
    print(f'Error: {e}')

# ===== 测试 4: GetATTACHMENTDetail =====
print('\n' + '='*60)
print('测试组 4: GetATTACHMENTDetail (ATTACHMENTId=1, DataType=0)')
params = {'ATTACHMENTId': 1, 'DataType': 0}
try:
    old = requests.get(f'{OLD_BASE}/Finance/GetATTACHMENTDetail', params=params, timeout=10).json()
    new = requests.get(f'{NEW_BASE}/Finance/GetATTACHMENTDetail', params=params, timeout=10).json()
    print(f'  Old Result_Code: {old.get("Result_Code")}')
    print(f'  New Result_Code: {new.get("Result_Code")}')
    old_data = old.get('Result_Data', {})
    new_data = new.get('Result_Data', {})
    if old_data and new_data:
        for key in old_data:
            if old_data[key] != new_data.get(key):
                if str(old_data[key]) != str(new_data.get(key)):
                    print(f'  ❌ {key}: old={old_data[key]!r}, new={new_data.get(key)!r}')
                else:
                    continue
        print(f'  对比完成 ✅')
    else:
        print(f'  old_data: {old_data}')
        print(f'  new_data: {new_data}')
except Exception as e:
    print(f'Error: {e}')
