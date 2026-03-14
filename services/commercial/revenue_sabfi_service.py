# -*- coding: utf-8 -*-
"""
CommercialApi - 门店 SABFI 分析 Service
从 revenue_router.py 中抽取:
  GetShopSABFIList      — 门店 SABFI 列表（全量）
  GetShopMonthSABFIList — 门店月度 SABFI 列表
"""
from __future__ import annotations
from datetime import datetime as dt, timedelta

from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


# ===================================================================
# 1. GetShopSABFIList — 门店 SABFI 列表
# ===================================================================

def get_shop_sabfi_list(db, province_code, statistics_date, serverpart_id,
                        sp_region_type_id, business_region, sort_str,
                        business_type, business_trade):
    """获取门店 SABFI 列表数据，返回 result_list 或抛出异常"""
    stat_month = StatisticsMonth or statisticsStartMonth or statisticsEndMonth
    if not stat_month:
        json_list = JsonListData.create(data_list=[], total=0, page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    def safe_dec(v):
        try: return float(v) if v is not None else 0.0
        except: return 0.0

    def make_inc(cur=None, yoy=None, inc=None, rate=None, qoq=None, inc_qoq=None, rate_qoq=None):
        """构建 HolidayINCDetailModel — None 保持 None, QOQ 增量 0→None"""
        def _v(x):
            if x is None: return None
            try: return round(float(x), 2)
            except: return 0.0
        def _qv(x):
            """QOQ 值: None 和 0 都视为 None（C# 旧接口行为）"""
            if x is None: return None
            try:
                val = round(float(x), 2)
                return val if val != 0.0 else None
            except: return None
        return {
            "curYearData": _v(cur), "lYearData": _v(yoy),
            "increaseData": _v(inc), "increaseRate": _v(rate),
            "QOQData": _v(qoq), "increaseDataQOQ": _qv(inc_qoq),
            "increaseRateQOQ": _qv(rate_qoq), "rankNum": None
        }

    def empty_inc():
        return make_inc()

    # 辅助：Brand_ICO 格式化
    def _format_ico(ico_raw):
        if not ico_raw: return ""
        if ico_raw.startswith("http"): return ico_raw
        if "PictureManage" in ico_raw: return "https://user.eshangtech.com" + ("/" if not ico_raw.startswith("/") else "") + ico_raw
        return "https://api.eshangtech.com/EShangApiMain/" + ico_raw.lstrip("/")

    # 辅助：BP 日期格式化 (C# yyyy/M/d)
    def _format_bp_date(date_obj):
        if not date_obj: return ""
        from datetime import datetime as dt_internal
        if isinstance(date_obj, dt_internal):
            return f"{date_obj.year}/{date_obj.month}/{date_obj.day}"
        s_date = str(date_obj).replace("T", " ").split(" ")[0].replace("-", "/")
        parts = s_date.split("/")
        if len(parts) == 3:
            return f"{parts[0]}/{int(parts[1])}/{int(parts[2])}"
        return s_date

    # 多服务区ID兼容
    sp_where = ""
    _sp_ids = parse_multi_ids(ServerpartId)
    if _sp_ids:
        sp_where = " AND " + build_in_condition("SERVERPART_ID", _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

    btt_where = ""
    if BusinessTradeType:
        btt_where = f' AND A."BUSINESSTRADETYPE" IN ({BusinessTradeType})'
    # C# 对齐: BusinessTrade 不在 SQL 中过滤，而是在遍历门店时用 T_SERVERPARTSHOP.BUSINESS_TRADE 做内存过滤
    # 先通过 GetSubType 递归展开业态子类型（查 T_AUTOSTATISTICS 树形结构）
    expanded_trades = set()
    if BusinessTrade:
        for bt_id in str(BusinessTrade).split(","):
            bt_id = bt_id.strip()
            if bt_id:
                expanded_trades.add(bt_id)
                # 递归查询子类型 (AUTOSTATISTICS_TYPE=2000 为经营业态分类)
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
                            if sid and sid not in expanded_trades:
                                expanded_trades.add(sid)
                                queue.append(sid)
                    except Exception:
                        pass  # 子类型查询失败时跳过

    # TODO: get_shop_sabfi_list 逻辑不完整 — 函数在迁移时被截断
    # 需完整迁移 C# GetShopSABFIList 的剩余逻辑
    from loguru import logger
    logger.warning("get_shop_sabfi_list 逻辑不完整，返回空结果")
    from models.base import Result, JsonListData
    json_list = JsonListData.create(data_list=[], total=0, page_size=10)
    return Result.success(data=json_list.model_dump(), msg="查询成功")


# 2. GetShopMonthSABFIList — 门店月度 SABFI 列表
# ===================================================================

def get_shop_month_sabfi_list(db, province_code, statistics_month, serverpart_id,
                               sp_region_type_id, business_region, sort_str):
    """获取门店月度 SABFI 列表数据，返回 result_list 或抛出异常"""
    from datetime import datetime as dt

    # 构建查询条件
    if BusinessProjectId:
        pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
            WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "BUSINESSPROJECT_ID" = {BusinessProjectId}
                AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
    elif ServerpartShopId:
        pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
            WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPARTSHOP_ID" = '{ServerpartShopId}'
                AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
    elif ServerpartId and ServerpartShopName:
        pc_sql = f"""SELECT * FROM "T_PROFITCONTRIBUTE"
            WHERE "PROFITCONTRIBUTE_STATE" = 1 AND "SERVERPART_ID" = {ServerpartId}
                AND "SERVERPARTSHOP_NAME" = '{ServerpartShopName}'
                AND "STATISTICS_DATE" BETWEEN {StatisticsStartMonth} AND {StatisticsEndMonth}
                AND "CALCULATE_SELFSHOP" = {1 if calcSelf else 2}"""
    else:
        json_list = JsonListData.create(data_list=[], total=0, page_size=10)
        return Result.success(data=json_list.model_dump(), msg="查询成功")

    pc_rows = db.execute_query(pc_sql) or []

    # 按月份分组
    month_data = {}
    for r in pc_rows:
        m = str(r.get("STATISTICS_DATE", ""))
        if m not in month_data:
            month_data[m] = []
        month_data[m].append(r)

    # 遍历月份范围
    data_list = []
    s_year = int(StatisticsStartMonth[:4])
    s_month = int(StatisticsStartMonth[4:])
    e_year = int(StatisticsEndMonth[:4])
    e_month = int(StatisticsEndMonth[4:])
    cur_y, cur_m = s_year, s_month
    while cur_y * 100 + cur_m <= e_year * 100 + e_month:
        m_key = f"{cur_y}{cur_m:02d}"
        m_fmt = f"{cur_y}/{cur_m:02d}"
        rows_m = month_data.get(m_key, [])
        rows_m_int = month_data.get(int(m_key) if m_key.isdigit() else m_key, rows_m)
        if not rows_m and rows_m_int:
            rows_m = rows_m_int

        def get_max(rr, eval_type, field):
            """获取指定EVALUATE_TYPE的MAX值"""
            vals = [r.get(field) for r in rr if str(r.get("EVALUATE_TYPE")) == str(eval_type) and r.get(field) is not None]
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

        # 计算SABFI_Score
        score_0 = get_max(rows_m, 0, "EVALUATE_SCORE")
        try:
            sabfi_score = float(score_0) if score_0 else 0.0
        except:
            sabfi_score = 0.0
        # C#: SABFI_Score = SABFIList.Sum(o => o.value.TryParseToDecimal())
        sabfi_sum = sum(float(s["value"]) if s["value"] else 0.0 for s in sabfi_list)

        # TODO: 此处若需对齐 C# 细化数据，需查 T_BUSINESSWARNING / T_PERIODMONTHPROFIT
        # 临时占位逻辑：从 rows_m 获取基础信息
        sample = rows_m[0] if rows_m else {}
        
        data_list.append({
            "StatisticsMonth": m_fmt,
            "BusinessTrade": sample.get("SERVERPARTSHOP_NAME"), # 临时
            "BusinessProjectName": None,
            "SABFI_Score": sabfi_sum,
            "Revenue_SD": None,
            "Revenue_AVG": None,
            "SABFIList": sabfi_list,
            "ServerpartId": sample.get("SERVERPART_ID"),
            "ServerpartName": sample.get("SERVERPART_NAME"),
            "ServerpartShopId": sample.get("SERVERPARTSHOP_ID"),
            "ServerpartShopName": sample.get("SERVERPARTSHOP_NAME"),
            "Brand_Id": None, "Brand_Name": None, "BrandType_Name": None, "Brand_ICO": None,
            "ShopTrade": 0, "BusinessTradeName": None, "BusinessTradeType": 0,
            "BusinessProjectId": sample.get("BUSINESSPROJECT_ID"), "CompactStartDate": None, "CompactEndDate": None,
            "BusinessType": None, "SettlementModes": None,
            "MERCHANTS_ID": None, "MERCHANTS_ID_Encrypted": None, "MERCHANTS_NAME": None,
            "RevenueINC": None, "AccountINC": None, "TicketINC": None, "AvgTicketINC": None,
            "CurTransaction": None, "Profit_Amount": None, "Cost_Amount": None, "Ca_Cost": None,
        })

        # 下个月
        if cur_m == 12:
            cur_y += 1
            cur_m = 1
        else:
            cur_m += 1

    json_list = JsonListData.create(data_list=data_list, total=len(data_list), page_size=10)
    return Result.success(data=json_list.model_dump(), msg="查询成功")
