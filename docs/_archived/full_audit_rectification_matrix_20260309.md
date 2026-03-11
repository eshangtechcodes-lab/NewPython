# 全量接口整改矩阵（2026-03-09）

## 1. 使用说明

这份文档不是总览结论，而是可执行整改台账。

使用原则：

- 只记录“不完全一致 / 占位实现 / Python 缺失 / Python 多出”的接口。
- 不再只说“某模块有问题”，而是明确到“哪组接口有问题、和原 C# 哪段逻辑不一致、应该怎么改”。
- 每个整改包都给出：
  - 涉及接口
  - 当前偏差
  - 对应 C# 逻辑
  - 整改动作
  - 实施批次
  - 验收重点

静态证据来源：

- [full_audit_window_1_result.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_window_1_result.md)
- [full_audit_window_2_result.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_window_2_result.md)
- [full_audit_window_3_result.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_window_3_result.md)
- [full_audit_window_4_result.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_window_4_result.md)

## 2. 批次定义

- `B1`：公共契约兼容层整改
- `B2`：P0 流程/状态机/附件/文件接口整改
- `B3`：helper 级业务语义回迁
- `B4`：缺失路由补齐
- `B5`：动态联调与回归验收

## 3. 接口级整改矩阵

**BaseInfo / Merchants**
- `BM-01 Header/Token/HTTP 方法兼容包`
  接口：`BaseInfo/GetServerpartShopList`、`BaseInfo/GetServerpartShopDetail`、`BaseInfo/DelServerpartShop`、`BaseInfo/GetUSERDEFINEDTYPEList`、`BaseInfo/DeleteUSERDEFINEDTYPE`、`BaseInfo/CreatePriceType`、`BaseInfo/BindingOwnerUnitDDL`、`BaseInfo/GetServerpartUDTypeTree`、`BaseInfo/GetServerPartShopNewList`、`BaseInfo/ServerPartShopNewSaveState`、`Merchants/GetCoopMerchantsList`、`Merchants/GetCoopMerchantsTypeList`、`Merchants/GetTradeBrandMerchantsList`
  当前偏差：漏读 `ProvinceCode`、`ServerpartCodes`、`ServerpartShopIds`、`UserPattern`、`Token`；部分接口 GET/POST 放宽或收窄；`GetServerpartUDTypeTree` 还把 C# 的可选参数裁成了必填。
  对应 C# 逻辑：BaseInfoController、MerchantsController 依赖 Header 回填权限和操作人上下文，部分接口还有超级管理员分支与空列表短路。
  整改动作：先做 BaseInfo/Merchants 公共上下文注入层，再逐路由恢复原 Header 回填、原 HTTP 方法和原参数可选性。
  实施批次：`B1`
  验收重点：同一组请求在有无 `ProvinceCode`、`UserPattern=2000/9000`、不同 `Token` 下，返回范围必须与 C# 一致。

- `BM-02 Commodity / PropertyAssets 简化逻辑回迁包`
  接口：`BaseInfo/SynchroCOMMODITY`、`Commodity/SyncCommodityInfo_AHJG`、`BaseInfo/GetPROPERTYASSETSList`、`BaseInfo/GetPROPERTYASSETSTreeList`、`BaseInfo/BatchPROPERTYASSETS`
  当前偏差：Python 以“简化版”或占位实现替代原 helper，缺编码/条码生成、下发指令、门店关联、树形汇总、副作用。
  对应 C# 逻辑：CommodityController、PROPERTYASSETSHelper 负责生成编码、同步、树构建、未匹配门店和批量关联。
  整改动作：不要继续保留“标准 CRUD + 少量拼接”方案，直接按原 helper 迁回同步、副作用和树形统计。
  实施批次：`B3`
  验收重点：编码生成、树结构、门店关联、批量设置副作用与 C# 对齐。

- `BM-03 Merchants 缺失路由补齐包`
  接口：`Merchants/GetCoopMerchantsDDL`
  当前偏差：原 C# 路由存在，Python 运行时缺失。
  对应 C# 逻辑：MerchantsController 提供下拉选择接口。
  整改动作：补 router、service、helper 对应实现。
  实施批次：`B4`
  验收重点：返回格式和权限范围与 C# 一致。

**Contract**
- `CT-01 RegisterCompact 主链回迁包`
  接口：`Contract/GetRegisterCompactList`、`Contract/SynchroRegisterCompact`、`Contract/DeleteRegisterCompact`、`Contract/SynchroRegisterCompactSub`、`Contract/AddContractSupplement`
  当前偏差：`ProvinceCode`、`Token`、操作人、历史备份、变更日志、失败信息、删除校验被裁掉；主合同补充协议逻辑退化成普通 upsert。
  对应 C# 逻辑：ContractController、REGISTERCOMPACTHelper、REGISTERCOMPACTSUBHelper 依赖 Token、权限解析、历史日志、失败原因和 ForceDelete 分支。
  整改动作：先恢复 Token/用户上下文，再按 helper 回迁删除检查、历史备份、补充协议和日志链路。
  实施批次：`B2`
  验收重点：删除失败原因、日志落库、历史记录、补充协议校验要和 C# 一致。

- `CT-02 附件文件接口整改包`
  接口：`Contract/SaveAttachment`、`Contract/DelFile`
  当前偏差：Python 明确写成占位接口，未接文件系统。
  对应 C# 逻辑：ATTACHMENTHelper.SaveAttachment / DelFile 会落物理文件并返回失败原因。
  整改动作：接入文件存储路径、删除逻辑、异常处理与回滚语义。
  实施批次：`B2`
  验收重点：真实上传、删除、文件路径和错误返回。

- `CT-03 ProjectSummary / GetFromRedis 兼容包`
  接口：`Contract/GetProjectSummaryInfo`、`Contract/GetContractExpiredInfo`、`Contract/GetProjectYearlyArrearageList`、`Contract/GetProjectMonthlyArrearageList`
  当前偏差：Python 接口表面接收 `GetFromRedis`，但没有真正透传到 service/helper；部分默认年份也和 C# 不一致。
  对应 C# 逻辑：ProjectSummaryHelper 区分缓存分支和实时分支。
  整改动作：恢复 `GetFromRedis` 透传、默认值、缓存/实时双路径。
  实施批次：`B1`
  验收重点：同参在缓存和非缓存模式下输出必须可对比。

- `CT-04 BusinessProject 汇总/审批/费用包`
  接口：`BusinessProject/GetBusinessProjectList`、`BusinessProject/GetBUSINESSPROJECTSPLITList`、`BusinessProject/GetBIZPSPLITMONTHDetail`、`BusinessProject/GetPROJECTWARNINGList`、`BusinessProject/GetPROJECTWARNINGDetail`、`BusinessProject/GetPERIODWARNINGList`、`BusinessProject/GetSHOPEXPENSEList`、`BusinessProject/SynchroSHOPEXPENSE`、`BusinessProject/DeleteSHOPEXPENSE`、`BusinessProject/GetMerchantsReceivablesList`、`BusinessProject/GetMerchantsReceivables`
  当前偏差：权限 Header 丢失，`summaryObject`、审批状态、四表 JOIN、`ModuleGuid`、`SourcePlatform`、历史作废、级联拆分都被简化。
  对应 C# 逻辑：BUSINESSPROJECTSPLITHelper、PROJECTWARNINGHelper、SHOPEXPENSEHelper、COOPMERCHANTSHelper。
  整改动作：按 helper 拆成三段回迁：
  费用/拆分链：`GetBUSINESSPROJECTSPLITList`、`GetSHOPEXPENSEList`、`SynchroSHOPEXPENSE`、`DeleteSHOPEXPENSE`
  预警链：`GetPROJECTWARNINGList`、`GetPROJECTWARNINGDetail`、`GetPERIODWARNINGList`
  商户应收链：`GetMerchantsReceivablesList`、`GetMerchantsReceivables`
  实施批次：`B3`
  验收重点：`summaryObject`、`OtherData`、审批状态、平台分支、历史作废记录。

- `CT-05 Contract 缺失路由补齐包`
  接口：`Contract/GetContractYearList`、`Contract/GetShopBusinessTypeRatio`
  当前偏差：原 C# 有，Python 缺失。
  对应 C# 逻辑：ContractController 对应列表/统计接口。
  整改动作：补 route/service/helper；补完后纳入动态对比。
  实施批次：`B4`
  验收重点：年份集合、业态占比统计口径。

**Finance**
- `FI-01 Budget 报表族回迁包`
  接口：`Budget/GetBudgetProjectReportOfMonth`、`Budget/GetbudgetProjectReport`、`Budget/GetbudgetProjectReportDynamic`、`Budget/GetbudgetProjectReportIn`、`Budget/GetbudgetProjectReportInDynamic`、`Budget/GetbudgetProjectReportOut`、`Budget/GetbudgetProjectReportOutDynamic`
  当前偏差：`GetBudgetProjectReportOfMonth` 返回结构漂移；其余多条接口为空字符串或未实现。
  对应 C# 逻辑：BudgetProjectAHController 下为完整动态列、进出项、月份报表。
  整改动作：不要在现有 service 上打补丁，直接按 C# 报表族逐条恢复。
  实施批次：`B2`
  验收重点：动态列、月份维度、进/出项字段和包结构一致。

- `FI-02 Finance 散装汇总/对账简化包`
  接口：`Finance/GetProjectSplitSummary`、`Finance/GetProjectSummary`、`Finance/GetRevenueSplitSummary`、`Finance/GetProjectMerchantSummary`、`Finance/GetRoyaltyDateSumReport`、`Finance/GetRoyaltyReport`、`Finance/GetProjectShopIncome`、`Finance/GetContractMerchant`、`Finance/GetAccountReached`、`Finance/GetShopExpense`、`Finance/GetReconciliation`、`Finance/GetProjectExpenseList`、`Finance/GetProjectPeriodAccount`
  当前偏差：多个不同接口被合并成同一套简化 SQL 或空壳，树形、`OtherData`、对账结果、日期对比字段都丢失。
  对应 C# 逻辑：BUSINESSPROJECTSPLITHelper、ProjectSummaryHelper、FinanceHelper 各自负责不同结果模型。
  整改动作：按 helper 重新拆分 service，禁止多个路由复用同一个“简化版”查询。
  实施批次：`B3`
  验收重点：接口间不能再互相复用错误结果；汇总模型必须恢复。

- `FI-03 审批流 / 固化 / 生成 / 补录占位清理包`
  接口：`Finance/CreateSingleProjectSplit`、`Finance/SolidMonthProjectSplit`、`Finance/GetRevenueRecognition`、`Finance/GetProjectPeriodIncome`、`Finance/ApplyAccountProinst`、`Finance/ApproveAccountProinst`、`Finance/RejectAccountProinst`、`Finance/GetMonthAccountProinst`、`Finance/ApplyMonthAccountProinst`、`Finance/ApproveMonthAccountProinst`、`Finance/ApproveMAPList`、`Finance/RejectMonthAccountProinst`、`Finance/StorageMonthProjectAccount`、`Finance/GetMonthAccountDiff`、`Finance/ApprovePeriodAccount`、`Finance/RejectPeriodAccount`、`Finance/GetPeriodSupplementList`、`Finance/GetBankAccountAnalyseList`、`Finance/GetBankAccountAnalyseTreeList`、`Finance/SolidBankAccountSplit`
  当前偏差：大量接口直接 `return True`、`return []` 或“简化版”，本质上未迁移。
  对应 C# 逻辑：FinanceController 下是完整审批和固化流程。
  整改动作：全部下掉“已迁移完成”状态，按流程接口优先级重做；先审批，再固化，再补录/分析。
  实施批次：`B2`
  验收重点：状态流转、批量审核、差异计算、银行分析树必须真实生效。

- `FI-04 高级流程/外部能力回迁包`
  接口：`Finance/GetContractExcuteAnalysis`、`Finance/RebuildSCSplit`、`Finance/CorrectRevenueAccountData`、`Finance/RebuildClosedPeriod`、`Finance/RebuildReductionPeriod`、`Finance/SendSMSMessage`、`Finance/LadingBill`、`Finance/RejectLadingBill`、`Finance/GetAHJKtoken`、`Finance/GetAccountCompare`、`Finance/GetAnnualAccountList`
  当前偏差：仍是占位或直接成功。
  对应 C# 逻辑：FinanceController 对应重算、短信、提单、对账、年报流程。
  整改动作：按“重算类 / 提单类 / 外部 token 类 / 分析报表类”拆 4 个子任务。
  实施批次：`B2`
  验收重点：不能再返回空值；每条接口都要有真实行为和失败分支。

- `FI-05 Invoice / Office 补齐与兼容包`
  接口：`Invoice/GetBILLDetail`、`Invoice/SendHXInvoiceInfo`、`Invoice/ForwardJDPJInterface`、`Invoice/GetINVOICEINFOList`、`Invoice/GetINVOICEINFODetail`、`Invoice/SynchroINVOICEINFO`、`Invoice/DeleteINVOICEINFO`、`Invoice/GetGOODSTAXINFOList`、`Invoice/GetGOODSTAXINFODetail`、`Invoice/SynchroGOODSTAXINFO`、`Invoice/DeleteGOODSTAXINFO`、`Office/GetAPPLYAPPROVEList`、`Office/GetAPPLYAPPROVEDetail`、`Office/SynchroAPPLYAPPROVE`、`Office/DeleteAPPLYAPPROVE`
  当前偏差：`GetBILLDetail` 少 `ApproveList`；`SendHXInvoiceInfo` 是占位；`ForwardJDPJInterface` 少 `access_token`；其余 12 条直接缺失。
  对应 C# 逻辑：InvoiceController、OfficeController。
  整改动作：先补缺失路由，再补外部转发与审批意见链。
  实施批次：`B4`
  验收重点：票据审批记录、转发 Header、Office 审批 CRUD 契约一致。

**Revenue**
- `RE-01 7 组实体 CRUD 契约与等价性复核包`
  接口：`Revenue/GetREVENUEDAILYSPLITList`、`Revenue/GetREVENUEDAILYSPLITDetail`、`Revenue/SynchroREVENUEDAILYSPLIT`、`Revenue/DeleteREVENUEDAILYSPLIT`、`Revenue/GetPERSONSELLList`、`Revenue/GetPERSONSELLDetail`、`Revenue/SynchroPERSONSELL`、`Revenue/DeletePERSONSELL`、`Revenue/GetBUSINESSANALYSISList`、`Revenue/GetBUSINESSANALYSISDetail`、`Revenue/SynchroBUSINESSANALYSIS`、`Revenue/DeleteBUSINESSANALYSIS`、`Revenue/GetBRANDANALYSISList`、`Revenue/GetBRANDANALYSISDetail`、`Revenue/SynchroBRANDANALYSIS`、`Revenue/DeleteBRANDANALYSIS`、`Revenue/GetSITUATIONANALYSISList`、`Revenue/GetSITUATIONANALYSISDetail`、`Revenue/SynchroSITUATIONANALYSIS`、`Revenue/DeleteSITUATIONANALYSIS`、`Revenue/GetBUSINESSWARNINGList`、`Revenue/GetBUSINESSWARNINGDetail`、`Revenue/SynchroBUSINESSWARNING`、`Revenue/DeleteBUSINESSWARNING`、`Revenue/GetACCOUNTWARNINGList`、`Revenue/GetACCOUNTWARNINGDetail`、`Revenue/SynchroACCOUNTWARNING`、`Revenue/DeleteACCOUNTWARNING`
  当前偏差：7 组实体目前使用 generic CRUD 实现；这一点本身不等于错误，但返回包装、参数模型、主键/状态字段、`PERSONSELL` 的汇总/`OtherData` 是否与各自 helper 等价，当前尚未逐组证实。
  对应 C# 逻辑：RevenueController 下每组实体都有独立 helper。
  整改动作：保留 generic CRUD 作为实现底座，逐实体核对表名、主键、状态字段、返回包装和 `OtherData`；只有确认与原 helper 不等价的实体才拆出独立 service/helper。
  实施批次：`B1`
  验收重点：7 组实体逐组完成 list/detail/synchro/delete 契约与字段级对比，`PERSONSELL` 额外核对汇总和 `OtherData`。

- `RE-02 收入报表/对账/分析包`
  接口：`Revenue/ModifyRevenueDailySplitList`、`Revenue/GetRevenuePushList`、`Revenue/GetHisCommoditySaleList`、`Revenue/GetRevenueDataList`、`Revenue/GetRevenueReport`、`Revenue/GetRevenueReportByDate`、`Revenue/GetMerchantRevenueReport`、`Revenue/BankAccountCompare`、`Revenue/GetBankAccountReport`、`Revenue/GetBankAccountList`、`Revenue/GetCurTotalRevenue`、`Revenue/GetTotalRevenue`、`Revenue/GetTransactionCustomer`、`Revenue/GetTransactionCustomerByDate`、`Revenue/GetMonthCompare`、`Revenue/GetBusinessAnalysisReport`、`Revenue/GetSituationAnalysis`、`Revenue/GetBusinessTradeAnalysis`、`Revenue/GetBrandAnalysis`、`Revenue/GetRevenueReportByBIZPSPLITMONTH`、`Revenue/GetCigaretteReport`
  当前偏差：Python 已有大量实际 SQL/聚合逻辑，并非空实现；但权限 Header 仍有缺漏，`GetHisCommoditySaleList` 与 `GetRevenueDataList` 存在 `params` 未定义的运行时错误，与原 helper 的口径等价性仍未逐条证实。
  对应 C# 逻辑：RevenueController、CommoditySaleHelper、对账 helper、分析 helper。
  整改动作：先修运行时错误和 Header 透传，再按“销售明细 / 收入报表 / 对账 / 分析”四条链做 SOP 深比对；仅对确认不等价的链路重构。
  实施批次：`B3`
  验收重点：Header 权限、客户统计、银行对账、按月/按日统计口径，以及已知运行时错误清零。

- `RE-03 方法与契约漂移包`
  接口：`Revenue/GetRevenueYOYQOQ`、`Revenue/GetRevenueYOYQOQByDate`、`Revenue/GetRevenueQOQ`、`Revenue/GetRevenueQOQByDate`、`Revenue/CorrectShopCigarette`
  当前偏差：核心计算可能还在，但 HTTP 方法和入参契约已改。
  对应 C# 逻辑：RevenueController 保持原 GET/POST 与 query/body 形态。
  整改动作：先恢复契约，再做动态回归。
  实施批次：`B1`
  验收重点：相同请求参数下，新旧接口可直接互换调用。

**BigData**
- `BG-01 实体 CRUD 契约回迁包`
  接口：`BigData/GetSECTIONFLOWList`、`BigData/GetSECTIONFLOWDetail`、`BigData/SynchroSECTIONFLOW`、`BigData/DeleteSECTIONFLOW`、`BigData/GetSECTIONFLOWMONTHList`、`BigData/GetSECTIONFLOWMONTHDetail`、`BigData/SynchroSECTIONFLOWMONTH`、`BigData/DeleteSECTIONFLOWMONTH`、`BigData/GetBAYONETList`、`BigData/GetBAYONETDetail`、`BigData/SynchroBAYONET`、`BigData/DeleteBAYONET`、`BigData/GetBAYONETDAILY_AHList`、`BigData/GetBAYONETDAILY_AHDetail`、`BigData/SynchroBAYONETDAILY_AH`、`BigData/DeleteBAYONETDAILY_AH`、`Revenue/GetBAYONETANALYSISList`、`Revenue/GetBAYONETANALYSISDetail`、`Revenue/SynchroBAYONETANALYSIS`、`Revenue/DeleteBAYONETANALYSIS`、`Revenue/GetBAYONETOAANALYSISList`、`Revenue/GetBAYONETOAANALYSISDetail`、`Revenue/SynchroBAYONETOAANALYSIS`、`Revenue/DeleteBAYONETOAANALYSIS`、`BigData/GetBAYONETWARNINGList`、`Customer/GetCUSTOMERGROUP_AMOUNTList`、`Customer/GetCUSTOMERGROUP_AMOUNTDetail`、`Customer/SynchroCUSTOMERGROUP_AMOUNT`、`Customer/DeleteCUSTOMERGROUP_AMOUNT`
  当前偏差：统一壳包装替代原 `JsonMsg<JsonList<...>>`，Customer 还漏 `ServerpartCodes` 权限。
  对应 C# 逻辑：BigDataController、CustomerController 对各实体有专用模型和权限分支。
  整改动作：拆除 generic CRUD 包装，恢复原模型、原返回壳、原 Header 处理。
  实施批次：`B1`
  验收重点：结果包、字段名、Customer 权限范围、Bayonet 各实体模型一致。

- `BG-02 BigData 报表/分析逻辑包`
  接口：`BigData/A2305052305180725`、`BigData/GetDailyBayonetAnalysis`、`BigData/GetServerpartSectionFlow`、`Revenue/GetBayonetVehicleAnalysis`、`BigData/GetTimeIntervalList`、`BigData/GetBayonetOwnerAHList`、`BigData/GetBayonetOwnerMonthAHList`、`BigData/GetUreaMasterList`
  当前偏差：多个接口直接复用前一个接口或简化成本地聚合，结果模型与 C# 专用模型不一致。
  对应 C# 逻辑：BigDataController 中各接口独立实现分析和时间区间逻辑。
  整改动作：按报表接口逐条回迁，禁止复用错误 service。
  实施批次：`B3`
  验收重点：时间区间、车流量、归属分析、尿素主单结果结构。

- `BG-03 缺失路由补齐包`
  接口：`BigData/GetBAYONETWARNINGDetail`、`BigData/SynchroBAYONETWARNING`、`BigData/DeleteBAYONETWARNING`
  当前偏差：原 C# 有，Python 缺失。
  对应 C# 逻辑：BigDataController 对 `BAYONETWARNING` 提供完整 CRUD。
  整改动作：补 router、service、helper 逻辑，并恢复与 `GetBAYONETWARNINGList` 的统一实体语义。
  实施批次：`B4`
  验收重点：列表/明细/同步/删除四条闭环。

**MobilePay**
- `MP-01 外部支付/银联语义回迁包`
  接口：`MobilePay/SetKwyRoyaltyRate`、`MobilePay/GetKwyRoyaltyRate`、`MobilePay/GetKwyRoyalty`、`MobilePay/GetKwyRoyaltyForAll`、`MobilePay/SynchroBANKACCOUNTVERIFY`、`MobilePay/GetBANKACCOUNTVERIFYList`、`MobilePay/GetBANKACCOUNTVERIFYRegionList`、`MobilePay/GetBANKACCOUNTVERIFYServerList`、`MobilePay/GetBANKACCOUNTVERIFYTreeList`、`MobilePay/GetRoyaltyRecordList`、`MobilePay/GetMobilePayResult`、`MobilePay/GetChinaUmsSubMaster`、`MobilePay/GetChinaUmsSubAccountDetail`、`MobilePay/GetChinaUmsSubAccountSummary`、`MobilePay/GetChinaUmsSubSummary`
  当前偏差：C# 通过 `MobilePayHelper` / `ChinaUmsSubHelper` 访问外部支付和银联能力，Python 改成本地表查询或简单树。
  对应 C# 逻辑：MobilePayController 不是本地 CRUD 模块，而是支付聚合模块。
  整改动作：恢复 helper 外部调用链、权限 Header、结果模型；停止用本地表兜底。
  实施批次：`B2`
  验收重点：分润、银联对账、银行对账树和外部接口返回必须真实生效。

- `MP-02 占位接口清理包`
  接口：`MobilePay/RoyaltyWithdraw`、`MobilePay/GetMobilePayRoyaltyReport`
  当前偏差：一个直接成功，一个直接空列表。
  对应 C# 逻辑：提现和分润报表均为真实 helper 流程。
  整改动作：补真实提现/报表逻辑，未补齐前不允许标记完成。
  实施批次：`B2`
  验收重点：提现动作和分润报表均需真实返回。

- `MP-03 缺失路由补齐包`
  接口：`MobilePay/CorrectSellMasterState`
  当前偏差：C# 有，Python 缺失。
  对应 C# 逻辑：销售主单纠偏接口。
  整改动作：补 route/service/helper。
  实施批次：`B4`
  验收重点：纠偏后销售主单状态与 C# 一致。

**Audit**
- `AU-01 实体 CRUD 契约修复包`
  接口：`Audit/GetYSABNORMALITYList`、`Audit/GetYSABNORMALITYDetail`、`Audit/GetYSABNORMALITYDETAILList`、`Audit/GetABNORMALAUDITList`、`Audit/GetAbnormalAuditDetail`、`Audit/SynchroAbnormalAudit`、`Audit/DeleteAbnormalAudit`、`Audit/GetCHECKACCOUNTList`、`Audit/GetCHECKACCOUNTDetail`、`Audit/SynchroCHECKACCOUNT`、`Audit/DeleteCHECKACCOUNT`、`Audit/GetAUDITTASKSList`、`Audit/GetAUDITTASKSDetail`、`Audit/SynchroAUDITTASKS`
  当前偏差：Audit 这组接口并不存在 `pk_val` 问题，但仍被 generic CRUD、`data: dict` 和小写包装覆盖，强类型 SearchModel/JsonMsg 契约丢失。
  对应 C# 逻辑：AuditController 下每组实体都有独立 SearchModel、详情模型和 helper。
  整改动作：保留现有实体参数名，优先修响应包装、强类型输入模型和同步/列表契约；不再按 `pk_val` 问题处理。
  实施批次：`B1`
  验收重点：详情/删除参数名、返回壳、列表查询条件、同步入参与 C# 兼容。

- `AU-02 稽核流程 / 报表 / 下发回迁包`
  接口：`Audit/GetAuditList`、`Audit/GetAuditDetils`、`Audit/UpLoadAuditExplain`、`Audit/GetCheckAccountReport`、`Audit/GetYsabnormalityReport`、`Audit/GetSpecialBehaviorReport`、`Audit/GetAbnormalRateReport`、`Audit/GetAuditTasksReport`、`Audit/GetAuditTasksDetailList`、`Audit/IssueAuditTasks`
  当前偏差：需拆分处理。`GetSpecialBehaviorReport`、`GetAbnormalRateReport` 属于纯占位；`GetAuditDetils`、`UpLoadAuditExplain`、`IssueAuditTasks`、`GetAuditTasksDetailList` 错误复用通用 CRUD；`GetAuditList`、`GetCheckAccountReport`、`GetYsabnormalityReport`、`GetAuditTasksReport` 已有 SQL，但与原 helper 是否等价仍需深比对。
  对应 C# 逻辑：ESCG.Audit、AuditHelper、IssueAuditTasksModel。
  整改动作：先修纯占位和错误复用接口，再对已有 SQL 的报表/列表按 SOP 做深比对，不预设全部重写。
  实施批次：`B2`
  验收重点：图片/说明上传、报表层级、任务下发副作用、任务明细结果，并区分“纯补实现”和“深比对微调”两类验收。

**Analysis**
- `AN-01 11 组实体 CRUD 壳化治理包`
  接口：`Analysis/GetANALYSISINSList`、`Analysis/GetANALYSISINSDetail`、`Analysis/SynchroANALYSISINS`、`Analysis/DeleteANALYSISINS`、`Analysis/GetSENTENCEList`、`Analysis/GetSENTENCEDetail`、`Analysis/SynchroSENTENCE`、`Analysis/DeleteSENTENCE`、`Analysis/GetASSETSPROFITSList`、`Analysis/GetASSETSPROFITSDetail`、`Analysis/SynchroASSETSPROFITS`、`Analysis/DeleteASSETSPROFITS`、`Analysis/GetPROFITCONTRIBUTEList`、`Analysis/GetPROFITCONTRIBUTEDetail`、`Analysis/SynchroPROFITCONTRIBUTE`、`Analysis/DeletePROFITCONTRIBUTE`、`Analysis/GetPERIODMONTHPROFITList`、`Analysis/GetPERIODMONTHPROFITDetail`、`Analysis/SynchroPERIODMONTHPROFIT`、`Analysis/DeletePERIODMONTHPROFIT`、`Analysis/GetVEHICLEAMOUNTList`、`Analysis/GetVEHICLEAMOUNTDetail`、`Analysis/SynchroVEHICLEAMOUNT`、`Analysis/DeleteVEHICLEAMOUNT`、`Analysis/GetANALYSISRULEList`、`Analysis/GetANALYSISRULEDetail`、`Analysis/SynchroANALYSISRULE`、`Analysis/DeleteANALYSISRULE`、`Analysis/GetPREFERRED_RATINGList`、`Analysis/GetPREFERRED_RATINGDetail`、`Analysis/SynchroPREFERRED_RATING`、`Analysis/DeletePREFERRED_RATING`、`Analysis/GetPROMPTList`、`Analysis/GetPROMPTDetail`、`Analysis/SynchroPROMPT`、`Analysis/DeletePROMPT`、`Analysis/GetINVESTMENTANALYSISList`、`Analysis/GetINVESTMENTANALYSISDetail`、`Analysis/SynchroINVESTMENTANALYSIS`、`Analysis/DeleteINVESTMENTANALYSIS`、`Analysis/GetINVESTMENTDETAILList`、`Analysis/GetINVESTMENTDETAILDetail`、`Analysis/SynchroINVESTMENTDETAIL`、`Analysis/DeleteINVESTMENTDETAIL`
  当前偏差：11 组实体被 batch router 批量模板化，典型问题是 `pk_val`、`data:dict`、小写包装和单表 CRUD。
  对应 C# 逻辑：AnalysisController 下每个实体都有独立 helper。
  整改动作：不要在现有模板上继续堆 patch，直接把 Analysis 从 batch 通用模板拆出来。
  实施批次：`B1`
  验收重点：11 组实体全部回到强类型模型和原返回包结构。

- `AN-02 Analysis 树 / 报表 / 固化回迁包`
  接口：`Analysis/GetASSETSPROFITSTreeList`、`Analysis/GetASSETSPROFITSBusinessTreeList`、`Analysis/GetASSETSPROFITSDateDetailList`、`Analysis/GetAssetsLossProfitList`、`Analysis/SyncPROFITCONTRIBUTEList`、`Analysis/ReCalcCACost`、`Analysis/GetShopSABFIList`、`Analysis/SolidProfitAnalysis`、`Analysis/GetPeriodMonthlyList`、`Analysis/GetRevenueEstimateList`、`Analysis/SolidShopSABFI`、`Analysis/SolidInvestmentAnalysis`、`Analysis/GetInvestmentReport`、`Analysis/GetNestingIAReport`
  当前偏差：树形、损益、固化、重算、SABFI、招商分析被简化成普通列表、单条保存或空返回。
  对应 C# 逻辑：ASSETSPROFITSHelper、PROFITCONTRIBUTEHelper、PERIODWARNINGHelper、VEHICLEAMOUNTHelper、INVESTMENTANALYSISHelper。
  整改动作：按“资产收益链 / 利润贡献链 / SABFI 固化链 / 招商分析链”四条线拆开回迁。
  实施批次：`B3`
  验收重点：树结构、固化结果、重算结果、招商报表嵌套结构。

- `AN-03 缺失路由补齐包`
  接口：`Analysis/GetSPCONTRIBUTIONList`、`Analysis/GetSPCONTRIBUTIONDetail`、`Analysis/SynchroSPCONTRIBUTION`、`Analysis/DeleteSPCONTRIBUTION`
  当前偏差：原 C# 有，Python 缺失。
  对应 C# 逻辑：AnalysisController 提供完整 SPCONTRIBUTION CRUD。
  整改动作：补完整 4 条并沿用原契约，不要再接 batch 通用模板。
  实施批次：`B4`
  验收重点：列表、明细、同步、删除 4 条接口闭环。

**BusinessMan**
- `BS-01 表映射修正包`
  接口：`Merchants/GetBusinessManList`、`Merchants/GetBusinessManDetail`、`Merchants/SynchroBusinessMan`、`Merchants/DeleteBusinessMan`、`Merchants/GetBusinessManDetailList`、`Merchants/GetBusinessManDetailDetail`、`Merchants/SynchroBusinessManDetail`、`Merchants/DeleteBusinessManDetail`、`Merchants/GetCommodityList`、`Merchants/GetCommodityDetail`、`Merchants/SynchroCommodity`、`Merchants/DeleteCommodity`
  当前偏差：已复核 C# Helper，Python 用 `T_BUSINESSMAN`、`T_BUSINESSMANDETAIL`、`T_COMMODITY` 代替了原 `OWNERUNIT`、`OWNERUNITDETAIL`、`COMMODITY_BUSINESS` 业务关系。
  对应 C# 逻辑：BusinessManHelper、BusinessManDetailHelper、COMMODITY_BUSINESSHelper。
  整改动作：先修表映射，再迁逻辑；这组接口不修表映射就没法谈一致性。
  实施批次：`B3`
  验收重点：创建、删除、详情、商品关系都要打到原业务关系表。

- `BS-02 CUSTOMTYPE / COMMODITY_TEMP 契约回迁包`
  接口：`Merchants/GetCUSTOMTYPEList`、`Merchants/GetCUSTOMTYPEDetail`、`Merchants/SynchroCUSTOMTYPE`、`Merchants/DeleteCUSTOMTYPE`、`BusinessMan/GetCOMMODITY_TEMPList`、`BusinessMan/GetCOMMODITY_TEMPDetail`、`BusinessMan/SynchroCOMMODITY_TEMP`、`BusinessMan/DeleteCOMMODITY_TEMP`
  当前偏差：仍被 batch router 套成 `pk_val` / `data:dict` / 统一删除。
  对应 C# 逻辑：CUSTOMTYPEHelper、COMMODITY_TEMPHelper。
  整改动作：恢复原强类型模型和 JsonMsg 包装。
  实施批次：`B1`
  验收重点：详情和同步契约不能再是通用模板。

- `BS-03 关系/授权/用户树回迁包`
  接口：`BusinessMan/AuthorizeQualification`、`Merchants/GetNestingCustomTypeLsit`、`Merchants/GetCustomTypeDDL`、`BusinessMan/CreateBusinessMan`、`BusinessMan/GetUserList`
  当前偏差：授权只做资质表 upsert；嵌套类型被降成平铺列表；创建商户只插一张表；用户接口变成商户列表甚至空列表。
  对应 C# 逻辑：AuthorizeQualification、CreateBusinessMan、GetUserList 都是业务流程接口，不是单表接口。
  整改动作：按“授权链 / 自定义类型树 / 创建商户链 / 用户树”四条线回迁。
  实施批次：`B2`
  验收重点：资质授权历史、门店/用户绑定、GET/POST 双入口、用户树结构。

**Supplier**
- `SU-01 Supplier / Qualification 去模板化包`
  接口：`Supplier/GetSupplierList`、`Supplier/GetSupplierTreeList`、`Supplier/GetSupplierDetail`、`Supplier/SynchroSupplier`、`Supplier/DeleteSupplier`、`Supplier/GetQualificationList`、`Supplier/GetQualificationDetail`、`Supplier/SynchroQualification`、`Supplier/DeleteQualification`、`Supplier/GetQUALIFICATION_HISList`、`Supplier/GetQUALIFICATION_HISDetail`、`Supplier/SynchroQUALIFICATION_HIS`
  当前偏差：列表、树、资质、历史全部被 generic CRUD 代替，`OtherData`、树结构和资质统计丢失。
  对应 C# 逻辑：SUPPLIERHelper、QUALIFICATIONHelper、历史 helper。
  整改动作：按“供应商主数据 / 资质 / 历史资质”三段回迁。
  实施批次：`B3`
  验收重点：供应商树、资质数量、历史列表、返回包结构。

- `SU-02 关联流程补齐包`
  接口：`Supplier/RelateBusinessCommodity`
  当前偏差：接口存在但直接 `return True, ""`。
  对应 C# 逻辑：QUALIFICATIONHelper.RelateBusinessCommodity 会写关联和历史。
  整改动作：恢复关联写入和历史链路。
  实施批次：`B2`
  验收重点：关联关系真实落库，且有失败分支。

- `SU-03 Python 多出路由清理包`
  接口：`Supplier/DeleteQUALIFICATION_HIS`
  当前偏差：原 C# 没有该删除入口，Python 多暴露了一条可执行删除接口。
  对应 C# 逻辑：SupplierController 不提供此路由。
  整改动作：先下线或隔离，不允许继续对外暴露。
  实施批次：`B1`
  验收重点：运行时路由集合重新与 C# 基线一致。

**Verification**
- `VE-01 ENDACCOUNT 基础实体回迁包`
  接口：`Verification/GetENDACCOUNTModel`、`Verification/SynchroENDACCOUNT`、`Verification/DeleteENDACCOUNT`、`Verification/GetEndaccountList`、`Verification/GetEndaccountDetail`、`Verification/GetEndaccountHisList`
  当前偏差：Python 把 `ENDACCOUNT` 迁成了 `ENDACCOUNT_DAILY` 通用 CRUD，连主键和表都漂了。
  对应 C# 逻辑：EndaccountHelper 以 `ENDACCOUNT` 为主模型，并区分当前和历史查询。
  整改动作：先恢复实体模型和表映射，再恢复当前/历史分支。
  实施批次：`B2`
  验收重点：主键、主表、当前/历史查询行为一致。

- `VE-02 日结状态机回迁包`
  接口：`Verification/VerifyEndaccount`、`Verification/ApproveEndaccount`、`Verification/SubmitEndaccountState`、`Verification/ApplyEndaccountInvalid`、`Verification/CancelEndaccount`
  当前偏差：被简化成单字段状态更新或复用同一路径。
  对应 C# 逻辑：EndaccountHelper 中为完整审核、审批、作废、取消状态机。
  整改动作：作为 P0 优先级最高的一批，直接按状态机回迁，不允许继续复用 CRUD。
  实施批次：`B2`
  验收重点：批量审核、错误返回、作废申请、取消作废、审计字段。

- `VE-03 校验查询链回迁包`
  接口：`Verification/GetSuppEndaccountList`、`Verification/GetDataVerificationList`、`Verification/GetShopEndaccountSum`、`Verification/GetEndAccountData`、`Verification/GetCommoditySaleList`、`Verification/GetMobilePayDataList`、`Verification/GetEndaccountSupplement`
  当前偏差：大量空实现，或错误复用日结主表。
  对应 C# 逻辑：DataVerificationHelper 提供按 `Data_Type` 分支的明细、汇总和补录查询。
  整改动作：按“补录 / 汇总 / 数据明细 / 移动支付 / 冲正”五条线恢复。
  实施批次：`B2`
  验收重点：数据类型分支、汇总字段和列表结果。

- `VE-04 写入/重建/纠错流程回迁包`
  接口：`Verification/SaveCorrectData`、`Verification/SaveSaleSupplement`、`Verification/ExceptionHandling`、`Verification/RebuildDailyAccount`、`Verification/CorrectDailyEndaccount`
  当前偏差：都是占位实现。
  对应 C# 逻辑：DataVerificationHelper、EndaccountHelper 承担真实写库、纠偏、重建流程。
  整改动作：全部按 P0 处理，未迁回前统一标记为未完成。
  实施批次：`B2`
  验收重点：真实写库、副作用、错误信息和刷新结果。

**Sales**
- `SA-01 COMMODITYSALE 契约/删除语义整改包`
  接口：`Sales/GetCOMMODITYSALEList`、`Sales/GetCOMMODITYSALEDetail`、`Sales/SynchroCOMMODITYSALE`、`Sales/DeleteCOMMODITYSALE`
  当前偏差：前三条被 generic CRUD 替代；`DeleteCOMMODITYSALE` 更严重，原 C# 实际不执行删除，Python 却执行了真实软删。
  对应 C# 逻辑：COMMODITYSALEHelper、原删除逻辑。
  整改动作：先确认删除语义必须回到 C# 口径，再恢复列表/明细/同步契约。
  实施批次：`B2`
  验收重点：删除行为必须和 C# 一致，不能继续产生实际删数。

- `SA-02 销售报表/纠错/刷新回迁包`
  接口：`Sales/GetEndaccountSaleInfo`、`Sales/RecordSaleData`、`Sales/GetEndaccountError`、`Sales/UpdateEndaccountError`、`Sales/GetCommoditySaleSummary`、`Sales/GetCommodityTypeSummary`、`Sales/GetCommodityTypeHistory`、`Sales/SaleRank`、`Sales/UpdateCommoditySale`
  当前偏差：被 `T_COMMODITYSALE` 原表分页、简单排名或单条保存替代。
  对应 C# 逻辑：EndaccountHelper、CommoditySaleHelper 下是汇总、排行、纠错、批量刷新链路。
  整改动作：按“账期快照 / 错误修正 / 汇总 / 排行 / 刷新”五条线回迁。
  实施批次：`B3`
  验收重点：排行筛选条件、历史汇总、批量刷新、副作用。

**Picture**
- `PI-01 同名接口错义整改包`
  接口：`Picture/GetPictureList`、`Picture/UploadPicture`、`Picture/DeletePicture`
  当前偏差：名字相同，但语义已经换成 `T_PICTURE` 管理接口；没有文件流、目录翻译、业务表删除或 HWS 图片语义。
  对应 C# 逻辑：PictureController、PictureHelper 基于 `TableId/TableName/TableType/ImageType/ImageIndex` 和真实文件系统工作。
  整改动作：不能在现有 `picture_service.py` 上继续补丁，必须按原 Picture 模块重建。
  实施批次：`B2`
  验收重点：multipart/base64、目录映射、物理文件、业务表记录、副作用。

- `PI-02 原 Picture 接口补齐包`
  接口：`Picture/SaveImgFile`、`Picture/GetEndaccountEvidence`、`Picture/UploadEndaccountEvidence`、`Picture/GetAuditEvidence`、`Picture/UploadAuditEvidence`、`Picture/DeleteMultiPicture`
  当前偏差：原 C# 路由存在，Python 全缺失。
  对应 C# 逻辑：PictureController 提供图片保存、HWS 凭证查询、上传、批量删除。
  整改动作：按“文件保存 / 凭证读取 / 上传 / 批删”四条链恢复。
  实施批次：`B4`
  验收重点：真实文件写入、读取、删除及 HWS 图片逻辑。

- `PI-03 Python 多出路由清理包`
  接口：`Picture/BatchDeletePicture`、`Picture/GetPictureDetail`、`Picture/GetPictureTypeList`、`Picture/GetPictureByShop`、`Picture/GetPictureCount`、`Picture/SynchroPicture`
  当前偏差：这 6 条是 Python 自己新起的一套 `T_PICTURE` 接口，不能冲抵原 Picture 模块完成度。
  对应 C# 逻辑：PictureController 无这些路由。
  整改动作：从迁移验收口径剔除，后续是否保留作为增量接口另议。
  实施批次：`B1`
  验收重点：运行时迁移清单与原 C# 路由集合重新对齐。

**Video**
- `VI-01 Video 批次 1：EXTRANET`
  接口：`Video/GetEXTRANETList`、`Video/GetEXTRANETDetail`、`Video/SynchroEXTRANET`、`Video/DeleteEXTRANET`
  当前偏差：原 C# 有，Python 全缺失。
  对应 C# 逻辑：EXTRANETHelper 标准列表/明细/同步/删除模板。
  整改动作：先补最标准的 4 条 CRUD，形成 Video 模块基础骨架。
  实施批次：`B4`
  验收重点：SearchModel、分页、排序、同步、删除闭环。

- `VI-02 Video 批次 2：EXTRANETDETAIL`
  接口：`Video/GetEXTRANETDETAILList`、`Video/GetEXTRANETDETAILDetail`、`Video/SynchroEXTRANETDETAIL`、`Video/DeleteEXTRANETDETAIL`
  当前偏差：原 C# 有，Python 全缺失。
  对应 C# 逻辑：EXTRANETDETAILHelper 标准 CRUD 模板。
  整改动作：沿用批次 1 的模板实现，但保留原契约。
  实施批次：`B4`
  验收重点：4 条接口闭环。

- `VI-03 Video 批次 3：SHOPVIDEO`
  接口：`Video/GetSHOPVIDEOList`、`Video/GetSHOPVIDEODetail`、`Video/SynchroSHOPVIDEO`、`Video/DeleteSHOPVIDEO`
  当前偏差：原 C# 有，Python 全缺失。
  对应 C# 逻辑：ShopVideoHelper 标准 CRUD 模板。
  整改动作：继续用 Video 模块专用模板补齐。
  实施批次：`B4`
  验收重点：4 条接口闭环。

- `VI-04 Video 批次 4：日志接口`
  接口：`Video/GetVIDEOLOGList`、`Video/SynchroVIDEOLOG`
  当前偏差：原 C# 有，Python 全缺失；其中 `GetVIDEOLOGList` 还带多种 `Search_Type` 分支。
  对应 C# 逻辑：VIDEOLOGHelper，涉及多表筛选。
  整改动作：`SynchroVIDEOLOG` 可先落地，`GetVIDEOLOGList` 单独按查询分支迁回。
  实施批次：`B4`
  验收重点：`Search_Type` 分支、联表筛选、日志字段。

- `VI-05 Video 批次 5：视频聚合接口`
  接口：`Video/GetShopVideoInfo`、`Video/GetYSShopVideoInfo`
  当前偏差：原 C# 有，Python 全缺失；且两条接口都是复杂聚合，不是 CRUD。
  对应 C# 逻辑：ShopVideoHelper 会读取 `V_SHOPVIDEO`、异常表、日结表、稽核表、商品明细并拼 `AbnormalityDetails`。
  整改动作：最后单独做，两条接口都要逐分支对齐，不允许套模板。
  实施批次：`B4`
  验收重点：异常类型分支、视频 IP 选择、文案拼装、商品明细、GET/POST 双入口。

## 4. 推荐实施顺序

按返工成本和线上风险，建议按下面顺序推进：

1. `B1` 契约层止血  
   Analysis、Audit、Supplier、BusinessMan、BigData、BaseInfo、Merchants、Revenue 的方法/参数/包装/Header 统一修正。

2. `B2` P0 流程接口回迁  
   Contract、Finance、MobilePay、Verification、Sales、Picture、Audit 的流程/状态机/文件接口先恢复真实行为。

3. `B3` helper 级业务回迁  
   Revenue、Analysis、BusinessMan、Supplier、BigData、BaseInfo/PropertyAssets、Contract/BusinessProject。

4. `B4` 缺失路由补齐  
   Video 全量、Picture 缺失 6 条、Analysis 4 条、BigData 3 条、Finance/Invoice/Office 12 条、Contract 缺失 2 条、Merchants 缺失 1 条。

5. `B5` 动态验收  
   每条整改后的接口至少做 3 组参数新旧比对，重点覆盖 Header、空参、边界日期、删除和状态机分支。

## 5. 本文档的使用方式

后续真正执行时，建议直接以本文件为整改总台账：

- 每完成一个整改包，就把该包内接口状态改成“已整改待联调 / 已联调通过”
- 不再按“模块完成率”推进，而按“整改包完成率”推进
- 如果需要继续沉淀到单接口级，可以从本台账继续往下拆成接口卡片
