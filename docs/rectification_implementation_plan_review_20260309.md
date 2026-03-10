# 综合实施方案整改意见（2026-03-09）

评审对象：

- [rectification_implementation_plan_20260309.md](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md)

评审目标：

- 不重写方案。
- 只指出这份方案当前还需要修正或补强的地方。
- 让后续执行、派工、验收不再因为文档自身歧义而返工。

## 1. 总体判断

这份综合方案的结构是可用的，优点有三点：

- 已经把上游 6 份文档收拢成了一个执行入口。
- 优先级基本正确，`Verification / Finance / Sales / Audit / Picture / Video` 仍然被放在高风险位置。
- 已经接受了 `Audit pk_val` 和 `Revenue generic CRUD` 的修正口径，方向比早期版本稳定。

但它还不能直接当最终执行底稿，原因不是“方向错”，而是“执行约束还不够严”。目前至少有 4 类问题：

- 个别事实判断与当前代码不一致。
- 阶段排期与窗口分工存在冲突。
- 状态定义和完成标准之间语义打架。
- 个别验收标准只验证“路由存在”，没有验证“逻辑正确”。

## 2. 必须修改的问题

### 2.1 `RE-02` 运行时错误的结论要改回去

问题：

- [rectification_implementation_plan_20260309.md:39](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L39)
  将 `RE-02 params运行时错误` 写成了“当前代码未发现，可能已修复”。

原因：

- 当前代码里该问题仍然存在：
  - [revenue_service.py:227](/E:/workfile/JAVA/NewAPI/services/revenue/revenue_service.py#L227)
  - [revenue_service.py:259](/E:/workfile/JAVA/NewAPI/services/revenue/revenue_service.py#L259)
- 两处仍在调用 `db.execute_query(sql, params)`，但 `params` 没有定义。

建议：

- 把这条结论改成“已确认存在，需先修再深比对”。
- 不要在综合方案里提前写成“可能已修复”。

影响：

- 这会直接影响 `RE-02` 的优先级判断。
- 如果不改，执行时容易把真实缺陷降级，导致报表链路带病进入 B3。

### 2.2 `CT-03` 的批次归属要纠正

问题：

- 阶段 1 的 B1 表里没有把 `CT-03` 排进去，见 [rectification_implementation_plan_20260309.md:202](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L202)-[rectification_implementation_plan_20260309.md:205](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L205)。
- 但阶段 3 又把 `CT-03/04` 一起放进了深逻辑阶段，见 [rectification_implementation_plan_20260309.md:226](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L226)。

原因：

- `CT-03` 本质上是契约和透传问题，不是 helper 级深逻辑问题。
- 在既有执行方案里，`CT-03` 属于 B1 契约层处理对象，而不是 B3。

建议：

- 把 `CT-03` 移回阶段 1。
- 阶段 3 只保留 `CT-04`。

影响：

- 如果不改，合同模块会出现“先做深逻辑、后修契约”的反顺序，验证会重复做两轮。

### 2.3 窗口定义和阶段表要统一口径

问题：

- 文档在 [rectification_implementation_plan_20260309.md:188](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L188)-[rectification_implementation_plan_20260309.md:198](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L198)
  已经定义了 `W1-W4` 的模块边界。
- 但阶段表又把这些模块重新打散：
  - [rectification_implementation_plan_20260309.md:205](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L205)
  - [rectification_implementation_plan_20260309.md:215](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L215)
  - [rectification_implementation_plan_20260309.md:216](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L216)
  - [rectification_implementation_plan_20260309.md:235](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L235)
  - [rectification_implementation_plan_20260309.md:236](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L236)

原因：

- 当前文档同时使用了两套规则：
  - 一套是固定窗口归属
  - 一套是按阶段临时拆包

建议：

- 二选一。
- 更推荐保留“固定窗口归属”，阶段表只写该窗口本阶段负责哪些整改包。
- 如果确实要跨窗口借人，单独加一列“例外原因”，不要直接打破窗口定义。

影响：

- 如果不改，实际执行时无法稳定派工，也无法判断窗口交接责任。

### 2.4 `B1` 完成标准的状态语义要修正

问题：

- 状态定义里：
  - [rectification_implementation_plan_20260309.md:30](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L30)
  - [rectification_implementation_plan_20260309.md:31](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L31)
  - [rectification_implementation_plan_20260309.md:32](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L32)
  已经定义 `C1=契约错误`、`C2=逻辑错误`。
- 但阶段 1 又写“所有 B1 包接口达到 C2（契约兼容）”，见 [rectification_implementation_plan_20260309.md:207](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L207)。

原因：

- 这里把 `C2` 当成了“达标状态”，但在状态体系里 `C2` 其实仍是错误状态。

建议：

- 把 B1 完成标准改成：
  - 清除 `C1` 和 `C5`
  - 契约进入可联调、可深比对状态
  - 不等同于整改完成

影响：

- 如果不改，阶段验收会出现“逻辑错误状态也算完成”的口径混乱。

## 3. 强烈建议修改的问题

### 3.1 `B4` 验收标准不能只看路由可见

问题：

- [rectification_implementation_plan_20260309.md:238](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L238)
  当前只写“原 C# 路由集合在 Python 运行时完整可见”。

原因：

- 这只能证明“路由注册了”，不能证明：
  - 参数对不对
  - 返回壳对不对
  - 逻辑是否与 C# 一致

建议：

- B4 验收至少补 3 项：
  - 路由可见
  - 基本 smoke 通过
  - 至少 3 组参数对比通过

影响：

- 否则会把“缺失接口补出来但逻辑仍然不对”的接口误判成完成。

### 3.2 “全局类任务”还需要再拆一层

问题：

- [rectification_implementation_plan_20260309.md:59](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L59)
  把“响应格式漂移”写成 `B1 全局`。
- [rectification_implementation_plan_20260309.md:83](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L83)-[rectification_implementation_plan_20260309.md:97](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L97)
  也基本是按问题类别写，没有拆到派工层。

原因：

- “全局”适合汇总，不适合执行。
- 真正执行时还需要知道：
  - 改哪些 router/service
  - 涉及哪些接口组
  - 哪一批算完成

建议：

- 至少拆成：
  - 整改包
  - 责任文件
  - 接口组

影响：

- 如果不拆，最后只能知道“做过响应格式修复”，但不知道“哪批接口已经修完并验收通过”。

### 3.3 实现手段不要写得比目标更重

问题：

- [rectification_implementation_plan_20260309.md:84](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L84)
  直接写 `Result.success()` / `Result.fail()`。
- [rectification_implementation_plan_20260309.md:88](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L88)
  直接写 `Query(..., alias=xxx)`。

原因：

- 这些是实现方式，不是目标本身。
- 目标应该是“恢复与 C# 一致的响应壳和参数契约”。

建议：

- 把文档口径改成“目标导向”：
  - 恢复原响应壳
  - 恢复原参数名/参数形态
- 实现方式交给具体整改时决定。

影响：

- 这样可以避免执行者为了套某种写法，反而把接口修偏。

### 3.4 多出路由不要直接写“下线”

问题：

- [rectification_implementation_plan_20260309.md:97](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L97)
  直接写“下线 `Supplier/DeleteQUALIFICATION_HIS`、Picture 多出 6 条”。

原因：

- 多出路由是否能删，取决于是否已有调用方。
- 在没有调用面确认前，直接写“下线”风险偏高。

建议：

- 调整成三步：
  1. 从迁移验收口径剔除
  2. 确认是否有调用方
  3. 再决定隔离、保留还是删除

影响：

- 可以避免清理动作引入新的回归。

## 4. 建议优化的问题

### 4.1 工期需要写清资源假设

问题：

- [rectification_implementation_plan_20260309.md:188](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L188)
  之后的各阶段天数没有明确资源前提。

原因：

- 这些工期只有在多窗口并行时才有成立可能。
- 如果实际只有单窗口或双窗口，时间会明显拉长。

建议：

- 在每个阶段标题旁补一句：
  - “以下为 4 窗口并行估算”
  - 或“若单窗口执行，工期至少翻倍”

影响：

- 避免排期时把并行估算误当成真实绝对工期。

### 4.2 建议明确这份文档的主从关系

问题：

- [rectification_implementation_plan_20260309.md:14](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L14)-[rectification_implementation_plan_20260309.md:19](/E:/workfile/JAVA/NewAPI/docs/rectification_implementation_plan_20260309.md#L19)
  这份文档同时引用了 6 份上游文档。

原因：

- 综合文档天然容易产生“复述后漂移”。
- 当前 `RE-02`、`CT-03` 就已经出现了这种情况。

建议：

- 在开头明确：
  - 接口级事实，以整改矩阵为准
  - 执行批次和验收规则，以执行方案为准
  - 本文只负责整合、排序和派工口径

影响：

- 这样后面即使综合文档没有同步更新，也不会覆盖上游事实文档。

## 5. 推荐修订顺序

如果只按执行风险排序，建议按下面顺序改这份方案：

1. 修正 `RE-02` 运行时错误结论。
2. 把 `CT-03` 从阶段 3 移回阶段 1。
3. 统一 `W1-W4` 与阶段表的窗口归属。
4. 改写 `B1` 完成标准，避免 `C2` 被当成完成态。
5. 补强 `B4` 验收标准。
6. 把“B1 全局”类任务拆到可派工层。

## 6. 结论

这份综合方案现在最大的价值，是把整改方向和批次收拢了。

它当前最大的短板，不是方向错，而是：

- 个别事实判断还没有跟最新代码保持一致。
- 执行分工和阶段表还没有完全收敛成一套口径。
- 验收标准在少数阶段仍然偏“看得到”，而不是“做得对”。

把前述 6 点修完后，这份文档就可以作为 Antigravity 和执行窗口共享的统一入口。
