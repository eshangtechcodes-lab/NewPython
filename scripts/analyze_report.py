import json
data = json.load(open('docs/window_1_dynamic_compare_report.json', 'r', encoding='utf-8'))
cases = data['cases']
passed = [c['endpoint'] for c in cases if c['status']=='pass']
print(f"PASS: {len(passed)}")
for p in passed:
    print(f"  {p}")
print()
# GetBusinessTradeDetail
btd = [c for c in cases if 'BusinessTradeDetail' in c['endpoint']]
for c in btd:
    print(f"{c['endpoint']}: {c['status']}, diffs={len(c.get('diffs',[]))}")
    for d in c.get('diffs', []):
        print(f"  {d[:200]}")
# GetPeriodWarningList
pwl = [c for c in cases if 'PeriodWarningList' in c['endpoint']]
for c in pwl:
    print(f"\n{c['endpoint']}: {c['status']}, old={c.get('old_status_code')}, new={c.get('new_status_code')}, diffs={len(c.get('diffs',[]))}")
    for d in c.get('diffs', []):
        print(f"  {d[:200]}")
# PaymentConfirmList
pcl = [c for c in cases if 'PaymentConfirmList' in c['endpoint']]
for c in pcl:
    print(f"\n{c['endpoint']}: {c['status']}, old={c.get('old_status_code')}, new={c.get('new_status_code')}, diffs={len(c.get('diffs',[]))}")
    for d in c.get('diffs', []):
        print(f"  {d[:200]}")
