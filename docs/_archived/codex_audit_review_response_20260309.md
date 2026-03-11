# Codex 对 Antigravity 审查结果的响应（2026-03-09）

## 1. 文档目的

这份文档只处理一件事：

- 对 [codex_audit_review_20260309.md](/E:/workfile/JAVA/NewAPI/docs/codex_audit_review_20260309.md) 中判为“不属实”或“半属实”的条目，说明原因、修正文档口径，并给出后续操作方式。

相关修订已同步回以下文件：

- [full_audit_rectification_matrix_20260309.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_rectification_matrix_20260309.md)
- [full_audit_execution_plan_20260309.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_execution_plan_20260309.md)

## 2. 逐条响应

### 2.1 `AU-01`：接受修正，原“`pk_val`”判断不属实

结论：

- 接受 Antigravity 审查意见。
- 我之前把 batch 模板问题泛化到了 Audit，属于过度外推。

原因：

- `Audit/GetYSABNORMALITYDetail`、`Audit/GetAbnormalAuditDetail`、`Audit/GetCHECKACCOUNTDetail`、`Audit/GetAUDITTASKSDetail` 以及对应删除接口，当前使用的是实体专属参数名，不是 `pk_val`。
- Audit 的真实问题在于：
  - 返回壳仍是 `code/message/data`
  - 输入模型被弱化成 `dict`
  - 原 C# 的强类型 SearchModel / JsonMsg 契约没有保持

后续操作：

1. 不再把 Audit 归入“`pk_val` 清理”范围。
2. `AU-01` 调整为“实体 CRUD 契约修复包”。
3. 实施重点改为：修返回壳、修强类型输入模型、核对列表/同步契约。
4. 验收重点改为：参数名保持不变，返回包结构与 C# 一致。

### 2.2 `RE-01`：部分接受修正，原“全部重做 generic CRUD”表述过强

结论：

- 接受“不能直接把 Revenue generic CRUD 全部判成错误重做”的意见。
- 但保留“当前尚未证明与 C# 完全等价，因此仍需列入整改”的判断。

原因：

- Python `revenue_service.py` 确实存在 7 组实体的 generic CRUD 映射。
- 这一点本身不自动等于错误，因为 C# 侧相当一部分 CRUD 也具有模板化特征。
- 真正未确认的是：
  - 表名/主键/状态字段是否逐组等价
  - 返回包结构是否一致
  - `PERSONSELL` 等接口的汇总值、`OtherData` 是否保持

后续操作：

1. `RE-01` 从“7 组实体 CRUD 壳化治理包”改为“7 组实体 CRUD 契约与等价性复核包”。
2. 不预设“全部重做”。
3. 先逐实体完成：
   - list/detail/synchro/delete 契约对比
   - 表名/主键/状态字段对比
   - `PERSONSELL` 汇总/`OtherData` 对比
4. 只有确认不等价的实体，再拆出独立 helper。
5. 因为这是契约和等价性基线问题，实施批次前移到 `B1`。

### 2.3 `RE-02`：接受“不是空实现”的修正，但维持“需要深比对”的判断

结论：

- 接受 Antigravity 关于“Revenue 报表/对账/分析并非纯占位”的修正。
- 我之前把“本地聚合替代 helper”写得过重，现在改为“已有实际逻辑，但与原 helper 的等价性未证实”。

原因：

- `revenue_service.py` 中确实存在较多实际 SQL/聚合代码。
- 但同时也存在确定性问题：
  - `GetHisCommoditySaleList`
  - `GetRevenueDataList`
  这两条存在 `params` 未定义的运行时错误。
- 另外，Header 透传和与原 helper 的统计口径是否一致，仍未逐条完成 SOP 级验证。

后续操作：

1. 先修运行时错误。
2. 补 Header 透传。
3. 再按“销售明细 / 收入报表 / 对账 / 分析”四条链做深比对。
4. 只对确认不等价的链路重构，不再预设整包重写。

### 2.4 `BS-01`：维持原判断，审查中的“待确认”在复核后可转为属实

结论：

- 这一条不按“不属实”处理，维持原判断。

原因：

- 我已复核原 C# Helper：
  - `BusinessManHelper` 使用 `OWNERUNIT`
  - `BusinessManDetailHelper` 使用 `OWNERUNITDETAIL`
  - `COMMODITY_BUSINESSHelper` 使用 `COMMODITY_BUSINESS`
- 当前 Python `businessman_service.py` 使用的是：
  - `T_BUSINESSMAN`
  - `T_BUSINESSMANDETAIL`
  - `T_COMMODITY`

这不是“命名差异”，而是业务关系表映射已经漂移。

后续操作：

1. `BS-01` 保持为表映射修正包。
2. 不把它降级为“待确认”。
3. 先修表映射，再谈创建、删除、关系维护、商品绑定的一致性。

### 2.5 `AU-02`：部分接受修正，改为分层处置

结论：

- 接受“不能把整个 Audit 报表/流程包都判为同一严重度”的意见。

原因：

- 该包内部实际分为 3 类：
  - 纯占位：
    - `GetSpecialBehaviorReport`
    - `GetAbnormalRateReport`
  - 错误复用通用 CRUD：
    - `GetAuditDetils`
    - `UpLoadAuditExplain`
    - `IssueAuditTasks`
    - `GetAuditTasksDetailList`
  - 已有 SQL，但仍需验证与原 helper 是否等价：
    - `GetAuditList`
    - `GetCheckAccountReport`
    - `GetYsabnormalityReport`
    - `GetAuditTasksReport`

后续操作：

1. 先补纯占位。
2. 再修错误复用。
3. 最后对已有 SQL 的接口做深比对和微调。
4. 不再把 `AU-02` 一刀切地写成“整包重做”。

### 2.6 `R1-R5`：接受修正，实施方案改为按模块工作流推进

结论：

- 接受“按抽象角色分工过于理想化”的意见。

原因：

- 现阶段执行资源更接近“1-4 个窗口并行”，而不是独立职能团队。
- 按模块工作流推进，更符合当前实际执行方式，也更利于文件和上下文集中。

后续操作：

1. 实施方案中的 `R1-R5` 已改为：
   - `W1 BaseInfo / Merchants / Contract`
   - `W2 Finance / Revenue / BigData / MobilePay`
   - `W3 Audit / Analysis / BusinessMan / Supplier / Verification / Sales`
   - `W4 Picture / Video / Tooling`
2. 资源不足时，优先顺序为：
   1. `W3`
   2. `W2`
   3. `W4`
   4. `W1`

## 3. 修订后的执行口径

后续整改按以下原则执行：

1. 纯占位、错误复用、状态机缺失，优先级最高，先补真逻辑。
2. 契约层错误但已有真实逻辑的接口，先做包装/参数/Header 修复，再做 SOP 深比对。
3. generic CRUD 不再天然视为错误；只有与原 C# helper 不等价时才拆出独立实现。
4. 表映射漂移一旦确认，必须先修表映射，再谈业务一致性。

## 4. 当前建议动作顺序

1. `B1`
   先做契约和等价性基线：`AU-01`、`RE-01`、`RE-03`、`BG-01`、`AN-01`、`BS-02`
2. `B2`
   先清真正的 P0 逻辑问题：`VE-01`、`VE-02`、`VE-03`、`VE-04`、`FI-03`、`FI-04`、`SA-01`、`PI-01`、`AU-02`
3. `B3`
   再做 helper 级深比对和业务语义回迁：`RE-02`、`CT-04`、`BG-02`、`AN-02`、`BS-01`、`SU-01`、`SA-02`
4. `B4`
   最后补缺失路由和外部能力：`PI-02`、`FI-05`、`VI-01`、`VI-02`、`VI-03`、`VI-04`、`VI-05`

## 5. 结论

Antigravity 的审查对本次整改规划是有效纠偏，尤其纠正了两个问题：

- 不能把所有 generic CRUD 直接等同于错误重做
- 不能把 Audit 的模板问题泛化成 `pk_val` 问题

但 `BusinessMan` 表映射漂移这一条，经复核原 C# Helper 后，仍然成立，不应降级。
