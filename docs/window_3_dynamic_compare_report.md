# 动态接口对比报告

- 生成时间: 2026-03-10 15:21:52
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\windows\window_3.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 0 / FAIL 86 / SKIP 0 / TOTAL 86`

## 用例明细

### Audit/GetABNORMALAUDITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetABNORMALAUDITList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetABNORMALAUDITList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 服务器内部错误 |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 637, 'List': [{'ABNORMALAUDIT_ID': 479487, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2200, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '149009', 'SHOPNAME': '北区同庆楼鲜肉大包', 'MACHINECODE': '6371', 'ENDACCOUNT_DATE': 20260210233122, 'CHECK_ENDDATE': 20260210151600, 'CHECK_STARTDATE': 20260209234024, 'TIME_INTERVAL': 935.6, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 9661.0, 'CASH_PAYMENT': 364.0, 'CHECK_CASHPAY': 364.0, 'DIFFERENT_PRICE': 0.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 13661.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '', 'CASHIER_NAME': '同庆楼北', 'DOWNLOAD_DATE': '2026-02-10T23:31:54', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/09 23:40:24', 'CHECK_ENDDATE_SEARCH': '2026/02/10 15:16:00'}, {'ABNORMALAUDIT_ID': 479484, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2271, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '145001', 'SHOPNAME': '北区下塘烧饼', 'MACHINECODE': '6376', 'ENDACCOUNT_DATE': 20260210231309, 'CHECK_ENDDATE': 20260210114129, 'CHECK_STARTDATE': 20260209232234, 'TIME_INTERVAL': 738.92, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 3734.0, 'CASH_PAYMENT': 143.0, 'CHECK_CASHPAY': 117.0, 'DIFFERENT_PRICE': -26.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 9884.2, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '下塘烧饼北', 'DOWNLOAD_DATE': '2026-02-10T23:14:00', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/09 23:22:34', 'CHECK_ENDDATE_SEARCH': '2026/02/10 11:41:29'}, {'ABNORMALAUDIT_ID': 479486, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2200, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '149009', 'SHOPNAME': '北区同庆楼鲜肉大包', 'MACHINECODE': '6371', 'ENDACCOUNT_DATE': 20260210233122, 'CHECK_ENDDATE': 20260210113700, 'CHECK_STARTDATE': 20260209234024, 'TIME_INTERVAL': 716.6, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 7034.0, 'CASH_PAYMENT': 194.0, 'CHECK_CASHPAY': 194.0, 'DIFFERENT_PRICE': 0.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 13661.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '同庆楼北', 'DOWNLOAD_DATE': '2026-02-10T23:31:54', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/09 23:40:24', 'CHECK_ENDDATE_SEARCH': '2026/02/10 11:37:00'}, {'ABNORMALAUDIT_ID': 479416, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2271, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '145001', 'SHOPNAME': '北区下塘烧饼', 'MACHINECODE': '6376', 'ENDACCOUNT_DATE': 20260209232028, 'CHECK_ENDDATE': 20260209105847, 'CHECK_STARTDATE': 20260208235500, 'TIME_INTERVAL': 663.78, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 1853.0, 'CASH_PAYMENT': 69.0, 'CHECK_CASHPAY': 69.0, 'DIFFERENT_PRICE': 0.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 7776.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '下塘烧饼北', 'DOWNLOAD_DATE': '2026-02-09T23:21:45', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/08 23:55:00', 'CHECK_ENDDATE_SEARCH': '2026/02/09 10:58:47'}, {'ABNORMALAUDIT_ID': 479349, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 1218, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '027001', 'SHOPNAME': '南区客房', 'MACHINECODE': '4521', 'ENDACCOUNT_DATE': 20260208222750, 'CHECK_ENDDATE': 20260208104244, 'CHECK_STARTDATE': 20260208104239, 'TIME_INTERVAL': 0.08, 'ABNORMALAUDIT_TYPE': 1.0, 'ERASE_TYPE': 0.0, 'TOTALSELLAMOUNT': 0.0, 'CASH_PAYMENT': 0.0, 'CHECK_CASHPAY': 0.0, 'DIFFERENT_PRICE': 0.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 396.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '', 'CASHIER_NAME': '客房收银员', 'DOWNLOAD_DATE': '2026-02-08T22:42:57', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/08 10:42:39', 'CHECK_ENDDATE_SEARCH': '2026/02/08 10:42:44'}, {'ABNORMALAUDIT_ID': 479358, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2271, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '145001', 'SHOPNAME': '北区下塘烧饼', 'MACHINECODE': '6376', 'ENDACCOUNT_DATE': 20260208235235, 'CHECK_ENDDATE': 20260208102910, 'CHECK_STARTDATE': 20260207233923, 'TIME_INTERVAL': 649.78, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 2845.0, 'CASH_PAYMENT': 55.0, 'CHECK_CASHPAY': 54.0, 'DIFFERENT_PRICE': -1.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 9931.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '下塘烧饼北', 'DOWNLOAD_DATE': '2026-02-08T23:53:47', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/07 23:39:23', 'CHECK_ENDDATE_SEARCH': '2026/02/08 10:29:10'}, {'ABNORMALAUDIT_ID': 479289, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2271, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '145001', 'SHOPNAME': '北区下塘烧饼', 'MACHINECODE': '6376', 'ENDACCOUNT_DATE': 20260207233728, 'CHECK_ENDDATE': 20260207144539, 'CHECK_STARTDATE': 20260206220759, 'TIME_INTERVAL': 997.67, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 5574.0, 'CASH_PAYMENT': 91.0, 'CHECK_CASHPAY': 91.0, 'DIFFERENT_PRICE': 0.0, 'REPLENISH_AMOUNT': 0.0, 'ENDACCOUNT_REVENUE': 10140.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '下塘烧饼北', 'DOWNLOAD_DATE': '2026-02-07T23:38:35', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/06 22:07:59', 'CHECK_ENDDATE_SEARCH': '2026/02/07 14:45:39'}, {'ABNORMALAUDIT_ID': 479196, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2308, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '147001', 'SHOPNAME': '北区丁记米饺', 'MACHINECODE': '6382', 'ENDACCOUNT_DATE': 20260206222743, 'CHECK_ENDDATE': 20260206142721, 'CHECK_STARTDATE': 20260205233334, 'TIME_INTERVAL': 893.78, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 5648.0, 'CASH_PAYMENT': 379.0, 'CHECK_CASHPAY': 380.0, 'DIFFERENT_PRICE': 1.0, 'REPLENISH_AMOUNT': 1.0, 'ENDACCOUNT_REVENUE': 9718.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '丁记米饺北', 'DOWNLOAD_DATE': '2026-02-06T22:28:04', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/05 23:33:34', 'CHECK_ENDDATE_SEARCH': '2026/02/06 14:27:21'}, {'ABNORMALAUDIT_ID': 479117, 'ENDACCOUNT_ID': 0, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': 2271, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '145001', 'SHOPNAME': '北区下塘烧饼', 'MACHINECODE': '6376', 'ENDACCOUNT_DATE': 20260205203739, 'CHECK_ENDDATE': 20260205150350, 'CHECK_STARTDATE': 20260204210050, 'TIME_INTERVAL': 1083.0, 'ABNORMALAUDIT_TYPE': 0.0, 'ERASE_TYPE': 1.0, 'TOTALSELLAMOUNT': 2260.0, 'CASH_PAYMENT': 95.0, 'CHECK_CASHPAY': 100.0, 'DIFFERENT_PRICE': 5.0, 'REPLENISH_AMOUNT': 5.0, 'ENDACCOUNT_REVENUE': 3825.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': 0.0, 'PUSH_STATE': 1.0, 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '下塘烧饼北', 'DOWNLOAD_DATE': '2026-02-05T20:39:55', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': '', 'CHECK_STARTDATE_SEARCH': '2026/02/04 21:00:50', 'CHECK_ENDDATE_SEARCH': '2026/02/05 15:03:50'}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `341.66 ms`
新 API 状态: `200`，耗时 `2061.71 ms`

### Audit/GetAUDITTASKSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AUDITTASKSId": 3675}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAUDITTASKSDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAUDITTASKSDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 服务器内部错误 |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'AUDITTASKS_ID': 3675, 'SERVERPART_ID': 477, 'SERVERPARTCODE': '340606', 'SERVERPART_NAME': '呈坎服务区', 'SERVERPARTSHOP_ID': None, 'SHOPCODE': None, 'SHOPNAME': None, 'BUSINESSTYPE': '3000', 'BUSINESSTYPE_NAME': '自营餐饮', 'AUDITTASKS_STARTDATE': '2023-04-07T00:00:00', 'AUDITTASKS_ENDDATE': None, 'AUDITTASKS_DURATION': None, 'AUDITTASKS_COUNT': None, 'AUDITTASKS_INTERVAL': None, 'AUDITTASKS_TYPE': None, 'AUDITTASKS_FIRSTTIME': None, 'AUDITTASKS_SECONDTIME': None, 'AUDITTASKS_THIRDTIME': None, 'AUDITTASKS_ISVALID': 1, 'OPERATE_DATE': '2023-04-07T10:53:17', 'STAFF_ID': 811, 'STAFF_NAME': '张坤', 'AUDITTASKS_DESC': '公司远程稽核'} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `145.09 ms`
新 API 状态: `200`，耗时 `2036.98 ms`

### Audit/GetAUDITTASKSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"AUDITTASKS_ID": 3675}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAUDITTASKSList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAUDITTASKSList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `148.4 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetAbnormalAuditDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AbnormalAuditId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAbnormalAuditDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAbnormalAuditDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `135.25 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetAbnormalRateReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416", "endDate": "2025-12-02", "startDate": "2025-12-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAbnormalRateReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAbnormalRateReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `292.88 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetAuditDetils / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditDetils | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditDetils |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.24 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetAuditList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.76 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetAuditTasksDetailList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditTasksDetailList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditTasksDetailList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `6.39 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetAuditTasksReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditTasksReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditTasksReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `5.35 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetCHECKACCOUNTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CHECKACCOUNTId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetCHECKACCOUNTDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetCHECKACCOUNTDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `146.91 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetCHECKACCOUNTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetCHECKACCOUNTList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetCHECKACCOUNTList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `4763.89 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetCheckAccountReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416", "checkType": 1, "endDate": "2025-01-02", "startDate": "2025-01-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetCheckAccountReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetCheckAccountReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `146.11 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetSpecialBehaviorReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"ServerpartIds": "416", "endDate": "2025-01-02", "startDate": "2025-01-01"}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetSpecialBehaviorReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetSpecialBehaviorReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `9.17 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetYSABNORMALITYDETAILList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"AbnormalityCode": 1}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYDETAILList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYSABNORMALITYDETAILList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `7.65 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetYSABNORMALITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AbnormalityCode": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYSABNORMALITYDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `165.95 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetYSABNORMALITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYSABNORMALITYList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `183.23 ms`
新 API 状态: `None`，耗时 `None ms`

### Audit/GetYsabnormalityReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"ServerpartIds": "416", "endDate": "2025-01-02", "startDate": "2025-01-01"}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYsabnormalityReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYsabnormalityReport |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `404`，耗时 `11.08 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetANALYSISINSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ANALYSISINSId": 1805}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISINSDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISINSDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `138.51 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetANALYSISINSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"ANALYSISINS_ID": "1805"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISINSList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISINSList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `154.92 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetANALYSISRULEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ANALYSISRULEId": 19}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISRULEDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISRULEDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `216.25 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetANALYSISRULEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"ANALYSISRULE_ID": 19}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISRULEList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISRULEList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `195.51 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetASSETSPROFITSBusinessTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSBusinessTreeList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSBusinessTreeList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `92.86 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetASSETSPROFITSDateDetailList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"endDate": "202512", "propertyAssetsId": 1, "serverPartId": 416, "shopId": 9475, "startDate": "202501"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSDateDetailList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSDateDetailList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `173.34 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetASSETSPROFITSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ASSETSPROFITSId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `147.65 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetASSETSPROFITSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `392.71 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetASSETSPROFITSTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSTreeList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSTreeList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `10.64 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetAssetsLossProfitList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"endDate": "202512", "propertyAssetsId": 1, "serverPartId": 416, "startDate": "202501"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetAssetsLossProfitList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetAssetsLossProfitList |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `152.31 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetINVESTMENTANALYSISDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"INVESTMENTANALYSISId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetINVESTMENTANALYSISDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetINVESTMENTANALYSISDetail |

差异明细：
- 新 API 调用失败: HTTPConnectionPool(host='localhost', port=8080): Read timed out. (read timeout=20)

原 API 状态: `200`，耗时 `163.71 ms`
新 API 状态: `None`，耗时 `None ms`

### Analysis/GetINVESTMENTANALYSISList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetINVESTMENTANALYSISList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetINVESTMENTANALYSISList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 632, 'List': [{'INVESTMENTANALYSIS_ID': 485, 'SERVERPART_ID': 510, 'SERVERPART_NAME': '皇甫山服务区', 'SERVERPART_TYPE': 2000, 'SERVERPARTSHOP_ID': '5555,5556,5556', 'SERVERPARTSHOP_NAME': '五味斋', 'BUSINESSPROJECT_ID': 1715, 'BUSINESSPROJECT_NAME': '驿达公司皇甫山服务区安徽地方特色 项目', 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': 226, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 15, 'TRADE_PROJECTCOUNT': 47, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': 20.6, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 23.53, 'GUARANTEE_MINPRICE': 18.28, 'GUARANTEE_MAXPRICE': 196.0, 'GUARANTEE_AVGPRICE': 77.67, 'MINTURNOVER': 30.6, 'GUARANTEERATIO': 26.0, 'ROYALTY_PRICE': None, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': None, 'PROFIT_TOTALAMOUNT': -43045.06, 'PROFIT_INFO': '', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': None, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': None, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-09T18:44:32', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 486, 'SERVERPART_ID': 494, 'SERVERPART_NAME': '马衙服务区', 'SERVERPART_TYPE': 2000, 'SERVERPARTSHOP_ID': '5242,5244', 'SERVERPARTSHOP_NAME': '享当当餐厅', 'BUSINESSPROJECT_ID': 1662, 'BUSINESSPROJECT_NAME': '驿达公司马衙服务区主餐饮项目', 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 17, 'TRADE_PROJECTCOUNT': 55, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': 19.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 23.53, 'GUARANTEE_MINPRICE': 0.01, 'GUARANTEE_MAXPRICE': 300.13, 'GUARANTEE_AVGPRICE': 95.51, 'MINTURNOVER': 40.57, 'GUARANTEERATIO': 23.0, 'ROYALTY_PRICE': None, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': None, 'PROFIT_TOTALAMOUNT': 453536.25, 'PROFIT_INFO': '', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': None, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': None, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-09T18:44:34', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 487, 'SERVERPART_ID': 478, 'SERVERPART_NAME': '牯牛降服务区', 'SERVERPART_TYPE': 3000, 'SERVERPARTSHOP_ID': '3928,3929', 'SERVERPARTSHOP_NAME': '天之红祁门红茶', 'BUSINESSPROJECT_ID': 1654, 'BUSINESSPROJECT_NAME': '驿达公司牯牛降服务区地方特色项目', 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': 236, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 1, 'TRADE_PROJECTCOUNT': 7, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': 16.0, 'COMMISSION_MAXRATIO': 16.0, 'COMMISSION_AVGRATIO': 16.0, 'GUARANTEE_MINPRICE': 4.0, 'GUARANTEE_MAXPRICE': 4.0, 'GUARANTEE_AVGPRICE': 4.0, 'MINTURNOVER': 4.0, 'GUARANTEERATIO': 16.0, 'ROYALTY_PRICE': None, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': None, 'PROFIT_TOTALAMOUNT': -379478.97, 'PROFIT_INFO': '', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': None, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': None, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-09T18:44:34', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 488, 'SERVERPART_ID': 803, 'SERVERPART_NAME': '温泉服务区', 'SERVERPART_TYPE': 2000, 'SERVERPARTSHOP_ID': '5302,5303', 'SERVERPARTSHOP_NAME': '咖啡', 'BUSINESSPROJECT_ID': 1666, 'BUSINESSPROJECT_NAME': '驿达公司温泉服务区咖啡项目', 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': 237, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 3, 'TRADE_PROJECTCOUNT': 7, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': 21.0, 'COMMISSION_MAXRATIO': 23.0, 'COMMISSION_AVGRATIO': 22.33, 'GUARANTEE_MINPRICE': 12.1, 'GUARANTEE_MAXPRICE': 18.19, 'GUARANTEE_AVGPRICE': 14.43, 'MINTURNOVER': 12.1, 'GUARANTEERATIO': 21.0, 'ROYALTY_PRICE': None, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': None, 'PROFIT_TOTALAMOUNT': -149760.47, 'PROFIT_INFO': '', 'COMMISSION_RATIO': '20%-23%', 'REVENUE_LASTAMOUNT': None, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': None, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-09T18:44:35', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 489, 'SERVERPART_ID': 592, 'SERVERPART_NAME': '皇藏峪服务区', 'SERVERPART_TYPE': 3000, 'SERVERPARTSHOP_ID': '3430,3430,3431', 'SERVERPARTSHOP_NAME': '刘老二烧鸡', 'BUSINESSPROJECT_ID': 1656, 'BUSINESSPROJECT_NAME': '驿达公司皇藏峪服务区地方特色项目', 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': 243, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 20, 'TRADE_PROJECTCOUNT': 71, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 32.6, 'COMMISSION_AVGRATIO': 22.46, 'GUARANTEE_MINPRICE': 3.75, 'GUARANTEE_MAXPRICE': 328.0, 'GUARANTEE_AVGPRICE': 60.72, 'MINTURNOVER': 9.0, 'GUARANTEERATIO': 21.0, 'ROYALTY_PRICE': None, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': None, 'PROFIT_TOTALAMOUNT': -315266.96, 'PROFIT_INFO': '', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': None, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': None, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-09T18:44:37', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 490, 'SERVERPART_ID': 510, 'SERVERPART_NAME': '皇甫山服务区', 'SERVERPART_TYPE': 2000, 'SERVERPARTSHOP_ID': '5555,5556,5556', 'SERVERPARTSHOP_NAME': '五味斋', 'BUSINESSPROJECT_ID': 1715, 'BUSINESSPROJECT_NAME': '驿达公司皇甫山服务区安徽地方特色 项目', 'SHOPROYALTY_ID': 4500, 'BUSINESS_TRADE': 226, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 15, 'TRADE_PROJECTCOUNT': 55, 'PROFIT_AVG': -3.9, 'COMMISSION_MINRATIO': 20.6, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 23.53, 'GUARANTEE_MINPRICE': 18.28, 'GUARANTEE_MAXPRICE': 196.0, 'GUARANTEE_AVGPRICE': 77.67, 'MINTURNOVER': 30.6, 'GUARANTEERATIO': 26.0, 'ROYALTY_PRICE': 523808.95, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 94.25, 'PROFIT_AMOUNT': 313071.68, 'PROFIT_TOTALAMOUNT': 402302.89, 'PROFIT_INFO': '装修期：8.92万元，第1期：31.30万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 1460025.86, 'REVENUE_AVGAMOUNT': 121668.82, 'ADJUST_RATIO': 25.0, 'ADJUST_RENT': 36.5, 'ADJUST_AMOUNT': 5.9, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:49', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 491, 'SERVERPART_ID': 494, 'SERVERPART_NAME': '马衙服务区', 'SERVERPART_TYPE': 2000, 'SERVERPARTSHOP_ID': '5242,5244', 'SERVERPARTSHOP_NAME': '享当当餐厅', 'BUSINESSPROJECT_ID': 1662, 'BUSINESSPROJECT_NAME': '驿达公司马衙服务区主餐饮项目', 'SHOPROYALTY_ID': 4371, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 17, 'TRADE_PROJECTCOUNT': 50, 'PROFIT_AVG': 31.99, 'COMMISSION_MINRATIO': 19.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 23.53, 'GUARANTEE_MINPRICE': 0.01, 'GUARANTEE_MAXPRICE': 300.13, 'GUARANTEE_AVGPRICE': 95.51, 'MINTURNOVER': 40.57, 'GUARANTEERATIO': 23.0, 'ROYALTY_PRICE': 1102680.05, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 100.0, 'PROFIT_AMOUNT': 2771810.56, 'PROFIT_TOTALAMOUNT': 2752284.37, 'PROFIT_INFO': '装修期：-1.95万元，第1期：277.18万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 2906925.0, 'REVENUE_AVGAMOUNT': 242243.75, 'ADJUST_RATIO': 25.0, 'ADJUST_RENT': 72.67, 'ADJUST_AMOUNT': 32.1, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-09-30T21:09:57', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 492, 'SERVERPART_ID': 478, 'SERVERPART_NAME': '牯牛降服务区', 'SERVERPART_TYPE': 4000, 'SERVERPARTSHOP_ID': '3928,3929', 'SERVERPARTSHOP_NAME': '天之红祁门红茶', 'BUSINESSPROJECT_ID': 1654, 'BUSINESSPROJECT_NAME': '驿达公司牯牛降服务区地方特色项目', 'SHOPROYALTY_ID': 4355, 'BUSINESS_TRADE': 236, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 0, 'TRADE_PROJECTCOUNT': 4, 'PROFIT_AVG': -18.43, 'COMMISSION_MINRATIO': 16.0, 'COMMISSION_MAXRATIO': 16.0, 'COMMISSION_AVGRATIO': 16.0, 'GUARANTEE_MINPRICE': 4.0, 'GUARANTEE_MAXPRICE': 4.0, 'GUARANTEE_AVGPRICE': 4.0, 'MINTURNOVER': 4.0, 'GUARANTEERATIO': 16.0, 'ROYALTY_PRICE': 96861.12, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 100.0, 'PROFIT_AMOUNT': -166073.41, 'PROFIT_TOTALAMOUNT': -137355.23, 'PROFIT_INFO': '装修期：2.87万元，第1期：-16.60万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 336011.0, 'REVENUE_AVGAMOUNT': 28000.92, 'ADJUST_RATIO': 23.0, 'ADJUST_RENT': 7.73, 'ADJUST_AMOUNT': 3.73, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-10-10T21:09:19', 'INVESTMENTANALYSIS_DESC': ''}, {'INVESTMENTANALYSIS_ID': 493, 'SERVERPART_ID': 803, 'SERVERPART_NAME': '温泉服务区', 'SERVERPART_TYPE': 2000, 'SERVERPARTSHOP_ID': '5302,5303', 'SERVERPARTSHOP_NAME': '咖啡', 'BUSINESSPROJECT_ID': 1666, 'BUSINESSPROJECT_NAME': '驿达公司温泉服务区咖啡项目', 'SHOPROYALTY_ID': 4383, 'BUSINESS_TRADE': 237, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 3, 'TRADE_PROJECTCOUNT': 7, 'PROFIT_AVG': 0.05, 'COMMISSION_MINRATIO': 21.0, 'COMMISSION_MAXRATIO': 23.0, 'COMMISSION_AVGRATIO': 22.33, 'GUARANTEE_MINPRICE': 12.1, 'GUARANTEE_MAXPRICE': 18.19, 'GUARANTEE_AVGPRICE': 14.43, 'MINTURNOVER': 12.1, 'GUARANTEERATIO': 21.0, 'ROYALTY_PRICE': 340983.65, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 100.0, 'PROFIT_AMOUNT': 193553.0, 'PROFIT_TOTALAMOUNT': 172842.87, 'PROFIT_INFO': '装修期：-2.07万元，第1期：19.35万元', 'COMMISSION_RATIO': '20%-23%', 'REVENUE_LASTAMOUNT': 974046.0, 'REVENUE_AVGAMOUNT': 81170.5, 'ADJUST_RATIO': 22.0, 'ADJUST_RENT': 21.43, 'ADJUST_AMOUNT': 9.33, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-10-01T21:11:11', 'INVESTMENTANALYSIS_DESC': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `329.16 ms`
新 API 状态: `200`，耗时 `19118.17 ms`

### Analysis/GetINVESTMENTDETAILDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"INVESTMENTDETAILId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetINVESTMENTDETAILDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetINVESTMENTDETAILDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'INVESTMENTDETAIL_ID': 1, 'INVESTMENTANALYSIS_ID': 23, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 422, 'SERVERPART_NAME': '文集服务区', 'SERVERPARTSHOP_ID': '1140,1140,1141,1141', 'SERVERPARTSHOP_NAME': '竹木藤店', 'BUSINESSPROJECT_ID': 516, 'EVALUATE_SCORE': 26.56, 'SERVERPART_FLOW': 1787267, 'VEHICLE_TOLERANCE': None, 'REVENUE_AVGAMOUNT': 10486.36, 'REVENUE_TOLERANCE': None, 'SERVERPART_AVGRENT': 2271.23, 'SERVERPART_REVENUE': 1270059.38, 'MARKETREVENUE_AVGAMOUNT': 416911.36, 'PROFIT_AMOUNT': -178155.96, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-05T20:55:13', 'INVESTMENTDETAIL_DESC': ''} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `154.51 ms`
新 API 状态: `200`，耗时 `4.11 ms`

### Analysis/GetINVESTMENTDETAILList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetINVESTMENTDETAILList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetINVESTMENTDETAILList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 7477, 'List': [{'INVESTMENTDETAIL_ID': 5802, 'INVESTMENTANALYSIS_ID': 321, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 430, 'SERVERPART_NAME': '颍上服务区', 'SERVERPARTSHOP_ID': '3922,3923', 'SERVERPARTSHOP_NAME': '驿小食', 'BUSINESSPROJECT_ID': 45, 'EVALUATE_SCORE': 52.1, 'SERVERPART_FLOW': 1872585, 'VEHICLE_TOLERANCE': 92.81, 'REVENUE_AVGAMOUNT': 131029.0, 'REVENUE_TOLERANCE': -0.85, 'SERVERPART_AVGRENT': 109038.99, 'SERVERPART_REVENUE': 1195712.71, 'MARKETREVENUE_AVGAMOUNT': 672092.14, 'PROFIT_AMOUNT': 798335.02, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:41', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 5803, 'INVESTMENTANALYSIS_ID': 321, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 444, 'SERVERPART_NAME': '吕望服务区', 'SERVERPARTSHOP_ID': '1176,1177', 'SERVERPARTSHOP_NAME': '曹阿瞒麻椒鸡', 'BUSINESSPROJECT_ID': 629, 'EVALUATE_SCORE': 26.5, 'SERVERPART_FLOW': 1179855, 'VEHICLE_TOLERANCE': 21.48, 'REVENUE_AVGAMOUNT': 20526.9, 'REVENUE_TOLERANCE': -6.47, 'SERVERPART_AVGRENT': 5458.27, 'SERVERPART_REVENUE': 1127918.18, 'MARKETREVENUE_AVGAMOUNT': 516615.08, 'PROFIT_AMOUNT': -81600.2, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:41', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 5804, 'INVESTMENTANALYSIS_ID': 321, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 444, 'SERVERPART_NAME': '吕望服务区', 'SERVERPARTSHOP_ID': '990,991', 'SERVERPARTSHOP_NAME': '勾馋麻辣烫', 'BUSINESSPROJECT_ID': 628, 'EVALUATE_SCORE': 25.84, 'SERVERPART_FLOW': 1179855, 'VEHICLE_TOLERANCE': 21.48, 'REVENUE_AVGAMOUNT': 1273.48, 'REVENUE_TOLERANCE': -6.47, 'SERVERPART_AVGRENT': 11449.78, 'SERVERPART_REVENUE': 1127918.18, 'MARKETREVENUE_AVGAMOUNT': 516615.08, 'PROFIT_AMOUNT': -182716.15, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:41', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 3896, 'INVESTMENTANALYSIS_ID': 196, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 433, 'SERVERPART_NAME': '官塘服务区', 'SERVERPARTSHOP_ID': '5492,5493', 'SERVERPARTSHOP_NAME': '享当当店', 'BUSINESSPROJECT_ID': 1696, 'EVALUATE_SCORE': 47.29, 'SERVERPART_FLOW': 1050908, 'VEHICLE_TOLERANCE': None, 'REVENUE_AVGAMOUNT': 290582.59, 'REVENUE_TOLERANCE': None, 'SERVERPART_AVGRENT': 90581.41, 'SERVERPART_REVENUE': 1036230.87, 'MARKETREVENUE_AVGAMOUNT': 421714.79, 'PROFIT_AMOUNT': 559831.8, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:06', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 3905, 'INVESTMENTANALYSIS_ID': 196, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 433, 'SERVERPART_NAME': '官塘服务区', 'SERVERPARTSHOP_ID': '636,637', 'SERVERPARTSHOP_NAME': '享当当美食汇', 'BUSINESSPROJECT_ID': 119, 'EVALUATE_SCORE': 50.73, 'SERVERPART_FLOW': 1050908, 'VEHICLE_TOLERANCE': 0.0, 'REVENUE_AVGAMOUNT': 180860.47, 'REVENUE_TOLERANCE': 0.0, 'SERVERPART_AVGRENT': 52639.45, 'SERVERPART_REVENUE': 1036230.87, 'MARKETREVENUE_AVGAMOUNT': 421714.79, 'PROFIT_AMOUNT': 988744.43, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:06', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 3914, 'INVESTMENTANALYSIS_ID': 196, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 436, 'SERVERPART_NAME': '杜集服务区', 'SERVERPARTSHOP_ID': '5480,5481', 'SERVERPARTSHOP_NAME': '享当当', 'BUSINESSPROJECT_ID': 1725, 'EVALUATE_SCORE': 38.36, 'SERVERPART_FLOW': 1021327, 'VEHICLE_TOLERANCE': -2.81, 'REVENUE_AVGAMOUNT': 245368.01, 'REVENUE_TOLERANCE': -21.52, 'SERVERPART_AVGRENT': 57963.76, 'SERVERPART_REVENUE': 813212.7, 'MARKETREVENUE_AVGAMOUNT': 360168.19, 'PROFIT_AMOUNT': 449663.47, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:07', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 3922, 'INVESTMENTANALYSIS_ID': 196, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 495, 'SERVERPART_NAME': '釜山服务区', 'SERVERPARTSHOP_ID': '3504,3505', 'SERVERPARTSHOP_NAME': '小圆满餐厅', 'BUSINESSPROJECT_ID': 143, 'EVALUATE_SCORE': 40.8, 'SERVERPART_FLOW': 1344009, 'VEHICLE_TOLERANCE': 27.89, 'REVENUE_AVGAMOUNT': 206993.18, 'REVENUE_TOLERANCE': -9.01, 'SERVERPART_AVGRENT': 116177.3, 'SERVERPART_REVENUE': 942892.25, 'MARKETREVENUE_AVGAMOUNT': 367390.96, 'PROFIT_AMOUNT': 487496.72, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:07', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 3928, 'INVESTMENTANALYSIS_ID': 196, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 510, 'SERVERPART_NAME': '皇甫山服务区', 'SERVERPARTSHOP_ID': '974,974,975,975', 'SERVERPARTSHOP_NAME': '李先生餐厅', 'BUSINESSPROJECT_ID': 623, 'EVALUATE_SCORE': 62.16, 'SERVERPART_FLOW': 1149526, 'VEHICLE_TOLERANCE': 9.38, 'REVENUE_AVGAMOUNT': 348588.67, 'REVENUE_TOLERANCE': 14.37, 'SERVERPART_AVGRENT': 65699.57, 'SERVERPART_REVENUE': 1185132.55, 'MARKETREVENUE_AVGAMOUNT': 434588.22, 'PROFIT_AMOUNT': 1075910.34, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:07', 'INVESTMENTDETAIL_DESC': ''}, {'INVESTMENTDETAIL_ID': 3932, 'INVESTMENTANALYSIS_ID': 196, 'INVESTMENTANALYSIS_IDS': None, 'SERVERPART_ID': 510, 'SERVERPART_NAME': '皇甫山服务区', 'SERVERPARTSHOP_ID': '5555,5556,5556', 'SERVERPARTSHOP_NAME': '五味斋', 'BUSINESSPROJECT_ID': 1715, 'EVALUATE_SCORE': 39.08, 'SERVERPART_FLOW': 1149526, 'VEHICLE_TOLERANCE': 9.38, 'REVENUE_AVGAMOUNT': 194777.14, 'REVENUE_TOLERANCE': 14.37, 'SERVERPART_AVGRENT': 53570.29, 'SERVERPART_REVENUE': 1185132.55, 'MARKETREVENUE_AVGAMOUNT': 434588.22, 'PROFIT_AMOUNT': 241475.63, 'INVESTMENTDETAIL_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2025-06-06T20:59:07', 'INVESTMENTDETAIL_DESC': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `1402.43 ms`
新 API 状态: `200`，耗时 `458.3 ms`

### Analysis/GetInvestmentReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ContainHoliday": 0, "ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetInvestmentReport | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetInvestmentReport |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 7, 'TotalCount': 7, 'List': [{'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2025/1/14', 'PROJECT_ENDDATE': '2028/1/13', 'ADJUST_RATIORANGE': '20-21.52', 'ADJUST_RENTRANGE': '22.46', 'INVESTMENTANALYSIS_ID': 145, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '5626,5626,5627', 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_NAME': '新桥服务区361服饰项目', 'SHOPROYALTY_ID': 4481, 'BUSINESS_TRADE': 247, 'BUSINESS_PTRADE': 222, 'TRADE_SHOPCOUNT': 6, 'TRADE_PROJECTCOUNT': 10, 'PROFIT_AVG': -20.92, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 30.1, 'COMMISSION_AVGRATIO': 21.52, 'GUARANTEE_MINPRICE': 1.1, 'GUARANTEE_MAXPRICE': 60.0, 'GUARANTEE_AVGPRICE': 19.9, 'MINTURNOVER': 18.0, 'GUARANTEERATIO': 15.0, 'ROYALTY_PRICE': 367564.6, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 97.26, 'PROFIT_AMOUNT': 315046.85, 'PROFIT_TOTALAMOUNT': 315046.85, 'PROFIT_INFO': '第1期：31.50万元', 'COMMISSION_RATIO': '18%-20%', 'REVENUE_LASTAMOUNT': 1122785.74, 'REVENUE_AVGAMOUNT': 93565.48, 'ADJUST_RATIO': 20.0, 'ADJUST_RENT': 22.46, 'ADJUST_AMOUNT': 4.46, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '47.09-125.40', 'INVESTMENTANALYSIS_ID': 146, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2306,2308', 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'SHOPROYALTY_ID': 4098, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 30.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 450383.08, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 176524.52, 'PROFIT_TOTALAMOUNT': 683134.19, 'PROFIT_INFO': '第1期：50.66万元，第2期：17.65万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 1811285.4, 'REVENUE_AVGAMOUNT': 98452.81, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 47.09, 'ADJUST_AMOUNT': 17.09, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '138.80', 'INVESTMENTANALYSIS_ID': 147, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2382,2383', 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'SHOPROYALTY_ID': 4094, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 126.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 1667473.64, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 764778.03, 'PROFIT_TOTALAMOUNT': 2762362.42, 'PROFIT_INFO': '第1期：199.75万元，第2期：76.47万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 5338492.0, 'REVENUE_AVGAMOUNT': 276088.7, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 138.8, 'ADJUST_AMOUNT': 12.8, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2018/2/1', 'PROJECT_ENDDATE': '2028/1/31', 'ADJUST_RATIORANGE': '20', 'ADJUST_RENTRANGE': '132.17', 'INVESTMENTANALYSIS_ID': 148, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '3064', 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'SHOPROYALTY_ID': 2945, 'BUSINESS_TRADE': 227, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 13, 'TRADE_PROJECTCOUNT': 15, 'PROFIT_AVG': -38.44, 'COMMISSION_MINRATIO': 8.0, 'COMMISSION_MAXRATIO': 35.0, 'COMMISSION_AVGRATIO': 19.33, 'GUARANTEE_MINPRICE': 7.0, 'GUARANTEE_MAXPRICE': 50.0, 'GUARANTEE_AVGPRICE': 29.79, 'MINTURNOVER': 40.0, 'GUARANTEERATIO': 16.0, 'ROYALTY_PRICE': 0.0, 'RENT_RATIO': 0.0, 'PERIOD_DEGREE': 92.33, 'PROFIT_AMOUNT': 2355426.57, 'PROFIT_TOTALAMOUNT': 15151589.24, 'PROFIT_INFO': '第1期：0万元，第2期：0万元，第3期：0万元，第4期：295.99万元，第5期：260.90万元，第6期：333.89万元，第7期：388.81万元，第8期：235.54万元', 'COMMISSION_RATIO': '15%-20%', 'REVENUE_LASTAMOUNT': 6608543.79, 'REVENUE_AVGAMOUNT': 379022.08, 'ADJUST_RATIO': 20.0, 'ADJUST_RENT': 132.17, 'ADJUST_AMOUNT': 92.17, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '75.51-125.40', 'INVESTMENTANALYSIS_ID': 149, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'SHOPROYALTY_ID': 4102, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 50.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 524524.08, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 126864.68, 'PROFIT_TOTALAMOUNT': 1027209.54, 'PROFIT_INFO': '第1期：90.03万元，第2期：12.68万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 2904355.8, 'REVENUE_AVGAMOUNT': 112052.78, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 75.51, 'ADJUST_AMOUNT': 25.51, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/2/14', 'ADJUST_RATIORANGE': '28-32.20', 'ADJUST_RENTRANGE': '95.89', 'INVESTMENTANALYSIS_ID': 150, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'SHOPROYALTY_ID': 4110, 'BUSINESS_TRADE': 234, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 12, 'TRADE_PROJECTCOUNT': 37, 'PROFIT_AVG': -16.6, 'COMMISSION_MINRATIO': 23.0, 'COMMISSION_MAXRATIO': 50.2, 'COMMISSION_AVGRATIO': 32.2, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 180.0, 'GUARANTEE_AVGPRICE': 89.92, 'MINTURNOVER': 126.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 1043528.57, 'RENT_RATIO': 82.82, 'PERIOD_DEGREE': 88.49, 'PROFIT_AMOUNT': -257172.1, 'PROFIT_TOTALAMOUNT': 662900.4, 'PROFIT_INFO': '第1期：92.00万元，第2期：-25.71万元', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': 3424569.8, 'REVENUE_AVGAMOUNT': 148457.63, 'ADJUST_RATIO': 28.0, 'ADJUST_RENT': 95.89, 'ADJUST_AMOUNT': -30.11, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '28-28.04', 'ADJUST_RENTRANGE': '55.12-77.76', 'INVESTMENTANALYSIS_ID': 151, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_NAME': '新桥服务区烧饼合同项目', 'SHOPROYALTY_ID': 4106, 'BUSINESS_TRADE': 243, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 40, 'TRADE_PROJECTCOUNT': 73, 'PROFIT_AVG': -73.24, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 50.2, 'COMMISSION_AVGRATIO': 28.04, 'GUARANTEE_MINPRICE': 5.0, 'GUARANTEE_MAXPRICE': 252.0, 'GUARANTEE_AVGPRICE': 77.76, 'MINTURNOVER': 45.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 476249.76, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': -130354.88, 'PROFIT_TOTALAMOUNT': 453220.46, 'PROFIT_INFO': '第1期：58.35万元，第2期：-13.03万元', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': 1968394.76, 'REVENUE_AVGAMOUNT': 71264.68, 'ADJUST_RATIO': 28.0, 'ADJUST_RENT': 55.12, 'ADJUST_AMOUNT': 10.12, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `149.84 ms`
新 API 状态: `200`，耗时 `5.23 ms`

### Analysis/GetNestingIAReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ContainHoliday": 0, "ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetNestingIAReport | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetNestingIAReport |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 7, 'TotalCount': 7, 'List': [{'node': {'SPREGIONTYPE_ID': 0, 'SPREGIONTYPE_NAME': '合计', 'SPREGIONTYPE_INDEX': None, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'ADJUST_RATIORANGE': None, 'ADJUST_RENTRANGE': None, 'INVESTMENTANALYSIS_ID': None, 'SERVERPART_ID': None, 'SERVERPART_NAME': None, 'SERVERPART_TYPE': None, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': None, 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': None, 'BUSINESS_PTRADE': None, 'TRADE_SHOPCOUNT': None, 'TRADE_PROJECTCOUNT': None, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': None, 'COMMISSION_MAXRATIO': None, 'COMMISSION_AVGRATIO': None, 'GUARANTEE_MINPRICE': None, 'GUARANTEE_MAXPRICE': None, 'GUARANTEE_AVGPRICE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ROYALTY_PRICE': 452.97, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': 335.11, 'PROFIT_TOTALAMOUNT': 2105.54, 'PROFIT_INFO': None, 'COMMISSION_RATIO': None, 'REVENUE_LASTAMOUNT': 2317.84, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': 132.04, 'HOLIDAY_TYPE': None, 'INVESTMENTANALYSIS_STATE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'ADJUST_RATIORANGE': None, 'ADJUST_RENTRANGE': None, 'INVESTMENTANALYSIS_ID': None, 'SERVERPART_ID': None, 'SERVERPART_NAME': None, 'SERVERPART_TYPE': None, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': None, 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': None, 'BUSINESS_PTRADE': None, 'TRADE_SHOPCOUNT': None, 'TRADE_PROJECTCOUNT': None, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': None, 'COMMISSION_MAXRATIO': None, 'COMMISSION_AVGRATIO': None, 'GUARANTEE_MINPRICE': None, 'GUARANTEE_MAXPRICE': None, 'GUARANTEE_AVGPRICE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ROYALTY_PRICE': 452.97, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': 335.11, 'PROFIT_TOTALAMOUNT': 2105.54, 'PROFIT_INFO': None, 'COMMISSION_RATIO': None, 'REVENUE_LASTAMOUNT': 2317.84, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': 132.04, 'HOLIDAY_TYPE': None, 'INVESTMENTANALYSIS_STATE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'INVESTMENTANALYSIS_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'ADJUST_RATIORANGE': None, 'ADJUST_RENTRANGE': None, 'INVESTMENTANALYSIS_ID': None, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': None, 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': None, 'BUSINESS_PTRADE': None, 'TRADE_SHOPCOUNT': None, 'TRADE_PROJECTCOUNT': None, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': None, 'COMMISSION_MAXRATIO': None, 'COMMISSION_AVGRATIO': None, 'GUARANTEE_MINPRICE': None, 'GUARANTEE_MAXPRICE': None, 'GUARANTEE_AVGPRICE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ROYALTY_PRICE': 452.97, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': 335.11, 'PROFIT_TOTALAMOUNT': 2105.54, 'PROFIT_INFO': None, 'COMMISSION_RATIO': None, 'REVENUE_LASTAMOUNT': 2317.84, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': 132.04, 'HOLIDAY_TYPE': None, 'INVESTMENTANALYSIS_STATE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'INVESTMENTANALYSIS_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2025/1/14', 'PROJECT_ENDDATE': '2028/1/13', 'ADJUST_RATIORANGE': '20-21.52', 'ADJUST_RENTRANGE': '22.46', 'INVESTMENTANALYSIS_ID': 145, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '5626,5626,5627', 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_NAME': '新桥服务区361服饰项目', 'SHOPROYALTY_ID': 4481, 'BUSINESS_TRADE': 247, 'BUSINESS_PTRADE': 222, 'TRADE_SHOPCOUNT': 6, 'TRADE_PROJECTCOUNT': 10, 'PROFIT_AVG': -20.92, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 30.1, 'COMMISSION_AVGRATIO': 21.52, 'GUARANTEE_MINPRICE': 1.1, 'GUARANTEE_MAXPRICE': 60.0, 'GUARANTEE_AVGPRICE': 19.9, 'MINTURNOVER': 18.0, 'GUARANTEERATIO': 15.0, 'ROYALTY_PRICE': 36.75, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 97.26, 'PROFIT_AMOUNT': 31.5, 'PROFIT_TOTALAMOUNT': 31.5, 'PROFIT_INFO': '第1期：31.50万元', 'COMMISSION_RATIO': '18%-20%', 'REVENUE_LASTAMOUNT': 112.27, 'REVENUE_AVGAMOUNT': 9.35, 'ADJUST_RATIO': 20.0, 'ADJUST_RENT': 22.46, 'ADJUST_AMOUNT': 4.46, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '47.09-125.40', 'INVESTMENTANALYSIS_ID': 146, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2306,2308', 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'SHOPROYALTY_ID': 4098, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 30.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 45.03, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 17.65, 'PROFIT_TOTALAMOUNT': 68.31, 'PROFIT_INFO': '第1期：50.66万元，第2期：17.65万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 181.12, 'REVENUE_AVGAMOUNT': 9.84, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 47.09, 'ADJUST_AMOUNT': 17.09, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '138.80', 'INVESTMENTANALYSIS_ID': 147, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2382,2383', 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'SHOPROYALTY_ID': 4094, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 126.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 166.74, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 76.47, 'PROFIT_TOTALAMOUNT': 276.23, 'PROFIT_INFO': '第1期：199.75万元，第2期：76.47万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 533.84, 'REVENUE_AVGAMOUNT': 27.6, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 138.8, 'ADJUST_AMOUNT': 12.8, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2018/2/1', 'PROJECT_ENDDATE': '2028/1/31', 'ADJUST_RATIORANGE': '20', 'ADJUST_RENTRANGE': '132.17', 'INVESTMENTANALYSIS_ID': 148, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '3064', 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'SHOPROYALTY_ID': 2945, 'BUSINESS_TRADE': 227, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 13, 'TRADE_PROJECTCOUNT': 15, 'PROFIT_AVG': -38.44, 'COMMISSION_MINRATIO': 8.0, 'COMMISSION_MAXRATIO': 35.0, 'COMMISSION_AVGRATIO': 19.33, 'GUARANTEE_MINPRICE': 7.0, 'GUARANTEE_MAXPRICE': 50.0, 'GUARANTEE_AVGPRICE': 29.79, 'MINTURNOVER': 40.0, 'GUARANTEERATIO': 16.0, 'ROYALTY_PRICE': 0.0, 'RENT_RATIO': 0.0, 'PERIOD_DEGREE': 92.33, 'PROFIT_AMOUNT': 235.54, 'PROFIT_TOTALAMOUNT': 1515.15, 'PROFIT_INFO': '第1期：0万元，第2期：0万元，第3期：0万元，第4期：295.99万元，第5期：260.90万元，第6期：333.89万元，第7期：388.81万元，第8期：235.54万元', 'COMMISSION_RATIO': '15%-20%', 'REVENUE_LASTAMOUNT': 660.85, 'REVENUE_AVGAMOUNT': 37.9, 'ADJUST_RATIO': 20.0, 'ADJUST_RENT': 132.17, 'ADJUST_AMOUNT': 92.17, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '75.51-125.40', 'INVESTMENTANALYSIS_ID': 149, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'SHOPROYALTY_ID': 4102, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 50.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 52.45, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 12.68, 'PROFIT_TOTALAMOUNT': 102.72, 'PROFIT_INFO': '第1期：90.03万元，第2期：12.68万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 290.43, 'REVENUE_AVGAMOUNT': 11.2, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 75.51, 'ADJUST_AMOUNT': 25.51, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/2/14', 'ADJUST_RATIORANGE': '28-32.20', 'ADJUST_RENTRANGE': '95.89', 'INVESTMENTANALYSIS_ID': 150, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'SHOPROYALTY_ID': 4110, 'BUSINESS_TRADE': 234, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 12, 'TRADE_PROJECTCOUNT': 37, 'PROFIT_AVG': -16.6, 'COMMISSION_MINRATIO': 23.0, 'COMMISSION_MAXRATIO': 50.2, 'COMMISSION_AVGRATIO': 32.2, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 180.0, 'GUARANTEE_AVGPRICE': 89.92, 'MINTURNOVER': 126.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 104.35, 'RENT_RATIO': 82.82, 'PERIOD_DEGREE': 88.49, 'PROFIT_AMOUNT': -25.71, 'PROFIT_TOTALAMOUNT': 66.29, 'PROFIT_INFO': '第1期：92.00万元，第2期：-25.71万元', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': 342.45, 'REVENUE_AVGAMOUNT': 14.84, 'ADJUST_RATIO': 28.0, 'ADJUST_RENT': 95.89, 'ADJUST_AMOUNT': -30.11, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '28-28.04', 'ADJUST_RENTRANGE': '55.12-77.76', 'INVESTMENTANALYSIS_ID': 151, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_NAME': '新桥服务区烧饼合同项目', 'SHOPROYALTY_ID': 4106, 'BUSINESS_TRADE': 243, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 40, 'TRADE_PROJECTCOUNT': 73, 'PROFIT_AVG': -73.24, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 50.2, 'COMMISSION_AVGRATIO': 28.04, 'GUARANTEE_MINPRICE': 5.0, 'GUARANTEE_MAXPRICE': 252.0, 'GUARANTEE_AVGPRICE': 77.76, 'MINTURNOVER': 45.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 47.62, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': -13.03, 'PROFIT_TOTALAMOUNT': 45.32, 'PROFIT_INFO': '第1期：58.35万元，第2期：-13.03万元', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': 196.83, 'REVENUE_AVGAMOUNT': 7.12, 'ADJUST_RATIO': 28.0, 'ADJUST_RENT': 55.12, 'ADJUST_AMOUNT': 10.12, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}]}]}]}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `248.23 ms`
新 API 状态: `200`，耗时 `5.0 ms`

### Analysis/GetPERIODMONTHPROFITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PERIODMONTHPROFITId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPERIODMONTHPROFITDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPERIODMONTHPROFITDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PERIODMONTHPROFIT_ID': None, 'STATISTICS_MONTH': None, 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': None, 'SERVERPART_ID': None, 'SERVERPART_IDS': None, 'SERVERPART_NAME': None, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESS_STATE': None, 'BUSINESS_STATES': None, 'BUSINESS_TRADE': None, 'MERCHANTS_ID': None, 'MERCHANTS_NAME': None, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'GUARANTEE_PRICE': None, 'SHOPROYALTY_ID': None, 'SHOPROYALTY_IDS': None, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'SETTLEMENT_MODES': None, 'SETTLEMENT_MODESS': None, 'BUSINESS_TYPE': None, 'BUSINESS_TYPES': None, 'RENTFEE': None, 'MINTURNOVER': None, 'ACTUAL_RATIO': None, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': None, 'TICKET_COUNT': None, 'ROYALTY_PRICE': None, 'ROYALTY_THEORY': None, 'SUBROYALTY_THEORY': None, 'PROFIT_AMOUNT': None, 'PROFIT_SD': None, 'PROFIT_AVG': None, 'COST_AMOUNT': None, 'COST_RATE': None, 'CA_COST': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'OTHER_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'MONTH_COUNT': None, 'GUARANTEERATIO': None, 'WARNING_TYPE': None, 'WARNING_TYPES': None, 'WARNING_CONTENT': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `168.35 ms`
新 API 状态: `200`，耗时 `4.5 ms`

### Analysis/GetPERIODMONTHPROFITList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"PERIODMONTHPROFIT_ID": 651}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPERIODMONTHPROFITList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPERIODMONTHPROFITList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'PERIODMONTHPROFIT_ID': 651, 'STATISTICS_MONTH': '2024/05', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'BUSINESSPROJECT_ID': 668, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '清溪服务区轻餐饮QX-07项目', 'SERVERPART_ID': 503, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '清溪服务区', 'SERVERPARTSHOP_ID': '1374,1375', 'SERVERPARTSHOP_NAME': '桐乡盛开源(粮大年)', 'BUSINESS_STATE': 1000, 'BUSINESS_STATES': None, 'BUSINESS_TRADE': 215, 'MERCHANTS_ID': -2036, 'MERCHANTS_NAME': '桐乡市盛开源高速公路服务区经营管理有限公司', 'PROJECT_STARTDATE': '2023/06/03', 'PROJECT_ENDDATE': '2026/06/02', 'GUARANTEE_PRICE': 105.0, 'SHOPROYALTY_ID': 2025, 'SHOPROYALTY_IDS': None, 'BUSINESS_PERIOD': '', 'PERIOD_INDEX': None, 'STARTDATE': '2023/06/03', 'ENDDATE': '2024/06/02', 'SETTLEMENT_MODES': 3000, 'SETTLEMENT_MODESS': None, 'BUSINESS_TYPE': 1000, 'BUSINESS_TYPES': None, 'RENTFEE': None, 'MINTURNOVER': 350000.0, 'ACTUAL_RATIO': 50.35, 'COMMISSION_RATIO': 28.0, 'REVENUE_AMOUNT': 1373523.0, 'TICKET_COUNT': 2023, 'ROYALTY_PRICE': 688560.35, 'ROYALTY_THEORY': 691533.94, 'SUBROYALTY_THEORY': 678378.97, 'PROFIT_AMOUNT': 62341.04, 'PROFIT_SD': 37405.78, 'PROFIT_AVG': 10390.17, 'COST_AMOUNT': 616037.93, 'COST_RATE': 20.0, 'CA_COST': None, 'LABOURS_COUNT': 4.0, 'LABOURS_WAGE': 6000.0, 'DEPRECIATION_EXPENSE': 10.0, 'OTHER_EXPENSE': 2.0, 'DEPRECIATION_YEAR': 3, 'MONTH_COUNT': 12.0, 'GUARANTEERATIO': 41.1, 'WARNING_TYPE': None, 'WARNING_TYPES': None, 'WARNING_CONTENT': '', 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2025-05-14T19:25:25'}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `157.92 ms`
新 API 状态: `200`，耗时 `4.04 ms`

### Analysis/GetPREFERRED_RATINGDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPREFERRED_RATINGDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPREFERRED_RATINGDetail |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Analysis/GetPREFERRED_RATINGDetail”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `8.34 ms`
新 API 状态: `200`，耗时 `6.93 ms`

### Analysis/GetPREFERRED_RATINGList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPREFERRED_RATINGList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPREFERRED_RATINGList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 查询失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `18.56 ms`
新 API 状态: `200`，耗时 `3.38 ms`

### Analysis/GetPROFITCONTRIBUTEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROFITCONTRIBUTEId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPROFITCONTRIBUTEDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPROFITCONTRIBUTEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PROFITCONTRIBUTE_ID': 1, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 490, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '周潭服务区', 'SERVERPARTSHOP_ID': '3912,3914', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '佐丹奴', 'BUSINESSPROJECT_ID': 36, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '周潭服务区（品牌服装）项目', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 0, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:30:43', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 0, 'PROFITCONTRIBUTE_DESC': ''} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `179.72 ms`
新 API 状态: `200`，耗时 `4.61 ms`

### Analysis/GetPROFITCONTRIBUTEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPROFITCONTRIBUTEList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPROFITCONTRIBUTEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 3003, 'List': [{'PROFITCONTRIBUTE_ID': 7, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3058,3059', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '鲜道寿司', 'BUSINESSPROJECT_ID': 50, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '新桥服务区（品牌寿司(新业态））项目', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 0, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:30:43', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 0, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 37, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 0, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 41.66, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:30:43', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 3960, 'PROFITCONTRIBUTE_PID': 270, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '1806,1807', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助售货机', 'BUSINESSPROJECT_ID': 884, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '新桥服务区【24小时自助服务】', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 1.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:48:23', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': 'REVENUE_INCRATE_QOQ:|VEHICLE_INCREASE_QOQ:18.64'}, {'PROFITCONTRIBUTE_ID': 445, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 0, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 51.85, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:30:43', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 446, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 0, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 24.82, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:30:43', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 447, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 0, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 48.86, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2024-11-01T16:30:43', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 831, 'PROFITCONTRIBUTE_PID': 484, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.6, 'SABFI_SCORE': 10.6, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2025-05-14T19:35:38', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 832, 'PROFITCONTRIBUTE_PID': 463, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 9.08, 'SABFI_SCORE': 9.08, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2025-05-14T19:35:38', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}, {'PROFITCONTRIBUTE_ID': 833, 'PROFITCONTRIBUTE_PID': 446, 'STATISTICS_DATE': '2024/10', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 9.4, 'SABFI_SCORE': 9.4, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'RECORD_DATE': '2025-05-14T19:35:38', 'CALCULATE_SELFSHOP': 1, 'PROFITCONTRIBUTE_STATE': 1, 'PROFITCONTRIBUTE_DESC': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `554.15 ms`
新 API 状态: `200`，耗时 `556.36 ms`

### Analysis/GetPROMPTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROMPTId": 5}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPROMPTDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPROMPTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PROMPT_ID': 5, 'PROMPT_TYPE': 1000, 'PROMPT_TYPES': None, 'PROMPT_CONTENT': '       请结合问题解析关键字和用户的提问，严谨分析数据字段内容，给出经营数据分析总结，无需建议，注意段落区分且清晰。\n\n       1、先有概述，分析整理数据统计汇总、统计时间、同环比日期和天数，金额和车辆数据请用万为单位，段落清晰；\n\n       2、如果查询日期内包含节假日概念，请给与具体日期说明，同比数据请注明日期比对天数，这里应该考虑车流的增减幅度对营收的影响；\n\n       3、整体服务区营收、车流、客单、盈利（甲方与商家）情况分析，重点关注同环比车流对各项数据造成的变化，根据合同时间，关注是否有新增或者关闭的门店；\n\n       4、分析每个在营门店的营收、车流、客单、盈利（甲方与商家）情况并分析，分析依据如下：\n---自营代表甲方自主经营，租赁代表甲方收取保底+提成，请分开展示；\n---根据合同时间判断门店是否已到期，已到期门店不进行数据分析；\n---如出现营收增幅与整体入区车流偏差较大的情况请列出，如车流增幅大于营收增幅，代表业态门店获客能力较差；\n---甲方更多收入的门店比较优秀，请说明；\n---需要结合客单量和客单均价来体现门店受消费者的喜爱程度，增幅较大的客单量和客单均价代表受顾客喜爱；\n\n      5、如有多服务区，结合多个服务区的经营数据进行分析，同比变化最大的需重点列出说明，没有则不进行比较；\n\n      6、暂时不结合区域周边县市（列出名字）的经济特色进行分析考虑；\n\n      7、总结内容提出对一些问题的思考逻辑。\n\n其他注意：\n      1、经营数据无需区分东（南）区或者西（北）区分析，且不要说出根据JSON数据的文字；\n      2、甲方收入=盈利收入=业主收入=驿达收入，统一用驿达公司表示；\n      3、如果需要更加深入的分析，请提出需要补充的数据内容，并用-----分隔。\n ', 'PROMPT_SWITCH': 1, 'STAFF_ID': 2785, 'STAFF_NAME': '严琅杰', 'OPERATE_DATE': '2025/3/28 10:24:37', 'OPERATE_DATE_Start': None, 'OPERATE_DATE_End': None, 'PROMPT_STATE': None, 'PROMPT_DESC': '引入地图的语义，对返回过来的表格或文字进行优化'} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `170.13 ms`
新 API 状态: `200`，耗时 `4.72 ms`

### Analysis/GetPROMPTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPROMPTList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPROMPTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 3, 'List': [{'PROMPT_ID': 5, 'PROMPT_TYPE': 1000, 'PROMPT_TYPES': None, 'PROMPT_CONTENT': '       请结合问题解析关键字和用户的提问，严谨分析数据字段内容，给出经营数据分析总结，无需建议，注意段落区分且清晰。\n\n       1、先有概述，分析整理数据统计汇总、统计时间、同环比日期和天数，金额和车辆数据请用万为单位，段落清晰；\n\n       2、如果查询日期内包含节假日概念，请给与具体日期说明，同比数据请注明日期比对天数，这里应该考虑车流的增减幅度对营收的影响；\n\n       3、整体服务区营收、车流、客单、盈利（甲方与商家）情况分析，重点关注同环比车流对各项数据造成的变化，根据合同时间，关注是否有新增或者关闭的门店；\n\n       4、分析每个在营门店的营收、车流、客单、盈利（甲方与商家）情况并分析，分析依据如下：\n---自营代表甲方自主经营，租赁代表甲方收取保底+提成，请分开展示；\n---根据合同时间判断门店是否已到期，已到期门店不进行数据分析；\n---如出现营收增幅与整体入区车流偏差较大的情况请列出，如车流增幅大于营收增幅，代表业态门店获客能力较差；\n---甲方更多收入的门店比较优秀，请说明；\n---需要结合客单量和客单均价来体现门店受消费者的喜爱程度，增幅较大的客单量和客单均价代表受顾客喜爱；\n\n      5、如有多服务区，结合多个服务区的经营数据进行分析，同比变化最大的需重点列出说明，没有则不进行比较；\n\n      6、暂时不结合区域周边县市（列出名字）的经济特色进行分析考虑；\n\n      7、总结内容提出对一些问题的思考逻辑。\n\n其他注意：\n      1、经营数据无需区分东（南）区或者西（北）区分析，且不要说出根据JSON数据的文字；\n      2、甲方收入=盈利收入=业主收入=驿达收入，统一用驿达公司表示；\n      3、如果需要更加深入的分析，请提出需要补充的数据内容，并用-----分隔。\n ', 'PROMPT_SWITCH': 1, 'STAFF_ID': 2785, 'STAFF_NAME': '严琅杰', 'OPERATE_DATE': '2025/3/28 10:24:37', 'OPERATE_DATE_Start': None, 'OPERATE_DATE_End': None, 'PROMPT_STATE': None, 'PROMPT_DESC': '引入地图的语义，对返回过来的表格或文字进行优化'}, {'PROMPT_ID': 6, 'PROMPT_TYPE': 2000, 'PROMPT_TYPES': None, 'PROMPT_CONTENT': '云南高速·智慧大屏数据洞察官 Prompt · V3（决策层友好版）\n\n你是“云南高速服务区智慧大屏”的数据洞察官，服务对象是集团高层管理者。你的职责是通过实时和历史结构化数据，提供有深度、节奏感、判断力、正负并重的运营播报，支持科学决策、运营预判与策略部署。\n？？【一、输出结构要求】（保留七段结构，优化语气和排序）\n\n每次播报需包含以下内容，建议1200字以内，语言自然流畅、避免堆砌数字：\n\n    今日亮点速览\n\n        优先输出关键经营表现中的积极变化、业务高点、优秀片区、数据新突破，树立正向感知。\n\n    波动与关注项\n\n        概括今日出现的波动或风险行为，简明归因，不夸张渲染，强调“可控+建议”。\n\n    月度趋势观察\n\n        判断当前月是否延续预期节奏，有无提前透支或滞后，指出需持续关注的变化项。\n\n    历史节奏对标\n\n        结合去年同期与上一季度，判断当前处于哪种阶段（爬坡、收缩、冲刺等），支持节奏判断。\n\n    策略建议精要\n\n        给出少而精、能落地的策略建议，适度点出片区/业务优先级，避免泛泛空话。\n\n    关键节点提醒\n\n        提前预警即将到来的节假日、季度切换或特殊事件，并建议提前部署内容。\n\n    运营协同建议\n\n        强调系统保障、权限设置、数据补录、行为闭环等底层机制，保障整体运行质量。\n\n？？？【二、语气与风格要求】\n\n    基调务实积极：正面 + 中性 + 预警并重，杜绝全是问题或消极分析；\n\n    语言自然有温度：像是一个懂业务、有判断力的“懂行人”在向高层“说话”；\n\n    判断优于数据堆砌：数据仅作为支撑，应以“趋势/节奏/建议”为主角；\n\n    避免模板腔：不使用模板化句式如“建议加强…”，鼓励定制化表达；\n\n    视角结构化：从“数据→发现→判断→建议”建立因果链条；\n\n？？？【三、字段兼容（自动适配缺失）】\n\n你可以处理的数据字段包括但不限于：\n\n    实时类：今日车流、营收、加水、油品、充电、门店收入等；\n\n    趋势类：月度营收、季度效益、区域表现；\n\n    异常类：特情行为、抽查异常、交易波动；\n\n    客群类：年龄性别结构、消费偏好、消费时段、品牌偏好；\n\n    结构类：片区营收占比、业态结构占比、节假日结构等；\n\n    缺失字段时请智能跳过，整体不出错。\n\n？？【四、命令支持】\n用户提问\t你要执行的任务\n“请生成今日运营播报”\t启动七段式“数据洞察型运营简报”输出\n“请简明汇报今日情况”\t输出带正向亮点的简要摘要\n“聚焦滇中片区”\t输出滇中片区的趋势、亮点、风险、建议\n“暑期节奏提醒”\t输出未来高峰节点 + 重点片区策略部署\n？？【启动规则】\n\n一旦接收到结构化数据，立即进入“数据洞察官”角色，生成自然语言播报内容。字段缺失不报错，内容必须整体通顺、具判断力、可执行。', 'PROMPT_SWITCH': 1, 'STAFF_ID': 2785, 'STAFF_NAME': '严琅杰', 'OPERATE_DATE': '2025/6/24 16:12:51', 'OPERATE_DATE_Start': None, 'OPERATE_DATE_End': None, 'PROMPT_STATE': None, 'PROMPT_DESC': '为true时会默认补充上接口配置说明,即后缀文字'}, {'PROMPT_ID': 7, 'PROMPT_TYPE': None, 'PROMPT_TYPES': None, 'PROMPT_CONTENT': '', 'PROMPT_SWITCH': None, 'STAFF_ID': None, 'STAFF_NAME': '', 'OPERATE_DATE': None, 'OPERATE_DATE_Start': None, 'OPERATE_DATE_End': None, 'PROMPT_STATE': 0, 'PROMPT_DESC': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `161.82 ms`
新 API 状态: `200`，耗时 `982.04 ms`

### Analysis/GetPeriodMonthlyList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416, "StatisticsMonth": "202512"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPeriodMonthlyList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPeriodMonthlyList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': None, 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': None, 'SERVERPART_NAME': None, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESS_STATE': None, 'BUSINESS_TRADE': None, 'MERCHANTS_ID': None, 'MERCHANTS_NAME': None, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'GUARANTEE_PRICE': None, 'BUSINESS_TYPE': None, 'SETTLEMENT_MODES': None, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': 0.0, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 60.55, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 699654.47, 'COST_AMOUNT': 367486.47, 'ROYALTY_PRICE': 211667.27, 'ROYALTY_THEORY': 423654.53, 'SUBROYALTY_THEORY': 274536.2, 'PROFIT_AMOUNT': -54730.99, 'PROFIT_RATE': None, 'PROFIT_SD': None, 'PROFIT_AVG': None, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 27752, 'CA_COST': 13.24, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': [{'node': {'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': None, 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESS_STATE': None, 'BUSINESS_TRADE': None, 'MERCHANTS_ID': None, 'MERCHANTS_NAME': None, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'GUARANTEE_PRICE': None, 'BUSINESS_TYPE': None, 'SETTLEMENT_MODES': None, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': 0.0, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 60.55, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 699654.47, 'COST_AMOUNT': 367486.47, 'ROYALTY_PRICE': 211667.27, 'ROYALTY_THEORY': 423654.53, 'SUBROYALTY_THEORY': 274536.2, 'PROFIT_AMOUNT': -54730.99, 'PROFIT_RATE': None, 'PROFIT_SD': None, 'PROFIT_AVG': None, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 27752, 'CA_COST': 13.24, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': [{'node': {'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_NAME': '新桥服务区361服饰项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_NAME': '361度', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 247, 'MERCHANTS_ID': -2188, 'MERCHANTS_NAME': '河南省道和高速公路服务区经营管理有限公司', 'PROJECT_STARTDATE': '2025/01/14', 'PROJECT_ENDDATE': '2028/01/13', 'GUARANTEE_PRICE': 54.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 35.46, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 50697.0, 'COST_AMOUNT': 38583.84, 'ROYALTY_PRICE': 7096.05, 'ROYALTY_THEORY': 17979.32, 'SUBROYALTY_THEORY': 32585.07, 'PROFIT_AMOUNT': -5998.77, 'PROFIT_RATE': None, 'PROFIT_SD': 64942.0, 'PROFIT_AVG': 51949.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 303, 'CA_COST': 127.34, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 229, 'MERCHANTS_ID': -2115, 'MERCHANTS_NAME': '合肥市丁记米饺食品有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 90.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 36.01, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 60423.0, 'COST_AMOUNT': 40529.05, 'ROYALTY_PRICE': 15740.48, 'ROYALTY_THEORY': 21755.43, 'SUBROYALTY_THEORY': 38512.48, 'PROFIT_AMOUNT': -2016.57, 'PROFIT_RATE': None, 'PROFIT_SD': 34324.0, 'PROFIT_AVG': 28753.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 3681, 'CA_COST': 11.01, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 229, 'MERCHANTS_ID': -2114, 'MERCHANTS_NAME': '淮南丁家餐饮有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 378.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 54.37, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 213846.0, 'COST_AMOUNT': 71213.65, 'ROYALTY_PRICE': 57374.52, 'ROYALTY_THEORY': 116274.11, 'SUBROYALTY_THEORY': 96989.49, 'PROFIT_AMOUNT': 25775.84, 'PROFIT_RATE': None, 'PROFIT_SD': 112653.0, 'PROFIT_AVG': 126487.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 7502, 'CA_COST': 9.49, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 227, 'MERCHANTS_ID': -580, 'MERCHANTS_NAME': '安徽联升餐厅食品有限公司', 'PROJECT_STARTDATE': '2018/02/01', 'PROJECT_ENDDATE': '2028/01/31', 'GUARANTEE_PRICE': 400.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 9999, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 16.0, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 144796.87, 'COST_AMOUNT': 57403.81, 'ROYALTY_PRICE': 0.0, 'ROYALTY_THEORY': 23167.5, 'SUBROYALTY_THEORY': 121629.37, 'PROFIT_AMOUNT': 64225.56, 'PROFIT_RATE': None, 'PROFIT_SD': 480316.0, 'PROFIT_AVG': 389118.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 4089, 'CA_COST': 14.04, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 229, 'MERCHANTS_ID': -2116, 'MERCHANTS_NAME': '合肥书山有陆餐饮管理有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 150.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 59.72, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 81904.8, 'COST_AMOUNT': 44825.41, 'ROYALTY_PRICE': 37804.06, 'ROYALTY_THEORY': 48910.62, 'SUBROYALTY_THEORY': 32778.57, 'PROFIT_AMOUNT': -12046.84, 'PROFIT_RATE': None, 'PROFIT_SD': 33288.0, 'PROFIT_AVG': 20478.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 6411, 'CA_COST': 6.99, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 234, 'MERCHANTS_ID': -1116, 'MERCHANTS_NAME': '合肥王仁和米线餐饮管理有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/02/14', 'GUARANTEE_PRICE': 378.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 112.95, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 101447.8, 'COST_AMOUNT': 48734.01, 'ROYALTY_PRICE': 68105.66, 'ROYALTY_THEORY': 114586.78, 'SUBROYALTY_THEORY': -13413.17, 'PROFIT_AMOUNT': -62147.18, 'PROFIT_RATE': None, 'PROFIT_SD': 39837.0, 'PROFIT_AVG': -42611.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 3312, 'CA_COST': 14.71, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 947, 'BUSINESSPROJECT_NAME': '合肥蔚电科技有限公司', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '1878,1872,1877,1871,1874,1868,1870,1875,1876', 'SERVERPARTSHOP_NAME': '蔚来换电', 'BUSINESS_STATE': 3000, 'BUSINESS_TRADE': None, 'MERCHANTS_ID': -1636, 'MERCHANTS_NAME': '合肥蔚电科技有限公司', 'PROJECT_STARTDATE': '2021/12/01', 'PROJECT_ENDDATE': '2026/11/30', 'GUARANTEE_PRICE': 225.0, 'BUSINESS_TYPE': 2000, 'SETTLEMENT_MODES': 1000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': None, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 0.0, 'COST_AMOUNT': 0.0, 'ROYALTY_PRICE': 0.0, 'ROYALTY_THEORY': 38219.28, 'SUBROYALTY_THEORY': -38219.28, 'PROFIT_AMOUNT': 0.0, 'PROFIT_RATE': None, 'PROFIT_SD': 0.0, 'PROFIT_AVG': 0.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 0, 'CA_COST': None, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_NAME': '新桥服务区烧饼合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 243, 'MERCHANTS_ID': -2117, 'MERCHANTS_NAME': '合肥徽蕴堂餐饮管理有限责任公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 135.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 109.0, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 38327.0, 'COST_AMOUNT': 36109.85, 'ROYALTY_PRICE': 25546.5, 'ROYALTY_THEORY': 41776.05, 'SUBROYALTY_THEORY': -3552.89, 'PROFIT_AMOUNT': -39662.74, 'PROFIT_RATE': None, 'PROFIT_SD': 21923.0, 'PROFIT_AVG': -21851.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 2336, 'CA_COST': 15.46, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_NAME': '服务区自助售卖玩具机项目租赁合同新桥', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 246, 'MERCHANTS_ID': -2182, 'MERCHANTS_NAME': '江苏乾上乾贸易有限公司', 'PROJECT_STARTDATE': '2025/07/15', 'PROJECT_ENDDATE': '2028/07/14', 'GUARANTEE_PRICE': 3.03, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 1000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 12.0, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 8212.0, 'COST_AMOUNT': 30086.85, 'ROYALTY_PRICE': 0.0, 'ROYALTY_THEORY': 985.44, 'SUBROYALTY_THEORY': 7226.56, 'PROFIT_AMOUNT': -22860.29, 'PROFIT_RATE': None, 'PROFIT_SD': 7770.0, 'PROFIT_AVG': -14338.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 118, 'CA_COST': 254.97, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}]}]}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `323.05 ms`
新 API 状态: `200`，耗时 `4.22 ms`

### Analysis/GetRevenueEstimateList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416, "StatisticsMonth": "202512"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetRevenueEstimateList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetRevenueEstimateList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'REVENUE_DIFF': None, 'DIFFERENCE_RATE': None, 'VEHICLEAMOUNT_ID': None, 'STATISTICS_MONTH': None, 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': None, 'SERVERPART_IDS': None, 'SERVERPART_NAME': None, 'SERVERPART_REGION': None, 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': None, 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 0, 'PROVINCE_NAME': None, 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': None, 'CONSUMPTION_COEFFICIENT': None, 'VEHICLE_AMOUNT': None, 'ADJUST_COUNT': None, 'VEHICLE_ADJAMOUNT': None, 'REVENUE_ADJAMOUNT': 0.0, 'REVENUE_ACTAMOUNT': 0.0, 'VEHICLE_TOTALCOUNT': 0, 'VEHICLEAMOUNT_STATE': None, 'RECORD_DATE': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'REVENUE_DIFF': None, 'DIFFERENCE_RATE': None, 'VEHICLEAMOUNT_ID': None, 'STATISTICS_MONTH': None, 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': None, 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': None, 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': None, 'PROVINCE_NAME': None, 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': None, 'CONSUMPTION_COEFFICIENT': None, 'VEHICLE_AMOUNT': None, 'ADJUST_COUNT': None, 'VEHICLE_ADJAMOUNT': None, 'REVENUE_ADJAMOUNT': None, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': None, 'RECORD_DATE': None}, 'children': []}]}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `366.88 ms`
新 API 状态: `200`，耗时 `701.62 ms`

### Analysis/GetSENTENCEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SENTENCEId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetSENTENCEDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetSENTENCEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'SENTENCE_ID': 1, 'SENTENCE_TYPE': 1, 'SENTENCE_CONTENT': '新桥', 'SENTENCE_RESULT': '已标出位置', 'SENTENCE_STATE': 1, 'STAFF_ID': 2785, 'STAFF_NAME': '严琅杰', 'OPERATE_DATE': '2024/10/30 17:59:17', 'OPERATE_DATE_Start': None, 'OPERATE_DATE_End': None, 'DIALOG_CODE': '', 'SERVERPART_ID': '', 'ANALYSISRULE_ID': ''} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `132.03 ms`
新 API 状态: `200`，耗时 `43.22 ms`

### Analysis/GetSENTENCEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 99, "SearchParameter": {"SENTENCE_ID": 1}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetSENTENCEList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetSENTENCEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 99, 'TotalCount': 1, 'List': [{'SENTENCE_ID': 1, 'SENTENCE_TYPE': 1, 'SENTENCE_CONTENT': '新桥', 'SENTENCE_RESULT': '已标出位置', 'SENTENCE_STATE': 1, 'STAFF_ID': 2785, 'STAFF_NAME': '严琅杰', 'OPERATE_DATE': '2024/10/30 17:59:17', 'OPERATE_DATE_Start': None, 'OPERATE_DATE_End': None, 'DIALOG_CODE': '', 'SERVERPART_ID': '', 'ANALYSISRULE_ID': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `132.91 ms`
新 API 状态: `200`，耗时 `4.57 ms`

### Analysis/GetShopSABFIList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartId": 416, "StatisticsMonth": "202511"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetShopSABFIList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetShopSABFIList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': None, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': None, 'SERVERPART_IDS': None, 'SERVERPART_NAME': None, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': None, 'BUSINESSTRADETYPE': None, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': None, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': None, 'BUSINESSTRADETYPE': None, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': None, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168474, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 6.751000000000001, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181722, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 7.13, 'SABFI_SCORE': 7.13, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181723, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.55, 'SABFI_SCORE': 5.55, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168475, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 8.13, 'SABFI_SCORE': 8.13, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181724, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.0, 'SABFI_SCORE': 6.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181725, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.0, 'SABFI_SCORE': 6.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181726, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.08, 'SABFI_SCORE': 6.08, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168474, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168476, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 5.649, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181727, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.48, 'SABFI_SCORE': 10.48, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181728, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168477, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.64, 'SABFI_SCORE': 6.64, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181729, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 8.73, 'SABFI_SCORE': 8.73, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181730, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 7.79, 'SABFI_SCORE': 7.79, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181731, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 2.23, 'SABFI_SCORE': 2.23, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168476, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168478, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 15.065999999999999, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181732, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 26.29, 'SABFI_SCORE': 26.29, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181733, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 3.84, 'SABFI_SCORE': 3.84, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168479, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 12.34, 'SABFI_SCORE': 12.34, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181734, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.0, 'SABFI_SCORE': 6.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181735, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.0, 'SABFI_SCORE': 10.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181736, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.3, 'SABFI_SCORE': 5.3, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168478, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168480, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 9.075999999999999, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181737, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.91, 'SABFI_SCORE': 6.91, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181738, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 14.17, 'SABFI_SCORE': 14.17, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168481, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 4.91, 'SABFI_SCORE': 4.91, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181739, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.0, 'SABFI_SCORE': 6.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181740, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 9.6, 'SABFI_SCORE': 9.6, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181741, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 7.19, 'SABFI_SCORE': 7.19, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168480, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168482, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 9.316, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181742, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 18.49, 'SABFI_SCORE': 18.49, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181743, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168483, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 9.09, 'SABFI_SCORE': 9.09, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181744, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.0, 'SABFI_SCORE': 10.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181745, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 9.0, 'SABFI_SCORE': 9.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181746, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 2.02, 'SABFI_SCORE': 2.02, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168482, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168484, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 16.722, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181747, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 35.34, 'SABFI_SCORE': 35.34, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181748, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168485, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 11.51, 'SABFI_SCORE': 11.51, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181749, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.0, 'SABFI_SCORE': 10.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181750, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 8.51, 'SABFI_SCORE': 8.51, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181751, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 4.33, 'SABFI_SCORE': 4.33, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168484, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168486, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 11.364000000000003, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181752, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 25.66, 'SABFI_SCORE': 25.66, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181753, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168487, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 6.79, 'SABFI_SCORE': 6.79, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181754, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.0, 'SABFI_SCORE': 10.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181755, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.25, 'SABFI_SCORE': 5.25, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181756, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 2.17, 'SABFI_SCORE': 2.17, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168486, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168488, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 1.2280000000000002, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168489, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168490, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168491, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168492, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.0, 'SABFI_SCORE': 5.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168493, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 7.28, 'SABFI_SCORE': 7.28, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168488, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5298,5299', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168494, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 1.7200000000000002, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168495, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 11.1, 'SABFI_SCORE': 11.1, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.0, 'SABFI_SCORE': 5.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168494, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5299,5298', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '星巴克咖啡', 'BUSINESSPROJECT_ID': 1766, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168496, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 3.516, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168497, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168498, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168499, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 12.58, 'SABFI_SCORE': 12.58, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168500, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168501, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 4.88, 'SABFI_SCORE': 4.88, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168502, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.12, 'SABFI_SCORE': 5.12, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168496, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5653', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '詹记桃酥', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168460, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 28.029, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168461, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 40.0, 'SABFI_SCORE': 40.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168462, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 30.0, 'SABFI_SCORE': 30.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168463, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 9.83, 'SABFI_SCORE': 9.83, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168464, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168465, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.0, 'SABFI_SCORE': 5.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168466, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.63, 'SABFI_SCORE': 5.63, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168460, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3080,3081', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营超市', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 1, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168467, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 27.729, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168468, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 40.0, 'SABFI_SCORE': 40.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168469, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 30.0, 'SABFI_SCORE': 30.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168470, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 8.63, 'SABFI_SCORE': 8.63, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168471, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168472, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.0, 'SABFI_SCORE': 5.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168473, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.03, 'SABFI_SCORE': 5.03, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168467, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2328,2329', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自营老乡鸡', 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 2, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168503, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': None, 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': None, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': None, 'SABFI_SCORE': 3.127, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181757, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 1, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 2.55, 'SABFI_SCORE': 2.55, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181758, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 2, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 168504, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 3, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.92, 'SABFI_SCORE': 10.92, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181759, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 4, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 10.0, 'SABFI_SCORE': 10.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181760, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 5, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 5.22, 'SABFI_SCORE': 5.22, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': 181761, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 6, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 4.01, 'SABFI_SCORE': 4.01, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': '2026-01-07T14:54:16', 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'PROFITCONTRIBUTE_ID': None, 'PROFITCONTRIBUTE_PID': 168503, 'STATISTICS_DATE': '2025/11', 'STATISTICS_DATE_Start': None, 'STATISTICS_DATE_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_IDS': None, 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_IDS': None, 'BUSINESSPROJECT_NAME': '', 'BUSINESSTRADETYPE': 3, 'EVALUATE_TYPE': 7, 'EVALUATE_TYPES': None, 'EVALUATE_SCORE': 0.0, 'SABFI_SCORE': 0.0, 'SABFI_TYPE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'CALCULATE_SELFSHOP': None, 'PROFITCONTRIBUTE_STATE': None, 'PROFITCONTRIBUTE_DESC': None}, 'children': None}]}]}]}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `442.44 ms`
新 API 状态: `200`，耗时 `2239.39 ms`

### Analysis/GetVEHICLEAMOUNTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"VEHICLEAMOUNTId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetVEHICLEAMOUNTDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetVEHICLEAMOUNTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'VEHICLEAMOUNT_ID': 1, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': None, 'PROVINCE_NAME': '', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': None, 'CONSUMPTION_COEFFICIENT': None, 'VEHICLE_AMOUNT': None, 'ADJUST_COUNT': None, 'VEHICLE_ADJAMOUNT': None, 'REVENUE_ADJAMOUNT': 4907073.93, 'REVENUE_ACTAMOUNT': 4797970.55, 'VEHICLE_TOTALCOUNT': 296163, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `172.13 ms`
新 API 状态: `200`，耗时 `3.8 ms`

### Analysis/GetVEHICLEAMOUNTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetVEHICLEAMOUNTList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetVEHICLEAMOUNTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 588, 'List': [{'VEHICLEAMOUNT_ID': 2, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '小型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 94289, 'PROVINCE_NAME': '安徽省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 30156.0, 'CONSUMPTION_COEFFICIENT': 0.926901, 'VEHICLE_AMOUNT': 15.02, 'ADJUST_COUNT': 1.5, 'VEHICLE_ADJAMOUNT': 16.52, 'REVENUE_ADJAMOUNT': 1557448.88, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'}, {'VEHICLEAMOUNT_ID': 1, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': None, 'PROVINCE_NAME': '', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': None, 'CONSUMPTION_COEFFICIENT': None, 'VEHICLE_AMOUNT': None, 'ADJUST_COUNT': None, 'VEHICLE_ADJAMOUNT': None, 'REVENUE_ADJAMOUNT': 4907073.93, 'REVENUE_ACTAMOUNT': 4797970.55, 'VEHICLE_TOTALCOUNT': 296163, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'}, {'VEHICLEAMOUNT_ID': 3, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '中型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 0, 'PROVINCE_NAME': '安徽省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 30156.0, 'CONSUMPTION_COEFFICIENT': 0.926901, 'VEHICLE_AMOUNT': 15.02, 'ADJUST_COUNT': -1.5, 'VEHICLE_ADJAMOUNT': 13.51, 'REVENUE_ADJAMOUNT': 0.0, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'}, {'VEHICLEAMOUNT_ID': 4, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '大型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 18054, 'PROVINCE_NAME': '安徽省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 30156.0, 'CONSUMPTION_COEFFICIENT': 0.926901, 'VEHICLE_AMOUNT': 15.02, 'ADJUST_COUNT': -1.5, 'VEHICLE_ADJAMOUNT': 13.51, 'REVENUE_ADJAMOUNT': 243992.25, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'}, {'VEHICLEAMOUNT_ID': 5, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '小型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 45594, 'PROVINCE_NAME': '江苏省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 48126.0, 'CONSUMPTION_COEFFICIENT': 1.170945, 'VEHICLE_AMOUNT': 18.97, 'ADJUST_COUNT': 1.9, 'VEHICLE_ADJAMOUNT': 20.87, 'REVENUE_ADJAMOUNT': 951400.73, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'}, {'VEHICLEAMOUNT_ID': 6, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '中型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 0, 'PROVINCE_NAME': '江苏省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 48126.0, 'CONSUMPTION_COEFFICIENT': 1.170945, 'VEHICLE_AMOUNT': 18.97, 'ADJUST_COUNT': -1.9, 'VEHICLE_ADJAMOUNT': 17.07, 'REVENUE_ADJAMOUNT': 0.0, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:28'}, {'VEHICLEAMOUNT_ID': 7, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '大型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 9772, 'PROVINCE_NAME': '江苏省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 48126.0, 'CONSUMPTION_COEFFICIENT': 1.170945, 'VEHICLE_AMOUNT': 18.97, 'ADJUST_COUNT': -1.9, 'VEHICLE_ADJAMOUNT': 17.07, 'REVENUE_ADJAMOUNT': 166835.73, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:29'}, {'VEHICLEAMOUNT_ID': 8, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '小型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 23396, 'PROVINCE_NAME': '河南省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 26125.0, 'CONSUMPTION_COEFFICIENT': 0.862729, 'VEHICLE_AMOUNT': 13.98, 'ADJUST_COUNT': 0.08, 'VEHICLE_ADJAMOUNT': 14.06, 'REVENUE_ADJAMOUNT': 328849.68, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:29'}, {'VEHICLEAMOUNT_ID': 9, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start': None, 'STATISTICS_MONTH_End': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_REGION': '', 'SERVERPART_REGIONS': None, 'VEHICLE_TYPE': '中型车', 'VEHICLE_TYPES': None, 'VEHICLE_COUNT': 0, 'PROVINCE_NAME': '河南省', 'PROVINCE_NAMES': None, 'PERCAPITA_INCOME': 26125.0, 'CONSUMPTION_COEFFICIENT': 0.862729, 'VEHICLE_AMOUNT': 13.98, 'ADJUST_COUNT': -1.4, 'VEHICLE_ADJAMOUNT': 12.58, 'REVENUE_ADJAMOUNT': 0.0, 'REVENUE_ACTAMOUNT': None, 'VEHICLE_TOTALCOUNT': None, 'VEHICLEAMOUNT_STATE': 1, 'RECORD_DATE': '2024-11-15T13:58:29'}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `236.86 ms`
新 API 状态: `200`，耗时 `5.41 ms`

### BusinessMan/GetCOMMODITY_TEMPDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"COMMODITY_TEMPId": 43}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPDetail | 新 API: http://localhost:8080/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'COMMODITY_TEMP_ID': 43, 'DATA_TYPE': 1000, 'COMMODITY_ID': 221921, 'COMMODITY_TYPE': 975, 'COMMODITY_TYPENAME': '休闲食品类', 'COMMODITY_NAME': '百斯顿巴旦木(100g）', 'COMMODITY_BARCODE': '6920732301166', 'SERVERPART_ID': 553, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '开江服务区', 'BUSINESSTYPE': 1000, 'QUALIFICATION_ID': 252, 'QUALIFICATION_DATE': '2022/08/01', 'QUALIFICATION_DELAYDATE': None, 'STATISTICS_DATE': '2022/07/25', 'CREATE_DATE': '2022-07-25T04:00:00', 'STAFF_ID': None, 'STAFF_NAME': None, 'OPERATE_DATE': None, 'COMMODITY_TEMP_STATE': 1, 'COMMODITY_TEMP_DESC': None, 'SEARCH_STARTDATE': None, 'SEARCH_ENDDATE': None, 'OPERATE_STARTDATE': None, 'OPERATE_ENDDATE': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `212.66 ms`
新 API 状态: `200`，耗时 `4.23 ms`

### BusinessMan/GetCOMMODITY_TEMPList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITY_TEMP_ID": 10459}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPList | 新 API: http://localhost:8080/EShangApiMain/BusinessMan/GetCOMMODITY_TEMPList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'COMMODITY_TEMP_ID': 10459, 'DATA_TYPE': 1000, 'COMMODITY_ID': 362267, 'COMMODITY_TYPE': 975, 'COMMODITY_TYPENAME': '休闲食品类', 'COMMODITY_NAME': '卫龙大面筋辣条', 'COMMODITY_BARCODE': '6935284412178', 'SERVERPART_ID': 553, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '开江服务区', 'BUSINESSTYPE': 1000, 'QUALIFICATION_ID': 3265, 'QUALIFICATION_DATE': '2026/02/14', 'QUALIFICATION_DELAYDATE': None, 'STATISTICS_DATE': '2026/02/10', 'CREATE_DATE': '2026-02-10T04:00:04', 'STAFF_ID': None, 'STAFF_NAME': '', 'OPERATE_DATE': None, 'COMMODITY_TEMP_STATE': 1, 'COMMODITY_TEMP_DESC': '', 'SEARCH_STARTDATE': None, 'SEARCH_ENDDATE': None, 'OPERATE_STARTDATE': None, 'OPERATE_ENDDATE': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `213.06 ms`
新 API 状态: `200`，耗时 `4.93 ms`

### BusinessMan/GetUserList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ProvinceCode": "340000", "ServerpartId": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BusinessMan/GetUserList | 新 API: http://localhost:8080/EShangApiMain/BusinessMan/GetUserList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'StaticsModel', 'TotalCount'] |
| TotalCount | ❌ | 16 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ❌ | 16 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- Result_Data.StaticsModel: 新 API 多出该字段
- Result_Data.List: 列表长度不一致 (16 vs 0)
- Result_Data.TotalCount: 值不一致 (16 vs 0)
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `1962.54 ms`
新 API 状态: `200`，耗时 `4479.85 ms`

### Merchants/GetBusinessManDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessManId": 123}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetBusinessManDetail | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetBusinessManDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'OWNERUNIT_ID': 123, 'OWNERUNIT_PID': 98, 'PROVINCE_CODE': 330000, 'PROVINCE_BUSINESSCODE': None, 'OWNERUNIT_NAME': '殷雪艳', 'OWNERUNIT_EN': None, 'OWNERUNIT_NATURE': 2000, 'OWNERUNIT_GUID': 'f9d10a07-c00a-436c-a3d9-2f53131e01c1', 'OWNERUNIT_INDEX': 10, 'OWNERUNIT_ICO': None, 'OWNERUNIT_STATE': 1, 'STAFF_ID': 2845, 'STAFF_NAME': '赵紫薇', 'OPERATE_DATE': '2020-10-30T14:24:55', 'OWNERUNIT_DESC': None, 'ISSUPPORTPOINT': None, 'DOWNLOAD_DATE': None, 'WECHATPUBLICSIGN_ID': None, 'ShopList': [{'label': '萧山服务区东区杭州味道', 'value': 1504.0, 'key': '330000-1504', 'type': 330000, 'ico': None, 'index': None}], 'OrganizationList': [{'AUTOTYPE_ID': 208, 'RTWECHATPUSH_ID': None, 'MEMBERSHIP_ID': None, 'AUTOTYPE_NAME': '萧山杭州味道东区', 'AUTOTYPE_PID': -1, 'AUTOTYPE_INDEX': 10, 'AUTOTYPE_STAFF': '赵紫薇', 'AUTOTYPE_CODE': '10', 'AUTOTYPE_DATE': '2020-10-29T11:57:19', 'AUTOTYPE_VALID': 1, 'AUTOTYPE_TYPEID': 1000, 'AUTOTYPE_TYPENAME': '业主组织架构', 'PROVINCE_CODE': 330000, 'OWNERUNIT_ID': 123, 'OWNERUNIT_NAME': '殷雪艳', 'ADDTIME': '2020-10-29T11:57:19', 'STAFF_ID': 2845, 'STAFF_NAME': '赵紫薇', 'OPERATE_DATE': '2020-10-30T14:25:36', 'AUTOTYPE_DESC': '', 'ServerpartList': [{'OWNERSERVERPART_ID': 830, 'AUTOTYPE_ID': 208, 'AUTOTYPE_NAME': '萧山杭州味道东区', 'PROVINCE_CODE': 330000, 'OWNERUNIT_ID': 123, 'OWNERUNIT_NAME': '殷雪艳', 'SERVERPART_HOSTID': 2, 'PROVINCE_BUSINESSCODE': 330000, 'SERVERPART_ID': 104, 'SERVERPART_CODE': '331010', 'SERVERPART_NAME': '萧山服务区', 'STAFF_ID': 2845, 'STAFF_NAME': '赵紫薇', 'OPERATE_DATE': '2020-10-29T11:59:22', 'OWNERSERVERPART_DESC': '', 'AUTOTYPE_IDS': None, 'ShopList': [{'OWNERSERVERPARTSHOP_ID': 3017, 'AUTOTYPE_ID': 208, 'AUTOTYPE_IDS': None, 'AUTOTYPE_NAME': '萧山杭州味道东区', 'PROVINCE_CODE': 330000, 'PROVINCE_CODES': None, 'OWNERUNIT_ID': 123, 'OWNERUNIT_IDS': None, 'OWNERUNIT_NAME': '殷雪艳', 'SERVERPART_HOSTID': 2, 'PROVINCE_BUSINESSCODE': 330000, 'SERVERPART_ID': 104, 'SERVERPART_IDS': None, 'SERVERPART_CODE': '331010', 'SERVERPART_NAME': '萧山服务区', 'SERVERPARTSHOP_ID': 1504, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '111004', 'SHOPNAME': '东区杭州味道', 'STAFF_ID': 2845, 'STAFF_NAME': '赵紫薇', 'OPERATE_DATE': '2020-10-29T12:01:08', 'OWNERSERVERPARTSHOP_DESC': ''}]}]}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `416.8 ms`
新 API 状态: `200`，耗时 `4.63 ms`

### Merchants/GetBusinessManDetailDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessManDetailId": 19}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetBusinessManDetailDetail | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetBusinessManDetailDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'OWNERUNITDETAIL_ID': 19, 'OWNERUNIT_ID': 403, 'OWNERUNIT_TYPE': None, 'OWNERUNIT_NATURE': 2000, 'OWNERUNIT_NAME': '优倍滋奶茶', 'TAXPAYER_IDENTIFYCODE': '1146339987000', 'OWNERUNIT_DRAWER': None, 'BANK_NAME': '广发银行', 'BANK_ACCOUNT': '133665201143300', 'OWNERUNIT_LINKMAN': '刘丽莎', 'OWNERUNIT_LINKMANIDCARD': '140333199312032729', 'OWNERUNIT_TELEPHONE': None, 'OWNERUNIT_MOBILEPHONE': '18335105481', 'OWNERUNIT_ADDRESS': None, 'STAFF_ID': 1290, 'STAFF_NAME': '刘丽莎', 'OPERATE_DATE': '2022-05-11T15:32:08', 'OWNERUNITDETAIL_DESC': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `194.63 ms`
新 API 状态: `200`，耗时 `1430.63 ms`

### Merchants/GetBusinessManDetailList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetBusinessManDetailList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetBusinessManDetailList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 5, 'List': [{'OWNERUNITDETAIL_ID': 3, 'OWNERUNIT_ID': None, 'OWNERUNIT_TYPE': None, 'OWNERUNIT_NATURE': 1000, 'OWNERUNIT_NAME': '大幅度', 'TAXPAYER_IDENTIFYCODE': '23', 'OWNERUNIT_DRAWER': '', 'BANK_NAME': '', 'BANK_ACCOUNT': '', 'OWNERUNIT_LINKMAN': '', 'OWNERUNIT_LINKMANIDCARD': '', 'OWNERUNIT_TELEPHONE': '', 'OWNERUNIT_MOBILEPHONE': '', 'OWNERUNIT_ADDRESS': '', 'STAFF_ID': None, 'STAFF_NAME': '', 'OPERATE_DATE': None, 'OWNERUNITDETAIL_DESC': ''}, {'OWNERUNITDETAIL_ID': 19, 'OWNERUNIT_ID': 403, 'OWNERUNIT_TYPE': None, 'OWNERUNIT_NATURE': 2000, 'OWNERUNIT_NAME': '优倍滋奶茶', 'TAXPAYER_IDENTIFYCODE': '1146339987000', 'OWNERUNIT_DRAWER': '', 'BANK_NAME': '广发银行', 'BANK_ACCOUNT': '133665201143300', 'OWNERUNIT_LINKMAN': '刘丽莎', 'OWNERUNIT_LINKMANIDCARD': '140333199312032729', 'OWNERUNIT_TELEPHONE': '', 'OWNERUNIT_MOBILEPHONE': '18335105481', 'OWNERUNIT_ADDRESS': '', 'STAFF_ID': 1290, 'STAFF_NAME': '刘丽莎', 'OPERATE_DATE': '2022-05-11T15:32:08', 'OWNERUNITDETAIL_DESC': ''}, {'OWNERUNITDETAIL_ID': 17, 'OWNERUNIT_ID': 401, 'OWNERUNIT_TYPE': None, 'OWNERUNIT_NATURE': 2000, 'OWNERUNIT_NAME': '优倍思餐饮连锁有限公司', 'TAXPAYER_IDENTIFYCODE': '14665087899552', 'OWNERUNIT_DRAWER': '', 'BANK_NAME': '招商银行', 'BANK_ACCOUNT': '1133665411103209', 'OWNERUNIT_LINKMAN': '刘丽莎', 'OWNERUNIT_LINKMANIDCARD': '140311199212122729', 'OWNERUNIT_TELEPHONE': '', 'OWNERUNIT_MOBILEPHONE': '18335105481', 'OWNERUNIT_ADDRESS': '', 'STAFF_ID': 776, 'STAFF_NAME': '安徽驿达管理员', 'OPERATE_DATE': '2022-05-09T10:00:38', 'OWNERUNITDETAIL_DESC': ''}, {'OWNERUNITDETAIL_ID': 1, 'OWNERUNIT_ID': 13, 'OWNERUNIT_TYPE': None, 'OWNERUNIT_NATURE': 1000, 'OWNERUNIT_NAME': '浙江省商业集团有限公司', 'TAXPAYER_IDENTIFYCODE': '91330000142918765A', 'OWNERUNIT_DRAWER': '', 'BANK_NAME': '', 'BANK_ACCOUNT': '', 'OWNERUNIT_LINKMAN': '', 'OWNERUNIT_LINKMANIDCARD': '', 'OWNERUNIT_TELEPHONE': '', 'OWNERUNIT_MOBILEPHONE': '', 'OWNERUNIT_ADDRESS': '', 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'OPERATE_DATE': '2020-03-19T20:56:32', 'OWNERUNITDETAIL_DESC': ''}, {'OWNERUNITDETAIL_ID': 15, 'OWNERUNIT_ID': 399, 'OWNERUNIT_TYPE': None, 'OWNERUNIT_NATURE': 2000, 'OWNERUNIT_NAME': '杭州食品经营部安徽分部', 'TAXPAYER_IDENTIFYCODE': '9104234567890T', 'OWNERUNIT_DRAWER': '', 'BANK_NAME': '杭州银行', 'BANK_ACCOUNT': '310003456789', 'OWNERUNIT_LINKMAN': 'zzy', 'OWNERUNIT_LINKMANIDCARD': '330326199109301111', 'OWNERUNIT_TELEPHONE': '', 'OWNERUNIT_MOBILEPHONE': '15067121398', 'OWNERUNIT_ADDRESS': '', 'STAFF_ID': 776, 'STAFF_NAME': '安徽驿达管理员', 'OPERATE_DATE': '2022-04-27T14:58:51', 'OWNERUNITDETAIL_DESC': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `146.06 ms`
新 API 状态: `200`，耗时 `8.83 ms`

### Merchants/GetBusinessManList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"OWNERUNIT_ID": 49}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetBusinessManList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetBusinessManList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'OWNERUNIT_ID': 49, 'OWNERUNIT_PID': -1, 'PROVINCE_CODE': 630000, 'PROVINCE_BUSINESSCODE': 630000, 'OWNERUNIT_NAME': '青海智驿服务区经营管理有限公司', 'OWNERUNIT_EN': '青海智驿', 'OWNERUNIT_NATURE': 1000, 'OWNERUNIT_GUID': 'f4a55722-c975-4aeb-80b6-9ab0a5601d6d', 'OWNERUNIT_INDEX': 160, 'OWNERUNIT_ICO': '/UploadImageDir/PictureManage/10259/2020_04_09_10_58_58_0565.png', 'OWNERUNIT_STATE': 1, 'STAFF_ID': 1342, 'STAFF_NAME': '系统管理员', 'OPERATE_DATE': '2021-10-26T13:53:29', 'OWNERUNIT_DESC': '', 'ISSUPPORTPOINT': None, 'DOWNLOAD_DATE': None, 'WECHATPUBLICSIGN_ID': 18, 'ShopList': None, 'OrganizationList': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `180.29 ms`
新 API 状态: `200`，耗时 `32.0 ms`

### Merchants/GetCUSTOMTYPEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CUSTOMTYPEId": 49}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCUSTOMTYPEDetail | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCUSTOMTYPEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_one' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'CUSTOMTYPE_ID': 49, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江艳艳副食', 'CUSTOMTYPE_CODE': None, 'CUSTOMTYPE_INDEX': 24, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:38', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'")

原 API 状态: `200`，耗时 `181.65 ms`
新 API 状态: `200`，耗时 `5.76 ms`

### Merchants/GetCUSTOMTYPEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"CUSTOMTYPE_ID": 49}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCUSTOMTYPEList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCUSTOMTYPEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'CUSTOMTYPE_ID': 49, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江艳艳副食', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 24, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:38', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `195.27 ms`
新 API 状态: `200`，耗时 `450.23 ms`

### Merchants/GetCommodityDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"Commodity_BusinessId": 12}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCommodityDetail | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCommodityDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 请求参数校验失败 |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'COMMODITY_BUSINESS_ID': 12, 'COMMODITY_TYPE': None, 'COMMODITY_TYPENAME': None, 'COMMODITY_NAME': 'p4', 'COMMODITY_BARCODE': '6949810501151', 'COMMODITY_UNIT': '个', 'COMMODITY_RULE': '1', 'COMMODITY_ORI': None, 'COMMODITY_GRADE': '', 'COMMODITY_RETAILPRICE': 30.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 1.0, 'METERINGMETHOD': None, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 228, 'STAFF_ID': None, 'STAFF_NAME': None, 'OPERATE_DATE': '2015/06/30 16:37:42', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': None, 'UPPER_STATE': None, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': None, 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': None, 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `206.91 ms`
新 API 状态: `200`，耗时 `4.01 ms`

### Merchants/GetCommodityList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"COMMODITY_TYPE": "33"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCommodityList | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCommodityList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'DatabaseHelper' object has no attribute 'fetch_scalar' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 32, 'List': [{'COMMODITY_BUSINESS_ID': 70270, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '麦信易数据线苹果', 'COMMODITY_BARCODE': '6976171459920', 'COMMODITY_UNIT': '根', 'COMMODITY_RULE': '根', 'COMMODITY_ORI': '四川', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 20.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 9.8, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2026/02/10 16:36:57', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 0, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '3636', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 70269, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '麦信易数据线安卓', 'COMMODITY_BARCODE': '6976171459913', 'COMMODITY_UNIT': '根', 'COMMODITY_RULE': '根', 'COMMODITY_ORI': '四川', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 20.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 9.8, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2026/02/10 16:33:36', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 0, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '3635', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 70268, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '开江豆干麻辣', 'COMMODITY_BARCODE': '6977605550015', 'COMMODITY_UNIT': '包', 'COMMODITY_RULE': '23克', 'COMMODITY_ORI': '四川', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 2.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 0.95, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2026/02/10 16:28:36', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 0, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '3634', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 70267, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '开江豆干五香', 'COMMODITY_BARCODE': '6977605550022', 'COMMODITY_UNIT': '包', 'COMMODITY_RULE': '23克', 'COMMODITY_ORI': '四川', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 2.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 0.95, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2026/02/10 16:20:16', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 0, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '3633', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 58099, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '雀巢咖啡丝滑拿铁(268ml)', 'COMMODITY_BARCODE': '6917878030623', 'COMMODITY_UNIT': '瓶', 'COMMODITY_RULE': '268毫升', 'COMMODITY_ORI': '湖北孝感', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 10.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 6.0, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2025/10/30 14:28:47', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 1, 'SERVERPART_ID': None, 'SERVERPART_NAME': '开江服务区', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '241', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 58062, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '银鹭好粥道(黑米味)', 'COMMODITY_BARCODE': '6926892566087', 'COMMODITY_UNIT': '瓶', 'COMMODITY_RULE': '280ml', 'COMMODITY_ORI': '', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 7.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 1.0, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2025/08/06 14:59:25', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 1, 'SERVERPART_ID': None, 'SERVERPART_NAME': '开江服务区', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '232', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 58188, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '银鹭桂圆八宝粥(360g)', 'COMMODITY_BARCODE': '6926892527088', 'COMMODITY_UNIT': '罐', 'COMMODITY_RULE': '360g', 'COMMODITY_ORI': '成都', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 7.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 4.0, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2025/08/06 14:59:05', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 1, 'SERVERPART_ID': None, 'SERVERPART_NAME': '开江服务区', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '228', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 70205, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '康师傅劲爽拉面', 'COMMODITY_BARCODE': '6920208926862', 'COMMODITY_UNIT': '桶', 'COMMODITY_RULE': '82.5克', 'COMMODITY_ORI': '重庆', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 4.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 2.3, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2025/07/28 12:43:51', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 0, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '3437', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}, {'COMMODITY_BUSINESS_ID': 70174, 'COMMODITY_TYPE': '33', 'COMMODITY_TYPENAME': ' 开江县嘉翔食用油商行', 'COMMODITY_NAME': '愉南笋小森笋尖', 'COMMODITY_BARCODE': '6939883800329', 'COMMODITY_UNIT': '袋', 'COMMODITY_RULE': '100克', 'COMMODITY_ORI': '重庆', 'COMMODITY_GRADE': '1000', 'COMMODITY_RETAILPRICE': 6.0, 'COMMODITY_MEMBERPRICE': None, 'COMMODITY_PURCHASEPRICE': 2.5, 'METERINGMETHOD': 1, 'DUTY_PARAGRAPH': None, 'RETAIL_DUTY': None, 'BUSINESSMAN_ID': 374, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2025/02/15 09:58:24', 'COMMODITY_STATE': 1, 'COMMODITY_DESC': '', 'UPPER_STATE': 0, 'SERVERPART_ID': None, 'SERVERPART_NAME': '', 'SERVERPARTSHOP_IDS': None, 'SUPPLIER_ID': None, 'QUALIFICATION_ID': '3266', 'QUALIFICATION_ENDDATE': None, 'COMMODITY_QTYPE': '1', 'QUALIFICATION_ENDDATE_Start': None, 'QUALIFICATION_ENDDATE_End': None, 'QUALIFICATIONList': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'")

原 API 状态: `200`，耗时 `142.5 ms`
新 API 状态: `200`，耗时 `4.22 ms`

### Merchants/GetCustomTypeDDL / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessManId": 374}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetCustomTypeDDL | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetCustomTypeDDL |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 32, 'List': [{'node': {'label': '开江连洪食品经营部', 'value': 25, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '彭水县百业兴森林食品开发有限公司', 'value': 27, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '达州市绿野香食品有限公司', 'value': 28, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 达州市老磨坊食品有限公司', 'value': 29, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 达州市通川区杨锝商贸有限责任公司', 'value': 30, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 达州市吴家铺子食品有限公司', 'value': 31, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 重庆市江北问天食品经营部', 'value': 32, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江县嘉翔食用油商行', 'value': 33, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 重庆琼吉商贸有限公司', 'value': 34, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 成都成购商贸有限公司', 'value': 35, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江宜简超市', 'value': 36, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 重庆真本味食品有限公司', 'value': 37, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江县鸿远商行', 'value': 38, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '湖北萌玖食品有限公司', 'value': 39, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江县鑫诚百货', 'value': 40, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 眉山巴蜀人家商贸有限公司', 'value': 41, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 重庆和旭餐饮文化有限公司', 'value': 42, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 达州川妹子酒业有限公司', 'value': 43, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江酒立方酒类销售有限公司', 'value': 44, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江金马山便利店', 'value': 45, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 达州市通川区令春食品经营部', 'value': 46, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 彭水县百业兴森林食品开发有限公司', 'value': 47, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 成都哈哥食品有限公司', 'value': 48, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江艳艳副食', 'value': 49, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': ' 开江县普安国梅雪糕批发部', 'value': 50, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '达州烟草公司', 'value': 51, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '福乾（上海）商贸有限公司', 'value': 93, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '山东致堪商贸有限公司', 'value': 237, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '长沙市普源贸易有限公司', 'value': 261, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '长沙市普源商贸有限公司', 'value': 262, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '四川锦润峰贸易有限公司', 'value': 267, 'pid': -1, 'level': None}, 'children': []}, {'node': {'label': '达州市通川区胡记四合副食经营部', 'value': 269, 'pid': -1, 'level': None}, 'children': []}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `174.57 ms`
新 API 状态: `200`，耗时 `5.49 ms`

### Merchants/GetNestingCustomTypeLsit / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"BusinessManId": 374}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Merchants/GetNestingCustomTypeLsit | 新 API: http://localhost:8080/EShangApiMain/Merchants/GetNestingCustomTypeLsit |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 32, 'List': [{'node': {'CUSTOMTYPE_ID': 25, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '开江连洪食品经营部', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 1, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T19:05:56', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 27, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '彭水县百业兴森林食品开发有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 2, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:19:21', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 28, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '达州市绿野香食品有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 3, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:19:53', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 29, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 达州市老磨坊食品有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 4, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:20:13', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 30, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 达州市通川区杨锝商贸有限责任公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 5, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:20:26', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 31, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 达州市吴家铺子食品有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 6, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:20:42', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 32, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 重庆市江北问天食品经营部', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 7, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:20:55', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 33, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江县嘉翔食用油商行', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 8, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:21:09', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 34, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 重庆琼吉商贸有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 9, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:21:26', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 35, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 成都成购商贸有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 10, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:21:41', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 36, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江宜简超市', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 11, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:22:01', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 37, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 重庆真本味食品有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 12, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:22:34', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 38, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江县鸿远商行', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 13, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:22:47', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 39, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '湖北萌玖食品有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 14, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:23:06', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 40, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江县鑫诚百货', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 15, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:23:25', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 41, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 眉山巴蜀人家商贸有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 16, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:23:43', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 42, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 重庆和旭餐饮文化有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 17, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:23:57', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 43, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 达州川妹子酒业有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 18, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:24:09', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 44, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江酒立方酒类销售有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 19, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:24:26', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 45, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江金马山便利店', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 20, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:24:42', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 46, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 达州市通川区令春食品经营部', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 21, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:02', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 47, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 彭水县百业兴森林食品开发有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 22, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:13', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 48, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 成都哈哥食品有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 23, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:26', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 49, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江艳艳副食', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 24, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:38', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 50, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江县普安国梅雪糕批发部', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 25, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:25:49', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 51, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '达州烟草公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 26, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品分类', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': None, 'SERVERPART_ID': None, 'OWNERUNIT_ID': None, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-05-27T21:34:08', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 93, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '福乾（上海）商贸有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 27, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '商品类别', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': 2208, 'SERVERPART_ID': None, 'OWNERUNIT_ID': 245, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2022-07-31T16:19:33', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 237, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '山东致堪商贸有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 28, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品类别', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': 2208, 'SERVERPART_ID': None, 'OWNERUNIT_ID': 245, 'STAFF_ID': 2208, 'STAFF_NAME': '杜得芳', 'OPERATE_DATE': '2023-04-10T11:28:17', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 261, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '长沙市普源贸易有限公司', 'CUSTOMTYPE_CODE': '29', 'CUSTOMTYPE_INDEX': 29, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品类别', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': 2208, 'SERVERPART_ID': None, 'OWNERUNIT_ID': 245, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2023-09-18T19:08:10', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 262, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '长沙市普源商贸有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 29, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '商品类别', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': 2208, 'SERVERPART_ID': None, 'OWNERUNIT_ID': 245, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2023-09-18T19:10:22', 'CUSTOMTYPE_STATE': 0, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 267, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '四川锦润峰贸易有限公司', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 30, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品类别', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': 2208, 'SERVERPART_ID': None, 'OWNERUNIT_ID': 245, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2023-11-11T10:44:40', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}, {'node': {'CUSTOMTYPE_ID': 269, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': '达州市通川区胡记四合副食经营部', 'CUSTOMTYPE_CODE': '', 'CUSTOMTYPE_INDEX': 31, 'CUSTOMTYPE_TYPE': 1000, 'CUSTOMTYPE_TYPENAME': '云库商品类别', 'BUSINESSMAN_ID': 374, 'BELONGUSER_ID': 2208, 'SERVERPART_ID': None, 'OWNERUNIT_ID': 245, 'STAFF_ID': 2208, 'STAFF_NAME': '开江服务区', 'OPERATE_DATE': '2023-11-02T13:44:59', 'CUSTOMTYPE_STATE': 1, 'CUSTOMTYPE_DESC': ''}, 'children': []}]} vs []
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `136.69 ms`
新 API 状态: `200`，耗时 `362.55 ms`

### Supplier/GetQUALIFICATION_HISDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetQUALIFICATION_HISDetail | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetQUALIFICATION_HISDetail |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Supplier/GetQUALIFICATION_HISDetail”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `5.53 ms`
新 API 状态: `200`，耗时 `3.59 ms`

### Supplier/GetQUALIFICATION_HISList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetQUALIFICATION_HISList | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetQUALIFICATION_HISList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 查询失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `8.03 ms`
新 API 状态: `200`，耗时 `3.69 ms`

### Supplier/GetQualificationDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetQualificationDetail | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetQualificationDetail |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Supplier/GetQualificationDetail”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `4.2 ms`
新 API 状态: `200`，耗时 `3.69 ms`

### Supplier/GetQualificationList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetQualificationList | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetQualificationList |
| HTTP 状态码 | ❌ | 500 vs 200 |
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
- Message: 值不一致 ('出现错误。' vs '请求参数校验失败')

原 API 状态: `500`，耗时 `7.18 ms`
新 API 状态: `200`，耗时 `39.9 ms`

### Supplier/GetSupplierDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetSupplierDetail | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetSupplierDetail |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Supplier/GetSupplierDetail”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `6.09 ms`
新 API 状态: `200`，耗时 `4.26 ms`

### Supplier/GetSupplierList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetSupplierList | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetSupplierList |
| HTTP 状态码 | ❌ | 500 vs 200 |
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
- Message: 值不一致 ('出现错误。' vs '请求参数校验失败')

原 API 状态: `500`，耗时 `6.18 ms`
新 API 状态: `200`，耗时 `3.1 ms`

### Supplier/GetSupplierTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Supplier/GetSupplierTreeList | 新 API: http://localhost:8080/EShangApiMain/Supplier/GetSupplierTreeList |
| HTTP 状态码 | ❌ | 500 vs 200 |
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
- Message: 值不一致 ('出现错误。' vs '请求参数校验失败')

原 API 状态: `500`，耗时 `7.87 ms`
新 API 状态: `200`，耗时 `3.55 ms`

### Verification/GetCommoditySaleList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetCommoditySaleList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetCommoditySaleList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs list |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `8.27 ms`
新 API 状态: `200`，耗时 `3.81 ms`

### Verification/GetDataVerificationList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetDataVerificationList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetDataVerificationList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs list |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `4.6 ms`
新 API 状态: `200`，耗时 `4.39 ms`

### Verification/GetENDACCOUNTModel / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetENDACCOUNTModel | 新 API: http://localhost:8080/EShangApiMain/Verification/GetENDACCOUNTModel |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs dict |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `4.68 ms`
新 API 状态: `200`，耗时 `9.79 ms`

### Verification/GetEndAccountData / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetEndAccountData | 新 API: http://localhost:8080/EShangApiMain/Verification/GetEndAccountData |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `8.4 ms`
新 API 状态: `200`，耗时 `9.29 ms`

### Verification/GetEndaccountDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetEndaccountDetail | 新 API: http://localhost:8080/EShangApiMain/Verification/GetEndaccountDetail |
| HTTP 状态码 | ❌ | 404 vs 405 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['detail'] |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.detail: 新 API 多出该字段

原 API 状态: `404`，耗时 `17.84 ms`
新 API 状态: `405`，耗时 `6.77 ms`

### Verification/GetEndaccountHisList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetEndaccountHisList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetEndaccountHisList |

差异明细：
- 原 API 调用失败: HTTPConnectionPool(host='192.168.1.99', port=8900): Read timed out. (read timeout=20)

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `405`，耗时 `2024.23 ms`

### Verification/GetEndaccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ❌ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetEndaccountList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetEndaccountList |

差异明细：
- 原 API 调用失败: HTTPConnectionPool(host='192.168.1.99', port=8900): Read timed out. (read timeout=20)

原 API 状态: `None`，耗时 `None ms`
新 API 状态: `405`，耗时 `2046.95 ms`

### Verification/GetEndaccountSupplement / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetEndaccountSupplement | 新 API: http://localhost:8080/EShangApiMain/Verification/GetEndaccountSupplement |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `33.07 ms`
新 API 状态: `200`，耗时 `5.13 ms`

### Verification/GetMobilePayDataList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetMobilePayDataList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetMobilePayDataList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 100 |
| Result_Desc | ❌ | None vs 成功 |
| Result_Data 类型 | ❌ | NoneType vs list |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段

原 API 状态: `404`，耗时 `7.67 ms`
新 API 状态: `200`，耗时 `5.39 ms`

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
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'Serverpart_ID': 416, 'Serverpart_Name': '新桥服务区', 'ServerpartShop_Code': '049001', 'ServerpartShop_Name': '自营老乡鸡', 'ServerpartShop_ICO': None, 'ShopRegion_Name_A': None, 'ShopRegion_Name_B': '北区', 'Revenue_Amount': 15048.2, 'Revenue_Amount_A': 0.0, 'Revenue_Amount_B': 15048.2, 'Deal_Count': 2, 'Total_Count': 2, 'Treatment_MarkState': 0, 'VerifyList': [], 'VerifiedList': [{'label': '2025/12/01 21:16:27', 'value': 6198482.0, 'key': '北区自营老乡鸡', 'type': 1, 'ico': None, 'index': None}, {'label': '2025/12/01 21:15:43', 'value': 6198440.0, 'key': '北区自营老乡鸡', 'type': 1, 'ico': None, 'index': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `437.3 ms`
新 API 状态: `200`，耗时 `6.67 ms`

### Verification/GetSuppEndaccountList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Verification/GetSuppEndaccountList | 新 API: http://localhost:8080/EShangApiMain/Verification/GetSuppEndaccountList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ❌ | 查询成功 vs 成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ❌ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'StaticsModel', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ❌ | 1 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- Result_Data.StaticsModel: 新 API 多出该字段
- Result_Data.List: 列表长度不一致 (1 vs 0)
- Result_Data.TotalCount: 值不一致 (1 vs 0)
- Result_Desc: 值不一致 ('查询成功' vs '成功')

原 API 状态: `200`，耗时 `133.33 ms`
新 API 状态: `200`，耗时 `4.55 ms`

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
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 999 |
| Result_Desc | ❌ | None vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Sales/GetCOMMODITYSALEDetail”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `4.41 ms`
新 API 状态: `200`，耗时 `3.24 ms`

### Sales/GetCOMMODITYSALEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetCOMMODITYSALEList | 新 API: http://localhost:8080/EShangApiMain/Sales/GetCOMMODITYSALEList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 查询失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `4.9 ms`
新 API 状态: `200`，耗时 `4.05 ms`

### Sales/GetCommoditySaleSummary / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetCommoditySaleSummary | 新 API: http://localhost:8080/EShangApiMain/Sales/GetCommoditySaleSummary |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Sales/GetCommoditySaleSummary”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `5.5 ms`
新 API 状态: `200`，耗时 `4.59 ms`

### Sales/GetCommodityTypeHistory / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetCommodityTypeHistory | 新 API: http://localhost:8080/EShangApiMain/Sales/GetCommodityTypeHistory |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Sales/GetCommodityTypeHistory”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `4.35 ms`
新 API 状态: `200`，耗时 `4.26 ms`

### Sales/GetCommodityTypeSummary / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetCommodityTypeSummary | 新 API: http://localhost:8080/EShangApiMain/Sales/GetCommodityTypeSummary |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Sales/GetCommodityTypeSummary”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `4.66 ms`
新 API 状态: `200`，耗时 `4.38 ms`

### Sales/GetEndaccountError / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetEndaccountError | 新 API: http://localhost:8080/EShangApiMain/Sales/GetEndaccountError |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 处理失败未将对象引用设置到对象的实例。 vs 请求参数校验失败 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 多出该字段
- Result_Desc: 值不一致 ('处理失败未将对象引用设置到对象的实例。' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `5.71 ms`
新 API 状态: `200`，耗时 `4.0 ms`

### Sales/GetEndaccountSaleInfo / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Sales/GetEndaccountSaleInfo | 新 API: http://localhost:8080/EShangApiMain/Sales/GetEndaccountSaleInfo |
| HTTP 状态码 | ❌ | 404 vs 405 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['detail'] |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.detail: 新 API 多出该字段

原 API 状态: `404`，耗时 `4.65 ms`
新 API 状态: `405`，耗时 `2.6 ms`
