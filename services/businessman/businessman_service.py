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
from loguru import logger
from core.database import DatabaseHelper


def _crud(db, table, pk, sm, extra_fields=None):
    pi = sm.get("PageIndex", 1); ps = sm.get("PageSize", 15)
    sd = sm.get("SearchData") or {}
    wp, pa = [], []
    for f in (extra_fields or []):
        if sd.get(f): wp.append(f"{f} = ?"); pa.append(sd[f])
    wc = " AND ".join(wp) if wp else "1=1"
    total = db.fetch_scalar(f"SELECT COUNT(*) FROM {table} WHERE {wc}", pa) or 0
    off = (pi - 1) * ps
    rows = db.fetch_all(f"SELECT * FROM {table} WHERE {wc} ORDER BY {pk} DESC LIMIT {ps} OFFSET {off}", pa) or []
    return rows, total

def _detail(db, table, pk, pk_val):
    return db.fetch_one(f"SELECT * FROM {table} WHERE {pk} = ?", [pk_val])

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

def get_entity_list(db, name, sm):
    e = ENTITIES[name]; return _crud(db, e["t"], e["pk"], sm, e.get("f"))
def get_entity_detail(db, name, pk_val):
    e = ENTITIES[name]; return _detail(db, e["t"], e["pk"], pk_val)
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

        # 1. 查询经营商户列表（OWNERUNIT_NATURE=2000 经营单位）
        where_sql = "A.OWNERUNIT_NATURE = 2000"
        if business_man_id:
            ids = ",".join(business_man_id.split(","))
            where_sql += f" AND A.OWNERUNIT_ID IN ({ids})"
        if province_code is not None:
            where_sql += f" AND A.PROVINCE_CODE = {province_code}"

        # 如果指定了 ServerpartId / ServerpartShopId，先反查关联的 OWNERUNIT_ID
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
                return [], 0  # 无匹配商户

        bm_sql = f"SELECT OWNERUNIT_ID, OWNERUNIT_NAME, OWNERUNIT_STATE FROM T_OWNERUNIT A WHERE {where_sql}"
        bm_rows = db.fetch_all(bm_sql) or []
        if not bm_rows:
            return [], 0

        bm_id_list = [str(r["OWNERUNIT_ID"]) for r in bm_rows]
        bm_ids_str = ",".join(bm_id_list)

        # 2. 查询经营单位用户（USER_PATTERN=2000）
        user_where = f"USER_PATTERN = 2000 AND BUSINESSMAN_ID IN ({bm_ids_str})"
        if province_code is not None:
            user_where += f" AND USER_PROVINCE = {province_code}"
        if valid_state is not None:
            user_where += f" AND USER_STATUS = {valid_state}"
        # 模糊查询
        if search_name and search_value:
            key_parts = []
            for kn in search_name.split(","):
                kn = kn.strip()
                if kn:
                    key_parts.append(f"{kn} LIKE '%{search_value}%'")
            if key_parts:
                user_where += f" AND ({' OR '.join(key_parts)})"
        user_rows = db.fetch_all(f"SELECT * FROM T_USER WHERE {user_where}") or []

        # 3. 查询用户门店权限（如果有用户数据）
        user_shop_map = {}  # user_id -> [shop_info]
        if user_rows:
            user_ids = ",".join([str(r["USER_ID"]) for r in user_rows])
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

        # 4. 构建树形 NestingModel：商户 → 用户列表
        result = []
        for bm in sorted(bm_rows, key=lambda x: x.get("OWNERUNIT_NAME", "")):
            bm_id = bm["OWNERUNIT_ID"]
            node = {
                "BUSINESSMAN_ID": bm_id,
                "BUSINESSMAN_NAME": bm.get("OWNERUNIT_NAME", ""),
                "USER_STATUS": bm.get("OWNERUNIT_STATE"),
            }
            # 查找属于该商户的用户
            bm_users = [u for u in user_rows if u.get("BUSINESSMAN_ID") == bm_id]
            children = None
            if bm_users:
                children = []
                # 按操作时间降序
                bm_users.sort(key=lambda x: str(x.get("OPERATE_DATE", "") or ""), reverse=True)
                for u in bm_users:
                    uid = u["USER_ID"]
                    shops = user_shop_map.get(uid, [])
                    # 构建门店名称列表
                    shop_names = []
                    sp_names = []
                    for s in sorted(shops, key=lambda x: (
                        x.get("SERVERPART_CODE", ""), x.get("SHOPCODE", ""))):
                        sp_name = str(s.get("SERVERPART_NAME", "") or "")
                        if sp_name and sp_name not in sp_names:
                            sp_names.append(sp_name)
                        short_sp = sp_name.replace("服务区", "")
                        full_shop = short_sp + str(s.get("SHOPNAME", "") or "")
                        if full_shop not in shop_names:
                            shop_names.append(full_shop)

                    user_node = dict(u)
                    user_node["ShopNameList"] = shop_names
                    user_node["ServerpartList"] = sp_names
                    children.append({"node": user_node, "children": None})

            # 过滤逻辑：有子节点，或搜索值匹配商户名，或无搜索条件
            should_add = (children is not None
                          or not search_value
                          or search_value in node.get("BUSINESSMAN_NAME", ""))
            # ValidState 过滤
            if valid_state is not None and children is None and node.get("USER_STATUS") != valid_state:
                should_add = False
            if should_add:
                result.append({"node": node, "children": children})

        return result, len(result)
    except Exception as e:
        logger.error(f"GetUserList 失败: {e}")
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
