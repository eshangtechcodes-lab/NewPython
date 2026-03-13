---
description: 接口调试排错标准流程（API 报错 → 定位根因 → 修复 → 验证）
---

# 接口调试排错工作流

> 当 API 返回非预期结果（500 错误、422 参数校验、数据不一致等）时，按此流程操作。

// turbo-all

## 步骤 1：确认错误现象

### 1.1 记录错误信息

```powershell
# 调用出错接口，获取完整响应
Invoke-RestMethod -Uri "http://localhost:8080/EShangApiMain/XXX/GetYYY" -Method Post -Body '{}' -ContentType 'application/json' 2>&1 | ConvertTo-Json -Depth 5
```

记录以下信息：

| 项目 | 值 |
|------|-----|
| 接口路径 | |
| HTTP 状态码 | |
| Result_Code | |
| 错误消息 | |
| 请求参数 | |

### 1.2 分类错误类型

| HTTP 状态 | 含义 | 大概率原因 |
|-----------|------|-----------|
| 422 | 参数校验失败 | Pydantic 模型定义问题或参数名大小写 |
| 500 | 服务器内部错误 | SQL 报错、Python 异常 |
| 404 | 路由未找到 | 未注册到 main.py 或路径大小写不对 |
| 200 + Code=101 | 业务失败 | SQL 查询返回空或逻辑错误 |

---

## 步骤 2：查看服务端日志

```powershell
# 查看最近的错误日志（uvicorn 终端输出）
# 如果使用 loguru 日志文件
Get-Content D:\AISpace\EShangPython\logs\app.log -Tail 50
```

关键信息：
- **Traceback** — Python 异常堆栈
- **SQL Error** — 数据库查询错误（表不存在、字段不存在、语法错误）
- **ValidationError** — Pydantic 参数校验详情

---

## 步骤 3：定位根因

### 3.1 SQL 错误

```powershell
# 直接在达梦中执行 SQL，验证是否报错
python -c "
import dmPython
conn = dmPython.connect(user='NEWPYTHON', password='NewPython@2025', server='192.168.1.99', port=5236)
cur = conn.cursor()
cur.execute('你的 SQL 语句')
print(cur.fetchall()[:5])
conn.close()
"
```

### 3.2 路由/参数问题

```powershell
# 列出所有已注册路由确认路径
python -c "
import sys; sys.path.insert(0, '.'); 
# 检查 main.py 中的路由注册
import re
content = open('main.py', 'r', encoding='utf-8').read()
for m in re.finditer(r'prefix=\"([^\"]+)\"', content):
    print(m.group(1))
"
```

### 3.3 对比原 C# 接口

```powershell
# 调原 API 确认预期行为
Invoke-RestMethod -Uri "http://192.168.1.99:8900/EShangApiMain/XXX/GetYYY" -Method Post -Body '{}' -ContentType 'application/json' | ConvertTo-Json -Depth 5
```

---

## 步骤 4：修复并验证

1. 修改代码（Service / Router / Model）
2. 重启服务

```powershell
Get-Process -Name python -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
python main.py
```

3. 重新调用接口确认修复
4. 如果涉及数据对比，运行对比脚本：

```powershell
python scripts/compare/compare_api.py --manifest scripts/manifests/_tmp_xxx.json
```

---

## 常见问题速查

| 错误提示 | 根因 | 修复 |
|---------|------|------|
| `无效的表或视图名[T_XXX]` | 达梦中表不存在 | 执行 `python scripts/migrate/server_migrate.py T_XXX` |
| `列[XXX_COLUMN]无效` | SQL 字段名拼写错误 | 核对原 Helper SQL |
| `value is not a valid dict` | POST Body 格式不对 | 检查 Pydantic 模型定义 |
| `name 'xxx' is not defined` | Service 中变量未定义 | 检查 import 和常量名 |
| `Too many values to unpack` | `execute_query` 返回值解构错误 | 检查函数签名 |
| `DPI-1047: Cannot locate a 64-bit Oracle Client` | Oracle 驱动路径 | 设置 `oracle_client` 路径 |
