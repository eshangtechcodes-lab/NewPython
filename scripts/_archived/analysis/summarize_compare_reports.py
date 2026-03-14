# -*- coding: utf-8 -*-
"""汇总 4 个窗口的动态对比报告。"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
DEFAULT_OUTPUT = DOCS_DIR / "dynamic_compare_master_report_20260309.md"
WINDOWS = [
    ("window_1", DOCS_DIR / "window_1_dynamic_compare_report.md"),
    ("window_2", DOCS_DIR / "window_2_dynamic_compare_report.md"),
    ("window_3", DOCS_DIR / "window_3_dynamic_compare_report.md"),
    ("window_4", DOCS_DIR / "window_4_dynamic_compare_report.md"),
]


def parse_markdown_report(report_path: Path) -> Dict[str, Any]:
    text = report_path.read_text(encoding="utf-8", errors="ignore")
    generated_at = None
    manifest_source = None
    counts = {"pass": 0, "fail": 0, "skip": 0, "total": 0}

    cases: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    for line in text.splitlines():
        if "生成时间:" in line:
            generated_at = line.split("`")[1] if "`" in line else line.split("生成时间:", 1)[1].strip()
        elif "Manifest:" in line:
            manifest_source = line.split("`")[1] if "`" in line else line.split("Manifest:", 1)[1].strip()
        elif "总结果:" in line:
            payload = line.split("`")[1] if "`" in line else line.split("总结果:", 1)[1].strip()
            parts = payload.split("/")
            if len(parts) == 4:
                counts = {
                    "pass": int(parts[0].replace("PASS", "").strip()),
                    "fail": int(parts[1].replace("FAIL", "").strip()),
                    "skip": int(parts[2].replace("SKIP", "").strip()),
                    "total": int(parts[3].replace("TOTAL", "").strip()),
                }
        if line.startswith("### "):
            heading = line[4:].strip()
            if " / " in heading:
                endpoint, case_name = heading.split(" / ", 1)
            else:
                endpoint, case_name = heading, "default"
            current = {"endpoint": endpoint, "case_name": case_name}
        elif current and line.startswith("- 方法: `"):
            current["method"] = line.split("`", 2)[1]
        elif current and line.startswith("- 结果: `"):
            current["status"] = line.split("`", 2)[1].lower()
            cases.append(current)
            current = None

    if counts["total"] == 0 and cases:
        counts = {"pass": 0, "fail": 0, "skip": 0, "total": len(cases)}
        for case in cases:
            status = case.get("status", "fail")
            counts[status] = counts.get(status, 0) + 1

    return {
        "generated_at": generated_at,
        "manifest_source": manifest_source,
        "report_path": str(report_path),
        "counts": counts,
        "module_scope": [],
        "cases": cases,
    }


def load_window_summary(window_id: str, report_path: Path) -> Dict[str, Any]:
    json_path = report_path.with_suffix(".json")
    if json_path.exists():
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    elif report_path.exists():
        payload = parse_markdown_report(report_path)
    else:
        payload = {
            "generated_at": None,
            "manifest_source": None,
            "report_path": str(report_path),
            "counts": {"pass": 0, "fail": 0, "skip": 0, "total": 0},
            "module_scope": [],
            "cases": [],
            "missing_report": True,
        }
    payload["window_id"] = window_id
    payload["report_path"] = str(report_path)
    payload["json_path"] = str(json_path)
    return payload


def build_master_report(window_summaries: List[Dict[str, Any]]) -> str:
    total_pass = sum(item["counts"]["pass"] for item in window_summaries)
    total_fail = sum(item["counts"]["fail"] for item in window_summaries)
    total_skip = sum(item["counts"]["skip"] for item in window_summaries)
    total_cases = sum(item["counts"]["total"] for item in window_summaries)

    lines = [
        "# 动态接口对比总汇总",
        "",
        f"- 生成时间：`{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- 总结果：`PASS {total_pass} / FAIL {total_fail} / SKIP {total_skip} / TOTAL {total_cases}`",
        "",
        "## 窗口结果",
        "",
        "| 窗口 | 生成时间 | PASS | FAIL | SKIP | TOTAL | 报告 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for item in window_summaries:
        report_path = item["report_path"]
        lines.append(
            f"| {item['window_id']} | {item.get('generated_at') or '未生成'} | "
            f"{item['counts']['pass']} | {item['counts']['fail']} | {item['counts']['skip']} | {item['counts']['total']} | "
            f"`{report_path}` |"
        )

    fail_cases = []
    missing_reports = []
    for item in window_summaries:
        if item.get("missing_report"):
            missing_reports.append(item)
        for case in item.get("cases", []):
            if case.get("status") == "fail":
                fail_cases.append(
                    {
                        "window_id": item["window_id"],
                        "endpoint": case.get("endpoint"),
                        "case_name": case.get("case_name"),
                        "method": case.get("method"),
                        "diffs": case.get("diffs", []),
                        "checks": case.get("checks", []),
                    }
                )

    lines.extend(["", "## 失败用例", ""])
    if fail_cases:
        lines.extend(
            [
                "| 窗口 | 接口 | 用例 | 方法 | 首个差异 |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for case in fail_cases:
            first_diff = ""
            if case["diffs"]:
                first_diff = case["diffs"][0]
            else:
                for check in case["checks"]:
                    if not check.get("ok", True):
                        first_diff = check.get("detail", "")
                        break
            lines.append(
                f"| {case['window_id']} | {case['endpoint']} | {case['case_name']} | {case.get('method') or ''} | {first_diff} |"
            )
    else:
        lines.append("当前没有失败用例，或对应窗口尚未生成可解析的报告。")

    lines.extend(["", "## 缺失报告", ""])
    if missing_reports:
        for item in missing_reports:
            lines.append(f"- {item['window_id']}: `{item['report_path']}` 尚未生成。")
    else:
        lines.append("4 个窗口报告均已找到。")

    lines.extend(
        [
            "",
            "## 使用说明",
            "",
            "- 窗口跑完后执行：`python scripts/summarize_compare_reports.py`",
            "- 如果窗口报告旁边已有同名 JSON 摘要，汇总脚本会优先读取 JSON。",
            "- 如果只有 Markdown 报告，汇总脚本会回退到基础 Markdown 解析。",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize dynamic compare reports from all windows.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output markdown path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path

    window_summaries = [load_window_summary(window_id, report_path) for window_id, report_path in WINDOWS]
    report_text = build_master_report(window_summaries)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")
    print(f"Wrote master report to: {output_path}")


if __name__ == "__main__":
    main()
