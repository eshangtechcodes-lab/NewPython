# -*- coding: utf-8 -*-
from __future__ import annotations
# -*- coding: utf-8 -*-
"""
CommercialApi - 合同分析业务服务
从 contract_router.py 中抽取的 SQL 和业务逻辑
"""
from typing import Optional
from collections import defaultdict
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


def _safe_dec(v):
    try: return float(v) if v is not None else 0.0
    except: return 0.0

def _safe_int(v):
    try: return int(v) if v is not None else 0
    except: return 0


def get_contract_analysis(db: DatabaseHelper, statistics_date: str,
                          province_code: Optional[str],
                          serverpart_id: Optional[str],
                          sp_region_type_id: Optional[str]) -> dict:
    """获取经营合同分析"""
    from datetime import datetime as dt, timedelta

    if not statistics_date:
        statistics_date = dt.now().strftime("%Y-%m-%d")

    # WHERE 子句
    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql = " AND " + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'D.SERVERPART_ID')
    elif sp_region_type_id:
        where_sql = f" AND D.SERVERPART_ID IN ({sp_region_type_id})"
    elif province_code:
        fe_rows = db.execute_query(f"""SELECT "FIELDENUM_ID" FROM "T_FIELDENUM"
            WHERE "FIELD_NAME" = 'DIVISION_CODE' AND "FIELDENUM_VALUE" = '{province_code}'""") or []
        if fe_rows:
            province_id = fe_rows[0].get("FIELDENUM_ID")
            where_sql = f" AND D.PROVINCE_CODE = {province_id}"

    exists_sql = ""
    if where_sql:
        exists_sql = f""" AND EXISTS (SELECT 1 FROM "T_RTREGISTERCOMPACT" C, "T_SERVERPART" D
            WHERE A."REGISTERCOMPACT_ID" = C."REGISTERCOMPACT_ID"
            AND C."SERVERPART_ID" = D."SERVERPART_ID"{where_sql})"""

    # 签约合同
    sql_contract = f"""SELECT SUM(A."COMPACT_AMOUNT") AS "TOTAL_AMOUNT"
        FROM "T_REGISTERCOMPACT" A, "T_REGISTERCOMPACTSUB" B
        WHERE A."REGISTERCOMPACT_ID" = B."REGISTERCOMPACT_ID"
            AND A."COMPACT_STATE" = 1000{exists_sql}"""
    contract_rows = db.execute_query(sql_contract) or []
    contract_profit_loss = round(_safe_dec(contract_rows[0].get("TOTAL_AMOUNT")) if contract_rows else 0, 2)

    # 门店数量
    shop_where = ""
    if _sp_ids:
        shop_where = ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'B."SERVERPART_ID"')
    elif province_code:
        fe_rows2 = db.execute_query(f"""SELECT "FIELDENUM_ID" FROM "T_FIELDENUM"
            WHERE "FIELD_NAME" = 'DIVISION_CODE' AND "FIELDENUM_VALUE" = '{province_code}'""") or []
        if fe_rows2:
            shop_where = f' AND B."PROVINCE_CODE" = {fe_rows2[0].get("FIELDENUM_ID")}'

    stat_date_str = dt.strptime(statistics_date, "%Y-%m-%d").strftime("%Y%m%d") if "-" in statistics_date else statistics_date
    stat_date_next = (dt.strptime(statistics_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y%m%d")
    shop_where += f' AND A."OPERATE_DATE" >= {stat_date_str} AND A."OPERATE_DATE" < {stat_date_next}'

    sql_shop = f"""SELECT SUM(A."SHOP_BUSINESSCOUNT") AS "SHOP_COUNT"
        FROM "T_SHOPCOUNT" A, "T_SERVERPART" B
        WHERE A."SERVERPART_ID" = B."SERVERPART_ID"{shop_where}"""
    shop_rows = db.execute_query(sql_shop) or []
    shop_count = _safe_int(shop_rows[0].get("SHOP_COUNT")) if shop_rows else 0

    # 欠款
    sql_arrearage = f"""SELECT SUM(A."CURRENTBALANCE" / 10000) AS "TOTAL_BALANCE"
        FROM "T_PAYMENTCONFIRM" A, "T_BUSINESSPROJECT" B
        WHERE A."BUSINESSPROJECT_ID" = B."BUSINESSPROJECT_ID"
            AND A."PAYMENTCONFIRM_VALID" = 1
            AND A."MERCHANTS_ID" IS NOT NULL
            AND A."ACCOUNT_TYPE" = 1000
            AND A."CURRENTBALANCE" <> 0
            AND B."PROJECT_VALID" > 0
            AND A."ACCOUNT_DATE" <= {stat_date_str}{exists_sql}"""
    arr_rows = db.execute_query(sql_arrearage) or []
    sales_per_sqm = round(_safe_dec(arr_rows[0].get("TOTAL_BALANCE")) if arr_rows else 0, 2)

    # 到期合同
    stat_dt = dt.strptime(statistics_date, "%Y-%m-%d") if "-" in statistics_date else dt.strptime(statistics_date, "%Y%m%d")
    stat_short = stat_dt.strftime("%Y/%m/%d")

    sql_expired = f"""SELECT
            CASE WHEN "COMPACT_ENDDATE" < ADD_MONTHS(TRUNC(SYSDATE),1) THEN 1
                WHEN "COMPACT_ENDDATE" > ADD_MONTHS(TRUNC(SYSDATE),1) AND
                    "COMPACT_ENDDATE" <= ADD_MONTHS(TRUNC(SYSDATE),3) THEN 2
                ELSE 3 END AS "EXPIRED_SITUATION",
            A."REGISTERCOMPACT_ID", A."COMPACT_NAME",
            TO_CHAR(A."COMPACT_ENDDATE", 'YYYY-MM-DD') AS "COMPACT_ENDDATE"
        FROM "T_REGISTERCOMPACT" A
        WHERE "COMPACT_STATE" = 1000
            AND "COMPACT_ENDDATE" > TO_DATE('{stat_short}','YYYY/MM/DD')
            AND "COMPACT_ENDDATE" <= ADD_MONTHS(TO_DATE('{stat_short}','YYYY/MM/DD'),6){exists_sql}"""
    expired_rows = db.execute_query(sql_expired) or []

    expired_3 = [r for r in expired_rows if _safe_int(r.get("EXPIRED_SITUATION")) == 3]
    contract_list = []
    if expired_3:
        expired_3.sort(key=lambda x: x.get("COMPACT_ENDDATE", ""))
        for r in expired_3:
            contract_list.append({
                "name": r.get("COMPACT_NAME", ""),
                "value": str(r.get("COMPACT_ENDDATE", "")).split(" ")[0]
            })

    return {
        "ContractProfitLoss": contract_profit_loss,
        "ShopCount": shop_count,
        "SalesPerSquareMeter": sales_per_sqm,
        "ExpiredShopCount": len(expired_3),
        "ContractList": contract_list if contract_list else None,
        "ContractCompletionDegree": 67.1,
        "ConvertRate": 50.5,
    }


def get_merchant_account_split(db: DatabaseHelper, statistics_month: str,
                               statistics_start_month: str, calc_type: int,
                               compact_types: str, business_types: str,
                               settlement_mods: str, merchant_ids: str,
                               sort_str: str) -> Optional[dict]:
    """获取经营商户应收拆分数据"""
    where_parts = ['"MERCHANTSPLIT_STATE" = 1']
    params = []

    if compact_types:
        where_parts.append(f'"COMPACT_TYPE" IN ({compact_types})')
    if business_types:
        where_parts.append(f'"BUSINESS_TYPE" IN ({business_types})')
    if settlement_mods:
        where_parts.append(f'"SETTLEMENT_MODES" IN ({settlement_mods})')
    if merchant_ids:
        where_parts.append(f'"MERCHANTS_ID" IN ({merchant_ids})')

    month_str = statistics_month.replace("-", "") if statistics_month else ""
    start_month_str = statistics_start_month.replace("-", "") if statistics_start_month else ""

    if calc_type == 1:
        where_parts.append('"STATISTICS_MONTH" = ?')
        params.append(int(month_str))
    else:
        where_parts.append('"STATISTICS_MONTH" >= ? AND "STATISTICS_MONTH" <= ?')
        params.append(int(start_month_str))
        params.append(int(month_str))

    where_sql = " AND ".join(where_parts)
    sql = f"""SELECT "MERCHANTS_ID", COUNT("BUSINESSPROJECT_ID") AS "PROJECT_COUNT",
        SUM("REVENUEDAILY_AMOUNT") AS "REVENUE_AMOUNT",
        SUM("ROYALTYDAILY_PRICE") AS "ROYALTY_PRICE",
        SUM("SUBROYALTYDAILY_PRICE") AS "SUBROYALTY_PRICE",
        SUM("TICKETDAILY_FEE") AS "TICKET_FEE",
        SUM("ROYALTYDAILY_THEORY") AS "ROYALTY_THEORY",
        SUM("SUBROYALTYDAILY_THEORY") AS "SUBROYALTY_THEORY"
    FROM "T_MERCHANTSPLIT"
    WHERE {where_sql}
    GROUP BY "MERCHANTS_ID" """
    rows = db.execute_query(sql, params)
    if not rows:
        return None

    total_project = sum(r.get("PROJECT_COUNT", 0) or 0 for r in rows)
    total_sub_royalty_price = sum(float(r.get("SUBROYALTY_PRICE", 0) or 0) for r in rows)
    total_sub_royalty_theory = sum(float(r.get("SUBROYALTY_THEORY", 0) or 0) for r in rows)

    merchant_names = {}
    try:
        merchant_rows = db.execute_query('SELECT "COOPMERCHANTS_ID", "COOPMERCHANTS_NAME" FROM "T_COOPMERCHANTS"')
        merchant_names = {r["COOPMERCHANTS_ID"]: r["COOPMERCHANTS_NAME"] for r in merchant_rows}
    except:
        pass

    merchant_list = []
    for r in rows:
        mid = r.get("MERCHANTS_ID")
        if not mid or int(mid) == 0:
            continue
        sub_price = float(r.get("SUBROYALTY_PRICE", 0) or 0)
        sub_theory = float(r.get("SUBROYALTY_THEORY", 0) or 0)
        merchant_list.append({
            "MerchantId": int(mid),
            "MerchantName": merchant_names.get(mid, "") if mid else "",
            "ProjectCount": int(r.get("PROJECT_COUNT", 0) or 0),
            "SubRoyaltyPrice": round(sub_price, 2),
            "SubRoyaltyTheory": round(sub_theory, 2),
            "ReceivableAmount": round(sub_price - sub_theory, 2),
            "ProjectDetailList": None,
        })

    _sort_merchant_list(merchant_list, sort_str)

    return {
        "ProjectCount": total_project,
        "SubRoyaltyPrice": round(total_sub_royalty_price, 2),
        "SubRoyaltyTheory": round(total_sub_royalty_theory, 2),
        "ReceivableAmount": round(total_sub_royalty_price - total_sub_royalty_theory, 2),
        "MerchantAccountList": merchant_list,
        "ProjectDetailList": None,
    }


def get_merchant_account_detail(db: DatabaseHelper, merchant_id: int,
                                statistics_month: str, statistics_start_month: str,
                                calc_type: int, compact_types: str, business_types: str,
                                settlement_mods: str, sort_str: str) -> Optional[dict]:
    """获取经营商户应收拆分明细"""
    where_sql = f" AND MERCHANTS_ID = {merchant_id}"
    if compact_types:
        where_sql += f" AND COMPACT_TYPE IN ({compact_types})"
    if business_types:
        where_sql += f" AND BUSINESS_TYPE IN ({business_types})"
    if settlement_mods:
        where_sql += f" AND SETTLEMENT_MODES IN ({settlement_mods})"
    if calc_type == 1:
        where_sql += f" AND STATISTICS_MONTH = {statistics_month}"
    else:
        where_sql += f" AND STATISTICS_MONTH >= {statistics_start_month} AND STATISTICS_MONTH <= {statistics_month}"

    sql = f"""SELECT * FROM "T_MERCHANTSPLIT"
        WHERE "MERCHANTSPLIT_STATE" = 1{where_sql}"""
    rows = db.execute_query(sql) or []
    if not rows:
        return None

    total_sub_royalty_price = sum(_safe_dec(r.get("SUBROYALTY_PRICE")) for r in rows)
    total_sub_royalty_theory = sum(_safe_dec(r.get("SUBROYALTY_THEORY")) for r in rows)

    merchant_name = ""
    m_rows = db.execute_query(f"""SELECT "COOPMERCHANTS_NAME" FROM "T_COOPMERCHANTS"
        WHERE "COOPMERCHANTS_ID" = {merchant_id}""") or []
    if m_rows:
        merchant_name = m_rows[0].get("COOPMERCHANTS_NAME", "")

    brand_rows = db.execute_query("""SELECT "BRAND_ID","BRAND_NAME","BRAND_INTRO"
        FROM "T_BRAND" WHERE "PROVINCE_CODE" = 340000""") or []
    brand_map = {str(b.get("BRAND_ID", "")): {
        "BrandId": _safe_int(b.get("BRAND_ID")),
        "BrandName": b.get("BRAND_NAME", ""),
        "BrandICO": b.get("BRAND_INTRO", ""),
    } for b in brand_rows}

    sp_groups = defaultdict(list)
    for r in rows:
        sp_groups[str(r.get("SERVERPART_ID", ""))].append(r)

    project_detail_list = []
    for sp_id, sp_rows in sp_groups.items():
        sp_name = sp_rows[0].get("SERVERPART_NAME", "")
        sp_sub_price = sum(_safe_dec(r.get("SUBROYALTY_PRICE")) for r in sp_rows)
        sp_sub_theory = sum(_safe_dec(r.get("SUBROYALTY_THEORY")) for r in sp_rows)

        brand_account_list = []
        for dr in sp_rows:
            brand_model = {
                "BusinessType": _safe_int(dr.get("BUSINESS_TYPE")),
                "SettlementMods": _safe_int(dr.get("SETTLEMENT_MODES")),
                "SubRoyaltyPrice": _safe_dec(dr.get("SUBROYALTY_PRICE")),
                "SubRoyaltyTheory": _safe_dec(dr.get("SUBROYALTY_THEORY")),
                "ReceivableAmount": round(_safe_dec(dr.get("SUBROYALTY_PRICE")) - _safe_dec(dr.get("SUBROYALTY_THEORY")), 2),
                "BrandId": None, "BrandName": None, "BrandICO": None,
            }
            shop_id = str(dr.get("SERVERPARTSHOP_ID", ""))
            if shop_id:
                shop_rows = db.execute_query(f"""SELECT "BUSINESS_BRAND","BRAND_NAME"
                    FROM "T_SERVERPARTSHOP"
                    WHERE "SERVERPARTSHOP_ID" IN ({shop_id}) AND "BUSINESS_BRAND" IS NOT NULL""") or []
                if shop_rows:
                    b_id = str(shop_rows[0].get("BUSINESS_BRAND", ""))
                    if b_id in brand_map:
                        brand_model["BrandId"] = brand_map[b_id]["BrandId"]
                        brand_model["BrandName"] = brand_map[b_id]["BrandName"]
                        brand_model["BrandICO"] = brand_map[b_id]["BrandICO"]
                        if brand_model["BrandICO"] and brand_model["BrandICO"].startswith("/"):
                            brand_model["BrandICO"] = "http://yida.anhighway.cn" + brand_model["BrandICO"]
                    else:
                        brand_model["BrandId"] = _safe_int(b_id)
                        brand_model["BrandName"] = shop_rows[0].get("BRAND_NAME", "")
            brand_account_list.append(brand_model)

        _sort_detail_list(brand_account_list, sort_str)
        project_detail_list.append({
            "ServerpartId": sp_id, "ServerpartName": sp_name,
            "BrandCount": len(sp_rows),
            "SubRoyaltyPrice": round(sp_sub_price, 2),
            "SubRoyaltyTheory": round(sp_sub_theory, 2),
            "ReceivableAmount": round(sp_sub_price - sp_sub_theory, 2),
            "BrandAccountList": brand_account_list,
        })

    _sort_detail_list(project_detail_list, sort_str)

    return {
        "MerchantId": merchant_id, "MerchantName": merchant_name,
        "ProjectCount": len(rows),
        "SubRoyaltyPrice": round(total_sub_royalty_price, 2),
        "SubRoyaltyTheory": round(total_sub_royalty_theory, 2),
        "ReceivableAmount": round(total_sub_royalty_price - total_sub_royalty_theory, 2),
        "ProjectDetailList": project_detail_list,
    }


def _sort_merchant_list(lst: list, sort_str: str):
    """通用排序"""
    if sort_str:
        sort_field = sort_str.split(' ')[0]
        desc = sort_str.lower().endswith(" desc")
        field_map = {"SubRoyaltyPrice": "SubRoyaltyPrice", "SubRoyaltyTheory": "SubRoyaltyTheory",
                     "ReceivableAmount": "ReceivableAmount"}
        if sort_field in field_map:
            lst.sort(key=lambda x: x.get(field_map[sort_field], 0), reverse=desc)
        else:
            lst.sort(key=lambda x: x.get("ProjectCount", 0), reverse=True)
    else:
        lst.sort(key=lambda x: x.get("ProjectCount", 0), reverse=True)


def _sort_detail_list(lst: list, sort_str: str):
    """明细排序"""
    if not sort_str:
        return
    sort_key = sort_str.split(" ")[0]
    is_desc = sort_str.lower().endswith(" desc")
    sort_fn = {"SubRoyaltyPrice": lambda x: x.get("SubRoyaltyPrice", 0),
               "SubRoyaltyTheory": lambda x: x.get("SubRoyaltyTheory", 0),
               "ReceivableAmount": lambda x: x.get("ReceivableAmount", 0)}.get(sort_key)
    if sort_fn:
        lst.sort(key=sort_fn, reverse=is_desc)
