# -*- coding: utf-8 -*-
"""对比新旧 API 接口返回结果"""
import json
import requests

API_BASE = "http://localhost:8080"

print("=" * 60)
print("  新 Python API 与原 C# API 对比验证")
print("=" * 60)

# 测试1: 空 {} 调用（完全模拟原 API 截图的请求）
print("\n测试: POST /EShangApiMain/BaseInfo/GetBrandList")
print("入参: {} (空 JSON，与原 C# API 截图一致)")
resp = requests.post(
    f"{API_BASE}/EShangApiMain/BaseInfo/GetBrandList",
    json={},
    headers={"Content-Type": "application/json"}
)
data = resp.json()

# 验证整体结构
print(f"\n--- 响应结构对比 ---")
print(f"  Result_Code: {data['Result_Code']}  (原API: 100) {'✅' if data['Result_Code'] == 100 else '❌'}")
print(f"  Result_Desc: {data['Result_Desc']}  (原API: 查询成功) {'✅' if '查询成功' in data['Result_Desc'] else '❌'}")

rd = data["Result_Data"]
print(f"  PageIndex:   {rd['PageIndex']}  (原API: 0) {'✅' if rd['PageIndex'] == 0 else '❌'}")
print(f"  PageSize:    {rd['PageSize']}  (原API: 0) {'✅' if rd['PageSize'] == 0 else '❌'}")
print(f"  TotalCount:  {rd['TotalCount']}  (原API: 2005) {'✅' if rd['TotalCount'] == 2005 else '❌'}")
print(f"  List 条数:   {len(rd['List'])}  (原API: 2005) {'✅' if len(rd['List']) == 2005 else '❌'}")

# 验证第一条数据的字段
if rd["List"]:
    first = rd["List"][0]
    print(f"\n--- 第一条数据字段对比 ---")
    print(f"  字段列表: {list(first.keys())}")
    print(f"  BRAND_ID:       {first.get('BRAND_ID')} (类型: {type(first.get('BRAND_ID')).__name__})")
    print(f"  BRAND_NAME:     {first.get('BRAND_NAME')}")
    print(f"  BRAND_CATEGORY: {first.get('BRAND_CATEGORY')}")
    print(f"  BRAND_INDUSTRY: {first.get('BRAND_INDUSTRY')}")
    print(f"  BRAND_TYPE:     {first.get('BRAND_TYPE')}")
    print(f"  BRAND_STATE:    {first.get('BRAND_STATE')}")
    print(f"  OWNERUNIT_NAME: {first.get('OWNERUNIT_NAME')}")

    # 打印完整 JSON（前2条）
    print(f"\n--- 前 2 条完整数据 ---")
    for i, item in enumerate(rd["List"][:2]):
        print(f"\n  [{i+1}] {json.dumps(item, ensure_ascii=False, indent=4)}")
