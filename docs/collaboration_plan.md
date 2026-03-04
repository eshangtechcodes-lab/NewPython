# API 接口迁移 — 实施计划

> EShangApi C# → Python FastAPI 接口迁移，以 Controller 文件夹为准，AutoBuild 不迁移。

## 迁移范围（精确统计）

**只迁移手动 Controller**，数据来自 C# 原项目 `[Route()]` 注解实际扫描。

### 已完成

| 模块 | Controller | 接口 | 数据量 | 状态 |
|------|-----------|------|--------|------|
| BaseInfo | BaseInfoController | OWNERUNIT 4 接口 | 592条/18字段 | ✅ |
| BaseInfo | BaseInfoController | SERVERPART 2 接口 | 1168条/42字段 | ✅ |
| BaseInfo | BaseInfoController | ServerpartShop 5 接口 | 7078条/54字段 | ✅ |
| BaseInfo | BaseInfoController | Brand 6 接口 | 2005条/21字段 | ✅ |
| BaseInfo | BaseInfoController | RTSERVERPARTSHOP 4 接口 | 3441条/23字段 | ✅ |
| BaseInfo | BaseInfoController | SERVERPARTSHOP_LOG 1 接口 | 4933条/23字段 | ✅ |
| BaseInfo | BaseInfoController | CASHWORKER 4 接口 | 9360条/22字段 | ✅ |

### 待迁移（24 Controller / ~551 路由）

| # | 模块 | Controller | 路由数 | 复杂度 | 优先级 | 阶段 |
|---|------|-----------|--------|--------|--------|------|
| 1 | **BaseInfo（基础信息）** | BaseInfoController | **99** | 🔴高 | P0 | 一 |
| 2 | | BasicConfigController | **29** | 🟡中 | P0 | 一 |
| 3 | | CommodityController | **17** | 🟡中 | P0 | 一 |
| 4 | **Merchants（商户管理）** | MerchantsController | **16** | 🟡中 | P0 | 二 |
| 5 | **Contract（合同管理）** | ContractController | **27** | 🟡中 | P1 | 三 |
| 6 | | BusinessProjectController | **87** | 🔴高 | P1 | 三 |
| 7 | | ExpensesController | **10** | 🟢低 | P1 | 三 |
| 8 | | ContractSynController | **4** | 🟢低 | P1 | 三 |
| 9 | | CONTRACT_SYNController | **4** | 🟢低 | P1 | 三 |
| 10 | **Finance（财务管理）** | FinanceController | **48** | 🔴高 | P1 | 四 |
| 11 | | InvoiceController | **24** | 🟡中 | P1 | 四 |
| 12 | | BudgetProjectAHController | **16** | 🟡中 | P2 | 四 |
| 13 | **Revenue（收入管理）** | RevenueController | **60** | 🔴高 | P2 | 五 |
| 14 | **BigData（大数据）** | BigDataController | **36** | 🔴高 | P2 | 六 |
| 15 | | CustomerController | **4** | 🟢低 | P2 | 六 |
| 16 | **MobilePay（移动支付）** | MobilePayController | **18** | 🟡中 | P3 | 七 |
| 17 | **Audit（审计）** | AuditController | **24** | 🟡中 | P3 | 七 |
| 18 | **Analysis（分析）** | AnalysisController | **62** | 🔴高 | P3 | 七 |
| 19 | **BusinessMan（招商）** | BusinessManController | **26** | 🟡中 | P3 | 七 |
| 20 | | SupplierController | **13** | 🟡中 | P3 | 七 |
| 21 | **DataVerification（数据核验）** | VerificationController | **23** | 🟡中 | P3 | 七 |
| 22 | | SalesController | **13** | 🟡中 | P3 | 七 |
| 23 | **Picture（图片管理）** | PictureController | **9** | 🟢低 | P4 | 八 |
| 24 | **Video（视频管理）** | ShopVideoController | **16** | 🟡中 | P4 | 八 |

---

## 实施阶段

### 阶段一：BaseInfo 基础信息补全（P0，预计 3-5 天）

完成 BaseInfo 全部 3 个 Controller 的迁移。BaseInfoController 的 99 个路由按实体分组，每组通常是 CRUD 四件套。

| 批次 | 内容 | 状态 |
|------|------|------|
| B1 | OWNERUNIT (4 接口) | ✅ 已完成 |
| B2 | SERVERPART (2 接口) | ✅ 已完成 |
| B3 | ServerpartShop (5 接口) | ✅ 已完成 |
| B4 | Brand (6 接口) | ✅ 已完成 |
| B5.1 | RTSERVERPARTSHOP, SERVERPARTSHOP_LOG, CASHWORKER (9 接口) | ✅ 已完成 |
| B5.2 | BaseInfoController 剩余其余接口 (~73 接口) | ⬜ |
| B6 | BasicConfigController (29 接口) | ⬜ |
| B7 | CommodityController (17 接口) | ⬜ |

### 阶段二：Merchants 商户管理（P0，预计 1 天）

MerchantsController 16 个路由：CoopMerchants CRUD、类型、联系人、关联查询。

### 阶段三：Contract 合同管理（P1，预计 4-5 天）

⚠️ BusinessProjectController 有 87 个路由，按子功能分批推进。

| Controller | 路由数 |
|------------|--------|
| ContractController | 27 |
| BusinessProjectController | 87 |
| ExpensesController | 10 |
| ContractSynController | 4 |
| CONTRACT_SYNController | 4 |

### 阶段四：Finance 财务管理（P1-P2，预计 3-4 天）

| Controller | 路由数 |
|------------|--------|
| FinanceController | 48 |
| InvoiceController | 24 |
| BudgetProjectAHController | 16 |

### 阶段五：Revenue 收入管理（P2，预计 2-3 天）

RevenueController 60 个路由：7 组 CRUD + 报表/银行/同环比分析。

### 阶段六：BigData 大数据（P2，预计 1-2 天）

BigDataController (36) + CustomerController (4)。

### 阶段七：中型模块批量迁移（P3，预计 5-7 天）

⚠️ AnalysisController 有 62 个路由。

| Controller | 路由数 |
|------------|--------|
| MobilePayController | 18 |
| AuditController | 24 |
| AnalysisController | 62 |
| BusinessManController | 26 |
| SupplierController | 13 |
| VerificationController | 23 |
| SalesController | 13 |

### 阶段八：轻量模块收尾（P4，预计 1 天）

PictureController (9) + ShopVideoController (16)。

---

## 工作量预估

| 阶段 | 接口数 | 预计天数 | 累计 |
|------|--------|---------|------|
| 一（BaseInfo） | ~139 | 3-5 | 3-5 |
| 二（Merchants） | 16 | 1 | 4-6 |
| 三（Contract） | 132 | 4-5 | 8-11 |
| 四（Finance） | 88 | 3-4 | 11-15 |
| 五（Revenue） | 60 | 2-3 | 13-18 |
| 六（BigData） | 40 | 1-2 | 14-20 |
| 七（中型模块） | 179 | 5-7 | 19-27 |
| 八（轻量收尾） | 25 | 1 | 20-28 |
| **总计** | **~551** | **20-28天** | |

---

## 执行流程

每个接口严格遵循 `/api-migration` 工作流 6 步法：

1. 读原 C# Controller → Helper → Model
2. 调原 API 获取基准数据
3. 同步数据库表（Oracle → 达梦）
4. 实现 Python 接口（Model → Service → Router）
5. 对比验证（compare_api.py）
6. 问题标注（更新 migration_issues.md + 工作流）

---

## 数据库同步策略

> Oracle（原库）→ 达梦 NEWPYTHON（新库），需要保证数据一致才能做接口对比验证。

### 阶段划分

```
[开发期] Oracle 为主库，达梦为镜像库 → 定期全量同步
[过渡期] 双库并行，新老 API 共存 → 增量同步或双写
[上线后] 达梦为主库 → Oracle 停用
```

### 一、初始全量同步（开发前）

每个 Controller 涉及的表，在开发前必须确认已同步到达梦。

**操作流程**：

1. **梳理依赖表清单**：读原 Helper SQL，列出每个接口涉及的所有表（含 JOIN 表、字典表）
2. **确认达梦已有数据**：

```python
# scripts/check_dm_tables.py
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()
# 检查所有需要的表是否存在及数据量
tables = ['T_BRAND', 'T_MERCHANTS', 'T_CONTRACT', ...]  # 按需补充
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  ✅ {t:30s} {cur.fetchone()[0]:>8} 条")
    except:
        print(f"  ❌ {t:30s} 表不存在")
```

3. **缺失的表**：用达梦数据迁移工具（DTS）或手动导入

### 二、字段类型校验（每张表必做）

已知问题 P1：达梦导入工具可能将 NUMBER 列导为 VARCHAR。

**每张表迁移后必须执行**：

```python
# 对比 Oracle 和达梦的字段类型
# Oracle 端
cur_ora.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, DATA_PRECISION, DATA_SCALE 
    FROM ALL_TAB_COLUMNS 
    WHERE OWNER='COOP_MERCHANT' AND TABLE_NAME='T_XXX' 
    ORDER BY COLUMN_ID
""")
# 达梦端
cur_dm.execute("""
    SELECT COLUMN_NAME, DATA_TYPE 
    FROM USER_TAB_COLUMNS 
    WHERE TABLE_NAME='T_XXX' 
    ORDER BY COLUMN_ID
""")
```

**类型不一致时**修改达梦列：

```sql
-- 示例：将 VARCHAR 改为 INT
ALTER TABLE T_BRAND MODIFY BRAND_ID INT;
ALTER TABLE T_BRAND MODIFY BRAND_PID INT;
ALTER TABLE T_BRAND MODIFY BRAND_CATEGORY INT;
-- 注意：有数据时需确保所有值能转为目标类型
```

### 三、开发期增量同步

开发期间 Oracle 仍然是生产库，数据会变化。两种方案选其一：

**方案 A：定期全量覆盖（推荐，简单可靠）**

- 每周一次全量重新导入（用达梦 DTS 工具）
- 适合：表数据量不大（万级以内），迁移窗口期短
- 脚本：`scripts/sync_full.py`

**方案 B：增量同步（数据量大时）**

- 按 `OPERATE_DATE` 或主键 ID 范围增量同步
- 适合：大表（十万级以上），不希望每次全量
- 脚本：`scripts/sync_incremental.py`
- 注意：需要原 Oracle 表有时间戳字段支持

### 四、表依赖关系记录

迁移每个 Controller 时，在 `docs/table_dependencies.md` 中记录该接口依赖的表：

```markdown
| Controller | 接口 | 主表 | JOIN 表 | 字典表 |
|------------|------|------|---------|--------|
| BaseInfoController | GetBrandList | T_BRAND | T_MERCHANTS, T_SERVERPART | T_BUSINESSTRADE |
| ContractController | GetContractList | T_CONTRACT | T_MERCHANTS, T_SERVERPART | T_CONTRACTTYPE |
```

这样可以：
- 快速知道迁移某个接口前需要同步哪些表
- 确保关联表都已导入达梦
- 排查数据不一致时精确定位

### 五、切换上线检查清单

正式切换到达梦前的最终验证：

- [ ] 所有依赖表的数据量与 Oracle 一致
- [ ] 所有字段类型已校正（无 VARCHAR 冒充 INT 的情况）
- [ ] 序列（SEQUENCE）的当前值 ≥ Oracle 最大 ID
- [ ] 全部接口对比验证通过
- [ ] 写操作（INSERT/UPDATE/DELETE）在达梦端测试通过
- [ ] 事务和并发测试通过

