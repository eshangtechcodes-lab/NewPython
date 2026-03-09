# -*- coding: utf-8 -*-
"""
CommercialApi - Examine 路由
对应原 CommercialApi/Controllers/ExamineController.cs
考核管理相关接口（13个接口）
"""
from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from loguru import logger
from datetime import datetime

from core.database import DatabaseHelper
from models.base import Result, JsonListData
from routers.deps import get_db

def _parse_multi_ids(raw: str) -> list:
    """解析逗号分隔的多值ID字符串，返回合法整数列表"""
    if not raw:
        return []
    ids = []
    for part in str(raw).split(","):
        part = part.strip()
        if part:
            try:
                ids.append(int(part))
            except ValueError:
                pass
    return ids

def _build_in_condition(column: str, ids: list) -> str:
    """构建 IN 或 = 条件表达式"""
    if len(ids) == 1:
        return f'{column} = {ids[0]}'
    return f'{column} IN ({",".join(str(i) for i in ids)})'

def _resolve_province_id(db, province_code: str):
    """将行政区划码(如 340000)转换为 FIELDENUM_ID（T_SERVERPART.PROVINCE_CODE 存的是内码）
    对齐 C# DictionaryHelper.GetFieldEnum("DIVISION_CODE", provinceCode)"""
    if not province_code:
        return None
    try:
        rows = db.execute_query(
            """SELECT B."FIELDENUM_ID" FROM "T_FIELDEXPLAIN" A, "T_FIELDENUM" B
                WHERE A."FIELDEXPLAIN_ID" = B."FIELDEXPLAIN_ID"
                AND A."FIELDEXPLAIN_FIELD" = 'DIVISION_CODE'
                AND B."FIELDENUM_VALUE" = ?""", [province_code])
        if rows:
            return rows[0]["FIELDENUM_ID"]
    except Exception as e:
        logger.warning(f"_resolve_province_id 转换失败: {e}")
    return province_code

router = APIRouter()


def _translate_datetime(val):
    """将 Oracle yyyyMMddHHmmss 数字格式日期转为可读字符串"""
    if val is None:
        return ""
    s = str(val).strip()
    if len(s) >= 8:
        try:
            return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
        except:
            return s
    return s


def _build_search_where(search_param: dict, prefix: str = ""):
    """构建通用搜索 WHERE 条件"""
    conditions = []
    params = []
    p = prefix + "." if prefix else ""

    # 日期范围
    date_start = search_param.get(f"{prefix.upper() if prefix else ''}EXAMINE_DATE_Start") or search_param.get("EXAMINE_DATE_Start")
    date_end = search_param.get(f"{prefix.upper() if prefix else ''}EXAMINE_DATE_End") or search_param.get("EXAMINE_DATE_End")
    if date_start:
        try:
            ds = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
            conditions.append(f"SUBSTR({p}EXAMINE_DATE,1,8) >= ?")
            params.append(ds)
        except:
            pass
    if date_end:
        try:
            de = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
            conditions.append(f"SUBSTR({p}EXAMINE_DATE,1,8) <= ?")
            params.append(de)
        except:
            pass

    # IDS 过滤
    ids = search_param.get("EXAMINE_IDS")
    if ids:
        conditions.append(f"{p}EXAMINE_ID IN ({ids})")

    types = search_param.get("EXAMINE_TYPES")
    if types:
        conditions.append(f"{p}EXAMINE_TYPE IN ({types})")

    sp_ids = search_param.get("SERVERPART_IDS")
    if sp_ids:
        conditions.append(f"{p}SERVERPART_ID IN ({sp_ids})")

    region_ids = search_param.get("SPREGIONTYPE_IDS")
    if region_ids:
        conditions.append(f"{p}SPREGIONTYPE_ID IN ({region_ids})")

    return conditions, params


# ===== 1. GetEXAMINEList =====
@router.post("/Examine/GetEXAMINEList")
async def get_examine_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取考核管理表列表"""
    try:
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        sort_str = searchModel.get("SortStr", "EXAMINE_ID DESC") or "EXAMINE_ID DESC"
        search_param = searchModel.get("SearchParameter") or {}

        conditions, params = _build_search_where(search_param)
        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        # 查询总数
        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_EXAMINE"{where_sql}'
        count_rows = db.execute_query(count_sql, params)
        total = count_rows[0]["CNT"] if count_rows else 0

        # 分页查询（SQL层分页，避免全量拉取）
        offset = (page_index - 1) * page_size
        data_sql = f'SELECT * FROM "T_EXAMINE"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
        page_params = (params if params else []) + [page_size, offset]
        page_rows = db.execute_query(data_sql, page_params)

        # 格式化日期字段
        for r in page_rows:
            r["EXAMINE_DATE"] = _translate_datetime(r.get("EXAMINE_DATE"))
            if r.get("EXAMINE_OPERATEDATE"):
                r["EXAMINE_OPERATEDATE"] = str(r["EXAMINE_OPERATEDATE"])

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXAMINEList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 2. GetEXAMINEDetail =====
@router.get("/Examine/GetEXAMINEDetail")
async def get_examine_detail(EXAMINEId: Optional[int] = Query(None, description="考核管理表内码"), db: DatabaseHelper = Depends(get_db)):
    """获取考核管理表明细"""
    try:
        sql = 'SELECT * FROM "T_EXAMINE" WHERE "EXAMINE_ID" = ?'
        rows = db.execute_query(sql, [EXAMINEId])
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        data = rows[0]
        data["EXAMINE_DATE"] = _translate_datetime(data.get("EXAMINE_DATE"))
        if data.get("EXAMINE_OPERATEDATE"):
            data["EXAMINE_OPERATEDATE"] = str(data["EXAMINE_OPERATEDATE"])
        # 补全C#模型的搜索参数字段
        data["DetailList"] = None
        data["EXAMINE_DATE_Start"] = None
        data["EXAMINE_DATE_End"] = None
        data["EXAMINE_IDS"] = None
        data["EXAMINE_TYPES"] = None
        data["SERVERPART_IDS"] = None
        data["SPREGIONTYPE_IDS"] = None

        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetEXAMINEDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 3. GetMEETINGList =====
@router.post("/Examine/GetMEETINGList")
async def get_meeting_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取晨会管理表列表"""
    try:
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        sort_str = searchModel.get("SortStr", "MEETING_ID DESC") or "MEETING_ID DESC"
        search_param = searchModel.get("SearchParameter") or {}

        conditions = []
        params = []

        # 日期范围
        date_start = search_param.get("MEETING_DATE_Start")
        date_end = search_param.get("MEETING_DATE_End")
        if date_start:
            try:
                ds = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(MEETING_DATE,1,8) >= ?")
                params.append(ds)
            except:
                pass
        if date_end:
            try:
                de = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(MEETING_DATE,1,8) <= ?")
                params.append(de)
            except:
                pass

        ids = search_param.get("MEETING_IDS")
        if ids:
            conditions.append(f"MEETING_ID IN ({ids})")

        sp_ids = search_param.get("SERVERPART_IDS")
        if sp_ids:
            conditions.append(f"SERVERPART_ID IN ({sp_ids})")

        region_ids = search_param.get("SPREGIONTYPE_IDS")
        if region_ids:
            conditions.append(f"SPREGIONTYPE_ID IN ({region_ids})")

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_MEETING"{where_sql}'
        count_rows = db.execute_query(count_sql, params)
        total = count_rows[0]["CNT"] if count_rows else 0

        offset = (page_index - 1) * page_size
        data_sql = f'SELECT * FROM "T_MEETING"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
        page_params = (params if params else []) + [page_size, offset]
        page_rows = db.execute_query(data_sql, page_params)

        for r in page_rows:
            r["MEETING_DATE"] = _translate_datetime(r.get("MEETING_DATE"))
            if r.get("MEETING_OPERATEDATE"):
                r["MEETING_OPERATEDATE"] = str(r["MEETING_OPERATEDATE"])

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMEETINGList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 4. GetMEETINGDetail =====
@router.get("/Examine/GetMEETINGDetail")
async def get_meeting_detail(MEETINGId: Optional[int] = Query(None, description="晨会管理表内码"), db: DatabaseHelper = Depends(get_db)):
    """获取晨会管理表明细"""
    try:
        sql = 'SELECT * FROM "T_MEETING" WHERE "MEETING_ID" = ?'
        rows = db.execute_query(sql, [MEETINGId])
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        data = rows[0]
        data["MEETING_DATE"] = _translate_datetime(data.get("MEETING_DATE"))
        if data.get("MEETING_OPERATEDATE"):
            data["MEETING_OPERATEDATE"] = str(data["MEETING_OPERATEDATE"])
        data["MEETING_DATE_Start"] = None
        data["MEETING_DATE_End"] = None
        data["MEETING_IDS"] = None
        data["SERVERPART_IDS"] = None
        data["SPREGIONTYPE_IDS"] = None

        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetMEETINGDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 5. GetPATROLList =====
@router.post("/Examine/GetPATROLList")
async def get_patrol_list(searchModel: dict = None, db: DatabaseHelper = Depends(get_db)):
    """获取日常巡检表列表"""
    try:
        searchModel = searchModel or {}
        page_index = searchModel.get("PageIndex", 1) or 1
        page_size = searchModel.get("PageSize", 20) or 20
        sort_str = searchModel.get("SortStr", "PATROL_ID DESC") or "PATROL_ID DESC"
        search_param = searchModel.get("SearchParameter") or {}

        conditions = []
        params = []

        date_start = search_param.get("PATROL_DATE_Start")
        date_end = search_param.get("PATROL_DATE_End")
        if date_start:
            try:
                ds = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(PATROL_DATE,1,8) >= ?")
                params.append(ds)
            except:
                pass
        if date_end:
            try:
                de = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(PATROL_DATE,1,8) <= ?")
                params.append(de)
            except:
                pass

        ids = search_param.get("PATROL_IDS")
        if ids:
            conditions.append(f"PATROL_ID IN ({ids})")

        types = search_param.get("PATROL_TYPES")
        if types:
            conditions.append(f"PATROL_TYPE IN ({types})")

        sp_ids = search_param.get("SERVERPART_IDS")
        if sp_ids:
            conditions.append(f"SERVERPART_ID IN ({sp_ids})")

        region_ids = search_param.get("SPREGIONTYPE_IDS")
        if region_ids:
            conditions.append(f"SPREGIONTYPE_ID IN ({region_ids})")

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""

        count_sql = f'SELECT COUNT(*) AS CNT FROM "T_PATROL"{where_sql}'
        count_rows = db.execute_query(count_sql, params)
        total = count_rows[0]["CNT"] if count_rows else 0

        offset = (page_index - 1) * page_size
        data_sql = f'SELECT * FROM "T_PATROL"{where_sql} ORDER BY {sort_str} LIMIT ? OFFSET ?'
        page_params = (params if params else []) + [page_size, offset]
        page_rows = db.execute_query(data_sql, page_params)

        for r in page_rows:
            r["PATROL_DATE"] = _translate_datetime(r.get("PATROL_DATE"))
            if r.get("PATROL_OPERATEDATE"):
                r["PATROL_OPERATEDATE"] = str(r["PATROL_OPERATEDATE"])

        json_list = JsonListData.create(data_list=page_rows, total=total,
                                        page_index=page_index, page_size=page_size)
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPATROLList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 6. GetPATROLDetail =====
@router.get("/Examine/GetPATROLDetail")
async def get_patrol_detail(PATROLId: Optional[int] = Query(None, description="日常巡检表内码"), db: DatabaseHelper = Depends(get_db)):
    """获取日常巡检表明细"""
    try:
        sql = 'SELECT * FROM "T_PATROL" WHERE "PATROL_ID" = ?'
        rows = db.execute_query(sql, [PATROLId])
        if not rows:
            return Result.fail(code=101, msg="查询失败，无数据返回！")

        data = rows[0]
        data["PATROL_DATE"] = _translate_datetime(data.get("PATROL_DATE"))
        if data.get("PATROL_OPERATEDATE"):
            data["PATROL_OPERATEDATE"] = str(data["PATROL_OPERATEDATE"])
        data["PATROL_DATE_Start"] = None
        data["PATROL_DATE_End"] = None
        data["PATROL_IDS"] = None
        data["PATROL_IMG"] = None
        data["PATROL_TYPES"] = None
        data["SERVERPART_IDS"] = None
        data["SPREGIONTYPE_IDS"] = None

        return Result.success(data=data, msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPATROLDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 7. WeChat_GetExamineList =====
@router.get("/Examine/WeChat_GetExamineList")
async def wechat_get_examine_list(
    SPRegionType_ID: Optional[str] = Query("", description="片区内码，多个用逗号隔开"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码，多个用逗号隔开"),
    SearchStartDate: Optional[str] = Query("", description="考核日期（开始时间）"),
    SearchEndDate: Optional[str] = Query("", description="考核日期（结束时间）"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取小程序考核列表"""
    try:
        conditions = []
        params = []

        if SPRegionType_ID:
            conditions.append(f"SPREGIONTYPE_ID IN ({SPRegionType_ID})")
        if Serverpart_ID:
            conditions.append(f"SERVERPART_ID IN ({Serverpart_ID})")
        if SearchStartDate:
            try:
                ds = datetime.strptime(SearchStartDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(EXAMINE_DATE,1,8) >= ?")
                params.append(ds)
            except:
                pass
        if SearchEndDate:
            try:
                de = datetime.strptime(SearchEndDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(EXAMINE_DATE,1,8) <= ?")
                params.append(de)
            except:
                pass

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f'SELECT * FROM "T_EXAMINE"{where_sql} ORDER BY EXAMINE_SCORE, SPREGIONTYPE_NAME, SERVERPART_NAME, EXAMINE_DATE DESC LIMIT 200'
        rows = db.execute_query(sql, params)

        for r in rows:
            r["EXAMINE_DATE"] = _translate_datetime(r.get("EXAMINE_DATE"))

        # 按服务区分组 → 按方位分组
        from collections import OrderedDict
        server_groups = OrderedDict()
        for r in rows:
            sp_name = r.get("SERVERPART_NAME", "")
            if sp_name not in server_groups:
                server_groups[sp_name] = []
            server_groups[sp_name].append(r)

        result_list = []
        regions = ["东", "南", "西", "北"]
        for sp_name, sp_rows in server_groups.items():
            region_list = []
            for region in regions:
                region_rows = [r for r in sp_rows if r.get("SERVERPART_REGION") == region]
                if region_rows:
                    region_list.append({
                        "REGION_NAME": region,
                        "SERVERPARTList": region_rows
                    })
            result_list.append({
                "SERVERPART_NAME": sp_name,
                "EXAMINE_MQUARTER": sp_rows[0].get("EXAMINE_MQUARTER", "") if sp_rows else "",
                "list": region_list
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetExamineList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 8. WeChat_GetExamineDetail =====
@router.get("/Examine/WeChat_GetExamineDetail")
async def wechat_get_examine_detail(request: Request, db: DatabaseHelper = Depends(get_db)):
    """获取小程序考核明细数据"""
    try:
        # 兼容 C# WebAPI 参数名大小写不敏感（ExamineId / EXAMINEId 均可）
        params_lower = {k.lower(): v for k, v in request.query_params.items()}
        examine_id_str = params_lower.get("examineid")
        if not examine_id_str:
            return Result.fail(code=200, msg="查询失败，请传入考核内码！")
        examine_id = int(examine_id_str)

        sql = 'SELECT * FROM "T_EXAMINEDETAIL" WHERE "EXAMINE_ID" = ? ORDER BY "EXAMINEDETAIL_ID"'
        rows = db.execute_query(sql, [examine_id])
        if not rows:
            json_list = JsonListData.create(data_list=[], total=0)
            return Result.success(data=json_list.model_dump(), msg="查询成功")

        # 按 EXAMINE_POSITION 分组
        from collections import OrderedDict
        position_groups = OrderedDict()
        for r in rows:
            pos = r.get("EXAMINE_POSITION", "")
            if pos not in position_groups:
                position_groups[pos] = []
            position_groups[pos].append(r)

        result_list = []
        for pos_name, pos_rows in position_groups.items():
            result_list.append({
                "REGION_NAME": pos_name,
                "SERVERPARTList": pos_rows
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetExamineDetail 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 9. WeChat_GetPatrolList =====
@router.get("/Examine/WeChat_GetPatrolList")
async def wechat_get_patrol_list(
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SearchStartDate: Optional[str] = Query("", description="巡检日期（开始时间）"),
    SearchEndDate: Optional[str] = Query("", description="巡检日期（结束时间）"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取小程序日常巡检列表"""
    try:
        # 与旧API一致：日期参数为空时返回999
        if not SearchStartDate and not SearchEndDate:
            return Result.fail(code=999, msg="查询失败，请传入有效的查询日期范围！")
        conditions = []
        params = []

        if SPRegionType_ID:
            conditions.append(f"SPREGIONTYPE_ID IN ({SPRegionType_ID})")
        if Serverpart_ID:
            conditions.append(f"SERVERPART_ID IN ({Serverpart_ID})")
        if SearchStartDate:
            try:
                ds = datetime.strptime(SearchStartDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(PATROL_DATE,1,8) >= ?")
                params.append(ds)
            except:
                pass
        if SearchEndDate:
            try:
                de = datetime.strptime(SearchEndDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(PATROL_DATE,1,8) <= ?")
                params.append(de)
            except:
                pass

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f'SELECT * FROM "T_PATROL"{where_sql} ORDER BY SPREGIONTYPE_NAME, SERVERPART_NAME, PATROL_DATE DESC LIMIT 200'
        rows = db.execute_query(sql, params)

        for r in rows:
            r["PATROL_DATE"] = _translate_datetime(r.get("PATROL_DATE"))

        # 按服务区分组 → 按方位分组
        from collections import OrderedDict
        server_groups = OrderedDict()
        for r in rows:
            sp_name = r.get("SERVERPART_NAME", "")
            if sp_name not in server_groups:
                server_groups[sp_name] = []
            server_groups[sp_name].append(r)

        result_list = []
        regions = ["东", "南", "西", "北"]
        for sp_name, sp_rows in server_groups.items():
            region_list = []
            for region in regions:
                region_rows = [r for r in sp_rows if r.get("SERVERPART_REGION") == region]
                if region_rows:
                    region_list.append({
                        "REGION_NAME": region,
                        "SERVERPARTList": region_rows
                    })
            result_list.append({
                "SERVERPART_NAME": sp_name,
                "list": region_list
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetPatrolList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 10. WeChat_GetMeetingList =====
@router.get("/Examine/WeChat_GetMeetingList")
async def wechat_get_meeting_list(
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    Serverpart_ID: Optional[str] = Query("", description="服务区内码"),
    SearchStartDate: Optional[str] = Query("", description="晨会日期（开始时间）"),
    SearchEndDate: Optional[str] = Query("", description="晨会日期（结束时间）"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取小程序晨会列表"""
    try:
        conditions = []
        params = []

        if SPRegionType_ID:
            conditions.append(f"SPREGIONTYPE_ID IN ({SPRegionType_ID})")
        if Serverpart_ID:
            conditions.append(f"SERVERPART_ID IN ({Serverpart_ID})")
        if SearchStartDate:
            try:
                ds = datetime.strptime(SearchStartDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(MEETING_DATE,1,8) >= ?")
                params.append(ds)
            except:
                pass
        if SearchEndDate:
            try:
                de = datetime.strptime(SearchEndDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("SUBSTR(MEETING_DATE,1,8) <= ?")
                params.append(de)
            except:
                pass

        where_sql = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        sql = f'SELECT * FROM "T_MEETING"{where_sql} ORDER BY SPREGIONTYPE_NAME, SERVERPART_NAME, MEETING_DATE DESC LIMIT 200'
        rows = db.execute_query(sql, params)

        for r in rows:
            r["MEETING_DATE"] = _translate_datetime(r.get("MEETING_DATE"))

        # 按服务区分组（晨会不按方位分组）
        from collections import OrderedDict
        server_groups = OrderedDict()
        for r in rows:
            sp_name = r.get("SERVERPART_NAME", "")
            if sp_name not in server_groups:
                server_groups[sp_name] = []
            server_groups[sp_name].append(r)

        result_list = []
        for sp_name, sp_rows in server_groups.items():
            result_list.append({
                "SERVERPART_NAME": sp_name,
                "list": [{
                    "SERVERPARTList": sp_rows
                }]
            })

        result_list.sort(key=lambda x: x.get("SERVERPART_NAME", ""))

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"WeChat_GetMeetingList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 11. GetPatrolAnalysis =====
@router.get("/Examine/GetPatrolAnalysis")
async def get_patrol_analysis(
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    StartDate: Optional[str] = Query(None, description="统计开始日期"),
    EndDate: Optional[str] = Query(None, description="统计结束日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取日常巡检分析数据"""
    try:
        conditions = ["A.\"SERVERPART_ID\" = B.\"SERVERPART_ID\"", "A.\"PATROLDAILY_STATE\" = 1"]
        params = []

        # C# 参数是 int?，多值时模型绑定失败=null，走 elif 分支
        _sp_ids = _parse_multi_ids(ServerpartId) if ServerpartId else []
        if len(_sp_ids) == 1:
            conditions.append(f'B."SERVERPART_ID" = {_sp_ids[0]}')
        elif SPRegionType_ID:
            conditions.append("B.\"SPREGIONTYPE_ID\" = ?")
            params.append(int(SPRegionType_ID))
        elif provinceCode:
            conditions.append("B.\"PROVINCE_CODE\" = ?")
            params.append(provinceCode)

        if StartDate:
            try:
                ds = datetime.strptime(StartDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("A.\"STATISTICS_DATE\" >= ?")
                params.append(ds)
            except:
                pass
        if EndDate:
            try:
                de = datetime.strptime(EndDate, "%Y-%m-%d").strftime("%Y%m%d")
                conditions.append("A.\"STATISTICS_DATE\" <= ?")
                params.append(de)
            except:
                pass

        where_sql = " WHERE " + " AND ".join(conditions)
        sql = f"""SELECT 
            SUM("PATROLTOTAL_COUNT") AS "TotalCount",
            SUM("PATROLABNORMAL_COUNT") AS "AbnormalCount",
            SUM("PATROLRECTIFY_COUNT") AS "RectifyCount"
        FROM "T_PATROLDAILY" A, "T_SERVERPART" B
        {where_sql}"""

        rows = db.execute_query(sql, params)
        if rows and rows[0].get("TotalCount") is not None:
            total = int(rows[0]["TotalCount"] or 0)
            abnormal = int(rows[0]["AbnormalCount"] or 0)
            rectify = int(rows[0]["RectifyCount"] or 0)
            un_rectify = abnormal - rectify
            complete_rate = round(100 - un_rectify * 100.0 / total, 2) if total > 0 else 0

            data = {
                "TotalCount": total,
                "AbnormalCount": abnormal,
                "RectifyCount": rectify,
                "UnRectifyCount": un_rectify,
                "CompleteRate": complete_rate
            }
            return Result.success(data=data, msg="查询成功")
        else:
            return Result.fail(code=200, msg="查询失败，无数据返回！")
    except Exception as ex:
        logger.error(f"GetPatrolAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 12. GetExamineAnalysis =====
@router.get("/Examine/GetExamineAnalysis")
async def get_examine_analysis(
    DataType: int = Query(1, description="考核类型：1月度 2季度"),
    StartMonth: Optional[str] = Query(None, description="统计开始月份"),
    EndMonth: Optional[str] = Query(None, description="统计结束月份"),
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取月度考核结果"""
    try:
        conditions = ["A.\"SERVERPART_ID\" = B.\"SERVERPART_ID\"", "A.\"EXAMINE_STATE\" = 1"]
        params = []

        conditions.append("A.\"EXAMINE_TYPE\" = ?")
        params.append(DataType)

        _sp_ids = _parse_multi_ids(ServerpartId) if ServerpartId else []
        if len(_sp_ids) == 1:
            conditions.append(f'B."SERVERPART_ID" = {_sp_ids[0]}')
        elif SPRegionType_ID:
            conditions.append("B.\"SPREGIONTYPE_ID\" = ?")
            params.append(int(SPRegionType_ID))
        elif provinceCode:
            # 行政区划码→FIELDENUM_ID 转换（T_SERVERPART.PROVINCE_CODE 存的是内码）
            province_id = _resolve_province_id(db, provinceCode)
            conditions.append(f'B."PROVINCE_CODE" = {province_id}')

        if StartMonth:
            conditions.append(f"A.\"EXAMINE_DATE\" >= ?")
            params.append(f"{StartMonth}01000000")
        if EndMonth:
            conditions.append(f"A.\"EXAMINE_DATE\" <= ?")
            params.append(f"{EndMonth}32000000")

        where_sql = " WHERE " + " AND ".join(conditions)
        sql = f"""SELECT 
            COUNT(1) AS "EXAMINE_COUNT",
            CASE WHEN "EXAMINE_SCORE" >= 90 THEN 'A' 
                 WHEN "EXAMINE_SCORE" >= 80 THEN 'B' ELSE 'C' END AS "EXAMINE_SCORE",
            CASE WHEN "EXAMINE_SCORE" >= 90 THEN '优秀' 
                 WHEN "EXAMINE_SCORE" >= 80 THEN '良好' ELSE '一般' END AS "EXAMINE_RESULT"
        FROM "T_EXAMINE" A, "T_SERVERPART" B
        {where_sql}
        GROUP BY 
            CASE WHEN "EXAMINE_SCORE" >= 90 THEN 'A' WHEN "EXAMINE_SCORE" >= 80 THEN 'B' ELSE 'C' END,
            CASE WHEN "EXAMINE_SCORE" >= 90 THEN '优秀' WHEN "EXAMINE_SCORE" >= 80 THEN '良好' ELSE '一般' END
        ORDER BY "EXAMINE_SCORE"
        """

        rows = db.execute_query(sql, params)
        result_list = []
        for r in rows:
            result_list.append({
                "name": r.get("EXAMINE_RESULT", ""),
                "value": str(r.get("EXAMINE_COUNT", "")),
                "data": r.get("EXAMINE_SCORE", "")
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetExamineAnalysis 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 13. GetExamineResultList =====
@router.get("/Examine/GetExamineResultList")
async def get_examine_result_list(
    DataType: Optional[int] = Query(None, description="考核类型：1月度 2季度"),
    StartMonth: Optional[str] = Query(None, description="统计开始月份"),
    EndMonth: Optional[str] = Query(None, description="统计结束月份"),
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取驿达看板-首页考核列表 — 对齐 C# 聚合结构（考核+嵌套明细列表）"""
    try:
        conditions = ["A.\"SERVERPART_ID\" = B.\"SERVERPART_ID\"", "A.\"EXAMINE_STATE\" = 1"]
        params = []

        if DataType is not None:
            conditions.append("A.\"EXAMINE_TYPE\" = ?")
            params.append(DataType)
        _sp_ids = _parse_multi_ids(ServerpartId) if ServerpartId else []
        if len(_sp_ids) == 1:
            conditions.append(f'B."SERVERPART_ID" = {_sp_ids[0]}')
        elif SPRegionType_ID:
            conditions.append("B.\"SPREGIONTYPE_ID\" = ?")
            params.append(int(SPRegionType_ID))
        elif provinceCode:
            # 行政区划码→FIELDENUM_ID 转换（T_SERVERPART.PROVINCE_CODE 存的是内码）
            province_id = _resolve_province_id(db, provinceCode)
            conditions.append(f'B."PROVINCE_CODE" = {province_id}')
        if StartMonth:
            conditions.append(f"A.\"EXAMINE_DATE\" >= ?")
            params.append(f"{StartMonth}01000000")
        if EndMonth:
            conditions.append(f"A.\"EXAMINE_DATE\" <= ?")
            params.append(f"{EndMonth}32000000")

        where_sql = " WHERE " + " AND ".join(conditions)

        # 对齐 C#：查考核主表 + 服务区信息（不 LEFT JOIN 明细表，按考核粒度返回）
        sql = f"""SELECT A."EXAMINE_ID", A."EXAMINE_MQUARTER", A."EXAMINE_DESC",
                A."EXAMINE_SCORE", A."EXAMINE_DATE",
                A."SPREGIONTYPE_ID", A."SPREGIONTYPE_NAME",
                A."SERVERPART_ID", A."SERVERPART_NAME",
                B."SPREGIONTYPE_INDEX", B."SERVERPART_INDEX"
            FROM "T_EXAMINE" A, "T_SERVERPART" B
            {where_sql}
            ORDER BY A."EXAMINE_SCORE" DESC"""

        rows = db.execute_query(sql, params)

        # 批量查考核明细 T_EXAMINEDETAIL，按 EXAMINE_ID 分组
        detail_map = {}
        examine_ids = [r.get("EXAMINE_ID") for r in rows if r.get("EXAMINE_ID")]
        if examine_ids:
            ids_str = ",".join(str(eid) for eid in examine_ids)
            detail_sql = f"""SELECT "EXAMINEDETAIL_ID", "EXAMINE_ID", "EXAMINE_POSITION",
                    "EXAMINE_CONTENT", "DEDUCTION_REASON", "DEDUCTION_SCORE",
                    "EXAMINEDETAIL_DESC", "EXAMINEDETAIL_URL", "EXAMINEDEAL_URL"
                FROM "T_EXAMINEDETAIL" WHERE "EXAMINE_ID" IN ({ids_str})
                ORDER BY "EXAMINEDETAIL_ID" """
            detail_rows = db.execute_query(detail_sql) or []
            for d in detail_rows:
                eid = d.get("EXAMINE_ID")
                if eid not in detail_map:
                    detail_map[eid] = []
                detail_map[eid].append({
                    "EXAMINEDETAIL_ID": d.get("EXAMINEDETAIL_ID"),
                    "EXAMINE_POSITION": d.get("EXAMINE_POSITION"),
                    "EXAMINE_CONTENT": d.get("EXAMINE_CONTENT"),
                    "DEDUCTION_REASON": d.get("DEDUCTION_REASON"),
                    "DEDUCTION_SCORE": d.get("DEDUCTION_SCORE"),
                    "EXAMINEDETAIL_DESC": d.get("EXAMINEDETAIL_DESC"),
                    "EXAMINEDETAIL_URL": d.get("EXAMINEDETAIL_URL"),
                    "EXAMINEDEAL_URL": d.get("EXAMINEDEAL_URL"),
                })

        # 组装结果 — 对齐 C# ExamineResultModel 字段结构
        result_list = []
        for r in rows:
            eid = r.get("EXAMINE_ID")
            result_list.append({
                "SPREGIONTYPE_ID": r.get("SPREGIONTYPE_ID"),
                "SPREGIONTYPE_NAME": r.get("SPREGIONTYPE_NAME"),
                "SPREGIONTYPE_INDEX": r.get("SPREGIONTYPE_INDEX"),
                "SERVERPART_ID": r.get("SERVERPART_ID"),
                "SERVERPART_INDEX": r.get("SERVERPART_INDEX"),
                "SERVERPART_NAME": r.get("SERVERPART_NAME"),
                "SERVERPART_TAG": None,
                "EXAMINE_MQUARTER": r.get("EXAMINE_MQUARTER"),
                "EXAMINE_DESC": r.get("EXAMINE_DESC"),
                "list": detail_map.get(eid, [])
            })

        json_list = JsonListData.create(data_list=result_list, total=len(result_list))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetExamineResultList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 14. GetPatrolResultList =====
@router.get("/Examine/GetPatrolResultList")
async def get_patrol_result_list(
    provinceCode: Optional[str] = Query(None, description="省份编码"),
    ServerpartId: Optional[str] = Query("", description="服务区内码"),
    SPRegionType_ID: Optional[str] = Query("", description="片区内码"),
    StartDate: Optional[str] = Query(None, description="查询开始日期"),
    EndDate: Optional[str] = Query(None, description="查询结束日期"),
    db: DatabaseHelper = Depends(get_db)
):
    """获取驿达看板-首页巡查列表"""
    try:
        conditions = [
            'A."SERVERPART_ID" = B."SERVERPART_ID"',
            'A."PATROL_ID" = C."PATROL_ID"',
            'A."PATROL_STATE" = 1',
            'C."PATROLDETAIL_STATE" <> 1'
        ]
        params = []

        _sp_ids = _parse_multi_ids(ServerpartId) if ServerpartId else []
        if len(_sp_ids) == 1:
            conditions.append(f'B."SERVERPART_ID" = {_sp_ids[0]}')
        elif SPRegionType_ID:
            conditions.append('B."SPREGIONTYPE_ID" = ?')
            params.append(int(SPRegionType_ID))
        elif provinceCode:
            conditions.append('B."PROVINCE_CODE" = ?')
            params.append(provinceCode)
        if StartDate:
            try:
                ds = datetime.strptime(StartDate, "%Y-%m-%d").strftime("%Y%m%d000000")
                conditions.append('A."PATROL_DATE" >= ?')
                params.append(ds)
            except:
                pass
        if EndDate:
            try:
                de = datetime.strptime(EndDate, "%Y-%m-%d").strftime("%Y%m%d240000")
                conditions.append('A."PATROL_DATE" <= ?')
                params.append(de)
            except:
                pass

        where_sql = " WHERE " + " AND ".join(conditions)
        sql = f"""SELECT A."PATROL_ID", A."SPREGIONTYPE_ID", A."SPREGIONTYPE_NAME",
            A."SERVERPART_ID", A."SERVERPART_NAME", A."SERVERPART_REGION",
            A."PATROL_PERSON", A."PATROL_DATE",
            C."PATROLDETAIL_ID", C."PATROL_POSITION", C."PATROL_SITUATION",
            C."PATROLDETAIL_STATE", C."RECTIFICATION_PERIOD",
            C."PATROLDETAIL_URL", C."PATROLDEAL_URL"
        FROM "T_PATROL" A, "T_SERVERPART" B, "T_PATROLDETAIL" C
        {where_sql}"""

        rows = db.execute_query(sql, params)
        for r in rows:
            r["PATROL_DATE"] = _translate_datetime(r.get("PATROL_DATE"))

        json_list = JsonListData.create(data_list=rows, total=len(rows))
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except Exception as ex:
        logger.error(f"GetPatrolResultList 查询失败: {ex}")
        return Result.fail(msg=f"查询失败{ex}")


# ===== 14. GetEvaluateResList (POST, AES) =====
@router.post("/Examine/GetEvaluateResList")
async def get_evaluate_res_list(postData: dict = None, db: DatabaseHelper = Depends(get_db)):
    """
    获取考评考核数据 (对齐 C# EvaluateHelper.GetEvaluateResList)
    数据源: Redis (db=3, key={ProvinceCode}:evaluate:{RoleType}:{StatisticsMonth})
    入参(AES加密): ProvinceCode, RoleType(1经营商户/2供应商), StatisticsMonth, ServerpartId
    """
    try:
        from core.aes_util import decrypt_post_data
        params = decrypt_post_data(postData)
        province_code = params.get("ProvinceCode", "")
        role_type = int(params.get("RoleType", 1))
        statistics_month = params.get("StatisticsMonth", "")
        serverpart_id = params.get("ServerpartId", "")
        logger.info(f"GetEvaluateResList 解密参数: ProvinceCode={province_code}, RoleType={role_type}, "
                     f"StatisticsMonth={statistics_month}, ServerpartId={serverpart_id}")

        # 从 Redis 读取考评数据 (对齐 C# RedisHelper(3, RevenueRedisConfig))
        evaluate_list = []
        try:
            import redis
            import json as json_mod
            # 读取 Redis 配置
            redis_host = "127.0.0.1"
            redis_port = 6379
            try:
                from core.config import settings
                if hasattr(settings, 'REVENUE_REDIS_HOST'):
                    redis_host = settings.REVENUE_REDIS_HOST
                if hasattr(settings, 'REVENUE_REDIS_PORT'):
                    redis_port = settings.REVENUE_REDIS_PORT
            except Exception:
                pass

            r = redis.Redis(host=redis_host, port=redis_port, db=3, decode_responses=True)
            table_name = f"{province_code}:evaluate:{role_type}:{statistics_month}"
            list_len = r.llen(table_name)
            if list_len > 0:
                # 从 Redis List 中获取所有元素
                raw_list = r.lrange(table_name, 0, -1)
                for item in raw_list:
                    try:
                        obj = json_mod.loads(item) if isinstance(item, str) else item
                        evaluate_list.append(obj)
                    except Exception:
                        continue

                # 按 ServerpartId 过滤
                if serverpart_id:
                    sp_ids = [s.strip() for s in str(serverpart_id).split(",")]
                    evaluate_list = [e for e in evaluate_list
                                     if str(e.get("ServerpartId", "")) in sp_ids]

                # 按 EvaluateScore 降序排序
                if evaluate_list:
                    evaluate_list.sort(
                        key=lambda x: float(x.get("EvaluateScore", 0) or 0),
                        reverse=True
                    )
        except Exception as redis_err:
            logger.warning(f"GetEvaluateResList Redis 读取失败: {redis_err}，返回空列表")
            evaluate_list = []

        # 返回结构对齐 C# JsonList<EvaluateModel>
        total = len(evaluate_list)
        json_list = JsonListData.create(
            data_list=evaluate_list,
            total=total,
            page_size=total if total > 0 else 10,
            page_index=1
        )
        return Result.success(data=json_list.model_dump(), msg="查询成功")
    except ValueError as ve:
        logger.error(f"GetEvaluateResList AES解密失败: {ve}")
        return Result.fail(msg=f"解密失败{ve}")
    except Exception as ex:
        return Result.fail(msg=f"查询失败{ex}")

