# Codex 整改矩阵 + 执行计划 — 审查结果

> 审查时间：2026-03-09 13:30
> 审查对象：`full_audit_rectification_matrix_20260309.md` + `full_audit_execution_plan_20260309.md`

---

## 一、总体判断

Codex 这两份文档**比上一份审计报告更加深入和具体**，列出了 40+ 个整改包、5 个批次、明确的验收标准。**大部分核心发现属实**，尤其是 Verification / Finance / Audit / Sales 模块的占位实现问题。

但在以下方面存在**偏差或过度推论**，需要修正后才能作为实施依据。

---

## 二、属实的问题（代码证据确凿）

### ✅ VE-02/03/04: Verification 日结状态机 + 占位 — **完全属实，极高风险**

实际代码证据（`verification_service.py`）：

| 函数 | 实际实现 | 问题 |
|------|----------|------|
| `verify_endaccount` | 仅执行 `UPDATE SET AUDIT_STATE = 1` | 无批量、无校验、无错误返回 |
| `approve_endaccount` | 仅执行 `UPDATE SET APPROVE_STATE = 1` | 同上 |
| `cancel_endaccount` | 直接调用 `apply_endaccount_invalid` | 两个不同业务动作复用同一实现 |
| `submit_endaccount_state` | 直接调用 `synchro_endaccount` | 无状态流转逻辑 |
| `get_supp_endaccount_list` | `return []` | 占位 |
| `get_data_verification_list` | `return []` | 占位 |
| `get_commodity_sale_list_v` | `return []` | 占位 |
| `get_mobilepay_data_list` | `return []` | 占位 |
| `get_endaccount_supplement` | `return {}` | 占位 |
| `save_correct_data` | `return True, ""` | 占位 |
| `save_sale_supplement` | `return True, ""` | 占位 |
| `exception_handling` | `return True, ""` | 占位 |
| `rebuild_daily_account` | `return {"status": "ok"}` | 占位 |
| `correct_daily_endaccount` | `return {"status": "ok"}` | 占位 |

此外，**表名确实漂移**：所有 ENDACCOUNT 接口操作的是 `T_ENDACCOUNT_DAILY` 而非 `T_ENDACCOUNT`。

**结论**：Codex 对 VE-01 到 VE-04 的判断**完全属实**。这是全项目最高风险模块。

---

### ✅ SA-01/02: Sales 接口复用同一查询 — **完全属实**

`verification_service.py` 中 Sales 散装接口：

| 函数名 | 实际实现 | 应有逻辑 |
|--------|----------|----------|
| `get_endaccount_sale_info` | `_crud(T_COMMODITYSALE)` | 账期快照查询 |
| `get_endaccount_error` | `_crud(T_COMMODITYSALE)` ← 同上 | 异常数据查询 |
| `get_commodity_sale_summary` | `_crud(T_COMMODITYSALE)` ← 同上 | 销售汇总 |
| `get_commodity_type_summary` | `_crud(T_COMMODITYSALE)` ← 同上 | 类别汇总 |
| `get_commodity_type_history` | `_crud(T_COMMODITYSALE)` ← 同上 | 历史趋势 |
| `record_sale_data` | `_synchro(T_COMMODITYSALE)` | 记录操作 |

6 个不同业务含义的接口全部复用同一个简单分页查询。**完全属实**。

---

### ✅ AU-02: Audit 报表/流程占位 — **大部分属实**

| 函数 | 实际实现 | 问题 |
|------|----------|------|
| `get_special_behavior_report` | `return []` | 纯占位 |
| `get_abnormal_rate_report` | `return []` | 纯占位 |
| `get_audit_details` | 调用 `get_entity_list("AUDITTASKS")` | 复用通用 CRUD |
| `upload_audit_explain` | 调用 `synchro_entity("ABNORMALAUDIT")` | 没有上传逻辑 |
| `issue_audit_tasks` | 调用 `synchro_entity("AUDITTASKS")` | 没有下发逻辑 |
| `get_audit_tasks_detail_list` | 调用 `get_entity_list("AUDITTASKS")` | 复用通用 CRUD |

但 `get_audit_list` 和 `get_check_account_report` **有实际 SQL 逻辑**（JOIN 查询），不是纯占位。

---

### ✅ FI-03/04: Finance 散装接口大量占位 — **完全属实**

`finance_scattered_service.py` 中发现 **22 处** `return []` / `return True, ""` 占位，涵盖审批流、固化、补录、重算、短信、提单等核心接口。**完全属实**。

---

### ✅ BS-03 / SU-02: BusinessMan 散装逻辑简化 — **属实**

| 函数 | 实际实现 | 问题 |
|------|----------|------|
| `relate_business_commodity` | `return True, ""` | 纯占位 |
| `create_businessman` | `_synchro("T_BUSINESSMAN")` | 只是通用 upsert |
| `get_user_list` | `_crud("T_BUSINESSMAN")` | 查的是商户表而非用户表 |
| `authorize_qualification` | `_synchro("T_QUALIFICATION")` | 只是通用 upsert |
| `get_nesting_custom_type_list` | 平铺查询 `T_CUSTOMTYPE` | 无嵌套/树结构 |
| `get_supplier_tree_list` | `get_entity_list("SUPPLIER")` | 无树结构 |

---

### ✅ PI-01/02/03: Picture 路由偏离 — **属实**（上一轮已确认）

### ✅ VI-01~05: Video 全部缺失 — **属实**（上一轮已确认）

---

## 三、需要辨析 / 修正的问题

### ⚠️ RE-01: Revenue "7 组实体被 generic CRUD 取代" — **半属实**

Codex 说 Revenue 需要"废除当前 generic CRUD 映射，按实体逐组恢复"——但实际情况需要辨析：

- **CRUD 部分确实用了通用模板**（`ENTITIES` 字典 + `_generic_list/detail/synchro/delete`） → **属实**
- **但散装报表有 2800+ 行实际业务代码**，含 `get_revenue_report`（148 行树形聚合）、`get_revenue_report_by_date`（131 行）、`bank_account_compare`、`get_his_commodity_sale_list` 等 → **不是空实现**

C# 原 CRUD 部分本身也是模板化的（每个 Helper 的 `GetList/GetDetail/Synchro/Delete` 都是标准 CRUD 四件套）。如果 Python 的通用 CRUD SQL 查的是正确的表、正确的主键、正确的状态字段，且 Router 层参数名正确，则 CRUD 部分**实质上是等价的**。

**建议修正**：
- RE-01 应改为"检查 CRUD 参数名和响应格式是否兼容"，而非"全部重做"
- RE-02 中的散装报表才是需要逐条核对的重点

---

### ⚠️ AU-01: Audit "被 pk_val 壳化" — **不属实**

之前已验证：`batch_router_part1.py` 中 Audit 的 Detail/Delete 使用了 `YSABNORMALITYId`、`AbnormalAuditId`、`CHECKACCOUNTId`、`AUDITTASKSId` 正确参数名。**Audit 不存在 `pk_val` 问题**。

但 Audit 确实存在 `code/message/data` 响应格式问题（上一轮已确认），这需要修复。

**建议修正**：AU-01 应改为"响应格式统一"，删除关于 `pk_val` 的描述。

---

### ⚠️ BS-01: BusinessMan 表映射"用 T_BUSINESSMAN 代替了 OWNERUNIT" — **需确认**

Codex 声称 Python 用 `T_BUSINESSMAN` 代替了原 C# 的 `OWNERUNIT` 表。但 **需要对照 C# 原代码确认**——C# 的 `BusinessManHelper` 操作的到底是 `T_OWNERUNIT` 还是 `T_BUSINESSMAN`。如果 C# 就有 `T_BUSINESSMAN` 表，则不存在映射漂移。

**建议**：此条暂不列为"属实"，需实际对照 C# 源码后才能判定。

---

### ⚠️ 整改工作量偏高估

Codex 将许多"实际有逻辑但可能与 C# 不完全一致"的接口也归入"需要重做"，例如：
- Revenue 散装报表（实际有复杂 SQL 和树形聚合）
- Audit 的 `get_audit_list`（实际有 JOIN 查询）
- Verification 的 `get_shop_endaccount_sum`（实际有聚合 SQL）

这些接口**不是占位**，只是可能需要细节调整（如字段名、排序、分页方式），而非全部重做。

---

## 四、执行计划评估

### 整体框架：✅ 合理

B1→B2→B3→B4→B5 的分层推进逻辑正确。SOP 6 步执行卡 + 3 组参数验证标准也合理。

### 需修正的点：

| 条目 | 问题 | 建议 |
|------|------|------|
| P0-01 重建基线 | 合理 | 可执行 |
| P0-02 对比脚本升级 | 合理 | 上一轮整改计划已包含 |
| P0-03 迁移脚本护栏 | 合理 | 上一轮整改计划已包含 |
| R1-R5 五角色分工 | **过于理想化** | 当前只有 1-2 个执行窗口，建议按模块而非角色分工 |
| B1 中 AU-01 | 错误包含 `pk_val` 修复 | Audit 不存在此问题，应只修响应格式 |
| B3 中 RE-01 | 全部重做 CRUD | 只需修响应格式和参数名即可 |

---

## 五、建议回复 Codex 修改的内容

1. **AU-01 删除 `pk_val` 相关描述** — Audit 使用了正确的实体专属参数名
2. **RE-01 降级为"契约修复"** — Revenue CRUD 只需修响应格式，散装报表有实际逻辑不需重做
3. **BS-01 标注"待确认"** — 表映射是否漂移需对照 C# 源码
4. **R1-R5 角色分工改为按模块分工** — 更符合实际执行场景
5. 补充说明**哪些接口有实际逻辑（只需微调）vs 哪些是纯占位（需重做）**

---

## 六、真正的 P0 紧急清单（按实际占位严重程度排序）

| 优先级 | 模块 | 占位接口数 | 说明 |
|--------|------|-----------|------|
| 🔴 P0-1 | **Verification** | **14 个** | 状态机简化 + 大量 return [] |
| 🔴 P0-2 | **Finance** | **22+ 个** | 审批流、固化、重算全部占位 |
| 🔴 P0-3 | **Sales** | **6 个** | 全部复用同一查询 |
| 🔴 P0-4 | **Audit** | **4 个** | 2 个 return [] + 2 个错误复用 |
| 🟡 P1-1 | **BusinessMan/Supplier** | **4 个** | 占位 + 简化 |
| 🟡 P1-2 | **Picture** | **9 个** | 路由集合偏离 |
| 🟡 P1-3 | **Video** | **16 个** | 全部未实现 |
| 🟢 P2-1 | **响应格式统一** | **~206 个** | `code/message/data` → `Result` |
| 🟢 P2-2 | **pk_val 泛化参数** | **~40 个** | Analysis + BusinessMan 动态 CRUD |

> **重要说明**：上述排序基于"接口有路由但实际无逻辑"的风险等级。相比之下，响应格式问题虽然涉及面广，但只要调用方能适配就不会造成数据错误，而占位实现会直接导致业务功能失效。
