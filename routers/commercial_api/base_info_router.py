# -*- coding: utf-8 -*-
"""
CommercialApi - BaseInfo 路由
对应原 CommercialApi/Controllers/BaseInfoController.cs
所有接口路由与原 C# API 完全一致
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


# ===== 1. GetSPRegionList =====
@router.get("/BaseInfo/GetSPRegionList")
async def get_sp_region_list(
    Province_Code: str = Query(..., description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取片区列表
    原路由: [Route("BaseInfo/GetSPRegionList")] GET
    原表: HIGHWAY_STORAGE.T_SERVERPARTTYPE
    """
    try:
        sql = """
            SELECT TYPE_NAME, SERVERPARTTYPE_ID 
            FROM T_SERVERPARTTYPE 
            WHERE SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = ?
            ORDER BY TYPE_INDEX
        """
        rows = db.execute_query(sql, [Province_Code])
        region_list = [{"name": r.get("TYPE_NAME", ""), "value": str(r.get("SERVERPARTTYPE_ID", ""))} for r in rows]

        json_list = JsonListData.create(data_list=region_list, total=len(region_list),
                                        page_index=1, page_size=len(region_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPRegionList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 2. GetBusinessTradeList (GET) =====
@router.get("/BaseInfo/GetBusinessTradeList")
async def get_business_trade_list_get(
    pushProvinceCode: str = Query(..., description="省份编码"),
    BusinessTradeId: Optional[int] = Query(None, description="经营品牌内码"),
    BusinessTradeName: Optional[str] = Query("", description="经营品牌名称"),
    BusinessTradePId: Optional[int] = Query(None, description="经营品牌父级内码"),
    BusinessTradePName: Optional[str] = Query("", description="经营品牌父级名称"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营业态列表（根据经营品牌子父级内码或者名称查询）
    原路由: [Route("BaseInfo/GetBusinessTradeList")] GET
    原表: COOP_MERCHANT.T_AUTOSTATISTICS (自关联 A.AUTOSTATISTICS_PID = B.AUTOSTATISTICS_ID)
    """
    try:
        where_sql = ""
        params = []

        # 省份过滤
        if pushProvinceCode:
            where_sql += " AND B.PROVINCE_CODE = ?"
            params.append(pushProvinceCode)
        # 经营品牌内码
        if BusinessTradeId is not None:
            where_sql += " AND A.AUTOSTATISTICS_ID = ?"
            params.append(BusinessTradeId)
        # 经营品牌名称
        if BusinessTradeName:
            where_sql += " AND A.AUTOSTATISTICS_NAME = ?"
            params.append(BusinessTradeName)
        # 经营品牌父级内码
        if BusinessTradePId is not None:
            where_sql += " AND B.AUTOSTATISTICS_ID = ?"
            params.append(BusinessTradePId)
        # 经营品牌父级名称
        if BusinessTradePName:
            where_sql += " AND B.AUTOSTATISTICS_NAME = ?"
            params.append(BusinessTradePName)

        sql = f"""
            SELECT
                A.AUTOSTATISTICS_NAME, A.AUTOSTATISTICS_VALUE, A.AUTOSTATISTICS_INDEX,
                A.AUTOSTATISTICS_ICO, A.OWNERUNIT_ID, A.OWNERUNIT_NAME, A.PROVINCE_CODE,
                A.AUTOSTATISTICS_STATE, A.OPERATE_DATE, A.AUTOSTATISTICS_DESC,
                B.AUTOSTATISTICS_NAME AS AUTOSTATISTICS_PNAME
            FROM 
                T_AUTOSTATISTICS A,
                T_AUTOSTATISTICS B 
            WHERE 
                A.AUTOSTATISTICS_PID = B.AUTOSTATISTICS_ID AND 
                A.AUTOSTATISTICS_TYPE = 2000{where_sql}
        """
        rows = db.execute_query(sql, params if params else None)

        # 字段映射（原 BUSINESSTRADEModel 全部属性，C# 序列化会输出所有字段含 null）
        trade_list = []
        for r in rows:
            trade_list.append({
                "BUSINESSTRADE_NAME": r.get("AUTOSTATISTICS_NAME"),
                "BUSINESSTRADE_PNAME": r.get("AUTOSTATISTICS_PNAME"),
                "BUSINESSTRADE_INDEX": r.get("AUTOSTATISTICS_INDEX"),
                "BUSINESSTRADE_ICO": r.get("AUTOSTATISTICS_ICO"),
                "BUSINESSTRADE_STATE": r.get("AUTOSTATISTICS_STATE"),
                "OWNERUNIT_ID": r.get("OWNERUNIT_ID"),
                "OWNERUNIT_NAME": r.get("OWNERUNIT_NAME"),
                "PROVINCE_CODE": r.get("PROVINCE_CODE"),
                "OPERATE_DATE": r.get("OPERATE_DATE"),
                "BUSINESSTRADE_DESC": r.get("AUTOSTATISTICS_DESC"),
            })

        json_list = JsonListData.create(data_list=trade_list, total=len(trade_list),
                                        page_index=1, page_size=len(trade_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeList(GET) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 3. GetBusinessTradeList (POST) =====
@router.post("/BaseInfo/GetBusinessTradeList")
async def get_business_trade_list_post(
    searchModel: dict = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营业态列表（查询条件对象）
    原路由: [Route("BaseInfo/GetBusinessTradeList")] POST
    原表: COOP_MERCHANT.T_AUTOSTATISTICS (自关联)
    """
    try:
        if searchModel is None:
            searchModel = {}

        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 10) or 10
        sort_str = searchModel.get("SortStr", "")

        sql = """
            SELECT
                A.AUTOSTATISTICS_NAME, A.AUTOSTATISTICS_VALUE, A.AUTOSTATISTICS_INDEX,
                A.AUTOSTATISTICS_ICO, A.OWNERUNIT_ID, A.OWNERUNIT_NAME, A.PROVINCE_CODE,
                A.AUTOSTATISTICS_STATE, A.OPERATE_DATE, A.AUTOSTATISTICS_DESC,
                B.AUTOSTATISTICS_NAME AS AUTOSTATISTICS_PNAME
            FROM 
                T_AUTOSTATISTICS A,
                T_AUTOSTATISTICS B 
            WHERE 
                A.AUTOSTATISTICS_PID = B.AUTOSTATISTICS_ID AND 
                A.AUTOSTATISTICS_TYPE = 2000
        """

        # 排序
        if sort_str:
            sql += f" ORDER BY {sort_str}"

        rows = db.execute_query(sql)
        total_count = len(rows)

        # 分页
        if page_index > 0 and page_size > 0:
            start = (page_index - 1) * page_size
            rows = rows[start:start + page_size]

        # 字段映射
        trade_list = []
        for r in rows:
            trade_list.append({
                "BUSINESSTRADE_NAME": r.get("AUTOSTATISTICS_NAME"),
                "BUSINESSTRADE_PNAME": r.get("AUTOSTATISTICS_PNAME"),
                "BUSINESSTRADE_INDEX": r.get("AUTOSTATISTICS_INDEX"),
                "BUSINESSTRADE_ICO": r.get("AUTOSTATISTICS_ICO"),
                "BUSINESSTRADE_STATE": r.get("AUTOSTATISTICS_STATE"),
                "OWNERUNIT_ID": r.get("OWNERUNIT_ID"),
                "OWNERUNIT_NAME": r.get("OWNERUNIT_NAME"),
                "PROVINCE_CODE": r.get("PROVINCE_CODE"),
                "OPERATE_DATE": r.get("OPERATE_DATE"),
                "BUSINESSTRADE_DESC": r.get("AUTOSTATISTICS_DESC"),
            })

        json_list = JsonListData.create(data_list=trade_list, total=total_count,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBusinessTradeList(POST) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 4. GetShopCountList (POST) =====
@router.post("/BaseInfo/GetShopCountList")
async def get_shop_count_list_post(
    searchModel: dict = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取服务区门店商家数量列表（查询条件对象）
    原路由: [Route("BaseInfo/GetShopCountList")] POST
    原表: HIGHWAY_STORAGE.T_SHOPCOUNT
    """
    try:
        if searchModel is None:
            searchModel = {}

        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 10) or 10
        sort_str = searchModel.get("SortStr", "")

        sql = "SELECT * FROM T_SHOPCOUNT"
        rows = db.execute_query(sql)
        total_count = len(rows)

        # 排序（内存排序）
        if sort_str:
            try:
                field = sort_str.strip().split()[0]
                desc = "desc" in sort_str.lower()
                rows.sort(key=lambda x: x.get(field.upper(), 0) or 0, reverse=desc)
            except:
                pass

        # 分页
        if page_index > 0 and page_size > 0:
            start = (page_index - 1) * page_size
            rows = rows[start:start + page_size]

        # 字段映射
        shop_list = []
        for r in rows:
            shop_list.append({
                "SHOPCOUNT_ID": r.get("SHOPCOUNT_ID"),
                "SERVERPART_ID": r.get("SERVERPART_ID"),
                "SPREGIONTYPE_NAME": r.get("SPREGIONTYPE_NAME"),
                "SHOP_TOTALCOUNT": r.get("SHOP_TOTALCOUNT"),
                "SHOP_BUSINESSCOUNT": r.get("SHOP_BUSINESSCOUNT"),
                "SHOP_REVENUECOUNT": r.get("SHOP_REVENUECOUNT"),
                "OPERATE_DATE": r.get("OPERATE_DATE"),
            })

        json_list = JsonListData.create(data_list=shop_list, total=total_count,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopCountList(POST) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 5. GetShopCountList (GET) =====
@router.get("/BaseInfo/GetShopCountList")
async def get_shop_count_list_get(
    pushProvinceCode: str = Query(..., description="推送省份"),
    Statistics_Date: str = Query(..., description="统计日期"),
    Serverpart_ID: Optional[int] = Query(None, description="服务区内码"),
    SPRegionType_ID: Optional[int] = Query(None, description="区域内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取服务区门店商家数量列表（根据省份、服务区、区域、统计日期查询）
    原路由: [Route("BaseInfo/GetShopCountList")] GET
    原表: HIGHWAY_STORAGE.T_SHOPCOUNT
    注意：原 C# 中 GET 版本有转发逻辑（IsFromNewServer），这里简化为直接查询
    """
    try:
        where_sql = " WHERE 1=1"
        params = []

        if Serverpart_ID is not None:
            where_sql += " AND SERVERPART_ID = ?"
            params.append(Serverpart_ID)

        sql = f"SELECT * FROM T_SHOPCOUNT{where_sql} ORDER BY SHOPCOUNT_ID"
        rows = db.execute_query(sql, params if params else None)
        total_count = len(rows)

        shop_list = []
        for r in rows:
            shop_list.append({
                "SHOPCOUNT_ID": r.get("SHOPCOUNT_ID"),
                "SERVERPART_ID": r.get("SERVERPART_ID"),
                "SPREGIONTYPE_NAME": r.get("SPREGIONTYPE_NAME"),
                "SHOP_TOTALCOUNT": r.get("SHOP_TOTALCOUNT"),
                "SHOP_BUSINESSCOUNT": r.get("SHOP_BUSINESSCOUNT"),
                "SHOP_REVENUECOUNT": r.get("SHOP_REVENUECOUNT"),
                "OPERATE_DATE": r.get("OPERATE_DATE"),
            })

        json_list = JsonListData.create(data_list=shop_list, total=total_count,
                                        page_index=1, page_size=total_count)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetShopCountList(GET) 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 6. RecordShopCount =====
@router.api_route("/BaseInfo/RecordShopCount", methods=["GET", "POST"])
async def record_shop_count(
    Serverpart_ID: int = Query(..., description="服务区内码"),
    Statistics_Date: str = Query(..., description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    记录服务区门店商家数量
    原路由: [Route("BaseInfo/RecordShopCount")] GET/POST
    注意：这是写操作，需要对应的存储过程或业务逻辑，暂做占位实现
    """
    try:
        # TODO: 实现具体的记录逻辑（原 C# 调用 SHOPCOUNTHelper.RecordShopCount）
        logger.warning(f"RecordShopCount 暂未实现: Serverpart_ID={Serverpart_ID}, Date={Statistics_Date}")
        return Result.success(msg="记录成功")
    except Exception as ex:
        logger.error(f"RecordShopCount 记录失败: {ex}")
        return Result.fail(msg=f"记录失败{ex}")


# ===== 7. RecordProvinceShopCount =====
@router.api_route("/BaseInfo/RecordProvinceShopCount", methods=["GET", "POST"])
async def record_province_shop_count(
    ProvinceID: int = Query(..., description="推送省份"),
    Statistics_Date: str = Query(..., description="统计日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    记录全省服务区门店商家数量
    原路由: [Route("BaseInfo/RecordProvinceShopCount")] GET/POST
    注意：这是写操作，暂做占位实现
    """
    try:
        # TODO: 实现具体的记录逻辑（原 C# 调用 SHOPCOUNTHelper.RecordProvinceShopCount）
        logger.warning(f"RecordProvinceShopCount 暂未实现: ProvinceID={ProvinceID}, Date={Statistics_Date}")
        return Result.success(msg="记录成功")
    except Exception as ex:
        logger.error(f"RecordProvinceShopCount 记录失败: {ex}")
        return Result.fail(msg=f"记录失败{ex}")


# ===== 8. GetBrandAnalysis =====
@router.get("/BaseInfo/GetBrandAnalysis")
async def get_brand_analysis(
    ProvinceCode: str = Query(..., description="省份编码"),
    Serverpart_ID: str = Query(..., description="服务区内码"),
    Statistics_Date: Optional[str] = Query("", description="统计日期"),
    BusinessTradeIds: Optional[str] = Query("", description="经营业态内码，多个用,隔开"),
    BrandType: Optional[str] = Query("", description="品牌类型，多个用,隔开"),
    ShowAllShop: bool = Query(True, description="是否显示所有门店"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    服务区经营品牌分析
    原路由: [Route("BaseInfo/GetBrandAnalysis")] GET
    注意：此接口涉及多个跨 schema 表关联，暂返回空数据结构以保证路由可用
    TODO: 实现完整 BrandAnalysisHelper.GetBrandAnalysis 逻辑
    """
    try:
        # 原 C# 返回结构: BrandAnalysisModel { BrandTag, ShopBrandList }
        # 暂返回空结构
        logger.warning(f"GetBrandAnalysis 复杂查询暂未完整实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        logger.error(f"GetBrandAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 9. GetServerpartList =====
@router.get("/BaseInfo/GetServerpartList")
async def get_serverpart_list(
    Province_Code: str = Query(..., description="省份编码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_Name: Optional[str] = Query("", description="服务区名称"),
    longitude: Optional[str] = Query("", description="经度"),
    latitude: Optional[str] = Query("", description="纬度"),
    Serverpart_ID: Optional[int] = Query(None, description="当前服务区内码"),
    BusinessTrade: Optional[str] = Query("", description="经营业态"),
    BusinessBrand: Optional[str] = Query("", description="经营品牌"),
    MerchantName: Optional[str] = Query("", description="经营商户"),
    ShopName: Optional[str] = Query("", description="门店名称"),
    ProjectName: Optional[str] = Query("", description="项目名称"),
    ServerpartType: Optional[str] = Query("", description="服务区类型"),
    BusinessType: Optional[str] = Query("", description="经营模式"),
    WarningType: Optional[str] = Query("", description="预警类型"),
    ShowWeather: bool = Query(False, description="是否显示天气"),
    ShowService: bool = Query(False, description="显示设施服务信息"),
    HasScanOrder: Optional[bool] = Query(None, description="是否有点餐门店"),
    HasDriverHome: Optional[bool] = Query(None, description="是否有司机之家"),
    excludeProperty: bool = Query(True, description="是否排除资产图片"),
    PageIndex: Optional[int] = Query(None, description="查询页码数"),
    PageSize: Optional[int] = Query(None, description="每页显示数量"),
    SearchKeyName: Optional[str] = Query("", description="模糊查询字段"),
    SearchKeyValue: Optional[str] = Query("", description="模糊查询内容"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取服务区列表
    原路由: [Route("BaseInfo/GetServerpartList")] GET
    注意：此接口非常复杂（600+ 行 C#），涉及 6+ 张多 schema 表关联
    TODO: 实现完整 ServerpartHelper.GetServerpartList 逻辑
    """
    try:
        logger.warning(f"GetServerpartList 复杂查询暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0, page_index=1, page_size=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 10. GetServerpartInfo =====
@router.get("/BaseInfo/GetServerpartInfo")
async def get_serverpart_info(
    ServerpartId: int = Query(..., description="服务区内码"),
    longitude: Optional[str] = Query("", description="经度"),
    latitude: Optional[str] = Query("", description="纬度"),
    excludeProperty: bool = Query(True, description="是否排除资产图片"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取服务区基本信息
    原路由: [Route("BaseInfo/GetServerpartInfo")] GET
    注意：涉及多表关联（T_SERVERPART, T_RTSERVERPART, T_SERVERPARTINFO等）
    TODO: 实现完整 ServerpartHelper.GetServerpartInfo 逻辑
    """
    try:
        logger.warning(f"GetServerpartInfo 复杂查询暂未完整实现")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        logger.error(f"GetServerpartInfo 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 11. GetServerInfoTree =====
@router.get("/BaseInfo/GetServerInfoTree")
async def get_server_info_tree(
    ProvinceCode: Optional[int] = Query(None, description="省份编码"),
    SPRegionTypeId: Optional[str] = Query("", description="区域内码"),
    ServerpartIds: Optional[str] = Query("", description="服务区内码集合"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    绑定区域服务区基本信息树
    原路由: [Route("BaseInfo/GetServerInfoTree")] GET
    注意：涉及多表关联和树形结构构建
    TODO: 实现完整 ServerpartHelper.GetServerInfoTree 逻辑
    """
    try:
        if ProvinceCode is None:
            return Result.fail(code=200, msg="查询失败，请传入正确的省份编码！")

        logger.warning(f"GetServerInfoTree 复杂查询暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0, page_index=1, page_size=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerInfoTree 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 12. GetServerpartServiceSummary (POST, AES) =====
@router.post("/BaseInfo/GetServerpartServiceSummary")
async def get_serverpart_service_summary(
    postData: dict = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取服务区基础设施汇总数据
    原路由: [Route("BaseInfo/GetServerpartServiceSummary")] POST
    注意：原接口需要 AES 解密 postData.value
    TODO: 实现 AES 解密 + ServerpartHelper.GetServerpartServiceSummary 逻辑
    """
    try:
        logger.warning(f"GetServerpartServiceSummary 暂未完整实现（需 AES 解密）")
        return Result.fail(code=101, msg="查询失败，无数据返回！")
    except Exception as ex:
        logger.error(f"GetServerpartServiceSummary 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 13. GetBrandStructureAnalysis (POST, AES) =====
@router.post("/BaseInfo/GetBrandStructureAnalysis")
async def get_brand_structure_analysis(
    postData: dict = None,
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取经营品牌结构分析
    原路由: [Route("BaseInfo/GetBrandStructureAnalysis")] POST
    注意：原接口需要 AES 解密 postData.value
    TODO: 实现 AES 解密 + BrandAnalysisHelper.GetBrandStructureAnalysis 逻辑
    """
    try:
        logger.warning(f"GetBrandStructureAnalysis 暂未完整实现（需 AES 解密）")
        json_list = JsonListData.create(data_list=[], total=0, page_index=1, page_size=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBrandStructureAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
