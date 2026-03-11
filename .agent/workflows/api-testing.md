---
description: CommercialApi 新旧接口数据对比测试工作流（基于基线缓存）
---

# CommercialApi 接口对比测试工作流

> 适用于 CommercialApi 新旧接口数据对比验证。采用「基线缓存」策略解决旧 API 响应慢的问题。
>
> ⚠️ **核心原则**：旧 C# API 因 WCF 中间层架构极慢（单次对比 60 分钟+），因此旧 API 的响应数据缓存在本地 JSON 文件中，后续对比只需调新 API。

## 前置条件

- 新 Python API 服务已启动：`http://127.0.0.1:8080/CommercialApi`
  - 启动方式：在 `d:\Projects\Python\eshang_api` 目录下执行 `python main.py`
- 原 C# API 服务（仅基线采集时需要）：`http://127.0.0.1:8900/CommercialApi`
- 接口文档路径：`D:\CSharp\Project\000_通用版本\000_通用版本\030_EShangApi\docs\CommercialApi接口文档说明.md`
- 基线缓存文件：`scripts/test_results/baseline_cache.json`

---

## 测试脚本清单

| 脚本 | 用途 | 频率 |
|------|------|------|
| `scripts/baseline_collect.py` | 并发采集旧 API 全部响应缓存到 JSON | 一次性（数据变化时重采） |
| `scripts/compare_cached.py` | 读缓存 + 调新 API → 快速对比 | 每次迭代后运行 |
| `scripts/compare_all.py` | 串行实时对比新旧 API（慢，备用） | 全量验证时用 |
| `scripts/perf_check_old_api.py` | 旧 API 性能基准测试 | 仅分析性能时用 |

---

## 快速测试流程（日常使用）

### Step 1：检查基线缓存是否存在

// turbo

```powershell
Test-Path scripts/test_results/baseline_cache.json
```

如果返回 `True` → 直接跳到 Step 3。
如果返回 `False` → 执行 Step 2。

### Step 2：采集旧 API 基线数据（仅首次或数据变化时）

> ⚠️ 需要原 C# API 在 8900 端口运行。耗时约 15 分钟。

// turbo

```powershell
python scripts/baseline_collect.py
```

**参数说明：**
- `MAX_WORKERS = 2`：并发线程数（旧 API WCF 架构不支持高并发，>2 会 HTTP 500）
- `TIMEOUT = 90`：超时秒数（给旧 API 充分响应时间）
- 输出：`scripts/test_results/baseline_cache.json`

**预期结果：**
- 成功 ~42 个接口获得有效响应数据
- 超时 ~6 个（旧 API 自身瓶颈，无法解决）
- HTTP 错误 ~76 个（旧 API 404/405 等，说明这些路由在旧 API 中不存在）

### Step 3：运行缓存对比

// turbo

```powershell
python scripts/compare_cached.py
```

**预期耗时：~3 分钟（仅调新 API）**
**输出文件：`scripts/test_results/compare_cached.json`**

### Step 4：分析结果

关注以下几类结果：

| 结果 | 含义 | 处理方式 |
|------|------|----------|
| ✅ PASS | 新旧完全一致 | 无需处理 |
| ❌ DIFF | 存在差异 | 需分析是否需要修复（见分类规则） |
| ⏭️ SKIP | 旧 API 本身 404/500/超时 | 无法对比，可跳过 |
| 🆕 NEW_ONLY | 新增路由无基线缓存 | 需重新采集基线 |
| ⚠️ WARN | Code 一致但数据字段有差异 | 检查字段级差异 |

---

## DIFF 分类规则

### 🟢 可忽略的 DIFF

**旧 API 返回 C=999，新 API 返回 C=100/101**

这类差异出现在 **AES 加密接口**上。测试时传空参数 `{"name": "", "value": ""}`：
- 旧 API 需要 AES 加密后的参数才能解析，收到空参数返回 999（参数错误）
- 新 API 实现了不加密的直接调用逻辑，返回正常结果

**涉及的接口**（约 14 个）：
- `AbnormalAudit/GetCurrentEarlyWarning`, `AbnormalAudit/GetMonthEarlyWarning`
- `BaseInfo/GetServerpartServiceSummary`, `BaseInfo/GetBrandStructureAnalysis`
- `Analysis/GetServerpartTypeAnalysis`
- `Revenue/GetBusinessRevenueList`, `Revenue/GetMonthlyBusinessRevenue`
- `SupplyChain` 全部 5 个接口

### 🟡 数据差异（需关注）

**TotalCount 略有不同（差几条）**

- 原因：Oracle 和达梦数据可能不完全同步
- 处理：确认是否为数据同步问题；若差异 < 5%，可接受

### 🔴 需修复

**新 API 返回 HTTP 422 或 C=101（参数校验失败）**

- 原因：参数名大小写不匹配或 Pydantic 模型校验过严
- 处理：对照接口文档修正参数定义

---

## 接口文档参考

接口文档位置：`D:\CSharp\Project\000_通用版本\000_通用版本\030_EShangApi\docs\CommercialApi接口文档说明.md`

文档包含：
- 每个接口的精确参数定义（类型、必填、说明）
- 完整测试用例（包含真实请求URL和参数）
- 预期响应数据结构
- 参考耗时基准

**使用规范：**
1. 实现新接口前，先查阅文档确认参数格式和预期返回
2. 对比测试时，用文档中的测试用例验证关键接口
3. 文档地址中的基础 URL 需替换为本地地址：
   - 原文档：`https://api.eshangtech.com/CommercialApi/`
   - 旧 API：`http://127.0.0.1:8900/CommercialApi/`
   - 新 API：`http://127.0.0.1:8080/CommercialApi/`

---

## 单接口手动测试

如果需要针对某个具体接口做精确对比（不用全量跑），可以用以下方式：

### GET 接口

```powershell
# 旧 API（从缓存读取，打开 baseline_cache.json 搜索对应 key）
# 新 API（实时调用）
Invoke-RestMethod -Uri "http://127.0.0.1:8080/CommercialApi/BaseInfo/GetSPRegionList?Province_Code=340000" | ConvertTo-Json -Depth 5
```

### POST 接口（普通）

```powershell
$body = '{"PageIndex":1,"PageSize":10,"SearchParameter":{"SERVERPART_IDS":"416"}}'
Invoke-RestMethod -Uri "http://127.0.0.1:8080/CommercialApi/Examine/GetEXAMINEList" -Method Post -Body $body -ContentType 'application/json' | ConvertTo-Json -Depth 5
```

### POST 接口（AES 加密）

AES 加密接口的测试需要先加密参数，加密配置在 `Web.config` 中：
- AES Key: `7tRqYw4XgL9Kv2Ef`
- AES IV: `P5mDn8ZsB3HjT6cN`

---

## 已知旧 API 特性

### 性能特性

| 分类 | 接口数 | 说明 |
|------|--------|------|
| ⏰ 超时(>60s) | 9 | WCF 链路 + 大数据量 |
| 🔴 极慢(>10s) | 2 | `GetANALYSISINSList`(40.8s), `GetBUDGETPROJECT_AHList`(16.8s) |
| 🟡 慢(5-10s) | 3 | `GetSPRegionList`(6.2s), `GetBusinessTradeList`(9.5s) |
| ✅ 正常(<2s) | 37 | 大部分快速接口 |

### 架构瓶颈（不可优化，已通过迁移解决）

- 旧 API 不直连 Oracle，通过 WCF 中间层（`wsHttpBinding` + 证书认证）
- 每请求新建 `Transaction` 对象（含 WCF 通道初始化）
- ORM 使用 `DataTable` 重量级序列化
- 并发能力弱，>2 线程就会 HTTP 500

### 旧 API 不可用的接口

以下接口在旧 API 中返回 404（路由不存在），无法做数据对比：
- 大部分 Revenue GET 接口（旧 API 只有 POST 版本）
- BigData 的大量 GET 接口
- Contract、BusinessProcess、Suggestion 全部
- Customer 的 GET 接口

---

## 重新采集基线的时机

以下情况需要重新运行 `baseline_collect.py`：

1. Oracle 源数据发生了大规模变更
2. 旧 API 修复了某些 Bug，需要获取新的正确响应
3. 新增了路由（`compare_cached.py` 会显示为 `NEW_ONLY`）
4. 对比中发现基线数据可能不准确

---

## 2026-03-05 基线测试报告摘要

总路由 123 个，有效对比 42 个：

| 类别 | 数量 | 比例 |
|------|------|------|
| ✅ 完全一致(PASS) | 20 | 47.6% |
| 🟢 可忽略差异(加密接口) | 14 | 33.3% |
| 🟡 数据微小差异 | 6 | 14.3% |
| 🔴 需修复 | 2 | 4.8% |

**80.9% 的有效接口功能正确。**
