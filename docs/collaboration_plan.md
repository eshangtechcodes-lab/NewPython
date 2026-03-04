# API 接口迁移 — 双人协同计划

> 两人协同迁移 EShangApi（C# → Python），以 Controller 文件夹为准，AutoBuild 不迁移。

## 迁移范围

**只迁移手动 Controller**，AutoBuild 是原项目代码生成器的产物，不需要平移。

### EShangApiMain — 53 个 Controller（排除 BaseController 基类）

| 模块 | Controller | 数量 |
|------|------------|------|
| **MainProject（核心框架）** | CommonController, DictionaryController, FrameWorkController, MainProjectController, PlatformController, InterfaceController, NoticeController, LogController, LoggingController, BusinessLogController, BusinessProcessController, CodeBuilderController | 12 |
| **BaseInfo（基础信息）** | BaseInfoController, BasicConfigController, CommodityController | 3 |
| **Contract（合同管理）** | ContractController, BusinessProjectController, ExpensesController, ContractSynController, CONTRACT_SYNController | 5 |
| **Finance（财务管理）** | FinanceController, InvoiceController, BudgetProjectAHController | 3 |
| **Merchants（商户管理）** | MerchantsController | 1 |
| **Revenue（收入管理）** | RevenueController | 1 |
| **Member（会员管理）** | MemberController | 1 |
| **Equipment（设备管理）** | EquipmentController | 1 |
| **BigData（大数据）** | BigDataController, CustomerController | 2 |
| **Order（订单管理）** | OnlineOrderController | 1 |
| **MobilePay（移动支付）** | MobilePayController | 1 |
| **Audit（审计）** | AuditController | 1 |
| **Analysis（分析）** | AnalysisController | 1 |
| **BusinessMan（招商）** | BusinessManController, SupplierController | 2 |
| **BID（招标）** | BIDController (×2) | 2 |
| **Evaluation（考核）** | EvaluationController | 1 |
| **Promotion（促销）** | PromotionController | 1 |
| **SaleStore（门店）** | SaleStoreController | 1 |
| **Seller（卖家）** | SellerController | 1 |
| **DataVerification（数据核验）** | VerificationController, SalesController | 2 |
| **SiteManage（场地管理）** | SiteManageController | 1 |
| **APPManage（APP管理）** | APPManageController | 1 |
| **Picture（图片管理）** | PictureController | 1 |
| **Video（视频管理）** | ShopVideoController | 1 |
| **SendRec（收发管理）** | SendRecController | 1 |
| **ThirdInterface（第三方接口）** | ThirdInterfaceController | 1 |
| **WeChatPay/Seller 等** | 其余 Controller | ~4 |

### CommercialApi — 14 个 Controller

| Controller | 说明 |
|------------|------|
| BaseInfoController | 基础信息 |
| RevenueController | 收入管理 |
| ContractController | 合同管理 |
| BigDataController | 大数据分析 |
| BudgetController | 预算管理 |
| ExamineController | 考核管理 |
| CustomerController | 客户管理 |
| BusinessProcessController | 业务审批 |
| CommonController | 公共方法 |
| AnalysisController | 数据分析 |
| AbnormalAuditController | 异常审计 |
| SuggestionController | 建议管理 |
| SupplyChainController | 供应链 |
| UserBehaviorController | 用户行为 |

---

## 分工原则

1. **按业务模块垂直切分**：一人负责一组完整的 Controller
2. **共享基础层**：`core/`、`models/base.py` 由角色 A 统一维护
3. **先串行后并行**：第一个 Controller（BaseInfo）两人一起做作为范例
4. **每个 Controller 对比验证后才算完成**

---

## 角色分配

### 角色 A：核心框架 + 业务模块（上半部分）

| 模块 | Controller 数 | 优先级 | 估时 |
|------|--------------|--------|------|
| MainProject（核心框架） | 12 | P0 | 4天 |
| Contract（合同管理） | 5 | P1 | 2天 |
| Finance（财务管理） | 3 | P1 | 1天 |
| Revenue（收入管理） | 1 | P2 | 0.5天 |
| Audit（审计） | 1 | P2 | 0.5天 |
| Evaluation（考核） | 1 | P3 | 0.5天 |
| DataVerification（数据核验） | 2 | P3 | 0.5天 |
| ThirdInterface（第三方接口） | 1 | P4 | 0.5天 |
| **小计** | **~26** | | **~9天** |

同时维护：`core/`、`config.py`、`main.py`、`models/base.py`

### 角色 B：基础信息 + 商户业务 + CommercialApi

| 模块 | Controller 数 | 优先级 | 估时 |
|------|--------------|--------|------|
| BaseInfo（基础信息） | 3 | P0 | 1天 |
| Merchants（商户管理） | 1 | P0 | 1天 |
| Member（会员管理） | 1 | P1 | 0.5天 |
| BusinessMan（招商） | 2 | P1 | 1天 |
| Equipment（设备管理） | 1 | P2 | 0.5天 |
| BigData + Analysis | 3 | P2 | 1天 |
| Order + MobilePay + 其余 | ~10 | P3 | 3天 |
| **CommercialApi 全部** | **14** | P4 | **4天** |
| **小计** | **~35** | | **~12天** |

---

## 执行阶段

### 阶段一：范例对齐（1-2天）

两人一起完成 `BaseInfoController` 中的 `GetBrandList` 接口完整迁移：
- 读原代码 → 调原 API → 实现 → 对比验证 → 全部 ✅
- 将此过程记录为范例文档，后续接口照此执行

### 阶段二：并行迁移 EShangApiMain（9-12天）

- A 从 MainProject 开始，B 从 BaseInfo + Merchants 开始
- 每完成一个 Controller，更新 `docs/migration_progress.md`
- 每天站会同步进度和问题

### 阶段三：CommercialApi 迁移（4天）

- B 负责全部 CommercialApi
- A 做接口互审

### 阶段四：集成测试（2-3天）

- 全量接口对比测试
- 性能基准测试

---

## Git 分支策略

```
main
├── feature/mainproject    ← A 负责
├── feature/contract       ← A 负责
├── feature/finance        ← A 负责
├── feature/baseinfo       ← B 负责
├── feature/merchants      ← B 负责
├── feature/commercial     ← B 负责
└── ...
```

---

## 文件分工约定

| 目录/文件 | A | B | 说明 |
|-----------|---|---|------|
| `core/` | ✏️ | 🔒 | 基础层由 A 维护 |
| `config.py` / `main.py` | ✏️ | 🔒 | 配置和路由注册由 A 管理 |
| `models/base.py` | ✏️ | 🔒 | 公共模型由 A 维护 |
| `routers/eshang_api_main/` 各子目录 | 各自负责 | 各自负责 | 按模块分工 |
| `routers/commercial_api/` | 🔒 | ✏️ | CommercialApi 由 B 维护 |
| `docs/` / `scripts/` | ✏️ | ✏️ | 双方都可更新 |

---

## 每日同步

1. 早上 10 分钟站会：昨天完成几个接口、遇到什么问题
2. 遇到通用问题：立即记录到 `docs/migration_issues.md` + 更新工作流
3. 下班前：推送代码 + 更新 `docs/migration_progress.md`
