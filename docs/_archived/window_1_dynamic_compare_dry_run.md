# 动态接口对比报告

- 生成时间: 2026-03-09 18:45:03
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_1.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 131 / FAIL 0 / SKIP 164 / TOTAL 295`

## 用例明细

### BaseInfo/BatchPROPERTYASSETS / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/BatchPROPERTYSHOP / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/BindingMerchantTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/BindingOwnerUnitTree |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/CreatePriceType / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DelServerpartShop / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteAUTOSTATISTICS / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteBUSINESSTRADE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteBrand / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteBusinessTrade / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteCASHWORKER / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteCOMMODITY / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteCOMMODITYTYPE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteOWNERUNIT / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeletePROPERTYASSETS / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeletePROPERTYSHOP / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteRTSERVERPARTSHOP / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteSERVERPART / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteSERVERPARTCRT / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteServerpartShop / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/DeleteUSERDEFINEDTYPE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetAUTOSTATISTICSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetAutoStatisticsTreeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBUSINESSTRADEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBUSINESSTRADEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBrandDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetBrandList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessBrandList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetBusinessTradeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetBusinessTradeTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetCASHWORKERList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCOMMODITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetCOMMODITYList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCOMMODITYTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetCOMMODITYTYPEList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetCombineBrandList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetOWNERUNITList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYASSETSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
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
- JSON: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetPROPERTYASSETSTreeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetPROPERTYSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetPROPERTYSHOPList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetRTSERVERPARTSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetRTSERVERPARTSHOPList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTCRTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTCRTTreeList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetSERVERPARTDetail |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTList / empty-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTList / search-model

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"ProvinceCode": "340000", "SERVERPART_ID": 416, "SERVERPART_IDS": 416}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSERVERPARTList / flat-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"ProvinceCode": "340000", "SERVERPART_ID": 416, "SERVERPART_IDS": 416}`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetSERVERPARTSHOP_LOGList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetSPRegionShopTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerPartShopNewList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartDDL / default-type

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartType": "1000"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartDDL |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartDDL / service-area-416

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SERVERPART_ID": 416}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET BaseInfo/GetServerpartDDL |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartDDL / empty-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetServerpartShopList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/GetServerpartShopTree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BaseInfo/GetUSERDEFINEDTYPEList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/LowerShelfCommodity / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/ModifyShopBusinessState / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/ModifyShopState / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/OnShelfCommodity / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/ServerPartShopNewSaveState / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SolidServerpartWeather / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroAUTOSTATISTICS / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroBUSINESSTRADE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroBrand / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroBusinessTrade / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroCASHWORKER / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroCOMMODITY / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroCOMMODITYTYPE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroOWNERUNIT / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroPROPERTYASSETS / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroPROPERTYASSETSLOG / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroPROPERTYSHOP / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroRTSERVERPARTSHOP / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroSERVERPART / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroSERVERPARTCRT / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroServerPartShopNew / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroServerpartShop / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BaseInfo/SynchroUSERDEFINEDTYPE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/DeleteAUTOTYPE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/DeleteOWNERSERVERPART / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/DeleteOWNERSERVERPARTSHOP / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/DeleteSERVERPARTSHOPCRT / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/DeleteSERVERPARTTYPE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/DeleteSPSTATICTYPE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetAUTOTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetAUTOTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetNestingAUTOTYPEList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetNestingAUTOTYPETree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetNestingSERVERPARTTYPEList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetNestingSERVERPARTTYPETree / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetOWNERSERVERPARTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetOWNERSERVERPARTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetOWNERSERVERPARTSHOPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetOWNERSERVERPARTSHOPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetSERVERPARTSHOPCRTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetSERVERPARTSHOPCRTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetSERVERPARTTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetSERVERPARTTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetSPSTATICTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/GetSPSTATICTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/ModifyRTServerpartType / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/SynchroAUTOTYPE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/SynchroOWNERSERVERPART / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/SynchroOWNERSERVERPARTSHOP / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/SynchroSERVERPARTSHOPCRT / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/SynchroSERVERPARTTYPE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BasicConfig/SynchroSPSTATICTYPE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/ApproveCommodityInfo_AHJG / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/DeleteCOMMODITY / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/DeleteCOMMODITY_RUNNING / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/DeleteRTUDType / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/GetApprovalCommodityList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

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

### Commodity/GetCOMMODITY_HISTORYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/GetCOMMODITY_RUNNINGDetail / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/GetCOMMODITY_RUNNINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

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

### Commodity/GetServerpartShopTrade / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/RelateUDType / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/SyncCommodityInfo_AHJG / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/SynchroCOMMODITY / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/SynchroCOMMODITY_HISTORY / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Commodity/SynchroCOMMODITY_RUNNING / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/DeleteCoopMerchants / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/DeleteCoopMerchantsLinker / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/DeleteCoopMerchantsType / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/DeleteRTCoopMerchants / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsDDL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/GetCoopMerchantsDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
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
- JSON: `null`
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
- JSON: `null`
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

### Merchants/SynchroCoopMerchants / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/SynchroCoopMerchantsLinker / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/SynchroCoopMerchantsType / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Merchants/SynchroRTCoopMerchants / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/ApproveProinst / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/ApproveSHOPEXPENSE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/CreateRevenueAccount / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteBIZPSPLITMONTH / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteBUSINESSPROJECTSPLIT / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteBusinessPayment / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteBusinessProject / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteCONTRACT_SYN / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeletePERIODWARNING / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeletePROJECTSPLITMONTH / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeletePROJECTWARNING / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeletePaymentConfirm / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteRTPaymentRecord / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteRemarks / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteRevenueConfirm / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteSHOPEXPENSE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteSHOPROYALTYDETAIL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/DeleteShopRoyalty / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetAPPROVEDList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetAPPROVEDList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetAccountWarningList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST BusinessProject/GetBIZPSPLITMONTHList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/GetBUSINESSPROJECTSPLITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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

### BusinessProject/ReconfigureProfit / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SaveHisPaymentAccount / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SeparatePaymentRecord / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SolidAccountWarningList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SolidPeriodAnalysis / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SolidPeriodWarningList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SolidProjectRevenue / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroBIZPSPLITMONTH / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroBUSINESSPROJECTSPLIT / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroBusinessPayment / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroBusinessProject / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroCONTRACT_SYN / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroPERIODWARNING / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroPROJECTSPLITMONTH / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroPROJECTWARNING / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroPaymentConfirm / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroRTPaymentRecord / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroRemarks / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroRevenueConfirm / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroSHOPEXPENSE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroSHOPROYALTYDETAIL / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/SynchroShopRoyalty / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### BusinessProject/UploadRevenueConfirmList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/AddContractSupplement / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/DelFile / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/DeleteAttachment / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/DeleteRTRegisterCompact / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/DeleteRegisterCompact / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/DeleteRegisterCompactSub / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetAttachmentDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetAttachmentList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetContractExpiredInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Contract/GetContractExpiredInfo |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetContractYearList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetProjectMonthlyArrearageList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetRTRegisterCompactList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRegisterCompactDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetRegisterCompactList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetRegisterCompactSubDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
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
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | POST Contract/GetRegisterCompactSubList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/GetShopBusinessTypeRatio / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SaveAttachment / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SynchroAttachment / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SynchroAttachmentList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SynchroContractSyn / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SynchroRTRegisterCompact / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SynchroRegisterCompact / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Contract/SynchroRegisterCompactSub / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### ContractSyn/DeleteContractSyn / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

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

### ContractSyn/SynchroContractSyn / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该接口不是明确读接口，按当前“禁止写接口”策略跳过。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/DeleteEXPENSESPREPAID / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/DeleteEXPENSESSEPARATE / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/GetEXPENSESPREPAIDDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/GetEXPENSESPREPAIDList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/GetEXPENSESSEPARATEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/GetEXPENSESSEPARATEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/GetShopExpenseHisList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/SynchroEXPENSESPREPAID / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/SynchroEXPENSESSEPARATE / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Expenses/SynchroHisData / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | Python 运行时不存在该路由，保留在 manifest 中做缺口记录。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`
