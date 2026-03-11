# 动态接口对比报告

- 生成时间: 2026-03-11 11:49:17
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_4.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 0 / FAIL 1 / SKIP 0 / TOTAL 1`

## 用例明细

### Picture/GetPictureList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Picture/GetPictureList | 新 API: http://localhost:8080/EShangApiMain/Picture/GetPictureList |
| HTTP 状态码 | ❌ | 404 vs 405 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['detail'] |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体(参考) | ✅ | 发现 2 处差异(不影响判定) |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.detail: 新 API 多出该字段

原 API 状态: `404`，耗时 `103.3 ms`
新 API 状态: `405`，耗时 `2066.55 ms`
