# 动态接口对比报告

- 生成时间: 2026-03-09 18:35:49
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\read_only_completeness_template.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `6/6` 个用例通过

## 用例明细

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
