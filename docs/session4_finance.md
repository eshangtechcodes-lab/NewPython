# 动态接口对比报告

- 生成时间: 2026-03-10 23:34:07
- Manifest: `E:\workfile\JAVA\NewAPI\scripts\manifests\_tmp_finance.json`
- 原 API: `http://192.168.1.99:8900/EShangApiMain`
- 新 API: `http://localhost:8080/EShangApiMain`
- 默认 Header: `{"ProvinceCode": "340000"}`
- 总结果: `PASS 1 / FAIL 1 / SKIP 0 / TOTAL 2`

## 用例明细

### Finance/GetAHJKtoken / default-body

- 方法: `POST`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `null`
- JSON: `null`
- 结果: `PASS`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetAHJKtoken | 新 API: http://localhost:8080/EShangApiMain/Finance/GetAHJKtoken |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 999 vs 999 |
| Result_Desc | ✅ | 获取失败未将对象引用设置到对象的实例。 vs 获取失败未将对象引用设置到对象的实例。 |
| Result_Data 类型 | ✅ | NoneType vs NoneType |
| 完整响应体 | ✅ | 完全一致 |

原 API 状态: `200`，耗时 `41.38 ms`
新 API 状态: `200`，耗时 `2034.94 ms`

### Finance/GetAccountCompare / default-query

- 方法: `GET`
- Headers: `{"ProvinceCode": "340000"}`
- Query: `{"CompareEndDate": "2024-12-31", "CompareStartDate": "2024-12-01", "EndDate": "2025-12-31", "ServerpartId": 416, "StartDate": "2025-12-01"}`
- JSON: `null`
- 结果: `FAIL`

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 接口可达 | ✅ | 原 API: http://192.168.1.99:8900/EShangApiMain/Finance/GetAccountCompare | 新 API: http://localhost:8080/EShangApiMain/Finance/GetAccountCompare |
| HTTP 状态码 | ✅ | 200 vs 200 |
| 响应可解析 JSON | ✅ | 原 API: True | 新 API: True |
| 顶层字段 | ✅ | ['Result_Code', 'Result_Data', 'Result_Desc'] vs ['Result_Code', 'Result_Data', 'Result_Desc'] |
| Result_Code | ✅ | 100 vs 100 |
| Result_Desc | ✅ | 查询成功 vs 查询成功 |
| Result_Data 类型 | ✅ | dict vs dict |
| Result_Data 字段 | ✅ | ['List', 'PageIndex', 'PageSize', 'TotalCount'] vs ['List', 'PageIndex', 'PageSize', 'TotalCount'] |
| TotalCount | ✅ | 1 vs 1 |
| PageIndex | ✅ | 1 vs 1 |
| PageSize | ✅ | 10 vs 10 |
| List 条数 | ✅ | 1 vs 1 |
| 首条字段集合 | ✅ | 字段一致，共 2 个 |
| 完整响应体 | ❌ | 发现 25 处差异 |

差异明细：
- Result_Data.List[0].children[0].children[0].children: 列表长度不一致 (14 vs 8)
- Result_Data.List[0].children[0].children[0].children[0].node.Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.Brand_Id: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.Brand_Name: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[0].node.ConfirmIncome.compareData: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.ConfirmIncome.curIntro: 值不一致 ('保底收入(14025.33)>提成收入(6976.65)=保底收入(14025.33)' vs '保底收入(14025.33)>提成收入(0)=保底收入(14025.33)')
- Result_Data.List[0].children[0].children[0].children[0].node.GuaranteeIncome.compareData: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.GuaranteeIncome.curIntro: 值不一致 ('第1期保底租金(180000)/周期天数(365)/税(1 + 9%)*执行天数(31)' vs '第1期保底租金(180000.0)/周期天数(365)/税(1 + 9.0%)*执行天数(31)')
- Result_Data.List[0].children[0].children[0].children[0].node.GuaranteePrice.compareData: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.GuaranteePrice.curIntro: 值不一致 ('第1期保底租金(180000)' vs '第1期保底租金(180000.0)')
- Result_Data.List[0].children[0].children[0].children[0].node.RevenueAmount.compareData: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.RevenueAmount.curData: 类型不一致 (float vs int)，值为 50697.0 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.RoyaltyIncome.compareData: 类型不一致 (float vs int)，值为 0.0 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.RoyaltyIncome.curData: 类型不一致 (float vs int)，值为 6976.65 vs 0
- Result_Data.List[0].children[0].children[0].children[0].node.RoyaltyIncome.curIntro: 类型不一致 (str vs NoneType)，值为 '营业额(50697)*提成比例(15%)/税(1 + 9%)' vs None
- Result_Data.List[0].children[0].children[0].children[0].node.ServerpartShopId: 值不一致 ('5627,5626' vs '5626,5627')
- Result_Data.List[0].children[0].children[0].children[1].node.Brand_ICO: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[1].node.Brand_Id: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[1].node.Brand_Name: 新 API 缺少该字段
- Result_Data.List[0].children[0].children[0].children[1].node.BusinessProjectId: 值不一致 ('1508' vs '1506')
- Result_Data.List[0].children[0].children[0].children[1].node.ConfirmIncome.compareData: 值不一致 (23311.69 vs 97909.47)
- Result_Data.List[0].children[0].children[0].children[1].node.ConfirmIncome.compareIntro: 值不一致 ('保底收入(23311.69)>提成收入(14525.22)=保底收入(23311.69)' vs '保底收入(97909.47)>提成收入(0)=保底收入(97909.47)')
- Result_Data.List[0].children[0].children[0].children[1].node.ConfirmIncome.curData: 值不一致 (23375.55 vs 98177.62)
- Result_Data.List[0].children[0].children[0].children[1].node.ConfirmIncome.curIntro: 值不一致 ('保底收入(23375.55)>提成收入(15521.50)=保底收入(23375.55)' vs '保底收入(98177.62)>提成收入(0)=保底收入(98177.62)')
- Result_Data.List[0].children[0].children[0].children[1].node.GuaranteeIncome.compareData: 值不一致 (23311.69 vs 97909.47)

原 API 状态: `200`，耗时 `346.92 ms`
新 API 状态: `200`，耗时 `203.14 ms`
