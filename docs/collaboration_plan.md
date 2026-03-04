# API 接口迁移 — 双人协同计划

> 两人协同迁移 EShangApi（C# → Python），按模块分工 + 接口互审。

## 分工原则

1. **按模块纵向切分**：一人负责一个完整模块（Controller + Helper + Model），避免交叉修改同一文件
2. **共享基础层**：`core/`、`models/base.py`、`models/common_model.py` 由一人统一维护，另一人只使用不修改
3. **先串行后并行**：第一个接口（GetBrandList）两人一起完成作为范例，之后并行各做各的模块
4. **接口互审**：每完成一个接口，对方进行 Code Review + 调用原 API 对比验证

---

## 角色定义

### 角色 A：框架维护 + EShangApiMain 迁移

负责范围：
- `core/` 基础层维护（database.py、aes_util.py 等）
- `models/base.py`、`models/common_model.py` 公共模型
- `middleware/` 中间件
- `main.py` 路由注册
- **EShangApiMain** 的手动 Controller 迁移（合同/财务/招商/设备/审计等复杂业务模块）

### 角色 B：AutoBuild 层 + CommercialApi 迁移

负责范围：
- `models/auto_build/` 所有自动生成的模型
- `services/auto_build/` 所有自动生成的服务
- `routers/eshang_api_main/auto_build/` AutoBuild 路由
- **CommercialApi** 全部接口（收入/大数据/预算/考核等）

---

## 执行计划

### 阶段一：协同完善范例（1-2天）

两人一起完善 GetBrandList 接口，将其作为后续所有迁移的标准范例：

| 任务 | 负责人 | 产出 |
|------|--------|------|
| 读原 BRANDController + BRANDHelper 代码 | A+B | 完整 SQL、字段列表 |
| 补齐 7 个关联字段 | A | brand_service.py 完善 |
| 修正达梦字段类型 | B | ALTER TABLE 脚本 |
| 对比验证全部 ✅ | A+B | compare_result.txt |
| 编写范例文档 | A | docs/example_migration.md |

### 阶段二：并行迁移 AutoBuild（5-7天）

B 负责 AutoBuild 层（约 100 个表的 CRUD），A 同时开始手动 Controller。

**角色 B 的工作清单**（AutoBuild 按优先级排序）：

| 优先级 | 模块 | 表数量 | 估时 |
|--------|------|--------|------|
| P0 | 基础信息（BaseInfo） | ~20 表 | 2天 |
| P1 | 合同相关（Contract） | ~15 表 | 1天 |
| P2 | 财务相关（Finance） | ~10 表 | 1天 |
| P3 | 设备相关（Equipment） | ~10 表 | 1天 |
| P4 | 其余 AutoBuild 表 | ~45 表 | 2天 |

**角色 A 的工作清单**（手动 Controller 按依赖排序）：

| 优先级 | 模块 | 接口数 | 估时 |
|--------|------|--------|------|
| P0 | GeneralMethod（通用方法）| ~30 | 3天 |
| P1 | 合同管理 | ~25 | 2天 |
| P2 | 财务管理 | ~20 | 2天 |
| P3 | 招商管理 | ~15 | 1天 |
| P4 | 其余模块 | ~60 | 4天 |

### 阶段三：CommercialApi 迁移（3-5天）

角色 B 负责，A 做接口互审。

### 阶段四：集成测试（2-3天）

两人共同完成全量接口对比测试。

---

## Git 分支策略

```
main
├── feature/autobuild-baseinfo      ← B 负责
├── feature/autobuild-contract      ← B 负责
├── feature/manual-general-method   ← A 负责
├── feature/manual-contract         ← A 负责
├── feature/commercial-api          ← B 负责
└── ...
```

- 每个模块一个分支
- 完成 + 互审通过后合并到 main
- **绝不同时修改同一个文件**（公共层由 A 统一修改）

---

## 每日同步机制

1. **早上 10 分钟站会**：各自汇报昨天完成了几个接口、遇到了什么问题
2. **遇到新的通用问题**：立即记录到 `docs/migration_issues.md` 并通知对方
3. **下班前**：各自推送代码、更新 `docs/migration_progress.md` 进度表

---

## 文件分工约定（避免冲突）

| 目录/文件 | 角色 A | 角色 B | 说明 |
|-----------|--------|--------|------|
| `core/` | ✏️ 可修改 | 🔒 只读 | 基础层由 A 维护 |
| `models/base.py` | ✏️ | 🔒 | 公共模型由 A 维护 |
| `models/auto_build/` | 🔒 | ✏️ | AutoBuild 模型由 B 维护 |
| `services/auto_build/` | 🔒 | ✏️ | AutoBuild 服务由 B 维护 |
| `routers/.../auto_build/` | 🔒 | ✏️ | AutoBuild 路由由 B 维护 |
| `routers/.../manual/` | ✏️ | 🔒 | 手动路由由 A 维护 |
| `main.py` | ✏️ | 🔒 | 路由注册由 A 统一管理 |
| `config.py` | ✏️ | 🔒 | 配置由 A 维护 |
| `docs/` | ✏️ | ✏️ | 文档双方都可更新 |
| `scripts/` | ✏️ | ✏️ | 脚本双方都可更新 |
