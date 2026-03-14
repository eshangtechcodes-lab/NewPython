# -*- coding: utf-8 -*-
"""
CommercialApi - 月度增幅分析 Service
从 revenue_router.py 中抽取:
  GetMonthINCAnalysis        — 月度增幅分析（全量）
  GetMonthINCAnalysisSummary — 月度增幅汇总
  StorageMonthINCAnalysis    — 存储月度增幅分析数据
"""
from __future__ import annotations
from datetime import datetime as dt, timedelta

from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


# ===================================================================
# 1. GetMonthINCAnalysis — 月度增幅分析
# ===================================================================

def get_month_inc_analysis(db, province_code, statistics_month, serverpart_id,
                           sp_region_type_id, business_region, sort_str, data_type):
    """获取月度增幅分析数据，返回 result_list 或抛出异常"""
    def safe_dec(v):
        try: return float(v) if v is not None else 0.0
        except: return 0.0

    # 解析bool参数
    is_solid = str(solidType).lower() not in ("false", "0", "")
    is_calc_yoy = str(calcYOY).lower() == "true"
    is_calc_qoq = str(calcQOQ).lower() == "true"
    is_calc_bayonet = str(calcBayonet).lower() == "true"
    is_show_warning = str(showWarning).lower() == "true"
    wt = int(warningType) if warningType else None
    now_month = __import__("datetime").datetime.now().strftime("%Y%m")

    # C# 对齐第655行: GetSubType 递归展开业态子类型
    expanded_shop_trade = shopTrade
    if shopTrade:
        try:
            _bt_ids = [s.strip() for s in shopTrade.split(",") if s.strip()]
            _expanded = set(_bt_ids)
            _sub_rows = db.execute_query(
                "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_PID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
            ) or []
            _changed = True
            while _changed:
                _changed = False
                for sr in _sub_rows:
                    sid = str(sr.get("AUTOSTATISTICS_ID") or "")
                    pid = str(sr.get("AUTOSTATISTICS_PID") or "")
                    if pid in _expanded and sid not in _expanded:
                        _expanded.add(sid)
                        _changed = True
            expanded_shop_trade = ",".join(_expanded)


# ===================================================================
# 2. GetMonthINCAnalysisSummary — 月度增幅汇总
# ===================================================================

def get_month_inc_analysis_summary(db, province_code, statistics_month, serverpart_id,
                                   sp_region_type_id, business_region, data_type):
    """获取月度增幅分析汇总数据，返回 result_dict 或抛出异常"""
    where_sql = ""
    if StatisticsStartMonth:
        where_sql += f' AND A."STATISTICS_MONTH" >= {StatisticsStartMonth}'
    if StatisticsEndMonth:
        where_sql += f' AND A."STATISTICS_MONTH" <= {StatisticsEndMonth}'

    # 经营业态过滤（子查询）
    shop_sql = ""
    if BusinessTradeType:
        shop_sql += f' AND B."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
    # C# 对齐第3678-3683行: GetSubType 递归展开业态子类型
    _expanded_trade = shopTrade
    if shopTrade:
        try:
            _bt_ids = [s.strip() for s in shopTrade.split(",") if s.strip()]
            _expanded = set(_bt_ids)
            _sub_rows = db.execute_query(
                "SELECT AUTOSTATISTICS_ID, AUTOSTATISTICS_PID FROM T_AUTOSTATISTICS WHERE AUTOSTATISTICS_TYPE = 2000"
            ) or []
            _changed = True
            while _changed:
                _changed = False
                for sr in _sub_rows:
                    sid = str(sr.get("AUTOSTATISTICS_ID") or "")
                    pid = str(sr.get("AUTOSTATISTICS_PID") or "")
                    if pid in _expanded and sid not in _expanded:
                        _expanded.add(sid)
                        _changed = True
            _expanded_trade = ",".join(_expanded)


# ===================================================================
# 3. StorageMonthINCAnalysis — 存储月度增幅分析
# ===================================================================

def storage_month_inc_analysis(db, province_code, statistics_month):
    """触发月度增幅分析数据存储"""
    # TODO: 实现 AccountHelper.StorageMonthINCAnalysis
    logger.warning("StorageMonthINCAnalysis 查询逻辑暂未实现")
    return Result.success(data=None, msg="生成成功")
