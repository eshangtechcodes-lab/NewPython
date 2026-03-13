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

# === 冒烟测试端点 ===
# expect_data: True 表示期望 Result_Data 非空（用于校验返回体）
SMOKE_ENDPOINTS = [
    # ── 系统 ──
    {"path": "/health", "method": "GET", "name": "健康检查"},
    {"path": "/", "method": "GET", "name": "根路径"},

    # ── CommercialApi / BaseInfo ──
    {"path": "/CommercialApi/BaseInfo/GetServerpartList", "method": "GET", "name": "CA-服务区列表",
     "expect_data": True},
    {"path": "/CommercialApi/BaseInfo/GetSPRegionList", "method": "GET",
     "params": {"Province_Code": "340000"}, "name": "CA-区域列表", "expect_data": True},
    {"path": "/CommercialApi/BaseInfo/GetBusinessTradeList", "method": "GET",
     "params": {"Province_Code": "340000"}, "name": "CA-业态列表"},

    # ── CommercialApi / Revenue（高频） ──
    {"path": "/CommercialApi/Revenue/GetCurRevenue", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "CA-当前营收"},
    {"path": "/CommercialApi/Revenue/GetRevenueReport", "method": "GET",
     "params": {"provinceCode": "340000", "startTime": "2025-12-01", "endTime": "2025-12-31"},
     "name": "CA-营收报告", "expect_data": True},
    {"path": "/CommercialApi/Revenue/GetRevenueTrend", "method": "GET",
     "params": {"ProvinceCode": "340000", "StatisticsDate": "2025", "StatisticsType": "1"},
     "name": "CA-营收趋势"},
    {"path": "/CommercialApi/Revenue/GetRevenueYOY", "method": "GET",
     "params": {"pushProvinceCode": "340000", "StatisticsStartDate": "2025-12-01",
                "StatisticsEndDate": "2025-12-07"}, "name": "CA-营收同比"},
    {"path": "/CommercialApi/Revenue/GetSPRevenueRank", "method": "GET",
     "params": {"pushProvinceCode": "340000", "Statistics_Date": "2025-12-01"},
     "name": "CA-服务区排行"},
    {"path": "/CommercialApi/Revenue/GetMobileShare", "method": "GET",
     "params": {"Province_Code": "340000", "StatisticsStartDate": "2025-12-01",
                "StatisticsEndDate": "2025-12-31"}, "name": "CA-移动支付"},
    {"path": "/CommercialApi/Revenue/GetTransactionAnalysis", "method": "GET",
     "params": {"Province_Code": "340000", "Statistics_Date": "2025-12-01",
                "Serverpart_ID": "416"}, "name": "CA-客单分析"},
    {"path": "/CommercialApi/Revenue/GetBusinessTradeRevenue", "method": "GET",
     "params": {"ProvinceCode": "340000", "StatisticsDate": "2025-12-01"},
     "name": "CA-业态营收"},
    {"path": "/CommercialApi/Revenue/GetLastSyncDateTime", "method": "GET",
     "params": {"ProvinceCode": "340000"}, "name": "CA-同步时间"},
    {"path": "/CommercialApi/Revenue/GetSalableCommodity", "method": "GET",
     "name": "CA-畅销商品", "expect_data": True},
    {"path": "/CommercialApi/Revenue/GetCompanyRevenueReport", "method": "GET",
     "params": {"provinceCode": "340000", "startTime": "2025-12-01", "endTime": "2025-12-31"},
     "name": "CA-公司营收报表"},

    # ── CommercialApi / BigData ──
    {"path": "/CommercialApi/BigData/GetDateAnalysis", "method": "GET",
     "params": {"ServerpartId": "416", "StatisticsDate": "2025-12-01"}, "name": "CA-日期分析"},
    {"path": "/CommercialApi/Revenue/GetBayonetEntryList", "method": "GET",
     "params": {"Province_Code": "340000", "StatisticsDate": "2025-12-01"},
     "name": "CA-入区车流"},
    {"path": "/CommercialApi/Revenue/GetBayonetRankList", "method": "GET",
     "params": {"Province_Code": "340000", "statisticsDate": "2025-12-01"},
     "name": "CA-车流排行"},
    {"path": "/CommercialApi/BigData/GetMonthAnalysis", "method": "GET",
     "params": {"Province_Code": "340000", "StatisticsDate": "202512"},
     "name": "CA-月度车流"},

    # ── CommercialApi / Examine ──
    {"path": "/CommercialApi/Examine/GetExamineAnalysis", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "CA-考核分析"},
    {"path": "/CommercialApi/Examine/GetExamineResultList", "method": "GET",
     "params": {"Province_Code": "340000"}, "name": "CA-考核结果列表"},

    # ── CommercialApi / Customer ──
    {"path": "/CommercialApi/Customer/GetCustomerRatio", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "CA-客群占比"},
    {"path": "/CommercialApi/Customer/GetCustomerGroupRatio", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "CA-客群分组"},

    # ── CommercialApi / Analysis ──
    {"path": "/CommercialApi/Analysis/GetANALYSISINSDetail", "method": "GET",
     "params": {"Province_Code": "340000", "AnalysisIns_Id": "1"}, "name": "CA-分析详情"},

    # ── CommercialApi / Budget ──
    {"path": "/CommercialApi/Revenue/GetRevenueBudget", "method": "GET",
     "params": {"Province_Code": "340000", "Statistics_Date": "2025-12-01"},
     "name": "CA-营收预算"},

    # ── CommercialApi / Contract ──
    {"path": "/CommercialApi/Contract/GetContractAnalysis", "method": "GET",
     "params": {"Province_Code": "340000"}, "name": "CA-合同分析"},

    # ── EShangApiMain — 核心 CRUD 模块 ──
    {"path": "/EShangApiMain/BaseInfo/GetBrandList", "method": "POST",
     "json": {}, "name": "EA-品牌列表", "expect_data": True},
    {"path": "/EShangApiMain/BaseInfo/GetServerpartShopList", "method": "POST",
     "json": {}, "name": "EA-门店列表", "expect_data": True},
    {"path": "/EShangApiMain/BaseInfo/GetOWNERUNITList", "method": "POST",
     "json": {}, "name": "EA-业主单位列表", "expect_data": True},
    {"path": "/EShangApiMain/BaseInfo/GetCASHWORKERList", "method": "POST",
     "json": {}, "name": "EA-收银人员列表"},
    {"path": "/EShangApiMain/BaseInfo/GetCOMMODITYList", "method": "POST",
     "json": {}, "name": "EA-商品列表"},
    {"path": "/EShangApiMain/Contract/GetRegisterCompactList", "method": "POST",
     "json": {}, "name": "EA-合同列表", "expect_data": True},
    {"path": "/EShangApiMain/BusinessProject/GetBusinessProjectList", "method": "POST",
     "json": {}, "name": "EA-经营项目列表"},
    {"path": "/EShangApiMain/Budget/GetBudgetProjectList", "method": "POST",
     "json": {}, "name": "EA-预算列表"},
    {"path": "/EShangApiMain/Revenue/GetTotalRevenue", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "EA-总营收"},
    {"path": "/EShangApiMain/Commodity/GetCOMMODITYList", "method": "POST",
     "json": {}, "name": "EA-商品管理列表"},
    {"path": "/EShangApiMain/ShopVideo/GetShopVideoInfo", "method": "GET",
     "params": {"ServerpartId": "416"}, "name": "EA-视频监控"},
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
    """冒烟测试：核心接口响应码 + 关键字段校验"""
    print_header(f"SMOKE TEST - 冒烟测试（{len(SMOKE_ENDPOINTS)} 个端点）")

    if not check_api_available(NEW_API_BASE):
        print(f"\n[ERROR] 新 API ({NEW_API_BASE}) 不可用，请先启动服务！")
        print(f"  启动命令: python main.py")
        return 1

    passed, failed, warned, errors = 0, 0, 0, []
    start = time.time()
    headers = {"ProvinceCode": "340000"}

    for i, ep in enumerate(SMOKE_ENDPOINTS, 1):
        try:
            url = f"{NEW_API_BASE}{ep['path']}"
            if ep["method"] == "GET":
                r = requests.get(url, params=ep.get("params"), headers=headers, timeout=15)
            else:
                r = requests.post(url, json=ep.get("json", {}), headers=headers, timeout=15)

            # 判定标准：HTTP 200 且 Result_Code 为 100 或 200
            ok = False
            warn_msg = ""
            if r.status_code == 200:
                try:
                    body = r.json()
                    code = body.get("Result_Code")
                    if code in (100, 200, "100", "200"):
                        ok = True
                        # 通过 expect_data 校验返回数据非空
                        if ep.get("expect_data"):
                            data = body.get("Result_Data") or body.get("data")
                            if not data:
                                warn_msg = "WARN:data=null"
                                warned += 1
                    elif ep["path"] in ("/", "/health"):
                        ok = True  # 系统端点不一定有 Result_Code
                except Exception:
                    pass

            status = "PASS" if ok else "FAIL"
            elapsed = r.elapsed.total_seconds() * 1000
            suffix = f"  {warn_msg}" if warn_msg else ""
            print(f"  [{i:2d}/{len(SMOKE_ENDPOINTS)}] {status} {ep['name']:22s} {elapsed:7.0f}ms  {ep['path']}{suffix}")

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
    print(f"  SMOKE RESULT: PASS {passed} / FAIL {failed} / WARN {warned} / TOTAL {len(SMOKE_ENDPOINTS)}")
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
        "passed": passed, "failed": failed, "warned": warned, "total": len(SMOKE_ENDPOINTS),
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
