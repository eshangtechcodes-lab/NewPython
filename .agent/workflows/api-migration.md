---
description: C# API 接口平移到 Python FastAPI 的标准工作流
---

# API 接口迁移工作流

> 适用于 EShangApi C# → Python FastAPI 的逐接口迁移。每迁移一个接口，严格按以下 5 步执行。

## 前置条件

- 原 C# API 服务已启动（`http://localhost:8900`）
- 新 Python API 服务已启动（`http://localhost:8080`）
- 原项目代码路径：`D:\Project\000_通用版本\000_通用版本\030_EShangApi`

---

## 第一步：读原代码（只读不写）

// turbo-all

### 1.1 定位原 Controller

在原 C# 项目中找到对应的 Controller 文件，确认：

- **路由路径**：`[Route("BaseInfo/GetXxxList")]` 的确切大小写拼写
- **入参格式**：是 `SearchModel<T>` 直接 JSON，还是 `CommonModel`（AES 加密的 `value`）
- **HTTP 方法**：POST / GET

```
# 示例：查找 BRAND 相关的 Controller
搜索路径：EShangApiMain/Controllers/ 或 EShangApiMain/Areas/
搜索关键词：GetBrandList 或 BRAND
```

### 1.2 定位原 Helper（Service 层）

找到对应的 Helper 文件，确认：

- **SQL 查询语句**：完整的 SELECT（含 JOIN、子查询）
- **默认排序**：ORDER BY 子句
- **默认分页**：不传参数时的默认行为（通常默认 10 条）
- **关联表**：JOIN 了哪些表，额外拼接了哪些字段

```
# 示例：查找 BRAND 的业务逻辑
搜索路径：EShang.Common/ 或 EShangApiMain/Helper/
搜索关键词：GetBrandList 或 T_BRAND
```

### 1.3 定位原 Model

确认返回的字段列表和类型（int / string / datetime / 嵌套对象）。

---

## 第二步：调原 API 获取基准数据

### 2.1 调用原接口记录基准响应

用空参数 `{}` 调用原接口，保存完整 JSON 响应作为基准：

```powershell
# 获取基准数据
Invoke-RestMethod -Uri "http://localhost:8900/EShangApiMain/BaseInfo/GetXxxList" -Method Post -Body '{}' -ContentType 'application/json' | ConvertTo-Json -Depth 10 > scripts/baseline/xxx_list_baseline.json
```

### 2.2 记录关键指标

从基准响应中提取并记录：

| 指标 | 值 |
|------|-----|
| Result_Code | ? |
| TotalCount | ? |
| List 条数 | ?（不传参数时的默认值） |
| PageIndex 默认值 | ? |
| PageSize 默认值 | ? |
| 字段列表 | [完整字段名列表] |
| 第一条数据排序依据 | ?（确认默认排序） |
| 字段类型 | int? string? datetime? |

---

## 第三步：创建达梦对应表

### 3.1 确认达梦表已存在

检查 NEWPYTHON 用户下是否已有对应的表和数据：

```python
# 在 scripts/check_dm_xxx.py 中验证
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='127.0.0.1', port=5236)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM T_XXX")
print(f"数据量: {cur.fetchone()[0]}")
# 打印字段列表和类型
cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM USER_TAB_COLUMNS WHERE TABLE_NAME='T_XXX' ORDER BY COLUMN_ID")
for row in cur.fetchall():
    print(f"  {row[0]:30s} {row[1]}")
```

### 3.2 字段类型校验

对比达梦字段类型与原 Oracle 表，确保数值列为 INT/DECIMAL 而非 VARCHAR。若类型不对，修改达梦表结构：

```sql
ALTER TABLE T_XXX MODIFY BRAND_ID INTEGER;
```

---

## 第四步：实现 Python 接口

按照第一步读取的原代码，创建以下文件：

### 4.1 Model（若尚不存在）

文件：`models/auto_build/xxx.py`

- 使用 Pydantic BaseModel
- 字段名与原 C# Model 完全一致
- 字段类型与原 API 返回类型对齐

### 4.2 Service

文件：`services/auto_build/xxx_service.py`

- **SQL 必须参考原 Helper 中的查询**，不能自己猜测
- 包含 JOIN、默认排序、默认分页逻辑
- 保持与原 Helper 完全一致的业务行为

### 4.3 Router

文件：`routers/eshang_api_main/auto_build/xxx_router.py`

- 路由路径与原 Controller 完全一致（注意大小写）
- 入参格式与原 Controller 一致
- 在 `main.py` 中注册路由时加 `prefix="/EShangApiMain"`

---

## 第五步：对比验证

### 5.1 运行对比脚本

修改 `scripts/compare_api.py`，替换为当前接口的路径，然后执行：

```powershell
python scripts/compare_api.py
```

### 5.2 对比清单（全部 ✅ 才算通过）

| 检查项 | 要求 |
|--------|------|
| Result_Code | 一致 |
| Result_Desc | 一致 |
| TotalCount | 一致 |
| List 条数 | 一致（默认分页行为相同） |
| PageIndex / PageSize | 一致 |
| 字段列表 | 完全一致（无缺失、无多余） |
| 字段值类型 | 一致（int/string/null） |
| 排序 | 第一条数据相同 |
| 空值处理 | null 的字段一致 |

### 5.3 提交代码

```powershell
git add -A
git commit -m "feat: 迁移 XxxList 接口 - 对比验证通过"
git push
```

---

## 注意事项

1. **绝不假设入参格式**，必须看原 Controller 代码确认
2. **绝不假设 SQL 查询**，必须看原 Helper 代码中的完整 SQL
3. **绝不假设默认行为**，必须先调用原 API 确认
4. **字段顺序不重要**，但字段名、类型、值必须完全一致
5. **每完成一个接口就提交一次 Git**，保持原子性
