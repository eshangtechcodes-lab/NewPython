from __future__ import annotations
# -*- coding: utf-8 -*-
"""SOP Step 2: 调原 API 获取 ATTACHMENT 基准数据"""
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

base_url = 'http://192.168.1.99:8900/EShangApiMain'

# 1. GetATTACHMENTList (DataType=0 RUNNING, FinanceProinstId=1)
print('=== GetATTACHMENTList (FinanceProinstId=1, DataType=0 RUNNING) ===')
try:
    r = requests.get(f'{base_url}/Finance/GetATTACHMENTList', params={'FinanceProinstId': 1, 'DataType': 0}, timeout=10)
    data = r.json()
    print(f'Result_Code: {data.get("Result_Code")}')
    rd = data.get('Result_Data', {})
    print(f'TotalCount: {rd.get("TotalCount")}')
    lst = rd.get('List', [])
    print(f'List count: {len(lst)}')
    if lst:
        print(f'First item keys: {list(lst[0].keys())}')
        print(f'First item: {json.dumps(lst[0], ensure_ascii=False, default=str)}')
except Exception as e:
    print(f'Error: {e}')

# 2. GetATTACHMENTList (DataType=0, FinanceProinstId=0 查全部)
print()
print('=== GetATTACHMENTList (FinanceProinstId=0, DataType=0) ===')
try:
    r = requests.get(f'{base_url}/Finance/GetATTACHMENTList', params={'FinanceProinstId': 0, 'DataType': 0}, timeout=10)
    data = r.json()
    print(f'Result_Code: {data.get("Result_Code")}')
    rd = data.get('Result_Data', {})
    print(f'TotalCount: {rd.get("TotalCount")}')
    lst = rd.get('List', [])
    print(f'List count: {len(lst)}')
    if lst:
        print(f'First item keys: {list(lst[0].keys())}')
        print(f'First item: {json.dumps(lst[0], ensure_ascii=False, default=str)}')
except Exception as e:
    print(f'Error: {e}')

# 3. GetATTACHMENTList (DataType=1 STORAGE)
print()
print('=== GetATTACHMENTList (FinanceProinstId=0, DataType=1 STORAGE) ===')
try:
    r = requests.get(f'{base_url}/Finance/GetATTACHMENTList', params={'FinanceProinstId': 0, 'DataType': 1}, timeout=10)
    data = r.json()
    print(f'Result_Code: {data.get("Result_Code")}')
    rd = data.get('Result_Data', {})
    print(f'TotalCount: {rd.get("TotalCount")}')
    lst = rd.get('List', [])
    print(f'List count: {len(lst)}')
    if lst:
        print(f'First item keys: {list(lst[0].keys())}')
        print(f'First item: {json.dumps(lst[0], ensure_ascii=False, default=str)}')
except Exception as e:
    print(f'Error: {e}')

# 4. GetATTACHMENTDetail
print()
print('=== GetATTACHMENTDetail (ATTACHMENTId=1, DataType=0) ===')
try:
    r = requests.get(f'{base_url}/Finance/GetATTACHMENTDetail', params={'ATTACHMENTId': 1, 'DataType': 0}, timeout=10)
    data = r.json()
    print(f'Result_Code: {data.get("Result_Code")}')
    rd = data.get('Result_Data', {})
    print(f'Result_Data: {json.dumps(rd, ensure_ascii=False, default=str)}')
except Exception as e:
    print(f'Error: {e}')
