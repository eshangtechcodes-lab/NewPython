# Session3 工作日志 — Merchants 模块接口差异修复

> 时间: 2026-03-10 17:00 ~ 17:29

## 成果概览

Merchants 模块 7 个接口，从 **PASS 0 → PASS 3**。

| 接口 | 修复前差异 | 修复后 | 状态 |
|---|---|---|---|
| GetCoopMerchantsLinkerDetail | 7 处 | 0 处 | ✅ PASS |
| GetCoopMerchantsLinkerList | 1 处 | 0 处 | ✅ PASS |
| GetCoopMerchantsTypeList | 2 处 | 0 处 | ✅ PASS |
| GetCoopMerchantsDetail | 12 处 | **2 处** | ❌ 待修 |
| GetCoopMerchantsList | 3 处 | **1 处** | ❌ 待修 |
| GetRTCoopMerchantsList | — | C# 端 404 | ❌ 原接口不存在 |
| GetTradeBrandMerchantsList | — | C# 端 415+SQL错误 | ❌ 原接口异常 |

## 已修改的文件（4 个）

### 1. core/database.py
- `execute_query` 加了 `null_to_empty` 参数（默认 True）
  - True = 字符串列 NULL→''（C# List 的 .ToString() 行为）
  - False = null 保持 null（C# Detail 的 entity 属性赋值行为）
- 日期格式转换改为 `datetime→v.isoformat()`（C# 端实际输出 ISO 格式，之前错误地转成了 yyyy/M/d 格式）

### 2. services/merchants/coopmerchants_service.py
- 加 `_STR_FIELDS` 字符串字段集合 + `_bind_coopmerchants_row`（List 用，None→''）
- Detail 查询传 `null_to_empty=False`
- List 中去掉多余的 BrandList 查询（C# List 没有 BrandList，改为 None）
- LINKER 无数据时默认值改为 `""` 而非 `None`
- LINKER 查询排序改为 `ORDER BY OPERATE_DATE DESC`

### 3. services/merchants/coopmerchants_linker_service.py
- 加 `_STR_FIELDS` + `_bind_linker_row`（List 用）
- Detail 查询传 `null_to_empty=False`

### 4. routers/eshang_api_main/merchants/merchants_router.py
- TypeList 的 `_bind_autostatistics_model` 中去掉日期格式化

## 剩余待修问题（3 个具体修法）

### 问题1: GetCoopMerchantsDetail — 2 差异
- `LINKER_NAME`: C# 返回 null，Python 返回 '杨雅意'
- `LINKER_MOBILEPHONE`: C# 返回 null，Python 返回 '0571-81991302'
- **原因**: C# Detail 不查 LINKER 表（Model 属性默认 null），Python 多查了
- **修法**: `coopmerchants_service.py` 的 `get_coopmerchants_detail` 函数中，把 LINKER 查询代码（约 line 224-240）替换为:
  ```python
  detail["LINKER_NAME"] = None
  detail["LINKER_MOBILEPHONE"] = None
  ```

### 问题2: GetCoopMerchantsList — 1 差异
- `COOPMERCHANTS_PID`: C# 返回 0 (int)，Python 返回 None
- **原因**: `_bind_coopmerchants_row` 中有一段错误逻辑把 PID=0 改成了 None
- **修法**: 删掉 `_bind_coopmerchants_row` 中这 4 行:
  ```python
  # C# TryParseToInt() 对 DBNull 返回 null...
  pid = row.get("COOPMERCHANTS_PID")
  if pid is not None and (pid == 0 or pid == 0.0):
      row["COOPMERCHANTS_PID"] = None
  ```

### 问题3: RTCoopMerchantsList + TradeBrandMerchantsList
- C# 端分别返回 404 / 415，原接口不可用
- **修法**: 在 `scripts/manifests/modules/merchants.json` 中这两个接口加 `"enabled": false`

## 验证命令

```bash
# 修改后杀掉所有 python 进程重启
Get-Process | Where-Object { $_.ProcessName -like '*python*' } | Stop-Process -Force
Start-Sleep -Seconds 2
Start-Process python -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080" -WorkingDirectory "E:\workfile\JAVA\NewAPI" -NoNewWindow
Start-Sleep -Seconds 12

# 运行对比
python scripts/compare_api.py --manifest scripts/manifests/modules/merchants.json --report docs/session3_merchants_final.md
```

目标: **PASS 5 / SKIP 2**

## 关键注意事项

1. **对比脚本方向**: old(C#) vs new(Python)，即 `NoneType vs str` = C# 返回 None, Python 返回 str
2. **database.py 全局转换会影响所有接口**: NULL→'' 和日期格式在 DB 层做，service 层再改无效
3. **C# 实际返回 ISO 日期**: 不要做 ISO→C# 格式转换
4. **修改后必须杀掉所有 python 进程重启才生效**
5. **database.py 日期改动是全局的**: 可能影响其他模块，修完 Merchants 后需要跑全量对比确认
