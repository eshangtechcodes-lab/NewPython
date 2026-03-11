# API 接口整改进度表（真实差异）

> 更新时间: 2026-03-11 09:52
> 数据来源: `docs/session5_full.json`（全量对比 329 接口）
> 本表仅列出 **真实字段差异** 的接口（排除 C# 旧 API 报错和新 API 代码 bug）

## 总览

| 分类 | 数量 |
|------|------|
| 总接口数 | 329 |
| ✅ PASS | 38 |
| ❌ 真实差异（本表） | 169 |
| ⚠️ 新 API 报错/空参 | 57 |
| 🔕 C# 旧 API 报错/404 | 65 |

## 模块汇总

| # | 模块 | 差异接口数 | 修复状态 |
|---|------|-----------|----------|
| 1 | [Analysis](#analysis) | 19 | ⬜ 待修复 |
| 2 | [Audit](#audit) | 9 | ⬜ 待修复 |
| 3 | [BaseInfo](#baseinfo) | 44 | ⬜ 待修复 |
| 4 | [BigData](#bigdata) | 11 | ⬜ 待修复 |
| 5 | [BusinessMan](#businessman) | 1 | ⬜ 待修复 |
| 6 | [BusinessProject](#businessproject) | 39 | ⬜ 待修复 |
| 7 | [Commodity](#commodity) | 2 | ⬜ 待修复 |
| 8 | [Contract](#contract) | 8 | ⬜ 待修复 |
| 9 | [Finance](#finance) | 1 | ⬜ 待修复 |
| 10 | [Merchants](#merchants) | 6 | ⬜ 待修复 |
| 11 | [MobilePay](#mobilepay) | 2 | ⬜ 待修复 |
| 12 | [Revenue](#revenue) | 24 | ⬜ 待修复 |
| 13 | [Supplier](#supplier) | 2 | ⬜ 待修复 |
| 14 | [Verification](#verification) | 1 | ⬜ 待修复 |
| | **合计** | **169** | |

---

## Analysis

> 19 个接口存在差异

### 1. `GetANALYSISINSDetail`

- **接口**: `Analysis/GetANALYSISINSDetail`
- **差异数**: 6
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `ANALYSISINS_FORMATS`, `ANALYSISINS_TYPES`, `SERVERPART_IDS`

**类型不一致** (2):
  - KEY_CONTENT: str→NoneType
  - STAFF_NAME: str→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 2. `GetANALYSISINSList`

- **接口**: `Analysis/GetANALYSISINSList`
- **差异数**: 18
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `ANALYSISINS_FORMATS`, `ANALYSISINS_TYPES`, `SERVERPART_IDS`

**多出字段** (2):
  `OtherData`, `StaticsModel`

**类型不一致** (7):
  - ANALYSISINS_FORMAT: int→NoneType
  - ANALYSISINS_STATE: int→NoneType
  - ANALYSISINS_TYPE: int→NoneType
  - OPERATE_DATE: str→NoneType
  - PROVINCE_CODE: int→NoneType
  - SERVERPART_ID: int→NoneType
  - SPREGIONTYPE_ID: int→NoneType

**值不一致** (5):
  - ANALYSISINS_ID: 1805 → 7249
  - ANALYSIS_CONTENT
  - PageSize: 9 → 10
  - TotalCount: 1 → 7207
  - Result_Desc: `查询成功` → `成功`

**列表差异** (1):
  - List: 1→9

### 3. `GetANALYSISRULEDetail`

- **接口**: `Analysis/GetANALYSISRULEDetail`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 4. `GetANALYSISRULEList`

- **接口**: `Analysis/GetANALYSISRULEList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `ANALYSISRULE_IDS`, `CREATE_DATE_End`, `CREATE_DATE_Start`, `UPDATE_DATE_End`, `UPDATE_DATE_Start`

**多出字段** (2):
  `OtherData`, `StaticsModel`

**类型不一致** (8):
  - ANALYSISRULE_STATE: int→NoneType
  - ENABLE_CHART: int→NoneType
  - ENABLE_PDF_EXPORT: int→NoneType
  - ENABLE_TABLE: int→NoneType
  - ENABLE_VIEW_MORE: int→NoneType
  - RULE_PRIORITY: int→NoneType
  - RULE_SOURCE: int→NoneType
  - SPRESPONSE_TYPE: int→NoneType

**值不一致** (10):
  - ANALYSISRULE_DESC: `通过传递日期参数，查询服务区门店客单数量、同比客单、同比增长` → ``
  - ANALYSISRULE_ID: 19 → 54
  - API_ENDPOINT
  - CREATE_DATE: `2024/11/22 0:00:00` → `2026-01-05T11:54:19`
  - OUTPUT_FORMAT
  - PARAM_TEMPLATE
  - PARSING_RULES
  - RESPONSE_CONFIG
  - RESPONSE_FIELD
  - TRIGGER_WORDS: `客单均价|客单` → `预警|问题|特情`

### 5. `GetASSETSPROFITSBusinessTreeList`

- **接口**: `Analysis/GetASSETSPROFITSBusinessTreeList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (2):
  - PageSize: 999 → 10
  - Result_Desc: `查询成功` → `成功`

### 6. `GetASSETSPROFITSDateDetailList`

- **接口**: `Analysis/GetASSETSPROFITSDateDetailList`
- **差异数**: 1
- **状态**: ⬜ 待修复

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 7. `GetASSETSPROFITSTreeList`

- **接口**: `Analysis/GetASSETSPROFITSTreeList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (2):
  - PageSize: 9 → 10
  - Result_Desc: `查询成功` → `成功`

### 8. `GetAssetsLossProfitList`

- **接口**: `Analysis/GetAssetsLossProfitList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 9. `GetInvestmentReport`

- **接口**: `Analysis/GetInvestmentReport`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 10. `GetNestingIAReport`

- **接口**: `Analysis/GetNestingIAReport`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 11. `GetPERIODMONTHPROFITDetail`

- **接口**: `Analysis/GetPERIODMONTHPROFITDetail`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 12. `GetPERIODMONTHPROFITList`

- **接口**: `Analysis/GetPERIODMONTHPROFITList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (9):
  `BUSINESSPROJECT_IDS`, `BUSINESS_STATES`, `BUSINESS_TYPES`, `SERVERPART_IDS`, `SETTLEMENT_MODESS`, `SHOPROYALTY_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`, `WARNING_TYPES`

**多出字段** (2):
  `OtherData`, `StaticsModel`

**类型不一致** (1):
  - ENDDATE: str→int

**值不一致** (12):
  - ACTUAL_RATIO
  - BUSINESSPROJECT_ID: 668 → 912
  - BUSINESSPROJECT_NAME: `清溪服务区轻餐饮QX-07项目` → `君王服务区麦当劳项目`
  - BUSINESS_TRADE: 215 → 227
  - COMMISSION_RATIO
  - COST_AMOUNT
  - GUARANTEERATIO
  - GUARANTEE_PRICE
  - MERCHANTS_ID
  - MERCHANTS_NAME: `桐乡市盛开源高速公路服务区经营管理有限公司` → `安徽联升餐厅食品有限公司`
  - ...等12处

**列表差异** (1):
  - List: 1→9

### 13. `GetPROFITCONTRIBUTEDetail`

- **接口**: `Analysis/GetPROFITCONTRIBUTEDetail`
- **差异数**: 10
- **状态**: ⬜ 待修复

**缺少字段** (6):
  `BUSINESSPROJECT_IDS`, `EVALUATE_TYPES`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `STATISTICS_DATE_End`, `STATISTICS_DATE_Start`

**类型不一致** (3):
  - PROFITCONTRIBUTE_DESC: str→NoneType
  - STAFF_NAME: str→NoneType
  - STATISTICS_DATE: str→int

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 14. `GetPROFITCONTRIBUTEList`

- **接口**: `Analysis/GetPROFITCONTRIBUTEList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (6):
  `BUSINESSPROJECT_IDS`, `EVALUATE_TYPES`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `STATISTICS_DATE_End`, `STATISTICS_DATE_Start`

**多出字段** (2):
  `OtherData`, `StaticsModel`

**类型不一致** (3):
  - EVALUATE_SCORE: NoneType→float
  - SABFI_SCORE: NoneType→float
  - STATISTICS_DATE: str→int

**值不一致** (12):
  - BUSINESSPROJECT_ID: 50 → 1760
  - BUSINESSPROJECT_NAME: `新桥服务区（品牌寿司(新业态））项目` → ``
  - CALCULATE_SELFSHOP: 1 → 2
  - EVALUATE_TYPE: 0 → 6
  - PROFITCONTRIBUTE_ID: 7 → 190668
  - PROFITCONTRIBUTE_PID
  - PROFITCONTRIBUTE_STATE: 0 → 1
  - RECORD_DATE: `2024-11-01T16:30:43` → `2026-01-07T15:21:49`
  - SERVERPARTSHOP_ID: `3058,3059` → `5580,5581`
  - SERVERPARTSHOP_NAME: `鲜道寿司` → `美食汇`
  - ...等12处

### 15. `GetPeriodMonthlyList`

- **接口**: `Analysis/GetPeriodMonthlyList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 16. `GetRevenueEstimateList`

- **接口**: `Analysis/GetRevenueEstimateList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 17. `GetSENTENCEDetail`

- **接口**: `Analysis/GetSENTENCEDetail`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `OPERATE_DATE_End`, `OPERATE_DATE_Start`

**类型不一致** (3):
  - ANALYSISRULE_ID: str→NoneType
  - DIALOG_CODE: str→NoneType
  - SERVERPART_ID: str→NoneType

**值不一致** (2):
  - OPERATE_DATE: `2024/10/30 17:59:17` → `2024-10-30T17:59:17`
  - Result_Desc: `查询成功` → `成功`

### 18. `GetSENTENCEList`

- **接口**: `Analysis/GetSENTENCEList`
- **差异数**: 17
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `OPERATE_DATE_End`, `OPERATE_DATE_Start`

**多出字段** (2):
  `OtherData`, `StaticsModel`

**类型不一致** (1):
  - STAFF_ID: int→NoneType

**值不一致** (11):
  - ANALYSISRULE_ID: `` → `1,39`
  - DIALOG_CODE: `` → `1aade67c-c26a-40ed-a271-4c20af`
  - OPERATE_DATE: `2024/10/30 17:59:17` → `2026-01-26T11:22:19`
  - SENTENCE_CONTENT: `新桥` → `新桥服务区5月份营收情况\n`
  - SENTENCE_ID: 1 → 6369
  - SENTENCE_RESULT
  - SENTENCE_TYPE: 1 → 2
  - STAFF_NAME: `严琅杰` → `新项目`
  - PageSize: 99 → 10
  - TotalCount: 1 → 5899
  - ...等11处

**列表差异** (1):
  - List: 1→99

### 19. `GetShopSABFIList`

- **接口**: `Analysis/GetShopSABFIList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

---

## Audit

> 9 个接口存在差异

### 1. `GetABNORMALAUDITList`

- **接口**: `Audit/GetABNORMALAUDITList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

### 2. `GetAUDITTASKSDetail`

- **接口**: `Audit/GetAUDITTASKSDetail`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

### 3. `GetAUDITTASKSList`

- **接口**: `Audit/GetAUDITTASKSList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

### 4. `GetAbnormalAuditDetail`

- **接口**: `Audit/GetAbnormalAuditDetail`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

### 5. `GetAbnormalRateReport`

- **接口**: `Audit/GetAbnormalRateReport`
- **差异数**: 1
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

### 6. `GetCHECKACCOUNTDetail`

- **接口**: `Audit/GetCHECKACCOUNTDetail`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

### 7. `GetCHECKACCOUNTList`

- **接口**: `Audit/GetCHECKACCOUNTList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

### 8. `GetCheckAccountReport`

- **接口**: `Audit/GetCheckAccountReport`
- **差异数**: 1
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

### 9. `GetYSABNORMALITYList`

- **接口**: `Audit/GetYSABNORMALITYList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `查询成功` → `服务器内部错误`

---

## BaseInfo

> 44 个接口存在差异

### 1. `BindingOwnerUnitTree`

- **接口**: `BaseInfo/BindingOwnerUnitTree`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - children: list→NoneType
  - children: list→NoneType

### 2. `GetAUTOSTATISTICSDetail`

- **接口**: `BaseInfo/GetAUTOSTATISTICSDetail`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (1):
  `INELASTIC_DEMAND`

**类型不一致** (3):
  - AUTOSTATISTICS_DESC: NoneType→str
  - AUTOSTATISTICS_VALUE: NoneType→str
  - STATISTICS_TYPE: NoneType→int

**值不一致** (1):
  - AUTOSTATISTICS_ICO

### 3. `GetAssetsRevenueAmount`

- **接口**: `BaseInfo/GetAssetsRevenueAmount`
- **差异数**: 2
- **状态**: ⬜ 待修复

**值不一致** (1):
  - TotalCount: 1 → 0

**列表差异** (1):
  - List: 1→0

### 4. `GetBrandDetail`

- **接口**: `BaseInfo/GetBrandDetail`
- **差异数**: 16
- **状态**: ⬜ 待修复

**缺少字段** (6):
  `BUSINESSTRADE_NAME`, `MerchantID`, `MerchantID_Encrypt`, `MerchantName`, `SERVERPART_IDS`, `SPREGIONTYPE_IDS`

**类型不一致** (9):
  - BRAND_CATEGORY: int→float
  - BRAND_ID: int→float
  - BRAND_INDEX: int→float
  - BRAND_INDUSTRY: NoneType→str
  - BRAND_PID: int→float
  - BRAND_STATE: int→float
  - OWNERUNIT_ID: int→float
  - STAFF_ID: int→float
  - WECHATAPPSIGN_ID: int→float

**值不一致** (1):
  - OPERATE_DATE: `2020-04-15T21:34:06` → `2020-04-15T00:00:00`

### 5. `GetBrandList`

- **接口**: `BaseInfo/GetBrandList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `MerchantID_Encrypt`, `SERVERPART_IDS`, `SPREGIONTYPE_IDS`

**类型不一致** (12):
  - BRAND_CATEGORY: int→float
  - BRAND_ID: int→float
  - BRAND_INDEX: int→float
  - BRAND_INDUSTRY: int→str
  - BRAND_PID: int→float
  - BRAND_STATE: int→float
  - BRAND_TYPE: int→float
  - MANAGE_TYPE: int→float
  - OWNERUNIT_ID: int→float
  - PROVINCE_CODE: int→float
  - ...等12处

**值不一致** (10):
  - BUSINESSTRADE_NAME: `西式快餐` → ``
  - MerchantID: `-1115` → `-2096`
  - MerchantName: `艾比克` → `安徽艾芝餐饮管理有限责任公司`
  - OPERATE_DATE: `2023-04-17T17:27:15` → `2023-04-17T00:00:00`
  - Serverpartlabel: `釜山服务区` → `四方湖服务区`
  - Serverpartvalue: `495` → `443`
  - Serverpartlabel: `福山服务区` → `釜山服务区`
  - Serverpartvalue: `520` → `495`
  - Serverpartlabel: `四方湖服务区` → `福山服务区`
  - Serverpartvalue: `443` → `520`

### 6. `GetBusinessBrandList`

- **接口**: `BaseInfo/GetBusinessBrandList`
- **差异数**: 16
- **状态**: ⬜ 待修复

**类型不一致** (15):
  - BRAND_CATEGORY: int→float
  - BRAND_DESC: NoneType→str
  - BRAND_ID: int→float
  - BRAND_INDEX: int→float
  - BRAND_PID: int→float
  - BRAND_STATE: int→float
  - BRAND_TYPE: int→float
  - COMMISSION_RATIO: NoneType→str
  - MANAGE_TYPE: NoneType→float
  - OWNERUNIT_ID: int→float
  - ...等15处

**值不一致** (1):
  - OPERATE_DATE: `2023-04-18T09:33:35` → `2023-04-18T00:00:00`

### 7. `GetBusinessTradeDetail`

- **接口**: `BaseInfo/GetBusinessTradeDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (3):
  - AUTOSTATISTICS_DESC: NoneType→str
  - AUTOSTATISTICS_VALUE: NoneType→str
  - INELASTIC_DEMAND: NoneType→int

### 8. `GetBusinessTradeEnum`

- **接口**: `BaseInfo/GetBusinessTradeEnum`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (1):
  `desc`

### 9. `GetBusinessTradeTree`

- **接口**: `BaseInfo/GetBusinessTradeTree`
- **差异数**: 25
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - INELASTIC_DEMAND: NoneType→int

**值不一致** (24):
  - STATISTICS_TYPE: 35 → 0
  - STATISTICS_TYPE: 20 → 0
  - STATISTICS_TYPE: 11 → 0
  - STATISTICS_TYPE: 27 → 0
  - STATISTICS_TYPE: 2 → 0
  - STATISTICS_TYPE: 95 → 0
  - STATISTICS_TYPE: 66 → 0
  - STATISTICS_TYPE: 23 → 0
  - STATISTICS_TYPE: 3 → 0
  - STATISTICS_TYPE: 16 → 0
  - ...等24处

### 10. `GetCASHWORKERDetail`

- **接口**: `BaseInfo/GetCASHWORKERDetail`
- **差异数**: 6
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `OPERATE_DATE_End`, `OPERATE_DATE_Start`, `SERVERPART_CODES`, `SERVERPART_IDS`, `ServerPart_Name`

**值不一致** (1):
  - OPERATE_DATE: `2018/11/7 10:36:59` → `2018-11-07T10:36:59`

### 11. `GetCASHWORKERList`

- **接口**: `BaseInfo/GetCASHWORKERList`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `OPERATE_DATE_End`, `OPERATE_DATE_Start`, `SERVERPART_CODES`, `SERVERPART_IDS`

**值不一致** (2):
  - OPERATE_DATE: `2021/7/5 15:30:25` → `2021-07-05T15:30:25`
  - TotalCount: 1 → 2

**列表差异** (1):
  - List: 1→2

### 12. `GetCOMMODITYDetail`

- **接口**: `BaseInfo/GetCOMMODITYDetail`
- **差异数**: 24
- **状态**: ⬜ 待修复

**缺少字段** (9):
  `COMMODITY_BUSINESS_ID`, `HIGHWAYPROINST_ID`, `QUALIFICATIONList`, `QUALIFICATION_ID`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `SERVERPART_NAME`, `SHOPNAME`, `originCommodity`

**多出字段** (13):
  `COMMODITY_ALLNAME`, `COMMODITY_BRAND`, `COMMODITY_COUNT`, `COMMODITY_CURRPRICE`, `COMMODITY_FROZENCOUNT`, `COMMODITY_GROUPPRICE`, `COMMODITY_MAXPRICE`, `COMMODITY_MINPRICE`, `COMMODITY_ORIPRICE`, `COMMODITY_PROMOTIONPRICE`, `COMMODITY_SERVERCODE`, `COMMODITY_UNIFORMPRICE`, `SUPPLIER_ID`

**类型不一致** (2):
  - COMMODITY_EN: NoneType→str
  - COMMODITY_HOTKEY: NoneType→str

### 13. `GetCOMMODITYList`

- **接口**: `BaseInfo/GetCOMMODITYList`
- **差异数**: 18
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `HIGHWAYPROINST_ID`, `QUALIFICATIONList`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `originCommodity`

**多出字段** (13):
  `COMMODITY_ALLNAME`, `COMMODITY_BRAND`, `COMMODITY_COUNT`, `COMMODITY_CURRPRICE`, `COMMODITY_FROZENCOUNT`, `COMMODITY_GROUPPRICE`, `COMMODITY_MAXPRICE`, `COMMODITY_MINPRICE`, `COMMODITY_ORIPRICE`, `COMMODITY_PROMOTIONPRICE`, `COMMODITY_SERVERCODE`, `COMMODITY_UNIFORMPRICE`, `SUPPLIER_ID`

### 14. `GetCOMMODITYTYPEDetail`

- **接口**: `BaseInfo/GetCOMMODITYTYPEDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (3):
  - COMMODITYTYPE_EN: NoneType→str
  - COMMODITYTYPE_ID: int→float
  - STAFF_NAME: NoneType→str

### 15. `GetCOMMODITYTYPEList`

- **接口**: `BaseInfo/GetCOMMODITYTYPEList`
- **差异数**: 1
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - COMMODITYTYPE_ID: int→float

### 16. `GetCombineBrandList`

- **接口**: `BaseInfo/GetCombineBrandList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (9):
  `BRAND_TYPENAME`, `BUSINESS_TRADE`, `COMMISSION_RATIO`, `MerchantName`, `REVENUE_AMOUNT`, `REVENUE_DAILYAMOUNT`, `ROYALTY_PRICE`, `SETTLEMENT_MODES`, `WECHATAPP_APPID`

**类型不一致** (10):
  - BRAND_CATEGORY: int→float
  - BRAND_DESC: NoneType→str
  - BRAND_ID: int→float
  - BRAND_INDEX: int→float
  - BRAND_PID: int→float
  - BRAND_STATE: int→float
  - BusinessState: int→NoneType
  - OWNERUNIT_ID: int→float
  - PROVINCE_CODE: int→float
  - STAFF_ID: int→float

**值不一致** (6):
  - BRAND_INDUSTRY: `244` → `243`
  - BRAND_INTRO
  - BRAND_NAME: `驿达万佳生活馆` → `刘鸿盛`
  - BRAND_TYPE: `2000` → `2000.0`
  - BUSINESSTRADE_NAME: `商超零售` → `地方特色小吃`
  - OPERATE_DATE: `2023-04-18T09:33:35` → `2021-02-03T00:00:00`

### 17. `GetNestingCOMMODITYTYPEList`

- **接口**: `BaseInfo/GetNestingCOMMODITYTYPEList`
- **差异数**: 3
- **状态**: ⬜ 待修复

**值不一致** (2):
  - PageSize: 10 → 0
  - TotalCount: 10 → 0

**列表差异** (1):
  - List: 10→0

### 18. `GetNestingCOMMODITYTYPETree`

- **接口**: `BaseInfo/GetNestingCOMMODITYTYPETree`
- **差异数**: 3
- **状态**: ⬜ 待修复

**值不一致** (2):
  - PageSize: 10 → 0
  - TotalCount: 10 → 0

**列表差异** (1):
  - List: 10→0

### 19. `GetOWNERUNITDetail`

- **接口**: `BaseInfo/GetOWNERUNITDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (3):
  - OWNERUNIT_DESC: NoneType→str
  - OWNERUNIT_EN: NoneType→str
  - OWNERUNIT_ICO: NoneType→str

### 20. `GetPROPERTYASSETSDetail`

- **接口**: `BaseInfo/GetPROPERTYASSETSDetail`
- **差异数**: 6
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `PROPERTYASSETS_IDS`, `PROPERTYASSETS_TYPES`, `PropertyShop`, `SERVERPART_IDS`

**类型不一致** (2):
  - PROPERTYASSETS_REGION: int→float
  - PROPERTYASSETS_TYPE: int→float

### 21. `GetPROPERTYASSETSList`

- **接口**: `BaseInfo/GetPROPERTYASSETSList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSPROJECT_ID`, `BUSINESSPROJECT_NAME`, `COMPACT_NAME`, `PROJECT_ENDDATE`, `PROJECT_STARTDATE`, `PROJECT_VALID`, `PROPERTYASSETS_IDS`, `PROPERTYASSETS_TYPES`, `REGISTERCOMPACT_ID`, `SERVERPART_IDS`, `SPREGIONTYPE_ID`, `SPREGIONTYPE_INDEX`, `SPREGIONTYPE_NAME`, `TOTAL_AREA`

**值不一致** (11):
  - BUSINESS_STATE: 1000 → 3000
  - CREATE_DATE: `2024-07-30T14:48:11` → `2024-08-13T15:59:16`
  - OPERATE_DATE: `2024-08-01T10:31:10` → `2024-08-13T15:59:16`
  - OPERATOR_ID: 2785 → 3595
  - OPERATOR_NAME: `严琅杰` → `苹果测试机`
  - PROPERTYASSETS_AREA
  - PROPERTYASSETS_CODE: `XQ-01` → `123`
  - PROPERTYASSETS_DESC: `测试备注` → ``
  - PROPERTYASSETS_ID: 1 → 79
  - PROPERTYASSETS_INFO: `测试说明信息` → ``
  - ...等11处

### 22. `GetPROPERTYASSETSTreeList`

- **接口**: `BaseInfo/GetPROPERTYASSETSTreeList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (18):
  `children`, `BUSINESSPROJECT_ID`, `BUSINESSPROJECT_NAME`, `BUSINESS_STATE`, `COMPACT_NAME`, `PROJECT_ENDDATE`, `PROJECT_STARTDATE`, `PROJECT_VALID`, `PROPERTYASSETS_IDS`, `PROPERTYASSETS_TYPES`, `REGISTERCOMPACT_ID`, `SERVERPARTSHOP_ID`, `SERVERPART_IDS`, `SHOPNAME`, `SPREGIONTYPE_ID` 等18个

**类型不一致** (5):
  - CREATE_DATE: NoneType→str
  - EXTENDJSON: NoneType→str
  - OPERATE_DATE: NoneType→str
  - OPERATOR_ID: NoneType→int
  - OPERATOR_NAME: NoneType→str

**值不一致** (1):
  - PROPERTYASSETS_AREA

**列表差异** (1):
  - children: 2→9

### 23. `GetPROPERTYSHOPDetail`

- **接口**: `BaseInfo/GetPROPERTYSHOPDetail`
- **差异数**: 22
- **状态**: ⬜ 待修复

**缺少字段** (13):
  `ENDDATE_End`, `ENDDATE_Start`, `PROPERTYASSETS_IDS`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `STARTDATE_End`, `STARTDATE_Start`, `ServerpartShop.BANK_ACCOUNT`, `ServerpartShop.BANK_NAME`, `ServerpartShop.PROVINCE_CODE`, `ServerpartShop.SERVERPARTSHOP_IDS`, `ServerpartShop.SERVERPART_IDS`, `ServerpartShop.TAXPAYER_IDENTIFYCODE`

**多出字段** (1):
  `ServerpartShop.COMMISSION_TYPE`

**类型不一致** (8):
  - ServerpartShop.BUSINESS_UNIT: NoneType→str
  - ServerpartShop.BUS_STARTDATE: NoneType→str
  - ServerpartShop.LINKMAN: NoneType→str
  - ServerpartShop.LINKMAN_MOBILE: NoneType→str
  - ServerpartShop.REGISTERCOMPACT_NAME: NoneType→str
  - ServerpartShop.SERVERPARTSHOP_DESC: NoneType→str
  - ServerpartShop.TOPPERSON: NoneType→str
  - ServerpartShop.TOPPERSON_MOBILE: NoneType→str

### 24. `GetPROPERTYSHOPList`

- **接口**: `BaseInfo/GetPROPERTYSHOPList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (7):
  `ENDDATE_End`, `ENDDATE_Start`, `PROPERTYASSETS_IDS`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `STARTDATE_End`, `STARTDATE_Start`

### 25. `GetRTSERVERPARTSHOPDetail`

- **接口**: `BaseInfo/GetRTSERVERPARTSHOPDetail`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `BUSINESS_TYPES`, `SERVERPARTSHOP_IDS`

**值不一致** (3):
  - BUSINESS_DATE: `2019/3/28 0:00:00` → `2019-03-28T00:00:00`
  - BUSINESS_ENDDATE: `2022/8/18 0:00:00` → `2022-08-18T00:00:00`
  - OPERATE_DATE: `2022/8/31 14:38:39` → `2022-08-31T14:38:39`

### 26. `GetRTSERVERPARTSHOPList`

- **接口**: `BaseInfo/GetRTSERVERPARTSHOPList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `BUSINESS_TYPES`, `SERVERPARTSHOP_IDS`

**值不一致** (2):
  - BUSINESS_DATE: `2020/4/12 0:00:00` → `2020-04-12T00:00:00`
  - OPERATE_DATE: `2020/4/10 19:10:50` → `2020-04-10T19:10:50`

### 27. `GetSERVERPARTCRTDetail`

- **接口**: `BaseInfo/GetSERVERPARTCRTDetail`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (7):
  `SERVERPART_CODES`, `SERVERPART_IDS`, `SERVERPART_INDEX`, `SERVERPART_NAME`, `SPREGIONTYPE_ID`, `SPREGIONTYPE_INDEX`, `SPREGIONTYPE_NAME`

### 28. `GetSERVERPARTCRTList`

- **接口**: `BaseInfo/GetSERVERPARTCRTList`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (7):
  `SERVERPART_CODES`, `SERVERPART_IDS`, `SERVERPART_INDEX`, `SERVERPART_NAME`, `SPREGIONTYPE_ID`, `SPREGIONTYPE_INDEX`, `SPREGIONTYPE_NAME`

### 29. `GetSERVERPARTCRTTreeList`

- **接口**: `BaseInfo/GetSERVERPARTCRTTreeList`
- **差异数**: 23
- **状态**: ⬜ 待修复

**缺少字段** (20):
  `children`, `SERVERPART_CODES`, `SERVERPART_IDS`, `SERVERPART_INDEX`, `ACCOUNTBODY_CODE`, `ACCOUNTBODY_NAME`, `ACCOUNTTAX`, `COSTCENTER_CODE`, `COSTCENTER_NAME`, `DEPARTMENT_CODE`, `OPERATE_DATE`, `PROPERTYTAX`, `RESPONSIBLEDEP_CODE`, `SERVERPARTCRT_ID`, `SERVERPART_CODE` 等20个

### 30. `GetSERVERPARTDetail`

- **接口**: `BaseInfo/GetSERVERPARTDetail`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `SERVERPART_CODES`, `SERVERPART_IDS`, `ServerPartInfo.SERVERPART_IDS`

**多出字段** (14):
  `ServerPartInfo.BABY_COT`, `ServerPartInfo.CHANGING_TABLE`, `ServerPartInfo.DROOMWATER_DISPENSER`, `ServerPartInfo.HASGASSTATION`, `ServerPartInfo.HASRESTROOM`, `ServerPartInfo.MABROOMWATER_DISPENSER`, `ServerPartInfo.NURSING_TABLE`, `ServerPartInfo.REFUELINGGUN98`, `ServerPartInfo.REPAIR_TEL`, `ServerPartInfo.REPAIR_TIME`, `ServerPartInfo.SHOWERROOM`, `ServerPartInfo.SLEEPCABIN_PRICE`, `ServerPartInfo.TOILET_PAPER`, `ServerPartInfo.UREA_COUNT`

**类型不一致** (6):
  - HKBL: NoneType→str
  - REGIONTYPE_NAME: NoneType→str
  - SELLERCOUNT: int→float
  - SERVERPART_DESC: NoneType→str
  - SERVERPART_IPADDRESS: NoneType→str
  - SHORTNAME: NoneType→str

**值不一致** (2):
  - SERVERPART_X
  - SERVERPART_Y

### 31. `GetSERVERPARTList`

- **接口**: `BaseInfo/GetSERVERPARTList`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `RtServerPart`, `SERVERPART_CODES`, `SERVERPART_IDS`, `ServerPartInfo`

**类型不一致** (1):
  - SELLERCOUNT: int→float

**值不一致** (2):
  - SERVERPART_X
  - SERVERPART_Y

### 32. `GetSERVERPARTSHOP_LOGList`

- **接口**: `BaseInfo/GetSERVERPARTSHOP_LOGList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `OPERATE_DATE_End`, `OPERATE_DATE_Start`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `SHOPTRADES`

**值不一致** (4):
  - OPERATE_DATE: `2021/6/25 18:40:01` → `2021-06-25T18:40:01`
  - OPERATE_DATE: `2021/2/2 0:04:09` → `2021-02-02T00:04:09`
  - OPERATE_DATE: `2021/2/2 0:04:09` → `2021-02-02T00:04:09`
  - OPERATE_DATE: `2021/2/2 0:15:44` → `2021-02-02T00:15:44`

### 33. `GetSPRegionShopTree`

- **接口**: `BaseInfo/GetSPRegionShopTree`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `desc`, `ico`

### 34. `GetServerPartShopNewDetail`

- **接口**: `BaseInfo/GetServerPartShopNewDetail`
- **差异数**: 24
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `ServerPartShop.PROVINCE_CODE`, `ServerPartShop.SERVERPARTSHOP_IDS`, `ServerPartShop.SERVERPART_IDS`

**多出字段** (1):
  `ServerPartShop.COMMISSION_TYPE`

**类型不一致** (8):
  - ServerPartShop.BANK_ACCOUNT: NoneType→str
  - ServerPartShop.BANK_NAME: NoneType→str
  - ShopBusinessStateBankAccount: NoneType→str
  - ShopBusinessStateBankName: NoneType→str
  - ShopBusinessStateTaxPayerIdEntityCode: NoneType→str
  - ShopBusinessStateBankAccount: NoneType→str
  - ShopBusinessStateBankName: NoneType→str
  - ShopBusinessStateTaxPayerIdEntityCode: NoneType→str

**值不一致** (12):
  - RtServerPartShopBusinessEndDate: `2022年7月21日` → `2022年7月20日`
  - RtServerPartShopBusinessEndDate: `2022年7月7日` → `2022年7月6日`
  - RtServerPartShopBusinessEndDate: `2022年7月6日` → `2022年7月5日`
  - RtServerPartShopBusinessEndDate: `2022年4月30日` → `2022年4月29日`
  - RtServerPartShopBusinessEndDate: `2022年4月28日` → `2022年4月27日`
  - RtServerPartShopBusinessEndDate: `2022年4月13日` → `2022年4月12日`
  - RtServerPartShopOperateDate: `2022/9/17 23:01:46` → `2022/9/17 23:1:46`
  - RtServerPartShopBusinessEndDate: `2022年9月15日` → `2022年9月14日`
  - RtServerPartShopOperateDate: `2022/9/16 20:46:02` → `2022/9/16 20:46:2`
  - RtServerPartShopBusinessEndDate: `2022年4月30日` → `2022年4月29日`
  - ...等12处

### 35. `GetServerPartShopNewList`

- **接口**: `BaseInfo/GetServerPartShopNewList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (10):
  `BUSINESS_BRAND`, `BUSINESS_DATE`, `BUSINESS_TRADE`, `BUS_STARTDATE`, `LINKMAN`, `LINKMAN_MOBILE`, `OPERATE_DATE`, `OWNERUNIT_ID`, `OWNERUNIT_NAME`, `SELLER_ID`

**多出字段** (13):
  `EXPRESSWAY_NAME`, `FIELDENUM_ID`, `REGIONTYPE_ID`, `REGISTERCOMPACT_NAME`, `SERVERPART_ADDRESS`, `SERVERPART_INDEX`, `SERVERPART_TYPE`, `SERVERPART_X`, `SERVERPART_Y`, `SPREGIONTYPE_ID`, `SPREGIONTYPE_INDEX`, `SPREGIONTYPE_NAME`, `TRANSFER_TYPE`

**值不一致** (1):
  - BRAND_NAME: `自营客房` → `加油站便利店`

**列表差异** (1):
  - List: 29→38

### 36. `GetServerpartShopDetail`

- **接口**: `BaseInfo/GetServerpartShopDetail`
- **差异数**: 12
- **状态**: ⬜ 待修复

**缺少字段** (6):
  `BANK_ACCOUNT`, `BANK_NAME`, `PROVINCE_CODE`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `TAXPAYER_IDENTIFYCODE`

**多出字段** (1):
  `COMMISSION_TYPE`

**类型不一致** (5):
  - BUS_STARTDATE: NoneType→str
  - LINKMAN: NoneType→str
  - LINKMAN_MOBILE: NoneType→str
  - REGISTERCOMPACT_NAME: NoneType→str
  - SERVERPARTSHOP_DESC: NoneType→str

### 37. `GetServerpartShopInfo`

- **接口**: `BaseInfo/GetServerpartShopInfo`
- **差异数**: 19
- **状态**: ⬜ 待修复

**缺少字段** (19):
  `Business_BrandIcon`, `Business_BrandName`, `Business_State`, `Business_TradeName`, `Business_Type`, `InSalesType`, `OwnerUnit_Id`, `OwnerUnit_Name`, `ServerpartShopId`, `ServerpartShop_Code`, `ServerpartShop_Name`, `ServerpartShop_Region`, `ServerpartShop_ShortName`, `ServerpartShop_State`, `ServerpartShop_Trade` 等19个

### 38. `GetServerpartShopList`

- **接口**: `BaseInfo/GetServerpartShopList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**值不一致** (1):
  - TotalCount: 69 → 0

**列表差异** (1):
  - List: 69→0

### 39. `GetServerpartShopTree`

- **接口**: `BaseInfo/GetServerpartShopTree`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `desc`, `ico`

### 40. `GetServerpartUDTypeTree`

- **接口**: `BaseInfo/GetServerpartUDTypeTree`
- **差异数**: 25
- **状态**: ⬜ 待修复

**值不一致** (24):
  - key: `2-9475` → `2-1019`
  - label: `【361度】衣服` → `新桥服务区`
  - value: 9475 → 1019
  - key: `2-9476` → `2-1021`
  - label: `【361度】裤子` → `猫屎咖啡`
  - value: 9476 → 1021
  - key: `2-9477` → `2-1022`
  - label: `【361度】鞋子` → `精品咖啡`
  - value: 9477 → 1022
  - key: `2-9478` → `2-1023`
  - ...等24处

**列表差异** (1):
  - children: 99→114

### 41. `GetShopReceivables`

- **接口**: `BaseInfo/GetShopReceivables`
- **差异数**: 25
- **状态**: ⬜ 待修复

**值不一致** (25):
  - PROJECT_ENDDATE: `2024/1/31` → `2024-01-31T00:00:00`
  - PROJECT_STARTDATE: `2021/2/1` → `2021-02-01T00:00:00`
  - PROJECT_ENDDATE: `2028/1/13` → `2028-01-13T00:00:00`
  - PROJECT_STARTDATE: `2025/1/14` → `2025-01-14T00:00:00`
  - PROJECT_ENDDATE: `2024/1/31` → `2024-01-31T00:00:00`
  - PROJECT_STARTDATE: `2021/2/1` → `2021-02-01T00:00:00`
  - PROJECT_ENDDATE: `2028/7/14` → `2028-07-14T00:00:00`
  - PROJECT_STARTDATE: `2025/7/15` → `2025-07-15T00:00:00`
  - SERVERPARTSHOP_ID: `7105,7104` → `7104,7105`
  - BUSINESSPROJECT_ICO
  - ...等25处

### 42. `GetTradeBrandTree`

- **接口**: `BaseInfo/GetTradeBrandTree`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `BrandTreeBrand_ICO`, `BrandTreeBrand_ID`, `BrandTreeBrand_Name`, `BrandTreeBrand_Type`

**多出字段** (4):
  `BrandTreeBRAND_ID`, `BrandTreeBRAND_INTRO`, `BrandTreeBRAND_NAME`, `BrandTreeBRAND_STATE`

**类型不一致** (1):
  - children: NoneType→list

### 43. `GetUSERDEFINEDTYPEDetail`

- **接口**: `BaseInfo/GetUSERDEFINEDTYPEDetail`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `SERVERPARTCODES`, `ShopNames`

**多出字段** (16):
  `GOODSTYPE`, `MERCHANTS_ID`, `MERCHANTS_NAME`, `OWNERUNIT_ID`, `OWNERUNIT_NAME`, `PRESALE_ENDTIME`, `PRESALE_STARTTIME`, `PRESALE_TYPE`, `PROVINCE_CODE`, `SERVERPART_NAME`, `SHOPCODE`, `SHOPNAME`, `USERDEFINEDTYPE_ICO`, `WECHATAPPSIGN_ID`, `WECHATAPPSIGN_NAME` 等16个

**类型不一致** (4):
  - BUSINESSTYPE: int→NoneType
  - SCANCODE_ORDER: int→NoneType
  - SERVERPARTSHOP_ID: int→str
  - SERVERPART_ID: int→str

**值不一致** (3):
  - OPERATE_DATE: `2018/11/20 16:14:29` → `2019-09-30T16:00:24`
  - SERVERPARTCODE: `620036` → `888888`
  - STAFF_ID: 2 → 1

### 44. `GetUSERDEFINEDTYPEList`

- **接口**: `BaseInfo/GetUSERDEFINEDTYPEList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `SERVERPARTCODES`, `ShopNames`

**多出字段** (16):
  `GOODSTYPE`, `MERCHANTS_ID`, `MERCHANTS_NAME`, `OWNERUNIT_ID`, `OWNERUNIT_NAME`, `PRESALE_ENDTIME`, `PRESALE_STARTTIME`, `PRESALE_TYPE`, `PROVINCE_CODE`, `SERVERPART_NAME`, `SHOPCODE`, `SHOPNAME`, `USERDEFINEDTYPE_ICO`, `WECHATAPPSIGN_ID`, `WECHATAPPSIGN_NAME` 等16个

**类型不一致** (3):
  - BUSINESSTYPE: int→NoneType
  - SERVERPARTSHOP_ID: NoneType→str
  - SERVERPART_ID: int→str

**值不一致** (4):
  - OPERATE_DATE: `2020/4/28 13:41:05` → `2019-06-23T17:54:27`
  - SERVERPARTCODE: `141010` → `331010`
  - STAFF_ID: 268 → 1835
  - STAFF_NAME: `山西管理账号` → `中餐公司`

---

## BigData

> 11 个接口存在差异

### 1. `GetBAYONETDAILY_AHList`

- **接口**: `BigData/GetBAYONETDAILY_AHList`
- **差异数**: 10
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `INOUT_TYPES`, `SERVERPART_IDS`, `STATISTICS_DATE_End`, `STATISTICS_DATE_Start`, `VEHICLE_TYPES`

**多出字段** (3):
  `AVGSTAY_TIMES`, `STAY_TIMES`, `STAY_TIMESCOUNT`

**类型不一致** (2):
  - OPERATE_DATE: str→int
  - STATISTICS_DATE: str→int

### 2. `GetBAYONETWARNINGList`

- **接口**: `BigData/GetBAYONETWARNINGList`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `SERVERPART_IDS`, `SERVERPART_REGIONS`, `STATISTICS_DATE_End`, `STATISTICS_DATE_Start`

**类型不一致** (1):
  - STATISTICS_DATE: str→int

### 3. `GetBayonetOwnerAHList`

- **接口**: `BigData/GetBayonetOwnerAHList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `成功` → `服务器内部错误`

### 4. `GetBayonetOwnerMonthAHList`

- **接口**: `BigData/GetBayonetOwnerMonthAHList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (1):
  `Message`

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 999
  - Result_Desc: `成功` → `服务器内部错误`

### 5. `GetDailyBayonetAnalysis`

- **接口**: `BigData/GetDailyBayonetAnalysis`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 6. `GetSECTIONFLOWDetail`

- **接口**: `BigData/GetSECTIONFLOWDetail`
- **差异数**: 8
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `SERVERPART_IDS`, `STATISTICS_DATE_End`, `STATISTICS_DATE_Start`, `Serverpart_Flow_Analog`

**多出字段** (3):
  `AVGENTRY_RATE`, `AVGSTAY_TIMES`, `SERVERPART_FLOW_ANALOG`

**类型不一致** (1):
  - STATISTICS_DATE: str→int

### 7. `GetSECTIONFLOWList`

- **接口**: `BigData/GetSECTIONFLOWList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `SERVERPART_IDS`, `STATISTICS_DATE_End`, `STATISTICS_DATE_Start`, `Serverpart_Flow_Analog`

**多出字段** (3):
  `AVGENTRY_RATE`, `AVGSTAY_TIMES`, `SERVERPART_FLOW_ANALOG`

**类型不一致** (3):
  - STATISTICS_DATE: str→int
  - STATISTICS_DATE: str→int
  - STATISTICS_DATE: str→int

### 8. `GetSECTIONFLOWMONTHDetail`

- **接口**: `BigData/GetSECTIONFLOWMONTHDetail`
- **差异数**: 21
- **状态**: ⬜ 待修复

**缺少字段** (21):
  `HOLIDAY_TYPE`, `LARGEVEHICLE_COUNT`, `MEDIUMVEHICLE_COUNT`, `MINVEHICLE_COUNT`, `NEWENERGYVEHICLE_COUNT`, `OPERATE_DATE`, `SECTIONFLOWMONTH_ID`, `SECTIONFLOWMONTH_STATE`, `SECTIONFLOW_DAYS`, `SECTIONFLOW_DESC`, `SECTIONFLOW_NUM`, `SERVERPART_FLOW`, `SERVERPART_ID`, `SERVERPART_IDS`, `SERVERPART_NAME` 等21个

### 9. `GetSECTIONFLOWMONTHList`

- **接口**: `BigData/GetSECTIONFLOWMONTHList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `SERVERPART_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`

**类型不一致** (5):
  - STATISTICS_MONTH: str→int
  - STATISTICS_MONTH: str→int
  - STATISTICS_MONTH: str→int
  - STATISTICS_MONTH: str→int
  - STATISTICS_MONTH: str→int

**值不一致** (5):
  - OPERATE_DATE: `2024//4//2 4 :14::0` → `2024-04-24T14:02:15`
  - OPERATE_DATE: `2024//4//2 4 :14::0` → `2024-04-24T14:02:15`
  - OPERATE_DATE: `2024//4//2 4 :14::0` → `2024-04-24T14:02:15`
  - OPERATE_DATE: `2024//4//2 4 :14::0` → `2024-04-24T14:02:15`
  - OPERATE_DATE: `2024//4//2 4 :14::0` → `2024-04-24T14:02:15`

### 10. `GetServerpartSectionFlow`

- **接口**: `BigData/GetServerpartSectionFlow`
- **差异数**: 25
- **状态**: ⬜ 待修复

**多出字段** (3):
  `OtherData`, `StaticsModel`, `list.SERVERPART.DATE_COUNT`

**类型不一致** (12):
  - list.SERVERPART.VEHICLE_COUNT: float→int
  - list.SERVERPART.VEHICLE_COUNT_DXC: float→int
  - list.SERVERPART.VEHICLE_COUNT_XXC: float→int
  - list.SERVERPART.VEHICLE_COUNT_ZXC: float→int
  - list.SERVERPART.VEHICLE_COUNT: float→int
  - list.SERVERPART.VEHICLE_COUNT_DXC: float→int
  - list.SERVERPART.VEHICLE_COUNT_XXC: float→int
  - list.SERVERPART.VEHICLE_COUNT_ZXC: float→int
  - list.SERVERPART.VEHICLE_COUNT: float→int
  - list.SERVERPART.VEHICLE_COUNT_DXC: float→int
  - ...等12处

**值不一致** (8):
  - STATISTICS_DATE: `2023-08` → `202112`
  - list.SERVERPART.REVENUE_AMOUNT
  - list.SERVERPART.STATISTICS_DATE: `2023-08` → `202112`
  - list.SERVERPART.REVENUE_AMOUNT
  - list.SERVERPART.STATISTICS_DATE: `2023-08` → `202112`
  - STATISTICS_DATE: `2024-02` → `202201`
  - list.SERVERPART.REVENUE_AMOUNT
  - list.SERVERPART.STATISTICS_DATE: `2024-02` → `202201`

### 11. `GetTimeIntervalList`

- **接口**: `BigData/GetTimeIntervalList`
- **差异数**: 10
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `Data`, `Name`

**多出字段** (6):
  `OtherData`, `StaticsModel`, `SERVERPART_ID`, `SERVERPART_NAME`, `STATISTICS_HOUR`, `VEHICLE_COUNT`

**值不一致** (1):
  - TotalCount: 1 → 24

**列表差异** (1):
  - List: 1→24

---

## BusinessMan

> 1 个接口存在差异

### 1. `GetUserList`

- **接口**: `BusinessMan/GetUserList`
- **差异数**: 24
- **状态**: ⬜ 待修复

**类型不一致** (24):
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - USER_ID_Encrypted: str→NoneType
  - ...等24处

---

## BusinessProject

> 39 个接口存在差异

### 1. `GetAPPROVEDList`

- **接口**: `BusinessProject/GetAPPROVEDList`
- **差异数**: 6
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `APPROVED_DATE_End`, `APPROVED_DATE_Start`, `APPROVED_TYPES`, `TABLE_IDS`

**多出字段** (1):
  `CONTRACTPROINST_ID`

**类型不一致** (1):
  - APPROVED_DATE: str→float

### 2. `GetAccountWarningList`

- **接口**: `BusinessProject/GetAccountWarningList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (17):
  `BUSINESS_ENDDATE`, `BUSINESS_STARTDATE`, `BUSINESS_TRADE`, `Brand_ICO`, `CA_COST`, `GUARANTEERATIO`, `MERCHANTS_ID_Encrypted`, `PROFIT_AVG`, `PROFIT_RATE`, `PROFIT_SD`, `PaymentProgress`, `ProjectProgress`, `ROYALTY_PRICE`, `SPREGIONTYPE_ID`, `SPREGIONTYPE_NAME` 等17个

**多出字段** (2):
  `ACCOUNTWARNING_ID`, `RECORD_DATE`

**类型不一致** (3):
  - ACTUAL_RATIO: NoneType→float
  - COMMISSION_RATIO: NoneType→float
  - COST_AMOUNT: NoneType→float

**值不一致** (3):
  - BUSINESSPROJECT_ID: 32 → 1508
  - BUSINESSPROJECT_NAME: `新桥服务区（中式餐饮）项目` → `新桥三河米饺合同项目`
  - BUSINESS_STATE: 3000 → 1000

### 3. `GetAccountWarningListSummary`

- **接口**: `BusinessProject/GetAccountWarningListSummary`
- **差异数**: 9
- **状态**: ⬜ 待修复

**值不一致** (9):
  - value: 103 → 158
  - value: 5 → 4
  - value: 35 → 50
  - value: 8 → 56
  - value: 54 → 48
  - label: `保底提成过高` → `租金提成过高`
  - value: 119 → 101
  - label: `业态缺失告警` → `保底偏低预警`
  - value: 40 → 35

### 4. `GetAnnualSplit`

- **接口**: `BusinessProject/GetAnnualSplit`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSPROJECT_NAME`, `BUSINESS_ENDDATE`, `BUSINESS_PERIOD`, `BUSINESS_STARTDATE`, `BUSINESS_STATE`, `CLOSED_DATE`, `DAILY_AMOUNT`, `EXPENSE_TYPE`, `MERCHANTS_NAME`, `MERCHANT_PAYMENT`, `OTHER_EXPENSE`, `PERIOD_INDEX`, `PROPERTY_FEE`, `WATERELECTRIC_EXPENSE`

**多出字段** (11):
  `ACCCASHPAY_CORRECT`, `ACCCIGARETTE_AMOUNT`, `ACCMOBILEPAY_CORRECT`, `ACCOUNT_TYPE`, `ACCREVENUE_AMOUNT`, `ACCROYALTY_PRICE`, `ACCROYALTY_THEORY`, `ACCSUBROYALTY_PRICE`, `ACCSUBROYALTY_THEORY`, `ACCTICKET_FEE`, `BIZPSPLITMONTH_ID`

### 5. `GetBIZPSPLITMONTHDetail`

- **接口**: `BusinessProject/GetBIZPSPLITMONTHDetail`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `Approvalstate`, `BIZPSPLITMONTH_IDS`, `SHOPROYALTY_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`

### 6. `GetBIZPSPLITMONTHList`

- **接口**: `BusinessProject/GetBIZPSPLITMONTHList`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `Approvalstate`, `BIZPSPLITMONTH_IDS`, `SHOPROYALTY_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`

### 7. `GetBUSINESSPROJECTSPLITDetail`

- **接口**: `BusinessProject/GetBUSINESSPROJECTSPLITDetail`
- **差异数**: 24
- **状态**: ⬜ 待修复

**缺少字段** (21):
  `ACCOUNT_AMOUNT`, `BUSINESSPROJECT_IDS`, `CURCASHPAY_AMOUNT`, `CURMOBILEPAY_AMOUNT`, `CURROYALTY_PRICE`, `CURSUBROYALTY_PRICE`, `CURTICKET_FEE`, `CalcAccumulate`, `CalcExpiredDays`, `CompleteState`, `ENDDATE_End`, `ENDDATE_Start`, `ExpenseAmount`, `ExpenseList`, `LogList` 等21个

**类型不一致** (3):
  - ENDDATE: str→int
  - STARTDATE: str→int
  - STATISTICS_DATE: str→int

### 8. `GetBUSINESSPROJECTSPLITList`

- **接口**: `BusinessProject/GetBUSINESSPROJECTSPLITList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (22):
  `OtherData`, `ACCOUNT_AMOUNT`, `BUSINESSPROJECT_IDS`, `CURCASHPAY_AMOUNT`, `CURMOBILEPAY_AMOUNT`, `CURROYALTY_PRICE`, `CURSUBROYALTY_PRICE`, `CURTICKET_FEE`, `CalcAccumulate`, `CalcExpiredDays`, `CompleteState`, `ENDDATE_End`, `ENDDATE_Start`, `ExpenseAmount`, `ExpenseList` 等22个

**类型不一致** (3):
  - ENDDATE: str→int
  - STARTDATE: str→int
  - STATISTICS_DATE: str→int

### 9. `GetBrandReceivables`

- **接口**: `BusinessProject/GetBrandReceivables`
- **差异数**: 4
- **状态**: ⬜ 待修复

**值不一致** (2):
  - PageSize: 10 → 999
  - TotalCount: 26 → 0

**列表差异** (2):
  - List: 26→0
  - OtherData: 11→0

### 10. `GetBusinessPaymentDetail`

- **接口**: `BusinessProject/GetBusinessPaymentDetail`
- **差异数**: 4
- **状态**: ⬜ 待修复

**多出字段** (3):
  `BUSINESS_TRADE`, `BUSINESS_TRADENAME`, `SERVERPART_TYPE`

**类型不一致** (1):
  - BUSINESSPAYMENT_DESC: NoneType→str

### 11. `GetBusinessPaymentList`

- **接口**: `BusinessProject/GetBusinessPaymentList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**多出字段** (3):
  `BUSINESS_TRADE`, `BUSINESS_TRADENAME`, `SERVERPART_TYPE`

**类型不一致** (7):
  - OPERATE_DATE: int→NoneType
  - GUARANTEERATIO: float→NoneType
  - OPERATE_DATE: int→NoneType
  - OPERATE_DATE: int→NoneType
  - OPERATE_DATE: int→NoneType
  - OPERATE_DATE: int→NoneType
  - OPERATE_DATE: int→NoneType

### 12. `GetBusinessProjectDetail`

- **接口**: `BusinessProject/GetBusinessProjectDetail`
- **差异数**: 16
- **状态**: ⬜ 待修复

**缺少字段** (16):
  `BUSINESSPROJECT_IDS`, `CLOSED_DATE_End`, `CLOSED_DATE_Start`, `DueDate_End`, `DueDate_Start`, `EXPIREDAYS`, `LogList`, `MerchantsIdEncrypted`, `Period_AvgAmount`, `Period_Count`, `ProjectStateSearch`, `ProjectTypeSearch`, `Project_ICO`, `ROYALTY_PRICE`, `ShowShare` 等16个

### 13. `GetBusinessProjectList`

- **接口**: `BusinessProject/GetBusinessProjectList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSPROJECT_IDS`, `CLOSED_DATE_End`, `CLOSED_DATE_Start`, `DueDate_End`, `DueDate_Start`, `EXPIREDAYS`, `LogList`, `MerchantsIdEncrypted`, `ProjectStateSearch`, `ProjectTypeSearch`, `Project_ICO`, `ROYALTY_PRICE`, `ShowShare`, `SwitchLogList`

**类型不一致** (1):
  - Period_Count: float→int

### 14. `GetExpenseSummary`

- **接口**: `BusinessProject/GetExpenseSummary`
- **差异数**: 11
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `children`, `node`

**多出字段** (6):
  `BUSINESS_UNIT`, `SERVERPARTSHOP_ID`, `SERVERPARTSHOP_NAME`, `SHOPEXPENSE_AMOUNT`, `SHOPEXPENSE_TYPE`, `STATISTICS_MONTH`

**值不一致** (1):
  - TotalCount: 137 → 690

**列表差异** (2):
  - List: 1→690
  - OtherData: 5→0

### 15. `GetMerchantSplit`

- **接口**: `BusinessProject/GetMerchantSplit`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSPROJECT_NAME`, `BUSINESS_ENDDATE`, `BUSINESS_PERIOD`, `BUSINESS_STARTDATE`, `BUSINESS_STATE`, `CLOSED_DATE`, `DAILY_AMOUNT`, `EXPENSE_TYPE`, `MERCHANTS_NAME`, `MERCHANT_PAYMENT`, `OTHER_EXPENSE`, `PERIOD_INDEX`, `PROPERTY_FEE`, `WATERELECTRIC_EXPENSE`

**多出字段** (10):
  `ACCCASHPAY_CORRECT`, `ACCCIGARETTE_AMOUNT`, `ACCMOBILEPAY_CORRECT`, `ACCOUNT_TYPE`, `ACCREVENUE_AMOUNT`, `ACCROYALTY_PRICE`, `ACCROYALTY_THEORY`, `ACCSUBROYALTY_PRICE`, `ACCSUBROYALTY_THEORY`, `ACCTICKET_FEE`

**列表差异** (1):
  - List: 4→91

### 16. `GetMerchantsReceivables`

- **接口**: `BusinessProject/GetMerchantsReceivables`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: NoneType→dict

**值不一致** (2):
  - Result_Code: 200 → 100
  - Result_Desc: `查询失败，请传入经营商户内码或门店内码集合！` → `查询成功`

### 17. `GetMerchantsReceivablesList`

- **接口**: `BusinessProject/GetMerchantsReceivablesList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (8):
  `ACCOUNT_DATE`, `AccountReceivablesList`, `COOPMERCHANTS_EN`, `COOPMERCHANTS_ID_Encrypted`, `COOPMERCHANTS_LINKMAN`, `COOPMERCHANTS_MOBILEPHONE`, `TAXPAYER_IDENTIFYCODE`, `UNDISTRIBUTED_AMOUNT`

**类型不一致** (4):
  - ACCOUNT_AMOUNT: float→int
  - ACTUAL_PAYMENT: float→int
  - COOPMERCHANTS_ID: str→int
  - CURRENTBALANCE: float→int

**值不一致** (6):
  - BANK_ACCOUNT: `` → `1`
  - BANK_NAME: `` → `1`
  - COOPMERCHANTS_NAME: `广州弘胜餐饮管理有限公司` → `1`
  - COOPMERCHANTS_NATURE: `企业公司` → ``
  - COOPMERCHANTS_TYPENAME: `合作经营类` → ``
  - PROJECT_SIGNCOUNT: 97 → 0

### 18. `GetMerchantsReceivablesReport`

- **接口**: `BusinessProject/GetMerchantsReceivablesReport`
- **差异数**: 3
- **状态**: ⬜ 待修复

**值不一致** (2):
  - PageSize: 185 → 999
  - TotalCount: 185 → 0

**列表差异** (1):
  - List: 185→0

### 19. `GetNoProjectShopList`

- **接口**: `BusinessProject/GetNoProjectShopList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `index`, `type`

**类型不一致** (8):
  - value: float→int
  - value: float→int
  - value: float→int
  - value: float→int
  - value: float→int
  - value: float→int
  - value: float→int
  - value: float→int

**列表差异** (1):
  - List: 10→11

### 20. `GetPERIODWARNINGDetail`

- **接口**: `BusinessProject/GetPERIODWARNINGDetail`
- **差异数**: 18
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSPROJECT_IDS`, `BUSINESS_STATES`, `BUSINESS_TRADES`, `ENDDATE_End`, `ENDDATE_Start`, `GUARANTEED_PROGRESS`, `MERCHANTS_IDS`, `PERIOD_PROGRESS`, `PROJECT_ENDDATE_End`, `PROJECT_ENDDATE_Start`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `SHOPROYALTY_IDS`, `WARNING_TYPES`

**多出字段** (1):
  `PERIODWARNING_DESC`

**类型不一致** (1):
  - STAFF_ID: NoneType→int

**值不一致** (2):
  - RECORD_DATE: `2026-03-06T20:36:57` → `2025-06-09T18:46:24`
  - STAFF_NAME: `` → `系统开发者`

### 21. `GetPERIODWARNINGList`

- **接口**: `BusinessProject/GetPERIODWARNINGList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSPROJECT_IDS`, `BUSINESS_STATES`, `BUSINESS_TRADES`, `ENDDATE_End`, `ENDDATE_Start`, `GUARANTEED_PROGRESS`, `MERCHANTS_IDS`, `PERIOD_PROGRESS`, `PROJECT_ENDDATE_End`, `PROJECT_ENDDATE_Start`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `SHOPROYALTY_IDS`, `WARNING_TYPES`

**多出字段** (1):
  `PERIODWARNING_DESC`

**类型不一致** (1):
  - STAFF_ID: NoneType→int

**值不一致** (2):
  - RECORD_DATE: `2026-03-06T20:36:57` → `2025-06-09T18:46:24`
  - STAFF_NAME: `` → `系统开发者`

### 22. `GetPROJECTSPLITMONTHDetail`

- **接口**: `BusinessProject/GetPROJECTSPLITMONTHDetail`
- **差异数**: 7
- **状态**: ⬜ 待修复

**缺少字段** (7):
  `BUSINESSPROJECT_IDS`, `MERCHANTS_IDS`, `REGISTERCOMPACT_IDS`, `SERVERPART_IDS`, `SHOPROYALTY_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`

### 23. `GetPROJECTSPLITMONTHList`

- **接口**: `BusinessProject/GetPROJECTSPLITMONTHList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (7):
  `BUSINESSPROJECT_IDS`, `MERCHANTS_IDS`, `REGISTERCOMPACT_IDS`, `SERVERPART_IDS`, `SHOPROYALTY_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`

### 24. `GetPROJECTWARNINGDetail`

- **接口**: `BusinessProject/GetPROJECTWARNINGDetail`
- **差异数**: 13
- **状态**: ⬜ 待修复

**缺少字段** (5):
  `BUSINESSPROJECT_ICO`, `PROJECTWARNING_STATES`, `SERVERPART_IDS`, `WARNING_DATE_End`, `WARNING_DATE_Start`

**多出字段** (4):
  `BUSINESS_BRAND`, `GUARANTEERATIO`, `SECONDPART_LINKMAN`, `SECONDPART_MOBILE`

**类型不一致** (1):
  - SWITCH_DATE: str→float

**值不一致** (3):
  - COMPACT_ENDDATE: `2027/03/02` → `2027-03-02T00:00:00`
  - COMPACT_STARTDATE: `2024/02/01` → `2024-02-01T00:00:00`
  - MerchantRatio: `28:72` → `28.0:72.0`

### 25. `GetPROJECTWARNINGList`

- **接口**: `BusinessProject/GetPROJECTWARNINGList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (10):
  `BUSINESSPROJECT_ICO`, `COMPACT_ENDDATE`, `COMPACT_STARTDATE`, `COOPMERCHANTS_LINKMAN`, `COOPMERCHANTS_MOBILEPHONE`, `MerchantRatio`, `PROJECTWARNING_STATES`, `SERVERPART_IDS`, `WARNING_DATE_End`, `WARNING_DATE_Start`

**类型不一致** (2):
  - SWITCH_DATE: str→float
  - SWITCH_DATE: str→float

### 26. `GetPaymentConfirmDetail`

- **接口**: `BusinessProject/GetPaymentConfirmDetail`
- **差异数**: 13
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `BUSINESSPROJECT_NAME`, `PAYMENTCONFIRM_PID`, `REMARKS_DESC`, `SERVERPART_NAME`

**类型不一致** (9):
  - ACCOUNT_DATE: str→NoneType
  - ACCOUNT_NAME: NoneType→str
  - ACCOUNT_TYPE: str→int
  - ATTACHMENT_FILES: NoneType→str
  - CONFIRMDATE: NoneType→int
  - MERCHANTS_NAME: NoneType→str
  - PAYMENTCONFIRM_DESC: NoneType→str
  - PAYMENTDATE: NoneType→int
  - PAYMENT_ACCOUNTINFO: NoneType→str

### 27. `GetPaymentConfirmList`

- **接口**: `BusinessProject/GetPaymentConfirmList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**缺少字段** (1):
  `Message`

**多出字段** (3):
  `Result_Code`, `Result_Data`, `Result_Desc`

### 28. `GetPeriodWarningList`

- **接口**: `BusinessProject/GetPeriodWarningList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `children`, `node`

**多出字段** (22):
  `ACTUAL_RATIO`, `BUSINESSPROJECT_ID`, `BUSINESSPROJECT_NAME`, `BUSINESS_PERIOD`, `BUSINESS_STATE`, `BUSINESS_TRADE`, `BUSINESS_TYPE`, `CA_COST`, `COMMISSION_RATIO`, `COST_AMOUNT`, `COST_RATE`, `DEPRECIATION_EXPENSE`, `DEPRECIATION_YEAR`, `ENDDATE`, `GUARANTEERATIO` 等22个

**列表差异** (1):
  - List: 1→10

### 29. `GetProjectAccountDetail`

- **接口**: `BusinessProject/GetProjectAccountDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (2):
  - Result_Code: 100 → 200
  - Result_Desc: `查询成功` → `查询失败，无数据返回！`

### 30. `GetProjectAccountList`

- **接口**: `BusinessProject/GetProjectAccountList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (24):
  `APPLY_PROCCESS`, `APPOVED_IDS`, `APPOVED_NAME`, `BUSINESSAPPROVAL_ID`, `CLOSED_DATE`, `COMPACT_NAME`, `CURRENT_PERIOD`, `CURREVENUE_AMOUNT`, `ENDDATE`, `MONTH_COUNT`, `MONTH_ENDCOUNT`, `MONTH_PROCESSCOUNT`, `NATUREDAY`, `PEND_STATE`, `PERIOD_COUNT` 等24个

**列表差异** (1):
  - List: 574→10

### 31. `GetProjectAccountTree`

- **接口**: `BusinessProject/GetProjectAccountTree`
- **差异数**: 8
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `children`, `node`

**多出字段** (4):
  `SERVERPART_ID`, `SERVERPART_NAME`, `SPREGIONTYPE_ID`, `SPREGIONTYPE_NAME`

**值不一致** (2):
  - PageSize: 1 → 9999
  - TotalCount: 0 → 1

### 32. `GetRTPaymentRecordDetail`

- **接口**: `BusinessProject/GetRTPaymentRecordDetail`
- **差异数**: 9
- **状态**: ⬜ 待修复

**缺少字段** (7):
  `ACCOUNT_AMOUNT`, `ACCOUNT_DATE`, `ACTUAL_PAYMENT`, `BUSINESSPROJECT_ID`, `BUSINESSPROJECT_NAME`, `MERCHANTS_ID`, `SERVERPART_NAME`

**类型不一致** (2):
  - OPERATE_DATE: NoneType→float
  - RECORD_DATE: NoneType→str

### 33. `GetRemarksDetail`

- **接口**: `BusinessProject/GetRemarksDetail`
- **差异数**: 1
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - OPERATE_DATE: str→float

### 34. `GetRemarksList`

- **接口**: `BusinessProject/GetRemarksList`
- **差异数**: 1
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - OPERATE_DATE: str→float

### 35. `GetRevenueConfirmDetail`

- **接口**: `BusinessProject/GetRevenueConfirmDetail`
- **差异数**: 12
- **状态**: ⬜ 待修复

**缺少字段** (12):
  `BUSINESSAPPROVAL_IDS`, `BUSINESSPROJECT_IDS`, `BUSINESSPROJECT_NAME`, `BUSINESS_BRANDS`, `BUSINESS_ENDDATE_End`, `BUSINESS_ENDDATE_Start`, `BUSINESS_STARTDATE_End`, `BUSINESS_STARTDATE_Start`, `BUSINESS_TRADES`, `MERCHANTS_ID`, `MERCHANTS_NAME`, `SHOPROYALTY_IDS`

### 36. `GetRevenueConfirmList`

- **接口**: `BusinessProject/GetRevenueConfirmList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (25):
  `BREACHPENALTY`, `BUSINESSAPPROVAL_ID`, `BUSINESSAPPROVAL_IDS`, `BUSINESSPROJECT_IDS`, `BUSINESS_BRAND`, `BUSINESS_BRANDS`, `BUSINESS_ENDDATE_End`, `BUSINESS_ENDDATE_Start`, `BUSINESS_PERIOD`, `BUSINESS_STARTDATE_End`, `BUSINESS_STARTDATE_Start`, `BUSINESS_TRADE`, `BUSINESS_TRADES`, `CASHPAY_AMOUNT`, `EARLY_SETTLEMENT` 等25个

### 37. `GetSHOPEXPENSEDetail`

- **接口**: `BusinessProject/GetSHOPEXPENSEDetail`
- **差异数**: 16
- **状态**: ⬜ 待修复

**缺少字段** (13):
  `ApprovalProcess`, `ChangeFlag`, `ImageFlag`, `PREPAIDLAST_AMOUNT`, `PREPAID_AMOUNT`, `RevenueAmount`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `SPREGIONTYPE_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`, `ShowRevenue`, `notExist`

**多出字段** (3):
  `BUSINESSPROJECT_ID`, `PERIOD_INDEX`, `SHOPROYALTY_ID`

### 38. `GetSHOPEXPENSEList`

- **接口**: `BusinessProject/GetSHOPEXPENSEList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (13):
  `ApprovalProcess`, `ChangeFlag`, `ImageFlag`, `PREPAIDLAST_AMOUNT`, `PREPAID_AMOUNT`, `RevenueAmount`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`, `SPREGIONTYPE_IDS`, `STATISTICS_MONTH_End`, `STATISTICS_MONTH_Start`, `ShowRevenue`, `notExist`

**多出字段** (4):
  `summaryObject`, `BUSINESSPROJECT_ID`, `PERIOD_INDEX`, `SHOPROYALTY_ID`

### 39. `GetShopExpenseSummary`

- **接口**: `BusinessProject/GetShopExpenseSummary`
- **差异数**: 3
- **状态**: ⬜ 待修复

**值不一致** (2):
  - PageSize: 10 → 9999
  - TotalCount: 1 → 0

**列表差异** (1):
  - List: 1→0

---

## Commodity

> 2 个接口存在差异

### 1. `GetCOMMODITYDetail`

- **接口**: `Commodity/GetCOMMODITYDetail`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (25):
  `ADDTIME`, `BUSINESSAPPROVAL_ID`, `BUSINESSTYPE`, `CANSALE`, `COMMODITY_ALLNAME`, `COMMODITY_BARCODE`, `COMMODITY_BRAND`, `COMMODITY_CODE`, `COMMODITY_COUNT`, `COMMODITY_CURRPRICE`, `COMMODITY_DESC`, `COMMODITY_EN`, `COMMODITY_FROZENCOUNT`, `COMMODITY_GRADE`, `COMMODITY_GROUPPRICE` 等25个

### 2. `GetCommodityList`

- **接口**: `Commodity/GetCommodityList`
- **差异数**: 10
- **状态**: ⬜ 待修复

**值不一致** (10):
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `锅盔` → `906`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `休闲食品类` → `1134`
  - COMMODITY_TYPE: `素菜类` → `913`

---

## Contract

> 8 个接口存在差异

### 1. `GetAttachmentDetail`

- **接口**: `Contract/GetAttachmentDetail`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - OPERATE_DATE: int→float
  - STAFF_NAME: NoneType→str

### 2. `GetAttachmentList`

- **接口**: `Contract/GetAttachmentList`
- **差异数**: 1
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - OPERATE_DATE: int→float

### 3. `GetProjectMonthlyArrearageList`

- **接口**: `Contract/GetProjectMonthlyArrearageList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `ProjectMonthlyCompleteBusiness_Year`, `ProjectMonthlyCompleteProjectCompleteDetailExpired_Amount`, `ProjectMonthlyCompleteProjectCompleteDetailUnExpired_Amount`

**类型不一致** (12):
  - ProjectMonthlyCompleteProjectCompleteDetailAccount_Amount: NoneType→int
  - ProjectMonthlyCompleteProjectCompleteDetailComplete_Degree: float→int
  - ProjectMonthlyCompleteProjectCompleteDetailPayment_Amount: NoneType→int
  - ProjectMonthlyCompleteProjectCompleteDetailAccount_Amount: NoneType→int
  - ProjectMonthlyCompleteProjectCompleteDetailComplete_Degree: float→int
  - ProjectMonthlyCompleteProjectCompleteDetailPayment_Amount: NoneType→int
  - ProjectMonthlyCompleteProjectCompleteDetailAccount_Amount: NoneType→int
  - ProjectMonthlyCompleteProjectCompleteDetailComplete_Degree: float→int
  - ProjectMonthlyCompleteProjectCompleteDetailPayment_Amount: NoneType→int
  - ProjectMonthlyCompleteProjectCompleteDetailAccount_Amount: NoneType→int
  - ...等12处

**列表差异** (1):
  - ProjectCompleteDetailList: 5→0

### 4. `GetProjectYearlyArrearageList`

- **接口**: `Contract/GetProjectYearlyArrearageList`
- **差异数**: 1
- **状态**: ⬜ 待修复

**列表差异** (1):
  - ProjectCompleteDetailList: 5→0

### 5. `GetRegisterCompactDetail`

- **接口**: `Contract/GetRegisterCompactDetail`
- **差异数**: 15
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `CLOSED_DATE`, `RELATE_COMPACT`, `SERVERPARTSHOP_IDS`, `SERVERPARTSHOP_NAME`

**类型不一致** (11):
  - BUSINESS_TRADE: NoneType→int
  - BUSINESS_TYPE: NoneType→int
  - COMPACT_CHILDTYPE: NoneType→int
  - DURATIONDAY: int→float
  - LogList: NoneType→list
  - OPERATING_AREA: NoneType→float
  - OTHER_SCHARGE: NoneType→str
  - PROPERTY_FEE: NoneType→float
  - SERVERPART_TYPE: NoneType→int
  - SETTLEMENT_CYCLE: NoneType→int
  - ...等11处

### 6. `GetRegisterCompactList`

- **接口**: `Contract/GetRegisterCompactList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `LogList`, `RENEWAL_YEARS`

**类型不一致** (17):
  - BUSINESS_TRADE: int→NoneType
  - DURATIONDAY: int→float
  - OTHER_SCHARGE: str→NoneType
  - PROPERTY_FEE: float→NoneType
  - RELATE_COMPACT: int→NoneType
  - SERVERPARTSHOP_NAME: str→NoneType
  - BUSINESS_TRADE: int→NoneType
  - OTHER_SCHARGE: str→NoneType
  - PROPERTY_FEE: float→NoneType
  - RELATE_COMPACT: int→NoneType
  - ...等17处

### 7. `GetRegisterCompactSubDetail`

- **接口**: `Contract/GetRegisterCompactSubDetail`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - OPERATING_AREA: float→int
  - PROPERTY_FEE: float→int

### 8. `GetRegisterCompactSubList`

- **接口**: `Contract/GetRegisterCompactSubList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - OPERATING_AREA: float→int
  - PROPERTY_FEE: float→int

---

## Finance

> 1 个接口存在差异

### 1. `GetAccountCompare`

- **接口**: `Finance/GetAccountCompare`
- **差异数**: 25
- **状态**: ⬜ 待修复

**类型不一致** (8):
  - ConfirmIncome.compareData: float→int
  - GuaranteeIncome.compareData: float→int
  - GuaranteePrice.compareData: float→int
  - RevenueAmount.compareData: float→int
  - RevenueAmount.curData: float→int
  - RoyaltyIncome.compareData: float→int
  - RoyaltyIncome.curData: float→int
  - RoyaltyIncome.curIntro: str→NoneType

**值不一致** (16):
  - ConfirmIncome.curIntro
  - GuaranteeIncome.curIntro
  - GuaranteePrice.curIntro: `第1期保底租金(180000)` → `第1期保底租金(180000.0)`
  - ServerpartShopId: `5627,5626` → `5626,5627`
  - BusinessProjectId: `1508` → `1506`
  - ConfirmIncome.compareData
  - ConfirmIncome.compareIntro
  - ConfirmIncome.curData
  - ConfirmIncome.curIntro
  - GuaranteeIncome.compareData
  - ...等16处

**列表差异** (1):
  - children: 14→8

---

## Merchants

> 6 个接口存在差异

### 1. `GetBusinessManDetail`

- **接口**: `Merchants/GetBusinessManDetail`
- **差异数**: 2
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `OrganizationList`, `ShopList`

### 2. `GetBusinessManList`

- **接口**: `Merchants/GetBusinessManList`
- **差异数**: 3
- **状态**: ⬜ 待修复

**缺少字段** (2):
  `OrganizationList`, `ShopList`

**类型不一致** (1):
  - OWNERUNIT_DESC: str→NoneType

### 3. `GetCommodityList`

- **接口**: `Merchants/GetCommodityList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (14):
  `BUSINESSMAN_ID`, `COMMODITY_BUSINESS_ID`, `COMMODITY_QTYPE`, `COMMODITY_TYPENAME`, `QUALIFICATIONList`, `QUALIFICATION_ENDDATE`, `QUALIFICATION_ENDDATE_End`, `QUALIFICATION_ENDDATE_Start`, `QUALIFICATION_ID`, `SERVERPARTSHOP_IDS`, `SERVERPART_NAME`, `STAFF_ID`, `STAFF_NAME`, `UPPER_STATE`

**多出字段** (11):
  `ADDTIME`, `BUSINESSAPPROVAL_ID`, `BUSINESSTYPE`, `CANSALE`, `COMMODITY_ALLNAME`, `COMMODITY_BRAND`, `COMMODITY_CODE`, `COMMODITY_COUNT`, `COMMODITY_CURRPRICE`, `COMMODITY_EN`, `COMMODITY_FROZENCOUNT`

### 4. `GetCustomTypeDDL`

- **接口**: `Merchants/GetCustomTypeDDL`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 5. `GetNestingCustomTypeLsit`

- **接口**: `Merchants/GetNestingCustomTypeLsit`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 6. `GetTradeBrandMerchantsList`

- **接口**: `Merchants/GetTradeBrandMerchantsList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**缺少字段** (1):
  `Message`

**多出字段** (3):
  `Result_Code`, `Result_Data`, `Result_Desc`

---

## MobilePay

> 2 个接口存在差异

### 1. `GetBANKACCOUNTVERIFYTreeList`

- **接口**: `MobilePay/GetBANKACCOUNTVERIFYTreeList`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 2. `GetMobilePayRoyaltyReport`

- **接口**: `MobilePay/GetMobilePayRoyaltyReport`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→list

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

---

## Revenue

> 24 个接口存在差异

### 1. `GetACCOUNTWARNINGDetail`

- **接口**: `Revenue/GetACCOUNTWARNINGDetail`
- **差异数**: 2
- **状态**: ⬜ 待修复

**类型不一致** (1):
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 2. `GetACCOUNTWARNINGList`

- **接口**: `Revenue/GetACCOUNTWARNINGList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**多出字段** (3):
  `OtherData`, `StaticsModel`, `RECORD_DATE`

**类型不一致** (15):
  - ACTUAL_RATIO: float→NoneType
  - COMMISSION_RATIO: float→NoneType
  - COST_AMOUNT: float→NoneType
  - COST_RATE: float→NoneType
  - DEPRECIATION_YEAR: int→NoneType
  - ENDDATE: str→int
  - LABOURS_WAGE: float→NoneType
  - MINTURNOVER: float→NoneType
  - MONTH_COUNT: float→NoneType
  - PERIOD_INDEX: int→NoneType
  - ...等15处

**值不一致** (6):
  - ACCOUNTWARNING_ID: 8941 → 8521
  - BUSINESSPROJECT_ID: 1838 → 1926
  - BUSINESSPROJECT_NAME: `驿达集团红星服务区中餐项目租赁合同` → `徐集服务区蒸小皖中式餐饮合同延长补充协议`
  - BUSINESS_STATE: 1000 → 3000
  - BUSINESS_TYPE: 1000 → 2000
  - GUARANTEE_PRICE

**列表差异** (1):
  - List: 1→9

### 3. `GetBRANDANALYSISDetail`

- **接口**: `Revenue/GetBRANDANALYSISDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - Result_Code: int→str
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `失败`

### 4. `GetBRANDANALYSISList`

- **接口**: `Revenue/GetBRANDANALYSISList`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - Result_Code: int→str
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `失败`

### 5. `GetBUSINESSWARNINGDetail`

- **接口**: `Revenue/GetBUSINESSWARNINGDetail`
- **差异数**: 17
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `DATATYPES`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`

**多出字段** (13):
  `BUSINESSPROJECT_ID`, `BUSINESSTRADETYPE`, `BUSINESS_TRADE`, `REVENUE_AVG`, `REVENUE_SD`, `ROYALTY_THEORY`, `ROYALTY_THEORY_QOQ`, `ROYALTY_THEORY_YOY`, `TICKET_COUNT`, `TICKET_COUNT_QOQ`, `TICKET_COUNT_YOY`, `VEHICLE_COUNT_ORI`, `VEHICLE_COUNT_ORI_YOY`

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 6. `GetBUSINESSWARNINGList`

- **接口**: `Revenue/GetBUSINESSWARNINGList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `DATATYPES`, `SERVERPARTSHOP_IDS`, `SERVERPART_IDS`

**多出字段** (15):
  `OtherData`, `StaticsModel`, `BUSINESSPROJECT_ID`, `BUSINESSTRADETYPE`, `BUSINESS_TRADE`, `REVENUE_AVG`, `REVENUE_SD`, `ROYALTY_THEORY`, `ROYALTY_THEORY_QOQ`, `ROYALTY_THEORY_YOY`, `TICKET_COUNT`, `TICKET_COUNT_QOQ`, `TICKET_COUNT_YOY`, `VEHICLE_COUNT_ORI`, `VEHICLE_COUNT_ORI_YOY`

**类型不一致** (1):
  - REVENUE_AMOUNT_YOY: float→NoneType

**值不一致** (6):
  - BUSINESSWARNING_ID: 21487 → 44672
  - RECORD_DATE: `2024-07-04T14:51:25` → `2026-03-10T12:01:40`
  - SERVERPARTSHOP_ID: `3066,3067` → `4077,4076`
  - SERVERPARTSHOP_NAME: `老乡鸡` → `八公山泉豆制品`
  - SERVERPART_ID: 416 → 432
  - SERVERPART_NAME: `新桥服务区` → `八公山服务区`

### 7. `GetBankAccountReport`

- **接口**: `Revenue/GetBankAccountReport`
- **差异数**: 3
- **状态**: ⬜ 待修复

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 8. `GetBrandAnalysis`

- **接口**: `Revenue/GetBrandAnalysis`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `List`, `PageIndex`, `PageSize`, `TotalCount`

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 9. `GetBusinessDate`

- **接口**: `Revenue/GetBusinessDate`
- **差异数**: 3
- **状态**: ⬜ 待修复

**值不一致** (3):
  - label: `2021/01/30` → `2021-01-30`
  - value: `2026/02/10` → `2026-02-10`
  - Result_Desc: `查询成功` → `成功`

### 10. `GetBusinessItemSummary`

- **接口**: `Revenue/GetBusinessItemSummary`
- **差异数**: 6
- **状态**: ⬜ 待修复

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (3):
  - PageSize: 1 → 10
  - TotalCount: 1 → 0
  - Result_Desc: `查询成功` → `成功`

**列表差异** (1):
  - List: 1→0

### 11. `GetBusinessTradeAnalysis`

- **接口**: `Revenue/GetBusinessTradeAnalysis`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `List`, `PageIndex`, `PageSize`, `TotalCount`

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 12. `GetCigaretteReport`

- **接口**: `Revenue/GetCigaretteReport`
- **差异数**: 6
- **状态**: ⬜ 待修复

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (3):
  - PageSize: 1 → 10
  - TotalCount: 1 → 0
  - Result_Desc: `查询成功` → `成功`

**列表差异** (1):
  - List: 1→0

### 13. `GetCurTotalRevenue`

- **接口**: `Revenue/GetCurTotalRevenue`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (18):
  `BankAccount_Amount`, `CashPay_Amount`, `Cash_Correct`, `Cigarette_Amount`, `Correct_Amount`, `CostBill_Amount`, `Different_Price_Less`, `Different_Price_More`, `InternalPay_Amount`, `MobilePay_Amount`, `Mobile_Correct`, `Revenue_Amount`, `Supplement_Amount`, `Supplement_State`, `Ticket_Count` 等18个

**多出字段** (7):
  `CASHPAY_AMOUNT`, `COSTBILL_AMOUNT`, `DIFFERENT_PRICE_LESS`, `DIFFERENT_PRICE_MORE`, `INTERNALPAY_AMOUNT`, `MOBILEPAY_AMOUNT`, `REVENUE_AMOUNT`

### 14. `GetMerchantRevenueReport`

- **接口**: `Revenue/GetMerchantRevenueReport`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (20):
  `Business_Type`, `Business_Type_Text`, `LineIndex`, `MERCHANTS_ID`, `MERCHANTS_NAME`, `RegionARevenue`, `RegionBRevenue`, `ServerpartShop_Id`, `ServerpartShop_Name`, `ShopTrade`, `Shop_Count`, `Statistics_Date`, `Transfer_Type`, `TotalRevenue.BankAccount_Amount`, `TotalRevenue.Cash_Correct` 等20个

**多出字段** (1):
  `StaticsModel`

**值不一致** (3):
  - TotalRevenue.CashPay_Amount
  - TotalRevenue.MobilePay_Amount
  - TotalRevenue.Revenue_Amount

**列表差异** (1):
  - children: 14→0

### 15. `GetMonthINCAnalysis`

- **接口**: `Revenue/GetMonthINCAnalysis`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (18):
  `SERVERPARTSHOP_ID`, `SERVERPARTSHOP_IDS`, `SERVERPARTSHOP_NAME`, `SERVERPART_ID`, `SERVERPART_NAME`, `INCREASE_DIFF`, `Id`, `Name`, `REVENUE_AMOUNT`, `REVENUE_AMOUNT_QOQ`, `REVENUE_AMOUNT_YOY`, `REVENUE_INCRATE_QOQ`, `REVENUE_INCRATE_YOY`, `REVENUE_INCREASE_QOQ`, `REVENUE_INCREASE_YOY` 等18个

**多出字段** (2):
  `OtherData`, `StaticsModel`

### 16. `GetREVENUEDAILYSPLITDetail`

- **接口**: `Revenue/GetREVENUEDAILYSPLITDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - Result_Code: int→str
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `失败`

### 17. `GetREVENUEDAILYSPLITList`

- **接口**: `Revenue/GetREVENUEDAILYSPLITList`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - Result_Code: int→str
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `失败`

### 18. `GetRevenueDataList`

- **接口**: `Revenue/GetRevenueDataList`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (21):
  `Business_Type`, `Business_Type_Text`, `CashPay_Amount`, `CostBill_Amount`, `Different_Price_Less`, `Different_Price_More`, `InternalPay_Amount`, `MobilePay_Amount`, `Revenue_Amount`, `ServerpartShop_ID`, `ServerpartShop_Name`, `ServerpartShop_Region`, `ServerpartShop_ShortName`, `ServerpartShop_Trade`, `Serverpart_ID` 等21个

**多出字段** (3):
  `OtherData`, `StaticsModel`, `AUDIT_COUNT`

**列表差异** (1):
  - List: 29→19564

### 19. `GetRevenueReport`

- **接口**: `Revenue/GetRevenueReport`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (20):
  `children`, `Business_Type`, `Business_Type_Text`, `LineIndex`, `MERCHANTS_ID`, `MERCHANTS_NAME`, `RegionARevenue`, `RegionBRevenue`, `ServerpartShop_Id`, `ServerpartShop_Name`, `ShopTrade`, `Statistics_Date`, `Transfer_Type`, `TotalRevenue.BankAccount_Amount`, `TotalRevenue.Cash_Correct` 等20个

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (3):
  - Shop_Count: 43 → 50
  - TotalRevenue.CashPay_Amount
  - TotalRevenue.Different_Price_Less

### 20. `GetRevenueReportByDate`

- **接口**: `Revenue/GetRevenueReportByDate`
- **差异数**: 25
- **状态**: ⬜ 待修复

**缺少字段** (21):
  `Business_Type`, `Business_Type_Text`, `LineIndex`, `MERCHANTS_ID`, `MERCHANTS_NAME`, `RegionARevenue`, `RegionBRevenue`, `ServerpartShop_Id`, `ServerpartShop_Name`, `Serverpart_ID`, `ShopTrade`, `Shop_Count`, `Transfer_Type`, `TotalRevenue.BankAccount_Amount`, `TotalRevenue.Cash_Correct` 等21个

**多出字段** (2):
  `OtherData`, `StaticsModel`

**值不一致** (2):
  - Serverpart_Name: `2025-12-01` → `20251201`
  - Statistics_Date: `2025-12-01` → `20251201`

### 21. `GetSITUATIONANALYSISDetail`

- **接口**: `Revenue/GetSITUATIONANALYSISDetail`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - Result_Code: int→str
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `失败`

### 22. `GetSITUATIONANALYSISList`

- **接口**: `Revenue/GetSITUATIONANALYSISList`
- **差异数**: 3
- **状态**: ⬜ 待修复

**类型不一致** (2):
  - Result_Code: int→str
  - Result_Data: dict→NoneType

**值不一致** (1):
  - Result_Desc: `查询成功` → `失败`

### 23. `GetSituationAnalysis`

- **接口**: `Revenue/GetSituationAnalysis`
- **差异数**: 5
- **状态**: ⬜ 待修复

**缺少字段** (4):
  `List`, `PageIndex`, `PageSize`, `TotalCount`

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

### 24. `GetTotalRevenue`

- **接口**: `Revenue/GetTotalRevenue`
- **差异数**: 19
- **状态**: ⬜ 待修复

**缺少字段** (18):
  `BankAccount_Amount`, `CashPay_Amount`, `Cash_Correct`, `Cigarette_Amount`, `Correct_Amount`, `CostBill_Amount`, `Different_Price_Less`, `Different_Price_More`, `InternalPay_Amount`, `MobilePay_Amount`, `Mobile_Correct`, `Revenue_Amount`, `Supplement_Amount`, `Supplement_State`, `Ticket_Count` 等18个

**值不一致** (1):
  - Result_Desc: `查询成功` → `成功`

---

## Supplier

> 2 个接口存在差异

### 1. `GetQualificationList`

- **接口**: `Supplier/GetQualificationList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**缺少字段** (1):
  `Message`

**多出字段** (3):
  `Result_Code`, `Result_Data`, `Result_Desc`

### 2. `GetSupplierList`

- **接口**: `Supplier/GetSupplierList`
- **差异数**: 4
- **状态**: ⬜ 待修复

**缺少字段** (1):
  `Message`

**多出字段** (3):
  `Result_Code`, `Result_Data`, `Result_Desc`

---

## Verification

> 1 个接口存在差异

### 1. `GetShopEndaccountSum`

- **接口**: `Verification/GetShopEndaccountSum`
- **差异数**: 10
- **状态**: ⬜ 待修复

**缺少字段** (3):
  `ServerpartShop_ICO`, `ShopRegion_Name_A`, `ShopRegion_Name_B`

**类型不一致** (3):
  - Revenue_Amount: float→int
  - Revenue_Amount_A: float→int
  - Revenue_Amount_B: float→int

**值不一致** (3):
  - Deal_Count: 2 → 0
  - Total_Count: 2 → 0
  - Treatment_MarkState

**列表差异** (1):
  - VerifiedList: 2→0
