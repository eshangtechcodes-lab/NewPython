# -*- coding: utf-8 -*-
"""Generate dynamic compare manifests from baseline and a central case library."""
from __future__ import annotations

import copy
import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "docs" / "full_audit_baseline_20260309.json"
MANIFEST_ROOT = ROOT / "scripts" / "manifests"
MODULE_DIR = MANIFEST_ROOT / "modules"
WINDOW_DIR = MANIFEST_ROOT / "windows"
CASE_LIBRARY_PATH = MANIFEST_ROOT / "endpoint_case_library.json"
SUMMARY_PATH = MANIFEST_ROOT / "manifest_summary_20260309.json"
PLAN_PATH = ROOT / "docs" / "parallel_dynamic_test_plan_20260309.md"

DEFAULT_HEADERS = {"ProvinceCode": "340000"}
DEFAULT_TIMEOUT = 20
READ_PREFIXES = ("Get", "Binding")
ENDPOINT_OPTIONAL_KEYS = ("headers", "query", "json", "timeout", "enabled", "skip_reason", "notes")
SEEDED_CASES: Dict[str, List[Dict[str, Any]]] = {
    "BaseInfo/GetSERVERPARTList": [
        {"name": "empty-body", "json": {}},
        {
            "name": "search-model",
            "json": {
                "SearchParameter": {
                    "SERVERPART_IDS": 416,
                    "SERVERPART_ID": 416,
                    "ProvinceCode": "340000",
                },
                "PageIndex": 1,
                "PageSize": 999,
            },
        },
        {
            "name": "flat-body",
            "json": {
                "SERVERPART_IDS": 416,
                "SERVERPART_ID": 416,
                "ProvinceCode": "340000",
            },
        },
    ],
    "BaseInfo/GetServerpartDDL": [
        {"name": "default-type", "query": {"ServerpartType": "1000"}},
        {"name": "service-area-416", "query": {"SERVERPART_ID": 416}},
        {"name": "empty-query", "query": {}},
    ],
}

WINDOWS: List[Tuple[str, str, List[str]]] = [
    ("window_1", "基础与合同", ["BaseInfo", "Merchants", "Contract"]),
    ("window_2", "财务与营收", ["Finance", "Revenue", "BigData", "MobilePay"]),
    ("window_3", "批量中型模块", ["Audit", "Analysis", "BusinessMan", "Supplier", "Verification", "Sales"]),
    ("window_4", "收尾与高风险模块", ["Picture", "Video"]),
]

DEFAULT_LIBRARY_NOTES = [
    "这是动态对比测试的唯一入参源。需要调整接口入参时，优先修改本文件。",
    "修改完成后，先执行 `python scripts/generate_compare_manifests.py` 重生成 manifests，再执行 compare_api。",
    "每个接口建议至少保留 3 组 cases：空参、常规参数、边界参数。当前没有真实样本的接口会自动保留默认空参。",
    "GET 接口用 `query`，POST 接口用 `json`，如果某个接口需要特殊 Header，可在 endpoint 或 case 内补 `headers`。",
]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_baseline() -> Dict[str, Any]:
    return read_json(BASELINE_PATH)


def default_case_library() -> Dict[str, Any]:
    return {
        "version": date.today().isoformat(),
        "default_headers": copy.deepcopy(DEFAULT_HEADERS),
        "default_timeout": DEFAULT_TIMEOUT,
        "ignore_paths": [],
        "notes": copy.deepcopy(DEFAULT_LIBRARY_NOTES),
        "endpoints": {},
    }


def load_case_library() -> Dict[str, Any]:
    if CASE_LIBRARY_PATH.exists():
        return read_json(CASE_LIBRARY_PATH)
    return default_case_library()


def first_method(item: Dict[str, Any]) -> str:
    csharp = item.get("csharp") or {}
    python = item.get("python") or {}
    methods = csharp.get("methods") or python.get("methods") or ["POST"]
    return str(methods[0]).upper()


def route_name(route: str) -> str:
    return route.split("/", 1)[1] if "/" in route else route


def is_read_route(route: str) -> bool:
    return route_name(route).startswith(READ_PREFIXES)


def is_executable_route(item: Dict[str, Any]) -> bool:
    return item["status"] == "matched" and is_read_route(item["route"])


def default_cases_for_method(method: str) -> List[Dict[str, Any]]:
    if method.upper() == "GET":
        return [{"name": "default-query", "query": {}}]
    return [{"name": "default-body", "json": {}}]


def clone_cases(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return copy.deepcopy(cases)


def normalize_case_list(route: str, method: str, existing: Dict[str, Any]) -> List[Dict[str, Any]]:
    cases = existing.get("cases")
    if isinstance(cases, list) and cases:
        if route in SEEDED_CASES and cases == default_cases_for_method(method):
            return clone_cases(SEEDED_CASES[route])
        return clone_cases(cases)
    if route in SEEDED_CASES:
        return clone_cases(SEEDED_CASES[route])
    return clone_cases(default_cases_for_method(method))


def build_case_library_entry(module_name: str, item: Dict[str, Any], existing: Dict[str, Any]) -> Dict[str, Any]:
    method = str(existing.get("method") or first_method(item)).upper()
    entry: Dict[str, Any] = {
        "module": module_name,
        "method": method,
        "cases": normalize_case_list(item["route"], method, existing),
    }
    for key in ENDPOINT_OPTIONAL_KEYS:
        if key in existing:
            entry[key] = copy.deepcopy(existing[key])
    return entry


def sync_case_library(baseline: Dict[str, Any], case_library: Dict[str, Any]) -> Dict[str, Any]:
    synced = default_case_library()
    synced["default_headers"] = copy.deepcopy(case_library.get("default_headers", DEFAULT_HEADERS))
    synced["default_timeout"] = int(case_library.get("default_timeout", DEFAULT_TIMEOUT))
    synced["ignore_paths"] = copy.deepcopy(case_library.get("ignore_paths", []))
    synced["notes"] = copy.deepcopy(case_library.get("notes", DEFAULT_LIBRARY_NOTES))

    existing_endpoints = case_library.get("endpoints") or {}
    synced_endpoints: Dict[str, Any] = {}
    for module in baseline["modules"]:
        module_name = module["summary"]["module"]
        for item in module["route_items"]:
            if not is_executable_route(item):
                continue
            route = item["route"]
            existing_entry = existing_endpoints.get(route) or {}
            synced_endpoints[route] = build_case_library_entry(module_name, item, existing_entry)

    synced["endpoints"] = {route: synced_endpoints[route] for route in sorted(synced_endpoints)}
    return synced


def has_custom_endpoint_config(route: str, entry: Dict[str, Any]) -> bool:
    method = str(entry.get("method") or "POST").upper()
    if any(key in entry for key in ("headers", "query", "json", "timeout", "enabled", "skip_reason")):
        return True
    return entry.get("cases") != default_cases_for_method(method)


def build_endpoint(module_name: str, item: Dict[str, Any], entry: Dict[str, Any]) -> Dict[str, Any]:
    method = str(entry.get("method") or first_method(item)).upper()
    endpoint = {
        "name": item["route"],
        "endpoint": item["route"],
        "method": method,
        "meta": {
            "module": module_name,
            "baseline_status": item["status"],
            "method_match": item.get("method_match"),
            "param_match": item.get("param_match"),
            "csharp_source": (item.get("csharp") or {}).get("source_file"),
            "python_source": (item.get("python") or {}).get("source_file"),
            "case_library_route": str(CASE_LIBRARY_PATH),
        },
        "cases": clone_cases(entry.get("cases") or default_cases_for_method(method)),
    }
    for key in ENDPOINT_OPTIONAL_KEYS:
        if key in entry:
            endpoint[key] = copy.deepcopy(entry[key])
    return endpoint


def build_manifest(
    name: str,
    note: str,
    modules: List[Dict[str, Any]],
    case_library: Dict[str, Any],
) -> Dict[str, Any]:
    endpoints: List[Dict[str, Any]] = []
    module_names: List[str] = []
    case_entries = case_library.get("endpoints") or {}
    for module in modules:
        module_name = module["summary"]["module"]
        module_names.append(module_name)
        for item in module["route_items"]:
            if is_executable_route(item):
                route = item["route"]
                entry = case_entries.get(route) or build_case_library_entry(module_name, item, {})
                endpoints.append(build_endpoint(module_name, item, entry))

    return {
        "name": name,
        "note": note,
        "case_library_path": str(CASE_LIBRARY_PATH),
        "old_api_base": "http://192.168.1.99:8900/EShangApiMain",
        "new_api_base": "http://localhost:8080/EShangApiMain",
        "default_headers": copy.deepcopy(case_library.get("default_headers", DEFAULT_HEADERS)),
        "default_timeout": int(case_library.get("default_timeout", DEFAULT_TIMEOUT)),
        "diff_limit": 25,
        "ignore_paths": copy.deepcopy(case_library.get("ignore_paths", [])),
        "module_scope": module_names,
        "endpoints": endpoints,
    }


def module_summary(module: Dict[str, Any], manifest: Dict[str, Any], case_library: Dict[str, Any]) -> Dict[str, Any]:
    summary = dict(module["summary"])
    case_entries = case_library.get("endpoints") or {}
    summary["execution_manifest_total"] = len(manifest["endpoints"])
    summary["excluded_non_read"] = sum(
        1 for item in module["route_items"] if item["status"] == "matched" and not is_read_route(item["route"])
    )
    summary["excluded_missing_in_python"] = sum(
        1 for item in module["route_items"] if item["status"] == "missing_in_python"
    )
    summary["excluded_python_only"] = sum(1 for item in module["route_items"] if item["status"] == "python_only")
    summary["custom_case_routes"] = sum(
        1
        for ep in manifest["endpoints"]
        if has_custom_endpoint_config(ep["endpoint"], case_entries.get(ep["endpoint"], {}))
    )
    return summary


def window_summary(
    window_id: str,
    window_name: str,
    manifest: Dict[str, Any],
    modules: List[Dict[str, Any]],
    case_library: Dict[str, Any],
) -> Dict[str, Any]:
    case_entries = case_library.get("endpoints") or {}
    return {
        "window_id": window_id,
        "window_name": window_name,
        "modules": [module["summary"]["module"] for module in modules],
        "csharp_unique_routes": sum(module["summary"]["csharp_unique_routes"] for module in modules),
        "python_runtime_routes": sum(module["summary"]["python_runtime_routes"] for module in modules),
        "matched_routes": sum(module["summary"]["matched_routes"] for module in modules),
        "missing_in_python": sum(module["summary"]["missing_in_python"] for module in modules),
        "python_only_routes": sum(module["summary"]["python_only_routes"] for module in modules),
        "execution_manifest_total": len(manifest["endpoints"]),
        "excluded_non_read": sum(
            1
            for module in modules
            for item in module["route_items"]
            if item["status"] == "matched" and not is_read_route(item["route"])
        ),
        "excluded_missing_in_python": sum(
            1 for module in modules for item in module["route_items"] if item["status"] == "missing_in_python"
        ),
        "excluded_python_only": sum(
            1 for module in modules for item in module["route_items"] if item["status"] == "python_only"
        ),
        "custom_case_routes": sum(
            1
            for ep in manifest["endpoints"]
            if has_custom_endpoint_config(ep["endpoint"], case_entries.get(ep["endpoint"], {}))
        ),
    }


def render_plan(module_summaries: List[Dict[str, Any]], window_summaries: List[Dict[str, Any]]) -> str:
    lines = [
        "# 多窗口动态测试执行计划",
        "",
        f"- 日期：{date.today().isoformat()}",
        "- 路由真源：`docs/full_audit_baseline_20260309.json`",
        "- 入参总配置：`scripts/manifests/endpoint_case_library.json`",
        "- 业务范围：以 `docs/collaboration_plan.md` 中 15 个模块为准，实际可执行数量按机器基线收口。",
        "- 默认 Header：`{\"ProvinceCode\":\"340000\"}`，如需统一调整，请改入参总配置。",
        "- 执行限制：`不允许真实写接口`，因此执行 manifest 只保留 `matched + 读接口`。",
        "",
        "## 推荐流程",
        "",
        "1. 先编辑 `scripts/manifests/endpoint_case_library.json`，补真实 `cases/query/json/headers`。",
        "2. 再执行 `python scripts/generate_compare_manifests.py` 重生成 modules/windows manifests。",
        "3. 最后执行 `compare_api.py` 跑动态对比。",
        "",
        "## 模块数量",
        "",
        "| 模块 | C# 路由数 | Python 路由数 | matched | missing | extra | 执行manifest | 排除写接口 | 排除缺失 | 排除多出 | 已配真实参数 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for summary in module_summaries:
        lines.append(
            f"| {summary['module']} | {summary['csharp_unique_routes']} | {summary['python_runtime_routes']} | "
            f"{summary['matched_routes']} | {summary['missing_in_python']} | {summary['python_only_routes']} | "
            f"{summary['execution_manifest_total']} | {summary['excluded_non_read']} | "
            f"{summary['excluded_missing_in_python']} | {summary['excluded_python_only']} | "
            f"{summary['custom_case_routes']} |"
        )

    lines.extend(
        [
            "",
            "## 窗口分组",
            "",
            "| 窗口 | 模块 | C# 总数 | matched | 执行manifest | 排除写接口 | 排除缺失 | 排除多出 | 已配真实参数 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for summary in window_summaries:
        lines.append(
            f"| {summary['window_id']} {summary['window_name']} | {', '.join(summary['modules'])} | "
            f"{summary['csharp_unique_routes']} | {summary['matched_routes']} | {summary['execution_manifest_total']} | "
            f"{summary['excluded_non_read']} | {summary['excluded_missing_in_python']} | "
            f"{summary['excluded_python_only']} | {summary['custom_case_routes']} |"
        )

    lines.extend(
        [
            "",
            "## 执行命令",
            "",
            "重生成 manifests：",
            "",
            "`python scripts/generate_compare_manifests.py`",
            "",
            "单窗口执行：",
            "",
        ]
    )
    for summary in window_summaries:
        report_name = f"docs/{summary['window_id']}_dynamic_compare_report.md"
        manifest_name = f"scripts/manifests/windows/{summary['window_id']}.json"
        lines.extend(
            [
                f"`python scripts/compare_api.py --manifest {manifest_name} --report {report_name}`",
                "",
            ]
        )

    lines.extend(
        [
            "并行开 4 个窗口：",
            "",
            "`powershell -ExecutionPolicy Bypass -File scripts/start_parallel_compare_windows.ps1`",
            "",
            "## 使用说明",
            "",
            "- `endpoint_case_library.json`：全部接口测试入参的唯一配置入口。",
            "- `modules/*.json`：按模块拆分的执行 manifest，由脚本自动生成。",
            "- `windows/*.json`：按窗口聚合的执行 manifest，由脚本自动生成。",
            "- 当前执行 manifest 不再包含写接口、Python 缺失接口、Python 多出接口。",
            "- 全接口数量仍保留在 `manifest_summary_20260309.json` 和本计划文档里，用来做完整性统计。",
            "- 如需补某个接口的真实参数，只改 `endpoint_case_library.json`，不要手工长期维护 `window_*.json`。",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    baseline = load_baseline()
    raw_case_library = load_case_library()
    case_library = sync_case_library(baseline, raw_case_library)

    MODULE_DIR.mkdir(parents=True, exist_ok=True)
    WINDOW_DIR.mkdir(parents=True, exist_ok=True)

    write_json(CASE_LIBRARY_PATH, case_library)

    module_map = {module["summary"]["module"]: module for module in baseline["modules"]}
    module_summaries: List[Dict[str, Any]] = []
    window_summaries: List[Dict[str, Any]] = []

    for module_name, module in module_map.items():
        manifest = build_manifest(
            name=f"{module_name} dynamic compare manifest",
            note=f"{module_name} 动态执行 manifest；仅保留 matched + 读接口。",
            modules=[module],
            case_library=case_library,
        )
        module_path = MODULE_DIR / f"{module_name.lower()}.json"
        write_json(module_path, manifest)
        module_summaries.append(module_summary(module, manifest, case_library))

    for window_id, window_name, module_names in WINDOWS:
        modules = [module_map[name] for name in module_names]
        manifest = build_manifest(
            name=f"{window_id} dynamic compare manifest",
            note=f"{window_name} 窗口并行测试 manifest；仅保留可执行读接口。",
            modules=modules,
            case_library=case_library,
        )
        manifest["report_path"] = f"docs/{window_id}_dynamic_compare_report.md"
        window_path = WINDOW_DIR / f"{window_id}.json"
        write_json(window_path, manifest)
        window_summaries.append(window_summary(window_id, window_name, manifest, modules, case_library))

    write_json(SUMMARY_PATH, {"modules": module_summaries, "windows": window_summaries})
    PLAN_PATH.write_text(render_plan(module_summaries, window_summaries), encoding="utf-8")

    print(f"Wrote case library to: {CASE_LIBRARY_PATH}")
    print(f"Wrote module manifests to: {MODULE_DIR}")
    print(f"Wrote window manifests to: {WINDOW_DIR}")
    print(f"Wrote summary to: {SUMMARY_PATH}")
    print(f"Wrote plan to: {PLAN_PATH}")


if __name__ == "__main__":
    main()
