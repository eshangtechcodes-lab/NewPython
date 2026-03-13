"""生成窗口 1 修复清单：按差异类型分组"""
import json
import sys

data = json.load(open('docs/window_1_dynamic_compare_report.json', 'r', encoding='utf-8'))

# 分类接口
groups = {
    'code_mismatch_py_err': [],   # Python 999, C# 100
    'code_mismatch_cs_err': [],   # Python 100, C# 999
    'only_message_diff': [],       # 仅 Message 差异
    'field_missing': [],           # 缺字段
    'list_length': [],             # 列表长度
    'value_mismatch': [],          # 值不一致
    'type_mismatch': [],           # 类型不一致
    'statics_extra': [],           # StaticsModel 多出
}

for c in data['cases']:
    if c['status'] != 'fail':
        continue
    diffs = c.get('diffs', [])
    
    # 跳过 result_extra, parse_fail, timeout
    if any('Result_Code: 新 API 多出该字段' in d for d in diffs):
        continue
    if any('原 API JSON 解析失败' in d for d in diffs):
        continue
    if any('timed out' in d for d in diffs):
        continue
    
    ep = c['endpoint']
    cn = c['case_name']
    key = f"{ep} / {cn}"
    
    has_code_999 = any('999 vs 100' in d and 'Result_Code' in d for d in diffs)
    has_code_100 = any('100 vs 999' in d and 'Result_Code' in d for d in diffs)
    
    if has_code_999:
        desc = [d for d in diffs if 'Result_Desc' in d]
        groups['code_mismatch_py_err'].append((key, desc[0][:100] if desc else ''))
        continue
    if has_code_100:
        desc = [d for d in diffs if 'Result_Desc' in d]
        groups['code_mismatch_cs_err'].append((key, desc[0][:100] if desc else ''))
        continue
    
    # 非 code mismatch，分析具体差异类型
    non_msg_diffs = [d for d in diffs if 'Message' not in d]
    msg_diffs = [d for d in diffs if 'Message' in d]
    
    if not non_msg_diffs and msg_diffs:
        groups['only_message_diff'].append(key)
        continue
    
    for d in non_msg_diffs:
        if '缺少该字段' in d or '多出该字段' in d:
            groups['field_missing'].append((key, d[:100]))
        elif '列表长度不一致' in d:
            groups['list_length'].append((key, d[:100]))
        elif '值不一致' in d:
            groups['value_mismatch'].append((key, d[:100]))
        elif '类型不一致' in d:
            groups['type_mismatch'].append((key, d[:100]))

# 输出
with open('docs/w1_fix_plan.md', 'w', encoding='utf-8') as f:
    f.write('# 窗口 1 深度修复清单\n\n')
    
    f.write(f'## 1. Python 报错但 C# 成功 ({len(groups["code_mismatch_py_err"])} 个)\n\n')
    for key, desc in groups['code_mismatch_py_err']:
        f.write(f'- `{key}`\n  - {desc}\n')
    
    f.write(f'\n## 2. Python 成功但 C# 报错 ({len(groups["code_mismatch_cs_err"])} 个)\n\n')
    for key, desc in groups['code_mismatch_cs_err']:
        f.write(f'- `{key}`\n  - {desc}\n')
    
    f.write(f'\n## 3. 仅 Message 差异 ({len(groups["only_message_diff"])} 个)\n\n')
    for key in groups['only_message_diff']:
        f.write(f'- `{key}`\n')
    
    # 去重统计
    field_eps = sorted(set(k for k, _ in groups['field_missing']))
    f.write(f'\n## 4. 缺少/多出字段 ({len(field_eps)} 个接口)\n\n')
    for ep in field_eps:
        details = [d for k, d in groups['field_missing'] if k == ep]
        f.write(f'- `{ep}`\n')
        for d in details[:5]:
            f.write(f'  - {d}\n')
        if len(details) > 5:
            f.write(f'  - ... 还有 {len(details)-5} 处\n')
    
    list_eps = sorted(set(k for k, _ in groups['list_length']))
    f.write(f'\n## 5. 列表长度不一致 ({len(list_eps)} 个接口)\n\n')
    for ep in list_eps:
        details = [d for k, d in groups['list_length'] if k == ep]
        f.write(f'- `{ep}`: {details[0]}\n')
    
    type_eps = sorted(set(k for k, _ in groups['type_mismatch']))
    f.write(f'\n## 6. 类型不一致 ({len(type_eps)} 个接口)\n\n')
    for ep in type_eps:
        details = [d for k, d in groups['type_mismatch'] if k == ep]
        f.write(f'- `{ep}`\n')
        for d in details[:3]:
            f.write(f'  - {d}\n')

print('修复清单已写入 docs/w1_fix_plan.md')
