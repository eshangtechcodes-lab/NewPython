# -*- coding: utf-8 -*-
"""根据全量对比 JSON 报告，生成分类整改文档"""
import json
from collections import defaultdict
from datetime import datetime

with open("docs/session4_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ===== 分类 =====
pass_list = []                    # PASS
csharp_error = []                 # C# 端报错（404/500/超时等）
python_timeout = []               # Python 端因空参数导致超时或无响应
fail_by_module = defaultdict(list)  # 按模块分组的 FAIL（排除上面两类）

for case in data["cases"]:
    ep = case["endpoint"]
    module = ep.split("/")[0] if "/" in ep else "Unknown"
    status = case["status"]
    method = case["method"]
    case_name = case["case_name"]
    old_sc = case.get("old_status_code")
    new_sc = case.get("new_status_code")
    diffs = case.get("diffs", [])
    checks = case.get("checks", [])

    if status == "pass":
        pass_list.append(case)
        continue

    if status == "skip":
        continue

    # ---- 判断 C# 端报错 ----
    # C# 返回 404/405/415/500
    is_csharp_error = False
    if old_sc and old_sc >= 400:
        is_csharp_error = True
    # C# 端调用失败（连接超时等）
    for ch in checks:
        if ch["name"] == "接口可达" and not ch["ok"]:
            detail = ch.get("detail", "")
            if "原 API 调用失败" in str(diffs):
                is_csharp_error = True

    if is_csharp_error:
        csharp_error.append(case)
        continue

    # ---- 判断空参数导致的超时/报错 ----
    query = case.get("query")
    json_body = case.get("json_body")
    is_empty_param = False
    # 检查是否无查询参数或空 SearchParameter
    if query is None and json_body is None:
        is_empty_param = True
    elif json_body and isinstance(json_body, dict):
        sp = json_body.get("SearchParameter")
        if sp is not None and isinstance(sp, dict) and len(sp) == 0:
            # SearchParameter 为空 {}
            pass  # 不一定是空参数问题，看是否超时
    # 检查是否 Python 端超时（连接失败）
    for d in diffs:
        if "新 API 调用失败" in d and ("timed out" in d.lower() or "timeout" in d.lower() or "Read timed out" in d):
            is_empty_param = True
    # 检查 new_response 是否超时
    if new_sc is None:
        for d in diffs:
            if "timed out" in d.lower() or "timeout" in d.lower():
                is_empty_param = True

    if is_empty_param and new_sc is None:
        python_timeout.append(case)
        continue

    # ---- 其余按模块分组 ----
    fail_by_module[module].append(case)


def describe_fail(case):
    """简要描述一个 FAIL 用例的差异"""
    diffs = case.get("diffs", [])
    old_sc = case.get("old_status_code")
    new_sc = case.get("new_status_code")
    parts = []
    if old_sc != new_sc:
        parts.append("HTTP {}/{}".format(old_sc, new_sc))

    for d in diffs[:3]:
        # 截断过长的 diff
        if len(d) > 120:
            d = d[:120] + "..."
        parts.append(d)
    if len(diffs) > 3:
        parts.append("...共{}处差异".format(len(diffs)))
    return "; ".join(parts) if parts else "未知差异"


def classify_fail_reason(case):
    """对 FAIL 用例做简要分类"""
    diffs = case.get("diffs", [])
    new_sc = case.get("new_status_code")
    old_sc = case.get("old_status_code")
    diff_text = " ".join(diffs)

    if new_sc == 422 or new_sc == 405:
        return "HTTP方法/参数校验错误"
    if "fetch_one" in diff_text or "fetch_scalar" in diff_text:
        return "DatabaseHelper缺少方法"
    if new_sc == 404:
        return "Python端路由未注册"
    if "查询失败" in diff_text and "Result_Code" in diff_text:
        return "Python查询报错"
    if "查询成功" in diff_text and "成功" in diff_text:
        if any("值不一致" in d and "Result_Desc" in d for d in diffs):
            return "Result_Desc措辞差异"
    if any("多出该字段" in d or "缺少该字段" in d for d in diffs):
        return "字段差异"
    if any("类型不一致" in d for d in diffs):
        return "类型差异"
    if any("值不一致" in d for d in diffs):
        return "值差异"
    return "其他"


# ===== 生成文档 =====
lines = []
lines.append("# 全量 API 对比整改清单")
lines.append("")
lines.append("- 生成时间: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
lines.append("- 数据来源: `docs/session4_full.json`")
lines.append("- 总计: **PASS {} / FAIL {} / TOTAL {}**".format(
    data["counts"]["pass"], data["counts"]["fail"], data["counts"]["total"]))
lines.append("")

# ---- 1. PASS 列表 ----
lines.append("## 1. 已通过接口 ({} 个)".format(len(pass_list)))
lines.append("")
for c in pass_list:
    lines.append("- `{}` / {} `{}`".format(c["endpoint"], c["method"], c["case_name"]))
lines.append("")

# ---- 2. 原接口 (C#) 报错 ----
lines.append("## 2. 原接口 (C#) 报错 ({} 个)".format(len(csharp_error)))
lines.append("")
lines.append("> 这些接口 C# 端返回 404/500 等错误，说明原 API 也不可用或未部署。")
lines.append("> 建议：Python 端可暂时跳过或标记为 SKIP。")
lines.append("")
if csharp_error:
    # 按模块分组
    csharp_by_module = defaultdict(list)
    for c in csharp_error:
        mod = c["endpoint"].split("/")[0]
        csharp_by_module[mod].append(c)
    for mod in sorted(csharp_by_module.keys()):
        lines.append("### {}".format(mod))
        lines.append("")
        lines.append("| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |")
        lines.append("|---|---|---|---|")
        for c in csharp_by_module[mod]:
            lines.append("| `{}` | {} | {} | {} |".format(
                c["endpoint"], c["method"], c.get("old_status_code"), c.get("new_status_code")))
        lines.append("")

# ---- 3. 空参数/超时 ----
lines.append("## 3. 空参数导致超时 ({} 个)".format(len(python_timeout)))
lines.append("")
if python_timeout:
    lines.append("> 这些接口因测试用例未提供必要参数，导致 Python 端超时或无法响应。")
    lines.append("> 建议：补充 case_library 中的参数后重新测试。")
    lines.append("")
    lines.append("| 接口 | 方法 | 说明 |")
    lines.append("|---|---|---|")
    for c in python_timeout:
        lines.append("| `{}` | {} | {} |".format(
            c["endpoint"], c["method"], c["case_name"]))
    lines.append("")
else:
    lines.append("无。")
    lines.append("")

# ---- 4. 按模块分组的 FAIL ----
lines.append("## 4. 按模块分组的 FAIL 接口")
lines.append("")

# 先统计各模块按原因分类
for mod in sorted(fail_by_module.keys()):
    cases = fail_by_module[mod]
    # 按原因分类
    reason_groups = defaultdict(list)
    for c in cases:
        reason = classify_fail_reason(c)
        reason_groups[reason].append(c)

    lines.append("### {} ({} 个 FAIL)".format(mod, len(cases)))
    lines.append("")

    for reason in sorted(reason_groups.keys()):
        group = reason_groups[reason]
        lines.append("#### {} ({})".format(reason, len(group)))
        lines.append("")
        lines.append("| 接口 | 方法 | 差异摘要 |")
        lines.append("|---|---|---|")
        for c in group:
            desc = describe_fail(c)
            # 进一步截断
            if len(desc) > 200:
                desc = desc[:200] + "..."
            lines.append("| `{}` | {} | {} |".format(
                c["endpoint"], c["method"], desc))
        lines.append("")

# 写出文件
output_path = "docs/session4_rectification.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("文档已生成: {}".format(output_path))
print("PASS: {}".format(len(pass_list)))
print("C# 端报错: {}".format(len(csharp_error)))
print("空参数超时: {}".format(len(python_timeout)))
print("按模块 FAIL: {}".format(sum(len(v) for v in fail_by_module.values())))
