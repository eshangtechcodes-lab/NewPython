# -*- coding: utf-8 -*-
"""
CommercialApi - 门店 SABFI 分析 Service
从 revenue_router.py 中抽取:
  GetShopSABFIList      — 门店 SABFI 列表（全量）
  GetShopMonthSABFIList — 门店月度 SABFI 列表
"""
from __future__ import annotations
from datetime import datetime as dt
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


def _make_inc(cur=None, yoy=None, inc=None, rate=None, qoq=None, inc_qoq=None, rate_qoq=None):
    """构建 HolidayINCDetailModel"""
    def _v(x):
        if x is None:
            return None
        try:
            return round(float(x), 2)
        except (ValueError, TypeError):
            return 0.0

    def _qv(x):
        """QOQ 值: None 和 0 都视为 None"""
        if x is None:
            return None
        try:
            val = round(float(x), 2)
            return val if val != 0.0 else None
        except (ValueError, TypeError):
            return None

    return {
        "curYearData": _v(cur), "lYearData": _v(yoy),
        "increaseData": _v(inc), "increaseRate": _v(rate),
        "QOQData": _v(qoq), "increaseDataQOQ": _qv(inc_qoq),
        "increaseRateQOQ": _qv(rate_qoq), "rankNum": None
    }


def _format_ico(ico_raw):
    """Brand_ICO 格式化"""
    if not ico_raw:
        return ""
    if ico_raw.startswith("http"):
        return ico_raw
    if "PictureManage" in ico_raw:
        return "https://user.eshangtech.com" + ("/" if not ico_raw.startswith("/") else "") + ico_raw
    return "https://api.eshangtech.com/EShangApiMain/" + ico_raw.lstrip("/")


def _expand_trade_types(db, trade_ids_str):
    """
    递归展开业态子类型 (GetSubType)
    查 T_AUTOSTATISTICS 树, AUTOSTATISTICS_TYPE=2000
    """
    if not trade_ids_str:
        return set()
    expanded = set()
    for bt_id in str(trade_ids_str).split(","):
        bt_id = bt_id.strip()
        if not bt_id:
            continue
        expanded.add(bt_id)
        queue = [bt_id]
        while queue:
            pid = queue.pop(0)
            try:
                sub_rows = db.execute_query(
                    f'SELECT "AUTOSTATISTICS_ID" FROM "T_AUTOSTATISTICS" '
                    f'WHERE "AUTOSTATISTICS_PID" = {pid} AND "AUTOSTATISTICS_TYPE" = 2000'
                ) or []
                for sr in sub_rows:
                    sid = str(sr.get("AUTOSTATISTICS_ID", ""))
                    if sid and sid not in expanded:
                        expanded.add(sid)
                        queue.append(sid)
            except Exception:
                pass
    return expanded


# ===================================================================
# 1. GetShopSABFIList — 门店 SABFI 列表
# ===================================================================

def get_shop_sabfi_list(db: DatabaseHelper, province_code, statistics_date,
                        serverpart_id, sp_region_type_id, business_region,
                        sort_str, business_type, business_trade) -> list:
    """
    获取门店 SABFI（服务区业态综合评分）列表
    Router 传入: province_code, statistics_date, serverpart_id,
                 sp_region_type_id, business_region, sort_str,
                 business_type, business_trade
    返回: list[dict] 或 None
    """
    # 参数映射
    ServerpartId = serverpart_id
    BusinessTrade = business_trade

    if not statistics_date:
        return None

    # 将统计日期转换为月份
    stat_date_str = str(statistics_date).replace("-", "").replace("/", "")
    if len(stat_date_str) >= 6:
        stat_month = stat_date_str[:6]
    else:
        return None

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
    sp_where = f' AND B."PROVINCE_CODE" = {province_id}'
    if ServerpartId:
        _sp_ids = parse_multi_ids(ServerpartId)
        if _sp_ids:
            sp_where += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
    if business_region and str(business_region) == "1":
        sp_where += ' AND B."SPREGIONTYPE_ID" NOT IN (89)'

    # 3. 展开业态子类型
    expanded_trades = _expand_trade_types(db, BusinessTrade)

    # 4. 查 T_PROFITCONTRIBUTE（SABFI 评分数据）
    sql = f"""SELECT A."SERVERPART_ID", A."SERVERPARTSHOP_ID", A."SERVERPARTSHOP_NAME",
            A."EVALUATE_TYPE", A."EVALUATE_SCORE", A."PROFITCONTRIBUTE_ID", A."PROFITCONTRIBUTE_PID"
        FROM "T_PROFITCONTRIBUTE" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"
            AND A."PROFITCONTRIBUTE_STATE" = 1
            AND A."STATISTICS_DATE" = {stat_month}
            AND B."STATISTIC_TYPE" = 1000{sp_where}
        ORDER BY A."SERVERPART_ID", A."SERVERPARTSHOP_ID" """
    pc_rows = db.execute_query(sql) or []

    if not pc_rows:
        return None

    # 5. 按 SERVERPARTSHOP_ID 分组
    shop_map = {}
    for r in pc_rows:
        shop_id = str(r.get("SERVERPARTSHOP_ID", ""))
        if shop_id not in shop_map:
            shop_map[shop_id] = {"info": r, "scores": []}
        shop_map[shop_id]["scores"].append(r)

    # 6. 查门店额外信息（品牌、业态关联）
    sp_ids_str = ",".join(set(str(r.get("SERVERPART_ID", "")) for r in pc_rows))
    shop_info_map = {}
    if sp_ids_str:
        shop_info_rows = db.execute_query(f"""SELECT "SERVERPARTSHOP_ID", "SERVERPART_ID",
                "SHOPSHORTNAME", "BUSINESS_BRAND", "SHOPTRADE", "BUSINESSTRADETYPE"
            FROM "T_SERVERPARTSHOP"
            WHERE "SERVERPART_ID" IN ({sp_ids_str})""") or []
        for si in shop_info_rows:
            shop_info_map[str(si.get("SERVERPARTSHOP_ID", ""))] = si

    # 7. 查服务区名称
    sp_name_map = {}
    if sp_ids_str:
        sp_rows = db.execute_query(f"""SELECT "SERVERPART_ID", "SERVERPART_NAME",
                "SPREGIONTYPE_ID", "SPREGIONTYPE_NAME"
            FROM "T_SERVERPART" WHERE "SERVERPART_ID" IN ({sp_ids_str})""") or []
        for sp in sp_rows:
            sp_name_map[str(sp.get("SERVERPART_ID", ""))] = sp

    # 8. 构建结果
    result_list = []
    for shop_id, data in shop_map.items():
        scores = data["scores"]
        info = data["info"]
        sp_id = str(info.get("SERVERPART_ID", ""))
        shop_detail = shop_info_map.get(shop_id, {})
        sp_detail = sp_name_map.get(sp_id, {})

        # 业态过滤
        if expanded_trades:
            shop_trade = str(shop_detail.get("SHOPTRADE", ""))
            if shop_trade and shop_trade not in expanded_trades:
                continue

        # 构建 SABFI 评分列表
        sabfi_list = []
        for et in range(1, 8):
            et_scores = [r for r in scores if str(r.get("EVALUATE_TYPE")) == str(et)]
            if et_scores:
                best = max(et_scores, key=lambda x: _safe_float(x.get("EVALUATE_SCORE")))
                sabfi_list.append({
                    "name": str(et),
                    "value": str(_safe_float(best.get("EVALUATE_SCORE"))),
                    "key": str(best.get("PROFITCONTRIBUTE_ID", "")),
                    "data": str(best.get("PROFITCONTRIBUTE_PID", "")),
                })
            else:
                sabfi_list.append({"name": str(et), "value": "", "key": "", "data": ""})

        sabfi_sum = sum(_safe_float(s["value"]) for s in sabfi_list)

        item = {
            "ServerpartId": info.get("SERVERPART_ID"),
            "ServerpartName": sp_detail.get("SERVERPART_NAME", ""),
            "SPRegionTypeId": sp_detail.get("SPREGIONTYPE_ID"),
            "SPRegionTypeName": sp_detail.get("SPREGIONTYPE_NAME", ""),
            "ServerpartShopId": shop_id,
            "ServerpartShopName": info.get("SERVERPARTSHOP_NAME", ""),
            "SABFI_Score": round(sabfi_sum, 2),
            "SABFIList": sabfi_list,
            "Brand_Id": None,
            "Brand_Name": shop_detail.get("BUSINESS_BRAND"),
            "Brand_ICO": _format_ico(None),
            "ShopTrade": shop_detail.get("SHOPTRADE", 0),
            "BusinessTradeName": None,
            "BusinessTradeType": shop_detail.get("BUSINESSTRADETYPE", 0),
            "RevenueINC": _make_inc(),
            "AccountINC": _make_inc(),
            "TicketINC": _make_inc(),
            "AvgTicketINC": _make_inc(),
        }
        result_list.append(item)

    # 9. 排序
    if sort_str and result_list:
        ss = str(sort_str).lower()
        is_desc = "desc" in ss
        result_list.sort(key=lambda x: x.get("SABFI_Score", 0), reverse=is_desc)

    return result_list if result_list else None


# ===================================================================
# 2. GetShopMonthSABFIList — 门店月度 SABFI 列表
# ===================================================================

def get_shop_month_sabfi_list(db: DatabaseHelper, province_code, statistics_month,
                              serverpart_id, sp_region_type_id,
                              business_region, sort_str) -> list:
    """
    获取门店月度 SABFI 列表数据
    Router 传入: province_code, statistics_month, serverpart_id,
                 sp_region_type_id, business_region, sort_str
    按月分组展示 T_PROFITCONTRIBUTE 数据
    返回: list[dict] 或 None
    """
    # 参数映射
    ServerpartId = serverpart_id

    if not statistics_month or not ServerpartId:
        return None

    stat_month = str(statistics_month).replace("-", "").replace("/", "")[:6]

    # 查看当前月往前 12 个月的范围
    try:
        y, m = int(stat_month[:4]), int(stat_month[4:])
        end_month = stat_month
        # 往前推 11 个月作为开始
        if m <= 11:
            start_month = f"{y - 1}{m + 1:02d}"
        else:
            start_month = f"{y}01"
    except (ValueError, IndexError):
        return None

    # 查 T_PROFITCONTRIBUTE
    pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
        WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPART_ID" = {ServerpartId}
            AND "STATISTICS_DATE" BETWEEN {start_month} AND {end_month}"""
    pc_rows = db.execute_query(pc_sql) or []

    if not pc_rows:
        return None

    # 按月份分组
    month_data = {}
    for r in pc_rows:
        m_val = str(r.get("STATISTICS_DATE", ""))
        if m_val not in month_data:
            month_data[m_val] = []
        month_data[m_val].append(r)

    # 遍历月份范围构建结果
    data_list = []
    try:
        s_year, s_month_n = int(start_month[:4]), int(start_month[4:])
        e_year, e_month_n = int(end_month[:4]), int(end_month[4:])
    except (ValueError, IndexError):
        return None

    cur_y, cur_m = s_year, s_month_n
    while cur_y * 100 + cur_m <= e_year * 100 + e_month_n:
        m_key = f"{cur_y}{cur_m:02d}"
        m_fmt = f"{cur_y}/{cur_m:02d}"
        rows_m = month_data.get(m_key, [])
        # 兼容数字类型 key
        if not rows_m:
            rows_m = month_data.get(int(m_key) if m_key.isdigit() else m_key, [])

        def get_max(rr, eval_type, field):
            """获取指定 EVALUATE_TYPE 的 MAX 值"""
            vals = [r.get(field) for r in rr
                    if str(r.get("EVALUATE_TYPE")) == str(eval_type) and r.get(field) is not None]
            if vals:
                return str(max(vals))
            return ""

        sabfi_list = []
        for et in range(1, 8):
            sabfi_list.append({
                "name": str(et),
                "value": get_max(rows_m, et, "EVALUATE_SCORE"),
                "key": get_max(rows_m, et, "PROFITCONTRIBUTE_ID"),
                "data": get_max(rows_m, et, "PROFITCONTRIBUTE_PID"),
            })

        sabfi_sum = sum(_safe_float(s["value"]) for s in sabfi_list)
        sample = rows_m[0] if rows_m else {}

        data_list.append({
            "StatisticsMonth": m_fmt,
            "BusinessTrade": sample.get("SERVERPARTSHOP_NAME"),
            "BusinessProjectName": None,
            "SABFI_Score": round(sabfi_sum, 2),
            "Revenue_SD": None,
            "Revenue_AVG": None,
            "SABFIList": sabfi_list,
            "ServerpartId": sample.get("SERVERPART_ID"),
            "ServerpartName": sample.get("SERVERPART_NAME"),
            "ServerpartShopId": sample.get("SERVERPARTSHOP_ID"),
            "ServerpartShopName": sample.get("SERVERPARTSHOP_NAME"),
            "Brand_Id": None, "Brand_Name": None, "BrandType_Name": None, "Brand_ICO": None,
            "ShopTrade": 0, "BusinessTradeName": None, "BusinessTradeType": 0,
            "BusinessProjectId": sample.get("BUSINESSPROJECT_ID"),
            "CompactStartDate": None, "CompactEndDate": None,
            "BusinessType": None, "SettlementModes": None,
            "MERCHANTS_ID": None, "MERCHANTS_ID_Encrypted": None, "MERCHANTS_NAME": None,
            "RevenueINC": None, "AccountINC": None, "TicketINC": None, "AvgTicketINC": None,
            "CurTransaction": None, "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
        })

        if cur_m == 12:
            cur_y += 1
            cur_m = 1
        else:
            cur_m += 1

    return data_list if data_list else None
