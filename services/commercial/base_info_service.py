# -*- coding: utf-8 -*-
from __future__ import annotations

from services.commercial.service_utils import (
    safe_float as _sf,
    safe_int as _si,
)

# -*- coding: utf-8 -*-
"""
CommercialApi - 基础信息业务服务
从 base_info_router.py 中抽取的 SQL 和业务逻辑（996 行 → Service）
"""
from typing import Optional
from collections import defaultdict
from core.database import DatabaseHelper
from routers.deps import parse_multi_ids, build_in_condition


def _to_bool(v):
    if v is None: return False
    try: return float(v) > 0
    except: return False


# ===== 1. 片区列表 =====
def get_sp_region_list(db: DatabaseHelper, province_code: str) -> list[dict]:
    sql = """SELECT TYPE_NAME, SERVERPARTTYPE_ID FROM T_SERVERPARTTYPE
        WHERE SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = ? ORDER BY TYPE_INDEX"""
    rows = db.execute_query(sql, [province_code])
    return [{"name": r.get("TYPE_NAME", ""), "value": str(r.get("SERVERPARTTYPE_ID", ""))} for r in rows]


# ===== 2/3. 经营业态列表 =====
def get_business_trade_list_get(db: DatabaseHelper, push_province_code, bt_id, bt_name, bt_pid, bt_pname) -> list[dict]:
    where_sql, params = "", []
    if push_province_code:
        where_sql += " AND B.PROVINCE_CODE = ?"; params.append(push_province_code)
    if bt_id is not None:
        where_sql += " AND A.AUTOSTATISTICS_ID = ?"; params.append(bt_id)
    if bt_name:
        where_sql += " AND A.AUTOSTATISTICS_NAME = ?"; params.append(bt_name)
    if bt_pid is not None:
        where_sql += " AND B.AUTOSTATISTICS_ID = ?"; params.append(bt_pid)
    if bt_pname:
        where_sql += " AND B.AUTOSTATISTICS_NAME = ?"; params.append(bt_pname)

    sql = f"""SELECT A.AUTOSTATISTICS_NAME, B.AUTOSTATISTICS_NAME AS AUTOSTATISTICS_PNAME
        FROM T_AUTOSTATISTICS A, T_AUTOSTATISTICS B
        WHERE A.AUTOSTATISTICS_PID = B.AUTOSTATISTICS_ID AND A.AUTOSTATISTICS_TYPE = 2000{where_sql}"""
    rows = db.execute_query(sql, params if params else None)
    return [{"BUSINESSTRADE_NAME": r.get("AUTOSTATISTICS_NAME"), "BUSINESSTRADE_PNAME": r.get("AUTOSTATISTICS_PNAME"),
             "BUSINESSTRADE_INDEX": None, "BUSINESSTRADE_ICO": None, "BUSINESSTRADE_STATE": None,
             "OWNERUNIT_ID": None, "OWNERUNIT_NAME": None, "PROVINCE_CODE": None,
             "OPERATE_DATE": None, "BUSINESSTRADE_DESC": None} for r in rows]


def get_business_trade_list_post(db: DatabaseHelper, search_model: dict) -> tuple[int, list[dict]]:
    search_model = search_model or {}
    page_index = int(search_model.get("PageIndex", 0) or 0)
    page_size = int(search_model.get("PageSize", 0) or 0)
    sort_str = search_model.get("SortStr", "")

    sql = """SELECT A.AUTOSTATISTICS_NAME, A.AUTOSTATISTICS_VALUE, A.AUTOSTATISTICS_INDEX,
            A.AUTOSTATISTICS_ICO, A.OWNERUNIT_ID, A.OWNERUNIT_NAME, A.PROVINCE_CODE,
            A.AUTOSTATISTICS_STATE, A.OPERATE_DATE, A.AUTOSTATISTICS_DESC,
            B.AUTOSTATISTICS_NAME AS AUTOSTATISTICS_PNAME
        FROM T_AUTOSTATISTICS A, T_AUTOSTATISTICS B
        WHERE A.AUTOSTATISTICS_PID = B.AUTOSTATISTICS_ID AND A.AUTOSTATISTICS_TYPE = 2000"""
    if sort_str:
        sql += f" ORDER BY {sort_str}"
    rows = db.execute_query(sql)
    total = len(rows)

    if page_size > 0 and page_index > 0:
        start = page_size * (page_index - 1)
        rows = rows[start:start + page_size]
    else:
        rows = []

    trade_list = [{"BUSINESSTRADE_NAME": r.get("AUTOSTATISTICS_NAME"), "BUSINESSTRADE_PNAME": r.get("AUTOSTATISTICS_PNAME"),
                   "BUSINESSTRADE_INDEX": r.get("AUTOSTATISTICS_INDEX"), "BUSINESSTRADE_ICO": r.get("AUTOSTATISTICS_ICO"),
                   "BUSINESSTRADE_STATE": r.get("AUTOSTATISTICS_STATE"), "OWNERUNIT_ID": r.get("OWNERUNIT_ID"),
                   "OWNERUNIT_NAME": r.get("OWNERUNIT_NAME"), "PROVINCE_CODE": r.get("PROVINCE_CODE"),
                   "OPERATE_DATE": r.get("OPERATE_DATE"), "BUSINESSTRADE_DESC": r.get("AUTOSTATISTICS_DESC")} for r in rows]
    return total, trade_list


# ===== 8. 品牌分析 =====
def get_brand_analysis(db: DatabaseHelper, province_code, serverpart_id, business_trade_ids, brand_type, show_all) -> dict:
    where_sql = ""
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids:
        where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')
    elif province_code:
        fe_rows = db.execute_query(f"""SELECT "FIELDENUM_ID" FROM "T_FIELDENUM"
            WHERE "FIELD_NAME" = 'DIVISION_CODE' AND "FIELDENUM_VALUE" = '{province_code}'""") or []
        if fe_rows:
            where_sql += f' AND A."PROVINCE_CODE" = {fe_rows[0].get("FIELDENUM_ID")}'
    if business_trade_ids:
        where_sql += f' AND A."BUSINESS_TRADE" IN ({business_trade_ids})'
    if brand_type:
        where_sql += f' AND B."BRAND_TYPE" IN ({brand_type})'

    show_all_sql = "" if show_all else ' AND A."BUSINESS_STATE" = 1000'
    sql = f"""SELECT A."SERVERPARTSHOP_ID", A."SERVERPART_ID", A."SHOPSHORTNAME",
            A."BUSINESS_STATE", A."BUSINESS_BRAND", A."BUSINESS_TRADE",
            A."BUSINESS_DATE", B."BRAND_NAME", B."BRAND_TYPE", B."BRAND_INTRO"
        FROM "T_SERVERPARTSHOP" A LEFT JOIN "T_BRAND" B ON A."BUSINESS_BRAND" = B."BRAND_ID"
        WHERE A."ISVALID" = 1{where_sql}{show_all_sql}
        ORDER BY A."SERVERPART_ID", A."BUSINESS_TRADE" """
    rows = db.execute_query(sql) or []

    # 品牌标签
    brand_tag_set = {str(r.get("BRAND_TYPE")): True for r in rows if r.get("BRAND_TYPE") is not None}
    brand_tag, type_name_map = [], {}
    try:
        enum_rows = db.execute_query("""SELECT E."FIELDENUM_VALUE", E."FIELDENUM_NAME" FROM "T_FIELDENUM" E
            JOIN "T_FIELDEXPLAIN" F ON E."FIELDEXPLAIN_ID" = F."FIELDEXPLAIN_ID"
            WHERE F."FIELDEXPLAIN_FIELD" = 'BRAND_TYPE' ORDER BY E."FIELDENUM_VALUE" """)
        for er in (enum_rows or []):
            ev = str(er.get("FIELDENUM_VALUE", ""))
            type_name_map[ev] = er.get("FIELDENUM_NAME", "")
            if ev in brand_tag_set:
                brand_tag.append({"name": er.get("FIELDENUM_NAME", ""), "value": ev})
    except: pass

    shop_brand_list = []
    for r in rows:
        bt = str(r.get("BRAND_TYPE", "") or "")
        shop_brand_list.append({
            "Brand_Id": _si(r.get("BUSINESS_BRAND")), "Brand_Name": r.get("BRAND_NAME"),
            "BrandType_Name": type_name_map.get(bt, ""), "Brand_ICO": r.get("BRAND_INTRO"),
            "ServerpartShop_Id": _si(r.get("SERVERPARTSHOP_ID")),
            "Bussiness_Time": str(r.get("BUSINESS_DATE", "") or ""),
            "Bussiness_Name": r.get("SHOPSHORTNAME"), "Bussiness_State": _si(r.get("BUSINESS_STATE")),
            "CurRevenue": None, "Revenue_Amount": None, "Business_Trade": _si(r.get("BUSINESS_TRADE")),
            "Business_TradeICO": None, "Business_TradeId": _si(r.get("BUSINESS_TRADE")),
            "ShopEndaccountList": None,
        })
    return {"BrandTag": brand_tag, "ShopBrandList": shop_brand_list}


# ===== 9. 服务区列表 =====
def get_serverpart_list(db: DatabaseHelper, province_code, sp_region_type_id, serverpart_name,
                        serverpart_type, serverpart_id_cur, page_index, page_size) -> tuple[list[dict], int]:
    conditions = ["A.STATISTICS_TYPE = 1000", "A.SERVERPART_CODE NOT IN ('340001','530590')"]
    params = {}
    if sp_region_type_id:
        conditions.append(f"A.SPREGIONTYPE_ID IN ({sp_region_type_id})")
    elif province_code:
        pcode_rows = db.execute_query("SELECT FIELDENUM_ID FROM T_FIELDENUM WHERE FIELDENUM_VALUE = :pc AND ROWNUM = 1", {"pc": province_code})
        if pcode_rows:
            conditions.append("A.PROVINCE_CODE = :pcode"); params["pcode"] = pcode_rows[0]["FIELDENUM_ID"]
    if serverpart_type:
        conditions.append(f"A.SERVERPART_TYPE IN ({serverpart_type})")
    if serverpart_name:
        conditions.append("A.SERVERPART_NAME LIKE :sp_name"); params["sp_name"] = f"%{serverpart_name}%"

    where_sql = " AND ".join(conditions)
    sql = f"""SELECT A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
            A.PROVINCE_CODE, A.SERVERPART_TYPE, A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME,
            A.SPREGIONTYPE_INDEX, A.STATISTICS_TYPE, A.OWNERUNIT_ID, A.OWNERUNIT_NAME,
            A.OPERATE_DATE, A.SERVERPART_X, A.SERVERPART_Y, A.SERVERPART_TEL,
            SUM(NVL(C.HASMOTHER,0)) AS HASMOTHER, SUM(NVL(C.HASPILOTLOUNGE,0)) AS HASPILOTLOUNGE,
            SUM(NVL(C.LIVESTOCKPACKING,0)) AS HASCHARGE, SUM(NVL(C.POINTCONTROLCOUNT,0)) AS HASGUESTROOM
        FROM T_SERVERPART A LEFT JOIN T_SERVERPARTINFO C ON A.SERVERPART_ID = C.SERVERPART_ID
        WHERE {where_sql}
        GROUP BY A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
            A.PROVINCE_CODE, A.SERVERPART_TYPE, A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME,
            A.SPREGIONTYPE_INDEX, A.STATISTICS_TYPE, A.OWNERUNIT_ID, A.OWNERUNIT_NAME,
            A.OPERATE_DATE, A.SERVERPART_X, A.SERVERPART_Y, A.SERVERPART_TEL
        ORDER BY A.SERVERPART_INDEX"""
    rows = db.execute_query(sql, params)

    if page_index and page_size:
        start = (page_index - 1) * page_size
        rows = rows[start:start + page_size]

    # 批量查 RT 表
    sp_ids = [str(r.get("SERVERPART_ID")) for r in rows if r.get("SERVERPART_ID")]
    rt_map = {}
    if sp_ids:
        rt_rows = db.execute_query(f'SELECT * FROM "T_RTSERVERPART" WHERE "SERVERPART_ID" IN ({",".join(sp_ids)})')
        for rt in (rt_rows or []):
            rt_map[rt.get("SERVERPART_ID")] = rt

    for r in rows:
        r["ISCUR_SERVERPART"] = 0; r["ImageLits"] = []; r["SERVERPART_DISTANCE"] = 0.0
        r.setdefault("LoadBearing_Id", None); r.setdefault("LoadBearing_State", None)
        r.setdefault("STARTDATE", None); r.setdefault("RegionInfo", None)
        r["tmwWeatherModel"] = None; r["weatherModel"] = None
        r["HASMOTHER"] = _to_bool(r.get("HASMOTHER")); r["HASPILOTLOUNGE"] = _to_bool(r.get("HASPILOTLOUNGE"))
        r["HASCHARGE"] = _to_bool(r.get("HASCHARGE")); r["HASGUESTROOM"] = _to_bool(r.get("HASGUESTROOM"))
        rt = rt_map.get(r.get("SERVERPART_ID"))
        if rt:
            r["SERVERPART_X"] = _sf(rt.get("SERVERPART_X")) or _sf(r.get("SERVERPART_X"))
            r["SERVERPART_Y"] = _sf(rt.get("SERVERPART_Y")) or _sf(r.get("SERVERPART_Y"))
            r["SERVERPART_ADDRESS"] = rt.get("SERVERPART_ADDRESS", "")
            r["ServerpartInfo"] = _build_sp_info(r, rt)
        else:
            r["SERVERPART_X"] = _sf(r.get("SERVERPART_X"))
            r["SERVERPART_Y"] = _sf(r.get("SERVERPART_Y"))
            r.setdefault("SERVERPART_ADDRESS", None)
            r["ServerpartInfo"] = _build_sp_info_empty(r)

    return rows, len(rows)


def _build_sp_info(r, rt):
    return {
        "SERVERPART_ID": r.get("SERVERPART_ID"), "RTSERVERPART_ID": rt.get("RTSERVERPART_ID"),
        "SERVERPART_ADDRESS": rt.get("SERVERPART_ADDRESS"),
        "SERVERPART_X": _sf(rt.get("SERVERPART_X")), "SERVERPART_Y": _sf(rt.get("SERVERPART_Y")),
        "SERVERPART_TEL": rt.get("SERVERPART_TEL"), "SERVERPART_AREA": _sf(rt.get("SERVERPART_AREA")),
        "SERVERPART_INFO": rt.get("SERVERPART_INFO"), "SERVERPART_TARGET": rt.get("SERVERPART_TARGET"),
        "STARTDATE": rt.get("STARTDATE"), "CENTERSTAKE_NUM": rt.get("CENTERSTAKE_NUM"),
        "EXPRESSWAY_NAME": rt.get("EXPRESSWAY_NAME"), "FLOORAREA": _sf(rt.get("FLOORAREA")),
        "BUSINESSAREA": _sf(rt.get("BUSINESSAREA")), "SHAREAREA": _sf(rt.get("SHAREAREA")),
        "BUSINESS_REGION": rt.get("BUSINESS_REGION"), "MANAGERCOMPANY": rt.get("MANAGERCOMPANY"),
        "OWNEDCOMPANY": rt.get("OWNEDCOMPANY"), "SELLERCOUNT": rt.get("SELLERCOUNT"),
        "TAXPAYER_IDENTIFYCODE": rt.get("TAXPAYER_IDENTIFYCODE"),
        "SEWAGEDISPOSAL_TYPE": rt.get("SEWAGEDISPOSAL_TYPE"), "WATERINTAKE_TYPE": rt.get("WATERINTAKE_TYPE"),
    }


def _build_sp_info_empty(r):
    return {
        "SERVERPART_ID": r.get("SERVERPART_ID"), "RTSERVERPART_ID": None,
        "SERVERPART_ADDRESS": None, "SERVERPART_X": _sf(r.get("SERVERPART_X")),
        "SERVERPART_Y": _sf(r.get("SERVERPART_Y")), "SERVERPART_TEL": r.get("SERVERPART_TEL"),
        "SERVERPART_AREA": None, "SERVERPART_INFO": None, "SERVERPART_TARGET": None,
        "STARTDATE": None, "CENTERSTAKE_NUM": None, "EXPRESSWAY_NAME": None,
        "FLOORAREA": None, "BUSINESSAREA": None, "SHAREAREA": None,
        "BUSINESS_REGION": None, "MANAGERCOMPANY": None, "OWNEDCOMPANY": None,
        "SELLERCOUNT": None, "TAXPAYER_IDENTIFYCODE": None, "SEWAGEDISPOSAL_TYPE": None, "WATERINTAKE_TYPE": None,
    }


# ===== 10. 服务区详情 =====
def get_serverpart_info(db: DatabaseHelper, serverpart_id: int) -> Optional[dict]:
    sql = "SELECT * FROM T_SERVERPART WHERE SERVERPART_ID = :id"
    rows = db.execute_query(sql, {"id": serverpart_id})
    if not rows:
        return None
    sp = rows[0]

    bt_name_map = {}
    try:
        bt_rows = db.execute_query("""SELECT E."FIELDENUM_VALUE", E."FIELDENUM_NAME" FROM "T_FIELDENUM" E
            JOIN "T_FIELDEXPLAIN" F ON E."FIELDEXPLAIN_ID" = F."FIELDEXPLAIN_ID"
            WHERE F."FIELDEXPLAIN_FIELD" = 'BUSINESSTYPE' """)
        bt_name_map = {str(r.get("FIELDENUM_VALUE", "")): r.get("FIELDENUM_NAME", "") for r in (bt_rows or [])}
    except: pass

    result = {k: (_si(sp.get(k)) if k.endswith("_ID") or k.endswith("_INDEX") or k.endswith("_TYPE") or k == "PROVINCE_CODE"
                   else _sf(sp.get(k)) if k in ("SERVERPART_X", "SERVERPART_Y")
                   else sp.get(k, ""))
              for k in ["SERVERPART_ID", "SERVERPART_NAME", "SERVERPART_TEL", "SERVERPART_ADDRESS",
                        "SERVERPART_INDEX", "PROVINCE_CODE", "SERVERPART_CODE", "SERVERPART_TYPE",
                        "SPREGIONTYPE_ID", "SPREGIONTYPE_NAME", "SPREGIONTYPE_INDEX", "OWNERUNIT_ID",
                        "OWNERUNIT_NAME", "SERVERPART_X", "SERVERPART_Y"]}
    result["STATISTICS_TYPE"] = str(sp.get("STATISTICS_TYPE", "") or "")

    # RT 扩展
    rt_rows = db.execute_query("SELECT * FROM T_RTSERVERPART WHERE SERVERPART_ID = :id", {"id": serverpart_id})
    if rt_rows:
        rt = rt_rows[0]
        for k in ["SERVERPART_X", "SERVERPART_Y", "SERVERPART_AREA", "FLOORAREA", "BUSINESSAREA", "SHAREAREA"]:
            rt[k] = _sf(rt.get(k))
        for k in ["SERVERPART_ID", "RTSERVERPART_ID", "SELLERCOUNT"]:
            rt[k] = _si(rt.get(k))
        result["ServerpartInfo"] = rt
        if rt.get("SERVERPART_X") is not None: result["SERVERPART_X"] = rt["SERVERPART_X"]
        if rt.get("SERVERPART_Y") is not None: result["SERVERPART_Y"] = rt["SERVERPART_Y"]

    # 设施信息
    info_rows = db.execute_query("SELECT * FROM T_SERVERPARTINFO WHERE SERVERPART_ID = :id", {"id": serverpart_id})
    if info_rows:
        result["HASMOTHER"] = any(float(r.get("HASMOTHER", 0) or 0) > 0 for r in info_rows)
        result["HASPILOTLOUNGE"] = any(float(r.get("HASPILOTLOUNGE", 0) or 0) > 0 for r in info_rows)
        result["HASCHARGE"] = any(float(r.get("LIVESTOCKPACKING", 0) or 0) > 0 for r in info_rows)
        result["HASGUESTROOM"] = any(float(r.get("POINTCONTROLCOUNT", 0) or 0) > 0 for r in info_rows)
        for ri in info_rows:
            for k in ["BUILDINGAREA", "FLOORAREA", "PARKINGAREA", "GREENSPACEAREA"]:
                ri[k] = _sf(ri.get(k))
            for k in ["TOILETCOUNT", "SMALLPARKING", "PACKING", "TRUCKPACKING"]:
                ri[k] = _si(ri.get(k))
            bt_val = str(ri.get("BUSINESSTYPE", "") or "")
            ri["BUSINESSTYPE"] = bt_name_map.get(bt_val, bt_val)
            ri.setdefault("REPAIR_TIME", None)
        result["RegionInfo"] = info_rows
    _fill_sp_defaults(result)
    return result


def _fill_sp_defaults(result):
    result["ISCUR_SERVERPART"] = 0; result["ImageLits"] = []
    result.setdefault("LoadBearing_Id", None); result.setdefault("LoadBearing_State", None)
    result.setdefault("OPERATE_DATE", None); result["SERVERPART_DISTANCE"] = 0.0
    result.setdefault("STARTDATE", None); result["tmwWeatherModel"] = None; result["weatherModel"] = None
    if "RegionInfo" in result and isinstance(result["RegionInfo"], list):
        _ckm = {"data": None, "key": None, "name": None, "value": None}
        for ri in result["RegionInfo"]:
            for k in ["SERVERPART_REGIONNAME", "SPRegionTypeId", "SPRegionTypeIndex", "ServerPartIndex", "TreeNodeName", "TreeNodePName"]:
                ri.setdefault(k, None)
            ri.setdefault("ImgList", [_ckm])
    else:
        result["RegionInfo"] = [{"SERVERPART_REGIONNAME": None, "SPRegionTypeId": None,
            "SPRegionTypeIndex": None, "ServerPartIndex": None,
            "TreeNodeName": None, "TreeNodePName": None,
            "ImgList": [{"data": None, "key": None, "name": None, "value": None}]}]


# ===== 11. 服务区树 =====
def get_server_info_tree(db: DatabaseHelper, province_code, sp_region_type_id,
                         serverpart_ids, serverpart_codes) -> list[dict]:
    if serverpart_codes:
        codes_in = ",".join([f"'{c.strip()}'" for c in serverpart_codes.split(",") if c.strip()])
        id_rows = db.execute_query(
            f'SELECT LISTAGG(CAST("SERVERPART_ID" AS VARCHAR),\',\') WITHIN GROUP(ORDER BY "SERVERPART_ID") AS IDS FROM "T_SERVERPART" WHERE "SERVERPART_CODE" IN ({codes_in})')
        if id_rows and id_rows[0].get("IDS"):
            code_ids = id_rows[0]["IDS"]
            if serverpart_ids:
                set1 = set(code_ids.split(",")); set2 = set(serverpart_ids.split(","))
                serverpart_ids = ",".join(set1 & set2)
            else:
                serverpart_ids = code_ids
    else:
        return []

    where_parts = ["1=1"]
    if sp_region_type_id: where_parts.append(f'"SPREGIONTYPE_ID" IN ({sp_region_type_id})')
    if serverpart_ids: where_parts.append(f'"SERVERPART_ID" IN ({serverpart_ids})')
    sp_rows = db.execute_query(f'SELECT * FROM "T_SERVERPART" WHERE {" AND ".join(where_parts)}')
    if not sp_rows:
        return []

    sp_map = {r.get("SERVERPART_ID"): r for r in sp_rows}
    sp_id_list = ",".join([str(sid) for sid in sp_map.keys()])
    info_rows = db.execute_query(
        f'SELECT * FROM "T_SERVERPARTINFO" WHERE "SERVERPART_ID" IN ({sp_id_list}) AND "SERVERPART_REGION" IS NOT NULL')

    INT_FIELDS = ["TOILETCOUNT","SMALLPARKING","PACKING","TRUCKPACKING","LONGPACKING","DANPACKING",
        "LIVESTOCKPACKING","DININGROOMCOUNT","POINTCONTROLCOUNT","DININGBXCOUNT","MICROWAVEOVEN",
        "WASHERCOUNT","SLEEPINGPODS","REFUELINGGUN92","REFUELINGGUN95","REFUELINGGUN0",
        "STATEGRIDCHARGE","LIAUTOCHARGE","GACENERGYCHARGE","OTHERCHARGE"]
    SHORT_FIELDS = ["HASMOTHER","HASPILOTLOUNGE","HASPANTRY","HASWIFI","HASTHIRDTOILETS","HASCHILD",
        "HASSHOWERROOM","HASWATERROOM","VEHICLEWATERFILLING","HASBACKGROUNDRADIO","HASMESSAGESEARCH"]
    DEC_FIELDS = ["GREENSPACEAREA","FLOORAREA","PARKINGAREA","BUILDINGAREA"]

    info_nodes = []
    for r in (info_rows or []):
        sp_id = r.get("SERVERPART_ID"); sp = sp_map.get(sp_id, {})
        node = {"SERVERPART_ID": sp_id, "TreeNodeName": r.get("SERVERPART_REGION", ""),
                "TreeNodePName": sp.get("SERVERPART_NAME", ""), "BUSINESSTYPE": str(r.get("BUSINESSTYPE", "") or "")}
        for f in INT_FIELDS + SHORT_FIELDS: node[f] = _si(r.get(f))
        for f in DEC_FIELDS: node[f] = _sf(r.get(f))
        info_nodes.append({"node": node, "children": []})

    # 按服务区分组
    sp_groups = defaultdict(list)
    for item in info_nodes:
        sp_groups[item["node"]["SERVERPART_ID"]].append(item)

    def _sum(items, f):
        vals = [it["node"].get(f) for it in items if it["node"].get(f) is not None]
        return sum(vals) if vals else None

    sp_nesting = []
    for sp_id, children in sp_groups.items():
        sp = sp_map.get(sp_id, {})
        node = {"SERVERPART_ID": sp_id, "TreeNodeName": sp.get("SERVERPART_NAME", ""),
                "TreeNodePName": sp.get("SPREGIONTYPE_NAME", ""),
                "SPRegionTypeId": sp.get("SPREGIONTYPE_ID"), "ServerPartIndex": _si(sp.get("SERVERPART_INDEX"))}
        for f in INT_FIELDS + SHORT_FIELDS + DEC_FIELDS: node[f] = _sum(children, f)
        sp_nesting.append({"node": node, "children": sorted(children, key=lambda x: str(x["node"].get("TreeNodeName", "")))})

    # 按片区分组
    rg = defaultdict(list); no_rg = []
    for item in sp_nesting:
        rid = item["node"].get("SPRegionTypeId")
        (rg[rid] if rid is not None else no_rg).append(item)

    result_list = []
    for rid, sp_items in rg.items():
        sp = next((r for r in sp_rows if r.get("SPREGIONTYPE_ID") == rid), None)
        node = {"TreeNodeName": sp.get("SPREGIONTYPE_NAME", "") if sp else "", "TreeNodePName": "",
                "SPRegionTypeId": rid, "SPRegionTypeIndex": _si(sp.get("SPREGIONTYPE_INDEX")) if sp else None}
        for f in INT_FIELDS + SHORT_FIELDS + DEC_FIELDS: node[f] = _sum(sp_items, f)
        result_list.append({"node": node, "children": sorted(sp_items, key=lambda x: x["node"].get("ServerPartIndex") or 0)})
    result_list.sort(key=lambda x: x["node"].get("SPRegionTypeIndex") or 0)
    result_list.extend(no_rg)
    return result_list


# ===== 12. 设施汇总 =====
def get_serverpart_service_summary(db: DatabaseHelper, province_code, sp_region_type_id, serverpart_id) -> Optional[dict]:
    province_key = province_code
    try:
        key_rows = db.execute_query(f"""SELECT E."FIELDENUM_ID" FROM "T_FIELDENUM" E
            JOIN "T_FIELDEXPLAIN" F ON E."FIELDEXPLAIN_ID" = F."FIELDEXPLAIN_ID"
            WHERE F."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND E."FIELDENUM_VALUE" = '{province_code}'""")
        if key_rows: province_key = str(key_rows[0].get("FIELDENUM_ID", province_code))
    except: pass

    where_sql = f' AND A."PROVINCE_CODE" = {province_key}'
    if sp_region_type_id: where_sql += f' AND A."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
    _sp_ids = parse_multi_ids(serverpart_id)
    if _sp_ids: where_sql += ' AND ' + build_in_condition('SERVERPART_ID', _sp_ids).replace('"SERVERPART_ID"', 'A."SERVERPART_ID"')

    sql = f"""SELECT A."SERVERPART_ID", A."SERVERPART_NAME",
            COALESCE(SUM(C."FLOORAREA"),0) AS "FLOORAREA", COALESCE(SUM(C."PARKINGAREA"),0) AS "PARKINGAREA",
            COALESCE(SUM(C."BUILDINGAREA"),0) AS "BUILDINGAREA", COALESCE(SUM(C."HASGASSTATION"),0) AS "HASGASSTATION",
            COALESCE(SUM(C."LIVESTOCKPACKING"),0) AS "HASCHARGESTATION",
            COALESCE(SUM(C."SMALLPARKING"),0) AS "SMALLPARKING", COALESCE(SUM(C."PACKING"),0) AS "PACKING",
            COALESCE(SUM(C."TRUCKPACKING"),0) AS "TRUCKPACKING", COALESCE(SUM(C."LONGPACKING"),0) AS "LONGPACKING",
            COALESCE(SUM(C."DANPACKING"),0) AS "DANPACKING",
            COALESCE(SUM(C."HASCHILD"),0) AS "HASAUTOREPAIR", COALESCE(SUM(C."HASRESTROOM"),0) AS "HASRESTROOM",
            COALESCE(SUM(C."HASPILOTLOUNGE"),0) AS "HASPILOTLOUNGE", COALESCE(SUM(C."HASMOTHER"),0) AS "HASMOTHER",
            COALESCE(SUM(C."HASBACKGROUNDRADIO"),0) AS "HASSTORE",
            COALESCE(SUM(C."DININGROOMCOUNT"),0) AS "DININGROOMCOUNT",
            COALESCE(SUM(C."HASMESSAGESEARCH"),0) AS "HASLODGING",
            COALESCE(SUM(C."VEHICLEWATERFILLING"),0) AS "VEHICLEWATERFILLING",
            COALESCE(SUM(C."UREA_COUNT"),0) AS "UREA_COUNT"
        FROM "T_SERVERPART" A LEFT JOIN "T_SERVERPARTINFO" C ON A."SERVERPART_ID" = C."SERVERPART_ID"
        WHERE A."STATISTICS_TYPE" = 1000 AND A."STATISTIC_TYPE" = 1000
            AND A."SERVERPART_CODE" NOT IN ('340001','530590') AND A."SPREGIONTYPE_ID" NOT IN (89){where_sql}
        GROUP BY A."SERVERPART_ID", A."SERVERPART_NAME" """
    rows = db.execute_query(sql)
    if not rows: return None

    def _cnt(field): return sum(1 for r in rows if float(r.get(field, 0) or 0) > 0)
    tc = len(rows)
    ps = sum(1 for r in rows if "停车区" in str(r.get("SERVERPART_NAME", "")))
    return {
        "ServerpartTotalCount": tc, "ServerpartCount": tc - ps, "ParkingServiceCount": ps,
        "WaterStationCount": 0, "ViewingDeckCount": 0, "RestAreaCount": 0, "ClosedCountCount": 0,
        "FLoorArea": round(sum(float(r.get("FLOORAREA",0) or 0) for r in rows)/666.67, 2),
        "ParkingArea": round(sum(float(r.get("PARKINGAREA",0) or 0) for r in rows)/666.67, 2),
        "BuildingArea": round(sum(float(r.get("BUILDINGAREA",0) or 0) for r in rows)/666.67, 2),
        "GasStationCount": _cnt("HASGASSTATION"), "ChargeStationCount": _cnt("HASCHARGESTATION"),
        "ParkingLotCount": sum(1 for r in rows if any(float(r.get(k,0) or 0)>0 for k in ["SMALLPARKING","PACKING","TRUCKPACKING","LONGPACKING","DANPACKING"])),
        "AutoRepairCount": _cnt("HASAUTOREPAIR"), "ToiletCount": _cnt("HASRESTROOM"),
        "DriverRoomCount": _cnt("HASPILOTLOUNGE"), "NursingRoomCount": _cnt("HASMOTHER"),
        "StoreCount": _cnt("HASSTORE"), "CateringCount": _cnt("DININGROOMCOUNT"),
        "LodgingCount": _cnt("HASLODGING"), "WaterCount": _cnt("VEHICLEWATERFILLING"), "UreaCount": _cnt("UREA_COUNT"),
    }


# ===== 13. 品牌结构分析 =====
def get_brand_structure_analysis(db: DatabaseHelper, province_code: str, business_trade: str) -> list[dict]:
    where_sql = f""" AND "PROVINCE_CODE" = '{province_code}'"""
    if business_trade: where_sql += f""" AND "BRAND_INDUSTRY" IN ({business_trade})"""
    sql = f"""SELECT "BRAND_TYPE", COUNT(1) AS CNT FROM "T_BRAND"
        WHERE "BRAND_CATEGORY" = 1000 AND "BRAND_STATE" = 1{where_sql}
        GROUP BY "BRAND_TYPE" ORDER BY "BRAND_TYPE" """
    rows = db.execute_query(sql)

    brand_type_names = {}
    try:
        enum_rows = db.execute_query("""SELECT E."FIELDENUM_VALUE", E."FIELDENUM_NAME" FROM "T_FIELDENUM" E
            JOIN "T_FIELDEXPLAIN" F ON E."FIELDEXPLAIN_ID" = F."FIELDEXPLAIN_ID"
            WHERE F."FIELDEXPLAIN_FIELD" = 'BRAND_TYPE'""")
        brand_type_names = {str(r["FIELDENUM_VALUE"]): r["FIELDENUM_NAME"] for r in enum_rows}
    except: pass

    return [{"name": brand_type_names.get(str(r.get("BRAND_TYPE","")), str(r.get("BRAND_TYPE",""))),
             "value": str(r.get("CNT", 0)), "data": None, "key": str(r.get("BRAND_TYPE",""))} for r in rows]
