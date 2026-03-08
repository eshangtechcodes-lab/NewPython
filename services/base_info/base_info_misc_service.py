from __future__ import annotations
# -*- coding: utf-8 -*-
"""
基础信息-散装独立接口 业务服务
替代原 BaseInfoController 中不属于标准 CRUD 的独立接口

接口列表:
- GetShopShortNames: 获取服务区门店简称列表
- GetServerpartShopInfo: 根据编码获取门店信息
- GetServerpartDDL: 服务区下拉框
- GetServerpartTree: 区域服务区树
- GetSPRegionShopTree: 区域服务区门店树
- GetServerpartShopDDL: 门店下拉框
- GetServerpartShopTree: 服务区门店树
- GetNestingOwnerUnitList: 业主嵌套列表
- BindingOwnerUnitDDL: 业主下拉框
- BindingOwnerUnitTree: 业主树
- BindingMerchantTree: 商户树
- GetBusinessBrandList: 门店品牌列表
- ModifyShopState: 变更门店状态
- GetShopReceivables: 门店合同信息
- GetServerpartUDTypeTree: 自定义类别树
- GetServerPartShopNewList: 门店列表(业主)
- GetServerPartShopNewDetail: 门店明细(业主)
- ServerPartShopNewSaveState: 设置门店状态
- SynchroServerPartShopNew: 同步门店(业主)
- GetSERVERPARTDetail: 服务区详情
- SynchroSERVERPART: 同步服务区
"""
from typing import Optional, List
from loguru import logger
from core.database import DatabaseHelper


# =====================================
# 1. GetShopShortNames - 获取服务区门店简称
#    对应原 ServerpartShopHelper.GetShopShortNames
#    应用场景: 查询自营业态有哪些门店
# =====================================
def get_shop_short_names(
    db: DatabaseHelper,
    serverpart_id: str,
    shop_trade: Optional[str] = None,
    business_type: Optional[str] = "1000",
    business_state: Optional[str] = None,
    shop_valid: Optional[int] = 1,
    exclude_staff_meal: bool = True,
    show_finance: bool = False
) -> list:
    """
    获取服务区门店简称列表
    返回: List[str] 门店简称列表
    """
    if not serverpart_id or not serverpart_id.strip():
        return []

    sql_where = ""

    # 过滤服务区
    if serverpart_id and serverpart_id.strip():
        sql_where += f" AND A.SERVERPART_ID IN ({serverpart_id})"

    # 过滤商品业态
    if shop_trade and shop_trade.strip():
        sql_where += f" AND A.SHOPTRADE IN ({shop_trade})"
    elif exclude_staff_meal:
        # 排除员工餐 (SHOPTRADE=3999)
        sql_where += " AND A.SHOPTRADE <> 3999"

    # 只显示财务共享业态
    if show_finance:
        sql_where += " AND A.SHOPTRADE >= '2000' AND A.SHOPTRADE < '9050'"
        if business_type == "2000":
            sql_where += " AND A.SHOPSHORTNAME LIKE '%提成%'"

    # 过滤经营模式
    if business_type and business_type.strip():
        sql_where += f" AND A.BUSINESS_TYPE IN ({business_type})"

    # 过滤经营状态
    if business_state and business_state.strip():
        sql_where += f" AND A.BUSINESS_STATE IN ({business_state})"

    # 过滤门店有效状态
    if shop_valid is not None:
        sql_where += f" AND A.ISVALID = {shop_valid}"

    sql = f"""SELECT DISTINCT A.SHOPSHORTNAME
        FROM T_SERVERPARTSHOP A
        WHERE A.SHOPSHORTNAME IS NOT NULL
          AND EXISTS (SELECT 1 FROM T_SERVERPART B
              WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.STATISTICS_TYPE = 1000)
          {sql_where}
        ORDER BY A.SHOPSHORTNAME"""

    rows = db.execute_query(sql)
    # 返回简称字符串列表（去重、排序）
    return [r.get("SHOPSHORTNAME", "") for r in rows if r.get("SHOPSHORTNAME")]


# =====================================
# 2. GetServerpartShopInfo - 根据编码获取门店信息
#    对应原 ServerpartShopHelper.GetShopInfoByCode
# =====================================
def get_serverpart_shop_info(
    db: DatabaseHelper,
    serverpart_code: str,
    shop_code: str
) -> dict:
    """
    根据服务区编码和门店编码获取门店信息
    对应原 ServerpartShopHelper.GetShopInfoByCode
    """
    sql = f"""SELECT A.*, B.SERVERPART_NAME, B.SERVERPART_CODE, B.OWNERUNIT_NAME
        FROM T_SERVERPARTSHOP A
        LEFT JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
        WHERE B.SERVERPART_CODE = '{serverpart_code}'
          AND A.SHOPCODE = '{shop_code}'
          AND ROWNUM = 1"""
    rows = db.execute_query(sql)
    if not rows:
        return {}

    row = rows[0]
    
    # 映射到 ServerpartShopModel (驼峰命名)
    model = {
        "ServerpartShopId": row.get("SERVERPARTSHOP_ID"),
        "ServerpartShop_Code": row.get("SHOPCODE"),
        "ServerpartShop_Name": row.get("SHOPNAME"),
        "Serverpart_Id": row.get("SERVERPART_ID"),
        "Serverpart_Code": row.get("SERVERPART_CODE"),
        "Serverpart_Name": row.get("SERVERPART_NAME"),
        "ServerpartShop_Trade": row.get("SHOPTRADE"),
        "ServerpartShop_Region": row.get("SHOPREGION"),
        "ServerpartShop_ShortName": row.get("SHOPSHORTNAME"),
        "OwnerUnit_Id": row.get("OWNERUNIT_ID"),
        "OwnerUnit_Name": row.get("OWNERUNIT_NAME"),
        "Business_TradeName": row.get("BUSINESS_TRADENAME"),
        "Business_BrandName": row.get("BRAND_NAME"),
        "Business_BrandIcon": "https://user.eshangtech.com",  # 默认值
        "Business_Type": row.get("BUSINESS_TYPE"),
        "Business_State": row.get("BUSINESS_STATE"),
        "Transfer_Type": row.get("TRANSFER_TYPE"),
        "InSalesType": row.get("INSALES_TYPE"),
        "ServerpartShop_State": row.get("ISVALID")
    }

    # 获取品牌图标逻辑
    business_brand = row.get("BUSINESS_BRAND")
    if business_brand:
        brand_sql = f"SELECT BRAND_INTRO FROM T_BRAND WHERE BRAND_ID = {business_brand}"
        brand_rows = db.execute_query(brand_sql)
        if brand_rows and brand_rows[0].get("BRAND_INTRO"):
            # 参考原 C#: Config.AppSettings.CoopMerchantUrls + _BRAND.BRAND_INTRO
            # 基准数据中显示为 https://user.eshangtech.com
            model["Business_BrandIcon"] = "https://user.eshangtech.com" + brand_rows[0]["BRAND_INTRO"]

    return model


# =====================================
# 辅助函数: 省份编码 -> FIELDENUM_ID 映射
#   对应原 DictionaryHelper.GetFieldEnum("DIVISION_CODE", ProvinceCode)
# =====================================
def _get_province_id_by_code(db: DatabaseHelper, province_code: str) -> Optional[int]:
    """
    将省份编码（如 340000）映射为 FIELDENUM_ID（T_SERVERPART.PROVINCE_CODE 的值）
    查询路径: T_FIELDENUM(FIELDEXPLAIN_ID=154, VALUE=省份编码) -> FIELDENUM_ID
    FIELDEXPLAIN_ID=154 对应 DIVISION_CODE
    """
    sql = f"SELECT FIELDENUM_ID FROM T_FIELDENUM WHERE FIELDEXPLAIN_ID = 154 AND FIELDENUM_VALUE = '{province_code}'"
    rows = db.execute_query(sql)
    if rows:
        return rows[0].get("FIELDENUM_ID")
    return None


# =====================================
# 3. GetServerpartDDL - 服务区下拉框
#    对应原 ServerpartHelper.GetServerpartDDL
# =====================================
def get_serverpart_ddl(
    db: DatabaseHelper,
    serverpart_codes: Optional[str] = None,
    province_code: Optional[str] = None,
    serverpart_type: str = "1000",
    statistics_type: Optional[str] = None
) -> list:
    """
    获取服务区下拉框数据
    返回: List[dict] 含 label(名称) 和 value(内码)
    """
    where_parts = []

    # 按服务区编码筛选
    if serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"SERVERPART_CODE IN ('{codes}')")
    elif province_code and province_code.strip():
        # 按省份编码筛选 — 先查省份对应的内码
        province_id = _get_province_id_by_code(db, province_code)
        if province_id:
            where_parts.append(f"PROVINCE_CODE = {province_id}")

    # 服务区类型（站点类型）
    if serverpart_type and serverpart_type.strip():
        where_parts.append(f"STATISTICS_TYPE IN ({serverpart_type})")

    # 统计类型
    if statistics_type and statistics_type.strip():
        where_parts.append(f"STATISTIC_TYPE IN ({statistics_type})")

    where_sql = " WHERE " + " AND ".join(where_parts) if where_parts else ""

    sql = f"""SELECT SERVERPART_ID, SERVERPART_NAME
        FROM T_SERVERPART{where_sql}
        ORDER BY SERVERPART_INDEX, SERVERPART_CODE"""

    rows = db.execute_query(sql)
    return [{"label": r.get("SERVERPART_NAME", ""),
             "value": str(r.get("SERVERPART_ID", ""))} for r in rows]


# =====================================
# 4. GetServerpartTree - 区域服务区树
#    对应原 ServerpartHelper.GetServerpartTree (L405-658)
#    树形结构: 区域(type=0) -> 服务区(type=1)
# =====================================
def get_serverpart_tree(
    db: DatabaseHelper,
    province_code: int,
    sp_region_type_id: Optional[int] = None,
    serverpart_type: str = "1000",
    statistics_type: Optional[str] = None,
    serverpart_ids: Optional[str] = None,
    serverpart_codes: Optional[str] = None,
    show_sp_region: bool = True,
    show_royalty: bool = False,
    show_compact_count: bool = False,
    just_serverpart: bool = False
) -> list:
    """
    获取区域服务区树形结构
    返回: List[dict] 树形节点列表
    节点字段: label, value(int), key(str), type(int), ico(null), desc(str|null), children(list|null)
    """
    # ---- 构建 WHERE 条件（参考原 Helper L412-444） ----
    # 原 C# 中 ShowRoyalty 时条件用 "A." 前缀，此处简化为单表别名
    where_parts = [f"STATISTICS_TYPE IN ({serverpart_type})"]

    if statistics_type and statistics_type.strip():
        where_parts.append(f"STATISTIC_TYPE IN ({statistics_type})")

    if sp_region_type_id is not None:
        where_parts.append(f"SPREGIONTYPE_ID IN ({sp_region_type_id})")

    if serverpart_ids and serverpart_ids.strip():
        where_parts.append(f"SERVERPART_ID IN ({serverpart_ids})")

    if serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"SERVERPART_CODE IN ('{codes}')")
    elif province_code is not None:
        # T_SERVERPART.PROVINCE_CODE 存的是 FIELDENUM_ID（如 3544=安徽省）
        # 用 SQL 子查询直接映射: ProvinceCode(340000) -> FIELDENUM_ID
        where_parts.append(
            f"PROVINCE_CODE = (SELECT FIELDENUM_ID FROM T_FIELDENUM "
            f"WHERE FIELDEXPLAIN_ID = 154 AND FIELDENUM_VALUE = '{province_code}')"
        )

    where_sql = " WHERE " + " AND ".join(where_parts)

    # ---- 查询服务区数据（参考原 Helper L449-467） ----
    if show_royalty:
        # ShowRoyalty 模式：JOIN T_SERVERPARTSHOP 统计门店数
        sp_sql = f"""SELECT
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                A.PROVINCE_CODE, A.SERVERPART_TYPE, A.STATISTIC_TYPE,
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                COUNT(DISTINCT B.SHOPSHORTNAME) AS SHOP_COUNT
            FROM T_SERVERPART A, T_SERVERPARTSHOP B
            {where_sql.replace('STATISTICS_TYPE', 'A.STATISTICS_TYPE').replace('STATISTIC_TYPE', 'A.STATISTIC_TYPE').replace('SPREGIONTYPE_ID', 'A.SPREGIONTYPE_ID').replace('SERVERPART_ID', 'A.SERVERPART_ID').replace('SERVERPART_CODE', 'A.SERVERPART_CODE').replace('PROVINCE_CODE', 'A.PROVINCE_CODE')}
                AND A.SERVERPART_ID = B.SERVERPART_ID AND B.ROYALTYRATE IS NOT NULL
            GROUP BY
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                A.PROVINCE_CODE, A.SERVERPART_TYPE, A.STATISTIC_TYPE,
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX"""
    else:
        sp_sql = f"SELECT * FROM T_SERVERPART{where_sql}"
    sp_sql += " ORDER BY SPREGIONTYPE_INDEX, SPREGIONTYPE_ID, SERVERPART_INDEX, SERVERPART_CODE"

    sp_rows = db.execute_query(sp_sql)

    # ---- 构建树形结构（参考原 Helper L499-553） ----
    result = []

    if show_sp_region:
        # 查询区域类型表 T_SERVERPARTTYPE
        # 注意: 这里用原始 province_code (如 340000)，原 C# 直接用 ProvinceCode 参数值
        region_where = f"SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = {province_code}"
        if sp_region_type_id is not None:
            region_where += f" AND SERVERPARTTYPE_ID = {sp_region_type_id}"
        region_sql = f"SELECT * FROM T_SERVERPARTTYPE WHERE {region_where} ORDER BY TYPE_INDEX, SERVERPARTTYPE_ID"
        region_rows = db.execute_query(region_sql)

        # 遍历区域，构建树节点（原 Helper L506-539）
        assigned_sp_ids = set()
        for region in region_rows:
            region_id = region.get("SERVERPARTTYPE_ID")
            # 收集属于该区域的服务区
            children = []
            for sp in sp_rows:
                if sp.get("SPREGIONTYPE_ID") == region_id:
                    sp_node = {
                        "label": sp.get("SERVERPART_NAME", ""),
                        "value": sp.get("SERVERPART_ID"),
                        "key": f"1-{sp.get('SERVERPART_ID')}",
                        "type": 1,
                        "desc": str(sp.get("SHOP_COUNT", "")) if sp.get("SHOP_COUNT") is not None else None,
                        "ico": None,
                    }
                    children.append(sp_node)
                    assigned_sp_ids.add(sp.get("SERVERPART_ID"))

            if children:
                # 区域 desc: 累计子节点的 desc（门店数）
                desc_sum = 0
                for ch in children:
                    try:
                        desc_sum += int(ch.get("desc") or 0)
                    except (ValueError, TypeError):
                        pass
                region_node = {
                    "label": region.get("TYPE_NAME", ""),
                    "value": region_id,
                    "key": f"0-{region_id}",
                    "type": 0,
                    "ico": None,
                    "desc": str(desc_sum) if desc_sum else "0",
                    "children": children,
                }
                result.append(region_node)

        # 追加无区域归属的服务区（原 Helper L542-545）
        for sp in sp_rows:
            sp_id = sp.get("SERVERPART_ID")
            if sp_id not in assigned_sp_ids:
                result.append({
                    "label": sp.get("SERVERPART_NAME", ""),
                    "value": sp.get("SERVERPART_ID"),
                    "key": f"1-{sp.get('SERVERPART_ID')}",
                    "type": 1,
                    "desc": str(sp.get("SHOP_COUNT", "")) if sp.get("SHOP_COUNT") is not None else None,
                    "ico": None,
                })
    else:
        # 不显示区域（原 Helper L550-553）
        for sp in sp_rows:
            result.append({
                "label": sp.get("SERVERPART_NAME", ""),
                "value": sp.get("SERVERPART_ID"),
                "key": f"1-{sp.get('SERVERPART_ID')}",
                "type": 1,
                "desc": str(sp.get("SHOP_COUNT", "")) if sp.get("SHOP_COUNT") is not None else None,
                "ico": None,
            })

    return result


# =====================================
# 5. GetServerpartShopDDL - 门店下拉框
#    对应原 ServerpartShopHelper.GetServerpartShopDDL
# =====================================
def get_serverpart_shop_ddl(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_id: Optional[str] = None,
    serverpart_codes: Optional[str] = None
) -> list:
    """
    获取门店下拉框数据
    返回: List[dict] 含 label(门店名称) 和 value(门店内码)
    """
    where_parts = ["ISVALID = 1"]

    if serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"SERVERPART_CODE IN ('{codes}')")
    elif serverpart_id and serverpart_id.strip():
        where_parts.append(f"SERVERPART_ID IN ({serverpart_id})")
    elif province_code is not None:
        province_id = _get_province_id_by_code(db, str(province_code))
        if province_id:
            where_parts.append(
                f"EXISTS (SELECT 1 FROM T_SERVERPART WHERE T_SERVERPART.SERVERPART_ID = T_SERVERPARTSHOP.SERVERPART_ID AND PROVINCE_CODE = {province_id})"
            )

    where_sql = " WHERE " + " AND ".join(where_parts)
    sql = f"""SELECT SERVERPARTSHOP_ID, SHOPNAME
        FROM T_SERVERPARTSHOP{where_sql}
        ORDER BY SERVERPART_NAME, SHOPTRADE, SHOPSHORTNAME, SHOPREGION, SHOPCODE"""

    rows = db.execute_query(sql)
    return [{"label": r.get("SHOPNAME", ""),
             "value": str(r.get("SERVERPARTSHOP_ID", ""))} for r in rows]


# =====================================
# 6. GetNestingOwnerUnitList - 业主单位嵌套列表
#    对应原 OwnerUnitHelper.GetNestingOwnerUnitList
# =====================================
def get_nesting_ownerunit_list(
    db: DatabaseHelper,
    ownerunit_pid: int = -1,
    show_status: bool = False,
    province_code: Optional[int] = None,
    ownerunit_nature: Optional[str] = None,
    ownerunit_name: Optional[str] = None
) -> list:
    """
    获取业主单位嵌套列表（递归树结构）
    返回: List[dict] 嵌套节点
    """
    where_parts = []

    if show_status:
        where_parts.append("OWNERUNIT_STATE = 1")

    if province_code is not None:
        where_parts.append(f"PROVINCE_CODE = {province_code}")

    if ownerunit_nature and ownerunit_nature.strip():
        where_parts.append(f"OWNERUNIT_NATURE IN ({ownerunit_nature})")

    where_sql = " WHERE " + " AND ".join(where_parts) if where_parts else ""
    sql = f"SELECT * FROM T_OWNERUNIT{where_sql} ORDER BY OWNERUNIT_INDEX, OWNERUNIT_ID"
    all_rows = db.execute_query(sql)

    def build_tree(parent_id):
        children = []
        for row in all_rows:
            pid = row.get("OWNERUNIT_PID")
            if pid is None:
                pid = -1
            if int(pid) == int(parent_id):
                # 模糊查询过滤
                name = row.get("OWNERUNIT_NAME", "")
                child_nodes = build_tree(row.get("OWNERUNIT_ID"))
                # 如果有模糊查询条件，过滤不匹配的叶子节点
                if ownerunit_name and ownerunit_name.strip():
                    if ownerunit_name not in name and not child_nodes:
                        continue
                children.append({
                    "node": row,
                    "children": child_nodes
                })
        return children

    return build_tree(ownerunit_pid)


# =====================================
# 7. BindingOwnerUnitDDL - 业主单位下拉框
#    对应原 OwnerUnitHelper.BindingOwnerUnitDDL
# =====================================
def binding_ownerunit_ddl(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    data_type: int = 0
) -> list:
    """
    获取业主单位下拉框
    data_type: 0=返回编码, 1=返回内码
    返回: List[dict] 含 label 和 value
    """
    where_parts = ["OWNERUNIT_STATE = 1", "OWNERUNIT_NATURE = 1000"]

    if province_code is not None:
        where_parts.append(f"PROVINCE_CODE = {province_code}")

    where_sql = " WHERE " + " AND ".join(where_parts)
    value_field = "OWNERUNIT_ID"  # T_OWNERUNIT 表无 OWNERUNIT_CODE 列，统一用 OWNERUNIT_ID

    sql = f"""SELECT OWNERUNIT_ID, OWNERUNIT_NAME
        FROM T_OWNERUNIT{where_sql}
        ORDER BY OWNERUNIT_INDEX, OWNERUNIT_ID"""

    rows = db.execute_query(sql)
    return [{"label": r.get("OWNERUNIT_NAME", ""),
             "value": r.get(value_field),
             "type": 1} for r in rows]


# =====================================
# 8. BindingOwnerUnitTree - 业主单位树
#    对应原 OwnerUnitHelper.BindingOwnerUnitTree
# =====================================
def binding_ownerunit_tree(
    db: DatabaseHelper,
    data_type: int = 0,
    ownerunit_pid: int = -1
) -> list:
    """
    获取业主单位树
    返回: List[dict] 嵌套树
    """
    where_parts = ["OWNERUNIT_STATE = 1", "OWNERUNIT_NATURE = 1000"]
    where_sql = " WHERE " + " AND ".join(where_parts)
    value_field = "OWNERUNIT_ID"  # T_OWNERUNIT 表无 OWNERUNIT_CODE 列，统一用 OWNERUNIT_ID

    sql = f"SELECT * FROM T_OWNERUNIT{where_sql} ORDER BY OWNERUNIT_INDEX, OWNERUNIT_ID"
    all_rows = db.execute_query(sql)

    def build_tree(parent_id):
        children = []
        for row in all_rows:
            pid = row.get("OWNERUNIT_PID")
            if pid is None:
                pid = -1
            if int(pid) == int(parent_id):
                child_nodes = build_tree(row.get("OWNERUNIT_ID"))
                node = {
                    "label": row.get("OWNERUNIT_NAME", ""),
                    "value": row.get(value_field),
                    "type": 1,
                    "key": f"1-{row.get('OWNERUNIT_ID')}"
                }
                item = {"node": node, "children": child_nodes}
                children.append(item)
        return children

    return build_tree(ownerunit_pid)


# =====================================
# 9. BindingMerchantTree - 经营商户树
#    对应原 OwnerUnitHelper.BindingOwnerUnitTree (nature=2000)
# =====================================
def binding_merchant_tree(
    db: DatabaseHelper,
    merchant_pid: int = -1,
    province_code: Optional[int] = None
) -> list:
    """
    获取经营商户树（调用业主单位树，nature=2000）
    返回: List[dict] 嵌套树
    """
    where_parts = ["OWNERUNIT_STATE = 1", "OWNERUNIT_NATURE = 2000"]
    if province_code is not None:
        where_parts.append(f"PROVINCE_CODE = {province_code}")

    where_sql = " WHERE " + " AND ".join(where_parts)

    sql = f"SELECT * FROM T_OWNERUNIT{where_sql} ORDER BY OWNERUNIT_INDEX, OWNERUNIT_ID"
    all_rows = db.execute_query(sql)

    def build_tree(parent_id):
        children = []
        for row in all_rows:
            pid = row.get("OWNERUNIT_PID")
            if pid is None:
                pid = -1
            if int(pid) == int(parent_id):
                child_nodes = build_tree(row.get("OWNERUNIT_ID"))
                node = {
                    "label": row.get("OWNERUNIT_NAME", ""),
                    "value": row.get("OWNERUNIT_ID"),
                    "type": 1,
                    "key": f"1-{row.get('OWNERUNIT_ID')}"
                }
                item = {"node": node, "children": child_nodes}
                children.append(item)
        return children

    return build_tree(merchant_pid)


# =====================================
# 10. GetBusinessBrandList - 门店经营品牌列表
#     对应原 BRANDHelper.GetBusinessBrandList
# =====================================
def get_business_brand_list(
    db: DatabaseHelper,
    serverpart_shop_ids: str
) -> list:
    """
    获取门店经营品牌列表
    返回: List[dict]
    """
    if not serverpart_shop_ids or not serverpart_shop_ids.strip():
        return []

    sql = f"""SELECT DISTINCT B.*
        FROM T_SERVERPARTSHOP A
        LEFT JOIN T_BRAND B ON A.BUSINESS_BRAND = B.BRAND_ID
        WHERE A.SERVERPARTSHOP_ID IN ({serverpart_shop_ids})
          AND B.BRAND_ID IS NOT NULL
        ORDER BY B.BRAND_NAME"""

    return db.execute_query(sql)


# =====================================
# 11. ModifyShopState - 变更门店经营状态
#     对应原 ServerpartShopHelper.ModifyShopState
# =====================================
def modify_shop_state(
    db: DatabaseHelper,
    shop_modify_list: list
) -> bool:
    """
    批量变更门店经营状态
    shop_modify_list: List[dict] 含 SERVERPARTSHOP_ID, BUSINESS_STATE 等字段
    """
    if not shop_modify_list:
        return False

    for item in shop_modify_list:
        shop_id = item.get("SERVERPARTSHOP_ID")
        business_state = item.get("BUSINESS_STATE")
        if shop_id is None or business_state is None:
            continue

        sql = f"""UPDATE T_SERVERPARTSHOP
            SET BUSINESS_STATE = {business_state}
            WHERE SERVERPARTSHOP_ID = {shop_id}"""
        db.execute_non_query(sql)

    return True


# =====================================
# 12. GetSERVERPARTDetail - 服务区详情
#     对应原 ServerpartHelper.GetSERVERPARTDetail
# =====================================
def get_serverpart_detail(
    db: DatabaseHelper,
    serverpart_id: Optional[int] = None,
    field_enum_id: Optional[int] = None
) -> dict:
    """
    获取服务区详情
    可通过 serverpart_id 或 field_enum_id 查询
    """
    if serverpart_id is not None:
        sql = f"SELECT * FROM T_SERVERPART WHERE SERVERPART_ID = {serverpart_id}"
    elif field_enum_id is not None:
        sql = f"SELECT * FROM T_SERVERPART WHERE FIELDENUM_ID = {field_enum_id}"
    else:
        return {}

    rows = db.execute_query(sql)
    if not rows:
        return {}

    sp = rows[0]

    # 关联附属信息 RTSERVERPARTSHOP
    try:
        rt_sql = f"SELECT * FROM T_RTSERVERPARTSHOP WHERE SERVERPART_ID = {sp.get('SERVERPART_ID')}"
        rt_rows = db.execute_query(rt_sql)
        sp["RtServerPart"] = rt_rows[0] if rt_rows else {}
    except Exception:
        sp["RtServerPart"] = {}

    # 关联服务区详情 SERVERPARTINFO
    info_sql = f"SELECT * FROM T_SERVERPARTINFO WHERE SERVERPART_ID = {sp.get('SERVERPART_ID')} ORDER BY SERVERPART_REGION"
    try:
        info_rows = db.execute_query(info_sql)
        sp["ServerPartInfo"] = info_rows
    except Exception:
        sp["ServerPartInfo"] = []

    return sp


# =====================================
# 13. GetServerpartUDTypeTree - 服务区自定义类别树
#     对应原 USERDEFINEDTYPEHelper.GetServerpartUDTypeTree
# =====================================
def get_serverpart_ud_type_tree(
    db: DatabaseHelper,
    serverpart_id: str,
    shop_trade: Optional[str] = None,
    user_defined_type_state: Optional[int] = 1
) -> list:
    """
    获取服务区自定义类别树
    返回: List[dict] 嵌套树（按服务区分组 -> 门店 -> 类别）
    """
    where_parts = []

    if serverpart_id and serverpart_id.strip():
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_id})")

    if user_defined_type_state is not None:
        where_parts.append(f"A.USERDEFINEDTYPE_STATE = {user_defined_type_state}")

    if shop_trade and shop_trade.strip():
        where_parts.append(f"A.SHOPTRADE IN ({shop_trade})")

    where_sql = " WHERE " + " AND ".join(where_parts) if where_parts else ""

    sql = f"""SELECT A.*, B.SERVERPART_NAME
        FROM T_USERDEFINEDTYPE A
        LEFT JOIN T_SERVERPART B ON A.SERVERPART_ID = B.SERVERPART_ID
        {where_sql}
        ORDER BY B.SERVERPART_NAME, A.USERDEFINEDTYPE_INDEX"""

    rows = db.execute_query(sql)

    # 按服务区分组构建树
    sp_map = {}
    for row in rows:
        sp_id = row.get("SERVERPART_ID")
        sp_name = row.get("SERVERPART_NAME", "")
        if sp_id not in sp_map:
            sp_map[sp_id] = {
                "node": {
                    "label": sp_name,
                    "value": sp_id,
                    "type": 0,
                    "key": f"0-{sp_id}"
                },
                "children": []
            }
        sp_map[sp_id]["children"].append({
            "node": {
                "label": row.get("USERDEFINEDTYPE_NAME", ""),
                "value": row.get("USERDEFINEDTYPE_ID"),
                "type": 1,
                "key": f"1-{row.get('USERDEFINEDTYPE_ID')}"
            },
            "children": []
        })

    return list(sp_map.values())


# =====================================
# 14. GetSPRegionShopTree - 区域服务区门店树
#     对应原 ServerpartShopHelper.GetSPRegionShopTree
# =====================================
def get_sp_region_shop_tree(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_id: Optional[str] = None,
    serverpart_codes: Optional[str] = None,
    serverpartshop_id: Optional[str] = None,
    business_state: Optional[str] = None,
    business_type: Optional[str] = None,
    show_state: bool = False,
    show_short_name: bool = False,
    show_in_sale: bool = False,
    sort_str: Optional[str] = None,
    show_royalty: bool = False,
    show_unpaid_expense: bool = False
) -> list:
    """
    获取区域服务区门店树
    返回: List[dict] 嵌套树（区域 -> 服务区 -> 门店）
    """
    where_parts = ["A.SERVERPART_ID = B.SERVERPART_ID", "B.ISVALID = 1"]

    if serverpartshop_id and serverpartshop_id.strip():
        where_parts.append(f"B.SERVERPARTSHOP_ID IN ({serverpartshop_id})")
    if serverpart_id and serverpart_id.strip():
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_id})")
    elif serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"A.SERVERPART_CODE IN ('{codes}')")
    elif province_code is not None:
        province_id = _get_province_id_by_code(db, str(province_code))
        if province_id:
            where_parts.append(f"A.PROVINCE_CODE = {province_id}")
            where_parts.append("A.STATISTICS_TYPE = 1000")
    if business_state and business_state.strip():
        where_parts.append(f"B.BUSINESS_STATE IN ({business_state})")
    if business_type and business_type.strip():
        where_parts.append(f"B.BUSINESS_TYPE IN ({business_type})")
    if show_royalty:
        where_parts.append("B.ROYALTYRATE IS NOT NULL")
    if show_in_sale:
        where_parts.append("B.INSALES_TYPE = 1")

    where_sql = " AND ".join(where_parts)
    shop_name_field = "B.SHOPSHORTNAME" if show_short_name else "B.SHOPNAME"
    order_str = sort_str if sort_str else "A.SPREGIONTYPE_INDEX, A.SERVERPART_INDEX, B.SERVERPARTSHOP_INDEX"

    sql = f"""SELECT
            A.PROVINCE_CODE, A.SERVERPART_ID, A.SERVERPART_CODE, A.SERVERPART_NAME,
            A.SERVERPART_INDEX, A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
            B.SERVERPARTSHOP_ID, B.SHOPTRADE, {shop_name_field} AS SHOPNAME,
            B.BUSINESS_STATE, B.BUSINESS_TYPE, B.SERVERPARTSHOP_INDEX
        FROM T_SERVERPART A, T_SERVERPARTSHOP B
        WHERE {where_sql}
        ORDER BY {order_str}"""

    rows = db.execute_query(sql)

    # 构建区域 -> 服务区 -> 门店 三级树
    region_map = {}
    sp_map = {}

    for row in rows:
        region_id = row.get("SPREGIONTYPE_ID")
        region_name = row.get("SPREGIONTYPE_NAME", "")
        sp_id = row.get("SERVERPART_ID")
        sp_name = row.get("SERVERPART_NAME", "")

        # 门店节点
        shop_node = {
            "label": row.get("SHOPNAME", ""),
            "value": row.get("SERVERPARTSHOP_ID"),
            "type": 2,
            "key": f"2-{row.get('SERVERPARTSHOP_ID')}"
        }
        if show_state:
            shop_node["desc"] = str(row.get("BUSINESS_STATE", ""))

        # 服务区节点
        sp_key = f"{region_id}-{sp_id}"
        if sp_key not in sp_map:
            sp_map[sp_key] = {
                "node": {
                    "label": sp_name,
                    "value": sp_id,
                    "type": 1,
                    "key": f"1-{sp_id}"
                },
                "children": [],
                "region_id": region_id,
                "region_name": region_name
            }
        sp_map[sp_key]["children"].append({"node": shop_node, "children": []})

    # 按区域分组
    for sp_data in sp_map.values():
        region_id = sp_data.pop("region_id")
        region_name = sp_data.pop("region_name")
        if region_id not in region_map:
            region_map[region_id] = {
                "node": {
                    "label": region_name or "未分区",
                    "value": region_id,
                    "type": 0,
                    "key": f"0-{region_id}"
                },
                "children": []
            }
        region_map[region_id]["children"].append(sp_data)

    return list(region_map.values())


# =====================================
# 15. GetServerpartShopTree - 服务区门店树
#     对应原 ServerpartShopHelper.GetServerpartShopTree
# =====================================
def get_serverpart_shop_tree(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_id: Optional[str] = None,
    serverpart_codes: Optional[str] = None,
    serverpartshop_id: Optional[str] = None,
    business_state: Optional[str] = None,
    business_type: Optional[str] = None,
    show_state: bool = False
) -> list:
    """
    获取服务区门店树（二级结构，无区域层）
    返回: List[dict]
    """
    # 复用 GetSPRegionShopTree 的逻辑，但不按区域分组
    where_parts = ["A.SERVERPART_ID = B.SERVERPART_ID", "B.ISVALID = 1"]

    if serverpartshop_id and serverpartshop_id.strip():
        where_parts.append(f"B.SERVERPARTSHOP_ID IN ({serverpartshop_id})")
    if serverpart_id and serverpart_id.strip():
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_id})")
    elif serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"A.SERVERPART_CODE IN ('{codes}')")
    elif province_code is not None:
        province_id = _get_province_id_by_code(db, str(province_code))
        if province_id:
            where_parts.append(f"A.PROVINCE_CODE = {province_id}")
            where_parts.append("A.STATISTICS_TYPE = 1000")
    if business_state and business_state.strip():
        where_parts.append(f"B.BUSINESS_STATE IN ({business_state})")
    if business_type and business_type.strip():
        where_parts.append(f"B.BUSINESS_TYPE IN ({business_type})")

    where_sql = " AND ".join(where_parts)

    sql = f"""SELECT A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX,
            B.SERVERPARTSHOP_ID, B.SHOPNAME, B.BUSINESS_STATE, B.SERVERPARTSHOP_INDEX
        FROM T_SERVERPART A, T_SERVERPARTSHOP B
        WHERE {where_sql}
        ORDER BY A.SERVERPART_INDEX, B.SERVERPARTSHOP_INDEX"""

    rows = db.execute_query(sql)

    sp_map = {}
    for row in rows:
        sp_id = row.get("SERVERPART_ID")
        if sp_id not in sp_map:
            sp_map[sp_id] = {
                "node": {
                    "label": row.get("SERVERPART_NAME", ""),
                    "value": sp_id,
                    "type": 1,
                    "key": f"1-{sp_id}"
                },
                "children": []
            }
        shop_node = {
            "label": row.get("SHOPNAME", ""),
            "value": row.get("SERVERPARTSHOP_ID"),
            "type": 2,
            "key": f"2-{row.get('SERVERPARTSHOP_ID')}"
        }
        if show_state:
            shop_node["desc"] = str(row.get("BUSINESS_STATE", ""))
        sp_map[sp_id]["children"].append({"node": shop_node, "children": []})

    return list(sp_map.values())


# =====================================
# 辅助方法: 根据省份编码获取省份内码
# =====================================
def _get_province_id_by_code(db: DatabaseHelper, province_code: str) -> Optional[int]:
    """
    根据省份编码获取省份内码
    对应原 ServerpartHelper.GetProvinceIdByCode
    """
    if not province_code or province_code.strip() == "0":
        return None
    try:
        sql = f"""SELECT FIELDENUM_ID FROM T_FIELDENUM
            WHERE FIELDEXPLAIN_ID = (SELECT FIELDEXPLAIN_ID FROM T_FIELDEXPLAIN WHERE FIELDEXPLAIN_NAME = 'DIVISION_CODE')
              AND FIELDENUM_VALUE = '{province_code}'"""
        rows = db.execute_query(sql)
        if rows:
            return rows[0].get("FIELDENUM_ID")
    except Exception as e:
        logger.warning(f"获取省份内码失败: {e}")
    return None


# =====================================
# 辅助方法: 根据服务区编码获取服务区内码集合
# =====================================
def _get_serverpart_ids_by_codes(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_codes: Optional[str] = None
) -> str:
    """
    根据服务区编码获取服务区内码集合
    对应原 ServerpartHelper.GetServerpartIdsByCodes
    """
    where_parts = []
    if serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"SERVERPART_CODE IN ('{codes}')")
    elif province_code is not None:
        province_id = _get_province_id_by_code(db, str(province_code))
        if province_id:
            where_parts.append(f"PROVINCE_CODE = {province_id}")
        else:
            return ""
    else:
        return ""

    where_sql = " WHERE " + " AND ".join(where_parts)
    sql = f"SELECT SERVERPART_ID FROM T_SERVERPART{where_sql}"
    rows = db.execute_query(sql)
    return ",".join(str(r.get("SERVERPART_ID")) for r in rows if r.get("SERVERPART_ID"))


# =====================================
# 4.5 GetServerpartShopDDL - 门店下拉框
#     对应原 ServerpartShopHelper.GetServerpartShopDDL (L1031-1065)
# =====================================
def get_serverpart_shop_ddl(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_id: Optional[str] = None,
    serverpart_codes: Optional[str] = None,
) -> list:
    """
    获取门店下拉框列表
    SQL: SELECT * FROM T_SERVERPARTSHOP WHERE ISVALID = 1 + 条件
    排序: SERVERPART_NAME, SHOPTRADE, SHOPSHORTNAME, SHOPREGION, SHOPCODE
    返回: List[{label: SHOPNAME, value: SERVERPARTSHOP_ID(str)}]
    """
    # ---- 构建 WHERE 条件（参考原 Helper L1036-1053）----
    where_parts = ["ISVALID = 1"]

    if serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"SERVERPART_CODE IN ('{codes}')")
    elif serverpart_id and serverpart_id.strip():
        where_parts.append(f"SERVERPART_ID IN ({serverpart_id})")
    elif province_code is not None:
        # 省份过滤: EXISTS子查询
        where_parts.append(
            f"EXISTS (SELECT 1 FROM T_SERVERPART "
            f"WHERE T_SERVERPART.SERVERPART_ID = T_SERVERPARTSHOP.SERVERPART_ID "
            f"AND PROVINCE_CODE = (SELECT FIELDENUM_ID FROM T_FIELDENUM "
            f"WHERE FIELDEXPLAIN_ID = 154 AND FIELDENUM_VALUE = '{province_code}'))"
        )

    where_sql = " WHERE " + " AND ".join(where_parts)

    # 原 Helper: FillDataTable(WhereSQL) — 单表查 T_SERVERPARTSHOP
    # 排序: .Select("", "SERVERPART_NAME,SHOPTRADE,SHOPSHORTNAME,SHOPREGION,SHOPCODE")
    sql = f"""SELECT SERVERPARTSHOP_ID, SHOPNAME, SHOPTRADE, SHOPSHORTNAME,
            SHOPREGION, SHOPCODE, SERVERPART_NAME
        FROM T_SERVERPARTSHOP
        {where_sql}
        ORDER BY SERVERPART_NAME, SHOPTRADE, SHOPSHORTNAME, SHOPREGION, SHOPCODE"""

    rows = db.execute_query(sql)

    # 构建 CommonModel 列表: {label, value}
    result = []
    for r in rows:
        result.append({
            "label": str(r.get("SHOPNAME") or ""),
            "value": str(r.get("SERVERPARTSHOP_ID") or ""),
        })

    return result


# =====================================
# 4.6 GetServerpartShopTree - 服务区门店二级树（无区域层）
#     对应原 ServerpartShopHelper.GetServerpartShopTree (L1504-1569)
# =====================================
def get_serverpart_shop_tree(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_id: Optional[str] = None,
    serverpart_codes: Optional[str] = None,
    serverpart_shop_id: Optional[str] = None,
    business_state: Optional[str] = None,
    business_type: Optional[str] = None,
    show_state: bool = False,
) -> list:
    """
    获取服务区→门店二级嵌套树（无区域层）
    返回: List[NestingModel<CommonTypeTreeModel>]
      - node = 服务区(type=1), node.children = 门店列表(type=2)
    对应原 GetSPRegionShopTree 减去区域分组
    """
    # ---- 构建 WHERE 条件（参考原 Helper L1512-1543）----
    where_parts = []

    if serverpart_shop_id and serverpart_shop_id.strip():
        where_parts.append(f"B.SERVERPARTSHOP_ID IN ({serverpart_shop_id})")

    if serverpart_id and serverpart_id.strip():
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_id})")
    elif serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"A.SERVERPART_CODE IN ('{codes}')")
    elif province_code is not None:
        where_parts.append(
            f"A.PROVINCE_CODE = (SELECT FIELDENUM_ID FROM T_FIELDENUM "
            f"WHERE FIELDEXPLAIN_ID = 154 AND FIELDENUM_VALUE = '{province_code}')"
        )

    if business_state and business_state.strip():
        where_parts.append(f"B.BUSINESS_STATE IN ({business_state})")

    if business_type and business_type.strip():
        where_parts.append(f"B.BUSINESS_TYPE IN ({business_type})")

    where_extra = (" AND " + " AND ".join(where_parts)) if where_parts else ""

    # ---- 查询服务区门店数据（参考原 Helper L1545-1551）----
    sp_sql = f"""SELECT A.PROVINCE_CODE, A.SERVERPART_ID,
            A.SERVERPART_CODE, A.SERVERPART_NAME, A.SERVERPART_INDEX,
            B.SERVERPARTSHOP_ID, B.SHOPTRADE, B.SHOPNAME, B.SHOPSHORTNAME,
            B.SHOPREGION, B.SHOPCODE, B.BUSINESS_STATE, B.BUSINESS_TYPE
        FROM T_SERVERPART A, T_SERVERPARTSHOP B
        WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.ISVALID = 1{where_extra}"""

    dt_shop = db.execute_query(sp_sql)

    if not dt_shop:
        return []

    # 提取去重服务区列表（参考原 Helper L1555-1557）
    sp_map = {}
    for r in dt_shop:
        sp_id = r.get("SERVERPART_ID")
        if sp_id not in sp_map:
            sp_map[sp_id] = {
                "PROVINCE_CODE": r.get("PROVINCE_CODE"),
                "SERVERPART_ID": sp_id,
                "SERVERPART_CODE": r.get("SERVERPART_CODE"),
                "SERVERPART_NAME": r.get("SERVERPART_NAME"),
                "SERVERPART_INDEX": r.get("SERVERPART_INDEX"),
            }

    province_id = str(list(sp_map.values())[0].get("PROVINCE_CODE", ""))

    # 复用 BingServerpartShopTree 构建服务区→门店节点
    return _bing_serverpart_shop_tree(
        province_id, sp_map, dt_shop, show_state, "SHOPREGION,SHOPTRADE,SHOPNAME"
    )


# =====================================
# 4.7 GetNestingOwnerUnitList - 业主单位嵌套列表
#     对应原 OwnerUnitHelper.GetNestingOwnerUnitList (L528-585)
#     + BinData (L594-624) 递归
# =====================================
def get_nesting_ownerunit_list(
    db: DatabaseHelper,
    ownerunit_pid: Optional[int] = -1,
    show_status: bool = False,
    province_code: Optional[int] = None,
    ownerunit_nature: Optional[str] = None,
    ownerunit_name: Optional[str] = None,
) -> list:
    """
    获取业主单位嵌套列表
    返回: List[NestingModel<OWNERUNITModel>]
      - node = OWNERUNITModel(18字段)
      - children = List[NestingModel<OWNERUNITModel>] (递归)
    """
    # ---- 构建 WHERE 条件（参考原 Helper L534-548）----
    where_parts = []

    if show_status:
        where_parts.append("OWNERUNIT_STATE = 1")

    if province_code is not None:
        where_parts.append(f"PROVINCE_BUSINESSCODE = {province_code}")

    if ownerunit_nature and ownerunit_nature.strip():
        where_parts.append(f"OWNERUNIT_NATURE IN ({ownerunit_nature})")

    where_sql = (" WHERE " + " AND ".join(where_parts)) if where_parts else ""

    # 查询全表
    sql = f"SELECT * FROM T_OWNERUNIT{where_sql}"
    rows = db.execute_query(sql)

    if not rows:
        return []

    # 构建嵌套树
    if ownerunit_pid == -1 or ownerunit_pid is None:
        # 从根节点(-1)开始递归
        return _bind_ownerunit_data(-1, rows, ownerunit_name)
    else:
        # 先查指定 PID 节点，再递归子树
        root_rows = [r for r in rows if r.get("OWNERUNIT_ID") == ownerunit_pid]
        if not root_rows:
            return []

        root = root_rows[0]
        node = _ownerunit_row_to_model(root)
        children = _bind_ownerunit_data(ownerunit_pid, rows, ownerunit_name)

        # 模糊查询过滤
        if ownerunit_name and ownerunit_name.strip():
            if not children and node.get("OWNERUNIT_NAME", "") and ownerunit_name not in str(node.get("OWNERUNIT_NAME", "")):
                return []

        return [{
            "node": node,
            "children": children if children else None,
        }]


def _bind_ownerunit_data(
    parent_id: int,
    rows: list,
    ownerunit_name: Optional[str] = None,
) -> list:
    """
    递归构建业主单位嵌套树
    对应原 BinData (L594-624)
    按 OWNERUNIT_PID 过滤，排序 OWNERUNIT_INDEX, OWNERUNIT_ID
    """
    # 筛选 OWNERUNIT_PID = parent_id 的行
    children_rows = [r for r in rows if r.get("OWNERUNIT_PID") == parent_id]

    # 排序
    children_rows.sort(key=lambda x: (x.get("OWNERUNIT_INDEX") or 0, x.get("OWNERUNIT_ID") or 0))

    result = []
    for row in children_rows:
        node = _ownerunit_row_to_model(row)
        uid = row.get("OWNERUNIT_ID")

        # 检查是否有子节点
        has_children = any(r.get("OWNERUNIT_PID") == uid for r in rows)
        children = None
        if has_children:
            children = _bind_ownerunit_data(uid, rows, ownerunit_name)

        # 模糊查询过滤
        if ownerunit_name and ownerunit_name.strip():
            name = str(node.get("OWNERUNIT_NAME", ""))
            if not (children and len(children) > 0) and ownerunit_name not in name:
                continue

        result.append({
            "node": node,
            "children": children,
        })

    return result


def _ownerunit_row_to_model(row: dict) -> dict:
    """
    将数据库行转换为 OWNERUNITModel
    对应原 BindDataRowToModel (L77-133)
    """
    return {
        "OWNERUNIT_ID": row.get("OWNERUNIT_ID"),
        "OWNERUNIT_PID": row.get("OWNERUNIT_PID"),
        "PROVINCE_CODE": row.get("PROVINCE_CODE"),
        "PROVINCE_BUSINESSCODE": row.get("PROVINCE_BUSINESSCODE"),
        "OWNERUNIT_NAME": row.get("OWNERUNIT_NAME") or "",
        "OWNERUNIT_EN": row.get("OWNERUNIT_EN") or "",
        "OWNERUNIT_NATURE": row.get("OWNERUNIT_NATURE"),
        "OWNERUNIT_GUID": row.get("OWNERUNIT_GUID") or "",
        "OWNERUNIT_INDEX": row.get("OWNERUNIT_INDEX"),
        "OWNERUNIT_ICO": row.get("OWNERUNIT_ICO") or "",
        "OWNERUNIT_STATE": row.get("OWNERUNIT_STATE"),
        "STAFF_ID": row.get("STAFF_ID"),
        "STAFF_NAME": row.get("STAFF_NAME") or "",
        "OPERATE_DATE": str(row.get("OPERATE_DATE") or ""),
        "OWNERUNIT_DESC": row.get("OWNERUNIT_DESC") or "",
        "ISSUPPORTPOINT": row.get("ISSUPPORTPOINT"),
        "DOWNLOAD_DATE": str(row.get("DOWNLOAD_DATE") or ""),
        "WECHATPUBLICSIGN_ID": row.get("WECHATPUBLICSIGN_ID"),
    }


# =====================================
# 4.8 BindingOwnerUnitDDL - 业主单位下拉框
#     对应原 OwnerUnitHelper.BindingOwnerUnitDDL (L635-664)
# =====================================
COOP_MERCHANT_URL = "https://user.eshangtech.com"


def binding_ownerunit_ddl(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    data_type: int = 0,
) -> list:
    """
    绑定业主单位下拉框
    WHERE OWNERUNIT_PID = -1 AND OWNERUNIT_NATURE = 1000
    DataType=0: value=PROVINCE_BUSINESSCODE; DataType=1: value=OWNERUNIT_ID
    排序: PROVINCE_BUSINESSCODE
    返回: List[CommonTypeModel{label, value, key, type, desc, ico}]
    """
    province_filter = ""
    if province_code is not None:
        province_filter = f" AND PROVINCE_BUSINESSCODE = {province_code}"

    sql = f"""SELECT * FROM T_OWNERUNIT
        WHERE OWNERUNIT_PID = -1 AND OWNERUNIT_NATURE = 1000{province_filter}
        ORDER BY PROVINCE_BUSINESSCODE"""

    rows = db.execute_query(sql)

    result = []
    for r in rows:
        if data_type == 0:
            value = r.get("PROVINCE_BUSINESSCODE")
        else:
            value = r.get("OWNERUNIT_ID")

        ico = None
        ownerunit_ico = r.get("OWNERUNIT_ICO")
        if ownerunit_ico and str(ownerunit_ico).strip():
            ico = COOP_MERCHANT_URL + str(ownerunit_ico)

        result.append({
            "label": r.get("OWNERUNIT_NAME") or "",
            "value": value,
            "key": None,
            "type": None,
            "desc": None,
            "ico": ico,
        })

    return result


# =====================================
# 4.9 BindingOwnerUnitTree - 业主单位嵌套树
#     对应原 OwnerUnitHelper.BindingOwnerUnitTree (L677-740)
#     + BindChildOwnerUnit (L750-803)
# =====================================
def binding_ownerunit_tree(
    db: DatabaseHelper,
    ownerunit_nature: int = 1000,
    ownerunit_pid: int = -1,
    data_type: int = 0,
    province_code: Optional[int] = None,
) -> list:
    """
    绑定业主单位嵌套树
    WHERE OWNERUNIT_NATURE = {ownerunit_nature}
    递归构建 CommonTypeModel 嵌套树
    DataType=0: value=PROVINCE_BUSINESSCODE; DataType=1: value=OWNERUNIT_ID
    """
    where_sql = ""
    if ownerunit_nature is not None:
        where_sql = f"WHERE OWNERUNIT_NATURE = {ownerunit_nature}"

    sql = f"SELECT * FROM T_OWNERUNIT {where_sql}"
    rows = db.execute_query(sql)

    if not rows:
        return []

    # 按 OWNERUNIT_PID = ownerunit_pid 过滤顶层
    top_rows = [r for r in rows if r.get("OWNERUNIT_PID") == ownerunit_pid]
    top_rows.sort(key=lambda x: (x.get("OWNERUNIT_INDEX") or 0, x.get("OWNERUNIT_ID") or 0))

    result = []
    for r in top_rows:
        node = _build_ownerunit_common_type_node(r, data_type)
        nesting = {"node": node}

        # 检查子节点（原 Helper L714 用 OWNERUNIT_ID 检查）
        actual_id = r.get("OWNERUNIT_ID")
        has_children = any(cr.get("OWNERUNIT_PID") == actual_id for cr in rows)
        if has_children:
            # 原 Helper L718 用 value.TryParseToInt() 做递归 PID
            # DataType=0 时 value=PROVINCE_BUSINESSCODE, DataType=1 时 value=OWNERUNIT_ID
            recurse_pid = node.get("value")
            children = _bind_child_ownerunit(recurse_pid, rows, data_type, province_code)
            nesting["children"] = children if children else None
        else:
            nesting["children"] = None

        # 省份过滤（参考原 Helper L724-736）
        if province_code is not None:
            pb = r.get("PROVINCE_BUSINESSCODE")
            pc = r.get("PROVINCE_CODE")
            has_ch = nesting.get("children") and len(nesting.get("children", [])) > 0
            if pb == province_code or pc == province_code or has_ch:
                result.append(nesting)
        else:
            result.append(nesting)

    return result


def _bind_child_ownerunit(
    parent_id: int,
    rows: list,
    data_type: int = 0,
    province_code: Optional[int] = None,
) -> list:
    """
    递归绑定子级业主单位（CommonTypeModel）
    对应原 BindChildOwnerUnit (L750-803)
    """
    child_rows = [r for r in rows if r.get("OWNERUNIT_PID") == parent_id]
    child_rows.sort(key=lambda x: (x.get("OWNERUNIT_INDEX") or 0, x.get("OWNERUNIT_ID") or 0))

    result = []
    for r in child_rows:
        node = _build_ownerunit_common_type_node(r, data_type)
        nesting = {"node": node}

        actual_id = r.get("OWNERUNIT_ID")
        has_children = any(cr.get("OWNERUNIT_PID") == actual_id for cr in rows)
        if has_children:
            # 原 Helper L784 用 value.TryParseToInt() 做递归 PID
            recurse_pid = node.get("value")
            children = _bind_child_ownerunit(recurse_pid, rows, data_type, province_code)
            nesting["children"] = children if children else None
        else:
            nesting["children"] = None

        # 省份过滤
        if province_code is not None:
            pb = r.get("PROVINCE_BUSINESSCODE")
            pc = r.get("PROVINCE_CODE")
            has_ch = nesting.get("children") and len(nesting.get("children", [])) > 0
            if pb == province_code or pc == province_code or has_ch:
                result.append(nesting)
        else:
            result.append(nesting)

    return result


def _build_ownerunit_common_type_node(row: dict, data_type: int = 0) -> dict:
    """
    构建 CommonTypeModel 节点
    DataType=0: value=PROVINCE_BUSINESSCODE; DataType=1: value=OWNERUNIT_ID
    """
    if data_type == 0:
        value = row.get("PROVINCE_BUSINESSCODE")
    else:
        value = row.get("OWNERUNIT_ID")

    ico = None
    ownerunit_ico = row.get("OWNERUNIT_ICO")
    if ownerunit_ico and str(ownerunit_ico).strip():
        ico = COOP_MERCHANT_URL + str(ownerunit_ico)

    return {
        "label": row.get("OWNERUNIT_NAME") or "",
        "value": value,
        "key": f"1-{value}",
        "type": 1,
        "desc": None,
        "ico": ico,
    }


# =====================================
# 5. GetSPRegionShopTree - 区域服务区门店三级树
#    对应原 ServerpartShopHelper.GetSPRegionShopTree (L1330-1488)
#    + BingServerpartShopTree (L1585-1666)
# =====================================
def get_sp_region_shop_tree(
    db: DatabaseHelper,
    province_code: Optional[int] = None,
    serverpart_id: Optional[str] = None,
    serverpart_codes: Optional[str] = None,
    serverpart_shop_id: Optional[str] = None,
    business_state: Optional[str] = None,
    business_type: Optional[str] = None,
    show_state: bool = False,
    show_short_name: bool = False,
    show_in_sale: bool = False,
    sort_str: Optional[str] = None,
    show_royalty: bool = False,
    show_unpaid_expense: bool = False,
) -> list:
    """
    获取区域→服务区→门店三级嵌套树
    返回: List[NestingModel<CommonTypeTreeModel>]
      - node = CommonTypeTreeModel { label, value, type, key, ico, desc, children }
      - children = List[NestingModel<CommonTypeTreeModel>]

    三级结构:
      区域(type=0, desc=门店数)
        └ 服务区(type=1, desc=门店数)
            └ 门店(type=2, 在 node.children 中)
    """
    # ---- 构建 WHERE 条件（参考原 Helper L1338-1379）----
    where_parts = []

    if serverpart_shop_id and serverpart_shop_id.strip():
        where_parts.append(f"B.SERVERPARTSHOP_ID IN ({serverpart_shop_id})")

    if serverpart_id and serverpart_id.strip():
        where_parts.append(f"A.SERVERPART_ID IN ({serverpart_id})")
    elif serverpart_codes and serverpart_codes.strip():
        codes = "','".join(serverpart_codes.split(","))
        where_parts.append(f"A.SERVERPART_CODE IN ('{codes}')")
    elif province_code is not None:
        # 省份编码字典映射（与 GetServerpartTree 一致）
        where_parts.append(
            f"A.PROVINCE_CODE = (SELECT FIELDENUM_ID FROM T_FIELDENUM "
            f"WHERE FIELDEXPLAIN_ID = 154 AND FIELDENUM_VALUE = '{province_code}') "
            f"AND A.STATISTICS_TYPE = 1000"
        )

    if business_state and business_state.strip():
        where_parts.append(f"B.BUSINESS_STATE IN ({business_state})")

    if business_type and business_type.strip():
        where_parts.append(f"B.BUSINESS_TYPE IN ({business_type})")

    if show_royalty:
        where_parts.append("B.ROYALTYRATE IS NOT NULL")

    if show_in_sale:
        where_parts.append("B.INSALES_TYPE = 1")

    where_extra = (" AND " + " AND ".join(where_parts)) if where_parts else ""

    # ---- 查询服务区门店数据（参考原 Helper L1382-1414）----
    if show_short_name:
        # ShowShortName 模式：按简称分组
        sp_sql = f"""SELECT
                A.PROVINCE_CODE, A.SERVERPART_ID,
                A.SERVERPART_CODE, A.SERVERPART_NAME, A.SERVERPART_INDEX,
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                MIN(B.SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID, B.SHOPTRADE,
                B.SHOPSHORTNAME, B.SHOPSHORTNAME AS SHOPNAME, B.BUSINESS_TYPE,
                MIN(B.BUSINESS_STATE) AS BUSINESS_STATE,
                MIN(B.SERVERPARTSHOP_INDEX) AS SERVERPARTSHOP_INDEX
            FROM T_SERVERPART A, T_SERVERPARTSHOP B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.ISVALID = 1{where_extra}
            GROUP BY
                A.PROVINCE_CODE, A.SERVERPART_ID,
                A.SERVERPART_CODE, A.SERVERPART_NAME, A.SERVERPART_INDEX,
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                B.SHOPTRADE, B.SHOPSHORTNAME, B.BUSINESS_TYPE"""
    else:
        # 正常模式
        sp_sql = f"""SELECT A.PROVINCE_CODE, A.SERVERPART_ID,
                A.SERVERPART_CODE, A.SERVERPART_NAME, A.SERVERPART_INDEX,
                A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
                B.SERVERPARTSHOP_ID, B.SHOPTRADE, B.SHOPNAME, B.SHOPSHORTNAME,
                B.SHOPREGION, B.SHOPCODE, B.BUSINESS_STATE, B.BUSINESS_TYPE
            FROM T_SERVERPART A, T_SERVERPARTSHOP B
            WHERE A.SERVERPART_ID = B.SERVERPART_ID AND B.ISVALID = 1{where_extra}"""

    dt_shop = db.execute_query(sp_sql)

    if not dt_shop:
        return []

    # ---- 构建三级树（参考原 Helper L1429-1482）----
    # 1. 提取去重区域列表（SPREGIONTYPE_ID is not null）
    region_map = {}
    for row in dt_shop:
        rt_id = row.get("SPREGIONTYPE_ID")
        if rt_id is not None:
            if rt_id not in region_map:
                region_map[rt_id] = {
                    "id": rt_id,
                    "name": row.get("SPREGIONTYPE_NAME", ""),
                    "index": row.get("SPREGIONTYPE_INDEX", 0),
                }

    # 按 index, id 排序
    sorted_regions = sorted(region_map.values(), key=lambda x: (x.get("index") or 0, x.get("id") or 0))

    # 默认排序字段
    if not sort_str or not sort_str.strip():
        sort_str = "SHOPREGION,SHOPTRADE,SHOPNAME"

    nesting_model_list = []

    for region in sorted_regions:
        rt_id = region["id"]

        # 筛选该区域的行
        region_rows = [r for r in dt_shop if r.get("SPREGIONTYPE_ID") == rt_id]

        # 提取去重服务区列表
        sp_map = {}
        for r in region_rows:
            sp_id = r.get("SERVERPART_ID")
            if sp_id not in sp_map:
                sp_map[sp_id] = {
                    "PROVINCE_CODE": r.get("PROVINCE_CODE"),
                    "SERVERPART_ID": sp_id,
                    "SERVERPART_CODE": r.get("SERVERPART_CODE"),
                    "SERVERPART_NAME": r.get("SERVERPART_NAME"),
                    "SERVERPART_INDEX": r.get("SERVERPART_INDEX"),
                }

        province_id = str(list(sp_map.values())[0].get("PROVINCE_CODE", "")) if sp_map else ""

        # 构建服务区→门店子节点（BingServerpartShopTree 逻辑）
        children_list = _bing_serverpart_shop_tree(
            province_id, sp_map, dt_shop, show_state, sort_str
        )

        # 区域 node
        region_node = {
            "label": region["name"],
            "value": int(rt_id),
            "type": 0,
            "key": f"0-{rt_id}",
            "ico": None,
            "desc": None,
            "children": None,
        }

        # 累计门店数量（desc = 所有服务区的门店数之和）
        total_shop_count = 0
        for child in children_list:
            child_node = child.get("node", {})
            total_shop_count += len(child_node.get("children") or [])
        region_node["desc"] = str(total_shop_count)

        nesting_model_list.append({
            "node": region_node,
            "children": children_list,
        })

    # 2. 处理无区域归属的服务区（SPREGIONTYPE_ID is null）
    no_region_rows = [r for r in dt_shop if r.get("SPREGIONTYPE_ID") is None]
    if no_region_rows:
        sp_map = {}
        for r in no_region_rows:
            sp_id = r.get("SERVERPART_ID")
            if sp_id not in sp_map:
                sp_map[sp_id] = {
                    "PROVINCE_CODE": r.get("PROVINCE_CODE"),
                    "SERVERPART_ID": sp_id,
                    "SERVERPART_CODE": r.get("SERVERPART_CODE"),
                    "SERVERPART_NAME": r.get("SERVERPART_NAME"),
                    "SERVERPART_INDEX": r.get("SERVERPART_INDEX"),
                }
        province_id = str(list(sp_map.values())[0].get("PROVINCE_CODE", ""))
        nesting_model_list.extend(
            _bing_serverpart_shop_tree(province_id, sp_map, dt_shop, show_state, sort_str)
        )

    return nesting_model_list


def _bing_serverpart_shop_tree(
    province_id: str,
    sp_map: dict,
    dt_shop: list,
    show_state: bool,
    sort_str: str,
) -> list:
    """
    构建服务区→门店节点列表
    对应原 BingServerpartShopTree (L1585-1666)
    返回: List[NestingModel<CommonTypeTreeModel>]
      - 每个元素: { node: CommonTypeTreeModel, children: None }
      - node.children 为门店列表(CommonTypeModel)
    """
    result = []

    # 按 SERVERPART_INDEX, SERVERPART_CODE 排序
    sorted_sps = sorted(
        sp_map.values(),
        key=lambda x: (x.get("SERVERPART_INDEX") or 0, x.get("SERVERPART_CODE") or "")
    )

    # 解析排序字段
    sort_keys = [s.strip() for s in sort_str.split(",") if s.strip()]

    for sp in sorted_sps:
        sp_id = sp["SERVERPART_ID"]

        # 服务区 node
        sp_node = {
            "label": sp.get("SERVERPART_NAME", ""),
            "value": int(sp_id) if sp_id else 0,
            "type": 1,
            "key": f"1-{sp_id}",
            "ico": None,
            "desc": None,
            "children": [],
        }

        # 筛选该服务区的门店行
        shop_rows = [r for r in dt_shop if r.get("SERVERPART_ID") == sp_id]

        # 排序门店
        def shop_sort_key(r):
            return tuple(r.get(k, "") or "" for k in sort_keys)
        shop_rows.sort(key=shop_sort_key)

        for shop in shop_rows:
            shop_label = str(shop.get("SHOPNAME") or "")

            # ShowState: 非运营中状态追加标签
            if show_state and str(shop.get("BUSINESS_STATE", "")) != "1000":
                bs = str(shop.get("BUSINESS_STATE", ""))
                if bs == "1010":
                    shop_label += "【待运营】"
                elif bs == "2000":
                    shop_label += "【暂停中】"
                elif bs == "3000":
                    shop_label += "【已停业】"

            shop_model = {
                "label": shop_label,
                "value": int(shop.get("SERVERPARTSHOP_ID") or 0),
                "type": 2,
                "key": f"2-{shop.get('SERVERPARTSHOP_ID')}",
            }
            sp_node["children"].append(shop_model)

        sp_node["desc"] = str(len(sp_node["children"]))

        # 只有有门店的服务区才加入结果
        if sp_node["children"]:
            result.append({
                "node": sp_node,
                "children": None,
            })

    return result


# =====================================
# 辅助方法: 日期格式化 (ISO datetime)
# =====================================
def _format_datetime(val) -> str:
    """
    将数据库日期值格式化为原 C# API 的 yyyy-MM-ddTHH:mm:ss 格式
    达梦返回可能是 datetime 对象或字符串
    """
    if val is None:
        return None
    from datetime import datetime as dt
    if isinstance(val, dt):
        return val.strftime("%Y-%m-%dT%H:%M:%S")
    s = str(val).strip()
    if not s:
        return None
    # 如果是 "2021-07-14" 格式（无时间部分），不追加 T00:00:00
    # 原 C# 返回 datetime 的完整 ISO 格式
    return s.replace(" ", "T") if " " in s else s


# =====================================
# 12. GetBusinessBrandList - 查询门店经营品牌列表
#     对应原 BRANDHelper.GetBusinessBrandList (L1283-1320)
# =====================================
def get_business_brand_list(
    db: DatabaseHelper,
    serverpart_shop_ids: str,
) -> list:
    """
    查询门店经营品牌列表
    逻辑:
      1. 查 T_SERVERPARTSHOP: 按门店 ID 筛选, BUSINESS_BRAND IS NOT NULL
      2. 去重 BUSINESS_BRAND + BRAND_NAME
      3. 逐个品牌查 T_BRAND 获取全量字段 (BindObjectToModel)
      4. 为每个品牌构建 ServerpartList (服务区名称去掉"服务区"后缀)
      5. 按 BRAND_NAME 排序
    """
    if not serverpart_shop_ids or not serverpart_shop_ids.strip():
        return []

    # 步骤1: 查门店数据 — 原 Helper L1287-1288
    # FillDataTable("WHERE BUSINESS_BRAND IS NOT NULL AND SERVERPARTSHOP_ID IN (...)")
    shop_sql = f"""SELECT SERVERPARTSHOP_ID, BUSINESS_BRAND, BRAND_NAME,
            SERVERPART_ID, SERVERPART_NAME
        FROM T_SERVERPARTSHOP
        WHERE BUSINESS_BRAND IS NOT NULL
          AND SERVERPARTSHOP_ID IN ({serverpart_shop_ids})"""
    shop_rows = db.execute_query(shop_sql)

    if not shop_rows:
        return []

    # 步骤2: 去重 BUSINESS_BRAND (原 Helper L1291-1292)
    # dtShopList.DefaultView.ToTable(true, "BUSINESS_BRAND", "BRAND_NAME").Select("", "BRAND_NAME")
    seen_brands = {}
    for r in shop_rows:
        brand_id = r.get("BUSINESS_BRAND")
        if brand_id is not None and brand_id not in seen_brands:
            seen_brands[brand_id] = r.get("BRAND_NAME", "")

    # 按 BRAND_NAME 排序
    sorted_brand_ids = sorted(seen_brands.keys(), key=lambda bid: seen_brands[bid] or "")

    result = []
    for brand_id in sorted_brand_ids:
        # 步骤3: 查 T_BRAND 获取品牌全量字段 (原 Helper L1294-1300)
        brand_sql = f"SELECT * FROM T_BRAND WHERE BRAND_ID = {brand_id}"
        brand_rows = db.execute_query(brand_sql)
        if not brand_rows:
            continue

        brand = brand_rows[0]

        # BindObjectToModel 映射 (参考原 Helper L904-933)
        brand_intro = brand.get("BRAND_INTRO")
        if brand_intro and str(brand_intro).startswith("/"):
            brand_intro = COOP_MERCHANT_URL + str(brand_intro)

        brand_model = {
            "BRAND_ID": brand.get("BRAND_ID"),
            "BRAND_PID": brand.get("BRAND_PID"),
            "BRAND_INDEX": brand.get("BRAND_INDEX"),
            "BRAND_NAME": brand.get("BRAND_NAME") or "",
            "BRAND_CATEGORY": brand.get("BRAND_CATEGORY"),
            "BRAND_INDUSTRY": int(brand["BRAND_INDUSTRY"]) if brand.get("BRAND_INDUSTRY") not in (None, "") else None,
            "BUSINESSTRADE_NAME": None,
            "BRAND_TYPE": brand.get("BRAND_TYPE"),
            "BRAND_INTRO": brand_intro,
            "BRAND_STATE": brand.get("BRAND_STATE"),
            "WECHATAPPSIGN_ID": brand.get("WECHATAPPSIGN_ID"),
            "WECHATAPPSIGN_NAME": brand.get("WECHATAPPSIGN_NAME"),
            "WECHATAPP_APPID": brand.get("WECHATAPP_APPID"),
            "OWNERUNIT_ID": brand.get("OWNERUNIT_ID"),
            "OWNERUNIT_NAME": brand.get("OWNERUNIT_NAME") or "",
            "PROVINCE_CODE": brand.get("PROVINCE_CODE"),
            "STAFF_ID": brand.get("STAFF_ID"),
            "STAFF_NAME": brand.get("STAFF_NAME") or "",
            "OPERATE_DATE": _format_datetime(brand.get("OPERATE_DATE")),
            "BRAND_DESC": brand.get("BRAND_DESC"),
            "MANAGE_TYPE": brand.get("MANAGE_TYPE"),
            "COMMISSION_RATIO": brand.get("COMMISSION_RATIO"),
            "SPREGIONTYPE_IDS": None,
            "SERVERPART_IDS": None,
            "MerchantID": None,
            "MerchantID_Encrypt": None,
            "MerchantName": None,
            "ServerpartList": [],
        }

        # 步骤4: 构建 ServerpartList (原 Helper L1303-1313)
        # 筛选当前品牌的门店, 去重服务区, 按 SERVERPART_NAME 排序
        seen_sp = set()
        sp_rows = [r for r in shop_rows if r.get("BUSINESS_BRAND") == brand_id]
        sp_rows.sort(key=lambda x: str(x.get("SERVERPART_NAME") or ""))
        for r in sp_rows:
            sp_id = r.get("SERVERPART_ID")
            if sp_id is not None and sp_id not in seen_sp:
                seen_sp.add(sp_id)
                # 原 Helper L1309: drServerpart["SERVERPART_NAME"].ToString().Replace("服务区", "")
                sp_name = str(r.get("SERVERPART_NAME") or "").replace("服务区", "")
                brand_model["ServerpartList"].append({
                    "label": sp_name,
                    "value": str(sp_id),
                })

        result.append(brand_model)

    return result


# =====================================
# 13. ModifyShopState - 变更门店经营状态
#     对应原 ServerpartShopHelper.ModifyShopState (L1738-1795)
#     + SetShopBusinessState (L1798-1815)
# =====================================
def modify_shop_state(
    db: DatabaseHelper,
    shop_modify_list: list,
) -> bool:
    """
    批量变更门店经营状态
    逻辑 (原 Helper L1738-1795):
      1. 遍历 ShopModifyList
      2. 按 SERVERPARTSHOP_ID 查 T_SERVERPARTSHOP
      3. 查 T_RTSERVERPARTSHOP (运营记录) 并根据状态 Insert/Update
      4. 更新 T_SERVERPARTSHOP.BUSINESS_STATE (SetShopBusinessState L1798-1815)
    返回: True=全部成功, False=有失败
    """
    if not shop_modify_list:
        return False

    modify_flag = False

    for item in shop_modify_list:
        shop_id = item.get("SERVERPARTSHOP_ID")
        if shop_id is None:
            continue

        # 步骤2: 查 T_SERVERPARTSHOP (原 Helper L1745-1747)
        shop_sql = f"""SELECT SERVERPARTSHOP_ID, SHOPNAME, BUSINESS_TYPE,
                BUSINESS_REGION, BUSINESS_NATURE, BUSINESS_STATE,
                BUSINESS_ENDDATE, ISVALID, STAFF_ID, STAFF_NAME,
                SERVERPART_ID
            FROM T_SERVERPARTSHOP WHERE SERVERPARTSHOP_ID = {shop_id}"""
        shop_rows = db.execute_query(shop_sql)
        if not shop_rows:
            continue

        shop = shop_rows[0]

        # 步骤3: 查 T_RTSERVERPARTSHOP (原 Helper L1750-1752)
        rt_sql = f"""SELECT * FROM T_RTSERVERPARTSHOP
            WHERE SERVERPARTSHOP_ID = {shop_id}
            ORDER BY RTSERVERPARTSHOP_ID DESC"""
        rt_rows = db.execute_query(rt_sql)

        business_state = item.get("BUSINESS_STATE")
        business_date = item.get("BUSINESS_DATE")
        business_enddate = item.get("BUSINESS_ENDDATE")
        staff_id = item.get("STAFF_ID")
        staff_name = item.get("STAFF_NAME", "")
        operate_date = item.get("OPERATE_DATE")

        # 根据状态决定 Insert 还是 Update (原 Helper L1754-1773)
        if business_state in (1000, 1010):
            # 运营中/待运营: 更新现有记录的 BUSINESS_DATE
            if rt_rows and rt_rows[0].get("BUSINESS_ENDDATE") is None:
                # 更新现有记录
                rt_id = rt_rows[0].get("RTSERVERPARTSHOP_ID")
                update_rt_sql = f"""UPDATE T_RTSERVERPARTSHOP SET
                    BUSINESS_DATE = '{business_date}',
                    SERVERPARTSHOP_ID = {shop_id},
                    SHOPNAME = '{shop.get("SHOPNAME", "")}',
                    BUSINESS_TYPE = {shop.get("BUSINESS_TYPE") or "NULL"},
                    BUSINESS_REGION = '{shop.get("BUSINESS_REGION", "") or ""}',
                    BUSINESS_NATURE = '{shop.get("BUSINESS_NATURE", "") or ""}',
                    STAFF_ID = {staff_id or "NULL"},
                    STAFF_NAME = '{staff_name}',
                    OPERATE_DATE = '{operate_date}'
                    WHERE RTSERVERPARTSHOP_ID = {rt_id}"""
                db.execute_non_query(update_rt_sql)
            else:
                # 插入新记录
                insert_rt_sql = f"""INSERT INTO T_RTSERVERPARTSHOP
                    (RTSERVERPARTSHOP_ID, SERVERPARTSHOP_ID, SHOPNAME,
                     BUSINESS_TYPE, BUSINESS_REGION, BUSINESS_NATURE,
                     BUSINESS_DATE, STAFF_ID, STAFF_NAME, OPERATE_DATE)
                    VALUES ((SELECT COALESCE(MAX(RTSERVERPARTSHOP_ID),0)+1 FROM T_RTSERVERPARTSHOP), {shop_id},
                     '{shop.get("SHOPNAME", "")}',
                     {shop.get("BUSINESS_TYPE") or "NULL"},
                     '{shop.get("BUSINESS_REGION", "") or ""}',
                     '{shop.get("BUSINESS_NATURE", "") or ""}',
                     '{business_date}',
                     {staff_id or "NULL"},
                     '{staff_name}', '{operate_date}')"""
                db.execute_non_query(insert_rt_sql)
        else:
            # 暂停/关闭: 更新 BUSINESS_ENDDATE
            if rt_rows:
                rt_id = rt_rows[0].get("RTSERVERPARTSHOP_ID")
                update_rt_sql = f"""UPDATE T_RTSERVERPARTSHOP SET
                    BUSINESS_ENDDATE = '{business_enddate}',
                    SERVERPARTSHOP_ID = {shop_id},
                    SHOPNAME = '{shop.get("SHOPNAME", "")}',
                    BUSINESS_TYPE = {shop.get("BUSINESS_TYPE") or "NULL"},
                    BUSINESS_REGION = '{shop.get("BUSINESS_REGION", "") or ""}',
                    BUSINESS_NATURE = '{shop.get("BUSINESS_NATURE", "") or ""}',
                    STAFF_ID = {staff_id or "NULL"},
                    STAFF_NAME = '{staff_name}',
                    OPERATE_DATE = '{operate_date}'
                    WHERE RTSERVERPARTSHOP_ID = {rt_id}"""
                db.execute_non_query(update_rt_sql)
            else:
                insert_rt_sql = f"""INSERT INTO T_RTSERVERPARTSHOP
                    (RTSERVERPARTSHOP_ID, SERVERPARTSHOP_ID, SHOPNAME,
                     BUSINESS_TYPE, BUSINESS_REGION, BUSINESS_NATURE,
                     BUSINESS_ENDDATE, STAFF_ID, STAFF_NAME, OPERATE_DATE)
                    VALUES ((SELECT COALESCE(MAX(RTSERVERPARTSHOP_ID),0)+1 FROM T_RTSERVERPARTSHOP), {shop_id},
                     '{shop.get("SHOPNAME", "")}',
                     {shop.get("BUSINESS_TYPE") or "NULL"},
                     '{shop.get("BUSINESS_REGION", "") or ""}',
                     '{shop.get("BUSINESS_NATURE", "") or ""}',
                     '{business_enddate}',
                     {staff_id or "NULL"},
                     '{staff_name}', '{operate_date}')"""
                db.execute_non_query(insert_rt_sql)

        # 步骤4: SetShopBusinessState (原 Helper L1798-1815)
        # 更新 T_SERVERPARTSHOP.BUSINESS_STATE
        enddate_update = ""
        if business_state is not None and int(business_state) < 2000:
            # 运营中/待运营: 如果新停业日期 > 原停业日期, 清空停业日期
            enddate_update = ", BUSINESS_ENDDATE = NULL"

        update_shop_sql = f"""UPDATE T_SERVERPARTSHOP
            SET BUSINESS_STATE = {business_state}{enddate_update}
            WHERE SERVERPARTSHOP_ID = {shop_id}"""
        db.execute_non_query(update_shop_sql)

        modify_flag = True

    return modify_flag


# =====================================
# 14. GetShopReceivables - 获取经营门店关联合同项目信息
#     对应原 ServerpartShopHelper.GetShopReceivables (L1829-2152)
# =====================================
# 服务区类型枚举映射（原 C# DictionaryHelper.GetFieldEnumName）
_SERVERPART_TYPE_MAP = {
    "1000": "A类", "2000": "B类", "3000": "C类", "4000": "D类",
}

# 品牌图标 URL 前缀（原 C# Config.AppSettings.CoopMerchantUrls）
_COOP_MERCHANT_URLS = "https://api.eshangtech.com/EShangApiMain"


def get_shop_receivables(
    db: DatabaseHelper,
    server_part_id: str,
    business_state: str = "",
    business_type: str = "",
    abnormal_shop: bool = False,
) -> tuple:
    """
    获取经营门店关联合同项目信息
    返回: (AccountReceivablesList, HisProjectList)
    """
    account_list = []      # 主列表
    null_list = []         # 无门店关联的合同列表（OtherData）

    where_sql = ""
    # 服务区过滤（用于合同和经营项目查询）
    if server_part_id:
        where_sql += f" AND B.SERVERPART_ID IN ({server_part_id})"

    # ===== SQL1: 查询经营合同数据 (原 Helper L1846-1862) =====
    compact_sql = f"""SELECT
            A.REGISTERCOMPACT_ID, A.SECONDPART_NAME, A.SECONDPART_MOBILE,
            A.SECONDPART_LINKMAN, A.THREEPART_LINKMAN,
            A.SECONDPART_ID, A.ATTACHMENT_STATE, A.DURATION,
            B.SERVERPART_ID, C.COMPACT_CHILDTYPE, A.COMPACT_NAME,
            C.BUSINESS_TRADE, C.BUSINESS_TYPE, C.OPERATING_AREA,
            C.OPERATING_SCOPE, C.SETTLEMENT_MODES
        FROM
            T_REGISTERCOMPACT A,
            T_RTREGISTERCOMPACT B,
            T_REGISTERCOMPACTSUB C
        WHERE
            A.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND
            A.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID AND
            A.COMPACT_STATE = 1000 AND A.COMPACT_DETAILS = 1000{where_sql}
        GROUP BY
            A.REGISTERCOMPACT_ID, A.SECONDPART_NAME, A.SECONDPART_MOBILE,
            A.SECONDPART_LINKMAN, A.THREEPART_LINKMAN,
            A.SECONDPART_ID, A.ATTACHMENT_STATE, A.DURATION,
            B.SERVERPART_ID, C.COMPACT_CHILDTYPE, A.COMPACT_NAME,
            C.BUSINESS_TRADE, C.BUSINESS_TYPE, C.OPERATING_AREA,
            C.OPERATING_SCOPE, C.SETTLEMENT_MODES"""
    dt_compact = db.execute_query(compact_sql)
    # 复制一份合同数据，记录没有关联门店的合同（原 Helper L1864）
    dt_ex_compact_ids = {str(r.get("REGISTERCOMPACT_ID")) for r in dt_compact}

    # ===== SQL2: 查询经营项目数据 (原 Helper L1866-1909) =====
    project_sql = f"""SELECT
            A.BUSINESSPROJECT_ID, A.SERVERPARTSHOP_ID, A.GUARANTEE_PRICE,
            A.BUSINESS_TYPE, A.PROJECT_DAYS,
            A.BUSINESSPROJECT_NAME, B.SERVERPART_ID, D.REGISTERCOMPACT_ID,
            C.SHOPROYALTY_ID, C.NATUREDAY, C.GUARANTEERATIO,
            CASE A.BUSINESS_TYPE WHEN 2000 THEN C.RENTFEE ELSE C.MINTURNOVER END AS GUARANTEE_AMOUNT,
            C.SERVERPARTSHOP_ID AS ROYALTY_SHOP, A.PROJECT_STARTDATE, A.PROJECT_ENDDATE,
            ',' || A.SERVERPARTSHOP_ID || ',' AS RELATE_SHOP,
            COUNT(C.SHOPROYALTY_ID) AS SEPARATE_COUNT
        FROM
            T_REGISTERCOMPACT E,
            T_RTBUSINESSPROJECT D,
            T_RTREGISTERCOMPACT B,
            T_BUSINESSPROJECT A,
            T_SHOPROYALTY C
        WHERE
            A.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID AND
            D.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND
            A.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID AND
            D.REGISTERCOMPACT_ID = C.REGISTERCOMPACT_ID AND
            D.REGISTERCOMPACT_ID = E.REGISTERCOMPACT_ID AND
            E.COMPACT_STATE = 1000 AND E.COMPACT_DETAILS = 1000 AND
            A.PROJECT_VALID = 1{where_sql}
        GROUP BY
            A.BUSINESSPROJECT_ID, A.SERVERPARTSHOP_ID, A.GUARANTEE_PRICE,
            A.BUSINESS_TYPE, A.PROJECT_DAYS,
            B.SERVERPART_ID, D.REGISTERCOMPACT_ID,
            C.SHOPROYALTY_ID, C.NATUREDAY, C.GUARANTEERATIO,
            CASE A.BUSINESS_TYPE WHEN 2000 THEN C.RENTFEE ELSE C.MINTURNOVER END,
            C.SERVERPARTSHOP_ID,
            A.BUSINESSPROJECT_NAME, ',' || A.SERVERPARTSHOP_ID || ',',
            A.PROJECT_STARTDATE, A.PROJECT_ENDDATE
        UNION ALL
        SELECT
            A.BUSINESSPROJECT_ID, A.SERVERPARTSHOP_ID, A.GUARANTEE_PRICE,
            A.BUSINESS_TYPE, A.PROJECT_DAYS,
            A.BUSINESSPROJECT_NAME, B.SERVERPART_ID, D.REGISTERCOMPACT_ID,
            NULL, NULL, NULL, NULL, NULL,
            A.PROJECT_STARTDATE, A.PROJECT_ENDDATE,
            ',' || A.SERVERPARTSHOP_ID || ',', 0
        FROM
            T_RTBUSINESSPROJECT D,
            T_RTREGISTERCOMPACT B,
            T_BUSINESSPROJECT A
        WHERE
            A.BUSINESSPROJECT_ID = D.BUSINESSPROJECT_ID AND
            D.REGISTERCOMPACT_ID = B.REGISTERCOMPACT_ID AND
            NOT EXISTS (SELECT 1 FROM T_SHOPROYALTY C
                WHERE A.BUSINESSPROJECT_ID = C.BUSINESSPROJECT_ID) AND
            A.PROJECT_VALID = 1{where_sql}
        GROUP BY
            A.BUSINESSPROJECT_ID, A.SERVERPARTSHOP_ID, A.GUARANTEE_PRICE,
            A.BUSINESS_TYPE, A.PROJECT_DAYS, A.BUSINESSPROJECT_NAME,
            B.SERVERPART_ID, D.REGISTERCOMPACT_ID,
            ',' || A.SERVERPARTSHOP_ID || ',',
            A.PROJECT_STARTDATE, A.PROJECT_ENDDATE"""
    dt_business_project = db.execute_query(project_sql)

    # ===== SQL3: 查询门店数据 (原 Helper L1923-1940) =====
    # 门店查询额外加经营状态和经营模式过滤
    shop_where = where_sql
    if business_state:
        shop_where += f" AND B.BUSINESS_STATE IN ({business_state})"
    if business_type:
        shop_where += f" AND B.BUSINESS_TYPE IN ({business_type})"

    # 达梦使用 LISTAGG 代替 Oracle WM_CONCAT
    shop_sql = f"""SELECT
            A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
            A.SERVERPART_INDEX,
            A.SERVERPART_ID, A.SERVERPART_CODE, A.SERVERPART_NAME,
            A.SERVERPART_TYPE, A.DAYINCAR,
            B.BUSINESS_BRAND, B.SHOPTRADE, B.SHOPSHORTNAME, B.BUSINESS_UNIT,
            LISTAGG(CAST(B.SERVERPARTSHOP_ID AS VARCHAR), ',')
                WITHIN GROUP(ORDER BY B.SERVERPARTSHOP_ID) AS SERVERPARTSHOP_ID,
            MIN(B.BUSINESS_STATE) AS BUSINESS_STATE,
            MIN(B.BUSINESS_TYPE) AS BUSINESS_TYPE
        FROM
            T_SERVERPART A,
            T_SERVERPARTSHOP B
        WHERE
            A.STATISTICS_TYPE = 1000 AND A.STATISTIC_TYPE = 1000 AND
            A.SERVERPART_ID = B.SERVERPART_ID AND B.ISVALID = 1{shop_where}
        GROUP BY
            A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME, A.SPREGIONTYPE_INDEX,
            A.SERVERPART_INDEX,
            A.SERVERPART_ID, A.SERVERPART_CODE, A.SERVERPART_NAME,
            A.SERVERPART_TYPE, A.DAYINCAR,
            B.BUSINESS_BRAND, B.SHOPTRADE, B.SHOPSHORTNAME, B.BUSINESS_UNIT
        ORDER BY B.SHOPTRADE, B.SHOPSHORTNAME"""
    dt_shop = db.execute_query(shop_sql)

    # ===== 遍历门店，关联经营项目和合同 (原 Helper L1942-2099) =====
    for dr_shop in dt_shop:
        sp_type_val = str(dr_shop.get("SERVERPART_TYPE") or "")
        base_model = {
            "COOPMERCHANTS_ID": None,
            "COOPMERCHANTS_ID_Encrypted": None,
            "COOPMERCHANTS_NAME": str(dr_shop.get("BUSINESS_UNIT") or ""),
            "THREEPART_NAME": None,
            "SERVERPART_IDS": str(dr_shop.get("SERVERPART_ID") or ""),
            "SERVERPART_TYPE": _SERVERPART_TYPE_MAP.get(sp_type_val, sp_type_val),
            "SERVERPART_NAME": str(dr_shop.get("SERVERPART_NAME") or ""),
            "SECTIONFLOW_NUM": _safe_int_zero(dr_shop.get("DAYINCAR")),
            "REGISTERCOMPACT_ID": None,
            "BUSINESSPROJECT_ID": None,
            "BUSINESSPROJECT_NAME": None,
            "BUSINESSPROJECT_ICO": None,
            "BRAND_NAME": None,
            "BUSINESSTRADE_NAME": None,
            "BRAND_TYPENAME": None,
            "BUSINESS_TRADE": None,
            "BUSINESS_TYPE": _safe_int(dr_shop.get("BUSINESS_TYPE")),
            "SETTLEMENT_MODES": None,
            "PROJECT_STARTDATE": None,
            "PROJECT_ENDDATE": None,
            "PROJECT_AMOUNT": None,
            "COMPACT_DURATION": None,
            "PROJECT_DAYS": None,
            "BUSINESSDAYS": None,
            "DAILY_AMOUNT": None,
            "SERVERPARTSHOP_ID": str(dr_shop.get("SERVERPARTSHOP_ID") or ""),
            "SERVERPARTSHOP_NAME": str(dr_shop.get("SHOPSHORTNAME") or ""),
            "BUSINESS_STATE": _safe_int(dr_shop.get("BUSINESS_STATE")),
            "COMMISSION_RATIO": None,
            "ACCOUNT_DATE": None,
            "PAYABLE_AMOUNT": None,
            "COMPACT_NAME": None,
            "COMMODITY_COUNT": None,
            "REVENUE_AMOUNT": None,
            "ROYALTY_PRICE": None,
            "SUBROYALTY_PRICE": None,
            "CompactWarning": False,
            "ProjectWarning": False,
            "ProjectAccountDetailList": None,
        }

        # 品牌查询 (原 Helper L1967-1986)
        business_brand = dr_shop.get("BUSINESS_BRAND")
        if business_brand is not None and str(business_brand) != "":
            brand_sql = f"SELECT BRAND_NAME, BRAND_INTRO FROM T_BRAND WHERE BRAND_ID = {business_brand}"
            brand_rows = db.execute_query(brand_sql)
            if brand_rows:
                base_model["BRAND_NAME"] = str(brand_rows[0].get("BRAND_NAME") or "")
                brand_intro = str(brand_rows[0].get("BRAND_INTRO") or "")
                if brand_intro:
                    if brand_intro.startswith("/"):
                        base_model["BUSINESSPROJECT_ICO"] = _COOP_MERCHANT_URLS + brand_intro
                    else:
                        base_model["BUSINESSPROJECT_ICO"] = brand_intro

        # 查询匹配的经营项目 (原 Helper L1989-2098)
        shop_ids_str = str(dr_shop.get("SERVERPARTSHOP_ID") or "")
        matched_projects = []
        for p in dt_business_project:
            relate_shop = str(p.get("RELATE_SHOP") or "")
            for sid in shop_ids_str.split(","):
                if sid and f",{sid}," in relate_shop:
                    matched_projects.append(p)
                    break

        if matched_projects:
            # 去重: 按 BUSINESSPROJECT_ID 分组取唯一
            seen_project_ids = set()
            unique_projects = []
            for mp in matched_projects:
                bp_id = mp.get("BUSINESSPROJECT_ID")
                if bp_id not in seen_project_ids:
                    seen_project_ids.add(bp_id)
                    unique_projects.append(mp)

            for dr_project in unique_projects:
                item = dict(base_model)  # 复制基础模型
                item["BUSINESSPROJECT_ID"] = _safe_int(dr_project.get("BUSINESSPROJECT_ID"))
                item["BUSINESSPROJECT_NAME"] = str(dr_project.get("BUSINESSPROJECT_NAME") or "")
                # 日期格式: 去掉时间部分 (原 Helper L2030-2031)
                item["PROJECT_STARTDATE"] = _format_date_only(dr_project.get("PROJECT_STARTDATE"))
                item["PROJECT_ENDDATE"] = _format_date_only(dr_project.get("PROJECT_ENDDATE"))

                # 查找对应合同 (原 Helper L2033-2087)
                rc_id = str(dr_project.get("REGISTERCOMPACT_ID") or "")
                compact_match = [c for c in dt_compact
                                 if str(c.get("REGISTERCOMPACT_ID")) == rc_id]
                if compact_match:
                    dr_compact = compact_match[0]
                    item["COOPMERCHANTS_NAME"] = str(dr_compact.get("SECONDPART_NAME") or "")
                    # 原 C# .ToString(): null→""，保持空字符串而非 None
                    threepart = dr_compact.get("THREEPART_LINKMAN")
                    item["THREEPART_NAME"] = str(threepart) if threepart else ""
                    item["REGISTERCOMPACT_ID"] = rc_id
                    item["COMPACT_NAME"] = str(dr_compact.get("COMPACT_NAME") or "")
                    item["COMPACT_DURATION"] = _safe_int(dr_compact.get("DURATION"))
                    item["BUSINESS_TRADE"] = _safe_int(dr_compact.get("BUSINESS_TRADE"))

                    # CompactWarning (原 Helper L2052-2060)
                    # 注意: 原 C# 用 .ToString() == "" 判定空值
                    # Python 中 not 0.0 为 True 会误判, 必须用 _is_empty() 只检查 None/空串
                    if (_is_empty(dr_compact.get("COMPACT_CHILDTYPE"))
                            or str(dr_compact.get("SECONDPART_NAME")) == "待补充"
                            or _is_empty(dr_compact.get("SECONDPART_MOBILE"))
                            or _is_empty(dr_compact.get("SECONDPART_LINKMAN"))
                            or str(dr_compact.get("SECONDPART_ID")) == "-1"
                            or _is_empty(dr_compact.get("BUSINESS_TRADE"))
                            or _is_empty(dr_compact.get("BUSINESS_TYPE"))
                            or _is_empty(dr_compact.get("OPERATING_AREA"))
                            or _is_empty(dr_compact.get("OPERATING_SCOPE"))
                            or _is_empty(dr_compact.get("SETTLEMENT_MODES"))
                            or _safe_int_zero(dr_compact.get("ATTACHMENT_STATE")) == 0):
                        item["CompactWarning"] = True

                    # ProjectWarning (原 Helper L2062-2076)
                    # 查该项目所有记录
                    bp_id = str(dr_project.get("BUSINESSPROJECT_ID"))
                    all_for_project = [p for p in dt_business_project
                                       if str(p.get("BUSINESSPROJECT_ID")) == bp_id]
                    guarantee_price = _safe_decimal(dr_project.get("GUARANTEE_PRICE"))
                    sep_count_sum = sum(_safe_decimal(p.get("SEPARATE_COUNT")) for p in all_for_project)
                    guarantee_sum = sum(_safe_decimal(p.get("GUARANTEE_AMOUNT")) for p in all_for_project)

                    if (_is_empty(dr_project.get("SERVERPARTSHOP_ID"))
                            or guarantee_price == 0
                            or sep_count_sum == 0
                            or guarantee_price != guarantee_sum):
                        item["ProjectWarning"] = True
                    elif (str(dr_project.get("BUSINESS_TYPE")) != "2000"
                          and any(not p.get("ROYALTY_SHOP") for p in all_for_project)):
                        item["ProjectWarning"] = True

                    # 移除有经营项目的合同 (原 Helper L2078-2081)
                    dt_ex_compact_ids.discard(rc_id)
                else:
                    item["CompactWarning"] = True
                    item["ProjectWarning"] = True

                account_list.append(item)
        else:
            # 无经营项目匹配 (原 Helper L2092-2098)
            base_model["CompactWarning"] = True
            base_model["ProjectWarning"] = True
            account_list.append(base_model)

    # ===== 无门店关联的合同追加到 NullList (原 Helper L2101-2132) =====
    if not business_type and not business_state:
        for dr_compact in dt_compact:
            rc_id = str(dr_compact.get("REGISTERCOMPACT_ID"))
            if rc_id not in dt_ex_compact_ids:
                continue
            item = {
                "COOPMERCHANTS_ID": None,
                "COOPMERCHANTS_ID_Encrypted": None,
                "COOPMERCHANTS_NAME": str(dr_compact.get("SECONDPART_NAME") or ""),
                "THREEPART_NAME": None,
                "SERVERPART_IDS": str(dr_compact.get("SERVERPART_ID") or ""),
                "SERVERPART_TYPE": None,
                "SERVERPART_NAME": None,
                "SECTIONFLOW_NUM": None,
                "REGISTERCOMPACT_ID": rc_id,
                "BUSINESSPROJECT_ID": None,
                "BUSINESSPROJECT_NAME": None,
                "BUSINESSPROJECT_ICO": None,
                "BRAND_NAME": None,
                "BUSINESSTRADE_NAME": None,
                "BRAND_TYPENAME": None,
                "BUSINESS_TRADE": None,
                "BUSINESS_TYPE": None,
                "SETTLEMENT_MODES": None,
                "PROJECT_STARTDATE": None,
                "PROJECT_ENDDATE": None,
                "PROJECT_AMOUNT": None,
                "COMPACT_DURATION": None,
                "PROJECT_DAYS": None,
                "BUSINESSDAYS": None,
                "DAILY_AMOUNT": None,
                "SERVERPARTSHOP_ID": None,
                "SERVERPARTSHOP_NAME": None,
                "BUSINESS_STATE": None,
                "COMMISSION_RATIO": None,
                "ACCOUNT_DATE": None,
                "PAYABLE_AMOUNT": None,
                "COMPACT_NAME": str(dr_compact.get("COMPACT_NAME") or ""),
                "COMMODITY_COUNT": None,
                "REVENUE_AMOUNT": None,
                "ROYALTY_PRICE": None,
                "SUBROYALTY_PRICE": None,
                "CompactWarning": True,
                "ProjectWarning": True,
                "ProjectAccountDetailList": None,
            }
            # 查该合同的经营项目 (原 Helper L2120-2128)
            sp_id = str(dr_compact.get("SERVERPART_ID") or "")
            for p in dt_business_project:
                if (str(p.get("REGISTERCOMPACT_ID")) == rc_id
                        and str(p.get("SERVERPART_ID")) == sp_id):
                    item["BUSINESSPROJECT_ID"] = _safe_int(p.get("BUSINESSPROJECT_ID"))
                    item["BUSINESSPROJECT_NAME"] = str(p.get("BUSINESSPROJECT_NAME") or "")
                    break
            null_list.append(item)

    # ===== 过滤 (原 Helper L2134-2149) =====
    if account_list:
        # 移除自营无合同数据 (原 Helper L2137)
        account_list = [item for item in account_list
                        if not (item.get("BUSINESS_TYPE") == 1000
                                and not item.get("REGISTERCOMPACT_ID"))]
        # 追加无门店关联合同
        if null_list:
            account_list.extend(null_list)

    # AbnormalShop 过滤 (原 Helper L2145-2148)
    if abnormal_shop:
        account_list = [item for item in account_list
                        if item.get("BUSINESS_STATE") == 1000
                        and (not item.get("REGISTERCOMPACT_ID")
                             or item.get("BUSINESSPROJECT_ID") is None)]

    return account_list, []


def get_serverpart_ud_type_tree(
    db: DatabaseHelper,
    server_part_id: str,
    shop_trade: str = "",
    user_defined_type_state: int = None,
) -> list:
    """
    获取服务区自定义类别树 (原 C# USERDEFINEDTYPEHelper.GetServerpartUDTypeTree L574-692)
    返回: NestingModel<CommonTypeModel> 列表（3层树: 区域→服务区→自定义类别）
    """
    # 构建 WHERE 条件 (原 Helper L577-587)
    # 注意: T_USERDEFINEDTYPE.SERVERPART_ID 是 VARCHAR，需要用字符串方式比较
    # 把 "369,370" 转为 "'369','370'"
    sp_ids_quoted = ",".join(f"'{x.strip()}'" for x in server_part_id.split(",") if x.strip())
    where_sql = f" AND A.SERVERPART_ID IN ({sp_ids_quoted})"
    if shop_trade:
        where_sql += f" AND A.BUSINESSTYPE IN ({shop_trade})"
    if user_defined_type_state is not None:
        where_sql += f" AND A.USERDEFINEDTYPE_STATE = {user_defined_type_state}"

    # SQL: JOIN 自定义类别和服务区 (原 Helper L589-598)
    ud_sql = f"""SELECT
            B.SPREGIONTYPE_ID, B.SPREGIONTYPE_NAME, B.SPREGIONTYPE_INDEX,
            B.SERVERPART_ID, B.SERVERPART_NAME, B.SERVERPART_INDEX, B.SERVERPART_CODE,
            A.USERDEFINEDTYPE_ID, A.USERDEFINEDTYPE_NAME, A.USERDEFINEDTYPE_INDEX,
            A.BUSINESSTYPE, A.USERDEFINEDTYPE_STATE
        FROM
            T_USERDEFINEDTYPE A,
            T_SERVERPART B
        WHERE
            A.SERVERPART_ID = CAST(B.SERVERPART_ID AS VARCHAR){where_sql}"""
    dt_ud_type = db.execute_query(ud_sql)

    if not dt_ud_type:
        return []

    # 查门店数据 (原 Helper L602-608)
    shop_where = f"WHERE ISVALID = 1 AND SHOPSHORTNAME IS NOT NULL AND SERVERPART_ID IN ({server_part_id})"
    if shop_trade:
        # 原 C# 用单引号包裹: IN ('1','2')
        quoted = "','".join(shop_trade.split(","))
        shop_where += f" AND SHOPTRADE IN ('{quoted}')"
    shop_sql = f"SELECT SERVERPART_ID, SHOPTRADE, SHOPSHORTNAME FROM T_SERVERPARTSHOP {shop_where}"
    dt_shop = db.execute_query(shop_sql)

    # 构建门店快速查找字典: (serverpart_id, shoptrade) → shopshortname
    shop_map = {}
    for s in dt_shop:
        key = (str(s.get("SERVERPART_ID")), str(s.get("SHOPTRADE")))
        if key not in shop_map:
            shop_map[key] = str(s.get("SHOPSHORTNAME") or "")

    # 提取去重的区域列表 (原 Helper L611-612)
    regions = {}
    for r in dt_ud_type:
        rid = r.get("SPREGIONTYPE_ID")
        if rid is not None and rid not in regions:
            regions[rid] = {
                "id": rid,
                "name": str(r.get("SPREGIONTYPE_NAME") or ""),
                "index": r.get("SPREGIONTYPE_INDEX"),
            }
    # 按 SPREGIONTYPE_INDEX, SPREGIONTYPE_ID 排序
    sorted_regions = sorted(regions.values(), key=lambda x: (x["index"] or 0, x["id"] or 0))

    ud_type_tree = []

    # 遍历区域，构建树 (原 Helper L613-630)
    for region in sorted_regions:
        region_node = {
            "node": {
                "label": region["name"],
                "value": _safe_int_zero(region["id"]),
                "key": f"0-{region['id']}",
                "type": 0,
                "desc": None,
                "ico": None,
            },
            "children": [],
        }

        # 过滤当前区域的数据
        region_data = [r for r in dt_ud_type if r.get("SPREGIONTYPE_ID") == region["id"]]
        _bind_serverpart_ud_type_node(region_node["children"], region_data, shop_map)

        ud_type_tree.append(region_node)

    # 处理没有区域的数据 (原 Helper L632-633)
    null_region_data = [r for r in dt_ud_type if r.get("SPREGIONTYPE_ID") is None]
    if null_region_data:
        _bind_serverpart_ud_type_node(ud_type_tree, null_region_data, shop_map)

    return ud_type_tree


def _bind_serverpart_ud_type_node(tree_list: list, ud_data: list, shop_map: dict):
    """
    绑定服务区自定义类别节点 (原 C# BindServerpartUDTypeNode L647-692)
    """
    # 提取去重的服务区列表
    serverparts = {}
    for r in ud_data:
        sid = r.get("SERVERPART_ID")
        if sid is not None and sid not in serverparts:
            serverparts[sid] = {
                "id": sid,
                "name": str(r.get("SERVERPART_NAME") or ""),
                "index": r.get("SERVERPART_INDEX"),
                "code": str(r.get("SERVERPART_CODE") or ""),
            }
    # 按 SERVERPART_INDEX, SERVERPART_CODE 排序
    sorted_sps = sorted(serverparts.values(), key=lambda x: (x["index"] or 0, x["code"]))

    for sp in sorted_sps:
        sp_node = {
            "node": {
                "label": sp["name"],
                "value": _safe_int_zero(sp["id"]),
                "key": f"1-{sp['id']}",
                "type": 1,
                "desc": None,
                "ico": None,
            },
            "children": [],
        }

        # 过滤当前服务区的自定义类别，按 BUSINESSTYPE, USERDEFINEDTYPE_STATE desc, USERDEFINEDTYPE_INDEX, USERDEFINEDTYPE_ID 排序
        sp_ud_data = [r for r in ud_data if r.get("SERVERPART_ID") == sp["id"]]
        sp_ud_data.sort(key=lambda x: (
            x.get("BUSINESSTYPE") or 0,
            -(x.get("USERDEFINEDTYPE_STATE") or 0),  # desc
            x.get("USERDEFINEDTYPE_INDEX") or 0,
            x.get("USERDEFINEDTYPE_ID") or 0,
        ))

        for ud in sp_ud_data:
            ud_id = ud.get("USERDEFINEDTYPE_ID")
            ud_name = str(ud.get("USERDEFINEDTYPE_NAME") or "")
            ud_state = str(ud.get("USERDEFINEDTYPE_STATE") or "")
            biz_type = str(ud.get("BUSINESSTYPE") or "")

            # 拼接门店简称前缀 (原 Helper L680-685)
            shop_key = (str(sp["id"]), biz_type)
            if shop_key in shop_map:
                ud_name = f"【{shop_map[shop_key]}】{ud_name}"

            ud_node = {
                "node": {
                    "label": ud_name,
                    "value": _safe_int_zero(ud_id),
                    "key": f"2-{ud_id}",
                    "type": 2,
                    "desc": ud_state,
                    "ico": None,
                },
                "children": None,
            }
            sp_node["children"].append(ud_node)

        tree_list.append(sp_node)


def get_serverpart_detail(
    db: DatabaseHelper,
    serverpart_id: int = None,
    field_enum_id: int = None,
) -> dict:
    """
    获取服务区站点明细 (原 C# ServerpartHelper.GetSERVERPARTDetail L818-896)
    按 SERVERPARTId 或 FieldEnumId 查单条记录，附加 RtServerPart + ServerPartInfo
    """
    # 空模型默认值 (原 Helper L820: 新的空 SERVERPARTModel)
    empty_model = {
        "SERVERPART_ID": None, "SERVERPART_NAME": None, "SERVERPART_ADDRESS": None,
        "SERVERPART_INDEX": None, "EXPRESSWAY_NAME": None, "SELLERCOUNT": None,
        "SERVERPART_AREA": None, "SERVERPART_X": None, "SERVERPART_Y": None,
        "SERVERPART_TEL": None, "SERVERPART_INFO": None, "PROVINCE_CODE": None,
        "CITY_CODE": None, "COUNTY_CODE": None, "SERVERPART_CODE": None,
        "FIELDENUM_ID": None, "SERVERPART_IPADDRESS": None, "SERVERPART_TYPE": None,
        "DAYINCAR": None, "HKBL": None, "STARTDATE": None, "OWNEDCOMPANY": None,
        "FLOORAREA": None, "BUSINESSAREA": None, "SHAREAREA": None, "TOTALPARKING": None,
        "MANAGERCOMPANY": None, "SHORTNAME": None, "REGIONTYPE_ID": None,
        "STATISTIC_TYPE": None, "PROVINCE_NAME": None, "SPREGIONTYPE_ID": None,
        "SPREGIONTYPE_NAME": None, "SPREGIONTYPE_INDEX": None, "REGIONTYPE_NAME": None,
        "STATISTICS_TYPE": None, "STAFF_ID": None, "STAFF_NAME": None,
        "OPERATE_DATE": None, "SERVERPART_DESC": None, "OWNERUNIT_ID": None,
        "OWNERUNIT_NAME": None, "RtServerPart": None, "ServerPartInfo": None,
    }

    # 查询主表 (原 Helper L822-836)
    if serverpart_id is not None:
        rows = db.execute_query(
            f"SELECT * FROM T_SERVERPART WHERE SERVERPART_ID = {serverpart_id}")
    elif field_enum_id is not None:
        rows = db.execute_query(
            f"SELECT * FROM T_SERVERPART WHERE FIELDENUM_ID = {field_enum_id}")
    else:
        return empty_model

    if not rows:
        return empty_model

    sp = rows[0]
    # 赋值所有字段 (原 Helper L840-881)
    for key in empty_model:
        if key in ("RtServerPart", "ServerPartInfo"):
            continue
        if key in sp:
            empty_model[key] = sp[key]

    sp_id = sp.get("SERVERPART_ID")

    # 查附属信息 RtServerPart (原 Helper L882)
    rt_rows = db.execute_query(
        f"SELECT * FROM T_RTSERVERPART WHERE SERVERPART_ID = {sp_id}")
    empty_model["RtServerPart"] = rt_rows[0] if rt_rows else None

    # 查详情列表 ServerPartInfo (原 Helper L884-892)
    info_rows = db.execute_query(
        f"SELECT * FROM T_SERVERPARTINFO WHERE SERVERPART_ID = {sp_id} ORDER BY SERVERPART_REGION")
    empty_model["ServerPartInfo"] = info_rows if info_rows else None

    return empty_model


def _is_empty(val):
    """
    模拟 C# 的 .ToString() == "" 语义
    只有 None 和空字符串视为空，数值 0/0.0 不视为空
    """
    if val is None:
        return True
    return str(val).strip() == ""


def _safe_int(val):
    """安全转 int，None 返回 None"""
    if val is None:
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def _safe_int_zero(val):
    """安全转 int，None 返回 0（模拟 C# TryParseToInt() 语义）"""
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def _safe_decimal(val):
    """安全转 Decimal，None 返回 Decimal(0)（匹配 C# Decimal 精确计算）"""
    from decimal import Decimal, InvalidOperation
    if val is None:
        return Decimal(0)
    try:
        return Decimal(str(val))
    except (ValueError, TypeError, InvalidOperation):
        return Decimal(0)


def _format_date_only(val):
    """格式化日期为 yyyy/M/d（去掉时间部分），与原 C# .Split(' ')[0] 一致"""
    if val is None:
        return None
    from datetime import datetime as dt
    if isinstance(val, dt):
        return f"{val.year}/{val.month}/{val.day}"
    s = str(val).split(" ")[0]
    # 尝试解析并格式化
    try:
        d = dt.strptime(s, "%Y-%m-%d")
        return f"{d.year}/{d.month}/{d.day}"
    except ValueError:
        return s


# 20. SolidServerpartWeather - 存储服务区天气情况
#     对应原 ServerpartHelper.SolidServerpartWeather (L1181-1329)
#     + WEATHERHelper.GetWeather (L289-332)
#     + WEATHERHelper.SynchroWEATHER (L201-256)

# 天气 API 配置（原 C# WEATHERHelper 常量）
_WEATHER_API_HOST = "http://tianqi3.market.alicloudapi.com"
_WEATHER_API_PATH = "/gps-to-weather"
_WEATHER_APPCODE = "99f7d21d35e647e98706f75109f4b655"


def _get_weather(longitude: str, latitude: str) -> dict:
    """
    根据经纬度获取天气（原 WEATHERHelper.GetWeather L289-332）
    调用阿里云天气 API，返回 JSON 响应
    """
    import requests

    url = f"{_WEATHER_API_HOST}{_WEATHER_API_PATH}"
    params = {
        "from": "5",
        "lng": str(longitude),
        "lat": str(latitude),
        "needMoreDay": "0",
        "needIndex": "0",
        "needHourData": "0",
        "need3HourForcast": "0",
        "needAlarm": "0",
    }
    headers = {
        "Authorization": f"APPCODE {_WEATHER_APPCODE}"
    }
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def _synchro_weather(db: DatabaseHelper, weather_model: dict) -> bool:
    """
    同步天气记录到 T_WEATHER（原 WEATHERHelper.SynchroWEATHER L201-256）
    操作 HIGHWAY_STORAGE.T_WEATHER 表

    有 WEATHER_ID → 更新；无 → 用 SEQ_WEATHER.NEXTVAL 新增
    STATISTICS_DATE 以日期格式 TO_DATE('yyyyMMdd', 'YYYYMMDD') 写入
    """
    # 排除非数据库字段
    exclude_fields = {"STATISTICS_DATE_Start", "STATISTICS_DATE_End", "SERVERPART_IDS"}

    # 处理日期字段
    statistics_date = weather_model.get("STATISTICS_DATE")
    date_sql = "NULL"
    if statistics_date and str(statistics_date).strip():
        from datetime import datetime as dt
        try:
            d = dt.strptime(str(statistics_date).split(" ")[0], "%Y-%m-%d")
            date_sql = f"TO_DATE('{d.strftime('%Y%m%d')}', 'YYYYMMDD')"
        except ValueError:
            try:
                d = dt.strptime(str(statistics_date).split(" ")[0], "%Y/%m/%d")
                date_sql = f"TO_DATE('{d.strftime('%Y%m%d')}', 'YYYYMMDD')"
            except ValueError:
                date_sql = f"TO_DATE('{statistics_date}', 'YYYYMMDD')"

    weather_id = weather_model.get("WEATHER_ID")
    table_name = "T_WEATHER"

    if weather_id is not None:
        # 更新：先检查是否存在
        check = db.execute_scalar(
            f"SELECT COUNT(*) FROM {table_name} WHERE WEATHER_ID = {weather_id}"
        )
        if not check or check == 0:
            return False

        # 构建 UPDATE
        set_parts = []
        for key, value in weather_model.items():
            if key == "WEATHER_ID" or key in exclude_fields:
                continue
            if key == "STATISTICS_DATE":
                set_parts.append(f"STATISTICS_DATE = {date_sql}")
                continue
            if key == "RECORD_DATE":
                set_parts.append("RECORD_DATE = SYSDATE")
                continue
            if value is None:
                set_parts.append(f"{key} = NULL")
            elif isinstance(value, str):
                set_parts.append(f"{key} = '{value}'")
            else:
                set_parts.append(f"{key} = {value}")

        if set_parts:
            sql = f"UPDATE {table_name} SET {', '.join(set_parts)} WHERE WEATHER_ID = {weather_id}"
            db.execute_non_query(sql)
    else:
        # 新增：获取序列值
        try:
            new_id = db.execute_scalar("SELECT SEQ_WEATHER.NEXTVAL FROM DUAL")
        except Exception:
            new_id = db.execute_scalar(f"SELECT NVL(MAX(WEATHER_ID), 0) + 1 FROM {table_name}") or 1

        weather_model["WEATHER_ID"] = new_id

        cols = ["WEATHER_ID"]
        vals = [str(new_id)]
        for key, value in weather_model.items():
            if key == "WEATHER_ID" or key in exclude_fields:
                continue
            if key == "STATISTICS_DATE":
                cols.append("STATISTICS_DATE")
                vals.append(date_sql)
                continue
            if key == "RECORD_DATE":
                cols.append("RECORD_DATE")
                vals.append("SYSDATE")
                continue
            if value is None:
                continue
            cols.append(key)
            if isinstance(value, str):
                vals.append(f"'{value}'")
            else:
                vals.append(str(value))

        sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        db.execute_non_query(sql)

    return True


def _safe_float(val, default=0.0):
    """安全转 float"""
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def solid_serverpart_weather(db: DatabaseHelper, serverpart_ids: str) -> bool:
    """
    存储服务区天气情况（原 ServerpartHelper.SolidServerpartWeather L1181-1325）

    完整逻辑:
    1. 查询 T_WEATHER 获取今日+明日已有天气记录
    2. 查询 T_SERVERPART 获取服务区坐标
    3. 对每个有坐标的服务区调用天气 API
    4. 解析 showapi 返回的 now/f1(今日)/f2(明日) 数据
    5. 对今日和明日分别做新增/更新 T_WEATHER 记录
    """
    from datetime import datetime, timedelta

    if not serverpart_ids or not serverpart_ids.strip():
        return False

    cur_date = datetime.now().date()
    next_date = cur_date + timedelta(days=1)
    cur_date_str = cur_date.strftime("%Y-%m-%d")
    next_date_str = next_date.strftime("%Y-%m-%d")
    day_after_str = (cur_date + timedelta(days=2)).strftime("%Y-%m-%d")

    # 1. 查询今日+明日已有天气记录（原 C# L1185-1196）
    weather_sql = (
        f"SELECT * FROM T_WEATHER WHERE SERVERPART_ID IN ({serverpart_ids}) "
        f"AND STATISTICS_DATE >= TO_DATE('{cur_date_str}', 'YYYY-MM-DD') "
        f"AND STATISTICS_DATE < TO_DATE('{day_after_str}', 'YYYY-MM-DD')"
    )
    existing_weather = db.execute_query(weather_sql)

    # 按 (SERVERPART_ID, 日期) 建立索引
    weather_today = {}  # sp_id -> weather_model
    weather_tomorrow = {}
    for w in existing_weather:
        sp_id = w.get("SERVERPART_ID")
        stat_date = w.get("STATISTICS_DATE")
        if stat_date is not None:
            from datetime import datetime as dt
            if isinstance(stat_date, dt):
                d = stat_date.date()
            else:
                try:
                    d = dt.strptime(str(stat_date).split(" ")[0], "%Y-%m-%d").date()
                except ValueError:
                    continue
            if d == cur_date:
                weather_today[sp_id] = w
            elif d == next_date:
                weather_tomorrow[sp_id] = w

    # 2. 查询服务区坐标（原 C# L1198-1204）
    sp_sql = (
        f"SELECT SERVERPART_ID, SERVERPART_NAME, SERVERPART_X, SERVERPART_Y "
        f"FROM T_SERVERPART WHERE SERVERPART_ID IN ({serverpart_ids})"
    )
    serverpart_list = db.execute_query(sp_sql)

    if not serverpart_list:
        return False

    # 3. 对每个服务区获取天气并存储（原 C# L1206-1322）
    for sp in serverpart_list:
        sp_id = sp.get("SERVERPART_ID")
        sp_name = sp.get("SERVERPART_NAME", "")
        sp_x = sp.get("SERVERPART_X")
        sp_y = sp.get("SERVERPART_Y")

        # 原 C# L1208: 无坐标则跳过
        if sp_x is None or sp_y is None:
            continue

        try:
            # 调用天气 API（原 C# L1213）
            weather_data = _get_weather(str(sp_x), str(sp_y))
        except Exception as e:
            logger.warning(f"获取服务区 {sp_id} ({sp_name}) 天气失败: {e}")
            continue

        # 原 C# L1231: 检查 API 返回码
        if str(weather_data.get("showapi_res_code")) != "0":
            logger.warning(f"天气 API 返回错误: 服务区 {sp_id}, code={weather_data.get('showapi_res_code')}")
            continue

        weather_info = weather_data.get("showapi_res_body", {})

        # === 同步今日天气（原 C# L1236-1280） ===
        now_info = weather_info.get("now", {})
        f1_info = weather_info.get("f1", {})

        if sp_id in weather_today:
            # 已有记录 → 更新（原 C# L1238-1254）
            existing = weather_today[sp_id]
            existing["CUR_WEATHER"] = str(now_info.get("weather", ""))
            existing["CUR_WEATHER_PIC"] = str(now_info.get("weather_pic", ""))
            existing["CUR_AIR_TEMPERATURE"] = _safe_float(now_info.get("temperature"))
            existing["DAY_WEATHER"] = str(f1_info.get("day_weather", ""))
            existing["DAY_WEATHER_PIC"] = str(f1_info.get("day_weather_pic", ""))
            existing["DAY_AIR_TEMPERATURE"] = _safe_float(f1_info.get("day_air_temperature"))
            existing["NIGHT_WEATHER"] = str(f1_info.get("night_weather", ""))
            existing["NIGHT_WEATHER_PIC"] = str(f1_info.get("night_weather_pic", ""))
            existing["NIGHT_AIR_TEMPERATURE"] = _safe_float(f1_info.get("night_air_temperature"))
            existing["RECORD_DATE"] = "SYSDATE"
            _synchro_weather(db, existing)
        else:
            # 无记录 → 新增（原 C# L1258-1278）
            new_weather = {
                "STATISTICS_DATE": cur_date_str,
                "SERVERPART_ID": sp_id,
                "SERVERPART_NAME": sp_name,
                "CUR_WEATHER": str(now_info.get("weather", "")),
                "CUR_WEATHER_PIC": str(now_info.get("weather_pic", "")),
                "CUR_AIR_TEMPERATURE": _safe_float(now_info.get("temperature")),
                "DAY_WEATHER": str(f1_info.get("day_weather", "")),
                "DAY_WEATHER_PIC": str(f1_info.get("day_weather_pic", "")),
                "DAY_AIR_TEMPERATURE": _safe_float(f1_info.get("day_air_temperature")),
                "NIGHT_WEATHER": str(f1_info.get("night_weather", "")),
                "NIGHT_WEATHER_PIC": str(f1_info.get("night_weather_pic", "")),
                "NIGHT_AIR_TEMPERATURE": _safe_float(f1_info.get("night_air_temperature")),
                "WEATHER_STATE": 1,
                "RECORD_DATE": "SYSDATE",
            }
            _synchro_weather(db, new_weather)

        # === 同步明日天气（原 C# L1282-1319） ===
        f2_info = weather_info.get("f2", {})

        if sp_id in weather_tomorrow:
            # 已有记录 → 更新（原 C# L1286-1297）
            existing = weather_tomorrow[sp_id]
            existing["DAY_WEATHER"] = str(f2_info.get("day_weather", ""))
            existing["DAY_WEATHER_PIC"] = str(f2_info.get("day_weather_pic", ""))
            existing["DAY_AIR_TEMPERATURE"] = _safe_float(f2_info.get("day_air_temperature"))
            existing["NIGHT_WEATHER"] = str(f2_info.get("night_weather", ""))
            existing["NIGHT_WEATHER_PIC"] = str(f2_info.get("night_weather_pic", ""))
            existing["NIGHT_AIR_TEMPERATURE"] = _safe_float(f2_info.get("night_air_temperature"))
            existing["RECORD_DATE"] = "SYSDATE"
            _synchro_weather(db, existing)
        else:
            # 无记录 → 新增（原 C# L1301-1317）
            new_weather = {
                "STATISTICS_DATE": next_date_str,
                "SERVERPART_ID": sp_id,
                "SERVERPART_NAME": sp_name,
                "DAY_WEATHER": str(f2_info.get("day_weather", "")),
                "DAY_WEATHER_PIC": str(f2_info.get("day_weather_pic", "")),
                "DAY_AIR_TEMPERATURE": _safe_float(f2_info.get("day_air_temperature")),
                "NIGHT_WEATHER": str(f2_info.get("night_weather", "")),
                "NIGHT_WEATHER_PIC": str(f2_info.get("night_weather_pic", "")),
                "NIGHT_AIR_TEMPERATURE": _safe_float(f2_info.get("night_air_temperature")),
                "WEATHER_STATE": 1,
                "RECORD_DATE": "SYSDATE",
            }
            _synchro_weather(db, new_weather)

    return True

