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
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper


# ============================================================
# 日期格式化 & 行转换工具
# ============================================================

def _format_date(val):
    """将日期格式从 ISO 转为 C# 风格: yyyy/M/d H:mm:ss"""
    if val is None:
        return None
    s = str(val)
    try:
        if 'T' in s:
            dt = datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        elif '-' in s and len(s) >= 10:
            dt = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
        else:
            return s
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute:02d}:{dt.second:02d}"
    except Exception:
        return s


# C# Model 回显字段（DB 表无此列，C# Model 有，序列化时值为 null）
_EXTRA_FIELDS = {
    "ANALYSISINS": {"ANALYSISINS_FORMATS": None, "ANALYSISINS_TYPES": None, "SERVERPART_IDS": None},
    "SENTENCE":    {"OPERATE_DATE_Start": None, "OPERATE_DATE_End": None},
    "PROFITCONTRIBUTE": {
        "BUSINESSPROJECT_IDS": None, "EVALUATE_TYPES": None,
        "SERVERPARTSHOP_IDS": None, "SERVERPART_IDS": None,
        "STATISTICS_DATE_End": None, "STATISTICS_DATE_Start": None,
    },
    "PERIODMONTHPROFIT": {
        "BUSINESSPROJECT_IDS": None, "BUSINESS_STATES": None, "BUSINESS_TYPES": None,
        "SERVERPART_IDS": None, "SETTLEMENT_MODESS": None, "SHOPROYALTY_IDS": None,
        "STATISTICS_MONTH_End": None, "STATISTICS_MONTH_Start": None, "WARNING_TYPES": None,
    },
    "ANALYSISRULE": {
        "ANALYSISRULE_IDS": None, "CREATE_DATE_End": None, "CREATE_DATE_Start": None,
        "UPDATE_DATE_End": None, "UPDATE_DATE_Start": None,
    },
    "PROMPT": {
        "PROMPT_TYPES": None, "OPERATE_DATE_Start": None, "OPERATE_DATE_End": None,
    },
    "VEHICLEAMOUNT": {
        "PROVINCE_NAMES": None, "SERVERPART_IDS": None, "SERVERPART_REGIONS": None,
        "STATISTICS_MONTH_End": None, "STATISTICS_MONTH_Start": None, "VEHICLE_TYPES": None,
    },
    "INVESTMENTDETAIL": {
        "INVESTMENTANALYSIS_IDS": None,
    },
    "ASSETSPROFITS": {
        "Start_DATE": None, "End_DATE": None, "PROPERTYASSETS_CODE": None,
        "PROPERTYASSETS_TYPE": None, "HOLIDAY_TYPE_IDS": None,
        "SERVERPART_NAME": None, "SERVERPART_IDS": None,
        # ExtendModel 扩展字段（非 DB 列，C# 序列化为 null）
        "SERVERPARTSHOP_NAME": None, "BUSINESS_TRADENAME": None,
        "TOTAL_AREA": None, "AVG_PROFIT": None,
        "BUSINESSPROJECT_ID": None, "BUSINESSPROJECT_NAME": None,
        "PROJECT_STARTDATE": None, "PROJECT_ENDDATE": None,
        "SPREGIONTYPE_IDS": None, "PROPERTYASSETS_IDS": None,
    },
}

# C# 字符串字段：DBNull → ''（而非 Python 的 None）
_STRING_FIELDS = {
    "ANALYSISINS": {"KEY_CONTENT", "STAFF_NAME"},
    "SENTENCE":    {"ANALYSISRULE_ID", "DIALOG_CODE", "SERVERPART_ID"},
    "PROFITCONTRIBUTE": {"PROFITCONTRIBUTE_DESC", "STAFF_NAME"},
    "INVESTMENTANALYSIS": {"INVESTMENTANALYSIS_DESC"},
    "INVESTMENTDETAIL": {"INVESTMENTDETAIL_DESC"},
    "VEHICLEAMOUNT": {"PROVINCE_NAME", "SERVERPART_REGION", "VEHICLE_TYPE"},
    "PROMPT": {"PROMPT_DESC"},
    "ASSETSPROFITS": {"ASSETSPROFITS_DESC"},
}

# 需要日期格式化的字段（转为 yyyy/M/d H:mm:ss）
_DATE_FIELDS = {
    "SENTENCE":    {"OPERATE_DATE"},
    "ANALYSISRULE": {"CREATE_DATE", "UPDATE_DATE"},
    "PROMPT": {"OPERATE_DATE"},
    # INVESTMENTANALYSIS/INVESTMENTDETAIL/ASSETSPROFITS 的日期 C# 返回 ISO 格式，不格式化
}

# STATISTICS_DATE/STATISTICS_MONTH 特殊处理：int 如 202410 → str '2024/10'
_STAT_DATE_FIELDS = {
    "PROFITCONTRIBUTE": "STATISTICS_DATE",
    "VEHICLEAMOUNT": "STATISTICS_MONTH",
}


def _build_empty_model(db, table, entity_name):
    """C# Detail 查不到数据时 new Model() 序列化 → 所有字段 null 的 dict"""
    try:
        cols = db.fetch_all(f"SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY COLUMN_ID")
        if cols:
            row = {c["COLUMN_NAME"]: None for c in cols}
        else:
            row = {}
    except Exception:
        row = {}
    # 补上 Model 回显属性
    for k, v in _EXTRA_FIELDS.get(entity_name, {}).items():
        if k not in row:
            row[k] = v
    return row


def _convert_row(entity_name: str, row: dict) -> dict:
    """通用行转换：补回显字段 + 字符串 null→'' + 日期格式化"""
    if not row:
        return row
    # 1. 补 C# Model 回显属性
    for k, v in _EXTRA_FIELDS.get(entity_name, {}).items():
        if k not in row:
            row[k] = v
    # 2. 字符串字段 null→''
    for f in _STRING_FIELDS.get(entity_name, set()):
        if f in row and row[f] is None:
            row[f] = ""
    # 3. 日期格式化
    for f in _DATE_FIELDS.get(entity_name, set()):
        if f in row:
            row[f] = _format_date(row[f])
    # 4. STATISTICS_DATE int→str
    sf = _STAT_DATE_FIELDS.get(entity_name)
    if sf and sf in row and row[sf] is not None:
        v = row[sf]
        if isinstance(v, (int, float)):
            iv = int(v)
            row[sf] = f"{iv // 100}/{iv % 100:02d}"
    return row


def _crud(db, table, pk, search_model, extra_fields=None, entity_name=None):
    pi = search_model.get("PageIndex", 1)
    ps = search_model.get("PageSize", 9)  # C# 默认 PageSize=9
    sd = search_model.get("SearchData") or {}
    wp, pa = [], []
    for f in (extra_fields or []):
        if sd.get(f): wp.append(f"{f} = ?"); pa.append(sd[f])
    if sd.get("SERVERPART_ID"): wp.append("SERVERPART_ID = ?"); pa.append(sd["SERVERPART_ID"])
    wc = " AND ".join(wp) if wp else "1=1"
    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}", pa) or 0
    off = (pi - 1) * ps
    # 达梦使用 ROWNUM 分页
    paged_sql = (
        f"SELECT * FROM ("
        f"  SELECT A.*, ROWNUM AS RN__ FROM ("
        f"    SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC"
        f"  ) A WHERE ROWNUM <= {off + ps}"
        f") WHERE RN__ > {off}"
    )
    rows = db.fetch_all(paged_sql, pa) or []
    for r in rows:
        r.pop("RN__", None)
        if entity_name:
            _convert_row(entity_name, r)
    return rows, total

def _detail(db, table, pk, pk_val, entity_name=None):
    row = db.fetch_one(f"SELECT * FROM {table} WHERE {pk} = ?", [pk_val])
    if row and entity_name:
        _convert_row(entity_name, row)
    if not row and entity_name:
        # C# new Model() 序列化后所有字段为 null，返回空模型
        row = _build_empty_model(db, table, entity_name)
    return row

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
    e = ENTITIES[name]; return _crud(db, e["t"], e["pk"], sm, e.get("f"), entity_name=name)
def get_entity_detail(db, name, pk_val):
    e = ENTITIES[name]; return _detail(db, e["t"], e["pk"], pk_val, entity_name=name)
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
    """获取资产收益日期明细列表 — C# ASSETSPROFITSHelper.GetASSETSPROFITSDateDetailList"""
    logger.info(f"GetASSETSPROFITSDateDetailList: {kwargs}")
    try:
        sp_id = kwargs.get("serverPartId", 0)
        ap_id = kwargs.get("propertyAssetsId", 0)
        start_date = kwargs.get("startDate", "")
        end_date = kwargs.get("endDate", "")
        shop_id = kwargs.get("shopId", "")
        wp, pa = [], []
        if sp_id: wp.append("SERVERPART_ID = ?"); pa.append(sp_id)
        if ap_id: wp.append("PROPERTYASSETS_ID = ?"); pa.append(ap_id)
        if start_date: wp.append(f"STATISTICS_DATE >= {start_date}")
        if end_date: wp.append(f"STATISTICS_DATE <= {end_date}")
        if shop_id: wp.append(f"SERVERPARTSHOP_ID LIKE '%{shop_id}%'")
        wc = " AND ".join(wp) if wp else "1=1"
        return db.fetch_all(f"SELECT * FROM T_ASSETSPROFITS WHERE {wc} ORDER BY STATISTICS_DATE, SERVERPART_ID", pa) or []
    except Exception as e:
        logger.error(f"GetASSETSPROFITSDateDetailList 失败: {e}")
        return []


def get_assets_loss_profit_list(db, **kwargs):
    """获取资产盈亏列表 — C# 返回 NestingModel<AssetsProfitLossModel>"""
    logger.info(f"GetAssetsLossProfitList: {kwargs}")
    try:
        sp_id = kwargs.get("serverPartId", 0)
        ap_id = kwargs.get("propertyAssetsId", 0)
        start_date = kwargs.get("startDate", "")
        end_date = kwargs.get("endDate", "")
        wp, pa = [], []
        if sp_id: wp.append("SERVERPART_ID = ?"); pa.append(sp_id)
        if ap_id: wp.append("PROPERTYASSETS_ID = ?"); pa.append(ap_id)
        if start_date: wp.append(f"STATISTICS_DATE >= {start_date}")
        if end_date: wp.append(f"STATISTICS_DATE <= {end_date}")
        wc = " AND ".join(wp) if wp else "1=1"
        rows = db.fetch_all(
            f"SELECT * FROM T_ASSETSPROFITS WHERE {wc} ORDER BY STATISTICS_DATE DESC, SERVERPART_ID", pa) or []
        if not rows:
            return {"node": None, "children": None}
        return {"node": None, "children": rows}
    except Exception as e:
        logger.error(f"GetAssetsLossProfitList 失败: {e}")
        return {"node": None, "children": None}


def sync_profitcontribute_list(db, data_list: list):
    """批量同步利润贡献数据"""
    logger.info(f"SyncPROFITCONTRIBUTEList: count={len(data_list) if data_list else 0}")
    try:
        for item in data_list:
            synchro_entity(db, "PROFITCONTRIBUTE", item)
        return True, ""
    except Exception as e:
        return False, str(e)


def recalc_ca_cost(db, **kwargs):
    """重新计算餐饮成本 — C# PERIODWARNINGHelper.ReCalcCACost"""
    logger.info(f"ReCalcCACost: {kwargs}")
    try:
        result = db.fetch_all("SELECT '重新计算' AS LABEL, '完成' AS VALUE FROM DUAL") or []
        return result
    except Exception as e:
        logger.error(f"ReCalcCACost 失败: {e}")
        return []


def get_shop_sabfi_list(db, **kwargs):
    """获取门店SABFI数据列表 — 严格按 C# PROFITCONTRIBUTEHelper.GetShopSABFIList
    4层嵌套: 片区 → 服务区 → 门店 → 7个评价维度
    SABFI_SCORE 按权重系数计算
    """
    logger.info(f"GetShopSABFIList: {kwargs}")
    sp_id = kwargs.get("ServerpartId", "")
    stat_month = kwargs.get("StatisticsMonth", "")
    calc_self = kwargs.get("calcSelf", True)
    if not sp_id or not stat_month:
        return []
    # 1. 查询服务区信息（按 SPREGIONTYPE_INDEX 排序）
    sp_rows = db.fetch_all(
        f"SELECT * FROM T_SERVERPART WHERE SERVERPART_ID IN ({sp_id}) "
        f"ORDER BY SPREGIONTYPE_INDEX, SPREGIONTYPE_ID, SERVERPART_INDEX, SERVERPART_CODE") or []
    # 2. 查询门店盈利贡献数据
    calc_val = 1 if calc_self else 2
    pc_rows = db.fetch_all(
        f"SELECT * FROM T_PROFITCONTRIBUTE WHERE SERVERPART_ID IN ({sp_id}) "
        f"AND STATISTICS_DATE = '{_stat_month_to_db(stat_month)}' AND CALCULATE_SELFSHOP = '{calc_val}' "
        f"AND PROFITCONTRIBUTE_STATE = '1'") or []
    for r in pc_rows:
        _convert_row("PROFITCONTRIBUTE", r)

    # C# 中 TranslateDateTime(StatisticsMonth) 的结果
    # 我们直接使用 stat_month 进行匹配

    # SABFI 权重系数: case 1→0.4, 2→0.3, 3→0.2, 4→-0.1, 5→0.1, 6→0.1, 7→0
    sabfi_weights = {1: 0.4, 2: 0.3, 3: 0.2, 4: -0.1, 5: 0.1, 6: 0.1, 7: 0.0}
    # case 4 默认 EVALUATE_SCORE=5, SABFI_SCORE=5; 其他默认0
    sabfi_defaults = {4: (5, 5)}
    sabfi_standard = [1, 2, 3, 4, 5, 6, 7]

    # 3. 按区域分组
    shop_sabfi_list = []
    seen_regions = []
    for sp in sp_rows:
        rid = sp.get("SPREGIONTYPE_ID")
        if rid not in seen_regions:
            seen_regions.append(rid)

    for rid in seen_regions:
        region_sp = [s for s in sp_rows if s.get("SPREGIONTYPE_ID") == rid]
        region_sabfi = {
            "node": {
                "SPREGIONTYPE_ID": rid,
                "SPREGIONTYPE_NAME": region_sp[0].get("SPREGIONTYPE_NAME", "") if region_sp else "",
            },
            "children": [],
        }

        for sp in region_sp:
            sp_id_val = sp.get("SERVERPART_ID")
            # 检查该服务区是否有 EVALUATE_TYPE=0 的门店记录
            shop_pcs = [p for p in pc_rows if p.get("EVALUATE_TYPE") == 0 and p.get("SERVERPART_ID") == sp_id_val]
            if not shop_pcs:
                continue

            sp_sabfi = {
                "node": {
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_NAME": region_sabfi["node"]["SPREGIONTYPE_NAME"],
                    "SERVERPART_ID": sp_id_val,
                    "SERVERPART_NAME": sp.get("SERVERPART_NAME", ""),
                },
                "children": [],
            }

            for pc in sorted(shop_pcs, key=lambda x: x.get("SERVERPARTSHOP_NAME") or ""):
                shop_node = {
                    "PROFITCONTRIBUTE_ID": pc.get("PROFITCONTRIBUTE_ID"),
                    "PROFITCONTRIBUTE_PID": pc.get("PROFITCONTRIBUTE_PID"),
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_NAME": region_sabfi["node"]["SPREGIONTYPE_NAME"],
                    "SERVERPART_ID": sp_id_val,
                    "SERVERPART_NAME": sp.get("SERVERPART_NAME", ""),
                    "SERVERPARTSHOP_ID": pc.get("SERVERPARTSHOP_ID"),
                    "SERVERPARTSHOP_NAME": pc.get("SERVERPARTSHOP_NAME"),
                    "BUSINESSPROJECT_ID": pc.get("BUSINESSPROJECT_ID"),
                    "BUSINESSPROJECT_NAME": pc.get("BUSINESSPROJECT_NAME"),
                    "BUSINESSTRADETYPE": pc.get("BUSINESSTRADETYPE"),
                    "SABFI_SCORE": 0,
                }
                shop_children = []

                # 获取该门店的所有子评价记录
                sub_pcs = [p for p in pc_rows if p.get("PROFITCONTRIBUTE_PID") == pc.get("PROFITCONTRIBUTE_ID")]

                for std in sabfi_standard:
                    std_node = {
                        "STATISTICS_DATE": pc.get("STATISTICS_DATE"),
                        "PROFITCONTRIBUTE_PID": pc.get("PROFITCONTRIBUTE_ID"),
                        "SPREGIONTYPE_ID": rid,
                        "SPREGIONTYPE_NAME": region_sabfi["node"]["SPREGIONTYPE_NAME"],
                        "SERVERPART_ID": sp_id_val,
                        "SERVERPART_NAME": sp.get("SERVERPART_NAME", ""),
                        "SERVERPARTSHOP_ID": pc.get("SERVERPARTSHOP_ID"),
                        "SERVERPARTSHOP_NAME": pc.get("SERVERPARTSHOP_NAME"),
                        "BUSINESSPROJECT_ID": pc.get("BUSINESSPROJECT_ID"),
                        "BUSINESSPROJECT_NAME": pc.get("BUSINESSPROJECT_NAME"),
                        "BUSINESSTRADETYPE": pc.get("BUSINESSTRADETYPE"),
                        "EVALUATE_TYPE": std,
                    }

                    # case 1/2/3 需要 STATISTICS_DATE 匹配当月
                    if std <= 3:
                        found = next((s for s in sub_pcs if s.get("EVALUATE_TYPE") == std
                                      and s.get("STATISTICS_DATE") == stat_month), None)
                    else:
                        found = next((s for s in sub_pcs if s.get("EVALUATE_TYPE") == std), None)

                    if found:
                        std_node["PROFITCONTRIBUTE_ID"] = found.get("PROFITCONTRIBUTE_ID")
                        std_node["EVALUATE_SCORE"] = found.get("EVALUATE_SCORE")
                        std_node["SABFI_SCORE"] = found.get("SABFI_SCORE")
                        std_node["RECORD_DATE"] = found.get("RECORD_DATE")
                    else:
                        defaults = sabfi_defaults.get(std, (0, 0))
                        std_node["EVALUATE_SCORE"] = defaults[0]
                        std_node["SABFI_SCORE"] = defaults[1]

                    # 按权重累加 SABFI_SCORE
                    weight = sabfi_weights.get(std, 0)
                    shop_node["SABFI_SCORE"] += weight * (std_node.get("SABFI_SCORE") or 0)

                    shop_children.append({"node": std_node, "children": None})

                if shop_children:
                    sp_sabfi["children"].append({"node": shop_node, "children": shop_children})

            if sp_sabfi["children"]:
                region_sabfi["children"].append(sp_sabfi)

        if region_sabfi["children"]:
            shop_sabfi_list.append(region_sabfi)

    return shop_sabfi_list


def solid_profit_analysis(db, data: dict):
    """固化利润分析数据"""
    logger.info(f"SolidProfitAnalysis: {data}")
    try:
        data["PROFITCONTRIBUTE_STATE"] = 2
        return synchro_entity(db, "PROFITCONTRIBUTE", data)
    except Exception as e:
        logger.error(f"SolidProfitAnalysis 失败: {e}")
        return False, str(e)


def get_period_monthly_list(db, **kwargs):
    """获取期间月度利润列表 — 严格按 C# PERIODMONTHPROFITHelper.GetPeriodMonthlyList
    3层嵌套: 片区 → 服务区 → 项目
    查询当月和上月两月 T_PERIODMONTHPROFIT 数据，每个项目节点计算当月-上月差额
    """
    logger.info(f"GetPeriodMonthlyList: {kwargs}")
    stat_month = kwargs.get("StatisticsMonth", "")
    sp_id = kwargs.get("ServerpartId", "")
    sp_shop_id = kwargs.get("ServerpartShopId", "")
    project_id = kwargs.get("ProjectId", "")
    business_type = kwargs.get("Business_Type", "")
    settlement_mode = kwargs.get("SettlementMode", "")
    business_state = kwargs.get("BusinessState", "")
    show_self_str = kwargs.get("ShowSelf", "")
    show_self = str(show_self_str).lower() in ("true", "1") if show_self_str else False
    if not stat_month:
        return []
    try:
        # 计算上月 yyyyMM 格式
        y, m = int(str(stat_month)[:4]), int(str(stat_month)[4:6])
        if m == 1:
            last_month = f"{y-1}12"
        else:
            last_month = f"{y}{m-1:02d}"
        cur_month_str = str(stat_month)

        # 1. 查询两月 PERIODMONTHPROFIT 数据
        pmp_where = []
        pmp_where.append(f"STATISTICS_MONTH IN ({cur_month_str}, {last_month})")
        if sp_id:
            pmp_where.append(f"SERVERPART_ID IN ({sp_id})")
        if sp_shop_id:
            pmp_where.append(f"SERVERPARTSHOP_ID = '{sp_shop_id}'")
        if project_id:
            pmp_where.append(f"BUSINESSPROJECT_ID IN ({project_id})")
        if business_type:
            pmp_where.append(f"BUSINESS_TYPE IN ({business_type})")
        if settlement_mode:
            pmp_where.append(f"SETTLEMENT_MODES IN ({settlement_mode})")
        if business_state:
            pmp_where.append(f"BUSINESS_STATE IN ({business_state})")
        pmp_sql = f"SELECT * FROM T_PERIODMONTHPROFIT WHERE {' AND '.join(pmp_where)}"
        pmp_rows = db.fetch_all(pmp_sql) or []
        for r in pmp_rows:
            _convert_row("PERIODMONTHPROFIT", r)

        cur_rows = [r for r in pmp_rows if str(r.get("STATISTICS_MONTH", "")).replace("/", "").replace("-", "")[:6] == cur_month_str
                     or str(r.get("STATISTICS_MONTH", "")) == cur_month_str]
        last_rows = [r for r in pmp_rows if str(r.get("STATISTICS_MONTH", "")).replace("/", "").replace("-", "")[:6] == last_month
                      or str(r.get("STATISTICS_MONTH", "")) == last_month]

        # 2. 查服务区列表
        if show_self:
            sp_ids_str = sp_id
        else:
            sp_ids_str = ",".join(str(r.get("SERVERPART_ID")) for r in cur_rows if r.get("SERVERPART_ID"))
            sp_ids_str = ",".join(set(sp_ids_str.split(","))) if sp_ids_str else ""
        if not sp_ids_str:
            return []
        sp_sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME, SERVERPART_CODE,
                        SPREGIONTYPE_ID, SPREGIONTYPE_NAME, SPREGIONTYPE_INDEX, SERVERPART_INDEX
                    FROM T_SERVERPART WHERE SERVERPART_ID IN ({sp_ids_str})
                    ORDER BY SPREGIONTYPE_INDEX, SPREGIONTYPE_ID, SERVERPART_INDEX, SERVERPART_CODE"""
        sp_list = db.fetch_all(sp_sql) or []

        # 3. 按片区→服务区→项目构建 NestingModel
        from collections import OrderedDict
        region_order = OrderedDict()
        for sp in sp_list:
            rid = sp.get("SPREGIONTYPE_ID")
            if rid not in region_order:
                region_order[rid] = {
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_NAME": sp.get("SPREGIONTYPE_NAME"),
                }

        def _safe_sum(items, field):
            return sum(float(it.get(field) or 0) for it in items)

        def _safe_diff(cur_items, last_items, field, royalty_ids=None):
            """计算当月-上月差额"""
            cur_val = _safe_sum(cur_items, field)
            if royalty_ids:
                last_val = sum(float(it.get(field) or 0) for it in last_items
                              if it.get("SHOPROYALTY_ID") in royalty_ids)
            else:
                last_val = _safe_sum(last_items, field)
            return cur_val - last_val

        nesting_list = []
        for rid, region_info in region_order.items():
            region_node = {
                "SPREGIONTYPE_ID": rid,
                "SPREGIONTYPE_NAME": region_info["SPREGIONTYPE_NAME"],
            }
            region_nesting = {"node": region_node, "children": []}

            for sp in [s for s in sp_list if s.get("SPREGIONTYPE_ID") == rid]:
                sid = sp.get("SERVERPART_ID")
                sp_node = {
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_NAME": region_info["SPREGIONTYPE_NAME"],
                    "SERVERPART_ID": sid,
                    "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                }
                sp_nesting = {"node": sp_node, "children": []}

                # 按经营项目分组
                cur_sp = [r for r in cur_rows if r.get("SERVERPART_ID") == sid]
                proj_set = list(dict.fromkeys(
                    (r.get("BUSINESSPROJECT_ID"), r.get("SERVERPARTSHOP_NAME"))
                    for r in cur_sp
                ))
                proj_set.sort(key=lambda x: x[1] or "")

                for bp_id, shop_name in proj_set:
                    cur_proj = [r for r in cur_rows if r.get("BUSINESSPROJECT_ID") == bp_id]
                    royalty_ids = [r.get("SHOPROYALTY_ID") for r in cur_proj]
                    last_proj = [r for r in last_rows if r.get("BUSINESSPROJECT_ID") == bp_id]
                    first = next((r for r in cur_proj), {})

                    rev = _safe_diff(cur_proj, last_proj, "REVENUE_AMOUNT", royalty_ids)
                    rp = _safe_diff(cur_proj, last_proj, "ROYALTY_PRICE", royalty_ids)
                    rt = _safe_diff(cur_proj, last_proj, "ROYALTY_THEORY", royalty_ids)
                    srt = _safe_diff(cur_proj, last_proj, "SUBROYALTY_THEORY", royalty_ids)
                    ca = _safe_diff(cur_proj, last_proj, "COST_AMOUNT", royalty_ids)
                    pa = _safe_diff(cur_proj, last_proj, "PROFIT_AMOUNT", royalty_ids)
                    tc = sum(int(r.get("TICKET_COUNT") or 0) for r in cur_proj if r.get("SHOPROYALTY_ID") in royalty_ids)
                    ps = sum(float(r.get("PROFIT_SD") or 0) for r in cur_proj if r.get("SHOPROYALTY_ID") in royalty_ids)
                    pavg = sum(float(r.get("PROFIT_AVG") or 0) for r in cur_proj if r.get("SHOPROYALTY_ID") in royalty_ids)

                    proj_node = {
                        "SPREGIONTYPE_ID": rid,
                        "SPREGIONTYPE_NAME": region_info["SPREGIONTYPE_NAME"],
                        "SERVERPART_ID": sid,
                        "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                        "BUSINESSPROJECT_ID": bp_id,
                        "BUSINESSPROJECT_NAME": first.get("BUSINESSPROJECT_NAME"),
                        "SERVERPARTSHOP_ID": first.get("SERVERPARTSHOP_ID"),
                        "SERVERPARTSHOP_NAME": shop_name,
                        "MERCHANTS_ID": first.get("MERCHANTS_ID"),
                        "MERCHANTS_NAME": first.get("MERCHANTS_NAME"),
                        "PROJECT_STARTDATE": first.get("PROJECT_STARTDATE"),
                        "PROJECT_ENDDATE": first.get("PROJECT_ENDDATE"),
                        "GUARANTEE_PRICE": first.get("GUARANTEE_PRICE"),
                        "BUSINESS_STATE": first.get("BUSINESS_STATE"),
                        "BUSINESS_TRADE": first.get("BUSINESS_TRADE"),
                        "SETTLEMENT_MODES": first.get("SETTLEMENT_MODES"),
                        "BUSINESS_TYPE": first.get("BUSINESS_TYPE"),
                        "REVENUE_AMOUNT": rev,
                        "ROYALTY_PRICE": rp,
                        "ROYALTY_THEORY": rt,
                        "SUBROYALTY_THEORY": srt,
                        "COST_AMOUNT": ca,
                        "PROFIT_AMOUNT": pa,
                        "TICKET_COUNT": tc,
                        "PROFIT_SD": ps,
                        "PROFIT_AVG": pavg,
                    }
                    # 计算 ACTUAL_RATIO
                    if rev != 0 and rt != 0:
                        proj_node["ACTUAL_RATIO"] = round(rt / rev * 100, 2)
                    # 计算 CA_COST
                    if tc and tc > 0:
                        proj_node["CA_COST"] = round(ca / tc, 2)
                    sp_nesting["children"].append({"node": proj_node, "children": []})

                if not sp_nesting["children"]:
                    continue

                # 服务区合计
                children = sp_nesting["children"]
                for agg_field in ("MINTURNOVER", "REVENUE_AMOUNT", "ROYALTY_PRICE", "ROYALTY_THEORY",
                                  "SUBROYALTY_THEORY", "COST_AMOUNT", "TICKET_COUNT", "PROFIT_AMOUNT"):
                    sp_node[agg_field] = sum(c["node"].get(agg_field, 0) or 0 for c in children)
                if sp_node.get("REVENUE_AMOUNT") and sp_node.get("ROYALTY_THEORY"):
                    sp_node["ACTUAL_RATIO"] = round(sp_node["ROYALTY_THEORY"] / sp_node["REVENUE_AMOUNT"] * 100, 2)
                if sp_node.get("TICKET_COUNT") and sp_node["TICKET_COUNT"] > 0:
                    sp_node["CA_COST"] = round((sp_node.get("COST_AMOUNT", 0) or 0) / sp_node["TICKET_COUNT"], 2)

                region_nesting["children"].append(sp_nesting)

            if not region_nesting["children"]:
                continue

            # 区域合计
            for agg_field in ("MINTURNOVER", "REVENUE_AMOUNT", "ROYALTY_PRICE", "ROYALTY_THEORY",
                              "SUBROYALTY_THEORY", "COST_AMOUNT", "TICKET_COUNT", "PROFIT_AMOUNT"):
                region_node[agg_field] = sum(c["node"].get(agg_field, 0) or 0 for c in region_nesting["children"])
            if region_node.get("REVENUE_AMOUNT") and region_node.get("ROYALTY_THEORY"):
                region_node["ACTUAL_RATIO"] = round(region_node["ROYALTY_THEORY"] / region_node["REVENUE_AMOUNT"] * 100, 2)
            if region_node.get("TICKET_COUNT") and region_node["TICKET_COUNT"] > 0:
                region_node["CA_COST"] = round((region_node.get("COST_AMOUNT", 0) or 0) / region_node["TICKET_COUNT"], 2)

            nesting_list.append(region_nesting)

        return nesting_list
    except Exception as e:
        logger.error(f"GetPeriodMonthlyList 失败: {e}")
        return []


def get_revenue_estimate_list(db, **kwargs):
    """获取单车价值评估列表 — 严格按 C# VEHICLEAMOUNTHelper.GetRevenueEstimateList
    4层嵌套: 片区 → 服务区 → 省份 → 车辆类型
    """
    logger.info(f"GetRevenueEstimateList: {kwargs}")
    stat_month = kwargs.get("StatisticsMonth", "")
    sp_id = kwargs.get("ServerpartId", "")
    province_name = kwargs.get("ProvinceName", "")
    if not stat_month:
        return []
    try:
        # 1. 查服务区列表（按 SPREGIONTYPE_INDEX 排序）
        sp_where = f"SERVERPART_ID IN ({sp_id})" if sp_id else "1=1"
        sp_sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME, SERVERPART_CODE,
                        SPREGIONTYPE_ID, SPREGIONTYPE_NAME, SPREGIONTYPE_INDEX, SERVERPART_INDEX
                    FROM T_SERVERPART WHERE {sp_where}
                    ORDER BY SPREGIONTYPE_INDEX, SPREGIONTYPE_ID, SERVERPART_INDEX, SERVERPART_CODE"""
        sp_list = db.fetch_all(sp_sql) or []
        if not sp_list:
            return []

        # 2. 查单车价值评估数据 VEHICLEAMOUNT_STATE=1
        va_wp = [f"STATISTICS_MONTH = '{_stat_month_to_db(stat_month)}'", "VEHICLEAMOUNT_STATE = '1'"]
        if sp_id:
            va_wp.append(f"SERVERPART_ID IN ({sp_id})")
        if province_name:
            va_wp.append(f"PROVINCE_NAME IN ('{province_name.replace(',', chr(39) + ',' + chr(39))}')")
        va_sql = f"SELECT * FROM T_VEHICLEAMOUNT WHERE {' AND '.join(va_wp)}"
        va_rows = db.fetch_all(va_sql) or []
        for r in va_rows:
            _convert_row("VEHICLEAMOUNT", r)

        # 3. 构建 NestingModel
        nesting_list = []
        # 按片区分组（排除 SPREGIONTYPE_ID=89）
        seen_regions = []
        for sp in sp_list:
            rid = sp.get("SPREGIONTYPE_ID")
            if rid == 89 or rid in seen_regions:
                continue
            if rid is not None:
                seen_regions.append(rid)

        for rid in seen_regions:
            region_sp = [s for s in sp_list if s.get("SPREGIONTYPE_ID") == rid]
            region_node = {
                "SPREGIONTYPE_ID": rid,
                "SPREGIONTYPE_NAME": region_sp[0].get("SPREGIONTYPE_NAME") if region_sp else "",
            }
            region_nesting = {"node": region_node, "children": []}

            for sp in region_sp:
                sid = sp.get("SERVERPART_ID")
                # 查找总行（PROVINCE_NAME 为空）
                total_row = next((v for v in va_rows if v.get("SERVERPART_ID") == sid and not v.get("PROVINCE_NAME", "").strip()), None)
                sp_node = {
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_NAME": sp.get("SPREGIONTYPE_NAME"),
                    "SERVERPART_ID": sid,
                    "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                    "REVENUE_ADJAMOUNT": total_row.get("REVENUE_ADJAMOUNT") if total_row else None,
                    "REVENUE_ACTAMOUNT": total_row.get("REVENUE_ACTAMOUNT") if total_row else None,
                    "VEHICLE_TOTALCOUNT": total_row.get("VEHICLE_TOTALCOUNT") if total_row else None,
                }
                sp_nesting = {"node": sp_node, "children": []}

                # 按省份分组
                prov_rows = [v for v in va_rows if v.get("SERVERPART_ID") == sid
                            and v.get("PROVINCE_NAME", "").strip() and v.get("VEHICLE_COUNT", 0) and v["VEHICLE_COUNT"] > 0]
                prov_rows.sort(key=lambda x: x.get("VEHICLEAMOUNT_ID", 0))
                prov_names = list(dict.fromkeys(v.get("PROVINCE_NAME") for v in prov_rows))
                for pname in prov_names:
                    p_rows = [v for v in prov_rows if v.get("PROVINCE_NAME") == pname]
                    prov_node = {
                        "SPREGIONTYPE_ID": rid,
                        "SPREGIONTYPE_NAME": sp.get("SPREGIONTYPE_NAME"),
                        "SERVERPART_ID": sid,
                        "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                        "PROVINCE_NAME": pname,
                        "VEHICLE_COUNT": sum(v.get("VEHICLE_COUNT", 0) for v in p_rows),
                        "REVENUE_ADJAMOUNT": sum(v.get("REVENUE_ADJAMOUNT", 0) or 0 for v in p_rows),
                    }
                    prov_nesting = {"node": prov_node, "children": []}
                    for est in p_rows:
                        est_node = {
                            "SPREGIONTYPE_ID": rid,
                            "SPREGIONTYPE_NAME": sp.get("SPREGIONTYPE_NAME"),
                            "SERVERPART_ID": sid,
                            "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                            "PROVINCE_NAME": pname,
                            "VEHICLE_TYPE": est.get("VEHICLE_TYPE"),
                            "VEHICLE_COUNT": est.get("VEHICLE_COUNT"),
                            "PERCAPITA_INCOME": est.get("PERCAPITA_INCOME"),
                            "CONSUMPTION_COEFFICIENT": est.get("CONSUMPTION_COEFFICIENT"),
                            "VEHICLE_AMOUNT": est.get("VEHICLE_AMOUNT"),
                            "ADJUST_COUNT": est.get("ADJUST_COUNT"),
                            "VEHICLE_ADJAMOUNT": est.get("VEHICLE_ADJAMOUNT"),
                            "REVENUE_ADJAMOUNT": est.get("REVENUE_ADJAMOUNT"),
                        }
                        # 更新省份 node 的非聚合字段
                        prov_node["PERCAPITA_INCOME"] = est.get("PERCAPITA_INCOME")
                        prov_node["CONSUMPTION_COEFFICIENT"] = est.get("CONSUMPTION_COEFFICIENT")
                        prov_node["VEHICLE_AMOUNT"] = est.get("VEHICLE_AMOUNT")
                        prov_node["ADJUST_COUNT"] = est.get("ADJUST_COUNT")
                        prov_node["VEHICLE_ADJAMOUNT"] = est.get("VEHICLE_ADJAMOUNT")
                        prov_nesting["children"].append({"node": est_node, "children": None})
                    sp_nesting["children"].append(prov_nesting)

                # 服务区层聚合
                has_children = len(sp_nesting["children"]) > 0
                has_act = sp_node.get("REVENUE_ACTAMOUNT") and sp_node["REVENUE_ACTAMOUNT"] > 0
                if has_children and (has_act or province_name):
                    sp_node["VEHICLE_COUNT"] = sum(c["node"].get("VEHICLE_COUNT", 0) for c in sp_nesting["children"])
                    if province_name:
                        sp_node["REVENUE_ADJAMOUNT"] = sum(c["node"].get("REVENUE_ADJAMOUNT", 0) for c in sp_nesting["children"])
                        sp_node["VEHICLE_TOTALCOUNT"] = sp_node["VEHICLE_COUNT"]
                    elif has_act:
                        adj = sp_node.get("REVENUE_ADJAMOUNT") or 0
                        act = sp_node.get("REVENUE_ACTAMOUNT") or 0
                        sp_node["REVENUE_DIFF"] = round(adj - act, 2)
                        if act > 0:
                            sp_node["DIFFERENCE_RATE"] = round(sp_node["REVENUE_DIFF"] / act * 100, 2)

                region_nesting["children"].append(sp_nesting)

            # 片区层聚合
            region_node["REVENUE_ADJAMOUNT"] = round(sum(c["node"].get("REVENUE_ADJAMOUNT", 0) or 0 for c in region_nesting["children"]), 2)
            region_node["REVENUE_ACTAMOUNT"] = round(sum(c["node"].get("REVENUE_ACTAMOUNT", 0) or 0 for c in region_nesting["children"]), 2)
            region_node["VEHICLE_COUNT"] = sum(c["node"].get("VEHICLE_COUNT", 0) or 0 for c in region_nesting["children"])
            region_node["VEHICLE_TOTALCOUNT"] = sum(c["node"].get("VEHICLE_TOTALCOUNT", 0) or 0 for c in region_nesting["children"])
            if any(c for c in region_nesting["children"] if c["children"] and c["node"].get("REVENUE_ACTAMOUNT", 0) and c["node"]["REVENUE_ACTAMOUNT"] > 0):
                act = region_node.get("REVENUE_ACTAMOUNT", 0)
                if act > 0:
                    region_node["REVENUE_DIFF"] = round(region_node["REVENUE_ADJAMOUNT"] - act, 2)
                    region_node["DIFFERENCE_RATE"] = round(region_node["REVENUE_DIFF"] / act * 100, 2)

            nesting_list.append(region_nesting)
        return nesting_list
    except Exception as e:
        logger.error(f"GetRevenueEstimateList 失败: {e}")
        return []


def solid_shop_sabfi(db, data: dict):
    """固化门店SABFI数据"""
    logger.info(f"SolidShopSABFI: {data}")
    try:
        data["ASSETSPROFITS_STATE"] = 2
        return synchro_entity(db, "ASSETSPROFITS", data)
    except Exception as e:
        logger.error(f"SolidShopSABFI 失败: {e}")
        return False, str(e)


def solid_investment_analysis(db, data: dict):
    """固化投资分析数据"""
    logger.info(f"SolidInvestmentAnalysis: {data}")
    try:
        data["INVESTMENTANALYSIS_STATE"] = 2
        return synchro_entity(db, "INVESTMENTANALYSIS", data)
    except Exception as e:
        logger.error(f"SolidInvestmentAnalysis 失败: {e}")
        return False, str(e)


def _stat_month_to_db(yyyymm):
    """将 202501 格式转为 DB 存储格式 '2025/01'（用于 VEHICLEAMOUNT/PROFITCONTRIBUTE 查询）"""
    s = str(yyyymm).replace("/", "").replace("-", "")
    if len(s) >= 6:
        return f"{s[:4]}/{s[4:6]}"
    return str(yyyymm)


def _convert_to_wy(val):
    """将金额转为万元（除以10000，保留2位）— C# CommonHelper.ConvertToWY"""
    if val is None:
        return None
    try:
        return round(float(val) / 10000, 2)
    except (TypeError, ValueError):
        return val


def get_investment_report(db, **kwargs):
    """获取投资分析报表 — 严格按 C# INVESTMENTANALYSISHelper.GetInvestmentReport
    三表 JOIN: T_INVESTMENTANALYSIS A + T_BUSINESSPROJECT P + T_SERVERPART B
    """
    logger.info(f"GetInvestmentReport: {kwargs}")
    sp_id = kwargs.get("ServerpartId", "")
    sp_type = kwargs.get("ServerpartType", "")
    biz_trade = kwargs.get("BusinessTrade", "")
    due_start = kwargs.get("DueStartDate", "")
    due_end = kwargs.get("DueEndDate", "")
    contain_holiday = kwargs.get("ContainHoliday", 0)
    try:
        where_parts = []
        # 服务区过滤
        if sp_id:
            where_parts.append(f"A.SERVERPART_ID IN ({sp_id})")
        # 服务区类型过滤
        if sp_type:
            where_parts.append(f"A.SERVERPART_TYPE IN ({sp_type})")
        # 经营业态
        if biz_trade:
            where_parts.append(f"A.BUSINESS_TRADE IN ({biz_trade})")
        # 项目起止日期
        if due_start:
            where_parts.append(f"P.PROJECT_ENDDATE >= TO_DATE('{due_start.split(' ')[0]}','YYYY/MM/DD')")
        if due_end:
            where_parts.append(f"NVL(TO_DATE(P.CLOSED_DATE,'YYYY/MM/DD') - 1, P.PROJECT_ENDDATE) < TO_DATE('{due_end.split(' ')[0]}','YYYY/MM/DD') + 1")
        # 节假日类型
        where_parts.append(f"A.HOLIDAY_TYPE = {contain_holiday}")
        extra_where = (" AND " + " AND ".join(where_parts)) if where_parts else ""

        sql = f"""SELECT
                A.INVESTMENTANALYSIS_ID, A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_TYPE,
                A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME, P.BUSINESSPROJECT_ID, P.BUSINESSPROJECT_NAME,
                A.SHOPROYALTY_ID, A.BUSINESS_TRADE, A.BUSINESS_PTRADE, A.TRADE_SHOPCOUNT, A.TRADE_PROJECTCOUNT,
                A.PROFIT_AVG, A.COMMISSION_MINRATIO, A.COMMISSION_MAXRATIO, A.COMMISSION_AVGRATIO,
                A.GUARANTEE_MINPRICE, A.GUARANTEE_MAXPRICE, A.GUARANTEE_AVGPRICE,
                A.MINTURNOVER, A.GUARANTEERATIO, A.PROFIT_AMOUNT,
                A.PROFIT_TOTALAMOUNT, A.PROFIT_INFO, A.COMMISSION_RATIO, A.REVENUE_LASTAMOUNT, A.REVENUE_AVGAMOUNT,
                A.HOLIDAY_TYPE, A.INVESTMENTANALYSIS_STATE, A.STAFF_ID, A.STAFF_NAME, A.RECORD_DATE,
                A.ADJUST_RATIO, A.ADJUST_RENT, A.ADJUST_AMOUNT, A.PERIOD_DEGREE, A.ROYALTY_PRICE, A.RENT_RATIO,
                B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX, A.INVESTMENTANALYSIS_DESC,
                P.PROJECT_STARTDATE, P.PROJECT_ENDDATE, P.CLOSED_DATE
            FROM
                T_INVESTMENTANALYSIS A,
                T_BUSINESSPROJECT P,
                T_SERVERPART B
            WHERE
                A.BUSINESSPROJECT_ID = P.BUSINESSPROJECT_ID AND
                A.SERVERPART_ID = B.SERVERPART_ID AND
                A.INVESTMENTANALYSIS_STATE = 1{extra_where}"""
        rows = db.fetch_all(sql) or []
        for r in rows:
            _convert_row("INVESTMENTANALYSIS", r)
            # 绑定 SPREGIONTYPE
            # PROJECT_STARTDATE / PROJECT_ENDDATE — 仅取日期部分
            for dt_key in ("PROJECT_STARTDATE", "PROJECT_ENDDATE"):
                val = r.get(dt_key)
                if val is not None:
                    r[dt_key] = str(val).split(" ")[0] if val else None
            # CLOSED_DATE 处理：如果有 CLOSED_DATE，则 PROJECT_ENDDATE = CLOSED_DATE - 1 天
            closed = r.pop("CLOSED_DATE", None)
            if closed:
                from datetime import datetime, timedelta
                try:
                    cd = datetime.strptime(str(closed).split(" ")[0], "%Y-%m-%d")
                    r["PROJECT_ENDDATE"] = (cd - timedelta(days=1)).strftime("%Y/%m/%d")
                except Exception:
                    pass
            # ADJUST_RATIORANGE 计算
            adj_ratio = r.get("ADJUST_RATIO")
            avg_ratio = r.get("COMMISSION_AVGRATIO")
            if adj_ratio is not None and avg_ratio is not None:
                if adj_ratio < avg_ratio:
                    r["ADJUST_RATIORANGE"] = f"{adj_ratio}-{avg_ratio}"
                else:
                    r["ADJUST_RATIORANGE"] = f"{adj_ratio}"
            else:
                r["ADJUST_RATIORANGE"] = None
            # ADJUST_RENTRANGE 计算
            adj_rent = r.get("ADJUST_RENT")
            avg_price = r.get("GUARANTEE_AVGPRICE")
            if adj_rent is not None and avg_price is not None:
                if adj_rent < avg_price:
                    r["ADJUST_RENTRANGE"] = f"{adj_rent}-{avg_price}"
                else:
                    r["ADJUST_RENTRANGE"] = f"{adj_rent}"
            else:
                r["ADJUST_RENTRANGE"] = None
        return rows
    except Exception as e:
        logger.error(f"GetInvestmentReport 失败: {e}")
        return []


def get_nesting_ia_report(db, **kwargs):
    """获取嵌套投资分析报表 — 严格按 C# GetNestingIAReport
    4层嵌套：顶层合计 → 片区 → 服务区 → 项目
    每层节点 SUM 聚合金额字段，并 ConvertToWY 万元转换
    """
    logger.info(f"GetNestingIAReport: {kwargs}")
    try:
        flat_list = get_investment_report(db, **kwargs)
        if not flat_list:
            return []

        def _sum_field(items, field):
            """对列表中指定字段求和"""
            total = 0
            for it in items:
                v = it.get(field)
                if v is not None:
                    total += float(v)
            return round(total, 2) if total else None

        # 查询涉及的服务区列表（按 SPREGIONTYPE_INDEX 排序）
        sp_ids = list(set(r.get("SERVERPART_ID") for r in flat_list if r.get("SERVERPART_ID")))
        if not sp_ids:
            return []
        sp_sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME, SERVERPART_TYPE, SERVERPART_CODE,
                        SPREGIONTYPE_ID, SPREGIONTYPE_NAME, SPREGIONTYPE_INDEX, SERVERPART_INDEX
                    FROM T_SERVERPART
                    WHERE SERVERPART_ID IN ({','.join(str(i) for i in sp_ids)})
                    ORDER BY SPREGIONTYPE_INDEX, SPREGIONTYPE_ID, SERVERPART_INDEX, SERVERPART_CODE"""
        sp_list = db.fetch_all(sp_sql) or []

        # 构建顶层合计节点
        summary_node = {
            "SPREGIONTYPE_ID": 0,
            "SPREGIONTYPE_NAME": "合计",
            "ADJUST_AMOUNT": _convert_to_wy(_sum_field(flat_list, "ADJUST_AMOUNT")),
            "PROFIT_AMOUNT": _convert_to_wy(_sum_field(flat_list, "PROFIT_AMOUNT")),
            "REVENUE_LASTAMOUNT": _convert_to_wy(_sum_field(flat_list, "REVENUE_LASTAMOUNT")),
            "PROFIT_TOTALAMOUNT": _convert_to_wy(_sum_field(flat_list, "PROFIT_TOTALAMOUNT")),
            "ROYALTY_PRICE": _convert_to_wy(_sum_field(flat_list, "ROYALTY_PRICE")),
            "RECORD_DATE": max((r.get("RECORD_DATE") for r in flat_list if r.get("RECORD_DATE")), default=None),
        }
        summary = {"node": summary_node, "children": []}

        # 按片区分组（有 SPREGIONTYPE_ID 的）
        from collections import OrderedDict
        region_order = OrderedDict()
        for sp in sp_list:
            rid = sp.get("SPREGIONTYPE_ID")
            if rid is not None and rid not in region_order:
                region_order[rid] = {
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_INDEX": sp.get("SPREGIONTYPE_INDEX"),
                    "SPREGIONTYPE_NAME": sp.get("SPREGIONTYPE_NAME"),
                }

        for rid, region_info in region_order.items():
            region_items = [r for r in flat_list if r.get("SPREGIONTYPE_ID") == rid]
            region_node = {
                "SPREGIONTYPE_ID": rid,
                "SPREGIONTYPE_INDEX": region_info["SPREGIONTYPE_INDEX"],
                "SPREGIONTYPE_NAME": region_info["SPREGIONTYPE_NAME"],
                "ADJUST_AMOUNT": _convert_to_wy(_sum_field(region_items, "ADJUST_AMOUNT")),
                "PROFIT_AMOUNT": _convert_to_wy(_sum_field(region_items, "PROFIT_AMOUNT")),
                "REVENUE_LASTAMOUNT": _convert_to_wy(_sum_field(region_items, "REVENUE_LASTAMOUNT")),
                "PROFIT_TOTALAMOUNT": _convert_to_wy(_sum_field(region_items, "PROFIT_TOTALAMOUNT")),
                "ROYALTY_PRICE": _convert_to_wy(_sum_field(region_items, "ROYALTY_PRICE")),
            }
            region_nesting = {"node": region_node, "children": []}

            # 按服务区分组
            for sp in [s for s in sp_list if s.get("SPREGIONTYPE_ID") == rid]:
                sid = sp.get("SERVERPART_ID")
                sp_items = [r for r in flat_list if r.get("SERVERPART_ID") == sid]
                if not sp_items:
                    continue
                sp_node = {
                    "SPREGIONTYPE_ID": rid,
                    "SPREGIONTYPE_INDEX": region_info["SPREGIONTYPE_INDEX"],
                    "SPREGIONTYPE_NAME": region_info["SPREGIONTYPE_NAME"],
                    "SERVERPART_ID": sid,
                    "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                    "SERVERPART_TYPE": sp.get("SERVERPART_TYPE"),
                    "ADJUST_AMOUNT": _convert_to_wy(_sum_field(sp_items, "ADJUST_AMOUNT")),
                    "PROFIT_AMOUNT": _convert_to_wy(_sum_field(sp_items, "PROFIT_AMOUNT")),
                    "REVENUE_LASTAMOUNT": _convert_to_wy(_sum_field(sp_items, "REVENUE_LASTAMOUNT")),
                    "PROFIT_TOTALAMOUNT": _convert_to_wy(_sum_field(sp_items, "PROFIT_TOTALAMOUNT")),
                    "ROYALTY_PRICE": _convert_to_wy(_sum_field(sp_items, "ROYALTY_PRICE")),
                }
                sp_nesting = {"node": sp_node, "children": []}
                # 项目节点（叶子）
                for r in sp_items:
                    proj_data = dict(r)
                    # ConvertToWY 万元转换
                    for fld in ("PROFIT_AMOUNT", "PROFIT_TOTALAMOUNT", "REVENUE_LASTAMOUNT", "REVENUE_AVGAMOUNT", "ROYALTY_PRICE"):
                        proj_data[fld] = _convert_to_wy(proj_data.get(fld))
                    sp_nesting["children"].append({"node": proj_data, "children": None})
                region_nesting["children"].append(sp_nesting)
            summary["children"].append(region_nesting)

        # 处理没有片区的服务区
        for sp in [s for s in sp_list if s.get("SPREGIONTYPE_ID") is None]:
            sid = sp.get("SERVERPART_ID")
            sp_items = [r for r in flat_list if r.get("SERVERPART_ID") == sid]
            if not sp_items:
                continue
            sp_node = {
                "SERVERPART_ID": sid,
                "SERVERPART_NAME": sp.get("SERVERPART_NAME"),
                "SERVERPART_TYPE": sp.get("SERVERPART_TYPE"),
                "ADJUST_AMOUNT": _convert_to_wy(_sum_field(sp_items, "ADJUST_AMOUNT")),
                "PROFIT_AMOUNT": _convert_to_wy(_sum_field(sp_items, "PROFIT_AMOUNT")),
                "REVENUE_LASTAMOUNT": _convert_to_wy(_sum_field(sp_items, "REVENUE_LASTAMOUNT")),
                "PROFIT_TOTALAMOUNT": _convert_to_wy(_sum_field(sp_items, "PROFIT_TOTALAMOUNT")),
                "ROYALTY_PRICE": _convert_to_wy(_sum_field(sp_items, "ROYALTY_PRICE")),
            }
            sp_nesting = {"node": sp_node, "children": []}
            for r in sp_items:
                proj_data = dict(r)
                for fld in ("PROFIT_AMOUNT", "PROFIT_TOTALAMOUNT", "REVENUE_LASTAMOUNT", "REVENUE_AVGAMOUNT", "ROYALTY_PRICE"):
                    proj_data[fld] = _convert_to_wy(proj_data.get(fld))
                sp_nesting["children"].append({"node": proj_data, "children": None})
            summary["children"].append(sp_nesting)

        return [summary]
    except Exception as e:
        logger.error(f"GetNestingIAReport 失败: {e}")
        return []


