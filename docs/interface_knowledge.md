# 接口迁移知识库

> 本文件用于沉淀整改过程中的接口级知识，每次整改完成后同步更新
> 格式：按模块 → 接口组 → 单接口三层组织

---

## 一、通用规范

### 1.1 响应包标准

C# 原格式：
```json
{
  "Result_Code": 200,
  "Result_Desc": "ok",
  "Result_Data": { ... }
}
```

列表接口：
```json
{
  "Result_Code": 200,
  "Result_Desc": "ok",
  "Result_Data": {
    "TotalCount": 100,
    "List": [ ... ]
  }
}
```

Python 应使用 `Result.success()` / `Result.fail()` + `JsonListData` 保持一致。

### 1.2 迁移状态分级

| 级别 | 含义 | 判定标准 |
|------|------|----------|
| L0 | 未迁移 | Python 无此路由 |
| L1 | 路由已注册 | 路由在但逻辑为占位/通用CRUD |
| L2 | 契约兼容 | 参数名、响应格式、HTTP方法与 C# 一致 |
| L3 | 逻辑等价 | SQL、分页、排序、副作用与 C# helper 一致 |
| L4 | 动态验收通过 | 3 组参数新旧对比全部通过 |

### 1.3 10 项 Checklist

每个接口整改后需逐项检查：

1. 路由名与 C# 完全一致
2. HTTP 方法一致
3. 参数名、参数类型、GET/POST 双入口一致
4. Header 注入完整
5. 返回包结构一致
6. 保留原 helper 业务语义
7. 分页/排序/OtherData/summaryObject 一致
8. 删除语义一致
9. 文件系统/外部系统/缓存分支/审批状态机
10. 3 组参数新旧对比通过

### 1.4 已知反模式（禁止使用）

- ❌ `return []` / `return True` / `return {}` 作为已迁移接口
- ❌ 使用 `pk_val` 泛化参数名替代实体专属参数名
- ❌ `code/message/data` 响应格式（应使用 `Result` 标准格式）
- ❌ 多个不同业务接口复用同一个简单 CRUD 查询
- ❌ Python 多出接口计入原模块迁移完成度

---

## 二、已整改模块知识卡

> 以下在整改完成后逐步填充

---

### Revenue 模块

**C# Controller**: `RevenueController`
**Python Router**: `revenue_router.py`
**Python Service**: `revenue_service.py` (2836行)

**已知问题**：
- ~~`revenue_service.py` 第 227 行 `get_his_commodity_sale_list`: `params` 未定义~~ → ✅ 已修复
- ~~`revenue_service.py` 第 259 行 `get_revenue_data_list`: `params` 未定义~~ → ✅ 已修复
- 7 组 CRUD 使用通用模板（需核对契约兼容性）
- 散装报表有 2800+ 行实际业务逻辑（不是占位）

**当前状态**：
- CRUD 部分: L1（通用模板，需契约复核）
- 散装报表: L1-L2（有逻辑，运行时错误已修复）

**整改记录**：
| 日期 | 整改包 | 内容 | 结果 |
|------|--------|------|------|
| 2026-03-09 | RE-02 前置修复 | 修复第227/259行 `params` 未定义 | ✅ 移除多余 params 参数 |

---

### Verification 模块

**C# Controller**: `VerificationController`
**Python Service**: `verification_service.py` (291行)

**已知问题**：
- 表名漂移：操作 `T_ENDACCOUNT_DAILY` 而非 `T_ENDACCOUNT`
- `verify_endaccount`: 仅 `SET AUDIT_STATE = 1`，无批量/校验/错误返回
- `approve_endaccount`: 仅 `SET APPROVE_STATE = 1`
- `cancel_endaccount` 复用 `apply_endaccount_invalid`
- 7 个接口纯占位 (`return []` / `return True` / `return {}`)

**当前状态**：全部 L1

**整改记录**：
| 日期 | 整改包 | 内容 | 结果 |
|------|--------|------|------|
| — | — | — | — |

---

### Sales 模块

**Python Service**: `verification_service.py` (共享文件, 239-291行)

**已知问题**：
- 6 个不同业务接口全部复用 `_crud(T_COMMODITYSALE)` 同一查询
- `DeleteCOMMODITYSALE` 执行真实软删，但 C# 原逻辑不可删

**当前状态**：全部 L1

---

### Audit 模块

**Python Service**: `audit_service.py` (194行)

**已知问题**：
- `get_special_behavior_report`: `return []` 占位
- `get_abnormal_rate_report`: `return []` 占位
- `issue_audit_tasks`: 仅调用 `synchro_entity`（无下发逻辑）
- `upload_audit_explain`: 仅调用 `synchro_entity`（无上传逻辑）
- CRUD 部分使用通用模板但参数名正确（不存在 pk_val 问题）

**当前状态**：
- CRUD: L1（需修响应格式）
- 散装: L0-L1（2个占位 + 4个简化 + 4个有SQL逻辑）

---

### BusinessMan/Supplier 模块

**Python Service**: `businessman_service.py` (128行)

**已知问题**：
- 表映射漂移：C# 用 OWNERUNIT，Python 用 T_BUSINESSMAN
- `relate_business_commodity`: `return True, ""` 占位
- `create_businessman`: 仅通用 upsert 包装
- `get_user_list`: 查 T_BUSINESSMAN 而非用户表
- `get_nesting_custom_type_list`: 平铺查询，无嵌套/树
- `get_supplier_tree_list`: 无树结构

**当前状态**：全部 L1

---

### Finance 模块

**Python Service**: `finance_scattered_service.py`

**已知问题**：
- 22 处 `return []` / `return True, ""` 占位
- 覆盖审批流、固化、重算、短信、提单等核心接口

**当前状态**：大量 L0-L1

---

### Picture 模块

**已知问题**：
- 路由集合被替换（9 个路由中仅 2 个匹配 C# 原接口）
- Python 独有 6 条不在 C# PictureController 中
- C# 原有 6 条未实现

**当前状态**：L1（语义偏离）

---

### Video 模块

**已知问题**：
- 16 条接口全部未实现

**当前状态**：全部 L0
