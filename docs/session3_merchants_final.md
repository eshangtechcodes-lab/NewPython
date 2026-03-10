# 动态接口对比报告

- 生成时间: 2026-03-10 17:20:47
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\modules\merchants.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 0 / FAIL 7 / SKIP 0 / TOTAL 7`

## 用例明细

### Merchants/GetCoopMerchantsDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsId": 1}`
- JSON: `null`
- 结果: `FAIL`

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
| 完整响应体 | ❌ | 发现 12 处差异 |

差异明细：
- Result_Data.COOPMERCHANTS_ADDRESS: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_BRAND: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_DRAWER: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_LINKMAN: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_MOBILEPHONE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_TELEPHONE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_TYPE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.LINKER_MOBILEPHONE: 类型不一致 (NoneType vs str)，值为 None vs '0571-81991302'
- Result_Data.LINKER_NAME: 类型不一致 (NoneType vs str)，值为 None vs '杨雅意'
- Result_Data.MERCHANTTYPE_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OPERATE_DATE: 值不一致 ('2017-01-10T20:32:50' vs '2017/1/10 20:32:50')

原 API 状态: `200`，耗时 `179.35 ms`
新 API 状态: `200`，耗时 `2096.98 ms`

### Merchants/GetCoopMerchantsLinkerDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsLinkerId": 383}`
- JSON: `null`
- 结果: `FAIL`

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
| 完整响应体 | ❌ | 发现 7 处差异 |

差异明细：
- Result_Data.BANK_ACCOUNT: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.BANK_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_DRAWER: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COOPMERCHANTS_LINKER_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.LINKER_ADDRESS: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.LINKER_TELEPHONE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OPERATE_DATE: 值不一致 ('2021-04-01T15:29:15' vs '2021/4/1 15:29:15')

原 API 状态: `200`，耗时 `105.31 ms`
新 API 状态: `200`，耗时 `15.95 ms`

### Merchants/GetCoopMerchantsLinkerList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COOPMERCHANTS_LINKER_ID": 383}}`
- 结果: `FAIL`

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
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2021-04-01T15:29:15' vs '2021/4/1 15:29:15')

原 API 状态: `200`，耗时 `82.5 ms`
新 API 状态: `200`，耗时 `13.29 ms`

### Merchants/GetCoopMerchantsList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COOPMERCHANTS_ID": -2867}}`
- 结果: `FAIL`

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
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List[0].COOPMERCHANTS_PID: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2026-02-10T14:59:47' vs '2026/2/10 14:59:47')

原 API 状态: `200`，耗时 `99.65 ms`
新 API 状态: `200`，耗时 `28.76 ms`

### Merchants/GetCoopMerchantsTypeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

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
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2021-12-16T10:27:35' vs '2021/12/16 10:27:35')
- Result_Data.List[1].OPERATE_DATE: 值不一致 ('2021-12-16T10:27:42' vs '2021/12/16 10:27:42')

原 API 状态: `200`，耗时 `195.95 ms`
新 API 状态: `200`，耗时 `12.23 ms`

### Merchants/GetRTCoopMerchantsList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetRTCoopMerchantsList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetRTCoopMerchantsList |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Merchants/GetRTCoopMerchantsList”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `6.19 ms`
新 API 状态: `200`，耗时 `2.65 ms`

### Merchants/GetTradeBrandMerchantsList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetTradeBrandMerchantsList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetTradeBrandMerchantsList |
| HTTP 状态码 | ❌ | 415 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Desc'] |
| Result_Code | ❌ | None vs 999 |
| Result_Desc | ❌ | None vs 查询失败[CODE:-2111]第19 行附近出现错误:
无效的列名[NONE] |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `415`，耗时 `3.44 ms`
新 API 状态: `200`，耗时 `26.28 ms`
