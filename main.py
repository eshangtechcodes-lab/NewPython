# -*- coding: utf-8 -*-
"""
EShangApi - FastAPI 应用入口
替代原 ASP.NET Web API 项目
"""
import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import settings
from middleware.error_handler import (
    global_exception_handler,
    validation_exception_handler,
    http_exception_handler
)

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

# 全局异常处理 — PKG-RESP-CORE-01: 注册三种处理器，确保所有错误都返回 Result 格式
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# 查询参数清洗中间件（兼容 C# ASP.NET 的空字符串参数行为）
from middleware.query_cleanup import QueryParamCleanupMiddleware
app.add_middleware(QueryParamCleanupMiddleware)

# === 注册路由 ===

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

# FinanceController 相关路由（附件上传 CRUD）
from routers.eshang_api_main.finance.fattachment_router import router as fattachment_router
app.include_router(fattachment_router, prefix="/EShangApiMain", tags=["附件上传 (Finance ATTACHMENT)"])

# FinanceController 散装接口路由（44 个报表/审批/固化接口）
from routers.eshang_api_main.finance.finance_scattered_router import router as finance_scattered_router
app.include_router(finance_scattered_router, prefix="/EShangApiMain", tags=["财务散装接口 (Finance Scattered)"])

# InvoiceController 路由（BILL/BILLDETAIL CRUD + 散装接口）
from routers.eshang_api_main.finance.invoice_router import router as invoice_router
app.include_router(invoice_router, prefix="/EShangApiMain", tags=["票据管理 (InvoiceController)"])

# BudgetProjectAHController 路由（预算项目/明细 CRUD + 报表接口）
from routers.eshang_api_main.finance.budget_router import router as budget_router
app.include_router(budget_router, prefix="/EShangApiMain", tags=["财务预算 (BudgetProjectAHController)"])

# RevenueController 路由（营收数据 7组CRUD + 31散装报表）
from routers.eshang_api_main.revenue.revenue_router import router as revenue_router
app.include_router(revenue_router, prefix="/EShangApiMain", tags=["营收管理 (RevenueController)"])

# BigData + Customer 路由（大数据车流 8组CRUD + 散装接口）
from routers.eshang_api_main.bigdata.bigdata_router import router as bigdata_router
app.include_router(bigdata_router, prefix="/EShangApiMain", tags=["大数据车流 (BigDataController)"])

# Audit + MobilePay 路由
from routers.eshang_api_main.batch_modules.batch_router_part1 import audit_router, mobilepay_router
app.include_router(audit_router, prefix="/EShangApiMain", tags=["审核管理 (AuditController)"])
app.include_router(mobilepay_router, prefix="/EShangApiMain", tags=["移动支付 (MobilePayController)"])

# Analysis + BusinessMan + DataVerification + Picture 路由
from routers.eshang_api_main.batch_modules.batch_router_part2 import (
    analysis_router, businessman_router, verification_router, picture_router
)
app.include_router(analysis_router, prefix="/EShangApiMain", tags=["经营分析 (AnalysisController)"])
app.include_router(businessman_router, prefix="/EShangApiMain", tags=["商家管理 (BusinessManController)"])
app.include_router(verification_router, prefix="/EShangApiMain", tags=["数据核实 (VerificationController)"])
app.include_router(picture_router, prefix="/EShangApiMain", tags=["图片管理 (PictureController)"])

# ShopVideoController 路由（视频监控 16 接口）
from routers.eshang_api_main.video.video_router import router as video_router
app.include_router(video_router, prefix="/EShangApiMain", tags=["视频监控 (ShopVideoController)"])


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
