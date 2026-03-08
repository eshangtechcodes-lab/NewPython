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

# 全局异常处理
app.add_exception_handler(Exception, global_exception_handler)

# === 注册路由 ===
# EShangApiMain - BaseInfo 路由（前缀 /EShangApiMain 与原 C# API 路径一致）
from routers.eshang_api_main.base_info.ownerunit_router import router as ownerunit_router
app.include_router(ownerunit_router, prefix="/EShangApiMain", tags=["业主单位管理 (OWNERUNIT)"])

from routers.eshang_api_main.base_info.serverpart_router import router as serverpart_router
app.include_router(serverpart_router, prefix="/EShangApiMain", tags=["服务区站点 (SERVERPART)"])

from routers.eshang_api_main.base_info.serverpartshop_router import router as serverpartshop_router
app.include_router(serverpartshop_router, prefix="/EShangApiMain", tags=["门店管理 (SERVERPARTSHOP)"])

from routers.eshang_api_main.base_info.brand_router import router as brand_router
app.include_router(brand_router, prefix="/EShangApiMain", tags=["品牌管理 (BRAND)"])

from routers.eshang_api_main.base_info.rtserverpartshop_router import router as rtserverpartshop_router
app.include_router(rtserverpartshop_router, prefix="/EShangApiMain", tags=["门店经营时间 (RTSERVERPARTSHOP)"])

from routers.eshang_api_main.base_info.serverpartshop_log_router import router as serverpartshop_log_router
app.include_router(serverpartshop_log_router, prefix="/EShangApiMain", tags=["门店变更日志 (SERVERPARTSHOP_LOG)"])

from routers.eshang_api_main.base_info.cashworker_router import router as cashworker_router
app.include_router(cashworker_router, prefix="/EShangApiMain", tags=["收银人员 (CASHWORKER)"])

from routers.eshang_api_main.base_info.businesstrade_router import router as businesstrade_router
app.include_router(businesstrade_router, prefix="/EShangApiMain", tags=["经营业态 (BusinessTrade)"])

from routers.eshang_api_main.base_info.autostatistics_router import router as autostatistics_router
app.include_router(autostatistics_router, prefix="/EShangApiMain", tags=["自定义统计归口 (AUTOSTATISTICS)"])

from routers.eshang_api_main.base_info.commoditytype_router import router as commoditytype_router
app.include_router(commoditytype_router, prefix="/EShangApiMain", tags=["商品类别 (COMMODITYTYPE)"])

from routers.eshang_api_main.base_info.userdefinedtype_router import router as userdefinedtype_router
app.include_router(userdefinedtype_router, prefix="/EShangApiMain", tags=["商品自定义类别 (USERDEFINEDTYPE)"])

from routers.eshang_api_main.base_info.serverpartcrt_router import router as serverpartcrt_router
app.include_router(serverpartcrt_router, prefix="/EShangApiMain", tags=["服务区成本核算对照 (SERVERPARTCRT)"])

from routers.eshang_api_main.base_info.propertyassets_router import router as propertyassets_router
app.include_router(propertyassets_router, prefix="/EShangApiMain", tags=["服务区资产 (PROPERTYASSETS)"])

from routers.eshang_api_main.base_info.commodity_router import router as commodity_router
app.include_router(commodity_router, prefix="/EShangApiMain", tags=["在售商品 (COMMODITY)"])

from routers.eshang_api_main.base_info.base_info_misc_router import router as base_info_misc_router
app.include_router(base_info_misc_router, prefix="/EShangApiMain", tags=["基础信息-散装接口 (BaseInfo Misc)"])

from routers.eshang_api_main.base_info.propertyassetslog_router import router as propertyassetslog_router
app.include_router(propertyassetslog_router, prefix="/EShangApiMain", tags=["资产操作日志 (PROPERTYASSETSLOG)"])

from routers.eshang_api_main.base_info.serverpartshop_new_router import router as serverpartshop_new_router
app.include_router(serverpartshop_new_router, prefix="/EShangApiMain", tags=["门店管理-业主端 (ServerPartShopNew)"])

from routers.eshang_api_main.base_info.propertyshop_router import router as propertyshop_router
app.include_router(propertyshop_router, prefix="/EShangApiMain", tags=["物业资产与商户对照 (PROPERTYSHOP)"])

# BasicConfigController 相关路由
from routers.eshang_api_main.base_info.autotype_router import router as autotype_router
app.include_router(autotype_router, prefix="/EShangApiMain", tags=["自定义类别 (AUTOTYPE)"])

from routers.eshang_api_main.base_info.ownerserverpart_router import router as ownerserverpart_router
app.include_router(ownerserverpart_router, prefix="/EShangApiMain", tags=["业主-服务区关联 (OWNERSERVERPART)"])

from routers.eshang_api_main.base_info.ownerserverpartshop_router import router as ownerserverpartshop_router
app.include_router(ownerserverpartshop_router, prefix="/EShangApiMain", tags=["业主-门店关联 (OWNERSERVERPARTSHOP)"])

from routers.eshang_api_main.base_info.serverparttype_router import router as serverparttype_router
app.include_router(serverparttype_router, prefix="/EShangApiMain", tags=["服务区类别 (SERVERPARTTYPE)"])

from routers.eshang_api_main.base_info.spstatictype_router import router as spstatictype_router
app.include_router(spstatictype_router, prefix="/EShangApiMain", tags=["服务区类别关联 (SPSTATICTYPE)"])

from routers.eshang_api_main.base_info.serverpartshopcrt_router import router as serverpartshopcrt_router
app.include_router(serverpartshopcrt_router, prefix="/EShangApiMain", tags=["服务区门店对照 (SERVERPARTSHOPCRT)"])

# 后续在这里注册更多路由...

# CommodityController 相关路由
from routers.eshang_api_main.base_info.commodity_ctrl_router import router as commodity_ctrl_router
app.include_router(commodity_ctrl_router, prefix="/EShangApiMain", tags=["商品管理 (CommodityController)"])

# ContractController 相关路由
from routers.eshang_api_main.contract.contract_router import router as contract_router
app.include_router(contract_router, prefix="/EShangApiMain", tags=["合同备案管理 (ContractController)"])

# BusinessProjectController 相关路由
from routers.eshang_api_main.contract.business_project_router import router as business_project_router
app.include_router(business_project_router, prefix="/EShangApiMain", tags=["经营项目管理 (BusinessProjectController)"])

# ShopRoyalty + SHOPROYALTYDETAIL 路由
from routers.eshang_api_main.contract.shoproyalty_router import router as shoproyalty_router
app.include_router(shoproyalty_router, prefix="/EShangApiMain", tags=["门店提成/应收拆分 (ShopRoyalty)"])

# RevenueConfirm + PaymentConfirm + RTPaymentRecord + Remarks 路由
from routers.eshang_api_main.contract.revenue_payment_router import router as revenue_payment_router
app.include_router(revenue_payment_router, prefix="/EShangApiMain", tags=["营收回款/商家应收/备注 (Revenue/Payment)"])

# 第三批：BusinessPayment + ProjectWarning + PeriodWarning + BizpSplitMonth + BusinessProjectSplit 路由
from routers.eshang_api_main.contract.bp_batch3_router import router as bp_batch3_router
app.include_router(bp_batch3_router, prefix="/EShangApiMain", tags=["经营执行/拆分/预警 (BP Batch3)"])

# 第四批：APPROVED + SHOPEXPENSE + PROJECTSPLITMONTH 路由
from routers.eshang_api_main.contract.bp_batch4_router import router as bp_batch4_router
app.include_router(bp_batch4_router, prefix="/EShangApiMain", tags=["审批/门店费用/月度拆分 (BP Batch4)"])

# 第五批a：散装接口（简单8个）
from routers.eshang_api_main.contract.bp_batch5a_router import router as bp_batch5a_router
app.include_router(bp_batch5a_router, prefix="/EShangApiMain", tags=["散装接口-简单 (BP Batch5a)"])

# 第五批b：散装接口（复杂18个）
from routers.eshang_api_main.contract.bp_batch5b_router import router as bp_batch5b_router
app.include_router(bp_batch5b_router, prefix="/EShangApiMain", tags=["散装接口-复杂 (BP Batch5b)"])

# ExpensesController 相关路由（商家预缴费用 + 费用拆分）
from routers.eshang_api_main.contract.expenses_router import router as expenses_router
app.include_router(expenses_router, prefix="/EShangApiMain", tags=["商家预缴费用 (Expenses)"])

# ContractSynController + CONTRACT_SYNController 路由（合同信息同步）
from routers.eshang_api_main.contract.contractsyn_router import router as contractsyn_router
app.include_router(contractsyn_router, prefix="/EShangApiMain", tags=["合同信息同步 (ContractSyn)"])

# MerchantsController 相关路由（经营商户/商户类型/联系人/品牌关联）
from routers.eshang_api_main.merchants.merchants_router import router as merchants_router
app.include_router(merchants_router, prefix="/EShangApiMain", tags=["商户管理 (MerchantsController)"])


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
