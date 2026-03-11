---
description: 按模块修复 FAIL 接口的标准操作流程（SOP），基于全量对比结果逐模块整改至 PASS
---

# 模块 FAIL 接口整改操作手册（SOP）

> **目标读者**：任何新接手的 AI。只需阅读本文件即可独立完成一个模块的 FAIL 接口整改。
>
> **一个"整改单元"** = 一个模块（如 Budget、BusinessMan、Contract）下所有 FAIL 状态的接口

// turbo-all

---

> [!CAUTION]
> **必须严格按本 SOP 步骤顺序执行，不允许跳步或凭猜测修改代码！**
> - 每步必须有实证（对比脚本输出、C# 源码截取）才能进入下一步
> - 最终验收标准：**对比脚本跑出 PASS**，而非手动 curl 验证
> - 修改代码时只改有差异的部分，不做"顺手重构"

---

## 背景知识

### 项目架构

本项目是将 C# ASP.NET Web API 迁移到 Python FastAPI。两套系统同时运行：

| 角色 | 地址 | 说明 |
|------|------|------|
| 原 C# API | `http://192.168.1.99:8900/EShangApiMain` | 线上环境，只读参考 |
| 新 Python API | `http://localhost:8080/EShangApiMain` | 本地开发环境 |

### 关键文件路径

| 类型 | 路径 |
|------|------|
| Python 项目根目录 | `E:\workfile\JAVA\NewAPI\` |
| C# Controller 目录 | `E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\` |
| C# Helper 目录 | `E:\workfile\JAVA\API\CSharp\EShangApi.Common\GeneralMethod\` |
| C# Model 目录 | `E:\workfile\JAVA\API\CSharp\EShangApi.Common\Model\` |
| Python Service 目录 | `E:\workfile\JAVA\NewAPI\services\` |
| Python Router 目录 | `E:\workfile\JAVA\NewAPI\routers\eshang_api_main\` |
| 全量 Manifest | `E:\workfile\JAVA\NewAPI\scripts\manifests\endpoint_case_library.json` |
| 对比脚本 | `E:\workfile\JAVA\NewAPI\scripts\compare_api.py` |
| 通用响应模型 | `E:\workfile\JAVA\NewAPI\models\base.py` |
| 数据库 Helper | `E:\workfile\JAVA\NewAPI\core\database.py` |
| 全量对比结果 | `E:\workfile\JAVA\NewAPI\docs\session4_full.json` |
| 模块修改计划 | `E:\workfile\JAVA\NewAPI\docs\session4_implementation_plan.md` |

### 对比脚本机制

`compare_api.py` 使用 `endpoint_case_library.json`（manifest）作为测试输入：
- manifest 的 `endpoints` 字典包含每个接口的请求方法、参数、Header
- 脚本同时调用 C# 和 Python 接口，逐字段对比 JSON 响应
- 判定标准：**所有** 检查项（HTTP 状态码、Result_Code、Result_Desc、Result_Data 字段集合、字段值）全部一致才算 PASS

### 常见 FAIL 根因分类

| 根因 | 典型差异表现 | 修复位置 |
|------|-------------|---------|
| **缺少 C# Model 回显字段** | `新 API 缺少该字段`（如 SERVERPART_IDS、OPERATE_DATE_Start） | Service 层 `_convert_xxx_row()` 补字段 |
| **Result_Desc 措辞** | `成功` vs `查询成功` | Router 层 `msg="查询成功"` |
| **日期格式** | `2023-03-30T14:02:47` vs `2023/3/30 14:02:47` | Service 层 `_format_date()` |
| **null_to_empty 过度转换** | C# 为 None 但 Python 为 '' | `fetch_all(null_to_empty=False)` + 精确 `_convert` |
| **分页语法不兼容** | `LIMIT OFFSET` 在达梦不工作 | 改为 ROWNUM 子查询 |
| **多出/缺少 JsonListData 字段** | `StaticsModel`、`OtherData` 多出 | `model_dump(exclude_none=True)` |
| **搜索条件未匹配** | TotalCount/List 长度不同 | Service 层补 WHERE 条件 |
| **C# 端 404** | 原 API HTTP 404 | 这类属于 C# 侧未部署，应标为 SKIP，不修 |

---

## 步骤 0：确定目标模块

### 0.1 查看修改计划

```
view_file docs/session4_implementation_plan.md
```

找到目标模块及其 FAIL 接口列表。记录：

```
目标模块: ___________（例如：Budget）
FAIL 接口数: ___________（例如：4）
接口清单: ___________（逐个列出）
```

### 0.2 查看全量对比结果

```
# 从 session4_full.json 提取该模块所有 case 的详细差异
python -c "
import json
d = json.load(open('docs/session4_full.json', 'r', encoding='utf-8'))
for c in d['cases']:
    if c['endpoint'].startswith('模块名/'):
        print('接口:', c['endpoint'], '/', c['case_name'])
        print('  状态:', c['status'])
        print('  old_http:', c.get('old_status_code'), 'new_http:', c.get('new_status_code'))
        for diff in c.get('diffs', []):
            print('  差异:', diff[:150])
        print()
"
```

### 0.3 分类接口

将接口分为三类：

| 分类 | 说明 | 处理方式 |
|------|------|---------|
| **需修复** | C# 200 + Python 200，但响应内容有差异 | 按步骤 1-5 修复 |
| **C# 404** | C# 侧返回 404（未部署/配置缺失） | 标为 SKIP，不修 |
| **Python 报错** | Python 侧抛异常（如缺方法、SQL 报错） | 先修代码错误，再走对比 |

---

## 步骤 1：读取 C# 源码（只读分析）

### 1.1 定位 C# Controller

找到 `docs/` 下的整改文档中该模块引用的 C# Controller 路径，或直接搜索：

```
find_by_name "模块名*Controller*" E:\workfile\JAVA\API\CSharp\EShangApiMain\Controllers\
```

### 1.2 逐个分析 FAIL 接口的 C# 实现

对每个 FAIL 接口，从 C# Controller 中提取以下信息并记录：

```markdown
| 项目 | 内容 |
|------|------|
| 路由 | `[Route("Budget/GetXXX")]` 精确大小写 |
| HTTP 方法 | GET / POST / GET+POST |
| 返回包装 | `Models.JsonMsg<T>.Success(data, 100, "查询成功")` |
| Result_Desc 措辞 | "查询成功" / "同步成功" / "删除成功" |
| 返回结构 | JsonList<T> / JsonList<T, T2>（有 OtherData） |
| Helper 调用 | `XXXHelper.GetXXXList(transaction, ...)` |
```

### 1.3 分析 C# Model 回显字段

C# 的 Model 类包含的属性 **不一定全在数据库表中**。部分属性仅作为查询条件回显（如 `OPERATE_DATE_Start`、`SERVERPART_IDS`）。

确认方法：
1. 查看 C# Model 定义中的所有 public 属性
2. 与数据库表 `SELECT *` 返回的列对比
3. 差集就是 **C# Model 回显字段**，需要在 Python 侧手动补 `None`

> [!IMPORTANT]
> **这是最容易遗漏的差异！** C# 序列化 Model 时，即使属性值为 null 也会输出字段名。
> Python 的 `SELECT *` 只返回数据库列，必须手动补齐。

### 1.4 分析特殊逻辑

重点关注：
- **OtherData / Summary**：C# `JsonList<T, T2>` 用于返回汇总对象（如 `SUM(金额)`）
- **日期格式**：C# `DateTime.ToString()` 默认输出 `yyyy/M/d H:mm:ss`（注意月日不补零）
- **字符串 null 处理**：C# `string` 属性 DBNull → `""`，Python 需精确控制

---

## 步骤 2：对比 Python 实现

### 2.1 定位 Python Service 和 Router

```
find_by_name "*模块名*" E:\workfile\JAVA\NewAPI\services\
find_by_name "*模块名*" E:\workfile\JAVA\NewAPI\routers\
```

### 2.2 逐接口对比差异

对每个 FAIL 接口，将 C#（步骤 1 的分析结果）与 Python 实现逐项对照：

```markdown
| 对比项 | C# 行为 | Python 现状 | 需修改？ |
|--------|---------|-------------|---------|
| Result_Desc | "查询成功" | "成功" | ✅ Router 加 msg |
| 回显字段 SERVERPART_IDS | 有（值 null） | 无 | ✅ _convert 补字段 |
| OPERATE_DATE 格式 | 2023/3/30 14:02:47 | 2023-03-30T14:02:47 | ✅ _format_date |
| BUDGETDETAIL_AH_DESC null | "" | None | ✅ 字符串 null→'' |
| OtherData | 有完整 Model | 无/仅部分字段 | ✅ 补完整字段 |
| StaticsModel | 无 | 有（序列化泄漏） | ✅ model_dump exclude_none |
| 分页 SQL | ROWNUM 子查询 | LIMIT OFFSET | ✅ 改 ROWNUM 子查询 |
```

---

## 步骤 3：实施修改

### 3.1 修改顺序（推荐）

按以下顺序修改，影响面从小到大：

1. **Router 层**：`msg="查询成功"` / `model_dump()` 显式调用
2. **Service 层**：添加 `_convert_xxx_row()` 转换函数（补回显字段 + 日期格式化 + 字符串 null→''）
3. **Service 层**：修改 `get_xxx_list()` / `get_xxx_detail()` 调用 `_convert_xxx_row()`
4. **Service 层**：搜索条件补全（对照 C# SearchModel 属性）
5. **Service 层**：`fetch_all(null_to_empty=False)` 避免过度转换

### 3.2 标准 _convert 函数模板

```python
# C# Model 回显属性（DB表没有，C# Model有，值为 null）
XX_EXTRA_FIELDS = {"SERVERPART_IDS": None, "OPERATE_DATE_Start": None, "OPERATE_DATE_End": None}
# C# Model 字符串字段，DBNull → ''
XX_STRING_FIELDS = {"XXX_DESC", "XXX_NAME"}


def _format_date(val):
    """将日期格式从 ISO 转为 C# 风格: 2023/3/30 14:02:47"""
    if val is None:
        return None
    s = str(val)
    try:
        if 'T' in s:
            dt = datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        elif '-' in s and len(s) >= 10:
            dt = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
        else:
            return s
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute:02d}:{dt.second:02d}"
    except Exception:
        return s


def _convert_xx_row(row: dict) -> dict:
    """转换行数据：补 C# Model 回显字段 + 字符串 null→'' + 日期格式化"""
    if not row:
        return row
    # 1. 补 C# Model 回显属性
    for k, v in XX_EXTRA_FIELDS.items():
        if k not in row:
            row[k] = v
    # 2. 字符串字段 null→''
    for f in XX_STRING_FIELDS:
        if f in row and row[f] is None:
            row[f] = ""
    # 3. 日期格式化
    if "OPERATE_DATE" in row:
        row["OPERATE_DATE"] = _format_date(row["OPERATE_DATE"])
    return row
```

### 3.3 标准 ROWNUM 分页模板

达梦不支持 `LIMIT OFFSET`，使用 ROWNUM 子查询：

```python
offset = (pi - 1) * ps
paged_sql = f"""
    SELECT * FROM (
        SELECT A.*, ROWNUM AS RN__ FROM (
            SELECT * FROM {TABLE} WHERE {wc} ORDER BY {sort_str}
        ) A WHERE ROWNUM <= {offset + ps}
    ) WHERE RN__ > {offset}
"""
rows = db.fetch_all(paged_sql, pa, null_to_empty=False) or []
for r in rows:
    r.pop("RN__", None)
```

### 3.4 Router 层 JsonListData 序列化规范

```python
# ✅ 正确：用 model_dump() 显式序列化，确保 None 字段不输出
jld = JsonListData(List=rows, TotalCount=total, PageIndex=pi, PageSize=ps)
return Result.success(jld.model_dump(), msg="查询成功")

# ❌ 错误：直接传 JsonListData 对象，FastAPI 序列化会泄漏 StaticsModel=None
return Result.success(JsonListData(...), msg="查询成功")
```

### 3.5 JsonListData OtherData 字段

`JsonListData` 支持可选 `OtherData` 字段。仅当 C# 使用 `JsonList<T, T2>` 时才传：

```python
# C# 有 OtherData 时：
jld = JsonListData(List=rows, TotalCount=total, PageIndex=pi, PageSize=ps, OtherData=summary)

# C# 没有 OtherData 时：不传该参数
jld = JsonListData(List=rows, TotalCount=total, PageIndex=pi, PageSize=ps)
```

---

## 步骤 4：对比脚本验证

### 4.1 创建模块验证脚本（每个模块必须创建）

> [!IMPORTANT]
> **每个模块必须创建一个独立的验证脚本文件**，路径为 `scripts/run_{模块名小写}_compare.py`。
> 这个脚本会从全量 manifest 中提取该模块的接口，生成临时 manifest，然后调用 `compare_api.py` 执行对比。
> 脚本创建后可反复使用：每次修改代码后重启服务 → 直接跑此脚本验证。

创建文件 `scripts/run_{模块名小写}_compare.py`，内容如下（替换 `模块名`）：

```python
# -*- coding: utf-8 -*-
"""从全量 manifest 中提取 {模块名} 模块，生成临时 manifest，然后调用 compare_api.py"""
import json, os

MODULE_PREFIX = "模块名/"  # ⬅️ 改这里：如 "Budget/", "BusinessMan/", "Contract/"

with open("scripts/manifests/endpoint_case_library.json", "r", encoding="utf-8") as f:
    full = json.load(f)

module_eps = {k: v for k, v in full["endpoints"].items() if k.startswith(MODULE_PREFIX)}

mini = {
    "version": full.get("version", "1.0"),
    "default_headers": full.get("default_headers", {}),
    "default_timeout": full.get("default_timeout", 15),
    "endpoints": module_eps
}

module_name = MODULE_PREFIX.rstrip("/").lower()
tmp_path = f"scripts/manifests/_tmp_{module_name}.json"
report_path = f"docs/session4_{module_name}.md"

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(mini, f, ensure_ascii=False, indent=2)

print(f"{MODULE_PREFIX} manifest: {len(module_eps)} endpoints")
print("Running compare_api.py ...")
os.system(f'python scripts/compare_api.py --manifest {tmp_path} --report {report_path}')
```

**示例：Budget 模块的验证脚本** `scripts/run_budget_compare.py`：

```python
# -*- coding: utf-8 -*-
"""从全量 manifest 中提取 Budget 模块，生成临时 manifest，然后调用 compare_api.py"""
import json, os

MODULE_PREFIX = "Budget/"

with open("scripts/manifests/endpoint_case_library.json", "r", encoding="utf-8") as f:
    full = json.load(f)

module_eps = {k: v for k, v in full["endpoints"].items() if k.startswith(MODULE_PREFIX)}

mini = {
    "version": full.get("version", "1.0"),
    "default_headers": full.get("default_headers", {}),
    "default_timeout": full.get("default_timeout", 15),
    "endpoints": module_eps
}

tmp_path = "scripts/manifests/_tmp_budget.json"
report_path = "docs/session4_budget.md"

with open(tmp_path, "w", encoding="utf-8") as f:
    json.dump(mini, f, ensure_ascii=False, indent=2)

print(f"Budget manifest: {len(module_eps)} endpoints")
print("Running compare_api.py ...")
os.system(f'python scripts/compare_api.py --manifest {tmp_path} --report {report_path}')
```

执行命令：
```powershell
python scripts/run_budget_compare.py
```

预期输出：
```
Budget manifest: 11 endpoints
Running compare_api.py ...
[1/11] GET Budget/GetBudgetDetailDetail / default-query
  -> PASS
[2/11] POST Budget/GetBudgetDetailList / default-body
  -> PASS
...
对比完成: PASS 4 / FAIL 7 / SKIP 0 / TOTAL 11
```

### 4.2 重启 Python 服务并执行验证脚本

每次修改代码后，必须按以下命令重启服务并执行验证：

```powershell
# 杀旧进程 + 启动新进程 + 等待启动 + 跑该模块的验证脚本
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2
Start-Process -FilePath python -ArgumentList "-m","uvicorn","main:app","--host","0.0.0.0","--port","8080","--workers","1" -WorkingDirectory "E:\workfile\JAVA\NewAPI" -WindowStyle Hidden
Start-Sleep -Seconds 5
python scripts/run_{模块名小写}_compare.py
```

> 修复过程中需要**反复执行**：修改代码 → 重启 → 跑脚本 → 看差异 → 修改代码 → 重启 → 跑脚本 → 直到全部 PASS。

### 4.3 解读对比结果

```
对比完成: PASS X / FAIL Y / SKIP 0 / TOTAL Z
```

- **PASS = CRUD 接口数** → 整改成功 ✅
- **FAIL 中 C# 404 的** → 属于 C# 侧问题，标为 SKIP
- **FAIL 中非 C# 404 的** → 需继续修复，回步骤 2 重新对比

### 4.4 查看具体 FAIL 差异

```python
import json
d = json.load(open("docs/session4_模块名.json", "r", encoding="utf-8"))
for c in d["cases"]:
    if c["status"] == "fail":
        print("---", c["endpoint"])
        print("  old_http:", c.get("old_status_code"), "new_http:", c.get("new_status_code"))
        for diff in c.get("diffs", []):
            print("  ", diff[:120])
```

如果 FAIL 是差异字段，回步骤 3 针对性修复，然后重新跑步骤 4。

---

## 步骤 5：记录结果

### 5.1 汇报格式

整改完成后，汇报以下信息：

```markdown
## 模块名 模块整改结果

对比脚本结果: PASS X / FAIL Y (C# 404) / TOTAL Z

### PASS 接口
| 接口 | 状态 |
|------|------|
| 模块/接口名1 | ✅ PASS |
| 模块/接口名2 | ✅ PASS |

### FAIL 接口（C# 404，不可修）
| 接口 | 原因 |
|------|------|
| 模块/Report接口 | C# 端 404 |

### 修改的文件
| 文件 | 修改内容 |
|------|---------|
| xxx_router.py | msg="查询成功" |
| xxx_service.py | _convert_xx_row + ROWNUM 分页 + ... |
```

### 5.2 继续下一个模块

回到步骤 0，选择下一个模块，重复整个流程。

---

## 附录：Budget 模块整改实例

以下是 Budget 模块的完整整改过程，作为典型参考：

### 模块概况

- 11 个接口：4 个 CRUD + 7 个 Report
- 初始状态：PASS 0 / FAIL 11
- 最终状态：PASS 4 / FAIL 7（全部 C# 404）

### 发现的差异及修复

| # | 差异 | 文件 | 修复方式 |
|---|------|------|---------|
| 1 | `fetch_one`/`fetch_scalar` 方法缺失 | `core/database.py` | 添加两个方法 |
| 2 | `Result_Desc` 默认 "成功" 而非 "查询成功" | `budget_router.py` | 4 处加 `msg="查询成功"` |
| 3 | `LIMIT OFFSET` 达梦不兼容 | `budget_service.py` | 改为 ROWNUM 子查询 |
| 4 | 缺少 C# Model 回显字段 | `budget_service.py` | `BP_EXTRA_FIELDS` + `BD_EXTRA_FIELDS` |
| 5 | `OPERATE_DATE` 日期格式 | `budget_service.py` | `_format_date()` 转为 `yyyy/M/d H:mm:ss` |
| 6 | 字符串 null 未转 '' | `budget_service.py` | `BD_STRING_FIELDS` + `_convert_bd_row()` |
| 7 | `JsonListData` 泄漏 `StaticsModel` | `budget_router.py` | `jld.model_dump()` 显式调用 |
| 8 | `OtherData` 字段缺失 | `models/base.py` | `JsonListData` 添加 `OtherData` 属性 |
| 9 | 搜索条件缺少 `BUDGETDETAIL_AH_ID` | `budget_service.py` | 补 WHERE 条件 |
| 10 | `fetch_all(null_to_empty=True)` 过度转换 | `budget_service.py` | 改为 `null_to_empty=False` |

### 关键经验

1. **先用对比脚本跑出差异，再看 C# 源码定位原因** — 不要凭猜测修改
2. **C# Model 的回显字段是最隐蔽的差异** — 对比脚本会报 `新 API 缺少该字段`
3. **`null_to_empty` 是双刃剑** — 全局开启会把非字符串列的 null 也转为 ''，应用 `_convert` 精确控制
4. **`JsonListData` 必须用 `model_dump()`** — 否则 FastAPI 序列化会泄漏 None 字段
5. **Report 类接口大概率 C# 404** — 不需要花时间修，直接标 SKIP
