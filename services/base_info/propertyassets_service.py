from __future__ import annotations
# -*- coding: utf-8 -*-
"""
服务区资产表业务服务
替代原 PROPERTYASSETSHelper.cs（1107行）
使用 HIGHWAY_STORAGE.T_PROPERTYASSETS 表
"""
from typing import Optional
from datetime import datetime
from loguru import logger
from core.database import DatabaseHelper
from models.common_model import SearchModel, SEARCH_PARAM_SKIP_FIELDS


# 表名常量
TABLE_NAME = "T_PROPERTYASSETS"
PRIMARY_KEY = "PROPERTYASSETS_ID"

# 排除字段（非数据库字段）
EXCLUDE_FIELDS = {
    "PROPERTYASSETS_IDS", "SERVERPART_IDS", "PROPERTYASSETS_TYPES",
    "SERVERPARTSHOP_ID", "BUSINESS_STATE", "SHOPNAME",
    "BUSINESSPROJECT_ID", "BUSINESSPROJECT_NAME", "REGISTERCOMPACT_ID",
    "COMPACT_NAME", "PROJECT_STARTDATE", "PROJECT_ENDDATE", "PROJECT_VALID",
    "ShopList", "PropertyShop", "BusinessProjectList",
    "SPREGIONTYPE_ID", "SPREGIONTYPE_NAME", "SPREGIONTYPE_INDEX",
    "TOTAL_AREA", "RN",
}


def _build_where_sql(search_param: dict, query_type: int = 0) -> str:
    """构建 WHERE 条件"""
    conditions = []
    for key, value in search_param.items():
        if key in EXCLUDE_FIELDS:

            continue

        if value is None:

            continue

        if isinstance(value, str) and value.strip() == "":

            continue

        if query_type == 0 and isinstance(value, str):
            conditions.append(f"{key} LIKE '%{value}%'")
        else:
            if isinstance(value, str):
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"{key} = {value}")
    return " AND ".join(conditions)


def _build_keyword_filter(keyword: dict) -> str:
    """构建关键字过滤条件"""
    if not keyword or not keyword.get("Key") or not keyword.get("Value"):
        return ""
    keys = keyword["Key"].split(",")
    conditions = [f"{k.strip()} LIKE '%{keyword['Value']}%'" for k in keys if k.strip()]
    return " OR ".join(conditions)


# ========== 1. GetPROPERTYASSETSList ==========

def get_propertyassets_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区资产表列表
    对应原 PROPERTYASSETSHelper.GetPROPERTYASSETSList（L22-230）
    简化版：不关联门店/项目信息（TreeList 中有完整版）
    """
    where_sql = ""
    if search_model.SearchParameter:
        sp = search_model.SearchParameter
        where_clause = _build_where_sql(sp, search_model.QueryType or 0)

        # PROPERTYASSETS_IDS（资产内码列表）
        ids = sp.get("PROPERTYASSETS_IDS")
        if ids and str(ids).strip():
            id_list = ",".join(ids.split(","))
            extra = f"PROPERTYASSETS_ID IN ({id_list})"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra

        # SERVERPART_IDS（服务区内码）
        sp_ids = sp.get("SERVERPART_IDS")
        if sp_ids and str(sp_ids).strip():
            extra = f"SERVERPART_ID IN ({sp_ids})"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra

        # PROPERTYASSETS_TYPES（资产类型，简化：直接 IN 查询）
        types = sp.get("PROPERTYASSETS_TYPES")
        if types and str(types).strip():
            extra = f"PROPERTYASSETS_TYPE IN ({types})"
            where_clause = f"{where_clause} AND {extra}" if where_clause else extra

        if where_clause:
            where_sql = f" WHERE {where_clause}"

    base_sql = f"SELECT * FROM {TABLE_NAME}{where_sql}"

    # 关键字过滤
    if search_model.keyWord:
        kw = search_model.keyWord
        if hasattr(kw, 'model_dump'):
            kw = kw.model_dump()
        keyword_filter = _build_keyword_filter(kw)
        if keyword_filter:
            if where_sql:
                base_sql += f" AND ({keyword_filter})"
            else:
                base_sql += f" WHERE ({keyword_filter})"

    # 排序
    if search_model.SortStr:
        base_sql += f" ORDER BY {search_model.SortStr}"
    else:
        base_sql += " ORDER BY PROPERTYASSETS_CODE"

    # 总数
    count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
    total_count = db.execute_scalar(count_sql) or 0

    # 分页
    page_index = search_model.PageIndex or 0
    page_size = search_model.PageSize or 0
    if page_index > 0 and page_size > 0:
        start_row = (page_index - 1) * page_size + 1
        end_row = page_index * page_size
        paged_sql = f"""
            SELECT * FROM (
                SELECT A.*, ROWNUM RN FROM ({base_sql}) A
                WHERE ROWNUM <= {end_row}
            ) WHERE RN >= {start_row}
        """
        rows = db.execute_query(paged_sql)
        for row in rows:
            row.pop("RN", None)
    else:
        rows = db.execute_query(base_sql)

    # 关联门店对照信息（批量预加载）
    if rows:
        asset_ids = [str(r.get("PROPERTYASSETS_ID")) for r in rows if r.get("PROPERTYASSETS_ID")]
        if asset_ids:
            _enrich_assets_with_shop(db, rows, asset_ids)

    return int(total_count), rows


def _enrich_assets_with_shop(db: DatabaseHelper, rows: list, asset_ids: list):
    """批量预加载资产关联的门店信息"""
    try:
        # 查询资产与门店对照
        shop_map_sql = f"""SELECT A.PROPERTYASSETS_ID, A.SERVERPARTSHOP_ID, A.PROPERTYSHOP_STATE,
                A.STARTDATE, A.ENDDATE, B.SHOPNAME, B.BUSINESS_STATE
            FROM T_PROPERTYSHOP A
            LEFT JOIN T_SERVERPARTSHOP B ON A.SERVERPARTSHOP_ID = B.SERVERPARTSHOP_ID
            WHERE A.PROPERTYASSETS_ID IN ({','.join(asset_ids)})
            ORDER BY A.PROPERTYSHOP_STATE, A.ENDDATE DESC"""
        shop_maps = db.execute_query(shop_map_sql)

        # 按 PROPERTYASSETS_ID 分组
        shop_by_asset = {}
        for sm in shop_maps:
            aid = sm.get("PROPERTYASSETS_ID")
            if aid not in shop_by_asset:
                shop_by_asset[aid] = []
            shop_by_asset[aid].append(sm)

        for row in rows:
            aid = row.get("PROPERTYASSETS_ID")
            maps = shop_by_asset.get(aid, [])
            if maps:
                first = maps[0]
                row["SERVERPARTSHOP_ID"] = str(first.get("SERVERPARTSHOP_ID")) if first.get("SERVERPARTSHOP_ID") else None
                row["SHOPNAME"] = first.get("SHOPNAME")
                row["BUSINESS_STATE"] = first.get("BUSINESS_STATE")
                row["ShopList"] = [{
                    "SERVERPARTSHOP_ID": m.get("SERVERPARTSHOP_ID"),
                    "SHOPNAME": m.get("SHOPNAME"),
                    "BUSINESS_STATE": m.get("BUSINESS_STATE"),
                    "BUSINESS_DATE": str(m.get("STARTDATE")) if m.get("STARTDATE") else None,
                    "BUSINESS_ENDDATE": str(m.get("ENDDATE")) if m.get("ENDDATE") else None,
                } for m in maps if m.get("SHOPNAME")]
            else:
                row["ShopList"] = []
    except Exception as e:
        logger.warning(f"关联门店信息查询失败: {e}")


# ========== 2. GetPROPERTYASSETSTreeList ==========

def get_propertyassets_tree_list(db: DatabaseHelper, search_model: SearchModel) -> tuple:
    """
    获取服务区资产 树形分组列表
    对应原 PROPERTYASSETSHelper.GetPROPERTYASSETSTreeList（L540-832）
    简化版：区域→服务区→资产列表（两级树），不含门店匹配逻辑
    """
    # 强制查有效数据
    if search_model.SearchParameter is None:
        search_model.SearchParameter = {}
    search_model.SearchParameter["PROPERTYASSETS_STATE"] = 1

    total_count, assets_list = get_propertyassets_list(db, search_model)
    tree_list = []

    if not assets_list:
        return total_count, tree_list

    # 获取服务区信息
    sp_ids = search_model.SearchParameter.get("SERVERPART_IDS") if search_model.SearchParameter else None
    sp_where = ""
    if sp_ids and str(sp_ids).strip():
        sp_where = f" WHERE SERVERPART_ID IN ({sp_ids})"
    sp_rows = db.execute_query(f"SELECT * FROM T_SERVERPART{sp_where}")
    if not sp_rows:
        return total_count, tree_list

    # 按区域排序
    sp_rows.sort(key=lambda x: (
        x.get("SPREGIONTYPE_INDEX") or 0,
        x.get("SPREGIONTYPE_ID") or 0,
        x.get("SERVERPART_ID") or 0
    ))

    # 构建资产按服务区分组
    assets_by_sp = {}
    for a in assets_list:
        sp_id = a.get("SERVERPART_ID")
        if sp_id not in assets_by_sp:
            assets_by_sp[sp_id] = []
        assets_by_sp[sp_id].append(a)

    # 构建区域分组
    seen_regions = {}
    for sp in sp_rows:
        region_id = sp.get("SPREGIONTYPE_ID") or 0
        if region_id not in seen_regions:
            seen_regions[region_id] = {"info": sp, "serverparts": []}
        seen_regions[region_id]["serverparts"].append(sp)

    for region_id, region_data in seen_regions.items():
        info = region_data["info"]
        region_node = {
            "node": {
                "SPREGIONTYPE_ID": region_id,
                "SPREGIONTYPE_NAME": info.get("SPREGIONTYPE_NAME"),
                "SPREGIONTYPE_INDEX": info.get("SPREGIONTYPE_INDEX"),
                "PROPERTYASSETS_AREA": 0,
                "TOTAL_AREA": 0,
            },
            "children": []
        }

        for sp in region_data["serverparts"]:
            sp_id = sp.get("SERVERPART_ID")
            sp_assets = assets_by_sp.get(sp_id, [])
            if not sp_assets:
                continue

            child_area = sum(a.get("PROPERTYASSETS_AREA") or 0 for a in sp_assets if (a.get("PROPERTYASSETS_TYPE") or 0) > 100)
            parent_area = sum(a.get("PROPERTYASSETS_AREA") or 0 for a in sp_assets if (a.get("PROPERTYASSETS_TYPE") or 0) < 100)

            sp_node = {
                "node": {
                    "SERVERPART_ID": sp_id,
                    "SPREGIONTYPE_ID": region_id,
                    "SPREGIONTYPE_NAME": info.get("SPREGIONTYPE_NAME"),
                    "SPREGIONTYPE_INDEX": info.get("SPREGIONTYPE_INDEX"),
                    "PROPERTYASSETS_AREA": round(child_area, 2),
                    "TOTAL_AREA": parent_area,
                },
                "children": [{"node": a} for a in sorted(sp_assets, key=lambda x: x.get("PROPERTYASSETS_CODE") or "")]
            }
            region_node["children"].append(sp_node)
            region_node["node"]["PROPERTYASSETS_AREA"] = round(
                region_node["node"]["PROPERTYASSETS_AREA"] + child_area, 2)
            region_node["node"]["TOTAL_AREA"] += parent_area

        if region_node["children"]:
            tree_list.append(region_node)

    return total_count, tree_list


# ========== 3. GetAssetsRevenueAmount ==========

def get_assets_revenue_amount(db: DatabaseHelper, search_month: str, serverpart_ids: str) -> list:
    """
    获取服务区资产总效益（每平米效益）
    对应原 PROPERTYASSETSHelper.GetAssetsRevenueAmountList（L868-914）
    查询 PLATFORM_DASHBOARD.T_REVENUEDAILY 表
    """
    result = []
    if not search_month or not serverpart_ids:
        return result

    try:
        sql = f"""SELECT SERVERPART_ID,
                SUM(REVENUE_AMOUNT) AS REVENUE_AMOUNT,
                COUNT(DISTINCT STATISTICS_DATE) AS BUSINESS_DAYS
            FROM T_REVENUEDAILY
            WHERE SERVERPART_ID IN ({serverpart_ids})
                AND TO_CHAR(STATISTICS_DATE, 'YYYYMM') = '{search_month}'
            GROUP BY SERVERPART_ID"""
        rows = db.execute_query(sql)
        for row in rows:
            result.append({
                "SERVERPART_ID": row.get("SERVERPART_ID"),
                "REVENUE_AMOUNT": row.get("REVENUE_AMOUNT"),
                "BUSINESS_DAYS": row.get("BUSINESS_DAYS"),
            })
    except Exception as e:
        logger.warning(f"资产收益查询失败（可能缺少 T_REVENUEDAILY 表）: {e}")

    return result


# ========== 4. GetPROPERTYASSETSDetail ==========

def get_propertyassets_detail(db: DatabaseHelper, propertyassets_id: int) -> Optional[dict]:
    """
    获取服务区资产表明细
    对应原 PROPERTYASSETSHelper.GetPROPERTYASSETSDetail（L305-363）
    """
    sql = f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {propertyassets_id}"
    rows = db.execute_query(sql)
    if not rows:
        return None

    detail = rows[0]

    # 关联门店信息（如果资产有效）
    if detail.get("PROPERTYASSETS_STATE") == 1:
        try:
            # 查询资产关联的门店对照
            shop_sql = f"""SELECT A.*, B.SHOPNAME, B.BUSINESS_STATE, B.SERVERPARTSHOP_ID AS SHOP_ID
                FROM T_PROPERTYSHOP A
                LEFT JOIN T_SERVERPARTSHOP B ON A.SERVERPARTSHOP_ID = B.SERVERPARTSHOP_ID
                WHERE A.PROPERTYASSETS_ID = {propertyassets_id} AND A.PROPERTYSHOP_STATE = 1"""
            shop_rows = db.execute_query(shop_sql)
            if shop_rows:
                first_shop = shop_rows[0]
                detail["PropertyShop"] = {
                    "SERVERPARTSHOP_ID": first_shop.get("SERVERPARTSHOP_ID"),
                    "SHOPNAME": first_shop.get("SHOPNAME"),
                    "BUSINESS_STATE": first_shop.get("BUSINESS_STATE"),
                }
            else:
                detail["PropertyShop"] = None
        except Exception as e:
            logger.warning(f"资产明细关联门店查询失败: {e}")
            detail["PropertyShop"] = None

    detail["BusinessProjectList"] = []
    return detail


# ========== 5. SynchroPROPERTYASSETS ==========

def synchro_propertyassets(db: DatabaseHelper, data: dict) -> tuple:
    """
    同步服务区资产表（新增/更新）
    对应原 PROPERTYASSETSHelper.SynchroPROPERTYASSETS（L367-505）
    返回: (成功, 资产ID, 提示信息)
    """
    # 必填校验
    if not data.get("PROPERTYASSETS_CODE"):
        return False, 0, "资产编码必填"
    if data.get("SERVERPART_ID") is None:
        return False, 0, "服务区内码必填"

    assets_id = data.get("PROPERTYASSETS_ID")
    assets_code = data["PROPERTYASSETS_CODE"]
    serverpart_id = data["SERVERPART_ID"]

    # 检查资产编码唯一性
    check_sql = f"""SELECT PROPERTYASSETS_ID FROM {TABLE_NAME}
        WHERE PROPERTYASSETS_STATE = 1 AND PROPERTYASSETS_CODE = '{assets_code}'
        AND SERVERPART_ID = {serverpart_id}"""
    existing = db.execute_query(check_sql)
    if existing:
        existing_id = existing[0].get("PROPERTYASSETS_ID")
        if assets_id is not None:
            if str(existing_id) != str(assets_id):
                return False, 0, "资产请求内码错误，或资产编号重复"
        else:
            return False, 0, "资产编码不唯一，请核对编码"

    # 父类资产唯一性检查（TYPE < 100）
    assets_type = data.get("PROPERTYASSETS_TYPE")
    if assets_type is not None and int(assets_type) < 100:
        region = data.get("PROPERTYASSETS_REGION")
        parent_check = f"""SELECT PROPERTYASSETS_ID, PROPERTYASSETS_CODE FROM {TABLE_NAME}
            WHERE PROPERTYASSETS_STATE = 1 AND PROPERTYASSETS_TYPE = {assets_type}
            AND PROPERTYASSETS_REGION = {region} AND SERVERPART_ID = {serverpart_id}"""
        parent_rows = db.execute_query(parent_check)
        if parent_rows:
            if assets_id is None:
                return False, 0, "资产父类不唯一，请核对类型"
            elif str(parent_rows[0].get("PROPERTYASSETS_ID")) != str(assets_id):
                return False, 0, f"资产父类已存在，资产编码为：{parent_rows[0].get('PROPERTYASSETS_CODE')}"

    # 移除非数据库字段
    db_data = {k: v for k, v in data.items() if k not in EXCLUDE_FIELDS}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if assets_id is not None:
        # 更新模式
        check = db.execute_query(f"SELECT * FROM {TABLE_NAME} WHERE {PRIMARY_KEY} = {assets_id}")
        if not check:
            return False, 0, "未找到请求数据"

        ori = check[0]
        # 保留创建人信息
        db_data["STAFF_ID"] = ori.get("STAFF_ID")
        db_data["STAFF_NAME"] = ori.get("STAFF_NAME")
        db_data["CREATE_DATE"] = ori.get("CREATE_DATE")
        db_data["OPERATE_DATE"] = now

        set_parts = []
        for key, value in db_data.items():
            if key == PRIMARY_KEY:
                continue
            if value is None:
                continue
            if isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            elif isinstance(value, datetime):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            update_sql = f"UPDATE {TABLE_NAME} SET {', '.join(set_parts)} WHERE {PRIMARY_KEY} = {assets_id}"
            db.execute_non_query(update_sql)

        # 记录操作日志（简化版）
        _write_log(db, assets_id, "修改", "Update",
                    data.get("OPERATOR_ID"), data.get("OPERATOR_NAME"), 2)

        return True, int(assets_id), ""
    else:
        # 新增模式
        try:
            new_id = db.execute_scalar("SELECT SEQ_PROPERTYASSETS.NEXTVAL FROM DUAL")
        except Exception:
            new_id = (db.execute_scalar(f"SELECT MAX({PRIMARY_KEY}) FROM {TABLE_NAME}") or 0) + 1

        db_data["PROPERTYASSETS_ID"] = new_id
        db_data["CREATE_DATE"] = now
        db_data["OPERATE_DATE"] = now

        columns = []
        values = []
        for key, value in db_data.items():
            if value is None:
                continue
            columns.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            elif isinstance(value, datetime):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        insert_sql = f"INSERT INTO {TABLE_NAME} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        db.execute_non_query(insert_sql)

        # 记录新增日志
        _write_log(db, new_id, "新增", "Create",
                    data.get("OPERATOR_ID"), data.get("OPERATOR_NAME"), 1)

        data["PROPERTYASSETS_ID"] = new_id
        return True, int(new_id), ""


# ========== 6. BatchPROPERTYASSETS ==========

def batch_propertyassets(db: DatabaseHelper, model_list: list) -> tuple:
    """
    批量同步服务区资产表
    对应原 Controller.BatchPROPERTYASSETS（L2358-2443）
    返回: (成功, 提示信息)
    """
    if not model_list:
        return False, "资产列表不能为空"

    # 校验必填
    for m in model_list:
        if not m.get("PROPERTYASSETS_CODE") or m.get("SERVERPART_ID") is None:
            return False, "同步失败：资产编码,服务区内码必填"

    for model in model_list:
        success, assets_id, message = synchro_propertyassets(db, model)
        if not success:
            return False, message or "更新失败，数据不存在！"

        # 处理关联门店（SERVERPARTSHOP_ID）
        shop_id = model.get("SERVERPARTSHOP_ID")
        if shop_id is not None:
            try:
                # 简化版：直接插入对照记录
                from services.base_info import propertyshop_service
                shop_data = {
                    "PROPERTYASSETS_ID": assets_id,
                    "SERVERPARTSHOP_ID": int(shop_id) if int(shop_id) != -1 else None,
                    "SERVERPART_ID": model.get("SERVERPART_ID"),
                    "STAFF_ID": model.get("STAFF_ID"),
                    "STAFF_NAME": model.get("STAFF_NAME"),
                    "OPERATOR_ID": model.get("STAFF_ID"),
                    "OPERATOR_NAME": model.get("STAFF_NAME"),
                }
                if int(shop_id) != -1:
                    propertyshop_service.synchro_propertyshop(db, shop_data)
            except Exception as e:
                logger.warning(f"关联门店处理失败: {e}")

    return True, ""


# ========== 7. DeletePROPERTYASSETS ==========

def delete_propertyassets(db: DatabaseHelper, propertyassets_id: int,
                           operate_id: int = 0, operate_name: str = "") -> bool:
    """
    删除服务区资产表（软删除 PROPERTYASSETS_STATE=0，含操作人记录）
    对应原 PROPERTYASSETSHelper.DeletePROPERTYASSETS（L509-536）
    """
    sql = f"""UPDATE {TABLE_NAME} SET PROPERTYASSETS_STATE = 0,
        OPERATOR_ID = '{operate_id}', OPERATOR_NAME = '{operate_name}'
        WHERE {PRIMARY_KEY} = {propertyassets_id}"""
    affected = db.execute_non_query(sql)
    if affected and affected > 0:
        _write_log(db, propertyassets_id, "状态", "Delete",
                    operate_id, operate_name, 3)
        return True
    return False


# ========== 辅助函数 ==========

def _write_log(db: DatabaseHelper, assets_id: int, op_type: str, op_desc: str,
                operator_id, operator_name, change_type: int = 2):
    """写操作日志到 T_PROPERTYASSETSLOG（简化版）"""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_sql = f"""INSERT INTO T_PROPERTYASSETSLOG
            (PROPERTYASSETS_ID, OPERATE_TYPE, OPERATE_DESC,
             OPERATOR_ID, OPERATOR_NAME, OPERATE_DATE, CHANGE_TYPE)
            VALUES ({assets_id}, '{op_type}', '{op_desc}',
             {operator_id or 0}, '{operator_name or ""}', '{now}', {change_type})"""
        db.execute_non_query(log_sql)
    except Exception as e:
        logger.warning(f"写操作日志失败: {e}")
