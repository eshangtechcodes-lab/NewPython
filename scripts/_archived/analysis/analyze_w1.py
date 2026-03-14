"""分析窗口 1：精确分类并统计"""
import json
from collections import Counter

data = json.load(open('docs/window_1_dynamic_compare_report.json', 'r', encoding='utf-8'))

# 统计 diffs
all_diffs = []
for c in data['cases']:
    if c['status'] == 'fail':
        all_diffs.extend(c.get('diffs', []))

print(f"=== FAIL 数: {sum(1 for c in data['cases'] if c['status']=='fail')} / {len(data['cases'])} ===")
print(f"=== PASS 数: {sum(1 for c in data['cases'] if c['status']=='pass')} / {len(data['cases'])} ===\n")

# 按类型分类
cats = {'result_extra': 0, 'code_999_100': 0, 'code_100_999': 0, 
        'message_extra': 0, 'message_missing': 0, 'statics_extra': 0,
        'timeout': 0, 'strip_bug': 0, 'data_diff': 0, 'orig_parse_fail': 0}

for c in data['cases']:
    if c['status'] != 'fail':
        continue
    diffs = c.get('diffs', [])
    for d in diffs:
        if 'Result_Code: 新 API 多出该字段' in d:
            cats['result_extra'] += 1
        elif '999 vs 100' in d and 'Result_Code' in d:
            cats['code_999_100'] += 1
        elif '100 vs 999' in d and 'Result_Code' in d:
            cats['code_100_999'] += 1
        elif 'Message: 新 API 多出该字段' in d:
            cats['message_extra'] += 1
        elif 'Message: 新 API 缺少该字段' in d:
            cats['message_missing'] += 1
        elif 'StaticsModel: 新 API 多出该字段' in d:
            cats['statics_extra'] += 1
        elif 'Read timed out' in d:
            cats['timeout'] += 1
        elif "has no attribute 'strip'" in d:
            cats['strip_bug'] += 1
        elif '原 API JSON 解析失败' in d:
            cats['orig_parse_fail'] += 1

print("=== 差异类型统计 ===")
for k, v in sorted(cats.items(), key=lambda x: -x[1]):
    if v > 0:
        print(f"  {k}: {v}")

# 列出 code_999_100 的具体接口
print("\n=== Result_Code 999 vs 100 (Python 错, C# 对) ===")
for c in data['cases']:
    if c['status'] != 'fail':
        continue
    for d in c.get('diffs', []):
        if '999 vs 100' in d and 'Result_Code' in d:
            desc = [x for x in c.get('diffs', []) if 'Result_Desc' in x and '值不一致' in x]
            print(f"  {c['endpoint']}: {desc[0][:80] if desc else ''}")
            break

# 列出 strip bug 接口
print("\n=== strip bug 接口 ===")
for c in data['cases']:
    if c['status'] != 'fail':
        continue
    for d in c.get('diffs', []):
        if "has no attribute 'strip'" in d:
            print(f"  {c['endpoint']}")
            break
