# 动态接口对比总汇总

- 生成时间：`2026-03-09 18:57:21`
- 总结果：`PASS 0 / FAIL 1 / SKIP 30 / TOTAL 31`

## 窗口结果

| 窗口 | 生成时间 | PASS | FAIL | SKIP | TOTAL | 报告 |
| --- | --- | --- | --- | --- | --- | --- |
| window_1 | 未生成 | 0 | 0 | 0 | 0 | `E:\workfile\JAVA\NewAPI\docs\window_1_dynamic_compare_report.md` |
| window_2 | 未生成 | 0 | 0 | 0 | 0 | `E:\workfile\JAVA\NewAPI\docs\window_2_dynamic_compare_report.md` |
| window_3 | 未生成 | 0 | 0 | 0 | 0 | `E:\workfile\JAVA\NewAPI\docs\window_3_dynamic_compare_report.md` |
| window_4 | 2026-03-09 18:49:27 | 0 | 1 | 30 | 31 | `E:\workfile\JAVA\NewAPI\docs\window_4_dynamic_compare_report.md` |

## 失败用例

| 窗口 | 接口 | 用例 | 方法 | 首个差异 |
| --- | --- | --- | --- | --- |
| window_4 | Picture/GetPictureList | default-query | GET |  |

## 缺失报告

- window_1: `E:\workfile\JAVA\NewAPI\docs\window_1_dynamic_compare_report.md` 尚未生成。
- window_2: `E:\workfile\JAVA\NewAPI\docs\window_2_dynamic_compare_report.md` 尚未生成。
- window_3: `E:\workfile\JAVA\NewAPI\docs\window_3_dynamic_compare_report.md` 尚未生成。

## 使用说明

- 窗口跑完后执行：`python scripts/summarize_compare_reports.py`
- 如果窗口报告旁边已有同名 JSON 摘要，汇总脚本会优先读取 JSON。
- 如果只有 Markdown 报告，汇总脚本会回退到基础 Markdown 解析。
