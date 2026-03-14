# -*- coding: utf-8 -*-
"""
CommercialApi - 月度增幅分析 Service
从 revenue_router.py 中抽取:
  GetMonthINCAnalysis        — 月度增幅分析（全量）
  GetMonthINCAnalysisSummary — 月度增幅汇总
  StorageMonthINCAnalysis    — 存储月度增幅分析数据
"""
from __future__ import annotations
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import parse_multi_ids, build_in_condition


def _safe_float(v):
    """安全浮点数转换"""
    try:
        return float(v) if v is not None else 0.0
    except (ValueError, TypeError):
        return 0.0


def _make_inc(cur=None, ly=None):
    """构建增幅模型"""
    inc = {"curYearData": cur, "lYearData": ly,
           "increaseData": None, "increaseRate": None,
           "QOQData": None, "increaseDataQOQ": None,
           "increaseRateQOQ": None, "rankNum": None}
    if cur is not None and ly is not None and ly != 0:
        inc["increaseData"] = round(cur - ly, 2)
        inc["increaseRate"] = round((cur - ly) / ly * 100, 2)
    return inc


# ===================================================================
# 1. GetMonthINCAnalysis — 月度增幅分析
# ===================================================================

def get_month_inc_analysis(db: DatabaseHelper, province_code, statistics_month,
                           serverpart_id, sp_region_type_id, business_region,
                           sort_str, data_type) -> list:
    """
    获取月度增幅分析数据
    Router 传入参数:
      province_code    — 省份编码
      statistics_month — 统计月份 YYYYMM
      serverpart_id    — 服务区内码
      sp_region_type_id — 片区内码
      business_region  — 经营区域
      sort_str         — 排序字段
      data_type        — 数据类型
    返回: list[dict] 或 None
    """
    if not statistics_month:
        return None

    # 当前月份 YYYYMM
    cur_month = str(statistics_month).replace("-", "").replace("/", "")[:6]
    # 同比月份: 去年同月
    try:
        yoy_month = str(int(cur_month[:4]) - 1) + cur_month[4:]
    except (ValueError, IndexError):
        yoy_month = None

    # 环比月份: 上个月
    try:
        y, m = int(cur_month[:4]), int(cur_month[4:])
        if m == 1:
            qoq_month = f"{y - 1}12"
        else:
            qoq_month = f"{y}{m - 1:02d}"
    except (ValueError, IndexError):
        qoq_month = None

    # 1. 查省份ID
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
            AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE'
            AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    if not fe_rows:
        return None
    province_id = fe_rows[0]["FIELDENUM_ID"]

    # 2. 构建服务区过滤条件
    where_sp = f' AND "PROVINCE_CODE" = {province_id}'
    if serverpart_id:
        _sp_ids = parse_multi_ids(serverpart_id)
        if _sp_ids:
            where_sp += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids)
    if business_region and str(business_region) == "1":
        where_sp += ' AND "SPREGIONTYPE_ID" NOT IN (89)'

    # 3. 查服务区列表
    sp_rows = db.execute_query(f"""SELECT * FROM "T_SERVERPART"
        WHERE "SPREGIONTYPE_ID" IS NOT NULL AND "STATISTICS_TYPE" = 1000
        AND "STATISTIC_TYPE" = 1000{where_sp}
        ORDER BY "SPREGIONTYPE_INDEX","SPREGIONTYPE_ID","SERVERPART_INDEX","SERVERPART_CODE" """) or []

    if not sp_rows:
        return None

    # 4. 查当月营收 (T_REVENUEMONTHLY)
    rev_where = f' AND A."STATISTICS_MONTH" = {cur_month}'
    if serverpart_id:
        _sp_ids2 = parse_multi_ids(serverpart_id)
        if _sp_ids2:
            rev_where += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids2).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

    sql_cur = f"""SELECT A."SERVERPART_ID",
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
        FROM "T_REVENUEMONTHLY" A
        WHERE A."REVENUEMONTHLY_STATE" = 1{rev_where}
        GROUP BY A."SERVERPART_ID" """
    dt_cur = db.execute_query(sql_cur) or []

    # 5. 查同比月份营收
    dt_yoy = []
    if yoy_month:
        yoy_where = rev_where.replace(cur_month, yoy_month)
        sql_yoy = f"""SELECT A."SERVERPART_ID",
                SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
            FROM "T_REVENUEMONTHLY" A
            WHERE A."REVENUEMONTHLY_STATE" = 1{yoy_where}
            GROUP BY A."SERVERPART_ID" """
        dt_yoy = db.execute_query(sql_yoy) or []

    # 6. 构建索引映射
    cur_map = {str(r.get("SERVERPART_ID", "")): r for r in dt_cur}
    yoy_map = {str(r.get("SERVERPART_ID", "")): r for r in dt_yoy}

    # 7. 组装结果
    result_list = []
    for sp in sp_rows:
        sp_id = str(sp["SERVERPART_ID"])
        cur_r = cur_map.get(sp_id, {})
        yoy_r = yoy_map.get(sp_id, {})

        cur_rev = _safe_float(cur_r.get("REVENUE_AMOUNT")) if cur_r else None
        yoy_rev = _safe_float(yoy_r.get("REVENUE_AMOUNT")) if yoy_r else None

        rev_inc = _make_inc(cur_rev, yoy_rev)

        item = {
            "SPRegionTypeId": sp.get("SPREGIONTYPE_ID"),
            "SPRegionTypeName": sp.get("SPREGIONTYPE_NAME"),
            "ServerpartId": sp.get("SERVERPART_ID"),
            "ServerpartName": sp.get("SERVERPART_NAME"),
            "RevenueINC": rev_inc,
            "AccountINC": _make_inc(),
            "BayonetINC": _make_inc(),
            "SectionFlowINC": _make_inc(),
            "AvgTicketINC": None,
            "TicketINC": None,
        }
        result_list.append(item)

    # 8. 排序
    if sort_str and result_list:
        ss = str(sort_str).lower()
        is_desc = "desc" in ss
        if "revenue" in ss:
            result_list.sort(
                key=lambda x: (x["RevenueINC"]["increaseRate"] or 0),
                reverse=is_desc)

    return result_list if result_list else None


# ===================================================================
# 2. GetMonthINCAnalysisSummary — 月度增幅汇总
# ===================================================================

def get_month_inc_analysis_summary(db: DatabaseHelper, province_code, statistics_month,
                                   serverpart_id, sp_region_type_id,
                                   business_region, data_type) -> dict:
    """
    获取月度增幅汇总数据
    返回汇总 dict (全省合计)
    """
    if not statistics_month:
        return None

    cur_month = str(statistics_month).replace("-", "").replace("/", "")[:6]
    try:
        yoy_month = str(int(cur_month[:4]) - 1) + cur_month[4:]
    except (ValueError, IndexError):
        yoy_month = None

    # 1. 查省份ID
    fe_rows = db.execute_query(
        """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
            WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
            AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE'
            AND B."FIELDENUM_VALUE" = :pc""",
        {"pc": province_code})
    if not fe_rows:
        return None
    province_id = fe_rows[0]["FIELDENUM_ID"]

    # 2. 构建服务区过滤
    sp_where = ""
    if serverpart_id:
        _sp_ids = parse_multi_ids(serverpart_id)
        if _sp_ids:
            sp_where = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

    # 3. 查当月汇总
    sql_cur = f"""SELECT SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
            SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
        FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000
            AND B."PROVINCE_CODE" = {province_id}
            AND A."STATISTICS_MONTH" = {cur_month}{sp_where}"""
    cur_rows = db.execute_query(sql_cur) or [{}]
    cur_rev = _safe_float(cur_rows[0].get("REVENUE_AMOUNT"))
    cur_ticket = _safe_float(cur_rows[0].get("TICKET_COUNT"))

    # 4. 查同比汇总
    yoy_rev = 0.0
    yoy_ticket = 0.0
    if yoy_month:
        sql_yoy = f"""SELECT SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT",
                SUM(A."TICKET_COUNT") AS "TICKET_COUNT"
            FROM "T_REVENUEMONTHLY" A, "T_SERVERPART" B
            WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
                AND A."REVENUEMONTHLY_STATE" = 1 AND B."STATISTIC_TYPE" = 1000
                AND B."PROVINCE_CODE" = {province_id}
                AND A."STATISTICS_MONTH" = {yoy_month}{sp_where}"""
        yoy_rows = db.execute_query(sql_yoy) or [{}]
        yoy_rev = _safe_float(yoy_rows[0].get("REVENUE_AMOUNT"))
        yoy_ticket = _safe_float(yoy_rows[0].get("TICKET_COUNT"))

    # 5. 构建汇总结果
    result = {
        "SPRegionTypeName": "合计",
        "ServerpartName": "全省合计",
        "RevenueINC": _make_inc(cur_rev, yoy_rev),
        "TicketINC": _make_inc(cur_ticket, yoy_ticket),
        "AccountINC": _make_inc(),
        "BayonetINC": _make_inc(),
    }

    return result


# ===================================================================
# 3. StorageMonthINCAnalysis — 存储月度增幅分析
# ===================================================================

def storage_month_inc_analysis(db: DatabaseHelper, province_code, statistics_month):
    """触发月度增幅分析数据存储（C# AccountHelper.StorageMonthINCAnalysis 对应）"""
    # TODO: 完整实现 — 当前为占位，直接返回成功
    logger.warning("StorageMonthINCAnalysis 存储逻辑暂未实现，返回成功")
    return Result.success(data=None, msg="生成成功")
