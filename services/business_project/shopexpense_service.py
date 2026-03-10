from __future__ import annotations
# -*- coding: utf-8 -*-
"""
门店费用表业务服务
替代原 SHOPEXPENSEHelper.cs（1765行）中标准 CRUD 逻辑
对应 BusinessProjectController 中 SHOPEXPENSE 相关 5 个接口

注意：
- 原 Synchro 有极复杂的级联逻辑（写 BUSINESSPROJECTSPLIT + 多次合同查询），这里简化为标准更新
- 原 Delete 有级联作废 BUSINESSPROJECTSPLIT + 备份到历史库，这里简化为标准软删除
- 原 GetList 有 summaryList 聚合返回，需特殊处理
- ApproveSHOPEXPENSE 接口对应审批流程（实际调用 Synchro 带 ApprovalProcess=true）
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from core.format_utils import format_row_dates
from models.common_model import SearchModel


TABLE_NAME = "T_SHOPEXPENSE"
PRIMARY_KEY = "SHOPEXPENSE_ID"

EXCLUDE_FIELDS = {
    "SERVERPART_IDS", "SPREGIONTYPE_IDS", "SERVERPARTSHOP_IDS",
    "STATISTICS_MONTH_Start", "STATISTICS_MONTH_End",
    "PREPAID_AMOUNT", "PREPAIDLAST_AMOUNT", "notExist",
    "ShowRevenue", "RevenueAmount", "ApprovalProcess",
    "ChangeFlag", "ImageFlag", "SHOPEXPENSE_TYPE",
}

DATE_FIELDS = {"STATISTICS_MONTH"}

SEARCH_PARAM_SKIP_FIELDS = {"PageIndex", "PageSize", "SortStr", "keyWord", "QueryType"}


def get_shopexpense_list(db: DatabaseHelper, search_model: SearchModel) -> tuple[int, list[dict]]:
    """获取门店费用列表 — C# SHOPEXPENSEHelper.GetSHOPEXPENSEList (含 summaryObject)"""
    conditions = []

    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        for k, v in sp.items():
            if k in EXCLUDE_FIELDS or k in SEARCH_PARAM_SKIP_FIELDS:
                continue
            if v is None or (isinstance(v, str) and v.strip() == ""):
                continue
            qt = search_model.QueryType or 0
            if qt == 0 and isinstance(v, str):
                conditions.append(f"{k} LIKE '%{v}%'")
            elif isinstance(v, str):
                conditions.append(f"{k} = '{v}'")
            else:
                conditions.append(f"{k} = {v}")

        # SERVERPART_IDS IN
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            conditions.append(f"SERVERPART_ID IN ({sp_ids})")

        # SERVERPARTSHOP_IDS IN
        sps_ids = sp.get("SERVERPARTSHOP_IDS")
        if sps_ids and str(sps_ids).strip():
            conditions.append(f"SERVERPARTSHOP_ID IN ({sps_ids})")

        # SPREGIONTYPE_IDS IN（服务区区域类型）
        spr_ids = sp.get("SPREGIONTYPE_IDS")
        if spr_ids and str(spr_ids).strip():
            conditions.append(
                f"EXISTS (SELECT 1 FROM T_SERVERPARTSHOP B WHERE B.ISVALID = 1 "
                f"AND B.SPREGIONTYPE_ID IN ({spr_ids}) AND A.SERVERPARTSHOP_ID = B.SERVERPARTSHOP_ID)")

        # STATISTICS_MONTH 日期范围
        sm_start = sp.get("STATISTICS_MONTH_Start")
        if sm_start and str(sm_start).strip():
            try:
                d = datetime.strptime(str(sm_start).split(" ")[0], "%Y/%m/%d" if "/" in str(sm_start) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(STATISTICS_MONTH,1,6) >= {d.strftime('%Y%m')}")
            except Exception:
                pass

        sm_end = sp.get("STATISTICS_MONTH_End")
        if sm_end and str(sm_end).strip():
            try:
                d = datetime.strptime(str(sm_end).split(" ")[0], "%Y/%m/%d" if "/" in str(sm_end) else "%Y-%m-%d")
                conditions.append(f"SUBSTR(STATISTICS_MONTH,1,6) <= {d.strftime('%Y%m')}")
            except Exception:
                pass

        # SHOPEXPENSE_TYPE 费用类型（原 C# 查子枚举，简化为直接 IN）
        se_type = sp.get("SHOPEXPENSE_TYPE")
        if se_type and str(se_type).strip():
            conditions.append(f"SHOPEXPENSE_TYPE IN ({se_type})")

        # notExist 排除费用类型
        not_exist = sp.get("notExist")
        if not_exist and str(not_exist).strip():
            conditions.append(f"SHOPEXPENSE_TYPE NOT IN ({not_exist})")

        # SERVERPARTSHOP_NAME 经营门店子查询
        shop_name = sp.get("SERVERPARTSHOP_NAME")
        if shop_name and str(shop_name).strip():
            conditions.append(
                f"EXISTS (SELECT 1 FROM T_SERVERPARTSHOP B WHERE B.ISVALID = 1 "
                f"AND B.SHOPSHORTNAME = '{shop_name}' AND A.SERVERPARTSHOP_ID = B.SERVERPARTSHOP_ID)")

        # BUSINESS_UNIT 经营单位子查询
        biz_unit = sp.get("BUSINESS_UNIT")
        if biz_unit and str(biz_unit).strip():
            conditions.append(
                f"EXISTS (SELECT 1 FROM T_SERVERPARTSHOP B WHERE B.ISVALID = 1 "
                f"AND B.BUSINESS_UNIT = '{biz_unit}' AND A.SERVERPARTSHOP_ID = B.SERVERPARTSHOP_ID)")

    where_sql = " WHERE " + " AND ".join(conditions) if conditions else ""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} A{where_sql}")

    # 关键字过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        if kw.get("Key") and kw.get("Value"):
            sv = kw["Value"]
            keys = [k.strip() for k in kw["Key"].split(",") if k.strip()]
            rows = [r for r in rows if any(sv in str(r.get(k, "")) for k in keys)]

    # 排序
    if search_model.SortStr:
        sf = search_model.SortStr.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "desc" in (search_model.SortStr or "").lower()
        try:
            rows.sort(key=lambda x: x.get(sf) or "", reverse=is_desc)
        except Exception:
            pass

    total_count = len(rows)

    # 费用合计 summaryObject（C# L144-155）— 按 SHOPEXPENSE_TYPE 分组求和
    summary_list = []
    type_sums = {}
    for r in rows:
        se_type = r.get("SHOPEXPENSE_TYPE")
        if se_type is not None:
            t = int(se_type)
            if t not in type_sums:
                type_sums[t] = 0.0
            type_sums[t] += float(r.get("SHOPEXPENSE_AMOUNT", 0) or 0)
    for t in sorted(type_sums.keys()):
        summary_list.append({
            "SHOPEXPENSE_TYPE": t,
            "SHOPEXPENSE_AMOUNT": round(type_sums[t], 2)
        })

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]
    elif len(rows) > 10:
        rows = rows[:10]

    # C# TranslateDateTime: int 日期→格式化字符串 (STATISTICS_MONTH 202406 → '2024/06')
    for r in rows:
        format_row_dates(r, DATE_FIELDS)
    return int(total_count), rows, summary_list


def get_shopexpense_detail(db: DatabaseHelper, se_id: int) -> Optional[dict]:
    """获取门店费用明细"""
    rows = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {se_id}")
    if not rows:
        return None
    format_row_dates(rows[0], DATE_FIELDS)
    return rows[0]


def synchro_shopexpense(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    同步门店费用 — C# SHOPEXPENSEHelper.SynchroSHOPEXPENSE (L365-674)
    完整逻辑：标准 upsert + ApprovalProcess 校验 + 历史备份 + 级联写 BUSINESSPROJECTSPLIT
    """
    from datetime import datetime as _dt
    record_id = data.get(PRIMARY_KEY)
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}
    is_insert = True

    # 默认有效状态
    if db_data.get("SHOPEXPENSE_STATE") is None:
        db_data["SHOPEXPENSE_STATE"] = 1

    def _fmt_month(val):
        if val is None:
            return None
        s = str(val).strip()
        if not s:
            return None
        try:
            dt = _dt.strptime(s.split(" ")[0], "%Y/%m/%d" if "/" in s else "%Y-%m-%d")
            return dt.strftime("%Y%m")
        except Exception:
            return s

    # 解析统计日期（用于级联查询项目周期）
    stat_month_raw = data.get("STATISTICS_MONTH", "")
    statistics_date = _dt.now().strftime("%Y/%m/%d")
    last_day = statistics_date
    stat_month_db = None
    if stat_month_raw and str(stat_month_raw).strip():
        s = str(stat_month_raw).strip().replace("-", "/")
        slen = len(s.replace("/", ""))
        try:
            if slen == 6:  # yyyyMM
                dt = _dt.strptime(s.replace("/", "") + "01", "%Y%m%d")
                statistics_date = dt.strftime("%Y/%m/%d")
                last_day = (dt.replace(month=dt.month % 12 + 1, day=1) if dt.month < 12
                            else dt.replace(year=dt.year + 1, month=1, day=1))
                last_day = (last_day - __import__('datetime').timedelta(days=1)).strftime("%Y/%m/%d")
            elif slen == 7:  # yyyy/MM
                dt = _dt.strptime(s.split("/")[0] + s.split("/")[1] + "01", "%Y%m%d")
                statistics_date = dt.strftime("%Y/%m/%d")
                last_day = (dt.replace(month=dt.month % 12 + 1, day=1) if dt.month < 12
                            else dt.replace(year=dt.year + 1, month=1, day=1))
                last_day = (last_day - __import__('datetime').timedelta(days=1)).strftime("%Y/%m/%d")
                stat_month_db = dt.strftime("%Y%m")
            elif slen == 8:  # yyyyMMdd
                dt = _dt.strptime(s.replace("/", ""), "%Y%m%d")
                statistics_date = dt.strftime("%Y/%m/%d")
                last_day = statistics_date
            elif slen >= 9:  # yyyy/MM/dd 或 yyyy-MM-dd
                dt = _dt.strptime(s.split(" ")[0], "%Y/%m/%d")
                statistics_date = dt.strftime("%Y/%m/%d")
                last_day = statistics_date
                stat_month_db = dt.strftime("%Y%m%d")
            else:
                statistics_date = s[:4] + "/12/01"
                last_day = s[:4] + "/12/31"
                stat_month_db = s[:4]
        except Exception:
            pass

    # ========== 标准 upsert ==========
    if record_id is not None:
        is_insert = False
        check_rows = db.execute_query(
            f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}")
        if not check_rows:
            return False, data

        # ApprovalProcess 校验（C# L453-457）
        if data.get("ApprovalProcess") is True:
            old_amount = check_rows[0].get("SHOPEXPENSE_AMOUNT", 0)
            new_amount = data.get("SHOPEXPENSE_AMOUNT", 0)
            try:
                if float(old_amount or 0) != float(new_amount or 0):
                    raise Exception("费用差异与实际情况不符，请联系中心财务进行修改调整！")
            except (ValueError, TypeError):
                pass

        # 执行更新
        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if key in DATE_FIELDS:
                fv = _fmt_month(value)
                set_parts.append(f"{key} = {fv}" if fv else f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {record_id}")

        # 历史备份（C# L467-468）
        try:
            db.execute_non_query(
                f"INSERT INTO T_SHOPEXPENSE_HIS SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {record_id}")
        except Exception:
            pass
    else:
        # ApprovalProcess 校验（C# L472-475）
        if data.get("ApprovalProcess") is True:
            if float(data.get("SHOPEXPENSE_AMOUNT", 0) or 0) != 0:
                raise Exception("费用差异与实际情况不符，请联系中心财务进行修改调整！")

        # 生成新 ID
        try:
            new_id = db.execute_scalar("SELECT SEQ_SHOPEXPENSE.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1
        data[PRIMARY_KEY] = new_id
        db_data[PRIMARY_KEY] = new_id
        record_id = new_id

        columns, values = [], []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if key in DATE_FIELDS:
                fv = _fmt_month(value)
                values.append(str(fv) if fv else "NULL")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(
            f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    # ========== 级联写 BUSINESSPROJECTSPLIT (C# L485-670) ==========
    pay_status = data.get("PAY_STATUS")
    if pay_status is not None and int(pay_status) in (0, 1):
        expense_type = int(data.get("SHOPEXPENSE_TYPE", 0) or 0)
        expense_amount = float(data.get("SHOPEXPENSE_AMOUNT", 0) or 0)
        staff_name = str(data.get("STAFF_NAME", "") or "")
        operate_date = str(data.get("OPERATE_DATE", "") or "")
        log_desc = f"{stat_month_raw}，费用类型{expense_type}，记录人：{staff_name}[{operate_date}]"
        sp_shop_id = data.get("SERVERPARTSHOP_ID")

        need_insert_split = is_insert

        if not is_insert:
            # 检查已有拆分记录（C# L493-523）
            split_rows = db.execute_query(
                f"SELECT * FROM T_BUSINESSPROJECTSPLIT "
                f"WHERE BUSINESSPROJECTSPLIT_STATE = 1 AND SHOPEXPENSE_ID = {record_id}")
            if split_rows:
                old_price = float(split_rows[0].get("ROYALTY_PRICE", 0) or 0)
                if old_price != expense_amount:
                    split_id = split_rows[0]["BUSINESSPROJECTSPLIT_ID"]
                    if expense_type < 9000 or expense_type == 9999:
                        db.execute_non_query(
                            f"""UPDATE T_BUSINESSPROJECTSPLIT
                                SET REVENUEDAILY_AMOUNT = -{expense_amount},
                                    ROYALTY_PRICE = {expense_amount},
                                    BUSINESSPROJECTSPLIT_DESC = '{log_desc}',
                                    RECORD_DATE = SYSDATE
                                WHERE BUSINESSPROJECTSPLIT_ID = {split_id}""")
                    else:
                        db.execute_non_query(
                            f"""UPDATE T_BUSINESSPROJECTSPLIT
                                SET ROYALTY_PRICE = {expense_amount},
                                    BUSINESSPROJECTSPLIT_DESC = '{log_desc}',
                                    RECORD_DATE = SYSDATE
                                WHERE BUSINESSPROJECTSPLIT_ID = {split_id}""")
            else:
                need_insert_split = True

        if need_insert_split and sp_shop_id:
            # 查询所属项目周期 — 4级回退（C# L529-599）
            project_row = None
            # 1. 精确匹配：门店在项目周期内
            prj_sql = f"""SELECT C.SHOPROYALTY_ID, B.REGISTERCOMPACT_ID, B.BUSINESSPROJECT_ID,
                    B.MERCHANTS_ID, B.SERVERPARTSHOP_ID, B.SERVERPARTSHOP_NAME,
                    B.BUSINESS_TYPE, C.STARTDATE, C.ENDDATE
                FROM T_BUSINESSPROJECT B, T_SHOPROYALTY C
                WHERE ',' || B.SERVERPARTSHOP_ID || ',' LIKE '%,{sp_shop_id},%'
                    AND C.STARTDATE <= TO_DATE('{last_day}','YYYY/MM/DD')
                    AND C.ENDDATE >= TO_DATE('{statistics_date}','YYYY/MM/DD')
                    AND B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID AND B.PROJECT_VALID = 1"""
            prj_rows = db.execute_query(prj_sql)
            last_month = False
            if not prj_rows:
                # 2. 项目最后一个月
                prj_sql = f"""SELECT C.SHOPROYALTY_ID, B.REGISTERCOMPACT_ID, B.BUSINESSPROJECT_ID,
                        B.MERCHANTS_ID, B.SERVERPARTSHOP_ID, B.SERVERPARTSHOP_NAME,
                        B.BUSINESS_TYPE, C.STARTDATE, C.ENDDATE
                    FROM T_BUSINESSPROJECT B, T_SHOPROYALTY C
                    WHERE ',' || B.SERVERPARTSHOP_ID || ',' LIKE '%,{sp_shop_id},%'
                        AND C.ENDDATE < TO_DATE('{statistics_date}','YYYY/MM/DD')
                        AND B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID AND B.PROJECT_VALID = 1"""
                prj_rows = db.execute_query(prj_sql)
                if prj_rows:
                    last_month = True
                else:
                    # 3. 装修期
                    prj_sql = f"""SELECT 0 AS SHOPROYALTY_ID, B.REGISTERCOMPACT_ID, B.BUSINESSPROJECT_ID,
                            B.MERCHANTS_ID, B.SERVERPARTSHOP_ID, B.SERVERPARTSHOP_NAME,
                            B.BUSINESS_TYPE, C.DECORATE_STARTDATE AS STARTDATE, C.DECORATE_ENDDATE AS ENDDATE
                        FROM T_RTBUSINESSPROJECT A, T_BUSINESSPROJECT B, T_REGISTERCOMPACTSUB C
                        WHERE A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
                            AND A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
                            AND ',' || B.SERVERPARTSHOP_ID || ',' LIKE '%,{sp_shop_id},%'
                            AND B.PROJECT_VALID = 1"""
                    prj_rows = db.execute_query(prj_sql)
                    if not prj_rows:
                        # 4. 项目开始前
                        prj_sql = f"""SELECT -1 AS SHOPROYALTY_ID, B.REGISTERCOMPACT_ID, B.BUSINESSPROJECT_ID,
                                B.MERCHANTS_ID, B.SERVERPARTSHOP_ID, B.SERVERPARTSHOP_NAME,
                                B.BUSINESS_TYPE, TO_DATE('{statistics_date}','YYYY/MM/DD') AS STARTDATE,
                                B.PROJECT_STARTDATE - 1 AS ENDDATE
                            FROM T_BUSINESSPROJECT B
                            WHERE ',' || B.SERVERPARTSHOP_ID || ',' LIKE '%,{sp_shop_id},%'
                                AND B.PROJECT_STARTDATE > TO_DATE('{statistics_date}','YYYY/MM/DD')
                                AND B.PROJECT_VALID = 1"""
                        prj_rows = db.execute_query(prj_sql)

            if prj_rows:
                # 按 ENDDATE 排序（lastMonth 降序）
                prj_rows.sort(key=lambda x: str(x.get("ENDDATE", "")), reverse=last_month)
                project_row = prj_rows[0]

                # ACCOUNT_TYPE 映射（C# L631-666）
                account_type = expense_type
                rev_daily = None
                if expense_type in (1000, 2000):  # 水费、电费
                    rev_daily = -expense_amount
                    account_type = 3000
                elif expense_type == 3000:  # 住宿费
                    rev_daily = -expense_amount
                    account_type = 4000
                elif expense_type == 4000:  # 就餐费
                    rev_daily = -expense_amount
                    account_type = 5000
                elif expense_type == 5000:  # 物业费
                    rev_daily = -expense_amount
                    account_type = 2000
                elif expense_type == 9000:  # 商家缴款
                    account_type = 9000
                elif expense_type < 9000 or expense_type == 9999:
                    rev_daily = -expense_amount
                    account_type = expense_type
                else:
                    account_type = 9000

                # 插入 BUSINESSPROJECTSPLIT
                rev_col = f", REVENUEDAILY_AMOUNT" if rev_daily is not None else ""
                rev_val = f", {rev_daily}" if rev_daily is not None else ""
                try:
                    split_id = db.execute_scalar("SELECT SEQ_BUSINESSPROJECTSPLIT.NEXTVAL FROM DUAL")
                except Exception:
                    split_id = (db.execute_scalar(
                        "SELECT MAX(BUSINESSPROJECTSPLIT_ID) FROM T_BUSINESSPROJECTSPLIT") or 0) + 1
                db.execute_non_query(
                    f"""INSERT INTO T_BUSINESSPROJECTSPLIT (
                            BUSINESSPROJECTSPLIT_ID, STATISTICS_DATE, SHOPROYALTY_ID,
                            REGISTERCOMPACT_ID, BUSINESSPROJECT_ID, MERCHANTS_ID,
                            SERVERPART_ID, SERVERPART_NAME, SERVERPARTSHOP_ID,
                            SERVERPARTSHOP_NAME, BUSINESS_TYPE, STARTDATE, ENDDATE,
                            ROYALTY_PRICE, RECORD_DATE, BUSINESSPROJECTSPLIT_STATE,
                            BUSINESSPROJECTSPLIT_DESC, SHOPEXPENSE_ID, ACCOUNT_TYPE
                            {rev_col})
                        VALUES ({split_id},
                            TO_DATE('{last_day}','YYYY/MM/DD'),
                            {project_row.get('SHOPROYALTY_ID', 0)},
                            {project_row.get('REGISTERCOMPACT_ID', 0)},
                            {project_row.get('BUSINESSPROJECT_ID', 0)},
                            {project_row.get('MERCHANTS_ID', 0)},
                            {data.get('SERVERPART_ID', 0)},
                            '{data.get('SERVERPART_NAME', '')}',
                            '{project_row.get('SERVERPARTSHOP_ID', '')}',
                            '{project_row.get('SERVERPARTSHOP_NAME', '')}',
                            {project_row.get('BUSINESS_TYPE', 0)},
                            {project_row.get('STARTDATE', 'NULL')},
                            {project_row.get('ENDDATE', 'NULL')},
                            {expense_amount}, SYSDATE, 1,
                            '{log_desc}', {record_id}, {account_type}
                            {rev_val})""")

    return True, data


def delete_shopexpense(db: DatabaseHelper, se_id: int,
                       staff_id: int = None, staff_name: str = "") -> bool:
    """
    删除门店费用 — C# SHOPEXPENSEHelper.DeleteSHOPEXPENSE (L685-712)
    1. 级联作废 BUSINESSPROJECTSPLIT（按 SHOPEXPENSE_ID）
    2. 备份当前记录到历史库
    3. 软删除 + 记录操作人 + 追加备注
    """
    if not se_id:
        return False
    # 1. 级联作废经营项目拆分表
    try:
        db.execute_non_query(
            f"UPDATE T_BUSINESSPROJECTSPLIT SET BUSINESSPROJECTSPLIT_STATE = 0 "
            f"WHERE SHOPEXPENSE_ID = {se_id}")
    except Exception as e:
        logger.warning(f"级联作废 BUSINESSPROJECTSPLIT 失败: {e}")

    # 2. 备份到历史库（如果历史表存在）
    try:
        db.execute_non_query(
            f"INSERT INTO T_SHOPEXPENSE_HIS SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {se_id}")
    except Exception:
        pass  # 历史表可能不存在

    # 3. 软删除 + 记录操作人信息
    from datetime import datetime
    delete_desc = f"{staff_name}[{staff_id}]于{datetime.now()}作废门店费用"
    staff_sql = ""
    if staff_id is not None:
        staff_sql = f", STAFF_ID = {staff_id}"
    if staff_name:
        staff_sql += f", STAFF_NAME = '{staff_name}'"
    affected = db.execute_non_query(
        f"""UPDATE {TABLE_NAME}
            SET SHOPEXPENSE_STATE = 0, OPERATE_DATE = SYSDATE{staff_sql},
                SHOPEXPENSE_DESC = CASE WHEN SHOPEXPENSE_DESC IS NOT NULL
                    THEN SHOPEXPENSE_DESC || CHR(10) END || '{delete_desc}'
            WHERE {PRIMARY_KEY} = {se_id}""")
    return affected > 0


def approve_shopexpense(db: DatabaseHelper, data: dict) -> tuple[bool, dict]:
    """
    审批门店费用（对应 ApproveSHOPEXPENSE 接口）
    原 C# 中 Approve 实际调用 SynchroSHOPEXPENSE 并带 ApprovalProcess=true
    """
    data["ApprovalProcess"] = True
    return synchro_shopexpense(db, data)
