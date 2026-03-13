# -*- coding: utf-8 -*-
"""
CommercialApi Service 包 — 统一导出

用法:
    from services.commercial import service_utils
    from services.commercial.revenue_push_service import get_revenue_push_list
"""

# 公共工具
from services.commercial.service_utils import (  # noqa: F401
    safe_float, safe_int,
    get_province_id, build_sp_where,
    format_date_no_pad, format_date_short,
)

# Service 模块清单（按功能分组）
# ── Batch 1-3: Router 已瘦身，直接调用 Service ──
# analysis_service, base_info_service, budget_service,
# contract_service, customer_service, examine_service

# ── Batch 4a: BigData 框架 ──
# bigdata_bayonet_service, bigdata_month_service,
# bigdata_warning_service, bigdata_detail_service

# ── Batch 4b: Revenue 框架 ──
# revenue_push_service, revenue_brand_service,
# revenue_budget_service, revenue_transaction_service,
# revenue_trend_service, revenue_holiday_service
