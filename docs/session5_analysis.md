# 动态接口对比报告

- 生成时间: 2026-03-11 10:43:26
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_analysis.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 12 / FAIL 19 / SKIP 0 / TOTAL 31`

## 用例明细

### Analysis/GetANALYSISINSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ANALYSISINSId": 1805}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISINSDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISINSDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ANALYSISINS_FORMAT', 'ANALYSISINS_FORMATS', 'ANALYSISINS_ID', 'ANALYSISINS_INDEX', 'ANALYSISINS_PID', 'ANALYSISINS_STATE', 'ANALYSISINS_TYPE', 'ANALYSISINS_TYPES', 'ANALYSIS_CONTENT', 'KEY_CONTENT', 'OPERATE_DATE', 'PELLUCIDITY', 'PROVINCE_CODE', 'SERVERPART_ID', 'SERVERPART_IDS', 'SPREGIONTYPE_ID', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE'] vs ['ANALYSISINS_FORMAT', 'ANALYSISINS_FORMATS', 'ANALYSISINS_ID', 'ANALYSISINS_INDEX', 'ANALYSISINS_PID', 'ANALYSISINS_STATE', 'ANALYSISINS_TYPE', 'ANALYSISINS_TYPES', 'ANALYSIS_CONTENT', 'KEY_CONTENT', 'OPERATE_DATE', 'PELLUCIDITY', 'PROVINCE_CODE', 'SERVERPART_ID', 'SERVERPART_IDS', 'SPREGIONTYPE_ID', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `144.91 ms`
新 API 状态: `200`，耗时 `2070.41 ms`

### Analysis/GetANALYSISINSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"ANALYSISINS_ID": "1805"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISINSList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISINSList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 7207 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ❌ | 1 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 19 个 |
| 完整响应体 | ❌ | 发现 11 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 9)
- Result_Data.List[0].ANALYSISINS_FORMAT: 类型不一致 (int vs NoneType)，值为 2000 vs None
- Result_Data.List[0].ANALYSISINS_ID: 值不一致 (1805 vs 7249)
- Result_Data.List[0].ANALYSISINS_STATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[0].ANALYSISINS_TYPE: 类型不一致 (int vs NoneType)，值为 1202 vs None
- Result_Data.List[0].ANALYSIS_CONTENT: 值不一致 ('统计口径:\n1、月均客单交易:月总客单数量/交易天数(取>0的天数)\n2、客单均价=本月总营业额/本月总客单数量\n消费水平从【服务区门店月度消费水平表取数】，数据按日均客单交易数量进行对比\n其中:高消费【X>90元】、普通消费【30元<X≤90元】、低消费【X≤30元】\n' vs '')
- Result_Data.List[0].OPERATE_DATE: 类型不一致 (str vs NoneType)，值为 '2023-04-07T17:25:45' vs None
- Result_Data.List[0].PROVINCE_CODE: 类型不一致 (int vs NoneType)，值为 340000 vs None
- Result_Data.List[0].SERVERPART_ID: 类型不一致 (int vs NoneType)，值为 460 vs None
- Result_Data.List[0].SPREGIONTYPE_ID: 类型不一致 (int vs NoneType)，值为 67 vs None
- Result_Data.TotalCount: 值不一致 (1 vs 7207)

原 API 状态: `200`，耗时 `79.47 ms`
新 API 状态: `200`，耗时 `24.81 ms`

### Analysis/GetANALYSISRULEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ANALYSISRULEId": 19}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISRULEDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISRULEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ANALYSISRULE_DESC', 'ANALYSISRULE_ID', 'ANALYSISRULE_IDS', 'ANALYSISRULE_STATE', 'API_ENDPOINT', 'CHILD_NODENAME', 'CREATE_DATE', 'CREATE_DATE_End', 'CREATE_DATE_Start', 'ENABLE_CHART', 'ENABLE_PDF_EXPORT', 'ENABLE_TABLE', 'ENABLE_VIEW_MORE', 'OUTPUT_FORMAT', 'OUTPUT_STANDARD', 'PARAM_FIELD', 'PARAM_TEMPLATE', 'PARSING_RULES', 'RESPONSE_CONFIG', 'RESPONSE_FIELD', 'RULE_PRIORITY', 'RULE_SOURCE', 'SHOW_CHILDNODE', 'SPRESPONSE_TYPE', 'TRIGGER_WORDS', 'UPDATE_DATE', 'UPDATE_DATE_End', 'UPDATE_DATE_Start', 'USER_INTENT'] vs ['ANALYSISRULE_DESC', 'ANALYSISRULE_ID', 'ANALYSISRULE_IDS', 'ANALYSISRULE_STATE', 'API_ENDPOINT', 'CHILD_NODENAME', 'CREATE_DATE', 'CREATE_DATE_End', 'CREATE_DATE_Start', 'ENABLE_CHART', 'ENABLE_PDF_EXPORT', 'ENABLE_TABLE', 'ENABLE_VIEW_MORE', 'OUTPUT_FORMAT', 'OUTPUT_STANDARD', 'PARAM_FIELD', 'PARAM_TEMPLATE', 'PARSING_RULES', 'RESPONSE_CONFIG', 'RESPONSE_FIELD', 'RULE_PRIORITY', 'RULE_SOURCE', 'SHOW_CHILDNODE', 'SPRESPONSE_TYPE', 'TRIGGER_WORDS', 'UPDATE_DATE', 'UPDATE_DATE_End', 'UPDATE_DATE_Start', 'USER_INTENT'] |
| 完整响应体 | ❌ | 发现 23 处差异 |

差异明细：
- Result_Data.ANALYSISRULE_DESC: 类型不一致 (str vs NoneType)，值为 '通过传递日期参数，查询服务区门店客单数量、同比客单、同比增长率' vs None
- Result_Data.ANALYSISRULE_ID: 类型不一致 (int vs NoneType)，值为 19 vs None
- Result_Data.ANALYSISRULE_STATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.API_ENDPOINT: 类型不一致 (str vs NoneType)，值为 'CommercialApi/Revenue/GetMonthINCAnalysis' vs None
- Result_Data.CHILD_NODENAME: 类型不一致 (str vs NoneType)，值为 '' vs None
- Result_Data.CREATE_DATE: 类型不一致 (str vs NoneType)，值为 '2024/11/22 0:00:00' vs None
- Result_Data.ENABLE_CHART: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.ENABLE_PDF_EXPORT: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.ENABLE_TABLE: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.ENABLE_VIEW_MORE: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.OUTPUT_FORMAT: 类型不一致 (str vs NoneType)，值为 '{"acceptVerbs":"get","responseType":"json","responseFormat":"nestingList","total":null,"region":null,"serverpart":null,"shop":null,"shopList":"ShopINCList","showLevel":3}' vs None
- Result_Data.OUTPUT_STANDARD: 类型不一致 (str vs NoneType)，值为 '' vs None
- Result_Data.PARAM_FIELD: 类型不一致 (str vs NoneType)，值为 '' vs None
- Result_Data.PARAM_TEMPLATE: 类型不一致 (str vs NoneType)，值为 '{"ServerpartId":"服务区内码","pushProvinceCode":"省份编码","StatisticsStartMonth":"开始月份，格式yyyyMM","StatisticsEndMonth":"结束月份，格式yyyyMM","calcYOY":"统计同比：0【不计】，1【计算】","calcQOQ":"统计环比：0【不计】，1【计算】","statisticsType":"统计方式：1【门店】，2【经营模式】，3【服务区类型】","sorterType":"固化数据：0【实时】，1【固化】"}' vs None
- Result_Data.PARSING_RULES: 类型不一致 (str vs NoneType)，值为 '{"ServerpartId":{"formatType":1,"fieldName":"ServerpartId","value":null},"StatisticsStartMonth":{"formatType":4,"fieldName":"StartDate","value":null},"StatisticsEndMonth":{"formatType":4,"fieldName":"EndDate","value":null},"pushProvinceCode":{"formatType":2,"fieldName":"ProvinceCode","value":null},"statisticsType":{"formatType":0,"fieldName":null,"value":1},"sorterType":{"formatType":0,"fieldName":null,"value":1},"calcYOY":{"formatType":0,"fieldName":null,"value":true},"calcQOQ":{"formatType":0,"fieldName":null,"value":true}}' vs None
- Result_Data.RESPONSE_CONFIG: 类型不一致 (str vs NoneType)，值为 '{"Name":{"label":"服务区名称","prop":"Name","width":150,"align":"left","isSlot":false,"isMoney":false,"isRate":false,"isTenThousand":false,"multipleNames":"SPRegionTypeName,ServerpartName,ServerpartShopName"},"TicketINCcurYearData":{"label":"客单数量(笔)","prop":"TicketINCcurYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"TicketINClYearData":{"label":"同比客单(笔)","prop":"TicketINClYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"TicketINCincreaseData":{"label":"增长(笔)","prop":"TicketINCincreaseData","width":100,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"TicketINCincreaseRate":{"label":"增幅(%)","prop":"TicketINCincreaseRate","width":100,"align":"right","isSlot":false,"isMoney":false,"isRate":true,"isTenThousand":false},"AvgTicketINCcurYearData":{"label":"客单均价(元)","prop":"AvgTicketINCcurYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"AvgTicketINClYearData":{"label":"同比客均(元)","prop":"AvgTicketINClYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"AvgTicketINCincreaseData":{"label":"增长(元)","prop":"AvgTicketINCincreaseData","width":100,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"AvgTicketINCincreaseRate":{"label":"增幅(%)","prop":"AvgTicketINCincreaseRate","width":100,"align":"right","isSlot":false,"isMoney":false,"isRate":true,"isTenThousand":false}}' vs None
- Result_Data.RESPONSE_FIELD: 类型不一致 (str vs NoneType)，值为 '{"ServerpartName":"服务区名称","ServerpartShopName":"门店名称","TicketINCcurYearData":"客单数量(笔)","TicketINClYearData":"同比客单(笔)","TicketINCincreaseData":"增长(笔)","TicketINCincreaseRate":"增幅(%)"}' vs None
- Result_Data.RULE_PRIORITY: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.RULE_SOURCE: 类型不一致 (int vs NoneType)，值为 2000 vs None
- Result_Data.SPRESPONSE_TYPE: 类型不一致 (int vs NoneType)，值为 2 vs None
- Result_Data.TRIGGER_WORDS: 类型不一致 (str vs NoneType)，值为 '客单均价|客单' vs None
- Result_Data.UPDATE_DATE: 类型不一致 (str vs NoneType)，值为 '2025/2/14 10:46:10' vs None
- Result_Data.USER_INTENT: 类型不一致 (str vs NoneType)，值为 '服务区门店客单交易数据' vs None

原 API 状态: `200`，耗时 `107.19 ms`
新 API 状态: `200`，耗时 `33.7 ms`

### Analysis/GetANALYSISRULEList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"ANALYSISRULE_ID": 19}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetANALYSISRULEList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetANALYSISRULEList |
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
| 完整响应体 | ❌ | 发现 20 处差异 |

差异明细：
- Result_Data.List[0].ANALYSISRULE_DESC: 值不一致 ('通过传递日期参数，查询服务区门店客单数量、同比客单、同比增长率' vs '')
- Result_Data.List[0].ANALYSISRULE_ID: 值不一致 (19 vs 54)
- Result_Data.List[0].ANALYSISRULE_STATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[0].API_ENDPOINT: 值不一致 ('CommercialApi/Revenue/GetMonthINCAnalysis' vs '')
- Result_Data.List[0].CREATE_DATE: 值不一致 ('2024/11/22 0:00:00' vs '2026/1/5 11:54:19')
- Result_Data.List[0].ENABLE_CHART: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[0].ENABLE_PDF_EXPORT: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[0].ENABLE_TABLE: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[0].ENABLE_VIEW_MORE: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[0].OUTPUT_FORMAT: 值不一致 ('{"acceptVerbs":"get","responseType":"json","responseFormat":"nestingList","total":null,"region":null,"serverpart":null,"shop":null,"shopList":"ShopINCList","showLevel":3}' vs '')
- Result_Data.List[0].PARAM_TEMPLATE: 值不一致 ('{"ServerpartId":"服务区内码","pushProvinceCode":"省份编码","StatisticsStartMonth":"开始月份，格式yyyyMM","StatisticsEndMonth":"结束月份，格式yyyyMM","calcYOY":"统计同比：0【不计】，1【计算】","calcQOQ":"统计环比：0【不计】，1【计算】","statisticsType":"统计方式：1【门店】，2【经营模式】，3【服务区类型】","sorterType":"固化数据：0【实时】，1【固化】"}' vs '')
- Result_Data.List[0].PARSING_RULES: 值不一致 ('{"ServerpartId":{"formatType":1,"fieldName":"ServerpartId","value":null},"StatisticsStartMonth":{"formatType":4,"fieldName":"StartDate","value":null},"StatisticsEndMonth":{"formatType":4,"fieldName":"EndDate","value":null},"pushProvinceCode":{"formatType":2,"fieldName":"ProvinceCode","value":null},"statisticsType":{"formatType":0,"fieldName":null,"value":1},"sorterType":{"formatType":0,"fieldName":null,"value":1},"calcYOY":{"formatType":0,"fieldName":null,"value":true},"calcQOQ":{"formatType":0,"fieldName":null,"value":true}}' vs '')
- Result_Data.List[0].RESPONSE_CONFIG: 值不一致 ('{"Name":{"label":"服务区名称","prop":"Name","width":150,"align":"left","isSlot":false,"isMoney":false,"isRate":false,"isTenThousand":false,"multipleNames":"SPRegionTypeName,ServerpartName,ServerpartShopName"},"TicketINCcurYearData":{"label":"客单数量(笔)","prop":"TicketINCcurYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"TicketINClYearData":{"label":"同比客单(笔)","prop":"TicketINClYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"TicketINCincreaseData":{"label":"增长(笔)","prop":"TicketINCincreaseData","width":100,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"TicketINCincreaseRate":{"label":"增幅(%)","prop":"TicketINCincreaseRate","width":100,"align":"right","isSlot":false,"isMoney":false,"isRate":true,"isTenThousand":false},"AvgTicketINCcurYearData":{"label":"客单均价(元)","prop":"AvgTicketINCcurYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"AvgTicketINClYearData":{"label":"同比客均(元)","prop":"AvgTicketINClYearData","width":120,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"AvgTicketINCincreaseData":{"label":"增长(元)","prop":"AvgTicketINCincreaseData","width":100,"align":"right","isSlot":false,"isMoney":true,"isRate":false,"isTenThousand":false},"AvgTicketINCincreaseRate":{"label":"增幅(%)","prop":"AvgTicketINCincreaseRate","width":100,"align":"right","isSlot":false,"isMoney":false,"isRate":true,"isTenThousand":false}}' vs '')
- Result_Data.List[0].RESPONSE_FIELD: 值不一致 ('{"ServerpartName":"服务区名称","ServerpartShopName":"门店名称","TicketINCcurYearData":"客单数量(笔)","TicketINClYearData":"同比客单(笔)","TicketINCincreaseData":"增长(笔)","TicketINCincreaseRate":"增幅(%)"}' vs '')
- Result_Data.List[0].RULE_PRIORITY: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[0].RULE_SOURCE: 类型不一致 (int vs NoneType)，值为 2000 vs None
- Result_Data.List[0].SPRESPONSE_TYPE: 类型不一致 (int vs NoneType)，值为 2 vs None
- Result_Data.List[0].TRIGGER_WORDS: 值不一致 ('客单均价|客单' vs '预警|问题|特情')
- Result_Data.List[0].UPDATE_DATE: 值不一致 ('2025/2/14 10:46:10' vs '2026/1/5 11:54:19')
- Result_Data.List[0].USER_INTENT: 值不一致 ('服务区门店客单交易数据' vs '')

原 API 状态: `200`，耗时 `91.61 ms`
新 API 状态: `200`，耗时 `35.35 ms`

### Analysis/GetASSETSPROFITSBusinessTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSBusinessTreeList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSBusinessTreeList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 0 vs 25 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 999 vs 999 |
| List 条数 | ❌ | 0 vs 25 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (0 vs 25)
- Result_Data.TotalCount: 值不一致 (0 vs 25)

原 API 状态: `200`，耗时 `4.78 ms`
新 API 状态: `200`，耗时 `5066.48 ms`

### Analysis/GetASSETSPROFITSDateDetailList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"endDate": "202512", "propertyAssetsId": 1, "serverPartId": 416, "shopId": 9475, "startDate": "202501"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSDateDetailList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSDateDetailList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | list vs list |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `111.2 ms`
新 API 状态: `200`，耗时 `86.1 ms`

### Analysis/GetASSETSPROFITSDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ASSETSPROFITSId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ASSETSPROFITS_CLOSEDAY', 'ASSETSPROFITS_DAY', 'ASSETSPROFITS_DESC', 'ASSETSPROFITS_ID', 'ASSETSPROFITS_STATE', 'AVG_PROFIT', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_TRADE', 'BUSINESS_TRADENAME', 'DETAIL_DATA', 'End_DATE', 'HOLIDAY_TYPE', 'HOLIDAY_TYPE_IDS', 'LOSS_AMOUNT', 'MONTHDAYS', 'OPRATE_DATE', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'PROPERTYASSETS_AREA', 'PROPERTYASSETS_CODE', 'PROPERTYASSETS_ID', 'PROPERTYASSETS_IDS', 'PROPERTYASSETS_REGION', 'PROPERTYASSETS_TYPE', 'REVENUE_AMOUNT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_CODE', 'SERVERPART_FLOW', 'SERVERPART_FLOWDAYS', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_IDS', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE', 'Start_DATE', 'TOTAL_AREA', 'WEEKDAY_AMOUNT', 'WEEKDAY_AVG', 'WEEKEND_AMOUNT', 'WEEKEND_AVG', 'WEEKEND_DAYS'] vs ['ASSETSPROFITS_CLOSEDAY', 'ASSETSPROFITS_DAY', 'ASSETSPROFITS_DESC', 'ASSETSPROFITS_ID', 'ASSETSPROFITS_STATE', 'AVG_PROFIT', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_TRADE', 'BUSINESS_TRADENAME', 'DETAIL_DATA', 'End_DATE', 'HOLIDAY_TYPE', 'HOLIDAY_TYPE_IDS', 'LOSS_AMOUNT', 'MONTHDAYS', 'OPRATE_DATE', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'PROPERTYASSETS_AREA', 'PROPERTYASSETS_CODE', 'PROPERTYASSETS_ID', 'PROPERTYASSETS_IDS', 'PROPERTYASSETS_REGION', 'PROPERTYASSETS_TYPE', 'REVENUE_AMOUNT', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_CODE', 'SERVERPART_FLOW', 'SERVERPART_FLOWDAYS', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SPREGIONTYPE_ID', 'SPREGIONTYPE_IDS', 'SPREGIONTYPE_NAME', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE', 'Start_DATE', 'TOTAL_AREA', 'WEEKDAY_AMOUNT', 'WEEKDAY_AVG', 'WEEKEND_AMOUNT', 'WEEKEND_AVG', 'WEEKEND_DAYS'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `69.31 ms`
新 API 状态: `200`，耗时 `28.69 ms`

### Analysis/GetASSETSPROFITSList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 537 vs 25909 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 47 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].ASSETSPROFITS_CLOSEDAY: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.List[0].ASSETSPROFITS_DAY: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.List[0].ASSETSPROFITS_DESC: 值不一致 ('春运' vs '元旦')
- Result_Data.List[0].ASSETSPROFITS_ID: 值不一致 (151727 vs 174031)
- Result_Data.List[0].BUSINESS_TRADE: 值不一致 ('' vs '223')
- Result_Data.List[0].DETAIL_DATA: 类型不一致 (NoneType vs str)，值为 None vs '[{"DATE":"2024-12-31","WEEK":2,"AMOUNT":71.5,"LOSS":0.0}]'
- Result_Data.List[0].HOLIDAY_TYPE: 值不一致 (2 vs 1)
- Result_Data.List[0].LOSS_AMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 0.0
- Result_Data.List[0].MONTHDAYS: 值不一致 (29 vs 1)
- Result_Data.List[0].OPRATE_DATE: 值不一致 ('2024-11-25T17:33:23' vs '2025-01-09T17:23:59')
- Result_Data.List[0].PROPERTYASSETS_AREA: 值不一致 (289.0 vs 1.0)
- Result_Data.List[0].PROPERTYASSETS_ID: 值不一致 (81 vs 0)
- Result_Data.List[0].REVENUE_AMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 71.5
- Result_Data.List[0].SERVERPARTSHOP_ID: 值不一致 ('3065' vs '1424')
- Result_Data.List[0].SERVERPART_CODE: 值不一致 ('341003' vs '340104')
- Result_Data.List[0].SERVERPART_FLOW: 值不一致 (239106 vs 0)
- Result_Data.List[0].SERVERPART_FLOWDAYS: 值不一致 (29 vs 0)
- Result_Data.List[0].SERVERPART_ID: 值不一致 (416 vs 364)
- Result_Data.List[0].SPREGIONTYPE_ID: 值不一致 (72 vs 47)
- Result_Data.List[0].SPREGIONTYPE_NAME: 值不一致 ('皖中管理中心' vs '皖南管理中心')
- Result_Data.List[0].STAFF_ID: 值不一致 (1 vs 776)
- Result_Data.List[0].STAFF_NAME: 值不一致 ('系统生成' vs '安徽驿达管理员')
- Result_Data.List[0].STATISTICS_DATE: 值不一致 (202402 vs 202412)
- Result_Data.List[0].WEEKDAY_AMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 0.0
- Result_Data.List[0].WEEKDAY_AVG: 类型不一致 (NoneType vs float)，值为 None vs 0.0

原 API 状态: `200`，耗时 `203.96 ms`
新 API 状态: `200`，耗时 `41.74 ms`

### Analysis/GetASSETSPROFITSTreeList / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 9, "SearchParameter": {"SERVERPART_IDS": "416"}}`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetASSETSPROFITSTreeList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetASSETSPROFITSTreeList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 0 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 0 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `3.99 ms`
新 API 状态: `200`，耗时 `6.17 ms`

### Analysis/GetAssetsLossProfitList / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"endDate": "202512", "propertyAssetsId": 1, "serverPartId": 416, "startDate": "202501"}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetAssetsLossProfitList | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetAssetsLossProfitList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['children', 'node'] vs ['children', 'node'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `95.5 ms`
新 API 状态: `200`，耗时 `40.73 ms`

### Analysis/GetINVESTMENTANALYSISDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"INVESTMENTANALYSISId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetINVESTMENTANALYSISDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetINVESTMENTANALYSISDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ADJUST_AMOUNT', 'ADJUST_RATIO', 'ADJUST_RENT', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_PTRADE', 'BUSINESS_TRADE', 'COMMISSION_AVGRATIO', 'COMMISSION_MAXRATIO', 'COMMISSION_MINRATIO', 'COMMISSION_RATIO', 'GUARANTEERATIO', 'GUARANTEE_AVGPRICE', 'GUARANTEE_MAXPRICE', 'GUARANTEE_MINPRICE', 'HOLIDAY_TYPE', 'INVESTMENTANALYSIS_DESC', 'INVESTMENTANALYSIS_ID', 'INVESTMENTANALYSIS_STATE', 'MINTURNOVER', 'PERIOD_DEGREE', 'PROFIT_AMOUNT', 'PROFIT_AVG', 'PROFIT_INFO', 'PROFIT_TOTALAMOUNT', 'RECORD_DATE', 'RENT_RATIO', 'REVENUE_AVGAMOUNT', 'REVENUE_LASTAMOUNT', 'ROYALTY_PRICE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SERVERPART_TYPE', 'SHOPROYALTY_ID', 'STAFF_ID', 'STAFF_NAME', 'TRADE_PROJECTCOUNT', 'TRADE_SHOPCOUNT'] vs ['ADJUST_AMOUNT', 'ADJUST_RATIO', 'ADJUST_RENT', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_NAME', 'BUSINESS_PTRADE', 'BUSINESS_TRADE', 'COMMISSION_AVGRATIO', 'COMMISSION_MAXRATIO', 'COMMISSION_MINRATIO', 'COMMISSION_RATIO', 'GUARANTEERATIO', 'GUARANTEE_AVGPRICE', 'GUARANTEE_MAXPRICE', 'GUARANTEE_MINPRICE', 'HOLIDAY_TYPE', 'INVESTMENTANALYSIS_DESC', 'INVESTMENTANALYSIS_ID', 'INVESTMENTANALYSIS_STATE', 'MINTURNOVER', 'PERIOD_DEGREE', 'PROFIT_AMOUNT', 'PROFIT_AVG', 'PROFIT_INFO', 'PROFIT_TOTALAMOUNT', 'RECORD_DATE', 'RENT_RATIO', 'REVENUE_AVGAMOUNT', 'REVENUE_LASTAMOUNT', 'ROYALTY_PRICE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_NAME', 'SERVERPART_TYPE', 'SHOPROYALTY_ID', 'STAFF_ID', 'STAFF_NAME', 'TRADE_PROJECTCOUNT', 'TRADE_SHOPCOUNT'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `90.69 ms`
新 API 状态: `200`，耗时 `15.04 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 632 vs 632 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 40 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].ADJUST_AMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 35.5
- Result_Data.List[0].ADJUST_RATIO: 类型不一致 (NoneType vs float)，值为 None vs 20.0
- Result_Data.List[0].ADJUST_RENT: 类型不一致 (NoneType vs float)，值为 None vs 65.5
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (1715 vs 191)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 值不一致 ('驿达公司皇甫山服务区安徽地方特色 项目' vs '八公山服务区（麦当劳）项目')
- Result_Data.List[0].BUSINESS_TRADE: 值不一致 (226 vs 227)
- Result_Data.List[0].COMMISSION_AVGRATIO: 值不一致 (23.53 vs 19.33)
- Result_Data.List[0].COMMISSION_MAXRATIO: 值不一致 (28.0 vs 35.0)
- Result_Data.List[0].COMMISSION_MINRATIO: 值不一致 (20.6 vs 8.0)
- Result_Data.List[0].COMMISSION_RATIO: 值不一致 ('23%-26%' vs '15%-20%')
- Result_Data.List[0].GUARANTEERATIO: 值不一致 (26.0 vs 13.0)
- Result_Data.List[0].GUARANTEE_AVGPRICE: 值不一致 (77.67 vs 29.79)
- Result_Data.List[0].GUARANTEE_MAXPRICE: 值不一致 (196.0 vs 50.0)
- Result_Data.List[0].GUARANTEE_MINPRICE: 值不一致 (18.28 vs 7.0)
- Result_Data.List[0].INVESTMENTANALYSIS_ID: 值不一致 (485 vs 651)
- Result_Data.List[0].MINTURNOVER: 值不一致 (30.6 vs 30.0)
- Result_Data.List[0].PERIOD_DEGREE: 类型不一致 (NoneType vs float)，值为 None vs 0.82
- Result_Data.List[0].PROFIT_AMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 19590.8
- Result_Data.List[0].PROFIT_AVG: 类型不一致 (NoneType vs float)，值为 None vs -38.44
- Result_Data.List[0].PROFIT_INFO: 值不一致 ('' vs '第1期：-66.90万元，第2期：174.13万元，第3期：274.10万元，第4期：260.21万元，第5期：187.85万元，第6期：1.95万元')
- Result_Data.List[0].PROFIT_TOTALAMOUNT: 值不一致 (-43045.06 vs 8313636.01)
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2025-06-09T18:44:32' vs '2026-01-04T21:07:53')
- Result_Data.List[0].RENT_RATIO: 类型不一致 (NoneType vs float)，值为 None vs 0.0
- Result_Data.List[0].REVENUE_AVGAMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 0.0
- Result_Data.List[0].REVENUE_LASTAMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 3275134.19

原 API 状态: `200`，耗时 `188.43 ms`
新 API 状态: `200`，耗时 `34.43 ms`

### Analysis/GetINVESTMENTDETAILDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"INVESTMENTDETAILId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetINVESTMENTDETAILDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetINVESTMENTDETAILDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BUSINESSPROJECT_ID', 'EVALUATE_SCORE', 'INVESTMENTANALYSIS_ID', 'INVESTMENTANALYSIS_IDS', 'INVESTMENTDETAIL_DESC', 'INVESTMENTDETAIL_ID', 'INVESTMENTDETAIL_STATE', 'MARKETREVENUE_AVGAMOUNT', 'PROFIT_AMOUNT', 'RECORD_DATE', 'REVENUE_AVGAMOUNT', 'REVENUE_TOLERANCE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_AVGRENT', 'SERVERPART_FLOW', 'SERVERPART_ID', 'SERVERPART_NAME', 'SERVERPART_REVENUE', 'STAFF_ID', 'STAFF_NAME', 'VEHICLE_TOLERANCE'] vs ['BUSINESSPROJECT_ID', 'EVALUATE_SCORE', 'INVESTMENTANALYSIS_ID', 'INVESTMENTANALYSIS_IDS', 'INVESTMENTDETAIL_DESC', 'INVESTMENTDETAIL_ID', 'INVESTMENTDETAIL_STATE', 'MARKETREVENUE_AVGAMOUNT', 'PROFIT_AMOUNT', 'RECORD_DATE', 'REVENUE_AVGAMOUNT', 'REVENUE_TOLERANCE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_AVGRENT', 'SERVERPART_FLOW', 'SERVERPART_ID', 'SERVERPART_NAME', 'SERVERPART_REVENUE', 'STAFF_ID', 'STAFF_NAME', 'VEHICLE_TOLERANCE'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `100.4 ms`
新 API 状态: `200`，耗时 `23.37 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 7477 vs 7477 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 22 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (45 vs 1670)
- Result_Data.List[0].EVALUATE_SCORE: 值不一致 (52.1 vs 31.38)
- Result_Data.List[0].INVESTMENTANALYSIS_ID: 值不一致 (321 vs 474)
- Result_Data.List[0].INVESTMENTDETAIL_ID: 值不一致 (5802 vs 8720)
- Result_Data.List[0].MARKETREVENUE_AVGAMOUNT: 值不一致 (672092.14 vs 380615.05)
- Result_Data.List[0].PROFIT_AMOUNT: 值不一致 (798335.02 vs 357296.07)
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2025-06-06T20:59:41' vs '2025-06-06T21:00:28')
- Result_Data.List[0].REVENUE_AVGAMOUNT: 值不一致 (131029.0 vs 145955.96)
- Result_Data.List[0].REVENUE_TOLERANCE: 类型不一致 (float vs NoneType)，值为 -0.85 vs None
- Result_Data.List[0].SERVERPARTSHOP_ID: 值不一致 ('3922,3923' vs '5318,5319')
- Result_Data.List[0].SERVERPARTSHOP_NAME: 值不一致 ('驿小食' vs '王仁和美食汇')
- Result_Data.List[0].SERVERPART_AVGRENT: 值不一致 (109038.99 vs 41282.48)
- Result_Data.List[0].SERVERPART_FLOW: 类型不一致 (int vs NoneType)，值为 1872585 vs None
- Result_Data.List[0].SERVERPART_ID: 值不一致 (430 vs 943)
- Result_Data.List[0].SERVERPART_NAME: 值不一致 ('颍上服务区' vs '迎河服务区')
- Result_Data.List[0].SERVERPART_REVENUE: 值不一致 (1195712.71 vs 791396.84)
- Result_Data.List[0].VEHICLE_TOLERANCE: 类型不一致 (float vs NoneType)，值为 92.81 vs None
- Result_Data.List[1].BUSINESSPROJECT_ID: 值不一致 (629 vs 1582)
- Result_Data.List[1].EVALUATE_SCORE: 值不一致 (26.5 vs 34.96)
- Result_Data.List[1].INVESTMENTANALYSIS_ID: 值不一致 (321 vs 474)
- Result_Data.List[1].INVESTMENTDETAIL_ID: 值不一致 (5803 vs 8719)
- Result_Data.List[1].MARKETREVENUE_AVGAMOUNT: 值不一致 (516615.08 vs 577765.39)
- Result_Data.List[1].PROFIT_AMOUNT: 值不一致 (-81600.2 vs 112432.91)
- Result_Data.List[1].RECORD_DATE: 值不一致 ('2025-06-06T20:59:41' vs '2025-06-06T21:00:28')
- Result_Data.List[1].REVENUE_AVGAMOUNT: 值不一致 (20526.9 vs 98597.38)

原 API 状态: `200`，耗时 `965.73 ms`
新 API 状态: `200`，耗时 `27.42 ms`

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
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 7 vs 7 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 7 vs 7 |
| List 条数 | ✅ | 7 vs 7 |
| 首条字段集合 | ❌ | 仅原 API: [] | 仅新 API: ['SERVERPART_CODE'] |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].SERVERPART_CODE: 新 API 多出该字段
- Result_Data.List[0].ADJUST_AMOUNT: 值不一致 (4.46 vs 17.09)
- Result_Data.List[0].ADJUST_RATIO: 值不一致 (20.0 vs 26.0)
- Result_Data.List[0].ADJUST_RATIORANGE: 类型不一致 (str vs NoneType)，值为 '20-21.52' vs None
- Result_Data.List[0].ADJUST_RENT: 值不一致 (22.46 vs 47.09)
- Result_Data.List[0].ADJUST_RENTRANGE: 类型不一致 (str vs NoneType)，值为 '22.46' vs None
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (1706 vs 1508)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 值不一致 ('新桥服务区361服饰项目' vs '新桥三河米饺合同项目')
- Result_Data.List[0].BUSINESS_PTRADE: 值不一致 (222 vs 214)
- Result_Data.List[0].BUSINESS_TRADE: 值不一致 (247 vs 229)
- Result_Data.List[0].COMMISSION_AVGRATIO: 值不一致 (21.52 vs 25.12)
- Result_Data.List[0].COMMISSION_MAXRATIO: 值不一致 (30.1 vs 28.0)
- Result_Data.List[0].COMMISSION_MINRATIO: 值不一致 (15.0 vs 20.0)
- Result_Data.List[0].COMMISSION_RATIO: 值不一致 ('18%-20%' vs '23%-26%')
- Result_Data.List[0].GUARANTEERATIO: 值不一致 (15.0 vs 28.0)
- Result_Data.List[0].GUARANTEE_AVGPRICE: 值不一致 (19.9 vs 125.4)
- Result_Data.List[0].GUARANTEE_MAXPRICE: 值不一致 (60.0 vs 350.0)
- Result_Data.List[0].GUARANTEE_MINPRICE: 值不一致 (1.1 vs 25.0)
- Result_Data.List[0].INVESTMENTANALYSIS_ID: 值不一致 (145 vs 146)
- Result_Data.List[0].MINTURNOVER: 值不一致 (18.0 vs 30.0)
- Result_Data.List[0].PERIOD_DEGREE: 值不一致 (97.26 vs 84.11)
- Result_Data.List[0].PROFIT_AMOUNT: 值不一致 (315046.85 vs 176524.52)
- Result_Data.List[0].PROFIT_AVG: 值不一致 (-20.92 vs -1.11)
- Result_Data.List[0].PROFIT_INFO: 值不一致 ('第1期：31.50万元' vs '第1期：50.66万元，第2期：17.65万元')
- Result_Data.List[0].PROFIT_TOTALAMOUNT: 值不一致 (315046.85 vs 683134.19)

原 API 状态: `200`，耗时 `100.43 ms`
新 API 状态: `200`，耗时 `21.36 ms`

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
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 7 vs 7 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 7 vs 7 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children: 列表长度不一致 (1 vs 7)
- Result_Data.List[0].children[0].children: 类型不一致 (list vs NoneType)，值为 [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': None, 'PROJECT_ENDDATE': None, 'ADJUST_RATIORANGE': None, 'ADJUST_RENTRANGE': None, 'INVESTMENTANALYSIS_ID': None, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': None, 'SERVERPARTSHOP_NAME': None, 'BUSINESSPROJECT_ID': None, 'BUSINESSPROJECT_NAME': None, 'SHOPROYALTY_ID': None, 'BUSINESS_TRADE': None, 'BUSINESS_PTRADE': None, 'TRADE_SHOPCOUNT': None, 'TRADE_PROJECTCOUNT': None, 'PROFIT_AVG': None, 'COMMISSION_MINRATIO': None, 'COMMISSION_MAXRATIO': None, 'COMMISSION_AVGRATIO': None, 'GUARANTEE_MINPRICE': None, 'GUARANTEE_MAXPRICE': None, 'GUARANTEE_AVGPRICE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ROYALTY_PRICE': 452.97, 'RENT_RATIO': None, 'PERIOD_DEGREE': None, 'PROFIT_AMOUNT': 335.11, 'PROFIT_TOTALAMOUNT': 2105.54, 'PROFIT_INFO': None, 'COMMISSION_RATIO': None, 'REVENUE_LASTAMOUNT': 2317.84, 'REVENUE_AVGAMOUNT': None, 'ADJUST_RATIO': None, 'ADJUST_RENT': None, 'ADJUST_AMOUNT': 132.04, 'HOLIDAY_TYPE': None, 'INVESTMENTANALYSIS_STATE': None, 'STAFF_ID': None, 'STAFF_NAME': None, 'RECORD_DATE': None, 'INVESTMENTANALYSIS_DESC': None}, 'children': [{'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2025/1/14', 'PROJECT_ENDDATE': '2028/1/13', 'ADJUST_RATIORANGE': '20-21.52', 'ADJUST_RENTRANGE': '22.46', 'INVESTMENTANALYSIS_ID': 145, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '5626,5626,5627', 'SERVERPARTSHOP_NAME': '361度', 'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_NAME': '新桥服务区361服饰项目', 'SHOPROYALTY_ID': 4481, 'BUSINESS_TRADE': 247, 'BUSINESS_PTRADE': 222, 'TRADE_SHOPCOUNT': 6, 'TRADE_PROJECTCOUNT': 10, 'PROFIT_AVG': -20.92, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 30.1, 'COMMISSION_AVGRATIO': 21.52, 'GUARANTEE_MINPRICE': 1.1, 'GUARANTEE_MAXPRICE': 60.0, 'GUARANTEE_AVGPRICE': 19.9, 'MINTURNOVER': 18.0, 'GUARANTEERATIO': 15.0, 'ROYALTY_PRICE': 36.75, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 97.26, 'PROFIT_AMOUNT': 31.5, 'PROFIT_TOTALAMOUNT': 31.5, 'PROFIT_INFO': '第1期：31.50万元', 'COMMISSION_RATIO': '18%-20%', 'REVENUE_LASTAMOUNT': 112.27, 'REVENUE_AVGAMOUNT': 9.35, 'ADJUST_RATIO': 20.0, 'ADJUST_RENT': 22.46, 'ADJUST_AMOUNT': 4.46, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '47.09-125.40', 'INVESTMENTANALYSIS_ID': 146, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2306,2308', 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'SHOPROYALTY_ID': 4098, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 30.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 45.03, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 17.65, 'PROFIT_TOTALAMOUNT': 68.31, 'PROFIT_INFO': '第1期：50.66万元，第2期：17.65万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 181.12, 'REVENUE_AVGAMOUNT': 9.84, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 47.09, 'ADJUST_AMOUNT': 17.09, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '138.80', 'INVESTMENTANALYSIS_ID': 147, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2382,2383', 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'SHOPROYALTY_ID': 4094, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 126.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 166.74, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 76.47, 'PROFIT_TOTALAMOUNT': 276.23, 'PROFIT_INFO': '第1期：199.75万元，第2期：76.47万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 533.84, 'REVENUE_AVGAMOUNT': 27.6, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 138.8, 'ADJUST_AMOUNT': 12.8, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2018/2/1', 'PROJECT_ENDDATE': '2028/1/31', 'ADJUST_RATIORANGE': '20', 'ADJUST_RENTRANGE': '132.17', 'INVESTMENTANALYSIS_ID': 148, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '3064', 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'SHOPROYALTY_ID': 2945, 'BUSINESS_TRADE': 227, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 13, 'TRADE_PROJECTCOUNT': 15, 'PROFIT_AVG': -38.44, 'COMMISSION_MINRATIO': 8.0, 'COMMISSION_MAXRATIO': 35.0, 'COMMISSION_AVGRATIO': 19.33, 'GUARANTEE_MINPRICE': 7.0, 'GUARANTEE_MAXPRICE': 50.0, 'GUARANTEE_AVGPRICE': 29.79, 'MINTURNOVER': 40.0, 'GUARANTEERATIO': 16.0, 'ROYALTY_PRICE': 0.0, 'RENT_RATIO': 0.0, 'PERIOD_DEGREE': 92.33, 'PROFIT_AMOUNT': 235.54, 'PROFIT_TOTALAMOUNT': 1515.15, 'PROFIT_INFO': '第1期：0万元，第2期：0万元，第3期：0万元，第4期：295.99万元，第5期：260.90万元，第6期：333.89万元，第7期：388.81万元，第8期：235.54万元', 'COMMISSION_RATIO': '15%-20%', 'REVENUE_LASTAMOUNT': 660.85, 'REVENUE_AVGAMOUNT': 37.9, 'ADJUST_RATIO': 20.0, 'ADJUST_RENT': 132.17, 'ADJUST_AMOUNT': 92.17, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '26', 'ADJUST_RENTRANGE': '75.51-125.40', 'INVESTMENTANALYSIS_ID': 149, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'SHOPROYALTY_ID': 4102, 'BUSINESS_TRADE': 229, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 18, 'TRADE_PROJECTCOUNT': 59, 'PROFIT_AVG': -1.11, 'COMMISSION_MINRATIO': 20.0, 'COMMISSION_MAXRATIO': 28.0, 'COMMISSION_AVGRATIO': 25.12, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 350.0, 'GUARANTEE_AVGPRICE': 125.4, 'MINTURNOVER': 50.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 52.45, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': 12.68, 'PROFIT_TOTALAMOUNT': 102.72, 'PROFIT_INFO': '第1期：90.03万元，第2期：12.68万元', 'COMMISSION_RATIO': '23%-26%', 'REVENUE_LASTAMOUNT': 290.43, 'REVENUE_AVGAMOUNT': 11.2, 'ADJUST_RATIO': 26.0, 'ADJUST_RENT': 75.51, 'ADJUST_AMOUNT': 25.51, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/2/14', 'ADJUST_RATIORANGE': '28-32.20', 'ADJUST_RENTRANGE': '95.89', 'INVESTMENTANALYSIS_ID': 150, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'SHOPROYALTY_ID': 4110, 'BUSINESS_TRADE': 234, 'BUSINESS_PTRADE': 214, 'TRADE_SHOPCOUNT': 12, 'TRADE_PROJECTCOUNT': 37, 'PROFIT_AVG': -16.6, 'COMMISSION_MINRATIO': 23.0, 'COMMISSION_MAXRATIO': 50.2, 'COMMISSION_AVGRATIO': 32.2, 'GUARANTEE_MINPRICE': 25.0, 'GUARANTEE_MAXPRICE': 180.0, 'GUARANTEE_AVGPRICE': 89.92, 'MINTURNOVER': 126.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 104.35, 'RENT_RATIO': 82.82, 'PERIOD_DEGREE': 88.49, 'PROFIT_AMOUNT': -25.71, 'PROFIT_TOTALAMOUNT': 66.29, 'PROFIT_INFO': '第1期：92.00万元，第2期：-25.71万元', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': 342.45, 'REVENUE_AVGAMOUNT': 14.84, 'ADJUST_RATIO': 28.0, 'ADJUST_RENT': 95.89, 'ADJUST_AMOUNT': -30.11, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}, {'node': {'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'PROJECT_STARTDATE': '2024/2/1', 'PROJECT_ENDDATE': '2027/3/2', 'ADJUST_RATIORANGE': '28-28.04', 'ADJUST_RENTRANGE': '55.12-77.76', 'INVESTMENTANALYSIS_ID': 151, 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_TYPE': 1000, 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_NAME': '新桥服务区烧饼合同项目', 'SHOPROYALTY_ID': 4106, 'BUSINESS_TRADE': 243, 'BUSINESS_PTRADE': 220, 'TRADE_SHOPCOUNT': 40, 'TRADE_PROJECTCOUNT': 73, 'PROFIT_AVG': -73.24, 'COMMISSION_MINRATIO': 15.0, 'COMMISSION_MAXRATIO': 50.2, 'COMMISSION_AVGRATIO': 28.04, 'GUARANTEE_MINPRICE': 5.0, 'GUARANTEE_MAXPRICE': 252.0, 'GUARANTEE_AVGPRICE': 77.76, 'MINTURNOVER': 45.0, 'GUARANTEERATIO': 28.0, 'ROYALTY_PRICE': 47.62, 'RENT_RATIO': 100.0, 'PERIOD_DEGREE': 84.11, 'PROFIT_AMOUNT': -13.03, 'PROFIT_TOTALAMOUNT': 45.32, 'PROFIT_INFO': '第1期：58.35万元，第2期：-13.03万元', 'COMMISSION_RATIO': '25%-28%', 'REVENUE_LASTAMOUNT': 196.83, 'REVENUE_AVGAMOUNT': 7.12, 'ADJUST_RATIO': 28.0, 'ADJUST_RENT': 55.12, 'ADJUST_AMOUNT': 10.12, 'HOLIDAY_TYPE': 0, 'INVESTMENTANALYSIS_STATE': 1, 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'RECORD_DATE': '2026-01-04T21:07:48', 'INVESTMENTANALYSIS_DESC': ''}, 'children': None}]}] vs None
- Result_Data.List[0].children[0].node.SERVERPART_CODE: 新 API 多出该字段
- Result_Data.List[0].children[0].node.ADJUST_AMOUNT: 值不一致 (132.04 vs 17.09)
- Result_Data.List[0].children[0].node.ADJUST_RATIO: 类型不一致 (NoneType vs float)，值为 None vs 26.0
- Result_Data.List[0].children[0].node.ADJUST_RENT: 类型不一致 (NoneType vs float)，值为 None vs 47.09
- Result_Data.List[0].children[0].node.BUSINESSPROJECT_ID: 类型不一致 (NoneType vs int)，值为 None vs 1508
- Result_Data.List[0].children[0].node.BUSINESSPROJECT_NAME: 类型不一致 (NoneType vs str)，值为 None vs '新桥三河米饺合同项目'
- Result_Data.List[0].children[0].node.BUSINESS_PTRADE: 类型不一致 (NoneType vs int)，值为 None vs 214
- Result_Data.List[0].children[0].node.BUSINESS_TRADE: 类型不一致 (NoneType vs int)，值为 None vs 229
- Result_Data.List[0].children[0].node.COMMISSION_AVGRATIO: 类型不一致 (NoneType vs float)，值为 None vs 25.12
- Result_Data.List[0].children[0].node.COMMISSION_MAXRATIO: 类型不一致 (NoneType vs float)，值为 None vs 28.0
- Result_Data.List[0].children[0].node.COMMISSION_MINRATIO: 类型不一致 (NoneType vs float)，值为 None vs 20.0
- Result_Data.List[0].children[0].node.COMMISSION_RATIO: 类型不一致 (NoneType vs str)，值为 None vs '23%-26%'
- Result_Data.List[0].children[0].node.GUARANTEERATIO: 类型不一致 (NoneType vs float)，值为 None vs 28.0
- Result_Data.List[0].children[0].node.GUARANTEE_AVGPRICE: 类型不一致 (NoneType vs float)，值为 None vs 125.4
- Result_Data.List[0].children[0].node.GUARANTEE_MAXPRICE: 类型不一致 (NoneType vs float)，值为 None vs 350.0
- Result_Data.List[0].children[0].node.GUARANTEE_MINPRICE: 类型不一致 (NoneType vs float)，值为 None vs 25.0
- Result_Data.List[0].children[0].node.HOLIDAY_TYPE: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.List[0].children[0].node.INVESTMENTANALYSIS_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.List[0].children[0].node.INVESTMENTANALYSIS_ID: 类型不一致 (NoneType vs int)，值为 None vs 146
- Result_Data.List[0].children[0].node.INVESTMENTANALYSIS_STATE: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.List[0].children[0].node.MINTURNOVER: 类型不一致 (NoneType vs float)，值为 None vs 30.0
- Result_Data.List[0].children[0].node.PERIOD_DEGREE: 类型不一致 (NoneType vs float)，值为 None vs 84.11
- Result_Data.List[0].children[0].node.PROFIT_AMOUNT: 值不一致 (335.11 vs 176524.52)

原 API 状态: `200`，耗时 `189.38 ms`
新 API 状态: `200`，耗时 `26.02 ms`

### Analysis/GetPERIODMONTHPROFITDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PERIODMONTHPROFITId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPERIODMONTHPROFITDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPERIODMONTHPROFITDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ACTUAL_RATIO', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESS_PERIOD', 'BUSINESS_STATE', 'BUSINESS_STATES', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'BUSINESS_TYPES', 'CA_COST', 'COMMISSION_RATIO', 'COST_AMOUNT', 'COST_RATE', 'DEPRECIATION_EXPENSE', 'DEPRECIATION_YEAR', 'ENDDATE', 'GUARANTEERATIO', 'GUARANTEE_PRICE', 'LABOURS_COUNT', 'LABOURS_WAGE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MINTURNOVER', 'MONTH_COUNT', 'OTHER_EXPENSE', 'PERIODMONTHPROFIT_ID', 'PERIOD_INDEX', 'PROFIT_AMOUNT', 'PROFIT_AVG', 'PROFIT_SD', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'RECORD_DATE', 'RENTFEE', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SETTLEMENT_MODESS', 'SHOPROYALTY_ID', 'SHOPROYALTY_IDS', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'SUBROYALTY_THEORY', 'TICKET_COUNT', 'WARNING_CONTENT', 'WARNING_TYPE', 'WARNING_TYPES'] vs ['ACTUAL_RATIO', 'BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESS_PERIOD', 'BUSINESS_STATE', 'BUSINESS_STATES', 'BUSINESS_TRADE', 'BUSINESS_TYPE', 'BUSINESS_TYPES', 'CA_COST', 'COMMISSION_RATIO', 'COST_AMOUNT', 'COST_RATE', 'DEPRECIATION_EXPENSE', 'DEPRECIATION_YEAR', 'ENDDATE', 'GUARANTEERATIO', 'GUARANTEE_PRICE', 'LABOURS_COUNT', 'LABOURS_WAGE', 'MERCHANTS_ID', 'MERCHANTS_NAME', 'MINTURNOVER', 'MONTH_COUNT', 'OTHER_EXPENSE', 'PERIODMONTHPROFIT_ID', 'PERIOD_INDEX', 'PROFIT_AMOUNT', 'PROFIT_AVG', 'PROFIT_SD', 'PROJECT_ENDDATE', 'PROJECT_STARTDATE', 'RECORD_DATE', 'RENTFEE', 'REVENUE_AMOUNT', 'ROYALTY_PRICE', 'ROYALTY_THEORY', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SETTLEMENT_MODES', 'SETTLEMENT_MODESS', 'SHOPROYALTY_ID', 'SHOPROYALTY_IDS', 'STAFF_ID', 'STAFF_NAME', 'STARTDATE', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'SUBROYALTY_THEORY', 'TICKET_COUNT', 'WARNING_CONTENT', 'WARNING_TYPE', 'WARNING_TYPES'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `67.05 ms`
新 API 状态: `200`，耗时 `20.64 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 9847 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ❌ | 1 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 58 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 9)
- Result_Data.List[0].ACTUAL_RATIO: 值不一致 (50.35 vs 8.0)
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (668 vs 912)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 值不一致 ('清溪服务区轻餐饮QX-07项目' vs '君王服务区麦当劳项目')
- Result_Data.List[0].BUSINESS_TRADE: 值不一致 (215 vs 227)
- Result_Data.List[0].COMMISSION_RATIO: 值不一致 (28.0 vs 20.0)
- Result_Data.List[0].COST_AMOUNT: 值不一致 (616037.93 vs 483473.6)
- Result_Data.List[0].ENDDATE: 类型不一致 (str vs int)，值为 '2024/06/02' vs 20260630
- Result_Data.List[0].GUARANTEERATIO: 值不一致 (41.1 vs 8.0)
- Result_Data.List[0].GUARANTEE_PRICE: 值不一致 (105.0 vs 250.0)
- Result_Data.List[0].MERCHANTS_ID: 值不一致 (-2036 vs -580)
- Result_Data.List[0].MERCHANTS_NAME: 值不一致 ('桐乡市盛开源高速公路服务区经营管理有限公司' vs '安徽联升餐厅食品有限公司')
- Result_Data.List[0].MINTURNOVER: 值不一致 (350000.0 vs 200000.0)
- Result_Data.List[0].MONTH_COUNT: 值不一致 (12.0 vs 6.0)
- Result_Data.List[0].PERIODMONTHPROFIT_ID: 值不一致 (651 vs 9852)
- Result_Data.List[0].PROFIT_AMOUNT: 值不一致 (62341.04 vs 955438.29)
- Result_Data.List[0].PROFIT_AVG: 值不一致 (10390.17 vs 159239.72)
- Result_Data.List[0].PROFIT_SD: 值不一致 (37405.78 vs 104319.21)
- Result_Data.List[0].PROJECT_ENDDATE: 类型不一致 (str vs int)，值为 '2026/06/02' vs 20330630
- Result_Data.List[0].PROJECT_STARTDATE: 类型不一致 (str vs int)，值为 '2023/06/03' vs 20230701
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2025-05-14T19:25:25' vs '2026-01-07T12:24:39')
- Result_Data.List[0].REVENUE_AMOUNT: 值不一致 (1373523.0 vs 1564034.66)
- Result_Data.List[0].ROYALTY_PRICE: 值不一致 (688560.35 vs 0.0)
- Result_Data.List[0].ROYALTY_THEORY: 值不一致 (691533.94 vs 125122.77)
- Result_Data.List[0].SERVERPARTSHOP_ID: 值不一致 ('1374,1375' vs '1461,1460')

原 API 状态: `200`，耗时 `91.68 ms`
新 API 状态: `200`，耗时 `30.63 ms`

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

原 API 状态: `404`，耗时 `4.3 ms`
新 API 状态: `200`，耗时 `6.71 ms`

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

原 API 状态: `200`，耗时 `10.43 ms`
新 API 状态: `200`，耗时 `6.41 ms`

### Analysis/GetPROFITCONTRIBUTEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROFITCONTRIBUTEId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPROFITCONTRIBUTEDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPROFITCONTRIBUTEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESSTRADETYPE', 'CALCULATE_SELFSHOP', 'EVALUATE_SCORE', 'EVALUATE_TYPE', 'EVALUATE_TYPES', 'PROFITCONTRIBUTE_DESC', 'PROFITCONTRIBUTE_ID', 'PROFITCONTRIBUTE_PID', 'PROFITCONTRIBUTE_STATE', 'RECORD_DATE', 'SABFI_SCORE', 'SABFI_TYPE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE', 'STATISTICS_DATE_End', 'STATISTICS_DATE_Start'] vs ['BUSINESSPROJECT_ID', 'BUSINESSPROJECT_IDS', 'BUSINESSPROJECT_NAME', 'BUSINESSTRADETYPE', 'CALCULATE_SELFSHOP', 'EVALUATE_SCORE', 'EVALUATE_TYPE', 'EVALUATE_TYPES', 'PROFITCONTRIBUTE_DESC', 'PROFITCONTRIBUTE_ID', 'PROFITCONTRIBUTE_PID', 'PROFITCONTRIBUTE_STATE', 'RECORD_DATE', 'SABFI_SCORE', 'SABFI_TYPE', 'SERVERPARTSHOP_ID', 'SERVERPARTSHOP_IDS', 'SERVERPARTSHOP_NAME', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'STAFF_ID', 'STAFF_NAME', 'STATISTICS_DATE', 'STATISTICS_DATE_End', 'STATISTICS_DATE_Start'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `74.74 ms`
新 API 状态: `200`，耗时 `14.57 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 3003 vs 149590 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 26 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].BUSINESSPROJECT_ID: 值不一致 (50 vs 1760)
- Result_Data.List[0].BUSINESSPROJECT_NAME: 值不一致 ('新桥服务区（品牌寿司(新业态））项目' vs '')
- Result_Data.List[0].CALCULATE_SELFSHOP: 值不一致 (1 vs 2)
- Result_Data.List[0].EVALUATE_SCORE: 类型不一致 (NoneType vs float)，值为 None vs 7.0
- Result_Data.List[0].EVALUATE_TYPE: 值不一致 (0 vs 6)
- Result_Data.List[0].PROFITCONTRIBUTE_ID: 值不一致 (7 vs 190668)
- Result_Data.List[0].PROFITCONTRIBUTE_PID: 值不一致 (-1 vs 190662)
- Result_Data.List[0].PROFITCONTRIBUTE_STATE: 值不一致 (0 vs 1)
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2024-11-01T16:30:43' vs '2026-01-07T15:21:49')
- Result_Data.List[0].SABFI_SCORE: 类型不一致 (NoneType vs float)，值为 None vs 7.0
- Result_Data.List[0].SERVERPARTSHOP_ID: 值不一致 ('3058,3059' vs '5580,5581')
- Result_Data.List[0].SERVERPARTSHOP_NAME: 值不一致 ('鲜道寿司' vs '美食汇')
- Result_Data.List[0].SERVERPART_ID: 值不一致 (416 vs 967)
- Result_Data.List[0].SERVERPART_NAME: 值不一致 ('新桥服务区' vs '洪林服务区')
- Result_Data.List[0].STATISTICS_DATE: 值不一致 ('2024/10' vs '2025/07')
- Result_Data.List[1].BUSINESSPROJECT_ID: 值不一致 (166 vs 1760)
- Result_Data.List[1].BUSINESSPROJECT_NAME: 值不一致 ('新桥服务区（麦当劳）项目' vs '')
- Result_Data.List[1].CALCULATE_SELFSHOP: 值不一致 (1 vs 2)
- Result_Data.List[1].EVALUATE_SCORE: 值不一致 (41.66 vs 10.0)
- Result_Data.List[1].EVALUATE_TYPE: 值不一致 (0 vs 5)
- Result_Data.List[1].PROFITCONTRIBUTE_ID: 值不一致 (37 vs 190667)
- Result_Data.List[1].PROFITCONTRIBUTE_PID: 值不一致 (-1 vs 190662)
- Result_Data.List[1].RECORD_DATE: 值不一致 ('2024-11-01T16:30:43' vs '2026-01-07T15:21:49')
- Result_Data.List[1].SABFI_SCORE: 类型不一致 (NoneType vs float)，值为 None vs 10.0
- Result_Data.List[1].SERVERPARTSHOP_ID: 值不一致 ('3065,3064' vs '5580,5581')

原 API 状态: `200`，耗时 `298.91 ms`
新 API 状态: `200`，耗时 `48.74 ms`

### Analysis/GetPROMPTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"PROMPTId": 5}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetPROMPTDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetPROMPTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'PROMPT_CONTENT', 'PROMPT_DESC', 'PROMPT_ID', 'PROMPT_STATE', 'PROMPT_SWITCH', 'PROMPT_TYPE', 'PROMPT_TYPES', 'STAFF_ID', 'STAFF_NAME'] vs ['OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'PROMPT_CONTENT', 'PROMPT_DESC', 'PROMPT_ID', 'PROMPT_STATE', 'PROMPT_SWITCH', 'PROMPT_TYPE', 'PROMPT_TYPES', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `69.73 ms`
新 API 状态: `200`，耗时 `38.64 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 3 vs 3 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 3 vs 3 |
| 首条字段集合 | ✅ | 字段一致，共 12 个 |
| 完整响应体 | ❌ | 发现 18 处差异 |

差异明细：
- Result_Data.List[0].OPERATE_DATE: 类型不一致 (str vs NoneType)，值为 '2025/3/28 10:24:37' vs None
- Result_Data.List[0].PROMPT_CONTENT: 值不一致 ('       请结合问题解析关键字和用户的提问，严谨分析数据字段内容，给出经营数据分析总结，无需建议，注意段落区分且清晰。\n\n       1、先有概述，分析整理数据统计汇总、统计时间、同环比日期和天数，金额和车辆数据请用万为单位，段落清晰；\n\n       2、如果查询日期内包含节假日概念，请给与具体日期说明，同比数据请注明日期比对天数，这里应该考虑车流的增减幅度对营收的影响；\n\n       3、整体服务区营收、车流、客单、盈利（甲方与商家）情况分析，重点关注同环比车流对各项数据造成的变化，根据合同时间，关注是否有新增或者关闭的门店；\n\n       4、分析每个在营门店的营收、车流、客单、盈利（甲方与商家）情况并分析，分析依据如下：\n---自营代表甲方自主经营，租赁代表甲方收取保底+提成，请分开展示；\n---根据合同时间判断门店是否已到期，已到期门店不进行数据分析；\n---如出现营收增幅与整体入区车流偏差较大的情况请列出，如车流增幅大于营收增幅，代表业态门店获客能力较差；\n---甲方更多收入的门店比较优秀，请说明；\n---需要结合客单量和客单均价来体现门店受消费者的喜爱程度，增幅较大的客单量和客单均价代表受顾客喜爱；\n\n      5、如有多服务区，结合多个服务区的经营数据进行分析，同比变化最大的需重点列出说明，没有则不进行比较；\n\n      6、暂时不结合区域周边县市（列出名字）的经济特色进行分析考虑；\n\n      7、总结内容提出对一些问题的思考逻辑。\n\n其他注意：\n      1、经营数据无需区分东（南）区或者西（北）区分析，且不要说出根据JSON数据的文字；\n      2、甲方收入=盈利收入=业主收入=驿达收入，统一用驿达公司表示；\n      3、如果需要更加深入的分析，请提出需要补充的数据内容，并用-----分隔。\n ' vs '')
- Result_Data.List[0].PROMPT_DESC: 值不一致 ('引入地图的语义，对返回过来的表格或文字进行优化' vs '')
- Result_Data.List[0].PROMPT_ID: 值不一致 (5 vs 7)
- Result_Data.List[0].PROMPT_STATE: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.List[0].PROMPT_SWITCH: 类型不一致 (int vs NoneType)，值为 1 vs None
- Result_Data.List[0].PROMPT_TYPE: 类型不一致 (int vs NoneType)，值为 1000 vs None
- Result_Data.List[0].STAFF_ID: 类型不一致 (int vs NoneType)，值为 2785 vs None
- Result_Data.List[0].STAFF_NAME: 值不一致 ('严琅杰' vs '')
- Result_Data.List[2].OPERATE_DATE: 类型不一致 (NoneType vs str)，值为 None vs '2025/3/28 10:24:37'
- Result_Data.List[2].PROMPT_CONTENT: 值不一致 ('' vs '       请结合问题解析关键字和用户的提问，严谨分析数据字段内容，给出经营数据分析总结，无需建议，注意段落区分且清晰。\n\n       1、先有概述，分析整理数据统计汇总、统计时间、同环比日期和天数，金额和车辆数据请用万为单位，段落清晰；\n\n       2、如果查询日期内包含节假日概念，请给与具体日期说明，同比数据请注明日期比对天数，这里应该考虑车流的增减幅度对营收的影响；\n\n       3、整体服务区营收、车流、客单、盈利（甲方与商家）情况分析，重点关注同环比车流对各项数据造成的变化，根据合同时间，关注是否有新增或者关闭的门店；\n\n       4、分析每个在营门店的营收、车流、客单、盈利（甲方与商家）情况并分析，分析依据如下：\n---自营代表甲方自主经营，租赁代表甲方收取保底+提成，请分开展示；\n---根据合同时间判断门店是否已到期，已到期门店不进行数据分析；\n---如出现营收增幅与整体入区车流偏差较大的情况请列出，如车流增幅大于营收增幅，代表业态门店获客能力较差；\n---甲方更多收入的门店比较优秀，请说明；\n---需要结合客单量和客单均价来体现门店受消费者的喜爱程度，增幅较大的客单量和客单均价代表受顾客喜爱；\n\n      5、如有多服务区，结合多个服务区的经营数据进行分析，同比变化最大的需重点列出说明，没有则不进行比较；\n\n      6、暂时不结合区域周边县市（列出名字）的经济特色进行分析考虑；\n\n      7、总结内容提出对一些问题的思考逻辑。\n\n其他注意：\n      1、经营数据无需区分东（南）区或者西（北）区分析，且不要说出根据JSON数据的文字；\n      2、甲方收入=盈利收入=业主收入=驿达收入，统一用驿达公司表示；\n      3、如果需要更加深入的分析，请提出需要补充的数据内容，并用-----分隔。\n ')
- Result_Data.List[2].PROMPT_DESC: 值不一致 ('' vs '引入地图的语义，对返回过来的表格或文字进行优化')
- Result_Data.List[2].PROMPT_ID: 值不一致 (7 vs 5)
- Result_Data.List[2].PROMPT_STATE: 类型不一致 (int vs NoneType)，值为 0 vs None
- Result_Data.List[2].PROMPT_SWITCH: 类型不一致 (NoneType vs int)，值为 None vs 1
- Result_Data.List[2].PROMPT_TYPE: 类型不一致 (NoneType vs int)，值为 None vs 1000
- Result_Data.List[2].STAFF_ID: 类型不一致 (NoneType vs int)，值为 None vs 2785
- Result_Data.List[2].STAFF_NAME: 值不一致 ('' vs '严琅杰')

原 API 状态: `200`，耗时 `95.13 ms`
新 API 状态: `200`，耗时 `45.77 ms`

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
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 1 vs 1 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children: 列表长度不一致 (1 vs 9)
- Result_Data.List[0].children[0].children: 类型不一致 (list vs NoneType)，值为 [{'node': {'BUSINESSPROJECT_ID': 1706, 'BUSINESSPROJECT_NAME': '新桥服务区361服饰项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '5626,5627', 'SERVERPARTSHOP_NAME': '361度', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 247, 'MERCHANTS_ID': -2188, 'MERCHANTS_NAME': '河南省道和高速公路服务区经营管理有限公司', 'PROJECT_STARTDATE': '2025/01/14', 'PROJECT_ENDDATE': '2028/01/13', 'GUARANTEE_PRICE': 54.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 35.46, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 50697.0, 'COST_AMOUNT': 38583.84, 'ROYALTY_PRICE': 7096.05, 'ROYALTY_THEORY': 17979.32, 'SUBROYALTY_THEORY': 32585.07, 'PROFIT_AMOUNT': -5998.77, 'PROFIT_RATE': None, 'PROFIT_SD': 64942.0, 'PROFIT_AVG': 51949.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 303, 'CA_COST': 127.34, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1508, 'BUSINESSPROJECT_NAME': '新桥三河米饺合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2308,2306', 'SERVERPARTSHOP_NAME': '丁记米饺', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 229, 'MERCHANTS_ID': -2115, 'MERCHANTS_NAME': '合肥市丁记米饺食品有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 90.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 36.01, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 60423.0, 'COST_AMOUNT': 40529.05, 'ROYALTY_PRICE': 15740.48, 'ROYALTY_THEORY': 21755.43, 'SUBROYALTY_THEORY': 38512.48, 'PROFIT_AMOUNT': -2016.57, 'PROFIT_RATE': None, 'PROFIT_SD': 34324.0, 'PROFIT_AVG': 28753.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 3681, 'CA_COST': 11.01, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1506, 'BUSINESSPROJECT_NAME': '新桥服务区丁家馄饨合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2383,2382', 'SERVERPARTSHOP_NAME': '丁家馄饨', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 229, 'MERCHANTS_ID': -2114, 'MERCHANTS_NAME': '淮南丁家餐饮有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 378.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 54.37, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 213846.0, 'COST_AMOUNT': 71213.65, 'ROYALTY_PRICE': 57374.52, 'ROYALTY_THEORY': 116274.11, 'SUBROYALTY_THEORY': 96989.49, 'PROFIT_AMOUNT': 25775.84, 'PROFIT_RATE': None, 'PROFIT_SD': 112653.0, 'PROFIT_AVG': 126487.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 7502, 'CA_COST': 9.49, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 166, 'BUSINESSPROJECT_NAME': '新桥服务区（麦当劳）项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '3065,3064', 'SERVERPARTSHOP_NAME': '麦当劳', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 227, 'MERCHANTS_ID': -580, 'MERCHANTS_NAME': '安徽联升餐厅食品有限公司', 'PROJECT_STARTDATE': '2018/02/01', 'PROJECT_ENDDATE': '2028/01/31', 'GUARANTEE_PRICE': 400.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 9999, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 16.0, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 144796.87, 'COST_AMOUNT': 57403.81, 'ROYALTY_PRICE': 0.0, 'ROYALTY_THEORY': 23167.5, 'SUBROYALTY_THEORY': 121629.37, 'PROFIT_AMOUNT': 64225.56, 'PROFIT_RATE': None, 'PROFIT_SD': 480316.0, 'PROFIT_AVG': 389118.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 4089, 'CA_COST': 14.04, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1510, 'BUSINESSPROJECT_NAME': '新桥服务区同庆楼鲜肉大包合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2198,2200', 'SERVERPARTSHOP_NAME': '同庆楼鲜肉大包', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 229, 'MERCHANTS_ID': -2116, 'MERCHANTS_NAME': '合肥书山有陆餐饮管理有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 150.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 59.72, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 81904.8, 'COST_AMOUNT': 44825.41, 'ROYALTY_PRICE': 37804.06, 'ROYALTY_THEORY': 48910.62, 'SUBROYALTY_THEORY': 32778.57, 'PROFIT_AMOUNT': -12046.84, 'PROFIT_RATE': None, 'PROFIT_SD': 33288.0, 'PROFIT_AVG': 20478.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 6411, 'CA_COST': 6.99, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1514, 'BUSINESSPROJECT_NAME': '新桥服务区王仁和米线店新店合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2468,2469', 'SERVERPARTSHOP_NAME': '王仁和米线店', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 234, 'MERCHANTS_ID': -1116, 'MERCHANTS_NAME': '合肥王仁和米线餐饮管理有限公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/02/14', 'GUARANTEE_PRICE': 378.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 112.95, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 101447.8, 'COST_AMOUNT': 48734.01, 'ROYALTY_PRICE': 68105.66, 'ROYALTY_THEORY': 114586.78, 'SUBROYALTY_THEORY': -13413.17, 'PROFIT_AMOUNT': -62147.18, 'PROFIT_RATE': None, 'PROFIT_SD': 39837.0, 'PROFIT_AVG': -42611.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 3312, 'CA_COST': 14.71, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 947, 'BUSINESSPROJECT_NAME': '合肥蔚电科技有限公司', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '1878,1872,1877,1871,1874,1868,1870,1875,1876', 'SERVERPARTSHOP_NAME': '蔚来换电', 'BUSINESS_STATE': 3000, 'BUSINESS_TRADE': None, 'MERCHANTS_ID': -1636, 'MERCHANTS_NAME': '合肥蔚电科技有限公司', 'PROJECT_STARTDATE': '2021/12/01', 'PROJECT_ENDDATE': '2026/11/30', 'GUARANTEE_PRICE': 225.0, 'BUSINESS_TYPE': 2000, 'SETTLEMENT_MODES': 1000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': None, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 0.0, 'COST_AMOUNT': 0.0, 'ROYALTY_PRICE': 0.0, 'ROYALTY_THEORY': 38219.28, 'SUBROYALTY_THEORY': -38219.28, 'PROFIT_AMOUNT': 0.0, 'PROFIT_RATE': None, 'PROFIT_SD': 0.0, 'PROFIT_AVG': 0.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 0, 'CA_COST': None, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1512, 'BUSINESSPROJECT_NAME': '新桥服务区烧饼合同项目', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '2270,2271', 'SERVERPARTSHOP_NAME': '下塘烧饼', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 243, 'MERCHANTS_ID': -2117, 'MERCHANTS_NAME': '合肥徽蕴堂餐饮管理有限责任公司', 'PROJECT_STARTDATE': '2024/02/01', 'PROJECT_ENDDATE': '2027/03/02', 'GUARANTEE_PRICE': 135.0, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 3000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 109.0, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 38327.0, 'COST_AMOUNT': 36109.85, 'ROYALTY_PRICE': 25546.5, 'ROYALTY_THEORY': 41776.05, 'SUBROYALTY_THEORY': -3552.89, 'PROFIT_AMOUNT': -39662.74, 'PROFIT_RATE': None, 'PROFIT_SD': 21923.0, 'PROFIT_AVG': -21851.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 2336, 'CA_COST': 15.46, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}, {'node': {'BUSINESSPROJECT_ID': 1905, 'BUSINESSPROJECT_NAME': '服务区自助售卖玩具机项目租赁合同新桥', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SERVERPART_ID': 416, 'SERVERPART_NAME': '新桥服务区', 'SERVERPARTSHOP_ID': '7105,7104', 'SERVERPARTSHOP_NAME': '自助玩具机', 'BUSINESS_STATE': 1000, 'BUSINESS_TRADE': 246, 'MERCHANTS_ID': -2182, 'MERCHANTS_NAME': '江苏乾上乾贸易有限公司', 'PROJECT_STARTDATE': '2025/07/15', 'PROJECT_ENDDATE': '2028/07/14', 'GUARANTEE_PRICE': 3.03, 'BUSINESS_TYPE': 1000, 'SETTLEMENT_MODES': 1000, 'BUSINESS_PERIOD': None, 'PERIOD_INDEX': None, 'STARTDATE': None, 'ENDDATE': None, 'RENTFEE': None, 'MINTURNOVER': None, 'GUARANTEERATIO': None, 'ACTUAL_RATIO': 12.0, 'COMMISSION_RATIO': None, 'REVENUE_AMOUNT': 8212.0, 'COST_AMOUNT': 30086.85, 'ROYALTY_PRICE': 0.0, 'ROYALTY_THEORY': 985.44, 'SUBROYALTY_THEORY': 7226.56, 'PROFIT_AMOUNT': -22860.29, 'PROFIT_RATE': None, 'PROFIT_SD': 7770.0, 'PROFIT_AVG': -14338.0, 'COST_RATE': None, 'MONTH_COUNT': None, 'LABOURS_COUNT': None, 'LABOURS_WAGE': None, 'DEPRECIATION_EXPENSE': None, 'DEPRECIATION_YEAR': None, 'OTHER_EXPENSE': None, 'WARNING_TYPE': None, 'WARNING_CONTENT': None, 'TICKET_COUNT': 118, 'CA_COST': 254.97, 'BUSINESS_STARTDATE': None, 'BUSINESS_ENDDATE': None, 'Brand_ICO': None, 'MERCHANTS_ID_Encrypted': None, 'ProjectProgress': None, 'PaymentProgress': None}, 'children': []}] vs None
- Result_Data.List[0].children[0].node.BUSINESS_ENDDATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.BUSINESS_STARTDATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.MERCHANTS_ID_Encrypted: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.PROFIT_RATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.PaymentProgress: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.ProjectProgress: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].node.PERIODMONTHPROFIT_ID: 新 API 多出该字段
- Result_Data.List[0].children[0].node.RECORD_DATE: 新 API 多出该字段
- Result_Data.List[0].children[0].node.SHOPROYALTY_ID: 新 API 多出该字段
- Result_Data.List[0].children[0].node.STAFF_ID: 新 API 多出该字段
- Result_Data.List[0].children[0].node.STAFF_NAME: 新 API 多出该字段
- Result_Data.List[0].children[0].node.STATISTICS_MONTH: 新 API 多出该字段
- Result_Data.List[0].children[0].node.ACTUAL_RATIO: 值不一致 (60.55 vs 32.96)
- Result_Data.List[0].children[0].node.BUSINESSPROJECT_ID: 类型不一致 (NoneType vs int)，值为 None vs 1508
- Result_Data.List[0].children[0].node.BUSINESSPROJECT_NAME: 类型不一致 (NoneType vs str)，值为 None vs '新桥三河米饺合同项目'
- Result_Data.List[0].children[0].node.BUSINESS_PERIOD: 类型不一致 (NoneType vs str)，值为 None vs ''
- Result_Data.List[0].children[0].node.BUSINESS_STATE: 类型不一致 (NoneType vs int)，值为 None vs 1000
- Result_Data.List[0].children[0].node.BUSINESS_TRADE: 类型不一致 (NoneType vs int)，值为 None vs 229
- Result_Data.List[0].children[0].node.BUSINESS_TYPE: 类型不一致 (NoneType vs int)，值为 None vs 1000
- Result_Data.List[0].children[0].node.CA_COST: 类型不一致 (float vs NoneType)，值为 13.24 vs None

原 API 状态: `200`，耗时 `182.5 ms`
新 API 状态: `200`，耗时 `55.71 ms`

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
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 0 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 1 vs 1 |
| List 条数 | ❌ | 1 vs 0 |
| 首条字段集合 | ✅ | 至少一侧为空列表，跳过字段扫描 |
| 完整响应体 | ❌ | 发现 2 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 0)
- Result_Data.TotalCount: 值不一致 (1 vs 0)

原 API 状态: `200`，耗时 `158.89 ms`
新 API 状态: `200`，耗时 `38.28 ms`

### Analysis/GetSENTENCEDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SENTENCEId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetSENTENCEDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetSENTENCEDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ANALYSISRULE_ID', 'DIALOG_CODE', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'SENTENCE_CONTENT', 'SENTENCE_ID', 'SENTENCE_RESULT', 'SENTENCE_STATE', 'SENTENCE_TYPE', 'SERVERPART_ID', 'STAFF_ID', 'STAFF_NAME'] vs ['ANALYSISRULE_ID', 'DIALOG_CODE', 'OPERATE_DATE', 'OPERATE_DATE_End', 'OPERATE_DATE_Start', 'SENTENCE_CONTENT', 'SENTENCE_ID', 'SENTENCE_RESULT', 'SENTENCE_STATE', 'SENTENCE_TYPE', 'SERVERPART_ID', 'STAFF_ID', 'STAFF_NAME'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `84.6 ms`
新 API 状态: `200`，耗时 `37.32 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 1 vs 5899 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 99 vs 99 |
| List 条数 | ❌ | 1 vs 99 |
| 首条字段集合 | ✅ | 字段一致，共 13 个 |
| 完整响应体 | ❌ | 发现 11 处差异 |

差异明细：
- Result_Data.List: 列表长度不一致 (1 vs 99)
- Result_Data.List[0].ANALYSISRULE_ID: 值不一致 ('' vs '1,39')
- Result_Data.List[0].DIALOG_CODE: 值不一致 ('' vs '1aade67c-c26a-40ed-a271-4c20afbc2159')
- Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024/10/30 17:59:17' vs '2026/1/26 11:22:19')
- Result_Data.List[0].SENTENCE_CONTENT: 值不一致 ('新桥' vs '新桥服务区5月份营收情况\n')
- Result_Data.List[0].SENTENCE_ID: 值不一致 (1 vs 6369)
- Result_Data.List[0].SENTENCE_RESULT: 值不一致 ('已标出位置' vs '为您查找【营收|营收】【5月：2026/5/1至2026/5/31】【新桥服务区】的相关数据\r\n{\r\n  "TriggerWords#关键字#": "营收|营收",\r\n  "AppointDays#指定时间段#": "5月",\r\n  "CurYear#年份#": 2026,\r\n  "ServerpartName#服务区#": "新桥服务区",\r\n  "StartDate#开始日期#": "2026/5/1",\r\n  "EndDate#结束日期#": "2026/5/31"\r\n}')
- Result_Data.List[0].SENTENCE_TYPE: 值不一致 (1 vs 2)
- Result_Data.List[0].STAFF_ID: 类型不一致 (int vs NoneType)，值为 2785 vs None
- Result_Data.List[0].STAFF_NAME: 值不一致 ('严琅杰' vs '新项目')
- Result_Data.TotalCount: 值不一致 (1 vs 5899)

原 API 状态: `200`，耗时 `94.8 ms`
新 API 状态: `200`，耗时 `54.78 ms`

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
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 1 vs 1 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].children[0].children: 列表长度不一致 (7 vs 6)
- Result_Data.List[0].children[0].children[0].children[0].node.BUSINESSPROJECT_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.BUSINESSPROJECT_IDS: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.BUSINESSPROJECT_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.BUSINESSTRADETYPE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.CALCULATE_SELFSHOP: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.EVALUATE_TYPES: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.PROFITCONTRIBUTE_DESC: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.PROFITCONTRIBUTE_PID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.PROFITCONTRIBUTE_STATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.RECORD_DATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SABFI_SCORE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SABFI_TYPE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SERVERPARTSHOP_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SERVERPARTSHOP_IDS: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SERVERPARTSHOP_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SERVERPART_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SERVERPART_IDS: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SERVERPART_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SPREGIONTYPE_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.SPREGIONTYPE_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.STAFF_ID: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.STAFF_NAME: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.STATISTICS_DATE: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.STATISTICS_DATE_End: 新 API 缺少该字段

原 API 状态: `200`，耗时 `271.95 ms`
新 API 状态: `200`，耗时 `61.74 ms`

### Analysis/GetVEHICLEAMOUNTDetail / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"VEHICLEAMOUNTId": 1}`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Analysis/GetVEHICLEAMOUNTDetail | 新 API: http://localhost:8080/EShangApiMain/Analysis/GetVEHICLEAMOUNTDetail |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['ADJUST_COUNT', 'CONSUMPTION_COEFFICIENT', 'PERCAPITA_INCOME', 'PROVINCE_NAME', 'PROVINCE_NAMES', 'RECORD_DATE', 'REVENUE_ACTAMOUNT', 'REVENUE_ADJAMOUNT', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SERVERPART_REGION', 'SERVERPART_REGIONS', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'VEHICLEAMOUNT_ID', 'VEHICLEAMOUNT_STATE', 'VEHICLE_ADJAMOUNT', 'VEHICLE_AMOUNT', 'VEHICLE_COUNT', 'VEHICLE_TOTALCOUNT', 'VEHICLE_TYPE', 'VEHICLE_TYPES'] vs ['ADJUST_COUNT', 'CONSUMPTION_COEFFICIENT', 'PERCAPITA_INCOME', 'PROVINCE_NAME', 'PROVINCE_NAMES', 'RECORD_DATE', 'REVENUE_ACTAMOUNT', 'REVENUE_ADJAMOUNT', 'SERVERPART_ID', 'SERVERPART_IDS', 'SERVERPART_NAME', 'SERVERPART_REGION', 'SERVERPART_REGIONS', 'STATISTICS_MONTH', 'STATISTICS_MONTH_End', 'STATISTICS_MONTH_Start', 'VEHICLEAMOUNT_ID', 'VEHICLEAMOUNT_STATE', 'VEHICLE_ADJAMOUNT', 'VEHICLE_AMOUNT', 'VEHICLE_COUNT', 'VEHICLE_TOTALCOUNT', 'VEHICLE_TYPE', 'VEHICLE_TYPES'] |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `78.58 ms`
新 API 状态: `200`，耗时 `17.11 ms`

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
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ❌ | 588 vs 64350 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 9 vs 9 |
| List 条数 | ✅ | 9 vs 9 |
| 首条字段集合 | ✅ | 字段一致，共 24 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].ADJUST_COUNT: 类型不一致 (float vs NoneType)，值为 1.5 vs None
- Result_Data.List[0].CONSUMPTION_COEFFICIENT: 类型不一致 (float vs NoneType)，值为 0.926901 vs None
- Result_Data.List[0].PERCAPITA_INCOME: 类型不一致 (float vs NoneType)，值为 30156.0 vs None
- Result_Data.List[0].PROVINCE_NAME: 值不一致 ('安徽省' vs '')
- Result_Data.List[0].RECORD_DATE: 值不一致 ('2024-11-15T13:58:28' vs '2025-01-25T12:08:33')
- Result_Data.List[0].REVENUE_ACTAMOUNT: 类型不一致 (NoneType vs float)，值为 None vs 145570.18
- Result_Data.List[0].REVENUE_ADJAMOUNT: 值不一致 (1557448.88 vs 0.0)
- Result_Data.List[0].SERVERPART_ID: 值不一致 (416 vs 943)
- Result_Data.List[0].SERVERPART_NAME: 值不一致 ('新桥服务区' vs '迎河服务区')
- Result_Data.List[0].STATISTICS_MONTH: 值不一致 ('2024/08' vs '2024/12')
- Result_Data.List[0].VEHICLEAMOUNT_ID: 值不一致 (2 vs 65308)
- Result_Data.List[0].VEHICLE_ADJAMOUNT: 类型不一致 (float vs NoneType)，值为 16.52 vs None
- Result_Data.List[0].VEHICLE_AMOUNT: 类型不一致 (float vs NoneType)，值为 15.02 vs None
- Result_Data.List[0].VEHICLE_COUNT: 类型不一致 (int vs NoneType)，值为 94289 vs None
- Result_Data.List[0].VEHICLE_TOTALCOUNT: 类型不一致 (NoneType vs int)，值为 None vs 0
- Result_Data.List[0].VEHICLE_TYPE: 值不一致 ('小型车' vs '')
- Result_Data.List[1].ADJUST_COUNT: 类型不一致 (NoneType vs float)，值为 None vs -0.32
- Result_Data.List[1].CONSUMPTION_COEFFICIENT: 类型不一致 (NoneType vs float)，值为 None vs 1.0
- Result_Data.List[1].PERCAPITA_INCOME: 类型不一致 (NoneType vs float)，值为 None vs 35100.0
- Result_Data.List[1].PROVINCE_NAME: 值不一致 ('' vs '其他省份')
- Result_Data.List[1].RECORD_DATE: 值不一致 ('2024-11-15T13:58:28' vs '2025-01-25T12:08:33')
- Result_Data.List[1].REVENUE_ACTAMOUNT: 类型不一致 (float vs NoneType)，值为 4797970.55 vs None
- Result_Data.List[1].REVENUE_ADJAMOUNT: 值不一致 (4907073.93 vs 1280.98)
- Result_Data.List[1].SERVERPART_ID: 值不一致 (416 vs 453)
- Result_Data.List[1].SERVERPART_NAME: 值不一致 ('新桥服务区' vs '砀山服务区')

原 API 状态: `200`，耗时 `200.95 ms`
新 API 状态: `200`，耗时 `41.67 ms`
