from __future__ import annotations
# -*- coding: utf-8 -*-
"""
基础信息-散装独立接口 路由
替代原 BaseInfoController 中不属于标准 CRUD 的独立接口

按 BaseInfoController 中出现顺序排列。
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, Header, Body
from loguru import logger

from routers.deps import get_db, get_int_header
from core.database import DatabaseHelper
from models.base import Result
from services.base_info import base_info_misc_service as service

router = APIRouter()


# =====================================
# 1. GetShopShortNames - 获取服务区门店简称
#    路由: BaseInfo/GetShopShortNames
#    方法: GET + POST
#    原 C# 返回: JsonList<string>
# =====================================
@router.api_route("/BaseInfo/GetShopShortNames", methods=["GET", "POST"])
async def get_shop_short_names(
    request: Request,
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    ShopTrade: Optional[str] = Query("", description="商品业态"),
    BusinessType: Optional[str] = Query("1000", description="经营模式，默认自营1000"),
    BusinessState: Optional[str] = Query("", description="经营状态"),
    ShopValid: Optional[int] = Query(1, description="有效状态，默认有效1"),
    ExcludeStaffMeal: bool = Query(True, description="是否排除员工餐"),
    ShowFinance: bool = Query(False, description="是否显示财务共享业态"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区门店简称列表（查询自营业态有哪些门店）"""
    try:
        # 如果 ServerpartId 为空，从 Header 获取 ProvinceCode 和 ServerpartCodes 反查
        if not ServerpartId or not ServerpartId.strip():
            header_province = ProvinceCode
            if provincecode and not header_province:
                header_province = int(provincecode)
            header_codes = serverpartcodes or ""

            if header_province or header_codes:
                ServerpartId = service._get_serverpart_ids_by_codes(
                    db, header_province, header_codes
                )

        result = service.get_shop_short_names(
            db, ServerpartId, ShopTrade, BusinessType,
            BusinessState, ShopValid, ExcludeStaffMeal, ShowFinance
        )

        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetShopShortNames 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 2. GetServerpartShopInfo - 根据编码获取门店信息
#    路由: BaseInfo/GetServerpartShopInfo
#    方法: GET + POST
# =====================================
@router.api_route("/BaseInfo/GetServerpartShopInfo", methods=["GET", "POST"])
async def get_serverpart_shop_info(
    ServerpartCode: str = Query("", description="服务区编码"),
    ShopCode: str = Query("", description="门店编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """根据服务区编码和门店编码获取门店信息"""
    try:
        result = service.get_serverpart_shop_info(db, ServerpartCode, ShopCode)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": result
        }
    except Exception as e:
        logger.error(f"GetServerpartShopInfo 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 3. GetServerpartDDL - 服务区下拉框
#    路由: BaseInfo/GetServerpartDDL
#    方法: GET
# =====================================
@router.get("/BaseInfo/GetServerpartDDL")
async def get_serverpart_ddl(
    request: Request,
    ServerpartCodes: Optional[str] = Query(None, description="服务区编码集合"),
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartType: str = Query("1000", description="站点类型"),
    StatisticsType: Optional[str] = Query(None, description="统计类型"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区下拉框数据"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        # 优先用 query 参数，否则用 header
        codes = ServerpartCodes or serverpartcodes
        province = ProvinceCode or provincecode

        result = service.get_serverpart_ddl(
            db, codes, province, ServerpartType, StatisticsType
        )
        # 原 C# 返回 JsonMsg<JsonList<CommonModel>> — 嵌套结构
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetServerpartDDL 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 4. GetServerpartTree - 区域服务区树
#    路由: BaseInfo/GetServerpartTree
#    方法: GET
# =====================================
@router.get("/BaseInfo/GetServerpartTree")
async def get_serverpart_tree(
    request: Request,
    ProvinceCode: int = Query(..., description="省份编码"),
    SPRegionType_ID: Optional[int] = Query(None, description="区域类型内码"),
    ServerpartType: str = Query("1000", description="站点类型"),
    StatisticsType: Optional[str] = Query(None, description="统计类型"),
    ServerpartIds: Optional[str] = Query(None, description="服务区内码集合"),
    ServerpartCodes: Optional[str] = Query(None, description="服务区编码集合"),
    ShowSPRegion: bool = Query(True, description="是否显示区域分组"),
    ShowRoyalty: bool = Query(False, description="是否只显示营收分润"),
    ShowCompactCount: bool = Query(False, description="是否显示合同数量"),
    JustServerpart: bool = Query(False, description="是否只显示服务区"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取区域服务区树形结构"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        codes = ServerpartCodes or serverpartcodes
        result = service.get_serverpart_tree(
            db, ProvinceCode, SPRegionType_ID, ServerpartType,
            StatisticsType, ServerpartIds, codes,
            ShowSPRegion, ShowRoyalty, ShowCompactCount, JustServerpart
        )
        # 原 C# 返回 JsonMsg<JsonList<CommonTypeTreeModel>> — 嵌套结构
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetServerpartTree 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 5. GetSPRegionShopTree - 区域服务区门店树
#    路由: BaseInfo/GetSPRegionShopTree
#    方法: GET
# =====================================
@router.get("/BaseInfo/GetSPRegionShopTree")
async def get_sp_region_shop_tree(
    request: Request,
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query(None, description="服务区内码"),
    ServerpartCodes: Optional[str] = Query(None, description="服务区编码集合"),
    ServerpartShopId: Optional[str] = Query(None, description="门店内码集合"),
    BusinessState: Optional[str] = Query(None, description="经营状态"),
    BusinessType: Optional[str] = Query(None, description="经营模式"),
    ShowState: bool = Query(False, description="是否显示经营状态"),
    ShowShortName: bool = Query(False, description="是否按门店简称显示"),
    SortStr: Optional[str] = Query(None, description="门店排序规则"),
    ShowRoyalty: bool = Query(False, description="是否只显示营收分润"),
    ShowUnpaidExpense: bool = Query(False, description="是否显示未缴付费用"),
    ShowInSale: bool = Query(False, description="是否只显示进销存门店"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取区域服务区门店树"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        province = ProvinceCode
        if not province and provincecode:
            try:
                province = int(provincecode)
            except Exception:
                pass
        codes = ServerpartCodes or serverpartcodes

        result = service.get_sp_region_shop_tree(
            db, province, ServerpartId, codes,
            ServerpartShopId, BusinessState, BusinessType,
            ShowState, ShowShortName, ShowInSale, SortStr,
            ShowRoyalty, ShowUnpaidExpense
        )
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetSPRegionShopTree 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 6. GetServerpartShopDDL - 门店下拉框
#    路由: BaseInfo/GetServerpartShopDDL
#    方法: GET
# =====================================
@router.get("/BaseInfo/GetServerpartShopDDL")
async def get_serverpart_shop_ddl(
    request: Request,
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query(None, description="服务区内码集合"),
    ServerpartCodes: Optional[str] = Query(None, description="服务区编码集合"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店下拉框数据"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        province = ProvinceCode
        if not province and provincecode:
            try:
                province = int(provincecode)
            except Exception:
                pass
        codes = ServerpartCodes or serverpartcodes
        sp_id = ServerpartId

        result = service.get_serverpart_shop_ddl(db, province, sp_id, codes)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetServerpartShopDDL 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 7. GetServerpartShopTree - 服务区门店树
#    路由: BaseInfo/GetServerpartShopTree
#    方法: GET
# =====================================
@router.get("/BaseInfo/GetServerpartShopTree")
async def get_serverpart_shop_tree(
    request: Request,
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query(None, description="服务区内码"),
    ServerpartCodes: Optional[str] = Query(None, description="服务区编码集合"),
    ServerpartShopId: Optional[str] = Query(None, description="门店内码集合"),
    BusinessState: Optional[str] = Query(None, description="经营状态"),
    BusinessType: Optional[str] = Query(None, description="经营模式"),
    ShowState: bool = Query(False, description="是否显示经营状态"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    serverpartcodes: Optional[str] = Header(None, alias="ServerpartCodes"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区门店树（二级结构，无区域层）"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        province = ProvinceCode
        if not province and provincecode:
            try:
                province = int(provincecode)
            except Exception:
                pass
        codes = ServerpartCodes or serverpartcodes

        result = service.get_serverpart_shop_tree(
            db, province, ServerpartId, codes,
            ServerpartShopId, BusinessState, BusinessType, ShowState
        )
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetServerpartShopTree 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 8. GetNestingOwnerUnitList - 业主单位嵌套列表
#    路由: BaseInfo/GetNestingOwnerUnitList
#    方法: GET
# =====================================
@router.get("/BaseInfo/GetNestingOwnerUnitList")
async def get_nesting_ownerunit_list(
    OwnerUnitPid: int = Query(-1, description="上级内码，-1为全部"),
    ShowStatus: bool = Query(False, description="是否只显示有效"),
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    OwnerUnitNature: Optional[str] = Query(None, description="业主性质"),
    OwnerUnitName: Optional[str] = Query(None, description="业主名称（模糊）"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业主单位嵌套列表"""
    try:
        result = service.get_nesting_ownerunit_list(
            db, OwnerUnitPid, ShowStatus, ProvinceCode,
            OwnerUnitNature, OwnerUnitName
        )
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetNestingOwnerUnitList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 9. BindingOwnerUnitDDL - 业主单位下拉框
#    路由: BaseInfo/BindingOwnerUnitDDL
#    方法: GET
# =====================================
@router.get("/BaseInfo/BindingOwnerUnitDDL")
async def binding_ownerunit_ddl(
    request: Request,
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    DataType: int = Query(0, description="0=返回编码, 1=返回内码"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业主单位下拉框"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        province = ProvinceCode
        if not province and provincecode:
            try:
                province = int(provincecode)
            except Exception:
                pass
        result = service.binding_ownerunit_ddl(db, province, DataType)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"BindingOwnerUnitDDL 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 10. BindingOwnerUnitTree - 业主单位树
#     路由: BaseInfo/BindingOwnerUnitTree
#     方法: GET
# =====================================
@router.get("/BaseInfo/BindingOwnerUnitTree")
async def binding_ownerunit_tree(
    DataType: int = Query(0, description="0=返回编码, 1=返回内码"),
    OwnerUnitPid: int = Query(-1, description="上级内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取业主单位树"""
    try:
        # 原 C# Controller 固定传入 OwnerUnitNature=1000
        result = service.binding_ownerunit_tree(db, 1000, OwnerUnitPid, DataType)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"BindingOwnerUnitTree 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 11. BindingMerchantTree - 经营商户树
#     路由: BaseInfo/BindingMerchantTree
#     方法: GET
# =====================================
@router.get("/BaseInfo/BindingMerchantTree")
async def binding_merchant_tree(
    MerchantPid: int = Query(-1, description="上级内码"),
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    provincecode: Optional[str] = Header(None, alias="ProvinceCode"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营商户树"""
    try:
        province = ProvinceCode
        if not province and provincecode:
            try:
                province = int(provincecode)
            except Exception:
                pass
        # 原 C# Controller: BindingOwnerUnitTree(2000, MerchantPid, 1, ProvinceCode)
        result = service.binding_ownerunit_tree(db, 2000, MerchantPid, 1, province)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"BindingMerchantTree 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 12. GetBusinessBrandList - 门店经营品牌列表
#     路由: BaseInfo/GetBusinessBrandList
#     方法: GET
# =====================================
@router.get("/BaseInfo/GetBusinessBrandList")
async def get_business_brand_list(
    ServerpartShopIds: str = Query(..., description="门店内码集合"),
    ShowWholePower: bool = Query(False, description="是否显示全局权限"),
    serverpartshopids: Optional[str] = Header(None, alias="ServerpartShopIds"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取门店经营品牌列表"""
    try:
        # 原 C# Controller L3594-3596: 非全局权限时从 Header 读取
        shop_ids = ServerpartShopIds
        if not ShowWholePower and serverpartshopids:
            shop_ids = serverpartshopids

        if not shop_ids or not shop_ids.strip():
            return {"Result_Code": 101, "Result_Desc": "查询失败，请传入门店内码参数！"}

        result = service.get_business_brand_list(db, shop_ids)
        # 原 C# 返回 JsonMsg<JsonList<BRANDModel>>: 嵌套结构
        # PageIndex=1, PageSize=result.Count, TotalCount=result.Count
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": len(result),
                "TotalCount": len(result),
                "List": result
            }
        }
    except Exception as e:
        logger.error(f"GetBusinessBrandList 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}



# =====================================
# 13. ModifyShopState - 变更门店经营状态
#     路由: BaseInfo/ModifyShopState
#     方法: POST
# =====================================
@router.post("/BaseInfo/ModifyShopState")
async def modify_shop_state(
    ShopModifyList: list = Body([], description="变更的门店列表"),
    db: DatabaseHelper = Depends(get_db)
):
    """批量变更门店经营状态"""
    try:
        result = service.modify_shop_state(db, ShopModifyList)
        if result:
            return {"Result_Code": 100, "Result_Desc": "变更成功", "Result_Data": None}
        else:
            return {"Result_Code": 200, "Result_Desc": "变更失败，数据更新失败！", "Result_Data": None}
    except Exception as e:
        logger.error(f"ModifyShopState 变更失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"变更失败{str(e)}", "Result_Data": None}


# =====================================
# 14. GetShopReceivables - 获取经营门店关联合同项目信息
#     路由: BaseInfo/GetShopReceivables
#     方法: GET
# =====================================
@router.get("/BaseInfo/GetShopReceivables")
async def get_shop_receivables(
    ServerpartId: str = Query(..., description="服务区内码"),
    BusinessState: str = Query("", description="门店经营状态"),
    BusinessType: str = Query("", description="门店经营模式"),
    AbnormalShop: bool = Query(False, description="无合同在营门店"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营门店关联合同项目信息"""
    try:
        result_list, other_data = service.get_shop_receivables(
            db, ServerpartId, BusinessState, BusinessType, AbnormalShop
        )
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": len(result_list),
                "TotalCount": len(result_list),
                "List": result_list,
                "OtherData": other_data
            }
        }
    except Exception as e:
        logger.error(f"GetShopReceivables 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 15. GetServerpartUDTypeTree - 服务区自定义类别树
#     路由: BaseInfo/GetServerpartUDTypeTree
#     方法: GET
# =====================================
@router.get("/BaseInfo/GetServerpartUDTypeTree")
async def get_serverpart_ud_type_tree(
    request: Request,
    ServerpartId: str = Query(..., description="服务区内码集合"),
    ShopTrade: Optional[str] = Query(None, description="商品业态"),
    UserDefinedTypeState: Optional[int] = Query(1, description="有效状态"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区自定义类别树"""
    try:
        # 原 C# : ProvinceCode = GetIntHeader("ProvinceCode", ProvinceCode)
        ProvinceCode = get_int_header(request, "ProvinceCode", ProvinceCode)

        tree_list = service.get_serverpart_ud_type_tree(
            db, ServerpartId, ShopTrade or "", UserDefinedTypeState
        )
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": {
                "PageIndex": 1,
                "PageSize": 10,
                "TotalCount": len(tree_list),
                "List": tree_list,
            }
        }
    except Exception as e:
        logger.error(f"GetServerpartUDTypeTree 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 15. GetSERVERPARTDetail - 服务区详情
#     路由: BaseInfo/GetSERVERPARTDetail
#     方法: GET
# =====================================
@router.get("/BaseInfo/GetSERVERPARTDetail")
async def get_serverpart_detail(
    SERVERPARTId: Optional[int] = Query(None, description="服务区内码"),
    FieldEnumId: Optional[int] = Query(None, description="枚举内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取服务区详情"""
    try:
        result = service.get_serverpart_detail(db, SERVERPARTId, FieldEnumId)
        return {
            "Result_Code": 100,
            "Result_Desc": "查询成功",
            "Result_Data": result
        }
    except Exception as e:
        logger.error(f"GetSERVERPARTDetail 查询失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"查询失败{str(e)}"}


# =====================================
# 16. SynchroSERVERPART - 同步服务区
#     路由: BaseInfo/SynchroSERVERPART
#     方法: POST
#     入参: SERVERPARTModel (body JSON)
#     原 C# L3934-3964, Helper L905-1013
# =====================================
@router.post("/BaseInfo/SynchroSERVERPART")
async def synchro_serverpart(
    serverpartModel: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步服务区信息（新增/更新）"""
    try:
        from services.base_info import serverpart_service
        success, updated_model = serverpart_service.synchro_serverpart(db, serverpartModel)

        if success:
            return {"Result_Code": 100, "Result_Desc": "同步成功", "Result_Data": updated_model}
        else:
            return {"Result_Code": 200, "Result_Desc": "更新失败，数据不存在！"}
    except Exception as e:
        logger.error(f"SynchroSERVERPART 同步失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"同步失败{str(e)}"}


# =====================================
# 17. SolidServerpartWeather - 存储天气
#     路由: BaseInfo/SolidServerpartWeather
#     方法: POST
#     入参: List<CommonModel> (body JSON)
#     原 C# L3973-4003, Helper L1181-1329
# =====================================
@router.post("/BaseInfo/SolidServerpartWeather")
async def solid_serverpart_weather(
    ServerpartList: list,
    db: DatabaseHelper = Depends(get_db)
):
    """存储服务区天气情况"""
    try:
        # 提取 value 列表，逗号拼接为 ServerpartId 字符串
        serverpart_ids = ",".join([str(item.get("value", "")) for item in ServerpartList if item.get("value")])
        success = service.solid_serverpart_weather(db, serverpart_ids)

        if success:
            return {"Result_Code": 100, "Result_Desc": "同步成功"}
        else:
            return {"Result_Code": 200, "Result_Desc": "更新失败，数据不存在！"}
    except Exception as e:
        logger.error(f"SolidServerpartWeather 同步失败: {e}")
        return {"Result_Code": 999, "Result_Desc": f"同步失败{str(e)}"}


# =====================================
# 18. ModifyShopBusinessState - 批量变更经营状态
#     ⚠️ 跳过：涉及 AES 加密解密（CommonModel.value），后续统一处理
#     路由: BaseInfo/ModifyShopBusinessState
#     方法: POST
#     原 C# L4012-4053
# =====================================
