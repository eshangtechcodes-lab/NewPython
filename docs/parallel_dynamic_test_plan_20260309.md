# 多窗口动态测试执行计划

- 日期：2026-03-10
- 路由真源：`docs/full_audit_baseline_20260309.json`
- 入参总配置：`scripts/manifests/endpoint_case_library.json`
- 业务范围：以 `docs/collaboration_plan.md` 中 15 个模块为准，实际可执行数量按机器基线收口。
- 默认 Header：`{"ProvinceCode":"340000"}`，如需统一调整，请改入参总配置。
- 执行限制：`不允许真实写接口`，因此执行 manifest 只保留 `matched + 读接口`。

## 推荐流程

1. 先编辑 `scripts/manifests/endpoint_case_library.json`，补真实 `cases/query/json/headers`。
2. 再执行 `python scripts/generate_compare_manifests.py` 重生成 modules/windows manifests。
3. 最后执行 `compare_api.py` 跑动态对比。

## 模块数量

| 模块 | C# 路由数 | Python 路由数 | matched | missing | extra | 执行manifest | 排除写接口 | 排除缺失 | 排除多出 | 已配真实参数 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BaseInfo | 145 | 100 | 100 | 45 | 0 | 58 | 42 | 45 | 0 | 58 |
| Merchants | 16 | 15 | 15 | 1 | 0 | 7 | 8 | 1 | 0 | 5 |
| Contract | 130 | 118 | 118 | 12 | 0 | 62 | 56 | 12 | 0 | 53 |
| Finance | 88 | 76 | 76 | 12 | 0 | 41 | 35 | 12 | 0 | 28 |
| Revenue | 60 | 60 | 60 | 0 | 0 | 43 | 17 | 0 | 0 | 34 |
| BigData | 40 | 28 | 28 | 12 | 0 | 17 | 11 | 12 | 0 | 16 |
| MobilePay | 18 | 17 | 17 | 1 | 0 | 14 | 3 | 1 | 0 | 2 |
| Audit | 24 | 24 | 24 | 0 | 0 | 17 | 7 | 0 | 0 | 13 |
| Analysis | 62 | 58 | 58 | 4 | 0 | 31 | 27 | 4 | 0 | 29 |
| BusinessMan | 25 | 25 | 25 | 0 | 0 | 13 | 12 | 0 | 0 | 13 |
| Supplier | 13 | 14 | 13 | 0 | 1 | 7 | 6 | 0 | 1 | 0 |
| Verification | 23 | 23 | 23 | 0 | 0 | 11 | 12 | 0 | 0 | 2 |
| Sales | 13 | 13 | 13 | 0 | 0 | 7 | 6 | 0 | 0 | 0 |
| Picture | 9 | 9 | 3 | 6 | 6 | 1 | 2 | 6 | 6 | 0 |
| Video | 16 | 0 | 0 | 16 | 0 | 0 | 0 | 16 | 0 | 0 |

## 窗口分组

| 窗口 | 模块 | C# 总数 | matched | 执行manifest | 排除写接口 | 排除缺失 | 排除多出 | 已配真实参数 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| window_1 基础与合同 | BaseInfo, Merchants, Contract | 291 | 233 | 127 | 106 | 58 | 0 | 116 |
| window_2 财务与营收 | Finance, Revenue, BigData, MobilePay | 206 | 181 | 115 | 66 | 25 | 0 | 80 |
| window_3 批量中型模块 | Audit, Analysis, BusinessMan, Supplier, Verification, Sales | 160 | 156 | 86 | 70 | 4 | 1 | 57 |
| window_4 收尾与高风险模块 | Picture, Video | 25 | 3 | 1 | 2 | 22 | 6 | 0 |

## 执行命令

重生成 manifests：

`python scripts/generate_compare_manifests.py`

单窗口执行：

`python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md`

`python scripts/compare_api.py --manifest scripts/manifests/windows/window_2.json --report docs/window_2_dynamic_compare_report.md`

`python scripts/compare_api.py --manifest scripts/manifests/windows/window_3.json --report docs/window_3_dynamic_compare_report.md`

`python scripts/compare_api.py --manifest scripts/manifests/windows/window_4.json --report docs/window_4_dynamic_compare_report.md`

并行开 4 个窗口：

`powershell -ExecutionPolicy Bypass -File scripts/start_parallel_compare_windows.ps1`

## 使用说明

- `endpoint_case_library.json`：全部接口测试入参的唯一配置入口。
- `modules/*.json`：按模块拆分的执行 manifest，由脚本自动生成。
- `windows/*.json`：按窗口聚合的执行 manifest，由脚本自动生成。
- 当前执行 manifest 不再包含写接口、Python 缺失接口、Python 多出接口。
- 全接口数量仍保留在 `manifest_summary_20260309.json` 和本计划文档里，用来做完整性统计。
- 如需补某个接口的真实参数，只改 `endpoint_case_library.json`，不要手工长期维护 `window_*.json`。
