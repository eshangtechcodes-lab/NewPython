# 动态接口对比报告

- 生成时间: 2026-03-10 17:03:20
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_1.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 11 / FAIL 116 / SKIP 0 / TOTAL 127`

## 用例明细

### BaseInfo/BindingMerchantTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/BindingMerchantTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/BindingMerchantTree |
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
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `294.51 ms`
新 API 状态: `200`，耗时 `2161.18 ms`

### BaseInfo/BindingOwnerUnitDDL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"DataType": 0, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/BindingOwnerUnitDDL | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/BindingOwnerUnitDDL |
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
| 首条字段集合 | ✅ | 字段一致，共 6 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `106.7 ms`
新 API 状态: `200`，耗时 `15.85 ms`

### BaseInfo/BindingOwnerUnitTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"DataType": 0}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/BindingOwnerUnitTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/BindingOwnerUnitTree |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 19 vs 19 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 19 vs 19 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List[0].children: 类型不一致 (list vs NoneType)，值为 [] vs None
- Result_Data.List[13].children: 类型不一致 (list vs NoneType)，值为 [] vs None

原 API 状态: `200`，耗时 `173.87 ms`
新 API 状态: `200`，耗时 `11.22 ms`

### BaseInfo/GetAUTOSTATISTICSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AUTOSTATISTICSId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetAUTOSTATISTICSDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetAUTOSTATISTICSDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['AUTOSTATISTICS_DESC', 'AUTOSTATISTICS_ICO', 'AUTOSTATISTICS_ID', 'AUTOSTATISTICS_INDEX', 'AUTOSTATISTICS_NAME', 'AUTOSTATISTICS_PID', 'AUTOSTATISTICS_STATE', 'AUTOSTATISTICS_TYPE', 'AUTOSTATISTICS_VALUE', 'INELASTIC_DEMAND', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAF_NAME', 'STATISTICS_TYPE'] vs ['AUTOSTATISTICS_DESC', 'AUTOSTATISTICS_ICO', 'AUTOSTATISTICS_ID', 'AUTOSTATISTICS_INDEX', 'AUTOSTATISTICS_NAME', 'AUTOSTATISTICS_PID', 'AUTOSTATISTICS_STATE', 'AUTOSTATISTICS_TYPE', 'AUTOSTATISTICS_VALUE', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAF_NAME', 'STATISTICS_TYPE'] |
| 完整响应体 | ❌ | 发现 6 处差异 |

差异明细：
- Result_Data.INELASTIC_DEMAND: 新 API 缺少该字段
- Result_Data.AUTOSTATISTICS_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.AUTOSTATISTICS_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10260/2020_04_03_21_13_36_7765.png' vs 'https://eshangtech.com:8443/UploadImageDir/PictureManage/10260/2020_04_03_21_13_36_7765.png')
- Result_Data.AUTOSTATISTICS_VALUE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OPERATE_DATE: 值不一致 ('2021-07-08T15:17:58' vs '2021/7/8 15:17:58')
- Result_Data.STATISTICS_TYPE: 类型不一致 (NoneType vs int)，值为 None vs 0

原 API 状态: `200`，耗时 `108.85 ms`
新 API 状态: `200`，耗时 `9.85 ms`

### BaseInfo/GetAssetsRevenueAmount / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416", "searchMonth": "202512"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetAssetsRevenueAmount | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetAssetsRevenueAmount |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ❌ | 1 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 0)
- Result_Data.TotalCount: 值不一致 (1 vs 0)

原 API 状态: `200`，耗时 `179.64 ms`
新 API 状态: `200`，耗时 `13.66 ms`

### BaseInfo/GetAutoStatisticsTreeList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AutoStatistics_Type": 0, "OwnerUnit_Id": 211, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetAutoStatisticsTreeList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetAutoStatisticsTreeList |
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

原 API 状态: `200`，耗时 `185.37 ms`
新 API 状态: `200`，耗时 `28.33 ms`

### BaseInfo/GetBrandDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BrandId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBrandDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBrandDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BRAND_CATEGORY', 'BRAND_DESC', 'BRAND_ID', 'BRAND_INDEX', 'BRAND_INDUSTRY', 'BRAND_INTRO', 'BRAND_NAME', 'BRAND_PID', 'BRAND_STATE', 'BRAND_TYPE', 'BUSINESSTRADE_NAME', 'COMMISSION_RATIO', 'MANAGE_TYPE', 'MerchantID', 'MerchantID_Encrypt', 'MerchantName', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'SERVERPART_IDS', 'SPREGIONTYPE_IDS', 'STAFF_ID', 'STAFF_NAME', 'ServerpartList', 'WECHATAPPSIGN_ID', 'WECHATAPPSIGN_NAME', 'WECHATAPP_APPID'] vs ['BRAND_CATEGORY', 'BRAND_DESC', 'BRAND_ID', 'BRAND_INDEX', 'BRAND_INDUSTRY', 'BRAND_INTRO', 'BRAND_NAME', 'BRAND_PID', 'BRAND_STATE', 'BRAND_TYPE', 'COMMISSION_RATIO', 'MANAGE_TYPE', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAFF_NAME', 'ServerpartList', 'WECHATAPPSIGN_ID', 'WECHATAPPSIGN_NAME', 'WECHATAPP_APPID'] |
| 完整响应体 | ❌ | 发现 16 处差异 |

差异明细：
- Result_Data.BUSINESSTRADE_NAME: 新 API 缺少该字段
- Result_Data.MerchantID: 新 API 缺少该字段
- Result_Data.MerchantID_Encrypt: 新 API 缺少该字段
- Result_Data.MerchantName: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.SPREGIONTYPE_IDS: 新 API 缺少该字段
- Result_Data.BRAND_CATEGORY: 类型不一致 (int vs float)，值为 2000 vs 2000.0
- Result_Data.BRAND_ID: 类型不一致 (int vs float)，值为 1 vs 1.0
- Result_Data.BRAND_INDEX: 类型不一致 (int vs float)，值为 2000 vs 2000.0
- Result_Data.BRAND_INDUSTRY: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.BRAND_PID: 类型不一致 (int vs float)，值为 -1 vs -1.0
- Result_Data.BRAND_STATE: 类型不一致 (int vs float)，值为 1 vs 1.0
- Result_Data.OPERATE_DATE: 值不一致 ('2020-04-15T21:34:06' vs '2020/4/15 0:00:00')
- Result_Data.OWNERUNIT_ID: 类型不一致 (int vs float)，值为 13 vs 13.0
- Result_Data.STAFF_ID: 类型不一致 (int vs float)，值为 1492 vs 1492.0
- Result_Data.WECHATAPPSIGN_ID: 类型不一致 (int vs float)，值为 13 vs 13.0

原 API 状态: `200`，耗时 `304.68 ms`
新 API 状态: `200`，耗时 `33.39 ms`

### BaseInfo/GetBrandList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"BRAND_ID": 1314}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBrandList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBrandList |
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
| 首条字段集合 | ❌ | 仅原 API: ['MerchantID_Encrypt', 'SERVERPART_IDS', 'SPREGIONTYPE_IDS'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].MerchantID_Encrypt: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_IDS: 新 API 缺少该字段
- Result_Data.List[0].BRAND_CATEGORY: 类型不一致 (int vs float)，值为 1000 vs 1000.0
- Result_Data.List[0].BRAND_ID: 类型不一致 (int vs float)，值为 1314 vs 1314.0
- Result_Data.List[0].BRAND_INDEX: 类型不一致 (int vs float)，值为 10 vs 10.0
- Result_Data.List[0].BRAND_INDUSTRY: 类型不一致 (int vs str)，值为 227 vs '227'
- Result_Data.List[0].BRAND_PID: 类型不一致 (int vs float)，值为 -1 vs -1.0
- Result_Data.List[0].BRAND_STATE: 类型不一致 (int vs float)，值为 1 vs 1.0
- Result_Data.List[0].BRAND_TYPE: 类型不一致 (int vs float)，值为 3000 vs 3000.0
- Result_Data.List[0].BUSINESSTRADE_NAME: 值不一致 ('西式快餐' vs '')
- Result_Data.List[0].MANAGE_TYPE: 类型不一致 (int vs float)，值为 2000 vs 2000.0
- Result_Data.List[0].MerchantID: 值不一致 ('-1115' vs '-2096')
- Result_Data.List[0].MerchantName: 值不一致 ('艾比克' vs '安徽艾芝餐饮管理有限责任公司')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2023-04-17T17:27:15' vs '2023/4/17 0:00:00')
- Result_Data.List[0].OWNERUNIT_ID: 类型不一致 (int vs float)，值为 249 vs 249.0
- Result_Data.List[0].PROVINCE_CODE: 类型不一致 (int vs float)，值为 340000 vs 340000.0
- Result_Data.List[0].STAFF_ID: 类型不一致 (int vs float)，值为 2633 vs 2633.0
- Result_Data.List[0].ServerpartList[1].label: 值不一致 ('釜山服务区' vs '四方湖服务区')
- Result_Data.List[0].ServerpartList[1].value: 值不一致 ('495' vs '443')
- Result_Data.List[0].ServerpartList[2].label: 值不一致 ('福山服务区' vs '釜山服务区')
- Result_Data.List[0].ServerpartList[2].value: 值不一致 ('520' vs '495')
- Result_Data.List[0].ServerpartList[3].label: 值不一致 ('四方湖服务区' vs '福山服务区')
- Result_Data.List[0].ServerpartList[3].value: 值不一致 ('443' vs '520')
- Result_Data.List[0].WECHATAPPSIGN_ID: 类型不一致 (int vs float)，值为 1314 vs 1314.0

原 API 状态: `200`，耗时 `339.17 ms`
新 API 状态: `200`，耗时 `91.45 ms`

### BaseInfo/GetBusinessBrandList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartShopIds": 3080}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBusinessBrandList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBusinessBrandList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 1 vs 1 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 28 个 |
| 完整响应体 | ❌ | 发现 16 处差异 |

差异明细：
- Result_Data.List[0].BRAND_CATEGORY: 类型不一致 (int vs float)，值为 1000 vs 1000.0
- Result_Data.List[0].BRAND_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.List[0].BRAND_ID: 类型不一致 (int vs float)，值为 696 vs 696.0
- Result_Data.List[0].BRAND_INDEX: 类型不一致 (int vs float)，值为 10 vs 10.0
- Result_Data.List[0].BRAND_PID: 类型不一致 (int vs float)，值为 -1 vs -1.0
- Result_Data.List[0].BRAND_STATE: 类型不一致 (int vs float)，值为 1 vs 1.0
- Result_Data.List[0].BRAND_TYPE: 类型不一致 (int vs float)，值为 2000 vs 2000.0
- Result_Data.List[0].COMMISSION_RATIO: 类型不一致 (NoneType vs str)，值为 None vs '18%-20%'
- Result_Data.List[0].MANAGE_TYPE: 类型不一致 (NoneType vs float)，值为 None vs 2000.0
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2023-04-18T09:33:35' vs '2023/4/18T0:00:00')
- Result_Data.List[0].OWNERUNIT_ID: 类型不一致 (int vs float)，值为 249 vs 249.0
- Result_Data.List[0].PROVINCE_CODE: 类型不一致 (int vs float)，值为 340000 vs 340000.0
- Result_Data.List[0].STAFF_ID: 类型不一致 (int vs float)，值为 2633 vs 2633.0
- Result_Data.List[0].WECHATAPPSIGN_ID: 类型不一致 (int vs float)，值为 696 vs 696.0
- Result_Data.List[0].WECHATAPPSIGN_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.List[0].WECHATAPP_APPID: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `263.48 ms`
新 API 状态: `200`，耗时 `16.29 ms`

### BaseInfo/GetBusinessTradeDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessTradeId": 214}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBusinessTradeDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBusinessTradeDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['AUTOSTATISTICS_DESC', 'AUTOSTATISTICS_ICO', 'AUTOSTATISTICS_ID', 'AUTOSTATISTICS_INDEX', 'AUTOSTATISTICS_NAME', 'AUTOSTATISTICS_PID', 'AUTOSTATISTICS_STATE', 'AUTOSTATISTICS_TYPE', 'AUTOSTATISTICS_VALUE', 'INELASTIC_DEMAND', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAF_NAME', 'STATISTICS_TYPE'] vs ['AUTOSTATISTICS_DESC', 'AUTOSTATISTICS_ICO', 'AUTOSTATISTICS_ID', 'AUTOSTATISTICS_INDEX', 'AUTOSTATISTICS_NAME', 'AUTOSTATISTICS_PID', 'AUTOSTATISTICS_STATE', 'AUTOSTATISTICS_TYPE', 'AUTOSTATISTICS_VALUE', 'INELASTIC_DEMAND', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'STAFF_ID', 'STAF_NAME', 'STATISTICS_TYPE'] |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- Result_Data.AUTOSTATISTICS_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.AUTOSTATISTICS_VALUE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.INELASTIC_DEMAND: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:26' vs '2024/11/8 17:39:26')

原 API 状态: `200`，耗时 `77.76 ms`
新 API 状态: `200`，耗时 `9.97 ms`

### BaseInfo/GetBusinessTradeEnum / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessTradeState": 1, "BusinessTrade_PID": 214, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBusinessTradeEnum | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBusinessTradeEnum |
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
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 7 处差异 |

差异明细：
- Result_Data.List[0].children[0].node.desc: 新 API 缺少该字段
- Result_Data.List[0].children[1].node.desc: 新 API 缺少该字段
- Result_Data.List[0].children[2].node.desc: 新 API 缺少该字段
- Result_Data.List[0].children[3].node.desc: 新 API 缺少该字段
- Result_Data.List[0].children[4].node.desc: 新 API 缺少该字段
- Result_Data.List[0].children[5].node.desc: 新 API 缺少该字段
- Result_Data.List[0].node.desc: 新 API 缺少该字段

原 API 状态: `200`，耗时 `172.48 ms`
新 API 状态: `200`，耗时 `14.37 ms`

### BaseInfo/GetBusinessTradeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PROVINCE_CODE": 340000}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBusinessTradeList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBusinessTradeList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 41 vs 41 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 17 个 |
| 完整响应体 | ❌ | 发现 9 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024-11-08T17:39:26' vs '2024/11/8 17:39:26')
- Result_Data.List[1].OPERATE_DATE: 值不一致 ('2024-11-08T17:39:59' vs '2024/11/8 17:39:59')
- Result_Data.List[2].OPERATE_DATE: 值不一致 ('2024-11-08T17:41:21' vs '2024/11/8 17:41:21')
- Result_Data.List[3].OPERATE_DATE: 值不一致 ('2024-11-08T17:39:35' vs '2024/11/8 17:39:35')
- Result_Data.List[4].OPERATE_DATE: 值不一致 ('2024-11-08T17:39:45' vs '2024/11/8 17:39:45')
- Result_Data.List[5].OPERATE_DATE: 值不一致 ('2024-11-08T17:39:42' vs '2024/11/8 17:39:42')
- Result_Data.List[6].OPERATE_DATE: 值不一致 ('2024-11-08T17:39:54' vs '2024/11/8 17:39:54')
- Result_Data.List[7].OPERATE_DATE: 值不一致 ('2024-11-08T17:40:31' vs '2024/11/8 17:40:31')
- Result_Data.List[8].OPERATE_DATE: 值不一致 ('2024-11-08T17:40:36' vs '2024/11/8 17:40:36')

原 API 状态: `200`，耗时 `200.08 ms`
新 API 状态: `200`，耗时 `23.8 ms`

### BaseInfo/GetBusinessTradeTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessTradeState": 1, "BusinessTrade_PID": -1, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetBusinessTradeTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetBusinessTradeTree |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 6 vs 6 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 6 vs 6 |
| List 条数 | ✅ | 6 vs 6 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:35' vs '2024/11/8 17:39:35')
- Result_Data.List[0].children[0].node.STATISTICS_TYPE: 值不一致 (35 vs 0)
- Result_Data.List[0].children[1].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:42' vs '2024/11/8 17:39:42')
- Result_Data.List[0].children[1].node.STATISTICS_TYPE: 值不一致 (20 vs 0)
- Result_Data.List[0].children[2].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:45' vs '2024/11/8 17:39:45')
- Result_Data.List[0].children[2].node.STATISTICS_TYPE: 值不一致 (11 vs 0)
- Result_Data.List[0].children[3].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:51' vs '2024/11/8 17:39:51')
- Result_Data.List[0].children[3].node.STATISTICS_TYPE: 值不一致 (27 vs 0)
- Result_Data.List[0].children[4].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:54' vs '2024/11/8 17:39:54')
- Result_Data.List[0].children[5].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:59' vs '2024/11/8 17:39:59')
- Result_Data.List[0].children[5].node.STATISTICS_TYPE: 值不一致 (2 vs 0)
- Result_Data.List[0].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:39:26' vs '2024/11/8 17:39:26')
- Result_Data.List[0].node.STATISTICS_TYPE: 值不一致 (95 vs 0)
- Result_Data.List[1].children[0].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:40:25' vs '2024/11/8 17:40:25')
- Result_Data.List[1].children[0].node.STATISTICS_TYPE: 值不一致 (66 vs 0)
- Result_Data.List[1].children[1].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:40:28' vs '2024/11/8 17:40:28')
- Result_Data.List[1].children[1].node.STATISTICS_TYPE: 值不一致 (23 vs 0)
- Result_Data.List[1].children[2].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:40:31' vs '2024/11/8 17:40:31')
- Result_Data.List[1].children[2].node.STATISTICS_TYPE: 值不一致 (3 vs 0)
- Result_Data.List[1].children[3].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:40:36' vs '2024/11/8 17:40:36')
- Result_Data.List[1].children[3].node.STATISTICS_TYPE: 值不一致 (16 vs 0)
- Result_Data.List[1].children[4].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:40:55' vs '2024/11/8 17:40:55')
- Result_Data.List[1].children[4].node.STATISTICS_TYPE: 值不一致 (1 vs 0)
- Result_Data.List[1].children[5].node.OPERATE_DATE: 值不一致 ('2024-11-08T17:41:03' vs '2024/11/8 17:41:03')
- Result_Data.List[1].children[5].node.STATISTICS_TYPE: 值不一致 (7 vs 0)

原 API 状态: `200`，耗时 `145.35 ms`
新 API 状态: `200`，耗时 `27.14 ms`

### BaseInfo/GetCASHWORKERDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CASHWORKERId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCASHWORKERDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCASHWORKERDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BIRTH', 'CASHWORKER_ID', 'CASHWORKER_LOGINNAME', 'CASHWORKER_LOGINPWD', 'CASHWORKER_NAME', 'CASHWORKER_TYPE', 'DISCOUNT_RATE', 'EDUCATIONAL', 'HEALTHCERT', 'LINKTEL', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'OPERATE_ID', 'OPERATE_NAME', 'PERSONCERT', 'POST', 'SERVERPART_CODE', 'SERVERPART_CODES', 'SERVERPART_ID', 'SERVERPART_IDS', 'ServerPart_Name', 'WORKER_ADDRESS', 'WORKER_CODE', 'WORKER_OTHER', 'WORKER_VALID', 'WORK_OLD'] vs ['BIRTH', 'CASHWORKER_ID', 'CASHWORKER_LOGINNAME', 'CASHWORKER_LOGINPWD', 'CASHWORKER_NAME', 'CASHWORKER_TYPE', 'DISCOUNT_RATE', 'EDUCATIONAL', 'HEALTHCERT', 'LINKTEL', 'OPERATE_DATE', 'OPERATE_ID', 'OPERATE_NAME', 'PERSONCERT', 'POST', 'SERVERPART_CODE', 'SERVERPART_ID', 'WORKER_ADDRESS', 'WORKER_CODE', 'WORKER_OTHER', 'WORKER_VALID', 'WORK_OLD'] |
| 完整响应体 | ❌ | 发现 5 处差异 |

差异明细：
- Result_Data.OPERATE_DATE_End: 新 API 缺少该字段
- Result_Data.OPERATE_DATE_Start: 新 API 缺少该字段
- Result_Data.SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.ServerPart_Name: 新 API 缺少该字段

原 API 状态: `200`，耗时 `135.33 ms`
新 API 状态: `200`，耗时 `11.14 ms`

### BaseInfo/GetCASHWORKERList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 99, "SearchParameter": {"CASHWORKER_ID": "1477"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCASHWORKERList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCASHWORKERList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 2 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 99 vs 99 |
| List 条数 | ❌ | 1 vs 2 |
| 首条字段集合 | ❌ | 仅原 API: ['OPERATE_DATE_End', 'OPERATE_DATE_Start', 'SERVERPART_CODES', 'SERVERPART_IDS'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 6 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 2)
- Result_Data.List[0].OPERATE_DATE_End: 新 API 缺少该字段
- Result_Data.List[0].OPERATE_DATE_Start: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.TotalCount: 值不一致 (1 vs 2)

原 API 状态: `200`，耗时 `207.97 ms`
新 API 状态: `200`，耗时 `16.06 ms`

### BaseInfo/GetCOMMODITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYId": 864}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCOMMODITYDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCOMMODITYDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ADDTIME', 'BUSINESSTYPE', 'CANSALE', 'COMMODITY_BARCODE', 'COMMODITY_BUSINESS_ID', 'COMMODITY_CODE', 'COMMODITY_DESC', 'COMMODITY_EN', 'COMMODITY_GRADE', 'COMMODITY_HOTKEY', 'COMMODITY_ID', 'COMMODITY_MEMBERPRICE', 'COMMODITY_NAME', 'COMMODITY_ORI', 'COMMODITY_PURCHASEPRICE', 'COMMODITY_RETAILPRICE', 'COMMODITY_RULE', 'COMMODITY_STATE', 'COMMODITY_SYMBOL', 'COMMODITY_TYPE', 'COMMODITY_UNIT', 'DUTY_PARAGRAPH', 'HIGHWAYPROINST_ID', 'ISBULK', 'METERINGMETHOD', 'OPERATE_DATE', 'PROVINCE_CODE', 'QUALIFICATIONList', 'QUALIFICATION_ID', 'RETAIL_DUTY', 'SERVERPARTSHOP_IDS', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SHOPNAME', 'USERDEFINEDTYPE_ID', 'originCommodity'] vs ['ADDTIME', 'BUSINESSTYPE', 'CANSALE', 'COMMODITY_ALLNAME', 'COMMODITY_BARCODE', 'COMMODITY_BRAND', 'COMMODITY_CODE', 'COMMODITY_COUNT', 'COMMODITY_CURRPRICE', 'COMMODITY_DESC', 'COMMODITY_EN', 'COMMODITY_FROZENCOUNT', 'COMMODITY_GRADE', 'COMMODITY_GROUPPRICE', 'COMMODITY_HOTKEY', 'COMMODITY_ID', 'COMMODITY_MAXPRICE', 'COMMODITY_MEMBERPRICE', 'COMMODITY_MINPRICE', 'COMMODITY_NAME', 'COMMODITY_ORI', 'COMMODITY_ORIPRICE', 'COMMODITY_PROMOTIONPRICE', 'COMMODITY_PURCHASEPRICE', 'COMMODITY_RETAILPRICE', 'COMMODITY_RULE', 'COMMODITY_SERVERCODE', 'COMMODITY_STATE', 'COMMODITY_SYMBOL', 'COMMODITY_TYPE', 'COMMODITY_UNIFORMPRICE', 'COMMODITY_UNIT', 'DUTY_PARAGRAPH', 'ISBULK', 'METERINGMETHOD', 'OPERATE_DATE', 'PROVINCE_CODE', 'RETAIL_DUTY', 'SERVERPART_ID', 'SUPPLIER_ID', 'USERDEFINEDTYPE_ID'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.COMMODITY_BUSINESS_ID: 新 API 缺少该字段
- Result_Data.HIGHWAYPROINST_ID: 新 API 缺少该字段
- Result_Data.QUALIFICATIONList: 新 API 缺少该字段
- Result_Data.QUALIFICATION_ID: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.SHOPNAME: 新 API 缺少该字段
- Result_Data.originCommodity: 新 API 缺少该字段
- Result_Data.COMMODITY_ALLNAME: 新 API 多出该字段
- Result_Data.COMMODITY_BRAND: 新 API 多出该字段
- Result_Data.COMMODITY_COUNT: 新 API 多出该字段
- Result_Data.COMMODITY_CURRPRICE: 新 API 多出该字段
- Result_Data.COMMODITY_FROZENCOUNT: 新 API 多出该字段
- Result_Data.COMMODITY_GROUPPRICE: 新 API 多出该字段
- Result_Data.COMMODITY_MAXPRICE: 新 API 多出该字段
- Result_Data.COMMODITY_MINPRICE: 新 API 多出该字段
- Result_Data.COMMODITY_ORIPRICE: 新 API 多出该字段
- Result_Data.COMMODITY_PROMOTIONPRICE: 新 API 多出该字段
- Result_Data.COMMODITY_SERVERCODE: 新 API 多出该字段
- Result_Data.COMMODITY_UNIFORMPRICE: 新 API 多出该字段
- Result_Data.SUPPLIER_ID: 新 API 多出该字段
- Result_Data.ADDTIME: 值不一致 ('2018-11-07T17:00:46' vs '2018/11/7 17:00:46')
- Result_Data.COMMODITY_EN: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COMMODITY_HOTKEY: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `194.27 ms`
新 API 状态: `200`，耗时 `32.47 ms`

### BaseInfo/GetCOMMODITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITY_ID": 864}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCOMMODITYList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCOMMODITYList |
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
| 首条字段集合 | ❌ | 仅原 API: ['HIGHWAYPROINST_ID', 'QUALIFICATIONList', 'SERVERPARTSHOP_IDS', 'SERVERPART_IDS', 'originCommodity'] | 仅新 API: ['COMMODITY_ALLNAME', 'COMMODITY_BRAND', 'COMMODITY_COUNT', 'COMMODITY_CURRPRICE', 'COMMODITY_FROZENCOUNT', 'COMMODITY_GROUPPRICE', 'COMMODITY_MAXPRICE', 'COMMODITY_MINPRICE', 'COMMODITY_ORIPRICE', 'COMMODITY_PROMOTIONPRICE', 'COMMODITY_SERVERCODE', 'COMMODITY_UNIFORMPRICE', 'SUPPLIER_ID'] |
| 完整响应体 | ❌ | 发现 20 处差异 |

差异明细：
- Result_Data.List[0].HIGHWAYPROINST_ID: 新 API 缺少该字段
- Result_Data.List[0].QUALIFICATIONList: 新 API 缺少该字段
- Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].originCommodity: 新 API 缺少该字段
- Result_Data.List[0].COMMODITY_ALLNAME: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_BRAND: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_COUNT: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_CURRPRICE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_FROZENCOUNT: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_GROUPPRICE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_MAXPRICE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_MINPRICE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_ORIPRICE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_PROMOTIONPRICE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_SERVERCODE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_UNIFORMPRICE: 新 API 多出该字段
- Result_Data.List[0].SUPPLIER_ID: 新 API 多出该字段
- Result_Data.List[0].ADDTIME: 值不一致 ('2018-11-07T17:00:46' vs '2018/11/7 17:00:46')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2021-11-03T18:08:07' vs '2021/11/3 18:08:07')

原 API 状态: `200`，耗时 `1941.18 ms`
新 API 状态: `200`，耗时 `85.24 ms`

### BaseInfo/GetCOMMODITYTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYTYPEId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCOMMODITYTYPEDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCOMMODITYTYPEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ADDTIME', 'CIGARETTE_TYPE', 'COMMODITYTYPE_CODE', 'COMMODITYTYPE_DESC', 'COMMODITYTYPE_EN', 'COMMODITYTYPE_ID', 'COMMODITYTYPE_INDEX', 'COMMODITYTYPE_NAME', 'COMMODITYTYPE_PID', 'COMMODITYTYPE_VALID', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'PROVINCE_CODE', 'PROVINCE_ID', 'STAFF_ID', 'STAFF_NAME'] vs ['ADDTIME', 'CIGARETTE_TYPE', 'COMMODITYTYPE_CODE', 'COMMODITYTYPE_DESC', 'COMMODITYTYPE_EN', 'COMMODITYTYPE_ID', 'COMMODITYTYPE_INDEX', 'COMMODITYTYPE_NAME', 'COMMODITYTYPE_PID', 'COMMODITYTYPE_VALID', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'PROVINCE_CODE', 'PROVINCE_ID', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.COMMODITYTYPE_EN: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.COMMODITYTYPE_ID: 类型不一致 (int vs float)，值为 1 vs 1.0
- Result_Data.STAFF_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `117.33 ms`
新 API 状态: `200`，耗时 `10.63 ms`

### BaseInfo/GetCOMMODITYTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITYTYPE_ID": 418}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCOMMODITYTYPEList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCOMMODITYTYPEList |
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
| 首条字段集合 | ✅ | 字段一致，共 17 个 |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.List[0].ADDTIME: 值不一致 ('2020-04-02T15:35:33' vs '2020/4/2 15:35:33')
- Result_Data.List[0].COMMODITYTYPE_ID: 类型不一致 (int vs float)，值为 418 vs 418.0
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2020-09-10T11:18:05' vs '2020/9/10 11:18:05')

原 API 状态: `200`，耗时 `136.18 ms`
新 API 状态: `200`，耗时 `15.73 ms`

### BaseInfo/GetCombineBrandList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BRAND_TYPE": 2000, "PROVINCE_CODE": 340000}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetCombineBrandList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetCombineBrandList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 43 vs 43 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 43 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ✅ | 43 vs 43 |
| 首条字段集合 | ❌ | 仅原 API: ['BRAND_TYPENAME', 'BUSINESS_TRADE', 'COMMISSION_RATIO', 'MerchantName', 'REVENUE_AMOUNT', 'REVENUE_DAILYAMOUNT', 'ROYALTY_PRICE', 'SETTLEMENT_MODES', 'WECHATAPP_APPID'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BRAND_TYPENAME: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADE: 新 API 缺少该字段
- Result_Data.List[0].COMMISSION_RATIO: 新 API 缺少该字段
- Result_Data.List[0].MerchantName: 新 API 缺少该字段
- Result_Data.List[0].REVENUE_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].REVENUE_DAILYAMOUNT: 新 API 缺少该字段
- Result_Data.List[0].ROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.List[0].SETTLEMENT_MODES: 新 API 缺少该字段
- Result_Data.List[0].WECHATAPP_APPID: 新 API 缺少该字段
- Result_Data.List[0].BRAND_CATEGORY: 类型不一致 (int vs float)，值为 1000 vs 1000.0
- Result_Data.List[0].BRAND_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.List[0].BRAND_ID: 类型不一致 (int vs float)，值为 696 vs 670.0
- Result_Data.List[0].BRAND_INDEX: 类型不一致 (int vs float)，值为 10 vs 10.0
- Result_Data.List[0].BRAND_INDUSTRY: 值不一致 ('244' vs '243')
- Result_Data.List[0].BRAND_INTRO: 值不一致 ('https://api.eshangtech.com/EShangApiMain/UploadImageDir/BRAND/202304180933371258_驿达万佳_1681781175.jpg' vs '/UploadImageDir/PictureManage/10292/2021_02_03_12_03_53_4354.png')
- Result_Data.List[0].BRAND_NAME: 值不一致 ('驿达万佳生活馆' vs '刘鸿盛')
- Result_Data.List[0].BRAND_PID: 类型不一致 (int vs float)，值为 -1 vs -1.0
- Result_Data.List[0].BRAND_STATE: 类型不一致 (int vs float)，值为 1 vs 1.0
- Result_Data.List[0].BRAND_TYPE: 值不一致 ('2000' vs '2000.0')
- Result_Data.List[0].BUSINESSTRADE_NAME: 值不一致 ('商超零售' vs '地方特色小吃')
- Result_Data.List[0].BusinessState: 类型不一致 (int vs NoneType)，值为 1000 vs None
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2023-04-18T09:33:35' vs '2021/2/3 0:00:00')
- Result_Data.List[0].OWNERUNIT_ID: 类型不一致 (int vs float)，值为 249 vs 249.0
- Result_Data.List[0].PROVINCE_CODE: 类型不一致 (int vs float)，值为 340000 vs 340000.0
- Result_Data.List[0].STAFF_ID: 类型不一致 (int vs float)，值为 2633 vs 1342.0

原 API 状态: `200`，耗时 `904.79 ms`
新 API 状态: `200`，耗时 `116.53 ms`

### BaseInfo/GetNestingCOMMODITYTYPEList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYTYPE_PID": -1, "COMMODITYTYPE_VALID": 1, "PROVINCE_CODE": 340000}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetNestingCOMMODITYTYPEList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetNestingCOMMODITYTYPEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 10 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 0 |
| List 条数 | ❌ | 10 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (10 vs 0)
- Result_Data.PageSize: 值不一致 (10 vs 0)
- Result_Data.TotalCount: 值不一致 (10 vs 0)

原 API 状态: `200`，耗时 `115.17 ms`
新 API 状态: `200`，耗时 `53.92 ms`

### BaseInfo/GetNestingCOMMODITYTYPETree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYTYPE_PID": -1, "COMMODITYTYPE_VALID": 1, "PROVINCE_CODE": 340000}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetNestingCOMMODITYTYPETree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetNestingCOMMODITYTYPETree |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 10 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 0 |
| List 条数 | ❌ | 10 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (10 vs 0)
- Result_Data.PageSize: 值不一致 (10 vs 0)
- Result_Data.TotalCount: 值不一致 (10 vs 0)

原 API 状态: `200`，耗时 `179.39 ms`
新 API 状态: `200`，耗时 `71.33 ms`

### BaseInfo/GetNestingOwnerUnitList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"OwnerUnitNature": 1000, "ProvinceCode": 340000, "ShowStatus": true}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetNestingOwnerUnitList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetNestingOwnerUnitList |
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
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.List[0].node.OPERATE_DATE: 值不一致 ('2026-01-19T12:02:35' vs '2026/1/19 12:02:35')

原 API 状态: `200`，耗时 `125.39 ms`
新 API 状态: `200`，耗时 `17.58 ms`

### BaseInfo/GetOWNERUNITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"OWNERUNITId": 211}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetOWNERUNITDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetOWNERUNITDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['DOWNLOAD_DATE', 'ISSUPPORTPOINT', 'OPERATE_DATE', 'OWNERUNIT_DESC', 'OWNERUNIT_EN', 'OWNERUNIT_GUID', 'OWNERUNIT_ICO', 'OWNERUNIT_ID', 'OWNERUNIT_INDEX', 'OWNERUNIT_NAME', 'OWNERUNIT_NATURE', 'OWNERUNIT_PID', 'OWNERUNIT_STATE', 'PROVINCE_BUSINESSCODE', 'PROVINCE_CODE', 'STAFF_ID', 'STAFF_NAME', 'WECHATPUBLICSIGN_ID'] vs ['DOWNLOAD_DATE', 'ISSUPPORTPOINT', 'OPERATE_DATE', 'OWNERUNIT_DESC', 'OWNERUNIT_EN', 'OWNERUNIT_GUID', 'OWNERUNIT_ICO', 'OWNERUNIT_ID', 'OWNERUNIT_INDEX', 'OWNERUNIT_NAME', 'OWNERUNIT_NATURE', 'OWNERUNIT_PID', 'OWNERUNIT_STATE', 'PROVINCE_BUSINESSCODE', 'PROVINCE_CODE', 'STAFF_ID', 'STAFF_NAME', 'WECHATPUBLICSIGN_ID'] |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- Result_Data.OPERATE_DATE: 值不一致 ('2020-11-19T15:53:58' vs '2020/11/19 15:53:58')
- Result_Data.OWNERUNIT_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OWNERUNIT_EN: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OWNERUNIT_ICO: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `158.29 ms`
新 API 状态: `200`，耗时 `27.79 ms`

### BaseInfo/GetOWNERUNITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PROVINCE_CODE": 340000}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetOWNERUNITList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetOWNERUNITList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 264 vs 264 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 18 个 |
| 完整响应体 | ❌ | 发现 9 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2025-01-10T16:07:26' vs '2025/1/10 16:07:26')
- Result_Data.List[1].OPERATE_DATE: 值不一致 ('2026-02-05T13:32:04' vs '2026/2/5 13:32:04')
- Result_Data.List[2].OPERATE_DATE: 值不一致 ('2021-06-11T19:04:53' vs '2021/6/11 19:04:53')
- Result_Data.List[3].OPERATE_DATE: 值不一致 ('2021-06-11T19:05:04' vs '2021/6/11 19:05:04')
- Result_Data.List[4].OPERATE_DATE: 值不一致 ('2021-07-08T21:50:36' vs '2021/7/8 21:50:36')
- Result_Data.List[5].OPERATE_DATE: 值不一致 ('2021-08-05T10:35:13' vs '2021/8/5 10:35:13')
- Result_Data.List[6].OPERATE_DATE: 值不一致 ('2021-08-25T14:23:32' vs '2021/8/25 14:23:32')
- Result_Data.List[7].OPERATE_DATE: 值不一致 ('2021-09-01T09:34:19' vs '2021/9/1 9:34:19')
- Result_Data.List[8].OPERATE_DATE: 值不一致 ('2021-10-26T13:49:50' vs '2021/10/26 13:49:50')

原 API 状态: `200`，耗时 `239.85 ms`
新 API 状态: `200`，耗时 `17.67 ms`

### BaseInfo/GetPROPERTYASSETSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROPERTYASSETSId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetPROPERTYASSETSDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetPROPERTYASSETSDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BusinessProjectList', 'CREATE_DATE', 'EXTENDJSON', 'OPERATE_DATE', 'OPERATOR_ID', 'OPERATOR_NAME', 'PROPERTYASSETS_AMOUNT', 'PROPERTYASSETS_AREA', 'PROPERTYASSETS_CODE', 'PROPERTYASSETS_DESC', 'PROPERTYASSETS_FEETYPE', 'PROPERTYASSETS_ID', 'PROPERTYASSETS_IDS', 'PROPERTYASSETS_INDEX', 'PROPERTYASSETS_INFO', 'PROPERTYASSETS_NAME', 'PROPERTYASSETS_REGION', 'PROPERTYASSETS_STATE', 'PROPERTYASSETS_TYPE', 'PROPERTYASSETS_TYPES', 'PropertyShop', 'SERVERPART_ID', 'SERVERPART_IDS', 'STAFF_ID', 'STAFF_NAME'] vs ['BusinessProjectList', 'CREATE_DATE', 'EXTENDJSON', 'OPERATE_DATE', 'OPERATOR_ID', 'OPERATOR_NAME', 'PROPERTYASSETS_AMOUNT', 'PROPERTYASSETS_AREA', 'PROPERTYASSETS_CODE', 'PROPERTYASSETS_DESC', 'PROPERTYASSETS_FEETYPE', 'PROPERTYASSETS_ID', 'PROPERTYASSETS_INDEX', 'PROPERTYASSETS_INFO', 'PROPERTYASSETS_NAME', 'PROPERTYASSETS_REGION', 'PROPERTYASSETS_STATE', 'PROPERTYASSETS_TYPE', 'SERVERPART_ID', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ❌ | 发现 8 处差异 |

差异明细：
- Result_Data.PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.PROPERTYASSETS_TYPES: 新 API 缺少该字段
- Result_Data.PropertyShop: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.CREATE_DATE: 值不一致 ('2024-07-30T14:48:11' vs '2024/7/30 14:48:11')
- Result_Data.OPERATE_DATE: 值不一致 ('2024-08-01T10:31:10' vs '2024/8/1 10:31:10')
- Result_Data.PROPERTYASSETS_REGION: 类型不一致 (int vs float)，值为 40 vs 40.0
- Result_Data.PROPERTYASSETS_TYPE: 类型不一致 (int vs float)，值为 1000 vs 1000.0

原 API 状态: `200`，耗时 `86.43 ms`
新 API 状态: `200`，耗时 `32.3 ms`

### BaseInfo/GetPROPERTYASSETSLOGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PROPERTYASSETSLOG_ID": 6}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetPROPERTYASSETSLOGList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetPROPERTYASSETSLOGList |
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
| 首条字段集合 | ✅ | 字段一致，共 11 个 |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024-07-30T15:09:24' vs '2024/7/30 15:09:24')

原 API 状态: `200`，耗时 `252.62 ms`
新 API 状态: `200`，耗时 `17.58 ms`

### BaseInfo/GetPROPERTYASSETSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetPROPERTYASSETSList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetPROPERTYASSETSList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 51 vs 51 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'COMPACT_NAME', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'PROJECT_VALID', 'PROPERTYASSETS_IDS', 'PROPERTYASSETS_TYPES', 'REGISTERCOMPACT_ID', 'SERVERPART_IDS', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_INDEX', 'SPREGIONTYPE_NAME', 'TOTAL_AREA'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_ID: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.List[0].COMPACT_NAME: 新 API 缺少该字段
- Result_Data.List[0].PROJECT_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].PROJECT_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].PROJECT_VALID: 新 API 缺少该字段
- Result_Data.List[0].PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.List[0].PROPERTYASSETS_TYPES: 新 API 缺少该字段
- Result_Data.List[0].REGISTERCOMPACT_ID: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_INDEX: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].TOTAL_AREA: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STATE: 值不一致 (1000 vs 3000)
- Result_Data.List[0].CREATE_DATE: 值不一致 ('2024-07-30T14:48:11' vs '2024/8/13 15:59:16')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024-08-01T10:31:10' vs '2024/8/13 15:59:16')
- Result_Data.List[0].OPERATOR_ID: 值不一致 (2785 vs 3595)
- Result_Data.List[0].OPERATOR_NAME: 值不一致 ('严琅杰' vs '苹果测试机')
- Result_Data.List[0].PROPERTYASSETS_AREA: 值不一致 (289.0 vs 123.0)
- Result_Data.List[0].PROPERTYASSETS_CODE: 值不一致 ('XQ-01' vs '123')
- Result_Data.List[0].PROPERTYASSETS_DESC: 值不一致 ('测试备注' vs '')
- Result_Data.List[0].PROPERTYASSETS_ID: 值不一致 (1 vs 79)
- Result_Data.List[0].PROPERTYASSETS_INFO: 值不一致 ('测试说明信息' vs '')
- Result_Data.List[0].PROPERTYASSETS_NAME: 值不一致 ('麦当劳' vs '')

原 API 状态: `200`，耗时 `348.77 ms`
新 API 状态: `200`，耗时 `48.46 ms`

### BaseInfo/GetPROPERTYASSETSTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetPROPERTYASSETSTreeList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetPROPERTYASSETSTreeList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 52 vs 28 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].children: 列表长度不一致 (2 vs 9)
- Result_Data.List[0].children[0].children[0].children: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.BUSINESSPROJECT_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.BUSINESS_STATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.COMPACT_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.PROJECT_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.PROJECT_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.PROJECT_VALID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.PROPERTYASSETS_TYPES: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.REGISTERCOMPACT_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.SERVERPARTSHOP_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.SHOPNAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.SPREGIONTYPE_INDEX: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.TOTAL_AREA: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].node.CREATE_DATE: 类型不一致 (NoneType vs str)，值为 None vs '2024/9/2 10:57:49'
- Result_Data.List[0].children[0].children[0].node.EXTENDJSON: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.List[0].children[0].children[0].node.OPERATE_DATE: 类型不一致 (NoneType vs str)，值为 None vs '2024/9/6 18:42:19'
- Result_Data.List[0].children[0].children[0].node.OPERATOR_ID: 类型不一致 (NoneType vs int)，值为 None vs 776
- Result_Data.List[0].children[0].children[0].node.OPERATOR_NAME: 类型不一致 (NoneType vs str)，值为 None vs '安徽驿达管理员'
- Result_Data.List[0].children[0].children[0].node.PROPERTYASSETS_AREA: 值不一致 (289.0 vs 4300.8)

原 API 状态: `200`，耗时 `368.45 ms`
新 API 状态: `200`，耗时 `34.19 ms`

### BaseInfo/GetPROPERTYSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROPERTYSHOPId": 42}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetPROPERTYSHOPDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetPROPERTYSHOPDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['CREATE_DATE', 'ENDDATE', 'ENDDATE_End', 'ENDDATE_Start', 'EXTENDJSON', 'OPERATE_DATE', 'OPERATOR_ID', 'OPERATOR_NAME', 'PROPERTYASSETS_ID', 'PROPERTYASSETS_IDS', 'PROPERTYSHOP_DESC', 'PROPERTYSHOP_ID', 'PROPERTYSHOP_STATE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SERVERPART_ID', 'SERVERPART_IDS', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STARTDATE_End', 'STARTDATE_Start', 'ServerpartShop'] vs ['CREATE_DATE', 'ENDDATE', 'EXTENDJSON', 'OPERATE_DATE', 'OPERATOR_ID', 'OPERATOR_NAME', 'PROPERTYASSETS_ID', 'PROPERTYSHOP_DESC', 'PROPERTYSHOP_ID', 'PROPERTYSHOP_STATE', 'SERVERPARTSHOP_ID', 'SERVERPART_ID', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'ServerpartShop'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.ENDDATE_End: 新 API 缺少该字段
- Result_Data.ENDDATE_Start: 新 API 缺少该字段
- Result_Data.PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.STARTDATE_End: 新 API 缺少该字段
- Result_Data.STARTDATE_Start: 新 API 缺少该字段
- Result_Data.CREATE_DATE: 值不一致 ('2024-08-02T16:33:58' vs '2024/8/2 16:33:58')
- Result_Data.OPERATE_DATE: 值不一致 ('2024-08-02T16:33:58' vs '2024/8/2 16:33:58')
- Result_Data.ServerpartShop.BANK_ACCOUNT: 新 API 缺少该字段
- Result_Data.ServerpartShop.BANK_NAME: 新 API 缺少该字段
- Result_Data.ServerpartShop.PROVINCE_CODE: 新 API 缺少该字段
- Result_Data.ServerpartShop.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.ServerpartShop.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.ServerpartShop.TAXPAYER_IDENTIFYCODE: 新 API 缺少该字段
- Result_Data.ServerpartShop.COMMISSION_TYPE: 新 API 多出该字段
- Result_Data.ServerpartShop.BUSINESS_UNIT: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.BUS_STARTDATE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.LINKMAN: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.LINKMAN_MOBILE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.OPERATE_DATE: 值不一致 ('2022-09-06T07:35:31' vs '2022/9/6 7:35:31')
- Result_Data.ServerpartShop.REGISTERCOMPACT_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.SERVERPARTSHOP_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.TOPPERSON: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ServerpartShop.TOPPERSON_MOBILE: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `125.44 ms`
新 API 状态: `200`，耗时 `18.65 ms`

### BaseInfo/GetPROPERTYSHOPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetPROPERTYSHOPList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetPROPERTYSHOPList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 54 vs 54 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['ENDDATE_End', 'ENDDATE_Start', 'PROPERTYASSETS_IDS', 'SERVERPARTSHOP_IDS', 'SERVERPART_IDS', 'STARTDATE_End', 'STARTDATE_Start'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].STARTDATE_End: 新 API 缺少该字段
- Result_Data.List[0].STARTDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].CREATE_DATE: 值不一致 ('2024-08-15T14:42:29' vs '2024/8/15 14:42:29')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024-08-15T14:42:29' vs '2024/8/15 14:42:29')
- Result_Data.List[1].ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[1].ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[1].PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.List[1].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[1].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[1].STARTDATE_End: 新 API 缺少该字段
- Result_Data.List[1].STARTDATE_Start: 新 API 缺少该字段
- Result_Data.List[1].CREATE_DATE: 值不一致 ('2024-08-15T14:47:55' vs '2024/8/15 14:47:55')
- Result_Data.List[1].OPERATE_DATE: 值不一致 ('2024-08-15T14:47:55' vs '2024/8/15 14:47:55')
- Result_Data.List[2].ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[2].ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[2].PROPERTYASSETS_IDS: 新 API 缺少该字段
- Result_Data.List[2].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[2].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[2].STARTDATE_End: 新 API 缺少该字段
- Result_Data.List[2].STARTDATE_Start: 新 API 缺少该字段

原 API 状态: `200`，耗时 `130.88 ms`
新 API 状态: `200`，耗时 `12.02 ms`

### BaseInfo/GetRTSERVERPARTSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RTSERVERPARTSHOPId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetRTSERVERPARTSHOPDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetRTSERVERPARTSHOPDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BUSINESSAREA', 'BUSINESS_DATE', 'BUSINESS_ENDDATE', 'BUSINESS_NATURE', 'BUSINESS_REGION', 'BUSINESS_TYPE', 'BUSINESS_TYPES', 'BUSINESS_UNIT', 'BUS_STARTDATE', 'LINKMAN', 'LINKMAN_MOBILE', 'OPERATE_DATE', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_NAME', 'ROYALTYRATE', 'RTSERVERPARTSHOP_DESC', 'RTSERVERPARTSHOP_ID', 'SELLER_ID', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SHOPNAME', 'STAFF_ID', 'STAFF_NAME', 'TOPPERSON', 'TOPPERSON_MOBILE'] vs ['BUSINESSAREA', 'BUSINESS_DATE', 'BUSINESS_ENDDATE', 'BUSINESS_NATURE', 'BUSINESS_REGION', 'BUSINESS_TYPE', 'BUSINESS_UNIT', 'BUS_STARTDATE', 'LINKMAN', 'LINKMAN_MOBILE', 'OPERATE_DATE', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_NAME', 'ROYALTYRATE', 'RTSERVERPARTSHOP_DESC', 'RTSERVERPARTSHOP_ID', 'SELLER_ID', 'SERVERPARTSHOP_ID', 'SHOPNAME', 'STAFF_ID', 'STAFF_NAME', 'TOPPERSON', 'TOPPERSON_MOBILE'] |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.BUSINESS_TYPES: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `168.75 ms`
新 API 状态: `200`，耗时 `11.37 ms`

### BaseInfo/GetRTSERVERPARTSHOPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"RTSERVERPARTSHOP_ID": 101}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetRTSERVERPARTSHOPList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetRTSERVERPARTSHOPList |
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
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESS_TYPES', 'SERVERPARTSHOP_IDS'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List[0].BUSINESS_TYPES: 新 API 缺少该字段
- Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `171.28 ms`
新 API 状态: `200`，耗时 `15.78 ms`

### BaseInfo/GetSERVERPARTCRTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SERVERPARTTId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTCRTDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTCRTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACCOUNTBODY_CODE', 'ACCOUNTBODY_NAME', 'ACCOUNTTAX', 'COSTCENTER_CODE', 'COSTCENTER_NAME', 'DEPARTMENT_CODE', 'OPERATE_DATE', 'PROPERTYTAX', 'RESPONSIBLEDEP_CODE', 'SERVERPARTCRT_ID', 'SERVERPART_CODE', 'SERVERPART_CODES', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_INDEX', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_INDEX', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'STAYTAX'] vs ['ACCOUNTBODY_CODE', 'ACCOUNTBODY_NAME', 'ACCOUNTTAX', 'COSTCENTER_CODE', 'COSTCENTER_NAME', 'DEPARTMENT_CODE', 'OPERATE_DATE', 'PROPERTYTAX', 'RESPONSIBLEDEP_CODE', 'SERVERPARTCRT_ID', 'SERVERPART_CODE', 'SERVERPART_ID', 'STAFF_ID', 'STAFF_NAME', 'STAYTAX'] |
| 完整响应体 | ❌ | 发现 8 处差异 |

差异明细：
- Result_Data.SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_INDEX: 新 API 缺少该字段
- Result_Data.SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.SPREGIONTYPE_INDEX: 新 API 缺少该字段
- Result_Data.SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.OPERATE_DATE: 值不一致 ('2025-08-13T16:30:00' vs '2025/8/13 16:30:00')

原 API 状态: `200`，耗时 `96.0 ms`
新 API 状态: `200`，耗时 `8.58 ms`

### BaseInfo/GetSERVERPARTCRTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTCRTList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTCRTList |
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
| 首条字段集合 | ❌ | 仅原 API: ['SERVERPART_CODES', 'SERVERPART_IDS', 'SERVERPART_INDEX', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_INDEX', 'SPREGIONTYPE_NAME'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 8 处差异 |

差异明细：
- Result_Data.List[0].SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_INDEX: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_INDEX: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2025-08-13T16:30:00' vs '2025/8/13 16:30:00')

原 API 状态: `200`，耗时 `124.23 ms`
新 API 状态: `200`，耗时 `18.31 ms`

### BaseInfo/GetSERVERPARTCRTTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTCRTTreeList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTCRTTreeList |
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
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 24 处差异 |

差异明细：
- Result_Data.List[0].children[0].children: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.SERVERPART_INDEX: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.OPERATE_DATE: 值不一致 ('2025-08-13T16:30:00' vs '2025/8/13 16:30:00')
- Result_Data.List[0].node.ACCOUNTBODY_CODE: 新 API 缺少该字段
- Result_Data.List[0].node.ACCOUNTBODY_NAME: 新 API 缺少该字段
- Result_Data.List[0].node.ACCOUNTTAX: 新 API 缺少该字段
- Result_Data.List[0].node.COSTCENTER_CODE: 新 API 缺少该字段
- Result_Data.List[0].node.COSTCENTER_NAME: 新 API 缺少该字段
- Result_Data.List[0].node.DEPARTMENT_CODE: 新 API 缺少该字段
- Result_Data.List[0].node.OPERATE_DATE: 新 API 缺少该字段
- Result_Data.List[0].node.PROPERTYTAX: 新 API 缺少该字段
- Result_Data.List[0].node.RESPONSIBLEDEP_CODE: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPARTCRT_ID: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPART_CODE: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPART_ID: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPART_INDEX: 新 API 缺少该字段
- Result_Data.List[0].node.SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.List[0].node.STAFF_ID: 新 API 缺少该字段
- Result_Data.List[0].node.STAFF_NAME: 新 API 缺少该字段
- Result_Data.List[0].node.STAYTAX: 新 API 缺少该字段

原 API 状态: `200`，耗时 `190.7 ms`
新 API 状态: `200`，耗时 `38.7 ms`

### BaseInfo/GetSERVERPARTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SERVERPARTId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BUSINESSAREA', 'CITY_CODE', 'COUNTY_CODE', 'DAYINCAR', 'EXPRESSWAY_NAME', 'FIELDENUM_ID', 'FLOORAREA', 'HKBL', 'MANAGERCOMPANY', 'OPERATE_DATE', 'OWNEDCOMPANY', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'PROVINCE_NAME', 'REGIONTYPE_ID', 'REGIONTYPE_NAME', 'RtServerPart', 'SELLERCOUNT', 'SERVERPART_ADDRESS', 'SERVERPART_AREA', 'SERVERPART_CODE', 'SERVERPART_CODES', 'SERVERPART_DESC', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_INDEX', 'SERVERPART_INFO', 'SERVERPART_IPADDRESS', 'SERVERPART_NAME', 'SERVERPART_TEL', 'SERVERPART_TYPE', 'SERVERPART_X', 'SERVERPART_Y', 'SHAREAREA', 'SHORTNAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_INDEX', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STATISTICS_TYPE', 'STATISTIC_TYPE', 'ServerPartInfo', 'TOTALPARKING'] vs ['BUSINESSAREA', 'CITY_CODE', 'COUNTY_CODE', 'DAYINCAR', 'EXPRESSWAY_NAME', 'FIELDENUM_ID', 'FLOORAREA', 'HKBL', 'MANAGERCOMPANY', 'OPERATE_DATE', 'OWNEDCOMPANY', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'PROVINCE_NAME', 'REGIONTYPE_ID', 'REGIONTYPE_NAME', 'RtServerPart', 'SELLERCOUNT', 'SERVERPART_ADDRESS', 'SERVERPART_AREA', 'SERVERPART_CODE', 'SERVERPART_DESC', 'SERVERPART_ID', 'SERVERPART_INDEX', 'SERVERPART_INFO', 'SERVERPART_IPADDRESS', 'SERVERPART_NAME', 'SERVERPART_TEL', 'SERVERPART_TYPE', 'SERVERPART_X', 'SERVERPART_Y', 'SHAREAREA', 'SHORTNAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_INDEX', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STATISTICS_TYPE', 'STATISTIC_TYPE', 'ServerPartInfo', 'TOTALPARKING'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.HKBL: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OPERATE_DATE: 值不一致 ('2025-05-28T11:31:45' vs '2025/5/28 11:31:45')
- Result_Data.REGIONTYPE_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.RtServerPart.OPERATE_DATE: 值不一致 ('2025-04-28T13:40:39' vs '2025/4/28 13:40:39')
- Result_Data.RtServerPart.STARTDATE: 值不一致 ('2013-06-06T00:00:00' vs '2013/6/6 0:00:00')
- Result_Data.SELLERCOUNT: 类型不一致 (int vs float)，值为 5000 vs 5000.0
- Result_Data.SERVERPART_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.SERVERPART_IPADDRESS: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.SERVERPART_X: 值不一致 (116.893886 vs 117.0)
- Result_Data.SERVERPART_Y: 值不一致 (31.918931 vs 32.0)
- Result_Data.SHORTNAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.STARTDATE: 值不一致 ('2013-06-06T00:00:00' vs '2013/6/6 0:00:00')
- Result_Data.ServerPartInfo[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.ServerPartInfo[0].BABY_COT: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].CHANGING_TABLE: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].DROOMWATER_DISPENSER: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].HASGASSTATION: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].HASRESTROOM: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].MABROOMWATER_DISPENSER: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].NURSING_TABLE: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].REFUELINGGUN98: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].REPAIR_TEL: 新 API 多出该字段
- Result_Data.ServerPartInfo[0].REPAIR_TIME: 新 API 多出该字段

原 API 状态: `200`，耗时 `181.1 ms`
新 API 状态: `200`，耗时 `27.2 ms`

### BaseInfo/GetSERVERPARTList / search-model

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"SERVERPART_IDS": 416}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 999 vs 999 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ❌ | 仅原 API: ['RtServerPart', 'SERVERPART_CODES', 'SERVERPART_IDS', 'ServerPartInfo'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 9 处差异 |

差异明细：
- Result_Data.List[0].RtServerPart: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_CODES: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].ServerPartInfo: 新 API 缺少该字段
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2025-05-28T11:31:45' vs '2025/5/28 11:31:45')
- Result_Data.List[0].SELLERCOUNT: 类型不一致 (int vs float)，值为 5000 vs 5000.0
- Result_Data.List[0].SERVERPART_X: 值不一致 (116.893886 vs 117.0)
- Result_Data.List[0].SERVERPART_Y: 值不一致 (31.918931 vs 32.0)
- Result_Data.List[0].STARTDATE: 值不一致 ('2013-06-06T00:00:00' vs '2013/6/6 0:00:00')

原 API 状态: `200`，耗时 `89.43 ms`
新 API 状态: `200`，耗时 `24.64 ms`

### BaseInfo/GetSERVERPARTSHOP_LOGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"SERVERPART_IDS": 416}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTSHOP_LOGList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTSHOP_LOGList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 394 vs 394 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 999 vs 999 |
| List 条数 | ✅ | 394 vs 394 |
| 首条字段集合 | ❌ | 仅原 API: ['OPERATE_DATE_End', 'OPERATE_DATE_Start', 'SERVERPARTSHOP_IDS', 'SERVERPART_IDS', 'SHOPTRADES'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE_End: 新 API 缺少该字段
- Result_Data.List[0].OPERATE_DATE_Start: 新 API 缺少该字段
- Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SHOPTRADES: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_DATE: 值不一致 ('2021-02-02T00:00:00' vs '2021/2/2 0:00:00')
- Result_Data.List[0].BUSINESS_ENDDATE: 值不一致 ('2024-01-29T00:00:00' vs '2024/1/29 0:00:00')
- Result_Data.List[1].OPERATE_DATE_End: 新 API 缺少该字段
- Result_Data.List[1].OPERATE_DATE_Start: 新 API 缺少该字段
- Result_Data.List[1].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[1].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[1].SHOPTRADES: 新 API 缺少该字段
- Result_Data.List[1].BUSINESS_DATE: 值不一致 ('2021-01-30T00:00:00' vs '2021/1/30 0:00:00')
- Result_Data.List[2].OPERATE_DATE_End: 新 API 缺少该字段
- Result_Data.List[2].OPERATE_DATE_Start: 新 API 缺少该字段
- Result_Data.List[2].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[2].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[2].SHOPTRADES: 新 API 缺少该字段
- Result_Data.List[3].OPERATE_DATE_End: 新 API 缺少该字段
- Result_Data.List[3].OPERATE_DATE_Start: 新 API 缺少该字段
- Result_Data.List[3].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[3].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[3].SHOPTRADES: 新 API 缺少该字段
- Result_Data.List[3].BUSINESS_DATE: 值不一致 ('2021-01-30T00:00:00' vs '2021/1/30 0:00:00')
- Result_Data.List[4].OPERATE_DATE_End: 新 API 缺少该字段

原 API 状态: `200`，耗时 `162.52 ms`
新 API 状态: `200`，耗时 `64.52 ms`

### BaseInfo/GetSPRegionShopTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSPRegionShopTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSPRegionShopTree |
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
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].node.children[0].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[0].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[1].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[1].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[2].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[2].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[3].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[3].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[4].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[4].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[5].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[5].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[6].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[6].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[7].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[7].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[8].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[8].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[9].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[9].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[10].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[10].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[11].desc: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[11].ico: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.children[12].desc: 新 API 缺少该字段

原 API 状态: `200`，耗时 `133.0 ms`
新 API 状态: `200`，耗时 `11.74 ms`

### BaseInfo/GetServerPartShopNewDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"serverPartShopId": 3080}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerPartShopNewDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerPartShopNewDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 成功 vs 成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['RtServerPartShopList', 'ServerPartShop', 'ShopBusinessStateList'] vs ['RtServerPartShopList', 'ServerPartShop', 'ShopBusinessStateList'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.RtServerPartShopList[0].BusinessDate: 值不一致 ('2022年8月8日' vs '2022/8/8 0:00:00')
- Result_Data.RtServerPartShopList[1].BusinessDate: 值不一致 ('2022年7月20日' vs '2022/7/20 0:00:00')
- Result_Data.RtServerPartShopList[1].BusinessEndDate: 值不一致 ('2022年7月21日' vs '2022/7/20 0:00:00')
- Result_Data.RtServerPartShopList[2].BusinessDate: 值不一致 ('2022年5月1日' vs '2022/5/1 0:00:00')
- Result_Data.RtServerPartShopList[2].BusinessEndDate: 值不一致 ('2022年7月7日' vs '2022/7/6 0:00:00')
- Result_Data.RtServerPartShopList[3].BusinessDate: 值不一致 ('2022年7月8日' vs '2022/7/8 0:00:00')
- Result_Data.RtServerPartShopList[3].BusinessEndDate: 值不一致 ('2022年7月6日' vs '2022/7/5 0:00:00')
- Result_Data.RtServerPartShopList[4].BusinessDate: 值不一致 ('2022年4月28日' vs '2022/4/28 0:00:00')
- Result_Data.RtServerPartShopList[4].BusinessEndDate: 值不一致 ('2022年4月30日' vs '2022/4/29 0:00:00')
- Result_Data.RtServerPartShopList[5].BusinessDate: 值不一致 ('2022年4月12日' vs '2022/4/12 0:00:00')
- Result_Data.RtServerPartShopList[5].BusinessEndDate: 值不一致 ('2022年4月28日' vs '2022/4/27 0:00:00')
- Result_Data.RtServerPartShopList[6].BusinessEndDate: 值不一致 ('2022年4月13日' vs '2022/4/12 0:00:00')
- Result_Data.RtServerPartShopList[7].BusinessDate: 值不一致 ('2022年9月16日' vs '2022/9/16 0:00:00')
- Result_Data.RtServerPartShopList[8].BusinessDate: 值不一致 ('2022年5月1日' vs '2022/5/1 0:00:00')
- Result_Data.RtServerPartShopList[8].BusinessEndDate: 值不一致 ('2022年9月15日' vs '2022/9/14 0:00:00')
- Result_Data.RtServerPartShopList[9].BusinessDate: 值不一致 ('2022年4月28日' vs '2022/4/28 0:00:00')
- Result_Data.RtServerPartShopList[9].BusinessEndDate: 值不一致 ('2022年4月30日' vs '2022/4/29 0:00:00')
- Result_Data.RtServerPartShopList[10].BusinessDate: 值不一致 ('2022年4月12日' vs '2022/4/12 0:00:00')
- Result_Data.RtServerPartShopList[10].BusinessEndDate: 值不一致 ('2022年4月28日' vs '2022/4/27 0:00:00')
- Result_Data.RtServerPartShopList[11].BusinessEndDate: 值不一致 ('2022年4月13日' vs '2022/4/12 0:00:00')
- Result_Data.ServerPartShop.PROVINCE_CODE: 新 API 缺少该字段
- Result_Data.ServerPartShop.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.ServerPartShop.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.ServerPartShop.COMMISSION_TYPE: 新 API 多出该字段
- Result_Data.ServerPartShop.BANK_ACCOUNT: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `205.83 ms`
新 API 状态: `200`，耗时 `76.32 ms`

### BaseInfo/GetServerPartShopNewList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"provinceCode": "340000", "serverPartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerPartShopNewList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerPartShopNewList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 成功 vs 成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 29 vs 38 |
| PageIndex | ❌ | 1 vs 0 |
| PageSize | ❌ | 10 vs 0 |
| List 条数 | ❌ | 29 vs 38 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESS_BRAND', 'BUSINESS_DATE', 'BUSINESS_TRADE', 'BUS_STARTDATE', 'LINKMAN', 'LINKMAN_MOBILE', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'SELLER_ID'] | 仅新 API: ['EXPRESSWAY_NAME', 'FIELDENUM_ID', 'REGIONTYPE_ID', 'REGISTERCOMPACT_NAME', 'SERVERPART_ADDRESS', 'SERVERPART_INDEX', 'SERVERPART_TYPE', 'SERVERPART_X', 'SERVERPART_Y', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_INDEX', 'SPREGIONTYPE_NAME', 'TRANSFER_TYPE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (29 vs 38)
- Result_Data.List[0].BUSINESS_BRAND: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_DATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADE: 新 API 缺少该字段
- Result_Data.List[0].BUS_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].LINKMAN: 新 API 缺少该字段
- Result_Data.List[0].LINKMAN_MOBILE: 新 API 缺少该字段
- Result_Data.List[0].OPERATE_DATE: 新 API 缺少该字段
- Result_Data.List[0].OWNERUNIT_ID: 新 API 缺少该字段
- Result_Data.List[0].OWNERUNIT_NAME: 新 API 缺少该字段
- Result_Data.List[0].SELLER_ID: 新 API 缺少该字段
- Result_Data.List[0].EXPRESSWAY_NAME: 新 API 多出该字段
- Result_Data.List[0].FIELDENUM_ID: 新 API 多出该字段
- Result_Data.List[0].REGIONTYPE_ID: 新 API 多出该字段
- Result_Data.List[0].REGISTERCOMPACT_NAME: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_ADDRESS: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_INDEX: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_X: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_Y: 新 API 多出该字段
- Result_Data.List[0].SPREGIONTYPE_ID: 新 API 多出该字段
- Result_Data.List[0].SPREGIONTYPE_INDEX: 新 API 多出该字段
- Result_Data.List[0].SPREGIONTYPE_NAME: 新 API 多出该字段
- Result_Data.List[0].TRANSFER_TYPE: 新 API 多出该字段
- Result_Data.List[0].BRAND_NAME: 值不一致 ('自营客房' vs '加油站便利店')

原 API 状态: `200`，耗时 `248.0 ms`
新 API 状态: `200`，耗时 `29.8 ms`

### BaseInfo/GetServerpartDDL / service-area-416

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartType": "1000", "StatisticsType": "1000"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartDDL | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartDDL |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 142 vs 142 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 142 vs 142 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `340.31 ms`
新 API 状态: `200`，耗时 `22.19 ms`

### BaseInfo/GetServerpartShopDDL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartShopDDL | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartShopDDL |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 54 vs 54 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 54 vs 54 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `141.95 ms`
新 API 状态: `200`，耗时 `11.1 ms`

### BaseInfo/GetServerpartShopDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartShopId": 3080}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartShopDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartShopDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['APPROVAL_TYPE', 'AUDIT_UPLOADSTATE', 'BANK_ACCOUNT', 'BANK_NAME', 'BRAND_NAME', 'BUSINESSAREA', 'BUSINESS_BRAND', 'BUSINESS_DATE', 'BUSINESS_ENDDATE', 'BUSINESS_NATURE', 'BUSINESS_REGION', 'BUSINESS_STATE', 'BUSINESS_TRADE', 'BUSINESS_TRADENAME', 'BUSINESS_TYPE', 'BUSINESS_UNIT', 'BUS_STARTDATE', 'INSALES_TYPE', 'ISVALID', 'LINKMAN', 'LINKMAN_MOBILE', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PROVINCE_CODE', 'RECORD_DISCOUNT', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_NAME', 'REVENUE_INCLUDE', 'REVENUE_UPLOADSTATE', 'ROYALTYRATE', 'SALEAMOUNT_LIMIT', 'SALECOUNT_LIMIT', 'SELLER_ID', 'SELLER_NAME', 'SERVERPARTSHOP_DESC', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SERVERPARTSHOP_INDEX', 'SERVERPART_CODE', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLINGACCOUNTS', 'SHOPCODE', 'SHOPNAME', 'SHOPREGION', 'SHOPSHORTNAME', 'SHOPTRADE', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_TYPE', 'STATISTIC_TYPE', 'STOREHOUSE_TYPE', 'TAXPAYER_IDENTIFYCODE', 'TOPPERSON', 'TOPPERSON_MOBILE', 'TRANSFER_TYPE', 'UNIFORMMANAGE_TYPE'] vs ['APPROVAL_TYPE', 'AUDIT_UPLOADSTATE', 'BRAND_NAME', 'BUSINESSAREA', 'BUSINESS_BRAND', 'BUSINESS_DATE', 'BUSINESS_ENDDATE', 'BUSINESS_NATURE', 'BUSINESS_REGION', 'BUSINESS_STATE', 'BUSINESS_TRADE', 'BUSINESS_TRADENAME', 'BUSINESS_TYPE', 'BUSINESS_UNIT', 'BUS_STARTDATE', 'COMMISSION_TYPE', 'INSALES_TYPE', 'ISVALID', 'LINKMAN', 'LINKMAN_MOBILE', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'RECORD_DISCOUNT', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_NAME', 'REVENUE_INCLUDE', 'REVENUE_UPLOADSTATE', 'ROYALTYRATE', 'SALEAMOUNT_LIMIT', 'SALECOUNT_LIMIT', 'SELLER_ID', 'SELLER_NAME', 'SERVERPARTSHOP_DESC', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_INDEX', 'SERVERPART_CODE', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLINGACCOUNTS', 'SHOPCODE', 'SHOPNAME', 'SHOPREGION', 'SHOPSHORTNAME', 'SHOPTRADE', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_TYPE', 'STATISTIC_TYPE', 'STOREHOUSE_TYPE', 'TOPPERSON', 'TOPPERSON_MOBILE', 'TRANSFER_TYPE', 'UNIFORMMANAGE_TYPE'] |
| 完整响应体 | ❌ | 发现 13 处差异 |

差异明细：
- Result_Data.BANK_ACCOUNT: 新 API 缺少该字段
- Result_Data.BANK_NAME: 新 API 缺少该字段
- Result_Data.PROVINCE_CODE: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.TAXPAYER_IDENTIFYCODE: 新 API 缺少该字段
- Result_Data.COMMISSION_TYPE: 新 API 多出该字段
- Result_Data.BUS_STARTDATE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.LINKMAN: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.LINKMAN_MOBILE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.OPERATE_DATE: 值不一致 ('2022-09-17T23:01:48' vs '2022/9/17 23:01:48')
- Result_Data.REGISTERCOMPACT_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.SERVERPARTSHOP_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `172.22 ms`
新 API 状态: `200`，耗时 `12.9 ms`

### BaseInfo/GetServerpartShopInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartCode": "1", "ShopCode": "1"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartShopInfo | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartShopInfo |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['Business_BrandIcon', 'Business_BrandName', 'Business_State', 'Business_TradeName', 'Business_Type', 'InSalesType', 'OwnerUnit_Id', 'OwnerUnit_Name', 'ServerpartShopId', 'ServerpartShop_Code', 'ServerpartShop_Name', 'ServerpartShop_Region', 'ServerpartShop_ShortName', 'ServerpartShop_State', 'ServerpartShop_Trade', 'Serverpart_Code', 'Serverpart_Id', 'Serverpart_Name', 'Transfer_Type'] vs [] |
| 完整响应体 | ❌ | 发现 19 处差异 |

差异明细：
- Result_Data.Business_BrandIcon: 新 API 缺少该字段
- Result_Data.Business_BrandName: 新 API 缺少该字段
- Result_Data.Business_State: 新 API 缺少该字段
- Result_Data.Business_TradeName: 新 API 缺少该字段
- Result_Data.Business_Type: 新 API 缺少该字段
- Result_Data.InSalesType: 新 API 缺少该字段
- Result_Data.OwnerUnit_Id: 新 API 缺少该字段
- Result_Data.OwnerUnit_Name: 新 API 缺少该字段
- Result_Data.ServerpartShopId: 新 API 缺少该字段
- Result_Data.ServerpartShop_Code: 新 API 缺少该字段
- Result_Data.ServerpartShop_Name: 新 API 缺少该字段
- Result_Data.ServerpartShop_Region: 新 API 缺少该字段
- Result_Data.ServerpartShop_ShortName: 新 API 缺少该字段
- Result_Data.ServerpartShop_State: 新 API 缺少该字段
- Result_Data.ServerpartShop_Trade: 新 API 缺少该字段
- Result_Data.Serverpart_Code: 新 API 缺少该字段
- Result_Data.Serverpart_Id: 新 API 缺少该字段
- Result_Data.Serverpart_Name: 新 API 缺少该字段
- Result_Data.Transfer_Type: 新 API 缺少该字段

原 API 状态: `200`，耗时 `173.27 ms`
新 API 状态: `200`，耗时 `9.93 ms`

### BaseInfo/GetServerpartShopList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"SERVERPART_IDS": 416}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartShopList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartShopList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 69 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 999 vs 999 |
| List 条数 | ❌ | 69 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (69 vs 0)
- Result_Data.TotalCount: 值不一致 (69 vs 0)

原 API 状态: `200`，耗时 `192.01 ms`
新 API 状态: `200`，耗时 `89.21 ms`

### BaseInfo/GetServerpartShopTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartShopTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartShopTree |
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
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].node.children[0].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[0].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[1].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[1].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[2].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[2].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[3].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[3].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[4].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[4].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[5].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[5].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[6].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[6].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[7].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[7].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[8].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[8].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[9].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[9].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[10].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[10].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[11].desc: 新 API 缺少该字段
- Result_Data.List[0].node.children[11].ico: 新 API 缺少该字段
- Result_Data.List[0].node.children[12].desc: 新 API 缺少该字段

原 API 状态: `200`，耗时 `150.41 ms`
新 API 状态: `200`，耗时 `11.39 ms`

### BaseInfo/GetServerpartTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartType": "1000", "StatisticsType": "1000"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartTree |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 7 vs 7 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 7 vs 7 |
| 首条字段集合 | ✅ | 字段一致，共 7 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `252.96 ms`
新 API 状态: `200`，耗时 `32.49 ms`

### BaseInfo/GetServerpartUDTypeTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartUDTypeTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartUDTypeTree |
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
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].children: 列表长度不一致 (99 vs 114)
- Result_Data.List[0].children[0].children[0].node.key: 值不一致 ('2-9475' vs '2-1019')
- Result_Data.List[0].children[0].children[0].node.label: 值不一致 ('【361度】衣服' vs '新桥服务区')
- Result_Data.List[0].children[0].children[0].node.value: 值不一致 (9475 vs 1019)
- Result_Data.List[0].children[0].children[1].node.key: 值不一致 ('2-9476' vs '2-1021')
- Result_Data.List[0].children[0].children[1].node.label: 值不一致 ('【361度】裤子' vs '猫屎咖啡')
- Result_Data.List[0].children[0].children[1].node.value: 值不一致 (9476 vs 1021)
- Result_Data.List[0].children[0].children[2].node.key: 值不一致 ('2-9477' vs '2-1022')
- Result_Data.List[0].children[0].children[2].node.label: 值不一致 ('【361度】鞋子' vs '精品咖啡')
- Result_Data.List[0].children[0].children[2].node.value: 值不一致 (9477 vs 1022)
- Result_Data.List[0].children[0].children[3].node.key: 值不一致 ('2-9478' vs '2-1023')
- Result_Data.List[0].children[0].children[3].node.label: 值不一致 ('【361度】饰品' vs '经典咖啡')
- Result_Data.List[0].children[0].children[3].node.value: 值不一致 (9478 vs 1023)
- Result_Data.List[0].children[0].children[4].node.key: 值不一致 ('2-175' vs '2-1024')
- Result_Data.List[0].children[0].children[4].node.label: 值不一致 ('【刘鸿盛小吃】包子系列' vs '冰雪乐咖啡')
- Result_Data.List[0].children[0].children[4].node.value: 值不一致 (175 vs 1024)
- Result_Data.List[0].children[0].children[5].node.key: 值不一致 ('2-176' vs '2-1025')
- Result_Data.List[0].children[0].children[5].node.label: 值不一致 ('【刘鸿盛小吃】汤包系列' vs '茶和其他')
- Result_Data.List[0].children[0].children[5].node.value: 值不一致 (176 vs 1025)
- Result_Data.List[0].children[0].children[6].node.key: 值不一致 ('2-177' vs '2-1026')
- Result_Data.List[0].children[0].children[6].node.label: 值不一致 ('【刘鸿盛小吃】蒸饺系列' vs '气泡水')
- Result_Data.List[0].children[0].children[6].node.value: 值不一致 (177 vs 1026)
- Result_Data.List[0].children[0].children[7].node.key: 值不一致 ('2-178' vs '2-1027')
- Result_Data.List[0].children[0].children[7].node.label: 值不一致 ('【刘鸿盛小吃】油炸系列' vs '冰淇淋')
- Result_Data.List[0].children[0].children[7].node.value: 值不一致 (178 vs 1027)

原 API 状态: `200`，耗时 `161.21 ms`
新 API 状态: `200`，耗时 `42.51 ms`

### BaseInfo/GetShopReceivables / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetShopReceivables | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetShopReceivables |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 31 vs 31 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 31 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ✅ | 31 vs 31 |
| 首条字段集合 | ✅ | 字段一致，共 39 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[3].SERVERPARTSHOP_ID: 值不一致 ('7105,7104' vs '7104,7105')
- Result_Data.List[4].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_15_57_42_9497.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_15_57_42_9497.png')
- Result_Data.List[4].SERVERPARTSHOP_ID: 值不一致 ('3063,3062' vs '3062,3063')
- Result_Data.List[5].SERVERPARTSHOP_ID: 值不一致 ('1991,1990' vs '1990,1991')
- Result_Data.List[6].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_12_03_53_4354.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_12_03_53_4354.png')
- Result_Data.List[6].SERVERPARTSHOP_ID: 值不一致 ('3047,3046' vs '3046,3047')
- Result_Data.List[11].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_15_41_35_3219.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_15_41_35_3219.png')
- Result_Data.List[12].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2020_04_08_11_51_47_0248.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2020_04_08_11_51_47_0248.png')
- Result_Data.List[14].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_15_29_22_5453.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_15_29_22_5453.png')
- Result_Data.List[14].SERVERPARTSHOP_ID: 值不一致 ('3067,3066' vs '3066,3067')
- Result_Data.List[16].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_15_41_35_3219.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_15_41_35_3219.png')
- Result_Data.List[16].SERVERPARTSHOP_ID: 值不一致 ('3057,3056' vs '3056,3057')
- Result_Data.List[17].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2020_04_08_11_57_05_8062.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2020_04_08_11_57_05_8062.png')
- Result_Data.List[17].SERVERPARTSHOP_ID: 值不一致 ('3065,3064' vs '3064,3065')
- Result_Data.List[18].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_15_48_05_8374.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_15_48_05_8374.png')
- Result_Data.List[19].BUSINESSPROJECT_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/PictureManage/10292/2021_02_03_15_44_45_0421.png' vs 'https://api.eshangtech.com/EShangApiMain/UploadImageDir/PictureManage/10292/2021_02_03_15_44_45_0421.png')
- Result_Data.List[19].SERVERPARTSHOP_ID: 值不一致 ('3059,3058' vs '3058,3059')
- Result_Data.List[22].COMPACT_NAME: 值不一致 ('安徽易加能数字科技有限公司' vs '扶贫项目')
- Result_Data.List[22].COOPMERCHANTS_NAME: 值不一致 ('安徽易加能数字科技有限公司' vs '安徽菜大师农业控股集团有限公司')
- Result_Data.List[22].REGISTERCOMPACT_ID: 值不一致 ('795' vs '173')
- Result_Data.List[23].COMPACT_NAME: 值不一致 ('扶贫项目' vs '安徽易加能数字科技有限公司')
- Result_Data.List[23].COOPMERCHANTS_NAME: 值不一致 ('安徽菜大师农业控股集团有限公司' vs '安徽易加能数字科技有限公司')
- Result_Data.List[23].REGISTERCOMPACT_ID: 值不一致 ('173' vs '795')
- Result_Data.List[24].BUSINESSPROJECT_ID: 值不一致 (947 vs 1090)
- Result_Data.List[24].BUSINESSPROJECT_NAME: 值不一致 ('合肥蔚电科技有限公司' vs '广东省绿行医疗科技有限公司')

原 API 状态: `200`，耗时 `572.91 ms`
新 API 状态: `200`，耗时 `334.92 ms`

### BaseInfo/GetShopShortNames / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416, "ShopValid": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetShopShortNames | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetShopShortNames |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 5 vs 5 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 5 vs 5 |
| 首条字段集合 | ✅ | 首项不是对象列表，跳过字段扫描 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `120.06 ms`
新 API 状态: `200`，耗时 `11.0 ms`

### BaseInfo/GetTradeBrandTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BrandState": 1, "BusinessTrade_PID": -1, "ProvinceCode": "340000"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetTradeBrandTree | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetTradeBrandTree |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 6 vs 6 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 6 vs 6 |
| List 条数 | ✅ | 6 vs 6 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].children: 类型不一致 (NoneType vs list)，值为 None vs []
- Result_Data.List[0].children[0].node.BrandTreeList[0].Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].Brand_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].Brand_Name: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].Brand_Type: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].BRAND_ID: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].BRAND_INTRO: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].BRAND_NAME: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[0].BRAND_STATE: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].Brand_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].Brand_Name: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].Brand_Type: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].BRAND_ID: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].BRAND_INTRO: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].BRAND_NAME: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[1].BRAND_STATE: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].Brand_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].Brand_Name: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].Brand_Type: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].BRAND_ID: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].BRAND_INTRO: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].BRAND_NAME: 新 API 多出该字段
- Result_Data.List[0].children[0].node.BrandTreeList[2].BRAND_STATE: 新 API 多出该字段

原 API 状态: `200`，耗时 `342.39 ms`
新 API 状态: `200`，耗时 `108.85 ms`

### BaseInfo/GetUSERDEFINEDTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"USERDEFINEDTYPEId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetUSERDEFINEDTYPEDetail | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetUSERDEFINEDTYPEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BUSINESSTYPE', 'OPERATE_DATE', 'SCANCODE_ORDER', 'SERVERPARTCODE', 'SERVERPARTCODES', 'SERVERPARTSHOP_ID', 'SERVERPART_ID', 'STAFF_ID', 'STAFF_NAME', 'ShopNames', 'USERDEFINEDTYPE_DATE', 'USERDEFINEDTYPE_DESC', 'USERDEFINEDTYPE_ID', 'USERDEFINEDTYPE_INDEX', 'USERDEFINEDTYPE_NAME', 'USERDEFINEDTYPE_PID', 'USERDEFINEDTYPE_STATE'] vs ['BUSINESSTYPE', 'GOODSTYPE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'OPERATE_DATE', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PRESALE_ENDTIME', 'PRESALE_STARTTIME', 'PRESALE_TYPE', 'PROVINCE_CODE', 'SCANCODE_ORDER', 'SERVERPARTCODE', 'SERVERPARTSHOP_ID', 'SERVERPART_ID', 'SERVERPART_NAME', 'SHOPCODE', 'SHOPNAME', 'STAFF_ID', 'STAFF_NAME', 'USERDEFINEDTYPE_DATE', 'USERDEFINEDTYPE_DESC', 'USERDEFINEDTYPE_ICO', 'USERDEFINEDTYPE_ID', 'USERDEFINEDTYPE_INDEX', 'USERDEFINEDTYPE_NAME', 'USERDEFINEDTYPE_PID', 'USERDEFINEDTYPE_STATE', 'WECHATAPPSIGN_ID', 'WECHATAPPSIGN_NAME', 'WECHATAPP_APPID'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.SERVERPARTCODES: 新 API 缺少该字段
- Result_Data.ShopNames: 新 API 缺少该字段
- Result_Data.GOODSTYPE: 新 API 多出该字段
- Result_Data.MERCHANTS_ID: 新 API 多出该字段
- Result_Data.MERCHANTS_NAME: 新 API 多出该字段
- Result_Data.OWNERUNIT_ID: 新 API 多出该字段
- Result_Data.OWNERUNIT_NAME: 新 API 多出该字段
- Result_Data.PRESALE_ENDTIME: 新 API 多出该字段
- Result_Data.PRESALE_STARTTIME: 新 API 多出该字段
- Result_Data.PRESALE_TYPE: 新 API 多出该字段
- Result_Data.PROVINCE_CODE: 新 API 多出该字段
- Result_Data.SERVERPART_NAME: 新 API 多出该字段
- Result_Data.SHOPCODE: 新 API 多出该字段
- Result_Data.SHOPNAME: 新 API 多出该字段
- Result_Data.USERDEFINEDTYPE_ICO: 新 API 多出该字段
- Result_Data.WECHATAPPSIGN_ID: 新 API 多出该字段
- Result_Data.WECHATAPPSIGN_NAME: 新 API 多出该字段
- Result_Data.WECHATAPP_APPID: 新 API 多出该字段
- Result_Data.BUSINESSTYPE: 类型不一致 (int vs NoneType)，值为 3000 vs None
- Result_Data.OPERATE_DATE: 值不一致 ('2018/11/20 16:14:29' vs '2019/9/30 16:00:24')
- Result_Data.SCANCODE_ORDER: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.SERVERPARTCODE: 值不一致 ('620036' vs '888888')
- Result_Data.SERVERPARTSHOP_ID: 类型不一致 (int vs str)，值为 87 vs '1212,882'
- Result_Data.SERVERPART_ID: 类型不一致 (int vs str)，值为 42 vs '3748'
- Result_Data.STAFF_ID: 值不一致 (2 vs 1)

原 API 状态: `200`，耗时 `126.4 ms`
新 API 状态: `200`，耗时 `12.49 ms`

### BaseInfo/GetUSERDEFINEDTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"USERDEFINEDTYPE_ID": 40}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetUSERDEFINEDTYPEList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetUSERDEFINEDTYPEList |
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
| 首条字段集合 | ❌ | 仅原 API: ['SERVERPARTCODES', 'ShopNames'] | 仅新 API: ['GOODSTYPE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'OWNERUNIT_ID', 'OWNERUNIT_NAME', 'PRESALE_ENDTIME', 'PRESALE_STARTTIME', 'PRESALE_TYPE', 'PROVINCE_CODE', 'SERVERPART_NAME', 'SHOPCODE', 'SHOPNAME', 'USERDEFINEDTYPE_ICO', 'WECHATAPPSIGN_ID', 'WECHATAPPSIGN_NAME', 'WECHATAPP_APPID'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].SERVERPARTCODES: 新 API 缺少该字段
- Result_Data.List[0].ShopNames: 新 API 缺少该字段
- Result_Data.List[0].GOODSTYPE: 新 API 多出该字段
- Result_Data.List[0].MERCHANTS_ID: 新 API 多出该字段
- Result_Data.List[0].MERCHANTS_NAME: 新 API 多出该字段
- Result_Data.List[0].OWNERUNIT_ID: 新 API 多出该字段
- Result_Data.List[0].OWNERUNIT_NAME: 新 API 多出该字段
- Result_Data.List[0].PRESALE_ENDTIME: 新 API 多出该字段
- Result_Data.List[0].PRESALE_STARTTIME: 新 API 多出该字段
- Result_Data.List[0].PRESALE_TYPE: 新 API 多出该字段
- Result_Data.List[0].PROVINCE_CODE: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_NAME: 新 API 多出该字段
- Result_Data.List[0].SHOPCODE: 新 API 多出该字段
- Result_Data.List[0].SHOPNAME: 新 API 多出该字段
- Result_Data.List[0].USERDEFINEDTYPE_ICO: 新 API 多出该字段
- Result_Data.List[0].WECHATAPPSIGN_ID: 新 API 多出该字段
- Result_Data.List[0].WECHATAPPSIGN_NAME: 新 API 多出该字段
- Result_Data.List[0].WECHATAPP_APPID: 新 API 多出该字段
- Result_Data.List[0].BUSINESSTYPE: 类型不一致 (int vs NoneType)，值为 2000 vs None
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2020/4/28 13:41:05' vs '2019/6/23 17:54:27')
- Result_Data.List[0].SERVERPARTCODE: 值不一致 ('141010' vs '331010')
- Result_Data.List[0].SERVERPARTSHOP_ID: 类型不一致 (NoneType vs str)，值为 None vs '3132,3133'
- Result_Data.List[0].SERVERPART_ID: 类型不一致 (int vs str)，值为 127 vs '104'
- Result_Data.List[0].STAFF_ID: 值不一致 (268 vs 1835)
- Result_Data.List[0].STAFF_NAME: 值不一致 ('山西管理账号' vs '中餐公司')

原 API 状态: `200`，耗时 `110.35 ms`
新 API 状态: `200`，耗时 `15.49 ms`

### Commodity/GetCOMMODITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYId": 13232}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Commodity/GetCOMMODITYDetail | 新 API: http://localhost:8080/EShangApiMain/Commodity/GetCOMMODITYDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ADDTIME', 'BUSINESSAPPROVAL_ID', 'BUSINESSTYPE', 'CANSALE', 'COMMODITY_ALLNAME', 'COMMODITY_BARCODE', 'COMMODITY_BRAND', 'COMMODITY_CODE', 'COMMODITY_COUNT', 'COMMODITY_CURRPRICE', 'COMMODITY_DESC', 'COMMODITY_EN', 'COMMODITY_FROZENCOUNT', 'COMMODITY_GRADE', 'COMMODITY_GROUPPRICE', 'COMMODITY_HOTKEY', 'COMMODITY_ID', 'COMMODITY_MAXPRICE', 'COMMODITY_MEMBERPRICE', 'COMMODITY_MINPRICE', 'COMMODITY_NAME', 'COMMODITY_ORI', 'COMMODITY_ORIPRICE', 'COMMODITY_PROMOTIONPRICE', 'COMMODITY_PURCHASEPRICE', 'COMMODITY_RETAILPRICE', 'COMMODITY_RULE', 'COMMODITY_SERVERCODE', 'COMMODITY_STATE', 'COMMODITY_SYMBOL', 'COMMODITY_TYPE', 'COMMODITY_UNIFORMPRICE', 'COMMODITY_UNIT', 'DUTY_PARAGRAPH', 'ISBULK', 'METERINGMETHOD', 'OPERATE_DATE', 'PROVINCE_CODE', 'RETAIL_DUTY', 'SERVERPART_ID', 'SUPPLIER_ID', 'USERDEFINEDTYPE_ID'] vs [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.ADDTIME: 新 API 缺少该字段
- Result_Data.BUSINESSAPPROVAL_ID: 新 API 缺少该字段
- Result_Data.BUSINESSTYPE: 新 API 缺少该字段
- Result_Data.CANSALE: 新 API 缺少该字段
- Result_Data.COMMODITY_ALLNAME: 新 API 缺少该字段
- Result_Data.COMMODITY_BARCODE: 新 API 缺少该字段
- Result_Data.COMMODITY_BRAND: 新 API 缺少该字段
- Result_Data.COMMODITY_CODE: 新 API 缺少该字段
- Result_Data.COMMODITY_COUNT: 新 API 缺少该字段
- Result_Data.COMMODITY_CURRPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_DESC: 新 API 缺少该字段
- Result_Data.COMMODITY_EN: 新 API 缺少该字段
- Result_Data.COMMODITY_FROZENCOUNT: 新 API 缺少该字段
- Result_Data.COMMODITY_GRADE: 新 API 缺少该字段
- Result_Data.COMMODITY_GROUPPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_HOTKEY: 新 API 缺少该字段
- Result_Data.COMMODITY_ID: 新 API 缺少该字段
- Result_Data.COMMODITY_MAXPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_MEMBERPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_MINPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_NAME: 新 API 缺少该字段
- Result_Data.COMMODITY_ORI: 新 API 缺少该字段
- Result_Data.COMMODITY_ORIPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_PROMOTIONPRICE: 新 API 缺少该字段
- Result_Data.COMMODITY_PURCHASEPRICE: 新 API 缺少该字段

原 API 状态: `200`，耗时 `139.55 ms`
新 API 状态: `200`，耗时 `28.31 ms`

### Commodity/GetCOMMODITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Commodity/GetCOMMODITYList | 新 API: http://localhost:8080/EShangApiMain/Commodity/GetCOMMODITYList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1614 vs 1614 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 42 个 |
| 完整响应体 | ❌ | 发现 9 处差异 |

差异明细：
- Result_Data.List[0].ADDTIME: 值不一致 ('2024-01-30T17:10:54' vs '2024/1/30 17:10:54')
- Result_Data.List[1].ADDTIME: 值不一致 ('2021-01-30T19:24:37' vs '2021/1/30 19:24:37')
- Result_Data.List[2].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')
- Result_Data.List[3].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')
- Result_Data.List[4].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')
- Result_Data.List[5].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')
- Result_Data.List[6].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')
- Result_Data.List[7].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')
- Result_Data.List[8].ADDTIME: 值不一致 ('2021-01-30T09:45:38' vs '2021/1/30 9:45:38')

原 API 状态: `200`，耗时 `487.03 ms`
新 API 状态: `200`，耗时 `23.87 ms`

### Commodity/GetCommodityList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "SearchType": 1, "ServerpartID": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Commodity/GetCommodityList | 新 API: http://localhost:8080/EShangApiMain/Commodity/GetCommodityList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1614 vs 1614 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 10 vs 10 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSTYPE_NAME'] | 仅新 API: ['BUSINESSTYPE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[0].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[1].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[1].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[1].COMMODITY_TYPE: 值不一致 ('锅盔' vs '906')
- Result_Data.List[2].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[2].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[2].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[3].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[3].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[3].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[4].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[4].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[4].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[5].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[5].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[5].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[6].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[6].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[6].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[7].BUSINESSTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[7].BUSINESSTYPE: 新 API 多出该字段
- Result_Data.List[7].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[8].BUSINESSTYPE_NAME: 新 API 缺少该字段

原 API 状态: `200`，耗时 `271.91 ms`
新 API 状态: `200`，耗时 `19.82 ms`

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

原 API 状态: `200`，耗时 `121.78 ms`
新 API 状态: `200`，耗时 `25.21 ms`

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

原 API 状态: `200`，耗时 `101.58 ms`
新 API 状态: `200`，耗时 `60.23 ms`

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

原 API 状态: `200`，耗时 `90.77 ms`
新 API 状态: `200`，耗时 `19.19 ms`

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

原 API 状态: `200`，耗时 `102.7 ms`
新 API 状态: `200`，耗时 `37.82 ms`

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

原 API 状态: `200`，耗时 `101.39 ms`
新 API 状态: `200`，耗时 `9.68 ms`

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

原 API 状态: `404`，耗时 `3.32 ms`
新 API 状态: `200`，耗时 `2.28 ms`

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

原 API 状态: `415`，耗时 `3.33 ms`
新 API 状态: `200`，耗时 `9.7 ms`

### BusinessProject/GetAPPROVEDList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"APPROVED_ID": 5419}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetAPPROVEDList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetAPPROVEDList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 999 vs 999 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ❌ | 仅原 API: ['APPROVED_DATE_End', 'APPROVED_DATE_Start', 'APPROVED_TYPES', 'TABLE_IDS'] | 仅新 API: ['CONTRACTPROINST_ID'] |
| 完整响应体 | ❌ | 发现 6 处差异 |

差异明细：
- Result_Data.List[0].APPROVED_DATE_End: 新 API 缺少该字段
- Result_Data.List[0].APPROVED_DATE_Start: 新 API 缺少该字段
- Result_Data.List[0].APPROVED_TYPES: 新 API 缺少该字段
- Result_Data.List[0].TABLE_IDS: 新 API 缺少该字段
- Result_Data.List[0].CONTRACTPROINST_ID: 新 API 多出该字段
- Result_Data.List[0].APPROVED_DATE: 类型不一致 (str vs float)，值为 '2024/07/22 09:31:00' vs 20240722093100.0

原 API 状态: `200`，耗时 `101.06 ms`
新 API 状态: `200`，耗时 `33.19 ms`

### BusinessProject/GetAccountWarningList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetAccountWarningList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetAccountWarningList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 9 vs 9 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 9 vs 10 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESS_ENDDATE', 'BUSINESS_STARTDATE', 'BUSINESS_TRADE', 'Brand_ICO', 'CA_COST', 'GUARANTEERATIO', 'MERCHANTS_ID_Encrypted', 'PROFIT_AVG', 'PROFIT_RATE', 'PROFIT_SD', 'PaymentProgress', 'ProjectProgress', 'ROYALTY_PRICE', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_NAME', 'SUBROYALTY_THEORY', 'TICKET_COUNT'] | 仅新 API: ['ACCOUNTWARNING_ID', 'RECORD_DATE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESS_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADE: 新 API 缺少该字段
- Result_Data.List[0].Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].CA_COST: 新 API 缺少该字段
- Result_Data.List[0].GUARANTEERATIO: 新 API 缺少该字段
- Result_Data.List[0].MERCHANTS_ID_Encrypted: 新 API 缺少该字段
- Result_Data.List[0].PROFIT_AVG: 新 API 缺少该字段
- Result_Data.List[0].PROFIT_RATE: 新 API 缺少该字段
- Result_Data.List[0].PROFIT_SD: 新 API 缺少该字段
- Result_Data.List[0].PaymentProgress: 新 API 缺少该字段
- Result_Data.List[0].ProjectProgress: 新 API 缺少该字段
- Result_Data.List[0].ROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].SUBROYALTY_THEORY: 新 API 缺少该字段
- Result_Data.List[0].TICKET_COUNT: 新 API 缺少该字段
- Result_Data.List[0].ACCOUNTWARNING_ID: 新 API 多出该字段
- Result_Data.List[0].RECORD_DATE: 新 API 多出该字段
- Result_Data.List[0].ACTUAL_RATIO: 类型不一致 (NoneType vs float)，值为 None vs 35.31
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (32 vs 1508)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 值不一致 ('新桥服务区（中式餐饮）项目' vs '新桥三河米饺合同项目')
- Result_Data.List[0].BUSINESS_STATE: 值不一致 (3000 vs 1000)
- Result_Data.List[0].COMMISSION_RATIO: 类型不一致 (NoneType vs float)，值为 None vs 26.0
- Result_Data.List[0].COST_AMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 697194.49

原 API 状态: `200`，耗时 `412.46 ms`
新 API 状态: `200`，耗时 `24.41 ms`

### BusinessProject/GetAccountWarningListSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetAccountWarningListSummary | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetAccountWarningListSummary |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 8 vs 8 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 8 vs 8 |
| List 条数 | ✅ | 8 vs 8 |
| 首条字段集合 | ✅ | 字段一致，共 4 个 |
| 完整响应体 | ❌ | 发现 9 处差异 |

差异明细：
- Result_Data.List[1].value: 值不一致 (103 vs 158)
- Result_Data.List[2].value: 值不一致 (5 vs 4)
- Result_Data.List[3].value: 值不一致 (35 vs 50)
- Result_Data.List[4].value: 值不一致 (8 vs 56)
- Result_Data.List[5].value: 值不一致 (54 vs 48)
- Result_Data.List[6].label: 值不一致 ('保底提成过高' vs '租金提成过高')
- Result_Data.List[6].value: 值不一致 (119 vs 101)
- Result_Data.List[7].label: 值不一致 ('业态缺失告警' vs '保底偏低预警')
- Result_Data.List[7].value: 值不一致 (40 vs 35)

原 API 状态: `200`，耗时 `206.38 ms`
新 API 状态: `200`，耗时 `21.82 ms`

### BusinessProject/GetAnnualSplit / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessProjectId": 1905, "DataType": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetAnnualSplit | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetAnnualSplit |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 8 vs 8 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 9999 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ✅ | 8 vs 8 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_NAME', 'BUSINESS_ENDDATE', 'BUSINESS_PERIOD', 'BUSINESS_STARTDATE', 'BUSINESS_STATE', 'CLOSED_DATE', 'DAILY_AMOUNT', 'EXPENSE_TYPE', 'MERCHANTS_NAME', 'MERCHANT_PAYMENT', 'OTHER_EXPENSE', 'PERIOD_INDEX', 'PROPERTY_FEE', 'WATERELECTRIC_EXPENSE'] | 仅新 API: ['ACCCASHPAY_CORRECT', 'ACCCIGARETTE_AMOUNT', 'ACCMOBILEPAY_CORRECT', 'ACCOUNT_TYPE', 'ACCREVENUE_AMOUNT', 'ACCROYALTY_PRICE', 'ACCROYALTY_THEORY', 'ACCSUBROYALTY_PRICE', 'ACCSUBROYALTY_THEORY', 'ACCTICKET_FEE', 'BIZPSPLITMONTH_ID', 'BIZPSPLITMONTH_STATE', 'BUSINESSAPPROVAL_ID', 'CASHPAY_AMOUNT', 'CASHPAY_CORRECT', 'CORRECT_AMOUNT', 'DIFFERENT_AMOUNT', 'MOBILEPAY_AMOUNT', 'MOBILEPAY_CORRECT', 'NATUREDAY', 'OTHERPAY_AMOUNT', 'RECORD_DATE', 'SMOKERATIO'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_PERIOD: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STATE: 新 API 缺少该字段
- Result_Data.List[0].CLOSED_DATE: 新 API 缺少该字段
- Result_Data.List[0].DAILY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].EXPENSE_TYPE: 新 API 缺少该字段
- Result_Data.List[0].MERCHANTS_NAME: 新 API 缺少该字段
- Result_Data.List[0].MERCHANT_PAYMENT: 新 API 缺少该字段
- Result_Data.List[0].OTHER_EXPENSE: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_INDEX: 新 API 缺少该字段
- Result_Data.List[0].PROPERTY_FEE: 新 API 缺少该字段
- Result_Data.List[0].WATERELECTRIC_EXPENSE: 新 API 缺少该字段
- Result_Data.List[0].ACCCASHPAY_CORRECT: 新 API 多出该字段
- Result_Data.List[0].ACCCIGARETTE_AMOUNT: 新 API 多出该字段
- Result_Data.List[0].ACCMOBILEPAY_CORRECT: 新 API 多出该字段
- Result_Data.List[0].ACCOUNT_TYPE: 新 API 多出该字段
- Result_Data.List[0].ACCREVENUE_AMOUNT: 新 API 多出该字段
- Result_Data.List[0].ACCROYALTY_PRICE: 新 API 多出该字段
- Result_Data.List[0].ACCROYALTY_THEORY: 新 API 多出该字段
- Result_Data.List[0].ACCSUBROYALTY_PRICE: 新 API 多出该字段
- Result_Data.List[0].ACCSUBROYALTY_THEORY: 新 API 多出该字段
- Result_Data.List[0].ACCTICKET_FEE: 新 API 多出该字段
- Result_Data.List[0].BIZPSPLITMONTH_ID: 新 API 多出该字段

原 API 状态: `200`，耗时 `731.98 ms`
新 API 状态: `200`，耗时 `51.01 ms`

### BusinessProject/GetBIZPSPLITMONTHDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BIZPSPLITMONTHId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBIZPSPLITMONTHDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBIZPSPLITMONTHDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACCCASHPAY_CORRECT', 'ACCCIGARETTE_AMOUNT', 'ACCMOBILEPAY_CORRECT', 'ACCOUNT_TYPE', 'ACCREVENUE_AMOUNT', 'ACCROYALTY_PRICE', 'ACCROYALTY_THEORY', 'ACCSUBROYALTY_PRICE', 'ACCSUBROYALTY_THEORY', 'ACCTICKET_FEE', 'Approvalstate', 'BIZPSPLITMONTH_DESC', 'BIZPSPLITMONTH_ID', 'BIZPSPLITMONTH_IDS', 'BIZPSPLITMONTH_STATE', 'BUSINESSAPPROVAL_ID', 'BUSINESSDAYS', 'BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'CASHPAY_AMOUNT', 'CASHPAY_CORRECT', 'CIGARETTE_AMOUNT', 'CORRECT_AMOUNT', 'DIFDAILY_REVENUE', 'DIFFERENT_AMOUNT', 'ENDDATE', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MINTURNOVER', 'MOBILEPAY_AMOUNT', 'MOBILEPAY_CORRECT', 'NATUREDAY', 'OTHERPAY_AMOUNT', 'RECORD_DATE', 'REGISTERCOMPACT_ID', 'REVENUEDAILY_AMOUNT', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SHOPROYALTY_ID', 'SHOPROYALTY_IDS', 'SMOKERATIO', 'STARTDATE', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'SUBROYALTY_PRICE', 'SUBROYALTY_THEORY', 'TICKET_FEE'] vs ['ACCCASHPAY_CORRECT', 'ACCCIGARETTE_AMOUNT', 'ACCMOBILEPAY_CORRECT', 'ACCOUNT_TYPE', 'ACCREVENUE_AMOUNT', 'ACCROYALTY_PRICE', 'ACCROYALTY_THEORY', 'ACCSUBROYALTY_PRICE', 'ACCSUBROYALTY_THEORY', 'ACCTICKET_FEE', 'BIZPSPLITMONTH_DESC', 'BIZPSPLITMONTH_ID', 'BIZPSPLITMONTH_STATE', 'BUSINESSAPPROVAL_ID', 'BUSINESSDAYS', 'BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'CASHPAY_AMOUNT', 'CASHPAY_CORRECT', 'CIGARETTE_AMOUNT', 'CORRECT_AMOUNT', 'DIFDAILY_REVENUE', 'DIFFERENT_AMOUNT', 'ENDDATE', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MINTURNOVER', 'MOBILEPAY_AMOUNT', 'MOBILEPAY_CORRECT', 'NATUREDAY', 'OTHERPAY_AMOUNT', 'RECORD_DATE', 'REGISTERCOMPACT_ID', 'REVENUEDAILY_AMOUNT', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SHOPROYALTY_ID', 'SMOKERATIO', 'STARTDATE', 'STATISTICS_MONTH', 'SUBROYALTY_PRICE', 'SUBROYALTY_THEORY', 'TICKET_FEE'] |
| 完整响应体 | ❌ | 发现 6 处差异 |

差异明细：
- Result_Data.Approvalstate: 新 API 缺少该字段
- Result_Data.BIZPSPLITMONTH_IDS: 新 API 缺少该字段
- Result_Data.SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.RECORD_DATE: 值不一致 ('2024-03-13T12:04:30' vs '2024/3/13 12:04:30')

原 API 状态: `200`，耗时 `214.9 ms`
新 API 状态: `200`，耗时 `17.24 ms`

### BusinessProject/GetBIZPSPLITMONTHList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"BIZPSPLITMONTH_ID": 3106}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBIZPSPLITMONTHList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBIZPSPLITMONTHList |
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
| 首条字段集合 | ❌ | 仅原 API: ['Approvalstate', 'BIZPSPLITMONTH_IDS', 'SHOPROYALTY_IDS', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 6 处差异 |

差异明细：
- Result_Data.List[0].Approvalstate: 新 API 缺少该字段
- Result_Data.List[0].BIZPSPLITMONTH_IDS: 新 API 缺少该字段
- Result_Data.List[0].SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2026-02-08T12:04:22' vs '2026/2/8 12:04:22')

原 API 状态: `200`，耗时 `104.32 ms`
新 API 状态: `200`，耗时 `11.46 ms`

### BusinessProject/GetBUSINESSPROJECTSPLITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BUSINESSPROJECTSPLITId": 87658}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBUSINESSPROJECTSPLITDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBUSINESSPROJECTSPLITDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACCOUNT_AMOUNT', 'ACCOUNT_TYPE', 'BUSINESSDAYS', 'BUSINESSPROJECTSPLIT_DESC', 'BUSINESSPROJECTSPLIT_ID', 'BUSINESSPROJECTSPLIT_STATE', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESS_TYPE', 'CASHPAY_AMOUNT', 'CIGARETTEDAILY_AMOUNT', 'CIGARETTE_AMOUNT', 'CORRECT_AMOUNT', 'CURCASHPAY_AMOUNT', 'CURMOBILEPAY_AMOUNT', 'CURROYALTY_PRICE', 'CURSUBROYALTY_PRICE', 'CURTICKET_FEE', 'CalcAccumulate', 'CalcExpiredDays', 'CompleteState', 'DATE_TYPE', 'DIFDAILY_REVENUE', 'DIFFERENT_AMOUNT', 'ENDDATE', 'ENDDATE_End', 'ENDDATE_Start', 'EXPIREDAYS', 'ExpenseAmount', 'ExpenseList', 'GUARANTEERATIO', 'LogList', 'MERCHANTS_ID', 'MINTURNOVER', 'MOBILEPAY_AMOUNT', 'NATUREDAY', 'OTHERPAY_AMOUNT', 'RECORD_DATE', 'REGISTERCOMPACT_ID', 'REVENUEDAILY_AMOUNT', 'REVENUE_AMOUNT', 'ROYALTYDAILY_PRICE', 'ROYALTYDAILY_THEORY', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLEMENT_STATE', 'SHOPEXPENSE_ID', 'SHOPROYALTY_ID', 'SMOKERATIO', 'STARTDATE', 'STARTDATE_End', 'STARTDATE_Start', 'STATISTICS_DATE', 'STATISTICS_DATE_End', 'STATISTICS_DATE_Start', 'SUBROYALTYDAILY_PRICE', 'SUBROYALTYDAILY_THEORY', 'SUBROYALTY_PRICE', 'SUBROYALTY_THEORY', 'ShopRoyaltyId', 'ShowAccount', 'TICKETDAILY_FEE', 'TICKET_FEE'] vs ['ACCOUNT_TYPE', 'BUSINESSDAYS', 'BUSINESSPROJECTSPLIT_DESC', 'BUSINESSPROJECTSPLIT_ID', 'BUSINESSPROJECTSPLIT_STATE', 'BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'CASHPAY_AMOUNT', 'CIGARETTEDAILY_AMOUNT', 'CIGARETTE_AMOUNT', 'CORRECT_AMOUNT', 'DATE_TYPE', 'DIFDAILY_REVENUE', 'DIFFERENT_AMOUNT', 'ENDDATE', 'EXPIREDAYS', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MINTURNOVER', 'MOBILEPAY_AMOUNT', 'NATUREDAY', 'OTHERPAY_AMOUNT', 'RECORD_DATE', 'REGISTERCOMPACT_ID', 'REVENUEDAILY_AMOUNT', 'REVENUE_AMOUNT', 'ROYALTYDAILY_PRICE', 'ROYALTYDAILY_THEORY', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLEMENT_STATE', 'SHOPEXPENSE_ID', 'SHOPROYALTY_ID', 'SMOKERATIO', 'STARTDATE', 'STATISTICS_DATE', 'SUBROYALTYDAILY_PRICE', 'SUBROYALTYDAILY_THEORY', 'SUBROYALTY_PRICE', 'SUBROYALTY_THEORY', 'TICKETDAILY_FEE', 'TICKET_FEE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.ACCOUNT_AMOUNT: 新 API 缺少该字段
- Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.CURCASHPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.CURMOBILEPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.CURROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.CURSUBROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.CURTICKET_FEE: 新 API 缺少该字段
- Result_Data.CalcAccumulate: 新 API 缺少该字段
- Result_Data.CalcExpiredDays: 新 API 缺少该字段
- Result_Data.CompleteState: 新 API 缺少该字段
- Result_Data.ENDDATE_End: 新 API 缺少该字段
- Result_Data.ENDDATE_Start: 新 API 缺少该字段
- Result_Data.ExpenseAmount: 新 API 缺少该字段
- Result_Data.ExpenseList: 新 API 缺少该字段
- Result_Data.LogList: 新 API 缺少该字段
- Result_Data.STARTDATE_End: 新 API 缺少该字段
- Result_Data.STARTDATE_Start: 新 API 缺少该字段
- Result_Data.STATISTICS_DATE_End: 新 API 缺少该字段
- Result_Data.STATISTICS_DATE_Start: 新 API 缺少该字段
- Result_Data.ShopRoyaltyId: 新 API 缺少该字段
- Result_Data.ShowAccount: 新 API 缺少该字段
- Result_Data.ENDDATE: 类型不一致 (str vs int)，值为 '2024/01/31' vs 20240131
- Result_Data.RECORD_DATE: 值不一致 ('2023-12-21T21:13:07' vs '2023/12/21 21:13:07')
- Result_Data.STARTDATE: 类型不一致 (str vs int)，值为 '2023/02/01' vs 20230201
- Result_Data.STATISTICS_DATE: 类型不一致 (str vs int)，值为 '2023/06/03' vs 20230603

原 API 状态: `200`，耗时 `77.29 ms`
新 API 状态: `200`，耗时 `18.78 ms`

### BusinessProject/GetBUSINESSPROJECTSPLITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"BUSINESSPROJECTSPLIT_ID": 138058}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBUSINESSPROJECTSPLITList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBUSINESSPROJECTSPLITList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| OtherData 存在性 | ❌ | True vs False |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ❌ | 仅原 API: ['ACCOUNT_AMOUNT', 'BUSINESSPROJECT_IDS', 'CURCASHPAY_AMOUNT', 'CURMOBILEPAY_AMOUNT', 'CURROYALTY_PRICE', 'CURSUBROYALTY_PRICE', 'CURTICKET_FEE', 'CalcAccumulate', 'CalcExpiredDays', 'CompleteState', 'ENDDATE_End', 'ENDDATE_Start', 'ExpenseAmount', 'ExpenseList', 'LogList', 'STARTDATE_End', 'STARTDATE_Start', 'STATISTICS_DATE_End', 'STATISTICS_DATE_Start', 'ShopRoyaltyId', 'ShowAccount'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.OtherData: 新 API 缺少该字段
- Result_Data.List[0].ACCOUNT_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[0].CURCASHPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].CURMOBILEPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].CURROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.List[0].CURSUBROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.List[0].CURTICKET_FEE: 新 API 缺少该字段
- Result_Data.List[0].CalcAccumulate: 新 API 缺少该字段
- Result_Data.List[0].CalcExpiredDays: 新 API 缺少该字段
- Result_Data.List[0].CompleteState: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].ExpenseAmount: 新 API 缺少该字段
- Result_Data.List[0].ExpenseList: 新 API 缺少该字段
- Result_Data.List[0].LogList: 新 API 缺少该字段
- Result_Data.List[0].STARTDATE_End: 新 API 缺少该字段
- Result_Data.List[0].STARTDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_DATE_End: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_DATE_Start: 新 API 缺少该字段
- Result_Data.List[0].ShopRoyaltyId: 新 API 缺少该字段
- Result_Data.List[0].ShowAccount: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE: 类型不一致 (str vs int)，值为 '2024/01/31' vs 20240131
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2023-12-21T21:24:25' vs '2023/12/21 21:24:25')
- Result_Data.List[0].STARTDATE: 类型不一致 (str vs int)，值为 '2023/02/01' vs 20230201

原 API 状态: `200`，耗时 `312.02 ms`
新 API 状态: `200`，耗时 `10.37 ms`

### BusinessProject/GetBrandReceivables / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBrandReceivables | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBrandReceivables |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 26 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 999 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ❌ | 26 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (26 vs 0)
- Result_Data.OtherData: 列表长度不一致 (11 vs 0)
- Result_Data.PageSize: 值不一致 (10 vs 999)
- Result_Data.TotalCount: 值不一致 (26 vs 0)

原 API 状态: `200`，耗时 `151.43 ms`
新 API 状态: `200`，耗时 `2.97 ms`

### BusinessProject/GetBusinessPaymentDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessPaymentId": 2}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBusinessPaymentDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBusinessPaymentDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACTUAL_REVENUE', 'BUSINESSDAYS', 'BUSINESSPAYMENT_DESC', 'BUSINESSPAYMENT_ID', 'BUSINESSPAYMENT_STATUS', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_BRAND', 'BUSINESS_BRANDNAME', 'BUSINESS_TYPE', 'ENDACCOUNT_ENDDATE', 'ENDACCOUNT_STARTDATE', 'ENDDATE', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'NATUREDAY', 'OPERATE_DATE', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_NAME', 'REVENUE_ACCOUNT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SHOPROYALTY_ID', 'STARTDATE', 'TICKET_COUNT', 'TOTAL_COUNT'] vs ['ACTUAL_REVENUE', 'BUSINESSDAYS', 'BUSINESSPAYMENT_DESC', 'BUSINESSPAYMENT_ID', 'BUSINESSPAYMENT_STATUS', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_BRAND', 'BUSINESS_BRANDNAME', 'BUSINESS_TRADE', 'BUSINESS_TRADENAME', 'BUSINESS_TYPE', 'ENDACCOUNT_ENDDATE', 'ENDACCOUNT_STARTDATE', 'ENDDATE', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'NATUREDAY', 'OPERATE_DATE', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_NAME', 'REVENUE_ACCOUNT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SERVERPART_TYPE', 'SHOPROYALTY_ID', 'STARTDATE', 'TICKET_COUNT', 'TOTAL_COUNT'] |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- Result_Data.BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.BUSINESSPAYMENT_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `108.9 ms`
新 API 状态: `200`，耗时 `12.99 ms`

### BusinessProject/GetBusinessPaymentList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_ID": 416}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBusinessPaymentList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBusinessPaymentList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 6 vs 6 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 6 vs 6 |
| 首条字段集合 | ❌ | 仅原 API: [] | 仅新 API: ['BUSINESS_TRADE', 'BUSINESS_TRADENAME', 'SERVERPART_TYPE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[0].BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[0].OPERATE_DATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[1].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[1].BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.List[1].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[1].GUARANTEERATIO: 类型不一致 (float vs NoneType)，值为 0.0 vs None
- Result_Data.List[1].OPERATE_DATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[2].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[2].BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.List[2].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[2].OPERATE_DATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[3].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[3].BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.List[3].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[3].OPERATE_DATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[4].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[4].BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.List[4].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[4].OPERATE_DATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[5].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[5].BUSINESS_TRADENAME: 新 API 多出该字段
- Result_Data.List[5].SERVERPART_TYPE: 新 API 多出该字段
- Result_Data.List[5].OPERATE_DATE: 类型不一致 (int vs NoneType)，值为 0 vs None

原 API 状态: `200`，耗时 `107.74 ms`
新 API 状态: `200`，耗时 `10.96 ms`

### BusinessProject/GetBusinessProjectDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessProjectId": 1905}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBusinessProjectDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBusinessProjectDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BUSINESSPROJECT_DESC', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESS_TYPE', 'CLOSED_DATE', 'CLOSED_DATE_End', 'CLOSED_DATE_Start', 'COMPACT_NAME', 'COMPACT_TYPE', 'DueDate_End', 'DueDate_Start', 'EXPIREDAYS', 'GUARANTEE_PRICE', 'GUARANTEE_RATE', 'LogList', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MULTIPROJECT_STATE', 'MerchantsIdEncrypted', 'OPERATE_DATE', 'OVERGUARANTEE_RATE', 'PROJECT_DAYS', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'PROJECT_VALID', 'Period_AvgAmount', 'Period_Count', 'ProjectStateSearch', 'ProjectTypeSearch', 'Project_ICO', 'REGISTERCOMPACT_ID', 'ROYALTY_PRICE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'SPREGIONTYPE_IDS', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'SWITCH_DATE', 'SWITCH_MODES', 'ShowShare', 'SwitchLogList'] vs ['BUSINESSPROJECT_DESC', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_TYPE', 'CLOSED_DATE', 'COMPACT_NAME', 'COMPACT_TYPE', 'GUARANTEE_PRICE', 'GUARANTEE_RATE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MULTIPROJECT_STATE', 'OPERATE_DATE', 'OVERGUARANTEE_RATE', 'PROJECT_DAYS', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'PROJECT_VALID', 'REGISTERCOMPACT_ID', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'SPREGIONTYPE_IDS', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'SWITCH_DATE', 'SWITCH_MODES'] |
| 完整响应体 | ❌ | 发现 19 处差异 |

差异明细：
- Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.CLOSED_DATE_End: 新 API 缺少该字段
- Result_Data.CLOSED_DATE_Start: 新 API 缺少该字段
- Result_Data.DueDate_End: 新 API 缺少该字段
- Result_Data.DueDate_Start: 新 API 缺少该字段
- Result_Data.EXPIREDAYS: 新 API 缺少该字段
- Result_Data.LogList: 新 API 缺少该字段
- Result_Data.MerchantsIdEncrypted: 新 API 缺少该字段
- Result_Data.Period_AvgAmount: 新 API 缺少该字段
- Result_Data.Period_Count: 新 API 缺少该字段
- Result_Data.ProjectStateSearch: 新 API 缺少该字段
- Result_Data.ProjectTypeSearch: 新 API 缺少该字段
- Result_Data.Project_ICO: 新 API 缺少该字段
- Result_Data.ROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.ShowShare: 新 API 缺少该字段
- Result_Data.SwitchLogList: 新 API 缺少该字段
- Result_Data.OPERATE_DATE: 值不一致 ('2025-11-18T17:50:26' vs '2025/11/18 17:50:26')
- Result_Data.PROJECT_ENDDATE: 值不一致 ('2028-07-14T00:00:00' vs '2028/7/14 0:00:00')
- Result_Data.PROJECT_STARTDATE: 值不一致 ('2025-07-15T00:00:00' vs '2025/7/15 0:00:00')

原 API 状态: `200`，耗时 `537.41 ms`
新 API 状态: `200`，耗时 `109.74 ms`

### BusinessProject/GetBusinessProjectList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetBusinessProjectList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetBusinessProjectList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 41 vs 41 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_IDS', 'CLOSED_DATE_End', 'CLOSED_DATE_Start', 'DueDate_End', 'DueDate_Start', 'EXPIREDAYS', 'LogList', 'MerchantsIdEncrypted', 'ProjectStateSearch', 'ProjectTypeSearch', 'Project_ICO', 'ROYALTY_PRICE', 'ShowShare', 'SwitchLogList'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[0].CLOSED_DATE_End: 新 API 缺少该字段
- Result_Data.List[0].CLOSED_DATE_Start: 新 API 缺少该字段
- Result_Data.List[0].DueDate_End: 新 API 缺少该字段
- Result_Data.List[0].DueDate_Start: 新 API 缺少该字段
- Result_Data.List[0].EXPIREDAYS: 新 API 缺少该字段
- Result_Data.List[0].LogList: 新 API 缺少该字段
- Result_Data.List[0].MerchantsIdEncrypted: 新 API 缺少该字段
- Result_Data.List[0].ProjectStateSearch: 新 API 缺少该字段
- Result_Data.List[0].ProjectTypeSearch: 新 API 缺少该字段
- Result_Data.List[0].Project_ICO: 新 API 缺少该字段
- Result_Data.List[0].ROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.List[0].ShowShare: 新 API 缺少该字段
- Result_Data.List[0].SwitchLogList: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSPROJECT_DESC: 值不一致 ('' vs '【与台账金额不符】保底租金40万/年，年营业额1000万以下按16%提成，1000万（含）-1800万按17%提成，1800（含）以上按22%提。')
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (1905 vs 166)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 值不一致 ('服务区自助售卖玩具机项目租赁合同新桥' vs '新桥服务区（麦当劳）项目')
- Result_Data.List[0].COMPACT_NAME: 值不一致 ('服务区自助售卖玩具机项目租赁合同新桥' vs '驿达公司新桥服务区麦当劳项目')
- Result_Data.List[0].COMPACT_TYPE: 类型不一致 (int vs NoneType)，值为 340001 vs None
- Result_Data.List[0].GUARANTEE_PRICE: 值不一致 (3.03 vs 400.0)
- Result_Data.List[0].MERCHANTS_ID: 值不一致 (-2182 vs -580)
- Result_Data.List[0].MERCHANTS_NAME: 值不一致 ('江苏乾上乾贸易有限公司' vs '安徽联升餐厅食品有限公司')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2025-11-18T17:50:26' vs '2025/9/16 15:49:39')
- Result_Data.List[0].PROJECT_DAYS: 值不一致 (1095 vs 3652)
- Result_Data.List[0].PROJECT_ENDDATE: 值不一致 ('2028-07-14T00:00:00' vs '2028/1/31 0:00:00')

原 API 状态: `200`，耗时 `200.45 ms`
新 API 状态: `200`，耗时 `87.33 ms`

### BusinessProject/GetCONTRACT_SYNDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetCONTRACT_SYNDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetCONTRACT_SYNDetail |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ❌ | 原 API: False | 新 API: True |

差异明细：
- 原 API JSON 解析失败: Expecting value: line 1 column 1 (char 0)

原 API 状态: `404`，耗时 `7.32 ms`
新 API 状态: `200`，耗时 `2.99 ms`

### BusinessProject/GetCONTRACT_SYNList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetCONTRACT_SYNList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetCONTRACT_SYNList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ❌ | 原 API: False | 新 API: True |

差异明细：
- 原 API JSON 解析失败: Expecting value: line 1 column 1 (char 0)

原 API 状态: `404`，耗时 `4.01 ms`
新 API 状态: `200`，耗时 `12.25 ms`

### BusinessProject/GetExpenseSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"serverpart_ids": "416"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetExpenseSummary | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetExpenseSummary |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 137 vs 690 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9999 vs 9999 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ❌ | 1 vs 690 |
| 首条字段集合 | ❌ | 仅原 API: ['children', 'node'] | 仅新 API: ['BUSINESS_UNIT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SHOPEXPENSE_AMOUNT', 'SHOPEXPENSE_TYPE', 'STATISTICS_MONTH'] |
| 完整响应体 | ❌ | 发现 11 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 690)
- Result_Data.List[0].children: 新 API 缺少该字段
- Result_Data.List[0].node: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_UNIT: 新 API 多出该字段
- Result_Data.List[0].SERVERPARTSHOP_ID: 新 API 多出该字段
- Result_Data.List[0].SERVERPARTSHOP_NAME: 新 API 多出该字段
- Result_Data.List[0].SHOPEXPENSE_AMOUNT: 新 API 多出该字段
- Result_Data.List[0].SHOPEXPENSE_TYPE: 新 API 多出该字段
- Result_Data.List[0].STATISTICS_MONTH: 新 API 多出该字段
- Result_Data.OtherData: 列表长度不一致 (5 vs 0)
- Result_Data.TotalCount: 值不一致 (137 vs 690)

原 API 状态: `200`，耗时 `218.94 ms`
新 API 状态: `200`，耗时 `37.12 ms`

### BusinessProject/GetMerchantSplit / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"MerchantId": -1104, "ServerpartId": 419}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetMerchantSplit | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetMerchantSplit |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 4 vs 91 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 91 |
| List 条数 | ❌ | 4 vs 91 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_NAME', 'BUSINESS_ENDDATE', 'BUSINESS_PERIOD', 'BUSINESS_STARTDATE', 'BUSINESS_STATE', 'CLOSED_DATE', 'DAILY_AMOUNT', 'EXPENSE_TYPE', 'MERCHANTS_NAME', 'MERCHANT_PAYMENT', 'OTHER_EXPENSE', 'PERIOD_INDEX', 'PROPERTY_FEE', 'WATERELECTRIC_EXPENSE'] | 仅新 API: ['ACCCASHPAY_CORRECT', 'ACCCIGARETTE_AMOUNT', 'ACCMOBILEPAY_CORRECT', 'ACCOUNT_TYPE', 'ACCREVENUE_AMOUNT', 'ACCROYALTY_PRICE', 'ACCROYALTY_THEORY', 'ACCSUBROYALTY_PRICE', 'ACCSUBROYALTY_THEORY', 'ACCTICKET_FEE', 'BIZPSPLITMONTH_ID', 'BIZPSPLITMONTH_STATE', 'BUSINESSAPPROVAL_ID', 'CASHPAY_AMOUNT', 'CASHPAY_CORRECT', 'CORRECT_AMOUNT', 'DIFFERENT_AMOUNT', 'MOBILEPAY_AMOUNT', 'MOBILEPAY_CORRECT', 'NATUREDAY', 'OTHERPAY_AMOUNT', 'RECORD_DATE', 'SMOKERATIO'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (4 vs 91)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_PERIOD: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STATE: 新 API 缺少该字段
- Result_Data.List[0].CLOSED_DATE: 新 API 缺少该字段
- Result_Data.List[0].DAILY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].EXPENSE_TYPE: 新 API 缺少该字段
- Result_Data.List[0].MERCHANTS_NAME: 新 API 缺少该字段
- Result_Data.List[0].MERCHANT_PAYMENT: 新 API 缺少该字段
- Result_Data.List[0].OTHER_EXPENSE: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_INDEX: 新 API 缺少该字段
- Result_Data.List[0].PROPERTY_FEE: 新 API 缺少该字段
- Result_Data.List[0].WATERELECTRIC_EXPENSE: 新 API 缺少该字段
- Result_Data.List[0].ACCCASHPAY_CORRECT: 新 API 多出该字段
- Result_Data.List[0].ACCCIGARETTE_AMOUNT: 新 API 多出该字段
- Result_Data.List[0].ACCMOBILEPAY_CORRECT: 新 API 多出该字段
- Result_Data.List[0].ACCOUNT_TYPE: 新 API 多出该字段
- Result_Data.List[0].ACCREVENUE_AMOUNT: 新 API 多出该字段
- Result_Data.List[0].ACCROYALTY_PRICE: 新 API 多出该字段
- Result_Data.List[0].ACCROYALTY_THEORY: 新 API 多出该字段
- Result_Data.List[0].ACCSUBROYALTY_PRICE: 新 API 多出该字段
- Result_Data.List[0].ACCSUBROYALTY_THEORY: 新 API 多出该字段
- Result_Data.List[0].ACCTICKET_FEE: 新 API 多出该字段

原 API 状态: `200`，耗时 `384.54 ms`
新 API 状态: `200`，耗时 `590.48 ms`

### BusinessProject/GetMerchantsReceivables / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetMerchantsReceivables | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetMerchantsReceivables |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 200 vs 100 |
| Result_Desc | ❌ | 查询失败，请传入经营商户内码或门店内码集合！ vs 查询成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (200 vs 100)
- Result_Data: 类型不一致 (NoneType vs dict)，值为 None vs {'COOPMERCHANTS_ID': None, 'COOPMERCHANTS_NAME': '', 'COOPMERCHANTS_TYPENAME': '', 'COOPMERCHANTS_NATURE': '', 'BANK_NAME': '', 'BANK_ACCOUNT': '', 'ACCOUNT_AMOUNT': 0, 'ACTUAL_PAYMENT': 0, 'CURRENTBALANCE': 0, 'UNDISTRIBUTED_AMOUNT': 0, 'AccountReceivablesList': []}
- Result_Desc: 值不一致 ('查询失败，请传入经营商户内码或门店内码集合！' vs '查询成功')

原 API 状态: `200`，耗时 `15.63 ms`
新 API 状态: `200`，耗时 `2.32 ms`

### BusinessProject/GetMerchantsReceivablesList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetMerchantsReceivablesList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetMerchantsReceivablesList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 300 vs 1891 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 10 vs 10 |
| 首条字段集合 | ❌ | 仅原 API: ['ACCOUNT_DATE', 'AccountReceivablesList', 'COOPMERCHANTS_EN', 'COOPMERCHANTS_ID_Encrypted', 'COOPMERCHANTS_LINKMAN', 'COOPMERCHANTS_MOBILEPHONE', 'TAXPAYER_IDENTIFYCODE', 'UNDISTRIBUTED_AMOUNT'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].ACCOUNT_DATE: 新 API 缺少该字段
- Result_Data.List[0].AccountReceivablesList: 新 API 缺少该字段
- Result_Data.List[0].COOPMERCHANTS_EN: 新 API 缺少该字段
- Result_Data.List[0].COOPMERCHANTS_ID_Encrypted: 新 API 缺少该字段
- Result_Data.List[0].COOPMERCHANTS_LINKMAN: 新 API 缺少该字段
- Result_Data.List[0].COOPMERCHANTS_MOBILEPHONE: 新 API 缺少该字段
- Result_Data.List[0].TAXPAYER_IDENTIFYCODE: 新 API 缺少该字段
- Result_Data.List[0].UNDISTRIBUTED_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].ACCOUNT_AMOUNT: 类型不一致 (float vs int)，值为 10616.184456 vs 0
- Result_Data.List[0].ACTUAL_PAYMENT: 类型不一致 (float vs int)，值为 80.008 vs 0
- Result_Data.List[0].BANK_ACCOUNT: 值不一致 ('' vs '1')
- Result_Data.List[0].BANK_NAME: 值不一致 ('' vs '1')
- Result_Data.List[0].COOPMERCHANTS_ID: 类型不一致 (str vs int)，值为 'C64BAE48506C3ACB' vs -684
- Result_Data.List[0].COOPMERCHANTS_NAME: 值不一致 ('广州弘胜餐饮管理有限公司' vs '1')
- Result_Data.List[0].COOPMERCHANTS_NATURE: 值不一致 ('企业公司' vs '')
- Result_Data.List[0].COOPMERCHANTS_TYPENAME: 值不一致 ('合作经营类' vs '')
- Result_Data.List[0].CURRENTBALANCE: 类型不一致 (float vs int)，值为 10536.176456 vs 0
- Result_Data.List[0].PROJECT_SIGNCOUNT: 值不一致 (97 vs 0)
- Result_Data.List[1].ACCOUNT_DATE: 新 API 缺少该字段
- Result_Data.List[1].AccountReceivablesList: 新 API 缺少该字段
- Result_Data.List[1].COOPMERCHANTS_EN: 新 API 缺少该字段
- Result_Data.List[1].COOPMERCHANTS_ID_Encrypted: 新 API 缺少该字段
- Result_Data.List[1].COOPMERCHANTS_LINKMAN: 新 API 缺少该字段
- Result_Data.List[1].COOPMERCHANTS_MOBILEPHONE: 新 API 缺少该字段
- Result_Data.List[1].TAXPAYER_IDENTIFYCODE: 新 API 缺少该字段

原 API 状态: `200`，耗时 `15358.15 ms`
新 API 状态: `200`，耗时 `2059.48 ms`

### BusinessProject/GetMerchantsReceivablesReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetMerchantsReceivablesReport | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetMerchantsReceivablesReport |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 185 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 185 vs 999 |
| List 条数 | ❌ | 185 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (185 vs 0)
- Result_Data.PageSize: 值不一致 (185 vs 999)
- Result_Data.TotalCount: 值不一致 (185 vs 0)

原 API 状态: `200`，耗时 `2341.42 ms`
新 API 状态: `200`，耗时 `2.62 ms`

### BusinessProject/GetMonthSummaryList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetMonthSummaryList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetMonthSummaryList |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetMonthSummaryList”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `4.1 ms`
新 API 状态: `200`，耗时 `2.74 ms`

### BusinessProject/GetNoProjectShopList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": 340000, "ServerpartID": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetNoProjectShopList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetNoProjectShopList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 10 vs 11 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 11 |
| List 条数 | ❌ | 10 vs 11 |
| 首条字段集合 | ❌ | 仅原 API: ['index', 'type'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (10 vs 11)
- Result_Data.List[0].index: 新 API 缺少该字段
- Result_Data.List[0].type: 新 API 缺少该字段
- Result_Data.List[0].value: 类型不一致 (float vs int)，值为 3066.0 vs 3066
- Result_Data.List[1].index: 新 API 缺少该字段
- Result_Data.List[1].type: 新 API 缺少该字段
- Result_Data.List[1].value: 类型不一致 (float vs int)，值为 3046.0 vs 3046
- Result_Data.List[2].index: 新 API 缺少该字段
- Result_Data.List[2].type: 新 API 缺少该字段
- Result_Data.List[2].value: 类型不一致 (float vs int)，值为 3064.0 vs 3064
- Result_Data.List[3].index: 新 API 缺少该字段
- Result_Data.List[3].type: 新 API 缺少该字段
- Result_Data.List[3].value: 类型不一致 (float vs int)，值为 3062.0 vs 3062
- Result_Data.List[4].index: 新 API 缺少该字段
- Result_Data.List[4].type: 新 API 缺少该字段
- Result_Data.List[4].value: 类型不一致 (float vs int)，值为 3068.0 vs 3068
- Result_Data.List[5].index: 新 API 缺少该字段
- Result_Data.List[5].type: 新 API 缺少该字段
- Result_Data.List[5].value: 类型不一致 (float vs int)，值为 4128.0 vs 4128
- Result_Data.List[6].index: 新 API 缺少该字段
- Result_Data.List[6].type: 新 API 缺少该字段
- Result_Data.List[6].value: 类型不一致 (float vs int)，值为 3056.0 vs 3056
- Result_Data.List[7].index: 新 API 缺少该字段
- Result_Data.List[7].type: 新 API 缺少该字段
- Result_Data.List[7].value: 类型不一致 (float vs int)，值为 3044.0 vs 3044

原 API 状态: `200`，耗时 `176.44 ms`
新 API 状态: `200`，耗时 `61.3 ms`

### BusinessProject/GetPERIODWARNINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PERIODWARNINGId": 884}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPERIODWARNINGDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPERIODWARNINGDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACTUAL_RATIO', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESS_PERIOD', 'BUSINESS_STATE', 'BUSINESS_STATES', 'BUSINESS_TRADE', 'BUSINESS_TRADES', 'BUSINESS_TYPE', 'CA_COST', 'COMMISSION_RATIO', 'COST_AMOUNT', 'COST_RATE', 'DEPRECIATION_EXPENSE', 'DEPRECIATION_YEAR', 'ENDDATE', 'ENDDATE_End', 'ENDDATE_Start', 'GUARANTEED_PROGRESS', 'GUARANTEERATIO', 'GUARANTEE_PRICE', 'LABOURS_COUNT', 'LABOURS_WAGE', 'MERCHANTS_ID', 'MERCHANTS_IDS', 'MERCHANTS_NAME', 'MINTURNOVER', 'MONTH_COUNT', 'OTHER_EXPENSE', 'PERIODWARNING_ID', 'PERIOD_INDEX', 'PERIOD_PROGRESS', 'PROFIT_AMOUNT', 'PROJECT_ENDDATE', 'PROJECT_ENDDATE_End', 'PROJECT_ENDDATE_Start', 'PROJECT_STARTDATE', 'RECORD_DATE', 'RENTFEE', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SHOPROYALTY_ID', 'SHOPROYALTY_IDS', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'SUBROYALTY_THEORY', 'TICKET_COUNT', 'WARNING_CONTENT', 'WARNING_TYPE', 'WARNING_TYPES'] vs ['ACTUAL_RATIO', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_PERIOD', 'BUSINESS_STATE', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'CA_COST', 'COMMISSION_RATIO', 'COST_AMOUNT', 'COST_RATE', 'DEPRECIATION_EXPENSE', 'DEPRECIATION_YEAR', 'ENDDATE', 'GUARANTEERATIO', 'GUARANTEE_PRICE', 'LABOURS_COUNT', 'LABOURS_WAGE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MINTURNOVER', 'MONTH_COUNT', 'OTHER_EXPENSE', 'PERIODWARNING_DESC', 'PERIODWARNING_ID', 'PERIOD_INDEX', 'PROFIT_AMOUNT', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'RECORD_DATE', 'RENTFEE', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SHOPROYALTY_ID', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'SUBROYALTY_THEORY', 'TICKET_COUNT', 'WARNING_CONTENT', 'WARNING_TYPE'] |
| 完整响应体 | ❌ | 发现 18 处差异 |

差异明细：
- Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.BUSINESS_STATES: 新 API 缺少该字段
- Result_Data.BUSINESS_TRADES: 新 API 缺少该字段
- Result_Data.ENDDATE_End: 新 API 缺少该字段
- Result_Data.ENDDATE_Start: 新 API 缺少该字段
- Result_Data.GUARANTEED_PROGRESS: 新 API 缺少该字段
- Result_Data.MERCHANTS_IDS: 新 API 缺少该字段
- Result_Data.PERIOD_PROGRESS: 新 API 缺少该字段
- Result_Data.PROJECT_ENDDATE_End: 新 API 缺少该字段
- Result_Data.PROJECT_ENDDATE_Start: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.WARNING_TYPES: 新 API 缺少该字段
- Result_Data.PERIODWARNING_DESC: 新 API 多出该字段
- Result_Data.RECORD_DATE: 值不一致 ('2026-03-06T20:36:57' vs '2025/6/9 18:46:24')
- Result_Data.STAFF_ID: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.STAFF_NAME: 值不一致 ('' vs '系统开发者')

原 API 状态: `200`，耗时 `125.51 ms`
新 API 状态: `200`，耗时 `9.29 ms`

### BusinessProject/GetPERIODWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPERIODWARNINGList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPERIODWARNINGList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 62 vs 57 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_IDS', 'BUSINESS_STATES', 'BUSINESS_TRADES', 'ENDDATE_End', 'ENDDATE_Start', 'GUARANTEED_PROGRESS', 'MERCHANTS_IDS', 'PERIOD_PROGRESS', 'PROJECT_ENDDATE_End', 'PROJECT_ENDDATE_Start', 'SERVERPARTSHOP_IDS', 'SERVERPART_IDS', 'SHOPROYALTY_IDS', 'WARNING_TYPES'] | 仅新 API: ['PERIODWARNING_DESC'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STATES: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADES: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].GUARANTEED_PROGRESS: 新 API 缺少该字段
- Result_Data.List[0].MERCHANTS_IDS: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_PROGRESS: 新 API 缺少该字段
- Result_Data.List[0].PROJECT_ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[0].PROJECT_ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.List[0].WARNING_TYPES: 新 API 缺少该字段
- Result_Data.List[0].PERIODWARNING_DESC: 新 API 多出该字段
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2026-03-06T20:36:57' vs '2025/6/9 18:46:24')
- Result_Data.List[0].STAFF_ID: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.List[0].STAFF_NAME: 值不一致 ('' vs '系统开发者')
- Result_Data.List[1].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[1].BUSINESS_STATES: 新 API 缺少该字段
- Result_Data.List[1].BUSINESS_TRADES: 新 API 缺少该字段
- Result_Data.List[1].ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[1].ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[1].GUARANTEED_PROGRESS: 新 API 缺少该字段
- Result_Data.List[1].MERCHANTS_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `107.57 ms`
新 API 状态: `200`，耗时 `21.05 ms`

### BusinessProject/GetPROJECTSPLITMONTHDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROJECTSPLITMONTHId": 109}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPROJECTSPLITMONTHDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPROJECTSPLITMONTHDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BREACH_PENALTY', 'BUSINESSDAYS', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESS_TYPE', 'CASHPAY_AMOUNT', 'CASHPAY_CORRECT', 'CMONTH_COMINCOME', 'CMONTH_TAXCOMINCOME', 'COMPACT_ENDDATE', 'COMPACT_STARTDATE', 'CONFIRM_COMINCOME', 'CONFIRM_INCOME', 'CONFIRM_TAXCOMINCOME', 'CONFIRM_TAXINCOME', 'DECORATE_ENDDATE', 'DECORATE_STARTDATE', 'DUTY_PARAGRAPH', 'ELECTRIC_EXPENSE', 'ENDDATE', 'GUARANTEERATIO', 'HOUSE_RENT', 'LMONTH_COMINCOME', 'LMONTH_TAXCOMINCOME', 'MERCHANTS_ID', 'MERCHANTS_IDS', 'MINTURNOVER', 'MOBILEPAY_AMOUNT', 'MOBILEPAY_CORRECT', 'MONTHLY_COUNT', 'MONTHLY_INCOME', 'MONTHLY_TAXINCOME', 'MONTHLY_TOTALINCOME', 'MONTHLY_TOTALTAXINCOME', 'NATUREDAY', 'OTHER_EXPENSE', 'PERIOD_INDEX', 'PROJECTSPLITMONTH_DESC', 'PROJECTSPLITMONTH_ID', 'PROJECTSPLITMONTH_STATE', 'PROPERTY_FEE', 'RECORD_DATE', 'REFUND_SUPPLEMENT', 'REGISTERCOMPACT_ID', 'REGISTERCOMPACT_IDS', 'REVENUE_AMOUNT', 'REVENUE_TOTALAMOUNT', 'ROYALTY_PRICE', 'ROYALTY_TOTALAMOUNT', 'SECURITYDEPOSIT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SETTLEMENT_TYPE', 'SHOPROYALTY_ID', 'SHOPROYALTY_IDS', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'SUBROYALTY_PRICE', 'SWITCH_DATE', 'TICKET_FEE', 'WATER_EXPENSE'] vs ['BREACH_PENALTY', 'BUSINESSDAYS', 'BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'CASHPAY_AMOUNT', 'CASHPAY_CORRECT', 'CMONTH_COMINCOME', 'CMONTH_TAXCOMINCOME', 'COMPACT_ENDDATE', 'COMPACT_STARTDATE', 'CONFIRM_COMINCOME', 'CONFIRM_INCOME', 'CONFIRM_TAXCOMINCOME', 'CONFIRM_TAXINCOME', 'DECORATE_ENDDATE', 'DECORATE_STARTDATE', 'DUTY_PARAGRAPH', 'ELECTRIC_EXPENSE', 'ENDDATE', 'GUARANTEERATIO', 'HOUSE_RENT', 'LMONTH_COMINCOME', 'LMONTH_TAXCOMINCOME', 'MERCHANTS_ID', 'MINTURNOVER', 'MOBILEPAY_AMOUNT', 'MOBILEPAY_CORRECT', 'MONTHLY_COUNT', 'MONTHLY_INCOME', 'MONTHLY_TAXINCOME', 'MONTHLY_TOTALINCOME', 'MONTHLY_TOTALTAXINCOME', 'NATUREDAY', 'OTHER_EXPENSE', 'PERIOD_INDEX', 'PROJECTSPLITMONTH_DESC', 'PROJECTSPLITMONTH_ID', 'PROJECTSPLITMONTH_STATE', 'PROPERTY_FEE', 'RECORD_DATE', 'REFUND_SUPPLEMENT', 'REGISTERCOMPACT_ID', 'REVENUE_AMOUNT', 'REVENUE_TOTALAMOUNT', 'ROYALTY_PRICE', 'ROYALTY_TOTALAMOUNT', 'SECURITYDEPOSIT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SETTLEMENT_TYPE', 'SHOPROYALTY_ID', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STATISTICS_MONTH', 'SUBROYALTY_PRICE', 'SWITCH_DATE', 'TICKET_FEE', 'WATER_EXPENSE'] |
| 完整响应体 | ❌ | 发现 8 处差异 |

差异明细：
- Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.MERCHANTS_IDS: 新 API 缺少该字段
- Result_Data.REGISTERCOMPACT_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.RECORD_DATE: 值不一致 ('2024-07-03T16:05:32' vs '2024/7/3 16:05:32')

原 API 状态: `200`，耗时 `160.18 ms`
新 API 状态: `200`，耗时 `13.81 ms`

### BusinessProject/GetPROJECTSPLITMONTHList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPROJECTSPLITMONTHList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPROJECTSPLITMONTHList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 190 vs 190 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_IDS', 'MERCHANTS_IDS', 'REGISTERCOMPACT_IDS', 'SERVERPART_IDS', 'SHOPROYALTY_IDS', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[0].MERCHANTS_IDS: 新 API 缺少该字段
- Result_Data.List[0].REGISTERCOMPACT_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2024-07-03T16:05:32' vs '2024/7/3 16:05:32')
- Result_Data.List[1].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[1].MERCHANTS_IDS: 新 API 缺少该字段
- Result_Data.List[1].REGISTERCOMPACT_IDS: 新 API 缺少该字段
- Result_Data.List[1].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[1].SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.List[1].STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.List[1].STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.List[1].RECORD_DATE: 值不一致 ('2024-07-03T16:05:32' vs '2024/7/3 16:05:32')
- Result_Data.List[2].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[2].MERCHANTS_IDS: 新 API 缺少该字段
- Result_Data.List[2].REGISTERCOMPACT_IDS: 新 API 缺少该字段
- Result_Data.List[2].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[2].SHOPROYALTY_IDS: 新 API 缺少该字段
- Result_Data.List[2].STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.List[2].STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.List[2].RECORD_DATE: 值不一致 ('2024-07-03T16:05:32' vs '2024/7/3 16:05:32')
- Result_Data.List[3].BUSINESSPROJECT_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `156.13 ms`
新 API 状态: `200`，耗时 `28.13 ms`

### BusinessProject/GetPROJECTWARNINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROJECTWARNINGId": 293}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPROJECTWARNINGDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPROJECTWARNINGDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['BUSINESSPROJECTSPLIT_ID', 'BUSINESSPROJECT_ICO', 'BUSINESSPROJECT_NAME', 'BUSINESS_TYPE', 'COMPACT_ENDDATE', 'COMPACT_STARTDATE', 'COOPMERCHANTS_LINKMAN', 'COOPMERCHANTS_MOBILEPHONE', 'DealMark', 'ENDDATE', 'EXPENSE_AMOUNT', 'EXPIREDAYS', 'MINTURNOVER', 'MerchantRatio', 'PROJECTWARNING_DESC', 'PROJECTWARNING_ID', 'PROJECTWARNING_STATE', 'PROJECTWARNING_STATES', 'RECORD_DATE', 'ROYALTY_CRATE', 'ROYALTY_PRICE', 'ROYALTY_RATE', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SHOPROYALTY_ID', 'STARTDATE', 'SWITCH_DATE', 'WARNING_DATE', 'WARNING_DATE_End', 'WARNING_DATE_Start'] vs ['BUSINESSPROJECTSPLIT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_BRAND', 'BUSINESS_TYPE', 'COMPACT_ENDDATE', 'COMPACT_STARTDATE', 'COOPMERCHANTS_LINKMAN', 'COOPMERCHANTS_MOBILEPHONE', 'DealMark', 'ENDDATE', 'EXPENSE_AMOUNT', 'EXPIREDAYS', 'GUARANTEERATIO', 'MINTURNOVER', 'MerchantRatio', 'PROJECTWARNING_DESC', 'PROJECTWARNING_ID', 'PROJECTWARNING_STATE', 'RECORD_DATE', 'ROYALTY_CRATE', 'ROYALTY_PRICE', 'ROYALTY_RATE', 'SECONDPART_LINKMAN', 'SECONDPART_MOBILE', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SHOPROYALTY_ID', 'STARTDATE', 'SWITCH_DATE', 'WARNING_DATE'] |
| 完整响应体 | ❌ | 发现 14 处差异 |

差异明细：
- Result_Data.BUSINESSPROJECT_ICO: 新 API 缺少该字段
- Result_Data.PROJECTWARNING_STATES: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.WARNING_DATE_End: 新 API 缺少该字段
- Result_Data.WARNING_DATE_Start: 新 API 缺少该字段
- Result_Data.BUSINESS_BRAND: 新 API 多出该字段
- Result_Data.GUARANTEERATIO: 新 API 多出该字段
- Result_Data.SECONDPART_LINKMAN: 新 API 多出该字段
- Result_Data.SECONDPART_MOBILE: 新 API 多出该字段
- Result_Data.COMPACT_ENDDATE: 值不一致 ('2027/03/02' vs '2027/3/2 0:00:00')
- Result_Data.COMPACT_STARTDATE: 值不一致 ('2024/02/01' vs '2024/2/1 0:00:00')
- Result_Data.MerchantRatio: 值不一致 ('28:72' vs '28.0:72.0')
- Result_Data.RECORD_DATE: 值不一致 ('2024-03-07T12:27:11' vs '2024/3/7 12:27:11')
- Result_Data.SWITCH_DATE: 类型不一致 (str vs float)，值为 '2024/04/01 00:00:07' vs 20240401000007.0

原 API 状态: `200`，耗时 `103.9 ms`
新 API 状态: `200`，耗时 `67.49 ms`

### BusinessProject/GetPROJECTWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPROJECTWARNINGList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPROJECTWARNINGList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 10 vs 10 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['BUSINESSPROJECT_ICO', 'COMPACT_ENDDATE', 'COMPACT_STARTDATE', 'COOPMERCHANTS_LINKMAN', 'COOPMERCHANTS_MOBILEPHONE', 'MerchantRatio', 'PROJECTWARNING_STATES', 'SERVERPART_IDS', 'WARNING_DATE_End', 'WARNING_DATE_Start'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_ICO: 新 API 缺少该字段
- Result_Data.List[0].COMPACT_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].COMPACT_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].COOPMERCHANTS_LINKMAN: 新 API 缺少该字段
- Result_Data.List[0].COOPMERCHANTS_MOBILEPHONE: 新 API 缺少该字段
- Result_Data.List[0].MerchantRatio: 新 API 缺少该字段
- Result_Data.List[0].PROJECTWARNING_STATES: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].WARNING_DATE_End: 新 API 缺少该字段
- Result_Data.List[0].WARNING_DATE_Start: 新 API 缺少该字段
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2024-03-07T12:27:11' vs '2024/3/7 12:27:11')
- Result_Data.List[0].SWITCH_DATE: 类型不一致 (str vs float)，值为 '2024/04/01 00:00:07' vs 20240401000007.0
- Result_Data.List[1].BUSINESSPROJECT_ICO: 新 API 缺少该字段
- Result_Data.List[1].COMPACT_ENDDATE: 新 API 缺少该字段
- Result_Data.List[1].COMPACT_STARTDATE: 新 API 缺少该字段
- Result_Data.List[1].COOPMERCHANTS_LINKMAN: 新 API 缺少该字段
- Result_Data.List[1].COOPMERCHANTS_MOBILEPHONE: 新 API 缺少该字段
- Result_Data.List[1].MerchantRatio: 新 API 缺少该字段
- Result_Data.List[1].PROJECTWARNING_STATES: 新 API 缺少该字段
- Result_Data.List[1].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[1].WARNING_DATE_End: 新 API 缺少该字段
- Result_Data.List[1].WARNING_DATE_Start: 新 API 缺少该字段
- Result_Data.List[1].RECORD_DATE: 值不一致 ('2024-05-07T12:16:38' vs '2024/5/7 12:16:38')
- Result_Data.List[1].SWITCH_DATE: 类型不一致 (str vs float)，值为 '2024/06/01 00:00:15' vs 20240601000015.0
- Result_Data.List[2].BUSINESSPROJECT_ICO: 新 API 缺少该字段

原 API 状态: `200`，耗时 `152.04 ms`
新 API 状态: `200`，耗时 `12.68 ms`

### BusinessProject/GetPaymentConfirmDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PaymentConfirmId": 5240}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPaymentConfirmDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPaymentConfirmDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACCOUNT_AMOUNT', 'ACCOUNT_DATE', 'ACCOUNT_NAME', 'ACCOUNT_TYPE', 'ACTUAL_PAYMENT', 'ATTACHMENT_FILES', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_TYPE', 'CONFIRMDATE', 'CURRENTBALANCE', 'MANAGEMONTH', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'PAYMENTCONFIRM_DESC', 'PAYMENTCONFIRM_ID', 'PAYMENTCONFIRM_PID', 'PAYMENTCONFIRM_VALID', 'PAYMENTDATE', 'PAYMENT_ACCOUNTINFO', 'REGISTERCOMPACT_ID', 'REMARKS_DESC', 'SERVERPART_NAME', 'STAFF_ID', 'STAFF_NAME'] vs ['ACCOUNT_AMOUNT', 'ACCOUNT_DATE', 'ACCOUNT_NAME', 'ACCOUNT_TYPE', 'ACTUAL_PAYMENT', 'ATTACHMENT_FILES', 'BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'CONFIRMDATE', 'CURRENTBALANCE', 'MANAGEMONTH', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'PAYMENTCONFIRM_DESC', 'PAYMENTCONFIRM_ID', 'PAYMENTCONFIRM_VALID', 'PAYMENTDATE', 'PAYMENT_ACCOUNTINFO', 'REGISTERCOMPACT_ID', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ❌ | 发现 13 处差异 |

差异明细：
- Result_Data.BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.PAYMENTCONFIRM_PID: 新 API 缺少该字段
- Result_Data.REMARKS_DESC: 新 API 缺少该字段
- Result_Data.SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.ACCOUNT_DATE: 类型不一致 (str vs NoneType)，值为 '2024/01/10 19:34:06' vs None
- Result_Data.ACCOUNT_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.ACCOUNT_TYPE: 类型不一致 (str vs int)，值为 '0' vs 0
- Result_Data.ATTACHMENT_FILES: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.CONFIRMDATE: 类型不一致 (NoneType vs int)，值为 None vs 20240110193406
- Result_Data.MERCHANTS_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.PAYMENTCONFIRM_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.PAYMENTDATE: 类型不一致 (NoneType vs int)，值为 None vs 20240205
- Result_Data.PAYMENT_ACCOUNTINFO: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `174.78 ms`
新 API 状态: `200`，耗时 `9.88 ms`

### BusinessProject/GetPaymentConfirmList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PAYMENTCONFIRM_ID": 5240}}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPaymentConfirmList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPaymentConfirmList |
| HTTP 状态码 | ❌ | 500 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 查询成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `500`，耗时 `5.51 ms`
新 API 状态: `200`，耗时 `269.62 ms`

### BusinessProject/GetPeriodWarningList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetPeriodWarningList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetPeriodWarningList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 57 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 1 vs 10 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ❌ | 1 vs 10 |
| 首条字段集合 | ❌ | 仅原 API: ['children', 'node'] | 仅新 API: ['ACTUAL_RATIO', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_PERIOD', 'BUSINESS_STATE', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'CA_COST', 'COMMISSION_RATIO', 'COST_AMOUNT', 'COST_RATE', 'DEPRECIATION_EXPENSE', 'DEPRECIATION_YEAR', 'ENDDATE', 'GUARANTEERATIO', 'GUARANTEE_PRICE', 'LABOURS_COUNT', 'LABOURS_WAGE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MINTURNOVER', 'MONTH_COUNT', 'OTHER_EXPENSE', 'PERIODWARNING_DESC', 'PERIODWARNING_ID', 'PERIOD_INDEX', 'PROFIT_AMOUNT', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'RECORD_DATE', 'RENTFEE', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SHOPROYALTY_ID', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'SUBROYALTY_THEORY', 'TICKET_COUNT', 'WARNING_CONTENT', 'WARNING_TYPE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 10)
- Result_Data.List[0].children: 新 API 缺少该字段
- Result_Data.List[0].node: 新 API 缺少该字段
- Result_Data.List[0].ACTUAL_RATIO: 新 API 多出该字段
- Result_Data.List[0].BUSINESSPROJECT_ID: 新 API 多出该字段
- Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 多出该字段
- Result_Data.List[0].BUSINESS_PERIOD: 新 API 多出该字段
- Result_Data.List[0].BUSINESS_STATE: 新 API 多出该字段
- Result_Data.List[0].BUSINESS_TRADE: 新 API 多出该字段
- Result_Data.List[0].BUSINESS_TYPE: 新 API 多出该字段
- Result_Data.List[0].CA_COST: 新 API 多出该字段
- Result_Data.List[0].COMMISSION_RATIO: 新 API 多出该字段
- Result_Data.List[0].COST_AMOUNT: 新 API 多出该字段
- Result_Data.List[0].COST_RATE: 新 API 多出该字段
- Result_Data.List[0].DEPRECIATION_EXPENSE: 新 API 多出该字段
- Result_Data.List[0].DEPRECIATION_YEAR: 新 API 多出该字段
- Result_Data.List[0].ENDDATE: 新 API 多出该字段
- Result_Data.List[0].GUARANTEERATIO: 新 API 多出该字段
- Result_Data.List[0].GUARANTEE_PRICE: 新 API 多出该字段
- Result_Data.List[0].LABOURS_COUNT: 新 API 多出该字段
- Result_Data.List[0].LABOURS_WAGE: 新 API 多出该字段
- Result_Data.List[0].MERCHANTS_ID: 新 API 多出该字段
- Result_Data.List[0].MERCHANTS_NAME: 新 API 多出该字段
- Result_Data.List[0].MINTURNOVER: 新 API 多出该字段
- Result_Data.List[0].MONTH_COUNT: 新 API 多出该字段

原 API 状态: `200`，耗时 `309.36 ms`
新 API 状态: `200`，耗时 `24.21 ms`

### BusinessProject/GetProjectAccountDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessApprovalId": 18751}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetProjectAccountDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetProjectAccountDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 200 |
| Result_Desc | ❌ | 查询成功 vs 查询失败，无数据返回！ |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 200)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'BUSINESSPROJECT_ID': 1498, 'BUSINESSPROJECT_NAME': '太白服务区同庆楼合同项目', 'REGISTERCOMPACT_ID': 1537, 'COMPACT_NAME': '太白服务区同庆楼合同项目', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': None, 'SERVERPART_ID': '505', 'SERVERPART_NAME': '太白服务区', 'SERVERPARTSHOP_ID': '2158,2156', 'SERVERPARTSHOP_NAME': '西区同庆楼,东区同庆楼', 'MERCHANTS_ID': -1104, 'MERCHANTS_NAME': '广州弘胜餐饮管理有限公司', 'CURRENT_PERIOD': '第2期', 'SHOPROYALTY_ID': 4074, 'STARTDATE': '2025/02/01', 'ENDDATE': '2026/01/31', 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'NATUREDAY': 365.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': 566218.0, 'CURREVENUE_AMOUNT': 26795.0, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2026/01', 'SETTLEMENT_TYPE': 2, 'SETTLEMENT_STATE': 2, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': 18751, 'APPOVED_IDS': '1333', 'APPOVED_NAME': None, 'PEND_STATE': -1, 'APPLY_PROCCESS': False, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs '查询失败，无数据返回！')

原 API 状态: `200`，耗时 `225.37 ms`
新 API 状态: `200`，耗时 `26.48 ms`

### BusinessProject/GetProjectAccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetProjectAccountList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetProjectAccountList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 574 vs 20 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 574 vs 10 |
| List 条数 | ❌ | 574 vs 10 |
| 首条字段集合 | ❌ | 仅原 API: ['APPLY_PROCCESS', 'APPOVED_IDS', 'APPOVED_NAME', 'BUSINESSAPPROVAL_ID', 'CLOSED_DATE', 'COMPACT_NAME', 'CURRENT_PERIOD', 'CURREVENUE_AMOUNT', 'ENDDATE', 'MONTH_COUNT', 'MONTH_ENDCOUNT', 'MONTH_PROCESSCOUNT', 'NATUREDAY', 'PEND_STATE', 'PERIOD_COUNT', 'PERIOD_ENDCOUNT', 'PERIOD_PROCESSCOUNT', 'PERIOD_STATE', 'PeriodClosed', 'ProjectExit', 'REGISTERCOMPACT_ID', 'REVENUE_AMOUNT', 'SERVERPART_ID', 'SERVERPART_NAME', 'SETTLEMENT_DATE', 'SETTLEMENT_STATE', 'SETTLEMENT_TYPE', 'SHOPEXPENSE_AMOUNT', 'SHOPROYALTY_ID', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_NAME', 'STARTDATE', 'SWITCH_DATE', 'SWITCH_MODES', 'approveSummaryList'] | 仅新 API: ['GUARANTEE_PRICE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (574 vs 10)
- Result_Data.List[0].APPLY_PROCCESS: 新 API 缺少该字段
- Result_Data.List[0].APPOVED_IDS: 新 API 缺少该字段
- Result_Data.List[0].APPOVED_NAME: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSAPPROVAL_ID: 新 API 缺少该字段
- Result_Data.List[0].CLOSED_DATE: 新 API 缺少该字段
- Result_Data.List[0].COMPACT_NAME: 新 API 缺少该字段
- Result_Data.List[0].CURRENT_PERIOD: 新 API 缺少该字段
- Result_Data.List[0].CURREVENUE_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].MONTH_COUNT: 新 API 缺少该字段
- Result_Data.List[0].MONTH_ENDCOUNT: 新 API 缺少该字段
- Result_Data.List[0].MONTH_PROCESSCOUNT: 新 API 缺少该字段
- Result_Data.List[0].NATUREDAY: 新 API 缺少该字段
- Result_Data.List[0].PEND_STATE: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_COUNT: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_ENDCOUNT: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_PROCESSCOUNT: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_STATE: 新 API 缺少该字段
- Result_Data.List[0].PeriodClosed: 新 API 缺少该字段
- Result_Data.List[0].ProjectExit: 新 API 缺少该字段
- Result_Data.List[0].REGISTERCOMPACT_ID: 新 API 缺少该字段
- Result_Data.List[0].REVENUE_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_ID: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_NAME: 新 API 缺少该字段

原 API 状态: `200`，耗时 `1311.83 ms`
新 API 状态: `200`，耗时 `62.94 ms`

### BusinessProject/GetProjectAccountTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetProjectAccountTree | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetProjectAccountTree |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 0 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 1 vs 9999 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ❌ | 仅原 API: ['children', 'node'] | 仅新 API: ['SERVERPART_ID', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_NAME'] |
| 完整响应体 | ❌ | 发现 8 处差异 |

差异明细：
- Result_Data.List[0].children: 新 API 缺少该字段
- Result_Data.List[0].node: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_ID: 新 API 多出该字段
- Result_Data.List[0].SERVERPART_NAME: 新 API 多出该字段
- Result_Data.List[0].SPREGIONTYPE_ID: 新 API 多出该字段
- Result_Data.List[0].SPREGIONTYPE_NAME: 新 API 多出该字段
- Result_Data.PageSize: 值不一致 (1 vs 9999)
- Result_Data.TotalCount: 值不一致 (0 vs 1)

原 API 状态: `200`，耗时 `1091.6 ms`
新 API 状态: `200`，耗时 `11.18 ms`

### BusinessProject/GetRTPaymentRecordDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RTPaymentRecordId": 675}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetRTPaymentRecordDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetRTPaymentRecordDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACCOUNT_AMOUNT', 'ACCOUNT_DATE', 'ACTUAL_PAYMENT', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'MERCHANTS_ID', 'OPERATE_DATE', 'PAYMENTCONFIRM_ID', 'RECORD_DATE', 'RTPAYMENTRECORD_DESC', 'RTPAYMENTRECORD_ID', 'RTPAYMENTRECORD_VALID', 'SEPARATE_AMOUNT', 'SEPARATE_ID', 'SERVERPART_NAME', 'STAFF_NAME'] vs ['OPERATE_DATE', 'PAYMENTCONFIRM_ID', 'RECORD_DATE', 'RTPAYMENTRECORD_DESC', 'RTPAYMENTRECORD_ID', 'RTPAYMENTRECORD_VALID', 'SEPARATE_AMOUNT', 'SEPARATE_ID', 'STAFF_NAME'] |
| 完整响应体 | ❌ | 发现 9 处差异 |

差异明细：
- Result_Data.ACCOUNT_AMOUNT: 新 API 缺少该字段
- Result_Data.ACCOUNT_DATE: 新 API 缺少该字段
- Result_Data.ACTUAL_PAYMENT: 新 API 缺少该字段
- Result_Data.BUSINESSPROJECT_ID: 新 API 缺少该字段
- Result_Data.BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.MERCHANTS_ID: 新 API 缺少该字段
- Result_Data.SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.OPERATE_DATE: 类型不一致 (NoneType vs float)，值为 None vs 20240109.0
- Result_Data.RECORD_DATE: 类型不一致 (NoneType vs str)，值为 None vs '2024/1/9 21:22:22'

原 API 状态: `200`，耗时 `138.95 ms`
新 API 状态: `200`，耗时 `10.73 ms`

### BusinessProject/GetRTPaymentRecordList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 0, "PageSize": 0, "SearchParameter": {"RTPAYMENTRECORD_ID": 675}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetRTPaymentRecordList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetRTPaymentRecordList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败[CODE:-2207]第11 行附近出现错误:
无法解析的成员访问表达式[C.BUSINESSPROJECT_NAME] |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 0, 'PageSize': 0, 'TotalCount': 1, 'List': [{'RTPAYMENTRECORD_ID': 675, 'PAYMENTCONFIRM_ID': 5189, 'SEPARATE_ID': 2700, 'SEPARATE_AMOUNT': 10000.0, 'STAFF_NAME': '安徽驿达管理员', 'OPERATE_DATE': '2024/01/09', 'RECORD_DATE': '2024/1/9 21:22:22', 'RTPAYMENTRECORD_VALID': 1, 'RTPAYMENTRECORD_DESC': '商家缴款1万元【201606】拆分1万元 至 新竹服务区（享当当）项目应收账款【20160613】', 'MERCHANTS_ID': '-1104', 'SERVERPART_NAME': '新竹服务区', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': '新竹服务区（享当当）项目', 'ACCOUNT_AMOUNT': 725000.0, 'ACCOUNT_DATE': '2016/06/13', 'ACTUAL_PAYMENT': 10000.0}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-2207]第11 行附近出现错误:\n无法解析的成员访问表达式[C.BUSINESSPROJECT_NAME]')

原 API 状态: `200`，耗时 `687.11 ms`
新 API 状态: `200`，耗时 `17.39 ms`

### BusinessProject/GetRemarksDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RemarksId": 113}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetRemarksDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetRemarksDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['OPERATE_DATE', 'REMARKS_CONTENT', 'REMARKS_ID', 'REMARKS_STATUS', 'STAFF_ID', 'STAFF_NAME', 'TABLE_ID', 'TABLE_NAME'] vs ['OPERATE_DATE', 'REMARKS_CONTENT', 'REMARKS_ID', 'REMARKS_STATUS', 'STAFF_ID', 'STAFF_NAME', 'TABLE_ID', 'TABLE_NAME'] |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.OPERATE_DATE: 类型不一致 (str vs float)，值为 '2023/05/26 15:52:50' vs 20230526155250.0

原 API 状态: `200`，耗时 `133.24 ms`
新 API 状态: `200`，耗时 `28.33 ms`

### BusinessProject/GetRemarksList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"REMARKS_ID": 113}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetRemarksList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetRemarksList |
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
| 首条字段集合 | ✅ | 字段一致，共 8 个 |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 类型不一致 (str vs float)，值为 '2023/05/26 15:52:50' vs 20230526155250.0

原 API 状态: `200`，耗时 `155.09 ms`
新 API 状态: `200`，耗时 `12.58 ms`

### BusinessProject/GetRevenueConfirmDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RevenueConfirmId": 13849}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetRevenueConfirmDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetRevenueConfirmDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ACTUAL_ACCOUNTS', 'ACTUAL_REVENUE', 'BREACHPENALTY', 'BUSINESSAPPROVAL_ID', 'BUSINESSAPPROVAL_IDS', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESS_BRAND', 'BUSINESS_BRANDS', 'BUSINESS_DAYS', 'BUSINESS_ENDDATE', 'BUSINESS_ENDDATE_End', 'BUSINESS_ENDDATE_Start', 'BUSINESS_MONTH', 'BUSINESS_PERIOD', 'BUSINESS_STARTDATE', 'BUSINESS_STARTDATE_End', 'BUSINESS_STARTDATE_Start', 'BUSINESS_TRADE', 'BUSINESS_TRADES', 'CASHPAY_AMOUNT', 'CORRECT_AMOUNT', 'EARLY_SETTLEMENT', 'ELECTRICITYCHARGE', 'GUARANTEERATIO', 'GUARANTEE_AMOUNT', 'HOUSERENT', 'LIQUIDATION_AMOUNT', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MOBILEPAY_AMOUNT', 'OTHERFEE', 'OTHERPAY_AMOUNT', 'PAID_AMOUNT', 'PARTYA_SHAREPROFIT', 'PARTYB_SHAREPROFIT', 'PARTYC_SHAREPROFIT', 'PERIOD_INDEX', 'PROPERTYFEE', 'REDUCTION_AMOUNT', 'REVENUECONFIRM_DESC', 'REVENUECONFIRM_ID', 'REVENUE_VALID', 'ROYALTY_PRICE', 'SERVERPARTSHOP_ID', 'SHOPROYALTY_ID', 'SHOPROYALTY_IDS', 'SUBROYALTY_PRICE', 'WATERCHARGE'] vs ['ACTUAL_ACCOUNTS', 'ACTUAL_REVENUE', 'BREACHPENALTY', 'BUSINESSAPPROVAL_ID', 'BUSINESSPROJECT_ID', 'BUSINESS_BRAND', 'BUSINESS_DAYS', 'BUSINESS_ENDDATE', 'BUSINESS_MONTH', 'BUSINESS_PERIOD', 'BUSINESS_STARTDATE', 'BUSINESS_TRADE', 'CASHPAY_AMOUNT', 'CORRECT_AMOUNT', 'EARLY_SETTLEMENT', 'ELECTRICITYCHARGE', 'GUARANTEERATIO', 'GUARANTEE_AMOUNT', 'HOUSERENT', 'LIQUIDATION_AMOUNT', 'MOBILEPAY_AMOUNT', 'OTHERFEE', 'OTHERPAY_AMOUNT', 'PAID_AMOUNT', 'PARTYA_SHAREPROFIT', 'PARTYB_SHAREPROFIT', 'PARTYC_SHAREPROFIT', 'PERIOD_INDEX', 'PROPERTYFEE', 'REDUCTION_AMOUNT', 'REVENUECONFIRM_DESC', 'REVENUECONFIRM_ID', 'REVENUE_VALID', 'ROYALTY_PRICE', 'SERVERPARTSHOP_ID', 'SHOPROYALTY_ID', 'SUBROYALTY_PRICE', 'WATERCHARGE'] |
| 完整响应体 | ❌ | 发现 12 处差异 |

差异明细：
- Result_Data.BUSINESSAPPROVAL_IDS: 新 API 缺少该字段
- Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.BUSINESS_BRANDS: 新 API 缺少该字段
- Result_Data.BUSINESS_ENDDATE_End: 新 API 缺少该字段
- Result_Data.BUSINESS_ENDDATE_Start: 新 API 缺少该字段
- Result_Data.BUSINESS_STARTDATE_End: 新 API 缺少该字段
- Result_Data.BUSINESS_STARTDATE_Start: 新 API 缺少该字段
- Result_Data.BUSINESS_TRADES: 新 API 缺少该字段
- Result_Data.MERCHANTS_ID: 新 API 缺少该字段
- Result_Data.MERCHANTS_NAME: 新 API 缺少该字段
- Result_Data.SHOPROYALTY_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `107.65 ms`
新 API 状态: `200`，耗时 `13.78 ms`

### BusinessProject/GetRevenueConfirmList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetRevenueConfirmList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetRevenueConfirmList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 74 vs 74 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 74 vs 74 |
| List 条数 | ✅ | 74 vs 74 |
| 首条字段集合 | ❌ | 仅原 API: ['BREACHPENALTY', 'BUSINESSAPPROVAL_ID', 'BUSINESSAPPROVAL_IDS', 'BUSINESSPROJECT_IDS', 'BUSINESS_BRAND', 'BUSINESS_BRANDS', 'BUSINESS_ENDDATE_End', 'BUSINESS_ENDDATE_Start', 'BUSINESS_PERIOD', 'BUSINESS_STARTDATE_End', 'BUSINESS_STARTDATE_Start', 'BUSINESS_TRADE', 'BUSINESS_TRADES', 'CASHPAY_AMOUNT', 'EARLY_SETTLEMENT', 'ELECTRICITYCHARGE', 'HOUSERENT', 'MOBILEPAY_AMOUNT', 'OTHERFEE', 'OTHERPAY_AMOUNT', 'PAID_AMOUNT', 'PERIOD_INDEX', 'PROPERTYFEE', 'ROYALTY_PRICE', 'SHOPROYALTY_IDS', 'SUBROYALTY_PRICE', 'WATERCHARGE'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BREACHPENALTY: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSAPPROVAL_ID: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSAPPROVAL_IDS: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_BRAND: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_BRANDS: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_ENDDATE_End: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_ENDDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_PERIOD: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STARTDATE_End: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_STARTDATE_Start: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADE: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADES: 新 API 缺少该字段
- Result_Data.List[0].CASHPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].EARLY_SETTLEMENT: 新 API 缺少该字段
- Result_Data.List[0].ELECTRICITYCHARGE: 新 API 缺少该字段
- Result_Data.List[0].HOUSERENT: 新 API 缺少该字段
- Result_Data.List[0].MOBILEPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].OTHERFEE: 新 API 缺少该字段
- Result_Data.List[0].OTHERPAY_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].PAID_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].PERIOD_INDEX: 新 API 缺少该字段
- Result_Data.List[0].PROPERTYFEE: 新 API 缺少该字段
- Result_Data.List[0].ROYALTY_PRICE: 新 API 缺少该字段
- Result_Data.List[0].SHOPROYALTY_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `184.2 ms`
新 API 状态: `200`，耗时 `27.3 ms`

### BusinessProject/GetSHOPEXPENSEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SHOPEXPENSEId": 21018}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetSHOPEXPENSEDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetSHOPEXPENSEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ApprovalProcess', 'BUSINESS_UNIT', 'ChangeFlag', 'ImageFlag', 'MERCHANTS_ID', 'OPERATE_DATE', 'PAY_STATUS', 'PREPAIDLAST_AMOUNT', 'PREPAID_AMOUNT', 'PROVINCE_CODE', 'RevenueAmount', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SHOPEXPENSE_AMOUNT', 'SHOPEXPENSE_DESC', 'SHOPEXPENSE_ID', 'SHOPEXPENSE_STATE', 'SHOPEXPENSE_TYPE', 'SPREGIONTYPE_IDS', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'ShowRevenue', 'notExist'] vs ['BUSINESSPROJECT_ID', 'BUSINESS_UNIT', 'MERCHANTS_ID', 'OPERATE_DATE', 'PAY_STATUS', 'PERIOD_INDEX', 'PROVINCE_CODE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SHOPEXPENSE_AMOUNT', 'SHOPEXPENSE_DESC', 'SHOPEXPENSE_ID', 'SHOPEXPENSE_STATE', 'SHOPEXPENSE_TYPE', 'SHOPROYALTY_ID', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_MONTH'] |
| 完整响应体 | ❌ | 发现 17 处差异 |

差异明细：
- Result_Data.ApprovalProcess: 新 API 缺少该字段
- Result_Data.ChangeFlag: 新 API 缺少该字段
- Result_Data.ImageFlag: 新 API 缺少该字段
- Result_Data.PREPAIDLAST_AMOUNT: 新 API 缺少该字段
- Result_Data.PREPAID_AMOUNT: 新 API 缺少该字段
- Result_Data.RevenueAmount: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.SPREGIONTYPE_IDS: 新 API 缺少该字段
- Result_Data.STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.ShowRevenue: 新 API 缺少该字段
- Result_Data.notExist: 新 API 缺少该字段
- Result_Data.BUSINESSPROJECT_ID: 新 API 多出该字段
- Result_Data.PERIOD_INDEX: 新 API 多出该字段
- Result_Data.SHOPROYALTY_ID: 新 API 多出该字段
- Result_Data.OPERATE_DATE: 值不一致 ('2024-07-12T16:43:08' vs '2024/7/12 16:43:08')

原 API 状态: `200`，耗时 `148.18 ms`
新 API 状态: `200`，耗时 `9.98 ms`

### BusinessProject/GetSHOPEXPENSEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetSHOPEXPENSEList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetSHOPEXPENSEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'OtherData', 'PageIndex', 'PageSize', 'TotalCount', 'summaryObject'] |
| TotalCount | ✅ | 723 vs 723 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| OtherData 存在性 | ✅ | True vs True |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['ApprovalProcess', 'ChangeFlag', 'ImageFlag', 'PREPAIDLAST_AMOUNT', 'PREPAID_AMOUNT', 'RevenueAmount', 'SERVERPARTSHOP_IDS', 'SERVERPART_IDS', 'SPREGIONTYPE_IDS', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'ShowRevenue', 'notExist'] | 仅新 API: ['BUSINESSPROJECT_ID', 'PERIOD_INDEX', 'SHOPROYALTY_ID'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.summaryObject: 新 API 多出该字段
- Result_Data.List[0].ApprovalProcess: 新 API 缺少该字段
- Result_Data.List[0].ChangeFlag: 新 API 缺少该字段
- Result_Data.List[0].ImageFlag: 新 API 缺少该字段
- Result_Data.List[0].PREPAIDLAST_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].PREPAID_AMOUNT: 新 API 缺少该字段
- Result_Data.List[0].RevenueAmount: 新 API 缺少该字段
- Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].SPREGIONTYPE_IDS: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_MONTH_End: 新 API 缺少该字段
- Result_Data.List[0].STATISTICS_MONTH_Start: 新 API 缺少该字段
- Result_Data.List[0].ShowRevenue: 新 API 缺少该字段
- Result_Data.List[0].notExist: 新 API 缺少该字段
- Result_Data.List[0].BUSINESSPROJECT_ID: 新 API 多出该字段
- Result_Data.List[0].PERIOD_INDEX: 新 API 多出该字段
- Result_Data.List[0].SHOPROYALTY_ID: 新 API 多出该字段
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024-07-12T16:43:08' vs '2024/7/12 16:43:08')
- Result_Data.List[1].ApprovalProcess: 新 API 缺少该字段
- Result_Data.List[1].ChangeFlag: 新 API 缺少该字段
- Result_Data.List[1].ImageFlag: 新 API 缺少该字段
- Result_Data.List[1].PREPAIDLAST_AMOUNT: 新 API 缺少该字段
- Result_Data.List[1].PREPAID_AMOUNT: 新 API 缺少该字段
- Result_Data.List[1].RevenueAmount: 新 API 缺少该字段
- Result_Data.List[1].SERVERPARTSHOP_IDS: 新 API 缺少该字段

原 API 状态: `200`，耗时 `184.13 ms`
新 API 状态: `200`，耗时 `28.74 ms`

### BusinessProject/GetSHOPROYALTYDETAILDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SHOPROYALTYDETAILId": 92}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetSHOPROYALTYDETAILDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetSHOPROYALTYDETAILDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BUSINESSPROJECT_ID', 'DAILY_AMOUNT', 'GUARANTEERATIO', 'MINTURNOVER', 'OPERATE_DATE', 'REGISTERCOMPACT_ID', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SHOPROYALTYDETAIL_ID', 'SHOPROYALTYDETAIL_STATE', 'SHOPROYALTY_ID'] vs ['BUSINESSPROJECT_ID', 'DAILY_AMOUNT', 'GUARANTEERATIO', 'MINTURNOVER', 'OPERATE_DATE', 'REGISTERCOMPACT_ID', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SHOPROYALTYDETAIL_ID', 'SHOPROYALTYDETAIL_STATE', 'SHOPROYALTY_ID'] |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.OPERATE_DATE: 值不一致 ('2023-11-23T16:49:52' vs '2023/11/23 16:49:52')

原 API 状态: `200`，耗时 `149.17 ms`
新 API 状态: `200`，耗时 `56.38 ms`

### BusinessProject/GetSHOPROYALTYDETAILList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SHOPROYALTYDETAIL_ID": 92}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetSHOPROYALTYDETAILList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetSHOPROYALTYDETAILList |
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
| 首条字段集合 | ✅ | 字段一致，共 11 个 |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2023-11-23T16:49:52' vs '2023/11/23 16:49:52')

原 API 状态: `200`，耗时 `134.84 ms`
新 API 状态: `200`，耗时 `16.78 ms`

### BusinessProject/GetShopExpenseSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"serverpartshop_id": 3080, "statistics_month_end": "2025-12-31", "statistics_month_start": "2025-12-31"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetShopExpenseSummary | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetShopExpenseSummary |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ❌ | 10 vs 9999 |
| List 条数 | ❌ | 1 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 0)
- Result_Data.PageSize: 值不一致 (10 vs 9999)
- Result_Data.TotalCount: 值不一致 (1 vs 0)

原 API 状态: `200`，耗时 `262.75 ms`
新 API 状态: `200`，耗时 `28.21 ms`

### BusinessProject/GetShopRoyaltyDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ShopRoyaltyId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetShopRoyaltyDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetShopRoyaltyDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'DAILY_AMOUNT', 'ENDDATE', 'EXCESSRATIO', 'EXPENSE_AMOUNT', 'EXPENSE_NAME', 'EXPENSE_TYPE', 'FEWTHYEAR', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MINTURNOVER', 'NATUREDAY', 'PROPERTY_FEE', 'REGISTERCOMPACT_ID', 'RENTFEE', 'SEPARATE_STATE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'SHOPROYALTY_ID', 'SHOPROYALTY_STATE', 'SMOKERATIO', 'STARTDATE'] vs ['BUSINESSPROJECT_ID', 'BUSINESS_TYPE', 'DAILY_AMOUNT', 'ENDDATE', 'EXCESSRATIO', 'EXPENSE_AMOUNT', 'EXPENSE_NAME', 'EXPENSE_TYPE', 'FEWTHYEAR', 'GUARANTEERATIO', 'MERCHANTS_ID', 'MINTURNOVER', 'NATUREDAY', 'PROPERTY_FEE', 'REGISTERCOMPACT_ID', 'RENTFEE', 'SEPARATE_STATE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'SHOPROYALTY_ID', 'SHOPROYALTY_STATE', 'SMOKERATIO', 'STARTDATE'] |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.ENDDATE: 值不一致 ('2020-07-11T00:00:00' vs '2020/7/11 0:00:00')
- Result_Data.STARTDATE: 值不一致 ('2020-01-12T00:00:00' vs '2020/1/12 0:00:00')

原 API 状态: `200`，耗时 `161.59 ms`
新 API 状态: `200`，耗时 `17.47 ms`

### BusinessProject/GetShopRoyaltyList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SHOPROYALTY_ID": 1}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetShopRoyaltyList | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetShopRoyaltyList |
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
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List[0].ENDDATE: 值不一致 ('2020-07-11T00:00:00' vs '2020/7/11 0:00:00')
- Result_Data.List[0].STARTDATE: 值不一致 ('2020-01-12T00:00:00' vs '2020/1/12 0:00:00')

原 API 状态: `200`，耗时 `85.71 ms`
新 API 状态: `200`，耗时 `12.67 ms`

### BusinessProject/GetWillSettleProject / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"EndDate": "2025-12-31", "ServerpartId": 416, "StartDate": "2025-01-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessProject/GetWillSettleProject | 新 API: http://localhost:8080/EShangApiMain/BusinessProject/GetWillSettleProject |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败[CODE:-6130]文字与格式字符串不匹配 |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 6, 'TotalCount': 6, 'List': [{'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'REGISTERCOMPACT_ID': 281, 'COMPACT_NAME': '驿达公司新桥服务区麦当劳项目', 'SPREGIONTYPE_ID': '72', 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': '416', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_NAME': '麦当劳', 'MERCHANTS_ID': -580, 'MERCHANTS_NAME': '安徽联升餐厅食品有限公司', 'CURRENT_PERIOD': '第7期', 'SHOPROYALTY_ID': 2944, 'STARTDATE': '2024/2/1', 'ENDDATE': '2025/1/31', 'PROJECT_STARTDATE': '2018/2/1', 'PROJECT_ENDDATE': '2028/1/31', 'NATUREDAY': 1.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 9999, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': None, 'CURREVENUE_AMOUNT': None, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2025/1/31', 'SETTLEMENT_TYPE': 2, 'SETTLEMENT_STATE': None, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': None, 'APPOVED_IDS': None, 'APPOVED_NAME': None, 'PEND_STATE': None, 'APPLY_PROCCESS': None, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None}, {'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'REGISTERCOMPACT_ID': 1543, 'COMPACT_NAME': '新桥服务区丁家馄饨合同项目', 'SPREGIONTYPE_ID': '72', 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': '416', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_NAME': '丁家馄饨', 'MERCHANTS_ID': -2114, 'MERCHANTS_NAME': '淮南丁家餐饮有限公司', 'CURRENT_PERIOD': '第1期', 'SHOPROYALTY_ID': 4093, 'STARTDATE': '2024/2/1', 'ENDDATE': '2025/3/2', 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'NATUREDAY': 1.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': None, 'CURREVENUE_AMOUNT': None, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2025/3/2', 'SETTLEMENT_TYPE': 1, 'SETTLEMENT_STATE': None, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': None, 'APPOVED_IDS': None, 'APPOVED_NAME': None, 'PEND_STATE': None, 'APPLY_PROCCESS': None, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None}, {'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_NAME': '新桥服务区烧饼合同项目', 'REGISTERCOMPACT_ID': 1549, 'COMPACT_NAME': '新桥服务区烧饼合同项目', 'SPREGIONTYPE_ID': '72', 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': '416', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_NAME': '下塘烧饼', 'MERCHANTS_ID': -2117, 'MERCHANTS_NAME': '合肥徽蕴堂餐饮管理有限责任公司', 'CURRENT_PERIOD': '第1期', 'SHOPROYALTY_ID': 4105, 'STARTDATE': '2024/2/1', 'ENDDATE': '2025/3/2', 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'NATUREDAY': 1.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': None, 'CURREVENUE_AMOUNT': None, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2025/3/2', 'SETTLEMENT_TYPE': 1, 'SETTLEMENT_STATE': None, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': None, 'APPOVED_IDS': None, 'APPOVED_NAME': None, 'PEND_STATE': None, 'APPLY_PROCCESS': None, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None}, {'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'REGISTERCOMPACT_ID': 1547, 'COMPACT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'SPREGIONTYPE_ID': '72', 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': '416', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'MERCHANTS_ID': -2116, 'MERCHANTS_NAME': '合肥书山有陆餐饮管理有限公司', 'CURRENT_PERIOD': '第1期', 'SHOPROYALTY_ID': 4101, 'STARTDATE': '2024/2/1', 'ENDDATE': '2025/3/2', 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'NATUREDAY': 1.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': None, 'CURREVENUE_AMOUNT': None, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2025/3/2', 'SETTLEMENT_TYPE': 1, 'SETTLEMENT_STATE': None, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': None, 'APPOVED_IDS': None, 'APPOVED_NAME': None, 'PEND_STATE': None, 'APPLY_PROCCESS': None, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None}, {'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'REGISTERCOMPACT_ID': 1551, 'COMPACT_NAME': '新桥服务区王仁和米线店新店合同项目', 'SPREGIONTYPE_ID': '72', 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': '416', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_NAME': '王仁和米线店', 'MERCHANTS_ID': -1116, 'MERCHANTS_NAME': '合肥王仁和米线餐饮管理有限公司', 'CURRENT_PERIOD': '第1期', 'SHOPROYALTY_ID': 4109, 'STARTDATE': '2024/2/1', 'ENDDATE': '2025/2/14', 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/2/14', 'NATUREDAY': 1.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': None, 'CURREVENUE_AMOUNT': None, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2025/2/14', 'SETTLEMENT_TYPE': 1, 'SETTLEMENT_STATE': None, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': None, 'APPOVED_IDS': None, 'APPOVED_NAME': None, 'PEND_STATE': None, 'APPLY_PROCCESS': None, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None}, {'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'REGISTERCOMPACT_ID': 1545, 'COMPACT_NAME': '新桥三河米饺合同项目', 'SPREGIONTYPE_ID': '72', 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': '416', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_NAME': '丁记米饺', 'MERCHANTS_ID': -2115, 'MERCHANTS_NAME': '合肥市丁记米饺食品有限公司', 'CURRENT_PERIOD': '第1期', 'SHOPROYALTY_ID': 4097, 'STARTDATE': '2024/2/1', 'ENDDATE': '2025/3/2', 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'NATUREDAY': 1.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'CLOSED_DATE': None, 'SWITCH_DATE': None, 'SWITCH_MODES': None, 'REVENUE_AMOUNT': None, 'CURREVENUE_AMOUNT': None, 'SHOPEXPENSE_AMOUNT': None, 'SETTLEMENT_DATE': '2025/3/2', 'SETTLEMENT_TYPE': 1, 'SETTLEMENT_STATE': None, 'PERIOD_STATE': 1, 'BUSINESSAPPROVAL_ID': None, 'APPOVED_IDS': None, 'APPOVED_NAME': None, 'PEND_STATE': None, 'APPLY_PROCCESS': None, 'PERIOD_COUNT': None, 'MONTH_COUNT': None, 'PERIOD_PROCESSCOUNT': None, 'MONTH_PROCESSCOUNT': None, 'PERIOD_ENDCOUNT': None, 'MONTH_ENDCOUNT': None, 'PeriodClosed': False, 'ProjectExit': False, 'approveSummaryList': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-6130]文字与格式字符串不匹配')

原 API 状态: `200`，耗时 `166.68 ms`
新 API 状态: `200`，耗时 `12.63 ms`

### Contract/GetAttachmentDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AttachmentId": 1903}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetAttachmentDetail | 新 API: http://localhost:8080/EShangApiMain/Contract/GetAttachmentDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ATTACHMENT_ID', 'ATTACHMENT_NAME', 'ATTACHMENT_PATH', 'ATTACHMENT_URL', 'OPERATE_DATE', 'STAFF_ID', 'STAFF_NAME', 'TABLE_ID', 'TABLE_NAME'] vs ['ATTACHMENT_ID', 'ATTACHMENT_NAME', 'ATTACHMENT_PATH', 'ATTACHMENT_URL', 'OPERATE_DATE', 'STAFF_ID', 'STAFF_NAME', 'TABLE_ID', 'TABLE_NAME'] |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.OPERATE_DATE: 类型不一致 (int vs float)，值为 20240117110440 vs 20240117110440.0
- Result_Data.STAFF_NAME: 类型不一致 (NoneType vs str)，值为 None vs ''

原 API 状态: `200`，耗时 `164.55 ms`
新 API 状态: `200`，耗时 `29.15 ms`

### Contract/GetAttachmentList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"ATTACHMENT_ID": 1903}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetAttachmentList | 新 API: http://localhost:8080/EShangApiMain/Contract/GetAttachmentList |
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
| 首条字段集合 | ✅ | 字段一致，共 9 个 |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 类型不一致 (int vs float)，值为 20240117110440 vs 20240117110440.0

原 API 状态: `200`，耗时 `88.63 ms`
新 API 状态: `200`，耗时 `18.34 ms`

### Contract/GetContractExpiredInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetContractExpiredInfo | 新 API: http://localhost:8080/EShangApiMain/Contract/GetContractExpiredInfo |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['Complete_Degree', 'ContractHalfYearListExpired', 'Expired_Amount', 'Expired_HalfYearCount', 'Paid_Amount', 'Total_Amount', 'UnExpired_Amount', 'UnPaid_Amount'] vs ['Complete_Degree', 'ContractHalfYearListExpired', 'Expired_Amount', 'Expired_HalfYearCount', 'Paid_Amount', 'Total_Amount', 'UnExpired_Amount', 'UnPaid_Amount'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `229.34 ms`
新 API 状态: `200`，耗时 `104.69 ms`

### Contract/GetProjectMonthlyArrearageList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "StatisticsYear": 2025}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetProjectMonthlyArrearageList | 新 API: http://localhost:8080/EShangApiMain/Contract/GetProjectMonthlyArrearageList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ProjectCompleteDetailList', 'ProjectMonthlyCompleteList', 'ProjectMonthlyUnpaidList'] vs ['ProjectCompleteDetailList', 'ProjectMonthlyCompleteList', 'ProjectMonthlyUnpaidList'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.ProjectCompleteDetailList: 列表长度不一致 (5 vs 0)
- Result_Data.ProjectMonthlyCompleteList[0].Business_Year: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[0].Expired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[0].UnExpired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[1].Expired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[1].UnExpired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[1].Account_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[1].Complete_Degree: 类型不一致 (float vs int)，值为 100.0 vs 100
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[1].Payment_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[2].Expired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[2].UnExpired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[2].Account_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[2].Complete_Degree: 类型不一致 (float vs int)，值为 100.0 vs 100
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[2].Payment_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[3].Expired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[3].UnExpired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[3].Account_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[3].Complete_Degree: 类型不一致 (float vs int)，值为 100.0 vs 100
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[3].Payment_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[4].Expired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[4].UnExpired_Amount: 新 API 缺少该字段
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[4].Account_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[4].Complete_Degree: 类型不一致 (float vs int)，值为 100.0 vs 100
- Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[4].Payment_Amount: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.ProjectMonthlyCompleteList[1].Business_Year: 新 API 缺少该字段

原 API 状态: `200`，耗时 `233.57 ms`
新 API 状态: `200`，耗时 `53.46 ms`

### Contract/GetProjectSummaryInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetProjectSummaryInfo | 新 API: http://localhost:8080/EShangApiMain/Contract/GetProjectSummaryInfo |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ArrearageContract_Count', 'ArrearageList', 'ArrearageMerchant_Count', 'Arrearage_Amount', 'BusinessTypeSummaryList', 'Contract_Amount', 'Contract_SignCount', 'Contractor_Count', 'NewlyAccount_Amount', 'NewlyContract_Amount', 'NewlyContract_Count'] vs ['ArrearageContract_Count', 'ArrearageList', 'ArrearageMerchant_Count', 'Arrearage_Amount', 'BusinessTypeSummaryList', 'Contract_Amount', 'Contract_SignCount', 'Contractor_Count', 'NewlyAccount_Amount', 'NewlyContract_Amount', 'NewlyContract_Count'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `261.51 ms`
新 API 状态: `200`，耗时 `61.75 ms`

### Contract/GetProjectYearlyArrearageList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetProjectYearlyArrearageList | 新 API: http://localhost:8080/EShangApiMain/Contract/GetProjectYearlyArrearageList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ProjectCompleteDetailList', 'ProjectMonthlyCompleteList', 'ProjectMonthlyUnpaidList'] vs ['ProjectCompleteDetailList', 'ProjectMonthlyCompleteList', 'ProjectMonthlyUnpaidList'] |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data.ProjectCompleteDetailList: 列表长度不一致 (5 vs 0)

原 API 状态: `200`，耗时 `196.69 ms`
新 API 状态: `200`，耗时 `54.64 ms`

### Contract/GetRTRegisterCompactDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RTRegisterCompactId": 12426, "RegisterCompactId": 466}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetRTRegisterCompactDetail | 新 API: http://localhost:8080/EShangApiMain/Contract/GetRTRegisterCompactDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['PROVINCE_CODE', 'REGISTERCOMPACT_ID', 'RTREGISTERCOMPACT_ID', 'SERVERPART_ID'] vs ['PROVINCE_CODE', 'REGISTERCOMPACT_ID', 'RTREGISTERCOMPACT_ID', 'SERVERPART_ID'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `120.55 ms`
新 API 状态: `200`，耗时 `28.25 ms`

### Contract/GetRTRegisterCompactList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetRTRegisterCompactList | 新 API: http://localhost:8080/EShangApiMain/Contract/GetRTRegisterCompactList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 2112 vs 2112 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 4 个 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `159.53 ms`
新 API 状态: `200`，耗时 `22.0 ms`

### Contract/GetRegisterCompactDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RegisterCompactId": 21}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetRegisterCompactDetail | 新 API: http://localhost:8080/EShangApiMain/Contract/GetRegisterCompactDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['ATTACHMENT_STATE', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'CLOSED_DATE', 'COMPACT_ACCOUNTDATE', 'COMPACT_AMOUNT', 'COMPACT_CHILDTYPE', 'COMPACT_CODE', 'COMPACT_DESC', 'COMPACT_DETAILS', 'COMPACT_ENDDATE', 'COMPACT_NAME', 'COMPACT_STARTDATE', 'COMPACT_STATE', 'COMPACT_TYPE', 'DURATION', 'DURATIONDAY', 'ELECTRICITY_FEES', 'EQUIPMENT_DEPOSIT', 'FIRSTPART_ID', 'FIRSTPART_LINKMAN', 'FIRSTPART_MOBILE', 'FIRSTPART_NAME', 'FIRSTYEAR_RENT', 'GUARANTEE_RATIO', 'LogList', 'OPERATE_DATE', 'OPERATING_AREA', 'ORGANIZER', 'ORGANIZER_LINKMAN', 'ORGANIZER_TEL', 'OTHER_SCHARGE', 'PROINSTCOMPACT_ID', 'PROPERTY_FEE', 'REGISTERCOMPACT_HOSTID', 'REGISTERCOMPACT_ID', 'RELATE_COMPACT', 'RENEWAL_YEARS', 'SAFETYRISKMORTGAGE', 'SAFETYRISKMORTGAGE_ENDDATE', 'SAFETYRISKMORTGAGE_STARTDATE', 'SECONDPART_ID', 'SECONDPART_LINKMAN', 'SECONDPART_MOBILE', 'SECONDPART_NAME', 'SECURITYDEPOSIT', 'SECURITYDEPOSIT_ENDDATE', 'SECURITYDEPOSIT_STARTDATE', 'SERVERPARTSHOP_IDS', 'SERVERPARTSHOP_NAME', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SERVERPART_TYPE', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'STAFF_ID', 'STAFF_NAME', 'THREEPART_ID', 'THREEPART_LINKMAN', 'THREEPART_MOBILE', 'THREEPART_NAME', 'WATER_CHARGE'] vs ['ATTACHMENT_STATE', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'COMPACT_ACCOUNTDATE', 'COMPACT_AMOUNT', 'COMPACT_CHILDTYPE', 'COMPACT_CODE', 'COMPACT_DESC', 'COMPACT_DETAILS', 'COMPACT_ENDDATE', 'COMPACT_NAME', 'COMPACT_STARTDATE', 'COMPACT_STATE', 'COMPACT_TYPE', 'DURATION', 'DURATIONDAY', 'ELECTRICITY_FEES', 'EQUIPMENT_DEPOSIT', 'FIRSTPART_ID', 'FIRSTPART_LINKMAN', 'FIRSTPART_MOBILE', 'FIRSTPART_NAME', 'FIRSTYEAR_RENT', 'GUARANTEE_RATIO', 'LogList', 'OPERATE_DATE', 'OPERATING_AREA', 'ORGANIZER', 'ORGANIZER_LINKMAN', 'ORGANIZER_TEL', 'OTHER_SCHARGE', 'PROINSTCOMPACT_ID', 'PROPERTY_FEE', 'REGISTERCOMPACT_HOSTID', 'REGISTERCOMPACT_ID', 'RENEWAL_YEARS', 'SAFETYRISKMORTGAGE', 'SAFETYRISKMORTGAGE_ENDDATE', 'SAFETYRISKMORTGAGE_STARTDATE', 'SECONDPART_ID', 'SECONDPART_LINKMAN', 'SECONDPART_MOBILE', 'SECONDPART_NAME', 'SECURITYDEPOSIT', 'SECURITYDEPOSIT_ENDDATE', 'SECURITYDEPOSIT_STARTDATE', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SERVERPART_TYPE', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'STAFF_ID', 'STAFF_NAME', 'THREEPART_ID', 'THREEPART_LINKMAN', 'THREEPART_MOBILE', 'THREEPART_NAME', 'WATER_CHARGE'] |
| 完整响应体 | ❌ | 发现 23 处差异 |

差异明细：
- Result_Data.CLOSED_DATE: 新 API 缺少该字段
- Result_Data.RELATE_COMPACT: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.SERVERPARTSHOP_NAME: 新 API 缺少该字段
- Result_Data.BUSINESS_TRADE: 类型不一致 (NoneType vs int)，值为 None vs 2
- Result_Data.BUSINESS_TYPE: 类型不一致 (NoneType vs int)，值为 None vs 2000
- Result_Data.COMPACT_ACCOUNTDATE: 值不一致 ('2021-09-24T00:00:00' vs '2021/9/24 0:00:00')
- Result_Data.COMPACT_CHILDTYPE: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.COMPACT_ENDDATE: 值不一致 ('2025-02-15T00:00:00' vs '2025/2/15 0:00:00')
- Result_Data.COMPACT_STARTDATE: 值不一致 ('2024-09-29T00:00:00' vs '2024/9/29 0:00:00')
- Result_Data.DURATIONDAY: 类型不一致 (int vs float)，值为 139 vs 139.0
- Result_Data.LogList: 类型不一致 (NoneType vs list)，值为 None vs []
- Result_Data.OPERATE_DATE: 值不一致 ('2023-11-09T14:03:24' vs '2023/11/9 14:03:24')
- Result_Data.OPERATING_AREA: 类型不一致 (NoneType vs float)，值为 None vs 64.0
- Result_Data.OTHER_SCHARGE: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.PROPERTY_FEE: 类型不一致 (NoneType vs float)，值为 None vs 1600.0
- Result_Data.SAFETYRISKMORTGAGE_ENDDATE: 值不一致 ('2024-10-03T00:00:00' vs '2024/10/3 0:00:00')
- Result_Data.SAFETYRISKMORTGAGE_STARTDATE: 值不一致 ('2021-09-24T00:00:00' vs '2021/9/24 0:00:00')
- Result_Data.SECURITYDEPOSIT_ENDDATE: 值不一致 ('2025-03-28T00:00:00' vs '2025/3/28 0:00:00')
- Result_Data.SECURITYDEPOSIT_STARTDATE: 值不一致 ('2021-09-24T00:00:00' vs '2021/9/24 0:00:00')
- Result_Data.SERVERPART_TYPE: 类型不一致 (NoneType vs int)，值为 None vs 2000
- Result_Data.SETTLEMENT_CYCLE: 类型不一致 (NoneType vs int)，值为 None vs 3000
- Result_Data.SETTLEMENT_MODES: 类型不一致 (NoneType vs int)，值为 None vs 1000

原 API 状态: `200`，耗时 `338.37 ms`
新 API 状态: `200`，耗时 `40.65 ms`

### Contract/GetRegisterCompactList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetRegisterCompactList | 新 API: http://localhost:8080/EShangApiMain/Contract/GetRegisterCompactList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 41 vs 41 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ❌ | 仅原 API: ['LogList', 'RENEWAL_YEARS'] | 仅新 API: [] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].LogList: 新 API 缺少该字段
- Result_Data.List[0].RENEWAL_YEARS: 新 API 缺少该字段
- Result_Data.List[0].BUSINESS_TRADE: 类型不一致 (int vs NoneType)，值为 4 vs None
- Result_Data.List[0].COMPACT_ENDDATE: 值不一致 ('2028-07-14T00:00:00' vs '2028/7/14 0:00:00')
- Result_Data.List[0].COMPACT_STARTDATE: 值不一致 ('2025-07-15T00:00:00' vs '2025/7/15 0:00:00')
- Result_Data.List[0].DURATIONDAY: 类型不一致 (int vs float)，值为 1095 vs 1095.0
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2025-11-18T17:46:05' vs '2025/11/18 17:46:05')
- Result_Data.List[0].OTHER_SCHARGE: 类型不一致 (str vs NoneType)，值为 '' vs None
- Result_Data.List[0].PROPERTY_FEE: 类型不一致 (float vs NoneType)，值为 0.0 vs None
- Result_Data.List[0].RELATE_COMPACT: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[0].SERVERPARTSHOP_NAME: 类型不一致 (str vs NoneType)，值为 '南区自助玩具机,北区自助玩具机' vs None
- Result_Data.List[1].LogList: 新 API 缺少该字段
- Result_Data.List[1].RENEWAL_YEARS: 新 API 缺少该字段
- Result_Data.List[1].BUSINESS_TRADE: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[1].OPERATE_DATE: 值不一致 ('2025-09-05T16:09:05' vs '2025/9/5 16:09:05')
- Result_Data.List[1].OTHER_SCHARGE: 类型不一致 (str vs NoneType)，值为 '' vs None
- Result_Data.List[1].PROPERTY_FEE: 类型不一致 (float vs NoneType)，值为 0.0 vs None
- Result_Data.List[1].RELATE_COMPACT: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[2].LogList: 新 API 缺少该字段
- Result_Data.List[2].RENEWAL_YEARS: 新 API 缺少该字段
- Result_Data.List[2].BUSINESS_TRADE: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[2].OPERATE_DATE: 值不一致 ('2025-09-05T16:04:33' vs '2025/9/5 16:04:33')
- Result_Data.List[2].OTHER_SCHARGE: 类型不一致 (str vs NoneType)，值为 '' vs None
- Result_Data.List[2].PROPERTY_FEE: 类型不一致 (float vs NoneType)，值为 0.0 vs None
- Result_Data.List[2].RELATE_COMPACT: 类型不一致 (int vs NoneType)，值为 0 vs None

原 API 状态: `200`，耗时 `116.53 ms`
新 API 状态: `200`，耗时 `28.23 ms`

### Contract/GetRegisterCompactSubDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RegisterCompactId": 731, "RegisterCompactSubId": 737}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetRegisterCompactSubDetail | 新 API: http://localhost:8080/EShangApiMain/Contract/GetRegisterCompactSubDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BRAND_NAME', 'BUSINESS_BRAND', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'COMPACT_BASIS', 'COMPACT_CHILDTYPE', 'COMPACT_DPDESC', 'DECORATE_ENDDATE', 'DECORATE_STARTDATE', 'ELECTRICITY_FEES', 'EQUIPMENT_DEPOSIT', 'FIRSTYEAR_RENT', 'GUARANTEE_RATIO', 'OPERATING_AREA', 'OPERATING_SCOPE', 'OPERATING_SITE', 'OTHER_SCHARGE', 'PROPERTY_FEE', 'REGISTERCOMPACTSUB_ID', 'REGISTERCOMPACT_ID', 'RENTFREE_ENDDATE', 'RENTFREE_STARTDATE', 'REPAIR_TIME', 'SERVERPARTREGION', 'SERVERPART_TYPE', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'WATER_CHARGE'] vs ['BRAND_NAME', 'BUSINESS_BRAND', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'COMPACT_BASIS', 'COMPACT_CHILDTYPE', 'COMPACT_DPDESC', 'DECORATE_ENDDATE', 'DECORATE_STARTDATE', 'ELECTRICITY_FEES', 'EQUIPMENT_DEPOSIT', 'FIRSTYEAR_RENT', 'GUARANTEE_RATIO', 'OPERATING_AREA', 'OPERATING_SCOPE', 'OPERATING_SITE', 'OTHER_SCHARGE', 'PROPERTY_FEE', 'REGISTERCOMPACTSUB_ID', 'REGISTERCOMPACT_ID', 'RENTFREE_ENDDATE', 'RENTFREE_STARTDATE', 'REPAIR_TIME', 'SERVERPARTREGION', 'SERVERPART_TYPE', 'SETTLEMENT_CYCLE', 'SETTLEMENT_MODES', 'WATER_CHARGE'] |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.OPERATING_AREA: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.PROPERTY_FEE: 类型不一致 (float vs int)，值为 0.0 vs 0

原 API 状态: `200`，耗时 `85.82 ms`
新 API 状态: `200`，耗时 `9.62 ms`

### Contract/GetRegisterCompactSubList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"REGISTERCOMPACTSUB_ID": 737}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Contract/GetRegisterCompactSubList | 新 API: http://localhost:8080/EShangApiMain/Contract/GetRegisterCompactSubList |
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
| 首条字段集合 | ✅ | 字段一致，共 28 个 |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List[0].OPERATING_AREA: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.List[0].PROPERTY_FEE: 类型不一致 (float vs int)，值为 0.0 vs 0

原 API 状态: `200`，耗时 `115.11 ms`
新 API 状态: `200`，耗时 `20.62 ms`

### ContractSyn/GetContractSynDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/ContractSyn/GetContractSynDetail | 新 API: http://localhost:8080/EShangApiMain/ContractSyn/GetContractSynDetail |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ❌ | 原 API: False | 新 API: True |

差异明细：
- 原 API JSON 解析失败: Expecting value: line 1 column 1 (char 0)

原 API 状态: `404`，耗时 `5.45 ms`
新 API 状态: `200`，耗时 `2.9 ms`

### ContractSyn/GetContractSynList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/ContractSyn/GetContractSynList | 新 API: http://localhost:8080/EShangApiMain/ContractSyn/GetContractSynList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ❌ | 原 API: False | 新 API: True |

差异明细：
- 原 API JSON 解析失败: Expecting value: line 1 column 1 (char 0)

原 API 状态: `404`，耗时 `6.93 ms`
新 API 状态: `200`，耗时 `20.53 ms`
