from __future__ import annotations
# -*- coding: utf-8 -*-
"""
商品管理业务服务（CommodityController 专属）
对应 C# CommodityController.cs 中的非加密接口
使用 COMMODITYHelper.cs（GeneralMethod\BaseInfo\Commodity）

注意：与 BaseInfo 下已有的 commodity_service.py 不同！
  - BaseInfo 的 COMMODITY 接口查 V_WHOLE_COMMODITY 视图 (SaleCommodityHelper)
  - 本 Controller 的 COMMODITY 接口查 T_COMMODITY 表 (COMMODITYHelper)
  - 表名按省份拆分：DefaultPCode=620000 用 T_COMMODITY，其他用 T_COMMODITY_{ProvinceCode}
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper

# 甘肃默认省份编码（C# DefaultPCode = ConfigurationManager.AppSettings["PROVINCE_CODE"]）
DEFAULT_PROVINCE_CODE = "620000"
PRIMARY_KEY = "COMMODITY_ID"

# 字符串字段列表（NULL 转空字符串）
STR_FIELDS = [
    "COMMODITY_TYPE", "COMMODITY_CODE", "COMMODITY_NAME", "COMMODITY_BARCODE",
    "COMMODITY_ALLNAME", "COMMODITY_EN", "COMMODITY_UNIT", "COMMODITY_RULE",
    "COMMODITY_ORI", "COMMODITY_GRADE", "COMMODITY_DESC", "COMMODITY_SERVERCODE",
    "COMMODITY_HOTKEY", "COMMODITY_SYMBOL", "COMMODITY_BRAND"
]

# SearchParameter 中需要排除的字段（不直接用 GetWhereSQL 生成 WHERE）
EXCLUDE_FIELDS = {
    "COMMODITY_STATES", "SERVERPART_IDS", "BUSINESSTYPES",
    "OPERATE_DATE_Start", "OPERATE_DATE_End", "COMMODITY_IDS", "COMMODITY_TYPE"
}


def _get_table_name(province_code: str = "") -> str:
    """
    根据省份编码获取商品表名
    C# 逻辑：ProvinceCode == DefaultPCode || IsNullOrWhiteSpace(ProvinceCode) ? T_COMMODITY : T_COMMODITY_{ProvinceCode}
    """
    if not province_code or province_code.strip() == "" or province_code == DEFAULT_PROVINCE_CODE:
        return "T_COMMODITY"
    return f"T_COMMODITY_{province_code}"


def _format_date(val):
    """将日期格式从 ISO 转为 C# 风格: yyyy/M/d H:mm:ss"""
    if val is None:
        return None
    s = str(val)
    try:
        if 'T' in s:
            dt = datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
        elif '-' in s and len(s) >= 10:
            dt = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
        else:
            return s
        return f"{dt.year}/{dt.month}/{dt.day} {dt.hour}:{dt.minute:02d}:{dt.second:02d}"
    except Exception:
        return s


# 日期字段列表（需要格式化为 C# 风格）
# 注意：ADDTIME 是 DateTime 类型，C# 序列化保持 ISO 格式，不需要格式化
DATE_FIELDS = ["OPERATE_DATE"]


def _process_row(row: dict) -> dict:
    """处理单行数据：字符串 null→''、OPERATE_DATE 日期格式化"""
    for field in STR_FIELDS:
        if field in row and row[field] is None:
            row[field] = ""
    # 日期格式化
    for df in DATE_FIELDS:
        if df in row:
            row[df] = _format_date(row[df])
    return row


# ========== 1. GetCOMMODITYList ==========

def get_commodity_list(db: DatabaseHelper, search_param: dict,
                       province_code: str = "", sp_region_type_id: str = "",
                       serverpart_shop_id: str = "", user_defined_type_id: str = "",
                       show_just_udtype: bool = None,
                       keyword: dict = None,
                       page_index: int = 1, page_size: int = 10,
                       sort_str: str = "") -> tuple:
    """
    获取商品管理列表
    对应 C# COMMODITYHelper.GetCOMMODITYList

    C# 关键逻辑：
    1. WHERE 条件：COMMODITY_IDS, SERVERPART_IDS, BUSINESSTYPES, COMMODITY_STATES, COMMODITY_TYPE, OPERATE_DATE
    2. 甘肃(620000)特殊：合并统一定价商品（STATISTIC_TYPE=4000）
    3. keyWord 模糊查询
    """
    table_name = _get_table_name(province_code)
    where_sql = ""
    sp = search_param or {}

    # OPERATE_DATE 日期范围
    if sp.get("OPERATE_DATE_Start") and str(sp["OPERATE_DATE_Start"]).strip():
        date_start = str(sp["OPERATE_DATE_Start"]).split(" ")[0]
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}OPERATE_DATE >= TO_DATE('{date_start}','YYYY/MM/DD')"
    if sp.get("OPERATE_DATE_End") and str(sp["OPERATE_DATE_End"]).strip():
        date_end = str(sp["OPERATE_DATE_End"]).split(" ")[0]
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}OPERATE_DATE < TO_DATE('{date_end}','YYYY/MM/DD') + 1"

    # COMMODITY_IDS
    if sp.get("COMMODITY_IDS") and str(sp["COMMODITY_IDS"]).strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}COMMODITY_ID IN ({sp['COMMODITY_IDS']})"

    # SERVERPART_IDS（对应 C# searchModel.SearchParameter.SERVERPART_IDS）
    if sp.get("SERVERPART_IDS") and str(sp["SERVERPART_IDS"]).strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}SERVERPART_ID IN ({sp['SERVERPART_IDS']})"

    # BUSINESSTYPES
    if sp.get("BUSINESSTYPES") and str(sp["BUSINESSTYPES"]).strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}BUSINESSTYPE IN ({sp['BUSINESSTYPES']})"

    # COMMODITY_STATES
    if sp.get("COMMODITY_STATES") and str(sp["COMMODITY_STATES"]).strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}COMMODITY_STATE IN ({sp['COMMODITY_STATES']})"

    # COMMODITY_TYPE（简化，不含递归子类型）
    if sp.get("COMMODITY_TYPE") and str(sp["COMMODITY_TYPE"]).strip():
        type_ids = str(sp["COMMODITY_TYPE"]).replace(",", "','")
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}COMMODITY_TYPE IN ('{type_ids}')"

    # 片区内码
    if sp_region_type_id and sp_region_type_id.strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"""{prefix}EXISTS (SELECT 1 FROM T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.SPREGIONTYPE_ID IN ({sp_region_type_id}))"""

    # 指定门店
    if serverpart_shop_id and serverpart_shop_id.strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"""{prefix}EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
            WHERE A.SERVERPART_ID = C.SERVERPART_ID AND A.BUSINESSTYPE = C.SHOPTRADE AND
                C.SERVERPARTSHOP_ID IN ({serverpart_shop_id}))"""

    # 自定义类型
    if user_defined_type_id and user_defined_type_id.strip():
        prefix = " AND " if where_sql else " WHERE "
        where_sql += f"{prefix}USERDEFINEDTYPE_ID IN ({user_defined_type_id})"
    elif show_just_udtype is not None:
        prefix = " AND " if where_sql else " WHERE "
        if show_just_udtype:
            where_sql += f"{prefix}USERDEFINEDTYPE_ID IS NOT NULL"
        else:
            where_sql += f"{prefix}USERDEFINEDTYPE_ID IS NULL"

    base_sql = f"SELECT * FROM {table_name} A{where_sql}"

    # keyWord 模糊过滤
    if keyword and keyword.get("Key") and keyword.get("Value"):
        kw_parts = []
        for k in keyword["Key"].split(","):
            k = k.strip()
            if k:
                kw_parts.append(f"{k} LIKE '%{keyword['Value']}%'")
        if kw_parts:
            kw_filter = " OR ".join(kw_parts)
            if where_sql:
                base_sql += f" AND ({kw_filter})"
            else:
                base_sql += f" WHERE ({kw_filter})"

    # 排序
    if sort_str and sort_str.strip():
        base_sql += f" ORDER BY {sort_str}"

    # 总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 分页
    if page_index and page_size and page_size < 999999:
        start_row = (page_index - 1) * page_size + 1
        end_row = page_index * page_size
        paged_sql = f"""SELECT * FROM (
            SELECT A2.*, ROWNUM RN FROM ({base_sql}) A2
            WHERE ROWNUM <= {end_row}
        ) WHERE RN >= {start_row}"""
        rows = db.execute_query(paged_sql)
        for row in rows:
            row.pop("RN", None)
    else:
        rows = db.execute_query(base_sql)

    for row in rows:
        _process_row(row)

    return int(total_count), rows


# ========== 2. GetCOMMODITYDetail ==========

def get_commodity_detail(db: DatabaseHelper, commodity_id: int,
                          province_code: str = "") -> dict:
    """
    获取商品管理明细
    对应 C# COMMODITYHelper.GetCOMMODITYDetail(transaction, COMMODITYId, ProvinceCode)
    """
    table_name = _get_table_name(province_code)
    sql = f"SELECT * FROM {table_name} WHERE {PRIMARY_KEY} = {commodity_id}"
    rows = db.execute_query(sql)
    if rows:
        return _process_row(rows[0])
    return {}


# ========== 3. SynchroCOMMODITY ==========

def synchro_commodity(db: DatabaseHelper, data: dict, province_code: str = "") -> tuple:
    """
    同步商品管理（新增/更新）
    对应 C# COMMODITYHelper.SynchroCOMMODITY
    简化版：不含下发指令、不含自动生成编码/条码逻辑
    """
    table_name = _get_table_name(province_code)

    # 排除非表字段
    for f in list(EXCLUDE_FIELDS):
        data.pop(f, None)

    commodity_id = data.get("COMMODITY_ID")

    if commodity_id is not None:
        check_sql = f"SELECT COUNT(*) FROM {table_name} WHERE {PRIMARY_KEY} = {commodity_id}"
        count = db.execute_scalar(check_sql)
        if count == 0:
            return False, None

        set_parts = []
        for key, value in data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {commodity_id}"
            db.execute_non_query(update_sql)
    else:
        max_id = db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {table_name}")
        new_id = (max_id or 0) + 1
        data["COMMODITY_ID"] = new_id

        columns = []
        values = []
        for key, value in data.items():
            if value is None:
                continue
            columns.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

    return True, data


# ========== 4. DeleteCOMMODITY ==========

def delete_commodity(db: DatabaseHelper, commodity_id: int, province_code: str = "") -> bool:
    """
    删除商品管理（软删除）
    C# 逻辑：UPDATE T_COMMODITY SET COMMODITY_STATE = 0 WHERE COMMODITY_ID = ?
    """
    table_name = _get_table_name(province_code)
    sql = f"UPDATE {table_name} SET COMMODITY_STATE = 0 WHERE {PRIMARY_KEY} = {commodity_id}"
    affected = db.execute_non_query(sql)
    return affected > 0 if affected else False


# ========== 5. GetCommodityList (SearchType switch) ==========

def get_commodity_list_by_type(db: DatabaseHelper, search_type: int, province_code: int = None,
                                sp_region_type_id: str = "", serverpart_id: str = "",
                                serverpart_shop_id: str = "", shop_trade: str = "",
                                commodity_type_id: str = "", commodity_state: str = "",
                                user_defined_type_id: str = "", show_just_udtype: bool = None,
                                operate_date_start: str = "", operate_date_end: str = "",
                                search_key: str = "", search_value: str = "",
                                page_index: int = 1, page_size: int = 10,
                                sort_str: str = "") -> tuple:
    """
    获取商品信息列表（多种 SearchType 分支）
    对应 C# GetCommodityList 控制器方法

    SearchType:
      0 = 商品名称/条码/单价列表（CommodityBasicModel）
      1 = 商品标准信息列表（CommodityStdModel）
      2 = 商品标价签列表（CommodityLabelModel）
      其他 = 商品全字段列表（COMMODITYModel，走 GetCOMMODITYList）
    """
    if province_code is None:
        return -1, []

    pcode = str(province_code)
    table_suffix = "" if pcode == DEFAULT_PROVINCE_CODE else f"_{pcode}"

    # 公共 WHERE
    where_sql = ""
    shop_sql = ""
    if serverpart_id and serverpart_id.strip():
        where_sql += f" AND B.SERVERPART_ID IN ({serverpart_id})"
    if sp_region_type_id and sp_region_type_id.strip():
        where_sql += f" AND B.SPREGIONTYPE_ID IN ({sp_region_type_id})"
    if shop_trade and shop_trade.strip():
        where_sql += f" AND A.BUSINESSTYPE IN ({shop_trade})"
    if serverpart_shop_id and serverpart_shop_id.strip():
        shop_sql += f""" AND EXISTS (SELECT 1 FROM T_SERVERPARTSHOP C
            WHERE A.SERVERPART_ID = C.SERVERPART_ID AND A.BUSINESSTYPE = C.SHOPTRADE AND
                C.SERVERPARTSHOP_ID IN ({serverpart_shop_id}))"""

    if search_type == 0:
        sql = f"""SELECT MAX(A.COMMODITY_NAME) AS COMMODITY_NAME,
                A.COMMODITY_BARCODE, A.COMMODITY_RETAILPRICE
            FROM T_COMMODITY{table_suffix} A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND A.COMMODITY_STATE = 1
                AND B.STATISTIC_TYPE <> 4000{where_sql}{shop_sql}
            GROUP BY A.COMMODITY_BARCODE, A.COMMODITY_RETAILPRICE"""

    elif search_type == 1:
        sql = f"""SELECT A.COMMODITY_ID, A.COMMODITY_TYPE, A.COMMODITY_NAME,
                A.COMMODITY_BARCODE, A.COMMODITY_RETAILPRICE, A.BUSINESSTYPE,
                A.COMMODITY_STATE, A.OPERATE_DATE, B.SERVERPART_NAME
            FROM T_COMMODITY{table_suffix} A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
                AND B.STATISTIC_TYPE <> 4000{where_sql}{shop_sql}"""

    elif search_type == 2:
        sql = f"""SELECT A.COMMODITY_CODE, A.COMMODITY_NAME, A.COMMODITY_BARCODE,
                A.COMMODITY_EN, A.COMMODITY_UNIT, A.COMMODITY_RULE, A.COMMODITY_ORI,
                A.COMMODITY_RETAILPRICE, B.SERVERPART_NAME, A.OPERATE_DATE
            FROM T_COMMODITY{table_suffix} A, T_SERVERPART B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID
                AND B.STATISTIC_TYPE <> 4000{where_sql}{shop_sql}"""

    else:
        # 其他 SearchType: 走 GetCOMMODITYList 逻辑
        sp = {
            "SERVERPART_IDS": serverpart_id,
            "BUSINESSTYPES": shop_trade,
            "COMMODITY_TYPE": commodity_type_id,
            "COMMODITY_STATES": commodity_state,
            "OPERATE_DATE_Start": operate_date_start,
            "OPERATE_DATE_End": operate_date_end,
        }
        kw = {"Key": search_key, "Value": search_value} if search_key else None
        return get_commodity_list(
            db, sp, pcode, sp_region_type_id, serverpart_shop_id,
            user_defined_type_id, show_just_udtype,
            keyword=kw, page_index=page_index or 1, page_size=page_size or 10,
            sort_str=sort_str
        )

    # keyWord 模糊查询（SearchType 0/1/2）
    if search_key and search_key.strip():
        kw_parts = []
        for k in search_key.split(","):
            k = k.strip()
            if k:
                kw_parts.append(f"{k} LIKE '%{search_value}%'")
        if kw_parts:
            sql += f" AND ({' OR '.join(kw_parts)})"

    if sort_str and sort_str.strip():
        sql += f" ORDER BY {sort_str}"

    count_sql = f"SELECT COUNT(*) FROM ({sql})"
    total_count = db.execute_scalar(count_sql) or 0

    if page_index and page_size:
        start_row = (page_index - 1) * page_size + 1
        end_row = page_index * page_size
        paged_sql = f"""SELECT * FROM (
            SELECT A2.*, ROWNUM RN FROM ({sql}) A2
            WHERE ROWNUM <= {end_row}
        ) WHERE RN >= {start_row}"""
        rows = db.execute_query(paged_sql)
        for row in rows:
            row.pop("RN", None)
    else:
        rows = db.execute_query(sql)

    # SearchType=1 后处理：解析 COMMODITY_TYPE 名称、BUSINESSTYPE→BUSINESSTYPE_NAME
    if search_type == 1 and rows:
        # 查询商品类型表，将类型内码转为名称
        # C# T_COMMODITYTYPE.PROVINCE_CODE 存的是 FIELDENUM_ID（与 T_SERVERPART.PROVINCE_CODE 一致）
        # 从 T_SERVERPART 中直接获取该省份对应的 PROVINCE_CODE（FIELDENUM_ID）
        pcode_int = int(province_code) if province_code else 620000
        try:
            # 通过 T_FIELDEXPLAIN → T_FIELDENUM 将省份编码映射为 FIELDENUM_ID
            fe_sql = ("SELECT FIELDENUM_ID FROM T_FIELDENUM "
                      "WHERE FIELDEXPLAIN_ID = (SELECT FIELDEXPLAIN_ID FROM T_FIELDEXPLAIN WHERE FIELDEXPLAIN_FIELD = 'DIVISION_CODE') "
                      f"AND FIELDENUM_VALUE = '{pcode_int}'")
            fe_rows = db.execute_query(fe_sql)
            if fe_rows:
                province_enum_id = fe_rows[0]["FIELDENUM_ID"]
                ct_sql = f"SELECT COMMODITYTYPE_ID, COMMODITYTYPE_NAME FROM T_COMMODITYTYPE WHERE PROVINCE_CODE = {province_enum_id}"
                ct_rows = db.execute_query(ct_sql)
                ct_map = {str(int(r["COMMODITYTYPE_ID"])): r["COMMODITYTYPE_NAME"] for r in ct_rows} if ct_rows else {}
                logger.debug(f"COMMODITYTYPE: ProvinceCode={pcode_int}→ENUM_ID={province_enum_id}, 结果数={len(ct_rows) if ct_rows else 0}")
            else:
                logger.warning(f"COMMODITYTYPE: 找不到 ProvinceCode={pcode_int} 对应的 FIELDENUM_ID")
                ct_map = {}
        except Exception as e:
            logger.error(f"COMMODITYTYPE 查询异常: {e}")
            ct_map = {}
        # 查询业态字典，将业态内码转为名称
        # C# DictionaryHelper.GetDictionaryKeyValue(transaction, "BUSINESSTYPE")
        # 两步法：先查 T_FIELDEXPLAIN 获取 FIELDEXPLAIN_ID，再查 T_FIELDENUM 子枚举
        try:
            fe_rows = db.execute_query(
                "SELECT FIELDEXPLAIN_ID FROM T_FIELDEXPLAIN WHERE FIELDEXPLAIN_FIELD = 'BUSINESSTYPE'")
            if fe_rows:
                fe_id = fe_rows[0]["FIELDEXPLAIN_ID"]
                bt_rows = db.execute_query(
                    f"SELECT FIELDENUM_VALUE, FIELDENUM_NAME FROM T_FIELDENUM "
                    f"WHERE FIELDEXPLAIN_ID = {fe_id} AND FIELDENUM_STATUS > 0")
                bt_map = {str(r["FIELDENUM_VALUE"]): r["FIELDENUM_NAME"] for r in bt_rows} if bt_rows else {}
                logger.debug(f"BUSINESSTYPE: FIELDEXPLAIN_ID={fe_id}, 结果数={len(bt_rows) if bt_rows else 0}")
            else:
                logger.warning("BUSINESSTYPE: T_FIELDEXPLAIN 未找到 BUSINESSTYPE 记录")
                bt_map = {}
        except Exception as e:
            logger.error(f"BUSINESSTYPE 字典查询异常: {e}")
            bt_map = {}
        for row in rows:
            # COMMODITY_TYPE: 内码→名称
            ct_id = str(row.get("COMMODITY_TYPE") or "").strip()
            if ct_id and ct_id in ct_map:
                row["COMMODITY_TYPE"] = ct_map[ct_id]
            # BUSINESSTYPE→BUSINESSTYPE_NAME
            bt_val = str(row.get("BUSINESSTYPE") or "").strip()
            row["BUSINESSTYPE_NAME"] = bt_map.get(bt_val)
            row.pop("BUSINESSTYPE", None)  # C# CommodityStdModel 没有 BUSINESSTYPE 字段，只有 BUSINESSTYPE_NAME
            # OPERATE_DATE 格式化
            if "OPERATE_DATE" in row:
                row["OPERATE_DATE"] = _format_date(row["OPERATE_DATE"])
    elif search_type == 2 and rows:
        for row in rows:
            if "OPERATE_DATE" in row:
                row["OPERATE_DATE"] = _format_date(row["OPERATE_DATE"])

    return int(total_count), rows


# ========== 6. SyncCommodityInfo_AHJG ==========

def sync_commodity_info_ahjg(db: DatabaseHelper, last_time: str) -> bool:
    """
    更新安徽建工待审核商品数据
    对应 C# COMMODITYHelper.SyncCommodityInfo_AHJG(transaction, LastTime)
    注意：C# 逻辑较复杂，此处简化为占位实现
    """
    logger.info(f"SyncCommodityInfo_AHJG called with LastTime={last_time}")
    return True
