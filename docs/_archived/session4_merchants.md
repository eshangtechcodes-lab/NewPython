# 动态接口对比报告

- 生成时间: 2026-03-10 17:44:21
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\modules\merchants.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 7 / FAIL 0 / SKIP 0 / TOTAL 7`

## 用例明细

### Merchants/GetCoopMerchantsDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCoopMerchantsDetail | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCoopMerchantsDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BANK_ACCOUNT', 'BANK_NAME', 'BrandList', 'COOPMERCHANTS_ADDRESS', 'COOPMERCHANTS_BRAND', 'COOPMERCHANTS_CODE', 'COOPMERCHANTS_DESC', 'COOPMERCHANTS_DRAWER', 'COOPMERCHANTS_EN', 'COOPMERCHANTS_ID', 'COOPMERCHANTS_LINKMAN', 'COOPMERCHANTS_MOBILEPHONE', 'COOPMERCHANTS_NAME', 'COOPMERCHANTS_NATURE', 'COOPMERCHANTS_PID', 'COOPMERCHANTS_STATE', 'COOPMERCHANTS_TELEPHONE', 'COOPMERCHANTS_TYPE', 'LINKER_MOBILEPHONE', 'LINKER_NAME', 'MERCHANTTYPE_ID', 'MERCHANTTYPE_NAME', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAFF_NAME', 'TAXPAYER_IDENTIFYCODE'] vs ['BANK_ACCOUNT', 'BANK_NAME', 'BrandList', 'COOPMERCHANTS_ADDRESS', 'COOPMERCHANTS_BRAND', 'COOPMERCHANTS_CODE', 'COOPMERCHANTS_DESC', 'COOPMERCHANTS_DRAWER', 'COOPMERCHANTS_EN', 'COOPMERCHANTS_ID', 'COOPMERCHANTS_LINKMAN', 'COOPMERCHANTS_MOBILEPHONE', 'COOPMERCHANTS_NAME', 'COOPMERCHANTS_NATURE', 'COOPMERCHANTS_PID', 'COOPMERCHANTS_STATE', 'COOPMERCHANTS_TELEPHONE', 'COOPMERCHANTS_TYPE', 'LINKER_MOBILEPHONE', 'LINKER_NAME', 'MERCHANTTYPE_ID', 'MERCHANTTYPE_NAME', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAFF_NAME', 'TAXPAYER_IDENTIFYCODE'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `230.58 ms`
新 API 状态: `200`，耗时 `2123.07 ms`

### Merchants/GetCoopMerchantsLinkerDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsLinkerId": 383}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCoopMerchantsLinkerDetail | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCoopMerchantsLinkerDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BANK_ACCOUNT', 'BANK_NAME', 'COOPMERCHANTS_DRAWER', 'COOPMERCHANTS_ID', 'COOPMERCHANTS_LINKER_DESC', 'COOPMERCHANTS_LINKER_ID', 'LINKER_ADDRESS', 'LINKER_MOBILEPHONE', 'LINKER_NAME', 'LINKER_STATE', 'LINKER_TELEPHONE', 'OPERATE_DATE', 'STAFF_ID', 'STAFF_NAME'] vs ['BANK_ACCOUNT', 'BANK_NAME', 'COOPMERCHANTS_DRAWER', 'COOPMERCHANTS_ID', 'COOPMERCHANTS_LINKER_DESC', 'COOPMERCHANTS_LINKER_ID', 'LINKER_ADDRESS', 'LINKER_MOBILEPHONE', 'LINKER_NAME', 'LINKER_STATE', 'LINKER_TELEPHONE', 'OPERATE_DATE', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `106.88 ms`
新 API 状态: `200`，耗时 `25.79 ms`

### Merchants/GetCoopMerchantsLinkerList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COOPMERCHANTS_LINKER_ID": 383}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCoopMerchantsLinkerList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCoopMerchantsLinkerList |
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
| 首条字段集合 | ✅ | 字段一致，共 14 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `137.64 ms`
新 API 状态: `200`，耗时 `18.1 ms`

### Merchants/GetCoopMerchantsList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COOPMERCHANTS_ID": -2867}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCoopMerchantsList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCoopMerchantsList |
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
| 首条字段集合 | ✅ | 字段一致，共 29 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `167.73 ms`
新 API 状态: `200`，耗时 `23.65 ms`

### Merchants/GetCoopMerchantsTypeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCoopMerchantsTypeList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCoopMerchantsTypeList |
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
| 首条字段集合 | ✅ | 字段一致，共 17 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `140.17 ms`
新 API 状态: `200`，耗时 `49.82 ms`

### Merchants/GetRTCoopMerchantsList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetRTCoopMerchantsList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetRTCoopMerchantsList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 0 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 0 vs 0 |
| List 条数 | ✅ | 0 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `129.36 ms`
新 API 状态: `200`，耗时 `11.09 ms`

### Merchants/GetTradeBrandMerchantsList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}, "SortStr": "RTCOOPMERCHANTS_ID"}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetTradeBrandMerchantsList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetTradeBrandMerchantsList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 611 vs 611 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 12 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `488.64 ms`
新 API 状态: `200`，耗时 `109.81 ms`
