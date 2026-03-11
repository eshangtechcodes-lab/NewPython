# -*- coding: utf-8 -*-
"""
第二步：调原 API 获取基准数据 + 第零步：检查达梦中依赖表
接口: GET BaseInfo/GetSPRegionList?Province_Code=340000
"""
import json
import requests
import dmPython

# ===== 第二步：调原 API =====
print("=" * 60)
print("  第二步：调原 CommercialApi 获取基准数据")
print("=" * 60)

# CommercialApi 端口需要确认（先试 8900 同端口）
urls = [
    "http://localhost:8900/BaseInfo/GetSPRegionList?Province_Code=340000",
    "http://localhost:8901/BaseInfo/GetSPRegionList?Province_Code=340000",
]

old_data = None
for url in urls:
    print(f"\n尝试: GET {url}")
    try:
        resp = requests.get(url, timeout=5)
        old_data = resp.json()
        print(f"  ✅ 响应成功")
        print(f"  Result_Code: {old_data.get('Result_Code')}")
        print(f"  Result_Desc: {old_data.get('Result_Desc')}")
        rd = old_data.get('Result_Data', {})
        lst = rd.get('List', [])
        print(f"  TotalCount:  {rd.get('TotalCount')}")
        print(f"  List 条数:   {len(lst)}")
        if lst:
            print(f"  第一条: {json.dumps(lst[0], ensure_ascii=False)}")
            print(f"  最后一条: {json.dumps(lst[-1], ensure_ascii=False)}")
        # 保存基准
        with open("scripts/baseline_GetSPRegionList.json", "w", encoding="utf-8") as f:
            json.dump(old_data, f, ensure_ascii=False, indent=2)
        print(f"\n  基准数据已保存到 scripts/baseline_GetSPRegionList.json")
        break
    except Exception as ex:
        print(f"  ❌ 失败: {ex}")

# ===== 第零步：检查达梦依赖表 =====
print(f"\n{'=' * 60}")
print("  第零步：检查达梦中依赖表")
print("=" * 60)

try:
    conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
    cur = conn.cursor()
    
    tables = ['T_SERVERPARTTYPE']
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            count = cur.fetchone()[0]
            print(f"  {'✅' if count > 0 else '⚠️'} {t:30s} {count:>8} 条")
        except Exception as ex:
            print(f"  ❌ {t:30s} 不存在 → 需要从 Oracle 同步")
            print(f"     错误: {ex}")
    
    conn.close()
except Exception as ex:
    print(f"  ❌ 达梦连接失败: {ex}")
