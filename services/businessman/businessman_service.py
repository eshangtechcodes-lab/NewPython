from __future__ import annotations
# -*- coding: utf-8 -*-
"""
BusinessManController + SupplierController 业务服务（39 个接口）

CRUD 实体:
  BusinessMan/BusinessManDetail/Commodity/CUSTOMTYPE/COMMODITY_TEMP (BusinessManCtrl)
  Supplier/Qualification/QUALIFICATION_HIS (SupplierCtrl)

散装接口:
  AuthorizeQualification / GetNestingCustomTypeLsit / GetCustomTypeDDL
  CreateBusinessMan / GetUserList / RelateBusinessCommodity / GetSupplierTreeList
"""
from typing import Tuple
from datetime import datetime
import locale
try:
    locale.setlocale(locale.LC_COLLATE, 'Chinese_China.936')  # Windows GBK 拼音排序
except locale.Error:
    try:
        locale.setlocale(locale.LC_COLLATE, 'zh_CN.GBK')
    except locale.Error:
        pass  # 回退到 Unicode 排序

from loguru import logger
from core.database import DatabaseHelper


def _crud(db, table, pk, sm, extra_fields=None, convert_fn=None):
    pi = sm.get("PageIndex", 1); ps = sm.get("PageSize", 10)
    sd = sm.get("SearchData") or sm.get("SearchParameter") or {}
    wp, pa = [], []
    # 主键精确匹配
    if sd.get(pk):
        wp.append(f"{pk} = ?"); pa.append(sd[pk])
    for f in (extra_fields or []):
        if sd.get(f): wp.append(f"{f} = ?"); pa.append(sd[f])
    wc = " AND ".join(wp) if wp else "1=1"
    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}", pa) or 0
    off = (pi - 1) * ps
    # 达梦兼容分页（ROWNUM 子查询）
    paged_sql = f"""
        SELECT * FROM (
            SELECT A.*, ROWNUM AS RN__ FROM (
                SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC
            ) A WHERE ROWNUM <= {off + ps}
        ) WHERE RN__ > {off}
    """
    rows = db.fetch_all(paged_sql, pa, null_to_empty=False) or []
    for r in rows:
        r.pop("RN__", None)
    if convert_fn:
        rows = [convert_fn(r) for r in rows]
    return rows, total

def _detail(db, table, pk, pk_val, convert_fn=None):
    row = db.fetch_one(f"SELECT * FROM {table} WHERE {pk} = ?", [pk_val])
    if row and convert_fn:
        row = convert_fn(row)
    return row

def _synchro(db, table, pk, data):
    pv = data.get(pk)
    if pv:
        c = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [pv])
        if c and c > 0:
            fs = {k: v for k, v in data.items() if k != pk}
            if not fs: return True, data
            sc = ", ".join([f"{k} = ?" for k in fs.keys()])
            db.execute(f"UPDATE {table} SET {sc} WHERE {pk} = ?", list(fs.values()) + [pv])
            return True, data
    try:
        nid = db.fetch_scalar(f"SELECT NEWPYTHON.SEQ_{table.replace('T_','')}.NEXTVAL FROM DUAL")
        data[pk] = nid
    except:
        nid = db.fetch_scalar(f"SELECT COALESCE(MAX({pk}), 0) + 1 FROM {table}")
        data[pk] = nid
    cols = ", ".join(data.keys())
    phs = ", ".join(["?"] * len(data))
    db.execute(f"INSERT INTO {table} ({cols}) VALUES ({phs})", list(data.values()))
    return True, data

def _delete(db, table, pk, sf, pk_val):
    c = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {pk} = ?", [pk_val])
    if not c or c == 0: return False
    db.execute(f"UPDATE {table} SET {sf} = 0 WHERE {pk} = ?", [pk_val])
    return True


ENTITIES = {
    # BS-01 修正：C# 底层 ORM 实体为 Business.OWNERUNIT，表名 T_OWNERUNIT
    # Python 迁移时误用 T_BUSINESSMAN，现恢复为 C# 原始表名
    "BUSINESSMAN": {"t": "T_OWNERUNIT", "pk": "OWNERUNIT_ID", "s": "OWNERUNIT_STATE", "f": []},
    "BUSINESSMANDETAIL": {"t": "T_OWNERUNITDETAIL", "pk": "OWNERUNITDETAIL_ID", "s": "OWNERUNITDETAIL_STATE", "f": ["OWNERUNIT_ID"]},
    "COMMODITY": {"t": "T_COMMODITY", "pk": "COMMODITY_ID", "s": "COMMODITY_STATE", "f": []},
    "CUSTOMTYPE": {"t": "T_CUSTOMTYPE", "pk": "CUSTOMTYPE_ID", "s": "CUSTOMTYPE_STATE", "f": []},
    "COMMODITY_TEMP": {"t": "T_COMMODITY_TEMP", "pk": "COMMODITY_TEMP_ID", "s": "COMMODITY_TEMP_STATE", "f": []},
    "SUPPLIER": {"t": "T_SUPPLIER", "pk": "SUPPLIER_ID", "s": "SUPPLIER_STATE", "f": []},
    "QUALIFICATION": {"t": "T_QUALIFICATION", "pk": "QUALIFICATION_ID", "s": "QUALIFICATION_STATE", "f": ["SUPPLIER_ID"]},
    "QUALIFICATION_HIS": {"t": "T_QUALIFICATION_HIS", "pk": "QUALIFICATION_HIS_ID", "s": "QUALIFICATION_HIS_STATE", "f": ["SUPPLIER_ID"]},
}

# C# Model 回显属性和类型转换配置
_ENTITY_CONVERT = {
    "COMMODITY_TEMP": {
        "extra": {"SERVERPART_IDS": None, "SEARCH_STARTDATE": None, "SEARCH_ENDDATE": None,
                  "OPERATE_STARTDATE": None, "OPERATE_ENDDATE": None},
        "int_to_date": ["QUALIFICATION_DATE", "STATISTICS_DATE"],  # int(20220801) → str('2022/08/01')
        "string_fields": {"COMMODITY_TEMP_DESC", "STAFF_NAME"},  # C# List/Detail null→''
    },
}

def _format_int_date(val):
    """将 int 日期转为 C# 格式: 20220801 → '2022/08/01'"""
    if val is None:
        return None
    s = str(val)
    if len(s) == 8:
        y, m, d = int(s[:4]), int(s[4:6]), int(s[6:8])
        return f"{y}/{m:02d}/{d:02d}"
    return s

def _make_convert(cfg, for_list=False):
    """生成实体行转换函数"""
    extra = cfg.get("extra", {})
    int_to_date = cfg.get("int_to_date", [])
    string_fields = cfg.get("string_fields", set()) if for_list else set()
    def _convert(row):
        if not row:
            return row
        for k, v in extra.items():
            if k not in row:
                row[k] = v
        for f in int_to_date:
            if f in row:
                row[f] = _format_int_date(row[f])
        for f in string_fields:
            if f in row and row[f] is None:
                row[f] = ""
        return row
    return _convert

# 预编译转换函数（区分 list 和 detail）
_CONVERT_LIST_FNS = {name: _make_convert(cfg, for_list=True) for name, cfg in _ENTITY_CONVERT.items()}
_CONVERT_DETAIL_FNS = {name: _make_convert(cfg, for_list=False) for name, cfg in _ENTITY_CONVERT.items()}

def get_entity_list(db, name, sm):
    e = ENTITIES[name]; fn = _CONVERT_LIST_FNS.get(name)
    return _crud(db, e["t"], e["pk"], sm, e.get("f"), convert_fn=fn)
def get_entity_detail(db, name, pk_val):
    e = ENTITIES[name]; fn = _CONVERT_DETAIL_FNS.get(name)
    return _detail(db, e["t"], e["pk"], pk_val, convert_fn=fn)
def synchro_entity(db, name, data):
    e = ENTITIES[name]; return _synchro(db, e["t"], e["pk"], data)
def delete_entity(db, name, pk_val):
    e = ENTITIES[name]; return _delete(db, e["t"], e["pk"], e["s"], pk_val)


# 散装接口
def authorize_qualification(db, data: dict):
    """授权资质"""
    logger.info(f"AuthorizeQualification: {data}")
    return _synchro(db, "T_QUALIFICATION", "QUALIFICATION_ID", data)

def get_nesting_custom_type_list(db, **kwargs):
    """获取嵌套自定义类型列表"""
    logger.info(f"GetNestingCustomTypeLsit: {kwargs}")
    try:
        return db.fetch_all("SELECT * FROM T_CUSTOMTYPE WHERE CUSTOMTYPE_STATE = 1 ORDER BY CUSTOMTYPE_ID") or []
    except Exception as e:
        logger.error(f"GetNestingCustomTypeLsit 失败: {e}")
        return []

def get_custom_type_ddl(db, **kwargs):
    """获取自定义类型下拉"""
    logger.info(f"GetCustomTypeDDL: {kwargs}")
    try:
        return db.fetch_all("SELECT CUSTOMTYPE_ID, CUSTOMTYPE_NAME FROM T_CUSTOMTYPE WHERE CUSTOMTYPE_STATE = 1") or []
    except Exception as e:
        logger.error(f"GetCustomTypeDDL 失败: {e}")
        return []

def create_businessman(db, data: dict):
    """创建商家 — C# BusinessManHelper.CreateBusinessMan
    底层操作 T_OWNERUNIT 表（COOP_MERCHANT schema）
    """
    logger.info(f"CreateBusinessMan: {data}")
    return _synchro(db, "T_OWNERUNIT", "OWNERUNIT_ID", data)

def get_user_list(db, search_model: dict = None, **kwargs):
    """获取经营单位账号列表 — C# BusinessManHelper.GetUserList (L528-691)
    构建树形 NestingModel：经营商户 → 子节点为关联账户（含门店权限列表）
    """
    logger.info(f"GetUserList: {search_model or kwargs}")
    try:
        # 从 search_model 或 kwargs 提取参数（兼容 POST body 和 GET query）
        params = search_model or kwargs or {}
        business_man_id = str(params.get("BusinessManId", "") or "")
        province_code = params.get("ProvinceCode")
        serverpart_id = str(params.get("ServerpartId", "") or "")
        serverpart_shop_id = str(params.get("ServerpartShopId", "") or "")
        valid_state = params.get("ValidState")
        search_name = str(params.get("SearchName", "") or params.get("keyWord", {}).get("Key", "") or "")
        search_value = str(params.get("SearchValue", "") or params.get("keyWord", {}).get("Value", "") or "")

        # 1. 查询经营商户列表（C# L534-576: 只取 3 字段）
        where_sql = "A.OWNERUNIT_NATURE = 2000"
        if business_man_id:
            ids = ",".join(business_man_id.split(","))
            where_sql += f" AND A.OWNERUNIT_ID IN ({ids})"
        if province_code is not None:
            where_sql += f" AND A.PROVINCE_CODE = {province_code}"

        # 过滤服务区门店权限（C# L551-573: OWNERSERVERPARTSHOPHelper）
        if serverpart_id or serverpart_shop_id:
            shop_where = "1=1"
            if province_code is not None:
                shop_where += f" AND PROVINCE_CODE = {province_code}"
            if serverpart_id:
                shop_where += f" AND SERVERPART_ID IN ({serverpart_id})"
            if serverpart_shop_id:
                shop_where += f" AND SERVERPARTSHOP_ID IN ({serverpart_shop_id})"
            owner_shops = db.fetch_all(
                f"SELECT DISTINCT OWNERUNIT_ID FROM T_OWNERSERVERPARTSHOP WHERE {shop_where}") or []
            if owner_shops:
                owner_ids = ",".join([str(r["OWNERUNIT_ID"]) for r in owner_shops])
                where_sql += f" AND A.OWNERUNIT_ID IN ({owner_ids})"
            else:
                return [], 0  # C# L572: 无匹配时返回空

        # C# L575: 只查 3 个字段
        bm_sql = f"SELECT OWNERUNIT_ID, OWNERUNIT_NAME, OWNERUNIT_STATE FROM T_OWNERUNIT A WHERE {where_sql}"
        bm_rows = db.fetch_all(bm_sql) or []
        if not bm_rows:
            return [], 0

        # 2. 查询经营单位用户（C# L580-595: USERHelper.GetUSERList）
        # C# 传参: BUSINESSMAN_IDS=请求参数(非查出的bm_ids)、USER_PATTERN=2000、
        #          USER_PROVINCE=ProvinceCode、USER_STATUS=ValidState、ServerpartIds=ServerpartId
        bm_id_list = [str(r["OWNERUNIT_ID"]) for r in bm_rows]
        bm_ids_str = ",".join(bm_id_list)

        # 构建 USER 查询 WHERE（模拟 USERHelper L46-114）
        user_where = "A.USER_PATTERN = 2000"
        # BUSINESSMAN_IDS: C# 从请求参数直接传，非空时过滤；为空时不加此条件
        # 但因为 OWNERUNIT 已用 ServerpartId 过滤，仍需限定 BUSINESSMAN_ID 在 bm_ids 中
        user_where += f" AND A.BUSINESSMAN_ID IN ({bm_ids_str})"
        if province_code is not None:
            user_where += f" AND A.USER_PROVINCE = {province_code}"
        if valid_state is not None:
            user_where += f" AND A.USER_STATUS = {valid_state}"

        # C# L80-103: 当 USER_PATTERN=2000 且有 ServerpartIds 时，
        # 用 EXISTS 子查询过滤 T_USERAUTHORITY + T_SERVERPARTSHOP
        if serverpart_id or serverpart_shop_id:
            exists_extra = ""
            if serverpart_id:
                exists_extra += f" AND C.SERVERPART_ID IN ({serverpart_id})"
            if serverpart_shop_id:
                exists_extra += f" AND C.SERVERPARTSHOP_ID IN ({serverpart_shop_id})"
            user_where += (
                " AND EXISTS (SELECT 1 FROM T_USERAUTHORITY B, T_SERVERPARTSHOP C"
                f" WHERE A.USER_ID = B.USER_ID AND B.SERVERPARTSHOP_ID = C.SERVERPARTSHOP_ID{exists_extra})"
            )

        user_sql = f"SELECT * FROM T_USER A WHERE {user_where}"
        user_rows = db.fetch_all(user_sql) or []

        # 模糊查询（C# L120-131: keyWord 过滤，在 DataTable RowFilter 层面）
        if search_name and search_value:
            filtered = []
            for u in user_rows:
                match = False
                for kn in search_name.split(","):
                    kn = kn.strip()
                    if kn and search_value in str(u.get(kn, "") or ""):
                        match = True; break
                if match:
                    filtered.append(u)
            user_rows = filtered

        # 3. 查询用户门店权限（C# L597-611）
        user_shop_map = {}  # user_id -> [shop_info]
        if user_rows:
            user_ids = ",".join([str(r["USER_ID"]) for r in user_rows])
            # C# L601-609: 额外查了 SHOPSHORTNAME 和 SHOPREGION
            shop_auth_sql = f"""SELECT A.USER_ID, B.SERVERPART_ID, B.SERVERPART_CODE,
                    B.SERVERPART_NAME, B.SERVERPARTSHOP_ID, B.SHOPNAME,
                    B.SHOPTRADE, B.SHOPCODE
                FROM T_USERAUTHORITY A, T_SERVERPARTSHOP B
                WHERE A.SERVERPARTSHOP_ID = B.SERVERPARTSHOP_ID
                    AND A.USER_ID IN ({user_ids})"""
            shop_auth_rows = db.fetch_all(shop_auth_sql) or []
            for sr in shop_auth_rows:
                uid = sr["USER_ID"]
                if uid not in user_shop_map:
                    user_shop_map[uid] = []
                user_shop_map[uid].append(sr)

        # 4. 构建树形 NestingModel（C# L613-687）
        # C# L613: foreach (DataRow in dtBusinessMan.Select("", "OWNERUNIT_NAME"))
        result = []
        for bm in sorted(bm_rows, key=lambda x: locale.strxfrm(str(x.get("OWNERUNIT_NAME", "") or ""))):
            bm_id = bm["OWNERUNIT_ID"]
            # C# L618-623: parent node = new USERModel {...}
            # 序列化时输出 USERModel 全部 38 个属性（含默认值）
            node = {
                # 3 个赋值字段
                "BUSINESSMAN_ID": bm_id,
                "BUSINESSMAN_NAME": bm.get("OWNERUNIT_NAME", ""),
                "USER_STATUS": bm.get("OWNERUNIT_STATE"),
                # USERModel 其余 35 个字段的默认值
                "USER_ID": None,
                "USER_ID_Encrypted": None,
                "USERTYPE_ID": None,
                "USER_NAME": None,
                "USER_PASSPORT": None,
                "USER_PASSWORD": None,
                "USER_TIMEOUT": None,
                "USER_INDEX": None,
                "USER_INDEFINIT": None,
                "USER_EXPIRY": None,
                "USER_CITYAUTHORITY": None,
                "USER_REPEATLOGON": None,
                "USER_MOBILEPHONE": None,
                "USER_PROVINCE": None,
                "PROVINCE_UNIT": None,
                "USER_PATTERN": None,
                "SUPER_ADMIN": None,
                "STAFF_ID": None,
                "STAFF_NAME": None,
                "OPERATE_DATE": None,
                "USER_DESC": None,
                "USER_HEADIMGURL": None,
                # 扩展属性默认值
                "AnalysisPermission": False,
                "BUSINESSMAN_IDS": None,
                "IDENTITY_CODE": None,
                "PushPermission": False,
                "PushList": None,
                "SYSTEMROLE_IDS": None,
                "ServerpartIds": None,
                "ServerpartList": None,
                "ServerpartShopList": None,
                "ShopNameList": None,
                "SystemRoleList": None,
                "USER_IDS": None,
                "UserTypeIds": None,
            }

            # 查找属于该商户的用户（C# L626-663）
            bm_users = [u for u in user_rows if u.get("BUSINESSMAN_ID") == bm_id]
            children = None
            if bm_users:
                children = []
                # C# L632: OrderByDescending(o => o.OPERATE_DATE)
                bm_users.sort(key=lambda x: str(x.get("OPERATE_DATE", "") or ""), reverse=True)
                for u in bm_users:
                    uid = u["USER_ID"]
                    shops = user_shop_map.get(uid, [])
                    # C# L641-642: 按 SERVERPART_CODE,SHOPTRADE,SHOPSHORTNAME,SHOPREGION,SHOPCODE 排序
                    shop_names = []
                    sp_names = []
                    for s in sorted(shops, key=lambda x: (
                        str(x.get("SERVERPART_CODE", "") or ""),
                        str(x.get("SHOPTRADE", "") or ""),
                        str(x.get("SHOPCODE", "") or ""))):
                        sp_name = str(s.get("SERVERPART_NAME", "") or "")
                        if sp_name and sp_name not in sp_names:
                            sp_names.append(sp_name)
                        short_sp = sp_name.replace("服务区", "")
                        full_shop = short_sp + str(s.get("SHOPNAME", "") or "")
                        if full_shop not in shop_names:
                            shop_names.append(full_shop)

                    user_node = dict(u)
                    # C# BindDataRowToModel (L184-272) 输出 27 个字段
                    # 去掉 C# 不输出的多余数据库字段
                    for _rm in ("USER_ENABLEDCITYAUTHORITY", "USER_ENABLEDLICENSE", "USER_LICENSE"):
                        user_node.pop(_rm, None)
                    # C# USERModel 回显属性（默认值）
                    for _extra in ("BUSINESSMAN_IDS", "IDENTITY_CODE",
                                   "SYSTEMROLE_IDS", "ServerpartIds",
                                   "USER_IDS", "USER_ID_Encrypted", "UserTypeIds"):
                        if _extra not in user_node:
                            user_node[_extra] = None
                    # 布尔回显字段默认 False
                    for _bool_f in ("AnalysisPermission", "PushPermission"):
                        if _bool_f not in user_node:
                            user_node[_bool_f] = False
                    for _extra_list in ("PushList", "ServerpartShopList", "SystemRoleList"):
                        if _extra_list not in user_node:
                            user_node[_extra_list] = None
                    user_node["ShopNameList"] = shop_names
                    user_node["ServerpartList"] = sp_names
                    children.append({"node": user_node, "children": None})

            # C# L666-683: 过滤逻辑
            should_add = (children is not None
                          or not search_value
                          or search_value in node.get("BUSINESSMAN_NAME", ""))
            # ValidState 过滤
            if valid_state is not None and children is None and node.get("USER_STATUS") != valid_state:
                should_add = False
            if should_add:
                result.append({"node": node, "children": children})

        # C# L687: 最终按 BUSINESSMAN_NAME 排序
        result.sort(key=lambda x: locale.strxfrm(str(x.get("node", {}).get("BUSINESSMAN_NAME", "") or "")))

        return result, len(result)
    except Exception as e:
        logger.error(f"GetUserList 失败: {e}")
        import traceback; traceback.print_exc()
        return [], 0

def get_supplier_tree_list(db, search_model: dict):
    """获取供应商树形列表 — C# SUPPLIERHelper.GetSUPPLIERTreeList (L172-358)
    用 T_AUTOSTATISTICS (TYPE=4000 供应商考评类型) 递归构建树形结构
    每个叶子节点下挂供应商列表
    """
    logger.info("GetSupplierTreeList")
    try:
        sp = search_model.get("SearchParameter") or search_model.get("SearchData") or {}
        province_code = sp.get("PROVINCE_CODE")

        # 1. 获取 AUTOSTATISTICS 考评类型列表（TYPE=4000, STATE=1）
        stat_where = "AUTOSTATISTICS_STATE = 1 AND AUTOSTATISTICS_TYPE = 4000"
        if province_code is not None:
            stat_where += f" AND PROVINCE_CODE = {province_code}"
        stat_rows = db.fetch_all(
            f"SELECT * FROM T_AUTOSTATISTICS WHERE {stat_where} "
            f"ORDER BY AUTOSTATISTICS_INDEX, AUTOSTATISTICS_ID") or []

        # 2. 获取供应商列表（带资质统计）
        sup_where = "SUPPLIER_STATE > 0"
        ownerunit_id = sp.get("OWNERUNIT_ID")
        if ownerunit_id is not None:
            # 查询经营商户及子公司
            bm_rows = db.fetch_all(
                f"SELECT OWNERUNIT_ID FROM T_OWNERUNIT WHERE OWNERUNIT_NATURE = 2000") or []
            # 简化：直接使用 OWNERUNIT_ID 过滤
            sup_where += f" AND OWNERUNIT_ID = {ownerunit_id}"
        if province_code is not None:
            sup_where += f" AND PROVINCE_CODE = {province_code}"

        sup_rows = db.fetch_all(
            f"SELECT * FROM T_SUPPLIER WHERE {sup_where} ORDER BY OPERATE_DATE DESC") or []

        # 查询资质统计
        if sup_rows:
            sup_ids = ",".join([str(r["SUPPLIER_ID"]) for r in sup_rows])
            qual_stat = db.fetch_all(
                f"SELECT COUNT(1) AS QUALIFICATION_COUNT, QUALIFICATION_STATE, SUPPLIER_ID "
                f"FROM T_QUALIFICATION WHERE QUALIFICATION_STATE > 0 AND SUPPLIER_ID IN ({sup_ids}) "
                f"GROUP BY QUALIFICATION_STATE, SUPPLIER_ID") or []
            # 构建统计映射
            for s in sup_rows:
                sid = s["SUPPLIER_ID"]
                s["UPLOAD_QUALIFICATION"] = sum(
                    int(q.get("QUALIFICATION_COUNT", 0) or 0)
                    for q in qual_stat if q.get("SUPPLIER_ID") == sid)
                s["EXPIRED_QUALIFICATION"] = sum(
                    int(q.get("QUALIFICATION_COUNT", 0) or 0)
                    for q in qual_stat if q.get("SUPPLIER_ID") == sid
                    and q.get("QUALIFICATION_STATE") == 2)

        # 3. 递归构建 NestingModel 树
        def _bind_data(parent_id, suppliers):
            """递归绑定树形节点"""
            children_types = [t for t in stat_rows if t.get("AUTOSTATISTICS_PID") == parent_id]
            result_nodes = []

            if children_types:
                for st in children_types:
                    st_id = st["AUTOSTATISTICS_ID"]
                    # 获取当前分类下的供应商
                    type_suppliers = [s for s in suppliers
                                     if s.get("PROVINCE_CODE") == st.get("PROVINCE_CODE")
                                     and s.get("MERCHANTTYPE_ID") == st_id]

                    node = {
                        "AUTOSTATISTICS_ID": st_id,
                        "AUTOSTATISTICS_PID": st.get("AUTOSTATISTICS_PID"),
                        "AUTOSTATISTICS_NAME": st.get("AUTOSTATISTICS_NAME"),
                        "AUTOSTATISTICS_ICO": st.get("AUTOSTATISTICS_ICO"),
                        "OWNERUNIT_ID": st.get("OWNERUNIT_ID"),
                        "OWNERUNIT_NAME": st.get("OWNERUNIT_NAME"),
                        "PROVINCE_CODE": st.get("PROVINCE_CODE"),
                    }

                    # 检查是否还有下级分类
                    has_sub = any(t.get("AUTOSTATISTICS_PID") == st_id for t in stat_rows)

                    if not has_sub:
                        # 叶子节点：挂供应商数据
                        child_nodes = []
                        for sup in type_suppliers:
                            child_node = dict(sup)
                            child_node.update({
                                "AUTOSTATISTICS_ID": st_id,
                                "AUTOSTATISTICS_PID": st.get("AUTOSTATISTICS_PID"),
                                "AUTOSTATISTICS_NAME": st.get("AUTOSTATISTICS_NAME"),
                            })
                            child_nodes.append({"node": child_node, "children": None})
                        result_nodes.append({
                            "node": node,
                            "children": child_nodes if child_nodes else None
                        })
                    else:
                        # 中间节点：递归
                        sub_nodes = _bind_data(st_id, type_suppliers or suppliers)
                        result_nodes.append({
                            "node": node,
                            "children": sub_nodes if sub_nodes else None
                        })
            else:
                # 没有子分类时，按 MERCHANTTYPE_ID = parent_id 挂供应商
                type_suppliers = [s for s in suppliers if s.get("MERCHANTTYPE_ID") == parent_id]
                if type_suppliers:
                    parent_stat = next((t for t in stat_rows if t.get("AUTOSTATISTICS_ID") == parent_id), None)
                    child_nodes = []
                    for sup in type_suppliers:
                        child_node = dict(sup)
                        if parent_stat:
                            child_node.update({
                                "AUTOSTATISTICS_ID": parent_stat.get("AUTOSTATISTICS_ID"),
                                "AUTOSTATISTICS_PID": parent_stat.get("AUTOSTATISTICS_PID"),
                                "AUTOSTATISTICS_NAME": parent_stat.get("AUTOSTATISTICS_NAME"),
                            })
                        child_nodes.append({"node": child_node, "children": None})
                    node = {}
                    if parent_stat:
                        node = {
                            "AUTOSTATISTICS_ID": parent_stat.get("AUTOSTATISTICS_ID"),
                            "AUTOSTATISTICS_PID": parent_stat.get("AUTOSTATISTICS_PID"),
                            "AUTOSTATISTICS_NAME": parent_stat.get("AUTOSTATISTICS_NAME"),
                            "AUTOSTATISTICS_ICO": parent_stat.get("AUTOSTATISTICS_ICO"),
                            "OWNERUNIT_ID": parent_stat.get("OWNERUNIT_ID"),
                            "OWNERUNIT_NAME": parent_stat.get("OWNERUNIT_NAME"),
                            "PROVINCE_CODE": parent_stat.get("PROVINCE_CODE"),
                        }
                    result_nodes.append({
                        "node": node,
                        "children": child_nodes
                    })
            return result_nodes

        # 从根节点开始（AUTOSTATISTICS_PID = -1）
        root_types = [t for t in stat_rows if t.get("AUTOSTATISTICS_PID") == -1]
        tree_list = []
        for root in root_types:
            sub_nodes = _bind_data(root["AUTOSTATISTICS_ID"], sup_rows)
            root_node = {
                "AUTOSTATISTICS_ID": root["AUTOSTATISTICS_ID"],
                "AUTOSTATISTICS_PID": root.get("AUTOSTATISTICS_PID"),
                "AUTOSTATISTICS_NAME": root.get("AUTOSTATISTICS_NAME"),
                "AUTOSTATISTICS_ICO": root.get("AUTOSTATISTICS_ICO"),
                "OWNERUNIT_ID": root.get("OWNERUNIT_ID"),
                "OWNERUNIT_NAME": root.get("OWNERUNIT_NAME"),
                "PROVINCE_CODE": root.get("PROVINCE_CODE"),
            }
            tree_list.append({
                "node": root_node,
                "children": sub_nodes if sub_nodes else None
            })

        return tree_list, len(tree_list)
    except Exception as e:
        logger.error(f"GetSupplierTreeList 失败: {e}")
        import traceback; traceback.print_exc()
        return [], 0

def relate_business_commodity(db, data: dict):
    """关联商家商品 — C# QUALIFICATIONHelper.RelateBusinessCommodity (L371-416)
    更新 T_COMMODITY_BUSINESS 的资质关联 + 插入 T_RELATIONTABLES 关联记录
    """
    logger.info(f"RelateBusinessCommodity: {data}")
    try:
        qualification_id = data.get("QualificationId")
        commodity_ids = data.get("CommodityIds", "")
        staff_id = data.get("StaffId")
        staff_name = data.get("StaffName", "")

        if not qualification_id or not commodity_ids:
            return False, "请传入资质内码和商品内码"

        execute_count = 0

        # 更新商品库关联的资质信息
        db.execute(
            f"UPDATE T_COMMODITY_BUSINESS SET QUALIFICATION_ID = ?, QUALIFICATION_ENDDATE = NULL, "
            f"COMMODITY_QTYPE = 1 WHERE COMMODITY_BUSINESS_ID IN ({commodity_ids})",
            [qualification_id])
        execute_count += 1

        # 查询已有的关联记录
        existing = db.fetch_all(
            "SELECT NEXTTABLE_ID FROM T_RELATIONTABLES WHERE FORMATTABLE_ID = ? "
            "AND FORMATTABLE_NAME = 'T_QUALIFICATION' AND FORMATUSER_NAME = 'COOP_MERCHANT' "
            "AND NEXTTABLE_NAME = 'T_COMMODITY_BUSINESS' AND NEXTUSER_NAME = 'HIGHWAY_STORAGE'",
            [qualification_id]) or []
        existing_ids = {str(r.get("NEXTTABLE_ID")) for r in existing}

        # 插入新的关联记录
        for cid in commodity_ids.split(","):
            cid = cid.strip()
            if cid and cid not in existing_ids:
                db.execute(
                    """INSERT INTO T_RELATIONTABLES (FORMATTABLE_ID, FORMATTABLE_NAME, FORMATUSER_NAME,
                        NEXTTABLE_ID, NEXTTABLE_NAME, NEXTUSER_NAME,
                        STAFF_ID, STAFF_NAME, RELATE_DATE, RTPROINST_DESC)
                    VALUES (?, 'T_QUALIFICATION', 'COOP_MERCHANT',
                        ?, 'T_COMMODITY_BUSINESS', 'HIGHWAY_STORAGE',
                        ?, ?, SYSDATE, '从供应商资质管理页面授权商品')""",
                    [qualification_id, cid, staff_id, staff_name])
                execute_count += 1

        return True, ""
    except Exception as e:
        logger.error(f"RelateBusinessCommodity 失败: {e}")
        return False, f"关联失败: {e}"
