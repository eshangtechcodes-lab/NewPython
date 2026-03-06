# -*- coding: utf-8 -*-
"""
CommercialApi - BaseInfo 路由
对应原 CommercialApi/Controllers/BaseInfoController.cs
所有接口路由与原 C# API 完全一致
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


# ===== 1. GetSPRegionList =====
@router.get("/BaseInfo/GetSPRegionList")
async def get_sp_region_list(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
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
    pushProvinceCode: Optional[str] = Query(None, description="省份编码"),
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



# ===== 8. GetBrandAnalysis =====
@router.get("/BaseInfo/GetBrandAnalysis")
async def get_brand_analysis(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    Serverpart_ID: Optional[str] = Query(None, description="服务区内码"),
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
        _shop_brand = {
            "Brand_Id": None, "Brand_Name": None, "BrandType_Name": None, "Brand_ICO": None,
            "ServerpartShop_Id": None, "Bussiness_Time": None,
            "CurRevenue": None, "Revenue_Amount": None,
            "BrandTrade": None, "BrandTradeName": None, "BrandTradeType": None,
            "BrandProject": None, "BrandProjectName": None,
            "ShopEndaccountList": None,
        }
        data = {"BrandTag": "", "ShopBrandList": [_shop_brand]}
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBrandAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 9. GetServerpartList =====
@router.get("/BaseInfo/GetServerpartList")
async def get_serverpart_list(
    Province_Code: Optional[str] = Query(None, description="省份编码"),
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
        # 动态构建 WHERE 条件（参照 C# ServerpartHelper.GetServerpartList）
        # 注：达梦中无 STATISTIC_TYPE 字段，只有 STATISTICS_TYPE
        conditions = ["A.STATISTICS_TYPE = 1000",
                       "A.SERVERPART_CODE NOT IN ('340001','530590')"]
        params = {}

        # 注: Serverpart_ID 是"当前服务区"（用于标记距离排序），不是 WHERE 过滤条件
        # C# 中用 ServerpartId（另一个参数）做 WHERE 过滤
        if SPRegionType_ID:
            conditions.append(f"A.SPREGIONTYPE_ID IN ({SPRegionType_ID})")
        elif Province_Code:
            # C# 通过 DictionaryHelper.GetFieldEnum("DIVISION_CODE", ProvinceCode) 将编码转内码
            pcode_rows = db.execute_query(
                "SELECT FIELDENUM_ID FROM T_FIELDENUM WHERE FIELDENUM_VALUE = :pc AND ROWNUM = 1",
                {"pc": Province_Code})
            if pcode_rows:
                conditions.append("A.PROVINCE_CODE = :pcode")
                params["pcode"] = pcode_rows[0]["FIELDENUM_ID"]
        if ServerpartType:
            conditions.append(f"A.SERVERPART_TYPE IN ({ServerpartType})")
        if Serverpart_Name:
            conditions.append("A.SERVERPART_NAME LIKE :sp_name")
            params["sp_name"] = f"%{Serverpart_Name}%"

        where_sql = " AND ".join(conditions)
        sql = f"""SELECT 
                A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                A.PROVINCE_CODE, A.SERVERPART_TYPE, A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME,
                A.SPREGIONTYPE_INDEX, A.STATISTICS_TYPE, A.OWNERUNIT_ID, A.OWNERUNIT_NAME,
                A.OPERATE_DATE, A.SERVERPART_X, A.SERVERPART_Y, A.SERVERPART_TEL,
                SUM(NVL(C.HASMOTHER,0)) AS HASMOTHER, SUM(NVL(C.HASPILOTLOUNGE,0)) AS HASPILOTLOUNGE,
                SUM(NVL(C.LIVESTOCKPACKING,0)) AS HASCHARGE, SUM(NVL(C.POINTCONTROLCOUNT,0)) AS HASGUESTROOM
            FROM T_SERVERPART A
            LEFT JOIN T_SERVERPARTINFO C ON A.SERVERPART_ID = C.SERVERPART_ID
            WHERE {where_sql}
            GROUP BY A.SERVERPART_ID, A.SERVERPART_NAME, A.SERVERPART_INDEX, A.SERVERPART_CODE,
                A.PROVINCE_CODE, A.SERVERPART_TYPE, A.SPREGIONTYPE_ID, A.SPREGIONTYPE_NAME,
                A.SPREGIONTYPE_INDEX, A.STATISTICS_TYPE, A.OWNERUNIT_ID, A.OWNERUNIT_NAME,
                A.OPERATE_DATE, A.SERVERPART_X, A.SERVERPART_Y, A.SERVERPART_TEL
            ORDER BY A.SERVERPART_INDEX"""

        rows = db.execute_query(sql, params)

        # 分页（C# 中 TotalCount = 分页后列表长度）
        if PageIndex and PageSize:
            start = (PageIndex - 1) * PageSize
            rows = rows[start:start + PageSize]

        # 每行补全C#模型中的额外字段
        for r in rows:
            r.setdefault("ISCUR_SERVERPART", None)
            r.setdefault("ImageLits", None)
            r.setdefault("LoadBearing_Id", None)
            r.setdefault("LoadBearing_State", None)
            r.setdefault("SERVERPART_ADDRESS", None)
            r.setdefault("SERVERPART_DISTANCE", None)
            r.setdefault("STARTDATE", None)
            r.setdefault("RegionInfo", None)
            r.setdefault("tmwWeatherModel", None)
            r.setdefault("weatherModel", None)
            if "ServerpartInfo" not in r:
                r["ServerpartInfo"] = {
                    "SERVERPART_ID": r.get("SERVERPART_ID"),
                    "RTSERVERPART_ID": None, "SERVERPART_ADDRESS": None,
                    "SERVERPART_X": r.get("SERVERPART_X"), "SERVERPART_Y": r.get("SERVERPART_Y"),
                    "SERVERPART_TEL": r.get("SERVERPART_TEL"),
                    "SERVERPART_AREA": None, "SERVERPART_INFO": None, "SERVERPART_TARGET": None,
                    "STARTDATE": None, "CENTERSTAKE_NUM": None, "EXPRESSWAY_NAME": None,
                    "FLOORAREA": None, "BUSINESSAREA": None, "SHAREAREA": None,
                    "BUSINESS_REGION": None, "MANAGERCOMPANY": None, "OWNEDCOMPANY": None,
                    "SELLERCOUNT": None, "TAXPAYER_IDENTIFYCODE": None,
                    "SEWAGEDISPOSAL_TYPE": None, "WATERINTAKE_TYPE": None,
                }

        json_list = JsonListData.create(data_list=rows, total=len(rows),
                                        page_index=PageIndex or 1, page_size=PageSize or len(rows))
        resp = json_list.model_dump()
        resp["OtherData"] = None
        return Result.success(data=resp, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 10. GetServerpartInfo =====
@router.get("/BaseInfo/GetServerpartInfo")
async def get_serverpart_info(
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
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
        if not ServerpartId:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        # 查询服务区基础信息
        sql = "SELECT * FROM T_SERVERPART WHERE SERVERPART_ID = :id"
        rows = db.execute_query(sql, {"id": ServerpartId})
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        sp = rows[0]

        result = {
            "SERVERPART_ID": sp.get("SERVERPART_ID"),
            "SERVERPART_NAME": sp.get("SERVERPART_NAME", ""),
            "SERVERPART_TEL": sp.get("SERVERPART_TEL", ""),
            "SERVERPART_ADDRESS": sp.get("SERVERPART_ADDRESS", ""),
            "SERVERPART_INDEX": sp.get("SERVERPART_INDEX"),
            "PROVINCE_CODE": sp.get("PROVINCE_CODE"),
            "SERVERPART_CODE": sp.get("SERVERPART_CODE", ""),
            "SERVERPART_TYPE": sp.get("SERVERPART_TYPE"),
            "SPREGIONTYPE_ID": sp.get("SPREGIONTYPE_ID"),
            "SPREGIONTYPE_NAME": sp.get("SPREGIONTYPE_NAME", ""),
            "SPREGIONTYPE_INDEX": sp.get("SPREGIONTYPE_INDEX"),
            "STATISTICS_TYPE": str(sp.get("STATISTICS_TYPE", "")),
            "OWNERUNIT_ID": sp.get("OWNERUNIT_ID"),
            "OWNERUNIT_NAME": sp.get("OWNERUNIT_NAME", ""),
            "SERVERPART_X": sp.get("SERVERPART_X"),
            "SERVERPART_Y": sp.get("SERVERPART_Y"),
        }

        # 查询服务区扩展信息 T_RTSERVERPART
        rt_rows = db.execute_query("SELECT * FROM T_RTSERVERPART WHERE SERVERPART_ID = :id", {"id": ServerpartId})
        if rt_rows:
            rt = rt_rows[0]
            result["ServerpartInfo"] = rt
            # 补充经纬度
            if not result["SERVERPART_X"] and rt.get("SERVERPART_X"):
                result["SERVERPART_X"] = rt["SERVERPART_X"]
            if not result["SERVERPART_Y"] and rt.get("SERVERPART_Y"):
                result["SERVERPART_Y"] = rt["SERVERPART_Y"]

        # 查询服务区设施信息 T_SERVERPARTINFO
        info_rows = db.execute_query("SELECT * FROM T_SERVERPARTINFO WHERE SERVERPART_ID = :id", {"id": ServerpartId})
        if info_rows:
            result["HASMOTHER"] = any(float(r.get("HASMOTHER", 0) or 0) > 0 for r in info_rows)
            result["HASPILOTLOUNGE"] = any(float(r.get("HASPILOTLOUNGE", 0) or 0) > 0 for r in info_rows)
            result["HASCHARGE"] = any(float(r.get("LIVESTOCKPACKING", 0) or 0) > 0 for r in info_rows)
            result["HASGUESTROOM"] = any(float(r.get("POINTCONTROLCOUNT", 0) or 0) > 0 for r in info_rows)
            result["RegionInfo"] = info_rows

        # 补全C#模型字段
        result.setdefault("ISCUR_SERVERPART", None)
        result.setdefault("ImageLits", None)
        result.setdefault("LoadBearing_Id", None)
        result.setdefault("LoadBearing_State", None)
        result.setdefault("OPERATE_DATE", None)
        result.setdefault("SERVERPART_DISTANCE", None)
        result.setdefault("STARTDATE", None)
        result.setdefault("tmwWeatherModel", None)
        result.setdefault("weatherModel", None)

        # RegionInfo子项补全字段
        if "RegionInfo" in result and isinstance(result["RegionInfo"], list):
            _ckm = {"data": None, "key": None, "name": None, "value": None}
            for ri in result["RegionInfo"]:
                ri.setdefault("SERVERPART_REGIONNAME", None)
                ri.setdefault("SPRegionTypeId", None)
                ri.setdefault("SPRegionTypeIndex", None)
                ri.setdefault("ServerPartIndex", None)
                ri.setdefault("TreeNodeName", None)
                ri.setdefault("TreeNodePName", None)
                ri.setdefault("ImgList", [_ckm])
        else:
            _ckm = {"data": None, "key": None, "name": None, "value": None}
            result["RegionInfo"] = [{"SERVERPART_REGIONNAME": None, "SPRegionTypeId": None,
                                      "SPRegionTypeIndex": None, "ServerPartIndex": None,
                                      "TreeNodeName": None, "TreeNodePName": None, "ImgList": [_ckm]}]

        return Result.success(data=result, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetServerpartInfo 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 11. GetServerInfoTree =====
@router.get("/BaseInfo/GetServerInfoTree")
async def get_server_info_tree(
    request: Request,
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
        # 从Header获取省份编码和服务区编码（页面权限验证来源）
        if ProvinceCode is None:
            header_pc = request.headers.get("ProvinceCode", "")
            if header_pc:
                try:
                    ProvinceCode = int(header_pc)
                except ValueError:
                    pass
        ServerpartCodes = request.headers.get("ServerpartCodes", "")
        if not ServerpartIds:
            ServerpartIds = ""
        if ProvinceCode is None:
            return Result.fail(code=200, msg="查询失败，请传入正确的省份编码！")

        # 1. 根据 ServerpartCodes 解析出 ServerpartIds
        if ServerpartCodes:
            codes_in = ",".join([f"'{c.strip()}'" for c in ServerpartCodes.split(",") if c.strip()])
            id_rows = db.execute_query(
                f'SELECT LISTAGG(CAST("SERVERPART_ID" AS VARCHAR),\',\') WITHIN GROUP(ORDER BY "SERVERPART_ID") AS IDS FROM "T_SERVERPART" WHERE "SERVERPART_CODE" IN ({codes_in})')
            if id_rows and id_rows[0].get("IDS"):
                code_ids = id_rows[0]["IDS"]
                if ServerpartIds:
                    # 取交集
                    set1 = set(code_ids.split(","))
                    set2 = set(ServerpartIds.split(","))
                    ServerpartIds = ",".join(set1 & set2)
                else:
                    ServerpartIds = code_ids
        else:
            # 没有 ServerpartCodes 权限直接返回空
            json_list = JsonListData.create(data_list=[], total=0, page_index=1, page_size=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 2. 构建服务区查询条件
        where_parts = ["1=1"]
        if SPRegionTypeId:
            where_parts.append(f'"SPREGIONTYPE_ID" IN ({SPRegionTypeId})')
        if ServerpartIds:
            where_parts.append(f'"SERVERPART_ID" IN ({ServerpartIds})')
        where_sql = " AND ".join(where_parts)

        # 3. 查询服务区基本信息
        sp_rows = db.execute_query(f'SELECT * FROM "T_SERVERPART" WHERE {where_sql}')
        if not sp_rows:
            json_list = JsonListData.create(data_list=[], total=0, page_index=1, page_size=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 构建服务区ID → 信息的映射
        sp_map = {}
        for r in sp_rows:
            sp_map[r.get("SERVERPART_ID")] = r
        sp_id_list = ",".join([str(sid) for sid in sp_map.keys()])

        # 4. 查询服务区详情信息（T_SERVERPARTINFO）
        info_rows = db.execute_query(
            f'SELECT * FROM "T_SERVERPARTINFO" WHERE "SERVERPART_ID" IN ({sp_id_list}) AND "SERVERPART_REGION" IS NOT NULL')

        # 数值字段列表
        int_fields = ["TOILETCOUNT", "SMALLPARKING", "PACKING", "TRUCKPACKING", "LONGPACKING",
                       "DANPACKING", "LIVESTOCKPACKING", "DININGROOMCOUNT", "POINTCONTROLCOUNT",
                       "DININGBXCOUNT", "MICROWAVEOVEN", "WASHERCOUNT", "SLEEPINGPODS",
                       "REFUELINGGUN92", "REFUELINGGUN95", "REFUELINGGUN0",
                       "STATEGRIDCHARGE", "LIAUTOCHARGE", "GACENERGYCHARGE", "OTHERCHARGE"]
        short_fields = ["HASMOTHER", "HASPILOTLOUNGE", "HASPANTRY", "HASWIFI",
                        "HASTHIRDTOILETS", "HASCHILD", "HASSHOWERROOM", "HASWATERROOM",
                        "VEHICLEWATERFILLING", "HASBACKGROUNDRADIO", "HASMESSAGESEARCH"]
        decimal_fields = ["GREENSPACEAREA", "FLOORAREA", "PARKINGAREA", "BUILDINGAREA"]

        def safe_int(v):
            if v is None: return None
            try: return int(v)
            except: return None

        def safe_float(v):
            if v is None: return None
            try: return float(v)
            except: return None

        # 5. 构建区域详情列表（第三层节点）
        info_nodes = []
        for r in (info_rows or []):
            sp_id = r.get("SERVERPART_ID")
            sp = sp_map.get(sp_id, {})
            node = {
                "SERVERPART_ID": sp_id,
                "TreeNodeName": r.get("SERVERPART_REGION", ""),
                "TreeNodePName": sp.get("SERVERPART_NAME", ""),
                "BUSINESSTYPE": str(r.get("BUSINESSTYPE", "") or ""),
            }
            for f in int_fields:
                node[f] = safe_int(r.get(f))
            for f in short_fields:
                node[f] = safe_int(r.get(f))
            for f in decimal_fields:
                node[f] = safe_float(r.get(f))
            info_nodes.append({"node": node, "children": []})

        # 6. 按服务区分组汇总（第二层节点）
        from collections import defaultdict
        sp_groups = defaultdict(list)
        for item in info_nodes:
            sp_groups[item["node"]["SERVERPART_ID"]].append(item)

        def sum_field(items, field):
            vals = [it["node"].get(field) for it in items if it["node"].get(field) is not None]
            return sum(vals) if vals else None

        sp_nesting = []
        for sp_id, children in sp_groups.items():
            sp = sp_map.get(sp_id, {})
            node = {
                "SERVERPART_ID": sp_id,
                "TreeNodeName": sp.get("SERVERPART_NAME", ""),
                "TreeNodePName": sp.get("SPREGIONTYPE_NAME", ""),
                "SPRegionTypeId": sp.get("SPREGIONTYPE_ID"),
                "ServerPartIndex": safe_int(sp.get("SERVERPART_INDEX")),
            }
            for f in int_fields + short_fields:
                node[f] = sum_field(children, f)
            for f in decimal_fields:
                node[f] = sum_field(children, f)
            sorted_children = sorted(children, key=lambda x: str(x["node"].get("TreeNodeName", "")))
            sp_nesting.append({"node": node, "children": sorted_children})

        # 7. 按片区分组汇总（第一层节点）
        region_groups = defaultdict(list)
        no_region = []
        for item in sp_nesting:
            rid = item["node"].get("SPRegionTypeId")
            if rid is not None:
                region_groups[rid].append(item)
            else:
                no_region.append(item)

        result_list = []
        for rid, sp_items in region_groups.items():
            sp = None
            for r in sp_rows:
                if r.get("SPREGIONTYPE_ID") == rid:
                    sp = r
                    break
            node = {
                "TreeNodeName": sp.get("SPREGIONTYPE_NAME", "") if sp else "",
                "TreeNodePName": "",
                "SPRegionTypeId": rid,
                "SPRegionTypeIndex": safe_int(sp.get("SPREGIONTYPE_INDEX")) if sp else None,
            }
            for f in int_fields + short_fields:
                node[f] = sum_field(sp_items, f)
            for f in decimal_fields:
                node[f] = sum_field(sp_items, f)
            sorted_sp = sorted(sp_items, key=lambda x: x["node"].get("ServerPartIndex") or 0)
            result_list.append({"node": node, "children": sorted_sp})

        result_list.sort(key=lambda x: x["node"].get("SPRegionTypeIndex") or 0)
        result_list.extend(no_region)

        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_index=1, page_size=0)
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
    入参(AES加密)：ProvinceCode省份编码
    """
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        sp_region_type_id = params.get("SPRegionType_ID", "")
        serverpart_id = params.get("ServerpartId", "")
        logger.info(f"GetServerpartServiceSummary 解密参数: ProvinceCode={province_code}, SPRegionType_ID={sp_region_type_id}, ServerpartId={serverpart_id}")

        # 参照 C#: ServerpartHelper.GetServerpartServiceSummary
        # 先通过 PROVINCE_CODE 获取 FIELDENUM 的 KEY_ID
        province_key = province_code
        try:
            key_rows = db.execute_query(f"""
                SELECT E."FIELDENUM_ID" FROM "T_FIELDENUM" E
                JOIN "T_FIELDEXPLAIN" F ON E."FIELDEXPLAIN_ID" = F."FIELDEXPLAIN_ID"
                WHERE F."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE' AND E."FIELDENUM_VALUE" = '{province_code}'
            """)
            if key_rows:
                province_key = str(key_rows[0].get("FIELDENUM_ID", province_code))
        except:
            pass

        # 构建 WHERE
        where_sql = f' AND A."PROVINCE_CODE" = {province_key}'
        if sp_region_type_id:
            where_sql += f' AND A."SPREGIONTYPE_ID" IN ({sp_region_type_id})'
        if serverpart_id:
            where_sql += f' AND A."SERVERPART_ID" IN ({serverpart_id})'

        # 排除片区（安徽驿达=89）
        exclude_region = "89"
        
        sql = f"""SELECT 
                A."SERVERPART_ID", A."SERVERPART_NAME",
                COALESCE(SUM(C."FLOORAREA"), 0) AS "FLOORAREA",
                COALESCE(SUM(C."PARKINGAREA"), 0) AS "PARKINGAREA",
                COALESCE(SUM(C."BUILDINGAREA"), 0) AS "BUILDINGAREA",
                COALESCE(SUM(C."HASGASSTATION"), 0) AS "HASGASSTATION",
                COALESCE(SUM(C."LIVESTOCKPACKING"), 0) AS "HASCHARGESTATION",
                COALESCE(SUM(C."SMALLPARKING"), 0) AS "SMALLPARKING",
                COALESCE(SUM(C."PACKING"), 0) AS "PACKING",
                COALESCE(SUM(C."TRUCKPACKING"), 0) AS "TRUCKPACKING",
                COALESCE(SUM(C."LONGPACKING"), 0) AS "LONGPACKING",
                COALESCE(SUM(C."DANPACKING"), 0) AS "DANPACKING",
                COALESCE(SUM(C."HASCHILD"), 0) AS "HASAUTOREPAIR",
                COALESCE(SUM(C."HASRESTROOM"), 0) AS "HASRESTROOM",
                COALESCE(SUM(C."HASPILOTLOUNGE"), 0) AS "HASPILOTLOUNGE",
                COALESCE(SUM(C."HASMOTHER"), 0) AS "HASMOTHER",
                COALESCE(SUM(C."HASBACKGROUNDRADIO"), 0) AS "HASSTORE",
                COALESCE(SUM(C."DININGROOMCOUNT"), 0) AS "DININGROOMCOUNT",
                COALESCE(SUM(C."HASMESSAGESEARCH"), 0) AS "HASLODGING",
                COALESCE(SUM(C."VEHICLEWATERFILLING"), 0) AS "VEHICLEWATERFILLING",
                COALESCE(SUM(C."UREA_COUNT"), 0) AS "UREA_COUNT"
            FROM "T_SERVERPART" A
            LEFT JOIN "T_SERVERPARTINFO" C ON A."SERVERPART_ID" = C."SERVERPART_ID"
            WHERE A."STATISTICS_TYPE" = 1000
                AND A."SPREGIONTYPE_ID" NOT IN ({exclude_region}){where_sql}
            GROUP BY A."SERVERPART_ID", A."SERVERPART_NAME" """
        
        rows = db.execute_query(sql)
        
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")
        
        # 汇总统计（参照 C# 逻辑）
        import decimal
        total_count = len(rows)
        floor_area = round(sum(float(r.get("FLOORAREA", 0) or 0) for r in rows) / 666.67, 2)
        parking_area = round(sum(float(r.get("PARKINGAREA", 0) or 0) for r in rows) / 666.67, 2)
        building_area = round(sum(float(r.get("BUILDINGAREA", 0) or 0) for r in rows) / 666.67, 2)
        
        gas_count = sum(1 for r in rows if float(r.get("HASGASSTATION", 0) or 0) > 0)
        charge_count = sum(1 for r in rows if float(r.get("HASCHARGESTATION", 0) or 0) > 0)
        parking_lot = sum(1 for r in rows if any(float(r.get(k, 0) or 0) > 0 for k in ["SMALLPARKING", "PACKING", "TRUCKPACKING", "LONGPACKING", "DANPACKING"]))
        repair_count = sum(1 for r in rows if float(r.get("HASAUTOREPAIR", 0) or 0) > 0)
        toilet_count = sum(1 for r in rows if float(r.get("HASRESTROOM", 0) or 0) > 0)
        driver_count = sum(1 for r in rows if float(r.get("HASPILOTLOUNGE", 0) or 0) > 0)
        nursing_count = sum(1 for r in rows if float(r.get("HASMOTHER", 0) or 0) > 0)
        store_count = sum(1 for r in rows if float(r.get("HASSTORE", 0) or 0) > 0)
        catering_count = sum(1 for r in rows if float(r.get("DININGROOMCOUNT", 0) or 0) > 0)
        lodging_count = sum(1 for r in rows if float(r.get("HASLODGING", 0) or 0) > 0)
        water_count = sum(1 for r in rows if float(r.get("VEHICLEWATERFILLING", 0) or 0) > 0)
        urea_count = sum(1 for r in rows if float(r.get("UREA_COUNT", 0) or 0) > 0)
        
        # 停车区数量
        parking_service = sum(1 for r in rows if "停车区" in str(r.get("SERVERPART_NAME", "")))
        sp_count = total_count - parking_service
        
        result_data = {
            "ServerpartTotalCount": total_count,
            "ServerpartCount": sp_count,
            "ParkingServiceCount": parking_service,
            "WaterStationCount": 0,
            "ViewingDeckCount": 0,
            "RestAreaCount": 0,
            "ClosedCountCount": 0,
            "FLoorArea": floor_area,
            "ParkingArea": parking_area,
            "BuildingArea": building_area,
            "GasStationCount": gas_count,
            "ChargeStationCount": charge_count,
            "ParkingLotCount": parking_lot,
            "AutoRepairCount": repair_count,
            "ToiletCount": toilet_count,
            "DriverRoomCount": driver_count,
            "NursingRoomCount": nursing_count,
            "StoreCount": store_count,
            "CateringCount": catering_count,
            "LodgingCount": lodging_count,
            "WaterCount": water_count,
            "UreaCount": urea_count,
        }
        
        return Result.success(data=result_data, msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetServerpartServiceSummary AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
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
    入参(AES加密)：ProvinceCode省份编码
    """
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        business_trade = params.get("BusinessTrade", "")
        logger.info(f"GetBrandStructureAnalysis 解密参数: ProvinceCode={province_code}, BusinessTrade={business_trade}")

        # 参照 C#: BrandAnalysisHelper.GetBrandStructureAnalysis
        # SQL: SELECT BRAND_TYPE, COUNT(1) FROM T_BRAND
        #      WHERE BRAND_CATEGORY=1000 AND BRAND_STATE=1 AND PROVINCE_CODE=xxx
        #      GROUP BY BRAND_TYPE
        where_sql = f" AND \"PROVINCE_CODE\" = '{province_code}'"
        if business_trade:
            where_sql += f" AND \"BRAND_INDUSTRY\" IN ({business_trade})"
        
        sql = f"""SELECT "BRAND_TYPE", COUNT(1) AS CNT
            FROM "T_BRAND"
            WHERE "BRAND_CATEGORY" = 1000 AND "BRAND_STATE" = 1{where_sql}
            GROUP BY "BRAND_TYPE"
            ORDER BY "BRAND_TYPE" """
        rows = db.execute_query(sql)
        
        # 翻译 BRAND_TYPE 的字段枚举名称（从 T_FIELDENUM 表）
        brand_type_names = {}
        try:
            enum_rows = db.execute_query("""
                SELECT E."FIELDENUM_VALUE", E."FIELDENUM_NAME" 
                FROM "T_FIELDENUM" E
                JOIN "T_FIELDEXPLAIN" F ON E."FIELDEXPLAIN_ID" = F."FIELDEXPLAIN_ID"
                WHERE F."FIELDEXPLAIN_FIELD" = 'BRAND_TYPE'
            """)
            brand_type_names = {str(r["FIELDENUM_VALUE"]): r["FIELDENUM_NAME"] for r in enum_rows}
        except:
            pass
        
        result_list = []
        for row in rows:
            bt = str(row.get("BRAND_TYPE", ""))
            result_list.append({
                "name": brand_type_names.get(bt, bt),
                "value": str(row.get("CNT", 0)),
                "data": None,
                "key": bt
            })
        
        json_list = JsonListData.create(data_list=result_list, total=len(result_list), page_index=1, page_size=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetBrandStructureAnalysis AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        logger.error(f"GetBrandStructureAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
