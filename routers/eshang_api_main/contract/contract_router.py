from __future__ import annotations
# -*- coding: utf-8 -*-
"""
合同备案管理 API 路由（ContractController 专属）
路由前缀：/Contract/
对应 C# ContractController.cs 中 25 个非加密接口
"""
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, Query, Header, Request
from loguru import logger

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from models.common_model import SearchModel
from services.contract import contract_service
from routers.deps import get_db

router = APIRouter()


# ===================================================================
# 1. RegisterCompact（合同备案表）CRUD
# ===================================================================

@router.post("/Contract/GetRegisterCompactList")
async def get_registercompact_list(
    request: Request,
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同备案列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        sp = search_model.SearchParameter or {}

        # C# 逻辑：Header ServerpartCodes -> SERVERPART_IDS
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

        # C# 逻辑：Header ServerpartShopIds
        if not sp.get("SERVERPARTSHOP_IDS"):
            sp["SERVERPARTSHOP_IDS"] = request.headers.get("ServerpartShopIds", "")

        # 商户账号（UserPattern=2000）无门店权限返回空
        user_pattern = request.headers.get("UserPattern", "")
        if user_pattern == "2000" and not sp.get("SERVERPARTSHOP_IDS"):
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        total, data_list = contract_service.get_registercompact_list(
            db, search_model, sp.get("SERVERPART_IDS", ""), sp.get("SERVERPARTSHOP_IDS", ""))
        json_list = JsonListData.create(data_list=data_list, total=total,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetRegisterCompactList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetRegisterCompactDetail")
async def get_registercompact_detail(
    RegisterCompactId: int = Query(..., description="合同备案内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同备案明细"""
    try:
        detail = contract_service.get_registercompact_detail(db, RegisterCompactId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetRegisterCompactDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Contract/SynchroRegisterCompact")
async def synchro_registercompact(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步合同备案表"""
    try:
        success, result_data = contract_service.synchro_registercompact(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/SynchroRegisterCompact 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Contract/DeleteRegisterCompact", methods=["GET", "POST"])
async def delete_registercompact(
    RegisterCompactId: int = Query(..., description="合同备案内码"),
    ForceDelete: bool = Query(False, description="是否强制删除"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除合同备案表"""
    try:
        success, msg = contract_service.delete_registercompact(db, RegisterCompactId, ForceDelete)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc=msg or "删除失败")
    except Exception as ex:
        logger.error(f"Contract/DeleteRegisterCompact 删除失败: {ex}")
        return Result.fail(msg="删除失败")


# ===================================================================
# 2. RegisterCompactSub（备案合同附属表）CRUD
# ===================================================================

@router.post("/Contract/GetRegisterCompactSubList")
async def get_registercompactsub_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取备案合同附属列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total, data_list = contract_service.get_registercompactsub_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetRegisterCompactSubList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetRegisterCompactSubDetail")
async def get_registercompactsub_detail(
    RegisterCompactSubId: int = Query(None, description="附属内码"),
    RegisterCompactId: int = Query(None, description="备案合同内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取备案合同附属表明细"""
    try:
        detail = contract_service.get_registercompactsub_detail(db, RegisterCompactSubId, RegisterCompactId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetRegisterCompactSubDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Contract/SynchroRegisterCompactSub")
async def synchro_registercompactsub(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步备案合同附属表"""
    try:
        success, result_data = contract_service.synchro_registercompactsub(db, data)
        if success:
            return Result.success(data=result_data, msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/SynchroRegisterCompactSub 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Contract/DeleteRegisterCompactSub", methods=["GET", "POST"])
async def delete_registercompactsub(
    RegisterCompactSubId: int = Query(..., description="附属内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除备案合同附属表"""
    try:
        success = contract_service.delete_registercompactsub(db, RegisterCompactSubId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/DeleteRegisterCompactSub 删除失败: {ex}")
        return Result.fail(msg="删除失败")


# ===================================================================
# 3. RTRegisterCompact（经营合同-服务区关联表）CRUD
# ===================================================================

@router.post("/Contract/GetRTRegisterCompactList")
async def get_rtregistercompact_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营合同服务区关联表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total, data_list = contract_service.get_rtregistercompact_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetRTRegisterCompactList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetRTRegisterCompactDetail")
async def get_rtregistercompact_detail(
    RTRegisterCompactId: int = Query(None, description="关联表内码"),
    RegisterCompactId: int = Query(None, description="备案合同内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取经营合同服务区关联表明细"""
    try:
        detail = contract_service.get_rtregistercompact_detail(db, RTRegisterCompactId, RegisterCompactId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetRTRegisterCompactDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Contract/SynchroRTRegisterCompact")
async def synchro_rtregistercompact(
    data: list,
    db: DatabaseHelper = Depends(get_db)
):
    """同步经营合同服务区关联表（批量）"""
    try:
        success = contract_service.synchro_rtregistercompact_list(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/SynchroRTRegisterCompact 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Contract/DeleteRTRegisterCompact", methods=["GET", "POST"])
async def delete_rtregistercompact(
    RTRegisterCompactId: int = Query(..., description="关联表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除经营合同服务区关联表"""
    try:
        success = contract_service.delete_rtregistercompact(db, RTRegisterCompactId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/DeleteRTRegisterCompact 删除失败: {ex}")
        return Result.fail(msg="删除失败")


# ===================================================================
# 4. Attachment（附件表）CRUD + SaveAttachment + DelFile
# ===================================================================

@router.post("/Contract/GetAttachmentList")
async def get_attachment_list(
    search_model: Optional[SearchModel] = None,
    db: DatabaseHelper = Depends(get_db)
):
    """获取附件表列表"""
    try:
        if search_model is None:
            search_model = SearchModel()
        total, data_list = contract_service.get_attachment_list(db, search_model)
        json_list = JsonListData.create(data_list=data_list, total=total,
                                         page_index=search_model.PageIndex, page_size=search_model.PageSize)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetAttachmentList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetAttachmentDetail")
async def get_attachment_detail(
    AttachmentId: int = Query(..., description="附件表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取附件表明细"""
    try:
        detail = contract_service.get_attachment_detail(db, AttachmentId)
        return Result.success(data=detail, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetAttachmentDetail 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.post("/Contract/SynchroAttachmentList")
async def synchro_attachment_list(
    data: list,
    db: DatabaseHelper = Depends(get_db)
):
    """保存附件列表（批量同步）"""
    try:
        success = contract_service.synchro_attachment_list(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/SynchroAttachmentList 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.post("/Contract/SynchroAttachment")
async def synchro_attachment(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """同步附件表"""
    try:
        success, result_data = contract_service.synchro_attachment(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="更新失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/SynchroAttachment 同步失败: {ex}")
        return Result.fail(msg="同步失败")


@router.api_route("/Contract/DeleteAttachment", methods=["GET", "POST"])
async def delete_attachment(
    AttachmentId: int = Query(..., description="附件表内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """删除附件表"""
    try:
        success = contract_service.delete_attachment(db, AttachmentId)
        if success:
            return Result.success(msg="删除成功")
        return Result(Result_Code=200, Result_Desc="删除失败，数据不存在！")
    except Exception as ex:
        logger.error(f"Contract/DeleteAttachment 删除失败: {ex}")
        return Result.fail(msg="删除失败")


@router.post("/Contract/SaveAttachment")
async def save_attachment(
    request: Request,
    db: DatabaseHelper = Depends(get_db)
):
    """上传附件信息（占位接口，原 C# 涉及文件系统操作）"""
    try:
        return Result(Result_Code=200, Result_Desc="此接口需要文件系统支持，暂未实现")
    except Exception as ex:
        logger.error(f"Contract/SaveAttachment 上传失败: {ex}")
        return Result.fail(msg="上传失败")


@router.api_route("/Contract/DelFile", methods=["GET", "POST"])
async def del_file(
    request: Request,
    db: DatabaseHelper = Depends(get_db)
):
    """根据路径删除附件（占位接口）"""
    try:
        return Result(Result_Code=200, Result_Desc="此接口需要文件系统支持，暂未实现")
    except Exception as ex:
        logger.error(f"Contract/DelFile 删除失败: {ex}")
        return Result.fail(msg="删除失败")


# ===================================================================
# 5. 汇总查询
# ===================================================================

@router.get("/Contract/GetProjectSummaryInfo")
async def get_project_summary_info(
    request: Request,
    ProvinceCode: int = Query(None, description="省份编码"),
    ServerpartId: int = Query(None, description="服务区内码"),
    ServerpartShopIds: str = Query("", description="门店内码集合"),
    GetFromRedis: bool = Query(False, description="从缓存表取值"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取项目欠款汇总信息"""
    try:
        # C# 逻辑：商户账号需要门店权限
        user_pattern = request.headers.get("UserPattern", "")
        if user_pattern == "2000":
            ServerpartShopIds = request.headers.get("ServerpartShopIds", ServerpartShopIds) or "0"
        ProvinceCode = int(request.headers.get("ProvinceCode", str(ProvinceCode or ""))) if not ProvinceCode else ProvinceCode

        data = contract_service.get_project_summary_info(
            db, ProvinceCode, ServerpartId, ServerpartShopIds, get_from_redis=GetFromRedis)
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetProjectSummaryInfo 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetContractExpiredInfo")
async def get_contract_expired_info(
    request: Request,
    ProvinceCode: int = Query(None, description="省份编码"),
    ServerpartId: int = Query(None, description="服务区内码"),
    ServerpartShopIds: str = Query("", description="门店内码集合"),
    GetFromRedis: bool = Query(False, description="从缓存表取值"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同到期信息"""
    try:
        user_pattern = request.headers.get("UserPattern", "")
        if user_pattern == "2000":
            ServerpartShopIds = request.headers.get("ServerpartShopIds", ServerpartShopIds) or "0"
        ProvinceCode = int(request.headers.get("ProvinceCode", str(ProvinceCode or ""))) if not ProvinceCode else ProvinceCode

        data = contract_service.get_contract_expired_info(
            db, ProvinceCode, ServerpartId, ServerpartShopIds, get_from_redis=GetFromRedis)
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetContractExpiredInfo 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetProjectYearlyArrearageList")
async def get_project_yearly_arrearage_list(
    request: Request,
    ProvinceCode: int = Query(None, description="省份编码"),
    ServerpartId: int = Query(None, description="服务区内码"),
    ServerpartShopIds: str = Query("", description="门店内码集合"),
    GetFromRedis: bool = Query(False, description="从缓存表取值"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同年度完成度信息"""
    try:
        user_pattern = request.headers.get("UserPattern", "")
        if user_pattern == "2000":
            ServerpartShopIds = request.headers.get("ServerpartShopIds", ServerpartShopIds) or "0"
        ProvinceCode = int(request.headers.get("ProvinceCode", str(ProvinceCode or ""))) if not ProvinceCode else ProvinceCode

        data = contract_service.get_project_yearly_arrearage(
            db, ProvinceCode, ServerpartId, ServerpartShopIds, get_from_redis=GetFromRedis)
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetProjectYearlyArrearageList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetProjectMonthlyArrearageList")
async def get_project_monthly_arrearage_list(
    request: Request,
    StatisticsYear: int = Query(None, description="统计年份"),
    ProvinceCode: int = Query(None, description="省份编码"),
    ServerpartId: int = Query(None, description="服务区内码"),
    ServerpartShopIds: str = Query("", description="门店内码集合"),
    GetFromRedis: bool = Query(False, description="从缓存表取值"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同月度完成度信息"""
    try:
        user_pattern = request.headers.get("UserPattern", "")
        if user_pattern == "2000":
            ServerpartShopIds = request.headers.get("ServerpartShopIds", ServerpartShopIds) or "0"
        ProvinceCode = int(request.headers.get("ProvinceCode", str(ProvinceCode or ""))) if not ProvinceCode else ProvinceCode

        if StatisticsYear is None:
            StatisticsYear = (datetime.now().year)

        data = contract_service.get_project_monthly_arrearage(
            db, StatisticsYear, ProvinceCode, ServerpartId, ServerpartShopIds,
            get_from_redis=GetFromRedis)
        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetProjectMonthlyArrearageList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


# ===================================================================
# 6. AddContractSupplement / SynchroContractSyn
# ===================================================================

@router.post("/Contract/AddContractSupplement")
async def add_contract_supplement(
    data: dict,
    db: DatabaseHelper = Depends(get_db)
):
    """增加合同补充协议"""
    try:
        success, result_data = contract_service.add_contract_supplement(db, data)
        if success:
            return Result.success(data=result_data, msg="操作成功")
        return Result(Result_Code=200, Result_Desc="操作失败")
    except Exception as ex:
        logger.error(f"Contract/AddContractSupplement 失败: {ex}")
        return Result.fail(msg="操作失败")


@router.post("/Contract/SynchroContractSyn")
async def synchro_contract_syn(
    data: list,
    db: DatabaseHelper = Depends(get_db)
):
    """同步合同信息同步表"""
    try:
        success = contract_service.synchro_contract_syn(db, data)
        if success:
            return Result.success(msg="同步成功")
        return Result(Result_Code=200, Result_Desc="同步失败")
    except Exception as ex:
        logger.error(f"Contract/SynchroContractSyn 同步失败: {ex}")
        return Result.fail(msg="同步失败")


# ===================================================================
# 7. CT-05 补齐路由
# ===================================================================

@router.get("/Contract/GetContractYearList")
async def get_contract_year_list(
    SortStr: str = Query("YEAR", description="排序条件"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取合同年份列表"""
    try:
        data = contract_service.get_contract_year_list(db, SortStr)
        json_list = JsonListData.create(data_list=data, total=len(data),
                                         page_index=1, page_size=len(data))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetContractYearList 查询失败: {ex}")
        return Result.fail(msg="查询失败")


@router.get("/Contract/GetShopBusinessTypeRatio")
async def get_shop_business_type_ratio(
    request: Request,
    ProvinceCode: int = Query(None, description="省份编码"),
    db: DatabaseHelper = Depends(get_db)
):
    """统计门店经营模式占比"""
    try:
        # C# 逻辑：从 Header 获取 ProvinceCode
        if ProvinceCode is None:
            hdr = request.headers.get("ProvinceCode", "")
            if hdr:
                ProvinceCode = int(hdr)
        data = contract_service.get_shop_business_type_ratio(db, ProvinceCode)
        json_list = JsonListData.create(data_list=data, total=len(data),
                                         page_index=1, page_size=len(data))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"Contract/GetShopBusinessTypeRatio 查询失败: {ex}")
        return Result.fail(msg="查询失败")
