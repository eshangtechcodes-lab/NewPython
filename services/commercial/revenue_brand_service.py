# -*- coding: utf-8 -*-
"""
CommercialApi - 品牌营收 + 结账数据 Service
从 revenue_router.py 中抽取: GetServerpartBrand, _get_end_account_data,
GetServerpartEndAccountList, GetShopEndAccountList
每个函数独立、可单独迁移
"""
from typing import Optional
from collections import defaultdict
from core.database import DatabaseHelper


def _sf(v):
    try: return float(v) if v is not None else 0.0
    except: return 0.0


# ===== 1. GetServerpartBrand =====
def get_serverpart_brand(db: DatabaseHelper, serverpart_id, statistics_time, push_province_code) -> dict:
    """获取服务区品牌营收"""
    from datetime import datetime, timedelta

    stat_time = statistics_time or datetime.now().strftime("%Y-%m-%d")
    stat_dt = datetime.strptime(stat_time.split(" ")[0], "%Y-%m-%d")
    table_suffix = "" if stat_dt < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=9) else "_TEMP"

    # 品牌详情
    brand_rows = db.execute_query(
        'SELECT "BRAND_ID", "BRAND_INTRO" FROM "T_BRAND" WHERE "BRAND_STATE" = 1 AND "PROVINCE_CODE" = :pc',
        {"pc": push_province_code}) or []
    brand_intro_map = {str(r["BRAND_ID"]): r["BRAND_INTRO"] for r in brand_rows}

    # 业态字典
    auto_rows = db.execute_query(
        'SELECT "AUTOSTATISTICS_ID", "AUTOSTATISTICS_NAME", "AUTOSTATISTICS_PID" FROM "T_AUTOSTATISTICS" WHERE "AUTOSTATISTICS_TYPE" = 2000 AND "PROVINCE_CODE" = :pc',
        {"pc": push_province_code}) or []
    auto_map = {str(r["AUTOSTATISTICS_ID"]): r for r in auto_rows}

    where_sql = f" AND A.SERVERPART_ID = {serverpart_id}" if serverpart_id else ""
    revenue_sql = f"""
        SELECT A.SERVERPARTSHOP_ID,
            NVL(A.BUSINESS_TRADE, -1) AS BUSINESS_TRADE,
            NVL(A.BUSINESS_BRAND, -1) AS BUSINESS_BRAND,
            NVL(A.BRAND_NAME, '其他') AS BRAND_NAME,
            NVL(A.BUSINESS_TRADENAME, '其他') AS BUSINESS_TRADENAME,
            SUM(NVL(B.CASHPAY, 0)) AS FACTAMOUNT,
            A.SERVERPART_ID, A.SERVERPART_NAME
        FROM T_SERVERPARTSHOP A, T_ENDACCOUNT{table_suffix} B
        WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPCODE = B.SHOPCODE
            AND A.STATISTIC_TYPE = 1000 AND A.ISVALID = 1 AND B.VALID = 1
            AND A.SHOPTRADE IS NOT NULL
            AND B.STATISTICS_DATE >= TO_DATE('{stat_dt.strftime("%Y/%m/%d")}', 'YYYY/MM/DD')
            AND B.STATISTICS_DATE < TO_DATE('{stat_dt.strftime("%Y/%m/%d")}', 'YYYY/MM/DD') + 1
            {where_sql}
        GROUP BY A.SERVERPARTSHOP_ID, NVL(A.BUSINESS_TRADE, -1), NVL(A.BUSINESS_BRAND, -1),
            NVL(A.BRAND_NAME, '其他'), NVL(A.BUSINESS_TRADENAME, '其他'), A.SERVERPART_ID, A.SERVERPART_NAME"""
    rev_rows = db.execute_query(revenue_sql) or []

    if not rev_rows:
        return {"Serverpart_Id": None, "Serverpart_Name": None, "Revenue_Amount": None,
                "listCurBusinessModel": None, "listBusinessModel": None}

    sp_id = rev_rows[0]["SERVERPART_ID"]
    sp_name = rev_rows[0]["SERVERPART_NAME"]
    total_revenue = sum(_sf(r["FACTAMOUNT"]) for r in rev_rows)

    # 按父级业态聚合
    parent_trade_groups = defaultdict(list)
    for r in rev_rows:
        trade_id = str(r["BUSINESS_TRADE"])
        trade_info = auto_map.get(trade_id)
        pid = str(trade_info["AUTOSTATISTICS_PID"]) if trade_info and str(trade_info["AUTOSTATISTICS_PID"]) != "-1" else trade_id
        p_name = auto_map[pid]["AUTOSTATISTICS_NAME"] if pid in auto_map else "其他"
        parent_trade_groups[(pid, p_name)].append(r)

    list_business_model = []
    for (pid, pname), items in parent_trade_groups.items():
        p_rev = sum(_sf(it["FACTAMOUNT"]) for it in items)
        list_shop_brand = []
        for it in items:
            brand_id = str(it["BUSINESS_BRAND"])
            ico = brand_intro_map.get(brand_id, "")
            brand_ico = ico if (not ico or ico.startswith("http")) else f"http://img.eshang.com{ico}"
            list_shop_brand.append({
                "ServerpartShop_Id": str(it["SERVERPARTSHOP_ID"]),
                "Brand_Id": int(it["BUSINESS_BRAND"]),
                "Brand_Name": it["BRAND_NAME"],
                "Revenue_Amount": round(_sf(it["FACTAMOUNT"]), 2),
                "Business_Trade": str(it["BUSINESS_TRADE"]),
                "Bussiness_Name": it["BUSINESS_TRADENAME"],
                "Brand_ICO": brand_ico,
            })
        list_business_model.append({
            "Business_Trade": pid, "Bussiness_Name": pname,
            "Revenue_Amount": round(p_rev, 2), "listShopBrandModel": list_shop_brand,
        })

    return {
        "Revenue_Amount": round(total_revenue, 2),
        "Serverpart_Id": int(sp_id), "Serverpart_Name": sp_name,
        "listBusinessModel": list_business_model, "listCurBusinessModel": [],
    }


# ===== 2. _get_end_account_data (结账数据核心逻辑) =====
def get_end_account_data(db: DatabaseHelper, serverpart_id: int, statistics_date: str,
                          serverpart_shop_ids: str = None) -> tuple[Optional[dict], list]:
    """获取结账数据，返回 (common_info, shop_end_account_list)"""
    from datetime import datetime, timedelta

    stat_date_str = statistics_date.split(" ")[0] if statistics_date else datetime.now().strftime("%Y-%m-%d")
    st_date = datetime.strptime(stat_date_str, "%Y-%m-%d")
    is_history = st_date < (datetime.now() - timedelta(days=9))
    table_name = "T_ENDACCOUNT" if is_history else "T_ENDACCOUNT_TEMP"

    where_sql = f" AND A.SERVERPART_ID = {serverpart_id}"
    if serverpart_shop_ids:
        ids_str = ",".join([str(i.strip()) for i in serverpart_shop_ids.split(",") if i.strip().isdigit()])
        if ids_str:
            where_sql += f" AND B.SERVERPARTSHOP_ID IN ({ids_str})"

    sql = f"""SELECT A.*, B.SERVERPARTSHOP_ID, B.SHOPREGION, B.SHOPTRADE, B.SHOPNAME,
            B.BUSINESS_BRAND, NVL(B.BRAND_NAME, B.SHOPSHORTNAME) AS BRAND_NAME_FIX,
            B.SERVERPART_NAME AS SERVERPART_NAME_FIX
        FROM {table_name} A
            JOIN T_SERVERPARTSHOP B ON A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPCODE = B.SHOPCODE
        WHERE A.VALID = 1 {where_sql}
            AND A.STATISTICS_DATE >= TO_DATE('{stat_date_str}', 'YYYY-MM-DD')
            AND A.STATISTICS_DATE < TO_DATE('{stat_date_str}', 'YYYY-MM-DD') + 1
        ORDER BY B.SERVERPART_NAME, B.SHOPREGION, B.SHOPTRADE, B.SHOPCODE, A.ENDACCOUNT_DATE"""

    rows = db.execute_query(sql)
    if not rows:
        return None, []

    shop_groups = defaultdict(list)
    common_info = {
        "Serverpart_ID": rows[0]["SERVERPART_ID"],
        "Serverpart_Name": rows[0]["SERVERPART_NAME_FIX"],
        "TotalAmount": sum(_sf(r["CASHPAY"]) for r in rows),
    }
    for r in rows: shop_groups[r["SERVERPARTSHOP_ID"]].append(r)

    shop_end_account_list = []
    upload_count = 0
    for shop_id, s_rows in shop_groups.items():
        first_r = s_rows[0]
        biz_type = int(first_r["BUSINESS_TYPE"] or 1000)
        shop_model = {
            "SERVERPARTSHOP_ID": int(shop_id), "SHOPNAME": first_r["SHOPNAME"],
            "SERVERPART_ID": int(first_r["SERVERPART_ID"]),
            "SERVERPART_NAME": first_r["SERVERPART_NAME_FIX"],
            "BUSINESS_TYPE": biz_type,
            "BUSINESS_TYPENAME": {1000: "自营", 2000: "合作经营", 3000: "固定租金", 4000: "展销"}.get(biz_type, "其他"),
            "SHOWABNORMAL_SIGN": 0, "SHOWSCAN_SIGN": 0, "INTERFACE_SIGN": 0,
            "SHOWSSUPPLY_SIGN": 0, "SHOWCHECK_SIGN": 0, "SHOWDEAL_SIGN": 0, "UNACCOUNT_SIGN": 0,
            "CASHPAY_TOTAL": sum(_sf(r["CASHPAY"]) for r in s_rows),
            "ShopEndAccountList": [],
        }

        for r in s_rows:
            check_info = r.get("CHECK_INFO")
            sell_amt = _sf(r.get("TOTALSELLAMOUNT"))
            cash_pay = _sf(r.get("CASHPAY"))
            diff_price = _sf(r.get("DIFFERENT_PRICE"))
            if check_info and (sell_amt > cash_pay or (sell_amt + diff_price) > cash_pay):
                shop_model["SHOWABNORMAL_SIGN"] = 1
            worker = str(r.get("WORKER_NAME") or "")
            if "【扫】" in worker or "【扫码】" in worker: shop_model["SHOWSCAN_SIGN"] = 1
            elif "【接口】" in worker: shop_model["INTERFACE_SIGN"] = 1
            desc_staff = str(r.get("DESCRIPTION_STAFF") or "")
            if "【补】" in desc_staff: shop_model["SHOWSSUPPLY_SIGN"] = 1
            if int(r.get("CHECK_COUNT") or 0) > 0: shop_model["SHOWCHECK_SIGN"] = 1
            if check_info: shop_model["SHOWDEAL_SIGN"] = 1
            diff_reason = r.get("DIFFERENCE_REASON")
            if not diff_reason or diff_reason != "无结账信息": shop_model["UNACCOUNT_SIGN"] = 1
            transfer_type = 0
            if "【扫】" in worker: transfer_type = 1
            elif "【补】" in desc_staff: transfer_type = 2
            elif "接口" in worker or "扫码" in worker: transfer_type = 3
            shop_model["ShopEndAccountList"].append({
                "TRANSFER_TYPE": transfer_type,
                "ENDACCOUNT_STARTDATE": str(r.get("ENDACCOUNT_STARTDATE") or ""),
                "ENDACCOUNT_DATE": str(r.get("ENDACCOUNT_DATE") or ""),
                "DESCRIPTION_STAFF": desc_staff, "DIFFERENCE_REASON": diff_reason,
                "DESCRIPTION_DATE": str(r.get("DESCRIPTION_DATE") or ""),
                "CASHPAY": cash_pay, "CASH": _sf(r.get("CASH")),
                "DIFFERENT_PRICE": diff_price, "CHECK_COUNT": int(r.get("CHECK_COUNT") or 0),
            })

        if shop_model["UNACCOUNT_SIGN"] == 1: upload_count += 1
        shop_end_account_list.append(shop_model)

    common_info["UploadShopCount"] = upload_count
    common_info["TotalShopCount"] = len(shop_end_account_list)
    return common_info, shop_end_account_list
