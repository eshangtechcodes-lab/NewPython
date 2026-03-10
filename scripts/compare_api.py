# -*- coding: utf-8 -*-
"""通用 API 对比脚本，支持单接口和 manifest 批量对比。"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENDPOINT = "BaseInfo/GetSERVERPARTCRTList"
DEFAULT_OLD_API_BASE = "http://192.168.1.99:8900/EShangApiMain"
DEFAULT_NEW_API_BASE = "http://localhost:8080/EShangApiMain"
DEFAULT_HEADERS = {"ProvinceCode": "340000"}
DEFAULT_TIMEOUT = 20
DEFAULT_DIFF_LIMIT = 25
DEFAULT_REPORT = ROOT / "scripts" / "compare_result.md"


def deep_merge(base: Optional[Dict[str, Any]], override: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """浅层合并 dict，用于 headers/query/json 配置。"""
    result = copy.deepcopy(base or {})
    for key, value in (override or {}).items():
        result[key] = value
    return result


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return ROOT / path


def load_json_value(raw_value: Optional[str]) -> Optional[Dict[str, Any]]:
    if raw_value is None:
        return None
    return json.loads(raw_value)


def render_path(path_parts: Sequence[Any]) -> str:
    if not path_parts:
        return "<root>"
    chunks: List[str] = []
    for part in path_parts:
        if isinstance(part, int):
            chunks.append(f"[{part}]")
        elif not chunks:
            chunks.append(str(part))
        else:
            chunks.append(f".{part}")
    return "".join(chunks)


def should_ignore(path_parts: Sequence[Any], ignored_paths: Iterable[str]) -> bool:
    path = render_path(path_parts)
    for ignored in ignored_paths:
        if path == ignored or path.startswith(f"{ignored}.") or path.startswith(f"{ignored}["):
            return True
    return False


def type_name(value: Any) -> str:
    return type(value).__name__


def compare_values(
    old_value: Any,
    new_value: Any,
    path_parts: Sequence[Any],
    diffs: List[str],
    ignored_paths: Iterable[str],
    diff_limit: int,
) -> None:
    if len(diffs) >= diff_limit or should_ignore(path_parts, ignored_paths):
        return

    current_path = render_path(path_parts)

    if isinstance(old_value, dict) and isinstance(new_value, dict):
        old_keys = set(old_value.keys())
        new_keys = set(new_value.keys())
        for key in sorted(old_keys - new_keys):
            diffs.append(f"{current_path}.{key}: 新 API 缺少该字段")
            if len(diffs) >= diff_limit:
                return
        for key in sorted(new_keys - old_keys):
            diffs.append(f"{current_path}.{key}: 新 API 多出该字段")
            if len(diffs) >= diff_limit:
                return
        for key in sorted(old_keys & new_keys):
            compare_values(old_value[key], new_value[key], [*path_parts, key], diffs, ignored_paths, diff_limit)
            if len(diffs) >= diff_limit:
                return
        return

    if isinstance(old_value, list) and isinstance(new_value, list):
        if len(old_value) != len(new_value):
            diffs.append(f"{current_path}: 列表长度不一致 ({len(old_value)} vs {len(new_value)})")
            if len(diffs) >= diff_limit:
                return
        for index, (old_item, new_item) in enumerate(zip(old_value, new_value)):
            compare_values(old_item, new_item, [*path_parts, index], diffs, ignored_paths, diff_limit)
            if len(diffs) >= diff_limit:
                return
        return

    if type(old_value) != type(new_value):
        diffs.append(
            f"{current_path}: 类型不一致 ({type_name(old_value)} vs {type_name(new_value)})，"
            f"值为 {old_value!r} vs {new_value!r}"
        )
        return

    if old_value != new_value:
        diffs.append(f"{current_path}: 值不一致 ({old_value!r} vs {new_value!r})")


def compare_list_item_fields(old_data: Any, new_data: Any) -> Tuple[bool, str]:
    if not isinstance(old_data, list) or not isinstance(new_data, list):
        return False, "至少一侧不是 List"
    if not old_data or not new_data:
        return True, "至少一侧为空列表，跳过字段扫描"
    if not isinstance(old_data[0], dict) or not isinstance(new_data[0], dict):
        return True, "首项不是对象列表，跳过字段扫描"
    old_fields = set(old_data[0].keys())
    new_fields = set(new_data[0].keys())
    if old_fields == new_fields:
        return True, f"字段一致，共 {len(old_fields)} 个"
    return False, f"仅原 API: {sorted(old_fields - new_fields)} | 仅新 API: {sorted(new_fields - old_fields)}"


def call_api(
    session: requests.Session,
    base_url: str,
    endpoint: str,
    method: str,
    headers: Dict[str, Any],
    params: Optional[Dict[str, Any]],
    json_body: Optional[Dict[str, Any]],
    timeout: int,
) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    request_kwargs: Dict[str, Any] = {"headers": headers, "timeout": timeout}
    if params is not None:
        request_kwargs["params"] = params
    if json_body is not None and method not in {"GET", "HEAD"}:
        request_kwargs["json"] = json_body

    try:
        response = session.request(method=method, url=url, **request_kwargs)
        try:
            response_json = response.json()
            parse_error = None
        except ValueError as exc:
            response_json = None
            parse_error = str(exc)
        return {
            "ok": True,
            "url": url,
            "status_code": response.status_code,
            "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 2),
            "json": response_json,
            "text": response.text[:4000],
            "parse_error": parse_error,
        }
    except Exception as exc:
        return {
            "ok": False,
            "url": url,
            "status_code": None,
            "elapsed_ms": None,
            "json": None,
            "text": None,
            "parse_error": None,
            "error": str(exc),
        }


def build_checks(
    old_response: Dict[str, Any],
    new_response: Dict[str, Any],
    ignored_paths: Iterable[str],
    diff_limit: int,
) -> Tuple[List[Tuple[str, bool, str]], List[str]]:
    checks: List[Tuple[str, bool, str]] = []
    diffs: List[str] = []

    checks.append(
        (
            "接口可达",
            old_response.get("ok", False) and new_response.get("ok", False),
            f"原 API: {old_response.get('url')} | 新 API: {new_response.get('url')}",
        )
    )

    if not old_response.get("ok") or not new_response.get("ok"):
        if not old_response.get("ok"):
            diffs.append(f"原 API 调用失败: {old_response.get('error')}")
        if not new_response.get("ok"):
            diffs.append(f"新 API 调用失败: {new_response.get('error')}")
        return checks, diffs

    checks.append(
        (
            "HTTP 状态码",
            old_response["status_code"] == new_response["status_code"],
            f"{old_response['status_code']} vs {new_response['status_code']}",
        )
    )

    old_json = old_response.get("json")
    new_json = new_response.get("json")
    old_parse_ok = old_json is not None and old_response.get("parse_error") is None
    new_parse_ok = new_json is not None and new_response.get("parse_error") is None
    checks.append(("响应可解析 JSON", old_parse_ok and new_parse_ok, f"原 API: {old_parse_ok} | 新 API: {new_parse_ok}"))
    if not old_parse_ok or not new_parse_ok:
        if old_response.get("parse_error"):
            diffs.append(f"原 API JSON 解析失败: {old_response['parse_error']}")
        if new_response.get("parse_error"):
            diffs.append(f"新 API JSON 解析失败: {new_response['parse_error']}")
        return checks, diffs

    if isinstance(old_json, dict) and isinstance(new_json, dict):
        checks.append(
            (
                "顶层字段",
                set(old_json.keys()) == set(new_json.keys()),
                f"{sorted(old_json.keys())} vs {sorted(new_json.keys())}",
            )
        )
        if "Result_Code" in old_json or "Result_Code" in new_json:
            checks.append(
                (
                    "Result_Code",
                    old_json.get("Result_Code") == new_json.get("Result_Code"),
                    f"{old_json.get('Result_Code')} vs {new_json.get('Result_Code')}",
                )
            )
        if "Result_Desc" in old_json or "Result_Desc" in new_json:
            checks.append(
                (
                    "Result_Desc",
                    old_json.get("Result_Desc") == new_json.get("Result_Desc"),
                    f"{old_json.get('Result_Desc')} vs {new_json.get('Result_Desc')}",
                )
            )

        old_data = old_json.get("Result_Data")
        new_data = new_json.get("Result_Data")
        checks.append(
            (
                "Result_Data 类型",
                type_name(old_data) == type_name(new_data),
                f"{type_name(old_data)} vs {type_name(new_data)}",
            )
        )
        if isinstance(old_data, dict) and isinstance(new_data, dict):
            checks.append(
                (
                    "Result_Data 字段",
                    set(old_data.keys()) == set(new_data.keys()),
                    f"{sorted(old_data.keys())} vs {sorted(new_data.keys())}",
                )
            )
            for key in ("TotalCount", "PageIndex", "PageSize"):
                if key in old_data or key in new_data:
                    checks.append((key, old_data.get(key) == new_data.get(key), f"{old_data.get(key)} vs {new_data.get(key)}"))
            if "OtherData" in old_data or "OtherData" in new_data:
                checks.append(
                    (
                        "OtherData 存在性",
                        ("OtherData" in old_data) == ("OtherData" in new_data),
                        f"{'OtherData' in old_data} vs {'OtherData' in new_data}",
                    )
                )
            old_list = old_data.get("List")
            new_list = new_data.get("List")
            if "List" in old_data or "List" in new_data:
                checks.append(
                    (
                        "List 条数",
                        isinstance(old_list, list) and isinstance(new_list, list) and len(old_list) == len(new_list),
                        f"{len(old_list) if isinstance(old_list, list) else 'N/A'} vs {len(new_list) if isinstance(new_list, list) else 'N/A'}",
                    )
                )
                field_ok, field_detail = compare_list_item_fields(old_list, new_list)
                checks.append(("首条字段集合", field_ok, field_detail))

    compare_values(old_json, new_json, [], diffs, ignored_paths, diff_limit)
    checks.append(("完整响应体", len(diffs) == 0, "完全一致" if not diffs else f"发现 {len(diffs)} 处差异"))
    return checks, diffs


def prepare_case(manifest: Dict[str, Any], endpoint_config: Dict[str, Any], case_config: Dict[str, Any]) -> Dict[str, Any]:
    method = str(case_config.get("method") or endpoint_config.get("method") or "POST").upper()
    headers = deep_merge(manifest.get("default_headers"), endpoint_config.get("headers"))
    headers = deep_merge(headers, case_config.get("headers"))
    params = deep_merge(endpoint_config.get("query"), case_config.get("query"))
    json_body = deep_merge(endpoint_config.get("json"), case_config.get("json"))

    if method in {"GET", "HEAD"} and not params and json_body:
        params = json_body
        json_body = None

    return {
        "name": case_config.get("name", "default"),
        "method": method,
        "headers": headers,
        "params": params or None,
        "json_body": json_body or None,
        "timeout": int(case_config.get("timeout") or endpoint_config.get("timeout") or manifest.get("default_timeout") or DEFAULT_TIMEOUT),
        "enabled": case_config.get("enabled", endpoint_config.get("enabled", True)),
        "skip_reason": case_config.get("skip_reason") or endpoint_config.get("skip_reason"),
    }


def load_manifest(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    manifest.setdefault("old_api_base", DEFAULT_OLD_API_BASE)
    manifest.setdefault("new_api_base", DEFAULT_NEW_API_BASE)
    manifest.setdefault("default_headers", DEFAULT_HEADERS)
    manifest.setdefault("default_timeout", DEFAULT_TIMEOUT)
    manifest.setdefault("diff_limit", DEFAULT_DIFF_LIMIT)
    manifest.setdefault("ignore_paths", [])
    manifest.setdefault("report_path", str(DEFAULT_REPORT))
    manifest.setdefault("endpoints", [])
    # endpoint_case_library 格式：endpoints 是 dict（endpoint_name→config）
    # run_manifest 需要 list 格式，自动转换
    if isinstance(manifest["endpoints"], dict):
        ep_list = []
        for ep_name, ep_config in manifest["endpoints"].items():
            ep_item = {
                "name": ep_name,
                "endpoint": ep_name,
                "method": ep_config.get("method", "POST"),
                "meta": {"module": ep_config.get("module", "")},
                "cases": ep_config.get("cases", [{"name": "default"}]),
            }
            ep_list.append(ep_item)
        manifest["endpoints"] = ep_list
    return manifest


def build_manifest_from_cli(args: argparse.Namespace) -> Dict[str, Any]:
    json_body = load_json_value(args.json_body)
    query = load_json_value(args.query)
    headers = deep_merge(DEFAULT_HEADERS, load_json_value(args.headers))
    endpoint = args.endpoint or DEFAULT_ENDPOINT
    return {
        "old_api_base": args.old_base or DEFAULT_OLD_API_BASE,
        "new_api_base": args.new_base or DEFAULT_NEW_API_BASE,
        "default_headers": headers,
        "default_timeout": args.timeout or DEFAULT_TIMEOUT,
        "diff_limit": DEFAULT_DIFF_LIMIT,
        "ignore_paths": [],
        "report_path": str(resolve_path(args.report)) if args.report else str(DEFAULT_REPORT),
        "endpoints": [
            {
                "name": endpoint,
                "endpoint": endpoint,
                "method": args.method,
                "cases": [
                    {
                        "name": args.case_name or "default",
                        "query": query,
                        "json": json_body if json_body is not None else ({} if args.method.upper() != "GET" else None),
                    }
                ],
            }
        ],
    }


def format_case_report(endpoint_config: Dict[str, Any], case_request: Dict[str, Any], result: Dict[str, Any]) -> List[str]:
    result_label = "PASS" if result["status"] == "pass" else ("SKIP" if result["status"] == "skip" else "FAIL")
    lines = [
        f"### {endpoint_config['endpoint']} / {case_request['name']}",
        "",
        f"- 方法: `{case_request['method']}`",
        f"- Headers: `{json.dumps(case_request['headers'], ensure_ascii=False, sort_keys=True)}`",
        f"- Query: `{json.dumps(case_request['params'], ensure_ascii=False, sort_keys=True) if case_request['params'] is not None else 'null'}`",
        f"- JSON: `{json.dumps(case_request['json_body'], ensure_ascii=False, sort_keys=True) if case_request['json_body'] is not None else 'null'}`",
        f"- 结果: `{result_label}`",
        "",
        "| 检查项 | 结果 | 说明 |",
        "| --- | --- | --- |",
    ]
    for name, ok, detail in result["checks"]:
        lines.append(f"| {name} | {'✅' if ok else '❌'} | {detail} |")
    if result["diffs"]:
        lines.extend(["", "差异明细："])
        for diff in result["diffs"]:
            lines.append(f"- {diff}")
    lines.extend(
        [
            "",
            f"原 API 状态: `{result['old_response'].get('status_code')}`，耗时 `{result['old_response'].get('elapsed_ms')} ms`",
            f"新 API 状态: `{result['new_response'].get('status_code')}`，耗时 `{result['new_response'].get('elapsed_ms')} ms`",
            "",
        ]
    )
    return lines


def format_report(manifest_source: str, manifest: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
    passed_cases = sum(1 for result in results if result["status"] == "pass")
    skipped_cases = sum(1 for result in results if result["status"] == "skip")
    failed_cases = sum(1 for result in results if result["status"] == "fail")
    total_cases = len(results)
    lines = [
        "# 动态接口对比报告",
        "",
        f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Manifest: `{manifest_source}`",
        f"- 原 API: `{manifest['old_api_base']}`",
        f"- 新 API: `{manifest['new_api_base']}`",
        f"- 默认 Header: `{json.dumps(manifest.get('default_headers', {}), ensure_ascii=False, sort_keys=True)}`",
        f"- 总结果: `PASS {passed_cases} / FAIL {failed_cases} / SKIP {skipped_cases} / TOTAL {total_cases}`",
        "",
        "## 用例明细",
        "",
    ]
    for result in results:
        lines.extend(format_case_report(result["endpoint_config"], result["case_request"], result))
    return "\n".join(lines).strip() + "\n"


def build_report_summary(
    manifest_source: str,
    manifest: Dict[str, Any],
    results: List[Dict[str, Any]],
    report_path: Path,
) -> Dict[str, Any]:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {
        "generated_at": generated_at,
        "manifest_source": manifest_source,
        "report_path": str(report_path),
        "old_api_base": manifest["old_api_base"],
        "new_api_base": manifest["new_api_base"],
        "default_headers": manifest.get("default_headers", {}),
        "module_scope": manifest.get("module_scope", []),
        "counts": {
            "pass": sum(1 for result in results if result["status"] == "pass"),
            "fail": sum(1 for result in results if result["status"] == "fail"),
            "skip": sum(1 for result in results if result["status"] == "skip"),
            "total": len(results),
        },
        "cases": [],
    }
    for result in results:
        case_item = {
            "endpoint": result["endpoint_config"]["endpoint"],
            "case_name": result["case_request"]["name"],
            "method": result["case_request"]["method"],
            "status": result["status"],
            "query": result["case_request"]["params"],
            "json_body": result["case_request"]["json_body"],
            "checks": [
                {"name": name, "ok": ok, "detail": detail}
                for name, ok, detail in result["checks"]
            ],
            "diffs": result["diffs"],
            "old_status_code": result["old_response"].get("status_code"),
            "new_status_code": result["new_response"].get("status_code"),
        }
        summary["cases"].append(case_item)
    return summary


def run_manifest(manifest: Dict[str, Any], dry_run: bool = False) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    total_cases = sum(len(endpoint_config.get("cases") or [{"name": "default"}]) for endpoint_config in manifest.get("endpoints", []))
    case_index = 0
    with requests.Session() as session:
        for endpoint_config in manifest.get("endpoints", []):
            endpoint = endpoint_config["endpoint"]
            cases = endpoint_config.get("cases") or [{"name": "default"}]
            for case_config in cases:
                case_index += 1
                case_request = prepare_case(manifest, endpoint_config, case_config)
                print(f"[{case_index}/{total_cases}] {case_request['method']} {endpoint} / {case_request['name']}", flush=True)
                if not case_request["enabled"]:
                    print(f"  -> SKIP: {case_request.get('skip_reason') or '该接口按当前策略不执行'}", flush=True)
                    results.append(
                        {
                            "endpoint_config": endpoint_config,
                            "case_request": case_request,
                            "status": "skip",
                            "passed": False,
                            "checks": [("Skip", True, case_request.get("skip_reason") or "该接口按当前策略不执行")],
                            "diffs": [],
                            "old_response": {"status_code": None, "elapsed_ms": None},
                            "new_response": {"status_code": None, "elapsed_ms": None},
                        }
                    )
                    continue
                if dry_run:
                    print("  -> DRY RUN", flush=True)
                    results.append(
                        {
                            "endpoint_config": endpoint_config,
                            "case_request": case_request,
                            "status": "pass",
                            "passed": True,
                            "checks": [("Dry Run", True, f"{case_request['method']} {endpoint}")],
                            "diffs": [],
                            "old_response": {"status_code": None, "elapsed_ms": None},
                            "new_response": {"status_code": None, "elapsed_ms": None},
                        }
                    )
                    continue

                old_response = call_api(
                    session=session,
                    base_url=manifest["old_api_base"],
                    endpoint=endpoint,
                    method=case_request["method"],
                    headers=case_request["headers"],
                    params=case_request["params"],
                    json_body=case_request["json_body"],
                    timeout=case_request["timeout"],
                )
                new_response = call_api(
                    session=session,
                    base_url=manifest["new_api_base"],
                    endpoint=endpoint,
                    method=case_request["method"],
                    headers=case_request["headers"],
                    params=case_request["params"],
                    json_body=case_request["json_body"],
                    timeout=case_request["timeout"],
                )
                checks, diffs = build_checks(
                    old_response=old_response,
                    new_response=new_response,
                    ignored_paths=manifest.get("ignore_paths", []),
                    diff_limit=int(manifest.get("diff_limit", DEFAULT_DIFF_LIMIT)),
                )
                results.append(
                    {
                        "endpoint_config": endpoint_config,
                        "case_request": case_request,
                        "status": "pass" if all(check[1] for check in checks) else "fail",
                        "passed": all(check[1] for check in checks),
                        "checks": checks,
                        "diffs": diffs,
                        "old_response": old_response,
                        "new_response": new_response,
                    }
                )
                status_text = "PASS" if all(check[1] for check in checks) else "FAIL"
                print(f"  -> {status_text}", flush=True)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare original C# API responses with new Python API responses.")
    parser.add_argument("--manifest", help="JSON manifest path for batch comparisons.")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Single endpoint path, e.g. BaseInfo/GetSERVERPARTCRTList.")
    parser.add_argument("--method", default="POST", help="HTTP method for single-endpoint mode.")
    parser.add_argument("--json-body", help="JSON body string for single-endpoint mode.")
    parser.add_argument("--query", help="JSON query string for single-endpoint mode.")
    parser.add_argument("--headers", help="JSON headers override for single-endpoint mode.")
    parser.add_argument("--case-name", help="Case name for single-endpoint mode.")
    parser.add_argument("--old-base", help="Old API base URL, default is the online C# service.")
    parser.add_argument("--new-base", help="New API base URL, default is the local FastAPI service.")
    parser.add_argument("--timeout", type=int, help="Request timeout in seconds.")
    parser.add_argument("--report", help="Output markdown report path.")
    parser.add_argument("--dry-run", action="store_true", help="Validate manifest and render report without sending requests.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.manifest:
        manifest_path = resolve_path(args.manifest)
        manifest = load_manifest(manifest_path)
        manifest_source = str(manifest_path)
    else:
        manifest = build_manifest_from_cli(args)
        manifest_source = "CLI"

    if args.report:
        manifest["report_path"] = str(resolve_path(args.report))

    results = run_manifest(manifest, dry_run=args.dry_run)
    report = format_report(manifest_source, manifest, results)
    report_path = resolve_path(manifest["report_path"])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    summary_path = report_path.with_suffix(".json")
    summary_payload = build_report_summary(manifest_source, manifest, results, report_path)
    summary_path.write_text(json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    passed_cases = sum(1 for result in results if result["status"] == "pass")
    failed_cases = sum(1 for result in results if result["status"] == "fail")
    skipped_cases = sum(1 for result in results if result["status"] == "skip")
    total_cases = len(results)
    print(f"对比完成: PASS {passed_cases} / FAIL {failed_cases} / SKIP {skipped_cases} / TOTAL {total_cases}")
    print(f"报告已写入: {report_path}")
    print(f"摘要已写入: {summary_path}")
    if args.dry_run:
        print("当前为 dry-run，未发起真实请求。")

    return 0 if failed_cases == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
