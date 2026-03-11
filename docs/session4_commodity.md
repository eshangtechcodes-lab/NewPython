# 动态接口对比报告

- 生成时间: 2026-03-11 09:23:51
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_commodity.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 1 / FAIL 2 / SKIP 0 / TOTAL 3`

## 用例明细

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

原 API 状态: `200`，耗时 `138.55 ms`
新 API 状态: `200`，耗时 `2086.12 ms`

### Commodity/GetCOMMODITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

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
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `434.81 ms`
新 API 状态: `200`，耗时 `56.73 ms`

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
| 首条字段集合 | ✅ | 字段一致，共 9 个 |
| 完整响应体 | ❌ | 发现 10 处差异 |

差异明细：
- Result_Data.List[0].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[1].COMMODITY_TYPE: 值不一致 ('锅盔' vs '906')
- Result_Data.List[2].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[3].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[4].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[5].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[6].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[7].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[8].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134')
- Result_Data.List[9].COMMODITY_TYPE: 值不一致 ('素菜类' vs '913')

原 API 状态: `200`，耗时 `550.78 ms`
新 API 状态: `200`，耗时 `221.6 ms`
