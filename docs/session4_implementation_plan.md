# 208 个 FAIL 接口 — 按模块修改计划

> 全局前置修复：在 `core/database.py` 补充 `fetch_one` / `fetch_scalar` 两个方法，可一次性解决 33 个接口报错。

---

## 1. Analysis（30 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- `services/analysis/` 下各手写 service

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetANALYSISINS Detail/List` | `fetch_one`/`fetch_scalar` 缺失 | **全局修复 R1** |
| `GetANALYSISRULE Detail/List` | 同上 | **全局修复 R1** |
| `GetASSETSPROFITS Detail/List` | 同上 | **全局修复 R1** |
| `GetINVESTMENTANALYSIS Detail/List` | 同上 | **全局修复 R1** |
| `GetINVESTMENTDETAIL Detail/List` | 同上 | **全局修复 R1** |
| `GetPERIODMONTHPROFIT Detail/List` | 同上 | **全局修复 R1** |
| `GetPROFITCONTRIBUTE Detail/List` | 同上 | **全局修复 R1** |
| `GetPROMPT Detail/List` | 同上 | **全局修复 R1** |
| `GetSENTENCE Detail/List` | 同上 | **全局修复 R1** |
| `GetVEHICLEAMOUNT Detail/List` | 同上 | **全局修复 R1** |
| `GetASSETSPROFITSBusinessTreeList` | Desc "成功"→"查询成功" + 多出 StaticsModel + PageSize 不回显 | 修改 service 的 Result_Desc + 移除 StaticsModel + 回显 PageSize |
| `GetASSETSPROFITSDateDetailList` | Desc "成功"→"查询成功" | 修改 Result_Desc |
| `GetASSETSPROFITSTreeList` | 同 BusinessTreeList | 同上 |
| `GetAssetsLossProfitList` | Desc + Result_Data 类型 dict→list | 修改返回结构对齐 C# |
| `GetInvestmentReport` | Desc + Result_Data 类型 | 同上 |
| `GetNestingIAReport` | Desc + Result_Data 类型 | 同上 |
| `GetPeriodMonthlyList` | Desc + Result_Data 类型 | 同上 |
| `GetRevenueEstimateList` | Desc + Result_Data 类型 | 同上 |
| `GetShopSABFIList` | Desc + Result_Data 类型 | 同上 |
| `GetPREFERRED_RATINGList` | 参数校验错误 | 修复路由参数定义 |

---

## 2. Audit（10 个 FAIL）

### 涉及文件
- `services/audit/audit_service.py`
- `routers/eshang_api_main/audit/audit_router.py`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetABNORMALAUDITList` | Desc + Result_Code 999 + 多出 Message | service 中 `fetch_scalar` 缺失 → **全局修复 R1** 后验证 |
| `GetAUDITTASKS Detail/List` | 同上 | 同上 |
| `GetAbnormalAuditDetail` | 同上 | 同上 |
| `GetCHECKACCOUNT Detail/List` | 同上 | 同上 |
| `GetYSABNORMALITY Detail/List` | 同上 | 同上 |
| `GetAbnormalRateReport` | HTTP 405 方法不允许 | 路由加 `GET` 方法支持 |
| `GetCheckAccountReport` | HTTP 405 方法不允许 | 路由加 `GET` 方法支持 |

---

## 3. BaseInfo（44 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part1.py`
- `services/base_info/` 下各手写 service
- `core/database.py`（类型转换）

### 修改内容

**字段差异 (31个)** — 批量路由的 Detail/List 缺少 `_IDS`/`_Start`/`_End` 等 SearchParameter 回显字段：
- `GetAUTOSTATISTICSDetail`、`GetSERVERPARTDetail/List/CRTDetail/CRTList/CRTTreeList`、`GetPROPERTYASSETSDetail/List/TreeList`、`GetPROPERTYSHOPDetail/List`、`GetRTSERVERPARTSHOPDetail/List`、`GetCASHWORKERDetail/List`、`GetSERVERPARTSHOP_LOGList`、`GetUSERDEFINEDTYPEDetail/List`
- 手写接口：`GetBrandDetail/List`（缺 JOIN 字段）、`GetCombineBrandList`（缺扩展字段）、`GetServerpartShopDetail/Info`（缺扩展字段）、`GetServerPartShopNewList`（缺字段+长度差异）、`GetCOMMODITYDetail/List`（缺字段）、`GetBusinessTradeEnum`（缺 desc）、`GetSPRegionShopTree/ServerpartShopTree`（缺 desc/ico）、`GetTradeBrandTree`（children 类型差异）

**类型差异 (7个)**：
- `GetBusinessBrandList`：int→float（NUMBER 类型）→ `database.py` 全局 float→int
- `GetBusinessTradeDetail/Tree`：None→"" / None→int → service 层绑定
- `GetCOMMODITYTYPEDetail/List`：int→float → `database.py` 全局
- `GetOWNERUNITDetail`：None→"" → service 层绑定
- `BindingOwnerUnitTree`：children `[]` vs `None` → service 层处理

**值差异 (6个)**：
- `GetShopReceivables`：日期格式 → `database.py` 日期格式化
- `GetServerpartUDTypeTree`：排序差异 → service 排序逻辑
- `GetAssetsRevenueAmount/GetNestingCOMMODITYTYPEList/Tree/GetServerpartShopList`：数据为空 → 参数/SQL 问题

---

## 4. BigData（13 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part1.py`
- `services/bigdata/` 下手写 service

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetBAYONETDAILY_AHList`、`GetBAYONETWARNINGList`、`GetSECTIONFLOWDetail/List`、`GetSECTIONFLOWMONTHDetail/List` | 缺 `_IDS`/`_Start`/`_End` 回显字段 | batch_router 补回显 |
| `GetBAYONETDetail/List` | SQL 报错：缺表 `T_BAYONET` | 同步表 |
| `GetBayonetOwnerAHList/MonthAHList` | Result_Code 999 | 修复 service 查询逻辑 |
| `GetDailyBayonetAnalysis` | Desc + Result_Data 类型 | 修改返回结构 |
| `GetServerpartSectionFlow` | StaticsModel 多出 + 值差异 | 修改 service |
| `GetTimeIntervalList` | StaticsModel 多出 + 列表长度差异 | 修改 service |

---

## 5. Budget（4 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/budget/budget_router.py`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetBudgetDetailDetail/List`、`GetBudgetProjectList`、`GetbudgetProjectDetail` | `fetch_one`/`fetch_scalar` 缺失 | **全局修复 R1** |

---

## 6. BusinessMan（3 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- `services/businessman/`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetCOMMODITY_TEMP Detail/List` | `fetch_one`/`fetch_scalar` 缺失 | **全局修复 R1** |
| `GetUserList` | StaticsModel 多出 + 数据为空 | 修改 service |

---

## 7. BusinessProject（40 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part1.py`、`batch_router_part2.py`
- `services/businessproject/` 下各手写 service

### 修改内容

**字段差异 (30个)** — 主要是批量路由缺少回显字段和手写接口缺扩展字段：
- 批量路由：`GetAPPROVEDList`、`GetBIZPSPLITMONTHDetail/List`、`GetBUSINESSPROJECTSPLITDetail/List`、`GetPERIODWARNINGDetail/List`、`GetPROJECTSPLITMONTHDetail/List`、`GetPROJECTWARNINGDetail/List`、`GetSHOPEXPENSEDetail/List`
- 手写接口：`GetAccountWarningList`、`GetAnnualSplit`、`GetBusinessProjectDetail/List`、`GetExpenseSummary`、`GetMerchantSplit`、`GetMerchantsReceivablesList`、`GetNoProjectShopList`、`GetPaymentConfirmDetail`、`GetPeriodWarningList`、`GetProjectAccountList/Tree`、`GetRTPaymentRecordDetail`、`GetRevenueConfirmDetail/List`、`GetBusinessPaymentDetail/List`（多出字段）

**Python 查询报错 (4个)**：
- `GetMerchantsReceivables`：返回结构差异 → 修改 service
- `GetProjectAccountDetail`：查询逻辑 → 修改 service
- `GetRTPaymentRecordList`：SQL 语法错误 → 修复 SQL
- `GetWillSettleProject`：SQL 语法错误 → 修复 SQL

**值差异 (4个)**：`GetAccountWarningListSummary`、`GetBrandReceivables`、`GetMerchantsReceivablesReport`、`GetShopExpenseSummary`

**类型差异 (2个)**：`GetRemarksDetail/List` — OPERATE_DATE 类型 str↔float

---

## 8. Commodity（3 个 FAIL）

### 涉及文件
- `services/commodity/`、`routers/.../commodity/`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetCOMMODITYDetail` | 缺 25 个字段 | 对照 C# 补充 JOIN/计算字段 |
| `GetCommodityList` | 缺字段 + COMMODITY_TYPE 值差异 | 同上 |
| `GetCOMMODITYList` | 日期格式差异 | `database.py` 日期格式化 |

---

## 9. Contract（8 个 FAIL）

### 涉及文件
- `services/contract/`、`routers/.../contract/`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetRegisterCompactDetail` | 缺 3 字段 + 15 处差异 | 对照 C# 补字段 |
| `GetRegisterCompactList` | 缺 LogList/RENEWAL_YEARS 等 | 同上 |
| `GetAttachmentDetail/List` | OPERATE_DATE int→float | `database.py` float→int |
| `GetRegisterCompactSubDetail/List` | OPERATING_AREA float→int | 同上 |
| `GetProjectYearlyArrearageList` | 列表长度差异 | 修复 service 查询 |
| `GetProjectMonthlyArrearageList` | 缺字段 + 长度差异 | 修复 service |

---

## 10. Customer（2 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetCUSTOMERGROUP_AMOUNTDetail` | 缺 `_IDS`/`_Start`/`_End` 回显字段 | batch_router 补回显 |
| `GetCUSTOMERGROUP_AMOUNTList` | SQL 报错 | 修复 SQL（表名错误） |

---

## 11. Finance（2 个 FAIL）

### 涉及文件
- `services/finance/`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetAccountCompare` | StaticsModel 多出 + 数据差异 | 修改 service |
| `GetAHJKtoken` | 参数校验错误 | 修复路由参数 |

---

## 12. Merchants（11 个 FAIL）

### 涉及文件
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- `services/merchants/`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetBusinessManDetail/List`、`GetBusinessManDetailDetail/List` | `fetch_one`/`fetch_scalar` 缺失 | **全局修复 R1** |
| `GetCUSTOMTYPEDetail/List` | 同上 | **全局修复 R1** |
| `GetCommodityList` (Merchants下) | 同上 | **全局修复 R1** |
| `GetCoopMerchantsList` | `超出全局排序空间` | SQL 加 LIMIT 或达梦参数调优 |
| `GetCommodityDetail` | Result_Code 999 | 修复 service |
| `GetCustomTypeDDL` | Desc + Result_Data 类型 | 修改返回结构 |
| `GetNestingCustomTypeLsit` | 同上 | 同上 |

---

## 13. MobilePay（6 个 FAIL）

### 涉及文件
- `services/mobilepay/`、`routers/.../mobilepay/`

### 修改内容

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetBANKACCOUNTVERIFYTreeList` | Desc + Result_Data 类型 | 修改返回结构 |
| `GetMobilePayRoyaltyReport` | 同上 | 同上 |
| `GetBANKACCOUNTVERIFYList/RegionList/ServerList` | 参数校验错误 | 修复路由参数 |
| `GetMobilePayResult` | 参数校验错误 | 修复路由参数 |

---

## 14. Revenue（27 个 FAIL）

### 涉及文件
- `services/revenue/revenue_service.py`
- `routers/eshang_api_main/revenue/`
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`

### 修改内容

**Python 查询报错 (7个)**：
- `GetBRANDANALYSIS Detail/List`：缺表 `T_BRANDANALYSIS` → 同步表
- `GetREVENUEDAILYSPLIT Detail/List`：缺表 `T_REVENUEDAILYSPLIT` → 同步表
- `GetSITUATIONANALYSIS Detail/List`：缺表 `T_SITUATIONANALYSIS` → 同步表
- `GetACCOUNTWARNINGList`：`超出全局排序空间` → SQL 优化

**Desc + 返回结构差异 (10个)**：
- `GetACCOUNTWARNINGDetail`、`GetBankAccountReport`、`GetBusinessDate`、`GetBusinessItemSummary`、`GetCigaretteReport`、`GetBrandAnalysis`、`GetBusinessTradeAnalysis`、`GetSituationAnalysis`、`GetTotalRevenue`、`GetRevenueYOYQOQ`(405)

**字段差异 (9个)**：
- `GetBUSINESSWARNINGDetail/List`、`GetCurTotalRevenue`、`GetMerchantRevenueReport`、`GetMonthINCAnalysis`、`GetRevenueDataList`、`GetRevenueReport/ByDate`、`GetBUSINESSANALYSISList`、`GetPERSONSELLList`

**HTTP 方法错误 (1个)**：`GetRevenueYOYQOQ` → 路由加 GET

---

## 15. Sales（2 个 FAIL）

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetCOMMODITYSALEList` | 参数校验错误 | 修复路由参数 |
| `GetEndaccountError` | 参数校验错误 | 修复路由参数 |

## 16. Supplier（1 个 FAIL）

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetQUALIFICATION_HISList` | 参数校验错误 | 修复路由参数 |

## 17. Verification（2 个 FAIL）

| 接口 | 原因 | 修改 |
|---|---|---|
| `GetShopEndaccountSum` | Desc + Result_Data 类型 | 修改 service 返回结构 |
| `GetSuppEndaccountList` | StaticsModel 多出 + 数据差异 | 修改 service |

---

## 执行顺序建议

1. **全局修复**：`database.py` 补 `fetch_one`/`fetch_scalar` → 覆盖 33 个（Analysis 20 + Budget 4 + BusinessMan 2 + Merchants 7）
2. **简单模块优先**：Budget(4)、BusinessMan(3)、Customer(2)、Finance(2)、Sales(2)、Supplier(1)、Verification(2)
3. **中等模块**：Audit(10)、Merchants(11)、Contract(8)、Commodity(3)、MobilePay(6)、BigData(13)
4. **复杂模块最后**：BaseInfo(44)、BusinessProject(40)、Revenue(27)
