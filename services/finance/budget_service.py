from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BudgetProjectAHController 业务服务
移植自 C#: BUDGETPROJECTAHHelper.cs / BUDGETDETAILAHHelper.cs

BUDGETPROJECT_AH CRUD（4）+ BUDGETDETAIL_AH CRUD（4）
+ SetBudgetDetailAHList（1）+ 报表接口（7）

重要逻辑差异（与 C# 保持一致）：
- Delete: 设 BUDGETPROJECT_STATE = 0（C# 原逻辑）
- SynchroBUDGETPROJECT_AH: 自动从 T_SERVERPART 获取 SPREGIONTYPE_ID/NAME
- GetBudgetDetailList: 附带计算 Summary（BUDGETDETAIL_AMOUNT 和 REVENUE_AMOUNT 汇总）
- GetBudgetProjectReportOfMonth: JOIN T_BUDGETPROJECT_AH + T_BUDGETDETAIL_AH, 按月份做数据透视
- 动态报表接口: 依赖 FieldEnum 枚举树，简化实现（直接查询 SQL）
"""
from typing import Optional, Tuple
from loguru import logger
from core.database import DatabaseHelper
from datetime import datetime


# ============================================================
#               BUDGETPROJECT_AH（安徽财务预算表）
# ============================================================
BP_TABLE = "T_BUDGETPROJECT_AH"
BP_PK = "BUDGETPROJECT_AH_ID"

BP_EXCLUDE_FIELDS = {"SERVERPART_IDS", "OPERATE_DATE_Start", "OPERATE_DATE_End"}
BP_STRING_FIELDS = {
    "BUDGETPROJECT_CODE", "BUDGETPROJECT_UNIT", "SERVERPART_NAME",
    "SPREGIONTYPE_NAME", "STAFF_NAME", "BUDGETPROJECT_AH_DESC"
}
# C# Model 回显属性（DB 没有，C# Model 有，值为 null）
BP_EXTRA_FIELDS = {"SERVERPART_IDS": None, "OPERATE_DATE_Start": None, "OPERATE_DATE_End": None}


def _format_date(val):
    """将日期格式从 ISO 转为 C# 风格: 2023/3/30 14:02:47"""
    if val is None:
        return None
    s = str(val)
    try:
        # 处理 ISO 格式：2023-03-30T14:02:47
        if 'T' in s:
            dt = datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        elif '-' in s and len(s) >= 10:
            dt = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
        else:
            return s  # 已经是正确格式或其他格式
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute:02d}:{dt.second:02d}"
    except Exception:
        return s


def _convert_bp_row(row: dict) -> dict:
    """转换 BUDGETPROJECT_AH 行：补 C# Model 回显字段 + 字符串 null→'' + 日期格式化"""
    if not row:
        return row
    for f in BP_STRING_FIELDS:
        if f in row and row[f] is None:
            row[f] = ""
    # 补 C# Model 回显属性
    for k, v in BP_EXTRA_FIELDS.items():
        if k not in row:
            row[k] = v
    # 日期格式化
    if "OPERATE_DATE" in row:
        row["OPERATE_DATE"] = _format_date(row["OPERATE_DATE"])
    return row


# ========== 1. GetBudgetProjectList ==========
def get_budget_project_list(db: DatabaseHelper, search_model: dict) -> Tuple[list, int]:
    """
    获取安徽财务预算表列表
    C# 搜索条件: SERVERPART_IDS, OPERATE_DATE范围, BUDGETPROJECT_YEAR范围，软删除 STATE<>0
    """
    pi = search_model.get("PageIndex", 1)
    ps = search_model.get("PageSize", 15)
    sd = search_model.get("SearchData") or search_model.get("SearchParameter") or {}
    kw = search_model.get("keyWord") or {}

    wp, pa = [], []

    # 服务区 IN
    sp_ids = sd.get("SERVERPART_IDS", "") or sd.get("SERVERPART_ID", "")
    if sp_ids:
        wp.append(f"SERVERPART_ID IN ({sp_ids})")

    # 操作日期范围
    if sd.get("OPERATE_DATE_Start"):
        wp.append(f"OPERATE_DATE >= TO_DATE('{str(sd['OPERATE_DATE_Start'])[:10]}','YYYY-MM-DD')")
    if sd.get("OPERATE_DATE_End"):
        wp.append(f"OPERATE_DATE < TO_DATE('{str(sd['OPERATE_DATE_End'])[:10]}','YYYY-MM-DD') + 1")

    # 年份范围
    if sd.get("OPERATE_DATE_Start"):
        try:
            y = datetime.strptime(str(sd["OPERATE_DATE_Start"])[:10], "%Y-%m-%d").year
            wp.append(f"BUDGETPROJECT_YEAR >= {y}")
        except Exception:
            pass
    if sd.get("OPERATE_DATE_End"):
        try:
            y = datetime.strptime(str(sd["OPERATE_DATE_End"])[:10], "%Y-%m-%d").year
            wp.append(f"BUDGETPROJECT_YEAR <= {y}")
        except Exception:
            pass

    # 软删除（C# 原逻辑）
    wp.append("BUDGETPROJECT_STATE <> 0")

    wc = " AND ".join(wp) if wp else "BUDGETPROJECT_STATE <> 0"

    # 关键字搜索
    kk, kv = kw.get("Key", ""), kw.get("Value", "")
    if kk and kv:
        like_parts = [f"{k.strip()} LIKE '%{kv}%'" for k in kk.split(',') if k.strip()]
        if like_parts:
            wc += f" AND ({' OR '.join(like_parts)})"

    sort_str = search_model.get("SortStr", f"{BP_PK} DESC")

    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {BP_TABLE} WHERE {wc}", pa) or 0
    offset = (pi - 1) * ps
    # 达梦兼容分页（用 ROWNUM 子查询替代 LIMIT OFFSET）
    paged_sql = f"""
        SELECT * FROM (
            SELECT A.*, ROWNUM AS RN__ FROM (
                SELECT * FROM {BP_TABLE} WHERE {wc} ORDER BY {sort_str}
            ) A WHERE ROWNUM <= {offset + ps}
        ) WHERE RN__ > {offset}
    """
    rows = db.fetch_all(paged_sql, pa) or []
    # 移除辅助列
    for r in rows:
        r.pop("RN__", None)
    return [_convert_bp_row(r) for r in rows], total


# ========== 2. GetBudgetProjectDetail ==========
def get_budget_project_detail(db: DatabaseHelper, pk_val: int) -> Optional[dict]:
    row = db.fetch_one(f"SELECT * FROM {BP_TABLE} WHERE {BP_PK} = ?", [pk_val])
    return _convert_bp_row(row)


# ========== 3. SynchroBudgetProject ==========
def synchro_budget_project(db: DatabaseHelper, data: dict) -> Tuple[bool, dict]:
    """
    同步安徽财务预算表
    C# 逻辑: 自动从 T_SERVERPART 获取 SPREGIONTYPE_ID / SPREGIONTYPE_NAME
    """
    pk_val = data.get(BP_PK)

    # 自动获取片区信息（C# ServerpartHelper.GetSERVERPARTDetail）
    sp_id = data.get("SERVERPART_ID")
    if sp_id:
        try:
            sp_row = db.fetch_one(
                "SELECT SPREGIONTYPE_ID, SPREGIONTYPE_NAME FROM T_SERVERPART WHERE SERVERPART_ID = ?",
                [sp_id])
            if sp_row:
                data["SPREGIONTYPE_ID"] = sp_row.get("SPREGIONTYPE_ID")
                data["SPREGIONTYPE_NAME"] = sp_row.get("SPREGIONTYPE_NAME", "")
        except Exception as e:
            logger.warning(f"获取片区信息失败: {e}")

    save_data = {k: v for k, v in data.items() if k not in BP_EXCLUDE_FIELDS}

    if pk_val:
        check = db.fetch_scalar(f"SELECT COUNT(*) FROM {BP_TABLE} WHERE {BP_PK} = ?", [pk_val])
        if check and check > 0:
            fields = {k: v for k, v in save_data.items() if k != BP_PK}
            if not fields:
                return True, data
            sc = ", ".join([f"{k} = ?" for k in fields.keys()])
            db.execute(f"UPDATE {BP_TABLE} SET {sc} WHERE {BP_PK} = ?",
                       list(fields.values()) + [pk_val])
            return True, data
        else:
            return False, data
    else:
        try:
            new_id = db.fetch_scalar("SELECT NEWPYTHON.SEQ_BUDGETPROJECT_AH.NEXTVAL FROM DUAL")
            save_data[BP_PK] = new_id
            data[BP_PK] = new_id
        except Exception:
            new_id = db.fetch_scalar(f"SELECT COALESCE(MAX({BP_PK}), 0) + 1 FROM {BP_TABLE}")
            save_data[BP_PK] = new_id
            data[BP_PK] = new_id
        cols = ", ".join(save_data.keys())
        phs = ", ".join(["?"] * len(save_data))
        db.execute(f"INSERT INTO {BP_TABLE} ({cols}) VALUES ({phs})", list(save_data.values()))
        return True, data


# ========== 4. DeleteBudgetProject ==========
def delete_budget_project(db: DatabaseHelper, pk_val: int) -> bool:
    """C# 原逻辑: UPDATE BUDGETPROJECT_STATE = 0"""
    if not pk_val:
        return False
    db.execute(f"UPDATE {BP_TABLE} SET BUDGETPROJECT_STATE = 0 WHERE {BP_PK} = ?", [pk_val])
    return True


# ============================================================
#              BUDGETDETAIL_AH（安徽财务预算明细表）
# ============================================================
BD_TABLE = "T_BUDGETDETAIL_AH"
BD_PK = "BUDGETDETAIL_AH_ID"
# C# BUDGETDETAIL_AHModel 回显属性（DB 没有，值为 null）
BD_EXTRA_FIELDS = {"STATISTICS_MONTH_Start": None, "STATISTICS_MONTH_End": None}
# C# Model 字符串字段，DBNull→''
BD_STRING_FIELDS = {"BUDGETDETAIL_AH_DESC"}


def _convert_bd_row(row: dict) -> dict:
    """转换 BUDGETDETAIL_AH 行：补 C# Model 回显字段 + 字符串 null→'' + 日期格式化"""
    if not row:
        return row
    # 补 C# Model 回显属性
    for k, v in BD_EXTRA_FIELDS.items():
        if k not in row:
            row[k] = v
    # 字符串字段 null→''
    for f in BD_STRING_FIELDS:
        if f in row and row[f] is None:
            row[f] = ""
    # 日期格式化
    if "OPERATE_DATE" in row:
        row["OPERATE_DATE"] = _format_date(row["OPERATE_DATE"])
    return row


# ========== 5. GetBudgetDetailList ==========
def get_budget_detail_list(db: DatabaseHelper, search_model: dict) -> Tuple[list, int, dict]:
    """
    获取预算明细列表
    C# 附带 Summary 对象：计算 BUDGETDETAIL_AMOUNT 和 REVENUE_AMOUNT 的汇总
    """
    pi = search_model.get("PageIndex", 1)
    ps = search_model.get("PageSize", 15)
    sd = search_model.get("SearchData") or search_model.get("SearchParameter") or {}

    wp, pa = [], []
    # BUDGETDETAIL_AH_ID 精确匹配
    if sd.get("BUDGETDETAIL_AH_ID"):
        wp.append("BUDGETDETAIL_AH_ID = ?")
        pa.append(sd["BUDGETDETAIL_AH_ID"])
    if sd.get("BUDGETPROJECT_AH_ID"):
        wp.append("BUDGETPROJECT_AH_ID = ?")
        pa.append(sd["BUDGETPROJECT_AH_ID"])
    if sd.get("STATISTICS_MONTH"):
        wp.append("STATISTICS_MONTH = ?")
        pa.append(sd["STATISTICS_MONTH"])
    if sd.get("ACCOUNT_CODE"):
        wp.append("ACCOUNT_CODE LIKE ?")
        pa.append(f"{sd['ACCOUNT_CODE']}%")

    wp.append("BUDGETDETAIL_AH_STATE <> 0")
    wc = " AND ".join(wp) if wp else "BUDGETDETAIL_AH_STATE <> 0"

    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {BD_TABLE} WHERE {wc}", pa) or 0

    # Summary 汇总（C# 原逻辑：遍历列表累加 BUDGETDETAIL_AMOUNT + REVENUE_AMOUNT）
    # C# 返回的是完整 Model 对象，除 BUDGETDETAIL_AMOUNT/REVENUE_AMOUNT 外都是 null
    _BD_COLUMNS = [
        "BUDGETDETAIL_AH_ID", "BUDGETPROJECT_AH_ID", "ACCOUNT_PCODE",
        "ACCOUNT_CODE", "STATISTICS_MONTH", "STATISTICS_MONTH_Start",
        "STATISTICS_MONTH_End", "BUDGETDETAIL_AMOUNT", "REVENUE_AMOUNT",
        "UPDATE_TIME", "BUDGETDETAIL_AH_STATE", "STAFF_ID", "STAFF_NAME",
        "OPERATE_DATE", "BUDGETDETAIL_AH_DESC", "ACCOMPLISH", "YEARBUDGET",
        "YEARTOTAL", "YEARPROGRESS", "BUDGETTPE"
    ]
    try:
        sum_sql = f"""
            SELECT COALESCE(SUM(BUDGETDETAIL_AMOUNT), 0) AS TOTAL_BUDGET,
                   COALESCE(SUM(REVENUE_AMOUNT), 0) AS TOTAL_REVENUE
            FROM {BD_TABLE} WHERE {wc}
        """
        sum_row = db.fetch_one(sum_sql, pa)
        # 构建完整 Model（与 C# 一致）
        summary = {col: None for col in _BD_COLUMNS}
        summary["BUDGETDETAIL_AMOUNT"] = sum_row.get("TOTAL_BUDGET", 0) if sum_row else 0
        summary["REVENUE_AMOUNT"] = sum_row.get("TOTAL_REVENUE", 0) if sum_row else 0
    except Exception:
        summary = {col: None for col in _BD_COLUMNS}
        summary["BUDGETDETAIL_AMOUNT"] = 0
        summary["REVENUE_AMOUNT"] = 0

    sort_str = search_model.get("SortStr", f"{BD_PK} DESC")
    offset = (pi - 1) * ps
    # 达梦兼容分页
    paged_sql = f"""
        SELECT * FROM (
            SELECT A.*, ROWNUM AS RN__ FROM (
                SELECT * FROM {BD_TABLE} WHERE {wc} ORDER BY {sort_str}
            ) A WHERE ROWNUM <= {offset + ps}
        ) WHERE RN__ > {offset}
    """
    rows = db.fetch_all(paged_sql, pa, null_to_empty=False) or []
    for r in rows:
        r.pop("RN__", None)
    return [_convert_bd_row(r) for r in rows], total, summary


# ========== 6. GetBudgetDetailDetail ==========
def get_budget_detail_detail(db: DatabaseHelper, pk_val: int) -> Optional[dict]:
    row = db.fetch_one(f"SELECT * FROM {BD_TABLE} WHERE {BD_PK} = ?", [pk_val])
    return _convert_bd_row(row)


# ========== 7. SynchroBudgetDetail ==========
def synchro_budget_detail(db: DatabaseHelper, data: dict) -> Tuple[bool, dict]:
    pk_val = data.get(BD_PK)
    if pk_val:
        check = db.fetch_scalar(f"SELECT COUNT(*) FROM {BD_TABLE} WHERE {BD_PK} = ?", [pk_val])
        if check and check > 0:
            fields = {k: v for k, v in data.items() if k != BD_PK}
            if not fields:
                return True, data
            sc = ", ".join([f"{k} = ?" for k in fields.keys()])
            db.execute(f"UPDATE {BD_TABLE} SET {sc} WHERE {BD_PK} = ?",
                       list(fields.values()) + [pk_val])
            return True, data

    try:
        new_id = db.fetch_scalar("SELECT NEWPYTHON.SEQ_BUDGETDETAIL_AH.NEXTVAL FROM DUAL")
        data[BD_PK] = new_id
    except Exception:
        new_id = db.fetch_scalar(f"SELECT COALESCE(MAX({BD_PK}), 0) + 1 FROM {BD_TABLE}")
        data[BD_PK] = new_id
    cols = ", ".join(data.keys())
    phs = ", ".join(["?"] * len(data))
    db.execute(f"INSERT INTO {BD_TABLE} ({cols}) VALUES ({phs})", list(data.values()))
    return True, data


# ========== 8. DeleteBudgetDetail ==========
def delete_budget_detail(db: DatabaseHelper, pk_val: int) -> bool:
    """C# 原逻辑: BUDGETDETAIL_AH_STATE = 0"""
    if not pk_val:
        return False
    db.execute(f"UPDATE {BD_TABLE} SET BUDGETDETAIL_AH_STATE = 0 WHERE {BD_PK} = ?", [pk_val])
    return True


# ============================================================
#                     散装接口
# ============================================================

# ========== 9. SetBudgetDetailAHList ==========
def set_budget_detail_ah_list(db: DatabaseHelper, data_list: list) -> Tuple[bool, str]:
    """
    批量保存预算明细
    C# 逻辑: 遍历列表逐个调用 SynchroBUDGETDETAIL_AH
    """
    logger.info(f"SetBudgetDetailAHList: 数量={len(data_list) if data_list else 0}")
    try:
        for item in data_list:
            synchro_budget_detail(db, item)
        return True, ""
    except Exception as e:
        return False, str(e)


# ========== 10. GetBudgetProjectReportOfMonth ==========
def get_budget_project_report_of_month(db: DatabaseHelper, serverpart_id: str,
                                        year: int, account_code: str) -> list:
    """
    财务报表统计
    C# 原逻辑: JOIN T_BUDGETPROJECT_AH + T_BUDGETDETAIL_AH
    按 ACCOUNT_CODE 分组，将12个月的 BUDGETDETAIL_AMOUNT 做数据透视
    """
    logger.info(f"GetBudgetProjectReportOfMonth: SP={serverpart_id}, Year={year}, Code={account_code}")
    try:
        sql = f"""
            SELECT B.* FROM {BP_TABLE} A
            LEFT JOIN {BD_TABLE} B ON A.{BP_PK} = B.{BP_PK}
            WHERE A.SERVERPART_ID = ? AND A.BUDGETPROJECT_YEAR = ?
            AND B.BUDGETDETAIL_AH_STATE = 1
            AND B.ACCOUNT_CODE LIKE ?
        """
        params = [serverpart_id, year, f"{account_code}%"]
        rows = db.fetch_all(sql, params) or []

        if not rows:
            return []

        # 按 ACCOUNT_CODE 分组做数据透视（C# SetBaseData 逻辑）
        from collections import defaultdict
        grouped = defaultdict(list)
        for r in rows:
            code = r.get("ACCOUNT_CODE", "")
            grouped[code].append(r)

        result = []
        for code, items in grouped.items():
            report_item = {"Account_Code": code}
            for month_num in range(1, 13):
                stat_month = int(f"{year}{month_num:02d}")
                month_items = [i for i in items if i.get("STATISTICS_MONTH") == stat_month]
                amount = month_items[0].get("BUDGETDETAIL_AMOUNT") if month_items else None
                report_item[f"BudGETDetail_Amount_{month_num:02d}"] = amount

            # 年度预算（STATISTICS_MONTH = year13）
            year_items = [i for i in items if i.get("STATISTICS_MONTH") == int(f"{year}13")]
            report_item["BudGETDetail_Amount"] = year_items[0].get("BUDGETDETAIL_AMOUNT") if year_items else None

            # 调整后预算（STATISTICS_MONTH > year13 的最新值）
            adjusted = [i for i in items if (i.get("STATISTICS_MONTH") or 0) > int(f"{year}13")]
            adjusted.sort(key=lambda x: x.get("STATISTICS_MONTH", 0), reverse=True)
            report_item["AdjustedBudget"] = adjusted[0].get("BUDGETDETAIL_AMOUNT") if adjusted else None

            # 调整差额
            budget = report_item["BudGETDetail_Amount"] or 0
            adj = report_item["AdjustedBudget"] or 0
            report_item["AdjustmentAmount"] = budget - adj

            result.append(report_item)

        return result
    except Exception as e:
        logger.error(f"GetBudgetProjectReportOfMonth 失败: {e}")
        return []


# ========== 11. GetbudgetProjectReport ==========
def get_budget_project_report(db: DatabaseHelper, month: int) -> str:
    """
    读取报表文件内容
    C# 原逻辑: 从服务器文件系统读取 txt 文件
    简化: 返回空字符串（需要配置文件路径后实现）
    """
    logger.info(f"GetbudgetProjectReport: Month={month}")
    return ""


# ========== 12-16. 动态报表接口 ==========
def get_budget_project_in_dynamic(db: DatabaseHelper, month: int,
                                   two_code: int, field_explain_id: int) -> list:
    """
    获取财务营收报表-收入明细(动态)
    C# 原逻辑: 使用 FieldEnum 枚举树 + BUDGETDETAIL_AH 数据，构建层级报表
    简化: 直接查询 T_BUDGETDETAIL_AH 数据
    """
    logger.info(f"GetbudgetProjectInDynamic: Month={month}, Code={two_code}")
    try:
        sql = f"""
            SELECT * FROM {BD_TABLE}
            WHERE STATISTICS_MONTH = ? AND BUDGETDETAIL_AH_STATE = 1
            ORDER BY ACCOUNT_CODE
        """
        rows = db.fetch_all(sql, [month]) or []
        return rows
    except Exception as e:
        logger.error(f"GetbudgetProjectInDynamic 失败: {e}")
        return []


def get_budget_project_out_dynamic(db: DatabaseHelper, month: int,
                                    two_code: int, field_explain_id: int) -> list:
    """获取财务营收报表-支出明细(动态)"""
    logger.info(f"GetbudgetProjectOutDynamic: Month={month}, Code={two_code}")
    try:
        rows = db.fetch_all(
            f"SELECT * FROM {BD_TABLE} WHERE STATISTICS_MONTH = ? AND BUDGETDETAIL_AH_STATE = 1 ORDER BY ACCOUNT_CODE",
            [month]) or []
        return rows
    except Exception as e:
        logger.error(f"GetbudgetProjectOutDynamic 失败: {e}")
        return []


def get_budget_project_out_dynamic_one(db: DatabaseHelper, month: int,
                                        two_code: int, field_explain_id: int) -> list:
    """获取财务营收报表-支出明细(动态，少一层级)"""
    logger.info(f"GetbudgetProjectOutDynamicOne: Month={month}, Code={two_code}")
    return get_budget_project_out_dynamic(db, month, two_code, field_explain_id)


def get_budget_value(db: DatabaseHelper, month: int, key: str) -> Optional[dict]:
    """
    获取财务营收报表-获取Value值
    C# GetbudgetValue: 根据 month + key 查询单条预算明细
    """
    logger.info(f"GetbudgetValue: Month={month}, Key={key}")
    try:
        sql = f"""
            SELECT * FROM {BD_TABLE}
            WHERE STATISTICS_MONTH = ? AND ACCOUNT_CODE = ?
            AND BUDGETDETAIL_AH_STATE = 1
        """
        return db.fetch_one(sql, [month, key])
    except Exception as e:
        logger.error(f"GetbudgetValue 失败: {e}")
        return {}


def get_budget_all_report(db: DatabaseHelper, serverpart_id: str, year: int) -> list:
    """
    获取全部财务营收概览
    """
    logger.info(f"GetBudgetAllReport: SP={serverpart_id}, Year={year}")
    try:
        sql = f"""
            SELECT B.* FROM {BP_TABLE} A
            LEFT JOIN {BD_TABLE} B ON A.{BP_PK} = B.{BP_PK}
            WHERE A.SERVERPART_ID = ? AND A.BUDGETPROJECT_YEAR = ?
            AND B.BUDGETDETAIL_AH_STATE = 1
            ORDER BY B.ACCOUNT_CODE, B.STATISTICS_MONTH
        """
        return db.fetch_all(sql, [serverpart_id, year]) or []
    except Exception as e:
        logger.error(f"GetBudgetAllReport 失败: {e}")
        return []
