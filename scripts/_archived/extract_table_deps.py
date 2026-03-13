# -*- coding: utf-8 -*-
"""
从 C# Helper 源码中自动提取各 Controller 依赖的数据库表
然后检查哪些表在 Dameng 中不存在
"""
import re, os, json
from collections import defaultdict

HELPER_DIR = r"D:\CSharp\Project\000_通用版本\000_通用版本\030_EShangApi\CommercialApi\GeneralMethod"

# 正则提取表名（包含 schema 前缀）
table_pattern = re.compile(r'(?:FROM|JOIN|INTO|UPDATE|EXISTS\s*\(SELECT\s+\d+\s+FROM)\s+([\w]+\.T_[\w]+)', re.IGNORECASE)

# 按 Helper 文件夹分组（对应 Controller）
controller_tables = defaultdict(set)
all_tables = set()

for root, dirs, files in os.walk(HELPER_DIR):
    folder = os.path.basename(root)
    for fname in files:
        if not fname.endswith('.cs'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        matches = table_pattern.findall(content)
        for m in matches:
            controller_tables[folder].add(m.upper())
            all_tables.add(m.upper())

# 打印按 Controller 分组的表依赖
print("=" * 70)
print("Controller 依赖表统计")
print("=" * 70)
for folder in sorted(controller_tables.keys()):
    tables = sorted(controller_tables[folder])
    print(f"\n[{folder}] ({len(tables)} 张表)")
    for t in tables:
        print(f"  {t}")

# 按 schema 分组
schema_tables = defaultdict(set)
for t in all_tables:
    parts = t.split('.')
    if len(parts) == 2:
        schema_tables[parts[0]].add(parts[1])

print("\n" + "=" * 70)
print("按 Schema 分组")
print("=" * 70)
for schema in sorted(schema_tables.keys()):
    tables = sorted(schema_tables[schema])
    print(f"\n[{schema}] ({len(tables)} 张表)")
    for t in tables:
        print(f"  {t}")

# 已存在于 Dameng 的表
dm_existing = [
    "T_AUTOSTATISTICS", "T_BRAND", "T_OWNERUNIT", "T_SERVERPART",
    "T_SERVERPARTSHOP", "T_SERVERPARTTYPE", "T_SHOPCOUNT"
]

# HIGHWAY_STORAGE schema 下需要的表
hs_needed = schema_tables.get("HIGHWAY_STORAGE", set())
hs_missing = hs_needed - set(dm_existing)

print("\n" + "=" * 70)
print(f"HIGHWAY_STORAGE 需要但 Dameng 缺少的表: {len(hs_missing)} 张")
print("=" * 70)
for t in sorted(hs_missing):
    print(f"  - {t}")

print("\n" + "=" * 70)
print("所有 schema 需要同步的表总计")
print("=" * 70)
total_missing = 0
for schema in sorted(schema_tables.keys()):
    tables = sorted(schema_tables[schema])
    missing = [t for t in tables if t not in dm_existing]
    if missing:
        total_missing += len(missing)
        print(f"\n[{schema}] 缺少 {len(missing)} 张:")
        for t in missing:
            print(f"  - {schema}.{t}")

print(f"\n总计缺少: {total_missing} 张表")

# 保存结果
os.makedirs("scripts/test_results", exist_ok=True)
output = {
    "controller_tables": {k: sorted(v) for k, v in controller_tables.items()},
    "schema_tables": {k: sorted(v) for k, v in schema_tables.items()},
    "dm_existing": dm_existing,
    "total_missing": total_missing
}
with open("scripts/test_results/table_deps.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("\n详细结果已保存: scripts/test_results/table_deps.json")
