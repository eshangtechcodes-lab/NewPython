from __future__ import annotations
# -*- coding: utf-8 -*-
"""
AuditController 业务服务（24 个接口）

CRUD 实体:
  YSABNORMALITY / ABNORMALAUDIT / CHECKACCOUNT / AUDITTASKS

散装接口:
  GetAuditList / GetAuditDetils / UpLoadAuditExplain
  GetCheckAccountReport / GetYsabnormalityReport / GetSpecialBehaviorReport
  GetAbnormalRateReport / GetAuditTasksReport / GetAuditTasksDetailList / IssueAuditTasks
"""
from typing import Tuple
from loguru import logger
from core.database import DatabaseHelper


# ============================================================
# 通用 CRUD
# ============================================================
def _generic_list(db, table, pk, search_model, extra_fields=None):
    pi = search_model.get("PageIndex", 1)
    ps = search_model.get("PageSize", 15)
    sd = search_model.get("SearchData") or search_model.get("SearchParameter") or {}
    wp, pa = [], []
    # 主键精确匹配
    if sd.get(pk):
        wp.append(f"{pk} = ?"); pa.append(sd[pk])
    for f in (extra_fields or []):
        if sd.get(f):
            wp.append(f"{f} = ?"); pa.append(sd[f])
    # SERVERPART_IDS 支持多个 ID（逗号分隔）
    sp_ids = sd.get("SERVERPART_IDS", "")
    if sp_ids:
        ids = [s.strip() for s in str(sp_ids).split(",") if s.strip()]
        if ids:
            wp.append(f"SERVERPART_ID IN ({','.join(ids)})")
    elif sd.get("SERVERPART_ID"):
        wp.append("SERVERPART_ID = ?"); pa.append(sd["SERVERPART_ID"])
    wc = " AND ".join(wp) if wp else "1=1"
    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}", pa) or 0
    off = (pi - 1) * ps
    # 达梦兼容分页（ROWNUM 子查询）
    paged_sql = f"""
        SELECT * FROM (
            SELECT A.*, ROWNUM AS RN__ FROM (
                SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC
            ) A WHERE ROWNUM <= {off + ps}
        ) WHERE RN__ > {off}
    """
    rows = db.fetch_all(paged_sql, pa, null_to_empty=False) or []
    for r in rows:
        r.pop("RN__", None)
    return rows, total

def _generic_detail(db, table, pk, pk_val):
    return db.fetch_one(f"SELECT * FROM {table} WHERE {pk} = ?", [pk_val])

def _generic_synchro(db, table, pk, data):
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

def _generic_delete(db, table, pk, status_field, pk_val):
    """软删除（C# 原逻辑: STATE = 0）"""
    c = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [pk_val])
    if not c or c == 0: return False
    db.execute(f"UPDATE {table} SET {status_field} = 0 WHERE {pk} = ?", [pk_val])
    return True


# ============================================================
# 实体定义
# ============================================================
ENTITIES = {
    "YSABNORMALITY": {"table": "T_YSABNORMALITY", "pk": "YSABNORMALITY_ID", "status": "YSABNORMALITY_STATE", "search_fields": ["SERVERPART_ID"]},
    "ABNORMALAUDIT": {"table": "T_ABNORMALAUDIT", "pk": "ABNORMALAUDIT_ID", "status": "ABNORMALAUDIT_STATE", "search_fields": ["SERVERPART_ID"]},
    "CHECKACCOUNT": {"table": "T_CHECKACCOUNT", "pk": "CHECKACCOUNT_ID", "status": "CHECKACCOUNT_STATE", "search_fields": ["SERVERPART_ID"]},
    "AUDITTASKS": {"table": "T_AUDITTASKS", "pk": "AUDITTASKS_ID", "status": "AUDITTASKS_STATE", "search_fields": ["SERVERPART_ID"]},
}

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

def get_ysabnormality_list(db, search_model: dict):
    """获取异常数据列表（带明细）"""
    logger.info("GetYSABNORMALITYList")
    return get_entity_list(db, "YSABNORMALITY", search_model)

def get_ysabnormality_detail_list(db, search_model: dict):
    """获取异常明细列表"""
    logger.info("GetYSABNORMALITYDETAILList")
    return _generic_list(db, "T_YSABNORMALITYDETAIL", "YSABNORMALITYDETAIL_ID", search_model)

def get_audit_list(db, search_model: dict):
    """获取审核列表"""
    logger.info("GetAuditList")
    try:
        wp = ["A.AUDITTASKS_STATE = 1"]
        sd = search_model.get("SearchData") or search_model.get("SearchParameter") or {}
        if sd.get("SERVERPART_ID"):
            wp.append(f"A.SERVERPART_ID = {sd['SERVERPART_ID']}")
        wc = " AND ".join(wp)
        sql = f"""SELECT A.*, B.SERVERPART_NAME
                 FROM T_AUDITTASKS A
                 JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
                 WHERE {wc} ORDER BY A.AUDITTASKS_ID DESC"""
        rows = db.fetch_all(sql) or []
        return rows, len(rows)
    except Exception as e:
        logger.error(f"GetAuditList 失败: {e}")
        return [], 0

def get_audit_details(db, search_model: dict):
    """获取审核详情"""
    logger.info("GetAuditDetils")
    return get_entity_list(db, "AUDITTASKS", search_model)

def upload_audit_explain(db, data: dict):
    """上传审核说明"""
    logger.info(f"UpLoadAuditExplain: {data}")
    return synchro_entity(db, "ABNORMALAUDIT", data)

def get_check_account_report(db, search_model: dict) -> list:
    """获取对账报表"""
    logger.info("GetCheckAccountReport")
    try:
        wp = ["CHECKACCOUNT_STATE = 1"]
        sd = search_model.get("SearchData") or search_model.get("SearchParameter") or {}
        if sd.get("SERVERPART_ID"):
            wp.append(f"SERVERPART_ID = {sd['SERVERPART_ID']}")
        wc = " AND ".join(wp)
        sql = f"SELECT * FROM T_CHECKACCOUNT WHERE {wc} ORDER BY CHECKACCOUNT_ID DESC"
        return db.fetch_all(sql) or []
    except Exception as e:
        logger.error(f"GetCheckAccountReport 失败: {e}")
        return []

def get_ysabnormality_report(db, search_model: dict) -> list:
    """获取异常报表"""
    logger.info("GetYsabnormalityReport")
    try:
        sql = "SELECT * FROM T_YSABNORMALITY WHERE YSABNORMALITY_STATE = 1 ORDER BY YSABNORMALITY_ID DESC"
        return db.fetch_all(sql) or []
    except Exception as e:
        logger.error(f"GetYsabnormalityReport 失败: {e}")
        return []

def get_special_behavior_report(db, search_model: dict) -> list:
    """获取特殊行为报表 — C# 中无对应实现（前端预留空接口）"""
    logger.info("GetSpecialBehaviorReport")
    return []

def get_abnormal_rate_report(db, search_model: dict) -> list:
    """获取异常率报表 — C# 中无对应实现（前端预留空接口）"""
    logger.info("GetAbnormalRateReport")
    return []

def get_audit_tasks_report(db, search_model: dict) -> list:
    """获取审核任务报表"""
    logger.info("GetAuditTasksReport")
    try:
        sql = "SELECT * FROM T_AUDITTASKS WHERE AUDITTASKS_STATE = 1 ORDER BY AUDITTASKS_ID DESC"
        return db.fetch_all(sql) or []
    except Exception as e:
        logger.error(f"GetAuditTasksReport 失败: {e}")
        return []

def get_audit_tasks_detail_list(db, search_model: dict):
    """获取审核任务明细列表"""
    logger.info("GetAuditTasksDetailList")
    return get_entity_list(db, "AUDITTASKS", search_model)

def issue_audit_tasks(db, data: dict):
    """下发审核任务"""
    logger.info(f"IssueAuditTasks: {data}")
    return synchro_entity(db, "AUDITTASKS", data)
