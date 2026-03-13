# SQL 安全扫描报告

> 扫描时间: 2026-03-13 | 扫描范围: services/ + routers/ | 共 142 个文件

## 概览

| 指标 | 数值 |
|------|------|
| 扫描文件数 | 142 |
| 发现拼接点 | 1,359 |
| 高危（用户输入参数） | 292 |
| 低危（内部/常量参数） | 1,067 |
| 涉及文件 | 71 |

## 风险说明

> [!IMPORTANT]
> 当前系统为**内网 API 服务**，前端由公司内部系统调用，非面向公网。
> 因此实际风险等级低于公网应用，但仍应逐步改善。

**HIGH** = f-string SQL 中直接使用了用户输入参数（`SearchParameter`、`data`、`request` 等）或在 `_build_where_sql` 函数内
**LOW** = f-string SQL 中使用的是内部常量或已转型的参数（如 `int(xxx_id)`）

## 高危文件 TOP 10

| 文件 | HIGH | LOW | 说明 |
|------|------|-----|------|
| `routers/commercial_api/revenue_router.py` | 18 | 117 | 业务逻辑直接在 Router，无 Service 层 |
| `services/business_project/paymentconfirm_service.py` | 18 | 12 | 支付确认，涉及金额 |
| `services/revenue/revenue_service.py` | 15 | 59 | 营收服务 |
| `services/contract/contract_service.py` | 12 | 30 | 合同服务 |
| `services/base_info/spstatictype_service.py` | 11 | 3 | 静态类型 |
| `services/base_info/brand_service.py` | 10 | 23 | 品牌服务 |
| `services/bigdata/bigdata_service.py` | 10 | 49 | 大数据分析 |
| `services/finance/finance_scattered_service.py` | 10 | 67 | 财务散装接口 |
| `services/base_info/commoditytype_service.py` | 8 | 18 | 商品类型 |
| `services/verification/verification_service.py` | 8 | 45 | 核销服务 |

## 改进策略

### 短期（低成本）
**在 `_build_where_sql` 中增加输入净化**：

```python
# 当前：直接拼接
conditions.append(f"{key} LIKE '%{value}%'")

# 改进：转义单引号防止注入
safe_value = str(value).replace("'", "''")
conditions.append(f"{key} LIKE '%{safe_value}%'")
```

### 中期（推荐）
**整数参数强制类型转换**：

```python
# 对 ID 类参数
xxx_id = int(xxx_id)  # 非整数会直接报错
sql = f"SELECT * FROM T_XXX WHERE XXX_ID = {xxx_id}"
```

### 长期（参数化查询）
**逐步迁移到参数化查询**：

```python
# 当前
sql = f"SELECT * FROM T_XXX WHERE NAME = '{value}'"
rows = db.execute_query(sql)

# 目标
sql = "SELECT * FROM T_XXX WHERE NAME = ?"
rows = db.execute_query(sql, [value])
```

> 注意：参数化查询需要 `DatabaseHelper` 支持参数占位符传递，建议先确认。

## 修复优先级

| 优先级 | 范围 | 动作 |
|--------|------|------|
| P0 | `_build_where_sql` 通用函数 | 加入 `replace("'", "''")`，一次修改惠及所有 Service |
| P1 | Synchro/Delete 中的 data 参数 | INSERT/UPDATE 涉及写入，需检查输入净化 |
| P2 | CommercialApi Router 层 SQL | 随 Phase 3.1 架构统一一同改进 |
| P3 | 内部参数 LOW 级别 | 风险低，长期改进 |
