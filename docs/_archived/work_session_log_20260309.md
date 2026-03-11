# 整改工作日志 & 接口知识 — 2026-03-09

> 本文件为本次整改会话的完整记录，供后续会话接续使用
> 关联文件：`rectification_progress.md`（进度跟踪）、`rectification_implementation_plan_20260309.md`（实施方案）

---

## 一、本次会话完成工作（B1 + B2 全部完成）

### B1 公共契约层止血（10/10 ✅）

| 整改包 | 文件 | 改动内容 |
|--------|------|----------|
| RE-02 | `services/revenue/revenue_service.py` L227,259 | 修复 `params` 未定义运行时错误 |
| RE-01 | `routers/eshang_api_main/revenue/` | 7 组 CRUD 已用 Result + 实体专属参数名，无需修改 |
| AU-01 | `routers/.../batch_router_part1.py` | Audit 24 + MobilePay 17 = 41 接口响应格式统一 Result |
| AN-01 | `routers/.../batch_router_part2.py` | Analysis 58 接口 pk_val→{Entity}Id（Query alias） |
| BS-02 | `routers/.../batch_router_part2.py` | BusinessMan 39 接口 pk_val→{Entity}Id（Query alias） |
| BG-01 | `routers/.../bigdata_router.py` | 8 个散装接口响应格式统一 |
| CT-03 | `routers/.../contract/contract_router.py` | GetFromRedis 参数声明 |
| BM-01 | 多个 router | Header 注入（ServerpartCodes/Token/UserPattern） |
| SU-03 | `batch_router_part2.py` | DeleteQUALIFICATION_HIS 标注为多出路由 |
| PI-03 | `batch_router_part2.py` | Picture 多出 6 条已记录 |

### B2 P0 占位清理 + 契约兼容（16/16 ✅）

#### 第一梯队：占位实现

| 模块 | 文件 | 函数 | 改动 |
|------|------|------|------|
| Verification | `services/verification/verification_service.py` | `get_supp_endaccount_list` | 完整查询实现（T_ENDACCOUNT WHERE OPERATE_TYPE=1010，分页/排序/过滤） |
| BusinessMan | `services/businessman/businessman_service.py` | `relate_business_commodity` | 更新 T_COMMODITY_BUSINESS + 插入 T_RELATIONTABLES |
| Router | `routers/.../batch_router_part2.py` | `GetSuppEndaccountList` | 补全 9 个参数（ServerpartIds/Code/ShopCode/Date/State/Page/Sort） |
| Audit | `services/audit/audit_service.py` | `get_special_behavior_report` | 标注：C# 无实现（前端预留） |
| Audit | `services/audit/audit_service.py` | `get_abnormal_rate_report` | 标注：C# 无实现（前端预留） |
| MobilePay | `services/mobilepay/mobilepay_service.py` | `royalty_withdraw` | 标注：依赖外部支付通道 API（B3） |
| MobilePay | `services/mobilepay/mobilepay_service.py` | `get_mobilepay_royalty_report` | 标注：依赖银联分账 API（B3） |
| Analysis | `services/analysis/analysis_service.py` | `get_revenue_estimate_list` | 标注：B3 深逻辑（C# 有复杂预估算法） |

#### 审核通过（无真占位的模块）

| 模块 | 文件 | 行数 | 结论 |
|------|------|------|------|
| Contract | `services/contract/contract_service.py` | 935 行 | 完整实现 |
| Picture | `services/picture/picture_service.py` | 112 行 | 完整实现 |
| Invoice | `services/finance/invoice_service.py` | 660 行 | 完整实现（含 JDPJ/航行/金蝶转发） |
| Budget | `services/finance/budget_service.py` | 435 行 | 完整实现（含月度透视报表） |
| Finance散装 | `services/finance/finance_scattered_service.py` | 615 行 | 20 个有 SQL，14 个"简化版"审批属 B3 |
| Revenue | `services/revenue/revenue_service.py` | 2836 行 | 完整实现，RE-02 params 已修 |
| Analysis | `services/analysis/analysis_service.py` | 204 行 | 仅 1 个 B3 占位已标注 |

#### 第二梯队：契约兼容

| 整改包 | 改动 |
|--------|------|
| **BS-01** | `businessman_service.py` ENTITIES 表映射：`T_BUSINESSMAN`→`T_OWNERUNIT`，`BUSINESSMAN_ID`→`OWNERUNIT_ID`，`BUSINESSMAN_STATE`→`OWNERUNIT_STATE`；`BUSINESSMANDETAIL`同理；`create_businessman` 和 `get_user_list` 中硬编码表名同步修正 |
| **CT-03** | `contract_router.py` 4 个汇总接口透传 `GetFromRedis` 参数到 `contract_service.py`（get_project_summary_info/get_contract_expired_info/get_project_yearly_arrearage/get_project_monthly_arrearage） |
| **AN-01/BS-02/AU-01** | 确认 B1 已完成 |
| **BM-01** | 确认已在 Contract/BaseInfo/BusinessProject 等模块单独实现 Header/Token 读取 |

---

## 二、关键接口知识（C#↔Python 映射）

### 表名映射差异（已修复）

| C# ORM 实体 | C# 实际表名 | Python 原错误表名 | 已修正为 |
|-------------|-------------|------------------|----------|
| `Business.OWNERUNIT` | `COOP_MERCHANT.T_OWNERUNIT` | `T_BUSINESSMAN` | `T_OWNERUNIT` ✅ |
| `Business.OWNERUNITDETAIL` | `T_OWNERUNITDETAIL` | `T_BUSINESSMANDETAIL` | `T_OWNERUNITDETAIL` ✅ |

### BusinessMan CRUD 字段映射

| C# 字段 | 用途 |
|---------|------|
| `OWNERUNIT_ID` | 主键（商户内码） |
| `OWNERUNIT_NAME` | 商户名称 |
| `OWNERUNIT_EN` | 业主简称 |
| `OWNERUNIT_NATURE` | 商户性质（1000=管理单位，2000=经营单位） |
| `OWNERUNIT_STATE` | 有效状态（0=删除） |
| `OWNERUNIT_PID` | 父级内码 |
| `OWNERUNIT_GUID` | 标识 |
| `PROVINCE_CODE` | 省份标识 |
| `ISSUPPORTPOINT` | 是否支持积分 |

### GetUserList 逻辑（C# L528-691）

- 查 `COOP_MERCHANT.T_OWNERUNIT`（OWNERUNIT_NATURE=2000 经营单位）
- JOIN `PLATFORM_FRAMEWORK.T_USERAUTHORITY` + `HIGHWAY_STORAGE.T_SERVERPARTSHOP`
- 返回嵌套树：经营商户 → 用户 → 门店权限
- Python 当前简化为仅查 T_OWNERUNIT 列表（B3 深逻辑待完善）

### Contract GetFromRedis 双路径

- C# 中 `GetFromRedis=true` → 从**缓存表**读取汇总数据
- `GetFromRedis=false` → **实时计算**
- Python 当前仅实现实时计算路径，参数已透传备用

### Finance 简化版函数清单（14 个待 B3 深逻辑）

| 函数 | C# 行数 | 复杂度 |
|------|---------|--------|
| `get_revenue_recognition` | 2000+ 行 | 极高（分账/收银/收入确认） |
| `get_month_account_diff` | ~300 行 | 高（累计营业额差异对比） |
| `get_contract_excute_analysis` | ~500 行 | 高（合同执行情况一览） |
| `get_annual_account_list` | ~400 行 | 高（年度结算汇总） |
| `approve_*` 系列 (6个) | 各 100-300 行 | 中（审批状态流转） |
| `solid_*` 系列 (4个) | 各 200-500 行 | 高（固化/重算逻辑） |

### 外部 API 依赖（B3 范畴）

| 函数 | 依赖 |
|------|------|
| `royalty_withdraw` | 银联/客无忧支付通道 HTTP API |
| `get_mobilepay_royalty_report` | 银联分账 API |
| `send_hx_invoice_info` | 航行 SOAP WebService（WSDL） |

---

## 三、当前总进度

| 阶段 | 数量 | 状态 | 说明 |
|------|------|------|------|
| **B1 公共契约** | 10/10 | ✅ 100% | 响应格式、参数名、运行时错误 |
| **B2 占位+契约** | 16/16 | ✅ 100% | 占位清理、表映射、参数透传 |
| **B3 深逻辑** | 0/9 | ⬜ 0% | 需要逐函数翻译 C# 业务逻辑 |
| **B4 缺失路由** | 0/12 | ⬜ 0% | 需要新建 service + router |

---

## 四、后续任务清单

### B3 深逻辑回迁（9 个包，优先级从高到低）

| 窗口 | 整改包 | 模块 | 具体内容 | 预估工作量 |
|------|--------|------|----------|-----------|
| W1 | CT-04 | Contract | BusinessProject 审批状态、summaryObject 汇总 | 中 |
| W1 | BM-02 | BaseInfo | Commodity 控制器深逻辑（加密接口除外） | 中 |
| W2 | RE-02 | Revenue | 销售明细/收入报表/对账/分析四链核对 | 高 |
| W2 | FI-02 | Finance | 14 个简化版函数：审批流、固化、重算（2000+ 行 C#） | 极高 |
| W2 | BG-02 | BigData | 报表逐条回迁 | 中 |
| W3 | AN-02 | Analysis | 树形/固化/报表分四链回迁 | 高 |
| W3 | BS-01 | BusinessMan | OWNERUNIT 表已修正，GetUserList 嵌套树待完善 | 中 |
| W3 | SU-01 | Supplier | 供应商树/资质分三段回迁 | 中 |
| W3 | SA-02 | Sales | 6 个复用同一查询的接口拆为独立实现 | 中 |

### B4 缺失路由补齐（12 个包，共约 45 条路由）

| 窗口 | 整改包 | 数量 | 具体内容 |
|------|--------|------|----------|
| W4 | VI-01~05 | 16 条 | Video 全模块（EXTRANET/EXTRANETDETAIL/SHOPVIDEO/VIDEOLOG/散装） |
| W4 | PI-02 | 6 条 | Picture 原路由重建 |
| W2 | FI-05 | 12 条 | Finance Invoice/Office 缺失路由 |
| W2 | BG-03 | 3 条 | BigData BAYONETWARNING |
| W2 | MP-03 | 1 条 | MobilePay 缺失路由 |
| W3 | AN-03 | 4 条 | Analysis SPCONTRIBUTION |
| W1 | CT-05 | 2 条 | Contract 缺失路由 |
| W1 | BM-03 | 1 条 | Merchants 缺失路由 |

### 建议执行顺序

```
1. B4-VI（Video 16 条路由）— 纯新增，风险最低
2. B4 其他路由补齐 — 同上
3. B3-SA-02（Sales 拆分）— 工作量小
4. B3-BS-01（BusinessMan GetUserList 完善）— 已有基础
5. B3-CT-04 / BM-02 — 中等工作量
6. B3-AN-02 / SU-01 — 需要深度翻译
7. B3-RE-02 / BG-02 — 报表类
8. B3-FI-02 — 最复杂（2000+ 行审批流/固化逻辑），最后处理
```

---

## 五、关键文件索引

| 文件 | 用途 |
|------|------|
| `docs/rectification_progress.md` | 整改进度跟踪（实时更新） |
| `docs/rectification_implementation_plan_20260309.md` | 综合实施方案（B1-B4 方案详述） |
| `docs/full_audit_rectification_matrix_20260309.md` | Codex 审计整改矩阵（接口级台账） |
| `docs/full_audit_execution_plan_20260309.md` | B1-B5 执行方案 |
| `docs/interface_migration_knowledge_base_20260309.md` | 迁移知识库（7类反模式、10项 checklist） |
| `docs/collaboration_plan.md` | 主协作计划（631/645 接口进度） |
| `docs/work_session_log_20260309.md` | 本文件 |
