# 接口迁移知识库（2026-03-09）

## 1. 这份知识库的用途

这份文档用于沉淀这次全量审计形成的稳定知识，避免后续又回到“看路由是否存在”这种低质量判断。

后续可直接基于本知识库继续扩展：

- 模块知识卡
- 单接口知识卡
- 审计 checklist
- 动态联调基准

## 2. 当前项目的真实迁移目标

当前项目的目标不是“用 FastAPI 做一套功能相近的新接口”，而是：

- 保持原 C# 路由集合
- 保持原入参和 Header 语义
- 保持原响应包结构
- 保持原 helper 级业务逻辑
- 保持原 SQL、分页、排序、删除、副作用语义
- 最终让 Python 对外表现为原 C# 的兼容实现

所以：

- 只要契约变了，就不能算兼容迁移
- 只要 helper 语义被 generic CRUD 替代，就不能算逻辑等价
- 只要外部系统/文件系统/状态机被砍掉，就不能算完成

## 3. 迁移完成度的正确分级

后续所有模块和接口，都建议统一按下面 5 级打标：

- L0：未迁移
- L1：路由已注册
- L2：契约兼容
- L3：逻辑等价
- L4：通过动态比对验收

判定原则：

- L1 不能当作完成
- L2 也不能当作完成
- 只有 L3 才能说“静态上迁移完成”
- 只有 L4 才能说“可上线验收”

## 4. 本次审计识别出的 7 类高频反模式

### 4.1 通用 CRUD 壳化

表现：

- 原接口有独立 helper 和业务语义
- Python 统一变成 `list/detail/synchro/delete`

高发模块：

- Revenue
- Audit
- Analysis
- BusinessMan
- Supplier
- Sales
- BigData 部分实体

风险：

- 返回数据不代表语义正确
- `OtherData`、树形、汇总、审批状态全部容易丢

### 4.2 batch router 统一 `pk_val`

表现：

- 原详情/删除接口有各自实体参数名
- Python 被统一成 `pk_val`

风险：

- 契约直接不兼容
- 前端/调用方原参数名失效

### 4.3 小写通用响应包装

表现：

- Python 统一返回 `code/message/data`
- 原 C# 使用 `Result_Code/Result_Desc/Result_Data`

风险：

- 调用方兼容性破坏
- 模块间风格混杂

### 4.4 Header / Token / 上下文丢失

高发字段：

- `ProvinceCode`
- `ServerpartCodes`
- `ServerpartShopIds`
- `UserPattern`
- `Token`
- `ModuleGuid`
- `SourcePlatform`
- `GetFromRedis`

风险：

- 权限越界
- 操作人丢失
- 缓存/实时分支失效
- 审批和统计口径漂移

### 4.5 占位实现误判为完成

识别信号：

- 注释写“简化版”
- 直接 `return []`
- 直接 `return True`
- 直接 `return {}`
- 直接 `return {"status":"ok"}`

这类接口应统一判定为：

- 未迁移完成

### 4.6 外部系统 / 文件系统被抹平

高发场景：

- 图片上传/删除
- 合同附件
- 航信 / 金蝶
- MobilePay / ChinaUMS
- 视频聚合

风险：

- 本地表看起来有数据，但原系统副作用完全没发生

### 4.7 用 Python 多出接口冲抵缺失接口

典型案例：

- `Picture` 模块新增了 `GetPictureDetail/GetPictureCount/...`
- 但原 `SaveImgFile/GetEndaccountEvidence/...` 仍缺失

原则：

- Python 多出接口不计入原模块迁移完成度

## 5. 各模块的关键业务语义

### BaseInfo

关键点：

- 强依赖 `ProvinceCode`、`ServerpartCodes`、`ServerpartShopIds`、`UserPattern`
- 列表、树和绑定关系接口容易出现权限回填缺失
- `ServerpartShop`、`USERDEFINEDTYPE`、`PROPERTYASSETS` 不是简单单表 CRUD

### Merchants

关键点：

- 省份权限是核心
- `GetCoopMerchants*` 系列不能漏 `ProvinceCode`

### Contract

关键点：

- `RegisterCompact` 系列依赖 Token、历史备份、删除校验、变更日志
- 多个接口依赖 `GetFromRedis`
- `BusinessProject` 相关接口重度依赖 `summaryObject`、审批状态、多表 JOIN
- 附件接口依赖真实文件系统

### Finance

关键点：

- 报表、审批、固化、生成、重算、补录都不是普通查询
- 很多接口本质上是流程接口，不是 CRUD
- 发票模块还涉及航信/金蝶语义

### Revenue

关键点：

- 大量实体接口必须保留各自 helper
- `OtherData`、分析模型、对账、同比环比很关键
- 不能用统一 CRUD 替代 7 组实体

### BigData

关键点：

- 原接口返回的是特定模型，不是通用壳
- `Customer` 相关仍依赖 Header 权限
- `BAYONETWARNING` 需要单独补齐

### MobilePay

关键点：

- 不应以本地表查询替代 `MobilePayHelper` / `ChinaUmsSubHelper`
- 提现、分润、银行对账都带外部系统语义

### Audit

关键点：

- 报表、任务下发、说明上传都不是单表 CRUD
- `GetAuditDetils`、`IssueAuditTasks`、`UpLoadAuditExplain` 都是高复杂度接口

### Analysis

关键点：

- 分析、固化、重算、报表接口远重于普通 CRUD
- `SPCONTRIBUTION` 缺失必须单独跟踪

### BusinessMan

关键点：

- 原业务重点是关系、授权、用户树，不是 `T_BUSINESSMAN` 单表
- 表映射一旦错，整个模块都会“看起来能跑，实际语义全错”

### Supplier

关键点：

- 树、资质、关联关系是核心
- 不能用额外暴露的删除路由掩盖主逻辑缺失

### Verification

关键点：

- 这是状态机模块，不是表维护模块
- 审核、提交、作废、冲正、重建都必须保留原状态迁移和错误返回

### Sales

关键点：

- 汇总、排行、纠错、批量刷新是核心
- `DeleteCOMMODITYSALE` 还存在“原系统实际不可删”的语义风险

### Picture

关键点：

- 这是文件/凭证中心，不是 `T_PICTURE` 管理中心
- 依赖目录映射、物理文件、业务表、HWS 图片表、副作用调用

### Video

关键点：

- 前 12 条可按 CRUD 模板迁移
- `GetVIDEOLOGList`、`GetShopVideoInfo`、`GetYSShopVideoInfo` 必须当复杂聚合接口处理

## 6. 后续审计的标准 Checklist

后面每做一个接口，都建议至少检查这 10 项：

1. 路由名是否与原 C# 完全一致
2. HTTP 方法是否一致
3. 参数名、参数类型、是否支持 GET/POST 双入口是否一致
4. Header 注入是否完整
5. 返回包结构是否一致
6. 是否保留原 helper 的业务语义，而不是 generic CRUD
7. 分页、排序、`OtherData/summaryObject` 是否一致
8. 删除语义是否一致
9. 是否涉及文件系统、外部系统、缓存分支、审批状态机
10. 是否已做新旧接口 3 组参数动态比对

## 7. 后续知识沉淀建议

后续建议继续按两层沉淀：

### 第一层：模块知识卡

每个模块固定记录：

- 原 C# controller 列表
- Python router/service 对应关系
- 关键 Header
- 关键 helper
- 高风险接口
- 已知差异
- 验收样例

### 第二层：单接口知识卡

每个接口固定记录：

- 原路由
- C# controller 方法
- C# helper 方法
- Python router 方法
- Python service 方法
- 当前状态（L0-L4）
- 已知差异
- 修复计划
- 对比样例

## 8. 建议保留的后续文档结构

建议后续在 `docs` 下逐步形成：

- 总控文档：整改总报告
- 知识库：本文件
- 模块知识卡：每模块一份
- 动态比对报告：按批次输出
- 迁移状态表：按 L0-L4 跟踪

## 9. 这次审计后不应再使用的判断方式

以下判断方式后续应停止使用：

- “路由在，就算完成”
- “能查到数据，就算一致”
- “先返回空列表，后面再补”
- “新增了几个 Python 接口，可以抵掉缺失接口”
- “统一 CRUD 模板先跑通，后面再看”

这些做法已经被证明会显著抬高返工成本。

## 10. 当前最有价值的下一步

从知识保留和实施效率看，最有价值的下一步不是继续统计“完成率”，而是：

- 先把迁移状态表切到 L0-L4
- 先修公共契约层
- 先下掉所有占位实现的“已完成”标签
- 再按模块补 helper 级逻辑
- 最后做动态对比验收

这套顺序能最大程度减少重复返工。
