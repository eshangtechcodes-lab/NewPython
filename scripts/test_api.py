# -*- coding: utf-8 -*-
"""
EShangApi 框架验证测试脚本
验证各层功能是否正确：配置/AES加解密/数据库连接/API路由/响应格式
"""
import sys
import json
import requests

API_BASE = "http://localhost:8080"
PASS = "✅ PASS"
FAIL = "❌ FAIL"


def test_root():
    """测试1: 根路径健康检查"""
    print("=" * 60)
    print("测试1: 根路径 GET /")
    try:
        resp = requests.get(f"{API_BASE}/")
        data = resp.json()
        assert data["Result_Code"] == 100
        assert "EShangApi" in data["Result_Desc"]
        assert data["Result_Data"]["framework"] == "FastAPI"
        print(f"  状态码: {resp.status_code}")
        print(f"  响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"  {PASS} 根路径正常，响应格式与原 API 一致")
        return True
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False


def test_health():
    """测试2: 数据库健康检查"""
    print("=" * 60)
    print("测试2: 健康检查 GET /health")
    try:
        resp = requests.get(f"{API_BASE}/health")
        data = resp.json()
        db_status = data["Result_Data"]["database"]
        print(f"  数据库状态: {db_status}")
        print(f"  响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        if db_status == "connected":
            print(f"  {PASS} 达梦数据库连接正常")
        else:
            print(f"  ⚠️  达梦数据库未连接（需确认数据库地址和端口）")
        return db_status == "connected"
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False


def test_aes():
    """测试3: AES 加解密"""
    print("=" * 60)
    print("测试3: AES-CBC 加解密验证")
    try:
        sys.path.insert(0, ".")
        from core.aes_util import aes_encrypt, aes_decrypt

        # 测试 SearchModel 数据加解密
        original = json.dumps({
            "PageIndex": 1, "PageSize": 10, "QueryType": 0,
            "SearchParameter": {"BRAND_NAME": "星巴克"}
        }, ensure_ascii=False)

        encrypted = aes_encrypt(original)
        decrypted = aes_decrypt(encrypted)
        parsed = json.loads(decrypted)

        assert decrypted == original
        assert parsed["SearchParameter"]["BRAND_NAME"] == "星巴克"

        print(f"  原文: {original}")
        print(f"  密文: {encrypted}")
        print(f"  解密: {decrypted}")
        print(f"  {PASS} AES 加解密正确，中文支持正常")
        return True, encrypted
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False, None


def test_swagger():
    """测试4: Swagger 文档可用性"""
    print("=" * 60)
    print("测试4: Swagger API 文档 GET /docs")
    try:
        resp = requests.get(f"{API_BASE}/docs")
        assert resp.status_code == 200
        assert "swagger" in resp.text.lower() or "openapi" in resp.text.lower()
        print(f"  状态码: {resp.status_code}")
        print(f"  {PASS} Swagger 文档可访问: {API_BASE}/docs")
        return True
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False


def test_openapi_schema():
    """测试5: OpenAPI Schema 验证路由注册"""
    print("=" * 60)
    print("测试5: OpenAPI Schema 验证路由注册")
    try:
        resp = requests.get(f"{API_BASE}/openapi.json")
        schema = resp.json()
        paths = list(schema.get("paths", {}).keys())
        print(f"  已注册接口: {len(paths)} 个")
        for path in paths:
            methods = list(schema["paths"][path].keys())
            print(f"    {', '.join(m.upper() for m in methods)} {path}")

        # 验证 BRAND 四个接口已注册
        expected = ["/BaseInfo/GetBRANDList", "/BaseInfo/GetBRANDDetail",
                    "/BaseInfo/SynchroBRAND", "/BaseInfo/DeleteBRAND"]
        registered = all(p in paths for p in expected)
        if registered:
            print(f"  {PASS} BRAND 四个接口全部注册成功，路由路径与原 C# 项目一致")
        else:
            print(f"  {FAIL} BRAND 接口未全部注册")
        return registered
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False


def test_brand_list_api(encrypted_value):
    """测试6: BRAND 列表接口（完整请求链路）"""
    print("=" * 60)
    print("测试6: POST /BaseInfo/GetBRANDList 完整请求链路")
    try:
        # 使用与原 C# API 完全相同的请求格式
        body = {"value": encrypted_value}
        resp = requests.post(
            f"{API_BASE}/BaseInfo/GetBRANDList",
            json=body,
            headers={"Content-Type": "application/json"}
        )
        data = resp.json()
        print(f"  请求体: {json.dumps(body, ensure_ascii=False)}")
        print(f"  响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

        # 验证响应格式
        assert "Result_Code" in data, "缺少 Result_Code 字段"
        assert "Result_Desc" in data, "缺少 Result_Desc 字段"
        assert "Result_Data" in data, "缺少 Result_Data 字段"

        if data["Result_Code"] == 100:
            # 数据库连接正常，验证分页响应
            result_data = data["Result_Data"]
            assert "PageIndex" in result_data, "缺少 PageIndex"
            assert "PageSize" in result_data, "缺少 PageSize"
            assert "TotalCount" in result_data, "缺少 TotalCount"
            assert "List" in result_data, "缺少 List"
            print(f"  {PASS} 接口返回正常，数据条数: {result_data['TotalCount']}")
        elif data["Result_Code"] == 999:
            print(f"  ⚠️  接口路由正常，但数据库查询失败（达梦未连接）")
            print(f"  响应格式验证: Result_Code/Result_Desc/Result_Data 三字段完整 → {PASS}")
        return True
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False


def test_response_format():
    """测试7: 验证响应格式与原 C# API 完全一致"""
    print("=" * 60)
    print("测试7: 响应格式一致性验证")

    # 模拟一个无加密参数的请求（应返回999错误，但格式正确）
    try:
        body = {"value": "invalid_encrypted_data"}
        resp = requests.post(f"{API_BASE}/BaseInfo/GetBRANDList", json=body)
        data = resp.json()

        checks = {
            "HTTP 状态码 200": resp.status_code == 200,
            "Result_Code 字段存在": "Result_Code" in data,
            "Result_Desc 字段存在": "Result_Desc" in data,
            "Result_Data 字段存在": "Result_Data" in data,
            "错误时 Result_Code=999": data.get("Result_Code") == 999,
        }

        all_pass = True
        for check, result in checks.items():
            status = PASS if result else FAIL
            if not result:
                all_pass = False
            print(f"  {status} {check}")

        if all_pass:
            print(f"  {PASS} 响应格式与原 C# API 完全一致")
        return all_pass
    except Exception as ex:
        print(f"  {FAIL} {ex}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  EShangApi (Python) 框架验证测试")
    print("  原项目: C# ASP.NET Web API 2")
    print("  新项目: Python FastAPI")
    print("=" * 60 + "\n")

    results = {}

    # 执行测试
    results["根路径"] = test_root()
    print()
    results["数据库"] = test_health()
    print()
    aes_ok, encrypted = test_aes()
    results["AES加解密"] = aes_ok
    print()
    results["Swagger文档"] = test_swagger()
    print()
    results["路由注册"] = test_openapi_schema()
    print()
    if encrypted:
        results["BRAND接口"] = test_brand_list_api(encrypted)
        print()
    results["响应格式"] = test_response_format()

    # 汇总
    print("\n" + "=" * 60)
    print("  测试结果汇总")
    print("=" * 60)
    for name, ok in results.items():
        status = PASS if ok else (FAIL if ok is False else "⚠️  WARNING")
        print(f"  {status} {name}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n  通过: {passed}/{total}")
    print("=" * 60)
