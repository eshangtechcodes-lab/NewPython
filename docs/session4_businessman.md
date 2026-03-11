# 动态接口对比报告

- 生成时间: 2026-03-10 22:36:00
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_businessman.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 3 / FAIL 0 / SKIP 0 / TOTAL 3`

## 用例明细

### BusinessMan/GetCOMMODITY_TEMPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITY_TEMPId": 43}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BUSINESSTYPE', 'COMMODITY_BARCODE', 'COMMODITY_ID', 'COMMODITY_NAME', 'COMMODITY_TEMP_DESC', 'COMMODITY_TEMP_ID', 'COMMODITY_TEMP_STATE', 'COMMODITY_TYPE', 'COMMODITY_TYPENAME', 'CREATE_DATE', 'DATA_TYPE', 'OPERATE_DATE', 'OPERATE_ENDDATE', 'OPERATE_STARTDATE', 'QUALIFICATION_DATE', 'QUALIFICATION_DELAYDATE', 'QUALIFICATION_ID', 'SEARCH_ENDDATE', 'SEARCH_STARTDATE', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE'] vs ['BUSINESSTYPE', 'COMMODITY_BARCODE', 'COMMODITY_ID', 'COMMODITY_NAME', 'COMMODITY_TEMP_DESC', 'COMMODITY_TEMP_ID', 'COMMODITY_TEMP_STATE', 'COMMODITY_TYPE', 'COMMODITY_TYPENAME', 'CREATE_DATE', 'DATA_TYPE', 'OPERATE_DATE', 'OPERATE_ENDDATE', 'OPERATE_STARTDATE', 'QUALIFICATION_DATE', 'QUALIFICATION_DELAYDATE', 'QUALIFICATION_ID', 'SEARCH_ENDDATE', 'SEARCH_STARTDATE', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `113.7 ms`
新 API 状态: `200`，耗时 `2033.11 ms`

### BusinessMan/GetCOMMODITY_TEMPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITY_TEMP_ID": 10459}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPList | 新 API: http://localhost:8080/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 25 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `214.14 ms`
新 API 状态: `200`，耗时 `28.46 ms`

### BusinessMan/GetUserList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessMan/GetUserList | 新 API: http://localhost:8080/EShangApiMain/BusinessMan/GetUserList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 16 vs 16 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 16 vs 16 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `507.08 ms`
新 API 状态: `200`，耗时 `57.02 ms`
