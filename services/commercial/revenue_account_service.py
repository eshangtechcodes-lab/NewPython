# -*- coding: utf-8 -*-
"""
CommercialApi - 账务 + 同步 Service
从 revenue_router.py 中抽取:
  GetAccountReceivable  — 营收统计明细
  GetCurRevenue         — 实时营收交易
  GetShopCurRevenue     — 实时门店营收
  GetLastSyncDateTime   — 最新同步日期
"""
from __future__ import annotations
from datetime import datetime as dt, timedelta

from core.database import DatabaseHelper
from services.commercial.service_utils import safe_float as _sf, safe_int as _si
from routers.deps import parse_multi_ids, build_in_condition


# ===================================================================
# 1. GetAccountReceivable — 营收统计明细数据
# ===================================================================

def get_account_receivable(db, calc_type, province_code, statistics_month,
                           statistics_start_month, statistics_date):
    """
    获取营收统计明细数据
    返回 dict 结果，无数据返回 None
    """
    if not statistics_month:
        return None

    # 经营模式枚举映射
    bt_names = {4000: "业主自营", 3000: "自营提成", 1000: "合作分成", 2000: "固定租金"}

    sm = statistics_start_month if statistics_start_month else f"{statistics_month[:4]}01"
    if (statistics_date and
            dt.strptime(statistics_date.split(" ")[0], "%Y-%m-%d").strftime("%Y%m") == statistics_month):
        date_sql = (f' AND "STATISTICS_DATE" >= {sm}01 AND "STATISTICS_DATE" <= '
                    f'{dt.strptime(statistics_date.split(" ")[0], "%Y-%m-%d").strftime("%Y%m%d")}')
        detail_sql = (f'SELECT * FROM "T_ACCOUNTRECDETAIL" '
                      f'WHERE "PROVINCE_ID" = 3544 AND "SERVERPART_ID" = 0 '
                      f'AND "DATE_TYPE" = 1 AND "ACCOUNTRECDETAIL_STATE" = 1{date_sql}')
        date_sql_rev = f' AND "STATISTICS_DATE" BETWEEN {sm}01 AND {statistics_month}31'
    else:
        if calc_type == 1:
            date_sql = f' AND "STATISTICS_DATE" = {statistics_month}'
        else:
            date_sql = f' AND "STATISTICS_DATE" >= {sm} AND "STATISTICS_DATE" <= {statistics_month}'
        detail_sql = (f'SELECT * FROM "T_ACCOUNTRECDETAIL" '
                      f'WHERE "PROVINCE_ID" = 3544 AND "SERVERPART_ID" = 0 '
                      f'AND "DATE_TYPE" = 2 AND "ACCOUNTRECDETAIL_STATE" = 1{date_sql}')
        date_sql_rev = f' AND "STATISTICS_DATE" BETWEEN {sm}01 AND {statistics_month}31'

    detail_rows = db.execute_query(detail_sql) or []

    # 查 T_PROVINCEREVENUE 获取业主营业收入
    account_sql = f'''SELECT
            SUM(A."REVENUE_AMOUNT") AS "REVENUE_AMOUNT", A."BUSINESS_TYPE",
            SUM(A."ACCOUNT_AMOUNTNOTAX") AS "ACCOUNT_AMOUNT",
            CASE WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" = 2 THEN 1
                WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" <> 2 THEN 2 ELSE 3 END AS "SHOPTRADE"
        FROM "T_PROVINCEREVENUE" A
        WHERE A."PROVINCEREVENUE_STATE" = 1{date_sql_rev}
        GROUP BY A."BUSINESS_TYPE",
            CASE WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" = 2 THEN 1
                WHEN A."BUSINESS_TYPE" = 4000 AND "SHOPTRADE" <> 2 THEN 2 ELSE 3 END'''
    account_rows = db.execute_query(account_sql) or []

    # 辅助汇总函数
    def _sd(v):
        try:
            return float(v) if v is not None else 0.0
        except Exception:
            return 0.0

    def sum_detail(stat_type, biz_type=None):
        total = 0.0
        for r in detail_rows:
            st = int(_sd(r.get("STATISTICS_TYPE")))
            bt = int(_sd(r.get("BUSINESS_TYPE")))
            if st == stat_type:
                if biz_type is not None:
                    if bt == biz_type:
                        total += _sd(r.get("DATA_VALUE"))
                else:
                    total += _sd(r.get("DATA_VALUE"))
        return total

    def sum_detail_lt(stat_type, biz_lt):
        total = 0.0
        for r in detail_rows:
            st = int(_sd(r.get("STATISTICS_TYPE")))
            bt = int(_sd(r.get("BUSINESS_TYPE")))
            if st == stat_type and bt < biz_lt:
                total += _sd(r.get("DATA_VALUE"))
        return total

    def max_detail(stat_type, biz_type=None):
        vals = []
        for r in detail_rows:
            st = int(_sd(r.get("STATISTICS_TYPE")))
            bt = int(_sd(r.get("BUSINESS_TYPE")))
            if st == stat_type:
                if biz_type is not None:
                    if bt == biz_type:
                        vals.append(_sd(r.get("DATA_VALUE")))
                else:
                    vals.append(_sd(r.get("DATA_VALUE")))
        return max(vals) if vals else 0.0

    def sum_account(biz_type):
        total = 0.0
        for r in account_rows:
            bt = int(_sd(r.get("BUSINESS_TYPE")))
            if bt == biz_type:
                total += _sd(r.get("ACCOUNT_AMOUNT"))
        return total

    owner_rev = sum_detail(1000)
    merchant_rev = sum_detail(2000)

    # project_count: 按 BUSINESS_TYPE 分组取 max 再求和
    pc_map = {}
    for r in detail_rows:
        st = int(_sd(r.get("STATISTICS_TYPE")))
        bt = int(_sd(r.get("BUSINESS_TYPE")))
        if st == 3001:
            dv = _sd(r.get("DATA_VALUE"))
            pc_map[bt] = max(pc_map.get(bt, 0), dv)
    project_count = int(sum(pc_map.values()))

    # CommissionRatio
    s1004 = sum_detail_lt(1004, 4000)
    s3003 = sum_detail_lt(3003, 4000)
    commission_ratio = round(s1004 / s3003 * 100, 2) if s3003 > 0 else 0.0

    # 按经营模式遍历
    bt_list = [4000, 3000, 1000, 2000]
    owner_acount, owner_entry, owner_recv = [], [], []
    merchant_acount, merchant_entry, merchant_recv = [], [], []
    proj_count_list, proj_ratio_list, rev_ratio_list, commission_list = [], [], [], []

    def fmt_val(v):
        v = round(v, 2)
        return "0" if v == 0 else f"{v:.2f}"

    for bt in bt_list:
        name = bt_names.get(bt, str(bt))
        owner_acount.append({"name": name, "value": fmt_val(sum_detail(1001, bt))})
        owner_entry.append({"name": name, "value": fmt_val(sum_account(bt))})
        owner_recv.append({"name": name, "value": fmt_val(sum_detail(1003, bt))})
        merchant_acount.append({"name": name, "value": fmt_val(sum_detail(2001, bt))})
        merchant_entry.append({"name": name, "value": fmt_val(sum_detail(2002, bt))})
        merchant_recv.append({"name": name, "value": fmt_val(sum_detail(2003, bt))})
        pc_val = max_detail(3001, bt)
        proj_count_list.append({"name": name, "value": str(int(pc_val))})
        proj_ratio_list.append({"name": name, "value": str(round(pc_val / project_count * 100, 2) if project_count > 0 else 0)})
        s3003_bt = sum_detail(3003, bt)
        rev_ratio_list.append({"name": name, "value": str(round(s3003_bt / owner_rev * 100, 2) if owner_rev > 0 else 0)})
        if bt == 4000:
            commission_list.append({"name": name, "value": "0"})
        else:
            s1004_bt = sum_detail(1004, bt)
            s3003_bt2 = sum_detail(3003, bt)
            commission_list.append({"name": name, "value": str(round(s1004_bt / s3003_bt2 * 100, 2) if s3003_bt2 > 0 else 0)})

    return {
        "OwnerRevenue": round(owner_rev, 2),
        "MerchantRevenue": round(merchant_rev, 2),
        "OwnerList": {"AcountList": owner_acount, "EntryList": owner_entry, "ReceivableList": owner_recv},
        "MerchantList": {"AcountList": merchant_acount, "EntryList": merchant_entry, "ReceivableList": merchant_recv},
        "ProjectCount": project_count,
        "ProjectCountList": proj_count_list,
        "ProjectRatioList": proj_ratio_list,
        "RevenueRatioList": rev_ratio_list,
        "CommissionRatio": commission_ratio,
        "CommissionList": commission_list,
    }


# ===================================================================
# 2. GetCurRevenue — 实时营收交易数据
# ===================================================================

def get_cur_revenue(db, province_code, statistics_date, serverpart_id):
    """获取实时营收交易数据，无数据返回 None"""
    if not statistics_date:
        return None

    stat_date = (dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date
                 else dt.strptime(statistics_date, "%Y%m%d"))
    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition(
            'SERVERPART_ID', _sp_ids
        ).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

    sql = f"""SELECT SUM(A."CASHPAY") AS "CASHPAY",
            SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
            SUM(A."TOTALCOUNT") AS "TOTALCOUNT"
        FROM "T_ENDACCOUNT_TEMP" A
        WHERE A."VALID" = 1
            AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
            AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1{where_sql}"""
    rows = db.execute_query(sql) or []

    cashpay = _sf(rows[0].get("CASHPAY")) if rows else 0
    ticketcount = _si(rows[0].get("TICKETCOUNT")) if rows else 0
    totalcount = _sf(rows[0].get("TOTALCOUNT")) if rows else 0
    avg_ticket = round(cashpay / ticketcount, 2) if ticketcount > 0 else None
    avg_sell = round(cashpay / totalcount, 2) if totalcount > 0 else None

    return {
        "AnnualRevenue": None,
        "CurRevenueAmount": cashpay, "CurTicketCount": ticketcount,
        "CurTotalCount": totalcount,
        "CurAvgTicketAmount": avg_ticket, "CurAvgSellAmount": avg_sell,
        "AddRevenueAmount": None, "AddTicketCount": None, "AddTotalCount": None,
    }


# ===================================================================
# 3. GetShopCurRevenue — 实时门店营收
# ===================================================================

def get_shop_cur_revenue(db, serverpart_id, statistics_date, group_by_shop):
    """获取实时门店营收交易数据，返回列表或 None"""
    if not serverpart_id or not statistics_date:
        return None

    stat_date = (dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date
                 else dt.strptime(statistics_date, "%Y%m%d"))

    _sp_ids = parse_multi_ids(serverpart_id)
    if not _sp_ids:
        return None
    sp_condition = build_in_condition("SERVERPART_ID", _sp_ids).replace(
        '"SERVERPART_ID"', 'A."SERVERPART_ID"')

    sql = f"""SELECT A."BUSINESS_TYPE", A."SHOPNAME",
            SUM(A."CASHPAY") AS "CASHPAY",
            SUM(A."TICKETCOUNT") AS "TICKETCOUNT",
            SUM(A."TOTALCOUNT") AS "TOTALCOUNT"
        FROM "T_ENDACCOUNT_TEMP" A
        WHERE A."VALID" = 1 AND {sp_condition}
            AND A."STATISTICS_DATE" >= TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD')
            AND A."STATISTICS_DATE" < TO_DATE('{stat_date.strftime('%Y-%m-%d')}','YYYY-MM-DD') + 1
        GROUP BY A."BUSINESS_TYPE", A."SHOPNAME"
        ORDER BY SUM(A."CASHPAY") DESC"""
    rows = db.execute_query(sql) or []

    if not rows:
        return None

    data_list = []
    for r in rows:
        data_list.append({
            "ShopTrade": r.get("BUSINESS_TYPE", ""),
            "ShopName": r.get("SHOPNAME", ""),
            "CashPay": _sf(r.get("CASHPAY")),
            "TicketCount": _sf(r.get("TICKETCOUNT")),
            "TotalCount": _sf(r.get("TOTALCOUNT")),
        })
    return data_list


# ===================================================================
# 4. GetLastSyncDateTime — 最新同步日期
# ===================================================================

def get_last_sync_date_time(db):
    """获取最新的同步日期，返回日期字符串或空字符串"""
    now = dt.now()
    yesterday = now - timedelta(days=1)
    month_start = yesterday.strftime("%Y%m") + "01"
    today_str = now.strftime("%Y%m%d")

    sql = f"""SELECT
            STATISTICS_DATE, MAX(RECORD_DATE) AS RECORD_DATE
        FROM
            T_PROVINCEREVENUE
        WHERE
            PROVINCEREVENUE_STATE = 1 AND
            DATA_TYPE = 1 AND HOLIDAY_TYPE > 0 AND
            STATISTICS_DATE >= {month_start} AND
            STATISTICS_DATE < {today_str}
        GROUP BY
            STATISTICS_DATE
        ORDER BY STATISTICS_DATE DESC"""
    rows = db.execute_query(sql)
    for r in rows:
        stat_date_str = str(r["STATISTICS_DATE"])
        record_dt = r["RECORD_DATE"]

        stat_dt = dt.strptime(stat_date_str, "%Y%m%d")
        threshold_dt = stat_dt + timedelta(days=1, hours=8, minutes=30)

        if record_dt and record_dt >= threshold_dt:
            return stat_dt.strftime("%Y-%m-%d")

    return ""
