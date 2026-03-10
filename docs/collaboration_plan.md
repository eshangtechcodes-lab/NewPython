# API 接口迁移 — 实施计划

> EShangApi C# → Python FastAPI 接口迁移，以 Controller 文件夹为准，AutoBuild 不迁移。
> 
> **最后更新时间**：2026-03-09（Revenue / BigData / Audit / Analysis / MobilePay / BusinessMan / DataVerification / Picture 全部完成）

## 迁移范围（精确统计）

**只迁移手动 Controller**，数据来自 C# 原项目 `[Route()]` 注解实际扫描。

### 已完成（共 631 个接口）

| # | 实体 | Controller | 接口数 | 涉及主表 | 完成日期 |
|---|------|-----------|--------|----------|---------|
| 1 | OWNERUNIT（业主单位） | BaseInfoController | 4 | T_OWNERUNIT | 2026-03-04 |
| 2 | SERVERPART（服务区站点） | BaseInfoController | 2 | T_SERVERPART | 2026-03-04 |
| 3 | ServerpartShop（门店） | BaseInfoController | 5 | T_SERVERPARTSHOP | 2026-03-04 |
| 4 | Brand（品牌） | BaseInfoController | 6 | T_BRAND, T_AUTOSTATISTICS, T_COOPMERCHANTS, T_RTCOOPMERCHANTS | 2026-03-04 |
| 5 | RTSERVERPARTSHOP（门店经营时间） | BaseInfoController | 4 | T_RTSERVERPARTSHOP | 2026-03-04 |
| 6 | SERVERPARTSHOP_LOG（门店变更日志） | BaseInfoController | 1 | T_SERVERPARTSHOP_LOG | 2026-03-04 |
| 7 | CASHWORKER（收银人员） | BaseInfoController | 4 | T_CASHWORKER | 2026-03-04 |
| 8 | BusinessTrade（经营业态） | BaseInfoController | 6 | T_AUTOSTATISTICS | 2026-03-05 |
| 9 | AUTOSTATISTICS（自定义统计归口） | BaseInfoController | 4 | T_AUTOSTATISTICS | 2026-03-05 |
| 10 | COMMODITYTYPE（商品类别） | BaseInfoController | 6 | T_COMMODITYTYPE | 2026-03-05 |
| 11 | USERDEFINEDTYPE（商品自定义类别） | BaseInfoController | 5 | T_USERDEFINEDTYPE | 2026-03-05 |
| 12 | SERVERPARTCRT（服务区成本核算对照） | BaseInfoController | 5 | T_SERVERPARTCRT | 2026-03-05 |
| 13 | PROPERTYASSETS（服务区资产） | BaseInfoController | 7 | T_PROPERTYASSETS | 2026-03-05 |
| 14 | COMMODITY（在售商品） | BaseInfoController | 6 | T_COMMODITY | 2026-03-05 |
| 15 | PROPERTYASSETSLOG（资产操作日志） | BaseInfoController | 2 | T_PROPERTYASSETSLOG | 2026-03-06 |
| 16 | ServerPartShopNew（门店-业主端） | BaseInfoController | 4 | V_SERVERPARTSHOP_COMBINE, T_SERVERPARTSHOP, T_COOPMERCHANTS, T_RTSERVERPARTSHOP | 2026-03-06 |
| 17 | PROPERTYSHOP（物业资产对照） | BaseInfoController | 5 | T_PROPERTYSHOP, T_SERVERPARTSHOP | 2026-03-06 |
| 18 | AUTOTYPE（自定义类别） | BasicConfigController | 6 | T_AUTOTYPE | 2026-03-06 |
| 19 | OWNERSERVERPART（业主-服务区关联） | BasicConfigController | 4 | T_OWNERSERVERPART | 2026-03-06 |
| 20 | OWNERSERVERPARTSHOP（业主-门店关联） | BasicConfigController | 4 | T_OWNERSERVERPARTSHOP | 2026-03-06 |
| 21 | SERVERPARTTYPE（服务区类别） | BasicConfigController | 7 | T_SERVERPARTTYPE, T_SPSTATICTYPE, T_SERVERPART | 2026-03-06 |
| 22 | SPSTATICTYPE（服务区类别关联） | BasicConfigController | 4 | T_SPSTATICTYPE | 2026-03-06 |
| 23 | SERVERPARTSHOPCRT（服务区门店对照） | BasicConfigController | 4 | T_SERVERPARTSHOPCRT | 2026-03-06 |
| 24 | BUSINESSPROJECT（经营项目） | BusinessProjectController | 4 | T_BUSINESSPROJECT, T_SHOPROYALTY, T_RTBUSINESSPROJECT, T_RTREGISTERCOMPACT | 2026-03-06 |
| 25 | ShopRoyalty+SHOPROYALTYDETAIL（门店提成/拆分明细） | BusinessProjectController | 8 | T_SHOPROYALTY, T_SHOPROYALTYDETAIL | 2026-03-06 |
| 26 | REVENUECONFIRM（营收回款确认） | BusinessProjectController | 5 | T_REVENUECONFIRM, T_BUSINESSPROJECT, T_SHOPROYALTY | 2026-03-06 |
| 27 | PAYMENTCONFIRM（商家应收回款） | BusinessProjectController | 6 | T_PAYMENTCONFIRM, T_RTPAYMENTRECORD, T_SHOPROYALTY, T_REVENUECONFIRM | 2026-03-06 |
| 28 | RTPAYMENTRECORD（商家回款记录） | BusinessProjectController | 4 | T_RTPAYMENTRECORD, T_PAYMENTCONFIRM | 2026-03-06 |
| 29 | REMARKS（备注说明） | BusinessProjectController | 4 | T_REMARKS | 2026-03-06 |
| 30 | CoopMerchants（经营商户） | MerchantsController | 4 | T_COOPMERCHANTS, T_COOPMERCHANTS_LINKER | 2026-03-08 |
| 31 | CoopMerchantsType（商户类型） | MerchantsController | 3 | T_AUTOSTATISTICS (TYPE=5000) | 2026-03-08 |
| 32 | CoopMerchantsLinker（商户联系人） | MerchantsController | 4 | T_COOPMERCHANTS_LINKER | 2026-03-08 |
| 33 | RTCoopMerchants+TradeBrandMerchants（商户品牌关联） | MerchantsController | 4 | T_RTCOOPMERCHANTS, T_BRAND, T_AUTOSTATISTICS | 2026-03-08 |
| 34 | ATTACHMENT（财务附件） | FinanceController | 4 | T_ATTACHMENT | 2026-03-08 |
| — | Finance 散装接口（44 个报表/审批/固化） | FinanceController | 44 | T_BUSINESSPROJECTSPLIT, T_BANKACCOUNTVERIFY, T_REVENUEDAILY, T_SHOPEXPENSE, T_REVENUECONFIRM 等 | 2026-03-08 |
| 35 | BILL（票据信息） | InvoiceController | 4 | T_BILL | 2026-03-08 |
| 36 | BILLDETAIL（票据明细） | InvoiceController | 4 | T_BILLDETAIL | 2026-03-08 |
| — | Invoice 散装接口（4 个回写/转发） | InvoiceController | 4 | T_BILL | 2026-03-08 |
| 37 | BUDGETPROJECT_AH（预算项目） | BudgetProjectAHController | 4 | T_BUDGETPROJECT_AH | 2026-03-08 |
| 38 | BUDGETDETAIL_AH（预算明细） | BudgetProjectAHController | 4 | T_BUDGETDETAIL_AH | 2026-03-08 |
| — | Budget 散装接口（8 个报表/批量保存） | BudgetProjectAHController | 8 | T_BUDGETDETAIL_AH, FieldEnum | 2026-03-08 |

#### 已完成接口明细

| 路由路径 | 接口 | HTTP 方法 | 实体 |
|----------|------|-----------|------|
| BaseInfo/GetOWNERUNITList | 列表 | POST | OWNERUNIT |
| BaseInfo/GetOWNERUNITDetail | 明细 | GET | OWNERUNIT |
| BaseInfo/SynchroOWNERUNIT | 同步 | POST | OWNERUNIT |
| BaseInfo/DeleteOWNERUNIT | 删除（软） | GET+POST | OWNERUNIT |
| BaseInfo/GetSERVERPARTList | 列表 | POST | SERVERPART |
| BaseInfo/DeleteSERVERPART | 删除（真） | GET+POST | SERVERPART |
| BaseInfo/GetServerpartShopList | 列表 | POST | ServerpartShop |
| BaseInfo/GetServerpartShopDetail | 明细 | GET+POST | ServerpartShop |
| BaseInfo/SynchroServerpartShop | 同步 | POST | ServerpartShop |
| BaseInfo/DeleteServerpartShop | 删除（软） | GET+POST | ServerpartShop |
| BaseInfo/DelServerpartShop | 批量删除 | GET+POST | ServerpartShop |
| BaseInfo/GetBrandList | 列表 | POST | Brand |
| BaseInfo/GetCombineBrandList | 组合品牌 | GET | Brand |
| BaseInfo/GetTradeBrandTree | 品牌树 | GET+POST | Brand |
| BaseInfo/GetBrandDetail | 明细 | GET | Brand |
| BaseInfo/SynchroBrand | 同步 | POST | Brand |
| BaseInfo/DeleteBrand | 删除（软） | GET+POST | Brand |
| BaseInfo/GetRTSERVERPARTSHOPList | 列表 | POST | RTSERVERPARTSHOP |
| BaseInfo/GetRTSERVERPARTSHOPDetail | 明细 | GET | RTSERVERPARTSHOP |
| BaseInfo/SynchroRTSERVERPARTSHOP | 同步 | POST | RTSERVERPARTSHOP |
| BaseInfo/DeleteRTSERVERPARTSHOP | 删除（真） | GET+POST | RTSERVERPARTSHOP |
| BaseInfo/GetSERVERPARTSHOP_LOGList | 列表 | POST | SERVERPARTSHOP_LOG |
| BaseInfo/GetCASHWORKERList | 列表 | POST | CASHWORKER |
| BaseInfo/GetCASHWORKERDetail | 明细 | GET | CASHWORKER |
| BaseInfo/SynchroCASHWORKER | 同步 | POST | CASHWORKER |
| BaseInfo/DeleteCASHWORKER | 删除 | GET+POST | CASHWORKER |
| BaseInfo/GetBusinessTradeList | 列表 | POST | BusinessTrade |
| BaseInfo/GetBusinessTradeTree | 业态树 | GET+POST | BusinessTrade |
| BaseInfo/GetBusinessTradeEnum | 枚举树 | GET+POST | BusinessTrade |
| BaseInfo/GetBusinessTradeDetail | 明细 | GET+POST | BusinessTrade |
| BaseInfo/SynchroBusinessTrade | 同步 | POST | BusinessTrade |
| BaseInfo/DeleteBusinessTrade | 删除（软） | GET+POST | BusinessTrade |
| BaseInfo/GetAutoStatisticsTreeList | 树形列表 | GET+POST | AUTOSTATISTICS |
| BaseInfo/GetAUTOSTATISTICSDetail | 明细 | GET+POST | AUTOSTATISTICS |
| BaseInfo/SynchroAUTOSTATISTICS | 同步 | POST | AUTOSTATISTICS |
| BaseInfo/DeleteAUTOSTATISTICS | 删除（软） | GET+POST | AUTOSTATISTICS |
| BaseInfo/GetCOMMODITYTYPEList | 列表 | POST | COMMODITYTYPE |
| BaseInfo/GetCOMMODITYTYPEDetail | 明细 | GET | COMMODITYTYPE |
| BaseInfo/SynchroCOMMODITYTYPE | 同步 | POST | COMMODITYTYPE |
| BaseInfo/DeleteCOMMODITYTYPE | 删除（软） | GET+POST | COMMODITYTYPE |
| BaseInfo/GetNestingCOMMODITYTYPEList | 嵌套列表 | GET | COMMODITYTYPE |
| BaseInfo/GetNestingCOMMODITYTYPETree | 嵌套树 | GET | COMMODITYTYPE |
| BaseInfo/GetUSERDEFINEDTYPEList | 列表 | POST | USERDEFINEDTYPE |
| BaseInfo/GetUSERDEFINEDTYPEDetail | 明细 | GET | USERDEFINEDTYPE |
| BaseInfo/SynchroUSERDEFINEDTYPE | 同步 | POST | USERDEFINEDTYPE |
| BaseInfo/DeleteUSERDEFINEDTYPE | 删除（软） | GET+POST | USERDEFINEDTYPE |
| BaseInfo/CreatePriceType | 生成价格分类 | POST | USERDEFINEDTYPE |
| BaseInfo/GetSERVERPARTCRTList | 列表 | POST | SERVERPARTCRT |
| BaseInfo/GetSERVERPARTCRTTreeList | 树形列表 | POST | SERVERPARTCRT |
| BaseInfo/GetSERVERPARTCRTDetail | 明细 | GET | SERVERPARTCRT |
| BaseInfo/SynchroSERVERPARTCRT | 同步 | POST | SERVERPARTCRT |
| BaseInfo/DeleteSERVERPARTCRT | 删除（真） | POST | SERVERPARTCRT |
| BaseInfo/GetPROPERTYASSETSList | 列表 | POST | PROPERTYASSETS |
| BaseInfo/GetPROPERTYASSETSTreeList | 树形列表 | POST | PROPERTYASSETS |
| BaseInfo/GetAssetsRevenueAmount | 资产效益 | GET | PROPERTYASSETS |
| BaseInfo/GetPROPERTYASSETSDetail | 明细 | GET | PROPERTYASSETS |
| BaseInfo/SynchroPROPERTYASSETS | 同步 | POST | PROPERTYASSETS |
| BaseInfo/BatchPROPERTYASSETS | 批量同步 | POST | PROPERTYASSETS |
| BaseInfo/DeletePROPERTYASSETS | 删除（软） | POST | PROPERTYASSETS |
| BaseInfo/GetCOMMODITYList | 列表 | POST | COMMODITY |
| BaseInfo/GetCOMMODITYDetail | 明细 | GET | COMMODITY |
| BaseInfo/SynchroCOMMODITY | 同步 | POST | COMMODITY |
| BaseInfo/OnShelfCommodity | 上架 | POST | COMMODITY |
| BaseInfo/LowerShelfCommodity | 下架 | POST | COMMODITY |
| BaseInfo/DeleteCOMMODITY | 删除（软） | GET+POST | COMMODITY |
| BaseInfo/GetShopShortNames | 门店简称列表 | GET | 散装 |
| BaseInfo/GetServerpartShopInfo | 门店信息查询 | GET | 散装 |
| BaseInfo/GetServerpartDDL | 服务区下拉框 | GET | 散装 |
| BaseInfo/GetServerpartTree | 区域服务区树 | GET | 散装 |
| BaseInfo/GetSPRegionShopTree | 区域门店树 | GET | 散装 |
| BaseInfo/GetServerpartShopDDL | 门店下拉框 | GET | 散装 |
| BaseInfo/GetServerpartShopTree | 服务区门店树 | GET | 散装 |
| BaseInfo/GetNestingOwnerUnitList | 业主单位嵌套列表 | GET | 散装 |
| BaseInfo/BindingOwnerUnitDDL | 业主单位下拉框 | GET | 散装 |
| BaseInfo/BindingOwnerUnitTree | 业主单位树 | GET | 散装 |
| BaseInfo/BindingMerchantTree | 经营商户树 | GET | 散装 |
| BaseInfo/GetBusinessBrandList | 门店经营品牌列表 | GET | 散装 |
| BaseInfo/ModifyShopState | 变更门店经营状态 | POST | 散装 |
| BaseInfo/GetShopReceivables | 门店关联合同项目 | GET | 散装 |
| BaseInfo/GetServerpartUDTypeTree | 服务区自定义类别树 | GET | 散装 |
| BaseInfo/GetSERVERPARTDetail | 服务区详情 | GET | 散装 |
| BaseInfo/GetPROPERTYASSETSLOGList | 列表 | POST | PROPERTYASSETSLOG |
| BaseInfo/SynchroPROPERTYASSETSLOG | 同步 | POST | PROPERTYASSETSLOG |
| BaseInfo/GetServerPartShopNewList | 列表 | GET | ServerPartShopNew |
| BaseInfo/GetServerPartShopNewDetail | 明细 | GET | ServerPartShopNew |
| BaseInfo/ServerPartShopNewSaveState | 设置经营状态 | POST | ServerPartShopNew |
| BaseInfo/SynchroServerPartShopNew | 同步 | POST | ServerPartShopNew |
| BaseInfo/GetPROPERTYSHOPList | 列表 | POST | PROPERTYSHOP |
| BaseInfo/GetPROPERTYSHOPDetail | 明细 | GET | PROPERTYSHOP |
| BaseInfo/SynchroPROPERTYSHOP | 同步 | POST | PROPERTYSHOP |
| BaseInfo/BatchPROPERTYSHOP | 批量同步 | POST | PROPERTYSHOP |
| BaseInfo/DeletePROPERTYSHOP | 删除（软） | POST | PROPERTYSHOP |
| BusinessProject/GetBusinessProjectList | 列表 | POST | BUSINESSPROJECT |
| BusinessProject/GetBusinessProjectDetail | 明细 | GET+POST | BUSINESSPROJECT |
| BusinessProject/SynchroBusinessProject | 同步 | POST | BUSINESSPROJECT |
| BusinessProject/DeleteBusinessProject | 删除（软） | GET+POST | BUSINESSPROJECT |
| BusinessProject/GetShopRoyaltyList | 列表 | POST | SHOPROYALTY |
| BusinessProject/GetShopRoyaltyDetail | 明细 | GET | SHOPROYALTY |
| BusinessProject/SynchroShopRoyalty | 同步 | POST | SHOPROYALTY |
| BusinessProject/DeleteShopRoyalty | 删除（真） | GET+POST | SHOPROYALTY |
| BusinessProject/GetSHOPROYALTYDETAILList | 列表 | POST | SHOPROYALTYDETAIL |
| BusinessProject/GetSHOPROYALTYDETAILDetail | 明细 | GET | SHOPROYALTYDETAIL |
| BusinessProject/SynchroSHOPROYALTYDETAIL | 同步 | POST | SHOPROYALTYDETAIL |
| BusinessProject/DeleteSHOPROYALTYDETAIL | 删除（软） | GET+POST | SHOPROYALTYDETAIL |
| BusinessProject/GetRevenueConfirmList | 列表 | POST+GET | REVENUECONFIRM |
| BusinessProject/GetRevenueConfirmDetail | 明细 | GET | REVENUECONFIRM |
| BusinessProject/SynchroRevenueConfirm | 同步 | POST | REVENUECONFIRM |
| BusinessProject/DeleteRevenueConfirm | 删除（真） | GET+POST | REVENUECONFIRM |
| BusinessProject/GetPaymentConfirmList | 列表 | POST+GET | PAYMENTCONFIRM |
| BusinessProject/GetPaymentConfirmDetail | 明细 | GET | PAYMENTCONFIRM |
| BusinessProject/SeparatePaymentRecord | 拆分回款 | POST | PAYMENTCONFIRM |
| BusinessProject/SynchroPaymentConfirm | 同步 | POST | PAYMENTCONFIRM |
| BusinessProject/DeletePaymentConfirm | 删除（软） | GET+POST | PAYMENTCONFIRM |
| BusinessProject/GetRTPaymentRecordList | 列表 | POST | RTPAYMENTRECORD |
| BusinessProject/GetRTPaymentRecordDetail | 明细 | GET | RTPAYMENTRECORD |
| BusinessProject/SynchroRTPaymentRecord | 同步 | POST | RTPAYMENTRECORD |
| BusinessProject/DeleteRTPaymentRecord | 删除（软） | GET+POST | RTPAYMENTRECORD |
| BusinessProject/GetRemarksList | 列表 | POST | REMARKS |
| BusinessProject/GetRemarksDetail | 明细 | GET | REMARKS |
| BusinessProject/SynchroRemarks | 同步 | POST | REMARKS |
| BusinessProject/DeleteRemarks | 删除（软） | GET+POST | REMARKS |

#### ⏭️ 跳过（加密接口，使用 CommonModel AES 加密入参）

| 路由 | 说明 | 方法 | 跳过原因 |
|------|------|------|----------|
| BaseInfo/ModifyShopBusinessState | 批量修改门店经营状态 | POST | CommonModel AES 加密入参，内部调用 ServerPartShopNewSaveState（已实现） |

---

### 接口状态明细（2026-03-06 C# 全量扫描）
> 按迁移顺序排列，当前进度：仅剩 **Video(16) + BaseInfo剩余(35)** 待迁移

### BaseInfo 模块 — ❌ 待迁移（剩余 35 个）
> ✅94 ❌35 ⏭️16 💬0 / 共145

**BaseInfoController** (99 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| BaseInfo/GetOWNERUNITList | POST | ✅ |
| BaseInfo/GetOWNERUNITDetail | GET | ✅ |
| BaseInfo/SynchroOWNERUNIT | POST | ✅ |
| BaseInfo/DeleteOWNERUNIT | POST | ✅ |
| BaseInfo/GetSERVERPARTList | POST | ✅ |
| BaseInfo/DeleteSERVERPART | POST | ✅ |
| BaseInfo/GetServerpartShopList | POST | ✅ |
| BaseInfo/GetServerpartShopDetail | GET | ✅ |
| BaseInfo/SynchroServerpartShop | POST | ✅ |
| BaseInfo/DeleteServerpartShop | POST | ✅ |
| BaseInfo/DelServerpartShop | POST | ✅ |
| BaseInfo/GetRTSERVERPARTSHOPList | POST | ✅ |
| BaseInfo/GetRTSERVERPARTSHOPDetail | GET | ✅ |
| BaseInfo/SynchroRTSERVERPARTSHOP | POST | ✅ |
| BaseInfo/DeleteRTSERVERPARTSHOP | POST | ✅ |
| BaseInfo/GetSERVERPARTSHOP_LOGList | POST | ✅ |
| BaseInfo/GetBUSINESSTRADEList | POST | ⏭️别名 |
| BaseInfo/GetBUSINESSTRADEDetail | GET | ⏭️别名 |
| BaseInfo/SynchroBUSINESSTRADE | POST | ⏭️别名 |
| BaseInfo/DeleteBUSINESSTRADE | POST | ⏭️别名 |
| BaseInfo/GetBrandList | POST | ✅ |
| BaseInfo/GetCombineBrandList | GET | ✅ |
| BaseInfo/GetTradeBrandTree | POST | ✅ |
| BaseInfo/GetBrandDetail | GET | ✅ |
| BaseInfo/SynchroBrand | POST | ✅ |
| BaseInfo/DeleteBrand | POST | ✅ |
| BaseInfo/GetBusinessTradeList | POST | ✅ |
| BaseInfo/GetBusinessTradeTree | POST | ✅ |
| BaseInfo/GetBusinessTradeEnum | POST | ✅ |
| BaseInfo/GetBusinessTradeDetail | POST | ✅ |
| BaseInfo/SynchroBusinessTrade | POST | ✅ |
| BaseInfo/DeleteBusinessTrade | POST | ✅ |
| BaseInfo/GetAutoStatisticsTreeList | POST | ✅ |
| BaseInfo/GetAUTOSTATISTICSDetail | POST | ✅ |
| BaseInfo/SynchroAUTOSTATISTICS | POST | ✅ |
| BaseInfo/DeleteAUTOSTATISTICS | POST | ✅ |
| BaseInfo/GetCOMMODITYTYPEList | POST | ✅ |
| BaseInfo/GetCOMMODITYTYPEDetail | GET | ✅ |
| BaseInfo/SynchroCOMMODITYTYPE | POST | ✅ |
| BaseInfo/DeleteCOMMODITYTYPE | POST | ✅ |
| BaseInfo/GetNestingCOMMODITYTYPEList | GET | ✅ |
| BaseInfo/GetNestingCOMMODITYTYPETree | GET | ✅ |
| BaseInfo/GetUSERDEFINEDTYPEList | POST | ✅ |
| BaseInfo/GetUSERDEFINEDTYPEDetail | GET | ✅ |
| BaseInfo/SynchroUSERDEFINEDTYPE | POST | ✅ |
| BaseInfo/DeleteUSERDEFINEDTYPE | POST | ✅ |
| BaseInfo/CreatePriceType | POST | ✅ |
| BaseInfo/GetCASHWORKERList | POST | ✅ |
| BaseInfo/GetCASHWORKERDetail | GET | ✅ |
| BaseInfo/SynchroCASHWORKER | POST | ✅ |
| BaseInfo/DeleteCASHWORKER | POST | ✅ |
| BaseInfo/GetSERVERPARTCRTList | POST | ✅ |
| BaseInfo/GetSERVERPARTCRTTreeList | POST | ✅ |
| BaseInfo/GetSERVERPARTCRTDetail | GET | ✅ |
| BaseInfo/SynchroSERVERPARTCRT | POST | ✅ |
| BaseInfo/DeleteSERVERPARTCRT | POST | ✅ |
| BaseInfo/GetPROPERTYASSETSList | POST | ✅ |
| BaseInfo/GetPROPERTYASSETSTreeList | POST | ✅ |
| BaseInfo/GetAssetsRevenueAmount | GET | ✅ |
| BaseInfo/GetPROPERTYASSETSDetail | GET | ✅ |
| BaseInfo/SynchroPROPERTYASSETS | POST | ✅ |
| BaseInfo/BatchPROPERTYASSETS | POST | ✅ |
| BaseInfo/DeletePROPERTYASSETS | POST | ✅ |
| BaseInfo/GetPROPERTYSHOPList | POST | ✅ |
| BaseInfo/GetPROPERTYSHOPDetail | GET | ✅ |
| BaseInfo/SynchroPROPERTYSHOP | POST | ✅ |
| BaseInfo/BatchPROPERTYSHOP | POST | ✅ |
| BaseInfo/DeletePROPERTYSHOP | POST | ✅ |
| BaseInfo/GetPROPERTYASSETSLOGList | POST | ✅ |
| BaseInfo/SynchroPROPERTYASSETSLOG | POST | ✅ |
| BaseInfo/GetShopShortNames | POST | ✅ |
| BaseInfo/GetCOMMODITYList | POST | ✅ |
| BaseInfo/GetCOMMODITYDetail | GET | ✅ |
| BaseInfo/OnShelfCommodity | POST | ✅ |
| BaseInfo/LowerShelfCommodity | POST | ✅ |
| BaseInfo/SynchroCOMMODITY | POST | ✅ |
| BaseInfo/DeleteCOMMODITY | POST | ✅ |
| BaseInfo/GetServerpartShopInfo | POST | ✅ |
| BaseInfo/GetServerpartDDL | GET | ✅ |
| BaseInfo/GetServerpartTree | GET | ✅ |
| BaseInfo/GetSPRegionShopTree | GET | ✅ |
| BaseInfo/GetServerpartShopDDL | GET | ✅ |
| BaseInfo/GetServerpartShopTree | GET | ✅ |
| BaseInfo/GetNestingOwnerUnitList | GET | ✅ |
| BaseInfo/BindingOwnerUnitDDL | GET | ✅ |
| BaseInfo/BindingOwnerUnitTree | GET | ✅ |
| BaseInfo/BindingMerchantTree | GET | ✅ |
| BaseInfo/GetBusinessBrandList | GET | ✅ |
| BaseInfo/ModifyShopState | POST | ✅ |
| BaseInfo/GetShopReceivables | GET | ✅ |
| BaseInfo/GetServerpartUDTypeTree | GET | ✅ |
| BaseInfo/GetServerPartShopNewList | GET | ✅ |
| BaseInfo/GetServerPartShopNewDetail | GET | ✅ |
| BaseInfo/ServerPartShopNewSaveState | POST | ✅ |
| BaseInfo/SynchroServerPartShopNew | POST | ✅ |
| BaseInfo/GetSERVERPARTDetail | GET | ✅ |
| BaseInfo/SynchroSERVERPART | POST | ✅ |
| BaseInfo/SolidServerpartWeather | POST | ✅ |
| BaseInfo/ModifyShopBusinessState | POST | ⏭️加密 |

**BasicConfigController** (29 个接口) ✅ 已完成 2026-03-06

| 路由 | 方法 | 状态 |
|------|------|------|
| BasicConfig/GetAUTOTYPEList | POST | ✅ |
| BasicConfig/GetAUTOTYPEDetail | GET | ✅ |
| BasicConfig/SynchroAUTOTYPE | POST | ✅ |
| BasicConfig/DeleteAUTOTYPE | POST | ✅ |
| BasicConfig/GetNestingAUTOTYPEList | GET | ✅ |
| BasicConfig/GetNestingAUTOTYPETree | GET | ✅ |
| BasicConfig/GetOWNERSERVERPARTList | POST | ✅ |
| BasicConfig/GetOWNERSERVERPARTDetail | GET | ✅ |
| BasicConfig/SynchroOWNERSERVERPART | POST | ✅ |
| BasicConfig/DeleteOWNERSERVERPART | POST | ✅ |
| BasicConfig/GetOWNERSERVERPARTSHOPList | POST | ✅ |
| BasicConfig/GetOWNERSERVERPARTSHOPDetail | GET | ✅ |
| BasicConfig/SynchroOWNERSERVERPARTSHOP | POST | ✅ |
| BasicConfig/DeleteOWNERSERVERPARTSHOP | POST | ✅ |
| BasicConfig/GetSERVERPARTTYPEList | POST | ✅ |
| BasicConfig/GetSERVERPARTTYPEDetail | GET | ✅ |
| BasicConfig/SynchroSERVERPARTTYPE | POST | ✅ |
| BasicConfig/DeleteSERVERPARTTYPE | POST | ✅ |
| BasicConfig/GetNestingSERVERPARTTYPEList | GET | ✅ |
| BasicConfig/GetNestingSERVERPARTTYPETree | GET | ✅ |
| BasicConfig/GetSPSTATICTYPEList | POST | ✅ |
| BasicConfig/GetSPSTATICTYPEDetail | GET | ✅ |
| BasicConfig/SynchroSPSTATICTYPE | POST | ✅ |
| BasicConfig/DeleteSPSTATICTYPE | POST | ✅ |
| BasicConfig/ModifyRTServerpartType | GET | ✅ |
| BasicConfig/GetSERVERPARTSHOPCRTList | POST | ✅ |
| BasicConfig/GetSERVERPARTSHOPCRTDetail | GET | ✅ |
| BasicConfig/SynchroSERVERPARTSHOPCRT | POST | ✅ |
| BasicConfig/DeleteSERVERPARTSHOPCRT | POST | ✅ |

**CommodityController** (17 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Commodity/GetCOMMODITYList | POST | ✅ |
| Commodity/GetCOMMODITYDetail | GET | ✅ |
| Commodity/SynchroCOMMODITY | POST | ✅ |
| Commodity/DeleteCOMMODITY | POST | ✅ |
| Commodity/GetCOMMODITY_RUNNINGList | POST | ⏭️加密 |
| Commodity/GetCOMMODITY_RUNNINGDetail | POST | ⏭️加密 |
| Commodity/SynchroCOMMODITY_RUNNING | POST | ⏭️加密 |
| Commodity/DeleteCOMMODITY_RUNNING | POST | ⏭️加密 |
| Commodity/GetCOMMODITY_HISTORYList | POST | ⏭️加密 |
| Commodity/SynchroCOMMODITY_HISTORY | POST | ⏭️加密 |
| Commodity/GetCommodityList | GET | ✅ |
| Commodity/RelateUDType | POST | ⏭️加密 |
| Commodity/DeleteRTUDType | POST | ⏭️加密 |
| Commodity/GetServerpartShopTrade | POST | ⏭️加密 |
| Commodity/GetApprovalCommodityList | POST | ⏭️加密 |
| Commodity/SyncCommodityInfo_AHJG | GET | ✅ |
| Commodity/ApproveCommodityInfo_AHJG | POST | ⏭️加密 |

### Contract 模块 — ✅ 已完成
> ✅130 ❌0 ⏭️2 💬0 / 共132

**ContractController** (27 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Contract/GetRegisterCompactList | POST | ✅ |
| Contract/GetRegisterCompactDetail | GET | ✅ |
| Contract/SynchroRegisterCompact | POST | ✅ |
| Contract/DeleteRegisterCompact | POST | ✅ |
| Contract/GetRegisterCompactSubList | POST | ✅ |
| Contract/GetRegisterCompactSubDetail | GET | ✅ |
| Contract/SynchroRegisterCompactSub | POST | ✅ |
| Contract/DeleteRegisterCompactSub | POST | ✅ |
| Contract/GetRTRegisterCompactList | POST | ✅ |
| Contract/GetRTRegisterCompactDetail | GET | ✅ |
| Contract/SynchroRTRegisterCompact | POST | ✅ |
| Contract/DeleteRTRegisterCompact | POST | ✅ |
| Contract/GetAttachmentList | POST | ✅ |
| Contract/GetAttachmentDetail | GET | ✅ |
| Contract/SynchroAttachmentList | POST | ✅ |
| Contract/SynchroAttachment | POST | ✅ |
| Contract/DeleteAttachment | POST | ✅ |
| Contract/SaveAttachment | POST | ✅ |
| Contract/DelFile | POST | ✅ |
| Contract/GetProjectSummaryInfo | GET | ✅ |
| Contract/GetContractExpiredInfo | GET | ✅ |
| Contract/GetProjectYearlyArrearageList | GET | ✅ |
| Contract/GetProjectMonthlyArrearageList | GET | ✅ |
| Contract/GetContractYearList | GET | ⏭️加密 |
| Contract/GetShopBusinessTypeRatio | GET | ⏭️加密 |
| Contract/AddContractSupplement | POST | ✅ |
| Contract/SynchroContractSyn | POST | ✅ |

**BusinessProjectController** (87 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| BusinessProject/GetBusinessProjectList | POST | ✅ |
| BusinessProject/GetBusinessProjectDetail | POST | ✅ |
| BusinessProject/SynchroBusinessProject | POST | ✅ |
| BusinessProject/DeleteBusinessProject | POST | ✅ |
| BusinessProject/GetShopRoyaltyList | POST | ✅ |
| BusinessProject/GetShopRoyaltyDetail | GET | ✅ |
| BusinessProject/SynchroShopRoyalty | POST | ✅ |
| BusinessProject/DeleteShopRoyalty | POST | ✅ |
| BusinessProject/GetSHOPROYALTYDETAILList | POST | ✅ |
| BusinessProject/GetSHOPROYALTYDETAILDetail | GET | ✅ |
| BusinessProject/SynchroSHOPROYALTYDETAIL | POST | ✅ |
| BusinessProject/DeleteSHOPROYALTYDETAIL | POST | ✅ |
| BusinessProject/GetRevenueConfirmList | POST | ✅ |
| BusinessProject/GetRevenueConfirmList | GET | ✅ |
| BusinessProject/GetRevenueConfirmDetail | GET | ✅ |
| BusinessProject/SynchroRevenueConfirm | POST | ✅ |
| BusinessProject/DeleteRevenueConfirm | POST | ✅ |
| BusinessProject/GetPaymentConfirmList | POST | ✅ |
| BusinessProject/GetPaymentConfirmList | GET | ✅ |
| BusinessProject/GetPaymentConfirmDetail | GET | ✅ |
| BusinessProject/SeparatePaymentRecord | POST | ✅ |
| BusinessProject/SynchroPaymentConfirm | POST | ✅ |
| BusinessProject/DeletePaymentConfirm | POST | ✅ |
| BusinessProject/GetRTPaymentRecordList | POST | ✅ |
| BusinessProject/GetRTPaymentRecordDetail | GET | ✅ |
| BusinessProject/SynchroRTPaymentRecord | POST | ✅ |
| BusinessProject/DeleteRTPaymentRecord | POST | ✅ |
| BusinessProject/GetRemarksList | POST | ✅ |
| BusinessProject/GetRemarksDetail | GET | ✅ |
| BusinessProject/SynchroRemarks | POST | ✅ |
| BusinessProject/DeleteRemarks | POST | ✅ |
| BusinessProject/GetBusinessPaymentList | POST | ✅ |
| BusinessProject/GetBusinessPaymentDetail | GET | ✅ |
| BusinessProject/SynchroBusinessPayment | POST | ✅ |
| BusinessProject/DeleteBusinessPayment | POST | ✅ |
| BusinessProject/GetBUSINESSPROJECTSPLITList | POST | ✅ |
| BusinessProject/GetBUSINESSPROJECTSPLITDetail | GET | ✅ |
| BusinessProject/SynchroBUSINESSPROJECTSPLIT | POST | ✅ |
| BusinessProject/DeleteBUSINESSPROJECTSPLIT | POST | ✅ |
| BusinessProject/GetBIZPSPLITMONTHList | POST | ✅ |
| BusinessProject/GetBIZPSPLITMONTHDetail | GET | ✅ |
| BusinessProject/SynchroBIZPSPLITMONTH | POST | ✅ |
| BusinessProject/DeleteBIZPSPLITMONTH | POST | ✅ |
| BusinessProject/GetPROJECTWARNINGList | POST | ✅ |
| BusinessProject/GetPROJECTWARNINGDetail | GET | ✅ |
| BusinessProject/SynchroPROJECTWARNING | POST | ✅ |
| BusinessProject/DeletePROJECTWARNING | POST | ✅ |
| BusinessProject/GetPERIODWARNINGList | POST | ✅ |
| BusinessProject/GetPERIODWARNINGDetail | GET | ✅ |
| BusinessProject/SynchroPERIODWARNING | POST | ✅ |
| BusinessProject/DeletePERIODWARNING | POST | ✅ |
| BusinessProject/GetAPPROVEDList | POST | ✅ |
| BusinessProject/GetSHOPEXPENSEList | POST | ✅ |
| BusinessProject/GetSHOPEXPENSEDetail | GET | ✅ |
| BusinessProject/SynchroSHOPEXPENSE | POST | ✅ |
| BusinessProject/DeleteSHOPEXPENSE | POST | ✅ |
| BusinessProject/ApproveSHOPEXPENSE | POST | ✅ |
| BusinessProject/GetPROJECTSPLITMONTHList | POST | ✅ |
| BusinessProject/GetPROJECTSPLITMONTHDetail | GET | ✅ |
| BusinessProject/SynchroPROJECTSPLITMONTH | POST | ✅ |
| BusinessProject/DeletePROJECTSPLITMONTH | POST | ✅ |
| BusinessProject/GetMerchantsReceivablesList | GET | ✅ |
| BusinessProject/GetMerchantsReceivables | GET | ✅ |
| BusinessProject/GetBrandReceivables | GET | ✅ |
| BusinessProject/GetMerchantsReceivablesReport | GET | ✅ |
| BusinessProject/CreateRevenueAccount | POST | ✅ |
| BusinessProject/ApproveProinst | GET | ✅ |
| BusinessProject/GetExpenseSummary | GET | ✅ |
| BusinessProject/GetShopExpenseSummary | GET | ✅ |
| BusinessProject/GetMonthSummaryList | GET | ✅ |
| BusinessProject/GetNoProjectShopList | GET | ✅ |
| BusinessProject/GetAnnualSplit | GET | ✅ |
| BusinessProject/SaveHisPaymentAccount | POST | ✅ |
| BusinessProject/GetProjectAccountList | GET | ✅ |
| BusinessProject/GetProjectAccountTree | GET | ✅ |
| BusinessProject/GetProjectAccountDetail | GET | ✅ |
| BusinessProject/GetAccountWarningList | GET | ✅ |
| BusinessProject/SolidAccountWarningList | GET | ✅ |
| BusinessProject/GetAccountWarningListSummary | GET | ✅ |
| BusinessProject/GetMerchantSplit | GET | ✅ |
| BusinessProject/SolidProjectRevenue | GET | ✅ |
| BusinessProject/SolidPeriodWarningList | POST | ✅ |
| BusinessProject/SolidPeriodAnalysis | POST | ✅ |
| BusinessProject/GetPeriodWarningList | GET | ✅ |
| BusinessProject/ReconfigureProfit | GET | ✅ |
| BusinessProject/GetWillSettleProject | GET | ✅ |
| BusinessProject/UploadRevenueConfirmList | POST | ✅ |

**ExpensesController** (10 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Expenses/GetEXPENSESPREPAIDList | POST | ✅ |
| Expenses/GetEXPENSESPREPAIDDetail | GET | ✅ |
| Expenses/SynchroEXPENSESPREPAID | POST | ✅ |
| Expenses/DeleteEXPENSESPREPAID | POST | ✅ |
| Expenses/GetEXPENSESSEPARATEList | POST | ✅ |
| Expenses/GetEXPENSESSEPARATEDetail | GET | ✅ |
| Expenses/SynchroEXPENSESSEPARATE | POST | ✅ |
| Expenses/DeleteEXPENSESSEPARATE | POST | ✅ |
| Expenses/SynchroHisData | POST | ✅ |
| Expenses/GetShopExpenseHisList | POST | ✅ |

**ContractSynController** (4 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| ContractSyn/GetContractSynList | POST | ✅ |
| ContractSyn/GetContractSynDetail | GET | ✅ |
| ContractSyn/SynchroContractSyn | POST | ✅ |
| ContractSyn/DeleteContractSyn | POST | ✅ |

**CONTRACT_SYNController** (4 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| BusinessProject/GetCONTRACT_SYNList | POST | ✅ |
| BusinessProject/GetCONTRACT_SYNDetail | GET | ✅ |
| BusinessProject/SynchroCONTRACT_SYN | POST | ✅ |
| BusinessProject/DeleteCONTRACT_SYN | POST | ✅ |

### Finance 模块 — ✅ 全部完成
> ✅76 ❌0 ⏭️12 💬0 / 共88

**FinanceController** (48 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Finance/GetATTACHMENTList | POST | ✅ |
| Finance/GetATTACHMENTDetail | POST | ✅ |
| Finance/SynchroATTACHMENT | POST | ✅ |
| Finance/DeleteATTACHMENT | POST | ✅ |
| Finance/GetProjectSplitSummary | GET | ✅ |
| Finance/GetProjectSummary | GET | ✅ |
| Finance/GetRevenueSplitSummary | GET | ✅ |
| Finance/GetProjectMerchantSummary | GET | ✅ |
| Finance/CreateSingleProjectSplit | GET | ✅ |
| Finance/SolidMonthProjectSplit | GET | ✅ |
| Finance/GetRoyaltyDateSumReport | GET | ✅ |
| Finance/GetRoyaltyReport | GET | ✅ |
| Finance/GetProjectShopIncome | GET | ✅ |
| Finance/GetContractMerchant | GET | ✅ |
| Finance/GetAccountReached | GET | ✅ |
| Finance/GetShopExpense | GET | ✅ |
| Finance/GetReconciliation | GET | ✅ |
| Finance/GetRevenueRecognition | GET | ✅ |
| Finance/GetProjectPeriodIncome | GET | ✅ |
| Finance/GetProjectPeriodAccount | GET | ✅ |
| Finance/ApplyAccountProinst | POST | ✅ |
| Finance/ApproveAccountProinst | GET+POST | ✅ |
| Finance/RejectAccountProinst | GET+POST | ✅ |
| Finance/GetMonthAccountProinst | POST | ✅ |
| Finance/ApplyMonthAccountProinst | POST | ✅ |
| Finance/ApproveMonthAccountProinst | GET+POST | ✅ |
| Finance/ApproveMAPList | GET+POST | ✅ |
| Finance/RejectMonthAccountProinst | GET+POST | ✅ |
| Finance/StorageMonthProjectAccount | POST | ✅ |
| Finance/GetMonthAccountDiff | GET | ✅ |
| Finance/ApprovePeriodAccount | GET | ✅ |
| Finance/RejectPeriodAccount | GET | ✅ |
| Finance/GetPeriodSupplementList | GET | ✅ |
| Finance/GetProjectExpenseList | GET | ✅ |
| Finance/GetBankAccountAnalyseList | GET | ✅ |
| Finance/GetBankAccountAnalyseTreeList | GET | ✅ |
| Finance/SolidBankAccountSplit | POST | ✅ |
| Finance/GetContractExcuteAnalysis | GET | ✅ |
| Finance/RebuildSCSplit | GET+POST | ✅ |
| Finance/CorrectRevenueAccountData | POST | ✅ |
| Finance/RebuildClosedPeriod | POST | ✅ |
| Finance/RebuildReductionPeriod | POST | ✅ |
| Finance/SendSMSMessage | GET | ✅ |
| Finance/LadingBill | GET+POST | ✅ |
| Finance/RejectLadingBill | GET+POST | ✅ |
| Finance/GetAHJKtoken | POST | ✅ |
| Finance/GetAccountCompare | GET | ✅ |
| Finance/GetAnnualAccountList | GET | ✅ |

**InvoiceController** (24 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Invoice/GetBILLList | POST | ✅ |
| Invoice/GetBILLDetail | GET | ✅ |
| Invoice/SynchroBILL | POST | ✅ |
| Invoice/DeleteBILL | POST | ✅ |
| Invoice/GetBILLDETAILList | POST | ✅ |
| Invoice/GetBILLDETAILDetail | GET | ✅ |
| Invoice/SynchroBILLDETAIL | POST | ✅ |
| Invoice/DeleteBILLDETAIL | POST | ✅ |
| Invoice/GetINVOICEINFOList | POST | ⏭️加密 |
| Invoice/GetINVOICEINFODetail | POST | ⏭️加密 |
| Invoice/SynchroINVOICEINFO | POST | ⏭️加密 |
| Invoice/DeleteINVOICEINFO | POST | ⏭️加密 |
| Invoice/GetGOODSTAXINFOList | POST | ⏭️加密 |
| Invoice/GetGOODSTAXINFODetail | POST | ⏭️加密 |
| Invoice/SynchroGOODSTAXINFO | POST | ⏭️加密 |
| Invoice/DeleteGOODSTAXINFO | POST | ⏭️加密 |
| Office/GetAPPLYAPPROVEList | POST | ⏭️加密 |
| Office/GetAPPLYAPPROVEDetail | POST | ⏭️加密 |
| Office/SynchroAPPLYAPPROVE | POST | ⏭️加密 |
| Office/DeleteAPPLYAPPROVE | POST | ⏭️加密 |
| Invoice/WriteBackInvoice | POST | ✅ |
| Invoice/SendHXInvoiceInfo | POST | ✅ |
| Invoice/RewriteJDPJInfo | POST | ✅ |
| Invoice/ForwardJDPJInterface | POST | ✅ |

**BudgetProjectAHController** (16 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Budget/GetBudgetProjectList | POST | ✅ |
| Budget/GetbudgetProjectDetail | GET | ✅ |
| Budget/SynchroBudgetProject | POST | ✅ |
| Budget/DeleteBudgetProject | POST | ✅ |
| Budget/GetBudgetDetailList | POST | ✅ |
| Budget/GetBudgetDetailDetail | GET | ✅ |
| Budget/SynchroBudgetDetail | POST | ✅ |
| Budget/DeleteBudgetDetail | POST | ✅ |
| Budget/SetBudgetDetailAHList | POST | ✅ |
| Budget/GetBudgetProjectReportOfMonth | GET | ✅ |
| Budget/GetbudgetProjectReport | GET | ✅ |
| Budget/GetbudgetProjectReportDynamic | GET | ✅ |
| Budget/GetbudgetProjectReportIn | GET | ✅ |
| Budget/GetbudgetProjectReportInDynamic | GET | ✅ |
| Budget/GetbudgetProjectReportOut | GET | ✅ |
| Budget/GetbudgetProjectReportOutDynamic | GET | ✅ |

### Merchants 模块 — ✅ 已完成
> ✅15 ❌0 ⏭️1 💬0 / 共16

**MerchantsController** (16 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Merchants/GetCoopMerchantsList | POST | ✅ |
| Merchants/GetCoopMerchantsDetail | GET | ✅ |
| Merchants/SynchroCoopMerchants | POST | ✅ |
| Merchants/DeleteCoopMerchants | POST | ✅ |
| Merchants/GetCoopMerchantsTypeList | POST | ✅ |
| Merchants/SynchroCoopMerchantsType | POST | ✅ |
| Merchants/DeleteCoopMerchantsType | POST | ✅ |
| Merchants/GetCoopMerchantsLinkerList | POST | ✅ |
| Merchants/GetCoopMerchantsLinkerDetail | GET | ✅ |
| Merchants/SynchroCoopMerchantsLinker | POST | ✅ |
| Merchants/DeleteCoopMerchantsLinker | POST | ✅ |
| Merchants/GetRTCoopMerchantsList | POST | ✅ |
| Merchants/GetTradeBrandMerchantsList | POST | ✅ |
| Merchants/SynchroRTCoopMerchants | POST | ✅ |
| Merchants/DeleteRTCoopMerchants | POST | ✅ |
| Merchants/GetCoopMerchantsDDL | GET | ⏭️加密 |

### Revenue 模块 — ✅ 已完成
> ✅59 ❌0 ⏭️1 💬0 / 共60 | 完成日期: 2026-03-09

**RevenueController** (60 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Revenue/GetREVENUEDAILYSPLITList | POST | ✅ |
| Revenue/GetREVENUEDAILYSPLITDetail | GET | ✅ |
| Revenue/SynchroREVENUEDAILYSPLIT | POST | ✅ |
| Revenue/DeleteREVENUEDAILYSPLIT | POST | ✅ |
| Revenue/GetPERSONSELLList | POST | ✅ |
| Revenue/GetPERSONSELLDetail | GET | ✅ |
| Revenue/SynchroPERSONSELL | POST | ✅ |
| Revenue/DeletePERSONSELL | POST | ✅ |
| Revenue/GetBUSINESSANALYSISList | POST | ✅ |
| Revenue/GetBUSINESSANALYSISDetail | GET | ✅ |
| Revenue/SynchroBUSINESSANALYSIS | POST | ✅ |
| Revenue/DeleteBUSINESSANALYSIS | POST | ✅ |
| Revenue/GetBRANDANALYSISList | POST | ✅ |
| Revenue/GetBRANDANALYSISDetail | GET | ✅ |
| Revenue/SynchroBRANDANALYSIS | POST | ✅ |
| Revenue/DeleteBRANDANALYSIS | POST | ✅ |
| Revenue/GetSITUATIONANALYSISList | POST | ✅ |
| Revenue/GetSITUATIONANALYSISDetail | GET | ✅ |
| Revenue/SynchroSITUATIONANALYSIS | POST | ✅ |
| Revenue/DeleteSITUATIONANALYSIS | POST | ✅ |
| Revenue/GetBUSINESSWARNINGList | POST | ✅ |
| Revenue/GetBUSINESSWARNINGDetail | GET | ✅ |
| Revenue/SynchroBUSINESSWARNING | POST | ✅ |
| Revenue/DeleteBUSINESSWARNING | POST | ✅ |
| Revenue/GetACCOUNTWARNINGList | POST | ✅ |
| Revenue/GetACCOUNTWARNINGDetail | GET | ✅ |
| Revenue/SynchroACCOUNTWARNING | POST | ✅ |
| Revenue/DeleteACCOUNTWARNING | POST | ✅ |
| Revenue/GetBusinessDate | GET | ⏭️加密 |
| Revenue/ModifyRevenueDailySplitList | POST | ✅ |
| Revenue/GetRevenuePushList | POST | ✅ |
| Revenue/GetHisCommoditySaleList | POST | ✅ |
| Revenue/GetRevenueDataList | GET | ✅ |
| Revenue/GetRevenueReport | GET | ✅ |
| Revenue/GetRevenueReportByDate | GET | ✅ |
| Revenue/GetMerchantRevenueReport | GET | ✅ |
| Revenue/BankAccountCompare | GET | ✅ |
| Revenue/GetBankAccountReport | GET | ✅ |
| Revenue/GetBankAccountList | GET | ✅ |
| Revenue/GetCurTotalRevenue | GET | ✅ |
| Revenue/GetTotalRevenue | GET | ✅ |
| Revenue/GetYSSellMasterList | POST | ✅ |
| Revenue/GetSellMasterCompareList | POST | ✅ |
| Revenue/GetYSSellDetailsList | POST | ✅ |
| Revenue/GetTransactionCustomer | POST | ✅ |
| Revenue/GetTransactionCustomerByDate | POST | ✅ |
| Revenue/GetRevenueYOYQOQ | POST | ✅ |
| Revenue/GetRevenueYOYQOQByDate | POST | ✅ |
| Revenue/GetRevenueQOQ | POST | ✅ |
| Revenue/GetRevenueQOQByDate | POST | ✅ |
| Revenue/GetMonthCompare | POST | ✅ |
| Revenue/GetBusinessAnalysisReport | POST | ✅ |
| Revenue/GetSituationAnalysis | GET | ✅ |
| Revenue/GetBusinessTradeAnalysis | GET | ✅ |
| Revenue/GetBrandAnalysis | GET | ✅ |
| Revenue/GetMonthINCAnalysis | GET | ✅ |
| Revenue/GetRevenueReportByBIZPSPLITMONTH | GET | ✅ |
| Revenue/CorrectShopCigarette | POST | ✅ |
| Revenue/GetCigaretteReport | GET | ✅ |
| Revenue/GetBusinessItemSummary | GET | ✅ |

### BigData 模块 — ✅ 已完成
> ✅37 ❌0 ⏭️3 💬0 / 共40 | 完成日期: 2026-03-09

**BigDataController** (36 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| BigData/GetSECTIONFLOWList | POST | ✅ |
| BigData/GetSECTIONFLOWDetail | GET | ✅ |
| BigData/SynchroSECTIONFLOW | POST | ✅ |
| BigData/DeleteSECTIONFLOW | POST | ✅ |
| BigData/GetSECTIONFLOWMONTHList | POST | ✅ |
| BigData/GetSECTIONFLOWMONTHDetail | GET | ✅ |
| BigData/SynchroSECTIONFLOWMONTH | POST | ✅ |
| BigData/DeleteSECTIONFLOWMONTH | POST | ✅ |
| BigData/GetBAYONETList | POST | ✅ |
| BigData/GetBAYONETDetail | GET | ✅ |
| BigData/SynchroBAYONET | POST | ✅ |
| BigData/DeleteBAYONET | POST | ✅ |
| BigData/GetBAYONETDAILY_AHList | POST | ✅ |
| BigData/GetBAYONETDAILY_AHDetail | GET | ✅ |
| BigData/SynchroBAYONETDAILY_AH | POST | ✅ |
| BigData/DeleteBAYONETDAILY_AH | POST | ✅ |
| BigData/A2305052305180725 | GET | ✅ |
| BigData/GetDailyBayonetAnalysis | GET | ✅ |
| BigData/GetServerpartSectionFlow | GET | ✅ |
| Revenue/GetBAYONETANALYSISList | POST | ✅ |
| Revenue/GetBAYONETANALYSISDetail | GET | ✅ |
| Revenue/SynchroBAYONETANALYSIS | POST | ✅ |
| Revenue/DeleteBAYONETANALYSIS | POST | ✅ |
| Revenue/GetBAYONETOAANALYSISList | POST | ✅ |
| Revenue/GetBAYONETOAANALYSISDetail | GET | ✅ |
| Revenue/SynchroBAYONETOAANALYSIS | POST | ✅ |
| Revenue/DeleteBAYONETOAANALYSIS | POST | ✅ |
| BigData/GetBAYONETWARNINGList | POST | ✅ |
| BigData/GetBAYONETWARNINGDetail | POST | ⏭️加密 |
| BigData/SynchroBAYONETWARNING | POST | ⏭️加密 |
| BigData/DeleteBAYONETWARNING | POST | ⏭️加密 |
| Revenue/GetBayonetVehicleAnalysis | GET | ✅ |
| BigData/GetTimeIntervalList | GET | ✅ |
| BigData/GetBayonetOwnerAHList | GET | ✅ |
| BigData/GetBayonetOwnerMonthAHList | GET | ✅ |
| BigData/GetUreaMasterList | POST | ✅ |

**CustomerController** (4 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Customer/GetCUSTOMERGROUP_AMOUNTList | POST | ✅ |
| Customer/GetCUSTOMERGROUP_AMOUNTDetail | GET | ✅ |
| Customer/SynchroCUSTOMERGROUP_AMOUNT | POST | ✅ |
| Customer/DeleteCUSTOMERGROUP_AMOUNT | POST | ✅ |

### MobilePay 模块 — ✅ 已完成
> ✅17 ❌0 ⏭️1 💬0 / 共18 | 完成日期: 2026-03-09

**MobilePayController** (18 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| MobilePay/SetKwyRoyaltyRate | POST | ✅ |
| MobilePay/GetKwyRoyaltyRate | POST | ✅ |
| MobilePay/RoyaltyWithdraw | POST | ✅ |
| MobilePay/GetKwyRoyalty | GET | ✅ |
| MobilePay/GetKwyRoyaltyForAll | GET | ✅ |
| MobilePay/GetMobilePayRoyaltyReport | GET | ✅ |
| MobilePay/SynchroBANKACCOUNTVERIFY | POST | ✅ |
| MobilePay/GetBANKACCOUNTVERIFYList | POST | ✅ |
| MobilePay/GetBANKACCOUNTVERIFYRegionList | POST | ✅ |
| MobilePay/GetBANKACCOUNTVERIFYServerList | POST | ✅ |
| MobilePay/GetBANKACCOUNTVERIFYTreeList | GET | ✅ |
| MobilePay/GetRoyaltyRecordList | POST | ✅ |
| MobilePay/GetMobilePayResult | POST | ✅ |
| MobilePay/CorrectSellMasterState | POST | ⏭️加密 |
| MobilePay/GetChinaUmsSubMaster | POST | ✅ |
| MobilePay/GetChinaUmsSubAccountDetail | POST | ✅ |
| MobilePay/GetChinaUmsSubAccountSummary | POST | ✅ |
| MobilePay/GetChinaUmsSubSummary | POST | ✅ |

### Audit 模块 — ✅ 已完成
> ✅24 ❌0 ⏭️0 💬0 / 共24 | 完成日期: 2026-03-09

**AuditController** (24 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Audit/GetYSABNORMALITYList | POST | ✅ |
| Audit/GetYSABNORMALITYDetail | GET | ✅ |
| Audit/GetYSABNORMALITYDETAILList | POST | ✅ |
| Audit/GetABNORMALAUDITList | POST | ✅ |
| Audit/GetAbnormalAuditDetail | GET | ✅ |
| Audit/SynchroAbnormalAudit | POST | ✅ |
| Audit/DeleteAbnormalAudit | POST | ✅ |
| Audit/GetCHECKACCOUNTList | POST | ✅ |
| Audit/GetCHECKACCOUNTDetail | GET | ✅ |
| Audit/SynchroCHECKACCOUNT | POST | ✅ |
| Audit/DeleteCHECKACCOUNT | POST | ✅ |
| Audit/GetAUDITTASKSList | POST | ✅ |
| Audit/GetAUDITTASKSDetail | GET | ✅ |
| Audit/SynchroAUDITTASKS | POST | ✅ |
| Audit/GetAuditList | POST | ✅ |
| Audit/GetAuditDetils | POST | ✅ |
| Audit/UpLoadAuditExplain | POST | ✅ |
| Audit/GetCheckAccountReport | POST | ✅ |
| Audit/GetYsabnormalityReport | POST | ✅ |
| Audit/GetSpecialBehaviorReport | POST | ✅ |
| Audit/GetAbnormalRateReport | POST | ✅ |
| Audit/GetAuditTasksReport | POST | ✅ |
| Audit/GetAuditTasksDetailList | POST | ✅ |
| Audit/IssueAuditTasks | POST | ✅ |

### Analysis 模块 — ✅ 已完成
> ✅58 ❌0 ⏭️4 💬0 / 共62 | 完成日期: 2026-03-09

**AnalysisController** (62 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Analysis/GetANALYSISINSList | POST | ✅ |
| Analysis/GetANALYSISINSDetail | GET | ✅ |
| Analysis/SynchroANALYSISINS | POST | ✅ |
| Analysis/DeleteANALYSISINS | POST | ✅ |
| Analysis/GetSENTENCEList | POST | ✅ |
| Analysis/GetSENTENCEDetail | GET | ✅ |
| Analysis/SynchroSENTENCE | POST | ✅ |
| Analysis/DeleteSENTENCE | POST | ✅ |
| Analysis/GetASSETSPROFITSList | POST | ✅ |
| Analysis/GetASSETSPROFITSTreeList | POST | ✅ |
| Analysis/GetASSETSPROFITSBusinessTreeList | POST | ✅ |
| Analysis/GetASSETSPROFITSDetail | GET | ✅ |
| Analysis/GetASSETSPROFITSDateDetailList | GET | ✅ |
| Analysis/SynchroASSETSPROFITS | POST | ✅ |
| Analysis/DeleteASSETSPROFITS | POST | ✅ |
| Analysis/GetAssetsLossProfitList | GET | ✅ |
| Analysis/GetPROFITCONTRIBUTEList | POST | ✅ |
| Analysis/GetPROFITCONTRIBUTEDetail | GET | ✅ |
| Analysis/SynchroPROFITCONTRIBUTE | POST | ✅ |
| Analysis/DeletePROFITCONTRIBUTE | POST | ✅ |
| Analysis/GetPERIODMONTHPROFITList | POST | ✅ |
| Analysis/GetPERIODMONTHPROFITDetail | GET | ✅ |
| Analysis/SynchroPERIODMONTHPROFIT | POST | ✅ |
| Analysis/DeletePERIODMONTHPROFIT | POST | ✅ |
| Analysis/GetVEHICLEAMOUNTList | POST | ✅ |
| Analysis/GetVEHICLEAMOUNTDetail | GET | ✅ |
| Analysis/SynchroVEHICLEAMOUNT | POST | ✅ |
| Analysis/DeleteVEHICLEAMOUNT | POST | ✅ |
| Analysis/GetANALYSISRULEList | POST | ✅ |
| Analysis/GetANALYSISRULEDetail | GET | ✅ |
| Analysis/SynchroANALYSISRULE | POST | ✅ |
| Analysis/DeleteANALYSISRULE | POST | ✅ |
| Analysis/GetPREFERRED_RATINGList | POST | ✅ |
| Analysis/GetPREFERRED_RATINGDetail | GET | ✅ |
| Analysis/SynchroPREFERRED_RATING | POST | ✅ |
| Analysis/DeletePREFERRED_RATING | POST | ✅ |
| Analysis/GetPROMPTList | POST | ✅ |
| Analysis/GetPROMPTDetail | GET | ✅ |
| Analysis/SynchroPROMPT | POST | ✅ |
| Analysis/DeletePROMPT | POST | ✅ |
| Analysis/GetINVESTMENTANALYSISList | POST | ✅ |
| Analysis/GetINVESTMENTANALYSISDetail | GET | ✅ |
| Analysis/SynchroINVESTMENTANALYSIS | POST | ✅ |
| Analysis/DeleteINVESTMENTANALYSIS | POST | ✅ |
| Analysis/GetINVESTMENTDETAILList | POST | ✅ |
| Analysis/GetINVESTMENTDETAILDetail | GET | ✅ |
| Analysis/SynchroINVESTMENTDETAIL | POST | ✅ |
| Analysis/DeleteINVESTMENTDETAIL | POST | ✅ |
| Analysis/GetSPCONTRIBUTIONList | POST | ⏭️加密 |
| Analysis/GetSPCONTRIBUTIONDetail | POST | ⏭️加密 |
| Analysis/SynchroSPCONTRIBUTION | POST | ⏭️加密 |
| Analysis/DeleteSPCONTRIBUTION | POST | ⏭️加密 |
| Analysis/SyncPROFITCONTRIBUTEList | POST | ✅ |
| Analysis/ReCalcCACost | GET | ✅ |
| Analysis/GetShopSABFIList | GET | ✅ |
| Analysis/SolidProfitAnalysis | POST | ✅ |
| Analysis/GetPeriodMonthlyList | GET | ✅ |
| Analysis/GetRevenueEstimateList | GET | ✅ |
| Analysis/SolidShopSABFI | POST | ✅ |
| Analysis/SolidInvestmentAnalysis | POST | ✅ |
| Analysis/GetInvestmentReport | GET | ✅ |
| Analysis/GetNestingIAReport | GET | ✅ |

### BusinessMan 模块 — ✅ 已完成
> ✅39 ❌0 ⏭️0 💬0 / 共39 | 完成日期: 2026-03-09

**BusinessManController** (26 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Merchants/GetBusinessManList | POST | ✅ |
| Merchants/GetBusinessManDetail | GET | ✅ |
| Merchants/SynchroBusinessMan | POST | ✅ |
| Merchants/DeleteBusinessMan | POST | ✅ |
| Merchants/GetBusinessManDetailList | POST | ✅ |
| Merchants/GetBusinessManDetailDetail | GET | ✅ |
| Merchants/SynchroBusinessManDetail | POST | ✅ |
| Merchants/DeleteBusinessManDetail | POST | ✅ |
| Merchants/GetCommodityList | POST | ✅ |
| Merchants/GetCommodityDetail | GET | ✅ |
| Merchants/SynchroCommodity | POST | ✅ |
| Merchants/DeleteCommodity | POST | ✅ |
| Merchants/GetCUSTOMTYPEList | POST | ✅ |
| Merchants/GetCUSTOMTYPEDetail | GET | ✅ |
| Merchants/SynchroCUSTOMTYPE | POST | ✅ |
| Merchants/DeleteCUSTOMTYPE | POST | ✅ |
| BusinessMan/GetCOMMODITY_TEMPList | POST | ✅ |
| BusinessMan/GetCOMMODITY_TEMPDetail | GET | ✅ |
| BusinessMan/SynchroCOMMODITY_TEMP | POST | ✅ |
| BusinessMan/DeleteCOMMODITY_TEMP | POST | ✅ |
| BusinessMan/AuthorizeQualification | POST | ✅ |
| Merchants/GetNestingCustomTypeLsit | GET | ✅ |
| Merchants/GetCustomTypeDDL | GET | ✅ |
| BusinessMan/CreateBusinessMan | POST | ✅ |
| BusinessMan/GetUserList | POST | ✅ |
| BusinessMan/GetUserList | GET | ✅ |

**SupplierController** (13 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Supplier/GetSupplierList | POST | ✅ |
| Supplier/GetSupplierTreeList | POST | ✅ |
| Supplier/GetSupplierDetail | GET | ✅ |
| Supplier/SynchroSupplier | POST | ✅ |
| Supplier/DeleteSupplier | POST | ✅ |
| Supplier/GetQualificationList | POST | ✅ |
| Supplier/GetQualificationDetail | GET | ✅ |
| Supplier/SynchroQualification | POST | ✅ |
| Supplier/DeleteQualification | POST | ✅ |
| Supplier/GetQUALIFICATION_HISList | POST | ✅ |
| Supplier/GetQUALIFICATION_HISDetail | GET | ✅ |
| Supplier/SynchroQUALIFICATION_HIS | POST | ✅ |
| Supplier/RelateBusinessCommodity | POST | ✅ |

### DataVerification 模块 — ✅ 已完成
> ✅36 ❌0 ⏭️0 💬0 / 共36 | 完成日期: 2026-03-09

**VerificationController** (23 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Verification/GetENDACCOUNTModel | GET | ✅ |
| Verification/SynchroENDACCOUNT | POST | ✅ |
| Verification/DeleteENDACCOUNT | POST | ✅ |
| Verification/GetEndaccountList | POST | ✅ |
| Verification/GetEndaccountDetail | POST | ✅ |
| Verification/VerifyEndaccount | POST | ✅ |
| Verification/ApproveEndaccount | POST | ✅ |
| Verification/SubmitEndaccountState | POST | ✅ |
| Verification/GetEndaccountHisList | POST | ✅ |
| Verification/GetSuppEndaccountList | GET | ✅ |
| Verification/ApplyEndaccountInvalid | POST | ✅ |
| Verification/CancelEndaccount | POST | ✅ |
| Verification/GetDataVerificationList | GET | ✅ |
| Verification/GetShopEndaccountSum | GET | ✅ |
| Verification/GetEndAccountData | GET | ✅ |
| Verification/GetCommoditySaleList | GET | ✅ |
| Verification/GetMobilePayDataList | GET | ✅ |
| Verification/GetEndaccountSupplement | GET | ✅ |
| Verification/SaveCorrectData | POST | ✅ |
| Verification/SaveSaleSupplement | POST | ✅ |
| Verification/ExceptionHandling | POST | ✅ |
| Verification/RebuildDailyAccount | GET | ✅ |
| Verification/CorrectDailyEndaccount | GET | ✅ |

**SalesController** (13 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Sales/GetCOMMODITYSALEList | POST | ✅ |
| Sales/GetCOMMODITYSALEDetail | GET | ✅ |
| Sales/SynchroCOMMODITYSALE | POST | ✅ |
| Sales/DeleteCOMMODITYSALE | POST | ✅ |
| Sales/GetEndaccountSaleInfo | POST | ✅ |
| Sales/RecordSaleData | POST | ✅ |
| Sales/GetEndaccountError | POST | ✅ |
| Sales/UpdateEndaccountError | POST | ✅ |
| Sales/GetCommoditySaleSummary | POST | ✅ |
| Sales/GetCommodityTypeSummary | POST | ✅ |
| Sales/GetCommodityTypeHistory | POST | ✅ |
| Sales/SaleRank | POST | ✅ |
| Sales/UpdateCommoditySale | POST | ✅ |

### Picture 模块 — ✅ 已完成
> ✅9 ❌0 ⏭️0 💬0 / 共9 | 完成日期: 2026-03-09

**PictureController** (9 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| Picture/GetPictureList | POST | ✅ |
| Picture/UploadPicture | POST | ✅ |
| Picture/SaveImgFile | POST | ✅ |
| Picture/GetEndaccountEvidence | POST | ✅ |
| Picture/UploadEndaccountEvidence | POST | ✅ |
| Picture/GetAuditEvidence | POST | ✅ |
| Picture/UploadAuditEvidence | POST | ✅ |
| Picture/DeletePicture | POST | ✅ |
| Picture/DeleteMultiPicture | POST | ✅ |

### Video 模块 — ❌ 待迁移（剩余 16 个）
> ✅0 ❌16 ⏭️0 💬0 / 共16

**ShopVideoController** (16 个接口)

| 路由 | 方法 | 状态 |
|------|------|------|
| ShopVideo/GetEXTRANETList | POST | ❌ |
| ShopVideo/GetEXTRANETDetail | GET | ❌ |
| ShopVideo/SynchroEXTRANET | POST | ❌ |
| ShopVideo/DeleteEXTRANET | POST | ❌ |
| ShopVideo/GetEXTRANETDETAILList | POST | ❌ |
| ShopVideo/GetEXTRANETDETAILDetail | GET | ❌ |
| ShopVideo/SynchroEXTRANETDETAIL | POST | ❌ |
| ShopVideo/DeleteEXTRANETDETAIL | POST | ❌ |
| ShopVideo/GetSHOPVIDEOList | POST | ❌ |
| ShopVideo/GetSHOPVIDEODetail | GET | ❌ |
| ShopVideo/SynchroSHOPVIDEO | POST | ❌ |
| ShopVideo/DeleteSHOPVIDEO | POST | ❌ |
| ShopVideo/GetVIDEOLOGList | POST | ❌ |
| ShopVideo/SynchroVIDEOLOG | POST | ❌ |
| ShopVideo/GetShopVideoInfo | POST | ❌ |
| ShopVideo/GetYSShopVideoInfo | POST | ❌ |
---

## 进度总览

| 指标 | 数值 |
|------|------|
| 迁移范围总路由 | 685 |
| 其中加密跳过 | 36 |
| 其中别名跳过 | 4 |
| 实际需迁移 | **645** |
| 已完成 | **631** |
| 剩余 | **14**（Video 16 − BaseInfo 已含） |
| 完成率 | **97.8%** |
| 已完成 Controller | BaseInfo✅ BasicConfig✅ Contract✅ Merchants✅ Finance✅ Invoice✅ BudgetProjectAH✅ Revenue✅ BigData✅ Customer✅ MobilePay✅ Audit✅ Analysis✅ BusinessMan✅ Supplier✅ Verification✅ Sales✅ Picture✅ |

---

## 实施阶段

### 阶段一：BaseInfo 基础信息补全（P0）

> **当前进度：94 / 145 接口，完成率 64.8%**（BaseInfoController 94✅ + BasicConfigController 29✅ + CommodityController 6✅ = 129✅）

| 批次 | 内容 | 接口数 | 状态 |
|------|------|--------|------|
| B1 | OWNERUNIT（业主单位） | 4 | ✅ 已完成 |
| B2 | SERVERPART（服务区站点） | 2 | ✅ 已完成 |
| B3 | ServerpartShop（门店） | 5 | ✅ 已完成 |
| B4 | Brand（品牌） | 6 | ✅ 已完成 |
| B5.1 | RTSERVERPARTSHOP + SERVERPARTSHOP_LOG + CASHWORKER | 9 | ✅ 已完成 |
| B5.2 | BusinessTrade（经营业态） | 6 | ✅ 已完成 |
| B5.3 | AUTOSTATISTICS（自定义统计归口） | 4 | ✅ 已完成 |
| B5.4 | COMMODITYTYPE（商品类别） | 6 | ✅ 已完成 |
| B5.5 | USERDEFINEDTYPE（商品自定义类别） | 5 | ✅ 已完成 |
| B5.6 | SERVERPARTCRT（服务区成本核算对照） | 5 | ✅ 已完成 |
| B5.7 | PROPERTYASSETS（服务区资产） | 7 | ✅ 已完成 |
| B5.8 | COMMODITY（在售商品） | 6 | ✅ 已完成 |
| B5.9 | BaseInfoController 散装接口 | 20 | ✅ 已完成 |
| B6 | BasicConfigController | 29 | ✅ 已完成 |
| B7 | CommodityController（6✅ / 11⏭️加密） | 17 | ✅ 已完成 |

### 阶段二：Merchants 商户管理（P0）✅ 已完成

MerchantsController 16 个路由（15✅ + 1⏭️加密）：CoopMerchants CRUD、类型、联系人、关联查询。

| 状态 | 说明 |
|------|------|
| ✅ 已完成 | 15/16 接口（1个加密跳过）2026-03-08 |

### 阶段三：Contract 合同管理（P1）✅ 已完成

✅ 全部 132 个路由已完成（130 实现 + 2 加密跳过）

| Controller | 路由数 | 状态 |
|------------|--------|------|
| ContractController | 27 | ✅ 已完成25/⏭️2 |
| BusinessProjectController | 87 | ✅ 全部完成 |
| ExpensesController | 10 | ✅ 全部完成 |
| ContractSynController | 4 | ✅ 全部完成 |
| CONTRACT_SYNController | 4 | ✅ 全部完成 |

### 阶段四：Finance 财务管理（P1-P2）

| Controller | 路由数 | 状态 |
|------------|--------|------|
| FinanceController | 48 | ✅ 已完成 2026-03-08 |
| InvoiceController | 24 | ✅ 已完成 12实现+12加密跳过 |
| BudgetProjectAHController | 16 | ✅ 已完成 2026-03-08 |

### 阶段五：Revenue 收入管理（P2）✅ 已完成

RevenueController 60 个路由：7 组 CRUD + 31 散装报表/销售/同环比分析。

| 状态 | 说明 |
|------|------|
| ✅ 已完成 | 59/60 接口（1个加密跳过）2026-03-09 |

### 阶段六：BigData 大数据（P2）✅ 已完成

BigDataController (36) + CustomerController (4)。

| 状态 | 说明 |
|------|------|
| ✅ 已完成 | 37/40 接口（3个加密跳过）2026-03-09 |

### 阶段七：中型模块批量迁移（P3）✅ 已完成

| Controller | 路由数 | 状态 |
|------------|--------|------|
| MobilePayController | 18 | ✅ 17实现+1加密 |
| AuditController | 24 | ✅ 全部完成 |
| AnalysisController | 62 | ✅ 58实现+4加密 |
| BusinessManController | 26 | ✅ 全部完成 |
| SupplierController | 13 | ✅ 全部完成 |
| VerificationController | 23 | ✅ 全部完成 |
| SalesController | 13 | ✅ 全部完成 |

### 阶段八：轻量模块收尾（P4）

PictureController (9✅) + ShopVideoController (16❌)。

| 状态 | 说明 |
|------|------|
| 🟡 部分完成 | Picture 9✅ / Video 16❌待迁移 |

---

## 工作量预估

| 阶段 | 总接口数 | 已完成 | 剩余 | 状态 |
|------|---------|--------|------|------|
| 一（BaseInfo） | 145 | 129 | 16（加密+别名） | ✅ 已完成 |
| 二（Merchants） | 16 | 15 | 1⏭️ | ✅ 已完成 |
| 三（Contract） | 132 | 130 | 2⏭️ | ✅ 已完成 |
| 四（Finance） | 88 | 76 | 12⏭️ | ✅ 已完成 |
| 五（Revenue） | 60 | 59 | 1⏭️ | ✅ 已完成 |
| 六（BigData） | 40 | 37 | 3⏭️ | ✅ 已完成 |
| 七（中型模块） | 179 | 174 | 5⏭️ | ✅ 已完成 |
| 八（轻量收尾） | 25 | 9 | 16 | 🟡 Video待迁移 |
| **总计** | **685** | **631**（+40⏭️） | **16** | **97.8%** |

---

## 执行流程

每个接口严格遵循 `/api-migration` 工作流 6 步法：

1. 读原 C# Controller → Helper → Model
2. 调原 API 获取基准数据
3. 同步数据库表（Oracle → 达梦）
4. 实现 Python 接口（Model → Service → Router）
5. 对比验证（compare_api.py）
6. 问题标注（更新 migration_issues.md + 工作流）

---

## 数据库同步策略

> Oracle（原库）→ 达梦 NEWPYTHON（新库），需要保证数据一致才能做接口对比验证。

### 阶段划分

```
[开发期] Oracle 为主库，达梦为镜像库 → 定期全量同步
[过渡期] 双库并行，新老 API 共存 → 增量同步或双写
[上线后] 达梦为主库 → Oracle 停用
```

### 一、初始全量同步（开发前）

每个 Controller 涉及的表，在开发前必须确认已同步到达梦。

**操作流程**：

1. **梳理依赖表清单**：读原 Helper SQL，列出每个接口涉及的所有表（含 JOIN 表、字典表）
2. **确认达梦已有数据**：

```python
# scripts/check_dm_tables.py
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()
# 检查所有需要的表是否存在及数据量
tables = ['T_BRAND', 'T_MERCHANTS', 'T_CONTRACT', ...]  # 按需补充
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  ✅ {t:30s} {cur.fetchone()[0]:>8} 条")
    except:
        print(f"  ❌ {t:30s} 表不存在")
```

3. **缺失的表**：用达梦数据迁移工具（DTS）或手动导入

### 二、字段类型校验（每张表必做）

已知问题 P1：达梦导入工具可能将 NUMBER 列导为 VARCHAR。

**每张表迁移后必须执行**：

```python
# 对比 Oracle 和达梦的字段类型
# Oracle 端
cur_ora.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, DATA_PRECISION, DATA_SCALE 
    FROM ALL_TAB_COLUMNS 
    WHERE OWNER='COOP_MERCHANT' AND TABLE_NAME='T_XXX' 
    ORDER BY COLUMN_ID
""")
# 达梦端
cur_dm.execute("""
    SELECT COLUMN_NAME, DATA_TYPE 
    FROM USER_TAB_COLUMNS 
    WHERE TABLE_NAME='T_XXX' 
    ORDER BY COLUMN_ID
""")
```

**类型不一致时**修改达梦列：

```sql
-- 示例：将 VARCHAR 改为 INT
ALTER TABLE T_BRAND MODIFY BRAND_ID INT;
ALTER TABLE T_BRAND MODIFY BRAND_PID INT;
ALTER TABLE T_BRAND MODIFY BRAND_CATEGORY INT;
-- 注意：有数据时需确保所有值能转为目标类型
```

### 三、开发期增量同步

开发期间 Oracle 仍然是生产库，数据会变化。两种方案选其一：

**方案 A：定期全量覆盖（推荐，简单可靠）**

- 每周一次全量重新导入（用达梦 DTS 工具）
- 适合：表数据量不大（万级以内），迁移窗口期短
- 脚本：`scripts/sync_full.py`

**方案 B：增量同步（数据量大时）**

- 按 `OPERATE_DATE` 或主键 ID 范围增量同步
- 适合：大表（十万级以上），不希望每次全量
- 脚本：`scripts/sync_incremental.py`
- 注意：需要原 Oracle 表有时间戳字段支持

### 四、表依赖关系记录

迁移每个 Controller 时，在 `docs/table_dependencies.md` 中记录该接口依赖的表：

```markdown
| Controller | 接口 | 主表 | JOIN 表 | 字典表 |
|------------|------|------|---------|--------|
| BaseInfoController | GetBrandList | T_BRAND | T_MERCHANTS, T_SERVERPART | T_BUSINESSTRADE |
| ContractController | GetContractList | T_CONTRACT | T_MERCHANTS, T_SERVERPART | T_CONTRACTTYPE |
```

这样可以：
- 快速知道迁移某个接口前需要同步哪些表
- 确保关联表都已导入达梦
- 排查数据不一致时精确定位

### 五、切换上线检查清单

正式切换到达梦前的最终验证：

- [ ] 所有依赖表的数据量与 Oracle 一致
- [ ] 所有字段类型已校正（无 VARCHAR 冒充 INT 的情况）
- [ ] 序列（SEQUENCE）的当前值 ≥ Oracle 最大 ID
- [ ] 全部接口对比验证通过
- [ ] 写操作（INSERT/UPDATE/DELETE）在达梦端测试通过
- [ ] 事务和并发测试通过
