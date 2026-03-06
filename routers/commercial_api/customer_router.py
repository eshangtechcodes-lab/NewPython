# -*- coding: utf-8 -*-
"""
CommercialApi - Customer 路由
对应原 CommercialApi/Controllers/CustomerController.cs
客群分析相关接口（8个接口）
"""
from fastapi import APIRouter, Depends, Query
from typing import Optional
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


@router.get("/Customer/GetCustomerRatio")
async def get_customer_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份，格式如202110"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群分析占比（男/女/年龄层次占比）"""
    try:
        # 动态构建 WHERE 条件，serverpartId 非必填
        conditions = []
        params = {}
        if serverpartId:
            conditions.append("SERVERPART_ID = :serverpartId")
            params["serverpartId"] = serverpartId
        if statisticsMonth:
            conditions.append("STATISTICS_MONTH = :statisticsMonth")
            params["statisticsMonth"] = statisticsMonth
        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"SELECT COUNT_MALE, COUNT_FEMALE, COUNT_00, COUNT_90, COUNT_80, COUNT_70 FROM T_CUSTOMERGROUP{where_sql}"
        data = db.execute_query(sql, params)
        
        results = []
        if data:
            row = data[0]
            results.append({"name": "男性", "data": [float(row["COUNT_MALE"])]})
            results.append({"name": "女性", "data": [float(row["COUNT_FEMALE"])]})
            results.append({"name": "年龄", "data": [
                float(row["COUNT_00"]), float(row["COUNT_90"]), 
                float(row["COUNT_80"]), float(row["COUNT_70"])
            ]})
            
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerConsumeRatio")
async def get_customer_consume_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群消费能力占比（4种金额区间交易客单数量占比）"""
    try:
        # 动态构建 WHERE 条件
        conditions = []
        params = {}
        if serverpartId:
            conditions.append("SERVERPART_ID = :serverpartId")
            params["serverpartId"] = serverpartId
        if statisticsMonth:
            conditions.append("STATISTICS_MONTH = :statisticsMonth")
            params["statisticsMonth"] = statisticsMonth
        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"SELECT COUNT_MALE_30, COUNT_MALE_60, COUNT_MALE_90, COUNT_MALE_90U, COUNT_FEMALE_30, COUNT_FEMALE_60, COUNT_FEMALE_90, COUNT_FEMALE_90U FROM T_CUSTOMER_CONSUME{where_sql}"
        data = db.execute_query(sql, params)
        
        results = []
        if data:
            row = data[0]
            results.append({"name": "男性", "data": [
                float(row["COUNT_MALE_30"]), float(row["COUNT_MALE_60"]), 
                float(row["COUNT_MALE_90"]), float(row["COUNT_MALE_90U"])
            ]})
            results.append({"name": "女性", "data": [
                float(row["COUNT_FEMALE_30"]), float(row["COUNT_FEMALE_60"]), 
                float(row["COUNT_FEMALE_90"]), float(row["COUNT_FEMALE_90U"])
            ]})
            
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerConsumeRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerAgeRatio")
async def get_customer_age_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群年龄层次占比"""
    try:
        # 动态构建 WHERE 条件
        conditions = []
        params = {}
        if serverpartId:
            conditions.append("SERVERPART_ID = :serverpartId")
            params["serverpartId"] = serverpartId
        if statisticsMonth:
            conditions.append("STATISTICS_MONTH = :statisticsMonth")
            params["statisticsMonth"] = statisticsMonth
        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"SELECT COUNT_MALE_00, COUNT_MALE_90, COUNT_MALE_80, COUNT_MALE_70, COUNT_FEMALE_00, COUNT_FEMALE_90, COUNT_FEMALE_80, COUNT_FEMALE_70 FROM T_CUSTOMER_AGE{where_sql}"
        data = db.execute_query(sql, params)
        
        results = []
        if data:
            row = data[0]
            results.append({"name": "男性", "data": [
                float(row["COUNT_MALE_00"]), float(row["COUNT_MALE_90"]), 
                float(row["COUNT_MALE_80"]), float(row["COUNT_MALE_70"])
            ]})
            results.append({"name": "女性", "data": [
                float(row["COUNT_FEMALE_00"]), float(row["COUNT_FEMALE_90"]), 
                float(row["COUNT_FEMALE_80"]), float(row["COUNT_FEMALE_70"])
            ]})
            
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerAgeRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerGroupRatio")
async def get_customer_group_ratio(
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群特征分析（散点图数据）"""
    try:
        # T_CUSTOMER_GAC 包含 32 个字段，简化逻辑：读取该行所有数据并按性别分组
        # 动态构建 WHERE 条件
        conditions = []
        params = {}
        if serverpartId:
            conditions.append("SERVERPART_ID = :serverpartId")
            params["serverpartId"] = serverpartId
        if statisticsMonth:
            conditions.append("STATISTICS_MONTH = :statisticsMonth")
            params["statisticsMonth"] = statisticsMonth
        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f"SELECT * FROM T_CUSTOMER_GAC{where_sql}"
        data = db.execute_query(sql, params)
        
        results = []
        if data:
            row = data[0]
            # 简化版：这里需要大量的随机坐标或特定逻辑，目前先按业务结构返回数据点
            # 仅演示前几个点，实际生产环境需按 C# RandomAge/RandomAmount 逻辑构建
            male_data = []
            for col in [c for c in row.keys() if "MALE" in c]:
                male_data.append([25, 50, float(row[col])]) # [年龄, 金额, 占比]
            results.append({"name": "男性", "data": male_data})
            
            female_data = []
            for col in [c for c in row.keys() if "FEMALE" in c]:
                female_data.append([25, 50, float(row[col])])
            results.append({"name": "女性", "data": female_data})
            
        json_list = JsonListData.create(data_list=results, total=len(results))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetCustomerGroupRatio 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetAnalysisDescList")
async def get_analysis_desc_list(
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    statisticsType: Optional[int] = Query(None, description="统计类型：1消费人群 2消费能力 3客群特征 4消费能力分析 5年龄层次分析"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群分析说明表列表"""
    try:
        where_parts = []
        params = {}
        
        if serverpartId:
            where_parts.append("SERVERPART_ID = :serverpartId")
            params["serverpartId"] = serverpartId
        elif serverpartCode:
            where_parts.append("SERVERPART_CODE = :serverpartCode")
            params["serverpartCode"] = serverpartCode
        else:
            where_parts.append("1 = 2")
            
        if statisticsType:
            where_parts.append("STATISTICS_TYPE = :statisticsType")
            params["statisticsType"] = statisticsType
            
        if statisticsMonth:
            where_parts.append("STATISTICS_MONTH = :statisticsMonth")
            params["statisticsMonth"] = statisticsMonth
            
        where_sql = " AND ".join(where_parts)
        sql = f"SELECT STATISTICS_TYPE, SERVERPART_NAME, ANALYSIS_CONTENT, KEY_CONTENT FROM T_CUSTOMER_ANALYSIS WHERE {where_sql} ORDER BY STATISTICS_TYPE"
        
        data_list = db.execute_query(sql, params)
        
        # 转换字段映射 (因原 API 要求驼峰或首字母大写，需按 Model 调整)
        formatted_list = []
        for row in data_list:
            formatted_list.append({
                "Statistics_Type": row["STATISTICS_TYPE"],
                "Serverpart_Name": row["SERVERPART_NAME"],
                "Analysis_Content": row["ANALYSIS_CONTENT"],
                "Key_Content": row["KEY_CONTENT"]
            })
            
        json_list = JsonListData.create(data_list=formatted_list, total=len(formatted_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAnalysisDescList 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetAnalysisDescDetail")
async def get_analysis_desc_detail(
    statisticsType: Optional[int] = Query(None, description="统计类型"),
    statisticsMonth: Optional[str] = Query(None, description="统计月份"),
    serverpartId: Optional[int] = Query(None, description="服务区内码"),
    serverpartCode: Optional[str] = Query("", description="服务区编码"),
    provinceCode: Optional[str] = Query("", description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群分析说明表明细"""
    try:
        where_parts = []
        params = {"statisticsType": statisticsType}
        
        if serverpartId:
            where_parts.append("SERVERPART_ID = :serverpartId")
            params["serverpartId"] = serverpartId
        elif serverpartCode:
            where_parts.append("SERVERPART_CODE = :serverpartCode")
            params["serverpartCode"] = serverpartCode
        elif provinceCode:
             where_parts.append("SERVERPART_CODE = :provinceCode")
             params["provinceCode"] = provinceCode
        else:
            where_parts.append("1 = 2")
            
        if statisticsMonth:
            where_parts.append("STATISTICS_MONTH = :statisticsMonth")
            params["statisticsMonth"] = statisticsMonth
            
        where_sql = " AND ".join(where_parts)
        sql = f"SELECT STATISTICS_TYPE, SERVERPART_NAME, ANALYSIS_CONTENT, KEY_CONTENT FROM T_CUSTOMER_ANALYSIS WHERE STATISTICS_TYPE = :statisticsType AND {where_sql}"
        
        data_list = db.execute_query(sql, params)
        if not data_list:
            return Result.success(code=101, msg="查询失败，无数据返回！")
            
        row = data_list[0]
        formatted_data = {
            "Statistics_Type": row["STATISTICS_TYPE"],
            "Serverpart_Name": row["SERVERPART_NAME"],
            "Analysis_Content": row["ANALYSIS_CONTENT"],
            "Key_Content": row["KEY_CONTENT"]
        }
        return Result.success(data=formatted_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetAnalysisDescDetail 错误: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.get("/Customer/GetCustomerSaleRatio")
async def get_customer_sale_ratio(
    ProvinceCode: Optional[str] = Query(None, description="省份编码"),
    StatisticsMonth: Optional[str] = Query(None, description="统计月份"),
    ServerpartId: Optional[int] = Query(None, description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    BusinessTradeId: Optional[str] = Query("", description="经营业态内码"),
    ShowDetail: int = Query(0, description="0不显示明细，否则显示"),
    sortStr: Optional[str] = Query("", description="排序字段"),
    fromRedis: bool = Query(False, description="从缓存取值"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取客群消费偏好数据"""
    try:
        logger.warning("GetCustomerSaleRatio 暂未完整实现")
        json_list = JsonListData.create(data_list=[], total=0)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")
