from __future__ import annotations
# -*- coding: utf-8 -*-
"""
合同备案管理业务服务（ContractController 专属）
对应 C# ContractController.cs 中 25 个非加密接口
使用 CONTRACT_STORAGE schema 下的表：
  - T_REGISTERCOMPACT（合同备案表）
  - T_REGISTERCOMPACTSUB（备案合同附属表）
  - T_RTREGISTERCOMPACT（经营合同-服务区关联表）
  - T_ATTACHMENT（附件表）
  - T_BUSINESSPROJECT（经营项目）
  - T_BUSINESSLOG（业务日志）
  - T_CONTRACTSYN（合同同步表）
"""
from typing import Optional
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# ===================================================================
# 通用辅助：标准 CRUD 工厂
# ===================================================================

def _std_get_list(db: DatabaseHelper, table_name: str, search_model: SearchModel,
                  pk_field: str, extra_where: str = "",
                  default_sort: str = "") -> tuple:
    """标准列表查询（SELECT *，带分页和 keyword 过滤）"""
    where_sql = extra_where
    sp = search_model.SearchParameter or {}

    # 常规字段 WHERE
    for key, value in sp.items():
        if value is None or (isinstance(value, str) and value.strip() == ""):
            continue
        prefix = " AND " if where_sql else " WHERE "
        if isinstance(value, str):
            where_sql += f"{prefix}{key} LIKE '%{value}%'"
        else:
            where_sql += f"{prefix}{key} = {value}"

    base_sql = f"SELECT * FROM {table_name}{where_sql}"

    # 排序
    sort = search_model.SortStr or default_sort
    if sort:
        base_sql += f" ORDER BY {sort}"

    # 总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total = db.execute_scalar(count_sql) or 0

    # 分页
    pi, ps = search_model.PageIndex, search_model.PageSize
    if pi and ps and ps < 999999:
        s, e = (pi - 1) * ps + 1, pi * ps
        paged = f"SELECT * FROM (SELECT A2.*, ROWNUM RN FROM ({base_sql}) A2 WHERE ROWNUM <= {e}) WHERE RN >= {s}"
        rows = db.execute_query(paged)
        for r in rows:
            r.pop("RN", None)
    else:
        rows = db.execute_query(base_sql)

    return int(total), rows


def _std_get_detail(db: DatabaseHelper, table_name: str, pk_field: str, pk_value) -> dict:
    """标准明细查询"""
    rows = db.execute_query(f"SELECT * FROM {table_name} WHERE {pk_field} = {pk_value}")
    return rows[0] if rows else {}


def _std_synchro(db: DatabaseHelper, table_name: str, pk_field: str,
                 data: dict, exclude_fields: list = None) -> tuple:
    """标准同步（新增/更新）"""
    exclude = set(exclude_fields or [])
    pk_value = data.get(pk_field)
    clean = {k: v for k, v in data.items() if k not in exclude and v is not None}

    if pk_value is not None:
        cnt = db.execute_scalar(f"SELECT COUNT(*) FROM {table_name} WHERE {pk_field} = {pk_value}")
        if cnt == 0:
            return False, None
        parts = [f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}"
                 for k, v in clean.items() if k != pk_field]
        if parts:
            db.execute_non_query(f"UPDATE {table_name} SET {', '.join(parts)} WHERE {pk_field} = {pk_value}")
    else:
        max_id = db.execute_scalar(f"SELECT MAX({pk_field}) FROM {table_name}")
        new_id = (max_id or 0) + 1
        data[pk_field] = new_id
        clean[pk_field] = new_id
        cols = [k for k in clean]
        vals = [f"'{v}'" if isinstance(v, str) else str(v) for v in clean.values()]
        db.execute_non_query(f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(vals)})")

    return True, data


def _std_delete(db: DatabaseHelper, table_name: str, pk_field: str, pk_value) -> bool:
    """标准真删除"""
    affected = db.execute_non_query(f"DELETE FROM {table_name} WHERE {pk_field} = {pk_value}")
    return affected > 0 if affected else False


# ===================================================================
# 1. RegisterCompact（合同备案表）CRUD
# ===================================================================

def get_registercompact_list(db: DatabaseHelper, search_model: SearchModel,
                              serverpart_ids: str = "",
                              serverpartshop_ids: str = "") -> tuple:
    """
    获取合同备案列表
    C# 核心 SQL：多表 JOIN（T_REGISTERCOMPACT A LEFT JOIN T_REGISTERCOMPACTSUB D
        JOIN T_RTREGISTERCOMPACT B JOIN T_SERVERPART C）+ WM_CONCAT + GROUP BY
    Python 简化版：直接查 T_REGISTERCOMPACT，关联数据在 Python 层拼接
    """
    sp = search_model.SearchParameter or {}
    where_sql = ""

    # SERVERPART_IDS 过滤
    ids = sp.get("SERVERPART_IDS") or serverpart_ids
    if ids and str(ids).strip():
        where_sql += f""" WHERE EXISTS (SELECT 1 FROM T_RTREGISTERCOMPACT B
            WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND B.SERVERPART_ID IN ({ids}))"""

    # SERVERPARTSHOP_IDS 过滤
    shop_ids = sp.get("SERVERPARTSHOP_IDS") or serverpartshop_ids
    if shop_ids and str(shop_ids).strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"""{prefix}EXISTS (SELECT 1 FROM T_RTBUSINESSPROJECT F, T_BUSINESSPROJECT G,
            T_SERVERPARTSHOP E
            WHERE A.REGISTERCOMPACT_ID = F.REGISTERCOMPACT_ID AND F.BUSINESSPROJECT_ID = G.BUSINESSPROJECT_ID AND
            E.SERVERPARTSHOP_ID IN ({shop_ids}))"""

    # 通用字段过滤（排除特殊字段）
    exclude = {"SERVERPART_IDS", "SERVERPARTSHOP_IDS", "SERVERPART_NAME",
               "BUSINESS_TYPE", "SETTLEMENT_CYCLE", "COMPACT_STARTDATE", "COMPACT_ENDDATE",
               "CLOSED_DATE", "Due_StartDate", "Due_EndDate", "AbnormalContract"}
    for key, value in sp.items():
        if key in exclude or value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        prefix = " AND " if where_sql else " WHERE "
        if isinstance(value, str):
            where_sql += f"{prefix}A.{key} LIKE '%{value}%'"
        else:
            where_sql += f"{prefix}A.{key} = {value}"

    # 日期范围
    if sp.get("COMPACT_STARTDATE"):
        prefix = " AND " if where_sql else " WHERE "
        date = str(sp["COMPACT_STARTDATE"]).split(" ")[0]
        where_sql += f"{prefix}A.COMPACT_ENDDATE >= TO_DATE('{date}','YYYY/MM/DD')"
    if sp.get("COMPACT_ENDDATE"):
        prefix = " AND " if where_sql else " WHERE "
        date = str(sp["COMPACT_ENDDATE"]).split(" ")[0]
        where_sql += f"{prefix}A.COMPACT_ENDDATE <= TO_DATE('{date}','YYYY/MM/DD')"

    base_sql = f"SELECT * FROM T_REGISTERCOMPACT A{where_sql}"

    # keyWord 过滤
    if search_model.keyWord:
        kw = search_model.keyWord.model_dump() if hasattr(search_model.keyWord, 'model_dump') else search_model.keyWord
        if kw and kw.get("Key") and kw.get("Value"):
            parts = [f"{k.strip()} LIKE '%{kw['Value']}%'" for k in kw["Key"].split(",") if k.strip()]
            if parts:
                prefix = " AND " if where_sql else " WHERE "
                base_sql += f"{prefix}({' OR '.join(parts)})"

    # 排序
    sort = search_model.SortStr or "OPERATE_DATE DESC"
    base_sql += f" ORDER BY {sort}"

    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total = db.execute_scalar(count_sql) or 0

    pi, ps = search_model.PageIndex, search_model.PageSize
    if pi and ps and ps < 999999:
        s, e = (pi - 1) * ps + 1, pi * ps
        paged = f"SELECT * FROM (SELECT A2.*, ROWNUM RN FROM ({base_sql}) A2 WHERE ROWNUM <= {e}) WHERE RN >= {s}"
        rows = db.execute_query(paged)
        for r in rows:
            r.pop("RN", None)
    else:
        rows = db.execute_query(base_sql)

    # 补充关联信息（服务区名称、关联合同数量等）
    for row in rows:
        rc_id = row.get("REGISTERCOMPACT_ID")
        if rc_id:
            try:
                rt_rows = db.execute_query(
                    f"""SELECT B.SERVERPART_ID, C.SERVERPART_NAME
                    FROM T_RTREGISTERCOMPACT B, T_SERVERPART C
                    WHERE B.SERVERPART_ID = C.SERVERPART_ID AND B.REGISTERCOMPACT_ID = {rc_id}""")
                row["SERVERPART_IDS"] = ",".join([str(r["SERVERPART_ID"]) for r in rt_rows])
                row["SERVERPART_NAME"] = ",".join([r["SERVERPART_NAME"] or "" for r in rt_rows])
            except:
                row["SERVERPART_IDS"] = ""
                row["SERVERPART_NAME"] = ""

    return int(total), rows


def get_registercompact_detail(db: DatabaseHelper, rc_id: int) -> dict:
    """获取合同备案明细（含服务区名称、日志）"""
    detail = _std_get_detail(db, "T_REGISTERCOMPACT", "REGISTERCOMPACT_ID", rc_id)
    if not detail:
        return {}

    # 补充服务区关联
    try:
        rt_rows = db.execute_query(
            f"""SELECT B.SERVERPART_ID, C.SERVERPART_NAME
            FROM T_RTREGISTERCOMPACT B, T_SERVERPART C
            WHERE B.SERVERPART_ID = C.SERVERPART_ID AND B.REGISTERCOMPACT_ID = {rc_id}""")
        detail["SERVERPART_IDS"] = ",".join([str(r["SERVERPART_ID"]) for r in rt_rows])
        detail["SERVERPART_NAME"] = ",".join([r["SERVERPART_NAME"] or "" for r in rt_rows])
    except:
        detail["SERVERPART_IDS"] = ""
        detail["SERVERPART_NAME"] = ""

    # 补充操作日志
    try:
        logs = db.execute_query(
            f"""SELECT * FROM T_BUSINESSLOG
            WHERE BUSINESSLOG_TYPE = 14 AND BUSINESS_ID = {rc_id}
            ORDER BY BUSINESSLOG_ID DESC""")
        detail["LogList"] = [l for l in logs if l.get("BUSINESSLOG_CONTENT") and
                             not str(l["BUSINESSLOG_CONTENT"]).endswith("：")]
    except:
        detail["LogList"] = []

    return detail


def synchro_registercompact(db: DatabaseHelper, data: dict) -> tuple:
    """同步合同备案表（简化版，不含历史备份和变更日志）"""
    exclude = ["SERVERPART_IDS", "SERVERPART_NAME", "SERVERPARTSHOP_IDS",
               "SERVERPARTSHOP_NAME", "COMPACT_CHILDTYPE", "FIRSTYEAR_RENT",
               "GUARANTEE_RATIO", "OPERATING_AREA", "SERVERPART_TYPE",
               "BUSINESS_TRADE", "BUSINESS_TYPE", "SETTLEMENT_MODES",
               "SETTLEMENT_CYCLE", "PROPERTY_FEE", "EQUIPMENT_DEPOSIT",
               "WATER_CHARGE", "ELECTRICITY_FEES", "OTHER_SCHARGE",
               "RELATE_COMPACT", "CLOSED_DATE", "LogList"]
    return _std_synchro(db, "T_REGISTERCOMPACT", "REGISTERCOMPACT_ID", data, exclude)


def delete_registercompact(db: DatabaseHelper, rc_id: int, force_delete: bool = False) -> tuple:
    """
    删除合同备案表（软删除 COMPACT_STATE=0）
    C# 逻辑：级联检查关联项目，有数据不允许删除（除非 ForceDelete）
    """
    if not force_delete:
        # 检查关联的经营项目
        cnt = db.execute_scalar(
            f"""SELECT COUNT(*) FROM T_RTBUSINESSPROJECT
            WHERE REGISTERCOMPACT_ID = {rc_id}""") or 0
        if cnt > 0:
            proj_cnt = db.execute_scalar(
                f"""SELECT COUNT(*) FROM T_BUSINESSPROJECT BP
                JOIN T_RTBUSINESSPROJECT RT ON BP.BUSINESSPROJECT_ID = RT.BUSINESSPROJECT_ID
                WHERE RT.REGISTERCOMPACT_ID = {rc_id} AND BP.PROJECT_VALID > 0""") or 0
            if proj_cnt > 0:
                return False, "删除失败，请删除合同关联的经营项目、拆分、往来款信息后再删除合同信息"

    # 软删除
    affected = db.execute_non_query(
        f"UPDATE T_REGISTERCOMPACT SET COMPACT_STATE = 0 WHERE REGISTERCOMPACT_ID = {rc_id}")
    if affected and affected > 0:
        # 清空附属合同的主合同内码
        db.execute_non_query(
            f"UPDATE T_REGISTERCOMPACT SET REGISTERCOMPACT_HOSTID = NULL WHERE REGISTERCOMPACT_HOSTID = {rc_id}")
        return True, ""
    return False, "删除失败，数据不存在"


# ===================================================================
# 2. RegisterCompactSub（备案合同附属表）CRUD
# ===================================================================

def get_registercompactsub_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    return _std_get_list(db, "T_REGISTERCOMPACTSUB", search_model, "REGISTERCOMPACTSUB_ID")


def get_registercompactsub_detail(db: DatabaseHelper,
                                   sub_id: int = None, rc_id: int = None) -> dict:
    """获取附属明细（支持 SubId 或 RegisterCompactId 查询）"""
    if sub_id:
        return _std_get_detail(db, "T_REGISTERCOMPACTSUB", "REGISTERCOMPACTSUB_ID", sub_id)
    elif rc_id:
        rows = db.execute_query(
            f"SELECT * FROM T_REGISTERCOMPACTSUB WHERE REGISTERCOMPACT_ID = {rc_id}")
        return rows[0] if rows else {}
    return {}


def synchro_registercompactsub(db: DatabaseHelper, data: dict) -> tuple:
    return _std_synchro(db, "T_REGISTERCOMPACTSUB", "REGISTERCOMPACTSUB_ID", data)


def delete_registercompactsub(db: DatabaseHelper, sub_id: int) -> bool:
    return _std_delete(db, "T_REGISTERCOMPACTSUB", "REGISTERCOMPACTSUB_ID", sub_id)


# ===================================================================
# 3. RTRegisterCompact（经营合同-服务区关联表）CRUD
# ===================================================================

def get_rtregistercompact_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    return _std_get_list(db, "T_RTREGISTERCOMPACT", search_model, "RTREGISTERCOMPACT_ID")


def get_rtregistercompact_detail(db: DatabaseHelper,
                                  rt_id: int = None, rc_id: int = None) -> dict:
    if rt_id:
        return _std_get_detail(db, "T_RTREGISTERCOMPACT", "RTREGISTERCOMPACT_ID", rt_id)
    elif rc_id:
        rows = db.execute_query(
            f"SELECT * FROM T_RTREGISTERCOMPACT WHERE REGISTERCOMPACT_ID = {rc_id}")
        return rows[0] if rows else {}
    return {}


def synchro_rtregistercompact_list(db: DatabaseHelper, data_list: list) -> bool:
    """同步经营合同服务区关联表（批量）"""
    flag = False
    for data in data_list:
        ok, _ = _std_synchro(db, "T_RTREGISTERCOMPACT", "RTREGISTERCOMPACT_ID", data)
        flag = ok
    return flag


def delete_rtregistercompact(db: DatabaseHelper, rt_id: int) -> bool:
    return _std_delete(db, "T_RTREGISTERCOMPACT", "RTREGISTERCOMPACT_ID", rt_id)


# ===================================================================
# 4. Attachment（附件表）CRUD
# ===================================================================

def get_attachment_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    return _std_get_list(db, "T_ATTACHMENT", search_model, "ATTACHMENT_ID")


def get_attachment_detail(db: DatabaseHelper, attachment_id: int) -> dict:
    return _std_get_detail(db, "T_ATTACHMENT", "ATTACHMENT_ID", attachment_id)


def synchro_attachment_list(db: DatabaseHelper, data_list: list) -> bool:
    flag = False
    for data in data_list:
        ok, _ = _std_synchro(db, "T_ATTACHMENT", "ATTACHMENT_ID", data)
        flag = ok
    return flag


def synchro_attachment(db: DatabaseHelper, data: dict) -> tuple:
    return _std_synchro(db, "T_ATTACHMENT", "ATTACHMENT_ID", data)


def delete_attachment(db: DatabaseHelper, attachment_id: int) -> bool:
    return _std_delete(db, "T_ATTACHMENT", "ATTACHMENT_ID", attachment_id)


# ===================================================================
# 5. 汇总查询（基于 C# ProjectSummaryHelper 的 Python SQL 实现）
# ===================================================================

from datetime import datetime
from dateutil.relativedelta import relativedelta


def _get_compact_type(db: DatabaseHelper, province_code: int) -> str:
    """
    获取省份对应的合同类型列表（逗号分隔）
    C# REGISTERCOMPACTHelper.GetCompactType → CoreDictionaryHelper.GetFieldEnumByField:
      1. 查 T_FIELDEXPLAIN 获取 FIELDEXPLAIN_ID (WHERE FIELDEXPLAIN_FIELD='COMPACT_CHARACTER')
      2. 查 T_FIELDENUM WHERE FIELDEXPLAIN_ID=? AND FIELDENUM_STATUS=1
         AND FIELDENUM_VALUE LIKE '省份前2位%'（安徽340000→'34%'）
      特殊：420000/451200 用 LENGTH(FIELDENUM_VALUE)=1
    """
    if not province_code:
        return ""
    try:
        # 获取 FIELDEXPLAIN_ID
        fe_rows = db.execute_query(
            "SELECT FIELDEXPLAIN_ID FROM T_FIELDEXPLAIN "
            "WHERE FIELDEXPLAIN_FIELD = 'COMPACT_CHARACTER'")
        if not fe_rows:
            return ""
        fe_id = fe_rows[0]["FIELDEXPLAIN_ID"]

        # 构建省份过滤条件
        pc = int(province_code)
        if pc in (420000, 451200):
            province_filter = "AND LENGTH(FIELDENUM_VALUE) = 1"
        else:
            prefix = str(pc)[:2]  # 取省份编码前 2 位
            province_filter = f"AND FIELDENUM_VALUE LIKE '{prefix}%'"

        rows = db.execute_query(
            f"SELECT FIELDENUM_VALUE FROM T_FIELDENUM "
            f"WHERE FIELDEXPLAIN_ID = {fe_id} AND FIELDENUM_STATUS IN (1) "
            f"{province_filter}")
        if rows:
            return ",".join([str(r["FIELDENUM_VALUE"]) for r in rows])
    except Exception as e:
        logger.warning(f"GetCompactType 查询失败: {e}")
    return ""


def _build_serverpart_where(serverpart_id, serverpartshop_ids, alias_prefix="A") -> str:
    """构建服务区/门店权限过滤 SQL"""
    w = ""
    if serverpartshop_ids and str(serverpartshop_ids).strip():
        w += f""" AND EXISTS (SELECT 1 FROM T_RTBUSINESSPROJECT C,
            T_BUSINESSPROJECT D, T_SERVERPARTSHOP E
            WHERE {alias_prefix}.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND C.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID
            AND ',' || D.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
            AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""
    elif serverpart_id:
        w += f""" AND EXISTS (SELECT 1 FROM T_RTREGISTERCOMPACT C
            WHERE {alias_prefix}.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND C.SERVERPART_ID IN ({serverpart_id}))"""
    return w


def _get_account_type_dict(db: DatabaseHelper) -> list:
    """
    获取 ACCOUNT_TYPE 字典列表（C# CoreDictionaryHelper.GetFieldEnumByField("ACCOUNT_TYPE")）
    返回 [{"value": "1000", "label": "保底租金"}, ...]
    排除特殊类型：1100/1200/1300/8000/9000
    """
    skip = {"1100", "1200", "1300", "8000", "9000"}
    try:
        fe_rows = db.execute_query(
            "SELECT FIELDEXPLAIN_ID FROM T_FIELDEXPLAIN "
            "WHERE FIELDEXPLAIN_FIELD = 'ACCOUNT_TYPE'")
        if not fe_rows:
            return []
        fe_id = fe_rows[0]["FIELDEXPLAIN_ID"]
        rows = db.execute_query(
            f"SELECT FIELDENUM_VALUE, FIELDENUM_NAME FROM T_FIELDENUM "
            f"WHERE FIELDEXPLAIN_ID = {fe_id} AND FIELDENUM_STATUS > 0 "
            f"ORDER BY FIELDENUM_VALUE")
        return [{"value": str(r["FIELDENUM_VALUE"]), "label": r.get("FIELDENUM_NAME", "")}
                for r in rows if str(r["FIELDENUM_VALUE"]) not in skip]
    except Exception as e:
        logger.warning(f"GetAccountTypeDict 查询失败: {e}")
        return []


def get_project_summary_info(db: DatabaseHelper, province_code: int = None,
                              serverpart_id: int = None,
                              serverpartshop_ids: str = "") -> dict:
    """
    获取项目欠款汇总信息（C# ProjectSummaryHelper.GetProjectSummaryInfo 的 Python 实现）
    返回结构：Contract_SignCount, Contract_Amount, Contractor_Count,
    NewlyContract_Count/Amount, ArrearageMerchant/Contract_Count, Arrearage_Amount,
    BusinessTypeSummaryList, ArrearageList
    """
    result = {}

    # 获取合同类型
    compact_type = _get_compact_type(db, province_code)
    if not compact_type:
        return result

    where_sql = f" AND A.COMPACT_TYPE IN ({compact_type})"
    where_sql += _build_serverpart_where(serverpart_id, serverpartshop_ids)

    try:
        # 1. 查询签约合同信息
        sql = f"""SELECT A.COMPACT_AMOUNT, A.REGISTERCOMPACT_ID, A.SECONDPART_ID,
                B.BUSINESS_TYPE, TO_CHAR(A.COMPACT_STARTDATE,'YYYY') AS OPERATE_DATE
            FROM T_REGISTERCOMPACT A, T_REGISTERCOMPACTSUB B
            WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID
            AND A.COMPACT_STATE = 1000{where_sql}"""
        dt_contract = db.execute_query(sql)

        # 合同签约金额
        contract_amount = sum(float(r.get("COMPACT_AMOUNT") or 0) for r in dt_contract)
        # 合同签约份数
        contract_sign_count = len(dt_contract)
        # 签约商家（去重）
        contractor_ids = set(r.get("SECONDPART_ID") for r in dt_contract if r.get("SECONDPART_ID"))
        contractor_count = len(contractor_ids)

        # 新增招商合同（今年）
        current_year = str(datetime.now().year)
        new_contracts = [r for r in dt_contract if str(r.get("OPERATE_DATE", "")) == current_year]
        newly_contract_count = len(new_contracts)
        newly_contract_amount = sum(float(r.get("COMPACT_AMOUNT") or 0) for r in new_contracts)

        # 2. 查询今年新增合同的应收金额
        where_sql2 = f" AND A.COMPACT_TYPE IN ({compact_type})"
        if serverpartshop_ids and str(serverpartshop_ids).strip():
            where_sql2 += f""" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP E
                WHERE ',' || D.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
                AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""
        elif serverpart_id:
            where_sql2 += f""" AND EXISTS (SELECT 1 FROM T_RTREGISTERCOMPACT E
                WHERE A.REGISTERCOMPACT_ID = E.REGISTERCOMPACT_ID
                AND E.SERVERPART_ID IN ({serverpart_id}))"""

        sql2 = f"""SELECT SUM(CASE WHEN D.BUSINESS_TYPE = 2000 THEN C.RENTFEE
                ELSE C.MINTURNOVER * C.GUARANTEERATIO / 100 END) AS EXPENSE_AMOUNT
            FROM T_REGISTERCOMPACT A, T_RTBUSINESSPROJECT B,
                T_SHOPROYALTY C, T_BUSINESSPROJECT D
            WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID
            AND B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND B.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID
            AND A.COMPACT_STARTDATE >= TRUNC(SYSDATE,'YYYY')
            AND C.ENDDATE >= TRUNC(SYSDATE,'YYYY')
            AND C.ENDDATE < TRUNC(ADD_MONTHS(SYSDATE,12),'YYYY')
            AND A.COMPACT_STATE = 1000 AND D.PROJECT_VALID > 0{where_sql2}"""
        newly_account_rows = db.execute_query(sql2)
        newly_account_amount = float(newly_account_rows[0].get("EXPENSE_AMOUNT") or 0) if newly_account_rows else 0

        # 3. 查询欠款项目
        now_str = datetime.now().strftime("%Y%m%d")
        where_sql3 = f" AND C.COMPACT_TYPE IN ({compact_type})"
        if serverpartshop_ids and str(serverpartshop_ids).strip():
            where_sql3 += f""" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP E
                WHERE ',' || B.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
                AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""
        elif serverpart_id:
            where_sql3 += f""" AND EXISTS (SELECT 1 FROM T_RTREGISTERCOMPACT E
                WHERE A.REGISTERCOMPACT_ID = E.REGISTERCOMPACT_ID
                AND E.SERVERPART_ID IN ({serverpart_id}))"""

        sql3 = f"""SELECT MIN(A.ACCOUNT_DATE) AS ACCOUNT_DATE,
                SUM(A.CURRENTBALANCE / 10000) AS CURRENTBALANCE,
                A.MERCHANTS_ID, A.BUSINESSPROJECT_ID, B.BUSINESS_TYPE
            FROM T_PAYMENTCONFIRM A, T_BUSINESSPROJECT B, T_REGISTERCOMPACT C
            WHERE A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
            AND A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND A.MERCHANTS_ID IS NOT NULL AND A.PAYMENTCONFIRM_VALID = 1
            AND A.CURRENTBALANCE <> 0 AND A.ACCOUNT_TYPE <> 9000
            AND B.PROJECT_VALID > 0 AND A.ACCOUNT_DATE <= {now_str}{where_sql3}
            GROUP BY A.MERCHANTS_ID, A.BUSINESSPROJECT_ID, B.BUSINESS_TYPE"""
        dt_arrearage = db.execute_query(sql3)

        # 欠款商家/项目数量/金额
        arr_merchant_ids = set(r.get("MERCHANTS_ID") for r in dt_arrearage)
        arr_project_ids = set(r.get("BUSINESSPROJECT_ID") for r in dt_arrearage)
        arrearage_amount = sum(float(r.get("CURRENTBALANCE") or 0) for r in dt_arrearage)

        result = {
            "Contract_SignCount": contract_sign_count,
            "Contract_Amount": round(contract_amount, 4),
            "Contractor_Count": contractor_count,
            "ArrearageMerchant_Count": len(arr_merchant_ids),
            "ArrearageContract_Count": len(arr_project_ids),
            "Arrearage_Amount": round(arrearage_amount, 6),
            "NewlyContract_Count": newly_contract_count,
            "NewlyContract_Amount": round(newly_contract_amount, 2),
            "NewlyAccount_Amount": round(newly_account_amount, 2),
        }

        # 4. 按经营模式分组统计 BusinessTypeSummaryList
        bts_list = []
        for bt in [1000, 2000]:
            bt_contracts = [r for r in dt_contract if r.get("BUSINESS_TYPE") == bt]
            bt_amount = sum(float(r.get("COMPACT_AMOUNT") or 0) for r in bt_contracts)
            bt_sign_count = len(bt_contracts)
            bt_contractor_ids = set(r.get("SECONDPART_ID") for r in bt_contracts if r.get("SECONDPART_ID"))

            bt_arr = [r for r in dt_arrearage if r.get("BUSINESS_TYPE") == bt]
            bt_arr_merchants = set(r.get("MERCHANTS_ID") for r in bt_arr)
            bt_arr_projects = set(r.get("BUSINESSPROJECT_ID") for r in bt_arr)
            bt_arr_amount = sum(float(r.get("CURRENTBALANCE") or 0) for r in bt_arr)

            bts_list.append({
                "BusinessType": bt,
                "Contract_SignCount": bt_sign_count,
                "Contract_Amount": round(bt_amount, 4),
                "Contractor_Count": len(bt_contractor_ids),
                "ArrearageMerchant_Count": len(bt_arr_merchants),
                "ArrearageContract_Count": len(bt_arr_projects),
                "Arrearage_Amount": round(bt_arr_amount, 6),
            })
        result["BusinessTypeSummaryList"] = bts_list

        # 5. 按逾期时间分段 ArrearageList
        now = datetime.now()
        m3 = int((now - relativedelta(months=3)).strftime("%Y%m%d"))
        m6 = int((now - relativedelta(months=6)).strftime("%Y%m%d"))
        arr_list = []
        for label, filter_fn in [
            ("3个月内", lambda r: int(r.get("ACCOUNT_DATE") or 0) >= m3),
            ("3-6个月", lambda r: m6 < int(r.get("ACCOUNT_DATE") or 0) < m3),
            ("≥6个月", lambda r: int(r.get("ACCOUNT_DATE") or 0) <= m6),
        ]:
            filtered = [r for r in dt_arrearage if filter_fn(r)]
            arr_list.append({
                "Overdue_Situation": label,
                "ArrearageMerchant_Count": len(set(r.get("MERCHANTS_ID") for r in filtered)),
                "ArrearageContract_Count": len(set(r.get("BUSINESSPROJECT_ID") for r in filtered)),
                "Arrearage_Amount": round(sum(float(r.get("CURRENTBALANCE") or 0) for r in filtered), 6),
            })
        result["ArrearageList"] = arr_list

    except Exception as e:
        logger.warning(f"GetProjectSummaryInfo 查询失败: {e}")
        import traceback; traceback.print_exc()

    return result


def get_contract_expired_info(db: DatabaseHelper, province_code: int = None,
                               serverpart_id: int = None,
                               serverpartshop_ids: str = "") -> dict:
    """
    获取合同到期信息（C# ProjectSummaryHelper.GetContractExpiredInfo 的 Python 实现）
    """
    result = {
        "Expired_Amount": 0, "UnExpired_Amount": 0, "Expired_HalfYearCount": 0,
        "Total_Amount": 0, "Paid_Amount": 0, "UnPaid_Amount": 0, "Complete_Degree": 0,
    }

    compact_type = _get_compact_type(db, province_code)
    if not compact_type:
        return result

    try:
        now_str = datetime.now().strftime("%Y%m%d")
        year_end = str(datetime.now().year) + "1231"
        where_sql = f" AND B.COMPACT_TYPE IN ({compact_type})"
        if serverpartshop_ids and str(serverpartshop_ids).strip():
            where_sql += f""" AND EXISTS (SELECT 1 FROM T_BUSINESSPROJECT D, T_SERVERPARTSHOP E
                WHERE D.PROJECT_VALID > 0 AND A.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID
                AND ',' || D.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
                AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""
        elif serverpart_id:
            where_sql += f""" AND EXISTS (SELECT 1 FROM T_RTREGISTERCOMPACT E
                WHERE A.REGISTERCOMPACT_ID = E.REGISTERCOMPACT_ID
                AND E.SERVERPART_ID IN ({serverpart_id}))"""

        # 查询合同金额汇总（已到期/未到期）
        sql = f"""SELECT CASE WHEN ACCOUNT_DATE <= {now_str} THEN 0 ELSE 1 END AS EXPIRED_FLAG,
                SUM(ACCOUNT_AMOUNT / 10000) AS ACCOUNT_AMOUNT,
                SUM(A.ACTUAL_PAYMENT / 10000) AS ACTUAL_PAYMENT
            FROM T_PAYMENTCONFIRM A, T_REGISTERCOMPACT B
            WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND B.COMPACT_STATE = 1000
            AND A.ACCOUNT_TYPE NOT IN (9000) AND MERCHANTS_ID IS NOT NULL
            AND A.PAYMENTCONFIRM_VALID = 1 AND A.ACCOUNT_DATE <= {year_end}{where_sql}
            GROUP BY CASE WHEN ACCOUNT_DATE <= {now_str} THEN 0 ELSE 1 END"""
        rows = db.execute_query(sql)
        for row in rows:
            flag = str(row.get("EXPIRED_FLAG", ""))
            if flag == "0":
                result["Expired_Amount"] = float(row.get("ACCOUNT_AMOUNT") or 0)
                result["Paid_Amount"] = float(row.get("ACTUAL_PAYMENT") or 0)
                result["UnPaid_Amount"] = result["Expired_Amount"] - result["Paid_Amount"]
            else:
                result["UnExpired_Amount"] = float(row.get("ACCOUNT_AMOUNT") or 0)

        result["Total_Amount"] = result["Expired_Amount"] + result["UnExpired_Amount"]
        if result["Expired_Amount"] != 0 and result["Paid_Amount"]:
            result["Complete_Degree"] = round(result["Paid_Amount"] / result["Expired_Amount"] * 100, 2)

        # 查询合同半年到期列表
        where_sql2 = f" AND A.COMPACT_TYPE IN ({compact_type})"
        where_sql2 += _build_serverpart_where(serverpart_id, serverpartshop_ids)

        sql2 = f"""SELECT CASE WHEN COMPACT_ENDDATE < ADD_MONTHS(TRUNC(SYSDATE),1) THEN 1
                WHEN COMPACT_ENDDATE > ADD_MONTHS(TRUNC(SYSDATE),1)
                    AND COMPACT_ENDDATE <= ADD_MONTHS(TRUNC(SYSDATE),3) THEN 2
                ELSE 3 END AS EXPIRED_SITUATION,
                COUNT(REGISTERCOMPACT_ID) AS CNT
            FROM T_REGISTERCOMPACT A
            WHERE COMPACT_STATE = 1000 AND COMPACT_ENDDATE > TRUNC(SYSDATE)
            AND COMPACT_ENDDATE <= ADD_MONTHS(TRUNC(SYSDATE),6){where_sql2}
            GROUP BY CASE WHEN COMPACT_ENDDATE < ADD_MONTHS(TRUNC(SYSDATE),1) THEN 1
                WHEN COMPACT_ENDDATE > ADD_MONTHS(TRUNC(SYSDATE),1)
                    AND COMPACT_ENDDATE <= ADD_MONTHS(TRUNC(SYSDATE),3) THEN 2 ELSE 3 END"""
        expired_rows = db.execute_query(sql2)

        half_year_list = []
        labels = {"1": "1个月内到期", "2": "1-3个月内到期", "3": "3-6个月内到期"}
        total_half_year = 0
        for row in sorted(expired_rows, key=lambda r: str(r.get("EXPIRED_SITUATION", ""))):
            sit = str(row.get("EXPIRED_SITUATION", ""))
            cnt = int(row.get("CNT") or 0)
            total_half_year += cnt
            half_year_list.append({
                "Expired_Situation": labels.get(sit, sit),
                "Expired_Count": cnt,
            })
        result["Expired_HalfYearCount"] = total_half_year
        result["ContractHalfYearListExpired"] = half_year_list

    except Exception as e:
        logger.warning(f"GetContractExpiredInfo 查询失败: {e}")
        import traceback; traceback.print_exc()

    return result


def get_project_yearly_arrearage(db: DatabaseHelper, province_code: int = None,
                                  serverpart_id: int = None,
                                  serverpartshop_ids: str = "") -> dict:
    """
    获取合同年度完成度信息（C# ProjectSummaryHelper.GetProjectYearlyArrearageList 的 Python 实现）
    """
    result = {"ProjectMonthlyCompleteList": [], "ProjectMonthlyUnpaidList": [],
              "ProjectCompleteDetailList": []}

    compact_type = _get_compact_type(db, province_code)
    if not compact_type:
        return result

    try:
        where_sql = f" AND B.COMPACT_TYPE IN ({compact_type})"
        if serverpartshop_ids and str(serverpartshop_ids).strip():
            where_sql += f""" AND EXISTS (SELECT 1 FROM T_BUSINESSPROJECT D, T_SERVERPARTSHOP E
                WHERE D.PROJECT_VALID > 0 AND A.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID
                AND ',' || D.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
                AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""
        elif serverpart_id:
            where_sql += f""" AND EXISTS (SELECT 1 FROM T_REGISTERCOMPACTSHOP C
                WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
                AND C.SERVERPART_ID IN ({serverpart_id}))"""

        current_year = datetime.now().year
        now_str = datetime.now().strftime("%Y%m%d")

        sql = f"""SELECT SUBSTR(MANAGEMONTH,1,4) AS MANAGEYEAR, ACCOUNT_TYPE, ACCOUNT_NAME,
                SUM(CASE WHEN ACCOUNT_DATE <= '{now_str}' THEN ACCOUNT_AMOUNT / 10000 END) AS EXPIRED_AMOUNT,
                SUM(CASE WHEN ACCOUNT_DATE > '{now_str}' THEN ACCOUNT_AMOUNT / 10000 END) AS UNEXPIRED_AMOUNT,
                SUM(ACCOUNT_AMOUNT / 10000) AS ACCOUNT_AMOUNT,
                SUM(ACTUAL_PAYMENT / 10000) AS ACTUAL_PAYMENT
            FROM T_PAYMENTCONFIRM A, T_REGISTERCOMPACT B
            WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND B.COMPACT_STATE = 1000
            AND PAYMENTCONFIRM_VALID = 1 AND ACCOUNT_TYPE <> 9000
            AND MERCHANTS_ID IS NOT NULL AND SUBSTR(MANAGEMONTH,1,4) <= '{current_year}'{where_sql}
            GROUP BY SUBSTR(MANAGEMONTH,1,4), ACCOUNT_TYPE, ACCOUNT_NAME"""
        dt = db.execute_query(sql)

        # 获取款项字典（C# 通过 keyValues 遍历只取已注册的类型）
        key_values = _get_account_type_dict(db)
        valid_types = {kv["value"] for kv in key_values}

        # 按年份分组
        years = sorted(set(r.get("MANAGEYEAR", "") for r in dt), reverse=True)
        yearly_list = []
        for year in years:
            year_data = {str(r.get("ACCOUNT_TYPE", "")): r for r in dt if r.get("MANAGEYEAR") == year}
            account_amount = 0
            payment_amount = 0
            detail_list = []
            # C# 遍历 keyValues 字典而非 SQL 结果
            for kv in key_values:
                at = kv["value"]
                row = year_data.get(at)
                pcd = {"Account_Type": int(at) if at.isdigit() else 0, "Account_Name": kv["label"]}
                if row:
                    aa = float(row.get("ACCOUNT_AMOUNT") or 0)
                    pa = float(row.get("ACTUAL_PAYMENT") or 0)
                    cd = round(pa / aa * 100, 2) if aa != 0 else 100
                    account_amount += aa
                    payment_amount += pa
                    pcd.update({"Account_Amount": round(aa, 4), "Payment_Amount": round(pa, 4), "Complete_Degree": cd})
                else:
                    pcd.update({"Account_Amount": 0, "Payment_Amount": 0, "Complete_Degree": 100})
                detail_list.append(pcd)

            unpaid = account_amount - payment_amount
            cd_year = round(payment_amount / account_amount * 100, 2) if account_amount != 0 else 100
            yearly_list.append({
                "Business_Year": int(year) if year.isdigit() else 0,
                "Account_Amount": round(account_amount, 4),
                "Payment_Amount": round(payment_amount, 4),
                "Unpaid_Amount": round(unpaid, 4),
                "Complete_Degree": cd_year,
                "ProjectCompleteDetailList": detail_list,
            })

        result["ProjectMonthlyCompleteList"] = yearly_list
        result["ProjectMonthlyUnpaidList"] = yearly_list

        # 总计明细（跨年份汇总按账目类型，只取字典中注册的类型）
        all_data = {}
        for r in dt:
            at = str(r.get("ACCOUNT_TYPE", ""))
            if at not in valid_types:
                continue
            if at not in all_data:
                all_data[at] = {"aa": 0, "pa": 0, "ea": 0, "ua": 0}
            all_data[at]["aa"] += float(r.get("ACCOUNT_AMOUNT") or 0)
            all_data[at]["pa"] += float(r.get("ACTUAL_PAYMENT") or 0)
            all_data[at]["ea"] += float(r.get("EXPIRED_AMOUNT") or 0)
            all_data[at]["ua"] += float(r.get("UNEXPIRED_AMOUNT") or 0)

        total_detail = []
        for kv in key_values:
            at = kv["value"]
            v = all_data.get(at, {"aa": 0, "pa": 0, "ea": 0, "ua": 0})
            cd = round(v["pa"] / v["aa"] * 100, 2) if v["aa"] != 0 else 100
            total_detail.append({
                "Account_Type": int(at) if at.isdigit() else 0,
                "Account_Name": kv["label"],
                "Account_Amount": round(v["aa"], 4),
                "Payment_Amount": round(v["pa"], 4),
                "Complete_Degree": cd,
                "Expired_Amount": round(v["ea"], 4),
                "UnExpired_Amount": round(v["ua"], 4),
            })
        result["ProjectCompleteDetailList"] = total_detail

    except Exception as e:
        logger.warning(f"GetProjectYearlyArrearage 查询失败: {e}")
        import traceback; traceback.print_exc()

    return result


def get_project_monthly_arrearage(db: DatabaseHelper, statistics_year: int,
                                   province_code: int = None,
                                   serverpart_id: int = None,
                                   serverpartshop_ids: str = "") -> dict:
    """
    获取合同月度完成度信息（C# ProjectSummaryHelper.GetProjectMonthlyArrearageList 的 Python 实现）
    """
    result = {"ProjectMonthlyCompleteList": [], "ProjectMonthlyUnpaidList": [],
              "ProjectCompleteDetailList": []}

    compact_type = _get_compact_type(db, province_code)
    if not compact_type:
        return result

    if not statistics_year:
        statistics_year = datetime.now().year

    try:
        where_sql = f" AND B.COMPACT_TYPE IN ({compact_type})"
        if serverpartshop_ids and str(serverpartshop_ids).strip():
            where_sql += f""" AND EXISTS (SELECT 1 FROM T_BUSINESSPROJECT D, T_SERVERPARTSHOP E
                WHERE D.PROJECT_VALID > 0 AND A.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID
                AND ',' || D.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
                AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""
        elif serverpart_id:
            where_sql += f""" AND EXISTS (SELECT 1 FROM T_REGISTERCOMPACTSHOP C
                WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
                AND C.SERVERPART_ID IN ({serverpart_id}))"""

        now_str = datetime.now().strftime("%Y%m%d")

        # 按月份查询
        sql = f"""SELECT MANAGEMONTH, ACCOUNT_TYPE, ACCOUNT_NAME,
                SUM(ACCOUNT_AMOUNT / 10000) AS ACCOUNT_AMOUNT,
                SUM(ACTUAL_PAYMENT / 10000) AS ACTUAL_PAYMENT
            FROM T_PAYMENTCONFIRM A, T_REGISTERCOMPACT B
            WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND B.COMPACT_STATE = 1000
            AND PAYMENTCONFIRM_VALID = 1 AND ACCOUNT_TYPE <> 9000
            AND MERCHANTS_ID IS NOT NULL
            AND SUBSTR(MANAGEMONTH,1,4) = '{statistics_year}'{where_sql}
            GROUP BY MANAGEMONTH, ACCOUNT_TYPE, ACCOUNT_NAME"""
        dt = db.execute_query(sql)

        # 获取款项字典（与 C# keyValues 遍历一致）
        key_values = _get_account_type_dict(db)

        # 按月份分组
        months = sorted(set(r.get("MANAGEMONTH", "") for r in dt))
        monthly_list = []
        for month in months:
            month_data = {str(r.get("ACCOUNT_TYPE", "")): r for r in dt if r.get("MANAGEMONTH") == month}
            account_amount = 0
            payment_amount = 0
            detail_list = []
            # C# 遍历 keyValues 字典
            for kv in key_values:
                at = kv["value"]
                row = month_data.get(at)
                pcd = {"Account_Type": int(at) if at.isdigit() else 0, "Account_Name": kv["label"]}
                if row:
                    aa = float(row.get("ACCOUNT_AMOUNT") or 0)
                    pa = float(row.get("ACTUAL_PAYMENT") or 0)
                    cd = round(pa / aa * 100, 2) if aa != 0 else 100
                    account_amount += aa
                    payment_amount += pa
                    pcd.update({"Account_Amount": round(aa, 4), "Payment_Amount": round(pa, 4), "Complete_Degree": cd})
                else:
                    pcd.update({"Account_Amount": 0, "Payment_Amount": 0, "Complete_Degree": 100})
                detail_list.append(pcd)

            unpaid = account_amount - payment_amount
            cd_month = round(payment_amount / account_amount * 100, 2) if account_amount != 0 else 100
            monthly_list.append({
                "Business_Month": month,
                "Account_Amount": round(account_amount, 4),
                "Payment_Amount": round(payment_amount, 4),
                "Unpaid_Amount": round(unpaid, 4),
                "Complete_Degree": cd_month,
                "ProjectCompleteDetailList": detail_list,
            })

        result["ProjectMonthlyCompleteList"] = monthly_list
        result["ProjectMonthlyUnpaidList"] = monthly_list

    except Exception as e:
        logger.warning(f"GetProjectMonthlyArrearage 查询失败: {e}")
        import traceback; traceback.print_exc()

    return result


# ===================================================================
# 6. AddContractSupplement / SynchroContractSyn
# ===================================================================

def add_contract_supplement(db: DatabaseHelper, data: dict) -> tuple:
    """增加合同补充协议（简化版）"""
    return _std_synchro(db, "T_REGISTERCOMPACT", "REGISTERCOMPACT_ID", data)


def synchro_contract_syn(db: DatabaseHelper, data_list: list) -> bool:
    """同步合同同步表（批量）"""
    flag = False
    for data in data_list:
        ok, _ = _std_synchro(db, "T_CONTRACTSYN", "CONTRACTSYN_ID", data)
        flag = ok
    return flag
