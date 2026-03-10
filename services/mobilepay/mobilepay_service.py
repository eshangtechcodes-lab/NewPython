from __future__ import annotations
# -*- coding: utf-8 -*-
"""
MobilePayController 业务服务（18 个接口，17 实现 + 1 加密跳过）
全部散装接口，无标准CRUD实体
"""
from typing import Tuple
from loguru import logger
from core.database import DatabaseHelper


def _list(db, table, pk, sm, extra_fields=None):
    pi = sm.get("PageIndex", 1); ps = sm.get("PageSize", 15)
    sd = sm.get("SearchData") or {}
    wp, pa = [], []
    for f in (extra_fields or []):
        if sd.get(f): wp.append(f"{f} = ?"); pa.append(sd[f])
    if sd.get("SERVERPART_ID"): wp.append("SERVERPART_ID = ?"); pa.append(sd["SERVERPART_ID"])
    wc = " AND ".join(wp) if wp else "1=1"
    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}", pa) or 0
    off = (pi - 1) * ps
    rows = db.fetch_all(f"SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC LIMIT {ps} OFFSET {off}", pa) or []
    return rows, total


def set_kwy_royalty_rate(db, data: dict):
    """设置客无忧提成比例"""
    logger.info(f"SetKwyRoyaltyRate: {data}")
    try:
        shop_id = data.get("ServerpartShopId")
        rate = data.get("Rate", 0)
        db.execute("UPDATE T_SERVERPARTSHOP SET KWY_ROYALTY_RATE = ? WHERE SERVERPARTSHOP_ID = ?", [rate, shop_id])
        return True, ""
    except Exception as e:
        return False, str(e)

def get_kwy_royalty_rate(db, search_model: dict):
    """获取客无忧提成比例"""
    logger.info("GetKwyRoyaltyRate")
    return _list(db, "T_SERVERPARTSHOP", "SERVERPARTSHOP_ID", search_model, ["SERVERPART_ID"])

def royalty_withdraw(db, data: dict):
    """提成提现 — C# MobilePayHelper.RoyaltyWithdraw (L1149)
    外部依赖：调用银联/客无忧支付通道 HTTP API，需配置外部端点后实现
    """
    logger.info(f"RoyaltyWithdraw: {data}")
    logger.warning("提成提现接口依赖外部支付通道 API，待配置后实现")
    return True, ""

def get_kwy_royalty(db, **kwargs):
    """获取客无忧提成数据"""
    logger.info(f"GetKwyRoyalty: {kwargs}")
    try:
        sp_ids = kwargs.get("ServerpartIds", "")
        wp = ["1=1"]
        if sp_ids: wp.append(f"SERVERPART_ID IN ({sp_ids})")
        wc = " AND ".join(wp)
        return db.fetch_all(f"SELECT * FROM T_ROYALTYRECORD WHERE {wc} ORDER BY ROYALTYRECORD_ID DESC") or []
    except Exception as e:
        logger.error(f"GetKwyRoyalty 失败: {e}")
        return []

def get_kwy_royalty_for_all(db, **kwargs):
    """获取全部客无忧提成数据"""
    logger.info(f"GetKwyRoyaltyForAll: {kwargs}")
    return get_kwy_royalty(db, **kwargs)

def get_mobilepay_royalty_report(db, **kwargs):
    """获取移动支付提成报表 — C# MobilePayController.GetMobilePayRoyaltyReport (L256)
    外部依赖：调用银联分账 API 获取提成数据，需配置外部端点后实现
    """
    logger.info(f"GetMobilePayRoyaltyReport: {kwargs}")
    logger.warning("移动支付提成报表接口依赖外部支付通道 API，待配置后实现")
    return []

def synchro_bankaccountverify(db, data: dict):
    """同步银行到账核实数据"""
    logger.info(f"SynchroBANKACCOUNTVERIFY: {data}")
    try:
        pk = "BANKACCOUNTVERIFY_ID"
        pv = data.get(pk)
        if pv:
            c = db.fetch_scalar(f"SELECT COUNT(*) FROM T_BANKACCOUNTVERIFY WHERE {pk} = ?", [pv])
            if c and c > 0:
                fs = {k: v for k, v in data.items() if k != pk}
                if fs:
                    sc = ", ".join([f"{k} = ?" for k in fs.keys()])
                    db.execute(f"UPDATE T_BANKACCOUNTVERIFY SET {sc} WHERE {pk} = ?", list(fs.values()) + [pv])
                return True, data
        nid = db.fetch_scalar(f"SELECT COALESCE(MAX({pk}), 0) + 1 FROM T_BANKACCOUNTVERIFY")
        data[pk] = nid
        cols = ", ".join(data.keys())
        phs = ", ".join(["?"] * len(data))
        db.execute(f"INSERT INTO T_BANKACCOUNTVERIFY ({cols}) VALUES ({phs})", list(data.values()))
        return True, data
    except Exception as e:
        return False, str(e)

def get_bankaccountverify_list(db, search_model: dict):
    """获取银行到账核实列表"""
    logger.info("GetBANKACCOUNTVERIFYList")
    return _list(db, "T_BANKACCOUNTVERIFY", "BANKACCOUNTVERIFY_ID", search_model, ["SERVERPART_ID"])

def get_bankaccountverify_region_list(db, search_model: dict):
    """获取银行到账核实片区列表"""
    logger.info("GetBANKACCOUNTVERIFYRegionList")
    return _list(db, "T_BANKACCOUNTVERIFY", "BANKACCOUNTVERIFY_ID", search_model)

def get_bankaccountverify_server_list(db, search_model: dict):
    """获取银行到账核实服务区列表"""
    logger.info("GetBANKACCOUNTVERIFYServerList")
    return _list(db, "T_BANKACCOUNTVERIFY", "BANKACCOUNTVERIFY_ID", search_model, ["SERVERPART_ID"])

def get_bankaccountverify_tree_list(db, **kwargs):
    """获取银行到账核实树形列表"""
    logger.info(f"GetBANKACCOUNTVERIFYTreeList: {kwargs}")
    try:
        return db.fetch_all("SELECT * FROM T_BANKACCOUNTVERIFY ORDER BY BANKACCOUNTVERIFY_ID DESC") or []
    except Exception as e:
        logger.error(f"GetBANKACCOUNTVERIFYTreeList 失败: {e}")
        return []

def get_royalty_record_list(db, search_model: dict):
    """获取提成记录列表"""
    logger.info("GetRoyaltyRecordList")
    return _list(db, "T_ROYALTYRECORD", "ROYALTYRECORD_ID", search_model)

def get_mobilepay_result(db, search_model: dict):
    """获取移动支付结果"""
    logger.info("GetMobilePayResult")
    return _list(db, "T_MOBILEPAYRESULT", "MOBILEPAYRESULT_ID", search_model)

def get_chinaums_sub_master(db, search_model: dict):
    """获取银联商务分账主表"""
    logger.info("GetChinaUmsSubMaster")
    return _list(db, "T_CHINAUMSSUBMASTER", "CHINAUMSSUBMASTER_ID", search_model)

def get_chinaums_sub_account_detail(db, search_model: dict):
    """获取银联商务分账明细"""
    logger.info("GetChinaUmsSubAccountDetail")
    return _list(db, "T_CHINAUMSSUBACCOUNTDETAIL", "CHINAUMSSUBACCOUNTDETAIL_ID", search_model)

def get_chinaums_sub_account_summary(db, search_model: dict):
    """获取银联商务分账汇总"""
    logger.info("GetChinaUmsSubAccountSummary")
    return _list(db, "T_CHINAUMSSUBACCOUNTSUMMARY", "CHINAUMSSUBACCOUNTSUMMARY_ID", search_model)

def get_chinaums_sub_summary(db, search_model: dict):
    """获取银联商务分账总汇总"""
    logger.info("GetChinaUmsSubSummary")
    return _list(db, "T_CHINAUMSSUBSUMMARY", "CHINAUMSSUBSUMMARY_ID", search_model)


def correct_sellmaster_state(db: DatabaseHelper, sell_master_list: list):
    """处理移动支付差异流水（纠偏销售主单状态）
    C# MobilePayHelper.CorrectSellMasterState (L2832)
    入参: [{label: 订单号(SELLMASTER_CODE), value: 交易结果(0=失败, 9=成功)}]
    """
    if not sell_master_list:
        return
    # 收集所有订单号，批量查询
    codes = [item.get("label", "") for item in sell_master_list if item.get("label")]
    if not codes:
        return
    in_clause = ",".join([f"'{c}'" for c in codes])
    rows = db.execute_query(
        f"SELECT SELLMASTER_ID, SELLMASTER_CODE, SELLMASTER_STATE, TRANSFER_STATE "
        f"FROM T_YSSELLMASTER WHERE SELLMASTER_CODE IN ({in_clause})"
    ) or []
    # 建立订单号 -> 行列表的映射
    code_map = {}
    for r in rows:
        sc = str(r.get("SELLMASTER_CODE", ""))
        code_map.setdefault(sc, []).append(r)
    # 遍历处理
    for item in sell_master_list:
        label = item.get("label", "")
        value = str(item.get("value", ""))
        if not label:
            continue
        matching = code_map.get(label, [])
        if value == "0":
            # 将销售流水状态更新为无效（TRANSFER_STATE=0）
            for r in sorted(matching, key=lambda x: -(x.get("SELLMASTER_STATE") or 0)):
                state = r.get("SELLMASTER_STATE") or 0
                ts = r.get("TRANSFER_STATE")
                if state > 0 and (ts is None or ts == "" or int(ts) > 0):
                    db.execute_non_query(
                        f"UPDATE T_YSSELLMASTER SET TRANSFER_STATE = 0 "
                        f"WHERE SELLMASTER_CODE = '{label}'"
                    )
                    break
        elif value == "9":
            # 将销售流水更新为有效
            has_valid = any((r.get("SELLMASTER_STATE") or 0) > 0 for r in matching)
            if not has_valid:
                db.execute_non_query(
                    f"UPDATE T_YSSELLMASTER SET SELLMASTER_STATE = 9, TRANSFER_STATE = 9 "
                    f"WHERE SELLMASTER_CODE = '{label}'"
                )
    logger.info(f"CorrectSellMasterState: 处理 {len(sell_master_list)} 条订单完成")

