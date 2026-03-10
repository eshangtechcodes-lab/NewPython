# 动态接口对比报告

- 生成时间: 2026-03-10 12:12:56
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_2.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 0 / FAIL 115 / SKIP 0 / TOTAL 115`

## 用例明细

### Budget/GetBudgetDetailDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetDetailDetail | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetDetailDetail |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetDetailDetail”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `38.71 ms`
新 API 状态: `200`，耗时 `2055.23 ms`

### Budget/GetBudgetDetailList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetDetailList | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetDetailList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 查询失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `7.43 ms`
新 API 状态: `200`，耗时 `4.07 ms`

### Budget/GetBudgetProjectList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetProjectList | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetProjectList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 查询失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `7.62 ms`
新 API 状态: `200`，耗时 `4.94 ms`

### Budget/GetBudgetProjectReportOfMonth / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetProjectReportOfMonth | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetProjectReportOfMonth |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `4.18 ms`
新 API 状态: `200`，耗时 `4.21 ms`

### Budget/GetbudgetProjectDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectDetail | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectDetail |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectDetail”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `6.01 ms`
新 API 状态: `200`，耗时 `3.52 ms`

### Budget/GetbudgetProjectReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReport | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectReport |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs str |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `3.65 ms`
新 API 状态: `200`，耗时 `4.73 ms`

### Budget/GetbudgetProjectReportDynamic / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportDynamic | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectReportDynamic |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_dynamic' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportDynamic”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `7.46 ms`
新 API 状态: `200`，耗时 `4.56 ms`

### Budget/GetbudgetProjectReportIn / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportIn | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectReportIn |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_in' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportIn”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `4.32 ms`
新 API 状态: `200`，耗时 `4.81 ms`

### Budget/GetbudgetProjectReportInDynamic / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportInDynamic | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectReportInDynamic |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_in_dynamic' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportInDynamic”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `3.69 ms`
新 API 状态: `200`，耗时 `4.53 ms`

### Budget/GetbudgetProjectReportOut / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportOut | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectReportOut |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_out' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportOut”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `5.24 ms`
新 API 状态: `200`，耗时 `4.4 ms`

### Budget/GetbudgetProjectReportOutDynamic / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportOutDynamic | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectReportOutDynamic |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_out_dynamic' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectReportOutDynamic”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `3.87 ms`
新 API 状态: `200`，耗时 `3.68 ms`

### Finance/GetAHJKtoken / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetAHJKtoken | 新 API: http://localhost:8080/EShangApiMain/Finance/GetAHJKtoken |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 获取失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('获取失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `10.8 ms`
新 API 状态: `200`，耗时 `4.07 ms`

### Finance/GetATTACHMENTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetATTACHMENTDetail | 新 API: http://localhost:8080/EShangApiMain/Finance/GetATTACHMENTDetail |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 999 |
| Result_Desc | ❌ | None vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetATTACHMENTDetail”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `4.05 ms`
新 API 状态: `200`，耗时 `4.71 ms`

### Finance/GetATTACHMENTList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetATTACHMENTList | 新 API: http://localhost:8080/EShangApiMain/Finance/GetATTACHMENTList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 999 |
| Result_Desc | ❌ | None vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetATTACHMENTList”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `5.28 ms`
新 API 状态: `200`，耗时 `4.37 ms`

### Finance/GetAccountCompare / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetAccountCompare | 新 API: http://localhost:8080/EShangApiMain/Finance/GetAccountCompare |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `4.39 ms`
新 API 状态: `200`，耗时 `4.1 ms`

### Finance/GetAccountReached / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetAccountReached | 新 API: http://localhost:8080/EShangApiMain/Finance/GetAccountReached |

差异明细：
- 原 API 调用失败: HTTPConnectionPool(host='192.168.1.99', port=8900): Read timed out. (read timeout=20)
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetAnnualAccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetAnnualAccountList | 新 API: http://localhost:8080/EShangApiMain/Finance/GetAnnualAccountList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `23.37 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetBankAccountAnalyseList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetBankAccountAnalyseList | 新 API: http://localhost:8080/EShangApiMain/Finance/GetBankAccountAnalyseList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.8 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetBankAccountAnalyseTreeList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetBankAccountAnalyseTreeList | 新 API: http://localhost:8080/EShangApiMain/Finance/GetBankAccountAnalyseTreeList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.96 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetContractExcuteAnalysis / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetContractExcuteAnalysis | 新 API: http://localhost:8080/EShangApiMain/Finance/GetContractExcuteAnalysis |

差异明细：
- 原 API 调用失败: HTTPConnectionPool(host='192.168.1.99', port=8900): Read timed out. (read timeout=20)
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetContractMerchant / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetContractMerchant | 新 API: http://localhost:8080/EShangApiMain/Finance/GetContractMerchant |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `4507.64 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetMonthAccountDiff / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetMonthAccountDiff | 新 API: http://localhost:8080/EShangApiMain/Finance/GetMonthAccountDiff |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `10.96 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetMonthAccountProinst / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetMonthAccountProinst | 新 API: http://localhost:8080/EShangApiMain/Finance/GetMonthAccountProinst |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `500`，耗时 `6.17 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetPeriodSupplementList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetPeriodSupplementList | 新 API: http://localhost:8080/EShangApiMain/Finance/GetPeriodSupplementList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `8.62 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetProjectExpenseList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectExpenseList | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectExpenseList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.72 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetProjectMerchantSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectMerchantSummary | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectMerchantSummary |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.41 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetProjectPeriodAccount / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectPeriodAccount | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectPeriodAccount |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.89 ms`
新 API 状态: `None`，耗时 `None ms`

### Finance/GetProjectPeriodIncome / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectPeriodIncome | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectPeriodIncome |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `6.02 ms`
新 API 状态: `200`，耗时 `20318.41 ms`

### Finance/GetProjectShopIncome / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectShopIncome | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectShopIncome |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 获取失败: [CODE:-2207]第6 行附近出现错误:
无法解析的成员访问表达式[A.SELLER_NAME] |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectShopIncome”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `4.12 ms`
新 API 状态: `200`，耗时 `177.96 ms`

### Finance/GetProjectSplitSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectSplitSummary | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectSplitSummary |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 获取失败: [CODE:-544]超出全局排序空间，请调整SORT_BUF_GLOBAL_SIZE、SORT_BUF_SIZE、SORT_BLK_SIZE |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectSplitSummary”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `4.76 ms`
新 API 状态: `200`，耗时 `804.12 ms`

### Finance/GetProjectSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectSummary | 新 API: http://localhost:8080/EShangApiMain/Finance/GetProjectSummary |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 获取失败: time data '' does not match format '%Y-%m-%d' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetProjectSummary”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `4.09 ms`
新 API 状态: `200`，耗时 `3.17 ms`

### Finance/GetReconciliation / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetReconciliation | 新 API: http://localhost:8080/EShangApiMain/Finance/GetReconciliation |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `3.95 ms`
新 API 状态: `200`，耗时 `300.36 ms`

### Finance/GetRevenueRecognition / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetRevenueRecognition | 新 API: http://localhost:8080/EShangApiMain/Finance/GetRevenueRecognition |

差异明细：
- 原 API 调用失败: HTTPConnectionPool(host='192.168.1.99', port=8900): Read timed out. (read timeout=20)

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `200`，耗时 `3222.4 ms`

### Finance/GetRevenueSplitSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetRevenueSplitSummary | 新 API: http://localhost:8080/EShangApiMain/Finance/GetRevenueSplitSummary |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 获取失败: time data '' does not match format '%Y-%m-%d' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetRevenueSplitSummary”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `50.71 ms`
新 API 状态: `200`，耗时 `3.63 ms`

### Finance/GetRoyaltyDateSumReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetRoyaltyDateSumReport | 新 API: http://localhost:8080/EShangApiMain/Finance/GetRoyaltyDateSumReport |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 获取失败: [CODE:-2106]第7 行附近出现错误:
无效的表或视图名[T_BANKACCOUNTVERIFY] |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetRoyaltyDateSumReport”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `5.82 ms`
新 API 状态: `200`，耗时 `24.22 ms`

### Finance/GetRoyaltyReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetRoyaltyReport | 新 API: http://localhost:8080/EShangApiMain/Finance/GetRoyaltyReport |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 获取失败: [CODE:-2106]第2 行附近出现错误:
无效的表或视图名[T_BANKACCOUNTVERIFY] |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Finance/GetRoyaltyReport”匹配的 HTTP 资源。' vs '失败')

原 API 状态: `404`，耗时 `4.84 ms`
新 API 状态: `200`，耗时 `56.05 ms`

### Finance/GetShopExpense / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetShopExpense | 新 API: http://localhost:8080/EShangApiMain/Finance/GetShopExpense |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `25.15 ms`
新 API 状态: `None`，耗时 `None ms`

### Invoice/GetBILLDETAILDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Invoice/GetBILLDETAILDetail | 新 API: http://localhost:8080/EShangApiMain/Invoice/GetBILLDETAILDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.84 ms`
新 API 状态: `None`，耗时 `None ms`

### Invoice/GetBILLDETAILList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Invoice/GetBILLDETAILList | 新 API: http://localhost:8080/EShangApiMain/Invoice/GetBILLDETAILList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `8.72 ms`
新 API 状态: `None`，耗时 `None ms`

### Invoice/GetBILLDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Invoice/GetBILLDetail | 新 API: http://localhost:8080/EShangApiMain/Invoice/GetBILLDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `26.79 ms`
新 API 状态: `None`，耗时 `None ms`

### Invoice/GetBILLList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Invoice/GetBILLList | 新 API: http://localhost:8080/EShangApiMain/Invoice/GetBILLList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `11.32 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetACCOUNTWARNINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetACCOUNTWARNINGDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetACCOUNTWARNINGDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `12.71 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetACCOUNTWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetACCOUNTWARNINGList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetACCOUNTWARNINGList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `7.97 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBRANDANALYSISDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBRANDANALYSISDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBRANDANALYSISDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `9.18 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBRANDANALYSISList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBRANDANALYSISList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBRANDANALYSISList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `14.1 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBUSINESSANALYSISDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBUSINESSANALYSISDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBUSINESSANALYSISDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `13.85 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBUSINESSANALYSISList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBUSINESSANALYSISList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBUSINESSANALYSISList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `10.45 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBUSINESSWARNINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBUSINESSWARNINGDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBUSINESSWARNINGDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `10.04 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBUSINESSWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBUSINESSWARNINGList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBUSINESSWARNINGList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `9.64 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBankAccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBankAccountList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBankAccountList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.91 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBankAccountReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBankAccountReport | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBankAccountReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.0 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBrandAnalysis / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBrandAnalysis | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBrandAnalysis |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `25.65 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBusinessAnalysisReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBusinessAnalysisReport | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBusinessAnalysisReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.63 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBusinessDate / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBusinessDate | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBusinessDate |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `890.75 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBusinessItemSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBusinessItemSummary | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBusinessItemSummary |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.98 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetBusinessTradeAnalysis / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetBusinessTradeAnalysis | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetBusinessTradeAnalysis |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.63 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetCigaretteReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetCigaretteReport | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetCigaretteReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `3.95 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetCurTotalRevenue / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetCurTotalRevenue | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetCurTotalRevenue |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `141.25 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetHisCommoditySaleList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetHisCommoditySaleList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetHisCommoditySaleList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `21.53 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetMerchantRevenueReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetMerchantRevenueReport | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetMerchantRevenueReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `116.39 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetMonthCompare / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetMonthCompare | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetMonthCompare |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.57 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetMonthINCAnalysis / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetMonthINCAnalysis | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetMonthINCAnalysis |

差异明细：
- 原 API 调用失败: HTTPConnectionPool(host='192.168.1.99', port=8900): Read timed out. (read timeout=20)
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetPERSONSELLDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetPERSONSELLDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetPERSONSELLDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `43.98 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetPERSONSELLList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetPERSONSELLList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetPERSONSELLList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `11.23 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetREVENUEDAILYSPLITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetREVENUEDAILYSPLITDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetREVENUEDAILYSPLITDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.94 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetREVENUEDAILYSPLITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetREVENUEDAILYSPLITList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetREVENUEDAILYSPLITList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `11.2 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueDataList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueDataList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueDataList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `122.91 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenuePushList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenuePushList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenuePushList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.58 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueQOQ / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueQOQ | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueQOQ |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `15.21 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueQOQByDate / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueQOQByDate | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueQOQByDate |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.41 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueReport | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.87 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueReportByBIZPSPLITMONTH / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueReportByBIZPSPLITMONTH | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueReportByBIZPSPLITMONTH |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.12 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueReportByDate / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueReportByDate | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueReportByDate |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `93.9 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueYOYQOQ / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueYOYQOQ | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueYOYQOQ |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `17.75 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetRevenueYOYQOQByDate / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetRevenueYOYQOQByDate | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetRevenueYOYQOQByDate |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `19.81 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetSITUATIONANALYSISDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetSITUATIONANALYSISDetail | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetSITUATIONANALYSISDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `17.38 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetSITUATIONANALYSISList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetSITUATIONANALYSISList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetSITUATIONANALYSISList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `10.97 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetSellMasterCompareList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetSellMasterCompareList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetSellMasterCompareList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.91 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetSituationAnalysis / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetSituationAnalysis | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetSituationAnalysis |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.68 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetTotalRevenue / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetTotalRevenue | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetTotalRevenue |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `153.58 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetTransactionCustomer / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetTransactionCustomer | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetTransactionCustomer |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `13.68 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetTransactionCustomerByDate / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetTransactionCustomerByDate | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetTransactionCustomerByDate |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `8.41 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetYSSellDetailsList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetYSSellDetailsList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetYSSellDetailsList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `500`，耗时 `12.24 ms`
新 API 状态: `None`，耗时 `None ms`

### Revenue/GetYSSellMasterList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Revenue/GetYSSellMasterList | 新 API: http://localhost:8080/EShangApiMain/Revenue/GetYSSellMasterList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `500`，耗时 `13.59 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBAYONETDAILY_AHDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBAYONETDAILY_AHDetail | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBAYONETDAILY_AHDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `10.01 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBAYONETDAILY_AHList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBAYONETDAILY_AHList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBAYONETDAILY_AHList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `12.17 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBAYONETDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBAYONETDetail | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBAYONETDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.42 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBAYONETList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBAYONETList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBAYONETList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `7.82 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBAYONETWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBAYONETWARNINGList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBAYONETWARNINGList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `5.04 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBayonetOwnerAHList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBayonetOwnerAHList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBayonetOwnerAHList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.97 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetBayonetOwnerMonthAHList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetBayonetOwnerMonthAHList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetBayonetOwnerMonthAHList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.44 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetDailyBayonetAnalysis / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetDailyBayonetAnalysis | 新 API: http://localhost:8080/EShangApiMain/BigData/GetDailyBayonetAnalysis |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `15338.88 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetSECTIONFLOWDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetSECTIONFLOWDetail | 新 API: http://localhost:8080/EShangApiMain/BigData/GetSECTIONFLOWDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `4.01 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetSECTIONFLOWList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetSECTIONFLOWList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetSECTIONFLOWList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `4.62 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetSECTIONFLOWMONTHDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetSECTIONFLOWMONTHDetail | 新 API: http://localhost:8080/EShangApiMain/BigData/GetSECTIONFLOWMONTHDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.63 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetSECTIONFLOWMONTHList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetSECTIONFLOWMONTHList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetSECTIONFLOWMONTHList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `10.36 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetServerpartSectionFlow / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetServerpartSectionFlow | 新 API: http://localhost:8080/EShangApiMain/BigData/GetServerpartSectionFlow |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `2369.37 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetTimeIntervalList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetTimeIntervalList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetTimeIntervalList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `8.11 ms`
新 API 状态: `None`，耗时 `None ms`

### BigData/GetUreaMasterList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/BigData/GetUreaMasterList | 新 API: http://localhost:8080/EShangApiMain/BigData/GetUreaMasterList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.01 ms`
新 API 状态: `None`，耗时 `None ms`

### Customer/GetCUSTOMERGROUP_AMOUNTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTDetail | 新 API: http://localhost:8080/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.95 ms`
新 API 状态: `None`，耗时 `None ms`

### Customer/GetCUSTOMERGROUP_AMOUNTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTList | 新 API: http://localhost:8080/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `500`，耗时 `19.32 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetBANKACCOUNTVERIFYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYList | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `5.22 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetBANKACCOUNTVERIFYRegionList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYRegionList | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYRegionList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `7.52 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetBANKACCOUNTVERIFYServerList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYServerList | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYServerList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `8.52 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetBANKACCOUNTVERIFYTreeList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYTreeList | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetBANKACCOUNTVERIFYTreeList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.43 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetChinaUmsSubAccountDetail / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetChinaUmsSubAccountDetail | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetChinaUmsSubAccountDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.59 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetChinaUmsSubAccountSummary / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetChinaUmsSubAccountSummary | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetChinaUmsSubAccountSummary |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `9.57 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetChinaUmsSubMaster / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetChinaUmsSubMaster | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetChinaUmsSubMaster |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `294.08 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetChinaUmsSubSummary / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetChinaUmsSubSummary | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetChinaUmsSubSummary |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.83 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetKwyRoyalty / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetKwyRoyalty | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetKwyRoyalty |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `3.84 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetKwyRoyaltyForAll / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetKwyRoyaltyForAll | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetKwyRoyaltyForAll |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `3.68 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetKwyRoyaltyRate / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetKwyRoyaltyRate | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetKwyRoyaltyRate |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.69 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetMobilePayResult / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetMobilePayResult | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetMobilePayResult |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `7.44 ms`
新 API 状态: `None`，耗时 `None ms`

### MobilePay/GetMobilePayRoyaltyReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetMobilePayRoyaltyReport | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetMobilePayRoyaltyReport |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs list |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `9.92 ms`
新 API 状态: `200`，耗时 `2040.51 ms`

### MobilePay/GetRoyaltyRecordList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/MobilePay/GetRoyaltyRecordList | 新 API: http://localhost:8080/EShangApiMain/MobilePay/GetRoyaltyRecordList |
| HTTP 状态码 | ❌ | 500 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 999 |
| Result_Desc | ❌ | None vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('出现错误。' vs '请求参数校验失败')

原 API 状态: `500`，耗时 `21.0 ms`
新 API 状态: `200`，耗时 `5.22 ms`
