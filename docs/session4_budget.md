# 动态接口对比报告

- 生成时间: 2026-03-10 18:32:18
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_budget.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 4 / FAIL 7 / SKIP 0 / TOTAL 11`

## 用例明细

### Budget/GetBudgetDetailDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BUDGETDETAIL_AHId": 132}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetDetailDetail | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetDetailDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ACCOMPLISH', 'ACCOUNT_CODE', 'ACCOUNT_PCODE', 'BUDGETDETAIL_AH_DESC', 'BUDGETDETAIL_AH_ID', 'BUDGETDETAIL_AH_STATE', 'BUDGETDETAIL_AMOUNT', 'BUDGETPROJECT_AH_ID', 'BUDGETTPE', 'OPERATE_DATE', 'REVENUE_AMOUNT', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'UPDATE_TIME', 'YEARBUDGET', 'YEARPROGRESS', 'YEARTOTAL'] vs ['ACCOMPLISH', 'ACCOUNT_CODE', 'ACCOUNT_PCODE', 'BUDGETDETAIL_AH_DESC', 'BUDGETDETAIL_AH_ID', 'BUDGETDETAIL_AH_STATE', 'BUDGETDETAIL_AMOUNT', 'BUDGETPROJECT_AH_ID', 'BUDGETTPE', 'OPERATE_DATE', 'REVENUE_AMOUNT', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'UPDATE_TIME', 'YEARBUDGET', 'YEARPROGRESS', 'YEARTOTAL'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `227.13 ms`
新 API 状态: `200`，耗时 `2089.74 ms`

### Budget/GetBudgetDetailList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"BUDGETDETAIL_AH_ID": 10518}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetDetailList | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetDetailList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 20 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `93.54 ms`
新 API 状态: `200`，耗时 `53.32 ms`

### Budget/GetBudgetProjectList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetBudgetProjectList | 新 API: http://localhost:8080/EShangApiMain/Budget/GetBudgetProjectList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 2 vs 2 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 2 vs 2 |
| 首条字段集合 | ✅ | 字段一致，共 18 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `188.91 ms`
新 API 状态: `200`，耗时 `29.58 ms`

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

原 API 状态: `404`，耗时 `4.5 ms`
新 API 状态: `200`，耗时 `37.33 ms`

### Budget/GetbudgetProjectDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BUDGETPROJECT_AHId": 128}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Budget/GetbudgetProjectDetail | 新 API: http://localhost:8080/EShangApiMain/Budget/GetbudgetProjectDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BUDGETPROJECT_AH_DESC', 'BUDGETPROJECT_AH_ID', 'BUDGETPROJECT_CODE', 'BUDGETPROJECT_ENDDATE', 'BUDGETPROJECT_STATE', 'BUDGETPROJECT_TYPE', 'BUDGETPROJECT_UNIT', 'BUDGETPROJECT_YEAR', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME'] vs ['BUDGETPROJECT_AH_DESC', 'BUDGETPROJECT_AH_ID', 'BUDGETPROJECT_CODE', 'BUDGETPROJECT_ENDDATE', 'BUDGETPROJECT_STATE', 'BUDGETPROJECT_TYPE', 'BUDGETPROJECT_UNIT', 'BUDGETPROJECT_YEAR', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `171.92 ms`
新 API 状态: `200`，耗时 `25.75 ms`

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

原 API 状态: `404`，耗时 `4.09 ms`
新 API 状态: `200`，耗时 `3.39 ms`

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
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_dynamic' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `3.73 ms`
新 API 状态: `200`，耗时 `3.83 ms`

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
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_in' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `3.37 ms`
新 API 状态: `200`，耗时 `4.38 ms`

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
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_in_dynamic' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `8.27 ms`
新 API 状态: `200`，耗时 `5.83 ms`

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
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_out' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `5.61 ms`
新 API 状态: `200`，耗时 `4.77 ms`

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
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 查询失败module 'services.finance.budget_service' has no attribute 'get_budget_project_report_out_dynamic' |
| Result_Desc | ❌ | None vs 失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `6.82 ms`
新 API 状态: `200`，耗时 `4.45 ms`
