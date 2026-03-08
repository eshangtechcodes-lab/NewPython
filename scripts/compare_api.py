# -*- coding: utf-8 -*-
"""
API 对比脚本 - 对比原 C# API 和新 Python API 的响应
用法: python scripts/compare_api.py
"""
import requests
import json
import sys

# 当前对比的接口
ENDPOINT = "BaseInfo/GetSERVERPARTCRTList"

OLD_API = f"http://192.168.1.99:8900/EShangApiMain/{ENDPOINT}"
NEW_API = f"http://localhost:8080/EShangApiMain/{ENDPOINT}"

def compare():
    output = []
    output.append(f"=" * 60)
    output.append(f"  对比接口: {ENDPOINT}")
    output.append(f"=" * 60)

    # 调用原 API
    try:
        old_resp = requests.post(OLD_API, json={}, timeout=10)
        old_data = old_resp.json()
        output.append(f"\n[原 API] 状态码: {old_resp.status_code}")
        output.append(f"  Result_Code: {old_data.get('Result_Code')}")
        if old_data.get('Result_Data'):
            rd = old_data['Result_Data']
            output.append(f"  TotalCount: {rd.get('TotalCount')}")
            lst = rd.get('List', [])
            output.append(f"  List 条数: {len(lst)}")
            if lst:
                output.append(f"  首条字段: {sorted(lst[0].keys())}")
    except Exception as e:
        output.append(f"\n[原 API] 调用失败: {e}")
        old_data = None

    # 调用新 API
    try:
        new_resp = requests.post(NEW_API, json={}, timeout=10)
        new_data = new_resp.json()
        output.append(f"\n[新 API] 状态码: {new_resp.status_code}")
        output.append(f"  Result_Code: {new_data.get('Result_Code')}")
        if new_data.get('Result_Data'):
            rd = new_data['Result_Data']
            output.append(f"  TotalCount: {rd.get('TotalCount')}")
            lst = rd.get('List', [])
            output.append(f"  List 条数: {len(lst)}")
            if lst:
                output.append(f"  首条字段: {sorted(lst[0].keys())}")
    except Exception as e:
        output.append(f"\n[新 API] 调用失败: {e}")
        new_data = None

    # 对比
    output.append(f"\n{'=' * 60}")
    output.append(f"  对比结果")
    output.append(f"{'=' * 60}")

    if old_data and new_data:
        # 对比 Result_Code
        old_code = old_data.get('Result_Code')
        new_code = new_data.get('Result_Code')
        output.append(f"  Result_Code: {'✅ 一致' if old_code == new_code else f'❌ 不一致 ({old_code} vs {new_code})'}")

        # 对比 TotalCount
        old_rd = old_data.get('Result_Data', {})
        new_rd = new_data.get('Result_Data', {})
        old_tc = old_rd.get('TotalCount', 0)
        new_tc = new_rd.get('TotalCount', 0)
        output.append(f"  TotalCount: {'✅ 一致' if old_tc == new_tc else f'❌ 不一致 ({old_tc} vs {new_tc})'}")

        # 对比 List 条数
        old_list = old_rd.get('List', [])
        new_list = new_rd.get('List', [])
        output.append(f"  List 条数: {'✅ 一致' if len(old_list) == len(new_list) else f'❌ 不一致 ({len(old_list)} vs {len(new_list)})'}")

        # 对比字段
        if old_list and new_list:
            old_fields = set(old_list[0].keys())
            new_fields = set(new_list[0].keys())

            only_old = old_fields - new_fields
            only_new = new_fields - old_fields
            common = old_fields & new_fields

            output.append(f"\n  共同字段: {len(common)}")
            if only_old:
                output.append(f"  仅原 API: {sorted(only_old)}")
            if only_new:
                output.append(f"  仅新 API: {sorted(only_new)}")
            if not only_old and not only_new:
                output.append(f"  ✅ 字段完全一致")

            # 对比首条数据值
            output.append(f"\n  首条数据对比:")
            diff_count = 0
            for field in sorted(common):
                old_val = old_list[0].get(field)
                new_val = new_list[0].get(field)
                # 统一 None 处理
                if old_val is None and new_val is None:
                    continue
                if str(old_val) != str(new_val):
                    diff_count += 1
                    output.append(f"    ❌ {field}: [{old_val}] vs [{new_val}]")
            if diff_count == 0:
                output.append(f"    ✅ 所有字段值一致")
            else:
                output.append(f"    共 {diff_count} 个字段值不一致")

    result_text = "\n".join(output)
    print(result_text)

    with open("scripts/compare_result.txt", "w", encoding="utf-8") as f:
        f.write(result_text)
    print(f"\n结果已保存到 scripts/compare_result.txt")


if __name__ == "__main__":
    compare()
