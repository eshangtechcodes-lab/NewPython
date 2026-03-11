# 动态接口对比报告

- 生成时间: 2026-03-10 23:57:39
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_audit.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 0 / FAIL 17 / SKIP 0 / TOTAL 17`

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

原 API 状态: `200`，耗时 `301.54 ms`
新 API 状态: `200`，耗时 `2077.19 ms`

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

原 API 状态: `200`，耗时 `78.5 ms`
新 API 状态: `200`，耗时 `2044.32 ms`

### Audit/GetAUDITTASKSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"AUDITTASKS_ID": 3675}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAUDITTASKSList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAUDITTASKSList |
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
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'AUDITTASKS_ID': 3675, 'SERVERPART_ID': 477, 'SERVERPARTCODE': '340606', 'SERVERPART_NAME': '呈坎服务区', 'SERVERPARTSHOP_ID': None, 'SHOPCODE': '', 'SHOPNAME': '', 'BUSINESSTYPE': '3000', 'BUSINESSTYPE_NAME': '自营餐饮', 'AUDITTASKS_STARTDATE': '2023-04-07T00:00:00', 'AUDITTASKS_ENDDATE': None, 'AUDITTASKS_DURATION': None, 'AUDITTASKS_COUNT': None, 'AUDITTASKS_INTERVAL': None, 'AUDITTASKS_TYPE': None, 'AUDITTASKS_FIRSTTIME': None, 'AUDITTASKS_SECONDTIME': None, 'AUDITTASKS_THIRDTIME': None, 'AUDITTASKS_ISVALID': 1, 'OPERATE_DATE': '2023-04-07T10:53:17', 'STAFF_ID': 811, 'STAFF_NAME': '张坤', 'AUDITTASKS_DESC': '公司远程稽核'}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `174.5 ms`
新 API 状态: `200`，耗时 `2059.42 ms`

### Audit/GetAbnormalAuditDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AbnormalAuditId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAbnormalAuditDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAbnormalAuditDetail |
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
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ABNORMALAUDIT_ID': 1, 'ENDACCOUNT_ID': None, 'PROVINCE_CODE': 3544, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 586, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '348888', 'SERVERPART_NAME': '安徽测试服务区', 'SERVERPARTSHOP_ID': 3408, 'SERVERPARTSHOP_IDS': None, 'SHOPCODE': '012001', 'SHOPNAME': 'A区测试便利店', 'MACHINECODE': '9999', 'ENDACCOUNT_DATE': 20211207195211, 'CHECK_ENDDATE': 20211207195008, 'CHECK_STARTDATE': 20211207194941, 'TIME_INTERVAL': 2.05, 'ABNORMALAUDIT_TYPE': 2.0, 'ERASE_TYPE': None, 'TOTALSELLAMOUNT': 22.5, 'CASH_PAYMENT': 22.5, 'CHECK_CASHPAY': 50.0, 'DIFFERENT_PRICE': 27.5, 'REPLENISH_AMOUNT': 27.5, 'ENDACCOUNT_REVENUE': 50.0, 'CHECK_TYPE': '现场稽查', 'PRINTBILL_STATE': None, 'PUSH_STATE': None, 'WORKER_NAME': '系统管理员', 'CASHIER_NAME': '收银员A', 'DOWNLOAD_DATE': '2021-12-07T19:58:20', 'ABNORMALAUDIT_VALID': 1, 'ABNORMALAUDIT_DESC': None, 'CHECK_STARTDATE_SEARCH': '2021/12/07 19:49:41', 'CHECK_ENDDATE_SEARCH': '2021/12/07 19:50:08'} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `150.42 ms`
新 API 状态: `200`，耗时 `2087.23 ms`

### Audit/GetAbnormalRateReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416", "endDate": "2025-12-02", "startDate": "2025-12-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAbnormalRateReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAbnormalRateReport |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'Id': None, 'Name': '合计', 'SpregiontypeName': None, 'ServerpartId': None, 'ServerpartName': None, 'ShopId': None, 'ShopName': None, 'TOTALCOUNT': 0.0, 'TICKETCOUNT': 0.0, 'EXCEPTIONCOUNT_1011': 0.0, 'EXCEPTIONCOUNT_1011Rate': None, 'EXCEPTIONCOUNT_1050': 0.0, 'EXCEPTIONCOUNT_1050Rate': None, 'EXCEPTIONCOUNT_1099': 0.0, 'EXCEPTIONCOUNT_1099Rate': None, 'EXCEPTIONCOUNT_1060': 0.0, 'EXCEPTIONCOUNT_1060Rate': None, 'EXCEPTIONCOUNT_2010': 0.0, 'EXCEPTIONCOUNT_2010Rate': None, 'EXCEPTIONCOUNT_3030': 0.0, 'EXCEPTIONCOUNT_3030Rate': None, 'EXCEPTIONCOUNT_3050': 0.0, 'EXCEPTIONCOUNT_3050Rate': None, 'EXCEPTIONCOUNT_3010': 0.0, 'EXCEPTIONCOUNT_3010Rate': None, 'EXCEPTIONCOUNT_3020': 0.0, 'EXCEPTIONCOUNT_3020Rate': None, 'EXCEPTIONCOUNT_3990': 0.0, 'EXCEPTIONCOUNT_3990Rate': None}, 'children': []}]} vs []

原 API 状态: `200`，耗时 `252.56 ms`
新 API 状态: `200`，耗时 `2044.55 ms`

### Audit/GetAuditDetils / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditDetils | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditDetils |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditDetils”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `3.86 ms`
新 API 状态: `200`，耗时 `3.05 ms`

### Audit/GetAuditList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditList |
| HTTP 状态码 | ❌ | 404 vs 405 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['detail'] |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- <root>.Message: 新 API 缺少该字段
- <root>.detail: 新 API 多出该字段

原 API 状态: `404`，耗时 `3.47 ms`
新 API 状态: `405`，耗时 `2.69 ms`

### Audit/GetAuditTasksDetailList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditTasksDetailList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditTasksDetailList |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditTasksDetailList”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `3.26 ms`
新 API 状态: `200`，耗时 `3.18 ms`

### Audit/GetAuditTasksReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditTasksReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetAuditTasksReport |
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
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Audit/GetAuditTasksReport”匹配的 HTTP 资源。' vs '请求参数校验失败')

原 API 状态: `404`，耗时 `3.18 ms`
新 API 状态: `200`，耗时 `3.64 ms`

### Audit/GetCHECKACCOUNTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CHECKACCOUNTId": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetCHECKACCOUNTDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetCHECKACCOUNTDetail |
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
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'CHECKACCOUNT_ID': None, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': None, 'SERVERPART_IDS': None, 'SERVERPARTCODE': None, 'SERVERPART_NAME': None, 'PROVINCE_CODE': None, 'SERVERPARTSHOP_ID': None, 'SHOPCODE': None, 'SHOPNAME': None, 'MACHINECODE': None, 'CHECK_ENDDATE': None, 'CHECK_STARTDATE': None, 'CHECK_TYPE': None, 'CHECKPERSON_CODE': None, 'WORKER_NAME': None, 'CASHIER_NAME': None, 'TICKETCOUNT': None, 'TOTALCOUNT': None, 'TOTALSELLAMOUNT': None, 'TOTALOFFAMOUNT': None, 'CASH': None, 'CREDITCARD': None, 'TICKETBILL': None, 'VIPPERSON': None, 'COSTBILL': None, 'OTHERPAY': None, 'CASHPAY': None, 'DIFFERENT_PRICE': None, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': None, 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': None, 'CHECK_STATE': None, 'DOWNLOAD_DATE': None, 'VALID': None, 'CHECKACCOUNT_DESC': None, 'CHECKACCOUNT_CODE': None, 'ERROR_RATE': None, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `115.28 ms`
新 API 状态: `200`，耗时 `38.18 ms`

### Audit/GetCHECKACCOUNTList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetCHECKACCOUNTList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetCHECKACCOUNTList |
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
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 9420, 'List': [{'CHECKACCOUNT_ID': 6461557, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 1218, 'SHOPCODE': '027001', 'SHOPNAME': '南区客房', 'MACHINECODE': '4521', 'CHECK_ENDDATE': '2026/2/10 20:04:42', 'CHECK_STARTDATE': '2026/2/10 8:57:47', 'CHECK_TYPE': '智能稽查', 'CHECKPERSON_CODE': 'ZN9999', 'WORKER_NAME': '客房收银员', 'CASHIER_NAME': '客房收银员', 'TICKETCOUNT': 0.0, 'TOTALCOUNT': 0.0, 'TOTALSELLAMOUNT': 0.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 0.0, 'CREDITCARD': 0.0, 'TICKETBILL': 0.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 0.0, 'CASHPAY': 0.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T20:11:23', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003027001452120260210200442371008', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460668, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 5627, 'SHOPCODE': '144601', 'SHOPNAME': '北区361度', 'MACHINECODE': '6583', 'CHECK_ENDDATE': '2026/2/10 15:49:05', 'CHECK_STARTDATE': '2026/2/10 9:37:03', 'CHECK_TYPE': '现场稽查', 'CHECKPERSON_CODE': '6666', 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '361北区', 'TICKETCOUNT': 3.0, 'TOTALCOUNT': 3.0, 'TOTALSELLAMOUNT': 364.0, 'TOTALOFFAMOUNT': 9.0, 'CASH': 0.0, 'CREDITCARD': 0.0, 'TICKETBILL': 284.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 80.0, 'CASHPAY': 0.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T16:08:17', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003144601658320260210154905661008', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460569, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 2306, 'SHOPCODE': '127001', 'SHOPNAME': '南区丁记米饺', 'MACHINECODE': '6381', 'CHECK_ENDDATE': '2026/2/10 15:45:36', 'CHECK_STARTDATE': '2026/2/10 5:43:48', 'CHECK_TYPE': '现场稽查', 'CHECKPERSON_CODE': '6666', 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '丁记米饺南', 'TICKETCOUNT': 72.0, 'TOTALCOUNT': 140.0, 'TOTALSELLAMOUNT': 984.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 78.0, 'CREDITCARD': 0.0, 'TICKETBILL': 786.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 120.0, 'CASHPAY': 78.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T15:50:14', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003127001638120260210154536409004', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460686, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 2382, 'SHOPCODE': '126001', 'SHOPNAME': '南区丁家馄饨', 'MACHINECODE': '6408', 'CHECK_ENDDATE': '2026/2/10 15:43:06', 'CHECK_STARTDATE': '2026/2/10 4:45:54', 'CHECK_TYPE': '现场稽查', 'CHECKPERSON_CODE': '6666', 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '丁家馄饨南', 'TICKETCOUNT': 80.0, 'TOTALCOUNT': 116.0, 'TOTALSELLAMOUNT': 2232.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 198.0, 'CREDITCARD': 0.0, 'TICKETBILL': 1701.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 333.0, 'CASHPAY': 198.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T16:12:10', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003126001640820260210154306748004', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460632, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 2198, 'SHOPCODE': '129009', 'SHOPNAME': '南区同庆楼鲜肉大包', 'MACHINECODE': '6370', 'CHECK_ENDDATE': '2026/2/10 15:42:28', 'CHECK_STARTDATE': '2026/2/10 4:45:46', 'CHECK_TYPE': '现场稽查', 'CHECKPERSON_CODE': '6666', 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '同庆楼南', 'TICKETCOUNT': 59.0, 'TOTALCOUNT': 161.0, 'TOTALSELLAMOUNT': 984.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 95.0, 'CREDITCARD': 0.0, 'TICKETBILL': 841.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 48.0, 'CASHPAY': 95.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T16:03:12', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003129009637020260210154228211008', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460685, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 2468, 'SHOPCODE': '129007', 'SHOPNAME': '南区王仁和米线店', 'MACHINECODE': '4764', 'CHECK_ENDDATE': '2026/2/10 15:41:47', 'CHECK_STARTDATE': '2026/2/10 5:41:05', 'CHECK_TYPE': '现场稽查', 'CHECKPERSON_CODE': '6666', 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '王仁和南', 'TICKETCOUNT': 35.0, 'TOTALCOUNT': 51.0, 'TOTALSELLAMOUNT': 848.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 48.0, 'CREDITCARD': 0.0, 'TICKETBILL': 712.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 88.0, 'CASHPAY': 48.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T16:12:09', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003129007476420260210154147327001', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460581, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 2270, 'SHOPCODE': '125001', 'SHOPNAME': '南区下塘烧饼', 'MACHINECODE': '6375', 'CHECK_ENDDATE': '2026/2/10 15:41:14', 'CHECK_STARTDATE': '2026/2/10 5:53:29', 'CHECK_TYPE': '现场稽查', 'CHECKPERSON_CODE': '6666', 'WORKER_NAME': '杨杰', 'CASHIER_NAME': '下塘烧饼南', 'TICKETCOUNT': 36.0, 'TOTALCOUNT': 58.0, 'TOTALSELLAMOUNT': 626.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 20.0, 'CREDITCARD': 0.0, 'TICKETBILL': 549.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 57.0, 'CASHPAY': 20.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T15:54:15', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '3410031250016375202602101541147560010', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460428, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 2198, 'SHOPCODE': '129009', 'SHOPNAME': '南区同庆楼鲜肉大包', 'MACHINECODE': '6370', 'CHECK_ENDDATE': '2026/2/10 15:22:52', 'CHECK_STARTDATE': '2026/2/10 4:45:46', 'CHECK_TYPE': '智能稽查', 'CHECKPERSON_CODE': 'ZN9999', 'WORKER_NAME': '同庆楼南', 'CASHIER_NAME': '同庆楼南', 'TICKETCOUNT': 58.0, 'TOTALCOUNT': 156.0, 'TOTALSELLAMOUNT': 954.0, 'TOTALOFFAMOUNT': 0.0, 'CASH': 65.0, 'CREDITCARD': 0.0, 'TICKETBILL': 841.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 48.0, 'CASHPAY': 65.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T15:24:08', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '341003129009637020260210152252077006', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}, {'CHECKACCOUNT_ID': 6460392, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPARTCODE': '341003', 'SERVERPART_NAME': '新桥服务区', 'PROVINCE_CODE': 3544, 'SERVERPARTSHOP_ID': 5626, 'SHOPCODE': '122601', 'SHOPNAME': '南区361度', 'MACHINECODE': '6582', 'CHECK_ENDDATE': '2026/2/10 15:16:56', 'CHECK_STARTDATE': '2026/2/10 8:05:28', 'CHECK_TYPE': '智能稽查', 'CHECKPERSON_CODE': 'ZN9999', 'WORKER_NAME': '361北区', 'CASHIER_NAME': '361北区', 'TICKETCOUNT': 7.0, 'TOTALCOUNT': 7.0, 'TOTALSELLAMOUNT': 1616.0, 'TOTALOFFAMOUNT': 157.0, 'CASH': 458.0, 'CREDITCARD': 0.0, 'TICKETBILL': 679.0, 'VIPPERSON': 0.0, 'COSTBILL': 0.0, 'OTHERPAY': 479.0, 'CASHPAY': 458.0, 'DIFFERENT_PRICE': 0.0, 'CALIBRATOR_ID': None, 'CALIBRATOR_NAME': '', 'CALIBRATOR_DATE': None, 'REPLENISH_AMOUNT': 0.0, 'CHECK_STATE': None, 'DOWNLOAD_DATE': '2026-02-10T15:18:08', 'VALID': 1, 'CHECKACCOUNT_DESC': '', 'CHECKACCOUNT_CODE': '3410031226016582202602101516566950010', 'ERROR_RATE': 0.0, 'SERVERPARTSHOP_IDS': None, 'TREATMENT_MARKSTATE': None, 'HasImage': False}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `3237.93 ms`
新 API 状态: `200`，耗时 `2155.42 ms`

### Audit/GetCheckAccountReport / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartIds": "416", "checkType": 1, "endDate": "2025-01-02", "startDate": "2025-01-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetCheckAccountReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetCheckAccountReport |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ❌ | dict vs list |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'Id': None, 'Name': '合计', 'SpregiontypeName': None, 'ServerpartId': None, 'ServerpartName': None, 'TypePoint': 1.0, 'ExauditCount': 0.0, 'ExauditRate': 0.0, 'FeedbackCount': 0.0, 'FeedbackRate': None, 'TypeCount': 2.0, 'PricePercent': None, 'PriceMore': 0.0, 'PriceLess': 0.0, 'TypeDays': None, 'DaysCpercent': None, 'TotalSellAmount': 0.0}, 'children': [{'node': {'Id': '72', 'Name': '皖中管理中心', 'SpregiontypeName': None, 'ServerpartId': None, 'ServerpartName': None, 'TypePoint': 1.0, 'ExauditCount': 0.0, 'ExauditRate': 0.0, 'FeedbackCount': 0.0, 'FeedbackRate': None, 'TypeCount': 2.0, 'PricePercent': None, 'PriceMore': 0.0, 'PriceLess': 0.0, 'TypeDays': None, 'DaysCpercent': None, 'TotalSellAmount': 0.0}, 'children': [{'node': {'Id': '416', 'Name': '新桥服务区', 'SpregiontypeName': '皖中管理中心', 'ServerpartId': 416.0, 'ServerpartName': '新桥服务区', 'TypePoint': 1.0, 'ExauditCount': 0.0, 'ExauditRate': 0.0, 'FeedbackCount': 0.0, 'FeedbackRate': None, 'TypeCount': 2.0, 'PricePercent': 0.0, 'PriceMore': 0.0, 'PriceLess': 0.0, 'TypeDays': 2.0, 'DaysCpercent': 100.0, 'TotalSellAmount': None}, 'children': []}]}]}]} vs []

原 API 状态: `200`，耗时 `120.14 ms`
新 API 状态: `200`，耗时 `2117.5 ms`

### Audit/GetSpecialBehaviorReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"ServerpartIds": "416", "endDate": "2025-01-02", "startDate": "2025-01-01"}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetSpecialBehaviorReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetSpecialBehaviorReport |
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

原 API 状态: `404`，耗时 `18.83 ms`
新 API 状态: `200`，耗时 `4.57 ms`

### Audit/GetYSABNORMALITYDETAILList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"AbnormalityCode": 1}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYDETAILList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYSABNORMALITYDETAILList |
| HTTP 状态码 | ❌ | 404 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Message'] vs ['Message', 'Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | None vs 999 |
| Result_Desc | ❌ | None vs 服务器内部错误 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 4 处差异 |

差异明细：
- <root>.Result_Code: 新 API 多出该字段
- <root>.Result_Data: 新 API 多出该字段
- <root>.Result_Desc: 新 API 多出该字段
- Message: 值不一致 ('找不到与请求 URI“http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYDETAILList”匹配的 HTTP 资源。' vs '服务器内部错误')

原 API 状态: `404`，耗时 `4.69 ms`
新 API 状态: `200`，耗时 `42.55 ms`

### Audit/GetYSABNORMALITYDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"AbnormalityCode": 1}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYDetail | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYSABNORMALITYDetail |
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
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ABNORMALITY_CODE': None, 'SERVERPART_ID': None, 'SERVERPART_IDS': None, 'SERVERPART_NAME': None, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_IDS': None, 'SHOPNAME': None, 'MACHINECODE': None, 'SELLWORK_NAME': None, 'ABNORMALITY_TIME': None, 'ABNORMALITY_TYPE': None, 'ABNORMALITY_TYPES': None, 'EXCEPTION_TYPE': None, 'TICKET_CODE': None, 'COMMOTITY_COUNT': None, 'TOTALAMOUNT': None, 'SELLMASTER_CODE': None, 'ABNORMALITY_DESC': None, 'Start_Date': None, 'End_Date': None, 'ApprovalComments': None} vs None
- Result_Desc: 值不一致 ('查询成功' vs '请求参数校验失败')

原 API 状态: `200`，耗时 `193.15 ms`
新 API 状态: `200`，耗时 `2048.08 ms`

### Audit/GetYSABNORMALITYList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYSABNORMALITYList | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYSABNORMALITYList |
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
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 0, 'List': []} vs None
- Result_Desc: 值不一致 ('查询成功' vs '服务器内部错误')

原 API 状态: `200`，耗时 `126.9 ms`
新 API 状态: `200`，耗时 `37.91 ms`

### Audit/GetYsabnormalityReport / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"ServerpartIds": "416", "endDate": "2025-01-02", "startDate": "2025-01-01"}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Audit/GetYsabnormalityReport | 新 API: http://localhost:8080/EShangApiMain/Audit/GetYsabnormalityReport |
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

原 API 状态: `404`，耗时 `5.77 ms`
新 API 状态: `200`，耗时 `2071.52 ms`
