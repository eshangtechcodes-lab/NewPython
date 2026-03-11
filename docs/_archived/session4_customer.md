# 动态接口对比报告

- 生成时间: 2026-03-10 22:43:27
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_customer.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 2 / FAIL 0 / SKIP 0 / TOTAL 2`

## 用例明细

### Customer/GetCUSTOMERGROUP_AMOUNTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CUSTOMERGROUP_AMOUNTId": 296}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTDetail | 新 API: http://localhost:8080/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['AMOUNT_00', 'AMOUNT_70', 'AMOUNT_80', 'AMOUNT_90', 'AMOUNT_FEMALE', 'AMOUNT_MALE', 'CUSTOMERGROUP_AMOUNT_ID', 'PROVINCE_ID', 'SERVERPART_CODE', 'SERVERPART_CODES', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'TOTAL_COUNT'] vs ['AMOUNT_00', 'AMOUNT_70', 'AMOUNT_80', 'AMOUNT_90', 'AMOUNT_FEMALE', 'AMOUNT_MALE', 'CUSTOMERGROUP_AMOUNT_ID', 'PROVINCE_ID', 'SERVERPART_CODE', 'SERVERPART_CODES', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'TOTAL_COUNT'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `175.14 ms`
新 API 状态: `200`，耗时 `2075.18 ms`

### Customer/GetCUSTOMERGROUP_AMOUNTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTList | 新 API: http://localhost:8080/EShangApiMain/Customer/GetCUSTOMERGROUP_AMOUNTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 52 vs 52 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 17 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `127.49 ms`
新 API 状态: `200`，耗时 `18.76 ms`
