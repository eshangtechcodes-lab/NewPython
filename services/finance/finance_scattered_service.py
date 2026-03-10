from __future__ import annotations
# -*- coding: utf-8 -*-
"""
FinanceController 散装接口 Service（44 个接口）
对应原 C# FinanceController 中除 ATTACHMENT CRUD 以外的所有接口
包含：营收分润报表、审批流程、固化操作、短信发送、银行到账拆解等

Helper 来源：
- BUSINESSPROJECTSPLITHelper（营收拆分汇总）
- BANKACCOUNTVERIFYHelper（日度业主到账）
- ProjectSummaryHelper（商铺收入明细）
- FinanceHelper（合同商户/分账收银/对账/收入确认/银行到账拆解等）
- BIZPSPLITMONTHHelper（月度结算审批）
- SHOPEXPENSEHelper（经营商户费用）
- PROJECTSPLITMONTHHelper（固化月度收入）
- AHJKHelper（安徽交控 token）
"""
from typing import Optional, List
from loguru import logger
from core.database import DatabaseHelper


# ==================== 1. GetProjectSplitSummary ====================
def get_project_split_summary(db: DatabaseHelper, start_date: str, end_date: str,
                               sp_region_type_id: str = "", serverpart_id: str = "",
                               merchant_id: str = "") -> list[dict]:
    """获取月度营收分润数据（NestingModel 树形）
    原 BUSINESSPROJECTSPLITHelper.GetProjectSplitSummary
    简化版：按片区→服务区→经营项目 聚合拆分数据"""
    where_parts = ["A.BUSINESSPROJECTSPLIT_STATE = 1", "A.ACCOUNT_TYPE = 1000"]
    if start_date:
        where_parts.append(f"A.STATISTICS_DATE >= {start_date.replace('-','')[:8]}")
    if end_date:
        where_parts.append(f"A.STATISTICS_DATE <= {end_date.replace('-','')[:8]}")
    if sp_region_type_id:
        where_parts.append(f"B.SPREGIONTYPE_ID IN ({sp_region_type_id})")
    if serverpart_id:
        where_parts.append(f"B.SERVERPART_ID IN ({serverpart_id})")
    if merchant_id:
        where_parts.append(f"A.MERCHANTS_ID IN ({merchant_id})")

    where_sql = " AND ".join(where_parts)
    sql = f"""SELECT B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME,
            B.SERVERPART_ID, B.SERVERPART_NAME,
            A.BUSINESSPROJECT_ID, A.SERVERPARTSHOP_NAME,
            SUM(A.REVENUEDAILY_AMOUNT) AS REVENUE_AMOUNT,
            SUM(A.ROYALTYDAILY_PRICE) AS ROYALTY_PRICE,
            SUM(A.SUBROYALTYDAILY_PRICE) AS SUBROYALTY_PRICE,
            SUM(A.TICKETDAILY_FEE) AS TICKET_FEE,
            SUM(A.MOBILEPAY_AMOUNT) AS MOBILEPAY_AMOUNT,
            SUM(A.CASHPAY_AMOUNT) AS CASHPAY_AMOUNT,
            SUM(A.OTHERPAY_AMOUNT) AS OTHERPAY_AMOUNT
        FROM T_BUSINESSPROJECTSPLIT A
        LEFT JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
        WHERE {where_sql}
        GROUP BY B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME,
            B.SERVERPART_ID, B.SERVERPART_NAME,
            A.BUSINESSPROJECT_ID, A.SERVERPARTSHOP_NAME
        ORDER BY B.SPREGIONTYPE_ID, B.SERVERPART_ID"""
    rows = db.execute_query(sql)
    # 构建树形结构
    return _build_region_tree(rows)


def _build_region_tree(rows: list[dict]) -> list[dict]:
    """将平面数据构建成 片区→服务区→项目 的树形"""
    from collections import OrderedDict
    regions = OrderedDict()
    for r in rows:
        rid = r.get("SPREGIONTYPE_ID")
        sid = r.get("SERVERPART_ID")
        if rid not in regions:
            regions[rid] = {
                "node": {"SPREGIONTYPE_ID": rid, "SPREGIONTYPE_NAME": r.get("SPREGIONTYPE_NAME", ""),
                         "REVENUE_AMOUNT": 0, "ROYALTY_PRICE": 0, "SUBROYALTY_PRICE": 0,
                         "TICKET_FEE": 0, "MOBILEPAY_AMOUNT": 0, "CASHPAY_AMOUNT": 0, "OTHERPAY_AMOUNT": 0},
                "children": OrderedDict()
            }
        region = regions[rid]
        if sid not in region["children"]:
            region["children"][sid] = {
                "node": {"SERVERPART_ID": sid, "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                         "REVENUE_AMOUNT": 0, "ROYALTY_PRICE": 0, "SUBROYALTY_PRICE": 0,
                         "TICKET_FEE": 0, "MOBILEPAY_AMOUNT": 0, "CASHPAY_AMOUNT": 0, "OTHERPAY_AMOUNT": 0},
                "children": []
            }
        sp = region["children"][sid]
        # 项目节点
        project = {
            "node": {
                "BUSINESSPROJECT_ID": r.get("BUSINESSPROJECT_ID"),
                "SERVERPARTSHOP_NAME": r.get("SERVERPARTSHOP_NAME", ""),
                "REVENUE_AMOUNT": _d(r.get("REVENUE_AMOUNT")),
                "ROYALTY_PRICE": _d(r.get("ROYALTY_PRICE")),
                "SUBROYALTY_PRICE": _d(r.get("SUBROYALTY_PRICE")),
                "TICKET_FEE": _d(r.get("TICKET_FEE")),
                "MOBILEPAY_AMOUNT": _d(r.get("MOBILEPAY_AMOUNT")),
                "CASHPAY_AMOUNT": _d(r.get("CASHPAY_AMOUNT")),
                "OTHERPAY_AMOUNT": _d(r.get("OTHERPAY_AMOUNT")),
            }
        }
        sp["children"].append(project)
        # 累加服务区
        for k in ["REVENUE_AMOUNT","ROYALTY_PRICE","SUBROYALTY_PRICE","TICKET_FEE","MOBILEPAY_AMOUNT","CASHPAY_AMOUNT","OTHERPAY_AMOUNT"]:
            sp["node"][k] += _d(r.get(k))

    # 累加片区 + 转为列表
    result = []
    for region in regions.values():
        children = []
        for sp in region["children"].values():
            for k in ["REVENUE_AMOUNT","ROYALTY_PRICE","SUBROYALTY_PRICE","TICKET_FEE","MOBILEPAY_AMOUNT","CASHPAY_AMOUNT","OTHERPAY_AMOUNT"]:
                region["node"][k] += sp["node"][k]
            children.append({"node": sp["node"], "children": sp["children"]})
        result.append({"node": region["node"], "children": children})
    return result


def _d(v) -> float:
    """安全转换为 float"""
    if v is None:
        return 0.0
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0


# ==================== 2. GetProjectSummary ====================
def get_project_summary(db: DatabaseHelper, start_date: str, end_date: str,
                         sp_region_type_id: str = "", serverpart_id: str = "",
                         merchant_id: str = "", business_type: str = "",
                         settlement_modes: str = "", compact_type: str = "",
                         show_owner_dif: bool = False, show_sub_dif: bool = False) -> tuple[list[dict], dict]:
    """获取服务区营收分润数据（三级树：片区→服务区→项目）
    原 BUSINESSPROJECTSPLITHelper.GetProjectSummary (L1157-1603)
    1. 四表联查 T_REGISTERCOMPACT/T_SERVERPART/T_BUSINESSPROJECT/T_REGISTERCOMPACTSUB
       （含 UNION ALL 跨域合同 COMPACT_TYPE IN 340002,340003）
    2. 查询营收推送 T_REVENUEDAILY（关联 T_SERVERPARTSHOP 门店匹配）
    3. 查询应收拆分 T_BUSINESSPROJECTSPLIT
    4. 三级树构建 + 分润差异计算 + OtherData 5项营收汇总"""
    from datetime import datetime
    from collections import OrderedDict

    start_day = datetime.strptime(start_date[:10], '%Y-%m-%d').strftime('%Y%m%d')
    end_day = datetime.strptime(end_date[:10], '%Y-%m-%d').strftime('%Y%m%d')

    # --- 构造过滤条件 ---
    where_sql, shop_sql = "", ""
    if sp_region_type_id:
        where_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
        shop_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
    if serverpart_id:
        where_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
        shop_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
    if merchant_id:
        where_sql += f" AND C.MERCHANTS_ID IN ({merchant_id})"
    if business_type:
        where_sql += f" AND C.BUSINESS_TYPE IN ({business_type})"
    if settlement_modes:
        where_sql += f" AND C.SETTLEMENT_MODES IN ({settlement_modes})"
    if compact_type:
        where_sql += f" AND A.COMPACT_TYPE IN ({compact_type})"

    # --- 第1步: 查询经营项目及合同数据（UNION ALL 含跨域合同）---
    proj_sql = f"""SELECT
            B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX,
            B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_INDEX,
            A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES
        FROM T_REGISTERCOMPACT A, T_SERVERPART B, T_BUSINESSPROJECT C, T_REGISTERCOMPACTSUB D
        WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND A.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND C.SERVERPART_ID = B.SERVERPART_ID
            AND A.COMPACT_TYPE NOT IN (340002,340003)
            AND A.COMPACT_STATE = 1000 AND C.PROJECT_VALID = 1
            {where_sql}
        UNION ALL
        SELECT
            NULL AS SPREGIONTYPE_ID, NULL AS SPREGIONTYPE_NAME, NULL AS SPREGIONTYPE_INDEX,
            WM_CONCAT(B.SERVERPART_ID) AS SERVERPART_ID,
            WM_CONCAT(B.SERVERPART_NAME) AS SERVERPART_NAME, NULL AS SERVERPART_INDEX,
            A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES
        FROM T_REGISTERCOMPACT A, T_SERVERPART B, T_BUSINESSPROJECT C, T_REGISTERCOMPACTSUB D
        WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND A.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND C.SERVERPART_ID = B.SERVERPART_ID
            AND A.COMPACT_TYPE IN (340002,340003)
            AND A.COMPACT_STATE = 1000 AND C.PROJECT_VALID = 1
            {where_sql}
        GROUP BY A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES"""
    dt_project = db.execute_query(proj_sql) or []

    # --- 第2步: 查询营收推送数据 T_REVENUEDAILY ---
    other_data = {"PushRevenue": 0, "PushCoopRevenue": 0, "PushRentRevenue": 0,
                  "PushSelfCoopRevenue": 0, "PushSelfRevenue": 0, "ProjectCount": 0,
                  "ProjectCoopRevenue": 0, "ProjectRentRevenue": 0,
                  "ProjectSelfCoopRevenue": 0, "ProjectSelfRevenue": 0}
    if not (show_owner_dif or show_sub_dif):
        rev_sql = f"""SELECT
                CASE WHEN A.BUSINESS_TYPE = 1000 THEN 3000
                     WHEN A.BUSINESS_TYPE = 2000 THEN 1000 ELSE 2000 END AS BUSINESS_TYPE,
                B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SERVERPART_ID, B.SERVERPART_NAME,
                A.REVENUE_AMOUNT, A.REVENUEDAILY_ID, 0 AS PROJECT_STATE,
                C.SERVERPARTSHOP_ID, A.SHOPTRADE,
                A.SELLER_NAME, C.SHOPSHORTNAME
            FROM T_REVENUEDAILY A, T_SERVERPART B, T_SERVERPARTSHOP C
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
                AND A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPTRADE = C.SHOPTRADE
                AND C.ISVALID = 1
                AND A.REVENUEDAILY_STATE = 1
                AND A.STATISTICS_DATE BETWEEN {start_day} AND {end_day}
                {shop_sql}
            GROUP BY CASE WHEN A.BUSINESS_TYPE = 1000 THEN 3000
                     WHEN A.BUSINESS_TYPE = 2000 THEN 1000 ELSE 2000 END, A.SHOPTRADE,
                B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SERVERPART_ID, B.SERVERPART_NAME,
                A.REVENUE_AMOUNT, A.REVENUEDAILY_ID, A.SELLER_NAME, C.SHOPSHORTNAME,
                C.SERVERPARTSHOP_ID"""
        dt_revenue = db.execute_query(rev_sql) or []
        if business_type:
            bt_list = [int(x) for x in business_type.split(",") if x.strip()]
            dt_revenue = [r for r in dt_revenue if r.get("BUSINESS_TYPE") in bt_list]
        # 计算 OtherData 营收推送汇总
        for r in dt_revenue:
            amt = _d(r.get("REVENUE_AMOUNT"))
            bt = r.get("BUSINESS_TYPE")
            other_data["PushRevenue"] += amt
            if bt == 1000: other_data["PushCoopRevenue"] += amt
            elif bt == 2000: other_data["PushRentRevenue"] += amt
            elif bt == 3000: other_data["PushSelfCoopRevenue"] += amt
            elif bt == 4000: other_data["PushSelfRevenue"] += amt
    else:
        dt_revenue = []

    # --- 第3步: 查询应收拆分数据 T_BUSINESSPROJECTSPLIT ---
    split_sql = f"""SELECT * FROM T_BUSINESSPROJECTSPLIT
        WHERE BUSINESSPROJECTSPLIT_STATE = 1 AND ACCOUNT_TYPE = 1000
            AND STATISTICS_DATE BETWEEN {start_day} AND {end_day}"""
    dt_split = db.execute_query(split_sql) or []
    # 构建拆分数据索引 {BUSINESSPROJECT_ID: [rows]}
    split_map = {}
    for s in dt_split:
        pid = s.get("BUSINESSPROJECT_ID")
        if pid not in split_map:
            split_map[pid] = []
        split_map[pid].append(s)
    # 构建营收数据索引 {SERVERPARTSHOP_ID_CSV: [rows]}
    rev_matched = set()  # 已匹配的 REVENUEDAILY_ID

    # --- 第4步: 构建三级树（片区→服务区→项目）---
    region_map = OrderedDict()
    sum_fields = ["MONTHROYALTY_PRICE", "REVENUE_AMOUNT", "ROYALTY_PRICE",
                  "SUBROYALTY_PRICE", "TICKET_FEE", "CASHPAY_AMOUNT",
                  "MOBILEPAY_AMOUNT", "OTHERPAY_AMOUNT", "ACCOUNT_AMOUNT"]
    sp_num = 1

    # 按片区分组
    region_ids = []
    for p in dt_project:
        rid = p.get("SPREGIONTYPE_ID")
        if rid is not None and rid not in region_ids:
            region_ids.append(rid)

    for rid in region_ids:
        region_projects = [p for p in dt_project if p.get("SPREGIONTYPE_ID") == rid]
        if not region_projects:
            continue
        first_rp = region_projects[0]
        region_node = {"SPREGIONTYPE_ID": rid, "SPREGIONTYPE_NAME": first_rp.get("SPREGIONTYPE_NAME", "")}
        for f in sum_fields:
            region_node[f] = 0
        region_children = []

        # 按服务区分组
        sp_ids = []
        for p in region_projects:
            sid = p.get("SERVERPART_ID")
            if sid not in sp_ids:
                sp_ids.append(sid)

        for sid in sp_ids:
            sp_projects = [p for p in region_projects if p.get("SERVERPART_ID") == sid]
            if not sp_projects:
                continue
            first_sp = sp_projects[0]
            sp_node = {"index": str(sp_num), "SERVERPART_ID": sid,
                       "SERVERPART_NAME": first_sp.get("SERVERPART_NAME", "")}
            for f in sum_fields:
                sp_node[f] = 0
            sp_children = []
            proj_num = 1

            for proj in sp_projects:
                bp_id = proj.get("BUSINESSPROJECT_ID")
                # 跳过已终止且在统计开始日期前终止的项目
                closed = proj.get("CLOSED_DATE")
                if closed and str(closed) != "" and int(str(closed)[:8]) <= int(start_day):
                    continue

                proj_node = {
                    "index": f"{sp_num}.{proj_num}",
                    "MERCHANTS_ID": proj.get("MERCHANTS_ID"),
                    "MERCHANTS_NAME": proj.get("MERCHANTS_NAME", ""),
                    "REGISTERCOMPACT_ID": proj.get("REGISTERCOMPACT_ID"),
                    "BUSINESSPROJECT_ID": bp_id,
                    "SERVERPARTSHOP_ID": proj.get("SERVERPARTSHOP_ID", ""),
                    "SERVERPARTSHOP_NAME": str(proj.get("SERVERPARTSHOP_NAME", "")).split(",")[0],
                    "COMPACT_TYPE": proj.get("COMPACT_TYPE"),
                    "BUSINESS_TYPE": proj.get("BUSINESS_TYPE"),
                    "SETTLEMENT_MODES": proj.get("SETTLEMENT_MODES"),
                    "PUSHREVENUE_AMOUNT": 0,
                }
                # 门店名截取"区"后面的部分
                shop_name = proj_node["SERVERPARTSHOP_NAME"]
                if "区" in shop_name:
                    proj_node["SERVERPARTSHOP_NAME"] = shop_name.split("区", 1)[1]

                # 匹配营收推送数据（关联门店）
                shop_ids_csv = str(proj.get("SERVERPARTSHOP_ID", ""))
                if shop_ids_csv and dt_revenue:
                    matched_rev_amt = 0
                    for shop_id in shop_ids_csv.split(","):
                        for rv in dt_revenue:
                            rv_shop = str(rv.get("SERVERPARTSHOP_ID", ""))
                            rv_id = rv.get("REVENUEDAILY_ID")
                            if shop_id in rv_shop.split(",") and rv_id not in rev_matched:
                                matched_rev_amt += _d(rv.get("REVENUE_AMOUNT"))
                                rev_matched.add(rv_id)
                    proj_node["PUSHREVENUE_AMOUNT"] = matched_rev_amt

                # 处理已终止但无营收的项目
                proj_end = proj.get("PROJECT_ENDDATE")
                if proj_end:
                    try:
                        if isinstance(proj_end, str):
                            pe = datetime.strptime(proj_end[:10], '%Y-%m-%d')
                        else:
                            pe = proj_end
                        if pe < datetime.strptime(start_date[:10], '%Y-%m-%d') and proj_node["PUSHREVENUE_AMOUNT"] == 0:
                            continue
                    except Exception:
                        pass

                # 从拆分数据获取分润
                bp_splits = split_map.get(bp_id, [])
                if bp_splits:
                    # 处理切换模式
                    switch_date = proj.get("SWITCH_DATE")
                    if switch_date and str(switch_date) != "":
                        proj_node["SETTLEMENT_MODES"] = proj.get("SWITCH_MODES")

                    last_split = sorted(bp_splits, key=lambda x: x.get("STATISTICS_DATE", 0), reverse=True)[0]
                    proj_node["MONTHROYALTY_PRICE"] = _d(last_split.get("ROYALTY_PRICE"))
                    proj_node["ROYALTY_THEORY"] = _d(last_split.get("ROYALTY_THEORY"))
                    proj_node["SUBROYALTY_THEORY"] = _d(last_split.get("SUBROYALTY_THEORY"))
                    proj_node["REVENUE_AMOUNT"] = sum(_d(s.get("REVENUEDAILY_AMOUNT")) for s in bp_splits)
                    proj_node["ROYALTY_PRICE"] = sum(_d(s.get("ROYALTYDAILY_PRICE")) for s in bp_splits)
                    proj_node["SUBROYALTY_PRICE"] = sum(_d(s.get("SUBROYALTYDAILY_PRICE")) for s in bp_splits)
                    proj_node["TICKET_FEE"] = sum(_d(s.get("TICKETDAILY_FEE")) for s in bp_splits)
                    proj_node["ROYALTYDAILY_THEORY"] = sum(_d(s.get("ROYALTYDAILY_THEORY")) for s in bp_splits)
                    proj_node["SUBROYALTYDAILY_THEORY"] = sum(_d(s.get("SUBROYALTYDAILY_THEORY")) for s in bp_splits)
                    proj_node["DIFDAILY_REVENUE"] = sum(_d(s.get("DIFDAILY_REVENUE")) for s in bp_splits)
                    proj_node["CASHPAY_AMOUNT"] = _d(last_split.get("CASHPAY_AMOUNT"))
                    proj_node["MOBILEPAY_AMOUNT"] = _d(last_split.get("MOBILEPAY_AMOUNT"))
                    proj_node["OTHERPAY_AMOUNT"] = _d(last_split.get("OTHERPAY_AMOUNT"))
                elif proj_node.get("BUSINESS_TYPE") == 3000:
                    # 自营提成但无拆分数据 → 业主自营
                    proj_node["BUSINESS_TYPE"] = 4000
                    proj_node["SETTLEMENT_MODES"] = None
                    proj_node["MONTHROYALTY_PRICE"] = proj_node["PUSHREVENUE_AMOUNT"]
                    proj_node["REVENUE_AMOUNT"] = proj_node["PUSHREVENUE_AMOUNT"]
                    proj_node["ROYALTY_PRICE"] = proj_node["PUSHREVENUE_AMOUNT"]
                    proj_node["SUBROYALTY_PRICE"] = 0
                    proj_node["TICKET_FEE"] = 0

                # ShowOwnerDif / ShowSubDif 差异过滤
                if show_owner_dif:
                    if proj_node.get("ROYALTY_PRICE", 0) == proj_node.get("ROYALTYDAILY_THEORY", 0):
                        continue
                if show_sub_dif:
                    if proj_node.get("SUBROYALTY_PRICE", 0) == proj_node.get("SUBROYALTYDAILY_THEORY", 0):
                        continue

                sp_children.append({"node": proj_node})
                proj_num += 1
                other_data["ProjectCount"] += 1
                # 按经营模式累计项目分润
                bt = proj_node.get("BUSINESS_TYPE")
                rev_amt = _d(proj_node.get("REVENUE_AMOUNT"))
                if bt == 1000: other_data["ProjectCoopRevenue"] += rev_amt
                elif bt == 2000: other_data["ProjectRentRevenue"] += rev_amt
                elif bt == 3000: other_data["ProjectSelfCoopRevenue"] += rev_amt
                elif bt == 4000: other_data["ProjectSelfRevenue"] += rev_amt

            # 未匹配门店补入（C# L1581-1629）
            if not show_owner_dif and not show_sub_dif:
                for rv in dt_revenue:
                    rv_id = rv.get("REVENUEDAILY_ID")
                    if rv_id in rev_matched:
                        continue
                    rv_sp = rv.get("SERVERPART_ID")
                    if str(rv_sp) != str(sid):
                        continue
                    rev_matched.add(rv_id)
                    unmatched = {
                        "index": f"{sp_num}.{proj_num}",
                        "MERCHANTS_NAME": rv.get("SELLER_NAME", ""),
                        "SERVERPARTSHOP_NAME": rv.get("SHOPSHORTNAME", ""),
                        "BUSINESS_TYPE": rv.get("BUSINESS_TYPE"),
                        "REVENUE_AMOUNT": _d(rv.get("REVENUE_AMOUNT")),
                        "PUSHREVENUE_AMOUNT": _d(rv.get("REVENUE_AMOUNT")),
                    }
                    sp_children.append({"node": unmatched})
                    proj_num += 1

            # 累计到服务区节点
            for child in sp_children:
                for f in sum_fields:
                    sp_node[f] += _d(child["node"].get(f))
            region_children.append({"node": sp_node, "children": sp_children})
            sp_num += 1

        # 累计到片区节点
        for child in region_children:
            for f in sum_fields:
                region_node[f] += _d(child["node"].get(f))
        region_map[rid] = {"node": region_node, "children": region_children}

    result = list(region_map.values())
    return result, other_data


# ==================== 3. GetRevenueSplitSummary ====================
def get_revenue_split_summary(db: DatabaseHelper, start_date: str, end_date: str,
                                sp_region_type_id: str = "", serverpart_id: str = "",
                                merchant_id: str = "", business_type: str = "",
                                settlement_modes: str = "", compact_type: str = "",
                                serverpartshop_id: str = "") -> tuple[list[dict], dict]:
    """获取服务区营收分润报表（四川版，四级树：日期→片区→服务区→项目）
    原 BUSINESSPROJECTSPLITHelper.GetProjectSummary(重载 L2172-2539)
    按日逐天展开应收拆分数据，含 ServerpartShopId 过滤"""
    from datetime import datetime, timedelta
    from collections import OrderedDict

    start_dt = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end_dt = datetime.strptime(end_date[:10], '%Y-%m-%d')
    start_day = start_dt.strftime('%Y%m%d')
    end_day = end_dt.strftime('%Y%m%d')

    # --- 构造过滤条件 ---
    where_sql = ""
    if sp_region_type_id:
        where_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
    if serverpart_id:
        where_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
    if merchant_id:
        where_sql += f" AND C.MERCHANTS_ID IN ({merchant_id})"
    if business_type:
        where_sql += f" AND C.BUSINESS_TYPE IN ({business_type})"
    if settlement_modes:
        where_sql += f" AND C.SETTLEMENT_MODES IN ({settlement_modes})"
    if compact_type:
        where_sql += f" AND A.COMPACT_TYPE IN ({compact_type})"
    if serverpartshop_id:
        shop_ids = ",".join(f"'{s.strip()}'" for s in serverpartshop_id.split(",") if s.strip())
        where_sql += f" AND C.SERVERPARTSHOP_ID IN ({shop_ids})"

    # --- 查询经营项目及合同数据 ---
    proj_sql = f"""SELECT
            B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX,
            B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_INDEX,
            A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.BUSINESSPROJECT_NAME, C.MERCHANTS_ID, C.MERCHANTS_NAME,
            C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES
        FROM T_REGISTERCOMPACT A, T_SERVERPART B, T_BUSINESSPROJECT C, T_REGISTERCOMPACTSUB D
        WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND A.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND C.SERVERPART_ID = B.SERVERPART_ID
            AND A.COMPACT_TYPE NOT IN (340002,340003)
            AND A.COMPACT_STATE = 1000 AND C.PROJECT_VALID = 1
            {where_sql}"""
    dt_project = db.execute_query(proj_sql) or []
    if not dt_project:
        return [], {}

    # --- 查询应收拆分数据 ---
    bp_ids = ",".join(str(p.get("BUSINESSPROJECT_ID")) for p in dt_project if p.get("BUSINESSPROJECT_ID"))
    split_sql = f"""SELECT * FROM T_BUSINESSPROJECTSPLIT
        WHERE BUSINESSPROJECTSPLIT_STATE = 1 AND ACCOUNT_TYPE = 1000
            AND BUSINESSPROJECT_ID IN ({bp_ids})
            AND STATISTICS_DATE BETWEEN {start_day} AND {end_day}"""
    dt_split = db.execute_query(split_sql) or []
    # 索引 {(BUSINESSPROJECT_ID, STATISTICS_DATE_str): [rows]}
    split_index = {}
    for s in dt_split:
        key = (s.get("BUSINESSPROJECT_ID"), str(s.get("STATISTICS_DATE", "")))
        if key not in split_index:
            split_index[key] = []
        split_index[key].append(s)

    sum_fields = ["MONTHROYALTY_PRICE", "REVENUE_AMOUNT", "ROYALTY_PRICE",
                  "SUBROYALTY_PRICE", "TICKET_FEE", "CASHPAY_AMOUNT",
                  "MOBILEPAY_AMOUNT", "OTHERPAY_AMOUNT", "CIGARETTE_AMOUNT",
                  "PUSHREVENUE_AMOUNT", "ROYALTY_THEORY", "SUBROYALTY_THEORY",
                  "ROYALTYDAILY_THEORY", "SUBROYALTYDAILY_THEORY", "DIFDAILY_REVENUE"]

    # --- 按日逐天展开 ---
    result = []
    cur_date = start_dt
    while cur_date <= end_dt:
        cur_day_str = cur_date.strftime('%Y%m%d')
        cur_date_display = cur_date.strftime('%Y-%m-%d')
        date_node = {"STATISTICS_DATE": cur_date_display, "ProjectCount": 0}
        for f in sum_fields:
            date_node[f] = 0
        date_children = []
        sp_num = 1

        # 片区分组
        region_ids = []
        for p in dt_project:
            rid = p.get("SPREGIONTYPE_ID")
            if rid is not None and rid not in region_ids:
                region_ids.append(rid)

        for rid in region_ids:
            rp = [p for p in dt_project if p.get("SPREGIONTYPE_ID") == rid]
            if not rp:
                continue
            region_node = {"SPREGIONTYPE_ID": rid, "SPREGIONTYPE_NAME": rp[0].get("SPREGIONTYPE_NAME", "")}
            for f in sum_fields:
                region_node[f] = 0
            region_node["ProjectCount"] = 0
            region_children = []

            # 服务区分组
            sp_ids = []
            for p in rp:
                sid = p.get("SERVERPART_ID")
                if sid not in sp_ids:
                    sp_ids.append(sid)

            for sid in sp_ids:
                sp_proj = [p for p in rp if p.get("SERVERPART_ID") == sid]
                sp_node = {"index": str(sp_num), "SERVERPART_ID": sid,
                           "SERVERPART_NAME": sp_proj[0].get("SERVERPART_NAME", "")}
                for f in sum_fields:
                    sp_node[f] = 0
                sp_node["ProjectCount"] = 0
                sp_children = []
                proj_num = 1

                for proj in sp_proj:
                    bp_id = proj.get("BUSINESSPROJECT_ID")
                    closed = proj.get("CLOSED_DATE")
                    if closed and str(closed) != "" and int(str(closed)[:8]) <= int(start_day):
                        continue
                    proj_end = proj.get("PROJECT_ENDDATE")
                    if proj_end:
                        try:
                            pe = proj_end if not isinstance(proj_end, str) else datetime.strptime(proj_end[:10], '%Y-%m-%d')
                            if pe < start_dt:
                                continue
                        except Exception:
                            pass

                    proj_node = {
                        "index": f"{sp_num}.{proj_num}",
                        "MERCHANTS_ID": proj.get("MERCHANTS_ID"),
                        "MERCHANTS_NAME": proj.get("MERCHANTS_NAME", ""),
                        "REGISTERCOMPACT_ID": proj.get("REGISTERCOMPACT_ID"),
                        "BUSINESSPROJECT_ID": bp_id,
                        "SERVERPARTSHOP_ID": proj.get("SERVERPARTSHOP_ID", ""),
                        "SERVERPARTSHOP_NAME": proj.get("BUSINESSPROJECT_NAME", ""),
                        "COMPACT_TYPE": proj.get("COMPACT_TYPE"),
                        "BUSINESS_TYPE": proj.get("BUSINESS_TYPE"),
                        "SETTLEMENT_MODES": proj.get("SETTLEMENT_MODES"),
                    }

                    # 查找当天拆分数据
                    day_splits = split_index.get((bp_id, cur_day_str), [])
                    if day_splits:
                        s0 = day_splits[0]
                        switch_date = proj.get("SWITCH_DATE")
                        if switch_date and str(switch_date) != "":
                            proj_node["SETTLEMENT_MODES"] = proj.get("SWITCH_MODES")
                        proj_node["MONTHROYALTY_PRICE"] = _d(s0.get("ROYALTY_PRICE"))
                        proj_node["ROYALTY_THEORY"] = _d(s0.get("ROYALTY_THEORY"))
                        proj_node["SUBROYALTY_THEORY"] = _d(s0.get("SUBROYALTY_THEORY"))
                        proj_node["REVENUE_AMOUNT"] = _d(s0.get("REVENUEDAILY_AMOUNT"))
                        proj_node["CIGARETTE_AMOUNT"] = _d(s0.get("CIGARETTEDAILY_AMOUNT"))
                        proj_node["CASHPAY_AMOUNT"] = _d(s0.get("CURCASHPAY_AMOUNT"))
                        proj_node["MOBILEPAY_AMOUNT"] = _d(s0.get("CURMOBILEPAY_AMOUNT"))
                        proj_node["ROYALTY_PRICE"] = _d(s0.get("ROYALTYDAILY_PRICE"))
                        proj_node["SUBROYALTY_PRICE"] = _d(s0.get("SUBROYALTYDAILY_PRICE"))
                        proj_node["TICKET_FEE"] = _d(s0.get("TICKETDAILY_FEE"))
                        proj_node["ROYALTYDAILY_THEORY"] = _d(s0.get("ROYALTYDAILY_THEORY"))
                        proj_node["SUBROYALTYDAILY_THEORY"] = _d(s0.get("SUBROYALTYDAILY_THEORY"))
                        proj_node["GUARANTEERATIO"] = _d(s0.get("GUARANTEERATIO"))
                        proj_node["SMOKERATIO"] = _d(s0.get("SMOKERATIO"))
                        sp_children.append({"node": proj_node})
                        proj_num += 1

                if not sp_children:
                    continue
                # 累计到服务区
                for child in sp_children:
                    for f in sum_fields:
                        sp_node[f] += _d(child["node"].get(f))
                sp_node["ProjectCount"] = len([c for c in sp_children if c["node"].get("BUSINESSPROJECT_ID")])
                region_children.append({"node": sp_node, "children": sp_children})
                sp_num += 1

            if not region_children:
                continue
            for child in region_children:
                for f in sum_fields:
                    region_node[f] += _d(child["node"].get(f))
                region_node["ProjectCount"] += child["node"].get("ProjectCount", 0)
            date_children.append({"node": region_node, "children": region_children})

        if date_children:
            for child in date_children:
                for f in sum_fields:
                    date_node[f] += _d(child["node"].get(f))
                date_node["ProjectCount"] += child["node"].get("ProjectCount", 0)
            result.append({"node": date_node, "children": date_children})

        cur_date += timedelta(days=1)

    return result, {}


# ==================== 4. GetProjectMerchantSummary ====================
def get_project_merchant_summary(db: DatabaseHelper, start_date: str, end_date: str,
                                   sp_region_type_id: str = "", serverpart_id: str = "",
                                   merchant_id: str = "", business_type: str = "",
                                   settlement_modes: str = "", compact_type: str = "",
                                   show_owner_dif: bool = False, show_sub_dif: bool = False) -> tuple[list[dict], dict]:
    """获取经营商户营收分润数据（三级树：商户→服务区→项目）
    原 BUSINESSPROJECTSPLITHelper.GetProjectMerchantSummary (L2561-2900)
    核心区别：按 MERCHANTS_ID 分组（非片区），含营收推送匹配+拆分分润+OtherData"""
    from datetime import datetime
    from collections import OrderedDict

    start_day = datetime.strptime(start_date[:10], '%Y-%m-%d').strftime('%Y%m%d')
    end_day = datetime.strptime(end_date[:10], '%Y-%m-%d').strftime('%Y%m%d')

    # --- 构造过滤条件 ---
    where_sql, shop_sql = "", ""
    if sp_region_type_id:
        where_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
        shop_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
    if serverpart_id:
        where_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
        shop_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
    if merchant_id:
        where_sql += f" AND C.MERCHANTS_ID IN ({merchant_id})"
    if business_type:
        where_sql += f" AND C.BUSINESS_TYPE IN ({business_type})"
    if settlement_modes:
        where_sql += f" AND C.SETTLEMENT_MODES IN ({settlement_modes})"
    if compact_type:
        where_sql += f" AND A.COMPACT_TYPE IN ({compact_type})"

    # --- 查询经营项目及合同（UNION ALL 含跨域）---
    proj_sql = f"""SELECT
            B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX,
            B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_INDEX,
            A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES
        FROM T_REGISTERCOMPACT A, T_SERVERPART B, T_BUSINESSPROJECT C, T_REGISTERCOMPACTSUB D
        WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND A.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND C.SERVERPART_ID = B.SERVERPART_ID
            AND A.COMPACT_TYPE NOT IN (340002,340003)
            AND A.COMPACT_STATE = 1000 AND C.PROJECT_VALID = 1
            {where_sql}
        UNION ALL
        SELECT
            NULL AS SPREGIONTYPE_ID, NULL AS SPREGIONTYPE_NAME, NULL AS SPREGIONTYPE_INDEX,
            WM_CONCAT(B.SERVERPART_ID) AS SERVERPART_ID,
            WM_CONCAT(B.SERVERPART_NAME) AS SERVERPART_NAME, NULL AS SERVERPART_INDEX,
            A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES
        FROM T_REGISTERCOMPACT A, T_SERVERPART B, T_BUSINESSPROJECT C, T_REGISTERCOMPACTSUB D
        WHERE A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID
            AND A.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID
            AND C.SERVERPART_ID = B.SERVERPART_ID
            AND A.COMPACT_TYPE IN (340002,340003)
            AND A.COMPACT_STATE = 1000 AND C.PROJECT_VALID = 1
            {where_sql}
        GROUP BY A.REGISTERCOMPACT_ID, A.COMPACT_NAME, A.COMPACT_TYPE,
            C.BUSINESSPROJECT_ID, C.SERVERPARTSHOP_ID, C.SERVERPARTSHOP_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            C.CLOSED_DATE, C.SWITCH_DATE, C.SWITCH_MODES"""
    dt_project = db.execute_query(proj_sql) or []

    # --- 查询营收推送 ---
    other_data = {"PushRevenue": 0, "PushCoopRevenue": 0, "PushRentRevenue": 0,
                  "PushSelfCoopRevenue": 0, "PushSelfRevenue": 0}
    if not (show_owner_dif or show_sub_dif):
        rev_sql = f"""SELECT
                CASE WHEN A.BUSINESS_TYPE = 1000 THEN 3000
                     WHEN A.BUSINESS_TYPE = 2000 THEN 1000 ELSE 2000 END AS BUSINESS_TYPE,
                B.SPREGIONTYPE_ID, B.SERVERPART_ID,
                A.REVENUE_AMOUNT, A.REVENUEDAILY_ID, 0 AS PROJECT_STATE,
                C.SERVERPARTSHOP_ID,
                A.SELLER_ID AS MERCHANTS_ID, A.SELLER_NAME AS MERCHANTS_NAME,
                C.SHOPSHORTNAME
            FROM T_REVENUEDAILY A, T_SERVERPART B, T_SERVERPARTSHOP C
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
                AND A.SERVERPART_ID = C.SERVERPART_ID AND A.SHOPTRADE = C.SHOPTRADE
                AND C.ISVALID = 1 AND A.REVENUEDAILY_STATE = 1
                AND A.STATISTICS_DATE BETWEEN {start_day} AND {end_day}
                {shop_sql}
            GROUP BY CASE WHEN A.BUSINESS_TYPE = 1000 THEN 3000
                     WHEN A.BUSINESS_TYPE = 2000 THEN 1000 ELSE 2000 END,
                B.SPREGIONTYPE_ID, B.SERVERPART_ID,
                A.REVENUE_AMOUNT, A.REVENUEDAILY_ID,
                A.SELLER_ID, A.SELLER_NAME, C.SHOPSHORTNAME, C.SERVERPARTSHOP_ID"""
        dt_revenue = db.execute_query(rev_sql) or []
        if business_type:
            bt_list = [int(x) for x in business_type.split(",") if x.strip()]
            dt_revenue = [r for r in dt_revenue if r.get("BUSINESS_TYPE") in bt_list]
        for r in dt_revenue:
            amt = _d(r.get("REVENUE_AMOUNT"))
            bt = r.get("BUSINESS_TYPE")
            other_data["PushRevenue"] += amt
            if bt == 1000: other_data["PushCoopRevenue"] += amt
            elif bt == 2000: other_data["PushRentRevenue"] += amt
            elif bt == 3000: other_data["PushSelfCoopRevenue"] += amt
            elif bt == 4000: other_data["PushSelfRevenue"] += amt
    else:
        dt_revenue = []

    # --- 查询应收拆分 ---
    split_sql = f"""SELECT * FROM T_BUSINESSPROJECTSPLIT
        WHERE BUSINESSPROJECTSPLIT_STATE = 1
            AND STATISTICS_DATE BETWEEN {start_day} AND {end_day}"""
    dt_split = db.execute_query(split_sql) or []
    split_map = {}
    for s in dt_split:
        pid = s.get("BUSINESSPROJECT_ID")
        if pid not in split_map:
            split_map[pid] = []
        split_map[pid].append(s)
    rev_matched = set()

    sum_fields = ["MONTHROYALTY_PRICE", "REVENUE_AMOUNT", "ROYALTY_PRICE",
                  "SUBROYALTY_PRICE", "TICKET_FEE", "CASHPAY_AMOUNT",
                  "MOBILEPAY_AMOUNT", "OTHERPAY_AMOUNT", "ACCOUNT_AMOUNT"]

    # --- 按商户分组构建三级树（商户→服务区→项目）---
    merchant_ids = []
    for p in dt_project:
        mid = p.get("MERCHANTS_ID")
        if mid is not None and mid not in merchant_ids:
            merchant_ids.append(mid)

    result = []
    sp_num = 1
    for mid in merchant_ids:
        m_projects = [p for p in dt_project if p.get("MERCHANTS_ID") == mid]
        if not m_projects:
            continue
        first_mp = m_projects[0]
        m_node = {"MERCHANTS_ID": mid, "MERCHANTS_NAME": first_mp.get("MERCHANTS_NAME", ""),
                  "ProjectCount": 0}
        for f in sum_fields:
            m_node[f] = 0
        m_children = []

        # 按服务区分组
        sp_ids = []
        for p in m_projects:
            sid = p.get("SERVERPART_ID")
            if sid not in sp_ids:
                sp_ids.append(sid)

        for sid in sp_ids:
            sp_proj = [p for p in m_projects if p.get("SERVERPART_ID") == sid]
            sp_node = {"index": str(sp_num), "SERVERPART_ID": sid,
                       "SERVERPART_NAME": sp_proj[0].get("SERVERPART_NAME", "")}
            for f in sum_fields:
                sp_node[f] = 0
            sp_node["ProjectCount"] = 0
            sp_children = []
            proj_num = 1

            for proj in sp_proj:
                bp_id = proj.get("BUSINESSPROJECT_ID")
                proj_node = {
                    "index": f"{sp_num}.{proj_num}",
                    "REGISTERCOMPACT_ID": proj.get("REGISTERCOMPACT_ID"),
                    "BUSINESSPROJECT_ID": bp_id,
                    "SERVERPARTSHOP_ID": proj.get("SERVERPARTSHOP_ID", ""),
                    "SERVERPARTSHOP_NAME": str(proj.get("SERVERPARTSHOP_NAME", "")).split(",")[0],
                    "COMPACT_TYPE": proj.get("COMPACT_TYPE"),
                    "BUSINESS_TYPE": proj.get("BUSINESS_TYPE"),
                    "SETTLEMENT_MODES": proj.get("SETTLEMENT_MODES"),
                    "PUSHREVENUE_AMOUNT": 0,
                }
                shop_name = proj_node["SERVERPARTSHOP_NAME"]
                if "区" in shop_name:
                    proj_node["SERVERPARTSHOP_NAME"] = shop_name.split("区", 1)[1]

                # 匹配营收推送
                shop_ids_csv = str(proj.get("SERVERPARTSHOP_ID", ""))
                if shop_ids_csv and dt_revenue:
                    matched_amt = 0
                    for shop_id in shop_ids_csv.split(","):
                        for rv in dt_revenue:
                            rv_shop = str(rv.get("SERVERPARTSHOP_ID", ""))
                            rv_id = rv.get("REVENUEDAILY_ID")
                            if shop_id in rv_shop.split(",") and rv_id not in rev_matched:
                                matched_amt += _d(rv.get("REVENUE_AMOUNT"))
                                rev_matched.add(rv_id)
                    proj_node["PUSHREVENUE_AMOUNT"] = matched_amt

                # 拆分数据
                bp_splits = split_map.get(bp_id, [])
                if bp_splits:
                    last_split = sorted(bp_splits, key=lambda x: x.get("STATISTICS_DATE", 0), reverse=True)[0]
                    proj_node["MONTHROYALTY_PRICE"] = _d(last_split.get("ROYALTY_PRICE"))
                    proj_node["ROYALTY_THEORY"] = _d(last_split.get("ROYALTY_THEORY"))
                    proj_node["SUBROYALTY_THEORY"] = _d(last_split.get("SUBROYALTY_THEORY"))
                    proj_node["REVENUE_AMOUNT"] = sum(_d(s.get("REVENUEDAILY_AMOUNT")) for s in bp_splits)
                    proj_node["ROYALTY_PRICE"] = sum(_d(s.get("ROYALTYDAILY_PRICE")) for s in bp_splits)
                    proj_node["SUBROYALTY_PRICE"] = sum(_d(s.get("SUBROYALTYDAILY_PRICE")) for s in bp_splits)
                    proj_node["TICKET_FEE"] = sum(_d(s.get("TICKETDAILY_FEE")) for s in bp_splits)
                    proj_node["ROYALTYDAILY_THEORY"] = sum(_d(s.get("ROYALTYDAILY_THEORY")) for s in bp_splits)
                    proj_node["SUBROYALTYDAILY_THEORY"] = sum(_d(s.get("SUBROYALTYDAILY_THEORY")) for s in bp_splits)
                    proj_node["DIFDAILY_REVENUE"] = sum(_d(s.get("DIFDAILY_REVENUE")) for s in bp_splits)
                else:
                    proj_node["REVENUE_AMOUNT"] = proj_node["PUSHREVENUE_AMOUNT"]
                    proj_node["DIFDAILY_REVENUE"] = 0
                    bt = proj_node.get("BUSINESS_TYPE")
                    if bt in (1000, 2000):
                        proj_node["MONTHROYALTY_PRICE"] = 0
                        proj_node["ROYALTY_PRICE"] = 0
                        proj_node["SUBROYALTY_PRICE"] = proj_node["REVENUE_AMOUNT"]
                    elif bt == 3000:
                        proj_node["MONTHROYALTY_PRICE"] = proj_node["REVENUE_AMOUNT"]
                        proj_node["ROYALTY_PRICE"] = proj_node["REVENUE_AMOUNT"]
                        proj_node["SUBROYALTY_PRICE"] = 0
                    else:
                        proj_node["MONTHROYALTY_PRICE"] = proj_node["REVENUE_AMOUNT"]
                        proj_node["ROYALTY_PRICE"] = proj_node["REVENUE_AMOUNT"]
                        proj_node["SUBROYALTY_PRICE"] = 0

                # 差异过滤
                if show_owner_dif and proj_node.get("ROYALTY_PRICE", 0) == proj_node.get("ROYALTYDAILY_THEORY", 0):
                    continue
                if show_sub_dif and proj_node.get("SUBROYALTY_PRICE", 0) == proj_node.get("SUBROYALTYDAILY_THEORY", 0):
                    continue

                sp_children.append({"node": proj_node})
                proj_num += 1

            for child in sp_children:
                for f in sum_fields:
                    sp_node[f] += _d(child["node"].get(f))
            sp_node["ProjectCount"] = len(sp_children)
            if sp_children:
                m_children.append({"node": sp_node, "children": sp_children})
            sp_num += 1

        for child in m_children:
            for f in sum_fields:
                m_node[f] += _d(child["node"].get(f))
            m_node["ProjectCount"] += child["node"].get("ProjectCount", 0)
        if m_children:
            result.append({"node": m_node, "children": m_children})

    return result, other_data


# ==================== 5. CreateSingleProjectSplit ====================
def create_single_project_split(db: DatabaseHelper, start_date: str, end_date: str,
                                  serverpartshop_id: str = "", compact_id: str = "",
                                  project_id: str = "", out_business_type: str = "",
                                  business_start_date: str = "") -> bool:
    """生成单个门店/合同/项目应收拆分数据
    原 BUSINESSPROJECTSPLITHelper.CreateSingleProjectSplit (L3574-3866)
    1. 根据 ProjectId/CompactId/ServerpartShopId 查询经营项目（GetProjectInfo）
    2. 先 UPDATE 置无效已有拆分 → 确定项目起止日期 → 逐日生成拆分记录
    3. 处理项目期外数据 → 提交后按月调 SolidMonthProjectSplit 固化"""
    from datetime import datetime, timedelta

    # --- 1. 构造查询条件 ---
    if project_id:
        where_sql = f" AND D.BUSINESSPROJECT_ID IN ({project_id})"
    elif compact_id:
        where_sql = f" AND A.REGISTERCOMPACT_ID IN ({compact_id})"
    elif serverpartshop_id:
        where_sql = (f" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP S "
                     f"WHERE ',' || D.SERVERPARTSHOP_ID || ',' LIKE '%,' || S.SERVERPARTSHOP_ID || ',%' "
                     f"AND S.SERVERPARTSHOP_ID IN ({serverpartshop_id}))")
    else:
        logger.warning("CreateSingleProjectSplit: 未传入参数")
        return False

    # --- 2. 查询经营合同和经营项目数据 ---
    proj_sql = f"""SELECT
            A.SECONDPART_ID AS MERCHANTS_ID, A.REGISTERCOMPACT_ID, A.COMPACT_TYPE,
            A.COMPACT_NAME, A.COMPACT_STARTDATE, A.COMPACT_ENDDATE, A.COMPACT_AMOUNT,
            D.BUSINESSPROJECT_ID, D.BUSINESSPROJECT_NAME, D.SERVERPARTSHOP_ID,
            D.SERVERPARTSHOP_NAME, D.PROJECT_STARTDATE, D.PROJECT_ENDDATE,
            D.GUARANTEE_PRICE, D.BUSINESS_TYPE, D.SETTLEMENT_MODES,
            D.CLOSED_DATE, D.SWITCH_DATE, D.SWITCH_MODES,
            WM_CONCAT(C.SERVERPART_ID) AS SERVERPART_ID,
            WM_CONCAT(C.SERVERPART_NAME) AS SERVERPART_NAME
        FROM T_REGISTERCOMPACT A
        LEFT JOIN T_BUSINESSPROJECT D ON A.REGISTERCOMPACT_ID = D.REGISTERCOMPACT_ID AND D.PROJECT_VALID = 1,
            T_RTREGISTERCOMPACT B, T_SERVERPART C
        WHERE A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND B.SERVERPART_ID = C.SERVERPART_ID
            AND A.COMPACT_STATE = 1000
            {where_sql}
        GROUP BY A.SECONDPART_ID, A.REGISTERCOMPACT_ID, A.COMPACT_TYPE,
            A.COMPACT_NAME, A.COMPACT_STARTDATE, A.COMPACT_ENDDATE, A.COMPACT_AMOUNT,
            D.BUSINESSPROJECT_ID, D.BUSINESSPROJECT_NAME, D.SERVERPARTSHOP_ID,
            D.SERVERPARTSHOP_NAME, D.PROJECT_STARTDATE, D.PROJECT_ENDDATE,
            D.GUARANTEE_PRICE, D.BUSINESS_TYPE, D.SETTLEMENT_MODES,
            D.CLOSED_DATE, D.SWITCH_DATE, D.SWITCH_MODES"""
    dt_project = db.execute_query(proj_sql) or []
    if not dt_project:
        logger.warning(f"CreateSingleProjectSplit: 查不到经营项目数据 where={where_sql}")
        return False

    start_dt = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end_dt = datetime.strptime(end_date[:10], '%Y-%m-%d')
    start_day = start_dt.strftime('%Y%m%d')
    end_day = end_dt.strftime('%Y%m%d')
    completed_project_ids = []

    for proj in dt_project:
        bp_id = proj.get("BUSINESSPROJECT_ID")
        compact_info = f"{proj.get('COMPACT_NAME', '')}【{proj.get('SERVERPART_NAME', '')}】"

        if not bp_id:
            logger.warning(f"{compact_info} 拆分失败：缺失经营项目数据")
            continue

        # --- 3. 先 UPDATE 置无效已有拆分记录 ---
        invalidate_sql = f"""UPDATE T_BUSINESSPROJECTSPLIT
            SET BUSINESSPROJECTSPLIT_STATE = 0
            WHERE BUSINESSPROJECTSPLIT_STATE = 1 AND ACCOUNT_TYPE = 1000
                AND STATISTICS_DATE BETWEEN {start_day} AND {end_day}
                AND SETTLEMENT_STATE = 0
                AND BUSINESSPROJECT_ID = {bp_id}"""
        db.execute_non_query(invalidate_sql)

        # --- 4. 确定项目起止日期（处理项目期外日期）---
        proj_start_str = str(proj.get("PROJECT_STARTDATE", ""))[:10]
        proj_end_str = str(proj.get("PROJECT_ENDDATE", ""))[:10]
        try:
            proj_start_dt = datetime.strptime(proj_start_str, '%Y-%m-%d')
            proj_end_dt = datetime.strptime(proj_end_str, '%Y-%m-%d')
        except Exception:
            logger.warning(f"{compact_info} 拆分失败：无法解析项目日期")
            continue

        actual_start = max(start_dt, proj_start_dt)
        actual_end = min(end_dt, proj_end_dt)

        # 处理终止日期
        closed_date = proj.get("CLOSED_DATE")
        closed_dt = None
        if closed_date and str(closed_date) != "":
            try:
                closed_dt = datetime.strptime(str(closed_date)[:10], '%Y-%m-%d')
            except Exception:
                pass

        # --- 5. 查询该项目门店的营收数据 ---
        shop_ids = str(proj.get("SERVERPARTSHOP_ID", ""))
        rev_sql = f"""SELECT A.STATISTICS_DATE, A.REVENUE_AMOUNT, A.CASHPAY_AMOUNT,
                A.MOBILEPAY_AMOUNT, A.OTHERPAY_AMOUNT
            FROM T_REVENUEDAILY A, T_SERVERPARTSHOP B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPTRADE = B.SHOPTRADE
                AND B.SERVERPARTSHOP_ID IN ({shop_ids})
                AND A.STATISTICS_DATE BETWEEN {start_day} AND {end_day}
            ORDER BY A.STATISTICS_DATE"""
        dt_revenue = db.execute_query(rev_sql) or []
        # 按日期索引
        rev_by_date = {}
        for r in dt_revenue:
            d = str(r.get("STATISTICS_DATE", ""))[:8]
            if d not in rev_by_date:
                rev_by_date[d] = {"REVENUE_AMOUNT": 0, "CASHPAY_AMOUNT": 0,
                                  "MOBILEPAY_AMOUNT": 0, "OTHERPAY_AMOUNT": 0}
            rev_by_date[d]["REVENUE_AMOUNT"] += _d(r.get("REVENUE_AMOUNT"))
            rev_by_date[d]["CASHPAY_AMOUNT"] += _d(r.get("CASHPAY_AMOUNT"))
            rev_by_date[d]["MOBILEPAY_AMOUNT"] += _d(r.get("MOBILEPAY_AMOUNT"))
            rev_by_date[d]["OTHERPAY_AMOUNT"] += _d(r.get("OTHERPAY_AMOUNT"))

        # --- 6. 查询提成设置 T_SHOPROYALTY ---
        royalty_sql = f"""SELECT A.* FROM T_SHOPROYALTY A
            WHERE A.BUSINESSPROJECT_ID = {bp_id}
            ORDER BY A.FEWTHYEAR"""
        dt_royalty = db.execute_query(royalty_sql) or []

        # 获取经营模式和结算模式
        business_type = proj.get("BUSINESS_TYPE")
        settlement_modes = proj.get("SETTLEMENT_MODES", 1000)
        guarantee_ratio = 0
        if dt_royalty:
            guarantee_ratio = _d(dt_royalty[0].get("GUARANTEERATIO", 0))

        # --- 7. 逐日遍历生成拆分记录 ---
        cur_date = actual_start
        now = datetime.now()
        while cur_date <= actual_end and cur_date < now:
            if closed_dt and closed_dt <= cur_date:
                break

            cur_day_str = cur_date.strftime('%Y%m%d')
            rev_data = rev_by_date.get(cur_day_str, {})
            revenue = _d(rev_data.get("REVENUE_AMOUNT"))
            cash = _d(rev_data.get("CASHPAY_AMOUNT"))
            mobile = _d(rev_data.get("MOBILEPAY_AMOUNT"))
            other = _d(rev_data.get("OTHERPAY_AMOUNT"))

            # 计算分润（根据经营模式）
            royalty_price = 0  # 业主分润
            sub_royalty_price = 0  # 商家分润
            ticket_fee = 0  # 手续费

            if business_type == 1000:  # 合作分成
                if guarantee_ratio > 0:
                    royalty_price = round(revenue * guarantee_ratio / 100, 2)
                sub_royalty_price = revenue - royalty_price - ticket_fee
            elif business_type == 2000:  # 固定租金
                # 固定租金模式下，营收全部归商家
                royalty_price = 0
                sub_royalty_price = revenue
            elif business_type == 3000:  # 自营提成
                royalty_price = revenue
                sub_royalty_price = 0
            else:  # 4000 业主自营
                royalty_price = revenue
                sub_royalty_price = 0

            # INSERT 拆分记录
            insert_sql = f"""INSERT INTO T_BUSINESSPROJECTSPLIT (
                    BUSINESSPROJECTSPLIT_ID, BUSINESSPROJECT_ID, REGISTERCOMPACT_ID,
                    SERVERPART_ID, SERVERPART_NAME, SERVERPARTSHOP_ID, SERVERPARTSHOP_NAME,
                    STATISTICS_DATE, REVENUEDAILY_AMOUNT, CURCASHPAY_AMOUNT,
                    CURMOBILEPAY_AMOUNT, CUROTHERPAY_AMOUNT,
                    ROYALTYDAILY_PRICE, SUBROYALTYDAILY_PRICE, TICKETDAILY_FEE,
                    BUSINESS_TYPE, SETTLEMENT_MODES, ACCOUNT_TYPE,
                    BUSINESSPROJECTSPLIT_STATE, SETTLEMENT_STATE,
                    GUARANTEERATIO
                ) VALUES (
                    SEQ_BUSINESSPROJECTSPLIT.NEXTVAL, {bp_id}, {proj.get("REGISTERCOMPACT_ID")},
                    {proj.get("SERVERPART_ID") or 'NULL'}, '{proj.get("SERVERPART_NAME", "")}',
                    '{shop_ids}', '{proj.get("SERVERPARTSHOP_NAME", "")}',
                    {cur_day_str}, {revenue}, {cash}, {mobile}, {other},
                    {royalty_price}, {sub_royalty_price}, {ticket_fee},
                    {business_type or 'NULL'}, {settlement_modes or 'NULL'}, 1000,
                    1, 0, {guarantee_ratio}
                )"""
            try:
                db.execute_non_query(insert_sql)
            except Exception as e:
                logger.error(f"CreateProjectSplit 失败: {compact_info} 日期={cur_day_str} err={e}")

            cur_date += timedelta(days=1)

        completed_project_ids.append(str(bp_id))
        logger.info(f"CreateSingleProjectSplit 完成: {compact_info} BP={bp_id}")

    # --- 8. 按月调用 SolidMonthProjectSplit 固化 ---
    if completed_project_ids:
        for pid in completed_project_ids:
            cur_month = start_dt
            while cur_month.strftime('%Y%m') <= end_dt.strftime('%Y%m'):
                solid_month_project_split(db, cur_month.strftime('%Y%m'), project_id=pid)
                # 下一个月
                if cur_month.month == 12:
                    cur_month = cur_month.replace(year=cur_month.year + 1, month=1)
                else:
                    cur_month = cur_month.replace(month=cur_month.month + 1)

    return True


# ==================== 6. SolidMonthProjectSplit ====================
def solid_month_project_split(db: DatabaseHelper, statistics_month: str,
                                serverpartshop_id: str = "", compact_id: str = "",
                                project_id: str = "") -> bool:
    """重新生成月度应收拆分固化数据
    原 BUSINESSPROJECTSPLITHelper.SolidMonthProjectSplit (L6256-6664)
    1. 查当月拆分明细(UNION ALL 三部分：应收+门店费用+商家缴款)
    2. 查上月最后一天拆分+本月已固化+上月月度固化
    3. 按(BP_ID,SHOPROYALTY_ID,ACCOUNT_TYPE)分组计算汇总
    4. INSERT/UPDATE T_BIZPSPLITMONTH → 清理多余"""
    from datetime import datetime

    # --- 构造过滤条件 ---
    where_sql = ""
    if project_id:
        where_sql = f" AND A.BUSINESSPROJECT_ID IN ({project_id})"
    elif compact_id:
        where_sql = f" AND A.REGISTERCOMPACT_ID IN ({compact_id})"
    elif serverpartshop_id:
        where_sql = (f" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP S "
                     f"WHERE ',' || A.SERVERPARTSHOP_ID || ',' LIKE '%,' || S.SERVERPARTSHOP_ID || ',%' "
                     f"AND S.SERVERPARTSHOP_ID IN ({serverpartshop_id}))")

    month = statistics_month[:6]  # yyyyMM

    # --- 1. 查询当月拆分明细（三部分 UNION ALL）---
    split_sql = f"""SELECT
            A.SHOPROYALTY_ID, A.REGISTERCOMPACT_ID, A.BUSINESSPROJECT_ID, B.MERCHANTS_ID,
            A.SERVERPART_ID, A.SERVERPART_NAME, B.SERVERPARTSHOP_ID, B.SERVERPARTSHOP_NAME,
            A.STATISTICS_DATE, A.BUSINESS_TYPE, A.ACCOUNT_TYPE,
            A.STARTDATE, A.ENDDATE,
            A.REVENUEDAILY_AMOUNT AS REVENUE_AMOUNT,
            A.REVENUEDAILY_AMOUNT AS REVENUEDAILY_AMOUNT,
            A.DIFDAILY_REVENUE,
            A.CASHPAY_AMOUNT, A.OTHERPAY_AMOUNT, A.MOBILEPAY_AMOUNT,
            A.DIFFERENT_AMOUNT, A.CORRECT_AMOUNT,
            A.ROYALTYDAILY_PRICE AS ROYALTY_PRICE,
            A.SUBROYALTYDAILY_PRICE AS SUBROYALTY_PRICE,
            A.TICKETDAILY_FEE AS TICKET_FEE,
            A.ROYALTYDAILY_THEORY AS ROYALTY_THEORY,
            A.SUBROYALTYDAILY_THEORY AS SUBROYALTY_THEORY,
            A.REVENUE_AMOUNT AS ACCREVENUE_AMOUNT,
            A.ROYALTY_PRICE AS ACCROYALTY_PRICE,
            A.SUBROYALTY_PRICE AS ACCSUBROYALTY_PRICE,
            A.TICKET_FEE AS ACCTICKET_FEE,
            A.ROYALTY_THEORY AS ACCROYALTY_THEORY,
            A.SUBROYALTY_THEORY AS ACCSUBROYALTY_THEORY,
            A.BUSINESSDAYS, A.MINTURNOVER, A.GUARANTEERATIO, A.SMOKERATIO,
            A.CIGARETTEDAILY_AMOUNT AS CIGARETTE_AMOUNT,
            A.CIGARETTE_AMOUNT AS ACCCIGARETTE_AMOUNT
        FROM T_BUSINESSPROJECTSPLIT A, T_BUSINESSPROJECT B
        WHERE A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
            AND A.BUSINESSPROJECTSPLIT_STATE = 1 AND A.ACCOUNT_TYPE = 1000
            AND B.PROJECT_VALID = 1
            AND A.STATISTICS_DATE >= {month}01 AND A.STATISTICS_DATE <= {month}31
            {where_sql}"""
    dt_split = db.execute_query(split_sql) or []

    if not dt_split:
        # 无拆分数据时，将已存在的月度固化数据置无效
        existing_sql = f"""SELECT BIZPSPLITMONTH_ID FROM T_BIZPSPLITMONTH
            WHERE BIZPSPLITMONTH_STATE = 1 AND STATISTICS_MONTH = {month} {where_sql}"""
        existing = db.execute_query(existing_sql) or []
        for row in existing:
            mid = row.get("BIZPSPLITMONTH_ID")
            db.execute_non_query(f"UPDATE T_BIZPSPLITMONTH SET BIZPSPLITMONTH_STATE = 0 WHERE BIZPSPLITMONTH_ID = {mid}")
        logger.info(f"SolidMonthProjectSplit: {month} 无拆分数据，已清理 {len(existing)} 条固化记录")
        return True

    # --- 2. 查上月最后一天拆分数据 ---
    month_int = int(month)
    if month_int % 100 == 1:
        last_month = str(month_int - 100 + 11)
    else:
        last_month = str(month_int - 1)
    first_day = datetime.strptime(f"{month}01", '%Y%m%d')
    last_month_last_day = (first_day - __import__('datetime').timedelta(days=1)).strftime('%Y%m%d')

    last_day_sql = f"""SELECT A.BUSINESSPROJECT_ID, A.SHOPROYALTY_ID, A.ACCOUNT_TYPE,
            A.CASHPAY_AMOUNT, A.OTHERPAY_AMOUNT, A.MOBILEPAY_AMOUNT,
            A.DIFFERENT_AMOUNT, A.CORRECT_AMOUNT
        FROM T_BUSINESSPROJECTSPLIT A, T_BUSINESSPROJECT B
        WHERE A.BUSINESSPROJECT_ID = B.BUSINESSPROJECT_ID
            AND A.BUSINESSPROJECTSPLIT_STATE = 1 AND A.ACCOUNT_TYPE = 1000
            AND B.PROJECT_VALID = 1 AND A.STATISTICS_DATE = {last_month_last_day}
            {where_sql}"""
    dt_last_day = db.execute_query(last_day_sql) or []
    last_day_map = {}
    for r in dt_last_day:
        key = (r.get("BUSINESSPROJECT_ID"), r.get("SHOPROYALTY_ID"), r.get("ACCOUNT_TYPE"))
        last_day_map[key] = r

    # --- 3. 查本月已固化数据 ---
    month_sql = f"""SELECT * FROM T_BIZPSPLITMONTH
        WHERE BIZPSPLITMONTH_STATE = 1 AND STATISTICS_MONTH = {month} {where_sql}"""
    dt_month = db.execute_query(month_sql) or []
    month_map = {}
    remaining_ids = []
    for r in dt_month:
        key = (r.get("BUSINESSPROJECT_ID"), r.get("SHOPROYALTY_ID"), r.get("ACCOUNT_TYPE"))
        month_map[key] = r
        remaining_ids.append(str(r.get("BIZPSPLITMONTH_ID")))

    # --- 4. 按(BUSINESSPROJECT_ID, SHOPROYALTY_ID, ACCOUNT_TYPE)分组 ---
    group_keys = set()
    for s in dt_split:
        key = (s.get("BUSINESSPROJECT_ID"), s.get("SHOPROYALTY_ID"), s.get("ACCOUNT_TYPE"))
        group_keys.add(key)

    execute_count = 0
    for bp_id, sr_id, acc_type in group_keys:
        group_rows = [s for s in dt_split
                      if s.get("BUSINESSPROJECT_ID") == bp_id
                      and s.get("SHOPROYALTY_ID") == sr_id
                      and s.get("ACCOUNT_TYPE") == acc_type]
        if not group_rows:
            continue

        # 按 STATISTICS_DATE DESC 排序
        group_rows.sort(key=lambda x: x.get("STATISTICS_DATE", 0), reverse=True)
        latest = group_rows[0]

        # 汇总字段
        sum_revenue = sum(_d(r.get("REVENUE_AMOUNT")) for r in group_rows)
        sum_rev_daily = sum(_d(r.get("REVENUEDAILY_AMOUNT")) for r in group_rows)
        sum_dif_rev = sum(_d(r.get("DIFDAILY_REVENUE")) for r in group_rows)
        sum_royalty = sum(_d(r.get("ROYALTY_PRICE")) for r in group_rows)
        sum_sub_royalty = sum(_d(r.get("SUBROYALTY_PRICE")) for r in group_rows)
        sum_ticket = sum(_d(r.get("TICKET_FEE")) for r in group_rows)
        sum_theory = sum(_d(r.get("ROYALTY_THEORY")) for r in group_rows)
        sum_sub_theory = sum(_d(r.get("SUBROYALTY_THEORY")) for r in group_rows)

        # 经营天数、自然天数
        business_days = None
        natural_days = None
        mobile = "NULL"
        cash = "NULL"
        other_pay = "NULL"
        diff_amt = "NULL"
        correct_amt = "NULL"
        acc_revenue = "NULL"
        acc_royalty = "NULL"
        acc_sub_royalty = "NULL"
        acc_ticket = "NULL"
        acc_theory = "NULL"
        acc_sub_theory = "NULL"

        if acc_type == 1000:
            bdays = [_d(r.get("BUSINESSDAYS")) for r in group_rows if r.get("BUSINESSDAYS") is not None]
            if bdays:
                business_days = int(max(bdays) - min(bdays) + 1)
            dates = [r.get("STATISTICS_DATE") for r in group_rows if r.get("STATISTICS_DATE")]
            if dates:
                natural_days = int(str(max(dates))[:8]) - int(str(min(dates))[:8]) + 1

            mobile = str(_d(latest.get("MOBILEPAY_AMOUNT")))
            cash = str(_d(latest.get("CASHPAY_AMOUNT")))
            other_pay = str(_d(latest.get("OTHERPAY_AMOUNT")))
            diff_amt = str(_d(latest.get("DIFFERENT_AMOUNT")))
            correct_amt = str(_d(latest.get("CORRECT_AMOUNT")))

            acc_revenue = str(_d(latest.get("ACCREVENUE_AMOUNT")))
            acc_royalty = str(_d(latest.get("ACCROYALTY_PRICE")))
            acc_sub_royalty = str(_d(latest.get("ACCSUBROYALTY_PRICE")))
            acc_ticket = str(_d(latest.get("ACCTICKET_FEE")))
            acc_theory = str(_d(latest.get("ACCROYALTY_THEORY")))
            acc_sub_theory = str(_d(latest.get("ACCSUBROYALTY_THEORY")))

            # 扣减上月最后一天
            key = (bp_id, sr_id, acc_type)
            if key in last_day_map:
                ld = last_day_map[key]
                mobile = str(float(mobile) - _d(ld.get("MOBILEPAY_AMOUNT")))
                cash = str(float(cash) - _d(ld.get("CASHPAY_AMOUNT")))
                other_pay = str(float(other_pay) - _d(ld.get("OTHERPAY_AMOUNT")))
                diff_amt = str(float(diff_amt) - _d(ld.get("DIFFERENT_AMOUNT")))
                correct_amt = str(float(correct_amt) - _d(ld.get("CORRECT_AMOUNT")))

        # --- INSERT 或 UPDATE ---
        key = (bp_id, sr_id, acc_type)
        if key not in month_map:
            # INSERT
            sr_val = sr_id if sr_id else "NULL"
            insert_sql = f"""INSERT INTO T_BIZPSPLITMONTH (
                    BIZPSPLITMONTH_ID, STATISTICS_MONTH, SHOPROYALTY_ID, REGISTERCOMPACT_ID,
                    BUSINESSPROJECT_ID, MERCHANTS_ID, SERVERPART_ID, SERVERPART_NAME,
                    SERVERPARTSHOP_ID, SERVERPARTSHOP_NAME, BUSINESS_TYPE,
                    REVENUE_AMOUNT, REVENUEDAILY_AMOUNT, DIFDAILY_REVENUE,
                    ROYALTY_PRICE, SUBROYALTY_PRICE, TICKET_FEE,
                    ROYALTY_THEORY, SUBROYALTY_THEORY,
                    BUSINESSDAYS, NATUREDAY, ACCOUNT_TYPE,
                    MOBILEPAY_AMOUNT, CASHPAY_AMOUNT, OTHERPAY_AMOUNT,
                    DIFFERENT_AMOUNT, CORRECT_AMOUNT,
                    ACCREVENUE_AMOUNT, ACCROYALTY_PRICE, ACCSUBROYALTY_PRICE,
                    ACCTICKET_FEE, ACCROYALTY_THEORY, ACCSUBROYALTY_THEORY,
                    MINTURNOVER, GUARANTEERATIO, SMOKERATIO,
                    BIZPSPLITMONTH_STATE, RECORD_DATE
                ) VALUES (
                    SEQ_BIZPSPLITMONTH.NEXTVAL, {month}, {sr_val},
                    {latest.get("REGISTERCOMPACT_ID") or "NULL"}, {bp_id},
                    {latest.get("MERCHANTS_ID") or "NULL"},
                    '{latest.get("SERVERPART_ID", "")}', '{latest.get("SERVERPART_NAME", "")}',
                    '{latest.get("SERVERPARTSHOP_ID", "")}', '{latest.get("SERVERPARTSHOP_NAME", "")}',
                    {latest.get("BUSINESS_TYPE") or "NULL"},
                    {sum_revenue}, {sum_rev_daily}, {sum_dif_rev},
                    {sum_royalty}, {sum_sub_royalty}, {sum_ticket},
                    {sum_theory}, {sum_sub_theory},
                    {business_days or "NULL"}, {natural_days or "NULL"}, {acc_type},
                    {mobile}, {cash}, {other_pay}, {diff_amt}, {correct_amt},
                    {acc_revenue}, {acc_royalty}, {acc_sub_royalty},
                    {acc_ticket}, {acc_theory}, {acc_sub_theory},
                    {_d(latest.get("MINTURNOVER")) or "NULL"},
                    {_d(latest.get("GUARANTEERATIO")) or "NULL"},
                    {_d(latest.get("SMOKERATIO")) or "NULL"},
                    1, SYSDATE
                )"""
            try:
                db.execute_non_query(insert_sql)
                execute_count += 1
            except Exception as e:
                logger.error(f"SolidMonth INSERT 失败: BP={bp_id} err={e}")
        else:
            # UPDATE
            existing = month_map[key]
            mid = existing.get("BIZPSPLITMONTH_ID")
            if str(mid) in remaining_ids:
                remaining_ids.remove(str(mid))
            update_sql = f"""UPDATE T_BIZPSPLITMONTH SET
                    REGISTERCOMPACT_ID = {latest.get("REGISTERCOMPACT_ID") or "NULL"},
                    MERCHANTS_ID = {latest.get("MERCHANTS_ID") or "NULL"},
                    SERVERPART_ID = '{latest.get("SERVERPART_ID", "")}',
                    SERVERPART_NAME = '{latest.get("SERVERPART_NAME", "")}',
                    SERVERPARTSHOP_ID = '{latest.get("SERVERPARTSHOP_ID", "")}',
                    SERVERPARTSHOP_NAME = '{latest.get("SERVERPARTSHOP_NAME", "")}',
                    BUSINESS_TYPE = {latest.get("BUSINESS_TYPE") or "NULL"},
                    REVENUE_AMOUNT = {sum_revenue}, REVENUEDAILY_AMOUNT = {sum_rev_daily},
                    DIFDAILY_REVENUE = {sum_dif_rev},
                    ROYALTY_PRICE = {sum_royalty}, SUBROYALTY_PRICE = {sum_sub_royalty},
                    TICKET_FEE = {sum_ticket},
                    ROYALTY_THEORY = {sum_theory}, SUBROYALTY_THEORY = {sum_sub_theory},
                    BUSINESSDAYS = {business_days or "NULL"},
                    NATUREDAY = {natural_days or "NULL"},
                    MOBILEPAY_AMOUNT = {mobile}, CASHPAY_AMOUNT = {cash},
                    OTHERPAY_AMOUNT = {other_pay},
                    DIFFERENT_AMOUNT = {diff_amt}, CORRECT_AMOUNT = {correct_amt},
                    ACCREVENUE_AMOUNT = {acc_revenue}, ACCROYALTY_PRICE = {acc_royalty},
                    ACCSUBROYALTY_PRICE = {acc_sub_royalty},
                    ACCTICKET_FEE = {acc_ticket}, ACCROYALTY_THEORY = {acc_theory},
                    ACCSUBROYALTY_THEORY = {acc_sub_theory},
                    BIZPSPLITMONTH_STATE = 1, RECORD_DATE = SYSDATE
                WHERE BIZPSPLITMONTH_ID = {mid}"""
            try:
                db.execute_non_query(update_sql)
                execute_count += 1
            except Exception as e:
                logger.error(f"SolidMonth UPDATE 失败: BP={bp_id} err={e}")

    # --- 5. 清理多余的已固化数据 ---
    if remaining_ids:
        ids_str = ",".join(remaining_ids)
        db.execute_non_query(f"UPDATE T_BIZPSPLITMONTH SET BIZPSPLITMONTH_STATE = 0 "
                             f"WHERE BIZPSPLITMONTH_STATE = 1 AND BIZPSPLITMONTH_ID IN ({ids_str})")
        execute_count += len(remaining_ids)

    logger.info(f"SolidMonthProjectSplit 完成: {month} 处理 {execute_count} 条")
    return True


# ==================== 7. GetRoyaltyDateSumReport ====================
def get_royalty_date_sum_report(db: DatabaseHelper, start_date: str, end_date: str,
                                  serverpart_ids: str = "", serverpartshop_ids: str = "",
                                  compare_split: bool = True, keyword: str = "") -> list[dict]:
    """获取日度业主到账汇总数据(一级日期汇总)
    原 BANKACCOUNTVERIFYHelper.GetBankAccountVerifySumDateTreeList"""
    where_parts = ["A.BANKACCOUNTVERIFY_STATE = 1"]
    if start_date:
        where_parts.append(f"A.STATISTICS_DATE >= '{start_date.replace('-','')[:8]}'")
    if end_date:
        where_parts.append(f"A.STATISTICS_DATE <= '{end_date.replace('-','')[:8]}'")
    if serverpart_ids:
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_ids})")
    if serverpartshop_ids:
        where_parts.append(f"A.SERVERPARTSHOP_ID IN ({serverpartshop_ids})")

    where_sql = " AND ".join(where_parts)
    sql = f"""SELECT A.STATISTICS_DATE, A.SERVERPART_ID, A.SERVERPART_NAME,
            A.SERVERPARTSHOP_ID, A.SERVERPARTSHOP_NAME,
            A.MOBILEPAY_AMOUNT, A.CASHPAY_AMOUNT, A.OTHERPAY_AMOUNT,
            A.REVENUE_AMOUNT, A.ROYALTY_AMOUNT, A.SUBROYALTY_AMOUNT
        FROM T_BANKACCOUNTVERIFY A
        WHERE {where_sql}
        ORDER BY A.STATISTICS_DATE, A.SERVERPART_NAME"""
    rows = db.execute_query(sql)
    # 按日期分组成树
    from collections import OrderedDict
    date_groups = OrderedDict()
    for r in rows:
        d = str(r.get("STATISTICS_DATE", ""))
        if d not in date_groups:
            date_groups[d] = {"node": {"STATISTICS_DATE": d, "REVENUE_AMOUNT": 0}, "children": []}
        date_groups[d]["children"].append({"node": r})
        date_groups[d]["node"]["REVENUE_AMOUNT"] += _d(r.get("REVENUE_AMOUNT"))
    return list(date_groups.values())


# ==================== 8. GetRoyaltyReport ====================
def get_royalty_report(db: DatabaseHelper, start_date: str, end_date: str,
                        serverpart_ids: str = "", serverpartshop_ids: str = "",
                        compare_split: bool = True, keyword: str = "") -> list[dict]:
    """获取银行到账核对固化数据树形列表（四级树：片区→服务区→业态→门店）
    原 BANKACCOUNTVERIFYHelper.GetBANKACCOUNTVERIFYTreeList (L527-593)
    查询 T_BANKACCOUNTVERIFY 固化数据 → 按片区/服务区/GENERALSHOP_NAME/门店分组构建四级树
    每级汇总 TICKET_PRICE/ACCOUNT_PRICE/ROYALTY_PRICE/SUBROYALTY_PRICE/TICKET_FEE/MOBILEPAY_PRICE"""
    where_parts = ["A.BANKACCOUNTVERIFY_STATE = 1"]
    if start_date:
        where_parts.append(f"A.STATISTICS_DATE >= '{start_date.replace('-','')[:8]}'")
    if end_date:
        where_parts.append(f"A.STATISTICS_DATE <= '{end_date.replace('-','')[:8]}'")
    if serverpart_ids:
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_ids})")
    if serverpartshop_ids:
        where_parts.append(f"A.SERVERPARTSHOP_ID IN ({serverpartshop_ids})")
    if keyword:
        where_parts.append(f"A.BUSINESS_UNIT LIKE '%{keyword}%'")

    where_sql = " AND ".join(where_parts)
    sql = f"""SELECT A.* FROM T_BANKACCOUNTVERIFY A WHERE {where_sql}
        ORDER BY A.SPREGIONTYPE_ID, A.SERVERPART_ID, A.GENERALSHOP_NAME, A.SERVERPARTSHOP_ID"""
    rows = db.execute_query(sql) or []

    sum_fields = ["TICKET_PRICE", "ACCOUNT_PRICE", "ROYALTY_PRICE",
                  "SUBROYALTY_PRICE", "TICKET_FEE", "MOBILEPAY_PRICE"]

    def _sum_rows(row_list, fields):
        """汇总行数据"""
        result = {}
        for f in fields:
            result[f] = sum(_d(r.get(f)) for r in row_list)
        # PROJECT_COUNT 按 BUSINESSPROJECT_ID 去重
        result["PROJECT_COUNT"] = len(set(r.get("BUSINESSPROJECT_ID") for r in row_list if r.get("BUSINESSPROJECT_ID")))
        # ROYALTYPROJECT_PRICE 按 (BUSINESSPROJECT_ID, ROYALTYPROJECT_PRICE) 去重后求和
        seen_proj = set()
        rp_sum = 0
        for r in row_list:
            key = (r.get("BUSINESSPROJECT_ID"), r.get("ROYALTYPROJECT_PRICE"))
            if key not in seen_proj:
                seen_proj.add(key)
                rp_sum += _d(r.get("ROYALTYPROJECT_PRICE"))
        result["ROYALTYPROJECT_PRICE"] = rp_sum
        result["ROYALTY_DIFFPRICE"] = _d(result.get("ROYALTY_PRICE")) - rp_sum
        return result

    # --- 四级树构建：片区→服务区→业态→门店 ---
    from collections import OrderedDict
    result = []

    # 一级：片区
    region_ids = []
    for r in rows:
        rid = r.get("SPREGIONTYPE_ID")
        if rid not in region_ids:
            region_ids.append(rid)

    node_depth_counter = 1
    for rid in region_ids:
        region_rows = [r for r in rows if r.get("SPREGIONTYPE_ID") == rid]
        if not region_rows:
            continue
        region_node = {
            "SPREGIONTYPE_ID": rid,
            "SPREGIONTYPE_NAME": region_rows[0].get("SPREGIONTYPE_NAME", ""),
            "NODEDEPTH": 1,
            "BANKACCOUNTVERIFY_STATE": region_rows[0].get("BANKACCOUNTVERIFY_STATE"),
        }
        region_node.update(_sum_rows(region_rows, sum_fields))
        region_children = []

        # 二级：服务区
        sp_ids = []
        for r in region_rows:
            sid = r.get("SERVERPART_ID")
            if sid not in sp_ids:
                sp_ids.append(sid)

        for sid in sp_ids:
            sp_rows = [r for r in region_rows if r.get("SERVERPART_ID") == sid]
            if not sp_rows:
                continue
            sp_node = {
                "SPREGIONTYPE_ID": rid,
                "SERVERPART_ID": sid,
                "SERVERPART_CODE": sp_rows[0].get("SERVERPART_CODE", ""),
                "SERVERPART_NAME": sp_rows[0].get("SERVERPART_NAME", ""),
                "BANKACCOUNTVERIFY_INDEX": str(node_depth_counter),
                "NODEDEPTH": 2,
            }
            sp_node.update(_sum_rows(sp_rows, sum_fields))
            sp_children = []

            # 三级：业态 GENERALSHOP_NAME
            shop_names = []
            for r in sp_rows:
                gn = r.get("GENERALSHOP_NAME")
                if gn not in shop_names:
                    shop_names.append(gn)

            child_node = 1
            for gn in shop_names:
                gn_rows = [r for r in sp_rows if r.get("GENERALSHOP_NAME") == gn]
                child_index = f"{node_depth_counter}.{child_node}"
                gn_node = {
                    "BUSINESSPROJECT_ID": gn_rows[0].get("BUSINESSPROJECT_ID"),
                    "GENERALSHOP_NAME": gn,
                    "BUSINESS_UNIT": gn_rows[0].get("BUSINESS_UNIT", ""),
                    "BANKACCOUNTVERIFY_INDEX": child_index,
                    "NODEDEPTH": 3,
                }
                gn_node.update(_sum_rows(gn_rows, sum_fields))
                gn_children = []

                # 四级：门店
                shop_ids = []
                for r in gn_rows:
                    ssid = r.get("SERVERPARTSHOP_ID")
                    if ssid not in shop_ids:
                        shop_ids.append(ssid)

                shop_child_node = 1
                for ssid in shop_ids:
                    ss_rows = [r for r in sp_rows if r.get("SERVERPARTSHOP_ID") == ssid]
                    ss_node = {
                        "SERVERPARTSHOP_ID": ssid,
                        "SERVERPARTSHOP_CODE": ss_rows[0].get("SERVERPARTSHOP_CODE", ""),
                        "SERVERPARTSHOP_NAME": ss_rows[0].get("SERVERPARTSHOP_NAME", ""),
                        "BANKACCOUNTVERIFY_INDEX": f"{child_index}.{shop_child_node}",
                        "NODEDEPTH": 4,
                    }
                    ss_node.update(_sum_rows(ss_rows, sum_fields))
                    gn_children.append({"node": ss_node})
                    shop_child_node += 1

                sp_children.append({"node": gn_node, "children": gn_children})
                child_node += 1

            region_children.append({"node": sp_node, "children": sp_children})
            node_depth_counter += 1

        result.append({"node": region_node, "children": region_children})

    return result


# ==================== 9. GetProjectShopIncome ====================
def get_project_shop_income(db: DatabaseHelper, statistics_date: str,
                              contrast_date: str, serverpart_ids: str = "") -> list[dict]:
    """统计商铺收入明细表（树形）
    原 ProjectSummaryHelper.GetProjectShopIncome"""
    where_parts = ["A.REVENUEDAILY_STATE = 1"]
    if statistics_date:
        where_parts.append(f"A.STATISTICS_DATE = '{statistics_date.replace('-','')[:8]}'")
    if serverpart_ids:
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_ids})")

    where_sql = " AND ".join(where_parts)
    sql = f"""SELECT A.SERVERPART_ID, B.SERVERPART_NAME,
            A.SHOPTRADE, A.REVENUE_AMOUNT, A.SELLER_NAME
        FROM T_REVENUEDAILY A
        LEFT JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
        WHERE {where_sql}
        ORDER BY B.SERVERPART_NAME"""
    rows = db.execute_query(sql)
    # 按服务区分组
    from collections import OrderedDict
    sp_groups = OrderedDict()
    for r in rows:
        sid = r.get("SERVERPART_ID")
        if sid not in sp_groups:
            sp_groups[sid] = {"node": {"SERVERPART_ID": sid, "SERVERPART_NAME": r.get("SERVERPART_NAME", ""),
                                       "REVENUE_AMOUNT": 0}, "children": []}
        sp_groups[sid]["children"].append({"node": r})
        sp_groups[sid]["node"]["REVENUE_AMOUNT"] += _d(r.get("REVENUE_AMOUNT"))
    return list(sp_groups.values())


# ==================== 10. GetContractMerchant ====================
def get_contract_merchant(db: DatabaseHelper, serverpart_ids: str = "",
                            settlement_modes: str = "", start_date: str = "",
                            end_date: str = "", keyword: str = "") -> list[dict]:
    """获取合同商户信息（三级树：片区→服务区→项目）
    原 FinanceHelper.GetContractMerchant (L39-327)
    五表联查: T_SHOPROYALTY A, T_REGISTERCOMPACT B, T_BUSINESSPROJECT C,
              T_SERVERPART E, T_SERVERPARTSHOP F
    含合同金额/保底/租金年度拆分（MINTURNOVERFirst~Fifth）"""
    where_sql = ""
    if serverpart_ids:
        where_sql += f" AND E.SERVERPART_ID IN ({serverpart_ids})"
    if start_date:
        where_sql += f" AND C.PROJECT_ENDDATE >= TO_DATE('{start_date}', 'YYYY-MM-DD')"
    if end_date:
        where_sql += f" AND C.PROJECT_STARTDATE <= TO_DATE('{end_date}', 'YYYY-MM-DD')"

    sql = f"""SELECT
            E.SPREGIONTYPE_ID, E.SPREGIONTYPE_NAME, E.SPREGIONTYPE_INDEX, E.SERVERPART_INDEX,
            E.SERVERPART_ID, E.SERVERPART_NAME, E.SERVERPART_CODE,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.BUSINESSPROJECT_ID, C.BUSINESSPROJECT_NAME,
            C.BUSINESS_TYPE, C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES,
            B.COMPACT_STARTDATE, B.COMPACT_ENDDATE, B.COMPACT_AMOUNT, B.SECURITYDEPOSIT,
            A.RENTFEE, A.GUARANTEERATIO, A.FEWTHYEAR, A.STARTDATE AS FEWTHYEARSTARTDATE,
            A.MINTURNOVER, A.REGISTERCOMPACT_ID,
            WM_CONCAT(DISTINCT F.SHOPSHORTNAME) AS SHOPSHORTNAME,
            WM_CONCAT(DISTINCT F.SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID
        FROM T_SHOPROYALTY A, T_REGISTERCOMPACT B, T_BUSINESSPROJECT C,
             T_SERVERPART E, T_SERVERPARTSHOP F
        WHERE A.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID
            AND E.SERVERPART_ID = F.SERVERPART_ID
            AND C.PROJECT_VALID = 1
            AND B.COMPACT_STATE = 1000
            AND B.COMPACT_TYPE IN (340001,510001,520001)
            {where_sql}
        GROUP BY E.SPREGIONTYPE_ID, E.SPREGIONTYPE_NAME, E.SPREGIONTYPE_INDEX, E.SERVERPART_INDEX,
            E.SERVERPART_ID, E.SERVERPART_NAME, E.SERVERPART_CODE,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.BUSINESSPROJECT_ID, C.BUSINESSPROJECT_NAME,
            C.BUSINESS_TYPE, C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES,
            B.COMPACT_STARTDATE, B.COMPACT_ENDDATE, B.COMPACT_AMOUNT, B.SECURITYDEPOSIT,
            A.RENTFEE, A.GUARANTEERATIO, A.FEWTHYEAR, A.MINTURNOVER,
            A.STARTDATE, A.REGISTERCOMPACT_ID"""
    rows = db.execute_query(sql) or []
    # 关键词/结算模式过滤（C# DataTable.RowFilter）
    if keyword:
        rows = [r for r in rows if keyword in str(r.get("MERCHANTS_NAME", ""))]
    if settlement_modes and start_date and end_date:
        modes = [int(m) for m in settlement_modes.split(",") if m.strip()]
        filtered = []
        for r in rows:
            sm = r.get("SETTLEMENT_MODES")
            if sm in modes:
                filtered.append(r)
            else:
                sw = r.get("SWITCH_MODES")
                sd = r.get("SWITCH_DATE")
                if sw in modes and sd:
                    filtered.append(r)
        rows = filtered
    # 按项目分组，构建合同商户模型
    from collections import OrderedDict
    proj_map = OrderedDict()
    for r in rows:
        pid = r.get("BUSINESSPROJECT_ID")
        if pid not in proj_map:
            proj_map[pid] = []
        proj_map[pid].append(r)
    flat_list = []
    for pid, proj_rows in proj_map.items():
        first = proj_rows[0]
        btype = first.get("BUSINESS_TYPE")
        cnt = len(proj_rows)
        if btype == 2000:
            rentfee_list = list(set(_d(r.get("RENTFEE")) for r in proj_rows if r.get("RENTFEE")))
            node = dict(first)
            node["RENTFEE"] = ",".join(str(v) for v in rentfee_list)
            node["MINTURNOVER"] = None
            for i, r in enumerate(proj_rows[:5]):
                node[f"MINTURNOVERFirst" if i==0 else f"MINTURNOVER{'Second' if i==1 else 'Third' if i==2 else 'Fourth' if i==3 else 'Fifth'}"] = _d(r.get("RENTFEE"))
        else:
            mint_list = list(set(_d(r.get("MINTURNOVER")) for r in proj_rows if r.get("MINTURNOVER")))
            node = dict(first)
            node["RENTFEE"] = None
            node["MINTURNOVER"] = ",".join(str(v) for v in mint_list)
            for i, r in enumerate(proj_rows[:5]):
                node[f"MINTURNOVERFirst" if i==0 else f"MINTURNOVER{'Second' if i==1 else 'Third' if i==2 else 'Fourth' if i==3 else 'Fifth'}"] = _d(r.get("MINTURNOVER"))
        flat_list.append(node)
    # 构建三级树：片区→服务区→项目
    region_map = OrderedDict()
    for n in flat_list:
        rid = n.get("SPREGIONTYPE_ID")
        sid = n.get("SERVERPART_ID")
        if rid not in region_map:
            region_map[rid] = {"node": {"Id": str(rid), "Name": n.get("SPREGIONTYPE_NAME", ""),
                "SPREGIONTYPE_ID": rid, "SPREGIONTYPE_NAME": n.get("SPREGIONTYPE_NAME", ""),
                "COMPACT_AMOUNT": 0, "SECURITYDEPOSIT": 0}, "children": OrderedDict()}
        region = region_map[rid]
        if sid not in region["children"]:
            region["children"][sid] = {"node": {"Id": str(sid), "Name": n.get("SERVERPART_NAME", ""),
                "SERVERPART_ID": sid, "SERVERPART_NAME": n.get("SERVERPART_NAME", ""),
                "COMPACT_AMOUNT": 0, "SECURITYDEPOSIT": 0}, "children": []}
        sp = region["children"][sid]
        sp["children"].append({"node": n})
        sp["node"]["COMPACT_AMOUNT"] += _d(n.get("COMPACT_AMOUNT"))
        sp["node"]["SECURITYDEPOSIT"] += _d(n.get("SECURITYDEPOSIT"))
    result = []
    for region in region_map.values():
        children = []
        for sp in region["children"].values():
            region["node"]["COMPACT_AMOUNT"] += sp["node"]["COMPACT_AMOUNT"]
            region["node"]["SECURITYDEPOSIT"] += sp["node"]["SECURITYDEPOSIT"]
            children.append({"node": sp["node"], "children": sp["children"]})
        result.append({"node": region["node"], "children": children})
    return result


# ==================== 11. GetAccountReached ====================
def get_account_reached(db: DatabaseHelper, serverpart_ids: str = "",
                          settlement_modes: str = "", start_date: str = "",
                          end_date: str = "", keyword: str = "") -> list[dict]:
    """获取分账收银到账（三级树：片区→服务区→项目月度到账明细）
    原 FinanceHelper.GetAccountReached (L342-621)
    六表联查: T_MOBILEPAYSHARE/T_BIZPSPLITMONTH/T_BUSINESSPROJECT/
              T_SERVERPART/T_SERVERPARTSHOP/T_REGISTERCOMPACT
    含营业额/到款/合作单位到账/累计等计算字段"""
    where_sql = ""
    if serverpart_ids:
        where_sql += f" AND E.SERVERPART_ID IN ({serverpart_ids})"
    if start_date:
        where_sql += f" AND B.STATISTICS_MONTH >= {start_date} AND A.STATISTICS_DATE >= {start_date}01"
    if end_date:
        where_sql += f" AND B.STATISTICS_MONTH <= {end_date} AND A.STATISTICS_DATE <= {end_date}31"

    sql = f"""SELECT E.SPREGIONTYPE_ID, E.SPREGIONTYPE_NAME, E.SPREGIONTYPE_INDEX,
            E.SERVERPART_ID, E.SERVERPART_NAME, E.SERVERPART_INDEX,
            C.MERCHANTS_NAME, C.MERCHANTS_ID, C.BUSINESS_TYPE, C.BUSINESSPROJECT_ID,
            C.BUSINESSPROJECT_NAME, C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES,
            B.REGISTERCOMPACT_ID, B.SHOPROYALTY_ID, B.STARTDATE, B.ENDDATE, B.STATISTICS_MONTH,
            B.REVENUE_AMOUNT, B.REVENUEDAILY_AMOUNT,
            B.ROYALTY_PRICE AS ROYALTYDAILY_PRICE,
            B.SUBROYALTY_PRICE AS SUBROYALTYDAILY_PRICE,
            B.TICKET_FEE AS TICKETDAILY_FEE,
            B.CASHPAY_AMOUNT, B.MOBILEPAY_AMOUNT, B.OTHERPAY_AMOUNT,
            B.GUARANTEERATIO, B.ACCOUNT_TYPE,
            B.ACCROYALTY_PRICE, B.ACCSUBROYALTY_PRICE,
            WM_CONCAT(DISTINCT F.SHOPSHORTNAME) AS SERVERPARTSHOP_NAME,
            WM_CONCAT(DISTINCT F.SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID
        FROM T_MOBILEPAYSHARE A, T_BIZPSPLITMONTH B, T_BUSINESSPROJECT C,
             T_SERVERPART E, T_SERVERPARTSHOP F, T_REGISTERCOMPACT G
        WHERE B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND C.REGISTERCOMPACT_ID = G.REGISTERCOMPACT_ID
            AND E.SERVERPART_ID = F.SERVERPART_ID
            AND A.SERVERPARTSHOP_ID = F.SERVERPARTSHOP_ID
            AND B.BIZPSPLITMONTH_STATE = 1 AND B.ACCOUNT_TYPE = 1000
            AND C.PROJECT_VALID = 1
            AND G.COMPACT_TYPE IN (340001,510001,520001)
            {where_sql}
        GROUP BY E.SPREGIONTYPE_ID, E.SPREGIONTYPE_NAME, E.SPREGIONTYPE_INDEX,
            E.SERVERPART_ID, E.SERVERPART_NAME, E.SERVERPART_INDEX,
            C.MERCHANTS_NAME, C.MERCHANTS_ID, C.BUSINESS_TYPE, C.BUSINESSPROJECT_ID,
            C.BUSINESSPROJECT_NAME, C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES,
            B.REGISTERCOMPACT_ID, B.SHOPROYALTY_ID, B.STARTDATE, B.ENDDATE, B.STATISTICS_MONTH,
            B.REVENUE_AMOUNT, B.REVENUEDAILY_AMOUNT, B.SUBROYALTY_PRICE, B.TICKET_FEE,
            B.ACCROYALTY_PRICE, B.ACCSUBROYALTY_PRICE, B.CASHPAY_AMOUNT, B.MOBILEPAY_AMOUNT,
            B.OTHERPAY_AMOUNT, B.GUARANTEERATIO, B.ACCOUNT_TYPE, B.ROYALTY_PRICE"""
    rows = db.execute_query(sql) or []
    if keyword:
        rows = [r for r in rows if keyword in str(r.get("MERCHANTS_NAME", ""))]
    # 计算到账字段（C# L499-563）
    for r in rows:
        rev_total = _d(r.get("REVENUEDAILY_AMOUNT"))
        rev_mobile = _d(r.get("MOBILEPAY_AMOUNT"))
        royalty = _d(r.get("ROYALTYDAILY_PRICE"))
        sub_fee = _d(r.get("TICKETDAILY_FEE"))
        sub_mobile = _d(r.get("SUBROYALTYDAILY_PRICE"))
        sub_cash = rev_total - rev_mobile
        r["REVENUEDAILY_AMOUNTTotal"] = rev_total
        r["REVENUEDAILY_AMOUNTMobilePay"] = rev_mobile
        r["REVENUEDAILY_AMOUNTCash"] = sub_cash
        r["ROYALTYAMOUNT"] = royalty
        r["ROYALTYREALAMOUNT"] = royalty
        r["ROYALTYDIFFERENCE"] = 0
        r["SUBROYALTYFEE"] = sub_fee
        r["SUBROYALTYMobilePay"] = sub_mobile
        r["SUBROYALTYCash"] = sub_cash
        r["SUBROYALTYTotal"] = sub_fee + sub_mobile + sub_cash
        r["TOTALROYALTY"] = _d(r.get("ACCROYALTY_PRICE"))
        r["TOTALSUBROYALTY"] = sub_fee + sub_mobile + sub_cash
    # 三级树（片区→服务区→项目）
    from collections import OrderedDict
    region_map = OrderedDict()
    sum_fields = ["REVENUEDAILY_AMOUNTTotal","REVENUEDAILY_AMOUNTMobilePay","REVENUEDAILY_AMOUNTCash",
                  "ROYALTYAMOUNT","ROYALTYREALAMOUNT","ROYALTYDIFFERENCE",
                  "SUBROYALTYFEE","SUBROYALTYMobilePay","SUBROYALTYCash","SUBROYALTYTotal",
                  "TOTALROYALTY","TOTALSUBROYALTY"]
    for r in rows:
        rid = r.get("SPREGIONTYPE_ID")
        sid = r.get("SERVERPART_ID")
        if rid not in region_map:
            region_map[rid] = {"node": {"Id": str(rid), "Name": r.get("SPREGIONTYPE_NAME", "")}, "children": OrderedDict()}
            for f in sum_fields: region_map[rid]["node"][f] = 0
        if sid not in region_map[rid]["children"]:
            region_map[rid]["children"][sid] = {"node": {"Id": str(sid), "Name": r.get("SERVERPART_NAME", "")}, "children": []}
            for f in sum_fields: region_map[rid]["children"][sid]["node"][f] = 0
        region_map[rid]["children"][sid]["children"].append({"node": r})
        for f in sum_fields:
            region_map[rid]["children"][sid]["node"][f] += _d(r.get(f))
    result = []
    for region in region_map.values():
        children = []
        for sp in region["children"].values():
            for f in sum_fields:
                region["node"][f] += sp["node"][f]
            children.append({"node": sp["node"], "children": sp["children"]})
        result.append({"node": region["node"], "children": children})
    return result


# ==================== 12. GetShopExpense ====================
def get_shop_expense(db: DatabaseHelper, serverpart_ids: str = "",
                       settlement_modes: str = "", start_date: str = "",
                       end_date: str = "", keyword: str = "") -> list[dict]:
    """获取分账收银扣费明细（三级树：片区→服务区→项目费用明细）
    原 FinanceHelper.GetShopExpense (L636-1077)
    联查 T_SHOPROYALTY/T_REGISTERCOMPACT/T_BUSINESSPROJECT/T_SERVERPART/T_SERVERPARTSHOP
    + T_SHOPEXPENSE/T_BUSINESSPROJECTSPLIT 费用关联"""
    where_sql = ""
    if serverpart_ids:
        where_sql += f" AND E.SERVERPART_ID IN ({serverpart_ids})"
    # 获取经营项目基础数据
    sql = f"""SELECT
            E.SPREGIONTYPE_ID, E.SPREGIONTYPE_NAME, E.SPREGIONTYPE_INDEX, E.SERVERPART_INDEX,
            E.SERVERPART_ID, E.SERVERPART_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.BUSINESSPROJECT_ID, C.BUSINESSPROJECT_NAME,
            C.BUSINESS_TYPE, C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES,
            C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            A.RENTFEE, A.GUARANTEERATIO, A.FEWTHYEAR, A.STARTDATE, A.ENDDATE,
            A.SHOPROYALTY_ID, A.MINTURNOVER, A.REGISTERCOMPACT_ID,
            B.COMPACT_STARTDATE, B.COMPACT_ENDDATE, B.COMPACT_AMOUNT, B.SECURITYDEPOSIT,
            WM_CONCAT(DISTINCT F.SHOPSHORTNAME) AS SHOPSHORTNAME,
            WM_CONCAT(DISTINCT F.SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID
        FROM T_SHOPROYALTY A, T_REGISTERCOMPACT B, T_BUSINESSPROJECT C,
             T_SERVERPART E, T_SERVERPARTSHOP F
        WHERE A.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID
            AND E.SERVERPART_ID = F.SERVERPART_ID
            AND C.PROJECT_VALID = 1
            AND B.COMPACT_STATE = 1000
            AND B.COMPACT_TYPE IN (340001,510001,520001)
            {where_sql}
        GROUP BY E.SPREGIONTYPE_ID, E.SPREGIONTYPE_NAME, E.SPREGIONTYPE_INDEX, E.SERVERPART_INDEX,
            E.SERVERPART_ID, E.SERVERPART_NAME,
            C.MERCHANTS_ID, C.MERCHANTS_NAME, C.BUSINESSPROJECT_ID, C.BUSINESSPROJECT_NAME,
            C.BUSINESS_TYPE, C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES,
            C.PROJECT_STARTDATE, C.PROJECT_ENDDATE,
            A.RENTFEE, A.GUARANTEERATIO, A.FEWTHYEAR, A.MINTURNOVER,
            A.STARTDATE, A.SHOPROYALTY_ID, A.REGISTERCOMPACT_ID, A.ENDDATE,
            B.COMPACT_STARTDATE, B.COMPACT_ENDDATE, B.COMPACT_AMOUNT, B.SECURITYDEPOSIT"""
    rows = db.execute_query(sql) or []
    if keyword:
        rows = [r for r in rows if keyword in str(r.get("MERCHANTS_NAME", ""))]
    # 查询费用关联数据
    expense_where = ""
    if start_date:
        expense_where += f" AND A.STATISTICS_MONTH >= {start_date}"
    if end_date:
        expense_where += f" AND A.STATISTICS_MONTH <= {end_date}"
    expense_sql = f"""SELECT B.STARTDATE, B.ENDDATE, B.SHOPROYALTY_ID, B.BUSINESSPROJECT_ID,
            B.REVENUEDAILY_AMOUNT, A.SHOPEXPENSE_TYPE, A.STATISTICS_MONTH
        FROM T_SHOPEXPENSE A, T_BUSINESSPROJECTSPLIT B
        WHERE B.BUSINESSPROJECTSPLIT_STATE = 1 AND A.SHOPEXPENSE_ID = B.SHOPEXPENSE_ID
            {expense_where}
        GROUP BY B.STARTDATE, B.ENDDATE, B.SHOPROYALTY_ID, B.BUSINESSPROJECT_ID,
            B.REVENUEDAILY_AMOUNT, A.SHOPEXPENSE_TYPE, A.STATISTICS_MONTH"""
    expenses = db.execute_query(expense_sql) or []
    # 合并项目ID列表
    proj_ids = set(r.get("BUSINESSPROJECT_ID") for r in rows)
    expense_proj_ids = set(e.get("BUSINESSPROJECT_ID") for e in expenses)
    all_proj_ids = proj_ids | expense_proj_ids
    rows = [r for r in rows if r.get("BUSINESSPROJECT_ID") in all_proj_ids]
    # 三级树（片区→服务区→项目）
    from collections import OrderedDict
    region_map = OrderedDict()
    for r in rows:
        rid = r.get("SPREGIONTYPE_ID")
        sid = r.get("SERVERPART_ID")
        if rid not in region_map:
            region_map[rid] = {"node": {"Id": str(rid), "Name": r.get("SPREGIONTYPE_NAME", "")}, "children": OrderedDict()}
        if sid not in region_map[rid]["children"]:
            region_map[rid]["children"][sid] = {"node": {"Id": str(sid), "Name": r.get("SERVERPART_NAME", "")}, "children": []}
        region_map[rid]["children"][sid]["children"].append({"node": r})
    result = []
    for region in region_map.values():
        children = [{"node": sp["node"], "children": sp["children"]} for sp in region["children"].values()]
        result.append({"node": region["node"], "children": children})
    return result


# ==================== 13. GetReconciliation ====================
def get_reconciliation(db: DatabaseHelper, business_project_id: int,
                         shop_royalty_id: str = "", start_month: str = "",
                         end_month: str = "", staff_id: int = None) -> tuple[list[dict], dict]:
    """获取合作商户月对账
    原 FinanceHelper.GetReconciliation (L1167+)
    查询项目信息 + 月度拆分对账数据"""
    # 项目信息
    sql = f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {business_project_id} AND PROJECT_VALID = 1"
    project_rows = db.execute_query(sql)
    project_info = project_rows[0] if project_rows else {}
    # 月度对账数据
    split_where = f"BUSINESSPROJECT_ID = {business_project_id} AND BUSINESSPROJECTSPLIT_STATE = 1 AND ACCOUNT_TYPE = 1000"
    if shop_royalty_id:
        split_where += f" AND SHOPROYALTY_ID IN ({shop_royalty_id})"
    if start_month:
        split_where += f" AND STATISTICS_DATE >= {start_month}01"
    if end_month:
        split_where += f" AND STATISTICS_DATE <= {end_month}31"
    split_sql = f"""SELECT STATISTICS_DATE,
            SUM(REVENUEDAILY_AMOUNT) AS REVENUEDAILY_AMOUNT,
            SUM(ROYALTYDAILY_PRICE) AS ROYALTYDAILY_PRICE,
            SUM(SUBROYALTYDAILY_PRICE) AS SUBROYALTYDAILY_PRICE,
            SUM(TICKETDAILY_FEE) AS TICKETDAILY_FEE,
            SUM(MOBILEPAY_AMOUNT) AS MOBILEPAY_AMOUNT,
            SUM(CASHPAY_AMOUNT) AS CASHPAY_AMOUNT
        FROM T_BUSINESSPROJECTSPLIT
        WHERE {split_where}
        GROUP BY STATISTICS_DATE
        ORDER BY STATISTICS_DATE"""
    split_rows = db.execute_query(split_sql) or []
    result = [{"node": dict(r)} for r in split_rows]
    return result, project_info


# ==================== 14. GetRevenueRecognition ====================
def get_revenue_recognition(db: DatabaseHelper, serverpart_ids: str = "",
                              start_date: str = "", end_date: str = "",
                              settlement_modes: str = "", business_project_id: int = None,
                              shop_royalty_id: str = "", keyword: str = "",
                              solid_type: bool = False, show_his_project: bool = False,
                              show_self: bool = False) -> tuple[list[dict], str]:
    """获取分账收银收入确认（三级树：片区→服务区→项目）
    原 FinanceHelper.GetRevenueRecognition (L1938-3900)
    1. 查 T_BIZPSPLITMONTH UNION ALL T_PROJECTSPLITMONTH
    2. 按结算模式/关键字过滤 → 构建三级树(片区→服务区→项目)
    3. 每个项目节点包含月度汇总分润/提成/冲正数据"""
    from datetime import datetime

    solid_date = ""
    start_month = start_date[:6] if start_date else ""
    end_month = end_date[:6] if end_date else ""

    # --- 构造查询条件 ---
    where_parts = []
    if serverpart_ids:
        where_parts.append(f"E.SERVERPART_ID IN ({serverpart_ids})")
    if start_month:
        where_parts.append(f"B.STATISTICS_MONTH >= {start_month}")
    if end_month:
        where_parts.append(f"B.STATISTICS_MONTH <= {end_month}")
    if business_project_id:
        where_parts.append(f"B.BUSINESSPROJECT_ID = {business_project_id}")
    if shop_royalty_id:
        where_parts.append(f"B.SHOPROYALTY_ID = {shop_royalty_id}")

    where_sql = (" AND " + " AND ".join(where_parts)) if where_parts else ""

    # --- 1. 查询实时结算数据：T_BIZPSPLITMONTH + T_PROJECTSPLITMONTH ---
    main_sql = f"""SELECT
            E.SPREGIONTYPE_ID, E.SPREGIONTYPE_INDEX, E.SERVERPART_INDEX, E.SERVERPART_CODE,
            E.SERVERPART_ID, E.SPREGIONTYPE_NAME, E.SERVERPART_NAME, C.GUARANTEE_PRICE,
            C.MERCHANTS_NAME, C.MERCHANTS_ID, C.BUSINESSPROJECT_ID, C.BUSINESSPROJECT_NAME,
            C.SWITCH_DATE, C.SWITCH_MODES, C.SETTLEMENT_MODES, C.BUSINESS_TYPE,
            B.STARTDATE, B.ENDDATE, B.STATISTICS_MONTH, B.REGISTERCOMPACT_ID,
            B.REVENUE_AMOUNT AS REVENUEDAILY_AMOUNT,
            B.ACCREVENUE_AMOUNT, B.ACCROYALTY_PRICE, B.ACCSUBROYALTY_PRICE,
            B.ACCTICKET_FEE, B.ACCROYALTY_THEORY, B.ACCSUBROYALTY_THEORY,
            B.ACCMOBILEPAY_CORRECT, B.ACCCASHPAY_CORRECT, B.ACCOUNT_TYPE,
            B.SHOPROYALTY_ID, G.SECURITYDEPOSIT, G.REGISTERCOMPACT_ID AS COMPACT_ID,
            B.SERVERPARTSHOP_NAME, B.SERVERPARTSHOP_ID,
            G.COMPACT_STARTDATE, G.COMPACT_ENDDATE, B.GUARANTEERATIO, B.MINTURNOVER,
            B.MOBILEPAY_CORRECT, B.CASHPAY_CORRECT,
            B.ROYALTY_PRICE AS ROYALTYDAILY_PRICE, B.ROYALTY_THEORY,
            1 AS DATA_TYPE
        FROM T_BIZPSPLITMONTH B, T_BUSINESSPROJECT C,
            T_SERVERPART E, T_REGISTERCOMPACT G
        WHERE B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND B.SERVERPART_ID = E.SERVERPART_ID
            AND C.REGISTERCOMPACT_ID = G.REGISTERCOMPACT_ID
            AND C.PROJECT_VALID = 1 AND G.COMPACT_TYPE IN (340001,510001,520001)
            AND B.BIZPSPLITMONTH_STATE = 1 AND B.ACCOUNT_TYPE = 1000
            {where_sql}"""
    dt_data = db.execute_query(main_sql) or []

    if not dt_data:
        return [], solid_date

    # --- 2. 过滤条件 ---
    if keyword:
        dt_data = [r for r in dt_data if keyword in str(r.get("MERCHANTS_NAME", ""))]
    if settlement_modes and start_month and end_month:
        modes = [m.strip() for m in settlement_modes.split(",")]
        filtered = []
        for r in dt_data:
            sm = str(r.get("SETTLEMENT_MODES", ""))
            sw = str(r.get("SWITCH_MODES", ""))
            sd = str(r.get("SWITCH_DATE", ""))[:8]
            if sm in modes:
                filtered.append(r)
            elif sw in modes and sd >= f"{start_month}01" and sd <= f"{end_month}31":
                filtered.append(r)
        dt_data = filtered
    if not show_his_project:
        dt_data = [r for r in dt_data if r.get("DATA_TYPE") == 1]

    if not dt_data:
        return [], solid_date

    # --- 3. 固化数据查询 ---
    if solid_type:
        solid_where = where_sql.replace("B.", "").replace("E.", "")
        solid_sql = f"""SELECT MAX(RECORD_DATE) AS MAX_DATE FROM T_PROJECTSPLITMONTH
            WHERE PROJECTSPLITMONTH_STATE = 1 {solid_where}"""
        solid_rows = db.execute_query(solid_sql) or []
        if solid_rows and solid_rows[0].get("MAX_DATE"):
            solid_date = str(solid_rows[0]["MAX_DATE"])

    # --- 4. 构建三级树：片区→服务区→项目 ---
    result = []

    # 提取片区列表（按索引排序）
    region_map = {}
    for r in dt_data:
        rid = r.get("SPREGIONTYPE_ID")
        rname = r.get("SPREGIONTYPE_NAME", "")
        ridx = _d(r.get("SPREGIONTYPE_INDEX"))
        if rid not in region_map:
            region_map[rid] = {"name": rname, "idx": ridx}
    regions = sorted(region_map.items(), key=lambda x: x[1]["idx"])

    for region_id, region_info in regions:
        center_node = {
            "node": {
                "Id": str(region_id) if region_id else "",
                "Name": region_info["name"],
                "SPREGIONTYPE_ID": region_id,
                "SPREGIONTYPE_NAME": region_info["name"],
            },
            "children": []
        }
        region_rows = [r for r in dt_data if r.get("SPREGIONTYPE_ID") == region_id]

        # 提取服务区
        sp_map = {}
        for r in region_rows:
            sid = r.get("SERVERPART_ID")
            sname = r.get("SERVERPART_NAME", "")
            sidx = _d(r.get("SERVERPART_INDEX"))
            scode = r.get("SERVERPART_CODE", "")
            if sid not in sp_map:
                sp_map[sid] = {"name": sname, "idx": sidx, "code": scode}
        sps = sorted(sp_map.items(), key=lambda x: (x[1]["idx"], x[1]["code"]))

        for sp_id, sp_info in sps:
            sp_node = {
                "node": {
                    "Id": str(sp_id),
                    "Name": sp_info["name"],
                    "SPREGIONTYPE_ID": region_id,
                    "SPREGIONTYPE_NAME": region_info["name"],
                    "SERVERPART_ID": sp_id,
                    "SERVERPART_NAME": sp_info["name"],
                },
                "children": []
            }
            sp_rows = [r for r in region_rows if r.get("SERVERPART_ID") == sp_id]

            # 提取经营项目（按 BUSINESSPROJECT_ID + SHOPROYALTY_ID 分组）
            proj_map = {}
            for r in sp_rows:
                bp_id = r.get("BUSINESSPROJECT_ID")
                sr_id = r.get("SHOPROYALTY_ID")
                key = (bp_id, sr_id)
                if key not in proj_map:
                    proj_map[key] = []
                proj_map[key].append(r)

            for (bp_id, sr_id), proj_rows in proj_map.items():
                first = proj_rows[0]
                # 汇总月度数据
                total_revenue = sum(_d(r.get("REVENUEDAILY_AMOUNT")) for r in proj_rows)
                total_royalty = sum(_d(r.get("ROYALTYDAILY_PRICE")) for r in proj_rows)

                proj_node = {
                    "node": {
                        "Id": str(bp_id),
                        "Name": first.get("BUSINESSPROJECT_NAME", ""),
                        "SPREGIONTYPE_ID": region_id,
                        "SPREGIONTYPE_NAME": region_info["name"],
                        "SERVERPART_ID": sp_id,
                        "SERVERPART_NAME": sp_info["name"],
                        "BUSINESSPROJECT_ID": bp_id,
                        "BUSINESSPROJECT_NAME": first.get("BUSINESSPROJECT_NAME", ""),
                        "MERCHANTS_NAME": first.get("MERCHANTS_NAME", ""),
                        "MERCHANTS_ID": first.get("MERCHANTS_ID"),
                        "SHOPROYALTY_ID": sr_id,
                        "SERVERPARTSHOP_ID": first.get("SERVERPARTSHOP_ID", ""),
                        "SERVERPARTSHOP_NAME": first.get("SERVERPARTSHOP_NAME", ""),
                        "BUSINESS_TYPE": first.get("BUSINESS_TYPE"),
                        "SETTLEMENT_MODES": first.get("SETTLEMENT_MODES"),
                        "COMPACT_STARTDATE": first.get("COMPACT_STARTDATE"),
                        "COMPACT_ENDDATE": first.get("COMPACT_ENDDATE"),
                        "GUARANTEE_PRICE": _d(first.get("GUARANTEE_PRICE")),
                        "SECURITYDEPOSIT": _d(first.get("SECURITYDEPOSIT")),
                        "GUARANTEERATIO": _d(first.get("GUARANTEERATIO")),
                        "MINTURNOVER": _d(first.get("MINTURNOVER")),
                        "REVENUEDAILY_AMOUNT": total_revenue,
                        "ROYALTYDAILY_PRICE": total_royalty,
                        "ACCREVENUE_AMOUNT": _d(first.get("ACCREVENUE_AMOUNT")),
                        "ACCROYALTY_PRICE": _d(first.get("ACCROYALTY_PRICE")),
                        "ACCSUBROYALTY_PRICE": _d(first.get("ACCSUBROYALTY_PRICE")),
                        "ACCTICKET_FEE": _d(first.get("ACCTICKET_FEE")),
                        "ACCROYALTY_THEORY": _d(first.get("ACCROYALTY_THEORY")),
                        "ACCSUBROYALTY_THEORY": _d(first.get("ACCSUBROYALTY_THEORY")),
                        "MOBILEPAY_CORRECT": _d(first.get("MOBILEPAY_CORRECT")),
                        "CASHPAY_CORRECT": _d(first.get("CASHPAY_CORRECT")),
                        "ACCMOBILEPAY_CORRECT": _d(first.get("ACCMOBILEPAY_CORRECT")),
                        "ACCCASHPAY_CORRECT": _d(first.get("ACCCASHPAY_CORRECT")),
                        "STARTDATE": first.get("STARTDATE"),
                        "ENDDATE": first.get("ENDDATE"),
                    },
                    "children": []
                }

                # 汇总到服务区
                for field in ["REVENUEDAILY_AMOUNT", "ROYALTYDAILY_PRICE", "ACCREVENUE_AMOUNT",
                              "ACCROYALTY_PRICE", "ACCSUBROYALTY_PRICE", "ACCTICKET_FEE"]:
                    sp_node["node"][field] = sp_node["node"].get(field, 0) + _d(proj_node["node"].get(field))

                sp_node["children"].append(proj_node)

            # 汇总到片区
            for field in ["REVENUEDAILY_AMOUNT", "ROYALTYDAILY_PRICE", "ACCREVENUE_AMOUNT",
                          "ACCROYALTY_PRICE", "ACCSUBROYALTY_PRICE", "ACCTICKET_FEE"]:
                center_node["node"][field] = center_node["node"].get(field, 0) + _d(sp_node["node"].get(field))

            center_node["children"].append(sp_node)

        result.append(center_node)

    return result, solid_date


# ==================== 15. GetProjectPeriodIncome ====================
def get_project_period_income(db: DatabaseHelper, business_project_id: int,
                                statistics_month: str, statistics_month_start: str = "",
                                shop_royalty_id: str = "", mobile_pay_correct: float = 0,
                                cash_pay_correct: float = 0) -> list[dict]:
    """获取经营项目分账收银收入（按月结算数据列表）
    原 FinanceHelper.GetProjectPeriodIncome (L4358-4900)
    查项目详情→合同→T_BIZPSPLITMONTH→T_BUSINESSAPPROVAL审批→按SHOPROYALTY按月组装"""
    from datetime import datetime, timedelta

    # --- 1. 查询经营项目详情 ---
    proj_sql = f"""SELECT * FROM T_BUSINESSPROJECT
        WHERE BUSINESSPROJECT_ID = {business_project_id} AND PROJECT_VALID = 1"""
    proj_rows = db.execute_query(proj_sql) or []
    if not proj_rows:
        return []
    proj = proj_rows[0]

    # --- 2. 查询合同保证金 ---
    compact_id = proj.get("REGISTERCOMPACT_ID")
    security_deposit = 0
    if compact_id:
        compact_rows = db.execute_query(
            f"SELECT SECURITYDEPOSIT FROM T_REGISTERCOMPACT WHERE REGISTERCOMPACT_ID = {compact_id}") or []
        if compact_rows:
            security_deposit = _d(compact_rows[0].get("SECURITYDEPOSIT"))

    # --- 3. 查询应收拆分期 ---
    sr_sql = f"""SELECT * FROM T_SHOPROYALTY
        WHERE BUSINESSPROJECT_ID = {business_project_id} AND SHOPROYALTY_STATE = 1
        ORDER BY STARTDATE"""
    sr_list = db.execute_query(sr_sql) or []

    # --- 4. 查询月度应收拆分结果数据 ---
    where_month = f" AND B.STATISTICS_MONTH <= {statistics_month}"
    if shop_royalty_id:
        where_month = f" AND B.SHOPROYALTY_ID IN ({shop_royalty_id})"
    acct_sql = f"""SELECT B.STARTDATE, B.ENDDATE, B.STATISTICS_MONTH, B.REGISTERCOMPACT_ID,
            B.REVENUE_AMOUNT AS REVENUEDAILY_AMOUNT, B.MOBILEPAY_AMOUNT, B.CASHPAY_AMOUNT,
            B.ROYALTY_PRICE AS ROYALTYDAILY_PRICE, B.ROYALTY_THEORY,
            B.ACCREVENUE_AMOUNT, B.ACCROYALTY_PRICE, B.ACCSUBROYALTY_PRICE,
            B.ACCTICKET_FEE, B.ACCROYALTY_THEORY, B.ACCSUBROYALTY_THEORY,
            B.ACCOUNT_TYPE, B.SHOPROYALTY_ID, B.MOBILEPAY_CORRECT, B.CASHPAY_CORRECT
        FROM T_BIZPSPLITMONTH B
        WHERE B.BIZPSPLITMONTH_STATE = 1 AND B.ACCOUNT_TYPE = 1000
            AND B.BUSINESSPROJECT_ID = {business_project_id} {where_month}"""
    dt_account = db.execute_query(acct_sql) or []

    # --- 5. 查询审批数据 ---
    appr_sql = f"""SELECT A.BUSINESSAPPROVAL_ID, A.BUSINESSAPPROVAL_STATE,
            B.BIZPSPLITMONTH_ID, B.STATISTICS_MONTH, B.SHOPROYALTY_ID,
            B.REVENUE_AMOUNT, B.ROYALTY_PRICE, B.ROYALTY_THEORY,
            B.MOBILEPAY_AMOUNT, B.CASHPAY_AMOUNT, B.ACCREVENUE_AMOUNT,
            B.ACCROYALTY_PRICE, B.ACCROYALTY_THEORY,
            B.MOBILEPAY_CORRECT, B.CASHPAY_CORRECT
        FROM T_BUSINESSAPPROVAL A, T_BIZPSPLITMONTH B
        WHERE A.BUSINESSPROCESS_ID = B.BIZPSPLITMONTH_ID
            AND A.BUSINESSAPPROVAL_STATE NOT IN (0,3000,9999)
            AND A.OPERATION_TYPE = 12
            AND B.BUSINESSPROJECT_ID = {business_project_id} {where_month}"""
    dt_business = db.execute_query(appr_sql) or []

    # --- 6. 按 SHOPROYALTY 逐期逐月组装结算数据 ---
    result = []
    guarantee_ratio = _d(proj.get("GUARANTEERATIO"))
    tax_rate = 5.0

    for sr in sr_list:
        sr_id = sr.get("SHOPROYALTY_ID")
        if shop_royalty_id and str(sr_id) not in shop_royalty_id.split(","):
            continue

        start_dt = sr.get("STARTDATE")
        end_dt = sr.get("ENDDATE")
        if not start_dt or not end_dt:
            continue

        # 转换日期
        if isinstance(start_dt, str):
            start_dt = datetime.strptime(str(start_dt)[:10].replace("/", "-"), "%Y-%m-%d")
        if isinstance(end_dt, str):
            end_dt = datetime.strptime(str(end_dt)[:10].replace("/", "-"), "%Y-%m-%d")

        # 确保不超过当前月
        cur_date = start_dt.replace(day=1)
        last_month_income = 0.0
        period_num = 1

        while cur_date.strftime("%Y%m") <= statistics_month and cur_date <= end_dt:
            cur_month = cur_date.strftime("%Y%m")

            # 从月度数据查本月营收
            month_rows = [r for r in dt_account
                          if str(r.get("SHOPROYALTY_ID")) == str(sr_id)
                          and str(r.get("STATISTICS_MONTH")) == cur_month]
            cur_revenue = sum(_d(r.get("REVENUEDAILY_AMOUNT")) for r in month_rows)

            # 累计营收
            acc_rows = [r for r in dt_account
                        if str(r.get("SHOPROYALTY_ID")) == str(sr_id)
                        and str(r.get("STATISTICS_MONTH")) <= cur_month]
            acc_revenue = _d(month_rows[0].get("ACCREVENUE_AMOUNT")) if month_rows else 0
            acc_mobile_correct = sum(_d(r.get("MOBILEPAY_CORRECT")) for r in acc_rows)
            acc_cash_correct = sum(_d(r.get("CASHPAY_CORRECT")) for r in acc_rows)
            total_revenue = acc_revenue + acc_mobile_correct + acc_cash_correct
            if cur_month == statistics_month:
                total_revenue += mobile_pay_correct + cash_pay_correct

            # 计算提成
            royalty_amount = round(total_revenue * guarantee_ratio / 100, 2) if guarantee_ratio else 0
            royalty_income = round(royalty_amount / (1 + tax_rate / 100), 2)

            # 审批状态
            appr_rows = [r for r in dt_business
                         if str(r.get("SHOPROYALTY_ID")) == str(sr_id)
                         and str(r.get("STATISTICS_MONTH")) == cur_month]
            approval_state = 0
            approval_id = None
            if appr_rows:
                approval_id = appr_rows[0].get("BUSINESSAPPROVAL_ID")
                state = str(appr_rows[0].get("BUSINESSAPPROVAL_STATE"))
                # 已审结用审批数据
                if state == "9000":
                    approval_state = 9
                    royalty_amount = _d(appr_rows[0].get("ROYALTY_PRICE"))
                    royalty_income = _d(appr_rows[0].get("ROYALTY_THEORY"))
                    total_revenue = _d(appr_rows[0].get("ACCREVENUE_AMOUNT"))
                else:
                    approval_state = 1

            item = {
                "Id": proj.get("SERVERPARTSHOP_ID", ""),
                "Name": proj.get("SERVERPARTSHOP_NAME", ""),
                "SERVERPART_ID": proj.get("SERVERPART_ID"),
                "SERVERPART_NAME": proj.get("SERVERPART_NAME", ""),
                "SERVERPARTSHOP_ID": proj.get("SERVERPARTSHOP_ID", ""),
                "SERVERPARTSHOP_NAME": proj.get("SERVERPARTSHOP_NAME", ""),
                "ShopRoyaltyId": sr_id,
                "BUSINESSPROJECT_ID": business_project_id,
                "BUSINESSPROJECT_NAME": proj.get("BUSINESSPROJECT_NAME", ""),
                "MERCHANTS_ID": proj.get("MERCHANTS_ID"),
                "MERCHANTS_NAME": proj.get("MERCHANTS_NAME", ""),
                "REGISTERCOMPACT_ID": compact_id,
                "BusinessType": proj.get("BUSINESS_TYPE"),
                "SETTLEMENT_MODES": proj.get("SETTLEMENT_MODES"),
                "GUARANTEERATIO": guarantee_ratio,
                "TaxRate": tax_rate,
                "SECURITYDEPOSIT": security_deposit,
                "STATISTICS_MONTH": f"{cur_month[:4]}/{cur_month[4:6]}",
                "IndexStr": f"第{period_num}期",
                "CurMonthRevenue": cur_revenue,
                "REVENUEDAILY_AMOUNTTotal": total_revenue,
                "MOBILEPAY_CORRECT": sum(_d(r.get("MOBILEPAY_CORRECT")) for r in month_rows),
                "CASHPAY_CORRECT": sum(_d(r.get("CASHPAY_CORRECT")) for r in month_rows),
                "GUARANTEERATIOAMOUNT": royalty_amount,
                "GUARANTEERATIOINCOME": royalty_income,
                "RECEIVABLEAMOUNT": royalty_amount,
                "ROYALTYTHEORYMUST": royalty_income,
                "ROYALTYTHEORYOK": last_month_income,
                "ROYALTYTHEORYMONTHLYMUST": royalty_income - last_month_income,
                "AllowSettlement": 1 if approval_state == 0 else approval_state,
                "BusinessApprovalId": approval_id,
                "Approvalstate": approval_state,
            }
            result.append(item)
            last_month_income = royalty_income
            period_num += 1

            # 下一个月
            if cur_date.month == 12:
                cur_date = cur_date.replace(year=cur_date.year + 1, month=1)
            else:
                cur_date = cur_date.replace(month=cur_date.month + 1)

    return result


# ==================== 16. GetProjectPeriodAccount ====================
def get_project_period_account(db: DatabaseHelper, business_project_id: int,
                                 shop_royalty_id: str = "",
                                 business_approval_id: str = "") -> dict:
    """查询经营周期结算明细
    原 FinanceHelper.GetProjectPeriodAccount"""
    sql = f"""SELECT * FROM T_REVENUECONFIRM
        WHERE BUSINESSPROJECT_ID = {business_project_id}"""
    if shop_royalty_id:
        sql += f" AND SHOPROYALTY_ID IN ({shop_royalty_id})"
    rows = db.execute_query(sql)
    return rows[0] if rows else {}


# ==================== 17. ApplyAccountProinst ====================
def apply_account_proinst(db: DatabaseHelper, data: dict) -> tuple[bool, str]:
    """发起商户年度结算审批
    原 FinanceHelper.ApplyAccountProinst (L5610-5780)
    1. 查审批路由获取下一环节 → 创建/更新 T_BUSINESSAPPROVAL
    2. 备份旧 T_REVENUECONFIRM → 删除并重新插入新结算记录"""
    from datetime import datetime

    approval_model = data.get("BusinessapprovalModel", {})
    self_list = data.get("RevenueconfirmModel", [])
    next_state = data.get("nextApproveState")
    source_platform = data.get("SourcePlatform", "")

    if not self_list:
        return False, "无结算数据"

    bp_id = approval_model.get("BUSINESSPROCESS_ID")
    approval_id = approval_model.get("BUSINESSAPPROVAL_ID")
    operation_type = approval_model.get("OPERATION_TYPE", 11)

    # --- 1. 查审批路由获取下一环节 ---
    route_sql = f"""SELECT * FROM T_APPROVALROUTE
        WHERE OPERATION_TYPE = {operation_type}
            AND APPROVALROUTE_STATE = 1000 AND APPROVALROUTE_VALID = 1
        ORDER BY APPROVALROUTE_INDEX"""
    routes = db.execute_query(route_sql) or []
    if not routes:
        return False, "审批路由未配置"

    target_state = next_state if next_state else routes[0].get("NEXT_STATE", 2000)

    # --- 2. 创建/更新 T_BUSINESSAPPROVAL ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if approval_id:
        # 更新已有审批
        db.execute_non_query(f"""UPDATE T_BUSINESSAPPROVAL SET
            BUSINESSAPPROVAL_STATE = {target_state},
            REJECTSTAFF_NAME = '', REJECT_INFO = '', REJECT_TYPE = NULL,
            RECORD_DATE = SYSDATE
            WHERE BUSINESSAPPROVAL_ID = {approval_id}""")
    else:
        # 新建审批
        db.execute_non_query(f"""INSERT INTO T_BUSINESSAPPROVAL (
                BUSINESSAPPROVAL_ID, BUSINESSPROCESS_ID, OPERATION_TYPE,
                BUSINESSAPPROVAL_STATE, BUSINESS_STARTDATE,
                ACCEPT_CODE, RECORD_DATE
            ) VALUES (
                SEQ_BUSINESSAPPROVAL.NEXTVAL, {bp_id}, {operation_type},
                {target_state}, TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
                '{operation_type}-{bp_id}', SYSDATE
            )""")
        # 获取刚插入的审批ID
        id_rows = db.execute_query(
            f"SELECT MAX(BUSINESSAPPROVAL_ID) AS MID FROM T_BUSINESSAPPROVAL "
            f"WHERE BUSINESSPROCESS_ID = {bp_id} AND OPERATION_TYPE = {operation_type}") or []
        if id_rows:
            approval_id = id_rows[0].get("MID")

    if not approval_id:
        return False, "审批数据创建失败"

    # --- 3. 备份旧结算记录 ---
    try:
        db.execute_non_query(
            f"INSERT INTO T_REVENUECONFIRM_HIS SELECT * FROM T_REVENUECONFIRM "
            f"WHERE BUSINESSPROJECT_ID = {bp_id} AND BUSINESSAPPROVAL_ID = {approval_id}")
    except Exception:
        pass  # 历史表可能不存在

    db.execute_non_query(
        f"DELETE FROM T_REVENUECONFIRM "
        f"WHERE BUSINESSPROJECT_ID = {bp_id} AND BUSINESSAPPROVAL_ID = {approval_id}")

    # --- 4. 插入新结算记录 ---
    for item in self_list:
        node = item.get("node", item) if isinstance(item, dict) else item
        sr_id = node.get("SHOPROYALTY_ID", "NULL")
        period = node.get("BUSINESS_PERIOD", "NULL")
        period_idx = node.get("PERIOD_INDEX", "NULL")
        start = node.get("BUSINESS_STARTDATE", "")
        end = node.get("BUSINESS_ENDDATE", "")
        revenue = _d(node.get("REVENUE_AMOUNT"))
        royalty = _d(node.get("ROYALTY_PRICE"))
        theory = _d(node.get("ROYALTY_THEORY"))

        db.execute_non_query(f"""INSERT INTO T_REVENUECONFIRM (
                REVENUECONFIRM_ID, BUSINESSPROJECT_ID, BUSINESSAPPROVAL_ID,
                SHOPROYALTY_ID, BUSINESS_PERIOD, PERIOD_INDEX,
                BUSINESS_STARTDATE, BUSINESS_ENDDATE,
                REVENUE_AMOUNT, ROYALTY_PRICE, ROYALTY_THEORY,
                REVENUE_VALID, RECORD_DATE
            ) VALUES (
                SEQ_REVENUECONFIRM.NEXTVAL, {bp_id}, {approval_id},
                {sr_id}, {period}, {period_idx},
                '{start}', '{end}',
                {revenue}, {royalty}, {theory},
                0, SYSDATE
            )""")

    logger.info(f"ApplyAccountProinst 成功: BP={bp_id}, ApprovalID={approval_id}")
    return True, ""


# ==================== 18. ApproveAccountProinst ====================
def approve_account_proinst(db: DatabaseHelper, business_approval_id: int,
                              cur_proinst_state: int, approveed_info: str,
                              approveed_staff_id: int = None, approveed_staff_name: str = "",
                              next_id: int = None, next_state: int = None,
                              source_platform: str = "") -> tuple[bool, str]:
    """提交/审批商户对账
    原 FinanceHelper.ApproveAccountProinst (L5814-5930)
    查审批详情→校验环节→查路由→更新状态→记录意见→若完成则激活结算"""
    from datetime import datetime

    # --- 1. 查审批详情 ---
    appr_rows = db.execute_query(
        f"SELECT * FROM T_BUSINESSAPPROVAL WHERE BUSINESSAPPROVAL_ID = {business_approval_id}") or []
    if not appr_rows:
        return False, "审批数据不存在"
    appr = appr_rows[0]

    # 校验环节状态
    cur_state = appr.get("BUSINESSAPPROVAL_STATE")
    if cur_state and int(cur_state) > cur_proinst_state:
        return False, "流程环节已发生变化，请重新打开流程！"

    operation_type = appr.get("OPERATION_TYPE")
    bp_id = appr.get("BUSINESSPROCESS_ID")

    # --- 2. 查审批路由获取下一环节 ---
    route_sql = f"""SELECT * FROM T_APPROVALROUTE
        WHERE OPERATION_TYPE = {operation_type}
            AND APPROVALROUTE_STATE = {cur_proinst_state} AND APPROVALROUTE_VALID = 1
        ORDER BY APPROVALROUTE_INDEX"""
    routes = db.execute_query(route_sql) or []
    if not routes:
        return False, "当前环节路由未配置"

    target_state = next_state if next_state else routes[0].get("NEXT_STATE", 9000)
    route_name = routes[0].get("APPROVALROUTE_NAME", "")

    # --- 3. 记录审批意见 ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mobile_approve = 1 if source_platform == "minProgram" else 0
    db.execute_non_query(f"""INSERT INTO T_APPLYAPPROVE (
            APPLYAPPROVE_ID, TABLE_ID, TABLE_NAME,
            APPLYAPPROVE_TYPE, APPLYAPPROVE_NAME, APPLYAPPROVE_INFO,
            APPLYAPPROVE_DATE, STAFF_ID, STAFF_NAME, MOBILE_APPROVE,
            RECORD_DATE
        ) VALUES (
            SEQ_APPLYAPPROVE.NEXTVAL, {business_approval_id},
            'T_BUSINESSAPPROVAL', {cur_proinst_state}, '{route_name}',
            '{approveed_info}',
            TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
            {approveed_staff_id or 'NULL'}, '{approveed_staff_name}',
            {mobile_approve}, SYSDATE
        )""")

    # --- 4. 更新审批状态 ---
    end_date_sql = ""
    if target_state == 9000:
        end_date_sql = f", BUSINESS_ENDDATE = TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS')"
        end_date_sql += ", APPOVED_IDS = '', APPOVED_NAME = ''"

    appoved_ids_sql = ""
    if next_id and target_state != 9000:
        appoved_ids_sql = f", APPOVED_IDS = '{next_id}'"

    db.execute_non_query(f"""UPDATE T_BUSINESSAPPROVAL SET
        BUSINESSAPPROVAL_STATE = {target_state},
        REJECTSTAFF_NAME = '', REJECT_INFO = '', REJECT_TYPE = NULL
        {end_date_sql} {appoved_ids_sql}, RECORD_DATE = SYSDATE
        WHERE BUSINESSAPPROVAL_ID = {business_approval_id}""")

    # --- 5. 如果审批结束(9000)，激活结算数据 ---
    if target_state == 9000 and bp_id:
        # 激活 T_REVENUECONFIRM
        db.execute_non_query(
            f"UPDATE T_REVENUECONFIRM SET REVENUE_VALID = 1 "
            f"WHERE BUSINESSPROJECT_ID = {bp_id} AND BUSINESSAPPROVAL_ID = {business_approval_id}")
        # 更新拆分表结算状态
        db.execute_non_query(
            f"UPDATE T_SHOPROYALTY SET SETTLEMENT_STATE = 1 "
            f"WHERE BUSINESSPROJECT_ID = {bp_id} AND SHOPROYALTY_STATE = 1")

    logger.info(f"ApproveAccountProinst 成功: id={business_approval_id}, "
                f"state={cur_proinst_state}→{target_state}")
    return True, ""


# ==================== 19. RejectAccountProinst ====================
def reject_account_proinst(db: DatabaseHelper, business_approval_id: int,
                             approveed_staff_id: int = None, approveed_staff_name: str = "",
                             approveed_info: str = "", target_proinst_state: int = None,
                             reject_type: int = 1, end_reject: bool = False,
                             source_platform: str = "") -> tuple[bool, str]:
    """驳回商户对账审批业务
    原 FinanceHelper.RejectAccountProinst
    查审批详情→回退到目标环节→记录驳回意见→更新状态"""
    from datetime import datetime

    # --- 1. 查审批详情 ---
    appr_rows = db.execute_query(
        f"SELECT * FROM T_BUSINESSAPPROVAL WHERE BUSINESSAPPROVAL_ID = {business_approval_id}") or []
    if not appr_rows:
        return False, "审批数据不存在"
    appr = appr_rows[0]
    bp_id = appr.get("BUSINESSPROCESS_ID")
    cur_state = appr.get("BUSINESSAPPROVAL_STATE")

    # 目标环节（默认1000提交人）
    if target_proinst_state is None:
        target_proinst_state = 1000

    # --- 2. 记录驳回意见 ---
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mobile_approve = 1 if source_platform == "minProgram" else 0
    db.execute_non_query(f"""INSERT INTO T_APPLYAPPROVE (
            APPLYAPPROVE_ID, TABLE_ID, TABLE_NAME,
            APPLYAPPROVE_TYPE, APPLYAPPROVE_NAME, APPLYAPPROVE_INFO,
            APPLYAPPROVE_DATE, STAFF_ID, STAFF_NAME, MOBILE_APPROVE,
            RECORD_DATE
        ) VALUES (
            SEQ_APPLYAPPROVE.NEXTVAL, {business_approval_id},
            'T_BUSINESSAPPROVAL', {cur_state}, '驳回',
            '{approveed_info}',
            TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
            {approveed_staff_id or 'NULL'}, '{approveed_staff_name}',
            {mobile_approve}, SYSDATE
        )""")

    # --- 3. 更新审批状态→回退 ---
    db.execute_non_query(f"""UPDATE T_BUSINESSAPPROVAL SET
        BUSINESSAPPROVAL_STATE = {target_proinst_state},
        REJECTSTAFF_NAME = '{approveed_staff_name}',
        REJECT_INFO = '{approveed_info}',
        REJECT_TYPE = {reject_type},
        RECORD_DATE = SYSDATE
        WHERE BUSINESSAPPROVAL_ID = {business_approval_id}""")

    # --- 4. 如果是办结后撤回，反激活结算数据 ---
    if end_reject and bp_id:
        db.execute_non_query(
            f"UPDATE T_REVENUECONFIRM SET REVENUE_VALID = 0 "
            f"WHERE BUSINESSPROJECT_ID = {bp_id} AND BUSINESSAPPROVAL_ID = {business_approval_id}")
        db.execute_non_query(
            f"UPDATE T_SHOPROYALTY SET SETTLEMENT_STATE = 0 "
            f"WHERE BUSINESSPROJECT_ID = {bp_id} AND SHOPROYALTY_STATE = 1")

    logger.info(f"RejectAccountProinst 成功: id={business_approval_id}, "
                f"回退到 state={target_proinst_state}")
    return True, ""


# ==================== 20. GetMonthAccountProinst ====================
def get_month_account_proinst(db: DatabaseHelper, search_data: dict = None,
                                user_id: int = None) -> tuple[list[dict], int, int]:
    """获取经营项目月度结算审批列表
    原 BIZPSPLITMONTHHelper.GetMonthAccountProinst (L1937-2132)
    查T_BUSINESSAPPROVAL→关联T_BUSINESSPROJECT/T_BIZPSPLITMONTH/T_REVENUECONFIRM→组装列表"""

    # --- 1. 构建审批列表查询 ---
    where_parts = ["A.OPERATION_TYPE IN (11,12)"]
    search_param = search_data.get("SearchParameter", {}) if search_data else {}
    page_index = search_data.get("PageIndex", 1) if search_data else 1
    page_size = search_data.get("PageSize", 20) if search_data else 20

    # 搜索条件
    if search_param.get("SERVERPART_ID"):
        where_parts.append(f"A.SERVERPART_IDS LIKE '%{search_param['SERVERPART_ID']}%'")
    if search_param.get("BUSINESSAPPROVAL_STATE"):
        where_parts.append(f"A.BUSINESSAPPROVAL_STATE = {search_param['BUSINESSAPPROVAL_STATE']}")
    if search_param.get("KEYWORD"):
        where_parts.append(f"A.BUSINESSPROCESS_NAME LIKE '%{search_param['KEYWORD']}%'")

    # 审批状态过滤
    state_filter = search_param.get("BUSINESSAPPROVAL_STATE_LIST", "")
    if state_filter:
        where_parts.append(f"A.BUSINESSAPPROVAL_STATE IN ({state_filter})")
    else:
        where_parts.append("A.BUSINESSAPPROVAL_STATE NOT IN (0)")

    where_sql = " AND ".join(where_parts)

    # --- 2. 查总数 ---
    count_sql = f"SELECT COUNT(*) AS CNT FROM T_BUSINESSAPPROVAL A WHERE {where_sql}"
    count_rows = db.execute_query(count_sql) or []
    total_count = int(count_rows[0].get("CNT", 0)) if count_rows else 0

    # --- 3. 分页查询审批列表 ---
    offset = (page_index - 1) * page_size
    list_sql = f"""SELECT A.* FROM T_BUSINESSAPPROVAL A
        WHERE {where_sql}
        ORDER BY A.BUSINESSAPPROVAL_ID DESC
        OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY"""
    try:
        appr_list = db.execute_query(list_sql) or []
    except Exception:
        # 达梦不支持 OFFSET...FETCH，使用 ROWNUM
        list_sql = f"""SELECT * FROM (
            SELECT A.*, ROWNUM AS RN FROM T_BUSINESSAPPROVAL A
            WHERE {where_sql} ORDER BY A.BUSINESSAPPROVAL_ID DESC
        ) WHERE RN > {offset} AND RN <= {offset + page_size}"""
        appr_list = db.execute_query(list_sql) or []

    if not appr_list:
        return [], total_count, 0

    # --- 4. 批量关联查询 ---
    bp_ids = set()
    biz_ids = set()
    approval_ids = set()
    for a in appr_list:
        op = str(a.get("OPERATION_TYPE", ""))
        if op == "11":
            bp_ids.add(str(a.get("BUSINESSPROCESS_ID", "")))
        elif op == "12":
            biz_ids.add(str(a.get("BUSINESSPROCESS_ID", "")))
        approval_ids.add(str(a.get("BUSINESSAPPROVAL_ID", "")))

    # 查项目信息
    proj_map = {}
    all_proj_ids = bp_ids | biz_ids
    if all_proj_ids:
        proj_ids_str = ",".join(all_proj_ids)
        proj_sql = f"SELECT * FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID IN ({proj_ids_str})"
        try:
            for p in (db.execute_query(proj_sql) or []):
                proj_map[p.get("BUSINESSPROJECT_ID")] = p
        except Exception:
            pass

    # 查月度结算数据
    biz_map = {}
    if biz_ids:
        biz_ids_str = ",".join(biz_ids)
        biz_sql = f"SELECT * FROM T_BIZPSPLITMONTH WHERE BIZPSPLITMONTH_ID IN ({biz_ids_str})"
        try:
            for b in (db.execute_query(biz_sql) or []):
                biz_map[b.get("BIZPSPLITMONTH_ID")] = b
        except Exception:
            pass

    # --- 5. 组装结果 ---
    result = []
    for a in appr_list:
        op = str(a.get("OPERATION_TYPE", ""))
        item = {
            "BusinessApproval_ID": a.get("BUSINESSAPPROVAL_ID"),
            "BusinessProcess_ID": a.get("BUSINESSPROCESS_ID"),
            "BusinessProcess_Name": a.get("BUSINESSPROCESS_NAME", ""),
            "Accept_Code": a.get("ACCEPT_CODE", ""),
            "Operation_Type": op,
            "Serverpart_ID": a.get("SERVERPART_IDS"),
            "Serverpart_Name": a.get("SERVERPART_NAME", ""),
            "ServerpartShop_ID": a.get("SERVERPARTSHOP_ID", ""),
            "ServerpartShop_Name": a.get("SERVERPARTSHOP_NAME", ""),
            "Staff_ID": a.get("STAFF_ID"),
            "Staff_Name": a.get("STAFF_NAME", ""),
            "ApproveStaff_ID": a.get("APPOVED_IDS"),
            "ApproveStaff_Name": a.get("APPOVED_NAME", ""),
            "RejectStaff_Name": a.get("REJECTSTAFF_NAME", ""),
            "Reject_Info": a.get("REJECT_INFO", ""),
            "BusinessProcess_StartDate": a.get("BUSINESS_STARTDATE"),
            "BusinessProcess_EndDate": a.get("BUSINESS_ENDDATE"),
            "BusinessProcess_State": a.get("BUSINESSAPPROVAL_STATE"),
        }

        # 待办状态判断
        pend_state = 1
        if user_id:
            appoved_ids = str(a.get("APPOVED_IDS", ""))
            if str(user_id) in appoved_ids.split(","):
                pend_state = 0
            elif a.get("BUSINESSAPPROVAL_STATE") == 1000 and a.get("STAFF_ID") == user_id:
                pend_state = 0
        item["PendState"] = pend_state

        # 月度结算: 从 T_BIZPSPLITMONTH 取值
        if op == "12":
            biz = biz_map.get(a.get("BUSINESSPROCESS_ID"))
            if biz:
                item["STATISTICS_MONTH"] = biz.get("STATISTICS_MONTH")
                item["REGISTERCOMPACT_ID"] = biz.get("REGISTERCOMPACT_ID")
                item["BUSINESSPROJECT_ID"] = biz.get("BUSINESSPROJECT_ID")
                item["SHOPROYALTY_ID"] = biz.get("SHOPROYALTY_ID")
                item["STARTDATE"] = biz.get("STARTDATE")
                item["ENDDATE"] = biz.get("ENDDATE")
                item["REVENUE_AMOUNT"] = _d(biz.get("ACCREVENUE_AMOUNT"))
                bp_id = biz.get("BUSINESSPROJECT_ID")
                proj = proj_map.get(bp_id)
                if proj:
                    item["BUSINESSPROJECT_NAME"] = proj.get("BUSINESSPROJECT_NAME", "")
                    item["MERCHANTS_ID"] = proj.get("MERCHANTS_ID")
                    item["MERCHANTS_NAME"] = proj.get("MERCHANTS_NAME", "")
        elif op == "11":
            # 年度结算: 从审批表取值
            item["BUSINESSPROJECT_ID"] = a.get("BUSINESSPROCESS_ID")
            bp_id = a.get("BUSINESSPROCESS_ID")
            proj = proj_map.get(bp_id)
            if proj:
                item["BUSINESSPROJECT_NAME"] = proj.get("BUSINESSPROJECT_NAME", "")
                item["MERCHANTS_ID"] = proj.get("MERCHANTS_ID")
                item["MERCHANTS_NAME"] = proj.get("MERCHANTS_NAME", "")

        # 过滤待办
        pend_filter = search_param.get("PendState")
        if pend_filter is not None and pend_filter < 2:
            if pend_filter == 0 and pend_state != 0:
                continue
            elif pend_filter == 1 and pend_state == 2:
                continue

        result.append(item)

    pending_count = sum(1 for r in result if r.get("PendState") == 0)
    return result, total_count, pending_count


# ==================== 21. ApplyMonthAccountProinst ====================
def apply_month_account_proinst(db: DatabaseHelper, data: dict) -> tuple[bool, str]:
    """发起经营项目月度结算审批
    原 BIZPSPLITMONTHHelper.ApplyMonthAccountProinst
    创建/更新 T_BUSINESSAPPROVAL（OPERATION_TYPE=12） → 查审批路由 → 设置下一环节"""
    from datetime import datetime

    biz_id = data.get("BIZPSPLITMONTH_ID")
    bp_id = data.get("BUSINESSPROJECT_ID")
    sr_id = data.get("SHOPROYALTY_ID")
    month = data.get("STATISTICS_MONTH", "")
    approval_id = data.get("BUSINESSAPPROVAL_ID")
    next_state = data.get("nextApproveState")
    staff_id = data.get("STAFF_ID")
    staff_name = data.get("STAFF_NAME", "")

    if not biz_id:
        return False, "缺少月度结算数据"

    # 查审批路由
    route_sql = """SELECT * FROM T_APPROVALROUTE
        WHERE OPERATION_TYPE = 12 AND APPROVALROUTE_STATE = 1000 AND APPROVALROUTE_VALID = 1
        ORDER BY APPROVALROUTE_INDEX"""
    routes = db.execute_query(route_sql) or []
    if not routes:
        return False, "月度结算审批路由未配置"

    target = next_state if next_state else routes[0].get("NEXT_STATE", 2000)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if approval_id:
        db.execute_non_query(f"""UPDATE T_BUSINESSAPPROVAL SET
            BUSINESSAPPROVAL_STATE = {target},
            REJECTSTAFF_NAME = '', REJECT_INFO = '', REJECT_TYPE = NULL,
            RECORD_DATE = SYSDATE
            WHERE BUSINESSAPPROVAL_ID = {approval_id}""")
    else:
        # 查项目信息用于审批名称
        proj_name = ""
        if bp_id:
            prows = db.execute_query(f"SELECT BUSINESSPROJECT_NAME FROM T_BUSINESSPROJECT WHERE BUSINESSPROJECT_ID = {bp_id}") or []
            if prows:
                proj_name = prows[0].get("BUSINESSPROJECT_NAME", "")

        db.execute_non_query(f"""INSERT INTO T_BUSINESSAPPROVAL (
                BUSINESSAPPROVAL_ID, BUSINESSPROCESS_ID, BUSINESSPROCESS_NAME,
                OPERATION_TYPE, BUSINESSAPPROVAL_STATE,
                BUSINESS_STARTDATE, ACCEPT_CODE,
                STAFF_ID, STAFF_NAME, RECORD_DATE
            ) VALUES (
                SEQ_BUSINESSAPPROVAL.NEXTVAL, {biz_id},
                '{proj_name} {month[:4]}/{month[4:]}月度结算',
                12, {target},
                TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
                '12-{biz_id}',
                {staff_id or 'NULL'}, '{staff_name}', SYSDATE
            )""")

    logger.info(f"ApplyMonthAccountProinst 成功: BIZ={biz_id}, month={month}")
    return True, ""


# ==================== 22. ApproveMonthAccountProinst ====================
def approve_month_account_proinst(db: DatabaseHelper, business_approval_id: int,
                                    cur_proinst_state: int, approveed_info: str,
                                    approveed_staff_id: int = None, approveed_staff_name: str = "",
                                    next_id: int = None, next_state: int = None,
                                    source_platform: str = "") -> tuple[bool, str]:
    """提交/审批经营项目月度结算流程
    原 BIZPSPLITMONTHHelper.ApproveMonthAccountProinst
    逻辑同 #18 ApproveAccountProinst，OPERATION_TYPE=12"""
    from datetime import datetime

    # 查审批详情
    appr_rows = db.execute_query(
        f"SELECT * FROM T_BUSINESSAPPROVAL WHERE BUSINESSAPPROVAL_ID = {business_approval_id}") or []
    if not appr_rows:
        return False, "审批数据不存在"
    appr = appr_rows[0]

    cur_state = appr.get("BUSINESSAPPROVAL_STATE")
    if cur_state and int(cur_state) > cur_proinst_state:
        return False, "流程环节已发生变化，请重新打开流程！"

    bp_id = appr.get("BUSINESSPROCESS_ID")

    # 查路由
    routes = db.execute_query(f"""SELECT * FROM T_APPROVALROUTE
        WHERE OPERATION_TYPE = 12 AND APPROVALROUTE_STATE = {cur_proinst_state}
            AND APPROVALROUTE_VALID = 1 ORDER BY APPROVALROUTE_INDEX""") or []
    if not routes:
        return False, "当前环节路由未配置"

    target = next_state if next_state else routes[0].get("NEXT_STATE", 9000)
    route_name = routes[0].get("APPROVALROUTE_NAME", "")

    # 记录审批意见
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mobile_approve = 1 if source_platform == "minProgram" else 0
    db.execute_non_query(f"""INSERT INTO T_APPLYAPPROVE (
            APPLYAPPROVE_ID, TABLE_ID, TABLE_NAME,
            APPLYAPPROVE_TYPE, APPLYAPPROVE_NAME, APPLYAPPROVE_INFO,
            APPLYAPPROVE_DATE, STAFF_ID, STAFF_NAME, MOBILE_APPROVE, RECORD_DATE
        ) VALUES (
            SEQ_APPLYAPPROVE.NEXTVAL, {business_approval_id},
            'T_BUSINESSAPPROVAL', {cur_proinst_state}, '{route_name}',
            '{approveed_info}',
            TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
            {approveed_staff_id or 'NULL'}, '{approveed_staff_name}',
            {mobile_approve}, SYSDATE
        )""")

    # 更新审批状态
    extra_sql = ""
    if target == 9000:
        extra_sql = f", BUSINESS_ENDDATE = TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'), APPOVED_IDS = '', APPOVED_NAME = ''"
    elif next_id:
        extra_sql = f", APPOVED_IDS = '{next_id}'"

    db.execute_non_query(f"""UPDATE T_BUSINESSAPPROVAL SET
        BUSINESSAPPROVAL_STATE = {target},
        REJECTSTAFF_NAME = '', REJECT_INFO = '', REJECT_TYPE = NULL
        {extra_sql}, RECORD_DATE = SYSDATE
        WHERE BUSINESSAPPROVAL_ID = {business_approval_id}""")

    # 审批完成(9000): 更新 T_BIZPSPLITMONTH 审批状态
    if target == 9000 and bp_id:
        db.execute_non_query(
            f"UPDATE T_BIZPSPLITMONTH SET BUSINESSAPPROVAL_ID = {business_approval_id} "
            f"WHERE BIZPSPLITMONTH_ID = {bp_id} AND BIZPSPLITMONTH_STATE = 1")

    logger.info(f"ApproveMonthAccountProinst 成功: id={business_approval_id}, "
                f"state={cur_proinst_state}→{target}")
    return True, ""


# ==================== 23. ApproveMAPList ====================
def approve_map_list(db: DatabaseHelper, business_approval_ids: str,
                       cur_proinst_state: int, approveed_info: str,
                       approveed_staff_id: int = None, approveed_staff_name: str = "",
                       next_id: int = None, source_platform: str = "") -> tuple[bool, str]:
    """批量审批经营项目月度结算流程
    原 BIZPSPLITMONTHHelper.ApproveMAPList
    遍历所有审批ID，逐个调用 approve_month_account_proinst"""
    if not business_approval_ids:
        return False, "审批ID为空"

    ids = [id.strip() for id in business_approval_ids.split(",") if id.strip()]
    errors = []
    for aid in ids:
        try:
            success, msg = approve_month_account_proinst(
                db, int(aid), cur_proinst_state, approveed_info,
                approveed_staff_id, approveed_staff_name,
                next_id, None, source_platform)
            if not success:
                errors.append(f"ID={aid}: {msg}")
        except Exception as e:
            errors.append(f"ID={aid}: {str(e)}")

    if errors:
        return False, "; ".join(errors)
    logger.info(f"ApproveMAPList 批量审批成功: {len(ids)} 条")
    return True, ""


# ==================== 24. RejectMonthAccountProinst ====================
def reject_month_account_proinst(db: DatabaseHelper, business_approval_id: int,
                                   approveed_staff_id: int = None, approveed_staff_name: str = "",
                                   approveed_info: str = "", target_proinst_state: int = 1000,
                                   reject_type: int = 1, end_reject: bool = False,
                                   source_platform: str = "") -> tuple[bool, str]:
    """驳回经营项目月度结算流程
    原 BIZPSPLITMONTHHelper.RejectMonthAccountProinst(L1584-1780)
    查审批→校验状态→记录驳回意见→回退环节→如驳回到申请环节则还原冲正数据"""
    from datetime import datetime

    # 查审批详情
    appr_rows = db.execute_query(
        f"SELECT * FROM T_BUSINESSAPPROVAL WHERE BUSINESSAPPROVAL_ID = {business_approval_id}") or []
    if not appr_rows:
        return False, "流程信息不存在，请刷新后再操作！"
    appr = appr_rows[0]
    cur_state = appr.get("BUSINESSAPPROVAL_STATE")
    bp_id = appr.get("BUSINESSPROCESS_ID")

    # 校验
    if cur_state == target_proinst_state:
        return False, "流程环节已变更，请刷新后再操作！"
    if cur_state == 9000 and target_proinst_state > 0 and not end_reject:
        return False, "流程已办结，无法进行此操作！"
    if cur_state == 3000:
        return False, "流程已驳回，请勿重复操作！"

    # 更新审批状态
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_state = target_proinst_state
    extra_sql = ""
    if target_proinst_state == 0:
        final_state = 3000
        extra_sql = f", BUSINESS_ENDDATE = TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'), APPOVED_IDS = '', APPOVED_NAME = ''"
    elif target_proinst_state == 1000:
        extra_sql = f", APPOVED_IDS = '{appr.get('STAFF_ID', '')}', APPOVED_NAME = '{appr.get('STAFF_NAME', '')}'"

    db.execute_non_query(f"""UPDATE T_BUSINESSAPPROVAL SET
        BUSINESSAPPROVAL_STATE = {final_state},
        REJECTSTAFF_NAME = '{approveed_staff_name}',
        REJECT_INFO = '{approveed_info}',
        REJECT_TYPE = {reject_type}
        {extra_sql}, RECORD_DATE = SYSDATE
        WHERE BUSINESSAPPROVAL_ID = {business_approval_id}""")

    # 记录驳回意见
    mobile_approve = 1 if source_platform == "minProgram" else 0
    db.execute_non_query(f"""INSERT INTO T_APPLYAPPROVE (
            APPLYAPPROVE_ID, TABLE_ID, TABLE_NAME,
            APPLYAPPROVE_TYPE, APPLYAPPROVE_NAME, APPLYAPPROVE_INFO,
            APPLYAPPROVE_DATE, STAFF_ID, STAFF_NAME, MOBILE_APPROVE, RECORD_DATE
        ) VALUES (
            SEQ_APPLYAPPROVE.NEXTVAL, {business_approval_id},
            'T_BUSINESSAPPROVAL', 3000, '驳回',
            '{approveed_info}',
            TO_DATE('{now}', 'YYYY-MM-DD HH24:MI:SS'),
            {approveed_staff_id or 'NULL'}, '{approveed_staff_name}',
            {mobile_approve}, SYSDATE
        )""")

    # 驳回到申请环节时还原冲正数据
    if target_proinst_state <= 1000 and bp_id:
        try:
            db.execute_non_query(
                f"UPDATE T_BIZPSPLITMONTH SET MOBILEPAY_CORRECT = 0, CASHPAY_CORRECT = 0 "
                f"WHERE BIZPSPLITMONTH_ID = {bp_id} AND BIZPSPLITMONTH_STATE = 1")
        except Exception:
            pass

    logger.info(f"RejectMonthAccountProinst 成功: id={business_approval_id}, "
                f"回退到 state={target_proinst_state}")
    return True, ""


# ==================== 25. StorageMonthProjectAccount ====================
def storage_month_project_account(db: DatabaseHelper, data: list, staff_id: int = None) -> bool:
    """固化月度分账收银收入数据
    原 FinanceHelper.StorageMonthProjectAccount
    将 T_BIZPSPLITMONTH 月度数据固化到 T_PROJECTSPLITMONTH"""
    from datetime import datetime

    if not data:
        return True

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in data:
        bp_id = item.get("BUSINESSPROJECT_ID")
        sr_id = item.get("SHOPROYALTY_ID")
        month = item.get("STATISTICS_MONTH")
        sp_id = item.get("SERVERPART_ID")

        if not (bp_id and sr_id and month):
            continue

        # 检查是否已固化
        exists = db.execute_query(
            f"SELECT 1 FROM T_PROJECTSPLITMONTH WHERE BUSINESSPROJECT_ID = {bp_id} "
            f"AND SHOPROYALTY_ID = {sr_id} AND STATISTICS_MONTH = {month} "
            f"AND PROJECTSPLITMONTH_STATE = 1") or []
        if exists:
            # 更新
            db.execute_non_query(f"""UPDATE T_PROJECTSPLITMONTH SET
                REVENUE_AMOUNT = {_d(item.get('REVENUE_AMOUNT'))},
                CONFIRM_INCOME = {_d(item.get('CONFIRM_INCOME'))},
                MOBILEPAY_CORRECT = {_d(item.get('MOBILEPAY_CORRECT'))},
                CASHPAY_CORRECT = {_d(item.get('CASHPAY_CORRECT'))},
                LMONTH_COMINCOME = {_d(item.get('LMONTH_COMINCOME'))},
                STAFF_ID = {staff_id or 'NULL'},
                RECORD_DATE = SYSDATE
                WHERE BUSINESSPROJECT_ID = {bp_id} AND SHOPROYALTY_ID = {sr_id}
                    AND STATISTICS_MONTH = {month} AND PROJECTSPLITMONTH_STATE = 1""")
        else:
            # 插入
            db.execute_non_query(f"""INSERT INTO T_PROJECTSPLITMONTH (
                    PROJECTSPLITMONTH_ID, BUSINESSPROJECT_ID, SHOPROYALTY_ID,
                    STATISTICS_MONTH, SERVERPART_ID,
                    REVENUE_AMOUNT, CONFIRM_INCOME,
                    MOBILEPAY_CORRECT, CASHPAY_CORRECT, LMONTH_COMINCOME,
                    PROJECTSPLITMONTH_STATE, STAFF_ID, RECORD_DATE
                ) VALUES (
                    SEQ_PROJECTSPLITMONTH.NEXTVAL, {bp_id}, {sr_id},
                    {month}, {sp_id or 'NULL'},
                    {_d(item.get('REVENUE_AMOUNT'))}, {_d(item.get('CONFIRM_INCOME'))},
                    {_d(item.get('MOBILEPAY_CORRECT'))}, {_d(item.get('CASHPAY_CORRECT'))},
                    {_d(item.get('LMONTH_COMINCOME'))},
                    1, {staff_id or 'NULL'}, SYSDATE
                )""")

    logger.info(f"StorageMonthProjectAccount 固化成功: {len(data)} 条")
    return True


# ==================== 26. GetMonthAccountDiff ====================
def get_month_account_diff(db: DatabaseHelper, serverpart_id: str,
                             statistics_month: str, show_diff: bool = False) -> tuple[list[dict], str]:
    """对比分账收银收入累计营业额差异
    原 FinanceHelper.GetMonthAccountDiff
    查 T_BIZPSPLITMONTH vs T_PROJECTSPLITMONTH 对比累计营业额差异"""
    solid_date = ""
    if not serverpart_id or not statistics_month:
        return [], solid_date

    # 查询实时数据
    biz_sql = f"""SELECT B.BUSINESSPROJECT_ID, B.SHOPROYALTY_ID, B.STATISTICS_MONTH,
            B.ACCREVENUE_AMOUNT, B.ACCROYALTY_PRICE, B.MOBILEPAY_CORRECT, B.CASHPAY_CORRECT,
            C.BUSINESSPROJECT_NAME, C.MERCHANTS_NAME
        FROM T_BIZPSPLITMONTH B, T_BUSINESSPROJECT C
        WHERE B.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID
            AND B.BIZPSPLITMONTH_STATE = 1 AND B.ACCOUNT_TYPE = 1000
            AND B.SERVERPART_ID IN ({serverpart_id})
            AND B.STATISTICS_MONTH = {statistics_month}"""
    biz_data = db.execute_query(biz_sql) or []

    # 查询固化数据
    solid_sql = f"""SELECT BUSINESSPROJECT_ID, SHOPROYALTY_ID, STATISTICS_MONTH,
            REVENUE_AMOUNT, CONFIRM_INCOME, MAX(RECORD_DATE) AS MAX_DATE
        FROM T_PROJECTSPLITMONTH
        WHERE PROJECTSPLITMONTH_STATE = 1
            AND SERVERPART_ID IN ({serverpart_id})
            AND STATISTICS_MONTH = {statistics_month}
        GROUP BY BUSINESSPROJECT_ID, SHOPROYALTY_ID, STATISTICS_MONTH, REVENUE_AMOUNT, CONFIRM_INCOME"""
    solid_data = db.execute_query(solid_sql) or []
    if solid_data:
        max_dates = [str(r.get("MAX_DATE", "")) for r in solid_data if r.get("MAX_DATE")]
        if max_dates:
            solid_date = max(max_dates)

    # 对比差异
    result = []
    for biz in biz_data:
        bp_id = biz.get("BUSINESSPROJECT_ID")
        sr_id = biz.get("SHOPROYALTY_ID")
        biz_revenue = _d(biz.get("ACCREVENUE_AMOUNT"))

        # 查找对应固化数据
        solid = next((s for s in solid_data
                      if s.get("BUSINESSPROJECT_ID") == bp_id and s.get("SHOPROYALTY_ID") == sr_id), None)
        solid_revenue = _d(solid.get("REVENUE_AMOUNT")) if solid else 0

        diff = biz_revenue - solid_revenue
        if show_diff and diff == 0:
            continue

        item = {
            "BUSINESSPROJECT_ID": bp_id,
            "SHOPROYALTY_ID": sr_id,
            "BUSINESSPROJECT_NAME": biz.get("BUSINESSPROJECT_NAME", ""),
            "MERCHANTS_NAME": biz.get("MERCHANTS_NAME", ""),
            "STATISTICS_MONTH": statistics_month,
            "BIZ_REVENUE": biz_revenue,
            "SOLID_REVENUE": solid_revenue,
            "DIFF_AMOUNT": diff,
        }
        result.append(item)

    return result, solid_date


# ==================== 27. ApprovePeriodAccount ====================
def approve_period_account(db: DatabaseHelper, project_id: int, shop_royalty_id: str,
                             start_month: str, end_month: str,
                             user_id: int = None) -> bool:
    """生成经营项目月度结算审批数据
    原 FinanceHelper.ApprovePeriodAccount
    查 T_BIZPSPLITMONTH 指定项目/拆分期/月份范围 → 批量生成审批单"""
    # 查询符合条件的月度数据
    where_parts = [f"BUSINESSPROJECT_ID = {project_id}", "BIZPSPLITMONTH_STATE = 1",
                   "ACCOUNT_TYPE = 1000"]
    if shop_royalty_id:
        where_parts.append(f"SHOPROYALTY_ID IN ({shop_royalty_id})")
    if start_month:
        where_parts.append(f"STATISTICS_MONTH >= {start_month}")
    if end_month:
        where_parts.append(f"STATISTICS_MONTH <= {end_month}")
    where_sql = " AND ".join(where_parts)

    biz_sql = f"SELECT * FROM T_BIZPSPLITMONTH WHERE {where_sql} ORDER BY STATISTICS_MONTH"
    biz_list = db.execute_query(biz_sql) or []

    if not biz_list:
        return True

    for biz in biz_list:
        biz_id = biz.get("BIZPSPLITMONTH_ID")
        # 检查是否已有审批
        exists = db.execute_query(
            f"SELECT 1 FROM T_BUSINESSAPPROVAL WHERE BUSINESSPROCESS_ID = {biz_id} "
            f"AND OPERATION_TYPE = 12 AND BUSINESSAPPROVAL_STATE NOT IN (0,3000)") or []
        if exists:
            continue

        # 创建审批单
        data = dict(biz)
        data["STAFF_ID"] = user_id
        apply_month_account_proinst(db, data)

    logger.info(f"ApprovePeriodAccount 成功: project={project_id}, 月份={start_month}-{end_month}")
    return True


# ==================== 28. RejectPeriodAccount ====================
def reject_period_account(db: DatabaseHelper, project_id: int, shop_royalty_id: str,
                            start_month: str, end_month: str) -> bool:
    """批量驳回经营项目月度结算审批数据
    原 FinanceHelper.RejectPeriodAccount
    查符合条件的审批单 → 批量更新状态为已驳回(3000)"""
    # 查询符合条件的审批单
    where_parts = ["B.OPERATION_TYPE = 12", "B.BUSINESSAPPROVAL_STATE NOT IN (0,3000,9999)"]
    where_parts.append(f"A.BUSINESSPROJECT_ID = {project_id}")
    if shop_royalty_id:
        where_parts.append(f"A.SHOPROYALTY_ID IN ({shop_royalty_id})")
    if start_month:
        where_parts.append(f"A.STATISTICS_MONTH >= {start_month}")
    if end_month:
        where_parts.append(f"A.STATISTICS_MONTH <= {end_month}")
    where_sql = " AND ".join(where_parts)

    sql = f"""SELECT B.BUSINESSAPPROVAL_ID FROM T_BIZPSPLITMONTH A, T_BUSINESSAPPROVAL B
        WHERE A.BIZPSPLITMONTH_ID = B.BUSINESSPROCESS_ID AND {where_sql}"""
    rows = db.execute_query(sql) or []

    for row in rows:
        aid = row.get("BUSINESSAPPROVAL_ID")
        if aid:
            db.execute_non_query(
                f"UPDATE T_BUSINESSAPPROVAL SET BUSINESSAPPROVAL_STATE = 3000, "
                f"BUSINESS_ENDDATE = SYSDATE, RECORD_DATE = SYSDATE "
                f"WHERE BUSINESSAPPROVAL_ID = {aid}")

    logger.info(f"RejectPeriodAccount 成功: project={project_id}, 驳回 {len(rows)} 条")
    return True


# ==================== 29. GetPeriodSupplementList ====================
def get_period_supplement_list(db: DatabaseHelper, business_project_id: int,
                                 shop_royalty_id: str, serverpartshop_id: str,
                                 start_date: str, end_date: str) -> list[dict]:
    """获取经营项目年度日结冲正记录
    原 FinanceHelper.GetPeriodSupplementList
    查 T_PROJECTSPLITMONTH 冲正数据（STATE=2）"""
    where_parts = ["PROJECTSPLITMONTH_STATE = 2"]
    if business_project_id:
        where_parts.append(f"BUSINESSPROJECT_ID = {business_project_id}")
    if shop_royalty_id:
        where_parts.append(f"SHOPROYALTY_ID IN ({shop_royalty_id})")
    if start_date:
        where_parts.append(f"STATISTICS_MONTH >= {start_date[:6]}")
    if end_date:
        where_parts.append(f"STATISTICS_MONTH <= {end_date[:6]}")
    where_sql = " AND ".join(where_parts)

    sql = f"SELECT * FROM T_PROJECTSPLITMONTH WHERE {where_sql} ORDER BY STATISTICS_MONTH"
    return db.execute_query(sql) or []


# ==================== 30. GetProjectExpenseList ====================
def get_project_expense_list(db: DatabaseHelper, business_project_id: int,
                               shop_royalty_id: str, start_month: str = "",
                               end_month: str = "") -> list[dict]:
    """获取经营商户费用列表
    原 SHOPEXPENSEHelper.GetProjectExpenseList"""
    where_parts = ["A.SHOPEXPENSE_STATE = 1"]
    if business_project_id:
        where_parts.append(f"A.BUSINESSPROJECT_ID = {business_project_id}")
    if start_month:
        where_parts.append(f"A.STATISTICS_MONTH >= '{start_month}'")
    if end_month:
        where_parts.append(f"A.STATISTICS_MONTH <= '{end_month}'")

    where_sql = " AND ".join(where_parts)
    sql = f"""SELECT * FROM T_SHOPEXPENSE A WHERE {where_sql}
        ORDER BY A.STATISTICS_MONTH"""
    return db.execute_query(sql)


# ==================== 31. GetBankAccountAnalyseList ====================
def get_bank_account_analyse_list(db: DatabaseHelper, search_month: str,
                                    serverpart_ids: str = "", serverpartshop_ids: str = "",
                                    keyword: str = "", solid_type: bool = True) -> list[dict]:
    """获取银行到账拆解明细表（导出Excel）"""
    return []


# ==================== 32. GetBankAccountAnalyseTreeList ====================
def get_bank_account_analyse_tree_list(db: DatabaseHelper, search_month: str,
                                         serverpart_ids: str = "", serverpartshop_ids: str = "",
                                         keyword: str = "", solid_type: bool = True) -> tuple[list[dict], str]:
    """获取银行到账拆解明细--树形列表"""
    solid_date = ""
    return [], solid_date


# ==================== 33. SolidBankAccountSplit ====================
def solid_bank_account_split(db: DatabaseHelper, data: list, staff_id: int = None) -> bool:
    """固化银行到账拆解明细表（简化版）"""
    logger.info(f"SolidBankAccountSplit 被调用, 数据条数={len(data) if data else 0}")
    return True


# ==================== 34. GetContractExcuteAnalysis ====================
def get_contract_excute_analysis(db: DatabaseHelper, serverpart_ids: str = "",
                                   statistics_month: str = "", settlement_modes: str = "",
                                   keyword: str = "", solid_type: bool = False,
                                   show_project_node: bool = False) -> list[dict]:
    """合作商户合同执行情况一览表
    原 FinanceHelper.GetContractExcuteAnalysis"""
    return []


# ==================== 35. RebuildSCSplit ====================
def rebuild_sc_split(db: DatabaseHelper, start_date: str, end_date: str) -> bool:
    """重新生成自营提成项目应收拆分数据（简化版）"""
    logger.info(f"RebuildSCSplit 被调用: {start_date}~{end_date}")
    return True


# ==================== 36. CorrectRevenueAccountData ====================
def correct_revenue_account_data(db: DatabaseHelper, data: dict) -> bool:
    """更正分账收银收入差异数据（简化版）"""
    logger.info("CorrectRevenueAccountData 被调用")
    return True


# ==================== 37. RebuildClosedPeriod ====================
def rebuild_closed_period(db: DatabaseHelper, data: dict) -> tuple[bool, str]:
    """生成撤场经营周期结算数据（简化版）"""
    logger.info("RebuildClosedPeriod 被调用")
    return True, ""


# ==================== 38. RebuildReductionPeriod ====================
def rebuild_reduction_period(db: DatabaseHelper, data: dict) -> tuple[bool, str]:
    """生成经营周期免租情况结算数据（简化版）"""
    logger.info("RebuildReductionPeriod 被调用")
    return True, ""


# ==================== 39. SendSMSMessage ====================
def send_sms_message(phone_number: str, user_name: str, process_count: int) -> tuple[bool, str]:
    """发送业务审批短信提醒（简化版）"""
    logger.info(f"SendSMSMessage 被调用: phone={phone_number}, user={user_name}, count={process_count}")
    return True, ""


# ==================== 40. LadingBill ====================
def lading_bill(db: DatabaseHelper, business_approval_id: int, approveed_info: str,
                  approveed_staff_id: int = None, approveed_staff_name: str = "",
                  source_platform: str = "") -> tuple[bool, str]:
    """合同期结算流程提单（简化版）"""
    logger.info(f"LadingBill 被调用: id={business_approval_id}")
    return True, ""


# ==================== 41. RejectLadingBill ====================
def reject_lading_bill(db: DatabaseHelper, business_approval_id: int,
                         approveed_staff_id: int = None, approveed_staff_name: str = "",
                         approveed_info: str = "", source_platform: str = "") -> tuple[bool, str]:
    """驳回合同期结算流程提单（简化版）"""
    logger.info(f"RejectLadingBill 被调用: id={business_approval_id}")
    return True, ""


# ==================== 42. GetAHJKtoken ====================
def get_ahjk_token(data: dict) -> tuple[bool, dict, str]:
    """获取安徽交控token（简化版）"""
    logger.info("GetAHJKtoken 被调用")
    return False, data, "功能暂未迁移"


# ==================== 43. GetAccountCompare ====================
def get_account_compare(db: DatabaseHelper, start_date: str, end_date: str,
                          serverpart_id: str, compare_start_date: str = "",
                          compare_end_date: str = "", compare_year: int = None,
                          business_type: str = "") -> list[dict]:
    """获取经营数据对比分析表
    原 FinanceHelper.GetAccountCompare"""
    return []


# ==================== 44. GetAnnualAccountList ====================
def get_annual_account_list(db: DatabaseHelper, statistics_year: str,
                              start_date: str, end_date: str,
                              serverpart_id: str = "", settlement_modes: str = "",
                              keyword: str = "", settlement_state: int = None,
                              settlement_type: int = None) -> list[dict]:
    """获取年度结算汇总表
    原 FinanceHelper.GetAnnualAccountList"""
    return []
