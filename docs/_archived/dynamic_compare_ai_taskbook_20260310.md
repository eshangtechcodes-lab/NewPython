# 动态对比整改执行任务书（供其他 AI 直接执行）

## 1. 用途

这不是概览文档，而是执行任务书。

其他 AI 接手时，不要再从总报告自由发挥，直接按本文的任务包执行。

目标：

- 让其他 AI 可以直接领取任务包并修改代码
- 限制修改边界，避免多人互相覆盖
- 固定回归命令和完成定义

## 2. 必读输入

每个任务包开始前，必须先读这些文件：

- [dynamic_compare_master_report_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_master_report_20260310.md)
- [dynamic_compare_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_rectification_plan_20260310.md)
- [api-migration.md](/E:/workfile/JAVA/NewAPI/.agent/workflows/api-migration.md)
- [collaboration_plan.md](/E:/workfile/JAVA/NewAPI/docs/collaboration_plan.md)

每个窗口的精确失败清单，以 JSON 摘要为准：

- [window_1_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_1_dynamic_compare_report.json)
- [window_2_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_2_dynamic_compare_report.json)
- [window_3_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_3_dynamic_compare_report.json)
- [window_4_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_4_dynamic_compare_report.json)

## 3. 统一执行规则

所有 AI 都必须遵守：

1. 一次只领取一个任务包，不允许跨包大面积改动。
2. 只改本任务包允许修改的文件。
3. 不要改 `scripts/manifests/windows/*.json`，除非任务包明确要求。
4. 不要把所有接口继续强行统一成单一返回壳，必须以原 C# Controller/Helper 为准。
5. 修改完成后，必须跑该任务包指定的窗口回归命令。
6. 回归后，必须再执行总汇总命令。

统一回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_2.json --report docs/window_2_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_3.json --report docs/window_3_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_4.json --report docs/window_4_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

单包开发时，只跑相关窗口，不要每次全量跑 4 个窗口。

## 4. 执行顺序

任务包有依赖，不能乱序。

### 第一轮必须先做

- `PKG-RESP-CORE-01`
- `PKG-TIMEOUT-INFRA-01`

### 第二轮并行做

- `PKG-W1-BASE-CONTRACT-01`
- `PKG-W2-FINANCE-REVENUE-01`
- `PKG-W3-BATCH-MODULES-01`
- `PKG-W4-PICTURE-01`

### 第三轮再做

- `PKG-BASELINE-ISOLATE-01`

说明：

- `PKG-RESP-CORE-01` 不先完成，窗口 1/2/3 里大量 `Message/Result_Code/Result_Data` 缺失会继续污染结果。
- `PKG-TIMEOUT-INFRA-01` 不先完成，窗口 1/2 里大量超时接口无法进入字段级比对。

## 5. 任务包总览

| 任务包 | 优先级 | 目标 | 对应窗口 | 失败量级 |
| --- | --- | --- | --- | --- |
| `PKG-RESP-CORE-01` | `P0` | 修统一响应壳、错误分支、Pydantic 泄漏 | 1/2/3/4 | 至少 132 |
| `PKG-TIMEOUT-INFRA-01` | `P0` | 修新 API 超时、增加慢查询定位 | 1/2/3 | 165 |
| `PKG-W1-BASE-CONTRACT-01` | `P1` | 修 BaseInfo / Merchants / Contract 主链 | 1 | 131 |
| `PKG-W2-FINANCE-REVENUE-01` | `P1` | 修 Finance / Revenue / BigData / MobilePay | 2 | 115 |
| `PKG-W3-BATCH-MODULES-01` | `P1` | 修 Audit / Analysis / BusinessMan / Supplier / Verification / Sales | 3 | 86 |
| `PKG-W4-PICTURE-01` | `P2` | 修 Picture 当前仅剩的可执行读接口 | 4 | 1 |
| `PKG-BASELINE-ISOLATE-01` | `P2` | 隔离原 API 不稳定路由 | 汇总层 | 12 |

---

## 6. 任务包详情

### `PKG-RESP-CORE-01`

目标：

- 修掉所有“统一响应包装错误”和“Pydantic 校验异常直接泄漏”的共性问题。

高频表现：

- `<root>.Message: 新 API 缺少该字段`
- `<root>.Result_Code: 新 API 缺少该字段`
- `<root>.Result_Data: 新 API 缺少该字段`
- `validation error for JsonListData`

必须阅读：

- [models/base.py](/E:/workfile/JAVA/NewAPI/models/base.py)
- [middleware/error_handler.py](/E:/workfile/JAVA/NewAPI/middleware/error_handler.py)
- [window_1_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_1_dynamic_compare_report.json)
- [window_2_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_2_dynamic_compare_report.json)
- [window_3_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_3_dynamic_compare_report.json)

允许修改：

- [models/base.py](/E:/workfile/JAVA/NewAPI/models/base.py)
- [middleware/error_handler.py](/E:/workfile/JAVA/NewAPI/middleware/error_handler.py)
- [routers/eshang_api_main/batch_modules/batch_router_part1.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/batch_modules/batch_router_part1.py)
- [routers/eshang_api_main/batch_modules/batch_router_part2.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/batch_modules/batch_router_part2.py)
- 相关 BaseInfo / Merchants / Finance / Revenue router 中明显统一包装错误的返回分支

禁止修改：

- 业务 SQL
- manifest 生成脚本
- 对比脚本逻辑

完成定义：

- `validation error for JsonListData` 这 13 条归零
- 明显的 `Message / Result_Code / Result_Data` 缺失大幅下降
- 不再出现“把 Python 模型异常直接塞进 Result_Desc”

回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_3.json --report docs/window_3_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

---

### `PKG-TIMEOUT-INFRA-01`

目标：

- 把新 API 侧 `localhost:8080` 的 165 条超时先打散成可定位的慢查询/慢逻辑问题。

高频模块：

- Revenue
- BusinessProject
- Finance
- MobilePay
- Contract
- BigData

必须阅读：

- [core/database.py](/E:/workfile/JAVA/NewAPI/core/database.py)
- [routers/deps.py](/E:/workfile/JAVA/NewAPI/routers/deps.py)
- [window_1_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_1_dynamic_compare_report.json)
- [window_2_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_2_dynamic_compare_report.json)

允许修改：

- [core/database.py](/E:/workfile/JAVA/NewAPI/core/database.py)
- [routers/deps.py](/E:/workfile/JAVA/NewAPI/routers/deps.py)
- 各 service 中明显存在全表查 + Python 二次聚合的函数

建议优先修改文件：

- [services/business_project](/E:/workfile/JAVA/NewAPI/services/business_project)
- [services/revenue/revenue_service.py](/E:/workfile/JAVA/NewAPI/services/revenue/revenue_service.py)
- [services/finance](/E:/workfile/JAVA/NewAPI/services/finance)
- [services/contract/contract_service.py](/E:/workfile/JAVA/NewAPI/services/contract/contract_service.py)
- [services/mobilepay/mobilepay_service.py](/E:/workfile/JAVA/NewAPI/services/mobilepay/mobilepay_service.py)
- [services/bigdata/bigdata_service.py](/E:/workfile/JAVA/NewAPI/services/bigdata/bigdata_service.py)

禁止修改：

- 路由路径
- HTTP 方法
- 报告生成脚本

完成定义：

- 新 API 超时数明显下降
- 至少先把接口从“超时”拉到“有响应可比”
- 在日志中能定位慢 SQL / 慢服务函数

回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md
python scripts/compare_api.py --manifest scripts/manifests/windows/window_2.json --report docs/window_2_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

---

### `PKG-W1-BASE-CONTRACT-01`

目标：

- 修窗口 1 的失败接口。

窗口 1 当前分布：

- BaseInfo：59
- BusinessProject：48
- Contract：12
- Merchants：7
- Commodity：3
- ContractSyn：2

精确失败接口来源：

- [window_1_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_1_dynamic_compare_report.json)

允许修改：

- [routers/eshang_api_main/base_info](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/base_info)
- [services/base_info](/E:/workfile/JAVA/NewAPI/services/base_info)
- [routers/eshang_api_main/merchants/merchants_router.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/merchants/merchants_router.py)
- [services/merchants](/E:/workfile/JAVA/NewAPI/services/merchants)
- [routers/eshang_api_main/contract](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/contract)
- [services/business_project](/E:/workfile/JAVA/NewAPI/services/business_project)
- [services/contract](/E:/workfile/JAVA/NewAPI/services/contract)

重点接口：

- `BaseInfo/GetSERVERPARTList`
- `BaseInfo/GetServerpartDDL`
- `BaseInfo/GetShopShortNames`
- `BaseInfo/GetTradeBrandTree`
- `Merchants/GetCoopMerchantsList`
- `BusinessProject/GetBusinessProjectList`
- `BusinessProject/GetPaymentConfirmList`
- `Contract/GetRegisterCompactList`

依赖：

- 必须在 `PKG-RESP-CORE-01` 后执行
- 最好在 `PKG-TIMEOUT-INFRA-01` 有初步结果后执行

完成定义：

- 窗口 1 不再全部失败
- BaseInfo/Contract 至少出现首批 `PASS`

回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_1.json --report docs/window_1_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

---

### `PKG-W2-FINANCE-REVENUE-01`

目标：

- 修窗口 2 的失败接口。

窗口 2 当前分布：

- Revenue：43
- Finance：26
- BigData：15
- MobilePay：14
- Budget：11
- Invoice：4
- Customer：2

精确失败接口来源：

- [window_2_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_2_dynamic_compare_report.json)

允许修改：

- [routers/eshang_api_main/revenue](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/revenue)
- [services/revenue](/E:/workfile/JAVA/NewAPI/services/revenue)
- [routers/eshang_api_main/finance](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/finance)
- [services/finance](/E:/workfile/JAVA/NewAPI/services/finance)
- [routers/eshang_api_main/bigdata/bigdata_router.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/bigdata/bigdata_router.py)
- [services/bigdata/bigdata_service.py](/E:/workfile/JAVA/NewAPI/services/bigdata/bigdata_service.py)
- [services/mobilepay/mobilepay_service.py](/E:/workfile/JAVA/NewAPI/services/mobilepay/mobilepay_service.py)

重点接口：

- Revenue 全链：`GetPERSONSELLList`、`GetRevenueReport`、`GetMonthCompare`
- Finance 报表链：`GetProjectSummary`、`GetReconciliation`
- BigData 报表链：`GetBAYONETList`、`GetSECTIONFLOWList`
- MobilePay：全部已执行读接口

依赖：

- 必须在 `PKG-RESP-CORE-01` 后执行
- 强依赖 `PKG-TIMEOUT-INFRA-01`

完成定义：

- 窗口 2 从“超时为主”转成“字段差异为主”
- 至少出现可稳定返回的报表接口

回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_2.json --report docs/window_2_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

---

### `PKG-W3-BATCH-MODULES-01`

目标：

- 修窗口 3 的模板化问题。

窗口 3 当前分布：

- Analysis：31
- Audit：17
- Verification：11
- Merchants 前缀下的 BusinessMan 路由：10
- Supplier：7
- Sales：7
- BusinessMan：3

精确失败接口来源：

- [window_3_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_3_dynamic_compare_report.json)

注意：

- 这里很多路由前缀不等于业务模块名。
- 不要只按 URL 前缀判断归属，要以窗口 3 JSON 摘要为准。

允许修改：

- [routers/eshang_api_main/batch_modules/batch_router_part1.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/batch_modules/batch_router_part1.py)
- [routers/eshang_api_main/batch_modules/batch_router_part2.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/batch_modules/batch_router_part2.py)
- [services/audit](/E:/workfile/JAVA/NewAPI/services/audit)
- [services/analysis](/E:/workfile/JAVA/NewAPI/services/analysis)
- [services/businessman](/E:/workfile/JAVA/NewAPI/services/businessman)
- [services/verification](/E:/workfile/JAVA/NewAPI/services/verification)

重点接口：

- Analysis：全部 list/detail 链
- Audit：`GetAuditList`、`GetCHECKACCOUNTList`
- Verification：`GetEndaccountList`、`GetSuppEndaccountList`
- Sales：排行、汇总、历史链

依赖：

- 必须在 `PKG-RESP-CORE-01` 后执行

完成定义：

- 窗口 3 不再“全部失败”
- batch 模块不再依赖统一模板壳强行返回

回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_3.json --report docs/window_3_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

---

### `PKG-W4-PICTURE-01`

目标：

- 修窗口 4 当前唯一可执行读接口。

接口范围：

- `Picture/GetPictureList`

精确失败接口来源：

- [window_4_dynamic_compare_report.json](/E:/workfile/JAVA/NewAPI/docs/window_4_dynamic_compare_report.json)

允许修改：

- [routers/eshang_api_main/batch_modules/batch_router_part2.py](/E:/workfile/JAVA/NewAPI/routers/eshang_api_main/batch_modules/batch_router_part2.py)
- [services/picture/picture_service.py](/E:/workfile/JAVA/NewAPI/services/picture/picture_service.py)

依赖：

- 建议在 `PKG-RESP-CORE-01` 后执行

完成定义：

- `window_4` 变为 `PASS 1 / FAIL 0`

回归命令：

```powershell
python scripts/compare_api.py --manifest scripts/manifests/windows/window_4.json --report docs/window_4_dynamic_compare_report.md
python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
```

---

### `PKG-BASELINE-ISOLATE-01`

目标：

- 把原 API 不稳定的 12 条接口隔离出最终验收口径。

接口来源：

- 原 API 超时：8 条
- 原 API 断连 / 非 JSON：4 条

代表接口：

- `BusinessProject/GetPeriodWarningList`
- `Finance/GetAccountReached`
- `Finance/GetContractExcuteAnalysis`
- `Revenue/GetMonthINCAnalysis`
- `BigData/GetDailyBayonetAnalysis`
- `BigData/GetSECTIONFLOWMONTHDetail`
- `BigData/GetSECTIONFLOWMONTHList`
- `BigData/GetServerpartSectionFlow`
- `BigData/GetUreaMasterList`

允许修改：

- [dynamic_compare_master_report_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_master_report_20260310.md)
- [dynamic_compare_rectification_plan_20260310.md](/E:/workfile/JAVA/NewAPI/docs/dynamic_compare_rectification_plan_20260310.md)
- 如确有需要，可新增一份基线隔离清单文档到 `docs/`

禁止修改：

- Python 业务代码

完成定义：

- 这 12 条不再被当作 Python 真问题统计
- 总汇总中能区分“Python 失败”和“旧基线失败”

---

## 7. 可直接复制给其他 AI 的任务提示模板

```text
你现在领取的任务包是：<TASK_ID>

执行规则：
1. 只修改该任务包允许修改的文件。
2. 先阅读 docs/dynamic_compare_ai_taskbook_20260310.md 中对应任务包。
3. 以对应 window_X_dynamic_compare_report.json 为精确失败接口清单。
4. 修改后只跑该任务包要求的回归命令。
5. 最后执行 python scripts/summarize_compare_reports.py --output docs/dynamic_compare_master_report_20260310.md
6. 不要顺手改别的模块。
```

## 8. 当前推荐分配

推荐并行分配：

- AI-1：`PKG-RESP-CORE-01`
- AI-2：`PKG-TIMEOUT-INFRA-01`
- AI-3：`PKG-W1-BASE-CONTRACT-01`
- AI-4：`PKG-W2-FINANCE-REVENUE-01`
- AI-5：`PKG-W3-BATCH-MODULES-01`
- AI-6：`PKG-W4-PICTURE-01`

其中：

- `AI-3/4/5/6` 开始前必须先确认 `AI-1` 的公共响应层修改已经合入或至少明确方案。
