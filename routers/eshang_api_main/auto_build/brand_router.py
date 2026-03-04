# -*- coding: utf-8 -*-
"""
品牌表 API 路由
对应原 BRANDController.cs，保持相同的路由路径和响应格式
"""
import json
from fastapi import APIRouter, Depends
from loguru import logger

from core.database import DatabaseHelper
from core.aes_util import aes_decrypt
from models.base import Result, JsonListData
from models.common_model import CommonModel, SearchModel
from models.auto_build.brand import BRANDModel
from services.auto_build import brand_service
from routers.deps import get_db

router = APIRouter()


@router.post("/BaseInfo/GetBRANDList")
async def get_brand_list(post_data: CommonModel, db: DatabaseHelper = Depends(get_db)):
    """
    获取品牌表列表
    对应原: [Route("BaseInfo/GetBRANDList")]
    """
    try:
        # 解密并解析查询参数
        decrypted = aes_decrypt(post_data.value)
        search_data = json.loads(decrypted)
        search_model = SearchModel(**search_data)

        # 查询数据
        total_count, brand_list = brand_service.get_brand_list(db, search_model)

        # 构建分页响应（保持原格式）
        json_list = JsonListData.create(
            data_list=brand_list,
            total=total_count,
            page_index=search_model.PageIndex,
            page_size=search_model.PageSize
        )

        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBRANDList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/GetBRANDDetail")
async def get_brand_detail(post_data: CommonModel, db: DatabaseHelper = Depends(get_db)):
    """
    获取品牌表明细
    对应原: [Route("BaseInfo/GetBRANDDetail")]
    """
    try:
        # 解密并解析参数
        decrypted = aes_decrypt(post_data.value)
        params = json.loads(decrypted)
        brand_id = int(params.get("BRANDId", 0))

        # 查询明细
        brand = brand_service.get_brand_detail(db, brand_id)

        return Result.success(data=brand, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetBRANDDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


@router.post("/BaseInfo/SynchroBRAND")
async def synchro_brand(post_data: CommonModel, db: DatabaseHelper = Depends(get_db)):
    """
    同步品牌表（新增/更新）
    对应原: [Route("BaseInfo/SynchroBRAND")]
    """
    try:
        # 解密并解析品牌数据
        decrypted = aes_decrypt(post_data.value)
        brand_data = json.loads(decrypted)

        # 执行同步
        success, result_data = brand_service.synchro_brand(db, brand_data)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        else:
            return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"SynchroBRAND 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


@router.post("/BaseInfo/DeleteBRAND")
async def delete_brand(post_data: CommonModel, db: DatabaseHelper = Depends(get_db)):
    """
    删除品牌表（软删除）
    对应原: [Route("BaseInfo/DeleteBRAND")]
    """
    try:
        # 解密并解析参数
        decrypted = aes_decrypt(post_data.value)
        params = json.loads(decrypted)
        brand_id = int(params.get("BRANDId", 0))

        # 执行删除
        success = brand_service.delete_brand(db, brand_id)

        if success:
            return Result.success(msg="删除成功")
        else:
            return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"DeleteBRAND 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
