"""列出所有 code_999_100 的接口和错误信息"""
import json

data = json.load(open('docs/window_1_dynamic_compare_report.json', 'r', encoding='utf-8'))

print("=== Result_Code 999 vs 100 (Python 报错, C# 成功) ===\n")
count = 0
for c in data['cases']:
    if c['status'] != 'fail':
        continue
    diffs = c.get('diffs', [])
    has_999 = any('999 vs 100' in d and 'Result_Code' in d for d in diffs)
    if has_999:
        count += 1
        desc = [d for d in diffs if 'Result_Desc' in d and '\u503c\u4e0d\u4e00\u81f4' in d]
        print(f"  [{count}] {c['endpoint']} / {c['case_name']}")
        if desc:
            print(f"      {desc[0][:120]}")
        print()

print(f"Total: {count}\n")

print("=== strip bug ===\n")
for c in data['cases']:
    if c['status'] != 'fail':
        continue
    for d in c.get('diffs', []):
        if "strip" in d:
            print(f"  {c['endpoint']}: {d[:100]}")
