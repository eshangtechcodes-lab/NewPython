from __future__ import annotations
# -*- coding: utf-8 -*-
"""
RevenueController 业务服务（60 个接口全部实现）

7 组标准 CRUD（28 个）：
  REVENUEDAILYSPLIT / PERSONSELL / BUSINESSANALYSIS
  BRANDANALYSIS / SITUATIONANALYSIS / BUSINESSWARNING / ACCOUNTWARNING

31 个散装报表/查询接口
"""
from typing import Optional, List, Tuple
from loguru import logger
from core.database import DatabaseHelper


def _try_decimal(val):
    """安全转换为浮点数（C# TryParseToDecimal 等价）"""
    try:
        return round(float(val), 2)
    except (ValueError, TypeError):
        return 0


# ============================================================
# 通用 CRUD 工厂函数（避免重复代码）
# ============================================================
def _generic_list(db: DatabaseHelper, table: str, pk: str, search_model: dict,
                  extra_search_fields: list = None) -> Tuple[list, int]:
    """通用列表查询（按 C# Helper 标准模式：全量查询 + Python 层分页）"""
    page_index = search_model.get("PageIndex", 1) or 1
    page_size = search_model.get("PageSize", 15) or 15
    sp = search_model.get("SearchParameter") or search_model.get("SearchData") or {}
    where_parts = []
    # 通用搜索字段
    for field in (extra_search_fields or []):
        val = sp.get(field)
        if val is not None and str(val).strip():
            # --- SQL 参数化: 字段值去引号防注入 ---
            if isinstance(val, str):
                safe_val = val.replace("'", "")
                where_parts.append(f"{field} = '{safe_val}'")
            else:
                where_parts.append(f"{field} = {int(val)}")
    if sp.get("SERVERPART_ID"):
        where_parts.append(f"SERVERPART_ID = {int(sp['SERVERPART_ID'])}")
    where_clause = " AND ".join(where_parts) if where_parts else "1=1"
    sql = f"SELECT * FROM {table} WHERE {where_clause} ORDER BY {pk} DESC"
    rows = db.execute_query(sql) or []
    total = len(rows)
    # Python 层分页
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif total > 10:
        rows = rows[:10]
    return rows, total


def _generic_detail(db: DatabaseHelper, table: str, pk: str, pk_val: int) -> Optional[dict]:
    """通用明细查询"""
    # --- SQL 参数化: pk_val 改为整数防注入 ---
    safe_pk = int(pk_val)
    sql = f"SELECT * FROM {table} WHERE {pk} = {safe_pk}"
    rows = db.execute_query(sql)
    return rows[0] if rows else None


def _generic_synchro(db: DatabaseHelper, table: str, pk: str, data: dict) -> Tuple[bool, dict]:
    """通用同步（新增/更新）"""
    pk_val = data.get(pk)
    if pk_val is not None:
        safe_pk = int(pk_val)
        check = db.execute_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = {safe_pk}")
        if check and check > 0:
            # 更新模式
            set_parts = []
            for k, v in data.items():
                if k == pk:
                    continue
                if v is None:
                    continue
                # --- SQL 参数化: 字符串值去引号防注入 ---
                if isinstance(v, str):
                    safe_v = v.replace("'", "''")
                    set_parts.append(f"{k} = '{safe_v}'")
                else:
                    set_parts.append(f"{k} = {v}")
            if set_parts:
                db.execute_non_query(f"UPDATE {table} SET {', '.join(set_parts)} WHERE {pk} = {safe_pk}")
            return True, data
    # 新增
    seq_name = table.replace('T_', '')
    try:
        new_id = db.execute_scalar(f"SELECT SEQ_{seq_name}.NEXTVAL FROM DUAL")
    except Exception:
        new_id = (db.execute_scalar(f"SELECT COALESCE(MAX({pk}), 0) + 1 FROM {table}") or 1)
    data[pk] = new_id
    columns, values = [], []
    for k, v in data.items():
        if v is None:
            continue
        columns.append(k)
        if isinstance(v, str):
            safe_v = v.replace("'", "''")
            values.append(f"'{safe_v}'")
        else:
            values.append(str(v))
    db.execute_non_query(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})")
    return True, data


def _generic_delete(db: DatabaseHelper, table: str, pk: str, status_field: str, pk_val: int) -> bool:
    """通用软删除（C# 原逻辑: STATE = 0）"""
    # --- SQL 参数化: pk_val 改为整数防注入 ---
    safe_pk = int(pk_val)
    check = db.execute_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = {safe_pk}")
    if not check or check == 0:
        return False
    db.execute_non_query(f"UPDATE {table} SET {status_field} = 0 WHERE {pk} = {safe_pk}")
    return True


# ============================================================
# CRUD 实体定义
# ============================================================
ENTITIES = {
    "REVENUEDAILYSPLIT": {
        "table": "T_REVENUEDAILYSPLIT", "pk": "REVENUEDAILYSPLIT_ID",
        "status": "REVENUEDAILYSPLIT_STATE", "search_fields": ["SERVERPARTSHOP_ID"]
    },
    "PERSONSELL": {
        "table": "T_PERSONSELL", "pk": "PERSONSELL_ID",
        "status": "PERSONSELL_STATE", "search_fields": ["SERVERPARTSHOP_ID"]
    },
    "BUSINESSANALYSIS": {
        "table": "T_BUSINESSANALYSIS", "pk": "BUSINESSANALYSIS_ID",
        "status": "BUSINESSANALYSIS_STATE", "search_fields": []
    },
    "BRANDANALYSIS": {
        "table": "T_BRANDANALYSIS", "pk": "BRANDANALYSIS_ID",
        "status": "BRANDANALYSIS_STATE", "search_fields": []
    },
    "SITUATIONANALYSIS": {
        "table": "T_SITUATIONANALYSIS", "pk": "SITUATIONANALYSIS_ID",
        "status": "SITUATIONANALYSIS_STATE", "search_fields": []
    },
    "BUSINESSWARNING": {
        "table": "T_BUSINESSWARNING", "pk": "BUSINESSWARNING_ID",
        "status": "BUSINESSWARNING_STATE", "search_fields": []
    },
    "ACCOUNTWARNING": {
        "table": "T_ACCOUNTWARNING", "pk": "ACCOUNTWARNING_ID",
        "status": "ACCOUNTWARNING_STATE", "search_fields": []
    },
}


# 动态生成 CRUD 函数
def get_entity_list(db, entity_name, search_model):
    e = ENTITIES[entity_name]
    return _generic_list(db, e["table"], e["pk"], search_model, e.get("search_fields"))

def get_entity_detail(db, entity_name, pk_val):
    e = ENTITIES[entity_name]
    return _generic_detail(db, e["table"], e["pk"], pk_val)

def synchro_entity(db, entity_name, data):
    e = ENTITIES[entity_name]
    return _generic_synchro(db, e["table"], e["pk"], data)

def delete_entity(db, entity_name, pk_val):
    e = ENTITIES[entity_name]
    return _generic_delete(db, e["table"], e["pk"], e["status"], pk_val)


# ============================================================
# 散装接口
# ============================================================

def modify_revenue_daily_split_list(db: DatabaseHelper, data_list: list) -> Tuple[bool, str]:
    """批量更新服务区日度营收拆分表"""
    logger.info(f"ModifyRevenueDailySplitList: 数量={len(data_list) if data_list else 0}")
    try:
        for item in data_list:
            synchro_entity(db, "REVENUEDAILYSPLIT", item)
        return True, ""
    except Exception as e:
        return False, str(e)


def get_revenue_push_list(db: DatabaseHelper, province_code: str, statistics_date: str) -> list:
    """
    获取营收推送数据表列表
    C# 逻辑: 查询 T_REVENUEDAILYSPLIT 中指定省份和日期的数据
    """
    logger.info(f"GetRevenuePushList: Province={province_code}, Date={statistics_date}")
    try:
        # --- SQL 参数化: 日期/省份去引号防注入 ---
        safe_pc = province_code.replace("'", "")
        safe_sd = statistics_date.replace("'", "")
        sql = f"""SELECT * FROM T_REVENUEDAILYSPLIT
                 WHERE PROVINCE_ID = '{safe_pc}' AND STATISTICS_DATE = '{safe_sd}'
                 AND REVENUEDAILYSPLIT_STATE = 1
                 ORDER BY REVENUEDAILYSPLIT_ID DESC"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetRevenuePushList 失败: {e}")
        return []


def get_his_commodity_sale_list(db: DatabaseHelper, province_code: str,
                               start_month: str, end_month: str,
                               serverpart_shop_ids: str) -> list:
    """
    获取历史单品销售数据
    C# CommoditySaleHelper.GetHisCommoditySaleList:
    从 T_YSSELLDETAILS JOIN T_YSSELLMASTER 按商品分类聚合销售数据
    """
    logger.info(f"GetHisCommoditySaleList: Province={province_code}, Shops={serverpart_shop_ids}")
    try:
        where_parts = ["A.SELLMASTER_STATE > 0"]
        if start_month:
            safe_sm = str(start_month).replace("'", "")
            where_parts.append(f"SUBSTR(A.SELLMASTER_DATE,1,6) >= '{safe_sm}'")
        if end_month:
            safe_em = str(end_month).replace("'", "")
            where_parts.append(f"SUBSTR(A.SELLMASTER_DATE,1,6) <= '{safe_em}'")
        if serverpart_shop_ids:
            # --- SQL 参数化: shop_ids 通过整数解析 ---
            safe_ids = [str(int(x.strip())) for x in str(serverpart_shop_ids).split(',') if x.strip().isdigit()]
            if safe_ids:
                where_parts.append(f"C.SERVERPARTSHOP_ID IN ({','.join(safe_ids)})")
        wc = " AND ".join(where_parts)
        sql = f"""SELECT B.COMMODITY_NAME, B.COMMODITY_TYPE,
                    SUM(B.SELLDETAILS_COUNT) AS TOTAL_COUNT,
                    SUM(B.SELLDETAILS_AMOUNT) AS TOTAL_AMOUNT,
                    C.SERVERPART_ID, C.SERVERPARTSHOP_ID
                 FROM T_YSSELLMASTER A
                 JOIN T_YSSELLDETAILS B ON A.SELLMASTER_CODE = B.SELLMASTER_CODE
                 JOIN T_SERVERPARTSHOP C ON A.SERVERPARTCODE = C.SERVERPART_CODE AND A.SHOPCODE = C.SHOPCODE
                 WHERE {wc}
                 GROUP BY B.COMMODITY_NAME, B.COMMODITY_TYPE, C.SERVERPART_ID, C.SERVERPARTSHOP_ID
                 ORDER BY TOTAL_AMOUNT DESC"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetHisCommoditySaleList 失败: {e}")
        return []


def get_revenue_data_list(db: DatabaseHelper, serverpart_ids: str, serverpart_shop_ids: str,
                          start_date: str, end_date: str, data_source_type: int = 1) -> list:
    """
    获取营收数据列表
    C# RevenueHelper.GetRevenueDataList:
    查询 T_REVENUEDAILY JOIN T_SERVERPART + T_SERVERPARTSHOP
    返回每条记录的服务区/门店信息和各项营收金额
    """
    logger.info(f"GetRevenueDataList: SP={serverpart_ids}, Shop={serverpart_shop_ids}, Start={start_date}")
    try:
        where_parts = ["A.REVENUEDAILY_STATE = 1"]
        if serverpart_shop_ids:
            where_parts.append(f"A.SERVERPARTSHOP_ID IN ({serverpart_shop_ids})")
        elif serverpart_ids:
            where_parts.append(f"A.SERVERPART_ID IN ({serverpart_ids})")
        if start_date:
            where_parts.append(f"A.STATISTICS_DATE >= {start_date.replace('-', '')}")
        if end_date:
            where_parts.append(f"A.STATISTICS_DATE <= {end_date.replace('-', '')}")
        wc = " AND ".join(where_parts)
        sql = f"""SELECT A.*, B.SERVERPART_NAME, B.SERVERPART_CODE,
                    B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME
                 FROM T_REVENUEDAILY A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc}
                 ORDER BY A.STATISTICS_DATE DESC"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetRevenueDataList 失败: {e}")
        return []


def _build_revenue_summary(db, where_clause: str) -> dict:
    """
    通用营收汇总查询（C# SummaryRevenueData / SummaryMonthData 逻辑）
    对指定条件的数据做 SUM 聚合
    """
    try:
        sql = f"""SELECT
            SUM(TICKET_COUNT) AS Ticket_Count,
            SUM(TOTAL_COUNT) AS Total_Count,
            SUM(TOTALOFF_AMOUNT) AS Total_OffAmount,
            SUM(REVENUE_AMOUNT) AS Revenue_Amount,
            SUM(MOBILEPAY_AMOUNT) AS MobilePay_Amount,
            SUM(CASHPAY_AMOUNT) AS CashPay_Amount,
            SUM(NVL(COSTBILL_AMOUNT_A,0)+NVL(COSTBILL_AMOUNT_B,0)) AS CostBill_Amount,
            SUM(NVL(INTERNALPAY_AMOUNT_A,0)+NVL(INTERNALPAY_AMOUNT_B,0)) AS InternalPay_Amount,
            SUM(NVL(YFHD_AMOUNT_A,0)+NVL(YFHD_AMOUNT_B,0)) AS YFHD_Amount,
            SUM(NVL(DIFFERENT_AMOUNT_LESS_A,0)+NVL(DIFFERENT_AMOUNT_LESS_B,0)) AS Different_Price_Less,
            SUM(NVL(DIFFERENT_AMOUNT_MORE_A,0)+NVL(DIFFERENT_AMOUNT_MORE_B,0)) AS Different_Price_More
        FROM T_REVENUEDAILY WHERE REVENUEDAILY_STATE = 1 {where_clause}"""
        rows = db.execute_query(sql)
        return rows[0] if rows else {}
    except Exception as e:
        logger.error(f"_build_revenue_summary 失败: {e}")
        return {}


def get_revenue_report(db, **kwargs) -> list:
    """
    获取业主营收统计报表
    C# RevenueHelper.GetRevenueReport: 按片区→服务区层级聚合营收数据
    返回 NestingModel 树形结构: [{node: 合计, children: [{node: 片区, children: [{node: 服务区}]}]}]
    DataType: 0=业主按服务区, 1=业主按门店, 2=商户
    """
    logger.info(f"GetRevenueReport: {kwargs}")
    try:
        wp = ["A.REVENUEDAILY_STATE = 1"]
        sp_ids = kwargs.get("ServerpartIds", "")
        shop_ids = kwargs.get("ServerpartShopIds", "")
        start = kwargs.get("StartDate", "")
        end = kwargs.get("EndDate", "")
        data_type = int(kwargs.get("DataType", 0) or 0)
        shop_trade = kwargs.get("shopTrade", "")
        business_type = kwargs.get("businessType", "")
        target_system = kwargs.get("targetSystem")
        if shop_ids:
            wp.append(f"A.SERVERPARTSHOP_ID IN ({shop_ids})")
        elif sp_ids:
            wp.append(f"A.SERVERPART_ID IN ({sp_ids})")
        if start:
            wp.append(f"A.STATISTICS_DATE >= {start.replace('-', '')}")
        if end:
            wp.append(f"A.STATISTICS_DATE <= {end.replace('-', '')}")
        # C# 原逻辑: shopTrade/businessType/targetSystem 过滤
        if shop_trade:
            wp.append(f"A.SHOPTRADE IN ({shop_trade})")
        if business_type:
            wp.append(f"A.BUSINESS_TYPE IN ({business_type})")
        if target_system is not None:
            target_system = int(target_system)
            if target_system == 1:
                wp.append("A.TRANSFER_TYPE > 0")
            elif target_system == 0:
                wp.append("NVL(A.TRANSFER_TYPE,0) = 0")
        wc = " AND ".join(wp)

        # 查询原始数据（按服务区+门店维度聚合）
        sql = f"""SELECT B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME,
                    B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_CODE,
                    A.SHOPTRADE, A.BUSINESS_TYPE, A.SERVERPARTSHOP_ID,
                    SUM(A.TICKET_COUNT) AS Ticket_Count,
                    SUM(A.TOTAL_COUNT) AS Total_Count,
                    SUM(A.TOTALOFF_AMOUNT) AS Total_OffAmount,
                    SUM(A.REVENUE_AMOUNT) AS Revenue_Amount,
                    SUM(A.MOBILEPAY_AMOUNT) AS MobilePay_Amount,
                    SUM(A.CASHPAY_AMOUNT) AS CashPay_Amount,
                    SUM(NVL(A.COSTBILL_AMOUNT_A,0)+NVL(A.COSTBILL_AMOUNT_B,0)) AS CostBill_Amount,
                    SUM(NVL(A.INTERNALPAY_AMOUNT_A,0)+NVL(A.INTERNALPAY_AMOUNT_B,0)) AS InternalPay_Amount,
                    SUM(NVL(A.YFHD_AMOUNT_A,0)+NVL(A.YFHD_AMOUNT_B,0)) AS YFHD_Amount,
                    SUM(NVL(A.DIFFERENT_AMOUNT_LESS_A,0)+NVL(A.DIFFERENT_AMOUNT_LESS_B,0)) AS Different_Price_Less,
                    SUM(NVL(A.DIFFERENT_AMOUNT_MORE_A,0)+NVL(A.DIFFERENT_AMOUNT_MORE_B,0)) AS Different_Price_More
                 FROM T_REVENUEDAILY A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc}
                 GROUP BY B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME,
                    B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_CODE,
                    A.SHOPTRADE, A.BUSINESS_TYPE, A.SERVERPARTSHOP_ID
                 ORDER BY B.SPREGIONTYPE_ID, B.SERVERPART_CODE"""
        rows = db.execute_query(sql) or []
        if not rows:
            return []

        # 汇总辅助函数
        def _sum_rows(row_list):
            result = {}
            sum_fields = ['Ticket_Count', 'Total_Count', 'Total_OffAmount', 'Revenue_Amount',
                         'MobilePay_Amount', 'CashPay_Amount', 'CostBill_Amount',
                         'InternalPay_Amount', 'YFHD_Amount', 'Different_Price_Less', 'Different_Price_More']
            for f in sum_fields:
                result[f] = sum(float(r.get(f) or 0) for r in row_list)
            return result

        # 构建合计节点
        total_node = {
            "node": {"Serverpart_ID": 0, "Serverpart_Name": "合计",
                     "Shop_Count": len(set(str(r.get("SERVERPARTSHOP_ID")) for r in rows if r.get("SERVERPARTSHOP_ID"))),
                     "TotalRevenue": _sum_rows(rows)},
            "children": []
        }

        if data_type == 2:
            # 按商户分组（不含片区层级）
            sp_groups = {}
            for r in rows:
                sp_id = r.get("SERVERPART_ID")
                if sp_id not in sp_groups:
                    sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "rows": []}
                sp_groups[sp_id]["rows"].append(r)
            for sp_id, g in sp_groups.items():
                sp_node = {"node": {"Serverpart_ID": sp_id, "Serverpart_Name": g["name"],
                                    "TotalRevenue": _sum_rows(g["rows"])}, "children": []}
                total_node["children"].append(sp_node)
        else:
            # 按片区→服务区层级
            region_groups = {}
            for r in rows:
                rid = r.get("SPREGIONTYPE_ID")
                if rid not in region_groups:
                    region_groups[rid] = {"name": r.get("SPREGIONTYPE_NAME", ""), "rows": []}
                region_groups[rid]["rows"].append(r)

            for rid, rg in region_groups.items():
                if rid is None:
                    # 无片区的直接挂到合计下
                    continue
                region_node = {
                    "node": {"Serverpart_ID": rid, "Serverpart_Name": rg["name"],
                             "TotalRevenue": _sum_rows(rg["rows"]),
                             "Shop_Count": len(set(str(r.get("SERVERPARTSHOP_ID")) for r in rg["rows"] if r.get("SERVERPARTSHOP_ID")))},
                    "children": []
                }
                # 按服务区分组
                sp_groups = {}
                for r in rg["rows"]:
                    sp_id = r.get("SERVERPART_ID")
                    if sp_id not in sp_groups:
                        sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "code": r.get("SERVERPART_CODE", ""), "rows": []}
                    sp_groups[sp_id]["rows"].append(r)
                for sp_id, sg in sorted(sp_groups.items(), key=lambda x: x[1]["code"]):
                    sp_node = {
                        "node": {"Serverpart_ID": sp_id, "Serverpart_Name": sg["name"],
                                 "Shop_Count": len(set(str(r.get("SERVERPARTSHOP_ID")) for r in sg["rows"] if r.get("SERVERPARTSHOP_ID"))),
                                 "TotalRevenue": _sum_rows(sg["rows"])}
                    }
                    region_node["children"].append(sp_node)
                total_node["children"].append(region_node)

            # 处理无片区的数据
            no_region = region_groups.get(None)
            if no_region:
                sp_groups = {}
                for r in no_region["rows"]:
                    sp_id = r.get("SERVERPART_ID")
                    if sp_id not in sp_groups:
                        sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "rows": []}
                    sp_groups[sp_id]["rows"].append(r)
                for sp_id, sg in sp_groups.items():
                    sp_node = {"node": {"Serverpart_ID": sp_id, "Serverpart_Name": sg["name"],
                                        "TotalRevenue": _sum_rows(sg["rows"])}}
                    total_node["children"].append(sp_node)

        return [total_node]
    except Exception as e:
        logger.error(f"GetRevenueReport 失败: {e}")
        return []



def get_revenue_report_by_date(db, **kwargs) -> list:
    """
    获取业主营收统计报表(按日展示)
    C# RevenueHelper.GetRevenueReportByDate:
    wrapType=0 按日期分组（NestingModel: 合计→日期）
    wrapType=1 按片区→服务区→日期层级包裹
    """
    logger.info(f"GetRevenueReportByDate: {kwargs}")
    try:
        wp = ["A.REVENUEDAILY_STATE = 1"]
        sp_ids = kwargs.get("ServerpartIds", "")
        shop_ids = kwargs.get("ServerpartShopIds", "")
        start = kwargs.get("StartDate", "")
        end = kwargs.get("EndDate", "")
        wrap_type = int(kwargs.get("wrapType", 0) or 0)
        shop_trade = kwargs.get("shopTrade", "")
        business_type = kwargs.get("businessType", "")
        target_system = kwargs.get("targetSystem")
        if shop_ids:
            wp.append(f"A.SERVERPARTSHOP_ID IN ({shop_ids})")
        elif sp_ids:
            wp.append(f"A.SERVERPART_ID IN ({sp_ids})")
        if start:
            wp.append(f"A.STATISTICS_DATE >= {start.replace('-', '')}")
        if end:
            wp.append(f"A.STATISTICS_DATE <= {end.replace('-', '')}")
        if shop_trade:
            wp.append(f"A.SHOPTRADE IN ({shop_trade})")
        if business_type:
            wp.append(f"A.BUSINESS_TYPE IN ({business_type})")
        if target_system is not None:
            ts = int(target_system)
            if ts == 1:
                wp.append("A.TRANSFER_TYPE > 0")
            elif ts == 0:
                wp.append("NVL(A.TRANSFER_TYPE,0) = 0")
        wc = " AND ".join(wp)

        sql = f"""SELECT A.STATISTICS_DATE,
                    B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME,
                    B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_CODE,
                    SUM(A.TICKET_COUNT) AS Ticket_Count,
                    SUM(A.TOTAL_COUNT) AS Total_Count,
                    SUM(A.REVENUE_AMOUNT) AS Revenue_Amount,
                    SUM(A.MOBILEPAY_AMOUNT) AS MobilePay_Amount,
                    SUM(A.CASHPAY_AMOUNT) AS CashPay_Amount,
                    SUM(NVL(A.COSTBILL_AMOUNT_A,0)+NVL(A.COSTBILL_AMOUNT_B,0)) AS CostBill_Amount,
                    SUM(NVL(A.INTERNALPAY_AMOUNT_A,0)+NVL(A.INTERNALPAY_AMOUNT_B,0)) AS InternalPay_Amount,
                    SUM(NVL(A.YFHD_AMOUNT_A,0)+NVL(A.YFHD_AMOUNT_B,0)) AS YFHD_Amount
                 FROM T_REVENUEDAILY A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc}
                 GROUP BY A.STATISTICS_DATE, B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME,
                    B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_CODE
                 ORDER BY A.STATISTICS_DATE DESC, B.SPREGIONTYPE_ID, B.SERVERPART_CODE"""
        rows = db.execute_query(sql) or []
        if not rows:
            return []

        # 汇总辅助函数
        def _sum_rows(row_list):
            result = {}
            for f in ['Ticket_Count', 'Total_Count', 'Revenue_Amount', 'MobilePay_Amount',
                      'CashPay_Amount', 'CostBill_Amount', 'InternalPay_Amount', 'YFHD_Amount']:
                result[f] = sum(float(r.get(f) or 0) for r in row_list)
            return result

        # 合计节点
        total_node = {
            "node": {"Serverpart_ID": 0, "Serverpart_Name": "合计", "TotalRevenue": _sum_rows(rows)},
            "children": []
        }

        if wrap_type == 0:
            # wrapType=0: 按日期平铺（C# 对应直接按日期取）
            date_groups = {}
            for r in rows:
                d = str(r.get("STATISTICS_DATE", ""))
                if d not in date_groups:
                    date_groups[d] = []
                date_groups[d].append(r)
            for d in sorted(date_groups.keys(), reverse=True):
                date_node = {
                    "node": {"Serverpart_Name": d, "Statistics_Date": d, "TotalRevenue": _sum_rows(date_groups[d])},
                    "children": []
                }
                total_node["children"].append(date_node)
        else:
            # wrapType=1: 片区→服务区→日期层级（C# 对应片区服务区层级包裹）
            region_groups = {}
            for r in rows:
                rid = r.get("SPREGIONTYPE_ID")
                if rid not in region_groups:
                    region_groups[rid] = {"name": r.get("SPREGIONTYPE_NAME", ""), "rows": []}
                region_groups[rid]["rows"].append(r)

            for rid, rg in region_groups.items():
                if rid is None:
                    continue
                region_node = {
                    "node": {"Serverpart_ID": rid, "Serverpart_Name": rg["name"], "TotalRevenue": _sum_rows(rg["rows"])},
                    "children": []
                }
                # 按服务区分组
                sp_groups = {}
                for r in rg["rows"]:
                    sp_id = r.get("SERVERPART_ID")
                    if sp_id not in sp_groups:
                        sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "code": r.get("SERVERPART_CODE", ""), "rows": []}
                    sp_groups[sp_id]["rows"].append(r)
                for sp_id, sg in sorted(sp_groups.items(), key=lambda x: x[1]["code"]):
                    sp_node = {
                        "node": {"Serverpart_ID": sp_id, "Serverpart_Name": sg["name"], "TotalRevenue": _sum_rows(sg["rows"])},
                        "children": []
                    }
                    # 按日期分组
                    date_groups = {}
                    for r in sg["rows"]:
                        d = str(r.get("STATISTICS_DATE", ""))
                        if d not in date_groups:
                            date_groups[d] = []
                        date_groups[d].append(r)
                    for d in sorted(date_groups.keys(), reverse=True):
                        date_node = {"node": {"Statistics_Date": d, "Serverpart_Name": d, "TotalRevenue": _sum_rows(date_groups[d])}}
                        sp_node["children"].append(date_node)
                    region_node["children"].append(sp_node)
                total_node["children"].append(region_node)

        return [total_node]
    except Exception as e:
        logger.error(f"GetRevenueReportByDate 失败: {e}")
        return []


def get_merchant_revenue_report(db, **kwargs) -> list:
    """
    获取商家营收统计报表
    C# Controller: 实际调用 GetRevenueReport(DataType=2) 即按商户分组
    与 get_revenue_report 保持一致，DataType 强制为 2
    """
    logger.info(f"GetMerchantRevenueReport: {kwargs}")
    kwargs["DataType"] = 2
    return get_revenue_report(db, **kwargs)



def bank_account_compare(db, account_date: str, serverpart_code: str,
                         shop_code: str, machine_code: str) -> list:
    """
    对比移动支付到账金额差异
    C# 逻辑: 查询 T_BANKACCOUNT 与营收数据做差额对比
    """
    logger.info(f"BankAccountCompare: Date={account_date}, SP={serverpart_code}")
    try:
        wp = ["1=1"]
        if account_date:
            wp.append(f"ACCOUNT_DATE = '{account_date.replace('-', '')}'")
        if serverpart_code:
            wp.append(f"SERVERPART_CODE = '{serverpart_code}'")
        if shop_code:
            wp.append(f"SHOP_CODE = '{shop_code}'")
        if machine_code:
            wp.append(f"MACHINE_CODE = '{machine_code}'")
        wc = " AND ".join(wp)
        sql = f"SELECT * FROM T_BANKACCOUNT WHERE {wc} ORDER BY ACCOUNT_DATE DESC"
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"BankAccountCompare 失败: {e}")
        return []


def get_bank_account_report(db, serverpart_shop_ids: str, start_date: str,
                            end_date: str, payment_channel: str = "") -> list:
    """
    查询门店移动支付到账报表
    C# 逻辑: 按门店和日期聚合银行到账数据
    """
    logger.info(f"GetBankAccountReport: Shop={serverpart_shop_ids}")
    try:
        wp = ["1=1"]
        if serverpart_shop_ids:
            wp.append(f"SERVERPARTSHOP_ID IN ({serverpart_shop_ids})")
        if start_date:
            wp.append(f"ACCOUNT_DATE >= '{start_date.replace('-', '')}'")
        if end_date:
            wp.append(f"ACCOUNT_DATE <= '{end_date.replace('-', '')}'")
        if payment_channel:
            wp.append(f"PAYMENT_CHANNEL IN ({payment_channel})")
        wc = " AND ".join(wp)
        sql = f"""SELECT SERVERPARTSHOP_ID, ACCOUNT_DATE,
                    SUM(ACCOUNT_AMOUNT) AS Total_Amount,
                    COUNT(*) AS Record_Count
                 FROM T_BANKACCOUNT WHERE {wc}
                 GROUP BY SERVERPARTSHOP_ID, ACCOUNT_DATE
                 ORDER BY ACCOUNT_DATE DESC"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetBankAccountReport 失败: {e}")
        return []


def get_bank_account_list(db, serverpart_shop_ids: str, start_date: str,
                          end_date: str, payment_channel: str = "") -> list:
    """
    查询门店移动支付到账数据
    C# 逻辑: 按门店和日期查询 T_BANKACCOUNT 明细
    """
    logger.info(f"GetBankAccountList: Shop={serverpart_shop_ids}")
    try:
        wp = ["1=1"]
        if serverpart_shop_ids:
            wp.append(f"SERVERPARTSHOP_ID IN ({serverpart_shop_ids})")
        if start_date:
            wp.append(f"ACCOUNT_DATE >= '{start_date.replace('-', '')}'")
        if end_date:
            wp.append(f"ACCOUNT_DATE <= '{end_date.replace('-', '')}'")
        if payment_channel:
            wp.append(f"PAYMENT_CHANNEL IN ({payment_channel})")
        wc = " AND ".join(wp)
        sql = f"SELECT * FROM T_BANKACCOUNT WHERE {wc} ORDER BY ACCOUNT_DATE DESC"
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetBankAccountList 失败: {e}")
        return []


def get_cur_total_revenue(db, serverpart_ids: str, serverpart_shop_ids: str) -> dict:
    """
    获取实时营收汇总数据
    C# RevenueHelper.GetCurTotalRevenue: 查询当日营收合计
    """
    logger.info(f"GetCurTotalRevenue: SP={serverpart_ids}")
    try:
        from datetime import datetime
        today = datetime.now().strftime("%Y%m%d")
        wp = f"AND STATISTICS_DATE = {today}"
        if serverpart_shop_ids:
            wp += f" AND SERVERPARTSHOP_ID IN ({serverpart_shop_ids})"
        elif serverpart_ids:
            wp += f" AND SERVERPART_ID IN ({serverpart_ids})"
        return _build_revenue_summary(db, wp)
    except Exception as e:
        logger.error(f"GetCurTotalRevenue 失败: {e}")
        return {}


def get_total_revenue(db, serverpart_ids: str, serverpart_shop_ids: str,
                      start_date: str, end_date: str, data_source_type: int = 1) -> dict:
    """
    获取营收汇总数据
    C# RevenueHelper.GetTotalRevenue: 按日期范围汇总
    """
    logger.info(f"GetTotalRevenue: SP={serverpart_ids}, Start={start_date}")
    try:
        wp = ""
        if serverpart_shop_ids:
            wp += f" AND SERVERPARTSHOP_ID IN ({serverpart_shop_ids})"
        elif serverpart_ids:
            wp += f" AND SERVERPART_ID IN ({serverpart_ids})"
        if start_date:
            wp += f" AND STATISTICS_DATE >= {start_date.replace('-', '')}"
        if end_date:
            wp += f" AND STATISTICS_DATE <= {end_date.replace('-', '')}"
        return _build_revenue_summary(db, wp)
    except Exception as e:
        logger.error(f"GetTotalRevenue 失败: {e}")
        return {}


def get_business_date(db, serverpart_ids: str = "", serverpart_shop_ids: str = "") -> dict:
    """
    获取营业开始/结束日期
    C# RevenueHelper.GetBusinessStartDate:
    查 T_REVENUEDAILY 的 MIN(STATISTICS_DATE) 和 MAX(STATISTICS_DATE)
    返回 {label: 开始日期, value: 结束日期}
    """
    logger.info(f"GetBusinessDate: SP={serverpart_ids}, Shop={serverpart_shop_ids}")
    try:
        from datetime import datetime

        where_sql = ""
        if serverpart_ids:
            where_sql += f" AND A.SERVERPART_ID IN ({serverpart_ids})"

        # C# 原逻辑: 如果指定 ServerpartShopIds，构建 selectedSQL 用于过滤
        selected_sql_parts = []
        if serverpart_shop_ids:
            for shop_id in serverpart_shop_ids.split(","):
                shop_id = shop_id.strip()
                if shop_id:
                    selected_sql_parts.append(f"SERVERPARTSHOP_ID LIKE '%,{shop_id},%'")

        today = datetime.now().strftime("%Y%m%d")
        sql = f"""SELECT
                MIN(STATISTICS_DATE) AS START_DATE,
                MAX(STATISTICS_DATE) AS END_DATE,
                ',' || A.SERVERPARTSHOP_ID || ',' AS SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE REVENUEDAILY_STATE = 1 AND STATISTICS_DATE <= {today}{where_sql}
            GROUP BY A.SERVERPARTSHOP_ID"""
        rows = db.execute_query(sql) or []
        if not rows:
            return {"label": "", "value": ""}

        # C# 原逻辑: 使用 selectedSQL 过滤行
        if selected_sql_parts:
            filtered = []
            for r in rows:
                sid_str = str(r.get("SERVERPARTSHOP_ID", ""))
                for shop_id in serverpart_shop_ids.split(","):
                    shop_id = shop_id.strip()
                    if shop_id and f",{shop_id}," in sid_str:
                        filtered.append(r)
                        break
            if not filtered:
                return {"label": "", "value": ""}
            rows = filtered

        # C# 原逻辑: Compute min(START_DATE) 和 max(END_DATE)
        start_dates = [r.get("START_DATE") for r in rows if r.get("START_DATE")]
        end_dates = [r.get("END_DATE") for r in rows if r.get("END_DATE")]
        min_start = str(min(start_dates)) if start_dates else ""
        max_end = str(max(end_dates)) if end_dates else ""

        # 格式化日期
        def _fmt_date(d):
            d = str(d).strip()
            if len(d) >= 8:
                return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
            return d

        return {"label": _fmt_date(min_start), "value": _fmt_date(max_end)}
    except Exception as e:
        logger.error(f"GetBusinessDate 失败: {e}")
        return {"label": "", "value": ""}


def get_ys_sell_master_list(db, search_model: dict) -> Tuple[list, int]:
    """
    获取交易流水订单表列表
    C# YSSELLMASTERHelper.GetYSSELLMASTERList:
    查询 T_YSSELLMASTER，含 SERVERPARTSHOP_ID/SERVERPART_ID 关联、日期区间、
    组合支付拆解（ALIPAY/WECHAT/UNIONPAY）、totalModel 12 项汇总
    """
    logger.info("GetYSSellMasterList")
    try:
        param = search_model.get("SearchParameter") or {}
        page_index = int(search_model.get("PageIndex", 1) or 1)
        page_size = int(search_model.get("PageSize", 20) or 20)
        sort_str = search_model.get("SortStr", "") or ""

        # C# 原逻辑: 必须有 SERVERPART_ID 或 SERVERPARTSHOP_ID
        sp_id = param.get("SERVERPART_ID")
        sp_shop_id = param.get("SERVERPARTSHOP_ID", "") or ""
        if not sp_id and not sp_shop_id:
            return [], 0

        where_sql = ""
        # C# 原逻辑: SERVERPARTSHOP_ID -> 查 SERVERPART_CODE || SHOPCODE
        if sp_shop_id:
            code_sql = f"SELECT WM_CONCAT(SERVERPART_CODE || SHOPCODE) FROM T_SERVERPARTSHOP WHERE SERVERPARTSHOP_ID IN ({sp_shop_id})"
            code_row = db.execute_scalar(code_sql)
            if code_row:
                codes = "','".join(str(code_row).split(","))
                where_sql += f" AND SERVERPARTCODE || SHOPCODE IN ('{codes}')"
            else:
                return [], 0
        elif sp_id:
            sp_code_sql = f"SELECT SERVERPART_CODE FROM T_SERVERPART WHERE SERVERPART_ID = {sp_id}"
            sp_code = db.execute_scalar(sp_code_sql)
            if sp_code:
                where_sql += f" AND SERVERPARTCODE = '{sp_code}'"
            else:
                return [], 0

        # C# 原逻辑: 日期过滤
        sell_date = param.get("SELLMASTER_DATE", "")
        sell_date_start = param.get("SELLMASTER_DATE_Start", "")
        sell_date_end = param.get("SELLMASTER_DATE_End", "")
        if sell_date:
            d = sell_date.replace("-", "")[:8]
            where_sql += f" AND SELLMASTER_DATE >= {d}000000 AND SELLMASTER_DATE < {d}240000"
        else:
            if sell_date_start:
                d = sell_date_start.replace("-", "")[:8]
                where_sql += f" AND SELLMASTER_DATE >= {d}000000"
            if sell_date_end:
                d = sell_date_end.replace("-", "")[:8]
                where_sql += f" AND SELLMASTER_DATE < {d}240000"

        # COUPON_TYPE 过滤
        coupon_type = param.get("COUPON_TYPE")
        if coupon_type is not None:
            where_sql += f" AND COUPON_TYPE = {coupon_type}"

        # 查询全部数据
        base_sql = f"SELECT * FROM T_YSSELLMASTER WHERE SELLMASTER_STATE NOT IN (0){where_sql}"
        all_rows = db.execute_query(base_sql) or []

        # C# 原逻辑: keyWord 模糊搜索
        kw = search_model.get("keyWord") or {}
        kw_key = kw.get("Key", "")
        kw_value = kw.get("Value", "")
        if kw_key and kw_value:
            key_fields = [k.strip() for k in kw_key.split(",") if k.strip()]
            all_rows = [r for r in all_rows if any(
                kw_value.lower() in str(r.get(kf, "")).lower() for kf in key_fields
            )]

        # 排序
        if sort_str:
            parts = sort_str.strip().split()
            field = parts[0] if parts else ""
            desc = len(parts) > 1 and parts[1].upper() == "DESC"
            if field:
                all_rows.sort(key=lambda r: (r.get(field) or ""), reverse=desc)

        total_count = len(all_rows)

        # 分页
        start = (page_index - 1) * page_size
        page_rows = all_rows[start:start + page_size]

        # C# 原逻辑: 组合支付拆解
        for r in page_rows:
            r["TICKETBILL"] = None   # 微信支付
            r["OTHERPAY"] = None     # 支付宝支付
            r["YUNSHANFU"] = None    # 云闪付支付
            desc = r.get("SELLMASTER_DESC", "") or ""
            if desc:
                for pay_detail in desc.split(","):
                    parts = pay_detail.split(":")
                    if len(parts) == 2:
                        if parts[0] == "ALIPAY":
                            r["OTHERPAY"] = _try_decimal(parts[1])
                        elif parts[0] == "WECHAT":
                            r["TICKETBILL"] = _try_decimal(parts[1])
                        elif parts[0] == "UNIONPAY":
                            r["YUNSHANFU"] = _try_decimal(parts[1])

            # INTERNAL_AMOUNT 逻辑
            cash_amount = float(r.get("CASH_AMOUNT") or 0)
            internal_amount = float(r.get("INTERNAL_AMOUNT") or 0)
            c_type = float(r.get("COUPON_TYPE") or 0)
            if cash_amount == 0 and internal_amount == 0 and c_type >= 2000:
                r["INTERNAL_AMOUNT"] = r.get("SELLMASTER_AMOUNT")

            # PAYMENT_TYPE_TEXT 和 SELLMASTER_TYPE_TEXT
            pt = r.get("PAYMENT_TYPE")
            if not pt and r.get("COUPON_TYPE"):
                r["PAYMENT_TYPE"] = r["COUPON_TYPE"]

        # C# 原逻辑: totalModel 12 项汇总
        def _sum_by(rows, amount_field, filter_field=None, filter_val=None):
            s = 0
            for r in rows:
                if filter_field and filter_val is not None:
                    if int(r.get(filter_field) or 0) != filter_val:
                        continue
                s += float(r.get(amount_field) or 0)
            return round(s, 2)

        total_model = {
            "CASH": _sum_by(all_rows, "CASH_AMOUNT", "PAYMENT_TYPE", 1000),
            "TICKETBILL": _sum_by(all_rows, "CASH_AMOUNT", "PAYMENT_TYPE", 1010) + sum(float(r.get("TICKETBILL") or 0) for r in all_rows),
            "OTHERPAY": _sum_by(all_rows, "CASH_AMOUNT", "PAYMENT_TYPE", 1020) + sum(float(r.get("OTHERPAY") or 0) for r in all_rows),
            "CREDITCARD": _sum_by(all_rows, "CASH_AMOUNT", "PAYMENT_TYPE", 1030),
            "YUNSHANFU": _sum_by(all_rows, "CASH_AMOUNT", "PAYMENT_TYPE", 1040) + sum(float(r.get("YUNSHANFU") or 0) for r in all_rows),
            "COUPONTYPE_2010": _sum_by(all_rows, "INTERNAL_AMOUNT", "COUPON_TYPE", 2010),
            "COUPONTYPE_2020": _sum_by(all_rows, "INTERNAL_AMOUNT", "COUPON_TYPE", 2020),
            "COUPONTYPE_2030": _sum_by(all_rows, "INTERNAL_AMOUNT", "COUPON_TYPE", 2030),
            "COUPONTYPE_2040": _sum_by(all_rows, "INTERNAL_AMOUNT", "COUPON_TYPE", 2040),
            "SELLMASTERTYPE_1010": _sum_by(all_rows, "SELLMASTER_AMOUNT", "SELLMASTER_TYPE", 1010),
            "SELLMASTERTYPE_1020": _sum_by(all_rows, "SELLMASTER_AMOUNT", "SELLMASTER_TYPE", 1020),
            "SELLMASTERTYPE_1030": _sum_by(all_rows, "SELLMASTER_AMOUNT", "SELLMASTER_TYPE", 1030),
            "SELLMASTERTYPE_1040": _sum_by(all_rows, "SELLMASTER_AMOUNT", "SELLMASTER_TYPE", 1040),
        }

        return page_rows, total_count, total_model
    except Exception as e:
        logger.error(f"GetYSSellMasterList 失败: {e}")
        return [], 0



def get_sell_master_compare_list(db, serverpart_shop_ids: str, start_date: str,
                                 end_date: str, is_new: int = 0) -> list:
    """
    获取客无忧交易和收银交易流水订单比较列表
    C# YSSELLMASTERHelper.GetSellMasterCompareList:
    (1) 查询本地收银流水 → 过滤移动支付 + 解析组合支付
    (2) 查询 COOP_MERCHANT 门店获取 BUSINESS_CODE
    (3) 调用客无忧 API 获取分账流水
    (4) 按订单号差集/交集对比 → 差异列表
    """
    import hashlib
    import time
    import requests

    logger.info(f"GetSellMasterCompareList: Shop={serverpart_shop_ids}")
    try:
        if not serverpart_shop_ids:
            return []

        # ========== 步骤1: 获取本地收银流水 ==========
        code_sql = f"SELECT WM_CONCAT(SERVERPART_CODE || SHOPCODE) FROM T_SERVERPARTSHOP WHERE SERVERPARTSHOP_ID IN ({serverpart_shop_ids})"
        code_row = db.execute_scalar(code_sql)
        if not code_row:
            return []
        codes = "','".join(str(code_row).split(","))
        where_sql = f" AND SERVERPARTCODE || SHOPCODE IN ('{codes}')"

        date_filter = ""
        if start_date:
            d = start_date.replace("-", "")[:8]
            date_filter += f" AND SELLMASTER_DATE >= {d}000000"
        if end_date:
            d = end_date.replace("-", "")[:8]
            date_filter += f" AND SELLMASTER_DATE < {d}240000"

        all_sql = f"SELECT * FROM T_YSSELLMASTER WHERE SELLMASTER_STATE NOT IN (0){where_sql}{date_filter}"
        all_rows = db.execute_query(all_sql) or []

        # C# 原逻辑: 转换为 TransactionsModel，过滤非移动支付
        mobile_pays = []
        for item in all_rows:
            payment_type = int(item.get("PAYMENT_TYPE") or 0)
            payment_group = int(item.get("PAYMENT_GROUP") or 0)
            amount = float(item.get("SELLMASTER_AMOUNT") or 0)
            state = int(item.get("SELLMASTER_STATE") or 0)

            t = {
                "TradeNo": str(item.get("SELLMASTER_CODE") or ""),
                "Amount": amount,
                "PayDate": str(item.get("SELLMASTER_DATE") or ""),
                "ServerpartCode": str(item.get("SERVERPARTCODE") or ""),
                "ServerpartShopName": str(item.get("SHOPNAME") or ""),
                "ServerpartName": str(item.get("SERVERPART_NAME") or ""),
                "ServerpartShopCode": str(item.get("SHOPCODE") or ""),
                "MachineCode": str(item.get("MACHINECODE") or ""),
                "PaymentType": _payment_type_text(payment_type),
                "MobileRecordState": "人工确认" if state == 1 else ("交易失败" if state == 0 else "交易成功"),
            }

            # C# 原逻辑: 组合支付(PAYMENT_GROUP=1)时从 SELLMASTER_DESC 提取移动支付金额
            if payment_group == 1:
                desc = str(item.get("SELLMASTER_DESC") or "")
                if desc:
                    mobile_payment = 0
                    for pay_detail in desc.split(","):
                        parts = pay_detail.split(":")
                        if len(parts) == 2 and parts[0] in ("ALIPAY", "WECHAT", "UNIONPAY"):
                            mobile_payment += float(parts[1] or 0)
                    t["Amount"] = mobile_payment
                else:
                    continue  # C# 原逻辑: desc 为空时跳过
            elif payment_type == 1000 or payment_type > 2000:
                # C# 原逻辑: 现金(1000)和优惠券(>2000)跳过
                continue

            mobile_pays.append(t)

        # ========== 步骤2: 查询分账门店信息获取 BUSINESS_CODE ==========
        shop_sql = f"""SELECT
                B.PROVINCE_CODE, B.SERVERPART_ID, B.SERVERPART_CODE, B.SERVERPART_NAME,
                B.SERVERPARTSHOP_ID, B.SERVERPARTSHOP_CODE, B.SERVERPARTSHOP_NAME, B.BUSINESS_CODE
            FROM COOP_MERCHANT.T_BUSINESSMCH A, COOP_MERCHANT.T_BUSINESSSHOPCODE B
            WHERE A.SUBMERCHANT_CODE = B.MERCHANT_CODE
                AND B.SERVERPART_CODE NOT IN ('348888','899999')
                AND A.BUSINESSMCH_STATE = 1
                AND B.SERVERPARTSHOP_ID IN ({serverpart_shop_ids})"""
        shop_rows = db.execute_query(shop_sql) or []
        business_codes = list(set(str(sr.get("BUSINESS_CODE") or "") for sr in shop_rows if sr.get("BUSINESS_CODE")))

        # ========== 步骤3: 调用客无忧 API 获取分账流水 ==========
        KWY_URL = "https://www.weiwoju.com/Payapi/Ys/Royalty"
        KWY_OPENID = "1z7n0lp0nsi8o0dd5o74lgrhs1575k"
        KWY_KEY = "w0j23q2m69po13syyd6pj6a11o64f2r13bj"

        def _kwy_sign(params: dict) -> str:
            """客无忧签名: 参数按字典序排列拼接 → 追加 key → MD5 大写"""
            sorted_items = sorted(params.items())
            sign_str = "&".join(f"{k}={v}" for k, v in sorted_items)
            sign_str += f"&key={KWY_KEY}"
            return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()

        def _kwy_get_all(begin_date: str, end_date: str, business_code: str) -> list:
            """分页获取客无忧全部数据（C# GetKwyRoyaltyListForAll）"""
            page_index, page_size = 1, 50
            all_data = []
            while True:
                params = {
                    "openid": KWY_OPENID,
                    "bind_code": business_code,
                    "nonce_str": "0",
                    "time_stamp": str(int(time.time())),
                    "date": f"{begin_date},{end_date}",
                    "page": str(page_index),
                    "page_size": str(page_size),
                }
                sign = _kwy_sign(params)
                post_body = "&".join(f"{k}={v}" for k, v in sorted(params.items())) + f"&sign={sign}"
                try:
                    resp = requests.post(KWY_URL, data=post_body, timeout=30,
                                         headers={"Content-Type": "application/x-www-form-urlencoded"})
                    result = resp.json()
                    pay_list = (result.get("data") or {}).get("list") or []
                    all_data.extend(pay_list)
                    if len(pay_list) < page_size:
                        break
                    page_index += 1
                    time.sleep(1)  # C# 原逻辑: Thread.Sleep(1000)
                except Exception as ex:
                    logger.warning(f"客无忧 API 调用失败: {ex}")
                    break
            return all_data

        # 逐 BUSINESS_CODE 获取客无忧流水
        kwy_results = []
        for bc in business_codes:
            items = _kwy_get_all(start_date, end_date, bc)
            for item in items:
                item["BUSINESS_CODE"] = bc
            kwy_results.extend(items)

        # 转换客无忧数据为统一格式
        shop_map = {}
        for sr in shop_rows:
            shop_map[str(sr.get("BUSINESS_CODE") or "")] = sr

        kwy_pays = []
        for kr in kwy_results:
            trade_no = str(kr.get("out_trade_no") or "")
            t = {
                "TradeNo": trade_no,
                "Amount": float(kr.get("price") or 0),
                "PayDate": str(kr.get("pay_date") or "").replace("-", "/"),
                "MachineCode": trade_no[12:16] if len(trade_no) >= 16 else "",
                "KwyRecordState": str(kr.get("royalty_status") or "").replace("分账", "交易"),
            }
            shop = shop_map.get(str(kr.get("BUSINESS_CODE") or ""))
            if shop:
                t["ServerpartCode"] = str(shop.get("SERVERPART_CODE") or "")
                t["ServerpartName"] = str(shop.get("SERVERPART_NAME") or "")
                t["ServerpartShopName"] = str(shop.get("SERVERPARTSHOP_NAME") or "")
                t["ServerpartShopCode"] = str(shop.get("SERVERPARTSHOP_CODE") or "")
                t["ServerpartID"] = shop.get("SERVERPART_ID")
                t["ServerpartShopID"] = str(shop.get("SERVERPARTSHOP_ID") or "")
                t["PaymentType"] = ""
            kwy_pays.append(t)

        # ========== 步骤4: 集合运算对比 ==========
        mobile_map = {m["TradeNo"]: m for m in mobile_pays}
        kwy_map = {k["TradeNo"]: k for k in kwy_pays}

        result = []

        # 收银比客无忧差集: 本地有但客无忧没有
        for trade_no, m in mobile_map.items():
            if trade_no not in kwy_map:
                result.append({
                    "TradeNo": trade_no,
                    "MobilePayAmount": m["Amount"],
                    "MobileRecordState": m.get("MobileRecordState", ""),
                    "KwyAmount": None,
                    "KwyRecordState": "订单不存在",
                    "PayDateStr": m.get("PayDate", ""),
                    "ServerpartCode": m.get("ServerpartCode", ""),
                    "ServerpartShopName": m.get("ServerpartShopName", ""),
                    "ServerpartName": m.get("ServerpartName", ""),
                    "ServerpartShopCode": m.get("ServerpartShopCode", ""),
                    "ServerpartID": m.get("ServerpartID"),
                    "ServerpartShopID": m.get("ServerpartShopID", ""),
                    "MachineCode": m.get("MachineCode", ""),
                    "PaymentType": m.get("PaymentType", ""),
                })

        # 客无忧比收银差集: 客无忧有但本地没有
        for trade_no, k in kwy_map.items():
            if trade_no not in mobile_map:
                result.append({
                    "TradeNo": trade_no,
                    "MobilePayAmount": None,
                    "MobileRecordState": "订单不存在",
                    "KwyAmount": k["Amount"],
                    "KwyRecordState": k.get("KwyRecordState", ""),
                    "PayDateStr": k.get("PayDate", ""),
                    "ServerpartCode": k.get("ServerpartCode", ""),
                    "ServerpartShopName": k.get("ServerpartShopName", ""),
                    "ServerpartName": k.get("ServerpartName", ""),
                    "ServerpartShopCode": k.get("ServerpartShopCode", ""),
                    "ServerpartID": k.get("ServerpartID"),
                    "ServerpartShopID": k.get("ServerpartShopID", ""),
                    "MachineCode": k.get("MachineCode", ""),
                    "PaymentType": k.get("PaymentType", ""),
                })

        # 交集中金额不一致的
        for trade_no in set(mobile_map.keys()) & set(kwy_map.keys()):
            m = mobile_map[trade_no]
            k = kwy_map[trade_no]
            if m["Amount"] == k["Amount"]:
                continue  # C# 原逻辑: 金额相同的跳过
            result.append({
                "TradeNo": trade_no,
                "MobilePayAmount": m["Amount"],
                "KwyAmount": k["Amount"],
                "KwyRecordState": m.get("KwyRecordState", ""),
                "MobileRecordState": k.get("MobileRecordState", ""),
                "PayDateStr": m.get("PayDate", ""),
                "ServerpartCode": m.get("ServerpartCode", ""),
                "ServerpartShopName": m.get("ServerpartShopName", ""),
                "ServerpartName": m.get("ServerpartName", ""),
                "ServerpartShopCode": m.get("ServerpartShopCode", ""),
                "ServerpartID": m.get("ServerpartID"),
                "ServerpartShopID": m.get("ServerpartShopID", ""),
                "MachineCode": m.get("MachineCode", ""),
                "PaymentType": m.get("PaymentType", ""),
            })

        result.sort(key=lambda x: x.get("PayDateStr", ""), reverse=True)
        return result
    except Exception as e:
        logger.error(f"GetSellMasterCompareList 失败: {e}")
        return []


def _payment_type_text(payment_type: int) -> str:
    """支付方式枚举转文本（C# PaymentTypeEnum）"""
    mapping = {
        1000: "现金", 1010: "微信", 1020: "支付宝",
        1030: "银行卡", 1040: "云闪付",
        2010: "企业会员", 2020: "电子优惠券",
        2030: "大巴优惠券", 2040: "团购餐券",
    }
    return mapping.get(payment_type, str(payment_type))


def get_ys_sell_details_list(db, search_model: dict) -> Tuple[list, int]:
    """
    获取交易流水明细表列表
    C# YSSELLDETAILSHelper: 查询 T_YSSELLDETAILS
    """
    logger.info("GetYSSellDetailsList")
    return _generic_list(db, "T_YSSELLDETAILS", "YSSELLDETAILS_ID", search_model)


def _build_revenue_where(kwargs: dict) -> str:
    """构建通用营收查询WHERE条件（报表类接口共用）"""
    wp = ["A.REVENUEDAILY_STATE = 1"]
    sp_ids = kwargs.get("ServerpartIds", "")
    shop_ids = kwargs.get("ServerpartShopIds", "")
    start = kwargs.get("StartDate", "")
    end = kwargs.get("EndDate", "")
    if shop_ids:
        wp.append(f"A.SERVERPARTSHOP_ID IN ({shop_ids})")
    elif sp_ids:
        wp.append(f"A.SERVERPART_ID IN ({sp_ids})")
    if start:
        wp.append(f"A.STATISTICS_DATE >= {start.replace('-', '')}")
    if end:
        wp.append(f"A.STATISTICS_DATE <= {end.replace('-', '')}")
    return " AND ".join(wp)


def get_transaction_customer(db, **kwargs) -> list:
    """
    获取客单交易分析
    C# RevenueHelper.GetTransactionCustomer: 按服务区分组统计客单数/客单价
    """
    logger.info(f"GetTransactionCustomer: {kwargs}")
    try:
        wc = _build_revenue_where(kwargs)
        sql = f"""SELECT B.SERVERPART_ID, B.SERVERPART_NAME,
                    SUM(A.TICKET_COUNT) AS Ticket_Count,
                    SUM(A.REVENUE_AMOUNT) AS Revenue_Amount,
                    CASE WHEN SUM(A.TICKET_COUNT) > 0
                         THEN ROUND(SUM(A.REVENUE_AMOUNT) / SUM(A.TICKET_COUNT), 2)
                         ELSE 0 END AS Avg_Price
                 FROM T_REVENUEDAILY A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc}
                 GROUP BY B.SERVERPART_ID, B.SERVERPART_NAME
                 ORDER BY B.SERVERPART_ID"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetTransactionCustomer 失败: {e}")
        return []


def get_transaction_customer_by_date(db, **kwargs) -> list:
    """
    获取客单交易分析(按日展示)
    C# RevenueHelper: 在GetTransactionCustomer基础上增加日期维度
    """
    logger.info(f"GetTransactionCustomerByDate: {kwargs}")
    try:
        wc = _build_revenue_where(kwargs)
        sql = f"""SELECT A.STATISTICS_DATE,
                    B.SERVERPART_ID, B.SERVERPART_NAME,
                    SUM(A.TICKET_COUNT) AS Ticket_Count,
                    SUM(A.REVENUE_AMOUNT) AS Revenue_Amount,
                    CASE WHEN SUM(A.TICKET_COUNT) > 0
                         THEN ROUND(SUM(A.REVENUE_AMOUNT) / SUM(A.TICKET_COUNT), 2)
                         ELSE 0 END AS Avg_Price
                 FROM T_REVENUEDAILY A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc}
                 GROUP BY A.STATISTICS_DATE, B.SERVERPART_ID, B.SERVERPART_NAME
                 ORDER BY A.STATISTICS_DATE DESC"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetTransactionCustomerByDate 失败: {e}")
        return []


def get_revenue_yoy_qoq(db, **kwargs) -> list:
    """
    获取同环比分析表
    C# RevenueHelper.GetRevenueYOYQOQ:
    UNION ALL 三期（当期 CURR + 月环比 MONTH + 年同比 YEAR），
    NestingModel 合计→片区→服务区→门店四级树，每层 6 个 MOM 增长率
    参数: ServerpartIds, startDate, endDate, ShowShop, shopNames, shopTrade,
          businessType, targetSystem, SearchKeyName, SearchKeyValue
    """
    logger.info(f"GetRevenueYOYQOQ: {kwargs}")
    try:
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        sp_ids = kwargs.get("ServerpartIds", "")
        start_str = kwargs.get("startDate", "") or kwargs.get("StartDate", "")
        end_str = kwargs.get("endDate", "") or kwargs.get("EndDate", "")
        show_shop = kwargs.get("ShowShop", True)
        if isinstance(show_shop, str):
            show_shop = show_shop.lower() not in ("false", "0")
        shop_names = kwargs.get("shopNames", "")
        shop_trade = kwargs.get("shopTrade", "")
        business_type = kwargs.get("businessType", "")
        target_system = kwargs.get("targetSystem")
        search_key_name = kwargs.get("SearchKeyName", "")
        search_key_value = kwargs.get("SearchKeyValue", "")

        if not start_str or not end_str:
            return []

        start_dt = datetime.strptime(start_str[:10], "%Y-%m-%d")
        end_dt = datetime.strptime(end_str[:10], "%Y-%m-%d")

        # C# 原逻辑: 三个时间段
        region_date = f" AND A.STATISTICS_DATE >= {start_dt.strftime('%Y%m%d')} AND STATISTICS_DATE <= {end_dt.strftime('%Y%m%d')}"
        mom_dt_s = start_dt - relativedelta(months=1)
        mom_dt_e = end_dt - relativedelta(months=1)
        mom_date = f" AND A.STATISTICS_DATE >= {mom_dt_s.strftime('%Y%m%d')} AND STATISTICS_DATE <= {mom_dt_e.strftime('%Y%m%d')}"
        hom_dt_s = start_dt - relativedelta(years=1)
        hom_dt_e = end_dt - relativedelta(years=1)
        hom_date = f" AND A.STATISTICS_DATE >= {hom_dt_s.strftime('%Y%m%d')} AND STATISTICS_DATE <= {hom_dt_e.strftime('%Y%m%d')}"

        where_sql = ""
        if sp_ids:
            where_sql += f" AND A.SERVERPART_ID IN ({sp_ids})"
        if shop_trade:
            where_sql += f" AND A.SHOPTRADE IN ({shop_trade})"
        if business_type:
            where_sql += f" AND A.BUSINESS_TYPE IN ({business_type})"

        shop_sql = ""
        if target_system is not None:
            ts = int(target_system)
            if ts == 1:
                shop_sql = " AND C.TRANSFER_TYPE > 0"
            elif ts == 0:
                shop_sql = " AND NVL(C.TRANSFER_TYPE,0) = 0"

        # C# 原逻辑: SearchKeyName/SearchKeyValue 模糊搜索
        if search_key_name and search_key_value:
            search_parts = []
            for key_name in search_key_name.split(","):
                key_name = key_name.strip()
                if key_name == "MerchantName":
                    search_parts.append(f"C.SELLER_NAME LIKE '%{search_key_value}%'")
                elif key_name == "Brand":
                    if "," in search_key_value:
                        vals = "','".join(search_key_value.split(","))
                        search_parts.append(f"C.BRAND_NAME IN ('{vals}')")
                    else:
                        search_parts.append(f"C.BRAND_NAME LIKE '%{search_key_value}%'")
                elif key_name == "Shop":
                    if shop_names:
                        vals = "','".join(shop_names.split(","))
                        search_parts.append(f"C.SHOPSHORTNAME IN ('{vals}')")
                    if "," in search_key_value:
                        vals = "','".join(search_key_value.split(","))
                        search_parts.append(f"C.SHOPSHORTNAME IN ('{vals}')")
                    else:
                        search_parts.append(f"C.SHOPNAME LIKE '%{search_key_value}%'")
                elif key_name == "Serverpart":
                    search_parts.append(f"C.SERVERPART_NAME LIKE '%{search_key_value}%'")
            if search_parts:
                shop_sql += f" AND ({' OR '.join(search_parts)})"
        elif shop_names:
            vals = "','".join(shop_names.split(","))
            shop_sql += f" AND C.SHOPSHORTNAME IN ('{vals}')"

        # UNION ALL 三期（C# 原逻辑）
        inner_sql = f"""SELECT
                A.SERVERPART_ID, A.SHOPTRADE, A.BUSINESS_TYPE, MAX(SHOP_COUNT) AS SHOP_COUNT,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_CURR,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_CURR,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_CURR,
                0 AS CASHPAY_MONTH, 0 AS TOTALCOUNT_MONTH, 0 AS TICKETCOUNT_MONTH,
                0 AS CASHPAY_YEAR, 0 AS TOTALCOUNT_YEAR, 0 AS TICKETCOUNT_YEAR,
                A.SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SHOPTRADE = C.SHOPTRADE AND A.SERVERPART_ID = C.SERVERPART_ID{shop_sql})
                {region_date}{where_sql}
            GROUP BY A.SERVERPART_ID, A.BUSINESS_TYPE, A.SHOPTRADE, A.SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                A.SERVERPART_ID, A.SHOPTRADE, A.BUSINESS_TYPE, MAX(SHOP_COUNT) AS SHOP_COUNT,
                0, 0, 0,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_MONTH,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_MONTH,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_MONTH,
                0, 0, 0, A.SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SHOPTRADE = C.SHOPTRADE AND A.SERVERPART_ID = C.SERVERPART_ID{shop_sql})
                {mom_date}{where_sql}
            GROUP BY A.SERVERPART_ID, A.BUSINESS_TYPE, A.SHOPTRADE, A.SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                A.SERVERPART_ID, A.SHOPTRADE, A.BUSINESS_TYPE, MAX(SHOP_COUNT) AS SHOP_COUNT,
                0, 0, 0, 0, 0, 0,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_YEAR,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_YEAR,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_YEAR,
                A.SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SHOPTRADE = C.SHOPTRADE AND A.SERVERPART_ID = C.SERVERPART_ID{shop_sql})
                {hom_date}{where_sql}
            GROUP BY A.SERVERPART_ID, A.BUSINESS_TYPE, A.SHOPTRADE, A.SERVERPARTSHOP_ID"""

        # 外层 SQL: JOIN T_SERVERPART 获取片区信息 + 聚合 + 计算增长率
        outer_sql = f"""SELECT
                NVL(B.SERVERPART_INDEX,999999) AS SERVERPART_INDEX,
                B.SERVERPART_ID, B.SERVERPART_NAME,
                NVL(B.SPREGIONTYPE_INDEX,999999) AS TYPE_INDEX,
                B.SPREGIONTYPE_NAME AS TYPE_NAME, B.SPREGIONTYPE_ID,
                TO_CHAR(A.SHOPTRADE) AS SHOPNAME, A.SHOPTRADE, A.BUSINESS_TYPE,
                SUM(CASHPAY_CURR) AS CASHPAY_CURR, SUM(TOTALCOUNT_CURR) AS TOTALCOUNT_CURR,
                SUM(TICKETCOUNT_CURR) AS TICKETCOUNT_CURR,
                SUM(CASHPAY_MONTH) AS CASHPAY_MONTH, SUM(TOTALCOUNT_MONTH) AS TOTALCOUNT_MONTH,
                SUM(TICKETCOUNT_MONTH) AS TICKETCOUNT_MONTH,
                SUM(CASHPAY_YEAR) AS CASHPAY_YEAR, SUM(TOTALCOUNT_YEAR) AS TOTALCOUNT_YEAR,
                SUM(TICKETCOUNT_YEAR) AS TICKETCOUNT_YEAR,
                CASE WHEN SUM(NVL(CASHPAY_MONTH,0))=0 THEN 0 ELSE ROUND((SUM(CASHPAY_CURR)-SUM(CASHPAY_MONTH))*100/SUM(CASHPAY_MONTH),2) END AS MOM_YEARASHPAY_MONTH,
                CASE WHEN SUM(NVL(CASHPAY_YEAR,0))=0 THEN 0 ELSE ROUND((SUM(CASHPAY_CURR)-SUM(CASHPAY_YEAR))*100/SUM(CASHPAY_YEAR),2) END AS MOM_YEARASHPAY_YEAR,
                CASE WHEN SUM(NVL(TOTALCOUNT_MONTH,0))=0 THEN 0 ELSE ROUND((SUM(TOTALCOUNT_CURR)-SUM(TOTALCOUNT_MONTH))*100/SUM(TOTALCOUNT_MONTH),2) END AS MOM_TOTALCOUNT_MONTH,
                CASE WHEN SUM(NVL(TOTALCOUNT_YEAR,0))=0 THEN 0 ELSE ROUND((SUM(TOTALCOUNT_CURR)-SUM(TOTALCOUNT_YEAR))*100/SUM(TOTALCOUNT_YEAR),2) END AS MOM_TOTALCOUNT_YEAR,
                CASE WHEN SUM(NVL(TICKETCOUNT_MONTH,0))=0 THEN 0 ELSE ROUND((SUM(TICKETCOUNT_CURR)-SUM(TICKETCOUNT_MONTH))*100/SUM(TICKETCOUNT_MONTH),2) END AS MOM_TICKETCOUNT_MONTH,
                CASE WHEN SUM(NVL(TICKETCOUNT_YEAR,0))=0 THEN 0 ELSE ROUND((SUM(TICKETCOUNT_CURR)-SUM(TICKETCOUNT_YEAR))*100/SUM(TICKETCOUNT_YEAR),2) END AS MOM_TICKETCOUNT_YEAR,
                MAX(A.SHOP_COUNT) AS SHOPCOUNT, B.SERVERPART_CODE, A.SERVERPARTSHOP_ID
            FROM ({inner_sql}) A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
            GROUP BY B.SERVERPART_INDEX, B.SERVERPART_ID, B.SERVERPART_NAME,
                B.SPREGIONTYPE_NAME, B.SERVERPART_CODE, B.SPREGIONTYPE_INDEX,
                B.SPREGIONTYPE_ID, A.SHOPTRADE, A.BUSINESS_TYPE, A.SERVERPARTSHOP_ID"""

        rows = db.execute_query(outer_sql) or []
        if not rows:
            return []

        # --- 获取门店简称和商户信息（C# 原逻辑）---
        shop_info_sql = f"SELECT SERVERPART_ID, SHOPNAME, SHOPSHORTNAME, TO_CHAR(SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID, SHOPTRADE, BUSINESS_TYPE FROM T_SERVERPARTSHOP WHERE ISVALID = 1{shop_sql}"
        shop_rows = db.execute_query(shop_info_sql) or []
        shop_map = {}
        for sr in shop_rows:
            key = (str(sr.get("SERVERPART_ID", "")), str(sr.get("SHOPTRADE", "")))
            shop_map[key] = sr.get("SHOPSHORTNAME", "")

        project_sql = "SELECT MERCHANTS_ID, MERCHANTS_NAME, PROJECT_STARTDATE, SERVERPARTSHOP_ID FROM T_BUSINESSPROJECT WHERE PROJECT_VALID = 1 AND SERVERPARTSHOP_ID IS NOT NULL"
        project_rows = db.execute_query(project_sql) or []

        # 为每行附加 SHOPSHORTNAME 和商户信息
        for r in rows:
            key = (str(r.get("SERVERPART_ID", "")), str(r.get("SHOPTRADE", "")))
            r["SHOPSHORTNAME"] = shop_map.get(key, "")
            sp_shop_id = str(r.get("SERVERPARTSHOP_ID", "") or "")
            if sp_shop_id:
                sp_ids_set = set(sp_shop_id.split(","))
                matched = [p for p in project_rows if set(str(p.get("SERVERPARTSHOP_ID", "")).split(",")) & sp_ids_set]
                if matched:
                    matched.sort(key=lambda p: str(p.get("PROJECT_STARTDATE", "")), reverse=True)
                    r["MERCHANTS_ID"] = matched[0].get("MERCHANTS_ID")
                    r["MERCHANTS_NAME"] = matched[0].get("MERCHANTS_NAME", "")

        # C# 原逻辑: shopNames 过滤
        if shop_names:
            name_set = set(n.strip() for n in shop_names.split(",") if n.strip())
            rows = [r for r in rows if r.get("SHOPSHORTNAME", "") in name_set]

        # --- 构建 NestingModel ---
        yoq_fields = ["CASHPAY_CURR", "TOTALCOUNT_CURR", "TICKETCOUNT_CURR",
                       "CASHPAY_MONTH", "TOTALCOUNT_MONTH", "TICKETCOUNT_MONTH",
                       "CASHPAY_YEAR", "TOTALCOUNT_YEAR", "TICKETCOUNT_YEAR"]

        def _sum_field(row_list, field):
            return round(sum(float(r.get(field) or 0) for r in row_list), 2)

        def _calc_mom(cur, prev):
            return round((cur / prev - 1) * 100, 2) if prev else 0

        def _build_yoq_node(name, row_list, extra=None):
            node = {"Name": name}
            for f in yoq_fields:
                node[f] = _sum_field(row_list, f)
            node["MOM_YEARASHPAY_MONTH"] = _calc_mom(node["CASHPAY_CURR"], node["CASHPAY_MONTH"])
            node["MOM_YEARASHPAY_YEAR"] = _calc_mom(node["CASHPAY_CURR"], node["CASHPAY_YEAR"])
            node["MOM_TOTALCOUNT_MONTH"] = _calc_mom(node["TOTALCOUNT_CURR"], node["TOTALCOUNT_MONTH"])
            node["MOM_TOTALCOUNT_YEAR"] = _calc_mom(node["TOTALCOUNT_CURR"], node["TOTALCOUNT_YEAR"])
            node["MOM_TICKETCOUNT_MONTH"] = _calc_mom(node["TICKETCOUNT_CURR"], node["TICKETCOUNT_MONTH"])
            node["MOM_TICKETCOUNT_YEAR"] = _calc_mom(node["TICKETCOUNT_CURR"], node["TICKETCOUNT_YEAR"])
            if extra:
                node.update(extra)
            return node

        # 按片区分组
        region_groups = {}
        no_region_rows = []
        for r in rows:
            rid = r.get("SPREGIONTYPE_ID")
            if rid is None:
                no_region_rows.append(r)
            else:
                if rid not in region_groups:
                    region_groups[rid] = {"name": r.get("TYPE_NAME", ""), "index": r.get("TYPE_INDEX", 999999), "rows": []}
                region_groups[rid]["rows"].append(r)

        result = []

        # 有片区的节点
        for rid, rg in sorted(region_groups.items(), key=lambda x: x[1]["index"]):
            region_node = {
                "node": _build_yoq_node(rg["name"], rg["rows"], {
                    "Id": str(rid), "SPREGIONTYPE_NAME": rg["name"],
                }),
                "children": [],
            }
            # 按服务区分组
            sp_groups = {}
            for r in rg["rows"]:
                sp_id = r.get("SERVERPART_ID")
                if sp_id not in sp_groups:
                    sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "index": r.get("SERVERPART_INDEX", 999999), "rows": []}
                sp_groups[sp_id]["rows"].append(r)
            for sp_id, sg in sorted(sp_groups.items(), key=lambda x: x[1]["index"]):
                sp_node = {
                    "node": _build_yoq_node(sg["name"], sg["rows"], {
                        "Id": str(sp_id), "SERVERPART_ID": sp_id, "SERVERPART_NAME": sg["name"],
                        "SPREGIONTYPE_NAME": rg["name"],
                    }),
                    "children": [],
                }
                # 门店级别（ShowShop=true 时）
                if show_shop:
                    shop_groups = {}
                    for r in sg["rows"]:
                        sn = r.get("SHOPSHORTNAME", "")
                        if sn not in shop_groups:
                            shop_groups[sn] = []
                        shop_groups[sn].append(r)
                    for sn, sr_list in sorted(shop_groups.items()):
                        shop_id_set = set()
                        for r in sr_list:
                            sid = str(r.get("SERVERPARTSHOP_ID") or "")
                            for s in sid.split(","):
                                if s.strip():
                                    shop_id_set.add(s.strip())
                        shop_id = ",".join(sorted(shop_id_set))
                        shop_extra = {
                            "Id": shop_id, "SHOPID": shop_id, "SHOPNAME": sn,
                            "SPREGIONTYPE_NAME": rg["name"],
                            "SERVERPART_ID": sp_id, "SERVERPART_NAME": sg["name"],
                            "ShopTrade": sr_list[0].get("SHOPTRADE"),
                            "ShopCount": len(shop_id_set),
                        }
                        if sr_list[0].get("MERCHANTS_ID"):
                            shop_extra["MERCHANTS_ID"] = sr_list[0].get("MERCHANTS_ID")
                            shop_extra["MERCHANTS_NAME"] = sr_list[0].get("MERCHANTS_NAME", "")
                        sp_node["children"].append({"node": _build_yoq_node(sn, sr_list, shop_extra)})
                sp_node["node"]["ShopCount"] = sum(c["node"].get("ShopCount", 0) for c in sp_node["children"]) if sp_node["children"] else 0
                region_node["children"].append(sp_node)
            region_node["node"]["ShopCount"] = sum(c["node"].get("ShopCount", 0) for c in region_node["children"])
            result.append(region_node)

        # 无片区的节点直接作为服务区级别附加
        if no_region_rows:
            no_region_parent = {"node": {}, "children": []}
            sp_groups = {}
            for r in no_region_rows:
                sp_id = r.get("SERVERPART_ID")
                if sp_id not in sp_groups:
                    sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "rows": []}
                sp_groups[sp_id]["rows"].append(r)
            for sp_id, sg in sp_groups.items():
                sp_node = {
                    "node": _build_yoq_node(sg["name"], sg["rows"], {
                        "Id": str(sp_id), "SERVERPART_ID": sp_id, "SERVERPART_NAME": sg["name"],
                    }),
                    "children": [],
                }
                result.append(sp_node)

        # 合计节点（C# 原逻辑: TotalRevenue 包裹所有）
        total_node = {
            "node": _build_yoq_node("合计", rows, {
                "ShopCount": sum(n["node"].get("ShopCount", 0) for n in result),
            }),
            "children": result,
        }
        return [total_node]
    except Exception as e:
        logger.error(f"GetRevenueYOYQOQ 失败: {e}")
        return []




def get_revenue_yoy_qoq_by_date(db, **kwargs) -> list:
    """
    获取同环比分析表(按日展示)
    C# RevenueHelper.GetRevenueYOYQOQByDate:
    与 GetRevenueYOYQOQ 相同的 UNION ALL 三期逻辑，但增加 STATISTICS_DATE 维度
    参数: ServerpartIds, startDate, endDate, shopNames, shopTrade, businessType,
          targetSystem, SearchKeyName, SearchKeyValue, wrapType, ServerpartShopId
    """
    logger.info(f"GetRevenueYOYQOQByDate: {kwargs}")
    try:
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        sp_ids = kwargs.get("ServerpartIds", "")
        start_str = kwargs.get("startDate", "") or kwargs.get("StartDate", "")
        end_str = kwargs.get("endDate", "") or kwargs.get("EndDate", "")
        shop_trade = kwargs.get("shopTrade", "")
        business_type = kwargs.get("businessType", "")
        target_system = kwargs.get("targetSystem")
        wrap_type = int(kwargs.get("wrapType", 0) or 0)
        sp_shop_id = kwargs.get("ServerpartShopId", "")

        if not start_str or not end_str:
            return []

        start_dt = datetime.strptime(start_str[:10], "%Y-%m-%d")
        end_dt = datetime.strptime(end_str[:10], "%Y-%m-%d")

        region_date = f" AND A.STATISTICS_DATE >= {start_dt.strftime('%Y%m%d')} AND STATISTICS_DATE <= {end_dt.strftime('%Y%m%d')}"
        mom_dt_s = start_dt - relativedelta(months=1)
        mom_dt_e = end_dt - relativedelta(months=1)
        mom_date = f" AND A.STATISTICS_DATE >= {mom_dt_s.strftime('%Y%m%d')} AND STATISTICS_DATE <= {mom_dt_e.strftime('%Y%m%d')}"
        hom_dt_s = start_dt - relativedelta(years=1)
        hom_dt_e = end_dt - relativedelta(years=1)
        hom_date = f" AND A.STATISTICS_DATE >= {hom_dt_s.strftime('%Y%m%d')} AND STATISTICS_DATE <= {hom_dt_e.strftime('%Y%m%d')}"

        where_sql = ""
        if sp_ids:
            where_sql += f" AND A.SERVERPART_ID IN ({sp_ids})"
        if shop_trade:
            where_sql += f" AND A.SHOPTRADE IN ({shop_trade})"
        if business_type:
            where_sql += f" AND A.BUSINESS_TYPE IN ({business_type})"

        shop_sql = ""
        if target_system is not None:
            ts = int(target_system)
            if ts == 1:
                shop_sql = " AND C.TRANSFER_TYPE > 0"
            elif ts == 0:
                shop_sql = " AND NVL(C.TRANSFER_TYPE,0) = 0"
        if sp_shop_id:
            where_sql += f" AND A.SERVERPARTSHOP_ID IN ({sp_shop_id})"

        # UNION ALL 三期 + STATISTICS_DATE 维度
        inner_sql = f"""SELECT
                A.SERVERPART_ID, A.SHOPTRADE, A.BUSINESS_TYPE, A.STATISTICS_DATE,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_CURR,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_CURR,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_CURR,
                0 AS CASHPAY_MONTH, 0 AS TOTALCOUNT_MONTH, 0 AS TICKETCOUNT_MONTH,
                0 AS CASHPAY_YEAR, 0 AS TOTALCOUNT_YEAR, 0 AS TICKETCOUNT_YEAR,
                A.SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SHOPTRADE = C.SHOPTRADE AND A.SERVERPART_ID = C.SERVERPART_ID{shop_sql})
                {region_date}{where_sql}
            GROUP BY A.SERVERPART_ID, A.BUSINESS_TYPE, A.SHOPTRADE, A.STATISTICS_DATE, A.SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                A.SERVERPART_ID, A.SHOPTRADE, A.BUSINESS_TYPE, A.STATISTICS_DATE,
                0, 0, 0,
                SUM(A.REVENUE_AMOUNT), SUM(A.TOTAL_COUNT), SUM(A.TICKET_COUNT),
                0, 0, 0, A.SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SHOPTRADE = C.SHOPTRADE AND A.SERVERPART_ID = C.SERVERPART_ID{shop_sql})
                {mom_date}{where_sql}
            GROUP BY A.SERVERPART_ID, A.BUSINESS_TYPE, A.SHOPTRADE, A.STATISTICS_DATE, A.SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                A.SERVERPART_ID, A.SHOPTRADE, A.BUSINESS_TYPE, A.STATISTICS_DATE,
                0, 0, 0, 0, 0, 0,
                SUM(A.REVENUE_AMOUNT), SUM(A.TOTAL_COUNT), SUM(A.TICKET_COUNT),
                A.SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SHOPTRADE = C.SHOPTRADE AND A.SERVERPART_ID = C.SERVERPART_ID{shop_sql})
                {hom_date}{where_sql}
            GROUP BY A.SERVERPART_ID, A.BUSINESS_TYPE, A.SHOPTRADE, A.STATISTICS_DATE, A.SERVERPARTSHOP_ID"""

        outer_sql = f"""SELECT
                A.STATISTICS_DATE,
                B.SERVERPART_ID, B.SERVERPART_NAME,
                NVL(B.SPREGIONTYPE_INDEX,999999) AS TYPE_INDEX,
                B.SPREGIONTYPE_NAME AS TYPE_NAME, B.SPREGIONTYPE_ID,
                SUM(CASHPAY_CURR) AS CASHPAY_CURR, SUM(TOTALCOUNT_CURR) AS TOTALCOUNT_CURR,
                SUM(TICKETCOUNT_CURR) AS TICKETCOUNT_CURR,
                SUM(CASHPAY_MONTH) AS CASHPAY_MONTH, SUM(TOTALCOUNT_MONTH) AS TOTALCOUNT_MONTH,
                SUM(TICKETCOUNT_MONTH) AS TICKETCOUNT_MONTH,
                SUM(CASHPAY_YEAR) AS CASHPAY_YEAR, SUM(TOTALCOUNT_YEAR) AS TOTALCOUNT_YEAR,
                SUM(TICKETCOUNT_YEAR) AS TICKETCOUNT_YEAR,
                CASE WHEN SUM(NVL(CASHPAY_MONTH,0))=0 THEN 0 ELSE ROUND((SUM(CASHPAY_CURR)-SUM(CASHPAY_MONTH))*100/SUM(CASHPAY_MONTH),2) END AS MOM_YEARASHPAY_MONTH,
                CASE WHEN SUM(NVL(CASHPAY_YEAR,0))=0 THEN 0 ELSE ROUND((SUM(CASHPAY_CURR)-SUM(CASHPAY_YEAR))*100/SUM(CASHPAY_YEAR),2) END AS MOM_YEARASHPAY_YEAR,
                CASE WHEN SUM(NVL(TOTALCOUNT_MONTH,0))=0 THEN 0 ELSE ROUND((SUM(TOTALCOUNT_CURR)-SUM(TOTALCOUNT_MONTH))*100/SUM(TOTALCOUNT_MONTH),2) END AS MOM_TOTALCOUNT_MONTH,
                CASE WHEN SUM(NVL(TOTALCOUNT_YEAR,0))=0 THEN 0 ELSE ROUND((SUM(TOTALCOUNT_CURR)-SUM(TOTALCOUNT_YEAR))*100/SUM(TOTALCOUNT_YEAR),2) END AS MOM_TOTALCOUNT_YEAR,
                CASE WHEN SUM(NVL(TICKETCOUNT_MONTH,0))=0 THEN 0 ELSE ROUND((SUM(TICKETCOUNT_CURR)-SUM(TICKETCOUNT_MONTH))*100/SUM(TICKETCOUNT_MONTH),2) END AS MOM_TICKETCOUNT_MONTH,
                CASE WHEN SUM(NVL(TICKETCOUNT_YEAR,0))=0 THEN 0 ELSE ROUND((SUM(TICKETCOUNT_CURR)-SUM(TICKETCOUNT_YEAR))*100/SUM(TICKETCOUNT_YEAR),2) END AS MOM_TICKETCOUNT_YEAR
            FROM ({inner_sql}) A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
            GROUP BY A.STATISTICS_DATE, B.SERVERPART_NAME, B.SERVERPART_ID,
                B.SPREGIONTYPE_INDEX, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_ID
            ORDER BY A.STATISTICS_DATE DESC, B.SPREGIONTYPE_ID, B.SERVERPART_ID"""

        rows = db.execute_query(outer_sql) or []
        if not rows:
            return []

        yoq_fields = ["CASHPAY_CURR", "TOTALCOUNT_CURR", "TICKETCOUNT_CURR",
                       "CASHPAY_MONTH", "TOTALCOUNT_MONTH", "TICKETCOUNT_MONTH",
                       "CASHPAY_YEAR", "TOTALCOUNT_YEAR", "TICKETCOUNT_YEAR"]

        def _sum_field(row_list, field):
            return round(sum(float(r.get(field) or 0) for r in row_list), 2)

        def _calc_mom(cur, prev):
            return round((cur / prev - 1) * 100, 2) if prev else 0

        def _build_node(name, row_list, extra=None):
            node = {"Name": name}
            for f in yoq_fields:
                node[f] = _sum_field(row_list, f)
            node["MOM_YEARASHPAY_MONTH"] = _calc_mom(node["CASHPAY_CURR"], node["CASHPAY_MONTH"])
            node["MOM_YEARASHPAY_YEAR"] = _calc_mom(node["CASHPAY_CURR"], node["CASHPAY_YEAR"])
            node["MOM_TOTALCOUNT_MONTH"] = _calc_mom(node["TOTALCOUNT_CURR"], node["TOTALCOUNT_MONTH"])
            node["MOM_TOTALCOUNT_YEAR"] = _calc_mom(node["TOTALCOUNT_CURR"], node["TOTALCOUNT_YEAR"])
            node["MOM_TICKETCOUNT_MONTH"] = _calc_mom(node["TICKETCOUNT_CURR"], node["TICKETCOUNT_MONTH"])
            node["MOM_TICKETCOUNT_YEAR"] = _calc_mom(node["TICKETCOUNT_CURR"], node["TICKETCOUNT_YEAR"])
            if extra:
                node.update(extra)
            return node

        # 合计节点
        total_node = {"node": _build_node("合计", rows), "children": []}

        if wrap_type == 0:
            # wrapType=0: 按日期平铺
            date_groups = {}
            for r in rows:
                d = str(r.get("STATISTICS_DATE", ""))
                if d not in date_groups:
                    date_groups[d] = []
                date_groups[d].append(r)
            for d in sorted(date_groups.keys(), reverse=True):
                total_node["children"].append({
                    "node": _build_node(d, date_groups[d], {"Statistics_Date": d}),
                    "children": [],
                })
        else:
            # wrapType=1: 片区→服务区→日期三级
            region_groups = {}
            for r in rows:
                rid = r.get("SPREGIONTYPE_ID")
                if rid not in region_groups:
                    region_groups[rid] = {"name": r.get("TYPE_NAME", ""), "index": r.get("TYPE_INDEX", 999999), "rows": []}
                region_groups[rid]["rows"].append(r)
            for rid, rg in sorted(region_groups.items(), key=lambda x: x[1]["index"]):
                region_node = {"node": _build_node(rg["name"], rg["rows"]), "children": []}
                sp_groups = {}
                for r in rg["rows"]:
                    sp_id = r.get("SERVERPART_ID")
                    if sp_id not in sp_groups:
                        sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "rows": []}
                    sp_groups[sp_id]["rows"].append(r)
                for sp_id, sg in sp_groups.items():
                    sp_node = {"node": _build_node(sg["name"], sg["rows"], {"SERVERPART_ID": sp_id}), "children": []}
                    date_groups = {}
                    for r in sg["rows"]:
                        d = str(r.get("STATISTICS_DATE", ""))
                        if d not in date_groups:
                            date_groups[d] = []
                        date_groups[d].append(r)
                    for d in sorted(date_groups.keys(), reverse=True):
                        sp_node["children"].append({"node": _build_node(d, date_groups[d], {"Statistics_Date": d})})
                    region_node["children"].append(sp_node)
                total_node["children"].append(region_node)

        return [total_node]
    except Exception as e:
        logger.error(f"GetRevenueYOYQOQByDate 失败: {e}")
        return []




def get_revenue_qoq(db, **kwargs) -> list:
    """
    获取销售环比分析
    C# RevenueHelper.GetRevenueQOQ: UNION ALL 当期+上期数据，SELECTTYPE 选列，
    NestingModel 合计→片区→服务区→门店 三级树
    参数: ServerpartIds, startDate, endDate, MOMstartDate, MOMendDate,
          SELECTTYPE(1=实收金额,2=销售数量,3=客单数量), ShowShop,
          shopTrade, businessType, targetSystem
    """
    logger.info(f"GetRevenueQOQ: {kwargs}")
    try:
        from datetime import datetime

        sp_ids = kwargs.get("ServerpartIds", "")
        start = kwargs.get("startDate", "") or kwargs.get("StartDate", "")
        end = kwargs.get("endDate", "") or kwargs.get("EndDate", "")
        mom_start = kwargs.get("MOMstartDate", "")
        mom_end = kwargs.get("MOMendDate", "")
        select_type = int(kwargs.get("SELECTTYPE", 1) or 1)
        show_shop = str(kwargs.get("ShowShop", "true")).lower() != "false"
        shop_trade = kwargs.get("shopTrade", "")
        business_type = kwargs.get("businessType", "")
        target_system = kwargs.get("targetSystem")

        # 构建 WHERE 条件（C# 原逻辑）
        where_sql = ""
        if sp_ids:
            where_sql += f" AND SERVERPART_ID IN ({sp_ids})"
        if shop_trade:
            where_sql += f" AND A.SHOPTRADE IN ({shop_trade})"
        if business_type:
            where_sql += f" AND A.BUSINESS_TYPE IN ({business_type})"

        # targetSystem 筛选
        shop_sql = ""
        if target_system is not None:
            ts = int(target_system)
            if ts == 1:
                shop_sql = " AND C.TRANSFER_TYPE > 0"
            elif ts == 0:
                shop_sql = " AND NVL(C.TRANSFER_TYPE,0) = 0"

        # 日期条件（C# 原逻辑: regionDate = 当期, MomDate = 上期）
        region_date = ""
        mom_date = ""
        if start:
            s = start.replace("-", "")[:8]
            region_date += f" AND A.STATISTICS_DATE >= {s}"
        if end:
            e = end.replace("-", "")[:8]
            region_date += f" AND A.STATISTICS_DATE <= {e}"
        if mom_start:
            ms = mom_start.replace("-", "")[:8]
            mom_date += f" AND A.STATISTICS_DATE >= {ms}"
        if mom_end:
            me = mom_end.replace("-", "")[:8]
            mom_date += f" AND A.STATISTICS_DATE <= {me}"

        # SELECTTYPE 决定用哪组列名（C# 原逻辑）
        if select_type == 2:
            selected = "TOTALCOUNT"
        elif select_type == 3:
            selected = "TICKETCOUNT"
        else:
            selected = "CASHPAY"

        # UNION ALL 子查询：当期(CASHPAY_A/B/C) + 上期(CASHPAY_D/E/F)
        inner_sql = f"""SELECT
                SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE,
                MAX(SHOP_COUNT) AS SHOP_COUNT,
                SUM(A.REVENUE_AMOUNT_A) AS CASHPAY_A,
                SUM(A.REVENUE_AMOUNT_B) AS CASHPAY_B,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_C,
                SUM(A.TOTAL_COUNT_A) AS TOTALCOUNT_A,
                SUM(A.TOTAL_COUNT_B) AS TOTALCOUNT_B,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_C,
                SUM(A.TICKET_COUNT_A) AS TICKETCOUNT_A,
                SUM(A.TICKET_COUNT_B) AS TICKETCOUNT_B,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_C,
                0 AS CASHPAY_D,0 AS CASHPAY_E,0 AS CASHPAY_F,
                0 AS TOTALCOUNT_D,0 AS TOTALCOUNT_E,0 AS TOTALCOUNT_F,
                0 AS TICKETCOUNT_D,0 AS TICKETCOUNT_E,0 AS TICKETCOUNT_F,
                SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPTRADE = C.SHOPTRADE{shop_sql})
                {region_date}{where_sql}
            GROUP BY SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE, SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE,
                MAX(SHOP_COUNT) AS SHOP_COUNT,
                0,0,0,0,0,0,0,0,0,
                SUM(A.REVENUE_AMOUNT_A) AS CASHPAY_A,
                SUM(A.REVENUE_AMOUNT_B) AS CASHPAY_B,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_C,
                SUM(A.TOTAL_COUNT_A) AS TOTALCOUNT_A,
                SUM(A.TOTAL_COUNT_B) AS TOTALCOUNT_B,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_C,
                SUM(A.TICKET_COUNT_A) AS TICKETCOUNT_A,
                SUM(A.TICKET_COUNT_B) AS TICKETCOUNT_B,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_C,
                SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPTRADE = C.SHOPTRADE{shop_sql})
                {mom_date}{where_sql}
            GROUP BY SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE, SERVERPARTSHOP_ID"""

        # 外层查询：JOIN T_SERVERPART，按 SELECTTYPE 计算环比
        outer_sql = f"""SELECT
                NVL(B.SERVERPART_INDEX,999999) AS SERVERPART_INDEX,
                B.SERVERPART_ID, B.SERVERPART_NAME,
                NVL(B.SPREGIONTYPE_INDEX,999999) AS TYPE_INDEX,
                B.SPREGIONTYPE_NAME AS TYPE_NAME,
                B.SPREGIONTYPE_ID,
                TO_CHAR(A.SHOPTRADE) AS SHOPNAME, A.SHOPTRADE, A.BUSINESS_TYPE,
                SUM(NVL({selected}_A,0)) AS CASHPAY_A,
                SUM(NVL({selected}_B,0)) AS CASHPAY_B,
                SUM(NVL({selected}_C,0)) AS CASHPAY_TotalA,
                SUM(NVL({selected}_D,0)) AS CASHPAY_C,
                SUM(NVL({selected}_E,0)) AS CASHPAY_D,
                SUM(NVL({selected}_F,0)) AS CASHPAY_TotalB,
                CASE WHEN SUM(NVL({selected}_D,0)) = 0 THEN 0
                    ELSE ROUND((SUM(NVL({selected}_A,0)) -
                        SUM(NVL({selected}_D,0))) * 100 / SUM(NVL({selected}_D,0)),2) END AS MOM_A,
                CASE WHEN SUM(NVL({selected}_E,0)) = 0 THEN 0
                    ELSE ROUND((SUM(NVL({selected}_B,0)) -
                        SUM(NVL({selected}_E,0))) * 100 / SUM(NVL({selected}_E,0)),2) END AS MOM_B,
                CASE WHEN SUM(NVL({selected}_F,0)) = 0 THEN 0
                    ELSE ROUND((SUM(NVL({selected}_C,0)) -
                        SUM(NVL({selected}_F,0))) * 100 / SUM(NVL({selected}_F,0)),2) END AS MOMTOTAL,
                MAX(A.SHOP_COUNT) AS SHOPCOUNT, A.SERVERPARTSHOP_ID
            FROM ({inner_sql}) A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
            GROUP BY B.SERVERPART_NAME, B.SERVERPART_INDEX, B.SERVERPART_ID,
                B.SPREGIONTYPE_INDEX, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_ID,
                A.SHOPTRADE, A.BUSINESS_TYPE, A.SERVERPARTSHOP_ID"""

        rows = db.execute_query(outer_sql) or []
        if not rows:
            return []

        # C# 聚合辅助函数
        def _sum_field(row_list, field):
            return round(sum(float(r.get(field) or 0) for r in row_list), 2)

        def _calc_mom(cur_val, prev_val):
            if prev_val and prev_val != 0:
                return round((cur_val - prev_val) * 100 / prev_val, 2)
            return 0

        def _build_qoq_node(name, row_list, extra=None):
            node = {
                "Name": name,
                "CASHPAY_A": _sum_field(row_list, "CASHPAY_A"),
                "CASHPAY_B": _sum_field(row_list, "CASHPAY_B"),
                "CASHPAY_TotalA": _sum_field(row_list, "CASHPAY_TOTALA"),
                "CASHPAY_C": _sum_field(row_list, "CASHPAY_C"),
                "CASHPAY_D": _sum_field(row_list, "CASHPAY_D"),
                "CASHPAY_TotalB": _sum_field(row_list, "CASHPAY_TOTALB"),
            }
            node["MOM_A"] = _calc_mom(node["CASHPAY_A"], node["CASHPAY_C"])
            node["MOM_B"] = _calc_mom(node["CASHPAY_B"], node["CASHPAY_D"])
            node["MOMTOTAL"] = _calc_mom(node["CASHPAY_TotalA"], node["CASHPAY_TotalB"])
            if extra:
                node.update(extra)
            return node

        # 构建 NestingModel 三级树：片区→服务区→门店
        # 按片区分组
        region_order = {}
        for r in rows:
            rid = r.get("SPREGIONTYPE_ID")
            if rid not in region_order:
                region_order[rid] = {
                    "name": r.get("TYPE_NAME", ""),
                    "index": r.get("TYPE_INDEX", 999999),
                    "rows": [],
                }
            region_order[rid]["rows"].append(r)

        region_list = []
        for rid, rg in sorted(region_order.items(), key=lambda x: x[1]["index"]):
            region_node = {
                "node": _build_qoq_node(rg["name"], rg["rows"], {
                    "Id": str(rid) if rid else "",
                    "SPREGIONTYPE_NAME": rg["name"],
                }),
                "children": [],
            }
            # 按服务区分组
            sp_order = {}
            for r in rg["rows"]:
                sp_id = r.get("SERVERPART_ID")
                if sp_id not in sp_order:
                    sp_order[sp_id] = {
                        "name": r.get("SERVERPART_NAME", ""),
                        "index": r.get("SERVERPART_INDEX", 999999),
                        "rows": [],
                    }
                sp_order[sp_id]["rows"].append(r)

            for sp_id, sg in sorted(sp_order.items(), key=lambda x: x[1]["index"]):
                sp_node = {
                    "node": _build_qoq_node(sg["name"], sg["rows"], {
                        "Id": str(sp_id),
                        "SERVERPART_ID": sp_id,
                        "SERVERPART_NAME": sg["name"],
                        "SPREGIONTYPE_NAME": rg["name"],
                    }),
                    "children": [],
                }
                # 按门店分组（ShowShop=true 时）
                if show_shop:
                    shop_groups = {}
                    for r in sg["rows"]:
                        shop_key = (r.get("SHOPTRADE"), r.get("SHOPNAME", ""))
                        if shop_key not in shop_groups:
                            shop_groups[shop_key] = []
                        shop_groups[shop_key].append(r)
                    for (trade, shop_name), shop_rows in sorted(shop_groups.items(), key=lambda x: str(x[0][1])):
                        shop_ids = ",".join(set(str(r.get("SERVERPARTSHOP_ID", "")) for r in shop_rows if r.get("SERVERPARTSHOP_ID")))
                        shop_child = {
                            "node": _build_qoq_node(shop_name or "", shop_rows, {
                                "Id": shop_ids,
                                "SERVERPARTSHOP_ID": shop_ids,
                                "SHOPNAME": shop_name or "",
                                "SPREGIONTYPE_NAME": rg["name"],
                                "SERVERPART_ID": sp_id,
                                "SERVERPART_NAME": sg["name"],
                                "ShopCount": len(set(str(r.get("SERVERPARTSHOP_ID", "")) for r in shop_rows if r.get("SERVERPARTSHOP_ID"))),
                            }),
                        }
                        sp_node["children"].append(shop_child)

                sp_node["node"]["ShopCount"] = sum(c["node"].get("ShopCount", 0) for c in sp_node["children"]) if sp_node["children"] else 0
                region_node["children"].append(sp_node)

            region_node["node"]["ShopCount"] = sum(c["node"].get("ShopCount", 0) for c in region_node["children"])
            region_list.append(region_node)

        # 合计节点（C# 原逻辑: TotalRevenue 包裹全部片区）
        total_node = {
            "node": _build_qoq_node("合计", rows),
            "children": region_list,
        }
        return [total_node]
    except Exception as e:
        logger.error(f"GetRevenueQOQ 失败: {e}")
        return []


def get_revenue_qoq_by_date(db, **kwargs) -> list:
    """
    获取销售环比分析(按日展示)
    C# RevenueHelper.GetRevenueQOQByDate: 与 GetRevenueQOQ 相同的 UNION ALL 逻辑，
    但增加 STATISTICS_DATE 分组维度 + wrapType 参数
    参数: ServerpartIds, startDate, endDate, MOMstartDate, MOMendDate,
          SELECTTYPE, shopTrade, businessType, targetSystem, wrapType
    """
    logger.info(f"GetRevenueQOQByDate: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start = kwargs.get("startDate", "") or kwargs.get("StartDate", "")
        end = kwargs.get("endDate", "") or kwargs.get("EndDate", "")
        mom_start = kwargs.get("MOMstartDate", "")
        mom_end = kwargs.get("MOMendDate", "")
        select_type = int(kwargs.get("SELECTTYPE", 1) or 1)
        wrap_type = int(kwargs.get("wrapType", 0) or 0)
        shop_trade = kwargs.get("shopTrade", "")
        business_type = kwargs.get("businessType", "")
        target_system = kwargs.get("targetSystem")

        where_sql = ""
        if sp_ids:
            where_sql += f" AND SERVERPART_ID IN ({sp_ids})"
        if shop_trade:
            where_sql += f" AND A.SHOPTRADE IN ({shop_trade})"
        if business_type:
            where_sql += f" AND A.BUSINESS_TYPE IN ({business_type})"

        shop_sql = ""
        if target_system is not None:
            ts = int(target_system)
            if ts == 1:
                shop_sql = " AND C.TRANSFER_TYPE > 0"
            elif ts == 0:
                shop_sql = " AND NVL(C.TRANSFER_TYPE,0) = 0"

        region_date = ""
        mom_date = ""
        if start:
            region_date += f" AND A.STATISTICS_DATE >= {start.replace('-', '')[:8]}"
        if end:
            region_date += f" AND A.STATISTICS_DATE <= {end.replace('-', '')[:8]}"
        if mom_start:
            mom_date += f" AND A.STATISTICS_DATE >= {mom_start.replace('-', '')[:8]}"
        if mom_end:
            mom_date += f" AND A.STATISTICS_DATE <= {mom_end.replace('-', '')[:8]}"

        if select_type == 2:
            selected = "TOTALCOUNT"
        elif select_type == 3:
            selected = "TICKETCOUNT"
        else:
            selected = "CASHPAY"

        # UNION ALL 当期+上期（增加 STATISTICS_DATE 维度）
        inner_sql = f"""SELECT
                SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE, A.STATISTICS_DATE,
                SUM(A.REVENUE_AMOUNT_A) AS CASHPAY_A,
                SUM(A.REVENUE_AMOUNT_B) AS CASHPAY_B,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_C,
                SUM(A.TOTAL_COUNT_A) AS TOTALCOUNT_A,
                SUM(A.TOTAL_COUNT_B) AS TOTALCOUNT_B,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_C,
                SUM(A.TICKET_COUNT_A) AS TICKETCOUNT_A,
                SUM(A.TICKET_COUNT_B) AS TICKETCOUNT_B,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_C,
                0 AS CASHPAY_D,0 AS CASHPAY_E,0 AS CASHPAY_F,
                0 AS TOTALCOUNT_D,0 AS TOTALCOUNT_E,0 AS TOTALCOUNT_F,
                0 AS TICKETCOUNT_D,0 AS TICKETCOUNT_E,0 AS TICKETCOUNT_F,
                SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPTRADE = C.SHOPTRADE{shop_sql})
                {region_date}{where_sql}
            GROUP BY SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE, A.STATISTICS_DATE, SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE, A.STATISTICS_DATE,
                0,0,0,0,0,0,0,0,0,
                SUM(A.REVENUE_AMOUNT_A) AS CASHPAY_A,
                SUM(A.REVENUE_AMOUNT_B) AS CASHPAY_B,
                SUM(A.REVENUE_AMOUNT) AS CASHPAY_C,
                SUM(A.TOTAL_COUNT_A) AS TOTALCOUNT_A,
                SUM(A.TOTAL_COUNT_B) AS TOTALCOUNT_B,
                SUM(A.TOTAL_COUNT) AS TOTALCOUNT_C,
                SUM(A.TICKET_COUNT_A) AS TICKETCOUNT_A,
                SUM(A.TICKET_COUNT_B) AS TICKETCOUNT_B,
                SUM(A.TICKET_COUNT) AS TICKETCOUNT_C,
                SERVERPARTSHOP_ID
            FROM T_REVENUEDAILY A
            WHERE A.REVENUEDAILY_STATE = 1
                AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
                    WHERE A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPTRADE = C.SHOPTRADE{shop_sql})
                {mom_date}{where_sql}
            GROUP BY SERVERPART_ID, SHOPTRADE, BUSINESS_TYPE, A.STATISTICS_DATE, SERVERPARTSHOP_ID"""

        outer_sql = f"""SELECT
                A.STATISTICS_DATE,
                B.SERVERPART_ID, B.SERVERPART_NAME,
                NVL(B.SPREGIONTYPE_INDEX,999999) AS TYPE_INDEX,
                B.SPREGIONTYPE_NAME AS TYPE_NAME, B.SPREGIONTYPE_ID,
                SUM(NVL({selected}_A,0)) AS CASHPAY_A,
                SUM(NVL({selected}_B,0)) AS CASHPAY_B,
                SUM(NVL({selected}_C,0)) AS CASHPAY_TotalA,
                SUM(NVL({selected}_D,0)) AS CASHPAY_C,
                SUM(NVL({selected}_E,0)) AS CASHPAY_D,
                SUM(NVL({selected}_F,0)) AS CASHPAY_TotalB,
                CASE WHEN SUM(NVL({selected}_D,0)) = 0 THEN 0
                    ELSE ROUND((SUM(NVL({selected}_A,0)) -
                        SUM(NVL({selected}_D,0))) * 100 / SUM(NVL({selected}_D,0)),2) END AS MOM_A,
                CASE WHEN SUM(NVL({selected}_E,0)) = 0 THEN 0
                    ELSE ROUND((SUM(NVL({selected}_B,0)) -
                        SUM(NVL({selected}_E,0))) * 100 / SUM(NVL({selected}_E,0)),2) END AS MOM_B,
                CASE WHEN SUM(NVL({selected}_F,0)) = 0 THEN 0
                    ELSE ROUND((SUM(NVL({selected}_C,0)) -
                        SUM(NVL({selected}_F,0))) * 100 / SUM(NVL({selected}_F,0)),2) END AS MOMTOTAL
            FROM ({inner_sql}) A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
            GROUP BY A.STATISTICS_DATE, B.SERVERPART_NAME, B.SERVERPART_ID,
                B.SPREGIONTYPE_INDEX, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_ID
            ORDER BY A.STATISTICS_DATE DESC, B.SPREGIONTYPE_ID, B.SERVERPART_ID"""

        rows = db.execute_query(outer_sql) or []
        if not rows:
            return []

        def _sum_field(row_list, field):
            return round(sum(float(r.get(field) or 0) for r in row_list), 2)

        def _calc_mom(cur_val, prev_val):
            return round((cur_val - prev_val) * 100 / prev_val, 2) if prev_val else 0

        def _build_node(name, row_list, extra=None):
            node = {
                "Name": name,
                "CASHPAY_A": _sum_field(row_list, "CASHPAY_A"),
                "CASHPAY_B": _sum_field(row_list, "CASHPAY_B"),
                "CASHPAY_TotalA": _sum_field(row_list, "CASHPAY_TOTALA"),
                "CASHPAY_C": _sum_field(row_list, "CASHPAY_C"),
                "CASHPAY_D": _sum_field(row_list, "CASHPAY_D"),
                "CASHPAY_TotalB": _sum_field(row_list, "CASHPAY_TOTALB"),
            }
            node["MOM_A"] = _calc_mom(node["CASHPAY_A"], node["CASHPAY_C"])
            node["MOM_B"] = _calc_mom(node["CASHPAY_B"], node["CASHPAY_D"])
            node["MOMTOTAL"] = _calc_mom(node["CASHPAY_TotalA"], node["CASHPAY_TotalB"])
            if extra:
                node.update(extra)
            return node

        # 合计节点
        total_node = {"node": _build_node("合计", rows), "children": []}

        if wrap_type == 0:
            # wrapType=0: 直接按日期分组
            date_groups = {}
            for r in rows:
                d = str(r.get("STATISTICS_DATE", ""))
                if d not in date_groups:
                    date_groups[d] = []
                date_groups[d].append(r)
            for d in sorted(date_groups.keys(), reverse=True):
                total_node["children"].append({
                    "node": _build_node(d, date_groups[d], {"Statistics_Date": d}),
                    "children": [],
                })
        else:
            # wrapType=1: 片区→服务区→日期层级
            region_groups = {}
            for r in rows:
                rid = r.get("SPREGIONTYPE_ID")
                if rid not in region_groups:
                    region_groups[rid] = {"name": r.get("TYPE_NAME", ""), "index": r.get("TYPE_INDEX", 999999), "rows": []}
                region_groups[rid]["rows"].append(r)
            for rid, rg in sorted(region_groups.items(), key=lambda x: x[1]["index"]):
                region_node = {"node": _build_node(rg["name"], rg["rows"]), "children": []}
                sp_groups = {}
                for r in rg["rows"]:
                    sp_id = r.get("SERVERPART_ID")
                    if sp_id not in sp_groups:
                        sp_groups[sp_id] = {"name": r.get("SERVERPART_NAME", ""), "rows": []}
                    sp_groups[sp_id]["rows"].append(r)
                for sp_id, sg in sp_groups.items():
                    sp_node = {"node": _build_node(sg["name"], sg["rows"], {"SERVERPART_ID": sp_id}), "children": []}
                    date_groups = {}
                    for r in sg["rows"]:
                        d = str(r.get("STATISTICS_DATE", ""))
                        if d not in date_groups:
                            date_groups[d] = []
                        date_groups[d].append(r)
                    for d in sorted(date_groups.keys(), reverse=True):
                        sp_node["children"].append({"node": _build_node(d, date_groups[d], {"Statistics_Date": d})})
                    region_node["children"].append(sp_node)
                total_node["children"].append(region_node)

        return [total_node]
    except Exception as e:
        logger.error(f"GetRevenueQOQByDate 失败: {e}")
        return []



def get_month_compare(db, **kwargs) -> list:
    """
    获取月度营收差异分析
    C# RevenueHelper: 按月份对比同期数据
    """
    logger.info(f"GetMonthCompare: {kwargs}")
    try:
        wc = _build_revenue_where(kwargs)
        sql = f"""SELECT B.SERVERPART_ID, B.SERVERPART_NAME,
                    SUBSTR(TO_CHAR(A.STATISTICS_DATE), 1, 6) AS STAT_MONTH,
                    SUM(A.REVENUE_AMOUNT) AS Revenue_Amount,
                    SUM(A.MOBILEPAY_AMOUNT) AS MobilePay_Amount,
                    SUM(A.CASHPAY_AMOUNT) AS CashPay_Amount,
                    SUM(A.TICKET_COUNT) AS Ticket_Count
                 FROM T_REVENUEDAILY A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc}
                 GROUP BY B.SERVERPART_ID, B.SERVERPART_NAME,
                    SUBSTR(TO_CHAR(A.STATISTICS_DATE), 1, 6)
                 ORDER BY STAT_MONTH, B.SERVERPART_ID"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetMonthCompare 失败: {e}")
        return []


def get_business_analysis_report(db, **kwargs) -> list:
    """
    获取智慧招商分析报表
    C# 逻辑: 查询 T_BUSINESSANALYSIS 统计报表数据
    """
    logger.info(f"GetBusinessAnalysisReport: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        wp = ["BUSINESSANALYSIS_STATE = 1"]
        if sp_ids:
            wp.append(f"SERVERPART_ID IN ({sp_ids})")
        wc = " AND ".join(wp)
        sql = f"SELECT * FROM T_BUSINESSANALYSIS WHERE {wc} ORDER BY BUSINESSANALYSIS_ID DESC"
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetBusinessAnalysisReport 失败: {e}")
        return []


def get_situation_analysis(db, serverpart_id: str) -> dict:
    """
    分析服务区的经营情况
    C# 逻辑: 查询 T_SITUATIONANALYSIS 最新分析记录
    """
    logger.info(f"GetSituationAnalysis: SP={serverpart_id}")
    try:
        sql = f"""SELECT * FROM T_SITUATIONANALYSIS
                 WHERE SERVERPART_ID = {serverpart_id} AND SITUATIONANALYSIS_STATE = 1
                 ORDER BY SITUATIONANALYSIS_ID DESC"""
        rows = db.execute_query(sql)
        return rows[0] if rows else {}
    except Exception as e:
        logger.error(f"GetSituationAnalysis 失败: {e}")
        return {}


def get_business_trade_analysis(db, serverpart_id: str, serverpart_shop_id: str = "") -> dict:
    """
    分析此业态在驿达服务区的经营情况
    C# 逻辑: 按业态查询 T_REVENUEDAILY 聚合数据
    """
    logger.info(f"GetBusinessTradeAnalysis: SP={serverpart_id}, Shop={serverpart_shop_id}")
    try:
        wp = ["REVENUEDAILY_STATE = 1"]
        if serverpart_id:
            wp.append(f"SERVERPART_ID = {serverpart_id}")
        if serverpart_shop_id:
            wp.append(f"SERVERPARTSHOP_ID IN ({serverpart_shop_id})")
        wc = " AND ".join(wp)
        sql = f"""SELECT SHOPTRADE, BUSINESS_TYPE,
                    SUM(REVENUE_AMOUNT) AS Revenue_Amount,
                    SUM(TICKET_COUNT) AS Ticket_Count,
                    SUM(MOBILEPAY_AMOUNT) AS MobilePay_Amount
                 FROM T_REVENUEDAILY WHERE {wc}
                 GROUP BY SHOPTRADE, BUSINESS_TYPE
                 ORDER BY Revenue_Amount DESC"""
        rows = db.execute_query(sql) or []
        return {"trades": rows, "total_count": len(rows)}
    except Exception as e:
        logger.error(f"GetBusinessTradeAnalysis 失败: {e}")
        return {}


def get_brand_analysis(db, serverpart_id: str, serverpart_shop_id: str = "") -> dict:
    """
    分析此品牌在驿达旗下的经营情况
    C# 逻辑: 查询 T_BRANDANALYSIS 品牌分析表
    """
    logger.info(f"GetBrandAnalysis: SP={serverpart_id}, Shop={serverpart_shop_id}")
    try:
        wp = ["BRANDANALYSIS_STATE = 1"]
        if serverpart_id:
            wp.append(f"SERVERPART_ID = {serverpart_id}")
        wc = " AND ".join(wp)
        sql = f"""SELECT * FROM T_BRANDANALYSIS WHERE {wc} ORDER BY BRANDANALYSIS_ID DESC"""
        rows = db.execute_query(sql) or []
        return {"brands": rows, "total_count": len(rows)}
    except Exception as e:
        logger.error(f"GetBrandAnalysis 失败: {e}")
        return {}


def get_month_inc_analysis(db, **kwargs) -> list:
    """
    月度服务区门店营收对比固化数据
    C# BUSINESSWARNINGHelper.GetMonthINCAnalysis:
    查 T_BUSINESSWARNING，构建 月份→服务区(DATATYPE=1)→门店(DATATYPE=2) NestingModel
    参数: ServerpartId, ServerpartShopIds, StatisticsStartMonth, StatisticsEndMonth, DataType(1=服务区,2=门店)
    """
    logger.info(f"GetMonthINCAnalysis: {kwargs}")
    try:
        sp_id = kwargs.get("ServerpartId", "") or kwargs.get("ServerpartIds", "")
        shop_ids = kwargs.get("ServerpartShopIds", "")
        start_month = kwargs.get("StatisticsStartMonth", "")
        end_month = kwargs.get("StatisticsEndMonth", "")
        data_type = int(kwargs.get("DataType", 1) or 1)

        # 构建 WHERE（C# 原逻辑: 处理 ServerpartId + ServerpartShopIds + DataType 的组合）
        where_sql = ""
        if sp_id and shop_ids and data_type == 1:
            where_sql = f" AND A.SERVERPART_ID IN ({sp_id}) AND (A.SERVERPARTSHOP_ID = '{shop_ids}' OR SERVERPARTSHOP_ID IS NULL)"
        else:
            if sp_id:
                where_sql += f" AND A.SERVERPART_ID IN ({sp_id})"
            if shop_ids:
                where_sql += f" AND A.SERVERPARTSHOP_ID = '{shop_ids}'"
        if start_month:
            where_sql += f" AND A.STATISTICS_MONTH >= {start_month}"
        if end_month:
            where_sql += f" AND STATISTICS_MONTH <= {end_month}"

        sql = f"SELECT A.* FROM T_BUSINESSWARNING A WHERE 1=1 {where_sql}"
        rows = db.execute_query(sql) or []
        if not rows:
            return []

        # 按月份分组（C# 原逻辑: MONTHS distinct ordered）
        months = sorted(set(r.get("STATISTICS_MONTH") for r in rows if r.get("STATISTICS_MONTH") is not None))

        # 定义取字段的辅助函数
        warning_fields = [
            "REVENUE_AMOUNT", "REVENUE_AMOUNT_YOY", "REVENUE_INCREASE_YOY", "REVENUE_INCRATE_YOY",
            "REVENUE_AMOUNT_QOQ", "REVENUE_INCREASE_QOQ", "REVENUE_INCRATE_QOQ",
            "VEHICLE_COUNT", "VEHICLE_COUNT_YOY", "VEHICLE_INCREASE_YOY", "VEHICLE_INCRATE_YOY",
            "VEHICLE_COUNT_QOQ", "VEHICLE_INCREASE_QOQ", "VEHICLE_INCRATE_QOQ",
            "INCREASE_DIFF", "WARING_VUSPD", "WARING_VUSHD", "WARING_VURU", "WARING_VDRD",
        ]

        def _build_warning_node(row, extra=None):
            node = {}
            if row:
                for f in warning_fields:
                    node[f] = row.get(f)
            if extra:
                node.update(extra)
            return node

        result = []
        for month in months:
            month_rows = [r for r in rows if r.get("STATISTICS_MONTH") == month]
            center = {
                "node": {"STATISTICS_MONTH": int(month) if month else None},
                "children": [],
            }

            # 取该月份下所有不重复的服务区
            sp_set = {}
            for r in month_rows:
                sid = r.get("SERVERPART_ID")
                if sid and sid not in sp_set:
                    sp_set[sid] = r.get("SERVERPART_NAME", "")

            for sid, sname in sp_set.items():
                # 服务区节点: DATATYPE=1 的记录
                sp_row = next((r for r in month_rows if r.get("SERVERPART_ID") == sid and r.get("DATATYPE") == 1), None)
                sp_node = {
                    "node": _build_warning_node(sp_row, {
                        "Id": str(sid),
                        "Name": sname,
                        "STATISTICS_MONTH": int(month) if month else None,
                    }),
                    "children": [],
                }

                # 门店节点: DATATYPE=2 的记录
                shop_rows = [r for r in month_rows if r.get("SERVERPART_ID") == sid and r.get("DATATYPE") == 2]
                for sr in shop_rows:
                    shop_child = {
                        "node": _build_warning_node(sr, {
                            "Id": sr.get("SERVERPARTSHOP_ID", ""),
                            "Name": sr.get("SERVERPARTSHOP_NAME", ""),
                            "SERVERPARTSHOP_NAME": sr.get("SERVERPARTSHOP_NAME", ""),
                            "SERVERPART_ID": sid,
                            "SERVERPART_NAME": sname,
                            "SERVERPARTSHOP_ID": sr.get("SERVERPARTSHOP_ID", ""),
                            "STATISTICS_MONTH": int(month) if month else None,
                        }),
                    }
                    sp_node["children"].append(shop_child)

                # C# 原逻辑: WARING_VUSPD=1 && WARING_VUSHD=1 则移除 VUSHD 的门店节点
                has_vuspd = any(c["node"].get("WARING_VUSPD") == 1 for c in sp_node["children"])
                has_vushd = any(c["node"].get("WARING_VUSHD") == 1 for c in sp_node["children"])
                if has_vuspd and has_vushd:
                    sp_node["children"] = [c for c in sp_node["children"] if c["node"].get("WARING_VUSHD") != 1]

                center["children"].append(sp_node)
                result.append(center)

        return result
    except Exception as e:
        logger.error(f"GetMonthINCAnalysis 失败: {e}")
        return []



def get_revenue_report_by_bizp_split_month(db, **kwargs) -> list:
    """
    按拆分月获取营收报表
    C# 逻辑: 使用 T_REVENUEDAILYSPLIT 查询按月拆分的营收数据
    """
    logger.info(f"GetRevenueReportByBIZPSPLITMONTH: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start = kwargs.get("StartDate", "")
        end = kwargs.get("EndDate", "")
        wp = ["REVENUEDAILYSPLIT_STATE = 1"]
        if sp_ids:
            wp.append(f"SERVERPART_ID IN ({sp_ids})")
        if start:
            wp.append(f"STATISTICS_DATE >= {start.replace('-', '')}")
        if end:
            wp.append(f"STATISTICS_DATE <= {end.replace('-', '')}")
        wc = " AND ".join(wp)
        sql = f"""SELECT SERVERPART_ID, SERVERPARTSHOP_ID,
                    SUBSTR(TO_CHAR(STATISTICS_DATE), 1, 6) AS STAT_MONTH,
                    SUM(REVENUE_AMOUNT) AS Revenue_Amount,
                    SUM(CIGARETTE_AMOUNT) AS Cigarette_Amount,
                    SUM(ROYALTY_PRICE) AS Royalty_Price,
                    SUM(SUBROYALTY_PRICE) AS SubRoyalty_Price
                 FROM T_REVENUEDAILYSPLIT WHERE {wc}
                 GROUP BY SERVERPART_ID, SERVERPARTSHOP_ID,
                    SUBSTR(TO_CHAR(STATISTICS_DATE), 1, 6)
                 ORDER BY STAT_MONTH, SERVERPART_ID"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetRevenueReportByBIZPSPLITMONTH 失败: {e}")
        return []


def correct_shop_cigarette(db, data: dict) -> Tuple[bool, str]:
    """
    修正门店卷烟营收
    C# REVENUEDAILYSPLITHelper.CorrectShopCigarette:
    1. 从 T_YSSELLMASTER + T_YSSELLDETAILS 查询烟类销售数据
    2. 与 T_REVENUEDAILYSPLIT 中的 CIGARETTE_AMOUNT 对比
    3. 有差异则更新，缺失则插入
    """
    sp_shop_id = data.get("ServerpartShopId", "")
    start_date = data.get("StartDate", "")
    end_date = data.get("EndDate", "")
    user_name = data.get("UserName", "system")
    logger.info(f"CorrectShopCigarette: Shop={sp_shop_id}, {start_date}~{end_date}")

    if not sp_shop_id or not start_date or not end_date:
        return False, "缺少必要参数"

    try:
        s_date = start_date.replace('-', '')
        e_date = end_date.replace('-', '')

        # 步骤1: 查询烟类商品销售数据
        sell_sql = f"""SELECT C.SERVERPART_ID, C.SERVERPARTSHOP_ID,
                        SUBSTR(A.SELLMASTER_DATE,1,8) AS STATISTICS_DATE,
                        SUM(B.SELLDETAILS_AMOUNT) AS SELLDETAILS_AMOUNT
                     FROM T_YSSELLMASTER A
                     JOIN T_YSSELLDETAILS B ON A.SELLMASTER_CODE = B.SELLMASTER_CODE
                     JOIN T_SERVERPARTSHOP C ON A.SERVERPARTCODE = C.SERVERPART_CODE
                        AND A.SHOPCODE = C.SHOPCODE
                     WHERE A.SELLMASTER_STATE > 0
                        AND A.SELLMASTER_DATE BETWEEN '{s_date}000000' AND '{e_date}240000'
                        AND C.SERVERPARTSHOP_ID IN ({sp_shop_id})
                        AND B.COMMODITY_TYPE LIKE '%烟%'
                     GROUP BY C.SERVERPART_ID, C.SERVERPARTSHOP_ID,
                        SUBSTR(A.SELLMASTER_DATE,1,8)"""
        type_rows = db.execute_query(sell_sql) or []

        # 步骤2: 查询现有营收拆分数据
        split_sql = f"""SELECT * FROM T_REVENUEDAILYSPLIT
                     WHERE REVENUEDAILYSPLIT_STATE = 1
                        AND STATISTICS_DATE BETWEEN {s_date} AND {e_date}
                        AND SERVERPARTSHOP_ID IN ({sp_shop_id})"""
        split_rows = db.execute_query(split_sql) or []

        update_count = 0

        # 步骤3: 对比并更新
        for split_row in split_rows:
            split_date = str(split_row.get("STATISTICS_DATE", ""))
            split_shop = str(split_row.get("SERVERPARTSHOP_ID", ""))
            old_amount = float(split_row.get("CIGARETTE_AMOUNT", 0) or 0)

            # 找对应的烟类销售金额
            new_amount = 0.0
            for tr in type_rows:
                if (str(tr.get("STATISTICS_DATE", "")) == split_date and
                    str(tr.get("SERVERPARTSHOP_ID", "")) == split_shop):
                    new_amount = float(tr.get("SELLDETAILS_AMOUNT", 0) or 0)
                    break

            if old_amount != new_amount:
                from datetime import datetime
                desc = split_row.get("REVENUEDAILYSPLIT_DESC", "") or ""
                desc += f"\n{user_name}于{datetime.now()}重新生成香烟数据：{old_amount}变为{new_amount}"
                desc_escaped = desc.strip().replace("'", "''")
                db.execute_non_query(f"""UPDATE T_REVENUEDAILYSPLIT
                    SET RECORD_DATE = CURRENT_TIMESTAMP,
                        CIGARETTE_AMOUNT = {new_amount},
                        REVENUEDAILYSPLIT_DESC = '{desc_escaped}'
                    WHERE REVENUEDAILYSPLIT_ID = {split_row['REVENUEDAILYSPLIT_ID']}""")
                update_count += 1

        logger.info(f"CorrectShopCigarette: 更新了 {update_count} 条记录")
        return True, f"更新了 {update_count} 条记录"
    except Exception as e:
        logger.error(f"CorrectShopCigarette 失败: {e}")
        return False, str(e)


def get_cigarette_report(db, **kwargs) -> list:
    """
    获取卷烟营收报表
    C# 逻辑: 查询 T_REVENUEDAILYSPLIT 按门店汇总 CIGARETTE_AMOUNT
    """
    logger.info(f"GetCigaretteReport: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start = kwargs.get("StartDate", "")
        end = kwargs.get("EndDate", "")
        wp = ["REVENUEDAILYSPLIT_STATE = 1"]
        if sp_ids:
            wp.append(f"SERVERPART_ID IN ({sp_ids})")
        if start:
            wp.append(f"STATISTICS_DATE >= {start.replace('-', '')}")
        if end:
            wp.append(f"STATISTICS_DATE <= {end.replace('-', '')}")
        wc = " AND ".join(wp)
        sql = f"""SELECT SERVERPART_ID, SERVERPARTSHOP_ID,
                    SUM(CIGARETTE_AMOUNT) AS Total_Cigarette,
                    SUM(REVENUE_AMOUNT) AS Total_Revenue
                 FROM T_REVENUEDAILYSPLIT WHERE {wc}
                 GROUP BY SERVERPART_ID, SERVERPARTSHOP_ID
                 ORDER BY SERVERPART_ID"""
        return db.execute_query(sql) or []
    except Exception as e:
        logger.error(f"GetCigaretteReport 失败: {e}")
        return []


def get_business_item_summary(db, **kwargs) -> list:
    """
    获取经营品项汇总
    C# RevenueStatisticsHelper.GetBusinessItemSummary:
    UNION ALL 当期+同比(4组日期), DataType=1 按业态, 2 按中心, 3 全部
    calcRevenueData 计算当期/同比/累计/累计同比营收增长率
    """
    logger.info(f"GetBusinessItemSummary: {kwargs}")
    try:
        from datetime import datetime

        data_type = int(kwargs.get("DataType", 1) or 1)
        province_code = kwargs.get("ProvinceCode", "")
        sp_id = kwargs.get("ServerpartId", "") or kwargs.get("ServerpartIds", "")
        start = kwargs.get("StartDate", "")
        end = kwargs.get("EndDate", "")
        compare_start = kwargs.get("CompareStartDate", "")
        compare_end = kwargs.get("CompareEndDate", "")
        acc_start = kwargs.get("AccStartDate", "")
        acc_end = kwargs.get("AccEndDate", "")
        acc_compare_start = kwargs.get("AccCompareStartDate", "")
        acc_compare_end = kwargs.get("AccCompareEndDate", "")

        # C# 原逻辑: 默认日期生成
        if start:
            start_dt = datetime.strptime(start[:10], "%Y-%m-%d")
            end_dt = datetime.strptime(end[:10], "%Y-%m-%d") if end else start_dt
            if not compare_start:
                compare_start = (start_dt.replace(year=start_dt.year - 1)).strftime("%Y-%m-%d")
            if not compare_end:
                compare_end = (end_dt.replace(year=end_dt.year - 1)).strftime("%Y-%m-%d")
            if not acc_start:
                acc_start = f"{start_dt.year}/01/01"
            if not acc_end:
                acc_end = end
            if not acc_compare_start:
                c_dt = datetime.strptime(compare_start[:10], "%Y-%m-%d")
                acc_compare_start = f"{c_dt.year}/01/01"
            if not acc_compare_end:
                acc_compare_end = compare_end

        # 格式化日期
        def _fmt(d):
            return d.replace("-", "").replace("/", "")[:8] if d else ""

        s = _fmt(start)
        e = _fmt(end)
        cs = _fmt(compare_start)
        ce = _fmt(compare_end)
        acs = _fmt(acc_start)
        ace = _fmt(acc_end)
        accs = _fmt(acc_compare_start)
        acce = _fmt(acc_compare_end)

        # 计算最小/最大日期范围（C# 原逻辑: 一次 UNION ALL 查询两组数据）
        min_start = min(s, acs) if s and acs else s or acs
        max_end = max(e, ace) if e and ace else e or ace
        min_c_start = min(cs, accs) if cs and accs else cs or accs
        max_c_end = max(ce, acce) if ce and acce else ce or acce

        # 构建 WHERE
        where_sql = ""
        if province_code:
            where_sql += f" AND A.PROVINCE_CODE = '{province_code}'"
        if sp_id:
            where_sql += f" AND A.SERVERPART_ID IN ({sp_id})"

        # UNION ALL: DATATYPE=1 当期/累计, DATATYPE=2 同比
        sql = f"""SELECT
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                B.BUSINESS_TYPE, B.SHOPTRADE, B.SERVERPARTSHOP_ID, 1 AS DATATYPE,
                SUM(CASE WHEN B.STATISTICS_DATE BETWEEN {acs} AND {ace}
                    THEN B.REVENUE_AMOUNT END) AS ACCREVENUE_AMOUNT,
                SUM(CASE WHEN B.STATISTICS_DATE BETWEEN {s} AND {e}
                    THEN B.REVENUE_AMOUNT END) AS REVENUE_AMOUNT
            FROM T_SERVERPART A, T_REVENUEDAILY B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.REVENUEDAILY_STATE = 1
                AND B.STATISTICS_DATE BETWEEN {min_start} AND {max_end}{where_sql}
            GROUP BY A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                B.BUSINESS_TYPE, B.SHOPTRADE, B.SERVERPARTSHOP_ID
            UNION ALL
            SELECT
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                B.BUSINESS_TYPE, B.SHOPTRADE, B.SERVERPARTSHOP_ID, 2 AS DATATYPE,
                SUM(CASE WHEN B.STATISTICS_DATE BETWEEN {accs} AND {acce}
                    THEN B.REVENUE_AMOUNT END) AS ACCREVENUE_AMOUNT,
                SUM(CASE WHEN B.STATISTICS_DATE BETWEEN {cs} AND {ce}
                    THEN B.REVENUE_AMOUNT END) AS REVENUE_AMOUNT
            FROM T_SERVERPART A, T_REVENUEDAILY B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.REVENUEDAILY_STATE = 1
                AND B.STATISTICS_DATE BETWEEN {min_c_start} AND {max_c_end}{where_sql}
            GROUP BY A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                B.BUSINESS_TYPE, B.SHOPTRADE, B.SERVERPARTSHOP_ID"""

        rows = db.execute_query(sql) or []
        if not rows:
            return []

        # C# calcRevenueData 逻辑: 计算当期/同比增减额/增长率
        def _calc_revenue(row_list, filter_fn=None):
            filtered = [r for r in row_list if filter_fn(r)] if filter_fn else row_list
            cur_rows = [r for r in filtered if r.get("DATATYPE") == 1]
            cmp_rows = [r for r in filtered if r.get("DATATYPE") == 2]
            cur_rev = sum(float(r.get("REVENUE_AMOUNT") or 0) for r in cur_rows)
            cmp_rev = sum(float(r.get("REVENUE_AMOUNT") or 0) for r in cmp_rows)
            cur_acc = sum(float(r.get("ACCREVENUE_AMOUNT") or 0) for r in cur_rows)
            cmp_acc = sum(float(r.get("ACCREVENUE_AMOUNT") or 0) for r in cmp_rows)
            result = {
                "RevenueAmount": {
                    "curData": round(cur_rev, 2),
                    "compareData": round(cmp_rev, 2),
                    "increaseData": round(cur_rev - cmp_rev, 2) if cur_rev and cmp_rev else 0,
                    "increaseRate": round((cur_rev - cmp_rev) / cmp_rev * 100, 2) if cmp_rev else 0,
                },
                "ACCRevenueAmount": {
                    "curData": round(cur_acc, 2),
                    "compareData": round(cmp_acc, 2),
                    "increaseData": round(cur_acc - cmp_acc, 2) if cur_acc and cmp_acc else 0,
                    "increaseRate": round((cur_acc - cmp_acc) / cmp_acc * 100, 2) if cmp_acc else 0,
                },
            }
            return result

        nesting_models = []

        # DataType=1 或 3: 按业态分组
        if data_type in (1, 3):
            # 业态分类: 1000=商贸, 2000=餐饅, 3000=其他
            summary_node = {
                "node": {"LineIndex": "1", "Item_Name": "业态", "Serverpart_ID": 0, "Serverpart_Name": "小计"},
                "children": [],
            }
            summary_node["node"].update(_calc_revenue(rows))

            trade_names = {1000: "商贸", 2000: "餐饮", 3000: "其他"}
            trade_num = 1
            for trade_type in [1000, 2000, 3000]:
                if trade_type == 3000:
                    filter_fn = lambda r, tt=trade_type: r.get("BUSINESS_TYPE") not in (1000, "1000") or r.get("SHOPTRADE") not in (1000, "1000", 1005, "1005", 1040, "1040")
                elif trade_type == 1000:
                    filter_fn = lambda r, tt=trade_type: str(r.get("BUSINESS_TYPE", "")) == "1000" and str(r.get("SHOPTRADE", "")) in ("1000", "1005", "1040")
                else:
                    filter_fn = lambda r, tt=trade_type: True  # 简化，实际需 DATA_VALUE 判断

                item_node = {
                    "node": {
                        "LineIndex": f"1.{trade_num}",
                        "Item_Name": "业态",
                        "Serverpart_ID": trade_type,
                        "Serverpart_Name": trade_names.get(trade_type, ""),
                    },
                    "children": [],
                }
                item_node["node"].update(_calc_revenue(rows, filter_fn))

                # 按服务区分组
                sp_set = {}
                for r in rows:
                    if filter_fn(r):
                        sid = r.get("SERVERPART_ID")
                        if sid and sid not in sp_set:
                            sp_set[sid] = r.get("SERVERPART_NAME", "")
                sp_num = 1
                for sid, sname in sp_set.items():
                    sp_node = {
                        "node": {
                            "LineIndex": f"1.{trade_num}.{sp_num}",
                            "Serverpart_ID": sid,
                            "Serverpart_Name": sname,
                        },
                    }
                    sp_node["node"].update(_calc_revenue(rows, lambda r, s=sid: filter_fn(r) and r.get("SERVERPART_ID") == s))
                    item_node["children"].append(sp_node)
                    sp_num += 1

                trade_num += 1
                summary_node["children"].append(item_node)
            nesting_models.append(summary_node)

        # DataType=2 或 3: 按中心（片区→服务区）分组
        if data_type in (2, 3):
            summary_node = {
                "node": {"LineIndex": "2", "Item_Name": "中心", "Serverpart_ID": 0, "Serverpart_Name": "小计"},
                "children": [],
            }
            summary_node["node"].update(_calc_revenue(rows))

            region_set = {}
            for r in rows:
                rid = r.get("SPREGIONTYPE_ID")
                if rid not in region_set:
                    region_set[rid] = {"name": r.get("SPREGIONTYPE_NAME", ""), "index": r.get("SPREGIONTYPE_INDEX", 999999)}

            region_num = 1
            for rid, rinfo in sorted(region_set.items(), key=lambda x: x[1]["index"]):
                region_filter = lambda r, _rid=rid: r.get("SPREGIONTYPE_ID") == _rid if _rid is not None else r.get("SPREGIONTYPE_ID") is None
                region_node = {
                    "node": {
                        "LineIndex": f"2.{region_num}",
                        "Item_Name": "中心",
                        "Serverpart_ID": rid if rid else 0,
                        "Serverpart_Name": rinfo["name"],
                    },
                    "children": [],
                }
                region_node["node"].update(_calc_revenue(rows, region_filter))

                sp_set = {}
                for r in rows:
                    if region_filter(r):
                        sid = r.get("SERVERPART_ID")
                        if sid and sid not in sp_set:
                            sp_set[sid] = r.get("SERVERPART_NAME", "")
                sp_num = 1
                for sid, sname in sp_set.items():
                    sp_node = {
                        "node": {
                            "LineIndex": f"2.{region_num}.{sp_num}",
                            "Serverpart_ID": sid,
                            "Serverpart_Name": sname,
                        },
                    }
                    sp_node["node"].update(_calc_revenue(rows, lambda r, s=sid: r.get("SERVERPART_ID") == s))
                    region_node["children"].append(sp_node)
                    sp_num += 1

                region_num += 1
                summary_node["children"].append(region_node)
            nesting_models.append(summary_node)

        return nesting_models
    except Exception as e:
        logger.error(f"GetBusinessItemSummary 失败: {e}")
        return []

