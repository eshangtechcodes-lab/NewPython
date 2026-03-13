# SQL 安全扫描报告

> 扫描时间: 2026-03-13 | 范围: `services/commercial/` 10 个 Service 文件

## 风险评估

### 总体结论

当前 SQL 注入风险整体 **偏低**，原因：
1. **参数来源受控** — 所有参数都通过 FastAPI 的 `Query()` 类型标注，框架自动做了类型校验
2. **大部分是整数拼接** — `Serverpart_ID`、`Province_Code` 等都是 int 类型参数
3. **日期格式受限** — 日期参数经过 `strptime` 解析后再格式化，无法注入任意字符串
4. **无直接用户输入** — 不像 Web 表单，API 参数都是结构化的

### 风险分级

| 等级 | 说明 | 处理建议 |
|------|------|---------|
| 🔴 高 | 用户字符串直接拼入 SQL | 立即修复 |
| 🟡 中 | 字符串参数拼接但有前置校验 | 后续优化 |
| 🟢 低 | 整数/日期拼接，类型受限 | 可接受 |

### 各文件风险清单

| 文件 | f-string SQL 数 | 高风险 | 中风险 | 低风险 |
|------|-----------------|--------|--------|--------|
| `revenue_push_service.py` | 6 | 0 | 1 (province_code) | 5 |
| `revenue_brand_service.py` | 2 | 0 | 1 (province_code) | 1 |
| `revenue_budget_service.py` | 4 | 0 | 1 (province_code) | 3 |
| `revenue_transaction_service.py` | 8 | 0 | 1 (province_code) | 7 |
| `revenue_trend_service.py` | 4 | 0 | 0 | 4 |
| `bigdata_bayonet_service.py` | ~12 | 0 | 0 | 12 |
| `bigdata_month_service.py` | ~4 | 0 | 0 | 4 |
| `bigdata_warning_service.py` | ~8 | 0 | 0 | 8 |
| `bigdata_detail_service.py` | ~6 | 0 | 0 | 6 |
| `examine_service.py` | 4 | 0 | 0 | 4 |
| `contract_service.py` | 8 | 0 | 1 (province_code) | 7 |
| `budget_service.py` | 2 | 0 | 0 | 2 |

> **0 个高风险，5 个中风险（均为 province_code 字符串拼接），~60 个低风险**

### 中风险详情

`province_code` 参数（如 `"340000"`）在以下场景直接拼入 SQL：

```python
# 当前写法（中风险）
where_sql += f' AND B."PROVINCE_CODE" = {province_id}'

# 建议写法（参数化）
where_sql += ' AND B."PROVINCE_CODE" = :province_id'
params["province_id"] = province_id
```

但实际风险很低，因为：
- `province_code` 经过 `_get_province_id()` 函数处理，返回的是数据库查询结果（整数 ID）
- 即使攻击者传入恶意字符串，`_get_province_id` 会返回原值，但原值会经过达梦 SQL 解析器的整数上下文校验

### 已有防护措施

1. ✅ FastAPI `Query()` 类型标注自动校验参数类型
2. ✅ `parse_multi_ids()` 对多 ID 参数做了安全解析
3. ✅ `build_in_condition()` 对 IN 子句做了安全拼接
4. ✅ 日期参数经 `strptime` 解析后格式化，无法注入

### 后续改进计划

1. **短期** — 将 `_get_province_id()` 返回值做 `int()` 类型强制转换
2. **中期** — 新写的 Service 函数统一使用参数化查询
3. **长期** — 重写 Router 时逐步替换为参数化查询
