# NewPython-Host

> 服务区经营管理 API（Python 版）—— 替代原 ASP.NET Web API（C# CommercialApi）

---

## 技术栈

| 项目 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.11 |
| Web 框架 | FastAPI | 0.115.0 |
| ASGI 服务器 | Uvicorn | 0.30.0 |
| 数据模型 | Pydantic | 2.9.0 |
| 数据库 | 达梦 (DM) | dmPython ≥ 2.4 |
| 缓存 | Redis | 5.0.0 |
| 加密 | PyCryptodome | 3.20.0 |
| 日志 | Loguru | 0.7.2 |

---

## 快速启动

```powershell
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器（热重载）
python main.py

# 访问
# API 服务:    http://localhost:8080
# Swagger 文档: http://localhost:8080/docs
# ReDoc 文档:   http://localhost:8080/redoc
```

---

## 项目目录结构

```
NewPython-Host/
├── main.py                         # 应用入口，注册路由与中间件
├── config.py                       # 全局配置（数据库/Redis/AES/CORS/日志）
├── requirements.txt                # Python 依赖清单
├── .gitignore
│
├── core/                           # 核心工具层
│   ├── database.py                 #   达梦数据库连接管理与查询封装（DatabaseHelper）
│   ├── aes_util.py                 #   AES 加解密工具
│   ├── des_helper.py               #   DES 加解密（兼容 C# 旧版加密）
│   ├── format_utils.py             #   日期/数值/字段格式化工具
│   └── old_api_proxy.py            #   旧 C# 接口代理转发（未平移接口透传）
│
├── models/                         # 数据模型定义
│   ├── base.py                     #   通用响应模型（Result/JsonListData/PageParams）
│   ├── common_model.py             #   业务公共模型（NestingModel 等）
│   └── base_info/                  #   BaseInfo 模块专用模型
│
├── middleware/                     # 中间件
│   ├── error_handler.py            #   全局异常处理（统一错误格式）
│   └── query_cleanup.py            #   查询参数清理（空值/格式标准化）
│
├── routers/                        # 路由层（API 接口定义）
│   ├── deps.py                     #   依赖注入（数据库连接等）
│   ├── commercial_api/             #   CommercialApi 模块（对应 C# CommercialApi）
│   │   ├── revenue_router.py       #     营收管理（50+ 接口，最大文件 ~420KB）
│   │   ├── bigdata_router.py       #     大数据分析（~175KB）
│   │   ├── base_info_router.py     #     基础信息管理
│   │   ├── examine_router.py       #     审核检查
│   │   ├── contract_router.py      #     合同管理
│   │   ├── budget_router.py        #     预算管理
│   │   ├── customer_router.py      #     客户管理
│   │   ├── analysis_router.py      #     分析报表
│   │   ├── abnormal_audit_router.py#     异常审计
│   │   ├── business_process_router.py#   业务流程
│   │   └── debug_router.py         #     调试接口
│   │
│   └── eshang_api_main/            #   EShangApiMain 模块（对应 C# EShangApiMain）
│       ├── base_info/              #     基础信息
│       ├── merchants/              #     商户管理
│       ├── contract/               #     合同
│       ├── finance/                #     财务
│       ├── revenue/                #     营收
│       ├── bigdata/                #     大数据
│       ├── auto_build/             #     自动构建
│       ├── batch_modules/          #     批量操作
│       └── video/                  #     视频管理
│
├── services/                       # 业务逻辑层
│   ├── revenue/                    #   营收相关业务逻辑
│   ├── merchants/                  #   商户相关
│   ├── contract/                   #   合同相关
│   ├── finance/                    #   财务相关
│   ├── base_info/                  #   基础信息
│   ├── business_project/           #   经营项目
│   ├── businessman/                #   经营者
│   ├── audit/                      #   审计
│   ├── analysis/                   #   分析
│   ├── bigdata/                    #   大数据
│   ├── auto_build/                 #   自动构建
│   ├── mobilepay/                  #   移动支付
│   ├── picture/                    #   图片管理
│   ├── video/                      #   视频管理
│   └── verification/               #   验证
│
├── scripts/                        # 工具脚本（开发/调试/迁移用）
│   ├── compare_*.py                #   新旧接口对比脚本
│   ├── sync_*.py                   #   Oracle → 达梦 数据同步脚本
│   ├── migrate_*.py                #   数据库迁移脚本
│   ├── test_*.py                   #   接口测试脚本
│   ├── verify_*.py                 #   验证脚本
│   ├── check_*.py                  #   数据/结构检查脚本
│   └── baseline/                   #   基线数据（旧接口响应缓存）
│
├── docs/                           # 项目文档
│   ├── 接口平移知识手册.md           #   C#→Python 平移标准参考（唯一源）
│   └── _archived/                  #   归档的历史过程性文档
│
├── logs/                           # 运行日志（按日期滚动）
├── workLog/                        # 工作日志
└── tmp_compare/                    # 临时对比数据（可清理）
```

---

## 架构说明

### 请求处理流程

```
客户端请求
  → FastAPI (main.py)
    → 中间件 (middleware/)
      → 路由层 (routers/)
        → 业务逻辑层 (services/)  [可选]
          → 核心工具层 (core/database.py)
            → 达梦数据库
```

### 两套路由模块

本项目平移了 C# 旧系统的两个独立 API 项目：

| 模块 | 路由前缀 | 说明 |
|------|---------|------|
| `commercial_api/` | `/CommercialApi/` | 商业经营管理（营收、合同、审核等） |
| `eshang_api_main/` | `/EShangApiMain/` | 基础信息、商户、财务等 |

### 数据库访问

- **主库**: 达梦数据库 (DM) — 通过 `core/database.py` 的 `DatabaseHelper` 类访问
- **缓存**: Redis — 营收趋势等高频查询的缓存
- **旧库**: Oracle — 仅用于验证测试（`core/old_api_proxy.py` 可透传未平移接口）

---

## 配置说明

通过环境变量或 `.env` 文件配置，主要配置项：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `DM_HOST` | `192.168.1.99` | 达梦数据库地址 |
| `DM_PORT` | `5236` | 达梦端口 |
| `DM_USER` | `NEWPYTHON` | 数据库用户 |
| `DM_PASSWORD` | `NewPython@2025` | 数据库密码 |
| `REDIS_HOST` | `127.0.0.1` | Redis 地址 |
| `LOG_LEVEL` | `INFO` | 日志级别 |
| `DEBUG` | `True` | 调试模式 |

---

## 相关文档

- [接口平移知识手册](docs/接口平移知识手册.md) — C# → Python 平移过程中的所有问题、坑、技术栈差异和业务逻辑对照
- [迁移完成接口文档](迁移完成接口文档_FastAPI.md) — 已完成平移的接口列表
- [EShangApiMain 接口文档](EShangApiMain接口文档.md) — EShangApiMain 模块接口详情
