# -*- coding: utf-8 -*-
"""
CommercialApi - BaseInfo 路由
对应原 CommercialApi/Controllers/BaseInfoController.cs
"""
from fastapi import APIRouter, Depends, Query
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

router = APIRouter()


@router.get("/BaseInfo/GetSPRegionList")
async def get_sp_region_list(
    Province_Code: str = Query(..., description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """
    获取片区列表
    对应原: [Route("BaseInfo/GetSPRegionList")] GET
    原 SQL: SELECT * FROM T_SERVERPARTTYPE 
            WHERE SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = ?
            ORDER BY TYPE_INDEX
    返回: CommonModel 列表 {name, value}
    """
    try:
        sql = """
            SELECT TYPE_NAME, SERVERPARTTYPE_ID 
            FROM T_SERVERPARTTYPE 
            WHERE SERVERPARTSTATICTYPE_ID = 1000 AND PROVINCE_CODE = ?
            ORDER BY TYPE_INDEX
        """
        rows = db.execute_query(sql, [Province_Code])

        # 转换为原 API 返回的 {name, value} 格式
        region_list = []
        for row in rows:
            region_list.append({
                "name": row.get("TYPE_NAME", ""),
                "value": str(row.get("SERVERPARTTYPE_ID", "")),
            })

        # 构建分页响应（原 API 格式：PageIndex=1, PageSize=全部数据量）
        json_list = JsonListData.create(
            data_list=region_list,
            total=len(region_list),
            page_index=1,
            page_size=len(region_list)
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetSPRegionList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")
