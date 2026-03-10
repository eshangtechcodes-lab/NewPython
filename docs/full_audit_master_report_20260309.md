# 全量接口一致性总报告（2026-03-09）

## 1. 审计结论

本次已汇总 4 个并行窗口的全量静态审计结果，覆盖你指定的 15 个模块：

- BaseInfo
- Merchants
- Contract
- Finance
- Revenue
- BigData
- MobilePay
- Audit
- Analysis
- BusinessMan
- Supplier
- Verification
- Sales
- Picture
- Video

结论不是“少量接口有问题”，而是“当前项目整体仍不能按逻辑等价迁移验收”。

可以明确下结论的点：

- 路由存在，不等于迁移完成。
- 当前大量接口只是“路由已挂出”或“单表 CRUD 可调用”，但和原 C# 的 controller/helper 逻辑并不一致。
- 高风险问题已不是零散问题，而是系统性问题：通用 CRUD 壳化、Header/Token 丢失、返回契约漂移、占位实现、文件/外部系统逻辑缺失。
- `Picture` 和 `Video` 不能算已收尾：前者是整套路由集合被替换，后者是原 C# 16 条接口全部未迁移。

按各窗口统计口径，当前可静态判定“完全一致”的接口主要集中在：

- BaseInfo / Merchants 的一部分普通查询与 CRUD
- Contract 的一部分简单路由
- Finance 中预算、附件、发票的部分路由
- Revenue 中极少数报表接口

其余大量接口属于以下几类之一：

- 契约不一致
- 逻辑不一致
- 占位实现
- Python 多出但不能冲抵迁移完成度
- Python 缺失

## 2. 模块总体判断

| 模块 | 当前判断 | 主要问题 | 整改优先级 |
| --- | --- | --- | --- |
| BaseInfo | 部分可用，但未等价 | Header/UserPattern/Token 注入不全，部分列表与树接口被简化，少量方法放宽 GET/POST | P1 |
| Merchants | 问题集中但可收敛 | `ProvinceCode` 权限注入缺失，列表范围可能越权 | P1 |
| Contract | 高风险，不能按完成验收 | Token、历史日志、软删校验、文件接口、`GetFromRedis`、`OtherData/summaryObject` 大量漂移或占位 | P0 |
| Finance | 高风险，不能按完成验收 | 报表、审批流、固化/生成、对账、短信/提单等大量是空实现或简化版 | P0 |
| Revenue | 高风险，需大面积重做 helper 逻辑 | 大量 entity-specific helper 被 generic CRUD 取代，报表/汇总/对账语义漂移 | P0 |
| BigData | 高风险 | 通用返回壳替代原模型，`BAYONETWARNING` 缺 3 条，Customer 权限逻辑丢失 | P1 |
| MobilePay | 高风险 | 外部支付/银联 helper 被本地表查询替代，提现/分润报表是占位 | P0 |
| Audit | 高风险 | 稽核任务、报表、上传说明流程被单表 CRUD 或空返回替代 | P0 |
| Analysis | 高风险 | 大面积 batch CRUD 壳化，`pk_val`、小写包装、4 条 `SPCONTRIBUTION` 缺失 | P0 |
| BusinessMan | 高风险 | 表映射漂移，授权/关系/用户树逻辑未迁回 | P0 |
| Supplier | 高风险 | 树、资质、关联逻辑未迁回，且多暴露 1 条额外删除路由 | P1 |
| Verification | 极高风险 | 日结状态机、审批、作废、冲正、重建等核心流程大量为空实现或简化版 | P0 |
| Sales | 高风险 | 汇总/排行/纠错/刷新逻辑被 `T_COMMODITYSALE` CRUD 替代，删除语义反向漂移 | P0 |
| Picture | 极高风险 | 原 9 条凭证接口被另一套 `T_PICTURE` 管理接口错误替代 | P0 |
| Video | 未开始 | 原 C# 16 条接口全部缺失 | P0 |

## 3. 共性问题归类

本次审计确认的共性问题，足以解释为什么“完成率看起来很高，但逻辑一致性并不高”。

### 3.1 通用 CRUD 壳化

高发模块：

- Revenue
- Audit
- Analysis
- BusinessMan
- Supplier
- Sales
- BigData 的部分实体

表现形式：

- 原 C# 每个接口都有独立 helper、聚合逻辑、`OtherData`、树形或审批语义。
- Python 统一收敛成 `get_list/detail/synchro/delete`。
- 结果是接口“能返回数据”，但业务语义已经换了。

### 3.2 契约层漂移

高发点：

- batch router 统一 `pk_val`
- `code/message/data` 替代原 `Result_Code/Result_Desc/Result_Data`
- GET/POST 方法被放宽或收窄
- 原强类型模型被改成 `dict`

这类问题即使 SQL 没错，也会直接破坏兼容性。

### 3.3 Header / Token / 上下文丢失

高发字段：

- `ProvinceCode`
- `ServerpartCodes`
- `ServerpartShopIds`
- `UserPattern`
- `Token`
- `ModuleGuid`
- `SourcePlatform`
- `GetFromRedis`

高发模块：

- BaseInfo
- Merchants
- Contract
- Revenue
- BigData
- MobilePay
- Audit
- Verification

这类问题会导致权限口径、操作人、缓存分支、审批上下文全部漂移。

### 3.4 占位实现被误算为完成

典型表现：

- `return []`
- `return {}`
- `return True`
- `return {"status": "ok"}`
- 注释中直接写“简化版”“暂未实现”“功能未迁移”

高发模块：

- Finance
- MobilePay
- Audit
- Analysis
- Verification

### 3.5 文件系统 / 外部系统逻辑被抹平

典型场景：

- `Picture` 文件上传、文件删除、目录映射、HWS 图片表
- `Contract` 附件保存/删除
- `Invoice` 航信 / 金蝶转发
- `MobilePay` / `ChinaUmsSub` 外部支付查询

这些接口如果被改成“只写本地表”，不属于兼容迁移。

### 3.6 路由集合被替换或缺失

最严重的两个模块：

- `Picture`：不是少量差异，而是原接口集合被另一套接口替代
- `Video`：原 C# 16 条接口全部未迁移

## 4. 最高优先级整改包

下面是建议的整改顺序。顺序不是按“模块名称”，而是按“回归风险”和“能否先止血”排序。

### 整改包 A：先修公共契约层

目标：先把最容易批量扩散的问题止住。

包含内容：

- 收敛 batch router，不再统一 `pk_val`
- 恢复原响应包装结构
- 收敛 GET/POST 到原 C# 口径
- 建立公共 Header/Token 注入层
- 明确“Python 多出路由”不计入迁移完成度
- 重建 baseline 与运行时路由口径，消除误统计算法

建议优先模块：

- Analysis
- Audit
- Supplier
- Sales
- BaseInfo
- Merchants
- Contract
- BigData

交付标准：

- 契约层兼容，不再出现统一 `pk_val` / 小写包装 / 错误 HTTP 方法的系统性扩散

### 整改包 B：先补 P0 占位与状态机

目标：优先消除“看起来有接口，实际上没逻辑”的核心业务风险。

包含内容：

- Verification 日结状态机
- Finance 审批流 / 固化 / 生成 / 对账 / 补录
- Audit 报表与任务流
- MobilePay 提现 / 分润 / 银联对账
- Contract 删除 / 历史 / 日志 / 文件

建议优先模块：

- Verification
- Finance
- Audit
- MobilePay
- Contract

交付标准：

- 不再允许 `return []/True/{}` 作为已迁移接口上线

### 整改包 C：恢复 helper 级业务语义

目标：解决“接口有返回，但业务含义不对”的深层问题。

包含内容：

- Revenue 去掉 generic CRUD，恢复各实体 helper
- Analysis 去掉 CRUD 壳，恢复分析/固化/报表逻辑
- BusinessMan 修正表映射和授权关系
- Supplier 恢复树、资质和关联
- Sales 恢复汇总、排行、纠错、刷新流程
- BigData 恢复实体特定模型与权限逻辑

建议优先模块：

- Revenue
- Analysis
- BusinessMan
- Supplier
- Sales
- BigData

交付标准：

- 列表、明细、同步、删除不再只是单表语义
- `OtherData/summaryObject/树形结果/审批状态` 恢复到原接口口径

### 整改包 D：补齐缺失路由

目标：把真正未迁移的接口补全。

包含内容：

- `Video` 全 16 条
- `Picture` 原 9 条恢复为正式验收集合
- `BigData/BAYONETWARNING` 3 条
- `Analysis/SPCONTRIBUTION` 4 条
- `Finance/Invoice/Office` 缺失 12 条
- `Merchants/GetCoopMerchantsDDL`
- `Contract` 明确缺失接口

交付标准：

- 所有原 C# 路由都能在 Python 运行时找到一一对应实现

## 5. 模块级整改建议

### BaseInfo / Merchants

- 先统一修 `ProvinceCode`、`ServerpartCodes`、`ServerpartShopIds`、`UserPattern` 注入。
- 优先修 `ServerpartShop`、`USERDEFINEDTYPE`、`ServerPartShopNew`。
- Merchants 先补 `ProvinceCode` 权限链和 `GetCoopMerchantsDDL`。

### Contract

- 第一优先级是 `RegisterCompact` 主链：列表、删除、同步、补充协议、历史、日志、Token。
- 第二优先级是文件接口：`SaveAttachment`、`DelFile`。
- 第三优先级是 `BusinessProject` 汇总类接口：`summaryObject`、审批状态、`GetFromRedis`。

### Finance / MobilePay

- Finance 先集中处理 `finance_scattered_service.py`。
- 预算报表族、审批流、固化/重算、对账、提单、短信这类接口不能再视为已完成。
- MobilePay 必须恢复 `MobilePayHelper` / `ChinaUmsSubHelper` 语义，不能本地表兜底。

### Revenue / BigData

- Revenue 需要整体去 generic CRUD 化，这是一个模块级重构，不是几条接口小修。
- BigData 先补 `BAYONETWARNING`，再恢复原模型和权限逻辑，避免再用统一返回壳。

### Audit / Analysis / BusinessMan / Supplier / Verification / Sales

- 这 6 个模块基本都受 batch router 模板缺陷影响。
- 应按“模板治理 + 模块回迁”两步走：
  - 先治模板
  - 再按 helper 恢复具体业务
- `Verification` 和 `Sales` 优先级要高于 `Analysis` / `BusinessMan` / `Supplier`，因为它们包含状态机、纠错和真实写操作。

### Picture / Video

- `Picture` 必须先恢复原接口集合，再谈是否保留额外 `T_PICTURE` 管理接口。
- `Video` 建议直接按 5 批迁移：
  1. `EXTRANET` 4 条
  2. `EXTRANETDETAIL` 4 条
  3. `SHOPVIDEO` 4 条
  4. `VIDEOLOG` 2 条
  5. `GetShopVideoInfo` + `GetYSShopVideoInfo`

## 6. 后续实施计划

建议不要再按“模块完成率”推进，而改成“整改批次 + 验收门槛”推进。

### 阶段 0：重建验收口径

输出物：

- 新的 runtime baseline
- 统一的迁移状态分级
- Python 多出 / 原路由缺失 / 契约漂移分层统计

完成标准：

- 后续进度不再用“路由挂出数”表示完成

### 阶段 1：公共层止血

输出物：

- 公共 Header/Token 注入层
- 原响应包装兼容层
- batch router 契约修复
- 原始 HTTP 方法校正

建议先覆盖模块：

- BaseInfo
- Merchants
- Contract
- Analysis
- Audit
- Supplier
- Sales
- BigData

完成标准：

- 不再新增新的契约漂移

### 阶段 2：P0 业务回迁

输出物：

- Verification 状态机恢复
- Finance 散装核心接口恢复
- Audit 任务/报表恢复
- MobilePay 外部支付链恢复
- Contract 删除/日志/附件恢复
- Picture 原接口恢复

完成标准：

- 所有 P0 占位接口下线或完成迁移

### 阶段 3：模块深逻辑回迁

输出物：

- Revenue helper 级回迁
- Analysis 分析/固化/报表回迁
- BusinessMan 关系与授权回迁
- Supplier 树和资质回迁
- Sales 汇总/排行/刷新回迁
- BigData 模型和权限回迁

完成标准：

- “返回数据但语义不对”的大头问题基本清空

### 阶段 4：缺失接口补齐

输出物：

- Video 全量接口
- BigData/Analysis/Finance 等缺失路由补齐

完成标准：

- 原 C# 路由集合在 Python 运行时完整可见

### 阶段 5：动态比对验收

输出物：

- 升级版 `compare_api.py`
- 每接口至少 3 组参数基准
- 新旧接口差异清单

完成标准：

- 验收不再停留在静态审计，而是进入真实数据对比

## 7. 建议的迁移状态分级

后续建议把“完成状态”改成以下 5 级：

- L0：未迁移
- L1：仅路由存在
- L2：契约兼容
- L3：逻辑等价
- L4：已通过新旧接口动态比对

当前项目的真实问题，是很多接口被提前标记为“已完成”，但实际上只到 L1 或 L2。

## 8. 范围说明

本次报告以 4 个窗口的静态审计结果为准，已经足够得出“不完全一致”的确定性结论。

需要注意的边界：

- 存在少量 baseline 漂移，例如 `Expenses`、BigData 部分路由的统计口径需要重新校正。
- 文件系统、外部支付、航信、视频聚合等接口，静态审计已能判定“不一致”，但精确行为仍需后续联调收口。
- 本报告不回滚任何现有代码，只作为整改和后续实施的总控依据。
