from __future__ import annotations
# -*- coding: utf-8 -*-
"""
经营项目管理 API 路由（BusinessProjectController 专属）
路由前缀：/BusinessProject/
当前实现：BusinessProject 的 4 个 CRUD 接口
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.business_project import business_project_service as bp_svc
from routers.deps import get_db

router = APIRouter()


# ===================================================================
# 1. GetBusinessProjectList（POST searchModel）
# C# 路由：BusinessProject/GetBusinessProjectList
# C# 方法：POST
# 核心逻辑：Header 获取 ProvinceCode/ServerpartCodes → SERVERPART_IDS
# ===================================================================

@router.post("/BusinessProject/GetBusinessProjectList")
async def get_businessproject_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        sp = search_model.SearchParameter or {}

        # C# 逻辑：从 Header 获取 ServerpartCodes 转 SERVERPART_IDS
        if not sp.get("SERVERPART_IDS"):
            serverpart_codes = request.headers.get("ServerpartCodes", "")
            if serverpart_codes:
                try:
                    codes_in = ",".join([f"'{c.strip()}'" for c in serverpart_codes.split(",") if c.strip()])
                    ids_sql = f"SELECT SERVERPART_ID FROM T_SERVERPART WHERE SERVERPART_CODE IN ({codes_in})"
                    id_rows = db.execute_query(ids_sql)
                    if id_rows:
                        sp["SERVERPART_IDS"] = ",".join([str(r["SERVERPART_ID"]) for r in id_rows])
                except Exception as e:
                    logger.warning(f"ServerpartCodes 转 IDS 失败: {e}")

        total, data_list, summary_list = bp_svc.get_businessproject_list(
            db, search_model, sp.get("SERVERPART_IDS", ""))

        json_list = JsonListData.create(
            data_list=data_list, total=total,
            page_index=search_model.PageIndex, page_size=search_model.PageSize)

        # C# 响应中包含 OtherData（summaryList）
        result_data = json_list.model_dump()
        result_data["OtherData"] = summary_list

        return Result.success(data=result_data, msg="查询成功")
    except Exception as ex:
        logger.error(f"BusinessProject/GetBusinessProjectList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===================================================================
# 2. GetBusinessProjectDetail（GET/POST BusinessProjectId）
# C# 路由：BusinessProject/GetBusinessProjectDetail
# C# 方法：GET, POST
# ===================================================================

@router.api_route("/BusinessProject/GetBusinessProjectDetail", methods=["GET", "POST"])
async def get_businessproject_detail(
    BusinessProjectId: int = Query(..., description="经营项目内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营项目明细"""
    try:
        detail = bp_svc.get_businessproject_detail(db, BusinessProjectId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"BusinessProject/GetBusinessProjectDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===================================================================
# 3. SynchroBusinessProject（POST model）
# C# 路由：BusinessProject/SynchroBusinessProject
# C# 方法：POST
# 核心逻辑：从 Header Token 中解析 UserId/UserName
# ===================================================================

@router.post("/BusinessProject/SynchroBusinessProject")
async def synchro_businessproject(
    request: Request,
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步经营项目"""
    try:
        # C# 逻辑：从 Header Token 中解析用户信息
        user_id = None
        user_name = ""
        token = request.headers.get("Token", "")
        if token:
            try:
                import json
                from core.security import decrypt_aes
                decoded = json.loads(decrypt_aes(token))
                user_id = decoded.get("UserID")
                user_name = decoded.get("UserName", "")
            except Exception as te:
                logger.debug(f"Token 解析跳过: {te}")

        success, result_data = bp_svc.synchro_businessproject(
            db, data, user_id, user_name)

        if success:
            return Result.success(data=result_data, msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"BusinessProject/SynchroBusinessProject 同步失败: {ex}")
        return Result.fail(msg=f"同步失败{ex}")


# ===================================================================
# 4. DeleteBusinessProject（GET/POST BusinessProjectId, ForceDelete）
# C# 路由：BusinessProject/DeleteBusinessProject
# C# 方法：GET, POST
# 核心逻辑：软删除 + ForceDelete 检查 + Token 解析
# ===================================================================

@router.api_route("/BusinessProject/DeleteBusinessProject", methods=["GET", "POST"])
async def delete_businessproject(
    request: Request,
    BusinessProjectId: int = Query(..., description="经营项目内码"),
    ForceDelete: bool = Query(False, description="是否强制删除"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除经营项目"""
    try:
        # C# 逻辑：从 Header Token 中解析用户信息
        user_id = None
        user_name = ""
        token = request.headers.get("Token", "")
        if token:
            try:
                import json
                from core.security import decrypt_aes
                decoded = json.loads(decrypt_aes(token))
                user_id = decoded.get("UserID")
                user_name = decoded.get("UserName", "")
            except Exception as te:
                logger.debug(f"Token 解析跳过: {te}")

        success, msg = bp_svc.delete_businessproject(
            db, BusinessProjectId, ForceDelete, user_id, user_name)

        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc=msg or "删除失败")
    except Exception as ex:
        logger.error(f"BusinessProject/DeleteBusinessProject 删除失败: {ex}")
        return Result.fail(msg=f"删除失败{ex}")
