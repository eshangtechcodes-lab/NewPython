# 动态接口对比报告

- 生成时间: 2026-03-10 23:48:50
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_ssv.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 4 / FAIL 2 / SKIP 0 / TOTAL 6`

## 用例明细

### Sales/GetCOMMODITYSALEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetCOMMODITYSALEDetail | 新 API: http://localhost:8080/EShangApiMain/Sales/GetCOMMODITYSALEDetail |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Message'] vs ['Message'] |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Sales/GetCOMMODITYSALEDetail”匹配的 HTTP 资源。' vs '找不到与请求 URI“http://localhost:8080/EShangApiMain/Sales/GetCOMMODITYSALEDetail”匹配的 HTTP 资源。')

原 API 状态: `404`，耗时 `24.29 ms`
新 API 状态: `200`，耗时 `2058.94 ms`

### Sales/GetCOMMODITYSALEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetCOMMODITYSALEList | 新 API: http://localhost:8080/EShangApiMain/Sales/GetCOMMODITYSALEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ✅ | 查询失败未将对象引用设置到对象的实例。 vs 查询失败未将对象引用设置到对象的实例。 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `5.22 ms`
新 API 状态: `200`，耗时 `3.6 ms`

### Sales/GetEndaccountError / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetEndaccountError | 新 API: http://localhost:8080/EShangApiMain/Sales/GetEndaccountError |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ✅ | 处理失败未将对象引用设置到对象的实例。 vs 处理失败未将对象引用设置到对象的实例。 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `8.43 ms`
新 API 状态: `200`，耗时 `4.23 ms`

### Supplier/GetQUALIFICATION_HISList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetQUALIFICATION_HISList | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetQUALIFICATION_HISList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ✅ | 查询失败未将对象引用设置到对象的实例。 vs 查询失败未将对象引用设置到对象的实例。 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `5.14 ms`
新 API 状态: `200`，耗时 `5.26 ms`

### Verification/GetShopEndaccountSum / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"EndDate": "2025-12-01", "RoleType": "1", "ServerpartId": "416", "ServerpartShopCode": "049001", "StartDate": "2025-12-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetShopEndaccountSum | 新 API: http://localhost:8080/EShangApiMain/Verification/GetShopEndaccountSum |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['Deal_Count', 'Revenue_Amount', 'Revenue_Amount_A', 'Revenue_Amount_B', 'ServerpartShop_Code', 'ServerpartShop_ICO', 'ServerpartShop_Name', 'Serverpart_ID', 'Serverpart_Name', 'ShopRegion_Name_A', 'ShopRegion_Name_B', 'Total_Count', 'Treatment_MarkState', 'VerifiedList', 'VerifyList'] vs ['Deal_Count', 'Revenue_Amount', 'Revenue_Amount_A', 'Revenue_Amount_B', 'ServerpartShop_Code', 'ServerpartShop_Name', 'Serverpart_ID', 'Serverpart_Name', 'Total_Count', 'Treatment_MarkState', 'VerifiedList', 'VerifyList'] |
| 完整响应体 | ❌ | 发现 10 处差异 |

差异明细：
- Result_Data.ServerpartShop_ICO: 新 API 缺少该字段
- Result_Data.ShopRegion_Name_A: 新 API 缺少该字段
- Result_Data.ShopRegion_Name_B: 新 API 缺少该字段
- Result_Data.Deal_Count: 值不一致 (2 vs 0)
- Result_Data.Revenue_Amount: 类型不一致 (float vs int)，值为 15048.2 vs 0
- Result_Data.Revenue_Amount_A: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.Revenue_Amount_B: 类型不一致 (float vs int)，值为 15048.2 vs 0
- Result_Data.Total_Count: 值不一致 (2 vs 0)
- Result_Data.Treatment_MarkState: 值不一致 (0 vs -1)
- Result_Data.VerifiedList: 列表长度不一致 (2 vs 0)

原 API 状态: `200`，耗时 `261.31 ms`
新 API 状态: `200`，耗时 `1019.12 ms`

### Verification/GetSuppEndaccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetSuppEndaccountList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetSuppEndaccountList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 73 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `205.76 ms`
新 API 状态: `200`，耗时 `277.21 ms`
