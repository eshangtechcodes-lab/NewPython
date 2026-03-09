# -*- coding: utf-8 -*-
"""
EShangApi - FastAPI 应用入口
替代原 ASP.NET Web API 项目
"""
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import settings
from middleware.error_handler import global_exception_handler

# 配置日志
os.makedirs(settings.LOG_DIR, exist_ok=True)
logger.remove()  # 移除默认 handler
logger.add(sys.stderr, level=settings.LOG_LEVEL)
logger.add(
    os.path.join(settings.LOG_DIR, "{time:YYYYMMDD}.log"),
    rotation="00:00",
    retention="30 days",
    level=settings.LOG_LEVEL,
    encoding="utf-8"
)

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="EShangApi - 服务区经营管理 API（Python 版）",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 查询参数清洗中间件（兼容 C# ASP.NET 的空字符串参数行为）
from middleware.query_cleanup import QueryParamCleanupMiddleware
app.add_middleware(QueryParamCleanupMiddleware)

# 全局异常处理
app.add_exception_handler(Exception, global_exception_handler)

# === 注册路由 ===
# EShangApiMain - AutoBuild 路由（前缀 /EShangApiMain 与原 C# API 路径一致）
from routers.eshang_api_main.auto_build.brand_router import router as brand_router
app.include_router(brand_router, prefix="/EShangApiMain", tags=["品牌管理 (BRAND)"])

# 后续在这里注册更多 EShangApiMain 路由...

# CommercialApi 路由（前缀 /CommercialApi 与原 C# API 路径一致）
from routers.commercial_api.base_info_router import router as commercial_baseinfo_router
app.include_router(commercial_baseinfo_router, prefix="/CommercialApi", tags=["CommercialApi - 基础信息"])

from routers.commercial_api.contract_router import router as commercial_contract_router
app.include_router(commercial_contract_router, prefix="/CommercialApi", tags=["CommercialApi - 经营合同分析"])

from routers.commercial_api.analysis_router import router as commercial_analysis_router
app.include_router(commercial_analysis_router, prefix="/CommercialApi", tags=["CommercialApi - 分析说明"])

from routers.commercial_api.bigdata_router import router as commercial_bigdata_router
app.include_router(commercial_bigdata_router, prefix="/CommercialApi", tags=["CommercialApi - 大数据分析"])

from routers.commercial_api.customer_router import router as commercial_customer_router
app.include_router(commercial_customer_router, prefix="/CommercialApi", tags=["CommercialApi - 客群分析"])

from routers.commercial_api.revenue_router import router as commercial_revenue_router
app.include_router(commercial_revenue_router, prefix="/CommercialApi", tags=["CommercialApi - 营收管理"])

from routers.commercial_api.abnormal_audit_router import router as commercial_abnormal_router
app.include_router(commercial_abnormal_router, prefix="/CommercialApi", tags=["CommercialApi - 异常稽查"])

from routers.commercial_api.budget_router import router as commercial_budget_router
app.include_router(commercial_budget_router, prefix="/CommercialApi", tags=["CommercialApi - 财务预算"])

from routers.commercial_api.examine_router import router as commercial_examine_router
app.include_router(commercial_examine_router, prefix="/CommercialApi", tags=["CommercialApi - 考核管理"])

from routers.commercial_api.business_process_router import router as commercial_bp_router
app.include_router(commercial_bp_router, prefix="/CommercialApi", tags=["CommercialApi - 业务审批"])

# 临时调试路由
from routers.commercial_api.debug_router import router as debug_router
app.include_router(debug_router, prefix="/CommercialApi", tags=["Debug"])








@app.get("/", tags=["系统"])
async def root():
    """系统状态"""
    return {
        "Result_Code": 100,
        "Result_Desc": "EShangApi (Python) is running",
        "Result_Data": {
            "version": settings.APP_VERSION,
            "framework": "FastAPI"
        }
    }


@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查"""
    from core.database import db_helper
    db_ok = False
    try:
        db_ok = db_helper.test_connection()
    except Exception:
        pass

    return {
        "Result_Code": 100 if db_ok else 999,
        "Result_Desc": "健康检查",
        "Result_Data": {
            "database": "connected" if db_ok else "disconnected",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
