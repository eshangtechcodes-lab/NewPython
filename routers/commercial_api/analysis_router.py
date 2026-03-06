# -*- coding: utf-8 -*-
"""
CommercialApi - Analysis 路由
对应原 CommercialApi/Controllers/AnalysisController.cs
分析说明表相关接口（12个接口）
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


# ===== 1. GetANALYSISINSList =====
@router.post("/Analysis/GetANALYSISINSList")
async def get_analysisins_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取分析说明表列表"""
    try:
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        sort_str = searchModel.get("SortStr", "ANALYSISINS_ID DESC") or "ANALYSISINS_ID DESC"
        search_param = searchModel.get("SearchParameter") or {}

        conditions = []
        params = []

        # 数据格式过滤
        formats = search_param.get("ANALYSISINS_FORMATS")
        if formats:
            conditions.append(f"\"ANALYSISINS_FORMAT\" IN ({formats})")

        # 分析类型过滤
        types = search_param.get("ANALYSISINS_TYPES")
        if types:
            conditions.append(f"\"ANALYSISINS_TYPE\" IN ({types})")

        # 服务区内码过滤
        sp_ids = search_param.get("SERVERPART_IDS")
        if sp_ids:
            conditions.append(f"\"SERVERPART_ID\" IN ({sp_ids})")

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        # 查询总数
        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_ANALYSISINS"{where_sql}'
        count_rows = db.execute_query(count_sql, params)
        total = count_rows[0]["CNT"] if count_rows else 0

        # 分页查询
        offset = (page_index - 1) * page_size
        data_sql = f'SELECT * FROM "T_ANALYSISINS"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
        page_params = (params if params else []) + [page_size, offset]
        page_rows = db.execute_query(data_sql, page_params)

        # 格式化日期，补全搜索参数字段
        for r in page_rows:
            if r.get("OPERATE_DATE"):
                r["OPERATE_DATE"] = str(r["OPERATE_DATE"])
            r["ANALYSISINS_FORMATS"] = formats
            r["ANALYSISINS_TYPES"] = types
            r["SERVERPART_IDS"] = sp_ids

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetANALYSISINSList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 2. GetANALYSISINSDetail =====
@router.get("/Analysis/GetANALYSISINSDetail")
async def get_analysisins_detail(ANALYSISINSId: Optional[int] = Query(None, description="分析说明表内码"), db: DatabaseHelper = Depends(get_db)):
    """获取分析说明表明细"""
    try:
        sql = 'SELECT * FROM "T_ANALYSISINS" WHERE "ANALYSISINS_ID" = ?'
        rows = db.execute_query(sql, [ANALYSISINSId])
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        data = rows[0]
        if data.get("OPERATE_DATE"):
            data["OPERATE_DATE"] = str(data["OPERATE_DATE"])
        data["ANALYSISINS_FORMATS"] = None
        data["ANALYSISINS_TYPES"] = None
        data["SERVERPART_IDS"] = None

        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetANALYSISINSDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")




# ===== 6. SolidTransactionAnalysis =====
@router.post("/Analysis/SolidTransactionAnalysis")
async def solid_transaction_analysis(analysisParamModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """生成时段客单交易分析数据"""
    try:
        analysisParamModel = analysisParamModel or {}
        amount_range_list = analysisParamModel.get("AmountRangeList")
        if not amount_range_list:
            return Result.fail(code=200, msg="生成失败！请传入正确的参数")

        # TODO: 实现生成逻辑
        logger.warning("SolidTransactionAnalysis 生成逻辑暂未实现")
        return Result.success(msg="生成成功")
    except Exception as ex:
        return Result.fail(msg=f"生成失败{ex}")


# ===== 7. GetTransactionAnalysis =====
@router.post("/Analysis/GetTransactionAnalysis")
async def get_transaction_analysis(tapModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取时段客单交易分析数据
    涉及表：T_TRANSACTIONANALYSIS JOIN T_SERVERPARTSHOP
    入参：ServerpartId, ServerpartShopId, StartMonth, EndMonth, DataType(1客单/2营收/3客单均价)
    返回：name=时段, value=数值, key=金额区间名称
    """
    try:
        tapModel = tapModel or {}
        conditions = []
        params = []

        # 门店内码过滤
        shop_id = tapModel.get("ServerpartShopId")
        sp_id = tapModel.get("ServerpartId")
        if shop_id:
            ids = [x.strip() for x in str(shop_id).split(",") if x.strip()]
            placeholders = ",".join(["?" for _ in ids])
            conditions.append(f'"A"."SERVERPARTSHOP_ID" IN ({placeholders})')
            params.extend(ids)
        elif sp_id:
            ids = [x.strip() for x in str(sp_id).split(",") if x.strip()]
            placeholders = ",".join(["?" for _ in ids])
            conditions.append(f'"A"."SERVERPART_ID" IN ({placeholders})')
            params.extend(ids)

        # 月份范围
        start_month = tapModel.get("StartMonth")
        end_month = tapModel.get("EndMonth")
        if start_month:
            conditions.append('"A"."STATISTICS_MONTH" >= ?')
            params.append(start_month)
        if end_month:
            conditions.append('"A"."STATISTICS_MONTH" <= ?')
            params.append(end_month)

        where_sql = (" AND " + " AND ".join(conditions)) if conditions else ""

        # 查询聚合数据：按小时和金额区间分组
        sql = f"""SELECT
            "A"."STATISTICS_HOUR", "A"."AMOUNT_STARTRANGE", "A"."AMOUNT_ENDRANGE",
            SUM("A"."TOTAL_COUNT") AS "TOTAL_COUNT",
            SUM("A"."TICKET_COUNT") AS "TICKET_COUNT",
            SUM("A"."REVENUE_AMOUNT") AS "REVENUE_AMOUNT"
        FROM "T_TRANSACTIONANALYSIS" "A", "T_SERVERPARTSHOP" "B"
        WHERE "A"."SERVERPARTSHOP_ID" = "B"."SERVERPARTSHOP_ID"{where_sql}
        GROUP BY "A"."STATISTICS_HOUR", "A"."AMOUNT_STARTRANGE", "A"."AMOUNT_ENDRANGE"
        """
        rows = db.execute_query(sql, params if params else None)

        if not rows:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 提取金额区间列表
        range_set = set()
        for r in rows:
            range_set.add((r.get("AMOUNT_STARTRANGE"), r.get("AMOUNT_ENDRANGE")))
        range_list = sorted(range_set, key=lambda x: (x[0] or 0))

        # 构建查找字典
        data_map = {}
        for r in rows:
            key = (r.get("STATISTICS_HOUR"), r.get("AMOUNT_STARTRANGE"), r.get("AMOUNT_ENDRANGE"))
            data_map[key] = r

        data_type = tapModel.get("DataType", 0)
        result_list = []

        for hour in range(24):
            for (start_range, end_range) in range_list:
                # 构造区间名称
                if start_range is not None and end_range is not None:
                    type_name = f"{start_range}-{end_range}元"
                elif start_range is not None:
                    type_name = f"{start_range}元以上"
                elif end_range is not None:
                    type_name = f"{end_range}元以下"
                else:
                    continue

                key = (hour, start_range, end_range)
                if key in data_map:
                    r = data_map[key]
                    ticket = r.get("TICKET_COUNT") or 0
                    revenue = r.get("REVENUE_AMOUNT") or 0
                    if data_type == 1:
                        value = str(ticket)
                    elif data_type == 2:
                        value = str(revenue)
                    else:
                        value = str(round(revenue / ticket, 2)) if ticket else "0"
                else:
                    value = "0"

                result_list.append({
                    "name": f"{hour}时",
                    "value": value,
                    "key": type_name,
                    "data": None,
                })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetTransactionAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 8. TranslateSentence =====
@router.get("/Analysis/TranslateSentence")
async def translate_sentence(
    Sentence: Optional[str] = Query(None, description="语义内容"),
    DialogCode: Optional[str] = Query("", description="对话框编码"),
    ProvinceCode: Optional[str] = Query("", description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """解析语义内容中的关键字信息"""
    try:
        logger.warning("TranslateSentence 暂未完整实现")
        return Result.success(data={}, msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")


# ===== 9. GetMapConfigByProvinceCode =====
@router.get("/Analysis/GetMapConfigByProvinceCode")
async def get_map_config_by_province_code(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取地图参数配置"""
    try:
        sql = 'SELECT * FROM "T_MAPCONFIG" WHERE "PROVINCE_CODE" = ?'
        rows = db.execute_query(sql, [ProvinceCode])
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        return Result.success(data=rows[0], msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMapConfigByProvinceCode 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 10. GetServerpartTypeAnalysis =====
@router.post("/Analysis/GetServerpartTypeAnalysis")
async def get_serverpart_type_analysis(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取服务区分类定级情况（AES加密，参数：ProvinceCode）"""
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        logger.info(f"GetServerpartTypeAnalysis 解密参数: ProvinceCode={province_code}")

        # TODO: 实现查询逻辑 - ESCG.BusinessAnalysisHelper.GetServerpartTypeList
        logger.warning("GetServerpartTypeAnalysis 查询逻辑暂未实现")
        json_list = JsonListData.create(data_list=[], total=0)
        resp = json_list.model_dump()
        resp["OtherData"] = None
        resp["legend"] = None
        resp["ColumnList"] = []
        return Result.success(data=resp, msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetServerpartTypeAnalysis AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")



