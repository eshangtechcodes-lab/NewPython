# -*- coding: utf-8 -*-
"""
按 service 文件分组分析所有失败接口，生成精确工作清单
确定哪些接口只需 DB 层修复（P1/P3/P4），哪些需要 service 改动
"""
import json
import re

report = json.load(open('docs/window_1_dynamic_compare_report.json', 'r', encoding='utf-8'))

# 分析每个失败接口的差异类型
results = []
for c in report['cases']:
    if c['status'] != 'fail':
        continue
    ep = c['endpoint']
    diffs = c.get('diffs', [])
    error = c.get('error', '')
    
    has_float_int = False
    has_none_str = False
    has_missing_field = False
    has_extra_field = False
    has_value_diff = False
    has_length_diff = False
    has_result_code = False
    has_error = bool(error)
    missing_fields = []
    extra_fields = []
    
    for d in diffs:
        s = str(d)
        if 'float vs int' in s or 'int vs float' in s:
            has_float_int = True
        elif 'NoneType vs str' in s or 'str vs NoneType' in s or 'NoneType vs int' in s or 'int vs NoneType' in s or 'NoneType vs list' in s or 'list vs NoneType' in s:
            has_none_str = True
        elif '新 API 缺少该字段' in s:
            has_missing_field = True
            field = s.split(':')[0].strip().split('.')[-1]
            missing_fields.append(field)
        elif '新 API 多出该字段' in s:
            has_extra_field = True
            field = s.split(':')[0].strip().split('.')[-1]
            extra_fields.append(field)
        elif '值不一致' in s:
            has_value_diff = True
        elif '列表长度不一致' in s:
            has_length_diff = True
        elif 'Result_Code' in s:
            has_result_code = True
    
    # 判断是否只需 DB 层修复
    only_db = (has_float_int or has_none_str) and not has_missing_field and not has_extra_field and not has_value_diff and not has_length_diff and not has_result_code and not has_error
    
    results.append({
        'endpoint': ep,
        'diff_count': len(diffs),
        'only_db': only_db,
        'has_missing': has_missing_field,
        'has_extra': has_extra_field,
        'has_value': has_value_diff,
        'has_length': has_length_diff,
        'has_error': has_error,
        'has_result_code': has_result_code,
        'missing_fields': missing_fields[:5],
        'extra_fields': extra_fields[:3],
    })

# 输出分类结果
only_db = [r for r in results if r['only_db']]
need_service = [r for r in results if not r['only_db']]

print(f"=== 仅需 DB 层修复（应自动通过）: {len(only_db)} 个 ===")
for r in sorted(only_db, key=lambda x: x['diff_count']):
    print(f"  [{r['diff_count']}差异] {r['endpoint']}")

print(f"\n=== 需要 service 层修改: {len(need_service)} 个 ===")

# 按模块分组
modules = {}
for r in need_service:
    module = r['endpoint'].split('/')[0]
    if module not in modules:
        modules[module] = []
    modules[module].append(r)

for module, items in sorted(modules.items()):
    print(f"\n--- {module} ({len(items)}个接口) ---")
    for r in sorted(items, key=lambda x: x['diff_count']):
        flags = []
        if r['has_missing']: flags.append(f"缺{len(r['missing_fields'])}字段")
        if r['has_extra']: flags.append(f"多{len(r['extra_fields'])}字段")
        if r['has_value']: flags.append("值差异")
        if r['has_length']: flags.append("长度差")
        if r['has_error']: flags.append("错误")
        if r['has_result_code']: flags.append("状态码")
        print(f"  [{r['diff_count']:2d}差异] {r['endpoint'].split('/')[1]}: {', '.join(flags)}")
        if r['missing_fields']:
            print(f"         缺: {', '.join(r['missing_fields'][:4])}")
