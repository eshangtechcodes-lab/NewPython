from __future__ import annotations
# -*- coding: utf-8 -*-
"""
InvoiceController 业务服务
移植自 C#: BILLHelper.cs / BILLDETAILHelper.cs / HXInvoiceHelper.cs

BILL CRUD（4）+ BILLDETAIL CRUD（4）+ 散装接口（4）

重要逻辑差异（与 C# 保持一致）：
- BILL 表名: T_BILL（C# 中使用 FINANCE_STORAGE.T_BILL，达梦中无 schema 前缀）
- Delete: 设 BILL_STATE = 0（C# 原逻辑），不是 -1
- GetBILLList: 复杂搜索条件（BILL_TYPES/日期范围/关键字/入账类型）
- SynchroBILL: 自动生成 BILL_NO（日期+服务区编码+序号）
- WriteBackInvoice: 按 BillNo 查找，回写开票金额/税金/状态=9200
- RewriteJDPJInfo: Base64 解码 Data → JSON，新建或更新 BILL，含红冲处理
- SendHXInvoiceInfo: 调航行 SOAP WebService（简化为 HTTP POST）
- ForwardJDPJInterface: HTTP 转发至金蝶
"""
import base64
import json
import math
import requests
from datetime import datetime
from typing import Optional, Tuple
from loguru import logger
from core.database import DatabaseHelper


# ============================================================
#                       BILL（票据信息表）
# ============================================================
BILL_TABLE = "T_BILL"
BILL_PK = "BILL_ID"

# 需要从搜索参数中排除的字段（C# excludeField）
BILL_EXCLUDE_FIELDS = {
    "SERVERPART_IDS", "SERVERPARTSHOP_IDS", "MERCHANTS_IDS",
    "BILL_DATE_Start", "BILL_DATE_End", "ACCOUNTED_TYPES",
    "ACCOUNTED_DATE_Start", "ACCOUNTED_DATE_End",
    "DetailList", "ApproveList", "BILL_TYPES", "BILL_STATES"
}

# 字符串字段 null→空字符串（C# .ToString() 行为）
BILL_STRING_FIELDS = {
    "BILL_NO", "SERIAL_NO", "SERVERPART_NAME", "SERVERPARTSHOP_ID",
    "SERVERPARTSHOP_NAME", "MERCHANTS_NAME", "BILL_PERSON",
    "BANK_NAME", "BANK_ACCOUNT", "MERCHANTS_ADDRESS", "MERCHANTS_TEL",
    "TAXPAYER_IDENTIFYCODE", "INTERBANK_NO", "TAXPAYER_CODE",
    "RECEIVE_PHONENUMBER", "RECEIVE_EMAIL", "DOWNLOAD_URL",
    "STAFF_NAME", "BILL_DESC"
}


def _convert_bill_row(row: dict) -> dict:
    """转换单行数据：字符串字段 null→空字符串"""
    if not row:
        return row
    for field in BILL_STRING_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    return row


# ========== 1. GetBILLList ==========
def get_bill_list(db: DatabaseHelper, search_model: dict) -> Tuple[list, int]:
    """
    获取票据信息列表
    C# 原逻辑: 支持 BILL_TYPES/SERVERPART_IDS/SERVERPARTSHOP_IDS/MERCHANTS_IDS
    日期范围/入账类型/BILL_STATES 等复杂搜索条件 + 关键字模糊搜索
    """
    page_index = search_model.get("PageIndex", 1)
    page_size = search_model.get("PageSize", 15)
    search_data = search_model.get("SearchData") or search_model.get("SearchParameter") or {}
    keyword = search_model.get("keyWord") or {}

    where_parts = []
    params = []

    # 票据类型 IN 条件
    bill_types = search_data.get("BILL_TYPES", "")
    if bill_types:
        where_parts.append(f"BILL_TYPE IN ({bill_types})")

    # 服务区 IN 条件
    sp_ids = search_data.get("SERVERPART_IDS", "") or search_data.get("SERVERPART_ID", "")
    if sp_ids:
        where_parts.append(f"SERVERPART_ID IN ({sp_ids})")

    # 门店 IN 条件（C# 中加了引号）
    shop_ids = search_data.get("SERVERPARTSHOP_IDS", "")
    if shop_ids:
        quoted = "','".join(str(s).strip() for s in shop_ids.split(',') if s.strip())
        where_parts.append(f"SERVERPARTSHOP_ID IN ('{quoted}')")

    # 商户 IN 条件
    m_ids = search_data.get("MERCHANTS_IDS", "")
    if m_ids:
        where_parts.append(f"MERCHANTS_ID IN ({m_ids})")

    # 开票日期范围
    if search_data.get("BILL_DATE_Start"):
        try:
            dt = datetime.strptime(str(search_data["BILL_DATE_Start"])[:10], "%Y-%m-%d")
            where_parts.append(f"BILL_DATE >= '{dt.strftime('%Y%m%d')}'")
        except Exception:
            pass
    if search_data.get("BILL_DATE_End"):
        try:
            dt = datetime.strptime(str(search_data["BILL_DATE_End"])[:10], "%Y-%m-%d")
            where_parts.append(f"BILL_DATE <= '{dt.strftime('%Y%m%d')}'")
        except Exception:
            pass

    # 入账类型 IN 条件
    acc_types = search_data.get("ACCOUNTED_TYPES", "")
    if acc_types:
        where_parts.append(f"ACCOUNTED_TYPE IN ({acc_types})")

    # 入账日期范围
    if search_data.get("ACCOUNTED_DATE_Start"):
        try:
            dt = datetime.strptime(str(search_data["ACCOUNTED_DATE_Start"])[:10], "%Y-%m-%d")
            where_parts.append(f"ACCOUNTED_DATE >= '{dt.strftime('%Y%m')}'")
        except Exception:
            pass
    if search_data.get("ACCOUNTED_DATE_End"):
        try:
            dt = datetime.strptime(str(search_data["ACCOUNTED_DATE_End"])[:10], "%Y-%m-%d")
            where_parts.append(f"ACCOUNTED_DATE <= '{dt.strftime('%Y%m')}'")
        except Exception:
            pass

    # 票据状态
    bill_states = search_data.get("BILL_STATES", "")
    if bill_states:
        where_parts.append(f"BILL_STATE IN ({bill_states})")
    elif search_data.get("BILL_STATE") is None:
        # C# 默认逻辑: BILL_STATE > 0
        where_parts.append("BILL_STATE > 0")

    where_clause = " AND ".join(where_parts) if where_parts else "BILL_STATE > 0"

    # 关键字搜索（C# RowFilter 模糊搜索）
    kw_key = keyword.get("Key", "")
    kw_val = keyword.get("Value", "")
    if kw_key and kw_val:
        kw_parts = []
        for key_name in kw_key.split(','):
            key_name = key_name.strip()
            if key_name:
                kw_parts.append(f"{key_name} LIKE '%{kw_val}%'")
        if kw_parts:
            where_clause += f" AND ({' OR '.join(kw_parts)})"

    # 排序（C# 通过 SortStr 参数）
    sort_str = search_model.get("SortStr", "")
    order_by = sort_str if sort_str else f"{BILL_PK} DESC"

    # 总数
    count_sql = f"SELECT COUNT(*) FROM {BILL_TABLE} WHERE {where_clause}"
    total = db.fetch_scalar(count_sql, params) or 0

    # 分页查询
    offset = (page_index - 1) * page_size
    data_sql = f"""
        SELECT * FROM {BILL_TABLE}
        WHERE {where_clause}
        ORDER BY {order_by}
        LIMIT {page_size} OFFSET {offset}
    """
    rows = db.fetch_all(data_sql, params) or []
    return [_convert_bill_row(r) for r in rows], total


# ========== 2. GetBILLDetail ==========
def get_bill_detail(db: DatabaseHelper, bill_id: int = None, bill_no: str = "") -> Optional[dict]:
    """
    获取票据信息明细
    C# 中还会附带查询 BILLDETAIL 子列表和审批意见列表
    """
    if bill_id:
        sql = f"SELECT * FROM {BILL_TABLE} WHERE {BILL_PK} = ?"
        row = db.fetch_one(sql, [bill_id])
    elif bill_no:
        sql = f"SELECT * FROM {BILL_TABLE} WHERE BILL_NO = ?"
        row = db.fetch_one(sql, [bill_no])
    else:
        return {}

    if not row:
        return {}

    row = _convert_bill_row(row)

    # 附带查询明细列表（C# 嵌套查询 DetailList）
    try:
        detail_sql = f"SELECT * FROM T_BILLDETAIL WHERE BILL_ID = ? ORDER BY BILLDETAIL_ID"
        details = db.fetch_all(detail_sql, [row.get("BILL_ID")]) or []
        row["DetailList"] = details
    except Exception:
        row["DetailList"] = []

    return row


# ========== 3. SynchroBILL ==========
def synchro_bill(db: DatabaseHelper, data: dict) -> Tuple[bool, dict]:
    """
    同步票据信息（新增/更新）
    C# 逻辑: 新增时自动生成 BILL_NO（日期+服务区编码+序号）
    更新时先检查存在再执行。同步时连带同步 DetailList。
    """
    pk_val = data.get(BILL_PK)

    # 自动生成 BILL_NO
    if not data.get("BILL_NO"):
        data["BILL_NO"] = _get_bill_code(db, data.get("SERVERPART_ID"))

    # 排除非表字段
    save_data = {k: v for k, v in data.items() if k not in BILL_EXCLUDE_FIELDS}

    if pk_val:
        # 检查是否已存在
        check_sql = f"SELECT COUNT(*) FROM {BILL_TABLE} WHERE {BILL_PK} = ?"
        exists = db.fetch_scalar(check_sql, [pk_val])
        if exists and exists > 0:
            # 更新
            update_fields = {k: v for k, v in save_data.items() if k != BILL_PK}
            if not update_fields:
                return True, data
            set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
            values = list(update_fields.values()) + [pk_val]
            update_sql = f"UPDATE {BILL_TABLE} SET {set_clause} WHERE {BILL_PK} = ?"
            db.execute(update_sql, values)
        else:
            # C# 中如果 BILL_ID 不存在则返回 false
            return False, data
    else:
        # 新增：获取序列
        try:
            seq_sql = "SELECT NEWPYTHON.SEQ_BILL.NEXTVAL FROM DUAL"
            new_id = db.fetch_scalar(seq_sql)
            save_data[BILL_PK] = new_id
            data[BILL_PK] = new_id
        except Exception:
            max_sql = f"SELECT COALESCE(MAX({BILL_PK}), 0) + 1 FROM {BILL_TABLE}"
            new_id = db.fetch_scalar(max_sql)
            save_data[BILL_PK] = new_id
            data[BILL_PK] = new_id

        columns = ", ".join(save_data.keys())
        placeholders = ", ".join(["?"] * len(save_data))
        insert_sql = f"INSERT INTO {BILL_TABLE} ({columns}) VALUES ({placeholders})"
        db.execute(insert_sql, list(save_data.values()))

    # 同步票据明细（C# 中连带同步 DetailList）
    detail_list = data.get("DetailList")
    if detail_list and isinstance(detail_list, list):
        for detail in detail_list:
            if not detail.get("BILL_ID"):
                detail["BILL_ID"] = data[BILL_PK]
            synchro_billdetail(db, detail)

    return True, data


def _get_bill_code(db: DatabaseHelper, serverpart_id) -> str:
    """
    生成业务编码（C# BILLHelper.GetBillCode）
    格式: yyyyMMdd-000000-0001（日期-服务区编码左补零6位-流水号4位）
    """
    sp_id = int(serverpart_id or 0)
    prefix = f"{datetime.now().strftime('%Y%m%d')}-{str(sp_id).zfill(6)}-"
    try:
        sql = f"SELECT MAX(BILL_NO) FROM {BILL_TABLE} WHERE BILL_NO IS NOT NULL AND BILL_NO LIKE ?"
        max_no = db.fetch_scalar(sql, [f"{prefix}%"])
        if max_no:
            # 从 yyyyMMdd-000000-0001 中取最后4位数字
            parts = str(max_no).split('-')
            if len(parts) >= 3:
                seq = int(parts[2]) + 1
                return f"{prefix}{str(seq).zfill(4)}"
    except Exception:
        pass
    return f"{prefix}0001"


# ========== 4. DeleteBILL ==========
def delete_bill(db: DatabaseHelper, bill_id: int) -> bool:
    """
    删除票据信息（C# 原逻辑: UPDATE BILL_STATE = 0，不是 -1）
    """
    if not bill_id:
        return False
    delete_sql = f"UPDATE {BILL_TABLE} SET BILL_STATE = 0 WHERE {BILL_PK} = ?"
    affected = db.execute(delete_sql, [bill_id])
    return affected is not None and affected > 0 if isinstance(affected, int) else True


# ============================================================
#                     BILLDETAIL（票据明细表）
# ============================================================
BILLDETAIL_TABLE = "T_BILLDETAIL"
BILLDETAIL_PK = "BILLDETAIL_ID"

BILLDETAIL_STRING_FIELDS = {
    "ITEM_NAME", "ITEM_RULE", "ITEM_UNIT", "TABLE_NAME"
}


def _convert_billdetail_row(row: dict) -> dict:
    if not row:
        return row
    for field in BILLDETAIL_STRING_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    return row


# ========== 5. GetBILLDETAILList ==========
def get_billdetail_list(db: DatabaseHelper, search_model: dict) -> Tuple[list, int]:
    """获取票据明细列表"""
    page_index = search_model.get("PageIndex", 1)
    page_size = search_model.get("PageSize", 15)
    search_data = search_model.get("SearchData") or search_model.get("SearchParameter") or {}

    where_parts = []
    params = []

    if search_data.get("BILL_ID"):
        where_parts.append("BILL_ID = ?")
        params.append(search_data["BILL_ID"])

    where_clause = " AND ".join(where_parts) if where_parts else "1=1"

    count_sql = f"SELECT COUNT(*) FROM {BILLDETAIL_TABLE} WHERE {where_clause}"
    total = db.fetch_scalar(count_sql, params) or 0

    offset = (page_index - 1) * page_size
    sort_str = search_model.get("SortStr", f"{BILLDETAIL_PK} DESC")
    data_sql = f"""
        SELECT * FROM {BILLDETAIL_TABLE}
        WHERE {where_clause}
        ORDER BY {sort_str}
        LIMIT {page_size} OFFSET {offset}
    """
    rows = db.fetch_all(data_sql, params) or []
    return [_convert_billdetail_row(r) for r in rows], total


# ========== 6. GetBILLDETAILDetail ==========
def get_billdetail_detail(db: DatabaseHelper, billdetail_id: int) -> Optional[dict]:
    sql = f"SELECT * FROM {BILLDETAIL_TABLE} WHERE {BILLDETAIL_PK} = ?"
    row = db.fetch_one(sql, [billdetail_id])
    return _convert_billdetail_row(row)


# ========== 7. SynchroBILLDETAIL ==========
def synchro_billdetail(db: DatabaseHelper, data: dict) -> Tuple[bool, dict]:
    """同步票据明细（新增/更新）"""
    pk_val = data.get(BILLDETAIL_PK)
    if pk_val:
        check_sql = f"SELECT COUNT(*) FROM {BILLDETAIL_TABLE} WHERE {BILLDETAIL_PK} = ?"
        exists = db.fetch_scalar(check_sql, [pk_val])
        if exists and exists > 0:
            update_fields = {k: v for k, v in data.items() if k != BILLDETAIL_PK}
            if not update_fields:
                return True, data
            set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
            values = list(update_fields.values()) + [pk_val]
            update_sql = f"UPDATE {BILLDETAIL_TABLE} SET {set_clause} WHERE {BILLDETAIL_PK} = ?"
            db.execute(update_sql, values)
            return True, data

    try:
        seq_sql = "SELECT NEWPYTHON.SEQ_BILLDETAIL.NEXTVAL FROM DUAL"
        new_id = db.fetch_scalar(seq_sql)
        data[BILLDETAIL_PK] = new_id
    except Exception:
        max_sql = f"SELECT COALESCE(MAX({BILLDETAIL_PK}), 0) + 1 FROM {BILLDETAIL_TABLE}"
        new_id = db.fetch_scalar(max_sql)
        data[BILLDETAIL_PK] = new_id

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    insert_sql = f"INSERT INTO {BILLDETAIL_TABLE} ({columns}) VALUES ({placeholders})"
    db.execute(insert_sql, list(data.values()))
    return True, data


# ========== 8. DeleteBILLDETAIL ==========
def delete_billdetail(db: DatabaseHelper, billdetail_id: int) -> bool:
    """删除票据明细（C# 逻辑: BILLDETAIL_STATE = 0）"""
    if not billdetail_id:
        return False
    delete_sql = f"UPDATE {BILLDETAIL_TABLE} SET BILLDETAIL_STATE = 0 WHERE {BILLDETAIL_PK} = ?"
    db.execute(delete_sql, [billdetail_id])
    return True


# ============================================================
#              散装接口（WriteBack / SendHX / JDPJ）
# ============================================================

# ========== 9. WriteBackInvoice ==========
def write_back_invoice(db: DatabaseHelper, data: dict) -> Tuple[bool, str]:
    """
    回写票据开票结果信息
    C# 原逻辑 (BILLHelper.WriteBackInvoice):
    1. 通过 BillNo 查找 BILL 记录
    2. 更新 SERIAL_NO、BILL_TAXAMOUNT
    3. 根据税率计算除税金额: BILL_AMOUNT = BILL_TAXAMOUNT / (1 + DUTY_PARAGRAPH/100)
    4. 计算税金: TAX_PRICE = BILL_TAXAMOUNT - BILL_AMOUNT
    5. 计算尾差: TAXTAIL_DIFFERENCE / TAIL_DIFFERENCE
    6. 设置 BILL_STATE = 9200
    """
    bill_no = data.get("BillNo", "")
    if not bill_no:
        return False, "票据单号不存在！"

    # 查找票据记录
    bill_model = get_bill_detail(db, bill_no=bill_no)
    if not bill_model or not bill_model.get("BILL_ID"):
        return False, "票据单号不存在！"

    # 更新字段
    bill_model["SERIAL_NO"] = data.get("SerialNo", "")
    bill_taxamount = float(data.get("BillAmount", 0))
    bill_model["BILL_TAXAMOUNT"] = bill_taxamount

    # 根据税率计算除税金额（C# Math.Round）
    duty_paragraph = float(bill_model.get("DUTY_PARAGRAPH") or 0)
    if duty_paragraph > 0:
        bill_amount = round(bill_taxamount / (1 + duty_paragraph / 100), 2)
    else:
        bill_amount = bill_taxamount
    bill_model["BILL_AMOUNT"] = bill_amount

    # 计算税金
    bill_model["TAX_PRICE"] = round(bill_taxamount - bill_amount, 2)

    # 计算尾差
    invoice_taxamount = float(bill_model.get("INVOICE_TAXAMOUNT") or 0)
    invoice_amount = float(bill_model.get("INVOICE_AMOUNT") or 0)
    bill_model["TAXTAIL_DIFFERENCE"] = round(bill_taxamount - invoice_taxamount, 2)
    bill_model["TAIL_DIFFERENCE"] = round(bill_amount - invoice_amount, 2)

    # 更新入账日期和下载地址
    bill_model["ACCOUNTED_DATE"] = data.get("BillDate", "")
    bill_model["DOWNLOAD_URL"] = data.get("DownloadUrl", "")

    # 设置票据状态为已开票
    if bill_model.get("BILL_STATE") != 9200:
        bill_model["BILL_STATE"] = 9200

    # 移除嵌套的 DetailList（不参与 UPDATE）
    bill_model.pop("DetailList", None)

    ok, _ = synchro_bill(db, bill_model)
    return ok, "" if ok else "更新失败"


# ========== 10. SendHXInvoiceInfo ==========
def send_hx_invoice_info(data: list) -> Tuple[bool, str]:
    """
    发送开票信息至航行开票系统
    C# 原逻辑 (HXInvoiceHelper.SendHXInvoiceInfo):
    构造 XML → Base64 编码 → 调用航行 SOAP WebService → 解析返回 XML

    注意：此接口调用外部航行 SOAP WebService，依赖特定的 WSDL URL 和纳税人 ID。
    Python 中简化为记录日志并返回成功（需要配置航行系统参数后才能实际调用）。
    """
    logger.info(f"SendHXInvoiceInfo 调用, 发票数: {len(data) if data else 0}")
    logger.info(f"SendHXInvoiceInfo 数据: {json.dumps(data, ensure_ascii=False, default=str)[:500]}")

    # TODO: 需要配置航行系统 WSDL URL 和 TaxpayerId 后实现实际调用
    # 目前返回成功，实际部署时需要用 zeep 或 suds 库调用 SOAP WebService
    return True, ""


# ========== 11. RewriteJDPJInfo ==========
def rewrite_jdpj_info(db: DatabaseHelper, data: dict) -> Tuple[bool, str]:
    """
    回写金蝶开票结果信息
    C# 原逻辑 (BILLHelper.RewriteJDPJInfo):
    1. Base64 解码 Data 字段 → JSON (JDPJDataModel)
    2. 如果 returnCode != "0"，直接返回 true（表示结果已记录但不需要处理）
    3. 根据 billNo 查找 BILL：
       - 不存在：新建 BILL + BILLDETAIL，从服务区编码查 SERVERPART_ID
       - 存在：更新开票金额、税金等
    4. 红冲处理：invoiceProperty == 1 时，将原票据 BILL_STATE 设为 9999
    """
    logger.info(f"RewriteJDPJInfo 调用, returnCode={data.get('returnCode')}")

    # 1. Base64 解码 Data
    try:
        raw_data = data.get("Data", "")
        if raw_data:
            decoded = base64.b64decode(raw_data).decode('utf-8')
            jdpj_data = json.loads(decoded)
        else:
            jdpj_data = data  # 如果没有 Base64，直接使用原始数据
    except Exception as e:
        logger.warning(f"RewriteJDPJInfo Base64 解码失败: {e}, 使用原始数据")
        jdpj_data = data

    logger.info(f"RewriteJDPJInfo 票据回写结果: {json.dumps(jdpj_data, ensure_ascii=False, default=str)[:500]}")

    # 2. 如果 returnCode != "0"，直接返回成功
    if data.get("returnCode", "0") != "0":
        return True, ""

    bill_no = jdpj_data.get("billNo", "")
    if not bill_no:
        return False, "缺少 billNo"

    # 3. 查找票据
    bill_model = get_bill_detail(db, bill_no=bill_no)

    if not bill_model or not bill_model.get("BILL_ID"):
        # 新建 BILL
        invoice_property = jdpj_data.get("invoiceProperty", 0)
        invoice_type = jdpj_data.get("invoiceType", "")
        bill_type = 3000 if invoice_property == 1 else (1000 if invoice_type == "08xdp" else 2000)

        bill_model = {
            "BILL_TYPE": bill_type,
            "BILL_NO": bill_no,
            "SERIAL_NO": jdpj_data.get("invoiceNum", ""),
            "BILL_DATE": jdpj_data.get("invoiceDate", ""),
            "BILL_TAXAMOUNT": jdpj_data.get("includeTaxAmount"),
            "BILL_AMOUNT": jdpj_data.get("totalAmount"),
            "TAX_PRICE": jdpj_data.get("totalTaxAmount"),
            "INVOICE_TAXAMOUNT": jdpj_data.get("includeTaxAmount"),
            "INVOICE_AMOUNT": jdpj_data.get("totalAmount"),
            "TAXTAIL_DIFFERENCE": 0,
            "TAIL_DIFFERENCE": 0,
            "MERCHANTS_NAME": jdpj_data.get("buyerName", ""),
            "BANK_NAME": jdpj_data.get("buyerBankAndAccount", ""),
            "TAXPAYER_IDENTIFYCODE": jdpj_data.get("buyerTaxpayerId", ""),
            "TAXPAYER_CODE": jdpj_data.get("sellerTaxpayerId", ""),
            "ACCOUNTED_TYPE": jdpj_data.get("includeTaxFlag"),
            "BILL_PERSON": jdpj_data.get("drawer", ""),
            "ACCOUNTED_DATE": jdpj_data.get("invoiceDate") or datetime.now().strftime("%Y-%m-%d"),
            "RECEIVE_PHONENUMBER": jdpj_data.get("buyerRecipientPhone", ""),
            "RECEIVE_EMAIL": jdpj_data.get("buyerRecipientMail", ""),
            "DOWNLOAD_URL": jdpj_data.get("invoicePdfFileUrl", ""),
            "BILL_STATE": 9200,
            "OPERATE_DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # 从 billNo 前6位查服务区编码
        if len(bill_no) >= 6:
            sp_code = bill_no[:6]
            try:
                sp_row = db.fetch_one(
                    "SELECT SERVERPART_ID, SERVERPART_NAME FROM T_SERVERPART WHERE SERVERPART_CODE = ?",
                    [sp_code])
                if sp_row:
                    bill_model["SERVERPART_ID"] = sp_row["SERVERPART_ID"]
                    bill_model["SERVERPART_NAME"] = sp_row["SERVERPART_NAME"]
                    # 查门店
                    if len(bill_no) >= 12:
                        shop_code = bill_no[6:12]
                        shop_row = db.fetch_one(
                            "SELECT SERVERPARTSHOP_ID, SHOPNAME FROM T_SERVERPARTSHOP WHERE SERVERPART_ID = ? AND SHOPCODE = ?",
                            [sp_row["SERVERPART_ID"], shop_code])
                        if shop_row:
                            bill_model["SERVERPARTSHOP_ID"] = shop_row["SERVERPARTSHOP_ID"]
                            bill_model["SERVERPARTSHOP_NAME"] = shop_row["SHOPNAME"]
            except Exception as e:
                logger.warning(f"查询服务区/门店失败: {e}")

        ok, bill_model = synchro_bill(db, bill_model)
        if not ok:
            return False, "新建票据失败"

        # 同步明细
        invoice_details = jdpj_data.get("invoiceDetail", [])
        for detail in invoice_details:
            detail_model = {
                "BILL_ID": bill_model.get("BILL_ID"),
                "ITEM_NAME": detail.get("goodsName", ""),
                "ITEM_RULE": detail.get("specification", ""),
                "ITEM_UNIT": detail.get("units", ""),
                "INVOICE_AMOUNT": detail.get("includeTaxAmount"),
                "DUTY_PARAGRAPH": (float(detail.get("taxRate", 0)) * 100) if detail.get("taxRate") else None,
                "INVOICE_TAX": detail.get("taxAmount"),
                "TABLE_NAME": detail.get("revenueCode", ""),
                "OPERATE_DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            synchro_billdetail(db, detail_model)
        return True, ""

    # 已存在的票据 → 更新
    bill_model.pop("DetailList", None)
    bill_model["SERIAL_NO"] = jdpj_data.get("invoiceNum", "")
    bill_model["BILL_TAXAMOUNT"] = jdpj_data.get("includeTaxAmount")
    bill_model["BILL_AMOUNT"] = jdpj_data.get("totalAmount")
    bill_model["TAX_PRICE"] = jdpj_data.get("totalTaxAmount")

    # 计算尾差
    invoice_taxamount = float(bill_model.get("INVOICE_TAXAMOUNT") or 0)
    invoice_amount = float(bill_model.get("INVOICE_AMOUNT") or 0)
    bill_taxamount = float(jdpj_data.get("includeTaxAmount") or 0)
    bill_amount = float(jdpj_data.get("totalAmount") or 0)
    bill_model["TAXTAIL_DIFFERENCE"] = round(bill_taxamount - invoice_taxamount, 2)
    bill_model["TAIL_DIFFERENCE"] = round(bill_amount - invoice_amount, 2)

    bill_model["BILL_PERSON"] = jdpj_data.get("drawer", "")
    bill_model["ACCOUNTED_DATE"] = jdpj_data.get("invoiceDate") or datetime.now().strftime("%Y-%m-%d")
    bill_model["DOWNLOAD_URL"] = jdpj_data.get("invoicePdfFileUrl", "")

    bill_state = int(bill_model.get("BILL_STATE") or 1000)
    if bill_state < 9200:
        bill_model["BILL_STATE"] = 9200

    # 红冲处理
    invoice_property = jdpj_data.get("invoiceProperty", 0)
    if invoice_property == 1 and len(bill_no) > 3:
        ori_bill_no = bill_no[3:]  # C#: billNo.Substring(3)
        ori_bill = get_bill_detail(db, bill_no=ori_bill_no)
        if ori_bill and ori_bill.get("BILL_ID"):
            ori_bill.pop("DetailList", None)
            ori_bill["BILL_STATE"] = 9999
            synchro_bill(db, ori_bill)
            logger.info(f"红冲处理：原票据 {ori_bill_no} 状态更新为 9999")

    ok, _ = synchro_bill(db, bill_model)
    return ok, "" if ok else "更新失败"


# ========== 12. ForwardJDPJInterface ==========
def forward_jdpj_interface(data: dict) -> Tuple[bool, str, str]:
    """
    金蝶开票/红冲申请（接口转发）
    C# 原逻辑 (InvoiceController.ForwardJDPJInterface):
    接收 JDPJReqModel（含 ReqUrl + Data），通过 HttpUrlPost 转发 HTTP POST 请求
    """
    req_url = data.get("ReqUrl", "")
    if not req_url:
        return False, "", "缺少 ReqUrl"

    req_data = data.get("Data", "{}")
    logger.info(f"ForwardJDPJInterface: URL={req_url}, Data={req_data[:200]}")

    try:
        resp = requests.post(
            req_url,
            data=req_data.encode('utf-8') if isinstance(req_data, str) else json.dumps(req_data).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        logger.info(f"ForwardJDPJInterface 响应: Status={resp.status_code}, Body={resp.text[:500]}")
        return True, resp.text, ""
    except Exception as e:
        error_msg = f"转发失败: {e}"
        logger.error(error_msg)
        return False, "", error_msg
