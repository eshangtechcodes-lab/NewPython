# -*- coding: utf-8 -*-
"""SOP Step 5: 对比 Batch 5a 8个散装接口 Python vs C#"""
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

PY = 'http://localhost:8080/EShangApiMain'
CS = 'http://192.168.1.99:8900/EShangApiMain'

results = []

def compare(name, path, method='GET', body=None, params=None):
    """对比 Python 和 C# 接口"""
    try:
        url_py = PY + path
        url_cs = CS + path
        if params:
            url_py += '?' + params
            url_cs += '?' + params

        if method == 'GET':
            rpy = requests.get(url_py, timeout=30).json()
            rcs = requests.get(url_cs, timeout=30).json()
        else:
            rpy = requests.post(url_py, json=body, timeout=30).json()
            rcs = requests.post(url_cs, json=body, timeout=30).json()

        py_code = rpy.get('Result_Code')
        cs_code = rcs.get('Result_Code')
        py_data = rpy.get('Result_Data')
        cs_data = rcs.get('Result_Data')

        # 比较 Code
        code_ok = py_code == cs_code

        # 比较 TotalCount
        py_tc = py_data.get('TotalCount') if isinstance(py_data, dict) else None
        cs_tc = cs_data.get('TotalCount') if isinstance(cs_data, dict) else None

        # 比较首条数据字段
        py_list = py_data.get('DataList') or py_data.get('List', []) if isinstance(py_data, dict) else []
        cs_list = cs_data.get('DataList') or cs_data.get('List', []) if isinstance(cs_data, dict) else []

        status = '✅' if code_ok else '❌'
        print(f'{status} [{name}] PY={py_code} CS={cs_code} | PY_TC={py_tc} CS_TC={cs_tc} | PY_rows={len(py_list)} CS_rows={len(cs_list)}')

        # 打印首条数据对比
        if py_list and cs_list:
            py0 = py_list[0]
            cs0 = cs_list[0]
            print(f'   PY[0]: {json.dumps(py0, ensure_ascii=False, default=str)[:120]}')
            print(f'   CS[0]: {json.dumps(cs0, ensure_ascii=False, default=str)[:120]}')
        elif py_list:
            print(f'   PY[0]: {json.dumps(py_list[0], ensure_ascii=False, default=str)[:120]}')
            print(f'   CS: 无数据')
        elif cs_list:
            print(f'   PY: 无数据')
            print(f'   CS[0]: {json.dumps(cs_list[0], ensure_ascii=False, default=str)[:120]}')

        results.append((name, status))
    except Exception as e:
        print(f'❌ [{name}] ERR: {e}')
        results.append((name, '❌'))


# ====== 测试 ======
print('=' * 80)
print('Batch 5a 散装接口对比验证')
print('=' * 80)

# 1. GetAccountWarningListSummary（无参数）
compare('GetAccountWarningListSummary', '/BusinessProject/GetAccountWarningListSummary')

# 2. GetAccountWarningListSummary + Business_Type=1
compare('GetAccountWarningListSummary+BT', '/BusinessProject/GetAccountWarningListSummary',
        params='Business_Type=1')

# 3. GetMerchantSplit
compare('GetMerchantSplit', '/BusinessProject/GetMerchantSplit', params='MerchantId=31')

# 4. GetNoProjectShopList
compare('GetNoProjectShopList', '/BusinessProject/GetNoProjectShopList', params='ProvinceCode=44')

# 5. ApproveProinst（用不存在的ID，期望失败但Code相同）
compare('ApproveProinst', '/BusinessProject/ApproveProinst',
        params='BusinessId=99999&StaffId=1&StaffName=test&SwitchRate=10&ApproveState=1')

print()
print('=' * 80)
print('汇总:')
for name, status in results:
    print(f'  {status} {name}')
print('=' * 80)
