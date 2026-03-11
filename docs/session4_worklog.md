# Session 4 工作日志 — FAIL 接口按模块整改

> 生成时间: 2026-03-11 08:59
> 总目标: 修复全量对比中 208 个 FAIL 接口，按模块逐个整改至 PASS

---

## 一、全局修复（已完成 ✅）

在 `core/database.py` 中补充了 `fetch_all` / `fetch_one` / `fetch_scalar` 三个方法，一次性覆盖 33+ 个因缺失方法导致 999 的接口。

---

## 二、已完成模块（简单模块 7 个）

### Budget (4 FAIL → 4 PASS ✅)
- 修复文件: `routers/eshang_api_main/budget/budget_router.py`
- 修复内容: CRUD 逻辑对齐、OtherData 去除、msg 改 "查询成功"
- 仅剩 OPERATE_DATE 日期格式差异（全局问题）

### BusinessMan (3 FAIL → 3 PASS ✅)
- 修复文件: `routers/eshang_api_main/batch_modules/batch_router_part2.py`, `services/businessman/businessman_service.py`
- 修复内容: locale 拼音排序、USERModel 38 字段补全、EXISTS 子查询

### Customer (2 FAIL → 2 PASS ✅)
- 修复文件: `routers/eshang_api_main/batch_modules/batch_router_part2.py`
- 修复内容: CRUD 配置 exclude/in_fields、TranslateDateTime 格式化

### Finance (2 FAIL → 1 PASS + 1 数据问题)
- `GetAHJKtoken` ✅ PASS
- `GetAccountCompare` — 代码逻辑✅（820+ 行 Python 完整移植 C# 树形嵌套逻辑）
  - **⚠️ 对比 FAIL 是数据问题**：达梦 `T_ENDACCOUNT_DAILY` 缺少 12 月营收数据
  - 修复的 bug: LIMIT→ROWNUM 分页、datetime.min Windows 不兼容、Brand 字段缺失、达梦列不存在
  - 修复文件: `services/finance/account_compare_service.py`

### Sales (3 接口 → 2 PASS + 1 环境差异)
- `GetCOMMODITYSALEList` ✅ — body 可选 + NullRef 模拟 + msg
- `GetEndaccountError` ✅ — body 可选 + NullRef 模拟
- `GetCOMMODITYSALEDetail` ⚠️ — 环境差异（URI 含不同服务器地址）
- 修复文件: `routers/eshang_api_main/batch_modules/batch_router_part2.py`

### Supplier (1 FAIL → 1 PASS ✅)
- `GetQUALIFICATION_HISList` ✅ — 批量 CRUD _list body 可选 + NullRef 模拟
- 修复文件: `routers/eshang_api_main/batch_modules/batch_router_part2.py` (_BM_CRUD 循环)

### Verification (2 FAIL → 1 PASS + 1 数据问题)
- `GetSuppEndaccountList` ✅ — 去 StaticsModel/OtherData + 搜索回显字段 + 日期格式 + 排除多出字段
- `GetShopEndaccountSum` ⚠️ — 数据差异（达梦数据不完整）
- 修复文件: `routers/eshang_api_main/batch_modules/batch_router_part2.py`

---

## 三、已部分处理模块（代码已修 但受阻于数据）

### Audit (10 FAIL → 代码已修 ⚠️ 数据受阻)
- **代码修复**:
  1. `services/audit/audit_service.py` — `_generic_list` 重写:
     - `LIMIT/OFFSET` → 达梦 ROWNUM 子查询分页
     - `SearchData` → 兼容 `SearchParameter`
     - 添加 `SERVERPART_IDS` IN 子句
     - 主键精确匹配
  2. `routers/eshang_api_main/batch_modules/batch_router_part1.py`:
     - `GetCheckAccountReport` / `GetAbnormalRateReport` — POST 改 GET+POST 双方法支持
     - 添加 msg="查询成功"
- **数据受阻**: 达梦数据库中 **全部 5 张 Audit 表不存在**（T_YSABNORMALITY, T_ABNORMALAUDIT, T_CHECKACCOUNT, T_AUDITTASKS, T_YSABNORMALITYDETAIL）

---

## 四、未处理模块 — 达梦数据库表可用性检查结果

> [!IMPORTANT]
> 批量检查发现大量模块的表在达梦中不存在。**代码修复无法解决表缺失问题**，需要先同步表到达梦。

| 模块 | FAIL数 | 表状态 | 缺失表 | 下一步 |
|------|--------|--------|--------|--------|
| **Commodity** | **3** | **✅ 3/3** | 无 | **优先修复 — 缺字段+日期格式** |
| **BaseInfo** | **44** | **✅ 11/11** | 无 | **优先修复 — 回显字段+JOIN+类型** |
| BigData | 13 | ⚠️ 4/5 | T_BAYONET | 部分可修（12/13），1个缺表 |
| Analysis | 30 | ⚠️ 5/11 | 6表缺失 | 部分可修，需逐个分析 |
| BusinessProject | 40 | ⚠️ 2/4 | T_PROJDECORATION, T_PROIINST | 部分可修，需逐个分析 |
| Revenue | 27 | ⚠️ 4/9 | 5表缺失 | 部分可修，需逐个分析 |
| Audit | 10 | ❌ 0/5 | 全部缺失 | **代码已修**，等数据同步 |
| Merchants | 11 | ❌ 0/3 | 全部缺失 | 等数据同步 |
| Contract | 8 | ❌ 1/4 | 3表缺失 | 等数据同步 |
| MobilePay | 6 | ❌ 0/4 | 全部缺失 | 等数据同步 |

---

## 五、关键发现和经验

### 系统性问题模式
1. **达梦 SQL 分页**: 不支持 `LIMIT/OFFSET`，需用 `ROWNUM` 子查询或 `OFFSET-FETCH`
2. **SearchParameter vs SearchData**: C# 用 `SearchParameter`，部分 Python 实现用了 `SearchData`，需兼容
3. **NullRef 模拟**: C# POST 接口收到 null body 抛 NullReferenceException，Python 需 `search_model: dict = None` + raise
4. **msg 差异**: C# `Result_Desc` 通常为 "查询成功"，Python 默认 "成功"
5. **StaticsModel/OtherData**: 部分接口 C# 不返回但 Python JsonListData 默认包含
6. **日期格式**: C# 用 `yyyy/MM/dd HH:mm:ss`，达梦返回 ISO 格式 `yyyy-MM-ddTHH:mm:ss`

### 对比验证脚本
- 入口: `scripts/compare_api.py --manifest <manifest.json> --report <output.md>`
- Manifest 库: `scripts/manifests/endpoint_case_library.json`
- 各模块快速验证: `scripts/run_*_compare.py`（run_finance_compare.py, run_ssv_compare.py, run_audit_compare.py）

### 修复工作流
1. 创建模块 manifest → 运行对比 → 分析差异
2. 修复 router 层（msg/NullRef/HTTP方法） + service 层（SQL/逻辑）
3. 重启服务 → 重新对比验证
4. 标记代码问题 vs 数据问题

---

## 六、下一步工作建议（按优先级）

### 优先修复（全表可用）
1. **Commodity (3 FAIL)** — 缺 25 个字段（需 JOIN 补充）、日期格式
2. **BaseInfo (44 FAIL)** — 回显字段、JOIN 字段、类型差异、排序差异（工作量最大）

### 部分可修（有表的接口先修）
3. **BigData (13 FAIL)** — 12 个不依赖 T_BAYONET 的可先修
4. **Analysis (30 FAIL)** — 不依赖缺失表的接口先修（约 20 个）
5. **BusinessProject (40 FAIL)** — 不依赖 T_PROJDECORATION/T_PROIINST 的先修
6. **Revenue (27 FAIL)** — 不依赖缺失表的先修

### 需数据同步后才能继续
7. Audit (10) — 代码已修，等 5 表同步
8. Merchants (11) — 等 3 表同步
9. Contract (8) — 等 3 表同步
10. MobilePay (6) — 等 4 表同步

---

## 七、修改过的核心文件清单

| 文件 | 修改内容 |
|------|---------|
| `core/database.py` | 补 fetch_all/fetch_one/fetch_scalar |
| `services/audit/audit_service.py` | _generic_list 重写（ROWNUM分页+SearchParameter+SERVERPART_IDS） |
| `services/finance/account_compare_service.py` | 820行完整移植 C# GetAccountCompare |
| `services/finance/budget_service.py` | Budget CRUD 逻辑对齐 |
| `services/businessman/businessman_service.py` | USERModel 38字段+拼音排序+EXISTS |
| `routers/eshang_api_main/batch_modules/batch_router_part1.py` | Audit HTTP方法修复 |
| `routers/eshang_api_main/batch_modules/batch_router_part2.py` | Sales/Supplier/Verification 修复 |
| `routers/eshang_api_main/budget/budget_router.py` | Budget msg+OtherData |
