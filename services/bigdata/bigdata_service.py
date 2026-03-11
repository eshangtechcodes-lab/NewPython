from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BigDataController + CustomerController 业务服务
严格按照 C# Helper 源码迁移，保持完全一致的 SQL 逻辑

C# 源文件参考：
  - SECTIONFLOWHelper.cs (712行)
  - SECTIONFLOWMONTHHelper.cs (293行)
  - BAYONETHelper.cs (449行)
  - BAYONETDAILY_AHHelper.cs
  - BAYONETANALYSISHelper.cs / BAYONETOAANALYSISHelper.cs
  - BAYONETWARNINGHelper.cs
  - CUSTOMERGROUP_AMOUNTHelper.cs
  - A2305052305180725Helper.cs (313行)
  - BigDataHelper.cs / CustomerHelper.cs
"""
from typing import Optional, Tuple, List
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper


# ============================================================
# 实体元数据（从 C# Helper 精确提取）
# ============================================================
ENTITIES = {
    "SECTIONFLOW": {
        "table": "T_SECTIONFLOW",
        "pk": "SECTIONFLOW_ID",
        "seq": "SEQ_SECTIONFLOW",
        "status": "SECTIONFLOW_STATUS",  # C# BindDataRowToModel L136: SECTIONFLOW_STATUS
        "delete_type": "none",  # C# DeleteSECTIONFLOW: 空实现，always return false
        "exclude": {"STATISTICS_DATE_Start", "STATISTICS_DATE_End", "SERVERPART_IDS"},
        "date_fields": {"STATISTICS_DATE"},
        "date_range": {"STATISTICS_DATE": ("STATISTICS_DATE_Start", "STATISTICS_DATE_End", "yyyyMMdd")},
        "in_fields": {"SERVERPART_ID": "SERVERPART_IDS"},
    },
    "SECTIONFLOWMONTH": {
        "table": "T_SECTIONFLOWMONTH",
        "pk": "SECTIONFLOWMONTH_ID",
        "seq": "SEQ_SECTIONFLOWMONTH",
        "status": "SECTIONFLOWMONTH_STATE",  # C# BindDataRowToModel L148: SECTIONFLOWMONTH_STATE
        "delete_type": "soft",  # C# UPDATE SET SECTIONFLOWMONTH_STATE = 0
        "exclude": {"SERVERPART_IDS", "STATISTICS_MONTH_Start", "STATISTICS_MONTH_End"},
        "date_fields": {"STATISTICS_MONTH", "OPERATE_DATE"},
        "date_range": {"STATISTICS_MONTH": ("STATISTICS_MONTH_Start", "STATISTICS_MONTH_End", "yyyyMM")},
        "in_fields": {"SERVERPART_ID": "SERVERPART_IDS"},
    },
    "BAYONET": {
        "table": "T_BAYONET",
        "pk": "BAYONET_ID",
        "seq": "SEQ_BAYONET",
        "status": "BAYONET_STATUS",  # C# BindDataRowToModel L144: BAYONET_STATUS
        "delete_type": "soft",  # C# _BAYONET.BAYONET_STATUS = 0; _BAYONET.Update()
        "exclude": {"INOUT_TYPES", "INOUT_TIME_Start", "INOUT_TIME_End",
                     "VEHICLE_TYPES", "STATISTICS_DATE_Start", "STATISTICS_DATE_End"},
        "date_fields": {"INOUT_TIME", "STATISTICS_DATE"},
        "date_range": {"STATISTICS_DATE": ("STATISTICS_DATE_Start", "STATISTICS_DATE_End", "yyyyMMdd")},
        "in_fields": {"INOUT_TYPE": "INOUT_TYPES"},
        "in_fields_str": {"VEHICLE_TYPE": "VEHICLE_TYPES"},  # 字符串 IN 需加引号
    },
    "BAYONETDAILY_AH": {
        "table": "T_BAYONETDAILY_AH",
        "pk": "BAYONETDAILY_AH_ID",
        "seq": "SEQ_BAYONETDAILY_AH",
        "status": "BAYONETDAILY_AH_STATE",
        "delete_type": "none",  # C# DeleteBAYONETDAILY_AH: 空实现，always return false
        "exclude": {"STATISTICS_DATE_Start", "STATISTICS_DATE_End", "SERVERPART_IDS"},
        "date_fields": set(),
        "date_range": {"STATISTICS_DATE": ("STATISTICS_DATE_Start", "STATISTICS_DATE_End", "yyyyMMdd")},
        "in_fields": {"SERVERPART_ID": "SERVERPART_IDS"},
    },
    "BAYONETANALYSIS": {
        "table": "T_BAYONETANALYSIS",
        "pk": "BAYONETANALYSIS_ID",
        "seq": "SEQ_BAYONETANALYSIS",
        "status": "BAYONETANALYSIS_STATE",
        "delete_type": "none",  # C# DeleteBAYONETANALYSIS: 空实现，always return false
        "exclude": {"SERVERPART_IDS"},
        "date_fields": set(),
        "date_range": {},
        "in_fields": {"SERVERPART_ID": "SERVERPART_IDS"},
    },
    "BAYONETOAANALYSIS": {
        "table": "T_BAYONETOAANALYSIS",
        "pk": "BAYONETOAANALYSIS_ID",
        "seq": "SEQ_BAYONETOAANALYSIS",
        "status": "BAYONETOAANALYSIS_STATE",
        "delete_type": "none",  # C# DeleteBAYONETOAANALYSIS: 空实现，always return false
        "exclude": {"SERVERPART_IDS"},
        "date_fields": set(),
        "date_range": {},
        "in_fields": {"SERVERPART_ID": "SERVERPART_IDS"},
    },
    "BAYONETWARNING": {
        "table": "T_BAYONETWARNING",
        "pk": "BAYONETWARNING_ID",
        "seq": "SEQ_BAYONETWARNING",
        "status": "BAYONETWARNING_STATE",
        "delete_type": "soft",
        "exclude": set(),
        "date_fields": set(),
        "date_range": {},
        "in_fields": {},
    },
    "CUSTOMERGROUP_AMOUNT": {
        "table": "T_CUSTOMERGROUP_AMOUNT",
        "pk": "CUSTOMERGROUP_AMOUNT_ID",
        "seq": "SEQ_CUSTOMERGROUP_AMOUNT",
        "status": "CUSTOMERGROUP_AMOUNT_STATE",
        "delete_type": "none",  # C# DeleteCUSTOMERGROUP_AMOUNT: 空实现，always return false
        # C# L32-33: GetWhereSQL exclude 参数
        "exclude": {"STATISTICS_MONTH_Start", "STATISTICS_MONTH_End", "SERVERPART_IDS", "SERVERPART_CODES"},
        # C# L112: STATISTICS_MONTH 通过 TranslateDateTime 格式化
        "date_fields": {"STATISTICS_MONTH"},
        # C# L39-48: STATISTICS_MONTH 日期范围
        "date_range": {"STATISTICS_MONTH": ("STATISTICS_MONTH_Start", "STATISTICS_MONTH_End", "yyyyMM")},
        # C# L50-52: SERVERPART_ID IN (SERVERPART_IDS) 数字型
        "in_fields": {"SERVERPART_ID": "SERVERPART_IDS"},
        # C# L55-58: SERVERPART_CODE IN ('SERVERPART_CODES') 字符串型
        "in_fields_str": {"SERVERPART_CODE": "SERVERPART_CODES"},
        # C# Model 非 DB 属性（序列化时输出默认值 null）
        "model_extra_fields": ["STATISTICS_MONTH_Start", "STATISTICS_MONTH_End", "SERVERPART_IDS", "SERVERPART_CODES"],
        # C# BindDataRowToModel L112: TranslateDateTime 格式化 (int 202112 → str '2021/12')
        "translate_date_fields": {"STATISTICS_MONTH": "yyyyMM"},
    },
}


# ============================================================
# 通用 CRUD 函数（按 C# OperationDataHelper 模式实现）
# ============================================================

def _build_where(sp: dict, entity_cfg: dict, query_type: int = 0) -> str:
    """
    按 C# OperationDataHelper.GetWhereSQL 逻辑构建 WHERE 条件
    - query_type=0: LIKE 模糊匹配字符串
    - query_type=1: = 精确匹配
    """
    conditions = []
    exclude = entity_cfg.get("exclude", set())
    in_fields = entity_cfg.get("in_fields", {})
    in_fields_str = entity_cfg.get("in_fields_str", {})
    date_range = entity_cfg.get("date_range", {})

    # 收集日期范围参数名（排除）
    date_range_params = set()
    for dr_cfg in date_range.values():
        date_range_params.add(dr_cfg[0])
        date_range_params.add(dr_cfg[1])

    for key, value in sp.items():
        if key in exclude or key in date_range_params:
            continue
        if value is None:
            continue
        if isinstance(value, str) and value.strip() == "":
            continue
        # IN 查询（数字型）
        if key in in_fields.values():
            continue  # 由 in_fields 处理
        if key in in_fields_str.values():
            continue
        # 普通字段
        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")

    # IN 查询处理
    for db_field, param_name in in_fields.items():
        val = sp.get(param_name, "")
        if val and str(val).strip():
            conditions.append(f"{db_field} IN ({val})")

    for db_field, param_name in in_fields_str.items():
        val = sp.get(param_name, "")
        if val and str(val).strip():
            quoted = "','".join(str(val).split(","))
            conditions.append(f"{db_field} IN ('{quoted}')")

    # 日期范围
    for db_field, (start_param, end_param, fmt) in date_range.items():
        s_val = sp.get(start_param, "")
        e_val = sp.get(end_param, "")
        if s_val and str(s_val).strip():
            try:
                s_fmt = datetime.strptime(str(s_val)[:10], "%Y-%m-%d").strftime(
                    "%Y%m%d" if fmt == "yyyyMMdd" else "%Y%m")
                conditions.append(f"{db_field} >= {s_fmt}")
            except Exception:
                conditions.append(f"{db_field} >= '{s_val}'")
        if e_val and str(e_val).strip():
            try:
                e_fmt = datetime.strptime(str(e_val)[:10], "%Y-%m-%d").strftime(
                    "%Y%m%d" if fmt == "yyyyMMdd" else "%Y%m")
                conditions.append(f"{db_field} <= {e_fmt}")
            except Exception:
                conditions.append(f"{db_field} <= '{e_val}'")

    return " AND ".join(conditions) if conditions else ""


def _apply_model_transform(row: dict, entity_cfg: dict) -> dict:
    """
    C# BindDataRowToModel 后处理：
    1. 补充 Model 非 DB 属性（默认 null）
    2. TranslateDateTime 日期格式化（int → str）
    """
    # 补充 Model 扩展字段
    for field in entity_cfg.get("model_extra_fields", []):
        if field not in row:
            row[field] = None
    # TranslateDateTime 格式化
    for field, fmt in entity_cfg.get("translate_date_fields", {}).items():
        val = row.get(field)
        if val is not None:
            s = str(val)
            if fmt == "yyyyMM" and len(s) >= 6:
                # 202112 → '2021/12'
                row[field] = f"{s[:4]}/{s[4:6]}"
            elif fmt == "yyyyMMdd" and len(s) >= 8:
                # 20211231 → '2021/12/31'
                row[field] = f"{s[:4]}/{s[4:6]}/{s[6:8]}"
    return row


def get_entity_list(db: DatabaseHelper, entity_name: str, search_model: dict):
    """
    通用 GetXXXList — 按 C# Helper.GetXXXList 逻辑
    1. 构建 WHERE (SearchParameter + 日期范围 + IN查询)
    2. SELECT * FROM T_XXX WHERE ...
    3. 关键词过滤 (keyWord)
    4. 排序 (SortStr)
    5. 计算 TotalCount
    6. 分页 (PageIndex/PageSize)
    """
    e = ENTITIES[entity_name]
    table = e["table"]

    # 构建 WHERE
    sp = search_model.get("SearchParameter") or {}
    qt = search_model.get("QueryType", 0) or 0
    where_clause = _build_where(sp, e, qt)
    where_sql = f" WHERE {where_clause}" if where_clause else ""

    # 查询
    sql = f"SELECT * FROM {table}{where_sql}"
    rows = db.execute_query(sql) or []

    # 关键词过滤（C# RowFilter）
    kw = search_model.get("keyWord")
    if kw and isinstance(kw, dict) and kw.get("Key") and kw.get("Value"):
        search_value = str(kw["Value"])
        keys = [k.strip() for k in str(kw["Key"]).split(",") if k.strip()]
        rows = [r for r in rows if any(
            search_value in str(r.get(k, "")) for k in keys
        )]

    # C# BindDataRowToModel 后处理
    rows = [_apply_model_transform(dict(r), e) for r in rows]

    # 排序
    sort_str = search_model.get("SortStr", "")
    if sort_str and sort_str.strip():
        sort_field = sort_str.replace(" DESC", "").replace(" ASC", "").replace(" desc", "").replace(" asc", "").strip()
        is_desc = "DESC" in sort_str.upper()
        try:
            rows.sort(key=lambda x: x.get(sort_field) or 0, reverse=is_desc)
        except Exception:
            pass

    # TotalCount
    total_count = len(rows)

    # 分页（C# CommonHelper.GetDataTableWithPageSize）
    pi = search_model.get("PageIndex")
    ps = search_model.get("PageSize")
    if pi and ps and int(pi) > 0 and int(ps) > 0:
        start = (int(pi) - 1) * int(ps)
        rows = rows[start:start + int(ps)]
    elif total_count > 10:
        rows = rows[:10]

    return rows, total_count


def get_entity_detail(db: DatabaseHelper, entity_name: str, pk_val: int):
    """通用 GetXXXDetail — SELECT * FROM T_XXX WHERE PK = ?"""
    e = ENTITIES[entity_name]
    sql = f"SELECT * FROM {e['table']} WHERE {e['pk']} = ?"
    rows = db.execute_query(sql, [pk_val])
    if rows:
        return _apply_model_transform(dict(rows[0]), e)
    return {}


def synchro_entity(db: DatabaseHelper, entity_name: str, data: dict):
    """
    通用 SynchroXXX — 按 C# OperationDataHelper.GetTableExcuteSQL 逻辑
    有 ID → 检查存在 → UPDATE；无 ID → SEQ.NEXTVAL → INSERT
    """
    e = ENTITIES[entity_name]
    table, pk, seq = e["table"], e["pk"], e["seq"]
    exclude = e.get("exclude", set())
    date_fields = e.get("date_fields", set())
    record_id = data.get(pk)

    # 过滤非数据库字段
    db_data = {k: v for k, v in data.items() if k not in exclude}

    if record_id is not None:
        # 更新模式：先检查存在
        cnt = db.execute_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [record_id])
        if not cnt or cnt == 0:
            return False, data

        set_parts = []
        for key, value in db_data.items():
            if key == pk:
                continue
            if value is None:
                if key in date_fields:
                    set_parts.append(f"{key} = NULL")
                continue
            if key in date_fields:
                set_parts.append(f"{key} = TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")
        if set_parts:
            db.execute_non_query(
                f"UPDATE {table} SET {', '.join(set_parts)} WHERE {pk} = {record_id}")
    else:
        # 新增模式
        try:
            new_id = db.execute_scalar(f"SELECT {seq}.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({pk}) FROM {table}") or 0) + 1
        data[pk] = new_id
        db_data[pk] = new_id

        columns, values = [], []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if key in date_fields:
                values.append(f"TO_DATE('{value}', 'YYYY/MM/DD HH24:MI:SS')")
            elif isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))
        db.execute_non_query(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})")

    return True, data


def delete_entity(db: DatabaseHelper, entity_name: str, pk_val: int):
    """
    通用 DeleteXXX — 按 C# Helper 各自的 Delete 实现
    - "none": 空实现（如 SECTIONFLOW Delete 始终返回 false）
    - "soft": 软删除 SET STATUS/STATE = 0
    """
    e = ENTITIES[entity_name]
    delete_type = e.get("delete_type", "soft")

    if delete_type == "none":
        # C# SECTIONFLOW DeleteSECTIONFLOW: 空方法体，总是返回 false
        return False

    # 软删除
    table, pk, status = e["table"], e["pk"], e["status"]
    cnt = db.execute_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [pk_val])
    if not cnt or cnt == 0:
        return False
    db.execute_non_query(f"UPDATE {table} SET {status} = 0 WHERE {pk} = {pk_val}")
    return True


# ============================================================
# 散装接口（C# BigDataController 非 CRUD 方法）
# ============================================================

def get_bayonet_daily_summary(db: DatabaseHelper, **kwargs) -> tuple:
    """
    卡口车辆进出日度汇总 — C# A2305052305180725Helper.GetDailyBayonetAnalysis
    按日维度汇总 T_BAYONETDAILY_AH + T_SECTIONFLOW (UNION ALL)
    """
    sp_ids = kwargs.get("ServerpartIds") or kwargs.get("SERVERPART_ID", "")
    sp_region = kwargs.get("ServerpartRegion") or kwargs.get("SERVERPART_REGION", "")
    inout_type = kwargs.get("InoutType") or kwargs.get("INOUT_TYPE", "")
    vehicle_type = kwargs.get("VehicleType") or kwargs.get("VEHICLE_TYPE", "")
    start = kwargs.get("StartDate") or kwargs.get("STATISTICS_DATE_Start", "")
    end = kwargs.get("EndDate") or kwargs.get("STATISTICS_DATE_End", "")
    pi = kwargs.get("PageIndex")
    ps = kwargs.get("PageSize")
    sort_str = kwargs.get("SortStr", "")

    where_sql, flow_sql = "", ""
    if sp_ids:
        where_sql += f" AND A.SERVERPART_ID IN ({sp_ids})"
        flow_sql += f" AND A.SERVERPART_ID IN ({sp_ids})"
    if sp_region:
        quoted = "','".join(sp_region.split(","))
        where_sql += f" AND A.SERVERPART_REGION IN ('{quoted}')"
        flow_sql += f" AND A.SERVERPART_REGION IN ('{quoted}')"
    if inout_type:
        where_sql += f" AND A.INOUT_TYPE IN ({inout_type})"
    if vehicle_type:
        vt_quoted = "','".join(vehicle_type.split(","))
        where_sql += f" AND A.VEHICLE_TYPE IN ('{vt_quoted}')"
    if start:
        try:
            s = datetime.strptime(str(start)[:10], '%Y-%m-%d').strftime('%Y%m%d')
        except Exception:
            s = start
        where_sql += f" AND STATISTICS_DATE >= {s}"
        flow_sql += f" AND STATISTICS_DATE >= {s}"
    if end:
        try:
            e = datetime.strptime(str(end)[:10], '%Y-%m-%d').strftime('%Y%m%d')
        except Exception:
            e = end
        where_sql += f" AND STATISTICS_DATE <= {e}"
        flow_sql += f" AND STATISTICS_DATE <= {e}"

    sql = f"""SELECT SERVERPART_NAME, SERVERPART_REGION, STATISTICS_DATE,
            1 AS DATE_COUNT, SUM(VEHICLE_COUNT) AS VEHICLE_COUNT,
            SUM(VEHICLE_COUNT_DXC) AS VEHICLE_COUNT_DXC,
            SUM(VEHICLE_COUNT_ZXC) AS VEHICLE_COUNT_ZXC,
            SUM(VEHICLE_COUNT_XXC) AS VEHICLE_COUNT_XXC
        FROM (
            SELECT A.SERVERPART_NAME, A.SERVERPART_REGION,
                SUM(A.VEHICLE_COUNT) AS VEHICLE_COUNT,
                SUM(CASE WHEN A.VEHICLE_TYPE='大型车' THEN A.VEHICLE_COUNT END) AS VEHICLE_COUNT_DXC,
                SUM(CASE WHEN A.VEHICLE_TYPE='中型车' THEN A.VEHICLE_COUNT END) AS VEHICLE_COUNT_ZXC,
                SUM(CASE WHEN A.VEHICLE_TYPE='小型车' THEN A.VEHICLE_COUNT END) AS VEHICLE_COUNT_XXC,
                A.STATISTICS_DATE
            FROM T_BAYONETDAILY_AH A WHERE 1=1{where_sql}
            GROUP BY A.SERVERPART_NAME, A.SERVERPART_REGION, A.STATISTICS_DATE
            UNION ALL
            SELECT A.SERVERPART_NAME, A.SERVERPART_REGION, 0, 0, 0, 0, A.STATISTICS_DATE
            FROM T_SECTIONFLOW A
            WHERE NOT EXISTS (
                SELECT 1 FROM T_BAYONETDAILY_AH B
                WHERE A.STATISTICS_DATE=B.STATISTICS_DATE
                  AND A.SERVERPART_ID=B.SERVERPART_ID
                  AND A.SERVERPART_REGION=B.SERVERPART_REGION){flow_sql}
            GROUP BY A.SERVERPART_NAME, A.SERVERPART_REGION, A.STATISTICS_DATE
        ) GROUP BY SERVERPART_NAME, SERVERPART_REGION, STATISTICS_DATE"""

    rows = db.execute_query(sql) or []
    total = len(rows)
    if pi and ps:
        start_idx = (int(pi) - 1) * int(ps)
        rows = rows[start_idx:start_idx + int(ps)]
    return rows, total


def get_daily_bayonet_analysis(db: DatabaseHelper, **kwargs) -> list:
    """
    日度服务区车流分析 — C# SECTIONFLOWHelper.GetDailyBayonetAnalysis (L315-499)
    1. 获取卡口日汇总数据
    2. 按日期分组→按方位(东南西北)嵌套
    3. 关联 T_REVENUEDAILY 营收数据（东/南→A侧, 西/北→B侧）
    4. 单方位自动补对向空节点
    返回 ServerpartSectionModel 嵌套结构
    """
    try:
        # 获取卡口日汇总基础数据
        flat_rows, _ = get_bayonet_daily_summary(db, **kwargs)
        if not flat_rows:
            return []

        sp_id = kwargs.get("ServerpartIds") or kwargs.get("SERVERPART_ID", "")
        start = kwargs.get("StartDate") or kwargs.get("STATISTICS_DATE_Start", "")
        end = kwargs.get("EndDate") or kwargs.get("STATISTICS_DATE_End", "")
        shop_ids = kwargs.get("ServerpartShopIds", "")

        # 按日期分组
        date_map = {}
        for r in flat_rows:
            d = r.get("STATISTICS_DATE")
            if d not in date_map:
                date_map[d] = {"SERVERPART_NAME": r.get("SERVERPART_NAME", ""), "rows": []}
            date_map[d]["rows"].append(r)

        # 查询营收数据（关联 T_REVENUEDAILY）
        revenue_map = {}
        if sp_id:
            rev_where = f" AND A.SERVERPART_ID = {sp_id}"
            if start:
                try:
                    s = datetime.strptime(str(start)[:10], '%Y-%m-%d').strftime('%Y%m%d')
                except Exception:
                    s = start
                rev_where += f" AND A.STATISTICS_DATE >= {s}"
            if end:
                try:
                    e = datetime.strptime(str(end)[:10], '%Y-%m-%d').strftime('%Y%m%d')
                except Exception:
                    e = end
                rev_where += f" AND A.STATISTICS_DATE <= {e}"
            if shop_ids:
                rev_where += (f" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP B "
                              f"WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPTRADE = B.SHOPTRADE "
                              f"AND B.SERVERPARTSHOP_ID IN ({shop_ids}))")
            rev_sql = (f"SELECT A.STATISTICS_DATE, "
                       f"SUM(REVENUE_AMOUNT_A) AS REVENUE_AMOUNT_A, "
                       f"SUM(REVENUE_AMOUNT_B) AS REVENUE_AMOUNT_B, "
                       f"COUNT(DISTINCT CASE WHEN REVENUE_AMOUNT_A <> 0 THEN STATISTICS_DATE END) AS COUNT_A, "
                       f"COUNT(DISTINCT CASE WHEN REVENUE_AMOUNT_B <> 0 THEN STATISTICS_DATE END) AS COUNT_B "
                       f"FROM T_REVENUEDAILY A WHERE A.REVENUEDAILY_STATE = 1{rev_where} "
                       f"GROUP BY A.STATISTICS_DATE")
            rev_rows = db.execute_query(rev_sql) or []
            for rv in rev_rows:
                revenue_map[str(rv.get("STATISTICS_DATE", ""))] = rv

        regions_order = ["东", "南", "西", "北"]
        opposite = {"东": "西", "西": "东", "南": "北", "北": "南"}

        result = []
        for stat_date, info in sorted(date_map.items(), key=lambda x: str(x[0])):
            section = {
                "SERVERPART_NAME": info["SERVERPART_NAME"],
                "STATISTICS_DATE": stat_date,
                "list": []
            }
            # 按方位分组
            region_data = {}
            for r in info["rows"]:
                reg = r.get("SERVERPART_REGION", "")
                if reg not in region_data:
                    region_data[reg] = r
            # 按方位顺序填充
            for reg in regions_order:
                if reg in region_data:
                    row = dict(region_data[reg])
                    # 关联营收
                    date_key = str(stat_date).replace("-", "")
                    if date_key in revenue_map:
                        rv = revenue_map[date_key]
                        count_f = "COUNT_A" if reg in ("东", "南") else "COUNT_B"
                        sum_f = "REVENUE_AMOUNT_A" if reg in ("东", "南") else "REVENUE_AMOUNT_B"
                        dc = float(rv.get(count_f, 0) or 0)
                        sa = float(rv.get(sum_f, 0) or 0)
                        row["REVENUE_AMOUNT"] = round(sa / dc, 2) if dc > 0 else sa
                    section["list"].append({
                        "SERVERPART_REGION": reg,
                        "SERVERPART": row
                    })
                    # 单方位补对向
                    if len(region_data) == 1 and opposite.get(reg):
                        section["list"].append({
                            "SERVERPART_REGION": opposite[reg],
                            "SERVERPART": {}
                        })
            result.append(section)
        return result
    except Exception as ex:
        logger.error(f"GetDailyBayonetAnalysis 失败: {ex}")
        return []


def get_serverpart_section_flow(db: DatabaseHelper, **kwargs) -> tuple:
    """
    月度服务区车流分析 — C# SECTIONFLOWHelper.GetServerpartSectionFlow (L523-708)
    1. 按月汇总 T_BAYONETDAILY_AH + T_SECTIONFLOW
    2. 按月份分组→按方位(东南西北)嵌套
    3. 关联月度 T_REVENUEDAILY 营收数据
    4. 单方位自动补对向空节点
    返回 ServerpartSectionModel 嵌套结构
    """
    sp_ids = kwargs.get("ServerpartIds") or kwargs.get("SERVERPART_ID", "")
    sp_region = kwargs.get("ServerpartRegion") or kwargs.get("SERVERPART_REGION", "")
    inout_type = kwargs.get("InoutType") or kwargs.get("INOUT_TYPE", "")
    vehicle_type = kwargs.get("VehicleType") or kwargs.get("VEHICLE_TYPE", "")
    start = kwargs.get("StartMonth") or kwargs.get("STATISTICS_DATE_Start", "")
    end = kwargs.get("EndMonth") or kwargs.get("STATISTICS_DATE_End", "")
    pi = kwargs.get("PageIndex")
    ps = kwargs.get("PageSize")
    shop_ids = kwargs.get("ServerpartShopIds", "")

    where_sql, flow_sql = "", ""
    if sp_ids:
        where_sql += f" AND A.SERVERPART_ID IN ({sp_ids})"
        flow_sql += f" AND A.SERVERPART_ID IN ({sp_ids})"
    if sp_region:
        quoted = "','".join(sp_region.split(","))
        where_sql += f" AND A.SERVERPART_REGION IN ('{quoted}')"
        flow_sql += f" AND A.SERVERPART_REGION IN ('{quoted}')"
    if inout_type:
        where_sql += f" AND A.INOUT_TYPE IN ({inout_type})"
    if vehicle_type:
        vt_quoted = "','".join(vehicle_type.split(","))
        where_sql += f" AND A.VEHICLE_TYPE IN ('{vt_quoted}')"
    if start:
        try:
            s = datetime.strptime(str(start)[:10], '%Y-%m-%d').strftime('%Y%m%d')
        except Exception:
            s = start
        where_sql += f" AND STATISTICS_DATE >= {s}"
        flow_sql += f" AND STATISTICS_DATE >= {s}"
    if end:
        try:
            e = datetime.strptime(str(end)[:10], '%Y-%m-%d').strftime('%Y%m%d')
        except Exception:
            e = end
        where_sql += f" AND STATISTICS_DATE <= {e}"
        flow_sql += f" AND STATISTICS_DATE <= {e}"

    sql = f"""SELECT SERVERPART_NAME, SERVERPART_REGION, STATISTICS_DATE,
            SUM(DATE_COUNT) AS DATE_COUNT, SUM(VEHICLE_COUNT) AS VEHICLE_COUNT,
            SUM(VEHICLE_COUNT_DXC) AS VEHICLE_COUNT_DXC,
            SUM(VEHICLE_COUNT_ZXC) AS VEHICLE_COUNT_ZXC,
            SUM(VEHICLE_COUNT_XXC) AS VEHICLE_COUNT_XXC
        FROM (
            SELECT A.SERVERPART_NAME, A.SERVERPART_REGION,
                SUM(A.VEHICLE_COUNT) AS VEHICLE_COUNT,
                SUM(CASE WHEN A.VEHICLE_TYPE='大型车' THEN A.VEHICLE_COUNT END) AS VEHICLE_COUNT_DXC,
                SUM(CASE WHEN A.VEHICLE_TYPE='中型车' THEN A.VEHICLE_COUNT END) AS VEHICLE_COUNT_ZXC,
                SUM(CASE WHEN A.VEHICLE_TYPE='小型车' THEN A.VEHICLE_COUNT END) AS VEHICLE_COUNT_XXC,
                SUBSTR(CAST(A.STATISTICS_DATE AS VARCHAR(8)),1,6) AS STATISTICS_DATE,
                COUNT(DISTINCT A.STATISTICS_DATE) AS DATE_COUNT
            FROM T_BAYONETDAILY_AH A WHERE 1=1{where_sql}
            GROUP BY A.SERVERPART_NAME, A.SERVERPART_REGION, SUBSTR(CAST(A.STATISTICS_DATE AS VARCHAR(8)),1,6)
            UNION ALL
            SELECT A.SERVERPART_NAME, A.SERVERPART_REGION, 0, 0, 0, 0,
                SUBSTR(CAST(A.STATISTICS_DATE AS VARCHAR(8)),1,6) AS STATISTICS_DATE, 0
            FROM T_SECTIONFLOW A
            WHERE NOT EXISTS (
                SELECT 1 FROM T_BAYONETDAILY_AH B
                WHERE A.STATISTICS_DATE=B.STATISTICS_DATE
                  AND A.SERVERPART_ID=B.SERVERPART_ID
                  AND A.SERVERPART_REGION=B.SERVERPART_REGION){flow_sql}
            GROUP BY A.SERVERPART_NAME, A.SERVERPART_REGION, SUBSTR(CAST(A.STATISTICS_DATE AS VARCHAR(8)),1,6)
        ) GROUP BY SERVERPART_NAME, SERVERPART_REGION, STATISTICS_DATE"""

    flat_rows = db.execute_query(sql) or []
    total = len(flat_rows)
    if pi and ps:
        start_idx = (int(pi) - 1) * int(ps)
        flat_rows = flat_rows[start_idx:start_idx + int(ps)]

    # 按月份分组→方位嵌套（C# L537-706）
    month_map = {}
    for r in flat_rows:
        m = r.get("STATISTICS_DATE")
        if m not in month_map:
            month_map[m] = {"SERVERPART_NAME": r.get("SERVERPART_NAME", ""), "rows": []}
        month_map[m]["rows"].append(r)

    # 查询月度营收数据
    revenue_map = {}
    if sp_ids:
        rev_where = f" AND A.SERVERPART_ID = {sp_ids}"
        if start:
            try:
                s = datetime.strptime(str(start)[:10], '%Y-%m-%d').strftime('%Y%m01')
            except Exception:
                s = start
            rev_where += f" AND A.STATISTICS_DATE >= {s}"
        if end:
            try:
                e = datetime.strptime(str(end)[:10], '%Y-%m-%d').strftime('%Y%m31')
            except Exception:
                e = end
            rev_where += f" AND A.STATISTICS_DATE <= {e}"
        if shop_ids:
            rev_where += (f" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP B "
                          f"WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.SHOPTRADE = B.SHOPTRADE "
                          f"AND B.SERVERPARTSHOP_ID IN ({shop_ids}))")
        rev_sql = (f"SELECT SUBSTR(A.STATISTICS_DATE,1,6) AS STATISTICS_MONTH, "
                   f"SUM(REVENUE_AMOUNT_A) AS REVENUE_AMOUNT_A, "
                   f"SUM(REVENUE_AMOUNT_B) AS REVENUE_AMOUNT_B, "
                   f"COUNT(DISTINCT CASE WHEN REVENUE_AMOUNT_A <> 0 THEN STATISTICS_DATE END) AS COUNT_A, "
                   f"COUNT(DISTINCT CASE WHEN REVENUE_AMOUNT_B <> 0 THEN STATISTICS_DATE END) AS COUNT_B "
                   f"FROM T_REVENUEDAILY A WHERE A.REVENUEDAILY_STATE = 1{rev_where} "
                   f"GROUP BY SUBSTR(A.STATISTICS_DATE,1,6)")
        try:
            rev_rows = db.execute_query(rev_sql) or []
            for rv in rev_rows:
                revenue_map[str(rv.get("STATISTICS_MONTH", ""))] = rv
        except Exception:
            pass

    regions_order = ["东", "南", "西", "北"]
    opposite = {"东": "西", "西": "东", "南": "北", "北": "南"}

    result = []
    for stat_month, info in sorted(month_map.items(), key=lambda x: str(x[0])):
        section = {
            "SERVERPART_NAME": info["SERVERPART_NAME"],
            "STATISTICS_DATE": stat_month,
            "list": []
        }
        region_data = {}
        for r in info["rows"]:
            reg = r.get("SERVERPART_REGION", "")
            if reg not in region_data:
                region_data[reg] = r
        for reg in regions_order:
            if reg in region_data:
                row = dict(region_data[reg])
                month_key = str(stat_month).replace("-", "")
                if month_key in revenue_map:
                    rv = revenue_map[month_key]
                    count_f = "COUNT_A" if reg in ("东", "南") else "COUNT_B"
                    sum_f = "REVENUE_AMOUNT_A" if reg in ("东", "南") else "REVENUE_AMOUNT_B"
                    dc = float(rv.get(count_f, 0) or 0)
                    sa = float(rv.get(sum_f, 0) or 0)
                    row["REVENUE_AMOUNT"] = round(sa / dc, 2) if dc > 0 else sa
                section["list"].append({
                    "SERVERPART_REGION": reg,
                    "SERVERPART": row
                })
                if len(region_data) == 1 and opposite.get(reg):
                    section["list"].append({
                        "SERVERPART_REGION": opposite[reg],
                        "SERVERPART": {}
                    })
        result.append(section)

    return result, total


def get_bayonet_vehicle_analysis(db: DatabaseHelper, serverpart_id: str, rank_num: int = 10) -> dict:
    """
    分析服务区车流情况 — C# BigDataHelper.GetBayonetVehicleAnalysis
    """
    try:
        sql = """SELECT * FROM T_BAYONETANALYSIS
            WHERE SERVERPART_ID = ? AND BAYONETANALYSIS_STATE = 1
            ORDER BY BAYONETANALYSIS_ID DESC"""
        rows = db.execute_query(sql, [serverpart_id]) or []
        return {"data": rows[:rank_num], "total": len(rows)}
    except Exception as ex:
        logger.error(f"GetBayonetVehicleAnalysis 失败: {ex}")
        return {}


def get_time_interval_list(db: DatabaseHelper, **kwargs) -> list:
    """
    获取时段卡口车流统计 — C# BAYONETHelper.GetTimeIntervalModelList
    """
    try:
        stat_type = kwargs.get("StatisticsType", "0")
        sp_ids = kwargs.get("ServerPartIds", "")
        stat_month = kwargs.get("StatisticsMonth", "")
        vehicle_type = kwargs.get("VehicleType", "")
        data_type = kwargs.get("DataType", "")

        where_sql = ""
        if stat_month:
            where_sql += f" AND STATISTICS_MONTH = {stat_month}"
        if vehicle_type:
            where_sql += f" AND VEHICLE_TYPE = '{vehicle_type}'"
        if data_type:
            where_sql += f" AND DATA_TYPE = '{data_type}'"
        if sp_ids:
            where_sql += f" AND SERVERPART_ID IN ({sp_ids})"

        if str(stat_type).strip() == "0":
            sql = f"""SELECT ROUND(SUM(VEHICLE_COUNT)/MAX(STATISTICS_DAYS),2) AS VEHICLE_COUNT,
                STATISTICS_HOUR, DATA_TYPE
                FROM T_BAYONETHOURMONTH_AH A WHERE INOUT_TYPE=1{where_sql}
                GROUP BY STATISTICS_HOUR, DATA_TYPE"""
            return db.execute_query(sql) or []
        else:
            sql = f"""SELECT ROUND(SUM(VEHICLE_COUNT)/MAX(STATISTICS_DAYS),2) AS VEHICLE_COUNT,
                STATISTICS_HOUR, SERVERPART_ID, SERVERPART_NAME
                FROM T_BAYONETHOURMONTH_AH A WHERE DATA_TYPE<>2{where_sql}
                GROUP BY STATISTICS_HOUR, SERVERPART_ID, SERVERPART_NAME"""
            return db.execute_query(sql) or []
    except Exception as ex:
        logger.error(f"GetTimeIntervalList 失败: {ex}")
        return []


def get_bayonet_owner_ah_list(db: DatabaseHelper, **kwargs) -> list:
    """
    获取车辆归属地统计列表 — C# BAYONETOWNER_AHHelper.GetBayonetOwnerAHList
    查询视图 V_BAYONETOWNER_AH，支持 serverPartId/vehicleType/日期范围/searchKey+Value 模糊过滤/sortKey+sortStr 排序
    """
    server_part_id = kwargs.get("serverPartId") or kwargs.get("ServerpartIds", "")
    vehicle_type = kwargs.get("vehicleType", "")
    start_time = kwargs.get("statisticsStartTime", "")
    end_time = kwargs.get("statisticsEndTime", "")
    search_key = kwargs.get("searchKey", "")
    search_value = kwargs.get("searchValue", "")
    sort_key = kwargs.get("sortKey", "")
    sort_str = kwargs.get("sortStr", "")

    where_sql = ""
    if server_part_id:
        where_sql += f" AND SERVERPART_ID = {server_part_id}"
    if vehicle_type:
        where_sql += f" AND VEHICLE_TYPE = '{vehicle_type}'"
    if start_time:
        where_sql += f" AND STATISTICS_DATE >= {start_time}"
    if end_time:
        where_sql += f" AND STATISTICS_DATE <= {end_time}"
    # 模糊搜索（C# DataTable.DefaultView.RowFilter 模拟）
    if search_key and search_value:
        like_parts = [f"{k} LIKE '%{search_value}%'" for k in search_key.split(",") if k.strip()]
        if like_parts:
            where_sql += f" AND ({' OR '.join(like_parts)})"

    sql = f"""SELECT BAYONETOWNER_ID, SERVERPART_NAME, SERVERPART_REGION, VEHICLE_TYPE,
            LICENSE_PLATE, VEHICLE_COUNT, STAY_TIMES, AVGSTAY_TIMES, STATISTICS_DATE
        FROM V_BAYONETOWNER_AH WHERE 1=1{where_sql}"""
    # 排序
    if sort_key and sort_str:
        sql += f" ORDER BY {sort_key} {sort_str}"
    else:
        sql += " ORDER BY BAYONETOWNER_ID DESC"
    return db.execute_query(sql) or []


def get_bayonet_owner_month_ah_list(db: DatabaseHelper, **kwargs) -> list:
    """
    获取月度车辆停留统计列表 — C# BAYONETOWNERMONTH_AHHelper.GetBayonetOwnerMonthAHList
    查询视图 V_BAYONETOWNERMONTH_AH，支持同类参数，日期字段为 STATISTICS_MONTH (yyyyMM)
    """
    server_part_id = kwargs.get("serverPartId") or kwargs.get("ServerpartIds", "")
    vehicle_type = kwargs.get("vehicleType", "")
    start_month = kwargs.get("statisticsStartMonth", "")
    end_month = kwargs.get("statisticsEndMonth", "")
    search_key = kwargs.get("searchKey", "")
    search_value = kwargs.get("searchValue", "")
    sort_key = kwargs.get("sortKey", "")
    sort_str = kwargs.get("sortStr", "")

    where_sql = ""
    if server_part_id:
        where_sql += f" AND SERVERPART_ID = {server_part_id}"
    if vehicle_type:
        where_sql += f" AND VEHICLE_TYPE = '{vehicle_type}'"
    if start_month:
        where_sql += f" AND STATISTICS_MONTH >= {start_month}"
    if end_month:
        where_sql += f" AND STATISTICS_MONTH <= {end_month}"
    if search_key and search_value:
        like_parts = [f"{k} LIKE '%{search_value}%'" for k in search_key.split(",") if k.strip()]
        if like_parts:
            where_sql += f" AND ({' OR '.join(like_parts)})"

    sql = f"""SELECT SERVERPART_NAME, SERVERPART_REGION, VEHICLE_TYPE, LICENSE_PLATE,
            VEHICLE_COUNT, AVGVEHICLE_COUNT, STAY_TIMES, STAY_TIMESCOUNT, AVGSTAY_TIMES,
            STATISTICS_MONTH
        FROM V_BAYONETOWNERMONTH_AH WHERE 1=1{where_sql}"""
    if sort_key and sort_str:
        sql += f" ORDER BY {sort_key} {sort_str}"
    return db.execute_query(sql) or []


def get_urea_master_list(db: DatabaseHelper, operate_date: str, province_code: int,
                         serverpart_id: str = "", device_name: str = "") -> list:
    """
    获取尿素交易流水 — C# UREAMASTERHelper.GetUreaMasterList
    先查 T_SERVERPARTUREADEVICE JOIN T_SERVERPART 获取设备列表，
    再联查 T_UREAMASTER 获取指定日期的尿素交易流水
    """
    # 第一步：获取服务区下的尿素站点设备
    where_sql = " WHERE A.SERVERPART_ID = B.SERVERPART_ID"
    if province_code and province_code != 0:
        # C# 通过 DictionaryHelper.GetFieldEnum 获取 KeyID，这里直接使用 province_code
        where_sql += f" AND B.PROVINCE_CODE = {province_code}"
    if serverpart_id:
        where_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
    if device_name:
        where_sql += f" AND A.DEVICE_NAME = '{device_name}'"

    device_sql = f"""SELECT A.SERVERPARTUREADEVICE_ID, A.DEVICE_NAME, A.SERVERPART_ID,
        A.DEVICE, A.SERVERPART_NAME
        FROM T_SERVERPARTUREADEVICE A, T_SERVERPART B{where_sql}"""
    devices = db.execute_query(device_sql) or []
    if not devices:
        return []

    # 第二步：联查尿素交易明细
    device_names = [f"'{d.get('DEVICE_NAME', '')}'"
                    for d in devices if d.get('DEVICE_NAME')]
    if not device_names:
        return []

    # 日期格式化为 yyyy-MM-dd
    try:
        from datetime import datetime as _dt
        dt = _dt.strptime(str(operate_date)[:10], '%Y-%m-%d')
        date_str = dt.strftime('%Y-%m-%d')
    except Exception:
        date_str = operate_date

    urea_sql = f"""SELECT A.*, B.SERVERPART_NAME, B.SERVERPART_ID
        FROM T_UREAMASTER A, T_SERVERPARTUREADEVICE B
        WHERE A.DEVICE_NAME = B.DEVICE_NAME
          AND UREAMASTER_DATE = '{date_str}'
          AND A.DEVICE_NAME IN ({','.join(device_names)})"""
    return db.execute_query(urea_sql) or []
