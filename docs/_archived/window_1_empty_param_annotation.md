# 窗口 1 空参失败用例标注

> 生成时间: 2026-03-10 15:45
> 关联报告: `docs/window_1_dynamic_compare_report.json`

以下 11 个用例因为**测试入参为空（null/{}）**导致失败，不属于 Python 代码 bug。

## 空参 + 旧 API 返回 404/415（5 个）

旧 C# API 路由不匹配（需要必传参数），返回 404/415；新 Python API 返回 200 + 校验信息。

| # | 接口 | 旧 HTTP | 新 HTTP | 原因 |
|---|------|---------|---------|------|
| 1 | `Merchants/GetRTCoopMerchantsList` | 404 | 200 | 空参：旧 API 路由不匹配 |
| 2 | `Merchants/GetTradeBrandMerchantsList` | 415 | 200 | 空参：旧 API 不支持无 Content-Type |
| 3 | `BusinessProject/GetCONTRACT_SYNDetail` | 404 | 200 | 空参：旧 API 路由不匹配 |
| 4 | `BusinessProject/GetCONTRACT_SYNList` | 404 | 200 | 空参：旧 API 路由不匹配 |
| 5 | `BusinessProject/GetMonthSummaryList` | 404 | 200 | 空参：旧 API 路由不匹配 |

## 空参 + 两侧都返回 200 但数据不一致（5 个）

空参下两侧都正常返回数据，但字段值、列表长度有差异。这些差异可能因空参导致查询范围不同。

| # | 接口 | 旧 HTTP | 新 HTTP | 原因 |
|---|------|---------|---------|------|
| 6 | `BusinessProject/GetAccountWarningListSummary` | 200 | 200 | 空参：统计值差异（可能是查询范围不同） |
| 7 | `BusinessProject/GetMerchantsReceivables` | 200 | 200 | 空参：旧 API 返回错误码而新 API 返回空数据 |
| 8 | `BusinessProject/GetMerchantsReceivablesList` | 200 | 200 | 空参：字段缺失差异 |
| 9 | `BusinessProject/GetMerchantsReceivablesReport` | 200 | 200 | 空参：列表长度差异（185 vs 0） |
| 10 | `ContractSyn/GetContractSynDetail` | 404 | 200 | 空参：旧 API 路由不匹配 |
| 11 | `ContractSyn/GetContractSynList` | 404 | 200 | 空参：旧 API 路由不匹配 |

## 空参 + 旧 API 返回 500（1 个）

| # | 接口 | 旧 HTTP | 新 HTTP | 原因 |
|---|------|---------|---------|------|
| 12 | `BusinessProject/GetPaymentConfirmList` | 500 | 200 | 空参：旧 API 内部异常 |

> **结论**：以上用例保留在测试集但标注为"空参导致失败"，不计入 Python 代码 bug 统计。
> 需要优先修复的是剩余 **97 个有参数但失败的用例**。
