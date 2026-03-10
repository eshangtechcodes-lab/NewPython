# -*- coding: utf-8 -*-
"""
PictureController 业务服务（15 个接口）
全部散装接口，无标准CRUD实体

C# 源: PictureController.cs (440行) + PictureHelper.cs
"""
from __future__ import annotations
from typing import Tuple
from loguru import logger
from core.database import DatabaseHelper


# ============================================================
# 内部辅助
# ============================================================

def _list(db: DatabaseHelper, table, pk, sm, extra_fields=None):
    """通用分页列表"""
    pi = sm.get("PageIndex", 1)
    ps = sm.get("PageSize", 15)
    sd = sm.get("SearchData") or {}
    conditions = []
    for f in (extra_fields or []):
        v = sd.get(f)
        if v:
            conditions.append(f"{f} = '{v}'")
    wc = " AND ".join(conditions) if conditions else "1=1"
    total = db.execute_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}") or 0
    sql = f"SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC"
    rows = db.execute_query(sql) or []
    off = (pi - 1) * ps
    rows = rows[off:off + ps]
    return rows, total


# ============================================================
# 原有 9 个接口（已修复方法名）
# ============================================================

def get_picture_list(db: DatabaseHelper, search_model: dict):
    """获取图片列表"""
    logger.info("GetPictureList")
    return _list(db, "T_IMAGE", "IMAGE_ID", search_model, ["SERVERPART_ID"])


def get_picture_detail(db: DatabaseHelper, pk_val: int):
    """获取图片详情"""
    logger.info(f"GetPictureDetail: {pk_val}")
    rows = db.execute_query("SELECT * FROM T_IMAGE WHERE IMAGE_ID = :pk", {"pk": pk_val})
    return rows[0] if rows else {}


def synchro_picture(db: DatabaseHelper, data: dict):
    """同步图片数据"""
    logger.info("SynchroPicture")
    pk = "IMAGE_ID"
    pv = data.get(pk)
    if pv:
        c = db.execute_scalar(f"SELECT COUNT(*) FROM T_IMAGE WHERE {pk} = :pv", {"pv": pv})
        if c and c > 0:
            fs = {k: v for k, v in data.items() if k != pk}
            if fs:
                set_parts = []
                params = {"pk_val": pv}
                for i, (k, v) in enumerate(fs.items()):
                    param_name = f"p{i}"
                    set_parts.append(f"{k} = :{param_name}")
                    params[param_name] = v
                sc = ", ".join(set_parts)
                db.execute_non_query(f"UPDATE T_IMAGE SET {sc} WHERE {pk} = :pk_val", params)
            return True, data
    # INSERT
    try:
        nid = db.execute_scalar("SELECT SEQ_IMAGE.NEXTVAL FROM DUAL")
        data[pk] = nid
    except Exception:
        nid = db.execute_scalar(f"SELECT NVL(MAX({pk}), 0) + 1 FROM T_IMAGE")
        data[pk] = nid

    cols = list(data.keys())
    col_str = ", ".join(cols)
    val_parts = []
    params = {}
    for i, c in enumerate(cols):
        param_name = f"v{i}"
        val_parts.append(f":{param_name}")
        params[param_name] = data[c]
    val_str = ", ".join(val_parts)
    db.execute_non_query(f"INSERT INTO T_IMAGE ({col_str}) VALUES ({val_str})", params)
    return True, data


def delete_picture(db: DatabaseHelper, pk_val: int):
    """删除图片"""
    c = db.execute_scalar("SELECT COUNT(*) FROM T_IMAGE WHERE IMAGE_ID = :pk", {"pk": pk_val})
    if not c or c == 0:
        return False
    db.execute_non_query("UPDATE T_IMAGE SET ISVALID = 0 WHERE IMAGE_ID = :pk", {"pk": pk_val})
    return True


def upload_picture(db: DatabaseHelper, data: dict):
    """上传图片"""
    logger.info("UploadPicture")
    return synchro_picture(db, data)


def get_picture_type_list(db: DatabaseHelper, **kwargs):
    """获取图片类型列表"""
    logger.info("GetPictureTypeList")
    try:
        return db.execute_query("SELECT DISTINCT IMAGE_TYPE FROM T_IMAGE WHERE ISVALID = 1") or []
    except Exception as e:
        logger.error(f"GetPictureTypeList error: {e}")
        return []


def get_picture_by_shop(db: DatabaseHelper, shop_id: str, picture_type: str = ""):
    """按门店获取图片"""
    logger.info(f"GetPictureByShop: Shop={shop_id}")
    try:
        wp = ["ISVALID = 1", f"TABLE_ID = '{shop_id}'"]
        if picture_type:
            wp.append(f"IMAGE_TYPE = '{picture_type}'")
        wc = " AND ".join(wp)
        return db.execute_query(f"SELECT * FROM T_IMAGE WHERE {wc} ORDER BY IMAGE_ID DESC") or []
    except Exception as e:
        logger.error(f"GetPictureByShop error: {e}")
        return []


def get_picture_count(db: DatabaseHelper, **kwargs):
    """获取图片统计"""
    logger.info(f"GetPictureCount: {kwargs}")
    try:
        total = db.execute_scalar("SELECT COUNT(*) FROM T_IMAGE WHERE ISVALID = 1") or 0
        return {"total_count": total}
    except Exception as e:
        logger.error(f"GetPictureCount error: {e}")
        return {}


def batch_delete_picture(db: DatabaseHelper, ids: list):
    """批量删除图片"""
    logger.info(f"BatchDeletePicture: {ids}")
    try:
        for pk_val in ids:
            delete_picture(db, pk_val)
        return True, ""
    except Exception as e:
        return False, str(e)


# ============================================================
# PI-02 补齐：C# PictureController 原有但 Python 缺失的接口
# ============================================================

def get_endaccount_evidence(db: DatabaseHelper, endaccount_id: int):
    """
    获取日结账单凭据 - C# PictureHelper.GetHWSImageList
    按 TableId + TableName 查询图片列表
    """
    logger.info(f"GetEndaccountEvidence: EndaccountId={endaccount_id}")
    try:
        sql = ("SELECT * FROM T_IMAGE "
               "WHERE TABLE_ID = :tid AND TABLE_NAME = :tname "
               "ORDER BY IMAGE_ID")
        rows = db.execute_query(sql, {
            "tid": endaccount_id,
            "tname": "HIGHWAY_SELLDATA.T_ENDACCOUNT"
        })
        return rows or [], len(rows or [])
    except Exception as e:
        logger.error(f"GetEndaccountEvidence error: {e}")
        return [], 0


def upload_endaccount_evidence(db: DatabaseHelper, data: dict):
    """
    上传日结账单凭据 - C# PictureHelper.UploadHWSImage
    接收 EndaccountId + ImageInfo(base64)
    """
    logger.info("UploadEndaccountEvidence")
    endaccount_id = data.get("EndaccountId") or data.get("ENDACCOUNT_ID")
    image_info = data.get("ImageInfo", "")

    if not endaccount_id:
        return False, "EndaccountId cannot be empty"

    picture_data = {
        "TABLE_ID": endaccount_id,
        "TABLE_NAME": "HIGHWAY_SELLDATA.T_ENDACCOUNT",
        "IMAGE_CONTENT": image_info,
        "IMAGE_PATH": "/UploadImageDir/ENDACCOUNT/",
    }
    return synchro_picture(db, picture_data)


def get_audit_evidence(db: DatabaseHelper, audit_id: int):
    """
    获取稽核数据凭据 - C# PictureHelper.GetHWSImageList
    按 TableId + TableName 查询图片列表（T_CHECKACCOUNT）
    """
    logger.info(f"GetAuditEvidence: AuditId={audit_id}")
    try:
        sql = ("SELECT * FROM T_IMAGE "
               "WHERE TABLE_ID = :tid AND TABLE_NAME = :tname "
               "ORDER BY IMAGE_ID")
        rows = db.execute_query(sql, {
            "tid": audit_id,
            "tname": "HIGHWAY_SELLDATA.T_CHECKACCOUNT"
        })
        return rows or [], len(rows or [])
    except Exception as e:
        logger.error(f"GetAuditEvidence error: {e}")
        return [], 0


def upload_audit_evidence(db: DatabaseHelper, data: dict):
    """
    上传稽核数据凭据 - C# PictureHelper.UploadHWSImage
    接收 AuditId + ImageInfo(base64) + ImageName
    """
    logger.info("UploadAuditEvidence")
    audit_id = data.get("AuditId") or data.get("AUDIT_ID")
    image_info = data.get("ImageInfo", "")
    image_name = data.get("ImageName", "")

    if not audit_id:
        return False, "AuditId cannot be empty"

    picture_data = {
        "TABLE_ID": audit_id,
        "TABLE_NAME": "HIGHWAY_SELLDATA.T_CHECKACCOUNT",
        "IMAGE_CONTENT": image_info,
        "IMAGE_TITLE": image_name,
        "IMAGE_PATH": "/UploadImageDir/CHECKACCOUNT/",
    }
    return synchro_picture(db, picture_data)


def save_img_file(db: DatabaseHelper, data: dict):
    """
    保存图片文件（只存储文件，不存储数据库）- C# PictureHelper.SaveImgFile
    注：文件存储需要文件系统支持，此处仅做路由占位和参数透传
    """
    logger.info("SaveImgFile")
    table_id = data.get("TableId") or data.get("TABLE_ID", 0)
    table_name = data.get("TableName") or data.get("TABLE_NAME", "")
    table_type = data.get("TableType") or data.get("TABLE_TYPE", "")
    image_name = data.get("ImageName") or data.get("IMAGE_NAME", "")

    result = {
        "TableId": table_id,
        "TableName": table_name,
        "TableType": table_type,
        "ImageName": image_name,
        "ImagePath": "",
    }
    return True, result


def delete_multi_picture(db: DatabaseHelper, picture_list: list):
    """
    删除多张图片 - C# PictureController.DeleteMultiPicture
    接收 PictureModel 列表，逐个删除
    """
    logger.info(f"DeleteMultiPicture: {len(picture_list)} items")
    try:
        for item in picture_list:
            image_id = item.get("ImageId") or item.get("IMAGE_ID") or item.get("IMAGE_ID", 0)
            if image_id:
                delete_picture(db, image_id)
        return True, ""
    except Exception as e:
        logger.error(f"DeleteMultiPicture error: {e}")
        return False, str(e)
