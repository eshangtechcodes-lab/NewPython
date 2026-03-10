# 全量接口整改实施方案（2026-03-09）

## 1. 文档目标

这份文档是“执行版实施方案”，不是概览。

它解决 4 件事：

1. 当前接口到底对不对
2. 错在哪里
3. 应该怎么改
4. 改完以后按什么步骤验证

本方案与以下文档配套使用：

- 基础结论：[full_audit_master_report_20260309.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_master_report_20260309.md)
- 接口级整改台账：[full_audit_rectification_matrix_20260309.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_rectification_matrix_20260309.md)
- 知识沉淀：[interface_migration_knowledge_base_20260309.md](/E:/workfile/JAVA/NewAPI/docs/interface_migration_knowledge_base_20260309.md)
- 迁移 SOP：[api-migration-sop.md](/E:/workfile/JAVA/NewAPI/.agent/workflows/api-migration-sop.md)

规则：

- `full_audit_rectification_matrix_20260309.md` 负责列清楚“哪几个接口有问题”
- 本文负责规定“这些问题按什么顺序、什么方法、什么验证规则去整改”

## 2. 统一判定标准

后续所有整改任务统一按以下状态管理：

- `C0`：完全正确
- `C1`：契约错误
- `C2`：逻辑错误
- `C3`：占位实现
- `C4`：Python 缺失
- `C5`：Python 多出，不计入原接口完成度

只有 `C0` 才能算整改完成。

## 3. 必须遵守的 SOP 执行方式

本次整改不是重新发明流程，而是把现有 SOP 用到“修错接口”上。

### 3.1 每个整改包必须走完 6 步

对每一个整改包，都必须严格执行：

1. 读原 C# Controller / Helper / Model
2. 调原 C# API 记录基准响应
3. 检查并同步所需表
4. 修改 Python router / service / model / main.py
5. 用 3 组参数对比验证
6. 更新整改状态、工作日志、修改记录

### 3.2 步骤 1 要记录什么

每个整改包都必须重新确认：

- 原路由大小写
- HTTP 方法
- 入参形态
- Header 读取
- Delete 语义
- Helper SQL
- JOIN 关联表
- 默认分页
- 默认排序
- 特殊副作用

### 3.3 步骤 2 要记录什么

每个整改包至少要记录：

- `Result_Code`
- `TotalCount`
- `List` 条数
- 字段名全集
- 关键字段类型
- 默认排序
- 第一条/关键条样本

### 3.4 步骤 3 的硬性要求

严禁无参执行全量迁移脚本。

每个整改包必须先列出：

- 主表
- 所有关联表
- 动态表或视图
- 需要的序列

然后只迁移本包用到的表。

### 3.5 步骤 5 的硬性要求

每个接口至少 3 组参数。

必须覆盖：

- 空参或默认参数
- 常规有效参数
- 边界参数或特殊 Header

检查项按 SOP 固定执行：

- `Result_Code`
- `TotalCount`
- `List` 条数
- 字段列表
- 字段类型
- 排序
- 空值处理
- 业务 Warning / 汇总字段 / `OtherData`

### 3.6 整改失败后的回退规则

如果验证失败，必须回到对应步骤重新处理：

- 契约不一致：回步骤 1 和步骤 4
- 字段缺失 / 总数不一致：回步骤 1、2、3、4
- 表或字段不存在：回步骤 3
- 排序 / 分页 / Header 错误：回步骤 1、4
- 占位逻辑或副作用错误：回步骤 1、2、4

## 4. 整改前置任务

这些任务先做，不然后面大批整改会反复返工。

### `P0-01` 运行时基线重建

目标：

- 重新导出最新 Python 运行时路由
- 校正 `baseline` 漂移
- 分开统计 `C4` 和 `C5`

原因：

- 目前 `Expenses`、BigData 部分路由存在 baseline 漂移
- 不先修基线，后面整改进度会持续失真

输出：

- 新版运行时 baseline JSON
- 新版“原 C# / Python / 差异”统计表

### `P0-02` 对比脚本升级

目标：

- 升级 `scripts/compare_api.py`
- 支持 GET / POST
- 支持 Header
- 支持 3 组参数
- 支持字段级 diff
- 支持 `Result_Data.List` 之外的结构比较

原因：

- 当前脚本不满足 SOP 的三组参数对比要求

输出：

- 升级后的 compare 脚本
- 标准对比报告模板

### `P0-03` 迁移脚本护栏

目标：

- 收紧 `scripts/server_migrate.py`
- 默认禁止无参数全量跑
- 明确必须带表名或显式 `--all`

原因：

- SOP 已明确禁止无参全量迁移

输出：

- 受控迁移脚本
- 表同步执行规范

## 5. 工作流与角色分工

建议按模块工作流并行推进，而不是按抽象角色分工：

- `W1 BaseInfo / Merchants / Contract`
  负责基础资料、商户、合同主链、BusinessProject 与配套契约修复。

- `W2 Finance / Revenue / BigData / MobilePay`
  负责财务、收入、大数据、外部支付及相关报表/对账链路。

- `W3 Audit / Analysis / BusinessMan / Supplier / Verification / Sales`
  负责 batch 模块、状态机、树/汇总、商户与供应商关系链。

- `W4 Picture / Video / Tooling`
  负责图片、视频缺失接口，以及 compare/migrate 工具护栏。

资源不足时按以下顺序投入：

1. `W3`
2. `W2`
3. `W4`
4. `W1`

## 6. 批次实施方案

## 6.1 B1 契约层止血批

目标：

- 先阻止错误模板继续扩散
- 先把“调用方式不兼容”的问题清掉

进入条件：

- `P0-01`、`P0-02` 至少完成基础版

完成标准：

- 所有 B1 包的接口都至少达到 `C2`，不再停留在 `C1/C5`

### B1 包清单

| 包ID | 接口是否正确 | 主要错误点 | 整改方法 | 主要文件范围 | 整改后验证 |
| --- | --- | --- | --- | --- | --- |
| `BM-01` | `C1/C2` | Header、Token、HTTP 方法、可选参数漂移 | 做 BaseInfo/Merchants 公共上下文注入层，逐路由恢复原契约 | `routers/eshang_api_main/base_info/*`、`routers/eshang_api_main/merchants/*`、`routers/deps.py`、相关 `service` | 3 组参数比对：空参、带 `ProvinceCode`、带 `UserPattern=2000/9000` |
| `CT-03` | `C1/C2` | `GetFromRedis` 未透传、默认值漂移 | 恢复参数透传、缓存/实时双路径 | `routers/eshang_api_main/contract/contract_router.py`、`services/contract/contract_service.py` | 同参对比缓存与非缓存分支 |
| `RE-01` | `C1/C2` | generic CRUD 等价性未证实，包装/参数/`OtherData` 漂移 | 保留 generic CRUD 底座，逐实体核对表/主键/状态字段/包装；只对确认不等价者拆独立 helper | `routers/eshang_api_main/revenue/revenue_router.py`、`services/revenue/revenue_service.py` | 7 组实体逐组完成 list/detail/sync/delete 对比，`PERSONSELL` 额外核对汇总/`OtherData` |
| `RE-03` | `C1` | GET/POST、query/body 契约漂移 | 先恢复路由和入参形态，再回归 | `routers/eshang_api_main/revenue/revenue_router.py` | 3 组同比/环比参数直接对比新旧接口 |
| `BG-01` | `C1/C2` | 通用包装、Customer Header 缺失 | 拆掉 generic CRUD 壳，恢复原响应模型和 Header | `routers/eshang_api_main/bigdata/*`、`services/bigdata/*` | 比对结果包结构、字段名、Customer 权限范围 |
| `AU-01` | `C1/C2` | `data:dict`、小写包装、强类型模型丢失 | 保留现有参数名，先修返回壳和强类型输入模型 | `routers/eshang_api_main/batch_modules/batch_router_part1.py`、`services/audit/audit_service.py` | 对比详情/删除参数名、列表查询条件、同步入参与返回壳 |
| `AN-01` | `C1/C2` | 11 组实体被模板化 | 把 Analysis 从 batch 模板中拆出，恢复原契约 | `routers/eshang_api_main/batch_modules/batch_router_part2.py`、`services/analysis/analysis_service.py` | 每组选 1 条 list/detail/synchro/delete 做 3 组参数对比 |
| `BS-02` | `C1` | CUSTOMTYPE / COMMODITY_TEMP 被模板化 | 恢复强类型模型和原 JsonMsg 包装 | `routers/eshang_api_main/batch_modules/batch_router_part2.py`、`services/businessman/businessman_service.py` | 比对详情、同步、删除契约 |
| `SU-03` | `C5` | 多出 `DeleteQUALIFICATION_HIS` | 下线或隔离多出路由 | `routers/eshang_api_main/batch_modules/batch_router_part2.py` | 运行时路由集合比对，不再出现多余路由 |
| `PI-03` | `C5` | Picture 多出 6 条不属于原模块的接口 | 从迁移验收口径剔除，必要时迁到独立模块 | `routers/eshang_api_main/batch_modules/batch_router_part2.py`、`services/picture/picture_service.py` | 路由集合与原 C# PictureController 重新对齐 |

## 6.2 B2 P0 流程与状态机批

目标：

- 优先解决“接口在，但逻辑根本不对”的高风险问题

进入条件：

- 相关模块的 B1 问题先清掉

完成标准：

- 所有 B2 包不得存在占位返回
- 不得再出现“真实写操作被替换成单表 upsert”

### B2 包清单

| 包ID | 接口是否正确 | 主要错误点 | 整改方法 | 主要文件范围 | 整改后验证 |
| --- | --- | --- | --- | --- | --- |
| `CT-01` | `C2` | Token、删除校验、历史、日志缺失 | 按 RegisterCompact 主链回迁 | `contract_router.py`、`contract_service.py`、相关 helper 映射 | 3 组参数：正常删除、删除失败、补充协议新增 |
| `CT-02` | `C3` | 附件接口占位 | 接入真实文件存储和删除 | `contract_router.py`、附件 service、文件路径配置 | 上传、删除、失败路径 3 组测试 |
| `FI-01` | `C1/C3` | Budget 报表族缺实现 | 逐条恢复原报表族 | `services/finance/budget_service.py`、`budget_router.py` | 月报、进项、出项 3 组参数对比 |
| `FI-03` | `C3` | 审批流、固化、补录为空实现 | 先审批，再固化，再补录，分链回迁 | `services/finance/finance_scattered_service.py` | 状态流转、批量审批、差异计算比对 |
| `FI-04` | `C3` | 重算、短信、提单、对账为空实现 | 拆子任务重做，不允许壳接口 | `finance_scattered_service.py` | 每条接口至少 1 组成功 + 1 组失败 + 1 组边界验证 |
| `MP-01` | `C2` | 外部支付/银联被本地表替代 | 恢复 `MobilePayHelper` / `ChinaUmsSubHelper` 调用链 | `services/mobilepay/mobilepay_service.py`、相关 router | 分润、对账树、银联查询 3 组验证 |
| `MP-02` | `C3` | 提现/报表占位 | 恢复提现和报表逻辑 | `mobilepay_service.py` | 提现动作、报表结果、失败分支验证 |
| `AU-02` | `C2/C3` | 稽核流程、说明上传、报表、任务下发不对 | 按四条业务链重做 | `batch_router_part1.py`、`audit_service.py` | 稽核明细、上传说明、报表、任务下发 4 组联调 |
| `BS-03` | `C2` | 授权、创建商户、用户树被简化 | 逐条恢复关系写入和用户树 | `businessman_service.py`、`batch_router_part2.py` | 授权历史、创建副作用、GET/POST 用户树 |
| `SU-02` | `C3` | `RelateBusinessCommodity` 直接成功 | 恢复关联写入和历史 | `businessman_service.py`、`batch_router_part2.py` | 关联前后数据和历史记录验证 |
| `VE-01` | `C2` | `ENDACCOUNT` 被迁成 `ENDACCOUNT_DAILY` | 先修主表与模型，再恢复当前/历史查询 | `verification_service.py`、`batch_router_part2.py` | 主表、主键、当前/历史 3 组验证 |
| `VE-02` | `C2` | 日结状态机被简化成状态位更新 | 直接按状态机全量回迁 | `verification_service.py` | 审核、批量审批、作废、取消 4 组验证 |
| `VE-03` | `C2/C3` | 数据校验查询链为空或错表 | 按数据类型和汇总链恢复 | `verification_service.py` | `Data_Type` 分支、汇总值、补录列表比对 |
| `VE-04` | `C3` | 保存/纠错/重建全是占位 | 恢复真实写入和重建逻辑 | `verification_service.py` | 写前写后状态、错误返回、重建结果验证 |
| `SA-01` | `C1/C2` | COMMODITYSALE 被模板化，删除语义反向漂移 | 先恢复删除语义，再恢复契约 | `verification_service.py`、`batch_router_part2.py` | 删除前后数据、列表明细契约、新旧删除行为比对 |
| `PI-01` | `C2` | 同名 Picture 接口被改义 | 按原 Picture 模块重建，不再沿用 `T_PICTURE` 思路 | `picture_service.py`、`batch_router_part2.py` | multipart、base64、物理文件、业务表、副作用 |

## 6.3 B3 helper 级业务语义回迁批

目标：

- 解决“看起来能返回数据，但业务语义不等价”的问题

进入条件：

- 对应包的 B1/B2 已清理完

完成标准：

- 所有 B3 包的接口至少达到 `C2` 以上
- `OtherData`、树、汇总、审批状态、动态计算恢复

### B3 包清单

| 包ID | 接口是否正确 | 主要错误点 | 整改方法 | 主要文件范围 | 整改后验证 |
| --- | --- | --- | --- | --- | --- |
| `BM-02` | `C2/C3` | Commodity / PropertyAssets 被简化 | 按原 helper 迁回编码、同步、树、关联 | `services/base_info/*`、对应 router | 编码生成、树结构、门店关联比对 |
| `CT-04` | `C2` | BusinessProject 汇总、审批、费用逻辑被裁剪 | 按费用链、预警链、应收链三段回迁 | `services/contract/*`、`routers/eshang_api_main/contract/*` | `summaryObject`、审批状态、平台分支、历史作废 |
| `FI-02` | `C2` | 多个散装汇总接口共用错误简化查询 | 按 helper 重新拆 service | `finance_scattered_service.py` | 汇总口径、树结构、对账结果、日期维度比对 |
| `RE-02` | `C2` | 已有较多 SQL/聚合逻辑，但运行时错误、Header 缺失、与原 helper 等价性未证实 | 先修已知 bug 与 Header，再按销售明细、报表、对账、分析四链做深比对；仅对不等价链路重构 | `revenue_service.py` | 3 组参数：空参、权限 Header、日期边界；同时确认运行时错误已清零 |
| `BG-02` | `C2` | BigData 报表直接复用错误 service | 逐条报表回迁 | `bigdata_service.py`、`bigdata_router.py` | 时间区间、车流、归属分析结构比对 |
| `AN-02` | `C2/C3` | Analysis 树/损益/固化/招商分析不对 | 按四条分析链回迁 | `analysis_service.py`、`batch_router_part2.py` | 树结构、固化结果、SABFI、招商报告比对 |
| `BS-01` | `C2` | 已复核 C# Helper，BusinessMan 表映射错，关系语义全错 | 先修表映射，再回迁关系逻辑 | `businessman_service.py` | 关系表、创建、删除、商品绑定结果验证 |
| `SU-01` | `C2` | Supplier 树、资质、历史都被模板化 | 分三段回迁 | `businessman_service.py`、`batch_router_part2.py` | 供应商树、资质数量、历史列表、OtherData |
| `SA-02` | `C2` | Sales 汇总/排行/纠错/刷新不对 | 按五条业务链回迁 | `verification_service.py`、`batch_router_part2.py` | 汇总、排行、账期快照、刷新副作用对比 |

## 6.4 B4 缺失路由补齐批

目标：

- 补齐原 C# 有、Python 没有的路由

进入条件：

- 对应模块的公共契约层已稳定

完成标准：

- 原 C# 路由在 Python 运行时能一一找到
- 补齐后马上进入 B5 验证

### B4 包清单

| 包ID | 接口是否正确 | 主要错误点 | 整改方法 | 主要文件范围 | 整改后验证 |
| --- | --- | --- | --- | --- | --- |
| `BM-03` | `C4` | Merchants 缺失 1 条 | 补 router/service/helper | `routers/eshang_api_main/merchants/*` | 下拉接口 3 组权限参数验证 |
| `CT-05` | `C4` | Contract 缺失 2 条 | 补列表/统计接口 | `contract_router.py`、`contract_service.py` | 年份集合、占比统计对比 |
| `FI-05` | `C4` | Invoice/Office 缺 12 条 | 先补缺路由，再补审批和转发细节 | `invoice_router.py`、`invoice_service.py`、Office 相关文件 | 票据信息、税目信息、Office 审批 3 组参数验证 |
| `BG-03` | `C4` | `BAYONETWARNING` 缺 3 条 | 补齐 detail/sync/delete | `bigdata_router.py`、`bigdata_service.py` | 列表-明细-同步-删除闭环验证 |
| `MP-03` | `C4` | MobilePay 缺 1 条 | 补纠偏接口 | `mobilepay_service.py` | 纠偏前后状态验证 |
| `AN-03` | `C4` | `SPCONTRIBUTION` 缺 4 条 | 补完整 CRUD，禁止接模板 | `analysis_service.py`、`batch_router_part2.py` | 4 条接口闭环验证 |
| `PI-02` | `C4` | Picture 缺 6 条 | 按文件保存/凭证读取/上传/批删四链补齐 | `picture_service.py`、Picture 路由文件 | 文件、HWS 图片、批删结果验证 |
| `VI-01` | `C4` | Video `EXTRANET` 缺 4 条 | 先补标准 CRUD | 新增 Video router/service | CRUD 四件套闭环验证 |
| `VI-02` | `C4` | Video `EXTRANETDETAIL` 缺 4 条 | 按模板补齐 | 新增 Video router/service | CRUD 四件套闭环验证 |
| `VI-03` | `C4` | Video `SHOPVIDEO` 缺 4 条 | 按模板补齐 | 新增 Video router/service | CRUD 四件套闭环验证 |
| `VI-04` | `C4` | Video 日志缺 2 条 | 先补 `SynchroVIDEOLOG`，再做 `GetVIDEOLOGList` 分支 | Video router/service | `Search_Type` 分支和日志写入验证 |
| `VI-05` | `C4` | Video 聚合缺 2 条 | 最后单独做复杂聚合 | Video router/service，相关 helper 映射 | 异常分支、IP 选择、文案拼接、商品明细验证 |

## 6.5 B5 动态验收批

目标：

- 把静态整改转成可证明的动态一致性

进入条件：

- B1-B4 的接口已经完成编码

完成标准：

- 每个整改包都有对比报告
- 至少 3 组参数全部通过

### B5 验收波次

| 波次 | 适用整改包 | 验证重点 | 输出物 |
| --- | --- | --- | --- |
| `V1` | `BM-01`、`CT-03`、`RE-01`、`RE-03`、`BG-01`、`AU-01`、`AN-01`、`BS-02` | 路由、方法、参数名、Header、响应包 | 契约一致性报告 |
| `V2` | `CT-01`、`FI-03`、`FI-04`、`MP-01`、`MP-02`、`AU-02`、`BS-03`、`SU-02`、`VE-01`、`VE-02`、`VE-03`、`VE-04`、`SA-01` | 状态机、审批流、删除语义、操作人、失败分支 | 流程一致性报告 |
| `V3` | `BM-02`、`CT-04`、`FI-01`、`FI-02`、`RE-02`、`BG-02`、`AN-02`、`BS-01`、`SU-01`、`SA-02` | 树、汇总、`OtherData`、报表、排序、分页 | 报表与汇总一致性报告 |
| `V4` | `CT-02`、`PI-01`、`PI-02`、`FI-05`、`VI-04`、`VI-05` | 文件、外部系统、上传、转发、日志、视频聚合 | 外部能力与文件链一致性报告 |
| `V5` | `BM-03`、`CT-05`、`BG-03`、`MP-03`、`AN-03`、`VI-01`、`VI-02`、`VI-03` | 缺失路由补齐后的闭环校验 | 缺失接口补齐报告 |

## 7. 每个整改包的标准执行卡

后续执行时，每个整改包都按下面模板落记录。

### 7.1 输入

- 包ID
- 接口清单
- 当前状态：`C1/C2/C3/C4/C5`
- 原 C# Controller 路径
- 原 C# Helper 路径
- 原 C# Model 路径
- 需要的表/视图/序列

### 7.2 产出

- 修改的 Python 文件清单
- 基准响应记录
- 3 组参数对比报告
- 是否通过
- 遇到的新问题

### 7.3 必填检查项

- [ ] 路由大小写一致
- [ ] HTTP 方法一致
- [ ] 参数名和参数类型一致
- [ ] Header 注入一致
- [ ] 返回包结构一致
- [ ] SQL / JOIN / 默认排序一致
- [ ] 默认分页一致
- [ ] 删除语义一致
- [ ] 副作用一致
- [ ] 3 组参数比对通过

## 8. 推荐执行顺序

建议按下面的固定顺序推进，不要跳批次：

1. `P0-01` 到 `P0-03`
2. `B1`
3. `B2`
4. `B3`
5. `B4`
6. `B5`

如果要并行，建议这样拆：

- 窗口 A：`B1`
- 窗口 B：`B2`
- 窗口 C：`B3`
- 窗口 D：`B4`
- 当前总控窗口：`B5` 和文档汇总

但同一模块内必须遵守依赖：

- 先契约，再流程
- 先流程，再汇总
- 先补路由，再联调

## 9. 完成定义

一个整改包只有满足下面全部条件，才能算完成：

- 包内接口已全部修改完成
- 已完成 SOP 步骤 1-6
- 3 组参数新旧对比全部通过
- 已更新整改矩阵状态
- 已更新工作日志和修改记录
- 如有新坑，已补入知识库

## 10. 文档更新要求

每完成一个整改包，必须同步更新：

- [full_audit_rectification_matrix_20260309.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_rectification_matrix_20260309.md)
- [full_audit_execution_plan_20260309.md](/E:/workfile/JAVA/NewAPI/docs/full_audit_execution_plan_20260309.md)
- [interface_migration_knowledge_base_20260309.md](/E:/workfile/JAVA/NewAPI/docs/interface_migration_knowledge_base_20260309.md)
- `docs/work_log_YYYYMMDD.md`
- `docs/change_log.md`

这样后续就不会再出现“知道有问题，但不知道做到哪儿了”的情况。
