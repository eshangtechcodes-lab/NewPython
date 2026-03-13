# -*- coding: utf-8 -*-
"""
回归测试框架 — 一键运行三档测试
用法:
  python scripts/regression.py              # 默认运行冒烟测试
  python scripts/regression.py smoke        # 冒烟测试（<1分钟，20个核心接口）
  python scripts/regression.py standard     # 标准测试（~3分钟，全量响应码检查）
  python scripts/regression.py full         # 全量测试（~15分钟，逐字段对比，需 C# API）
  python scripts/regression.py --list       # 列出所有测试档位
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# === 配置 ===
PROJECT_ROOT = Path(__file__).resolve().parents[1]
NEW_API_BASE = "http://localhost:8080"
OLD_API_BASE = "http://192.168.1.99:8900"
MANIFEST_PATH = PROJECT_ROOT / "scripts" / "manifests" / "endpoint_case_library.json"
RESULTS_DIR = PROJECT_ROOT / "scripts" / "test_results"

# === 冒烟测试端点（每个 Controller 至少 1 个高频接口）===
SMOKE_ENDPOINTS = [
    # 系统
    {"path": "/health", "method": "GET", "name": "健康检查"},
    {"path": "/", "method": "GET", "name": "根路径"},
    # CommercialApi — 核心模块各选 1 个
    {"path": "/CommercialApi/BaseInfo/GetServerpartList", "method": "GET", "name": "服务区列表"},
    {"path": "/CommercialApi/BaseInfo/GetSPRegionList", "method": "GET",
     "params": {"Province_Code": "340000"}, "name": "区域列表"},
    {"path": "/CommercialApi/Revenue/GetCurRevenue", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "当前营收"},
    {"path": "/CommercialApi/Revenue/GetRevenueReport", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "营收报告"},
    {"path": "/CommercialApi/Examine/GetExamineAnalysis", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "考核分析"},
    {"path": "/CommercialApi/Customer/GetCustomerRatio", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "客群占比"},
    {"path": "/CommercialApi/BigData/GetDateAnalysis", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "日期分析"},
    # EShangApiMain — 核心 CRUD 模块各选 1 个
    {"path": "/EShangApiMain/BaseInfo/GetBrandList", "method": "POST",
     "json": {}, "name": "品牌列表"},
    {"path": "/EShangApiMain/BaseInfo/GetServerpartShopList", "method": "POST",
     "json": {}, "name": "门店列表"},
    {"path": "/EShangApiMain/BaseInfo/GetOWNERUNITList", "method": "POST",
     "json": {}, "name": "业主单位列表"},
    {"path": "/EShangApiMain/BaseInfo/GetCASHWORKERList", "method": "POST",
     "json": {}, "name": "收银人员列表"},
    {"path": "/EShangApiMain/BaseInfo/GetCOMMODITYList", "method": "POST",
     "json": {}, "name": "商品列表"},
    {"path": "/EShangApiMain/Contract/GetRegisterCompactList", "method": "POST",
     "json": {}, "name": "合同列表"},
    {"path": "/EShangApiMain/BusinessProject/GetBusinessProjectList", "method": "POST",
     "json": {}, "name": "经营项目列表"},
    {"path": "/EShangApiMain/Budget/GetBudgetProjectList", "method": "POST",
     "json": {}, "name": "预算列表"},
    {"path": "/EShangApiMain/Revenue/GetTotalRevenue", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "总营收"},
    {"path": "/EShangApiMain/Commodity/GetCOMMODITYList", "method": "POST",
     "json": {}, "name": "商品管理列表"},
    {"path": "/EShangApiMain/ShopVideo/GetShopVideoInfo", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "视频监控"},
]


def print_header(title: str):
    """打印测试档位标题"""
    width = 60
    print("=" * width)
    print(f"  {title}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * width)


def check_api_available(base_url: str, timeout: int = 5) -> bool:
    """检查 API 是否可用"""
    try:
        r = requests.get(f"{base_url}/health", timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False


# === 冒烟测试 ===
def run_smoke() -> int:
    """冒烟测试：20 个核心接口，仅检查响应码"""
    print_header("SMOKE TEST - 冒烟测试（核心接口响应检查）")

    if not check_api_available(NEW_API_BASE):
        print(f"\n[ERROR] 新 API ({NEW_API_BASE}) 不可用，请先启动服务！")
        print(f"  启动命令: python main.py")
        return 1

    passed, failed, errors = 0, 0, []
    start = time.time()
    headers = {"ProvinceCode": "340000"}

    for i, ep in enumerate(SMOKE_ENDPOINTS, 1):
        try:
            url = f"{NEW_API_BASE}{ep['path']}"
            if ep["method"] == "GET":
                r = requests.get(url, params=ep.get("params"), headers=headers, timeout=10)
            else:
                r = requests.post(url, json=ep.get("json", {}), headers=headers, timeout=10)

            # 判定标准：HTTP 200 且 Result_Code 为 100 或 200
            ok = False
            if r.status_code == 200:
                try:
                    body = r.json()
                    code = body.get("Result_Code")
                    if code in (100, 200, "100", "200"):
                        ok = True
                    elif ep["path"] in ("/", "/health"):
                        ok = True  # 系统端点不一定有 Result_Code
                except Exception:
                    pass

            status = "PASS" if ok else "FAIL"
            elapsed = r.elapsed.total_seconds() * 1000
            print(f"  [{i:2d}/{len(SMOKE_ENDPOINTS)}] {status} {ep['name']:20s} {ep['method']:4s} {ep['path']:50s} {elapsed:7.0f}ms")

            if ok:
                passed += 1
            else:
                failed += 1
                errors.append(f"{ep['name']}: HTTP {r.status_code}, body={r.text[:200]}")
        except Exception as ex:
            failed += 1
            errors.append(f"{ep['name']}: {ex}")
            print(f"  [{i:2d}/{len(SMOKE_ENDPOINTS)}] FAIL {ep['name']:20s} ERROR: {ex}")

    elapsed_total = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"  SMOKE RESULT: PASS {passed} / FAIL {failed} / TOTAL {len(SMOKE_ENDPOINTS)}")
    print(f"  Elapsed: {elapsed_total:.1f}s")
    if errors:
        print(f"\n  Failures:")
        for e in errors:
            print(f"    - {e}")
    print(f"{'=' * 60}")

    # 保存结果
    RESULTS_DIR.mkdir(exist_ok=True)
    result = {
        "type": "smoke", "timestamp": datetime.now().isoformat(),
        "passed": passed, "failed": failed, "total": len(SMOKE_ENDPOINTS),
        "elapsed_seconds": round(elapsed_total, 1), "errors": errors,
    }
    (RESULTS_DIR / "smoke_latest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0 if failed == 0 else 1


# === 标准测试 ===
def run_standard() -> int:
    """标准测试：全量端点响应码检查（不需要 C# API）"""
    print_header("STANDARD TEST - 全量响应码检查")

    if not check_api_available(NEW_API_BASE):
        print(f"\n[ERROR] 新 API ({NEW_API_BASE}) 不可用！")
        return 1

    # 从 main.py 的路由扫描脚本获取端点，或从 manifest 获取
    if not MANIFEST_PATH.exists():
        print(f"[ERROR] Manifest 不存在: {MANIFEST_PATH}")
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text("utf-8"))
    endpoints = manifest.get("endpoints", {})
    headers = {"ProvinceCode": "340000"}

    passed, failed, error_count, skipped = 0, 0, 0, 0
    errors = []
    start = time.time()

    for i, (ep_name, ep_config) in enumerate(endpoints.items(), 1):
        method = ep_config.get("method", "POST").upper()
        url = f"{NEW_API_BASE}/EShangApiMain/{ep_name}"

        try:
            if method == "GET":
                query = ep_config.get("cases", [{}])[0].get("query", {})
                r = requests.get(url, params=query, headers=headers, timeout=10)
            else:
                body = ep_config.get("cases", [{}])[0].get("json", {})
                r = requests.post(url, json=body, headers=headers, timeout=10)

            ok = r.status_code == 200
            if ok:
                passed += 1
            else:
                failed += 1
                if len(errors) < 20:
                    errors.append(f"{ep_name}: HTTP {r.status_code}")

            if i % 50 == 0 or i == len(endpoints):
                print(f"  Progress: {i}/{len(endpoints)} (PASS {passed} / FAIL {failed})")

        except requests.exceptions.Timeout:
            skipped += 1
        except Exception as ex:
            error_count += 1
            if len(errors) < 20:
                errors.append(f"{ep_name}: {ex}")

    elapsed_total = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"  STANDARD RESULT: PASS {passed} / FAIL {failed} / ERROR {error_count} / TIMEOUT {skipped}")
    print(f"  Total endpoints: {len(endpoints)} | Elapsed: {elapsed_total:.1f}s")
    if errors:
        print(f"\n  Top failures (max 20):")
        for e in errors:
            print(f"    - {e}")
    print(f"{'=' * 60}")

    RESULTS_DIR.mkdir(exist_ok=True)
    result = {
        "type": "standard", "timestamp": datetime.now().isoformat(),
        "passed": passed, "failed": failed, "error": error_count,
        "timeout": skipped, "total": len(endpoints),
        "elapsed_seconds": round(elapsed_total, 1), "errors": errors[:20],
    }
    (RESULTS_DIR / "standard_latest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0 if failed == 0 and error_count == 0 else 1


# === 全量对比测试 ===
def run_full() -> int:
    """全量测试：调用 compare_api.py 进行逐字段对比（需要 C# API）"""
    print_header("FULL TEST - 全量逐字段对比（需要原 C# API）")

    if not check_api_available(NEW_API_BASE):
        print(f"\n[ERROR] 新 API ({NEW_API_BASE}) 不可用！")
        return 1

    if not check_api_available(OLD_API_BASE):
        print(f"\n[WARNING] 原 C# API ({OLD_API_BASE}) 不可用！")
        print(f"  全量对比需要原 C# API 在线。")
        return 1

    import subprocess
    compare_script = PROJECT_ROOT / "scripts" / "compare" / "compare_api.py"
    report_path = RESULTS_DIR / "full_latest.md"

    cmd = [
        sys.executable, str(compare_script),
        "--manifest", str(MANIFEST_PATH),
        "--report", str(report_path),
    ]

    print(f"  执行: {' '.join(cmd[-4:])}")
    print(f"  预计耗时: ~15 分钟")
    print()

    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="EShangApi 回归测试框架")
    parser.add_argument("level", nargs="?", default="smoke",
                        choices=["smoke", "standard", "full"],
                        help="测试档位: smoke(冒烟) / standard(标准) / full(全量)")
    parser.add_argument("--list", action="store_true", help="列出所有测试档位")
    args = parser.parse_args()

    if args.list:
        print("可用的测试档位:")
        print(f"  smoke    冒烟测试    {len(SMOKE_ENDPOINTS)} 个核心接口，<1分钟")
        print(f"  standard 标准测试    全量端点响应码检查，~3分钟")
        print(f"  full     全量测试    逐字段数据对比，~15分钟（需 C# API）")
        return 0

    runners = {"smoke": run_smoke, "standard": run_standard, "full": run_full}
    return runners[args.level]()


if __name__ == "__main__":
    sys.exit(main())
