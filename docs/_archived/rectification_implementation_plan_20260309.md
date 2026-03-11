# 接口迁移整改 — 综合修改方案与实施计划

> 基于 6 份 Codex 审计文档的代码级验证结果
> 生成时间：2026-03-09
> 最后修订：2026-03-09（采纳 Codex review 意见）

**文档主从关系说明**：
- 接口级事实依据，以 `full_audit_rectification_matrix_20260309.md` 为准
- 执行批次和验收规则，以 `full_audit_execution_plan_20260309.md` 为准
- 本文只负责整合、排序和派工口径，不覆盖上游事实文档

---

## 一、文档来源与验证结论

### 输入文档

| # | 文档 | 内容 |
|---|------|------|
| 1 | `full_audit_master_report_20260309.md` | Codex 全量审计总报告 |
| 2 | `full_audit_rectification_matrix_20260309.md` | 40+ 个整改包的接口级台账 |
| 3 | `full_audit_execution_plan_20260309.md` | B1-B5 五批执行方案 |
| 4 | `interface_migration_knowledge_base_20260309.md` | 迁移知识库（7类反模式、10项checklist） |
| 5 | `codex_audit_review_20260309.md` | Antigravity 对 Codex 第一轮审查 |
| 6 | `codex_audit_review_response_20260309.md` | Codex 对审查意见的响应和修正 |

### 验证总结

经逐项代码验证，**Codex 的核心发现大部分属实**，已知修正项已被 Codex 在 response 文档中接受。以下为最终定论：

| 条目 | Codex 原判 | 验证结论 | 最终定论 |
|------|-----------|----------|----------|
| Verification 状态机简化 | 极高风险 | **完全属实** — 14个占位/简化 | ✅ 按 Codex 方案执行 |
| Finance 散装占位 | 极高风险 | **完全属实** — 22处占位 | ✅ 按 Codex 方案执行 |
| Sales 接口复用 | 高风险 | **完全属实** — 6个复用同一查询 | ✅ 按 Codex 方案执行 |
| Audit 报表占位 | 高风险 | **大部分属实** — 2个return[]、4个错误复用 | ✅ 分层处置 |
| BusinessMan 表映射 | 高风险 | **属实** — C#用OWNERUNIT，Python用T_BUSINESSMAN | ✅ 按 Codex 方案执行 |
| BusinessMan 散装简化 | 高风险 | **属实** — relate_business_commodity等5个占位/简化 | ✅ 按 Codex 方案执行 |
| Picture 路由偏离 | 极高风险 | **属实** | ✅ 按 Codex 方案执行 |
| Video 全部缺失 | P0 | **属实** | ✅ 按 Codex 方案执行 |
| 响应格式漂移 | P0 | **属实** — ~206个接口 | ✅ 按 Codex 方案执行 |
| pk_val 泛化参数 | P0 | **属实** — ~40个接口（Analysis+BusinessMan） | ✅ 按 Codex 方案执行 |
| Revenue generic CRUD | 全部重做 | **半属实** — CRUD通用但散装有2800行逻辑 | ⚠️ 改为契约复核 |
| Audit pk_val 问题 | 壳化 | **不属实** — 已用正确参数名 | ❌ 已被Codex接受修正 |
| RE-02 params运行时错误 | 存在 | **已确认存在**（第227/259行 `params` 未定义） | ✅ 需先修再深比对 |

---

## 二、P0 紧急清单（按风险排序）

### 🔴 第一梯队 — 占位实现（接口存在但无逻辑，直接导致业务失效）

| # | 模块 | 占位数 | 关键接口 | 整改包ID |
|---|------|--------|----------|----------|
| 1 | **Verification** | 14个 | verify/approve/cancel_endaccount, save_correct_data, rebuild_daily_account 等 | VE-01~04 |
| 2 | **Finance** | 22+个 | 审批流、固化、重算、短信、提单 | FI-01~04 |
| 3 | **Sales** | 6个 | get_commodity_sale_summary, sale_rank 等全复用同一查询 | SA-01~02 |
| 4 | **Audit** | 4个 | get_special_behavior_report, get_abnormal_rate_report (return[]), issue_audit_tasks 等 | AU-02 |
| 5 | **BusinessMan/Supplier** | 4个 | relate_business_commodity(return True), get_user_list查错表 | BS-03, SU-02 |

### 🟡 第二梯队 — 契约不兼容（能返回数据但格式/参数不兼容）

| # | 问题 | 影响面 | 整改包ID |
|---|------|--------|----------|
| 6 | 响应格式恢复为与 C# 一致的响应壳 | ~206个接口（batch_router_part1 41 + part2 155 + bigdata ~10） | AN-01, AU-01, BG-01 等 |
| 7 | 恢复原实体专属参数名和参数形态 | ~40个接口（Analysis 11组 + BusinessMan 8组） | AN-01, BS-02 |
| 8 | BusinessMan 表映射漂移 | 12个接口 | BS-01 |
| 9 | Header/Token 注入缺失 | 多模块 | BM-01 |

### 🟢 第三梯队 — 路由缺失

| # | 模块 | 缺失数 | 整改包ID |
|---|------|--------|----------|
| 10 | Video 全模块 | 16个 | VI-01~05 |
| 11 | Picture 原路由 | 6个 | PI-02 |
| 12 | Analysis SPCONTRIBUTION | 4个 | AN-03 |
| 13 | BigData BAYONETWARNING | 3个 | BG-03 |
| 14 | Finance Invoice/Office | 12个 | FI-05 |

---

## 三、修改方案

### 方案 A：公共契约层止血（对应 B1）

**目标**：恢复原 C# 响应壳和参数契约，阻止不兼容格式继续扩散

**修改内容**：
1. **恢复原响应壳**（按模块拆分执行）：
   - `batch_router_part1.py`（Audit 24 + MobilePay 17 = 41个）→ 恢复与 C# 一致的响应包结构
   - `batch_router_part2.py`（Analysis 58 + BusinessMan 39 + Verification 36 + Sales 13 + Picture 9 = 155个）→ 同上
   - `bigdata_router.py` 散装接口（~10个）→ 同上
   
2. **恢复原参数名和参数形态**：`batch_router_part2.py` 中 Analysis 11组 + BusinessMan 8组动态 CRUD
   - 目标：参数名与 C# 原接口一致，具体实现方式在执行时根据上下文决定

3. **Audit CRUD 契约修复**（AU-01 — 修正版）：
   - 仅修响应格式和输入模型（不涉及 pk_val，Audit 已使用正确参数名）

4. **Revenue CRUD 契约复核 + 运行时错误修复**（RE-01 降级版 + RE-02 前置修复）：
   - 先修 `revenue_service.py` 第 227/259 行 `params` 未定义的运行时错误
   - 逐实体核对表名/主键/状态字段/返回包
   - 仅对不等价的拆出独立 helper

5. **Contract 契约透传修复**（CT-03）：
   - 恢复 `GetFromRedis` 参数透传、默认值、缓存/实时双路径
   - 本质是契约和透传问题，归入 B1 而非 B3

6. **多出路由处置**（三步走）：
   - 第一步：从迁移验收口径剔除（`Supplier/DeleteQUALIFICATION_HIS`、Picture 多出 6 条）
   - 第二步：确认是否有调用方
   - 第三步：根据调用面决定隔离、保留还是删除

**涉及文件**：
- `routers/eshang_api_main/batch_modules/batch_router_part1.py`
- `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- `routers/eshang_api_main/bigdata/bigdata_router.py`
- `routers/eshang_api_main/revenue/revenue_router.py`
- `services/revenue/revenue_service.py`

---

### 方案 B：P0 占位清理（对应 B2）

**目标**：消除"接口在但无逻辑"的高风险

**修改内容**：
1. **Verification 状态机回迁**（VE-01~VE-04）：
   - 修复表映射（`T_ENDACCOUNT_DAILY` → `T_ENDACCOUNT`）
   - 恢复 verify/approve/cancel/submit 状态机逻辑（批量、校验、错误返回）
   - 补齐 7 个 `return []` / `return True` 占位接口

2. **Finance 占位清理**（FI-03/FI-04）：
   - 审批流 → 恢复状态流转、批量审核
   - 固化/重算 → 恢复真实计算逻辑
   - 短信/提单 → 恢复外部调用或标注为待联调

3. **Sales 接口分离**（SA-01/SA-02）：
   - 将 6 个复用同一查询的接口拆为独立实现
   - 修复 DeleteCOMMODITYSALE 删除语义（C# 原逻辑不可删）

4. **Audit 流程补全**（AU-02 — 分层版）：
   - 先补 2 个纯占位（GetSpecialBehaviorReport, GetAbnormalRateReport）
   - 再修 4 个错误复用（恢复原 helper 语义）
   - 最后微调 4 个已有 SQL 的接口

5. **BusinessMan/Supplier 占位补全**（BS-03, SU-02）：
   - `relate_business_commodity` → 恢复关联写入和历史
   - `get_user_list` → 修正查询目标表
   - `authorize_qualification` → 恢复授权逻辑

6. **Contract 主链**（CT-01/CT-02）：
   - 恢复 Token/用户上下文、删除校验、历史备份
   - 附件接口接入文件存储

7. **MobilePay 外部链路**（MP-01/MP-02）：
   - 恢复 `MobilePayHelper` / `ChinaUmsSubHelper` 语义
   - 提现/分润报表补真实逻辑

8. **Picture 语义修正**（PI-01）：
   - 按 C# 原 PictureController 重建（文件系统、凭证、HWS）

**涉及文件**：
- `services/verification/verification_service.py`
- `services/finance/finance_scattered_service.py`
- `services/audit/audit_service.py`
- `services/businessman/businessman_service.py`
- `services/picture/picture_service.py`
- `services/mobilepay/mobilepay_service.py`
- `services/contract/contract_service.py`
- 对应 router 文件

---

### 方案 C：helper 级深逻辑回迁（对应 B3）

**目标**：修复"有数据但语义不对"的问题

1. **Revenue 报表深比对**（RE-02）：按销售明细/收入报表/对账/分析四链核对
2. **BusinessMan 表映射修正**（BS-01）：先修 OWNERUNIT/OWNERUNITDETAIL/COMMODITY_BUSINESS 表映射
3. **Analysis 树/固化/报表**（AN-02）：分四链回迁
4. **Supplier 树/资质**（SU-01）：分三段回迁
5. **Contract BusinessProject**（CT-04）：恢复 summaryObject、审批状态
6. **Finance 散装汇总**（FI-02）：按 helper 重新拆 service
7. **BigData 报表**（BG-02）：逐条回迁

---

### 方案 D：缺失路由补齐（对应 B4）

1. **Video 全量 16 条**（VI-01~05）：分 5 批
2. **Picture 原路由 6 条**（PI-02）
3. **Analysis SPCONTRIBUTION 4 条**（AN-03）
4. **BigData BAYONETWARNING 3 条**（BG-03）
5. **Finance Invoice/Office 12 条**（FI-05）
6. **Contract 缺失 2 条**（CT-05）
7. **Merchants 缺失 1 条**（BM-03）

---

## 四、实施计划

### 阶段 0：前置准备（1-2 天）

| 任务 | 输出物 | 说明 |
|------|--------|------|
| P0-01 重建运行时基线 | 新版 baseline JSON + 路由差异表 | 消除统计漂移 |
| P0-02 对比脚本升级 | 升级后的 `compare_api.py` | 支持 GET/POST、Header、3组参数、字段级diff |
| P0-03 迁移脚本护栏 | 受控版 `server_migrate.py` | 默认禁止无参全量、必须带表名或 `--all` |

### 阶段 1：B1 契约层止血（3-5 天，4 窗口并行估算；单窗口执行工期至少翻倍）

按固定窗口归属推进（后续阶段均遵循此窗口分配）：

| 窗口 | 固定模块 | 本阶段整改包 | 重点 |
|------|---------|-------------|------|
| W1 | BaseInfo/Merchants/Contract | BM-01, CT-03 | Header 注入、HTTP 方法、GetFromRedis 透传 |
| W2 | Finance/Revenue/BigData/MobilePay | RE-01(降级版), RE-02(前置修复), RE-03, BG-01 | CRUD 契约复核、params 运行时错误修复 |
| W3 | Audit/Analysis/BusinessMan/Supplier/Verification/Sales | AU-01, AN-01, BS-02, SU-03 | 响应格式、恢复原参数名 |
| W4 | Picture/Video/Tooling | PI-03 | 多出路由处置 |

**完成标准**：
- 清除所有 C1（契约错误）和 C5（多出路由）状态
- 契约进入可联调、可深比对状态
- 注意：达到此标准 ≠ 整改完成，仅代表契约层不再阻塞后续工作

### 阶段 2：B2 P0 占位清理（5-8 天，4 窗口并行估算）

| 窗口 | 本阶段整改包 | 重点 |
|------|-------------|------|
| W1 | CT-01, CT-02 | Contract 主链回迁、附件接入 |
| W2 | FI-01, FI-03, FI-04, MP-01, MP-02 | 审批流、固化、外部支付占位清理 |
| W3 | VE-01~04, SA-01, AU-02, BS-03, SU-02 | 状态机、表映射、删除语义、流程补全 |
| W4 | PI-01 | Picture 语义修正 |

**完成标准**：不允许任何 `return []` / `return True` / `return {}` 占位标记为已完成

### 阶段 3：B3 深逻辑回迁（5-8 天，4 窗口并行估算）

| 窗口 | 本阶段整改包 | 重点 |
|------|-------------|------|
| W1 | CT-04, BM-02 | BusinessProject 汇总/审批、Commodity/PropertyAssets |
| W2 | RE-02, FI-02, BG-02 | 报表/对账/分析深比对 |
| W3 | AN-02, BS-01, SU-01, SA-02 | 树/资质/表映射/汇总 |

**完成标准**：`OtherData`、树结构、审批状态、动态计算与 C# 一致

### 阶段 4：B4 缺失路由补齐（3-5 天，4 窗口并行估算）

| 窗口 | 本阶段整改包 | 数量 |
|------|-------------|------|
| W1 | CT-05, BM-03 | 3条 |
| W2 | FI-05, BG-03, MP-03 | 16条 |
| W3 | AN-03 | 4条 |
| W4 | VI-01~05, PI-02 | 22条 |

**完成标准**：
- 原 C# 路由集合在 Python 运行时完整可见
- 每条补齐的路由至少通过基本 smoke 测试
- 每条补齐的路由完成 3 组参数新旧对比

### 阶段 5：B5 动态验收（持续）

- 每个整改包完成后立即进行 3 组参数新旧对比
- 重点覆盖：Header、空参、边界日期、删除操作、状态机分支
- 输出：每模块对比报告

---

## 五、每个整改包的执行 SOP

严格遵循现有迁移 SOP 6 步：

1. **读 C# 源码** — Controller + Helper + Model，记录路由/方法/参数/Header/SQL
2. **调原 API 记录基准** — 至少 3 组参数，记录 Result_Code、TotalCount、字段全集
3. **同步数据表** — 仅迁本包用到的表，禁止无参全量
4. **修改 Python 代码** — router + service + model，修完后启动验证
5. **3 组参数对比** — 空参/常规/边界，逐项检查 10 项 checklist
6. **更新文档** — 整改矩阵状态、工作日志、知识库

---

## 六、迁移状态分级

后续所有接口按 L0-L4 打标：

| 级别 | 含义 | 判定标准 |
|------|------|----------|
| L0 | 未迁移 | Python 无此路由 |
| L1 | 路由已注册 | 路由在但逻辑为占位/通用CRUD |
| L2 | 契约兼容 | 参数名、响应格式、HTTP方法与 C# 一致 |
| L3 | 逻辑等价 | SQL、分页、排序、副作用与 C# helper 一致 |
| L4 | 动态验收通过 | 3 组参数新旧对比全部通过 |

**当前大量接口停留在 L1，不应标记为"已完成"。**

---

## 七、工作量估算

> 以下工期基于 **4 窗口并行** 估算。若实际仅 1-2 个窗口，工期至少翻倍。

| 阶段 | 整改包数 | 接口数 | 预估天数（4窗口） | 预估天数（单窗口） | 说明 |
|------|---------|--------|-------------------|-------------------|------|
| 阶段 0 | 3 | — | 1-2 天 | 1-2 天 | 工具和基线 |
| 阶段 1 (B1) | 10 | ~250 | 3-5 天 | 8-12 天 | 批量替换 + CT-03 透传 |
| 阶段 2 (B2) | 16 | ~60 | 5-8 天 | 15-25 天 | 需要逐接口回迁逻辑 |
| 阶段 3 (B3) | 9 | ~80 | 5-8 天 | 12-20 天 | 需要深比对 C# helper |
| 阶段 4 (B4) | 12 | ~45 | 3-5 天 | 8-12 天 | 新接口实现 |
| 阶段 5 (B5) | — | 全量 | 持续 | 持续 | 伴随各阶段 |
| **合计** | **~50** | **~435** | **17-28 天** | **44-71 天** | |

---

## 八、配套文件

| 文件 | 用途 | 更新频率 |
|------|------|----------|
| `docs/rectification_progress.md` | 整改进度跟踪 | 每完成一个整改包即更新 |
| `docs/interface_knowledge.md` | 接口级知识沉淀 | 每完成一个模块同步更新 |
