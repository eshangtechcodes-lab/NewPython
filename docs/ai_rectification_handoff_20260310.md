# 交给另一个 AI 的整改任务书

## 1. 任务目标

你要修复当前 Python 新接口与线上 C# 旧接口的动态对比失败问题。

本轮最新联调结果：

- 总用例：`329`
- 通过：`14`
- 失败：`315`

你不要从 315 个接口里无序挑接口乱改。必须按“先共性、后模块、再单接口”的顺序推进，这样才能高效收敛。

## 2. 必读文件

先读这些文件，再开始改代码：

- [dynamic_compare_issue_list_20260310_latest.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_issue_list_20260310_latest.md)
- [dynamic_compare_master_report_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_master_report_20260310.md)
- [window_1_interface_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/window_1_interface_rectification_plan_20260310.md)
- [window_2_interface_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/window_2_interface_rectification_plan_20260310.md)
- [window_3_interface_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/window_3_interface_rectification_plan_20260310.md)
- [window_4_interface_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/window_4_interface_rectification_plan_20260310.md)
- [api-migration.md](/E:/workfile/JAVA/NewAPI/.agent/workflows/api-migration.md)
- [collaboration_plan.md](/E:/workfile/JAVA/NewAPI/docs/collaboration_plan.md)

如果要看真实测试参数，统一看：

- [endpoint_case_library.json](/E:/workfile/JAVA/NewAPI/scripts/manifests/endpoint_case_library.json)

## 3. 你必须遵守的执行规则

1. 一次只处理一类问题，或者一个模块，不要跨模块大面积同时修改。
2. 修改代码前，先看对应接口条目里的 Python 实现文件和 C# 参考文件。
3. 不要直接把所有接口强行统一成单一返回壳，必须以旧 C# 当前行为为准。
4. 如果某条失败是因为旧 API 本身超时或基线异常，不要直接把 Python 改坏。
5. 如果发现是测试样本不合理，先改 [endpoint_case_library.json](/E:/workfile/JAVA/NewAPI/scripts/manifests/endpoint_case_library.json)，再重生成 manifest，不要硬改业务代码去迎合错误样本。
6. 每完成一批修改，都必须回归对应窗口；不要只看代码，不跑动态对比。

## 4. 正确的整改顺序

### 第一阶段：先修共性问题

先按下面顺序修：

1. `新 API 超时`
2. `HTTP 状态码不一致`
3. `响应包装漂移`
4. `空参/校验口径漂移`
5. `字段缺失`
6. `树结构/列表差异`
7. `字段类型映射差异`
8. `字段值映射差异`

理由：

- 超时不先修，后面根本进不了字段级比对。
- 状态码和返回壳不先修，很多接口会持续被错误判成失败。
- 只有前两层稳定后，字段缺失和树结构差异的整改才有意义。

### 第二阶段：再按模块推进

推荐顺序：

1. `BaseInfo + BusinessProject`
2. `Revenue + Finance`
3. `Analysis + Audit`
4. `Merchants + BigData + MobilePay`
5. `Picture + Verification + 其他边角模块`

理由：

- 这几个模块当前失败量最大，先修它们，整体通过率提升最快。

## 5. 你应该怎么改

### 5.1 遇到 `新 API 超时`

先查这些点：

- Python 路由是否漏绑筛选参数，导致查全表
- Service 是否出现 N+1 查询
- 树接口是否无条件递归展开
- SQL 是否和 C# 少了 `where` / `top` / 排序条件

改完的标准：

- 新 API 在 20 秒内稳定返回
- 该接口能进入字段级对比，不再直接 timeout

### 5.2 遇到 `HTTP 状态码不一致`

先查这些点：

- 旧接口在当前入参下是成功、404、405 还是业务异常
- Python 是否把旧接口的异常分支包装成了成功分支
- FastAPI 默认 `405/detail` 是否未经转换直接暴露

改完的标准：

- 状态码与旧接口一致
- 顶层返回壳一致

### 5.3 遇到 `响应包装漂移`

重点查：

- 旧接口是只返回 `Message`
- 还是返回 `Result_Code/Result_Data/Result_Desc`
- Python 是否混用了两套壳

改完的标准：

- 成功分支和错误分支都与旧接口一致
- 不再出现 `Message / Result_* / detail` 三套壳混用

### 5.4 遇到 `字段缺失 / 树结构差异 / 类型差异`

重点查：

- DTO/返回模型是否删字段
- SQL select 是否漏列
- Helper/树装配逻辑是否没完整迁移
- `None`、空串、数字精度、日期格式是否和 C# 一致

改完的标准：

- 报告里不再出现“新 API 缺少该字段”
- `children`、列表条数、字段类型、值格式全部对齐

## 6. 你不要怎么改

这些做法是错的：

- 不要为了一条接口通过，把公共层改成影响所有模块的强制统一壳
- 不要看到旧接口报错，就简单让 Python 也抛一个通用“请求参数校验失败”
- 不要忽略测试入参，凭猜测改代码
- 不要跳过回归，只看单元逻辑觉得“应该没问题”

## 7. 你的工作单位

你有两个工作粒度，只能选一个执行：

### 方案 A：按共性问题批次修

适合修：

- 超时
- 状态码
- 包装壳
- 类型映射

### 方案 B：按模块逐接口修

适合修：

- BaseInfo
- BusinessProject
- Revenue
- Analysis

如果不是明确的公共问题，优先用方案 B，不要误伤别的模块。

## 8. 交付要求

你每完成一批修改，必须交付：

1. 修改了哪些文件
2. 修了哪类问题
3. 回归跑了哪个窗口
4. 哪些接口从 `FAIL` 变成了 `PASS`
5. 哪些接口仍失败，以及新失败原因

## 9. 回归命令

先重生成 manifest：

```powershell
cd E:\workfile\JAVA\NewAPI
python scripts/generate_compare_manifests.py
```

按窗口回归：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_2.json --report docs/window_2_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_3.json --report docs/window_3_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_4.json --report docs/window_4_dynamic_compare_report.md
```

最后汇总：

```powershell
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

## 10. 最短交接话术

把下面这段直接发给另一个 AI：

```text
你现在要修复 E:\workfile\JAVA\NewAPI 里 Python 新接口与旧 C# 接口的动态对比失败问题。不要无序逐接口乱改，必须先按共性问题处理，再按模块逐接口收尾。先读 docs/dynamic_compare_issue_list_20260310_latest.md、docs/dynamic_compare_master_report_20260310.md、docs/window_1_interface_rectification_plan_20260310.md、docs/window_2_interface_rectification_plan_20260310.md、docs/window_3_interface_rectification_plan_20260310.md、docs/window_4_interface_rectification_plan_20260310.md。真实测试参数统一看 scripts/manifests/endpoint_case_library.json。优先顺序是：1. 新 API 超时，2. HTTP 状态码不一致，3. 响应包装漂移，4. 空参/校验口径漂移，5. 字段缺失，6. 树结构/列表差异，7. 字段类型映射差异，8. 字段值映射差异。模块顺序是：BaseInfo+BusinessProject，Revenue+Finance，Analysis+Audit，Merchants+BigData+MobilePay，最后 Picture+Verification。一次只处理一类问题或一个模块。每次修改后必须运行对应窗口的 compare_api 回归，并更新总汇总。
```
