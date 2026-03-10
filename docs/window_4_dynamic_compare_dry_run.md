# 动态接口对比报告

- 生成时间: 2026-03-09 18:50:31
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_4.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 1 / FAIL 0 / SKIP 30 / TOTAL 31`

## 用例明细

### Picture/BatchDeletePicture / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该路由是 Python 多出接口，不纳入原接口动态一致性测试。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/DeleteMultiPicture / default-body

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

### Picture/DeletePicture / default-query

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

### Picture/GetAuditEvidence / default-query

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

### Picture/GetEndaccountEvidence / default-query

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

### Picture/GetPictureByShop / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该路由是 Python 多出接口，不纳入原接口动态一致性测试。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/GetPictureCount / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该路由是 Python 多出接口，不纳入原接口动态一致性测试。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/GetPictureDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该路由是 Python 多出接口，不纳入原接口动态一致性测试。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/GetPictureList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Dry Run | ✅ | GET Picture/GetPictureList |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/GetPictureTypeList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该路由是 Python 多出接口，不纳入原接口动态一致性测试。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/SaveImgFile / default-body

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

### Picture/SynchroPicture / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `SKIP`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| Skip | ✅ | 该路由是 Python 多出接口，不纳入原接口动态一致性测试。 |

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `None`，耗时 `None ms`

### Picture/UploadAuditEvidence / default-body

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

### Picture/UploadEndaccountEvidence / default-body

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

### Picture/UploadPicture / default-body

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

### ShopVideo/DeleteEXTRANET / default-query

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

### ShopVideo/DeleteEXTRANETDETAIL / default-query

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

### ShopVideo/DeleteSHOPVIDEO / default-query

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

### ShopVideo/GetEXTRANETDETAILDetail / default-query

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

### ShopVideo/GetEXTRANETDETAILList / default-body

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

### ShopVideo/GetEXTRANETDetail / default-query

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

### ShopVideo/GetEXTRANETList / default-body

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

### ShopVideo/GetSHOPVIDEODetail / default-query

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

### ShopVideo/GetSHOPVIDEOList / default-body

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

### ShopVideo/GetShopVideoInfo / default-query

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

### ShopVideo/GetVIDEOLOGList / default-body

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

### ShopVideo/GetYSShopVideoInfo / default-query

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

### ShopVideo/SynchroEXTRANET / default-body

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

### ShopVideo/SynchroEXTRANETDETAIL / default-body

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

### ShopVideo/SynchroSHOPVIDEO / default-body

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

### ShopVideo/SynchroVIDEOLOG / default-body

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
