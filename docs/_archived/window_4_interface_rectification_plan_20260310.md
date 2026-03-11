# 窗口接口级整改清单

- 生成时间：2026-03-10 15:29:25
- 报告输入：`E:\workfile\JAVA\NewAPI\docs\window_4_dynamic_compare_report.json`
- 执行清单：`E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_4.json`
- 原 API：`http://192.168.1.99:8900/EShangApiMain`
- 新 API：`http://localhost:8080/EShangApiMain`
- 用例统计：`PASS 0 / FAIL 1 / TOTAL 1`

说明：

- 本清单按“接口 -> 失败用例”展开，只列失败项。
- 建议改动是基于测试报告的推断，真正修改代码时必须以对应 C# 源实现为准。
- 如果某条是原 API 基线异常，不要直接改坏 Python，要先补真实参数或隔离基线。

## 给另一个 AI 的执行方式

1. 一次只领取一个接口，不要跨接口大面积修改。
2. 先阅读该接口条目里的 Python 实现和 C# 参考，再开始改代码。
3. 修改时优先修复本接口直接相关的 Router、Service、Helper、DTO 和 SQL 映射，不要顺手改其他模块。
4. 修改完成后，必须重跑窗口 1 对比命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md
```

5. 只有当本接口对应 case 不再 FAIL，或者已明确归类为“原 API 基线异常”时，才允许转下一个接口。
6. 如果修接口时发现是测试样本问题，不要直接改坏代码，应先回写 `endpoint_case_library.json` 并重生成 manifest。

## 建议修复顺序

1. 先修 `新 API 超时`：这类接口当前连字段级比对都进不去。
2. 再修 `HTTP 状态码不一致 / 响应包装漂移 / 空参校验口径漂移`：先把壳层和错误分支拉齐。
3. 再修 `字段缺失 / 树结构差异 / 类型映射差异 / 值映射差异`：这类是具体业务字段回迁问题。
4. 最后处理明确属于 `原 API 基线异常` 的接口，避免把 Python 修坏。

## 失败分类汇总

| 分类 | 数量 |
| --- | --- |
| HTTP 状态码不一致 | 1 |

## 接口整改项

### `Picture/GetPictureList`

- 模块：`Picture`
- Python 实现：[batch_router_part2.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/batch_modules/batch_router_part2.py)
- C# 参考：[PictureController.cs](/E:/workfile/JAVA/API/CSharp/EShangApiMain/Controllers/Picture/PictureController.cs)
- 失败用例数：`1`

#### 用例 `default-query`

- 首因分类：`HTTP 状态码不一致`
- HTTP：`404 -> 405`
- 请求方法：`GET`
- Headers：`{"ProvinceCode": "340000"}`
- Query：`null`
- JSON：`null`

观察到的问题：
- <root>.Message: 新 API 缺少该字段
- <root>.detail: 新 API 多出该字段

建议改动：
- 按 C# 当前接口的成功分支和失败分支分别核对返回壳，不要继续统一套用单一 Result 包装。
- 对齐 HTTP 状态码、顶层字段名和错误文案，尤其是 Message 与 Result_Code/Result_Data/Result_Desc 的对应关系。
- 如果当前 case 是空参或边界参数，先确认 C# 的契约，再决定是改代码还是改测试样本。

完成定义：
- 重新执行当前接口所在窗口的 compare_api 命令，本接口对应 case 不再出现 FAIL。
- 原 API 与新 API 的 HTTP 状态码、顶层字段和 Result_Data 完全一致。
- 成功分支和错误分支都与 C# 契约一致，不再混用 Message 和 Result_* 返回壳。
