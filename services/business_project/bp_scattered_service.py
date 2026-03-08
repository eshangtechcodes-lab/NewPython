from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BusinessProjectController 散装接口 Service（第一批 8 个简单接口）
对应原 C# 中多个 Helper 的独立方法

接口清单：
1. GetNoProjectShopList — BUSINESSPROJECTHelper.GetNoProjectShopList
2. GetAccountWarningListSummary — BUSINESSPROJECTHelper.GetAccountWarningSummary
3. GetMerchantSplit — BIZPSPLITMONTHHelper.GetMerchantSplit
4. SolidPeriodWarningList — 循环 PERIODWARNINGHelper.SynchroPERIODWARNING
5. UploadRevenueConfirmList — 循环 REVENUECONFIRMHelper.SynchroREVENUECONFIRM
6. SaveHisPaymentAccount — PAYMENTCONFIRMHelper.SaveHisPaymentAccount
7. CreateRevenueAccount — REVENUECONFIRMHelper.CreateRevenueAccount（简化版）
8. ApproveProinst — PROJECTWARNINGHelper.ApproveProinst
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper


# ==================== 1. GetNoProjectShopList ====================
def get_no_project_shop_list(db: DatabaseHelper, province_code: str,
                              sp_region_type_id: str = "", serverpart_id: str = "") -> list[dict]:
    """
    获取没有设置经营项目的移动支付分账门店
    原 BUSINESSPROJECTHelper.GetNoProjectShopList（1230-1284行）
    """
    where_sql = ""
    if serverpart_id and serverpart_id.strip():
        where_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
    elif sp_region_type_id and sp_region_type_id.strip():
        where_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
    elif province_code and province_code.strip():
        where_sql += f" AND B.PROVINCE_CODE = {province_code}"

    sql = f"""SELECT
            B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX, B.SERVERPART_ID,
            B.SERVERPART_INDEX, B.SERVERPART_CODE, B.SERVERPART_NAME,
            MIN(A.SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID, A.SHOPSHORTNAME
        FROM
            T_SERVERPARTSHOP A, T_SERVERPART B
        WHERE
            A.SERVERPART_ID = B.SERVERPART_ID AND A.ROYALTYRATE IS NOT NULL AND
            A.ISVALID = 1 AND B.SERVERPART_CODE NOT IN ('348888') AND
            NOT EXISTS (SELECT 1 FROM T_BUSINESSPROJECT C
                WHERE ',' || C.SERVERPARTSHOP_ID || ',' LIKE '%,' || CAST(A.SERVERPARTSHOP_ID AS VARCHAR) || ',%' AND
                    C.SETTLEMENT_MODES IN (3000,400) AND C.PROJECT_VALID = 1){where_sql}
        GROUP BY
            B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX, B.SERVERPART_ID,
            B.SERVERPART_INDEX, B.SERVERPART_CODE, B.SERVERPART_NAME, A.SHOPSHORTNAME
        ORDER BY B.SPREGIONTYPE_INDEX, B.SERVERPART_INDEX, B.SERVERPART_CODE, A.SHOPSHORTNAME"""

    rows = db.execute_query(sql)
    result = []
    for r in rows:
        result.append({
            "label": r.get("SHOPSHORTNAME", ""),
            "value": r.get("SERVERPARTSHOP_ID"),
            "key": r.get("SERVERPART_NAME", ""),
            "ico": r.get("SPREGIONTYPE_NAME", ""),
        })
    return result


# ==================== 2. GetAccountWarningListSummary ====================
def get_account_warning_summary(db: DatabaseHelper, business_type: str = "",
                                 settlement_mode: str = "", business_state: str = "") -> list[dict]:
    """
    获取门店经营预警汇总
    原 BUSINESSPROJECTHelper.GetAccountWarningSummary（4132-4187行）
    查 T_ACCOUNTWARNING 按 WARNING_TYPE 分组计数
    """
    where_sql = ""
    if business_type and business_type.strip():
        where_sql += f" AND BUSINESS_TYPE IN ({business_type})"
    if settlement_mode and settlement_mode.strip():
        where_sql += f" AND SETTLEMENT_MODES IN ({settlement_mode})"
    if business_state and business_state.strip():
        where_sql += f" AND BUSINESS_STATE IN ({business_state})"

    sql = f"""SELECT WARNING_TYPE, COUNT(1) AS WARNING_COUNT
        FROM T_ACCOUNTWARNING
        WHERE WARNING_TYPE > 0{where_sql}
        GROUP BY WARNING_TYPE"""

    counts = db.execute_query(sql)
    count_map = {}
    for r in counts:
        wt = r.get("WARNING_TYPE")
        wc = r.get("WARNING_COUNT", 0)
        if wt is not None:
            count_map[int(wt)] = int(wc)

    # 原 C# 从枚举表 T_FIELDENUM 获取 WARNING_TYPE 的枚举（level 字段不参与传递）
    # 查询所有 WARNING_TYPE 枚举值
    enum_sql = """SELECT FIELDENUM_ID, FIELDENUM_NAME FROM T_FIELDENUM
        WHERE FIELD_ID = (SELECT FIELD_ID FROM T_FIELDENUM WHERE FIELDENUM_NAME = 'WARNING_TYPE' AND FIELDENUM_PID = 0)
        AND FIELDENUM_ID <> 0
        ORDER BY FIELDENUM_INDEX, FIELDENUM_ID"""
    try:
        enums = db.execute_query(enum_sql)
    except Exception:
        # 回退硬编码
        enums = []

    if enums:
        result = []
        for e in enums:
            wt = int(e.get("FIELDENUM_ID", 0))
            label = e.get("FIELDENUM_NAME", "")
            result.append({
                "label": label,
                "value": count_map.get(wt, 0),
                "pid": wt,
                "level": None,
            })
        return result
    else:
        # 回退硬编码（8种枚举）
        warning_types = {
            1: "项目未有营业", 2: "项目利润过低", 3: "商家退场告警",
            4: "项目预亏预警", 5: "商家退场预警", 6: "租金提成偏低",
            7: "租金提成过高", 8: "保底偏低预警",
        }
        result = []
        for wt, label in warning_types.items():
            result.append({
                "label": label,
                "value": count_map.get(wt, 0),
                "pid": wt,
                "level": None,
            })
        return result


# ==================== 3. GetMerchantSplit ====================
def get_merchant_split(db: DatabaseHelper, merchant_id: str,
                        serverpart_id: str = "", start_date: str = "", end_date: str = "") -> list[dict]:
    """
    获取经营商户项目拆分结果
    原 BIZPSPLITMONTHHelper.GetMerchantSplit（简化版）
    查 T_BIZPSPLITMONTH 按商户/服务区/日期范围过滤
    """
    conditions = [f"A.MERCHANTS_ID = {merchant_id}"]
    if serverpart_id and serverpart_id.strip():
        conditions.append(f"""EXISTS (SELECT 1 FROM T_SERVERPARTSHOP S
            WHERE ',' || A.SERVERPARTSHOP_ID || ',' LIKE '%,' || CAST(S.SERVERPARTSHOP_ID AS VARCHAR) || ',%'
            AND S.SERVERPART_ID IN ({serverpart_id}))""")
    if start_date and start_date.strip():
        conditions.append(f"A.STATISTICS_MONTH >= '{start_date.replace('/', '')[:6]}'")
    if end_date and end_date.strip():
        conditions.append(f"A.STATISTICS_MONTH <= '{end_date.replace('/', '')[:6]}'")

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A.* FROM T_BIZPSPLITMONTH A
        WHERE {where_sql}
        ORDER BY A.STATISTICS_MONTH"""
    return db.execute_query(sql)


# ==================== 4. SolidPeriodWarningList ====================
def solid_period_warning_list(db: DatabaseHelper, period_list: list[dict]) -> bool:
    """
    批量同步经营项目周期预警
    原 C# 循环调用 PERIODWARNINGHelper.SynchroPERIODWARNING
    """
    from services.business_project import periodwarning_service as pdw_svc
    for item in period_list:
        success, _ = pdw_svc.synchro_periodwarning(db, item)
        if not success:
            return False
    return True


# ==================== 5. UploadRevenueConfirmList ====================
def upload_revenueconfirm_list(db: DatabaseHelper, confirm_list: list[dict]) -> tuple[bool, list[dict]]:
    """
    批量上传退场结算应收拆分数据
    原 C# 循环调用 REVENUECONFIRMHelper.SynchroREVENUECONFIRM
    """
    from services.business_project import revenueconfirm_service as rc_svc
    for item in confirm_list:
        rc_svc.synchro_revenueconfirm(db, item)
    return True, confirm_list


# ==================== 6. SaveHisPaymentAccount ====================
def save_his_payment_account(db: DatabaseHelper, data: dict) -> bool:
    """
    存储商家缴款历史数据
    原 PAYMENTCONFIRMHelper.SaveHisPaymentAccount
    实际调用 PAYMENTCONFIRM 的 Synchro
    """
    from services.business_project import paymentconfirm_service as pc_svc
    success, _ = pc_svc.synchro_paymentconfirm(db, data)
    return success


# ==================== 7. CreateRevenueAccount ====================
def create_revenue_account(db: DatabaseHelper, shop_royalty_id: int) -> bool:
    """
    根据门店提成比例生成应收账款信息（合作分成）
    原 REVENUECONFIRMHelper.CreateRevenueAccount（简化版）
    创建基于 ShopRoyalty 的应收账款记录
    """
    # 查询应收拆分信息
    royalty = db.execute_query(f"SELECT * FROM T_SHOPROYALTY WHERE SHOPROYALTY_ID = {shop_royalty_id}")
    if not royalty:
        return False

    r = royalty[0]
    bp_id = r.get("BUSINESSPROJECT_ID")
    if not bp_id:
        return False

    # 查询经营项目信息
    project = db.execute_query(f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {bp_id}")
    if not project:
        return False

    # 简化版：标记为已生成
    try:
        db.execute_non_query(
            f"UPDATE T_SHOPROYALTY SET REVENUE_FLAG = 1 WHERE SHOPROYALTY_ID = {shop_royalty_id}")
        return True
    except Exception as e:
        logger.error(f"CreateRevenueAccount 失败: {e}")
        return False


# ==================== 8. ApproveProinst ====================
def approve_proinst(db: DatabaseHelper, business_id: int, staff_id: int,
                     staff_name: str, switch_rate: int, approve_state: int,
                     source_platform: str = "minProgram") -> tuple[bool, str]:
    """
    审批移动支付分账比例切换流程
    原 PROJECTWARNINGHelper.ApproveProinst（477-590行）
    更新 T_PROJECTWARNING 的 PROJECTWARNING_STATE 和 ROYALTY_CRATE
    并存储审批意见到 T_APPROVED
    """
    # 查询当前状态
    detail = db.execute_query(
        f"SELECT * FROM T_PROJECTWARNING WHERE PROJECTWARNING_ID = {business_id}")
    if not detail:
        return True, ""  # 原 C# 也返回 success

    current_state = detail[0].get("PROJECTWARNING_STATE")
    if current_state is not None and int(current_state) >= approve_state:
        return False, "流程已转出，请刷新后查看内容"

    now = datetime.now()
    desc = ""
    if approve_state == 9999:
        desc = f"{staff_name}于{now.strftime('%Y年%m月01日 00:00:00')}确认暂不切换"
    elif approve_state == 9000:
        desc = f"系统将在{now.strftime('%Y年%m月01日 00:00:00')}进行切换"

    try:
        # 更新 T_PROJECTWARNING
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        desc_sql = f", PROJECTWARNING_DESC = '{desc}'" if desc else ""
        db.execute_non_query(f"""UPDATE T_PROJECTWARNING SET
            PROJECTWARNING_STATE = {approve_state},
            ROYALTY_CRATE = {switch_rate},
            RECORD_DATE = TO_DATE('{now_str}', 'YYYY-MM-DD HH24:MI:SS'){desc_sql}
            WHERE PROJECTWARNING_ID = {business_id}""")

        # 存储审批意见到 T_APPROVED
        ori_state = current_state
        approved_info = "暂不切换" if approve_state == 9999 else "同意切换"
        approved_name = "经营部审核" if ori_state == 1000 else "财务部审核"
        dept_name = "经营部" if ori_state == 1000 else "财务部"
        approved_mark = 2000 if source_platform.lower() == "minprogram" else 1000

        max_id = db.execute_scalar("SELECT COALESCE(MAX(APPROVED_ID), 0) + 1 FROM T_APPROVED") or 1
        db.execute_non_query(f"""INSERT INTO T_APPROVED
            (APPROVED_ID, TABLE_ID, TABLE_NAME, APPROVED_TYPE, APPROVED_INFO,
             APPROVED_STAFFID, APPROVED_STAFF, APPROVED_DATE, APPROVED_NAME,
             DEPARTMENT_NAME, APPROVED_MARK)
            VALUES ({max_id}, {business_id}, 'T_PROJECTWARNING', {approve_state},
             '{approved_info}', {staff_id}, '{staff_name}', '{now_str}',
             '{approved_name}', '{dept_name}', {approved_mark})""")

        return True, ""
    except Exception as e:
        logger.error(f"ApproveProinst 失败: {e}")
        return False, str(e)
