# 动态接口对比报告

- 生成时间: 2026-03-10 12:04:57
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_1.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 127 / FAIL 0 / SKIP 0 / TOTAL 127`

## 用例明细

### BaseInfo/BindingMerchantTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/BindingMerchantTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/BindingOwnerUnitDDL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"DataType": 0, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/BindingOwnerUnitDDL |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/BindingOwnerUnitTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"DataType": 0}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/BindingOwnerUnitTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetAUTOSTATISTICSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AUTOSTATISTICSId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetAUTOSTATISTICSDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetAssetsRevenueAmount / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416", "searchMonth": "202512"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetAssetsRevenueAmount |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetAutoStatisticsTreeList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AutoStatistics_Type": 0, "OwnerUnit_Id": 211, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetAutoStatisticsTreeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBrandDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BrandId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetBrandDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBrandList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"BRAND_ID": 1314}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetBrandList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessBrandList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartShopIds": 3080}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetBusinessBrandList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessTradeDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessTradeId": 214}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetBusinessTradeDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessTradeEnum / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessTradeState": 1, "BusinessTrade_PID": 214, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetBusinessTradeEnum |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessTradeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PROVINCE_CODE": 340000}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetBusinessTradeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessTradeTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessTradeState": 1, "BusinessTrade_PID": -1, "ProvinceCode": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetBusinessTradeTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCASHWORKERDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CASHWORKERId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetCASHWORKERDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCASHWORKERList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 99, "SearchParameter": {"CASHWORKER_ID": "1477"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetCASHWORKERList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCOMMODITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYId": 864}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetCOMMODITYDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCOMMODITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITY_ID": 864}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetCOMMODITYList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCOMMODITYTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYTYPEId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetCOMMODITYTYPEDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCOMMODITYTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITYTYPE_ID": 418}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetCOMMODITYTYPEList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCombineBrandList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BRAND_TYPE": 2000, "PROVINCE_CODE": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetCombineBrandList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetNestingCOMMODITYTYPEList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYTYPE_PID": -1, "COMMODITYTYPE_VALID": 1, "PROVINCE_CODE": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetNestingCOMMODITYTYPEList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetNestingCOMMODITYTYPETree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITYTYPE_PID": -1, "COMMODITYTYPE_VALID": 1, "PROVINCE_CODE": 340000}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetNestingCOMMODITYTYPETree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetNestingOwnerUnitList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"OwnerUnitNature": 1000, "ProvinceCode": 340000, "ShowStatus": true}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetNestingOwnerUnitList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetOWNERUNITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"OWNERUNITId": 211}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetOWNERUNITDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetOWNERUNITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PROVINCE_CODE": 340000}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetOWNERUNITList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYASSETSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROPERTYASSETSId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetPROPERTYASSETSDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYASSETSLOGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PROPERTYASSETSLOG_ID": 6}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetPROPERTYASSETSLOGList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYASSETSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetPROPERTYASSETSList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYASSETSTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetPROPERTYASSETSTreeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROPERTYSHOPId": 42}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetPROPERTYSHOPDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYSHOPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetPROPERTYSHOPList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetRTSERVERPARTSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RTSERVERPARTSHOPId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetRTSERVERPARTSHOPDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetRTSERVERPARTSHOPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"RTSERVERPARTSHOP_ID": 101}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetRTSERVERPARTSHOPList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTCRTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SERVERPARTTId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetSERVERPARTCRTDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTCRTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTCRTList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTCRTTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTCRTTreeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SERVERPARTId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetSERVERPARTDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTList / search-model

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"SERVERPART_IDS": 416}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTSHOP_LOGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"SERVERPART_IDS": 416}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTSHOP_LOGList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSPRegionShopTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetSPRegionShopTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerPartShopNewDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"serverPartShopId": 3080}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerPartShopNewDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerPartShopNewList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"provinceCode": "340000", "serverPartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerPartShopNewList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartDDL / service-area-416

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartType": "1000", "StatisticsType": "1000"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartDDL |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartShopDDL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartShopDDL |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartShopDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartShopId": 3080}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartShopDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartShopInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartCode": "1", "ShopCode": "1"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartShopInfo |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartShopList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"SERVERPART_IDS": 416}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetServerpartShopList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartShopTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartShopTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartType": "1000", "StatisticsType": "1000"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartUDTypeTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartUDTypeTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetShopReceivables / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetShopReceivables |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetShopShortNames / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416, "ShopValid": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetShopShortNames |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetTradeBrandTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BrandState": 1, "BusinessTrade_PID": -1, "ProvinceCode": "340000"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetTradeBrandTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetUSERDEFINEDTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"USERDEFINEDTYPEId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetUSERDEFINEDTYPEDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetUSERDEFINEDTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"USERDEFINEDTYPE_ID": 40}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetUSERDEFINEDTYPEList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/GetCOMMODITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Commodity/GetCOMMODITYDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/GetCOMMODITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Commodity/GetCOMMODITYList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/GetCommodityList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Commodity/GetCommodityList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Merchants/GetCoopMerchantsDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsLinkerDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CoopMerchantsLinkerId": 383}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Merchants/GetCoopMerchantsLinkerDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsLinkerList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COOPMERCHANTS_LINKER_ID": 383}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Merchants/GetCoopMerchantsLinkerList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COOPMERCHANTS_ID": -2867}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Merchants/GetCoopMerchantsList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsTypeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Merchants/GetCoopMerchantsTypeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetRTCoopMerchantsList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Merchants/GetRTCoopMerchantsList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetTradeBrandMerchantsList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Merchants/GetTradeBrandMerchantsList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetAPPROVEDList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"APPROVED_ID": 5419}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetAPPROVEDList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetAccountWarningList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetAccountWarningList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetAccountWarningListSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetAccountWarningListSummary |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetAnnualSplit / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessProjectId": 1905, "DataType": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetAnnualSplit |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBIZPSPLITMONTHDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BIZPSPLITMONTHId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetBIZPSPLITMONTHDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBIZPSPLITMONTHList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"BIZPSPLITMONTH_ID": 3106}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetBIZPSPLITMONTHList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBUSINESSPROJECTSPLITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BUSINESSPROJECTSPLITId": 87658}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetBUSINESSPROJECTSPLITDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBUSINESSPROJECTSPLITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetBUSINESSPROJECTSPLITList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBrandReceivables / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetBrandReceivables |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBusinessPaymentDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetBusinessPaymentDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBusinessPaymentList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetBusinessPaymentList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBusinessProjectDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetBusinessProjectDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBusinessProjectList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetBusinessProjectList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetCONTRACT_SYNDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetCONTRACT_SYNDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetCONTRACT_SYNList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetCONTRACT_SYNList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetExpenseSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetExpenseSummary |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetMerchantSplit / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetMerchantSplit |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetMerchantsReceivables / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetMerchantsReceivables |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetMerchantsReceivablesList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetMerchantsReceivablesList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetMerchantsReceivablesReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetMerchantsReceivablesReport |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetMonthSummaryList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetMonthSummaryList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetNoProjectShopList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetNoProjectShopList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPERIODWARNINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetPERIODWARNINGDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPERIODWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetPERIODWARNINGList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPROJECTSPLITMONTHDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetPROJECTSPLITMONTHDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPROJECTSPLITMONTHList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetPROJECTSPLITMONTHList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPROJECTWARNINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetPROJECTWARNINGDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPROJECTWARNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetPROJECTWARNINGList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPaymentConfirmDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetPaymentConfirmDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPaymentConfirmList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetPaymentConfirmList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetPeriodWarningList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetPeriodWarningList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetProjectAccountDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetProjectAccountDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetProjectAccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetProjectAccountList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetProjectAccountTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetProjectAccountTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetRTPaymentRecordDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetRTPaymentRecordDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetRTPaymentRecordList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetRTPaymentRecordList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetRemarksDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetRemarksDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetRemarksList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetRemarksList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetRevenueConfirmDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetRevenueConfirmDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetRevenueConfirmList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetRevenueConfirmList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetSHOPEXPENSEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetSHOPEXPENSEDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetSHOPEXPENSEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetSHOPEXPENSEList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetSHOPROYALTYDETAILDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetSHOPROYALTYDETAILDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetSHOPROYALTYDETAILList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetSHOPROYALTYDETAILList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetShopExpenseSummary / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetShopExpenseSummary |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetShopRoyaltyDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetShopRoyaltyDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetShopRoyaltyList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetShopRoyaltyList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetWillSettleProject / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BusinessProject/GetWillSettleProject |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetAttachmentDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AttachmentId": 1903}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetAttachmentDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetAttachmentList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"ATTACHMENT_ID": 1903}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetAttachmentList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetContractExpiredInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetContractExpiredInfo |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetProjectMonthlyArrearageList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "StatisticsYear": 2025}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetProjectMonthlyArrearageList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetProjectSummaryInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetProjectSummaryInfo |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetProjectYearlyArrearageList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetProjectYearlyArrearageList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRTRegisterCompactDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RTRegisterCompactId": 12426, "RegisterCompactId": 466}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetRTRegisterCompactDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRTRegisterCompactList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetRTRegisterCompactList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRegisterCompactDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RegisterCompactId": 21}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetRegisterCompactDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRegisterCompactList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetRegisterCompactList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRegisterCompactSubDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"RegisterCompactId": 731, "RegisterCompactSubId": 737}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetRegisterCompactSubDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRegisterCompactSubList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"REGISTERCOMPACTSUB_ID": 737}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetRegisterCompactSubList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### ContractSyn/GetContractSynDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET ContractSyn/GetContractSynDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### ContractSyn/GetContractSynList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST ContractSyn/GetContractSynList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`
