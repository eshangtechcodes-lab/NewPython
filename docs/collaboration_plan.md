# API 接口迁移 — 双人协同计划

> 两人协同迁移 EShangApi（C# → Python），以 Controller 文件夹为准，AutoBuild 不迁移。

## 迁移范围

**只迁移手动 Controller**，AutoBuild 是原项目代码生成器的产物，不需要平移。

### EShangApiMain — 53 个 Controller（排除 BaseController 基类）

| 模块分类 | Controller | 数量 |
|----------|------------|------|
| **MainProject（核心框架）** | SystemController, LoggingController, BusinessController, DictionaryController, FrameWorkController, MainProjectController, CodeBuilderController 等 | 12 |
| **Contract（合同管理）** | ContractController, ContractMonthController, ContractIssueController, CONTRACT_SYNController 等 | 5 |
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
| **BID（招标）** | BIDController (x2) | 2 |
| **Evaluation（考核）** | EvaluationController | 1 |
| **Promotion（促销）** | PromotionController | 1 |
| **DataVerification（数据核验）** | DataVerificationController, DataVerificationOperationController | 2 |
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
| BaseInfoController | 服务区基础信息（片区、业态、门店数量、服务区列表等） |
| RevenueController | 服务区营收管理（日结、报表、收入统计） |
| ContractController | 合同管理（合同列表、合同明细、合同统计） |
| BigDataController | 大数据分析（流量、客流、热力图） |
| BudgetController | 预算管理（预算编制、执行、分析） |
| ExamineController | 考核管理（考核指标、评分、排名） |
| CustomerController | 客户管理（客户信息、画像、行为分析） |
| BusinessProcessController | 业务审批流程（工单、审批、流转） |
| CommonController | 公共方法（字符串加解密等通用工具） |
| AnalysisController | 数据分析（趋势分析、对比分析） |
| AbnormalAuditController | 异常审计（营收异常、日结异常检测） |
| SuggestionController | 建议管理（意见箱、反馈处理） |
| SupplyChainController | 供应链管理（采购、库存、供应商） |
| UserBehaviorController | 用户行为（操作日志、行为追踪） |

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
- 读原代码 → 调原 API → 实现 → 对比验证 → 全部通过
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

---

## 数据库同步策略

> Oracle（原库）→ 达梦 NEWPYTHON（新库），需要保证数据一致才能做接口对比验证。

### 阶段划分

```
[开发期] Oracle 为主库，达梦为镜像库 → 定期全量同步
[过渡期] 双库并行，新旧 API 共存 → 增量同步或双写
[上线后] 达梦为主库 → Oracle 停用
```

### 一、初始全量同步（开发前）

每个 Controller 涉及的表，在开发前必须确认已同步到达梦。

**操作流程**：

1. **梳理依赖表清单**：读取 Helper SQL，列出每个接口涉及的所有表（含 JOIN 表、字典表）
2. **确认达梦已有数据**：

```python
# scripts/check_dm_tables.py
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()
tables = ['T_BRAND', 'T_MERCHANTS', 'T_CONTRACT', ...]
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  OK {t:30s} {cur.fetchone()[0]:>8} 条")
    except:
        print(f"  NO {t:30s} 表不存在")
```

3. **缺失的表**：用达梦数据迁移工具（DTS）或手动导入

### 二、字段类型校验（每张表必做）

已知问题 P1：达梦导入工具可能将 NUMBER 列导为 VARCHAR。

**每张表迁移后必须执行**：

```python
# 对比 Oracle 和达梦的字段类型
# Oracle 侧
cur_ora.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, DATA_PRECISION, DATA_SCALE
    FROM ALL_TAB_COLUMNS
    WHERE OWNER='COOP_MERCHANT' AND TABLE_NAME='T_XXX'
    ORDER BY COLUMN_ID
""")
# 达梦侧
cur_dm.execute("""
    SELECT COLUMN_NAME, DATA_TYPE
    FROM USER_TAB_COLUMNS
    WHERE TABLE_NAME='T_XXX'
    ORDER BY COLUMN_ID
""")
```

**类型不一致时** 修改达梦列：

```sql
-- 示例：将 VARCHAR 改为 INT
ALTER TABLE T_BRAND MODIFY BRAND_ID INT;
ALTER TABLE T_BRAND MODIFY BRAND_PID INT;
ALTER TABLE T_BRAND MODIFY BRAND_CATEGORY INT;
-- 注意：有数据时需确保所有值能转为目标类型
```

### 三、开发期增量同步

开发期中 Oracle 仍然是生产库，数据会变化。两种方案选其一：

**方案 A：定期全量覆盖（推荐，简单可靠）**

- 每周一次全量重新导入（用达梦 DTS 工具）
- 适合：表数据量不大（万级以内），迁移窗口期短

**方案 B：增量同步（数据量大时）**

- 按 `OPERATE_DATE` 或主键 ID 范围增量同步
- 适合：大表（十万级以上），不希望每次全量
- 注意：需要原 Oracle 表有时间戳字段支持

### 四、表依赖关系记录

迁移每个 Controller 时，在 `docs/table_dependencies.md` 中记录该接口依赖的表：

| Controller | 接口 | 主表 | JOIN 表 | 字典表 |
|------------|------|------|---------|--------|
| BaseInfoController | GetSPRegionList | T_SERVERPARTTYPE | - | - |
| BaseInfoController | GetBusinessTradeList | T_AUTOSTATISTICS | T_AUTOSTATISTICS(自关联) | - |
| BaseInfoController | GetShopCountList | T_SHOPCOUNT | - | - |

### 五、切换上线检查清单

正式切换到达梦前的最终验证：

- [ ] 所有依赖表的数据量与 Oracle 一致
- [ ] 所有字段类型已校正（无 VARCHAR 冒充 INT 的情况）
- [ ] 序列（SEQUENCE）的当前值大于等于 Oracle 最大 ID
- [ ] 全部接口对比验证通过
- [ ] 写操作（INSERT/UPDATE/DELETE）在达梦端测试通过
- [ ] 事务和并发测试通过
