# 动态接口对比报告

- 生成时间: 2026-03-10 16:59:07
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

原 API 状态: `200`，耗时 `264.54 ms`
新 API 状态: `200`，耗时 `2072.53 ms`

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

原 API 状态: `200`，耗时 `100.27 ms`
新 API 状态: `200`，耗时 `11.71 ms`

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

原 API 状态: `200`，耗时 `145.4 ms`
新 API 状态: `200`，耗时 `11.33 ms`

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
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.List[0].BrandList: 类型不一致 (NoneType vs list)，值为 None vs [{'label': '品牌小吃', 'value': 1350.0, 'ico': ''}, {'label': '小吃', 'value': 1860.0, 'ico': ''}]
- Result_Data.List[0].COOPMERCHANTS_PID: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2026-02-10T14:59:47' vs '2026/2/10 14:59:47')

原 API 状态: `200`，耗时 `221.3 ms`
新 API 状态: `200`，耗时 `30.64 ms`

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
| TotalCount | ❌ | 2 vs 12 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ❌ | 2 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 17 个 |
| 完整响应体 | ❌ | 发现 21 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (2 vs 9)
- Result_Data.List[0].AUTOSTATISTICS_ID: 值不一致 (260 vs 203)
- Result_Data.List[0].AUTOSTATISTICS_INDEX: 值不一致 (10 vs 1000)
- Result_Data.List[0].AUTOSTATISTICS_VALUE: 值不一致 ('1000' vs '')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2021-12-16T10:27:35' vs '2020/2/7 17:04:29')
- Result_Data.List[0].OWNERUNIT_ID: 值不一致 (249 vs 8)
- Result_Data.List[0].OWNERUNIT_NAME: 值不一致 ('安徽交控驿达服务开发集团有限公司' vs '甘肃华运高速公路服务区管理有限公司')
- Result_Data.List[0].PROVINCE_CODE: 值不一致 (340000 vs 620000)
- Result_Data.List[0].STAFF_ID: 值不一致 (776 vs 1)
- Result_Data.List[0].STAF_NAME: 值不一致 ('安徽驿达管理员' vs '系统开发者')
- Result_Data.List[1].AUTOSTATISTICS_ID: 值不一致 (316 vs 204)
- Result_Data.List[1].AUTOSTATISTICS_INDEX: 值不一致 (20 vs 2000)
- Result_Data.List[1].AUTOSTATISTICS_NAME: 值不一致 ('业主自营类' vs '品牌展销类')
- Result_Data.List[1].AUTOSTATISTICS_VALUE: 值不一致 ('2000' vs '')
- Result_Data.List[1].OPERATE_DATE: 值不一致 ('2021-12-16T10:27:42' vs '2020/2/7 17:04:34')
- Result_Data.List[1].OWNERUNIT_ID: 值不一致 (249 vs 8)
- Result_Data.List[1].OWNERUNIT_NAME: 值不一致 ('安徽交控驿达服务开发集团有限公司' vs '甘肃华运高速公路服务区管理有限公司')
- Result_Data.List[1].PROVINCE_CODE: 值不一致 (340000 vs 620000)
- Result_Data.List[1].STAFF_ID: 值不一致 (776 vs 1)
- Result_Data.List[1].STAF_NAME: 值不一致 ('安徽驿达管理员' vs '系统开发者')
- Result_Data.TotalCount: 值不一致 (2 vs 12)

原 API 状态: `200`，耗时 `112.03 ms`
新 API 状态: `200`，耗时 `11.35 ms`

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

原 API 状态: `404`，耗时 `5.68 ms`
新 API 状态: `200`，耗时 `2.17 ms`

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

原 API 状态: `415`，耗时 `5.17 ms`
新 API 状态: `200`，耗时 `34.94 ms`
