# 动态接口对比报告

- 生成时间: 2026-03-09 18:36:18
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\read_only_completeness_template.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `0/6` 个用例通过

## 用例明细

### BaseInfo/GetSERVERPARTList / empty-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ❌ | 查询失败未将对象引用设置到对象的实例。 vs 查询失败1 validation error for JsonListData
StaticsModel
  Input should be a valid dictionary [type=dict_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.9/v/dict_type |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ❌ | 发现 1 处差异 |

差异明细：
- Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '查询失败1 validation error for JsonListData\nStaticsModel\n  Input should be a valid dictionary [type=dict_type, input_value=None, input_type=NoneType]\n    For further information visit https://errors.pydantic.dev/2.9/v/dict_type')

原 API 状态: `200`，耗时 `46.47 ms`
新 API 状态: `200`，耗时 `2298.5 ms`

### BaseInfo/GetSERVERPARTList / search-model

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"PageIndex": 1, "PageSize": 999, "SearchParameter": {"ProvinceCode": "340000", "SERVERPART_ID": 416, "SERVERPART_IDS": 416}}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败[CODE:-2111]第1 行附近出现错误:
无效的列名[PROVINCECODE] |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 999, 'TotalCount': 1, 'List': [{'SERVERPART_ID': 416, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '新桥服务区', 'SERVERPART_ADDRESS': '合肥市经开区高刘社区', 'SERVERPART_INDEX': 1001, 'EXPRESSWAY_NAME': '沪陕高速|G40', 'SELLERCOUNT': 5000, 'SERVERPART_AREA': 13462.0, 'SERVERPART_X': 116.893886, 'SERVERPART_Y': 31.918931, 'SERVERPART_TEL': '18956056157', 'SERVERPART_INFO': '新桥服务区于2020年改造升级，内部环境更加现代、主题特色更加突出、服务内容更加多元。目前，餐厅提供都市连锁快餐，含蒸式套餐、地方特色菜等各式菜品达50余种，有麦当劳、猫屎咖啡、老乡鸡、刘鸿盛等知名品牌进驻；全新的万佳生活馆24小时营业，有食品、饮料、水果、烟酒、生活用品、安徽土特产及工艺品等2000余种商品。全区覆盖免费WIFI，方便司乘处理商务和网上冲浪。\r\n       2014年7月，建成国内首个服务区候机楼，实现路空无缝对接，开创交通运输新方式。候机楼“一站式”服务与服务区基本服务有机结合，更加方便了司乘出行。设有值机服务中心，可实现订票、登机牌办理、航空信息咨询、候机等一站式业务，还专门为登机旅客提供标间客房和VIP旅客休息区、茶点供应、报刊阅览等服务。候机楼每天有10趟班车往返于服务区和机场之间，从服务区乘车前往新桥机场仅需15分钟，比到合肥市区再转车前往机场节省两个多小时。', 'PROVINCE_CODE': 3544, 'CITY_CODE': None, 'COUNTY_CODE': 2, 'SERVERPART_CODE': '341003', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 3576, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': 1000, 'DAYINCAR': 5518.0, 'HKBL': '', 'STARTDATE': '2013-06-06T00:00:00', 'OWNEDCOMPANY': '安徽省驿达高速公路服务区经营管理有限公司', 'FLOORAREA': 96313.0, 'BUSINESSAREA': None, 'SHAREAREA': 68538.0, 'TOTALPARKING': None, 'MANAGERCOMPANY': '六安北管理中心', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '安徽省', 'SPREGIONTYPE_ID': 72, 'SPREGIONTYPE_NAME': '皖中管理中心', 'SPREGIONTYPE_INDEX': 5, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 8040, 'STAFF_NAME': '何咏梅', 'OPERATE_DATE': '2025-05-28T11:31:45', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 249, 'OWNERUNIT_NAME': '安徽交控驿达服务开发集团有限公司', 'RtServerPart': None, 'ServerPartInfo': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-2111]第1 行附近出现错误:\n无效的列名[PROVINCECODE]')

原 API 状态: `200`，耗时 `312.11 ms`
新 API 状态: `200`，耗时 `3778.99 ms`

### BaseInfo/GetSERVERPARTList / flat-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `{"ProvinceCode": "340000", "SERVERPART_ID": 416, "SERVERPART_IDS": 416}`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetSERVERPARTList | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetSERVERPARTList |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败1 validation error for JsonListData
StaticsModel
  Input should be a valid dictionary [type=dict_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.9/v/dict_type |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- Result_Code: 值不一致 (100 vs 999)
- Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 0, 'PageSize': 0, 'TotalCount': 1168, 'List': [{'SERVERPART_ID': 206, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '水洋湾服务区', 'SERVERPART_ADDRESS': '贵州省遵义市播州区水洋湾服务区', 'SERVERPART_INDEX': 4050, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 106.63119, 'SERVERPART_Y': 27.582378, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 3250, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '521405', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 3284, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': 213, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': 40, 'SPREGIONTYPE_NAME': '北部区域', 'SPREGIONTYPE_INDEX': 40, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 714, 'STAFF_NAME': '李博文', 'OPERATE_DATE': '2020-08-27T18:15:16', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 351, 'OWNERUNIT_NAME': '贵州高投服务区管理有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 207, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '仁怀服务区', 'SERVERPART_ADDRESS': '贵州省遵义市仁怀市仁怀服务区', 'SERVERPART_INDEX': 4060, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 106.381816, 'SERVERPART_Y': 27.76408, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 3250, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '521406', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 3285, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': 213, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': 40, 'SPREGIONTYPE_NAME': '北部区域', 'SPREGIONTYPE_INDEX': 40, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 714, 'STAFF_NAME': '李博文', 'OPERATE_DATE': '2020-08-27T18:18:41', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 351, 'OWNERUNIT_NAME': '贵州高投服务区管理有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 214, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '贵州高投', 'SERVERPART_ADDRESS': '贵阳市云岩区三桥北路229', 'SERVERPART_INDEX': 10, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 106.673143, 'SERVERPART_Y': 26.59024, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 3250, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '521001', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 3292, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 4000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': None, 'STAFF_NAME': '', 'OPERATE_DATE': '2020-08-28T17:27:19', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 351, 'OWNERUNIT_NAME': '贵州高投服务区管理有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 71, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '杨店服务区', 'SERVERPART_ADDRESS': '甘肃兰州', 'SERVERPART_INDEX': 9004, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': None, 'SERVERPART_Y': None, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 8832, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '629004', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 5, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': 1000, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': 87, 'SPREGIONTYPE_NAME': '通美公司', 'SPREGIONTYPE_INDEX': 120, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'OPERATE_DATE': '2021-11-03T21:57:54', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 8, 'OWNERUNIT_NAME': '甘肃华运高速公路服务区管理有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 72, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '杨杨商贸', 'SERVERPART_ADDRESS': '甘肃兰州', 'SERVERPART_INDEX': None, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': None, 'SERVERPART_Y': None, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 8832, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '629005', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 17423, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': 1000.0, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': None, 'PROVINCE_NAME': '3000', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '13', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '', 'STAFF_ID': None, 'STAFF_NAME': '', 'OPERATE_DATE': None, 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 8, 'OWNERUNIT_NAME': '甘肃华运高速公路服务区管理有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 3974, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '黄堡服务区', 'SERVERPART_ADDRESS': '襄阳市保康县加油站', 'SERVERPART_INDEX': 4090, 'EXPRESSWAY_NAME': '谷竹高速', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 111.345672, 'SERVERPART_Y': 31.820342, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 9352, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '420092', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 576, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '湖北省交投投资有限公司', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 2, 'STAFF_NAME': '系统管理员', 'OPERATE_DATE': '2019-11-26T14:14:06', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 353, 'OWNERUNIT_NAME': '湖北交投实业发展有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 3975, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '南漳服务区', 'SERVERPART_ADDRESS': '襄阳市南漳县南漳服务区', 'SERVERPART_INDEX': 4070, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 111.903823, 'SERVERPART_Y': 31.812604, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 9352, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '420093', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 577, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '湖北省交投投资有限公司', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '麻竹高速', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 2, 'STAFF_NAME': '系统管理员', 'OPERATE_DATE': '2019-11-26T14:28:24', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 353, 'OWNERUNIT_NAME': '湖北交投实业发展有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 3977, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '溢水服务区', 'SERVERPART_ADDRESS': '十堰市竹山县溢水服务区', 'SERVERPART_INDEX': 4060, 'EXPRESSWAY_NAME': '', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 110.103141, 'SERVERPART_Y': 32.260004, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 9352, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '420094', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 578, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '湖北省交投投资有限公司', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '谷竹高速', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'OPERATE_DATE': '2019-05-21T14:03:31', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 353, 'OWNERUNIT_NAME': '湖北交投实业发展有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 3978, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '竹溪服务区', 'SERVERPART_ADDRESS': '十堰市竹溪县竹溪服务区', 'SERVERPART_INDEX': 4050, 'EXPRESSWAY_NAME': '麻安高速', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 109.579509, 'SERVERPART_Y': 32.329709, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 9352, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '420095', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 579, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '湖北省交投投资有限公司', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 1, 'STAFF_NAME': '系统开发者', 'OPERATE_DATE': '2019-05-21T14:03:44', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 353, 'OWNERUNIT_NAME': '湖北交投实业发展有限公司', 'RtServerPart': None, 'ServerPartInfo': None}, {'SERVERPART_ID': 3979, 'SERVERPART_IDS': None, 'SERVERPART_NAME': '谷城服务区', 'SERVERPART_ADDRESS': '襄阳市谷城县谷城服务区', 'SERVERPART_INDEX': 4040, 'EXPRESSWAY_NAME': '谷竹高速', 'SELLERCOUNT': None, 'SERVERPART_AREA': None, 'SERVERPART_X': 111.446523, 'SERVERPART_Y': 32.271583, 'SERVERPART_TEL': '', 'SERVERPART_INFO': '', 'PROVINCE_CODE': 9352, 'CITY_CODE': None, 'COUNTY_CODE': None, 'SERVERPART_CODE': '420096', 'SERVERPART_CODES': None, 'FIELDENUM_ID': 580, 'SERVERPART_IPADDRESS': '', 'SERVERPART_TYPE': None, 'DAYINCAR': None, 'HKBL': '', 'STARTDATE': None, 'OWNEDCOMPANY': '湖北省交投投资有限公司', 'FLOORAREA': None, 'BUSINESSAREA': None, 'SHAREAREA': None, 'TOTALPARKING': None, 'MANAGERCOMPANY': '', 'SHORTNAME': '', 'REGIONTYPE_ID': None, 'STATISTIC_TYPE': 1000, 'PROVINCE_NAME': '', 'SPREGIONTYPE_ID': None, 'SPREGIONTYPE_NAME': '', 'SPREGIONTYPE_INDEX': None, 'REGIONTYPE_NAME': '', 'STATISTICS_TYPE': '1000', 'STAFF_ID': 2, 'STAFF_NAME': '系统管理员', 'OPERATE_DATE': '2019-11-26T14:05:40', 'SERVERPART_DESC': '', 'OWNERUNIT_ID': 353, 'OWNERUNIT_NAME': '湖北交投实业发展有限公司', 'RtServerPart': None, 'ServerPartInfo': None}]} vs None
- Result_Desc: 值不一致 ('查询成功' vs '查询失败1 validation error for JsonListData\nStaticsModel\n  Input should be a valid dictionary [type=dict_type, input_value=None, input_type=NoneType]\n    For further information visit https://errors.pydantic.dev/2.9/v/dict_type')

原 API 状态: `200`，耗时 `414.35 ms`
新 API 状态: `200`，耗时 `283.15 ms`

### BaseInfo/GetServerpartDDL / default-type

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"ServerpartType": "1000"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartDDL | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartDDL |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'int' object has no attribute 'strip' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- <root>.Result_Data: 新 API 缺少该字段
- Result_Code: 值不一致 (100 vs 999)
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'int' object has no attribute 'strip'")

原 API 状态: `200`，耗时 `332.18 ms`
新 API 状态: `200`，耗时 `5.04 ms`

### BaseInfo/GetServerpartDDL / service-area-416

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"SERVERPART_ID": 416}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartDDL | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartDDL |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'int' object has no attribute 'strip' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- <root>.Result_Data: 新 API 缺少该字段
- Result_Code: 值不一致 (100 vs 999)
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'int' object has no attribute 'strip'")

原 API 状态: `200`，耗时 `297.51 ms`
新 API 状态: `200`，耗时 `4.05 ms`

### BaseInfo/GetServerpartDDL / empty-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/BaseInfo/GetServerpartDDL | 新 API: http://localhost:8080/EShangApiMain/BaseInfo/GetServerpartDDL |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ❌ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Desc'] |
| Result_Code | ❌ | 100 vs 999 |
| Result_Desc | ❌ | 查询成功 vs 查询失败'int' object has no attribute 'strip' |
| Result_Data 类型 | ❌ | dict vs NoneType |
| 完整响应体 | ❌ | 发现 3 处差异 |

差异明细：
- <root>.Result_Data: 新 API 缺少该字段
- Result_Code: 值不一致 (100 vs 999)
- Result_Desc: 值不一致 ('查询成功' vs "查询失败'int' object has no attribute 'strip'")

原 API 状态: `200`，耗时 `227.01 ms`
新 API 状态: `200`，耗时 `5.56 ms`
