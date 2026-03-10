from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商家应收回款(PaymentConfirm) + 商家回款记录(RTPaymentRecord) + 备注说明(Remarks) 业务服务
对应 C#: PAYMENTCONFIRMHelper.cs / RTPAYMENTRECORDHelper.cs / REMARKSHelper.cs
"""
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from core.format_utils import format_int_date, format_row_dates
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS

# 日期字段（纯日期 yyyyMMdd）和时间字段（yyyyMMddHHmmss）
_RTP_DATE_FIELDS = {"OPERATE_DATE", "PAYMENTDATE"}
_RTP_DATETIME_FIELDS = {"CONFIRMDATE"}
_REMARKS_DATETIME_FIELDS = {"OPERATE_DATE"}


def _apply_kw_sort_page(rows, search_model, default_sort=""):
    """通用 keyword + 排序 + 分页"""
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            val = str(kw["Value"]).lower()
            rows = [r for r in rows if any(val in str(r.get(k, "")).lower() for k in keys)]

    sort_str = search_model.SortStr or default_sort
    if sort_str:
        sf = sort_str.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip().split(",")[0].strip()
        is_desc = "desc" in (sort_str or "").lower()
        try:
            rows.sort(key=lambda r: r.get(sf) or "", reverse=is_desc)
        except Exception:
            pass

    total = len(rows)
    pi = search_model.PageIndex or 0
    ps = search_model.PageSize or 0
    if pi > 0 and ps > 0:
        start = (pi - 1) * ps
        rows = rows[start:start + ps]
    return total, rows


# ===================================================================
# PaymentConfirm - POST GetList
# ===================================================================

def get_paymentconfirm_list(db: DatabaseHelper, search_model: SearchModel):
    """获取商家应收回款表列表（POST 版本）"""
    sp = search_model.SearchParameter or {}
    parts = []
    for k, v in sp.items():
        if k == "ACCOUNT_TYPE" or k in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if (search_model.QueryType or 0) == 0 and isinstance(v, str):
            parts.append(f"{k} LIKE '%{v}%'")
        elif isinstance(v, str):
            parts.append(f"{k} = '{v}'")
        else:
            parts.append(f"{k} = {v}")
    if sp.get("ACCOUNT_TYPE"):
        parts.append(f"ACCOUNT_TYPE IN ({sp['ACCOUNT_TYPE']})")
    where_sql = " WHERE " + " AND ".join(parts) if parts else ""

    rows = db.execute_query(f"SELECT * FROM T_PAYMENTCONFIRM{where_sql}")
    if not rows:
        return 0, []
    return _apply_kw_sort_page(rows, search_model, "ACCOUNT_DATE")


# ===================================================================
# PaymentConfirm - GET GetList (复杂查询 + summaryList)
# ===================================================================

def get_paymentconfirm_list_get(db: DatabaseHelper, merchants_id: str = "", serverpartshop_ids: str = "",
                                 businessproject_id: str = "", account_date: str = "",
                                 show_just_payable: int = 0, whole_account_type: int = 1,
                                 account_type: str = "", start_date: str = "", end_date: str = "",
                                 show_remarks: bool = False, sort_str: str = ""):
    """获取商家应收回款表列表（GET 版本 - 复杂查询）"""
    parts = []
    if merchants_id:
        parts.append(f"MERCHANTS_ID = {merchants_id}")
    if businessproject_id:
        parts.append(f"BUSINESSPROJECT_ID = {businessproject_id}")
    # 日期条件
    now_date = datetime.now().strftime("%Y%m%d")
    if not account_date:
        if not start_date and not end_date:
            parts.append(f"ACCOUNT_DATE <= {now_date}")
    else:
        parts.append(f"ACCOUNT_DATE <= {account_date}")
    if start_date:
        try:
            sd = datetime.strptime(start_date, "%Y/%m/%d" if "/" in start_date else "%Y-%m-%d").strftime("%Y%m%d")
            parts.append(f"ACCOUNT_DATE >= {sd}")
        except Exception:
            pass
    if end_date:
        try:
            ed = datetime.strptime(end_date, "%Y/%m/%d" if "/" in end_date else "%Y-%m-%d").strftime("%Y%m%d")
            parts.append(f"ACCOUNT_DATE <= {ed}")
        except Exception:
            pass
    if show_just_payable == 1:
        parts.append("CURRENTBALANCE > 0")
    if whole_account_type == 0:
        parts.append("ACCOUNT_TYPE <> 9000")
    if account_type:
        parts.append(f"ACCOUNT_TYPE IN ({account_type})")
    if show_remarks:
        parts.append("EXISTS (SELECT 1 FROM T_REMARKS WHERE T_PAYMENTCONFIRM.PAYMENTCONFIRM_ID = T_REMARKS.TABLE_ID AND TABLE_NAME = 'T_PAYMENTCONFIRM' AND REMARKS_CONTENT IS NOT NULL)")
    parts.append("PAYMENTCONFIRM_VALID = 1")
    where_sql = "WHERE " + " AND ".join(parts) if parts else ""

    rows = db.execute_query(f"SELECT * FROM T_PAYMENTCONFIRM {where_sql}")
    if not rows:
        return [], []

    # summaryList 计算
    summary_list = []
    account_types = set(str(r.get("ACCOUNT_TYPE", "")) for r in rows if r.get("ACCOUNT_TYPE"))
    receivable_amount = 0
    for at in sorted(account_types):
        at_rows = [r for r in rows if str(r.get("ACCOUNT_TYPE", "")) == at]
        # 应缴金额
        amt_sum = sum(float(r.get("ACCOUNT_AMOUNT") or 0) for r in at_rows)
        summary_list.append({"label": at, "value": amt_sum, "type": 1})
        receivable_amount += amt_sum
        # 已缴金额
        pay_sum = sum(float(r.get("ACTUAL_PAYMENT") or 0) for r in at_rows)
        summary_list.append({"label": at, "value": pay_sum, "type": 2})
        receivable_amount -= pay_sum
    summary_list.append({"label": "0", "value": receivable_amount, "type": 0})

    # 排序
    sf = sort_str or "ACCOUNT_DATE desc"
    is_desc = "desc" in sf.lower()
    field = sf.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
    try:
        rows.sort(key=lambda r: r.get(field) or "", reverse=is_desc)
    except Exception:
        pass

    return rows, summary_list


# ===================================================================
# PaymentConfirm - Detail
# ===================================================================

def get_paymentconfirm_detail(db: DatabaseHelper, pc_id: int):
    """获取商家应收回款表明细"""
    rows = db.execute_query(f"SELECT * FROM T_PAYMENTCONFIRM WHERE PAYMENTCONFIRM_ID = {pc_id}")
    return rows[0] if rows else None


# ===================================================================
# SeparatePaymentRecord (Controller: SeparatePaymentRecord)
# ===================================================================

def separate_payment_record(db: DatabaseHelper, payment_list: list):
    """保存商家回款拆分记录"""
    for item in payment_list:
        pc_id = item.get("PAYMENTCONFIRM_ID")
        if pc_id is None:
            continue
        # 获取当前记录
        rows = db.execute_query(f"SELECT * FROM T_PAYMENTCONFIRM WHERE PAYMENTCONFIRM_ID = {pc_id}")
        if not rows:
            continue
        current = rows[0]
        cur_actual = float(current.get("ACTUAL_PAYMENT") or 0)
        cur_amount = float(current.get("ACCOUNT_AMOUNT") or 0)
        new_payment = float(item.get("ACTUAL_PAYMENT") or 0)

        if cur_actual + new_payment > cur_amount:
            actual_payment = round(cur_amount - cur_actual, 2)
            new_actual = cur_amount
            new_balance = 0
        else:
            actual_payment = new_payment
            new_actual = cur_actual + new_payment
            new_balance = round(cur_amount - new_actual, 2)

        # 更新主记录
        db.execute_non_query(
            f"""UPDATE T_PAYMENTCONFIRM SET
                ACTUAL_PAYMENT = {new_actual},
                CURRENTBALANCE = {new_balance}
            WHERE PAYMENTCONFIRM_ID = {pc_id}""")

    return True


# ===================================================================
# SynchroPaymentConfirm
# ===================================================================

def synchro_paymentconfirm(db: DatabaseHelper, data: dict):
    """同步商家应收回款表"""
    pc_id = data.get("PAYMENTCONFIRM_ID")
    if pc_id is not None:
        check = db.execute_query(f"SELECT 1 FROM T_PAYMENTCONFIRM WHERE PAYMENTCONFIRM_ID = {pc_id}")
        if not check:
            return False
        set_parts = []
        for k, v in data.items():
            if k == "PAYMENTCONFIRM_ID":
                continue
            if v is None:
                set_parts.append(f"{k} = NULL")
            elif isinstance(v, str):
                set_parts.append(f"{k} = '{v}'")
            else:
                set_parts.append(f"{k} = {v}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE T_PAYMENTCONFIRM SET {', '.join(set_parts)} WHERE PAYMENTCONFIRM_ID = {pc_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_PAYMENTCONFIRM.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar("SELECT MAX(PAYMENTCONFIRM_ID) FROM T_PAYMENTCONFIRM") or 0) + 1
        data["PAYMENTCONFIRM_ID"] = new_id
        # 计算 CURRENTBALANCE
        if data.get("CURRENTBALANCE") is None:
            amt = float(data.get("ACCOUNT_AMOUNT") or 0)
            pay = float(data.get("ACTUAL_PAYMENT") or 0)
            data["CURRENTBALANCE"] = round(amt - pay, 2)

        cols, vals = [], []
        for k, v in data.items():
            if v is None:
                continue
            cols.append(k)
            vals.append(f"'{v}'" if isinstance(v, str) else str(v))
        db.execute_non_query(f"INSERT INTO T_PAYMENTCONFIRM ({', '.join(cols)}) VALUES ({', '.join(vals)})")
    return True


# ===================================================================
# DeletePaymentConfirm（软删除 VALID=0 + 级联）
# ===================================================================

def delete_paymentconfirm(db: DatabaseHelper, pc_id: int):
    """删除商家应收回款表（软删除+级联）"""
    rows = db.execute_query(f"SELECT * FROM T_PAYMENTCONFIRM WHERE PAYMENTCONFIRM_ID = {pc_id}")
    if not rows:
        return False, "删除失败，数据不存在！"
    current = rows[0]
    # 检查是否有关联还款记录
    related = db.execute_query(
        f"SELECT 1 FROM T_RTPAYMENTRECORD WHERE SEPARATE_ID = {pc_id} AND RTPAYMENTRECORD_VALID = 1")
    if related:
        return False, "已存在还款信息，暂不能删除！"

    db.execute_non_query(
        f"UPDATE T_PAYMENTCONFIRM SET PAYMENTCONFIRM_VALID = 0 WHERE PAYMENTCONFIRM_ID = {pc_id}")
    # 当款项为应收账款时，还原应收拆分数据状态
    try:
        account_type = int(current.get("ACCOUNT_TYPE") or 0)
        if account_type == 1000:
            bp_id = current.get("BUSINESSPROJECT_ID")
            account_date = current.get("ACCOUNT_DATE")
            if bp_id and account_date:
                db.execute_non_query(
                    f"UPDATE T_SHOPROYALTY SET SHOPROYALTY_STATE = 0 WHERE SHOPROYALTY_STATE = 1 AND BUSINESSPROJECT_ID = {bp_id} AND ENDDATE = TO_DATE('{account_date}','YYYY/MM/DD')")
                db.execute_non_query(
                    f"UPDATE T_REVENUECONFIRM SET REVENUE_VALID = 0 WHERE REVENUE_VALID = 1 AND BUSINESSPROJECT_ID = {bp_id} AND BUSINESS_ENDDATE = TO_DATE('{account_date}','YYYY/MM/DD')")
    except Exception:
        pass
    return True, ""


# ===================================================================
# ===================================================================
# RTPaymentRecord（商家回款记录）
# ===================================================================
# ===================================================================

def get_rtpaymentrecord_list(db: DatabaseHelper, search_model: SearchModel):
    """获取商家回款记录表列表（三表 JOIN）"""
    sp = search_model.SearchParameter or {}
    where_sql = ""
    for k, v in sp.items():
        if k in ("MERCHANTS_ID", "BUSINESSPROJECT_ID") or k in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if (search_model.QueryType or 0) == 0 and isinstance(v, str):
            where_sql += f" AND A.{k} LIKE '%{v}%'"
        elif isinstance(v, str):
            where_sql += f" AND A.{k} = '{v}'"
        else:
            where_sql += f" AND A.{k} = {v}"
    if sp.get("MERCHANTS_ID"):
        where_sql += f" AND B.MERCHANTS_ID = {sp['MERCHANTS_ID']}"
    if sp.get("BUSINESSPROJECT_ID"):
        where_sql += f" AND C.BUSINESSPROJECT_ID IN ({sp['BUSINESSPROJECT_ID']})"

    sql = f"""SELECT
            A.*,B.ACCOUNT_AMOUNT AS ACTUAL_PAYMENT,C.MERCHANTS_ID,
            C.ACCOUNT_AMOUNT,C.ACCOUNT_DATE,C.BUSINESSPROJECT_ID,
            C.BUSINESSPROJECT_NAME, C.SERVERPART_NAME
        FROM
            T_RTPAYMENTRECORD A,
            T_PAYMENTCONFIRM B,
            T_PAYMENTCONFIRM C
        WHERE
            A.PAYMENTCONFIRM_ID = B.PAYMENTCONFIRM_ID AND
            A.SEPARATE_ID = C.PAYMENTCONFIRM_ID{where_sql}"""

    rows = db.execute_query(sql)
    if not rows:
        return 0, []
    # 格式化日期字段（int → C# 格式字符串）
    for row in rows:
        format_row_dates(row, _RTP_DATE_FIELDS, _RTP_DATETIME_FIELDS)
        # ACCOUNT_DATE 从关联表来，是 C# 格式化的日期
        if isinstance(row.get("ACCOUNT_DATE"), int):
            row["ACCOUNT_DATE"] = format_int_date(row["ACCOUNT_DATE"])
    return _apply_kw_sort_page(rows, search_model)


def get_rtpaymentrecord_detail(db: DatabaseHelper, rtp_id: int):
    """获取商家回款记录表明细"""
    rows = db.execute_query(f"SELECT * FROM T_RTPAYMENTRECORD WHERE RTPAYMENTRECORD_ID = {rtp_id}")
    if not rows:
        return None
    row = rows[0]
    format_row_dates(row, _RTP_DATE_FIELDS, _RTP_DATETIME_FIELDS)
    return row


def synchro_rtpaymentrecord(db: DatabaseHelper, data: dict):
    """同步商家回款记录表"""
    rtp_id = data.get("RTPAYMENTRECORD_ID")
    if rtp_id is not None:
        check = db.execute_query(f"SELECT 1 FROM T_RTPAYMENTRECORD WHERE RTPAYMENTRECORD_ID = {rtp_id}")
        if not check:
            return False
        set_parts = []
        for k, v in data.items():
            if k == "RTPAYMENTRECORD_ID":
                continue
            if v is None:
                set_parts.append(f"{k} = NULL")
            elif isinstance(v, str):
                set_parts.append(f"{k} = '{v}'")
            else:
                set_parts.append(f"{k} = {v}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE T_RTPAYMENTRECORD SET {', '.join(set_parts)} WHERE RTPAYMENTRECORD_ID = {rtp_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_RTPAYMENTRECORD.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar("SELECT MAX(RTPAYMENTRECORD_ID) FROM T_RTPAYMENTRECORD") or 0) + 1
        data["RTPAYMENTRECORD_ID"] = new_id
        cols, vals = [], []
        for k, v in data.items():
            if v is None:
                continue
            cols.append(k)
            vals.append(f"'{v}'" if isinstance(v, str) else str(v))
        db.execute_non_query(f"INSERT INTO T_RTPAYMENTRECORD ({', '.join(cols)}) VALUES ({', '.join(vals)})")
    return True


def delete_rtpaymentrecord(db: DatabaseHelper, rtp_id: int):
    """删除商家回款记录表（软删除 + 级联更新 PAYMENTCONFIRM）"""
    rows = db.execute_query(f"SELECT * FROM T_RTPAYMENTRECORD WHERE RTPAYMENTRECORD_ID = {rtp_id}")
    if not rows:
        return False
    current = rows[0]
    db.execute_non_query(
        f"UPDATE T_RTPAYMENTRECORD SET RTPAYMENTRECORD_VALID = 0 WHERE RTPAYMENTRECORD_ID = {rtp_id}")
    # 级联更新 PAYMENTCONFIRM（SEPARATE_ID 和 PAYMENTCONFIRM_ID 各更新一次）
    separate_id = current.get("SEPARATE_ID")
    pc_id = current.get("PAYMENTCONFIRM_ID")
    update_sql = """UPDATE T_PAYMENTCONFIRM SET
            ACTUAL_PAYMENT = NVL((SELECT SUM(SEPARATE_AMOUNT) FROM T_RTPAYMENTRECORD WHERE SEPARATE_ID = T_PAYMENTCONFIRM.PAYMENTCONFIRM_ID AND RTPAYMENTRECORD_VALID = 1), 0),
            CURRENTBALANCE = ACCOUNT_AMOUNT - NVL((SELECT SUM(SEPARATE_AMOUNT) FROM T_RTPAYMENTRECORD WHERE SEPARATE_ID = T_PAYMENTCONFIRM.PAYMENTCONFIRM_ID AND RTPAYMENTRECORD_VALID = 1), 0)
        WHERE PAYMENTCONFIRM_ID = """
    try:
        if separate_id:
            db.execute_non_query(f"{update_sql}{separate_id}")
        if pc_id:
            db.execute_non_query(f"{update_sql}{pc_id}")
    except Exception as e:
        logger.debug(f"RTPaymentRecord 级联更新跳过: {e}")
    return True


# ===================================================================
# ===================================================================
# Remarks（备注说明表）
# ===================================================================
# ===================================================================

def get_remarks_list(db: DatabaseHelper, search_model: SearchModel):
    """获取备注说明表列表"""
    sp = search_model.SearchParameter or {}
    parts = []
    for k, v in sp.items():
        if k in SEARCH_PARAM_SKIP_FIELDS:
            continue
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        if (search_model.QueryType or 0) == 0 and isinstance(v, str):
            parts.append(f"{k} LIKE '%{v}%'")
        elif isinstance(v, str):
            parts.append(f"{k} = '{v}'")
        else:
            parts.append(f"{k} = {v}")
    where_sql = "WHERE " + " AND ".join(parts) if parts else ""

    rows = db.execute_query(f"SELECT * FROM T_REMARKS {where_sql}")
    if not rows:
        return 0, []
    # 格式化日期字段: OPERATE_DATE (int 20230526155250 → '2023/05/26 15:52:50')
    for row in rows:
        format_row_dates(row, set(), _REMARKS_DATETIME_FIELDS)
    return _apply_kw_sort_page(rows, search_model)


def get_remarks_detail(db: DatabaseHelper, remarks_id: int):
    """获取备注说明表明细"""
    rows = db.execute_query(f"SELECT * FROM T_REMARKS WHERE REMARKS_ID = {remarks_id}")
    if not rows:
        return None
    row = rows[0]
    # 格式化日期字段: OPERATE_DATE (int 20230526155250 → '2023/05/26 15:52:50')
    format_row_dates(row, set(), _REMARKS_DATETIME_FIELDS)
    return row


def synchro_remarks(db: DatabaseHelper, data: dict):
    """同步备注说明表"""
    r_id = data.get("REMARKS_ID")
    if r_id is not None:
        check = db.execute_query(f"SELECT 1 FROM T_REMARKS WHERE REMARKS_ID = {r_id}")
        if not check:
            return False
        set_parts = []
        for k, v in data.items():
            if k == "REMARKS_ID":
                continue
            if v is None:
                set_parts.append(f"{k} = NULL")
            elif isinstance(v, str):
                set_parts.append(f"{k} = '{v}'")
            else:
                set_parts.append(f"{k} = {v}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE T_REMARKS SET {', '.join(set_parts)} WHERE REMARKS_ID = {r_id}")
    else:
        try:
            new_id = db.execute_scalar("SELECT SEQ_REMARKS.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar("SELECT MAX(REMARKS_ID) FROM T_REMARKS") or 0) + 1
        data["REMARKS_ID"] = new_id
        cols, vals = [], []
        for k, v in data.items():
            if v is None:
                continue
            cols.append(k)
            vals.append(f"'{v}'" if isinstance(v, str) else str(v))
        db.execute_non_query(f"INSERT INTO T_REMARKS ({', '.join(cols)}) VALUES ({', '.join(vals)})")
    return True


def delete_remarks(db: DatabaseHelper, remarks_id: int):
    """删除备注说明表（软删除 STATUS=0）"""
    check = db.execute_query(f"SELECT 1 FROM T_REMARKS WHERE REMARKS_ID = {remarks_id}")
    if not check:
        return False
    db.execute_non_query(
        f"UPDATE T_REMARKS SET REMARKS_STATUS = 0 WHERE REMARKS_ID = {remarks_id}")
    return True
