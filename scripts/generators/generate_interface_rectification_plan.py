# -*- coding: utf-8 -*-
"""Generate a per-interface rectification plan from compare report JSON."""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return ROOT / path


def deep_merge(base: Dict[str, Any] | None, override: Dict[str, Any] | None) -> Dict[str, Any]:
    payload = copy.deepcopy(base or {})
    for key, value in (override or {}).items():
        payload[key] = value
    return payload


def md_file_link(raw_path: str | None) -> str:
    if not raw_path:
        return "`未提供`"
    path = Path(raw_path)
    label = path.name
    target = raw_path.replace("\\", "/")
    if not target.startswith("/"):
        target = "/" + target
    return f"[{label}]({target})"


def json_code(value: Any) -> str:
    if value is None:
        return "`null`"
    return f"`{json.dumps(value, ensure_ascii=False, sort_keys=True)}`"


def extract_paths(diffs: Iterable[str], marker: str) -> List[str]:
    items: List[str] = []
    for diff in diffs:
        if marker not in diff:
            continue
        path = diff.split(":", 1)[0]
        if path not in items:
            items.append(path)
    return items


def detect_category(case: Dict[str, Any]) -> str:
    diffs = case.get("diffs") or []
    old_status = case.get("old_status_code")
    new_status = case.get("new_status_code")

    if any("新 API 调用失败" in diff and "Read timed out" in diff for diff in diffs):
        return "new_timeout"
    if any("原 API 调用失败" in diff and "Read timed out" in diff for diff in diffs):
        return "old_timeout"
    if any("原 API 调用失败" in diff for diff in diffs):
        return "old_baseline_failure"
    if any("新 API 调用失败" in diff for diff in diffs):
        return "new_runtime_failure"
    if old_status != new_status:
        if old_status and old_status >= 500 and (new_status or 0) < 500:
            return "baseline_or_validation_drift"
        if new_status and new_status >= 500 and (old_status or 0) < 500:
            return "new_error_branch"
        return "status_mismatch"
    if any(diff.startswith("<root>.Message:") or diff.startswith("<root>.Result_") for diff in diffs):
        return "wrapper_drift"
    if any("children" in diff or "列表长度不一致" in diff for diff in diffs):
        return "tree_or_list_drift"
    if any("新 API 缺少该字段" in diff for diff in diffs):
        return "missing_fields"
    if any("类型不一致" in diff for diff in diffs):
        return "type_mapping_drift"
    if any("值不一致" in diff for diff in diffs):
        return "value_mapping_drift"
    return "contract_drift"


def category_title(category: str) -> str:
    mapping = {
        "new_timeout": "新 API 超时",
        "old_timeout": "原 API 超时",
        "old_baseline_failure": "原 API 基线异常",
        "new_runtime_failure": "新 API 运行异常",
        "baseline_or_validation_drift": "空参/校验口径漂移",
        "new_error_branch": "新 API 异常分支错误",
        "status_mismatch": "HTTP 状态码不一致",
        "wrapper_drift": "响应包装漂移",
        "tree_or_list_drift": "树结构/列表差异",
        "missing_fields": "字段缺失",
        "type_mapping_drift": "字段类型映射差异",
        "value_mapping_drift": "字段值映射差异",
        "contract_drift": "返回契约差异",
    }
    return mapping.get(category, category)


def category_actions(category: str, case: Dict[str, Any]) -> List[str]:
    diffs = case.get("diffs") or []
    missing_fields = extract_paths(diffs, "新 API 缺少该字段")
    type_fields = extract_paths(diffs, "类型不一致")
    value_fields = extract_paths(diffs, "值不一致")

    if category == "new_timeout":
        actions = [
            "对照 C# 实现检查该接口在 Python 侧的路由、Service、SQL 是否走了全量扫描、递归加载或 N+1 查询。",
            "确认本用例的 query/json 参数都参与了筛选，避免因为漏绑参数导致返回全量数据。",
            "如果是树形接口，优先对齐 C# 的过滤条件、排序规则和 children 装配顺序，避免无条件展开整棵树。",
            "让该接口在 20 秒内稳定返回后，再做字段级一致性回归。",
        ]
        return actions

    if category in {"old_timeout", "old_baseline_failure"}:
        return [
            "先单独复核原 C# 接口基线，不要仅凭这条结果修改 Python 代码。",
            "如果原 API 本身不稳定或报错，把该接口加入基线隔离清单，暂不作为 Python 整改验收口径。",
            "如果原 API 在补充真实参数后能正常返回，再按补充后的真实参数重跑动态对比。",
        ]

    if category == "baseline_or_validation_drift":
        return [
            "先阅读 C# 接口对空参或缺参的处理逻辑，确认旧接口报错是契约还是偶发异常。",
            "如果旧接口对当前入参应报错，则在 Python 侧补齐同样的参数校验和错误包装。",
            "如果旧接口只是因为当前样本无效而报错，不要把新接口改坏，先更新测试入参再复跑。",
        ]

    if category == "new_runtime_failure":
        return [
            "复现并定位 Python 侧异常堆栈，修复路由、Service 或序列化阶段的运行时错误。",
            "确保异常分支的返回结构与 C# 保持一致，不要直接泄漏 Python 异常文本。",
        ]

    if category in {"new_error_branch", "status_mismatch", "wrapper_drift"}:
        return [
            "按 C# 当前接口的成功分支和失败分支分别核对返回壳，不要继续统一套用单一 Result 包装。",
            "对齐 HTTP 状态码、顶层字段名和错误文案，尤其是 Message 与 Result_Code/Result_Data/Result_Desc 的对应关系。",
            "如果当前 case 是空参或边界参数，先确认 C# 的契约，再决定是改代码还是改测试样本。",
        ]

    actions: List[str] = []
    if missing_fields:
        preview = "、".join(missing_fields[:6])
        actions.append(f"补齐旧 API 已返回但新 API 缺失的字段，优先处理：{preview}。")
        actions.append("从 C# Helper/DTO/SQL Select 中回迁这些字段，不要改字段名，不要随意删除旧字段。")
    if category == "tree_or_list_drift":
        actions.extend(
            [
                "检查树形构造、列表过滤和排序逻辑，确保节点数量、children 装配、递归终止条件与 C# 一致。",
                "如果旧接口返回的是部分树或懒加载树，新接口不要提前把额外层级展开。",
            ]
        )
    if type_fields:
        preview = "、".join(type_fields[:6])
        actions.append(f"修正字段类型映射，优先处理：{preview}。")
        actions.append("保持 C# 的空串、None、整数/小数精度语义，不要把 float 强转 int，也不要把空串改成 null。")
    if value_fields and not type_fields:
        preview = "、".join(value_fields[:6])
        actions.append(f"核对字段取值和格式化逻辑，优先处理：{preview}。")
        actions.append("重点检查默认值、字典映射、枚举文本、时间格式和排序稳定性。")
    if not actions:
        actions = [
            "对照 C# 当前接口逐字段核对 DTO、Helper、SQL 和返回结构，修复本 case 的契约差异。",
            "修复后重新跑该接口的动态对比，确认状态码、顶层壳和 Result_Data 全量一致。",
        ]
    return actions


def acceptance_lines(category: str) -> List[str]:
    lines = [
        "重新执行当前接口所在窗口的 compare_api 命令，本接口对应 case 不再出现 FAIL。",
        "原 API 与新 API 的 HTTP 状态码、顶层字段和 Result_Data 完全一致。",
    ]
    if category == "new_timeout":
        lines.insert(0, "新 API 在 20 秒超时阈值内返回，不再出现 Read timed out。")
    if category in {"wrapper_drift", "status_mismatch", "new_error_branch"}:
        lines.append("成功分支和错误分支都与 C# 契约一致，不再混用 Message 和 Result_* 返回壳。")
    if category in {"missing_fields", "type_mapping_drift", "value_mapping_drift", "tree_or_list_drift"}:
        lines.append("字段缺失、类型不一致、children/list 长度差异全部清零。")
    if category in {"old_timeout", "old_baseline_failure", "baseline_or_validation_drift"}:
        lines.append("如果旧 API 仍不稳定，先把该接口转入基线隔离清单，不以此 case 阻塞 Python 验收。")
    return lines


def build_request(manifest: Dict[str, Any], endpoint_config: Dict[str, Any], case_config: Dict[str, Any]) -> Dict[str, Any]:
    headers = deep_merge(manifest.get("default_headers"), endpoint_config.get("headers"))
    headers = deep_merge(headers, case_config.get("headers"))
    params = deep_merge(endpoint_config.get("query"), case_config.get("query"))
    json_body = deep_merge(endpoint_config.get("json"), case_config.get("json"))
    method = str(case_config.get("method") or endpoint_config.get("method") or "POST").upper()
    if method in {"GET", "HEAD"} and not params and json_body:
        params = json_body
        json_body = None
    return {
        "headers": headers or None,
        "query": params or None,
        "json_body": json_body or None,
        "method": method,
    }


def build_manifest_index(manifest: Dict[str, Any]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    index: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for endpoint in manifest.get("endpoints", []):
        for case in endpoint.get("cases", []) or [{"name": "default"}]:
            request = build_request(manifest, endpoint, case)
            index[(endpoint["endpoint"], case["name"])] = {
                "endpoint": endpoint,
                "case": case,
                "request": request,
            }
    return index


def render_case_block(case: Dict[str, Any], meta: Dict[str, Any], request: Dict[str, Any]) -> List[str]:
    category = detect_category(case)
    lines = [
        f"#### 用例 `{case['case_name']}`",
        "",
        f"- 首因分类：`{category_title(category)}`",
        f"- HTTP：`{case.get('old_status_code')} -> {case.get('new_status_code')}`",
        f"- 请求方法：`{request['method']}`",
        f"- Headers：{json_code(request.get('headers'))}",
        f"- Query：{json_code(request.get('query'))}",
        f"- JSON：{json_code(request.get('json_body'))}",
        "",
        "观察到的问题：",
    ]
    for diff in (case.get("diffs") or [])[:10]:
        lines.append(f"- {diff}")
    lines.extend(["", "建议改动："])
    for action in category_actions(category, case):
        lines.append(f"- {action}")
    lines.extend(["", "完成定义："])
    for item in acceptance_lines(category):
        lines.append(f"- {item}")
    return lines


def render_plan(report_path: Path, manifest_path: Path, report: Dict[str, Any], manifest: Dict[str, Any]) -> str:
    manifest_index = build_manifest_index(manifest)
    failed_cases = [case for case in report.get("cases", []) if case.get("status") == "fail"]
    failed_by_endpoint: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    category_counter: Counter[str] = Counter()
    for case in failed_cases:
        failed_by_endpoint[case["endpoint"]].append(case)
        category_counter[detect_category(case)] += 1

    lines = [
        "# 窗口接口级整改清单",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 报告输入：`{report_path}`",
        f"- 执行清单：`{manifest_path}`",
        f"- 原 API：`{report.get('old_api_base')}`",
        f"- 新 API：`{report.get('new_api_base')}`",
        f"- 用例统计：`PASS {report['counts']['pass']} / FAIL {report['counts']['fail']} / TOTAL {report['counts']['total']}`",
        "",
        "说明：",
        "",
        "- 本清单按“接口 -> 失败用例”展开，只列失败项。",
        "- 建议改动是基于测试报告的推断，真正修改代码时必须以对应 C# 源实现为准。",
        "- 如果某条是原 API 基线异常，不要直接改坏 Python，要先补真实参数或隔离基线。",
        "",
        "## 给另一个 AI 的执行方式",
        "",
        "1. 一次只领取一个接口，不要跨接口大面积修改。",
        "2. 先阅读该接口条目里的 Python 实现和 C# 参考，再开始改代码。",
        "3. 修改时优先修复本接口直接相关的 Router、Service、Helper、DTO 和 SQL 映射，不要顺手改其他模块。",
        "4. 修改完成后，必须重跑窗口 1 对比命令：",
        "",
        "```powershell",
        "python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md",
        "```",
        "",
        "5. 只有当本接口对应 case 不再 FAIL，或者已明确归类为“原 API 基线异常”时，才允许转下一个接口。",
        "6. 如果修接口时发现是测试样本问题，不要直接改坏代码，应先回写 `endpoint_case_library.json` 并重生成 manifest。",
        "",
        "## 建议修复顺序",
        "",
        "1. 先修 `新 API 超时`：这类接口当前连字段级比对都进不去。",
        "2. 再修 `HTTP 状态码不一致 / 响应包装漂移 / 空参校验口径漂移`：先把壳层和错误分支拉齐。",
        "3. 再修 `字段缺失 / 树结构差异 / 类型映射差异 / 值映射差异`：这类是具体业务字段回迁问题。",
        "4. 最后处理明确属于 `原 API 基线异常` 的接口，避免把 Python 修坏。",
        "",
        "## 失败分类汇总",
        "",
        "| 分类 | 数量 |",
        "| --- | --- |",
    ]
    for category, count in sorted(category_counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {category_title(category)} | {count} |")

    lines.extend(["", "## 接口整改项", ""])

    for endpoint_name in sorted(failed_by_endpoint):
        endpoint_cases = failed_by_endpoint[endpoint_name]
        manifest_item = manifest_index.get((endpoint_name, endpoint_cases[0]["case_name"]), {})
        endpoint_config = manifest_item.get("endpoint", {})
        meta = endpoint_config.get("meta", {})
        lines.extend(
            [
                f"### `{endpoint_name}`",
                "",
                f"- 模块：`{meta.get('module') or '未知'}`",
                f"- Python 实现：{md_file_link(meta.get('python_source'))}",
                f"- C# 参考：{md_file_link(meta.get('csharp_source'))}",
                f"- 失败用例数：`{len(endpoint_cases)}`",
                "",
            ]
        )
        for case in endpoint_cases:
            manifest_case = manifest_index.get((case["endpoint"], case["case_name"]))
            request = manifest_case["request"] if manifest_case else {"method": case["method"], "headers": None, "query": case.get("query"), "json_body": case.get("json_body")}
            lines.extend(render_case_block(case, meta, request))
            lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate interface rectification markdown from compare report JSON.")
    parser.add_argument("--report-json", required=True, help="Compare report JSON path.")
    parser.add_argument("--manifest", required=True, help="Manifest JSON path used for the report.")
    parser.add_argument("--output", required=True, help="Output markdown path.")
    args = parser.parse_args()

    report_path = resolve_path(args.report_json)
    manifest_path = resolve_path(args.manifest)
    output_path = resolve_path(args.output)

    report = read_json(report_path)
    manifest = read_json(manifest_path)
    content = render_plan(report_path, manifest_path, report, manifest)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote rectification plan to: {output_path}")


if __name__ == "__main__":
    main()
