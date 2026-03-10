# 窗口 2 审计结果

结论摘要：Finance、Revenue、BigData、MobilePay 共 206 条基线路由中，仅 28 条可判定为完全一致；Finance 以“简化版/直接成功/空返回”占位为主，Revenue 大量以通用 CRUD 替代原 helper，BigData 存在响应契约漂移且 `BAYONETWARNING` 缺 3 条，MobilePay 的外部支付/银联逻辑基本被本地表查询替代。

审计范围：Finance、Revenue、BigData、MobilePay。  
审计方式：按 `docs/full_audit_baseline_20260309.json` 的模块路由清单逐条静态比对 Python router/service 与原 C# controller/helper；为保证全量覆盖，下文“路由级问题清单”同时列出“完全一致”路由。

## 模块总表

| 模块 | 基线路由数 | 完全一致 | 契约不一致 | 逻辑不一致 | 占位实现 | Python 多出 | Python 缺失 | 备注 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Finance | 88 | 22 | 2 | 14 | 38 | 0 | 12 | “简化版”报表、审批、固化/生成接口集中 |
| Revenue | 60 | 6 | 5 | 49 | 0 | 0 | 0 | 大量 entity-specific helper 被 generic CRUD 替代 |
| BigData | 40 | 0 | 34 | 3 | 0 | 0 | 3 | baseline 标成 12 条缺失，实检仅 `BAYONETWARNING` 3 条真实缺失 |
| MobilePay | 18 | 0 | 0 | 15 | 2 | 0 | 1 | 外部支付、银联、对账 helper 基本未保留 |
| 合计 | 206 | 28 | 41 | 81 | 40 | 0 | 16 | 仅 13.59% 可判定为完全一致 |

## 路由级问题清单

### Finance

| 路由 | 归类 | Python 证据 | C# 证据 | 审计结论 |
| --- | --- | --- | --- | --- |
| `Budget/GetBUDGETPROJECTAHList`、`Budget/GetBUDGETPROJECTAHDetail`、`Budget/SynchroBUDGETPROJECTAH`、`Budget/DeleteBUDGETPROJECTAH`、`Budget/GetBUDGETDETAILAHList`、`Budget/GetBUDGETDETAILAHDetail`、`Budget/SynchroBUDGETDETAILAH`、`Budget/DeleteBUDGETDETAILAH`、`Budget/SetBudgetDetailAHList` | 完全一致 | `routers/eshang_api_main/finance/budget_router.py:21-155`；`services/finance/budget_service.py:46-282` | `API/CSharp/EShangApiMain/Controllers/Finance/BudgetProjectAHController.cs:32-346` | CRUD、删除状态、明细批量同步与 C# 控制器行为一致。 |
| `Budget/GetBudgetProjectReportOfMonth` | 契约不一致 | `budget_router.py:158-170`；`budget_service.py:286-343` | `BudgetProjectAHController.cs:360-392` | C# 返回按月份与科目展开的报表结构；Python 仅返回扁平 pivot 结果，响应包与字段组织方式已变。 |
| `Budget/GetbudgetProjectReport`、`Budget/GetbudgetProjectReportDynamic`、`Budget/GetbudgetProjectReportIn`、`Budget/GetbudgetProjectReportInDynamic`、`Budget/GetbudgetProjectReportOut`、`Budget/GetbudgetProjectReportOutDynamic` | 占位实现 | `budget_router.py:173-248`；`budget_service.py:347-354` 仅返回空字符串，且 dynamic/in/out 对应 service 方法不存在 | `BudgetProjectAHController.cs:394-1223` | 原 C# 为完整报表生成/动态列/进出项逻辑；Python 路由已挂出，但核心实现缺失或空返回。 |
| `Finance/GetFATTACHMENTList`、`Finance/GetFATTACHMENTDetail`、`Finance/SynchroFATTACHMENT`、`Finance/DeleteFATTACHMENT` | 完全一致 | `routers/eshang_api_main/finance/fattachment_router.py:25-95`；`services/finance/fattachment_service.py:49-159` | `API/CSharp/EShangApiMain/Controllers/Finance/FinanceController.cs:28-155` | 附件 CRUD、明细读取、状态删除逻辑与 C# 保持一致。 |
| `Finance/GetProjectSplitSummary`、`Finance/GetProjectSummary`、`Finance/GetRevenueSplitSummary`、`Finance/GetProjectMerchantSummary` | 逻辑不一致 | `services/finance/finance_scattered_service.py:23-161` 明写“简化版”，后 3 个接口直接复用 `get_project_split_summary/get_project_summary` | `FinanceController.cs:171-346` | C# 分别调用 `BUSINESSPROJECTSPLITHelper.GetProjectSplitSummary/GetProjectSummary/GetProjectMerchantSummary`，并返回 `RevenueCompareModel/OtherData`；Python 将 4 个接口收敛成同一套简化 SQL 聚合。 |
| `Finance/GetRoyaltyDateSumReport`、`Finance/GetRoyaltyReport` | 逻辑不一致 | `finance_scattered_service.py:184-226`，`GetRoyaltyReport` 直接复用 `GetRoyaltyDateSumReport` | `FinanceController.cs:448-539` | C# 分别调用 `GetBankAccountVerifySumDateTreeList` 与 `GetBANKACCOUNTVERIFYDateTreeList`；Python 将两者合并为同一查询，树形层级与对账逻辑丢失。 |
| `Finance/GetProjectShopIncome`、`Finance/GetContractMerchant`、`Finance/GetAccountReached`、`Finance/GetShopExpense` | 逻辑不一致 | `finance_scattered_service.py:229-314`，其中 `GetProjectShopIncome` 忽略 `ContrastDate`，`GetAccountReached/GetShopExpense` 直接复用 `get_contract_merchant` | `FinanceController.cs:550-705` | 原实现分别走 `ProjectSummaryHelper/FinanceHelper`；Python 用单表或同一查询替代，统计口径与树形结果均漂移。 |
| `Finance/GetReconciliation` | 逻辑不一致 | `finance_scattered_service.py:315-324` 仅返回项目基本信息和空 `ReconciliationData` | `FinanceController.cs:707-764` | C# 走对账 helper 生成真实对账结果；Python 只保留壳结构。 |
| `Finance/GetProjectPeriodAccount` | 逻辑不一致 | `finance_scattered_service.py:351-361` 仅查 `T_REVENUECONFIRM` 单表 | `FinanceController.cs:857-887` | 原接口为期间到账核算 helper；Python 退化为单表读取，无法覆盖原核算流程。 |
| `Finance/CreateSingleProjectSplit`、`Finance/SolidMonthProjectSplit` | 占位实现 | `finance_scattered_service.py:164-181` 仅记日志并 `return True` | `FinanceController.cs:361-425` | 原接口为生成/固化类重写逻辑；Python 仅保留成功壳接口。 |
| `Finance/GetRevenueRecognition`、`Finance/GetProjectPeriodIncome` | 占位实现 | `finance_scattered_service.py:328-347` 直接返回空列表 | `FinanceController.cs:766-855` | 原接口为收入确认/期间收入计算；Python 无真实报表逻辑。 |
| `Finance/ApplyAccountProinst`、`Finance/ApproveAccountProinst`、`Finance/RejectAccountProinst`、`Finance/GetMonthAccountProinst`、`Finance/ApplyMonthAccountProinst`、`Finance/ApproveMonthAccountProinst`、`Finance/ApproveMAPList`、`Finance/RejectMonthAccountProinst` | 占位实现 | `finance_scattered_service.py:365-437`，“简化版”、空列表、直接成功 | `FinanceController.cs:889-1270` | 原 C# 为完整审批流与月度确认流程；Python 仅保留接口外壳，审批节点、状态迁移、批量审核均未迁移。 |
| `Finance/StorageMonthProjectAccount`、`Finance/GetMonthAccountDiff`、`Finance/ApprovePeriodAccount`、`Finance/RejectPeriodAccount`、`Finance/GetPeriodSupplementList` | 占位实现 | `finance_scattered_service.py:441-479` | `FinanceController.cs:1313-1569` | 固化、差异、期间审批、补录等核心流程均被空结果/直接成功替代。 |
| `Finance/GetBankAccountAnalyseList`、`Finance/GetBankAccountAnalyseTreeList`、`Finance/SolidBankAccountSplit` | 占位实现 | `finance_scattered_service.py:503-523` | `FinanceController.cs:1611-1799` | 原对账分析与固化 helper 未迁移，Python 仅返回空数据或成功。 |
| `Finance/GetContractExcuteAnalysis`、`Finance/RebuildSCSplit`、`Finance/CorrectRevenueAccountData`、`Finance/RebuildClosedPeriod`、`Finance/RebuildReductionPeriod`、`Finance/SendSMSMessage`、`Finance/LadingBill`、`Finance/RejectLadingBill`、`Finance/GetAHJKtoken`、`Finance/GetAccountCompare`、`Finance/GetAnnualAccountList` | 占位实现 | `finance_scattered_service.py:527-614`；含“简化版”、`return True`、`return []`、`功能暂未迁移` | `FinanceController.cs:1801-2248` | 合同执行分析、重算、短信、提单、对账、年报等复杂 helper 流程未迁移。 |
| `Finance/GetProjectExpenseList` | 逻辑不一致 | `finance_scattered_service.py:483-499` 仅查单表费用 | `FinanceController.cs:1571-1609` | C# 通过 helper 组装费用维度与筛选；Python 退化为简单列表查询。 |
| `Invoice/GetBILLList`、`Invoice/SynchroBILL`、`Invoice/DeleteBILL` | 完全一致 | `routers/eshang_api_main/finance/invoice_router.py:32-88`；`services/finance/invoice_service.py:65-172,206-297` | `API/CSharp/EShangApiMain/Controllers/Finance/InvoiceController.cs:26-296` | 列表、同步、删除状态与单号生成逻辑基本一致。 |
| `Invoice/GetBILLDetail` | 契约不一致 | `invoice_service.py:175-203` 仅补 `DetailList` | `InvoiceController.cs:158-205`；`API/CSharp/EShangApi.Common/GeneralMethod/Finance/BILLHelper.cs:280-288` | C# 明细会同时带出 `DetailList` 与 `ApproveList`；Python 缺少审批意见列表。 |
| `Invoice/GetBILLDETAILList`、`Invoice/GetBILLDETAILDetail`、`Invoice/SynchroBILLDETAIL`、`Invoice/DeleteBILLDETAIL` | 完全一致 | `invoice_router.py:92-143`；`invoice_service.py:320-398` | `InvoiceController.cs:206-296` | BILLDETAIL CRUD、状态删除与 C# 一致。 |
| `Invoice/WriteBackInvoice`、`Invoice/RewriteJDPJInfo` | 完全一致 | `invoice_router.py:147-175`；`invoice_service.py:405-630` | `InvoiceController.cs:764-883`；`BILLHelper.cs` 对应回写逻辑 | 回写金额、税额、红冲状态与票据同步主流程已迁移。 |
| `Invoice/SendHXInvoiceInfo` | 占位实现 | `invoice_service.py:463-478` 仅日志 + `return True` | `InvoiceController.cs:803-838` | 原 C# 调用航信 SOAP WebService；Python 未实现外部开票推送。 |
| `Invoice/ForwardJDPJInterface` | 逻辑不一致 | `invoice_service.py:633-659` 仅 `requests.post`，固定 `Content-Type` | `InvoiceController.cs:885-923` | C# 转发时补 `access_token` 头并保留原接口契约；Python 未注入 token，外部调用语义漂移。 |
| `Invoice/GetINVOICEINFOList`、`Invoice/GetINVOICEINFODetail`、`Invoice/SynchroINVOICEINFO`、`Invoice/DeleteINVOICEINFO`、`Invoice/GetGOODSTAXINFOList`、`Invoice/GetGOODSTAXINFODetail`、`Invoice/SynchroGOODSTAXINFO`、`Invoice/DeleteGOODSTAXINFO`、`Office/GetAPPLYAPPROVEList`、`Office/GetAPPLYAPPROVEDetail`、`Office/SynchroAPPLYAPPROVE`、`Office/DeleteAPPLYAPPROVE` | Python 缺失 | `full_audit_baseline_20260309.json` 对应路由在 Python 侧无 router 注册 | `InvoiceController.cs:307-725` | 原 C# 已提供发票信息、货物税目、办公审批 12 条接口，Python 完全缺失。 |

### Revenue

| 路由 | 归类 | Python 证据 | C# 证据 | 审计结论 |
| --- | --- | --- | --- | --- |
| `Revenue/GetREVENUEDAILYSPLITList`、`Revenue/GetREVENUEDAILYSPLITDetail`、`Revenue/SynchroREVENUEDAILYSPLIT`、`Revenue/DeleteREVENUEDAILYSPLIT`、`Revenue/GetPERSONSELLList`、`Revenue/GetPERSONSELLDetail`、`Revenue/SynchroPERSONSELL`、`Revenue/DeletePERSONSELL`、`Revenue/GetBUSINESSANALYSISList`、`Revenue/GetBUSINESSANALYSISDetail`、`Revenue/SynchroBUSINESSANALYSIS`、`Revenue/DeleteBUSINESSANALYSIS`、`Revenue/GetBRANDANALYSISList`、`Revenue/GetBRANDANALYSISDetail`、`Revenue/SynchroBRANDANALYSIS`、`Revenue/DeleteBRANDANALYSIS`、`Revenue/GetSITUATIONANALYSISList`、`Revenue/GetSITUATIONANALYSISDetail`、`Revenue/SynchroSITUATIONANALYSIS`、`Revenue/DeleteSITUATIONANALYSIS`、`Revenue/GetBUSINESSWARNINGList`、`Revenue/GetBUSINESSWARNINGDetail`、`Revenue/SynchroBUSINESSWARNING`、`Revenue/DeleteBUSINESSWARNING`、`Revenue/GetACCOUNTWARNINGList`、`Revenue/GetACCOUNTWARNINGDetail`、`Revenue/SynchroACCOUNTWARNING`、`Revenue/DeleteACCOUNTWARNING` | 逻辑不一致 | `routers/eshang_api_main/revenue/revenue_router.py:81-305`；`services/revenue/revenue_service.py:28-164`，统一走 `ENTITIES + _generic_list/_generic_detail/_generic_synchro/_generic_delete` | `API/CSharp/EShangApiMain/Controllers/Revenue/RevenueController.cs:26-977` | 7 组实体路由被压缩为同一套泛型 CRUD；原 C# 为各自 helper，`PERSONSELL` 还返回 `OtherData` 汇总，分析/预警类接口也有各自过滤和字段装配。 |
| `Revenue/ModifyRevenueDailySplitList` | 逻辑不一致 | `revenue_service.py:171-179`，仅循环调用 generic `synchro_entity` | `RevenueController.cs:1047-1075` | C# 逐条调用 `REVENUEDAILYSPLITHelper.SynchroREVENUEDAILYSPLIT` 并在失败时中断回滚；Python 退化为泛型同步。 |
| `Revenue/GetRevenuePushList` | 逻辑不一致 | `revenue_service.py:182-196`，直接查 `T_REVENUEDAILYSPLIT` | `RevenueController.cs:1085-1097` | 原接口走 `RevenuePush.GetRevenuePushList`；Python 用本地表直接替代 helper。 |
| `Revenue/GetHisCommoditySaleList` | 逻辑不一致 | `revenue_service.py:199-230`，缺失 header 权限注入，且 `db.execute_query(sql, params)` 中 `params` 未定义 | `RevenueController.cs:1118-1145` | C# 先用 header 覆盖 `ServerpartShopIds` 再调用 `CommoditySaleHelper`；Python 既少权限收敛，又存在运行期缺陷。 |
| `Revenue/GetRevenueDataList` | 逻辑不一致 | `revenue_service.py:233-263`，缺失 header 权限注入，且 `params` 未定义 | `RevenueController.cs:1158-1188` | C# 用 `GetStringHeader("ServerpartShopIds")` 做门店权限过滤并返回 `JsonList`；Python 仅本地 SQL 拼装。 |
| `Revenue/GetRevenueReport`、`Revenue/GetRevenueReportByDate`、`Revenue/GetMerchantRevenueReport` | 逻辑不一致 | `revenue_service.py:291-584` | `RevenueController.cs:1215-1379` | 原 C# 依赖 `ProvinceCode/ServerpartShopIds` 头信息和 helper 分支逻辑；Python 改为本地统计，月报/日报/商户报表口径不再等价。 |
| `Revenue/BankAccountCompare`、`Revenue/GetBankAccountReport`、`Revenue/GetBankAccountList`、`Revenue/GetCurTotalRevenue`、`Revenue/GetTotalRevenue` | 逻辑不一致 | `revenue_service.py:588-708` | `RevenueController.cs:1401-1585` | C# 侧含 header 权限、补充银行到账口径和树形/报表返回；Python 退化为本地表汇总，其中 `BankAccountCompare` 甚至返回数据列表而非“对账完成”语义。 |
| `Revenue/GetBusinessDate` | 完全一致 | `revenue_service.py:711-776` | `RevenueController.cs:1018-1044` | 营业日计算逻辑与返回语义基本一致。 |
| `Revenue/GetYSSellMasterList`、`Revenue/GetSellMasterCompareList`、`Revenue/GetYSSellDetailsList` | 完全一致 | `revenue_service.py:779-1187` | `RevenueController.cs:1606-1701` | 销售主单、对比、明细的静态实现与 C# helper 行为接近，可判定为一致。 |
| `Revenue/GetTransactionCustomer`、`Revenue/GetTransactionCustomerByDate` | 逻辑不一致 | `revenue_service.py:1207-1252`，返回扁平列表 | `RevenueController.cs:1732-1830` | 原接口返回按客户/日期组织的统计结果；Python 仅做扁平明细聚合。 |
| `Revenue/GetRevenueYOYQOQ`、`Revenue/GetRevenueYOYQOQByDate`、`Revenue/GetRevenueQOQ`、`Revenue/GetRevenueQOQByDate` | 契约不一致 | `revenue_router.py:483-507` 仅以 POST/body 暴露；`revenue_service.py:1258-2028` | `RevenueController.cs:1838-2035` | 核心同比/环比计算基本保留，但 Python 改了 HTTP 方法与入参契约，已非原接口形态。 |
| `Revenue/GetMonthCompare`、`Revenue/GetBusinessAnalysisReport`、`Revenue/GetSituationAnalysis`、`Revenue/GetBusinessTradeAnalysis`、`Revenue/GetBrandAnalysis` | 逻辑不一致 | `revenue_service.py:2232-2338` | `RevenueController.cs:2060-2268` | 原 C# 多走分析 helper 和定制报表模型；Python 以简化 SQL/自组字典替代。 |
| `Revenue/GetMonthINCAnalysis` | 完全一致 | `revenue_service.py:2340-2450` | `RevenueController.cs:2285-2305` | 月度增量分析主逻辑与 C# 对应。 |
| `Revenue/GetRevenueReportByBIZPSPLITMONTH` | 逻辑不一致 | `revenue_service.py:2454-2485` | `RevenueController.cs:2336-2359` | 原接口直接读取月度拆分报表结果；Python 以简化聚合代替，口径不等价。 |
| `Revenue/CorrectShopCigarette` | 契约不一致 | `revenue_router.py:577-584` 仅 POST；`revenue_service.py:2488-2564` | `RevenueController.cs:2381-2393` | 纠偏逻辑基本保留，但 Python 改成 POST/body 契约，已与原接口不一致。 |
| `Revenue/GetCigaretteReport` | 逻辑不一致 | `revenue_service.py:2567-2594`，未体现 `DataSourceType`、`ServerpartShopIds` 权限收敛 | `RevenueController.cs:2422-2438` | C# 通过 helper 注入权限和数据源口径；Python 仅本地查询。 |
| `Revenue/GetBusinessItemSummary` | 完全一致 | `revenue_service.py:2597-2725` | `RevenueController.cs:2474-2518` | 经营项目汇总逻辑静态可对齐。 |

### BigData

| 路由 | 归类 | Python 证据 | C# 证据 | 审计结论 |
| --- | --- | --- | --- | --- |
| `BigData/GetSECTIONFLOWList`、`BigData/GetSECTIONFLOWDetail`、`BigData/SynchroSECTIONFLOW`、`BigData/DeleteSECTIONFLOW`、`BigData/GetSECTIONFLOWMONTHList`、`BigData/GetSECTIONFLOWMONTHDetail`、`BigData/SynchroSECTIONFLOWMONTH`、`BigData/DeleteSECTIONFLOWMONTH`、`BigData/GetBAYONETList`、`BigData/GetBAYONETDetail`、`BigData/SynchroBAYONET`、`BigData/DeleteBAYONET`、`BigData/GetBAYONETDAILY_AHList`、`BigData/GetBAYONETDAILY_AHDetail`、`BigData/SynchroBAYONETDAILY_AH`、`BigData/DeleteBAYONETDAILY_AH` | 契约不一致 | `routers/eshang_api_main/bigdata/bigdata_router.py:33-137`；`services/bigdata/bigdata_service.py:27-345` | `API/CSharp/EShangApiMain/Controllers/BigData/BigDataController.cs:26-558` | Python 统一走 generic CRUD 和 `Result/JsonListData` 包装；C# 为原始 `JsonMsg<JsonList<...>>` 模型与实体特定 helper，接口契约已漂移。 |
| `Revenue/GetBAYONETANALYSISList`、`Revenue/GetBAYONETANALYSISDetail`、`Revenue/SynchroBAYONETANALYSIS`、`Revenue/DeleteBAYONETANALYSIS` | 契约不一致 | `bigdata_router.py:142-145`；`bigdata_service.py:27-345` | `BigDataController.cs:745-847` | baseline JSON 误标为缺失，但 Python 路由实际存在；不过实现仍是 generic CRUD，未恢复原 C# 契约与模型。 |
| `Revenue/GetBAYONETOAANALYSISList`、`Revenue/GetBAYONETOAANALYSISDetail`、`Revenue/SynchroBAYONETOAANALYSIS`、`Revenue/DeleteBAYONETOAANALYSIS` | 契约不一致 | `bigdata_router.py:150-153`；`bigdata_service.py:27-345` | `BigDataController.cs:886-988` | 同上，baseline 误标缺失；Python 实际存在，但仅为通用 CRUD。 |
| `BigData/GetBAYONETWARNINGList` | 契约不一致 | `bigdata_router.py:156-158`；`bigdata_service.py:198-262` | `BigDataController.cs:1028-1064` | 仅列表路由存在，且仍为 generic CRUD 包装。 |
| `BigData/GetBAYONETWARNINGDetail`、`BigData/SynchroBAYONETWARNING`、`BigData/DeleteBAYONETWARNING` | Python 缺失 | `full_audit_baseline_20260309.json` 中存在，Python router 未注册 | `BigDataController.cs:1066-1138` | `BAYONETWARNING` 仅迁了 List，Detail/Sync/Delete 3 条均未迁移。 |
| `Customer/GetCUSTOMERGROUP_AMOUNTList` | 逻辑不一致 | `bigdata_router.py:163-166`；`bigdata_service.py:530-565` 缺失 header `ServerpartCodes` 收敛 | `API/CSharp/EShangApiMain/Controllers/BigData/CustomerController.cs:23-45` | C# 从 header 注入服务区权限再查客户群金额；Python 直接查表，权限口径丢失。 |
| `Customer/GetCUSTOMERGROUP_AMOUNTDetail`、`Customer/SynchroCUSTOMERGROUP_AMOUNT`、`Customer/DeleteCUSTOMERGROUP_AMOUNT` | 契约不一致 | `bigdata_router.py:163-166`；`bigdata_service.py:27-345` | `CustomerController.cs:64-140` | Python 仍是 generic CRUD 返回壳，未对齐原接口模型。 |
| `BigData/A2305052305180725` | 契约不一致 | `bigdata_router.py:173-187`；`bigdata_service.py:352-425` | `BigDataController.cs:605-652` | Python 用统一 `Result.success` 包装日汇总数据；原接口为 BigDataController 专用返回结构。 |
| `BigData/GetDailyBayonetAnalysis` | 逻辑不一致 | `bigdata_service.py:428-435` 直接复用 `get_bayonet_daily_summary` | `BigDataController.cs:654-701` | 原 C# 为独立日分析 helper；Python 直接复用上一接口逻辑。 |
| `BigData/GetServerpartSectionFlow` | 逻辑不一致 | `bigdata_service.py:438-512` | `BigDataController.cs:703-742` | 原接口为片区/服务区流量分析 helper；Python 简化为本地聚合，结果口径有漂移。 |
| `Revenue/GetBayonetVehicleAnalysis` | 契约不一致 | `bigdata_router.py:225-230`；`bigdata_service.py:515-527` | `BigDataController.cs:1181-1218` | baseline JSON 误标缺失，但 Python 路由实际存在；只是返回壳与原 C# 模型不一致。 |
| `BigData/GetTimeIntervalList`、`BigData/GetBayonetOwnerAHList`、`BigData/GetBayonetOwnerMonthAHList`、`BigData/GetUreaMasterList` | 契约不一致 | `bigdata_router.py:232-289`；`bigdata_service.py:530-688` | `BigDataController.cs:1221-1375` | C# 侧为专用模型/分页返回；Python 统一包装为 `Result.success`，契约未对齐。 |

### MobilePay

| 路由 | 归类 | Python 证据 | C# 证据 | 审计结论 |
| --- | --- | --- | --- | --- |
| `MobilePay/SetKwyRoyaltyRate`、`MobilePay/GetKwyRoyaltyRate`、`MobilePay/GetKwyRoyalty`、`MobilePay/GetKwyRoyaltyForAll` | 逻辑不一致 | `routers/eshang_api_main/batch_modules/batch_router_part1.py:143-190`；`services/mobilepay/mobilepay_service.py:26-63` | `API/CSharp/EShangApiMain/Controllers/MobilePay/MobilePayController.cs:29-223` | C# 统一调用 `MobilePayHelper` 访问外部支付侧数据；Python 改成本地 `T_SERVERPARTSHOP/T_ROYALTYRECORD` 读写，语义已变。 |
| `MobilePay/RoyaltyWithdraw`、`MobilePay/GetMobilePayRoyaltyReport` | 占位实现 | `mobilepay_service.py:42-68`，分别 `return True` 与 `return []` | `MobilePayController.cs:125-305` | 提现与分润报表原本依赖外部 helper 和权限头信息；Python 仅保留壳接口。 |
| `MobilePay/SynchroBANKACCOUNTVERIFY`、`MobilePay/GetBANKACCOUNTVERIFYList`、`MobilePay/GetBANKACCOUNTVERIFYRegionList`、`MobilePay/GetBANKACCOUNTVERIFYServerList`、`MobilePay/GetBANKACCOUNTVERIFYTreeList` | 逻辑不一致 | `mobilepay_service.py:70-115` | `MobilePayController.cs:316-596` | C# 侧有校验、树形组装、header 权限与 helper 逻辑；Python 只做本地表增删查与简单树。 |
| `MobilePay/GetRoyaltyRecordList`、`MobilePay/GetMobilePayResult` | 逻辑不一致 | `mobilepay_service.py:117-125` | `MobilePayController.cs:619-679` | 原实现分别调用 `GetRoyaltyRecordList` 与 `GetMobilePayResult` helper；Python 都退化为本地记录查询。 |
| `MobilePay/CorrectSellMasterState` | Python 缺失 | `full_audit_baseline_20260309.json` 中存在，Python router 未注册 | `MobilePayController.cs:702-713` | C# 的销售主单纠偏接口未迁移。 |
| `MobilePay/GetChinaUmsSubMaster`、`MobilePay/GetChinaUmsSubAccountDetail`、`MobilePay/GetChinaUmsSubAccountSummary`、`MobilePay/GetChinaUmsSubSummary` | 逻辑不一致 | `mobilepay_service.py:127-145` | `MobilePayController.cs:738-867` | 原 C# 依赖 `ChinaUmsSubHelper` 做银联子账户主单/明细/汇总查询；Python 直接查本地表，外部接口语义已丢失。 |

## 模块整改建议

### Finance

- 优先重做 `finance_scattered_service.py` 中所有“简化版/直接成功/空列表”接口，先恢复审批流、固化/拆分/生成、对账、短信/提单等核心 helper 逻辑。
- 补齐 Budget 报表族缺失实现，尤其 `GetbudgetProjectReport*` 动态列与进出项接口。
- 补齐 Invoice/Office 缺失 12 条路由，并修正 `GetBILLDetail` 的 `ApproveList`、`ForwardJDPJInterface` 的 `access_token` 转发。

### Revenue

- 拆掉当前 generic CRUD 覆盖 7 组实体的做法，恢复 entity-specific helper 与 `OtherData`/分析模型。
- 全面补回 header 权限收敛：`ServerpartShopIds`、`ProvinceCode`、`DataSourceType` 等必须按 C# 入口处理。
- 修复 `GetHisCommoditySaleList`、`GetRevenueDataList` 中未定义 `params` 的硬错误，再对齐报表/对账/同比环比的原契约。

### BigData

- 先补齐 `BAYONETWARNING` 的 Detail/Sync/Delete 3 条真实缺失路由。
- 将 `BAYONETANALYSIS`、`BAYONETOAANALYSIS`、`CUSTOMERGROUP_AMOUNT` 从 generic CRUD 恢复为原控制器模型与权限逻辑。
- 校正 BigData 模块路由映射口径，避免 baseline 将已存在的 `Revenue/*` 路由误记为缺失。

### MobilePay

- 恢复 `MobilePayHelper` 与 `ChinaUmsSubHelper` 外部调用链，不应以本地表查询替代外部支付/银联语义。
- 补齐 `CorrectSellMasterState`，并重做 `RoyaltyWithdraw`、`GetMobilePayRoyaltyReport` 两个占位接口。
- `BANKACCOUNTVERIFY` 相关接口需恢复原校验、树形、header 权限与报表逻辑，不能仅靠单表 CRUD。

## 风险与阻塞

- 本次为静态审计，未连接外部 SOAP、金蝶、航信、MobilePay/ChinaUMS 真实环境；凡 C# 明确调用外部 helper 而 Python 退化成本地表查询的接口，已按“逻辑不一致/占位实现”判定。
- BigData baseline 存在 9 条 `Revenue/*` 路由误标缺失：`Get/Delete/Sync BAYONETANALYSIS`、`Get/Delete/Sync BAYONETOAANALYSIS`、`GetBayonetVehicleAnalysis`。本次仍按 baseline 路由清单做全量覆盖，但在审计结论中按实际代码存在情况归类。
- 对于控制器能追到但 helper 实现不完全位于当前仓库的场景，本次以控制器调用语义、返回模型、header 权限和已能追到的 helper 片段为依据；若 Python 已明显退化为单表 CRUD、空返回或直接成功，已可静态确定为不一致。
