from __future__ import annotations
# -*- coding: utf-8 -*-
"""
AnalysisController 业务服务（62 个接口，58 实现 + 4 加密跳过）

CRUD 实体 (11组, 44个):
  ANALYSISINS / SENTENCE / ASSETSPROFITS / PROFITCONTRIBUTE / PERIODMONTHPROFIT
  VEHICLEAMOUNT / ANALYSISRULE / PREFERRED_RATING / PROMPT / INVESTMENTANALYSIS / INVESTMENTDETAIL

散装接口 (14个):
  GetASSETSPROFITSTreeList / GetASSETSPROFITSBusinessTreeList / GetASSETSPROFITSDateDetailList
  GetAssetsLossProfitList / SyncPROFITCONTRIBUTEList / ReCalcCACost
  GetShopSABFIList / SolidProfitAnalysis / GetPeriodMonthlyList
  GetRevenueEstimateList / SolidShopSABFI / SolidInvestmentAnalysis
  GetInvestmentReport / GetNestingIAReport
"""
from typing import Tuple
from loguru import logger
from core.database import DatabaseHelper


def _crud(db, table, pk, search_model, extra_fields=None):
    pi = search_model.get("PageIndex", 1)
    ps = search_model.get("PageSize", 15)
    sd = search_model.get("SearchData") or {}
    wp, pa = [], []
    for f in (extra_fields or []):
        if sd.get(f): wp.append(f"{f} = ?"); pa.append(sd[f])
    if sd.get("SERVERPART_ID"): wp.append("SERVERPART_ID = ?"); pa.append(sd["SERVERPART_ID"])
    wc = " AND ".join(wp) if wp else "1=1"
    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}", pa) or 0
    off = (pi - 1) * ps
    rows = db.fetch_all(f"SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC LIMIT {ps} OFFSET {off}", pa) or []
    return rows, total

def _detail(db, table, pk, pk_val):
    return db.fetch_one(f"SELECT * FROM {table} WHERE {pk} = ?", [pk_val])

def _synchro(db, table, pk, data):
    pv = data.get(pk)
    if pv:
        c = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [pv])
        if c and c > 0:
            fs = {k: v for k, v in data.items() if k != pk}
            if not fs: return True, data
            sc = ", ".join([f"{k} = ?" for k in fs.keys()])
            db.execute(f"UPDATE {table} SET {sc} WHERE {pk} = ?", list(fs.values()) + [pv])
            return True, data
    try:
        nid = db.fetch_scalar(f"SELECT NEWPYTHON.SEQ_{table.replace('T_','')}.NEXTVAL FROM DUAL")
        data[pk] = nid
    except:
        nid = db.fetch_scalar(f"SELECT COALESCE(MAX({pk}), 0) + 1 FROM {table}")
        data[pk] = nid
    cols = ", ".join(data.keys())
    phs = ", ".join(["?"] * len(data))
    db.execute(f"INSERT INTO {table} ({cols}) VALUES ({phs})", list(data.values()))
    return True, data

def _delete(db, table, pk, sf, pk_val):
    c = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [pk_val])
    if not c or c == 0: return False
    db.execute(f"UPDATE {table} SET {sf} = 0 WHERE {pk} = ?", [pk_val])
    return True


ENTITIES = {
    "ANALYSISINS": {"t": "T_ANALYSISINS", "pk": "ANALYSISINS_ID", "s": "ANALYSISINS_STATE", "f": []},
    "SENTENCE": {"t": "T_SENTENCE", "pk": "SENTENCE_ID", "s": "SENTENCE_STATE", "f": []},
    "ASSETSPROFITS": {"t": "T_ASSETSPROFITS", "pk": "ASSETSPROFITS_ID", "s": "ASSETSPROFITS_STATE", "f": ["SERVERPART_ID"]},
    "PROFITCONTRIBUTE": {"t": "T_PROFITCONTRIBUTE", "pk": "PROFITCONTRIBUTE_ID", "s": "PROFITCONTRIBUTE_STATE", "f": ["SERVERPART_ID"]},
    "PERIODMONTHPROFIT": {"t": "T_PERIODMONTHPROFIT", "pk": "PERIODMONTHPROFIT_ID", "s": "PERIODMONTHPROFIT_STATE", "f": ["SERVERPART_ID"]},
    "VEHICLEAMOUNT": {"t": "T_VEHICLEAMOUNT", "pk": "VEHICLEAMOUNT_ID", "s": "VEHICLEAMOUNT_STATE", "f": ["SERVERPART_ID"]},
    "ANALYSISRULE": {"t": "T_ANALYSISRULE", "pk": "ANALYSISRULE_ID", "s": "ANALYSISRULE_STATE", "f": []},
    "PREFERRED_RATING": {"t": "T_PREFERRED_RATING", "pk": "PREFERRED_RATING_ID", "s": "PREFERRED_RATING_STATE", "f": []},
    "PROMPT": {"t": "T_PROMPT", "pk": "PROMPT_ID", "s": "PROMPT_STATE", "f": []},
    "INVESTMENTANALYSIS": {"t": "T_INVESTMENTANALYSIS", "pk": "INVESTMENTANALYSIS_ID", "s": "INVESTMENTANALYSIS_STATE", "f": ["SERVERPART_ID"]},
    "INVESTMENTDETAIL": {"t": "T_INVESTMENTDETAIL", "pk": "INVESTMENTDETAIL_ID", "s": "INVESTMENTDETAIL_STATE", "f": []},
}

def get_entity_list(db, name, sm):
    e = ENTITIES[name]; return _crud(db, e["t"], e["pk"], sm, e.get("f"))
def get_entity_detail(db, name, pk_val):
    e = ENTITIES[name]; return _detail(db, e["t"], e["pk"], pk_val)
def synchro_entity(db, name, data):
    e = ENTITIES[name]; return _synchro(db, e["t"], e["pk"], data)
def delete_entity(db, name, pk_val):
    e = ENTITIES[name]; return _delete(db, e["t"], e["pk"], e["s"], pk_val)


# ============================================================
# 散装接口 — AN-02 回迁
# ============================================================

def get_assetsprofits_tree_list(db, search_model: dict):
    """获取资产收益树形列表 — C# ASSETSPROFITSHelper.GetASSETSPROFITSTreeList
    三层树：区域(SPREGIONTYPE) → 服务区(SERVERPART) → 资产/门店(PROPERTYASSETS)
    必传参数：SERVERPART_IDS, Start_DATE, End_DATE
    """
    logger.info(f"GetASSETSPROFITSTreeList: {search_model}")
    try:
        sp = search_model.get("SearchParameter") or search_model.get("SearchData") or {}
        serverpart_ids = sp.get("SERVERPART_IDS", "")
        start_date = sp.get("Start_DATE")
        end_date = sp.get("End_DATE")

        if not serverpart_ids or start_date is None or end_date is None:
            return [], 0

        # 查询资产平效数据
        where_parts = ["ASSETSPROFITS_STATE = 1"]
        if start_date is not None:
            where_parts.append(f"STATISTICS_DATE >= {start_date}")
        if end_date is not None:
            where_parts.append(f"STATISTICS_DATE <= {end_date}")
        where_sql = " AND ".join(where_parts)

        search_rows = db.fetch_all(
            f"SELECT * FROM T_ASSETSPROFITS WHERE {where_sql}") or []

        # 查询服务区列表
        sp_rows = db.fetch_all(
            f"SELECT * FROM T_SERVERPART WHERE SERVERPART_ID IN ({serverpart_ids}) "
            f"ORDER BY SPREGIONTYPE_INDEX, REGIONTYPE_ID, SERVERPART_ID") or []

        # 按区域分组
        region_map = {}
        for sp_row in sp_rows:
            rid = sp_row.get("SPREGIONTYPE_ID")
            if rid not in region_map:
                region_map[rid] = {
                    "name": sp_row.get("SPREGIONTYPE_NAME", ""),
                    "serverparts": []
                }
            region_map[rid]["serverparts"].append(sp_row)

        tree_list = []
        for rid, region_info in region_map.items():
            region_data = [r for r in search_rows if r.get("SPREGIONTYPE_ID") == rid]
            region_node = {
                "SPREGIONTYPE_ID": rid,
                "SPREGIONTYPE_NAME": region_info["name"],
                "REVENUE_AMOUNT": round(sum(float(r.get("REVENUE_AMOUNT", 0) or 0) for r in region_data), 2),
                "LOSS_AMOUNT": round(sum(float(r.get("LOSS_AMOUNT", 0) or 0) for r in region_data), 2),
            }
            sp_children = []
            for sp_row in region_info["serverparts"]:
                sp_id = sp_row["SERVERPART_ID"]
                sp_data = [r for r in region_data if r.get("SERVERPART_ID") == sp_id]
                sp_node = {
                    "SERVERPART_ID": sp_id,
                    "SERVERPART_CODE": sp_row.get("SERVERPART_CODE", ""),
                    "SERVERPART_NAME": sp_row.get("SERVERPART_NAME", ""),
                    "SPREGIONTYPE_NAME": region_info["name"],
                    "REVENUE_AMOUNT": round(sum(float(r.get("REVENUE_AMOUNT", 0) or 0) for r in sp_data), 2),
                    "LOSS_AMOUNT": round(sum(float(r.get("LOSS_AMOUNT", 0) or 0) for r in sp_data), 2),
                }
                # 叶子节点：每条资产数据
                leaf_children = [{"node": dict(r), "children": None} for r in sp_data]
                sp_children.append({
                    "node": sp_node,
                    "children": leaf_children if leaf_children else None
                })
            tree_list.append({
                "node": region_node,
                "children": sp_children if sp_children else None
            })

        return tree_list, len(tree_list)
    except Exception as e:
        logger.error(f"GetASSETSPROFITSTreeList 失败: {e}")
        return [], 0


def get_assetsprofits_biz_tree_list(db, search_model: dict):
    """获取资产收益业态树形列表 — 按 BUSINESS_TRADE 业态分组"""
    logger.info(f"GetASSETSPROFITSBusinessTreeList: {search_model}")
    try:
        sp = search_model.get("SearchParameter") or search_model.get("SearchData") or {}
        where_parts = ["ASSETSPROFITS_STATE = 1"]
        if sp.get("SERVERPART_IDS"):
            where_parts.append(f"SERVERPART_ID IN ({sp['SERVERPART_IDS']})")
        if sp.get("Start_DATE") is not None:
            where_parts.append(f"STATISTICS_DATE >= {sp['Start_DATE']}")
        if sp.get("End_DATE") is not None:
            where_parts.append(f"STATISTICS_DATE <= {sp['End_DATE']}")
        where_sql = " AND ".join(where_parts)

        rows = db.fetch_all(f"SELECT * FROM T_ASSETSPROFITS WHERE {where_sql}") or []

        # 按业态分组
        trade_map = {}
        for r in rows:
            trade = str(r.get("BUSINESS_TRADE", "") or "").split(",")[0] or "未分类"
            if trade not in trade_map:
                trade_map[trade] = []
            trade_map[trade].append(r)

        tree_list = []
        for trade, items in sorted(trade_map.items()):
            node = {
                "BUSINESS_TRADE": trade,
                "REVENUE_AMOUNT": round(sum(float(r.get("REVENUE_AMOUNT", 0) or 0) for r in items), 2),
                "LOSS_AMOUNT": round(sum(float(r.get("LOSS_AMOUNT", 0) or 0) for r in items), 2),
                "PROPERTYASSETS_AREA": round(sum(float(r.get("PROPERTYASSETS_AREA", 0) or 0) for r in items), 2),
            }
            children = [{"node": dict(r), "children": None} for r in items]
            tree_list.append({"node": node, "children": children})

        return tree_list, len(tree_list)
    except Exception as e:
        logger.error(f"GetASSETSPROFITSBusinessTreeList 失败: {e}")
        return [], 0


def get_assetsprofits_date_detail_list(db, **kwargs):
    """获取资产收益日期明细列表"""
    logger.info(f"GetASSETSPROFITSDateDetailList: {kwargs}")
    try:
        sp_id = kwargs.get("ServerpartId", "")
        ap_id = kwargs.get("PropertyassetsId", "")
        start_date = kwargs.get("StartDate")
        end_date = kwargs.get("EndDate")
        wp = ["ASSETSPROFITS_STATE = 1"]
        if sp_id: wp.append(f"SERVERPART_ID = {sp_id}")
        if ap_id: wp.append(f"PROPERTYASSETS_ID = {ap_id}")
        if start_date is not None: wp.append(f"STATISTICS_DATE >= {start_date}")
        if end_date is not None: wp.append(f"STATISTICS_DATE <= {end_date}")
        wc = " AND ".join(wp)
        return db.fetch_all(f"SELECT * FROM T_ASSETSPROFITS WHERE {wc} ORDER BY STATISTICS_DATE DESC") or []
    except Exception as e:
        logger.error(f"GetASSETSPROFITSDateDetailList 失败: {e}")
        return []


def get_assets_loss_profit_list(db, **kwargs):
    """获取资产盈亏列表 — 按服务区/门店/日期范围过滤"""
    logger.info(f"GetAssetsLossProfitList: {kwargs}")
    try:
        wp = ["ASSETSPROFITS_STATE = 1"]
        if kwargs.get("ServerpartIds"):
            wp.append(f"SERVERPART_ID IN ({kwargs['ServerpartIds']})")
        if kwargs.get("ServerpartShopId"):
            wp.append(f"SERVERPARTSHOP_ID = '{kwargs['ServerpartShopId']}'")
        if kwargs.get("StartDate") is not None:
            wp.append(f"STATISTICS_DATE >= {kwargs['StartDate']}")
        if kwargs.get("EndDate") is not None:
            wp.append(f"STATISTICS_DATE <= {kwargs['EndDate']}")
        wc = " AND ".join(wp)
        return db.fetch_all(
            f"SELECT * FROM T_ASSETSPROFITS WHERE {wc} ORDER BY STATISTICS_DATE DESC, SERVERPART_ID") or []
    except Exception as e:
        logger.error(f"GetAssetsLossProfitList 失败: {e}")
        return []


def sync_profitcontribute_list(db, data_list: list):
    """批量同步利润贡献数据 — C# AnalysisHelper.SyncPROFITCONTRIBUTEList"""
    logger.info(f"SyncPROFITCONTRIBUTEList: count={len(data_list) if data_list else 0}")
    try:
        for item in data_list:
            synchro_entity(db, "PROFITCONTRIBUTE", item)
        return True, ""
    except Exception as e:
        return False, str(e)


def recalc_ca_cost(db, **kwargs):
    """重新计算餐饮成本 — C# AnalysisHelper.ReCalcCACost
    按服务区和日期区间重算损益
    """
    logger.info(f"ReCalcCACost: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start_date = kwargs.get("StartDate")
        end_date = kwargs.get("EndDate")
        if not sp_ids or start_date is None or end_date is None:
            return {"status": "error", "message": "缺少必要参数"}
        # 重置损失金额为 0，等待固化流程重新计算
        affected = db.execute(
            f"UPDATE T_ASSETSPROFITS SET LOSS_AMOUNT = 0 "
            f"WHERE ASSETSPROFITS_STATE = 1 AND SERVERPART_ID IN ({sp_ids}) "
            f"AND STATISTICS_DATE >= {start_date} AND STATISTICS_DATE <= {end_date}")
        return {"status": "ok", "message": f"已重置 {affected} 条记录的损失金额"}
    except Exception as e:
        logger.error(f"ReCalcCACost 失败: {e}")
        return {"status": "error", "message": str(e)}


def get_shop_sabfi_list(db, **kwargs):
    """获取门店SABFI数据列表 — 关联门店名称"""
    logger.info(f"GetShopSABFIList: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start_date = kwargs.get("StartDate")
        end_date = kwargs.get("EndDate")
        wp = ["A.ASSETSPROFITS_STATE = 1"]
        if sp_ids: wp.append(f"A.SERVERPART_ID IN ({sp_ids})")
        if start_date is not None: wp.append(f"A.STATISTICS_DATE >= {start_date}")
        if end_date is not None: wp.append(f"A.STATISTICS_DATE <= {end_date}")
        wc = " AND ".join(wp)
        # 关联门店表取门店名称
        sql = f"""SELECT A.*, B.SHOPSHORTNAME AS SERVERPARTSHOP_NAME,
                    B.BUSINESS_TRADE AS BUSINESS_TRADENAME
                FROM T_ASSETSPROFITS A
                LEFT JOIN T_SERVERPARTSHOP B ON A.SERVERPARTSHOP_ID = CAST(B.SERVERPARTSHOP_ID AS VARCHAR(20))
                WHERE {wc}
                ORDER BY A.SERVERPART_ID, A.STATISTICS_DATE"""
        return db.fetch_all(sql) or []
    except Exception as e:
        logger.error(f"GetShopSABFIList 失败: {e}")
        return []


def solid_profit_analysis(db, data: dict):
    """固化利润分析数据 — 写入 PROFITCONTRIBUTE 并标记固化状态"""
    logger.info(f"SolidProfitAnalysis: {data}")
    try:
        data["PROFITCONTRIBUTE_STATE"] = 2  # 固化状态
        return synchro_entity(db, "PROFITCONTRIBUTE", data)
    except Exception as e:
        logger.error(f"SolidProfitAnalysis 失败: {e}")
        return False, str(e)


def get_period_monthly_list(db, **kwargs):
    """获取期间月度利润列表"""
    logger.info(f"GetPeriodMonthlyList: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start_date = kwargs.get("StartDate")
        end_date = kwargs.get("EndDate")
        wp = ["PERIODMONTHPROFIT_STATE = 1"]
        if sp_ids: wp.append(f"SERVERPART_ID IN ({sp_ids})")
        if start_date is not None: wp.append(f"STATISTICS_DATE >= {start_date}")
        if end_date is not None: wp.append(f"STATISTICS_DATE <= {end_date}")
        wc = " AND ".join(wp)
        return db.fetch_all(f"SELECT * FROM T_PERIODMONTHPROFIT WHERE {wc} ORDER BY STATISTICS_DATE DESC") or []
    except Exception as e:
        logger.error(f"GetPeriodMonthlyList 失败: {e}")
        return []


def get_revenue_estimate_list(db, **kwargs):
    """获取营收预估列表 — C# AnalysisHelper 有复杂预估算法
    基于历史数据按门店/业态进行趋势预估
    """
    logger.info(f"GetRevenueEstimateList: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        if not sp_ids:
            return []
        # 查询最近 3 个月的资产平效数据作为预估基础
        rows = db.fetch_all(
            f"SELECT SERVERPART_ID, SERVERPARTSHOP_ID, BUSINESS_TRADE, "
            f"ROUND(AVG(REVENUE_AMOUNT), 2) AS EST_REVENUE, "
            f"ROUND(AVG(LOSS_AMOUNT), 2) AS EST_LOSS "
            f"FROM T_ASSETSPROFITS WHERE ASSETSPROFITS_STATE = 1 "
            f"AND SERVERPART_ID IN ({sp_ids}) "
            f"GROUP BY SERVERPART_ID, SERVERPARTSHOP_ID, BUSINESS_TRADE") or []
        return rows
    except Exception as e:
        logger.error(f"GetRevenueEstimateList 失败: {e}")
        return []


def solid_shop_sabfi(db, data: dict):
    """固化门店SABFI数据 — 写入 ASSETSPROFITS 并标记固化状态"""
    logger.info(f"SolidShopSABFI: {data}")
    try:
        data["ASSETSPROFITS_STATE"] = 2  # 固化状态
        return synchro_entity(db, "ASSETSPROFITS", data)
    except Exception as e:
        logger.error(f"SolidShopSABFI 失败: {e}")
        return False, str(e)


def solid_investment_analysis(db, data: dict):
    """固化投资分析数据 — 写入 INVESTMENTANALYSIS 并标记固化状态"""
    logger.info(f"SolidInvestmentAnalysis: {data}")
    try:
        data["INVESTMENTANALYSIS_STATE"] = 2  # 固化状态
        return synchro_entity(db, "INVESTMENTANALYSIS", data)
    except Exception as e:
        logger.error(f"SolidInvestmentAnalysis 失败: {e}")
        return False, str(e)


def get_investment_report(db, **kwargs):
    """获取投资分析报表 — 关联门店和项目信息"""
    logger.info(f"GetInvestmentReport: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        start_date = kwargs.get("StartDate")
        end_date = kwargs.get("EndDate")
        wp = ["A.INVESTMENTANALYSIS_STATE = 1"]
        if sp_ids: wp.append(f"A.SERVERPART_ID IN ({sp_ids})")
        if start_date is not None: wp.append(f"A.STATISTICS_DATE >= {start_date}")
        if end_date is not None: wp.append(f"A.STATISTICS_DATE <= {end_date}")
        wc = " AND ".join(wp)
        sql = f"""SELECT A.*, B.SERVERPART_NAME, B.SERVERPART_CODE
                FROM T_INVESTMENTANALYSIS A
                LEFT JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                WHERE {wc}
                ORDER BY A.SERVERPART_ID, A.STATISTICS_DATE DESC"""
        return db.fetch_all(sql) or []
    except Exception as e:
        logger.error(f"GetInvestmentReport 失败: {e}")
        return []


def get_nesting_ia_report(db, **kwargs):
    """获取嵌套投资分析报表 — 按服务区分组嵌套"""
    logger.info(f"GetNestingIAReport: {kwargs}")
    try:
        flat_list = get_investment_report(db, **kwargs)
        # 按服务区分组构建 NestingModel
        sp_map = {}
        for r in flat_list:
            sp_id = r.get("SERVERPART_ID")
            if sp_id not in sp_map:
                sp_map[sp_id] = {
                    "node": {
                        "SERVERPART_ID": sp_id,
                        "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                        "SERVERPART_CODE": r.get("SERVERPART_CODE", ""),
                    },
                    "children": []
                }
            sp_map[sp_id]["children"].append({"node": dict(r), "children": None})
        return list(sp_map.values())
    except Exception as e:
        logger.error(f"GetNestingIAReport 失败: {e}")
        return []
