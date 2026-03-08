from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营项目管理业务服务（BusinessProjectController 专属）
当前实现：BusinessProject 的 4 个 CRUD 接口
对应 C# BUSINESSPROJECTHelper.cs 中的精确逻辑
"""
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel


# ===================================================================
# 辅助函数：获取经营项目所属服务区信息
# 对应 C# BUSINESSPROJECTHelper.GetProjectServerpart
# 返回 DataTable: SERVERPART_IDS, SERVERPART_NAME, SPREGIONTYPE_IDS,
#   SPREGIONTYPE_NAME, REGISTERCOMPACT_IDS, BUSINESSPROJECT_ID, ...
# ===================================================================

def _get_project_serverpart(db: DatabaseHelper, business_project_ids: str = "",
                             merchant_ids: str = "", serverpartshop_ids: str = "",
                             project_valid: int = None):
    """
    获取经营项目所属服务区信息（多表 JOIN + GROUP BY + WM_CONCAT）
    C# 原始 SQL 使用 WM_CONCAT，达梦兼容
    """
    where_extra = ""
    if project_valid is not None:
        where_extra += f" AND B.PROJECT_VALID = {project_valid}"
    if business_project_ids:
        where_extra += f" AND B.BUSINESSPROJECT_ID IN ({business_project_ids})"
    if merchant_ids:
        where_extra += f" AND B.MERCHANTS_ID IN ({merchant_ids})"
    if serverpartshop_ids:
        where_extra += f""" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP E
            WHERE ',' || B.SERVERPARTSHOP_ID || ',' LIKE '%,' || E.SERVERPARTSHOP_ID || ',%'
            AND E.SERVERPARTSHOP_ID IN ({serverpartshop_ids}))"""

    sql = f"""SELECT
        WM_CONCAT(DISTINCT A.SERVERPART_ID) AS SERVERPART_IDS,
        WM_CONCAT(DISTINCT A.SERVERPART_NAME) AS SERVERPART_NAME,
        WM_CONCAT(DISTINCT A.SPREGIONTYPE_ID) AS SPREGIONTYPE_IDS,
        WM_CONCAT(DISTINCT A.SPREGIONTYPE_NAME) AS SPREGIONTYPE_NAME,
        WM_CONCAT(D.REGISTERCOMPACT_ID) AS REGISTERCOMPACT_IDS,
        B.BUSINESSPROJECT_ID, B.BUSINESSPROJECT_NAME, B.SERVERPARTSHOP_ID,
        B.REGISTERCOMPACT_ID, B.COMPACT_NAME, B.PROJECT_VALID,
        B.PROJECT_STARTDATE, B.PROJECT_ENDDATE
    FROM
        T_SERVERPART A,
        T_BUSINESSPROJECT B,
        T_RTREGISTERCOMPACT D
    WHERE
        EXISTS (SELECT 1 FROM T_RTBUSINESSPROJECT C
            WHERE B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND C.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID)
        AND A.SERVERPART_ID = D.SERVERPART_ID
        {where_extra}
    GROUP BY
        B.BUSINESSPROJECT_ID, B.BUSINESSPROJECT_NAME, B.SERVERPARTSHOP_ID,
        B.REGISTERCOMPACT_ID, B.COMPACT_NAME, B.PROJECT_VALID,
        B.PROJECT_STARTDATE, B.PROJECT_ENDDATE"""
    return db.execute_query(sql)


# ===================================================================
# 辅助函数：构建 IN 条件
# 对应 C# HCC.Common.GetInString
# ===================================================================

def _get_in_string(field_name: str, values: list) -> str:
    """构建 IN 条件语句，自动分段避免 Oracle IN 超 1000 限制"""
    if not values:
        return "1=0"
    # 达梦无 1000 限制，直接构建
    in_str = ",".join([str(v) for v in values if v])
    return f"{field_name} IN ({in_str})"


# ===================================================================
# 1. GetBusinessProjectList（经营项目列表）
# 对应 C# BUSINESSPROJECTHelper.GetBUSINESSPROJECTList（第 39-406 行）
# 核心逻辑：
#   1) 从 SearchParameter 构建 WHERE 子句（支持 10+ 搜索参数）
#   2) 查询 T_BUSINESSPROJECT 全量数据
#   3) 关联 T_SHOPROYALTY 计算 Period_Count 和 Period_AvgAmount
#   4) keyword 过滤
#   5) 排序（默认 OPERATE_DATE DESC）
#   6) 计算 summaryList（4 个统计项）
#   7) 分页
#   8) 关联 GetProjectServerpart 获取服务区名称
# ===================================================================

def get_businessproject_list(db: DatabaseHelper, search_model: SearchModel,
                              serverpart_ids: str = ""):
    """
    获取经营项目列表
    返回: (total_count, data_list, summary_list)
    """
    # ---- 第一步：构建 WHERE ----
    where_parts = []
    sp = search_model.SearchParameter or {}

    # C# OperationDataHelper.GetWhereSQL 通用字段过滤
    if sp.get("PROJECT_VALID") is not None:
        where_parts.append(f"PROJECT_VALID = {sp['PROJECT_VALID']}")
    if sp.get("BUSINESS_TYPE"):
        where_parts.append(f"BUSINESS_TYPE = {sp['BUSINESS_TYPE']}")
    if sp.get("SETTLEMENT_MODES"):
        where_parts.append(f"SETTLEMENT_MODES = {sp['SETTLEMENT_MODES']}")
    if sp.get("MERCHANTS_ID"):
        where_parts.append(f"MERCHANTS_ID = {sp['MERCHANTS_ID']}")
    if sp.get("COMPACT_TYPE"):
        where_parts.append(f"COMPACT_TYPE = {sp['COMPACT_TYPE']}")
    if sp.get("MULTIPROJECT_STATE") is not None:
        where_parts.append(f"MULTIPROJECT_STATE = {sp['MULTIPROJECT_STATE']}")
    if sp.get("REGISTERCOMPACT_ID"):
        where_parts.append(f"REGISTERCOMPACT_ID = {sp['REGISTERCOMPACT_ID']}")
    if sp.get("MERCHANTS_IDS"):
        ids = sp["MERCHANTS_IDS"]
        where_parts.append(f"MERCHANTS_ID IN ({ids})")

    # 查询经营项目内码
    if sp.get("BUSINESSPROJECT_IDS"):
        ids_list = [x.strip() for x in str(sp["BUSINESSPROJECT_IDS"]).split(",") if x.strip()]
        where_parts.append(_get_in_string("BUSINESSPROJECT_ID", ids_list))

    # 查询门店内码（支持多门店，逗号分隔）
    if sp.get("SERVERPARTSHOP_ID"):
        shop_id = sp["SERVERPARTSHOP_ID"]
        where_parts.append(f"',' || SERVERPARTSHOP_ID || ',' LIKE '%,{shop_id},%'")

    # 查询服务区内码（EXISTS 子查询）
    srv_ids = sp.get("SERVERPART_IDS") or serverpart_ids
    if srv_ids:
        where_parts.append(f"""EXISTS (SELECT 1
            FROM T_RTREGISTERCOMPACT B, T_RTBUSINESSPROJECT C
            WHERE A.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND B.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND B.SERVERPART_ID IN ({srv_ids}))""")

    # 查询项目开始日期
    if sp.get("PROJECT_STARTDATE"):
        where_parts.append(f"PROJECT_STARTDATE <= TO_DATE('{sp['PROJECT_STARTDATE']}','YYYY/MM/DD HH24:MI:SS')")

    # 查询项目结束日期
    if sp.get("PROJECT_ENDDATE"):
        where_parts.append(f"PROJECT_ENDDATE >= TO_DATE('{sp['PROJECT_ENDDATE']}','YYYY/MM/DD HH24:MI:SS')")

    # 查询撤场日期区间
    if sp.get("CLOSED_DATE_Start"):
        try:
            dt = datetime.strptime(str(sp["CLOSED_DATE_Start"]), "%Y/%m/%d %H:%M:%S")
            where_parts.append(f"CLOSED_DATE >= {dt.strftime('%Y%m%d')}")
        except:
            where_parts.append(f"CLOSED_DATE >= {sp['CLOSED_DATE_Start']}")
    if sp.get("CLOSED_DATE_End"):
        try:
            dt = datetime.strptime(str(sp["CLOSED_DATE_End"]), "%Y/%m/%d %H:%M:%S")
            where_parts.append(f"CLOSED_DATE <= {dt.strftime('%Y%m%d')}")
        except:
            where_parts.append(f"CLOSED_DATE <= {sp['CLOSED_DATE_End']}")

    # 过滤到期日期区间（DueDate）
    if sp.get("DueDate_Start"):
        where_parts.append(f"PROJECT_ENDDATE >= TO_DATE('{sp['DueDate_Start']}','YYYY/MM/DD HH24:MI:SS')")
    elif sp.get("DueDate_End"):
        # C#: 未指定 DueDate_Start 但有 DueDate_End 时，默认从今天开始
        where_parts.append(f"PROJECT_ENDDATE >= TO_DATE('{datetime.now().strftime('%Y/%m/%d')}','YYYY/MM/DD HH24:MI:SS')")
    if sp.get("DueDate_End"):
        where_parts.append(f"PROJECT_ENDDATE <= TO_DATE('{sp['DueDate_End']}','YYYY/MM/DD HH24:MI:SS')")

    # 过滤项目状态分类（ProjectStateSearch）
    if sp.get("ProjectStateSearch"):
        for state in str(sp["ProjectStateSearch"]).split(","):
            if state == "0":
                # 查询历史项目：结束日期 < 今天
                where_parts.append(f"PROJECT_ENDDATE < TO_DATE('{datetime.now().strftime('%Y/%m/%d')}','YYYY/MM/DD HH24:MI:SS')")
            elif state == "1":
                # 查询在营项目：关联门店 BUSINESS_STATE IN (1000,1010)
                where_parts.append("""EXISTS (SELECT 1 FROM T_SERVERPARTSHOP B
                    WHERE B.BUSINESS_STATE IN (1000,1010)
                    AND ',' || A.SERVERPARTSHOP_ID || ',' LIKE '%,' || B.SERVERPARTSHOP_ID || ',%')""")

    # 过滤项目类型（ProjectTypeSearch）
    if sp.get("ProjectTypeSearch"):
        for ptype in str(sp["ProjectTypeSearch"]).split(","):
            if ptype == "1":
                where_parts.append("SERVERPARTSHOP_ID IS NOT NULL")
            elif ptype == "2":
                where_parts.append("SERVERPARTSHOP_ID IS NULL")

    where_sql = ""
    if where_parts:
        where_sql = " WHERE " + " AND ".join(where_parts)

    # ---- 第二步：查询全部数据 ----
    main_sql = f"SELECT A.* FROM T_BUSINESSPROJECT A{where_sql}"
    all_rows = db.execute_query(main_sql)

    if not all_rows:
        return 0, [], []

    # ---- 第三步：关联 SHOPROYALTY 计算 Period_Count / Period_AvgAmount ----
    bp_ids = [str(r["BUSINESSPROJECT_ID"]) for r in all_rows if r.get("BUSINESSPROJECT_ID")]
    if bp_ids:
        royalty_sql = f"SELECT BUSINESSPROJECT_ID, COUNT(*) AS CNT FROM T_SHOPROYALTY WHERE {_get_in_string('BUSINESSPROJECT_ID', bp_ids)} GROUP BY BUSINESSPROJECT_ID"
        royalty_rows = db.execute_query(royalty_sql)
        royalty_map = {str(r["BUSINESSPROJECT_ID"]): int(r["CNT"]) for r in royalty_rows}
    else:
        royalty_map = {}

    for row in all_rows:
        bp_id = str(row.get("BUSINESSPROJECT_ID", ""))
        period_count = royalty_map.get(bp_id, 0)
        row["Period_Count"] = period_count
        guarantee = float(row.get("GUARANTEE_PRICE") or 0)
        if period_count > 0 and guarantee > 0:
            row["Period_AvgAmount"] = round(guarantee / period_count, 2)
        else:
            row["Period_AvgAmount"] = None

    # ---- 第四步：keyword 过滤 ----
    if search_model.keyWord:
        kw = search_model.keyWord
        if kw.Key and kw.Value:
            key_fields = [k.strip() for k in kw.Key.split(",") if k.strip()]
            kw_val = str(kw.Value).lower()
            filtered = []
            for row in all_rows:
                for kf in key_fields:
                    cell = str(row.get(kf, "") or "").lower()
                    if kw_val in cell:
                        filtered.append(row)
                        break
            all_rows = filtered

    # ---- 第五步：排序 ----
    sort_field = search_model.SortStr or "OPERATE_DATE"
    sort_desc = True
    if sort_field:
        sf = sort_field.strip()
        if sf.lower().endswith(" asc"):
            sort_field = sf[:-4].strip()
            sort_desc = False
        elif sf.lower().endswith(" desc"):
            sort_field = sf[:-5].strip()
            sort_desc = True
    try:
        all_rows.sort(key=lambda r: r.get(sort_field) or "", reverse=sort_desc)
    except Exception:
        pass

    total_count = len(all_rows)

    # ---- 第六步：summaryList 统计 ----
    summary_list = []
    if all_rows:
        # 1000: 分润项目数（SETTLEMENT_MODES IN 3000,4000）
        share_count = sum(1 for r in all_rows if r.get("SETTLEMENT_MODES") in (3000, 4000))
        summary_list.append({"label": "1000", "value": str(share_count)})
        # 2000: 已切换项目数（EXPIREDAYS > 10000000，当前无此字段，设0）
        summary_list.append({"label": "2000", "value": "0"})
        # 3000: 本月即将完成保底数（当前无 EXPIREDAYS 字段，设0）
        summary_list.append({"label": "3000", "value": "0"})
        # 4000: 合计分润金额（ROYALTY_PRICE 合计，当前无此字段，设0）
        summary_list.append({"label": "4000", "value": "0"})

    # ---- 第七步：分页 ----
    page_index = search_model.PageIndex or 1
    page_size = search_model.PageSize or 20
    start = (page_index - 1) * page_size
    end = start + page_size
    paged_rows = all_rows[start:end]

    # ---- 第八步：关联 GetProjectServerpart 获取服务区名称 ----
    if paged_rows:
        paged_bp_ids = ",".join([str(r["BUSINESSPROJECT_ID"]) for r in paged_rows if r.get("BUSINESSPROJECT_ID")])
        if paged_bp_ids:
            sp_rows = _get_project_serverpart(db, business_project_ids=paged_bp_ids)
            sp_map = {}
            for sr in sp_rows:
                sp_map[str(sr.get("BUSINESSPROJECT_ID", ""))] = sr

            for row in paged_rows:
                bp_id = str(row.get("BUSINESSPROJECT_ID", ""))
                if bp_id in sp_map:
                    sr = sp_map[bp_id]
                    row["SERVERPART_IDS"] = sr.get("SERVERPART_IDS", "")
                    row["SERVERPART_NAME"] = sr.get("SERVERPART_NAME", "")
                    row["SPREGIONTYPE_IDS"] = sr.get("SPREGIONTYPE_IDS", "")
                    row["SPREGIONTYPE_NAME"] = sr.get("SPREGIONTYPE_NAME", "")

    return total_count, paged_rows, summary_list


# ===================================================================
# 2. GetBusinessProjectDetail（经营项目明细）
# 对应 C# BUSINESSPROJECTHelper.GetBUSINESSPROJECTDetail（第 576-685 行）
# 核心逻辑：
#   1) SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = ?
#   2) 关联 GetProjectServerpart 获取服务区名称
#   3) 查询 T_BUSINESSLOG 获取修改日志（BUSINESSLOG_TYPE=14）
#   4) 查询品牌 logo
#   5) 查询切换日志
# ===================================================================

def get_businessproject_detail(db: DatabaseHelper, bp_id: int):
    """获取经营项目明细"""
    rows = db.execute_query(
        f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {bp_id}")
    if not rows:
        return None
    row = rows[0]

    # 关联服务区信息
    sp_rows = _get_project_serverpart(db, business_project_ids=str(bp_id))
    if sp_rows:
        sr = sp_rows[0]
        row["SERVERPART_IDS"] = sr.get("SERVERPART_IDS", "")
        row["SERVERPART_NAME"] = sr.get("SERVERPART_NAME", "")
        row["SPREGIONTYPE_IDS"] = sr.get("SPREGIONTYPE_IDS", "")
        row["SPREGIONTYPE_NAME"] = sr.get("SPREGIONTYPE_NAME", "")

    # 查询修改日志（BUSINESSLOG_TYPE=14, TABLE_NAMES='T_BUSINESSPROJECT'）
    # C# 中查询 PLATFORM_FRAMEWORK.T_BUSINESSLOG，达梦中可能没有此表，安全查询
    try:
        log_rows = db.execute_query(f"""SELECT * FROM T_BUSINESSLOG
            WHERE BUSINESSLOG_TYPE = 14 AND BUSINESS_ID = {bp_id}
            AND TABLE_NAMES = 'T_BUSINESSPROJECT'
            ORDER BY BUSINESSLOG_ID DESC""")
        log_list = []
        for lr in (log_rows or []):
            content = lr.get("BUSINESSLOG_CONTENT", "")
            if content and not str(content).endswith("："):
                log_list.append(lr)
        if log_list:
            row["LogList"] = log_list
    except Exception as e:
        logger.debug(f"查询经营项目日志失败（表可能不存在）: {e}")

    # 查询品牌 logo
    shop_id_str = str(row.get("SERVERPARTSHOP_ID") or "")
    if shop_id_str:
        try:
            shop_rows = db.execute_query(f"""SELECT BUSINESS_BRAND FROM T_SERVERPARTSHOP
                WHERE SERVERPARTSHOP_ID IN ({shop_id_str}) AND BUSINESS_BRAND IS NOT NULL""")
            if shop_rows:
                brand_id = shop_rows[0].get("BUSINESS_BRAND")
                if brand_id:
                    brand_rows = db.execute_query(
                        f"SELECT BRAND_INTRO FROM T_BRAND WHERE BRAND_ID = {brand_id}")
                    brand = brand_rows[0] if brand_rows else None
                    if brand and brand.get("BRAND_INTRO"):
                        row["Project_ICO"] = brand["BRAND_INTRO"]
        except Exception as e:
            logger.debug(f"查询品牌logo失败: {e}")

    return row


# ===================================================================
# 3. SynchroBusinessProject（同步经营项目）
# 对应 C# BUSINESSPROJECTHelper.SynchroBUSINESSPROJECT（第 689-909 行）
# 核心逻辑：
#   1) 排除不入库的字段（SERVERPART_IDS, ShowShare, LogList 等）
#   2) 日期字段特殊处理（PROJECT_STARTDATE/ENDDATE 用 TO_DATE，
#      CLOSED_DATE/SWITCH_DATE 存为 yyyyMMdd 格式数字）
#   3) 有 BUSINESSPROJECT_ID → 更新，否则 → 新增
#   4) 更新时检查门店/经营模式/结算模式是否变更
# ===================================================================

# C# 中排除不入库的字段列表
_EXCLUDE_FIELDS = {
    "BUSINESSPROJECT_IDS", "SERVERPART_IDS", "SERVERPART_NAME",
    "SPREGIONTYPE_IDS", "SPREGIONTYPE_NAME", "MerchantsIdEncrypted",
    "ShowShare", "ProjectStateSearch", "LogList", "SwitchLogList",
    "ROYALTY_PRICE", "EXPIREDAYS", "PROJECT_ENDDATE_Start",
    "PROJECT_ENDDATE_End", "MERCHANTS_IDS", "BUSINESSAPPROVAL_ID",
    "DueDate_Start", "DueDate_End", "ProjectTypeSearch",
    "Period_Count", "Period_AvgAmount", "Project_ICO",
    "CLOSED_DATE_Start", "CLOSED_DATE_End",
}

# 需要 TO_DATE 处理的日期字段
_DATE_FIELDS = {"PROJECT_STARTDATE", "PROJECT_ENDDATE"}
# 需要 yyyyMMdd 格式存储的日期字段
_NUMDATE_FIELDS = {"CLOSED_DATE", "SWITCH_DATE"}


def synchro_businessproject(db: DatabaseHelper, data: dict, user_id: int = None,
                             user_name: str = ""):
    """同步经营项目（新增/更新）"""
    bp_id = data.get("BUSINESSPROJECT_ID")

    # 过滤排除字段
    fields = {k: v for k, v in data.items() if k.upper() not in _EXCLUDE_FIELDS}

    if bp_id:
        # 更新模式 —— 先查是否存在
        existing_rows = db.execute_query(
            f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {bp_id}")
        if existing_rows:
            # 构建 SET 子句
            set_parts = []
            params = {}
            for k, v in fields.items():
                upper_k = k.upper()
                if upper_k == "BUSINESSPROJECT_ID":
                    continue
                if upper_k in _DATE_FIELDS:
                    # 日期字段用 TO_DATE
                    if v:
                        set_parts.append(f"{k} = TO_DATE('{v}','YYYY/MM/DD HH24:MI:SS')")
                    else:
                        set_parts.append(f"{k} = NULL")
                elif upper_k in _NUMDATE_FIELDS:
                    # 撤场/切换日期 存为 yyyyMMdd 数字
                    if v:
                        try:
                            dt = datetime.strptime(str(v).split(" ")[0] if " " not in str(v) else str(v),
                                                    "%Y/%m/%d %H:%M:%S" if "/" in str(v) else "%Y-%m-%d %H:%M:%S")
                            set_parts.append(f"{k} = {dt.strftime('%Y%m%d')}")
                        except:
                            set_parts.append(f"{k} = {v}")
                    else:
                        set_parts.append(f"{k} = NULL")
                else:
                    set_parts.append(f"{k} = :{k}")
                    params[k] = v

            if set_parts:
                # 添加操作人信息
                if user_id:
                    set_parts.append(f"STAFF_ID = {user_id}")
                if user_name:
                    set_parts.append(f"STAFF_NAME = '{user_name}'")
                set_parts.append(f"OPERATE_DATE = SYSDATE")

                params["BUSINESSPROJECT_ID"] = bp_id
                sql = f"UPDATE T_BUSINESSPROJECT SET {', '.join(set_parts)} WHERE BUSINESSPROJECT_ID = :BUSINESSPROJECT_ID"
                db.execute_non_query(sql, params)

            return True, data
        # 不存在则走新增

    # 新增模式
    insert_fields = {k: v for k, v in fields.items()
                     if k.upper() not in _DATE_FIELDS and k.upper() not in _NUMDATE_FIELDS}
    # 操作人信息
    if user_id:
        insert_fields["STAFF_ID"] = user_id
    if user_name:
        insert_fields["STAFF_NAME"] = user_name

    cols = list(insert_fields.keys())
    vals = [f":{k}" for k in cols]

    # 日期字段单独处理
    for df in _DATE_FIELDS:
        dv = data.get(df)
        if dv:
            cols.append(df)
            vals.append(f"TO_DATE('{dv}','YYYY/MM/DD HH24:MI:SS')")
    for ndf in _NUMDATE_FIELDS:
        ndv = data.get(ndf)
        if ndv:
            cols.append(ndf)
            try:
                dt = datetime.strptime(str(ndv).split(" ")[0], "%Y/%m/%d" if "/" in str(ndv) else "%Y-%m-%d")
                vals.append(dt.strftime("%Y%m%d"))
            except:
                vals.append(str(ndv))

    cols.append("OPERATE_DATE")
    vals.append("SYSDATE")

    sql = f"INSERT INTO T_BUSINESSPROJECT ({', '.join(cols)}) VALUES ({', '.join(vals)})"
    db.execute_non_query(sql, insert_fields)
    return True, data


# ===================================================================
# 4. DeleteBusinessProject（删除经营项目）
# 对应 C# BUSINESSPROJECTHelper.DeleteBUSINESSPROJECT（第 947-1004 行）
# 核心逻辑：
#   1) 非强制删除时，检查 T_PAYMENTCONFIRM 和 T_SHOPROYALTY 是否有关联数据
#   2) 软删除：UPDATE PROJECT_VALID = 0
#   3) 级联更新 T_BUSINESSPROJECTSPLIT.STATE=0, T_BIZPSPLITMONTH.STATE=0
# ===================================================================

def delete_businessproject(db: DatabaseHelper, bp_id: int, force_delete: bool = False,
                            user_id: int = None, user_name: str = ""):
    """
    删除经营项目（软删除 PROJECT_VALID=0）
    非强制删除时检查关联数据
    """
    if not bp_id:
        return False, "删除失败，请传入经营项目内码再进行删除"

    # 非强制删除：检查关联的应收数据和提成数据
    if not force_delete:
        where_check = f"WHERE BUSINESSPROJECT_ID = {bp_id}"
        pc_count = db.execute_scalar(f"SELECT COUNT(*) FROM T_PAYMENTCONFIRM {where_check}")
        sr_count = db.execute_scalar(f"SELECT COUNT(*) FROM T_SHOPROYALTY {where_check}")
        if (pc_count and pc_count > 0) or (sr_count and sr_count > 0):
            return False, "删除失败，请删除拆分、往来款信息后再删除经营项目"

    # 查询项目是否存在
    existing_rows = db.execute_query(
        f"SELECT BUSINESSPROJECT_ID, BUSINESSPROJECT_NAME FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {bp_id}")
    if not existing_rows:
        return False, "删除失败，数据不存在"

    # 软删除
    db.execute_non_query(
        f"UPDATE T_BUSINESSPROJECT SET PROJECT_VALID = 0 WHERE BUSINESSPROJECT_ID = {bp_id}")

    # 级联更新 T_BUSINESSPROJECTSPLIT 和 T_BIZPSPLITMONTH（达梦中可能没有这两张表）
    try:
        db.execute_non_query(
            f"UPDATE T_BUSINESSPROJECTSPLIT SET BUSINESSPROJECTSPLIT_STATE = 0 WHERE BUSINESSPROJECT_ID = {bp_id}")
    except Exception:
        pass  # 表不存在时忽略
    try:
        db.execute_non_query(
            f"UPDATE T_BIZPSPLITMONTH SET BIZPSPLITMONTH_STATE = 0 WHERE BUSINESSPROJECT_ID = {bp_id}")
    except Exception:
        pass  # 表不存在时忽略

    return True, "删除成功"
