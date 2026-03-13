---
name: 达梦数据库 SQL
description: 达梦 vs Oracle 语法差异、分页模板、连接配置、常用 DDL 操作速查
---

# 达梦数据库 SQL 技能

> 本项目使用达梦数据库（DM8），兼容大部分 Oracle 语法但存在差异。本文档提供常用操作速查。

## 连接配置

```python
import dmPython

# 标准连接
conn = dmPython.connect(
    user='NEWPYTHON',
    password='NewPython@2025',
    server='192.168.1.99',
    port=5236
)

# 快速查询
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM T_XXX")
print(cur.fetchone()[0])
conn.close()
```

项目中使用 `core/database.py` 中的 `DatabaseHelper` 类，配置在 `config.py`。

---

## Oracle → 达梦语法差异

| 功能 | Oracle | 达梦 | 状态 |
|------|--------|------|------|
| 分页 | `ROWNUM` | `ROWNUM`（兼容） | ✅ |
| 当前日期 | `SYSDATE` | `SYSDATE`（兼容） | ✅ |
| 空值替换 | `NVL()` | `NVL()`（兼容） | ✅ |
| 条件表达式 | `DECODE()` | `DECODE()`（兼容） | ✅ |
| 外连接 | `(+)` | ❌ 改用 `LEFT JOIN` | ⚠️ |
| 树形查询 | `CONNECT BY` | `START WITH ... CONNECT BY` | ⚠️ |
| 字符串聚合 | `WM_CONCAT()` | `WM_CONCAT()`（兼容） | ✅ |
| 序列 | `SEQ.NEXTVAL` | `SEQ.NEXTVAL`（兼容但需权限） | ⚠️ |
| LIMIT | 不支持 | 不支持（用 ROWNUM） | ❌ |

---

## ROWNUM 分页模板

达梦不支持 `LIMIT OFFSET`，统一使用 ROWNUM 子查询分页：

```python
offset = (page_index - 1) * page_size
paged_sql = f"""
    SELECT * FROM (
        SELECT A.*, ROWNUM AS RN__ FROM (
            SELECT * FROM {TABLE_NAME} WHERE {where_clause} ORDER BY {sort_str}
        ) A WHERE ROWNUM <= {offset + page_size}
    ) WHERE RN__ > {offset}
"""
rows = db.fetch_all(paged_sql, params, null_to_empty=False) or []
# 删除临时 ROWNUM 列
for r in rows:
    r.pop("RN__", None)
```

---

## 常用 DDL

### 建表（从 Oracle 迁移）

```powershell
# 使用项目迁移脚本（自动处理建表+数据+注释）
python scripts/server_migrate.py T_XXX
python scripts/server_migrate.py T_XXX T_YYY  # 多张表
```

> ⚠️ 禁止不带参数运行 `python scripts/server_migrate.py`（会全量重跑所有表）

### 手动建表

```sql
CREATE TABLE T_EXAMPLE (
    EXAMPLE_ID INT PRIMARY KEY,
    EXAMPLE_NAME VARCHAR(100),
    EXAMPLE_STATE INT DEFAULT 1,
    OPERATE_DATE TIMESTAMP
);
```

### 添加表注释

```sql
COMMENT ON TABLE T_EXAMPLE IS '示例表';
COMMENT ON COLUMN T_EXAMPLE.EXAMPLE_ID IS '主键ID';
COMMENT ON COLUMN T_EXAMPLE.EXAMPLE_NAME IS '名称';
```

### 修改列类型（常见：VARCHAR → INT）

```sql
-- 达梦修改列类型（迁移工具可能把 NUMBER 导成 VARCHAR）
ALTER TABLE T_XXX MODIFY COLUMN_NAME INT;
```

### 查看表结构

```sql
-- 查看所有表
SELECT TABLE_NAME FROM USER_TABLES ORDER BY TABLE_NAME;

-- 查看表字段
SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH FROM USER_TAB_COLUMNS 
WHERE TABLE_NAME = 'T_XXX' ORDER BY COLUMN_ID;

-- 查看行数
SELECT COUNT(*) FROM T_XXX;

-- 查看表注释
SELECT TABLE_NAME, COMMENTS FROM USER_TAB_COMMENTS WHERE TABLE_NAME = 'T_XXX';
```

---

## 序列处理

NEWPYTHON 用户**无 CREATE SEQUENCE 权限**，新增记录使用 MAX+1 降级方案：

```python
try:
    new_id = db.execute_scalar("SELECT SEQ_XXX.NEXTVAL FROM DUAL")
except Exception:
    new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
```

---

## Oracle Schema 映射

| Oracle Schema | 包含的表 | 说明 |
|---------------|---------|------|
| `HIGHWAY_STORAGE` | T_SERVERPART, T_SERVERPARTSHOP, T_CASHWORKER, T_COMMODITY... | 服务区、门店、收银、商品 |
| `COOP_MERCHANT` | T_OWNERUNIT, T_BRAND, T_COOPMERCHANTS... | 业主、品牌、商户 |

---

## 常见错误及解决

| 错误 | 原因 | 解决 |
|------|------|------|
| `无效的表或视图名[T_XXX]` | 表未迁移到达梦 | `python scripts/server_migrate.py T_XXX` |
| `列[XXX]无效` | 字段名拼写错误或不存在 | 检查 `USER_TAB_COLUMNS` |
| `CODE:-5519 没有创建序列权限` | NEWPYTHON 权限不足 | 使用 MAX+1 降级方案 |
| `LIMIT 语法错误` | 达梦不支持 LIMIT | 改用 ROWNUM 子查询 |
| `NUMBER 返回字符串` | 迁移工具类型映射问题 | `ALTER TABLE MODIFY col INT` |
