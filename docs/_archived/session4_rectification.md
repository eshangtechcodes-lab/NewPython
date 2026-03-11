# 全量 API 对比整改清单

- 生成时间: 2026-03-10 18:04:02
- 数据来源: `docs/session4_full.json`
- 总计: **PASS 23 / FAIL 306 / TOTAL 329**

## 1. 已通过接口 (23 个)

- `BaseInfo/BindingMerchantTree` / GET `default-query`
- `BaseInfo/BindingOwnerUnitDDL` / GET `default-query`
- `BaseInfo/GetAutoStatisticsTreeList` / GET `default-query`
- `BaseInfo/GetBusinessTradeList` / POST `default-body`
- `BaseInfo/GetNestingOwnerUnitList` / GET `default-query`
- `BaseInfo/GetOWNERUNITList` / POST `default-body`
- `BaseInfo/GetPROPERTYASSETSLOGList` / POST `default-body`
- `BaseInfo/GetServerpartDDL` / GET `service-area-416`
- `BaseInfo/GetServerpartShopDDL` / GET `default-query`
- `BaseInfo/GetServerpartTree` / GET `default-query`
- `BaseInfo/GetShopShortNames` / GET `default-query`
- `BusinessProject/GetSHOPROYALTYDETAILDetail` / GET `default-query`
- `BusinessProject/GetSHOPROYALTYDETAILList` / POST `default-body`
- `BusinessProject/GetShopRoyaltyDetail` / GET `default-query`
- `BusinessProject/GetShopRoyaltyList` / POST `default-body`
- `Contract/GetContractExpiredInfo` / GET `default-query`
- `Contract/GetProjectSummaryInfo` / GET `default-query`
- `Contract/GetRTRegisterCompactDetail` / GET `default-query`
- `Contract/GetRTRegisterCompactList` / POST `default-body`
- `Merchants/GetCoopMerchantsDetail` / GET `default-query`
- `Merchants/GetCoopMerchantsLinkerDetail` / GET `default-query`
- `Merchants/GetCoopMerchantsLinkerList` / POST `default-body`
- `Merchants/GetCoopMerchantsTypeList` / POST `default-body`

## 2. 原接口 (C#) 报错 (75 个)

> 这些接口 C# 端返回 404/500 等错误，说明原 API 也不可用或未部署。
> 建议：Python 端可暂时跳过或标记为 SKIP。

### Analysis

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Analysis/GetPREFERRED_RATINGDetail` | GET | 404 | 200 |

### Audit

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Audit/GetAuditDetils` | POST | 404 | 200 |
| `Audit/GetAuditList` | GET | 404 | 405 |
| `Audit/GetAuditTasksDetailList` | POST | 404 | 200 |
| `Audit/GetAuditTasksReport` | POST | 404 | 200 |
| `Audit/GetSpecialBehaviorReport` | POST | 404 | 200 |
| `Audit/GetYSABNORMALITYDETAILList` | POST | 404 | 200 |
| `Audit/GetYsabnormalityReport` | POST | 404 | 200 |

### BigData

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `BigData/GetBAYONETDAILY_AHDetail` | GET | 404 | 200 |
| `BigData/GetUreaMasterList` | POST | 404 | 200 |

### Budget

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Budget/GetBudgetProjectReportOfMonth` | GET | 404 | 200 |
| `Budget/GetbudgetProjectReport` | GET | 404 | 200 |
| `Budget/GetbudgetProjectReportDynamic` | GET | 404 | 200 |
| `Budget/GetbudgetProjectReportIn` | GET | 404 | 200 |
| `Budget/GetbudgetProjectReportInDynamic` | GET | 404 | 200 |
| `Budget/GetbudgetProjectReportOut` | GET | 404 | 200 |
| `Budget/GetbudgetProjectReportOutDynamic` | GET | 404 | 200 |

### BusinessProject

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `BusinessProject/GetCONTRACT_SYNDetail` | GET | 404 | 200 |
| `BusinessProject/GetCONTRACT_SYNList` | POST | 404 | 200 |
| `BusinessProject/GetMonthSummaryList` | GET | 404 | 200 |
| `BusinessProject/GetPaymentConfirmList` | POST | 500 | 200 |

### ContractSyn

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `ContractSyn/GetContractSynDetail` | GET | 404 | 200 |
| `ContractSyn/GetContractSynList` | POST | 404 | 200 |

### Finance

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Finance/GetATTACHMENTDetail` | GET | 404 | 200 |
| `Finance/GetATTACHMENTList` | GET | 404 | 200 |
| `Finance/GetPeriodSupplementList` | GET | 404 | None |
| `Finance/GetProjectExpenseList` | GET | 404 | None |
| `Finance/GetRevenueSplitSummary` | GET | 404 | None |

### Merchants

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Merchants/GetRTCoopMerchantsList` | GET | 404 | 200 |
| `Merchants/GetTradeBrandMerchantsList` | GET | 415 | 200 |

### MobilePay

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `MobilePay/GetChinaUmsSubAccountDetail` | POST | 404 | 200 |
| `MobilePay/GetChinaUmsSubAccountSummary` | POST | 404 | 200 |
| `MobilePay/GetChinaUmsSubMaster` | POST | 404 | 200 |
| `MobilePay/GetChinaUmsSubSummary` | POST | 404 | 200 |
| `MobilePay/GetKwyRoyalty` | GET | 404 | 200 |
| `MobilePay/GetKwyRoyaltyForAll` | GET | 404 | 200 |
| `MobilePay/GetKwyRoyaltyRate` | POST | 404 | 200 |
| `MobilePay/GetRoyaltyRecordList` | POST | 500 | 200 |

### Picture

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Picture/GetPictureList` | GET | 404 | 405 |

### Revenue

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Revenue/GetBUSINESSANALYSISDetail` | GET | 404 | 200 |
| `Revenue/GetBankAccountList` | GET | 404 | 200 |
| `Revenue/GetBusinessAnalysisReport` | POST | 404 | 200 |
| `Revenue/GetHisCommoditySaleList` | POST | 404 | 200 |
| `Revenue/GetMonthCompare` | POST | 404 | 200 |
| `Revenue/GetPERSONSELLDetail` | GET | 404 | 200 |
| `Revenue/GetRevenuePushList` | POST | 404 | 200 |
| `Revenue/GetRevenueQOQ` | POST | 404 | 200 |
| `Revenue/GetRevenueQOQByDate` | POST | 404 | 200 |
| `Revenue/GetRevenueReportByBIZPSPLITMONTH` | GET | 404 | 200 |
| `Revenue/GetRevenueYOYQOQByDate` | POST | 404 | 200 |
| `Revenue/GetSellMasterCompareList` | POST | 404 | 200 |
| `Revenue/GetTransactionCustomer` | POST | 404 | 200 |
| `Revenue/GetTransactionCustomerByDate` | POST | 404 | 200 |
| `Revenue/GetYSSellDetailsList` | POST | 500 | 200 |
| `Revenue/GetYSSellMasterList` | POST | 500 | 200 |

### Sales

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Sales/GetCOMMODITYSALEDetail` | GET | 404 | 200 |
| `Sales/GetCommoditySaleSummary` | POST | 404 | 200 |
| `Sales/GetCommodityTypeHistory` | POST | 404 | 200 |
| `Sales/GetCommodityTypeSummary` | POST | 404 | 200 |
| `Sales/GetEndaccountSaleInfo` | GET | 404 | 405 |

### Supplier

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Supplier/GetQUALIFICATION_HISDetail` | GET | 404 | 200 |
| `Supplier/GetQualificationDetail` | GET | 404 | 200 |
| `Supplier/GetQualificationList` | POST | 500 | 200 |
| `Supplier/GetSupplierDetail` | GET | 404 | 200 |
| `Supplier/GetSupplierList` | POST | 500 | 200 |
| `Supplier/GetSupplierTreeList` | POST | 500 | 200 |

### Verification

| 接口 | 方法 | C# HTTP 状态 | Python HTTP 状态 |
|---|---|---|---|
| `Verification/GetCommoditySaleList` | GET | 404 | 200 |
| `Verification/GetDataVerificationList` | GET | 404 | 200 |
| `Verification/GetENDACCOUNTModel` | GET | 404 | 200 |
| `Verification/GetEndAccountData` | GET | 404 | 200 |
| `Verification/GetEndaccountDetail` | GET | 404 | 405 |
| `Verification/GetEndaccountHisList` | GET | None | 405 |
| `Verification/GetEndaccountList` | GET | None | 405 |
| `Verification/GetEndaccountSupplement` | GET | 404 | 200 |
| `Verification/GetMobilePayDataList` | GET | 404 | 200 |

## 3. 空参数导致超时 (23 个)

> 这些接口因测试用例未提供必要参数，导致 Python 端超时或无法响应。
> 建议：补充 case_library 中的参数后重新测试。

| 接口 | 方法 | 说明 |
|---|---|---|
| `Finance/GetAccountReached` | GET | default-query |
| `Finance/GetAnnualAccountList` | GET | default-query |
| `Finance/GetBankAccountAnalyseList` | GET | default-query |
| `Finance/GetBankAccountAnalyseTreeList` | GET | default-query |
| `Finance/GetContractExcuteAnalysis` | GET | default-query |
| `Finance/GetContractMerchant` | GET | default-query |
| `Finance/GetMonthAccountDiff` | GET | default-query |
| `Finance/GetMonthAccountProinst` | POST | default-body |
| `Finance/GetProjectMerchantSummary` | GET | default-query |
| `Finance/GetProjectPeriodAccount` | GET | default-query |
| `Finance/GetProjectPeriodIncome` | GET | default-query |
| `Finance/GetProjectShopIncome` | GET | default-query |
| `Finance/GetProjectSplitSummary` | GET | default-query |
| `Finance/GetProjectSummary` | GET | default-query |
| `Finance/GetReconciliation` | GET | default-query |
| `Finance/GetRevenueRecognition` | GET | default-query |
| `Finance/GetRoyaltyDateSumReport` | GET | default-query |
| `Finance/GetRoyaltyReport` | GET | default-query |
| `Finance/GetShopExpense` | GET | default-query |
| `Invoice/GetBILLDETAILDetail` | GET | default-query |
| `Invoice/GetBILLDETAILList` | POST | default-body |
| `Invoice/GetBILLDetail` | GET | default-query |
| `Invoice/GetBILLList` | POST | default-body |

## 4. 按模块分组的 FAIL 接口

### Analysis (30 个 FAIL)

#### DatabaseHelper缺少方法 (20)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Analysis/GetANALYSISINSDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ANALYSISINS_ID': 1805, 'ANALYSISINS_PID': None, 'STATISTICS_DATE': None, 'ANA...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetANALYSISINSList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'ANALYSISINS_ID': 18...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetANALYSISRULEDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ANALYSISRULE_ID': 19, 'ANALYSISRULE_IDS': None, 'TRIGGER_WORDS': '客单均价|客单', '...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetANALYSISRULEList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'ANALYSISRULE_ID': 1...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetASSETSPROFITSDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'Start_DATE': None, 'End_DATE': None, 'PROPERTYASSETS_CODE': None, 'PROPERTYAS...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetASSETSPROFITSList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 537, 'List': [{'Start_DATE': None...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetINVESTMENTANALYSISDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'INVESTMENTANALYSIS_ID': 1, 'SERVERPART_ID': 417, 'SERVERPART_NAME': '肥东服务区', ...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetINVESTMENTANALYSISList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 632, 'List': [{'INVESTMENTANALYSI...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetINVESTMENTDETAILDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'INVESTMENTDETAIL_ID': 1, 'INVESTMENTANALYSIS_ID': 23, 'INVESTMENTANALYSIS_IDS...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetINVESTMENTDETAILList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 7477, 'List': [{'INVESTMENTDETAIL...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetPERIODMONTHPROFITDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PERIODMONTHPROFIT_ID': None, 'STATISTICS_MONTH': None, 'STATISTICS_MONTH_Star...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetPERIODMONTHPROFITList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'PERIODMONTHPROFIT_I...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetPROFITCONTRIBUTEDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PROFITCONTRIBUTE_ID': 1, 'PROFITCONTRIBUTE_PID': -1, 'STATISTICS_DATE': '2024...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetPROFITCONTRIBUTEList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 3003, 'List': [{'PROFITCONTRIBUTE...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetPROMPTDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PROMPT_ID': 5, 'PROMPT_TYPE': 1000, 'PROMPT_TYPES': None, 'PROMPT_CONTENT': '...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetPROMPTList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 3, 'List': [{'PROMPT_ID': 5, 'PRO...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetSENTENCEDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'SENTENCE_ID': 1, 'SENTENCE_TYPE': 1, 'SENTENCE_CONTENT': '新桥', 'SENTENCE_RESU...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetSENTENCEList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 99, 'TotalCount': 1, 'List': [{'SENTENCE_ID': 1, '...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetVEHICLEAMOUNTDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'VEHICLEAMOUNT_ID': 1, 'STATISTICS_MONTH': '2024/08', 'STATISTICS_MONTH_Start'...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Analysis/GetVEHICLEAMOUNTList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 588, 'List': [{'VEHICLEAMOUNT_ID'...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |

#### Result_Desc措辞差异 (9)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Analysis/GetASSETSPROFITSBusinessTreeList` | POST | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.PageSize: 值不一致 (999 vs 10); Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetASSETSPROFITSDateDetailList` | GET | Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetASSETSPROFITSTreeList` | POST | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.PageSize: 值不一致 (9 vs 10); Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetAssetsLossProfitList` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'node': None, 'children': None} vs []; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetInvestmentReport` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 7, 'TotalCount': 7, 'List': [{'SPREGIONTYPE_ID': 72, '...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetNestingIAReport` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 7, 'TotalCount': 7, 'List': [{'node': {'SPREGIONTYPE_I...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetPeriodMonthlyList` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'BUSINESSPROJEC...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetRevenueEstimateList` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'SPREGIONTYPE_I...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Analysis/GetShopSABFIList` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'SPREGIONTYPE_I...; Result_Desc: 值不一致 ('查询成功' vs '成功') |

#### 字段差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Analysis/GetPREFERRED_RATINGList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |

### Audit (10 个 FAIL)

#### HTTP方法/参数校验错误 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Audit/GetAbnormalRateReport` | GET | HTTP 200/405; <root>.Result_Code: 新 API 缺少该字段; <root>.Result_Data: 新 API 缺少该字段; <root>.Result_Desc: 新 API 缺少该字段; ...共4处差异 |
| `Audit/GetCheckAccountReport` | GET | HTTP 200/405; <root>.Result_Code: 新 API 缺少该字段; <root>.Result_Data: 新 API 缺少该字段; <root>.Result_Desc: 新 API 缺少该字段; ...共4处差异 |

#### Result_Desc措辞差异 (8)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Audit/GetABNORMALAUDITList` | POST | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 637, 'List': [{'ABNORMALAUDIT_ID'...; ...共4处差异 |
| `Audit/GetAUDITTASKSDetail` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'AUDITTASKS_ID': 3675, 'SERVERPART_ID': 477, 'SERVERPARTCODE': '340606', 'SERV...; ...共4处差异 |
| `Audit/GetAUDITTASKSList` | POST | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'AUDITTASKS_ID': 367...; ...共4处差异 |
| `Audit/GetAbnormalAuditDetail` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ABNORMALAUDIT_ID': 1, 'ENDACCOUNT_ID': None, 'PROVINCE_CODE': 3544, 'SPREGION...; ...共4处差异 |
| `Audit/GetCHECKACCOUNTDetail` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'CHECKACCOUNT_ID': None, 'SPREGIONTYPE_IDS': None, 'SERVERPART_ID': None, 'SER...; ...共4处差异 |
| `Audit/GetCHECKACCOUNTList` | POST | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 9420, 'List': [{'CHECKACCOUNT_ID'...; ...共4处差异 |
| `Audit/GetYSABNORMALITYDetail` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ABNORMALITY_CODE': None, 'SERVERPART_ID': None, 'SERVERPART_IDS': None, 'SERV...; ...共4处差异 |
| `Audit/GetYSABNORMALITYList` | POST | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 0, 'List': []} vs None; ...共4处差异 |

### BaseInfo (44 个 FAIL)

#### 值差异 (6)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BaseInfo/GetAssetsRevenueAmount` | GET | Result_Data.List: 列表长度不一致 (1 vs 0); Result_Data.TotalCount: 值不一致 (1 vs 0) |
| `BaseInfo/GetNestingCOMMODITYTYPEList` | GET | Result_Data.List: 列表长度不一致 (10 vs 0); Result_Data.PageSize: 值不一致 (10 vs 0); Result_Data.TotalCount: 值不一致 (10 vs 0) |
| `BaseInfo/GetNestingCOMMODITYTYPETree` | GET | Result_Data.List: 列表长度不一致 (10 vs 0); Result_Data.PageSize: 值不一致 (10 vs 0); Result_Data.TotalCount: 值不一致 (10 vs 0) |
| `BaseInfo/GetServerpartShopList` | POST | Result_Data.List: 列表长度不一致 (69 vs 0); Result_Data.TotalCount: 值不一致 (69 vs 0) |
| `BaseInfo/GetServerpartUDTypeTree` | GET | Result_Data.List[0].children[0].children: 列表长度不一致 (99 vs 114); Result_Data.List[0].children[0].children[0].node.key: 值不一致 ('2-9475' vs '2-1019'); Result_Data.List[0].children[0].children[0].node.label... |
| `BaseInfo/GetShopReceivables` | GET | Result_Data.List[0].PROJECT_ENDDATE: 值不一致 ('2024/1/31' vs '2024-01-31T00:00:00'); Result_Data.List[0].PROJECT_STARTDATE: 值不一致 ('2021/2/1' vs '2021-02-01T00:00:00'); Result_Data.List[1].PROJECT_ENDDATE... |

#### 字段差异 (31)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BaseInfo/GetAUTOSTATISTICSDetail` | GET | Result_Data.INELASTIC_DEMAND: 新 API 缺少该字段; Result_Data.AUTOSTATISTICS_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.AUTOSTATISTICS_ICO: 值不一致 ('https://user.eshangtech.com/UploadImageDir/Pic... |
| `BaseInfo/GetBrandDetail` | GET | Result_Data.BUSINESSTRADE_NAME: 新 API 缺少该字段; Result_Data.MerchantID: 新 API 缺少该字段; Result_Data.MerchantID_Encrypt: 新 API 缺少该字段; ...共16处差异 |
| `BaseInfo/GetBrandList` | POST | Result_Data.List[0].MerchantID_Encrypt: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; Result_Data.List[0].SPREGIONTYPE_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetBusinessTradeEnum` | GET | Result_Data.List[0].children[0].node.desc: 新 API 缺少该字段; Result_Data.List[0].children[1].node.desc: 新 API 缺少该字段; Result_Data.List[0].children[2].node.desc: 新 API 缺少该字段; ...共7处差异 |
| `BaseInfo/GetCASHWORKERDetail` | GET | Result_Data.OPERATE_DATE_End: 新 API 缺少该字段; Result_Data.OPERATE_DATE_Start: 新 API 缺少该字段; Result_Data.SERVERPART_CODES: 新 API 缺少该字段; ...共6处差异 |
| `BaseInfo/GetCASHWORKERList` | POST | Result_Data.List: 列表长度不一致 (1 vs 2); Result_Data.List[0].OPERATE_DATE_End: 新 API 缺少该字段; Result_Data.List[0].OPERATE_DATE_Start: 新 API 缺少该字段; ...共7处差异 |
| `BaseInfo/GetCOMMODITYDetail` | GET | Result_Data.COMMODITY_BUSINESS_ID: 新 API 缺少该字段; Result_Data.HIGHWAYPROINST_ID: 新 API 缺少该字段; Result_Data.QUALIFICATIONList: 新 API 缺少该字段; ...共24处差异 |
| `BaseInfo/GetCOMMODITYList` | POST | Result_Data.List[0].HIGHWAYPROINST_ID: 新 API 缺少该字段; Result_Data.List[0].QUALIFICATIONList: 新 API 缺少该字段; Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段; ...共18处差异 |
| `BaseInfo/GetCombineBrandList` | GET | Result_Data.List[0].BRAND_TYPENAME: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_TRADE: 新 API 缺少该字段; Result_Data.List[0].COMMISSION_RATIO: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetPROPERTYASSETSDetail` | GET | Result_Data.PROPERTYASSETS_IDS: 新 API 缺少该字段; Result_Data.PROPERTYASSETS_TYPES: 新 API 缺少该字段; Result_Data.PropertyShop: 新 API 缺少该字段; ...共6处差异 |
| `BaseInfo/GetPROPERTYASSETSList` | POST | Result_Data.List[0].BUSINESSPROJECT_ID: 新 API 缺少该字段; Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 缺少该字段; Result_Data.List[0].COMPACT_NAME: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetPROPERTYASSETSTreeList` | POST | Result_Data.List[0].children[0].children: 列表长度不一致 (2 vs 9); Result_Data.List[0].children[0].children[0].children: 新 API 缺少该字段; Result_Data.List[0].children[0].children[0].node.BUSINESSPROJECT_ID: 新 AP... |
| `BaseInfo/GetPROPERTYSHOPDetail` | GET | Result_Data.ENDDATE_End: 新 API 缺少该字段; Result_Data.ENDDATE_Start: 新 API 缺少该字段; Result_Data.PROPERTYASSETS_IDS: 新 API 缺少该字段; ...共22处差异 |
| `BaseInfo/GetPROPERTYSHOPList` | POST | Result_Data.List[0].ENDDATE_End: 新 API 缺少该字段; Result_Data.List[0].ENDDATE_Start: 新 API 缺少该字段; Result_Data.List[0].PROPERTYASSETS_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetRTSERVERPARTSHOPDetail` | GET | Result_Data.BUSINESS_TYPES: 新 API 缺少该字段; Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段; Result_Data.BUSINESS_DATE: 值不一致 ('2019/3/28 0:00:00' vs '2019-03-28T00:00:00'); ...共5处差异 |
| `BaseInfo/GetRTSERVERPARTSHOPList` | POST | Result_Data.List[0].BUSINESS_TYPES: 新 API 缺少该字段; Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_DATE: 值不一致 ('2020/4/12 0:00:00' vs '2020-04-12T00:00:00'); ...共4处差异 |
| `BaseInfo/GetSERVERPARTCRTDetail` | GET | Result_Data.SERVERPART_CODES: 新 API 缺少该字段; Result_Data.SERVERPART_IDS: 新 API 缺少该字段; Result_Data.SERVERPART_INDEX: 新 API 缺少该字段; ...共7处差异 |
| `BaseInfo/GetSERVERPARTCRTList` | POST | Result_Data.List[0].SERVERPART_CODES: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_INDEX: 新 API 缺少该字段; ...共7处差异 |
| `BaseInfo/GetSERVERPARTCRTTreeList` | POST | Result_Data.List[0].children[0].children: 新 API 缺少该字段; Result_Data.List[0].children[0].node.SERVERPART_CODES: 新 API 缺少该字段; Result_Data.List[0].children[0].node.SERVERPART_IDS: 新 API 缺少该字段; ...共23处差异 |
| `BaseInfo/GetSERVERPARTDetail` | GET | Result_Data.SERVERPART_CODES: 新 API 缺少该字段; Result_Data.SERVERPART_IDS: 新 API 缺少该字段; Result_Data.HKBL: 类型不一致 (NoneType vs str)，值为 None vs ''; ...共25处差异 |
| `BaseInfo/GetSERVERPARTList` | POST | Result_Data.List[0].RtServerPart: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_CODES: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; ...共7处差异 |
| `BaseInfo/GetSERVERPARTSHOP_LOGList` | POST | Result_Data.List[0].OPERATE_DATE_End: 新 API 缺少该字段; Result_Data.List[0].OPERATE_DATE_Start: 新 API 缺少该字段; Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetSPRegionShopTree` | GET | Result_Data.List[0].children[0].node.children[0].desc: 新 API 缺少该字段; Result_Data.List[0].children[0].node.children[0].ico: 新 API 缺少该字段; Result_Data.List[0].children[0].node.children[1].desc: 新 API 缺少该字... |
| `BaseInfo/GetServerPartShopNewDetail` | GET | Result_Data.RtServerPartShopList[1].BusinessEndDate: 值不一致 ('2022年7月21日' vs '2022年7月20日'); Result_Data.RtServerPartShopList[2].BusinessEndDate: 值不一致 ('2022年7月7日' vs '2022年7月6日'); Result_Data.RtServerPa... |
| `BaseInfo/GetServerPartShopNewList` | GET | Result_Data.List: 列表长度不一致 (29 vs 38); Result_Data.List[0].BUSINESS_BRAND: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_DATE: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetServerpartShopDetail` | GET | Result_Data.BANK_ACCOUNT: 新 API 缺少该字段; Result_Data.BANK_NAME: 新 API 缺少该字段; Result_Data.PROVINCE_CODE: 新 API 缺少该字段; ...共12处差异 |
| `BaseInfo/GetServerpartShopInfo` | GET | Result_Data.Business_BrandIcon: 新 API 缺少该字段; Result_Data.Business_BrandName: 新 API 缺少该字段; Result_Data.Business_State: 新 API 缺少该字段; ...共19处差异 |
| `BaseInfo/GetServerpartShopTree` | GET | Result_Data.List[0].node.children[0].desc: 新 API 缺少该字段; Result_Data.List[0].node.children[0].ico: 新 API 缺少该字段; Result_Data.List[0].node.children[1].desc: 新 API 缺少该字段; ...共25处差异 |
| `BaseInfo/GetTradeBrandTree` | GET | Result_Data.List[0].children[0].children: 类型不一致 (NoneType vs list)，值为 None vs []; Result_Data.List[0].children[0].node.BrandTreeList[0].Brand_ICO: 新 API 缺少该字段; Result_Data.List[0].children[0].node.Bra... |
| `BaseInfo/GetUSERDEFINEDTYPEDetail` | GET | Result_Data.SERVERPARTCODES: 新 API 缺少该字段; Result_Data.ShopNames: 新 API 缺少该字段; Result_Data.GOODSTYPE: 新 API 多出该字段; ...共25处差异 |
| `BaseInfo/GetUSERDEFINEDTYPEList` | POST | Result_Data.List[0].SERVERPARTCODES: 新 API 缺少该字段; Result_Data.List[0].ShopNames: 新 API 缺少该字段; Result_Data.List[0].GOODSTYPE: 新 API 多出该字段; ...共25处差异 |

#### 类型差异 (7)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BaseInfo/BindingOwnerUnitTree` | GET | Result_Data.List[0].children: 类型不一致 (list vs NoneType)，值为 [] vs None; Result_Data.List[13].children: 类型不一致 (list vs NoneType)，值为 [] vs None |
| `BaseInfo/GetBusinessBrandList` | GET | Result_Data.List[0].BRAND_CATEGORY: 类型不一致 (int vs float)，值为 1000 vs 1000.0; Result_Data.List[0].BRAND_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.List[0].BRAND_ID: 类型不一致 (int vs float)，值为... |
| `BaseInfo/GetBusinessTradeDetail` | GET | Result_Data.AUTOSTATISTICS_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.AUTOSTATISTICS_VALUE: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.INELASTIC_DEMAND: 类型不一致 (NoneType vs int)，值... |
| `BaseInfo/GetBusinessTradeTree` | GET | Result_Data.List[0].children[0].node.STATISTICS_TYPE: 值不一致 (35 vs 0); Result_Data.List[0].children[1].node.STATISTICS_TYPE: 值不一致 (20 vs 0); Result_Data.List[0].children[2].node.STATISTICS_TYPE: 值不一致 (... |
| `BaseInfo/GetCOMMODITYTYPEDetail` | GET | Result_Data.COMMODITYTYPE_EN: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.COMMODITYTYPE_ID: 类型不一致 (int vs float)，值为 1 vs 1.0; Result_Data.STAFF_NAME: 类型不一致 (NoneType vs str)，值为 None vs '' |
| `BaseInfo/GetCOMMODITYTYPEList` | POST | Result_Data.List[0].COMMODITYTYPE_ID: 类型不一致 (int vs float)，值为 418 vs 418.0 |
| `BaseInfo/GetOWNERUNITDetail` | GET | Result_Data.OWNERUNIT_DESC: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.OWNERUNIT_EN: 类型不一致 (NoneType vs str)，值为 None vs ''; Result_Data.OWNERUNIT_ICO: 类型不一致 (NoneType vs str)，值为 None vs '' |

### BigData (13 个 FAIL)

#### Python查询报错 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BigData/GetBAYONETDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'BAYONET_ID': None, 'SERVERPART_ID': None, 'SERVERPART_NAME': None, 'SERVERPAR...; Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-21... |
| `BigData/GetBAYONETList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 0, 'List': []} vs None; Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-2106]第1 行附近出现错误:... |

#### Result_Desc措辞差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BigData/GetDailyBayonetAnalysis` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 2994, 'List': [{'SERVERPART_NAME': '...; Result_Desc: 值不一致 ('查询成功' vs '成功') |

#### 字段差异 (10)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BigData/GetBAYONETDAILY_AHList` | POST | Result_Data.List[0].INOUT_TYPES: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; Result_Data.List[0].STATISTICS_DATE_End: 新 API 缺少该字段; ...共10处差异 |
| `BigData/GetBAYONETWARNINGList` | POST | Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_REGIONS: 新 API 缺少该字段; Result_Data.List[0].STATISTICS_DATE_End: 新 API 缺少该字段; ...共5处差异 |
| `BigData/GetBayonetOwnerAHList` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 0, 'List': []} vs None; ...共4处差异 |
| `BigData/GetBayonetOwnerMonthAHList` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 0, 'List': []} vs None; ...共4处差异 |
| `BigData/GetSECTIONFLOWDetail` | GET | Result_Data.SERVERPART_IDS: 新 API 缺少该字段; Result_Data.STATISTICS_DATE_End: 新 API 缺少该字段; Result_Data.STATISTICS_DATE_Start: 新 API 缺少该字段; ...共8处差异 |
| `BigData/GetSECTIONFLOWList` | POST | Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; Result_Data.List[0].STATISTICS_DATE_End: 新 API 缺少该字段; Result_Data.List[0].STATISTICS_DATE_Start: 新 API 缺少该字段; ...共25处差异 |
| `BigData/GetSECTIONFLOWMONTHDetail` | GET | Result_Data.HOLIDAY_TYPE: 新 API 缺少该字段; Result_Data.LARGEVEHICLE_COUNT: 新 API 缺少该字段; Result_Data.MEDIUMVEHICLE_COUNT: 新 API 缺少该字段; ...共21处差异 |
| `BigData/GetSECTIONFLOWMONTHList` | POST | Result_Data.List[0].SERVERPART_IDS: 新 API 缺少该字段; Result_Data.List[0].STATISTICS_MONTH_End: 新 API 缺少该字段; Result_Data.List[0].STATISTICS_MONTH_Start: 新 API 缺少该字段; ...共25处差异 |
| `BigData/GetServerpartSectionFlow` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List[0].STATISTICS_DATE: 值不一致 ('2023-08' vs '202112'); Result_Data.List[0].list[0].SERVERPART.DATE_COUNT: 新 API 多出该字段; ...共25处差异 |
| `BigData/GetTimeIntervalList` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (1 vs 24); Result_Data.List[0].Data: 新 API 缺少该字段; ...共9处差异 |

### Budget (4 个 FAIL)

#### DatabaseHelper缺少方法 (4)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Budget/GetBudgetDetailDetail` | GET | Result_Code: 类型不一致 (int vs str)，值为 100 vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'"; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'BUDGETDETAIL_AH_ID': 132, 'BUDGETPROJECT_AH_ID': 2, 'AC... |
| `Budget/GetBudgetDetailList` | POST | Result_Code: 类型不一致 (int vs str)，值为 100 vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'"; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List... |
| `Budget/GetBudgetProjectList` | POST | Result_Code: 类型不一致 (int vs str)，值为 100 vs "查询失败'DatabaseHelper' object has no attribute 'fetch_scalar'"; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 2, 'List... |
| `Budget/GetbudgetProjectDetail` | GET | Result_Code: 类型不一致 (int vs str)，值为 100 vs "查询失败'DatabaseHelper' object has no attribute 'fetch_one'"; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'BUDGETPROJECT_AH_ID': 128, 'BUDGETPROJECT_CODE': '', 'B... |

### BusinessMan (3 个 FAIL)

#### DatabaseHelper缺少方法 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BusinessMan/GetCOMMODITY_TEMPDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'COMMODITY_TEMP_ID': 43, 'DATA_TYPE': 1000, 'COMMODITY_ID': 221921, 'COMMODITY...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `BusinessMan/GetCOMMODITY_TEMPList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'COMMODITY_TEMP_ID':...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |

#### Result_Desc措辞差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BusinessMan/GetUserList` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (16 vs 0); Result_Data.TotalCount: 值不一致 (16 vs 0); ...共4处差异 |

### BusinessProject (40 个 FAIL)

#### Python查询报错 (4)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BusinessProject/GetMerchantsReceivables` | GET | Result_Code: 值不一致 (200 vs 100); Result_Data: 类型不一致 (NoneType vs dict)，值为 None vs {'COOPMERCHANTS_ID': None, 'COOPMERCHANTS_NAME': '', 'COOPMERCHANTS_TYP...; Result_Desc: 值不一致 ('查询失败，请传入经营商户内码或门店内码集合！'... |
| `BusinessProject/GetProjectAccountDetail` | GET | Result_Code: 值不一致 (100 vs 200); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'BUSINESSPROJECT_ID': 1498, 'BUSINESSPROJECT_NAME': '太白服务区同庆楼合同项目', 'REGISTERC...; Result_Desc: 值不一致 ('查询成功' vs '查询失败，无数据返回！') |
| `BusinessProject/GetRTPaymentRecordList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 0, 'PageSize': 0, 'TotalCount': 1, 'List': [{'RTPAYMENTRECORD_ID'...; Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-22... |
| `BusinessProject/GetWillSettleProject` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 6, 'TotalCount': 6, 'List': [{'BUSINESSPROJECT_ID'...; Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-61... |

#### 值差异 (4)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BusinessProject/GetAccountWarningListSummary` | GET | Result_Data.List[1].value: 值不一致 (103 vs 158); Result_Data.List[2].value: 值不一致 (5 vs 4); Result_Data.List[3].value: 值不一致 (35 vs 50); ...共9处差异 |
| `BusinessProject/GetBrandReceivables` | GET | Result_Data.List: 列表长度不一致 (26 vs 0); Result_Data.OtherData: 列表长度不一致 (11 vs 0); Result_Data.PageSize: 值不一致 (10 vs 999); ...共4处差异 |
| `BusinessProject/GetMerchantsReceivablesReport` | GET | Result_Data.List: 列表长度不一致 (185 vs 0); Result_Data.PageSize: 值不一致 (185 vs 999); Result_Data.TotalCount: 值不一致 (185 vs 0) |
| `BusinessProject/GetShopExpenseSummary` | GET | Result_Data.List: 列表长度不一致 (1 vs 0); Result_Data.PageSize: 值不一致 (10 vs 9999); Result_Data.TotalCount: 值不一致 (1 vs 0) |

#### 字段差异 (30)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BusinessProject/GetAPPROVEDList` | POST | Result_Data.List[0].APPROVED_DATE_End: 新 API 缺少该字段; Result_Data.List[0].APPROVED_DATE_Start: 新 API 缺少该字段; Result_Data.List[0].APPROVED_TYPES: 新 API 缺少该字段; ...共6处差异 |
| `BusinessProject/GetAccountWarningList` | GET | Result_Data.List[0].BUSINESS_ENDDATE: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_STARTDATE: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_TRADE: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetAnnualSplit` | GET | Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_ENDDATE: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_PERIOD: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetBIZPSPLITMONTHDetail` | GET | Result_Data.Approvalstate: 新 API 缺少该字段; Result_Data.BIZPSPLITMONTH_IDS: 新 API 缺少该字段; Result_Data.SHOPROYALTY_IDS: 新 API 缺少该字段; ...共5处差异 |
| `BusinessProject/GetBIZPSPLITMONTHList` | POST | Result_Data.List[0].Approvalstate: 新 API 缺少该字段; Result_Data.List[0].BIZPSPLITMONTH_IDS: 新 API 缺少该字段; Result_Data.List[0].SHOPROYALTY_IDS: 新 API 缺少该字段; ...共5处差异 |
| `BusinessProject/GetBUSINESSPROJECTSPLITDetail` | GET | Result_Data.ACCOUNT_AMOUNT: 新 API 缺少该字段; Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.CURCASHPAY_AMOUNT: 新 API 缺少该字段; ...共24处差异 |
| `BusinessProject/GetBUSINESSPROJECTSPLITList` | POST | Result_Data.OtherData: 新 API 缺少该字段; Result_Data.List[0].ACCOUNT_AMOUNT: 新 API 缺少该字段; Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetBusinessPaymentDetail` | GET | Result_Data.BUSINESS_TRADE: 新 API 多出该字段; Result_Data.BUSINESS_TRADENAME: 新 API 多出该字段; Result_Data.SERVERPART_TYPE: 新 API 多出该字段; ...共4处差异 |
| `BusinessProject/GetBusinessPaymentList` | POST | Result_Data.List[0].BUSINESS_TRADE: 新 API 多出该字段; Result_Data.List[0].BUSINESS_TRADENAME: 新 API 多出该字段; Result_Data.List[0].SERVERPART_TYPE: 新 API 多出该字段; ...共25处差异 |
| `BusinessProject/GetBusinessProjectDetail` | GET | Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.CLOSED_DATE_End: 新 API 缺少该字段; Result_Data.CLOSED_DATE_Start: 新 API 缺少该字段; ...共16处差异 |
| `BusinessProject/GetBusinessProjectList` | POST | Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.List[0].CLOSED_DATE_End: 新 API 缺少该字段; Result_Data.List[0].CLOSED_DATE_Start: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetExpenseSummary` | GET | Result_Data.List: 列表长度不一致 (1 vs 690); Result_Data.List[0].children: 新 API 缺少该字段; Result_Data.List[0].node: 新 API 缺少该字段; ...共11处差异 |
| `BusinessProject/GetMerchantSplit` | GET | Result_Data.List: 列表长度不一致 (4 vs 91); Result_Data.List[0].BUSINESSPROJECT_NAME: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_ENDDATE: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetMerchantsReceivablesList` | GET | Result_Data.List[0].ACCOUNT_DATE: 新 API 缺少该字段; Result_Data.List[0].AccountReceivablesList: 新 API 缺少该字段; Result_Data.List[0].COOPMERCHANTS_EN: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetNoProjectShopList` | GET | Result_Data.List: 列表长度不一致 (10 vs 11); Result_Data.List[0].index: 新 API 缺少该字段; Result_Data.List[0].type: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetPERIODWARNINGDetail` | GET | Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.BUSINESS_STATES: 新 API 缺少该字段; Result_Data.BUSINESS_TRADES: 新 API 缺少该字段; ...共18处差异 |
| `BusinessProject/GetPERIODWARNINGList` | POST | Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_STATES: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_TRADES: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetPROJECTSPLITMONTHDetail` | GET | Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.MERCHANTS_IDS: 新 API 缺少该字段; Result_Data.REGISTERCOMPACT_IDS: 新 API 缺少该字段; ...共7处差异 |
| `BusinessProject/GetPROJECTSPLITMONTHList` | POST | Result_Data.List[0].BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.List[0].MERCHANTS_IDS: 新 API 缺少该字段; Result_Data.List[0].REGISTERCOMPACT_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetPROJECTWARNINGDetail` | GET | Result_Data.BUSINESSPROJECT_ICO: 新 API 缺少该字段; Result_Data.PROJECTWARNING_STATES: 新 API 缺少该字段; Result_Data.SERVERPART_IDS: 新 API 缺少该字段; ...共13处差异 |
| `BusinessProject/GetPROJECTWARNINGList` | POST | Result_Data.List[0].BUSINESSPROJECT_ICO: 新 API 缺少该字段; Result_Data.List[0].COMPACT_ENDDATE: 新 API 缺少该字段; Result_Data.List[0].COMPACT_STARTDATE: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetPaymentConfirmDetail` | GET | Result_Data.BUSINESSPROJECT_NAME: 新 API 缺少该字段; Result_Data.PAYMENTCONFIRM_PID: 新 API 缺少该字段; Result_Data.REMARKS_DESC: 新 API 缺少该字段; ...共13处差异 |
| `BusinessProject/GetPeriodWarningList` | GET | Result_Data.List: 列表长度不一致 (1 vs 10); Result_Data.List[0].children: 新 API 缺少该字段; Result_Data.List[0].node: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetProjectAccountList` | GET | Result_Data.List: 列表长度不一致 (574 vs 10); Result_Data.List[0].APPLY_PROCCESS: 新 API 缺少该字段; Result_Data.List[0].APPOVED_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetProjectAccountTree` | GET | Result_Data.List[0].children: 新 API 缺少该字段; Result_Data.List[0].node: 新 API 缺少该字段; Result_Data.List[0].SERVERPART_ID: 新 API 多出该字段; ...共8处差异 |
| `BusinessProject/GetRTPaymentRecordDetail` | GET | Result_Data.ACCOUNT_AMOUNT: 新 API 缺少该字段; Result_Data.ACCOUNT_DATE: 新 API 缺少该字段; Result_Data.ACTUAL_PAYMENT: 新 API 缺少该字段; ...共9处差异 |
| `BusinessProject/GetRevenueConfirmDetail` | GET | Result_Data.BUSINESSAPPROVAL_IDS: 新 API 缺少该字段; Result_Data.BUSINESSPROJECT_IDS: 新 API 缺少该字段; Result_Data.BUSINESSPROJECT_NAME: 新 API 缺少该字段; ...共12处差异 |
| `BusinessProject/GetRevenueConfirmList` | GET | Result_Data.List[0].BREACHPENALTY: 新 API 缺少该字段; Result_Data.List[0].BUSINESSAPPROVAL_ID: 新 API 缺少该字段; Result_Data.List[0].BUSINESSAPPROVAL_IDS: 新 API 缺少该字段; ...共25处差异 |
| `BusinessProject/GetSHOPEXPENSEDetail` | GET | Result_Data.ApprovalProcess: 新 API 缺少该字段; Result_Data.ChangeFlag: 新 API 缺少该字段; Result_Data.ImageFlag: 新 API 缺少该字段; ...共16处差异 |
| `BusinessProject/GetSHOPEXPENSEList` | POST | Result_Data.summaryObject: 新 API 多出该字段; Result_Data.List[0].ApprovalProcess: 新 API 缺少该字段; Result_Data.List[0].ChangeFlag: 新 API 缺少该字段; ...共25处差异 |

#### 类型差异 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `BusinessProject/GetRemarksDetail` | GET | Result_Data.OPERATE_DATE: 类型不一致 (str vs float)，值为 '2023/05/26 15:52:50' vs 20230526155250.0 |
| `BusinessProject/GetRemarksList` | POST | Result_Data.List[0].OPERATE_DATE: 类型不一致 (str vs float)，值为 '2023/05/26 15:52:50' vs 20230526155250.0 |

### Commodity (3 个 FAIL)

#### 值差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Commodity/GetCOMMODITYList` | POST | Result_Data.List[0].OPERATE_DATE: 值不一致 ('2024/6/11 10:37:22' vs '2024-06-11T10:37:22'); Result_Data.List[1].OPERATE_DATE: 值不一致 ('2021/4/6 17:58:24' vs '2021-04-06T17:58:24'); Result_Data.List[2].OPERA... |

#### 字段差异 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Commodity/GetCOMMODITYDetail` | GET | Result_Data.ADDTIME: 新 API 缺少该字段; Result_Data.BUSINESSAPPROVAL_ID: 新 API 缺少该字段; Result_Data.BUSINESSTYPE: 新 API 缺少该字段; ...共25处差异 |
| `Commodity/GetCommodityList` | GET | Result_Data.List[0].BUSINESSTYPE_NAME: 新 API 缺少该字段; Result_Data.List[0].BUSINESSTYPE: 新 API 多出该字段; Result_Data.List[0].COMMODITY_TYPE: 值不一致 ('休闲食品类' vs '1134'); ...共25处差异 |

### Contract (8 个 FAIL)

#### 其他 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Contract/GetProjectYearlyArrearageList` | GET | Result_Data.ProjectCompleteDetailList: 列表长度不一致 (5 vs 0) |

#### 字段差异 (3)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Contract/GetProjectMonthlyArrearageList` | GET | Result_Data.ProjectCompleteDetailList: 列表长度不一致 (5 vs 0); Result_Data.ProjectMonthlyCompleteList[0].Business_Year: 新 API 缺少该字段; Result_Data.ProjectMonthlyCompleteList[0].ProjectCompleteDetailList[0].Ex... |
| `Contract/GetRegisterCompactDetail` | GET | Result_Data.CLOSED_DATE: 新 API 缺少该字段; Result_Data.RELATE_COMPACT: 新 API 缺少该字段; Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段; ...共15处差异 |
| `Contract/GetRegisterCompactList` | POST | Result_Data.List[0].LogList: 新 API 缺少该字段; Result_Data.List[0].RENEWAL_YEARS: 新 API 缺少该字段; Result_Data.List[0].BUSINESS_TRADE: 类型不一致 (int vs NoneType)，值为 4 vs None; ...共25处差异 |

#### 类型差异 (4)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Contract/GetAttachmentDetail` | GET | Result_Data.OPERATE_DATE: 类型不一致 (int vs float)，值为 20240117110440 vs 20240117110440.0; Result_Data.STAFF_NAME: 类型不一致 (NoneType vs str)，值为 None vs '' |
| `Contract/GetAttachmentList` | POST | Result_Data.List[0].OPERATE_DATE: 类型不一致 (int vs float)，值为 20240117110440 vs 20240117110440.0 |
| `Contract/GetRegisterCompactSubDetail` | GET | Result_Data.OPERATING_AREA: 类型不一致 (float vs int)，值为 0.0 vs 0; Result_Data.PROPERTY_FEE: 类型不一致 (float vs int)，值为 0.0 vs 0 |
| `Contract/GetRegisterCompactSubList` | POST | Result_Data.List[0].OPERATING_AREA: 类型不一致 (float vs int)，值为 0.0 vs 0; Result_Data.List[0].PROPERTY_FEE: 类型不一致 (float vs int)，值为 0.0 vs 0 |

### Customer (2 个 FAIL)

#### Python查询报错 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Customer/GetCUSTOMERGROUP_AMOUNTList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 52, 'List': [{'CUSTOMERGROUP_AMOU...; Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-21... |

#### 字段差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Customer/GetCUSTOMERGROUP_AMOUNTDetail` | GET | Result_Data.SERVERPART_CODES: 新 API 缺少该字段; Result_Data.SERVERPART_IDS: 新 API 缺少该字段; Result_Data.STATISTICS_MONTH_End: 新 API 缺少该字段; ...共5处差异 |

### Finance (2 个 FAIL)

#### Result_Desc措辞差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Finance/GetAccountCompare` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (1 vs 0); Result_Data.TotalCount: 值不一致 (1 vs 0); ...共4处差异 |

#### 字段差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Finance/GetAHJKtoken` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('获取失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |

### Merchants (11 个 FAIL)

#### DatabaseHelper缺少方法 (7)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Merchants/GetBusinessManDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'OWNERUNIT_ID': 123, 'OWNERUNIT_PID': 98, 'PROVINCE_CODE': 330000, 'PROVINCE_B...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Merchants/GetBusinessManDetailDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'OWNERUNITDETAIL_ID': 19, 'OWNERUNIT_ID': 403, 'OWNERUNIT_TYPE': None, 'OWNERU...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Merchants/GetBusinessManDetailList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 5, 'List': [{'OWNERUNITDETAIL_ID'...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Merchants/GetBusinessManList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'OWNERUNIT_ID': 49, ...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Merchants/GetCUSTOMTYPEDetail` | GET | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'CUSTOMTYPE_ID': 49, 'CUSTOMTYPE_PID': -1, 'CUSTOMTYPE_NAME': ' 开江艳艳副食', 'CUST...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Merchants/GetCUSTOMTYPEList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{'CUSTOMTYPE_ID': 49,...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |
| `Merchants/GetCommodityList` | POST | Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 32, 'List': [{'COMMODITY_BUSINESS...; Result_Desc: 值不一致 ('查询成功' vs "查询失败'Database... |

#### Python查询报错 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Merchants/GetCoopMerchantsList` | POST | <root>.Result_Data: 新 API 缺少该字段; Result_Code: 值不一致 (100 vs 999); Result_Desc: 值不一致 ('查询成功' vs '查询失败[CODE:-544]超出全局排序空间，请调整SORT_BUF_GLOBAL_SIZE、SORT_BUF_SIZE、SORT_BLK_SIZE') |

#### Result_Desc措辞差异 (3)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Merchants/GetCommodityDetail` | GET | <root>.Message: 新 API 多出该字段; Result_Code: 值不一致 (100 vs 999); Result_Data: 类型不一致 (dict vs NoneType)，值为 {'COMMODITY_BUSINESS_ID': 12, 'COMMODITY_TYPE': None, 'COMMODITY_TYPENAME': Non...; ...共4处差异 |
| `Merchants/GetCustomTypeDDL` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 32, 'List': [{'node': {'label': '开江连...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Merchants/GetNestingCustomTypeLsit` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 10, 'TotalCount': 32, 'List': [{'node': {'CUSTOMTYPE_I...; Result_Desc: 值不一致 ('查询成功' vs '成功') |

### MobilePay (6 个 FAIL)

#### Result_Desc措辞差异 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `MobilePay/GetBANKACCOUNTVERIFYTreeList` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'SPREGIONTYPE_I...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `MobilePay/GetMobilePayRoyaltyReport` | GET | Result_Data: 类型不一致 (dict vs list)，值为 {'PageIndex': 1, 'PageSize': 1, 'TotalCount': 1, 'List': [{'node': {'index': None, ...; Result_Desc: 值不一致 ('查询成功' vs '成功') |

#### 字段差异 (4)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `MobilePay/GetBANKACCOUNTVERIFYList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |
| `MobilePay/GetBANKACCOUNTVERIFYRegionList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |
| `MobilePay/GetBANKACCOUNTVERIFYServerList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |
| `MobilePay/GetMobilePayResult` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |

### Revenue (27 个 FAIL)

#### HTTP方法/参数校验错误 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Revenue/GetRevenueYOYQOQ` | GET | HTTP 200/405; <root>.Result_Code: 新 API 缺少该字段; <root>.Result_Data: 新 API 缺少该字段; <root>.Result_Desc: 新 API 缺少该字段; ...共4处差异 |

#### Python查询报错 (7)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Revenue/GetACCOUNTWARNINGList` | POST | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-544]超出全局排序空间，请调整SORT_BUF_GLOBAL_SIZE、SORT_BUF_SIZE、SORT_BLK_SIZE'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'Total... |
| `Revenue/GetBRANDANALYSISDetail` | GET | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-2106]第1 行附近出现错误:\n无效的表或视图名[T_BRANDANALYSIS]'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'BRANDANALYSIS_ID': 4478, 'SERVERPART_ID': 416, 'SERVERPAR... |
| `Revenue/GetBRANDANALYSISList` | POST | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-2106]第1 行附近出现错误:\n无效的表或视图名[T_BRANDANALYSIS]'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List': [{... |
| `Revenue/GetREVENUEDAILYSPLITDetail` | GET | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-2106]第1 行附近出现错误:\n无效的表或视图名[T_REVENUEDAILYSPLIT]'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'REVENUEDAILYSPLIT_ID': 74914, 'STATISTICS_DATE': '202... |
| `Revenue/GetREVENUEDAILYSPLITList` | POST | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-2106]第1 行附近出现错误:\n无效的表或视图名[T_REVENUEDAILYSPLIT]'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List'... |
| `Revenue/GetSITUATIONANALYSISDetail` | GET | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-2106]第1 行附近出现错误:\n无效的表或视图名[T_SITUATIONANALYSIS]'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'SITUATIONANALYSIS_ID': 2446, 'SERVERPART_ID': 416, 'S... |
| `Revenue/GetSITUATIONANALYSISList` | POST | Result_Code: 类型不一致 (int vs str)，值为 100 vs '查询失败[CODE:-2106]第1 行附近出现错误:\n无效的表或视图名[T_SITUATIONANALYSIS]'; Result_Data: 类型不一致 (dict vs NoneType)，值为 {'PageIndex': 1, 'PageSize': 9, 'TotalCount': 1, 'List'... |

#### Result_Desc措辞差异 (10)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Revenue/GetACCOUNTWARNINGDetail` | GET | Result_Data: 类型不一致 (dict vs NoneType)，值为 {'ACCOUNTWARNING_ID': 8941, 'WARNING_TYPE': 0, 'BUSINESSPROJECT_ID': 1838, 'BUS...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Revenue/GetBUSINESSWARNINGDetail` | GET | Result_Data.DATATYPES: 新 API 缺少该字段; Result_Data.SERVERPARTSHOP_IDS: 新 API 缺少该字段; Result_Data.SERVERPART_IDS: 新 API 缺少该字段; ...共17处差异 |
| `Revenue/GetBankAccountReport` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Revenue/GetBrandAnalysis` | GET | Result_Data.List: 新 API 缺少该字段; Result_Data.PageIndex: 新 API 缺少该字段; Result_Data.PageSize: 新 API 缺少该字段; ...共5处差异 |
| `Revenue/GetBusinessDate` | GET | Result_Data.label: 值不一致 ('2021/01/30' vs '2021-01-30'); Result_Data.value: 值不一致 ('2026/02/10' vs '2026-02-10'); Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Revenue/GetBusinessItemSummary` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (1 vs 0); Result_Data.PageSize: 值不一致 (1 vs 10); ...共5处差异 |
| `Revenue/GetBusinessTradeAnalysis` | GET | Result_Data.List: 新 API 缺少该字段; Result_Data.PageIndex: 新 API 缺少该字段; Result_Data.PageSize: 新 API 缺少该字段; ...共5处差异 |
| `Revenue/GetCigaretteReport` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (1 vs 0); Result_Data.PageSize: 值不一致 (1 vs 10); ...共5处差异 |
| `Revenue/GetSituationAnalysis` | GET | Result_Data.List: 新 API 缺少该字段; Result_Data.PageIndex: 新 API 缺少该字段; Result_Data.PageSize: 新 API 缺少该字段; ...共5处差异 |
| `Revenue/GetTotalRevenue` | GET | Result_Data.BankAccount_Amount: 新 API 缺少该字段; Result_Data.CashPay_Amount: 新 API 缺少该字段; Result_Data.Cash_Correct: 新 API 缺少该字段; ...共19处差异 |

#### 字段差异 (9)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Revenue/GetBUSINESSANALYSISList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |
| `Revenue/GetBUSINESSWARNINGList` | POST | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List[0].DATATYPES: 新 API 缺少该字段; Result_Data.List[0].SERVERPARTSHOP_IDS: 新 API 缺少该字段; ...共25处差异 |
| `Revenue/GetCurTotalRevenue` | GET | Result_Data.BankAccount_Amount: 新 API 缺少该字段; Result_Data.CashPay_Amount: 新 API 缺少该字段; Result_Data.Cash_Correct: 新 API 缺少该字段; ...共25处差异 |
| `Revenue/GetMerchantRevenueReport` | GET | Result_Data.OtherData: 新 API 缺少该字段; Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List[0].children[0].children: 列表长度不一致 (14 vs 0); ...共25处差异 |
| `Revenue/GetMonthINCAnalysis` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List[0].children[0].node.SERVERPARTSHOP_ID: 新 API 缺少该字段; Result_Data.List[0].children[0].node.SERVERPARTSHOP_IDS: 新 API 缺少该字段; ...共25处差异 |
| `Revenue/GetPERSONSELLList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |
| `Revenue/GetRevenueDataList` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (29 vs 19564); Result_Data.List[0].Business_Type: 新 API 缺少该字段; ...共25处差异 |
| `Revenue/GetRevenueReport` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List[0].children[0].children[0].children: 新 API 缺少该字段; Result_Data.List[0].children[0].children[0].node.Business_Type: 新 API 缺少该字段; ...共25处差异 |
| `Revenue/GetRevenueReportByDate` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List[0].children[0].node.Business_Type: 新 API 缺少该字段; Result_Data.List[0].children[0].node.Business_Type_Text: 新 API 缺少该字段; ...共25处差异 |

### Sales (2 个 FAIL)

#### 字段差异 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Sales/GetCOMMODITYSALEList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |
| `Sales/GetEndaccountError` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('处理失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |

### Supplier (1 个 FAIL)

#### 字段差异 (1)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Supplier/GetQUALIFICATION_HISList` | POST | <root>.Message: 新 API 多出该字段; Result_Desc: 值不一致 ('查询失败未将对象引用设置到对象的实例。' vs '请求参数校验失败') |

### Verification (2 个 FAIL)

#### Result_Desc措辞差异 (2)

| 接口 | 方法 | 差异摘要 |
|---|---|---|
| `Verification/GetShopEndaccountSum` | GET | Result_Data: 类型不一致 (dict vs NoneType)，值为 {'Serverpart_ID': 416, 'Serverpart_Name': '新桥服务区', 'ServerpartShop_Code': '0490...; Result_Desc: 值不一致 ('查询成功' vs '成功') |
| `Verification/GetSuppEndaccountList` | GET | Result_Data.StaticsModel: 新 API 多出该字段; Result_Data.List: 列表长度不一致 (1 vs 0); Result_Data.TotalCount: 值不一致 (1 vs 0); ...共4处差异 |
