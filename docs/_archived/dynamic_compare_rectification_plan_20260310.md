# 动态对比整改方案（2026-03-10）

## 1. 输入依据

本方案基于以下动态联调结果：

- `docs/dynamic_compare_master_report_20260310.md`
- `docs/window_1_dynamic_compare_report.md`
- `docs/window_2_dynamic_compare_report.md`
- `docs/window_3_dynamic_compare_report.md`
- `docs/window_4_dynamic_compare_report.md`

本轮动态联调结论：

- 总用例数：`333`
- 通过：`0`
- 失败：`333`
- 跳过：`0`

窗口结果：

| 窗口 | FAIL | 说明 |
| --- | --- | --- |
| `window_1` | 131 | BaseInfo / Merchants / Contract 主链问题最集中 |
| `window_2` | 115 | Finance / Revenue / BigData / MobilePay 大量超时 |
| `window_3` | 86 | Analysis / Audit / Verification 等模板化问题明显 |
| `window_4` | 1 | Picture 仅剩 1 条可执行读接口，仍失败 |

## 2. 失败类型归类

按失败首因聚类后，可收口为 5 类问题：

### `P0-A` 新 API 超时 / 性能阻塞

- 数量：`165`
- 占比：约 `49.5%`
- 典型表现：`HTTPConnectionPool(host='localhost', port=8080): Read timed out`
- 主要集中模块：
  - Revenue
  - BusinessProject
  - Finance
  - MobilePay
  - Contract
  - BigData

判断：

- 当前首先不是“字段差一点”，而是大量接口在新 API 侧根本没有在 20 秒内返回。
- 这一类不先清掉，后续契约比对没有意义。

### `P0-B` 响应包装漂移 / 错误分支包装错误

明确统计到的高频项：

- `<root>.Message: 新 API 缺少该字段`：`100`
- `<root>.Result_Code: 新 API 缺少该字段`：`16`
- `<root>.Result_Data: 新 API 缺少该字段`：`3`
- Pydantic 校验错误直接泄漏到 `Result_Desc`：`13`

合计至少：`132`

判断：

- 当前仓库把不少接口强行包装成统一 `Result.success(...)` 风格，但原 C# 并不是所有模块都共享同一返回壳。
- 另外，空参 / 异常分支触发了 `JsonListData` 的模型校验异常，错误信息直接暴露到外层响应里。

### `P1-A` 业务状态码 / 错误文案不一致

- `Result_Code` 不一致：至少 `12`
- `Result_Desc` 不一致：高频分布在 BaseInfo / BusinessProject

判断：

- 这类通常不是单纯包装问题，而是参数处理、SQL 条件、空参行为、异常分支与原 C# 不一致。

### `P1-B` 字段契约 / 数据映射差异

典型表现：

- 字段缺失
- 字段类型不一致
- 列表长度不一致
- 树结构 / children / desc / StaticsModel 等字段不一致
- 示例：
  - `GetCombineBrandList` 缺 `BRAND_TYPENAME`
  - `GetServerpartDDL` 缺 `Result_Data`
  - `GetShopShortNames` 列表长度不一致
  - `GetTradeBrandTree` 子节点类型不一致

判断：

- 这类是 Helper 语义没有完整回迁，或 Python 模型把 `None`/空串/空数组处理错了。

### `P2` 原 API 基线不稳定

- 原 API 超时：`8`
- 原 API 断连 / 非 JSON / 网络异常：`4`

判断：

- 这 12 条不能直接归咎于 Python。
- 应先列入“基线隔离清单”，修 Python 时不拿它们做最终验收口径。

## 3. 整改优先级

必须按下面顺序推进，不能反过来：

1. 先清 `P0-A` 新 API 超时
2. 再清 `P0-B` 响应包装和错误分支
3. 再修 `P1-A/P1-B` 的模块逻辑和字段契约
4. 最后隔离并复测 `P2` 原 API 不稳定接口

原因：

- 只要新 API 还大量超时，其他差异都是噪音。
- 只要响应壳不对，动态脚本会把大量接口全部打成 fail，没法看清深层业务差异。

## 4. 整改批次

### 批次 0：联调口径止血

目标：

- 把当前 333 条失败先分成“Python 真问题”和“原 API 基线问题”

动作：

- 建立原 API 隔离清单，先标记这 12 条：
  - `BusinessProject/GetPeriodWarningList`
  - `Finance/GetAccountReached`
  - `Finance/GetContractExcuteAnalysis`
  - `Revenue/GetMonthINCAnalysis`
  - `BigData/GetDailyBayonetAnalysis`
  - `BigData/GetSECTIONFLOWMONTHDetail`
  - `BigData/GetSECTIONFLOWMONTHList`
  - `BigData/GetServerpartSectionFlow`
  - `BigData/GetUreaMasterList`
  - 以及汇总报告中其余原 API 超时 / 非 JSON 路由
- 这些接口暂时不作为“Python 一致性失败”统计口径。

输出：

- `docs/dynamic_compare_master_report_20260310.md` 旁补一份“基线隔离清单”

### 批次 1：公共层整改

目标：

- 先解决最通用、影响最广的包装和异常问题

建议改动文件：

- `models/base.py`
- `middleware/error_handler.py`
- `routers/eshang_api_main/batch_modules/batch_router_part1.py`
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- 相关返回壳固定化的 router 文件

动作：

1. `JsonListData` 的 `StaticsModel` 改成可空且不触发 Pydantic 校验异常。
2. 所有错误分支不得把模型校验异常原文直接暴露到 `Result_Desc`。
3. 不再把所有模块强行套同一种返回壳。
4. 恢复“按原 Controller 的返回结构”返回：
   - `Result_Code / Result_Desc / Result_Data`
   - 或原接口真实存在的 `Message` / `data` / 其他结构
5. 全局异常处理中间件只保底，不覆盖原接口应有的业务错误壳。

完成标准：

- `wrapper_message_missing + wrapper_result_code_missing + wrapper_result_data_missing + pydantic_error_leak` 清零

### 批次 2：新 API 超时整改

目标：

- 把 165 条新 API 超时先压到可对比状态

优先模块：

1. Revenue
2. BusinessProject
3. Finance
4. MobilePay
5. Contract
6. BigData

建议改动文件：

- `core/database.py`
- `routers/deps.py`
- `services/revenue/revenue_service.py`
- `services/business_project/*.py`
- `services/finance/*.py`
- `services/contract/contract_service.py`
- `services/mobilepay/mobilepay_service.py`
- `services/bigdata/bigdata_service.py`

动作：

1. 先在 `DatabaseHelper` 增加 SQL 耗时日志、慢查询日志、必要的执行超时控制。
2. 检查是否存在每次请求重复建连、重复查全表、Python 层二次聚合导致的阻塞。
3. 重报表接口优先分三类处理：
   - 能直接补分页 / where 条件的先补
   - SQL 明显不等价的，直接回迁 C# Helper 逻辑
   - 依赖多表汇总的，单独拆 service，不再复用通用 CRUD
4. 对 `BusinessProject` / `Revenue` / `Finance` 的 detail/list/report 接口逐条记录超时根因。

完成标准：

- 新 API 超时从 `165` 降到 `0`
- 先达到“接口能返回”，再进入字段级比对

### 批次 3：BaseInfo / Merchants / Commodity 契约修复

目标：

- 修掉最集中的非超时型差异

重点问题：

- `ProvinceCode` / Header / body 参数处理错位
- 空参行为不一致
- 扁平 body 与 `SearchParameter` 两种入参兼容性不一致
- 树结构字段缺失
- `None` / `""` / `[]` 的语义不一致

建议改动文件：

- `routers/eshang_api_main/base_info/*.py`
- `services/base_info/*.py`
- `routers/eshang_api_main/merchants/merchants_router.py`
- `services/merchants/*.py`
- `services/base_info/commodity_service.py`

首先处理的接口：

- `BaseInfo/GetSERVERPARTList`
- `BaseInfo/GetServerpartDDL`
- `BaseInfo/GetShopShortNames`
- `BaseInfo/GetTradeBrandTree`
- `BaseInfo/GetServerpartShopTree`
- `Merchants/GetCoopMerchantsList`
- `Merchants/GetTradeBrandMerchantsList`

完成标准：

- BaseInfo / Merchants / Commodity 模块先出现第一批 `PASS`

### 批次 4：Batch 模块模板化整改

目标：

- 清除 Audit / Analysis / BusinessMan / Supplier / Verification / Sales 的模板化问题

判断依据：

- 当前 `batch_router_part2.py` 明确采用“统一 Result 标准格式”思路，这与动态结果明显冲突。
- 这批模块不能再用“通用 CRUD + 统一壳”继续修补，必须按原 C# Controller/Helper 拆回真实契约。

建议改动文件：

- `routers/eshang_api_main/batch_modules/batch_router_part1.py`
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- `services/analysis/analysis_service.py`
- `services/businessman/businessman_service.py`
- `services/verification/verification_service.py`
- `services/audit/audit_service.py`

动作：

1. 优先恢复接口真实返回结构。
2. 再恢复 detail/list 的参数名和 Query / Body 形态。
3. 最后处理树、汇总、`OtherData`、状态机。

完成标准：

- `window_3` 不再全红

### 批次 5：Finance / Revenue / BusinessProject 深逻辑整改

目标：

- 在超时清零后，继续修真正的业务差异

重点链路：

- Revenue 报表 / 对账 / 分析
- BusinessProject 应收 / 预警 / 拆分 / 回款
- Finance 报表 / 对账 / 汇总

建议改动文件：

- `services/revenue/revenue_service.py`
- `services/business_project/*.py`
- `services/finance/finance_scattered_service.py`
- `services/finance/budget_service.py`
- `services/finance/invoice_service.py`

动作：

1. 逐条对照原 C# Helper 的 SQL、默认排序、默认分页。
2. 把 `return []`、`return True`、简化汇总壳接口全部替换成真实逻辑。
3. 对报表类接口增加“默认参数 + 常规参数 + 边界参数”三组专用 case。

完成标准：

- `window_2` 从“超时主导”转成“少量字段差异”

## 5. 建议排期

### 第一天

- 批次 0
- 批次 1
- 批次 2 的慢查询定位

### 第二天到第三天

- 批次 2 真正修复
- 批次 3 BaseInfo / Merchants / Commodity 修复

### 第四天到第六天

- 批次 4 Batch 模块拆模板
- 批次 5 Finance / Revenue / BusinessProject 深逻辑回迁

### 每天结束前固定动作

1. 重新跑对应窗口 manifest
2. 执行总汇总：
   - `python scripts/summarize_compare_reports.py`
3. 更新：
   - `docs/dynamic_compare_master_report_20260310.md`
   - `docs/dynamic_test_issue_log_20260309.md`

## 6. 完成定义

本轮整改完成标准不是“代码改了”，而是：

1. 新 API 超时归零
2. 响应包装漂移归零
3. Pydantic 错误泄漏归零
4. 原 API 不稳定路由已隔离
5. 重新跑 4 个窗口后，总汇总出现实质性 `PASS`

## 7. 建议的第一批实做清单

按收益排序，建议先改下面这批：

1. `models/base.py`
2. `middleware/error_handler.py`
3. `core/database.py`
4. `services/business_project/*.py`
5. `services/revenue/revenue_service.py`
6. `services/finance/*.py`
7. `routers/eshang_api_main/batch_modules/batch_router_part2.py`
8. `routers/eshang_api_main/base_info/*.py`

不建议直接从长尾字段差异开始补。

先把“超时”和“统一包装错误”这两件事清掉，才能看见真正剩余的业务差异。
