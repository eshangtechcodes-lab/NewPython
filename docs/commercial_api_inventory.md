# CommercialApi 接口台账（初始化）

> 来源：根据 `routers/commercial_api/*.py` 当前代码自动抽取路由后整理。
>
> 统计日期：2026-03-09
>
> 用途：作为 `CommercialApi` 内容级验收、问题归因、并行分工的基础台账。

## 1. 总览

- 当前已实现路由数：`123`
- 当前 router 文件数：`11`
- 其中业务 router：`10`
- 调试 router：`1`
- POST 路由数：`20`
- 明确使用 AES 解密的高风险接口：`11`

建议首轮验收批次：

1. `P0`：`Revenue`、`BaseInfo`、`Contract`、`Examine`
2. `P1`：`BigData`、`Customer`、`Analysis`
3. `P2`：`Budget`、`AbnormalAudit`、`BusinessProcess`
4. `P3`：`Debug`

## 2. 模块摘要

| 模块 | 文件 | 路由数 | POST | 已知高风险 | 验收优先级 |
|------|------|------:|-----:|------------|------------|
| Revenue | `revenue_router.py` | 50 | 3 | 统计口径、复杂聚合、部分 AES | P0 |
| BaseInfo | `base_info_router.py` | 9 | 3 | 列表筛选、树结构、2 个 AES | P0 |
| Contract | `contract_router.py` | 3 | 0 | 明细字段、账户拆分 | P0 |
| Examine | `examine_router.py` | 15 | 4 | 列表/明细混合、1 个 AES、数据同步依赖 | P0 |
| BigData | `bigdata_router.py` | 24 | 3 | 路由前缀混合、图表聚合、3 个 AES | P1 |
| Customer | `customer_router.py` | 7 | 0 | 画像统计、口径一致性 | P1 |
| Analysis | `analysis_router.py` | 7 | 4 | 文本分析、地图配置、1 个 AES | P1 |
| Budget | `budget_router.py` | 4 | 1 | 预算主从明细 | P2 |
| AbnormalAudit | `abnormal_audit_router.py` | 2 | 2 | 2 个 AES | P2 |
| BusinessProcess | `business_process_router.py` | 1 | 0 | 单接口，低复杂度 | P2 |
| Debug | `debug_router.py` | 1 | 0 | 调试用途，非验收主路径 | P3 |

## 3. 高风险接口标记规则

首轮验收时，优先关注以下类型：

- AES 解密接口
- POST Body 接口
- 聚合统计接口
- 树形结构接口
- 列表 + 明细联动接口
- 依赖实时/固化双口径接口
- 依赖 Oracle 与 DM 数据同步质量的接口

## 4. 明确使用 AES 的接口

以下接口在当前代码中明确调用了 `decrypt_post_data`：

| 模块 | 接口 |
|------|------|
| AbnormalAudit | `POST /AbnormalAudit/GetCurrentEarlyWarning` |
| AbnormalAudit | `POST /AbnormalAudit/GetMonthEarlyWarning` |
| Analysis | `POST /Analysis/GetServerpartTypeAnalysis` |
| BaseInfo | `POST /BaseInfo/GetServerpartServiceSummary` |
| BaseInfo | `POST /BaseInfo/GetBrandStructureAnalysis` |
| BigData | `POST /BigData/GetCurBusyRank` |
| BigData | `POST /BigData/GetRevenueTrendChart` |
| BigData | `POST /BigData/GetEnergyRevenueInfo` |
| Examine | `POST /Examine/GetEvaluateResList` |
| Revenue | `POST /Revenue/GetBusinessRevenueList` |
| Revenue | `POST /Revenue/GetMonthlyBusinessRevenue` |

## 5. 接口清单

### 5.1 Revenue

文件：[revenue_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/revenue_router.py)

- `GET /Revenue/GetRevenuePushList`
- `GET /Revenue/GetSummaryRevenue`
- `GET /Revenue/GetSummaryRevenueMonth`
- `GET /Revenue/GetWechatPushSalesList`
- `GET /Revenue/GetUnUpLoadShops`
- `GET /Revenue/GetServerpartBrand`
- `GET /Revenue/GetServerpartEndAccountList`
- `GET /Revenue/GetShopEndAccountList`
- `POST /Revenue/GetBudgetExpenseList`
- `GET /Revenue/GetBudgetExpenseList`
- `GET /Revenue/GetRevenueBudget`
- `GET /Revenue/GetProvinceRevenueBudget`
- `GET /Revenue/GetMobileShare`
- `GET /Revenue/GetMallDeliver`
- `GET /Revenue/GetTransactionAnalysis`
- `GET /Revenue/GetTransactionTimeAnalysis`
- `GET /Revenue/GetTransactionConvert`
- `GET /Revenue/GetBusinessTradeRevenue`
- `GET /Revenue/GetBusinessTradeLevel`
- `GET /Revenue/GetBusinessBrandLevel`
- `GET /Revenue/GetRevenueTrend`
- `GET /Revenue/GetRevenueReport`
- `GET /Revenue/GetRevenueReportDetil`
- `GET /Revenue/GetSalableCommodity`
- `GET /Revenue/GetSPRevenueRank`
- `GET /Revenue/GetRevenueYOY`
- `GET /Revenue/GetHolidayCompare`
- `GET /Revenue/GetAccountReceivable`
- `GET /Revenue/GetCurRevenue`
- `GET /Revenue/GetShopCurRevenue`
- `GET /Revenue/GetLastSyncDateTime`
- `GET /Revenue/GetHolidayAnalysis`
- `GET /Revenue/GetHolidayAnalysisBatch`
- `GET /Revenue/GetServerpartINCAnalysis`
- `GET /Revenue/GetShopINCAnalysis`
- `GET /Revenue/GetMonthlyBusinessAnalysis`
- `GET /Revenue/GetMonthlySPINCAnalysis`
- `GET /Revenue/GetTransactionDetailList`
- `GET /Revenue/GetHolidayRevenueRatio`
- `POST /Revenue/GetBusinessRevenueList`
- `POST /Revenue/GetMonthlyBusinessRevenue`
- `GET /Revenue/GetCompanyRevenueReport`
- `GET /Revenue/GetRevenueCompare`
- `GET /Revenue/GetHolidaySPRAnalysis`
- `GET /Revenue/GetHolidayDailyAnalysis`
- `GET /Revenue/GetMonthINCAnalysis`
- `GET /Revenue/GetMonthINCAnalysisSummary`
- `GET /Revenue/StorageMonthINCAnalysis`
- `GET /Revenue/GetShopSABFIList`
- `GET /Revenue/GetShopMonthSABFIList`

### 5.2 BaseInfo

文件：[base_info_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/base_info_router.py)

- `GET /BaseInfo/GetSPRegionList`
- `GET /BaseInfo/GetBusinessTradeList`
- `POST /BaseInfo/GetBusinessTradeList`
- `GET /BaseInfo/GetBrandAnalysis`
- `GET /BaseInfo/GetServerpartList`
- `GET /BaseInfo/GetServerpartInfo`
- `GET /BaseInfo/GetServerInfoTree`
- `POST /BaseInfo/GetServerpartServiceSummary`
- `POST /BaseInfo/GetBrandStructureAnalysis`

### 5.3 Contract

文件：[contract_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/contract_router.py)

- `GET /Contract/GetContractAnalysis`
- `GET /Contract/GetMerchantAccountSplit`
- `GET /Contract/GetMerchantAccountDetail`

### 5.4 Examine

文件：[examine_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/examine_router.py)

- `POST /Examine/GetEXAMINEList`
- `GET /Examine/GetEXAMINEDetail`
- `POST /Examine/GetMEETINGList`
- `GET /Examine/GetMEETINGDetail`
- `POST /Examine/GetPATROLList`
- `GET /Examine/GetPATROLDetail`
- `GET /Examine/WeChat_GetExamineList`
- `GET /Examine/WeChat_GetExamineDetail`
- `GET /Examine/WeChat_GetPatrolList`
- `GET /Examine/WeChat_GetMeetingList`
- `GET /Examine/GetPatrolAnalysis`
- `GET /Examine/GetExamineAnalysis`
- `GET /Examine/GetExamineResultList`
- `GET /Examine/GetPatrolResultList`
- `POST /Examine/GetEvaluateResList`

### 5.5 BigData

文件：[bigdata_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/bigdata_router.py)

- `GET /Revenue/GetBayonetEntryList`
- `GET /Revenue/GetBayonetSTAList`
- `GET /Revenue/GetBayonetOAList`
- `GET /Revenue/GetBayonetProvinceOAList`
- `GET /Revenue/GetSPBayonetList`
- `GET /Revenue/GetBayonetRankList`
- `GET /Revenue/GetAvgBayonetAnalysis`
- `GET /Revenue/GetProvinceAvgBayonetAnalysis`
- `GET /Revenue/GetBayonetSTAnalysis`
- `GET /BigData/GetMonthAnalysis`
- `GET /BigData/GetProvinceMonthAnalysis`
- `GET /BigData/GetBayonetWarning`
- `GET /BigData/GetHolidayBayonetWarning`
- `GET /BigData/GetBayonetGrowthAnalysis`
- `GET /BigData/GetBayonetCompare`
- `GET /BigData/GetHolidayCompare`
- `GET /BigData/GetBayonetOAAnalysis`
- `GET /BigData/GetDateAnalysis`
- `POST /BigData/GetCurBusyRank`
- `POST /BigData/GetRevenueTrendChart`
- `POST /BigData/GetEnergyRevenueInfo`
- `GET /BigData/GetBayonetOwnerAHTreeList`
- `GET /BigData/GetProvinceVehicleTreeList`
- `GET /BigData/GetProvinceVehicleDetail`

### 5.6 Customer

文件：[customer_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/customer_router.py)

- `GET /Customer/GetCustomerRatio`
- `GET /Customer/GetCustomerConsumeRatio`
- `GET /Customer/GetCustomerAgeRatio`
- `GET /Customer/GetCustomerGroupRatio`
- `GET /Customer/GetAnalysisDescList`
- `GET /Customer/GetAnalysisDescDetail`
- `GET /Customer/GetCustomerSaleRatio`

### 5.7 Analysis

文件：[analysis_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/analysis_router.py)

- `POST /Analysis/GetANALYSISINSList`
- `GET /Analysis/GetANALYSISINSDetail`
- `POST /Analysis/SolidTransactionAnalysis`
- `POST /Analysis/GetTransactionAnalysis`
- `GET /Analysis/TranslateSentence`
- `GET /Analysis/GetMapConfigByProvinceCode`
- `POST /Analysis/GetServerpartTypeAnalysis`

### 5.8 Budget

文件：[budget_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/budget_router.py)

- `POST /Budget/GetBUDGETPROJECT_AHList`
- `GET /Budget/GetBUDGETPROJECT_AHDetail`
- `GET /Budget/GetBudgetProjectDetailList`
- `GET /Budget/GetBudgetMainShow`

### 5.9 AbnormalAudit

文件：[abnormal_audit_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/abnormal_audit_router.py)

- `POST /AbnormalAudit/GetCurrentEarlyWarning`
- `POST /AbnormalAudit/GetMonthEarlyWarning`

### 5.10 BusinessProcess

文件：[business_process_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/business_process_router.py)

- `GET /BusinessProcess/GetBusinessProcessList`

### 5.11 Debug

文件：[debug_router.py](D:/Projects/Python/eshang_api/routers/commercial_api/debug_router.py)

- `GET /Debug/QuerySQL`

## 6. 首轮验收建议分工

如果多人并行推进，建议按以下任务卡切分：

| 任务卡 | 范围 | 说明 |
|--------|------|------|
| Task-01 | `Revenue` | 最大模块，单独拆出 |
| Task-02 | `BaseInfo + Contract` | 主流程基础查询 |
| Task-03 | `Examine` | 列表/明细与数据同步问题分开看 |
| Task-04 | `BigData + Analysis + Customer` | 统计和图表类集中处理 |
| Task-05 | `Budget + AbnormalAudit + BusinessProcess` | 低量接口集中验收 |

## 7. 下一步

基于这份台账，下一步应继续补以下内容：

1. 为每个接口补“样本类型”和“验收状态”列
2. 为每个模块补“依赖表”清单
3. 为每个高风险接口补“业务规则”摘要
4. 建立首轮问题单并分配到并行任务卡
